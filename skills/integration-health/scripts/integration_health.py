#!/usr/bin/env python3
"""
Score every connector on eight health dimensions, run the silent-failure sweep, and rank
remediation by whether the customer's core workflow breaks.

    python3 integration_health.py ../assets/sample-connectors.json
    python3 integration_health.py connectors.json --today 2026-08-28 --json

Stdlib only. No network. Nothing is inferred: a field that is absent prints UNKNOWN and caps that
connector's confidence — it never scores green, and it never gets a plausible substitute. The one
value this script will assume is the notice period, which it flags loudly, because the opt-out
deadline (`renewal_date - notice_period_days`, `R1`) is the date every expiry is measured against.

Dimensions: freshness · error rate by class · latency p50/p95 · throughput · partial failure ·
schema drift · deprecation exposure · credential runway.
Silent-failure codes: S1 partial batch drop · S3 filtered records · S4 paused-not-failed ·
S5 reduced scope · S6 webhook 200-and-discard. (S2 type coercion needs distribution checks; pass
`type_assertions_failed` if your pipeline runs them.)
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date, datetime, time, timedelta
from pathlib import Path

BAND_SCORE = {"Red": 3, "Amber": 2, "Green": 1, "UNKNOWN": 3}
BAND_ORDER = {"Red": 0, "Amber": 1, "UNKNOWN": 2, "Green": 3}
DEFAULT_ROTATION_LEAD_DAYS = 21
DEFAULT_NOTICE_DAYS = 30

# Error classes that never self-heal: one occurrence is a Red, because retrying changes nothing.
HARD_CLASSES = ("auth", "schema", "permanent")


def parse_dt(v, field: str):
    """Accept a date or an ISO timestamp; return a date. Absent stays absent."""
    if not v:
        return None
    s = str(v).replace("Z", "+00:00")
    try:
        if len(s) <= 10:
            return datetime.strptime(s[:10], "%Y-%m-%d").date()
        return datetime.fromisoformat(s).date()
    except ValueError:
        raise SystemExit(f"ERROR {field}: '{v}' is not an ISO date or timestamp")


def parse_ts(v, field: str):
    """Return a timezone-naive datetime, so every comparison in this file is like-for-like."""
    if not v:
        return None
    s = str(v).replace("Z", "+00:00")
    try:
        dt = datetime.fromisoformat(s)
        return dt.replace(tzinfo=None) - (dt.utcoffset() or timedelta(0)) if dt.tzinfo else dt
    except ValueError:
        d = parse_dt(v, field)
        return datetime.combine(d, time(0, 0)) if d else None


def worst(bands: list[str]) -> str:
    return sorted(bands, key=lambda b: BAND_ORDER[b])[0] if bands else "UNKNOWN"


def band_freshness(c, now: datetime) -> tuple[str, str]:
    last = parse_ts(c.get("last_success_at"), "last_success_at")
    interval = c.get("expected_interval_minutes")
    if last is None:
        return "UNKNOWN", "UNKNOWN — requires last_success_at"
    age_min = max(0.0, (now - last).total_seconds() / 60.0)
    age_days = age_min / 1440.0
    if age_days >= 30:
        return "Red", f"{age_days:.0f}d since last success — T2 severe (>30d unrepaired)"
    if age_days >= 7:
        return "Red", f"{age_days:.0f}d since last success — T2 risk (>7d)"
    if interval in (None, 0):
        return "UNKNOWN", f"{age_days:.1f}d old; UNKNOWN — requires expected_interval_minutes"
    ratio = age_min / float(interval)
    label = f"{ratio:.1f}x expected interval ({age_min:.0f} min since last success)"
    return ("Green" if ratio <= 1.5 else "Amber" if ratio <= 3 else "Red"), label


def band_errors(c) -> tuple[str, str]:
    errs = c.get("errors_by_class")
    attempts = c.get("attempts_24h")
    if not isinstance(errs, dict):
        return "UNKNOWN", "UNKNOWN — requires errors_by_class"
    hard = {k: errs.get(k, 0) for k in HARD_CLASSES if errs.get(k, 0)}
    if hard:
        return "Red", "hard: " + ", ".join(f"{k} {v}" for k, v in hard.items())
    if not attempts:
        return "UNKNOWN", "UNKNOWN — requires attempts_24h to rate soft classes"
    val = errs.get("validation", 0) / attempts
    rl = errs.get("rate_limit", 0) / attempts
    tr = errs.get("transient", 0) / attempts
    if val > 0.001:
        return "Red", f"validation {val*100:.2f}% of attempts (>0.1% permanent record loss)"
    if c.get("rate_limited_records_dropped", 0):
        return "Red", f"{c['rate_limited_records_dropped']} records dropped at rate limit, not retried"
    if rl > 0.01 or tr > 0.05:
        return "Amber", f"rate-limit {rl*100:.2f}%, transient {tr*100:.2f}%"
    return "Green", f"validation {val*100:.2f}%, transient {tr*100:.2f}%, no hard classes"


def band_latency(c) -> tuple[str, str]:
    p50, p95, budget = c.get("latency_p50_ms"), c.get("latency_p95_ms"), c.get("latency_budget_ms")
    if p95 is None or budget in (None, 0):
        return "UNKNOWN", "UNKNOWN — requires latency_p95_ms and latency_budget_ms (their deadline)"
    ratio = p95 / float(budget)
    tail = f"p50 {p50}ms / p95 {p95}ms vs {budget}ms budget"
    if ratio > 1.0:
        return "Red", tail + " — over budget"
    # The tail rule only fires once the tail is material against the budget. A very fast connector
    # with jitter (p95 4x p50 but 24% of budget) is not a finding; flagging it trains people to
    # ignore the amber.
    if p50 and p95 > 4 * p50 and ratio > 0.5:
        return "Red", tail + " — p95 > 4x p50 and past half the budget: retry or contention"
    return ("Green" if ratio <= 0.5 else "Amber"), tail


def band_throughput(c) -> tuple[str, str]:
    exp, got = c.get("records_expected_24h"), c.get("records_succeeded_24h")
    if not exp or got is None:
        return "UNKNOWN", "UNKNOWN — requires records_expected_24h and records_succeeded_24h"
    r = got / float(exp)
    label = f"{got:,} of {exp:,} expected ({r:.2f}x)"
    if r < 0.7 or r > 1.5:
        return "Red", label
    if r < 0.9 or r > 1.1:
        return "Amber", label
    return "Green", label


def reconcile(c) -> dict:
    """submitted = succeeded + failed + unprocessed, and expected = submitted. Residuals are lost
    records, not rounding — the arithmetic is printed so a reviewer can audit it."""
    keys = ("records_expected_24h", "records_submitted_24h", "records_succeeded_24h",
            "records_failed_24h", "records_unprocessed_24h")
    if any(c.get(k) is None for k in keys):
        return {"known": False, "band": "UNKNOWN", "unaccounted": None,
                "note": "UNKNOWN — requires record counts at both ends"}
    exp, sub, suc, fail, unp = (c[k] for k in keys)
    residual = sub - (suc + fail + unp)
    shortfall = exp - sub
    unaccounted = max(0, residual) + max(0, shortfall)
    pct = unaccounted / float(exp) if exp else 0.0
    strict = bool(c.get("financial_or_regulated"))
    band = "Green" if unaccounted == 0 else ("Red" if (strict or pct > 0.001) else "Amber")
    return {"known": True, "band": band, "unaccounted": unaccounted, "residual": residual,
            "shortfall": shortfall, "pct": pct,
            "note": f"{sub:,} submitted - ({suc:,}+{fail:,}+{unp:,}) = {residual:,} residual; "
                    f"{exp:,} expected - {sub:,} submitted = {shortfall:,} shortfall"}


def band_schema(c) -> tuple[str, str]:
    exp, obs = c.get("schema_fields_expected"), c.get("schema_fields_observed")
    changes = c.get("schema_changes") or []
    if changes:
        return "Red", "; ".join(str(x) for x in changes)
    if exp is None or obs is None:
        return "UNKNOWN", "UNKNOWN — requires the agreed field contract and the observed field set"
    if obs < exp:
        return "Red", f"{exp - obs} field(s) missing vs contract — removal, rename or lost permission"
    if obs > exp:
        return "Amber", f"{obs - exp} field(s) added vs contract — additive, confirm intent"
    return "Green", f"{obs} fields, identical to contract"


def band_deprecation(c, today: date, opt_out) -> tuple[str, str, int | None]:
    sunset = parse_dt(c.get("api_sunset_date"), "api_sunset_date")
    ver = c.get("api_version") or "UNKNOWN"
    if sunset is None:
        return "UNKNOWN", f"{ver} — UNKNOWN — requires the vendor sunset date or policy", None
    days = (sunset - today).days
    before = opt_out is not None and sunset <= opt_out
    label = f"{ver} sunsets {sunset.isoformat()} ({days}d)" + (" — before opt-out" if before else "")
    if days < 0 or before:
        return "Red", label, days
    return ("Amber" if days <= 730 else "Green"), label, days


def band_credential(c, today: date) -> tuple[str, str, int | None]:
    exp = parse_dt(c.get("credential_expires"), "credential_expires")
    lead = int(c.get("rotation_lead_days") or DEFAULT_ROTATION_LEAD_DAYS)
    if exp is None:
        return "UNKNOWN", "UNKNOWN — requires credential_expires; undated is unmeasured, not safe", None
    days = (exp - today).days
    label = f"expires {exp.isoformat()} ({days}d, rotation lead {lead}d)"
    if days < lead:
        return "Red", label, days
    return ("Green" if days >= 2 * lead else "Amber"), label, days


def silent_sweep(c, rec: dict) -> list[str]:
    found = []
    if rec.get("known") and rec.get("residual", 0) > 0:
        found.append("S1")
    if c.get("type_assertions_failed"):
        found.append("S2")
    if (rec.get("known") and rec.get("shortfall", 0) > 0) or \
       (c.get("schema_fields_observed") is not None and
            c.get("schema_fields_expected") is not None and
            c["schema_fields_observed"] < c["schema_fields_expected"]):
        found.append("S3")
    re_, ro = c.get("runs_expected_24h"), c.get("runs_observed_24h")
    if re_ and ro is not None and ro < re_:
        found.append("S4")
    req, grant = c.get("scopes_required"), c.get("scopes_granted")
    if isinstance(req, list) and isinstance(grant, list) and set(req) - set(grant):
        found.append("S5")
    em, mat = c.get("events_emitted_24h"), c.get("events_materialised_24h")
    if em is not None and mat is not None and mat < em:
        found.append("S6")
    return found


def urgency(days: int | None) -> float:
    if days is None:
        return 1.0
    if days <= 14:
        return 1.5
    if days <= 45:
        return 1.3
    if days <= 90:
        return 1.15
    if days <= 180:
        return 1.0
    return 0.85


def blast_band(c, account_daily: int | None) -> int | None:
    exp = c.get("records_expected_24h")
    tot = c.get("account_records_per_day") or account_daily
    if not exp or not tot:
        return None
    share = exp / float(tot)
    return 3 if share >= 0.10 else 2 if share >= 0.01 else 1


def score(c, today: date, now: datetime, opt_out, account_daily) -> dict:
    fresh_b, fresh_n = band_freshness(c, now)
    err_b, err_n = band_errors(c)
    lat_b, lat_n = band_latency(c)
    thr_b, thr_n = band_throughput(c)
    rec = reconcile(c)
    sch_b, sch_n = band_schema(c)
    dep_b, dep_n, dep_days = band_deprecation(c, today, opt_out)
    cred_b, cred_n, cred_days = band_credential(c, today)

    bands = {"freshness": fresh_b, "errors": err_b, "latency": lat_b, "throughput": thr_b,
             "partial": rec["band"], "schema": sch_b, "deprecation": dep_b, "credential": cred_b}
    severity_band = worst(list(bands.values()))

    tier = c.get("workflow_tier")
    blast = blast_band(c, account_daily)
    detect = 2 if c.get("alerting") is False else 1 if c.get("alerting") else None
    impact = tier * blast * detect if None not in (tier, blast, detect) else None

    opt_days = (opt_out - today).days if opt_out else None
    deadlines = [d for d in (cred_days, dep_days, opt_days) if d is not None]
    earliest = min(deadlines) if deadlines else None
    urg = urgency(earliest)
    priority = round(impact * BAND_SCORE[severity_band] * urg, 1) if impact is not None else None

    return {
        "name": c.get("name", "UNNAMED"), "direction": c.get("direction", "UNKNOWN"),
        "owner_ours": c.get("owner_ours"), "owner_theirs": c.get("owner_theirs"),
        "bands": bands,
        "notes": {"freshness": fresh_n, "errors": err_n, "latency": lat_n, "throughput": thr_n,
                  "partial": rec["note"], "schema": sch_n, "deprecation": dep_n,
                  "credential": cred_n},
        "unaccounted": rec.get("unaccounted"),
        "severity": severity_band, "silent": silent_sweep(c, rec),
        "workflow_tier": tier, "blast_band": blast, "detectability": detect,
        "impact": impact, "urgency": urg, "earliest_deadline_days": earliest,
        "arr_dependent": c.get("arr_dependent"), "priority": priority,
        "unknown_dimensions": [k for k, v in bands.items() if v == "UNKNOWN"],
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="Score connectors and rank remediation.")
    ap.add_argument("file", help="JSON: {account, renewal_date, notice_period_days, connectors:[...]}")
    ap.add_argument("--today", help="ISO date to evaluate against (default: system date)")
    ap.add_argument("--now", help="ISO timestamp for freshness maths (default: the newest "
                                  "last_success_at in the file — the export is treated as taken then)")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    path = Path(a.file)
    if not path.exists():
        print(f"no such file: {path}", file=sys.stderr)
        return 2
    data = json.loads(path.read_text())

    today = parse_dt(a.today, "--today") or date.today()
    renewal = parse_dt(data.get("renewal_date"), "renewal_date")
    notice, notice_assumed = data.get("notice_period_days"), False
    if renewal is not None and notice is None:
        notice, notice_assumed = DEFAULT_NOTICE_DAYS, True
    opt_out = renewal - timedelta(days=int(notice)) if renewal else None

    conns = data.get("connectors", [])
    stamps = [parse_ts(c.get("last_success_at"), "last_success_at") for c in conns]
    stamps = [s for s in stamps if s]
    now = parse_ts(a.now, "--now") or (max(stamps) if stamps else datetime.combine(today, time(0, 0)))
    now_assumed = a.now is None and bool(stamps)
    account_daily = data.get("account_records_per_day")

    rows = [score(c, today, now, opt_out, account_daily) for c in conns]
    rows.sort(key=lambda r: (-(r["priority"] or -1),
                             r["earliest_deadline_days"] if r["earliest_deadline_days"] is not None else 10**6,
                             -(r["arr_dependent"] or 0)))
    for i, r in enumerate(rows, 1):
        r["rank"] = i

    if a.json:
        print(json.dumps({"account": data.get("account"), "today": today.isoformat(),
                          "now": now.isoformat(), "now_assumed": now_assumed,
                          "as_of": data.get("as_of"),
                          "opt_out_deadline": opt_out.isoformat() if opt_out else None,
                          "notice_assumed": notice_assumed, "connectors": rows}, indent=2))
        return 0

    counts = {b: sum(1 for r in rows if r["severity"] == b) for b in ("Red", "Amber", "Green", "UNKNOWN")}
    unacc = [r["unaccounted"] for r in rows if r["unaccounted"] is not None]

    print(f"# Integration health — {data.get('account', path.stem)}\n")
    print(f"**{len(rows)} connectors · {counts['Red']} red / {counts['Amber']} amber / "
          f"{counts['Green']} green / {counts['UNKNOWN']} unknown · "
          f"{sum(unacc):,} records unaccounted for in the last 24h "
          f"({len(unacc)} of {len(rows)} connectors reconcilable).**\n")
    if opt_out:
        print(f"Opt-out deadline **{opt_out.isoformat()}** — {(opt_out - today).days} days "
              f"(renewal {renewal.isoformat()} minus {notice} days' notice"
              + (", **notice period ASSUMED — confirm against the signed contract and put it in the "
                 "Assumptions table**" if notice_assumed else "") + "). `R1`\n")
    else:
        print("**Opt-out deadline UNKNOWN — requires `renewal_date` and `notice_period_days`.** "
              "Every deadline below is dated against today only. Do not substitute the renewal "
              "date. `R1`\n")
    if not data.get("as_of"):
        print("**As-of date UNKNOWN — requires it.** No export is current by default; anything that "
              "expired or paused since the export is invisible here.\n")
    if now_assumed:
        print(f"Freshness measured against **{now.isoformat()}**, the newest `last_success_at` in "
              f"the file. Pass `--now` with the real collection time if the export is older than "
              f"that, and record it in the Assumptions table.\n")

    print("| # | Connector | Sev | Fresh | Err | Lat | Thru | Partial | Schema | Deprec | Cred | Silent | Impact | Urg | Priority |")
    print("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
    for r in rows:
        b = r["bands"]
        s = ",".join(r["silent"]) or "—"
        imp = r["impact"] if r["impact"] is not None else "UNK"
        pri = r["priority"] if r["priority"] is not None else "UNK"
        print(f"| {r['rank']} | {r['name']} | **{r['severity']}** | {b['freshness']} | {b['errors']} "
              f"| {b['latency']} | {b['throughput']} | {b['partial']} | {b['schema']} "
              f"| {b['deprecation']} | {b['credential']} | {s} | {imp} | {r['urgency']} | **{pri}** |")

    print("\n## Why each connector scored what it did\n")
    for r in rows:
        print(f"**{r['rank']}. {r['name']}** — {r['severity']} · priority {r['priority']} "
              f"= impact {r['impact']} x severity {BAND_SCORE[r['severity']]} x urgency {r['urgency']}")
        print(f"  - owners: {r['owner_ours'] or '**UNOWNED (ours)**'} / "
              f"{r['owner_theirs'] or '**UNOWNED (theirs)**'}")
        for k, v in r["notes"].items():
            print(f"  - {k}: {r['bands'][k]} — {v}")
        if r["silent"]:
            print(f"  - **silent failures: {', '.join(r['silent'])}** — see references/silent-failures.md")
        if r["unknown_dimensions"]:
            print(f"  - **confidence capped**: {len(r['unknown_dimensions'])} of 8 dimensions "
                  f"unmeasured ({', '.join(r['unknown_dimensions'])})")
        print()

    unowned = [r["name"] for r in rows if not r["owner_theirs"] or not r["owner_ours"]]
    if unowned:
        print(f"**UNOWNED on one or both sides ({len(unowned)}):** {', '.join(unowned)}. "
              f"A connector with a credential and no name attached fails on a Tuesday morning "
              f"and nobody is paged.\n")
    silent_any = [r["name"] for r in rows if r["silent"]]
    if silent_any:
        print(f"**Silent failures found on {len(silent_any)} of {len(rows)} connectors.** These raise "
              f"no alert and generate no ticket, so ticket volume cannot detect them (`C21`). "
              f"Each needs a detector left behind, not just a fix.\n")
    print("Severity is a band, not a failure probability, and priority is an ordering rather than a "
          "forecast (`R22`). Confidence never exceeds coverage (`R23`).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
