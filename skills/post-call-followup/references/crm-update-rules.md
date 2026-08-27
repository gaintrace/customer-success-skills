# CRM and CS-Platform Update Rules

> Section B of the post-call artifact. Field names follow
> `../../cs-context/references/normalized-schema.md`; map them to your own CRM's API names in
> `.agents/cs-context.md` §9. Never "update the CRM" — emit a diff, one row per field.

**Contents**
1. [The diff discipline](#1-the-diff-discipline)
2. [The interaction record — always written](#2-the-interaction-record--always-written)
3. [Contact fields](#3-contact-fields)
4. [Opportunity fields](#4-opportunity-fields)
5. [The forecast category gate](#5-the-forecast-category-gate)
6. [Subscription and contract fields](#6-subscription-and-contract-fields)
7. [Account fields and the health band rule](#7-account-fields-and-the-health-band-rule)
8. [Downstream trigger catalogue](#8-downstream-trigger-catalogue)
9. [System of record and conflicts](#9-system-of-record-and-conflicts)
10. [What a call may never change](#10-what-a-call-may-never-change)

**Evidence convention:** `[M]` measured · `[V]` vendor-analysed · `[P]` practitioner rule of
thumb · `[D]` derived here.

---

## 1. The diff discipline

Every change is one row:

| Object.field | Old | New | Evidence | Rule permitting the change | System of record |
|---|---|---|---|---|---|
| `contact.sentiment` (c_4471) | `positive` | `neutral` | "this is the third time this year" [Fireflies · 2026-08-26 · 00:02] | §3 R2 — a stated grievance moves sentiment one band, not two | Salesforce |

Four properties this buys you that a prose summary does not:

| Property | Why it matters |
| --- | --- |
| **Auditable** | A colleague can disagree with one row instead of rejecting the whole note |
| **Reversible** | The old value is recorded, so a wrong change can be undone |
| **Attributable** | The evidence is attached to the field, not to a paragraph three screens away |
| **Rule-bound** | The permitting rule is named, so the same input produces the same change next time |

**Never write a field you did not read first.** If the old value is unknown, write
`UNKNOWN — requires <system>` in the Old column rather than assuming it was empty. Overwriting
a field somebody else set, without knowing what they set, is how account history disappears.

---

## 2. The `interaction` record — always written

One row per call, every time, even when nothing else changed. This is the table that makes
relationship analysis possible downstream, and it is the one most often skipped because the
call "wasn't important".

| Field | Rule |
| --- | --- |
| `type` | `call` · `meeting` · `qbr` · `onsite` — use the actual type, not a default |
| `direction` | `inbound` if they requested it. An inbound-requested meeting is a different signal from one you chased |
| `timestamp` | Call **end** time, in the account's timezone |
| `internal_participants` | Everyone from your side who attended, including silent attendees |
| `customer_participants` | Contact IDs, not names. This array is the multithreading measure — a call logged without it is invisible to `churn-risk` |
| `response_latency_hours` | Populated on the reply to your recap, not now. Leave null and fill on reply |
| `sentiment` | −1..1, from evidence in §3 R1, not from how the call felt |
| `commitments` | Array of `{who, what, due}` — Grade A and B only. Grade C/D never enter this array |
| `summary` | The Bottom Line block from Section A. Not the transcript |
| `source_ref` | Link to the recording or the note. Without it the quotes cannot be audited |

**No-shows are logged too**, as an interaction with the attendee list showing who was absent.
A pattern of economic-buyer no-shows is a stronger relationship signal than a pattern of
attended calls, and it is invisible if no-shows are not recorded.

---

## 3. Contact fields

| Rule | Field | Trigger | What to write |
| --- | --- | --- | --- |
| **R1** | `contact.sentiment` | Evidence in the call, not the vibe | Move **one band at a time**: `advocate` → `positive` → `neutral` → `negative` → `hostile`. One difficult call does not take an advocate to hostile. Attach the quote and the timestamp |
| **R2** | `contact.influence` (1–5) | Observed behaviour — who deferred to whom, who closed the discussion, who was asked to approve | Never from job title. A director who ends every debate outranks a VP who attends silently |
| **R3** | `contact.role` | Behaviour, not title | Use the schema enum: `economic_buyer` `champion` `coach` `admin` `power_user` `user` `blocker` `technical_evaluator` `procurement` |
| **R4** | Champion status | A champion spends their own credibility on you internally | Promote to `champion` only on a specific act: they defended the tool in the meeting, brought a colleague, pushed their own team to adopt, or took an internal action for you. Log the act |
| **R5** | Champion demotion | Three consecutive calls without them advocating, or an observed refusal to carry something internally | Demote to `coach` or `user` and say why. A stale champion flag is worse than no flag |
| **R6** | `contact.is_active` / `departed_at` | Any departure language: "my last week", "handing over", "moving teams" | Set `is_active = false` and `departed_at` on **stated** departure. On inferred departure (bounce + directory removal), state the inference rule per the evidence standard |
| **R7** | New contact | Anyone on the call who is not in the CRM | Create immediately with role, influence and sentiment. A contact created three months after their first meeting has lost three months of relationship history |
| **R8** | `email_status` | A bounce noticed while sending the recap | `hard_bounce` is the strongest single departure signal available. Set it and fire the stakeholder trigger |

**Why role changes matter more than they look.** Multithreading is strongly associated with
outcome: Gong Labs' analysis of 1.8M opportunities reports 77% of deals involving multiple
contacts, closed-won deals carrying about twice as many buyer contacts as lost ones, and a
130% higher win rate on multithreaded deals over $50K (Gong Labs, 2025 `[V]` — vendor-analysed
sales data). Contact records that are not maintained after each call make an account look
single-threaded when it is not, and multithreaded when the extra contacts left last quarter.

---

## 4. Opportunity fields

| Rule | Field | Permitted change from a call | Never |
| --- | --- | --- | --- |
| **O1** | `opportunity.stage` | Advance only when the stage's own exit criteria were met **on this call** and you can name which | Advance because the call went well |
| **O2** | `opportunity.close_date` | A renewal close date is **contract-controlled**. Change it only for: a signed contract amendment, an agreed extension, or a correction of a data error | Move it because the deal feels slower. Slipping the date instead of the category is the oldest way to hide a miss |
| **O3** | `opportunity.amount` | Change when the customer stated a different quantity, term or scope. Record the `value_delta_reason`: seat_reduction · product_removal · discount_concession · usage_true_down · price_uplift · cross_sell · seat_expansion | Carry the full contract value by default. "The default assumption is where renewal forecasts go to die" (ORM 2026 `[V]`) |
| **O4** | `opportunity.competitor` | Any competitor named by the customer, in their words | Leave blank because they "only mentioned it in passing". A named competitor is an evaluation |
| **O5** | Next step field | Always populated after a call, with a **dated** action and a named owner | "Follow up" · "Await customer" · blank |
| **O6** | `opportunity.forecast_category` | See §5 | Promote on optimism |
| **O7** | New opportunity | Open the same day on an explicit expansion ask, with the exact quote in the description | Wait for the pricing to be ready before opening it |

**The next-step field is a leading indicator.** A book of business where 30% of open renewals
have a blank or undated next step is a forecasting problem before it is a retention problem —
you cannot call a renewal you cannot describe the next action on.

---

## 5. The forecast category gate

Renewal forecast categories carry hard entry criteria. A call may move a category **only** when
every criterion of the target category is true and was evidenced on the call. The rubric below
is owned by `renewal-forecast`; it is reproduced here because the post-call moment is when
categories actually get changed.

| Category | Every criterion must be true | Who may set it |
| --- | --- | --- |
| **Commit** | 1) Economic buyer confirmed in a live conversation ≤30 days ago · 2) price, term and quantity agreed in writing · 3) order form issued or customer PO/requisition in motion · 4) no open blocker owned by the customer · 5) due date unchanged for ≥2 weeks · 6) called value equals the quoted value | CSM/AM proposes, **manager approves** |
| **Most Likely** | Renewal conversation held with the buying group · proposal delivered · value and term proposed · exactly **one** named open dependency with a dated mitigation and a named owner · usage or value evidence documented in the last 30 days | CSM/AM |
| **Best Case** | Champion confirmed and in contact ≤30 days · proposal delivered · a single **named** risk with a dated mitigation · an explicit statement of what the "break" is | CSM/AM |
| **At Risk** | A risk record exists: cause code, ARR exposure, first-detected date, owner, dated save plan, named executive sponsor of the save · a called value (full / partial / zero) | CSM/AM; VP review above the ARR threshold |

> Entry criteria adapted from ORM's published forecast-category criteria (2026) `[V]` via the
> library's renewal-forecasting reference pack. Treat as an operating convention, not a
> measured benchmark.

**Auto-demotion triggers from a call.** Any of these, observed on the call, demotes immediately:

| Observed | Effect |
| --- | --- |
| Economic buyer did not attend and has not been in a live conversation in 30 days | Commit is not available |
| The customer raised a new blocker they own | Commit → Most Likely |
| Sponsor departure stated or inferred | Commit → Most Likely or At Risk, depending on whether a replacement is named |
| Consolidation, budget cut, or "evaluating options" stated | → At Risk, with a risk record opened the same day |
| The due date moved | Category recalculated from scratch; do not carry the old one forward |

**Any demotion to At Risk carries a written explanation**, treated exactly like a sales deal
slip (ORM 2026 `[V]`). Write it in the diff row's Evidence column, not in a separate document.

**Time-to-renewal ceiling.** Outside 90 days from the renewal date, Commit is unprovable
without a signed multi-year already in place or an auto-renew past the notice window `[P]`.
A call at T-140 cannot produce a Commit no matter how well it went.

---

## 6. Subscription and contract fields

| Rule | Field | When a call changes it |
| --- | --- | --- |
| **S1** | `subscription.auto_renew` | Only on a stated intention, and only after it is confirmed in writing by the customer. A verbal "we'll probably turn that off" opens a risk record; it does not flip the field |
| **S2** | `auto_renew_changed_at` | Set whenever S1 fires. A change here is a near-certain risk signal and must be timestamped |
| **S3** | `notice_period_days` | Correct it only against the contract document, never against what someone said on a call |
| **S4** | `opt_out_deadline` | Derived: `renewal_date − notice_period_days`. Never hand-entered. If your CRM does not hold it, compute and display it anyway — it is the date that governs every renewal conversation |
| **S5** | `seats_purchased` / `usage_entitlement` | Only on a signed amendment. A discussed seat increase is an opportunity, not an entitlement change |
| **S6** | `discount_expires` | Surface it, do not change it. An expiring discount is a renewal conversation whether or not you raise it |

**The opt-out deadline is the operative date.** A customer with a 60-day notice period on a
31 January renewal decides in November. Recording "renewal 31 Jan" and working backwards from
January means the decision is made before your first renewal conversation. Every date in
Section B works backwards from `opt_out_deadline`, not from `renewal_date`.

---

## 7. Account fields and the health band rule

| Rule | Field | Permitted from a call |
| --- | --- | --- |
| **A1** | Health band / score | **A call does not move a health band.** It moves the band's *inputs* — `contact.sentiment`, `contact.is_active`, `opportunity.competitor`, the interaction record. Let the model recompute |
| **A2** | Exceptions to A1 | Two only: a confirmed economic-buyer departure, and a stated commercial decision (non-renewal, consolidation, budget removal). Both are override floors in `churn-risk`, not score adjustments |
| **A3** | `account.status` | `at_risk` on an opened risk record; `churned` only on written notice, never on a verbal signal |
| **A4** | `account.owner_csm` / `owner_am` | Only on an actual ownership change, and the outgoing owner writes the handover note before the field changes |
| **A5** | Firmographic fields | Update on stated changes — funding, acquisition, headcount, reorg — with the quote as evidence |

**Why A1 exists.** A health score that moves after every call is measuring the CSM's mood, not
the account. It then fails to predict anything, everyone stops trusting it, and the team goes
back to gut feel. A health score reads trajectory, not a single absolute `[P]`; one
conversation is one point, not a trajectory. Log the inputs and let the model do its job.

---

## 8. Downstream trigger catalogue

| # | Observed on the call | Fires | Owner | Due | Success measure |
|---|---|---|---|---|---|
| T1 | Competitor named, or an evaluation described | `churn-risk` re-score + shadow-evaluation play | CSM | 2 business days | Risk band re-issued; competitor recorded on the opportunity |
| T2 | Economic buyer departed or replaced | `stakeholder-map` refresh + 30-day new-sponsor plan | CSM + AM | 5 business days | New sponsor named and a first meeting booked |
| T3 | Consolidation, budget cut, or headcount freeze stated | `save-play` + forecast review | AM | Same day | Risk record open with a dated save plan and an exec sponsor |
| T4 | Notice period, termination or auto-renew language raised | Escalation to the renewal owner; forecast category review | Renewal owner | Same day | Category re-set against §5 criteria with a written explanation |
| T5 | Explicit ask for seats, a gated feature, or a new product | Open `opportunity` type `expansion` with the exact quote | AM | Same day | Opportunity open with amount and close date |
| T6 | New use case or new team described | `expansion-finder` sizing pass | CSM | 5 business days | Sized opportunity or a written "not now" with the reason |
| T7 | Unresolved P1, SLA breach, or a broken commitment surfaced | Escalation record + named executive sponsor | Support lead | 4 hours | Customer has a dated fix plan in writing |
| T8 | Zero commitments obtained | Relationship & engagement signal update; one dated ask | CSM | 3 business days | A reply, or entry at §5 step 4 of `commitment-extraction.md` |
| T9 | Advocacy offered — reference, review, case study | Advocacy record. **Never raise expansion in the same thread** | CSM | 5 business days | Advocacy logged; expansion, if any, opened in a separate conversation |
| T10 | Success-plan milestone confirmed complete or missed | Milestone update; if missed, a dated recovery step | CSM | 2 business days | Milestone state and next date recorded |

**One owner per trigger.** A trigger routed to a team is a trigger nobody owns — everyone
assumes someone else will pick it up `[P]`. Where two people are genuinely needed, name one as
owner and the other as consulted.

**Tier the output.** Not everything is urgent. Sort the triggers you fire into *act today*,
*this week*, and *information only* `[P]` — a post-call update that produces nine same-day
alerts produces none.

---

## 9. System of record and conflicts

| Data | System of record | If the call contradicts it |
| --- | --- | --- |
| Contract terms, dates, notice period | The signed contract | The contract wins. Log the discrepancy — a customer who believes different terms is a renewal problem forming |
| ARR and invoicing | Billing system | Billing wins. Log what they believe they are paying |
| Seats provisioned | Product | Product wins for provisioned; CRM for purchased. Report both |
| Contact roles and sentiment | CRM, updated from calls | The call wins — this is the one place the conversation is the source |
| Support state | Ticketing | Ticketing wins. If they describe an issue with no ticket, open one |
| Health score | CS platform | The model wins. Log inputs, not conclusions |

**Never resolve a conflict silently.** Write both values and which one you acted on. A customer
who thinks their renewal is in March when the contract says January is a live problem, and it
disappears the moment you "correct" it in your own notes without telling anyone.

---

## 10. What a call may never change

| Never | Why | Do instead |
| --- | --- | --- |
| Health score, directly | It becomes a mood ring and stops predicting | Update the inputs |
| Renewal close date, without a contract event | Hides a miss | Move the category with a written explanation |
| `churned` status on a verbal signal | Churn is a written event | Open a risk record; set `churned` on notice |
| Contract terms from memory | Contract disputes start here | Read the document |
| ARR, from a verbal statement | Billing is the record | Log the belief, escalate the gap |
| A commitment they did not make | Fabrication under the evidence standard | Grade it; C and D never become commitments |
| A date engineering did not agree to | Breaks trust with technical buyers permanently | `UNKNOWN — date owed by <our date>` |
| Deleting an old note that turned out wrong | Destroys the audit trail the postmortem needs | Append a correction with today's date |
