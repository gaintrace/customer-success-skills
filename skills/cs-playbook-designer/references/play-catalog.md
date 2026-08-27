# The Play Catalogue

> Thirty-six standard plays across seven categories, each with its trigger, owner role, SLA, exit
> and the leading outcome it is measured on. Take six to eight. Sizing decides which — see
> `trigger-design.md` §3 and `../scripts/play_sizing.py`.
>
> Signal IDs refer to `../../cs-context/references/signal-library.md`; fields to
> `../../cs-context/references/normalized-schema.md`. `SLA` is measured from trigger fire, not
> from acknowledgement.

**Contents**
1. [What the business model changes](#1-what-the-business-model-changes)
2. [Human, automated, hybrid](#2-human-automated-hybrid)
3. [Risk plays](#3-risk-plays)
4. [Adoption plays](#4-adoption-plays)
5. [Onboarding plays](#5-onboarding-plays)
6. [Expansion plays](#6-expansion-plays)
7. [Lifecycle plays](#7-lifecycle-plays)
8. [Advocacy plays](#8-advocacy-plays)
9. [Administrative plays](#9-administrative-plays)
10. [Eight plays in full](#10-eight-plays-in-full)
11. [Choosing the starting set](#11-choosing-the-starting-set)

---

## 1. What the business model changes

Resolve the profile in `../../cs-context/references/business-model-profiles.md` first. This table
is the difference between a catalogue that fits the business and one that reads as generic.

| Model | Plays that do not apply | Plays that replace them | Timing change |
| --- | --- | --- | --- |
| **Consumption / usage-based** | Seat-limit approach, seat true-up, utilisation-floor adoption | Commitment-pacing rescue (`C15`), overage-to-commitment, true-up disclosure | Ladder keys to the commitment period, not the renewal |
| **Product-led / self-serve** | Review window, sponsor cadence, champion continuity (below the top ARR decile), goal-matched cross-sell | In-app activation stall, dunning, self-serve expansion prompt | No notice period — detection windows in days, not quarters |
| **Monthly evergreen** | The opt-out ladder | Continuous 7/14-day risk windows | `R1` does not apply as written: every day is the deadline |
| **Self-hosted / on-prem / channel** | Every usage-telemetry play | Support-load, relationship and commercial plays only | Coverage is structurally capped — say so in the ledger |
| **Regulated vertical** | — | Add a procurement/security-review step with its own owner to the lifecycle ladder | Ladder starts at T-270, not T-180 |
| **Seasonal** | — | — | Every decay qualifier masks the account's known low season |

**Never sell a play the model cannot execute.** A review-window play on a self-serve book, or seat
utilisation on a consumption book, is the most recognisable form of rookie output — it tells the
reader the catalogue was copied rather than designed.

## 2. Human, automated, hybrid

The default is **hybrid: automation prepares, a human decides, automation executes.** Detection,
assembly, task creation, logging and send mechanics are automated. The decision to run, and the
words in any relationship message, are not.

| Layer | Automate | Keep human |
| --- | --- | --- |
| Detect and qualify | Always | — |
| Assemble the evidence and pre-fill the draft | Always | — |
| Decide to run | Risk, expansion, advocacy and all exec-facing plays: **no** | Yes, on all four |
| Send | Administrative, in-app enablement, dunning first touch, review requests | Every relationship message |
| Log, remind, escalate on SLA breach | Always | — |
| Exit decision | Administrative and lifecycle only | Risk, save, expansion |

**Never automated, in any category** — each has ended a renewal that was not otherwise at risk:

- Anything carrying an apology, or following an incident on our side.
- Champion or exec-sponsor departure outreach (`R3` — VP or above, human, 48 hours).
- Any message addressed to a named executive.
- Any commercial ask, price change or contract term.
- Anything that reveals an inference about a named person ("we noticed Jamie left").
- Any send on an account with an open escalation, an active save play or a live negotiation.
- Any commitment to a date the sender does not own (`R19`).

---

## 3. Risk plays

| ID | Play | Trigger | Owner role | SLA | Exit (success) | Leading outcome measured |
| --- | --- | --- | --- | --- | --- | --- |
| `PB-R01` | Usage-decay rescue | `U2` WAU < 0.70 of own baseline, 2 weeks | CSM | 48h | Actives ≥70% of baseline within 45d | WAU ratio at day 45 |
| `PB-R02` | Champion continuity | `R1` hard bounce / directory removal on champion or economic buyer | VP CS (email 1), CSM (email 2) | **48h** (`R3`) | Named successor meets us within 21d | Successor engaged, second contact live |
| `PB-R03` | Support-cluster ownership | `P1` ≥3 tickets in 7d, normalised per 100 seats | CSM (not Support) | 24h | Root cause named and owned; no new cluster in 30d | Cluster recurrence at day 30 |
| `PB-R04` | Detractor closed loop | `S1` survey score 0–6 | CSM; VP CS if the respondent is an exec | 24h | Verbatim addressed, action agreed with a date | Re-survey or a stated resolution |
| `PB-R05` | Commercial-event response | `C1` auto-renew off · `C2` notice · `R11`/`R12` procurement or termination terms · `T6` bulk export | VP CS + AM | **Same day**, cool-down exempt (`R2`) | Customer confirms a review and includes us with a process and dates | Meeting held with the economic buyer |
| `PB-R06` | Silence re-engagement | `Z1` ≥45d no bilateral interaction, ARR ≥ floor | CSM, then CSM's manager | 5 business days | Reply from any named contact within 21d | Reply received; second contact engaged |
| `PB-R07` | Managed exit | Stop-loss reached on any save (`R21`) | AM | 5 business days | Exit dated, win-back record opened, reference preserved | Win-back record exists; no escalation at exit |

**Risk plays hand off, they do not compete.** `PB-R05` and any two P0 compound patterns go straight
to `save-play` and open a war room the same day (`R4`) — the playbook's job there is to route fast,
not to run the intervention itself.

## 4. Adoption plays

| ID | Play | Trigger | Owner role | SLA | Exit (success) | Leading outcome |
| --- | --- | --- | --- | --- | --- | --- |
| `PB-A01` | Unused entitled feature | Feature is paid for, mapped to a stated goal, adoption <50% at day 60 | CSM (digital below the ARR floor) | 7d after the gap persists | Feature in use by ≥3 users within 30d | Distinct users of that feature |
| `PB-A02` | Activation stall | `U8` activation event never reached, or reached then zero for 30d | CSM | 72h | Activation event recorded within 30d | Activation rate |
| `PB-A03` | Breadth gap | `U6` features used ÷ features in plan below the segment's own median | CSM | 14d | +1 material feature adopted in 60d | Feature breadth |
| `PB-A04` | Power-user drought | Distinct users doing the core action ≥ weekly fell below 3 | CSM | 14d | ≥3 weekly power users within 45d | Power-user count |
| `PB-A05` | Broken-integration repair | `T2` integration down >7 days | Support + CSM | 48h | Integration reconnected and passing for 14d | Integration uptime |

**Adoption plays are blacked out during escalations and onboarding.** An enablement nudge sent to
an account that is currently escalating is the single most common self-inflicted wound in an
automated library.

## 5. Onboarding plays

| ID | Play | Trigger | Owner role | SLA | Exit (success) | Leading outcome |
| --- | --- | --- | --- | --- | --- | --- |
| `PB-O01` | Kickoff-to-plan | Contract signed, no kickoff held within 10 business days | Onboarding lead | 2 business days | Kickoff held, plan agreed with dated milestones | Days signed → kickoff |
| `PB-O02` | Day-7 checklist stall | Fewer than 2 of 5 setup milestones at day 7 | Onboarding lead | Same day | ≥4 of 5 complete by day 21 | Milestone completion at day 21 |
| `PB-O03` | Admin never provisioned | No admin login within 48h of provisioning | Digital CS | 24h, automated | Admin logged in within 7d | Days to first admin login |
| `PB-O04` | Go-live to steady state | Go-live milestone reached | CSM | 5 business days | Handover held, success plan owner confirmed | Handover completed |
| `PB-O05` | First-90 exec check | Day 75 post-start, no exec-level contact recorded | CSM + VP CS | 10 business days | Exec meeting held before day 100 | Exec contact recorded |

Time-to-first-value is the number these five exist to move, and it is the strongest lever on
first-year retention. Measure them as a set, not individually.

## 6. Expansion plays

Every expansion play is gated on the health floor (`R8`) and on a **felt constraint** (`R10`) —
a utilisation number is a reason to look; "three people asked me for access and I said no" is a
reason to ask.

| ID | Play | Trigger | Owner role | SLA | Exit (success) | Leading outcome |
| --- | --- | --- | --- | --- | --- | --- |
| `PB-E01` | Seat-limit approach | `U4` utilisation ≥ 0.90 **and** a denied-access event or request | AM | 5 business days | Quote issued within 21d | Opportunity created with a named constraint |
| `PB-E02` | Overage-to-commitment | Overage on 2 consecutive invoices | AM | 5 business days | Commitment restructured or declined with a reason | Committed ARR change |
| `PB-E03` | New-department landing | A second department passes an adoption threshold | CSM → AM | 10 business days | Named buyer in the new department | New-department buyer identified |
| `PB-E04` | Goal-matched cross-sell | A stated objective in the success plan maps to an unpurchased product | AM | 10 business days | Discovery meeting held | Meeting held; objective restated by them |
| `PB-E05` | Co-term | Expansion opportunity inside 90 days of the opt-out deadline | AM | Immediate | Co-termed onto the renewal (`R12`) | Paper cycles avoided |

## 7. Lifecycle plays

The ladder keys to `opt_out_deadline = renewal_date − notice_period_days` (`R1`), and **every rung
carries a behavioural qualifier** — no rung fires on the calendar alone.

| ID | Rung | Behavioural qualifier | Owner role | Exit |
| --- | --- | --- | --- | --- |
| `PB-L01` | T-180 | Success plan not refreshed this term | CSM | Plan refreshed with dated objectives |
| `PB-L02` | T-120 | No exec-sponsor meeting in the last two quarters (`R6`) | CSM + VP CS | Exec meeting held |
| `PB-L03` | T-90 | Renewal conversation not yet held, or paper path unconfirmed (`R7`) | AM | Approval chain and signature process confirmed in writing |
| `PB-L04` | T-60 | Quote not issued, or procurement not engaged | AM | Quote issued and acknowledged |
| `PB-L05` | Review window | A decision is genuinely on the table (`R15`) | CSM | Decision made, or the review is cancelled and a one-pager sent |
| `PB-L06` | Anniversary value recap | Value evidence exists and is under 90 days old | CSM | Recap sent, response received |
| `PB-L07` | Sponsor cadence | Sponsor contact older than the segment's cadence | VP CS | Meeting held |
| `PB-L08` | Price-change notice | Contracted uplift or a list-price change lands this term | AM | Notice served inside the contractual window |

`PB-L05` is the rung that most often should not fire: **no decision to make means no review**
(`R15`). Send the one-pager and give the hour back.

## 8. Advocacy plays

| ID | Play | Trigger | Owner role | SLA | Exit (success) |
| --- | --- | --- | --- | --- | --- |
| `PB-V01` | Promoter to reference | `S1` score 9–10, health Secure, no ask in 180d | CSM | 5 business days | Reference agreed and logged |
| `PB-V02` | Milestone to case study | A **customer** milestone (a business outcome), not a functional one | CSM + Marketing | 10 business days | Approval to publish, or a documented no |
| `PB-V03` | Beta recruitment | Feature request logged by this account now shipping to beta | Product + CSM | 5 business days | Enrolled, or declined with a reason |
| `PB-V04` | Review request | Health Secure, no ask in 180d, at least one recorded win | Digital CS, automated | 5 business days | Review posted, or no response after 2 touches |

The functional-versus-customer milestone distinction is Lincoln Murphy's, and it is the whole play:
a feature being clicked is not an achievement worth congratulating, and treating it as one is how a
vendor teaches a customer to ignore its email `[P · Lincoln Murphy, Sixteen Ventures]`.

## 9. Administrative plays

These are the cheapest revenue in the catalogue: involuntary loss, prevented by a workflow.

| ID | Play | Trigger | Owner role | SLA | Exit (success) |
| --- | --- | --- | --- | --- | --- |
| `PB-X01` | Payment failure | 2 failed attempts, or `C10` dunning entered | Billing (automated first touch), AM at day 7 | 24h | Payment collected |
| `PB-X02` | Contact hygiene | Hard bounce on any non-champion contact, or a new admin detected | Digital CS, automated | 72h | Record corrected; new admin oriented |
| `PB-X03` | Entitlement true-up | Usage above contracted quantity | AM | 5 business days, disclosed within 5 days of detection | Resolved by upgrade or by a documented allowance |
| `PB-X04` | Ownership handover | `owner_csm` changes | Incoming CSM | 10 business days | Introduction sent, context transferred, first meeting held |
| `PB-X05` | Data-quality repair | An account fails the join, or a required field is null on a renewal inside 180 days | CS Ops | 10 business days | Field populated; account rejoins the eligible population |

`PB-X03` carries a rule worth stating plainly: **the first the customer hears about over-consumption
must not be the invoice.** Disclose within five business days of detection, with the value the
over-consumption produced. A true-up ambush triggers procurement involvement that costs more than
the overage.

---

## 10. Eight plays in full

The eight worth specifying completely, because they carry most of the revenue effect and most of
the ways to get it wrong.

### `PB-R01` Usage-decay rescue

| | |
| --- | --- |
| **Trigger** | `U2` `wau_7d / median(wau_7d, trailing 90d excl. last 14d) < 0.70`, two consecutive weekly evaluations |
| **Qualify** | Tenure ≥180d · ARR ≥ floor · not onboarding · seasonality mask on · instrumentation guard on · buying-team segmentation applied where department attribution exists |
| **Steps** | 1. Diagnose before contact: which team, which action, since when, and what else changed (CSM, 24h, automated assembly). 2. Reach out with the observation and a hypothesis, not a question (CSM, 48h). 3. Working session on the specific blocker, not a check-in (CSM, 14d). 4. Confirm the fix in the data (CSM, 45d) |
| **Exits** | Success: actives ≥70% of baseline by day 45 · Failure: flat at day 45 → escalate one band, hand to `churn-risk` for a full sweep · No longer eligible: ratio recovers above 0.85 before step 2 · Stop-loss: n/a |
| **Measure** | Leading: WAU ratio at day 45 against the account's own baseline. Retention delta: only against the 10% holdout |
| **The most common error** | Arriving without having read their tickets. If the decay followed a support cluster, showing up unprepared confirms their conclusion that nobody was listening |

### `PB-R02` Champion continuity

| | |
| --- | --- |
| **Trigger** | `R1` hard bounce, directory removal, or a title change on a contact with `role ∈ {champion, economic_buyer}` |
| **Qualify** | Run guard 11 first — mailbox full, out-of-office and domain migration are not departures. Check for a forwarding address and for a successor already appearing in product or ticket data |
| **Steps** | 1. Verify the departure (CS Ops, 4h, automated evidence assembly). 2. **Email 1 from VP CS or above** to the most senior known contact — continuity and partnership, not "who replaced Jamie" (VP CS, 48h, `R3`). 3. Email 2 from the CSM, 2–4 days later, with the working detail. 4. Rebuild the business case with the successor from zero inherited context (CSM, 21d). 5. Open a risk record that persists to the opt-out deadline regardless of how the first meeting goes |
| **Exits** | Success: successor named, meets us within 21d, and can state the objective in their own words · Failure: no successor at 30d, or the first meeting cancelled twice → `save-play` · Stop-loss: n/a |
| **Measure** | Leading: successor engaged within 21d; second contact live within 45d |
| **Never automated** | Every step that touches a person. An automated "sorry to see you go" to a departed champion's replacement is unrecoverable |

### `PB-R03` Support-cluster ownership

| | |
| --- | --- |
| **Trigger** | `P1` ≥3 tickets in a rolling 7 days, normalised per 100 seats |
| **Steps** | 1. Cluster the tickets and name the root cause (CSM + Support lead, 12h). 2. Message from the **CSM, not Support** — ownership, the pattern Support cannot see, and a named owner (CSM, 24h). 3. Fix or workaround delivered with a date the owner agreed (`R19`). 4. Check at 30 days for recurrence |
| **Exits** | Success: root cause owned, no new cluster in 30d · Failure: recurrence → escalate under the severity matrix · No longer eligible: cluster resolved before step 2 |
| **Measure** | Leading: cluster recurrence at day 30; reopen rate on the linked issue |

### `PB-R06` Silence re-engagement

| | |
| --- | --- |
| **Trigger** | `Z1` ≥45 days with no bilateral interaction, ARR ≥ floor, covered account |
| **Qualify** | This one fires broadly. Without an ARR floor and a renewal-proximity qualifier it becomes a list, not a trigger — see `trigger-design.md` §3 |
| **Steps** | 1. Touch 1: CSM, to the primary contact, with a specific observation (48h). 2. Touch 2: **a different named contact**, 7 days later. 3. Touch 3: **a different sender** — the CSM's manager — 14 days later. 4. Permission-to-close message at day 21, then park until a fresh trigger |
| **Exits** | Success: reply from any named contact within 21d · Failure: no reply after touch 3 → mark single-threaded, carry full ARR as at-risk (`R5`), revisit at the next lifecycle rung |
| **The rule** | Change the sender, the subject and the ask — not just the words. Three versions of the same message is one message sent three times |

### `PB-A01` Unused entitled feature

| | |
| --- | --- |
| **Trigger** | The feature is (a) paid for and (b) mapped to a stated customer objective, and adoption is below 50% at day 60 |
| **Qualify** | Both conditions, not just the first. A paid-for feature nobody asked for is a packaging problem, and pushing it is a vendor's agenda wearing a customer's clothes |
| **Steps** | 1. Quantify the gap in their terms — what the unused entitlement costs them per month. 2. Offer one 20-minute path, not a training programme. 3. Enable with the admin. 4. Confirm ≥3 distinct users at day 30 |
| **Exits** | Success: ≥3 users in 30d · Failure: no enablement session booked after 2 touches → log as a packaging finding, not a CSM failure |

### `PB-E01` Seat-limit approach

| | |
| --- | --- |
| **Trigger** | `U4` utilisation ≥ 0.90 **and** a felt constraint: a denied-access event, a request the admin refused, or a written ask |
| **Qualify** | Health Secure or Watch (`R8`) · demonstrated value ≥3× the increment (`R9`) · inside 90 days of opt-out, co-term instead (`R12`) |
| **Steps** | 1. Confirm the constraint in the customer's own words. 2. Quantify the value already delivered. 3. Size the increment against the constraint, not against the list price. 4. Quote |
| **Exits** | Success: quote issued within 21d · Failure: refused → record the reason, do not re-pitch inside 90 days without new evidence |
| **The gate that matters** | Utilisation is a reason to look. Only the felt constraint is a reason to ask (`R10`) |

### `PB-L03` T-90 renewal rung

| | |
| --- | --- |
| **Trigger** | `opt_out_deadline − today` crosses 90 **and** the renewal conversation has not been held, or the paper path is unconfirmed |
| **Steps** | 1. Confirm the approval chain and signature process in writing — before the contracting phase, not during it. 2. Confirm security review, vendor onboarding and PO requirements with dates (`R7`). 3. Value recap to the economic buyer. 4. Quote |
| **Exits** | Success: approval chain confirmed in writing and a quote acknowledged · Failure: no response from the economic buyer at T-60 → escalate to VP CS |
| **Why the behavioural qualifier** | Firing on all accounts at T-90 is a calendar, and it trains the team to close the task without reading it |

### `PB-X01` Payment failure

| | |
| --- | --- |
| **Trigger** | 2 failed payment attempts, or `C10` dunning entered |
| **Steps** | 1. Automated first touch to the billing contact within 24h — facts, two resolution options, no drama. 2. Automated reminder at day 3. 3. **Human** at day 7: AM to the commercial contact. 4. Escalate to the economic buyer at day 14 |
| **Exits** | Success: payment collected · Failure: day 21 → treat as intent, not as an accident, and open a risk record |
| **Why it earns its place** | This is revenue lost to nobody's decision. It is the cheapest play in the catalogue to automate and the one most often left manual |

---

## 11. Choosing the starting set

Six to eight plays. Choose by this order, and stop when the capacity budget is full:

| Rank | Choose | Why |
| --- | --- | --- |
| 1 | The administrative plays your billing data supports (`PB-X01`, `PB-X02`) | Involuntary loss, fully automatable, no capacity cost |
| 2 | The one commercial-event play (`PB-R05`) | Lowest volume, highest precision signal class in the taxonomy |
| 3 | `PB-R02` champion continuity | Step-change risk, invisible in usage data, and the window is short |
| 4 | The lifecycle rung your team most often misses — usually `PB-L03` | Renewals lost on a technicality, with a happy customer |
| 5 | One adoption play tied to your activation event (`PB-A02`) | First-year retention lever |
| 6 | `PB-R01` or `PB-R03`, whichever your fire log says is more common | Pick one; running both at launch usually exceeds the budget |
| 7 | One expansion play, only if the health gate and value ratio can be evaluated (`R8`, `R9`) | Otherwise it fires into accounts you should not be asking |
| 8 | One advocacy play, automated (`PB-V04`) | Cheap, and it feeds Sales |

**What to leave out at launch:** everything requiring a data source at ⚠️ Partial or ❌ Missing in
the Coverage Ledger, and every play whose owner role is currently unstaffed. Both come back at the
next quarterly review with the gap named — see `governance.md` §4.
