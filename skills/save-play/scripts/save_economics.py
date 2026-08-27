#!/usr/bin/env python3
"""
Save-play economics — deterministic arithmetic for the stop-loss decision.

Answers four questions a war room argues about badly without numbers:

  1. How much runway is left?        opt_out_deadline = renewal_date - notice_period_days
  2. What is actually at stake?      retained gross profit over the planning horizon
  3. What does the play cost?        fully loaded hours by role + concession cost
  4. When do we stop?                P* = (play cost + concession cost) / retained gross profit
                                     and the discount ceiling beyond which saving loses money

P* is the BREAK-EVEN SAVE PROBABILITY: the minimum chance of saving at which the play is worth
running. Compare it against the savability BAND for the diagnosed root cause -- never against an
invented per-account probability (R22). Bands are ordinal planning conventions [P], not measured
rates; replace them with your own backtested rates once churn-postmortem has coded 20+ plays.

Usage
    python3 save_economics.py accounts.json [--today YYYY-MM-DD] [--json]
    python3 save_economics.py sample_saves.json --today 2026-08-28

Input: a JSON list of objects, or {"accounts": [...]}. Only `name` and `arr` are required.

    {
      "name": "Acme Corp",
      "arr": 148000,
      "renewal_date": "2027-02-01",
      "notice_period_days": 90,
      "gross_margin_pct": 0.78,          default 0.75
      "horizon_years": 2.0,              default 1.0 -- one renewal cycle
      "root_cause": "RC6",
      "savability_band": "moderate",     high | moderate | low | structural
      "scenario": "full_churn",          full_churn | downsell
      "downsell_pct": 0.30,              share of ARR at risk when scenario = downsell
      "hours": {"csm": 12, "exec": 4, "engineering": 0, "services": 0, "am": 6},
      "concession": {"discount_pct": 0.05, "credits": 4000}
    }

Stdlib only. No network. Every figure is printed with the arithmetic that produced it.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date, datetime

# Fully loaded hourly cost by role, in the reporting currency. These are configurable defaults,
# not benchmarks -- override with your own via `loaded_rates` on any account object.
DEFAULT_RATES: dict[str, float] = {
    "csm": 85.0,
    "am": 95.0,
    "exec": 220.0,
    "engineering": 140.0,
    "services": 120.0,
    "support": 75.0,
    "solutions": 130.0,
}

# Ordinal planning conventions [P] -- the midpoint used only to say whether P* sits above or below
# the band. Never printed as a probability for an individual account.
BAND_MIDPOINT: dict[str, float] = {
    "high": 0.70,
    "moderate": 0.45,
    "low": 0.20,
    "structural": 0.05,
}

DEFAULT_GROSS_MARGIN = 0.75
DEFAULT_HORIZON_YEARS = 1.0
DEFAULT_NOTICE_DAYS = 30  # Common Paper 2026 SaaS Contract Benchmark: ~70% of CSAs use 30 days [M]


def parse_date(value: str | None) -> date | None:
    if not value:
        return None
    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y", "%Y/%m/%d"):
        try:
            return datetime.strptime(str(value).strip()[:10], fmt).date()
        except ValueError:
            continue
    return None


def money(value: float) -> str:
    """Composite/modelled figures round to two significant figures (R22).

    Costs built from real hours and real rates are measurements, not models, so they print
    exactly below $10k -- rounding them would hide the arithmetic a reviewer needs to audit.
    """
    if value is None:
        return "UNKNOWN"
    a = abs(value)
    if a >= 1_000_000:
        return f"${value / 1_000_000:.2f}M"
    if a >= 10_000:
        return f"${value / 1_000:.0f}k"
    return f"${value:,.0f}"


class Result:
    def __init__(self, account: dict, today: date) -> None:
        self.name = account.get("name") or account.get("account") or "UNKNOWN"
        self.notes: list[str] = []

        arr = account.get("arr")
        self.arr = float(arr) if arr not in (None, "") else None
        if self.arr is None:
            self.notes.append("UNKNOWN — requires account.arr; no economics computed")

        self.margin = float(account.get("gross_margin_pct", DEFAULT_GROSS_MARGIN))
        self.horizon = float(account.get("horizon_years", DEFAULT_HORIZON_YEARS))
        self.cause = account.get("root_cause", "UNKNOWN")
        self.band = str(account.get("savability_band", "")).lower() or None
        if self.band and self.band not in BAND_MIDPOINT:
            self.notes.append(f"savability_band '{self.band}' unrecognised — treated as unknown")
            self.band = None

        # --- clock (R1) -------------------------------------------------------------------
        self.renewal = parse_date(account.get("renewal_date"))
        notice = account.get("notice_period_days")
        if notice in (None, ""):
            self.notice = DEFAULT_NOTICE_DAYS
            self.notes.append(
                "notice_period_days missing — assumed 30 (the shorter, safer figure). "
                "UNKNOWN — requires the contract notice clause"
            )
        else:
            self.notice = int(notice)

        if self.renewal:
            self.opt_out = date.fromordinal(self.renewal.toordinal() - self.notice)
            self.runway = (self.opt_out - today).days
        else:
            self.opt_out = None
            self.runway = None
            self.notes.append("UNKNOWN — requires subscription.renewal_date; runway not computed")

        # --- value at stake ---------------------------------------------------------------
        scenario = str(account.get("scenario", "full_churn")).lower()
        share = 1.0
        if scenario == "downsell":
            share = float(account.get("downsell_pct", 0.30))
        self.scenario = scenario
        self.arr_at_stake = self.arr * share if self.arr is not None else None
        self.retained_gp = (
            self.arr_at_stake * self.margin * self.horizon
            if self.arr_at_stake is not None else None
        )

        # --- cost of the play -------------------------------------------------------------
        rates = dict(DEFAULT_RATES)
        rates.update({k: float(v) for k, v in (account.get("loaded_rates") or {}).items()})
        self.hours = {k: float(v) for k, v in (account.get("hours") or {}).items() if float(v) > 0}
        self.cost_lines: list[tuple[str, float, float, float]] = []
        for role, hrs in sorted(self.hours.items()):
            rate = rates.get(role)
            if rate is None:
                self.notes.append(f"no loaded rate for role '{role}' — excluded from play cost")
                continue
            self.cost_lines.append((role, hrs, rate, hrs * rate))
        self.play_cost = sum(line[3] for line in self.cost_lines)
        if not self.cost_lines:
            self.notes.append("no hours supplied — play cost is $0, which is certainly wrong")

        conc = account.get("concession") or {}
        self.discount_pct = float(conc.get("discount_pct", 0.0))
        self.credits = float(conc.get("credits", 0.0))
        self.concession_cost = (
            self.arr_at_stake * self.discount_pct * self.horizon + self.credits
            if self.arr_at_stake is not None else self.credits
        )

        # --- the decision -----------------------------------------------------------------
        self.total_cost = self.play_cost + self.concession_cost
        if self.retained_gp and self.retained_gp > 0:
            self.p_star = self.total_cost / self.retained_gp
            # Discount at which retained gross profit exactly equals the cost of the play.
            gp_per_point = self.arr_at_stake * self.margin * self.horizon
            self.discount_ceiling = max(
                0.0, (gp_per_point - self.play_cost - self.credits) / gp_per_point
            ) if gp_per_point > 0 else 0.0
        else:
            self.p_star = None
            self.discount_ceiling = None

        self.expected_value = (
            BAND_MIDPOINT[self.band] * self.retained_gp - self.total_cost
            if (self.band and self.retained_gp is not None) else None
        )
        planned = sum(self.hours.values())
        self.value_per_hour = (
            (BAND_MIDPOINT[self.band] * self.retained_gp) / planned
            if (self.band and self.retained_gp is not None and planned > 0) else None
        )

    # -------------------------------------------------------------------------------------
    def call(self) -> tuple[str, str]:
        """Returns (verdict, one-line reason). Never states a probability for this account."""
        if self.retained_gp is None:
            return "INSUFFICIENT", "no ARR supplied; cannot value the save"
        if self.band == "structural":
            return "EXIT", "structural cause — not savable as sold; restructure or exit"
        if self.runway is not None and self.runway <= 0:
            return "EXIT", "the opt-out deadline has passed; this is now a managed exit"
        if self.p_star is None:
            return "INSUFFICIENT", "no gross profit at stake"
        if self.p_star >= 1.0:
            return "EXIT", "break-even probability exceeds 100% — the play costs more than the outcome"
        if self.band and self.p_star > BAND_MIDPOINT[self.band]:
            return "RESTRUCTURE", (
                f"P* {self.p_star:.0%} sits above the {self.band} savability band — "
                "cut the play cost, cut the concession, or restructure"
            )
        if self.runway is not None and self.runway < 14:
            return "RESTRUCTURE", "under 14 days of runway; only a structural offer can land in time"
        return "CONTINUE", (
            f"P* {self.p_star:.0%}"
            + (f" sits below the {self.band} savability band" if self.band else " — band not supplied")
        )

    def to_dict(self) -> dict:
        verdict, reason = self.call()
        return {
            "account": self.name,
            "root_cause": self.cause,
            "savability_band": self.band,
            "opt_out_deadline": self.opt_out.isoformat() if self.opt_out else None,
            "runway_days": self.runway,
            "arr": self.arr,
            "arr_at_stake": self.arr_at_stake,
            "retained_gross_profit": round(self.retained_gp, 2) if self.retained_gp else None,
            "play_cost": round(self.play_cost, 2),
            "concession_cost": round(self.concession_cost, 2),
            "break_even_save_probability": round(self.p_star, 4) if self.p_star else None,
            "discount_ceiling": round(self.discount_ceiling, 4) if self.discount_ceiling else None,
            "expected_value_at_band_midpoint": round(self.expected_value, 2) if self.expected_value else None,
            "value_per_planned_hour": round(self.value_per_hour, 2) if self.value_per_hour else None,
            "call": verdict,
            "reason": reason,
            "notes": self.notes,
        }

    def render(self) -> str:
        verdict, reason = self.call()
        out: list[str] = []
        out.append("=" * 78)
        out.append(f"{self.name}  ·  cause {self.cause}  ·  savability {self.band or 'UNKNOWN'} [P]")
        out.append("=" * 78)

        out.append("\nCLOCK (R1)")
        if self.opt_out:
            out.append(f"  renewal {self.renewal}  −  notice {self.notice}d  =  opt-out {self.opt_out}")
            urgency = "PAST" if self.runway < 0 else ("critical" if self.runway < 14 else
                                                      "tight" if self.runway < 45 else "workable")
            out.append(f"  runway: {self.runway} days ({urgency})")
        else:
            out.append("  UNKNOWN — requires subscription.renewal_date")

        out.append("\nVALUE AT STAKE")
        if self.arr_at_stake is not None:
            scen = ("full loss" if self.scenario == "full_churn"
                    else f"downsell of {self.arr_at_stake / self.arr:.0%}")
            out.append(f"  ARR {money(self.arr)} · scenario {scen} → ARR at stake {money(self.arr_at_stake)}")
            out.append(f"  retained gross profit = {money(self.arr_at_stake)} × {self.margin:.0%} margin "
                       f"× {self.horizon:g}y = {money(self.retained_gp)}")
        else:
            out.append("  UNKNOWN — requires account.arr")

        out.append("\nCOST OF THE PLAY")
        for role, hrs, rate, cost in self.cost_lines:
            out.append(f"  {role:<13} {hrs:>6.1f} h × ${rate:>6.0f}/h = {money(cost):>10}")
        out.append(f"  {'play cost':<13} {sum(self.hours.values()):>6.1f} h"
                   f"{'':>16} = {money(self.play_cost):>10}")
        if self.discount_pct or self.credits:
            out.append(f"  concession    {self.discount_pct:.1%} discount + {money(self.credits)} credits"
                       f" = {money(self.concession_cost):>10}")
        out.append(f"  {'TOTAL':<13}{'':>25} = {money(self.total_cost):>10}")

        out.append("\nTHE DECISION (R21)")
        if self.p_star is not None:
            out.append(f"  P* = ({money(self.play_cost)} + {money(self.concession_cost)}) / "
                       f"{money(self.retained_gp)} = {self.p_star:.1%}")
            out.append("       the minimum chance of saving at which this play breaks even")
            if self.band:
                out.append(f"  band: {self.band} [P] — a planning convention, not a measured rate (R22)")
            if self.discount_ceiling is not None:
                out.append(f"  discount ceiling: {self.discount_ceiling:.1%} "
                           "(above this, saving is worth less than losing)")
                out.append("       gross profit is the outer bound only — the approval ladder in "
                           "references/plays.md")
                out.append("       binds first, and every rung must still buy a named get")
            if self.value_per_hour is not None:
                out.append(f"  value per planned hour: {money(self.value_per_hour)} "
                           "(use this to rank two live plays)")
        out.append(f"\n  CALL: {verdict} — {reason}")

        if self.notes:
            out.append("\nNOTES")
            for n in self.notes:
                out.append(f"  · {n}")
        return "\n".join(out)


def load(path: str) -> list[dict]:
    with open(path, encoding="utf-8") as fh:
        data = json.load(fh)
    if isinstance(data, dict):
        data = data.get("accounts", data.get("saves", []))
    if not isinstance(data, list):
        raise SystemExit("input must be a JSON list, or an object with an 'accounts' key")
    return data


def main() -> int:
    ap = argparse.ArgumentParser(description="Save-play economics and stop-loss arithmetic.")
    ap.add_argument("input", help="JSON file of accounts in an open or proposed save play")
    ap.add_argument("--today", default=date.today().isoformat(), help="as-of date, YYYY-MM-DD")
    ap.add_argument("--json", action="store_true", help="emit machine-readable JSON")
    args = ap.parse_args()

    today = parse_date(args.today)
    if today is None:
        raise SystemExit(f"could not parse --today '{args.today}'")

    results = [Result(a, today) for a in load(args.input)]

    if args.json:
        print(json.dumps([r.to_dict() for r in results], indent=2))
        return 0

    print(f"\nSave-play economics · as-of {today} · {len(results)} account(s)")
    print("INTERNAL. Contains exposure and commercial figures. Never shown to a customer (R18).")
    for r in results:
        print()
        print(r.render())

    print("\n" + "=" * 78)
    print("RANKED BY VALUE PER PLANNED HOUR (where a savability band was supplied)")
    print("=" * 78)
    ranked = sorted(
        [r for r in results if r.value_per_hour is not None],
        key=lambda r: r.value_per_hour, reverse=True,
    )
    if not ranked:
        print("  no account had both a savability band and planned hours")
    for i, r in enumerate(ranked, 1):
        verdict, _ = r.call()
        runway = f"{r.runway}d" if r.runway is not None else "—"
        print(f"  {i}. {r.name:<22} {money(r.value_per_hour):>9}/h  "
              f"P* {r.p_star:>5.0%}  runway {runway:>5}  {verdict}")
    print("\nBands are ordinal planning conventions [P], not measured save rates. Replace them with")
    print("your own backtested rates by root cause once churn-postmortem has coded 20+ closed plays.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
