# Prediction Methods

> Read this when someone challenges the rigour of the rules-based model in
> `scoring-model.md`, when you are moving from rules to a fitted model, or when you need to
> express uncertainty honestly without becoming useless.
>
> The short version, if you read nothing else:
>
> 1. A rules-based score is an **ordering**, not a probability, until it has been backtested.
> 2. Accuracy is a banned metric at a 5–20% base rate. Report lift at the top decile and
>    dollars-at-risk captured.
> 3. The precision threshold is set by **CSM capacity**, not by F1. You can only work the
>    number of red accounts you have hours for.
> 4. Label the churn **decision date**, not the contract end date. Getting this wrong is the
>    difference between a model that learns something and a model that memorises the notice period.
> 5. "100% accuracy" is not a goal to aspire to; claiming it is a violation of this library's
>    evidence standard. State the band, state the confidence, state what would change it.

---


Runtime reference for producing analyst-grade churn/renewal-risk analysis. Every threshold below carries a
provenance tag. **Do not present a tagged-`[P]` number as if it were a measured benchmark.**

| Tag | Meaning |
|---|---|
| `[M]` | Measured benchmark from a survey/study with a stated sample and year |
| `[V]` | Vendor product default or published product definition (real, but a vendor's choice, not an industry truth) |
| `[A]` | Academic / methodological result |
| `[P]` | Practitioner rule-of-thumb — widely used, **not measured**. Say so when you use it. |
| `[D]` | Design parameter you must set from the customer's own data. Never assert a value; compute it. |

---

## 1. Framing: three different questions, three different models

Most churn work fails at this step. "Predict churn" is not one problem.

| Formulation | Question it answers | Label / target | Use when | Weakness |
|---|---|---|---|---|
| **Binary classification at a fixed horizon** | "Will this account be gone within H days of the scoring date?" | `is_churn ∈ {0,1}` over `[t, t+H)` | Contractual B2B, fixed renewal dates, CSM workflow needs a ranked worklist | Discards *when*; needs a re-labeled dataset for every H |
| **Survival / time-to-event** | "What is P(still a customer at time t)? What is the hazard now?" | `(duration, event_observed)` with right-censoring | Multi-year contracts, ramped deals, cohort/tenure questions, when most accounts have **not** churned yet (censoring) | Cox assumes proportional hazards; harder to operationalize into a worklist |
| **Uplift / individual treatment effect** | "Which accounts change behavior *because* we intervened?" | Treatment vs. control outcome difference | You already have a good risk model and are allocating scarce CSM hours | Requires randomized or quasi-randomized holdout; most CS orgs have none |

**Uplift quadrants** (standard framing; Wikipedia, *Uplift modelling*): **Persuadables** (respond only if treated — the only group worth CSM time), **Sure Things** (renew anyway), **Lost Causes** (churn regardless), **Sleeping Dogs / Do-Not-Disturb** (intervention makes it *worse* — e.g. a "we noticed your usage dropped" email that hands a distracted buyer the idea of cancelling). A public benchmark for uplift-on-churn exists: the Orange Belgium telecom dataset (arXiv 2312.07206, 2023) `[A]`.

**Decision rule for an agent:** if the org has < ~200 completed renewal events, do **not** propose ML. Propose the
rules-based scorecard in §13 plus the calibration table in §13.5. Cite Google *Rules of ML* Rule #1
("Don't be afraid to launch a product without machine learning") and Rule #4 ("Keep the first model simple
and get the infrastructure right") `[A]`.

---

## 2. Prediction horizon: annual contracts vs. monthly

The horizon must be **long enough to act** and **short enough to be predictable**. In contractual B2B the
binding constraint is the *notice window*, not the model.

| Business model | Scoring cadence | Observation (feature) window | Lead-time gap | Prediction horizon H | Rationale |
|---|---|---|---|---|---|
| Annual contract, enterprise (ACV > $100k) | Weekly | trailing 90 d (with 30 d and 180 d companions) | 30–45 d | **90–120 d before renewal date** | Procurement cycles plus a typical 30–90 d notice clause: the window has to open before the customer's decision does `[P]` |
| Annual contract, mid-market ($25k–$100k) | Weekly | trailing 60–90 d | 14–30 d | **60–90 d** | Shorter buying cycle; still needs a QBR + exec touch to fit |
| Annual contract, SMB (< $25k) | Weekly | trailing 30–60 d | 7–14 d | **45–60 d** | Auto-renew common; window is really "can we get a human on the phone" |
| Monthly / MRR | Daily or weekly | trailing 28 d | 5–7 d | **30 d** | Matches billing cycle; *Fighting Churn With Data* ships `obs_interval = 1 month`, `lead_time = 5 day`, `metric_interval = 7 day` as defaults `[V]` |
| Usage-based / non-contractual | Daily | trailing 30 d | 0–7 d | **30 d** | arXiv 2606.06776 (2026) uses a 30-day observation window followed by a disjoint 30-day churn-evaluation window `[A]` |

**Lead time is not optional.** The observation date must sit *before* the horizon window opens, and features
must be cut off at the observation date, not the renewal date. The canonical construction (Gold, *Fighting
Churn With Data*, Manning 2020, listing 4.4) `[V]`:

```
obs_date   = start_date + n * obs_interval - lead_time
is_churn   = churn_date ∈ [obs_date, obs_date + obs_interval)
features   = aggregate(metrics) over (obs_date - metric_interval, obs_date]
```

The `lead_time` subtraction is what guarantees the model is usable: you are predicting a window that has not
started yet, using only data that existed at `obs_date`.

**Multi-horizon output is better than one number.** Produce `P(churn ≤ 30d)`, `P(≤ 90d)`, `P(≤ next renewal)`
separately. A CSM's action differs completely between "leaving in 3 weeks" and "will not renew in 7 months".

---

## 3. Label definition — the hardest and most-skipped problem

There are **at least five different dates**, and they can be 6+ months apart. Picking the wrong one destroys
the model silently.

| Date | Definition | Typical system-of-record field | Should it be the label? |
|---|---|---|---|
| **Decision date** | When the buying committee actually decided not to renew | *Not recorded anywhere.* Sometimes inferable from CRM stage change, or a "started evaluating competitor" timeline entry | This is the **true** target. Unobservable. |
| **Notice date** | Date the customer formally gave notice / opp moved to Closed-Lost | `Opportunity.CloseDate`, `Opportunity.StageName = 'Closed Lost'`, `Subscription.cancellation_requested_at` | **Best available proxy.** Use this. |
| **Contract end date** | When the subscription term expires | `Subscription.end_date`, `Contract.EndDate` | Use only for *timing* the renewal, not for labelling — it lags the decision by the whole notice period |
| **Service-off date** | When access was actually revoked | Provisioning system | Worst choice — can lag by another 30–90 d, and finance sometimes leaves accounts live |
| **Activity-churn date** | Last observed meaningful activity + inactivity gap | Derived | The only option for non-contractual/PLG. Gold uses a `gap_interval` of `7 day` for weekly-active products `[V]`; the gap must exceed the natural usage period (see the payroll example in §5) |

**Rules for an agent:**

1. **Label on notice date; time features on observation date; report against renewal date.** Confusing these three is the single most common cause of a model that "works" in backtest and fails in production.
2. **Churn is not one event.** Separate the labels: full non-renewal (logo churn), partial downgrade
   (seat/product contraction), involuntary/payment churn, and M&A-driven consolidation. A single binary label
   mixing these produces a model whose top features are billing failures — useless to a CSM. Model
   **voluntary logo non-renewal** as the primary target, **net ARR contraction ≥ X%** as a secondary.
3. **Involuntary churn must be excluded or modelled separately.** Card decline / dunning failure is a
   payments problem, not a CS problem.
4. **Right-censoring is real.** Accounts still active at the end of the observation period are censored, not
   negatives. Classification silently treats them as negatives; survival models handle them correctly. If
   > ~40% of accounts are censored, prefer survival, and use Uno's C (IPCW) rather than Harrell's C —
   Harrell's C starts overestimating performance at roughly **49% censoring** (scikit-survival docs) `[A]`.
5. **Renewal ≠ retention.** An account that renewed at a 40% discount after threatening to leave is a
   "renewed" label that poisons the training set. Add `renewal_arr_delta_pct` and consider labelling
   `arr_delta < -20%` as a positive for a "value-at-risk" model.

---

## 4. Feature engineering: the transformation catalog

Raw counts are nearly useless. Every raw event stream should be expanded through this catalog. Notation:
`m_t` = metric value in the window ending at time `t`; `W` = window length in days.

| Family | Formula | Why it works | Notes / defaults |
|---|---|---|---|
| **Rolling sum / count** | `Σ events ∈ (t-W, t]` | Base signal | Compute at W ∈ {7, 28, 90, 180} d `[D]` |
| **Rolling active users** | `COUNT(DISTINCT user_id) ∈ (t-W, t]` | Breadth, not just volume | WAU (7d) and MAU (28d) |
| **Delta (absolute)** | `m_t − m_{t−W}` | Change detection | |
| **Percent change** | `m_t / m_{t−W} − 1`, guarded `WHERE m_{t−W} > 0` | Scale-free change | Gold's `percent_change` metric guards the zero denominator explicitly `[V]` |
| **Ratio / normalization** | `num / den`, `0` when `den = 0` | Removes account-size confound | e.g. `active_users / users_purchased` = license utilization |
| **Trend slope** | OLS slope of `m` over the last k periods, or Theil–Sen for robustness | Distinguishes decline from a single bad week | k = 13 weekly points is a practical default `[P]` |
| **Volatility** | `stddev(m) / mean(m)` over k periods (coefficient of variation) | High CV = fragile, single-user-dependent usage | |
| **Recency** | `date_t − MAX(event_time WHERE event_time ≤ t)` | "Days since last X" is often the single strongest feature | Build for: last login by any admin, last exec-sponsor touch, last EBR, last support ticket, last invoice paid |
| **Streak / consecutive** | Longest run of periods below threshold | Separates a dip from a decline | e.g. `consecutive_weeks_mau_declining` |
| **Seasonality adjustment** | `m_t / median(m over same calendar window, prior years)` or STL residual | Prevents December/summer false alarms in seasonal verticals (education, retail, tax, healthcare open-enrolment) | Needs ≥ 2 years of history; otherwise use peer-relative instead |
| **Size normalization** | Per seat, per $10k ARR, per licensed user, per active user | An enterprise generating 34 tickets is not "worse" than an SMB generating 4 | **Mandatory** for tickets, events, contacts, meetings |
| **Peer-relative (percentile)** | `percentile_rank(m within {segment × lifecycle stage × product})` | The only way "normal" is meaningful across a heterogeneous book | Rank *within lifecycle stage*, never across the whole base — a 6-week-old account and a 3-year-old account have different normals, and comparing them manufactures risk on one and hides it on the other `[P]` |
| **Entitlement-relative** | `used / contracted` | Reveals shelfware directly, and it is what procurement will look at | |
| **Distributional transforms** | `log(1+x)` when `skew > 4.0 and min ≥ 0`; `asinh(x) = ln(x + √(x²+1))` when `skew > 4.0 and min < 0`; then z-score | Churn metrics are extremely fat-tailed; untransformed z-scores are dominated by 2–3 accounts | `skew_thresh = 4.0` is Gold's shipped default `[V]` |
| **Correlated-group collapse** | Cluster metrics with pairwise `|r| > θ`, average the z-scores within cluster | Kills multicollinearity, makes coefficients interpretable | Gold ships `group_corr_thresh` between **0.5 and 0.75** `[V]` |

**Two hard rules.**
- *Never* feed a raw count and its own size-normalized ratio to a linear model without grouping them; you get
  unstable, sign-flipped coefficients.
- Compute z-score parameters (mean, std) **on the training window only** and persist them
  (Gold saves a `_score_params.csv` with per-column `skew_score`, `fattail_score`, `mean`, `std`) `[V]`.
  Re-standardizing at scoring time on the current population is a leakage vector and causes score drift when
  the customer base grows.
