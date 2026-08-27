#!/usr/bin/env python3
"""
The CS headcount / budget case, computed deterministically, for the
`exec-retention-review` skill.

Why a script: this is the arithmetic a CFO re-does on the back of an envelope while you are
still talking. It must be right, it must show every step, and it must produce the breakeven
BEFORE the expected case — because breakeven is falsifiable and a forecast is discounted.

Produces
--------
  * Coverage waterfall and the uncovered-ARR disclosure
  * Bottom-up capacity: accounts a CSM can carry at each tier, and the resulting gap in heads
  * Fully loaded cost of the ask
  * Breakeven retained ARR, breakeven GRR improvement, breakeven save rate
  * Expected case from the OBSERVED covered/uncovered differential (never a benchmark)
  * Margin of safety, simple payback in months
  * The counterfactual prompt and the kill-criterion prompt, unfilled

Usage
-----
    python3 headcount_case.py sample_case.json
    python3 headcount_case.py --emit-sample > sample_case.json

No network access. Standard library only. Any input that is null prints
`UNKNOWN — requires <field>` and the dependent line is skipped, never estimated.
"""

from __future__ import annotations

import argparse
import json
from typing import Any

BPS = 10_000.0


def money(x: float) -> str:
    sign = "-" if x < 0 else ""
    return f"{sign}${abs(x):,.0f}"


def pct(x: float, dp: int = 1) -> str:
    return f"{x * 100:.{dp}f}%"


def bps(x: float) -> str:
    return f"{x * BPS:,.0f} bps"


def head(t: str) -> None:
    print(f"\n{t}\n" + "-" * len(t))


def coverage(d: dict[str, Any]) -> float:
    head("1. COVERAGE WATERFALL")
    tiers = d["coverage"]
    total = sum(t["arr"] for t in tiers)
    hdr = f"{'Tier':<16}{'ARR':>16}{'% of ARR':>11}{'Accounts':>10}{'GRR (TTM)':>12}"
    print(hdr)
    print("-" * len(hdr))
    uncovered = 0.0
    for t in tiers:
        grr = t.get("grr")
        print(f"{t['tier']:<16}{money(t['arr']):>16}{pct(t['arr'] / total, 1):>11}"
              f"{t['accounts']:>10}{(pct(grr, 1) if grr is not None else 'UNKNOWN'):>12}")
        if t["tier"].lower().startswith("uncovered"):
            uncovered = t["arr"]
    print("-" * len(hdr))
    print(f"{'TOTAL':<16}{money(total):>16}{'100.0%':>11}"
          f"{sum(t['accounts'] for t in tiers):>10}")
    print(f"\nUNCOVERED ARR: {money(uncovered)} ({pct(uncovered / total, 1)} of ARR) "
          "— this is the board-relevant disclosure.")
    win = d.get("uncovered_arr_in_optout_window")
    if win is not None:
        print(f"Of which decides inside the planning horizon (by OPT-OUT DEADLINE, "
              f"not renewal date): {money(win)}")
    else:
        print("Uncovered ARR inside the opt-out window: UNKNOWN — requires "
              "`uncovered_arr_in_optout_window` (subscription.opt_out_deadline).")
    return uncovered


