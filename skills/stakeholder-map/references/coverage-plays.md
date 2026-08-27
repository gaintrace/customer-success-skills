# Coverage Plays

> A gap analysis that ends in "we should get to know more people there" is not a plan. Every
> gap in this file resolves to a named person to meet, a reason they would take the meeting,
> an owner, a date, and an observable outcome that tells you it worked.
>
> The organising question for all of it: *if the person we speak to most stopped answering
> tomorrow, what would still be true?*

**Contents**
- [1. The gap catalogue](#1-the-gap-catalogue)
- [2. Sourcing a second contact from data](#2-sourcing-a-second-contact-from-data)
- [3. The reason-to-meet library](#3-the-reason-to-meet-library)
- [4. Blockers and detractors — convert, contain, bypass](#4-blockers-and-detractors--convert-contain-bypass)
  — [4.0 The output contract](#40-the-output-contract) · [4.1 The three dispositions](#41-the-three-dispositions)
- [5. The new-stakeholder onboarding play](#5-the-new-stakeholder-onboarding-play)
- [6. The executive sponsor programme](#6-the-executive-sponsor-programme)
- [7. Coverage cadence by segment](#7-coverage-cadence-by-segment)
- [8. Measuring whether any of this worked](#8-measuring-whether-any-of-this-worked)
- [9. Anti-patterns](#9-anti-patterns)

---

## 1. The gap catalogue

Nine gaps. Each row is a plan; the SKILL's output table takes the action, owner, date,
expected effect and success measure straight from here.

### 1.1 No economic buyer identified

| | |
| --- | --- |
| **Detection** | `economic_buyer` unfilled, or filled at `asserted` only |
| **Why it costs money** | The renewal has no owner on their side. Procurement fills the vacuum, and procurement optimises price |
| **Action** | Ask the champion for the introduction. This is simultaneously the champion test — refusal reclassifies them as a coach and creates a second, larger finding |
| **If refused** | Route through the executive sponsor programme (§6): our exec to their most senior known contact, with a business-outcome briefing |
| **Expected effect** | A named person with budget authority, at `evidenced` or better, before the opt-out deadline |
| **Success measure** | The buyer attends one meeting and states an objective in their own words |
| **Timebox** | 30 days, or 90 days before the opt-out deadline — whichever is sooner |

### 1.2 Economic buyer identified but never met

| | |
| --- | --- |
| **Detection** | `economic_buyer` filled, `last_two_way_contact` > 180d or null |
| **Why it costs money** | At renewal, someone who has never spoken to us approves a number they no longer experience |
| **Action** | Exec-to-exec, one page, outcomes and money, the ask in the first paragraph. Not a product update and not a QBR invitation |
| **Expected effect** | A live relationship at the level that signs |
| **Success measure** | Meeting held; a stated objective recorded; a repeat cadence agreed |
| **Timebox** | 45 days |

### 1.3 Single-threaded (depth 1)

| | |
| --- | --- |
| **Detection** | One contact with a two-way interaction in 90 days |
| **Why it costs money** | Price it — `ARR × p_departure × 0.51 × 1.00`. On a $300k account with a moderate champion-risk score that is roughly **~$46k** of priced dependency, all of it closable. `R5` additionally flags the full ARR at-risk to `churn-risk` |
| **Action** | Two named second contacts, sourced from §2, each with a reason from §3 |
| **Expected effect** | Depth ≥ the band target within one quarter |
| **Success measure** | Two contacts with a two-way interaction inside 60 days, in at least two functions |
| **Timebox** | 60 days |
| **Note** | Depth 1 is severe on every account, at every ARR band. It is the only structural gap that justifies interrupting an otherwise healthy account's cadence |

### 1.4 Breadth 1 — one function only

| | |
| --- | --- |
| **Detection** | All two-way contacts sit in one function |
| **Why it costs money** | Adoption is trapped in one team, so the value story has exactly one constituency at renewal. Win rates rise materially with the number of departments engaged — roughly 28% at one department, 39% at two, 44% at three or more (Outreach, vendor analysis of its own customers' deal data, methodology unpublished) `[V]` |
| **Action** | Find the adjacent function already present in usage data and give it its own success measure, not a copy of the first team's |
| **Expected effect** | A second constituency with its own reason to renew |
| **Success measure** | A named contact in a second function with two-way contact and one measurable objective |
| **Timebox** | One quarter |

### 1.5 Height gap — no director-or-above contact

| | |
| --- | --- |
| **Detection** | `multithread_height` below the ARR band's floor, with a renewal inside 180 days |
| **Why it costs money** | The conversation is happening two levels below where the decision is made |
| **Action** | Use the champion's own agenda: offer their leadership a briefing on the outcome *they* are being measured on, with the champion in the room. Never go over a champion's head without them |
| **Expected effect** | A relationship at the level where the budget conversation happens |
| **Success measure** | One meeting at Director+ with the champion present, before the opt-out deadline |
| **Timebox** | 60 days |

### 1.6 No executive sponsor on our side

| | |
| --- | --- |
| **Detection** | `account.exec_sponsor_internal` unfilled on an account above the segment threshold |
| **Why it costs money** | There is no path for their exec to talk to a peer, so every escalation arrives at a CSM who cannot authorise the answer. PMI's Pulse research found organisations where >80% of projects had actively engaged executive sponsors reported 76% success against 46% where fewer than half did `[A]` |
| **Action** | Assign one, with a scheduled cadence, per §6 |
| **Success measure** | Named in the CRM, first meeting held, next one booked |
| **Timebox** | 30 days |

### 1.7 Unmodelled blocker or detractor

| | |
| --- | --- |
| **Detection** | A contact with negative or hostile sentiment, or a rejected request they raised, and no strategy recorded |
| **Why it costs money** | Opposition surfaces at the renewal, when there is no time to answer it |
| **Action** | Choose convert, contain or bypass deliberately (§4) and record the choice with its risk. Inside the renewal window `UNKNOWN` is not an option: write the test, the owner and the date instead (§4.0) |
| **Success measure** | The objection is answered in writing and the answer is acknowledged |
| **Timebox** | 30 days |

### 1.10 Champion slot held only by a supporter

| | |
| --- | --- |
| **Detection** | The warmest contact scores `mobilising_capacity` ≤ 1 on `role-taxonomy.md` §3A, so the `champion` slot of `coverage_score` reads 0.0 while sentiment reads positive |
| **Why it costs money** | The renewal is being planned around someone who cannot convene the meeting where it is decided. This is the failure that looks healthiest right up to the day it does not |
| **Action** | Run M1–M3 on the two highest-influence contacts already in the data, and recruit from whoever scores ≥ 2 — never by promoting the supporter. Use the supporter to make the introduction; that is what they are good at |
| **Expected effect** | A champion slot filled by someone with a named instance of moving a decision through that org |
| **Success measure** | One contact at M ≥ 2 with a two-way interaction and one observed advocacy event inside 90 days |
| **Timebox** | 60 days, or before the opt-out deadline if that is sooner |

### 1.8 Key role at `asserted` confidence only

| | |
| --- | --- |
| **Detection** | `role_confidence = asserted` on any of the four key roles |
| **Why it costs money** | A forecast resting on a job title |
| **Action** | Put confirmation on the next call agenda; use the §8 confirmation questions in `org-inference.md` |
| **Success measure** | The role moves to `evidenced` or `verified`, or is corrected |
| **Timebox** | Next scheduled interaction |

### 1.9 Role concentration — one person holds three or more roles

| | |
| --- | --- |
| **Detection** | Same `contact_id` labelled buyer + champion + admin |
| **Why it costs money** | Departure is an extinction event for the relationship, not a setback |
| **Action** | Split the roles deliberately: recruit an operating champion one level down and a business-side second contact in a different function |
| **Success measure** | At least two of the three roles held by different people, both with two-way contact |
| **Timebox** | One quarter |

## 2. Sourcing a second contact from data

Never ask the champion "who else should I talk to?" as your opening move — it makes your
coverage problem their homework. Arrive with a name.

| Source | Query | Why they will answer |
| --- | --- | --- |
| Ticket submitters | `ticket.contact_id` over 180d, excluding the champion, ranked by volume | They have an open problem and we have information about it |
| Reopeners | `ticket.reopened_count > 0` | The friction landed on them personally; they want it fixed |
| Rollout owners | Whoever invited the most users | They own an internal rollout that is being judged |
| Power users | Top-decile `core_actions` in their cohort | They want capability we have and they have not found |
| Newly active users | First `usage_event` in the last 60 days | Genuinely new; enablement is welcome rather than intrusive |
| Newly *inactive* users | Active in the prior 90d, zero in the last 30d | Something blocked them, and asking what is a real question |
| Meeting delegates | Anyone who attended in the champion's place | Already briefed, already interested |
| Survey respondents | Anyone who left free text | They took the trouble to write; the reply is owed |
| The paper chain | Signatory, notices contact, procurement | You need them at renewal anyway; meet them when nothing is at stake |
| The adjacent function | The function with usage and no relationship | The most valuable and the most often missed |

**The rule of two.** Close a depth gap with **two** contacts, not one. One replacement
recreates the single-threaded state at a different name.

## 3. The reason-to-meet library

A second contact accepts a meeting when there is something in it for them. Specificity is the
whole play; a generic invitation is declined and then remembered as an interruption.

| Contact type | The reason | The form |
| --- | --- | --- |
| Ticket submitter | The pattern behind their tickets, and the fix or workaround | 20 minutes, we bring the analysis |
| Reopener | An owner and a date on the thing that keeps coming back | Named engineer, weekly closure updates |
| Rollout owner | Adoption by team, benchmarked against their own earlier cohorts | A one-page read they can forward |
| Power user | The capability they have not found, or early access | A working session, not a demo |
| Newly inactive user | "Your team's usage of the approvals workflow stopped in July after running steady since March — did something change your end?" | One question, easy to answer |
| Adjacent function lead | What the first team achieved, expressed in their function's terms | 20 minutes with the champion in the room |
| Procurement | The renewal shape, early, with the approval path mapped | Process conversation, no pressure |
| Their executive | The outcome they are measured on, quantified against their own baseline | One page, exec-to-exec |

**The test for every one of these:** could this invitation have gone to any of forty
customers? If yes, rewrite it. See `../../cs-context/references/customer-voice.md`.

## 4. Blockers and detractors — convert, contain, bypass

Pick one strategy deliberately and record it. Drifting between all three is how an
under-modelled objection becomes the reason a renewal is lost.

### 4.0 The output contract

The Blockers table is generated **before** the coverage plan, because a plan written first will
route around the detractor rather than resolve them, and the routing is what fails at the
approval step. Four rules govern what may be emitted:

| Rule | Enforcement |
| --- | --- |
| **Every negative or hostile contact gets a row** | Sweep `contact.sentiment ∈ {negative, hostile}`, on-record objections, and rejected requests the person raised. Nothing found prints as `Checked and clear — no contact carries an objection on record`, never as a missing section |
| **Disposition is one of three literal values** | `convert` · `contain` · `bypass`. There is no fourth valid value. A row without one is not valid output |
| **The risk of the chosen disposition is a required cell** | Taken from the table in §4.1 — the row states the cost of the choice that was made, not the cost of the objection |
| **`UNKNOWN` is prohibited inside the renewal window** | Opt-out deadline ≤120 days (`R1`). The cell instead reads `TEST — <the specific thing that must be found out>`, carries an owner and a date, and appears again as a dated action in the coverage plan. Outside the window `UNKNOWN` survives one cycle, with a printed revisit date |

**Why the prohibition is absolute inside the window.** An unknown disposition is not a neutral
state; it is a decision to do nothing, taken silently, on the one stakeholder who is actively
working against the renewal. The window is exactly when there is no longer time to discover the
objection by accident. What the map owes the reader in that situation is not a strategy it cannot
justify — it is the specific question, the person who will ask it, and the date they will ask it
by. `"Unknown — Priya asks Marcus on 12 Sept what Rae actually objected to in the March review"`
is a plan. `"Unknown"` is an omission with a heading.

**Choosing when the evidence is thin.** Default to `contain` — it is the only one of the three
that is reversible. `convert` commits you to a slow public attempt, and `bypass` is irreversible
the moment they notice.

### 4.1 The three dispositions

| | **Convert** | **Contain** | **Bypass** |
| --- | --- | --- | --- |
| **Use when** | The objection is specific, addressable, and about our product rather than their position | The objection is real but narrow, and the person has no veto over the whole relationship | They have no veto and no budget authority, and the economic buyer is engaged and aware |
| **The move** | Answer the specific objection in writing, with evidence, and invite them to test it | Scope it: acknowledge it, put it in writing with an owner and a date, and keep it out of the renewal conversation | Build the case with the buyer directly, with the blocker informed rather than consulted |
| **Time** | 30–90 days | Immediate, then maintained | Immediate |
| **The risk** | Slow; a failed convert hardens the position publicly and gives it an audience | It buys time rather than resolving; they can raise it later with allies | **The most dangerous option.** A bypassed blocker who later acquires authority becomes the reason you lose, and the bypass itself becomes their argument |
| **Never use when** | The objection is really about budget, status or a competing internal project | The objection touches security, legal, or data processing | They hold **any** veto — security, legal, procurement or technical sign-off |
| **How you know it failed** | They repeat the objection to someone new, unchanged | It appears in a renewal thread you were not on | They are promoted, or the buyer forwards them the proposal |

**The one rule with no exceptions:** never bypass a veto-holder. Consult the veto map in
`role-taxonomy.md` §7 before choosing.

**Converting well.** Detractors convert on being taken seriously, not on being persuaded. The
sequence that works: reflect their objection back in their own words before responding at all;
concede the parts that are true; answer the rest with specifics and dates; then ask them what
would change their mind. A detractor who is converted becomes a disproportionately strong
champion, because their advocacy carries the credibility of someone who was against you.

## 5. The new-stakeholder onboarding play

A new stakeholder arrives with none of the history and all of the authority. The default
outcome is that they re-evaluate a decision they did not make, and the default vendor
behaviour — sending them the existing success plan — makes it worse.

| Day | Action | Owner | Exit criteria |
| --- | --- | --- | --- |
| 0–2 | Detect and record: new name on threads, in product, or on the calendar. Add the contact with `role_confidence = asserted` and a dated note | CSM | Contact created |
| 0–2 | Find out what they inherited and from whom. Their predecessor's role, open commitments, unresolved friction | CSM | A one-page inheritance brief |
| 3–5 | Introduction, from a human, with something attached: the account's current state in one page, written for someone with zero context | CSM | Meeting requested |
| 5–10 | First meeting. **Ask, do not present.** What are they measured on, what did they inherit, what do they want changed. Their objectives may be entirely different from their predecessor's | CSM | They state an objective in their own words |
| 10–15 | Re-baseline the success plan around what they said, with a measure and a date. Show what has already been achieved — but framed as their team's achievement, not our delivery | CSM | Plan agreed, not merely sent |
| 15–20 | Introduce the rest of our team by name and role, so escalation has a face before it is needed | CSM | Named contacts exchanged |
| 20–30 | If they are senior enough, an executive touch from our side | Exec sponsor | Meeting held |
| 30 | Re-score their role at `evidenced`, update influence and sentiment, re-run the map | CSM | Map updated with dates |

**What not to do.** Do not send the previous stakeholder's QBR deck. Do not open with a
renewal ask. Do not describe the relationship's history as a list of things we delivered — a
new stakeholder hears that as an invoice. Do not assume they inherited goodwill; assume they
inherited a line item and a set of open questions.

**The one question that does the most work:** *"What did you inherit here that you'd change if
you could?"* It surfaces the unspoken objection, the predecessor's unfinished business, and
their own agenda in a single answer.

## 6. The executive sponsor programme

An executive sponsor programme is the assignment of our own executives to named accounts with
a scheduled cadence — not a phone number to call when something breaks. The failure mode is an
executive relationship that exists only during crises, which trains the customer to escalate
in order to be heard.

| Element | Design | Failure if skipped |
| --- | --- | --- |
| **Eligibility** | A stated ARR or strategic threshold, published internally | Sponsorship allocated by whoever asks loudest |
| **Assignment** | Named executive per account, recorded in `account.exec_sponsor_internal` | "The VP is across it" — nobody is |
| **Cadence** | Scheduled, minimum twice a year, plus on any change event | Contact only during escalations |
| **Preparation** | The exec reads a one-page brief before every touch: outcomes, money, the ask, the two things not to say | An exec touch that damages credibility is worse than none |
| **Content** | Business outcomes and the customer's own metrics. Never a product update, never a status recap | The meeting is remembered as a waste of a senior person's time |
| **Their counterpart** | Named, at an equivalent band. A VP sponsor with a manager counterpart is a mismatch that reads as a downgrade | Sponsorship with nobody to sponsor |
| **Measurement** | Renewal and expansion rates on sponsored accounts vs comparable unsponsored ones, plus meetings held against meetings scheduled | An unmeasured programme is quietly abandoned within two quarters |
| **Exit** | An account leaves the programme deliberately, with the relationship handed back | Sponsors accumulate accounts until the cadence becomes fictional |

**Sizing.** Cap sponsored accounts per executive at a number the cadence can actually support —
if each account needs two prepared meetings a year plus event-driven touches, an executive with
twenty sponsored accounts is committing to more than forty prepared conversations a year on top
of their day job. Set the cap from the arithmetic, then publish it.

**Triggering an exec touch outside the cadence:** an economic-buyer change, a champion
departure at an account above the threshold, a P1 with executive visibility, an opt-out
deadline inside 90 days with no renewal conversation held, or a coverage score below the band
floor. All five are events, not judgements, so the trigger can be automated.

## 7. Coverage cadence by segment

Maintenance is what separates a map from an archaeology project. Roughly 20–30% of B2B
contacts change job in a year (UserGems, 2026) `[V]`, so an unmaintained map loses about a
fifth of its accuracy annually — and the losses are not random. They concentrate in the senior
roles you rely on most.

| Segment | Full re-map | Coverage check | Champion risk check | Trigger events that override the cadence |
| --- | --- | --- | --- | --- |
| Strategic / top ARR band | Quarterly | Monthly | Weekly | Any of the five in §6 |
| Enterprise | Quarterly | Monthly | Monthly | Departure signal, exec change, opt-out inside 90d |
| Mid-market | Twice a year | Quarterly | Quarterly | Departure signal, opt-out inside 60d |
| SMB / pooled | Annually, or at renewal | At renewal | Automated flag only | Hard bounce on the only contact |

**Gate onboarding on it.** A minimum contact count should be a gate on marking onboarding
complete — a practice Emilia D'Anzica argues for directly `[P]`. An account that reaches
steady state single-threaded will still be single-threaded at its first renewal, because
nothing in the steady-state cadence creates a reason to meet anyone new.

## 8. Measuring whether any of this worked

Coverage work is easy to perform and hard to evidence, which is why it is the first thing cut
under pressure. Measure it at the portfolio level, in these terms:

| Metric | Computation | Useful target |
| --- | --- | --- |
| Single-threaded accounts | Accounts at depth ≤1 ÷ accounts in the tier | Trending to zero above the mid-market threshold |
| Single-thread exposure | Σ departure exposure at current depth, across the book | Falls quarter on quarter |
| Closable exposure | Σ (exposure at current depth − exposure at target depth) | The size of the prize; report it next to the work |
| Coverage score distribution | Accounts at ≥3/4 ÷ accounts in the tier | ≥80% for the strategic tier |
| Key-role verification rate | Key roles at `verified` ÷ key roles filled | Rising; it is the honesty metric |
| Exec sponsor cadence adherence | Sponsored meetings held ÷ scheduled | ≥90%, or the programme is fictional |
| Time-to-successor | Median days from departure detection to a named successor meeting | ≤21 days |
| Map staleness | Median days since last contact-level update | Under the segment's cadence |

Report **closable exposure** alongside the work, always. It converts "we need to meet more
people" into a dollar figure with a plan attached, which is the only form in which coverage
work survives a quota conversation.

## 9. Anti-patterns

| Anti-pattern | Correction |
| --- | --- |
| "Multi-thread the account" as an action item | Two named people, sourced from data, each with a specific reason to meet and a date |
| Asking the champion to do your coverage homework | Arrive with a name and a reason; ask them to make the introduction, not to build the list |
| Closing a depth gap with one new contact | The rule of two — one replacement recreates the single-threaded state |
| Going over a champion's head to reach their exec | Take the champion into the room; their agenda is the reason the meeting happens |
| Bypassing a blocker with a security or legal veto | Never bypass a veto. Convert or contain, and record which you chose and its risk |
| An exec sponsor programme with no cadence | Scheduled touches, a prepared brief, and a measured adherence rate |
| An exec touch that is a product update | Business outcomes, their metrics, the ask in the first paragraph |
| Sending a new stakeholder the previous one's success plan | Ask what they inherited and what they would change; re-baseline on their answer |
| Treating a coverage gap as a soft finding | Price it. Closable exposure in dollars, next to the plan |
| Re-mapping only when something breaks | Cadence by segment, plus event triggers that override it |
| Reporting coverage as a count of contacts | Depth, breadth, height and the four-role coverage score — counts are gameable, structure is not |
