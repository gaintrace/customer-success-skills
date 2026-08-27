#!/usr/bin/env python3
"""
Deterministic stakeholder scoring for the `stakeholder-map` skill.

Why a script: relationship arithmetic is small, repetitive and easy to get subtly wrong in
prose — a strength score renormalised over four dimensions when one is null, a coverage score
over four roles with a staleness rule, an exposure figure that multiplies three factors. Done
by hand across a book of accounts it drifts. This produces the same number every time and
shows every step, so a reviewer can disagree with the model rather than with the arithmetic.

Usage
-----
    python3 stakeholder_score.py sample-account.json
    python3 stakeholder_score.py sample-account.json --today 2026-08-28
    python3 stakeholder_score.py sample-account.json --explain NORTHWIND
    python3 stakeholder_score.py sample-account.json --horizon 180

Input: JSON — a single account object or a list of them. Missing values must be `null`, never
0: `null` means "not measured" and is renormalised out, 0 means "measured, and it is zero".
See sample-account.json for the full shape.

Three structural checks run on every account and print as refusals, not as advice:

  C7  authority triangle — `signs` / `decides` / `influences` are resolved separately from
      account["authority"] (falling back to is_signatory / economic_buyer / is_influencer).
      Two of three on one contact prints CONCENTRATION 2/3; three of three floors the
      structural multiplier at 1.00 whatever the depth. `signs` UNKNOWN with the opt-out
      deadline inside 120 days caps coverage_score at 2.0/4 and forces the signatory trace.

  C8  mobilising capacity — m1_moved_decision / m2_others_cite / m3_controls_budget. A contact
      labelled `champion` with mobilising < 2, or with advocacy_events 0, is reclassified
      coach + is_supporter and scores 0.0 on the champion coverage slot, exactly as an empty
      slot does. Untested (no M fields) is UNKNOWN and still forbids the champion label.

  C11 blocker dispositions — every negative or hostile contact needs disposition ∈
      {convert, contain, bypass} plus a non-empty disposition_risk. `bypass` against a
      veto-holder is refused and falls back to contain. A missing disposition inside the
      renewal window is an invalid row, and the fix is find_out + disposition_owner +
      disposition_by, not a blank cell.

Model constants mirror SKILL.md Steps 2, 3, 5, 6 and 7, references/champion-risk.md §4–5,
references/role-taxonomy.md §3A–3B and references/coverage-plays.md §4.0.
Change them together or the artifact and the script will disagree.

No network access. Standard library only.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date, datetime, timedelta

# ----------------------------------------------------------------------------------------
# Model constants
# ----------------------------------------------------------------------------------------

STRENGTH_WEIGHTS = {"influence": 0.30, "sentiment": 0.25, "recency": 0.25, "depth": 0.20}

SENTIMENT_VALUES = {"hostile": -2, "negative": -1, "neutral": 0, "positive": 1, "advocate": 2}
SENTIMENT_STALE_DAYS = 90          # evidence-standard.md §7 — survey/VoC decay

SENIORITY_ORDER = ["ic", "manager", "director", "vp", "c_level"]

KEY_ROLES = ["economic_buyer", "champion", "technical_evaluator", "exec_sponsor"]

# C7 — the authority triangle. Three fields, never merged. SKILL.md Step 2.
TRIANGLE = ["signs", "decides", "influences"]
RENEWAL_WINDOW_DAYS = 120          # inside this, UNKNOWN stops being a permitted answer
SIGNS_UNKNOWN_COVERAGE_CAP = 2.0

# C8 — mobilising capacity. Champion is the OUTPUT of these tests, never an input to them.
MOBILISING_TESTS = [
    ("m1_moved_decision",   "M1 · has moved a decision through this org before"),
    ("m2_others_cite",      "M2 · others cite them"),
    ("m3_controls_budget",  "M3 · controls budget or headcount"),
]
CHAMPION_MIN_MOBILISING = 2

# C11 — blocker dispositions. There is no fourth value.
DISPOSITIONS = ("convert", "contain", "bypass")
VETO_FUNCTIONS = ("security", "legal", "procurement")
VETO_ROLES = ("procurement", "technical_evaluator")

# (upper ARR bound, targets). First band whose bound the ARR falls under wins.
ARR_BANDS = [
    (10_000,        {"depth": 1, "breadth": 1, "height": "ic",       "coverage": 1.0, "shape": "1 named admin"}),
    (50_000,        {"depth": 2, "breadth": 1, "height": "manager",  "coverage": 2.0, "shape": "1 champion + 1 backup"}),
    (150_000,       {"depth": 3, "breadth": 2, "height": "director", "coverage": 2.5, "shape": "1-1-2"}),
    (500_000,       {"depth": 5, "breadth": 3, "height": "vp",       "coverage": 3.0, "shape": "1-2-3"}),
    (float("inf"),  {"depth": 7, "breadth": 4, "height": "c_level",  "coverage": 3.5, "shape": "1-3-5"}),
]

# references/champion-risk.md §4
RISK_FACTORS = [
    ("hard_bounce_key_contact", 4, "Hard bounce on the champion or economic buyer"),
    ("single_threaded",         3, "Single-threaded — depth <=1 two-way in 90d"),
    ("no_advocacy_180d",        2, "No observed internal advocacy in 180d"),
    ("intro_to_eb_declined",    2, "Introduction to the economic buyer declined or deflected"),
    ("title_or_employer_change",2, "Title or employer change detected"),
    ("login_gap",               2, "Login gap >=3x their own median interval and >=14 days"),
    ("reorg_or_acquisition",    2, "Customer reorg, acquisition or budget-owner change"),
]
RISK_CAP = 10

# Exposure — SKILL.md Step 5. Sources: base departure rate UserGems 2026 [V];
# loss-given-departure Sturdy AI [V]; structural ladder is a design convention [P].
BASE_ANNUAL_DEPARTURE_RATE = 0.20
P_LOSS_GIVEN_DEPARTURE = 0.51
P_DEPARTURE_CAP = 0.95


def risk_multiplier(score: int) -> float:
    if score <= 3:
        return 0.75
    if score <= 5:
        return 1.5
    if score <= 7:
        return 2.5
    return 4.0


def structural_multiplier(depth: int, verified_eb: bool) -> float:
    if depth <= 1:
        return 1.00
    if depth == 2:
        return 0.60
    if depth <= 4:
        return 0.35
    return 0.20 if verified_eb else 0.35


# ----------------------------------------------------------------------------------------
# Helpers
# ----------------------------------------------------------------------------------------

def parse_date(value):
    if not value:
        return None
    return datetime.strptime(value, "%Y-%m-%d").date()


def days_since(value, today: date):
    d = parse_date(value)
    return None if d is None else (today - d).days


def band_for(arr: float) -> dict:
    for bound, targets in ARR_BANDS:
        if arr < bound:
            return targets
    return ARR_BANDS[-1][1]


def norm_influence(v):
    return None if v is None else (max(1, min(5, v)) - 1) / 4 * 100


def norm_sentiment(label, as_of_days):
    if label is None or label not in SENTIMENT_VALUES:
        return None
    if as_of_days is not None and as_of_days > SENTIMENT_STALE_DAYS:
        return None                      # stale sentiment is nulled, never carried forward
    return (SENTIMENT_VALUES[label] + 2) / 4 * 100


def norm_recency(days):
    if days is None:
        return 0.0
    for limit, score in ((30, 100.0), (60, 75.0), (90, 50.0), (180, 25.0)):
        if days <= limit:
            return score
    return 0.0


def norm_depth(interactions, channels):
    if interactions is None:
        return None
    if interactions >= 8 and (channels or 0) >= 2:
        return 100.0
    if interactions >= 4:
        return 75.0
    if interactions >= 2:
        return 50.0
    if interactions == 1:
        return 25.0
    return 0.0


def mobilising(contact):
    """C8 — 0..3 from evidence flags, or an explicit integer. None means untested, which is
    NOT the same as 0: untested still forbids the champion label, but it is reported as
    UNKNOWN rather than as a measured zero."""
    explicit = contact.get("mobilising_capacity")
    if isinstance(explicit, int):
        return max(0, min(3, explicit)), [l for k, l in MOBILISING_TESTS if contact.get(k)]
    fired = [l for k, l in MOBILISING_TESTS if contact.get(k)]
    if not any(k in contact for k, _ in MOBILISING_TESTS):
        return None, []
    return len(fired), fired


def classify(contact):
    """C8 — a high-sentiment contact who cannot mobilise is a supporter, not a champion, and
    a supporter satisfies the champion requirement nowhere. Returns (role, is_supporter)."""
    role = contact.get("role")
    if role != "champion":
        return role, bool(contact.get("is_supporter"))
    m, _ = mobilising(contact)
    advocacy = contact.get("advocacy_events")
    if m is None or m < CHAMPION_MIN_MOBILISING or (advocacy is not None and advocacy < 1):
        return "coach", True
    return "champion", False


def strength(contact, today: date):
    """Weighted 0-100, renormalised over the dimensions that have data."""
    two_way_days = days_since(contact.get("last_two_way"), today)
    parts = {
        "influence": norm_influence(contact.get("influence")),
        "sentiment": norm_sentiment(contact.get("sentiment"),
                                    days_since(contact.get("sentiment_as_of"), today)),
        "recency": norm_recency(two_way_days),
        "depth": norm_depth(contact.get("interactions_180d"), contact.get("channels_180d")),
    }
    available = {k: v for k, v in parts.items() if v is not None}
    if not available:
        return None, parts, two_way_days
    total_w = sum(STRENGTH_WEIGHTS[k] for k in available)
    value = sum(STRENGTH_WEIGHTS[k] * v for k, v in available.items()) / total_w
    return round(value, 1), parts, two_way_days


# ----------------------------------------------------------------------------------------
# Account-level measures
# ----------------------------------------------------------------------------------------

def measure(account: dict, today: date, horizon: int) -> dict:
    contacts = account.get("contacts", [])
    arr = float(account.get("arr") or 0)
    targets = band_for(arr)

    scored = []
    for c in contacts:
        value, parts, two_way_days = strength(c, today)
        eff_role, is_supporter = classify(c)
        m, m_fired = mobilising(c)
        scored.append({**c, "strength": value, "parts": parts, "two_way_days": two_way_days,
                       "effective_role": eff_role, "is_supporter": is_supporter,
                       "mobilising": m, "m_fired": m_fired,
                       "claimed_role": c.get("role")})

    two_way_90 = [c for c in scored if c["two_way_days"] is not None and c["two_way_days"] <= 90]
    two_way_180 = [c for c in scored if c["two_way_days"] is not None and c["two_way_days"] <= 180]

    depth = len(two_way_90)
    breadth = len({c.get("function") for c in two_way_90 if c.get("function")})
    ranks = [SENIORITY_ORDER.index(c["seniority"]) for c in two_way_180
             if c.get("seniority") in SENIORITY_ORDER]
    height = SENIORITY_ORDER[max(ranks)] if ranks else None

    # Coverage over the four key roles.
    coverage_detail = {}
    for role in KEY_ROLES:
        if role == "exec_sponsor":
            holders = [c for c in scored if c.get("is_exec_sponsor")]
        else:
            # C8: effective_role, not the claimed role. A supporter scores 0.0 here.
            holders = [c for c in scored if c["effective_role"] == role]
        if not holders:
            coverage_detail[role] = (0.0, "unfilled")
            continue
        best = 0.0
        note = "filled, stale or unverified"
        for c in holders:
            fresh = c["two_way_days"] is not None and c["two_way_days"] <= 90
            if c.get("role_confidence") == "verified" and fresh:
                best, note = 1.0, f"{c['name']} — verified, two-way {c['two_way_days']}d"
                break
            best = max(best, 0.5)
            note = f"{c['name']} — {c.get('role_confidence')}, two-way {c['two_way_days']}d"
        coverage_detail[role] = (best, note)
    if not [c for c in scored if c["effective_role"] == "champion"] and \
            [c for c in scored if c["is_supporter"]]:
        names = ", ".join(c["name"] for c in scored if c["is_supporter"])
        coverage_detail["champion"] = (0.0, f"supporter only ({names}) — scores 0.0 (C8)")
    coverage_raw = sum(v for v, _ in coverage_detail.values())

    # --- C7: the authority triangle ---------------------------------------------------
    by_id = {c.get("contact_id"): c for c in scored}
    declared = account.get("authority") or {}
    triangle = {}
    for field in TRIANGLE:
        cid = declared.get(field)
        holder = by_id.get(cid)
        if holder is None:
            fallback = {"signs": "is_signatory", "decides": None, "influences": "is_influencer"}
            flag = fallback.get(field)
            if flag:
                holder = next((c for c in scored if c.get(flag)), None)
            elif field == "decides":
                holder = next((c for c in scored
                               if c["effective_role"] == "economic_buyer"), None)
        triangle[field] = holder
    filled_ids = [h.get("contact_id") for h in triangle.values() if h]
    dupes = {i: filled_ids.count(i) for i in set(filled_ids)}
    concentration = max(dupes.values()) if dupes else 0
    concentrated_on = next((by_id[i]["name"] for i, n in dupes.items()
                            if n == concentration and n >= 2), None)

    renewal = parse_date(account.get("renewal_date"))
    notice = account.get("notice_period_days")
    opt_out = renewal - timedelta(days=notice) if renewal and notice is not None else None
    days_to_opt_out = (opt_out - today).days if opt_out else None
    in_window = days_to_opt_out is not None and days_to_opt_out <= RENEWAL_WINDOW_DAYS

    coverage = coverage_raw
    coverage_capped = False
    if triangle["signs"] is None and in_window:
        coverage = min(coverage_raw, SIGNS_UNKNOWN_COVERAGE_CAP)
        coverage_capped = coverage != coverage_raw

    verified_eb = coverage_detail["economic_buyer"][0] == 1.0

    # Champion risk — derive what is derivable, accept explicit flags for the rest.
    flags = dict(account.get("risk_flags") or {})
    champion = next((c for c in scored if c.get("role") == "champion"), None)
    key = [c for c in scored if c.get("role") in ("champion", "economic_buyer")]
    if any(c.get("email_status") == "hard_bounce" for c in key):
        flags["hard_bounce_key_contact"] = True
    flags["single_threaded"] = depth <= 1
    if champion:
        gap = days_since(champion.get("last_seen_product"), today)
        baseline = champion.get("login_baseline_days")
        if gap is not None and baseline:
            flags["login_gap"] = gap >= max(14, 3 * baseline)
        if champion.get("advocacy_events") is not None:
            flags["no_advocacy_180d"] = champion["advocacy_events"] == 0

    fired = [(k, pts, label) for k, pts, label in RISK_FACTORS if flags.get(k)]
    risk = min(RISK_CAP, sum(p for _, p, _ in fired))

    # Exposure.
    mult = risk_multiplier(risk)
    p_dep = min(P_DEPARTURE_CAP, BASE_ANNUAL_DEPARTURE_RATE * (horizon / 365) * mult)
    struct_now = structural_multiplier(depth, verified_eb)
    if concentration >= 3:
        struct_now = 1.00          # C7 — one person holds all three; depth does not rescue it
    struct_target = structural_multiplier(targets["depth"], True)
    exposure = arr * p_dep * P_LOSS_GIVEN_DEPARTURE * struct_now
    exposure_target = arr * p_dep * P_LOSS_GIVEN_DEPARTURE * struct_target
    closable = max(0.0, exposure - exposure_target)

    blockers = blockers_for(scored, in_window)

    return {
        "account_id": account.get("account_id"),
        "name": account.get("name"),
        "arr": arr,
        "contacts": scored,
        "targets": targets,
        "depth": depth,
        "breadth": breadth,
        "height": height,
        "coverage": coverage,
        "coverage_detail": coverage_detail,
        "verified_eb": verified_eb,
        "risk": risk,
        "risk_fired": fired,
        "risk_flags": flags,
        "p_dep": p_dep,
        "mult": mult,
        "struct_now": struct_now,
        "struct_target": struct_target,
        "exposure": exposure,
        "exposure_target": exposure_target,
        "closable": closable,
        "renewal_date": renewal,
        "opt_out": opt_out,
        "days_to_opt_out": days_to_opt_out,
        "in_window": in_window,
        "triangle": triangle,
        "concentration": concentration,
        "concentrated_on": concentrated_on,
        "coverage_raw": coverage_raw,
        "coverage_capped": coverage_capped,
        "blockers": blockers,
        "gaps": gaps_for(depth, breadth, height, coverage, targets, coverage_detail,
                         triangle, concentration, in_window, blockers, scored),
    }


def blockers_for(scored, in_window):
    """C11 — every negative or hostile contact needs an explicit disposition with its risk.
    Returns rows plus the specific violation, so the artifact cannot print a blank cell."""
    rows = []
    for c in scored:
        negative = c.get("sentiment") in ("negative", "hostile") or c.get("role") == "blocker"
        if not (negative or c.get("objection")):
            continue
        disp = (c.get("disposition") or "").lower() or None
        holds_veto = bool(c.get("function") in VETO_FUNCTIONS
                          or c["effective_role"] in VETO_ROLES
                          or c.get("holds_veto"))
        violation = None
        if disp not in DISPOSITIONS:
            violation = ("UNKNOWN is not a permitted disposition inside the renewal window — "
                         "state the test, the owner and the date"
                         if in_window else
                         "no disposition recorded — permitted outside the renewal window only "
                         "with a revisit date")
        elif disp == "bypass" and holds_veto:
            violation = "bypass refused — this contact holds a veto; falls back to contain"
            disp = "contain"
        elif not c.get("disposition_risk"):
            violation = "disposition recorded with no risk stated — the risk cell is required"
        rows.append({
            "name": c.get("name"), "role": c["effective_role"],
            "sentiment": c.get("sentiment"), "objection": c.get("objection"),
            "holds_veto": holds_veto, "disposition": disp,
            "risk": c.get("disposition_risk"), "owner": c.get("disposition_owner"),
            "by": c.get("disposition_by"), "find_out": c.get("find_out"),
            "violation": violation,
        })
    return rows


def gaps_for(depth, breadth, height, coverage, targets, coverage_detail,
             triangle, concentration, in_window, blockers, scored):
    out = []
    # C7/C11 first: authority and opposition rank above structure, whatever the health reads.
    for field in TRIANGLE:
        if triangle.get(field) is None:
            src = {"signs": "the executed order form and the MSA notices clause",
                   "decides": "an observed override or unbudgeted approval",
                   "influences": "a decision that changed after someone spoke"}[field]
            urgent = " [PRIMARY PLAY — signs unknown inside the renewal window]" \
                if field == "signs" and in_window else ""
            out.append(f"C7: `{field}` UNKNOWN — requires {src}{urgent}")
    if concentration >= 3:
        out.append("C7: CONCENTRATION 3/3 — one person signs, decides and influences; "
                   "structural multiplier floored at 1.00")
    elif concentration == 2:
        out.append("C7: CONCENTRATION 2/3 — two of the three authority roles on one person")
    for b in blockers:
        if b["violation"]:
            out.append(f"C11: {b['name']} — {b['violation']}")
    supporters = [c["name"] for c in scored if c["is_supporter"]
                  and c.get("claimed_role") == "champion"]
    if supporters:
        out.append("C8: champion slot held only by a supporter (" + ", ".join(supporters) +
                   ") — scores 0.0; recruit from a contact at mobilising >= 2")
    if depth <= 1:
        out.append("SEVERE: single-threaded (depth 1)")
    elif depth < targets["depth"]:
        out.append(f"depth {depth} below band target {targets['depth']}")
    if breadth < targets["breadth"]:
        out.append(f"breadth {breadth} below band target {targets['breadth']}")
    hi = SENIORITY_ORDER.index(height) if height in SENIORITY_ORDER else -1
    if hi < SENIORITY_ORDER.index(targets["height"]):
        out.append(f"height {height or 'none'} below band target {targets['height']}")
    if coverage < targets["coverage"]:
        out.append(f"coverage {coverage:.1f}/4 below band floor {targets['coverage']}/4")
    for role, (value, note) in coverage_detail.items():
        if value == 0.0:
            out.append(f"no {role} identified")
    return out


# ----------------------------------------------------------------------------------------
# Rendering
# ----------------------------------------------------------------------------------------

def money(v):
    return f"${v:,.0f}"


def sig2(v):
    """Two significant figures — SKILL-STANDARD 4F / R22. A composite stated to the dollar
    implies a measurement that was never taken."""
    if v is None:
        return "-"
    if v == 0:
        return "$0"
    for unit, div in (("M", 1_000_000), ("k", 1_000)):
        if abs(v) >= div:
            x = v / div
            return f"~${x:.1f}{unit}" if abs(x) < 10 else f"~${x:.0f}{unit}"
    return f"~${v:.0f}"


def render_table(rows):
    head = (f"{'Account':<22}{'ARR':>11}{'Cov':>7}{'D/B/H':>14}{'Risk':>6}"
            f"{'Exposure':>12}{'Closable':>11}{'Opt-out':>9}")
    print(head)
    print("-" * len(head))
    for r in sorted(rows, key=lambda x: x["closable"], reverse=True):
        dbh = f"{r['depth']}/{r['breadth']}/{(r['height'] or '-')[:8]}"
        opt = "-" if r["days_to_opt_out"] is None else f"{r['days_to_opt_out']}d"
        print(f"{(r['name'] or r['account_id'])[:21]:<22}{money(r['arr']):>11}"
              f"{r['coverage']:>5.1f}/4{dbh:>14}{r['risk']:>4}/10"
              f"{sig2(r['exposure']):>12}{sig2(r['closable']):>11}{opt:>9}")
    total_e = sum(r["exposure"] for r in rows)
    total_c = sum(r["closable"] for r in rows)
    print("-" * len(head))
    print(f"{'TOTAL':<22}{money(sum(r['arr'] for r in rows)):>11}{'':>7}{'':>14}{'':>6}"
          f"{sig2(total_e):>12}{sig2(total_c):>11}")
    for r in rows:
        flags = []
        for f in TRIANGLE:
            if r["triangle"][f] is None:
                flags.append(f"{f}=UNKNOWN")
        if r["concentration"] >= 2:
            flags.append(f"CONCENTRATION {r['concentration']}/3")
        if r["coverage_capped"]:
            flags.append(f"coverage capped {r['coverage_raw']:.1f}->{r['coverage']:.1f} "
                         f"(C7: signs unknown, {r['days_to_opt_out']}d to opt-out)")
        if any(c["is_supporter"] and c.get("claimed_role") == "champion" for c in r["contacts"]):
            flags.append("champion slot = supporter only (C8)")
        bad = [b for b in r["blockers"] if b["violation"]]
        if bad:
            flags.append(f"{len(bad)} blocker row(s) invalid (C11)")
        if flags:
            print(f"  ! {r['name']}: " + " · ".join(flags))
    print("\nRanked by closable exposure — the dollars a coverage plan can actually remove.")
    print("Composites shown to two significant figures (R22): an ordering built on vendor rates,")
    print("not a calibrated forecast. Base departure rate UserGems 2026 [V]; loss-given-departure")
    print("Sturdy AI [V]; structural multipliers [P]. Use --explain for the exact arithmetic.")
    for r in rows:
        if r["depth"] <= 1:
            print(f"R5 single-thread tax: {r['name']} is depth {r['depth']} — flag the full "
                  f"{money(r['arr'])} as at-risk to churn-risk, not just the exposure above.")


def render_explain(r):
    print(f"\n=== {r['name']} ({r['account_id']}) ===")
    print(f"ARR {money(r['arr'])} · renewal {r['renewal_date']} · "
          f"opt-out {r['opt_out']} ({r['days_to_opt_out']}d)")
    t = r["targets"]
    print(f"Band target: depth {t['depth']} · breadth {t['breadth']} · height {t['height']} "
          f"· coverage {t['coverage']}/4 · shape {t['shape']}")
    print(f"Measured:    depth {r['depth']} · breadth {r['breadth']} · "
          f"height {r['height'] or 'none'} · coverage {r['coverage']:.1f}/4")

    print("\n-- Authority triangle (C7) --")
    for field in TRIANGLE:
        h = r["triangle"][field]
        if h is None:
            print(f"  {field:<12} UNKNOWN - requires a named source. Never inferred from title.")
        else:
            tw = "-" if h["two_way_days"] is None else f"{h['two_way_days']}d"
            print(f"  {field:<12} {h['name']} ({h.get('role_confidence')}, two-way {tw})")
    if r["concentration"] >= 3:
        print(f"  CONCENTRATION 3/3 on {r['concentrated_on']} - single point of authority; "
              f"structural multiplier floored at 1.00, ranks first in the plan.")
    elif r["concentration"] == 2:
        print(f"  CONCENTRATION 2/3 on {r['concentrated_on']}.")
    if r["coverage_capped"]:
        print(f"  REFUSED: coverage {r['coverage_raw']:.1f}/4 capped to {r['coverage']:.1f}/4 - "
              f"`signs` is UNKNOWN and the opt-out deadline is {r['days_to_opt_out']}d away. "
              f"Primary play is the signatory trace.")

    print("\n-- Coverage over the four key roles --")
    for role, (value, note) in r["coverage_detail"].items():
        print(f"  {role:<20} {value:>4.1f}  {note}")

    print("\n-- Contacts --")
    print(f"  {'Name':<20}{'Role (effective)':<22}{'Conf':<11}{'Mob':>5}{'2-way':>7}{'Strength':>10}")
    for c in sorted(r["contacts"], key=lambda x: (x["strength"] is None, -(x["strength"] or 0))):
        tw = "-" if c["two_way_days"] is None else f"{c['two_way_days']}d"
        st = "UNKNOWN" if c["strength"] is None else f"{c['strength']:.1f}"
        mob = "?" if c["mobilising"] is None else f"{c['mobilising']}/3"
        role = c["effective_role"] + (" (supporter)" if c["is_supporter"] else "")
        print(f"  {c['name'][:19]:<20}{role[:21]:<22}"
              f"{str(c.get('role_confidence'))[:10]:<11}{mob:>5}{tw:>7}{st:>10}")
    for c in r["contacts"]:
        if c["is_supporter"] and c.get("claimed_role") == "champion":
            print(f"  C8: {c['name']} was labelled champion but scores "
                  f"{'UNKNOWN' if c['mobilising'] is None else c['mobilising']}/3 on M1-M3 - "
                  f"recorded as coach + is_supporter. The champion slot scores 0.0.")
        elif c["effective_role"] == "champion":
            print(f"  C8: {c['name']} qualifies as champion - " + "; ".join(c["m_fired"]))

    print("\n-- Blockers (C11) --")
    if not r["blockers"]:
        print("  Checked and clear - no contact carries an objection on record.")
    for b in r["blockers"]:
        veto = "veto" if b["holds_veto"] else "no veto"
        print(f"  {b['name']} ({b['sentiment']}, {veto}) -> "
              f"{b['disposition'] or 'NO DISPOSITION'}"
              f"{'' if not b['risk'] else ' | risk: ' + b['risk']}")
        if b["violation"]:
            print(f"    INVALID: {b['violation']}")
            if b["find_out"]:
                print(f"    TEST: {b['find_out']} - {b['owner'] or 'OWNER REQUIRED'} "
                      f"by {b['by'] or 'DATE REQUIRED'}")

    print("\n-- Champion risk --")
    for k, pts, label in RISK_FACTORS:
        mark = "FIRED" if r["risk_flags"].get(k) else "clear"
        print(f"  [{mark:>5}] +{pts}  {label}")
    print(f"  TOTAL {r['risk']}/10  (>=6 = act this week)")

    print("\n-- Exposure arithmetic --")
    print(f"  risk_multiplier({r['risk']})            = {r['mult']}")
    print(f"  p_departure = 0.20 x horizon x mult   = {r['p_dep']:.4f}")
    print(f"  p_loss                                = {P_LOSS_GIVEN_DEPARTURE}")
    print(f"  structural(depth {r['depth']})                  = {r['struct_now']}")
    print(f"  exposure    = {money(r['arr'])} x {r['p_dep']:.4f} x {P_LOSS_GIVEN_DEPARTURE} "
          f"x {r['struct_now']} = {money(r['exposure'])}  -> report {sig2(r['exposure'])}")
    print(f"  at target depth {r['targets']['depth']} (structural {r['struct_target']})"
          f"      = {money(r['exposure_target'])}  -> report {sig2(r['exposure_target'])}")
    print(f"  CLOSABLE BY MULTITHREADING            = {money(r['closable'])}"
          f"  -> report {sig2(r['closable'])}")

    print("\n-- Gaps --")
    if r["gaps"]:
        for g in r["gaps"]:
            print(f"  - {g}")
    else:
        print("  none — measured structure meets the band target on every dimension")


def main() -> int:
    ap = argparse.ArgumentParser(description="Stakeholder coverage and champion-risk scoring.")
    ap.add_argument("path", help="JSON file: one account object or a list of them")
    ap.add_argument("--today", default=date.today().isoformat(), help="YYYY-MM-DD")
    ap.add_argument("--horizon", type=int, default=365, help="exposure horizon in days")
    ap.add_argument("--explain", help="account_id or name to print in full")
    args = ap.parse_args()

    today = parse_date(args.today)
    try:
        data = json.loads(open(args.path).read())
    except (OSError, json.JSONDecodeError) as e:
        print(f"could not read {args.path}: {e}", file=sys.stderr)
        return 2
    accounts = data if isinstance(data, list) else [data]

    rows = [measure(a, today, args.horizon) for a in accounts]

    print(f"Stakeholder coverage — as-of {today} · horizon {args.horizon}d · "
          f"{len(rows)} account(s)\n")
    render_table(rows)

    if args.explain:
        want = args.explain.lower()
        for r in rows:
            if want in (str(r["account_id"]).lower(), str(r["name"]).lower()):
                render_explain(r)
                break
        else:
            print(f"\nno account matching '{args.explain}'", file=sys.stderr)
            return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
