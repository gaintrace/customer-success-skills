#!/usr/bin/env python3
"""
Deterministic value-case arithmetic for the `qbr-builder` skill.

Why a script: a QBR value figure is four multiplications stacked on top of each other
(hours -> annual hours -> gross dollars -> risk-adjusted dollars) repeated per benefit
line, then rolled up into a net value, a ratio and a payback period. An LLM doing that in
prose drifts by a few percent per line, and the drifted number is the one the customer's
finance team checks. This produces the same answer every time and prints every step.

It also enforces the two rules that decide whether a figure may go on a slide at all:

  1. No customer-supplied baseline -> no dollar figure. The line is reported as
     NOT PRESENTABLE and contributes unit metrics only.
  2. Attribution is a stated factor with a stated level. A4 (correlation only) can never
     produce a dollar claim, and alpha is never allowed to be 1.0.

Usage
-----
    python3 value_case.py sample_value_case.json
    python3 value_case.py case.json --json
    python3 value_case.py case.json --explain          # show every arithmetic step
    python3 value_case.py --demo                       # run the bundled sample

Input: one JSON object.

    {
      "account": "Northwind Logistics",
      "period": "FY26 trailing 12 months (2025-07-01 .. 2026-06-30)",
      "as_of": "2026-08-24",
      "customer_cost": {
        "fees_in_period": 180000,
        "internal_cost": 24000,               // their admin FTE, integration, training
        "internal_cost_source": "K. Osei, Finance Ops, 2026-08-12"
      },
      "benefits": [
        {
          "name": "Month-end close cycle",
          "class": "time_released",           // time_released|cost_avoided|revenue_influenced|risk_reduced
          "baseline": {
            "value": 9.0, "unit": "working days", "date": "2025-11-30",
            "source": "Their close calendar, extracted by their FP&A team",
            "supplied_by": "customer"         // customer|reconstructed|none
          },
          "current": {"value": 5.5, "date": "2026-06-30"},
          "users_affected": 26,
          "hours_saved_per_user_per_week": 1.4,
          "working_weeks_per_year": 46,
          "adoption_rate": 0.85,
          "loaded_hourly_cost": 68.0,
          "loaded_cost_source": "customer",   // customer|estimated|none
          "alpha": 0.7,
          "alpha_level": "A2",                // A1|A2|A3|A4
          "alpha_attested_by": "J. Alvarez, Controller, email 2026-08-14",
          "haircut": 0.1,
          "haircut_reason": "Two of six teams changed process independently in April",
          "redeployment": "Two FTE-equivalents moved to the audit-readiness programme"
        }
      ],
      "exclusions": ["Licence cost of the two integrations they built themselves"]
    }

Both sides must cover the same window. Benefit arithmetic annualises hours, so
`fees_in_period` is the annual fee unless you scale the benefit lines to match.

Every field that is missing is reported as UNKNOWN and suppresses the dollar claim for
that line. Nothing is estimated, substituted or carried forward.

Standard library only. No network. Never mutates the input file.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

# --------------------------------------------------------------------------------------
# Rules. These mirror references/value-realization.md. Change both together.
# --------------------------------------------------------------------------------------

# Attribution levels, strongest first. A4 can never carry a dollar claim.
ALPHA_LEVELS = {
    "A1": "Treated vs untreated team, same period",
    "A2": "Pre/post with a stated counterfactual and named confounders",
    "A3": "Customer-attested share, in writing",
    "A4": "Correlation only",
}
ALPHA_MAX = 0.95          # alpha is never 1.0 — something else always contributed
BENEFIT_CLASSES = {"time_released", "cost_avoided", "revenue_influenced", "risk_reduced"}

BANDS = ["Not presentable", "Indicative", "Evidenced", "Attested"]

DEMO = {
    "account": "Northwind Logistics",
    "period": "FY26 trailing 12 months (2025-07-01 .. 2026-06-30)",
    "as_of": "2026-08-24",
    "customer_cost": {
        "fees_in_period": 180000,
        "internal_cost": 24000,
        "internal_cost_source": "K. Osei, Finance Ops, 2026-08-12",
    },
    "benefits": [
        {
            "name": "Month-end close cycle",
            "class": "time_released",
            "baseline": {
                "value": 9.0, "unit": "working days", "date": "2025-11-30",
                "source": "Their close calendar, extracted by their FP&A team",
                "supplied_by": "customer",
            },
            "current": {"value": 5.5, "date": "2026-06-30"},
            "users_affected": 140,
            "hours_saved_per_user_per_week": 1.2,
            "working_weeks_per_year": 46,
            "adoption_rate": 0.8,
            "loaded_hourly_cost": 68.0,
            "loaded_cost_source": "customer",
            "alpha": 0.7,
            "alpha_level": "A2",
            "alpha_attested_by": "J. Alvarez, Controller, email 2026-08-14",
            "haircut": 0.1,
            "haircut_reason": "Two of six teams changed process independently in April",
            "redeployment": "Two FTE-equivalents moved to the audit-readiness programme",
        },
        {
            "name": "Permissions support load",
            "class": "time_released",
            "baseline": {
                "value": 31, "unit": "tickets/month", "date": "2025-12-31",
                "source": "Zendesk, tag=permissions, extracted by us",
                "supplied_by": "reconstructed",
            },
            "current": {"value": 12, "date": "2026-06-30"},
            "users_affected": 3,
            "hours_saved_per_user_per_week": 2.0,
            "working_weeks_per_year": 46,
            "adoption_rate": 1.0,
            "loaded_hourly_cost": 55.0,
            "loaded_cost_source": "estimated",
            "alpha": 0.6,
            "alpha_level": "A2",
            "alpha_attested_by": None,
            "haircut": 0.15,
            "haircut_reason": "Their IT ran a separate access-review project in Q1",
            "redeployment": None,
        },
        {
            "name": "Faster quote turnaround correlates with win rate",
            "class": "revenue_influenced",
            "baseline": {
                "value": None, "unit": "win rate %", "date": None,
                "source": None, "supplied_by": "none",
            },
            "current": {"value": 34.0, "date": "2026-06-30"},
            "alpha": 0.4,
            "alpha_level": "A4",
            "alpha_attested_by": None,
        },
    ],
    "exclusions": [
        "Licence cost of the two integrations they built themselves",
        "Any revenue effect from the quote-turnaround change (A4 attribution)",
        "Headcount they did not hire — not claimed, because nobody has attested it",
    ],
}


# --------------------------------------------------------------------------------------
# Helpers
# --------------------------------------------------------------------------------------

def money(x: float | None) -> str:
    if x is None:
        return "UNKNOWN"
    return f"${x:,.0f}"


def num(x: Any) -> float | None:
    """Accept a number, or a string with currency and thousands separators. Never guess."""
    if x is None or x == "":
        return None
    if isinstance(x, (int, float)):
        return float(x)
    s = str(x).strip().replace(",", "").replace("$", "").replace("%", "")
    try:
        return float(s)
    except ValueError:
        return None


# --------------------------------------------------------------------------------------
# Per-line evaluation
# --------------------------------------------------------------------------------------

def evaluate_benefit(b: dict, idx: int) -> dict:
    """Return one benefit line with its arithmetic, its blockers and its band ceiling."""
    out: dict[str, Any] = {
        "n": idx,
        "name": b.get("name") or f"Benefit {idx}",
        "class": b.get("class"),
        "blockers": [],
        "steps": [],
        "gross": None,
        "risk_adjusted": None,
        "unit_gain": None,
        "band_ceiling": "Attested",
        "estimated_inputs": [],
    }
    blockers: list[str] = out["blockers"]

    if out["class"] not in BENEFIT_CLASSES:
        blockers.append(f"UNKNOWN — requires a benefit class, one of {sorted(BENEFIT_CLASSES)}")

    # ---- Baseline gate -----------------------------------------------------------
    baseline = b.get("baseline") or {}
    bl_value = num(baseline.get("value"))
    supplied_by = (baseline.get("supplied_by") or "none").lower()
    cur_value = num((b.get("current") or {}).get("value"))

    if bl_value is None or supplied_by == "none":
        blockers.append("UNKNOWN — requires a customer-supplied baseline (value, date, source)")
        out["band_ceiling"] = "Not presentable"
    elif not baseline.get("date"):
        blockers.append("UNKNOWN — requires the date the baseline was measured")
        out["band_ceiling"] = "Not presentable"
    elif supplied_by == "reconstructed":
        out["band_ceiling"] = "Evidenced"
        out["estimated_inputs"].append("baseline reconstructed from our data")

    if bl_value is not None and cur_value is not None:
        out["unit_gain"] = round(bl_value - cur_value, 4)
        out["steps"].append(
            f"unit gain = baseline {bl_value} {baseline.get('unit') or ''} "
            f"- current {cur_value} = {out['unit_gain']}"
        )

    # ---- Attribution gate --------------------------------------------------------
    alpha = num(b.get("alpha"))
    level = (b.get("alpha_level") or "").upper()
    if level not in ALPHA_LEVELS:
        blockers.append(f"UNKNOWN — requires an attribution level, one of {sorted(ALPHA_LEVELS)}")
        out["band_ceiling"] = "Not presentable"
    elif level == "A4":
        blockers.append("A4 attribution is correlation only — no dollar claim permitted")
        out["band_ceiling"] = "Not presentable"
    elif level == "A3" and not b.get("alpha_attested_by"):
        out["band_ceiling"] = min_band(out["band_ceiling"], "Indicative")
        out["estimated_inputs"].append("A3 attribution with nothing in writing")
    elif level in ("A1", "A2") and not b.get("alpha_attested_by"):
        out["band_ceiling"] = min_band(out["band_ceiling"], "Evidenced")
        out["estimated_inputs"].append("attribution not attested by the customer in writing")

    if alpha is None:
        blockers.append("UNKNOWN — requires an attribution factor alpha in 0..1")
    elif alpha <= 0 or alpha > ALPHA_MAX:
        blockers.append(
            f"attribution alpha={alpha} is outside 0 < alpha <= {ALPHA_MAX} — "
            "something else always contributed; state the share you can defend"
        )
        alpha = None

    # ---- Loaded cost -------------------------------------------------------------
    loaded = num(b.get("loaded_hourly_cost"))
    loaded_src = (b.get("loaded_cost_source") or "none").lower()
    if out["class"] == "time_released":
        if loaded is None or loaded_src == "none":
            blockers.append(
                "UNKNOWN — requires a customer-supplied fully loaded hourly cost; "
                "present released capacity as capacity until it exists"
            )
        elif loaded_src == "estimated":
            out["band_ceiling"] = min_band(out["band_ceiling"], "Evidenced")
            out["estimated_inputs"].append("loaded hourly cost is our estimate")
        if not b.get("redeployment"):
            out["estimated_inputs"].append(
                "no named redeployment — released capacity, not cash saved"
            )

    # ---- Arithmetic --------------------------------------------------------------
    users = num(b.get("users_affected"))
    hrs = num(b.get("hours_saved_per_user_per_week"))
    weeks = num(b.get("working_weeks_per_year"))
    adopt = num(b.get("adoption_rate"))
    haircut = num(b.get("haircut")) or 0.0

    if None not in (users, hrs, weeks, adopt):
        annual_hours = users * hrs * weeks * adopt
        out["annual_hours_released"] = round(annual_hours, 1)
        out["steps"].append(
            f"annual hours released = {users:g} users x {hrs:g} h/wk x {weeks:g} wks "
            f"x {adopt:g} adoption = {annual_hours:,.1f} h"
        )
        if loaded is not None:
            gross = annual_hours * loaded
            out["gross"] = round(gross, 2)
            out["steps"].append(
                f"gross value = {annual_hours:,.1f} h x {money(loaded)}/h = {money(gross)}"
            )
            if alpha is not None:
                risk_adj = gross * alpha * (1 - haircut)
                out["steps"].append(
                    f"risk-adjusted = {money(gross)} x alpha {alpha:g} "
                    f"x (1 - haircut {haircut:g}) = {money(risk_adj)}"
                )
                out["risk_adjusted"] = round(risk_adj, 2)
    elif out["class"] == "time_released":
        missing = [n for n, v in (
            ("users_affected", users), ("hours_saved_per_user_per_week", hrs),
            ("working_weeks_per_year", weeks), ("adoption_rate", adopt)) if v is None]
        blockers.append(f"UNKNOWN — requires {', '.join(missing)}")

    # A blocked line contributes no dollars, whatever the arithmetic produced.
    if blockers:
        out["risk_adjusted"] = None
        out["band_ceiling"] = "Not presentable" if out["band_ceiling"] == "Attested" \
            else out["band_ceiling"]

    # A clean line with two or more estimated inputs is Indicative at best.
    if not blockers and len(out["estimated_inputs"]) >= 2:
        out["band_ceiling"] = min_band(out["band_ceiling"], "Indicative")
    elif not blockers and len(out["estimated_inputs"]) == 1:
        out["band_ceiling"] = min_band(out["band_ceiling"], "Evidenced")

    return out


def min_band(a: str, b: str) -> str:
    """The weaker of two bands."""
    return BANDS[min(BANDS.index(a), BANDS.index(b))]


# --------------------------------------------------------------------------------------
# Roll-up
# --------------------------------------------------------------------------------------

def roll_up(case: dict) -> dict:
    lines = [evaluate_benefit(b, i + 1) for i, b in enumerate(case.get("benefits") or [])]

    presentable = [l for l in lines if l["risk_adjusted"] is not None]
    total_benefit = sum(l["risk_adjusted"] for l in presentable) if presentable else None

    cc = case.get("customer_cost") or {}
    fees = num(cc.get("fees_in_period"))
    internal = num(cc.get("internal_cost"))
    cost_notes = []
    if fees is None:
        cost_notes.append("UNKNOWN — requires fees in period")
    if internal is None:
        cost_notes.append("UNKNOWN — requires their internal cost (admin FTE, integration, training)")
    customer_cost = None if fees is None else fees + (internal or 0.0)

    net = ratio = payback = None
    if total_benefit is not None and customer_cost:
        net = total_benefit - customer_cost
        ratio = total_benefit / customer_cost
        payback = customer_cost / (total_benefit / 12) if total_benefit > 0 else None

    band = "Not presentable" if not presentable else BANDS[
        min(BANDS.index(l["band_ceiling"]) for l in presentable)]

    return {
        "account": case.get("account", "UNKNOWN"),
        "period": case.get("period", "UNKNOWN"),
        "as_of": case.get("as_of") or "UNKNOWN — requires the as-of date of the export",
        "lines": lines,
        "total_risk_adjusted_benefit": None if total_benefit is None else round(total_benefit, 2),
        "customer_cost": None if customer_cost is None else round(customer_cost, 2),
        "cost_notes": cost_notes,
        "net_value": None if net is None else round(net, 2),
        "value_ratio": None if ratio is None else round(ratio, 2),
        "payback_months": None if payback is None else round(payback, 1),
        "band": band,
        "exclusions": case.get("exclusions") or [],
        "suppressed_lines": [l["name"] for l in lines if l["risk_adjusted"] is None],
    }


# --------------------------------------------------------------------------------------
# Rendering
# --------------------------------------------------------------------------------------

def render(res: dict, explain: bool) -> str:
    w = []
    w.append(f"VALUE CASE — {res['account']} · {res['period']}")
    w.append(f"as of {res['as_of']}")
    w.append("")
    w.append(f"{'#':<3}{'Benefit':<42}{'Gross':>14}{'Risk-adj.':>14}  Band")
    w.append("-" * 92)
    for l in res["lines"]:
        w.append(
            f"{l['n']:<3}{l['name'][:40]:<42}{money(l['gross']):>14}"
            f"{money(l['risk_adjusted']):>14}  {l['band_ceiling']}"
        )
        for blk in l["blockers"]:
            w.append(f"     ! {blk}")
        if explain:
            for s in l["steps"]:
                w.append(f"       {s}")
            for e in l["estimated_inputs"]:
                w.append(f"       ~ estimated input: {e}")
    w.append("-" * 92)
    w.append(f"{'':<45}{'':>14}{money(res['total_risk_adjusted_benefit']):>14}  total")
    w.append("")
    w.append("ROLL-UP")
    w.append(f"  Risk-adjusted benefit   {money(res['total_risk_adjusted_benefit'])}")
    w.append(f"  Customer cost in period {money(res['customer_cost'])}")
    for n in res["cost_notes"]:
        w.append(f"     ! {n}")
    w.append(f"  Net value               {money(res['net_value'])}")
    w.append(f"  Value ratio             "
             f"{'UNKNOWN' if res['value_ratio'] is None else f'{res['value_ratio']}x'}")
    w.append(f"  Payback                 "
             f"{'UNKNOWN' if res['payback_months'] is None else f'{res['payback_months']} months'}")
    w.append("")
    w.append(f"BAND: {res['band']}")
    if res["band"] == "Not presentable":
        w.append("  No dollar figure goes on a slide. Present unit metrics and ask for the baseline.")
    if res["suppressed_lines"]:
        w.append("  Suppressed (no dollar claim): " + "; ".join(res["suppressed_lines"]))
    w.append("")
    w.append("DELIBERATELY EXCLUDED")
    for e in res["exclusions"]:
        w.append(f"  - {e}")
    if not res["exclusions"]:
        w.append("  ! UNKNOWN — requires an exclusions list. Naming what you did not count is "
                 "the fastest way to make the rest believable.")
    return "\n".join(w)


def main() -> int:
    ap = argparse.ArgumentParser(description="Deterministic QBR value-case arithmetic.")
    ap.add_argument("path", nargs="?", help="JSON case file")
    ap.add_argument("--demo", action="store_true", help="run the bundled sample case")
    ap.add_argument("--json", action="store_true", help="emit JSON instead of a table")
    ap.add_argument("--explain", action="store_true", help="show every arithmetic step")
    args = ap.parse_args()

    if args.demo:
        case = DEMO
    elif args.path:
        p = Path(args.path)
        if not p.exists():
            print(f"no such file: {p}", file=sys.stderr)
            return 2
        case = json.loads(p.read_text())
    else:
        ap.print_help()
        return 2

    res = roll_up(case)
    print(json.dumps(res, indent=2) if args.json else render(res, args.explain))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
