# Renewal Risk Register — <Account or window> · <date>
**Internal.** Review weekly at the renewal stand-up. A row with no dated mitigation and no
named owner is not tracked, it is remembered — and remembering does not survive a holiday.

## Register

| # | Risk | Cause code | Signal family | ARR exposure | Band | First detected | Owner | Mitigation (dated) | Exit criteria | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | | | | $ | | | | | | open / closed / escalated |
| 2 | | | | $ | | | | | | |
| 3 | | | | $ | | | | | | |

**Total ARR exposure across open rows: $<X>. Rows with a dated mitigation and a named owner: <n>/<N>.**
A register where that ratio is below 100% is not a plan.

## Field rules

| Field | Rule |
| --- | --- |
| Cause code | One of the fixed list below. Free text destroys cross-account analysis |
| Signal family | One of the seven fixed families — the same taxonomy `churn-risk` uses |
| ARR exposure | Dollars at risk from **this row**, not the whole contract, unless the row genuinely threatens the whole contract |
| Band | Renewal outcome band if this risk is not mitigated: Very likely to renew · Likely · Uncertain · At risk · Very likely to churn absent intervention. Never a percentage without a cited backtest |
| First detected | The date the signal was observable, not the date someone noticed. The gap between the two is the number worth tracking |
| Mitigation | Action · owner · date. All three, or the row is not mitigated |
| Exit criteria | The observable event that closes the row. "Improved" is not an exit criterion |

## Cause codes

| Code | Meaning | Typical family | Usual owner |
| --- | --- | --- | --- |
| `value_not_evidenced` | No customer-validated outcome in 12 months | Sentiment & VoC | CSM |
| `champion_loss` | Champion departed, moved role, or stopped advocating | Relationship & engagement | CSM |
| `eb_absent` | Economic buyer unidentified or not contacted in 90 days | Relationship & engagement | CSM |
| `budget_cut` | Budget reduced, frozen, or reallocated | Firmographic & external | Renewal Manager |
| `competitive_displacement` | Named alternative under evaluation | Commercial & contract | Renewal Manager |
| `consolidation` | Vendor rationalisation or suite consolidation program | Firmographic & external | VP CS |
| `price_objection` | Uplift or absolute price contested | Commercial & contract | Renewal Manager |
| `product_gap` | Required capability we do not have and will not ship in time | Product usage & adoption | Product + CSM |
| `support_scar` | Unresolved escalation or SLA history shaping the decision | Support & reliability | Support lead |
| `adoption_shortfall` | Utilisation or breadth below the level that justifies the spend | Product usage & adoption | CSM |
| `m_and_a` | Acquisition, merger or restructure on the customer side | Firmographic & external | VP CS |
| `paper_stall` | A paper workstream cannot finish before `D` | Commercial & contract | Renewal Manager |
| `procurement_late` | Procurement entered inside T-30 | Commercial & contract | Deal desk |
| `security_review` | Security or vendor-risk re-review open or failing | Commercial & contract | Security lead |
| `entitlement_true_down` | Seats or consumption below contracted level | Billing & payment | Renewal Manager |
| `verbal_only` | Verbal agreement logged, no paper-movement event on record 14+ days later (C15) | Commercial & contract | Renewal Manager |
| `cold_commercial` | No commercial conversation with the EB or budget holder in 12 months; the renewal ask would be the year's first (C25) | Relationship & engagement | CSM |

## Worked rows

| # | Risk | Cause code | Family | ARR exposure | Band | First detected | Owner | Mitigation (dated) | Exit criteria | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Security re-review not started; measured lead time 30 days, 22 days remain to `D` | `paper_stall` | Commercial & contract | $480,000 | At risk | 2026-08-27 | R. Malhotra (Renewal Mgr) | Send the full security pack to their InfoSec lead by 2026-08-28; request parallel legal review the same day | Written security clearance received | open |
| 2 | CFO has not had a business conversation in 178 days; champion untested | `eb_absent` | Relationship & engagement | $480,000 | Uncertain | 2026-08-27 | J. Whitfield (CSM) | 30-minute business conversation with the CFO booked by 2026-09-10; champion asked to carry the business case by 2026-09-05 | Meeting logged with the CFO; champion confirms they raised it | open |
| 3 | Their platform team scoping an in-house replacement | `competitive_displacement` | Commercial & contract | $480,000 | Uncertain | 2026-07-14 | R. Malhotra | Switching-cost statement delivered to the VP Ops by 2026-09-04; total-cost comparison including their build and run cost | Customer confirms the build is not proceeding this cycle, in writing | open |
| 4 | Q1 API latency incident unresolved for the overnight window | `support_scar` | Support & reliability | $120,000 (partial — the overnight SKU) | Likely | 2026-03-11 | A. Ferreira (Support lead) | Fix committed 2026-09-30 with weekly status to the VP Ops | Fix shipped and confirmed stable by the customer for 14 days | open |

## Weekly review questions

1. Which rows moved band this week, and why — not who.
2. Which rows have a mitigation date that has passed?
3. Which rows have no named owner? (Assign on the call. Do not carry an unowned row.)
4. What is total open exposure, and how does it compare with last week?
5. Which rows should escalate under the trigger table in `renewal-prep` Step 9?
7. Which `verbal_only` rows are past 14 days — and what is the named paper-process ask that closes each?
6. Which rows can close — and what is the observable evidence that closes them?
