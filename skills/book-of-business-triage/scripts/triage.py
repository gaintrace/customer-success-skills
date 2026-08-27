#!/usr/bin/env python3
"""
Capacity-constrained weekly triage for the `book-of-business-triage` skill.

Why a script: the queue is an allocation problem with a hard budget, and an LLM doing
running-total arithmetic across 40 accounts in prose will drift — usually in the direction
of "it all fits". This produces the same cut line every time and shows every step.

What it does NOT do: decide anything. It ranks, allocates and totals. Which play to run,
whether the addressability call is honest, and what to tell the customer are judgement.

Usage
-----
    python3 triage.py book.json
    python3 triage.py book.json --json
    python3 triage.py book.json --explain ACME

Input: see scripts/sample_book.json for a complete worked example.

    {
      "as_of": "2026-08-31",
      "owner": "r.mehta",
      "capacity": {
        "gross_hours": 40.0,            # line A
        "internal_load_hours": 13.3,    # line B  (default: two-thirds rule -> A/3)
        "committed_meeting_hours": 6.5, # line D  (costed at PLAY duration, not invite length)
        "reactive_reserve_hours": 6.0,  # line E  (P75 of last 8 weeks, or a labelled default)
        "realisation_factor": 0.85,     # line G
        "maintenance_share": 0.30,
        "rot_share": 0.12
      },
      "accounts": [ ... ]
    }

Nulls matter. `risk_band: null` means NOT MEASURED — the account is reported as unrankable,
never scored as low risk. `last_bilateral_touch: null` means not measured — it is reported as
UNKNOWN, never treated as "touched today".

No network. Standard library only.
"""

from __future__ import annotations

import argparse
import math
import json
import sys
from datetime import date, timedelta
from typing import Any

# --------------------------------------------------------------------------------------
# Model constants. These mirror SKILL.md and references/play-durations.md.
# Change them together or the artifact stops matching the script.
# --------------------------------------------------------------------------------------

# Band midpoints. Stated probabilities of a RULES-BASED model, not calibrated forecasts.
# Replace with backtested rates and cite the backtest before calling these probabilities.
BAND_PROB: dict[str, float] = {
    "secure": 0.05,
    "watch": 0.15,
    "at_risk": 0.35,
    "high": 0.60,
    "critical": 0.85,
}

# Urgency multiplier by days to the binding date (opt-out deadline / SLA / committed date).
URGENCY_BANDS: list[tuple[int, float]] = [
    (14, 1.60),
    (30, 1.40),
    (60, 1.20),
    (90, 1.05),
    (180, 0.90),
]
URGENCY_FAR = 0.75  # >180 days, or no binding date at all

ADDRESSABILITY: dict[str, float] = {
    "addressable": 1.2,   # adoption, enablement, relationship, support unblock
    "partial": 1.0,       # pricing, budget, needs a third party
    "structural": 0.5,    # acquired, shut down, product gap not on the roadmap
    "blocked": 0.2,       # awaiting customer, cooldown or blackout window
}
DEFAULT_ADDRESSABILITY = "partial"

# CSM hours, end to end: pull + prep + delivery + follow-up + write-up.
# Practitioner calibration [P] — replace with your own median at 8 instances.
PLAY_HOURS: dict[str, float] = {
    "templated_nudge": 0.10,
    "async_checkin": 0.50,
    "value_snapshot": 1.25,
    "commitment_chase": 0.25,
    "intro_request": 0.40,
    "rot_checkpoint": 0.25,
    "incident_apology": 1.50,
    "cadence_call_30": 1.25,
    "cadence_call_60": 2.00,
    "discovery_call": 2.00,
    "new_stakeholder_intro": 1.75,
    "renewal_conversation_mm": 3.00,
    "renewal_conversation_ent": 5.50,
    "escalation_day_one": 2.50,
    "escalation_weekly": 2.00,
    "save_play_kickoff": 4.00,
    "exec_reengagement": 2.50,
    "handover_call": 1.50,
    "adoption_reset": 4.50,
    "onboarding_kickoff": 5.00,
    "enablement_session": 3.00,
    "integration_unblock": 3.00,
    "success_plan_build": 4.00,
    "rethread_champion": 3.50,
    "qbr_templated": 4.00,
    "qbr_operational": 6.00,
    "ebr_live": 11.00,
    "csql_handoff": 1.00,
    "expansion_business_case": 5.00,
    "true_up_conversation": 2.00,
    "contract_admin": 1.00,
}

SEGMENT_MULTIPLIER: dict[str, float] = {
    "tech_touch": 0.6,
    "pooled": 0.6,
    "smb": 0.8,
    "mid_market": 1.0,
    "enterprise": 1.5,
    "strategic": 2.0,
}

# Silence thresholds for the rot sweep, in days. Practitioner [P], segment-scaled.
SILENCE_TOUCH_DAYS: dict[str, int] = {
    "strategic": 21, "enterprise": 45, "mid_market": 75,
    "smb": 120, "pooled": 120, "tech_touch": 120,
}
SILENCE_ACTIVITY_DAYS: dict[str, int] = {
    "strategic": 14, "enterprise": 21, "mid_market": 30,
    "smb": 45, "pooled": 45, "tech_touch": 45,
}
DARK_ACCOUNT_DAYS = 60          # contract active this long with zero core events
UNOWNED_DAYS = 30
DEFERRAL_FORCE_AT = 3           # third consecutive deferral forces a decision

