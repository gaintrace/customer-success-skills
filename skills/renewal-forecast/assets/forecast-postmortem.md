# Forecast Post-Mortem — <period>, graded against the frozen <vintage> snapshot

**Internal.** Scored against the snapshot frozen on <date>, not against any version edited during
the period. If the frozen snapshot does not exist, say so and score nothing — a forecast graded
against its own final edit measures field hygiene, not prediction.

---

## Bottom line

<Three sentences: what we called and what closed; which of the three error classes carried most of
the variance; the one process change committed for next quarter, with its owner.>

| | |
|---|---|
| Called (frozen <vintage>) / Actual | $F / $A |
| Forecast accuracy `1 − \|F−A\| / F` | X% (trailing 4Q: A / B / C / D) |
| WAPE `Σ\|Fᵢ−Aᵢ\| / ΣAᵢ` | X% |
| Bias `Σ(Fᵢ−Aᵢ) / ΣAᵢ`, signed | ±X% (3-period trend: …) |
| Gross / net renewal rate (ATR method) | X% / Y% |
| GRR / NRR (cohort method) | X% / Y% · reconciliation gap $Z, mid-term |
| Logo retention | X% (n logos reaching a decision) |

## 1. Accuracy by vintage

| Vintage | Called $ | Actual $ | Accuracy | WAPE | Bias | Read |
|---|---|---|---|---|---|---|
| T-90 | | | | | | The real prediction score |
| T-60 | | | | | | |
| T-30 | | | | | | Closer to bookkeeping than prediction |

**T-90 → actual movement:** $X. <What the movement says about how early risk was seen.>

## 2. Accuracy by segment and by owner

| Cut | Called $ | Actual $ | Accuracy | WAPE | Bias | Read |
|---|---|---|---|---|---|---|

Offsetting errors hide account-level chaos; publish WAPE beside accuracy on every cut.

## 3. Variance decomposition

| Class | $ variance | % of total | Top contributing accounts | Owner of the fix |
|---|---|---|---|---|
| Category error (closed in a different outcome class than called) | | | | Forecast owner |
| Value error (right class, wrong value) | | | | Renewal owner |
| Timing error (slipped into or out of the period) | | | | Ops / deal desk |
| **Total** | | **100%** | | |

## 4. Category performance — the new base rates

| Category | Called ATR $ | Closed won $ | Realised rate | n | Prior quarter | Use as next quarter's base rate? |
|---|---|---|---|---|---|---|
| Closed/Won · Commit · Most Likely · Best Case · At Risk | | | | | | |

Rates with n < 30 are pooled with the adjacent bin and labelled as pooled. These rates replace the
placeholders in `../scripts/forecast.py` input under `base_rates`.

## 5. Loss analysis

| Account | ATR $ | Lost $ | Class (logo / product / contraction) | Cause code | First detectable signal · date | Days of warning | Was it in the register? |
|---|---|---|---|---|---|---|---|

**Days of warning** is the gap between the earliest observable signal and the date the account
entered At Risk. It is the single most useful number in this document: it measures detection, not
outcome. Feed the cause codes to `churn-postmortem`.

## 6. Saves

| Account | ATR $ | Exposure $ | Retained $ | Cause code | Play used | Cost of the save (discount, services, exec time) |
|---|---|---|---|---|---|---|

**Save rate by cause code:** <a rate pooled across cause codes teaches nothing — a pricing save and
a champion-departure save are different motions with different rates.>

## 7. Process changes committed

| # | Change | Class it addresses | Owner | By | How we will know it worked |
|---|---|---|---|---|---|

One change per error class, maximum. A post-mortem that produces no process change was a reporting
exercise.

---

### Assumptions
| # | Assumption | Why it was needed | If wrong |
|---|---|---|---|

### Coverage
**X / 7 signal families (Y%), ATR-weighted → confidence capped at <level>.**
Blind spots: <what is missing and which direction it biases the score.>
