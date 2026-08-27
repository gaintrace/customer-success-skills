# The Kickoff Call

> The kickoff is not a status meeting and it is not a relationship meeting. It is the one hour in
> which the finish line, the owners, the measurement and the escalation path are fixed. Everything
> the implementation later argues about is either settled here or unsettled forever.

**Contents**
1. [What must be established](#1-what-must-be-established)
2. [Agenda with time allocations](#2-agenda-with-time-allocations)
3. [The questions that surface a doomed implementation](#3-the-questions-that-surface-a-doomed-implementation)
4. [Attendance rules](#4-attendance-rules)
5. [The baseline capture record](#5-the-baseline-capture-record)
6. [The escalation path](#6-the-escalation-path)
7. [The customer's internal comms plan](#7-the-customers-internal-comms-plan)
8. [The 24-hour written summary](#8-the-24-hour-written-summary)
9. [Kickoff failure modes](#9-kickoff-failure-modes)

---

## 1. What must be established

Six items. The call is not complete until all six exist in writing, and the exit criterion for
phase 1 is the **customer's written confirmation**, not the meeting itself.

| # | Item | What "established" means | If you leave without it |
| --- | --- | --- | --- |
| 1 | **Business objectives** | 1–3 outcomes in the customer's words, each tied to a metric that exists in a system they own | The plan optimises for product adoption, and adoption is not what gets renewed |
| 2 | **Success criteria and their measurement** | Per objective: the metric, the baseline value, the target, the date, the measurement owner, the attribution % | V-day is unprovable. The first renewal is argued on feelings |
| 3 | **Stakeholder map** | Exec sponsor · champion · process owner · data owner · admin(s) · system owner per integration · team leads. Named, with email and title | Phases serialise behind one person and the schedule you promised is fiction |
| 4 | **Timeline with both-side owners** | Every phase carries a customer owner, not just a vendor owner | Slip is invisible until it is expensive |
| 5 | **Escalation path** | Who to call, at what threshold, on both sides, with a response time | Problems escalate through the champion, who becomes the bottleneck and then the bad news |
| 6 | **The customer's internal comms plan** | Sender, date, distribution, stated deadline, non-adoption consequence | Trained users who were never given permission to change how they work |

**Anchor the whole call on item 1.** Open with their objectives, not your product. A kickoff that
opens with a product overview teaches the customer that this is a vendor project, and they will
staff it accordingly.

---

## 2. Agenda with time allocations

**60 minutes, white-glove.** Guided runs the same spine in 30 minutes by cutting §3 and §7 to
five minutes each and pre-filling them from the handover.

| Min | Segment | Who runs it | Output |
| --- | --- | --- | --- |
| 0–5 | **Sponsor opens** — why the customer bought, in their exec's own words | Customer exec sponsor | The room hears that this is a customer project |
| 5–15 | **Objectives and success criteria** — confirm or correct what sales recorded | Vendor implementation lead, asking | Item 1 + item 2 drafted live on screen |
| 15–25 | **Baseline capture** — for each objective: current value, source, owner, target, date | Vendor CSM | The §5 record, populated |
| 25–35 | **Stakeholders and owners** — walk the phase list, name a customer owner for each | Vendor PM | Item 3 + item 4 |
| 35–45 | **Timeline, backwards from V-day** — show the value gate, then the phases behind it | Vendor PM | Agreement, or a scope conversation now rather than in month four |
| 45–52 | **Risks, dependencies and the escalation path** | Vendor PM | Item 5, plus the top three dependencies with owners |
| 52–58 | **Internal comms plan and the rollout announcement** | Vendor CSM, asking the champion | Item 6 |
| 58–60 | **Next steps** — three actions, each with an owner and a date | Vendor PM | The first MAP rows |

**Show the value gate on screen.** Most kickoffs present a forward Gantt from today. Presenting the
timeline backwards from V-day — with the opt-out deadline visible behind it — changes the customer's
posture in the room, because it makes their own deadline the subject rather than yours.

---

## 3. The questions that surface a doomed implementation

Ask all nine. Each is designed so that the *dangerous* answer is the easy one to give, which is why
the answers are useful. Record the answer verbatim; the wording matters more than the summary.

| # | Question | The answer that should worry you | What it means | What to do about it |
| --- | --- | --- | --- | --- |
| 1 | "What has to be true in six months for you personally to say this was worth doing?" | A vendor-shaped answer ("we'll be fully rolled out") rather than a business-shaped one | Nobody on the customer side owns an outcome. The project is a purchase, not a change | Push for a number. If none exists, escalate to the exec sponsor before phase 2 |
| 2 | "Who else evaluated this, and what were they worried about?" | "Nobody, it was my call" | Single-threaded from day one, and the internal case has never been stress-tested | Multithread in phase 0. Ask the champion to introduce the sceptic |
| 3 | "What are you doing today instead, and who owns that process?" | A vague answer, or an owner nobody named | The incumbent process has a defender you have not met | Get the process owner into phase 2 as the named customer owner |
| 4 | "What else is your team delivering this quarter?" | Three or more competing initiatives, one of which is a platform migration | Your project is fourth in a queue of four. The slip is already scheduled | Re-plan the phase durations against their real capacity, now, and show the float impact |
| 5 | "Who is going to configure this, and how much of their week do they have?" | "We'll figure it out" or one person for everything | Single-admin serialisation — the critical path is about to triple | Name a second owner before committing to a date (see phase-playbook §3) |
| 6 | "What data does this need, where does it live today, and who owns it?" | "It's in the system somewhere" | A data gap, the most common cause of a blown migration estimate | Move data discovery into phase 0 and re-cost phase 4 |
| 7 | "When your finance team reviews this line item next year, what will they ask for?" | "I don't think they will" | No plan for the renewal conversation, and the buyer has not thought about defending it | Design the baseline record specifically to answer that question |
| 8 | "What would make you stop this project?" | Silence, or a laugh | Either the risk is unexamined, or they will not say it in front of their exec | Ask the champion again, privately, within 48 hours |
| 9 | "Has anything changed since you signed?" | A reorg, a budget review, a departure, a new CIO | The business case has an owner problem, and the sales handover is already stale | Re-run the Sold-vs-Real reconciliation before phase 2 |

**Two questions to ask privately after the call**, because they will not be answered honestly in
front of an exec sponsor: *"Where do you think this is most likely to get stuck?"* and *"Who on
your side is not convinced?"*

**Record every answer in the account record with the date and the speaker.** These verbatim quotes
are the highest-value asset in the whole implementation — they are what the first business review
opens with, and what the receiving CSM inherits.

---

## 4. Attendance rules

| Role | Required? | If absent |
| --- | --- | --- |
| Customer exec sponsor | Yes for white-glove; the first 5 minutes minimum | Reschedule once. If they decline twice, record it as a risk: an implementation with no exec sponsor has no escalation path and no budget defender |
| Champion | Always | Do not run the call |
| Process owner | White-glove and guided | Phase 2 configuration will be built to an assumption |
| Data owner | Where migration is in scope | Phase 4 has no sign-off authority; re-plan |
| Admin(s) | Always, both of them | Phase 5 has no audience and will be scheduled twice |
| Team leads | White-glove | Phase 6 has no owners; rollout stalls at the pilot |
| Vendor: implementation lead, CSM | Always | — |
| Vendor: AE who sold it | First 10 minutes | The handover has a gap the customer will find before you do |

**The AE's ten minutes matter.** Having the seller in the room while the buyer restates the
objectives is the cheapest possible detection of a Sold-vs-Real mismatch — it surfaces in front of
everyone, in week one, when it is still a scope conversation.

---

## 5. The baseline capture record

Capture at signature or kickoff, **never at renewal**. A baseline captured after go-live is not a
baseline — it already contains the effect you are trying to measure.

One record per value driver:

| Field | Type | Example | Why it is required |
| --- | --- | --- | --- |
| `value_driver` | string | Month-end close cycle time | The customer's outcome, not your feature |
| `metric_name` | string | Business days from period close to sign-off | Must be a metric that already exists in a system they own |
| `baseline_value` | number | 11.0 | The number V-day is measured against |
| `baseline_period` | date range | 2026-04-01 → 2026-06-30 (3-month average) | A single month is noise; use ≥3 periods |
| `baseline_source` | string | Customer ERP close log, export pulled 2026-07-08 | Provenance. Without it the number is unusable at renewal |
| `measurement_owner_customer` | person | Priya N., Director of Finance Ops | A named human who will confirm the number later |
| `unit_economics` | number + basis | $2,400 fully loaded cost per close day (customer-supplied) | Converts the metric into dollars — the language the renewal is decided in |
| `target_value` / `target_date` | number / date | 5.0 by 2026-12-15 | The target *is* V-day's success criterion |
| `attribution_pct` | number | 70%, set by Priya | Set by the customer, never by you. A silent 100% is indefensible |
| `confidence` | High / Medium / Low | Medium — one confounding process change in Q3 | Names the confounder before the customer does |
| `last_validated` | date | 2026-08-14 | Baselines drift; a stale baseline is a historical fact, not a measurement |

**When no baseline exists — fallbacks, in strict order of defensibility:**

| # | Fallback | Notes |
| --- | --- | --- |
| 1 | The customer's own pre-period system data, reconstructed from their warehouse or logs | Always try this first; it is usually available and nobody asked |
| 2 | A **control group** — a business unit, region or cohort not yet adopting | The strongest available substitute for a counterfactual, and it makes a difference-in-differences claim possible later |
| 3 | A **customer-attested estimate**, signed off by a named owner, in writing, using the **low end** of any range they give | The low end is what makes it survive scrutiny |
| 4 | An industry benchmark with an explicit haircut (e.g. × 0.5), labelled as an estimate | Last resort. Never present as measured |

If none of the four is achievable, write `UNKNOWN — requires a baseline for <metric> from
<system/owner>` and put it in the plan as a phase-0 action with an owner and a date. Do not proceed
to phase 2 with an unmeasurable success criterion and call the plan complete.

---

## 6. The escalation path

Agree it while nothing is wrong. An escalation path negotiated during an escalation is not a path,
it is a fight.

| Rung | Vendor side | Customer side | Trigger | Response time |
| --- | --- | --- | --- | --- |
| 1 | Implementation lead | Champion | Any milestone slips its due date | Same business day |
| 2 | CSM + CS manager | Champion's manager or the process owner | ≥2 milestones overdue, or cumulative slip >10 days | 2 business days |
| 3 | Vendor exec sponsor | Customer exec sponsor | Cumulative slip >30 days, float ≤4 days, or a phase blocked >10 business days | 48 hours |
| 4 | Vendor exec + commercial lead | Customer exec + procurement | Float negative, or a Sold-vs-Real capability gap with no resolution | 1 week, with a written plan |

Two rules that make the ladder work:

- **Named humans, both sides, in the plan.** "Support" and "the business" are not owners.
- **The trigger is objective.** Escalation on a threshold, not on someone's mood, is what stops
  escalation from being read as a complaint about a person.

---

## 7. The customer's internal comms plan

The customer's own announcement is a deliverable of the onboarding plan. Capture five fields and
put them in the MAP with a date:

| Field | Why it matters |
| --- | --- |
| **Sender** | An announcement from the vendor is marketing; from a team lead it is a nudge; from the exec sponsor it is a mandate. The sender sets the adoption ceiling |
| **Date** | Must land **before** end-user training, never after. Training without permission produces informed non-adopters |
| **Distribution** | The exact list. "Everyone" means the message reaches the people who already knew |
| **Stated deadline** | "From 1 October, expense approvals happen here." A rollout with no date is an invitation |
| **Non-adoption consequence** | What happens to the old process. If the old way still works, most people will keep using it — and no amount of training changes that |

**The old-process question is the one that predicts adoption.** Ask directly: "On what date does
the current way of doing this stop being available?" If the answer is "it doesn't", the plan needs
a phase-8 row for retiring it, with a customer owner and a date, or utilisation will plateau
wherever the enthusiasts stop.

---

## 8. The 24-hour written summary

Send within one business day. It is the phase-1 exit artifact, and the champion's written
confirmation is the exit criterion.

Required sections:

1. **Objectives** — 1–3, in their words, quoted
2. **Success criteria** — the baseline record table from §5, one row per driver
3. **The two gates** — G-day and V-day, with dates and the arithmetic that produced them
4. **Stakeholders and owners** — by name, per phase, both sides
5. **Timeline** — the backwards-planned phase table with dates
6. **Escalation path** — the §6 ladder with names filled in
7. **Internal comms plan** — the five §7 fields
8. **Open questions** — every `UNKNOWN — requires X`, with an owner and a date
9. **Next three actions** — action · owner · date · expected effect · success measure

Close with one sentence asking for written confirmation, and name what happens if it does not
arrive: *"If I don't hear back by Friday I'll assume this is right and start phase 2 against these
dates."* Silence then becomes a decision rather than a gap.

---

## 9. Kickoff failure modes

| Failure | Signature | Correction |
| --- | --- | --- |
| Kickoff as product demo | 40 of 60 minutes is vendor screen-share | Objectives first. The product is phase 2's problem |
| Kickoff as discovery | The vendor asks questions the customer answered during the sale | Phase 0 exists precisely to prevent this. Read the handover |
| No exec sponsor in the room | Champion says "they're busy, I'll brief them" | Reschedule once, then record it as a plan risk with a named escalation |
| Owners assigned to teams | "IT will handle integration" | Named humans with email addresses, or the phase has no owner |
| Timeline presented forwards | A Gantt starting today | Present it backwards from V-day with the opt-out deadline visible |
| Success criteria with no measurement | "Improve efficiency" | Metric, baseline, source, owner, target, date, attribution % — or it is not a criterion |
| Escalation path skipped because things are going well | Nobody mentions it | Agree it now; you will not get a clean agreement later |
| No written summary | The call was great, nothing was recorded | The meeting is not the exit criterion. The confirmed summary is |
| The comms plan treated as the customer's private business | "They'll tell their people" | It determines your adoption ceiling. Ask for the five fields |
| Everyone leaves without a date | "We'll follow up next week" | Three actions with owners and dates, before anyone drops off the call |
