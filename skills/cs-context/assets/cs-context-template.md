# CS Context — <Company Name>

```yaml
last_reviewed: YYYY-MM-DD
reviewed_by: <name>
next_review: YYYY-MM-DD
schema_version: 1.0
```

> Every skill in the customer-success skill library reads this file before doing anything.
> Fields marked `UNKNOWN — requires X` are honest gaps, not placeholders to be guessed at.
> Delete nothing; a missing field is itself a finding.

---

## 1. Company & Product

| Field | Value |
| --- | --- |
| Company | |
| What the product does (one sentence) | |
| Buyer persona | |
| User persona | |
| Products / SKUs | |
| Deployment model | SaaS multi-tenant / single-tenant / on-prem / hybrid |
| Go-to-market motion | PLG / sales-led / hybrid / partner-led |

## 2. Commercial Model

| Field | Value |
| --- | --- |
| Contract terms offered | monthly / annual / multi-year |
| % of ARR on annual+ terms | |
| Pricing basis | per-seat / usage / tiered flat / hybrid |
| Metered unit (if usage-based) | |
| Auto-renew default | yes / no |
| **Notice period (days)** | |
| **Opt-out deadline rule** | `renewal_date − notice_period_days` |
| Standard renewal uplift | |
| Typical ACV by segment | |
| Discounting norms | |
| Payment terms | |

## 3. Segments & Coverage

| Segment | ARR boundary | # accounts | ARR | Coverage model | Accounts / CSM | ARR / CSM |
| --- | --- | --- | --- | --- | --- | --- |
| Enterprise | ≥ $ | | | named CSM | | |
| Mid-Market | $ – $ | | | named / pooled | | |
| SMB | < $ | | | tech-touch | | |

## 4. Ownership

| Motion | Owner | Escalation path |
| --- | --- | --- |
| Renewal | | |
| Expansion / upsell | | |
| Onboarding | | |
| Technical escalation | | |
| Executive sponsor programme | | |

## 5. Success Definition

| Field | Value |
| --- | --- |
| **Activation event** (the action that predicts retention) | |
| Time-to-first-value target | |
| Time-to-full-value target | |
| Core outcomes customers buy | |
| How the customer measures ROI | |
| Baseline capture process | |

## 6. Health Model in Use

| Dimension | Inputs | Weight | Thresholds | Trusted by the team? |
| --- | --- | --- | --- | --- |
| | | | | |

Overall trust level: `high / medium / low / none — score is ignored in practice`

## 7. Retention Baseline

| Metric | Value | Window | Source |
| --- | --- | --- | --- |
| GRR | | | |
| NRR | | | |
| Logo retention | | | |
| Gross ARR churn | | | |
| Expansion rate | | | |
| Contraction rate | | | |
| Renewal forecast accuracy | | | |

## 8. Top Churn Reasons — last 12 months, ranked by ARR lost

| Rank | Reason | ARR lost | # logos | Savable? |
| --- | --- | --- | --- | --- |
| 1 | | | | |

## 9. Source Inventory

| Family | System | Connected | Access method | Latency | History | Account key | Data as of |
| --- | --- | --- | --- | --- | --- | --- | --- |
| CRM | | | | | | | |
| Billing | | | | | | | |
| Support | | | | | | | |
| Engineering | | | | | | | |
| Product analytics | | | | | | | |
| Warehouse | | | | | | | |
| Communication | | | | | | | |
| Conversation intelligence | | | | | | | |
| Scheduling | | | | | | | |
| Survey / VoC | | | | | | | |
| CS platform | | | | | | | |
| External / firmographic | | | | | | | |

*Data as of* is the date the export was taken or the source last synced. A source with no
as-of date is `UNKNOWN — requires whoever ran the export`, not a blank.

## 10. Identity Resolution

**Rule:**

**Join rate:** __% of product users resolve to a CRM account

**Known exceptions:**
- Free-email users:
- Multi-domain accounts:
- Agencies / external collaborators:
- Subsidiaries:
- Internal / test accounts (exclusion rule):
- Shared service accounts:

## 11. Data Quality Findings

| Check | Result | Detail | Downstream impact |
| --- | --- | --- | --- |
| Freshness | ✅/⚠️/❌ | | |
| Account coverage | | | |
| Identity join rate | | | |
| Duplicates | | | |
| Test/internal exclusion | | | |
| Currency | | | |
| History depth | | | |
| Churn labels (decision date, reason) | | | |

## 12. Coverage Ledger

| Signal family | Source | Status | Notes |
| --- | --- | --- | --- |
| Product usage & adoption | | | |
| Commercial & contract | | | |
| Support & reliability | | | |
| Relationship & engagement | | | |
| Sentiment & VoC | | | |
| Billing & payment | | | |
| Firmographic & external | | | |

**Coverage: _ / 7 families (__%) → maximum downstream confidence: ____**

Blind spots and what they typically hide:

## 13. Calendar

| Item | Value |
| --- | --- |
| Fiscal year start | |
| QBR cadence, by segment | |
| Renewal forecast call | |
| Board reporting cadence | |
| Seasonal patterns (budget freezes, industry cycles) | |

## 14. Glossary Overrides

Terms this company uses differently from the library defaults.

| Term | Library default | This company's meaning |
| --- | --- | --- |

## 15. Assumptions

Every default this file was built on, and what changes if it turns out to be wrong. An empty
table is a valid state — it means nothing was assumed. "May affect results" is not a
consequence; name the field, the section or the decision that moves.

| # | Assumption | Why it was needed | If wrong |
| --- | --- | --- | --- |
| 1 | | | |
