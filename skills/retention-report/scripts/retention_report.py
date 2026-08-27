#!/usr/bin/env python3
"""
Deterministic arithmetic for the `retention-report` skill.

Why a script: the monthly retention report is published on a calendar, read by finance, and
quoted for a year afterwards. Five of its computations are mechanical, auditable, and the
ones a language model reliably gets subtly wrong:

  1. ARR bridge          — the waterfall, its tie-out to finance, and the derived ratios
  2. Retention           — cohort GRR/NRR/logo retention AND the formula approximation,
                           with the gap between them stated in basis points
  3. Segment cuts        — per-segment retention plus the dollar-vs-logo adverse-selection index
  4. Cohort triangle     — dollar retention by acquisition cohort, immature cells left blank
  5. Migration matrix    — from/to health-band movement, and the six rates derived from it,
                           including the false-green rate that no other artifact exposes
  6. Forecast accuracy   — accuracy and signed bias by vintage, because bias is the real defect

Usage
-----
    python3 retention_report.py input.json
    python3 retention_report.py input.json --section migration
    python3 retention_report.py --emit-sample > input.json

Conventions
-----------
* Money in whole reporting-currency units unless the input says otherwise. The sample uses
  thousands and labels it; the script does not care, it only formats.
* Missing values must be `null`, never 0. `0` means measured-and-zero; `null` means
  not-measured and the affected line prints UNKNOWN rather than a fabricated number.
* Contraction and churn are supplied as POSITIVE magnitudes and subtracted here.
* Any section absent from the input is skipped, not faked.
* No network. Standard library only.
"""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any

BPS = 10_000.0
BANDS = ["Secure", "Watch", "At Risk", "High Risk", "Critical"]
CHURNED = "Churned"
SMALL_N_ACCOUNTS = 20          # suppress/asterisk a segment cell below this
SMALL_N_ARR_SHARE = 0.02       # ...or below this share of the total base


# ---------------------------------------------------------------------------------------
# formatting
# ---------------------------------------------------------------------------------------

def money(x: float | None) -> str:
    if x is None:
        return "UNKNOWN"
    sign = "-" if x < 0 else ""
    return f"{sign}${abs(x):,.0f}"


def pct(x: float | None, dp: int = 2) -> str:
    return "UNKNOWN" if x is None else f"{x * 100:.{dp}f}%"


def bps(x: float | None) -> str:
    return "UNKNOWN" if x is None else f"{x * BPS:+,.0f} bps"


def num(x: float | None, dp: int = 0) -> str:
    return "UNKNOWN" if x is None else f"{x:,.{dp}f}"


def rule(title: str) -> None:
    print(f"\n{title}\n" + "=" * len(title))


def sub(title: str) -> None:
    print(f"\n{title}\n" + "-" * len(title))


