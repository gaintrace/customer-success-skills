# The Sales-to-CS Handover

> The handover is the highest-leverage twenty minutes in the customer lifecycle and the most
> commonly skipped. Everything the implementation later assumes was decided here — or was never
> decided at all and the implementation is guessing.

**Contents**
1. [The 24 fields that must transfer](#1-the-24-fields-that-must-transfer)
2. [The gaps that always exist](#2-the-gaps-that-always-exist)
3. [Sold vs Real — the six mismatch classes](#3-sold-vs-real--the-six-mismatch-classes)
4. [Detection tests for the first ten business days](#4-detection-tests-for-the-first-ten-business-days)
5. [Recovering from a bad or missing handover](#5-recovering-from-a-bad-or-missing-handover)
6. [When what was sold does not exist](#6-when-what-was-sold-does-not-exist)
7. [The handover meeting](#7-the-handover-meeting)
8. [Making the handover stick structurally](#8-making-the-handover-stick-structurally)

---

## 1. The 24 fields that must transfer

Score completeness as `n of 24` and print it in the plan. Anything absent is written
`UNKNOWN — requires <source or person>`, never left blank and never inferred silently.

### Commercial (7)

| # | Field | Schema name | Why the implementation needs it |
| --- | --- | --- | --- |
| 1 | ARR and products/SKUs sold | `subscription.arr`, `subscription.product` | Sets the mode and the services budget |
| 2 | Term, start and renewal date | `subscription.start_date`, `renewal_date`, `term` | The forward end of the plan |
| 3 | **Notice period in days** | `subscription.notice_period_days` | Without it there is no `opt_out_deadline` and therefore no value gate |
| 4 | Auto-renew default | `subscription.auto_renew` | Determines whether silence at renewal favours you or them |
| 5 | Seats purchased vs expected to be provisioned | `subscription.seats_purchased`, `seats_provisioned` | The gap is the rollout plan; a large gap is a commercial mismatch |
| 6 | Ramp schedule and any usage entitlement | `subscription.is_ramped`, `usage_entitlement` | A ramped deal changes what "on track" means in month 3 |
| 7 | Discount level and expiry, plus contracted uplift | `subscription.discount_pct`, `discount_expires`, `uplift_pct` | An expiring discount is a first-renewal conversation whether you raise it or not |

### The business case (6)

| # | Field | Schema name | Why the implementation needs it |
| --- | --- | --- | --- |
| 8 | Primary use case, in the customer's words | `opportunity` notes → plan field | Phase 2 is built to this. Getting it wrong is the most expensive error available |
| 9 | Secondary use cases and their sequence | plan field | Phase 8 depends on knowing what comes second |
| 10 | The pain that triggered the purchase, with a number if one was quoted | plan field | Becomes the baseline record's `value_driver` |
| 11 | The quantified promise made, if any | plan field | The Sold-vs-Real anchor. If a number was quoted in the deal, it will be quoted back at renewal |
| 12 | What they are doing today instead, and who owns it | plan field | Names the process owner and the incumbent's defender |
| 13 | The critical event or deadline driving the purchase | plan field | If a customer date exists, it may override the TTFV target as the value-gate anchor |

### People (6)

| # | Field | Schema name | Why the implementation needs it |
| --- | --- | --- | --- |
| 14 | Economic buyer — name, title, and what they personally care about | `contact.role = economic_buyer` | The person whose number has to move |
| 15 | Champion, and why *they* wanted this | `contact.role = champion` | Their motivation is not the company's motivation, and both matter |
| 16 | Exec sponsor, and whether they are real or nominal | `contact.role`, `influence` | Determines whether rung 3 of the escalation ladder exists |
| 17 | Sceptics and blockers named during the cycle | `contact.role = blocker` | The people who will slow phase 2 and nobody warned you |
| 18 | Intended admin(s) and technical owner | `contact.role = admin` | Phase 5's audience; one name here is a schedule risk |
| 19 | Procurement/legal posture and how hard the deal was | plan field | Predicts the first renewal's friction level |

### Technical and delivery (5)

| # | Field | Schema name | Why the implementation needs it |
| --- | --- | --- | --- |
| 20 | Integrations promised, named individually | plan field | Each is a phase-3 workstream with its own customer owner |
| 21 | Data sources, volumes and the historical window discussed | plan field | Phase 4's scope. The commonest source of a blown estimate |
| 22 | Security, compliance and procurement gates still open | plan field | These block access, which blocks everything |
| 23 | Services sold: hours, SOW scope, and what was explicitly excluded | PSA `hours_sold` | The denominator of the burn ratio, and the boundary of "in scope" |
| 24 | Commitments made outside the contract — roadmap items, custom work, "we can probably…" | plan field | The single most common cause of a first-renewal dispute |

**Field 24 is the one everybody skips and everybody needs.** Ask it directly and ask it twice:
*"What did you tell them we'd do that isn't written down anywhere?"* Sellers answer this honestly
when asked plainly, and evasively when asked in a form.

---

## 2. The gaps that always exist

These recur across companies and motions. Assume they are present until you have checked.

| Gap | Why it happens | Cost if uncaught | Cheapest detection |
| --- | --- | --- | --- |
| **The use case is stated at feature level, not process level** | Sales sells capability; delivery needs workflow | Phase 2 configures the wrong thing and it is discovered at end-user training | Ask the champion to walk you through the process end to end in phase 0 |
| **Verbal commitments are unrecorded** | Nobody wants to write down what they hedged in a room | Surfaces at renewal as "you promised" | Field 24, asked verbally |
| **The admin was never identified** | The buyer is not the user, and nobody asked who would run it | Phase 5 has no audience; schedule slips a fortnight | Ask for the admin's name and email before kickoff, in phase 0 |
| **The historical data window was never discussed** | Migration was assumed to be "load the data" | Phase 4 estimate blows out 2–4× | Ask what window makes the first value moment believable |
| **Seats were bought for a future state** | Multi-year budget, or a discount tier | Utilisation looks catastrophic for two quarters and health scores go red for no reason | Get the intended rollout curve, by team and month, and score against *that* |
| **The critical event was never captured** | It was in the AE's head as urgency, not in the record | You plan to your TTFV target and miss their board date | Field 13; if a customer date exists it usually beats your target |
| **The sceptic was never named** | Sales talks to supporters | Phase 2 or 6 stalls on an objection nobody prepared for | Ask "who else evaluated this and what worried them" |
| **The security review was assumed complete** | It was "in progress" at signature | Access is blocked for weeks and the whole plan slides | Confirm status by document, not by recollection, in phase 0 |

---

## 3. Sold vs Real — the six mismatch classes

Every mismatch belongs to exactly one class, and the class determines the recovery. Log all of them
in the Sold-vs-Real table with an owner and a dated resolution.

| Class | Definition | Typical signature | Recovery | Escalate to |
| --- | --- | --- | --- | --- |
| **Capability** | A feature was promised that does not exist, or exists differently | The customer describes a behaviour the product does not have | Confirm in writing what the product does today; file a roadmap request with an ID; offer the nearest supported workflow; put the gap in the handover record so the renewal team is not ambushed | Product + vendor exec |
| **Scope** | Services were sized for less work than the use case requires | Burn ratio passes 1.0× before phase 4 completes | Re-scope with a change order, or cut the first use case to what the hours cover. Never absorb silently — that is how services margin disappears | Vendor PM + customer champion |
| **Timeline** | A go-live date was promised that the critical path does not support | Float is negative at kickoff | Present the float arithmetic, then choose: smaller first use case, more customer owners, or a re-baselined date agreed in writing | Both exec sponsors |
| **Stakeholder** | Nobody who will actually use the product was in the sales cycle | The champion cannot name the process owner | Insert a discovery session before phase 2; treat the phase-2 exit criterion as unmet until the process owner has witnessed it | Champion |
| **Commercial** | Entitlement far exceeds deployable capacity | 200 seats bought, 40 people in the whole function | Build the rollout curve by team and month, agree it with the buyer, and score utilisation against that curve rather than the contracted total | Economic buyer |
| **Data** | The source data does not exist in the shape the product needs | Field mapping cannot be completed | Re-scope phase 4; consider a narrower first use case that uses data that does exist. This is the mismatch most likely to end the implementation | Customer data owner + vendor architect |

**Timing is the whole economics of this table.** A capability gap found in week 2 is a roadmap
conversation with a filed request. The same gap found in month 5 is a renewal negotiation in which
you have no evidence and they have a grievance. Nothing about the gap changed — only when it was
named.

---

## 4. Detection tests for the first ten business days

Run all six. Each is designed to be cheap and to fail loudly.

| Day | Test | Detects | Fail signature |
| --- | --- | --- | --- |
| 1–2 | **Read the contract against the handover record.** Compare SKUs, seats, entitlement, term, notice period and any services line to what the handover claims | Commercial mismatch; missing notice period | Any field where the two disagree, or `notice_period_days` absent |
| 2–3 | **Have the champion describe the process end to end, unprompted.** Do not lead | Capability and stakeholder mismatch | They describe a behaviour the product does not have, or cannot name who owns a step |
| 3–5 | **Ask for one real sample of the source data**, not a description of it | Data mismatch | The extract is unavailable, or the required field is empty in most rows |
| 4–6 | **Price the critical path** against the SOW hours and the phase durations | Scope and timeline mismatch | Critical path exceeds the date, or estimated hours exceed hours sold before phase 4 |
| 5–8 | **Count the named customer owners** across phases 2, 3 and 4 | Serialisation risk | Fewer than three distinct names — the critical path is about to triple |
| 8–10 | **Ask the AE field 24 verbally**, then ask the champion the same question differently: *"What are you expecting from us that we haven't talked about yet?"* | Unrecorded commitments | The two answers differ, or the champion names something not in the contract |

Every failure becomes a row in the Sold-vs-Real table with a class, an owner and a dated
resolution. A detected mismatch with no date is not detected, it is noticed.

---

## 5. Recovering from a bad or missing handover

When the handover is thin, wrong or absent, do not start phase 2. Run this instead — it takes
about half a day and it is always cheaper than building to a guess.

| Step | Action | Source | Output |
| --- | --- | --- | --- |
| 1 | Reconstruct the commercial record from the contract and the billing system, not from the CRM opportunity | Contract PDF, `subscription`, `invoice` | Fields 1–7 |
| 2 | Read the closed-won opportunity: notes, competitor field, loss/win reason, and stage history | `opportunity` | Fields 8, 13, 19 |
| 3 | Read the last 10 emails and any call recordings from the final 30 days of the cycle | `interaction`, conversation intelligence | Fields 10, 11, 24 — verbal commitments live here |
| 4 | Rank contacts by participation in the final 30 days; the most-active non-vendor participant is usually the champion | `interaction.customer_participants` | Fields 14–18, marked `inferred` with the rule stated |
| 5 | Ask the AE the four questions in §7 verbally. Twenty minutes, not a form | The AE | Fields 8, 11, 24 confirmed or corrected |
| 6 | Confirm everything with the customer at kickoff by *restating* it, not by asking | Kickoff | Corrections, which are themselves findings |
| 7 | Write the completeness score and every remaining `UNKNOWN — requires X` into the plan | — | `n of 24`, with owners and dates on the gaps |

**Restating beats asking.** "Our understanding is that you bought this to cut month-end close from
eleven days to five, and that Priya owns that number — is that right?" surfaces mismatches
instantly and costs the customer no effort. Asking them to re-explain what they told sales costs
them effort and tells them nobody listened.

**If the AE has left the company**, steps 1–4 are the whole recovery and step 6 carries all the
weight. Say so in the plan and cap the confidence on the business-case fields accordingly.

---

## 6. When what was sold does not exist

The hardest case, and the one where most CSMs make it worse. Four rules:

| Rule | Why |
| --- | --- |
| **Establish the facts before the conversation.** Confirm with product what the capability does and does not do today, and whether it is on the roadmap with a date | Walking in without this turns the meeting into a negotiation over what was said |
| **Never re-promise on product's behalf.** A roadmap item is a request ID and a status, not a commitment | The second broken promise costs far more than the first, because it removes the customer's trust in your corrections too |
| **Offer the nearest supported workflow the same day.** "Here is what we can do now, here is what it costs you relative to what you expected" | Customers forgive a gap far more readily than they forgive a gap plus a delay |
| **Write the gap into the account record.** It travels to the receiving CSM and to the renewal | Otherwise it resurfaces at renewal as a surprise to the one person who could have prepared for it |

**The commercial conversation, when the gap is material.** If the missing capability is why they
bought, the options are, in order of preference: re-scope the first use case to something the
product delivers today and re-baseline V-day · extend the term at no charge to cover the roadmap
delivery window · restructure to a smaller entitlement now with an expansion trigger on delivery ·
a mutual exit. Raise it early, with the exec sponsor, while all four are still available. Waiting
until the renewal window leaves only the last one.

**Never argue about what was said.** The customer's recollection and the AE's recollection will
differ and neither can be settled. Argue about what happens next — that is the only part anyone can
change.

---

## 7. The handover meeting

Twenty minutes, live, with the AE. Not a form. A form gets the fields that are easy to type; the
call gets field 24.

**Attendees:** AE · implementation lead · receiving CSM. Solutions engineer if there was one.

**The four questions that carry the meeting:**

1. *"Walk me through what they're actually trying to do — the process, not the features."*
2. *"What did you tell them we'd do that isn't in the contract?"* (field 24)
3. *"Who on their side is going to make this hard, and why?"*
4. *"What's the one thing that, if it doesn't happen in the first 60 days, means this doesn't renew?"*

**Exit criterion:** the 24 fields are populated or explicitly marked `UNKNOWN — requires X`, and
the implementation lead can restate the primary use case in the customer's own words without
looking at notes.

**Compensation reality.** A handover that depends on the AE's goodwill will degrade the moment
their quota calendar gets tight. If handovers are chronically thin, the fix is structural — see §8 —
not another reminder email.

---

## 8. Making the handover stick structurally

Process discipline fails; structure holds. Four mechanisms, in increasing order of effectiveness:

| Mechanism | How it works | Effort |
| --- | --- | --- |
| **Required fields on close** | The opportunity cannot be marked closed-won without fields 8, 13, 14, 20, 21, 23 | CRM admin, one afternoon |
| **Completeness score on the account** | `n of 24` is a visible field; onboarding reports it weekly by AE | CRM + a report |
| **Kickoff cannot be booked without a completeness threshold** | Below a set score, the handover meeting is mandatory before scheduling | Process rule with a real gate |
| **Post-onboarding attribution** | Every first-year churn's postmortem records whether the root cause was visible in the handover; the pattern goes to sales leadership by rep | `churn-postmortem` feeds it |

The fourth is the only one that changes seller behaviour, because it is the only one that connects
handover quality to something the seller is measured on. Everything upstream of it relies on the
seller choosing to do a thing they are not measured on, at the moment they are least incentivised
to — which is an argument for instrumenting the input, not for asking harder.
