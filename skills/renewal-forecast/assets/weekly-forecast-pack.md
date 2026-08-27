# Weekly Forecast Pack — <scope> · <period> · snapshot <YYYY-MM-DD> (vintage T-<N>)

**Internal.** Forecast categories, risk bands, ARR-at-risk figures and save plans never leave this
document. Nothing on this page is customer-facing in any wording.

Published ≥12 hours before the call. Produced by `../scripts/forecast.py` plus the judgement calls.
Read before the call; the call does not read it aloud.

---

## The number

| | |
|---|---|
| Base case (Closed + Commit + Most Likely) | **$X** (Y% of ATR) |
| Band (downside / upside) | $A / $C |
| ATR | $X across N renewals |
| Change vs last week | $±X — <the two accounts that explain most of it> |
| At Risk exposure (excluded from base) | $X across N renewals · at-risk coverage Z% |
| Submitted last week | $X · variance to today $±Y |
| Confidence | High / Medium / Low — <criteria met> |

**Three swing accounts this week:** <Account> $X · <Account> $Y · <Account> $Z.

---

## 1. Paper and notice exceptions   <!-- first, because they are the only rows with a deadline -->

| Exception | Account | ATR $ | Opt-out date | Days left | Owner | Action · by |
|---|---|---|---|---|---|---|
| Commit inside T-45, no order form issued | | | | | | |
| Opt-out deadline passed, unconfirmed | | | | | | |
| `notice_period_days` null — `UNKNOWN — requires the executed contract` | | | | | | |
| Auto-renew flag changed since last snapshot | | | | | | |

## 2. Movement since <prior snapshot date>

| Account | From → To | ATR $ | Called Δ $ | Observable fact that changed (source · date) | Called by | On | Written explanation |
|---|---|---|---|---|---|---|---|

Every row answers all three: what observable fact changed · who called it and what artifact backs
it · the dated action and what the number becomes if it works and if it fails.

## 3. Inspection list   <!-- the §5 selection from references/forecast-call.md -->

| # | Account | ATR $ | Called $ | Category | Why inspected | Days to opt-out | Owner |
|---|---|---|---|---|---|---|---|

Ranked by `ATR × (1 − base rate for its category)`, tie-broken by days to opt-out ascending.

## 4. At-risk register

| Account | ATR $ | Called $ | Cause code | First detected | Save owner | Exec sponsor | Save plan · date | Save probability basis |
|---|---|---|---|---|---|---|---|---|

**At-risk coverage:** at-risk ARR with a dated save plan ÷ total at-risk ARR = **Z%**. Below 100%,
the uncovered dollars are called at zero.

## 5. Bias scan

| Tell | Measured | Threshold | Reading | Challenge question |
|---|---|---|---|---|

## 6. Actions out of this call

| # | Action | Owner | By | Expected effect ($) | Success measure |
|---|---|---|---|---|---|

---

### Assumptions
| # | Assumption | Why it was needed | If wrong |
|---|---|---|---|

### Coverage
**X / 7 signal families (Y%), ATR-weighted → confidence capped at <level>.**
Blind spots: <which families are missing, what they hide, and in which direction the forecast is
likely to be wrong.>
