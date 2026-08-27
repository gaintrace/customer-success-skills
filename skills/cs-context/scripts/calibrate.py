#!/usr/bin/env python3
"""
Calibrate the risk model against this company's own renewal history.

Why this exists: every default weight, band threshold and probability in this library was
chosen by a human being with an opinion. That is a legitimate starting point and an
illegitimate ending point. Until a model has been tested against renewals that actually
happened, it produces an *ordering* — this account is riskier than that one — and nothing
more. A cardinal probability from an uncalibrated rules-based score is a fabricated number
with a decimal point on it.

This script converts the ordering into something empirical, or tells you plainly that you do
not have enough history to do so yet.

    python3 calibrate.py history.json                       # report only
    python3 calibrate.py history.json --write               # write .agents/cs-calibration.json
    python3 calibrate.py history.json --capacity 12         # threshold for 12 workable red accounts/mo
    python3 calibrate.py history.json --profile plg

Input: JSON list of historical accounts, each scored at a frozen point BEFORE the outcome was
known, with the outcome that followed.

    [{
      "account_id": "ACME",
      "arr": 148000,
      "scored_at": "2025-06-01",          # feature freeze date
      "decision_date": "2025-08-14",      # when THEY decided, not the contract end date
      "outcome": "churned",               # renewed | churned | downgraded
      "arr_after": 0,
      "families": {"usage": 72, "commercial": 90, "relationship": 65,
                   "support": 30, "sentiment": null, "billing": 10, "firmographic": 0}
    }, ...]

Standard library only. No network. Deterministic — same input, same output.
"""

from __future__ import annotations

import argparse
import json
import math
import random
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any

FAMILIES = ["usage", "commercial", "relationship", "support",
            "sentiment", "billing", "firmographic"]

DEFAULT_WEIGHTS = {
    "enterprise":  {"usage": 22, "commercial": 25, "relationship": 20,
                    "support": 12, "sentiment": 9, "billing": 7, "firmographic": 5},
    "plg":         {"usage": 35, "commercial": 15, "relationship": 10,
                    "support": 13, "sentiment": 10, "billing": 12, "firmographic": 5},
    "consumption": {"usage": 30, "commercial": 20, "relationship": 15,
                    "support": 12, "sentiment": 8, "billing": 10, "firmographic": 5},
}

BANDS = [(24, "Secure"), (44, "Watch"), (64, "At Risk"), (84, "High Risk"), (100, "Critical")]

# Below these, a calibration is noise dressed as evidence. The script says so rather than
# emitting a confident number from 14 renewals.
MIN_TOTAL = 100
MIN_EVENTS = 30
MIN_PER_BAND = 8


# ======================================================================================
# Loading
# ======================================================================================

def load(path: Path) -> list[dict[str, Any]]:
    data = json.loads(path.read_text())
    if isinstance(data, dict):
        for k in ("accounts", "history", "records", "data"):
            if isinstance(data.get(k), list):
                data = data[k]
                break
    rows: list[dict[str, Any]] = []
    problems: list[str] = []
    for i, r in enumerate(data):
        outcome = str(r.get("outcome", "")).lower().strip()
        if outcome not in {"renewed", "churned", "downgraded"}:
            problems.append(f"row {i}: outcome {outcome!r} not in renewed/churned/downgraded")
            continue
        fams = r.get("families") or {}
        if not any(fams.get(f) is not None for f in FAMILIES):
            problems.append(f"row {i} ({r.get('account_id')}): no family scores")
            continue
        # Leakage guard. A feature frozen after the customer decided is not a prediction.
        sa, dd = r.get("scored_at"), r.get("decision_date")
        if sa and dd:
            try:
                if datetime.fromisoformat(sa).date() >= datetime.fromisoformat(dd).date():
                    problems.append(
                        f"row {i} ({r.get('account_id')}): scored_at {sa} is not before "
                        f"decision_date {dd} — LEAKAGE, excluded")
                    continue
            except ValueError:
                pass
        r["_label"] = 1 if outcome in {"churned", "downgraded"} else 0
        r["_horizon"] = _days(sa, dd)
        rows.append(r)
    if problems:
        print("Excluded rows:", file=sys.stderr)
        for p in problems[:20]:
            print(f"  {p}", file=sys.stderr)
        if len(problems) > 20:
            print(f"  … and {len(problems) - 20} more", file=sys.stderr)
        print(file=sys.stderr)
    return rows


