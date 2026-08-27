# Monthly Retention Report — Template

> Emit this verbatim when someone needs the blank document to fill. Fourteen sections in fixed
> order; cut for the audience, never reorder. Delete a `<…>` only by replacing it — a template
> that ships with an unfilled placeholder reads as finished and is not.
>
> Commentary prompts are written out under each section. Answer all five parts or delete none.

---

# Retention Report — <Company> · <period> · <VP / ops review | CSM team | Exec staff | Board appendix>

**Internal.** Published <date> by <name>. Do not forward outside the company.
Basis: <cohort | formula> method · <constant currency, FX as at date> · source of truth
<billing system, reconciled to finance> · as-of <date>.
Business-model profile: <per-seat | consumption | flat tier | hybrid | per-transaction>,
<sales-led | product-led | hybrid>, <monthly evergreen | annual | multi-year>.
<If any set-up question went unanswered: "Run on the recommended defaults: <list>. Say the word
and I'll re-run on a different basis.">

## 0. Headline

| Metric | This period | Prior | vs plan | Trend (6p) |
|---|---|---|---|---|
| TTM NRR | | | | |
| TTM GRR | | | | |
| TTM logo retention | | | | |
| Net new ARR (bridge) | | | | |
| At-risk ARR inside next 2 quarters' ATR | | | | |
| Current-quarter renewal call vs plan | | | | |

## 1. The Call

<3–5 sentences, written before any table exists: what happened · the driver with its arithmetic ·
what is being done · what changes in the forecast · the one decision requested.>

## 2. ARR Bridge

| Period | Beginning | New | Expansion | Reactivation | Contraction | Churn | Ending | Quick ratio |
|---|---|---|---|---|---|---|---|---|
| Month | | | | | | | | |
| QTD | | | | | | | | |
| TTM | | | | | | | | |

| Period | New | Expansion | React. | Contraction | Churn | Net new | Leaky bucket |
|---|---|---|---|---|---|---|---|
| Month | | | | | | | |
| TTM | | | | | | | |

**Tie-out to finance: computed $<X> vs finance ARR $<Y> as at <date> → variance $<Z>.**
*Publishes only at $0.*

*Commentary.* **What:** <number, prior, variance to plan.> **Where:** <which bridge line moved,
and its share of the variance.> **Why:** <mechanism, with evidence.> **So what:** <forward
implication in dollars, over a stated horizon.> **Now what:** <decision, owner, date.>

## 3. GRR · NRR · Logo Retention

| Measure | TTM | Prior TTM | vs plan | Benchmark band [label] |
|---|---|---|---|---|
| GRR (cohort) | | | | |
| NRR (cohort) | | | | |
| Logo retention (cohort) | | | | |

Cohort method; formula-method gap <bps> on GRR and <bps> on NRR (appendix).

| Segment / ACV band | t0 ARR | GRR | NRR | Logo ret. | Logos t0 | Churned | Adverse-selection |
|---|---|---|---|---|---|---|---|
| | | | | | | | |
| **Blended** | | | | | | | |

**Dollar-vs-logo:** dollar churn <X>% vs logo churn <Y>%; adverse-selection index <Z>× blended,
<Z>× in <segment>. <One sentence on what the blended index is hiding.>

*Commentary.* **What / Where / Why / So what / Now what.**

## 4. Cohort View

| Cohort | t0 ARR | T+0 | T+1 | T+2 | T+3 | T+4 | T+5 | T+6 | T+7 |
|---|---|---|---|---|---|---|---|---|---|
| | | | | | | | | | |

`·` = cell does not exist yet. **Cohort-quality drift at T+1:** <oldest> <x>% → <newest> <y>%,
<bps>.

*Commentary.* **What / Where / Why / So what / Now what.**

## 5. Churn by Reason, with ARR

| Reason code | Accounts | ARR | % of churned ARR | Controllable? | Prior period |
|---|---|---|---|---|---|
| | | | | | |
| **Total** | | | 100% | | |

**Controllable / partly / uncontrollable: $<a> (<x>%) · $<b> (<y>%) · $<c> (<z>%).**

### Named losses above <threshold>

| Account | ARR | Segment | Tenure | Reason chain | Contr. | Band at −90d | Flagged | Owner | Lesson |
|---|---|---|---|---|---|---|---|---|---|
| | | | | | | | | | |

*Commentary.* **What / Where / Why / So what / Now what.**

## 6. Contraction

| Reason code | Accounts | ARR | % of contracted ARR | Prior period |
|---|---|---|---|---|
| | | | | |
| **Total** | | 100% | | |

*Commentary.* **What / Where / Why / So what / Now what.**

## 7. Expansion

| Source | ARR | % of gross new ARR | vs plan | Prior period |
|---|---|---|---|---|
| Seats | | | | |
| Tier upgrade | | | | |
| Cross-sell (new SKU) | | | | |
| Price uplift | | | | |
| Usage-commit increase | | | | |
| **Total** | | | | |
| *of which contractual ramp step-ups* | | | | |

*Commentary.* **What / Where / Why / So what / Now what.**

## 8. Health Distribution — as at <date>

