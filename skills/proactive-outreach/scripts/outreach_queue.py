#!/usr/bin/env python3
"""
outreach_queue.py — deterministic outreach queue builder for the `proactive-outreach` skill.

Takes a JSON book of accounts with their fired triggers, applies the suppression gates,
ranks what survives by Outreach Priority, and fits the ranked list to a stated weekly
capacity in minutes. Prints markdown tables that paste straight into the artifact.

    Outreach Priority = (ARR / 1000) x Strength x Recency x Timing

Standard library only. No network. Every number it prints is reproducible from the input.

Usage
-----
    python3 outreach_queue.py book.json
    cat book.json | python3 outreach_queue.py -
    python3 outreach_queue.py book.json --capacity-minutes 480 --as-of 2026-08-28
    python3 outreach_queue.py --self-test

Input schema (see --print-sample for a complete runnable example)
----------------------------------------------------------------
{
  "as_of": "2026-08-28",                  # optional; defaults to today
  "capacity_minutes": 600,                # weekly proactive-outreach budget
  "touch_costs": {...},                   # optional override of the defaults below
  "accounts": [
    {
      "account_id": "a1", "name": "Acme", "arr": 420000,
      "renewal_date": "2027-02-14", "notice_period_days": 90,
      "risk_band": "Watch",               # Secure|Watch|At Risk|High Risk|Critical|unknown
      "outbound_touches_30d": 1,          # proactive touches already sent, rolling 30d
      "open_overdue_commitment": false,   # do we owe them something, overdue?
      "days_since_sev1_resolved": null,
      "days_since_escalation_closed": null,
      "ttfv_verified": true,              # time-to-first-value confirmed?
      "days_since_uplift": null,
      "days_since_last_ask": 200,
      "asks_this_year": 0,
      "triggers": [
        {"id": "U8", "name": "Entitlement limit approaching",
         "strength_tier": "T2", "fired_on": "2026-08-22",
         "channel": "email", "commercial_ask": true, "operational": false,
         "customer_quote": null,       # their verbatim sentence, if one exists
         "customer_sentiment": null}   # "negative" forces the Regulated register
      ]
    }
  ]
}

Any missing optional field is treated as unknown and is reported as such rather than
assumed clear — an unknown gate never silently passes.
"""

import argparse
import json
import sys
from datetime import date, datetime

# --- Scoring constants ------------------------------------------------------
# These mirror SKILL.md Step 3 and references/trigger-catalog.md section 2.
# They are practitioner operating conventions [P], not measured conversion curves.

STRENGTH = {"T1": 1.00, "T2": 0.85, "T3": 0.65, "T4": 0.50, "T5": 0.35, "T6": 0.15}

DEFAULT_DECAY_DAYS = {"T1": 7, "T2": 14, "T3": 21, "T4": 30, "T5": 45, "T6": 60}

DEFAULT_TOUCH_COSTS = {          # minutes: research + write + log
    "email": 20,
    "slack": 6,
    "relay": 12,
    "phone": 15,
    "exec_email": 30,
    "in_app": 0.5,
}

RISK_GATE_BANDS = {"at risk", "high risk", "critical"}

# --- Register (SKILL.md Step 6 · C4 · C27) --------------------------------
# The register is computed from the trigger, never chosen while writing. "voiced" means the
# customer said the thing themselves, so the acknowledgement slot must quote them and the
# message cannot be written without a verbatim on record. "found" means we detected it first,
# so slot 1 states what broke and what it cost them instead.
REGULATED_TRIGGERS = {
    "V1": "voiced",   # detractor response
    "S1": "voiced",   # escalation resolved
    "S2": "voiced",   # SLA breach on their ticket
    "S4": "voiced",   # volume spike then silence — quote what they stopped reporting
    "V4": "found",    # competitor named — never quoted back (trigger-catalog family 5)
    "U7": "found",    # activation not reached by day N — a miss we own
    "U9": "found",    # integration broken
    "B1": "found",    # payment failure
    "B2": "found",    # invoice overdue
    "C4": "found",    # seat reduction
    "X3": "found",    # layoffs / restructuring
}

