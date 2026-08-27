# The Health Score Audit

> Read in Audit mode — when someone says "nobody trusts the score" or "green accounts keep
> churning". Thirty checks in six groups, plus the test that outranks all of them.

**Contents**
- [Start here: the does-anyone-act-on-it test](#start-here-the-does-anyone-act-on-it-test)
- [The 30 checks](#the-30-checks)
- [Severity and the verdict](#severity-and-the-verdict)
- [The long-form Audit Report](#the-long-form-audit-report)

**Audit before you rebuild.** A score in production is your one real asset: a history of the
current model's errors. Rebuilding before diagnosing throws it away and usually reproduces the
same mistakes in a new coat.

---

## Start here: the does-anyone-act-on-it test

**A score nobody acts on has already failed, whatever its AUC.** Run these six before opening the
model. If four or more fail, stop the technical audit — the problem is adoption, and better
discrimination will not fix it.

| # | Test | Measure | Pass |
| --- | --- | --- | --- |
| 1 | **Reds worked** | % of red accounts with a documented save plan inside SLA | ≥80% |
| 2 | **Override rate** | % of portfolio manually overridden per quarter | ≤10% |
| 3 | **Forecast use** | Is the band cited by name in the renewal forecast call? | Yes |
| 4 | **CSM recall** | Can a CSM name their lowest pillar without opening the tool? | Yes |
| 5 | **Green-at-churn** | % of losses that were Green at T−90 | ≤10% |
| 6 | **Distribution** | % of accounts landing between 60 and 75 | ≤40% |

Check 6 is the central-tendency collapse: with enough contradictory dimensions, every account
averages to the middle and the score ranks nothing. It is the most common failure and the least
often diagnosed, because the score *looks* fine — it just never says anything.

Check 2 cuts both ways. Under 2% overrides usually means CSMs have given up on the tool rather
than that the model is perfect.

## The 30 checks

### A. The prediction (1–5)

| # | Check | Fail looks like |
| --- | --- | --- |
| 1 | A falsifiable prediction sentence exists in writing | "It measures overall customer health" |
| 2 | The event is named and singular | Churn, expansion and satisfaction blended into one number |
| 3 | The horizon is stated and measured to the **opt-out deadline** | Horizon measured to the renewal date, so the score is late by the notice period (`R1`) |
| 4 | The unit is stated (account / subscription / product line / parent) | A multi-product account goes red for one bad product |
| 5 | The population is stated, with exclusions | Onboarding accounts scored on trend, producing noise |

### B. The dimensions (6–12)

| # | Check | Fail looks like |
| --- | --- | --- |
| 6 | 5–8 dimensions, each mapped to one of the seven signal families | 15+ measures nobody remembers |
| 7 | Every dimension passed a predictiveness test on *this* book | Dimensions chosen in a workshop by seniority |
| 8 | Every dimension has a lead time, and ≥50% of weight is on leading dimensions | Score dominated by NPS and ticket counts — it turns red after the decision |
| 9 | Every dimension is actionable: a red names a play, an owner and an SLA | "Industry" or "company size" in the score. They belong in segmentation |
| 10 | No dimension can be moved by a CSM without changing reality | Contact stuffing, meeting theatre, sentiment inflation |
| 11 | Correlated dimensions deduplicated within a family | Logins, MAU and sessions all present — one signal with three votes |
| 12 | Rejected candidates are documented with the axis they failed | The same argument re-run every quarter |

### C. The arithmetic (13–19)

| # | Check | Fail looks like |
| --- | --- | --- |
| 13 | Weights sum to 100 at every tier | Rounding drift after an edit |
| 14 | Nothing below 5% | A dimension at 3%: a full swing from 100 to 0 moves the composite 3 points, less than one band width. It cannot matter — delete it or give it an override cap |
| 15 | Nothing above 35% in a composite of ≥5 | A single-metric score wearing a costume |
| 16 | Every dimension has an explicit transform, not a raw value | Raw logins entering the composite |
| 17 | Trend measures score against the account's **own** baseline | An absolute threshold calling a healthy weekly account sick |
| 18 | Cohort-percentile dimensions are not reported as absolute health | "Portfolio health improved" from a zero-sum measure |
| 19 | Non-monotone signals are U-curved | Zero support tickets scoring green |

### D. Missing data and staleness (20–24)

| # | Check | Fail looks like |
| --- | --- | --- |
| 20 | An explicit NA rule per dimension | Redistribution happening by default, silently |
| 21 | Redistribution capped, or disabled | The heaviest dimension quietly getting heavier every time a feed breaks |
| 22 | A data-sufficiency floor that suppresses the score | Missing data producing a green |
| 23 | Staleness forces NA on a per-source timer | A frozen green on a feed that died in June |
| 24 | Every rendered score shows its **oldest input timestamp** | Compute time shown instead of ingredient age |

### E. Validation (25–27)

| # | Check | Fail looks like |
| --- | --- | --- |
| 25 | Score history is stored as a time series | Overwritten in place. **Priority zero** — nothing can be validated without it and it cannot be recovered retroactively |
| 26 | A backtest exists, with temporal splits and named excluded leakage features | A random train/test split, and an AUC nobody can reproduce |
| 27 | No probability is published without a fitted calibration map | "87% churn risk" from a rubric (`R22`) |

### F. Operation (28–30)

| # | Check | Fail looks like |
| --- | --- | --- |
| 28 | One named owner in CS Ops | Owned by "the health score working group" |
| 29 | Every band owns a play with action · owner · date · expected effect · success measure | Bands that describe rather than instruct |
| 30 | The score is not an input to CSM compensation | Goodhart's law, arriving on schedule |

## Severity and the verdict

| Severity | Definition |
| --- | --- |
| **P0** | The score is producing wrong calls today, or cannot ever be validated. Checks 3, 22, 23, 25, 27 |
| **P1** | The score is materially weaker than it should be. Checks 6, 8, 9, 14, 15, 20, 26 |
| **P2** | Hygiene, clarity or governance debt |

| Verdict | Criteria | Consequence |
| --- | --- | --- |
| **Trustworthy** | No P0. ≤2 P1. Does-anyone-act-on-it ≥5/6 | Fix the P1s in place, keep the version |
| **Repairable** | ≤2 P0, all of them instrumentation or governance rather than design | Fix, re-backtest, minor version bump |
| **Rebuild** | ≥3 P0, or the prediction sentence cannot be written, or ≥4 of 6 adoption tests fail | Redesign from Step 1 — but keep the old score computing in shadow for a quarter |

**Rebuild is the rarest correct verdict.** Reach for it when the score predicts a different event
than the one people are using it for, not when it is merely mis-weighted.

## The long-form Audit Report

```markdown
# Health Score Audit — <existing score> · <date>
**Internal.** Direction: 0–100, higher = healthier. Auditor: <name>. Model version: <v>.

**Verdict:** Trustworthy / Repairable / Rebuild — <one line, and the single fix with the
largest expected effect>

## Does-anyone-act-on-it
| # | Test | Measure | Result | Pass |
|---|---|---|---|---|

## Findings
| # | Check | Group | Finding | Severity | Fix | Owner | By | Expected effect | Success measure |
|---|---|---|---|---|---|---|---|---|---|

## What is working
<Named, specifically. An audit that finds only faults is not read twice, and the things
worth preserving through a rebuild have to be written down before the rebuild starts.>

### Coverage Ledger
| Signal family | Source checked | Status | In score? | Weight | Notes |
|---|---|---|---|---|---|
| Product usage & adoption | | ✅/⚠️/❌ | | | |
| Commercial & contract | | | | | |
| Relationship & engagement | | | | | |
| Support & reliability | | | | | |
| Sentiment & VoC | | | | | |
| Billing & payment | | | | | |
| Firmographic & external | | | | | |

**Coverage: X / 7 families (Y%) → confidence capped at <level>** (`R23`).
Blind spots: <which families are missing and what they typically hide.>

### Assumptions
| # | Assumption | Why it was needed | If wrong |
|---|---|---|---|
```