def capacity(d: dict[str, Any]) -> None:
    head("2. BOTTOM-UP CAPACITY (ratios are the OUTPUT, never the input)")
    c = d.get("capacity")
    if not c:
        print("UNKNOWN — requires `capacity` (annual hours, internal share, hours per account "
              "by tier). Ratios alone are not a capacity argument.")
        return
    avail = c["annual_hours"] * (1 - c["internal_share"])
    print(f"Annual hours per CSM              : {c['annual_hours']:,}")
    print(f"Internal share (meetings, admin)  : {pct(c['internal_share'], 0)}")
    print(f"Customer-facing hours per CSM     : {avail:,.0f}")
    print(f"\n{'Tier':<16}{'Hrs/acct/yr':>13}{'Accts per CSM':>16}{'Accounts':>11}{'CSMs needed':>14}")
    print("-" * 70)
    total_needed = 0.0
    for t in c["tiers"]:
        per_csm = avail / t["hours_per_account_year"]
        needed = t["accounts"] / per_csm
        total_needed += needed
        print(f"{t['tier']:<16}{t['hours_per_account_year']:>13.0f}{per_csm:>16.0f}"
              f"{t['accounts']:>11}{needed:>14.1f}")
    print("-" * 70)
    have = c["csm_fte_today"]
    print(f"{'TOTAL NEEDED':<16}{'':>13}{'':>16}{'':>11}{total_needed:>14.1f}")
    print(f"{'IN SEAT TODAY':<16}{'':>13}{'':>16}{'':>11}{have:>14.1f}")
    print(f"{'GAP':<16}{'':>13}{'':>16}{'':>11}{total_needed - have:>14.1f}")
    print("\nHour assumptions above are planning conventions [P] — replace them with a time "
          "study of your own team before this reaches a CFO.")


def economics(d: dict[str, Any], uncovered: float) -> None:
    head("3. THE ASK: COST, BREAKEVEN, EXPECTED CASE")
    a = d["ask"]
    heads = a["heads"]
    loaded = a["fully_loaded_cost_per_head"]
    cost = heads * loaded
    gm = d["subscription_gross_margin"]

    print(f"Heads requested                   : {heads}")
    print(f"Fully loaded cost per head        : {money(loaded)}")
    print(f"TOTAL FULLY LOADED COST           : {money(cost)}")
    print(f"Subscription gross margin         : {pct(gm, 0)}")

    be_arr = cost / gm
    book = a.get("arr_the_hire_covers", uncovered)
    at_risk = d.get("at_risk_arr_in_book")

    head("   Breakeven — stated before the expected case, because it is falsifiable")
    print(f"Breakeven retained ARR            : {money(cost)} / {pct(gm, 0)} = {money(be_arr)}")
    print(f"Book the hire covers              : {money(book)}")
    be_grr = be_arr / book
    print(f"Breakeven GRR improvement         : {money(be_arr)} / {money(book)} = {bps(be_grr)}")
    if at_risk:
        print(f"At-risk ARR in that book          : {money(at_risk)}")
        print(f"Breakeven save rate on at-risk    : {money(be_arr)} / {money(at_risk)} "
              f"= {pct(be_arr / at_risk, 1)}")
    else:
        print("Breakeven save rate               : UNKNOWN — requires `at_risk_arr_in_book`.")

    grr_cov = d.get("grr_covered")
    grr_unc = d.get("grr_uncovered")
    head("   Expected case — from the OBSERVED differential, never a benchmark")
    if grr_cov is None or grr_unc is None:
        print("UNKNOWN — requires `grr_covered` and `grr_uncovered` for the same segment and "
              "period. Without both, make the breakeven argument only; do not substitute an "
              "industry retention benchmark.")
        return
    diff = grr_cov - grr_unc
    print(f"GRR, covered book                 : {pct(grr_cov, 1)}")
    print(f"GRR, uncovered book               : {pct(grr_unc, 1)}")
    print(f"Observed differential             : {bps(diff)}")
    retained = book * diff
    gp = retained * gm
    print(f"Expected retained ARR             : {money(book)} x {bps(diff)} = {money(retained)}")
    print(f"Expected gross profit             : {money(gp)}")
    if gp > 0:
        print(f"Simple payback                    : {money(cost)} / ({money(gp)}/12) "
              f"= {cost / (gp / 12):.1f} months")
    mos = (diff - be_grr) / be_grr if be_grr else 0.0
    print(f"Margin of safety                  : ({bps(diff)} - {bps(be_grr)}) / {bps(be_grr)} "
          f"= {pct(mos, 1)}")
    if mos < 0:
        print("  The observed differential does NOT clear breakeven. Do not make this ask as "
              "written — reduce the heads, retarget the book, or make a different argument.")
    elif mos < 0.25:
        print("  Thin margin of safety. Say so out loud — conceding it is what makes the rest "
              "of the case credible — and ask for fewer heads than the model would allow.")
    else:
        print("  Comfortable margin of safety. Still state the counterfactual and the kill "
              "criterion unprompted.")

    print("\nNote: LTV is deliberately not used here. The same company can produce a naive, a "
          "gross-margin-adjusted and a discounted LTV that differ by 2x; an LTV quoted without "
          "its formula is unreviewable. Retained gross profit is the reviewable number.")


