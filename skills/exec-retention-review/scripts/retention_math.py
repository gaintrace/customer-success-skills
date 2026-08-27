#!/usr/bin/env python3
"""
Deterministic board-pack arithmetic for the `exec-retention-review` skill.

Why a script: a board pack is the one CS artifact where a single arithmetic slip discards
every other number in the room. These computations are mechanical, auditable, and produce
the same answer every time — including the ones an LLM reliably gets subtly wrong
(cohort vs formula retention, and the shift-share decomposition of an NRR movement).

Computes
--------
1. ARR bridge tie-out            — does the waterfall reconcile to finance, to the dollar
2. Cohort GRR / NRR              — the correct cohort method AND the formula method, with the gap
3. Mix vs performance            — shift-share decomposition of the NRR movement, in basis points
4. Concentration                 — top 1/5/10/20 share, Herfindahl, retention ex-top-N,
                                   and the impact of losing the largest account
5. Forecast credibility          — accuracy, WAPE, signed bias, commit hit rate

Usage
-----
    python3 retention_math.py sample_input.json
    python3 retention_math.py sample_input.json --section mix
    python3 retention_math.py --emit-sample > sample_input.json

Input JSON shape: see --emit-sample. Any section may be omitted; it is skipped, not faked.
Missing values must be null, never 0 — 0 means measured-and-zero.

No network access. Standard library only.
"""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any

BPS = 10_000.0


# ----------------------------------------------------------------------------------------
# formatting helpers
# ----------------------------------------------------------------------------------------

def money(x: float) -> str:
    sign = "-" if x < 0 else ""
    return f"{sign}${abs(x):,.0f}"


def pct(x: float, dp: int = 1) -> str:
    return f"{x * 100:.{dp}f}%"


def bps(x: float) -> str:
    return f"{x * BPS:+,.0f} bps"


def rule(title: str) -> None:
    print(f"\n{title}\n" + "-" * len(title))


# ----------------------------------------------------------------------------------------
# 1. ARR bridge tie-out
# ----------------------------------------------------------------------------------------

def bridge(data: dict[str, Any]) -> None:
    rule("1. ARR BRIDGE TIE-OUT")
    rows = data["quarters"]
    finance_ending = data.get("finance_ending_arr")

    hdr = f"{'Quarter':<10}{'Beginning':>14}{'New':>13}{'Expansion':>13}{'React':>11}{'Contract':>13}{'Churn':>13}{'Ending':>14}{'Quick':>8}"
    print(hdr)
    print("-" * len(hdr))

    for r in rows:
        end = (r["beginning"] + r["new"] + r["expansion"] + r.get("reactivation", 0.0)
               - r["contraction"] - r["churn"])
        denom = r["churn"] + r["contraction"]
        qr = (r["new"] + r["expansion"]) / denom if denom else float("inf")
        print(f"{r['quarter']:<10}{money(r['beginning']):>14}{money(r['new']):>13}"
              f"{money(r['expansion']):>13}{money(r.get('reactivation', 0.0)):>11}"
              f"{money(-r['contraction']):>13}{money(-r['churn']):>13}{money(end):>14}"
              f"{qr:>8.2f}")
        r["_ending"] = end

    computed = rows[-1]["_ending"]
    print(f"\nComputed ending ARR : {money(computed)}")
    if finance_ending is None:
        print("Finance ending ARR  : UNKNOWN — requires finance ARR balance. "
              "This pack does not ship until the tie-out is $0.")
    else:
        var = computed - finance_ending
        print(f"Finance ending ARR  : {money(finance_ending)}")
        print(f"Variance            : {money(var)}  ->  "
              f"{'TIED' if abs(var) < 0.5 else 'NOT TIED — DO NOT SHIP THIS PACK'}")

    first, last = rows[0], rows[-1]
    net_new = last["_ending"] - first["beginning"]
    total_loss = sum(r["churn"] + r["contraction"] for r in rows)
    total_gross_new = sum(r["new"] + r["expansion"] for r in rows)
    print(f"\nNet new ARR over {len(rows)} quarters : {money(net_new)}")
    print(f"Leaky-bucket ratio (churn+contraction / new+expansion) : "
          f"{total_loss / total_gross_new:.2f}" if total_gross_new else "")


# ----------------------------------------------------------------------------------------
# 2. Cohort GRR / NRR, and the formula-method error
# ----------------------------------------------------------------------------------------

