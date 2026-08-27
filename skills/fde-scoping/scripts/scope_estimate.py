#!/usr/bin/env python3
"""
Deterministic scoping arithmetic for fde-scoping.

Computes, from one JSON file, the numbers a SOW must not get wrong by hand:

  * three-point (PERT) effort per work package: E = (O + 4M + P) / 6, sigma = (P - O) / 6
  * project totals with sigma summed in QUADRATURE, not added -- independent risks do not
    all land together, which is why padding every line item over-quotes an engagement
  * the P80 commitment line, E + 0.84 * sigma, which is the number to cap or fix
  * the presented range, its width set by the scoping stage (the cone of uncertainty),
    and the contingency reserve that stage warrants
  * duration from USABLE hours (~60% of a nominal week, R13) plus dependency wait days
    plus acceptance days
  * the opt-out deadline (renewal_date - notice_period_days, R1), the evidence window,
    the last acceptance date and the SLACK between them
  * the kickoff-readiness gate score out of 10

No network, stdlib only. Every figure it prints is reproducible from the input file.

Usage:
    python3 scope_estimate.py ../assets/sample-scope.json
    python3 scope_estimate.py my-scope.json --today 2026-09-01
    python3 scope_estimate.py my-scope.json --json

Input shape: see ../assets/sample-scope.json. Missing optional blocks are reported as
UNKNOWN rather than defaulted silently -- a guessed notice period is a guessed opt-out
deadline is a guessed last acceptance date.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from datetime import date, datetime, timedelta

# Cone of uncertainty (Boehm, Software Engineering Economics, 1981) applied by scoping stage.
# low/high multipliers on E_total; contingency is the project-level reserve for that stage.
STAGES = {
    "concept":      {"low": 0.50, "high": 2.00, "contingency": None,
                     "shape": "Quote the discovery, not the build"},
    "requirements": {"low": 0.75, "high": 1.50, "contingency": 0.25,
                     "shape": "Capped T&M"},
    "design":       {"low": 0.90, "high": 1.25, "contingency": 0.15,
                     "shape": "Fixed fee"},
    "reuse":        {"low": 0.95, "high": 1.10, "contingency": 0.10,
                     "shape": "Fixed fee"},
}

# Evidence window: days needed to accumulate value evidence and hold one review before the
# customer decides. Practitioner defaults [P] -- override in the input file.
EVIDENCE_WINDOW = {"enterprise": 90, "mid_market": 60, "tech_touch": 30}

GATE_ITEMS = [
    ("problem_statement_measurable", "Problem statement with a measurable current state, in writing"),
    ("definition_of_done_agreed",    "Definition of done agreed (end state, cadence, by whom, vs baseline)"),
    ("exclusions_acknowledged",      "Out-of-scope section acknowledged by their commercial owner"),
    ("criteria_and_acceptors",       "Every milestone has acceptance criteria and a named acceptor"),
    ("dependency_owners_named",      "Every dependency has a named customer-side owner and a date"),
    ("customer_hours_confirmed",     "Customer engineering hours confirmed by the manager who controls them"),
    ("access_requested",             "Access REQUESTED with a ticket number and an ETA (long lead)"),
    ("security_path_started",        "Security review / DPA / residency path started with a date (long lead)"),
    ("po_or_payment_path",           "PO raised or the payment path stated (long lead)"),
    ("sponsors_named_and_briefed",   "Executive sponsor named both sides and has read the plan"),
]
LONG_LEAD = {"access_requested", "security_path_started", "po_or_payment_path"}

USABLE_FRACTION = 0.60          # R13 -- usable time is ~60% of a nominal week
HOURS_PER_DAY = 8.0
ACCEPTANCE_DAYS_PER_MILESTONE = 5   # [P] deemed-acceptance review window
LAST_ACCEPTANCE_HEADROOM = 15       # [P] business days between last delivery and last acceptance
Z80 = 0.84                          # one-sided 80th percentile of the normal distribution


def parse_date(value: str | None) -> date | None:
    if not value:
        return None
    return datetime.strptime(value, "%Y-%m-%d").date()


def business_days_after(start: date, n: int) -> date:
    """Add n business days (Mon-Fri). Holidays are a calendar assumption the SOW states."""
    d, added = start, 0
    while added < n:
        d += timedelta(days=1)
        if d.weekday() < 5:
            added += 1
    return d


def business_days_between(a: date, b: date) -> int:
    """Signed business days from a to b. Negative when b precedes a."""
    if b < a:
        return -business_days_between(b, a)
    d, n = a, 0
    while d < b:
        d += timedelta(days=1)
        if d.weekday() < 5:
            n += 1
    return n


def pert(o: float, m: float, p: float) -> tuple[float, float]:
    return (o + 4 * m + p) / 6.0, (p - o) / 6.0


def slack_band(slack: int | None) -> str:
    if slack is None:
        return "UNKNOWN"
    if slack < 0:
        return "NEGATIVE -- the plan does not fit"
    if slack <= 4:
        return "No absorption"
    if slack <= 19:
        return "Tight"
    return "Healthy"


def compute(cfg: dict, today: date) -> dict:
    packages = cfg.get("work_packages", [])
    if not packages:
        raise SystemExit("input has no work_packages")

    rows, e_total, var_total = [], 0.0, 0.0
    for wp in packages:
        o, m, p = float(wp["optimistic"]), float(wp["most_likely"]), float(wp["pessimistic"])
        if not o <= m <= p:
            raise SystemExit(f"work package '{wp.get('name')}': need optimistic <= most_likely <= pessimistic")
        e, sd = pert(o, m, p)
        rows.append({"name": wp.get("name", "unnamed"), "o": o, "m": m, "p": p,
                     "e": round(e, 1), "sigma": round(sd, 2),
                     "owner": wp.get("owner", "UNKNOWN")})
        e_total += e
        var_total += sd ** 2

    sigma_total = math.sqrt(var_total)
    p80 = e_total + Z80 * sigma_total

    stage = cfg.get("scoping_stage", "requirements")
    if stage not in STAGES:
        raise SystemExit(f"scoping_stage must be one of {sorted(STAGES)}")
    s = STAGES[stage]

    fte = float(cfg.get("vendor_fte", 1.0))
    wait_days = sum(int(d.get("wait_days", 0)) for d in cfg.get("dependencies", []))
    milestones = int(cfg.get("milestone_count", max(1, len(packages) // 2)))
    build_days = e_total / (fte * HOURS_PER_DAY * USABLE_FRACTION)
    acceptance_days = milestones * ACCEPTANCE_DAYS_PER_MILESTONE
    duration_days = int(math.ceil(build_days + wait_days + acceptance_days))

    start = parse_date(cfg.get("planned_start")) or today
    last_delivery = business_days_after(start, duration_days)
    last_acceptance = business_days_after(last_delivery, LAST_ACCEPTANCE_HEADROOM)

    contract = cfg.get("contract", {})
    renewal = parse_date(contract.get("renewal_date"))
    notice = contract.get("notice_period_days")
    segment = contract.get("segment", "enterprise")
    evidence = int(contract.get("evidence_window_days", EVIDENCE_WINDOW.get(segment, 90)))

    opt_out = decide_by = slack = None
    if renewal and notice is not None:
        opt_out = renewal - timedelta(days=int(notice))
        decide_by = opt_out - timedelta(days=evidence)
        slack = business_days_between(last_acceptance, decide_by)

    gate = cfg.get("kickoff_gate", {})
    gate_rows = [{"key": k, "label": label, "met": bool(gate.get(k, False)),
                  "long_lead": k in LONG_LEAD} for k, label in GATE_ITEMS]
    gate_score = sum(1 for r in gate_rows if r["met"])

    return {
        "packages": rows,
        "e_total": round(e_total, 1),
        "sigma_total": round(sigma_total, 2),
        "sigma_naive_sum": round(sum(r["sigma"] for r in rows), 2),
        "p80": round(p80, 1),
        "stage": stage,
        "range_low": round(e_total * s["low"], 1),
        "range_high": round(e_total * s["high"], 1),
        "contingency_pct": s["contingency"],
        "contingency_hours": None if s["contingency"] is None else round(e_total * s["contingency"], 1),
        "shape_that_fits": s["shape"],
        "fte": fte,
        "build_days": round(build_days, 1),
        "wait_days": wait_days,
        "acceptance_days": acceptance_days,
        "duration_days": duration_days,
        "planned_start": start.isoformat(),
        "last_delivery": last_delivery.isoformat(),
        "last_acceptance": last_acceptance.isoformat(),
        "opt_out_deadline": opt_out.isoformat() if opt_out else None,
        "evidence_window_days": evidence,
        "decide_by": decide_by.isoformat() if decide_by else None,
        "slack_business_days": slack,
        "slack_band": slack_band(slack),
        "gate_rows": gate_rows,
        "gate_score": gate_score,
        "gate_verdict": "GO" if gate_score >= 8 else "HOLD -- move the kickoff and name the open items",
        "dependencies": cfg.get("dependencies", []),
    }


def render(r: dict, name: str) -> str:
    out: list[str] = []
    w = out.append
    w(f"# Scope estimate -- {name}")
    w("")
    w("## Work packages (PERT)")
    w("| Package | O | M | P | E | sigma | Owner |")
    w("|---|---|---|---|---|---|---|")
    for p in r["packages"]:
        w(f"| {p['name']} | {p['o']:g} | {p['m']:g} | {p['p']:g} | {p['e']:g} | {p['sigma']:g} | {p['owner']} |")
    w(f"| **Total** | | | | **{r['e_total']:g}** | **{r['sigma_total']:g}** (quadrature) | |")
    w("")
    w(f"Adding the sigmas instead of summing in quadrature would give {r['sigma_naive_sum']:g} -- "
      f"the over-quote that per-line padding produces.")
    w("")
    w("## Commitment")
    w("| | |")
    w("|---|---|")
    w(f"| Expected effort (E) | {r['e_total']:g} h |")
    w(f"| **P80 commitment (E + 0.84 sigma)** | **{r['p80']:g} h** -- this is the ceiling to cap or fix |")
    w(f"| Scoping stage | {r['stage']} |")
    w(f"| Range to present | {r['range_low']:g} - {r['range_high']:g} h |")
    cp = r["contingency_pct"]
    if cp is None:
        contingency = "n/a -- do not quote the build at this stage"
    else:
        contingency = f"{int(cp * 100)}% = {r['contingency_hours']:g} h"
    w(f"| Contingency (held once, at project level) | {contingency} |")
    w(f"| Commercial shape that fits | {r['shape_that_fits']} |")
    w("")
    w("## Duration (R13 -- usable hours, not nominal)")
    w("| | |")
    w("|---|---|")
    w(f"| Vendor FTE | {r['fte']:g} |")
    w(f"| Build days = E / (FTE x 8 x 0.60) | {r['build_days']:g} |")
    w(f"| Dependency wait days | {r['wait_days']} |")
    w(f"| Acceptance review days | {r['acceptance_days']} |")
    w(f"| **Duration** | **{r['duration_days']} business days** |")
    w(f"| Planned start | {r['planned_start']} |")
    w(f"| Last delivery | {r['last_delivery']} |")
    w(f"| **Last acceptance** (+{LAST_ACCEPTANCE_HEADROOM} business days) | **{r['last_acceptance']}** |")
    w("")
    w("## Renewal linkage (R1 -- opt-out calendar) [INTERNAL]")
    if r["opt_out_deadline"] is None:
        w("**UNKNOWN -- requires `renewal_date` and `notice_period_days`.** Without both, the last "
          "acceptance date cannot be tested against the opt-out deadline and every date below is a "
          "floor, not a commitment.")
    else:
        w("| | |")
        w("|---|---|")
        w(f"| Opt-out deadline (renewal - notice) | {r['opt_out_deadline']} |")
        w(f"| Evidence window | {r['evidence_window_days']} days |")
        w(f"| Customer decides by | {r['decide_by']} |")
        w(f"| **Slack** (decide_by - last acceptance) | **{r['slack_business_days']} business days "
          f"-- {r['slack_band']}** |")
        if r["slack_business_days"] is not None and r["slack_business_days"] < 0:
            w("")
            w("**The plan does not fit.** Say so in the first five lines. Choose explicitly: cut to a "
              "smaller first outcome, move the gate by re-terming, or accept a renewal decided on "
              "unaccepted work. Never re-baseline quietly.")
    w("")
    w("## Kickoff-readiness gate")
    w("| Item | Met | Long lead |")
    w("|---|---|---|")
    for g in r["gate_rows"]:
        w(f"| {g['label']} | {'yes' if g['met'] else 'NO'} | {'yes' if g['long_lead'] else ''} |")
    w(f"")
    w(f"**Score {r['gate_score']}/10 -- {r['gate_verdict']}**")
    missing_long = [g["label"] for g in r["gate_rows"] if g["long_lead"] and not g["met"]]
    if missing_long:
        w("")
        w("Long-lead items still open (R19 -- these take weeks and sit outside your control): "
          + "; ".join(missing_long))
    if r["dependencies"]:
        w("")
        w("## Dependencies")
        w("| Dependency | Owner | Needed by | Wait days assumed |")
        w("|---|---|---|---|")
        for d in r["dependencies"]:
            w(f"| {d.get('name','?')} | {d.get('owner','UNKNOWN')} | {d.get('needed_by','UNKNOWN')} "
              f"| {d.get('wait_days',0)} |")
        unowned = [d.get("name", "?") for d in r["dependencies"]
                   if not d.get("owner") or d.get("owner") == "UNKNOWN"]
        if unowned:
            w("")
            w("**Unowned dependencies -- these are the ones that slip:** " + "; ".join(unowned))
    w("")
    w("Figures are an ordering and a commitment line, not a forecast. Every number above is "
      "reproducible from the input file.")
    return "\n".join(out)


def main() -> int:
    ap = argparse.ArgumentParser(description="PERT estimate, duration, opt-out slack and kickoff gate.")
    ap.add_argument("input", help="path to the scope JSON (see ../assets/sample-scope.json)")
    ap.add_argument("--today", help="override today's date, YYYY-MM-DD")
    ap.add_argument("--json", action="store_true", help="emit raw JSON instead of a report")
    args = ap.parse_args()

    today = parse_date(args.today) or date.today()
    with open(args.input, encoding="utf-8") as fh:
        cfg = json.load(fh)

    result = compute(cfg, today)
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(render(result, cfg.get("engagement", args.input)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