# C31 · Touch the top decile weekly regardless of health. The largest accounts go red between
# reviews and do it most expensively, so their touch is reserved off the top of the budget
# (line I) BEFORE the remaining hours are allocated by risk (line J). Health never removes a
# member from the block; only a covering row elsewhere in the queue, or a named escalation.
TOP_DECILE_FRACTION = 0.10      # ceil(N * this) accounts, minimum 1
MATERIAL_ARR_SHARE = 0.10       # any account >= this share of book ARR joins whatever its rank
TOP_DECILE_RESERVE_CAP = 0.25   # line I may not exceed this share of line H

# Expansion is forbidden while any of these hold. Selling into dissatisfaction converts a
# renewal risk into a churn certainty.
EXPANSION_BLOCKING_BANDS = {"at_risk", "high", "critical"}


# --------------------------------------------------------------------------------------
# Helpers
# --------------------------------------------------------------------------------------

def d(value: Any) -> date | None:
    """Parse an ISO date, tolerating None."""
    if not value:
        return None
    return date.fromisoformat(str(value)[:10])


def days_between(later: date | None, earlier: date | None) -> int | None:
    if later is None or earlier is None:
        return None
    return (later - earlier).days


def urgency_for(days: int | None) -> float:
    if days is None:
        return URGENCY_FAR
    for threshold, mult in URGENCY_BANDS:
        if days <= threshold:
            return mult
    return URGENCY_FAR


def money(x: float) -> str:
    return f"${x:,.0f}"


def table(headers: list[str], rows: list[list[str]]) -> str:
    if not rows:
        return "  (none)\n"
    widths = [len(h) for h in headers]
    for r in rows:
        for i, cell in enumerate(r):
            widths[i] = max(widths[i], len(str(cell)))
    line = "  " + "  ".join(h.ljust(widths[i]) for i, h in enumerate(headers))
    sep = "  " + "  ".join("-" * widths[i] for i in range(len(headers)))
    out = [line, sep]
    for r in rows:
        out.append("  " + "  ".join(str(c).ljust(widths[i]) for i, c in enumerate(r)))
    return "\n".join(out) + "\n"


# --------------------------------------------------------------------------------------
# Capacity
# --------------------------------------------------------------------------------------

def compute_capacity(cap: dict[str, Any]) -> dict[str, float]:
    a = float(cap.get("gross_hours", 40.0))
    # Default line B is the two-thirds convention: reserve two-thirds of the week for
    # customers, one-third for internal load. Practitioner default [P], consistent with
    # library Operating Rule R13 (usable time is roughly 60% of a week). Not a benchmark.
    b = float(cap.get("internal_load_hours", round(a / 3.0, 1)))
    c = a - b
    dd = float(cap.get("committed_meeting_hours", 0.0))
    e = float(cap.get("reactive_reserve_hours", max(5.0, 0.10 * c)))
    f = c - dd - e
    g = float(cap.get("realisation_factor", 0.85))
    h = max(0.0, f * g)
    return {
        "A_gross": a, "B_internal": b, "C_deployable": c, "D_meetings": dd,
        "E_reserve": e, "F_discretionary": f, "G_realisation": g, "H_budget": h,
        "maintenance_share": float(cap.get("maintenance_share", 0.30)),
        "rot_share": float(cap.get("rot_share", 0.12)),
    }


# --------------------------------------------------------------------------------------
# Per-account derivation
# --------------------------------------------------------------------------------------

def play_hours(acct: dict[str, Any]) -> tuple[float, str]:
    """Hours for this account's play, with the segment multiplier applied."""
    if acct.get("play_hours") is not None:
        return float(acct["play_hours"]), "explicit override"
    play = acct.get("play")
    base = PLAY_HOURS.get(play)
    if base is None:
        return 1.25, f"UNKNOWN play '{play}' — defaulted to cadence_call_30 (1.25h)"
    mult = SEGMENT_MULTIPLIER.get(acct.get("segment", "mid_market"), 1.0)
    return round(base * mult, 2), f"{play} {base}h x {mult} ({acct.get('segment')})"


