#!/usr/bin/env python3
"""
Compute the onboarding gates, the backwards schedule, float, and the ten stall signals.

The two numbers this skill exists to produce — the value gate and the float — are arithmetic,
and arithmetic done in prose is arithmetic done wrong. This script does it deterministically so
the model spends its attention on the judgement calls instead: where the gate belongs, what
counts as evidence the customer got what they bought, and which conversation to have when float
goes negative.

    python3 onboarding_plan.py --demo                 # worked example, human-readable
    python3 onboarding_plan.py account.json           # your account
    python3 onboarding_plan.py account.json --json    # machine-readable, for the artifact
    python3 onboarding_plan.py --schema               # print the input schema and exit

Standard library only. No network. Never mutates the input file.

Design rules, in order of importance:

1.  A missing input is never guessed. Anything absent comes back as `UNKNOWN — requires <x>`
    and, where it gates a number, that number is withheld rather than estimated.
2.  A signal that cannot be computed is `NOT-CHECKABLE`, never `CLEAR`. `NULL` is a coverage
    gap; `0` core actions on day 70 of a live environment is a finding. They are not the same
    value and the script refuses to conflate them.
3.  Every threshold is a practitioner planning figure `[P]`, not a benchmark. Override them
    from your own cohort history the moment you have 20+ completed implementations.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Any

# ======================================================================================
# Planning constants — all `[P]` practitioner figures. Override per-account in the input.
# ======================================================================================

# Calendar days of value evidence needed before the customer's renewal decision.
EVIDENCE_WINDOW = {"white-glove": 90, "guided": 60, "tech-touch": 30, "recovery": 90}

# Calendar days from production go-live to the activation event recurring at its natural
# cadence. Floor only — a monthly close cycle needs two cycles, so 60+, not 21.
VALUE_LAG = {"white-glove": 21, "guided": 14, "tech-touch": 7, "recovery": 21}

# The first renewal is decided in months two to four of the first term, not at T-90. Days from
# contract_start. `[P]` — replace with your own first-term cohort history at 20+ first renewals.
DECISION_WINDOW_OPEN_DAYS = 30
DECISION_WINDOW_CLOSE_DAYS = 120

# Business days per phase, by mode. Phase 7 is the value gate itself and has no duration.
PHASE_NAMES = [
    "Pre-kickoff", "Kickoff", "Configuration", "Integration", "Data migration",
    "Admin enablement", "End-user enablement", "First value (V-day)",
    "Usage expansion", "Steady-state handover",
]
PHASE_DAYS = {
    "white-glove": [5, 1, 15, 20, 15, 5, 10, 0, 20, 5],
    "guided":      [3, 1, 8, 10, 5, 3, 5, 0, 15, 3],
    "tech-touch":  [1, 1, 3, 0, 2, 1, 2, 0, 10, 1],
    "recovery":    [3, 1, 10, 12, 8, 4, 6, 0, 15, 4],
}

# Phases 2, 3 and 4 run concurrently only if the customer has a separate owner for each.
PARALLEL_BLOCK = [2, 3, 4]

# Phases on the critical path to go-live (G-day). 7 onwards sit after it.
PATH_TO_GOLIVE = [0, 1, 2, 3, 4, 5, 6]

FLOAT_BANDS = [
    (20, "Healthy", "Proceed; re-check float weekly"),
    (5, "Tight", "Remove one non-critical phase from the path, or add a customer owner. Name which"),
    (0, "No absorption", "Any single slip breaks it. Escalate to the exec sponsor now, "
                         "naming the dependency you need unblocked"),
]
NEGATIVE_BAND = ("NEGATIVE", "The plan does not fit. Say so in the first five lines and choose "
                             "explicitly: cut scope, move the gate, or accept a first renewal "
                             "decided without value evidence")

UNKNOWN = "UNKNOWN"


# ======================================================================================
# Date arithmetic
# ======================================================================================

def parse_date(value: Any) -> date | None:
    if value in (None, "", UNKNOWN):
        return None
    if isinstance(value, date):
        return value
    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y", "%d %b %Y", "%d %B %Y"):
        try:
            return datetime.strptime(str(value).strip(), fmt).date()
        except ValueError:
            continue
    raise ValueError(f"unparseable date: {value!r} — use YYYY-MM-DD")


def add_business_days(start: date, n: int) -> date:
    """Add n business days (Mon–Fri). Negative n walks backwards."""
    step = 1 if n >= 0 else -1
    remaining, cursor = abs(n), start
    while remaining:
        cursor += timedelta(days=step)
        if cursor.weekday() < 5:
            remaining -= 1
    return cursor


def business_days_between(a: date, b: date) -> int:
    """Signed business days from a to b. Negative when b is before a."""
    if b < a:
        return -business_days_between(b, a)
    days, cursor = 0, a
    while cursor < b:
        cursor += timedelta(days=1)
        if cursor.weekday() < 5:
            days += 1
    return days


def iso(d: date | None) -> str:
    return d.isoformat() if d else f"{UNKNOWN} — requires the input field"


# ======================================================================================
# Step 1 — anchor the value gate
# ======================================================================================

def anchor_gates(a: dict) -> dict:
    """V-day and G-day, with every intermediate shown so a reviewer can audit the arithmetic."""
    mode = a.get("mode", "guided")
    out: dict[str, Any] = {"mode": mode, "unknowns": []}

    renewal = parse_date(a.get("renewal_date"))
    notice = a.get("notice_period_days")
    start = parse_date(a.get("contract_start"))
    target_ttfv = a.get("target_ttfv_days")

    evidence_window = a.get("evidence_window_days") or EVIDENCE_WINDOW.get(mode, 60)
    value_lag = a.get("value_lag_days") or VALUE_LAG.get(mode, 14)
    out["evidence_window_days"] = evidence_window
    out["value_lag_days"] = value_lag

    if not a.get("activation_event"):
        out["unknowns"].append(
            "activation_event — requires cs-context §5 or the customer's own success criterion. "
            "Without it there is no finish line to plan backwards from; derive it "
            "(references/phase-playbook.md §7) before laying any date."
        )
    out["activation_event"] = a.get("activation_event") or UNKNOWN

    opt_out = None
    if renewal and notice not in (None, "", UNKNOWN):
        opt_out = renewal - timedelta(days=int(notice))
    else:
        out["unknowns"].append(
            "opt_out_deadline — requires renewal_date and notice_period_days from the executed "
            "contract. Planning to the renewal date targets a decision that has already been made."
        )
    out["renewal_date"] = iso(renewal)
    out["notice_period_days"] = notice if notice is not None else UNKNOWN
    out["opt_out_deadline"] = iso(opt_out)

    # The renewal decision forms in months 2-4. Compute the window, never leave it to memory.
    dw_close = None
    if start:
        dw_close = start + timedelta(days=DECISION_WINDOW_CLOSE_DAYS)
        out["decision_window_open"] = iso(start + timedelta(days=DECISION_WINDOW_OPEN_DAYS))
        out["decision_window_close"] = iso(dw_close)
    else:
        out["decision_window_open"] = UNKNOWN
        out["decision_window_close"] = UNKNOWN
        out["unknowns"].append(
            "decision_window — requires contract_start. Without it there is no way to say whether "
            "the first renewal is decided before or after value exists."
        )
    out["decision_window_verdict"] = UNKNOWN

    candidates = []
    if opt_out:
        candidates.append(("opt_out − evidence_window", opt_out - timedelta(days=evidence_window)))
    if start and target_ttfv not in (None, "", UNKNOWN):
        candidates.append(("contract_start + target_ttfv", start + timedelta(days=int(target_ttfv))))
    if not candidates:
        out["unknowns"].append(
            "value_gate — requires either (renewal_date + notice_period_days) or "
            "(contract_start + target_ttfv_days). No gate is computed; none is invented."
        )
        out["v_day"] = None
        out["g_day"] = None
        out["v_day_basis"] = UNKNOWN
        return out

    basis, v_day = min(candidates, key=lambda c: c[1])
    out["v_day"] = v_day
    out["v_day_basis"] = basis
    out["v_day_candidates"] = {k: iso(v) for k, v in candidates}
    out["g_day"] = v_day - timedelta(days=value_lag)

    if dw_close:
        if v_day <= dw_close:
            out["decision_window_verdict"] = (
                "DECIDED ON EVIDENCE — V-day lands on or before the close of the window, so the "
                "renewal view forms with the activation event already recurring"
            )
        else:
            out["decision_window_verdict"] = (
                f"DECIDED ON FAITH — V-day is {(v_day - dw_close).days}d past the close of the "
                "window, so the customer forms their renewal view before value exists. Say so in "
                "the first five lines and name the choice: cut scope, move the gate, or accept a "
                "first renewal argued without evidence — with an owner and a date"
            )
    return out


# ======================================================================================
# Step 4 / 5 — backwards schedule and forward feasibility
# ======================================================================================

def schedule(a: dict, gates: dict) -> dict:
    """Lay the phases back from G-day, then run them forwards from today and compare."""
    mode = gates["mode"]
    durations = list(a.get("phase_days") or PHASE_DAYS.get(mode, PHASE_DAYS["guided"]))
    owners = int(a.get("customer_owner_count") or 1)
    completed = set(a.get("phases_complete") or [])
    parallel = owners >= 3 and not a.get("force_serial")

    block = [durations[i] for i in PARALLEL_BLOCK]
    block_days = max(block) if parallel else sum(block)

    def path_days(skip_complete: bool) -> int:
        total = 0
        for i in PATH_TO_GOLIVE:
            if skip_complete and i in completed:
                continue
            if i in PARALLEL_BLOCK:
                continue
            total += durations[i]
        if not (skip_complete and set(PARALLEL_BLOCK) <= completed):
            remaining = [durations[i] for i in PARALLEL_BLOCK
                         if not (skip_complete and i in completed)]
            total += (max(remaining) if parallel else sum(remaining)) if remaining else 0
        return total

    full_path = path_days(False)
    remaining_path = path_days(True)

    out: dict[str, Any] = {
        "parallelism": "assumed" if parallel else "not assumed",
        "parallelism_reason": (
            f"{owners} named customer owners — configuration, integration and migration can run "
            f"concurrently" if parallel else
            f"{owners} named customer owner(s) — a single owner serialises configuration, "
            f"integration and migration, which typically triples the critical path"
        ),
        "critical_path_days_full": full_path,
        "critical_path_days_remaining": remaining_path,
        "phases_complete": sorted(completed),
        "block_days": block_days,
    }

    g_day = gates.get("g_day")
    if not g_day:
        out["float_days"] = None
        out["float_band"] = UNKNOWN
        out["float_action"] = "No gate computed — no float can be stated. Do not estimate one."
        out["phases"] = []
        return out

    # Backwards schedule: lay each phase back from G-day in reverse path order.
    phases, cursor = [], g_day
    for i in reversed(PATH_TO_GOLIVE):
        if i in PARALLEL_BLOCK and parallel:
            end, start_d = cursor, add_business_days(cursor, -durations[i])
            if i == PARALLEL_BLOCK[0]:
                cursor = add_business_days(cursor, -block_days)
        else:
            end, start_d = cursor, add_business_days(cursor, -durations[i])
            cursor = start_d
        phases.append({
            "n": i, "phase": PHASE_NAMES[i], "days": durations[i],
            "start": iso(start_d), "end": iso(end),
            "parallel": i in PARALLEL_BLOCK and parallel,
            "complete": i in completed,
        })
    phases.reverse()
    for i in (7, 8, 9):
        anchor = gates["v_day"]
        phases.append({
            "n": i, "phase": PHASE_NAMES[i], "days": durations[i],
            "start": iso(anchor), "end": iso(anchor + timedelta(days=30 * (i - 7))),
            "parallel": False, "complete": i in completed,
        })
    out["phases"] = phases
    out["plan_start"] = iso(cursor)

    today = parse_date(a.get("as_of")) or date.today()
    available = business_days_between(today, g_day)
    float_days = available - remaining_path
    out["as_of"] = iso(today)
    out["business_days_to_g_day"] = available
    out["float_days"] = float_days
    out["projected_g_day"] = iso(add_business_days(today, remaining_path))

    if float_days < 0:
        out["float_band"], out["float_action"] = NEGATIVE_BAND
    else:
        for threshold, band, action in FLOAT_BANDS:
            if float_days >= threshold:
                out["float_band"], out["float_action"] = band, action
                break
    return out


# ======================================================================================
# Step 7 — the ten stall signals
# ======================================================================================

FIRED, CLEAR, NOT_CHECKABLE = "FIRED", "CLEAR", "NOT-CHECKABLE"


def _sig(n: str, name: str, value: Any, threshold: str, status: str,
         escalation: str, note: str = "") -> dict:
    return {"id": n, "signal": name, "value": value, "threshold": threshold,
            "status": status, "escalation": escalation, "note": note}


def stall_signals(a: dict, gates: dict, sched: dict) -> list[dict]:
    """All ten, every time. Missing inputs come back NOT-CHECKABLE, never CLEAR."""
    o = a.get("observed") or {}
    mode = gates["mode"]
    today = parse_date(a.get("as_of")) or date.today()
    start = parse_date(a.get("contract_start"))
    golive = parse_date(a.get("actual_go_live"))
    out: list[dict] = []

    def missing(n, name, field, escalation):
        return _sig(n, name, f"{UNKNOWN} — requires {field}", "—", NOT_CHECKABLE, escalation,
                    "A signal that cannot be computed is not a clear signal.")

    # S1 milestone slippage
    overdue, slip = o.get("milestones_overdue"), o.get("cumulative_slip_days")
    esc = "Re-plan with the customer, in writing, within 5 business days"
    if overdue is None or slip is None:
        out.append(missing("S1", "Milestone slippage",
                           "milestones_overdue and cumulative_slip_days", esc))
    else:
        fired = overdue >= 2 or slip > 30
        out.append(_sig("S1", "Milestone slippage", f"{overdue} overdue · {slip}d cumulative slip",
                        "≥2 overdue or >30d cumulative [P]", FIRED if fired else CLEAR, esc))

    # S2 TTFV overrun
    target = a.get("target_ttfv_days")
    esc = "Severe: exec-sponsored recovery with a re-baselined go-live and a named cause"
    if not start or target in (None, "", UNKNOWN):
        out.append(missing("S2", "TTFV overrun", "contract_start and target_ttfv_days", esc))
    else:
        elapsed = (today - start).days
        ratio = elapsed / int(target) if int(target) else 0
        value_seen = bool(o.get("activation_event_observed"))
        severe = ratio > 2.0 or (elapsed > 90 and not value_seen)
        fired = ratio > 1.5 or severe
        out.append(_sig("S2", "TTFV overrun", f"{elapsed}d elapsed / {target}d target = {ratio:.2f}×",
                        ">1.5× risk · >2.0× severe · no value event by d90 severe [P]",
                        FIRED if fired else CLEAR, esc, "SEVERE" if severe else ""))

    # S3 blocked-task ownership
    cust, tot = o.get("overdue_tasks_customer_side"), o.get("overdue_tasks_total")
    esc = "Escalate to the exec sponsor with the named blocker — never to the person being blocked"
    if cust is None or not tot:
        out.append(missing("S3", "Blocked-task ownership",
                           "overdue_tasks_customer_side and overdue_tasks_total", esc))
    else:
        share = cust / tot
        weeks = o.get("weeks_customer_side_majority", 0)
        fired = share >= 0.60 and weeks >= 2
        out.append(_sig("S3", "Blocked-task ownership",
                        f"{cust}/{tot} customer-side = {share:.0%} for {weeks} week(s)",
                        "≥60% customer-side for 2 consecutive weeks",
                        FIRED if fired else CLEAR, esc))

    # S4 unresponsive admin
    days_since = o.get("days_since_bilateral_touch")
    limit = {"white-glove": 10, "guided": 10, "tech-touch": 21, "recovery": 10}.get(mode, 10)
    esc = "Multithread the same week — the sponsor and a second named contact"
    if days_since is None:
        out.append(missing("S4", "Unresponsive admin",
                           "days_since_bilateral_touch (exclude one-way vendor outbound)", esc))
    else:
        out.append(_sig("S4", "Unresponsive admin", f"{days_since} business days",
                        f"{limit}d for {mode} [P]", FIRED if days_since > limit else CLEAR, esc))

    # S5 environment never in production
    prod, tot_ev = o.get("prod_events"), o.get("total_events")
    esc = "Technical escalation; treat go-live as not achieved regardless of project status"
    if prod is None or tot_ev is None:
        out.append(missing("S5", "Environment never in production",
                           "prod_events and total_events", esc))
    elif not tot_ev:
        out.append(_sig("S5", "Environment never in production", "0 events of any kind",
                        "<0.20 prod share after d90 [P]", FIRED, esc,
                        "Zero total events — read with S6."))
    else:
        share = prod / tot_ev
        past90 = bool(golive and (today - golive).days > 90)
        out.append(_sig("S5", "Environment never in production",
                        f"{prod}/{tot_ev} in production = {share:.0%}"
                        + (f" · {(today - golive).days}d post-go-live" if golive else ""),
                        "<0.20 after day 90 post-go-live [P]",
                        FIRED if (share < 0.20 and past90) else CLEAR, esc,
                        "" if golive else "go-live date absent — threshold applied on share only"))

    # S6 dark account
    core = o.get("core_events_since_start")
    esc = "Same-week exec-to-exec. Highest-precision signal in the set"
    if core is None or not start:
        out.append(missing("S6", "Dark account",
                           "core_events_since_start and contract_start", esc))
    else:
        elapsed = (today - start).days
        out.append(_sig("S6", "Dark account", f"{core} core events in {elapsed}d since start",
                        "0 events >60d from contract start [P] · near-certain",
                        FIRED if (core == 0 and elapsed > 60) else CLEAR, esc))

    # S7 no new users provisioned
    new_users, util = o.get("new_users_l30"), o.get("seat_utilisation")
    esc = "To the rollout owner, naming the team that has not started and its lead"
    if new_users is None or util is None:
        out.append(missing("S7", "No new users provisioned",
                           "new_users_l30 and seat_utilisation", esc))
    else:
        out.append(_sig("S7", "No new users provisioned",
                        f"{new_users} new users L30 · utilisation {util:.0%}",
                        "0 new users in 30d while utilisation <0.85",
                        FIRED if (new_users == 0 and util < 0.85) else CLEAR, esc))

    # S8 services burn ratio
    burned, sold = o.get("services_hours_burned"), o.get("services_hours_sold")
    changes = o.get("scope_change_count", 0)
    esc = "Depends on the pairing rule — see the burn/activation read below"
    if burned is None or not sold:
        out.append(missing("S8", "Services burn ratio",
                           "services_hours_burned and services_hours_sold", esc))
    else:
        ratio = burned / sold
        out.append(_sig("S8", "Services burn ratio",
                        f"{burned}/{sold}h = {ratio:.2f}× · {changes} change order(s)",
                        ">1.3× sold hours or ≥2 change orders [P]",
                        FIRED if (ratio > 1.3 or changes >= 2) else CLEAR, esc,
                        "Never read alone."))

    # S9 use case never live
    sold_uc = o.get("sold_use_case_ever_performed")
    esc = "Re-open the Sold-vs-Real table; the recovery is the gap class, not a training session"
    if sold_uc is None:
        out.append(missing("S9", "Use case never live", "sold_use_case_ever_performed", esc))
    else:
        past90 = bool(golive and (today - golive).days > 90)
        out.append(_sig("S9", "Use case never live",
                        "performed" if sold_uc else "never performed",
                        "never, by day 90 post-go-live [P] · near-certain",
                        FIRED if (not sold_uc and past90) else CLEAR, esc,
                        "" if golive else "go-live date absent — cannot apply the day-90 clock"))

    # S10 kickoff-to-config stall
    kickoff, config = parse_date(o.get("kickoff_date")), parse_date(o.get("config_complete_date"))
    default = PHASE_DAYS.get(mode, PHASE_DAYS["guided"])[2]
    esc = "Name the unmade decision and who can make it. More configuration help makes it worse"
    if not kickoff:
        out.append(missing("S10", "Kickoff-to-config stall", "observed.kickoff_date", esc))
    else:
        elapsed_bd = business_days_between(kickoff, config or today)
        out.append(_sig("S10", "Kickoff-to-config stall",
                        f"{elapsed_bd} business days{'' if config else ' and still open'}",
                        f">2× the {mode} default of {default}d",
                        FIRED if elapsed_bd > 2 * default else CLEAR, esc))
    return out


def burn_pairing(signals: list[dict], a: dict) -> str:
    """Burn is only interpretable against activation. See references/stall-detection.md §4."""
    o = a.get("observed") or {}
    burned, sold = o.get("services_hours_burned"), o.get("services_hours_sold")
    if burned is None or not sold:
        return f"{UNKNOWN} — requires services_hours_burned and services_hours_sold"
    ratio = burned / sold
    activated = bool(o.get("activation_event_observed"))
    start = parse_date(a.get("contract_start"))
    today = parse_date(a.get("as_of")) or date.today()
    past60 = bool(start and (today - start).days > 60)
    if ratio > 1.3 and activated:
        return "Healthy but unprofitable — a margin and scoping problem, NOT a churn signal"
    if ratio > 1.3 and not activated:
        return "SEVERE — money spent, no outcome. Candidate for the Failed launch pattern"
    if ratio <= 1.0 and not activated and past60:
        return ("SEVERE AND QUIET — nobody is working the account. Check the vendor-side book "
                "before concluding anything about the customer")
    if ratio <= 1.0 and activated:
        return "Model account — capture the configuration and the sequence; it is reusable"
    return "Within range on both — no pairing read required this week"


def compounds(signals: list[dict]) -> list[dict]:
    fired = {s["id"] for s in signals if s["status"] == FIRED}
    unknown = {s["id"] for s in signals if s["status"] == NOT_CHECKABLE}
    defs = [
        ("Failed launch", {"S2", "S1", "S8", "S6"},
         "180–365d, predicting the FIRST renewal — exec-sponsored recovery with a re-baselined "
         "go-live. Consider a term restart, not a renewal ask"),
        ("Pilot trap", {"S7", "S9"},
         "90–180d — the rollout owner, the named next team, and a dated session"),
        ("Phantom go-live", {"S5"},
         "Immediate — recompute float with go-live unachieved and correct the project record"),
        ("Quiet abandonment", {"S4", "S3"},
         "60–120d — multithread, and check the vendor-side book"),
        ("Decision deadlock", {"S10", "S3"},
         "30–90d — name the unmade decision and who can make it"),
    ]
    out = []
    for name, need, play in defs:
        blocked = sorted(need & unknown)
        out.append({
            "pattern": name,
            "matched": need <= fired,
            "requires": sorted(need),
            "not_checkable": blocked,
            "play": play,
        })
    return out


# ======================================================================================
# The first-renewal risk record — opens at the value gate, never at go-live
# ======================================================================================

STATE_OBLIGATION = {
    "VALUED": "Steady-state handover proceeds. Expansion unblocks from here, subject to R8 and R9",
    "LIVE, NOT VALUED": "Onboarding does NOT close. The account stays with the onboarding lead; "
                        "re-date the gate once, in writing, with the cause named, and ask the "
                        "customer's business owner for the attestation criterion directly",
    "NOT LIVE": "Exec-sponsored recovery. Run the Failed-launch test before any renewal or "
                "expansion motion",
    "NOT YET REACHED": "The record is scheduled to open on V-day. Nothing opens at G-day",
}


def risk_record(a: dict, gates: dict, signals: list[dict], comps: list[dict]) -> dict:
    """The account's first-renewal risk record.

    It opens at the value gate, never at go-live. They are different events with different
    owners and different evidence, and conflating them is why implementations delivered on
    time churn at the first renewal. Full contract: references/first-renewal.md.
    """
    o = a.get("observed") or {}
    v_day, g_day = gates.get("v_day"), gates.get("g_day")
    today = parse_date(a.get("as_of")) or date.today()
    attested = bool(o.get("value_gate_attested"))
    live = bool(parse_date(a.get("actual_go_live")))
    notes: list[str] = []

    if attested and o.get("activation_event_observed"):
        state = "VALUED"
    elif v_day and today >= v_day:
        state = "LIVE, NOT VALUED" if live else "NOT LIVE"
    elif v_day:
        state = "NOT YET REACHED"
    else:
        state = UNKNOWN

    if state == "VALUED":
        opened_at = o.get("value_gate_attested_on") or iso(v_day)
    elif state == UNKNOWN:
        opened_at = f"{UNKNOWN} — requires the value gate; a record cannot open on G-day"
    else:
        opened_at = iso(v_day)

    if g_day and v_day and v_day != g_day and opened_at == iso(g_day):
        notes.append("opened_at equals G-day — go-live is not the value gate. Re-date the record "
                     "to the V-day event, or fix the plan that made the two dates coincide")
    if state == "LIVE, NOT VALUED":
        notes.append("Live on the vendor's task list, unvalued on the customer's. This is the "
                     "state that reads as a successful implementation and churns at renewal #1")

    failed = next((c for c in comps if c["pattern"] == "Failed launch"), None)
    handoff = ["churn-risk"]
    payload = None
    if failed and failed["matched"]:
        handoff.append("save-play")
        payload = {
            "pattern": "Failed launch (P0)",
            "signals": {s["id"]: s["value"] for s in signals
                        if s["id"] in ("S2", "S1", "S8", "S6")},
            "churn_risk_codes": "S2 -> U9 · S1 -> U10 · S8 -> U11 · S6 -> Z4",
            "lead_time": "180-365 days to the first renewal decision",
            "decision_date": gates.get("opt_out_deadline"),
            "account_state": state,
            "play": "Exec-sponsored recovery with a re-baselined go-live and a stated cause. "
                    "Consider a term restart or extension, not a renewal ask",
            "withheld": "renewal motion · expansion ask (R8) — state the reason, never omit it",
        }

    return {
        "opens_at_rule": "the V-day event date — attested, or V-day passed unattested. Never G-day",
        "opened_at": opened_at,
        "opening_state": state,
        "obligation": STATE_OBLIGATION.get(state, UNKNOWN),
        "record_owner": a.get("record_owner") or f"{UNKNOWN} — requires a named person, not a team",
        "first_renewal_decision_date": gates.get("opt_out_deadline") or UNKNOWN,
        "decision_window": f"{gates.get('decision_window_open')} -> "
                           f"{gates.get('decision_window_close')}",
        "decision_window_verdict": gates.get("decision_window_verdict", UNKNOWN),
        "onboarding_closed": state == "VALUED",
        "expansion_gate": "OPEN (subject to R8, R9)" if state == "VALUED"
                          else "BLOCKED until the record reads VALUED (R8) — state the withholding",
        "handoff_to": handoff,
        "failed_launch_handoff": payload,
        "notes": notes,
    }


# ======================================================================================
# Reporting
# ======================================================================================

def build(a: dict) -> dict:
    gates = anchor_gates(a)
    sched = schedule(a, gates)
    signals = stall_signals(a, gates, sched)
    comps = compounds(signals)
    return {
        "account": a.get("account_name", UNKNOWN),
        "as_of": sched.get("as_of", iso(parse_date(a.get("as_of")) or date.today())),
        "gates": {**gates, "v_day": iso(gates.get("v_day")), "g_day": iso(gates.get("g_day"))},
        "schedule": sched,
        "signals": signals,
        "burn_pairing": burn_pairing(signals, a),
        "compounds": comps,
        "risk_record": risk_record(a, gates, signals, comps),
        "unknowns": gates["unknowns"],
    }


def render(r: dict) -> str:
    g, s = r["gates"], r["schedule"]
    L = [f"ONBOARDING PLAN — {r['account']} · {g['mode']} · as of {r['as_of']}", "=" * 78, ""]
    L += ["ANCHOR ARITHMETIC",
          f"  activation event      {g['activation_event']}",
          f"  renewal_date          {g['renewal_date']}",
          f"  notice_period_days    {g['notice_period_days']}",
          f"  opt_out_deadline      {g['opt_out_deadline']}",
          f"  evidence_window       {g['evidence_window_days']}d [P]",
          f"  VALUE GATE (V-day)    {g['v_day']}   basis: {g.get('v_day_basis')}",
          f"  value_lag             {g['value_lag_days']}d [P]",
          f"  GO-LIVE (G-day)       {g['g_day']}",
          f"  decision window       {g.get('decision_window_open')} -> "
          f"{g.get('decision_window_close')}  (months 2-4) [P]",
          f"  verdict               {g.get('decision_window_verdict')}", ""]
    if g.get("v_day_candidates"):
        L.append("  candidates: " + " · ".join(f"{k} = {v}" for k, v in g["v_day_candidates"].items()))
        L.append("")
    L += ["FEASIBILITY",
          f"  parallelism           {s['parallelism']} — {s['parallelism_reason']}",
          f"  critical path (full)  {s['critical_path_days_full']} business days",
          f"  remaining             {s['critical_path_days_remaining']} business days",
          f"  available to G-day    {s.get('business_days_to_g_day', UNKNOWN)} business days",
          f"  FLOAT                 "
          f"{s['float_days'] if s.get('float_days') is not None else UNKNOWN}"
          f"  → {s.get('float_band')}",
          f"  action                {s.get('float_action')}", ""]
    if s.get("phases"):
        L.append("BACKWARDS SCHEDULE (laid from G-day)")
        L.append(f"  {'#':<3}{'phase':<26}{'start':<13}{'end':<13}{'days':<6}flags")
        for p in s["phases"]:
            flags = " ".join(x for x in ("‖" if p["parallel"] else "",
                                         "done" if p["complete"] else "") if x)
            L.append(f"  {p['n']:<3}{p['phase']:<26}{p['start']:<13}{p['end']:<13}"
                     f"{p['days']:<6}{flags}")
        L.append("")
    L.append("STALL SIGNALS (all ten, every time)")
    for sig in r["signals"]:
        L.append(f"  {sig['id']:<4}{sig['status']:<15}{sig['signal']}")
        L.append(f"       {sig['value']}   [{sig['threshold']}]")
        if sig["status"] == FIRED:
            L.append(f"       → {sig['escalation']}")
        if sig["note"]:
            L.append(f"       ! {sig['note']}")
    fired = sum(1 for x in r["signals"] if x["status"] == FIRED)
    nc = sum(1 for x in r["signals"] if x["status"] == NOT_CHECKABLE)
    L += ["", f"  fired {fired}/10 · not-checkable {nc}/10 "
              f"(not-checkable is a coverage gap, not a clear signal)", ""]
    L += ["BURN / ACTIVATION PAIRING", f"  {r['burn_pairing']}", "", "COMPOUND PATTERNS"]
    for c in r["compounds"]:
        state = "MATCHED" if c["matched"] else "not matched"
        blocked = f"  (not-checkable: {', '.join(c['not_checkable'])})" if c["not_checkable"] else ""
        L.append(f"  {c['pattern']:<20}{state}{blocked}")
        if c["matched"]:
            L.append(f"       → {c['play']}")
    rr = r["risk_record"]
    L += ["", "FIRST-RENEWAL RISK RECORD (opens at V-day, never at G-day)",
          f"  opened_at             {rr['opened_at']}",
          f"  opening_state         {rr['opening_state']}",
          f"  obligation            {rr['obligation']}",
          f"  record_owner          {rr['record_owner']}",
          f"  decision date         {rr['first_renewal_decision_date']}  (opt-out, R1)",
          f"  onboarding closed     {'yes' if rr['onboarding_closed'] else 'NO'}",
          f"  expansion             {rr['expansion_gate']}",
          f"  handoff_to            {', '.join(rr['handoff_to'])}"]
    for n in rr["notes"]:
        L.append(f"       ! {n}")
    if rr["failed_launch_handoff"]:
        p = rr["failed_launch_handoff"]
        L += ["", "  FAILED-LAUNCH HANDOFF -> churn-risk",
              f"       {p['churn_risk_codes']}",
              f"       lead time {p['lead_time']}, decision {p['decision_date']}",
              f"       {p['play']}",
              f"       withheld: {p['withheld']}"]
    if r["unknowns"]:
        L += ["", "UNKNOWNS — never substituted with a plausible value"]
        L += [f"  - {u}" for u in r["unknowns"]]
    return "\n".join(L)


SCHEMA = """
{
  "account_name": "Northwind",
  "as_of": "2026-08-28",                  // omit to use today
  "mode": "guided",                       // white-glove | guided | tech-touch | recovery
  "contract_start": "2026-07-01",
  "renewal_date": "2027-06-30",
  "notice_period_days": 60,
  "target_ttfv_days": 120,                // cs-context §5
  "activation_event": "monthly close completed in the platform",
  "actual_go_live": null,                 // null until production go-live
  "record_owner": "Priya Raman",          // who owns the first renewal from V-day forward
  "customer_owner_count": 1,              // >=3 permits the parallel config/integration/migration block
  "phases_complete": [0, 1],              // phase numbers already finished
  "evidence_window_days": null,           // override the mode default
  "value_lag_days": null,                 // override; a monthly cycle needs 60+, not 21
  "phase_days": null,                     // override the whole duration vector
  "observed": {
    "milestones_overdue": 3,
    "cumulative_slip_days": 18,
    "activation_event_observed": false,
    "overdue_tasks_customer_side": 7,
    "overdue_tasks_total": 9,
    "weeks_customer_side_majority": 3,
    "days_since_bilateral_touch": 14,
    "prod_events": 0,
    "total_events": 412,
    "core_events_since_start": 0,
    "new_users_l30": 0,
    "seat_utilisation": 0.12,
    "services_hours_burned": 96,
    "services_hours_sold": 80,
    "scope_change_count": 1,
    "sold_use_case_ever_performed": false,
    "value_gate_attested": false,         // only the customer's business owner can set this true
    "value_gate_attested_on": null,       // the attestation date — never the go-live date
    "kickoff_date": "2026-07-14",
    "config_complete_date": null
  }
}