def cohort(data: dict[str, Any]) -> None:
    rule("2. COHORT GRR / NRR (and what the formula method would have said)")
    c = data["cohort"]
    beg = c["beginning_arr"]

    coh_churn = c["cohort_churn"]
    coh_contr = c["cohort_contraction"]
    coh_exp = c["cohort_expansion"]

    grr = (beg - coh_churn - coh_contr) / beg
    nrr = (beg - coh_churn - coh_contr + coh_exp) / beg

    print(f"Cohort beginning ARR (t0)     : {money(beg)}")
    print(f"  cohort churn                : {money(-coh_churn)}")
    print(f"  cohort contraction          : {money(-coh_contr)}")
    print(f"  cohort expansion            : {money(coh_exp)}")
    print(f"\nCOHORT GRR = ({money(beg)} - {money(coh_churn)} - {money(coh_contr)}) / {money(beg)} = {pct(grr, 1)}")
    print(f"COHORT NRR = (above + {money(coh_exp)}) / {money(beg)} = {pct(nrr, 1)}")
    if grr > 1.0:
        print("  !! GRR above 100% is a calculation bug — expansion has leaked into the numerator.")

    tot_churn = c.get("total_churn")
    tot_contr = c.get("total_contraction")
    tot_exp = c.get("total_expansion")
    react = c.get("reactivation", 0.0)
    if None not in (tot_churn, tot_contr, tot_exp):
        f_grr = (beg - tot_churn - tot_contr) / beg
        f_nrr = (beg + tot_exp - tot_contr - tot_churn) / beg
        f_nrr_react = (beg + tot_exp + react - tot_contr - tot_churn) / beg
        print("\nFormula method (period movements, including in-period new logos):")
        print(f"  GRR                         : {pct(f_grr, 1)}   error {bps(f_grr - grr)}")
        print(f"  NRR                         : {pct(f_nrr, 1)}   error {bps(f_nrr - nrr)}")
        print(f"  NRR + reactivation (worse)  : {pct(f_nrr_react, 1)}   error {bps(f_nrr_react - nrr)}")
        print("  Report the cohort values. Name the method on the slide.")

    logos = c.get("logos")
    if logos:
        lr = (logos["beginning"] - logos["cohort_churned"]) / logos["beginning"]
        avg_all = beg / logos["beginning"]
        avg_churned = coh_churn / logos["cohort_churned"] if logos["cohort_churned"] else 0.0
        idx = avg_churned / avg_all if avg_all else 0.0
        print(f"\nLogo retention               : {pct(lr, 1)}  "
              f"({logos['beginning'] - logos['cohort_churned']} of {logos['beginning']})")
        print(f"Dollar churn (1 - GRR)       : {pct(1 - grr, 1)}")
        print(f"Churned-account size index   : {idx:.2f}x  "
              f"(avg churned {money(avg_churned)} vs book avg {money(avg_all)})")
        if idx > 1.05:
            print("  Read: churn is adversely selected toward your LARGER customers.")
        elif idx < 0.95:
            print("  Read: churn is concentrated in your SMALLER customers.")
        else:
            print("  Read: churn is roughly size-neutral.")


# ----------------------------------------------------------------------------------------
# 3. Mix vs performance (shift-share)
# ----------------------------------------------------------------------------------------

