#!/usr/bin/env python3
"""
Deterministic arithmetic for a renewal negotiation. No network, no model judgement.

    python3 concession_math.py gates      --signs "Dana Osei" --signer-present yes \
                                          --last-business-conversation 2026-07-02 \
                                          --procurement-active yes --today 2026-08-28
    python3 concession_math.py ladder     --arr 480000 --tenure 4 --cost-of-capital 0.10
    python3 concession_math.py discount   --arr 480000 --pct 12 --tenure 4 --escalator 0.04
    python3 concession_math.py uplift     --pct 5
    python3 concession_math.py multiyear  --arr 480000 --escalator 0.04 --years 3 --discount 8

`gates` is the one that refuses. It implements C14 (test authority first) and C10 (never let
procurement be the only live thread) as a computed PASS/FAIL, so the ladder is gated by
arithmetic rather than by the writer remembering.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import sys

BUSINESS_THREAD_LIMIT_DAYS = 21

AUTHORITY_TEST = (
    "If I could get that approved, is this something you could sign this quarter?"
)
AUTHORITY_TEST_SIGNER_UNKNOWN = (
    "Before I take a number to our deal desk — who signs the order form on your side, "
    "and are they behind the figure you have asked me for?"
)


def sigfig2(x: float) -> str:
    """Two significant figures, per SKILL-STANDARD §4F. Derived figures are not stated to the dollar."""
    if x == 0:
        return "$0"
    neg = x < 0
    x = abs(x)
    if x >= 1_000_000:
        v, unit = x / 1_000_000, "m"
    elif x >= 1_000:
        v, unit = x / 1_000, "k"
    else:
        v, unit = x, ""
    v = round(v, 1) if v < 10 else round(v)
    return f"{'-' if neg else ''}${v:g}{unit}"


def parse_date(s: str) -> dt.date:
    return dt.datetime.strptime(s.strip(), "%Y-%m-%d").date()


# ─────────────────────────────────────────────────────────────────────────────
# gates — C14 authority, C10 business thread
# ─────────────────────────────────────────────────────────────────────────────

def cmd_gates(a: argparse.Namespace) -> int:
    today = parse_date(a.today) if a.today else dt.date.today()

    signs = (a.signs or "").strip()
    signer_known = bool(signs) and signs.upper() != "UNKNOWN"
    signer_present = (a.signer_present or "").strip().lower() in {"yes", "y", "true"}
    gate_a = signer_known and signer_present

    procurement_active = (a.procurement_active or "").strip().lower() in {"yes", "y", "true"}

    if a.last_business_conversation and a.last_business_conversation.upper() != "UNKNOWN":
        last = parse_date(a.last_business_conversation)
        days = (today - last).days
        days_str = str(days)
        days_known = True
    else:
        days = None
        days_str = "UNKNOWN — requires interaction history"
        days_known = False

    # Fail closed. An unknown last business conversation is treated as past the limit,
    # because the account where nobody logged the interaction is the account where it
    # did not happen.
    thread_stale = (not days_known) or days > BUSINESS_THREAD_LIMIT_DAYS
    gate_b = not (procurement_active and thread_stale)

    if gate_a and gate_b:
        action = "Ladder open. Offer one rung, with its What-we-get named in the same sentence."
    elif not gate_a:
        action = (
            "AUTHORITY TEST, not a concession (C14). Say: "
            f'"{AUTHORITY_TEST}"'
            if signer_known
            else f'AUTHORITY TEST, not a concession (C14). Say: "{AUTHORITY_TEST_SIGNER_UNKNOWN}"'
        )
    else:
        action = (
            "RE-OPEN A BUSINESS THREAD before any commercial reply (C10). Book a non-commercial "
            "conversation with the economic buyer on a named outcome — not price, not paper."
        )

    out = {
        "today": today.isoformat(),
        "gate_a_authority": "PASS" if gate_a else "FAIL",
        "gate_a_reason": (
            "signer named and in the conversation" if gate_a
            else ("signs is UNKNOWN" if not signer_known else f"{signs} is not in the conversation")
        ),
        "days_since_business_thread": days_str,
        "business_thread_limit_days": BUSINESS_THREAD_LIMIT_DAYS,
        "procurement_active": procurement_active,
        "gate_b_business_thread": "PASS" if gate_b else "FAIL",
        "gate_b_reason": (
            "procurement not active" if not procurement_active
            else ("business thread live within 21 days" if gate_b
                  else f"procurement active and business thread stale ({days_str})")
        ),
        "ladder_status": "OPEN" if (gate_a and gate_b) else "BLOCKED",
        "recommended_action": action,
        "authority_test_wording": AUTHORITY_TEST if signer_known else AUTHORITY_TEST_SIGNER_UNKNOWN,
    }
    print(json.dumps(out, indent=2))
    return 0 if out["ladder_status"] == "OPEN" else 3


# ─────────────────────────────────────────────────────────────────────────────
# ladder — what each rung costs this account
# ─────────────────────────────────────────────────────────────────────────────

RUNGS = [
    (1, "Net 30 → Net 45", "payment_days", 15),
    (1, "Net 30 → Net 60", "payment_days", 30),
    (2, "Waive the uplift", "uplift_waiver", None),
    (3, "Enablement / training credits / advisory seat", "service", None),
    (4, "0–5% discount", "discount", 5),
    (5, "5–10% discount", "discount", 10),
    (6, "10–15% discount", "discount", 15),
    (7, "15–25% discount", "discount", 25),
    (8, ">25% discount", "discount", 30),
]


def cmd_ladder(a: argparse.Namespace) -> int:
    arr, tenure, coc, uplift = a.arr, a.tenure, a.cost_of_capital, a.uplift
    print(f"Ladder cost — ARR {sigfig2(arr)} · assumed tenure {tenure}y · cost of capital {coc:.0%}")
    print(f"{'Rung':<5}{'Give':<46}{'Annual':>12}{'Lifetime':>12}")
    for rung, name, kind, param in RUNGS:
        if kind == "payment_days":
            annual = arr * (param / 365) * coc
            lifetime = annual * tenure
        elif kind == "uplift_waiver":
            annual = arr * uplift
            lifetime = sum(arr * ((1 + uplift) ** y - 1) for y in range(1, tenure + 1))
        elif kind == "service":
            annual = a.service_cost
            lifetime = a.service_cost
        else:
            pct = param / 100
            annual = arr * pct
            lifetime = sum(arr * pct * ((1 + uplift) ** (y - 1)) for y in range(1, tenure + 1))
        print(f"{rung:<5}{name:<46}{sigfig2(annual):>12}{sigfig2(lifetime):>12}")
    print("\nEvery rung requires a What-we-get in the same row (C12). A rung with an empty "
          "What-we-get cell is invalid output, not an incomplete one.")
    return 0


def cmd_discount(a: argparse.Namespace) -> int:
    pct = a.pct / 100
    print(f"Discount lifetime cost — ARR {sigfig2(a.arr)} · {a.pct:g}% off · "
          f"escalator {a.escalator:.1%} · tenure {a.tenure}y")
    print(f"{'Year':<6}{'List path':>14}{'Discounted path':>18}{'Gap':>12}")
    list_total = disc_total = 0.0
    for y in range(1, a.tenure + 1):
        list_y = a.arr * ((1 + a.escalator) ** (y - 1))
        disc_y = a.arr * (1 - pct) * ((1 + a.escalator) ** (y - 1))
        list_total += list_y
        disc_total += disc_y
        print(f"{y:<6}{sigfig2(list_y):>14}{sigfig2(disc_y):>18}{sigfig2(list_y - disc_y):>12}")
    print(f"{'Total':<6}{sigfig2(list_total):>14}{sigfig2(disc_total):>18}"
          f"{sigfig2(list_total - disc_total):>12}")
    print("\nThe forgone escalator on the reduced base is inside this figure. State it to two "
          "significant figures (§4F).")
    return 0


def cmd_uplift(a: argparse.Namespace) -> int:
    u = a.pct / 100
    be = u / (1 + u)
    print(f"Uplift {a.pct:g}% is value-neutral at {be:.1%} of added churn probability.")
    print("Arithmetic for ordering the decision, not a forecast (R22). No probability is stated "
          "without a cited backtest.")
    return 0


def cmd_multiyear(a: argparse.Namespace) -> int:
    esc, disc = a.escalator, a.discount / 100
    print(f"Structures — ARR {sigfig2(a.arr)} · escalator {esc:.1%} · {a.years}y term")
    annual = [a.arr * ((1 + esc) ** (y - 1)) for y in range(1, a.years + 1)]
    multi = [a.arr * (1 - disc) * ((1 + esc) ** (y - 1)) for y in range(1, a.years + 1)]
    flat = [a.arr * (1 - disc)] * a.years
    for label, path in (("1yr + escalator", annual),
                        (f"{a.years}yr @ -{a.discount:g}% w/ escalator", multi),
                        (f"{a.years}yr @ -{a.discount:g}% price-locked flat", flat)):
        total = sum(path)
        eff = total / a.years
        print(f"  {label:<40}{' '.join(sigfig2(v) for v in path):<30}"
              f"total {sigfig2(total)}  eff/yr {sigfig2(eff)}")
    print("\nWrite each year's fee in dollars on the order form, never as a formula.")
    return 0


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)

    g = sub.add_parser("gates", help="C14 authority gate + C10 business-thread gate")
    g.add_argument("--signs", default="", help="named signer, or UNKNOWN")
    g.add_argument("--signer-present", default="no", help="yes/no — is the signer in the conversation")
    g.add_argument("--last-business-conversation", default="UNKNOWN",
                   help="YYYY-MM-DD of the last non-commercial conversation, or UNKNOWN")
    g.add_argument("--procurement-active", default="no", help="yes/no")
    g.add_argument("--today", default="", help="YYYY-MM-DD override")
    g.set_defaults(func=cmd_gates)

    l = sub.add_parser("ladder", help="cost every rung for this account")
    l.add_argument("--arr", type=float, required=True)
    l.add_argument("--tenure", type=int, default=4)
    l.add_argument("--cost-of-capital", type=float, default=0.10)
    l.add_argument("--uplift", type=float, default=0.04)
    l.add_argument("--service-cost", type=float, default=0.0)
    l.set_defaults(func=cmd_ladder)

    d = sub.add_parser("discount", help="lifetime cost of a discount")
    d.add_argument("--arr", type=float, required=True)
    d.add_argument("--pct", type=float, required=True)
    d.add_argument("--tenure", type=int, default=4)
    d.add_argument("--escalator", type=float, default=0.04)
    d.set_defaults(func=cmd_discount)

    u = sub.add_parser("uplift", help="break-even added churn probability for an uplift")
    u.add_argument("--pct", type=float, required=True)
    u.set_defaults(func=cmd_uplift)

    m = sub.add_parser("multiyear", help="compare structures")
    m.add_argument("--arr", type=float, required=True)
    m.add_argument("--escalator", type=float, default=0.04)
    m.add_argument("--years", type=int, default=3)
    m.add_argument("--discount", type=float, default=0.0)
    m.set_defaults(func=cmd_multiyear)

    a = p.parse_args()
    return a.func(a)


if __name__ == "__main__":
    sys.exit(main())