def derive(acct: dict[str, Any], as_of: date) -> dict[str, Any]:
    r = dict(acct)
    renewal = d(acct.get("renewal_date"))
    notice = acct.get("notice_period_days")

    if renewal and notice is not None:
        r["opt_out_deadline"] = renewal - timedelta(days=int(notice))
        r["days_to_opt_out"] = days_between(r["opt_out_deadline"], as_of)
    else:
        r["opt_out_deadline"] = None
        r["days_to_opt_out"] = None
        r["opt_out_note"] = "UNKNOWN — requires subscription.renewal_date and notice_period_days"

    r["days_since_touch"] = days_between(as_of, d(acct.get("last_bilateral_touch")))
    r["days_since_activity"] = days_between(as_of, d(acct.get("last_product_activity")))

    # ---- must-do triggers -------------------------------------------------------------
    triggers: list[tuple[str, str, date | None]] = []

    if r["days_to_opt_out"] is not None and r["days_to_opt_out"] <= 30 \
            and not acct.get("renewal_conversation_held"):
        triggers.append((
            "Opt-out deadline <=30d, no renewal conversation logged",
            f"opt-out {r['opt_out_deadline']} ({r['days_to_opt_out']}d)",
            r["opt_out_deadline"]))

    flip = d(acct.get("auto_renew_changed_at"))
    if flip and (as_of - flip).days <= 7 and acct.get("auto_renew") is False:
        triggers.append(("Auto-renew switched off in the last 7 days",
                         f"changed {flip}", as_of + timedelta(days=1)))

    esc = acct.get("open_escalation_days")
    if esc and int(esc) > 14:
        triggers.append((f"Escalation open {esc}d (>14d)",
                         "ticket.type=escalation, status open", as_of + timedelta(days=2)))

    due = d(acct.get("committed_followup_due"))
    if due and due < as_of:
        triggers.append((f"Committed follow-up overdue by {(as_of - due).days}d",
                         f"promised due {due}", due))

    if acct.get("termination_terms_requested"):
        triggers.append(("Termination terms / data portability requested",
                         "legal or procurement thread", as_of + timedelta(days=1)))

    dsc = acct.get("days_since_contract_start")
    core = acct.get("core_events_since_start")
    if dsc is not None and core is not None and int(dsc) > DARK_ACCOUNT_DAYS and int(core) == 0:
        triggers.append((f"Dark account — {dsc}d since start, zero core events",
                         "usage_event", as_of + timedelta(days=5)))

    if acct.get("exec_requested_due"):
        triggers.append(("Executive- or manager-requested item with a date",
                         f"due {acct['exec_requested_due']}", d(acct["exec_requested_due"])))

    if int(acct.get("deferral_count", 0) or 0) >= DEFERRAL_FORCE_AT:
        triggers.append((
            f"Deferral counter {acct.get('deferral_count')} (>= {DEFERRAL_FORCE_AT}) — "
            "forced checkpoint or written demotion",
            "book-of-business-triage not-this-week list", as_of + timedelta(days=5)))

    r["must_do_triggers"] = triggers
    r["is_must_do"] = bool(triggers)

    # ---- health gate on the expansion basis --------------------------------------------
    gates: list[str] = list(acct.get("health_gate_blocks") or [])
    if acct.get("risk_band") in EXPANSION_BLOCKING_BANDS:
        gates.append(f"risk band {acct['risk_band']}")
    r["expansion_gates"] = gates

    # ---- value ------------------------------------------------------------------------
    band = acct.get("risk_band")
    arr = float(acct.get("arr") or 0.0)
    risk_value: float | None = None
    if band in BAND_PROB:
        risk_value = arr * BAND_PROB[band]
    elif band is not None:
        r["value_note"] = f"UNKNOWN — unrecognised risk_band '{band}'"

    exp_arr = acct.get("expansion_arr")
    exp_wr = acct.get("expansion_win_rate")
    exp_value: float | None = None
    if exp_arr and exp_wr is not None and not gates:
        exp_value = float(exp_arr) * float(exp_wr)
    elif exp_arr and exp_wr is None:
        r["expansion_note"] = "UNKNOWN — requires a cohort win rate for the expansion basis"

    if risk_value is None and exp_value is None:
        r["value"] = None
        r["basis"] = "UNRANKABLE"
        r["value_note"] = r.get("value_note") or (
            "UNKNOWN — requires a churn-risk band, or an expansion ARR with a win rate")
    elif exp_value is not None and (risk_value is None or exp_value > risk_value):
        r["value"], r["basis"] = exp_value, "expansion"
    else:
        r["value"], r["basis"] = risk_value, "risk"

    # ---- urgency, addressability, hours, RPH -------------------------------------------
    binding_candidates = [t[2] for t in triggers if t[2]]
    if r["opt_out_deadline"]:
        binding_candidates.append(r["opt_out_deadline"])
    r["binding_date"] = min(binding_candidates) if binding_candidates else None
    r["days_to_binding"] = days_between(r["binding_date"], as_of)
    r["urgency"] = urgency_for(r["days_to_binding"])

    addr_key = acct.get("addressability") or DEFAULT_ADDRESSABILITY
    if addr_key not in ADDRESSABILITY:
        addr_key = DEFAULT_ADDRESSABILITY
        r["addressability_note"] = "assumed 'partial' — addressability not stated"
    r["addressability"] = addr_key
    r["addressability_mult"] = ADDRESSABILITY[addr_key]

    r["hours"], r["hours_basis"] = play_hours(acct)
    if r["value"] is not None and r["hours"] > 0:
        r["rph"] = (r["value"] * r["urgency"] * r["addressability_mult"]) / r["hours"]
    else:
        r["rph"] = None

    # ---- rot sweep ---------------------------------------------------------------------
    seg = acct.get("segment", "mid_market")
    rot: list[str] = []
    if r["days_since_touch"] is None and acct.get("last_bilateral_touch") is None:
        rot.append("UNKNOWN last_bilateral_touch — requires an interaction source")
    elif r["days_since_touch"] is not None and \
            r["days_since_touch"] > SILENCE_TOUCH_DAYS.get(seg, 75):
        rot.append(f"no bilateral touch {r['days_since_touch']}d "
                   f"(>{SILENCE_TOUCH_DAYS.get(seg, 75)}d for {seg})")
    if r["days_since_activity"] is not None and \
            r["days_since_activity"] > SILENCE_ACTIVITY_DAYS.get(seg, 30):
        rot.append(f"no product activity {r['days_since_activity']}d "
                   f"(>{SILENCE_ACTIVITY_DAYS.get(seg, 30)}d for {seg})")
    if dsc is not None and core is not None and int(dsc) > DARK_ACCOUNT_DAYS and int(core) == 0:
        rot.append("dark account")
    if not acct.get("owner_csm"):
        rot.append(f"unowned (>{UNOWNED_DAYS}d threshold)")
    if int(acct.get("deferral_count", 0) or 0) >= DEFERRAL_FORCE_AT:
        rot.append(f"deferral counter {acct.get('deferral_count')}")
    r["rot_flags"] = rot

    return r


