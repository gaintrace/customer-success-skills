#!/usr/bin/env python3
"""
update_clock.py — the deterministic arithmetic behind an escalation note.

Three things a model should never do in prose, because a wrong one gets sent:

  1. The update clock. Given severity and the last update you actually sent, when is the
     next one due, is one overdue right now, and what are the next five commitment times?
     "Next update at 14:00" is the single line that stops a customer escalating, so the
     time has to be computed and then held.

  2. The impact arithmetic. Manual hours their team spent, and the loaded cost of those
     hours, with the working printed so the customer can check it against their own rates.

  3. Notice compliance for a planned change. Days of notice given, and — the one everybody
     misses — whether the announcement lands before each account's opt-out deadline
     (`renewal_date - notice_period_days`, R1). An announcement that arrives after a
     customer's notice window closed is a price increase they cannot decline.

Stdlib only. No network.

    python3 update_clock.py sample_incident.json
    python3 update_clock.py sample_incident.json --now 2026-08-27T13:30:00Z

Exit codes: 0 = clean · 1 = a compliance breach or an overdue update was found · 2 = bad input.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date, datetime, timedelta, timezone

# Cadence floors in minutes, by severity. These are floors, not ceilings: sending more often
# is always allowed, sending less often is a breach of the commitment made in the first note.
# Shape follows GitLab's published four-tier account-escalation matrix (Critical daily,
# High multiple times per week, Medium weekly/fortnightly) tightened at the top end to the
# 30-60 minute status-page practice for a live customer-impacting outage.
CADENCE_MINUTES = {
    "S1": 60,
    "S2": 240,
    "S3": 1440,
    "S4": 10080,
}

# How quickly the first note must go out after customer impact is confirmed, in minutes.
FIRST_NOTE_MINUTES = {"S1": 60, "S2": 240, "S3": 480, "S4": None}

DEFAULT_NOTICE_DAYS = {
    "price_increase": 90,
    "product_eol": 365,
    "api_deprecation": 180,
    "support_tier_change": 90,
    "feature_tier_move": 90,
    "csm_change": 10,
}


def parse_dt(value: str) -> datetime:
    """Accept ISO-8601 with a trailing Z, which datetime.fromisoformat rejects before 3.11."""
    if value.endswith("Z"):
        value = value[:-1] + "+00:00"
    dt = datetime.fromisoformat(value)
    return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)


def parse_d(value: str) -> date:
    return date.fromisoformat(value)


def fmt(dt: datetime) -> str:
    return dt.astimezone(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")


def money(x: float, currency: str) -> str:
    return f"{currency} {x:,.0f}"


def update_clock(inc: dict, now: datetime) -> tuple[list[str], bool]:
    out: list[str] = ["UPDATE CLOCK", "-" * 62]
    breach = False

    sev = str(inc.get("severity", "")).upper()
    if sev not in CADENCE_MINUTES:
        out.append(f"  severity {sev!r} not in {sorted(CADENCE_MINUTES)} — "
                   f"UNKNOWN, requires a severity before a cadence can be committed")
        return out, True

    cadence = CADENCE_MINUTES[sev]
    out.append(f"  Reference          {inc.get('reference', 'UNKNOWN — requires an incident ref')}")
    out.append(f"  Severity           {sev} · update floor every {cadence} min "
               f"({cadence / 60:.1f} h)")

    confirmed = inc.get("customer_impact_confirmed_at")
    if confirmed:
        c = parse_dt(confirmed)
        out.append(f"  Impact confirmed   {fmt(c)}")
        limit = FIRST_NOTE_MINUTES.get(sev)
        if limit is not None:
            due = c + timedelta(minutes=limit)
            out.append(f"  First note due by  {fmt(due)}  ({limit} min after confirmation)")

    sent = sorted(parse_dt(t) for t in inc.get("updates_sent_at", []))
    if sent:
        out.append(f"  Updates sent       {len(sent)} · last {fmt(sent[-1])}")
    else:
        out.append("  Updates sent       0 — nothing has gone out yet")

    resolved = inc.get("resolved_at")
    if resolved:
        r = parse_dt(resolved)
        out.append(f"  Resolved           {fmt(r)} — cadence stops; closure note is now due")
        out.append(f"  Closure note due   {fmt(r + timedelta(days=1))}  (within 1 business day)")
        out.append(f"  Written review due {fmt(r + timedelta(days=5))}  (5 business days)")
        return out, breach

    anchor = sent[-1] if sent else (parse_dt(confirmed) if confirmed else now)
    next_due = anchor + timedelta(minutes=cadence)
    overdue_min = (now - next_due).total_seconds() / 60

    if overdue_min > 0:
        breach = True
        out.append(f"  NEXT UPDATE        OVERDUE by {overdue_min:.0f} min "
                   f"(was due {fmt(next_due)})")
        out.append("                     Send now. Silence during a live incident reads as "
                   "loss of control,")
        out.append("                     and it is the part the customer's exec remembers.")
    else:
        out.append(f"  Next update due    {fmt(next_due)}  "
                   f"(in {abs(overdue_min):.0f} min)")

    out.append("  Schedule to commit in the note (send each one, new information or not):")
    t = next_due if overdue_min <= 0 else now
    for _ in range(5):
        out.append(f"      {fmt(t)}")
        t += timedelta(minutes=cadence)
    return out, breach


def impact_math(imp: dict) -> list[str]:
    out: list[str] = ["", "IMPACT ARITHMETIC — stated in their units, then in money", "-" * 62]
    required = ("units_affected", "manual_minutes_per_unit")
    missing = [k for k in required if imp.get(k) is None]
    if missing:
        out.append(f"  UNKNOWN — requires {', '.join(missing)}. Do not state a blast-radius")
        out.append("  number you have not computed; state what you know and when you will know")
        out.append("  the rest.")
        return out

    units = float(imp["units_affected"])
    minutes = float(imp["manual_minutes_per_unit"])
    people = float(imp.get("people_involved", 1) or 1)
    unit_name = imp.get("unit_name", "affected unit")
    hours = units * minutes * people / 60.0

    out.append(f"  {units:.0f} x {unit_name} affected")
    out.append(f"  hours = {units:.0f} units x {minutes:.0f} min x {people:.0f} people / 60"
               f"  =  {hours:,.1f} hours")

    rate = imp.get("loaded_hourly_rate")
    currency = imp.get("currency", "USD")
    if rate is None:
        out.append("  cost  = UNKNOWN — requires loaded_hourly_rate. Ask them for their own")
        out.append("          rate rather than asserting ours; a number they supplied is a")
        out.append("          number they will not dispute.")
    else:
        cost = hours * float(rate)
        out.append(f"  cost  = {hours:,.1f} h x {money(float(rate), currency)}/h"
                   f"  =  {money(cost, currency)}")
        out.append(f"  Round it before it goes in the note: ~{money(round(cost, -2), currency)}"
                   " — a composite to the dollar implies a measurement nobody took.")
    return out


def notice_compliance(change: dict, accounts: list[dict]) -> tuple[list[str], bool]:
    out: list[str] = ["", "NOTICE COMPLIANCE — planned change", "-" * 62]
    breach = False

    kind = change.get("kind", "unspecified")
    announce = parse_d(change["announce_on"])
    effective = parse_d(change["effective_on"])
    required = change.get("required_notice_days")
    if required is None:
        required = DEFAULT_NOTICE_DAYS.get(kind)
    given = (effective - announce).days

    out.append(f"  Change             {kind}")
    out.append(f"  Announce on        {announce}")
    out.append(f"  Effective on       {effective}")
    if required is None:
        out.append("  Required notice    UNKNOWN — requires the contract clause or a policy "
                   "default")
    else:
        verdict = "OK" if given >= required else "SHORT"
        if given < required:
            breach = True
        out.append(f"  Notice given       {given} days vs {required} required — {verdict}"
                   + ("" if given >= required else
                      f" by {required - given} days. Move the effective date, not the notice."))

    out.append("")
    out.append("  Per account — the announcement must land BEFORE the opt-out deadline (R1),")
    out.append("  not merely before the renewal date. A change announced after their notice")
    out.append("  window closed is a change they had no way to decline.")
    out.append("")
    header = f"  {'Account':<24}{'ARR':>12}  {'Opt-out':<12}{'Margin':>8}  Verdict"
    out.append(header)
    out.append("  " + "-" * (len(header) - 2))

    for a in accounts:
        name = str(a.get("name", "UNKNOWN"))[:23]
        arr = a.get("arr")
        arr_s = f"{arr:,.0f}" if isinstance(arr, (int, float)) else "UNKNOWN"
        npd = a.get("notice_period_days")
        if a.get("renewal_date") is None or npd is None:
            out.append(f"  {name:<24}{arr_s:>12}  {'UNKNOWN':<12}{'—':>8}  "
                       f"UNKNOWN — requires notice_period_days from the signed contract")
            breach = True
            continue
        opt_out = parse_d(a["renewal_date"]) - timedelta(days=int(npd))
        margin = (opt_out - announce).days
        if margin < 0:
            verdict = "BREACH — announced after their opt-out closed"
            breach = True
        elif margin < 14:
            verdict = "TIGHT — under 14 days; call before the email"
        else:
            verdict = "OK"
        out.append(f"  {name:<24}{arr_s:>12}  {str(opt_out):<12}{margin:>8}  {verdict}")
    return out, breach


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("input", help="path to an incident JSON file")
    ap.add_argument("--now", help="ISO-8601 timestamp to evaluate against (default: real now)")
    args = ap.parse_args()

    try:
        data = json.loads(open(args.input, encoding="utf-8").read())
    except (OSError, json.JSONDecodeError) as e:
        print(f"cannot read {args.input}: {e}", file=sys.stderr)
        return 2

    now = parse_dt(args.now) if args.now else datetime.now(timezone.utc)

    lines: list[str] = []
    breach = False

    lines.append("=" * 62)
    lines.append(f"ESCALATION CLOCK — evaluated at {fmt(now)}")
    lines.append("Internal working. None of this arithmetic is customer-facing until it has")
    lines.append("been rewritten in their units and passed the leak scan.")
    lines.append("=" * 62)
    lines.append("")

    if "incident" in data:
        block, b = update_clock(data["incident"], now)
        lines += block
        breach = breach or b

    if "impact" in data:
        lines += impact_math(data["impact"])

    if "planned_change" in data:
        block, b = notice_compliance(data["planned_change"], data.get("accounts", []))
        lines += block
        breach = breach or b

    lines.append("")
    lines.append("=" * 62)
    lines.append("BREACHES OR OVERDUE ITEMS FOUND — see above" if breach
                 else "No overdue update and no notice breach found.")
    lines.append("=" * 62)

    print("\n".join(lines))
    return 1 if breach else 0


if __name__ == "__main__":
    sys.exit(main())
