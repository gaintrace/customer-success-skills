# Outreach Queue — <scope> · week of <date>

**Internal above the separator. Customer-facing drafts sit in copy blocks below it.**

**Run parameters:** <scope · capacity in minutes · data as-of date · anything defaulted>. Every
default used is listed in the Assumptions table at the end.

## Bottom Line

<Three sentences: how many triggers fired, how many are queued vs suppressed vs deferred, the ARR
represented by the queue, and the single most time-critical send with its owner and send-by date.>

| | |
|---|---|
| Triggers fired | N across 7 families |
| Queued this week | N touches · $X ARR represented |
| Suppressed | N (reasons in §3) |
| Deferred to next week | N |
| Expired by decay | N |
| Capacity | X minutes budgeted · Y minutes queued · cut line at rank N |
| Register | N Regulated · N Standard |
| Held — no customer sentence on record | N (gate `C4 · acknowledgement source`, listed in §3) |
| Most time-critical | <Account> — <trigger> — send by <date> — <owner> |
| Queue confidence | High / Medium / Low — <criteria met> |

## 1. The Queue

| # | Account | ARR | Trigger | Family | Fired | Strength | Recency | Timing | Priority | Register | Channel | Sender | Recipient | Send by |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | | | | | | | | | | Standard / Regulated | | | | |
| 2 | | | | | | | | | | | | | | |

**Arithmetic, ranks 1–5:** `Priority = (ARR ÷ 1,000) × Strength × Recency × Timing`

1. <Account> · <trigger> — ($X ÷ 1,000) × S × R × T = **P**

## 2. Deferred (below the cut line)

| # | Account | Trigger | Priority | Expires | Disposition |
|---|---|---|---|---|---|
| | | | | | rolls to next week / expires by decay / routed to campaign <name> / escalated to <skill> |

## 3. Suppressed and held

| Account | Trigger | Gate hit | Evidence | Earliest re-eligible date |
|---|---|---|---|---|
| | | | | |

Gates include `C4 · acknowledgement source`: a customer-voiced Regulated trigger — detractor
free-text, escalation, complaint, a promise of ours they chased — with no verbatim sentence of
theirs on record is **held here, not written**. Evidence reads `UNKNOWN — requires <ticket ·
survey verbatim · transcript>`; the re-eligible date is the day that quote is retrieved, and the
recommended action in the meantime is a phone call, not a paraphrase.

## 4. Checked, No Triggers

| Family | Accounts swept | Result |
|---|---|---|
| Product usage & adoption | | |
| Commercial & contract | | |
| Relationship & engagement | | |
| Support & reliability | | |
| Sentiment & VoC | | |
| Billing & payment | | |
| Firmographic & external | | |

---

# Outreach Card — <Account>

*(repeat this block for every queued account)*

**Trigger <ID> · <Family> · Strength <tier> · Priority <score> · ARR $X · Renewal <date> ·
Opt-out <date> (<N> days) · Register <Standard | Regulated>**

**Register is computed from the trigger, not chosen.** Regulated on a detractor response, an
escalation or open Sev-1, a broken integration, a failed payment, an overdue commitment we owe, a
price increase, or a `churn-risk` band of At Risk or worse. Regulated adds three obligations: the
acknowledgement slot below, the four C27 constraints in the copy block, and — where the trigger is
customer-voiced — the `Customer words` evidence row without which nothing is written.

**Why now:** <One sentence: the observable event, and the window in which it is still true.>

### Evidence

| Fact | Value | Provenance | Tier |
|---|---|---|---|
| | | `[system · field · window]` | Observed / Inferred / Unknown |
| **Customer words** *(mandatory when Register = Regulated and the trigger is customer-voiced)* | "<their sentence, verbatim>" — <speaker> | `[Zendesk · ticket.description · 2026-08-14]` | Observed |

Anything unavailable is written `UNKNOWN — requires <source and field>`. No benchmark is
substituted, and no row is dropped. An empty `Customer words` row on a customer-voiced Regulated
trigger stops the message: hold it in §3, do not paraphrase it.

### Recipient

| Name | Title | Role | Altitude | Last contact | Why them |
|---|---|---|---|---|---|
| | | economic_buyer / champion / admin / power_user | practitioner / manager / VP / CFO-CIO | | |

