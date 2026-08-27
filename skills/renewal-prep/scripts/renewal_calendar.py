#!/usr/bin/env python3
"""
renewal_calendar.py — deterministic renewal stage-gate calendar, paper critical path,
forecast ceiling, and readiness/MEDDPICC-R scoring for one renewal or a book.

Standard library only. No network. Every figure it prints is arithmetic on inputs you
supply; anything you do not supply is printed as UNKNOWN and excluded from the maths.

THE TWO CLOCKS
--------------
  D = opt_out_deadline = renewal_date - notice_period_days   <- the decision clock
  R = renewal_date                                           <- the paper/term clock

All gates T-180 .. T-0 are offsets from **D**, not from R. T-0 IS the opt-out deadline.
T+7 / T+30 are offsets from R. The span D..R is the "paper runway": contingency, never plan.
Target countersignature by D. An explicit notice_period_days = 0 means D = R and the runway
is zero. An OMITTED notice period is not the same thing: it prints UNKNOWN, D is shown equal
to R as a CEILING, and every gate derived from it is a ceiling too.

USAGE
-----
  python3 renewal_calendar.py --renewal-date 2027-02-01 --notice-days 90 \
      --atr 480000 --segment enterprise --term annual --today 2026-08-27

  python3 renewal_calendar.py --renewal-date 2026-11-30 --notice-days 30 \
      --segment mid_market --readiness 2,1,1,2,0,1,0,2,1,0 \
      --meddpicc 2,1,2,1,0,2,1,2,1

  python3 renewal_calendar.py --batch book.json          # list of account dicts
  python3 renewal_calendar.py --renewal-date ... --json  # machine-readable

  Paper lead times (days) are supplied, not assumed:
      --paper security_review=30,legal_redlines=21,po_issuance=14
  Omitted workstreams print as UNKNOWN and are left out of the critical path,
  which is then reported as a FLOOR, not an estimate.

THE TWO ENTRY CRITERIA THIS SCRIPT ENFORCES
-------------------------------------------
C15 — a verbal yes is not a yes until paper moves. Commit requires at least one
observable paper-process event on record, supplied as event=YYYY-MM-DD:

      --paper-moved security_review=2026-09-04,po_requested=2026-09-19
      --verbal-yes 2026-09-01

  With none supplied the forecast ceiling is capped at Most Likely and the reason
  is printed verbatim as "C15 — verbal only, no paper movement". The one exception
  is --auto-renew true with --notice-confirmed, where the clause is the paper.
  With a verbal yes on record and no movement, days since it are computed: 14 days
  is a risk-register row (cause code `verbal_only`), 21 escalates.

C25 — the renewal is never the year's first commercial conversation:

      --last-commercial-touch 2026-03-12

  Days since are computed. Over 365, or omitted entirely, the T-180 gate fails and
  the script prints the latest date by which the prerequisite commercial-context
  conversation must be held — the T-120 gate date on this account's compression.
"""

import argparse
import json
import sys
from datetime import date, timedelta

# ---------------------------------------------------------------- configuration

# Gate ladder. Offsets are days BEFORE D (the opt-out deadline).
BASE_GATES = [
    (270, "T-270", "Strategic pre-work (multi-year / procurement-heavy only)"),
    (180, "T-180", "Open the renewal record. Baseline value + risk."),
    (150, "T-150", "Book the EBR with the economic buyer."),
    (120, "T-120", "Deliver the EBR. Ask the renewal-intent question. Set the price position."),
    (90,  "T-90",  "Deliver the proposal. Map the paper process. Complete MEDDPICC-R."),
    (75,  "T-75",  "Written confirmation of intent to continue. Courtesy notice-deadline letter."),
    (60,  "T-60",  "Open negotiation. Every objection gets an owner and a date."),
    (45,  "T-45",  "Issue the order form. Route approvals. Lock uplift and term."),
    (30,  "T-30",  "Name the signer. Raise the PO. Re-call anything in Best Case."),
    (14,  "T-14",  "Daily tracking. Validate billing entity and tax details."),
    (7,   "T-7",   "Executive-to-executive if unsigned. Prepare the bridge extension."),
    (0,   "T-0",   "OPT-OUT DEADLINE. Decision locked, or notice served."),
]

