#!/usr/bin/env python3
"""
Deterministic churn-risk scoring for the `churn-risk` skill.

Why a script: an LLM doing weighted arithmetic across dozens of accounts in prose will
drift. This produces the same number every time, shows every step, and is auditable by
anyone who disagrees with the model.

Usage
-----
    python risk_score.py accounts.json
    python risk_score.py accounts.json --profile plg
    python risk_score.py accounts.json --explain ACME

Input: JSON list of accounts. Missing families must be `null`, NOT 0 — `null` means
"not measured" and is renormalised out; 0 means "measured, no risk".

    [
      {
        "account_id": "ACME",
        "name": "Acme Corp",
        "arr": 148000,
        "renewal_date": "2026-11-01",
        "notice_period_days": 60,
        "families": {
          "usage": 72, "commercial": 90, "relationship": 65,
          "support": 30, "sentiment": null, "billing": 10, "firmographic": 0
        },
        "calendar": {
          "acceptance_latency_days": 6, "reschedules_90d": 3,
          "consecutive_buyer_reschedules": 2, "accepted_by": "delegate"
        },
        "negotiation_friction": "routine",
        "first_term": false,
        "floors": ["auto_renew_off"],
        "patterns": ["decapitation", "quiet_quit"],
        "savability": "addressable"
      }
    ]

Required fields, and why the script refuses without them
--------------------------------------------------------
These are craft mechanisms from `../../cs-context/references/practitioner-craft.md`, enforced
here rather than left to the writer to remember. `"UNKNOWN"` is always a legal value; omission
is not, because a dropped field reads as a clean one.

    C22  `calendar`  — acceptance_latency_days, reschedules_90d,
                       consecutive_buyer_reschedules, accepted_by.
                       Two consecutive reschedules by the economic buyer fires the 60 floor on
                       its own, with no usage decline required.
    C24  `negotiation_friction` — contested | routine | frictionless |
                       not_applicable_self_serve | UNKNOWN. `frictionless` on an account with
                       relationship risk >=50 (or engaged_contacts_below_target) matches the
                       Frictionless renewal pattern and floors the band at Watch.
    C23  `first_term` — when true, `days_since_contract_start` and `activation_fired` are
                       required. Day >=60 with no activation fires Failed launch now, and the
                       renewal plan is WITHHELD.

No network access. No dependencies beyond the standard library.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date, datetime
from typing import Any

# --------------------------------------------------------------------------------------
# Model constants — mirror references/scoring-model.md. Change both together.
# --------------------------------------------------------------------------------------

WEIGHT_PROFILES: dict[str, dict[str, int]] = {
    # Enterprise / annual contracts: a commercial action outweighs a usage dip.
    "enterprise": {
        "usage": 22, "commercial": 25, "relationship": 20,
        "support": 12, "sentiment": 9, "billing": 7, "firmographic": 5,
    },
    # PLG / monthly: the product IS the relationship, and there is no procurement layer.
    "plg": {
        "usage": 35, "commercial": 15, "relationship": 10,
        "support": 13, "sentiment": 10, "billing": 12, "firmographic": 5,
    },
    # Usage-based / consumption pricing: consumption trend is the revenue itself.
    "consumption": {
        "usage": 30, "commercial": 20, "relationship": 15,
        "support": 12, "sentiment": 8, "billing": 10, "firmographic": 5,
    },
}

FLOORS: dict[str, tuple[int, str]] = {
    "auto_renew_off":        (85, "Auto-renew switched off or non-renewal notice served"),
    "termination_language":  (80, "Termination / opt-out language requested via legal or procurement"),
    "data_export":           (80, "Bulk data export or full API extraction by an admin, with usage decline"),
    "zero_usage_30d":        (75, "Zero core-action usage for 30 consecutive days on a paid account"),
    "buyer_departed":        (70, "Economic buyer departed, no replacement identified within 30 days"),
    "optout_no_convo":       (70, "Opt-out deadline inside 30 days with no renewal conversation held"),
    "seat_reduction_25":     (65, "Seat count reduced by 25% or more during the term"),
    "competitor_named":      (60, "Competitor named in a ticket, transcript, or email thread"),
    "p1_open_14d":           (60, "P1 escalation open more than 14 days with executive visibility"),
    # C22 — the calendar moves before the product does. Fires on its own; healthy usage does
    # not offset it, because withdrawal is polite long before it is visible in telemetry.
    "buyer_reschedule_2x":   (60, "Economic buyer rescheduled or declined two consecutive meetings (C22)"),
    # C24 — a band floor, not an escalation. It does not claim the account is at 30 risk; it
    # forbids reporting it Secure. Absence of objection is not evidence of engagement.
    "frictionless_low_engagement": (30, "Renewal closing with zero negotiation events on a low-engagement account (C24)"),
}

BAND_FLOOR_PATTERNS: dict[str, int] = {
    # Pattern -> minimum final score. The risk is to the NEXT cycle, so this is a floor on
    # what may be reported rather than a P0 escalation.
    "frictionless_renewal": 30,
}

PATTERNS: dict[str, tuple[str, str]] = {
    # key: (composition, priority) — see references/compound-patterns.md
    "decapitation":        ("Champion departed + single-threaded + no exec sponsor", "P0"),
    "exit_preparation":    ("Data export + auto-renew off + procurement/termination terms", "P0"),
    "quiet_quit":          ("Ticket spike then silence + usage decay + no touch", "P0"),
    "buyer_disconnect":    ("Aggregate usage flat/up but buying-team usage down 50%+", "P0"),
    "regime_change":       ("New CIO/CFO + procurement re-engaged + competitor named", "P0"),
    "technical_decoupling":("Integration disconnected 30d+ + API decline + SSO removed", "P0"),
    "failed_launch":       ("TTFV overrun 2x+ + milestones slipped + services overrun + dark", "P0"),
    "consolidation_target":("Customer acquired + competitor named + SSO moved to acquirer IdP", "P0"),
    "shelfware":           ("Seat utilisation <0.5 + narrow breadth + use case never live", "P1"),
    "budget_squeeze":      ("Layoffs + financial distress + DSO deterioration + deprovisioning", "P1"),
    "value_vacuum":        ("No ROI evidence + no QBR in 2 quarters + exec disengaged", "P1"),
    "death_by_tickets":    ("Repeat issue 3+ + P1 aging + CSAT decline + blocking request rejected", "P1"),
    "contraction_spiral":  ("Seat reduction last cycle + utilisation falling + term shortened", "P1"),
    "frictionless_renewal":("Zero negotiation events + low engagement + no customer-stated value", "P1"),
}

# ------------------------------------------------------------------------------------
# Required fields (craft mechanisms). "UNKNOWN" is legal; omission is not.
# ------------------------------------------------------------------------------------

CALENDAR_FIELDS = ("acceptance_latency_days", "reschedules_90d",
                   "consecutive_buyer_reschedules", "accepted_by")
FRICTION_VALUES = {"contested", "routine", "frictionless",
                   "not_applicable_self_serve", "UNKNOWN"}
ACCEPTED_BY_VALUES = {"economic_buyer", "champion", "delegate", "nobody", "UNKNOWN"}
FIRST_TERM_GATE_DAY = 60          # C23 — months two to four decide the first renewal


def validate_account(acct: dict[str, Any]) -> list[str]:
    """Refuse to score an account whose craft fields were dropped.

    A missing field is not a short record; it is a record that will be read as clean. This is
    the whole reason these live in a validator rather than in prose.
    """
    aid = acct.get("account_id") or acct.get("name") or "<unnamed>"
    errs: list[str] = []

    cal = acct.get("calendar")
    if not isinstance(cal, dict):
        errs.append(f"{aid}: missing `calendar` (C22) — acceptance_latency_days, "
                    f"reschedules_90d, consecutive_buyer_reschedules, accepted_by. "
                    f'Write "UNKNOWN" per field; never omit the block.')
    else:
        for f in CALENDAR_FIELDS:
            if f not in cal:
                errs.append(f'{aid}: calendar.{f} missing (C22) — write "UNKNOWN" rather than '
                            f"omitting it, or the relationship family scores as clean.")
        ab = cal.get("accepted_by")
        if "accepted_by" in cal and ab not in ACCEPTED_BY_VALUES:
            errs.append(f"{aid}: calendar.accepted_by={ab!r} — one of "
                        f"{sorted(ACCEPTED_BY_VALUES)}. Who accepts is the signal.")

    nf = acct.get("negotiation_friction")
    if nf is None:
        errs.append(f"{aid}: missing `negotiation_friction` (C24) — one of "
                    f"{sorted(FRICTION_VALUES)}. The customer who negotiates hardest is "
                    f"engaged; the quiet one is the risk.")
    elif nf not in FRICTION_VALUES:
        errs.append(f"{aid}: negotiation_friction={nf!r} — one of {sorted(FRICTION_VALUES)}.")

    if acct.get("first_term"):
        if acct.get("days_since_contract_start") is None:
            errs.append(f"{aid}: first_term account missing `days_since_contract_start` (C23) "
                        f"— the onboarding gate runs before any renewal-window filter.")
        if "activation_fired" not in acct:
            errs.append(f"{aid}: first_term account missing `activation_fired` (C23) — a date "
                        f"string, or null meaning NEVER. Absence is not the same as null.")
    return errs

PATTERN_BONUS = 10          # per matched pattern
PATTERN_BONUS_CAP = 20      # total

BANDS: list[tuple[int, str, float]] = [
    #  upper bound (inclusive), label, band-midpoint probability used for exposure
    (24,  "Secure",    0.05),
    (44,  "Watch",     0.15),
    (64,  "At Risk",   0.35),
    (84,  "High Risk", 0.60),
    (100, "Critical",  0.85),
]

SAVABILITY = {"addressable": 1.2, "partial": 1.0, "structural": 0.5}


def band_for(score: float) -> tuple[str, float]:
    for upper, label, prob in BANDS:
        if score <= upper:
            return label, prob
    return BANDS[-1][1], BANDS[-1][2]


def urgency(days_to_optout: int | None) -> float:
    if days_to_optout is None:
        return 1.0
    if days_to_optout < 0:
        # The notice window has already closed. Either the term auto-renewed (risk deferred
        # to the next cycle) or notice was served. Either way it is no longer a race — the
        # play changes from "save the renewal" to "save the next one".
        return 0.9
    if days_to_optout <= 30:
        return 1.5
    if days_to_optout <= 60:
        return 1.3
    if days_to_optout <= 90:
        return 1.15
    if days_to_optout <= 180:
        return 1.0
    return 0.85


def days_to_optout(renewal: str | None, notice_days: int | None, today: date) -> int | None:
    """The date that actually matters is when they must give notice, not when the term ends."""
    if not renewal:
        return None
    try:
        r = datetime.strptime(renewal, "%Y-%m-%d").date()
    except ValueError:
        return None
    return (r - today).days - (notice_days or 0)


def score_account(acct: dict[str, Any], weights: dict[str, int], today: date) -> dict[str, Any]:
    fams: dict[str, Any] = acct.get("families", {})

    # Renormalise over families that were actually measured. Treating a missing family as
    # zero risk is how data gaps manufacture green accounts.
    present = {k: v for k, v in fams.items() if v is not None and k in weights}
    missing = [k for k in weights if fams.get(k) is None]
    total_w = sum(weights[k] for k in present) or 1
    weighted = sum(float(present[k]) * weights[k] for k in present) / total_w

    contributions = sorted(
        ({"family": k,
          "risk": float(present[k]),
          "weight": weights[k],
          "contribution": round(float(present[k]) * weights[k] / total_w, 2)}
         for k in present),
        key=lambda c: -c["contribution"],
    )

    # ---------------------------------------------------------------- craft derivations
    # Computed, not remembered. Each of these is a mechanism from practitioner-craft.md that
    # would otherwise depend on the writer noticing it at 4pm on a Friday.
    cal = acct.get("calendar") or {}
    derived_floors: list[str] = []
    derived_patterns: list[str] = []

    # C22 — two consecutive reschedules by the economic buyer. Independent of usage.
    cbr = cal.get("consecutive_buyer_reschedules")
    calendar_floor_fired = isinstance(cbr, (int, float)) and not isinstance(cbr, bool) and cbr >= 2
    if calendar_floor_fired:
        derived_floors.append("buyer_reschedule_2x")

    # C24 — frictionless close on an account nobody is invested in.
    rel = fams.get("relationship")
    low_engagement = (
        (isinstance(rel, (int, float)) and not isinstance(rel, bool) and rel >= 50)
        or bool(acct.get("engaged_contacts_below_target"))
    )
    frictionless = acct.get("negotiation_friction") == "frictionless" and low_engagement
    if frictionless:
        derived_floors.append("frictionless_low_engagement")
        derived_patterns.append("frictionless_renewal")

    # C23 — the onboarding gate. Fires at day 60 of the first term, not at T-90, and it runs
    # regardless of how far away the renewal is.
    dsc = acct.get("days_since_contract_start")
    first_term_gate = bool(
        acct.get("first_term")
        and isinstance(dsc, (int, float)) and not isinstance(dsc, bool)
        and dsc >= FIRST_TERM_GATE_DAY
        and not acct.get("activation_fired")
    )
    if first_term_gate:
        derived_patterns.append("failed_launch")

    matched = [p for p in acct.get("patterns", []) if p in PATTERNS]
    for dp in derived_patterns:
        if dp not in matched:
            matched.append(dp)
    bonus = min(len(matched) * PATTERN_BONUS, PATTERN_BONUS_CAP)
    p0_patterns = [p for p in matched if PATTERNS[p][1] == "P0"]
    after_bonus = min(weighted + bonus, 100.0)

    fired = [f for f in acct.get("floors", []) if f in FLOORS]
    for df in derived_floors:
        if df not in fired:
            fired.append(df)
    floor = max((FLOORS[f][0] for f in fired), default=0)
    final = max(after_bonus, float(floor))

    # Band floor: forbids reporting Secure rather than escalating. See BAND_FLOOR_PATTERNS.
    band_floor = max((BAND_FLOOR_PATTERNS[p] for p in matched if p in BAND_FLOOR_PATTERNS),
                     default=0)
    final = max(final, float(band_floor))

    label, prob = band_for(final)
    arr = float(acct.get("arr") or 0)
    dto = days_to_optout(acct.get("renewal_date"), acct.get("notice_period_days"), today)
    u = urgency(dto)
    s = SAVABILITY.get(acct.get("savability", "partial"), 1.0)
    exposure = arr * prob
    priority = exposure * u * s

    coverage = len(present) / len(weights)

    if coverage >= 0.8:
        conf = "High"
    elif coverage >= 0.6:
        conf = "Medium"
    elif coverage >= 0.4:
        conf = "Low"
    else:
        conf = "Insufficient"

    return {
        "account_id": acct.get("account_id"),
        "name": acct.get("name"),
        "arr": arr,
        "weighted_score": round(weighted, 1),
        "pattern_bonus": bonus,
        "floors_fired": [{"key": f, "floor": FLOORS[f][0], "reason": FLOORS[f][1]} for f in fired],
        "floor_applied": floor if floor > after_bonus else None,
        "final_score": round(final, 1),
        "band": label,
        "band_probability": prob,
        "patterns": [{"key": p, "composition": PATTERNS[p][0], "priority": PATTERNS[p][1]}
                     for p in matched],
        # A P0 pattern escalates regardless of the weighted score. Additive scorecards
        # systematically under-rank compounds because each component sits below its own
        # firing threshold while the combination is decisive.
        "escalate_regardless": bool(p0_patterns),
        "p0_patterns": p0_patterns,
        "contributions": contributions,
        "missing_families": missing,
        "coverage": round(coverage, 2),
        "confidence": conf,
        "days_to_optout": dto,
        "optout_status": (
            "UNKNOWN — requires renewal_date and notice_period_days" if dto is None
            else "window closed — notice period has passed" if dto < 0
            else "open"
        ),
        "urgency": u,
        "savability": s,
        "exposure": round(exposure, 0),
        "action_priority": round(priority, 0),

        # ------------------------------------------------------------ required craft reads
        "calendar": {f: cal.get(f, "MISSING") for f in CALENDAR_FIELDS},          # C22
        "calendar_floor_fired": calendar_floor_fired,                              # C22
        "negotiation_friction": acct.get("negotiation_friction", "MISSING"),       # C24
        "frictionless_low_engagement": frictionless,                               # C24
        "band_floor_applied": band_floor if band_floor and band_floor >= after_bonus else None,
        "first_term": bool(acct.get("first_term")),                                # C23
        "days_since_contract_start": dsc,                                          # C23
        "activation_fired": acct.get("activation_fired"),                          # C23
        "onboarding_gate_fired": first_term_gate,                                  # C23
        # Refusal, not a score. A T-90 plan on an implementation that never delivered is
        # negotiating from a position already lost.
        "renewal_plan": (
            "WITHHELD — activation event has never fired (C23); write the implementation "
            "restart and name the unlocking milestone"
            if first_term_gate else "written"
        ),
    }


def render(rows: list[dict[str, Any]]) -> str:
    rows = sorted(rows, key=lambda r: -r["action_priority"])
    out: list[str] = []
    out.append("| # | Account | ARR | Score | Band | P0 | Conf | Cov | Days to opt-out | Exposure | Priority |")
    out.append("|---|---|---|---|---|---|---|---|---|---|---|")
    for i, r in enumerate(rows, 1):
        dto = r["days_to_optout"]
        out.append(
            f"| {i} | {r['name']} | ${r['arr']:,.0f} | {r['final_score']} | {r['band']} | "
            f"{'⚠' if r['escalate_regardless'] else ''} | "
            f"{r['confidence']} | {int(r['coverage']*100)}% | "
            f"{dto if dto is not None else 'UNKNOWN'}{' ⚠closed' if dto is not None and dto < 0 else ''} | ${r['exposure']:,.0f} | ${r['action_priority']:,.0f} |"
        )
    total_arr = sum(r["arr"] for r in rows)
    total_exp = sum(r["exposure"] for r in rows)
    out.append("")
    out.append(f"**ARR assessed ${total_arr:,.0f} · exposure-weighted ARR at risk ${total_exp:,.0f} "
               f"({total_exp/total_arr*100:.1f}%)**" if total_arr else "")
    incomplete = [r for r in rows if r["confidence"] in ("Low", "Insufficient")]
    if incomplete:
        out.append("")
        out.append("**Confidence-limited accounts** (coverage gaps cap what can be claimed):")
        for r in incomplete:
            out.append(f"- {r['name']}: {r['confidence']} — missing {', '.join(r['missing_families']) or 'n/a'}")

    # These three blocks print whether or not anything fired. "Checked, clear" is the point.
    gated = [r for r in rows if r["onboarding_gate_fired"]]
    out.append("")
    out.append("**Onboarding gate (C23)** — first-term accounts, day 60, before any renewal-window filter:")
    out.extend(
        [f"- {r['name']}: day {r['days_since_contract_start']} · activation NEVER · "
         f"renewal plan {r['renewal_plan']}" for r in gated]
        or ["- none — no first-term account passed day 60 without activation"]
    )

    cal_fired = [r for r in rows if r["calendar_floor_fired"]]
    out.append("")
    out.append("**Calendar floor (C22)** — two consecutive economic-buyer reschedules, fires with no usage decline:")
    out.extend(
        [f"- {r['name']}: {r['calendar']['consecutive_buyer_reschedules']} consecutive · "
         f"accepted by {r['calendar']['accepted_by']} · latency "
         f"{r['calendar']['acceptance_latency_days']}d → floor 60" for r in cal_fired]
        or ["- none — no account showed two consecutive buyer reschedules"]
    )

    fric = [r for r in rows if r["frictionless_low_engagement"]]
    out.append("")
    out.append("**Frictionless renewal (C24)** — uncontested close on a low-engagement account, band floored at Watch:")
    out.extend(
        [f"- {r['name']}: friction {r['negotiation_friction']} · band {r['band']} "
         f"(may not be reported Secure) · open the next-cycle risk record at signature"
         for r in fric]
        or ["- none — no uncontested close on a low-engagement account"]
    )
    return "\n".join(out)


def explain(r: dict[str, Any]) -> str:
    out = [f"# {r['name']} ({r['account_id']})", ""]
    out.append(f"**Final {r['final_score']}/100 · {r['band']} · confidence {r['confidence']} "
               f"· coverage {int(r['coverage']*100)}%**")
    out.append("")
    out.append("## Required reads — no valid empty value")
    out.append("| Field | Value |")
    out.append("|---|---|")
    c = r["calendar"]
    out.append(f"| Calendar (C22) — acceptance latency | {c['acceptance_latency_days']} |")
    out.append(f"| Calendar (C22) — reschedules 90d / consecutive by buyer | "
               f"{c['reschedules_90d']} / {c['consecutive_buyer_reschedules']}"
               f"{' → floor 60, fires with no usage decline' if r['calendar_floor_fired'] else ''} |")
    out.append(f"| Calendar (C22) — who accepts | {c['accepted_by']} |")
    out.append(f"| Negotiation friction (C24) | {r['negotiation_friction']}"
               f"{' → Frictionless renewal, band floored at Watch' if r['frictionless_low_engagement'] else ''} |")
    out.append(f"| First term (C23) — days since contract start | "
               f"{r['days_since_contract_start'] if r['first_term'] else 'n/a — not a first term'} |")
    out.append(f"| First term (C23) — activation event | "
               f"{r['activation_fired'] or ('NEVER' if r['first_term'] else 'n/a')} |")
    out.append(f"| Renewal plan status (C23) | {r['renewal_plan']} |")
    if r["band_floor_applied"]:
        out.append("")
        out.append(f"Band floor {r['band_floor_applied']} applied — this account may not be "
                   f"reported Secure. It is a floor on what may be claimed, not a claim that "
                   f"the account sits at {r['band_floor_applied']} risk.")
    out.append("")
    out.append("## Weighted contribution")
    out.append("| Family | Risk | Weight | Contribution |")
    out.append("|---|---|---|---|")
    for c in r["contributions"]:
        out.append(f"| {c['family']} | {c['risk']:.0f} | {c['weight']} | {c['contribution']} |")
    out.append(f"| **Weighted total** | | | **{r['weighted_score']}** |")
    if r["missing_families"]:
        out.append("")
        out.append(f"Renormalised over measured families only. "
                   f"Missing: {', '.join(r['missing_families'])} — "
                   f"treated as UNKNOWN, not as zero risk.")
    if r["patterns"]:
        out.append("")
        out.append("## Compound patterns")
        for p in r["patterns"]:
            out.append(f"- **{p['key']}** ({p['priority']}) — {p['composition']}")
        out.append(f"\nPattern bonus applied: +{r['pattern_bonus']} (cap {PATTERN_BONUS_CAP}).")
        if r["escalate_regardless"]:
            out.append(f"**Escalate regardless of score** — P0 pattern(s) matched: "
                       f"{', '.join(r['p0_patterns'])}.")
    if r["floors_fired"]:
        out.append("")
        out.append("## Override floors")
        for f in r["floors_fired"]:
            out.append(f"- **{f['floor']}** — {f['reason']}")
        if r["floor_applied"]:
            out.append(f"\nFloor **{r['floor_applied']}** overrides the weighted score "
                       f"({r['weighted_score']} + {r['pattern_bonus']}). "
                       f"Commercial decisions beat indicators.")
    out.append("")
    out.append("## Priority arithmetic")
    out.append(f"Exposure = ARR ${r['arr']:,.0f} × band probability {r['band_probability']} "
               f"= ${r['exposure']:,.0f}")
    out.append(f"Action Priority = ${r['exposure']:,.0f} × urgency {r['urgency']} "
               f"× savability {r['savability']} = ${r['action_priority']:,.0f}")
    out.append("")
    out.append("> Band probabilities are the stated midpoints of a rules-based model, not "
               "calibrated forecasts. Replace them with observed renewal rates once the model "
               "has been backtested, and cite the backtest.")
    return "\n".join(out)


def main() -> int:
    ap = argparse.ArgumentParser(description="Deterministic churn-risk scoring.")
    ap.add_argument("input", help="JSON file: list of account objects")
    ap.add_argument("--profile", default="enterprise", choices=sorted(WEIGHT_PROFILES),
                    help="weight profile (default: enterprise)")
    ap.add_argument("--explain", metavar="ACCOUNT_ID", help="print the full derivation for one account")
    ap.add_argument("--json", action="store_true", help="emit JSON instead of markdown")
    ap.add_argument("--today", help="override today's date, YYYY-MM-DD (for reproducible runs)")
    args = ap.parse_args()

    today = datetime.strptime(args.today, "%Y-%m-%d").date() if args.today else date.today()
    weights = WEIGHT_PROFILES[args.profile]

    with open(args.input) as fh:
        accounts = json.load(fh)
    if isinstance(accounts, dict):
        accounts = [accounts]

    problems = [e for a in accounts for e in validate_account(a)]
    if problems:
        print("REFUSED — required craft fields are missing. A dropped field is read as a clean "
              "one, which is exactly the failure these prevent.\n", file=sys.stderr)
        for e in problems:
            print(f"  {e}", file=sys.stderr)
        print("\nWrite \"UNKNOWN\" where the data does not exist. Omission is not an option.",
              file=sys.stderr)
        return 1

    rows = [score_account(a, weights, today) for a in accounts]

    if args.explain:
        match = next((r for r in rows if r["account_id"] == args.explain), None)
        if not match:
            print(f"No account with id {args.explain!r}", file=sys.stderr)
            return 1
        print(explain(match))
        return 0

    print(json.dumps(rows, indent=2) if args.json else render(rows))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
