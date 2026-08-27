#!/usr/bin/env python3
"""
Backtest a health score against actual renewal outcomes.

Deterministic, standard library only, no network. Every figure it prints is
reproducible from the input file, and the arithmetic is printed alongside the
result so a reviewer can audit it rather than trust it.

    python3 backtest.py scores.csv
    python3 backtest.py scores.csv --capacity 200
    python3 backtest.py scores.csv --segment-col segment
    python3 backtest.py scores.csv --prob-col p_churn      # enables the Brier score

Input: a CSV with one row per *scored account at a point in time*, snapshotted
at T-N days from the OPT-OUT DEADLINE (not the renewal date). Required columns:

    account_id   any string
    score        0-100, higher = healthier   (health space)
    outcome      1 = the negative event happened, 0 = it did not
    arr          annual recurring revenue at snapshot time (numeric)

Optional:
    segment      any string, for the per-segment breakdown
    p_churn      a fitted probability, if one exists (--prob-col)

The script refuses to print a Brier score unless a probability column is
supplied. A rubric score is an ordering, not a forecast (R22), and dressing it
up as a probability is the fastest way to discredit it. Build the reliability
curve from the decile table once a calibration map exists (calibration.md §5).

Exit codes: 0 = ran · 1 = input problem
"""

from __future__ import annotations

import argparse
import csv
import sys
from collections import defaultdict


# ---------------------------------------------------------------- loading

REQUIRED = ("account_id", "score", "outcome", "arr")


def _num(value, field, row_no):
    text = str(value).strip().replace("$", "").replace(",", "").replace("%", "")
    if text in ("", "-", "NA", "N/A", "null", "None"):
        raise ValueError(f"row {row_no}: {field} is empty — drop the row or impute explicitly")
    try:
        return float(text)
    except ValueError:
        raise ValueError(f"row {row_no}: {field}={value!r} is not numeric")


def load(path, segment_col=None, prob_col=None):
    with open(path, newline="", encoding="utf-8-sig") as fh:
        sample = fh.read(8192)
        fh.seek(0)
        try:
            dialect = csv.Sniffer().sniff(sample, delimiters=",;\t|")
        except csv.Error:
            dialect = csv.excel
        reader = csv.DictReader(fh, dialect=dialect)
        headers = [h.strip() for h in (reader.fieldnames or [])]
        missing = [c for c in REQUIRED if c not in headers]
        if missing:
            raise ValueError(
                f"missing required column(s): {', '.join(missing)}\n"
                f"found: {', '.join(headers)}"
            )
        rows = []
        for i, raw in enumerate(reader, start=2):
            row = {(k.strip() if k else k): v for k, v in raw.items()}
            rec = {
                "account_id": (row.get("account_id") or "").strip(),
                "score": _num(row.get("score"), "score", i),
                "outcome": int(_num(row.get("outcome"), "outcome", i)),
                "arr": _num(row.get("arr"), "arr", i),
            }
            if rec["outcome"] not in (0, 1):
                raise ValueError(f"row {i}: outcome must be 0 or 1, got {rec['outcome']}")
            if not 0 <= rec["score"] <= 100:
                raise ValueError(f"row {i}: score {rec['score']} outside 0-100 health space")
            rec["segment"] = (row.get(segment_col) or "—").strip() if segment_col else "—"
            rec["prob"] = _num(row.get(prob_col), prob_col, i) if prob_col else None
            rows.append(rec)
    if not rows:
        raise ValueError("no data rows")
    return rows


# ---------------------------------------------------------------- metrics

def auc_roc(rows):
    """Rank-based AUC on RISK (100 - score), ties averaged. No numpy."""
    ranked = sorted(rows, key=lambda r: 100.0 - r["score"])
    ranks, i = {}, 0
    while i < len(ranked):
        j = i
        while j + 1 < len(ranked) and (100.0 - ranked[j + 1]["score"]) == (100.0 - ranked[i]["score"]):
            j += 1
        avg = (i + j) / 2.0 + 1.0
        for k in range(i, j + 1):
            ranks[id(ranked[k])] = avg
        i = j + 1
    pos = [r for r in rows if r["outcome"] == 1]
    neg = [r for r in rows if r["outcome"] == 0]
    if not pos or not neg:
        return None
    sum_pos = sum(ranks[id(r)] for r in pos)
    n1, n0 = len(pos), len(neg)
    return (sum_pos - n1 * (n1 + 1) / 2.0) / (n1 * n0)


def pr_auc(rows):
    """Average precision over the risk-ordered list."""
    ordered = sorted(rows, key=lambda r: r["score"])  # worst health first
    total_pos = sum(r["outcome"] for r in ordered)
    if not total_pos:
        return None
    tp = 0
    ap = 0.0
    for i, r in enumerate(ordered, start=1):
        if r["outcome"] == 1:
            tp += 1
            ap += tp / i
    return ap / total_pos


