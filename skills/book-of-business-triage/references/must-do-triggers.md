# Must-Do Triggers

> The eight deadline-driven triggers that put an account at the top of the week before anything is
> scored, what each one checks, the evidence each needs before it becomes a row, and the stop rule
> for a week whose must-dos already exceed the hours. Read when building the must-do block, when
> deciding whether something a stakeholder called "urgent" is actually a must-do, or when the
> must-do total is close to line C.

**Contents**
1. [What makes a row a must-do](#1-what-makes-a-row-a-must-do)
2. [The eight triggers](#2-the-eight-triggers)
3. [The evidence each trigger needs](#3-the-evidence-each-trigger-needs)
4. [The over-commitment stop rule](#4-the-over-commitment-stop-rule)
5. [What is not a must-do](#5-what-is-not-a-must-do)
6. [Anti-patterns](#6-anti-patterns)
7. [Evidence register](#7-evidence-register)

---

## 1. What makes a row a must-do

A must-do is **deadline-driven, not severity-driven**. The test is not "how bad is this account"
but "does a date outside my control pass this week, and does its passing foreclose an option I
still hold". That is why must-dos are never ranked against the rest of the book by return per
hour: an RPH ranking assumes the work can slip a week at a known cost, and these rows are the
ones where slipping a week changes what is possible rather than what is convenient.

Three consequences follow, and all three are load-bearing:

- **They come off the top of capacity.** Must-do hours are subtracted before Step 3 scores
  anything. What remains is what the ranked queue gets to allocate.
- **They are not negotiable against a bigger number.** A $12k account with an opt-out deadline in
  nine days outranks a $400k account with a renewal in seven months, because only one of them has
  a door closing this week. The $400k account is protected by the top-decile reserve (**C31**),
  not by the must-do block.
- **They are the input to the stop rule.** If the must-do block alone exceeds deployable hours,
  the week is a staffing problem and §4 applies.

---

## 2. The eight triggers

| Trigger | Check | Why it is non-negotiable |
| --- | --- | --- |
| **Opt-out deadline ≤30 days and no renewal conversation logged** | `renewal_date − notice_period_days − today ≤ 30` | The deadline is arithmetic. Missing it converts a negotiable renewal into an automatic loss |
| **Auto-renew switched off in the last 7 days** | `subscription.auto_renew_changed_at` | Ranked #1 in the churn-signal priority index; verify within 24 h |
| **Open escalation or P1 aging >14 days with executive visibility** | `ticket.type='escalation'`, `status≠closed` | Trust is the thing being spent, and it compounds daily |
| **Committed follow-up past its promised date** | `interaction.commitments[].due < today` | A broken promise costs more than the work it postponed |
| **Termination terms or data-portability requested** | Legal/procurement thread | Procurement does not do this speculatively |
| **Scheduled customer meeting this week** | Calendar | Already consumed as line D — prep is part of the cost, not an extra |
| **Never-onboarded account past day 60** | `days_since_contract_start > 60` and zero core events | Near-certain loss on the current path; a different play, not a lower priority |
| **Executive- or manager-requested item with a date** | — | Escalate if it does not fit; do not silently drop it |

**Order within the block.** The block is not ranked, but it is *sequenced* by binding date —
earliest date first, ties broken by ARR. Sequencing matters only when the block is at risk of not
finishing, and in that case the rows that finish should be the ones whose doors close first.

**A trigger fires per account, not per signal.** An account with an opt-out deadline in 20 days
*and* an aging escalation is one must-do row carrying both triggers and one hour estimate, not
two rows costed twice. Name both triggers in the row so the reason survives the week.

---

## 3. The evidence each trigger needs

A trigger that cannot be evidenced is a suspicion, and suspicions belong in Step 3 with an
`UNKNOWN` marker, not at the top of the week. Each row below states the minimum that makes the
trigger real and what to do when the evidence is missing.

| Trigger | Minimum evidence | If the evidence is missing |
| --- | --- | --- |
| Opt-out deadline ≤30 days | `renewal_date` **and** `notice_period_days` from the contract or `cs-context` §2, plus the absence of a logged renewal conversation | Use the company default notice period, record it in the Assumptions table with the dates it moves, and keep the row — an assumed 30 days that is really 90 is a row you needed a quarter ago |
| Auto-renew off | The change event with its timestamp and, where available, who changed it | Treat a null `auto_renew` as `UNKNOWN`, not as `true`; verify with the system of record within 24 h before standing the row down |
| Escalation / P1 aging | Ticket id, open date, current status, and whether an executive is on the thread | Without executive visibility it is still a support row; without an open date you cannot age it — ask for the id rather than guessing the age |
| Committed follow-up overdue | The commitment text, the person it was made to, and the promised date | If the commitment lives only in someone's memory, log it now with today's date and treat it as due — an unlogged promise is still a promise |
| Termination / data portability | The thread, the requester and the request date | Never infer this from a support ticket about exports; confirm the intent before it becomes a must-do row, because being wrong here is expensive in both directions |
| Meeting already scheduled | The calendar invite, with attendees | If attendance is unconfirmed, keep the row and cost it — an unattended meeting still consumed the prep |
| Never onboarded past day 60 | `contract_start_date` and zero core events in `usage_event` | A missing usage source makes this **unverifiable, not false** — name it in the Coverage Ledger and ask before writing the account off as onboarded |
| Executive or manager ask | The ask, the requester and the date | Ask for the date. A request without one is a Step 3 row, and saying so is the polite version of pushing back |

**Provenance travels with the row.** Every must-do row carries its source and the as-of date of
that source, exactly as `../../cs-context/references/evidence-standard.md` requires. A must-do
justified by a stale export is how a week gets spent on a renewal that was already signed.

---

## 4. The over-commitment stop rule

**If must-do hours exceed line C — deployable customer hours — stop triaging.** The week is
over-subscribed, and this is a staffing conversation, not a prioritisation one. Producing a
ranked queue on top of an impossible must-do block is a way of agreeing to something nobody can
deliver, and it moves the failure from Monday, where it can be escalated, to Friday, where it can
only be apologised for.

What to produce instead:

1. **The must-do block, costed**, with the running total and the point at which it crosses line C.
2. **The escalation packet** from `capacity-model.md` §9 — the ask, the dollars, the date, the
   options and a recommendation.
3. **A plain statement of which must-dos will not happen**, by name, with the ARR each carries and
   the date each one's door closes. Not "we are at capacity" — the specific rows.
4. **A decision request**, not a status update: who covers these, or which ones the business is
   choosing to let pass.

**The threshold is line C, not line H.** Comparing must-dos against the effective queue budget
understates the problem, because the realisation factor and the reactive reserve are allowances
for work you have not seen yet. If the work you *have* seen already exceeds deployable hours, the
allowances are irrelevant.

**Three weeks running is a different escalation.** One over-subscribed week is bad luck; three is
a structural deficit, and the argument moves from "help me with this week" to the
structural-deficit test in `capacity-model.md` §6.

---

## 5. What is not a must-do

The block only works if it stays small. Everything below feels urgent and is not, and each one
has a correct home.

| Looks like a must-do | Actually | Where it goes |
| --- | --- | --- |
| A newly Critical health band with no date attached | Severity without a deadline | Step 3, where it will score highly on Value and Urgency and win on its merits |
| The loudest inbound of the morning | An interrupt | Step 8's displacement test — reserve first, and it must pass 2 of 3 |
| A large account nobody has touched in a while | A coverage failure, not a deadline | The top-decile reserve (**C31**) if it qualifies, otherwise the maintenance block or the rot sweep |
| "Can you look at this today?" with no date behind it | An ask without a deadline | Reply with a dated commitment and queue it; the commitment then becomes a real trigger next week if it slips |
| An internal report due Friday | Internal load | Line B, not the customer queue |
| An expansion opportunity closing this quarter | Commercially urgent, not deadline-binding | Step 3 on the expansion basis, subject to the health gate in `rph-scoring.md` §5 |
| A renewal 120 days out on a 30-day notice period | Not yet binding — the opt-out date is 90 days away | Step 3 now, must-do when the window opens; see `cadence-by-segment.md` §9 |

**The discipline test.** If more than roughly a third of the ranked book qualifies as a must-do,
the triggers are being read as severity rather than as dates. Re-read §1 and check each row for
an actual date that passes without you.

---

## 6. Anti-patterns

| Anti-pattern | Correction |
| --- | --- |
| Ranking must-dos against the rest of the book by RPH | They come off the top; RPH assumes work can slip, and these rows cannot |
| Using the renewal date instead of the opt-out deadline | `renewal_date − notice_period_days`, always (**R1**) |
| Letting "urgent" without a date create a must-do row | A must-do has a date that passes without you. No date, no row |
| Dropping a must-do silently because the week is full | The stop rule: escalate the block, name the rows that will not happen |
| Costing a scheduled meeting at its invite length | Play duration, including prep and follow-up — `play-durations.md` |
| Treating a null field as a cleared trigger | `UNKNOWN` is not `false`; verify before standing a row down |
| A must-do block larger than a third of the book | The triggers are being read as severity. Re-check each for a real date |

---

## 7. Evidence register

| Claim | Value | Source | Year | Label |
| --- | --- | --- | --- | --- |
| Auto-renew switched off ranks first among near-term churn signals | #1 in the churn-signal priority index | This library's `churn-risk` signal ordering | — | `[P]` |
| Verify an auto-renew change within 24 hours | 24 h | Practitioner | — | `[P]` |
| Escalation / P1 aging threshold for a must-do row | >14 days with executive visibility | Practitioner | — | `[P]` |
| Never-onboarded threshold | day 60 with zero core events | Practitioner; aligns with this library's onboarding skills | — | `[P]` |
| Opt-out proximity that promotes a renewal to a must-do | ≤30 days | Practitioner; scaled by segment in `cadence-by-segment.md` §9 | — | `[P]` |
| Stop-rule threshold | must-do hours > line C | Practitioner rule for this library | — | `[P]` |

**Label key:** `[M]` measured benchmark with a named neutral study · `[P]` practitioner rule of
thumb, no published measurement · `[A]` academic. Every threshold above is `[P]`. Say "commonly
treated as", never "research shows".
