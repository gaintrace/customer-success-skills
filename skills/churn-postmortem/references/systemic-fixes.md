# Systemic Fixes, Attribution and the Loss Review

> A post-mortem with no systemic fix is a eulogy. This file covers the last third of the work:
> running the five whys so the chain terminates somewhere useful, choosing a fix that matches the
> failure mode, attributing across functions without turning the review into a trial, and running
> the meeting where a quarter's losses become three decisions.

**Contents**
- [1. What a systemic fix is](#1-what-a-systemic-fix-is)
- [2. Five whys, done properly](#2-five-whys-done-properly)
- [3. The termination bank](#3-the-termination-bank)
- [4. Fix patterns by failure mode](#4-fix-patterns-by-failure-mode)
- [5. Fix patterns by reason](#5-fix-patterns-by-reason)
- [6. The fix quality bar](#6-the-fix-quality-bar)
- [7. Attribution without blame](#7-attribution-without-blame)
- [8. The repeat-cause register](#8-the-repeat-cause-register)
- [9. The quarterly loss review](#9-the-quarterly-loss-review)
- [10. The reporting pack](#10-the-reporting-pack)
- [11. Anti-patterns](#11-anti-patterns)

---

## 1. What a systemic fix is

| It is | It is not |
| --- | --- |
| A change to a system, a threshold, a gate, a definition or an owner | A resolution to be more careful |
| Something that would have changed this outcome **and** changes the class of outcome | A fix for this one account |
| Owned by a named function lead with a date inside 90 days | Owned by "CS" or "the team" |
| Verifiable — you can say afterwards whether it shipped | "We'll keep this in mind at renewal" |
| Backtested against past losses **and** past renewals | Justified by a single loss |
| Exactly one per record (`R17`) | A list of eight improvements |

The one-fix rule is the hard part and the reason it works. A review that produces eight
improvements produces none of them; a review that produces one, owned and dated, produces roughly
one. Over four quarters that is four shipped changes, which is more than most CS organisations
manage, and each is traceable to the loss that paid for it.

**Rejected fixes are named, not queued.** Write the "not doing" line into the record with its
reason. A rejected fix that is merely omitted gets re-proposed every quarter by whoever is newest
to the problem.

## 2. Five whys, done properly

The question is **"why did we not prevent it?"** — never "why did the customer leave?", which
produces five restatements of the churn reason and terminates in the customer's own org chart.

**Three stop rules.**

| Rule | Statement | Why |
| --- | --- | --- |
| **Stop at what you own** | Stop at the first cause that is inside our control and that we can change | Going further reaches the customer's internal politics, which is not actionable |
| **Stop before headcount** | Stop before "we should hire more CSMs" | That is a budget argument. It may be true; it is not a root cause, and it lets every review end in the same place |
| **Redirect at human error** | When an answer names a person's mistake, ask what system permitted that decision | A chain terminating on a human terminates on something you cannot fix. This is the blameless-postmortem discipline from Google's SRE practice, applied to revenue rather than uptime `[P]` |

Each answer must be a **fact from the timeline**, with its date. An answer that cannot be sourced
is a hypothesis, and the chain stops there until it can be checked.

**Worked chain A — sponsor loss.**

> **Churn:** $180k, third renewal, non-renewed. Coded `sponsor-loss`, secondary `product-value-gap`.
> 1. *Why did they not renew?* A new VP of Operations ran a consolidation review and chose the ERP's bundled module `[interview · 2026-06-02]`.
> 2. *Why were we not in that review?* We learned of it six weeks before the renewal `[Gmail · 2026-04-11]`.
> 3. *Why so late?* Our only two-way contact was an operations manager who did not sit on the steering group `[interaction · customer_participants, 180 d]`.
> 4. *Why was our only contact at manager level?* The executive sponsor left 11 months earlier and was never replaced in the stakeholder map; multithread depth was 1 for 214 consecutive days `[CRM · Contact.departed_at · 2025-05-20]`.
> 5. *Why did nobody notice a 214-day single-threaded state on a $180k account?* No alert exists for multithread depth, and the health score weights usage at 60% — usage was healthy throughout `[health score v2 · Green at T−90]`.
>
> **Root cause:** the health model measures product usage but not relationship coverage, so a structurally fatal account scored Green for a year.
> **Fix:** add `multithread_depth ≤1 for 90 d` and `exec_sponsor_last_touch >180 d` as independent hard flags that override a healthy usage score. **Owner:** CS Ops. **Due:** 30 days. **Validation:** backtest against the last 12 months of losses plus 60 completed renewals; publish the alert-budget impact.
> **Not doing:** mandating quarterly exec meetings for every account — the cost lands on 400 accounts to fix a signal problem on 12.

**Worked chain B — the play that ran too late.**

> **Churn:** $62k, first renewal, coded `lack-of-adoption`, origin `onboarding`.
> 1. *Why did they not renew?* They never got the second use case live and could not justify the spend `[interview]`.
> 2. *Why did it never go live?* The data migration stalled in month two and was never re-baselined `[PSA · milestone overdue 2025-11-04]`.
> 3. *Why was it not re-baselined?* The onboarding project was marked complete on the go-live date rather than on the activation event `[PSA · project closed 2025-12-01]`.
> 4. *Why was completion defined that way?* The handover checklist has no activation gate; go-live is the exit criterion `[handover template v4]`.
> 5. *Why does the checklist have no activation gate?* It was written for the original single-use-case product and never revised when multi-use-case contracts started being sold.
>
> **Root cause:** onboarding exits on a vendor milestone rather than a customer outcome, so accounts that never activate are handed over as complete.
> **Fix:** the handover checklist requires the activation event fired at least twice in 14 days; projects failing it stay open with an escalation to the onboarding lead. **Owner:** VP Onboarding. **Due:** 45 days. **Validation:** re-score the last two cohorts against the new gate and report how many would have stayed open.
> **Not doing:** extending every onboarding by 30 days by default.

## 3. The termination bank

Chains converge. These are the terminations that recur, with the fix each implies — useful when a
chain stalls at why 3 or 4 and nobody can see the next step.

| Common termination | Owning function | The fix it implies |
| --- | --- | --- |
| No threshold existed for a signal we already stored | CS Ops | Add the threshold; state the alert budget |
| The signal existed but was not on the scorecard | CS Ops | Add the dimension; re-weight only with ≥3 records |
| The alert fired into a dashboard nobody owned | CS leadership | Named owner and a response SLA per alert class |
| The play required more days than the signal gives | CS leadership | Shorten the play, or move the trigger earlier |
| The account was below the coverage threshold for a human touch | CS leadership | Coverage-model change, or a digital play that fits the segment |
| Onboarding exited on a vendor milestone, not a customer outcome | Onboarding | Activation gate in the handover criteria |
| The requirement was never in scope and nobody said so | Sales / deal desk | Qualification gate; a named-exception path with sign-off |
| The renewal was worked from the renewal date, not the opt-out date | CS leadership | Opt-out calendar as the system of record (`R1`) |
| A fix date was committed that we did not own | CS / Product | `R19` — no date without the named owner's agreement |
| A defect recurred and no ticket linked the occurrences | Support | Repeat-issue linking and a per-account cumulative view `[A]` |
| The buying team's usage was never separated from the aggregate | CS Ops | Department segmentation on the usage rollup |
| Nobody owned the account for six weeks after a CSM change | CS leadership | Ownership-gap alert and a handover checklist |

## 4. Fix patterns by failure mode

The fix must match the mode. A training session cannot fix a missing threshold, and a new
dashboard cannot fix a capacity shortfall.

| Mode | Fix pattern | Owner | Ships in | Validation |
| --- | --- | --- | --- | --- |
| `absent` | Instrument the event in the product; add it to the schema | Product / data eng | A quarter | The event appears for ≥90% of accounts within 30 days of release |
| `uninstrumented` | Compute the metric; add it to the scorecard and the schema | CS Ops | Days | Metric populated for ≥90% of accounts; backfilled where possible |
| `unalerted` | Set the threshold, inside the P90 detection lag for that reason | CS Ops | Hours | Backtest on losses **and** a control set of renewals; alert budget stated |
| `unrouted` | Name an owner and a response SLA per alert class; route to a queue with a name on it | CS leadership | Days | Every alert in the class has an owner within 2 business days for a month |
| `unactioned` | Fix the play, the capacity, or the priority — one of the three, chosen explicitly | CS leadership | A planning cycle | Median action lag falls in the next quarter's records |
| `undetectable` | No fix. Record it and move on | — | — | Track the rate; a rising `undetectable` share usually means coding drift, not a stranger world |

**`undetectable` is unavailable to the no-decision family.** A renewal that lapsed always has a
dated antecedent — a stalled opportunity (C13), an unissued PO (C12), a vacant decision owner,
sixty silent days (Z1). Assign the mode that actually applies, which is almost always `unalerted`
(nobody watched opportunity stagnation) or `unrouted` (nobody owned the empty chair).

## 5. Fix patterns by reason

| `primary_reason` | Fix that usually works | Fix that usually does not |
| --- | --- | --- |
| `lack-of-adoption` | An activation gate in the onboarding exit criteria, with the project staying open until it fires | More training content |
| `product-value-gap` | The named gaps ranked by lost ARR, delivered to Product quarterly. Product organisations act on ranked dollars and almost nothing else | A feature request list with no revenue attached |
| `product-quality` | A per-account cumulative friction view — repeat issues, reopens, total time-to-resolution — with a threshold that escalates before the account gives up `[A]` | Faster first-response times on individual tickets |
| `sponsor-loss` | Multithreading floor as a gate (on onboarding completion, and as an independent risk flag), plus a 48-hour exec-to-exec response on departure (`R3`) | Asking CSMs to build more relationships |
| `budget-loss` | A downsell-over-logo-loss policy with pre-approved structures, so the CSM does not need three days of approvals during a two-week window | Discount authority alone |
| `corporate-decision` | Executive relationship coverage above an ARR threshold, owned by a named exec | A better QBR deck |
| `no-decision` | A named renewal decision owner per account, carried on the record, plus a T−180 opt-out-calendar gate that opens the opportunity whether or not anyone has asked for it (`R1`) | Sending a competitive battlecard to a renewal nobody was arguing about |
| `deprioritised` | Re-anchor the success plan to a programme that survived the reorg, or take the downsell deliberately rather than losing the logo | A QBR deck aimed at a programme that no longer has an owner |
| `budget-freeze` | Paper starts at T−90 (`R7`) with the approval threshold and the signature path known in advance, so the freeze is a scheduling problem rather than a surprise | Discount authority. The money was never the objection |
| `orphaned-renewal` | Succession as a play: 48-hour exec-to-exec on departure (`R3`), and a named decision owner re-established before the opt-out date, not after | Asking the CSM to rebuild the relationship alone, on the timeline the notice period allows |
| `competitive-displacement` | Competitive enablement tied to the re-bid play, plus a trigger on procurement or competitor mentions | A battlecard nobody reads at renewal time. **Refused outright where decision-process ≥3 and competitive ≤1** — that loss had no opponent to enable against |
| `involuntary` | Dunning sequence, retry logic, card-updater, and pre-expiry outreach. The cheapest retention work available | Anything owned by CS |

## 6. Attribution without blame

Attribution answers "which functions could have changed this?", weighted, summing to 100. It is
not a verdict on people, and the moment it becomes one the data stops being honest — defensive
coding is a far larger threat to a loss-review programme than imprecise weighting.

**Rules.**

| Rule | Detail |
| --- | --- |
| Function and mechanism, never a person | "Onboarding — exit criteria allowed handover without activation", not "Sam closed the project early" |
| Weights sum to 100 | Forces a real allocation. Everything-at-fault is nothing-at-fault |
| A `None — exogenous` row is allowed and often correct | Some losses are 100% exogenous. Coding them 30% CS to seem rigorous corrupts the aggregate |
| The facilitator writes it; the owner reviews and may dissent on the record | One line of dissent, with reasoning. Never average two positions |
| Include a "seen before?" count | Prior post-mortems with the same attribution. On the third appearance, the finding is an unshipped fix, not a cause |
| Never attribute to a departed employee | It is unfalsifiable and it teaches everyone still there what happens after they leave |

**Shape.**

| Function | Weight | Mechanism | What would have had to be different | Seen before? |
| --- | --- | --- | --- | --- |
| CS Ops | 45% | No threshold on multithread depth; relationship coverage absent from the scorecard | An alert at 90 days single-threaded, in May 2025 | 3rd time |
| Customer Success | 25% | Account worked from the renewal date rather than the opt-out date | Renewal motion opened at T−180 from opt-out | 2nd time |
| Sales | 20% | Sole champion at manager level at signature; no exec sponsor recorded | Exec sponsor named as a closing requirement above $150k | 1st time |
| Product | 10% | The reconciliation gap raised in March 2025 was never scheduled or answered | A dated answer, including a no | 4th time |
| **Total** | **100%** | | | |

## 7. The repeat-cause register

The table that makes the programme real. One row per distinct cause, carried across quarters.

| Column | Rule |
| --- | --- |
| Cause | The root cause as written in the record, not the reason code |
| Appearances | Count across all records, all time |
| ARR lost total | Cumulative, ARR-weighted — this is the number that funds the fix |
| Fix promised | The systemic fix from the record where it first appeared |
| Owner · Due | As recorded then, not as re-negotiated since |
| Shipped? | Yes / No / Partial, with the date |

**The rule that gives it teeth:** a cause appearing for the third time with its fix unshipped is
escalated to the CCO with the cumulative ARR attached, and the review does not propose a new fix
for it. Proposing a second fix for a cause whose first fix never shipped is how a loss-review
programme becomes theatre — and the register is the only artifact that makes that visible.

## 8. The quarterly loss review

Sixty minutes. It is a **causes** meeting, not an accounts meeting; a review that walks accounts
one by one runs out of time at account four and never reaches a decision.

| | |
| --- | --- |
| **Cadence** | Quarterly for the cohort review; individual records written within 30 days of each decision date |
| **Facilitator** | CS Ops or a manager who owned none of the accounts |
| **Attendees** | CS leadership, CS Ops, and a named person from Product, Support, Onboarding and Sales. Account owners attend as evidence, not as defendants |
| **Pre-read** | Circulated 48 hours ahead: the cohort roll-up, the repeat-cause register, and the three fix proposals. No pre-read, no meeting |
| **Ground rule** | Function and mechanism only. The facilitator stops any sentence that names an individual |
| **Output** | Three decisions, each with an owner and a date, written into the register before anyone leaves |

**Agenda.**

| Min | Item | Content |
| --- | --- | --- |
| 0–5 | The number | ARR lost, against plan and against the prior quarter. Reason mix **by ARR**. No commentary yet |
| 5–15 | Detection | Median and P90 detection lag, recognition lag, action lag, the count flagged after the decision, and the failure-mode distribution |
| 15–25 | The repeat-cause register | Every cause on its ≥2nd appearance, and the shipped status of every fix promised in prior quarters. **This is read before any new cause is discussed** |
| 25–40 | The two or three teaching losses | Chosen for what they show, not for their size. One should be a Green-at-T−90 record |
| 40–50 | Savability distribution | A+B vs C+D by ARR, with the >60% honesty check applied out loud |
| 50–60 | Decisions | Three fixes maximum, each with an owner, a date and a validation. Written down live |

**Losses not reviewed this cycle are listed with a reason and a revisit date** (`R14`). An
unwritten decision to skip a loss is indistinguishable from an oversight and repeats silently.

## 9. Fix quality bar

Run this before a fix leaves the room.

- [ ] It names a system, threshold, gate, definition or owner — not an intention
- [ ] It would have changed **this** outcome, and it changes the **class** of outcome
- [ ] It matches the failure mode, not the symptom
- [ ] Owner is a named function lead, not "CS" and not the most junior person present
- [ ] Due date is inside 90 days
- [ ] Validation is a backtest against past losses **and** a control set of renewals
- [ ] The alert-budget or workload impact is stated in numbers
- [ ] A "not doing" line names the rejected alternative and why
- [ ] It is the only primary fix for this record (`R17`)
- [ ] It is entered in the repeat-cause register with its shipped status open
- [ ] If it changes a weight, threshold or lead time, ≥3 records support it (`R22`)
- [ ] It does not depend on a date owned by someone not in the room (`R19`)

## 10. The reporting pack

| Artifact | Cadence | Audience | Contents |
| --- | --- | --- | --- |
| Loss-review record | Per loss | CS leadership, the account team | The full record from the Output Template |
| Reason mix by ARR | Monthly | VP CS | By reason, segment, tenure band, ARR band, with movement against the prior quarter |
| Detection-lag report | Quarterly | CS Ops, VP CS | Median and P90 by reason, failure-mode distribution, negative-lead-time count |
| Savability distribution | Quarterly | CCO | A+B vs C+D, with the trend in `unactioned` — the capacity signal |
| Instrumentation backlog | Quarterly | CS Ops | Signals seen ≥3 times, still uninstrumented, ranked by ARR behind them |
| Product feedback | Quarterly | CPO | ARR lost to `product-value-gap` and `product-quality`, with named gaps ranked by lost ARR |
| Qualification feedback | Quarterly | CRO | ARR lost coded `should never have been sold`, by source, segment and rep cohort — mechanism, never individuals |
| Repeat-cause register | Quarterly | CCO | Every cause on its ≥2nd appearance with fix status |

## 11. Anti-patterns

| Anti-pattern | Correction |
| --- | --- |
| Eight action items | One fix, owned, dated (`R17`). Name the rejected ones |
| A fix owned by "CS" | A named function lead |
| A fix with a date beyond the quarter | Inside 90 days, or split it so something ships inside 90 days |
| A fix validated only against losses | Control set of renewals, ≥3× the loss set |
| The losing CSM facilitating their own review | `facilitator ≠ account.owner_csm`, enforced as a field |
| Attribution naming individuals | Function and mechanism. The facilitator interrupts |
| A second fix for a cause whose first fix never shipped | Escalate the unshipped fix with cumulative ARR; do not propose a new one |
| Reviewing accounts one at a time in the quarterly | Group by cause; accounts are the appendix |
| Skipping the register because it is uncomfortable | It is read before any new cause is discussed |
| "We'll be more careful at renewal" | Not a fix. It names no system and cannot be verified |
| Ending every chain at headcount | Stop rule 2. Keep going, or stop at the last thing you own |
| Deciding the reason in the meeting | Reasons are coded from timelines beforehand. The meeting decides fixes |