POST_GATES = [
    (0,  "R-0",  "Renewal date. Countersign, book, start the new term."),
    (7,  "T+7",  "Reconcile called vs closed against the frozen snapshot."),
    (30, "T+30", "New-term kickoff: reset the success plan, set the next renewal record."),
]

# Compression multipliers applied to the D-clock offsets.
# Source: practitioner convention documented in the library research pack —
# full ladder at ACV >= $100k, ~50% compression for mid-market, automated ladder below.
SEGMENT_COMPRESSION = {
    "enterprise": 1.00,
    "mid_market": 0.50,
    "smb": 0.33,
    "tech_touch": 0.33,
}

TERM_COMPRESSION = {
    "annual": 1.00,
    "multi_year": 1.00,
    "quarterly": 0.35,
    "short_term": 0.35,
    "monthly": 0.00,   # handled separately: rolling 90-day ladder
}

MONTHLY_LADDER = [(90, "T-90"), (60, "T-60"), (30, "T-30"), (14, "T-14"), (7, "T-7"), (0, "T-0")]

# Paper workstreams. chain="serial" items sit on the critical path in this order.
PAPER_WORKSTREAMS = [
    ("security_review",             "serial",   "Security / vendor-risk re-review"),
    ("legal_redlines",              "serial",   "Legal redlines (MSA / DPA / SLA)"),
    ("order_form",                  "serial",   "Order form issued and approved internally"),
    ("signature_workflow",          "serial",   "Customer signature routing"),
    ("po_issuance",                 "serial",   "Requisition -> PO number"),
    ("procurement_portal",          "parallel", "Procurement portal / supplier onboarding"),
    ("vendor_master",               "parallel", "Vendor master, W-9/W-8, bank verification"),
    ("insurance_coi",               "parallel", "Certificates of insurance"),
    ("privacy_review",              "parallel", "Privacy / DPIA / sub-processor approval"),
    ("budget_approval",             "parallel", "Budget line confirmed for the new term"),
    ("tax_entity",                  "parallel", "Tax, entity and e-invoicing setup"),
]

READINESS_DIMENSIONS = [
    "Value evidence captured",
    "Executive sponsor contact (business conversation <=90d)",
    "Multithreading depth",
    "Health band",
    "Budget confirmed for the new term",
    "Decision process mapped",
    "Procurement path known",
    "Competitive position",
    "Uplift justified",
    "Paper path known (legal / security / PO / MSA)",
]

MEDDPICC_ELEMENTS = [
    "M  Metrics (value shown in their numbers)",
    "E  Economic buyer (spoken with <=90d)",
    "DC Decision criteria",
    "DP Decision process",
    "PP Paper process (notice window, signer, cycle time)",
    "I  Identified pain (still owned by someone)",
    "C  Champion (tested, still in role)",
    "Co Competition (named alternative incl. do-nothing)",
    "V  Value realised (usage evidence <=30d)",
]
# Gate indices that must be scored 2 for a Commit call: E, PP, C.
MEDDPICC_HARD_GATES = [1, 4, 6]

# C15 — the closed list of observable paper-process events. Nothing else counts as
# movement, and a verbal yes is not on this list by design. See
# references/paper-process.md §11 for what is and is not evidence for each.
PAPER_MOVEMENT_EVENTS = [
    ("security_review", "Security or vendor-risk re-review started"),
    ("redlines_returned", "Legal redlines returned, or written confirmation of none"),
    ("po_requested", "PO requested or requisition raised"),
    ("vendor_portal", "Vendor portal or supplier record created or refreshed"),
    ("signature_routing", "Order form in their signature routing"),
]

# C25 — a commercial touch older than this, or absent, fails the T-180 gate.
COMMERCIAL_TOUCH_MAX_AGE_DAYS = 365
# C15 — days a verbal yes may sit with no paper movement before it becomes a row.
VERBAL_ONLY_REGISTER_DAYS = 14
VERBAL_ONLY_ESCALATE_DAYS = 21


# ---------------------------------------------------------------- helpers

def parse_date(s):
    y, m, d = (int(p) for p in s.split("-"))
    return date(y, m, d)


def fmt(d):
    return d.isoformat()


