# The Onboarding Phase Playbook

> The ten phases, laid out backwards from the value gate. Every phase carries an objective, an
> owner on both sides, a duration by mode, its dependencies, an exit criterion that can be
> observed rather than asserted, and the risk you take if you skip it.

**Contents**
1. [How to use this file](#1-how-to-use-this-file)
2. [Mode-by-dimension matrix](#2-mode-by-dimension-matrix)
3. [Duration defaults and the critical path](#3-duration-defaults-and-the-critical-path)
4. [Phases 0–4 — from handover to migrated data](#4-phases-04--from-handover-to-migrated-data)
5. [Phase 5 — admin enablement](#5-phase-5--admin-enablement)
6. [Phase 6 — end-user enablement](#6-phase-6--end-user-enablement)
7. [Phase 7 — first value, and deriving the activation event](#7-phase-7--first-value-and-deriving-the-activation-event)
8. [Phases 8–9 — usage expansion and steady-state handover](#8-phases-89--usage-expansion-and-steady-state-handover)
9. [Exit-criteria library](#9-exit-criteria-library)
10. [Deferred scope and the "not in this phase" list](#10-deferred-scope-and-the-not-in-this-phase-list)

---

## 1. How to use this file

Read §3 to set durations, then walk §4–§8 once per implementation and copy the exit criteria
verbatim into the plan. Do not paraphrase an exit criterion: the whole point is that two people
who disagree about whether a phase is done can both read the same sentence and settle it.

Three rules govern every phase:

| Rule | Why it exists |
| --- | --- |
| **Both sides own it.** Every phase has a named vendor owner *and* a named customer owner. | A phase with only a vendor owner is a phase the customer has not agreed to. It will slip, and the slip will be invisible until it is expensive. |
| **The exit criterion is observable in a system.** | "Configuration complete" is an opinion. "The five contracted workflows exist in the production tenant and each has executed at least once without error" is a query. |
| **The skip-risk is written down before the phase is skipped.** | Phases get cut under time pressure. Recording the risk at plan time turns a silent shortcut into a decision with an owner. |

---

## 2. Mode-by-dimension matrix

The mode changes what the work *is*, not just how often you meet about it. Pick the mode in
SKILL.md Step 3, then apply this matrix before committing to a date.

| Dimension | White-glove | Guided | Tech-touch / self-serve |
| --- | --- | --- | --- |
| Who defines the success criteria | The customer's exec sponsor, in writing, before kickoff | The champion, on the kickoff call | The product, via a use-case selector at signup |
| Who writes the plan | Vendor PM, co-signed by the customer | CSM, confirmed by email | Generated from the selected use case |
| Configuration | Vendor-configured against a documented requirements pack | Vendor-configured in a working session, customer watching | Customer self-configures from templates |
| Integration | Vendor solution architect, with a test plan and a rollback | Vendor-guided, customer executes | Self-serve OAuth connector; failure = support ticket |
| Data migration | Vendor-executed, validated against a reconciliation report signed by the customer | Customer-executed with a vendor-supplied template and a vendor review | Not offered — greenfield only |
| Admin enablement | Live sessions + sandbox exercise + a certification check | One live session + recording | In-product checklist + docs |
| End-user enablement | Train-the-trainer; the customer runs its own rollout | Vendor-run session per team | Email sequence + in-app tour |
| Cadence | Weekly steering + daily standup during migration | Weekly 30-minute working session | Automated, triggered on milestone stall |
| Stall escalation ladder | PM → CSM → vendor exec → customer exec sponsor, 48h per rung | CSM → CS manager, 5 business days per rung | Automated nudge → pooled queue at 10 days |
| Value evidence | A baseline record per value driver, customer-attested | One baseline metric, customer-confirmed by email | Product-measured activation only |
| Cost tracking | Hours against the SOW; burn ratio reviewed weekly | Sessions delivered vs sessions sold | Cohort completion rate only |
| Handover artifact | Full MAP, both sides, dated, plus a written handover memo | Short MAP (8–12 rows) + account record fields | Account record fields only |

**When to upgrade a mode mid-flight.** Move an account up a tier when any of these appear —
and record the cost, because an unfunded upgrade is how services margin disappears:

| Trigger | Move to |
| --- | --- |
| A second integration appears that was not in the SOW | Guided → white-glove, with a change order |
| The customer's data turns out to need transformation, not just loading | Guided → white-glove |
| The named admin leaves during implementation | One tier up, temporarily, until a replacement is certified |
| Float drops below 5 days | Recovery mode, regardless of the original tier |
| Two consecutive weeks with no customer-side task completed | Recovery mode |

---

## 3. Duration defaults and the critical path

These are **starting defaults to be replaced by your own cohort medians** as soon as you have
20+ completed implementations. They are practitioner planning figures `[P]`, not benchmarks —
never present them to a customer as "typical". Business days.

| # | Phase | White-glove | Guided | Tech-touch | Can run parallel with |
| --- | --- | --- | --- | --- | --- |
| 0 | Pre-kickoff | 5 | 3 | 0 (automated) | — |
| 1 | Kickoff | 1 | 1 | 0 | — |
| 2 | Configuration | 15 | 7 | 1 | 3, 4 (if separate customer owners) |
| 3 | Integration | 15 | 7 | 1 | 2, 4 (if separate customer owners) |
| 4 | Data migration | 20 | 7 | n/a | 2, 3 (if separate customer owners) |
| 5 | Admin enablement | 5 | 3 | 1 | 4 |
| 6 | End-user enablement | 10 | 5 | 3 | — |
| 7 | First value (to V-day) | 21 | 14 | 7 | — |
| 8 | Usage expansion | 30 | 21 | 14 | 9 |
| 9 | Steady-state handover | 5 | 3 | 0 | 8 |

**Critical path arithmetic.**

```
serial_core   = phase2 + phase3 + phase4          (single customer owner across all three)
parallel_core = max(phase2, phase3, phase4)       (a separate named owner for each)

critical_path = phase0 + phase1 + core + phase5 + phase6 + phase7
```

White-glove worked example: serial core = 15+15+20 = 50; parallel core = 20.
Critical path serial = 5+1+50+5+10+21 = **92 business days** (~18 calendar weeks).
Critical path parallel = 5+1+20+5+10+21 = **62 business days** (~12 calendar weeks).

**That 30-day difference is bought with one thing: a second and third named customer owner.**
It is the single highest-leverage ask in the kickoff call, and it is why Emilia D'Anzica's rule
of gating onboarding completion on a minimum contact count `[P]` should also gate the *start*.

**Do not compress phase 7.** It is the only phase measuring the customer's reality rather than
your delivery. Compressing 2–9 is engineering; compressing 7 is pretending.

---

## 4. Phases 0–4 — from handover to migrated data

### Phase 0 — Pre-kickoff

| Field | Content |
| --- | --- |
| **Objective** | Arrive at kickoff with nothing left to discover — the use case, the stakeholders, the success criteria and the access requests are all known before the call starts |
| **Vendor owner** | Implementation lead (white-glove) / CSM (guided) |
| **Customer owner** | The champion — the person who signed off on the business case |
| **Depends on** | A completed sales handover (`handover.md`) |
| **Exit criterion** | Sold-vs-Real table drafted · admin named with email and title · security/access request submitted · agenda sent ≥3 business days before kickoff · pre-read acknowledged by the champion |
| **Risk if skipped** | Kickoff becomes discovery. Two weeks lost, and the customer's first experience of the post-sale relationship is being asked questions they already answered during the sale |

### Phase 1 — Kickoff

Full agenda, question set and baseline-capture record in `kickoff.md`.

| Field | Content |
| --- | --- |
| **Objective** | Establish, in writing: the business objectives, the success criteria and their measurement, the stakeholder map, the timeline with both-side owners, the escalation path, and the customer's internal comms plan |
| **Vendor owner** | Implementation lead; CSM attends and owns the relationship thread |
| **Customer owner** | Exec sponsor opens it; champion owns the follow-through |
| **Depends on** | Phase 0 exit |
| **Exit criterion** | A written summary sent within 24 hours containing all six items above, and confirmed by the champion in writing. **The confirmation is the exit criterion, not the meeting** |
| **Risk if skipped** | No shared definition of done. Every later disagreement about scope, date or value becomes unresolvable because there is no artifact to return to |

### Phase 2 — Configuration

| Field | Content |
| --- | --- |
| **Objective** | The contracted primary use case is configured to the customer's actual process, in a non-production environment |
| **Vendor owner** | Solution architect (white-glove) / CSM (guided) |
| **Customer owner** | Process owner — the person who will be blamed if the workflow is wrong. Not the IT admin |
| **Depends on** | Kickoff exit; access provisioned |
| **Exit criterion** | Every contracted workflow exists in the non-production tenant and each has executed end-to-end at least once without error, witnessed by the customer process owner |
| **Risk if skipped** | The product is configured to the vendor's demo rather than the customer's process. Users hit friction on day one and conclude the tool does not fit |

### Phase 3 — Integration

| Field | Content |
| --- | --- |
| **Objective** | Each contracted integration authenticated, syncing, and producing correct data in the customer's environment |
| **Vendor owner** | Solution architect / support engineer |
| **Customer owner** | The system owner for *each* integrated system — usually a different person per system, which is why this phase serialises unexpectedly |
| **Depends on** | Customer-side credentials, network/security approval, and a sandbox in the source system |
| **Exit criterion** | Each integration has run on its production schedule for **5 consecutive days with zero errors**, and a customer owner has confirmed a sample record matches the source |
| **Risk if skipped** | The silent value killer. The account appears live, users log in, and the data is stale or partial. Integration failure produces the exact signature of disengagement (`T2` in the churn-signal taxonomy) with none of the cause |

### Phase 4 — Data migration

| Field | Content |
| --- | --- |
| **Objective** | Historical data present, correct and reconciled — so users trust what they see the first time they look |
| **Vendor owner** | Data engineer / solution architect |
| **Customer owner** | A named data owner who can sign off on correctness. This person is almost never the champion |
| **Depends on** | Source extract available; a documented field mapping; a decision on the historical window |
| **Exit criterion** | A reconciliation report showing source record count, loaded record count, rejected records with reasons, and a spot-check of ≥20 records, **signed off by the named customer data owner** |
| **Risk if skipped** | Users hit wrong or missing data on day one. This is the fastest way to lose an end-user population, and it is nearly impossible to recover — first impressions of data quality do not get a second look |

**The historical-window decision.** Ask explicitly: how far back does the data need to go for the
first value moment to be believable? Migrating five years when the use case needs one quarter is
the commonest cause of a blown migration estimate, and it is a decision the customer can make in
five minutes if anyone asks them.

---

## 5. Phase 5 — admin enablement

| Field | Content |
| --- | --- |
| **Objective** | At least two customer administrators can operate and change the system without the vendor |
| **Vendor owner** | Enablement lead / CSM |
| **Customer owner** | The admins themselves, with the champion accountable for their attendance |
| **Depends on** | Configuration complete (they must train on their own configuration, never a generic sandbox) |
| **Exit criterion** | Both named admins complete the six core admin tasks unaided, observed, in the customer's own tenant |
| **Risk if skipped** | Single-admin dependency. Every configuration change becomes a support ticket, the support load looks like dissatisfaction, and an admin departure becomes an outage |

**The six core admin tasks** — define these per product, freeze them, and use the same six every
time so the certification means something across accounts:

| # | Task class | Example |
| --- | --- | --- |
| 1 | Add and deactivate a user, and assign a role | Provisioning without the vendor |
| 2 | Change a configuration object the business will want changed | The workflow, field, or rule most likely to need edits |
| 3 | Diagnose and resolve the most common end-user error | Cuts the ticket volume that otherwise arrives at your queue |
| 4 | Run and interpret the core report | The admin must be able to answer "is it working?" |
| 5 | Re-authenticate a failed integration | The single most common P2 in the first 90 days |
| 6 | Find the answer in the documentation, unaided | Tests self-sufficiency, not memory |

**Never train one admin.** A single trained admin is a single point of failure on the account,
and admin/owner change (`U15` in the churn-signal taxonomy) is a leading risk signal with a
60–180 day lead time `[P]`. Two admins is a gate, not a preference.

**Re-run trigger:** any change to the primary admin re-opens this phase. Do not treat a
replacement admin as trained because the role is filled.

---

## 6. Phase 6 — end-user enablement

| Field | Content |
| --- | --- |
| **Objective** | Every provisioned seat knows what to do, why, and by when |
| **Vendor owner** | Enablement lead (white-glove: train-the-trainer only) |
| **Customer owner** | Each team lead, individually named — not "the business" |
| **Depends on** | Admin enablement complete; production data loaded; the customer's internal announcement sent |
| **Exit criterion** | ≥70% of provisioned seats in each team performed the core action ≥1× within 14 days of their session `[P]` |
| **Risk if skipped** | Licences provisioned, nobody trained, utilisation flat. This produces the `Shelfware` compound pattern — seat utilisation <0.5 plus narrow breadth plus a use case never live — which survives only until the buyer looks |

**Design rules:**

| Rule | Reason |
| --- | --- |
| Train against the customer's own data, never a demo tenant | Users discount anything they cannot recognise |
| One session per team, not one session per company | Different teams have different jobs; a generic session teaches everyone the average job, which is nobody's job |
| Teach the 5–8 value-path features only | Pendo's 2019 Feature Adoption Report (615 subscriptions, three-month window) found ~80% of features are rarely or never used and ~12% drive ~80% of daily usage `[M]`. Teaching the catalogue teaches the 80% |
| Schedule the session **after** the internal announcement, never before | Training without permission to change how they work produces informed non-adopters |
| Book the measurement date at the same time as the session | If nobody is scheduled to check on day 14, nobody checks |

**Measurement, per team:**

| Metric | Target | If missed |
| --- | --- | --- |
| Session attendance / invited | ≥80% | The team lead did not require it — go back to the lead, not the users |
| Core action performed ≥1× within 14d | ≥70% `[P]` | Re-run for that team with the lead present |
| Core action performed ≥3× within 30d | ≥50% `[P]` | The workflow does not fit their process — this is a configuration finding, not a training finding |
| Team activation 30d post-training | ≥40% | Below this, treat the team as not launched and say so in the plan |

**The train-the-trainer decision.** Above roughly 150 end users, vendor-delivered training does
not scale and does not survive staff turnover. Certify the customer's own trainers, give them the
deck and the measurement sheet, and make the rollout schedule a customer-owned MAP row.

---

## 7. Phase 7 — first value, and deriving the activation event

| Field | Content |
| --- | --- |
| **Objective** | The customer observes the outcome they bought, at the cadence the business case assumed, and says so |
| **Vendor owner** | CSM |
| **Customer owner** | The named business owner from the baseline record — the person whose number is supposed to move |
| **Depends on** | Everything. This is the terminal phase of the plan |
| **Exit criterion** | The activation event has occurred at cadence for ≥2 natural cycles · was performed by the buying team, not only the admin · has been measured against the kickoff baseline · and a named customer owner has attested to it in writing |
| **Risk if skipped** | The Success Gap. The project closes green, the customer never got the outcome, and the first renewal is argued without evidence on either side |

### 7.1 Deriving the activation event when `cs-context` has none

If the activation event is `UNKNOWN`, do not invent one and do not substitute "logged in". Derive
it, and mark the result `inferred` with the rule stated:

| Step | Method | Output |
| --- | --- | --- |
| 1 | List 8–15 candidate events from the product's event taxonomy — actions that produce an artifact or complete a job, never page views | Candidate list |
| 2 | Build a labelled cohort: accounts with ≥12 months tenure, split into retained and churned/downsold at first renewal | Two cohorts |
| 3 | For each candidate, compute the share of each cohort that performed it ≥N times within the first 60 days, for N ∈ {1, 3, 10} | A separation table |
| 4 | Rank candidates by the retained-minus-churned gap at each N. Pick the event–threshold pair with the largest gap that at least 25% of retained accounts cleared | The candidate activation event |
| 5 | Sanity-check with the CSM team: can a human explain *why* this event predicts retention? Discard any event whose mechanism nobody can state | The activation event |

Two hard constraints. **Never pick an event the vendor can perform on the customer's behalf** —
it becomes a metric the team games rather than a signal. And **never pick a first-time-only
event**: value is recurrence, so the definition must include a frequency.

If there is no labelled cohort yet (fewer than ~30 first renewals), say so, use the customer's own
stated success criterion from kickoff as an account-specific proxy, and mark it
`UNKNOWN — requires a labelled renewal cohort` at the portfolio level.

### 7.2 What counts as attestation

Attestation is a sentence from a named customer owner, in writing, that contains a number:

> "We're now closing the month-end reconciliation in 4 days instead of 11, and it's held for two
> cycles." — Priya N., Director of Finance Ops, 2026-08-14

Not attestation: a thumbs-up in Slack · "yes it's going well" on a call · a vendor's summary of a
call · a green project status · an NPS score. A score is a feeling about a relationship; V-day
needs a claim about an outcome.

---

## 8. Phases 8–9 — usage expansion and steady-state handover

### Phase 8 — Usage expansion

| Field | Content |
| --- | --- |
| **Objective** | A second team or a second use case is live, so the account no longer depends on one process surviving unchanged |
| **Vendor owner** | CSM |
| **Customer owner** | Champion, with the second team's lead named |
| **Depends on** | V-day passed and attested |
| **Exit criterion** | The second team or use case has performed the core action for 2 consecutive weeks, **and** adoption breadth is at or above the core-feature floor agreed at kickoff |
| **Risk if skipped** | Single-use-case dependency. One process change, one reorg, or one champion departure removes the entire reason the account exists |

This is where the pre-mapped expansion milestone from kickoff becomes usable. Murphy's "logical
expansion" framing is that the next step should already be anticipated rather than merely
expected `[P]` — which is only true if you named it at kickoff. **Do not open the commercial
conversation before V-day.** Expansion before proven value is the anti-pattern that teaches the
customer to discount everything else you say.

### Phase 9 — Steady-state handover

| Field | Content |
| --- | --- |
| **Objective** | The receiving CSM owns the account with everything the onboarding team knew |
| **Vendor owner** | Implementation lead, jointly with the receiving CSM |
| **Customer owner** | Champion — the handover is announced to them, not performed behind them |
| **Depends on** | V-day attested; day-30 checkpoint scheduled |
| **Exit criterion** | Every item in the transfer list is present **in the account record** (not in a document, not in a person's head), the 30/60/90 checkpoints are in calendars on both sides, and the customer has been told who owns them now and why |
| **Risk if skipped** | The receiving CSM restarts discovery. The customer repeats themselves, concludes the vendor does not remember them, and the relationship resets to zero at exactly the moment it should compound |

**Transfer list:** captured baseline + measurement owner · attested V-day evidence · Sold-vs-Real
table with open gaps and dates · stakeholder map with roles and the champion's own words on why
they bought · configuration decisions and the reason for each · open defects with committed dates ·
deferred-scope list · the pre-mapped next expansion milestone · `opt_out_deadline`.

---

## 9. Exit-criteria library

Copy these verbatim. Each is written so that a query or a document settles the argument.

| Phase | Exit criterion (copy this) |
| --- | --- |
| 0 Pre-kickoff | Sold-vs-Real drafted; admin named with email and title; access request submitted; agenda sent ≥3 business days ahead; pre-read acknowledged by the champion |
| 1 Kickoff | Written summary sent within 24h covering objectives, success criteria + measurement, stakeholders, timeline with both-side owners, escalation path, and the customer's internal comms plan — **confirmed in writing by the champion** |
| 2 Configuration | All contracted workflows exist in the non-production tenant; each has executed end-to-end without error at least once, witnessed by the customer process owner |
| 3 Integration | Each integration has run on its production schedule for 5 consecutive days with zero errors; a customer owner has confirmed a sample record matches source |
| 4 Data migration | Reconciliation report (source count, loaded count, rejects with reasons, ≥20-record spot check) signed off by the named customer data owner |
| 5 Admin enablement | ≥2 named admins each completed the 6 core admin tasks unaided, observed, in the customer's own tenant |
| 6 End-user enablement | ≥70% of provisioned seats per team performed the core action ≥1× within 14 days of their session |
| 7 First value | Activation event at cadence for ≥2 natural cycles, by the buying team, measured against the kickoff baseline, attested in writing by a named customer owner with a number |
| 8 Usage expansion | Second team or use case performed the core action for 2 consecutive weeks; adoption breadth ≥ the agreed core-feature floor |
| 9 Handover | Every transfer-list item present in the account record; 30/60/90 in both calendars; customer informed of the new owner |

**Do not mark a phase complete on a date.** Mark it complete on evidence, and record where the
evidence lives. A phase marked complete by elapsed time is the mechanism by which a project shows
green while TTFV doubles.

---

## 10. Deferred scope and the "not in this phase" list

Every implementation accumulates requests that are real, reasonable, and not in this phase. If they
are not written down they either get silently absorbed — which is how burn ratio blows past 1.3× —
or silently dropped, which is how a customer arrives at the first renewal believing they were
promised something.

Keep one table, visible to both sides, reviewed at every steering call:

| # | Request | Raised by | Date | Why deferred | Where it goes | Revisit date | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |

Four dispositions, and they must be stated:

| Disposition | Meaning | Who owns the follow-through |
| --- | --- | --- |
| **Phase 8** | Real scope, after V-day | CSM |
| **Change order** | Real scope, needs funding | Vendor PM + customer champion |
| **Roadmap** | Product does not do this; a request has been filed with an ID | Product, with the CSM tracking the ID |
| **Declined** | We will not do this. Say so plainly, with the reason | Vendor PM — and it goes in the handover record |

A deferred item with no revisit date is a broken promise with a delay fuse. The revisit date is
the field that makes this table worth keeping.
