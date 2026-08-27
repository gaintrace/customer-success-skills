#!/usr/bin/env python3
"""
Plot every dated technical obligation on a deployment against the OPT-OUT DEADLINE.

Certificates, OAuth refresh tokens, service-account secrets, API and SDK sunsets, support-window
ends, SOC 2 / ISO evidence expiry, pen-test validity, DPA and subprocessor notice dates. Each is a
dated failure with a name on it, and the date that matters is not the renewal date — it is
`renewal_date - notice_period_days` (`R1`). An obligation maturing before the opt-out deadline is a
renewal dependency; one maturing after it is engineering work.

    python3 expiry_calendar.py ../assets/sample-expiries.json
    python3 expiry_calendar.py obligations.json --today 2026-08-27 --json

Stdlib only. No network. Nothing is inferred: an item with no date is printed as UNKNOWN, never
assumed safe, and an item with no owner is flagged rather than quietly assigned to nobody.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

# Lead time each class of obligation needs before its date, in days. These are the windows in
# which the work is actually schedulable — a customer-side change window is not the same as a
# certificate rotation. `R7` puts commercial paper at 90 days.
LEAD_DAYS = {
    "certificate": 30,
    "token": 21,
    "secret": 21,
    "api_sunset": 90,
    "sdk_sunset": 90,
    "version_eol": 120,
    "compliance_evidence": 90,
    "dpa": 90,
    "subprocessor_notice": 60,
    "pen_test": 60,
    "other": 30,
}
BANDS = (("Critical", 0), ("High", 30), ("Medium", 90), ("Low", 180))


def parse_date(v, field: str) -> date | None:
    if not v:
        return None
    try:
        return datetime.strptime(str(v)[:10], "%Y-%m-%d").date()
    except ValueError:
        raise SystemExit(f"ERROR {field}: '{v}' is not an ISO date (YYYY-MM-DD)")


def band(days_to_action: int | None) -> str:
    if days_to_action is None:
        return "UNKNOWN"
    if days_to_action < 0:
        return "Critical"
    for name, limit in BANDS:
        if days_to_action <= limit:
            return name
    return "Low"


def main() -> int:
    ap = argparse.ArgumentParser(description="Date every technical obligation against the opt-out deadline.")
    ap.add_argument("file", help="JSON: {account, renewal_date, notice_period_days, obligations:[...]}")
    ap.add_argument("--today", help="ISO date to evaluate against (default: system date)")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    path = Path(a.file)
    if not path.exists():
        print(f"no such file: {path}", file=sys.stderr)
        return 2
    data = json.loads(path.read_text())

    today = parse_date(a.today, "--today") or date.today()
    renewal = parse_date(data.get("renewal_date"), "renewal_date")
    notice = data.get("notice_period_days")
    account = data.get("account", path.stem)

    opt_out = None
    notice_assumed = False
    if renewal is not None:
        if notice is None:
            notice, notice_assumed = 30, True
        opt_out = renewal - timedelta(days=int(notice))

    rows = []
    for ob in data.get("obligations", []):
        kind = ob.get("kind", "other")
        if kind not in LEAD_DAYS:
            kind = "other"
        due = parse_date(ob.get("date"), f"obligation '{ob.get('name')}' date")
        lead = int(ob.get("lead_days", LEAD_DAYS[kind]))
        act_by = due - timedelta(days=lead) if due else None
        rows.append({
            "name": ob.get("name", "UNNAMED"),
            "kind": kind,
            "date": due.isoformat() if due else None,
            "owner": ob.get("owner"),
            "side": ob.get("side", "UNKNOWN"),
            "lead_days": lead,
            "act_by": act_by.isoformat() if act_by else None,
            "days_to_date": (due - today).days if due else None,
            "days_to_act_by": (act_by - today).days if act_by else None,
            "before_opt_out": None if (act_by is None or opt_out is None) else act_by <= opt_out,
            "band": band((act_by - today).days if act_by else None),
        })

    order = {"Critical": 0, "High": 1, "Medium": 2, "Low": 3, "UNKNOWN": 4}
    rows.sort(key=lambda r: (order[r["band"]], r["days_to_act_by"] if r["days_to_act_by"] is not None else 10**6))

    if a.json:
        print(json.dumps({"account": account, "today": today.isoformat(),
                          "renewal_date": renewal.isoformat() if renewal else None,
                          "notice_period_days": notice, "notice_assumed": notice_assumed,
                          "opt_out_deadline": opt_out.isoformat() if opt_out else None,
                          "obligations": rows}, indent=2))
        return 0

    print(f"# Expiry and sunset calendar — {account}\n")
    if opt_out:
        print(f"**Opt-out deadline {opt_out.isoformat()} — {(opt_out - today).days} days** "
              f"(renewal {renewal.isoformat()} minus {notice} days' notice"
              + (", **notice period assumed — confirm it against the signed contract and record it in "
                 "the Assumptions table**" if notice_assumed else "") + "). `R1`\n")
    else:
        print("**Opt-out deadline UNKNOWN — requires `subscription.renewal_date` and "
              "`notice_period_days`.** Every row below is dated against today only; the renewal "
              "consequence cannot be computed. Do not substitute the renewal date. `R1`\n")

    print("| Band | Obligation | Kind | Date | Act by | Days | Before opt-out? | Owner (side) |")
    print("|---|---|---|---|---|---|---|---|")
    for r in rows:
        pre = "—" if r["before_opt_out"] is None else ("**yes**" if r["before_opt_out"] else "no")
        days = "UNKNOWN" if r["days_to_act_by"] is None else str(r["days_to_act_by"])
        print(f"| {r['band']} | {r['name']} | {r['kind']} | {r['date'] or 'UNKNOWN'} "
              f"| {r['act_by'] or 'UNKNOWN'} | {days} | {pre} "
              f"| {r['owner'] or '**UNOWNED**'} ({r['side']}) |")

    crit = [r for r in rows if r["band"] == "Critical"]
    renewal_dep = [r for r in rows if r["before_opt_out"]]
    unowned = [r["name"] for r in rows if not r["owner"]]
    undated = [r["name"] for r in rows if not r["date"]]

    print()
    if crit:
        print(f"**{len(crit)} past its act-by date:** " + "; ".join(
            f"{r['name']} (act-by {r['act_by']}, {abs(r['days_to_act_by'])} days ago)" for r in crit) + "\n")
    if renewal_dep:
        print(f"**{len(renewal_dep)} of {len(rows)} obligations mature before the opt-out deadline** — they are "
              f"renewal dependencies, not engineering work, and belong in the renewal-critical facts at the "
              f"top of the plan.\n")
    if unowned:
        print(f"**UNOWNED ({len(unowned)}):** {', '.join(unowned)}. An obligation with a date and no name "
              f"attached is how deployments fail on a Tuesday morning.\n")
    if undated:
        print(f"**UNKNOWN — requires the expiry date:** {', '.join(undated)}. Never treat an undated "
              f"obligation as safe; it is unmeasured, not distant.\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
