# The Board Slide Set

> Ten slides, an appendix, and a one-page pre-read. This file specifies each slide's purpose,
> chart type, exact fields, the sentence that must sit beneath it, the question a director
> will ask, and the failure mode that kills it.

**Contents**
1. [Governing rules](#1-governing-rules)
2. [Slide 1 — The number and the call](#2-slide-1--the-number-and-the-call)
3. [Slide 2 — ARR bridge](#3-slide-2--arr-bridge)
4. [Slide 3 — NRR / GRR trend with a benchmark band](#4-slide-3--nrr--grr-trend-with-a-benchmark-band)
5. [Slide 4 — Retention by segment and ACV band](#5-slide-4--retention-by-segment-and-acv-band)
6. [Slide 5 — Cohort retention](#6-slide-5--cohort-retention)
7. [Slide 6 — Concentration and dependency](#7-slide-6--concentration-and-dependency)
8. [Slide 7 — Exposure: ATR and at-risk coverage](#8-slide-7--exposure-atr-and-at-risk-coverage)
9. [Slide 8 — Forecast credibility](#9-slide-8--forecast-credibility)
10. [Slide 9 — CS efficiency](#10-slide-9--cs-efficiency)
11. [Slide 10 — The one strategic issue and the ask](#11-slide-10--the-one-strategic-issue-and-the-ask)
12. [The pre-read](#12-the-pre-read)
13. [Appendix discipline](#13-appendix-discipline)
14. [What must never appear](#14-what-must-never-appear)
15. [Chart selection](#15-chart-selection)
16. [Sources](#16-sources)

---

## 1. Governing rules

| Rule | Reason |
| --- | --- |
| **TTM or cohort basis only.** Never a single month. | Monthly retention is dominated by contract-renewal timing, not customer behaviour. |
| **Constant currency, or say you did not.** | An FX swing presented as retention movement is a fabrication by omission. |
| **Every rate prints its numerator and denominator.** | "Churn improved to 4.1%" on a base that shrank 20% is a lie that survives one quarter. |
| **Every benchmark prints source · year · population · N · evidence label.** | Boards benchmark whether you supply one or not. Supply the good one so they do not use a worse one. |
| **Never introduce a metric without its prior 8 periods.** | A number with no history is judged on your tone. |
| **The metric set is fixed for the year.** Changes go in the change log with a reason. | Vanity-metric rotation — reporting only what is trending up — is detectable and fatal. |
| **One message per slide. No builds.** | Ten slides in eight minutes leaves time for the discussion that produces the decision. |
| **Reserve ≥ one third of the slot for discussion** [P]. | A pack that consumes the whole meeting produced no decision. |

---

## 2. Slide 1 — The number and the call

| Field | Spec |
| --- | --- |
| **Purpose** | Prove you know what happened and said it first. |
| **Format** | Six KPI tiles + 3–5 sentences of prose. No chart. |
| **Tiles** | TTM GRR · TTM NRR · TTM logo retention · net new ARR from the bridge · at-risk ARR within the next two quarters' ATR · current-quarter renewal call. Each with prior period, variance to plan, and direction. |
| **The sentence beneath** | The five-sentence spine: the number, the movement, the driver, the response, the ask. |
| **Director's question** | "Is this the number you gave us last quarter?" |
| **Failure mode** | Leading with a chart. A board reads the top and stops; if the call is not in the first five lines it will be inferred from your delivery. |

**Materiality threshold.** Declare one — commonly the greater of 1% of ARR or $250k — and
pre-brief the CEO and CFO on any movement above it at least 48 hours before the meeting.
Publish the threshold in the appendix so "material" is not renegotiated each quarter.

---

## 3. Slide 2 — ARR bridge

| Field | Spec |
| --- | --- |
| **Purpose** | Show which line of the bridge broke. This is the first thing an exec wants. |
| **Chart** | Waterfall for the current quarter; table for the trailing 8 quarters. |
| **Identity** | `Ending ARR = Beginning + New + Expansion + Reactivation − Contraction − Churn` |
| **Columns** | Quarter · Beginning · New · Expansion · Reactivation · Contraction · Churn · Ending · Quick ratio |
| **Tie-out line (mandatory)** | "Ties to finance ARR of $X as of <date>. Variance $0." |
| **Director's question** | "Is expansion real, or is it contracted ramp?" |
| **Failure mode** | A bridge that does not tie. The instant a CFO finds a variance, every number in the pack is discarded — including the correct ones. |

**Line definitions to freeze and publish** (from the operating decomposition an ARR waterfall
uses; terminology note: "ARR waterfall" is the operator term, "ARR bridge" the PE-diligence
term, "ARR rollforward" the accounting term [V]):

| Line | Rule | Boundary decision you must state |
| --- | --- | --- |
| New | Account had $0 at t0 and has never been a paying customer, or churned longer ago than the win-back window | Does a new subsidiary of an existing parent count as New or Expansion? Decide by `parent_account_id` and be consistent |
| Expansion | Same `account_id`, ARR_t1 > ARR_t0 | Split into seats / tier / cross-sell / price uplift / usage. **Flag contracted ramp separately — it is not a CS win** |
| Reactivation | Previously churned account returning after the win-back window (commonly 30–90 days) | Excluded from cohort NRR/GRR; bridge and growth only |
| Contraction | Same account, 0 < ARR_t1 < ARR_t0 | A downsell to $0 is Churn, not Contraction |
| Churn | ARR_t1 = 0 for an account with ARR_t0 > 0 | Churn date = contract end date. Track `decision_date` separately — the gap is your early-warning window |

**Quick ratio** = `(New + Expansion) / (Churn + Contraction)`. The canonical 4.0 target comes
from Mamoon Hamid at SaaStr, 2015 — a widely-adopted convention, not a measured median [P].
State whether reactivation is in your numerator; the strict form excludes it.

---

## 4. Slide 3 — NRR / GRR trend with a benchmark band

| Field | Spec |
| --- | --- |
| **Purpose** | Show whether the trend is inflecting, over at least 8 periods. |
| **Chart** | Two TTM lines (GRR, NRR) on one axis, with a shaded peer band and its citation printed on the slide. |
| **Method note on the slide** | Cohort or formula method; win-back window; whether usage overage is in the ARR base. |
| **Director's question** | "How does that compare to peers, and to whose peers?" |
| **Failure mode** | NRR shown without GRR. Expansion from twenty accounts masks churn in two hundred. |

**Benchmark band options — pick the closest population and print it, do not average them:**

| Value | Population | Source · year | Label |
| --- | --- | --- | --- |
| NRR median 101%; GRR median 88% | Private B2B SaaS, N=228 / N=225, CY2024 actuals | Benchmarkit, *2025 B2B SaaS Performance Metrics Benchmarks* | [M] |
| NRR median 102% (P75 110%, P25 92%); GRR median 84% (P75 91%, P25 76%) | SaaS + AI-native, N≈226–230, CY2025 | 2026 Aleph × Benchmarkit | [M], secondary reporting |
| NRR median 102% (P75 111%, P25 97%) at $25–50k ACV | Private B2B SaaS, $1M+ ARR | SaaS Capital, 2025 retention benchmarks | [M] |
| NRR median 82% (P75 97%) | ~2,700 B2B SaaS, $250k ARR floor — self-serve skew | ChartMogul, *The SaaS Retention Report*, Sept 2025 | [M], **not comparable to Benchmarkit's population** |
| GRR 92% under usage-based pricing vs 88% subscription/hybrid; NRR 110% for hybrid sub+usage | Private B2B SaaS, CY2024 | Benchmarkit 2025 | [M] |

Both the ChartMogul 82% and the Benchmarkit 101% are correct — for different populations.
Naming the population is the whole discipline. **Retention is compressing across every
population measured** (NRR ~105% in CY2021 → 101% CY2024; GRR 90% → 88%) [M]; a flat
retention line against a declining peer band is a gain, and saying so is legitimate.

**Public-company NDR is not a peer band.** Definitions diverge structurally: Snowflake keeps
churned customers in the cohort at $0 on a trailing-two-year basis; Figma's S-1 measures
backward from the measurement date and therefore excludes departed accounts entirely
(disclosed NRR 132%); Klaviyo excludes usage overage; Fastly publishes both single-month and
LTM [M, from filings]. Never draw a public NDR onto your band.

---

## 5. Slide 4 — Retention by segment and ACV band

| Field | Spec |
| --- | --- |
| **Purpose** | Locate the movement. Blended retention cannot be acted on by anyone. |
| **Chart** | Table plus small-multiple TTM trend lines, one per segment. |
| **Primary cut** | **ACV band.** It is the single most predictive segmentation variable for retention [M — SaaS Capital 2025; Benchmarkit 2025 states GRR benchmarks are best analysed by ACV]. Employee count and industry are secondary. |
| **Columns** | Segment · Beg ARR · New · Expansion · Contraction · Churn · End ARR · Cohort GRR · Cohort NRR · share of the variance |
| **Mandatory line beneath** | The mix/performance/interaction decomposition in basis points. |
| **Director's question** | "Is the NRR move mix or performance?" |
| **Failure mode** | Presenting a 97.8% blend that hides Enterprise 104.2% and SMB 80.8%. |

**The decomposition** (`scripts/retention_math.py --mix`):

```
ΔNRR = Σ (wᵢ,₁ − wᵢ,₀) × NRRᵢ,₀        MIX          base changed shape
     + Σ  wᵢ,₀ × (NRRᵢ,₁ − NRRᵢ,₀)     PERFORMANCE  customers behaved differently
     + Σ (wᵢ,₁ − wᵢ,₀)(NRRᵢ,₁ − NRRᵢ,₀) INTERACTION  report it; never fold it into mix
```

Mix is a go-to-market outcome. Performance is yours. Report the interaction term explicitly —
folding it into mix is the most common way a CS leader accidentally takes credit or blame.

**The dollar-vs-logo diagnostic belongs here too.** Compare `1 − GRR` to logo churn:

| Relationship | Read |
| --- | --- |
| Dollar churn > logo churn | You are losing your **larger** customers |
| Logo churn > dollar churn | You are losing your **smaller** customers |
| Quantify it | `avg ARR of churned account / avg ARR of all accounts` — an index above 1.0 means churn is adversely selected toward your better customers |

Run this **inside each segment**, not on the blend. A blended index of 0.83 can sit on top of
an SMB index of 1.67 — losing the best small customers while the blend says the opposite.

---

## 6. Slide 5 — Cohort retention

| Field | Spec |
| --- | --- |
| **Purpose** | The only slide that proves whether the business is structurally improving or just larger. |
| **Chart** | Triangle heat map. Rows = acquisition cohort (monthly or quarterly), columns = tenure (M0…M24/M36). Publish a **dollar** triangle and a **logo** triangle. |
| **Cohorts shown** | 8–12, most recent last. |
| **Director's question** | "Are the newest cohorts better than the old ones at the same age?" |
| **Failure mode** | Averaging cohorts of different ages together, or comparing a 4-month-old cohort's M12 cell to anything. |

| Construction rule | Consequence if broken |
| --- | --- |
| Membership frozen at t0; churned members stay at $0 | Dropping them is the most flattering error in retention reporting and it inflates every cell |
| Customers acquired after t0 never enter the cohort | Leaking new logos turns NRR into the growth rate |
| Reactivation excluded | A win-back is new revenue |
| Immature cells greyed out | A cohort cannot have an M12 value at month 4 |
| Cells with n < 20 accounts or < $2M ARR suppressed or asterisked | Small-n swings get quoted back at you for years |
| Both dollar and logo published | Dollar can exceed 100%; logo cannot. The gap between them **is** the expansion story |

**How to read it aloud, in one sentence:** read *down a tenure column*, not across a row.
"M6 dollar retention across the last four quarterly cohorts is 88% → 91% → 93% → 94%; the
onboarding change lands in cohorts, not in the pipeline."

**Hazard, not just survival.** The shape of period-over-period loss is the diagnosis: a spike
at month 12 is renewal-event churn; a monotonic early decline is onboarding failure. These
need opposite investments. Kaplan–Meier handles right-censored (still-active) accounts
without discarding them; discarding them biases recent cohorts downward. Cox proportional
hazards gives interpretable hazard ratios per covariate (ACV band, channel, TTV miss,
sponsor present) — run the proportional-hazards diagnostics before quoting one [A — *Journal
of Marketing Analytics*, 2025, methodological].

**Cohort-quality drift** is the early-warning version of this slide: compare M3/M6 retention
of the latest six cohorts to the trailing-12 average. It detects ICP drift from a new channel
roughly three quarters before it reaches NRR.

---

## 7. Slide 6 — Concentration and dependency

| Field | Spec |
| --- | --- |
| **Purpose** | Retention rates are averages; the board is exposed to the tail. |
| **Chart** | Pareto — cumulative % of ARR against rank-ordered accounts — plus the top-10 table. |
| **Director's question** | "What is our NRR excluding the top three accounts?" |
| **Failure mode** | Reporting mean ACV. One whale destroys a mean; report P25 / median / P75 / top-decile share. |

| Measure | Formula | Reference |
| --- | --- | --- |
| Top 1 / 5 / 10 / 20 share | `Σ ARR of top N / total ARR` | Print all four — the shape matters more than any one |
| Herfindahl index | `Σ (ARRᵢ / total ARR)²` | One number for the whole distribution's skew |
| Single-customer materiality | any account ≥10% of revenue | US GAAP requires disclosure of revenues from a single external customer at ≥10% of an entity's revenues (ASC 280-10-50-42) |
| Common investor red flags | single customer >10%; top 5 >25% | Widely repeated diligence heuristics [P] — not measured medians |
| Departure impact | GRR and NRR recomputed with account X removed | "If <Account> leaves at renewal, TTM GRR falls 88.4% → 84.1%" |
| Retention ex-top-N | NRR/GRR recomputed excluding the top 3 accounts | Have it ready; you will be asked for it live |

**Dependency is not only dollars.** Add a column for each top-10 account: exec sponsor named
and last contacted; number of live contacts (one is a single point of failure); reference
dependency; roadmap dependency (features built for them). A top-10 account carried by one
champion is a concentration risk no ARR table shows.

**Schedule the top-10 renewal calendar by opt-out deadline** (`renewal_date −
notice_period_days`), not renewal date. A 15 January renewal on 90 days' notice is an October
decision; a board reading renewal-date quarters is reading exposure that has already resolved.

---

## 8. Slide 7 — Exposure: ATR and at-risk coverage

| Field | Spec |
| --- | --- |
| **Purpose** | Answer "what is the exposure in the next two quarters" in one look. |
| **Chart** | Stacked bar: ATR by **decision quarter**, stacked by risk band. Second stack: at-risk ARR by reason code. |
| **Definitions** | ATR = ARR (or logos) with a contractual renewal date inside the period. At-risk = a **declared, dated, reason-coded** state with written entry and exit criteria — not a health-score band. |
| **Three views of at-risk, always** | (1) total, (2) within the next two quarters' ATR, (3) net of the mitigation plan's expected save |
| **Director's question** | "Of that at-risk number, how much have you actually saved historically?" |
| **Failure mode** | A count of at-risk accounts. A count is not a disclosure; a reason-coded dollar stack is. |

| Reason code | What it implies about savability |
| --- | --- |
| Value not realised | Addressable — the CS org owns it |
| Product gap | Addressable only if the roadmap commitment is real and dated |
| Champion loss | Addressable, and the fastest-decaying opportunity on the list |
| Support / reliability | Addressable, but the fix is not in CS |
| Budget / down-round | Partially addressable — change the conversation to value per dollar |
| Competitive displacement | Addressable early, rarely late |
| M&A / consolidation / shutdown | **Uncontrollable.** Tag it, show it as a memo line, and defend the classification |

Publish the **controllable vs uncontrollable split** and be conservative about what you claim
is uncontrollable — a board that suspects you are laundering churn into the "M&A" bucket will
discount your entire risk disclosure.

---

## 9. Slide 8 — Forecast credibility

| Field | Spec |
| --- | --- |
| **Purpose** | Establish that the number on slide 1 is worth believing. |
| **Chart** | Table by vintage (T-90, T-60, T-30) for the last four quarters. |
| **Non-negotiable** | Grade against a **frozen snapshot** written once at period start and never edited. Grading a forecast edited all quarter measures field hygiene, not forecasting [V]. |
| **Director's question** | "You called $19.8M last quarter and closed $18.9M. Is that a pattern?" |
| **Failure mode** | Publishing accuracy without signed bias. Offsetting errors make a bad book look accurate. |

| Metric | Formula | Read |
| --- | --- | --- |
| Forecast accuracy | `1 − abs(Called − Closed) / Called` | Headline only |
| WAPE | `Σ abs(Fᵢ − Aᵢ) / Σ Aᵢ` | Account-level dispersion; immune to offsetting errors |
| Bias (signed) | `Σ (Fᵢ − Aᵢ) / Σ Aᵢ` | Sustained optimism is a coaching problem, not a model problem |
| Commit hit rate | `Closed from Commit / Commit at snapshot` | Whether "Commit" means anything |
| Sandbag rate | `Closed from Omitted or At-Risk / total closed` | Hidden upside |
| Risk detection rate | `ARR flagged at-risk ≥60d before loss / total ARR lost` | Below ~60%, most churn is a surprise and the forecast is fiction [P] |
| Save rate | `At-risk ARR retained / at-risk ARR reaching renewal` | Meaningless without entry criteria; always paired with detection rate |

Published targets of ~90% for heavy manual forecasting and 95% held from day 1 to day 90 are
**vendor claims** [V]. There is no methodologically clean public benchmark for renewal
forecast accuracy. Say that on the slide rather than importing a vendor target as a peer bar.
The most informative number on this slide is how much the **T-90 call moved** — that measures
early-warning quality, which is the thing a board is actually buying.

---

## 10. Slide 9 — CS efficiency

| Field | Spec |
| --- | --- |
| **Purpose** | Show what the function costs and what it returns, before you ask for more. |
| **Chart** | Table plus the ARR coverage waterfall. |
| **Director's question** | "What is the payback on the last CS hire?" |
| **Failure mode** | Presenting activity — QBRs held, touches logged. Pair every activity metric with the outcome it produced (EBR → risk identified / expansion identified). |

| Metric | Formula | Reference point |
| --- | --- | --- |
| ARR per CSM | `ARR under management / quota-carrying CSM FTEs` (state whether managers, ops and onboarding are excluded) | **No current Grade-A public benchmark exists** — every range in circulation is a CS-platform content aggregation [P]. Use it as an internal capacity constant, and say so on the slide |
| Accounts per CSM | `# accounts / CSM FTEs`, by segment | No citable public benchmark. Derive it from hours per account by tier and print the assumption [P] |
| Touch coverage | `accounts with a logged meaningful touch in 90d / assigned accounts` | Below ~70% in a named-coverage tier, the book is oversized regardless of its ARR [P] |
| Cost of retention | `Fully loaded CS + Support opex / ARR` | Median **9% of ARR**, 1,000+ private B2B SaaS, SaaS Capital 2026 Spending Benchmarks; 10% at $3–5M ARR; equity-backed companies spend ~2× bootstrapped [M] |
| Cost per retained dollar | `CS + Support opex / (Beginning ARR × GRR)` | Internal; directly comparable to gross margin |
| Expansion CAC ratio | `(S&M + CS expense allocated to expansion) / Expansion ARR` | Median **$1.00** CY2024 (N=21) against **$2.00** new-logo CAC ratio (N=73), Benchmarkit 2025 [M]. Fewer than 20% of companies compute it [M] |
| Expansion share of new ARR | `Expansion / (New + Expansion)` | Median 40% CY2024 (N=81); 58% at $50–100M ARR; 67% above $100M (n=6 — fragile, say so) [M] |
| ARR coverage waterfall | % of ARR under named / pooled / digital / **uncovered** | "Uncovered ARR" is the board-relevant number, and the one most decks omit |

Computing the expansion CAC ratio is frequently the strongest single argument a CS org has for
budget: it is the number that shows expansion dollars cost roughly half what new-logo dollars
cost. Most companies cannot produce it, which is precisely why producing it lands.

---

## 11. Slide 10 — The one strategic issue and the ask

| Field | Spec |
| --- | --- |
| **Purpose** | Convert the analysis into a decision. |
| **Format** | One paragraph naming **one** issue, one action table, one ask line. |
| **Action table columns** | # · Action · Owner · By · Cost · Expected effect (in bps or $) · Success measure · Date we will know |
| **The ask line** | decision · dollar amount · decision needed by · what happens if the answer is no |
| **Director's question** | "What would you do if we said no?" |
| **Failure mode** | Three issues. A board can hold one. Three issues means none is chosen and you own all three anyway. |

Choose the issue by expected ARR effect, not by how much it annoys you. State the expected
effect as a band, never a point estimate, and name the date the leading indicator will be
reported. Then report it next quarter whether or not it worked — a leader who reports their
own failed intervention unprompted gets the next ask approved.

---

## 12. The pre-read

| Rule | Detail |
| --- | --- |
| **Length** | One page. If it is two, the second page is appendix. |
| **Timing** | 3–5 days before the meeting; a night-before send will not be read [P] |
| **Contents** | The five-sentence spine, the six-tile headline block, the ask |
| **What it is not** | A summary of the deck. It is the argument; the deck is the evidence |
| **Test** | If a director read only the pre-read, could they vote on your ask? If no, rewrite it |

Template: `../assets/board-pre-read.md`.

---

## 13. Appendix discipline

The appendix exists so a director can drill without the narrative being cluttered. Anything
you would be embarrassed to be asked for should already be in it.

| Section | Contents |
| --- | --- |
| **A1 Definitions and formulas** | Every metric on every slide: formula, window, denominator, exclusions, currency policy |
| **A2 Change log** | Dated. Every definition change, the reason, and the restated prior periods. Silent restatement destroys every trend line you have ever published |
| **A3 Reconciliation to finance** | The bridge tie-out, line by line, with the variance (which must be $0) |
| **A4 Churn post-mortem** | Every loss above the materiality threshold: account, ARR, tenure, segment, reason code, health at −90d, whether it was flagged, owner, what was learned |
| **A5 Method notes** | Cohort construction, win-back window, small-n suppression rule, FX policy, contracted-ramp treatment, test/internal account exclusion rule |
| **A6 Segment and ACV band definitions** | In dollars. Any re-segmentation during the period flagged and shown both ways |

Template: `../assets/definitions-changelog.md`.

---

## 14. What must never appear

| Never | Why | Instead |
| --- | --- | --- |
| An unexplained definitional change | Every trend line you have published becomes unreadable, retroactively | Change log entry, restated history, as-reported **and** pro-forma on the slide |
| A restated figure with no note | A director remembers last quarter's number better than you expect | "Restated from X to Y; reason: Z" on the same line as the number |
| A health score with no validated predictive lift | If Red-tier churn is not roughly ≥3× Green-tier, the score is decoration [P] | Publish the lift, or remove the score from the board pack |
| A metric that appears once and never again | It cannot be judged, so it will be discounted — and so will its neighbours | Fix the set for a year; new metrics arrive with 8 prior periods |
| Blended-only retention | Hides a 20-point spread between segments | ACV-band cut adjacent, always |
| A rate without its denominator | "Churn improved" on a shrinking base | Numerator and denominator printed |
| Single-month NRR or GRR | Renewal-timing noise presented as behaviour | TTM or cohort |
| Activity metrics as outcomes | QBRs held, emails sent, touches logged | Pair each with the outcome it produced |
| Account names in a risk list the CEO has not seen | You blindside your own CEO in front of the board | Pre-brief, then show top-10 renewal status only |
| A benchmark with no source, year or population | The director substitutes a worse one from memory | Full citation on the slide |
| Internal risk language that could be forwarded to a customer | Leaked risk language has ended renewals | Mark the pack internal; keep customer-facing text in a separate artifact |
| ARR presented that is actually CARR | Inflates growth and distorts every retention denominator | Label CARR as CARR |

---

## 15. Chart selection

| Job | Correct chart | Anti-pattern |
| --- | --- | --- |
| How ARR changed | Waterfall | Stacked bar of ending ARR by segment — that is stock, not flow |
| Retention trend | TTM line with segment small multiples | One blended line |
| Cohort behaviour | Triangle heat map | Averaging cohorts of different ages |
| Churn timing | Hazard bar chart by tenure bucket | Cumulative survival only |
| Health movement | Migration matrix, heat-shaded | Pie chart of current health distribution |
| Renewal exposure | ATR by decision quarter, stacked by risk band | A single "renewals this year" number |
| Risk composition | Stacked bar of at-risk ARR by reason code | A count of at-risk accounts |
| Concentration | Pareto: cumulative % ARR vs ranked accounts | Mean ACV; a gauge or a dial for efficiency |

---

## 16. Sources

- Benchmarkit, *2025 B2B SaaS Performance Metrics Benchmarks* (CY2024 actuals; per-metric N inline) — https://www.benchmarkit.ai/2025benchmarks — [M]
- 2026 Aleph × Benchmarkit SaaS & AI Performance Benchmarks (CY2025) — https://www.getaleph.com/answers/gross-revenue-retention-saas-2026 — [M], secondary
- SaaS Capital, *What is a Good Retention Rate for a Private SaaS Company in 2025?* — https://www.saas-capital.com/blog-posts/what-is-a-good-retention-rate-for-a-private-saas-company/ — [M]
- SaaS Capital, *2026 Spending Benchmarks for Private B2B SaaS Companies* (survey Mar 2026, 1,000+ companies) — https://www.saas-capital.com/blog-posts/spending-benchmarks-for-private-b2b-saas-companies/ — [M]
- ChartMogul, *The SaaS Retention Report: The AI Churn Wave*, Sept 2025 — https://chartmogul.com/reports/saas-retention-the-ai-churn-wave/ — [M]
- SaaS Metrics Standard Board — NRR / GRR / logo retention standards — https://www.saasmetricsboard.com/net-revenue-retention — [M]
- FASB ASC 280-10-50-42 — major-customer disclosure at ≥10% of revenues — regulatory
- Wall Street Prep, *Customer Concentration* — https://www.wallstreetprep.com/knowledge/customer-concentration/ — [P] thresholds
- Eru, *Board-Ready SaaS Revenue Metrics: NRR, GRR, Cohort Analysis & Due Diligence Prep* — https://www.joineru.com/blog/board-reporting-guide.html — [V]
- *Predictability & explainability of survival analysis in churn prediction*, Journal of Marketing Analytics, 2025 — https://link.springer.com/article/10.1057/s41270-025-00450-2 — [A]