def forecast_ceiling(days_to_renewal, auto_renew, notice_confirmed):
    """Max forecast category by time-to-renewal.
    Source: forecast-category ceiling table in the library research pack
    (practitioner governance convention, not a measured benchmark)."""
    if days_to_renewal < 0:
        return "At Risk (past due date, unsigned)"
    if days_to_renewal > 120:
        return "Most Likely"
    if days_to_renewal > 90:
        if auto_renew is True and notice_confirmed:
            return "Commit (auto-renew past the notice window, confirmed)"
        return "Most Likely"
    if days_to_renewal > 45:
        return "Commit (only if all six Commit criteria are evidenced)"
    return "Commit expected — Best Case is not a valid call inside T-45"


def paper_movement(moved, verbal_yes, today, auto_renew, notice_confirmed):
    """C15 — a verbal yes is not a yes until paper moves.

    Returns the full five-row ledger (including the rows that are `no` — the empty
    ledger is the finding), whether the Commit entry criterion is met, and the days a
    verbal yes has sat with no movement."""
    moved = moved or {}
    unknown_keys = [k for k in moved if k not in dict(PAPER_MOVEMENT_EVENTS)]
    rows = []
    for key, label in PAPER_MOVEMENT_EVENTS:
        d = moved.get(key)
        rows.append({"event": key, "label": label,
                     "on_record": bool(d), "date": d or None})
    n = sum(1 for r in rows if r["on_record"])
    clause_is_paper = bool(auto_renew) and bool(notice_confirmed)
    passed = n > 0 or clause_is_paper
    if n > 0:
        reason = "%d paper-movement event(s) on record" % n
    elif clause_is_paper:
        reason = "auto-renew past a confirmed notice window — the clause is the paper that moved"
    else:
        reason = "C15 — verbal only, no paper movement"
    stale_days = None
    if verbal_yes and n == 0 and not clause_is_paper:
        stale_days = (today - parse_date(verbal_yes)).days
    return {"rows": rows, "events_on_record": n, "commit_entry_met": passed,
            "reason": reason, "verbal_yes": verbal_yes,
            "days_verbal_only": stale_days,
            "register_row": stale_days is not None and stale_days >= VERBAL_ONLY_REGISTER_DAYS,
            "escalate": stale_days is not None and stale_days >= VERBAL_ONLY_ESCALATE_DAYS,
            "unrecognised_events": unknown_keys}


def commercial_touch(last_touch, today, D, segment, term):
    """C25 — never let the renewal be the year's first commercial conversation.

    Computes days since the last commercial touch and, where there is none inside
    12 months, the date by which the prerequisite conversation must be held: the
    T-120 gate on this account's compression."""
    comp = SEGMENT_COMPRESSION.get(segment, 1.0) * TERM_COMPRESSION.get(term, 1.0)
    prereq_by = D - timedelta(days=int(round(120 * comp)))
    if not last_touch:
        return {"last_touch": None, "days_since": None, "on_record": False,
                "gate_t180": "FAIL — no commercial touch on record (C25)",
                "prerequisite_required": True, "prerequisite_by": fmt(prereq_by),
                "days_to_prerequisite": (prereq_by - today).days}
    days = (today - parse_date(last_touch)).days
    fresh = days <= COMMERCIAL_TOUCH_MAX_AGE_DAYS
    return {"last_touch": last_touch, "days_since": days, "on_record": True,
            "gate_t180": "PASS" if fresh else
                         "FAIL — last commercial touch %d days ago, over %d (C25)"
                         % (days, COMMERCIAL_TOUCH_MAX_AGE_DAYS),
            "prerequisite_required": not fresh, "prerequisite_by": fmt(prereq_by),
            "days_to_prerequisite": (prereq_by - today).days}


def apply_c15_cap(ceiling, movement):
    """Commit is unavailable on verbal agreement alone, whatever the calendar allows."""
    if movement["commit_entry_met"] or "Commit" not in ceiling:
        return ceiling
    return "Most Likely — capped: C15 — verbal only, no paper movement"