# --------------------------------------------------------------------------------------
# Allocation
# --------------------------------------------------------------------------------------

def build_queue(book: dict[str, Any]) -> dict[str, Any]:
    as_of = d(book.get("as_of")) or date.today()
    cap = compute_capacity(book.get("capacity", {}))
    accounts = [derive(a, as_of) for a in book.get("accounts", [])]

    must_do = [a for a in accounts if a["is_must_do"]]
    rest = [a for a in accounts if not a["is_must_do"]]

    must_do_hours = round(sum(a["hours"] for a in must_do), 2)
    stop_rule = (cap["D_meetings"] + must_do_hours) > cap["C_deployable"]

    # ---- C31: reserve the top ARR decile BEFORE anything is ranked -------------------
    arr_book = sum(a.get("arr") or 0 for a in accounts)
    by_arr = sorted(accounts, key=lambda x: -(x.get("arr") or 0))
    n_decile = max(1, math.ceil(len(accounts) * TOP_DECILE_FRACTION)) if accounts else 0
    decile_ids = {a["account_id"] for a in by_arr[:n_decile]}
    if arr_book:
        decile_ids |= {a["account_id"] for a in accounts
                       if (a.get("arr") or 0) / arr_book >= MATERIAL_ARR_SHARE}
    decile_cutoff = min((a.get("arr") or 0) for a in accounts
                        if a["account_id"] in decile_ids) if decile_ids else 0
    must_do_ids = {a["account_id"] for a in must_do}

    decile_cap = round(cap["H_budget"] * TOP_DECILE_RESERVE_CAP, 2)
    decile_members = [a for a in by_arr if a["account_id"] in decile_ids]
    for a in decile_members:
        a["decile_member"] = True
        a["decile_share"] = round((a.get("arr") or 0) / arr_book, 4) if arr_book else None
        mult = SEGMENT_MULTIPLIER.get(a.get("segment", "mid_market"), 1.0)
        base = PLAY_HOURS["cadence_call_30"] if a.get("cadence_due_since") \
            else PLAY_HOURS["async_checkin"]
        a["decile_touch_hours"] = round(base * mult, 2)

    decile_touch, decile_escalate, decile_hours = [], [], 0.0
    # Longest silence first: an UNKNOWN last touch sorts as the longest silence there is,
    # because unmeasured is not the same as recent.
    for a in sorted(decile_members,
                    key=lambda x: -(x["days_since_touch"] if x["days_since_touch"] is not None
                                    else 10_000)):
        if a["account_id"] in must_do_ids:
            a["decile_covered_by"] = "must-do block"
            continue
        if decile_hours + a["decile_touch_hours"] <= decile_cap:
            decile_hours = round(decile_hours + a["decile_touch_hours"], 2)
            a["decile_covered_by"] = "section 2 · reserved touch"
            decile_touch.append(a)
        else:
            # Never a silent drop: the member becomes a named escalation with its hours.
            a["decile_covered_by"] = "ESCALATED — reserve cap reached"
            decile_escalate.append(a)
    decile_ids_touched = {a["account_id"] for a in decile_touch}

    remaining = round(cap["H_budget"] - must_do_hours - decile_hours, 2)
    if remaining <= 0:
        hr_budget = maint_budget = rot_budget = 0.0
    else:
        maint_budget = round(remaining * cap["maintenance_share"], 2)
        rot_budget = round(remaining * cap["rot_share"], 2)
        hr_budget = round(remaining - maint_budget - rot_budget, 2)

    rankable = [a for a in rest if a["rph"] is not None]
    unrankable = [a for a in rest if a["rph"] is None]
    # Tie-break, stated in SKILL.md Step 3: RPH desc -> earlier binding date -> larger value
    # -> longer since last bilateral touch.
    rankable.sort(key=lambda a: (
        -a["rph"],
        a["days_to_binding"] if a["days_to_binding"] is not None else 10_000,
        -(a["value"] or 0),
        -(a["days_since_touch"] if a["days_since_touch"] is not None else 0),
    ))

    high_return, below_cut, running = [], [], 0.0
    for a in rankable:
        if running + a["hours"] <= hr_budget:
            running = round(running + a["hours"], 2)
            a["running_total"] = running
            high_return.append(a)
        else:
            below_cut.append(a)
    cut_at = running

    maintenance, maint_running = [], 0.0
    for a in sorted([x for x in below_cut if x.get("cadence_due_since")],
                    key=lambda x: x["cadence_due_since"]):
        touch = min(a["hours"], PLAY_HOURS["async_checkin"]
                    * SEGMENT_MULTIPLIER.get(a.get("segment", "mid_market"), 1.0))
        if maint_running + touch <= maint_budget:
            maint_running = round(maint_running + touch, 2)
            a["maintenance_hours"] = round(touch, 2)
            a["running_total"] = maint_running
            maintenance.append(a)
    maint_ids = {a["account_id"] for a in maintenance}

    rot_hits = [a for a in accounts if a["rot_flags"]]
    hr_ids = {a["account_id"] for a in high_return}
    rot_queue, rot_running = [], 0.0
    for a in sorted(rot_hits, key=lambda x: -(x.get("arr") or 0)):
        if a["is_must_do"] or a["account_id"] in maint_ids or a["account_id"] in hr_ids:
            continue
        if rot_running + PLAY_HOURS["rot_checkpoint"] <= rot_budget:
            rot_running = round(rot_running + PLAY_HOURS["rot_checkpoint"], 2)
            a["rot_hours"] = PLAY_HOURS["rot_checkpoint"]
            rot_queue.append(a)
    rot_ids = {a["account_id"] for a in rot_queue}

    scheduled = {a["account_id"] for a in high_return} | maint_ids | rot_ids \
        | must_do_ids | decile_ids_touched
    not_this_week = [a for a in accounts if a["account_id"] not in scheduled]

    # C32 · every account skipped this cycle carries the row that displaced it and a revisit
    # date. "No capacity" is not a reason; the marginal row that consumed the budget is.
    if remaining <= 0:
        displaced_by = f"must-do block + top-decile reserve ({must_do_hours + decile_hours:.2f}h)"
    elif high_return:
        displaced_by = f"{high_return[-1]['name']} (last row above the cut line)"
    else:
        displaced_by = f"line J exhausted at {remaining:.2f}h before any ranked row fitted"
    next_review = (as_of + timedelta(days=7)).isoformat()
    for a in not_this_week:
        a["displaced_by"] = displaced_by
        a["next_review"] = next_review

    # Greedy allocation skips a high-RPH item that is simply too large for the remaining
    # budget. That is a real finding, not an artifact to hide: it means stage the play or
    # displace committed work.
    floor_rph = min((a["rph"] for a in high_return), default=None)
    skipped_for_size = [a for a in below_cut
                        if floor_rph is not None and a["rph"] > floor_rph]

    escalation_candidates = []
    arr_all = arr_book or 1
    for a, why in [(x, "top-decile member the reserve cap could not fund — "
                       f"needs {x['decile_touch_hours']:.2f}h (C31)") for x in decile_escalate]:
        escalation_candidates.append((a, [why]))
    for a in below_cut + unrankable:
        if a.get("decile_covered_by") == "ESCALATED — reserve cap reached":
            continue
        reasons = []
        if a.get("risk_band") in ("high", "critical"):
            reasons.append(f"{a['risk_band']} band, deliberately not covered")
        if (a.get("arr") or 0) / arr_all > 0.10:
            reasons.append(f">10% of book ARR ({(a.get('arr') or 0) / arr_all * 100:.0f}%)")
        if int(a.get("deferral_count", 0) or 0) >= DEFERRAL_FORCE_AT - 1:
            reasons.append(f"deferral counter {a.get('deferral_count')}")
        if a["rph"] is None:
            reasons.append("unrankable — data gap on a material account")
        if reasons:
            escalation_candidates.append((a, reasons))

    arr_total = sum(a.get("arr") or 0 for a in accounts)
    arr_touched = sum(a.get("arr") or 0 for a in accounts if a["account_id"] in scheduled)
    allocated = round(must_do_hours + decile_hours + cut_at + maint_running + rot_running, 2)

    deficit = round(allocated - cap["H_budget"], 2)
    if stop_rule:
        verdict = "STRUCTURALLY OVERSUBSCRIBED — must-do work exceeds deployable hours"
    elif remaining <= 0:
        verdict = "OVERSUBSCRIBED — must-do work consumes the entire queue budget"
    elif not_this_week:
        verdict = f"Servable with omissions — {len(not_this_week)} accounts deliberately not covered"
    else:
        verdict = "Servable — the whole book fits this week"

    return {
        "as_of": as_of.isoformat(),
        "owner": book.get("owner"),
        "capacity": cap,
        "budgets": {"must_do": must_do_hours, "top_decile": decile_hours,
                    "remaining_after_must_do": remaining,
                    "high_return": hr_budget, "maintenance": maint_budget, "rot": rot_budget},
        "stop_rule_fired": stop_rule,
        "must_do": must_do,
        "top_decile": decile_members,
        "top_decile_touch": decile_touch,
        "top_decile_escalated": decile_escalate,
        "top_decile_cutoff": decile_cutoff,
        "top_decile_cap": decile_cap,
        "high_return": high_return,
        "cut_line_hours": cut_at,
        "maintenance": maintenance,
        "rot_queue": rot_queue,
        "not_this_week": not_this_week,
        "unrankable": unrankable,
        "skipped_for_size": skipped_for_size,
        "escalation_candidates": escalation_candidates,
        "totals": {
            "accounts": len(accounts),
            "accounts_worked": len(accounts) - len(not_this_week),
            "accounts_written_off": len(not_this_week),
            # C32 · a genuine set check: every account is either worked in a named section or
            # written down in the not-this-week list. Neither silently absent nor double-counted.
            "reconciles": ({x["account_id"] for x in
                            must_do + decile_touch + high_return + maintenance
                            + rot_queue + not_this_week}
                           == {x["account_id"] for x in accounts}),
            "top_decile_members": len(decile_members),
            "top_decile_touched": len(decile_touch) + len([a for a in decile_members
                                                           if a["account_id"] in must_do_ids]),
            "top_decile_escalated": len(decile_escalate),
            "arr_total": arr_total,
            "arr_touched": arr_touched,
            "arr_not_touched": arr_total - arr_touched,
            "hours_top_decile": decile_hours,
            "hours_allocated": allocated,
            "hours_budget": round(cap["H_budget"], 2),
            "budget_utilisation": round(allocated / cap["H_budget"], 3) if cap["H_budget"] else None,
            "hours_over_budget": deficit if deficit > 0 else 0.0,
        },
        "verdict": verdict,
    }


