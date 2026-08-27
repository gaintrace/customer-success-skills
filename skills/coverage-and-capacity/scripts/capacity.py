#!/usr/bin/env python3
"""
Coverage capacity model for the `coverage-and-capacity` skill.

Why a script: this is one arithmetic chain — available hours, required hours, book size,
FTE gap, break-even — run across several segments, plus a sensitivity sweep over five
inputs. An LLM doing that in prose drifts, and it drifts in the direction of "it fits".
This produces the same numbers every time and shows every step.

What it does NOT do: decide anything. It does not choose segment boundaries, judge whether
an entitlement is right, or claim what a hire does to retention. Those are judgement calls
and they belong in SKILL.md and references/headcount-case.md.

Usage
-----
    python3 capacity.py sample_org.json
    python3 capacity.py sample_org.json --json
    python3 capacity.py sample_org.json --segment Enterprise

Input: see scripts/sample_org.json for a complete worked example.

Nulls matter. A missing `complexity_multiplier` is NOT 1.0 — it is unmeasured. The script
substitutes 1.0, prints the substitution in the assumption register, and caps confidence.
Same for every other defaulted input. Nothing is silently assumed.

No network. Standard library only.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from typing import Any

# --------------------------------------------------------------------------------------
# Defaults. These mirror references/capacity-math.md. Change them together or the
# artifact stops matching the script. Every one is [P] — a practitioner convention, not a
# benchmark — and every substitution is reported.
# --------------------------------------------------------------------------------------

DEFAULTS: dict[str, Any] = {
    "calendar_hours": 2080.0,          # line A
    "pto_hours": 160.0,                # line B
    "sick_hours": 40.0,                # line C
    "internal_load_fraction": 1.0 / 3, # line E, as a fraction of line D
    "realisation_factor": 0.85,        # line G
    "ote": 140000.0,
    "loading_factor": 1.30,
    "subscription_gross_margin": 0.81,
    "arr_multiple": None,              # no default: must come from Finance
    "coverage_share_of_margin": 0.15,
    "ramp_months_to_full": 6.0,
    "ramp_mean_productivity": 0.45,
    "complexity_multiplier": 1.0,
    "reactive_hours_per_account_per_year": 0.0,
    "onboarding_hours_per_new_account": 0.0,
    "new_accounts_per_year": 0.0,
}

UNKNOWN = "UNKNOWN"


class Assumptions:
    """Every defaulted input is recorded with a concrete consequence, never silently applied."""

    def __init__(self) -> None:
        self.rows: list[dict[str, str]] = []

    def add(self, field: str, value: Any, why: str, if_wrong: str) -> None:
        self.rows.append(
            {"field": field, "value": f"{value}", "why": why, "if_wrong": if_wrong}
        )

    def __len__(self) -> int:
        return len(self.rows)


def get(d: dict, key: str, default_key: str, notes: Assumptions,
        why: str, if_wrong: str) -> float:
    """Read a value, or substitute the default and record the substitution."""
    v = d.get(key)
    if v is None:
        v = DEFAULTS[default_key]
        if v is None:
            return float("nan")
        notes.add(key, v, why, if_wrong)
    return float(v)


# --------------------------------------------------------------------------------------
# Lines A - H
# --------------------------------------------------------------------------------------

def available_hours(csm: dict, notes: Assumptions) -> dict[str, float]:
    a = get(csm, "calendar_hours", "calendar_hours", notes,
            "no contracted-hours figure supplied",
            "a 37.5-hour week cuts H by ~6% and adds FTE to every segment")
    b = get(csm, "pto_hours", "pto_hours", notes,
            "no PTO policy supplied",
            "each extra week of PTO removes ~23 effective customer hours per FTE")
    c = get(csm, "sick_hours", "sick_hours", notes,
            "no HR absence actuals supplied",
            "understating absence transfers the error to the CSM as a permanent overrun")
    d = a - b - c

    if csm.get("internal_load_hours") is not None:
        e = float(csm["internal_load_hours"])
    else:
        frac = DEFAULTS["internal_load_fraction"]
        e = d * frac
        notes.add(
            "internal_load_hours", round(e, 1),
            "no four-week calendar audit supplied; one-third of paid hours used [P]",
            "internal load is the second-largest sensitivity — a measured 40% cuts H by ~10% "
            "and adds roughly one FTE per ten already required",
        )

    f = d - e
    g = get(csm, "realisation_factor", "realisation_factor", notes,
            "no measured realisation factor supplied",
            "realisation is a top-two sensitivity; 0.78 vs 0.85 moves required FTE by ~9%")
    h = f * g
    return {"A": a, "B": b, "C": c, "D": d, "E": e, "F": f, "G": g, "H": h}


def loaded_cost(csm: dict, h_hours: float, notes: Assumptions) -> dict[str, float]:
    ote = get(csm, "ote", "ote", notes,
              "no compensation band supplied",
              "comp varies more than 30% by geography; every cost figure scales with it")
    lf = get(csm, "loading_factor", "loading_factor", notes,
             "no loading factor supplied; ask Finance for theirs",
             "1.25 vs 1.40 moves the fully loaded cost by $21,000 per CSM")
    c_annual = ote * lf
    per_hour = c_annual / h_hours if h_hours > 0 else float("nan")
    return {"ote": ote, "loading_factor": lf, "annual": c_annual, "per_hour": per_hour}


# --------------------------------------------------------------------------------------
# Required hours and book size
# --------------------------------------------------------------------------------------

def segment_model(seg: dict, h_hours: float, cost_per_hour: float,
                  gross_margin: float, k_share: float,
                  notes: Assumptions) -> dict[str, Any]:
    name = seg.get("name", "unnamed")
    # Pooled, digital and player-coach roles have a different internal load and therefore a
    # different line H. capacity-math.md section 4 gives the variants.
    if seg.get("effective_hours_override") is not None:
        h_hours = float(seg["effective_hours_override"])
    accounts = float(seg.get("accounts") or 0)
    arr = float(seg.get("arr") or 0)

    scheduled = 0.0
    for m in seg.get("motions", []):
        scheduled += float(m.get("instances_per_year", 0)) * float(m.get("hours_each", 0))

    reactive = get(seg, "reactive_hours_per_account_per_year",
                   "reactive_hours_per_account_per_year", notes,
                   f"{name}: no ticket or interaction actuals supplied; reactive load set to 0",
                   "reactive load is never zero; omitting it understates required hours and "
                   "the deficit is discovered as an overrun instead of a plan")

    onboarding_hours = get(seg, "onboarding_hours_per_new_account",
                           "onboarding_hours_per_new_account", notes,
                           f"{name}: no onboarding cost supplied",
                           "onboarding is 2-4x steady-state hours; omitting it understates a "
                           "fast-growing segment most")
    new_accounts = get(seg, "new_accounts_per_year", "new_accounts_per_year", notes,
                       f"{name}: no new-logo plan supplied",
                       "a growing segment needs the onboarding overlay or it is short by the "
                       "growth rate")
    onboarding_amortised = (onboarding_hours * new_accounts / accounts) if accounts else 0.0

    cx = seg.get("complexity_multiplier")
    if cx is None:
        cx = DEFAULTS["complexity_multiplier"]
        notes.add(f"{name}.complexity_multiplier", cx,
                  "no complexity index computed",
                  "complexity is the LARGEST single sensitivity; a real 1.3 understates "
                  "required FTE by ~23% when modelled as 1.0")
    cx = float(cx)

    base = scheduled + reactive + onboarding_amortised
    required_per_account = base * cx

    sustainable_accounts = h_hours / required_per_account if required_per_account > 0 else float("nan")
    mean_arr = arr / accounts if accounts else float("nan")
    sustainable_arr = sustainable_accounts * mean_arr if accounts else float("nan")
    required_fte = accounts / sustainable_accounts if sustainable_accounts > 0 else float("nan")

    current_fte = seg.get("current_fte")
    current_fte = float(current_fte) if current_fte is not None else float("nan")
    gap_fte = required_fte - current_fte if not math.isnan(current_fte) else float("nan")

    cost_per_account = required_per_account * cost_per_hour
    cts_pct = (cost_per_account / mean_arr * 100) if mean_arr and not math.isnan(mean_arr) else float("nan")
    arr_floor = ((required_per_account * cost_per_hour) / (k_share * gross_margin)
                 if k_share > 0 and gross_margin > 0 else float("nan"))

    return {
        "name": name,
        "coverage_model": seg.get("coverage_model", UNKNOWN),
        "accounts": accounts,
        "arr": arr,
        "mean_arr": mean_arr,
        "scheduled_hours": scheduled,
        "reactive_hours": reactive,
        "onboarding_amortised": onboarding_amortised,
        "base_hours": base,
        "complexity_multiplier": cx,
        "required_hours_per_account": required_per_account,
        "sustainable_accounts_per_csm": sustainable_accounts,
        "sustainable_arr_per_csm": sustainable_arr,
        "required_fte": required_fte,
        "current_fte": current_fte,
        "gap_fte": gap_fte,
        "required_hours_total": required_per_account * accounts,
        "available_hours_total": (current_fte * h_hours) if not math.isnan(current_fte) else float("nan"),
        "cost_per_account": cost_per_account,
        "cost_to_serve_pct": cts_pct,
        "arr_floor_for_model": arr_floor,
        "effective_hours_used": h_hours,
        "hours_basis": seg.get("hours_basis", "default"),
    }


# --------------------------------------------------------------------------------------
# Headcount arithmetic
# --------------------------------------------------------------------------------------

def headcount(gap_fte: float, arr_covered_per_csm: float, cost: dict,
              finance: dict, ramp: dict, notes: Assumptions) -> dict[str, Any]:
    r = get(ramp, "months_to_full", "ramp_months_to_full", notes,
            "no measured ramp supplied",
            "a 9-month ramp cuts year-1 delivered capacity from 0.73 to 0.55 FTE per hire")
    p = get(ramp, "mean_productivity", "ramp_mean_productivity", notes,
            "no measured ramp productivity supplied",
            "p=0.30 rather than 0.45 raises year-1 cost per delivered FTE by ~10%")
    delivered = (r / 12.0) * p + (12.0 - r) / 12.0
    y1_cost = cost["annual"] / delivered if delivered > 0 else float("nan")

    gm = get(finance, "subscription_gross_margin", "subscription_gross_margin", notes,
             "no subscription gross margin supplied; Benchmarkit CY2024 median used [M]",
             "a 70% margin raises the cash break-even by ~16%")
    margin_dollars = arr_covered_per_csm * gm
    cash_pp = (cost["annual"] / margin_dollars * 100) if margin_dollars > 0 else float("nan")
    cash_pp_y1 = (y1_cost / margin_dollars * 100) if margin_dollars > 0 else float("nan")

    mult = finance.get("arr_multiple")
    if mult is None:
        value_pp = float("nan")
        value_pp_y1 = float("nan")
        notes.add("arr_multiple", UNKNOWN,
                  "no ARR multiple supplied; Finance owns this number and no default is safe",
                  "the value break-even cannot be computed, so the case must rest on cash "
                  "break-even alone — which is a much higher bar")
    else:
        mult = float(mult)
        value_pp = cost["annual"] / (arr_covered_per_csm * mult) * 100
        value_pp_y1 = y1_cost / (arr_covered_per_csm * mult) * 100

    return {
        "gap_fte": gap_fte,
        "hires_needed": math.ceil(gap_fte) if gap_fte and gap_fte > 0 and not math.isnan(gap_fte) else 0,
        "ramp_months": r,
        "ramp_mean_productivity": p,
        "year1_delivered_capacity": delivered,
        "year1_cost_per_delivered_fte": y1_cost,
        "arr_covered_per_csm": arr_covered_per_csm,
        "cash_break_even_pp": cash_pp,
        "cash_break_even_pp_year1": cash_pp_y1,
        "value_break_even_pp": value_pp,
        "value_break_even_pp_year1": value_pp_y1,
    }


# --------------------------------------------------------------------------------------
# Sensitivity
# --------------------------------------------------------------------------------------

SENSITIVITY_INPUTS = [
    ("internal_load", "Internal load (line E)"),
    ("realisation", "Realisation factor (line G)"),
    ("complexity", "Complexity multiplier"),
    ("motion_hours", "Scheduled motion hours"),
    ("reactive", "Reactive hours"),
]


def total_required_fte(doc: dict, lever: str | None, delta: float) -> float:
    """Recompute total required FTE with one input scaled by (1 + delta)."""
    sink = Assumptions()
    csm = dict(doc.get("csm", {}))
    if lever == "internal_load":
        lines0 = available_hours(dict(doc.get("csm", {})), Assumptions())
        csm["internal_load_hours"] = lines0["E"] * (1 + delta)
    if lever == "realisation":
        lines0 = available_hours(dict(doc.get("csm", {})), Assumptions())
        csm["realisation_factor"] = lines0["G"] * (1 + delta)
    lines = available_hours(csm, sink)
    cost = loaded_cost(csm, lines["H"], sink)
    fin = doc.get("finance", {})
    gm = fin.get("subscription_gross_margin") or DEFAULTS["subscription_gross_margin"]
    k = fin.get("coverage_share_of_margin") or DEFAULTS["coverage_share_of_margin"]

    total = 0.0
    for raw in doc.get("segments", []):
        seg = json.loads(json.dumps(raw))
        if lever == "complexity":
            cx = seg.get("complexity_multiplier") or DEFAULTS["complexity_multiplier"]
            seg["complexity_multiplier"] = cx * (1 + delta)
        if lever == "motion_hours":
            for m in seg.get("motions", []):
                m["hours_each"] = float(m.get("hours_each", 0)) * (1 + delta)
        if lever == "reactive":
            base = seg.get("reactive_hours_per_account_per_year") or 0.0
            seg["reactive_hours_per_account_per_year"] = base * (1 + delta)
        if lever == "realisation" and seg.get("effective_hours_override") is not None:
            seg["effective_hours_override"] = float(seg["effective_hours_override"]) * (1 + delta)
        if lever == "internal_load" and seg.get("effective_hours_override") is not None:
            # scale the override the same way line H moved, so the sweep stays coherent
            base_lines = available_hours(dict(doc.get("csm", {})), Assumptions())
            seg["effective_hours_override"] = (
                float(seg["effective_hours_override"]) * lines["H"] / base_lines["H"])
        row = segment_model(seg, lines["H"], cost["per_hour"], gm, k, sink)
        if not math.isnan(row["required_fte"]):
            total += row["required_fte"]
    return total


# --------------------------------------------------------------------------------------
# Rendering
# --------------------------------------------------------------------------------------

def fmt_money(v: float) -> str:
    if v is None or (isinstance(v, float) and math.isnan(v)):
        return UNKNOWN
    return f"${v:,.0f}"


def fmt(v: float, nd: int = 1) -> str:
    if v is None or (isinstance(v, float) and math.isnan(v)):
        return UNKNOWN
    return f"{v:,.{nd}f}"


def render(doc: dict, only: str | None) -> str:
    notes = Assumptions()
    csm = doc.get("csm", {})
    lines = available_hours(csm, notes)
    cost = loaded_cost(csm, lines["H"], notes)
    fin = doc.get("finance", {})
    gm = get(fin, "subscription_gross_margin", "subscription_gross_margin", notes,
             "no subscription gross margin supplied; Benchmarkit CY2024 median used [M]",
             "margin scales every cost-to-serve and break-even figure")
    k = get(fin, "coverage_share_of_margin", "coverage_share_of_margin", notes,
            "no coverage share of gross margin supplied",
            "k sets the derived ARR floor per model; 0.10 vs 0.15 raises every floor by 50%")

    segments = doc.get("segments", [])
    if only:
        segments = [s for s in segments if s.get("name", "").lower() == only.lower()]
        if not segments:
            return f"no segment named {only!r} in the input"

    rows = [segment_model(s, lines["H"], cost["per_hour"], gm, k, notes) for s in segments]

    out: list[str] = []
    w = out.append
    w(f"# Coverage capacity model — as of {doc.get('as_of', UNKNOWN)}")
    w("")

    # Lines A-H
    w("## Available hours per CSM FTE per year")
    w("")
    w("| Line | Item | Hours |")
    w("|---|---|---|")
    w(f"| A | Calendar hours | {fmt(lines['A'], 0)} |")
    w(f"| B | - PTO, holidays, shutdown | -{fmt(lines['B'], 0)} |")
    w(f"| C | - Sick and unplanned | -{fmt(lines['C'], 0)} |")
    w(f"| D | = Paid working hours | {fmt(lines['D'], 0)} |")
    w(f"| E | - Internal load | -{fmt(lines['E'], 0)} |")
    w(f"| F | = Customer-facing hours | {fmt(lines['F'], 0)} |")
    w(f"| G | x Realisation factor | {fmt(lines['G'], 2)} |")
    w(f"| H | **= Effective customer hours** | **{fmt(lines['H'], 0)}** |")
    w("")
    w(f"Fully loaded cost per CSM **{fmt_money(cost['annual'])}** "
      f"(OTE {fmt_money(cost['ote'])} x {fmt(cost['loading_factor'], 2)}) "
      f"-> **{fmt_money(cost['per_hour'])} per customer-facing hour**.")
    w("")

    # Per segment
    w("## Required hours and book size, by segment")
    w("")
    w("| Segment | Model | Accts | ARR | Sched | React | Onbd | Cx | Req h/acct | Sust. accts/CSM | Sust. ARR/CSM | Req FTE | Cur FTE | Gap FTE |")
    w("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
    for r in rows:
        w("| {} | {} | {:.0f} | {} | {} | {} | {} | {} | {} | {} | {} | {} | {} | {} |".format(
            r["name"], r["coverage_model"], r["accounts"], fmt_money(r["arr"]),
            fmt(r["scheduled_hours"]), fmt(r["reactive_hours"]),
            fmt(r["onboarding_amortised"]), fmt(r["complexity_multiplier"], 2),
            fmt(r["required_hours_per_account"]),
            fmt(r["sustainable_accounts_per_csm"]),
            fmt_money(r["sustainable_arr_per_csm"]),
            fmt(r["required_fte"], 2), fmt(r["current_fte"], 2), fmt(r["gap_fte"], 2)))
    w("")
    w("**Ratios above are outputs of this model, not benchmarks.** Sustainable accounts/CSM = H / required hours per account.")
    w("")

    w("## Cost to serve")
    w("")
    w("| Segment | Mean ARR | Cost/account/yr | Cost to serve | ARR floor for this model | Verdict |")
    w("|---|---|---|---|---|---|")
    for r in rows:
        below = (not math.isnan(r["mean_arr"]) and not math.isnan(r["arr_floor_for_model"])
                 and r["mean_arr"] < r["arr_floor_for_model"])
        verdict = "**BELOW FLOOR — model too rich for this ACV**" if below else "within floor"
        w("| {} | {} | {} | {} | {} | {} |".format(
            r["name"], fmt_money(r["mean_arr"]), fmt_money(r["cost_per_account"]),
            fmt(r["cost_to_serve_pct"], 1) + "%", fmt_money(r["arr_floor_for_model"]), verdict))
    w("")
    w(f"ARR floor = (required hours x {fmt_money(cost['per_hour'])}) / ({fmt(k,2)} x {fmt(gm,2)} gross margin). "
      "Sanity bound: CS + Support median 9% of ARR [SaaS Capital 2026 Spending Benchmarks, "
      "survey Mar 2026, 1,000+ private B2B SaaS - M].")
    w("")

    # Totals
    req_fte = sum(r["required_fte"] for r in rows if not math.isnan(r["required_fte"]))
    cur_fte = sum(r["current_fte"] for r in rows if not math.isnan(r["current_fte"]))
    req_h = sum(r["required_hours_total"] for r in rows if not math.isnan(r["required_hours_total"]))
    avail_h = sum(r["current_fte"] * r["effective_hours_used"]
                  for r in rows if not math.isnan(r["current_fte"]))
    total_arr = sum(r["arr"] for r in rows)
    total_accounts = sum(r["accounts"] for r in rows)

    w("## Totals")
    w("")
    w("| | |")
    w("|---|---|")
    w(f"| Base modelled | {fmt_money(total_arr)} across {total_accounts:.0f} accounts |")
    w(f"| Required hours / available hours | {fmt(req_h, 0)} / {fmt(avail_h, 0)} |")
    w(f"| Hours deficit | {fmt(req_h - avail_h, 0)} |")
    w(f"| Required FTE / current FTE | {fmt(req_fte, 2)} / {fmt(cur_fte, 2)} |")
    w(f"| **FTE gap** | **{fmt(req_fte - cur_fte, 2)}** |")
    unc = doc.get("uncovered") or {}
    if unc:
        w(f"| Uncovered accounts / ARR | {unc.get('accounts', UNKNOWN)} / {fmt_money(float(unc.get('arr', 0)))} |")
        w(f"| Uncovered ARR renewing <=180d | {fmt_money(float(unc.get('arr_renewing_180d', 0)))} |")
        w(f"| Earliest opt-out deadline in uncovered set | {unc.get('earliest_opt_out_deadline', UNKNOWN)} |")
    w("")

    # Headcount, on the largest-gap segment
    gapped = [r for r in rows if not math.isnan(r["gap_fte"])]
    if gapped:
        worst = max(gapped, key=lambda r: r["gap_fte"])
        hc = headcount(worst["gap_fte"], worst["sustainable_arr_per_csm"], cost,
                       fin, doc.get("ramp", {}), notes)
        w(f"## Headcount arithmetic — largest gap: {worst['name']}")
        w("")
        w("| | |")
        w("|---|---|")
        w(f"| FTE gap in this segment | {fmt(hc['gap_fte'], 2)} -> {hc['hires_needed']} hire(s) |")
        w(f"| Ramp | {fmt(hc['ramp_months'], 0)} months at {fmt(hc['ramp_mean_productivity'], 2)} mean productivity |")
        w(f"| Year-1 delivered capacity per hire | {fmt(hc['year1_delivered_capacity'], 3)} FTE |")
        w(f"| Year-1 cost per delivered FTE | {fmt_money(hc['year1_cost_per_delivered_fte'])} |")
        w(f"| ARR under coverage per CSM | {fmt_money(hc['arr_covered_per_csm'])} |")
        w(f"| **Cash break-even** | **{fmt(hc['cash_break_even_pp'], 1)} GRR pp** steady state - {fmt(hc['cash_break_even_pp_year1'], 1)} pp year 1 |")
        w(f"| **Value break-even** | **{fmt(hc['value_break_even_pp'], 1)} GRR pp** steady state - {fmt(hc['value_break_even_pp_year1'], 1)} pp year 1 |")
        w("")
        w("Break-even points are arithmetic, not forecasts. The evidence that a hire delivers "
          "that retention gain is a separate question - see references/headcount-case.md sections 4 and 8.")
        w("")

    # Sensitivity
    base_fte = total_required_fte(doc, None, 0.0)
    w("## Sensitivity — measure first whatever moves this most")
    w("")
    w("| Input varied +/-10% | Required FTE at -10% | Required FTE at +10% | Swing |")
    w("|---|---|---|---|")
    sens = []
    for lever, label in SENSITIVITY_INPUTS:
        lo = total_required_fte(doc, lever, -0.10)
        hi = total_required_fte(doc, lever, +0.10)
        swing = abs(hi - lo) / base_fte * 100 if base_fte else float("nan")
        sens.append((label, lo, hi, swing))
    for label, lo, hi, swing in sorted(sens, key=lambda t: -t[3]):
        w(f"| {label} | {fmt(lo, 2)} | {fmt(hi, 2)} | {fmt(swing, 1)}% |")
    w("")
    lo_all = min(min(lo, hi) for _, lo, hi, _ in sens)
    hi_all = max(max(lo, hi) for _, lo, hi, _ in sens)
    w(f"**Report the model as a range: {fmt(base_fte, 1)} FTE required, "
      f"{fmt(lo_all, 1)}-{fmt(hi_all, 1)} across the sensitivity band.**")
    w("")

    # Assumptions
    w("## Assumptions")
    w("")
    if not len(notes):
        w("None — every input was supplied.")
    else:
        w("| # | Assumption | Why it was needed | If wrong |")
        w("|---|---|---|---|")
        for i, row in enumerate(notes.rows, 1):
            w(f"| {i} | `{row['field']}` = {row['value']} | {row['why']} | {row['if_wrong']} |")
    w("")
    measured = sum(1 for r in rows if r["hours_basis"] == "measured")
    w(f"Hours basis: {measured} of {len(rows)} segments measured, "
      f"{len(rows) - measured} on labelled defaults. "
      + ("Confidence capped at **Low** while any segment runs on defaults."
         if measured < len(rows) else "All segments measured."))
    return "\n".join(out)


def build_json(doc: dict) -> dict:
    notes = Assumptions()
    csm = doc.get("csm", {})
    lines = available_hours(csm, notes)
    cost = loaded_cost(csm, lines["H"], notes)
    fin = doc.get("finance", {})
    gm = get(fin, "subscription_gross_margin", "subscription_gross_margin", notes, "", "")
    k = get(fin, "coverage_share_of_margin", "coverage_share_of_margin", notes, "", "")
    rows = [segment_model(s, lines["H"], cost["per_hour"], gm, k, notes)
            for s in doc.get("segments", [])]
    req = sum(r["required_fte"] for r in rows if not math.isnan(r["required_fte"]))
    cur = sum(r["current_fte"] for r in rows if not math.isnan(r["current_fte"]))
    return {
        "as_of": doc.get("as_of"),
        "lines": lines,
        "cost": cost,
        "segments": rows,
        "totals": {"required_fte": req, "current_fte": cur, "gap_fte": req - cur},
        "assumptions": notes.rows,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="Coverage capacity model.")
    ap.add_argument("path", help="input JSON — see sample_org.json")
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    ap.add_argument("--segment", help="restrict the segment tables to one segment")
    args = ap.parse_args()

    try:
        doc = json.loads(open(args.path, encoding="utf-8").read())
    except (OSError, json.JSONDecodeError) as e:
        print(f"could not read {args.path}: {e}", file=sys.stderr)
        return 2

    if not doc.get("segments"):
        print("input has no `segments` — nothing to model", file=sys.stderr)
        return 2

    if args.json:
        print(json.dumps(build_json(doc), indent=2, default=str))
    else:
        print(render(doc, args.segment))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