# Triggers that are never suppressed; they route out of this queue entirely.
ESCALATION_OVERRIDE = {"C5": "save-play (auto-renew switched off)",
                       "R1": "save-play (champion departure)"}


def register_for(account, trigger):
    """Return (register, origin, why). Computed, never chosen — SKILL.md Step 6."""
    tid = str(trigger.get("id", "")).upper()
    if tid in REGULATED_TRIGGERS:
        return "Regulated", REGULATED_TRIGGERS[tid], f"trigger {tid}"
    if str(trigger.get("customer_sentiment", "")).lower() == "negative":
        return "Regulated", "voiced", "negative customer sentiment on the trigger"
    if account.get("open_overdue_commitment"):
        return "Regulated", "voiced", "an overdue commitment we owe them"
    band = str(account.get("risk_band", "")).strip().lower()
    if band in RISK_GATE_BANDS:
        return "Regulated", "found", f"churn-risk band {account.get('risk_band')}"
    sev1 = account.get("days_since_sev1_resolved")
    if sev1 is not None and sev1 <= 14:
        return "Regulated", "found", f"Sev-1 resolved {sev1}d ago"
    esc = account.get("days_since_escalation_closed")
    if esc is not None and esc <= 30:
        return "Regulated", "found", f"escalation closed {esc}d ago"
    uplift = account.get("days_since_uplift")
    if uplift is not None and uplift <= 90:
        return "Regulated", "found", f"price increase {uplift}d ago"
    return "Standard", "-", ""


def recency_multiplier(days_since_fired):
    if days_since_fired is None:
        return None
    if days_since_fired <= 2:
        return 1.00
    if days_since_fired <= 7:
        return 0.80
    if days_since_fired <= 14:
        return 0.55
    if days_since_fired <= 30:
        return 0.30
    return 0.10


def timing_multiplier(days_to_opt_out):
    if days_to_opt_out is None:
        return 1.00
    if days_to_opt_out <= 30:
        return 1.60
    if days_to_opt_out <= 90:
        return 1.40
    if days_to_opt_out <= 180:
        return 1.15
    return 1.00


def parse_date(value):
    if not value:
        return None
    return datetime.strptime(value, "%Y-%m-%d").date()


def days_between(later, earlier):
    if later is None or earlier is None:
        return None
    return (later - earlier).days


def opt_out_deadline(account):
    """renewal_date - notice_period_days. Never the renewal date alone."""
    renewal = parse_date(account.get("renewal_date"))
    notice = account.get("notice_period_days")
    if renewal is None or notice is None:
        return None
    return date.fromordinal(renewal.toordinal() - int(notice))


