#!/usr/bin/env python3
"""
Deterministic expansion sizing and ranking for the `expansion-finder` skill.

Why a script: expansion sizing is four different arithmetics (seats, tier, cross-sell,
consumption commit) multiplied by a four-factor ranking model. An LLM doing that in prose
across a book of business drifts, and a drifted expansion number gets quoted to a customer.
This produces the same answer every time and shows every step.

It also enforces the health gate mechanically. An account that fails the gate cannot
produce an opportunity row — it produces a refusal with the reason and the remedy.

Usage
-----
    python size_expansion.py book.json
    python size_expansion.py book.json --today 2026-08-27
    python size_expansion.py book.json --explain ACME
    python size_expansion.py book.json --json

Input: JSON list of candidate opportunities (one per account per motion).

    [
      {
        "account_id": "ACME",
        "name": "Acme Corp",
        "arr": 312500,
        "renewal_date": "2027-01-24",
        "notice_period_days": 60,
        "health_band": "secure",              // secure|watch|at_risk|high_risk|critical
        "hard_blocks": [],                    // see HARD_BLOCKS
        "cooldowns": [],                      // see COOLDOWNS — force DEFER
        "relationship": "sponsor_engaged",    // see RELATIONSHIP
        "signal_tier": "T2",                  // T1..T6
        "independent_families": 3,            // distinct signal families that fired
        "last_value_artifact_days": 34,       // days since customer-validated value evidence
        "csm_hours": 6,
        "motion": "seat",                     // seat|tier|cross_sell|commit
        "seat": { ... }                       // motion-specific block, see below
      }
    ]

Motion blocks
-------------
seat:       contracted_seats, active_users_30d, blocked_users_60d,
            net_new_users_per_month, expected_discount_pct,
            [list_price_next_tier], [ceiling_corroborated]
tier:       current_arr, included_qty, current_overage_rate,
            target_arr, target_included_qty, target_overage_rate,
            current_usage, growth_mom
cross_sell: list_price_per_unit, attach_units, expected_discount_pct,
            [cohort_attach_rate], [lift]
commit:     current_committed_arr, proposed_commit_arr, trailing_12m_overage

Missing inputs are reported as UNKNOWN and the row is not sized. Nothing is guessed.
No network access. Standard library only.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from datetime import date, datetime
from typing import Any

# --------------------------------------------------------------------------------------
# Model constants — these mirror references/sizing-models.md. Change both together.
# All priors below are PRACTITIONER DEFAULTS, not measured benchmarks. Replace them with
# your own observed win rates as soon as you have >=30 closed expansion deals per motion.
# --------------------------------------------------------------------------------------

TIER_PRIOR: dict[str, float] = {
    "T1": 0.60,  # declared intent — customer asked
    "T2": 0.45,  # constraint hit — blocked right now
    "T3": 0.30,  # constraint approaching on current trajectory
    "T4": 0.20,  # structural growth in how they use us
    "T5": 0.12,  # favourable disposition only
    "T6": 0.10,  # their world changed, our data has not
}
FAMILY_BONUS = 0.05          # per additional independent signal family beyond the first
PROPENSITY_CAP = 0.75        # no rules-based prior may exceed this

RELATIONSHIP: dict[str, tuple[float, str]] = {
    "sponsor_engaged":   (1.00, "Exec sponsor met within 90 days; economic buyer mapped"),
    "champion_only":     (0.85, "Champion active; economic buyer mapped but not met in 90d"),
    "buyer_mapped_cold": (0.70, "Economic buyer identified, no contact in 90 days"),
    "single_threaded":   (0.50, "One user-level contact carries the whole relationship"),
}

HEALTH_GATE: dict[str, float] = {
    "secure": 1.00, "watch": 0.60,
    "at_risk": 0.0, "high_risk": 0.0, "critical": 0.0,
}

HARD_BLOCKS: dict[str, str] = {
    "onboarding_incomplete":  "Implementation not live — no basis for a value claim",
    "ttfv_not_reached":       "Time-to-first-value not achieved — nothing has been proven yet",
    "open_p1":                "Open P1/Sev-1 incident",
    "open_escalation":        "Active escalation or executive complaint",
    "detractor_90d":          "NPS detractor (0-6) from the buying centre in the last 90 days",
    "past_due_30d":           "Invoice past due more than 30 days, or an open billing dispute",
    "utilisation_under_50":   "Seat utilisation below 50% — this is shelfware, not headroom",
    "downgrade_requested":    "Customer has asked to reduce — an open downgrade conversation",
    "customer_reorg":         "Layoffs, reorg, or announced budget freeze on the customer side",
    "already_entitled":       "They already pay for this capability and have never used it",
}

COOLDOWNS: dict[str, str] = {
    "post_sev1_14d":          "Within 14 days of a Sev-1 resolution",
    "post_escalation_30d":    "Within 30 days of an escalation closing",
    "post_advocacy_14d":      "Within 14 days of an advocacy or reference ask",
    "post_ask_90d":           "Within 90 days of the last expansion ask to this buyer",
    "post_price_increase_90d": "Within 90 days of an uplift taking effect",
}

VALUE_EVIDENCE_MAX_DAYS = 120   # older than this and the ask has no foundation
VALUE_STALE_FACTOR = 0.70       # applied to ranked value; the row is also marked value-first


def timing_fit(days_to_opt_out: int | None, days_to_renewal: int | None) -> tuple[float, str]:
    """Timing is scored against the OPT-OUT deadline, never the renewal date."""
    if days_to_renewal is not None and days_to_renewal < 0:
        if days_to_renewal >= -60:
            return 0.90, "Post-renewal reset window (T+0 to T+60) — the strongest clean-air window"
        return 0.85, "Mid-term, next opt-out deadline not yet computed"
    if days_to_opt_out is None:
        return 0.60, "UNKNOWN — opt-out deadline not computable; timing scored at the neutral default"
    d = days_to_opt_out
    if d > 270:
        return 0.60, f"{d}d to opt-out — budget cycle not formed; seed only"
    if d > 150:
        return 0.85, f"{d}d to opt-out — whitespace and value-evidence window"
    if d > 90:
        return 1.00, f"{d}d to opt-out — optimal; open the expansion separately from renewal terms"
    if d > 45:
        return 0.90, f"{d}d to opt-out — proposal window; co-term decision lands here"
    if d > 30:
        return 0.60, f"{d}d to opt-out — last window for a co-termed add-on"
    if d >= 0:
        return 0.20, f"{d}d to opt-out — do not introduce a new ask; defer to post-renewal"
    return 0.30, f"opt-out deadline passed {abs(d)}d ago — renewal terms are set; hold"


# --------------------------------------------------------------------------------------
# Motion sizing
# --------------------------------------------------------------------------------------

def size_seat(b: dict[str, Any], months_to_renewal: float) -> dict[str, Any]:
    need = ["contracted_seats", "active_users_30d", "blocked_users_60d", "net_new_users_per_month"]
    missing = [k for k in need if b.get(k) is None]
    if missing:
        return {"unknown": f"UNKNOWN — requires {', '.join(missing)}"}

    contracted = float(b["contracted_seats"])
    active = float(b["active_users_30d"])
    blocked = float(b["blocked_users_60d"])
    velocity = float(b["net_new_users_per_month"])
    discount = float(b.get("expected_discount_pct", 0.0))

    p_eff = b.get("effective_price_per_seat")
    p_eff = float(p_eff) if p_eff is not None else None

    util = active / contracted if contracted else 0.0
    headroom = contracted - active
    runway = (headroom / velocity) if velocity > 0 else None

    floor = max(0.0, blocked)
    projected = active + velocity * months_to_renewal
    base = max(0.0, math.ceil(projected - contracted))
    ceiling = max(0.0, math.ceil(projected + velocity * 3 - contracted))
    recommended = ceiling if b.get("ceiling_corroborated") else base
    if recommended <= 0:
        recommended = floor

    price = p_eff if p_eff is not None else None
    return {
        "utilisation": round(util, 4),
        "headroom": headroom,
        "runway_months": round(runway, 1) if runway is not None else None,
        "floor_units": floor,
        "base_units": base,
        "ceiling_units": ceiling,
        "recommended_units": recommended,
        "unit_price": price,
        "expected_discount_pct": discount,
        "list_price_next_tier": b.get("list_price_next_tier"),
        "_needs_price": price is None,
    }


def size_tier(b: dict[str, Any], months_left_in_term: float) -> dict[str, Any]:
    need = ["current_arr", "included_qty", "current_overage_rate", "target_arr",
            "target_included_qty", "target_overage_rate", "current_usage", "growth_mom"]
    missing = [k for k in need if b.get(k) is None]
    if missing:
        return {"unknown": f"UNKNOWN — requires {', '.join(missing)}"}

    a_arr, b_arr = float(b["current_arr"]), float(b["target_arr"])
    a_inc, b_inc = float(b["included_qty"]), float(b["target_included_qty"])
    a_rate, b_rate = float(b["current_overage_rate"]), float(b["target_overage_rate"])
    usage, g = float(b["current_usage"]), float(b["growth_mom"])

    tier_delta = b_arr - a_arr
    monthly_delta = tier_delta / 12.0
    indifference_usage = a_inc + (monthly_delta / a_rate if a_rate > 0 else float("inf"))

    if usage >= indifference_usage:
        months_to_cross: float | None = 0.0
    elif g > 0 and indifference_usage > 0:
        months_to_cross = math.log(indifference_usage / usage) / math.log(1 + g)
    else:
        months_to_cross = None

    a_total, b_total, schedule = a_arr, b_arr, []
    u = usage
    for m in range(1, 13):
        u = usage * ((1 + g) ** m)
        a_over = max(0.0, u - a_inc) * a_rate
        b_over = max(0.0, u - b_inc) * b_rate
        a_total += a_over
        b_total += b_over
        schedule.append({"month": m, "usage": round(u, 1),
                         "current_overage": round(a_over, 2), "target_overage": round(b_over, 2)})

    crosses_in_term = months_to_cross is not None and months_to_cross <= months_left_in_term
    return {
        "tier_delta_arr": tier_delta,
        "indifference_usage": round(indifference_usage, 1),
        "months_to_indifference": round(months_to_cross, 1) if months_to_cross is not None else None,
        "months_left_in_term": round(months_left_in_term, 1),
        "crosses_in_term": crosses_in_term,
        "current_12m_total_cost": round(a_total, 2),
        "target_12m_total_cost": round(b_total, 2),
        "customer_saving": round(a_total - b_total, 2),
        "billings_delta": round(b_total - a_total, 2),
        "schedule": schedule,
        "honest_recommendation": "upgrade" if crosses_in_term else "stay on current tier",
    }


def size_cross_sell(b: dict[str, Any]) -> dict[str, Any]:
    need = ["list_price_per_unit", "attach_units"]
    missing = [k for k in need if b.get(k) is None]
    if missing:
        return {"unknown": f"UNKNOWN — requires {', '.join(missing)}"}
    price = float(b["list_price_per_unit"])
    units = float(b["attach_units"])
    discount = float(b.get("expected_discount_pct", 0.0))
    prior = None
    if b.get("cohort_attach_rate") is not None and b.get("lift") is not None:
        prior = min(0.60, float(b["cohort_attach_rate"]) * float(b["lift"]))
    return {
        "list_price_per_unit": price,
        "attach_units": units,
        "expected_discount_pct": discount,
        "gross_arr": price * units,
        "association_prior": round(prior, 3) if prior is not None else None,
    }


def size_commit(b: dict[str, Any]) -> dict[str, Any]:
    need = ["current_committed_arr", "proposed_commit_arr", "trailing_12m_overage"]
    missing = [k for k in need if b.get(k) is None]
    if missing:
        return {"unknown": f"UNKNOWN — requires {', '.join(missing)}"}
    cur = float(b["current_committed_arr"])
    prop = float(b["proposed_commit_arr"])
    over = float(b["trailing_12m_overage"])
    return {
        "current_committed_arr": cur,
        "proposed_commit_arr": prop,
        "committed_arr_delta": prop - cur,
        "trailing_12m_overage": over,
        "billings_delta": prop - (cur + over),
        "revenue_quality_note": (
            f"${over:,.0f} of variable, disputable overage converted to contracted ARR"),
    }


# --------------------------------------------------------------------------------------
# Scoring
# --------------------------------------------------------------------------------------

def evaluate(row: dict[str, Any], today: date) -> dict[str, Any]:
    name = row.get("name", row.get("account_id", "UNKNOWN"))
    motion = row.get("motion", "seat")

    renewal = row.get("renewal_date")
    notice = row.get("notice_period_days")
    d_renewal = d_optout = None
    opt_out_date = None
    if renewal:
        r = datetime.strptime(renewal, "%Y-%m-%d").date()
        d_renewal = (r - today).days
        if notice is not None:
            opt_out_date = date.fromordinal(r.toordinal() - int(notice))
            d_optout = (opt_out_date - today).days

    months_to_renewal = max(0.0, (d_renewal or 0) / 30.4)

    # --- gates -------------------------------------------------------------------------
    band = str(row.get("health_band", "")).lower()
    gate = HEALTH_GATE.get(band)
    blocks = [HARD_BLOCKS.get(k, k) for k in row.get("hard_blocks", [])]
    cools = [COOLDOWNS.get(k, k) for k in row.get("cooldowns", [])]

    refused = None
    if gate is None:
        refused = f"UNKNOWN — requires health_band (one of {', '.join(HEALTH_GATE)})"
    elif gate == 0.0:
        refused = (f"Health band '{band}' is below the expansion floor. "
                   f"Expansion is not recommended; run churn-risk and save-play instead.")
    elif blocks:
        refused = "Hard block: " + "; ".join(blocks)

    # --- sizing ------------------------------------------------------------------------
    sizing: dict[str, Any] = {}
    arr = float(row.get("arr") or 0)
    opportunity_arr: float | None = None
    unknown = None

    if motion == "seat":
        b = dict(row.get("seat") or {})
        if b.get("effective_price_per_seat") is None and b.get("contracted_seats"):
            b["effective_price_per_seat"] = arr / float(b["contracted_seats"]) if arr else None
        sizing = size_seat(b, months_to_renewal)
        if "unknown" in sizing:
            unknown = sizing["unknown"]
        elif sizing.get("_needs_price"):
            unknown = "UNKNOWN — requires arr and contracted_seats to derive effective price per seat"
        else:
            opportunity_arr = (sizing["recommended_units"] * sizing["unit_price"]
                               * (1 - sizing["expected_discount_pct"]))
    elif motion == "tier":
        sizing = size_tier(dict(row.get("tier") or {}), months_to_renewal)
        if "unknown" in sizing:
            unknown = sizing["unknown"]
        else:
            opportunity_arr = sizing["tier_delta_arr"] if sizing["crosses_in_term"] else 0.0
    elif motion == "cross_sell":
        sizing = size_cross_sell(dict(row.get("cross_sell") or {}))
        if "unknown" in sizing:
            unknown = sizing["unknown"]
        else:
            opportunity_arr = sizing["gross_arr"] * (1 - sizing["expected_discount_pct"])
    elif motion == "commit":
        sizing = size_commit(dict(row.get("commit") or {}))
        if "unknown" in sizing:
            unknown = sizing["unknown"]
        else:
            opportunity_arr = sizing["committed_arr_delta"]
    else:
        unknown = f"UNKNOWN — unrecognised motion {motion!r}"

    # --- ranking factors ----------------------------------------------------------------
    tier = str(row.get("signal_tier", "")).upper()
    fams = int(row.get("independent_families") or 1)
    base_prior = TIER_PRIOR.get(tier)
    if base_prior is None:
        propensity, prop_note = 0.0, f"UNKNOWN — requires signal_tier (one of {', '.join(TIER_PRIOR)})"
    else:
        propensity = min(PROPENSITY_CAP, base_prior + FAMILY_BONUS * max(0, fams - 1))
        prop_note = (f"{tier} prior {base_prior:.2f} + {max(0, fams-1)} extra "
                     f"{'family' if fams == 2 else 'families'} x {FAMILY_BONUS:.2f} "
                     f"= {propensity:.2f} (cap {PROPENSITY_CAP:.2f})")
    if motion == "cross_sell" and sizing.get("association_prior") is not None:
        propensity = min(PROPENSITY_CAP, max(propensity, sizing["association_prior"]))
        prop_note += f"; association-rule prior {sizing['association_prior']:.2f} applied"

    tfit, tnote = timing_fit(d_optout, d_renewal)
    rkey = str(row.get("relationship", "")).lower()
    rfit, rnote = RELATIONSHIP.get(rkey, (0.0, f"UNKNOWN — requires relationship "
                                              f"(one of {', '.join(RELATIONSHIP)})"))

    value_days = row.get("last_value_artifact_days")
    value_factor, value_note = 1.0, "Value evidence current"
    if value_days is None:
        value_factor = VALUE_STALE_FACTOR
        value_note = "UNKNOWN — requires last_value_artifact_days; treated as value-first required"
    elif int(value_days) > VALUE_EVIDENCE_MAX_DAYS:
        value_factor = VALUE_STALE_FACTOR
        value_note = (f"Value evidence {value_days}d old (>{VALUE_EVIDENCE_MAX_DAYS}d) — "
                      f"deliver a validated outcome before the ask")

    ranked = None
    if opportunity_arr is not None and gate:
        ranked = opportunity_arr * propensity * tfit * rfit * gate * value_factor

    hours = float(row.get("csm_hours") or 0)
    throughput = (ranked / hours) if (ranked is not None and hours > 0) else None

    status = "READY"
    if refused:
        status = "REFUSED"
    elif unknown:
        status = "UNSIZED"
    elif cools:
        status = "DEFER"
    elif motion == "tier" and not sizing.get("crosses_in_term"):
        status = "RECOMMEND STAY"
    elif value_factor < 1.0:
        status = "VALUE-FIRST"

    return {
        "account_id": row.get("account_id"), "name": name, "arr": arr, "motion": motion,
        "status": status, "refusal": refused, "unknown": unknown, "cooldowns": cools,
        "health_band": band, "health_gate": gate,
        "renewal_date": renewal, "opt_out_date": opt_out_date.isoformat() if opt_out_date else None,
        "days_to_opt_out": d_optout, "days_to_renewal": d_renewal,
        "sizing": {k: v for k, v in sizing.items() if not k.startswith("_")},
        "opportunity_arr": round(opportunity_arr, 2) if opportunity_arr is not None else None,
        "propensity": round(propensity, 3), "propensity_note": prop_note,
        "timing_fit": tfit, "timing_note": tnote,
        "relationship_fit": rfit, "relationship_note": rnote,
        "value_factor": value_factor, "value_note": value_note,
        "ranked_value": round(ranked, 2) if ranked is not None else None,
        "csm_hours": hours,
        "throughput_per_hour": round(throughput, 2) if throughput is not None else None,
    }


# --------------------------------------------------------------------------------------
# Rendering
# --------------------------------------------------------------------------------------

def render(rows: list[dict[str, Any]]) -> str:
    live = [r for r in rows if r["ranked_value"] is not None and r["status"] != "REFUSED"]
    live.sort(key=lambda r: (-(r["throughput_per_hour"] or 0), -(r["opportunity_arr"] or 0),
                             r["days_to_opt_out"] if r["days_to_opt_out"] is not None else 10**6))
    out = ["# Expansion Pipeline — sized and ranked", ""]
    total = sum(r["opportunity_arr"] or 0 for r in live)
    weighted = sum(r["ranked_value"] or 0 for r in live)
    out.append(f"**{len(live)} sized opportunities · ${total:,.0f} gross expansion ARR · "
               f"${weighted:,.0f} risk-adjusted.**")
    out.append("")
    out.append("| # | Account | Motion | Opp ARR | Propensity | Timing | Relationship | "
               "Gate | Ranked $ | Hours | $/hr | Status | Opt-out |")
    out.append("|---|---|---|---|---|---|---|---|---|---|---|---|---|")
    for i, r in enumerate(live, 1):
        out.append(
            f"| {i} | {r['name']} | {r['motion']} | ${r['opportunity_arr']:,.0f} | "
            f"{r['propensity']:.2f} | {r['timing_fit']:.2f} | {r['relationship_fit']:.2f} | "
            f"{r['health_gate']:.2f} | ${r['ranked_value']:,.0f} | {r['csm_hours']:.0f} | "
            f"{('$%.0f' % r['throughput_per_hour']) if r['throughput_per_hour'] else '—'} | "
            f"{r['status']} | {r['opt_out_date'] or 'UNKNOWN'} "
            f"({r['days_to_opt_out'] if r['days_to_opt_out'] is not None else '—'}d) |")

    refused = [r for r in rows if r["status"] == "REFUSED"]
    if refused:
        out += ["", "## Refused — health gate", "",
                "| Account | ARR | Band | Reason | Required before reconsidering |",
                "|---|---|---|---|---|"]
        for r in refused:
            out.append(f"| {r['name']} | ${r['arr']:,.0f} | {r['health_band']} | {r['refusal']} | "
                       f"Clear the block, then re-run; or evidence a genuinely separate "
                       f"business unit with its own budget holder |")

    unsized = [r for r in rows if r["status"] == "UNSIZED"]
    if unsized:
        out += ["", "## Unsized — missing inputs", "", "| Account | Motion | Gap |", "|---|---|---|"]
        for r in unsized:
            out.append(f"| {r['name']} | {r['motion']} | {r['unknown']} |")

    deferred = [r for r in rows if r["status"] == "DEFER"]
    if deferred:
        out += ["", "## Deferred — cooldown active", "", "| Account | Cooldown |", "|---|---|"]
        for r in deferred:
            out.append(f"| {r['name']} | {'; '.join(r['cooldowns'])} |")

    out += ["", "> Propensity values are practitioner priors by signal tier, not calibrated",
            "> win rates. Replace them with your own closed-won rates once you have >=30",
            "> closed expansion deals per motion, and cite the sample."]
    return "\n".join(out)


def explain(r: dict[str, Any]) -> str:
    o = [f"# {r['name']} — {r['motion']} expansion", ""]
    o.append(f"Status: **{r['status']}**")
    if r["refusal"]:
        o += ["", f"**Refused:** {r['refusal']}", "",
              "The only exception is a genuinely separate business unit — separate budget "
              "holder, separate workspace or contract entity, and no shared root cause with "
              "the failing unit. Evidence all three or the refusal stands."]
        return "\n".join(o)
    if r["unknown"]:
        o += ["", f"**Not sized:** {r['unknown']}"]
        return "\n".join(o)

    o += ["", "## Sizing"]
    for k, v in r["sizing"].items():
        if k == "schedule":
            o.append("")
            o.append("| Month | Usage | Current-tier overage | Target-tier overage |")
            o.append("|---|---|---|---|")
            for s in v:
                o.append(f"| {s['month']} | {s['usage']:,.0f} | ${s['current_overage']:,.2f} "
                         f"| ${s['target_overage']:,.2f} |")
            continue
        o.append(f"- `{k}` = {v}")
    o += ["", f"**Opportunity ARR = ${r['opportunity_arr']:,.2f}**", "", "## Ranking arithmetic"]
    o.append(f"- Propensity {r['propensity']:.2f} — {r['propensity_note']}")
    o.append(f"- Timing fit {r['timing_fit']:.2f} — {r['timing_note']}")
    o.append(f"- Relationship readiness {r['relationship_fit']:.2f} — {r['relationship_note']}")
    o.append(f"- Health gate {r['health_gate']:.2f} — band '{r['health_band']}'")
    o.append(f"- Value factor {r['value_factor']:.2f} — {r['value_note']}")
    o.append("")
    o.append(f"Ranked value = ${r['opportunity_arr']:,.2f} x {r['propensity']:.2f} "
             f"x {r['timing_fit']:.2f} x {r['relationship_fit']:.2f} x {r['health_gate']:.2f} "
             f"x {r['value_factor']:.2f} = **${r['ranked_value']:,.2f}**")
    if r["throughput_per_hour"]:
        o.append(f"Throughput = ${r['ranked_value']:,.2f} / {r['csm_hours']:.0f} CSM hours "
                 f"= **${r['throughput_per_hour']:,.2f} per hour**")
    return "\n".join(o)


def main() -> int:
    ap = argparse.ArgumentParser(description="Deterministic expansion sizing and ranking.")
    ap.add_argument("input", help="JSON file: list of candidate opportunity objects")
    ap.add_argument("--explain", metavar="ACCOUNT_ID", help="full derivation for one account")
    ap.add_argument("--json", action="store_true", help="emit JSON instead of markdown")
    ap.add_argument("--today", help="override today's date, YYYY-MM-DD (reproducible runs)")
    args = ap.parse_args()

    today = datetime.strptime(args.today, "%Y-%m-%d").date() if args.today else date.today()
    with open(args.input) as fh:
        book = json.load(fh)
    if isinstance(book, dict):
        book = [book]

    rows = [evaluate(r, today) for r in book]

    if args.explain:
        match = next((r for r in rows if r["account_id"] == args.explain), None)
        if not match:
            print(f"No candidate with account_id {args.explain!r}", file=sys.stderr)
            return 1
        print(explain(match))
        return 0

    print(json.dumps(rows, indent=2) if args.json else render(rows))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
