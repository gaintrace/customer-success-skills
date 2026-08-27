# The Expansion Signal Library

> The master taxonomy `expansion-finder` walks on every sweep. Every signal is specified with
> its source system and field, the computation, the threshold, what it implies, the motion it
> triggers, the typical deal-size effect, and its decay window. A signal missing any of those
> is an anecdote, not a signal.

**Contents**
1. [How to read a row](#1-how-to-read-a-row)
2. [Family 1 — Product usage & adoption](#2-family-1--product-usage--adoption)
3. [Family 2 — Commercial & contract](#3-family-2--commercial--contract)
4. [Family 3 — Relationship & engagement](#4-family-3--relationship--engagement)
5. [Family 4 — Support & reliability](#5-family-4--support--reliability)
6. [Family 5 — Sentiment & VoC](#6-family-5--sentiment--voc)
7. [Family 6 — Billing & payment](#7-family-6--billing--payment)
8. [Family 7 — Firmographic & external](#8-family-7--firmographic--external)
9. [Signal decay windows](#9-signal-decay-windows)
10. [Land-and-expand motion catalogue](#10-land-and-expand-motion-catalogue)
11. [Instrumentation contract](#11-instrumentation-contract)
12. [Evidence register](#12-evidence-register)

---

## 1. How to read a row

Field names use the normalised schema in `../../cs-context/references/normalized-schema.md`.
Where a source system is named, it is an example of where that field usually lives — map it
to your own stack in `cs-context` §9.

**Tier** is the intent weight from `../SKILL.md` Step 2: T1 declared · T2 constraint hit · T3
constraint approaching · T4 structural growth · T5 disposition · T6 exogenous.

**Deal-size effect** columns are a *sizing convention* derived from the arithmetic in
`sizing-models.md`. They are not measured industry statistics. Replace them with your own
closed-won distribution once you have ≥30 closed expansion deals per motion.

**Combination rule.** One T5 or T6 signal is never an opportunity on its own. Require one
T1/T2/T3, or two independent T4 signals plus one T5.

---

## 2. Family 1 — Product usage & adoption

### 2.1 The three sweeps everyone else misses

These three run before the signal table below, because each of them changes what the table
means. All three are cheap to compute and are the ones absent from most expansion programs.

| Sweep | Detection rule | Why it matters |
| --- | --- | --- |
| **Blocked people, not utilisation percentages** | `usage_event.event_name IN ('seat_limit_reached','invite_blocked')` in the last 30d, grouped by `properties.attempted_user_email` — count **distinct people** and **total attempts** | "94% utilised" is a ratio; "eighteen named people were denied access forty-one times" is a business problem the customer owns and can verify in their own admin console. Most companies never instrument this event, which is why it is the highest-yield and most-missed signal in the taxonomy |
| **Buying-team spread, not aggregate growth** | A new `workspace_created`, a new `properties.department` or job function among active users, or a new email domain on the account | A second budget holder has appeared inside the account. That is a land motion, not an add-on, and it is invisible in an account-level usage chart |
| **Already-entitled but unused** | `subscription.plan` entitlements ∖ features with any use in 90d | Pitching a capability they already pay for and have never adopted is the fastest way to lose an admin's credibility, and it converts an adoption problem into a commercial one |


```
Licence utilisation      = distinct active_users_30d ÷ subscription.seats_purchased
   active user          := ≥1 core_action in the window, NOT merely a login
   window               := 30 days rolling; 90 days for low-frequency or seasonal products
Provisioning gap         = seats_purchased − seats_provisioned          (contracted shelfware)
Shelfware gap            = seats_provisioned − active_users_30d         (deployed shelfware)
Headroom                 = seats_purchased − active_users_30d
Runway (months)          = headroom ÷ trailing-3-month net new active users per month
Adoption breadth         = usage_daily.feature_breadth ÷ features_in_plan
Utilisation slope        = 30d normalised slope of distinct active users
```

| Utilisation band | Read | What runs | Expansion? |
| --- | --- | --- | --- |
| **<50%** | Shelfware. Their SaaS-management tool is showing them the same number | Adoption recovery; expect a downgrade conversation at renewal | **Prohibited — hard block** |
| 50–70% | Under-adopted, value not proven | Adoption play only | No |
| 70–85% | Healthy steady state for mature B2B SaaS | Nothing | No |
| **≥85%** with positive slope | Watchlist | Model the runway; seed the seat conversation at the next scheduled touch | T3 |
| **≥90%** | Opportunity | Open a sized opportunity | T3 |
| **≥100% sustained 90d** | Over-consumption against entitlement — a contract fact read off your own provisioning data, not a benchmark | EBR framing **or** true-up notice — never lead with the true-up | T2 |

| # | Signal (threshold) | Source · field | Tier | Implies | Motion | Deal-size effect | Timing & decay |
| --- | --- | --- | --- | --- | --- | --- | --- |
| U1 | Licence utilisation ≥85% and 30d slope >0 | Product analytics `usage_daily.active_users` ÷ `subscription.seats_purchased` | T3 | The pool is filling on a trajectory | Runway model → seat conversation at next touch | Δ seats at renewal × `p_eff`; commonly +10–25% of account ARR | Raise ≥60d before projected exhaustion. Re-evaluate weekly on a 30d rolling window |
| U2 | Licence utilisation ≥100% | Same, or entitlement service `seats_in_use > seats_licensed` | T2 | Contractual over-consumption | Disclose within 5 business days with the value it produced; then EBR or true-up | Overage seats × `p_eff`; commonly +20–60% of ARR | Within 5 business days of detection — disclose before the invoice does |
| U3 | **Seat waitlist / access-denied**: ≥3 distinct blocked would-be users in 30d | Auth/provisioning logs `usage_event.event_name IN ('seat_limit_reached','invite_blocked')` with `properties.attempted_user_email` | T2 | Named individuals are being blocked from work right now | Send the **list of blocked people** with per-user value math to the admin | Blocked users × 1.2 buffer × `p_eff` | **14 days.** Intent decays fast; blocked users build workarounds |
| U4 | **Admin invite burst**: invites in 7d > 2× the trailing 8-week weekly mean | `usage_event.event_name='user_invited'` grouped by `account_id`, `properties.inviter_id` | T4 | A rollout or a new team is starting | Rollout-support play plus a proactive headroom check | Predicts U1/U3 by 2–6 weeks; not sized on its own | Act on the burst, not on the eventual cap hit |
| U5 | Metered usage ≥80% of included allotment with <60d left in the period | `subscription.usage_consumed` ÷ `subscription.usage_entitlement` | T3 | Will breach the allotment inside the period | Right-sizing: model overage vs tier delta honestly (`sizing-models.md` §4) | Tier delta, or a committed-volume uplift | Fire at 80% of allotment, or projected breach −45d, whichever is first |
| U6 | Record / storage / contact / MAU count ≥90% of a plan cap | Product counters vs `plan.limit_*` | T3 | Data-volume growth that will not reverse | Volume-tier upgrade | Proportional to the cap step | ≥90% alert; ≥98% open the opportunity |
| U7 | **Feature-gate hit**: ≥2 distinct users or ≥3 attempts on a locked capability in 30d | `usage_event.event_name IN ('paywall_viewed','feature_locked_clicked')` with `properties.feature_key` | T2 | Declared demand for a specific gated capability | Upsell **that exact feature**; in-app self-serve below the human-touch ARR threshold, CSM above it | Tier delta or add-on SKU price | **14 days** |
| U8 | Hard rate-limit / HTTP 429 ≥1% of API calls over 7d | API gateway logs; `usage_daily.api_calls` | T2 | An engineering project on their side is being throttled | Solutions-engineer conversation; rate-limit package or tier | Tier upgrade, commonly 30–60% of current ARR | **7 days** — engineering teams re-architect around limits quickly |
| U9 | **New workspace / team / org unit created** with ≥3 active users | `usage_event.event_name IN ('workspace_created','team_created')`; `account.parent_account_id` | T4 | Another budget-holding unit is adopting | Mini land motion inside the account, to the new unit's owner | Often a second contract, not an add-on | Within 21d of the workspace reaching 3 active users |
| U10 | **Adoption breadth** ≥60% of the core feature set in 90d, and rising for 2 consecutive months | `usage_daily.feature_breadth` ÷ features in plan | T4 | Embedded, not experimental | Cross-sell adjacency (see C4/C5) | Cross-sell SKU, commonly 25–50% of current ARR | Only after the threshold has held for two months |
| U11 | **Power-user emergence**: ≥3 users in the top decile of their segment cohort, sustained 60d | Percentile rank of per-user `core_actions` within the segment | T4 | Internal advocates exist; the beachhead is mature | Recruit power users to carry the internal business case | Enables the deal; does not size it | Approach power users *before* the buyer |
| U12 | **Integration added** (any new connector authorised) | `usage_daily.integrations_active` step change; OAuth grant log | T4 | You are being wired into a system of record; switching cost rising | Cross-sell the SKU that shares the same data | Cross-sell; also raises win probability on every other motion | Act 2–4 weeks after connection, once data is flowing |
| U13 | Integration count crosses 4 | Same | T4 | Deep embedding | Platform-tier conversation | Platform-tier delta | On crossing, not before |
| U14 | SSO / SCIM / directory sync enabled | Auth config; `usage_event.event_name='sso_enabled'` | T4 | IT has sanctioned you; auto-provisioning will grow seats | Enterprise-tier upsell (SSO is frequently already the tier gate); re-baseline the seat forecast upward | Enterprise tier delta | On enablement |
| U15 | Premium-module trial activated and used ≥3 sessions | `usage_event.event_name='trial_started'` with `properties.feature_key` | T2 | A real evaluation, not curiosity | Trial-conversion play with written success criteria | Add-on SKU price | Set the decision date at trial **start**, not at trial end |
| U16 | Automation / workflow objects created ≥10 in 60d, sustained ≥2 months | `usage_daily.admin_actions`; product `workflow_created` | T4 | They are building on you | Premium automation tier or higher execution limits | Tier or execution-volume SKU | On the second sustained month |
| U17 | Second use case or second team's workflow live | Product workspace/project taxonomy | T4 | Horizontal spread inside the account | Next-department motion (§10) | Roughly linear in seats added | On first evidence |

**Integration → retention, for the business case.** ProfitWell's *Integrations Benchmark*
(~500,000 companies) reports 10–15% higher retention for products with ≥1 integration and
18–22% for ≥4 — measured, vendor-run. Crossbeam (n=526, survey) reports users with
integrations are 58% less likely to churn, and RollWorks reports 4+ integrations 35% less
likely to churn than 1; both are single-vendor claims. Quote the ProfitWell figure; treat the
others as directional.

---

## 3. Family 2 — Commercial & contract

```
Whitespace ARR (account)  = Σ over SKUs not owned [ list_price(SKU, size band) × eligibility ]
Whitespace penetration    = owned SKU ARR ÷ (owned SKU ARR + whitespace ARR)
Effective unit price      = account.arr ÷ contracted units
Opt-out deadline          = subscription.renewal_date − subscription.notice_period_days
Co-term stub              = target_end_date − current_end_date, prorated at p_eff
```

| # | Signal (threshold) | Source · field | Tier | Implies | Motion | Deal-size effect | Timing & decay |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C1 | **Upgrade / pricing-page visit** by a known contact at an existing customer | Web analytics + first-party identity joined to `account_id`; `contact.email` | T1 | Active self-evaluation, possibly pre-negotiation | Route to the account owner. Approach as *"something seems to have changed on your side — what's driving the timing?"* — **never** name the page visit aloud | Tier delta | **7 days** |
| C2 | Enterprise-only documentation views spike | Docs analytics `page_path` under gated sections | T3 | Technical evaluation of a higher tier | Solutions-engineer conversation | Tier delta | 7–14 days |
| C3 | **Procurement or legal engages unprompted** (MSA amendment, order-form request) | CLM `request_type`; `interaction.type='email'` with procurement participants | T1 | The buying process has already started | Accelerate; do not re-discover requirements | Whatever they asked for | Same day |
| C4 | **Whitespace penetration <50%** on a Secure-band account | Product-ownership matrix (`subscription` rows per product) × SKU catalogue | T4 | Portfolio gap on a healthy account | Cross-sell prioritised by adjacency to the adopted use case | Σ eligible SKU list price × expected attach | Anchor to a scheduled business review, never a cold reach |
| C5 | **Peer-benchmark gap**: adoption of SKU X below the cohort median where ≥60% of the cohort owns X | Cohort table computed from your own base — same vertical, ±1 ARR band, ±1 tenure band, **n ≥ 20** | T4 | An earned "customers like you run X" recommendation | Peer-benchmark narrative delivered inside the QBR with the anonymised cohort stat | SKU list price × P(attach) | Refresh quarterly. Never publish a cohort stat that could identify one customer |
| C6 | Adjacency lift: accounts owning {A,B} own C at ≥2× the base rate | Market-basket rules over your own ownership matrix (support, confidence, lift) | T4 | Statistically grounded next-best-offer | Ranked next-best-offer | SKU price × P(attach), capped at 0.60 for a first-time SKU | Refresh the model quarterly |
| C7 | **Co-term opportunity**: ≥2 active `subscription` rows on one account with different `end_date` | `subscription.end_date` grouped by `account_id` | T4 | Administrative friction they feel every year | Co-term proposal: move both to the later end date, prorate the stub, consolidate to one paper | Consolidation can cross a volume tier — that is a **give**, not a get. The get is term length and predictability | Propose at the **earlier** of the two renewal dates |
| C8 | **Ramp maturation**: a contracted quantity or price step lands next period | CPQ ramp schedule; `subscription.is_ramped=true` | T4 | A pre-agreed increase is about to arrive | **Pre-brief 90 days out.** An unbriefed ramp step is the most common self-inflicted renewal surprise | Already booked — protect it, do not re-sell it | 90 days before the step |
| C9 | **Discount expiry** | `subscription.discount_pct`, `subscription.discount_expires` | T4 | Effective price rises with no added value | Value-recap sequence starting 120d out so the increase lands against demonstrated ROI | Protects existing ARR | Begin at 120d. Never surface it first at 30d |
| C10 | **Multi-year uplift / escalator due** | `subscription.uplift_pct`, CPI-linked clause | T4 | Contractual increase that still has to be justified | Same as C9. Justify in this order: outcomes in their metrics → roadmap shipped → usage growth → the clause → list movement | Market-standard negotiated escalators run 3–5%, often CPI-linked with a cap (contract-market guidance, practitioner convention, not a measured benchmark) | 120d out |
| C11 | Under-priced vs cohort: effective unit price in the bottom quartile of the segment | `account.arr` ÷ contracted units, percentiled within segment | T4 | Legacy pricing, margin leakage | Price correction **at renewal only**, paired with added value — never as a standalone increase | Effective-rate delta × units | At renewal only |
| C12 | Customer requests a longer term or a multi-year PO | Procurement communication; `opportunity.type='renewal'` notes | T1 | They want budget predictability | Trade term length for a capped escalator | Term extension; converts GRR risk into committed ARR | On request |
| C13 | Security review / vendor risk assessment initiated by the customer | Legal queue `questionnaire_received` | T1 | They are elevating you to a strategic vendor | Enterprise-agreement and multi-year motion | Multi-year + tier | Immediately |

**Co-terming is a customer-favourable concession.** Spend it to buy term length, a multi-year
commit, or an expansion attach. Granting it for free wastes the only currency the
administrative friction gave you.

---

## 4. Family 3 — Relationship & engagement

| # | Signal (threshold) | Source · field | Tier | Implies | Motion | Deal-size effect | Timing & decay |
| --- | --- | --- | --- | --- | --- | --- | --- |
| R1 | **Success-plan milestone verified complete** | CS platform milestone object; `interaction.commitments` closed | T5 | The beachhead is proven; the ascension model can advance | The upsell **pre-mapped to that milestone** (Lincoln Murphy's logical-expansion model: each Success Milestone carries its own next step, named at onboarding) | Pre-defined per milestone; forecastable bottom-up from milestone cohorts | Within **14 days** of verification — the momentum window. Verified, not merely marked done |
| R2 | **Champion promoted** or given wider scope | `contact.title` change; enrichment job-change feed | T4 | Your advocate now controls a bigger budget and a bigger population | Congratulate, then re-scope the success plan to their new remit. The expansion follows the remit | New population × `p_eff` | Within 30 days of the title change |
| R3 | **New department appears** among active users: ≥5 users from a new job function active for 30d | Enriched `contact.title` / department on product users | T4 | Horizontal spread past the original buying centre | Get introduced to the new department's owner. **Do not** ask the original champion to sell internally | New-department seat block | After 30 days of sustained activity |
| R4 | **New CxO or VP in the buying centre** | Enrichment; `contact.role='economic_buyer'` change | T6 | Budget authority changed and the agenda reset | 30-day new-exec play: value recap in their metrics, then their agenda | Neutral-to-positive if handled, negative if ignored | **Within 30 days of their start date** |
| R5 | Multithreading depth ≥4 distinct `customer_participants` in 90d, including an economic buyer | `interaction.customer_participants` | T5 | The relationship can carry a commercial conversation | Relationship readiness 1.00 in the ranking model | Raises win probability, does not size | Rolling 90 days |
| R6 | Exec sponsor met within the last 90 days | `interaction.type IN ('meeting','qbr')` with an `economic_buyer` participant | T5 | Permission exists for a business conversation | Precondition for the ask, not a trigger for it | Gate, not size | 90-day decay |
| R7 | Design-partner or product-council participation | Community platform join to `account_id` | T5 | Deep investment in your roadmap | Roadmap co-development → design-partner SKU | — | Ongoing |

---

## 5. Family 4 — Support & reliability

| # | Signal (threshold) | Source · field | Tier | Implies | Motion | Deal-size effect | Timing & decay |
| --- | --- | --- | --- | --- | --- | --- | --- |
| S1 | **Ticket requesting a capability that exists in a higher tier** | `ticket.type='feature_request'` with a tag mapped to a gated `feature_key` | T1 | Declared demand arriving through the wrong door | **Support must not sell.** Support tags → routes to CSM within 1 business day → CSM confirms the use case → opportunity. The support reply stays a support reply | Tier delta or add-on SKU | Route within 1 business day; CSM contact within 3 |
| S2 | Roadmap-portal request for a shipped-but-gated feature | Productboard/Canny request mapped to an entitlement | T1 | Same as S1, self-declared | Same routing | Same | Same |
| S3 | Volume of "how do I add users / raise the limit" admin tickets ≥3 in 60d | `ticket.type='question'` with an entitlement tag | T2 | The admin is hitting a boundary and asking politely | Route to the seat or limit conversation with the ticket IDs as evidence | Same as U3 | 30 days |
| S4 | Clean support posture: zero escalations, no SLA breach, no reopen in 90d | `ticket.sla_breached`, `ticket.reopened_count`, `ticket.type='escalation'` | T5 | No service-recovery memory in the way | Gate passes; proceed | Gate, not size | Rolling 90 days |

**The gating direction matters more than the sourcing direction here.** Family 4 produces
two T1 signals and one gate. The gate is the important part: an open escalation, an open P1,
or a Sev-1 closed inside 14 days blocks the motion outright — see `qualification.md` §2.

---

## 6. Family 5 — Sentiment & VoC

| # | Signal (threshold) | Source · field | Tier | Implies | Motion | Deal-size effect | Timing & decay |
| --- | --- | --- | --- | --- | --- | --- | --- |
| V1 | NPS promoter (9–10) from an economic buyer or admin | Survey → `contact.sentiment='advocate'`, response date | T5 | Favourable disposition **and** a permissioned moment | Advocacy ask first, expansion ask second — separated by ≥14 days | Win-rate multiplier, never a sizing input | Act within 7–14 days; expires at 90 |
| V2 | CSAT ≥4.5/5 on a substantive (non-trivial) ticket | `ticket.satisfaction` | T5 | A positive service memory | Re-engagement window | — | 7 days |
| V3 | Advocacy act: reference call, public review, case study, conference talk | Advocacy platform; CRM reference status | T5 | Public psychological commitment | Never ask for expansion in the same conversation as the advocacy ask | Raises win probability | Separate the two by ≥14 days |
| V4 | Referral submitted | Referral system, by `account_id` | T5 | Highest-order advocacy | Executive thank-you, then expansion 30–60 days later | — | ≥2 weeks of separation |
| V5 | Sustained Secure health for 2 consecutive quarters | `churn-risk` band history | T5 | Stability, not opportunity | Passes the gate at 1.00; combine with a constraint signal | Gate, not size | Quarterly |

**Do not treat NPS as a sizing input.** A promoter at 40% licence utilisation is a happy
under-adopter, not an expansion opportunity. CustomerGauge reports a 10-point NPS increase
correlating with 3.2% more upsell revenue and promoters expanding at 40% vs 15% for passives —
both vendor-reported, methodology not published. Use them as directional support for the
disposition gate, never as a benchmark quoted to a customer.

---

## 7. Family 6 — Billing & payment

| # | Signal (threshold) | Source · field | Tier | Implies | Motion | Deal-size effect | Timing & decay |
| --- | --- | --- | --- | --- | --- | --- | --- |
| B1 | **Overage incurred on ≥2 consecutive invoices** | `invoice` line items `type='overage'`, `amount>0` | T2 | Structural under-sizing, not a spike | Convert variable overage into a committed volume | See `sizing-models.md` §5 — usually *reduces* year-1 billings and raises committed ARR | Trigger on the **second** consecutive overage, never the first |
| B2 | Credit / token burn-down: projected exhaustion before period end | Metering ledger `credits_remaining`, `burn_rate_7d` | T3 | A consumption account will run dry mid-term | Top-up, or a higher commit with a committed-use discount | Top-up is incremental; commit is renewal-grade | Alert when `credits_remaining ÷ burn_rate_7d < 45 days` |
| B3 | `usage_consumed` ÷ `usage_entitlement` ≥ 0.80 with growth | `subscription.usage_consumed`, `subscription.usage_entitlement` | T3 | Will breach the allotment | Right-sizing with the indifference math shown | Tier delta | 45 days before projected breach |
| B4 | Clean payment posture: no failures in 180d, mean days-late ≤5 | `invoice.paid_at − invoice.due_at`, `invoice.payment_failures` | T5 | No commercial friction in the way of a larger line item | Gate passes | Gate, not size | Rolling 180 days |

**The true-up rule.** Over-consumption is disclosed within 5 business days of detection, with
the value it produced, and never for the first time on an invoice. A true-up ambush produces a
procurement escalation and costs more than the true-up recovers.

---

## 8. Family 7 — Firmographic & external

| # | Signal (threshold) | Source · field | Tier | Implies | Motion | Deal-size effect | Timing & decay |
| --- | --- | --- | --- | --- | --- | --- | --- |
| F1 | **Funding round announced** | Enrichment → CRM funding fields; news feed | T6 | The spending ceiling reset; hiring and tooling budget released | Growth-planning EBR: what their stack needs at 2× headcount | The largest exogenous multiplier; often unlocks a tier and a seat block together | **Open the conversation 30–90 days after the announcement, not day 1** — budget deploys with a one-to-two-quarter lag |
| F2 | **Headcount growth ≥10% in 90 days** | Enrichment `account.employee_count` time series | T6 | The seat denominator is growing | Pre-emptive seat forecast; propose a ramp instead of repeated true-ups | Seats scale with headcount in the relevant function | Re-baseline quarterly |
| F3 | **Hiring for roles in your product's category** | Job-posting feeds matched to a role taxonomy | T6 | The function you serve is being staffed | Onboard the new hire early — they become a champion or a re-evaluator | Correlates with seat and tier expansion | Contact within 30 days of the **hire's start date**, not the posting |
| F4 | **Customer acquires a company** | News/enrichment M&A event | T6 | A new population to serve — and a consolidation risk if the target runs a competitor | Consolidation play: standardise the merged entity on you; co-term the two contracts | Frequently the largest single expansion event | Within 30 days of the close announcement — standardisation decisions happen fast |
| F5 | **Customer is acquired** | Same | T6 | Bimodal: the parent standardises on you or off you | Immediate executive contact; assume displacement until proven otherwise | Bimodal — do not forecast it as expansion | Within 7 days |
| F6 | **New geography or subsidiary appears** — new country codes among users, a new domain under the same parent, or a data-residency/DPA request | User `locale`; `account.parent_account_id`; DPA request in the legal queue | T4 (T1 if a residency request) | Global rollout or M&A-driven expansion | Global-agreement motion; data-residency SKU; regional pricing alignment | Often the largest single expansion class | Immediately on a residency or DPA request — that is declared demand |
| F7 | Customer launches a product or enters a new market | Their newsroom, changelog, press | T6 | A new use case for your product | Use-case expansion | Cross-sell | Within 60 days |

---

## 9. Signal decay windows

A signal past its window is history, not intent. Print the age of every signal you cite.

| Signal class | Freshness window | Why |
| --- | --- | --- |
| Access-denied, feature-gate hit | 14 days | Intent is momentary; the customer routes around the block |
| Upgrade / pricing-page visit | 7 days | Web intent decays fastest of anything in the taxonomy |
| Rate-limit / 429 | 7 days | Engineering re-architects around limits quickly |
| Overage incurred | 30 days, or the next invoice | Tied to the billing cycle |
| Utilisation threshold | 30-day rolling, re-evaluated weekly | Smooths holidays and seasonality |
| Milestone completion, NPS promoter | 14 days to act; 90-day expiry | The momentum window |
| Champion promotion, new exec | 30 days | The agenda is being set now |
| Funding, M&A, headcount | 90–180 days | Budget deploys one to two quarters after the announcement |

---

## 10. Land-and-expand motion catalogue

| Motion | Trigger signals | Expansion vector | Sequence | Typical cycle |
| --- | --- | --- | --- | --- |
| **Seat densification** | U1, U3 | More seats, same team | Blocked-user list → value per user → add-on, co-termed | 7–21 days |
| **Next-department** | U9, R3 | New seat block, often a new use case | Champion introduction → new-owner discovery → mini-pilot → attach | 45–90 days |
| **Geographic / subsidiary** | F6, F4 | Regional contract or global agreement | Residency and compliance discovery → regional pilot → global MSA | 90–180 days |
| **Tier ascension** | U5, U6, U7, U8 | Same product, higher edition | Indifference math → trial of the gated capability → upgrade | 30–90 days |
| **Consumption commit** | B1, B2 | Variable spend → committed volume | Overage history → commit tier with true-forward → capped escalator | 30–60 days |
| **Cross-sell adjacency** | C4, C5, C6 + U10 breadth threshold | New SKU | Peer-benchmark narrative in the EBR → scoped pilot → attach | 60–180 days |
| **Platform consolidation** | U13, F4 | Displace point tools | TCO analysis against their current stack → phased migration | 120–270 days |
| **Multi-year / term extension** | C12, C13, F1 | Term, not units | Trade a capped escalator for term length | 60–120 days |
| **Self-serve in-product** | U7 on a low-ARR account | Tier or add-on | In-app prompt at the moment of the block; no human touch | Minutes–days |

Below the human-touch ARR threshold, every signal above maps to an automated motion — in-app
prompt, lifecycle email, in-product banner — rather than a CSM task, because the one-to-one
relationship does not exist to carry the ask.

---

## 11. Instrumentation contract

If these events are not emitted, most of this taxonomy cannot be operated. This is the
minimum. The first row is the highest-yield signal in the library and is almost always the
one that is missing.

| Event | Required properties | Enables |
| --- | --- | --- |
| `seat_limit_reached` / `invite_blocked` | `account_id`, `attempted_user_email`, `inviter_id`, `ts` | U3 |
| `user_invited` | `account_id`, `inviter_id`, `invitee_email`, `ts` | U4 |
| `paywall_viewed` / `feature_locked_clicked` | `account_id`, `user_id`, `feature_key`, `surface`, `ts` | U7 |
| `usage_meter_snapshot` (daily) | `account_id`, `meter_key`, `value`, `included_qty`, `ts` | U5, U6, B2, B3 |
| `overage_incurred` | `account_id`, `meter_key`, `qty`, `amount`, `invoice_id` | B1 |
| `rate_limited` | `account_id`, `endpoint`, `status=429`, `ts` | U8 |
| `workspace_created` / `team_created` | `account_id`, `creator_id`, `parent_id`, `ts` | U9 |
| `integration_connected` | `account_id`, `integration_key`, `connected_by`, `ts` | U12, U13 |
| `sso_enabled` / `scim_enabled` | `account_id`, `ts` | U14 |
| `milestone_completed` | `account_id`, `milestone_key`, `verified_by`, `ts` | R1 |
| Daily account rollup | `active_users_30d`, `seats_purchased`, `utilisation`, `feature_breadth_90d`, `integrations_active` | U1, U10 |

Persist these derived fields on the account so the sweep is a read, not a computation:
`seat_utilisation_30d` · `seat_utilisation_slope_30d` · `seat_headroom` ·
`seat_runway_months` · `blocked_users_60d` · `meter_pct_of_allotment` ·
`projected_breach_date` · `feature_breadth_pct_90d` · `power_user_count` ·
`integration_count` · `whitespace_arr` · `whitespace_penetration_pct` · `days_to_opt_out` ·
`health_gate_passed` · `last_value_artifact_date` · `last_expansion_ask_date`.

---

## 12. Evidence register

| Claim used in this file | Source | Year | Type |
| --- | --- | --- | --- |
| Expansion CAC $1.00 vs new-customer CAC $2.00; expansion = 40% of new ARR (median), 58% at $50–100M ARR, 67% >$100M (n=6); NRR 101%, GRR 88% | Benchmarkit / Pavilion, *2025 B2B SaaS Performance Metrics* (FY2024 data) | 2025 | **Measured** |
| ~60% of new ARR from existing customers above $50M ARR; 800+ respondents | High Alpha, *2025 SaaS Benchmarks Report* | 2025 | **Measured** |
| NRR by ACV band: <$5k 95% · $5–25k 98% · $25–50k 102% · $50–100k 107% · $100k+ 110% | SaaS Capital, *What Is a Good Retention Rate for a Private SaaS Company* | 2025 | **Measured** |
| NRR tiering: 100% good · 110% better · 120% best | Bessemer Venture Partners, *State of the Cloud* | 2023 | **Measured** |
| CAC ratio blended 1.2 / new 1.8 / expansion 0.6; NDR 109%; expansion 46% of new ARR | KeyBanc KBCM Private SaaS Survey | 2022 | **Measured**, dated |
| ≥1 integration → 10–15% higher retention; ≥4 → 18–22% (~500k companies) | ProfitWell Integrations Benchmark | — | Measured, vendor-run |
| Logical expansion, Success Milestones, ascension model, the quota anti-pattern | Lincoln Murphy, sixteenventures.com | — | Practitioner canon |
| Utilisation bands (<50 / 50–70 / 70–85 / ≥85 / ≥90), the whitespace method (purchased vs adopted, segmented by industry and ARR band, filtered by health), cohort n≥20, cooldown windows, CSM opportunity cap 5–8, propensity priors | Practitioner convention synthesised across CS platform practice | — | **Rule of thumb — not measured** |
| NPS → upsell correlation (10 points ≈ 3.2% more upsell revenue; promoters expand at 40% vs 15%) | CustomerGauge | — | Vendor-reported |

**Could not verify — do not cite:** "proactive predictive expansion outreach closes ~35%
higher than reactive"; "75% of B2B sales engagements originated from signal-based triggers";
Champify's champion-departure percentages (51% / 65% / 33%); "median NRR for usage-based
pricing ≈120%"; "12–30% of licence spend is shelfware". Each appears in vendor material with
no retrievable primary source.
