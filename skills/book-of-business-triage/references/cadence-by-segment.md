# Cadence by Segment

> What each account is actually entitled to, what that costs in annual hours, and how to run a
> pooled book without pretending it is a named one. Read when building the maintenance block,
> when a book changes shape, or when deciding whether an account should move coverage model.

**Contents**
1. [Coverage model vs segment — they are not the same axis](#1-coverage-model-vs-segment)
2. [Tier entitlements](#2-tier-entitlements)
3. [What a tier costs in annual hours](#3-what-a-tier-costs-in-annual-hours)
4. [Running a pooled book](#4-running-a-pooled-book)
5. [Named-CSM cosplay — the pooled failure mode](#5-named-csm-cosplay)
6. [Tech-touch and the exception queue](#6-tech-touch-and-the-exception-queue)
7. [Promotion and demotion between coverage models](#7-promotion-and-demotion)
8. [Silence thresholds — the rot-sweep parameters and the weekly filter set](#8-silence-thresholds)
9. [The renewal clock by segment](#9-the-renewal-clock-by-segment)
10. [What changes with contract shape](#10-what-changes-with-contract-shape)
11. [Which signals matter per segment](#11-which-signals-matter-per-segment)
12. [Anti-patterns](#12-anti-patterns)
13. [Evidence register](#13-evidence-register)

---

## 1. Coverage model vs segment

Two different things, routinely conflated, and the conflation is what produces unservable books.

| Axis | What it is | Set by |
| --- | --- | --- |
| **Segment** | Where the account sits on the ARR/complexity spectrum | Dollar boundaries in `cs-context` §3 |
| **Coverage model** | How much human attention the company has *funded* for it | CS budget and headcount |

An enterprise-segment account on a pooled coverage model is not a contradiction — it is a
funding decision, and it must be visible in the queue so nobody promises enterprise service on
a pooled budget. **Triage allocates against the coverage model, and flags any account where the
segment and the model have drifted apart** (§7).

### 1.1 The three coverage models at a glance

| | Named CSM | Pooled | Tech-touch |
| --- | --- | --- | --- |
| Unit of work | The account | The queue item | The segment |
| Planned touches / year | 12–24 | 3–6 (mostly triggered) | 0 human, unlimited automated |
| Business reviews | 1–4 live/yr by tier | 0–1, templated from live data | Automated value snapshot + webinar |
| Who answers inbound | The named CSM | Whoever is on rota, with a written handover note | Support queue, escalating on rule |
| Renewal ownership | Named | Pool lead by renewal calendar, not by relationship | Automated + AE on exception |
| What triage produces | A per-account plan | A ranked SLA-bounded queue | Exception list only |
| The trap | Over-servicing the loudest account | **Named-CSM cosplay** — promising a relationship the staffing does not fund | Never noticing the account that grew into needing a human |

Read this before building the maintenance block: the unit of work changes, and running a pooled
book as if every account had a named CSM produces a queue nobody finishes and a set of
relationships nobody owns.

---

## 2. Tier entitlements

A tier entitlement is a **design decision you fund**, not a benchmark you look up. The ladder
below is this library's default `[P]`, derived from the hour costs in §3 rather than copied from
anyone: the entitlement has to be affordable at the book size you actually carry. Set your own
numbers — the rule that matters is that they are written down, funded, and visible to the CSM
who has to honour them.

| Tier | Typical criteria `[P]` | Coverage | Live EBR | Operational QBR | Cadence touches/yr | Success plan | Format |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **Strategic / Premier+** | Top 5–10% of ARR, board-visible, reference-able | Named + exec sponsor | 4×/yr | Monthly ops sync | 20–24 | Monthly | Exec-to-exec, onsite where possible |
| **Enterprise / Premier** | High-touch segment | Named | 2×/yr | Quarterly | 12–16 | Quarterly | Live video, deck + 48-h pre-read |
| **Growth / Mid-market** | Named CSM, pooled backup | Named, thin | 1×/yr | 2×/yr | 6–10 | Semi-annual | Live video, templated deck from live data |
| **Scale / Tech-touch** | Below the named-coverage ARR floor | Pooled or digital | 0 | Digital only | 0–4 human, unlimited automated | Automated | Value snapshot + webinar + office hours |

**The entitlement is a floor, not a schedule.** A Growth-tier account inside its opt-out window
gets renewal work regardless of having had its two QBRs. The entitlement governs the
*maintenance* block; the must-do and high-return blocks override it.

---

## 3. What a tier costs in annual hours

A full-time CSM has roughly **1,147 annual deployable customer hours** (`capacity-model.md`
§6.1). Every entitlement above is a claim on that number. Here is what each tier costs, using
`play-durations.md` and the tier multipliers.

| Tier | Cadence touches | Business reviews | Renewal motion | Reactive allowance | **Annual hours/account** | Max accounts on one CSM (100% of capacity) |
| --- | --- | --- | --- | --- | --- | --- |
| Strategic | 22 × 2.0 = 44.0 | 4 × 14 = 56.0 | 8.0 | 24.0 | **132.0** | 8.7 |
| Enterprise | 14 × 2.0 = 28.0 | 2 × 11 = 22.0 | 5.5 | 16.0 | **71.5** | 16.0 |
| Growth / mid-market | 8 × 1.25 = 10.0 | 2 × 6 = 12.0 | 3.0 | 8.0 | **33.0** | 34.8 |
| Scale / tech-touch (pooled human) | 3 × 0.5 = 1.5 | 0 | 0.5 | 3.0 | **5.0** | 229.4 |

**How to read the last column.** It is the number of accounts that consumes 100% of deployable
capacity — which is not a target, it is a ceiling. Plan at **70–80% of it** so the must-do
block, escalations and expansion have somewhere to live. So:

| Tier | Ceiling | **Plannable book (75%)** |
| --- | --- | --- |
| Strategic | 8.7 | **6–7 accounts** |
| Enterprise | 16.0 | **12 accounts** |
| Growth / mid-market | 34.8 | **26 accounts** |
| Scale / tech-touch | 229.4 | **170 accounts** |

There is **no neutral published benchmark for accounts-per-CSM** to compare these against. The
ratios circulating in the market are either vendor marketing or a decade old, and predate digital
CS, PLG at scale and current tooling — so this file does not carry them. The bottom-up numbers
above are the argument, and they are auditable: every one of them decomposes into entitlements ×
play durations. If someone challenges the book size, walk them through §3, not through a ratio.

**Mixed books.** A CSM carrying 4 Enterprise + 18 Growth accounts: (4 × 71.5) + (18 × 33.0)
= 286 + 594 = **880 hours** against 1,147 — 77% loaded. Servable, tight. Add two more
Enterprise accounts and it is 1,023 h (89%) — oversubscribed the moment anything goes wrong.

---

## 4. Running a pooled book

A pooled book is not a named book with worse service levels. It is a **different operating
model**, and the switch is from managing accounts to managing a queue.

| Dimension | Named | Pooled |
| --- | --- | --- |
| Unit of work | The account | The queue item |
| Who owns it | One person, permanently | The rota, per item |
| What is promised | A relationship | A response time |
| What triage produces | A per-account plan | A ranked, SLA-bounded queue |
| Continuity mechanism | The CSM's memory | The written handover note — mandatory |
| Failure mode | Over-servicing the loudest account | Every item handled once, no item followed through |

### 4.1 Queue design

Route every trigger into exactly one queue with a written SLA. Nothing enters a pooled book
without a queue.

| Queue | Entry criteria | SLA `[P]` | Who |
| --- | --- | --- | --- |
| **Declared** | Customer asked for something explicitly | 1 business day | Rota |
| **Commercial** | Opt-out deadline ≤60 d · auto-renew flip · payment failure · downgrade request | 1 business day | Pool lead |
| **Risk** | Risk band moved to At Risk or worse · escalation opened · dark account past day 60 | 2 business days | Rota |
| **Expansion** | Entitlement ≥85% · limit breach · new-team signal, **health gate passed** | 5 business days | Rota, or AE above the ARR threshold |
| **Onboarding** | Contract start → verified time-to-first-value | Per onboarding plan | Onboarding specialist if one exists |
| **Maintenance sweep** | Silence threshold crossed (§8) | Batched weekly | Rota |
| **Program** | Content, automation upkeep, journey QA | Weekly block | Pool lead |

### 4.2 The four pooled rules

1. **Every item gets a written handover note or it does not close.** Two sentences: what
   happened, what is owed next and by when. Without this the pool has no memory and the
   customer re-explains their situation every time — the single most common pooled complaint.
2. **The SLA is the promise, not the person.** Never say "I'll own this" in a pooled model.
   Say "someone from the team will come back to you by Thursday", and make Thursday true.
3. **Batch the sweep.** Pooled maintenance is done in batches of 15–30 accounts with one data
   pull, not one account at a time. This is the only way the cycle time in §4.3 works.
4. **Escalate to a named owner on a rule, not on a feeling.** The promotion triggers in §7 are
   the rule. Anything above the named-coverage ARR floor with an open commercial risk gets a
   temporary named owner for the duration.

### 4.3 The pooled cycle-time arithmetic — do this before promising anything

```
Weeks to sweep the whole book = accounts per CSM ÷ ( maintenance hours per week ÷ hours per touch )
```

Worked: 110 accounts per pooled CSM, 14.9 discretionary hours, 30% to maintenance = 4.5 h,
async touch = 0.5 h → 9 touches/week → **12.2 weeks per full sweep.**

That is a quarterly proactive cycle. Publish it. A pool that promises monthly contact on this
arithmetic will miss, and the miss will be blamed on the CSMs rather than on the arithmetic.

---

## 5. Named-CSM cosplay

The dominant pooled failure mode: running a pooled book while promising named-CSM service.

| Symptom | What it actually costs |
| --- | --- |
| "I'm your CSM" said on a pooled account | The customer now escalates to a person who is on rota next week |
| Per-account plans written for 110 accounts | The plan-writing consumes the hours the touches needed |
| A recurring call booked with every pooled account | 110 × 1.25 h × 12/yr = 1,650 h against ~1,147 available |
| Ad-hoc ownership by whoever answered first | Coverage looks fine; follow-through is zero |
| No handover notes because "I remember this one" | The one person who remembers goes on leave |

**The test.** If the arithmetic in §4.3 does not support the cadence being promised, the
promise is the thing to change — not the effort. Write the supported cadence into the customer
communication, and put the difference into automation.

---

## 6. Tech-touch and the exception queue

Tech-touch is not "no service". It is service delivered by program rather than by person, and
the CSM hours go into building the program, not into accounts.

| Element | What it looks like |
| --- | --- |
| Onboarding | In-app walkthroughs, self-paced curriculum, automated milestone checks |
| Ongoing value | Automated value snapshot on a fixed cadence, webinars, office hours, community |
| Support path | Support queue, with rule-based escalation |
| Business review | Digital only — an automated snapshot, not a meeting |
| Content refresh | Quarterly `[V — vendor guidance]` |

**The exception rules — when a human enters.** These are the only human touches a tech-touch
account gets, and each is a queue item, not a relationship.

| Exception | Threshold | Response |
| --- | --- | --- |
| ARR crossed the named-coverage floor | Per `cs-context` §3 | Promote (§7) |
| Dark account | >60 days from contract start with zero core events | Onboarding queue, 2 business days |
| Payment failure or invoice >30 days past due | Billing family | Commercial queue, 1 business day |
| Explicit request for a human | Any | Declared queue, 1 business day |
| Escalation or P1 | Any | Risk queue, same day |
| Entitlement ≥85% with the health gate passed | Expansion family | Expansion queue, 5 business days |
| Opt-out deadline ≤30 days on an annual contract | Commercial | Commercial queue, 1 business day |

**The tech-touch blind spot to design against:** an account that grows into needing a human and
is never noticed, because tech-touch programs measure aggregates and this is a single-account
event. The ARR-floor check and the entitlement check above are what catch it. Run both weekly.

---

## 7. Promotion and demotion

Coverage model changes are decisions with dollars attached. Write them down; never let them
happen by drift.

### 7.1 Promotion triggers (to a higher-touch model)

| Trigger | Threshold | New model |
| --- | --- | --- |
| ARR crossed the segment boundary | Per `cs-context` §3 | Match the segment |
| Renewal ARR at stake exceeds the named floor | Opt-out ≤120 d | Temporary named owner through renewal |
| Escalation opened | Any P1 with exec visibility | Temporary named owner until closed + 30 d |
| Expansion opportunity above the AE threshold | Per `cs-context` §4 | Named + AE |
| Strategic designation | Reference-ability, logo value, design-partner status | Named; state the non-ARR rationale in writing |
| **Deferral counter ≥3** | Three consecutive weeks below the cut line | Forced 15-minute checkpoint, then promote or demote — never a fourth silent deferral |

### 7.2 Demotion triggers (to a lower-touch model)

| Trigger | Threshold | New model |
| --- | --- | --- |
| ARR fell below the segment boundary | Sustained 2 quarters | Match the segment |
| Structural deficit >15% of capacity | `capacity-model.md` §6.2 | Demote the lowest-ARR tier of the named book, in writing, with the ARR named |
| Account declines the cadence | 2 consecutive customer-cancelled reviews | Offer the digital program instead |
| Book handover with no replacement headcount | — | Explicit demotion beats silent neglect |

**The rule that matters.** A demotion is announced internally with the ARR and the account
list, and the accounts move to the receiving queue with handover notes. A demotion that happens
by nobody having time is not a demotion — it is the rot the sweep exists to catch.

---

## 8. Silence thresholds

The rot-sweep parameters. All are practitioner thresholds `[P]`, segment-scaled, and all count
**bilateral** contact only — vendor outbound, marketing sends and NPS blasts are not touches.

| Filter | Strategic | Enterprise | Mid-market | SMB / tech-touch |
| --- | --- | --- | --- | --- |
| No bilateral touch | 21 d | 45 d | 60–90 d | 120 d |
| No product activity (daily-cadence product) | 7 d | 14 d | 14 d | 21 d |
| No product activity (weekly-cadence product) | 21 d | 30 d | 30 d | 45 d |
| No product activity (monthly/quarterly-cadence) | 45 d | 60 d | 60 d | 90 d |
| No exec-sponsor contact | 60 d | 90 d | 180 d | n/a |
| Dark account (zero core events since start) | 30 d | 45 d | 60 d | 60 d |
| Unowned (`owner_csm IS NULL`) | 3 d | 7 d | 14 d | 30 d, above the tech-touch ARR floor |
| Risk band unreviewed | 30 d | 45 d | 60 d | 90 d |

**Know the product's natural cadence before using the activity thresholds.** A
quarterly-reporting tool with 60 days of silence is behaving normally; a daily workflow tool
with 14 is not. Getting this wrong manufactures false-red accounts and burns the sweep's
credibility.

### 8.1 The rot-sweep filter set — what to run weekly, and off which field

The thresholds above are the parameters; this is the filter set the weekly rot sweep actually
runs, collapsed to the six checks a triage can execute in a few minutes, each with the field it
reads. Accounts do not rot because someone decided to ignore them; they rot because nobody decided
anything — and this sweep is the cheap check that catches the failure the queue itself creates.

| Filter | Threshold (segment-scaled, practitioner) | Source field |
| --- | --- | --- |
| No bilateral touch | Enterprise 45 d · mid-market 60–90 d · SMB/tech-touch 120 d | `interaction.timestamp`, two-way only — vendor outbound and NPS blasts do not count |
| No product activity | 14 d daily-cadence products · 30 d weekly · 60 d monthly/quarterly | `usage_daily`, last non-null |
| Dark account | Contract active >60 d with zero core events since `start_date` | `usage_event` |
| Unowned | `owner_csm IS NULL` or owner inactive >30 d, above the tech-touch ARR floor | `account.owner_csm` |
| Stale assessment | Risk band unchanged and unreviewed >60 d | Last scoring run |
| **Deferral counter ≥3** | Below the cut line three weeks running | The triage's own not-this-week list |

**The six-filter table is the compressed form of the segment matrix above.** Where the two differ,
the matrix wins — it carries the Strategic column and the exec-sponsor-contact filter, which the
compressed set folds into the bilateral-touch row. Use the compressed set for the weekly run and
the matrix when a specific account's threshold is being argued about.

**The deferral counter is the only filter this library owns end to end.** The other five read
source systems; this one reads the previous weeks' not-this-week lists, which means it only works
if those lists are kept. An account deferred three weeks running gets exactly one of two outcomes —
a 15-minute checkpoint booked into next week's must-do block, or a written demotion to a lower
cadence tier with a named reason and a review date (**R14 · C32**). Never a silent fourth
deferral: that is where accounts die while the queue looks fine.

**A filter firing is a question, not a verdict.** The output of the sweep is a checkpoint — one
targeted question, 0.25 h, and a logged answer — not a save play. Treating every silent account as
at risk burns the sweep's credibility as fast as running it on the wrong thresholds.

---

## 9. The renewal clock by segment

All windows are relative to the **opt-out deadline** (`renewal_date − notice_period_days`),
never the renewal date `[P]`.

| Window | Strategic / Enterprise | Mid-market | SMB / tech-touch |
| --- | --- | --- | --- |
| Value baseline established | T−270 to T−180 | T−150 | Automated |
| Value evidence delivered | T−180 to T−120 | T−120 to T−90 | Automated snapshot |
| Commercial intent tested | T−120 to T−90 | T−90 to T−60 | T−45 |
| Paper in motion, risk surfaced | T−90 to T−60 | T−60 to T−30 | T−30 |
| Close and de-risk | T−60 to T−30 | T−30 to T−14 | T−14 |
| Exception handling only | T−30 to T−0 | T−14 to T−0 | T−7 |

**Triage consequence.** An account enters the must-do block the week its window opens, not the
week its renewal date approaches. Notice periods cluster at 30/60/90 days — 30 days is modal in
standard-form agreements and 60 is common in negotiated enterprise contracts `[P]` — so a
February renewal on 90 days' notice is a **November** must-do.

**Multi-year contracts start two quarters earlier** than annual ones. Multi-year customers
frequently have no living relationship at renewal time, because nobody had a reason to build
one for three years.

---

## 10. What changes with contract shape

| Contract shape | Triage consequence | Cadence consequence |
| --- | --- | --- |
| **Monthly / evergreen** | Churn can land in any month; there is no notice window to plan against | Continuous short-window scoring (7/14 d). Billing signals outrank relationship signals |
| **Annual** | Risk concentrates around the notice window | The renewal clock in §9 governs the maintenance block |
| **Multi-year** | Long silence between decisions; risk accumulates invisibly | Force an annual value checkpoint even with no commercial event — otherwise the account is unowned in practice for two years |
| **Usage-based** | Consumption pacing replaces seat utilisation as the primary metric; contraction shows up as a commitment reduction, not a logo loss | Add a mid-term pacing review to the cadence; a pacing check is a 0.5-hour async play |

Retention rises with ACV. Both Benchmarkit (CY2024, N=225) and SaaS Capital (2025) find GRR and
NRR increase monotonically with ACV `[M]`, and Benchmarkit's CY2024 medians are GRR 88% /
NRR 101% overall, with GRR 92% under usage-based pricing `[M]`. The triage implication is not
"ignore SMB" — it is that **SMB risk must be caught by program and automation, because the
per-account hours do not exist.**

---

## 11. Which signals matter per segment

Rank the queue on the signals that actually carry information for that segment.

| | SMB (<$25k ACV) | Mid-market ($25–100k) | Enterprise ($100k+) |
| --- | --- | --- | --- |
| Dominant churn driver | Business failure, affordability, involuntary/payment | Champion departure, unrealised value | Budget cycles, exec change, consolidation, procurement |
| Practical lead-time target | 14–30 d | 60–90 d | 120–180 d |
| Prioritise | Product silence, payment failure, cancel-flow behaviour, entitlement collapse | Seat utilisation, champion departure, meeting no-shows, success-plan milestones | Champion and exec-sponsor state, procurement re-engagement, auto-renew flag, exec change, ROI evidence |
| De-prioritise | Exec sponsor and QBR signals — that motion does not exist | — | DAU/MAU as an absolute; enterprise cadence is legitimately low |
| Detection budget | Fully automated on product + billing data | Automated scoring + CSM review | Human-led; signals are inputs to a judgement |

`[M]` for the ACV/retention gradient; the lead-time targets and signal rankings are
practitioner `[P]`.

---

## 12. Anti-patterns

| Anti-pattern | Correction |
| --- | --- |
| One cadence for the whole book | Cadence follows the coverage model, and the coverage model is a funding decision |
| Promising named service on a pooled book | §5. Change the promise, not the effort |
| A pooled item closed with no handover note | Two sentences: what happened, what is owed, by when |
| Sweeping a pooled book one account at a time | Batch 15–30 accounts on one data pull |
| Escalating a pooled account because it complained loudest | Promote on the §7 rules, not on volume |
| Letting an account drift between coverage models | Promotion and demotion are written decisions with ARR attached |
| Using aggregate thresholds for silence | Segment-scaled, and scaled to the product's natural cadence |
| Scoring against the renewal date | The opt-out deadline governs; a Feb renewal on 90-day notice is a November must-do |
| Treating a multi-year account as low-maintenance | Force an annual value checkpoint; multi-year accounts arrive at renewal with no relationship |
| Applying enterprise DAU/MAU expectations to enterprise accounts | Low cadence can be correct; check the buying team, not the aggregate |
| Justifying a book size with a published accounts-per-CSM ratio | No neutral one exists; build bottom-up (§3) and argue from entitlements × play durations |

---

## 13. Evidence register

| Claim | Value | Source | Year | Label |
| --- | --- | --- | --- | --- |
| Tier EBR entitlements (§2 ladder) | Strategic 4/yr · Enterprise 2/yr · Growth 1/yr · Scale 0 | Library default, derived from the §3 hour costs | — | `[P]` |
| Accounts per CSM | *No neutral published benchmark — figure deliberately not carried* | — | — | — |
| ARR per CSM | *No neutral published benchmark — figure deliberately not carried* | — | — | — |
| Build capacity bottom-up from touchpoint counts; two-thirds of the week to customers | 2/3 | Practitioner convention; cf. Operating Rule R13 | — | `[P]` |
| GRR/NRR rise monotonically with ACV | — | Benchmarkit (CY2024, N=225) and SaaS Capital (2025) | 2025 | `[M]` |
| GRR 88% / NRR 101% median; GRR 92% under usage-based pricing | as stated | Benchmarkit 2025 SaaS Performance Metrics, CY2024 | 2025 | `[M]` |
| Tech-touch content refresh cadence | Quarterly | Practitioner convention for this library | — | `[P]` |
| Notice periods cluster at 30/60/90 days; 30 modal, 60 common in negotiated enterprise | as stated | Practitioner | — | `[P]` |
| Renewal-clock windows (T−270 → T−0) | as stated | Practitioner operating cadence | — | `[P]` |
| Silence thresholds by segment | ENT 45 d · MM 60–90 d · SMB/tech-touch 120 d | Practitioner | — | `[P]` |
| Tier annual-hour costs and plannable book sizes (§3) | as stated | Derived from `play-durations.md` `[P]` × `capacity-model.md` | — | `[P]`, derived |
| Pooled queue SLAs | as stated | Practitioner | — | `[P]` |

**Label key:** `[M]` measured benchmark with a named neutral study · `[P]` practitioner rule of
thumb, no published measurement · `[A]` academic.