def table(headers: list[str], rows: list[list[str]], aligns: str | None = None) -> None:
    """Emit a markdown table so output can be pasted straight into the report."""
    widths = [len(h) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            widths[i] = max(widths[i], len(cell))
    aligns = aligns or ("l" + "r" * (len(headers) - 1))

    def fmt(cells: list[str]) -> str:
        out = []
        for i, c in enumerate(cells):
            out.append(c.ljust(widths[i]) if aligns[i] == "l" else c.rjust(widths[i]))
        return "| " + " | ".join(out) + " |"

    sep = "|" + "|".join(
        (":" + "-" * (w + 1)) if aligns[i] == "l" else ("-" * (w + 1) + ":")
        for i, w in enumerate(widths)
    ) + "|"
    print(fmt(headers))
    print(sep)
    for row in rows:
        print(fmt(row))


def safe_div(a: float | None, b: float | None) -> float | None:
    if a is None or b in (None, 0):
        return None
    return a / b


# ---------------------------------------------------------------------------------------
# 1. ARR bridge
# ---------------------------------------------------------------------------------------

def bridge_line(b: dict[str, Any]) -> dict[str, Any]:
    beg = b.get("beginning_arr")
    new = b.get("new_arr") or 0.0
    exp = b.get("expansion_arr") or 0.0
    rea = b.get("reactivation_arr") or 0.0
    con = b.get("contraction_arr") or 0.0
    chn = b.get("churn_arr") or 0.0
    end = beg + new + exp + rea - con - chn if beg is not None else None
    gross_new = new + exp
    losses = con + chn
    return {
        "beginning": beg, "new": new, "expansion": exp, "reactivation": rea,
        "contraction": con, "churn": chn, "computed_ending": end,
        "net_new": (end - beg) if (end is not None and beg is not None) else None,
        "quick_ratio_strict": safe_div(gross_new, losses),
        "quick_ratio_incl_reactivation": safe_div(gross_new + rea, losses),
        "leaky_bucket": safe_div(losses, gross_new),
        "stated_ending": b.get("stated_ending_arr"),
    }


def run_bridge(data: dict[str, Any]) -> None:
    rule("1. ARR BRIDGE")
    periods = [(k, v) for k, v in data.get("bridge", {}).items()]
    if not periods:
        print("No `bridge` block supplied — skipped, not faked.")
        return

    rows: list[list[str]] = []
    computed: dict[str, dict[str, Any]] = {}
    for label, blk in periods:
        r = bridge_line(blk)
        computed[label] = r
        beg = r["beginning"]
        rows.append([
            label, money(beg), money(r["new"]), money(r["expansion"]),
            money(r["reactivation"]), "(" + money(r["contraction"]) + ")",
            "(" + money(r["churn"]) + ")", money(r["computed_ending"]),
            num(r["quick_ratio_strict"], 2) if r["quick_ratio_strict"] is not None else "UNKNOWN",
        ])
    table(["Period", "Beginning", "New", "Expansion", "Reactivation",
           "Contraction", "Churn", "Ending", "Quick ratio"], rows)
    print("\nQuick ratio is the strict form: (New + Expansion) / (Churn + Contraction).")

    sub("Each line as a share of beginning ARR")
    rows = []
    for label, r in computed.items():
        beg = r["beginning"]
        rows.append([
            label,
            pct(safe_div(r["new"], beg), 1), pct(safe_div(r["expansion"], beg), 1),
            pct(safe_div(r["reactivation"], beg), 1), pct(safe_div(r["contraction"], beg), 1),
            pct(safe_div(r["churn"], beg), 1), pct(safe_div(r["net_new"], beg), 1),
            pct(r["leaky_bucket"], 1),
        ])
    table(["Period", "New", "Expansion", "React.", "Contraction", "Churn",
           "Net new", "Leaky bucket"], rows)
    print("\nLeaky bucket = (Churn + Contraction) / (New + Expansion). Above 50% means")
    print("more than half of gross new ARR is being consumed replacing losses.")

    sub("Tie-out to finance")
    for label, r in computed.items():
        stated = r["stated_ending"]
        if stated is None:
            print(f"{label}: computed ending {money(r['computed_ending'])} — "
                  f"UNKNOWN finance balance. DO NOT PUBLISH until reconciled.")
            continue
        var = r["computed_ending"] - stated
        verdict = "TIED — publish" if abs(var) < 0.5 else "VARIANCE — DO NOT PUBLISH"
        print(f"{label}: computed {money(r['computed_ending'])} vs finance {money(stated)} "
              f"→ variance {money(var)} — {verdict}")


# ---------------------------------------------------------------------------------------
# 2. Retention — cohort method and the formula approximation
# ---------------------------------------------------------------------------------------

def retention_pair(t0: float, churn: float, contraction: float,
                   expansion: float) -> tuple[float, float]:
    grr = (t0 - churn - contraction) / t0
    nrr = (t0 - churn - contraction + expansion) / t0
    return grr, nrr


def run_retention(data: dict[str, Any]) -> None:
    rule("2. RETENTION — COHORT METHOD vs FORMULA METHOD")
    coh = data.get("cohort_retention")
    if not coh:
        print("No `cohort_retention` block supplied — skipped, not faked.")
        return

    t0 = coh["t0_arr"]
    c_churn, c_contr, c_exp = coh["cohort_churn"], coh["cohort_contraction"], coh["cohort_expansion"]
    grr_c, nrr_c = retention_pair(t0, c_churn, c_contr, c_exp)

    tot = coh.get("total_period_movements") or {}
    have_total = all(k in tot for k in ("churn", "contraction", "expansion"))
    if have_total:
        grr_f, nrr_f = retention_pair(t0, tot["churn"], tot["contraction"], tot["expansion"])
        nrr_f_react = nrr_f + (tot.get("reactivation") or 0.0) / t0
    else:
        grr_f = nrr_f = nrr_f_react = None

    rows = [
        ["Cohort t0 ARR (frozen population)", money(t0), "", ""],
        ["GRR — cohort method (the standard)", pct(grr_c), "", ""],
        ["NRR — cohort method (the standard)", pct(nrr_c), "", ""],
    ]
    if grr_f is not None:
        rows += [
            ["GRR — formula approximation", pct(grr_f), bps(grr_f - grr_c),
             "understates" if grr_f < grr_c else "overstates"],
            ["NRR — formula approximation", pct(nrr_f), bps(nrr_f - nrr_c),
             "understates" if nrr_f < nrr_c else "overstates"],
            ["NRR — formula + reactivation (WRONG)", pct(nrr_f_react),
             bps(nrr_f_react - nrr_c), "overstates — reactivation is not retention"],
        ]
    table(["Measure", "Value", "vs cohort", "Direction"], rows, aligns="lrrl")

    logos = coh.get("logos")
    if logos:
        sub("Logo retention and the adverse-selection diagnostic")
        beg_logos = logos["beginning"]
        cohort_churned = logos["cohort_churned"]
        logo_ret = (beg_logos - cohort_churned) / beg_logos
        dollar_churn = c_churn / t0
        logo_churn = 1 - logo_ret
        avg_base = t0 / beg_logos
        avg_churned = safe_div(c_churn, cohort_churned)
        index = safe_div(avg_churned, avg_base)
        rows = [
            ["Cohort logo retention", pct(logo_ret)],
            ["Logo churn rate", pct(logo_churn)],
            ["Gross ARR churn rate (cohort)", pct(dollar_churn)],
            ["Average ARR, base at t0", money(avg_base)],
            ["Average ARR, churned account", money(avg_churned)],
            ["Adverse-selection index (churned ÷ base)", f"{index:.3f}x" if index else "UNKNOWN"],
        ]
        table(["Measure", "Value"], rows)
        if index and index > 1.0:
            print(f"\nDollar churn ({pct(dollar_churn,1)}) exceeds logo churn ({pct(logo_churn,1)}): "
                  "the accounts lost were LARGER than the base average.")
        elif index:
            print(f"\nLogo churn ({pct(logo_churn,1)}) exceeds dollar churn ({pct(dollar_churn,1)}): "
                  "the accounts lost were SMALLER than the base average.")
        print("Read this per segment as well — the blended index routinely hides both directions.")


# ---------------------------------------------------------------------------------------
# 3. Segment cuts
# ---------------------------------------------------------------------------------------

def run_segments(data: dict[str, Any]) -> None:
    rule("3. SEGMENT CUT — RETENTION AND ADVERSE SELECTION")
    segs = data.get("segments")
    if not segs:
        print("No `segments` block supplied — skipped, not faked.")
        return

    total_t0 = sum(s["t0_arr"] for s in segs)
    rows: list[list[str]] = []
    tot = {"t0": 0.0, "churn": 0.0, "contr": 0.0, "exp": 0.0, "logos": 0, "lchurn": 0}
    for s in segs:
        grr, nrr = retention_pair(s["t0_arr"], s["cohort_churn"],
                                  s["cohort_contraction"], s["cohort_expansion"])
        beg_l = s.get("t0_logos")
        ch_l = s.get("cohort_logos_churned")
        logo_ret = safe_div((beg_l - ch_l), beg_l) if beg_l else None
        avg_base = safe_div(s["t0_arr"], beg_l)
        avg_churned = safe_div(s["cohort_churn"], ch_l)
        index = safe_div(avg_churned, avg_base)
        small = (beg_l is not None and beg_l < SMALL_N_ACCOUNTS) or \
                (s["t0_arr"] / total_t0 < SMALL_N_ARR_SHARE)
        rows.append([
            s["name"] + (" *" if small else ""), money(s["t0_arr"]), pct(grr, 1), pct(nrr, 1),
            pct(logo_ret, 1), num(beg_l), num(ch_l),
            f"{index:.2f}x" if index else "UNKNOWN",
        ])
        tot["t0"] += s["t0_arr"]; tot["churn"] += s["cohort_churn"]
        tot["contr"] += s["cohort_contraction"]; tot["exp"] += s["cohort_expansion"]
        tot["logos"] += beg_l or 0; tot["lchurn"] += ch_l or 0

    grr_t, nrr_t = retention_pair(tot["t0"], tot["churn"], tot["contr"], tot["exp"])
    logo_ret_t = safe_div(tot["logos"] - tot["lchurn"], tot["logos"])
    idx_t = safe_div(safe_div(tot["churn"], tot["lchurn"]), safe_div(tot["t0"], tot["logos"]))
    rows.append(["**Blended**", money(tot["t0"]), pct(grr_t, 1), pct(nrr_t, 1),
                 pct(logo_ret_t, 1), num(tot["logos"]), num(tot["lchurn"]),
                 f"{idx_t:.2f}x" if idx_t else "UNKNOWN"])
    table(["Segment", "t0 ARR", "GRR", "NRR", "Logo ret.", "Logos t0",
           "Churned", "Adv. sel."], rows)
    print(f"\n* = below the small-n guard ({SMALL_N_ACCOUNTS} accounts or "
          f"{SMALL_N_ARR_SHARE:.0%} of base). Report the number, mark it, do not benchmark it.")
    spread = max(r for r in [retention_pair(s["t0_arr"], s["cohort_churn"],
                 s["cohort_contraction"], s["cohort_expansion"])[1] for s in segs]) - \
        min(r for r in [retention_pair(s["t0_arr"], s["cohort_churn"],
            s["cohort_contraction"], s["cohort_expansion"])[1] for s in segs])
    print(f"NRR spread across segments: {spread * 100:.1f} points. Above ~10 points the "
          "blended figure is not a usable number for anyone.")


# ---------------------------------------------------------------------------------------
# 4. Cohort retention triangle
# ---------------------------------------------------------------------------------------

def run_cohorts(data: dict[str, Any]) -> None:
    rule("4. COHORT RETENTION TRIANGLE (DOLLAR BASIS)")
    cohorts = data.get("cohort_table")
    if not cohorts:
        print("No `cohort_table` block supplied — skipped, not faked.")
        return

    max_len = max(len(c["arr_by_tenure"]) for c in cohorts)
    headers = ["Cohort", "t0 ARR"] + [f"T+{i}" for i in range(max_len)]
    rows: list[list[str]] = []
    for c in cohorts:
        series = c["arr_by_tenure"]
        base = series[0]
        cells = [pct(v / base, 1) if v is not None else "—" for v in series]
        cells += ["·"] * (max_len - len(series))
        rows.append([c["cohort"], money(base)] + cells)
    table(headers, rows)
    print("\n`·` = cell does not exist yet (cohort immature). Never compare an immature cell "
          "to a mature one;\nthe comparison is only valid down a column.")

    sub("Cohort-quality drift — same tenure point, successive cohorts")
    for t in (1, 2, 3):
        pts = [(c["cohort"], c["arr_by_tenure"][t] / c["arr_by_tenure"][0])
               for c in cohorts if len(c["arr_by_tenure"]) > t]
        if len(pts) < 3:
            continue
        first, last = pts[0], pts[-1]
        delta = last[1] - first[1]
        series = "  ".join(f"{lbl}:{v * 100:.1f}%" for lbl, v in pts)
        print(f"T+{t}:  {series}")
        print(f"       {first[0]} → {last[0]}: {bps(delta)}  "
              f"({'deteriorating' if delta < 0 else 'improving'})")


# ---------------------------------------------------------------------------------------
# 5. Health migration matrix — the section this report exists for
# ---------------------------------------------------------------------------------------

def _matrix_totals(matrix: dict[str, dict[str, float]]) -> dict[str, float]:
    return {band: sum(matrix.get(band, {}).values()) for band in BANDS}


def _split(matrix: dict[str, dict[str, float]]) -> dict[str, float]:
    """Four-way split of the t0 population: improved / held / degraded / churned."""
    improved = held = degraded = churned = 0.0
    for i, frm in enumerate(BANDS):
        row = matrix.get(frm, {})
        churned += row.get(CHURNED, 0.0)
        for j, to in enumerate(BANDS):
            v = row.get(to, 0.0)
            if j < i:
                improved += v
            elif j == i:
                held += v
            else:
                degraded += v
    return {"improved": improved, "held": held, "degraded": degraded, "churned": churned}


def _band_steps(matrix: dict[str, dict[str, float]]) -> float:
    """Weighted net band-steps. Positive = the book degraded. Churn counts as one step past Critical."""
    idx = {b: i for i, b in enumerate(BANDS)}
    idx[CHURNED] = len(BANDS)
    total = 0.0
    for frm, row in matrix.items():
        for to, v in row.items():
            total += v * (idx[to] - idx[frm])
    return total


def _rates(counts: dict[str, dict[str, float]]) -> dict[str, float | None]:
    tot = _matrix_totals(counts)
    n_total = sum(tot.values())
    split = _split(counts)

    eligible_up = n_total - tot.get("Secure", 0.0)
    eligible_down = n_total - tot.get("Critical", 0.0)
    red_t0 = tot.get("At Risk", 0.0) + tot.get("High Risk", 0.0) + tot.get("Critical", 0.0)
    rescued = sum(counts.get(b, {}).get(t, 0.0)
                  for b in ("At Risk", "High Risk", "Critical") for t in ("Secure", "Watch"))
    green_t0 = tot.get("Secure", 0.0) + tot.get("Watch", 0.0)
    slid = sum(counts.get(b, {}).get(t, 0.0)
               for b in ("Secure", "Watch")
               for t in ("At Risk", "High Risk", "Critical", CHURNED))
    false_green = sum(counts.get(b, {}).get(CHURNED, 0.0) for b in ("Secure", "Watch"))
    hi_t0 = tot.get("High Risk", 0.0) + tot.get("Critical", 0.0)
    hi_churn = sum(counts.get(b, {}).get(CHURNED, 0.0) for b in ("High Risk", "Critical"))
    sec_churn = counts.get("Secure", {}).get(CHURNED, 0.0)
    sec_rate = safe_div(sec_churn, tot.get("Secure", 0.0))
    hi_rate = safe_div(hi_churn, hi_t0)
    return {
        "n_total": n_total,
        "stability": safe_div(split["held"], n_total),
        "improvement": safe_div(split["improved"], eligible_up),
        "degradation": safe_div(split["degraded"], eligible_down),
        "rescue": safe_div(rescued, red_t0),
        "slide": safe_div(slid, green_t0),
        "false_green": safe_div(false_green, green_t0),
        "false_green_n": false_green,
        "churn_rate_secure": sec_rate,
        "churn_rate_high_critical": hi_rate,
        "predictive_lift": safe_div(hi_rate, sec_rate),
        "secure_churn_n": sec_churn,
    }


def run_migration(data: dict[str, Any]) -> None:
    rule("5. HEALTH MIGRATION MATRIX")
    mig = data.get("migration")
    if not mig:
        print("No `migration` block supplied — skipped, not faked.")
        return

    counts = mig["counts"]
    arr = mig.get("arr")
    print(f"Frozen t0 population as at {mig.get('t0_date', 'UNKNOWN')} → "
          f"band as at {mig.get('t1_date', 'UNKNOWN')}.")
    print("Accounts that entered the base after t0 are NOT in this matrix; they appear as a "
          "memo line only.")

    cols = BANDS + [CHURNED]
    for label, matrix, fmt in (("Accounts", counts, num), ("ARR", arr, money)):
        if matrix is None:
            continue
        sub(f"Matrix — {label} (rows = band at t0, columns = band at t1)")
        rows = []
        for b in BANDS:
            row = matrix.get(b, {})
            rows.append([b] + [fmt(row.get(c, 0)) for c in cols] +
                        [fmt(sum(row.values()))])
        rows.append(["**Total t1**"] +
                    [fmt(sum(matrix.get(b, {}).get(c, 0) for b in BANDS)) for c in cols] +
                    [fmt(sum(sum(matrix.get(b, {}).values()) for b in BANDS))])
        table(["t0 \\ t1"] + cols + ["Total t0"], rows)

    sub("Derived rates — accounts")
    r = _rates(counts)
    split_n = _split(counts)
    rows = [
        ["Stability (held their band)", pct(r["stability"], 1),
         "Σ diagonal ÷ total t0"],
        ["Improvement rate", pct(r["improvement"], 1),
         "moved ≥1 band toward Secure ÷ accounts able to improve"],
        ["Degradation rate", pct(r["degradation"], 1),
         "moved ≥1 band away from Secure (excl. churn) ÷ accounts able to degrade"],
        ["Rescue rate", pct(r["rescue"], 1),
         "At Risk/High/Critical at t0 that ended Secure or Watch"],
        ["Slide rate", pct(r["slide"], 1),
         "Secure/Watch at t0 that ended At Risk or worse, incl. churned"],
        ["**False-green rate**", pct(r["false_green"], 2),
         f"Secure/Watch at t0 that CHURNED (n={num(r['false_green_n'])})"],
    ]
    table(["Rate", "Value", "Definition"], rows, aligns="lrl")

    print(f"\nFour-way split of the t0 population (accounts): improved {num(split_n['improved'])} · "
          f"held {num(split_n['held'])} · degraded {num(split_n['degraded'])} · "
          f"churned {num(split_n['churned'])}")
    print(f"Net band-steps (positive = book degraded): {num(_band_steps(counts))}")

    if arr:
        split_a = _split(arr)
        ra = _rates(arr)
        total_churn_arr = split_a["churned"]
        fg_arr = sum(arr.get(b, {}).get(CHURNED, 0.0) for b in ("Secure", "Watch"))
        sub("Derived rates — ARR")
        rows = [
            ["ARR that improved a band", money(split_a["improved"])],
            ["ARR that held", money(split_a["held"])],
            ["ARR that degraded a band", money(split_a["degraded"])],
            ["ARR that churned", money(split_a["churned"])],
            ["ARR-weighted false-green rate", pct(ra["false_green"], 2)],
            ["Churned ARR that was Secure or Watch at t0", money(fg_arr)],
            ["...as a share of all ARR churned in the window",
             pct(safe_div(fg_arr, total_churn_arr), 1)],
            ["Net band-steps, ARR-weighted", money(_band_steps(arr))],
        ]
        table(["Measure", "Value"], rows)
        print("\nThe last three lines are the point of this matrix. A distribution chart cannot "
              "produce them,\nand they are the only evidence in the report that the health score "
              "discriminates and that the\nteam changed an outcome rather than watched one.")

    sub("Predictive lift — does the score discriminate?")
    rows = [
        ["Churn rate, Secure at t0", pct(r["churn_rate_secure"], 2),
         f"n={num(r['secure_churn_n'])} churned"],
        ["Churn rate, High Risk + Critical at t0", pct(r["churn_rate_high_critical"], 2), ""],
        ["Lift (High+Critical ÷ Secure)",
         f"{r['predictive_lift']:.1f}x" if r["predictive_lift"] else "UNKNOWN",
         "threshold: below 3x the score is decoration"],
    ]
    table(["Measure", "Value", "Note"], rows, aligns="lrl")
    if r["predictive_lift"] is not None and r["predictive_lift"] < 3:
        print("\nThe score does not discriminate. Retire or refit it before any section of this "
              "report\nuses a band as evidence — see health-score-designer.")
    if r["secure_churn_n"] is not None and r["secure_churn_n"] < 5:
        print(f"\nSMALL-N WARNING: the Secure churn numerator is n={num(r['secure_churn_n'])}. "
              "The lift ratio is unstable;\nreport the two absolute rates alongside it and do not "
              "quote the multiple on its own.")


# ---------------------------------------------------------------------------------------
# 6. Renewal forecast accuracy and bias
# ---------------------------------------------------------------------------------------

def run_forecast(data: dict[str, Any]) -> None:
    rule("6. RENEWAL FORECAST ACCURACY AND BIAS")
    hist = data.get("forecast_history")
    if not hist:
        print("No `forecast_history` block supplied — skipped, not faked.")
        return

    rows = []
    acc_sum = called_sum = closed_sum = abs_err = 0.0
    for h in hist:
        called, closed = h["called"], h["closed"]
        acc = 1 - abs(called - closed) / called
        bias = (called - closed) / closed
        rows.append([h["period"], money(called), money(closed),
                     money(closed - called), pct(acc, 1), pct(bias, 1)])
        acc_sum += acc
        called_sum += called
        closed_sum += closed
        abs_err += abs(called - closed)
    n = len(hist)
    rows.append(["**Mean / roll-up**", money(called_sum), money(closed_sum),
                 money(closed_sum - called_sum), pct(acc_sum / n, 1),
                 pct((called_sum - closed_sum) / closed_sum, 1)])
    table(["Period", "Called (frozen)", "Closed", "Variance", "Accuracy", "Bias"], rows)
    wape = abs_err / closed_sum
    print(f"\nWAPE across the window: {pct(wape, 1)} — the dispersion the roll-up hides.")
    signed = (called_sum - closed_sum) / closed_sum
    direction = "OPTIMISTIC" if signed > 0 else "CONSERVATIVE"
    print(f"Signed bias {pct(signed, 1)} → systematically {direction}.")
    print("Sustained bias in one direction is a coaching and category-definition problem, "
          "not a model problem.\nReport it next to accuracy; accuracy alone hides it because "
          "offsetting errors cancel in a roll-up.")


# ---------------------------------------------------------------------------------------
# sample input
# ---------------------------------------------------------------------------------------

SAMPLE: dict[str, Any] = {
    "meta": {
        "company": "Northwind Analytics",
        "period_label": "July 2026",
        "period_end": "2026-07-31",
        "units": "thousands of USD",
        "basis": "constant currency; cohort method; billing system as source of truth",
    },
    "bridge": {
        "Month (Jul-26)": {
            "beginning_arr": 103940, "new_arr": 1420, "expansion_arr": 980,
            "reactivation_arr": 60, "contraction_arr": 392, "churn_arr": 1196,
            "stated_ending_arr": 104812,
        },
        "TTM (Aug-25→Jul-26)": {
            "beginning_arr": 92600, "new_arr": 16840, "expansion_arr": 11120,
            "reactivation_arr": 640, "contraction_arr": 4510, "churn_arr": 11878,
            "stated_ending_arr": 104812,
        },
    },
    "cohort_retention": {
        "t0_date": "2025-08-01", "t1_date": "2026-07-31", "t0_arr": 92600,
        "cohort_churn": 11102, "cohort_contraction": 4268, "cohort_expansion": 9986,
        "total_period_movements": {
            "churn": 11878, "contraction": 4510, "expansion": 11120, "reactivation": 640,
        },
        "logos": {"beginning": 1148, "cohort_churned": 131},
    },
    "segments": [
        {"name": "Enterprise (>$150k ACV)", "t0_arr": 50300, "cohort_churn": 3820,
         "cohort_contraction": 2110, "cohort_expansion": 6940,
         "t0_logos": 96, "cohort_logos_churned": 7},
        {"name": "Mid-Market ($25–150k)", "t0_arr": 30100, "cohort_churn": 4180,
         "cohort_contraction": 1540, "cohort_expansion": 2620,
         "t0_logos": 352, "cohort_logos_churned": 46},
        {"name": "SMB (<$25k)", "t0_arr": 12200, "cohort_churn": 3102,
         "cohort_contraction": 618, "cohort_expansion": 426,
         "t0_logos": 700, "cohort_logos_churned": 78},
    ],
    "cohort_table": [
        {"cohort": "2024-Q3", "arr_by_tenure": [3820, 3735, 3660, 3600, 3540, 3490, 3450, 3420]},
        {"cohort": "2024-Q4", "arr_by_tenure": [4180, 4070, 3980, 3900, 3830, 3770, 3720]},
        {"cohort": "2025-Q1", "arr_by_tenure": [3960, 3830, 3730, 3640, 3560, 3490]},
        {"cohort": "2025-Q2", "arr_by_tenure": [4450, 4270, 4130, 4010, 3900]},
        {"cohort": "2025-Q3", "arr_by_tenure": [4310, 4090, 3930, 3790]},
        {"cohort": "2025-Q4", "arr_by_tenure": [4820, 4480, 4260]},
        {"cohort": "2026-Q1", "arr_by_tenure": [5140, 4640]},
        {"cohort": "2026-Q2", "arr_by_tenure": [4390]},
    ],
    "migration": {
        "t0_date": "2026-04-30", "t1_date": "2026-07-31",
        "counts": {
            "Secure":    {"Secure": 498, "Watch": 78, "At Risk": 19, "High Risk": 6, "Critical": 1, "Churned": 2},
            "Watch":     {"Secure": 62, "Watch": 231, "At Risk": 44, "High Risk": 15, "Critical": 4, "Churned": 5},
            "At Risk":   {"Secure": 11, "Watch": 43, "At Risk": 88, "High Risk": 21, "Critical": 6, "Churned": 7},
            "High Risk": {"Secure": 2, "Watch": 9, "At Risk": 21, "High Risk": 24, "Critical": 6, "Churned": 6},
            "Critical":  {"Secure": 0, "Watch": 1, "At Risk": 4, "High Risk": 5, "Critical": 6, "Churned": 7},
        },
        "arr": {
            "Secure":    {"Secure": 44900, "Watch": 5900, "At Risk": 1300, "High Risk": 430, "Critical": 90, "Churned": 180},
            "Watch":     {"Secure": 5400, "Watch": 17700, "At Risk": 3400, "High Risk": 1080, "Critical": 300, "Churned": 520},
            "At Risk":   {"Secure": 900, "Watch": 3500, "At Risk": 6700, "High Risk": 1400, "Critical": 500, "Churned": 900},
            "High Risk": {"Secure": 140, "Watch": 620, "At Risk": 1500, "High Risk": 1540, "Critical": 400, "Churned": 700},
            "Critical":  {"Secure": 0, "Watch": 80, "At Risk": 320, "High Risk": 400, "Critical": 400, "Churned": 700},
        },
    },
    "forecast_history": [
        {"period": "FY26 Q1", "called": 16900, "closed": 16100},
        {"period": "FY26 Q2", "called": 18200, "closed": 17050},
        {"period": "FY26 Q3", "called": 17400, "closed": 16900},
        {"period": "FY26 Q4", "called": 20300, "closed": 18600},
    ],
}

SECTIONS = {
    "bridge": run_bridge,
    "retention": run_retention,
    "segments": run_segments,
    "cohorts": run_cohorts,
    "migration": run_migration,
    "forecast": run_forecast,
}


def main() -> int:
    ap = argparse.ArgumentParser(description="Retention report arithmetic (stdlib only).")
    ap.add_argument("input", nargs="?", help="path to the input JSON")
    ap.add_argument("--section", choices=sorted(SECTIONS), help="run one section only")
    ap.add_argument("--emit-sample", action="store_true", help="print a sample input JSON")
    args = ap.parse_args()

    if args.emit_sample:
        print(json.dumps(SAMPLE, indent=2))
        return 0
    if not args.input:
        ap.error("provide an input JSON path, or --emit-sample")

    try:
        data = json.loads(open(args.input).read())
    except (OSError, json.JSONDecodeError) as e:
        print(f"could not read input: {e}", file=sys.stderr)
        return 2

    meta = data.get("meta", {})
    print(f"RETENTION REPORT ARITHMETIC — {meta.get('company', 'UNKNOWN')} · "
          f"{meta.get('period_label', 'UNKNOWN')}")
    print(f"Units: {meta.get('units', 'UNKNOWN')} · Basis: {meta.get('basis', 'UNKNOWN')}")
    print("Every figure below is computed from the supplied input. Nothing is imputed.")

    for name, fn in SECTIONS.items():
        if args.section and name != args.section:
            continue
        fn(data)

    print("\n" + "=" * 78)
    print("Reconcile the bridge to finance BEFORE quoting any retention figure. A retention")
    print("number computed off an unreconciled base is wrong in a way nobody can see.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