def _days(a: str | None, b: str | None) -> int | None:
    if not a or not b:
        return None
    try:
        return (datetime.fromisoformat(b).date() - datetime.fromisoformat(a).date()).days
    except ValueError:
        return None


# ======================================================================================
# Scoring with a given weight set (mirrors churn-risk/scripts/risk_score.py step 2)
# ======================================================================================

def score(row: dict[str, Any], weights: dict[str, float]) -> float:
    fams = row.get("families") or {}
    present = {f: float(fams[f]) for f in FAMILIES if fams.get(f) is not None}
    if not present:
        return 0.0
    total_w = sum(weights[f] for f in present) or 1.0
    return sum(present[f] * weights[f] for f in present) / total_w


def band_of(s: float) -> str:
    for upper, label in BANDS:
        if s <= upper:
            return label
    return BANDS[-1][1]


# ======================================================================================
# Metrics — the ones that mean something at a 5-20% base rate
# ======================================================================================

def auc(scores: list[float], labels: list[int]) -> float | None:
    """Probability a random churner scores above a random renewer. Ties count as half."""
    pos = [s for s, l in zip(scores, labels) if l == 1]
    neg = [s for s, l in zip(scores, labels) if l == 0]
    if not pos or not neg:
        return None
    wins = sum(1.0 if p > n else 0.5 if p == n else 0.0 for p in pos for n in neg)
    return wins / (len(pos) * len(neg))


def brier(probs: list[float], labels: list[int]) -> float:
    return sum((p - l) ** 2 for p, l in zip(probs, labels)) / len(labels)


def lift_at_decile(scores: list[float], labels: list[int], k: float = 0.1) -> tuple[float, float] | None:
    """(lift, capture rate) in the top k of the book by score."""
    n = len(scores)
    top = max(1, int(round(n * k)))
    order = sorted(range(n), key=lambda i: -scores[i])[:top]
    base = sum(labels) / n
    if base == 0:
        return None
    hits = sum(labels[i] for i in order)
    return (hits / top) / base, hits / sum(labels)


def dollars_captured(rows: list[dict], scores: list[float], k: float = 0.1) -> tuple[float, float]:
    n = len(rows)
    top = max(1, int(round(n * k)))
    order = sorted(range(n), key=lambda i: -scores[i])[:top]
    lost_total = sum(_arr_lost(r) for r in rows)
    lost_top = sum(_arr_lost(rows[i]) for i in order)
    return lost_top, (lost_top / lost_total if lost_total else 0.0)


def _arr_lost(r: dict) -> float:
    if r["_label"] == 0:
        return 0.0
    arr = float(r.get("arr") or 0)
    after = r.get("arr_after")
    return arr - float(after) if after is not None else arr


# ======================================================================================
# Weight fitting — plain logistic regression, no dependencies
# ======================================================================================

def fit_weights(rows: list[dict], start: dict[str, float], seed: int = 7,
                epochs: int = 400, lr: float = 0.08) -> tuple[dict[str, float], dict[str, Any]]:
    """
    Fit family weights by gradient descent on log-loss, then renormalise to sum 100 so the
    result is directly substitutable into the scoring model.

    Deliberately simple and deliberately regularised toward the defaults: with a few hundred
    rows and seven features, an unconstrained fit will happily produce a weight of 61 on
    `commercial` from noise. The L2 pull toward the prior keeps it defensible.
    """
    random.seed(seed)
    feats: list[list[float]] = []
    labels: list[int] = []
    for r in rows:
        fams = r.get("families") or {}
        # Mean-impute a missing family at the population mean so a gap does not read as zero risk.
        feats.append([(float(fams[f]) / 100.0) if fams.get(f) is not None else -1.0 for f in FAMILIES])
        labels.append(r["_label"])

    means = []
    for j in range(len(FAMILIES)):
        vals = [row[j] for row in feats if row[j] >= 0]
        means.append(sum(vals) / len(vals) if vals else 0.5)
    for row in feats:
        for j in range(len(FAMILIES)):
            if row[j] < 0:
                row[j] = means[j]

    prior = [start[f] / 100.0 for f in FAMILIES]
    w = list(prior)
    b = 0.0
    lam = 0.5                     # pull toward the prior

    n = len(feats)
    for _ in range(epochs):
        gw = [0.0] * len(FAMILIES)
        gb = 0.0
        for x, y in zip(feats, labels):
            z = b + sum(wi * xi for wi, xi in zip(w, x))
            p = 1.0 / (1.0 + math.exp(-max(-30.0, min(30.0, z))))
            err = p - y
            for j in range(len(FAMILIES)):
                gw[j] += err * x[j]
            gb += err
        for j in range(len(FAMILIES)):
            w[j] -= lr * (gw[j] / n + lam * (w[j] - prior[j]) / n)
        b -= lr * gb / n

    # Negative coefficients mean "this family, as measured, does not indicate risk here".
    # Floor at a small positive value rather than inverting the model's meaning.
    raw = {f: max(0.5, w[j] * 100.0) for j, f in enumerate(FAMILIES)}
    total = sum(raw.values())
    fitted = {f: round(v / total * 100.0, 1) for f, v in raw.items()}

    moves = {f: round(fitted[f] - start[f], 1) for f in FAMILIES}
    return fitted, {"intercept": round(b, 3), "moves": moves,
                    "regularisation": lam, "imputed_means": dict(zip(FAMILIES, [round(m, 3) for m in means]))}


