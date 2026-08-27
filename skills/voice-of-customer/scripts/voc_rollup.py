#!/usr/bin/env python3
"""voc_rollup.py — deterministic Voice-of-Customer roll-up.

Takes a coded mention corpus plus an account register and emits the markdown blocks the
voice-of-customer skill needs: representativeness, Silent ARR, the theme register with ARR
attribution and splits, the emergence screen, and the priority ranking with arithmetic shown.

Standard library only. No network. Every figure is computed; nothing is estimated.

Usage
-----
    python3 voc_rollup.py input.json [--as-of YYYY-MM-DD] [--window-days 120]
    python3 voc_rollup.py --self-test          # runs the built-in sample and prints the report

Input schema (JSON)
-------------------
{
  "as_of": "2026-08-27",                     # optional; --as-of overrides
  "exposure_window_days": 120,               # optional, default 120
  "taxonomy_version": "2.1",
  "accounts": [
    {"account_id": "a1", "name": "Acme Corp", "arr": 480000, "segment": "ENT",
     "health_band": "at_risk",               # secure|watch|at_risk|high|critical
     "renewal_date": "2027-01-12", "notice_period_days": 90,
     "is_internal": false}
  ],
  "mentions": [
    {"account_id": "a1", "theme": "INT-02", "theme_name": "Integration unreliable",
     "category": "INT", "channel": "ticket", "severity": 2, "period": "current",
     "contact_role": "admin", "is_primary": true}
  ],
  "themes": {                                # optional per-theme metadata
    "INT-02": {"tractability": "quarter"}    # quarter|year|structural
  },
  "invitations": [                           # optional; drives response-rate table
    {"channel": "nps", "invited": 412, "responded": 63, "accounts_responded": 41,
     "role_mix": "power_user 61%, admin 27%, economic_buyer 12%"}
  ]
}

Notes on method
---------------
* ARR attribution is at ACCOUNT grain, primary codes only. An account counts once per theme.
* Band midpoints are the rules-based midpoints from churn-risk. They are STATED probabilities
  of a rules-based model, not calibrated forecasts, and the report says so.
* The two-proportion z is a screening heuristic on dependent, non-random samples. It is not a
  significance test and the report labels it as a screen.
* Anything not computable is printed as `UNKNOWN — requires ...`, never filled with a default.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from collections import defaultdict
from datetime import date, timedelta

# --- constants ---------------------------------------------------------------------------

BAND_MIDPOINT = {          # churn-risk band midpoints; rules-based, not calibrated
    "secure": 0.05,
    "watch": 0.15,
    "at_risk": 0.35,
    "high": 0.60,
    "critical": 0.85,
}

TRACTABILITY = {"quarter": 1.2, "year": 1.0, "structural": 0.5}

TRAJECTORY_FACTOR = {
    "emerged": 1.4,
    "growing": 1.2,
    "flat": 1.0,
    "fading": 0.8,
    "newly visible": 1.0,
}

MIN_MENTIONS = 5           # emergence: minimum current-period mentions
MIN_ACCOUNTS = 3           # emergence: minimum distinct accounts
REL_SHARE_GATE = 0.50      # emergence: relative share increase
ABS_SHARE_GATE = 0.02      # emergence: absolute share-point increase
Z_GATE = 2.0               # emergence: two-proportion screen


# --- helpers -----------------------------------------------------------------------------


def money(x: float) -> str:
    return f"${x:,.0f}"


def pct(x: float, digits: int = 1) -> str:
    return f"{x * 100:.{digits}f}%"


def parse_date(s):
    if not s:
        return None
    y, m, d = (int(p) for p in s.split("-"))
    return date(y, m, d)


def opt_out_deadline(account) -> date | None:
    """renewal_date - notice_period_days. The date that actually governs the decision."""
    rd = parse_date(account.get("renewal_date"))
    if rd is None:
        return None
    notice = account.get("notice_period_days")
    if notice is None:
        return None
    return rd - timedelta(days=int(notice))


def two_proportion_z(x1: int, n1: int, x2: int, n2: int) -> float | None:
    """Screening statistic only. Samples are dependent and non-random; this ranks
    candidates for attention, it does not license the word 'significant'."""
    if n1 <= 0 or n2 <= 0:
        return None
    p1, p2 = x1 / n1, x2 / n2
    p_pool = (x1 + x2) / (n1 + n2)
    denom = p_pool * (1 - p_pool) * (1 / n1 + 1 / n2)
    if denom <= 0:
        return None
    return (p1 - p2) / math.sqrt(denom)


def classify(cur_m, prior_m, cur_share, prior_share, z, cur_accounts) -> str:
    if cur_m >= MIN_MENTIONS and prior_m < 3:
        return "emerged"
    rel = (cur_share / prior_share - 1) if prior_share > 0 else float("inf")
    absd = cur_share - prior_share
    if (
        cur_m >= MIN_MENTIONS
        and cur_accounts >= MIN_ACCOUNTS
        and rel >= REL_SHARE_GATE
        and absd >= ABS_SHARE_GATE
        and z is not None
        and z >= Z_GATE
    ):
        return "growing"
    if prior_m >= MIN_MENTIONS and rel <= -0.35:
        return "fading"
    return "flat"


# --- core --------------------------------------------------------------------------------


def build(data: dict, as_of: date, window_days: int) -> dict:
    accounts = {
        a["account_id"]: a for a in data.get("accounts", []) if not a.get("is_internal", False)
    }
    internal_excluded = len(data.get("accounts", [])) - len(accounts)
    theme_meta = data.get("themes", {})

    in_scope_arr = sum(float(a.get("arr", 0)) for a in accounts.values())

    mentions = [m for m in data.get("mentions", []) if m.get("is_primary", True)]
    unattributed = [m for m in mentions if m.get("account_id") not in accounts]
    mentions = [m for m in mentions if m.get("account_id") in accounts]

    cur = [m for m in mentions if m.get("period", "current") == "current"]
    prior = [m for m in mentions if m.get("period") == "prior"]
    n_cur, n_prior = len(cur), len(prior)

    # --- per-theme roll-up ---
    themes = {}
    for m in cur + prior:
        code = m["theme"]
        t = themes.setdefault(
            code,
            {
                "code": code,
                "name": m.get("theme_name", code),
                "category": m.get("category", code.split("-")[0]),
                "cur_mentions": 0,
                "prior_mentions": 0,
                "cur_accounts": set(),
                "prior_accounts": set(),
                "severities": [],
                "channels": set(),
                "buyer_mentions": 0,
            },
        )
        if m.get("period", "current") == "current":
            t["cur_mentions"] += 1
            t["cur_accounts"].add(m["account_id"])
            if m.get("severity") is not None:
                t["severities"].append(int(m["severity"]))
            t["channels"].add(m.get("channel", "unknown"))
            if m.get("contact_role") == "economic_buyer":
                t["buyer_mentions"] += 1
        else:
            t["prior_mentions"] += 1
            t["prior_accounts"].add(m["account_id"])

    horizon = as_of + timedelta(days=window_days)

    for t in themes.values():
        accs = [accounts[a] for a in t["cur_accounts"]]
        t["attributed_arr"] = sum(float(a.get("arr", 0)) for a in accs)

        rw, missing_band = 0.0, 0
        for a in accs:
            band = (a.get("health_band") or "").lower()
            if band in BAND_MIDPOINT:
                rw += float(a.get("arr", 0)) * BAND_MIDPOINT[band]
            else:
                missing_band += 1
        t["risk_weighted_arr"] = rw
        t["missing_band"] = missing_band

        seg = defaultdict(float)
        band_split = defaultdict(float)
        exposure, exposure_accounts, missing_optout = 0.0, [], 0
        for a in accs:
            seg[a.get("segment", "UNKNOWN")] += float(a.get("arr", 0))
            band_split[(a.get("health_band") or "unknown").lower()] += float(a.get("arr", 0))
            ood = opt_out_deadline(a)
            if ood is None:
                missing_optout += 1
            elif ood <= horizon:
                exposure += float(a.get("arr", 0))
                exposure_accounts.append((a.get("name", a["account_id"]), ood))
        t["segment_split"] = dict(seg)
        t["band_split"] = dict(band_split)
        t["exposure"] = exposure
        t["exposure_accounts"] = sorted(exposure_accounts, key=lambda r: r[1])
        t["missing_optout"] = missing_optout

        t["mean_severity"] = (
            sum(t["severities"]) / len(t["severities"]) if t["severities"] else None
        )
        t["cur_share"] = t["cur_mentions"] / n_cur if n_cur else 0.0
        t["prior_share"] = t["prior_mentions"] / n_prior if n_prior else 0.0
        t["z"] = two_proportion_z(
            t["cur_mentions"], n_cur, t["prior_mentions"], n_prior
        ) if (n_cur and n_prior) else None
        t["status"] = (
            classify(
                t["cur_mentions"],
                t["prior_mentions"],
                t["cur_share"],
                t["prior_share"],
                t["z"],
                len(t["cur_accounts"]),
            )
            if n_prior
            else "baseline"
        )

        t["intensity"] = (t["mean_severity"] / 2) if t["mean_severity"] is not None else None
        t["trajectory"] = TRAJECTORY_FACTOR.get(t["status"], 1.0)
        tract_key = theme_meta.get(t["code"], {}).get("tractability")
        t["tractability_key"] = tract_key
        t["tractability"] = TRACTABILITY.get(tract_key) if tract_key else None
        if t["intensity"] is None or t["tractability"] is None:
            t["priority"] = None
        else:
            t["priority"] = (
                t["risk_weighted_arr"] * t["intensity"] * t["trajectory"] * t["tractability"]
            )

    ranked = sorted(
        themes.values(),
        key=lambda t: (t["priority"] is not None, t["priority"] or 0),
        reverse=True,
    )

    # --- representativeness ---
    heard = {m["account_id"] for m in cur}
    heard_arr = sum(float(accounts[a].get("arr", 0)) for a in heard)

    silent = defaultdict(lambda: {"accounts": 0, "arr": 0.0, "renewals": 0, "renewal_arr": 0.0})
    for aid, a in accounts.items():
        if aid in heard:
            continue
        row = silent[a.get("segment", "UNKNOWN")]
        row["accounts"] += 1
        row["arr"] += float(a.get("arr", 0))
        ood = opt_out_deadline(a)
        if ood is not None and ood <= horizon:
            row["renewals"] += 1
            row["renewal_arr"] += float(a.get("arr", 0))

    seg_arr = defaultdict(float)
    for a in accounts.values():
        seg_arr[a.get("segment", "UNKNOWN")] += float(a.get("arr", 0))

    return {
        "as_of": as_of,
        "window_days": window_days,
        "accounts": accounts,
        "internal_excluded": internal_excluded,
        "in_scope_arr": in_scope_arr,
        "n_cur": n_cur,
        "n_prior": n_prior,
        "unattributed": unattributed,
        "themes": ranked,
        "heard": heard,
        "heard_arr": heard_arr,
        "silent": silent,
        "seg_arr": seg_arr,
        "invitations": data.get("invitations", []),
        "taxonomy_version": data.get("taxonomy_version"),
    }


# --- rendering ---------------------------------------------------------------------------


def render(r: dict) -> str:
    out = []
    w = out.append
    in_scope = r["in_scope_arr"]
    cov = (r["heard_arr"] / in_scope) if in_scope else 0.0

    w(f"## VoC Roll-up — as of {r['as_of']} · exposure window {r['window_days']}d")
    w(f"Taxonomy version: {r['taxonomy_version'] or '`UNKNOWN — requires taxonomy version`'}")
    w("")

    # 1. representativeness
    w("### 1. Who spoke")
    w("")
    w("| Metric | Value |")
    w("|---|---|")
    w(f"| Accounts in scope | {len(r['accounts'])} ({money(in_scope)} ARR) |")
    w(f"| Internal accounts excluded | {r['internal_excluded']} |")
    w(f"| Accounts heard from this period | {len(r['heard'])} |")
    w(f"| ARR represented | {money(r['heard_arr'])} ({pct(cov)} of in-scope ARR) |")
    w(f"| Coded mentions — current / prior | {r['n_cur']} / {r['n_prior']} |")
    unattr = len(r["unattributed"])
    total_m = r["n_cur"] + r["n_prior"] + unattr
    w(
        f"| Unattributed mentions | {unattr}"
        + (f" ({pct(unattr / total_m)} of all mentions)" if total_m else "")
        + " |"
    )
    w("")
    if cov < 0.50:
        w(
            f"> **Sentiment ARR coverage is {pct(cov)}, below the ~50% practitioner floor `[P]`.** "
            "Treat the theme register as evidence about the accounts that spoke, not as a "
            "measurement of the base. Cap confidence accordingly."
        )
    else:
        w(f"> Sentiment ARR coverage {pct(cov)}. State it in the readout Bottom Line block.")
    w("")

    if r["invitations"]:
        w("| Channel | Invited | Responded | Response rate | Accounts | Role mix |")
        w("|---|---|---|---|---|---|")
        for i in r["invitations"]:
            inv, resp = i.get("invited"), i.get("responded")
            rate = pct(resp / inv) if inv else "`UNKNOWN — requires invited count`"
            w(
                f"| {i.get('channel','?')} | {inv if inv is not None else 'UNKNOWN'} | "
                f"{resp if resp is not None else 'UNKNOWN'} | {rate} | "
                f"{i.get('accounts_responded','UNKNOWN')} | {i.get('role_mix','UNKNOWN — requires role mix')} |"
            )
        w("")
    else:
        w("Response rates: `UNKNOWN — requires invitation counts per channel`.")
        w("")

    # 2. silent ARR
    w("### 2. Silent ARR — no coded feedback this period")
    w("")
    w("| Segment | Accounts | ARR | % of segment ARR | Opt-out ≤window | ARR at those renewals |")
    w("|---|---|---|---|---|---|")
    tot = {"a": 0, "arr": 0.0, "r": 0, "rarr": 0.0}
    for seg in sorted(r["silent"], key=lambda s: -r["silent"][s]["arr"]):
        row = r["silent"][seg]
        denom = r["seg_arr"].get(seg, 0.0)
        share = pct(row["arr"] / denom) if denom else "n/a"
        w(
            f"| {seg} | {row['accounts']} | {money(row['arr'])} | {share} | "
            f"{row['renewals']} | {money(row['renewal_arr'])} |"
        )
        tot["a"] += row["accounts"]
        tot["arr"] += row["arr"]
        tot["r"] += row["renewals"]
        tot["rarr"] += row["renewal_arr"]
    w(
        f"| **Total** | **{tot['a']}** | **{money(tot['arr'])}** | "
        f"**{pct(tot['arr'] / in_scope) if in_scope else 'n/a'}** | "
        f"**{tot['r']}** | **{money(tot['rarr'])}** |"
    )
    w("")

    # 3. theme register
    w("### 3. Theme register")
    w("")
    w(
        "| # | Theme | Cat | Accts | Mentions cur/prior | Share cur/prior | Attributed ARR | "
        "Risk-wtd ARR | Exposure ≤window | Mean sev | Status | z | Tract. | Priority |"
    )
    w("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
    for i, t in enumerate(r["themes"], 1):
        z = f"{t['z']:+.2f}" if t["z"] is not None else "n/a"
        sev = f"{t['mean_severity']:.2f}" if t["mean_severity"] is not None else "UNKNOWN"
        tract = t["tractability_key"] or "UNKNOWN"
        prio = money(t["priority"]) if t["priority"] is not None else "UNKNOWN"
        w(
            f"| {i} | {t['code']} {t['name']} | {t['category']} | {len(t['cur_accounts'])} | "
            f"{t['cur_mentions']}/{t['prior_mentions']} | "
            f"{pct(t['cur_share'])}/{pct(t['prior_share'])} | {money(t['attributed_arr'])} | "
            f"{money(t['risk_weighted_arr'])} | {money(t['exposure'])} | {sev} | "
            f"{t['status']} | {z} | {tract} | {prio} |"
        )
    w("")
    w(
        "Attributed ARR = revenue of accounts raising the theme (account grain, primary codes "
        "only). It is **not** revenue at risk. Risk-weighted ARR uses churn-risk band midpoints "
        "(secure .05 · watch .15 · at_risk .35 · high .60 · critical .85) — stated probabilities "
        "of a rules-based model, **not calibrated forecasts**. `z` is a screening heuristic on "
        "dependent, non-random samples, **not a significance test**."
    )
    w("")

    # 4. arithmetic
    w("### 4. Priority arithmetic")
    w("")
    for t in r["themes"]:
        if t["priority"] is None:
            missing = []
            if t["intensity"] is None:
                missing.append("severity codes")
            if t["tractability"] is None:
                missing.append("tractability (quarter|year|structural)")
            w(f"- **{t['code']}** — priority `UNKNOWN — requires {', '.join(missing)}`")
            continue
        w(
            f"- **{t['code']}** — {money(t['risk_weighted_arr'])} × intensity "
            f"{t['intensity']:.2f} × trajectory {t['trajectory']:.1f} ({t['status']}) × "
            f"tractability {t['tractability']:.1f} ({t['tractability_key']}) = "
            f"**{money(t['priority'])}**"
        )
    w("")

    # 5. splits + exposure
    w("### 5. Splits and renewal exposure")
    w("")
    for t in r["themes"]:
        seg = " · ".join(
            f"{k} {money(v)}" for k, v in sorted(t["segment_split"].items(), key=lambda kv: -kv[1])
        ) or "none"
        band = " · ".join(
            f"{k} {money(v)}" for k, v in sorted(t["band_split"].items(), key=lambda kv: -kv[1])
        ) or "none"
        w(f"**{t['code']} {t['name']}**")
        w(f"- Segment split: {seg}")
        w(f"- Health band split: {band}")
        w(f"- Channels represented: {len(t['channels'])} ({', '.join(sorted(t['channels']))})")
        w(f"- Economic-buyer mentions: {t['buyer_mentions']}")
        if t["exposure_accounts"]:
            names = ", ".join(f"{n} (opt-out {d})" for n, d in t["exposure_accounts"])
            w(f"- Opt-out inside {r['window_days']}d: {money(t['exposure'])} — {names}")
        else:
            w(f"- Opt-out inside {r['window_days']}d: none")
        if t["missing_optout"]:
            w(
                f"- `UNKNOWN — requires renewal_date and notice_period_days` for "
                f"{t['missing_optout']} account(s); exposure is a floor"
            )
        if t["missing_band"]:
            w(
                f"- `UNKNOWN — requires health_band` for {t['missing_band']} account(s); "
                "risk-weighted ARR is a floor"
            )
        w("")

    if r["unattributed"]:
        w(
            f"> {len(r['unattributed'])} mention(s) could not be resolved to an in-scope account "
            "and carry no ARR. All dollar figures above are a floor."
        )
        w("")

    return "\n".join(out)


# --- sample ------------------------------------------------------------------------------

SAMPLE = {
    "as_of": "2026-08-27",
    "exposure_window_days": 120,
    "taxonomy_version": "2.1",
    "accounts": [
        {"account_id": "a1", "name": "Acme Corp", "arr": 480000, "segment": "ENT",
         "health_band": "at_risk", "renewal_date": "2027-01-12", "notice_period_days": 90},
        {"account_id": "a2", "name": "Northwind", "arr": 310000, "segment": "ENT",
         "health_band": "watch", "renewal_date": "2027-05-02", "notice_period_days": 90},
        {"account_id": "a3", "name": "Brightline", "arr": 92000, "segment": "MM",
         "health_band": "high", "renewal_date": "2026-11-29", "notice_period_days": 60},
        {"account_id": "a4", "name": "Vector Labs", "arr": 74000, "segment": "MM",
         "health_band": "secure", "renewal_date": "2027-06-19", "notice_period_days": 30},
        {"account_id": "a5", "name": "Pellet.io", "arr": 18000, "segment": "SMB",
         "health_band": "at_risk", "renewal_date": "2026-12-02", "notice_period_days": 30},
        {"account_id": "a6", "name": "Halcyon Group", "arr": 265000, "segment": "ENT",
         "health_band": "watch", "renewal_date": "2026-11-15", "notice_period_days": 60},
        {"account_id": "a7", "name": "Ridgeway", "arr": 41000, "segment": "MM",
         "health_band": "secure", "renewal_date": "2027-03-01", "notice_period_days": 30},
        {"account_id": "a9", "name": "Internal Sandbox", "arr": 0, "segment": "ENT",
         "health_band": "secure", "renewal_date": "2027-01-01", "notice_period_days": 30,
         "is_internal": True},
    ],
    "themes": {
        "INT-02": {"tractability": "quarter"},
        "CAP-01": {"tractability": "structural"},
        "SUP-02": {"tractability": "quarter"},
        "ONB-03": {"tractability": "year"},
    },
    "invitations": [
        {"channel": "nps", "invited": 412, "responded": 63, "accounts_responded": 41,
         "role_mix": "power_user 61%, admin 27%, economic_buyer 12%"},
        {"channel": "csat", "invited": 268, "responded": 97, "accounts_responded": 55,
         "role_mix": "user 74%, admin 26%"},
    ],
    "mentions": (
        # INT-02 current: 5 accounts, 6 mentions
        [{"account_id": a, "theme": "INT-02", "theme_name": "Integration unreliable",
          "category": "INT", "channel": c, "severity": s, "period": "current",
          "contact_role": role, "is_primary": True}
         for a, c, s, role in [
             ("a1", "ticket", 3, "admin"), ("a2", "call", 2, "economic_buyer"),
             ("a3", "ticket", 3, "admin"), ("a4", "nps", 2, "power_user"),
             ("a5", "email", 2, "admin"), ("a1", "call", 2, "economic_buyer")]]
        # CAP-01 current
        + [{"account_id": a, "theme": "CAP-01", "theme_name": "Missing capability on value path",
            "category": "CAP", "channel": c, "severity": s, "period": "current",
            "contact_role": role, "is_primary": True}
           for a, c, s, role in [
               ("a2", "call", 3, "economic_buyer"), ("a6", "call", 3, "economic_buyer"),
               ("a7", "community", 2, "power_user")]]
        # SUP-02 current
        + [{"account_id": a, "theme": "SUP-02", "theme_name": "Resolution quality",
            "category": "SUP", "channel": c, "severity": s, "period": "current",
            "contact_role": role, "is_primary": True}
           for a, c, s, role in [
               ("a3", "csat", 2, "user"), ("a6", "ticket", 2, "admin"),
               ("a1", "ticket", 2, "admin"), ("a5", "csat", 3, "user"),
               ("a7", "ticket", 2, "user")]]
        # ONB-03 current
        + [{"account_id": a, "theme": "ONB-03", "theme_name": "Training and enablement gap",
            "category": "ONB", "channel": "nps", "severity": 1, "period": "current",
            "contact_role": "power_user", "is_primary": True} for a in ["a4", "a7"]]
        # prior period
        + [{"account_id": a, "theme": t, "theme_name": n, "category": t.split("-")[0],
            "channel": "ticket", "severity": 2, "period": "prior",
            "contact_role": "admin", "is_primary": True}
           for a, t, n in [
               ("a1", "INT-02", "Integration unreliable"),
               ("a3", "INT-02", "Integration unreliable"),
               ("a2", "CAP-01", "Missing capability on value path"),
               ("a6", "CAP-01", "Missing capability on value path"),
               ("a7", "CAP-01", "Missing capability on value path"),
               ("a4", "ONB-03", "Training and enablement gap"),
               ("a5", "ONB-03", "Training and enablement gap"),
               ("a7", "ONB-03", "Training and enablement gap"),
               ("a1", "ONB-03", "Training and enablement gap"),
               ("a6", "ONB-03", "Training and enablement gap"),
               ("a3", "ONB-03", "Training and enablement gap")]]
        # unattributable (anonymous review, no account in scope)
        + [{"account_id": "zz-unknown", "theme": "REP-01", "theme_name": "Standard reporting gaps",
            "category": "REP", "channel": "review", "severity": 2, "period": "current",
            "contact_role": None, "is_primary": True}]
    ),
}


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description="Deterministic Voice-of-Customer roll-up.")
    p.add_argument("input", nargs="?", help="Path to the input JSON file")
    p.add_argument("--as-of", help="Override as-of date (YYYY-MM-DD)")
    p.add_argument("--window-days", type=int, help="Renewal exposure window (default 120)")
    p.add_argument("--self-test", action="store_true", help="Run the built-in sample")
    args = p.parse_args(argv)

    if args.self_test:
        data = SAMPLE
    elif args.input:
        with open(args.input, "r", encoding="utf-8") as fh:
            data = json.load(fh)
    else:
        p.error("provide an input file or --self-test")
        return 2

    as_of = parse_date(args.as_of or data.get("as_of")) or date.today()
    window = args.window_days or int(data.get("exposure_window_days", 120))
    print(render(build(data, as_of, window)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