**Not the recipient, and why:** <the person you deliberately did not write to>

### Plan

| Touch | Day | Channel | Sender | Purpose | Ask (verbatim) | Anchor | Send by |
|---|---|---|---|---|---|---|---|
| 1 | 0 | | | | <the question exactly as it will be asked> | <date/window · event · team · artifact> | |
| 2 | +4 | | | | | | |
| 3 | +12 | | permission close | | | | |

**Anchor** ∈ date or window · named event · named team · named artifact. **An empty Anchor cell is
invalid output.** Any ask in the form *how is X going · how are things · are you happy with · any
feedback on · thoughts on* is rejected and regenerated from the Evidence table
(`../references/email-craft.md` §6.1).

**Stop rule:** <any reply · the trigger clears · a fatigue cap is hit · a Sev-1 opens · the
customer asks for less contact>

**Escalation:** <the next rung on the ladder, and the condition that earns it>

### Recommendation

| Action | Owner | By | Expected effect | Success measure |
|---|---|---|---|---|
| | | | | |

*No row without all five fields. An action with no owner and no date is a wish.*

════════════════════════════════════════════════════════════
CUSTOMER-FACING — copy the block below and send as written.
Everything above this line is internal. Do not forward it.
════════════════════════════════════════════════════════════

**Register: Regulated** → slot order is fixed and the four constraints apply to every fence below:

```
1  Acknowledgement   their quoted words where they voiced it; what it cost them where we found it
2  Substance         what is true, what changed, what we are doing about it
3  Ask               one, anchored
```

Zero exclamation marks · no superlatives or intensifiers · every sentence ≤ 20 words, plain full
stops · one apology at most (`R20`). A draft opening with context, explanation, our activity or an
apology fails the pre-send checklist and is rewritten before it goes below the divider.

**Touch 1 · <channel> · from <sender> · to <recipient>**

```text
Subject: <1–4 words, lowercase, no punctuation>

<Body, written out in full and send-ready. 50–100 words. First line does
not begin with "I" or "We". Where the register is Regulated, sentence 1 is
the acknowledgement. At least two data points that trace to the Evidence
table above, stated in the customer's units. Exactly one anchored ask.
One honest exit.>

<Sign-off>
<Sender first name>
```

**Touch 2 · <channel> · day +4** — new information, not a reminder

```text
<Draft, send-ready, its own fence.>
```

**Touch 3 · <channel> · day +12 — permission close**

```text
<Draft, send-ready. Names the silence, states what you will stop doing,
leaves a one-word reply path.>
```

════════════════════════════════════════════════════════════
END CUSTOMER-FACING
════════════════════════════════════════════════════════════

Rules for everything inside a fence: plain text formatted for an email client, blank line between
paragraphs, `•` bullets, no markdown headings, no pipe tables, no `**` bold. Real names, real
dates, real numbers — **no unfilled placeholders**. If a value is genuinely unavailable, delete
that sentence and raise the gap above the divider as `UNKNOWN — requires <source>`. Nothing from
the firewall never-list appears here in any wording: no health score, risk band, ARR at risk,
forecast category, save play, coverage tier, champion-departure inference or assessment of a
named person.

### Coverage Ledger

| Signal family | Source checked | Status | Notes |
|---|---|---|---|
| Product usage & adoption | | ✅ / ⚠️ / ❌ | |
| Commercial & contract | | | |
| Relationship & engagement | | | |
| Support & reliability | | | |
| Sentiment & VoC | | | |
| Billing & payment | | | |
| Firmographic & external | | | |

**Coverage: X / 7 (Y%) → queue confidence capped at <level>.**

Blind spots: <which families produced no triggers because no source is connected, and which
specific triggers that hides — name them by ID.>

Scoring convention: `✅ Complete` = 1.0, `⚠️ Partial` = 0.5, `❌ Missing` = 0. Confidence never
exceeds what coverage permits.

### Assumptions

| # | Assumption | Why it was needed | If wrong |
|---|---|---|---|
| 1 | <the default you ran on> | <the question that went unanswered, or the blank field> | <the concrete thing that changes — a rank, a cut line, a date, a recipient> |

One row per assumption, each with a consequence you can name. "May affect results" is not a
consequence — if you cannot say what would change, you did not need the assumption.