def build_gates(D, R, today, segment, term, strategic=False):
    rows = []
    if term == "monthly":
        for off, label in MONTHLY_LADDER:
            g = D - timedelta(days=off)
            rows.append((label, off, g, "Rolling 90-day cadence — evergreen contract, no ATR event"))
    else:
        comp = SEGMENT_COMPRESSION.get(segment, 1.0) * TERM_COMPRESSION.get(term, 1.0)
        seen = set()
        for off, label, purpose in BASE_GATES:
            if off == 270 and not strategic:
                continue
            c_off = int(round(off * comp))
            if c_off in seen:
                continue
            seen.add(c_off)
            g = D - timedelta(days=c_off)
            shown = label if comp == 1.0 else "%s (compressed to D-%dd)" % (label, c_off)
            rows.append((shown, c_off, g, purpose))
    out = []
    for label, off, g, purpose in rows:
        delta = (g - today).days
        if delta < 0:
            status = "PASSED — audit the exit criteria, this gate may be MISSED"
        elif delta <= 7:
            status = "DUE NOW"
        else:
            status = "open"
        out.append({"gate": label, "offset_days": off, "date": fmt(g),
                    "days_from_today": delta, "status": status, "purpose": purpose})
    for off, label, purpose in POST_GATES:
        g = R + timedelta(days=off)
        out.append({"gate": label, "offset_days": off, "date": fmt(g),
                    "days_from_today": (g - today).days,
                    "status": "open" if g >= today else "PASSED",
                    "purpose": purpose})
    return out


def paper_plan(D, today, leads):
    """Backward plan from D. Serial items chain; parallel items each need their own runway."""
    serial = [w for w in PAPER_WORKSTREAMS if w[1] == "serial"]
    parallel = [w for w in PAPER_WORKSTREAMS if w[1] == "parallel"]

    rows = []
    cum = 0
    for key, _chain, label in reversed(serial):          # walk backwards from D
        lead = leads.get(key)
        if lead is None:
            rows.append({"workstream": label, "chain": "serial", "lead_days": None,
                         "latest_start": "UNKNOWN — requires your measured cycle time",
                         "slack_days": None, "late": None})
            continue
        cum += lead
        ls = D - timedelta(days=cum)
        rows.append({"workstream": label, "chain": "serial", "lead_days": lead,
                     "latest_start": fmt(ls), "slack_days": (ls - today).days,
                     "late": ls < today})
    rows.reverse()
    for key, _chain, label in parallel:
        lead = leads.get(key)
        if lead is None:
            rows.append({"workstream": label, "chain": "parallel", "lead_days": None,
                         "latest_start": "UNKNOWN — requires your measured cycle time",
                         "slack_days": None, "late": None})
            continue
        ls = D - timedelta(days=lead)
        rows.append({"workstream": label, "chain": "parallel", "lead_days": lead,
                     "latest_start": fmt(ls), "slack_days": (ls - today).days,
                     "late": ls < today})

    known = [leads[k] for k, c, _l in serial if k in leads]
    critical_path = sum(known)
    missing = [l for k, c, l in PAPER_WORKSTREAMS if k not in leads]
    return {
        "critical_path_days_floor": critical_path,
        "critical_path_is_floor": bool(missing),
        "unknown_workstreams": missing,
        "days_available_to_D": (D - today).days,
        "slack_days": (D - today).days - critical_path,
        "rows": rows,
    }


def score_block(values, labels, hard_gates=None, commit_min=None):
    total = sum(values)
    out = {"total": total, "max": 2 * len(labels),
           "rows": [{"item": l, "score": v} for l, v in zip(labels, values)]}
    if hard_gates is not None:
        failed = [labels[i] for i in hard_gates if values[i] < 2]
        out["hard_gates_failed"] = failed
    if commit_min is not None:
        gate_ok = not out.get("hard_gates_failed")
        out["commit_eligible"] = (total >= commit_min) and gate_ok
        out["commit_min"] = commit_min
    return out


# ---------------------------------------------------------------- rendering

