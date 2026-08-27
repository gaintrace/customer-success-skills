# The Forecast Call — inspection, bias, and the post-mortem

> Read this when running or preparing the weekly forecast call, when a number needs challenging,
> or when scoring a closed period.
>
> The call is not a status meeting. It is an **inspection**: a small number of renewals get their
> evidence examined out loud, and the roll-up changes as a result. A call where the number never
> moves is a call that is not working.

**Contents**
- [1. What the call is for](#1-what-the-call-is-for)
- [2. Cadence, roles and inputs](#2-cadence-roles-and-inputs)
- [3. The pre-read contract](#3-the-pre-read-contract)
- [4. The deal-inspection script](#4-the-deal-inspection-script)
- [5. What earns inspection](#5-what-earns-inspection)
- [6. The manager's job in the room](#6-the-managers-job-in-the-room)
- [7. Running it async](#7-running-it-async)
- [8. Sandbagging — tells and challenge questions](#8-sandbagging--tells-and-challenge-questions)
- [9. Happy ears — tells and challenge questions](#9-happy-ears--tells-and-challenge-questions)
- [10. The full call agenda](#10-the-full-call-agenda)
- [11. The post-mortem and variance decomposition](#11-the-post-mortem-and-variance-decomposition)

---

## 1. What the call is for

Three outputs, in priority order:

1. **A submitted number**, with the accounts that explain the change since last week.
2. **A shorter list of dated actions** on the renewals that moved or should have.
3. **Calibration of the team** — everyone leaves with the same understanding of what Commit means.

Everything else — pipeline chat, product complaints, general account colour — belongs somewhere
else. The test of the call is whether a category or a value changed in it. If nothing changed for
three weeks running, the categories are being set to survive the meeting rather than to predict.

## 2. Cadence, roles and inputs

| | |
| --- | --- |
| **Cadence** | Weekly, same slot, 30 minutes for a book, 45 for a segment roll-up |
| **Attendees** | Forecast owner (chairs) · renewal owners · CS ops (data) · deal desk (paper) · optionally the exec sponsor of any At Risk account |
| **Input** | The pre-read, published ≥12 hours before. No pre-read, no call |
| **Snapshot** | Frozen before the call, named by vintage. The call edits the *live* forecast, never the frozen one |
| **Output** | The submitted number, the movement table, and dated actions with owners |

**The one non-negotiable:** the snapshot used for grading is frozen and never edited afterwards. A
forecast edited all quarter and graded at the end measures the team's ability to update fields, not
to predict.

## 3. The pre-read contract

The pre-read is produced by `../scripts/forecast.py` plus the artifact in
`../assets/weekly-forecast-pack.md`. It answers four questions before anyone speaks:

| Question | Where it is answered |
| --- | --- |
| What is the number, and what is the band? | Roll-up header |
| What moved since last week, and why? | Movement table — with the observable fact, not the interpretation |
| What is exposed, and who owns the save? | At-risk register |
| What paper is late? | Paper and notice exceptions — order forms unissued inside T-45, opt-out deadlines passed unconfirmed, null notice periods |

Anyone who has not read it participates by listening. Reading the pre-read aloud is the most common
way a 30-minute call becomes 75 minutes and changes nothing.

## 4. The deal-inspection script

Six questions, in order, for any renewal under inspection. They are deliberately about artifacts.

1. **Who is the economic buyer, when did you last speak to them, and what did they say?**
   *(Not the champion. Not "the team". A person, a date, and a sentence they said.)*
2. **What is the paper status right now?** Issued, with the customer, in procurement, signed.
3. **What is the one thing that has to happen next, who owns it, and by when?**
4. **What is the value call, and why does it differ from ATR?** A value equal to ATR by default is
   not a call — it is a blank field.
5. **What would have to be true for this to close lost or downsell?** If the owner cannot answer,
   they have not tested it.
6. **What changed since last week, and what is your confidence now?**

If four of six answers are "I'll check", the row is demoted for the week. That is not a punishment;
it is what the category means.

## 5. What earns inspection

You cannot inspect 60 renewals in 30 minutes and should not try. Inspect by exposure, not by turn.

| Rule | Selection |
| --- | --- |
| Top exposure | Every renewal where `ATR × (1 − base rate for its category)` is in the top 5 |
| Movement | Every row that changed category or moved called value by more than the materiality line |
| Gate failure | Every Commit failing any of the six criteria |
| Clock | Every row inside T-45 without an issued order form, and every row past its opt-out deadline unconfirmed |
| Silence | Every row that has not moved in 3 weeks and is not Closed/Won — stasis is a signal |

Everything else is accepted as called and reviewed in the monthly deep-dive.

## 6. The manager's job in the room

| Do | Do not |
| --- | --- |
| Ask for the artifact, every time | Accept a summary of the artifact |
| Countersign Commit personally | Let Commit be a private call |
| Demote on the mechanical trigger, without debate | Negotiate the demotion with the owner |
| Praise an early demotion loudly | Punish the person who brought the bad news — it is the fastest way to build a book of happy ears |
| Name the three swing accounts before submitting | Submit a range with no named drivers |
| Track your own bias across quarters | Assume the bias belongs to the reps |

A manager who never demotes in the call is not inspecting. A manager whose demotions all land in
week 12 was inspecting too late.

## 7. Running it async

For distributed teams, the call can run as a written thread with one rule: **every inspected row
gets a written answer to the six questions in §4, posted before the deadline, and the manager posts
the demotions publicly.** Async loses the calibration benefit — people learn what Commit means by
hearing someone else's Commit taken apart — so run at least one live call a month.

## 8. Sandbagging — tells and challenge questions

Sandbagging is under-calling to be beaten later. It costs money in two ways: capacity is allocated
to the wrong accounts, and finance plans against a number that was never the real one.

| Tell | Measure | Threshold | Challenge question for the call |
| --- | --- | --- | --- |
| Best Case that always converts | Best Case ARR closed won ÷ Best Case ARR called | > 70% | "Best Case converted at 78% over four quarters. What is different about *this* account that keeps it out of Commit?" |
| Closing from Omitted or At Risk | ARR closed won from Omitted or At Risk ÷ total closed won | > 3% | "This closed from At Risk with no save plan on file. When did you know it was going to close?" |
| Value called below quote with no reason | Rows where called < quoted with `value_delta_reason` null | Any | "The quote is $240k and you called $200k. Which line item are you assuming they cut?" |
| Late promotion | Median days before renewal at which rows enter Commit | Inside T-20 | "Six of your Commits entered in the last three weeks. What did you learn in week 10 that you did not know in week 4?" |
| Persistent negative bias | `Σ(F − A) / Σ A` across 3 periods | < −2% | "You have come in over the number three quarters running. Where is the cushion this quarter?" |

The hardest sandbag to detect is the **correct-in-aggregate** book: a rep who under-calls three
accounts and over-calls one lands the roll-up and hides both errors. WAPE, not accuracy, is what
finds them.

## 9. Happy ears — tells and challenge questions

Happy ears is over-calling from optimism, and it is more expensive: the save window closes while the
account is still carried in Commit.

| Tell | Measure | Threshold | Challenge question for the call |
| --- | --- | --- | --- |
| Commit leakage | Commit ARR that closed lost or downsold ÷ Commit ARR called | > 5% | "Commit leaked 9% last quarter. Which of the six criteria was missing on the ones that leaked?" |
| No value calls at all | Share of the book where called value exactly equals ATR | 100% is unachievable in an enterprise book | "Every row in your book renews at exactly ATR. Which one is genuinely at risk of a seat cut, and what is the number?" |
| Commit without paper inside T-45 | Count | Any | "No order form, 31 days to the opt-out date, and procurement has not seen it. What makes this Commit?" |
| Held above At Risk past the opt-out deadline | Count | Any | "The notice window closed nine days ago and nothing came in writing. What are we actually forecasting?" |
| Stale buyer contact | Days since economic-buyer contact on Commit rows | > 30 | "The last contact with the budget owner was 41 days ago. Who has told you the budget survived planning?" |
| Date slipping repeatedly | Renewal date pushed ≥2 times | Any | "The date has moved twice. A date that moves is usually a decision that has not been made — what is the real one?" |
| Persistent positive bias | `Σ(F − A) / Σ A` across 3 periods | > +2% | "Three quarters over-called. This is a coaching problem, not a model problem — walk me through your Commit definition" |

**A sustained \|bias\| above 2% across three periods is a coaching problem, not a model problem.**
Recalibrating a model against a biased human input just encodes the bias.

## 10. The full call agenda

**30 minutes, for a single book. Timings are the point — this agenda fails when it runs long.**

| Min | Segment | What happens | Exit criterion |
| --- | --- | --- | --- |
| 0–2 | **The number** | Base case, band, change since last week, and the two accounts that explain the change | Everyone has heard the number |
| 2–5 | **Paper exceptions** | Order forms unissued inside T-45 · opt-outs passed unconfirmed · null notice periods | Every exception has an owner and a date |
| 5–8 | **Movement** | Every row that changed category or value: the observable fact, who called it, the artifact | No unexplained movement remains |
| 8–20 | **Inspection** | The §5 selection, run through the §4 script. Demote mechanically | The submitted number reflects what survived |
| 20–26 | **At-risk register** | Each At Risk row: cause code, exposure, save owner, dated plan, exec sponsor. At-risk coverage % stated | Every dollar of exposure has a dated plan or is called at zero |
| 26–29 | **Bias scan** | The measured tells from §8 and §9, with one challenge question asked out loud | The team hears its own numbers |
| 29–30 | **Submit** | The number, the band, the three swing accounts, and the actions | Number submitted with named drivers |

**Materiality line.** Set it once and hold it: the smallest ATR that can change the roll-up
conclusion. A common construction is the ATR of the account at the 80th percentile of cumulative
ATR — inspect above it, batch below it.

## 11. The post-mortem and variance decomposition

Run this within two weeks of the close, against the **frozen** snapshot, by vintage, by segment and
by owner. Roll-up accuracy is often right for the wrong reasons, because offsetting errors hide
account-level chaos — which is why WAPE sits beside it.

### The scorecard

| Metric | Formula | Reads |
| --- | --- | --- |
| Forecast accuracy | `1 − \|F − A\| / F` | Headline. Publish beside the new-business variance |
| WAPE | `Σ\|Fᵢ − Aᵢ\| / Σ Aᵢ` | Real dispersion; immune to offsetting errors |
| Bias | `Σ(Fᵢ − Aᵢ) / Σ Aᵢ`, signed | Direction — optimism or sandbagging |
| Commit hit rate / leakage | Closed won from Commit ÷ Commit ARR, and its inverse | Whether the category means one thing |
| Save rate | At-Risk ARR retained ÷ At-Risk ARR identified | Segment by cause code, or it teaches nothing |
| Vintage drift | Accuracy at T-90 vs T-60 vs T-30 | T-30 accuracy is near bookkeeping; the T-90 movement is the real score |

Grade each vintage separately. **How far the T-90 call moved** is the number that says whether the
team can predict; T-30 accuracy mostly says whether they can update fields.

### Decomposing the variance

Every dollar of miss belongs to exactly one of three classes. Different classes have different
owners and completely different fixes, which is why "we were 6% off" is not an actionable finding.

| Class | Definition | Typical cause | Owner of the fix |
| --- | --- | --- | --- |
| **Category error** | Closed in a different outcome class than called — a Commit that lost, an At Risk that closed won | Entry criteria not enforced; risk detected too late | Forecast owner (inspection discipline) |
| **Value error** | Right outcome class, wrong value — almost always an unforecast downsell | Value defaulted to ATR; consumption not tracked; expiring discount ignored | Renewal owner (value-call discipline) |
| **Timing error** | Slipped into or out of the period | Forecasting on the renewal date rather than the opt-out deadline; procurement lead time under-modelled | Ops / deal desk (date hygiene) |

**Method.**

1. Join the frozen snapshot to actuals on `account_id` + renewal event.
2. For each row: `variance = actual − forecast`.
3. Classify: outcome class differs → **category**. Same class, different value → **value**. Not in
   the period at all (either direction) → **timing**.
4. Sum the absolute variance per class, and express each as a share of total absolute variance.
5. Name the top three contributing accounts in each class.

**Worked example.**

| Class | $ variance | % of total | Top contributors | Fix committed |
| --- | --- | --- | --- | --- |
| Category error | −$540,000 | 61% | Pemberton (Commit → lost) | Commit countersignature; economic-buyer age check on every call |
| Value error | −$212,000 | 24% | Halcyon (−$60k seats), Cobalt (−$152k consumption) | Consumption run-rate rule at T-90; `value_delta_reason` mandatory |
| Timing error | −$132,000 | 15% | Vireo (slipped one quarter) | Forecast on opt-out deadline; procurement lead time added to the milestone plan |
| **Total** | **−$884,000** | **100%** | | |

One process change per class, with an owner and a date, carried into the next quarter's call. A
post-mortem that produces no process change was a reporting exercise.
