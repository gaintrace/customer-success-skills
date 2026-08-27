# Coverage Model Charter — <Segment name>

> Emit one of these per segment, verbatim, filled. This is the internal document that makes the
> coverage model real: it is what Sales quotes from, what a new CSM reads in week one, and what
> settles the argument about whether an account is entitled to something.
>
> **Internal.** Contains cost-to-serve and coverage language that never reaches a customer.
> Anything a customer sees about a coverage change comes from `coverage-change-note.md`.
>
> Version <n> · effective <date> · next review <date, at most 2 quarters out> · owner <name, role>

---

## 1. Who is in this segment

| | |
|---|---|
| **Boundary rule** | `<expression over normalized-schema fields, e.g. account.arr >= 250000 AND account.is_internal = FALSE>` |
| Additional dimensions applied | `<potential / complexity / strategic / product mix — or "revenue only">` |
| Accounts | `<N>` |
| ARR | `$<X>` (`<Y>`% of base) |
| Mean ACV | `$<X>` · median `$<X>` |
| Mean complexity index | `<X.XX>` → multiplier `<X.XX>` |
| Exceptions held in this segment | `<N>` accounts, `$<X>` ARR — granted by `<name>`, expiring `<date>` |
| As of | `<date>` · source `<system>` |

**Migration rules.** Promoted in after `<two consecutive quarters above the boundary / a contract
event>`. Demoted out after `<two consecutive quarters below, no renewal inside 180 days, no open
escalation>`. **No coverage change inside an account's opt-out window.** No account changes segment
twice in twelve months.

## 2. What this segment receives

| Entitlement | Commitment | Owner | Delivery format |
|---|---|---|---|
| Named contact | `<named CSM / pooled queue / digital only>` | | |
| Executive business review | `<N>` per year | | |
| Operational cadence call | `<N>` per year | | |
| Success plan | Reviewed `<monthly / quarterly / semi-annually / automated>` | | |
| Renewal motion | Starts at T-`<N>` days from the **opt-out deadline**, not the renewal date | | |
| Support entry point | `<queue, SLA per request class>` | | |
| Escalation path | `<named ladder>` | | |
| Onboarding | `<N>` hours, `<owner>`, target time-to-first-value `<N>` days | | |

**What an account below this boundary stops receiving:** `<the specific list — a named CSM, live
business reviews, a human-owned renewal conversation. If this is hard to write, the boundary is not
funded.>`

## 3. What this costs

| | |
|---|---|
| Required hours per account per year | `<X.X>` (scheduled `<X>` + reactive `<X>` + onboarding amortised `<X>`) × complexity `<X.XX>` |
| Loaded cost per customer-facing hour | `$<c>` (OTE `$<x>` × loading `<f>` ÷ H `<h>`) |
| **Cost to serve, per account per year** | **`$<X>`** |
| **Cost to serve, % of mean ARR** | **`<X.X>`%** |
| Sanity bound | CS + Support median 9% of ARR across the whole base `[SaaS Capital 2026 Spending Benchmarks, survey Mar 2026, 1,000+ private B2B SaaS · M]` |
| Segment subscription gross margin | `<X>`% — coverage consumes `<Y>`% of it |

## 4. Capacity and staffing

| | |
|---|---|
| Effective customer hours per FTE per year (line H) | `<X>` — basis `<measured / [P] default>` |
| Sustainable accounts per CSM | `<X.X>` |
| Sustainable ARR per CSM | `$<X>` |
| Current accounts per CSM | `<X.X>` |
| **Required FTE / current FTE / gap** | `<X.X>` / `<X.X>` / **`<±X.X>`** |
| Sensitivity range on required FTE | `<low>` – `<high>`, driven by `<the two dominant inputs>` |
| Verdict | `<Servable / Tight / Oversubscribed / Structurally oversized>` |

**Ratios above are outputs of the capacity model, not benchmarks.** Derivation:
`../references/capacity-math.md`, run on `<date>` with `<measured / default>` inputs.

## 5. Book assignment rules

| # | Constraint | Target | Type | Current status |
|---|---|---|---|---|
| 1 | ARR balance | ±10% of segment mean | Soft | |
| 2 | Account count | ±10% | Soft | |
| 3 | Complexity load | ±15% on the index | Hard | |
| 4 | Renewal concentration | No month above 20% of a rep's renewing ARR | Hard | |
| 5 | Risk load | No rep above 2× mean at-risk ARR | Hard | |
| 6 | Continuity | ≥80% of accounts keep their CSM per cycle | Hard | |
| 7 | Vertical clustering | ≥60% within ≤3 verticals | Soft | |
| 8 | Timezone / language | 100% servable in the rep's hours | Hard | |
| 9 | Ramp state | New hire ≤40% of a steady book at month 3, ≤70% at month 6 | Hard | |

Move budget: `<N>` accounts per quarter maximum, `<Y>` hours at 8–12 hours per reassignment.

## 6. How this segment is measured

| Measure | Definition | Target | Cadence | Current |
|---|---|---|---|---|
| GRR | Segment gross revenue retention | | Quarterly | |
| NRR | Segment net revenue retention | | Quarterly | |
| Touch coverage | Accounts with a bilateral interaction in 90 days ÷ assigned | ≥70% | Monthly | |
| Entitlement delivery | Business reviews completed ÷ entitled, ARR-weighted, trailing 2 quarters | ≥85% | Quarterly | |
| Cost to serve | Fully loaded CS cost ÷ segment ARR | | Quarterly | |
| Uncovered ARR | ARR with no owner, or owned and untouched in 90 days | $0 unassigned | Monthly | |
| Inbound requests per account | Only for pooled and digital segments — the abandonment detector | Flat or rising | Monthly | |

## 7. What would change this charter

| Trigger | Action | Owner |
|---|---|---|
| Touch coverage below 70% for two consecutive months | Run the capacity model; open the headcount case | |
| Cost to serve above `<X>`% of segment ARR | Review the entitlement or the segment floor | |
| Required FTE exceeds available by more than 15% | Escalate with `../references/headcount-case.md` | |
| Mean complexity index moves by more than 0.3 | Re-derive book size; rebalance | |
| Segment population falls below 20 accounts or $2M ARR | Merge the segment or convert it to a named exception list | |
| An adjacent segment's hours come within 25% of this one | Re-run the differentiation test; merge if it fails | |

### Assumptions
| # | Assumption | Why it was needed | If wrong |
|---|---|---|---|
| 1 | | | |

### Coverage Ledger
| Signal family | What it supplied | Source | Status | Notes |
|---|---|---|---|---|
| Product usage & adoption | Onboarding load, activation state, complexity inputs | | ✅/⚠️/❌ | |
| Commercial & contract | ARR, ACV, boundaries, renewal and opt-out dates | | | |
| Relationship & engagement | Touch coverage; hours actually spent per account | | | |
| Support & reliability | Ticket and escalation load — the reactive hours | | | |
| Sentiment & VoC | Whether this model is landing for this segment | | | |
| Billing & payment | Collections and payment-failure load | | | |
| Firmographic & external | Headcount, whitespace, vertical, timezone, language | | | |

**Coverage: X / 7 (Y%) → confidence capped at `<level>`.** Blind spots: `<what the gaps hide.>`
