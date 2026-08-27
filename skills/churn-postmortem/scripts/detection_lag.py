#!/usr/bin/env python3
"""
detection_lag.py — the arithmetic half of a churn post-mortem.

Reads a set of loss-review records and computes, deterministically:

  * per-record detection / recognition / realised-lead / action lags, with the identity check
  * median and P90 detection lag by primary_reason (and overall)
  * the decision-process vs competitive split, ARR-weighted, with the coding-drift check
  * the failure-mode distribution, ARR-weighted -- data vs tooling vs routing vs capacity
  * the savability split (A+B strategy number vs C+D execution number)
  * the health-score false-negative rate (Green at T-90 and churned anyway)
  * the instrumentation backlog: signals seen >=3 times and still uninstrumented, ranked by ARR
  * the repeat-cause register: root causes on their >=2nd appearance

No network, no dependencies beyond the standard library. Dates are ISO (YYYY-MM-DD).
Missing dates are reported as UNKNOWN rather than imputed -- an imputed date becomes a threshold.

    python3 detection_lag.py sample_losses.json
    python3 detection_lag.py sample_losses.json --json
    python3 detection_lag.py sample_losses.json --min-records 3

Identity that must hold for every record:  recognition_lag + realised_lead = detection_lag
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path

FAMILY_MODES = ["absent", "uninstrumented", "unalerted", "unrouted", "unactioned", "undetectable"]

# C16 -- the real competitor is no-decision. These five are first-class causes with their own
# root-cause branches, not an "other" bucket, and they are counted against the competitive share.
NO_DECISION_FAMILY = {"no-decision", "deprioritised", "deprioritized",
                      "budget-freeze", "orphaned-renewal", "budget-loss"}
SAVABLE_LABELS = {
    "A": "should never have been sold",
    "B": "not savable, exogenous",
    "C": "savable, we did not see it",
    "D": "savable, we saw it and it did not work",
}
INVESTMENT = {
    "absent": "product instrumentation",
    "uninstrumented": "CS Ops metrics",
    "unalerted": "thresholds",
    "unrouted": "routing and ownership",
    "unactioned": "play design or capacity",
    "undetectable": "none",
}


# ---------------------------------------------------------------- helpers

def parse_date(value):
    if not value:
        return None
    try:
        y, m, d = (int(p) for p in str(value).split("-"))
        return date(y, m, d)
    except (ValueError, TypeError):
        return None


def days_between(later, earlier):
    """Signed day count, or None when either date is missing."""
    if later is None or earlier is None:
        return None
    return (later - earlier).days


def median(values):
    """Median of a numeric list. Even counts average the two middle values."""
    vals = sorted(v for v in values if v is not None)
    if not vals:
        return None
    n = len(vals)
    mid = n // 2
    if n % 2:
        return float(vals[mid])
    return (vals[mid - 1] + vals[mid]) / 2.0


def p90(values):
    """90th percentile, nearest-rank method: the value at ceil(0.9 * n)."""
    vals = sorted(v for v in values if v is not None)
    if not vals:
        return None
    n = len(vals)
    rank = -(-9 * n // 10)  # ceil(0.9 * n) using integer arithmetic
    return float(vals[min(rank, n) - 1])


def money(amount):
    return f"${amount:,.0f}"


def pct(part, whole):
    return "n/a" if not whole else f"{100.0 * part / whole:.0f}%"


def fmt(value, suffix=" d"):
    return "UNKNOWN" if value is None else f"{value:.0f}{suffix}"


# ---------------------------------------------------------------- core

def compute_record(rec):
    """Return one record's lags plus the identity check."""
    decision = parse_date(rec.get("decision_date"))
    detectable = parse_date(rec.get("earliest_detectable_date"))
    flagged = parse_date(rec.get("first_flagged_date"))
    intervened = parse_date(rec.get("first_intervention_date"))

    out = {
        "account": rec.get("account", "UNNAMED"),
        "arr_lost": float(rec.get("arr_lost") or 0),
        "primary_reason": rec.get("primary_reason", "other"),
        "failure_mode": rec.get("failure_mode", "undetectable"),
        "savable": (rec.get("savable") or "").upper()[:1],
        "health_at_t90": (rec.get("health_at_t90") or "unknown").lower(),
        "signal": rec.get("earliest_detectable_signal") or "UNKNOWN",
        "instrumented": bool(rec.get("instrumented", False)),
        "root_cause": rec.get("root_cause") or "UNKNOWN",
        "decision_process_score": rec.get("decision_process_score"),
        "competitive_score": rec.get("competitive_score"),
        "decision_owner_vacancy_days": rec.get("decision_owner_vacancy_days"),
        "competitor_confirmed_sources": int(rec.get("competitor_confirmed_sources") or 0),
        "detection_lag": days_between(decision, detectable),
        "recognition_lag": days_between(flagged, detectable),
        "realised_lead": days_between(decision, flagged),
        "action_lag": days_between(intervened, flagged),
        "save_window": days_between(parse_date(rec.get("notice_date")), decision),
    }

    identity = None
    if out["detection_lag"] is not None and out["recognition_lag"] is not None \
            and out["realised_lead"] is not None:
        identity = (out["recognition_lag"] + out["realised_lead"]) == out["detection_lag"]
    out["identity_ok"] = identity
    return out


