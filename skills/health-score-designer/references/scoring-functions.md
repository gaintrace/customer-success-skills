# Scoring Functions

> Read when writing Step 4 — the transform, baseline, decay, noise suppression, seasonality mask
> and NA rule for every dimension. Raw values never enter a composite; this file is how they are
> converted.

**Contents**
- [The five transform types](#the-five-transform-types)
- [§1 — Baseline-relative trend](#1--baseline-relative-trend)
- [§2 — Exponential recency decay](#2--exponential-recency-decay)
- [§3 — Cohort-relative percentile](#3--cohort-relative-percentile)
- [§4 — U-curves and non-monotone signals](#4--u-curves-and-non-monotone-signals)
- [§5 — Noise suppression](#5--noise-suppression)
- [§6 — The NA rule](#6--the-na-rule)
- [§7 — Staleness](#7--staleness)
- [§8 — Per-dimension worked recipes](#8--per-dimension-worked-recipes)

---

## The five transform types

| Type | Shape | Use for | Do not use for |
| --- | --- | --- | --- |
| **Banded** | Step function into 0/25/50/75/100 | Anything a human reads and acts on | Anything feeding a model — steps destroy ordering inside a band |
| **Continuous** | Piecewise-linear or exponential, 0–100 | Model inputs, ranking, velocity | The display layer — a 3-point move looks like news and is not |
| **Baseline-relative** | Compares the account to its own past | Usage, cadence, volume — anything where "normal" is account-specific | Cross-account comparison |
| **Cohort-relative** | Percentile within a peer group | Signals with no natural scale | Absolute reporting — it is zero-sum |
| **Binary / state** | Present or absent | Decisions and structural facts (auto-renew off, notice served) | Anything with a degree |

**The house rule: banded at the display layer, continuous underneath.** Mixing them without
documenting which is which is the single most common cause of "the score jumped 12 points
overnight and nobody can say why."

## §1 — Baseline-relative trend

**Score against the account's own baseline, never an absolute threshold.** A weekly-cadence
account that stays weekly is healthy. A daily account that drops to weekly is churning. An
absolute threshold calls the first one sick and the second one fine.

```
base   = median(weekly_value_events, weeks t-12 … t-5)     # median, not mean: survives outages
recent = median(weekly_value_events, weeks t-3 … t)
trend  = (recent - base) / max(base, epsilon)

s_trend:
  trend >= +0.10           -> 100
  -0.10 <= trend < +0.10   ->  75
  -0.25 <= trend < -0.10   ->  50
  -0.50 <= trend < -0.25   ->  25
  trend <  -0.50           ->   0

Guard: if base < 20 events, return NA. Not 0, and not -100%.
```

**Why the guard matters.** An account with a baseline of 3 events per week that drops to 1 has
"fallen 67%" and is statistically indistinguishable from noise. Without the guard, every small
account is permanently red and the CSM learns to ignore the dimension entirely.

**Worked example.**

| Week | t-12..t-5 events | | Week | t-3..t events |
| --- | --- | --- | --- | --- |
| median of 41, 38, 44, 40, 12, 39, 43, 40 | **40** | | median of 26, 24, 25, 23 | **24.5** |

`trend = (24.5 - 40) / 40 = -0.39` → band `-0.50 ≤ -0.39 < -0.25` → **s_trend = 25**.
Note the 12 in week t-9 (an outage) did not move the median. A mean would have given base 37.1
and trend -0.34 — same band here, but a second outage would have flipped it.

**Choosing the windows.** The lookback must be long enough to establish normal and short enough
to still be about this customer. 8 weeks base / 4 weeks recent is the default `[DESIGN]`. For a
monthly-cadence product use 6 months / 2 months. For consumption, use the commitment period.

## §2 — Exponential recency decay

One interpretable parameter, and one property worth having: **one missed cadence scores exactly 50.**

```
s_recency = 100 × exp(-ln(2) × days_since_event / HL)
```

`HL` (half-life) = the expected cadence in days. Defaults `[DESIGN]`:

| Signal | HL | Reading |
| --- | --- | --- |
| Usage events | 14–30d | 30d for a weekly-use product, 14d for a daily-use one |
| Meetings | = expected cadence (30–90d) | Set from the touch model, not from a global constant |
| Support contact | 45–60d | Long, because silence here is ambiguous |
| Survey response | 90–180d | Very long — survey silence is weak evidence |
| Sponsor touch | 90d | One missed quarter = 50 |

**Worked:** HL = 60d, last exec touch 97 days ago →
`100 × exp(-0.6931 × 97/60) = 100 × exp(-1.1206) = 32.6` → **33**.

**Do not decay state.** Auto-renew being off does not become less true after 60 days. Decay
applies to *contact and activity*, never to decisions and structural facts.

## §3 — Cohort-relative percentile

Use only where there is no natural scale — "is a 12% breadth score good?" has no answer without
a peer group.

```
cohort   = segment × tenure_band × product_tier
minimum  = 30 accounts in the cohort, else fall back one level of granularity  [P]
s        = percentile_rank(account_value, cohort) × 100
```

**The zero-sum warning, stated in the spec every time it is used.** Half the book is below the
median by construction. Portfolio health measured in cohort percentiles **can never improve**,
so a percentile dimension must never appear in a board-level "health is up 4 points" claim. Use
it for ranking within a cohort and nothing else.

## §4 — U-curves and non-monotone signals

**Zero support tickets is not green.** A silent account is either perfectly served or has stopped
trying. In enterprise books the second is more common, and it is exactly the population that
churns without warning.

```
tickets_per_100_seats over 90 days:
  0             ->  60     # ambiguous, not healthy
  0.1 – 2.0     -> 100     # engaged and getting answers
  2.1 – 6.0     ->  75
  6.1 – 12.0    ->  45
  > 12.0        ->  20     # the product is costing them more than it returns
```

**Normalise per 100 licensed seats**, or every large account is red for the crime of being large.

Other non-monotone signals: login frequency at the very top end (a bot or a scraper), admin
config changes (healthy setup vs. panicked reconfiguration before an export), and executive
meeting frequency (a spike is often escalation, not health).

## §5 — Noise suppression

Three mechanisms, all of which belong in the spec rather than in someone's head:

**1. The consecutive-period rule.** Fire only after **N = 2 consecutive weekly periods** below
threshold. If the weekly probability of a spurious dip is roughly independent, requiring two in
a row cuts single-period false positives by roughly an order of magnitude `[P]`. The cost is one
week of lead time, which is worth paying — a dimension that flickers teaches CSMs to ignore it.

**2. Seasonality masks.** Suppress decay signals during known low seasons: the customer's own
quiet quarter (from `cs-context`), December holidays, academic summer, retail change-freeze
windows, and the customer's fiscal close weeks. A masked period holds the last score rather than
scoring the dip.

**3. The fleet-wide diff.** Before believing any account-level decline, check whether the whole
book moved. An event-taxonomy rename at release decays every account simultaneously, and the
first time this happens a CS team spends a week calling healthy customers. Rule: **if >15% of
accounts move the same direction by >5 points in one day, suppress alerts and page CS Ops.**

## §6 — The NA rule

**This is the most consequential line in the spec**, and it is usually written by accident.

When a dimension has no data, four things can happen. Choose explicitly and write it down:

| Option | Behaviour | Use when | Danger |
| --- | --- | --- | --- |
| **(a) Proportional redistribution, capped** | Spread the missing weight over survivors in proportion to their weights, but cap any dimension's increase at **20% of its original weight** | Occasional, random gaps | Uncapped, it hands the biggest increase to whatever was already heaviest — the usual platform default, and it is silent |
| **(b) Impute neutral** | Score the dimension 50 (or the cohort median) | The gap is genuinely uninformative | Pulls everything toward the middle; overused, it collapses the distribution |
| **(c) Composite = NA** | Suppress the whole score | The missing dimension carries >25% of weight | A book full of NAs, which is honest but unusable if it is most of the book |
| **(d) Structural zero, no redistribution** | Weight stays at 0 and the composite is out of <100 | The dimension is *systematically* unavailable (sparse model, on-prem) | None, provided the denominator is printed |

**The one absolute: missing data must never produce a green.** Enforce it with a
**data-sufficiency floor** — if under **70%** of total weight is populated, the account returns
`Insufficient Data`, not a number. An instrumentation failure is an ops defect, not a customer
state, and it routes to CS Ops rather than to the CSM.

## §7 — Staleness

A frozen green on a dead feed is the worst failure in the catalogue, because nothing about it
looks wrong. Staleness forces NA on a timer, per source.

GitLab's published policy is the usable reference point: product usage → NA after **60 days**
without data; support → **30 days**; CSM sentiment flagged stale at **90 days** and forced NA at
**120 days**. Their stated principle: they "prefer to show nothing ('NA') over outdated data."

Two derived requirements:

1. **Every rendered score carries the oldest input timestamp.** Not the score's own compute time
   — the age of its stalest ingredient.
2. **Staleness is monitored as a fleet metric**, not per account. Percentage of accounts with any
   stale input, trended weekly. A pipeline break shows up here days before anyone notices a
   wrong score.

## §8 — Per-dimension worked recipes

| Dimension | Family | Transform | Baseline | NA rule | Notes |
| --- | --- | --- | --- | --- | --- |
| Value-event trend | Usage | §1 baseline-relative, banded | Own 8-week median | (d) if no telemetry, else (a) | The highest-lift single dimension in most books |
| Licence utilisation | Usage | Continuous, `active_seats / purchased_seats`, clipped at 1.0 | Absolute | (b) neutral | Meaningless for consumption — use commitment pacing |
| Commitment pacing | Usage | `consumed / (commitment × elapsed_term_fraction)`, banded around 1.0 | Contract | (c) if consumption is the model | Below 0.7 at 60% elapsed is a shortfall, not a dip |
| Power-user retention | Usage | % of top-decile users active in last 30d vs 90d ago | Own | (a) | Losses concentrate here before they show in totals |
| Feature breadth | Usage | Count of distinct value events used / entitled | Entitlement | (b) | Score only against what they bought |
| Auto-renew state | Commercial | Binary state, override cap | — | (c) — never impute a contract field | A decision, not an indicator (`R2`) |
| Contract trajectory | Commercial | Banded: expansion / flat / downsell | Prior term | (b) | |
| Discount depth | Commercial | Percentile vs segment median, banded | Cohort | (b) | Deep discount = weak value case, not a bargain |
| Sponsor state | Relationship | State: named+active / named+quiet / departed / never | — | (a) | Departure with no replacement in 45 days is a cap |
| Multithreading | Relationship | Count of *personas* covered with a two-way interaction in 90d | Absolute, 3+ = 100 | (b) | Count personas, not contacts. Five people in one team is single-threaded |
| Meeting recency | Relationship | §2 decay, HL = expected cadence | Touch model | (d) for tech-touch | N/A for tech-touch, not zero |
| Tickets per 100 seats | Support | §4 U-curve | Absolute | (b) | Normalise or every large account is red |
| Open P1 age | Support | Continuous, days, banded | Absolute | (b) | Age of the *oldest* open, not the count |
| Reopen rate | Support | % reopened in 90d | Cohort | (b) | Best single proxy for "we are not actually fixing things" |
| CSM sentiment | Sentiment | R/Y/G, written justification mandatory | — | Stale 90d, NA 120d | Red forces the composite red. Audit per-CSM calibration |
| CSAT trend | Sentiment | §1 on resolved-ticket CSAT | Own | (b) | |
| NPS | Sentiment | Score with response rate as a confidence weight | Cohort | (b) | Under 20% response, treat as anecdote |
| Days-late trend | Billing | §1 on mean days-to-pay | Own | (b) | Slowing payment precedes non-renewal |
| Payment failures | Billing | Count in 90d, banded | Absolute | (c) for PLG | Involuntary churn is material in self-serve |
| Funding / layoff / M&A | Firmographic | State, decayed over 180d | — | (d) if no source | Unactionable alone; drives urgency, not the play |