def mix(data: dict[str, Any]) -> None:
    rule("3. NRR MOVEMENT: MIX vs PERFORMANCE (shift-share)")
    segs = data["mix"]["segments"]

    b0 = sum(s["beg_arr_prior"] for s in segs)
    b1 = sum(s["beg_arr_current"] for s in segs)

    nrr0 = sum(s["beg_arr_prior"] / b0 * s["nrr_prior"] for s in segs)
    nrr1 = sum(s["beg_arr_current"] / b1 * s["nrr_current"] for s in segs)

    hdr = f"{'Segment':<16}{'w0':>8}{'w1':>8}{'dw':>9}{'NRR0':>9}{'NRR1':>9}{'mix':>12}{'perf':>12}{'interact':>12}"
    print(hdr)
    print("-" * len(hdr))

    t_mix = t_perf = t_int = 0.0
    for s in segs:
        w0 = s["beg_arr_prior"] / b0
        w1 = s["beg_arr_current"] / b1
        dw = w1 - w0
        dn = s["nrr_current"] - s["nrr_prior"]
        m = dw * s["nrr_prior"]
        p = w0 * dn
        i = dw * dn
        t_mix += m
        t_perf += p
        t_int += i
        print(f"{s['name']:<16}{w0:>8.3f}{w1:>8.3f}{dw:>+9.3f}"
              f"{pct(s['nrr_prior'], 1):>9}{pct(s['nrr_current'], 1):>9}"
              f"{bps(m):>12}{bps(p):>12}{bps(i):>12}")

    print("-" * len(hdr))
    print(f"{'TOTAL':<16}{'':>8}{'':>8}{'':>9}{pct(nrr0, 1):>9}{pct(nrr1, 1):>9}"
          f"{bps(t_mix):>12}{bps(t_perf):>12}{bps(t_int):>12}")

    delta = nrr1 - nrr0
    recon = t_mix + t_perf + t_int
    print(f"\nBlended NRR moved {pct(nrr0, 1)} -> {pct(nrr1, 1)}  =  {bps(delta)}")
    print(f"  MIX         {bps(t_mix)}   the opening base changed shape (a go-to-market outcome)")
    print(f"  PERFORMANCE {bps(t_perf)}   customers behaved differently (yours)")
    print(f"  INTERACTION {bps(t_int)}   report it; never fold it into mix")
    print(f"  reconciles to {bps(recon)} (residual {bps(delta - recon)})")

    driver = max((("mix", t_mix), ("performance", t_perf), ("interaction", t_int)),
                 key=lambda kv: abs(kv[1]))
    share = abs(driver[1]) / abs(delta) if delta else 0.0
    print(f"\nOne-sentence answer: the move is predominantly {driver[0].upper()} "
          f"({pct(share, 0)} of the movement).")


# ----------------------------------------------------------------------------------------
# 4. Concentration
# ----------------------------------------------------------------------------------------

def concentration(data: dict[str, Any]) -> None:
    rule("4. CONCENTRATION AND DEPENDENCY")
    accts = sorted(data["accounts"], key=lambda a: a["arr"], reverse=True)
    tail_arr = data.get("other_accounts_arr", 0.0)
    tail_n = data.get("other_accounts_count", 0)
    total = sum(a["arr"] for a in accts) + tail_arr

    print(f"Total ARR across {len(accts) + tail_n} accounts : {money(total)}")
    if tail_arr:
        print(f"  (named accounts {len(accts)}; tail of {tail_n} accounts holding {money(tail_arr)})")
    for n in (1, 5, 10, 20):
        if n <= len(accts):
            share = sum(a["arr"] for a in accts[:n]) / total
            print(f"  Top {n:<3} share of ARR          : {pct(share, 1)}  ({money(sum(a['arr'] for a in accts[:n]))})")

    hhi = sum((a["arr"] / total) ** 2 for a in accts)
    if tail_arr and tail_n:
        # tail modelled at its mean size — states the assumption rather than ignoring the tail
        hhi += tail_n * ((tail_arr / tail_n) / total) ** 2
    print(f"  Herfindahl index             : {hhi:.4f}"
          + ("  (tail modelled at its mean account size)" if tail_arr else ""))

    over10 = [a for a in accts if a["arr"] / total >= 0.10]
    if over10:
        print(f"\n  !! {len(over10)} account(s) at or above 10% of revenue — "
              f"a US GAAP major-customer disclosure item (ASC 280-10-50-42):")
        for a in over10:
            print(f"       {a['name']}: {money(a['arr'])} ({pct(a['arr'] / total, 1)})")
    else:
        print("\n  No single account at or above 10% of revenue (ASC 280-10-50-42 threshold): checked, clear.")

    grr = data.get("current_grr")
    nrr = data.get("current_nrr")
    if grr is not None:
        top = accts[0]
        beg = data.get("beginning_arr", total)
        grr_after = grr - top["arr"] / beg
        line = (f"\n  If {top['name']} ({money(top['arr'])}) churns at renewal: "
                f"TTM GRR {pct(grr, 1)} -> {pct(grr_after, 1)} ({bps(grr_after - grr)})")
        if nrr is not None:
            line += f"; NRR {pct(nrr, 1)} -> {pct(nrr - top['arr'] / beg, 1)}"
        print(line)

    ex3 = accts[3:]
    if ex3:
        ex3_total = sum(a["arr"] for a in ex3) + tail_arr
        print(f"  ARR excluding the top 3      : {money(ex3_total)} "
              f"({pct(ex3_total / total, 1)} of the base) — have retention ex-top-3 ready; "
              "this is asked live.")

    single_threaded = [a for a in accts[:10] if a.get("live_contacts") is not None and a["live_contacts"] <= 1]
    if single_threaded:
        print(f"\n  Dependency risk — top-10 accounts carried by one live contact: "
              f"{', '.join(a['name'] for a in single_threaded)}")
    no_sponsor = [a for a in accts[:10] if a.get("exec_sponsor") in (None, "", "none")]
    if no_sponsor:
        print(f"  Top-10 accounts with no named executive sponsor: "
              f"{', '.join(a['name'] for a in no_sponsor)}")