def render(res):
    L = []
    a = res["anchor"]
    L.append("RENEWAL CALENDAR — %s" % (a.get("account") or "(unnamed account)"))
    L.append("=" * 78)
    L.append("Today                 %s" % a["today"])
    L.append("Renewal date  R       %s   (%+d days)" % (a["renewal_date"], a["days_to_renewal"]))
    if a.get("notice_known", True):
        L.append("Notice period         %s days" % a["notice_days"])
        L.append("Opt-out deadline D    %s   (%+d days)  <-- THE GOVERNING DATE" %
                 (a["opt_out_deadline"], a["days_to_opt_out"]))
        L.append("Paper runway D..R     %d days (contingency, not plan)" % a["notice_days"])
    else:
        L.append("Notice period         UNKNOWN — requires the executed contract")
        L.append("Opt-out deadline D    %s   (%+d days)  <-- CEILING ONLY, NOT THE GOVERNING DATE" %
                 (a["opt_out_deadline"], a["days_to_opt_out"]))
        L.append("Paper runway D..R     UNKNOWN")
        L.append("!! No notice period supplied. D has been set equal to R, which is the LATEST")
        L.append("   D can be — the real one is earlier by the notice period. Every gate below is")
        L.append("   a ceiling, and no Commit call is available until the clause is read.")
    atr = a["atr"]
    L.append("ATR                   %s" % ("$%s" % format(int(atr), ",") if isinstance(atr, (int, float)) else atr))
    L.append("Segment / term        %s / %s" % (a["segment"], a["term"]))
    L.append("Forecast ceiling      %s" % res["forecast_ceiling"])
    if res["forecast_ceiling"] != res.get("forecast_ceiling_by_calendar"):
        L.append("   (calendar alone would allow: %s)" % res["forecast_ceiling_by_calendar"])
    if a["days_to_opt_out"] < 0:
        L.append("!! OPT-OUT DEADLINE HAS PASSED. If no notice was served the term has rolled;")
        L.append("   confirm the new term dates before planning anything else.")
    elif a["days_to_opt_out"] <= 45:
        L.append("!! Opt-out deadline inside 45 days — written confirmation of intent is the")
        L.append("   action with the largest effect on the outcome left on this renewal.")
    ct = res["commercial_touch"]
    L.append("")
    L.append("COMMERCIAL TOUCH ON RECORD (C25)")
    L.append("-" * 78)
    if ct["on_record"]:
        L.append("Last commercial touch %s   (%d days ago)" % (ct["last_touch"], ct["days_since"]))
    else:
        L.append("Last commercial touch NONE ON RECORD — requires an `interaction` with the")
        L.append("                      economic buyer or budget holder on price, term, scope,")
        L.append("                      budget or the contract itself")
    L.append("T-180 gate            %s" % ct["gate_t180"])
    if ct["prerequisite_required"]:
        if ct["days_to_prerequisite"] >= 0:
            L.append("!! PREREQUISITE: a commercial-context conversation must be held by %s (%+d days)."
                     % (ct["prerequisite_by"], ct["days_to_prerequisite"]))
        else:
            L.append("!! PREREQUISITE OVERDUE: the commercial-context conversation was due %s,"
                     % ct["prerequisite_by"])
            L.append("   %d days ago. Hold it this week and before anything commercial is sent."
                     % abs(ct["days_to_prerequisite"]))
        L.append("   The T-120 price decision does not issue until it has been held.")
        L.append("   R11 governs its timing: never attached to an apology, an outage, a credit")
        L.append("   or a missed milestone. If one landed inside 14 days either side, move it.")

    m = res["paper_movement"]
    L.append("")
    L.append("PAPER-MOVEMENT LEDGER (C15) — the Commit entry criterion")
    L.append("-" * 78)
    for row in m["rows"]:
        L.append("  [%s] %-58s %s" % ("x" if row["on_record"] else " ",
                                      row["label"], row["date"] or ""))
    L.append("Commit entry          %s — %s" % ("PASS" if m["commit_entry_met"] else "REFUSED",
                                                m["reason"]))
    if m["days_verbal_only"] is not None:
        L.append("Verbal yes            %s   (%d days with no paper movement)"
                 % (m["verbal_yes"], m["days_verbal_only"]))
        if m["escalate"]:
            L.append("!! %d days verbal-only. Escalate to the Renewal Manager. The next action is a"
                     % m["days_verbal_only"])
            L.append("   paper-process ask — named person, named document, date — not another")
            L.append("   value conversation.")
        elif m["register_row"]:
            L.append("!! %d days verbal-only. Open a risk-register row, cause code `verbal_only`."
                     % m["days_verbal_only"])
    if m["unrecognised_events"]:
        L.append("!! Not paper-movement events, ignored: %s" % ", ".join(m["unrecognised_events"]))
        L.append("   Valid keys: %s" % ", ".join(k for k, _ in PAPER_MOVEMENT_EVENTS))
    L.append("")
    L.append("STAGE GATES")
    L.append("-" * 78)
    L.append("%-30s %-12s %7s  %s" % ("Gate", "Date", "Days", "Status"))
    for g in res["gates"]:
        L.append("%-30s %-12s %7d  %s" % (g["gate"][:30], g["date"], g["days_from_today"], g["status"]))
    L.append("")
    p = res["paper"]
    L.append("PAPER CRITICAL PATH (backward from D = %s)" % a["opt_out_deadline"])
    L.append("-" * 78)
    L.append("Serial critical path  %d days%s" %
             (p["critical_path_days_floor"], "  (FLOOR — some lead times UNKNOWN)"
              if p["critical_path_is_floor"] else ""))
    L.append("Days available to D   %d" % p["days_available_to_D"])
    L.append("Slack                 %d days%s" %
             (p["slack_days"], "   *** NEGATIVE — paper cannot finish by D ***"
              if p["slack_days"] < 0 else ""))
    L.append("%-42s %-9s %-12s %s" % ("Workstream", "Lead", "Latest start", "Slack"))
    for r in p["rows"]:
        lead = "UNKNOWN" if r["lead_days"] is None else "%dd" % r["lead_days"]
        start = "UNKNOWN" if r["lead_days"] is None else r["latest_start"]
        slack = "" if r["slack_days"] is None else ("%+dd%s" % (r["slack_days"], "  LATE" if r["late"] else ""))
        L.append("%-42s %-9s %-12s %s" % (r["workstream"][:42], lead, start, slack))
    if p["unknown_workstreams"]:
        L.append("UNKNOWN — requires your measured cycle time: %s" % "; ".join(p["unknown_workstreams"]))
    if res.get("readiness"):
        r = res["readiness"]
        L.append("")
        L.append("RENEWAL READINESS  %d / %d" % (r["total"], r["max"]))
        L.append("-" * 78)
        for row in r["rows"]:
            L.append("  %d/2  %s" % (row["score"], row["item"]))
        if r["hard_gates_failed"]:
            L.append("  HARD GATE FAILED (must be 2/2): %s" % "; ".join(r["hard_gates_failed"]))
        L.append("  Commit-eligible: %s (needs >=%d and value/sponsor/process/paper at 2)"
                 % (r["commit_eligible"], r["commit_min"]))
    if res.get("meddpicc"):
        m = res["meddpicc"]
        L.append("")
        L.append("MEDDPICC-R  %d / %d" % (m["total"], m["max"]))
        L.append("-" * 78)
        for row in m["rows"]:
            L.append("  %d/2  %s" % (row["score"], row["item"]))
        if m["hard_gates_failed"]:
            L.append("  HARD GATE FAILED (must be 2/2): %s" % "; ".join(m["hard_gates_failed"]))
        L.append("  Commit-eligible: %s (needs >=%d and E/PP/C at 2)" % (m["commit_eligible"], m["commit_min"]))
    return "\n".join(L)