def ks_stat(rows):
    ordered = sorted(rows, key=lambda r: r["score"])
    n1 = sum(r["outcome"] for r in ordered)
    n0 = len(ordered) - n1
    if not n1 or not n0:
        return None
    c1 = c0 = 0
    best = 0.0
    for r in ordered:
        if r["outcome"] == 1:
            c1 += 1
        else:
            c0 += 1
        best = max(best, abs(c1 / n1 - c0 / n0))
    return best


def brier(rows):
    vals = [r["prob"] for r in rows if r["prob"] is not None]
    if len(vals) != len(rows):
        return None
    return sum((r["prob"] - r["outcome"]) ** 2 for r in rows) / len(rows)


def deciles(rows, k=10):
    """Split worst-health-first into k equal buckets. Returns list of dicts."""
    ordered = sorted(rows, key=lambda r: r["score"])
    n = len(ordered)
    out = []
    for d in range(k):
        lo = (d * n) // k
        hi = ((d + 1) * n) // k
        chunk = ordered[lo:hi]
        if not chunk:
            continue
        losses = sum(r["outcome"] for r in chunk)
        out.append({
            "decile": d + 1,
            "n": len(chunk),
            "score_lo": min(r["score"] for r in chunk),
            "score_hi": max(r["score"] for r in chunk),
            "losses": losses,
            "loss_rate": losses / len(chunk),
            "arr_lost": sum(r["arr"] for r in chunk if r["outcome"] == 1),
        })
    return out


def threshold_table(rows, cuts=(0.05, 0.10, 0.20, 0.30)):
    ordered = sorted(rows, key=lambda r: r["score"])
    n = len(ordered)
    total_losses = sum(r["outcome"] for r in ordered)
    total_arr_lost = sum(r["arr"] for r in ordered if r["outcome"] == 1)
    table = []
    for c in cuts:
        k = max(1, int(round(n * c)))
        flagged = ordered[:k]
        caught = sum(r["outcome"] for r in flagged)
        arr_touched = sum(r["arr"] for r in flagged if r["outcome"] == 1)
        table.append({
            "cut": c,
            "flagged": k,
            "cut_score": flagged[-1]["score"],
            "caught": caught,
            "recall": caught / total_losses if total_losses else None,
            "precision": caught / k,
            "arr_touched": arr_touched,
            "arr_capture": arr_touched / total_arr_lost if total_arr_lost else None,
            "false_pos": k - caught,
        })
    return table


# ---------------------------------------------------------------- output

def money(x):
    if x >= 1_000_000:
        return f"${x/1_000_000:.1f}M"
    if x >= 1_000:
        return f"${x/1_000:.0f}k"
    return f"${x:.0f}"


def pct(x, dp=1):
    return "—" if x is None else f"{100*x:.{dp}f}%"


