#!/usr/bin/env python3
"""
Deterministic value-case arithmetic for the `value-case` skill.

Why a script. A value case is four multiplications stacked per benefit line, repeated across
six benefit classes, then rolled into a net benefit, an ROI ratio, a payback period, three
scenarios and a break-even. A model doing that in prose drifts a few percent per line, and the
drifted number is the one the customer's finance team checks. This produces the same answer
every time and prints every step.

It also enforces the four gates that decide whether a line may carry a dollar figure at all:

  1. Baseline rung B4 (industry proxy) -> NOT PRESENTABLE. Unit metrics only.
  2. Attribution level A4 (correlation only) -> NOT PRESENTABLE.
  3. Attribution alpha = 1.0 on anything but a cash-releasing line -> refused.
  4. Risk-reduction expected value without a customer-supplied probability -> refused (R22).

Usage
-----
    python3 roi.py sample_case.json
    python3 roi.py sample_case.json --explain      # show every arithmetic step
    python3 roi.py sample_case.json --json
    python3 roi.py --demo                          # run the bundled sample

Input: one JSON object. See sample_case.json for a complete example.

    {
      "account": "...", "period": "...", "as_of": "YYYY-MM-DD", "period_months": 12,
      "sensitivity_driver": "attribution",     # attribution|recapture|loaded_hourly|hours
      "costs": {"subscription_fees": 0, "services": 0, "customer_internal_labour": 0,
                "customer_admin": 0, "training": 0, "integration": 0},
      "benefits": [ {...} ],
      "exclusions": ["..."]
    }

Benefit classes and their required inputs:

    time_released     users, adoption, hours_per_user_per_week, weeks, loaded_hourly, recapture
    cost_avoided      baseline_unit_cost, volume_today, actual_cost
    error_reduction   error_rate_delta, volume, cost_per_error
    revenue_influenced conversion_delta, opportunity_volume, avg_deal_value
    risk_reduced      probability_delta, loss_magnitude, probability_source ("customer")
    headcount_avoided volume_delta, throughput_per_fte, loaded_fte_cost, requisition_ref
    hard_cash         amount

No network. Standard library only.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

BAND_ORDER = ["Measured", "Attested", "Evidenced", "Indicative"]

CLASS_INPUTS = {
    "time_released": ["users", "adoption", "hours_per_user_per_week", "weeks",
                      "loaded_hourly", "recapture"],
    "cost_avoided": ["baseline_unit_cost", "volume_today", "actual_cost"],
    "error_reduction": ["error_rate_delta", "volume", "cost_per_error"],
    "revenue_influenced": ["conversion_delta", "opportunity_volume", "avg_deal_value"],
    "risk_reduced": ["probability_delta", "loss_magnitude"],
    "headcount_avoided": ["volume_delta", "throughput_per_fte", "loaded_fte_cost"],
    "hard_cash": ["amount"],
}

SOFT_CLASSES = {"soft"}


# --------------------------------------------------------------------------- helpers

def money(x: float) -> str:
    return f"${x:,.0f}"


def rate(x: float) -> str:
    """Unit rates keep their cents — $18.40 per ticket is not $18."""
    return f"${x:,.2f}"


def two_sig(x: float) -> str:
    """Round a composite figure to two significant figures (SKILL-STANDARD 4F)."""
    if x == 0:
        return "$0"
    neg = x < 0
    x = abs(x)
    if x >= 1_000_000:
        v, unit = x / 1_000_000, "M"
    elif x >= 1_000:
        v, unit = x / 1_000, "k"
    else:
        v, unit = x, ""
    v = round(v, 1) if v < 10 else round(v)
    return f"{'-' if neg else ''}${v:g}{unit}"


def weakest(bands: list[str]) -> str:
    if not bands:
        return "Indicative"
    return max(bands, key=lambda b: BAND_ORDER.index(b))


# --------------------------------------------------------------------------- gates

def gate(b: dict) -> tuple[bool, list[str]]:
    """Return (presentable, reasons). A blocked line contributes unit metrics only."""
    reasons: list[str] = []
    cls = b.get("class", "")
    rung = str(b.get("baseline_rung", "")).upper()
    level = str(b.get("attribution_level", "")).upper()
    alpha = b.get("attribution")

    if cls in SOFT_CLASSES:
        reasons.append("soft benefit — never monetised, separate panel")
    if rung == "B4":
        reasons.append("baseline rung B4 (industry proxy) — illustrative only, no dollar headline")
    if rung not in {"B1", "B2", "B3", "B4"}:
        reasons.append(f"baseline rung '{b.get('baseline_rung')}' not one of B1-B4")
    if level == "A4":
        reasons.append("attribution level A4 (correlation only) — no dollar claim")
    if level not in {"A1", "A2", "A3", "A4"}:
        reasons.append(f"attribution level '{b.get('attribution_level')}' not one of A1-A4")
    if alpha is None:
        reasons.append("no attribution factor set")
    elif alpha >= 1.0 and cls != "hard_cash":
        reasons.append("alpha = 1.0 on a non-cash line — a silent 100% is refused")
    elif not 0 < alpha <= 1.0:
        reasons.append(f"alpha {alpha} outside (0, 1]")
    if cls == "risk_reduced" and b.get("inputs", {}).get("probability_source") != "customer":
        reasons.append("risk-reduction probability is not customer-supplied (R22)")
    if not b.get("attribution_set_by") and cls != "hard_cash":
        reasons.append("no attester named for the attribution factor")

    missing = [k for k in CLASS_INPUTS.get(cls, []) if b.get("inputs", {}).get(k) is None]
    if cls not in CLASS_INPUTS and cls not in SOFT_CLASSES:
        reasons.append(f"unknown benefit class '{cls}'")
    if missing:
        reasons.append("missing inputs: " + ", ".join(missing))

    return (not reasons), reasons


def band_for(b: dict) -> str:
    rung = str(b.get("baseline_rung", "")).upper()
    design = str(b.get("design", "")).upper()
    level = str(b.get("attribution_level", "")).upper()
    ue = b.get("unit_economics_source", "")
    if rung == "B4" or level == "A4":
        return "Indicative"
    # A cash-releasing line needs no counterfactual: the money already left the budget.
    if b.get("class") == "hard_cash":
        return "Measured" if (rung in {"B1", "B2"} and ue == "customer") else "Attested"
    if ue != "customer" or design in {"D4", "D5"}:
        return "Evidenced"
    if rung in {"B1", "B2"} and design in {"D1", "D2", "D3"} and level in {"A1", "A3"}:
        return "Measured"
    return "Attested"


# --------------------------------------------------------------------------- arithmetic

def gross(b: dict, mult: dict) -> tuple[float, list[str]]:
    """Gross benefit before recapture, attribution and haircut. `mult` scales one driver."""
    i = b.get("inputs", {})
    cls = b["class"]
    steps: list[str] = []
    if cls == "time_released":
        hours = (i["users"] * i["adoption"]
                 * i["hours_per_user_per_week"] * mult["hours"] * i["weeks"])
        hourly = i["loaded_hourly"] * mult["loaded_hourly"]
        g = hours * hourly
        steps.append(f"{i['users']} users x {i['adoption']} adoption x "
                     f"{i['hours_per_user_per_week'] * mult['hours']:.3g} h/week x {i['weeks']} weeks "
                     f"= {hours:,.0f} hours")
        steps.append(f"{hours:,.0f} h x {rate(hourly)}/h = {money(g)} gross")
    elif cls == "cost_avoided":
        g = i["baseline_unit_cost"] * i["volume_today"] - i["actual_cost"]
        steps.append(f"({rate(i['baseline_unit_cost'])} x {i['volume_today']:,.0f}) - "
                     f"{money(i['actual_cost'])} = {money(g)} gross")
    elif cls == "error_reduction":
        g = i["error_rate_delta"] * i["volume"] * i["cost_per_error"]
        steps.append(f"{i['error_rate_delta']:.4g} x {i['volume']:,.0f} x "
                     f"{rate(i['cost_per_error'])} = {money(g)} gross")
    elif cls == "revenue_influenced":
        g = i["conversion_delta"] * i["opportunity_volume"] * i["avg_deal_value"]
        steps.append(f"{i['conversion_delta']:.4g} x {i['opportunity_volume']:,.0f} x "
                     f"{money(i['avg_deal_value'])} = {money(g)} gross")
    elif cls == "risk_reduced":
        g = i["probability_delta"] * i["loss_magnitude"]
        steps.append(f"{i['probability_delta']:.4g} x {money(i['loss_magnitude'])} = "
                     f"{money(g)} expected value")
    elif cls == "headcount_avoided":
        fte = i["volume_delta"] / i["throughput_per_fte"]
        g = fte * i["loaded_fte_cost"]
        steps.append(f"{i['volume_delta']:,.0f} / {i['throughput_per_fte']:,.0f} = {fte:.2f} FTE")
        steps.append(f"{fte:.2f} FTE x {money(i['loaded_fte_cost'])} = {money(g)} gross")
    elif cls == "hard_cash":
        g = i["amount"]
        steps.append(f"cash released = {money(g)}")
    else:
        g = 0.0
    return g, steps


def line_value(b: dict, mult: dict, apply_haircut: bool) -> tuple[float, list[str]]:
    g, steps = gross(b, mult)
    v = g
    i = b.get("inputs", {})
    if b["class"] == "time_released":
        rec = min(1.0, i["recapture"] * mult["recapture"])
        v *= rec
        steps.append(f"x {rec:.2f} recapture = {money(v)}")
    if b["class"] != "hard_cash":
        alpha = min(1.0, b["attribution"] * mult["attribution"])
        v *= alpha
        steps.append(f"x {alpha:.2f} attribution ({b['attribution_level']}) = {money(v)}")
    if apply_haircut and b.get("haircut"):
        v *= (1 - b["haircut"])
        steps.append(f"x {1 - b['haircut']:.2f} haircut ({b.get('haircut_reason', 'unstated')}) "
                     f"= {money(v)}")
    return v, steps


def multipliers(driver: str, m: float) -> dict:
    base = {"attribution": 1.0, "recapture": 1.0, "loaded_hourly": 1.0, "hours": 1.0}
    if driver not in base:
        raise SystemExit(f"sensitivity_driver must be one of {sorted(base)}; got '{driver}'")
    base[driver] = m
    return base


def total(case: dict, m: float, apply_haircut: bool) -> float:
    mult = multipliers(case.get("sensitivity_driver", "attribution"), m)
    t = 0.0
    for b in case["benefits"]:
        ok, _ = gate(b)
        if not ok:
            continue
        t += line_value(b, mult, apply_haircut)[0]
    return t


def break_even(case: dict, cost: float) -> float | None:
    """Bisect for the driver multiplier at which conservative benefit equals total cost."""
    lo, hi = 0.0, 5.0
    if total(case, hi, True) < cost:
        return None
    if total(case, lo, True) >= cost:
        return 0.0
    for _ in range(200):
        mid = (lo + hi) / 2
        if total(case, mid, True) < cost:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


# --------------------------------------------------------------------------- report

def run(case: dict, explain: bool = False) -> dict:
    months = case.get("period_months", 12)
    costs = case.get("costs", {})
    cost_total = sum(v for v in costs.values() if isinstance(v, (int, float)))
    driver = case.get("sensitivity_driver", "attribution")

    lines, blocked, bands = [], [], []
    for b in case["benefits"]:
        ok, reasons = gate(b)
        if not ok:
            blocked.append({"name": b.get("name", "?"), "class": b.get("class"),
                            "reasons": reasons})
            continue
        cons, steps = line_value(b, multipliers(driver, 0.7), True)
        cent, _ = line_value(b, multipliers(driver, 1.0), True)
        stre, _ = line_value(b, multipliers(driver, 1.3), False)
        band = band_for(b)
        bands.append(band)
        lines.append({"name": b["name"], "class": b["class"], "band": band,
                      "rung": b.get("baseline_rung"), "design": b.get("design"),
                      "alpha": b.get("attribution"), "level": b.get("attribution_level"),
                      "set_by": b.get("attribution_set_by"),
                      "conservative": cons, "central": cent, "stretch": stre,
                      "steps": steps})

    cons_t = sum(l["conservative"] for l in lines)
    cent_t = sum(l["central"] for l in lines)
    stre_t = sum(l["stretch"] for l in lines)
    be = break_even(case, cost_total)

    def payback(benefit: float) -> float | None:
        if benefit <= 0:
            return None
        return cost_total / (benefit / months)

    result = {
        "account": case.get("account"), "period": case.get("period"),
        "as_of": case.get("as_of"), "period_months": months,
        "sensitivity_driver": driver,
        "cost_total": cost_total, "cost_components": costs,
        "conservative": cons_t, "central": cent_t, "stretch": stre_t,
        "headline_rounded": two_sig(cons_t),
        "net_benefit": cons_t - cost_total,
        "roi": (cons_t - cost_total) / cost_total if cost_total else None,
        "payback_months": payback(cons_t),
        "payback_months_central": payback(cent_t),
        "break_even_driver_multiplier": be,
        "band": weakest(bands),
        "lines": lines, "blocked": blocked,
        "exclusions": case.get("exclusions", []),
    }
    if explain:
        result["explain"] = True
    return result


def render(r: dict) -> str:
    o: list[str] = []
    o.append(f"VALUE CASE — {r['account']} · {r['period']} · as-of {r['as_of']}")
    o.append("=" * 78)
    o.append("")
    o.append(f"  Conservative (headline)  {money(r['conservative'])}   "
             f"state it as {r['headline_rounded']}")
    o.append(f"  Central / Stretch        {money(r['central'])} / {money(r['stretch'])}")
    o.append(f"  Customer cost in period  {money(r['cost_total'])}")
    o.append(f"  Net benefit              {money(r['net_benefit'])}")
    if r["roi"] is not None:
        o.append(f"  ROI                      {r['roi']:.2f} -> {1 + r['roi']:.2f}x return")
    if r["payback_months"]:
        o.append(f"  Payback (conservative)   {r['payback_months']:.1f} months"
                 + (f"   (central {r['payback_months_central']:.1f})"
                    if r["payback_months_central"] else ""))
    else:
        o.append("  Payback                  NOT REACHED on the conservative case")
    o.append(f"  Defensibility band       {r['band']}  (weakest contributing line)")
    o.append("")

    o.append("BENEFIT LINES")
    o.append(f"  {'line':<28}{'class':<20}{'band':<11}{'alpha rec':>10}  {'conservative':>13}")
    for l in r["lines"]:
        o.append(f"  {l['name'][:27]:<28}{l['class']:<20}{l['band']:<11}"
                 f"{l['alpha']:>10.2f}  {money(l['conservative']):>13}")
    o.append(f"  {'TOTAL':<28}{'':<20}{'':<11}{'':>10}  {money(r['conservative']):>13}")
    o.append("")

    if r.get("explain"):
        o.append("ARITHMETIC (conservative scenario)")
        for l in r["lines"]:
            o.append(f"  {l['name']}  [{l['rung']} · {l['design']} · {l['level']} "
                     f"set by {l['set_by']}]")
            for s in l["steps"]:
                o.append(f"     {s}")
        o.append("")

    if r["blocked"]:
        o.append("NOT PRESENTABLE — unit metrics only, no dollar figure")
        for b in r["blocked"]:
            o.append(f"  {b['name']} ({b['class']})")
            for reason in b["reasons"]:
                o.append(f"     - {reason}")
        o.append("")

    o.append("COST SIDE")
    for k, v in r["cost_components"].items():
        o.append(f"  {k.replace('_', ' '):<34}{money(v):>12}")
    o.append(f"  {'TOTAL':<34}{money(r['cost_total']):>12}")
    o.append("")

    o.append(f"SENSITIVITY — driver: {r['sensitivity_driver']}")
    o.append(f"  {'multiplier':<14}{'benefit':>14}{'payback (months)':>20}")
    for label, mult, val in (("-30% conserv.", 0.7, r["conservative"]),
                             ("central", 1.0, r["central"]),
                             ("+30% stretch", 1.3, r["stretch"])):
        pb = (r["cost_total"] / (val / r["period_months"])) if val > 0 else None
        o.append(f"  {label:<14}{money(val):>14}"
                 + (f"{pb:>20.1f}" if pb else f"{'not reached':>20}"))
    be = r["break_even_driver_multiplier"]
    if be is None:
        o.append("  break-even: NOT REACHABLE within a 5x move on this driver — "
                 "the case does not pay back on this driver alone")
    else:
        o.append(f"  break-even: driver at {be:.2f}x its recorded value "
                 f"(net benefit = cost at that point)")
    o.append("")

    if r["exclusions"]:
        o.append("NOT COUNTED IN THIS FIGURE")
        for e in r["exclusions"]:
            o.append(f"  - {e}")
        o.append("")

    o.append("Bands: Measured > Attested > Evidenced > Indicative. The case band is the weakest")
    o.append("contributing line. B4 baselines and A4 attribution carry no dollar figure.")
    return "\n".join(o)


def main() -> int:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    flags = {a for a in sys.argv[1:] if a.startswith("--")}
    here = Path(__file__).resolve().parent

    if "--demo" in flags or not args:
        path = here / "sample_case.json"
        if not path.exists():
            print("no input file given and sample_case.json is missing", file=sys.stderr)
            return 2
    else:
        path = Path(args[0])
        if not path.exists():
            print(f"no such file: {path}", file=sys.stderr)
            return 2

    case = json.loads(path.read_text())
    r = run(case, explain="--explain" in flags)
    if "--json" in flags:
        r.pop("explain", None)
        print(json.dumps(r, indent=2))
    else:
        print(render(r))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