| Band | Accounts | % | ARR | % of ARR | Prior period ARR % |
|---|---|---|---|---|---|
| Secure | | | | | |
| Watch | | | | | |
| At Risk | | | | | |
| High Risk | | | | | |
| Critical | | | | | |
| Churned in window | | | | | |

## 9. Health Migration Matrix — <t0 date> → <t1 date>

Frozen t0 population: <n> accounts, $<ARR>. Accounts entering after t0 are a memo line and are
excluded from every rate.

**Accounts**

| t0 \ t1 | Secure | Watch | At Risk | High Risk | Critical | **Churned** | Total t0 |
|---|---|---|---|---|---|---|---|
| Secure | | | | | | | |
| Watch | | | | | | | |
| At Risk | | | | | | | |
| High Risk | | | | | | | |
| Critical | | | | | | | |
| **Total t1** | | | | | | | |

**ARR**

| t0 \ t1 | Secure | Watch | At Risk | High Risk | Critical | **Churned** | Total t0 |
|---|---|---|---|---|---|---|---|
| Secure | | | | | | | |
| Watch | | | | | | | |
| At Risk | | | | | | | |
| High Risk | | | | | | | |
| Critical | | | | | | | |
| **Total t1** | | | | | | | |

*Memo — entered the base after <t0 date>: <n> accounts, $<ARR>. Not in the rates below.*

| Rate | Value | Prior window |
|---|---|---|
| Stability (held their band) | | |
| Improvement rate | | |
| Degradation rate | | |
| Rescue rate | | |
| Slide rate | | |
| **False-green rate** (Secure/Watch that churned) | <x>% (n=<n>) · <y>% ARR-weighted | |
| **Churned ARR that was Secure or Watch at t0** | $<X> — <y>% of all ARR churned in the window | |
| Predictive lift (High+Critical ÷ Secure churn rate) | <n>× (Secure <a>%, n=<n> · High+Critical <b>%) | |
| ARR improved / held / degraded / churned | | |
| Net band-steps, ARR-weighted (positive = degraded) | | |

*Commentary.* **What / Where / Why / So what / Now what.** Lead with the false-green line.

## 10. At-Risk ARR and Coverage

| Reason code | ARR | Accounts | Inside next 2 quarters' ATR | Net of expected save | Movement this period |
|---|---|---|---|---|---|
| | | | | | |
| **Total** | | | | | |

Bucketed by **opt-out deadline** (`renewal_date − notice_period_days`), not renewal date.
Flow this period: entered $<X> (<n> accounts) · resolved and exited $<Y> (<n>) · lost $<Z> (<n>).

| Coverage | ARR | % of base | Accounts | Touch coverage 90d |
|---|---|---|---|---|
| Named 1:1 | | | | |
| Pooled | | | | |
| Digital-only | | | | |
| **Uncovered** | | | | |
| Save rate TTM | | | | |
| Risk detection rate TTM | | | | |

*Commentary.* **What / Where / Why / So what / Now what.**

## 11. Renewals Closed vs Forecast

| Quarter | ATR | Called (frozen T-90) | Called (T-30) | Closed | Accuracy | Signed bias |
|---|---|---|---|---|---|---|
| | | | | | | |
| **Trailing 4** | | | | | | |
| Current QTD | | | | | | |

WAPE across the window <x>%. **Bias: <optimistic | conservative> in <n> of 4 quarters.**

*Commentary.* **What / Where / Why / So what / Now what.**

## 12. Onboarding & Time to Value

| Cohort | Accounts | ARR | Median TTV | P90 TTV | On-time go-live | 30d activation | Stalled ARR |
|---|---|---|---|---|---|---|---|
| | | | | | | | |

Target median TTV: <N> days. Stalled-onboarding ARR total: $<X>.

*Commentary.* **What / Where / Why / So what / Now what.**

## 13. Operating Notes

| Item | Detail | Effect on the numbers |
|---|---|---|
| Definition changes | | |
| Restatements | <use restatement-notice.md> | |
| Data faults found | | |
| Population changes (with the rule applied) | | |
| Changes to this report | | |
| Written skips (R14) — what was left out, why, revisit date | | |

## 14. Decisions Requested

| # | Decision | Owner | Options | Recommendation | $ at stake | Decide by | If deferred |
|---|---|---|---|---|---|---|---|
| 1 | | | | | | | |

### Assumptions

| # | Assumption | Why it was needed | If wrong |
|---|---|---|---|
| 1 | | | |

### Coverage Ledger

| Signal family | Feeds | Source checked | Status | Notes |
|---|---|---|---|---|
| Product usage & adoption | §8, §9, §12 | | ✅/⚠️/❌ | |
| Commercial & contract | §2, §3, §10, §11 | | | |
| Relationship & engagement | §10 coverage, touch coverage | | | |
| Support & reliability | §5 reason codes | | | |
| Sentiment & VoC | §5 reason evidence | | | |
| Billing & payment | §2 tie-out, involuntary churn | | | |
| Firmographic & external | §5 controllable split | | | |

**Coverage: <X> / 7 (<Y>%) → confidence capped at <level>.**
Blind spots: <which families are missing, what they hide here, and which direction the error runs.>