def closing(d: dict[str, Any]) -> None:
    head("4. WHAT YOU MUST STILL WRITE YOURSELF")
    cf = d.get("counterfactual", {})
    print("Counterfactual (state it before you are asked):")
    print(f"  What does not get done          : {cf.get('not_done') or 'UNKNOWN — write this'}")
    print(f"  What the exposure becomes       : {cf.get('exposure') or 'UNKNOWN — write this'}")
    print(f"  Zero-cost trade you will make   : {cf.get('zero_cost_trade') or 'UNKNOWN — write this'}")
    k = d.get("kill_criterion")
    print(f"\nKill criterion                    : {k or 'UNKNOWN — write this. Offering one '
          'converts a spend into an experiment, and almost nobody offers one.'}")
    print("\nEvery line of the ask needs: action - owner - date - cost - expected effect - "
          "success measure - review date.")


SAMPLE: dict[str, Any] = {
    "subscription_gross_margin": 0.81,
    "coverage": [
        {"tier": "Named 1:1", "arr": 61_300_000, "accounts": 240, "grr": 0.914},
        {"tier": "Pooled", "arr": 24_800_000, "accounts": 410, "grr": 0.883},
        {"tier": "Digital", "arr": 17_200_000, "accounts": 658, "grr": 0.861},
        {"tier": "Uncovered", "arr": 14_200_000, "accounts": 62, "grr": 0.880},
    ],
    "uncovered_arr_in_optout_window": 5_400_000,
    "at_risk_arr_in_book": 2_200_000,
    "grr_covered": 0.914,
    "grr_uncovered": 0.880,
    "capacity": {
        "annual_hours": 2000,
        "internal_share": 0.33,
        "csm_fte_today": 11.7,
        "tiers": [
            {"tier": "High-touch", "hours_per_account_year": 40, "accounts": 302},
            {"tier": "Mid-touch", "hours_per_account_year": 12, "accounts": 410},
            {"tier": "Low-touch", "hours_per_account_year": 2, "accounts": 658},
        ],
    },
    "ask": {
        "heads": 2,
        "fully_loaded_cost_per_head": 185_000,
        "arr_the_hire_covers": 14_200_000,
    },
    "counterfactual": {
        "not_done": "62 Enterprise and upper-Mid-Market accounts holding $14.2M stay uncovered",
        "exposure": "$5.4M of that decides on an opt-out deadline inside the next two quarters",
        "zero_cost_trade": "Move 42 Mid-Market accounts under $40k ARR to the digital programme "
                           "and cover the Enterprise gap with the existing team; that opens a "
                           "$3.1M Mid-Market gap and Mid-Market GRR is the bill",
    },
    "kill_criterion": "If uncovered-book GRR has not moved 150 bps by 31 March, I do not renew this ask",
}


def main() -> int:
    ap = argparse.ArgumentParser(description="CS headcount / budget case arithmetic.")
    ap.add_argument("input", nargs="?")
    ap.add_argument("--emit-sample", action="store_true")
    args = ap.parse_args()

    if args.emit_sample:
        print(json.dumps(SAMPLE, indent=2))
        return 0
    if not args.input:
        ap.error("provide an input JSON path, or use --emit-sample")

    with open(args.input, encoding="utf-8") as fh:
        d = json.load(fh)

    unc = coverage(d)
    capacity(d)
    economics(d, unc)
    closing(d)
    print("\n" + "=" * 78)
    print("Arithmetic only. No benchmark has been substituted for a company figure.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