# ---------------------------------------------------------------- entry points

def compute(account):
    today = parse_date(account.get("today")) if account.get("today") else date.today()
    R = parse_date(account["renewal_date"])
    notice_raw = account.get("notice_days")
    notice_known = notice_raw is not None
    notice = int(notice_raw) if notice_known else 0
    D = R - timedelta(days=notice)
    segment = account.get("segment", "enterprise")
    term = account.get("term", "annual")
    leads = account.get("paper", {}) or {}
    res = {
        "anchor": {
            "account": account.get("account"),
            "today": fmt(today),
            "renewal_date": fmt(R),
            "days_to_renewal": (R - today).days,
            "notice_days": notice if notice_known else
                           "UNKNOWN — requires the executed contract",
            "notice_known": notice_known,
            "opt_out_deadline": fmt(D),
            "days_to_opt_out": (D - today).days,
            "atr": account.get("atr", "UNKNOWN — requires the executed contract value"),
            "segment": segment,
            "term": term,
            "auto_renew": account.get("auto_renew", "UNKNOWN"),
        },
        "gates": build_gates(D, R, today, segment, term, account.get("strategic", False)),
        "paper": paper_plan(D, today, leads),
    }
    res["paper_movement"] = paper_movement(account.get("paper_moved"),
                                           account.get("verbal_yes"), today,
                                           account.get("auto_renew"),
                                           account.get("notice_confirmed", False))
    res["commercial_touch"] = commercial_touch(account.get("last_commercial_touch"),
                                               today, D, segment, term)
    res["forecast_ceiling_by_calendar"] = forecast_ceiling(
        (R - today).days, account.get("auto_renew"),
        account.get("notice_confirmed", False))
    res["forecast_ceiling"] = apply_c15_cap(res["forecast_ceiling_by_calendar"],
                                            res["paper_movement"])
    if account.get("readiness"):
        res["readiness"] = score_block(account["readiness"], READINESS_DIMENSIONS,
                                       hard_gates=[0, 1, 5, 9], commit_min=16)
    if account.get("meddpicc"):
        res["meddpicc"] = score_block(account["meddpicc"], MEDDPICC_ELEMENTS,
                                      hard_gates=MEDDPICC_HARD_GATES, commit_min=15)
    return res


