#!/usr/bin/env python3
"""
Deterministic advocacy readiness scoring, disqualifier evaluation, ladder ceilings, pool-cap
accounting and rotation ranking for the `customer-advocacy` skill.

Why a script: readiness is a weighted mean over seven families with renormalisation for missing
data, the caps are date arithmetic over a rolling 12-month window, and the routing score subtracts
two penalties. A model doing that in prose across fifteen candidates drifts — usually towards
"they're all available". This produces the same shortlist every time and shows every step.

What it does NOT do: decide anything. It scores, gates, ranks and totals. Whether the fit cell is
honest, whether the champion really has standing, what to offer in return and how to word the ask
are judgement.

Usage
-----
    python3 advocacy_score.py sample_pool.json
    python3 advocacy_score.py sample_pool.json --json
    python3 advocacy_score.py sample_pool.json --explain MERIDIAN
    python3 advocacy_score.py sample_pool.json --rung 8 --cell "enterprise|logistics|intercompany_close|ops_exec"

Input: see scripts/sample_pool.json for a complete worked example.

Nulls matter. A family score of `null` means NOT MEASURED — it is excluded from the weighted mean
and reported as missing coverage. It is never treated as zero, because a data gap must not
manufacture a false negative and quietly shrink the pool.

No network. Standard library only.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date, datetime, timedelta
from typing import Any

# --------------------------------------------------------------------------------------
# Model constants. These mirror SKILL.md and references/readiness-rubric.md.
# Change them together or the artifact stops matching the script.
# --------------------------------------------------------------------------------------

FAMILIES = [
    "product_usage",
    "commercial",
    "relationship",
    "support",
    "sentiment",
    "billing",
    "firmographic",
]

FAMILY_LABEL = {
    "product_usage": "Product usage & adoption",
    "commercial": "Commercial & contract",
    "relationship": "Relationship & engagement",
    "support": "Support & reliability",
    "sentiment": "Sentiment & VoC",
    "billing": "Billing & payment",
    "firmographic": "Firmographic & external",
}

WEIGHTS: dict[str, dict[str, int]] = {
    "enterprise": {"product_usage": 20, "commercial": 15, "relationship": 22,
                   "support": 15, "sentiment": 13, "billing": 5, "firmographic": 10},
    "plg": {"product_usage": 30, "commercial": 12, "relationship": 8,
            "support": 15, "sentiment": 22, "billing": 8, "firmographic": 5},
    "consumption": {"product_usage": 28, "commercial": 17, "relationship": 18,
                    "support": 15, "sentiment": 10, "billing": 5, "firmographic": 7},
}

# Readiness bands -> highest rung the band alone permits.
BANDS = [
    (80, "Ready", 10),
    (60, "Ready with limits", 5),
    (40, "Not yet", 2),
    (0, "Not a candidate", 0),
]

# Cost of each rung against the 3-per-12-months cap (readiness-rubric / pool-management).
RUNG_COST = {1: 0.0, 2: 0.5, 3: 0.5, 4: 0.5, 5: 1.0, 6: 1.0, 7: 1.5, 8: 0.5, 9: 0.0, 10: 0.0}
RUNG_LABEL = {
    1: "survey", 2: "testimonial", 3: "review", 4: "logo", 5: "case study",
    6: "webinar", 7: "conference", 8: "reference call", 9: "advisory board",
    10: "co-development",
}
RUNG_MIN_READINESS = {1: 40, 2: 40, 3: 55, 4: 55, 5: 65, 6: 70, 7: 75, 8: 75, 9: 85, 10: 85}

# Pool caps. Library conventions [P], not measured benchmarks.
CAP_ASKS_12M = 3.0
CAP_REF_CALLS_YEAR = 4
CAP_REF_CALLS_QUARTER = 1
REST_DAYS = 45
DECLINE_FREEZE_DAYS = 90

# Business models cap the ladder regardless of readiness.
MODEL_CEILING = {"enterprise": 10, "consumption": 8, "plg": 3, "regulated": 9, "partner": 8}


def _d(value: Any) -> date | None:
    if not value:
        return None
    if isinstance(value, date):
        return value
    return datetime.strptime(str(value)[:10], "%Y-%m-%d").date()


def _days(a: date | None, b: date) -> int | None:
    return None if a is None else (b - a).days


# --------------------------------------------------------------------------------------
# Readiness
# --------------------------------------------------------------------------------------

def readiness(cand: dict, profile: str) -> dict:
    """Weighted mean over families WITH DATA. Missing families are excluded, never zeroed."""
    weights = WEIGHTS[profile]
    scored, missing, total_w, acc = [], [], 0, 0.0
    for fam in FAMILIES:
        val = cand.get("families", {}).get(fam)
        if val is None:
            missing.append(fam)
            continue
        w = weights[fam]
        acc += float(val) * w
        total_w += w
        scored.append({"family": fam, "score": float(val), "weight": w,
                       "contribution": round(float(val) * w / 100.0, 2)})
    score = round(acc / total_w, 1) if total_w else 0.0
    coverage = round(len(scored) / len(FAMILIES), 3)
    band, band_ceiling = next((b, c) for cut, b, c in BANDS if score >= cut)
    return {
        "score": score, "band": band, "band_ceiling": band_ceiling,
        "breakdown": scored, "missing_families": missing,
        "coverage": coverage, "renormalised": bool(missing),
        "weight_denominator": total_w,
    }


def confidence(coverage: float) -> str:
    """Confidence never exceeds coverage (R23)."""
    if coverage >= 0.80:
        return "High"
    if coverage >= 0.60:
        return "Medium"
    if coverage >= 0.40:
        return "Low"
    return "Insufficient"


# --------------------------------------------------------------------------------------
# Disqualifiers — decisions, not indicators. Most restrictive ceiling wins.
# --------------------------------------------------------------------------------------

def disqualifiers(cand: dict, today: date) -> list[dict]:
    out: list[dict] = []

    def fire(code: str, ceiling: int, why: str, clears: date | str | None) -> None:
        out.append({"code": code, "ceiling": ceiling, "why": why,
                    "clears": str(clears) if clears else "—"})

    band = (cand.get("risk_band") or "").lower()
    if band in {"at_risk", "high_risk", "critical"}:
        fire("D1", 0, f"churn-risk band {band}", "Watch or better, sustained 30 days")
    elif band == "":
        out.append({"code": "D1?", "ceiling": 10,
                    "why": "risk_band UNKNOWN — requires a churn-risk run", "clears": "—"})

    if cand.get("open_p1"):
        fire("D2", 1, "open P1/Sev-1 or live escalation", "closed + 30 days")
    else:
        closed = _d(cand.get("last_p1_closed_on"))
        n = _days(closed, today)
        if n is not None and n < 30:
            fire("D2", 1, f"P1 closed {n}d ago", closed + timedelta(days=30))

    if cand.get("billing_dispute") or (cand.get("invoice_days_overdue") or 0) > 60:
        fire("D3", 0, "invoice >60d overdue, credit hold or open dispute", "cleared or resolved")

    # "Inside the opt-out window" = within 90 days of the opt-out deadline, the point at which
    # paper and the renewal decision are live (R7). Past the deadline with nothing signed is worse.
    optout = _d(cand.get("opt_out_deadline"))
    if optout and not cand.get("renewal_signed"):
        days_out = (optout - today).days
        if days_out <= 90:
            fire("D4", 2, f"opt-out {optout} in {days_out}d, renewal unresolved",
                 "renewal signed + 14 days")

    tenure = cand.get("champion_tenure_days")
    if tenure is None:
        out.append({"code": "D5?", "ceiling": 3,
                    "why": "champion tenure UNKNOWN — requires contact history", "clears": "—"})
    elif tenure < 180:
        fire("D5", 3, f"champion {tenure}d in role", f"{180 - tenure}d more, plus one advocacy event")

    dep = _d(cand.get("champion_departed_on"))
    n = _days(dep, today)
    if n is not None and n < 90:
        fire("D6", 3, f"champion departure {n}d ago", dep + timedelta(days=90))

    if not cand.get("quantified_outcome_stated"):
        fire("D7", 3, "no quantified outcome the customer stated", "an outcome in their numbers")

    if cand.get("publicity_restricted"):
        fire("D8", 8, "no-publicity / no-logo / blanket-NDA clause", "written legal exception")
    elif cand.get("publicity_restricted") is None:
        out.append({"code": "D8?", "ceiling": 8,
                    "why": "publicity clause UNKNOWN — requires the executed MSA", "clears": "—"})

    if cand.get("quiet_period"):
        fire("D9", 4, "earnings quiet period or blackout", "the window they name")

    if cand.get("overdue_commitment_to_them"):
        fire("D15", 0, "we owe them an overdue commitment", "delivered + 14 days")

    declined = _d(cand.get("last_declined_on"))
    n = _days(declined, today)
    if n is not None and n < DECLINE_FREEZE_DAYS:
        fire("D12", 0, f"declined {n}d ago", declined + timedelta(days=DECLINE_FREEZE_DAYS))
    if (cand.get("declines_12m") or 0) >= 2:
        fire("D13", 0, f"{cand['declines_12m']} declines in 12 months (R21)",
             "two quarters + a repair conversation")

    return out


# --------------------------------------------------------------------------------------
# Caps and rotation
# --------------------------------------------------------------------------------------

def cap_state(cand: dict, today: date) -> dict:
    asks = cand.get("asks_12m") or []
    spent = sum(RUNG_COST.get(int(a.get("rung", 0)), 0.0) for a in asks
                if (_days(_d(a.get("date")), today) or 999) <= 365)
    calls_year = sum(1 for a in asks if int(a.get("rung", 0)) == 8
                     and (_days(_d(a.get("date")), today) or 999) <= 365)
    calls_quarter = sum(1 for a in asks if int(a.get("rung", 0)) == 8
                        and (_days(_d(a.get("date")), today) or 999) <= 91)
    last = max((_d(a.get("date")) for a in asks if _d(a.get("date"))), default=None)
    since = _days(last, today)
    next_eligible = (last + timedelta(days=REST_DAYS)) if last else today
    return {
        "spent_12m": round(spent, 2), "cap_12m": CAP_ASKS_12M,
        "ref_calls_year": calls_year, "ref_calls_quarter": calls_quarter,
        "last_ask": str(last) if last else "—", "days_since_last_ask": since,
        "next_eligible": str(max(next_eligible, today)),
        "open_ask": bool(cand.get("open_ask")),
    }


def cap_blocks(caps: dict, rung: int) -> list[str]:
    blocks = []
    if caps["open_ask"]:
        blocks.append("an ask is already open (R17)")
    if caps["spent_12m"] + RUNG_COST.get(rung, 0.0) > CAP_ASKS_12M:
        blocks.append(f"12-month cap: {caps['spent_12m']} of {CAP_ASKS_12M} spent")
    if rung == 8:
        if caps["ref_calls_year"] >= CAP_REF_CALLS_YEAR:
            blocks.append(f"reference calls: {caps['ref_calls_year']} of {CAP_REF_CALLS_YEAR} this year")
        if caps["ref_calls_quarter"] >= CAP_REF_CALLS_QUARTER:
            blocks.append("one reference call per quarter already used")
    d = caps["days_since_last_ask"]
    if d is not None and d < REST_DAYS:
        blocks.append(f"rest interval: {d}d since last ask, {REST_DAYS}d required")
    return blocks


def fatigue(cand: dict) -> dict:
    f = cand.get("fatigue", {})
    flags = []
    lat, base = f.get("reply_latency_h"), f.get("baseline_latency_h")
    if lat is not None and base:
        if lat >= 2 * base or lat >= 5 * 24:
            flags.append(f"reply latency {lat}h vs own baseline {base}h")
    if (cand.get("declines_12m") or 0) >= 1:
        flags.append(f"{cand['declines_12m']} decline(s) in 12 months")
    if f.get("enthusiasm_delta_pct") is not None and f["enthusiasm_delta_pct"] <= -50:
        flags.append(f"reply length down {abs(f['enthusiasm_delta_pct'])}% since first ask")
    if f.get("delegation_drift"):
        flags.append("asks now redirected to someone more junior")
    call = "ok" if len(flags) < 2 else ("rest" if len(flags) == 2 else "freeze")
    return {"flags": flags, "call": call, "penalty": 0.0 if call == "ok" else 0.5}


def fit_score(cand: dict, cell: str | None) -> float:
    if not cell:
        return 1.0
    cells = [c.lower() for c in cand.get("fit_cells", [])]
    want = cell.lower().split("|")
    for c in cells:
        parts = c.split("|")
        if parts == want:
            return 1.0
    for c in cells:
        parts = c.split("|")
        if len(parts) == len(want) and parts[0] == want[0] and parts[3:] == want[3:]:
            return 0.7
    for c in cells:
        if c.split("|")[0] == want[0]:
            return 0.4
    return 0.0


def recency_penalty(caps: dict) -> float:
    d = caps["days_since_last_ask"]
    if d is None:
        return 0.0
    if d < REST_DAYS:
        return 0.5
    if d < 90:
        return 0.25
    return 0.0


# --------------------------------------------------------------------------------------
# Assessment
# --------------------------------------------------------------------------------------

def assess(cand: dict, profile: str, today: date, rung: int, cell: str | None) -> dict:
    r = readiness(cand, profile)
    dq = disqualifiers(cand, today)
    caps = cap_state(cand, today)
    fat = fatigue(cand)

    model_ceiling = MODEL_CEILING.get(cand.get("model", profile), 10)
    ceilings = [r["band_ceiling"], model_ceiling] + [d["ceiling"] for d in dq]
    ceiling = min(ceilings)
    if r["score"] < RUNG_MIN_READINESS.get(ceiling, 0):
        ceiling = max([k for k, v in RUNG_MIN_READINESS.items() if r["score"] >= v] or [0])

    blocks = cap_blocks(caps, rung)
    fit = fit_score(cand, cell)
    routing = round((r["score"] / 100.0) * fit - recency_penalty(caps) - fat["penalty"], 3)

    eligible = ceiling >= rung and not blocks and fit > 0.0
    reasons = []
    if ceiling < rung:
        reasons.append(f"ceiling rung {ceiling} < requested rung {rung}")
    reasons += blocks
    if fit == 0.0:
        reasons.append("no fit-cell match — do not route")

    return {
        "account": cand["account"], "advocate": cand.get("advocate", "UNKNOWN — requires a named contact"),
        "readiness": r["score"], "band": r["band"],
        "coverage": r["coverage"], "confidence": confidence(r["coverage"]),
        "missing_families": [FAMILY_LABEL[f] for f in r["missing_families"]],
        "ceiling": ceiling, "ceiling_label": RUNG_LABEL.get(ceiling, "no ask"),
        "disqualifiers": dq, "caps": caps, "fatigue": fat,
        "fit": fit, "routing_score": routing,
        "eligible": eligible, "blocked_by": reasons,
        "breakdown": r["breakdown"], "renormalised": r["renormalised"],
        "weight_denominator": r["weight_denominator"],
    }


# --------------------------------------------------------------------------------------
# Reporting
# --------------------------------------------------------------------------------------

def render(results: list[dict], rung: int, cell: str | None, today: date, profile: str) -> str:
    lines: list[str] = []
    elig = [r for r in results if r["eligible"]]
    blocked = [r for r in results if not r["eligible"]]
    elig.sort(key=lambda r: -r["routing_score"])
    blocked.sort(key=lambda r: -r["readiness"])

    lines.append(f"ADVOCACY READINESS — as-of {today} · profile {profile} · "
                 f"ask = rung {rung} ({RUNG_LABEL[rung]})")
    lines.append(f"cell = {cell or 'any'}")
    lines.append(f"{len(elig)} eligible · {len(blocked)} blocked · {len(results)} assessed")
    lines.append("")
    lines.append("SHORTLIST (routing = readiness/100 x fit - recency - fatigue)")
    lines.append(f"{'#':<3}{'ACCOUNT':<14}{'ADVOCATE':<34}{'RDY':>5}{'BAND':>20}"
                 f"{'CEIL':>6}{'FIT':>6}{'ROUTE':>8}{'NEXT ELIGIBLE':>15}  CONF")
    for i, r in enumerate(elig, 1):
        lines.append(f"{i:<3}{r['account'][:13]:<14}{r['advocate'][:33]:<34}"
                     f"{r['readiness']:>5.1f}{r['band']:>20}{r['ceiling']:>6}"
                     f"{r['fit']:>6.1f}{r['routing_score']:>8.3f}"
                     f"{r['caps']['next_eligible']:>15}  {r['confidence']}")
    if not elig:
        lines.append("   (none — see blocked list; decline the request and offer an alternative)")

    lines.append("")
    lines.append("NOT ASKING — reason and clearing date on every row (R14)")
    for r in blocked:
        codes = ", ".join(f"{d['code']} {d['why']} (clears {d['clears']})" for d in r["disqualifiers"]) or "—"
        lines.append(f"  {r['account'][:13]:<14}{r['readiness']:>5.1f}  {'; '.join(r['blocked_by'])}")
        lines.append(f"  {'':14}       disqualifiers: {codes}")

    lines.append("")
    lines.append("POOL CAPS")
    lines.append(f"{'ACCOUNT':<14}{'12M SPEND':>11}{'REF CALLS/YR':>14}{'THIS QTR':>10}"
                 f"{'LAST ASK':>12}{'FATIGUE':>9}")
    for r in results:
        c = r["caps"]
        lines.append(f"{r['account'][:13]:<14}{c['spent_12m']:>7} /{CAP_ASKS_12M:>3.0f}"
                     f"{c['ref_calls_year']:>10} /{CAP_REF_CALLS_YEAR}"
                     f"{c['ref_calls_quarter']:>10}{c['last_ask']:>12}{r['fatigue']['call']:>9}")

    fat = [r for r in results if r["fatigue"]["flags"]]
    if fat:
        lines.append("")
        lines.append("FATIGUE OBSERVABLES")
        for r in fat:
            lines.append(f"  {r['account']}: {r['fatigue']['call'].upper()} — "
                         + "; ".join(r["fatigue"]["flags"]))

    gaps = [r for r in results if r["missing_families"]]
    if gaps:
        lines.append("")
        lines.append("COVERAGE GAPS — confidence is capped by these, never above them (R23)")
        for r in gaps:
            lines.append(f"  {r['account']}: {r['coverage']:.0%} coverage, confidence {r['confidence']}"
                         f" — UNKNOWN: {', '.join(r['missing_families'])}")
    lines.append("")
    lines.append("Readiness is an ordering, not a probability that they say yes (R22).")
    return "\n".join(lines)


def explain(r: dict) -> str:
    lines = [f"{r['account']} — {r['advocate']}",
             f"  readiness {r['readiness']}/100 ({r['band']}) · ceiling rung {r['ceiling']} "
             f"({r['ceiling_label']}) · confidence {r['confidence']}", ""]
    lines.append(f"  {'FAMILY':<28}{'SCORE':>7}{'WEIGHT':>8}{'CONTRIB':>9}")
    for b in r["breakdown"]:
        lines.append(f"  {FAMILY_LABEL[b['family']]:<28}{b['score']:>7.0f}"
                     f"{b['weight']:>8}{b['contribution']:>9.2f}")
    if r["renormalised"]:
        lines.append(f"  renormalised over {r['weight_denominator']} of 100 weight — "
                     f"missing: {', '.join(r['missing_families'])}")
    lines.append(f"  {'WEIGHTED':<28}{r['readiness']:>7.1f}")
    lines.append("")
    lines.append("  DISQUALIFIERS")
    for d in r["disqualifiers"] or []:
        lines.append(f"    {d['code']:<5} ceiling {d['ceiling']:<3} {d['why']} — clears {d['clears']}")
    if not r["disqualifiers"]:
        lines.append("    none fired — all fifteen evaluated")
    lines.append("")
    lines.append("  CAPS  " + json.dumps(r["caps"]))
    lines.append(f"  FIT   {r['fit']} · ROUTING {r['routing_score']}")
    lines.append(f"  {'ELIGIBLE' if r['eligible'] else 'BLOCKED: ' + '; '.join(r['blocked_by'])}")
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("path")
    ap.add_argument("--today", default=None, help="YYYY-MM-DD; defaults to the file's as_of")
    ap.add_argument("--rung", type=int, default=None, help="1-10; defaults to the file's ask_rung")
    ap.add_argument("--cell", default=None, help="segment|industry|use_case|persona")
    ap.add_argument("--profile", default=None, choices=sorted(WEIGHTS), help="weight profile")
    ap.add_argument("--explain", default=None, help="account id to show the full workings for")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    data = json.loads(open(args.path).read())
    today = _d(args.today) or _d(data.get("as_of")) or date.today()
    rung = args.rung or int(data.get("ask_rung", 8))
    cell = args.cell if args.cell is not None else data.get("fit_cell")
    profile = args.profile or data.get("weight_profile", "enterprise")
    if profile not in WEIGHTS:
        print(f"unknown weight profile '{profile}'", file=sys.stderr)
        return 2

    results = [assess(c, profile, today, rung, cell) for c in data["candidates"]]

    if args.explain:
        match = [r for r in results if r["account"].lower() == args.explain.lower()]
        if not match:
            print(f"no candidate '{args.explain}'", file=sys.stderr)
            return 2
        print(explain(match[0]))
        return 0
    if args.json:
        print(json.dumps({"as_of": str(today), "rung": rung, "cell": cell,
                          "profile": profile, "results": results}, indent=2))
        return 0
    print(render(results, rung, cell, today, profile))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