def group_by(records, key):
    buckets = {}
    for r in records:
        buckets.setdefault(r[key], []).append(r)
    return buckets


def analyse(payload, min_records=3):
    records = [compute_record(r) for r in payload.get("losses", [])]
    total_arr = sum(r["arr_lost"] for r in records)

    reasons = []
    for reason, rows in sorted(group_by(records, "primary_reason").items(),
                               key=lambda kv: -sum(r["arr_lost"] for r in kv[1])):
        lags = [r["detection_lag"] for r in rows]
        arr = sum(r["arr_lost"] for r in rows)
        reasons.append({
            "reason": reason, "accounts": len(rows), "arr": arr,
            "share": (arr / total_arr) if total_arr else 0.0,
            "median_lag": median(lags), "p90_lag": p90(lags),
        })

    modes = []
    by_mode = group_by(records, "failure_mode")
    for mode in FAMILY_MODES:
        rows = by_mode.get(mode, [])
        arr = sum(r["arr_lost"] for r in rows)
        modes.append({
            "mode": mode, "accounts": len(rows), "arr": arr,
            "share": (arr / total_arr) if total_arr else 0.0,
            "investment": INVESTMENT[mode],
        })

    savable = {}
    for label in "ABCD":
        rows = [r for r in records if r["savable"] == label]
        savable[label] = {
            "accounts": len(rows),
            "arr": sum(r["arr_lost"] for r in rows),
            "label": SAVABLE_LABELS[label],
        }
    ab_arr = savable["A"]["arr"] + savable["B"]["arr"]
    cd_arr = savable["C"]["arr"] + savable["D"]["arr"]

    # ---- C16: decision-process vs competitive, ARR-weighted, with the refusal checks ----
    nd = [r for r in records if r["primary_reason"] in NO_DECISION_FAMILY]
    comp = [r for r in records if r["primary_reason"] == "competitive-displacement"]
    comp_unconfirmed = [r for r in comp if r["competitor_confirmed_sources"] < 2]
    nd_arr = sum(r["arr_lost"] for r in nd)
    comp_arr = sum(r["arr_lost"] for r in comp)
    missing_scores = [r["account"] for r in records
                      if r["decision_process_score"] is None or r["competitive_score"] is None]
    no_owner = [r for r in records if r["decision_owner_vacancy_days"] in (None, "UNKNOWN", "")]
    # A record scoring decision-process >=3 with competitive <=1 may not carry a competitive fix.
    process_losses = [r for r in records
                      if isinstance(r["decision_process_score"], int)
                      and isinstance(r["competitive_score"], int)
                      and r["decision_process_score"] >= 3 and r["competitive_score"] <= 1]
    miscoded_competitive = [r["account"] for r in process_losses
                            if r["primary_reason"] == "competitive-displacement"]
    decision_vs_competitive = {
        "no_decision_accounts": len(nd), "no_decision_arr": nd_arr,
        "no_decision_share": (nd_arr / total_arr) if total_arr else 0.0,
        "competitive_accounts": len(comp), "competitive_arr": comp_arr,
        "competitive_share": (comp_arr / total_arr) if total_arr else 0.0,
        "competitive_unconfirmed": [r["account"] for r in comp_unconfirmed],
        "median_decision_process": median([r["decision_process_score"] for r in records]),
        "median_competitive": median([r["competitive_score"] for r in records]),
        "missing_scores": missing_scores,
        "no_decision_owner": [r["account"] for r in no_owner],
        "process_losses": len(process_losses),
        "miscoded_competitive": miscoded_competitive,
        "drift": comp_arr > nd_arr,
    }

    green = [r for r in records if r["health_at_t90"] == "green"]

    backlog = {}
    for r in records:
        if r["instrumented"] or r["signal"] == "UNKNOWN":
            continue
        entry = backlog.setdefault(r["signal"], {"count": 0, "arr": 0.0, "modes": set()})
        entry["count"] += 1
        entry["arr"] += r["arr_lost"]
        entry["modes"].add(r["failure_mode"])
    backlog_rows = sorted(
        ({"signal": k, "count": v["count"], "arr": v["arr"],
          "modes": ", ".join(sorted(v["modes"])), "actionable": v["count"] >= min_records}
         for k, v in backlog.items()),
        key=lambda row: (-row["arr"], row["signal"]),
    )

    causes = {}
    for r in records:
        if r["root_cause"] == "UNKNOWN":
            continue
        entry = causes.setdefault(r["root_cause"], {"count": 0, "arr": 0.0})
        entry["count"] += 1
        entry["arr"] += r["arr_lost"]
    repeat_rows = sorted(
        ({"cause": k, "count": v["count"], "arr": v["arr"]}
         for k, v in causes.items() if v["count"] >= 2),
        key=lambda row: (-row["count"], -row["arr"]),
    )

    return {
        "as_of": payload.get("as_of", "UNKNOWN"),
        "period": payload.get("period", "UNKNOWN"),
        "records": records,
        "total_arr": total_arr,
        "overall": {
            "median_detection": median([r["detection_lag"] for r in records]),
            "p90_detection": p90([r["detection_lag"] for r in records]),
            "median_recognition": median([r["recognition_lag"] for r in records]),
            "median_action": median([r["action_lag"] for r in records]),
            "median_save_window": median([r["save_window"] for r in records]),
            "flagged_after_decision": sum(
                1 for r in records if r["realised_lead"] is not None and r["realised_lead"] < 0),
            "identity_failures": [r["account"] for r in records if r["identity_ok"] is False],
            "missing_dates": [r["account"] for r in records if r["detection_lag"] is None],
        },
        "reasons": reasons,
        "decision_vs_competitive": decision_vs_competitive,
        "modes": modes,
        "savable": savable,
        "ab_arr": ab_arr,
        "cd_arr": cd_arr,
        "false_negatives": [{"account": r["account"], "arr": r["arr_lost"]} for r in green],
        "backlog": backlog_rows,
        "repeat_causes": repeat_rows,
        "min_records": min_records,
    }


