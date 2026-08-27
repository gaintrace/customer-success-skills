# Report Structure

> The fourteen sections, in the order they are published, with what each must contain, the
> right chart for each job, and the four audience variants. Section 7 — the health migration
> matrix — is written out in full, because it is the section most often skipped and the one
> that carries the most information per square inch.
>
> Evidence labels: **[M]** measured with a disclosed population · **[V]** vendor claim ·
> **[P]** practitioner convention · **[A]** academic.

**Contents**
- [Why the order is fixed](#why-the-order-is-fixed)
- [1. The fourteen sections](#1-the-fourteen-sections)
- [2. Section-by-section spec](#2-section-by-section-spec)
- [3. The right chart for each job](#3-the-right-chart-for-each-job)
- [4. Audience variants](#4-audience-variants)
- [5. Period comparison rules](#5-period-comparison-rules)
- [6. Segmentation cuts that must always appear](#6-segmentation-cuts-that-must-always-appear)
- [7. The health migration matrix, in full](#7-the-health-migration-matrix-in-full)
- [8. Churn reason taxonomy](#8-churn-reason-taxonomy)
- [9. What to leave out](#9-what-to-leave-out)

---

## Why the order is fixed

An operating report is read the same way every month by the same people. When the order moves,
the reader hunts, and a reader who hunts stops reading — which is how a report dies without
anyone deciding to kill it. The order below is built around what an exec reads first: *did we
hit the number, which line of the bridge broke, is the trend inflecting, what is the exposure,
is the forecast credible, what do you need from me.* Everything else is support.

Three rules govern the whole document:

| Rule | Consequence of breaking it |
| --- | --- |
| Sections are cut, never reordered | The reader loses the map and starts skimming |
| A section with no movement prints "no movement" | Deletion reads as *checked and clear*, which is a different claim |
| Anything deliberately omitted gets a **written skip** — reason and revisit date (R14) | An undeclared omission is how a section disappears for a quarter |

---

## 1. The fourteen sections

| # | Section | The question it answers | Cadence |
| --- | --- | --- | --- |
| 0 | Headline (≤6 metrics) | Did we hit the number | Every edition |
| 1 | The Call (3–5 sentences) | What happened and what are we doing | Every edition |
| 2 | ARR bridge | Which line moved | Every edition, MoM + QTD + TTM |
| 3 | GRR · NRR · logo retention | Is the trend inflecting | TTM only |
| 4 | Cohort view | Is the business structurally improving | Monthly, quarterly cohorts |
| 5 | Churn by reason, with ARR | Why we lost what we lost | Every edition |
| 6 | Contraction | Is value density falling | Every edition |
| 7 | Expansion | Where growth inside the base came from | Every edition |
| 8 | Health distribution | What the book looks like now | Every edition |
| 9 | **Health migration matrix** | What the team changed | Monthly (MoM) + rolling 90-day |
| 10 | At-risk ARR and coverage | What is exposed, and who is on it | Every edition |
| 11 | Renewals closed vs forecast | Is the forecast credible | Quarterly, QTD in between |
| 12 | Onboarding and TTV | What next year's GRR will be | Monthly, six cohorts |
| 13 | Operating notes | What changed about the report itself | Every edition |
| 14 | Decisions requested | What do you need from the room | Every edition |

---

## 2. Section-by-section spec

### 0 · Headline

Six metrics, no more. Each carries **this period · prior period · variance to plan · six-period
trend**. A metric without a plan number is a fact, not a scoreboard; if a metric has no plan,
say so rather than dropping the column.

The six: TTM NRR · TTM GRR · TTM logo retention · net new ARR from the bridge · at-risk ARR
inside the next two quarters' ATR · current-quarter renewal call vs plan.

### 1 · The Call

Written **before any chart exists**. Five things in 3–5 sentences: what happened, the driver
with its arithmetic, what is being done about it, what changes in the forecast, and the one
decision requested. If it cannot be written before the charts, the charts are being used to
discover the story rather than to evidence it — and the story will end up being whatever the
charts happened to make easy.

### 2 · ARR bridge

| Line | Boundary rule to freeze and publish |
| --- | --- |
| Beginning ARR | Must equal the prior period's ending exactly. A mismatch is a restatement — label it |
| New | Account had $0 at t0 and has never been a paying customer, or churned longer ago than the win-back window. Decide subsidiaries by `account.parent_account_id` and be consistent |
| Expansion | Same `account_id`, ARR up. Split into seats · tier · cross-sell · price uplift · usage commit. Pre-signed ramp uplift is expansion but flagged separately — it is not a CS win |
| Reactivation | Returned after the win-back window (30–90 days is the common convention). **In the bridge, never in GRR/NRR** |
| Contraction | Same account, ARR down but above $0. Down to $0 is Churn |
| Churn | ARR to $0. Dated on the **decision**, not the contract end (R24). M&A-driven churn is tagged and shown as a memo line — real lost ARR, not a CS performance failure |

Derived and published alongside: net new ARR · each line as a share of beginning ARR · SaaS
Quick Ratio `(New + Expansion) / (Churn + Contraction)` · the leaky-bucket ratio, its inverse.
The Quick Ratio target of 4.0 is a 2015 practitioner convention (Mamoon Hamid, SaaStr) `[P]`,
not a measured median; a mature large-base company running 1.5–2.5 is not failing by that fact.

**The tie-out line is part of the section, not a footnote:**
`Computed ending $X vs finance ARR $Y as at <date> → variance $Z.`

### 3 · GRR · NRR · logo retention

Cohort method, TTM, GRR and NRR adjacent on the same denominator. Publish by ACV band before
publishing blended. Include the dollar-vs-logo adverse-selection index (§6). State the
cohort-vs-formula gap in basis points once, in the appendix.

### 4 · Cohort view

A dollar retention triangle and a logo retention triangle: rows = acquisition quarter, columns =
tenure. Dollar tables can exceed 100%; logo tables cannot, and one that does is a bug. Grey out
immature cells. The reading that matters is **down a column** — the same tenure point across
successive cohorts — because that is cohort-quality drift, and it moves nine months before NRR.

### 5 · Churn by reason

Reason mix table with ARR attributed, then one row per named loss above the materiality
threshold. Columns: account · ARR · segment · tenure · reason chain · controllable · health band
at −90 days · flagged at-risk and how many days before · owner · the lesson. Taxonomy in §8.

### 6 · Contraction

Its own reason mix. Contraction rising while churn is flat is a pricing and value-density
problem with a different owner and a different play. On per-seat models, contraction is the
leading edge of churn rather than a separate event — report the two adjacent.

### 7 · Expansion

Decomposed by source: seats · tier upgrade · cross-sell · price uplift · usage-commit increase.
A single "expansion" number is not actionable, because those five have five different owners.
Report expansion ARR as a share of gross new ARR — median **40%** in CY2024 (Benchmarkit 2025,
N=81) `[M]`, rising to 58% at $50–100M ARR `[M]`.

### 8 · Health distribution

By count **and** ARR-weighted, with the prior period's ARR share beside it. The ARR-weighted
view is the one that matters: forty Secure accounts at $8k each do not offset one Critical at
$400k.

### 9 · Health migration matrix

See §7 below.

### 10 · At-risk ARR and coverage

At-risk is a **declared, dated, reason-coded state** with written entry and exit criteria — not
a health band. Three views: total · inside the next two quarters' ATR · net of the mitigation
plan's expected save. Bucket by opt-out deadline (R1). Report movement in and out of the
at-risk state this period; a static at-risk number with no flow is a list, not a pipeline.

The coverage waterfall — named 1:1 / pooled / digital-only / **uncovered** — is published as ARR
and as a share of base. Uncovered ARR is the number a board asks about. Median CS + support
spend is **9% of ARR** (SaaS Capital 2026 spending benchmarks, 1,000+ private B2B SaaS) `[M]`,
which is the frame for any coverage argument.

### 11 · Renewals closed vs forecast

ATR by quarter for the next four quarters; current-quarter called vs closed vs plan; forecast
accuracy and **signed bias** for the trailing four quarters, graded by vintage (T-90 / T-60 /
T-30) against a frozen snapshot. Top ten renewals by ARR with status. No published,
methodologically clean industry benchmark for renewal forecast accuracy exists — targets in the
90–95% range circulate as vendor claims `[V]` — so grade against your own trailing four quarters.

### 12 · Onboarding and TTV

Six monthly cohorts: accounts · ARR · median and P90 TTV · on-time go-live % · 30-day activation
rate · stalled-onboarding ARR. Median and P90 always; a mean TTV is destroyed by one 300-day
implementation. Measure TTV to a customer-defined success milestone, not a vendor task list
(Lincoln Murphy) `[P]`.

### 13 · Operating notes

Definition changes with restated history · restatements as labelled lines · data faults found ·
population changes with the rule applied · changes to the report itself. Short in a good month,
and the section that keeps the report trustworthy across years.

### 14 · Decisions requested

| Column | Why |
| --- | --- |
| Decision | Phrased as a question the room can answer yes or no to |
| Owner | The person who executes, not the person who approves |
| Options | Two or three, with the trade-off named |
| Recommendation | Yours. A report that presents options without a recommendation has handed the work back |
| $ at stake | The number that determines whether this is worth the room's time |
| Decide by | A date, chosen against an opt-out deadline or a hiring lead time |
| If deferred | The concrete consequence. "We will revisit next month" is not one |

---

## 3. The right chart for each job

| Job | Chart | Anti-pattern |
| --- | --- | --- |
| How ARR changed | Waterfall | Stacked bar of ending ARR by segment — that shows stock, not flow |
| Retention trend | Line, TTM, with segment small multiples | One blended line |
| Cohort behaviour | Triangle heat map | Averaging cohorts of different ages together |
| Churn timing | Hazard bar chart by tenure bucket | Cumulative survival only — it hides where the loss happens |
| Health movement | **Migration matrix, heat-shaded** | Pie chart of the current distribution |
| Renewal exposure | ATR by quarter, stacked by health band | A single "renewals this year" number |
| Risk composition | Stacked bar of at-risk ARR by reason code | A count of at-risk accounts |
| Concentration | Pareto: cumulative % ARR vs ranked accounts | Mean ACV |
| Onboarding | Cohort table with median and P90 columns | A single average TTV |

---

## 4. Audience variants

| | CSM team | VP / ops review | Exec staff | Board appendix |
| --- | --- | --- | --- | --- |
| **Sections** | 0–2, 5, 6, 9 (by owner), 10, 11 | All fourteen | 0–3, 10, 11, 14 | 2 (8 quarters), 3 by ACV band, 4, 10, definitions |
| **Length** | 3–4 pages | 8–12 pages | 2 pages + appendix | 4–6 exhibits |
| **Basis** | Month + TTM | Month + QTD + TTM | TTM | TTM, constant currency |
| **Added** | Per-owner cuts; per-owner migration matrix | — | The single strategic issue | Peer benchmark band with citation |
| **Cut** | Unit economics, capacity, cohort triangle | — | Everything below §11 moves to appendix | Anything monthly; anything not restated |
| **The trap** | Turning the migration matrix into a performance review — publish it as a book-quality signal, not a scorecard | Growing past 12 pages and losing the front page | Presenting exposure with no ask | Introducing a metric without its prior 8 periods |

The per-owner migration matrix in the CSM-team variant is the highest-value and highest-risk cut
in the whole report. It is genuinely diagnostic — a CSM whose Secure accounts churn at three
times the team rate is miscalibrated, not unlucky — and it becomes useless the moment people
believe it is being used to rank them, because they will manage the bands instead of the
accounts. Publish it with the entry criteria attached and the calibration framing explicit.

---

## 5. Period comparison rules

| Comparison | Valid for | Misleads when |
| --- | --- | --- |
| MoM | ARR bridge, at-risk movement, expansion pipeline, ticket load | Applied to any retention rate — a monthly GRR is renewal-timing noise |
| QoQ | Renewal metrics with roughly flat ATR | >30% of ATR lands in one quarter. Print ATR dollars beside every rate |
| YoY | Renewal metrics under seasonality; anything spanning a re-segmentation | The inflection happened three months ago and YoY will not show it for nine |
| TTM | GRR, NRR, logo retention, save rate, detection rate, forecast accuracy | You need to show an inflection early — pair with a 3-month annualised view, labelled |
| QTD / MTD | Progress to plan | Compared against a prior *full* period |

Annualise a monthly retention rate geometrically — `GRR_annual = GRR_monthly ^ 12` — never
`1 − 12 × monthly_churn`, which overstates loss at any material churn rate.

**Guards.** Cohort maturity: grey out cells a cohort does not have. Small-n: asterisk any cell
under 20 accounts or 2% of base — report it, never benchmark it. Comparability: flag any period
containing an acquisition, a re-segmentation, a pricing-model change or a definition change, and
show as-reported *and* pro-forma where material.

---

## 6. Segmentation cuts that must always appear

| Cut | Buckets | What it detects |
| --- | --- | --- |
| **ACV band** | <$5k · $5–25k · $25–50k · $50–100k · $100–250k · >$250k | The most predictive retention cut and the one benchmarks are built on (SaaS Capital 2025; Benchmarkit 2025) `[M]` |
| **Segment** | Per `cs-context` §3 dollar boundaries | How the org is staffed and comped |
| **Tenure** | 0–90d · 91–365d · Y2 · Y3 · Y4+ | Front-loaded churn = onboarding/ICP failure. Back-loaded = value decay. Opposite investments |
| **Product / SKU** | Per SKU, plus multi-product attach rate | Multi-product NRR averages unlike things |
| **Coverage model** | Named · pooled · digital · uncovered | Converts a staffing argument into a measured one |
| **Acquisition channel** | `original_lead_source` | A sales-quality problem wearing a CS costume |
| **Region / currency** | Constant currency, or state you did not | FX moving a rate you attributed to behaviour |
| **Contract term** | Monthly · annual · multi-year | Multi-year contracts suppress this year's ATR and defer the risk into one quarter |

**The dollar-vs-logo diagnostic**, run on every cut:
`adverse-selection index = avg ARR of churned account ÷ avg ARR of base`.
Above 1.0, the accounts lost were larger than average. The blended index routinely reads near
1.0 while one segment sits at 2.3 and another at 0.8 — which is why it is computed per cut.

---

## 7. The health migration matrix, in full

### Construction

Rows are the band at t0. Columns are the band at t1, plus a **Churned** column. Cells carry both
account count and ARR. The t0 population is **frozen** at the t0 date; accounts that entered the
base after t0 appear as a memo line under the matrix and are excluded from every rate.

```
                  →  band at t1
band at t0    Secure  Watch  At Risk  High  Critical  Churned │ Total t0
Secure           ·      ·       ·      ·       ·         ·    │    ·
Watch            ·      ·       ·      ·       ·         ·    │    ·
At Risk          ·      ·       ·      ·       ·         ·    │    ·
High Risk        ·      ·       ·      ·       ·         ·    │    ·
Critical         ·      ·       ·      ·       ·         ·    │    ·
──────────────────────────────────────────────────────────────┼───────
Total t1         ·      ·       ·      ·       ·         ·    │    ·
Memo: entered after t0 — n accounts, $X ARR (not in the rates below)
```

Publish it **month over month** on the operating cadence, and on a **rolling 90-day** window
beside it. One month of movement on an enterprise book is often too small to read; the 90-day
window is where the pattern is legible.

### The rates

| Rate | Formula | Read it as |
| --- | --- | --- |
| Stability | Σ diagonal ÷ total t0 | How much of the book stood still. Very high stability on a book with poor retention means the score is not moving, not that the book is stable |
| Improvement | Σ cells above the diagonal ÷ (total t0 − Secure row) | Whether intervention moved anything. Secure accounts are excluded from the denominator because they cannot improve |
| Degradation | Σ cells below the diagonal, excluding Churned ÷ (total t0 − Critical row) | Whether the book is decaying under you |
| Rescue rate | (At Risk + High + Critical at t0 ending Secure or Watch) ÷ that t0 population | The save motion, measured on a frozen population instead of a self-selected list. The honest version of "save rate" |
| Slide rate | (Secure + Watch at t0 ending At Risk or worse, including Churned) ÷ that t0 population | Where next quarter's risk pipeline is coming from |
| **False-green rate** | (Secure + Watch at t0 that **Churned**) ÷ that t0 population | The credibility number. Publish it as a rate, as a count, and as a share of all ARR churned in the window |
| Predictive lift | churn rate of (High + Critical) ÷ churn rate of Secure | Below **3×**, the score is decoration. Refit or retire it |
| Net band-steps | Σ cells × (index_to − index_from), ARR-weighted, Churned = one step past Critical | One signed number for the direction of the whole book |

### Reading the quadrants

| Quadrant | What it means | The move |
| --- | --- | --- |
| Heavy diagonal, thin off-diagonal | The score is not responsive, or nothing is being done | Check the score's inputs before concluding the team is idle — a score built on quarterly survey data cannot move monthly |
| Heavy above-diagonal from At Risk / High | The save motion works | Name the plays that produced it in the commentary; this is the evidence for coverage investment |
| Heavy below-diagonal from Secure | Something systemic degraded — a release, a pricing change, a support backlog | Cut the degrading cells by segment, product and CSM before writing the driver |
| Churned column concentrated in At Risk / Critical | The score is discriminating | Report the lift; this is what makes §10's at-risk number believable |
| **Churned column with mass in Secure / Watch** | False green | The most important finding the report can produce. Root-cause each one and feed it back to `health-score-designer` |

### The four ways it gets built wrong

| Error | Effect | Fix |
| --- | --- | --- |
| Floating population — accounts added between t0 and t1 counted as rows | Improvement rate inflates, because new accounts start Secure | Freeze at t0; memo line for arrivals |
| No Churned column | The matrix becomes descriptive; false-green is invisible and the lift cannot be computed | Churned is an outcome column, not an omission |
| Bands re-cut between t0 and t1 | Every cell is meaningless and the movement is an artefact of the threshold change | Restate t0 bands under the new thresholds and label the restatement |
| Counts only, no ARR | A matrix dominated by 400 small accounts hides the two $500k slides | Both, always; the ARR matrix is the one that drives the decision |

### The sentence to lead with

> "Of the $3.0M ARR we lost in the last ninety days, **$700k — 23.3% — was sitting in Secure or
> Watch at the start of the window.** Rescue rate on the accounts we had already flagged was
> 24.7%; slide rate out of green was 9.9%."

Three numbers, no adjectives, and every one of them actionable. A distribution chart cannot
produce any of them.

---

## 8. Churn reason taxonomy

Fixed, mutually exclusive, and coded as a **chain**, not a single label. Dave Kellogg's framing:
"did not renew" is the event, not the cause of death — the useful record is
`churn → new sponsor → failed implementation → partner problem → partner training` `[P]`.

| Code | Definition | Controllable | Owner of the fix |
| --- | --- | --- | --- |
| `value_not_realised` | Contracted use case never produced the stated outcome | Yes | CS / Onboarding |
| `never_went_live` | Never reached production on the primary use case | Yes | Onboarding |
| `product_gap` | A required capability we do not have and will not build | Partly | Product |
| `champion_loss` | Sponsor departed and was not replaced | Yes | CS |
| `competitive_loss` | Displaced by a named alternative | Partly | CS + Sales |
| `price` | Renewal price or uplift rejected on value grounds | Partly | Pricing |
| `budget_cut` | Their budget removed; the value was not disputed | No | — |
| `m_and_a` | Acquired and consolidated onto another vendor | No | — |
| `business_failure` | Customer ceased trading | No | — |
| `involuntary` | Payment failure, card expiry, dunning exhausted | Yes | Billing ops |
| `strategy_change` | Their business exited the use case | No | — |

Rules: audit the codes quarterly; if `other` exceeds **15%** of coded ARR the taxonomy is broken
and must be fixed before the mix is published. Never let CSMs free-text the reason — it produces
hundreds of unique strings and no analysable signal. Publish the controllable/uncontrollable
split and defend it: attributing every loss to CS is false and demoralising, and attributing
every loss to M&A is self-serving and equally false.

---

## 9. What to leave out

| Leave out | Why |
| --- | --- |
| Activity counts with no outcome attached | QBRs held, emails sent, touches logged. Pair each with the outcome it produced (EBR → expansion identified / risk identified / neutral) or drop it |
| Any metric nobody has ever acted on | If no value of it changes a decision, it is decoration. Cut it, and log the cut |
| A thirtieth tile | Six headline, ≤15 in the body, everything else in the appendix |
| Mean values for time-based metrics | Median and P90. One outlier destroys a mean |
| A metric introduced this month with no history | Show its prior six periods, or hold it until you can |
| Blended-only anything | Blended NRR across segments differing by 20+ points is close to uninformative |
| Vanity selection | Fix the metric set for a year; changes go in the change log with a reason |