# ----------------------------------------------------------------------------------------
# 5. Forecast credibility
# ----------------------------------------------------------------------------------------

def forecast(data: dict[str, Any]) -> None:
    rule("5. FORECAST CREDIBILITY (frozen snapshots only)")
    for v in data["forecast"]["vintages"]:
        rows = v["accounts"]
        called = sum(r["called"] for r in rows)
        closed = sum(r["closed"] for r in rows)
        if closed == 0:
            print(f"\n{v['label']:<28} called {money(called)}  — period open, not gradable")
            continue
        acc = 1 - abs(called - closed) / called
        wape = sum(abs(r["called"] - r["closed"]) for r in rows) / closed
        bias = (called - closed) / closed

        print(f"\n{v['label']}")
        print(f"  Called / Closed            : {money(called)} / {money(closed)}")
        print(f"  Forecast accuracy          : {pct(acc, 1)}")
        print(f"  WAPE (account-level)       : {pct(wape, 1)}")
        print(f"  Bias (signed)              : {pct(bias, 1)} "
              f"({'optimistic' if bias > 0 else 'conservative'})")
        if abs(bias) > 0.02:
            print("    Sustained bias above 2% is a coaching problem, not a model problem [P].")

        commit = [r for r in rows if r.get("category") == "commit"]
        if commit:
            c_called = sum(r["called"] for r in commit)
            c_closed = sum(r["closed"] for r in commit)
            print(f"  Commit hit rate            : {pct(c_closed / c_called, 1)} "
                  f"({money(c_closed)} of {money(c_called)})")
            print(f"  Commit leakage             : {pct(1 - c_closed / c_called, 1)} "
                  f"(practitioner tolerance <=5% [P])")

    f = data["forecast"]
    if f.get("arr_lost_total") and f.get("arr_flagged_60d") is not None:
        dr = f["arr_flagged_60d"] / f["arr_lost_total"]
        print(f"\nRisk detection rate (TTM)    : {pct(dr, 1)} — "
              f"{money(f['arr_flagged_60d'])} of {money(f['arr_lost_total'])} lost ARR "
              "was flagged 60+ days out")
        print(f"Surprise loss                : {money(f['arr_lost_total'] - f['arr_flagged_60d'])} "
              f"({pct(1 - dr, 1)})")
        if dr < 0.60:
            print("  Below ~60%, most churn is a surprise and the renewal forecast is fiction [P].")
    if f.get("at_risk_reaching_renewal") and f.get("at_risk_retained") is not None:
        sr = f["at_risk_retained"] / f["at_risk_reaching_renewal"]
        print(f"Save rate (TTM)              : {pct(sr, 1)} — publish only alongside the "
              "detection rate and written entry/exit criteria")


# ----------------------------------------------------------------------------------------