def evaluate_gates(account, trigger, as_of, days_to_opt_out):
    """Return a list of (gate_name, reason) that block this trigger. Empty means clear."""
    tid = str(trigger.get("id", "")).upper()
    if tid in ESCALATION_OVERRIDE:
        return []

    commercial = bool(trigger.get("commercial_ask", False))
    operational = bool(trigger.get("operational", False))
    blocks = []

    def unknown(field):
        return account.get(field, "__missing__") == "__missing__"

    # Gates that apply to every discretionary trigger.
    if not operational:
        touches = account.get("outbound_touches_30d")
        if unknown("outbound_touches_30d"):
            blocks.append(("account fatigue cap",
                           "UNKNOWN — requires logged outbound interactions (30d)"))
        elif touches is not None and touches >= 4:
            blocks.append(("account fatigue cap",
                           f"{touches} proactive touches already sent in 30d (cap 4)"))

        if account.get("open_overdue_commitment"):
            blocks.append(("open-loop gate",
                           "an overdue commitment we owe is outstanding; that is the outreach"))

    # Gates that apply only to commercial asks.
    if commercial:
        band = str(account.get("risk_band", "")).strip().lower()
        if band in RISK_GATE_BANDS:
            blocks.append(("health gate", f"risk band is {account['risk_band']}"))

        sev1 = account.get("days_since_sev1_resolved")
        if sev1 is not None and sev1 < 14:
            blocks.append(("post-Sev-1 cooldown", f"Sev-1 resolved {sev1}d ago (14d cooldown)"))

        esc = account.get("days_since_escalation_closed")
        if esc is not None and esc < 30:
            blocks.append(("post-escalation cooldown",
                           f"escalation closed {esc}d ago (30d cooldown)"))

        if account.get("ttfv_verified") is False:
            blocks.append(("onboarding blackout", "time-to-first-value not yet verified"))

        uplift = account.get("days_since_uplift")
        if uplift is not None and uplift < 90:
            blocks.append(("post-uplift blackout", f"price increase took effect {uplift}d ago"))

        last_ask = account.get("days_since_last_ask")
        if last_ask is not None and last_ask < 90:
            blocks.append(("ask spacing", f"last commercial ask {last_ask}d ago (90d minimum)"))

        asks = account.get("asks_this_year")
        if asks is not None and asks >= 2:
            blocks.append(("annual ask ceiling", f"{asks} expansion asks already made this year"))

        # Renewal endgame blocks NEW commercial asks, but never the contract triggers
        # whose whole purpose is the renewal conversation.
        if days_to_opt_out is not None and days_to_opt_out <= 30 and not tid.startswith("C"):
            blocks.append(("renewal endgame",
                           f"{days_to_opt_out}d to opt-out deadline; no new asks inside T-30"))

    return blocks


def build(book, as_of=None, capacity_override=None):
    as_of = as_of or parse_date(book.get("as_of")) or date.today()
    capacity = capacity_override or book.get("capacity_minutes", 600)
    costs = dict(DEFAULT_TOUCH_COSTS)
    costs.update(book.get("touch_costs") or {})

    queued, suppressed, expired, routed, held = [], [], [], [], []

    for acct in book.get("accounts", []):
        deadline = opt_out_deadline(acct)
        d_out = days_between(deadline, as_of)

        for trg in acct.get("triggers", []):
            tid = str(trg.get("id", "?")).upper()
            tier = str(trg.get("strength_tier", "T6")).upper()
            strength = STRENGTH.get(tier, 0.15)
            fired = parse_date(trg.get("fired_on"))
            age = days_between(as_of, fired)
            decay = trg.get("decay_days", DEFAULT_DECAY_DAYS.get(tier, 30))
            channel = trg.get("channel", "email")
            minutes = costs.get(channel, costs["email"])

            register, origin, why = register_for(acct, trg)
            quote = (trg.get("customer_quote") or "").strip()

            row = {
                "register": register,
                "register_origin": origin,
                "register_reason": why,
                "customer_quote": quote,
                "account_id": acct.get("account_id"),
                "name": acct.get("name", acct.get("account_id", "?")),
                "arr": float(acct.get("arr") or 0.0),
                "trigger": tid,
                "trigger_name": trg.get("name", ""),
                "tier": tier,
                "fired_on": trg.get("fired_on"),
                "age_days": age,
                "decay_days": decay,
                "channel": channel,
                "minutes": minutes,
                "days_to_opt_out": d_out,
                "opt_out_deadline": deadline.isoformat() if deadline else "UNKNOWN",
            }

            if tid in ESCALATION_OVERRIDE:
                row["route"] = ESCALATION_OVERRIDE[tid]
                routed.append(row)
                continue

            if age is None:
                row["reason"] = "UNKNOWN — requires trigger fired_on date"
                suppressed.append(row)
                continue

            if age > decay:
                row["reason"] = f"expired: fired {age}d ago, decay window {decay}d"
                expired.append(row)
                continue

            blocks = evaluate_gates(acct, trg, as_of, d_out)
            if blocks:
                row["gate"] = blocks[0][0]
                row["reason"] = "; ".join(f"{g}: {r}" for g, r in blocks)
                suppressed.append(row)
                continue

            # C4 — a customer-voiced Regulated trigger cannot be written from our paraphrase.
            if register == "Regulated" and origin == "voiced" and not quote:
                row["gate"] = "C4 · acknowledgement source"
                row["reason"] = ("UNKNOWN — requires their verbatim sentence "
                                 "(ticket / survey free-text / transcript). Retrieve it or phone "
                                 "them; do not write from our summary of what they meant")
                held.append(row)
                continue

            rec = recency_multiplier(age)
            tim = timing_multiplier(d_out)
            row.update(strength=strength, recency=rec, timing=tim,
                       priority=round((row["arr"] / 1000.0) * strength * rec * tim, 1))
            queued.append(row)

    queued.sort(key=lambda r: (-r["priority"], r["name"], r["trigger"]))

    spent, cut_at = 0.0, None
    for i, row in enumerate(queued, start=1):
        if spent + row["minutes"] <= capacity:
            spent += row["minutes"]
            row["in_week"] = True
            cut_at = i
        else:
            row["in_week"] = False

    return {"as_of": as_of, "capacity_minutes": capacity, "minutes_queued": round(spent, 1),
            "cut_at": cut_at or 0, "queued": queued, "suppressed": suppressed,
            "expired": expired, "routed": routed, "held": held}


