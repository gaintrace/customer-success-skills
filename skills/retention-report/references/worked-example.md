# A Worked Example

> A complete `retention-report` output in **VP / ops review** mode, on realistic numbers for a
> ~$105M ARR private B2B SaaS company. Read it for the mechanics: how a driver is written, how
> the share of variance is computed, how the migration matrix earns its place, and how a gap is
> declared rather than filled.
>
> Every figure in §2, §3, §4, §9 and §11 is reproducible — amounts are in **thousands of USD**:
> `python3 skills/retention-report/scripts/retention_report.py skills/retention-report/scripts/sample_input.json`
>
> **Contents:** [the report](#retention-report--northwind-analytics--july-2026--vp--ops-review) ·
> [what this example is demonstrating](#what-this-example-is-demonstrating)

---

# Retention Report — Northwind Analytics · July 2026 · VP / ops review

**Internal.** Published 2026-08-07 by Dana Osei (CS Ops). Do not forward outside the company.
Basis: cohort method · constant currency (USD, FX as at 2026-07-31) · source of truth billing
(Stripe), reconciled to finance · as-of 2026-08-05.
Business-model profile: **per-seat, sales-led, annual contracts with notice periods.**

## 0. Headline

| Metric | This period | Prior | vs plan | Trend (6p) |
|---|---|---|---|---|
| TTM NRR | **94.2%** | 96.8% | −331 bps | ▼ 5 of 6 |
| TTM GRR | **83.4%** | 84.9% | −220 bps | ▼ 6 of 6 |
| TTM logo retention | **88.6%** | 89.7% | −140 bps | ▼ 4 of 6 |
| Net new ARR (TTM bridge) | **+$12,212** (+13.2%) | +$14,900 | −$2,690 | ▼ |
| At-risk ARR inside next 2 quarters' ATR | **$5,120** of $38,600 ATR | $4,980 | — | ▲ |
| FY27 Q1 renewal call vs plan | $17,650 called / $18,900 plan | — | −$1,250 | ▼ |

## 1. The Call

TTM GRR fell to 83.4%, 220bps below plan, and SMB carries **50.9% of the $2,036k variance on
13.2% of the base**. The mechanism is onboarding, not renewal: median SMB time-to-value rose
from 44 to 61 days between February and June while onboarding headcount stayed flat and SMB new
logos grew 34%, and $389k of July's $1,196k churn carries reason code `never_went_live`. At the
current cohort hazard this costs a further ~$1.1M of FY27 ARR. Two onboarding FTEs move from
Mid-Market and SMB go-live is gated on a 30-day activation milestone — **the decision needed
from this room is the FTE reallocation, by 2026-09-12, before Q4 hiring closes.** Separately,
$700k — 23.3% — of the ARR lost in the last ninety days was banded Secure or Watch ninety days
earlier, so the health score is not discriminating at the top end and §10's exposure number
should be read as a floor.

## 2. ARR Bridge

| Period | Beginning | New | Expansion | Reactivation | Contraction | Churn | Ending | Quick ratio |
|---|---|---|---|---|---|---|---|---|
| Month (Jul-26) | $103,940 | $1,420 | $980 | $60 | ($392) | ($1,196) | **$104,812** | 1.51 |
| TTM (Aug-25 → Jul-26) | $92,600 | $16,840 | $11,120 | $640 | ($4,510) | ($11,878) | **$104,812** | 1.71 |

| Period | New | Expansion | React. | Contraction | Churn | Net new | Leaky bucket |
|---|---|---|---|---|---|---|---|
| Month | 1.4% | 0.9% | 0.1% | 0.4% | 1.2% | 0.8% | 66.2% |
| TTM | 18.2% | 12.0% | 0.7% | 4.9% | 12.8% | **13.2%** | **58.6%** |

**Tie-out to finance: computed $104,812 vs finance ARR $104,812 as at 2026-08-05 → variance $0.**

*Commentary.* **What:** net new ARR +$12,212 TTM, $2,690 below plan. **Where:** the shortfall is
entirely on the loss side — gross new ARR (New + Expansion) came in $340 *above* plan at $27,960,
while churn plus contraction ran $3,030 above plan at $16,388. **Why:** the leaky-bucket ratio
rose from 46.2% to 58.6% year on year; 58.6 cents of every dollar of gross new ARR is now spent
replacing losses, and $6,290 of the $11,878 churned came from logos acquired in the trailing
eight quarters. **So what:** at this ratio, holding growth requires ~$3.0M more gross new ARR
per year than the FY26 plan assumed, at a new-logo CAC ratio well above the expansion CAC ratio.
**Now what:** the fix is in §12, not in sales capacity — decision 1 in §14.

## 3. GRR · NRR · Logo Retention

| Measure | TTM | Prior TTM | vs plan | Benchmark band |
|---|---|---|---|---|
| GRR (cohort) | **83.40%** | 84.90% | −220 bps (plan 85.6%) | P25 76% · median 84% · P75 91% [M] |
| NRR (cohort) | **94.19%** | 96.80% | −331 bps (plan 97.5%) | P25 92% · median 102% · P75 110% [M] |
| Logo retention (cohort) | **88.59%** | 89.70% | −140 bps (plan 90.0%) | no clean public benchmark — internal trend only |

Benchmark bands: CY2025 actuals, B2B SaaS + AI-native, N=226 (GRR) / N=230 (NRR),
Aleph × Benchmarkit 2026 `[M]`. Cohort method; formula-method gap −110bps on GRR and +13bps on
NRR (appendix A6).

| Segment | t0 ARR | GRR | NRR | Logo ret. | Logos t0 | Churned | Adverse-selection |
|---|---|---|---|---|---|---|---|
| Enterprise (>$150k ACV) | $50,300 | 88.2% | 102.0% | 92.7% | 96 | 7 | 1.04× |
| Mid-Market ($25–150k) | $30,100 | 81.0% | 89.7% | 86.9% | 352 | 46 | 1.06× |
| SMB (<$25k) | $12,200 | **69.5%** | **73.0%** | 88.9% | 700 | 78 | **2.28×** |
| **Blended** | $92,600 | 83.4% | 94.2% | 88.6% | 1,148 | 131 | 1.05× |

**Dollar-vs-logo:** blended dollar churn 11.99% vs logo churn 11.41% — index 1.05×, which reads
as unremarkable. It is not. Inside SMB the index is **2.28×**: the SMB accounts we lost averaged
$39.8k against a $17.4k segment average, which is why SMB GRR (69.5%) sits 19 points below SMB
logo retention (88.9%). We are losing the best SMB customers, and the blended index hides it.

*Commentary.* **What:** TTM GRR 83.4%, −220bps to plan; a $2,036 shortfall in retained ARR.
**Where:** SMB is 13.2% of the opening base and **50.9%** of the variance (−$1,036 of −$2,036);
Mid-Market 29.6% (−$603); Enterprise 19.5% (−$397). **Why:** of $3,102 SMB cohort churn, $1,860
carries `never_went_live`, and those accounts have a median TTV of 71 days against a 30-day
target. **So what:** NRR spread across segments is 29.0 points, so the blended 94.2% is not a
usable number for any decision — every action below is segment-specific. **Now what:** decisions
1 and 2 in §14.

## 4. Cohort View

Dollar retention by acquisition quarter. `·` = the cohort does not have this cell yet.

| Cohort | t0 ARR | T+0 | T+1 | T+2 | T+3 | T+4 | T+5 | T+6 | T+7 |
|---|---|---|---|---|---|---|---|---|---|
| 2024-Q3 | $3,820 | 100.0% | 97.8% | 95.8% | 94.2% | 92.7% | 91.4% | 90.3% | 89.5% |
| 2024-Q4 | $4,180 | 100.0% | 97.4% | 95.2% | 93.3% | 91.6% | 90.2% | 89.0% | · |
| 2025-Q1 | $3,960 | 100.0% | 96.7% | 94.2% | 91.9% | 89.9% | 88.1% | · | · |
| 2025-Q2 | $4,450 | 100.0% | 96.0% | 92.8% | 90.1% | 87.6% | · | · | · |
| 2025-Q3 | $4,310 | 100.0% | 94.9% | 91.2% | 87.9% | · | · | · | · |
| 2025-Q4 | $4,820 | 100.0% | 92.9% | 88.4% | · | · | · | · | · |
| 2026-Q1 | $5,140 | 100.0% | **90.3%** | · | · | · | · | · | · |
| 2026-Q2 | $4,390 | 100.0% | · | · | · | · | · | · | · |

**Cohort-quality drift, read down the columns:** T+1 fell from 97.8% (2024-Q3) to 90.3%
(2026-Q1), **−750 bps**. T+2: −743 bps. T+3: −631 bps.

*Commentary.* **What:** seven consecutive cohorts retained less at T+1 than the one before.
**Where:** the loss is concentrated in the first quarter of tenure and is monotonic — not noise.
**Why:** the 2025-Q4 and 2026-Q1 cohorts are the first whose onboarding ran at the degraded TTV in
§12, and the SMB share of new logos rose from 51% to 63% over the same window, so part of the
drift is mix and part is delivery. **So what:** each 100bps of T+1 drift on a ~$4,700 quarterly
cohort is ~$47 of first-year ARR and roughly double that over three years; the 750bps observed is
~$350 per cohort, ~$1.4M annualised. **Now what:** decision 1, and report the mix/delivery split
next edition once the SMB-only cohort triangle is built (owner: Dana Osei, 2026-09-04).

## 5. Churn by Reason, with ARR — July 2026

| Reason code | Accounts | ARR | % of churned ARR | Controllable? | Prior month |
|---|---|---|---|---|---|
| `m_and_a` | 1 | $412 | 34.4% | No | $0 |
| `never_went_live` | 9 | $389 | 32.5% | Yes | $214 |
| `champion_loss` | 1 | $268 | 22.4% | Yes | $0 |
| `product_gap` | 1 | $96 | 8.0% | Partly | $178 |
| `involuntary` | 1 | $31 | 2.6% | Yes | $22 |
| **Total** | **13** | **$1,196** | 99.9% (rounding) | | $980 |

**Controllable / partly / uncontrollable: $688 (57.5%) · $96 (8.0%) · $412 (34.4%).**

### Named losses above $50k

| Account | ARR | Segment | Tenure | Reason chain | Contr. | Band at −90d | Flagged | Owner | Lesson |
|---|---|---|---|---|---|---|---|---|---|
| Halden Freight | $412 | ENT | 38m | churn → M&A → acquirer consolidated onto incumbent | No | Watch | 34d | P. Raman | The acquisition was public on 2026-03-18 and we detected it 41 days later. No firmographic source is connected (see Coverage Ledger) |
| Corvid Labs | $268 | MM | 14m | churn → sponsor departure → no successor named → single-threaded for 11 months | Yes | **Secure** | never | M. Bell | The score has no multithreading or sponsor-liveness input. This is one of the seven false-greens in §9 |
| Pell & Roe | $141 | MM | 9m | churn → never went live → integration blocked → partner scoping error | Yes | At Risk | 76d | J. Nkemdirim | Flagged in good time and worked for four months past the point it was recoverable. A stop-loss criterion would have released ~120 CSM hours |
| Ostrand Health | $96 | MM | 26m | churn → product gap → audit-log retention | Partly | At Risk | 118d | A. Diallo | Third loss on this gap. $1,240 of regulated-FS ARR carries it — decision 3 |
| 9 SMB accounts | $279 | SMB | 4–11m | 8 × `never_went_live`, 1 × `involuntary` | Yes | 6 Watch, 3 At Risk | 2 of 9 | pooled | None reached the primary use case in production. Median TTV of the nine: 84 days |

*Commentary.* **What:** $1,196 churned in July against a $840 monthly plan. **Where:** one M&A
loss is 34.4% of it; strip it and controllable churn is $688, still $180 above plan. **Why:**
`never_went_live` is the largest controllable code for the third consecutive month and sits
entirely in cohorts onboarded after February. **So what:** at the current SMB cohort hazard FY27
SMB GRR lands at 70–73%, a further ~$1.1M ARR drag. **Now what:** decision 1; Ostrand is the third
FS loss to the same gap — decision 3.

## 6. Contraction — July 2026

| Reason code | Accounts | ARR | % of contracted ARR | Prior month |
|---|---|---|---|---|
| `seat_reduction` | 5 | $214 | 54.6% | $166 |
| `tier_downgrade` | 2 | $98 | 25.0% | $121 |
| `negotiated_discount` | 1 | $80 | 20.4% | $0 |
| **Total** | **8** | **$392** | 100% | $287 |

*Commentary.* **What:** contraction $392, +$105 MoM and +$1,340 TTM. **Where:** all five seat
reductions are Mid-Market accounts renewing in Q1, all five below 55% licence utilisation entering
their renewal window. **Why:** on a per-seat model the buyer trues down to observed usage; median
utilisation across the five was 48%. **So what:** 31 Mid-Market accounts carrying $6,900 of ARR
are below 60% utilisation with renewals inside two quarters — on the observed true-down rate that
is ~$620 of contraction exposure not yet in §10. **Now what:** add sub-60% utilisation to the
at-risk entry criteria. Owner: Dana Osei, by 2026-08-29.

## 7. Expansion — July 2026

| Source | ARR | % of gross new ARR | vs plan | Prior month |
|---|---|---|---|---|
| Seats | $402 | 16.7% | −$48 | $455 |
| Tier upgrade | $186 | 7.8% | +$11 | $174 |
| Cross-sell (new SKU) | $228 | 9.5% | +$36 | $141 |
| Price uplift | $91 | 3.8% | −$4 | $88 |
| Usage-commit increase | $73 | 3.0% | −$12 | $69 |
| **Total** | **$980** | **40.8%** | −$17 | $927 |
| *of which contractual ramp step-ups* | *$164* | *6.8%* | — | *$151* |

*Commentary.* **What:** expansion $980, 40.8% of gross new ARR — in line with the 40% CY2024
median (Benchmarkit 2025, N=81) `[M]`. **Where:** growth is in cross-sell (+$87 MoM), concentrated
in nine Enterprise accounts. **Why:** the second SKU launched in April and the attach motion works
where a named CSM owns it; there is no cross-sell in the pooled tier. **So what:** $19,100 of
pooled ARR has produced $0 cross-sell in four months. **Now what:** run `expansion-finder` across
the pooled tier before committing Q4 expansion quota. Owner: M. Bell, by 2026-09-05.

## 8. Health Distribution — as at 2026-07-31

| Band | Accounts | % | ARR | % of ARR | Prior period ARR % |
|---|---|---|---|---|---|
| Secure | 573 | 46.5% | $51,340 | 50.4% | 51.8% |
| Watch | 362 | 29.4% | $27,800 | 27.3% | 27.9% |
| At Risk | 176 | 14.3% | $13,220 | 13.0% | 13.6% |
| High Risk | 71 | 5.8% | $4,850 | 4.8% | 4.8% |
| Critical | 23 | 1.9% | $1,690 | 1.7% | 1.9% |
| Churned in window | 27 | 2.2% | $3,000 | 2.9% | — |

## 9. Health Migration Matrix — 2026-04-30 → 2026-07-31

Frozen t0 population: 1,232 accounts, $101,900 ARR. Accounts entering after t0 are a memo line
below and are excluded from every rate. Built on the rolling 90-day window rather than MoM — see
Assumption 3.

**Accounts**

| t0 \ t1 | Secure | Watch | At Risk | High Risk | Critical | **Churned** | Total t0 |
|---|---|---|---|---|---|---|---|
| Secure | 498 | 78 | 19 | 6 | 1 | **2** | 604 |
| Watch | 62 | 231 | 44 | 15 | 4 | **5** | 361 |
| At Risk | 11 | 43 | 88 | 21 | 6 | **7** | 176 |
| High Risk | 2 | 9 | 21 | 24 | 6 | **6** | 68 |
| Critical | 0 | 1 | 4 | 5 | 6 | **7** | 23 |
| **Total t1** | 573 | 362 | 176 | 71 | 23 | **27** | **1,232** |

**ARR**

| t0 \ t1 | Secure | Watch | At Risk | High Risk | Critical | **Churned** | Total t0 |
|---|---|---|---|---|---|---|---|
| Secure | $44,900 | $5,900 | $1,300 | $430 | $90 | **$180** | $52,800 |
| Watch | $5,400 | $17,700 | $3,400 | $1,080 | $300 | **$520** | $28,400 |
| At Risk | $900 | $3,500 | $6,700 | $1,400 | $500 | **$900** | $13,900 |
| High Risk | $140 | $620 | $1,500 | $1,540 | $400 | **$700** | $4,900 |
| Critical | $0 | $80 | $320 | $400 | $400 | **$700** | $1,900 |
| **Total t1** | $51,340 | $27,800 | $13,220 | $4,850 | $1,690 | **$3,000** | **$101,900** |

*Memo — entered the base after 2026-04-30: 56 accounts, $6,120 ARR. Not in the rates below.*

| Rate | Value | Prior window |
|---|---|---|
| Stability (held their band) | 68.8% | 71.2% |
| Improvement rate | 25.2% | 22.4% |
| Degradation rate | 16.5% | 14.1% |
| Rescue rate (At Risk/High/Critical → Secure/Watch) | 24.7% | 19.8% |
| Slide rate (Secure/Watch → At Risk or worse) | 9.9% | 8.1% |
| **False-green rate** (Secure/Watch that churned) | **0.73%** (n=7) · **0.86%** ARR-weighted | 0.41% (n=4) |
| **Churned ARR that was Secure or Watch at t0** | **$700 — 23.3% of all ARR churned in the window** | 14.2% |
| Predictive lift (High+Critical ÷ Secure churn rate) | 43.1× (Secure 0.33%, n=2 · High+Critical 14.29%) | 31.6× |
| ARR improved / held / degraded / churned | $12,860 / $71,240 / $14,800 / $3,000 | — |
| Net band-steps, ARR-weighted (positive = degraded) | +$12,050 | +$7,400 |

*Commentary.* **What:** rescue rate improved 490bps to 24.7% and the improvement rate rose to
25.2% — the save motion is working on accounts we have already identified. **Where:** the gain is
entirely in the At Risk row (54 of 176 accounts recovered to Secure or Watch); the High Risk and
Critical rows barely moved, which is consistent with those being decisions rather than signals.
**Why the number that matters is the other one:** 23.3% of all ARR churned in the window was
banded Secure or Watch at the start of it, up from 14.2%, and the largest single loss in that
group — Corvid Labs, $268 — had one contact for eleven months. The score has no multithreading or
sponsor-liveness input, so single-threaded accounts read Secure until the day the contact leaves.
The 43.1× predictive lift is real but built on n=2 in the Secure numerator and should not be
quoted on its own. **So what:** §10's at-risk ARR is a floor, not an estimate; roughly a quarter
of next quarter's losses are currently sitting outside it. **Now what:** decision 2.

## 10. At-Risk ARR and Coverage

| Reason code | ARR | Accounts | Inside next 2 quarters' ATR | Net of expected save | Movement this month |
|---|---|---|---|---|---|
| `value_not_realised` | $2,140 | 31 | $1,340 | $780 | +$410 |
| `champion_loss` | $1,690 | 14 | $980 | $590 | +$180 |
| `product_gap` | $1,480 | 9 | $860 | $640 | +$96 |
| `budget_cut` / `m_and_a` | $1,410 | 12 | $720 | $610 | −$220 |
| `competitive_loss` | $1,280 | 18 | $740 | $380 | −$310 |
| `price` | $940 | 12 | $480 | $180 | −$56 |
| **Total** | **$8,940** | **96** | **$5,120** | **$3,180** | **+$100** |

Bucketed by **opt-out deadline** (`renewal_date − notice_period_days`), not renewal date.
Flow this month: entered $1,860 (19 accounts) · resolved and exited $1,240 (14) · lost $520 (4).

| Coverage | ARR | % of base | Accounts | Touch coverage 90d |
|---|---|---|---|---|
| Named 1:1 | $76,400 | 72.9% | 312 | 84% |
| Pooled | $19,100 | 18.2% | 402 | 61% |
| Digital-only | $7,200 | 6.9% | 486 | n/a |
| **Uncovered** | **$2,112** | **2.0%** | 61 | 12% |
| Save rate TTM | 65.3% ($13,900 retained of $21,300 that reached renewal) | | | |
| Risk detection rate TTM | **43.3%** ($7,100 of $16,388 total loss flagged ≥60d out) | | | |

*Commentary.* **What:** at-risk ARR $8,940, up $100 net; detection rate 43.3%, meaning **$9,288
(56.7%) of the ARR lost over the trailing twelve months was never flagged more than sixty days
before the loss.** **Where:** the undetected loss is concentrated in accounts under 12 months old
and in the pooled tier, where touch coverage is 61%. **Why:** the health score's inputs are
usage-weighted, and a first-year account that never activated has no usage baseline to decline
from — it reads neutral rather than red. **So what:** a 65.3% save rate on a list capturing 43.3%
of eventual loss protects roughly 28% of the loss surface. **Now what:** decision 2 fixes the
score; add an activation-failure entry criterion to the at-risk state. Owner: Dana Osei, by
2026-09-05.

## 11. Renewals Closed vs Forecast

| Quarter | ATR | Called (frozen T-90) | Called (T-30) | Closed | Accuracy | Signed bias |
|---|---|---|---|---|---|---|
| FY26 Q1 | $17,900 | $16,900 | $16,600 | $16,100 | 95.3% | +5.0% |
| FY26 Q2 | $19,400 | $18,200 | $17,900 | $17,050 | 93.7% | +6.7% |
| FY26 Q3 | $18,300 | $17,400 | $17,200 | $16,900 | 97.1% | +3.0% |
| FY26 Q4 | $21,600 | $20,300 | $19,800 | $18,600 | 91.6% | +9.1% |
| **Trailing 4** | $77,200 | $72,800 | $71,500 | $68,650 | **94.4%** | **+6.0%** |
| FY27 Q1 (QTD) | $19,400 | $18,100 | — | $6,120 of $6,480 July ATR | — | — |

WAPE across the window **6.0%**. **Bias: optimistic in all four quarters.**

*Commentary.* **What:** mean accuracy 94.4%, which reads acceptable. **Where:** the defect is not
dispersion — every one of the four quarters was called high, and the T-30 call moved the number
by less than the eventual miss in three of them. **Why:** Commit is being used for "expected to
renew" rather than "committed", so it absorbs accounts that have not confirmed; 71% of the FY26
Q4 miss came from accounts that sat in Commit for the whole quarter without a customer-side
confirmation. **So what:** a systematic +6.0% bias on a $19,400 quarterly ATR is ~$1,160 of
overstatement per quarter carried into the company forecast. **Now what:** redefine Commit to
require a customer-side confirmation recorded against the opportunity, and re-grade Q1 at T-60.
Owner: M. Bell (Renewals), by 2026-08-22.

## 12. Onboarding & Time to Value

| Cohort | Accounts | ARR | Median TTV | P90 TTV | On-time go-live | 30d activation | Stalled ARR |
|---|---|---|---|---|---|---|---|
| 2026-02 | 21 | $1,640 | 44d | 96d | 71% | 62% | $0 |
| 2026-03 | 19 | $1,410 | 47d | 104d | 68% | 59% | $0 |
| 2026-04 | 24 | $1,880 | 52d | 118d | 63% | 55% | $210 |
| 2026-05 | 22 | $1,520 | 58d | 131d | 59% | 51% | $340 |
| 2026-06 | 18 | $1,290 | **61d** | **147d** | 55% | 48% | $480 |
| 2026-07 | 20 | $1,420 | · immature | · | · | 44% (7d partial) | $620 |

Target median TTV: **30 days**. Stalled-onboarding ARR total: **$1,650**.

*Commentary.* **What:** median TTV rose 39% in five months, 44d → 61d; P90 rose 53%, 96d → 147d.
**Where:** median and P90 deteriorate together, so the failure is capacity rather than a
concentrated set of hard implementations — onboarding headcount held at 6 FTE while monthly new
logos rose from 19 to 24 and the SMB share rose from 51% to 63%. **Why:** each onboarding
specialist now carries 4.0 concurrent implementations against a designed load of 2.5. **So what:**
this is the upstream cause of the cohort drift in §4 and of `never_went_live` in §5; $1,650 of ARR
sits in accounts past their target go-live, and on the observed hazard roughly 38% of stalled ARR
does not survive its first renewal. **Now what:** decision 1.

## 13. Operating Notes

| Item | Detail | Effect on the numbers |
|---|---|---|
| Definition change | GRR/NRR moved from formula to cohort method, effective 2026-04-01; 8 quarters restated | GRR +110bps, NRR −13bps against the previously published series. Change log entry 2026-04-01 |
| Restatement | FY26 Q4 churn restated from $2,240 to $2,410: three Mid-Market accounts reclassified from Contraction to Churn after review found they reached $0 ARR mid-term | FY26 Q4 GRR restated 85.3% → 85.1%, −20bps. See `../assets/restatement-notice.md` |
| Data fault | Health-band thresholds were re-cut on 2026-06-12; the June snapshot is not comparable to May | The migration matrix is published on the 90-day window (April → July) instead of MoM. Assumption 3 |
| Population change | 6 accounts reclassified `is_internal` (sandbox), $0 ARR | Logo count −6; logo retention unaffected (all reclassified accounts were excluded from both periods) |
| Change to this report | §6 gains a utilisation column from next edition, following the seat-reduction finding | None this period |
| Written skip (R14) | Per-CSM migration matrix withheld this edition — the band re-cut makes per-owner comparison unsafe. Revisit: 2026-09-07 edition | None |

## 14. Decisions Requested

| # | Decision | Owner | Options | Recommendation | $ at stake | Decide by | If deferred |
|---|---|---|---|---|---|---|---|
| 1 | Move 2 onboarding FTEs from Mid-Market to SMB and gate SMB go-live on a 30-day activation milestone | Rafael Nunes (VP Onboarding) | (a) reallocate 2 FTE · (b) hire 2 FTE (10-week lead) · (c) hold and cap SMB new-logo intake | (a). Reallocation lands in 3 weeks; hiring does not land before the Q4 cohort | ~$1,100 FY27 SMB ARR | **2026-09-12** (Q4 hiring close) | Sept and Oct SMB cohorts onboard at the 61-day median; on the observed hazard that is ~$310 of FY27 ARR per monthly cohort |
| 2 | Add multithreading and sponsor-liveness inputs to the health score and refit against 8 quarters of outcomes | Dana Osei (CS Ops) | (a) refit now · (b) refit at FY27 planning | (a). The score is producing a 23.3% false-green share on churned ARR now | $700 of churned ARR in the last 90 days was banded green | **2026-09-05** | §10 exposure keeps understating and the renewal forecast keeps running +6.0% optimistic |
| 3 | Build audit-log retention, or stop selling into regulated FS | Sasha Lindqvist (CPO) | (a) build (2 sprints) · (b) partner integration · (c) exit the segment | (a) — the gap has now cost 3 logos and gates 2 renewals inside two quarters | $1,240 FS ARR carries the gap; $340 renews in FY27 Q2 | **2026-10-01** | Two FS renewals reach their opt-out deadline with no answer, and the fourth loss is coded before the decision is made |

### Assumptions

| # | Assumption | Why it was needed | If wrong |
|---|---|---|---|
| 1 | 30-day notice period where `notice_period_days` was blank on 14 accounts ($1,900 ARR) | Opt-out bucketing in §10 | Those opt-out dates move up to 60 days earlier; up to $1,900 shifts from FY27 Q2 into FY27 Q1 exposure, and 4 accounts move inside the 90-day window |
| 2 | Reactivation ($640 TTM) excluded from the NRR numerator | Cohort definition — those accounts were not in the t0 cohort | Including it reads NRR 95.00%, +82bps. The trend direction and the segment ranking are unchanged |
| 3 | Migration matrix built on the 90-day window (2026-04-30 → 2026-07-31) rather than MoM | The 2026-06-12 band re-cut makes the June snapshot non-comparable | If the April snapshot is also affected by the re-cut, the improvement and degradation rates are unreliable and only the Churned column stands unaffected |
| 4 | `is_internal` exclusion held at the FY26 rule (34 accounts, $0 ARR) | No documented change to the rule this year | If the rule changed, logo counts move by up to 34 and logo retention by ~30bps; no ARR effect |

### Coverage Ledger

| Signal family | Feeds | Source checked | Status | Notes |
|---|---|---|---|---|
| Product usage & adoption | §8, §9, §12 | Amplitude (through 2026-08-05) | ✅ Complete | 94% account join rate; 26 months history |
| Commercial & contract | §2, §3, §10, §11 | Salesforce + Stripe (through 2026-08-05) | ✅ Complete | Notice period verified against signed MSAs on the top 40 |
| Relationship & engagement | §10 coverage, touch coverage | Gmail, Calendly (through 2026-08-06) | ⚠️ Partial | 2 of 4 pooled-team mailboxes connected — pooled touch coverage of 61% is a floor, not a measurement |
| Support & reliability | §5 reason codes | Zendesk (through 2026-08-04) | ✅ Complete | Jira linked for escalated tickets |
| Sentiment & VoC | §5 reason evidence | — | ❌ Missing | No NPS/CSAT/survey source connected |
| Billing & payment | §2 tie-out, involuntary churn | Stripe (through 2026-08-05) | ✅ Complete | — |
| Firmographic & external | §5 controllable split | — | ❌ Missing | No news/funding/M&A source |

**Coverage: 4.5 / 7 (64%) → confidence capped at Medium.**
Blind spots: with no VoC source, every reason code in §5 is CSM-assigned with no customer
corroboration — the `never_went_live` cluster is corroborated by product data, but `champion_loss`
and `price` are not. With no firmographic source, the controllable/uncontrollable split in §5 is
undefendable at the margin, and the Halden M&A was found manually 41 days after it was public.
Both gaps run the same way: they understate uncontrollable loss and detection lead time.

---

## What this example is demonstrating

| Mechanism | Where to see it |
| --- | --- |
| **A driver, not a description; the tie-out as a published line** | Every commentary block names a mechanism with its arithmetic share — §3 says "SMB is 13.2% of the base and 50.9% of the miss", not "weakness in SMB". §2 prints `variance $0` with the finance balance and its date |
| **Cohort method with the formula gap disclosed; the blended number refusing to hide the segment** | §3: −110bps on GRR so nobody re-derives a different number, and a 1.05× blended adverse-selection index printed next to a 2.28× SMB index |
| **The migration matrix earning its place; a strong statistic distrusted correctly** | §9: 23.3% of churned ARR was green ninety days earlier — a number no distribution chart can produce — and the 43.1× predictive lift is reported *and* flagged as unstable at n=2 |
| **Exposure bucketed by opt-out; bias reported next to accuracy** | §10 with the flow in and out of the at-risk state; §11, where 94.4% accuracy looks fine until you see +6.0% in all four quarters |
| **The leading indicator explaining the lagging one** | §12 onboarding capacity → §4 cohort drift → §5 reason mix → §3 GRR. One story, four sections |
| **Restatement published, not absorbed; a written skip instead of a silent omission** | §13: size, direction, cause and effect; and the per-CSM matrix withheld with a reason and a revisit date |
| **Decisions and assumptions with concrete consequences** | §14: "~$310 of FY27 ARR per monthly cohort", not "we will revisit next month". Each assumption row names what moves and by how much |
| **A gap declared, not filled** | Coverage 4.5/7, confidence capped at Medium, and the blind-spot sentence says which direction the error runs |
