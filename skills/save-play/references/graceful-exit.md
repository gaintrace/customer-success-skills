# The Stop-Loss and the Graceful Exit

> The least popular file in this library, and the one that protects the most revenue. A save
> pursued past the point of return consumes the hours that would have protected three healthy
> accounts, and it ends badly anyway (`R21`).
>
> This file covers three things: **when to stop**, computed rather than felt; **how to leave**, so
> the exit preserves the reference and the win-back; and **managed churn** — the notice, the
> export, the offboarding and the triggers that make a return possible.

**Contents**
- [Why the stop-loss is a discipline, not a mood](#why-the-stop-loss-is-a-discipline-not-a-mood)
- [The economics](#the-economics)
- [Stop-loss triggers](#stop-loss-triggers)
- [The stop-loss meeting](#the-stop-loss-meeting)
- [Restructure before exit](#restructure-before-exit)
- [The managed exit runbook](#the-managed-exit-runbook)
- [The exit interview](#the-exit-interview)
- [Data export and offboarding](#data-export-and-offboarding)
- [Win-back triggers](#win-back-triggers)
- [The win-back approach](#the-win-back-approach)
- [What to record](#what-to-record)
- [Anti-patterns](#anti-patterns)

---

## Why the stop-loss is a discipline, not a mood

Three failure modes cost more than the loss itself.

| Failure | What it looks like | What it costs |
| --- | --- | --- |
| **The zombie save** | A play nobody stopped and nobody is running. Status is "still working it" for four months | A CSM quarter, and a forecast that is wrong in a way nobody can see |
| **The fought exit** | Retention offers after notice, guilt, escalating to their boss, a surprise discount at the door | The reference, the win-back, and the way they describe you to peers who ask |
| **The silent fade** | The account leaves and no one recorded a decision, a cause, or a date | Nothing is learned; the same loss repeats next quarter with a different logo |

A managed exit preserves two assets a fought exit destroys: the **reference**, which the customer
gives on a call with a prospect who asks them directly, and the **win-back**, which is worth more
than it looks because the relationship survives the logo. Both are decided in the last three weeks.

## The economics

Run `../scripts/save_economics.py`. It computes each of these deterministically and prints the
arithmetic, which is the point — a stop-loss argued without numbers becomes an argument about who
cares most, and the person who cares most is usually the person closest to the account.

| Quantity | Formula |
| --- | --- |
| Opt-out deadline · runway | `renewal_date − notice_period_days`; runway is that minus today (`R1`) |
| Retained gross profit if saved | `ARR × gross_margin × horizon_years` |
| Fully-loaded play cost | `Σ (hours by role × loaded hourly cost)` across CS, exec, engineering, services |
| Concession cost | `ARR × discount_pct × horizon_years`, plus the cost of any credits or services given |
| **Break-even save probability `P*`** | `(play cost + concession cost) ÷ retained gross profit` |
| Discount ceiling | The discount at which retained gross profit no longer exceeds the play cost |
| Priority per hour | `expected retained gross profit ÷ planned hours` — how you rank two live plays |

**Reading `P*`.** It is the minimum chance of saving at which the play is worth running. If `P*` is
9%, almost any play is justified. If `P*` is 55% on a cause whose savability band is Low, you are
proposing to spend more than the outcome is worth, and the arithmetic says so before anyone has to.

`P*` is compared against the **savability band**, not against a number you invented for this
account (`R22`). Bands are ordinal planning conventions `[P]`. If your organisation has coded
twenty closed plays by root cause through `churn-postmortem`, replace the band with your own
observed rate and say which cohort it came from.

**Loaded cost, not salary.** Use fully-loaded hourly cost including benefits, tooling and overhead,
and count executive and engineering hours at their real rate. A play that looks cheap because only
CSM hours were counted is the most common way a stop-loss is avoided.

## Stop-loss triggers

Any single trigger ends the save and opens the exit. They are written into the record at
declaration, before anyone is emotionally invested.

| # | Trigger | Why it is terminal |
| --- | --- | --- |
| 1 | Break-even `P*` exceeds the play's savability band | Spending more than the outcome is worth |
| 2 | Two consecutive checkpoints with no working signal | The play is not landing; a third iteration will not differ |
| 3 | Locus is `customer-internal` or `market` and no restructure exists | Nothing we control changes the outcome |
| 4 | RC10 confirmed against the signed scope | Never savable; spending confirms a sales finding rather than changing it |
| 5 | The decision-maker declines every meeting format offered, twice | There is no forum in which a save can happen |
| 6 | Decision runway under 14 days with no engaged decision-maker | No time left to change a decision that has already been made |
| 7 | The required concession exceeds the computed discount ceiling | The retained revenue no longer covers the cost of serving it |
| 8 | A signed enterprise agreement or mandate names another vendor | The decision was taken above everyone in the conversation |
| 9 | Our own side will not resource the fix the diagnosis requires | The cause is real and we have declined to address it — say so plainly and exit |

Trigger 9 is the honest one and the one teams avoid writing down. If engineering will not resource
the fix, the account is not savable *by CS*, and pretending otherwise transfers an organisational
decision onto a CSM's personal credibility with the customer.

## The stop-loss meeting

Internal, 30 minutes, DRI plus manager plus the exec sponsor if one is engaged. Four questions,
answered with evidence rather than conviction:

1. **Which trigger fired, and what is the evidence?**
2. **What is `P*`, and where does the savability band sit?**
3. **Is there a restructure that changes the answer** — smaller, shorter, narrower, deferred?
4. **What do we lose by continuing** — which accounts are not being worked instead (`R14`)?

The outcome is one of three, recorded with a date: **continue** (with a revised plan and a new
trigger), **restructure**, or **exit**. "Keep an eye on it" is not an outcome.

**Marking will-churn** requires all four conditions in `war-room.md` §the-will-churn-transition:
options exhausted and shown, manager agreement, the renewal opportunity re-categorised with a
called value, and the loss coded to a root cause with the decision date (`R24`).

## Restructure before exit

Between "save as sold" and "exit" sits a third option that teams skip. Test it explicitly before
exiting, because a restructured account retains the data, the integration and the relationship —
all of which make a future expansion cheap and a competitor's entry expensive.

| Option | When it fits | Booked as |
| --- | --- | --- |
| Right-size the units | Utilisation well below entitlement (RC11, RC7) | Contraction, `value_delta_reason = seat_reduction` |
| Drop a tier | They use one of three product areas | Contraction, `product_removal` |
| Shorten the term | They cannot commit twelve months through uncertainty | Renewal at a shorter term |
| Defer or ramp | Budget returns next fiscal year (RC7) | Ramped renewal — flag it; ramps distort retention metrics |
| Narrow to one team | The value is real in one department and absent elsewhere | Contraction with a documented expansion trigger |
| Pause with data retention | A genuine, dated pause — not an indefinite one | A dated suspension with a restart date, or it is churn |

Every restructure records an **expansion trigger**: the observable event that would make growth
sensible again, and the date it is next checked. A contraction without a trigger is a churn with a
longer timeline.

## The managed exit runbook

Once the decision is made, the exit is a project with dates, not a wind-down.

| # | Step | Owner | By | Done when |
| --- | --- | --- | --- | --- |
| 0 | **Say it by voice first** (`C26`) — the DRI or VP CS phones on the computed Mon–Wed 08:00–11:30 recipient-local slot; the written confirmation follows within 2 hours and repeats only what was said | DRI / VP CS | +1d | `Call placed` recorded with date, time, caller and outcome |
| 1 | Confirm the decision, the effective date and the notice mechanics in writing | DRI | +2d | Customer confirms both dates |
| 2 | Tell the internal teams: support, billing, product, the account team | DRI | +2d | Suppression on, no renewal automation fires |
| 3 | Publish a dated offboarding plan to the customer | DRI | +5d | Plan acknowledged |
| 4 | Deliver the data export **before it is asked for** | Support / Solutions | +10d | Export delivered and verified by them |
| 5 | Documented decommissioning: integrations, SSO, webhooks, API keys | Solutions | +15d | Checklist complete, nothing left dangling |
| 6 | Run the exit interview | CS manager (not the DRI) | +14d | Notes recorded against the account |
| 7 | Final invoice reconciliation; credits or refunds resolved | Finance | +20d | Zero disputed balance |
| 8 | Close the commercial record: opportunity, cause code, decision date | DRI | +20d | `churn_event` complete |
| 9 | Set win-back triggers with review dates | DRI | +21d | Triggers on the account with owners |
| 10 | Send the closing note — no pitch, no guilt, a real door left open | DRI | +21d | Sent |

Every block in this runbook is written in the regulated register (`C27`): no exclamation marks, no
superlatives, no intensifiers, no sentence over 25 words, one apology at most. A departing customer
reads enthusiasm as relief that they are going.

**Never make a retention offer after notice has been served** unless the customer asks for options.
A discount produced at the door tells them the price was always negotiable and that it took a
cancellation to find out — the most expensive lesson you can teach a departing customer, because
they tell peers.

## The exit interview

Post-churn feedback is disproportionately honest, because the customer no longer has an interest in
managing the relationship. It is the highest-quality diagnostic input the whole system produces and
it is available for roughly thirty days.

| Rule | Why |
| --- | --- |
| Run it **within 30 days** of the decision | Memory and willingness both decay quickly |
| Conducted by someone **other than the account owner** | The account owner gets a polite version |
| Framed as improving the product, not reopening the deal | Any hint of a save closes the conversation |
| Recorded against a controlled vocabulary, not free text | Free-text reasons cannot be aggregated and therefore never get fixed |
| Ends with an explicit ask to stay in touch | The win-back is a relationship, not a campaign |

Six questions, in this order:

1. "When did you actually decide?" — sets `decision_date` (`R24`), usually far earlier than assumed.
2. "What was the moment you started looking?" — locates the origin stage.
3. "What did we know that we did not act on?" — the detection failure, in their words.
4. "What are you doing instead, and what does it cost you?" — separates RC7 from RC8 definitively.
5. "What would have had to be true for you to stay?" — the win-back trigger, stated by them.
6. "Who else should we have been talking to?" — the multithreading failure, named.

## Data export and offboarding

Offboarding quality is the single most-remembered part of a vendor relationship, and it is almost
free to do well.

| Element | Standard |
| --- | --- |
| **Export format** | Their choice from what exists — CSV, JSON, or a documented API pull. Documented, complete, with a schema |
| **Timing** | Delivered before they ask, and at least 30 days before access ends |
| **Completeness** | Everything they created, including attachments, comments, history and configuration |
| **Verification** | They confirm the export opens and is complete, in writing, before access ends |
| **Access window** | Read-only access after the effective date where the contract permits it — inexpensive, and remembered |
| **Deletion** | On request, with written confirmation and a date, per the DPA |
| **Decommissioning** | A checklist covering integrations, SSO, webhooks, API keys and scheduled jobs, so nothing fails noisily in their stack next month |

An export delivered late, incomplete, or only after three requests converts a neutral departure into
an active detractor — and the person who experienced it will be at a different company inside two
years, evaluating vendors.

## Win-back triggers

Set at exit, not remembered later. Each is an observable event with an owner and a review date.

| Cause | Trigger that makes returning rational | Typical review |
| --- | --- | --- |
| RC3 Product gap | The specific capability ships and is generally available | On the ship date |
| RC4 Reliability | The defect class is closed and the reliability metric is publishable | Quarterly |
| RC7 Budget | A funding event, a return to growth, or a new fiscal year | Quarterly |
| RC8 Competitive | The competitor's contract approaches its own renewal; or a public failure of theirs | At their renewal anniversary |
| RC9 M&A | The integration completes and the mandate lapses; or our champion resurfaces elsewhere | Every six months |
| RC10 Wrong-fit | We ship into their segment, or they change the use case | Annually |
| RC11 Pricing | Packaging changes; a tier now fits their shape | On any packaging change |
| Any | **The champion appears at a new company** — the relationship travels even when the logo does not | Monthly contact check |

The last row is the one most worth instrumenting. People move, and the person who fought for you
internally is a warm entry at their next employer regardless of how the account ended.

## The win-back approach

One note, at the trigger. Not a campaign, not a sequence, not a nurture track.

| Rule | Why |
| --- | --- |
| Name the failure plainly, do not relitigate it | "You left because of X. That was real." Anything else reads as revisionism |
| Lead with what changed, with a date | The only new information in the message |
| Offer value, not a meeting | A sandbox, a benchmark, a document — a meeting request asks them to spend before they receive |
| Commit to stopping | "If it is not relevant, I will not send another one of these." Then honour it |
| Send from the original relationship owner where possible | The relationship carries; the logo does not |

Cross-company win-back conversion benchmarks are not available from a source this library will
cite. Track your own rate by churn reason and use that — win-back after a budget loss behaves
nothing like win-back after a product gap, and a blended rate hides both.

## What to record

| Field | Value |
| --- | --- |
| `churn_event.decision_date` | When the customer decided (`R24`) |
| `churn_event.effective_date` | When service ends |
| `churn_event.type` | `full_churn` · `non_renewal` · `downgrade` · `partial_seat_reduction` · `involuntary` |
| `churn_event.arr_lost` | With the split between full loss and contraction |
| `primary_risk_reason` · `contributing_reasons` | RC1–RC11 |
| `locus` · `origin_stage` | Determines who owns the systemic fix |
| `was_savable` | `bad_fit_at_sale` · `exogenous` · `missed_signal` · `detected_not_actioned` · `actioned_insufficient` · `vendor_failure` — assigned by someone other than the account owner |
| `earliest_detectable_signal` + date | The forensic field; `churn-postmortem` computes realised lead time from it |
| `stop_loss_trigger` | Which trigger fired, with its evidence |
| `play_cost_actual` | Hours by role — this is what makes next quarter's capacity plan real |
| `win_back_triggers` | Each with an owner and a review date |

Hand the record to `churn-postmortem`, which owns the loss review, the five-whys on the
**vendor-side** failure chain, and the instrumentation backlog that improves the next diagnosis.

## Anti-patterns

| Anti-pattern | Correction |
| --- | --- |
| Continuing a play because stopping feels like giving up | The trigger fired; the arithmetic is the argument |
| A surprise discount after notice is served | Never, unless they ask for options. It teaches them the price was fiction |
| Guilt, pressure, or escalating over the buyer's head at the exit | The reference and the win-back are decided here |
| An export delivered late or incomplete | Before they ask, verified by them, with a schema |
| No exit interview | Thirty days of unusually honest feedback, thrown away |
| The account owner running the exit interview | They get the polite version. Use someone else |
| Free-text churn reasons | Controlled vocabulary, or nothing can be aggregated or fixed |
| Recording the effective date as the churn date | Record the decision date (`R24`) |
| Win-back as a nurture sequence | One note at a real trigger, offering value, with a promise to stop |
| No win-back triggers set | The relationship expires by default rather than by decision |
| Counting only CSM hours in the play cost | Executive and engineering hours are the expensive ones |
