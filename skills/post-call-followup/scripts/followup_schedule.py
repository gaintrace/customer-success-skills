#!/usr/bin/env python3
"""
Deterministic follow-through scheduling for the `post-call-followup` skill.

Why a script: business-day arithmetic done in prose drifts. Chase dates land on Saturdays,
"T+3" quietly becomes "T+3 calendar days", and the opt-out deadline gets computed from the
renewal date by subtracting a month. This produces the same dates every time and shows the
rule it applied to each one.

What it computes
----------------
  * Recap deadline from call end + the meeting type's latency target
  * Business-day due dates for every commitment
  * Chase 1 / Chase 2 / escalation dates (ours are chased BEFORE they are late; theirs after)
  * Opt-out deadline (renewal_date - notice_period_days) and days remaining
  * Commitment debt carried into the call: count, oldest age, ARR exposed
  * Validation: Grade C/D/E items rejected from the ledger, vague verbs flagged
  * C2 answer depth: every open question carries an integer `exchanges`; a one-exchange answer
    is thin, is refused as a finding, and must carry a verbatim follow-up question
  * C30 documentation gap: days since the last written internal note, and a dated write-up task
    for every interaction since that was never written up

Usage
-----
    python3 followup_schedule.py call.json
    python3 followup_schedule.py call.json --json
    python3 followup_schedule.py call.json --as-of 2026-09-10

Input JSON
----------
    {
      "account": "Orbital Systems",
      "arr": 196000,
      "call_end": "2026-09-02T15:30",
      "meeting_type": "renewal",
      "renewal_date": "2027-01-31",
      "notice_period_days": 60,
      "holidays": ["2026-12-25"],
      "commitments": [
        {"owner": "Aisha Bello", "side": "theirs", "grade": "A",
         "action": "Decide 12 vs 24 months", "due": "2026-10-03",
         "expected_effect": "Locks term before the notice window",
         "success_measure": "Written decision in the thread"},
        {"owner": "Ravi Menon", "side": "ours", "grade": "A",
         "action": "Send the formal quote covering both options",
         "due_in_business_days": 6,
         "expected_effect": "Starts procurement's clock",
         "success_measure": "Quote acknowledged by Dan Petrov"}
      ],
      "carried_debt": [
        {"owner": "Ravi Menon", "side": "ours", "action": "Send Q2 usage summary",
         "due": "2026-08-14", "status": "open"}
      ],
      "last_internal_note": "2026-08-06",
      "undocumented_interactions": [
        {"date": "2026-08-19", "what": "Slack thread with Aisha about the Q1 freeze"}
      ],
      "open_questions": [
        {"question": "What is driving the Q1 budget freeze?", "owes": "Aisha Bello",
         "exchanges": 1, "follow_up": "And what else is driving the Q1 freeze?",
         "central_issue": true}
      ]
    }

Either `due` (ISO date) or `due_in_business_days` (int, counted from the call date) is
required on each commitment. No network access, standard library only.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date, datetime, timedelta

# Latency targets measured from call end. Source: SKILL.md Step 1.
LATENCY_HOURS = {
    "escalation": 4,
    "renewal": 8,
    "expansion": 8,
    "check-in": 24,
    "qbr": 24,
    "technical": 24,
    "new-stakeholder": 24,
}
DEFAULT_LATENCY_HOURS = 24

BINDING_GRADES = {"A", "B"}
NON_BINDING = {
    "C": "intent without an act or a date - convert to a dated open question",
    "D": "courtesy statement - log as sentiment, never as a commitment",
    "E": "silence after an ask - log in bucket 6, not the ledger",
}

# Verbs that make a commitment unchaseable. The first group is banned library-wide;
# the second fails the "Act" limb of the three-part test.
VAGUE_VERBS = [
    "engage", "align", "touch base", "monitor closely", "drive adoption",
    "ensure success", "circle back", "leverage",
    "look into", "think about", "explore", "consider", "keep in mind",
    "follow up on", "revisit", "chat about", "discuss further",
]
VAGUE_ANCHORS = [
    "soon", "shortly", "next few weeks", "in the coming weeks",
    "after the holidays", "when things settle", "asap", "end of month",
]


# --------------------------------------------------------------------------- dates

def parse_date(value: str) -> date:
    return datetime.strptime(value[:10], "%Y-%m-%d").date()


def is_business_day(day: date, holidays: set[date]) -> bool:
    return day.weekday() < 5 and day not in holidays


def add_business_days(start: date, n: int, holidays: set[date]) -> date:
    """Add n business days. n may be negative. n == 0 rolls forward to a business day."""
    day = start
    if n == 0:
        while not is_business_day(day, holidays):
            day += timedelta(days=1)
        return day
    step = 1 if n > 0 else -1
    remaining = abs(n)
    while remaining:
        day += timedelta(days=step)
        if is_business_day(day, holidays):
            remaining -= 1
    return day


def business_days_between(a: date, b: date, holidays: set[date]) -> int:
    """Signed count of business days from a to b."""
    if a == b:
        return 0
    step = 1 if b > a else -1
    day, n = a, 0
    while day != b:
        day += timedelta(days=step)
        if is_business_day(day, holidays):
            n += step
    return n


# ----------------------------------------------------------------------- validation

def audit_text(action: str) -> list[str]:
    lowered = action.lower()
    flags = [f"vague verb: '{v}'" for v in VAGUE_VERBS if v in lowered]
    flags += [f"vague anchor: '{a}'" for a in VAGUE_ANCHORS if a in lowered]
    return flags


def audit_owner(owner: str) -> list[str]:
    generic = {"team", "the team", "engineering", "procurement", "support",
               "someone", "we", "us", "they", "them", "legal", "finance"}
    if owner.strip().lower() in generic:
        return [f"unnamed owner: '{owner}' - the Actor limb requires a named individual"]
    return []


# ------------------------------------------------------------------------ scheduling

def schedule_commitment(c: dict, call_day: date, holidays: set[date], as_of: date) -> dict:
    if "due" in c:
        due = parse_date(c["due"])
    elif "due_in_business_days" in c:
        due = add_business_days(call_day, int(c["due_in_business_days"]), holidays)
    else:
        raise ValueError(f"commitment missing 'due' or 'due_in_business_days': {c}")

    due = add_business_days(due, 0, holidays)  # roll a weekend due date forward
    ours = c.get("side", "ours").lower() == "ours"

    # Ours are chased before they are late; theirs after. Asymmetric on purpose:
    # a missed commitment by us is a trust event, by them it is a signal.
    chase1 = add_business_days(due, -2, holidays) if ours else add_business_days(due, 1, holidays)
    chase2 = None if ours else add_business_days(due, 3, holidays)
    escalate = add_business_days(due, 7, holidays)

    flags = audit_text(c.get("action", "")) + audit_owner(c.get("owner", ""))
    for field in ("expected_effect", "success_measure"):
        if not c.get(field):
            flags.append(f"missing {field} - every commitment slot requires all five fields")

    grade = str(c.get("grade", "")).upper()
    binding = grade in BINDING_GRADES
    if not binding:
        flags.append(f"grade {grade or '?'}: {NON_BINDING.get(grade, 'ungraded - grade it before logging')}")

    return {
        "owner": c.get("owner", "UNKNOWN"),
        "side": "ours" if ours else "theirs",
        "grade": grade or "?",
        "action": c.get("action", "UNKNOWN"),
        "due": due.isoformat(),
        "chase_1": chase1.isoformat(),
        "chase_2": chase2.isoformat() if chase2 else "-",
        "escalate": escalate.isoformat(),
        "days_to_due": business_days_between(as_of, due, holidays),
        "overdue": due < as_of,
        "binding": binding,
        "expected_effect": c.get("expected_effect", "UNKNOWN"),
        "success_measure": c.get("success_measure", "UNKNOWN"),
        "flags": flags,
    }


# C2: the first answer is rehearsed, the second considered, the third true. One exchange on the
# account's central issue is not a finding, whatever it was worth quoting. C2 grades the
# explanation, never the event - a stated commercial decision (R2) is logged and fires its
# trigger on one exchange; only the reason behind it stays thin.
THIN_EXCHANGES = 1
# C30: undocumented context survives until the first holiday, reorg or resignation.
NOTE_GAP_DAYS = 14
NOTE_BACKLOG_DUE_BUSINESS_DAYS = 2


def grade_answer_depth(q: dict) -> dict:
    """Route one open question or central-issue fact by how many exchanges it received."""
    raw = q.get("exchanges", None)
    flags: list[str] = []
    try:
        exchanges = int(raw)
    except (TypeError, ValueError):
        exchanges = None
        flags.append("exchanges missing or not an integer - required on every open question "
                     "and every central-issue fact (C2)")

    follow_up = (q.get("follow_up") or "").strip()
    if exchanges is None or exchanges <= THIN_EXCHANGES:
        grade, usable = "thin", False
        if not follow_up:
            flags.append("thin answer with no follow-up - the follow-up cell holds the literal "
                         "words to ask next, not a topic; the row is invalid without it")
        elif len(follow_up.split()) < 4 or follow_up.rstrip().endswith(("...",)):
            flags.append(f"follow-up '{follow_up}' reads as a topic, not a question to say out loud")
    elif exchanges == 2:
        grade, usable = "considered", True
    else:
        grade, usable = "tested", True

    if not usable and q.get("recorded_as_finding"):
        flags.append("recorded as a finding on one exchange - demote to an open question (C2)")

    return {
        "question": q.get("question", "UNKNOWN"),
        "owes": q.get("owes", "UNKNOWN"),
        "exchanges": exchanges if exchanges is not None else "UNKNOWN",
        "grade": grade,
        "central_issue": bool(q.get("central_issue", False)),
        "follow_up": follow_up or "MISSING - required",
        "usable_as_finding": usable,
        "flags": flags,
    }


def documentation_gap(payload: dict, as_of: date, holidays: set[date]) -> dict:
    """C30: days since the last written note, and the backlog it implies."""
    raw = payload.get("last_internal_note")
    backlog = payload.get("undocumented_interactions", []) or []
    due = add_business_days(as_of, NOTE_BACKLOG_DUE_BUSINESS_DAYS, holidays)

    if not raw:
        return {
            "last_note": "UNKNOWN - requires the account's interaction history",
            "days_since": None,
            "breach": True,
            "reason": "no last-note date supplied - treat as a breach; block 10 is mandatory",
            "backlog": [{"date": b.get("date", "UNKNOWN"), "what": b.get("what", "UNKNOWN"),
                         "write_up_by": due.isoformat()} for b in backlog],
            "backlog_due": due.isoformat(),
        }

    last = parse_date(raw)
    days = (as_of - last).days
    breach = days > NOTE_GAP_DAYS
    return {
        "last_note": last.isoformat(),
        "days_since": days,
        "breach": breach,
        "reason": (f"{days} days since the last written note (limit {NOTE_GAP_DAYS}) - "
                   f"block 10 lists every interaction since with no note"
                   if breach else f"{days} days since the last written note - within the limit"),
        "backlog": [{"date": b.get("date", "UNKNOWN"), "what": b.get("what", "UNKNOWN"),
                     "write_up_by": due.isoformat()} for b in backlog],
        "backlog_due": due.isoformat(),
    }


def compute(payload: dict, as_of: date) -> dict:
    holidays = {parse_date(h) for h in payload.get("holidays", [])}
    call_end_raw = payload["call_end"]
    call_end = datetime.strptime(call_end_raw, "%Y-%m-%dT%H:%M")
    call_day = call_end.date()

    meeting_type = payload.get("meeting_type", "check-in").lower()
    latency = LATENCY_HOURS.get(meeting_type, DEFAULT_LATENCY_HOURS)
    recap_deadline = call_end + timedelta(hours=latency)

    out: dict = {
        "account": payload.get("account", "UNKNOWN"),
        "arr": payload.get("arr"),
        "meeting_type": meeting_type,
        "call_end": call_end.strftime("%Y-%m-%d %H:%M"),
        "recap_latency_hours": latency,
        "recap_deadline": recap_deadline.strftime("%Y-%m-%d %H:%M"),
        "as_of": as_of.isoformat(),
    }

    # Opt-out deadline is the date that governs renewal timing, not the renewal date.
    if payload.get("renewal_date") and payload.get("notice_period_days") is not None:
        renewal = parse_date(payload["renewal_date"])
        notice = int(payload["notice_period_days"])
        opt_out = renewal - timedelta(days=notice)
        out["renewal_date"] = renewal.isoformat()
        out["notice_period_days"] = notice
        out["opt_out_deadline"] = opt_out.isoformat()
        out["days_to_opt_out"] = (opt_out - as_of).days
        out["opt_out_rule"] = f"{renewal.isoformat()} - {notice}d notice"
    else:
        out["opt_out_deadline"] = "UNKNOWN - requires renewal_date and notice_period_days"

    rows = [schedule_commitment(c, call_day, holidays, as_of)
            for c in payload.get("commitments", [])]
    rows.sort(key=lambda r: (r["due"], r["side"]))
    out["schedule"] = [r for r in rows if r["binding"]]
    out["rejected"] = [r for r in rows if not r["binding"]]

    # Commitment debt carried in.
    debt = [d for d in payload.get("carried_debt", [])
            if d.get("status", "open") == "open" and parse_date(d["due"]) < as_of]
    arr = payload.get("arr") or 0
    out["debt"] = {
        "count": len(debt),
        "ours": sum(1 for d in debt if d.get("side", "ours") == "ours"),
        "theirs": sum(1 for d in debt if d.get("side") == "theirs"),
        "oldest_days": max([(as_of - parse_date(d["due"])).days for d in debt], default=0),
        "arr_under_debt": arr if any(d.get("side", "ours") == "ours" for d in debt) else 0,
        "items": [{"owner": d.get("owner", "UNKNOWN"), "action": d.get("action", ""),
                   "due": d["due"], "days_overdue": (as_of - parse_date(d["due"])).days,
                   "side": d.get("side", "ours")} for d in debt],
    }
    questions = [grade_answer_depth(q) for q in payload.get("open_questions", [])]
    out["open_questions"] = questions
    out["thin_answers"] = [q for q in questions if not q["usable_as_finding"]]
    out["documentation"] = documentation_gap(payload, as_of, holidays)

    out["flag_count"] = (sum(len(r["flags"]) for r in rows)
                         + sum(len(q["flags"]) for q in questions)
                         + (1 if out["documentation"]["breach"] else 0))
    return out


# --------------------------------------------------------------------------- output

def render(r: dict) -> str:
    L: list[str] = []
    arr = f"${r['arr']:,.0f}" if r.get("arr") else "ARR UNKNOWN"
    L.append(f"FOLLOW-THROUGH SCHEDULE - {r['account']} ({arr}) - {r['meeting_type']}")
    L.append("=" * 96)
    L.append(f"Call end          {r['call_end']}")
    L.append(f"Recap deadline    {r['recap_deadline']}  (+{r['recap_latency_hours']}h, {r['meeting_type']} target)")
    if r.get("days_to_opt_out") is not None:
        L.append(f"Opt-out deadline  {r['opt_out_deadline']}  ({r['days_to_opt_out']} days) "
                 f"[{r['opt_out_rule']}]")
    else:
        L.append(f"Opt-out deadline  {r['opt_out_deadline']}")
    L.append(f"As of             {r['as_of']}")
    L.append("")

    L.append("COMMITMENTS (Grade A/B only)")
    hdr = f"{'#':<3}{'Side':<8}{'Owner':<16}{'Due':<12}{'Chase 1':<12}{'Chase 2':<12}{'Escalate':<12}{'BD':>4}"
    L.append(hdr)
    L.append("-" * len(hdr))
    if not r["schedule"]:
        L.append("  (none)")
    for i, c in enumerate(r["schedule"], 1):
        mark = "*" if c["overdue"] else ""
        L.append(f"{i:<3}{c['side']:<8}{c['owner'][:15]:<16}{c['due']:<12}"
                 f"{c['chase_1']:<12}{c['chase_2']:<12}{c['escalate']:<12}{c['days_to_due']:>4}{mark}")
        L.append(f"     {c['action']}")
        L.append(f"     effect: {c['expected_effect']}  |  measure: {c['success_measure']}")
    L.append("")

    if r["rejected"]:
        L.append("NOT COMMITMENTS - do not put these in the recap")
        for c in r["rejected"]:
            L.append(f"  [{c['grade']}] {c['owner']}: {c['action']}")
            for f in c["flags"]:
                L.append(f"        - {f}")
        L.append("")

    flagged = [c for c in r["schedule"] if c["flags"]]
    if flagged:
        L.append("QUALITY FLAGS")
        for c in flagged:
            L.append(f"  {c['owner']}: {c['action']}")
            for f in c["flags"]:
                L.append(f"        - {f}")
        L.append("")

    d = r["debt"]
    L.append("COMMITMENT DEBT CARRIED INTO THIS CALL")
    if d["count"] == 0:
        L.append("  None open and overdue.")
    else:
        L.append(f"  {d['count']} overdue ({d['ours']} ours, {d['theirs']} theirs) - "
                 f"oldest {d['oldest_days']} days - ARR under debt "
                 f"${d['arr_under_debt']:,.0f}")
        for it in sorted(d["items"], key=lambda x: -x["days_overdue"]):
            L.append(f"    {it['side']:<7}{it['owner'][:15]:<16}{it['due']}  "
                     f"{it['days_overdue']}d overdue  {it['action']}")
        if d["ours"] >= 3:
            L.append("  >=3 of our commitments overdue: capacity problem, not a discipline "
                     "problem. Re-commit with new dates rather than chasing.")
    L.append("")

    L.append("ANSWER DEPTH (C2) - one exchange is a rehearsed answer, not a finding")
    qs = r.get("open_questions", [])
    if not qs:
        L.append("  None recorded. If the call touched the account's central issue, this is a")
        L.append("  gap in the extraction, not an empty ledger.")
    for q in qs:
        mark = "THIN" if not q["usable_as_finding"] else q["grade"].upper()
        scope = "central issue" if q["central_issue"] else "secondary"
        L.append(f"  [{mark}] exchanges={q['exchanges']}  ({scope})  owes: {q['owes']}")
        L.append(f"        Q: {q['question']}")
        L.append(f"        follow-up to ask: {q['follow_up']}")
        for f in q["flags"]:
            L.append(f"        - {f}")
    thin = r.get("thin_answers", [])
    if thin:
        L.append(f"  {len(thin)} thin answer(s): open questions in note block 9, never findings,")
        L.append("  never CRM diff evidence, never decisions in the customer recap.")
    L.append("")

    d2 = r.get("documentation", {})
    L.append("DOCUMENTATION GAP (C30) - nothing lives in your head for two weeks")
    L.append(f"  Last written note: {d2.get('last_note')}")
    L.append(f"  {d2.get('reason')}")
    if d2.get("backlog"):
        for b in d2["backlog"]:
            L.append(f"    {b['date']}  {b['what']}  ->  write up by {b['write_up_by']}")
    elif d2.get("breach"):
        L.append("    No backlog supplied. List every interaction since the last note, or write")
        L.append("    UNKNOWN - requires <person> for anything no longer reconstructable.")
    L.append("")

    L.append("Chase rule: ours are chased 2 business days BEFORE due; theirs 1 and 3 business")
    L.append("days after. Escalation to the account owner at due + 7 business days.")
    return "\n".join(L)


def main() -> int:
    ap = argparse.ArgumentParser(description="Post-call follow-through scheduler")
    ap.add_argument("input", help="path to the call JSON")
    ap.add_argument("--json", action="store_true", help="emit JSON instead of a table")
    ap.add_argument("--as-of", help="evaluate against this date (default: today)")
    a = ap.parse_args()

    with open(a.input) as fh:
        payload = json.load(fh)

    as_of = parse_date(a.as_of) if a.as_of else date.today()
    try:
        result = compute(payload, as_of)
    except (KeyError, ValueError) as exc:
        print(f"input error: {exc}", file=sys.stderr)
        return 2

    print(json.dumps(result, indent=2) if a.json else render(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