def money(x):
    return f"${x:,.0f}"


def render(res):
    out = []
    q = res["queued"]
    in_week = [r for r in q if r["in_week"]]
    deferred = [r for r in q if not r["in_week"]]
    total = (len(q) + len(res["suppressed"]) + len(res["expired"]) + len(res["routed"])
             + len(res["held"]))
    regulated = [r for r in in_week if r["register"] == "Regulated"]

    out.append(f"# Outreach Queue — generated {res['as_of'].isoformat()}\n")
    out.append("| | |")
    out.append("|---|---|")
    out.append(f"| Triggers evaluated | {total} |")
    out.append(f"| Queued this week | {len(in_week)} · {money(sum(r['arr'] for r in in_week))} ARR represented |")
    out.append(f"| Deferred below the cut line | {len(deferred)} |")
    out.append(f"| Register | {len(regulated)} Regulated · "
               f"{len(in_week) - len(regulated)} Standard |")
    out.append(f"| Held — no customer sentence on record (C4) | {len(res['held'])} |")
    out.append(f"| Suppressed by a gate | {len(res['suppressed'])} |")
    out.append(f"| Expired by decay | {len(res['expired'])} |")
    out.append(f"| Routed out of this queue | {len(res['routed'])} |")
    out.append(f"| Capacity | {res['capacity_minutes']} min budgeted · "
               f"{res['minutes_queued']} min queued · cut at rank {res['cut_at']} |")
    out.append("")

    out.append("## 1. The Queue\n")
    out.append("| # | Account | ARR | Trigger | Tier | Fired | Age d | Days to opt-out | "
               "Strength | Recency | Timing | Priority | Register | Channel | Min |")
    out.append("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
    for i, r in enumerate(in_week, start=1):
        out.append(f"| {i} | {r['name']} | {money(r['arr'])} | {r['trigger']} {r['trigger_name']} "
                   f"| {r['tier']} | {r['fired_on']} | {r['age_days']} | "
                   f"{r['days_to_opt_out'] if r['days_to_opt_out'] is not None else 'UNKNOWN'} | "
                   f"{r['strength']:.2f} | {r['recency']:.2f} | {r['timing']:.2f} | "
                   f"**{r['priority']}** | {r['register']} | {r['channel']} | {r['minutes']} |")
    out.append("")
    if in_week:
        out.append("**Arithmetic, top 5:**\n")
        for i, r in enumerate(in_week[:5], start=1):
            out.append(f"{i}. {r['name']} · {r['trigger']} — "
                       f"({money(r['arr'])} / 1,000) x {r['strength']:.2f} x {r['recency']:.2f} "
                       f"x {r['timing']:.2f} = **{r['priority']}**")
        out.append("")

    out.append("## 2. Deferred (below the cut line)\n")
    out.append("| Account | Trigger | Priority | Fired | Expires in (d) |")
    out.append("|---|---|---|---|---|")
    for r in deferred:
        out.append(f"| {r['name']} | {r['trigger']} | {r['priority']} | {r['fired_on']} "
                   f"| {r['decay_days'] - r['age_days']} |")
    if not deferred:
        out.append("| — | — | — | — | — |")
    out.append("")

    out.append("## 3. Suppressed\n")
    out.append("| Account | Trigger | Gate | Reason |")
    out.append("|---|---|---|---|")
    for r in res["suppressed"]:
        out.append(f"| {r['name']} | {r['trigger']} | {r.get('gate', '—')} | {r['reason']} |")
    if not res["suppressed"]:
        out.append("| — | — | — | — |")
    out.append("")

    out.append("## 4. Expired by decay\n")
    out.append("| Account | Trigger | Reason |")
    out.append("|---|---|---|")
    for r in res["expired"]:
        out.append(f"| {r['name']} | {r['trigger']} | {r['reason']} |")
    if not res["expired"]:
        out.append("| — | — | — |")
    out.append("")

    out.append("## 5. Held — no customer sentence on record (C4)\n")
    out.append("| Account | Trigger | Register | Gate | What is required |")
    out.append("|---|---|---|---|---|")
    for r in res["held"]:
        out.append(f"| {r['name']} | {r['trigger']} | {r['register']} ({r['register_origin']}) "
                   f"| {r['gate']} | {r['reason']} |")
    if not res["held"]:
        out.append("| — | — | — | — | — |")
    out.append("")

    out.append("## 6. Routed out of this queue\n")
    out.append("| Account | Trigger | Routed to |")
    out.append("|---|---|---|")
    for r in res["routed"]:
        out.append(f"| {r['name']} | {r['trigger']} | {r['route']} |")
    if not res["routed"]:
        out.append("| — | — | — |")
    out.append("")

    out.append("> Register is computed from the trigger, not chosen while writing. A Regulated "
               "draft carries zero exclamation marks, no superlatives, sentences of 20 words or "
               "fewer and one apology at most, and opens on the acknowledgement slot "
               "(references/email-craft.md section 11).")
    out.append("")
    out.append("> Strength, recency and timing multipliers are practitioner operating conventions "
               "`[P]`, not measured conversion rates. Replace them with your own observed reply and "
               "meeting-booked rates by trigger ID once you have >=30 sends per trigger.")
    return "\n".join(out)


SAMPLE = {
    "as_of": "2026-08-28",
    "capacity_minutes": 120,
    "accounts": [
        {"account_id": "a1", "name": "Northwind", "arr": 420000,
         "renewal_date": "2027-02-14", "notice_period_days": 90, "risk_band": "Watch",
         "outbound_touches_30d": 1, "open_overdue_commitment": False,
         "ttfv_verified": True, "days_since_last_ask": 210, "asks_this_year": 0,
         "triggers": [
             {"id": "U8", "name": "seat limit", "strength_tier": "T2",
              "fired_on": "2026-08-26", "channel": "email", "commercial_ask": True},
             {"id": "V1", "name": "detractor", "strength_tier": "T2",
              "fired_on": "2026-08-27", "channel": "phone", "operational": True,
              "customer_quote": "four weeks of month-end done twice"}]},
        {"account_id": "a2", "name": "Contoso", "arr": 96000,
         "renewal_date": "2027-06-30", "notice_period_days": 30, "risk_band": "At Risk",
         "outbound_touches_30d": 0, "open_overdue_commitment": False,
         "ttfv_verified": True, "days_since_last_ask": 400, "asks_this_year": 0,
         "triggers": [
             {"id": "S3", "name": "asked for SSO", "strength_tier": "T1",
              "fired_on": "2026-08-27", "channel": "email", "commercial_ask": True},
             {"id": "R3", "name": "silence 60d", "strength_tier": "T3",
              "fired_on": "2026-08-20", "channel": "email"}]},
        {"account_id": "a3", "name": "Fabrikam", "arr": 610000,
         "renewal_date": "2026-09-20", "notice_period_days": 0, "risk_band": "Secure",
         "outbound_touches_30d": 4, "open_overdue_commitment": False,
         "ttfv_verified": True, "days_since_last_ask": 300, "asks_this_year": 0,
         "triggers": [
             {"id": "U1", "name": "usage drop", "strength_tier": "T3",
              "fired_on": "2026-08-25", "channel": "email"}]},
        {"account_id": "a4", "name": "Initech", "arr": 38000,
         "renewal_date": "2027-03-31", "notice_period_days": 60, "risk_band": "Secure",
         "outbound_touches_30d": 0, "open_overdue_commitment": True,
         "ttfv_verified": True, "days_since_last_ask": 500, "asks_this_year": 0,
         "triggers": [
             {"id": "X1", "name": "series C", "strength_tier": "T4",
              "fired_on": "2026-06-01", "channel": "email"},
             {"id": "R1", "name": "champion bounced", "strength_tier": "T4",
              "fired_on": "2026-08-27", "channel": "exec_email"}]},
    ],
}


def self_test():
    res = build(SAMPLE)
    names = {(r["name"], r["trigger"]): r for r in res["queued"]}
    sup = {(r["name"], r["trigger"]): r for r in res["suppressed"]}

    # Northwind U8: opt-out = 2027-02-14 minus 90d = 2026-11-16, i.e. 80 days out.
    # (420,000 / 1,000) x 0.85 x 1.00 (2d old) x 1.40 (31-90d band) = 499.8
    n = names[("Northwind", "U8")]
    assert n["opt_out_deadline"] == "2026-11-16", n["opt_out_deadline"]
    assert n["days_to_opt_out"] == 80, n["days_to_opt_out"]
    assert n["timing"] == 1.40 and n["recency"] == 1.00 and n["strength"] == 0.85
    assert abs(n["priority"] - 499.8) < 0.05, n["priority"]

    # An expansion ask inside the renewal endgame must be suppressed, not ranked.
    endgame = build({"as_of": "2026-08-28", "capacity_minutes": 600, "accounts": [
        {"account_id": "z", "name": "Endgame", "arr": 100000,
         "renewal_date": "2026-12-01", "notice_period_days": 90, "risk_band": "Secure",
         "outbound_touches_30d": 0, "ttfv_verified": True, "days_since_last_ask": 400,
         "asks_this_year": 0,
         "triggers": [{"id": "U8", "strength_tier": "T2", "fired_on": "2026-08-27",
                       "channel": "email", "commercial_ask": True}]}]})
    assert endgame["suppressed"][0]["gate"] == "renewal endgame", endgame["suppressed"]

    # Contoso S3 is a commercial ask on an At Risk account -> health gate.
    assert sup[("Contoso", "S3")]["gate"] == "health gate"
    # Fabrikam already had 4 proactive touches in 30d -> fatigue cap.
    assert sup[("Fabrikam", "U1")]["gate"] == "account fatigue cap"
    # Initech X1 fired 88 days ago against a 30-day decay -> expired, not suppressed.
    assert any(r["name"] == "Initech" and r["trigger"] == "X1" for r in res["expired"])
    # Initech R1 is an escalation override -> routed, never suppressed.
    assert any(r["name"] == "Initech" and r["trigger"] == "R1" for r in res["routed"])

    # C27 — the register is computed from the trigger, not chosen.
    assert names[("Northwind", "V1")]["register"] == "Regulated"
    assert names[("Northwind", "V1")]["register_origin"] == "voiced"
    assert names[("Northwind", "U8")]["register"] == "Standard"

    # C4 — a customer-voiced Regulated trigger with no verbatim on record is held, not queued.
    noquote = build({"as_of": "2026-08-28", "capacity_minutes": 600, "accounts": [
        {"account_id": "q", "name": "Quiet", "arr": 200000,
         "renewal_date": "2027-05-01", "notice_period_days": 30, "risk_band": "Secure",
         "outbound_touches_30d": 0, "ttfv_verified": True, "days_since_last_ask": 400,
         "asks_this_year": 0,
         "triggers": [{"id": "V1", "strength_tier": "T2", "fired_on": "2026-08-27",
                       "channel": "email"}]}]})
    assert not noquote["queued"], noquote["queued"]
    assert noquote["held"][0]["gate"] == "C4 · acknowledgement source", noquote["held"]
    # The same trigger with a verbatim on record queues normally.
    withquote = build({"as_of": "2026-08-28", "capacity_minutes": 600, "accounts": [
        {"account_id": "q", "name": "Quiet", "arr": 200000,
         "renewal_date": "2027-05-01", "notice_period_days": 30, "risk_band": "Secure",
         "outbound_touches_30d": 0, "ttfv_verified": True, "days_since_last_ask": 400,
         "asks_this_year": 0,
         "triggers": [{"id": "V1", "strength_tier": "T2", "fired_on": "2026-08-27",
                       "channel": "email", "customer_quote": "we are doing month-end twice"}]}]})
    assert len(withquote["queued"]) == 1 and not withquote["held"]
    # A we-found-it Regulated trigger is never held for want of a quote.
    found = build({"as_of": "2026-08-28", "capacity_minutes": 600, "accounts": [
        {"account_id": "f", "name": "Broken", "arr": 90000,
         "renewal_date": "2027-05-01", "notice_period_days": 30, "risk_band": "Secure",
         "outbound_touches_30d": 0, "ttfv_verified": True, "days_since_last_ask": 400,
         "asks_this_year": 0,
         "triggers": [{"id": "U9", "strength_tier": "T2", "fired_on": "2026-08-27",
                       "channel": "slack"}]}]})
    assert found["queued"][0]["register"] == "Regulated"
    assert found["queued"][0]["register_origin"] == "found" and not found["held"]
    # Capacity of 120 min: email 20 + phone 15 -> both Northwind rows fit; cut line respected.
    assert res["minutes_queued"] <= res["capacity_minutes"]
    assert all(r["in_week"] for r in res["queued"][:res["cut_at"]])
    print("self-test OK — {} queued, {} suppressed, {} expired, {} routed, {} held".format(
        len(res["queued"]), len(res["suppressed"]), len(res["expired"]),
        len(res["routed"]), len(res["held"])))
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("book", nargs="?", help="path to the JSON book, or - for stdin")
    ap.add_argument("--capacity-minutes", type=int, default=None)
    ap.add_argument("--as-of", default=None, help="YYYY-MM-DD")
    ap.add_argument("--json", action="store_true", help="emit raw JSON instead of markdown")
    ap.add_argument("--print-sample", action="store_true", help="print a runnable sample input")
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()

    if args.self_test:
        return self_test()
    if args.print_sample:
        print(json.dumps(SAMPLE, indent=2))
        return 0
    if not args.book:
        ap.error("a book path is required (or - for stdin); try --print-sample")

    raw = sys.stdin.read() if args.book == "-" else open(args.book).read()
    book = json.loads(raw)
    res = build(book, as_of=parse_date(args.as_of), capacity_override=args.capacity_minutes)
    if args.json:
        res = dict(res, as_of=res["as_of"].isoformat())
        print(json.dumps(res, indent=2))
    else:
        print(render(res))
    return 0


if __name__ == "__main__":
    sys.exit(main())
