# Coverage Models

> Five ways to cover a customer, what each one can and cannot deliver, what it costs per account per
> year, and the specific way each one fails. Read before binding a model to a segment, and again
> whenever someone proposes moving a tier to "digital" to save money.
>
> Evidence labels: `[M]` measured with a named study · `[V]` vendor or first-party operating model ·
> `[P]` practitioner convention · `[A]` academic.

**Contents**
1. [Model and segment are different axes](#1-model-and-segment-are-different-axes)
2. [Cost per account per year — the derivation](#2-cost-per-account-per-year)
3. [Named CSM](#3-named-csm)
4. [Pooled](#4-pooled)
5. [Tech-touch / digital](#5-tech-touch--digital)
6. [The six conditions for a real tech-touch programme](#6-the-six-conditions)
7. [Partner-led](#7-partner-led)
8. [Hybrid](#8-hybrid)
9. [Promotion and demotion between models](#9-promotion-and-demotion)
10. [Telling the customer](#10-telling-the-customer)
11. [Anti-patterns](#11-anti-patterns)
12. [Evidence register](#12-evidence-register)

---

## 1. Model and segment are different axes

| Axis | What it is | Set by |
| --- | --- | --- |
| **Segment** | Where the account sits on the revenue, potential, complexity and strategic spectrum | The boundary rules in `segmentation.md` |
| **Coverage model** | How much human attention the company has **funded** for it | The CS budget and headcount |

An Enterprise-segment account on a pooled model is not a contradiction. It is a funding decision,
and it must be visible everywhere — in the CRM, in the queue, in the forecast — so nobody promises
enterprise service on a pooled budget. Where segment and model disagree without a written decision,
that is the **mis-modelled** gap type in the skill's Step 7, and it is where most broken promises
originate.

GitLab's public handbook is a useful first-party reference for the shape: paid Success Tiers with a
designated named resource, alongside a pooled Customer Success Engineer model delivered through
webinars, hands-on labs, office hours and on-demand engagements, plus a **documented process for
transitioning an account from dedicated CSM coverage to the pooled tier** `[V — first-party public
operating model, 2026]`. The transition being *documented* is the part worth copying.

---

## 2. Cost per account per year

Every model costs hours; hours cost money. One derivation, used everywhere.

```
Loaded annual cost per CSM   C = OTE × loading factor
Effective customer hours     H = 1,065 per FTE per year        (capacity-math.md §1)
Loaded cost per customer hour c = C ÷ H
Cost per account per year      = hours per account per year × c
Cost-to-serve as % of ARR      = that ÷ account ARR
```

**Worked with published inputs.** RepVue's self-reported US panel puts the CSM median at **$105,000
base and $140,000 OTE as of August 2026** `[M — self-reported panel; treat as indicative, not a
survey with disclosed methodology]`. At a loading factor of 1.30 `[P]` for employer tax, benefits,
tooling, workspace and management overhead:

```
C = 140,000 × 1.30 = $182,000
c = 182,000 ÷ 1,065 ≈ $171 per customer-facing hour
```

**Every hour of CSM time costs about $171.** That single number is the most useful output of this
file, because it converts every cadence argument into a spend argument:

| Motion | Hours `[P]` | Cost |
| --- | --- | --- |
| Async data-backed check-in | 0.5 | $86 |
| 30-minute cadence call | 1.25 | $214 |
| Written value snapshot | 1.25 | $214 |
| Mid-market renewal conversation | 3.0 | $513 |
| Live executive business review | 8.0 | $1,368 |
| Escalation, first week | 4.5 | $770 |

Durations from `../../book-of-business-triage/references/play-durations.md`. Substitute your own
comp and loading factor before quoting any of these externally.

**Cost per account per year, by model** — using this library's default hour profiles:

| Model | Hours/account/yr `[P]` | Cost/account/yr | Affordable above (at k = 15% of an 81% gross margin) |
| --- | --- | --- | --- |
| Named, enterprise profile (complexity ×1.30) | 106.2 | $18,160 | ~$149,000 ARR |
| Named, mid-market profile (complexity ×1.20) | 50.7 | $8,670 | ~$71,000 ARR |
| Named, thin (Growth profile) | 24.1 | $4,120 | ~$34,000 ARR |
| Pooled | 4.1 | $700 | ~$5,800 ARR |
| Tech-touch (human hours only; programme cost is separate) | 0.4 | $68 | ~$560 ARR |

`A_min = (h × c) ÷ (k × g)` — see `segmentation.md` §3. Hour profiles from `capacity-math.md` §5
and §7; gross margin 81% `[Benchmarkit 2025, CY2024 · M]`. **These are the boundary candidates.**
They are derived from your inputs, not imported, which is the whole point — and note what the table
says about the mid-market named profile: at $71,000, the affordability floor sits well above a
typical mid-market ACV, which is exactly the finding that forces a real coverage decision.

**Sanity bound, not a target.** SaaS Capital's 2026 spending benchmarks (survey March 2026, 1,000+
private B2B SaaS) put CS + Support at a **9% of ARR median**, rising to 10% at $3–5M ARR, with
equity-backed companies spending about twice bootstrapped ones `[M]`. If your blended coverage cost
lands far above that, the mix is wrong somewhere — usually named coverage extending too far down.

---

## 3. Named CSM

| | |
| --- | --- |
| **Delivers** | Accountability with a face · context that compounds across quarters · executive relationships · proactive risk work that requires knowing what normal looks like for this account · negotiation credibility |
| **Structurally cannot deliver** | Coverage at volume · resilience to attrition · consistency across reps · anything at a cost below roughly $3,000 per account per year |
| **Staffing** | 1 CSM : book size from `capacity-math.md` §7. Hours dominated by scheduled motions |
| **Failure mode** | **Key-person dependency.** The entire relationship, and most of the knowledge, lives in one person's head. A resignation is an amnesia event for every account in the book |
| **Detect the failure with** | Share of accounts where a single CSM is the only internal person with a logged interaction in 180 days. Above ~60% you are one resignation away from a bad quarter `[P]` |
| **Mitigate with** | A second internal contact on every account above a stated ARR · handover packs maintained continuously, not written at exit (`segmentation.md` §7) · manager-level relationships on the top decile |

**Why the evidence supports named coverage where it is affordable.** The Customer Revenue Leadership
Study (Pavilion / 6sense, ~800 customer and post-sales leaders, October 2025) found that the presence
of a fuller post-sale role set — enablement, CSM, support and account management — correlates with
higher NRR, roughly 98–99% versus 90–94% where roles are missing `[M]`. Read it as correlational:
companies large enough to staff four post-sale roles differ in many other ways too. It supports "do
not strip roles casually"; it does not price a hire. That is what `headcount-case.md` is for.

---

## 4. Pooled

| | |
| --- | --- |
| **Delivers** | Responsiveness at volume · absorption of demand spikes · holiday and attrition resilience · consistent handling of common requests · a lower cost per account by roughly an order of magnitude |
| **Structurally cannot deliver** | Accumulated context · executive relationships · proactive multithreading · a negotiation · anything that depends on noticing what changed since last quarter |
| **Staffing** | A queue with a stated SLA per request class, staffed to the arrival rate, not to an account count |
| **Failure mode** | **Silent abandonment.** Customers do not complain about the queue; they stop using it, then stop engaging, then leave |
| **Detect the failure with** | **Inbound requests per account per quarter**, trended. Falling inbound after a move to pooled is the signal. Queue time looks fine precisely because the people who would have waited stopped arriving |

**The pooling caveat that most CS teams get wrong.** The operations-research default is that pooling
beats dedicated queues, because a pooled server never idles while another has a backlog. Sunar, Tu &
Ziya (*Pooled vs. Dedicated Queues when Customers Are Delay-Sensitive*, **Management Science** 67(6),
2021) show this breaks when customers *choose whether to join*: pooling can strictly reduce welfare,
the loss can **grow with system size** rather than shrink, and their numerical study finds welfare
and consumer-surplus reductions exceeding 95% in the worst regions `[A]`. The mechanism is exactly
CS's problem — a customer facing a queue with an uncertain wait does not wait, they disengage.

Three design consequences:

1. **Publish a first-response SLA per request class and hold it.** Certainty about the wait is what
   keeps people joining the queue. An unstated SLA is the worst configuration.
2. **Do not pool heterogeneous work.** A queue mixing five-minute password questions with two-week
   integration problems produces unpredictable waits for everyone. Separate the classes.
3. **Instrument arrivals, not just service.** Arrival rate per account is your abandonment detector.

**Running a pooled book properly:**

| Element | Requirement |
| --- | --- |
| Request classes | Named, each with an SLA — e.g. `how-do-I` 4h · `broken` 2h · `commercial` 1 business day · `onboarding` scheduled |
| Written handover on every item | Anyone picking up the next contact must not restart the conversation. This is the pool's substitute for memory |
| Account notes at the account, not the ticket | Context that survives the ticket closing |
| Escalation ladder to a named human | Any account crossing a risk threshold gets a person, temporarily, by rule |
| Proactive sweep budget | Explicit hours for outbound; without a ring-fence, inbound consumes 100% of the pool |
| Cycle-time arithmetic published | `accounts per CSM ÷ (sweep hours ÷ hours per touch)` = weeks per full sweep. Promise that cadence, never a better one |

---

## 5. Tech-touch / digital

| | |
| --- | --- |
| **Delivers** | Consistency · scale with no marginal cost per account · measurable iteration (you can actually A/B a lifecycle email; you cannot A/B a CSM) · 24/7 availability · a floor of service for accounts that would otherwise get nothing |
| **Structurally cannot deliver** | Anything requiring a relationship, a judgement call, a negotiation, or the discovery of a problem the customer has not articulated |
| **Cost** | Programme cost (content, tooling, ops FTE), largely fixed; near-zero marginal cost per account. Budget it as a **programme**, not as a per-account line |
| **Failure mode** | **Euphemism.** "Tech-touch" is what a coverage decision gets called when nobody wants to write "uncovered" on the slide |
| **Detect the failure with** | The six conditions below. Fail any one and the accounts are uncovered — put them in the gap table with their ARR |

---

## 6. The six conditions

| # | Condition | Concretely | Fails as |
| --- | --- | --- | --- |
| 1 | **Named owner** | A person whose job description contains this programme, with time allocated | "The CS team owns it" — meaning nobody does |
| 2 | **Dated journey** | A journey map with content assets, each carrying an author, a last-reviewed date and a next-review date | A sequence written eighteen months ago that references a deprecated UI |
| 3 | **Trigger → action inventory** | Every trigger written as a computable condition over `usage_daily`, `ticket`, `invoice` and `subscription`, with the action, the suppression rules and the owner | Broadcast sends on a calendar, which is a newsletter, not coverage |
| 4 | **Exception queue with an SLA** | A human works the accounts the automation flags, to a stated response time | Triggers that fire into a dashboard nobody opens |
| 5 | **Outcomes reported like a book** | Segment GRR, activation rate, expansion ARR, reported monthly next to the named tiers | Open and click rates. Nobody renewed because of an open rate |
| 6 | **Budget line** | Content production, tooling, ops hours, with a number | A programme funded from goodwill degrades to nothing within two quarters |

**The switch-off test.** If you turned the programme off, would any measurable thing change within a
quarter? If the honest answer is no, those accounts are uncovered. Say so in the gap table with the
ARR attached — that sentence is what funds the fix.

**Build sequence** — in this order, because each step depends on the last:

| Order | Step | Exit criterion |
| --- | --- | --- |
| 1 | Define the activation event for the segment (`cs-context` §5) | One computable event, agreed with product |
| 2 | Instrument it and baseline the current activation rate | A number with a date |
| 3 | Build the onboarding journey to that event only | Activation rate moves, measured against the baseline cohort |
| 4 | Add the risk triggers and the exception queue | Median time from trigger to human contact, under SLA |
| 5 | Add the renewal journey, anchored on the **opt-out deadline** | Renewal notices land before the notice window, not before the renewal date |
| 6 | Add expansion triggers | Qualified expansion conversations per quarter |

Doing 6 before 3 is the standard failure. Expansion automation on top of unactivated accounts sells
to people who have not yet succeeded, and it reads exactly as it is.

---

## 7. Partner-led

| | |
| --- | --- |
| **Delivers** | Local presence, language and time zone · vertical or implementation depth you do not staff · reach into markets without headcount · a lower cost of coverage per account |
| **Structurally cannot deliver** | Direct signal. You see the partner's account of the customer, filtered by the partner's commercial interest |
| **Failure mode** | **Signal blindness.** Usage, tickets and sentiment reach you late or not at all, and churn arrives as news rather than as a trend |
| **Detect the failure with** | Share of partner-covered accounts where you hold direct product telemetry and a named end-customer contact. Below ~50% you are not covering those accounts, the partner is `[P]` |
| **Non-negotiables** | Direct product telemetry for every end customer · at least one named contact you may email · a quarterly joint review with the partner using your data · renewal notice obligations flowing to you, not only to the partner · an explicit escalation path that bypasses the partner when severity warrants |

Model partner-led accounts in the coverage waterfall as **their own row**, never folded into
"covered". They are covered by someone whose incentives you do not control.

---

## 8. Hybrid

Named for the relationship, pooled or digital for volume work. The right answer for most mid-market
books and almost always mis-implemented.

| Requirement | Why |
| --- | --- |
| **Two hour budgets, split explicitly** (e.g. 60% named / 40% pooled) | Without a written split, the named accounts consume the pooled hours by the second week and the tail rots |
| **A written boundary of what the pool handles** | Ambiguity resolves toward the named CSM every time |
| **One customer-facing entry point** | The customer should not have to know your operating model to get help |
| **Separate measurement** | Report named-tier and pooled-tier outcomes separately or you cannot tell which half is failing |

**Failure mode:** the named side quietly eats the pooled side's hours. Detect it by comparing logged
interaction hours against the declared split, monthly.

---

## 9. Promotion and demotion

| Direction | Trigger | Guardrail |
| --- | --- | --- |
| **Digital → pooled** | Crosses the pooled ARR floor for two quarters, or opens a qualified expansion opportunity | Capacity in the pool must exist; adding accounts to a pool at capacity degrades everyone |
| **Pooled → named** | Crosses the named floor for two quarters, or a contract event, or a strategic grant | Named capacity must exist, or the promotion is a promise you cannot keep |
| **Named → pooled** | Two quarters below the floor, **and** no renewal inside 180 days, **and** no open escalation | **Never inside the opt-out window.** Reducing service while they are deciding is an avoidable loss |
| **Any → temporary named** | Any account entering a risk band above the escalation threshold | Time-boxed with an explicit exit date; otherwise the exception becomes the model |

Cap total movement at 15% of any tier per quarter `[P]`, and never move the same account twice in
twelve months.

---

## 10. Telling the customer

A coverage change is one of the few internal decisions a customer directly experiences. The
disclosure firewall in `../../cs-context/references/customer-voice.md` applies at full strength.

**Never appears in customer text, in any wording:** tier, book, pool, tech-touch, digital-touch,
coverage model, cost to serve, ARR, "your segment", "your account no longer qualifies", or any
reason grounded in what they spend.

| Internal | What the customer gets |
| --- | --- |
| "Moving Northwind to pooled coverage" | The new route to help, the response time attached to it, and what stays with a named person |
| "Below the named-CSM ARR floor" | *(never — the economics are not translatable)* |
| "Reassignment for territory balance" | "Sam is taking this on and here is why they are well matched" — with the outgoing CSM saying it, live |
| "Reducing EBR entitlement from 4 to 2" | The two dates, booked, plus the written summary that fills the gap |

Three rules that decide whether this lands:

1. **Lead with what improves.** There is almost always something real — faster first response, cover
   during leave, specialists on product questions. If there is genuinely nothing, do not invent it.
2. **Name what stays with a human.** The renewal, the escalation path, the specific project.
3. **Do not dress a reduction as an upgrade.** Customers recognise it instantly, and the credibility
   cost exceeds whatever the coverage change saved.

Send-ready blocks for both cases: `../assets/coverage-change-note.md`.

---

## 11. Anti-patterns

| Anti-pattern | Correction |
| --- | --- |
| "Tech-touch" used to mean no coverage | Score the six conditions; if it fails, report those accounts as uncovered with their ARR |
| Moving a tier to pooled to save money without pricing the retention risk | Estimate the GRR cost in basis points, state the basis, and put it in the options table |
| Pooling heterogeneous work into one queue | Separate request classes with their own SLAs; mixed queues produce unpredictable waits |
| Measuring a pool on queue time only | Track inbound requests per account — abandonment shows up in arrivals, not in service time |
| A hybrid book with one hour budget | Split line C explicitly and measure both halves |
| Partner-covered accounts counted as covered | Their own row in the waterfall, plus direct telemetry and a named contact |
| Demoting an account inside its opt-out window | Freeze coverage changes until the renewal closes |
| Launching expansion automation before activation automation | Build the journey to the activation event first |
| Announcing a coverage change by naming the tier | Lead with the new route to help and what improves; never name the economics |
| Reporting a digital programme on open and click rates | Report segment GRR, activation rate and expansion, next to the named tiers |
| Promoting accounts into a named tier that has no capacity | Check capacity before promoting; an unstaffed promise is worse than the honest tier |

---

## 12. Evidence register

| Claim | Value | Source | Year | Label |
| --- | --- | --- | --- | --- |
| Pooling can strictly reduce welfare when customers are delay-sensitive and choose whether to join; loss can grow with system size; >95% welfare reduction in the worst numerical regions | as stated | Sunar, Tu & Ziya, *Pooled vs. Dedicated Queues when Customers Are Delay-Sensitive*, Management Science 67(6) | 2021 | `[A]` |
| Fuller post-sale role coverage correlates with higher NRR (≈98–99% vs 90–94%) | as stated | Customer Revenue Leadership Study — Pavilion / 6sense, ~800 customer and post-sales leaders | Oct 2025 | `[M]`, correlational |
| CS + Support spend | 9% of ARR median; 10% at $3–5M ARR; equity-backed ≈2× bootstrapped | SaaS Capital, *2026 Spending Benchmarks*, survey Mar 2026, 1,000+ companies | 2026 | `[M]` |
| Subscription gross margin | 81% median | Benchmarkit 2025 SaaS Performance Metrics, CY2024, N=76 | 2025 | `[M]` |
| CSM compensation | $105,000 median base · $140,000 median OTE, US | RepVue self-reported panel | Aug 2026 | `[M]`, self-reported; no disclosed sampling method |
| Named and pooled tiers with a documented dedicated-to-pooled transition process; pooled delivery via webinars, labs, office hours, on-demand | first-party operating model | GitLab public handbook — Success Tiers and CSM → pooled CSE transition | 2026 | `[V]` |
| Loading factor 1.25–1.40; hours-per-account profiles; single-threaded-CSM threshold ~60%; partner telemetry floor ~50%; move cap 15%/quarter | as stated | Practitioner convention used by this library | — | `[P]` |
| Play durations | see file | `../../book-of-business-triage/references/play-durations.md` | — | `[P]` |

**Deliberately absent:** accounts-per-CSM and ARR-per-CSM ranges by touch model. Every reachable
version traces to a customer-success-platform vendor summarising its own installed base, undated and
without a disclosed sample. Derive the number from `capacity-math.md` instead.
