# Segmentation

> Segments exist for exactly one reason: to make coverage differ. A segmentation that does not
> change what a customer receives is a colour scheme with a budget line. This file is how to build
> one that survives a CFO reading it, and how to audit one that already exists.
>
> Evidence labels: `[M]` measured with a named study · `[V]` vendor or first-party operating model ·
> `[P]` practitioner convention, no published measurement · `[A]` academic.

**Contents**
1. [The only purpose](#1-the-only-purpose)
2. [The six dimensions](#2-the-six-dimensions)
3. [Setting the boundaries](#3-setting-the-boundaries)
4. [The composite score, and when to use it](#4-the-composite-score)
5. [The three tests, worked](#5-the-three-tests-worked)
6. [Migration and hysteresis](#6-migration-and-hysteresis)
7. [The handover pack](#7-the-handover-pack)
8. [The twelve audit tests](#8-the-twelve-audit-tests)
9. [Specialisation trade-offs](#9-specialisation-trade-offs)
10. [Anti-patterns](#10-anti-patterns)
11. [Evidence register](#11-evidence-register)

---

## 1. The only purpose

A segment is a promise about hours. On the worked profiles in `capacity-math.md`, Enterprise means
"this account gets about 106 hours a year"; Growth means "this one gets 24"; Scale means "four".
Everything else — the name, the colour, the slide — is packaging.

Three consequences follow, and every failure in this file traces back to ignoring one of them:

| Consequence | What it means in practice |
| --- | --- |
| **If two segments get the same hours, they are one segment** | Merge them. Two labels on one service level costs reporting complexity and buys nothing |
| **A boundary you cannot compute is not a boundary** | Every rule must be an expression over fields in `../../cs-context/references/normalized-schema.md` |
| **A segment you cannot fund is a lie** | If the hours implied by the entitlement exceed available capacity, the entitlement is aspirational and customers will experience it as broken promises |

The evidence for making ARR the *primary* axis is good and worth quoting when challenged: gross
revenue retention rises monotonically with ACV `[Benchmarkit 2025 SaaS Performance Metrics, CY2024
actuals · M]`, and ChartMogul's September 2025 analysis of ~2,700 B2B SaaS companies found **35.7%
of businesses with ARPA above $500/month achieve GRR above 85%, against 5.3% of those below
$10/month** `[M]`. Retention behaviour genuinely differs by contract size — which is why revenue is
the default axis and why the other five dimensions are corrections to it, not replacements.

---

## 2. The six dimensions

### 2.1 Revenue

| | |
| --- | --- |
| **Compute** | `subscription.arr` summed to `account.arr`; ACV = ARR ÷ products for multi-product accounts |
| **Use for** | The default axis. Sets the cost ceiling: coverage cost must stay well inside segment gross margin |
| **Trap** | Ranking on total ARR at a parent account when the contracts sit at subsidiaries. Use `parent_account_id` and declare the reporting grain |
| **Second trap** | Using booked ARR where ramped deals are present. A ramp deal at $300k that bills $80k this year does not fund $300k of coverage. Flag `is_ramped` and segment on the *current* year's recognised ARR |

### 2.2 Potential

| | |
| --- | --- |
| **Compute** | Whitespace = `(account.employee_count × addressable_share) − subscription.seats_purchased`, plus unsold products from the catalogue |
| **Use for** | Promoting an account above what its current ARR buys. A $40k account inside a 20,000-person enterprise is an Enterprise account with an SMB contract |
| **Guardrail** | Potential is a claim, not a fact. Cap the number of potential-based promotions at ~10% of the named tier, require a named opportunity with a close date, and **review every promotion at 2 quarters** — if the whitespace has not converted, demote |
| **Trap** | Letting Sales define potential. Segmentation is a spend decision; require the opportunity in the CRM |

### 2.3 Complexity

The dimension that actually drives hours, and the one most often missing.

| Factor | Score 0–4 on | Why it costs hours |
| --- | --- | --- |
| Live integrations | 0 = none · 4 = 5+ or any bidirectional/critical-path | Every integration is a failure mode with a support tail and a version deadline |
| Legal entities / subsidiaries | 0 = one · 4 = 5+ across jurisdictions | Multiplies stakeholders, invoices, and renewal conversations |
| Custom or bespoke work | 0 = none · 4 = custom code we maintain | Creates an upgrade tax nobody budgets for |
| Regulated status | 0 = none · 4 = FedRAMP / HIPAA / data-residency commitments | Security reviews, audits, DPAs, restricted support paths |
| Languages / regions | 0 = one · 4 = 4+ | Coverage-hours constraints, not just translation |
| Paid products | 0 = one · 4 = 4+ | Cross-product coordination and multiple renewal dates |
| Distinct stakeholders engaged 90d | 0 = 1–2 · 4 = 10+ | Multithreading is protective and expensive |
| Escalations, trailing 12 months | 0 = none · 4 = 3+ or any exec-visible | The strongest single predictor of next year's reactive hours `[P]` |

`complexity_multiplier = 1.0 + (mean score ÷ 8)`, capped at 2.0. An account scoring a mean of 3.0
costs 1.375× the segment baseline. Publish the index per account; it is the number that explains
why two reps with identical ARR have completely different weeks.

### 2.4 Strategic value

| | |
| --- | --- |
| **Qualifies on** | Named reference commitment · design-partner status · logo that opens a named vertical · board or investor visibility · a public case study in flight |
| **Rule** | Strategic status is **granted in writing by a named executive, for a named period, with a named benefit**, and it expires. Ungoverned, it grows until 30% of the base is "strategic" |
| **Cap** | ≤5% of accounts `[P]`. If more than that qualifies, the criteria are not criteria |

### 2.5 Product mix

Multi-product accounts consume more hours (coordination, multiple renewal dates, cross-product
enablement) and retain better. Benchmarkit identifies portfolio breadth as an NRR driver `[M]`.
Treat product count as a **complexity input and an expansion flag**, not as a segment axis of its
own — segmenting on it directly produces segments that are unstable as the catalogue changes.

### 2.6 Lifecycle stage

An **overlay**, never a segment. Accounts move through it; segments should not.

| Stage | Window | Hour multiplier `[P]` | Why |
| --- | --- | --- | --- |
| Onboarding / first value | Day 0 → activation | 2.0–4.0× | Implementation, enablement, stakeholder mapping, the first value proof |
| Adoption | Activation → month 9 | 1.2× | Rollout beyond the pilot team |
| Steady state | Month 9 → T-180 | 1.0× | Baseline |
| Renewal window | T-180 → opt-out deadline | 1.5× | Value case, commercial terms, procurement |
| Recovery | Any at-risk period | 2.0× | Save work is expensive and is not in the cadence budget |

Model the overlay as a **weighted average over the segment's expected stage mix**, not as a peak. A
segment with 20% of accounts onboarding at 3.0× carries a blended multiplier of 1.4, not 3.0.

---

## 3. Setting the boundaries

Three methods. Use the first that the data supports, and print which you used.

| Method | How | Use when |
| --- | --- | --- |
| **Cost-to-serve crossover** | Find the ARR at which the coverage cost of the higher model exceeds a fixed share of segment gross margin. That ARR is the boundary | Preferred. It is the only method that ties the boundary to the economics |
| **Natural break** | Plot the ARR distribution; put boundaries in the sparse regions between clusters | The distribution is genuinely multi-modal (common where pricing tiers drive ACV) |
| **Percentile** | Top 5% / next 20% / remainder | A fallback when cost data is missing. Say it is a fallback, and revisit once cost-to-serve exists |

**The crossover arithmetic.** With loaded cost per customer-facing hour `c`, a coverage model
costing `h` hours per account per year, and a subscription gross margin `g`, the model is
affordable at ARR `A` when `h × c ≤ k × A × g`, where `k` is the share of gross margin you are
willing to spend on coverage. Solving: **`A_min = (h × c) ÷ (k × g)`**.

Worked, using this library's defaults: `c = $171` (see `capacity-math.md` §2), the thin named
profile at `h = 24.1` hours (`capacity-math.md` §5), `g = 0.81` `[Benchmarkit 2025, CY2024 · M]`,
and `k = 0.15`:

```
A_min = (24.1 × 171) ÷ (0.15 × 0.81) = 4,121 ÷ 0.1215 ≈ $33,900
```

Below roughly $34k ARR, even a thin named model spends more than 15% of gross margin on coverage.
That is the boundary — and note it is **derived**, so it moves when your cost, hours or margin
move, which is exactly the property a copied ratio does not have.

**Choosing `k`.** SaaS Capital's 2026 spending benchmarks (survey March 2026, 1,000+ private B2B
SaaS) put **CS + Support at a 9% of ARR median, up from 8%**, 10% at $3–5M ARR, with equity-backed
companies spending roughly twice bootstrapped ones `[M]`. That is total CS *and* support across the
whole base. A `k` that implies blended CS-only spend far above ~9% of ARR needs a reason.

---

## 4. The composite score

When ARR alone mis-sorts the base — common in usage-based businesses and where ACV is compressed —
score each account and cut on the score.

| Component | Weight `[P]` | Normalisation |
| --- | --- | --- |
| Current ARR | 40 | Percentile within the base |
| Potential (whitespace + unsold products) | 20 | Percentile, capped at the 90th to stop one giant account dominating |
| Strategic value | 15 | 0 / 50 / 100, granted in writing |
| Complexity | 15 | Complexity index rescaled 0–100 — **note this raises cost, so it argues for a *different* model, not automatically a richer one** |
| Retention risk propensity | 10 | Segment-level historical GRR by cohort, not the account's current health score |

Two rules that keep this honest:

1. **Weights are declared and versioned.** An undeclared weighting is an opinion wearing arithmetic.
2. **Complexity raising the score must be interpreted.** A complex, low-ARR account does not deserve
   more coverage — it deserves *cheaper* coverage, a simplification project, or a price change. Send
   it to a different model, not up a tier.

---

## 5. The three tests, worked

### Differentiation

| Segment pair | h/account/yr | Δ | Model differs? | Renewal owner differs? | EBR entitlement differs? | Verdict |
| --- | --- | --- | --- | --- | --- | --- |
| Enterprise (58) vs Mid-Market (31) | 58 → 31 | −47% | Named → named | AM → AM | 4/yr → 2/yr | **Pass** — hours and entitlement both differ |
| Mid-Market (31) vs Growth (26) | 31 → 26 | −16% | Named → named | AM → AM | 2/yr → 2/yr | **FAIL — decorative.** Merge, or cut Growth to a pooled model |
| Growth (26) vs Scale (4) | 26 → 4 | −85% | Named → pooled | AM → renewals desk | 2/yr → 0 | **Pass** |

The failing row is the common one, and the correction is never "add a slide". It is either merge
the two segments or genuinely change the Growth model — which is a funding decision, and belongs in
the headcount case.

### Actionability

| Boundary as written | Verdict |
| --- | --- |
| `account.arr >= 250000` | ✅ Computable |
| `account.arr BETWEEN 50000 AND 249999 AND account.is_internal = FALSE` | ✅ Computable |
| "Accounts our VP considers strategic" | ❌ Not a rule. Replace with a written grant list carrying an owner and an expiry |
| "High-potential accounts" | ❌ Define: `employee_count >= 1000 AND seats_purchased < 100 AND open_opportunity_amount > 0` |

### Consequence

For each segment, write the sentence: *"An account below this line stops receiving ______."* If the
blank is hard to fill, the boundary is not funded. Good answers: a named CSM · live business
reviews · a success plan reviewed quarterly · a human-owned renewal conversation · onsite time.
Bad answers: "less attention", "lower priority" — those describe a feeling, not an entitlement.

---

## 6. Migration and hysteresis

Accounts move. Uncontrolled, they move every quarter, and each move costs 8–12 hours plus a
relationship reset `[P]`.

| Rule | Value | Reason |
| --- | --- | --- |
| **Promotion trigger** | Two consecutive quarters above the boundary, **or** an immediate contract event (new ARR, product added, multi-year signed) | Contract events are decisions; drift is noise |
| **Demotion trigger** | Two consecutive quarters below, **and** no renewal inside 180 days, **and** no open escalation | Never demote an account that is about to make a decision about you |
| **Demotion freeze** | No demotion inside the opt-out window | Reducing service while they are deciding is the most avoidable own goal in CS |
| **Move cap** | ≤15% of any tier per quarter | Protects continuity and the receiving team's capacity |
| **Communication** | Any change a customer can perceive gets a written note; see `../assets/coverage-change-note.md` | A silent downgrade is discovered at the worst moment |
| **Cooling-off** | No account changes segment twice in 12 months | Oscillation is worse than being in the wrong tier |

**The demotion that is actually a save opportunity.** An account falling below a boundary because
of a seat reduction is not a segmentation event, it is a contraction signal. Route it to
`churn-risk` before routing it to a cheaper coverage model.

---

## 7. The handover pack

Every reassignment ships this. Without it the receiving CSM rediscovers the account, which costs
more than the handover would have and is visible to the customer as an amnesia event.

| Section | Content | Why it cannot be skipped |
| --- | --- | --- |
| **Commercial state** | ARR, products, renewal date, **opt-out deadline**, notice period, auto-renew, discount and its expiry, uplift, last negotiation's hard points | The receiving CSM must not learn the notice period from the customer |
| **The customer's objective, in their words** | A verbatim quote with a date and where it came from | Paraphrase drifts; the quote is the anchor |
| **Relationship map** | Every contact with role, influence, sentiment, last interaction, and who is the economic buyer | This is the asset. Everything else is in a system somewhere |
| **Open commitments, both directions** | Who owes what, promised when, due when, current status | Walking into the first call unaware of a broken promise ends the relationship's credit |
| **What is not written down** | The outgoing CSM's answer to: what do you know about this account that is not in any system? | The single highest-value paragraph in the pack, and the one that disappears when someone resigns |
| **Live risks and history** | Current band, past escalations and how they were resolved, topics that are sensitive | Prevents the new CSM re-opening a settled wound |
| **First 30 days** | Three named actions with dates | A handover without a plan is a file transfer |

**The introduction is live, not written.** A joint call — outgoing CSM, incoming CSM, customer — of
fifteen minutes. The outgoing CSM introduces, states one thing the incoming CSM is better placed to
help with, and leaves. An email introduction is what teams do when they have already disengaged,
and customers read it correctly.

---

## 8. The twelve audit tests

| # | Test | Evidence to pull | Pass mark |
| --- | --- | --- | --- |
| 1 | Every account has an owner | `account` where `owner_csm IS NULL` and `status='active'` | Unassigned ARR = $0 |
| 2 | Segmentation is differentiated | Hours per account per segment; entitlement table | No adjacent pair fails §5 |
| 3 | Entitlements are delivered | Business reviews completed ÷ entitled, trailing 2 quarters, ARR-weighted | ≥85% in named tiers `[P]` |
| 4 | Books are actually served | Accounts with a bilateral `interaction` in 90d ÷ assigned | ≥70% in named tiers `[P]` |
| 5 | Ratios are derived | Ask for the derivation document | It exists, is dated within 2 quarters, and shows lines A–H |
| 6 | No structural deficit | Required hours vs available, per segment | Deficit ≤0, or a written funded plan |
| 7 | No over-service leakage | Interaction hours logged against digital/pooled-tier accounts | <5% of named-tier hours `[P]` |
| 8 | Tech-touch is real | The six conditions in `coverage-models.md` §6 | All six |
| 9 | Books balanced on complexity | Complexity index per rep vs the mean | Within ±15% |
| 10 | Renewal concentration | Max month's renewing ARR ÷ rep's total renewing ARR | ≤20% |
| 11 | Ramp respected | Book size of hires <6 months in role | ≤40% at month 3, ≤70% at month 6 |
| 12 | Cost-to-serve known | Fully loaded CS cost per segment ÷ segment ARR | Computed, and below the segment's gross-margin contribution |

Report each as pass/fail **with the number**, not a tick. "Test 4: 61% touch coverage against a 70%
threshold; the 39% not touched holds $4.1M ARR, of which $900k renews inside 180 days" is a finding.
A red tick is a mood.

---

## 9. Specialisation trade-offs

| Model | Buys | Costs | Use when |
| --- | --- | --- | --- |
| **Generalist CSM** | Continuity, simple assignment, resilience | Shallow depth in complex verticals | Default below ~$50M ARR, horizontal product |
| **Vertical specialist** | Credibility in the first meeting, faster diagnosis, reusable assets | Assignment rigidity — a departure strands a vertical; territory balance becomes hard | ≥3 named verticals each holding ≥15% of ARR |
| **Lifecycle split** (onboarding pod → CSM) | Onboarding gets an owner with real expertise; first-value time falls | A handover in the first 90 days, when trust is thinnest | Onboarding is >25% of total hours, or first-year churn is concentrated in failed launches |
| **Motion split** (CSM adoption / AM commercial) | Commercial skill on the renewal; CSM stays trusted | Two relationships to maintain; risk of the CSM discovering the renewal terms late | Enterprise, negotiated renewals, procurement involved |
| **Technical overlay** (SA/FDE alongside CSM) | Integration and architecture risk gets an owner | Expensive; scarce; needs explicit allocation rules | Complexity index mean ≥2.5 in the segment |

**Every split adds a handover, and every handover leaks.** Specialise when the depth gained is
larger than the continuity lost, and write down which specific handover you are accepting.

---

## 10. Anti-patterns

| Anti-pattern | Correction |
| --- | --- |
| Segments named for the sales team's territory | Segment on how the customer is served, not on who sold it |
| A "strategic" tier with no written criteria or expiry | Named grant, named benefit, named expiry, ≤5% of accounts |
| Boundaries set by percentile and never revisited | Derive from the cost-to-serve crossover once cost data exists |
| Segment on booked ARR including un-started ramps | Use the current year's recognised ARR; flag `is_ramped` |
| Promoting on potential with no opportunity record | Require a CRM opportunity with an amount and a close date; review at 2 quarters |
| Reassigning accounts every quarter to balance ARR | Continuity is a hard constraint; cap moves at 15% per tier per quarter |
| Demoting an account inside its opt-out window | Freeze all coverage changes until the renewal is closed |
| Complexity ignored, so books balance on ARR and break on hours | Publish the complexity index per rep |
| An entitlement the team cannot staff | If required hours exceed capacity, the entitlement is fiction — change it or fund it |
| Handover by email | A live three-way call, plus the written pack |
| Auditing with ticks | Every test reports its number and the ARR behind the gap |

---

## 11. Evidence register

| Claim | Value | Source | Year | Label |
| --- | --- | --- | --- | --- |
| GRR rises monotonically with ACV | directional | Benchmarkit, *2025 SaaS Performance Metrics Benchmarks*, CY2024 actuals | 2025 | `[M]` |
| GRR >85% achieved by 35.7% of businesses with ARPA >$500/mo vs 5.3% below $10/mo | as stated | ChartMogul, ~2,700 B2B SaaS companies, min $250k ARR | Sep 2025 | `[M]` |
| CS + Support spend | 9% of ARR median (8% prior year); 10% at $3–5M ARR; equity-backed ≈2× bootstrapped | SaaS Capital, *2026 Spending Benchmarks*, survey Mar 2026, 1,000+ private B2B SaaS | 2026 | `[M]` |
| Subscription gross margin | 81% median | Benchmarkit 2025, CY2024, N=76 | 2025 | `[M]` |
| Small-cell fragility | Benchmarkit's own >$100M expansion cohort at n=6 | Benchmarkit 2025 | 2025 | `[M]` |
| Portfolio breadth as an NRR driver | directional | Benchmarkit 2025 | 2025 | `[M]` |
| Named vs pooled tiers with a documented transition process between them | first-party operating model | GitLab public handbook — Success Tiers; CSM → pooled CSE account transition process | 2026 | `[V]` |
| Complexity multiplier formula, lifecycle multipliers, strategic-tier cap, move cap, handover cost | as stated | Practitioner convention used by this library | — | `[P]` |
| Touch coverage floor ~70%; entitlement delivery ≥85% | as stated | Practitioner convention | — | `[P]` |

**No accounts-per-CSM or ARR-per-CSM benchmark appears in this file.** The circulated figures are
vendor aggregations of their own customer bases, largely undated and without disclosed sample sizes,
several traceable to a single 2016 survey. Deriving the ratio from `capacity-math.md` is both more
defensible and more useful, because it moves when your inputs move.
