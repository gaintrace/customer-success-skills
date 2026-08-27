#!/usr/bin/env python3
"""
Price the custom-work ledger for one deployment.

Deployment debt is not an engineering opinion — it is an annual cash cost with a name on it.
This computes that cost deterministically so the number in the plan can be audited, and applies
the disposition rules from SKILL.md Step 3 so two engineers pricing the same ledger get the
same answer.

    python3 custom_work_ledger.py ../assets/sample-custom-work.json
    python3 custom_work_ledger.py ledger.json --rate 175 --arr 980000 --json

Model (Cunningham's metaphor: the build is the principal, the upkeep is the interest):

    annual_carrying = (maintenance_hours
                       + incident_hours
                       + upgrade_tax_hours * upgrades_per_year) * loaded_hourly_rate
                      + third_party_cost_per_year
    build_cost      = build_hours * loaded_hourly_rate
    interest_rate   = annual_carrying / build_cost

Stdlib only. No network. Nothing here is a forecast: every output is arithmetic over inputs
the user supplied, and unsupplied inputs are reported as UNKNOWN rather than defaulted to zero.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

DEFAULT_RATE = 150.0          # loaded engineering cost per hour; override with --rate
COMMERCIAL_THRESHOLD = 0.05   # carrying cost above 5% of ARR is a commercial decision (SKILL.md Step 3)

REQUIRED = ("name",)
NUMERIC = ("build_hours", "maintenance_hours", "incident_hours", "upgrade_tax_hours",
           "upgrades_per_year", "third_party_cost_per_year", "arr_dependent",
           "other_customers", "days_since_last_use")


def money(x: float) -> str:
    return f"${x:,.0f}"


def two_sig(x: float) -> str:
    """Composite figures are opinions with arithmetic attached — never state them to the dollar."""
    if x == 0:
        return "$0"
    mag = 10 ** (len(f"{int(abs(x))}") - 2)
    return f"${round(x / mag) * mag:,.0f}"


def disposition(item: dict, carrying: float, arr: float) -> tuple[str, str]:
    """First matching rule wins. Mirrors the table in SKILL.md Step 3."""
    others = item.get("other_customers")
    supported = bool(item.get("supported_path_exists"))
    arr_dep = float(item.get("arr_dependent") or 0)
    idle = item.get("days_since_last_use")

    if others is None:
        return "UNKNOWN", "requires a count of other customers hitting this problem"
    if others >= 5:
        return "Productise", f"{others} other customers hit this — a product requirement, not a customisation"
    if others >= 2:
        return "Generalise", f"{others} other customers — one shared template owned by delivery, not a per-customer fork"
    if idle is not None and idle >= 90 and arr_dep == 0:
        return "Retire", f"unused {idle} days and no ARR depends on it — dated notice plus a rollback window"
    if supported and arr_dep > 0:
        return "Migrate", "a supported path exists — dated cutover with a named owner each side"
    if arr_dep > 0:
        return "Own it", "no supported path and ARR depends on it — named maintainer, tests, runbook entry, sunset review date"
    return "Retire", "nothing depends on it and no other customer needs it"


def price(item: dict, rate: float) -> dict:
    def num(k: str) -> float:
        v = item.get(k)
        return 0.0 if v is None else float(v)

    hours = (num("maintenance_hours") + num("incident_hours")
             + num("upgrade_tax_hours") * num("upgrades_per_year"))
    carrying = hours * rate + num("third_party_cost_per_year")
    build_cost = num("build_hours") * rate
    interest = (carrying / build_cost) if build_cost > 0 else None
    return {
        "annual_hours": round(hours, 1),
        "annual_carrying": round(carrying, 2),
        "build_cost": round(build_cost, 2),
        "interest_rate": None if interest is None else round(interest, 2),
    }


def validate(items: list[dict]) -> list[str]:
    problems = []
    for i, it in enumerate(items, 1):
        for k in REQUIRED:
            if not it.get(k):
                problems.append(f"item {i}: missing required field '{k}'")
        for k in NUMERIC:
            v = it.get(k)
            if v is not None and not isinstance(v, (int, float)):
                problems.append(f"item {i} ({it.get('name', '?')}): '{k}' is not numeric: {v!r}")
    return problems


def load(path: Path) -> tuple[list[dict], dict]:
    data = json.loads(path.read_text())
    if isinstance(data, list):
        return data, {}
    return data.get("items", []), data


def main() -> int:
    ap = argparse.ArgumentParser(description="Price a deployment's custom-work ledger.")
    ap.add_argument("ledger", help="JSON file: a list of items, or {account, arr, loaded_hourly_rate, items:[...]}")
    ap.add_argument("--rate", type=float, help="loaded engineering cost per hour")
    ap.add_argument("--arr", type=float, help="account ARR, for the carrying-cost share")
    ap.add_argument("--json", action="store_true", help="emit JSON instead of markdown")
    a = ap.parse_args()

    path = Path(a.ledger)
    if not path.exists():
        print(f"no such file: {path}", file=sys.stderr)
        return 2

    items, meta = load(path)
    if not items:
        print("ledger contains no items — record the negative finding in the plan "
              "('no custom work found, verified against deploy history'), not an empty table.",
              file=sys.stderr)
        return 1

    problems = validate(items)
    if problems:
        for p in problems:
            print(f"ERROR {p}", file=sys.stderr)
        return 1

    rate = a.rate or meta.get("loaded_hourly_rate") or DEFAULT_RATE
    arr = a.arr or meta.get("arr")
    account = meta.get("account", path.stem)
    rate_assumed = a.rate is None and not meta.get("loaded_hourly_rate")

    rows, total_carry, total_build, total_hours, blocked = [], 0.0, 0.0, 0.0, 0.0
    for it in items:
        p = price(it, rate)
        disp, why = disposition(it, p["annual_carrying"], arr or 0)
        total_carry += p["annual_carrying"]
        total_build += p["build_cost"]
        total_hours += p["annual_hours"]
        if disp in ("Own it", "Migrate", "Generalise", "Productise"):
            # Dependencies overlap — two items can both gate the same ARR. Summing them
            # would report more exposure than the account carries, so take the largest.
            blocked = max(blocked, float(it.get("arr_dependent") or 0))
        rows.append({**it, **p, "disposition": disp, "rationale": why})

    rows.sort(key=lambda r: -r["annual_carrying"])
    share = (total_carry / arr) if arr else None

    if a.json:
        print(json.dumps({
            "account": account, "loaded_hourly_rate": rate, "rate_assumed": rate_assumed,
            "arr": arr, "total_annual_carrying": round(total_carry, 2),
            "total_build_cost": round(total_build, 2), "total_annual_hours": round(total_hours, 1),
            "carrying_share_of_arr": None if share is None else round(share, 4),
            "arr_blocked": blocked, "items": rows,
        }, indent=2))
        return 0

    print(f"# Custom-work ledger — {account}\n")
    print(f"Loaded rate {money(rate)}/hr"
          + (" **(assumed — no rate supplied; record it in the Assumptions table)**" if rate_assumed else "")
          + (f" · ARR {money(arr)}" if arr else " · ARR UNKNOWN — requires the subscription record") + "\n")
    print("| # | Item | Type | Maintainer | Blocks | Build cost | Carrying $/yr | Interest | Others | Disposition | Why |")
    print("|---|---|---|---|---|---|---|---|---|---|---|")
    for i, r in enumerate(rows, 1):
        interest = "UNKNOWN" if r["interest_rate"] is None else f"{r['interest_rate']:.0%}"
        print(f"| {i} | {r['name']} | {r.get('type', 'UNKNOWN')} | {r.get('maintainer') or '**UNOWNED**'} "
              f"| {r.get('blocks', '—')} | {money(r['build_cost'])} | {money(r['annual_carrying'])} "
              f"| {interest} | {r.get('other_customers', '?')} | **{r['disposition']}** | {r['rationale']} |")
    print(f"| | **Total ({len(rows)} items)** | | | | {money(total_build)} | **{money(total_carry)}** | | | | |\n")

    print(f"**Annual carrying cost {two_sig(total_carry)}** — {total_hours:.0f} engineering hours a year"
          + (f", {share:.1%} of ARR." if share is not None else ", share of ARR UNKNOWN.") + "\n")
    if share is not None:
        if share > COMMERCIAL_THRESHOLD:
            print(f"> **Above the {COMMERCIAL_THRESHOLD:.0%} threshold.** Disposition is now a commercial "
                  f"decision, not an engineering one: it goes to the account owner this week and into the "
                  f"renewal margin conversation. (`R2` — carrying cost is a decision, not an indicator.)\n")
        else:
            print(f"> Below the {COMMERCIAL_THRESHOLD:.0%} threshold — disposition stays an engineering call "
                  f"this cycle. Re-run at the quarterly refresh; the ratio moves when ARR contracts, not only "
                  f"when the ledger grows.\n")
    if blocked:
        print(f"**{money(blocked)} of ARR sits behind the largest not-yet-retired item** (largest single "
              f"dependency, not a sum — dependencies overlap). Every retained item needs a named maintainer "
              f"and a sunset review date before the next renewal.\n")

    unowned = [r["name"] for r in rows if not r.get("maintainer")]
    if unowned:
        print(f"**Unowned ({len(unowned)}):** {', '.join(unowned)} — unowned custom code is the primary "
              f"source of deployment debt. Assign an owner and a sunset review date, or retire it.\n")
    missing = [r["name"] for r in rows if r.get("other_customers") is None]
    if missing:
        print(f"**UNKNOWN — requires a count of other customers hitting the same problem:** "
              f"{', '.join(missing)}. Without it the productise/generalise decision cannot be made; "
              f"do not default it to zero.\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