# ======================================================================================
# Reporting
# ======================================================================================

def band_table(rows: list[dict], scores: list[float]) -> tuple[list[str], dict[str, float]]:
    buckets: dict[str, list[dict]] = defaultdict(list)
    for r, s in zip(rows, scores):
        buckets[band_of(s)].append(r)

    out = ["| Band | Accounts | Churn/downgrade events | **Observed rate** | Library default | Δ | ARR lost |",
           "|---|---|---|---|---|---|---|"]
    defaults = {"Secure": 0.05, "Watch": 0.15, "At Risk": 0.35, "High Risk": 0.60, "Critical": 0.85}
    observed: dict[str, float] = {}
    for _, label in BANDS:
        b = buckets.get(label, [])
        if not b:
            out.append(f"| {label} | 0 | 0 | — | {defaults[label]:.2f} | — | — |")
            continue
        events = sum(r["_label"] for r in b)
        rate = events / len(b)
        lost = sum(_arr_lost(r) for r in b)
        flag = "" if len(b) >= MIN_PER_BAND else " ⚠"
        observed[label] = round(rate, 3)
        out.append(f"| {label} | {len(b)}{flag} | {events} | **{rate:.2f}** | {defaults[label]:.2f} | "
                   f"{rate - defaults[label]:+.2f} | ${lost:,.0f} |")
    out.append("")
    out.append(f"⚠ = fewer than {MIN_PER_BAND} accounts in the band; that rate is not usable yet.")
    return out, observed


def monotonic(observed: dict[str, float]) -> tuple[bool, str]:
    order = [l for _, l in BANDS if l in observed]
    rates = [observed[l] for l in order]
    ok = all(rates[i] <= rates[i + 1] + 1e-9 for i in range(len(rates) - 1))
    if ok:
        return True, "Rates rise monotonically across bands — the ordering holds."
    breaks = [f"{order[i]} ({rates[i]:.2f}) → {order[i+1]} ({rates[i+1]:.2f})"
              for i in range(len(rates) - 1) if rates[i] > rates[i + 1]]
    return False, ("Rates are NOT monotonic: " + "; ".join(breaks) +
                   ". The model is mis-ordering accounts. Do not publish band probabilities; "
                   "investigate the families driving the inversion before using this in a forecast.")


def threshold_for_capacity(rows: list[dict], scores: list[float], capacity: int) -> list[str]:
    n = len(rows)
    order = sorted(range(n), key=lambda i: -scores[i])
    cap = min(capacity, n)
    picked = order[:cap]
    hits = sum(rows[i]["_label"] for i in picked)
    total_events = sum(r["_label"] for r in rows)
    cutoff = scores[picked[-1]] if picked else 0.0
    prec = hits / cap if cap else 0.0
    rec = hits / total_events if total_events else 0.0
    lost_caught = sum(_arr_lost(rows[i]) for i in picked)
    lost_total = sum(_arr_lost(r) for r in rows)
    lines = [
        f"With capacity for **{capacity}** worked accounts per cycle:",
        "",
        f"- Score cutoff: **{cutoff:.1f}**",
        f"- Precision: **{prec:.0%}** ({hits} of {cap} worked accounts were genuine events)",
        f"- Recall: **{rec:.0%}** ({hits} of {total_events} events caught)",
        f"- ARR at risk reached: **${lost_caught:,.0f}** of ${lost_total:,.0f} "
        f"(**{lost_caught / lost_total:.0%}**)" if lost_total else "- ARR at risk: no losses in sample",
    ]
    if prec < 0.30:
        lines.append("")
        lines.append("⚠ Precision below 30%. At that rate CSMs stop reading the alerts, and an "
                     "ignored alerting system is worse than none — it creates the appearance of "
                     "coverage. Either raise the cutoff (fewer, better accounts) or improve the "
                     "families driving the false positives before rolling this out.")
    return lines


