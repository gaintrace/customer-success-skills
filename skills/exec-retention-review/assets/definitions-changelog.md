# Appendix — Definitions, Formulas and Change Log

> Emitted verbatim as the appendix of every retention pack. Its purpose is that no number in
> the pack can be questioned on method without the answer already being in the room.

---

## A1. Definitions and formulas

| Metric | Formula | Window | Denominator | Exclusions | Source system |
|---|---|---|---|---|---|
| ARR | Annualised contracted recurring subscription revenue in force | Point in time | — | Professional services, one-time fees, overages (state policy), signed-not-live (that is CARR) | <billing> |
| CARR | ARR including signed contracts not yet live | Point in time | — | — | <CRM> |
| GRR | Cohort: t1 ARR from the t0 cohort with expansion above each account's t0 ARR stripped out ÷ t0 cohort ARR | TTM | t0 cohort ARR | Reactivation; in-period new logos | <billing> |
| NRR | Cohort: t1 ARR from the t0 cohort ÷ t0 cohort ARR | TTM | t0 cohort ARR | Reactivation; in-period new logos | <billing> |
| Logo retention | t0-cohort customers active at t1 ÷ active at t0 | TTM | t0 cohort count | Free, trial, freemium | <billing> |
| Gross $ renewal rate | Renewed ARR ÷ ATR ARR | Quarterly | ATR (smaller than total ARR — not comparable to GRR) | — | <CRM> |
| ATR | ARR with a contractual renewal date inside the period | Per quarter | — | — | <CRM> |
| Opt-out deadline | `renewal_date − notice_period_days` | Per subscription | — | — | <CRM> |
| At-risk ARR | Σ ARR of accounts in a declared, dated, reason-coded at-risk state | Point in time | — | Health-score bands alone do not qualify | <CS platform> |
| Risk detection rate | ARR flagged at-risk ≥60d before loss ÷ total ARR lost | TTM | Total ARR lost | — | <CS platform> |
| Save rate | At-risk ARR retained ÷ at-risk ARR reaching its renewal date | TTM | At-risk ARR reaching renewal | — | <CS platform> |
| Forecast accuracy | `1 − abs(Called − Closed) / Called` | Quarterly, by vintage | Called ARR | Graded from a frozen snapshot only | <CRM> |
| Forecast bias (signed) | `Σ(Fᵢ − Aᵢ) / Σ Aᵢ` | Quarterly, by vintage | Σ actuals | — | <CRM> |
| Quick ratio | `(New + Expansion) ÷ (Churn + Contraction)` | Quarterly | — | State whether reactivation is in the numerator | <billing> |
| Concentration (top N) | Σ ARR of top N ÷ total ARR | Point in time | Total ARR | — | <billing> |
| Herfindahl index | `Σ (ARRᵢ / total ARR)²` | Point in time | — | — | <billing> |
| Cost of retention | Fully loaded CS + Support opex ÷ ARR | TTM | ARR | State whether Support is included | <finance> |
| ARR per CSM | ARR under management ÷ quota-carrying CSM FTEs | Point in time | Quota-carrying FTEs only | Managers, ops, onboarding — or state that they are included | <finance + HRIS> |

---

## A2. Change log

Every definition change, restatement and segment-boundary move. Dated. **Silent restatement
destroys every trend line previously published, retroactively.**

| Date | What changed | Reason | Periods restated | Effect on the headline | Where shown |
|---|---|---|---|---|---|
| YYYY-MM-DD | <e.g. usage overage removed from the ARR base> | <e.g. single-period NRR unreadable due to overage volatility> | <e.g. 8 quarters> | <e.g. NRR −210 bps across all periods> | Slide 3, as-reported in grey and restated in black |

**Restatement policy.** Restatements are published as a separate line with the reason, never
folded into the new number. Any period containing an acquisition, a re-segmentation, a
pricing-model change or a definition change is flagged on the chart and, where material, shown
both as-reported and pro-forma.

---

## A3. Reconciliation to finance

| Line | CS pack | Finance | Variance | Note |
|---|---:|---:|---:|---|
| Beginning ARR | | | | |
| New | | | | |
| Expansion | | | | |
| Reactivation | | | | |
| Contraction | | | | |
| Churn | | | | |
| **Ending ARR** | | | **$0** | Must be $0 or this pack does not ship |

Reconciled by <name>, <date>, against <finance system> close of <date>.

---

## A4. Churn post-mortem (losses above the materiality threshold)

| Account | ARR | Segment | Tenure | Decision date | Effective date | Reason code | Controllable? | Health at −90d | Flagged? | Days of warning | Owner | What we learned |
|---|---:|---|---:|---|---|---|---|---|---|---:|---|---|

**Controllable vs uncontrollable split:** $<a> controllable / $<b> uncontrollable (<x>%).
Uncontrollable is limited to M&A consolidation, business failure and our own product sunsets;
every classification here is defensible on request.

---

## A5. Method notes

| Topic | Policy |
|---|---|
| Cohort construction | Membership frozen at t0. Churned members remain in the cohort at $0. Customers acquired after t0 never enter it |
| Win-back window | <30 / 60 / 90> days. Re-signs outside it are New, not never-churned |
| Reactivation | Bridge line only; excluded from cohort NRR/GRR |
| Contracted ramp | Tagged separately within expansion; not attributed to a CS or sales motion |
| Usage overage | <included / excluded> from the ARR base. Policy frozen since <date> |
| Currency | Constant currency at <rate date>, or FX shown as a separate bridge line |
| Small-n suppression | Cells with n < 20 accounts or < $2M ARR suppressed or asterisked |
| Cohort maturity | Immature cells greyed out; a cohort younger than the tenure column has no value there |
| Internal/test accounts | Excluded by rule: <state the rule> |
| Materiality threshold | $<threshold> — the greater of 1% of ARR or $250k |
| Frozen forecast snapshots | Written at T-90, T-60 and T-30, immutable thereafter |

---

## A6. Segment and ACV band definitions

| Segment | ACV boundary (dollars) | Accounts | ARR | Coverage model | Changed this period? |
|---|---|---:|---:|---|---|
| Enterprise | ≥ $<x> | | | | |
| Mid-Market | $<y>–$<x> | | | | |
| SMB | < $<y> | | | | |

Any re-segmentation during the period is flagged here and the affected slides show both the
old and new cuts. Segments are defined by **ACV band**, because ACV is the most predictive
segmentation variable for retention [M — SaaS Capital 2025; Benchmarkit 2025].