# --------------------------------------------------------------------------------------
# Report
# --------------------------------------------------------------------------------------

def _rot_display(q: dict[str, Any]) -> list[dict[str, Any]]:
    """Every account with a rot flag, once, richest first."""
    seen: dict[str, dict[str, Any]] = {}
    for a in (q["must_do"] + q["high_return"] + q["maintenance"]
              + q["rot_queue"] + q["not_this_week"] + q["unrankable"]):
        if a["rot_flags"]:
            seen.setdefault(a["account_id"], a)
    return sorted(seen.values(), key=lambda x: -(x.get("arr") or 0))


def render(q: dict[str, Any]) -> str:
    c, t, b = q["capacity"], q["totals"], q["budgets"]
    o: list[str] = []
    o.append(f"WEEKLY BOOK TRIAGE — {q['owner'] or 'unassigned'} · as of {q['as_of']}")
    o.append("INTERNAL. Contains risk language that must never be sent to a customer.\n")

    o.append("BOTTOM LINE")
    o.append(f"  Book                      {t['accounts']} accounts · {money(t['arr_total'])} ARR")
    o.append(f"  Effective queue budget    {t['hours_budget']} h")
    o.append(f"  Allocated                 {t['hours_allocated']} h "
             f"({(t['budget_utilisation'] or 0) * 100:.0f}% of budget)")
    o.append(f"  ARR touched this week     {money(t['arr_touched'])} "
             f"({t['arr_touched'] / t['arr_total'] * 100:.0f}% of book)"
             if t["arr_total"] else "  ARR touched this week     n/a")
    o.append(f"  ARR NOT touched           {money(t['arr_not_touched'])} "
             f"across {len(q['not_this_week'])} accounts")
    o.append(f"  Top decile (C31)          {t['top_decile_members']} members · "
             f"{t['top_decile_touched']} touched · {t['top_decile_escalated']} escalated")
    o.append(f"  Accounts reconciled       {t['accounts_worked']} worked + "
             f"{t['accounts_written_off']} written off = {t['accounts']} of {t['accounts']}")
    o.append(f"  Capacity verdict          {q['verdict']}\n")

    o.append("0. CAPACITY ARITHMETIC")
    o.append(table(["Line", "Hours", "Basis"], [
        ["A gross week", f"{c['A_gross']:.1f}", "contracted hours"],
        ["B internal load", f"-{c['B_internal']:.1f}", "measured, or two-thirds default [P]"],
        ["C deployable", f"{c['C_deployable']:.1f}", "A - B"],
        ["D committed meetings", f"-{c['D_meetings']:.1f}", "costed at play duration"],
        ["E reactive reserve", f"-{c['E_reserve']:.1f}", "P75 of last 8 weeks, or default [P]"],
        ["F discretionary", f"{c['F_discretionary']:.1f}", "C - D - E"],
        ["G realisation factor", f"x{c['G_realisation']:.2f}", "measured locally, or 0.85 [P]"],
        ["H queue budget", f"{c['H_budget']:.1f}", "F x G"],
        ["I top-decile reserve", f"-{b['top_decile']:.1f}",
         f"reserved before ranking, cap {q['top_decile_cap']:.1f}h (C31)"],
        ["J risk-allocatable", f"{max(0.0, c['H_budget'] - b['top_decile']):.1f}",
         "H - I — the ranked list is allocated against this"],
    ]))
    o.append(f"  Sub-budgets: must-do {b['must_do']}h · top decile {b['top_decile']}h · "
             f"high-return {b['high_return']}h · maintenance {b['maintenance']}h · "
             f"rot sweep {b['rot']}h")
    if q["stop_rule_fired"]:
        o.append("  ** OVER-COMMITMENT STOP RULE FIRED: must-do + committed meetings exceed "
                 "deployable hours (C).")
        o.append("     Escalate with the capacity stress-test memo; do not present this as a "
                 "prioritisation problem. **")
    o.append("")

    o.append("1. MUST-DO — deadline-driven, off the top")
    o.append(table(["#", "Account", "ARR", "Trigger", "Evidence", "Binding", "Days", "Est h"],
                   [[str(i + 1), a["name"], money(a.get("arr") or 0), a["must_do_triggers"][0][0],
                     a["must_do_triggers"][0][1],
                     str(a["binding_date"] or "—"),
                     str(a["days_to_binding"] if a["days_to_binding"] is not None else "—"),
                     f"{a['hours']:.2f}"]
                    for i, a in enumerate(q["must_do"])]))
    extra = [(a["name"], tr[0]) for a in q["must_do"] for tr in a["must_do_triggers"][1:]]
    if extra:
        o.append("  Additional triggers on the same accounts:")
        for n, tr in extra:
            o.append(f"    {n}: {tr}")
    o.append("")

    o.append("2. TOP DECILE — weekly touch regardless of health (C31)")
    o.append(f"  Membership: top ceil(N/10) by ARR plus any account >= "
             f"{MATERIAL_ARR_SHARE:.0%} of book ARR. Cut-off {money(q['top_decile_cutoff'])}.")
    o.append(table(["#", "Account", "ARR", "% book", "Band", "Since touch", "Touch this week",
                    "Est h", "Covered by"],
                   [[str(i + 1), a["name"], money(a.get("arr") or 0),
                     f"{(a.get('decile_share') or 0) * 100:.1f}%",
                     a.get("risk_band") or "UNKNOWN",
                     str(a["days_since_touch"] if a["days_since_touch"] is not None else "UNKNOWN"),
                     "async check-in" if a in q["top_decile_touch"] else
                     ("carried by a must-do row" if a.get("decile_covered_by") == "must-do block"
                      else "NOT TOUCHED — escalated"),
                     f"{a['decile_touch_hours']:.2f}", a.get("decile_covered_by", "—")]
                    for i, a in enumerate(q["top_decile"])]))
    if q["top_decile_escalated"]:
        o.append("  ** The reserve cap could not fund every member. Each account below is named in")
        o.append("     the escalation block with its ARR and the hours it needs — never dropped. **")
    o.append("  A health band is not a reason to remove a row from this block (C31).")
    o.append("")

    o.append("3. HIGH-RETURN — ranked by return per CSM hour, against line J")
    rows = [[str(i + 1), a["name"], money(a.get("arr") or 0), a["basis"],
             a.get("risk_band") or "—", money(a["value"]), f"{a['urgency']:.2f}",
             f"{a['addressability_mult']:.1f}", f"{a['hours']:.2f}",
             f"{a['rph']:,.0f}", f"{a['running_total']:.2f}"]
            for i, a in enumerate(q["high_return"])]
    rows.append(["—", f"CUT LINE at {q['cut_line_hours']:.2f}h of {b['high_return']:.2f}h "
                      f"(from line J)",
                 "", "", "", "", "", "", "", "", ""])
    o.append(table(["#", "Account", "ARR", "Basis", "Band", "Value", "Urg", "Adr", "Est h",
                    "RPH $/h", "Run h"], rows))
    if q["high_return"]:
        o.append("  Arithmetic, top 3:")
        for a in q["high_return"][:3]:
            o.append(f"    {a['name']}: {money(a['value'])} x {a['urgency']:.2f} x "
                     f"{a['addressability_mult']:.1f} / {a['hours']:.2f}h = "
                     f"{a['rph']:,.0f} $/h   [{a['hours_basis']}]")
    o.append("")

    gated = [a for a in q["high_return"] + q["not_this_week"] + q["must_do"]
             if a.get("expansion_gates") and a.get("expansion_arr")]
    if gated:
        o.append("  Expansion health gate — accounts excluded from the expansion basis:")
        o.append(table(["Account", "Expansion ARR", "Gate"],
                       [[a["name"], money(float(a["expansion_arr"])), "; ".join(a["expansion_gates"])]
                        for a in gated]))

    if q["skipped_for_size"]:
        o.append("  Skipped for size — higher return per hour than work above the cut line, but")
        o.append("  too large for the remaining budget. Stage the play, or displace committed work:")
        o.append(table(["Account", "ARR", "Band", "RPH $/h", "Est h", "Budget left"],
                       [[a["name"], money(a.get("arr") or 0), a.get("risk_band") or "—",
                         f"{a['rph']:,.0f}", f"{a['hours']:.2f}",
                         f"{b['high_return'] - q['cut_line_hours']:.2f}"]
                        for a in q["skipped_for_size"]]))

    o.append("4. MAINTENANCE — cadence touches owed")
    o.append(table(["#", "Account", "Segment", "Due since", "Touch h", "Run h"],
                   [[str(i + 1), a["name"], a.get("segment", "—"), str(a.get("cadence_due_since")),
                     f"{a['maintenance_hours']:.2f}", f"{a['running_total']:.2f}"]
                    for i, a in enumerate(q["maintenance"])]))
    o.append("")

    o.append("5. ROT SWEEP")
    o.append(table(["Account", "ARR", "Since touch", "Since activity", "Owner", "Defer",
                    "Filters fired", "In queue"],
                   [[a["name"], money(a.get("arr") or 0),
                     str(a["days_since_touch"] if a["days_since_touch"] is not None else "UNKNOWN"),
                     str(a["days_since_activity"] if a["days_since_activity"] is not None else "UNKNOWN"),
                     a.get("owner_csm") or "UNOWNED", str(a.get("deferral_count", 0)),
                     "; ".join(a["rot_flags"]),
                     "yes" if a.get("rot_hours") else "no"]
                    for a in _rot_display(q)]))
    o.append("")

    o.append("6. DELIBERATELY NOT THIS WEEK (R14 · C32)")
    o.append(table(["Account", "ARR", "Band", "RPH $/h", "Defer", "Why not", "Displaced by",
                    "Next review"],
                   [[a["name"], money(a.get("arr") or 0), a.get("risk_band") or "—",
                     f"{a['rph']:,.0f}" if a.get("rph") else "unrankable",
                     str(a.get("deferral_count", 0)),
                     "below the cut line" if a.get("rph") else
                     a.get("value_note", "unrankable"),
                     a["displaced_by"], a["next_review"]]
                    for a in sorted(q["not_this_week"],
                                    key=lambda x: -(x["rph"] or 0))]))
    o.append(f"  ARR deliberately not covered: {money(t['arr_not_touched'])} across "
             f"{t['accounts_written_off']} accounts.")
    o.append(f"  Reconciliation{'' if t['reconciles'] else ' FAILED — an account is listed nowhere'}: {t['accounts_worked']} worked + {t['accounts_written_off']} "
             f"written off = {t['accounts']} of {t['accounts']} accounts in the book.")
    forced = [a for a in q["not_this_week"]
              if int(a.get("deferral_count", 0) or 0) >= DEFERRAL_FORCE_AT - 1]
    if forced:
        o.append(f"  Approaching the forced-decision threshold (deferral >= {DEFERRAL_FORCE_AT - 1}):")
        for a in forced:
            o.append(f"    {a['name']} — deferral {a.get('deferral_count')}. Next week it must "
                     "become a booked checkpoint or a written demotion.")
    o.append("")

    if q["unrankable"]:
        o.append("7. UNRANKABLE — insufficient data to score. Not the same as low priority.")
        o.append(table(["Account", "ARR", "Missing"],
                       [[a["name"], money(a.get("arr") or 0),
                         a.get("value_note", "UNKNOWN")] for a in q["unrankable"]]))
        o.append("")

    if q["escalation_candidates"]:
        o.append("8. ESCALATION CANDIDATES — take the decision to a manager, with options")
        o.append(table(["Account", "ARR", "Band", "Why it needs a decision"],
                       [[a["name"], money(a.get("arr") or 0), a.get("risk_band") or "—",
                         "; ".join(reasons)] for a, reasons in q["escalation_candidates"]]))
        o.append("  Escalate the decision, not the problem: ask, dollars, date, options,")
        o.append("  recommendation. See SKILL.md Step 8.\n")

    o.append("NOTES")
    o.append("  · RPH ranks work under a capacity constraint. It is NOT revenue protected and")
    o.append("    NOT a forecast. Band midpoints are stated probabilities of a rules-based model.")
    o.append("  · Every play duration includes pull, prep, delivery, follow-up and write-up.")
    o.append("  · Nulls are reported as UNKNOWN, never scored as zero risk, and an unmeasured")
    o.append("    last touch sorts as the longest silence in the top-decile block.")
    o.append("  · Add the seven-family Coverage Ledger and a confidence cap before publishing.")
    return "\n".join(o)