def report(rows: list[dict], profile: str, capacity: int, do_fit: bool) -> tuple[str, dict | None]:
    o: list[str] = ["# Risk Model Calibration", ""]
    n = len(rows)
    events = sum(r["_label"] for r in rows)
    base = events / n if n else 0.0
    horizons = [r["_horizon"] for r in rows if r["_horizon"] is not None]

    o.append(f"**{n} accounts · {events} churn/downgrade events · base rate {base:.1%} · profile `{profile}`**")
    if horizons:
        horizons.sort()
        o.append(f"Feature-freeze horizon: median **{horizons[len(horizons)//2]} days** before the "
                 f"decision date (range {horizons[0]}–{horizons[-1]}).")
    o.append("")

    # --- The gate. Say plainly when there is not enough history. ---
    blocking: list[str] = []
    if n < MIN_TOTAL:
        blocking.append(f"only {n} scored accounts (need ≥{MIN_TOTAL})")
    if events < MIN_EVENTS:
        blocking.append(f"only {events} churn/downgrade events (need ≥{MIN_EVENTS})")

    weights = dict(DEFAULT_WEIGHTS[profile])
    scores = [score(r, weights) for r in rows]

    if blocking:
        o.append("## ⛔ Not enough history to calibrate")
        o.append("")
        o.append("Blocking: " + "; ".join(blocking) + ".")
        o.append("")
        o.append("Fitting weights or publishing band probabilities on this sample would produce "
                 "numbers that look empirical and are not. What you can legitimately do with what "
                 "you have:")
        o.append("")
        o.append("- **Keep using the model as an ordering.** Rank accounts by risk and work down "
                 "the list. Ordering needs far less data than probability and is what a CSM "
                 "actually acts on.")
        o.append("- **Never state a churn probability.** Bands only, explicitly labelled as a "
                 "rules-based ordering rather than a forecast.")
        o.append("- **Start capturing what is missing** — the fields below are what unlock this.")
        o.append("")
        o.append("| Requirement | Have | Need |")
        o.append("|---|---|---|")
        o.append(f"| Scored accounts | {n} | {MIN_TOTAL} |")
        o.append(f"| Churn/downgrade events | {events} | {MIN_EVENTS} |")
        o.append("| Decision date (not contract end) | see exclusions above | every event |")
        o.append("| Family scores frozen before the decision | see exclusions above | every account |")
        o.append("")
        a = auc(scores, [r["_label"] for r in rows])
        if a is not None:
            o.append(f"For information only, and not to be published: rank-ordering AUC on this "
                     f"sample is **{a:.2f}**. At this sample size the confidence interval is wide "
                     f"enough that the number is directional at best.")
        return "\n".join(o), None

    # --- Full calibration ---
    o.append("## Observed outcome by band")
    o.append("")
    tbl, observed = band_table(rows, scores)
    o.extend(tbl)
    o.append("")
    ok, note = monotonic(observed)
    o.append(("✅ " if ok else "❌ ") + note)
    o.append("")

    o.append("## Discrimination")
    o.append("")
    a = auc(scores, [r["_label"] for r in rows])
    o.append(f"- **AUC {a:.3f}** — probability a random churner outscores a random renewer. "
             f"{'Useful' if a and a >= 0.70 else 'Weak — barely better than ordering at random' if a and a >= 0.60 else 'Not usable'}.")
    ld = lift_at_decile(scores, [r["_label"] for r in rows])
    if ld:
        o.append(f"- **Lift at top decile {ld[0]:.1f}×**, capturing **{ld[1]:.0%}** of all events "
                 f"in the top 10% of the book.")
    lost_top, share = dollars_captured(rows, scores)
    o.append(f"- **${lost_top:,.0f} ({share:.0%})** of all ARR lost sat in the top decile by score.")
    probs = [observed.get(band_of(s), base) for s in scores]
    o.append(f"- **Brier {brier(probs, [r['_label'] for r in rows]):.3f}** using the observed band "
             f"rates as the probability (lower is better; {base * (1 - base):.3f} is the "
             f"no-skill baseline).")
    o.append("")
    o.append("Accuracy is deliberately not reported. At a "
             f"{base:.0%} base rate, predicting 'renews' for everything scores {1-base:.0%} and "
             "is worthless.")
    o.append("")

    o.append("## Threshold for your capacity")
    o.append("")
    o.extend(threshold_for_capacity(rows, scores, capacity))
    o.append("")

    fitted = None
    fit_meta: dict[str, Any] = {}
    if do_fit:
        fitted, fit_meta = fit_weights(rows, weights)
        fitted_scores = [score(r, fitted) for r in rows]
        a2 = auc(fitted_scores, [r["_label"] for r in rows])
        o.append("## Fitted weights")
        o.append("")
        o.append("| Family | Library default | Fitted | Move |")
        o.append("|---|---|---|---|")
        for f in FAMILIES:
            o.append(f"| {f} | {weights[f]} | {fitted[f]} | {fit_meta['moves'][f]:+.1f} |")
        o.append("")
        o.append(f"AUC {a:.3f} → **{a2:.3f}** with fitted weights.")
        o.append("")
        if a2 is not None and a is not None and a2 - a < 0.02:
            o.append("The fit barely improves discrimination. Keep the defaults — they are easier "
                     "to explain, and an unexplainable score is an unused score.")
        o.append("")
        o.append("Weights are regularised toward the library defaults. With seven features and a "
                 "few hundred rows, an unconstrained fit will produce confident weights from "
                 "noise; the pull toward the prior is what stops that.")
        o.append("")

    o.append("## What to do with this")
    o.append("")
    if ok:
        o.append("1. Replace the band midpoints in `churn-risk` with the **observed rates** above, "
                 "and cite this calibration wherever a probability appears.")
        o.append("2. Set the alert cutoff from the capacity section, not from an F1 optimum.")
        o.append("3. Re-run quarterly. Weights drift with pricing, packaging and segment mix.")
    else:
        o.append("1. **Do not publish probabilities.** The ordering is broken; fix it first.")
        o.append("2. Investigate the inverted bands — usually one family is scored backwards, or a "
                 "signal is leaking post-decision information.")
    o.append("4. Feed `churn-postmortem` detection-lag findings back into signal lead times, then "
             "re-run this.")

    payload = {
        "calibrated_at_sample": {"accounts": n, "events": events, "base_rate": round(base, 4)},
        "profile": profile,
        "band_probabilities": observed,
        "monotonic": ok,
        "auc": round(a, 4) if a is not None else None,
        "capacity_cutoff": round(sorted(scores, reverse=True)[min(capacity, len(scores)) - 1], 1),
        "weights": fitted or weights,
        "weights_source": "fitted" if fitted else "library default",
        "fit": fit_meta or None,
        "usable_for_probability": bool(ok),
    }
    return "\n".join(o), payload


