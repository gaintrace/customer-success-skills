#!/usr/bin/env python3
"""
Size a playbook library before switching any of it on.

Three deterministic calculations that must never be done in prose:

  1. FIRE RATE      distinct accounts firing per 30 days as a share of the eligible population,
                    with the band verdict from trigger-design.md §3.
  2. CAPACITY GATE  the weekly intake budget per CSM, derived from usable hours (R13), and
                    whether the modelled library fits inside it.
  3. POWER          the accounts per arm needed before a retention delta may be claimed
                    (two-proportion normal approximation), so "not powered" is a number
                    rather than an opinion.

Usage:
    python3 play_sizing.py sample-library.json
    python3 play_sizing.py sample-library.json --json
    python3 play_sizing.py --power --base 0.80 --delta 0.05
    python3 play_sizing.py --power-table

Standard library only. No network. Exit 0 clean, 1 over budget, 2 usage error.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

WEEKS_PER_MONTH = 4.33
USABLE_FRACTION = 0.60  # R13 — usable hours are roughly 60% of a nominal week

# Two-sided alpha=0.05, and power 0.80 / 0.90. Fixed constants keep this stdlib-only and
# auditable; anything else would need a normal quantile nobody can check by hand.
Z_ALPHA_TWO_SIDED = {0.05: 1.959964, 0.10: 1.644854, 0.01: 2.575829}
Z_POWER = {0.80: 0.841621, 0.90: 1.281552}


# --------------------------------------------------------------------------- fire rate


def band(fire_rate: float) -> tuple[str, str]:
    """Fire-rate verdict. Thresholds from trigger-design.md §3."""
    if fire_rate <= 0.02:
        return "healthy", "Ship it."
    if fire_rate <= 0.05:
        return "acceptable-if-cheap", "Only with a cheap action (task, in-app nudge, templated send)."
    if fire_rate <= 0.15:
        return "segment-not-trigger", "Tighten the qualifier, or publish it as a weekly list."
    return "report", "This is a report. Publish the list; page nobody."


def size_play(play: dict, eligible_default: int) -> dict:
    eligible = int(play.get("eligible_accounts") or eligible_default)
    fires = float(play["fires_per_30d"])
    if eligible <= 0:
        raise ValueError(f"play '{play.get('id')}' has no eligible population")
    rate = fires / eligible
    label, advice = band(rate)
    return {
        "id": play.get("id", "?"),
        "name": play.get("name", ""),
        "category": play.get("category", ""),
        "eligible_accounts": eligible,
        "fires_per_30d": fires,
        "fire_rate": rate,
        "band": label,
        "advice": advice,
        "hours_per_motion": float(play.get("hours_per_motion", 0.0)),
        "weeks_per_motion": float(play.get("weeks_per_motion", 1.0)),
        "automated": bool(play.get("automated", False)),
        "state": play.get("state", "live"),
    }


# ----------------------------------------------------------------------- capacity gate


def capacity_budget(cfg: dict) -> dict:
    nominal = float(cfg.get("nominal_hours_per_week", 40.0))
    proactive_share = float(cfg.get("proactive_share", 0.25))
    hours_per_motion = float(cfg.get("hours_per_motion", 4.0))
    weeks_per_motion = float(cfg.get("weeks_per_motion", 3.0))

    usable = nominal * USABLE_FRACTION
    proactive = usable * proactive_share
    if hours_per_motion <= 0 or weeks_per_motion <= 0:
        raise ValueError("hours_per_motion and weeks_per_motion must be positive")
    concurrent = proactive / (hours_per_motion / weeks_per_motion)
    weekly_intake = concurrent / weeks_per_motion
    return {
        "nominal_hours_per_week": nominal,
        "usable_hours_per_week": usable,
        "proactive_hours_per_week": proactive,
        "hours_per_motion": hours_per_motion,
        "weeks_per_motion": weeks_per_motion,
        "concurrent_motions_per_csm": concurrent,
        "weekly_intake_budget_per_csm": weekly_intake,
    }


def modelled_intake(plays: list[dict], csm_count: int) -> float:
    """Human-run plays only — an automated send costs no CSM intake."""
    if csm_count <= 0:
        raise ValueError("csm_count must be positive")
    human_fires = sum(p["fires_per_30d"] for p in plays
                      if not p["automated"] and p["state"] == "live")
    return human_fires / WEEKS_PER_MONTH / csm_count


# ------------------------------------------------------------------------------- power


def n_per_arm(base: float, delta: float, alpha: float = 0.05, power: float = 0.80) -> int:
    """Accounts per arm for a two-proportion test (normal approximation)."""
    if not 0 < base < 1:
        raise ValueError("base must be strictly between 0 and 1")
    p2 = base + delta
    if not 0 < p2 < 1:
        raise ValueError("base + delta must be strictly between 0 and 1")
    if alpha not in Z_ALPHA_TWO_SIDED:
        raise ValueError(f"alpha must be one of {sorted(Z_ALPHA_TWO_SIDED)}")
    if power not in Z_POWER:
        raise ValueError(f"power must be one of {sorted(Z_POWER)}")
    za, zb = Z_ALPHA_TWO_SIDED[alpha], Z_POWER[power]
    pbar = (base + p2) / 2
    term_a = za * math.sqrt(2 * pbar * (1 - pbar))
    term_b = zb * math.sqrt(base * (1 - base) + p2 * (1 - p2))
    return math.ceil(((term_a + term_b) ** 2) / (delta ** 2))


def years_to_power(n: int, fires_per_30d: float, holdout_share: float) -> float:
    """Years of firing before the *holdout* arm reaches n. The holdout is the binding arm."""
    per_year = fires_per_30d * 12 * holdout_share
    return float("inf") if per_year <= 0 else n / per_year


# ------------------------------------------------------------------------------ output


def fmt_pct(x: float) -> str:
    return f"{x * 100:.1f}%"


def report(cfg: dict) -> tuple[str, int]:
    csm_count = int(cfg.get("csm_count", 1))
    eligible_default = int(cfg.get("eligible_accounts", 0))
    holdout_share = float(cfg.get("holdout_share", 0.10))
    base = float(cfg.get("renewal_base_rate", 0.80))
    delta = float(cfg.get("target_delta", 0.05))

    plays = [size_play(p, eligible_default) for p in cfg["plays"]]
    cap = capacity_budget(cfg)
    intake = modelled_intake(plays, csm_count)
    budget = cap["weekly_intake_budget_per_csm"]

    out: list[str] = []
    out.append(f"PLAY SIZING — {cfg.get('label', 'library')}")
    out.append(f"{len(plays)} plays · {csm_count} CSMs · eligible population {eligible_default}")
    out.append("")
    out.append("1. FIRE RATES")
    out.append(f"{'ID':<9}{'Play':<28}{'Elig':>6}{'Fires/mo':>10}{'Rate':>8}  Verdict")
    for p in sorted(plays, key=lambda x: -x["fire_rate"]):
        flag = "" if p["state"] == "live" else f" [{p['state']}]"
        out.append(f"{p['id']:<9}{p['name'][:27]:<28}{p['eligible_accounts']:>6}"
                   f"{p['fires_per_30d']:>10.1f}{fmt_pct(p['fire_rate']):>8}  {p['band']}{flag}")
    over = [p for p in plays if p["fire_rate"] > 0.05 and not p["automated"]]
    for p in over:
        out.append(f"   ! {p['id']} {p['advice']}")

    out.append("")
    out.append("2. CAPACITY GATE (R13)")
    out.append(f"   usable hours/week        = {cap['nominal_hours_per_week']:.0f} x 0.60"
               f" = {cap['usable_hours_per_week']:.1f}")
    out.append(f"   proactive hours/week     = {cap['usable_hours_per_week']:.1f} x "
               f"{float(cfg.get('proactive_share', 0.25)):.2f} = {cap['proactive_hours_per_week']:.2f}")
    out.append(f"   concurrent motions/CSM   = {cap['proactive_hours_per_week']:.2f} / "
               f"({cap['hours_per_motion']:.1f} / {cap['weeks_per_motion']:.0f})"
               f" = {cap['concurrent_motions_per_csm']:.2f}")
    out.append(f"   weekly intake budget/CSM = {cap['concurrent_motions_per_csm']:.2f} / "
               f"{cap['weeks_per_motion']:.0f} = {budget:.2f}")
    out.append(f"   modelled human intake/CSM= {intake:.2f}")
    if intake > budget:
        out.append(f"   >> OVER BUDGET by {intake - budget:.2f} per CSM per week. "
                   f"Tighten a qualifier, cheapen an action, or do not switch one on.")
    else:
        out.append(f"   >> Within budget. Headroom {budget - intake:.2f} per CSM per week.")

    out.append("")
    out.append("3. POWER TO CLAIM A RETENTION DELTA (two-proportion, alpha 0.05, power 0.80)")
    need = n_per_arm(base, delta)
    out.append(f"   base {fmt_pct(base)} -> {fmt_pct(base + delta)}  requires {need} accounts per arm")
    for p in sorted(plays, key=lambda x: -x["fires_per_30d"]):
        yrs = years_to_power(need, p["fires_per_30d"], holdout_share)
        yrs_even = years_to_power(need, p["fires_per_30d"], 0.50)
        verdict = (f"NOT POWERED — {yrs:.0f}y" if yrs > 10
                   else f"powered after {yrs:.1f}y")
        out.append(f"   {p['id']:<9}{p['fires_per_30d']:>7.1f} fires/mo -> {verdict}"
                   f" at a {fmt_pct(holdout_share)} holdout; {yrs_even:.0f}y at 50/50")
    out.append("   >> Where a play is not powered, measure the LEADING outcome and report")
    out.append("      retention as observed, not attributed (R22).")

    return "\n".join(out), (1 if intake > budget else 0)


def power_table() -> str:
    rows = ["POWER TABLE — accounts per arm, two-sided alpha 0.05",
            f"{'base':>6}{'delta':>8}{'power 0.80':>12}{'power 0.90':>12}"]
    for base in (0.70, 0.80, 0.90):
        for delta in (0.02, 0.05, 0.10, 0.15):
            if base + delta >= 1.0:
                continue
            rows.append(f"{base:>6.2f}{delta:>8.2f}"
                        f"{n_per_arm(base, delta, power=0.80):>12}"
                        f"{n_per_arm(base, delta, power=0.90):>12}")
    return "\n".join(rows)


def main() -> int:
    ap = argparse.ArgumentParser(description="Size playbook triggers, capacity and power.")
    ap.add_argument("config", nargs="?", help="JSON library config")
    ap.add_argument("--json", action="store_true", help="emit machine-readable JSON")
    ap.add_argument("--power", action="store_true", help="single power calculation")
    ap.add_argument("--power-table", action="store_true", help="print the power reference table")
    ap.add_argument("--base", type=float, default=0.80)
    ap.add_argument("--delta", type=float, default=0.05)
    ap.add_argument("--alpha", type=float, default=0.05)
    ap.add_argument("--power-level", type=float, default=0.80)
    args = ap.parse_args()

    if args.power_table:
        print(power_table())
        return 0
    if args.power:
        n = n_per_arm(args.base, args.delta, args.alpha, args.power_level)
        print(f"{n} accounts per arm  (base {args.base:.2f} -> {args.base + args.delta:.2f}, "
              f"alpha {args.alpha}, power {args.power_level})")
        return 0
    if not args.config:
        ap.print_help()
        return 2

    path = Path(args.config)
    if not path.exists():
        print(f"no such file: {path}", file=sys.stderr)
        return 2
    cfg = json.loads(path.read_text())
    if not cfg.get("plays"):
        print("config has no 'plays' array", file=sys.stderr)
        return 2

    if args.json:
        plays = [size_play(p, int(cfg.get("eligible_accounts", 0))) for p in cfg["plays"]]
        cap = capacity_budget(cfg)
        print(json.dumps({
            "plays": plays,
            "capacity": cap,
            "modelled_intake_per_csm_week": modelled_intake(plays, int(cfg.get("csm_count", 1))),
            "n_per_arm": n_per_arm(float(cfg.get("renewal_base_rate", 0.80)),
                                   float(cfg.get("target_delta", 0.05))),
        }, indent=2))
        return 0

    text, code = report(cfg)
    print(text)
    return code


if __name__ == "__main__":
    raise SystemExit(main())