# ---------------------------------------------------------------- report

def render(a):
    L = []
    add = L.append
    total = a["total_arr"]
    n = len(a["records"])

    add(f"# Detection-lag report — {a['period']} · data as-of {a['as_of']}")
    add("")
    add(f"{n} losses · {money(total)} ARR lost. Medians and P90s over records with complete dates.")
    add("Median averages the two middle values; P90 is nearest-rank. Lags are in days.")
    add("")

    o = a["overall"]
    add("## Overall")
    add("| Metric | Value | What it decides |")
    add("|---|---|---|")
    add(f"| Median detection lag | {fmt(o['median_detection'])} | How much warning existed |")
    add(f"| P90 detection lag | {fmt(o['p90_detection'])} | Tune thresholds inside this, not the median |")
    add(f"| Median recognition lag | {fmt(o['median_recognition'])} | The size of the detection problem |")
    add(f"| Median action lag | {fmt(o['median_action'])} | The size of the capacity problem |")
    add(f"| Median save window (notice − decision) | {fmt(o['median_save_window'])} | The window we actually had once visible |")
    add(f"| Flagged AFTER the decision | {o['flagged_after_decision']} of {n} | Whether 'we intervene early' is true |")
    add("")
    if o["identity_failures"]:
        add(f"**Identity check failed** for: {', '.join(o['identity_failures'])} — a date is wrong. "
            "Fix the date, not the arithmetic.")
        add("")
    if o["missing_dates"]:
        add(f"**UNKNOWN detection lag** (missing dates): {', '.join(o['missing_dates'])} — "
            "excluded from every median above.")
        add("")

    d = a["decision_vs_competitive"]
    add("## Decision-process vs competitive (C16) — read before the reason mix")
    add("| Class | Accounts | ARR lost | % of lost ARR |")
    add("|---|---|---|---|")
    add(f"| No-decision family (no-decision, deprioritised, budget-freeze, orphaned-renewal, "
        f"budget-loss) | {d['no_decision_accounts']} | {money(d['no_decision_arr'])} | "
        f"{d['no_decision_share'] * 100:.0f}% |")
    add(f"| `competitive-displacement` | {d['competitive_accounts']} | "
        f"{money(d['competitive_arr'])} | {d['competitive_share'] * 100:.0f}% |")
    add("")
    add(f"Median decision-process score {fmt(d['median_decision_process'], '/5')} · "
        f"median competitive score {fmt(d['median_competitive'], '/5')}.")
    add("")
    if d["missing_scores"]:
        add("**Scores missing** (both axes are required on every record): "
            + ", ".join(d["missing_scores"]) + ". Score them before reading anything below.")
        add("")
    if d["competitive_unconfirmed"]:
        add("**Competitive code without a replacement confirmed by two independent sources**: "
            + ", ".join(d["competitive_unconfirmed"])
            + ". Move the claim to `competitor_claimed` and re-code from the no-decision family.")
        add("")
    if d["miscoded_competitive"]:
        add("**Coded competitive on a decision-process loss** (decision-process >=3, competitive "
            "<=1): " + ", ".join(d["miscoded_competitive"])
            + ". Re-code, and refuse any competitive fix for these.")
        add("")
    if d["drift"]:
        add("**Competitive ARR exceeds the no-decision family.** Named rivals are memorable and "
            "empty chairs are not, so treat this as coding drift until every competitive record "
            "clears the two-source bar.")
        add("")
    if d["no_decision_owner"]:
        add(f"**No decision owner ever identified** on {len(d['no_decision_owner'])} of {n} "
            "records: " + ", ".join(d["no_decision_owner"])
            + ". That is a live-account gap for `stakeholder-map`, not a post-mortem gap.")
        add("")
    if d["process_losses"]:
        add(f"{d['process_losses']} of {n} losses score decision-process >=3 with competitive "
            "<=1. Their fixes must be decision-process fixes — a named decision owner, a T-180 "
            "opt-out-calendar gate, a pre-wired approval path. Battlecards and price response are "
            "refused for these records.")
        add("")

    add("## Detection lag by primary reason (ARR-weighted order)")
    add("| primary_reason | Accounts | ARR lost | % of lost ARR | Median lag | P90 lag |")
    add("|---|---|---|---|---|---|")
    for r in a["reasons"]:
        add(f"| `{r['reason']}` | {r['accounts']} | {money(r['arr'])} | "
            f"{r['share'] * 100:.0f}% | {fmt(r['median_lag'])} | {fmt(r['p90_lag'])} |")
    add("")

    add("## Failure-mode distribution — where the warning was lost")
    add("| Mode | Accounts | ARR | % of lost ARR | Implied investment |")
    add("|---|---|---|---|---|")
    for m in a["modes"]:
        if not m["accounts"]:
            continue
        add(f"| `{m['mode']}` | {m['accounts']} | {money(m['arr'])} | "
            f"{m['share'] * 100:.0f}% | {m['investment']} |")
    add("")

    add("## Savability")
    add("| Verdict | Accounts | ARR | % of lost ARR |")
    add("|---|---|---|---|")
    for label in "ABCD":
        s = a["savable"][label]
        add(f"| {label} — {s['label']} | {s['accounts']} | {money(s['arr'])} | {pct(s['arr'], total)} |")
    add("")
    add(f"**A+B (strategy and qualification): {pct(a['ab_arr'], total)} · "
        f"C+D (CS execution): {pct(a['cd_arr'], total)}.**")
    if total and a["ab_arr"] / total > 0.60:
        add("Above 60% coded not-savable — either qualification is broken or the coding is. "
            "Defend the split with evidence before accepting it.")
    add("")

    fn = a["false_negatives"]
    fn_arr = sum(r["arr"] for r in fn)
    add("## Health-score false negatives (Green at T−90)")
    add(f"{len(fn)} of {n} losses ({pct(len(fn), n)} of records, {pct(fn_arr, total)} of lost ARR) "
        "were Green 90 days before the decision. Each is a scoring defect and routes to "
        "`health-score-designer` regardless of reason code.")
    if fn:
        add("")
        add("| Account | ARR |")
        add("|---|---|")
        for r in sorted(fn, key=lambda x: -x["arr"]):
            add(f"| {r['account']} | {money(r['arr'])} |")
    add("")

    add("## Instrumentation backlog — uninstrumented signals, ranked by ARR behind them")
    add(f"Actionable at >= {a['min_records']} appearances; below that a signal goes on the watch "
        "list only (never re-weight the model on N=1).")
    add("")
    add("| Signal | Appearances | ARR behind it | Failure modes | Actionable now? |")
    add("|---|---|---|---|---|")
    for row in a["backlog"]:
        add(f"| {row['signal']} | {row['count']} | {money(row['arr'])} | {row['modes']} | "
            f"{'yes' if row['actionable'] else 'watch list'} |")
    if not a["backlog"]:
        add("| — | — | — | — | every earliest-detectable signal is already instrumented |")
    add("")

    add("## Repeat-cause register — causes on their >=2nd appearance")
    add("| Root cause | Appearances | Cumulative ARR lost |")
    add("|---|---|---|")
    for row in a["repeat_causes"]:
        add(f"| {row['cause']} | {row['count']} | {money(row['arr'])} |")
    if not a["repeat_causes"]:
        add("| — | — | no cause has appeared twice yet |")
    add("")
    third = [r for r in a["repeat_causes"] if r["count"] >= 3]
    if third:
        add("**On its third appearance the finding is an unshipped fix, not a cause.** Escalate "
            "with cumulative ARR attached and do not propose a second fix: "
            + "; ".join(f"{r['cause']} ({r['count']}×, {money(r['arr'])})" for r in third))
        add("")

    add("---")
    add("Lags are measured to the **decision date**, never the churn or renewal date. "
        "Any threshold change needs a backtest against these losses **and** a control set of "
        "completed renewals at least 3× the loss set.")
    return "\n".join(L)


# ---------------------------------------------------------------- cli

def main(argv=None):
    ap = argparse.ArgumentParser(description="Detection-lag statistics for churn post-mortems.")
    ap.add_argument("path", help="JSON file of loss-review records")
    ap.add_argument("--json", action="store_true", help="emit machine-readable JSON")
    ap.add_argument("--min-records", type=int, default=3,
                    help="appearances required before a signal is actionable (default 3)")
    args = ap.parse_args(argv)

    path = Path(args.path)
    if not path.exists():
        print(f"no such file: {path}", file=sys.stderr)
        return 2
    try:
        payload = json.loads(path.read_text())
    except json.JSONDecodeError as exc:
        print(f"{path} is not valid JSON: {exc}", file=sys.stderr)
        return 2
    if not payload.get("losses"):
        print("no `losses` array in the input — nothing to compute", file=sys.stderr)
        return 2

    analysis = analyse(payload, min_records=args.min_records)
    if args.json:
        for r in analysis["records"]:
            r.pop("identity_ok", None)
        print(json.dumps(analysis, indent=2, default=str))
    else:
        print(render(analysis))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
