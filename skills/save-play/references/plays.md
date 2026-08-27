# The Plays

> One play per root cause. The play is chosen by the diagnosis in
> `root-cause-taxonomy.md`, never by the risk score — two accounts at 78/100 with different causes
> need opposite interventions, and running the wrong one costs the account faster than doing
> nothing, because it burns the meetings you were going to get.
>
> Every play below carries the same eight parts, and a play missing any of them is not ready to
> run. Savability bands are ordinal planning conventions `[P]` (`R22`) — they rank where to spend
> hours, and they are never the probability of saving this account.

**Contents**
- [Play selection and capacity](#play-selection-and-capacity)
- [The anatomy of a play](#the-anatomy-of-a-play)
- [Value reconstruction (RC1)](#value-reconstruction-rc1)
- [Implementation restart (RC2)](#implementation-restart-rc2)
- [Scope the gap honestly (RC3)](#scope-the-gap-honestly-rc3)
- [Named-owner remediation (RC4)](#named-owner-remediation-rc4)
- [Re-multithread (RC5)](#re-multithread-rc5)
- [Successor transfer (RC6)](#successor-transfer-rc6)
- [Structure for survival (RC7)](#structure-for-survival-rc7)
- [Competitive re-bid (RC8)](#competitive-re-bid-rc8)
- [Sell the new decision-maker (RC9)](#sell-the-new-decision-maker-rc9)
- [Dignified exit (RC10)](#dignified-exit-rc10)
- [Restructure, do not discount (RC11)](#restructure-do-not-discount-rc11)
- [Diagnostic conversation (cause unknown)](#diagnostic-conversation-cause-unknown)
- [The concession ladder](#the-concession-ladder)
- [Procurement counters](#procurement-counters)
- [Measuring whether plays work](#measuring-whether-plays-work)

---

## Play selection and capacity

| Cause | Play | Owner | First move | Savability `[P]` |
| --- | --- | --- | --- | --- |
| RC1 Value not realised | Value reconstruction | CSM + VP CS | 7 days | Moderate |
| RC2 Adoption failure | Implementation restart | VP CS + Services | 14 days | High with runway |
| RC3 Product gap | Scope the gap honestly | CSM + Product lead | 7 days | Low without a date we own |
| RC4 Reliability and trust | Named-owner remediation | Support lead + Eng | 72 hours | Moderate–High |
| RC5 Relationship loss | Re-multithread | CSM + VP CS | 7 days | Moderate |
| RC6 Champion departure | Successor transfer | VP CS then CSM | 48 hours (`R3`) | Moderate |
| RC7 Budget and economic | Structure for survival | AM + Finance | 14 days | Low as sold, Moderate restructured |
| RC8 Competitive displacement | Competitive re-bid | VP CS + AE | Same week | Moderate before scoring |
| RC9 M&A / reorg | Sell the new decision-maker | CCO / VP CS | 14 days | Low |
| RC10 Wrong-fit, sold badly | Dignified exit | CS manager | 14 days | Structural — do not spend |
| RC11 Pricing | Restructure, do not discount | AM + deal desk | 14 days | High |
| Cause not established | Diagnostic conversation | CSM | 72 hours | — |

**Capacity is the constraint, not willingness.** Plan against usable hours, roughly 60% of a week
(`R13`). A CSM carrying a 40-account book sustains **two to three** active plays alongside cadence
work. If six accounts qualify this cycle, three are not getting a play — decide which three
deliberately and write it down with a revisit date (`R14`). An undeclared decision to skip an
account is indistinguishable from an oversight, and it repeats silently for four quarters.

| Play | Realistic CSM hours | Other functions |
| --- | --- | --- |
| Diagnostic conversation · Dignified exit | 2–4 · 4–8 | Support 2–4h for the export |
| Re-multithread · Successor transfer | 6–10 · 8–14 | VP CS 2–4h |
| Scope the gap honestly | 6–10 | Product 4–6h |
| Structure for survival · Restructure, do not discount | 8–12 | AM 6–10h, Finance or deal desk 2–4h |
| Named-owner remediation | 5–10 | Support 5–10h, Engineering 10–20h — engineering is the real constraint |
| Value reconstruction | 10–16 | Analytics/ops 4–8h; baseline reconstruction dominates |
| Sell the new decision-maker | 10–20 | Exec 6–10h |
| Competitive re-bid | 20–35 | AE 15–25h, exec 4–8h |
| Implementation restart | 25–40 | Services 40–80h — effectively a second onboarding |

Splitting ownership across roles is measurably expensive: TSIA's *State of Customer Growth and
Renewal 2025* reports sales account executives handling medium-complexity renewals cost roughly
3× more and land about 10% lower net renewal rates than dedicated renewal specialists `[M]`. One
DRI, whatever the play.

## The anatomy of a play

| Part | Rule |
| --- | --- |
| **Objective** | One sentence: `<named person>` will have `<observable commitment>` by `<date>`. If it cannot be written this way, the play has no target |
| **Sequence** | Every step carries action · owner · date · expected effect · success measure |
| **Can commit** | Dated, owned, internally agreed — nothing else (`R19`) |
| **Cannot commit** | Said plainly, in the first sentence, with the nearest alternative |
| **Customer obligation** | At least one, with a named person and a date. A play with none is a wish |
| **Working / failing signals** | Observable inside 14 days, so the first checkpoint has something to test |
| **Exit criteria** | Written at declaration, specific and observable, agreed by both sides to close |
| **Stop-loss** | The condition that ends the play, and the date it is tested (`R21`) |

---

## Value reconstruction (RC1)

**Objective:** the economic buyer agrees, in writing, on one number that describes what the last
term produced — or agrees that it is not there, which is equally useful and far more honest.

| # | Action | Owner | By | Expected effect | Success measure |
| --- | --- | --- | --- | --- | --- |
| 1 | Reconstruct the baseline from the original business case, discovery notes and the success plan | CSM | +5d | A number both sides recognise | A written baseline with its source and date |
| 2 | Measure the same metric today, the same way, segmented by the buying team | CSM + ops | +7d | The honest delta, not a flattering one | Current value with a provenance tag |
| 3 | Pre-brief the champion on the number **before** the meeting, including if it is bad | CSM | +8d | No surprises in the room; they can defend it internally | Champion confirms the number is fair |
| 4 | Working session with the economic buyer: the number, the reason, and what changes | CSM + VP CS | +14d | Moves from "did it work" to "what do we do" | Buyer states the gap in their own words |
| 5 | Re-baseline the success plan with two dated milestones the customer owns | CSM | +21d | The next term has a measurable target | Signed success plan with customer-owned tasks |

**Can commit:** the measurement, the reporting cadence, named enablement, a re-baselined plan.
**Cannot commit:** that the number will move by a specific amount — that depends on their adoption.
**Customer must:** name the metric owner on their side and attend the working session.
**Working (≤14d):** the buyer attends; they correct your number rather than dismissing it; a second
stakeholder joins. **Failing:** the meeting is delegated twice; they decline to name a metric.
**Exit:** a re-baselined plan with two dated customer-owned milestones. **Stop-loss:** no baseline can
be reconstructed and the buyer will not agree a forward metric — that is a qualification finding.

## Implementation restart (RC2)

**Objective:** the contracted use case running in production with named users, on a plan the
customer co-signed, before the opt-out deadline minus 30 days.

| # | Action | Owner | By | Expected effect | Success measure |
| --- | --- | --- | --- | --- | --- |
| 1 | Root-cause the stall: blocked by us, by them, or by a missing decision | CSM + Services | +5d | Stops the restart repeating the original failure | Blocker named with an owner |
| 2 | Re-scope to the **smallest** valuable use case, not the original scope | Services lead | +10d | Something ships inside the runway | One use case, one team, one metric |
| 3 | Named customer project owner with allocated time, agreed by their manager | CSM | +10d | Removes the top cause of onboarding slip | Name and hours on record |
| 4 | Re-baselined plan: kickoff → configure → validate → train → production, each dated | Services | +14d | A schedule that fits inside the runway | Plan accepted in writing |
| 5 | Weekly 30-minute working session until first value event | CSM | ongoing | Momentum survives holidays and interrupts | Attendance ≥80% |
| 6 | Customer-verified first value milestone logged | CSM | by T-30 | The renewal has something to point at | The customer confirms it, in writing |

Anchor the milestone on **customer-verified value**, not vendor task completion — Lincoln Murphy's
formulation, Desired Outcome = the required result plus an appropriate experience `[P]`, is the
test: "training complete" is not value, "their team closed the month using it" is.

**Can commit:** services hours, a named implementation owner, a dated plan.
**Cannot commit:** their internal resourcing, or a go-live date that depends on their decisions.
**Customer must:** name a project owner with allocated hours and attend weekly.
**Working (≤14d):** the customer owner is named and attends; configuration progresses; a blocker they
own is cleared. **Failing:** two sessions missed; no owner named after 14 days.
**Exit:** first customer-verified value event. **Stop-loss:** runway under 45 days with no named
customer owner — there is no time left to implement before the decision.

## Scope the gap honestly (RC3)

**Objective:** the customer has, in writing, either a dated commitment we own, a documented
workaround they accept, or a clear no with the nearest alternative — inside 14 days.

| # | Action | Owner | By | Expected effect | Success measure |
| --- | --- | --- | --- | --- | --- |
| 1 | Write the requirement in one paragraph the customer would sign | CSM | +2d | Stops the gap drifting in scope | Customer confirms the wording |
| 2 | Solutions review: is there a configuration or integration path? | Solutions | +5d | Half of "gaps" are unbuilt workarounds | Written yes/no with the effort |
| 3 | Product decision with a **named owner**, ARR attached, and a date or an explicit no | Product lead | +10d | An answer we can stand behind (`R19`) | Committed / Intent / Declined, on record |
| 4 | Deliver the answer plainly, in the first sentence of the meeting | CSM | +14d | Trust survives a no; it does not survive a soft yes | They can repeat the answer accurately |
| 5 | If declined: price or scope the contract to reflect what they actually get | AM | +21d | A fair deal beats a fictional roadmap | Revised structure proposed |

**Can commit:** an internally-agreed dated deliverable, or a workaround with support behind it.
**Cannot commit:** anything on a roadmap without a named owner and an agreed date. A clear no
preserves more trust than a soft yes that turns out to be false (`R19`).
**Customer must:** confirm the requirement wording and say whether the workaround is acceptable.
**Working (≤14d):** they accept the workaround, or accept the no and continue the conversation.
**Failing:** they escalate the same requirement to procurement; a competitor appears.
**Exit:** written acceptance of the commitment, the workaround, or the no. **Stop-loss:** product
declines and the requirement is blocking — managed exit, preserving win-back for when the gap closes.

## Named-owner remediation (RC4)

**Objective:** a named engineer owns the root cause, the customer has a written RCA, and the defect
trend is one they can verify themselves — inside 30 days.

| # | Action | Owner | By | Expected effect | Success measure |
| --- | --- | --- | --- | --- | --- |
| 1 | Cluster the tickets and name the single root cause behind them | Support lead | +2d | Names a pattern support cannot see ticket-by-ticket | Cluster written with ticket IDs |
| 2 | Assign a named engineer and a target date; tell the customer both | Eng manager | +3d | Converts a queue into a person | Name and date communicated |
| 3 | Interim workaround, plus briefing support so the team stops re-explaining | Support lead | +5d | Reduces the daily cost of the defect | Workaround in place |
| 4 | Written RCA: timeline, root cause, blast radius **for this customer**, remediation with dates | Eng lead | +10d | Trust is rebuilt by specificity, not apology | RCA delivered in writing |
| 5 | Standing update every Tuesday until closed, whether or not there is news | CSM | weekly | Silence during an incident does more damage than the incident | Every update sent on time |
| 6 | Prevention: what changes so it does not recur | Eng lead | +30d | Ends the pattern, not just the ticket | Named change with an owner |

Read the ticket history cumulatively per account rather than per ticket — escalation risk is a
property of accumulated history [University of Victoria / IBM · arXiv:1901.01344 · 2019] `[A]`.

**Can commit:** the named owner, the update cadence, the RCA, the workaround.
**Cannot commit:** a fix date the engineering owner has not agreed.
**Customer must:** nominate one technical contact to receive updates.
**Working (≤14d):** ticket volume for the cluster falls; the customer stops copying executives; they
accept the workaround. **Failing:** a new ticket in the same cluster after the fix; the RCA is
challenged on facts. **Exit:** defect trend confirmed by their technical lead, both sides agreeing in
writing. **Stop-loss:** engineering will not resource the fix — that converts RC4 into RC3.

## Re-multithread (RC5)

**Objective:** three engaged contacts including one above the buyer, each with a two-way
interaction in the last 30 days, before the opt-out deadline minus 30 days.

| # | Action | Owner | By | Expected effect | Success measure |
| --- | --- | --- | --- | --- | --- |
| 1 | Map the current graph: who is engaged, who has gone quiet, who we have never met | CSM | +3d | Reveals the real depth, which is usually worse than assumed | Contact map with dates |
| 2 | Ask the remaining contact for one introduction, framed as helping them | CSM | +7d | An introduction beats a cold approach every time | Introduction made |
| 3 | Exec-to-exec note from our VP to their functional lead, offering something, asking nothing | VP CS | +10d | Positional weight without a demand | Reply or meeting accepted |
| 4 | Deliver a per-team artifact each new contact actually wants | CSM | +21d | Gives each contact their own reason to engage | Artifact opened / discussed |
| 5 | Book a recurring session with the widest group that will attend | CSM | +30d | Converts a person-dependency into a habit | Recurring invite accepted |

**Can commit:** the cadence, the artifacts, executive availability. **Cannot commit:** that their
organisation will make people available. **Customer must:** make one introduction.
**Working (≤14d):** one new two-way contact; an exec replies. **Failing:** the single contact declines
to introduce anyone, twice — a signal about the relationship, not about calendars.
**Exit:** three engaged contacts with persona coverage (`R5`). **Stop-loss:** depth still 1 at the
opt-out deadline minus 30 days; forecast accordingly and prepare the exit.

## Successor transfer (RC6)

**Objective:** a named successor who can state the business objective in their own words, plus a
second engaged contact, within 30 days. First outreach inside **48 hours** (`R3`).

| # | Action | Owner | By | Expected effect | Success measure |
| --- | --- | --- | --- | --- | --- |
| 1 | Confirm the departure: bounce body, domain migration, directory, admin logs, public profile | CSM | +24h | Avoids escalating on a mailbox quota error | Confirmed or disconfirmed with evidence |
| 2 | Identify the successor from admin logs, ticket ownership and org data | CSM | +48h | A person to address, not a title | Named individual |
| 3 | Exec-to-exec note from VP CS or above — offering context, not asking who replaced them | VP CS | +48h | Positional weight; hands the agenda to them | Reply or meeting |
| 4 | CSM note 2–4 days later: the three things in flight and the two decisions they now own | CSM | +5d | Makes the first contact useful rather than social | Decisions acknowledged |
| 5 | Rebuild the business case from zero inherited context and zero inherited goodwill | CSM | +21d | The successor owns the value, not the predecessor | They restate the objective |
| 6 | Open a risk record that persists to the renewal regardless of how the first meeting goes | CSM | +7d | Stops a good first meeting closing the risk early | Risk record open with a dated plan |

**Can commit:** a re-onboarding session, a written handover pack, executive time. **Cannot commit:**
anything the departed champion promised that was never internally agreed — check the commitment ledger
before the first call. **Customer must:** confirm who now owns the relationship.
**Working (≤14d):** a successor is named and accepts a meeting; they can describe the problem the
product was bought for. **Failing:** no successor after 30 days; the successor delegates to a junior;
the first meeting is cancelled twice. **Exit:** successor engaged, objective restated by them, second
contact active. **Stop-loss:** no named successor 45 days before the opt-out deadline.

## Structure for survival (RC7)

**Objective:** a smaller, affordable contract that keeps the relationship, the data and the
integration — proposed before the opt-out deadline minus 30 days.

| # | Action | Owner | By | Expected effect | Success measure |
| --- | --- | --- | --- | --- | --- |
| 1 | Establish the real constraint: a number, a headcount, or a policy | AM | +5d | Sizes the restructure to something they can approve | The constraint quantified |
| 2 | Model two or three structures inside it: fewer seats, lower tier, shorter term, deferred ramp | AM + Finance | +10d | Options beat a single take-it-or-leave-it | Three options with prices |
| 3 | Confirm which capability they must keep, and price around that | CSM | +10d | Protects the use case that regrows later | Named must-keep capability |
| 4 | Propose, with the trade named for each option (`R21` ladder below) | AM | +14d | Every give buys something | Option chosen |
| 5 | Set a documented expansion trigger for when their constraint lifts | CSM | +21d | Turns a contraction into a tracked recovery | Trigger with a review date |

Contraction is not failure here — it is the correct outcome, and it must be booked and coded as
contraction with `value_delta_reason` rather than reported as a flat renewal.

**Can commit:** structure, term, payment timing, scope. **Cannot commit:** a discount without an
approved get. **Customer must:** confirm the budget number and the approver.
**Working (≤14d):** they engage with the options rather than repeating the constraint. **Failing:**
"send your best price" with no engagement on structure — that is usually RC8.
**Exit:** a signed smaller contract with an expansion trigger recorded. **Stop-loss:** the affordable
structure is below the floor at which the account is worth serving — run `save_economics.py`.

## Competitive re-bid (RC8)

**Objective:** a seat in their evaluation with a defined process and timeline, agreed inside a week.

| # | Action | Owner | By | Expected effect | Success measure |
| --- | --- | --- | --- | --- | --- |
| 1 | Escalate to commercial leadership and the exec sponsor; treat it as a re-bid, not a save | VP CS | +2d | The right people are in from the start | Exec engaged |
| 2 | Ask directly and without defensiveness whether a review is running | VP CS | +3d | A customer preparing to leave respects being asked | They confirm the process |
| 3 | Establish stage: awareness, active evaluation, or decided | CSM | +5d | Decided evaluations need a different play | Stage on record |
| 4 | Build the switching-cost case: integration depth, data gravity, retraining, migration effort | CSM + Solutions | +10d | Competes on what price cannot replace | Written comparison |
| 5 | Deliver the differentiated case to the actual evaluator, not only the champion | AE + VP CS | +14d | Reaches the person scoring the decision | Meeting with the evaluator |
| 6 | Commercial response **last**, and only against a named get | AM | +21d | Price defends a position; it does not create one | Concession traded, not given |

**Can commit:** a migration or retraining plan, executive sponsorship, dated capability commitments
product has agreed. **Cannot commit:** matching a competitor's roadmap.
**Customer must:** state the evaluation criteria and the timeline.
**Working (≤14d):** they confirm the process and include us; the evaluator takes a meeting.
**Failing:** evasion, delegation to procurement only, refusal to schedule.
**Exit:** we are in the evaluation with criteria and a date, or we have lost and know why.
**Stop-loss:** the decision has been socialised and no criteria are shared — compete only if the ARR
justifies the hours, otherwise exit preserving win-back.

## Sell the new decision-maker (RC9)

**Objective:** a meeting with the incoming or acquiring executive, on their agenda, within 30 days.

| # | Action | Owner | By | Expected effect | Success measure |
| --- | --- | --- | --- | --- | --- |
| 1 | Map the new structure: who decides, who is displaced, what the mandate says | CSM | +5d | Stops effort landing on people without authority | Decision map |
| 2 | Establish whether the acquirer already runs a competing tool | AE | +5d | Determines whether this is a fight or a wind-down | Answer on record |
| 3 | Exec-to-exec introduction from CCO or VP CS, framed around their integration priorities | CCO | +10d | Speaks to their agenda, not our renewal | Meeting accepted |
| 4 | Quantify the cost of removing us: migration, retraining, integration rebuild, data | Solutions | +14d | Consolidation decisions are made on switching cost | Written estimate |
| 5 | Offer to be the consolidation *winner*, with a combined-entity proposal | AE + VP CS | +30d | Changes the question from whether to keep us to what we could replace | Proposal delivered |

**Can commit:** a combined-entity commercial structure, migration support, executive sponsorship.
**Cannot commit:** anything that pre-empts their integration decisions. **Customer must:** identify
the decision owner in the new structure.
**Working (≤14d):** the incoming exec takes a meeting; we are named in the rationalisation review.
**Failing:** the mandate names another vendor; our contact is displaced and cannot introduce us.
**Exit:** included in the consolidation decision with criteria and a date. **Stop-loss:** a signed
enterprise agreement elsewhere — managed exit, win-back triggers set on the integration timeline.

## Dignified exit (RC10)

**Objective:** a clean exit at minimum cost that preserves the reference and the win-back, and
delivers the qualification finding to sales leadership with the ARR attached.

| # | Action | Owner | By | Expected effect | Success measure |
| --- | --- | --- | --- | --- | --- |
| 1 | Confirm against the signed scope that the requirement was never in it | CS manager | +3d | Prevents spending a save budget on an unsavable account | Scope comparison on record |
| 2 | Tell the customer plainly what we can and cannot do for their use case | CSM | +7d | Honesty here is the whole basis of the win-back | They accept the position |
| 3 | Offer a clean, dated offboarding and a full data export | CSM | +10d | Leaving well is the last thing they remember | Offboarding plan sent |
| 4 | Exit interview while they will still speak to you | CS manager | +14d | Post-churn feedback is the most honest input the system gets | Interview completed |
| 5 | Route the qualification finding to sales leadership with the ARR | CS manager | +21d | Stops the same deal being sold next quarter | Finding filed with an owner |

**Can commit:** the export, the offboarding timeline, a pointer to a better-fitting alternative.
**Cannot commit:** a roadmap that would have made them a fit. **Customer must:** confirm the export
format and the effective date. **Exit:** offboarding completed, exit interview done, finding filed.
**Stop-loss:** not applicable — this play *is* the stop-loss.

## Restructure, do not discount (RC11)

**Objective:** an agreed structure that changes what they buy, not only what they pay, signed
before the opt-out deadline.

| # | Action | Owner | By | Expected effect | Success measure |
| --- | --- | --- | --- | --- | --- |
| 1 | Establish the actual objection: unit price, total, uplift, packaging, or an expiring discount | AM | +3d | Four different problems with four different fixes | Objection quantified |
| 2 | Compute the effective unit price now versus at signature, and the utilisation behind it | CSM | +5d | Often the price did not move — the denominator did | Arithmetic on one page |
| 3 | Build the value-density case: outcome per unit, in their metric | CSM | +10d | Reframes price as a ratio, not a number | Written case |
| 4 | Propose a structure: right-sized units, a different tier, a term change, a ramp | AM + deal desk | +14d | Fixes the packaging, not just the number | Structure proposed |
| 5 | Trade any concession against a named get from the ladder below | AM | +21d | Preserves the price integrity you need next renewal | Concession paired with a get |

**Can commit:** structure, term, payment timing, entitlement true-up. **Cannot commit:** a discount
outside the approved band. **Customer must:** name the approver and the signature date.
**Working (≤14d):** they engage with structure rather than repeating a number. **Failing:** "best and
final" with no reciprocal movement — check for RC8. **Exit:** signed at an agreed structure.
**Stop-loss:** the required discount exceeds the ceiling from `save_economics.py`.

## Diagnostic conversation (cause unknown)

**Objective:** the cause, on the record, from the customer, within 72 hours.

Run the six-step de-escalation sequence in `root-cause-taxonomy.md` §the-diagnostic-conversation. Arrive
with one artifact and no ask. Do not bring a value deck, a discount or an executive: any commercial
content converts the conversation into a negotiation before you know what you are negotiating about.

**Exit:** a primary cause coded with evidence, and the matching play opened.
**Stop-loss:** two declined meetings — treat unresponsiveness itself as evidence and escalate to
exec-to-exec contact.

---

## The concession ladder

**Trade, never give.** A concession offered without a named get is a discount, and it teaches the
customer that the price was never real — which you pay for at every future renewal. Approval bands
follow common deal-desk convention `[P]`; substitute your own where they differ.

| Rung | The give | The required get | Approval |
| --- | --- | --- | --- |
| 1 | Payment terms (Net 30 → Net 45/60) | Signature by a named date | CSM / RM |
| 2 | Waive or reduce the contracted uplift | Multi-year term, or a price lock in our favour | RM |
| 3 | Enablement, training or services credits; premium support trial | Exec sponsor meeting plus a written success plan | Manager |
| 4 | 0–5% discount | Named signature date plus reference rights | RM |
| 5 | 5–10% discount | Multi-year commitment, or expanded scope/seats | Manager |
| 6 | 10–15% discount | Multi-year plus prepayment | Manager / Director |
| 7 | 15–25% discount | Multi-year, prepay, expanded scope, logo and case-study rights | VP |
| 8 | Above 25%, or any unprecedented term (MFN, unlimited liability, termination for convenience, source-code escrow) | Board-visible logo, strategic justification, or a documented displacement threat | C-level / deal desk exception |

**Exhaust the non-price levers first.** Each has real value to the customer and costs less than
margin: term length · payment timing · SLA tier · named support contacts · scope and entitlement
true-up · roadmap influence or an advisory-board seat · early-access programme · training credits ·
migration and services credits · reference rights · case study · co-marketing · a speaking slot.

**Never trade away without VP approval:** the **notice window**, the **auto-renew clause**, the
**uplift clause**, and **audit/true-up rights**. Those four terms determine your negotiating
position at the next renewal — 87% of cloud service agreements auto-renew and about 70% carry a
30-day notice window [Common Paper · 2026 SaaS Contract Benchmark Report · 16,140 agreements from 2,223
companies, Jun 2025–Jun 2026] `[M]`, so surrendering them converts a renewable contract into an
annual re-sale.

**A multi-year with annual opt-outs is not a multi-year** for forecasting purposes. Price it as
what it is, and do not book the term as committed.

## Procurement counters

| They say | What it is | The response |
| --- | --- | --- |
| "We have quotes 30% lower" | Standard anchor | Ask for a scope-normalised comparison. Reframe on total cost including migration, retraining and integration rebuild |
| "Send your best and final" at T-14 | Deadline squeeze | Best-and-final is conditional on a named signature date and a get from the ladder |
| "This offer expires Friday" | Artificial urgency | Do not use it and do not respond to it. Anchor on the notice deadline, which is a real date |
| "Lesser of CPI or 3%, capped" | Uplift cap | Have a pre-approved position; trade the cap for term length |
| "We need termination for convenience" | Risk transfer | Rung 8. Trade only against prepayment or a materially longer term |
| Procurement arrives inside T-30 | Late, deliberately or otherwise | Expect slippage. Propose a 30–60 day extension at current terms to remove the artificial deadline |

The renewal manager, not the CSM, owns the procurement conversation. A CSM who negotiates price
loses the ability to be the customer's advocate at the next renewal.

## Measuring whether plays work

| Metric | Definition | Reporting rule |
| --- | --- | --- |
| **Save rate by cause** | ARR retained from plays opened on cause X ÷ ARR that entered a play on cause X and reached its decision date | Requires written open and exit criteria, dated and auditable. A save rate computed on an undisciplined risk list is meaningless — teams flag everything and inflate the numerator |
| **Risk detection rate** | Share of losses that were in an open play at least 60 days before the decision date | Report next to the save rate, always. A high save rate on a short list is a detection failure |
| **Median days from open to first customer meeting** | Per cause | The clearest signal of whether plays are actually running |
| **Stop-loss rate** | Plays exited deliberately ÷ plays closed | A rate near zero means nobody is stopping; a rate above roughly half means plays are opening on unsavable accounts |
| **Concession efficiency** | Share of granted concessions with a documented get | Below 100% is a training problem, not a pricing one |
| **Play cost variance** | Actual hours ÷ planned hours | Feeds the capacity table above; without it, next quarter's plan is fiction |

Segment every one of these by root cause. A blended save rate hides the only actionable fact in
the data — which causes you can actually beat, and which you should stop spending on.
