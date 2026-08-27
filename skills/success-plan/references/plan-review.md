# Plan Review, RAG and Recovery

> The governance half of a success plan: the monthly update, the plan-led business review, the
> arithmetic behind a status, objective RAG criteria that cannot be gamed, what to do when a
> milestone is missed, and when to re-baseline rather than re-date.
>
> Evidence labels: `[M]` measured · `[PROD]` published production configuration · `[V]` vendor ·
> `[P]` practitioner · `[A]` academic.

**Contents**
- [1. The cadence](#1-the-cadence)
- [2. The monthly update](#2-the-monthly-update)
- [3. The plan-led business review](#3-the-plan-led-business-review)
- [4. Attainment arithmetic](#4-attainment-arithmetic)
- [5. RAG criteria and the watermelon problem](#5-rag-criteria-and-the-watermelon-problem)
- [6. The missed-milestone protocol](#6-the-missed-milestone-protocol)
- [7. The Concern conversation](#7-the-concern-conversation)
- [8. Re-baseline triggers and the re-discovery agenda](#8-re-baseline-triggers-and-the-re-discovery-agenda)
- [9. Plan health signals](#9-plan-health-signals)
- [10. Portfolio view for a manager](#10-portfolio-view-for-a-manager)
- [11. Anti-patterns](#11-anti-patterns)

---

## 1. The cadence

| Activity | Cadence | Owner | Fails when |
| --- | --- | --- | --- |
| Objective status updated as evidence changes | Within 5 business days; **never batched at period end** | CSM | Batched at quarter end, which is how a plan becomes a self-graded exam. GitLab's published guidance treats the plan dashboard as live data rather than a quarter-end exercise `[PROD]` |
| Written plan update to the executive sponsor | Monthly, with a summary of what changed `[P]` | CSM | The plan only exists in the room at reviews |
| Milestone check with the customer owner | Fortnightly while a milestone is open | Customer owner + CSM | A slip is discovered at the review |
| Plan-led business review — the plan is agenda item one | Quarterly, or per tier entitlement | CSM + champion | The review presents *about* the plan instead of working *on* it |
| Full re-baseline | On any §8 trigger, or annually | CSM + sponsor | The plan aims at last year's objectives |
| Renewal evidence check | Opt-out deadline − 120 days | CSM + AM | The value case is assembled after the decision has formed |

**No decision to make means no review.** A review held because the calendar said so trains the
customer that these meetings are ceremonial, and the one that matters gets declined with the rest
(**R15**). Send the monthly update, give the hour back, and say why.

---

## 2. The monthly update

One page. Sent, not presented. Written for an executive who will read it on a phone.

| Block | Content | Length |
| --- | --- | --- |
| **What moved** | Per objective: the metric, where it was at the last update, where it is now, and the status | 3–5 lines |
| **What we closed** | Milestones completed since the last update, with the evidence | 2–3 lines |
| **What slipped** | Anything late, with the new date and the reason. Lead with this if it exists | 1–3 lines |
| **What we need from you** | Named person, specific ask, date | 1–2 lines |
| **Next** | The next milestone and its date | 1 line |

Rules: the same five blocks every month so it is scannable · never a status without a number ·
never a slip without a new date and a cause · never an ask without a named person and a date · and
if nothing moved, say that, because a month of no movement is the most important thing the sponsor
could learn.

---

## 3. The plan-led business review

The plan **is** the agenda, not an appendix to it. Hayer's framing is the operating instruction:
the review asks what we committed to, what we accomplished, what has changed in your business, and
what needs to be adjusted `[P]`.

| # | Segment | Minutes (of 45) | Who leads | Exit |
| --- | --- | --- | --- | --- |
| 1 | Objectives check — are these still your objectives? | 5 | Customer sponsor | Confirmed, amended, or one retired |
| 2 | Attainment against each goal: baseline → today → target | 10 | CSM, with the customer's own measurement owner confirming the numbers | Agreed status per objective |
| 3 | What changed in your business | 8 | Customer | New objectives surfaced, or existing ones re-ranked |
| 4 | Blockers and the register | 8 | Both | Owners and dates on every open row |
| 5 | Decisions needed today | 10 | CSM | Each decision made, deferred with a date, or escalated with a name |
| 6 | Next period commitments | 4 | Both | Milestones and owners for the next cycle |

**The customer's measurement owner confirms the numbers, not us.** A number the customer's own
person read out is worth ten that we presented. Where they cannot confirm it, the objective is
reported as unmeasured this period, not as on track.

**Preparation gates.** If any of these fails, move the review or change its purpose and say so:
objectives unconfirmed in the last two quarters · no baseline for two or more objectives · the
economic buyer not attending and not represented · fewer than two decisions on the agenda.

---

## 4. Attainment arithmetic

Show the arithmetic. A status without visible arithmetic is an opinion.

```
attainment      = (current − baseline) / (target − baseline)          # signed for direction
elapsed         = (today − start_date) / (target_date − start_date)
schedule_var    = elapsed − attainment                                 # percentage points; positive = behind
```

| Term | Rule |
| --- | --- |
| Direction | For a metric that must fall, invert the numerator so attainment rises as the metric improves |
| Attainment above 1.0 | Report it as achieved and check the measurement before celebrating |
| Attainment below 0 | The metric moved away from the target. Report the sign; never clip it to zero |
| Elapsed | Uses the objective's own start and target dates, not the contract term |
| Unmeasured periods | Do not interpolate. Report `UNKNOWN — requires <source>` and treat the objective as Watchpoint |

**Worked.** Baseline 412, target 290, current 355. Start 2026-04-01, target 2026-12-31, today
2026-08-27. Attainment = (412 − 355) / (412 − 290) = 57/122 = 0.47. Elapsed = 148/274 = 0.54.
Schedule variance = +7pp — inside the 10pp band, so **On Track**, provided the leading indicator is
at threshold and no blocking dependency is open.

`../scripts/plan_health.py` computes this deterministically for a whole plan; use it past two or three
goals so the arithmetic is auditable rather than retyped.

---

## 5. RAG criteria and the watermelon problem

A watermelon status is green on the outside and red the whole way through. It has two causes, and
both are structural rather than personal: **the criteria were never defined**, so green means
whatever the person reporting needs it to mean; and **reporting red is punished**, so nobody does it
until the fact is undeniable. Fix both. Define the thresholds before the plan starts, apply them
identically every period, and make the first red on a plan a normal event rather than an escalation.

| Status | Entry criteria |
| --- | --- |
| **On Track** | Leading indicator at or above threshold **and** schedule variance ≤10pp **and** no open blocking dependency |
| **Watchpoint** | Leading indicator below threshold for one period, **or** schedule variance 10–25pp, **or** a blocking dependency with a dated mitigation, **or** the leading indicator has never been measured |
| **Concern** | Outcome flat or moving away from target for two consecutive periods, **or** schedule variance >25pp, **or** a blocking dependency with no dated mitigation, **or** the customer owner changed and has not been replaced |
| **Closed — Verified** | A named customer person confirmed the outcome, with a date |
| **Closed — Retired** | Closed without achievement, with the reason and a revisit date recorded (**R14**) |

**Three guards that stop the gaming:**

| Guard | Rule |
| --- | --- |
| **Unmeasured is Watchpoint** | Never On Track on an indicator nobody has measured. Unmeasured is not fine |
| **Status is derived, not chosen** | Compute it from the thresholds first; a manual override is allowed, written on the row, with the reason |
| **Two-period rule for Concern** | One bad period is noise; two is a trend. Say which one you are looking at |

`Delivered` is not a status a customer sees, and it never counts as achievement. Only `Verified` —
customer-confirmed — enters a business review, a renewal case or a retention number `[PROD]`. This
single rule removes most success-plan inflation.

---

## 6. The missed-milestone protocol

Inside 5 business days of the miss, in this order:

| # | Step | Detail |
| --- | --- | --- |
| 1 | **Name it in writing before they do** | One sentence, first line, no preamble. Whoever raises the slip first sets the frame |
| 2 | **State the cause once, without defence** | "The article authoring did not get SME time in August." Not an explanation of why that was reasonable |
| 3 | **Re-forecast once** | A new date and what changed to make it real. Not a range, not "as soon as possible" |
| 4 | **Second slip on the same milestone: re-plan** | A date that slips twice is fictional. Re-plan the objective — scope, sequence or target — rather than issuing a third date |
| 5 | **State the effect on the objective** | Does the target value change, the target date, or neither? Answer explicitly. Silence here is read as both |
| 6 | **Log the cause in the register** | So the pattern is visible at review. Three slips from the same cause is a structural finding, not bad luck |

Apologise once, then act (**R20**). A second apology asks the customer to absolve you, which makes
your feelings their job. And never commit a date you do not own — a roadmap date, a fix date, a
delivery date — without the named owner having agreed it (**R19**).

---

## 7. The Concern conversation

When an objective enters Concern, the conversation is with the executive sponsor, not only the
champion, and it happens inside two weeks.

| Beat | What you say | What you must not do |
| --- | --- | --- |
| **Open with the position** | "The close-cycle objective is off track. We are at 8 days against a target of 4, and the September close will not make it." | Open with context or activity |
| **Cause, once** | "Two of six entities have not had their reconciliation rules configured, because the data mapping needed 30 hours from your finance systems team that were not allocated." | Assign blame to a named person on either side |
| **The choice, framed** | "Three options: move the target date to the December close; reduce scope to four entities and hit the date; or find the 30 hours. Each has a cost and I have the numbers." | Present one option and call it a recommendation without alternatives |
| **The ask** | "I need a decision from you by 12 September, and if it is option three I need a name." | Leave the ask implicit |
| **What we change** | "Fortnightly checks with a named owner on each entity, and I will flag any entity that has no owner within a week." | Promise more effort with no mechanism |

If the objective cannot be recovered, retire it with a reason and a revisit date rather than
carrying it as a permanent Watchpoint. A plan carrying a dead objective loses credibility for the
live ones.

---

## 8. Re-baseline triggers and the re-discovery agenda

| Trigger | Effect on the plan | First action |
| --- | --- | --- |
| Executive sponsor change | All objectives drop to `Proposed` | 30-minute briefing on why the programme exists, built from the original business case, not a demo |
| Champion departure | Objectives they owned drop to `Proposed` | Identify the successor from admin logs, ticket ownership and org data; exec-to-exec outreach inside 48 hours (**R3**) |
| Stated strategy or fiscal plan changes | Objectives re-ranked; some retired | Ask which of the current objectives survives the new plan |
| Reorganisation moving the owning team | Owners invalid; baselines may be too | Re-confirm the population behind every baseline |
| M&A on either side | Full re-baseline | Establish who now owns the budget line |
| Contract change (seats, products, term) | Scope and targets re-derived | Re-derive targets from the new entitlement |
| Their metric definition changes | Baseline invalid | Re-baseline and write a changelog row |
| A competing internal programme starts | Capacity risk | Register row with a named owner and a review date |
| Our roadmap changes under a committed initiative | Objective at risk | Name it, with a date we own, or retire the objective |
| Two consecutive Concern periods | Objective re-planned or retired | The Concern conversation in §7 |

**The re-discovery agenda** — 30 minutes, and it is not a status update:

1. Here is what your predecessor set as the objectives, when, and why (quote it, with dates).
2. Here is what has been achieved against them, with the evidence and the customer person who
   confirmed it.
3. Which of these are still yours?
4. What is now on your scorecard that is not in this plan?
5. Who owns each of these on your side today?
6. What would make you cancel this programme? — asked directly, because the answer is the register.

**Inherited acceptance is not acceptance.** Until the new sponsor has agreed the objective, the
baseline, the success criteria and the timeline, the plan is `Proposed` and reports as such.

---

## 9. Plan health signals

Leading indicators that a plan is decaying, before the objectives do. These are `[DESIGN]`
constructs — calibrate the thresholds against your own renewed and churned cohorts before treating
them as thresholds rather than prompts.

| Signal | Compute | Prompt |
| --- | --- | --- |
| Objectives with no measured baseline | count / total objectives | Above 1 in 3, the plan cannot produce a renewal argument |
| Milestones with a customer owner | count / total milestones | Below 40%, the plan is our task list |
| Days since the customer last confirmed anything in the plan | today − `last_customer_confirmation` | Past 60 days, treat the plan as unconfirmed regardless of its statuses |
| Milestones overdue and owned by the customer | count | The clearest single sign that the plan is ours, not theirs |
| Slip-twice count | milestones re-dated ≥2 times | Each one is a re-plan that did not happen |
| Objectives at `Delivered` but never `Verified` | count | Work finished, value never confirmed — the inflation the lifecycle exists to prevent |
| Days since any milestone completed | today − `last_milestone_completed` | Past 120 days on an active plan, the programme has stalled |
| Leading indicators never measured | count | Each one is an objective reporting a status it has not earned |
| Objectives whose executive owner has changed | count | Each triggers §8 |

**Trap:** overdue-milestone counts on a plan the customer never agreed to are meaningless. Check
the acceptance state before reading any of these numbers.

---

## 10. Portfolio view for a manager

One table across a book, sorted by days to the opt-out deadline. This is the artifact a VP uses to
find the plans that will not produce a renewal argument in time.

| Account | ARR | Opt-out (days) | Objectives (P/A/D/V) | With baseline | Customer-owned milestones | Days since customer confirmation | Worst status | Next decision · owner · date |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |

**The exception rule:** any account with zero `Verified` objectives inside 120 days of its opt-out
deadline is worked this week, whatever its health band says. Zero verified outcomes going into a
renewal is a value vacuum, and no health score compensates for it.

**The written skip:** any plan not worked this cycle is written down with a reason and a revisit
date (**R14**). An unwritten decision to skip is indistinguishable from an oversight and repeats
silently for four quarters.

---

## 11. Anti-patterns

| Anti-pattern | Correction |
| --- | --- |
| Statuses updated in a batch at quarter end | Within 5 business days of any evidence change |
| A review that presents slides about the plan | The plan is agenda item one and gets worked in the room |
| We read out the numbers | Their measurement owner confirms them; otherwise report the period as unmeasured |
| Green because nothing has obviously gone wrong | Green requires an indicator at threshold, variance inside 10pp, and no open blocker |
| A milestone re-dated a third time | Re-plan the objective; a third date is fiction |
| Carrying a dead objective as a permanent Watchpoint | Retire it, with a reason and a revisit date |
| Reporting `Delivered` as achievement | Only `Verified` counts, and only with a named person and a date |
| A slip communicated verbally on a call | In writing, with the new date and the cause |
| Interpolating an unmeasured period | `UNKNOWN — requires <source>`, and Watchpoint |
| A new sponsor inheriting the plan unchanged | Objectives drop to `Proposed` until they accept them in their own words |
| A review held because the calendar said so | No decision, no review. Send the update and give the hour back |
