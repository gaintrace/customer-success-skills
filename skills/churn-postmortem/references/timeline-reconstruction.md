# Timeline Reconstruction

> A post-mortem without a dated timeline is a memory test, and the people being tested are the
> ones with the most to lose from the answer. This file is the extraction procedure: what to pull
> from each system, the shape every event takes, how to date a decision nobody wrote down, and
> the retention traps that quietly delete the evidence before you go looking for it.

**Contents**
- [1. What the timeline is for](#1-what-the-timeline-is-for)
- [2. The window and the T-notation](#2-the-window-and-the-t-notation)
- [3. The event grammar](#3-the-event-grammar)
- [4. Extraction, source by source](#4-extraction-source-by-source)
- [5. The retention trap](#5-the-retention-trap)
- [6. Dating the undateable](#6-dating-the-undateable)
- [7. Known at the time vs known only now](#7-known-at-the-time-vs-known-only-now)
- [8. When there is no data — reconstructing from people](#8-when-there-is-no-data--reconstructing-from-people)
- [9. Reconstruction errors](#9-reconstruction-errors)
- [10. A worked fragment](#10-a-worked-fragment)

---

## 1. What the timeline is for

Three jobs, in this order. Everything that serves none of them is decoration.

| Job | The question it answers | The output it feeds |
| --- | --- | --- |
| **Locate the decision** | When did they actually decide? | `decision_date`, and therefore the label on the whole record |
| **Locate the first visible risk** | What is the earliest date a reasonable observer using only data available then could have called it? | `earliest_detectable_date`, and therefore the detection lag |
| **Establish the causal order** | What came first — the ticket cluster or the usage decline? The departure or the disengagement? | The five-whys chain, and which reason is primary |

A chronology answers none of these. A chronology is every event in date order; a timeline is
every event in date order **with an evidence tier, a source, and a known-at-the-time flag**, which
is what makes the three jobs possible.

## 2. The window and the T-notation

`T` is the **decision date**, not the churn date. Days are written as `T−N`.

| Window | Use | Why |
| --- | --- | --- |
| **T−540 → T−0** | Default, enterprise annual contracts | Covers the previous renewal cycle, so you can see whether the loss began at the *last* renewal |
| T−365 → T−0 | Mid-market, or where history is thin | One full cycle |
| T−180 → T−0 | Monthly/PLG contracts | Beyond this the population has turned over |
| T−0 → effective date | Always, as a tail | The save window, and what we did with it |

Extending backwards is cheap and frequently decisive: `sponsor-loss` and `lack-of-adoption`
losses commonly originate before the previous renewal, and a 90-day window finds the symptom
every time and the origin never.

## 3. The event grammar

Every row, in every family, takes the same seven fields. Uniformity is what lets a quarter of
timelines be aggregated rather than read one by one.

| Field | Rule |
| --- | --- |
| `day` | `T−N`, computed from `decision_date` |
| `date` | ISO date. A month with no day is written `2026-05` and flagged imprecise |
| `family` | One of the seven, never blank |
| `event` | One clause, past tense, factual. No adjectives, no interpretation |
| `evidence` | `[system · object/field · date or window]` per `../../cs-context/references/evidence-standard.md` §2 |
| `tier` | `Observed` or `Inferred`. Inferred rows carry the rule inline |
| `known_then` | `Yes` if the fact was visible to us on the day it happened; `No` if we learned it afterwards |

**Interpretation lives outside the table.** "Usage fell 62%" is an event; "they had checked out"
is an interpretation and belongs in the five whys, where it can be argued with.

## 4. Extraction, source by source

Walk all seven families. Print families where nothing was retained as "checked, no history
retained" — an empty family is a coverage finding, not an absence of events. Field names below
follow `../../cs-context/references/normalized-schema.md`; system-specific objects are in
`../../cs-context/references/data-source-map.md`.

### Product usage & adoption

| Pull | From | Watch for |
| --- | --- | --- |
| `usage_daily.core_actions`, `active_users`, `sessions` weekly series over the full window | Product analytics | The **inflection**, not the level. Note the week the slope turned, not the week it hit zero |
| The same series **segmented by the department named on the contract** | Product analytics group/department property | Buyer disconnect: aggregate flat while the buying team goes to zero. This is invisible in the account roll-up |
| `feature_breadth` quarter over quarter | Product analytics | Breadth collapse usually precedes depth collapse by a quarter |
| Activation event: did it ever fire, and when did it last fire | Product analytics + the definition in `cs-context` §5 | A `lack-of-adoption` loss is proven here or not at all |
| Seat utilisation `distinct_active_users_30d / seats_purchased`, monthly | Product + `subscription.seats_purchased` | Ramp deals and phased rollouts look identical to decay for the first 180 days |
| `user_deactivated_at` bursts | Identity / SCIM | Deprovisioning that matches their headcount news is `budget-loss`; deprovisioning that does not is churn in progress |

### Commercial & contract

| Pull | From | Watch for |
| --- | --- | --- |
| `subscription.auto_renew_changed_at`, and **who** changed it | CRM/CLM field history | Our own re-papering flips this flag too. Verify the actor before treating it as a decision |
| `renewal_date`, `notice_period_days`, computed `opt_out_deadline` | CRM / the signed contract | Verify the notice period against the **signed MSA**, not the CRM field. This field is wrong often enough to change the answer |
| Seat and ARR changes at each prior renewal | Subscription history | Two consecutive reductions is a contraction spiral that was already running |
| `opportunity.stage_changed_at` history, `loss_reason` | CRM | The stage history dates the internal recognition, which is usually `first_flagged_date` |
| Procurement, legal and termination-terms contacts | Email, tickets, CLM clause lookups | R11/R12 are near-certain and precisely dated. They are the best `decision_date` inference available |

### Relationship & engagement

| Pull | From | Watch for |
| --- | --- | --- |
| `contact` roster snapshots: `departed_at`, `email_status`, title changes | CRM + enrichment | A hard bounce is not a departure until you rule out a domain migration. Check whether other contacts at the domain bounced the same week |
| Multithreading depth by month: distinct `customer_participants` in the trailing 90 days | `interaction` | Plot it. A depth that fell to 1 and stayed there is a structural fact with a date |
| Buyer-side engagement: interactions including an `economic_buyer` or `champion` | `interaction` | The month buyer-side contact stopped is often the true start of the loss |
| Meeting acceptance, no-shows, reschedules | Calendar | Two consecutive cancellations is a dated event, not a scheduling annoyance |
| `response_latency_hours` trend | Email | Compute per contact. An account average hides one person going quiet |
| CSM changes **on our side** | CS platform owner history | Vendor-caused discontinuity shows up later as "customer disengagement" and is our event, not theirs |

### Support & reliability

| Pull | From | Watch for |
| --- | --- | --- |
| Every ticket in the window with `created_at`, `priority`, `resolved_at`, `reopened_count` | Support system | Cluster by root cause, not by date. Repeat issues matter more than volume |
| P1s and escalations with age and executive visibility | Support + escalation records | The date an escalation was opened, and the date it stopped being discussed without being closed |
| The **silence after the spike** | Derived | Ticket volume falling to zero within 30 days of an unresolved cluster is a dated event and a strong one |
| Linked engineering issues and their committed dates | Jira/Linear | A missed commitment date is an event on our side (`R19`) |
| Incidents touching this account | Status/incident system | Blast radius specific to them, not the global incident |

### Sentiment & VoC

| Pull | From | Watch for |
| --- | --- | --- |
| Every survey response **with the respondent's role and date** | Survey tool | A promoter score from someone who is not the buyer is not account sentiment |
| Transcript sentiment and risk phrases by call | Conversation intelligence | The first call where a forward-looking question got a non-answer |
| The sentence where someone first said the quiet thing | Transcripts, email | Quote it verbatim with its date. It is frequently the single most useful row in the table |

### Billing & payment

| Pull | From | Watch for |
| --- | --- | --- |
| Invoice history: `issued_at`, `due_at`, `paid_at`, status | Billing | Days-late against **their own** history, not an absolute threshold |
| `payment_failures`, `payment_method_status` | Billing | Rule out involuntary before writing any narrative |
| Disputes and credits | Billing + CRM | A credit issued without a fix is a dated event in the trust story |

### Firmographic & external

| Pull | From | Watch for |
| --- | --- | --- |
| M&A, funding, layoffs, leadership changes | News/enrichment, their own site and filings | Date the *announcement*, and separately the date **we** learned it. The gap is a coverage finding |
| Headcount trend | Enrichment | A shrinking company deprovisioning seats is not disengagement |
| Their public roadmap or platform standardisation announcements | Their site, job postings | An in-house build is usually visible in job postings months before it is mentioned to us |

## 5. The retention trap

The commonest reason a post-mortem cannot be done is that the evidence was deleted between the
churn and the review. Offboarding is designed to delete data; loss review needs it.

| System class | What typically disappears | When | Countermeasure |
| --- | --- | --- | --- |
| Product analytics | Event history for deleted/deprovisioned orgs; group properties needed for department segmentation | On deprovisioning, or at the plan's retention horizon | Export the weekly series and the segmented series **before** offboarding |
| Identity / SSO | User records, deactivation timestamps | On tenant deletion | Snapshot the roster and `user_deactivated_at` |
| Support | Org mapping for tickets, so tickets orphan even when they survive | On org merge/delete | Export tickets with `organization_id` resolved |
| Email / calendar | Ex-employee mailboxes on both sides | On staff departure | Export threads for the account, not the mailbox |
| CRM | Field *history* (auto-renew changes, stage changes) ages out before records do | Per field-history retention | Pull field history early; it is the least recoverable and the most probative |
| Conversation intelligence | Recordings and transcripts at the retention horizon | Policy-dependent | Export transcripts for the last four calls |

**The pre-export checklist**, run on the day a loss is confirmed and before any offboarding task:
weekly usage series (aggregate and segmented) · activation event history · seat and user roster
with deactivation dates · full ticket export with org resolved · CRM field history for contract
and opportunity objects · invoice history · survey responses with respondent roles · transcripts
for the last four calls · the shared-channel history. Ten minutes then; unrecoverable later.

## 6. Dating the undateable

`decision_date` is rarely recorded. Infer it, state the rule, and label it Inferred. Use the
**earliest** signal that qualifies — the decision precedes its administration.

| Basis | Signal | Precision | Notes |
| --- | --- | --- | --- |
| `inferred_autorenew` | Customer switched auto-renew off `[C1]` | High | Verify the actor. Our own re-papering produces the same field change |
| `inferred_termination_request` | Termination terms, notice period, data return or transition assistance requested `[R12]` | High | Procurement does not ask speculatively |
| `inferred_competitor_named` | A competitor named by an economic buyer `[R13]` | Medium | Names the evaluation, not necessarily the decision. Use only when nothing stronger exists |
| `inferred_procurement` | Procurement re-engaged outside the renewal window `[R11]` | Medium | Disambiguate: a security questionnaire is a review; termination-clause questions are a decision |
| `inferred_export` | Bulk export or full API extraction by an admin `[T6]` | Medium–High | Rule out scheduled jobs, audit season and a warehouse build |
| `proxy_notice_date` | Formal notice, or the opportunity moved to Closed Lost | Certain but late | The fallback. Caps confidence at Medium and understates every lag |

**The interview is the tiebreaker.** "When did you personally know this was probably not going to
continue?" produces a date more often than "why did you leave" produces a cause. Record their
answer as a separate `decision_date_stated` and note any gap from the inferred date — a customer
who says June against an inferred August tells you the administration lagged the decision by two
months, which is exactly the gap the save window lives in.

## 7. Known at the time vs known only now

Every row carries this flag, and it is the difference between analysis and hindsight theatre.

| Case | `known_then` | Why it matters |
| --- | --- | --- |
| Usage decline visible in the dashboard that week | Yes | Eligible as `earliest_detectable_signal` |
| Champion's departure, discovered at the exit interview | No | Not eligible. The **detectable** version is the hard bounce or the deactivation, which was visible |
| Their acquisition, announced publicly | Yes, from the announcement date | If no source was connected, it is `uninstrumented`, not `undetectable` |
| An internal decision at their end, told to us afterwards | No | Undetectable. Say so plainly rather than manufacturing a signal |
| A ticket cluster nobody aggregated | Yes — the data existed | The failure mode is `uninstrumented`, and this is the distinction that makes the classification honest |

The rule: **data that existed in a system we owned is `known_then`, whether or not anyone looked.**
"Nobody looked" is a failure mode, not an excuse, and separating the two is the entire point of
the detection-lag analysis.

## 8. When there is no data — reconstructing from people

Some accounts predate the instrumentation, and some exports are gone. Degrade rather than refuse.

| Source | How to use it | Confidence effect |
| --- | --- | --- |
| The CSM's own notes and calendar | Dates are reliable; interpretations are not. Extract events, discard conclusions | Medium on dated events |
| Slack and shared-channel history | Frequently the only surviving record of when someone first worried. Search for the account name and read the first three hits chronologically | Medium; strong for `first_flagged_date` |
| The renewal opportunity's stage history | Dates internal recognition even when nothing else survives | High for `first_flagged_date` |
| The customer, at interview | Best source for `decision_date` and for the proximate cause; worst for the root cause | Medium |
| Colleagues, asked in the loss review | Ask "what did you know, and when?" — never "why do you think we lost?" | Low, and label it Inferred |

A timeline built entirely from recollection is capped at **Low** confidence and must say so. It is
still worth building: even a recollected timeline usually establishes ordering, and ordering is
what the five whys need.

## 9. Reconstruction errors

| Error | Consequence | Correction |
| --- | --- | --- |
| Starting at the renewal date | Finds the negotiation, misses the loss | Start at T−540 from the decision date |
| Using aggregate usage only | Buyer disconnect is invisible; the account reads healthy to the last week | Segment by the contracted department, always |
| Treating a hard bounce as a departure without checking | A false `sponsor-loss` code, and a threshold change built on it | Check for domain migration, quota rejections, out-of-office and a forwarding address |
| Dating an event by when we noticed it | Every lag shrinks; the model looks better than it is | Two columns: event date and our-awareness date |
| Dropping families with no retained data | The reader assumes they were checked and clean | Print "checked, no history retained" with the retention horizon |
| Letting the usage export end at the offboarding date | Manufactures a cliff that was an offboarding artefact | Truncate the series at `decision_date` and say so |
| Reading interpretation into the event column | The five whys inherit the conclusion instead of testing it | Events are facts; conclusions live in §5 of the record |
| One row per ticket on a noisy account | Fifty rows nobody reads | Cluster tickets by root cause; one row per cluster with a count and a date range |

## 10. A worked fragment

Decision date inferred 2026-05-14 from the customer switching auto-renew off. Effective
2026-08-31. Fragment only — the full record runs to about forty rows.

| Day | Date | Family | Event | Evidence | Tier | Known then? |
|---|---|---|---|---|---|---|
| T−418 | 2025-03-21 | Relationship | Executive sponsor left; no successor was ever named in the CRM | `[CRM · Contact.departed_at · 2025-03-21]` `[Gmail · hard bounce · 2025-03-24]` | Observed | Yes |
| T−401 | 2025-04-07 | Relationship | Multithread depth fell to 1 and stayed there for the remainder of the term | `[interaction · distinct customer_participants, 90d rolling]` | Observed | Yes |
| T−290 | 2025-07-27 | Product usage | Finance (the contracted department) fell from 19 to 4 monthly actives while the account total rose 12% | `[Amplitude · distinct_users_30d, group=finance · 2025-07]` | Observed | Yes |
| T−212 | 2025-10-13 | Support | Cluster of 9 tickets on intercompany reconciliation opened over 5 weeks; none resolved; ticket volume then fell to zero | `[Zendesk · tickets #41102–#41term · 2025-09-08 → 2025-10-13]` | Observed | Yes |
| T−96 | 2026-02-07 | Commercial | Renewal opportunity created; forecast category Commit; no risk record opened | `[CRM · Opportunity.stage_changed_at]` | Observed | Yes |
| T−41 | 2026-04-03 | Firmographic | New VP of Finance started at the customer | `[LinkedIn · announced 2026-04-03; we learned 2026-05-20]` | Observed | No — no enrichment source connected |
| T−0 | 2026-05-14 | Commercial | Customer switched auto-renew off | `[CRM · Contract.AutoRenew__c · changed by d.osei@ · 2026-05-14]` | Observed | Yes |
| T+9 | 2026-05-23 | Relationship | First internal message describing the account as at risk | `[Slack · #cs-alerts · 2026-05-23]` | Observed | — |

Read from this fragment: the earliest detectable signal is the T−418 sponsor departure, giving a
detection lag of 418 days; the account was first flagged at T+9, so the realised lead time was
**negative** — it was flagged after the decision. The failure mode is `unalerted`: the departure
was in the CRM the week it happened and no threshold existed for multithread depth. That is a
`sponsor-loss` primary with `product-value-gap` secondary, origin `adoption`, surfaced
`renewal-execution`, and it produces exactly one fix.