def main() -> int:
    ap = argparse.ArgumentParser(description="Calibrate the risk model against renewal history.")
    ap.add_argument("history", help="JSON of historically scored accounts with outcomes")
    ap.add_argument("--profile", default="enterprise", choices=sorted(DEFAULT_WEIGHTS))
    ap.add_argument("--capacity", type=int, default=10,
                    help="accounts a CSM/team can genuinely work per cycle (default 10)")
    ap.add_argument("--no-fit", action="store_true", help="skip weight fitting")
    ap.add_argument("--write", action="store_true",
                    help="write .agents/cs-calibration.json for the skills to read")
    args = ap.parse_args()

    rows = load(Path(args.history))
    if not rows:
        print("No usable rows.", file=sys.stderr)
        return 1

    text, payload = report(rows, args.profile, args.capacity, not args.no_fit)
    print(text)

    if args.write:
        if payload is None:
            print("\nNothing written — sample too small to calibrate.", file=sys.stderr)
            return 1
        out = Path(".agents"); out.mkdir(exist_ok=True)
        (out / "cs-calibration.json").write_text(json.dumps(payload, indent=2))
        print(f"\nWrote .agents/cs-calibration.json — `churn-risk` and `renewal-forecast` will "
              f"use these rates instead of the library defaults.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
