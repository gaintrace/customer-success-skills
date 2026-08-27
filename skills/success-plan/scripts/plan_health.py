#!/usr/bin/env python3
"""
Deterministic success-plan arithmetic: attainment, schedule variance, derived RAG status,
ownership ratio, and the plan-health signals a reviewer would otherwise recompute by hand.

Standard library only. No network. Nothing is inferred that the input does not state — a
missing baseline or an unmeasured leading indicator is reported as UNKNOWN and caps the
status at Watchpoint rather than being filled with a plausible value.

The baseline gate (C18) runs first and prints first: an objective whose baseline is missing a
value, a source or an as-of date has no writeable goal, so it is reported as a Baseline Order
outstanding rather than as a goal with a gap. An objective already at Accepted or beyond with an
incomplete baseline is a Concern, because the starting point the customer agreed to does not exist.

    python3 plan_health.py ../assets/sample-plan.json
    python3 plan_health.py ../assets/sample-plan.json --today 2026-08-27
    python3 plan_health.py ../assets/sample-plan.json --json

Status thresholds (see references/plan-review.md §5):
  On Track    leading indicator at/above threshold AND schedule variance <= 10pp
              AND no open blocking dependency
  Watchpoint  indicator below threshold for one period, OR variance 10-25pp,
              OR a blocking dependency with a dated mitigation,
              OR the leading indicator has never been measured
  Concern     outcome adverse for two consecutive periods, OR variance > 25pp,
              OR a blocking dependency with no dated mitigation,
              OR the customer owner changed and was not replaced
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from typing import Any

ON_TRACK_VARIANCE_PP = 10.0
WATCHPOINT_VARIANCE_PP = 25.0
CUSTOMER_MILESTONE_GATE = 0.40
CONFIRMATION_STALE_DAYS = 60
STALLED_PLAN_DAYS = 120
STALE_BASELINE_DAYS = 400

# C18 — a goal may not be written without all three. There is no partial credit.
BASELINE_REQUIRED = ("value", "source", "as_of")

# The label a figure from this tier must carry wherever it is printed.
TIER_LABEL = {
    "reconstruct": "[T1 · reconstructed · measured]",
    "control": "[T2 · control · comparative, not measured]",
    "attested": "[T3 · attested · stated, not measured]",
    "benchmark": "[T4 · benchmark x0.5 · estimate, not measured]",
}
MEASURED_METHODS = ("reconstruct", "control")


def d(value: str | None) -> date | None:
    if not value:
        return None
    try:
        return date.fromisoformat(value)
    except ValueError:
        return None


def pct(x: float) -> str:
    return f"{x * 100:.0f}%"


def baseline_gaps(obj: dict[str, Any]) -> list[str]:
    """Which of value / source / as_of are missing. Empty list means the goal may be written."""
    base = obj.get("baseline") or {}
    return [f for f in BASELINE_REQUIRED
            if base.get(f) in (None, "", "TBC", "tbc", "n/a", "N/A")]


def baseline_age_days(obj: dict[str, Any], today: date) -> int | None:
    as_of = d((obj.get("baseline") or {}).get("as_of"))
    return (today - as_of).days if as_of else None


def order_defects(obj: dict[str, Any]) -> list[str]:
    """A Baseline Order that cannot be filled is a sponsor decision, not a gap to absorb."""
    order = obj.get("baseline_order") or {}
    defects = []
    if not order:
        defects.append("no Baseline Order raised")
        return defects
    measurer = str(order.get("measured_by") or "").strip()
    if not measurer or measurer.lower() in ("tbc", "n/a", "the team", "ops", "support"):
        defects.append("no named customer measurer")
    if not d(order.get("pull_by")):
        defects.append("no pull_by date")
    if not str(order.get("metric_definition") or "").strip():
        defects.append("no metric definition")
    if not str(order.get("source_system_field") or "").strip():
        defects.append("no source system and field")
    return defects


def attainment(obj: dict[str, Any]) -> float | None:
    """Signed progress from baseline to target, direction-aware. None when unmeasurable."""
    base = (obj.get("baseline") or {}).get("value")
    targ = (obj.get("target") or {}).get("value")
    curr = (obj.get("current") or {}).get("value")
    if base is None or targ is None or curr is None:
        return None
    span = targ - base
    if span == 0:
        return None
    return (curr - base) / span


def elapsed(obj: dict[str, Any], today: date) -> float | None:
    start = d(obj.get("start_date"))
    end = d((obj.get("target") or {}).get("date"))
    if not start or not end or end <= start:
        return None
    return max(0.0, min(1.0, (today - start).days / (end - start).days))


def indicator_state(obj: dict[str, Any]) -> str:
    """at_threshold | below | unmeasured"""
    li = obj.get("leading_indicator") or {}
    if not li or not li.get("measured"):
        return "unmeasured"
    thr, cur = li.get("threshold"), li.get("current")
    if thr is None or cur is None:
        return "unmeasured"
    up = (li.get("direction") or "up") == "up"
    return "at_threshold" if (cur >= thr if up else cur <= thr) else "below"


def status_for(obj: dict[str, Any], today: date) -> tuple[str, str]:
    """Returns (status, the reason that decided it). Derived, never chosen."""
    state = obj.get("state")
    if state == "Verified":
        return "Closed — Verified", "customer-confirmed"
    if state == "Retired":
        return "Closed — Retired", obj.get("retired_reason", "reason not recorded")
    # C18 decides before anything else: with no baseline there is no goal to grade.
    gaps = baseline_gaps(obj)
    if gaps:
        missing = ", ".join(gaps)
        if state in ("Accepted", "Delivered"):
            return "Concern", (f"reported as {state} with an incomplete baseline (C18 violation): "
                               f"missing {missing} — the agreed starting point does not exist")
        return "Watchpoint", (f"baseline incomplete (C18): missing {missing} — Baseline Order "
                              f"outstanding, no goal is writeable for this objective")

    if state == "Proposed":
        return "Watchpoint", "not yet Accepted — objective, baseline, criteria or timeline unagreed"

    reasons: list[str] = []
    if obj.get("customer_owner_vacant"):
        return "Concern", "customer owner changed and was not replaced"
    if obj.get("blocking_dependency_open") and not obj.get("mitigation_date"):
        return "Concern", "blocking dependency with no dated mitigation"
    if int(obj.get("adverse_periods", 0)) >= 2:
        return "Concern", f"outcome adverse for {obj.get('adverse_periods')} consecutive periods"

    att, el = attainment(obj), elapsed(obj, today)
    var = None
    if att is not None and el is not None:
        var = (el - att) * 100.0
        if var > WATCHPOINT_VARIANCE_PP:
            return "Concern", f"schedule variance {var:+.0f}pp"
        if var > ON_TRACK_VARIANCE_PP:
            reasons.append(f"schedule variance {var:+.0f}pp")
    else:
        reasons.append("attainment UNKNOWN — requires baseline, current and target values")

    ind = indicator_state(obj)
    if ind == "unmeasured":
        reasons.append("leading indicator never measured")
    elif ind == "below":
        reasons.append("leading indicator below threshold")

    if obj.get("blocking_dependency_open"):
        reasons.append(f"blocking dependency, mitigation dated {obj.get('mitigation_date')}")

    if reasons:
        return "Watchpoint", "; ".join(reasons)
    return "On Track", f"indicator at threshold, variance {var:+.0f}pp, no open blocker"


def analyse(plan: dict[str, Any], today: date) -> dict[str, Any]:
    objectives = plan.get("objectives", [])
    milestones = plan.get("milestones", [])
    sub = plan.get("subscription", {}) or {}

    rows = []
    for obj in objectives:
        att, el = attainment(obj), elapsed(obj, today)
        status, reason = status_for(obj, today)
        rows.append({
            "id": obj.get("id"),
            "statement": obj.get("statement", ""),
            "state": obj.get("state"),
            "customer_owner": obj.get("customer_owner") or "UNKNOWN — requires a named customer owner",
            "vendor_owner": obj.get("vendor_owner") or "UNKNOWN — requires a named vendor owner",
            "baseline_method": (obj.get("baseline") or {}).get("method"),
            "baseline_gaps": baseline_gaps(obj),
            "baseline_tier_label": TIER_LABEL.get((obj.get("baseline") or {}).get("method")),
            "baseline_age_days": baseline_age_days(obj, today),
            "baseline_order": obj.get("baseline_order") or None,
            "order_defects": order_defects(obj) if baseline_gaps(obj) else [],
            "attainment": att,
            "elapsed": el,
            "schedule_variance_pp": None if (att is None or el is None) else (el - att) * 100.0,
            "indicator": indicator_state(obj),
            "status": status,
            "reason": reason,
        })

    n_obj = len(objectives)
    states = {s: sum(1 for o in objectives if o.get("state") == s)
              for s in ("Proposed", "Accepted", "Delivered", "Verified", "Retired")}
    baselined = [o for o in objectives if not baseline_gaps(o)]
    orders = [o for o in objectives if baseline_gaps(o)]
    measured_baseline = sum(1 for o in baselined
                            if (o.get("baseline") or {}).get("method") in MEASURED_METHODS)
    tier_counts = {k: sum(1 for o in baselined
                          if (o.get("baseline") or {}).get("method") == k) for k in TIER_LABEL}
    pull_dates = [d((o.get("baseline_order") or {}).get("pull_by")) for o in orders]
    pull_dates = sorted([x for x in pull_dates if x])
    ages = [baseline_age_days(o, today) for o in baselined]
    ages = [a for a in ages if a is not None]
    unfillable = [o for o in orders if order_defects(o)]
    goals_accepted_unbaselined = [o for o in orders
                                  if o.get("state") in ("Accepted", "Delivered", "Verified")]
    cust_ms = sum(1 for m in milestones if m.get("owner_side") == "customer")
    n_ms = len(milestones)
    overdue = [m for m in milestones
               if m.get("status") != "closed" and (d(m.get("date")) or today) < today]
    slip_twice = [m for m in milestones if int(m.get("slips", 0)) >= 2]
    closed_dates = [d(m.get("closed_date")) for m in milestones if d(m.get("closed_date"))]

    opt_out = None
    renewal, notice = d(sub.get("renewal_date")), sub.get("notice_period_days")
    if renewal and isinstance(notice, int):
        opt_out = date.fromordinal(renewal.toordinal() - notice)

    last_conf = d((plan.get("plan") or {}).get("last_customer_confirmation"))

    cov = plan.get("coverage") or {}
    weights = {"complete": 1.0, "partial": 0.5, "missing": 0.0}
    cov_score = sum(weights.get(str(v).lower(), 0.0) for v in cov.values()) if cov else 0.0
    cov_of = len(cov) if cov else 7

    return {
        "today": today.isoformat(),
        "account": plan.get("account", {}),
        "objective_rows": rows,
        "summary": {
            "objectives": n_obj,
            "states": states,
            "goals_writeable": len(baselined),
            "baseline_orders_outstanding": len(orders),
            "baseline_orders_unfillable": len(unfillable),
            "earliest_pull_by": pull_dates[0].isoformat() if pull_dates else None,
            "pull_by_overdue": sum(1 for x in pull_dates if x < today),
            "goals_written_without_baseline": len(goals_accepted_unbaselined),
            "oldest_baseline_age_days": max(ages) if ages else None,
            "stale_baselines": sum(1 for a in ages if a > STALE_BASELINE_DAYS),
            "baseline_tiers": tier_counts,
            "with_measured_baseline": measured_baseline,
            "milestones": n_ms,
            "customer_owned_milestones": cust_ms,
            "customer_owned_ratio": (cust_ms / n_ms) if n_ms else None,
            "customer_gate_met": (cust_ms / n_ms >= CUSTOMER_MILESTONE_GATE) if n_ms else False,
            "overdue_milestones": len(overdue),
            "overdue_customer_owned": sum(1 for m in overdue if m.get("owner_side") == "customer"),
            "slip_twice": len(slip_twice),
            "delivered_not_verified": states["Delivered"],
            "indicators_unmeasured": sum(1 for r in rows if r["indicator"] == "unmeasured"),
            "renewal_date": renewal.isoformat() if renewal else None,
            "notice_period_days": notice,
            "opt_out_deadline": opt_out.isoformat() if opt_out else None,
            "days_to_opt_out": (opt_out - today).days if opt_out else None,
            "days_since_customer_confirmation": (today - last_conf).days if last_conf else None,
            "days_since_milestone_closed": (today - max(closed_dates)).days if closed_dates else None,
            "coverage_score": cov_score,
            "coverage_of": cov_of,
        },
    }


def confidence_cap(coverage_ratio: float) -> str:
    if coverage_ratio >= 0.80:
        return "High"
    if coverage_ratio >= 0.60:
        return "Medium"
    if coverage_ratio >= 0.40:
        return "Low"
    return "Insufficient"


def render(a: dict[str, Any]) -> str:
    s, out = a["summary"], []
    acct = a["account"].get("name", "<account>")
    out.append(f"Success Plan Health — {acct} · as-of {a['today']}")
    out.append("=" * 78)

    dto = s["days_to_opt_out"]
    if s["opt_out_deadline"]:
        out.append(f"Renewal {s['renewal_date']} · notice {s['notice_period_days']}d · "
                   f"OPT-OUT {s['opt_out_deadline']} ({dto} days) — the governing date")
    else:
        out.append("Opt-out deadline: UNKNOWN — requires renewal_date and notice_period_days")

    st = s["states"]
    out.append(f"Objectives {s['objectives']}: Proposed {st['Proposed']} · Accepted {st['Accepted']} "
               f"· Delivered {st['Delivered']} · Verified {st['Verified']} · Retired {st['Retired']}")
    tiers = s["baseline_tiers"]
    out.append(f"BASELINE GATE (C18): {s['goals_writeable']}/{s['objectives']} objectives carry "
               f"value+source+as_of and may have a goal written · "
               f"T1 {tiers['reconstruct']} / T2 {tiers['control']} / T3 {tiers['attested']} / "
               f"T4 {tiers['benchmark']} · oldest baseline "
               f"{s['oldest_baseline_age_days'] if s['oldest_baseline_age_days'] is not None else 'n/a'} days")
    if s["baseline_orders_outstanding"]:
        out.append(f"  Baseline Orders outstanding: {s['baseline_orders_outstanding']} "
                   f"(earliest pull_by {s['earliest_pull_by'] or 'UNKNOWN — requires a date'}) "
                   f"— no SMART goal is written for these")
        for r in a["objective_rows"]:
            if not r["baseline_gaps"]:
                continue
            order = r["baseline_order"] or {}
            who = order.get("measured_by") or "UNKNOWN — requires a named customer person"
            by = order.get("pull_by") or "UNKNOWN — requires a date"
            defects = f" !! {'; '.join(r['order_defects'])}" if r["order_defects"] else ""
            out.append(f"    {r['id']}: missing {', '.join(r['baseline_gaps'])} · "
                       f"measured by {who} by {by}{defects}")
    else:
        out.append("  Baseline Orders outstanding: none — every objective carries value, source "
                   "and as-of date")
    proxies = [r for r in a["objective_rows"]
               if not r["baseline_gaps"] and r["baseline_method"] not in MEASURED_METHODS]
    if proxies:
        out.append("  Proxy baselines — this label goes beside every figure derived from them, "
                   "internally and in the customer block:")
        for r in proxies:
            out.append(f"    {r['id']}: {r['baseline_tier_label'] or 'UNKNOWN — requires a method'}")

    if s["customer_owned_ratio"] is None:
        out.append("Milestones: none supplied")
    else:
        gate = "PASS" if s["customer_gate_met"] else "FAIL — the plan is our task list"
        out.append(f"Milestones {s['milestones']}: customer-owned {s['customer_owned_milestones']} "
                   f"({pct(s['customer_owned_ratio'])}) — gate >=40% {gate}")
        out.append(f"Overdue {s['overdue_milestones']} (customer-owned {s['overdue_customer_owned']}) "
                   f"· re-dated twice or more {s['slip_twice']}")

    out.append("")
    out.append(f"{'ID':<4}{'Status':<20}{'Attain':>8}{'Elapsed':>9}{'Var pp':>8}  Reason")
    out.append("-" * 78)
    for r in a["objective_rows"]:
        att = "n/a" if r["attainment"] is None else f"{r['attainment'] * 100:.0f}%"
        el = "n/a" if r["elapsed"] is None else f"{r['elapsed'] * 100:.0f}%"
        var = "n/a" if r["schedule_variance_pp"] is None else f"{r['schedule_variance_pp']:+.0f}"
        out.append(f"{str(r['id']):<4}{r['status']:<20}{att:>8}{el:>9}{var:>8}  {r['reason']}")

    out.append("")
    flags = []
    if s["goals_written_without_baseline"]:
        flags.append(f"{s['goals_written_without_baseline']} objective(s) at Accepted or beyond with "
                     f"an incomplete baseline — C18 violation: the starting point the customer agreed "
                     f"to does not exist, so no delta can be proved at renewal")
    if s["baseline_orders_unfillable"]:
        flags.append(f"{s['baseline_orders_unfillable']} Baseline Order(s) with no named customer "
                     f"measurer, no pull date, no metric definition or no source — unfillable; raise "
                     f"each to the executive sponsor as a decision, do not substitute our own pull")
    if s["pull_by_overdue"]:
        flags.append(f"{s['pull_by_overdue']} Baseline Order(s) past their pull_by date — the goals "
                     f"they block cannot be written and the plan is measuring nothing for them")
    if s["baseline_tiers"]["benchmark"]:
        flags.append(f"{s['baseline_tiers']['benchmark']} baseline(s) on a tier-4 benchmark — label "
                     f"every derived figure [T4 · benchmark x0.5 · estimate, not measured]; it never "
                     f"enters the customer block or the renewal value case")
    if s["stale_baselines"]:
        flags.append(f"{s['stale_baselines']} baseline(s) older than {STALE_BASELINE_DAYS} days — "
                     f"re-measure or mark the period UNKNOWN; do not carry the value forward silently")
    if s["delivered_not_verified"]:
        flags.append(f"{s['delivered_not_verified']} objective(s) at Delivered but never Verified — "
                     f"work finished, value unconfirmed; not reportable as achieved")
    if s["indicators_unmeasured"]:
        flags.append(f"{s['indicators_unmeasured']} leading indicator(s) never measured — "
                     f"those objectives are Watchpoint by default, not On Track")
    if s["days_since_customer_confirmation"] is not None and \
            s["days_since_customer_confirmation"] > CONFIRMATION_STALE_DAYS:
        flags.append(f"{s['days_since_customer_confirmation']} days since the customer confirmed "
                     f"anything in this plan — treat every status as unconfirmed")
    if s["days_since_milestone_closed"] is not None and \
            s["days_since_milestone_closed"] > STALLED_PLAN_DAYS:
        flags.append(f"{s['days_since_milestone_closed']} days since any milestone closed — stalled")
    if st["Verified"] == 0 and dto is not None and dto <= 120:
        flags.append(f"zero Verified objectives with {dto} days to the opt-out deadline — "
                     f"the renewal has no evidence; escalate as a value-evidence gap")
    if s["slip_twice"]:
        flags.append(f"{s['slip_twice']} milestone(s) re-dated twice or more — re-plan the objective "
                     f"rather than issuing a third date")

    out.append("FLAGS")
    out.extend([f"  - {f}" for f in flags] or ["  - none"])

    ratio = s["coverage_score"] / s["coverage_of"] if s["coverage_of"] else 0.0
    out.append("")
    out.append(f"Coverage {s['coverage_score']:.1f} / {s['coverage_of']} ({pct(ratio)}) "
               f"-> confidence capped at {confidence_cap(ratio)}")
    out.append("Bands and derived statuses only. This is ordering, not a calibrated forecast.")
    return "\n".join(out)


def main() -> int:
    ap = argparse.ArgumentParser(description="Success-plan attainment, RAG and health signals.")
    ap.add_argument("plan", help="path to a plan JSON file (see assets/sample-plan.json)")
    ap.add_argument("--today", help="ISO date to evaluate against (default: system date)")
    ap.add_argument("--json", action="store_true", help="emit the analysis as JSON")
    args = ap.parse_args()

    try:
        plan = json.loads(open(args.plan, encoding="utf-8").read())
    except OSError as e:
        print(f"cannot read {args.plan}: {e}", file=sys.stderr)
        return 2
    except json.JSONDecodeError as e:
        print(f"{args.plan} is not valid JSON: {e}", file=sys.stderr)
        return 2

    today = d(args.today) or date.today()
    if args.today and today is None:
        print("--today must be an ISO date, e.g. 2026-08-27", file=sys.stderr)
        return 2

    result = analyse(plan, today)
    print(json.dumps(result, indent=2, default=str) if args.json else render(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