Any field may be omitted or null. Omitted fields produce UNKNOWN or NOT-CHECKABLE, never a guess.
"""

DEMO = {
    "account_name": "Northwind (demo)",
    "as_of": "2026-08-28",
    "mode": "guided",
    "contract_start": "2026-07-01",
    "renewal_date": "2027-06-30",
    "notice_period_days": 60,
    "target_ttfv_days": 120,
    "activation_event": "monthly close completed in the platform, two consecutive cycles",
    "actual_go_live": None,
    "record_owner": "Priya Raman",
    "customer_owner_count": 1,
    "phases_complete": [0, 1],
    "value_lag_days": 60,
    "observed": {
        "milestones_overdue": 3,
        "cumulative_slip_days": 18,
        "activation_event_observed": False,
        "overdue_tasks_customer_side": 7,
        "overdue_tasks_total": 9,
        "weeks_customer_side_majority": 3,
        "days_since_bilateral_touch": 14,
        "prod_events": 0,
        "total_events": 412,
        "core_events_since_start": 0,
        "new_users_l30": 0,
        "seat_utilisation": 0.12,
        "services_hours_burned": 96,
        "services_hours_sold": 80,
        "scope_change_count": 1,
        "sold_use_case_ever_performed": False,
        "value_gate_attested": False,
        "value_gate_attested_on": None,
        "kickoff_date": "2026-07-14",
        "config_complete_date": None,
    },
}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("input", nargs="?", help="account JSON file")
    ap.add_argument("--demo", action="store_true", help="run the worked example")
    ap.add_argument("--schema", action="store_true", help="print the input schema and exit")
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    args = ap.parse_args()

    if args.schema:
        print(SCHEMA.strip())
        return 0
    if args.demo:
        account = DEMO
    elif args.input:
        path = Path(args.input)
        if not path.exists():
            print(f"no such file: {path}", file=sys.stderr)
            return 2
        account = json.loads(path.read_text())
    else:
        ap.print_help()
        return 2

    try:
        report = build(account)
    except ValueError as e:
        print(f"input error: {e}", file=sys.stderr)
        return 2

    print(json.dumps(report, indent=2, default=str) if args.json else render(report))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