def render_batch(accounts, today):
    rows = []
    for acc in accounts:
        acc.setdefault("today", fmt(today))
        r = compute(acc)
        a = r["anchor"]
        ct = r["commercial_touch"]
        rows.append((a["days_to_opt_out"], a["account"], a["atr"], a["opt_out_deadline"],
                     a["renewal_date"], a["notice_days"],
                     next((g["gate"] for g in r["gates"] if g["days_from_today"] >= 0), "T-0 passed"),
                     r["paper"]["slack_days"],
                     r["paper_movement"]["events_on_record"],
                     r["paper_movement"]["commit_entry_met"],
                     ct["days_since"], ct["prerequisite_required"]))
    rows.sort(key=lambda x: x[0])
    L = ["RENEWAL WINDOW BOARD — sorted by days to opt-out deadline", "=" * 118,
         "%-22s %12s %6s %-12s %-12s %6s %-24s %7s %-14s %-12s" %
         ("Account", "ATR", "D-days", "Opt-out D", "Renewal R", "Notice", "Next gate",
          "Paper", "Moved (C15)", "Touch (C25)")]
    exceptions = []
    for d, name, atr, D, R, n, gate, slack, moved_n, commit_ok, touch_days, prereq in rows:
        atr_s = ("%12s" % ("$%s" % format(int(atr), ",")) ) if isinstance(atr, (int, float)) else "%12s" % "UNKNOWN"
        n_s = "%6d" % n if isinstance(n, int) else "%6s" % "UNK"
        moved_s = ("%d event(s)" % moved_n) if moved_n else ("clause" if commit_ok else "NONE")
        touch_s = "none >12mo" if touch_days is None else "%dd ago" % touch_days
        L.append("%-22s %s %6d %-12s %-12s %s %-24s %7s %-14s %-12s" %
                 (str(name)[:22], atr_s, d, D, R, n_s, gate[:24],
                  "%+dd" % slack if slack is not None else "n/a", moved_s, touch_s))
        if not commit_ok:
            exceptions.append("%s — Commit refused (C15, no paper movement)" % name)
        if prereq:
            exceptions.append("%s — commercial-context conversation required (C25)" % name)
        if slack is not None and slack < 0:
            exceptions.append("%s — negative paper slack" % name)
    L.append("")
    L.append("Paper column = slack in days between today and D after the known serial critical path.")
    L.append("Negative slack means the paper process cannot finish by the opt-out deadline.")
    L.append("Moved (C15) = paper-movement events on record. NONE means Commit is refused, not")
    L.append("deferred. Touch (C25) = days since the last commercial conversation with the buyer.")
    L.append("Notice = UNK means no notice period was supplied: D is shown equal to R, which is a")
    L.append("ceiling. Read the executed contract before treating that account's dates as real.")
    if exceptions:
        L.append("")
        L.append("EXCEPTIONS REQUIRING A FULL PLAN THIS WEEK")
        L.append("-" * 118)
        for e in exceptions:
            L.append("  " + e)
    return "\n".join(L)


