# Model Archetypes

> Read when choosing the shape of the score, defending that choice to a sceptical exec, or
> building the enterprise / PLG / consumption / sparse-data variant.

**Contents**
- [The seven archetypes](#the-seven-archetypes)
- [Choosing between them](#choosing-between-them)
- [§3 — Weight profiles by business model](#3--weight-profiles-by-business-model)
- [§4 — The leading/lagging split](#4--the-leadinglagging-split)
- [§5 — When ML is actually justified](#5--when-ml-is-actually-justified)
- [§6 — The sparse model: no product telemetry](#6--the-sparse-model-no-product-telemetry)
- [§7 — Migrating between archetypes](#7--migrating-between-archetypes)
- [§8 — Segmenting the model](#8--segmenting-the-model)

---

## The seven archetypes

| Archetype | Minimum data | Explainability | Choose when | Main failure |
| --- | --- | --- | --- | --- |
| **Weighted rubric** | 5–8 fields, current-state | Total — a CSM can recompute it by hand | Under ~200 labelled renewals; explainability is a hard requirement | Compensatory: a 100 on Support cancels a 0 on Sponsor |
| **Rubric + override caps** | Same, plus governance | Total | One or more dimensions are genuinely disqualifying. **This is the default** | Caps get abused until half the book is capped |
| **Non-compensatory rollup** | Same | High | Pillars are prerequisites rather than substitutes | Harsh. Needs explaining, or CSMs file it as a bug |
| **Leading / lagging split** | Time series on both | High | Above roughly $50M ARR. Solves "green until it's suddenly red" | Two numbers to govern and two arguments to have |
| **Multi-dimensional, no composite** | Same | Total | As an exec layer *alongside* a composite, never instead of one | Execs ask for one number anyway, and there is no rank order |
| **ML propensity** | ≥300 outcomes, ≥50 negatives, a point-in-time feature store, a named owner | Low without SHAP-to-text | Two or more clean renewal cycles of stored history | Black box → non-adoption. Leakage. Silent decay |
| **Hybrid (rubric operates, model ranks)** | Both | High on the operating layer | Mature end-state | Two sources of truth. Publish the reconciliation rule or lose both |

## Choosing between them

Choose from **data maturity, not ambition.** The question is not "what is the best model" but
"what is the best model whose inputs I can populate for 90% of the book, every day, and whose
output a CSM will act on this week."

```
Do you store score history as a time series?
  no  → Rubric + override caps. Fix history storage first; nothing else is possible without it.
  yes ↓
Do you have ≥100 completed renewal outcomes with decision dates?
  no  → Rubric + override caps, weights v0 expert, validated against proxy labels.
  yes ↓
Do you have ≥300 outcomes and ≥50 negatives, and a point-in-time feature store?
  no  → Rubric + override caps, weights v1-lite (tercile lift).
  yes ↓
Is there a named owner who will re-fit and re-validate quarterly, forever?
  no  → Rubric + override caps, weights v1 outcome-derived. An unowned model decays silently.
  yes → Hybrid: rubric operates and explains, model ranks and forecasts.
```

**The published anchor.** GitLab runs the hybrid shape in production — a PROVE rubric alongside
separate propensity models — having abandoned a pure black box because it "was not easy to
understand the calculation… and was not action-oriented" [GitLab Handbook, *Customer Health
Scoring*, published production config]. That is the single most useful public data point in this
space, because it is a real config with its own stated regrets rather than a vendor's example.

**Reconciliation rule for the hybrid.** Write it before shipping, not after the first
disagreement: *the rubric band governs the play and the CSM's queue; the model's ranking governs
the order within a band and the forecast roll-up. Where they disagree by more than one band, the
account goes on a review list and the disagreement is a data point about the model, not about
the account.*

## §3 — Weight profiles by business model

Resolve the business model from `../../cs-context/references/business-model-profiles.md` **before**
setting weights. Recommending seat utilisation to a consumption business, or QBR completion to a
PLG business, is the most recognisable form of generic output.

All figures below are `[DESIGN]` starting points seeded from published configurations. They are
not measured benchmarks and they exist to be replaced by outcome-derived weights (SKILL.md Step 5).

| # | Family | Enterprise / annual | PLG / self-serve | Consumption | Sparse (no telemetry) |
| --- | --- | --- | --- | --- | --- |
| 1 | Product usage & adoption | 35 | 45 | 40 | **0 — unmeasurable** |
| 2 | Commercial & contract | 15 | 10 | 20 | 20 |
| 3 | Relationship & engagement | 20 | 5 | 15 | 30 |
| 4 | Support & reliability | 10 | 10 | 10 | 20 |
| 5 | Sentiment & VoC | 10 | 5 | 5 | 10 |
| 6 | Billing & payment | 5 | 20 | 5 | 15 |
| 7 | Firmographic & external | 5 | 5 | 5 | 5 |

**What changes, and why:**

- **PLG.** There is often no champion, no exec sponsor and no QBR. Scoring their absence
  manufactures risk on healthy accounts. Billing rises because involuntary churn — a failed card,
  an expired payment method — is a material share of losses rather than a rounding error.
- **Consumption.** Licence utilisation is meaningless. Replace it with **commitment pacing**:
  `consumed / (commitment × elapsed_term_fraction)`. Churn appears as *shortfall*, not logo loss,
  so the label in the prediction sentence must include consumption shortfall ≥ some threshold.
  Separate recurring volume from episodic volume — a one-off backfill is not health.
- **Monthly evergreen.** There is no opt-out deadline, so the horizon is a rolling window rather
  than a countdown. Score continuously on 7- and 14-day windows and expect a much shorter
  detection budget.
- **Self-hosted / on-prem / channel.** Telemetry may not exist at all, and coverage is
  structurally capped. Say so in the ledger rather than faking a usage read.
- **Seasonal (academic, retail, public sector).** Mask the known low season before any decay
  signal fires. Scoring a normal August as risk burns credibility with the CSM who knows better.

## §4 — The leading/lagging split

One composite hides the most important distinction in the score: whether a signal moved *before*
the customer decided or *after*.

| | Leading | Lagging |
| --- | --- | --- |
| Examples | Value-event trend vs own baseline · power-user retention · sponsor state · multithreading breadth · seat activation | NPS · CSAT · ticket volume · escalation count · invoice ageing |
| Answers | Is this relationship going to survive? | How did the last quarter feel? |
| Lead time | 60–180 days | 0–30 days, often after the decision |
| Use | Drives the play and the queue | Explains and confirms |

**Rule: ≥50% of composite weight on leading dimensions.** A score dominated by NPS and ticket
counts turns red after the decision has been made, which is a report, not an instrument.

Publish them as two numbers where the book is large enough to govern two. Where it is not, keep
one composite but tag every dimension `L` or `G` in the spec and check the ratio at every review.

## §5 — When ML is actually justified

Not "when we have data" — when all six of these are true:

1. ≥300 completed outcomes with honest decision dates, of which ≥50 are negatives.
2. A point-in-time feature store, so a feature can be rebuilt as it stood on any past date.
3. A named owner with standing time to re-fit and re-validate, indefinitely.
4. A reason-code layer that turns model output into templated sentences a CSM can act on.
5. A rubric already running, so there is something to fall back to and something to compare against.
6. A drift monitor with a defined rebuild trigger (PSI > 0.25 against the prior quarter).

Miss any one and the model will be built, admired for a quarter, quietly distrusted, and then
ignored — while the rubric everybody actually uses goes ungoverned because attention went to
the model.

**Events-per-variable honesty.** The classic rule is 10–20 churn *events* per predictor
[Peduzzi et al., 1996], so eight predictors implies 80–160 events, not 80 accounts. Riley et al.
(*Statistics in Medicine*, 2019) showed events-per-variable rules of thumb are unreliable and
derived closed-form minimum sample sizes accounting for prevalence and shrinkage. Below the
floor, ship the rubric and say why.

## §6 — The sparse model: no product telemetry

The most common real starting position: a CRM, a support desk, a billing system, and no usage
data joined to `account_id`.

**Build it. Do not wait for telemetry.** A sparse score with honest coverage beats no score, and
it beats a fabricated one.

**Rules specific to sparse:**

1. **Product usage prints as `❌ Missing` at weight 0, and its weight is NOT redistributed.**
   Silent redistribution manufactures a false green — the composite rises because a dimension
   vanished, not because the customer improved.
2. **Lean on override caps, which need no calibration to be useful.** Auto-renew off, notice
   served, sponsor departed, invoice >60 days overdue: each is a decision or a structural fact.
   Their value does not depend on having a fitted model.
3. **Report deciles, never probabilities.** Expect AUC in the **0.62–0.72** range `[P]` — usable
   for ordering, useless as a forecast.
4. **Carry a named instrumentation roadmap in the spec**, with an owner and dates, in this order:
   | # | Instrument | Unlocks | Typical effort |
   | --- | --- | --- | --- |
   | 1 | Login / MAU joined to `account_id` | Any usage dimension at all; the join rate itself | Days |
   | 2 | 5–10 **named value events** (not clicks — the things the customer bought the product to do) | Baseline-relative trend scoring, the highest-lift dimension in most books | Weeks |
   | 3 | Seat activation and last-active per seat | Licence utilisation, power-user retention | Weeks |
   | 4 | Entitlement vs use | Scoring an account only on what it actually bought | Weeks |
5. **Relationship weight rises to 30**, which makes CRM hygiene a scoring input. Say this out
   loud: in a sparse model, an un-logged meeting is indistinguishable from a meeting that did not
   happen, and the score will punish the CSM's admin rather than the customer's behaviour. That
   is a real cost of sparseness, not a reason to hide it.

## §7 — Migrating between archetypes

A change of archetype is a **major** version. It changes what the number means, so every
historical comparison breaks unless you restate history.

| Step | Action |
| --- | --- |
| 1 | Run the new archetype in **shadow** for one full renewal cycle. It computes, it stores history, it drives nothing |
| 2 | Publish the **migration matrix** — old band × new band, counts and ARR — *before* the cutover |
| 3 | Send each CSM the list of their accounts that move, with the reason per account. A silent rescore destroys trust once and permanently |
| 4 | Restate at least four quarters of history under the new model, or state plainly that trend comparisons start from the cutover |
| 5 | Keep the old score computing for one quarter after cutover so disagreements can be diagnosed rather than argued about |

## §8 — Segmenting the model

Segment when the **relationship between a signal and the outcome differs**, not merely when the level differs. If
SMB and Enterprise both churn on usage decline but at different absolute levels, you need different *thresholds*,
not different *models* — and a threshold change is a patch, while a new model is a whole second thing to govern.

| Split | Why one global model under-serves both ends | Published anchor |
| --- | --- | --- |
| **Lifecycle stage** | Onboarding accounts have no baseline; trend scoring on them produces noise | GitLab NULLs every measure except sentiment for the **first 30 days** |
| **Touch model** | Meeting cadence and sponsor state are meaningless for tech-touch | GitLab marks cadence and persona engagement **N/A for Scale and Tech Touch** |
| **Entitlement tier** | Scoring an account on features it never bought is a manufactured red | GitLab scores Premium customers only on Premium-level features |
| **ACV band** | Retention economics genuinely differ by ACV | Benchmarkit 2025 (CY2024, N=225): GRR rises monotonically with ACV, consistent across four years `[M]` |
| **Pricing model** | Usage-based accounts churn differently — as shortfall, not cancellation | Benchmarkit 2025: median GRR **92%** usage-based vs **88%** subscription and hybrid `[M]` |

**N/A is not zero.** The tech-touch and entitlement splits both fail the same way if implemented carelessly: a
dimension that does not apply must be excluded from the denominator, not scored 0. Scoring it 0 makes every
tech-touch account red and every Premium customer look under-adopted.

**Ceiling: 3–5 variants `[DESIGN]`.** Every variant is a separate spec, a separate backtest, a separate band cut
and a separate governance review. The fifth costs more to maintain than it adds in discrimination, and the
maintenance is what lapses first.

**The reconciliation rule.** Where variants exist, one line in the spec states how they roll up: the composite is
never averaged across variants (the scales are not comparable), so portfolio reporting uses **band distribution
per segment**, and a single company-wide "average health score" is not published at all.