SAMPLE: dict[str, Any] = {
    "finance_ending_arr": 117_500_000,
    "quarters": [
        {"quarter": "Q1 FY26", "beginning": 100_000_000, "new": 3_900_000, "expansion": 2_600_000,
         "reactivation": 100_000, "contraction": 1_000_000, "churn": 2_900_000},
        {"quarter": "Q2 FY26", "beginning": 102_700_000, "new": 4_300_000, "expansion": 2_900_000,
         "reactivation": 200_000, "contraction": 900_000, "churn": 2_100_000},
        {"quarter": "Q3 FY26", "beginning": 107_100_000, "new": 4_600_000, "expansion": 3_100_000,
         "reactivation": 200_000, "contraction": 1_100_000, "churn": 2_400_000},
        {"quarter": "Q4 FY26", "beginning": 111_500_000, "new": 5_600_000, "expansion": 3_700_000,
         "reactivation": 200_000, "contraction": 1_100_000, "churn": 2_400_000},
    ],
    "cohort": {
        "beginning_arr": 100_000_000,
        "cohort_churn": 9_200_000,
        "cohort_contraction": 3_900_000,
        "cohort_expansion": 10_900_000,
        "total_churn": 9_800_000,
        "total_contraction": 4_100_000,
        "total_expansion": 12_300_000,
        "reactivation": 700_000,
        "logos": {"beginning": 1240, "cohort_churned": 138},
    },
    "mix": {
        "segments": [
            {"name": "Enterprise", "beg_arr_prior": 55_000_000, "beg_arr_current": 58_000_000,
             "nrr_prior": 1.055, "nrr_current": 1.042},
            {"name": "Mid-Market", "beg_arr_prior": 32_000_000, "beg_arr_current": 36_000_000,
             "nrr_prior": 0.962, "nrr_current": 0.938},
            {"name": "SMB", "beg_arr_prior": 13_000_000, "beg_arr_current": 19_000_000,
             "nrr_prior": 0.845, "nrr_current": 0.808},
        ]
    },
    "beginning_arr": 100_000_000,
    "current_grr": 0.869,
    "current_nrr": 0.978,
    "accounts": [
        {"name": "Northwind", "arr": 6_200_000, "live_contacts": 1, "exec_sponsor": None},
        {"name": "Contoso", "arr": 4_800_000, "live_contacts": 4, "exec_sponsor": "CRO"},
        {"name": "Fabrikam", "arr": 3_900_000, "live_contacts": 3, "exec_sponsor": "CCO"},
        {"name": "Tailspin", "arr": 3_100_000, "live_contacts": 2, "exec_sponsor": None},
        {"name": "Adventure Works", "arr": 2_700_000, "live_contacts": 5, "exec_sponsor": "CEO"},
        {"name": "Litware", "arr": 2_200_000, "live_contacts": 3, "exec_sponsor": "CCO"},
        {"name": "Proseware", "arr": 1_900_000, "live_contacts": 2, "exec_sponsor": "CRO"},
        {"name": "Wingtip", "arr": 1_600_000, "live_contacts": 1, "exec_sponsor": "CCO"},
        {"name": "Woodgrove", "arr": 1_400_000, "live_contacts": 4, "exec_sponsor": "CTO"},
        {"name": "Lucerne", "arr": 1_200_000, "live_contacts": 3, "exec_sponsor": "CCO"},
    ],
    "other_accounts_arr": 88_500_000,
    "other_accounts_count": 1360,
    "forecast": {
        "arr_lost_total": 13_100_000,
        "arr_flagged_60d": 7_400_000,
        "at_risk_reaching_renewal": 22_000_000,
        "at_risk_retained": 14_600_000,
        "vintages": [
            {"label": "Q3 FY26 · T-90 snapshot", "accounts": [
                {"called": 8_100_000, "closed": 7_400_000, "category": "commit"},
                {"called": 6_200_000, "closed": 6_400_000, "category": "commit"},
                {"called": 5_500_000, "closed": 5_100_000, "category": "best_case"},
            ]},
            {"label": "Q3 FY26 · T-30 snapshot", "accounts": [
                {"called": 7_900_000, "closed": 7_400_000, "category": "commit"},
                {"called": 6_300_000, "closed": 6_400_000, "category": "commit"},
                {"called": 5_600_000, "closed": 5_100_000, "category": "best_case"},
            ]},
        ],
    },
}

SECTIONS = {
    "bridge": ("quarters", bridge),
    "cohort": ("cohort", cohort),
    "mix": ("mix", mix),
    "concentration": ("accounts", concentration),
    "forecast": ("forecast", forecast),
}


def main() -> int:
    ap = argparse.ArgumentParser(description="Board-pack retention arithmetic.")
    ap.add_argument("input", nargs="?", help="Path to the input JSON file")
    ap.add_argument("--section", choices=sorted(SECTIONS), help="Run one section only")
    ap.add_argument("--emit-sample", action="store_true", help="Print a sample input JSON and exit")
    args = ap.parse_args()

    if args.emit_sample:
        print(json.dumps(SAMPLE, indent=2))
        return 0
    if not args.input:
        ap.error("provide an input JSON path, or use --emit-sample")

    with open(args.input, encoding="utf-8") as fh:
        data = json.load(fh)

    wanted = [args.section] if args.section else list(SECTIONS)
    ran = 0
    for name in wanted:
        key, fn = SECTIONS[name]
        if key in data and data[key]:
            fn(data)
            ran += 1
        else:
            print(f"\n[skipped: {name}] UNKNOWN — requires '{key}' in the input. "
                  "Section omitted rather than estimated.")
    if ran == 0:
        print("\nNo sections could be computed. Nothing is estimated.", file=sys.stderr)
        return 1
    print("\n" + "=" * 78)
    print("Every figure above is arithmetic on supplied inputs. Nothing is benchmarked,")
    print("smoothed or inferred. Gaps print as UNKNOWN — requires <field>.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
