#!/usr/bin/env python3
"""
Price a custom-build decision: multi-year carrying cost, break-even generality
threshold, the gate sequence, and the recommended outcome.

The build decision is almost always made on build cost alone. This script exists to
make that impossible: it prices the three interest streams (engineering, upgrade,
renewal exposure), grows them by an annual drift, totals them over the horizon, and
computes the account count at which generalising costs less than repeating the
bespoke build. It then runs the ordered gate sequence and returns one of four
outcomes — GENERALISE, BUILD_BESPOKE, WORK_AROUND, DECLINE.

Nothing here is a forecast. Renewal exposure is ARR x a band midpoint, stated as
exposure, never as a churn probability (R22). Composites are rounded to two
significant figures on display (R22 / SKILL-STANDARD 4F).

    python3 carrying_cost.py ../assets/sample-request.json
    python3 carrying_cost.py request.json --json
    python3 carrying_cost.py request.json --horizon 5

Stdlib only. No network.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from datetime import date, datetime

USABLE_CAPACITY = 0.6          # R13 - usable hours per nominal hour
DEFAULT_DRIFT = 0.15           # library convention [P]
DEFAULT_HORIZON = 3            # years
DEFAULT_EVIDENCE_WINDOW = 60   # days
TIER_WEIGHTS = {"G0": 0.0, "G1": 0.25, "G2": 0.5, "G3": 1.0, "G4": 1.5, "G5": 2.0}
COUNTABLE_TIERS = ("G3", "G4", "G5")


# ---------------------------------------------------------------- helpers

def sig2(x: float) -> float:
    """Round to two significant figures. A composite stated to the dollar implies a
    measurement nobody took."""
    if x == 0:
        return 0.0
    mag = math.floor(math.log10(abs(x)))
    return round(x, -(mag - 1))


def money(x: float) -> str:
    x = sig2(x)
    if abs(x) >= 1_000_000:
        return f"${x/1_000_000:.2f}M".replace(".00M", "M")
    if abs(x) >= 1_000:
        return f"${x/1_000:.0f}k"
    return f"${x:,.0f}"


def parse_date(s):
    if not s:
        return None
    return datetime.strptime(s, "%Y-%m-%d").date()


def get(d: dict, key: str, default=0.0) -> float:
    v = d.get(key)
    return default if v in (None, "") else float(v)


# ---------------------------------------------------------------- model

def price_variant(v: dict, cfg: dict) -> dict:
    """Principal and the three annual interest streams for one build variant."""
    rate = cfg["loaded_rate"]
    principal = get(v, "build_hours") / USABLE_CAPACITY * rate

    engineering = (get(v, "maintenance_h") + get(v, "incident_h")
                   + get(v, "support_h") + get(v, "eval_regression_h")) * rate \
        + get(v, "third_party_cost_per_year")
    upgrade = get(v, "upgrade_tax_h") * cfg["upgrades_per_year"] * rate \
        + get(v, "withheld_feature_cost")
    renewal = cfg["arr_at_stake"] * get(v, "band_uplift", cfg["band_uplift"])

    year1 = engineering + upgrade + renewal
    drift, n = cfg["drift"], cfg["horizon_years"]
    years = [year1 * (1 + drift) ** (i) for i in range(n)]
    carry_total = sum(years)

    return {
        "principal": principal,
        "engineering_interest": engineering,
        "upgrade_interest": upgrade,
        "renewal_interest": renewal,
        "annual_carrying_year1": year1,
        "carrying_by_year": years,
        "carrying_total": carry_total,
        "tco": principal + carry_total,
        "interest_rate": (year1 / principal) if principal else None,
        "share_of_arr": (year1 / cfg["account_arr"]) if cfg["account_arr"] else None,
    }


def break_even_accounts(bespoke: dict, general: dict, cfg: dict):
    """K* — the account count at which the general version costs less than repeating
    the bespoke build. Returns (K*, note)."""
    if not general:
        return None, "no general variant supplied — Gate 3 cannot be evaluated"
    deploy_cost = get(cfg.get("general", {}), "deploy_hours_per_account") / USABLE_CAPACITY \
        * cfg["loaded_rate"]
    bespoke_unit = bespoke["principal"] + bespoke["carrying_total"]
    general_fixed = general["principal"] + general["carrying_total"]
    denom = bespoke_unit - deploy_cost
    if denom <= 0:
        return None, ("deploying the general version costs at least as much as building it "
                      "bespoke — generalising never pays back; decide between bespoke and decline")
    k = math.ceil((general_fixed - bespoke_unit) / denom) + 1
    return max(k, 1), None


def score_generality(rows: list) -> dict:
    total = 0.0
    countable = 0
    unnamed = 0
    for r in rows or []:
        tier = str(r.get("tier", "G0")).upper()
        if tier not in TIER_WEIGHTS:
            raise SystemExit(f"unknown generality tier {tier!r} — use G0..G5")
        total += TIER_WEIGHTS[tier]
        if tier in COUNTABLE_TIERS:
            countable += 1
        if not r.get("account"):
            unnamed += 1
    return {"n_evidenced": round(total, 2), "accounts_at_g3_plus": countable,
            "accounts": len(rows or []), "unnamed": unnamed}


def run_gates(cfg: dict, gen: dict, kstar, bespoke: dict) -> tuple:
    """Ordered. First match returns the outcome; later gates do not run."""
    g = cfg.get("gates", {})
    rows, decided = [], None

    def add(n, name, result, evidence):
        rows.append({"gate": n, "name": name, "result": result, "evidence": evidence})

    # Gate 0 - the fork test
    if g.get("requires_fork"):
        add(0, "Fork test", "MATCH -> DECLINE",
            "requires a fork, an internal patch, or a build outside the supported release stream")
        decided = ("DECLINE", 0, "Fork test")
    else:
        add(0, "Fork test", "clear", "builds on documented extension points")

    # Gate 1 - the roadmap test
    if decided is None:
        owner = g.get("roadmap_owner")
        inc = parse_date(g.get("roadmap_increment_date"))
        dw = cfg.get("decision_window")
        if owner and inc and dw and inc <= dw:
            add(1, "Roadmap test", "MATCH -> WORK_AROUND",
                f"product ships {inc} (owner {owner}), inside the decision window {dw}")
            decided = ("WORK_AROUND", 1, "Roadmap test")
        else:
            why = ("no named product owner" if not owner else
                   "no committed increment date" if not inc else
                   "increment lands after the decision window" if dw and inc > dw else
                   "decision window UNKNOWN")
            add(1, "Roadmap test", "clear", why)

    # Gate 2 - the workaround test
    if decided is None:
        fid = get(g, "workaround_fidelity", 0.0)
        eff = get(g, "workaround_effort_ratio", 1.0)
        if fid >= 0.8 and eff <= 0.2:
            add(2, "Workaround test", "MATCH -> WORK_AROUND",
                f"supported path reaches {fid:.0%} of the job at {eff:.0%} of the build effort")
            decided = ("WORK_AROUND", 2, "Workaround test")
        else:
            add(2, "Workaround test", "clear",
                f"supported path reaches {fid:.0%} at {eff:.0%} of effort — below the 80%/20% bar")

    # Gate 3 - the generality test
    if decided is None:
        if kstar is None:
            add(3, "Generality test", "cannot evaluate",
                "no general variant supplied, or generalising never pays back")
        elif gen["n_evidenced"] >= kstar and gen["accounts_at_g3_plus"] >= 2:
            add(3, "Generality test", "MATCH -> GENERALISE",
                f"N_evidenced {gen['n_evidenced']} >= K* {kstar}; "
                f"{gen['accounts_at_g3_plus']} accounts at G3+")
            decided = ("GENERALISE", 3, "Generality test")
        else:
            add(3, "Generality test", "clear",
                f"N_evidenced {gen['n_evidenced']} vs K* {kstar}; "
                f"{gen['accounts_at_g3_plus']} accounts at G3+ (need 2)")

    # Gate 4 - the payback test
    if decided is None:
        pays = cfg["arr_at_stake"] * cfg["savability"] > bespoke["tco"]
        owned = bool(g.get("named_maintainer"))
        sunset = bool(g.get("sunset_review_date"))
        revers = bool(g.get("rollback_within_sprint"))
        missing = [n for n, ok in (("payback", pays), ("named maintainer", owned),
                                   ("sunset review date", sunset),
                                   ("rollback <=1 sprint", revers)) if not ok]
        if not missing:
            add(4, "Payback test", "MATCH -> BUILD_BESPOKE",
                f"ARR at stake x savability {money(cfg['arr_at_stake'] * cfg['savability'])} "
                f"> TCO {money(bespoke['tco'])}; maintainer {g['named_maintainer']}; "
                f"sunset {g['sunset_review_date']}")
            decided = ("BUILD_BESPOKE", 4, "Payback test")
        else:
            add(4, "Payback test", "clear", "fails on: " + ", ".join(missing))

    if decided is None:
        add(5, "Nothing matched", "-> DECLINE",
            "no gate returned an outcome; decline with the nearest alternative priced")
        decided = ("DECLINE", 5, "Nothing matched")

    for n, name in ((0, "Fork test"), (1, "Roadmap test"), (2, "Workaround test"),
                    (3, "Generality test"), (4, "Payback test"), (5, "Nothing matched")):
        if not any(r["gate"] == n for r in rows):
            rows.append({"gate": n, "name": name, "result": "not reached",
                         "evidence": f"gate {decided[1]} returned the outcome"})
    rows.sort(key=lambda r: r["gate"])
    return decided, rows


def analyse(cfg: dict) -> dict:
    cfg.setdefault("drift", DEFAULT_DRIFT)
    cfg.setdefault("horizon_years", DEFAULT_HORIZON)
    cfg.setdefault("upgrades_per_year", 2)
    cfg.setdefault("band_uplift", 0.05)
    cfg.setdefault("savability", 1.0)
    cfg.setdefault("term_years", cfg["horizon_years"])
    cfg["loaded_rate"] = get(cfg, "loaded_rate", 150.0)
    cfg["account_arr"] = get(cfg, "account_arr")
    cfg["arr_at_stake"] = get(cfg, "arr_at_stake")

    # Decision window = opt-out deadline - evidence window (R1). Never the renewal date.
    ew = int(get(cfg, "evidence_window_days", DEFAULT_EVIDENCE_WINDOW))
    rd, npd = parse_date(cfg.get("renewal_date")), cfg.get("notice_period_days")
    opt_out = decision_window = None
    if rd and npd not in (None, ""):
        opt_out = date.fromordinal(rd.toordinal() - int(npd))
        decision_window = date.fromordinal(opt_out.toordinal() - ew)
    cfg["opt_out_deadline"] = opt_out
    cfg["decision_window"] = decision_window

    bespoke = price_variant(cfg.get("bespoke", {}), cfg)
    general = price_variant(cfg["general"], cfg) if cfg.get("general") else None
    kstar, kstar_note = break_even_accounts(bespoke, general, cfg)
    gen = score_generality(cfg.get("generality_evidence"))
    (outcome, gate_n, gate_name), gate_rows = run_gates(cfg, gen, kstar, bespoke)

    trade = None
    if cfg.get("revenue_contingent"):
        arr = cfg["arr_at_stake"] or cfg["account_arr"]
        ty = max(int(cfg["term_years"]), 1)
        trade = {"annual_trade_price": bespoke["tco"] / ty,
                 "effective_discount_pct": (bespoke["tco"] / (arr * ty) * 100) if arr else None}

    return {"config": cfg, "bespoke": bespoke, "general": general, "kstar": kstar,
            "kstar_note": kstar_note, "generality": gen, "outcome": outcome,
            "decided_at": f"Gate {gate_n} — {gate_name}", "gates": gate_rows, "trade": trade}


# ---------------------------------------------------------------- report

def report(r: dict) -> str:
    c, b, o = r["config"], r["bespoke"], r["outcome"]
    L = []
    L.append(f"CUSTOM VS PRODUCT — {c.get('request','(unnamed request)')} · "
             f"{c.get('account','(unnamed account)')}")
    L.append(f"data as-of {c.get('as_of','UNKNOWN — requires an as-of date')} · "
             f"loaded rate ${c['loaded_rate']:.0f}/h · horizon {c['horizon_years']}y · "
             f"drift {c['drift']:.0%}")
    L.append("")
    L.append(f"OUTCOME: {o}   (decided at {r['decided_at']})")
    L.append("")
    L.append("Carrying cost — bespoke")
    L.append(f"  principal (build {get(c.get('bespoke',{}),'build_hours'):.0f}h "
             f"÷ 0.6 usable)          {money(b['principal'])}")
    L.append(f"  engineering interest / yr                    {money(b['engineering_interest'])}")
    L.append(f"  upgrade interest / yr                        {money(b['upgrade_interest'])}")
    L.append(f"  renewal interest / yr (exposure, not a probability)  "
             f"{money(b['renewal_interest'])}")
    for i, v in enumerate(b["carrying_by_year"], 1):
        L.append(f"  year {i} carrying                              {money(v)}")
    L.append(f"  TCO over {c['horizon_years']}y                                 {money(b['tco'])}")
    if b["interest_rate"] is not None:
        L.append(f"  interest rate                                {b['interest_rate']*100:.0f}%/yr"
                 + ("   <-- costs more each year than it cost to build"
                    if b["interest_rate"] > 1 else ""))
    if b["share_of_arr"] is not None:
        L.append(f"  share of account ARR                         {b['share_of_arr']*100:.1f}%")
    if r["general"]:
        g = r["general"]
        L.append("")
        L.append(f"Carrying cost — generalised: principal {money(g['principal'])} · "
                 f"{c['horizon_years']}y TCO {money(g['tco'])}")
    L.append("")
    gen = r["generality"]
    L.append(f"Generality: N_evidenced {gen['n_evidenced']} across {gen['accounts']} accounts "
             f"({gen['accounts_at_g3_plus']} at G3+)")
    L.append(f"Break-even K*: {r['kstar'] if r['kstar'] else 'n/a — ' + (r['kstar_note'] or '')}")
    if gen["unnamed"]:
        L.append(f"  WARNING: {gen['unnamed']} evidence rows have no named account — "
                 f"an unnamed account is not evidence")
    L.append("")
    if c["decision_window"]:
        L.append(f"Decision window: opt-out {c['opt_out_deadline']} − evidence window "
                 f"{int(get(c,'evidence_window_days',DEFAULT_EVIDENCE_WINDOW))}d "
                 f"= {c['decision_window']}")
    else:
        L.append("Decision window: UNKNOWN — requires renewal_date and notice_period_days")
    L.append("")
    L.append("Gate sequence")
    for row in r["gates"]:
        L.append(f"  {row['gate']}  {row['name']:<18} {row['result']:<24} {row['evidence']}")
    if r["trade"]:
        t = r["trade"]
        L.append("")
        L.append(f"Revenue trade: {money(t['annual_trade_price'])}/yr; effective discount "
                 f"{t['effective_discount_pct']:.1f}% of contracted ARR over the term")
        L.append("  An absorbed build is a discount that never appears in the discount report.")
    L.append("")
    L.append("Bands and exposure only — no churn probability is stated (R22). "
             "Composites rounded to two significant figures.")
    return "\n".join(L)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("input", help="JSON file describing the request")
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    ap.add_argument("--horizon", type=int, help="override horizon_years")
    ap.add_argument("--drift", type=float, help="override annual drift, e.g. 0.20")
    args = ap.parse_args()

    try:
        cfg = json.loads(open(args.input).read())
    except FileNotFoundError:
        print(f"no such file: {args.input}", file=sys.stderr)
        return 2
    except json.JSONDecodeError as e:
        print(f"{args.input} is not valid JSON: {e}", file=sys.stderr)
        return 2

    if args.horizon:
        cfg["horizon_years"] = args.horizon
    if args.drift is not None:
        cfg["drift"] = args.drift

    r = analyse(cfg)
    if args.json:
        def enc(x):
            return x.isoformat() if isinstance(x, date) else x
        print(json.dumps(r, indent=2, default=enc))
    else:
        print(report(r))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
