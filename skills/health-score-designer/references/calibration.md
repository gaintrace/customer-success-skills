# Calibration and Backtesting

> Read when writing Step 8 or Step 9 — the backtest protocol, the metric definitions, the
> leakage traps, the capacity-threshold arithmetic, the reliability curve, and the false-green /
> false-red taxonomy.

**Contents**
- [§1 — The eight-step protocol](#1--the-eight-step-protocol)
- [§2 — Leakage: the seven traps](#2--leakage-the-seven-traps)
- [§3 — The metric suite](#3--the-metric-suite)
- [§4 — Capacity-set thresholds](#4--capacity-set-thresholds)
- [§5 — Turning a score into a probability](#5--turning-a-score-into-a-probability)
- [§6 — The error autopsy](#6--the-error-autopsy)
- [§7 — Drift](#7--drift)
- [§8 — The long-form Backtest Report](#8--the-long-form-backtest-report)

Run `../scripts/backtest.py` for the arithmetic. `../scripts/sample-scores.csv` is a deliberately
mediocre worked example — it fails the top-decile-lift target and trips both capacity warnings,
which is what most first backtests actually look like.

---

## §1 — The eight-step protocol

| # | Step | The trap it closes |
| --- | --- | --- |
| 1 | Snapshot point-in-time at T−180 / 120 / 90 / 60 / 30 **from the opt-out deadline**, not the renewal date | Scoring decisions that had already been made (`R1`, `R24`) |
| 2 | Rebuild every feature as-of each date from immutable event logs, never from current-state tables | The number-one source of leakage |
| 3 | Split temporally — train months 1–12, validate 13–18, test 19–24 | A random split leaks the future and inflates AUC by a lot |
| 4 | Exclude leakage features (§2) | A model that has read the answer |
| 5 | Beat three baselines: the constant base rate, the single best feature, and last quarter's model | A score beating none of them is not earning its build cost |
| 6 | Compute the suite **overall and per segment** | Strong in aggregate, worse than random inside Enterprise |
| 7 | Plot the lead-time curve — AUC at T−30 … T−180 | A score whose AUC only rises inside T−45 is a confirmation device, not a warning system |
| 8 | Autopsy 20 false-greens and 20 false-reds by hand (§6) | More improvement per hour than any parameter search |

**On step 7.** Neslin et al. (*Journal of Marketing Research*, 2006) found churn models suffered
"very little decrease in performance" when scored on a database compiled three months after the
calibration data. A sound model therefore holds at 90-day lead time. **If yours collapses beyond
T−45, suspect leakage in the short-horizon version rather than genius in the long one.**

## §2 — Leakage: the seven traps

Every one of these has been shipped by a competent team and produced an AUC above 0.90 that
evaporated in production.

| # | Leak | How it hides |
| --- | --- | --- |
| 1 | **Current-state tables** — `account.status`, `subscription.state` as they are *now* | Looks like a feature; is the label |
| 2 | **Churn reason / cancellation category** | Only populated after the decision |
| 3 | **`renewal_status`, opportunity stage = Closed Lost** | Same |
| 4 | **Cancellation-request ticket type** | Filed by the customer *as* they leave |
| 5 | **CSM sentiment recorded after notice was served** | GitLab's sentiment field refreshes every two hours — it is contaminated within hours of a churn conversation. Cut sentiment as-of the snapshot date, not the row's current value |
| 6 | **Post-decision activity collapse** | Usage drops *because* they decided. At T−30 this is prediction; at T−5 it is observation |
| 7 | **Aggregations computed over the full window** including post-snapshot months | The silent one. Any `AVG(x) OVER (whole period)` is a leak |

**The test:** for every feature, ask *could this value have been different if I had run the query
on the snapshot date?* If it could not, it is a leak.

## §3 — The metric suite

| Metric | Answers | Target `[DESIGN]` | Notes |
| --- | --- | --- | --- |
| **Base rate (logo and ARR)** | The number every other metric is read against | Compute per segment first | Report it before anything else, always |
| **Top-decile lift** | If CS only works the worst 10%, how much better than random? | ≥2.5× minimum · 3–4× good | The metric a VP actually understands |
| **ARR capture @ decile** | What share of churned *dollars* sits in the worst k%? | ≥40% in worst 10% · ≥65% in worst 20% | A model catching 80% of logos and 30% of dollars has failed |
| **AUC-ROC** | Rank-ordering, threshold-free | ≥0.70 usable · ≥0.78 good · ≥0.85 excellent | Above 0.90 on a first build, assume leakage |
| **PR-AUC** | Honest view under a low base rate | ≥2.5× the base rate | **Use this, not ROC-AUC, when churn is under 10%** |
| **Precision / recall @ threshold** | How often a red is a real loss; what share of loss got flagged | Precision set by capacity (§4) · recall ≥70% at red | These trade off; §4 is how you choose |
| **Brier** | Calibration and sharpness together, lower is better | Beat the base-rate-constant Brier by ≥20% | Requires a fitted probability. Not applicable to a raw rubric |
| **Reliability curve** | Are the stated probabilities real? | Monotone, near-diagonal | The most persuasive single chart for a CCO |
| **KS** | Maximum separation between the two distributions | ≥0.30 | Easy to explain, easy to plot |
| **PSI vs prior quarter** | Drift | <0.10 stable · 0.10–0.25 investigate · >0.25 rebuild | §7 |

**Accuracy is banned as a headline metric.** At a 5% base rate, predicting that nobody churns is
95% accurate and worth nothing. A published demonstration at a much higher (24–25%) base rate:
majority-class **76.6%**, a single-feature threshold rule **83.9%**, best supervised models
**88.5–89.5%** [arXiv:1512.06430, ~100k subscribers, telecom `[A]` — cited for the
methodological lesson, not as a SaaS benchmark]. The lesson is the gap between the second and
third rows: *a single well-chosen behavioural feature captured most of the achievable signal.*
Before building an ensemble, find out what one good feature does.

## §4 — Capacity-set thresholds

**The red line is an operations decision, not a statistical one.** You can only work the number
of red accounts you have hours for, and a red list longer than capacity trains everyone to
ignore all of it (`R13`).

```
capacity      = CSMs × hours_available_for_saves ÷ hours_per_save_motion
red_threshold = the score at which count(accounts below it) ≈ capacity per quarter
```

Use **usable** hours, roughly 60% of nominal (`R13`). A team of 8 CSMs with 4 usable hours a week
for save work and a 10-hour save motion: `8 × 4 × 13 ÷ 10 ≈ 41 save motions per quarter`. That
is the number that sets the threshold — not F1, not Youden's J, not the round number.

**Worked shape `[DESIGN]`** — 2,000 accounts, 8% base rate (160 losses), $60k average ARR,
top-decile lift ≈4.8× decaying across deciles, capacity 200/quarter:

| Threshold | Flagged | Losses caught (recall) | Precision | Churned ARR touched | False positives |
| --- | --- | --- | --- | --- | --- |
| Worst 5% | 100 | 48 (30%) | 48% | $2.9M | 52 |
| **Worst 10%** | **200** | **76 (48%)** | **38%** | **$4.6M** | **124** |
| Worst 20% | 400 | 106 (66%) | 27% | $6.4M | 294 |
| Worst 30% | 600 | 125 (78%) | 21% | $7.5M | 475 |

At capacity 200 you accept ~38% precision and ~48% recall. **That is the correct answer, not a
compromise** — working 400 accounts you do not have hours for produces less saved revenue than
working 200 you do.

**Two floors `[P]`:**
- **Precision below ~25%** — three in four reds are false, CSM credibility burns, and within a
  quarter the alerts are ignored. Raise the threshold or improve the model.
- **Recall below ~40%** — the score is not earning its build cost. Fix discrimination before
  fixing thresholds.

`scripts/backtest.py --capacity N` prints this table from your own data and fires both warnings.

**Cut bands where the observed loss rate changes, not at round numbers.** Published band cuts
differ widely — GitLab's public config uses Green 75–100 / Yellow 50–74 / Red 0–49 — which is
precisely the point: no cut is canonical, because each is fitted to one book's distribution and
one team's capacity. Derive yours, publish it, and do not move it mid-year without restating
history.

## §5 — Turning a score into a probability

**Only after the backtest, and only on data that fitted neither the weights nor the bands.**

1. Hold out a validation set not used to fit weights or bands.
2. Bin into deciles by score.
3. Fit a monotone map from score to observed rate: **Platt scaling under ~1,000 outcomes,
   isotonic regression above** `[P]`.
4. Check the reliability curve: predicted vs observed per decile, with N per bin. It must be
   monotone and near-diagonal.
5. Re-fit the map **quarterly**. Re-fit the weights far less often — the map absorbs base-rate
   drift, and re-weighting monthly makes backtesting impossible because every backtest is
   against a different score.

**Until that map exists, publish bands and deciles, never a percentage** (`R22`). "87% likely to
churn" from an uncalibrated rubric is a fabricated number with a decimal point on it, and the
first visible miss discredits the entire model permanently.

Where `.agents/cs-calibration.json` exists, use its observed band rates and cite the sample size.

## §6 — The error autopsy

Twenty false-greens and twenty false-reds, read by hand, by a human, with the account team.
Budget half a day. It will produce more improvement than a month of parameter search, and it is
the only step that finds *missing dimensions* rather than mis-weighted ones.

**The false-green taxonomy** — accounts that churned while scoring Green at T−90:

| Pattern | What the score missed | Structural fix |
| --- | --- | --- |
| **Aggregate masking** | The buying team left while another team grew. Account total looked fine | Score the *buying* team's usage separately, or add a per-department concentration dimension |
| **Champion departure** | Relationship equity was one person and nobody noticed | Sponsor-state dimension plus a cap; `R3` |
| **Silent dissatisfaction** | No tickets, no survey response, no complaints — and no engagement either | U-curve the support dimension; treat survey silence as missing, not neutral |
| **Budget event** | Layoffs, acquisition, a new CFO. Nothing internal changed | Firmographic family, even at weight 5 |
| **Value never landed** | Usage was fine; the outcome they bought never happened | Add verified-outcome or success-plan-completion as a dimension |
| **Procurement-driven** | Vendor consolidation. The product was liked and cut anyway | Not always predictable. Say so — some churn is genuinely exogenous |
| **Stale feed** | The score was computed on data that stopped arriving in June | Staleness → NA. This is a defect, not a miss |

**The false-red taxonomy** — accounts that scored Red and renewed cleanly:

| Pattern | Fix |
| --- | --- |
| **Seasonal trough scored as decline** | Seasonality mask |
| **Small-baseline noise** | The base ≥20 events guard |
| **Tech-touch scored on relationship dimensions** | N/A those dimensions for that touch model, do not zero them |
| **Entitlement mismatch** | Score only on features they bought |
| **Onboarding accounts with no baseline** | NULL every trend measure for the first 30 days |
| **Migration or replatform dip** | A known-events register that suppresses during planned change |

**Every false-green that was Green at T−90 needs a written post-mortem** and feeds
`churn-postmortem`. They are failures of the model itself, not of the CSM.

## §7 — Drift

| Signal | Threshold | Action |
| --- | --- | --- |
| PSI on the score distribution vs prior quarter | <0.10 | Nothing |
| | 0.10–0.25 | Investigate: a pricing change, a product launch, a segment shift, or a pipeline break |
| | >0.25 | Rebuild, and check whether the population changed before blaming the model |
| Share of accounts changing band per month | >15% | Cliff-edged transforms or noisy inputs (`scoring-functions.md` §5) |
| Share of accounts with any stale input | >5% | Pipeline defect. Route to CS Ops, not to CSMs |
| Score coverage (% of ARR-bearing accounts with a valid score) | <90% | A score covering 60% of the book cannot forecast retention |

## §8 — The long-form Backtest Report

```markdown
# Backtest Report — v<X.Y.Z> · <window> · N=<outcomes> (<neg> negatives)
Label: <event> · Snapshot: T−<N>d from the **opt-out deadline** · Split: train <window> / test <window>
Direction: 0–100, higher = healthier. **Internal.**

## Verdict
<Two sentences: is this score fit for the use it is put to, and the single change with the
largest expected effect on discrimination.>

| Metric | Value | Target | Pass | Baseline to beat |
|---|---|---|---|---|
| Base rate (logo / ARR) | | — | — | — |
| Top-decile lift | | ≥2.5× | | Single best feature: |
| ARR capture @ worst 10% / 20% | | ≥40% / ≥65% | | |
| AUC-ROC · PR-AUC | | ≥0.70 · ≥2.5× base | | |
| Precision / recall @ red | | capacity-set · ≥70% | | |
| Brier · KS | | −20% vs constant · ≥0.30 | | Constant-base-rate Brier: |

### Decile table
| Decile | Score range | N | Losses | Loss rate | Lift | ARR lost | Cumulative ARR capture |
|---|---|---|---|---|---|---|---|

### Per segment
| Segment | N | Base rate | AUC | Top-decile lift | ARR capture @10% |
|---|---|---|---|---|---|

### Reliability curve
| Decile | Mean predicted | Observed rate | N | Gap |
|---|---|---|---|---|
*(Omit entirely if no calibration map is fitted. Do not substitute the raw score.)*

### Lead-time curve
| Snapshot | T−180 | T−120 | T−90 | T−60 | T−30 |
|---|---|---|---|---|---|
| AUC | | | | | |

### Error autopsy
| # | Account | Score at T−90 | Outcome | Failure pattern (§6) | Structural fix | Owner | By |
|---|---|---|---|---|---|---|---|

### Migration matrix (start-of-quarter band → end-of-quarter band)
| Start ↓ / End → | Green | Yellow | Red | Churned | Start total | Qtr loss rate |
|---|---|---|---|---|---|---|

Required read-outs: predictive lift (Red loss rate ÷ Green loss rate) · recovery rate from Red ·
degradation rate from Green · **unforecast churn** — accounts Green at quarter start that churned.

### Assumptions
| # | Assumption | Why it was needed | If wrong |
|---|---|---|---|
```
