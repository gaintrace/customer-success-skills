#!/usr/bin/env python3
"""
cs-data-audit — deterministic scoring and ranking.

Three jobs the model must not do in prose:

  1. Score the seven signal families on five dimensions (0-20 each) using the bands in
     references/audit-procedures.md section 9, then derive the Coverage Ledger status,
     the coverage percentage and the downstream confidence cap (R23).
  2. Rank the remediation plan by  B * D * (1 + 0.1U) * C / E, with irreversible items
     (C = 1.5) surfacing ahead of larger-blast-radius items that can be fixed later.
  3. Compute the 95% confidence interval for a document-test accuracy, so no accuracy is
     ever published without n and an interval.

No network. Standard library only.

    python3 audit_score.py sample_audit.json
    python3 audit_score.py sample_audit.json --json
    python3 audit_score.py --ci 0.84 25
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

FAMILIES = [
    "product_usage",
    "commercial",
    "relationship",
    "support",
    "sentiment",
    "billing",
    "firmographic",
]

FAMILY_LABEL = {
    "product_usage": "Product usage & adoption",
    "commercial": "Commercial & contract",
    "relationship": "Relationship & engagement",
    "support": "Support & reliability",
    "sentiment": "Sentiment & VoC",
    "billing": "Billing & payment",
    "firmographic": "Firmographic & external",
}

# --- Band tables (references/audit-procedures.md section 9) -------------------------------
# Each is a list of (threshold, points) evaluated top-down; the first match wins.

PRESENCE = {
    "api": 20, "warehouse": 20,
    "export": 15, "export_only": 15,
    "manual": 10, "partial": 10,
    "adhoc": 5, "unowned": 5,
    "none": 0, "missing": 0,
}

ACCOUNT_COVERAGE = [(0.95, 20), (0.85, 15), (0.70, 10), (0.50, 5), (0.0, 0)]
FIELD_COMPLETENESS = [(0.90, 20), (0.75, 15), (0.60, 10), (0.40, 5), (0.0, 0)]
FIDELITY = [(0.90, 20), (0.80, 15), (0.65, 10), (0.50, 5), (0.0, 0)]

# Freshness is a ratio of observed p95 lag to expected latency; lower is better.
FRESHNESS = [(1.0, 20), (2.0, 15), (5.0, 10), (float("inf"), 5)]


def band(value: float, table: list[tuple[float, int]]) -> int:
    for threshold, points in table:
        if value >= threshold:
            return points
    return 0


def freshness_points(ratio: float | None, stale_30d: bool = False) -> int:
    if stale_30d:
        return 0
    if ratio is None:
        return 0
    for threshold, points in FRESHNESS:
        if ratio <= threshold:
            return points
    return 0


def score_family(f: dict) -> dict:
    """Score one family. Unmeasured dimensions score 0 and are named, never estimated."""
    unmeasured = []

    def get(key):
        v = f.get(key)
        if v is None:
            unmeasured.append(key)
        return v

    presence_raw = f.get("presence")
    if presence_raw is None:
        unmeasured.append("presence")
        presence = 0
    else:
        presence = PRESENCE.get(str(presence_raw).lower(), 0)

    ac = get("account_coverage")
    fc = get("field_completeness")
    fd = get("fidelity")
    fr = f.get("freshness_ratio")
    if fr is None and not f.get("no_write_30d"):
        unmeasured.append("freshness_ratio")

    dims = {
        "presence": presence,
        "account_coverage": band(ac, ACCOUNT_COVERAGE) if ac is not None else 0,
        "field_completeness": band(fc, FIELD_COMPLETENESS) if fc is not None else 0,
        "freshness": freshness_points(fr, bool(f.get("no_write_30d"))),
        "fidelity": band(fd, FIDELITY) if fd is not None else 0,
    }
    total = sum(dims.values())
    if total >= 80:
        status, weight = "COMPLETE", 1.0
    elif total >= 40:
        status, weight = "PARTIAL", 0.5
    else:
        status, weight = "MISSING", 0.0
    return {
        "dimensions": dims,
        "score": total,
        "status": status,
        "weight": weight,
        "unmeasured": unmeasured,
    }


def confidence_cap(coverage_pct: float) -> str:
    if coverage_pct >= 0.80:
        return "High"
    if coverage_pct >= 0.60:
        return "Medium"
    if coverage_pct >= 0.40:
        return "Low"
    return "Insufficient"


def score_coverage(families: dict) -> dict:
    scored, missing_input = {}, []
    for name in FAMILIES:
        f = families.get(name)
        if f is None:
            missing_input.append(name)
            f = {}
        scored[name] = score_family(f)
    coverage = sum(s["weight"] for s in scored.values()) / len(FAMILIES)
    return {
        "families": scored,
        "coverage_weighted": round(coverage, 4),
        "coverage_pct": round(coverage * 100, 1),
        "confidence_cap": confidence_cap(coverage),
        "families_not_supplied": missing_input,
    }


# --- Remediation ranking -------------------------------------------------------------------

DEGRADATION = {"blocks": 1.0, "caps": 0.6, "noise": 0.3}


def rank_remediation(items: list[dict]) -> list[dict]:
    out = []
    for i, it in enumerate(items):
        b = float(it["blast_radius_arr"])
        d_raw = it["degradation"]
        d = DEGRADATION[d_raw] if isinstance(d_raw, str) else float(d_raw)
        u = min(int(it.get("unlocks", 0)), 5)
        c = 1.5 if it.get("irreversible") else 1.0
        e = float(it["effort_days"])
        if e <= 0:
            raise ValueError(f"item {it.get('gap', i)}: effort_days must be > 0")
        priority = b * d * (1 + 0.1 * u) * c / e
        row = dict(it)
        row.update({
            "D": d, "U": u, "C": c,
            "priority": priority,
            "priority_2sf": two_sig_figs(priority),
            "workings": f"{b:,.0f} x {d} x (1 + 0.1*{u}) x {c} / {e} = {priority:,.0f}",
        })
        out.append(row)
    # Irreversible first within a tie band, then priority: an event not emitted today is
    # history that cannot be backfilled, whatever its blast radius.
    out.sort(key=lambda r: (-r["C"], -r["priority"]))
    for rank, row in enumerate(out, 1):
        row["rank"] = rank
    return out


def two_sig_figs(x: float) -> float:
    if x == 0:
        return 0.0
    return round(x, -int(math.floor(math.log10(abs(x)))) + 1)


# --- Document-test confidence interval ----------------------------------------------------

def wilson_ci(p_hat: float, n: int, z: float = 1.96) -> tuple[float, float, float]:
    """Wilson score interval — behaves at the extremes where the normal approximation does not."""
    if n <= 0:
        raise ValueError("n must be > 0")
    denom = 1 + z * z / n
    centre = (p_hat + z * z / (2 * n)) / denom
    half = z * math.sqrt(p_hat * (1 - p_hat) / n + z * z / (4 * n * n)) / denom
    return max(0.0, centre - half), min(1.0, centre + half), half


def normal_half_width(p_hat: float, n: int, z: float = 1.96) -> float:
    return z * math.sqrt(p_hat * (1 - p_hat) / n)


# --- Rendering -----------------------------------------------------------------------------

STATUS_MARK = {"COMPLETE": "[complete]", "PARTIAL": "[partial]", "MISSING": "[missing]"}


def render(result: dict) -> str:
    L = []
    cov = result["coverage"]
    L.append("COVERAGE SCORING")
    L.append("family                      pres acct comp fresh fid  score  status")
    for name in FAMILIES:
        s = cov["families"][name]
        d = s["dimensions"]
        L.append(
            f"{FAMILY_LABEL[name]:<27} {d['presence']:>4} {d['account_coverage']:>4} "
            f"{d['field_completeness']:>4} {d['freshness']:>5} {d['fidelity']:>3} "
            f"{s['score']:>6}  {STATUS_MARK[s['status']]}"
        )
    L.append("")
    L.append(f"Coverage: {cov['coverage_weighted'] * 7:.1f} / 7 families "
             f"({cov['coverage_pct']}%) -> downstream confidence capped at "
             f"{cov['confidence_cap']}")
    if cov["confidence_cap"] == "Insufficient":
        L.append("Under 40% coverage: name the gap, do not publish a grade (R23).")
    for name in FAMILIES:
        un = cov["families"][name]["unmeasured"]
        if un:
            L.append(f"  UNKNOWN — {FAMILY_LABEL[name]}: not measured: {', '.join(un)} "
                     f"(scored 0, not estimated)")

    if result.get("remediation"):
        L.append("")
        L.append("REMEDIATION RANKING  —  B x D x (1 + 0.1U) x C / E")
        L.append("Irreversible items rank ahead of higher-priority reversible ones: an event")
        L.append("not emitted today is history no later fix can recover. Priority is therefore")
        L.append("not monotonic down this list, and the report must say so.")
        L.append("rank  priority   irrev  gap")
        for r in result["remediation"]:
            L.append(f"{r['rank']:>4}  {r['priority_2sf']:>9,.0f}  "
                     f"{'yes' if r['C'] == 1.5 else '  -'}    {r['gap']}")
            L.append(f"        {r['workings']}")
        first = result["remediation"][0]
        L.append("")
        L.append(f"Fund first: {first['gap']} — {first['effort_days']} days"
                 + (f", owner {first['owner']}" if first.get("owner") else ""))

    if result.get("document_tests"):
        L.append("")
        L.append("DOCUMENT-TEST ACCURACY (95% CI, Wilson)")
        for t in result["document_tests"]:
            lo, hi = t["ci"]
            L.append(f"  {t['field']:<32} {t['accuracy']:.0%}  n={t['n']:<4} "
                     f"[{lo:.0%}, {hi:.0%}]  +/-{t['normal_half_width'] * 100:.1f}pp")
    return "\n".join(L)


def run(payload: dict) -> dict:
    result = {"coverage": score_coverage(payload.get("families", {}))}
    if payload.get("remediation"):
        result["remediation"] = rank_remediation(payload["remediation"])
    tests = []
    for t in payload.get("document_tests", []):
        n, matches = int(t["n"]), int(t["matches"])
        p = matches / n if n else 0.0
        lo, hi, half = wilson_ci(p, n)
        tests.append({
            "field": t["field"], "n": n, "matches": matches, "accuracy": p,
            "ci": (lo, hi), "wilson_half_width": half,
            "normal_half_width": normal_half_width(p, n),
        })
    if tests:
        result["document_tests"] = tests
    return result


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("input", nargs="?", help="audit measurements JSON")
    ap.add_argument("--json", action="store_true", help="emit JSON instead of a table")
    ap.add_argument("--ci", nargs=2, metavar=("ACCURACY", "N"),
                    help="just compute a 95%% CI for an observed accuracy and sample size")
    args = ap.parse_args()

    if args.ci:
        p, n = float(args.ci[0]), int(args.ci[1])
        lo, hi, half = wilson_ci(p, n)
        print(f"accuracy {p:.1%}  n={n}")
        print(f"  Wilson 95% CI  [{lo:.1%}, {hi:.1%}]  (+/-{half * 100:.1f}pp)")
        print(f"  normal approx  +/-{normal_half_width(p, n) * 100:.1f}pp")
        print(f"  worst case p=0.5 at this n: +/-{normal_half_width(0.5, n) * 100:.1f}pp")
        return 0

    if not args.input:
        ap.error("give an input JSON file, or use --ci")

    path = Path(args.input)
    if not path.is_absolute():
        candidate = Path(__file__).resolve().parent / path
        if candidate.exists():
            path = candidate
    payload = json.loads(path.read_text())
    result = run(payload)
    print(json.dumps(result, indent=2) if args.json else render(result))
    return 0


if __name__ == "__main__":
    sys.exit(main())