def explain(q: dict[str, Any], account_id: str) -> str:
    pool = (q["must_do"] + q["top_decile"] + q["high_return"] + q["maintenance"]
            + q["not_this_week"] + q["unrankable"])
    for a in pool:
        if a["account_id"] == account_id or a["name"] == account_id:
            o = [f"{a['name']} ({a['account_id']})", ""]
            o.append(f"  ARR                 {money(a.get('arr') or 0)}")
            o.append(f"  Segment / coverage  {a.get('segment')} / {a.get('coverage_model', '—')}")
            o.append(f"  Renewal             {a.get('renewal_date') or 'UNKNOWN'}")
            o.append(f"  Notice period       {a.get('notice_period_days', 'UNKNOWN')} d")
            o.append(f"  Opt-out deadline    {a['opt_out_deadline'] or a.get('opt_out_note')}")
            o.append(f"  Days to opt-out     {a['days_to_opt_out']}")
            o.append(f"  Binding date        {a['binding_date']} ({a['days_to_binding']} d)")
            o.append(f"  Risk band           {a.get('risk_band') or 'UNKNOWN'}")
            if a.get("decile_member"):
                o.append(f"  Top decile (C31)    yes — {a.get('decile_covered_by')}; "
                         f"touch costed at {a['decile_touch_hours']:.2f}h")
            o.append(f"  Basis               {a['basis']}")
            if a["value"] is not None:
                o.append(f"  Value               {money(a['value'])}")
                o.append(f"  Urgency             x{a['urgency']:.2f}")
                o.append(f"  Addressability      x{a['addressability_mult']:.1f} ({a['addressability']})")
                o.append(f"  Hours               {a['hours']:.2f}  [{a['hours_basis']}]")
                o.append(f"  RPH                 {money(a['value'])} x {a['urgency']:.2f} x "
                         f"{a['addressability_mult']:.1f} / {a['hours']:.2f} = "
                         f"{a['rph']:,.0f} $/h")
            else:
                o.append(f"  Value               {a.get('value_note')}")
            if a["must_do_triggers"]:
                o.append("  Must-do triggers:")
                for tr in a["must_do_triggers"]:
                    o.append(f"    - {tr[0]}  [{tr[1]}]")
            if a.get("expansion_gates"):
                o.append(f"  Expansion gated by: {'; '.join(a['expansion_gates'])}")
            if a["rot_flags"]:
                o.append(f"  Rot flags:          {'; '.join(a['rot_flags'])}")
            return "\n".join(o)
    return f"No account matching '{account_id}'."


def main() -> int:
    p = argparse.ArgumentParser(description="Capacity-constrained book triage.")
    p.add_argument("book", help="JSON book of accounts")
    p.add_argument("--json", action="store_true", help="emit the queue as JSON")
    p.add_argument("--explain", metavar="ACCOUNT", help="show the arithmetic for one account")
    args = p.parse_args()

    with open(args.book, encoding="utf-8") as fh:
        book = json.load(fh)

    q = build_queue(book)

    if args.explain:
        print(explain(q, args.explain))
    elif args.json:
        print(json.dumps(q, indent=2, default=str))
    else:
        print(render(q))
    return 0


if __name__ == "__main__":
    sys.exit(main())