def report(rows, capacity=None, segment_col=None, prob_col=None):
    n = len(rows)
    losses = sum(r["outcome"] for r in rows)
    arr_total = sum(r["arr"] for r in rows)
    arr_lost = sum(r["arr"] for r in rows if r["outcome"] == 1)
    base_logo = losses / n
    base_arr = arr_lost / arr_total if arr_total else 0.0

    print("=" * 78)
    print("BACKTEST — health score vs actual outcomes")
    print("=" * 78)
    print(f"Population        {n} scored accounts, {money(arr_total)} ARR")
    print(f"Negative events   {losses} logos, {money(arr_lost)} ARR")
    print(f"Base rate (logo)  {losses}/{n} = {pct(base_logo)}")
    print(f"Base rate (ARR)   {money(arr_lost)}/{money(arr_total)} = {pct(base_arr)}")
    print()
    if losses < 50:
        print(f"!! {losses} negative events. Below ~50 the metrics below are unstable;")
        print("   treat them as directional and report bands, not probabilities (R22).")
        print()

    print("-" * 78)
    print("DECILES (worst health first)")
    print("-" * 78)
    print(f"{'Dec':>3} {'score range':>13} {'N':>5} {'losses':>7} {'rate':>7} "
          f"{'lift':>6} {'ARR lost':>10} {'ARR cap':>8}")
    dec = deciles(rows)
    cum_arr = 0.0
    for d in dec:
        cum_arr += d["arr_lost"]
        lift = d["loss_rate"] / base_logo if base_logo else 0
        print(f"{d['decile']:>3} {d['score_lo']:>6.0f}-{d['score_hi']:<6.0f} {d['n']:>5} "
              f"{d['losses']:>7} {pct(d['loss_rate'],1):>7} {lift:>5.2f}x "
              f"{money(d['arr_lost']):>10} {pct(cum_arr/arr_lost if arr_lost else None):>8}")
    top = dec[0]
    print()
    print(f"Top-decile lift   {pct(top['loss_rate'])} / {pct(base_logo)} = "
          f"{top['loss_rate']/base_logo:.2f}x   (target >=2.5x)")

    print()
    print("-" * 78)
    print("DISCRIMINATION")
    print("-" * 78)
    a = auc_roc(rows)
    p = pr_auc(rows)
    k = ks_stat(rows)
    print(f"AUC-ROC           {a:.3f}" if a is not None else "AUC-ROC           —")
    if p is not None:
        ratio = p / base_logo if base_logo else 0
        print(f"PR-AUC            {p:.3f}  = {ratio:.2f}x base rate  (target >=2.5x)")
        print("                  ^ use PR-AUC, not ROC-AUC, when the base rate is under 10%")
    print(f"KS                {k:.3f}" if k is not None else "KS                —")
    b = brier(rows)
    if b is None:
        print("Brier             not computed — no probability column supplied.")
        print("                  A rubric score is an ordering, not a forecast (R22).")
        print("                  Fit a calibration map on a held-out set, then re-run")
        print("                  with --prob-col.")
    else:
        const = base_logo
        b0 = sum((const - r["outcome"]) ** 2 for r in rows) / n
        red = 100 * (b0 - b) / b0 if b0 else 0.0
        verdict = "PASS" if red >= 20 else "FAIL"
        print(f"Brier             {b:.4f}  vs base-rate-constant {b0:.4f}")
        print(f"                  reduces Brier by {red:.1f}%  (target: >=20% reduction)  {verdict}")

    print()
    print("-" * 78)
    print("THRESHOLD CHOICE — precision and recall at each cut")
    print("-" * 78)
    print(f"{'cut':>6} {'score<=':>8} {'flagged':>8} {'caught':>7} {'recall':>8} "
          f"{'prec':>7} {'ARR touched':>12} {'false+':>7}")
    for t in threshold_table(rows):
        print(f"{pct(t['cut'],0):>6} {t['cut_score']:>8.0f} {t['flagged']:>8} {t['caught']:>7} "
              f"{pct(t['recall']):>8} {pct(t['precision']):>7} "
              f"{money(t['arr_touched']):>12} {t['false_pos']:>7}")

    if capacity:
        ordered = sorted(rows, key=lambda r: r["score"])
        k_cap = min(capacity, n)
        flagged = ordered[:k_cap]
        caught = sum(r["outcome"] for r in flagged)
        cut_score = flagged[-1]["score"]
        prec = caught / k_cap
        rec = caught / losses if losses else 0
        arr_t = sum(r["arr"] for r in flagged if r["outcome"] == 1)
        print()
        print(f"CAPACITY-SET RED THRESHOLD (capacity = {capacity} save motions)")
        print(f"  red = score <= {cut_score:.0f}   flags {k_cap} accounts "
              f"({100*k_cap/n:.0f}% of the book)")
        print(f"  catches {caught}/{losses} losses = {pct(rec)} recall, "
              f"{pct(prec)} precision, {money(arr_t)} of churned ARR in scope")
        if prec < 0.25:
            print("  !! precision under 25% — CSM credibility burns and reds get ignored.")
        if rec < 0.40:
            print("  !! recall under 40% — the score is not earning its build cost.")

    if segment_col:
        print()
        print("-" * 78)
        print(f"PER SEGMENT ({segment_col}) — aggregate strength can hide a segment at random")
        print("-" * 78)
        groups = defaultdict(list)
        for r in rows:
            groups[r["segment"]].append(r)
        print(f"{'segment':>18} {'N':>6} {'events':>7} {'base':>7} {'AUC':>6} {'top-dec lift':>13}")
        for seg in sorted(groups):
            g = groups[seg]
            ev = sum(r["outcome"] for r in g)
            if len(g) < 30 or ev < 5:
                print(f"{seg[:18]:>18} {len(g):>6} {ev:>7} {'—':>7} {'—':>6} "
                      f"{'too few to score':>13}")
                continue
            gb = ev / len(g)
            gd = deciles(g)
            gl = gd[0]["loss_rate"] / gb if gb else 0
            ga = auc_roc(g)
            print(f"{seg[:18]:>18} {len(g):>6} {ev:>7} {pct(gb,1):>7} "
                  f"{(f'{ga:.3f}' if ga is not None else '—'):>6} {gl:>12.2f}x")

    print()
    print("-" * 78)
    print("READ THIS BEFORE QUOTING ANY NUMBER ABOVE")
    print("-" * 78)
    print("1. Accuracy is not reported here on purpose. At a low base rate, predicting")
    print("   nobody churns scores well and is worth nothing.")
    print("2. These figures are only honest if the scores were snapshotted point-in-time")
    print("   from the OPT-OUT DEADLINE and rebuilt from event logs, not current-state")
    print("   tables. Current-state features are the number-one source of leakage.")
    print("3. Split temporally before you trust a held-out figure. A random split leaks")
    print("   the future and inflates AUC.")
    print("4. Autopsy 20 false-greens and 20 false-reds by hand. That produces more")
    print("   improvement per hour than any parameter search.")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("csv_path")
    ap.add_argument("--capacity", type=int, default=None,
                    help="save motions available per period; sets the red threshold")
    ap.add_argument("--segment-col", default=None, help="column to break results down by")
    ap.add_argument("--prob-col", default=None,
                    help="fitted probability column; enables Brier")
    args = ap.parse_args()
    try:
        rows = load(args.csv_path, args.segment_col, args.prob_col)
    except (OSError, ValueError) as e:
        print(f"error: {e}", file=sys.stderr)
        return 1
    report(rows, args.capacity, args.segment_col, args.prob_col)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
