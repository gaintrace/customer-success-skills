# The CS Metric Dictionary

> The canonical definition of every customer success metric used in this library. When
> `retention-report`, `renewal-forecast`, `exec-retention-review` and `coverage-and-capacity`
> all quote NRR, they quote the formula in this file — which is what makes the artifacts
> reconcile with each other and with finance.
>
> **Rules for using it**
> 1. Never change a definition between reporting periods without a written restatement note.
> 2. Every metric you publish must name its window, its denominator and its cohort basis.
> 3. Evidence labels are load-bearing: `[M]` measured benchmark · `[V]` vendor research ·
>    `[P]` practitioner rule of thumb · `[A]` academic. A `[P]` number is a starting point
>    for a conversation, never a benchmark to be held to.
> 4. Benchmarks vary enormously by ACV, pricing model and company age. Quote the segment,
>    not the headline median.

---


Reference material for producing analyst-grade customer success and retention analysis.
Compiled 2026-08-27. Every benchmark carries a source, a year, and a confidence grade.

---

**Contents**

- [0. How to use this file](#0-how-to-use-this-file)
- [1. Foundational objects (get these right or nothing else works)](#1-foundational-objects-get-these-right-or-nothing-else-works)
- [2. Revenue retention metrics](#2-revenue-retention-metrics)
- [3. Logo / customer retention](#3-logo-customer-retention)
- [4. The ARR/MRR bridge (waterfall)](#4-the-arrmrr-bridge-waterfall)
- [5. Cohort retention curves & survival analysis](#5-cohort-retention-curves-survival-analysis)
- [6. Unit economics: CLV/LTV, LTV:CAC, CAC payback, ACV](#6-unit-economics-clvltv-ltvcac-cac-payback-acv)
- [7. Value realization, adoption, and product signals](#7-value-realization-adoption-and-product-signals)
- [8. Health score, sentiment, and support](#8-health-score-sentiment-and-support)
- [9. Usage-based and public-company methodology divergence (critical for benchmarking)](#9-usage-based-and-public-company-methodology-divergence-critical-for-benchmarking)
- [10. CS capacity, coverage, and cost](#10-cs-capacity-coverage-and-cost)
- [11. Renewal operations metrics](#11-renewal-operations-metrics)
- [12. Worked example: full ARR bridge and derived metrics](#12-worked-example-full-arr-bridge-and-derived-metrics)
- [13. The standard monthly CS / retention report](#13-the-standard-monthly-cs-retention-report)
- [14. Anti-patterns of CS reporting](#14-anti-patterns-of-cs-reporting)
- [15. Master benchmark table (quick reference)](#15-master-benchmark-table-quick-reference)
- [16. Sources](#16-sources)

---

## 0. How to use this file

**Confidence grading used throughout:**

| Grade | Meaning |
|---|---|
| **A** | Measured benchmark from a primary report with disclosed methodology and sample size (Benchmarkit, SaaS Capital, ChartMogul, Recurly, SEC filings, SaaS Metrics Standard Board) |
| **B** | Measured benchmark reported by a secondary source citing a named primary study; primary PDF not independently verified |
| **C** | Practitioner rule-of-thumb, vendor blog, or content-farm aggregation. Useful as a *heuristic*, never as a *fact*. Never present a C number to a board as "the benchmark." |

**Non-negotiable reporting rules baked into every metric below:**
1. Never quote a retention number without the **segment** and the **denominator construction**. "NRR is 104%" is not a fact; "Enterprise cohort NRR, TTM, ARR basis, excluding reactivation, is 104.2%" is.
2. Retention metrics are **cohort** metrics. The formula method is an approximation, not the definition.
3. Always publish GRR next to NRR. NRR alone hides churn behind expansion.
4. Every metric must name the **decision** it drives. If no decision changes at any value, delete the metric.

---

## 1. Foundational objects (get these right or nothing else works)

| Term | Precise definition | Common error |
|---|---|---|
| **ARR** | Annualized value of contracted recurring subscription revenue in force at a point in time. Excludes professional services, one-time fees, hardware, non-recurring overages. | Including implementation fees or perpetual license; including signed-but-not-live contracts (that is CARR, not ARR). |
| **CARR** (Contracted ARR) | ARR including signed contracts not yet live/billing. | Reporting CARR as ARR in a board deck without labeling it. Inflates growth and distorts every retention denominator. |
| **MRR** | ARR / 12 for annual contracts; contracted monthly value for monthly contracts. | Mixing billing-period revenue with normalized MRR. |
| **Cohort** | A set of customers **frozen** at a reference date (t0). Membership never changes. Customers acquired after t0 never enter the cohort. Churned members stay in the cohort contributing $0. | Letting new logos leak into the cohort; dropping churned customers from the denominator (the single most common — and most flattering — error). |
| **ATR** (Available to Renew) | ARR (or logo count) with a contractual renewal/expiry date falling inside the measurement period. | Using total ARR as the renewal denominator. On multi-year contracts this understates churn severity dramatically. |
| **Recurring vs. variable** | Committed subscription vs. usage/overage. Usage-based businesses must state whether overage is in the ARR base. | Snowflake, Klaviyo, Fastly, Datadog all treat usage differently — see §9. |
| **Segment** | The primary cut. **ACV band is the single most predictive segmentation variable for retention** (SaaS Capital 2025, Grade A; Benchmarkit 2025 states "GRR benchmarks are best analyzed by ACV", Grade A). | Segmenting only by employee count or industry and then wondering why the benchmark doesn't fit. |

---

## 2. Revenue retention metrics

### 2.1 Gross Revenue Retention (GRR / GDR)

| Field | Value |
|---|---|
| **Formula (cohort method — the standard)** | `GRR = (ARR at t1 from the t0 cohort, with all expansion above each account's t0 ARR stripped out) / (ARR at t0 from that cohort)` |
| **Formula (approximation)** | `GRR = (Beginning ARR − Churned ARR − Contraction ARR) / Beginning ARR` |
| **Unit** | % (capped at 100% by construction — a GRR > 100% is a calculation bug) |
| **Window** | Annual (TTM) primary. Monthly/quarterly permitted but must be annualized geometrically: `GRR_annual = (GRR_monthly)^12`, never `1 − 12 × monthly_churn`. |
| **Data source** | Billing/subscription system (source of truth) → CRM contract records. Never the CS platform's own rollup unless reconciled to billing. |
| **Miscalculations** | (a) Netting expansion inside an account against its own contraction — that is NRR, not GRR. (b) Dropping churned logos from the denominator. (c) Including new logos acquired mid-period. (d) Counting an accelerated-revenue write-off from a cancelled contract. (e) Including variable/usage overage (SaaS Metrics Standard Board recommends excluding). (f) Mixing win-backs in — define a win-back window (SMSB: typically 30–90 days) and treat re-signs outside it as New, not as never-churned. |
| **Benchmarks** | Median **88%**, CY2024 actuals, N=225 (Benchmarkit 2025 SaaS Performance Metrics Benchmarks) — **A**. Down from 90% in 2022 — **A**. By pricing model CY2024: usage-based **92%** median (Q1 88%, Q3 96%) vs. subscription and hybrid **88%** — **A**. GRR rises monotonically with ACV — **A** (directional; per-band values are in the interactive tool, not the PDF). For CY2025: median **84%**, top quartile **91%**, bottom quartile **76%**, N=226 (2026 Aleph × Benchmarkit) — **B**; same source: sales-led 88% / hybrid 80% / PLG 79%, $50–100K ACV 91%, sub-$5K ACV 80% — **B**. ChartMogul (Sept 2025, ~2,700 B2B SaaS, min $250K ARR): "best-in-class GRR ≈95% for mid-market/enterprise sellers"; 35.7% of businesses with ARPA > $500/mo have GRR > 85% vs. 5.3% of those with ARPA < $10/mo — **A**. |
| **Decision it drives** | Whether the product/onboarding/support engine is fundamentally sound. GRR is the CS org's own scoreboard because it cannot be rescued by sales-led expansion. A GRR miss is a product or delivery problem; an NRR miss with healthy GRR is a pricing/packaging or expansion-motion problem. |

### 2.2 Net Revenue Retention (NRR / NDR)

| Field | Value |
|---|---|
| **Formula (cohort — preferred; SaaS Metrics Standard Board)** | `NRR = (ARR at t1 from the t0 cohort) / (ARR at t0 from that cohort)` |
| **Formula (approximation)** | `NRR = (Beginning ARR + Expansion − Contraction − Churn) / Beginning ARR` |
| **Unit** | % (can exceed 100%) |
| **Window** | TTM / year-over-year. For usage-based or seasonal businesses, TTM is mandatory; monthly point-in-time NRR is noise. |
| **Data source** | Billing system, cohort table keyed on `account_id`, `arr_t0`, `arr_t1`, `cohort_date`. |
| **Miscalculations** | (a) **Including new-logo ARR in the numerator** — this produces the growth rate, not NRR. (b) Including **reactivation** ARR from customers who were not in the t0 cohort. (c) Including expansion earned by logos acquired *inside* the window. (d) Removing churned customers from the denominator (the "surviving customers only" trap — Figma's S-1 uses a look-backward construction that structurally excludes departed accounts; disclosed 132% NRR — **A** on the disclosure, and a caution on comparability). (e) Reporting blended NRR only — blended NRR across segments is nearly uninformative when segment NRRs differ by 20+ points. (f) FX: use constant currency or say you didn't. |
| **Benchmarks** | Median **101%**, CY2024, N=228 (Benchmarkit 2025) — **A**; down from 105% (CY2021) and 103% (CY2022, US) — **A**. Hybrid subscription+usage pricing **110%** median vs. usage-only and subscription-only lower — **A**. NRR rises with ACV, consistently over 4 years — **A**. CY2025 (2026 Aleph × Benchmarkit, N=230) — **B**: median **102%**, P75 **110%**, P25 **92%**; usage-based 108% (P75 155%) vs. seat-based 98%; >$100M ARR 103%; $20–50M 101%; <$5M 94%; $25–50K ACV 105%; $10–25K ACV fell below 100%; >50% growth cohort 111%, <10% growth cohort 92%. SaaS Capital 2025 (private B2B SaaS, $1M+ ARR): $25–50K ACV band median **102%**, P75 **111%**, P25 **97%** — **A**. ChartMogul Sept 2025 (~2,700 B2B SaaS, min $250K ARR): median **82%**, P75 **97%** — **A** but note this population skews to smaller/self-serve subscription businesses and is *not* comparable to Benchmarkit's survey population. |
| **Decision it drives** | Valuation, ARR plan attainment, and whether growth can come from the installed base vs. new logo. Sets the expansion quota and the CS-vs-AM comp design. |

### 2.3 Related revenue-retention variants

| Metric | Formula | Notes / benchmark |
|---|---|---|
| **Gross ARR churn rate** | `Churned ARR / Beginning ARR` | Complement of the churn half of GRR. Separate it from contraction — they have different root causes and different playbooks. |
| **Contraction (downsell) rate** | `Contraction ARR / Beginning ARR` | Seat reductions, tier downgrades, negotiated discounts at renewal, product de-scoping. Track *reason codes*. Contraction rising while churn is flat = pricing/value-density problem, not a churn problem. |
| **Net ARR churn** | `(Churn + Contraction − Expansion) / Beginning ARR` = `1 − NRR` | Negative net churn = NRR > 100%. |
| **Gross $ renewal rate** | `Renewed ARR / ATR ARR` | Always ≤ GRR when losses occur only at renewal, because the ATR denominator is smaller than total ARR. Do not benchmark renewal rate against GRR benchmarks. |
| **Net $ renewal rate** | `(Renewed ARR + Expansion booked at renewal) / ATR ARR` | Measures the renewal *event*, not the year. Best metric for a renewals desk's quota. |
| **Expansion ARR % of total new ARR** | `Expansion ARR / (New Customer ARR + Expansion ARR)` | Median **40%** CY2024, +5pp YoY, N=81 (Benchmarkit 2025) — **A**. $50–100M ARR: **58%**; >$100M ARR: **67%** (n=6, fragile) — **A**. 2022 baseline ~25% — **A**. |
| **Expansion rate** | `Expansion ARR / Beginning ARR` | Decompose into seat expansion / tier upgrade / cross-sell / price uplift / usage growth. A single "expansion" number is not actionable. |
| **Average renewal uplift** | `(Renewed ARR at new price − Renewed ARR at prior price) / Renewed ARR at prior price`, on renewals that did not add units | Isolates pure price realization from volume expansion. CFO-facing. Track against the list-price increase to get **price realization %**. |

---

## 3. Logo / customer retention

| Metric | Formula | Window | Notes |
|---|---|---|---|
| **Logo retention** | `(# of t0-cohort customers still active at t1) / (# active at t0)` (SaaS Metrics Standard Board) | TTM, computed monthly | Exclude freemium, free-trial, and trial accounts. Write down and apply consistently the policy for (a) customers current on invoices with no signed renewal, (b) usage-based accounts with a zero-usage month. |
| **Logo churn rate** | `1 − logo retention` | | |
| **ARR-weighted vs. count-weighted divergence** | Compare `1 − GRR` to `logo churn` | | **The single most useful two-number diagnostic in CS.** If dollar churn > logo churn, you are losing your *larger* customers. If logo churn > dollar churn, you are losing your *smaller* customers. Quantify with `avg ARR of churned account / avg ARR of all accounts`. |
| **Churn by acquisition channel** | Logo & $ churn segmented by `original_lead_source` | Annual, by cohort | Detects a sales-quality problem masquerading as a CS problem. If paid-search-sourced logos churn at 2x outbound-sourced logos, the fix is in demand gen, not in the CSM playbook. |
| **Churn by tenure** | Churn rate within tenure buckets: 0–90d, 91–180d, 181–365d, Y2, Y3, Y4+ | Rolling | Front-loaded churn = onboarding/ICP failure. Back-loaded churn = value-decay/competitive failure. These need opposite investments. |

**Logo-churn benchmarks**

| Population | Value | Source / year | Grade |
|---|---|---|---|
| B2B SaaS overall annual churn | **3.5%** total = 2.6% voluntary + 0.8% involuntary | Recurly 2025 Churn Report (subscription network) | A |
| Business & professional services, median annual | **3.21%** | Recurly network, 2025 | A |
| Monthly user churn by ARPU (self-serve skew) | <$10: 6.2% · $10–25: 6.6% · $25–50: 7.3% · $50–100: 6.3% · $100–250: 7.1% · >$250: 5.0% | Baremetrics Open Benchmarks, 2025 (relayed secondhand; not verified against the primary) | B |
| Monthly revenue churn by ARPU | <$10: 6.7% · $10–25: 6.9% · $25–50: 8.6% · $50–100: 7.3% · $100–250: 7.8% · >$250: 6.5% | Baremetrics Open Benchmarks, 2025 (relayed secondhand; not verified against the primary) | B |
| Monthly logo churn by segment: SMB 3–5%, MM 1.5–3%, ENT 1–2% | — | Aggregated vendor content, 2025–26 | C |

> **Warning:** Recurly's network is dominated by card-billed subscription businesses. Applying its 3.5% annual figure to a $100M-ARR enterprise B2B SaaS is a category error. For enterprise B2B, use Benchmarkit/SaaS Capital ARR-based retention, not Recurly logo churn.

---

## 4. The ARR/MRR bridge (waterfall)

**Canonical identity:**

```
Ending ARR = Beginning ARR
           + New ARR            (logos with no prior ARR)
           + Expansion ARR      (existing logos, increase above their beginning ARR)
           + Reactivation ARR   (logos previously churned, returning after the win-back window)
           − Contraction ARR    (existing logos, decrease, still > $0)
           − Churned ARR        (existing logos going to $0)
```

**Component definitions and boundary rules — write these down and freeze them:**

| Component | Rule | Boundary decisions you must make explicit |
|---|---|---|
| **New** | Account had $0 ARR at t0 and >$0 at t1, and has never previously been a paying customer (or churned longer ago than the win-back window). | Does a new subsidiary of an existing parent count as New or Expansion? Decide by `ultimate_parent_id` and be consistent. |
| **Expansion** | Same `account_id`, ARR_t1 > ARR_t0. | Split into: seats, tier upgrade, cross-sell (new SKU), price uplift, usage-commit increase. Contractual uplift from a pre-signed ramp is expansion but must be flagged separately — it is not a CS win. |
| **Reactivation** | Previously churned account returns after the win-back window (30–90 days per SMSB). | Reactivation is **excluded from NRR and GRR cohort math** because the account was not in the t0 cohort. It belongs in the bridge and in the growth number only. |
| **Contraction** | Same account, ARR_t1 < ARR_t0, ARR_t1 > 0. | An account that downsells to $0 is Churn, not Contraction. Multi-product: net at the account level, then classify — do not book both expansion on SKU A and contraction on SKU B for the same account in a way that double-counts. Report gross SKU-level movement separately. |
| **Churn** | ARR_t1 = 0 for an account with ARR_t0 > 0. | Date of churn = contract end date, not notice date. Track `notice_date` separately — the gap is your early-warning window. M&A-driven churn (customer acquired and consolidated onto another vendor) should be tagged and shown as a memo line; it is not a CS performance failure but it *is* real lost ARR. |

**Derived metrics off the bridge:**

| Metric | Formula | Benchmark |
|---|---|---|
| **SaaS Quick Ratio** | `(New + Expansion) / (Churn + Contraction)` | Introduced by Mamoon Hamid (then Social Capital, now Kleiner Perkins) at SaaStr 2015; the canonical target is **4.0** — **C** (widely-cited practitioner target, not a measured median). Mature/large-base companies commonly run 2.5–3.5 — **C**. Declare whether reactivation is in the numerator; the strict form excludes it. |
| **Net New ARR** | `Ending ARR − Beginning ARR` | |
| **Gross New ARR** | `New + Expansion` (+ Reactivation if disclosed) | Denominator for CAC ratios. |
| **Churn+contraction as % of gross new** | `(Churn + Contraction) / (New + Expansion)` | The "leaky bucket ratio." At 50%+ you are running a treadmill. |
| **SaaS Magic Number** | `(Current Qtr Revenue − Prior Qtr Revenue) / Prior Qtr S&M Expense` (Benchmarkit glossary, 2025) — **A** | Traditional low-water mark 0.75, ideal >1.0 — **C** (convention). Benchmarkit explicitly recommends CAC Ratio instead, because Magic Number conflates New, Expansion, Churn and Downsell into one uninterpretable number — **A**. |
| **Burn Multiple** | `Net Burn / Net New ARR` (Benchmarkit glossary, 2025) — **A**. Popularized by David Sacks (Craft Ventures). | Goal <1.0 by the $25–50M ARR range — **A** (Benchmarkit commentary). |

---

## 5. Cohort retention curves & survival analysis

| Concept | Definition | Practical guidance |
|---|---|---|
| **Cohort retention table** | Rows = acquisition cohort (signup month/quarter). Columns = months since acquisition (M0…M36). Cells = % of cohort still active (logo) or % of cohort's t0 ARR retained (dollar). | Publish **both** a logo table and a dollar table. Dollar tables can exceed 100% (expansion); logo tables cannot. |
| **Survival function S(t)** | Probability an account is still active beyond tenure t. Kaplan–Meier estimator handles **right-censored** accounts (still active at analysis date) without discarding them. | Discarding censored accounts is the classic naive error; it biases retention downward for recent cohorts. |
| **Hazard function h(t)** | Instantaneous churn rate at tenure t among accounts that survived to t. | The shape is the diagnosis: a spike at t=12 months means renewal-event churn; a monotonic early decline means onboarding failure. Plot hazard, not just survival. |
| **Cox proportional hazards** | Multivariate: hazard ratio per covariate (ACV band, channel, industry, onboarding-completion flag, TTFV days, health tier, exec-sponsor-present flag). | Gives interpretable hazard ratios ("accounts that miss TTFV by >30 days carry a 2.4x hazard"). Run PH diagnostics (Schoenfeld residuals); if PH is violated use an Aalen additive or time-varying-coefficient model. Ref: *Predictability & explainability of survival analysis in churn prediction*, Journal of Marketing Analytics, 2025 — **A** (methodological, not a benchmark). |
| **Curve flattening** | The tenure at which the retention curve's slope approaches zero. | If the curve never flattens, there is no stable customer base and LTV is unbounded-downward. Report "months to flatten" as a leading indicator of durable retention. |
| **Cohort-quality drift** | Compare M3/M6/M12 retention of the latest 6 cohorts to the trailing-12 average. | Detects ICP drift from a new segment/channel 9 months before it shows up in NRR. |

**Illustrative template (not a benchmark) — logo survival, monthly cohorts:**

| Tenure | M0 | M1 | M3 | M6 | M12 | M18 | M24 | M36 |
|---|---|---|---|---|---|---|---|---|
| Healthy enterprise cohort | 100% | 99% | 98% | 96% | 92% | 89% | 86% | 81% |
| Healthy SMB cohort | 100% | 93% | 86% | 79% | 70% | 65% | 61% | 55% |
| Broken onboarding (any segment) | 100% | 88% | 74% | 66% | 58% | 54% | 52% | 49% |

Diagnostic: subtract adjacent columns to get period hazard. In the "broken onboarding" row, 26 of the 42 points lost by M12 are lost by M3 — the fix is pre-M3, and no amount of renewal-quarter heroics will change the M12 number.

---

## 6. Unit economics: CLV/LTV, LTV:CAC, CAC payback, ACV

### 6.1 LTV — the naive formula vs. the defensible ones

| Version | Formula | When it's acceptable |
|---|---|---|
| **Naive (do not use)** | `LTV = ARPA / churn_rate` | Never. Treats every revenue dollar as profit; at 81% subscription gross margin it overstates LTV by ~23% (1/0.81). |
| **Gross-margin adjusted (minimum acceptable)** | `LTV = (ARPA × Gross Margin %) / Gross revenue churn rate` | Internal analysis, channel ROI, sales payback. Benchmarkit's published CLTV:CAC glossary formula is `(Average ARR per Account × Recurring Revenue Gross Margin / Churn Rate) / CAC per new customer` — **A**. |
| **Discounted perpetuity (board/valuation grade)** | `LTV = (ARPA × GM%) / (d + c)` where `d` = annual discount rate (WACC, commonly 10–15% for private SaaS) and `c` = annual gross revenue churn rate | Any LTV used to justify capital allocation. Mandatory when churn is low, because an undiscounted perpetuity explodes. |
| **Expansion-aware (negative-churn businesses)** | Replace `c` with net revenue churn `(1 − NRR)`. If NRR > 100%, `1 − NRR` is negative and you **must** carry a discount rate `d > |1 − NRR|`, or LTV is infinite. | Businesses with NRR > 100%. Cap the expansion assumption at a finite horizon (e.g., 5–7 years) rather than assuming perpetual expansion. |
| **Cohort-empirical (best)** | Sum of observed discounted gross profit per cohort through the observation window + a modeled tail from the fitted survival curve. | When you have ≥36 months of cohort data. Removes the constant-hazard assumption entirely. |

**Constant-hazard assumption warning:** `1/churn` as "average lifetime" is only valid if the hazard is constant over tenure. Real SaaS hazards are decreasing (front-loaded churn), which means `1/churn` *understates* the lifetime of survivors and *overstates* it for the cohort as a whole in the early months. Use the survival curve if you have it.

### 6.2 CAC, payback, and ratios

| Metric | Formula | Benchmark |
|---|---|---|
| **New Customer CAC** | `S&M expense attributable to new-logo acquisition (prior period, lagged by sales cycle) / # new logos` | Lag S&M by roughly one sales cycle. Unlagged CAC in a fast-growing company understates cost. |
| **New CAC Ratio** | `Total S&M expense / New Customer ARR` (Benchmarkit glossary) — **A** | Median **$2.00** of S&M per $1 new ARR, CY2024, +14% YoY, N=73; 4th quartile **$2.82** (Benchmarkit 2025) — **A**. |
| **Blended CAC Ratio** | `Total S&M expense / (New ARR + Expansion ARR)` — **A** | Median **$1.40** CY2024, down ~12% ($0.19) YoY, N=43 — **A**; still ~10% higher than 2022 — **A**. |
| **Expansion CAC Ratio** | `S&M + CS expense allocated to expansion / Expansion ARR` — **A** | Median **$1.00** CY2024, N=21. Was $0.61 in 2020 and $0.69 in 2021–22 — **A**. **<20% of companies calculate it** — **A**. This is the single highest-leverage missing metric in most CS orgs: it is the number that proves expansion is cheaper than new logo ($1.00 vs $2.00). |
| **CAC Payback Period** | `S&M Expense / (New Customer ARR × Gross Subscription Margin) × 12` → months (Benchmarkit glossary) — **A** | CY2024 median rose ~12.5% since 2022 and is highly correlated to ACV, N=148 — **A**. By ACV (Benchmarkit 2025, reported): ~9 mo sub-$5K, ~12 mo $10–25K, ~14 mo $25–50K, ~24 mo >$250K — **B**. CY2025 (2026 Aleph × Benchmarkit, N=198): median **16 months**, top quartile **≤6**, bottom quartile **≥24**; sub-$5K ACV 11 mo, $50–100K ACV 22 mo; horizontal 14 mo vs. vertical 18 mo — **B**. Conventional thresholds: <12 mo excellent, <18 mo acceptable — **C**. |
| **Public vs. private CAC payback is not comparable** | Private companies compute payback on **New Customer ARR only**; public-company "implied" payback uses **Net New ARR** (which nets churn, downsell and expansion) — Benchmarkit 2025 explicitly flags this — **A**. | Never benchmark a private company's payback against a public comp without normalizing. |
| **LTV:CAC** | `LTV (gross-margin adjusted) / New Customer CAC` | The 3:1 convention originates with David Skok (Matrix Partners, c. 2010) — **C** on provenance, universally adopted. Benchmarkit reports CLTV:CAC declines for companies above ~$20M ARR — **A**. A "3.2:1 2026 median" circulates in secondary sources — **C**, unverified. |
| **ACV** | `Total contract value / contract term in years`, per contract; report as a median and a distribution, never only a mean | Mean ACV is destroyed by one whale. Report P25 / median / P75 / top-decile share of ARR. |
| **ARR concentration** | `Top 10 accounts' ARR / total ARR`; also Herfindahl index | >25% in the top 10 is a board-level risk disclosure. Pair with a "top-10 renewal calendar" slide. |
| **Gross margin inputs** | Subscription GM median **81%**, total revenue GM **77%**, professional services GM **30%**, CY2024 (Benchmarkit 2025, N=76/196/38) — **A**. Prof services ≈15% of total revenue at median — **A**. | Use *subscription* GM in LTV and CAC payback, not blended. |

---

## 7. Value realization, adoption, and product signals

| Metric | Formula / definition | Window | Data source | Notes & benchmarks |
|---|---|---|---|---|
| **Time to First Value (TTFV)** | Days from contract start (or from signup for PLG) to the first completed **success milestone** — a customer-defined outcome, not a vendor task. Lincoln Murphy: measure on a *success-milestone* basis, not an arbitrary clock — **A** (framework, not a number). | Per account, cohorted | Product events + onboarding project system | Median TTV "compressed from 8.1 days (2022) to 4.2 days (2026)" across 412K signups / 38 products — **C**, single vendor-blog study, not independently verifiable. Use your own cohort baseline instead. |
| **Time to Value (TTV) / Time to Live** | Days from contract start to production go-live with the contracted primary use case | Per account | Onboarding/PS system | Report as median + P90, never mean. P90 is where the churn lives. |
| **Onboarding cycle time** | Days from contract signature to onboarding-complete milestone; decompose into: signature→kickoff, kickoff→config-complete, config→go-live, go-live→adoption-threshold | Monthly cohort | PS/onboarding tooling | Track **stalled onboarding ARR** ($ in accounts >X days past target go-live) as a distinct at-risk category. |
| **Activation rate** | `# accounts reaching the activation event within N days / # accounts starting in cohort`. Activation event must be empirically chosen as the usage behavior with the highest correlation to M6+ retention. | 7/14/30-day cohort | Product analytics | "Median activation 41.7%, P75 71%, P25 19%" — **C**, single vendor study. Amplitude's published rule: if ≥7% of an original cohort returns on day 7, the product is in the top quartile for activation (2025 Product Benchmark Report, 2,600+ companies) — **B**. Amplitude also reports 69% of top activation performers also lead in 3-month retention (10,600+ products) — **B**. |
| **Adoption breadth** | `# distinct core features used ≥1x in period / # core features in the entitled SKU`, at account level | Monthly | Product events | Define the "core feature" list once, with product, and freeze it. Breadth <40% at renewal is a contraction predictor. |
| **Adoption depth** | Usage volume per active user vs. the cohort P50 for accounts of the same size/plan (index, not raw count) | Monthly | Product events | Raw event counts are useless across account sizes. Always index. |
| **License / seat utilization** | `# licenses active in trailing 30 days / # licenses contracted` | Monthly | Product events × entitlement table | The single most direct contraction predictor in seat-based models. <60% utilization entering a renewal window is a red flag; <40% is near-certain seat reduction. Both thresholds are practitioner rules-of-thumb — **C** — but the *mechanism* is arithmetic, not opinion: the buyer will true down to observed usage. |
| **DAU/MAU (stickiness)** | `Avg DAU over period / MAU at period end` | Monthly | Product analytics | B2B SaaS typically **10–20%**; Mixpanel's cross-app average is **13%** — **B**. Daily-use tools 20–30%, weekly-use tools 10–15% — **C**. Only meaningful within a product category; a weekly-cadence tool is not unhealthy at 8%. Prefer **WAU/MAU** for weekly-cadence B2B products. |
| **Product Qualified Account (PQA)** | An account where a threshold share of users (commonly ≥50%) individually meet the PQL bar, or the account crosses a defined composite of usage depth, usage breadth, and limit proximity | Weekly | Product analytics + CRM | Three PQL signal families: **usage depth** (features explored, artifacts created), **usage breadth** (teammates invited, integrations connected), **limit proximity** (seat cap, storage quota, API call ceiling) — **B**. PQA count and PQA→expansion conversion rate belong on the CS report as leading indicators of the expansion line in the bridge. |
| **Executive sponsor coverage** | `# accounts with a named, verified exec sponsor engaged in last 90 days / # accounts` | Quarterly | CRM contact roles | Sponsor departure is one of the highest-signal single events in churn prediction. Instrument `sponsor_last_engagement_date` and `sponsor_departed_flag`. |
| **Multi-product / cross-sell attach** | `# accounts with ≥2 paid SKUs / # accounts`; also `avg SKUs per account` | Quarterly | Billing | Directly explains why NRR rises with product-portfolio breadth (Benchmarkit 2025 cites portfolio breadth as an NRR driver) — **A**. |

---

## 8. Health score, sentiment, and support

### 8.1 Health score

| Field | Guidance |
|---|---|
| **Construction** | 4–6 weighted measures, not 25. The dimension set CS platform scorecards converge on: **product usage** (breadth, depth, frequency, utilization), **support** (volume, severity, escalations, CSAT on tickets), **engagement** (exec sponsor activity, QBR attendance, enablement completion), **sentiment** (NPS/CSAT/CSM judgment), **commercial** (invoice aging, contract term remaining, prior downsells) — **C** (convergent vendor practice; no single citable source). |
| **Weighting** | Example practitioner weighting: usage 40% / support 25% / sentiment 20% / exec engagement 15% — **C**. On a 100-point scale, no single factor should be <10 or >20 points if you want a stable score — **C**. Weights must be **fit against observed churn**, not chosen in a workshop. |
| **Bands** | Green / Yellow / Red, with the boundaries published and fixed for the year. A widely used convention is Green 80–100 / Yellow 50–79 / Red <50 — **C** (convention, not a measured threshold). Fit the boundaries to your own observed churn rates, then never change them mid-year without restating history. |
| **Validation (mandatory)** | Back-test against ≥12 months and ≥50 churn events: did churned accounts score materially lower 30–60 days before cancellation? — **B**. Report the **lift**: `churn rate of Red / churn rate of Green`. If that ratio is under ~3x, the score has no predictive power and must not be used for forecasting. |
| **Trajectory beats level** | An account at 75 that was 95 two weeks ago is more at risk than a stable 65. Score **delta over 30/90 days** must be a first-class field (`health_score_delta_30d`). |
| **Distribution reporting** | Report both **count** distribution and **ARR-weighted** distribution across bands. They diverge, and the ARR-weighted one is the one the CFO cares about. |

**Health score migration (transition) matrix — the report artifact.** Rows = tier at start of quarter, columns = tier at end of quarter, plus a Churned column. This is the most under-used and most informative table in CS reporting because it shows *flow*, not *stock*.

Illustrative worked matrix, 1,370 accounts, Q4:

| Start ↓ / End → | Green | Yellow | Red | Churned | Start total | Qtr churn rate |
|---|---|---|---|---|---|---|
| **Green** | 731 | 65 | 8 | 8 | 812 | 1.0% |
| **Yellow** | 88 | 249 | 45 | 20 | 402 | 5.0% |
| **Red** | 9 | 38 | 78 | 31 | 156 | 19.9% |
| **End total** | 828 | 352 | 131 | 59 | 1,370 | 4.3% |

Read-outs an analyst must produce from this table:
- **Predictive lift** = Red churn ÷ Green churn = 19.9 / 1.0 = **20x**. The score works.
- **Net green flow** = (88+9) in − (65+8) out = **+24**. Health is improving on net.
- **Recovery rate from Red** = (9+38)/156 = **30.1%** of Red accounts improved a tier. This is the save motion's true efficacy.
- **Degradation rate from Green** = (65+8+8)/812 = **10.0%**. This is the leading indicator of next quarter's churn.
- **Unforecast churn** = 8 of 59 churned accounts (13.6%) were Green at quarter start. Every one of those requires a written post-mortem; they are the failures of the scoring model itself.

### 8.2 Sentiment metrics

| Metric | Formula | Scale | Cadence | Benchmarks |
|---|---|---|---|---|
| **NPS** | `% Promoters (9–10) − % Detractors (0–6)` | −100 to +100 | Relationship NPS 2x/yr; never more often than quarterly per respondent | B2B software/SaaS ≈ **41** (Retently, 2025–26) — **B**; B2B median ≈38 (Survicate) — **B**; SurveySparrow 2026 median ≈30 — **B**. Working consensus: median clusters **30–41**; >40 above median, >50 excelling — **B/C**. Report **response rate** alongside; NPS from a 6% response rate is not a measurement. Survey the **buying committee**, not only the daily user, and pair NPS with an explicit renewal-intent question — the score on its own does not tell you whether they intend to re-sign — **C** (practice guidance). |
| **CSAT** | `# responses rated 4–5 (or ≥8/10) / # responses × 100` | % | Transactional, per interaction | Cross-industry average ≈**78/100**; >80 good; top quartile ≥86 — **C**. B2B SaaS support CSAT ≈**68%** (with enterprise 72–75% and SMB 60–65%) — **C**, conflicting with other sources reporting SaaS CSAT ≈80%. Treat CSAT benchmarks as unreliable across sources; benchmark against your own trailing 12 months. |
| **CES** | "How easy was it to…" typically 1–7 | 1–7 | Transactional, post-onboarding and post-support | Industry medians cluster **4.8–5.6** on a 7-point scale; B2B software support 5.4–5.8; top quartile ≥6.2 — **C**. CES is the best of the three at predicting repurchase for *service* interactions; use it post-onboarding and post-ticket, not as a relationship metric. |
| **Sentiment coverage** | `# accounts with any sentiment response in trailing 12 months / # accounts` (ARR-weighted) | % | Quarterly | Below ~50% ARR coverage, the sentiment section of your report is anecdote. Report it. |

### 8.3 Support metrics (the ones that predict churn)

| Metric | Formula | Notes / benchmarks |
|---|---|---|
| **First Response Time (FRT)** | Median (not mean) business-hours minutes from ticket creation to first human/agent response, by priority | B2B SaaS email targets **<4h**, commonly 4–6h — **C**. Use median so weekend/outlier tickets don't distort. Report by priority band and by segment SLA. |
| **Time to Resolution (TTR)** | Median business-hours to `resolved`, by priority | Practitioner targets: P1 <1–4h, P2 <8 business hours, P3 <24 business hours, P4 <3 business days — **C**. |
| **SLA attainment** | `# tickets meeting contractual SLA / # tickets subject to SLA` | This is the contractual number; FRT/TTR are the operational ones. Both belong on the report. |
| **Backlog** | Open tickets at period end; **aged backlog** = open >X days; `backlog / avg weekly inbound` = weeks of backlog | Trend matters more than level. Rising aged backlog leads CSAT down by ~1 month and health scores down by ~2. |
| **Reopen rate** | `# tickets reopened after resolution / # tickets resolved` | Target **<5%**; >10% warrants systematic investigation — **C**. A 2022 survey of 260 companies (Endsight) found an average of **3.1%** — **B**. |
| **Escalation rate** | `# tickets escalated to L2/L3/engineering or to a manager / # tickets` | No credible cross-industry median exists. Forrester reports an average of **2.8 contacts per escalated issue** — **B**. Track your own trailing baseline and, critically, **escalations per account** — a single account generating repeated escalations is a churn signal regardless of the fleet-wide rate. |
| **First Contact Resolution (FCR)** | `# resolved on first contact / # contacts` | SQM Group 2025: average **70%**, top performers **85%** — **B**. |
| **Tickets per account per month** | `# tickets / # active accounts` (also per active user) | MetricNet cites ~**0.5 tickets per user per month** for top-performing support orgs — **B**. |
| **The bimodal churn signal** | Both extremes are risk: **zero** tickets in 12 months often means nobody is using the product; **≥7** tickets in 12 months indicates friction | Practitioner heuristic — **C** — but operationally valuable. Build it as a two-sided flag, not a monotonic "fewer tickets = healthier" rule. |

---

## 9. Usage-based and public-company methodology divergence (critical for benchmarking)

Public NDR disclosures are **not mutually comparable**. Never benchmark against a public NDR without reading the definition in the 10-K/S-1.

| Company | Measurement window | Cohort construction | Churn treatment | Grade |
|---|---|---|---|---|
| **Snowflake** | Trailing **two years** | Customers under capacity contracts who used the platform at any point in month 1 of year 1, including end-customers under reseller arrangements | Churned customers **remain in the cohort at $0** | A (SEC 8-K/10-K) |
| **Figma** (S-1) | Point of measurement, looking **backward** | Paid customers >$10K ARR **as of the measurement date** | Departed accounts **excluded entirely** — structurally inflationary | A (S-1); disclosed NRR 132% |
| **Klaviyo** | Weighted average of monthly point-in-time rates | Smooths volatility | Usage overages **excluded** | B |
| **Datadog / Elastic / Splunk / DigitalOcean** | Weighted average across trailing twelve months | Varies; DigitalOcean explicitly re-includes **re-engaged** customers | Varies | B |
| **Fastly** | Publishes **two** metrics: single-month and LTM NRR | Explicitly to damp usage volatility | — | B |
| **Confluent** | Dual ARR basis: platform = contractual commitments; cloud = annualized trailing-3-month consumption | — | — | B |

**Implications for your own usage-based NRR:**
- Use TTM or YoY, never single-month (Benchmarkit 2025 explicitly recommends this to capture seasonality) — **A**.
- Consider a two-year look-back (the "Snowflake model") if consumption ramps are long — **A** (Benchmarkit cites this as a best practice).
- Decide and disclose whether committed spend, consumed spend, or annualized run-rate consumption is the ARR basis. Changing it retroactively invalidates every trend line you have published.
- Benchmarkit CY2024: usage-based pricing had **higher** GRR (92% vs 88%) and hybrid subscription+usage had the highest NRR (110% median) — **A**.

---

## 10. CS capacity, coverage, and cost

| Metric | Formula | Benchmarks |
|---|---|---|
| **ARR per CSM (book of business)** | `ARR under management / # quota-carrying CSM FTEs` (exclude managers, ops, onboarding specialists — or state that you didn't) | Tomasz Tunguz, *How Much ARR Can a CSM Manage?* (2019): "most CSMs manage **$2–5M** ARR" — **B**, dated (secondary reporting; the underlying survey is not held in this library). 2025–26 vendor aggregations: ENT $2.5–4M (8–15 logos), MM $1.5–2.5M (25–45 logos), SMB pooled $1–1.8M (100–250 logos) — **C**. **No current Grade-A public benchmark for ARR/CSM exists.** Use it as an internal capacity-planning constant, not as an external benchmark. |
| **Accounts per CSM** | `# accounts / # CSM FTEs`, by segment and coverage model | 2025–26 vendor aggregations: ENT 10–50 (median ~22), MM 50–100 (median ~49), tech-touch 300–500+ — **C**. **No Grade-A public benchmark for accounts/CSM is held in this library** — treat these as orientation, not targets, and derive your own from section 3 of `cs-context`. |
| **Coverage ratio (by tier)** | `# accounts in tier requiring named coverage / # CSMs assigned to tier`; also `% of ARR under named 1:1 coverage` vs. `pooled` vs. `digital-only` | Report as an **ARR coverage waterfall**: % ARR with named CSM / pooled CSM / digital-only / no coverage. "Uncovered ARR" is a board-relevant risk number. |
| **CS + Support cost as % of ARR** | `Fully loaded CS + Support opex / ARR` | SaaS Capital 2026 spending benchmarks (survey Mar 2026, 1,000+ private B2B SaaS): median **9%** of ARR for customer support + customer success, up from 8% prior year — **A**. $3–5M ARR companies: **10%** — **A**. Equity-backed companies spend **~2x** bootstrapped on CS — **A**. |
| **Cost to serve** | `Fully loaded CS + Support cost for a segment / ARR in that segment` | The number that decides whether SMB gets a human. If SMB cost-to-serve exceeds SMB gross margin contribution, the answer is digital-led, full stop. |
| **ARR per FTE (company-wide)** | `End-of-period ARR / total FTEs` (Benchmarkit glossary) | CY2024: **$240,000** for $50–100M ARR companies; **$283,379** for >$100M (Benchmarkit 2025, N=174) — **A**. |
| **CSM utilization / touch coverage** | `# accounts with a logged meaningful touch in last 90 days / # assigned accounts` | Below ~70% for a named-coverage tier means the book is oversized regardless of the ARR number. |
| **Expansion ownership** | Who is comped on expansion | **UNKNOWN — no neutral public benchmark is held in this library.** Record your own split (CS / AM / Sales), whether CS carries an expansion quota, and how it has moved year over year; write it into `cs-context` §4. The split matters for role design and comp, and no external median tells you whether yours is right — the diagnostic is whether expansion ARR (section 5) is being produced at all. |

---

## 11. Renewal operations metrics

| Metric | Formula | Window | Notes |
|---|---|---|---|
| **At-Risk ARR** | `Σ ARR of accounts flagged at-risk` — where "at-risk" is a *declared, dated, reason-coded* state, not a health-score band | Point in time, with a renewal-date horizon (next 90 / 180 / 365 days) | Must be reported three ways: (1) total, (2) within the next-two-quarters renewal window, (3) net of the mitigation plan's expected save. Report **risk reason mix** (product gap / champion loss / budget / M&A / competitive / value not realized / pricing). |
| **Risk detection rate** | `ARR that was flagged at-risk ≥60 days before loss / total ARR lost` | TTM | The honest measure of whether your early-warning system works. Anything under ~60% means most churn is a surprise and your forecast is fiction. |
| **Save rate** | `ARR retained from accounts that entered the at-risk state / ARR that entered the at-risk state and reached its renewal date` | TTM | Define entry and exit criteria in writing. A save rate computed on an undisciplined risk list is meaningless — teams will flag everything to inflate the numerator. |
| **Renewal forecast accuracy** | `1 − |Called renewal ARR − Closed renewal ARR| / Called renewal ARR`, measured at Day 1, Day 45 and Day 90 of the quarter | Quarterly | Publish it next to the sales forecast accuracy number. A well-run manual renewal forecast lands near **90%**; automated/platform-assisted forecasts target **95%** held from day 1 through day 90 — **C** (vendor claim). Also report **directional bias** (are you systematically optimistic?) — bias is more damaging than variance. |
| **Renewal rate by ATR** | See §2.3 | Quarterly | Always show ATR $ alongside; a 95% renewal rate on a light ATR quarter is not a signal. |
| **Win-back rate** | `# (or ARR of) churned accounts returning within N months / # churned accounts in the base period`, N typically 12 or 24 | Cohorted on churn date | Distinguish from reactivation *dollars* in the bridge. Report separately by churn reason — win-back from "budget cut" behaves nothing like win-back from "product gap". |
| **Advocacy rate** | `# customers who completed ≥1 advocacy action (reference call, case study, review, speaking, referral) in trailing 12 months / # eligible customers` | TTM | Reference participation of **15–25%** among enterprise customers is cited as healthy B2B SaaS — **C**. General "advocacy rate >30% healthy, >40% exceptional" — **C**. Also track **reference supply vs. demand**: `# reference requests fulfilled / # requested`. A supply gap is a measurable revenue drag. |
| **Referral / customer-sourced pipeline** | `Pipeline $ sourced from existing customers / total pipeline $` | Quarterly | The most defensible way to put a revenue number on advocacy. |
| **QBR/EBR coverage** | `# accounts with a completed EBR in trailing 2 quarters / # accounts in the named-coverage tier` (ARR-weighted) | Quarterly | Pair with **EBR outcome** classification (expansion identified / risk identified / neutral). Coverage without outcomes is activity theater. |

---

## 12. Worked example: full ARR bridge and derived metrics

**Company:** private B2B SaaS, $100M beginning ARR, three segments, annual contracts, subscription pricing, 81% subscription gross margin.

### 12.1 Annual bridge ($M)

| Component | Amount | % of Beginning ARR |
|---|---:|---:|
| Beginning ARR (Jan 1) | 100.0 | — |
| **+ New logo ARR** | 18.4 | 18.4% |
| **+ Expansion ARR** | 12.3 | 12.3% |
| **+ Reactivation ARR** | 0.7 | 0.7% |
| **− Contraction ARR** | (4.1) | (4.1%) |
| **− Churned ARR** | (9.8) | (9.8%) |
| **= Ending ARR (Dec 31)** | **117.5** | — |
| Net New ARR | 17.5 | 17.5% growth |

### 12.2 Quarterly bridge ($M)

| Quarter | Beg | New | Expansion | Reactivation | Contraction | Churn | End | Quick Ratio |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Q1 | 100.0 | 3.9 | 2.6 | 0.1 | (1.0) | (2.9) | 102.7 | 1.69 |
| Q2 | 102.7 | 4.3 | 2.9 | 0.2 | (0.9) | (2.1) | 107.1 | 2.47 |
| Q3 | 107.1 | 4.6 | 3.1 | 0.2 | (1.1) | (2.4) | 111.5 | 2.26 |
| Q4 | 111.5 | 5.6 | 3.7 | 0.2 | (1.1) | (2.4) | 117.5 | 2.71 |
| **FY** | **100.0** | **18.4** | **12.3** | **0.7** | **(4.1)** | **(9.8)** | **117.5** | **2.26** |

*(Quick ratio here = (New + Expansion + Reactivation) / (Churn + Contraction). Strict form excluding reactivation: FY = 30.7/13.9 = 2.21.)*

### 12.3 Cohort attribution — why the formula method is wrong

Of the FY movements, some belong to logos acquired *inside* the year and therefore are **not** in the Jan-1 cohort:

| Movement | Total | From Jan-1 cohort | From in-year new logos |
|---|---:|---:|---:|
| Churn | 9.8 | 9.2 | 0.6 |
| Contraction | 4.1 | 3.9 | 0.2 |
| Expansion | 12.3 | 10.9 | 1.4 |
| Reactivation | 0.7 | 0.0 | 0.7 (by definition outside the cohort) |

| Metric | Correct (cohort) | Common wrong answer | Error |
|---|---:|---:|---|
| **GRR** | (100 − 9.2 − 3.9)/100 = **86.9%** | (100 − 9.8 − 4.1)/100 = 86.1% | Formula method understates GRR by 80bps by charging first-year-logo churn to the cohort |
| **NRR** | (100 − 9.2 − 3.9 + 10.9)/100 = **97.8%** | (100 + 12.3 − 4.1 − 9.8)/100 = 98.4% | Formula method **overstates** NRR by 60bps |
| **NRR (worse error: + reactivation)** | — | (100 + 12.3 + 0.7 − 4.1 − 9.8)/100 = 99.1% | +130bps |
| **NRR (worst error: + new logos)** | — | 117.5/100 = 117.5% | That is the **growth rate**, not NRR |

### 12.4 Segment cut (this is the table an exec reads first)

| Segment | Beg ARR | New | Expansion | React | Contraction | Churn | End ARR | Cohort GRR | Cohort NRR |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Enterprise (>$150K ACV) | 55.0 | 9.6 | 8.1 | 0.2 | (2.2) | (3.1) | 67.6 | **90.4%** | **104.2%** |
| Mid-Market ($25–150K) | 32.0 | 6.2 | 3.4 | 0.3 | (1.4) | (3.6) | 36.9 | **85.0%** | **93.8%** |
| SMB (<$25K) | 13.0 | 2.6 | 0.8 | 0.2 | (0.5) | (3.1) | 13.0 | **76.9%** | **80.8%** |
| **Total** | **100.0** | **18.4** | **12.3** | **0.7** | **(4.1)** | **(9.8)** | **117.5** | **86.9%** | **97.8%** |

*(Cohort GRR/NRR use only the Jan-1-cohort movements from §12.3, allocated: cohort churn ENT 3.1 / MM 3.5 / SMB 2.6; cohort contraction 2.2 / 1.3 / 0.4; cohort expansion 7.6 / 2.8 / 0.5.)*

### 12.5 Logo bridge and the dollar-vs-logo diagnostic

| Segment | Beg logos | Avg ARR/acct | Cohort logos churned | Cohort logo retention | Avg ARR of churned acct | Churned/avg size index |
|---|---:|---:|---:|---:|---:|---:|
| Enterprise | 110 | $500K | 5 | **95.5%** | $620K | **1.24x** |
| Mid-Market | 380 | $84.2K | 43 | **88.7%** | $81.4K | 0.97x |
| SMB | 750 | $17.3K | 90 | **88.0%** | $28.9K | **1.67x** |
| **Total** | **1,240** | **$80.6K** | **138** | **88.9%** | **$66.7K** | 0.83x |

FY logo bridge: 1,240 beginning + 268 new + 11 reactivated − 149 churned (138 cohort + 11 in-year) = **1,370 ending**.

**The analyst read-out this table forces:**
> "Blended logo retention of 88.9% looks acceptable and blended dollar churn (9.2%) is *below* logo churn (11.1%), which superficially says we lose small accounts. That blended read is wrong. Inside SMB we lose accounts that are 1.67x the average SMB size — we are losing the best SMB customers, which is why SMB GRR (76.9%) is 11 points worse than SMB logo retention (88.0%). And in Enterprise, the five accounts we lost averaged $620K against a $500K book average. In both segments, churn is adversely selected toward our larger customers. The blended number hides both facts."

### 12.6 Renewal, risk and save metrics from the same year

| Metric | Calculation | Result |
|---|---|---:|
| ATR (ARR up for renewal in FY) | given | $78.5M |
| Gross $ renewal rate | (78.5 − 9.2 − 3.9)/78.5 | **83.3%** |
| GRR (total ARR base) | (100 − 9.2 − 3.9)/100 | 86.9% |
| ARR that entered at-risk state and reached renewal | given | $22.0M |
| Of which retained | given | $14.6M |
| **Save rate** | 14.6/22.0 | **66.4%** |
| Loss that was flagged at-risk ≥60 days out | 22.0 − 14.6 = 7.4 of 13.1 total loss | — |
| **Risk detection rate** | 7.4/13.1 | **56.5%** |
| **Unforecast (surprise) loss** | 13.1 − 7.4 | **$5.7M (43.5%)** |
| Q4 renewal forecast accuracy | called $19.8M vs closed $18.9M | **95.5%**, biased +4.8% optimistic |

> Note the relationship: gross **renewal** rate (83.3%) < **GRR** (86.9%) because the ATR denominator is smaller than total ARR. These are different metrics; benchmarking one against the other's benchmark is a classic error.

### 12.7 Unit economics from the same year

| Metric | Calculation | Result |
|---|---|---:|
| ARPA (ending) | 117.5M / 1,370 | $85.8K |
| Subscription gross margin | given (= Benchmarkit CY2024 median) | 81% |
| Gross revenue churn rate | 1 − GRR | 13.1% |
| **LTV, naive** | 85.8 / 0.131 | **$655K** ← do not use |
| **LTV, GM-adjusted** | 85.8 × 0.81 / 0.131 | **$530K** |
| **LTV, GM-adjusted + 10% discount** | 69.5 / (0.10 + 0.131) | **$301K** |
| **LTV, expansion-aware (net churn 2.2%) + 10% discount** | 69.5 / (0.10 + 0.022) | **$570K** |
| New-logo-allocated S&M | given | $27.0M |
| New CAC per logo | 27.0M / 268 | $100.7K |
| **New CAC Ratio** | 27.0 / 18.4 | **$1.47** (vs Benchmarkit CY2024 median $2.00 — A) |
| **CAC Payback** | 27.0 / (18.4 × 0.81) × 12 | **21.7 months** |
| **LTV:CAC (GM-adjusted, undiscounted)** | 530 / 100.7 | **5.3 : 1** |
| **LTV:CAC (discounted)** | 301 / 100.7 | **3.0 : 1** |

> The 2.2x spread between the naive and the discounted LTV ($655K vs $301K) is exactly why the LTV method must be stated on the slide. Any LTV:CAC ratio quoted without its formula is unreviewable.

---

## 13. The standard monthly CS / retention report

Publish on a fixed calendar date (business day 5 or 8, after the billing close is locked). The ARR bridge must **tie to finance's ARR** to the dollar; if it doesn't, the report does not ship.

### 13.1 Required sections, in order

| # | Section | Content | Format |
|---|---|---|---|
| **0** | **Headline block** (top of page 1, ≤6 numbers) | TTM NRR, TTM GRR, logo retention, MoM/QoQ ARR bridge net, at-risk ARR in next 2 quarters, renewal forecast for current quarter — each with prior period, variance to plan, and a ▲/▼ arrow | 6 KPI tiles |
| **1** | **The call** (3–5 sentences) | What happened, why, what we are doing, what changes in the forecast. Written before any chart. | Prose |
| **2** | **ARR bridge** | Month, QTD, and TTM bridges. Waterfall chart + table. Must tie to finance. | Waterfall + table |
| **3** | **Retention detail** | GRR/NRR TTM, by segment, by ACV band, by product, by region. Both cohort values and the movement decomposition. | Table + small-multiple trend lines |
| **4** | **Churn & contraction post-mortem** | Every churned/contracted account above a materiality threshold (e.g., >$50K ARR, or top 10 by ARR): account, ARR, tenure, segment, reason code, health at −90d, whether flagged, owner, what we learned. | Table, one row per account |
| **5** | **Renewals & forecast** | ATR by quarter for next 4 quarters; current-quarter called vs. closed vs. plan; forecast accuracy and bias for the trailing 4 quarters; top 10 renewals by ARR with status. | Table |
| **6** | **At-risk pipeline** | At-risk ARR by reason code, by renewal quarter, by segment; movement in/out of at-risk this month; save rate TTM; risk detection rate TTM. | Stacked bar + table |
| **7** | **Expansion pipeline** | Expansion ARR closed MTD/QTD/TTM vs. plan; expansion pipeline by stage; PQA count and PQA→opportunity conversion; multi-product attach. | Table |
| **8** | **Health & leading indicators** | Health distribution (count and ARR-weighted); **migration matrix** vs. prior period; predictive lift (Red÷Green churn); adoption breadth/depth index; license utilization distribution; DAU/WAU/MAU. | Matrix + distribution |
| **9** | **Onboarding & time-to-value** | Cohort table of last 6 monthly cohorts: median and P90 TTFV, TTV, % on-time go-live, stalled-onboarding ARR, activation rate. | Cohort table |
| **10** | **Voice of customer** | NPS/CSAT/CES with response rates and ARR coverage; top 5 detractor themes with ARR attached; theme trend vs. prior quarter. | Table |
| **11** | **Support health** | FRT/TTR medians by priority, SLA attainment, backlog and aged backlog, reopen rate, escalation count, accounts with escalation clusters. | Table |
| **12** | **Team & capacity** | ARR/CSM and accounts/CSM by segment vs. target; ARR coverage waterfall (named / pooled / digital / uncovered); open reqs; touch coverage %. | Table |
| **13** | **Cohort & survival appendix** | Logo and dollar cohort retention triangles; survival curve by acquisition channel and by ACV band; cohort-quality drift on the last 6 cohorts. | Triangles + curves |
| **14** | **Definitions & change log** | Every formula, every window, every threshold — plus a dated log of any definition change and its restated impact. | Appendix |

### 13.2 Required charts (and the correct chart for each job)

| Job | Chart | Anti-pattern to avoid |
|---|---|---|
| Show how ARR changed | **Waterfall** | Stacked bar of ending ARR by segment — shows stock, not flow |
| Show retention trend | **Line, TTM, with segment small multiples** | One blended line |
| Show cohort behavior | **Triangle heat map** (rows = cohort, cols = tenure) | Averaging cohorts of different ages together |
| Show churn timing | **Hazard bar chart by tenure bucket** | Cumulative survival only |
| Show health movement | **Migration matrix** (heat-shaded) | Pie chart of current health distribution |
| Show renewal exposure | **ATR by quarter, stacked by health tier** | A single "renewals this year" number |
| Show risk composition | **Stacked bar of at-risk ARR by reason code** | A count of "at-risk accounts" |
| Show concentration | **Pareto: cumulative % ARR vs. ranked accounts** | Mean ACV |

### 13.3 Required commentary structure (per section)

Every section gets exactly this five-part structure. No exceptions, no free-form paragraphs.

1. **What** — the number, the prior period, the variance to plan. ("TTM GRR 86.9%, −40bps QoQ, −110bps vs. plan of 88.0%.")
2. **Where** — the segment/product/cohort concentration of the variance, with the arithmetic. ("94% of the miss is SMB: SMB GRR 76.9% vs. plan 84%. Enterprise and MM are on plan.")
3. **Why** — root cause with evidence, not hypothesis. ("Of $3.1M SMB churn, $1.9M carried reason code 'never reached go-live'; those accounts had a median TTV of 71 days vs. a 30-day target.")
4. **So what** — the forward-looking implication, quantified. ("At current SMB cohort hazard, FY+1 SMB GRR lands at 77–79%, a $1.1M ARR drag vs. plan.")
5. **Now what** — the decision or ask, with an owner and a date. ("Recommend gating SMB onboarding on a 30-day activation milestone and shifting 2 onboarding FTEs from MM. Owner: VP Onboarding. Decision needed by [date].")

Banned commentary: "we will continue to monitor," "engage proactively," "focus on adoption," any sentence with no number in it, and any explanation that cannot be falsified.

### 13.4 What an exec wants first

In order, an exec (CEO/CFO/CCO) reads:
1. **Did we hit the ARR number, and if not, which line of the bridge broke.**
2. **Is the retention trend inflecting** (TTM GRR direction, 3 periods).
3. **What is the exposure in the next two quarters** (ATR × at-risk).
4. **Is the forecast credible** (last 4 quarters' forecast accuracy and bias).
5. **What decision do you need from me.**

Everything else is appendix. If it takes more than 90 seconds to answer those five, the report is badly built.

### 13.5 What the board deck needs (different document, 3–5 slides)

| Slide | Content | Notes |
|---|---|---|
| 1 | **ARR bridge**, 8 quarters, with NRR/GRR trend overlaid | One slide, no builds |
| 2 | **Retention by segment / ACV band**, TTM, with the peer benchmark band drawn in and cited (source + year on the slide) | Boards benchmark; give them the citation so they don't use a worse one |
| 3 | **Cohort retention triangle** (dollar), last 8–12 cohorts | This is the slide that proves whether the business is structurally improving |
| 4 | **Renewal exposure + concentration**: next-4-quarter ATR, top-10 ARR concentration, named top-10 renewal status | Risk disclosure |
| 5 | **The one thing we are changing**, with the expected ARR impact and the date we will know if it worked | |

Board-specific rules: annual/TTM basis only (never a single month), constant currency, restate history whenever a definition changes and say so on the slide, and never introduce a new metric to the board without also showing its prior 8 periods.

### 13.6 MoM / QoQ / YoY comparison rules

| Rule | Detail |
|---|---|
| **Retention is never MoM** | GRR/NRR/logo retention are reported **TTM** or **YoY** only. A monthly NRR is dominated by contract-renewal timing, not by customer behavior. If you must show a monthly series, show TTM-NRR-as-of-that-month. |
| **Bridge is MoM and QTD** | The ARR bridge is the one artifact that is legitimately monthly. |
| **Renewals are quarterly, on the ATR calendar** | Compare Q4 to Q4, not Q4 to Q3, unless ATR is genuinely flat across quarters. Always print the ATR $ next to the rate. |
| **Seasonality** | If >30% of ATR lands in one quarter, YoY is the only valid comparison for renewal metrics. Print the ATR seasonality curve once a year so nobody forgets. |
| **Comparability guard** | Any period with an acquisition, a re-segmentation, a pricing-model change, or a definition change must be flagged in the chart and, where material, shown both as-reported and pro-forma. |
| **Cohort maturity guard** | Never compare a 4-month-old cohort's M12 retention to anything — it doesn't have one. Grey out immature cells in cohort triangles. |
| **Small-n guard** | Suppress or asterisk any segment cell with n < 20 accounts or < $2M ARR. (Benchmarkit itself flags this: its >$100M ARR expansion cohort had n=6.) |
| **Rate + absolute, always** | Every % gets its numerator and denominator printed. "Churn improved to 4.1%" alongside a shrinking denominator is a lie by omission. |
| **Restatement policy** | Publish restatements as a separate line with the reason. Silent restatement destroys the credibility of every number you have ever published. |

---

## 14. Anti-patterns of CS reporting

| # | Anti-pattern | Why it's fatal | Fix |
|---|---|---|---|
| 1 | **Blended-only retention** | A 97.8% blended NRR hides ENT 104.2% / SMB 80.8%. The blended number cannot be acted on by anyone. | Always segment by ACV band first; it is the most predictive cut. |
| 2 | **NRR without GRR** | Expansion from 20 accounts can mask churn in 200. | Publish them adjacent, always, with the same denominator. |
| 3 | **Survivor-biased denominators** | Dropping churned accounts, or computing retention "as of today, looking back" (Figma-style), structurally inflates the number. | Freeze the cohort at t0; churned accounts stay at $0. |
| 4 | **New logos leaking into the retention cohort** | Turns NRR into a growth rate. | Cohort membership frozen at t0, enforced in the query. |
| 5 | **Reactivation counted as retention** | Win-backs are new revenue, not retained revenue. | Bridge line: yes. NRR/GRR numerator: no. |
| 6 | **Single-month NRR in a usage-based business** | Pure noise; consumption seasonality dominates. | TTM or 2-year look-back. |
| 7 | **Health scores that don't predict** | If Red-tier churn isn't ≥3x Green-tier churn, the score is decoration. | Publish the predictive lift every quarter. Retire scores that fail. |
| 8 | **Activity metrics as outcomes** | QBRs held, emails sent, touches logged. None of these are results. | Every activity metric must be paired with the outcome it produced (EBR → expansion identified / risk identified). |
| 9 | **Vanity-metric selection** | Reporting only the metrics trending up. | Fix the metric set for a year. Changes go in the change log with a reason. |
| 10 | **Rates without denominators** | "Churn improved to 4.1%" when the base shrank 20%. | Print numerator and denominator on every rate. |
| 11 | **Mean instead of median for latency metrics** | One 40-day ticket destroys a mean FRT. | Median + P90 for all time-based metrics. |
| 12 | **Lagging indicators only** | NRR and churn tell you what already happened; by then the decision was made months ago. | Pair every lagging metric with its leading counterpart: GRR ← health degradation rate, license utilization, TTV miss rate, sponsor loss, support escalation clusters. |
| 13 | **30-metric dashboards** | Analysis paralysis; nobody can name the top 3. | 6 headline metrics, ≤15 in the body, everything else in the appendix. |
| 14 | **Retention numbers that don't tie to finance** | The instant the CFO finds a variance, the entire report is discarded. | Reconcile to the billing system every close; publish the reconciliation. |
| 15 | **Benchmarking against an incomparable population** | ChartMogul's B2B median NRR of 82% and Benchmarkit's 101% are both correct — for different populations. | Always state the benchmark's population, ARR floor, ACV mix, and year. |
| 16 | **Silent definition changes** | Destroys all trend lines retroactively. | Dated change log + restated history. |
| 17 | **Attributing all churn to CS** | M&A consolidation, business failure, and product-strategy sunsets are not CSM performance. | Reason-code every churn; report a "controllable vs. uncontrollable" split and defend the classification. |
| 18 | **Save rate on an undisciplined risk list** | Teams flag everything, inflating the numerator. | Written entry/exit criteria, dated, auditable, with the risk detection rate reported next to the save rate. |
| 19 | **Anecdote as evidence** | "Customers are telling us…" with n=3. | Attach ARR and account count to every qualitative theme. |
| 20 | **No decision attached** | A report that changes nothing is a cost center. | Section 5 of every commentary block: owner, decision, date. |

---

## 15. Master benchmark table (quick reference)

| Metric | Value | Population / segment | Source | Year | Grade |
|---|---|---|---|---|---|
| GRR median | 88% | Private B2B SaaS, N=225 | Benchmarkit 2025 SaaS Performance Metrics | CY2024 | A |
| GRR median | 84% (P75 91%, P25 76%) | SaaS + AI-native, N=226 | 2026 Aleph × Benchmarkit | CY2025 | B |
| GRR, usage-based pricing | 92% (P25 88%, P75 96%) | Private B2B SaaS | Benchmarkit 2025 | CY2024 | A |
| GRR, best-in-class MM/ENT | ~95% | B2B SaaS, min $250K ARR | ChartMogul | 2024–25 | A |
| NRR median | 101% | Private B2B SaaS, N=228 | Benchmarkit 2025 | CY2024 | A |
| NRR median | 102% (P75 110%, P25 92%) | SaaS + AI-native, N=230 | 2026 Aleph × Benchmarkit | CY2025 | B |
| NRR, hybrid sub+usage pricing | 110% | Private B2B SaaS | Benchmarkit 2025 | CY2024 | A |
| NRR, $25–50K ACV | 102% (P75 111%, P25 97%) | Private B2B SaaS, $1M+ ARR | SaaS Capital 2025 Retention Benchmarks | 2025 | A |
| NRR median | 82% (P75 97%) | ~2,700 B2B SaaS, min $250K ARR — self-serve skew | ChartMogul "AI churn wave" | Sept 2025 | A |
| Expansion ARR % of total new ARR | 40% median | Private B2B SaaS, N=81 | Benchmarkit 2025 | CY2024 | A |
| Expansion ARR % — $50–100M ARR | 58% | Private B2B SaaS | Benchmarkit 2025 | CY2024 | A |
| Expansion ARR % — >$100M ARR | 67% (n=6, fragile) | Private B2B SaaS | Benchmarkit 2025 | CY2024 | A |
| New CAC Ratio | $2.00 median; Q4 $2.82 | N=73 | Benchmarkit 2025 | CY2024 | A |
| Blended CAC Ratio | $1.40 median | N=43 | Benchmarkit 2025 | CY2024 | A |
| Expansion CAC Ratio | $1.00 median | N=21; <20% of cos. measure it | Benchmarkit 2025 | CY2024 | A |
| CAC payback median | 16 mo (P25 ≤6, P75 ≥24) | N=198 | 2026 Aleph × Benchmarkit | CY2025 | B |
| Subscription gross margin | 81% median | N=76 | Benchmarkit 2025 | CY2024 | A |
| Total gross margin | 77% median | N=196 | Benchmarkit 2025 | CY2024 | A |
| Prof. services gross margin | 30% | N=38 | Benchmarkit 2025 | CY2024 | A |
| ARR per FTE | $240K ($50–100M ARR); $283,379 (>$100M) | N=174 | Benchmarkit 2025 | CY2024 | A |
| Growth rate | 26% median; P75 50% | N=149 | Benchmarkit 2025 | CY2024 | A |
| CS + Support spend | 9% of ARR median (10% at $3–5M ARR) | 1,000+ private B2B SaaS | SaaS Capital Spending Benchmarks | 2026 | A |
| B2B SaaS annual churn | 3.5% (2.6% voluntary + 0.8% involuntary) | Recurly subscription network | Recurly 2025 Churn Report | 2025 | A |
| ARR per CSM | "most CSMs manage $2–5M" | — | Tomasz Tunguz | 2019 (dated) | B |
| NPS, B2B software/SaaS | ~41 (Retently); ~38 (Survicate); ~30 (SurveySparrow) | Cross-vendor | Multiple | 2025–26 | B |
| DAU/MAU, B2B+B2C SaaS apps | ~13% average | Mixpanel product benchmarks | Mixpanel | recent | B |
| Day-7 return ≥7% of cohort = top quartile activation | 7% | 2,600+ companies | Amplitude Product Benchmark Report | 2025 | B |
| FCR average / top | 70% / 85% | Contact centers | SQM Group | 2025 | B |
| Ticket reopen rate average | 3.1% | 260 companies | Endsight survey | 2022 | B |
| SaaS Quick Ratio target | 4.0 | — | Mamoon Hamid, SaaStr | 2015 | C (convention) |
| LTV:CAC target | 3:1 | — | David Skok, Matrix Partners | ~2010 | C (convention) |
| Rule of 40 / Magic Number thresholds | 40 / 0.75–1.0 | — | Industry convention | — | C |

---

## 16. Sources

**Grade A — primary, methodology disclosed**
- Benchmarkit, *2025 B2B SaaS Performance Metrics Benchmarks* (CY2024 actuals; N=563 participants, per-metric N noted inline; glossary of formulas on p.69–70) — https://www.benchmarkit.ai/2025benchmarks
- SaaS Capital, *What is a Good Retention Rate for a Private SaaS Company in 2025?* / 2025 Retention Benchmarks — https://www.saas-capital.com/blog-posts/what-is-a-good-retention-rate-for-a-private-saas-company/
- SaaS Capital, *2026 Spending Benchmarks for Private B2B SaaS Companies* (survey Mar 2026, 1,000+ companies) — https://www.saas-capital.com/blog-posts/spending-benchmarks-for-private-b2b-saas-companies/
- ChartMogul, *The SaaS Retention Report: The AI Churn Wave* (Sept 2025; ~2,700 B2B SaaS, ~600 B2C, ~200 AI-native; $250K ARR floor) — https://chartmogul.com/reports/saas-retention-the-ai-churn-wave/
- SaaS Metrics Standard Board — NRR, GRR, Logo Retention standards — https://www.saasmetricsboard.com/net-revenue-retention · /gross-revenue-retention · /logo-retention
- Snowflake Inc. SEC Form 8-K / 10-K NDR methodology — https://www.sec.gov/Archives/edgar/data/1640147/
- Recurly, *2025 Churn Report* / churn benchmarks — https://recurly.com/research/churn-rate-benchmarks/
- Bessemer Venture Partners, *Cloud 100 Benchmarks Report 2025* — https://www.bvp.com/atlas/the-cloud-100-benchmarks-report
- *Predictability & explainability of survival analysis in churn prediction*, Journal of Marketing Analytics (Springer), 2025 — https://link.springer.com/article/10.1057/s41270-025-00450-2

**Grade B — secondary reporting a named primary study**
- Aleph, *GRR / NRR / CAC Payback benchmarks (2026)* summarizing the 2026 Aleph × Benchmarkit SaaS & AI Performance Benchmarks (CY2025, N=342) — https://www.getaleph.com/answers/gross-revenue-retention-saas-2026 · /net-revenue-retention-saas-2026 · /cac-payback-period-saas-2026
- Ordway Labs, *Net Revenue Retention for Usage-Based Pricing* + *How public SaaS companies report NRR* — https://ordwaylabs.com/blog/net-revenue-retention-for-usage-based-pricing/
- Mostly Metrics, *How Public Companies Calculate Net Dollar Retention* (Figma, Snowflake, Confluent, Klaviyo) — https://www.mostlymetrics.com/p/how-public-companies-calculate-net
- Baremetrics Open Benchmarks — SaaS churn by ARPU band (2025; relayed secondhand via an aggregator, not verified against the primary)
- Tomasz Tunguz, *How Much ARR Can a CSM Manage?* (2019; secondary reporting of a vendor survey not held in this library) — https://tomtunguz.com/how-much-arr-can-a-csm-manage/
- Amplitude, *Product Benchmark Report* / *The 7% Retention Rule* — https://amplitude.com/blog/7-percent-retention-rule
- Mixpanel, benchmarks — https://mixpanel.com/benchmarks/
- Retently / Survicate NPS benchmarks — https://www.retently.com/blog/good-net-promoter-score/ · https://survicate.com/nps-benchmarks/
- Lincoln Murphy, *Success Milestones* — https://sixteenventures.com/success-milestones/
- Elena Verna, *B2B Product-Led Sales Guide* (PQL/PQA signal families) — https://www.elenaverna.com/p/b2b-product-led-sales-guide
- ChartMogul, *SaaS Quick Ratio* — https://chartmogul.com/blog/saas-quick-ratio/ ; Kellblog, *LTV:CAC* — https://kellblog.com/2014/07/30/the-ultimate-saas-metric-ltv-cac/

**Grade C — practitioner heuristics / unverified aggregations (flagged inline; never quote as measured benchmarks)**
CSAT/CES industry bands, escalation-rate and backlog "benchmarks", DAU/MAU category targets, health-score band churn probabilities, 2025–26 ARR-per-CSM and accounts-per-CSM ranges, time-to-value compression figures, "60–70% of churn in the first 90 days", renewal-forecast-accuracy vendor claims, advocacy/reference participation ranges, the Quick Ratio 4.0 target, and the LTV:CAC 3:1 convention.