def main(argv=None):
    p = argparse.ArgumentParser(description="Renewal stage-gate calendar and paper critical path.")
    p.add_argument("--renewal-date")
    p.add_argument("--notice-days", type=int, default=None,
                   help="from the executed contract; omitted prints UNKNOWN and D = R as a ceiling")
    p.add_argument("--today")
    p.add_argument("--account", default=None)
    p.add_argument("--atr", type=float, default=None)
    p.add_argument("--segment", default="enterprise",
                   choices=["enterprise", "mid_market", "smb", "tech_touch"])
    p.add_argument("--term", default="annual",
                   choices=["annual", "multi_year", "quarterly", "short_term", "monthly"])
    p.add_argument("--auto-renew", default="unknown", choices=["true", "false", "unknown"])
    p.add_argument("--notice-confirmed", action="store_true")
    p.add_argument("--strategic", action="store_true")
    p.add_argument("--paper", default="", help="k=v,k=v lead times in days")
    p.add_argument("--paper-moved", default="",
                   help="C15 entry criterion: event=YYYY-MM-DD pairs from "
                        "security_review, redlines_returned, po_requested, vendor_portal, "
                        "signature_routing. None supplied caps the ceiling at Most Likely.")
    p.add_argument("--verbal-yes", default=None,
                   help="date a verbal agreement was logged; days verbal-only are computed")
    p.add_argument("--last-commercial-touch", default=None,
                   help="C25: date of the last price/term/scope/budget conversation with the "
                        "economic buyer. Omitted means none on record and the T-180 gate fails.")
    p.add_argument("--readiness", default="", help="10 comma-separated scores 0-2")
    p.add_argument("--meddpicc", default="", help="9 comma-separated scores 0-2")
    p.add_argument("--batch", default=None, help="JSON file: list of account objects")
    p.add_argument("--json", action="store_true")
    args = p.parse_args(argv)

    today = parse_date(args.today) if args.today else date.today()

    if args.batch:
        with open(args.batch) as fh:
            accounts = json.load(fh)
        if args.json:
            print(json.dumps([compute(dict(a, today=a.get("today", fmt(today)))) for a in accounts], indent=2))
        else:
            print(render_batch(accounts, today))
        return 0

    if not args.renewal_date:
        p.error("--renewal-date is required (or use --batch)")

    leads = {}
    for pair in [x for x in args.paper.split(",") if x.strip()]:
        k, _, v = pair.partition("=")
        leads[k.strip()] = int(v)

    moved = {}
    for pair in [x for x in args.paper_moved.split(",") if x.strip()]:
        k, _, v = pair.partition("=")
        if not v.strip():
            p.error("--paper-moved needs event=YYYY-MM-DD; '%s' has no date, and an event "
                    "without a date is not evidence" % k.strip())
        moved[k.strip()] = v.strip()

    def scores(s, n, name):
        if not s:
            return None
        vals = [int(x) for x in s.split(",")]
        if len(vals) != n or any(v not in (0, 1, 2) for v in vals):
            p.error("--%s needs exactly %d values, each 0, 1 or 2" % (name, n))
        return vals

    account = {
        "account": args.account,
        "today": fmt(today),
        "renewal_date": args.renewal_date,
        "notice_days": args.notice_days,
        "atr": args.atr if args.atr is not None else "UNKNOWN — requires the executed contract value",
        "segment": args.segment,
        "term": args.term,
        "auto_renew": {"true": True, "false": False, "unknown": None}[args.auto_renew],
        "notice_confirmed": args.notice_confirmed,
        "strategic": args.strategic,
        "paper": leads,
        "paper_moved": moved,
        "verbal_yes": args.verbal_yes,
        "last_commercial_touch": args.last_commercial_touch,
        "readiness": scores(args.readiness, 10, "readiness"),
        "meddpicc": scores(args.meddpicc, 9, "meddpicc"),
    }
    res = compute(account)
    print(json.dumps(res, indent=2) if args.json else render(res))
    return 0


if __name__ == "__main__":
    sys.exit(main())
