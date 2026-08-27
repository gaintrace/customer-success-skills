# Health Score Specification — <Company> · v<X.Y.Z> · <date>

**Internal.** Direction: **0–100, higher = healthier.** Owner: <name, CS Ops>.
Supersedes: <v, date> · Next review: <date>

> Emit this verbatim in Full mode. In Brief mode, emit only the Bottom Line block plus §1 and §6
> and offer the rest. Health space is 0–100 and higher is better; `churn-risk` scores risk, where
> higher is worse. `health = 100 − risk` is **not** a safe conversion, so the direction line above
> is mandatory on every artifact.

---

## Bottom Line

<Three sentences. What this score predicts. How well it does it, with the number. The single
change with the largest expected effect on discrimination, its owner and its date.>

| | |
|---|---|
| Predicts | <event> within <H> days of the **opt-out deadline**, at the <unit> grain |
| Population | <tenure / segment / touch filter> — N accounts, $X ARR covered |
| Archetype | <rubric + caps / non-compensatory / leading-lagging / hybrid> |
| Business model | <annual contract / PLG / consumption / mixed> — profile applied |
| Weight method | v0 expert · v1-lite lift · v1 outcome-derived (N=<outcomes>, <neg> negatives) |
| Validated? | Backtested on N outcomes, <window> — OR — **Not yet validated: bands only, no probabilities** (`R22`) |
| Red threshold | <score>, from a stated capacity of <N> save motions per quarter (`R13`) |
| Score coverage | X% of ARR-bearing accounts carry a valid score |
| As-of | <date of the newest input; the oldest input timestamp per dimension is in §2> |
| Confidence | High / Medium / Low — <which criteria are met> (`R23`) |

---

## 1. Prediction Sentence

> An account scoring **X** on date *d* has probability **p** of **<named event>** at its next
> renewal decision within horizon **H**, at the **<unit>** grain, over population **<P>**.

| Decision | Value | Why this and not the alternative |
|---|---|---|
| Event (label) | | |
| Horizon H | | Measured to `renewal_date − notice_period_days`, never to the renewal date (`R1`) |
| Unit | | |
| Population | | |
| Second label tracked separately | ARR-weighted outcome | A model catching 80% of logos and 30% of dollars has failed |

---

## 2. Dimensions

| # | Family | Dimension | Weight | Transform | Green (100) | Yellow (60) | Red (0) | Source · field | NA rule | Staleness → NA | Lead time | Play if red |
|---|---|---|---|---|---|---|---|---|---|---|---|---|

**Hygiene check:** sums to 100 ✅/❌ · minimum weight X% (floor 5) · maximum Y% (ceiling 35) ·
count N (5–8) · leading share Z% (floor 50).

**Rejected candidates** — the record that stops the same argument being re-run every quarter:

| Candidate | Family | Axis failed (predictiveness / lead time / actionability / integrity) | Where it went instead |
|---|---|---|---|

---

## 3. Scoring Functions

| Dimension | Baseline | Formula | Decay half-life | Consecutive-period rule | Seasonality mask | Guard |
|---|---|---|---|---|---|---|

---

## 4. Non-Compensatory Layer

| Override cap | Condition | Cap | Evidence source · field | Expiry | Rule |
|---|---|---|---|---|---|
| | Non-renewal notice served, or auto-renew switched off | ≤29 | | | `R2` |
| | Competitive evaluation or RFP confirmed | ≤49 | | | `R2` |
| | Executive sponsor departed, no replacement named within 45 days | ≤49 | | | `R3` |
| | Invoice >60 days overdue | ≤49 | | | |
| | CSM sentiment = Red, with written justification | ≤49 | | | |
| | Licence utilisation <50% at >180 days tenure | ≤59 | | | |
| | **Data sufficiency <70% of weight populated** | **Suppress → "Insufficient Data"** | | | `R23` |

**NA policy:** <(a) proportional redistribution capped at 20% of original weight / (b) impute
neutral / (c) composite = NA / (d) structural zero, no redistribution>
**Data-sufficiency floor:** <X%> · **Sub-scores published with every composite:** yes / no

---

## 5. Segmentation

| Segment | Population rule | Parameter overrides | Justified by a *relationship* difference? | Reconciliation rule |
|---|---|---|---|---|

Ceiling: 3–5 variants. Every variant is a separate spec, backtest, band cut and governance
review, so the fifth costs more than it discriminates.

---

## 6. Bands and Plays

| Band | Range | % accounts | % ARR | Observed loss rate | Owner | Required action | SLA |
|---|---|---|---|---|---|---|---|
| Green & stable | | | | | | Expansion motion — gated on the health floor (`R8`), run by `expansion-finder` | |
| **Green, falling ≥10 pts / 30d** | | | | | | Diagnostic call. **Do not wait for the band to change** | |
| Yellow | | | | | | Play matched to the lowest-scoring pillar | |
| Red, or any cap fired | | | | | | Risk record + named root cause + save plan (`save-play`) | |
| Insufficient data | | | | — | CS Ops | Instrumentation fix — an ops defect, not a customer state | |

---

## 7. Explainability Contract

Rendered with every score, with no analyst in the loop:

| # | Element | Rule |
|---|---|---|
| 1 | Level | The composite, with its direction stated |
| 2 | Velocity | 30-day and 90-day delta as first-class fields |
| 3 | Top 3 movers | Attributed **to the delta**, not to the level. "Support is your lowest pillar" is true for half the book |
| 4 | Lowest pillar vs its band | |
| 5 | Data completeness | % of weight populated, and the **oldest input timestamp** |
| 6 | The play | Action · owner · date · expected effect · success measure |

---

## 8. Remediation Roadmap

| # | Action | Owner | By | Expected effect | Success measure |
|---|---|---|---|---|---|

---

## 9. Governance

| Object | Rule | Owner | Next review |
|---|---|---|---|
| Owner | | | |
| Versioning | major = dimensions/label · minor = weights · patch = thresholds | | |
| Change control | Champion/challenger, one full renewal cycle in shadow | | |
| Rescore comms | Migration matrix published before cutover | | |
| Refresh | Composite daily · history forever · bands quarterly · weights semi-annual | | |
| Coverage target | % of ARR-bearing accounts with a valid score | | |
| Compensation | The score is **not** an input to CSM comp | | |

---

### Coverage Ledger

| Signal family | Source checked | Status | In score? | Weight | Oldest input | Notes |
|---|---|---|---|---|---|---|
| Product usage & adoption | | ✅/⚠️/❌ | | | | |
| Commercial & contract | | | | | | |
| Relationship & engagement | | | | | | |
| Support & reliability | | | | | | |
| Sentiment & VoC | | | | | | |
| Billing & payment | | | | | | |
| Firmographic & external | | | | | | |

**Coverage: X / 7 families (Y%) → confidence capped at <level>** (`R23`).
Blind spots: <which families are missing, and what they typically hide.>

### Label & History Sufficiency

Anything absent is written `UNKNOWN — requires <source/field>`. Never a benchmark.

| Requirement | Have | Need | What it gates |
|---|---|---|---|
| Stored score history (time series) | | ≥1 renewal cycle | Backtest, drift, velocity |
| Completed renewal outcomes | | ≥100 (v1-lite) / ≥300 (v1) | Outcome-derived weights |
| Negative events | | ≥50 | Logistic fit |
| `churn_event.decision_date` captured | | required | Honest labels (`R24`) |
| Point-in-time feature store | | required | Leakage-free backtest |

### Assumptions

| # | Assumption | Why it was needed | If wrong |
|---|---|---|---|
