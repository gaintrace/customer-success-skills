# Qualification, the Health Gate, and Refusal

> Read this when deciding whether a signal is an opportunity. Most expansion programs fail not
> because they miss signals but because they act on all of them. This file is the filter.

**Contents**
1. [The difference between a signal and an opportunity](#1-the-difference-between-a-signal-and-an-opportunity)
2. [The health gate](#2-the-health-gate)
3. [The five qualification gates](#3-the-five-qualification-gates)
4. [Disqualifiers](#4-disqualifiers)
5. [Cooldowns and cadence caps](#5-cooldowns-and-cadence-caps)
6. [How to refuse](#6-how-to-refuse)
7. [The trust-damage anti-pattern register](#7-the-trust-damage-anti-pattern-register)
8. [The CSQL record](#8-the-csql-record)
9. [Queue design and SLAs](#9-queue-design-and-slas)
10. [Measuring the program itself](#10-measuring-the-program-itself)

---

## 1. The difference between a signal and an opportunity

| A signal is… | An opportunity is… |
| --- | --- |
| An observation with a threshold | A signal that survived the health gate and five qualification gates |
| Owned by the data | Owned by a named person, with a date |
| Sized as a range | Sized as three numbers with the middle one recommended |
| Worth a look | Worth CSM hours you could have spent on a renewal |

The test: **could you write down what the customer loses each month by not doing this, in
their own units, and name the person on their side who feels it?** If not, it is a signal.

---

## 2. The health gate

Expansion is never recommended on an account below the health floor. The floor is **Secure or
Watch** on the `churn-risk` band scale (score ≤ 44).

| Band | Gate | What runs instead |
| --- | --- | --- |
| Secure (0–24) | 1.00 | Full expansion motion |
| Watch (25–44) | 0.60 | Adoption-recovery play first; re-test the signal in 45 days |
| At Risk (45–64) | **0.00** | `churn-risk` → `save-play`. No expansion artifact is produced |
| High Risk (65–84) | **0.00** | `save-play`, executive escalation |
| Critical (85–100) | **0.00** | `save-play`. A commercial ask here is extraction |

### 2.1 Hard blocks — the gate is 0.00 regardless of band

| Block | Field / check | Why it is absolute |
| --- | --- | --- |
| Implementation not live | Project `go_live_date IS NULL` | Selling before go-live signals you are transactional before value exists |
| TTFV not reached | Milestone `ttfv_achieved = false` | No proof of value means no basis for a business case |
| Open P1 / Sev-1, or one closed inside 14 days | `ticket.priority='urgent'`, `ticket.resolved_at` | Service-recovery memory dominates every other impression |
| Active escalation or executive complaint | `ticket.type='escalation' AND status<>'closed'` | You are spending trust, not banking it |
| NPS detractor (0–6) in the buying centre inside 90 days | `contact.sentiment='negative'`, response date | Someone with influence has already told you no |
| Invoice past due >30 days, or an open dispute | `invoice.status IN ('overdue','disputed')` | The last invoice is unresolved; a bigger one is not the answer |
| Seat utilisation <50% | `usage_daily.active_users` ÷ `subscription.seats_purchased` | Their own SaaS-management tool already flags this as shelfware |
| Open downgrade conversation | `opportunity.type` with a reduction request | They asked to reduce. Asking to increase reads as not listening |
| Customer reorg, layoffs, or announced budget freeze | Enrichment / news / account notes | Nothing you propose survives contact with a frozen budget |
| Already entitled and unused | `subscription.plan` vs actual feature use | Pitching what they already pay for destroys the admin's confidence in you |

### 2.2 Soft gates — proceed with a modified motion

| Condition | Modification |
| --- | --- |
| Health = Watch | Adoption play first; re-test the signal in 45 days |
| No mapped economic buyer | Multithread first — the ask cannot land on a user-level contact |
| No exec sponsor met in 90 days | Sponsor re-contact before the ask; relationship readiness 0.70 |
| Last value conversation >120 days ago | Value factor 0.70 and the motion becomes value-first |
| Ticket volume in the top decile of the cohort | Investigate the root cause first — high volume is adoption *or* dysfunction |
| Champion recently departed | Re-multithread within 48 hours; hold the ask until a new sponsor is named |

### 2.3 The one exception: a genuinely different business unit

All three must be evidenced in writing, inside the artifact. Two of three is not enough.

| Condition | Acceptable evidence | Not acceptable |
| --- | --- | --- |
| Separate budget holder | A named `economic_buyer` outside the failing unit's reporting chain, with a contact date | "Different team" |
| Separate contracting or product boundary | Own workspace/tenant, own `subscription` row, a `parent_account_id` child, or a distinct legal entity | Same workspace, different folder |
| No shared root cause | The failing unit's issue (defect, broken integration, pricing dispute) does not touch the new unit's use case, stated explicitly | "The escalation is unrelated" with no reasoning |

When the exception is used, the artifact must also name **who is fixing the failing unit's
problem, and by when**. Expanding into unit B while unit A burns, with nobody assigned to
unit A, is how a $30k attach costs a $480k renewal.

### 2.4 The gate must actually block things

Track **health-gate block rate = blocked candidates ÷ signals fired**. A rate near 0% means
the gate is not running or the thresholds are wrong, not that your base is uniformly healthy.

---

## 3. The five qualification gates

All five pass, or it is not an opportunity. Print each with its evidence, and print failures
with what fixes them, who owns the fix, and by when.

| # | Gate | Passes when | Fails when |
| --- | --- | --- | --- |
| 1 | **The constraint is countable** | Named blocked users, measured units over allotment, a specific `feature_key` attempted, a specific entity count | The evidence is a percentage or a trend line with no countable unit behind it |
| 2 | **Someone on their side feels it** | A named person raised it, was blocked, or owns the affected workflow | You inferred the pain from telemetry and nobody has mentioned it |
| 3 | **A mapped economic buyer** | `contact.role='economic_buyer'` with a contact date inside 90 days, or a named introduction path with a named introducer and a date | The only contact is a user or an admin with no budget |
| 4 | **Value already proven** | A customer-validated outcome — their baseline, their number, their attribution — dated within 120 days | Value is asserted by you, undated, or older than 120 days |
| 5 | **A budget path exists** | Named approver, budget cycle timing, and the source of funds (existing line, new request, reallocation) | "They'll find the money" |

Gate 4 is the one most often waved through, and it is the one that determines whether the
conversation is a business case or a price negotiation.

---

## 4. Disqualifiers

These close the candidate. Do not nurture, do not re-queue on a timer — close it with the
reason, and let a genuinely new signal re-open it.

| Disqualifier | The test | Why it is fatal |
| --- | --- | --- |
| Seat utilisation <50% | Active users ÷ seats purchased | You are asking them to buy more of something they are not using |
| Already entitled and unused | `subscription.plan` includes the capability; feature usage = 0 | The correct action is enablement, and pitching it as new is a credibility event |
| Only T5/T6 signals fired | No T1/T2/T3, and fewer than two independent T4 | Disposition and exogenous news are not demand |
| The blocked "users" are not people | Service accounts, sandbox, internal test, external collaborators | The Floor size collapses and the T2 signal was never real |
| Declined inside 12 months with no new evidence | `opportunity.loss_reason` on the same SKU | Re-pitching a "no" without new evidence tells them you were not listening |
| The indifference math says stay | §4 of `sizing-models.md` | Recommending an upgrade the customer's own arithmetic contradicts is discovered exactly once |
| No introduction path to a budget holder | Gate 3 fails and there is no named introducer | The champion becomes an unpaid internal seller and resents it |
| The signal has decayed | Older than the window in `expansion-signals.md` §9 | A 60-day-old feature-gate hit means they already built the workaround |
| Cross-sell while SKU A adoption is <60% breadth | `usage_daily.feature_breadth` on the owned SKU | Compounding shelfware sets up a single consolidated churn event later |
| The account is inside its onboarding blackout | Contract start → verified TTFV | Nothing has been proven; there is nothing to expand from |

---

## 5. Cooldowns and cadence caps

Practitioner conventions, not measured benchmarks. Adopt them, or set your own and write them
down — the failure mode is having none.

| Rule | Window |
| --- | --- |
| After a Sev-1 resolution, before any commercial ask | 14 days minimum |
| After an escalation closes | 30 days |
| After an advocacy, reference, or review ask | 14 days |
| Between distinct expansion asks to the same buyer | 90 days |
| Maximum expansion asks per account per year | 2, excluding customer-initiated |
| After a price increase takes effect | 90 days |
| Onboarding blackout | Contract start → verified TTFV |
| **Momentum window — act, do not wait** | Within 14 days of a verified milestone, a delivered outcome report, a new team's go-live, or a promoter response from a buyer |

---

## 6. How to refuse

Refusing is a deliverable, not a failure to deliver. A good refusal has five parts and takes
one paragraph.

1. **The decision**, stated first.
2. **The blocking condition with its evidence and date.**
3. **The economics of the refusal** — what the ask would have been worth against what it puts
   at risk.
4. **What is available instead**, with an owner and a date.
5. **The re-test condition** — what must be true, and when you will look again.

> Not recommending an expansion motion on Helios Health. The account is At Risk (58/100) with
> an executive escalation open since 2026-08-04 [Zendesk · #51203 · status=open · 23 days] and
> an SLA breach on 2026-08-11. The cross-sell would have been worth $31,200 gross / $18,720
> expected; the renewal it would put at risk is $480,000 with an opt-out deadline on
> 2026-08-17. Available instead: the escalation close-out plan — owner Priya Raman, resolution
> committed by 2026-09-12, success measure = ticket closed with a CSAT response ≥4. Re-test the
> cross-sell signal on 2026-10-12, thirty days after closure. If the Manufacturing division is
> a genuinely separate business unit, name its economic buyer and its workspace and I will
> re-run the gate against that unit alone.

**When the user pushes back**, do not soften the gate — restate the arithmetic. The refusal is
defensible because the numbers are on the page: an $18,720 expected value against $480,000 of
exposure is a 26:1 ratio against the ask.

---

## 7. The trust-damage anti-pattern register

| Anti-pattern | What it looks like | The damage | The correct move |
| --- | --- | --- | --- |
| **Quota-driven expansion** | Expansion targets set like new-business quota, with no reference to installed-base readiness | Customers stop reading your emails and skip meetings — including the genuinely helpful ones. This is Lincoln Murphy's documented failure mode | Forecast expansion bottom-up from milestone cohorts, not top-down from a quota |
| **Upselling before value** | Any ask before verified TTFV | You are transactional before you were useful | Hard block until TTFV |
| **Upselling into an escalation** | "While I have you…" after a Sev-1 | Converts service recovery into extraction | 14-day post-Sev-1 and 30-day post-escalation cooldowns |
| **Upselling the wrong stakeholder** | Selling a new department's seats to the original champion | The champion becomes an unpaid internal seller with no budget and resents it | Get introduced to the new unit's owner |
| **Selling what they already own** | Proposing a capability included in their current plan and never adopted | The admin concludes you do not know their account | Check entitlement before proposing any SKU |
| **True-up ambush** | The first they hear of over-consumption is the invoice | Procurement escalation; the trust cost exceeds the recovery | Disclose within 5 business days of detection, with the value it produced |
| **Selling the seat, not the outcome** | "You're at 96% utilisation, let's add 40 seats" | Reads as meter reading | "Eighteen named people were blocked from the workflow last month; here is what that cost you" |
| **Pricing-page stalking** | "I saw you visiting our pricing page" | Damages trust in your telemetry generally | Use the signal to *time* the outreach, never to justify it aloud |
| **Advocacy and ask in one breath** | Reference request and upsell in the same meeting | Retroactively makes the advocacy ask feel transactional | Separate by ≥14 days |
| **Ignoring the honest downgrade** | Recommending a tier upgrade when the math says stay | One discovered instance destroys every future recommendation | Run the indifference math and say "stay" when it says stay |
| **Cross-selling onto shelfware** | Selling SKU B at 45% adoption of SKU A | Sets up a single consolidated churn event later | Require the breadth threshold on SKU A first |
| **The ask inside the notice window** | A new proposal 20 days before the opt-out deadline | Reads as pressure timed to the deadline; endangers the renewal | Defer to the post-renewal reset window |

---

## 8. The CSQL record

A Customer Success Qualified Lead without linked signal records is an opinion. Minimum viable
schema for the CS → Sales handoff:

| Field | Type | Why it is mandatory |
| --- | --- | --- |
| `csql_id`, `account_id` | id, ref | — |
| `signal_ids[]` | array | The evidence. Without it this is a hunch with a dollar figure |
| `signal_tier` | T1–T6 | Drives the queue and the SLA |
| `motion_type` | seat / tier / cross_sell / commit | Drives the owner |
| `opportunity_arr_floor` / `_base` / `_ceiling` | currency ×3 | Forces the three-size discipline |
| `health_band`, `health_gate_passed` | enum, bool + reason | Auditable proof the gate ran |
| `economic_buyer_contact_id` | ref | Null → relationship readiness 0.70 |
| `value_evidence_url`, `value_evidence_date` | url, date | Link to the value artifact delivered **before** the ask |
| `opt_out_deadline`, `days_to_opt_out` | date, int | Timing fit |
| `csm_hours_estimate` | int | Throughput ranking |
| `created_at` / `accepted_at` / `closed_at` | ts ×3 | Cycle time and accept rate |
| `disposition` | accepted / rejected+reason / won / lost+reason | Closes the learning loop |

---

## 9. Queue design and SLAs

| Queue | Entry criteria | SLA | Owner |
| --- | --- | --- | --- |
| **Declared (T1)** | Any explicit-demand signal — C1, C3, S1, S2, C12, C13, F6 residency request | Contact within 1 business day | CSM, or AE above the ARR threshold |
| **Blocked (T2)** | U2, U3, U7, U8, U15, S3, B1 | Contact within 5 business days | CSM |
| **Trajectory (T3)** | U1, U5, U6, B2, B3 | Included in the next scheduled touch; opportunity opened at 45 days to breach | CSM |
| **Structural (T4)** | U9–U14, U16, U17, R2, R3, C7–C11 | Investigate within 21 days | CSM |
| **Portfolio (whitespace)** | C4, C5, C6 | Reviewed quarterly, delivered at business reviews | CSM + AE |
| **Exogenous (T6)** | F1–F7 | Reviewed weekly; F4/F5 and R4 within 48 hours | CSM + AE |

SLAs are practitioner conventions. Set your own if you have cycle-time data, but publish them —
an unpublished SLA is not a queue, it is a list.

---

## 10. Measuring the program itself

| Metric | Formula | What a bad number means |
| --- | --- | --- |
| Signal → CSQL conversion | CSQLs created ÷ signals fired | Above ~50% means the thresholds are too loose and CSM time is being spent on noise |
| CSQL accept rate | Accepted ÷ created | Below ~70% means the qualification criteria are wrong, not that the reps are wrong |
| CSQL → closed-won, by signal tier | Won ÷ created | If T5/T6-only opportunities win at the same rate as T1/T2, the tiering is not predictive — rebuild it |
| Expansion cycle time by motion | `closed_at − created_at` | Compare to the motion catalogue in `expansion-signals.md` §10 |
| Expansion CAC ratio | Loaded expansion cost ÷ expansion ARR won | Compare against the measured median of **$1.00** (Benchmarkit/Pavilion 2025, FY2024 data) versus **$2.00** for new-customer ARR |
| Expansion ARR % of new ARR | Expansion ÷ (new logo + expansion) | Compare against **40%** median, **58%** at $50–100M ARR (Benchmarkit 2025), and ~**60%** above $50M (High Alpha 2025, 800+ respondents) |
| NRR | See `renewal-forecast` | SaaS Capital 2025 by ACV band: <$5k **95%** · $5–25k **98%** · $25–50k **102%** · $50–100k **107%** · $100k+ **110%**. Bessemer 2023 tiering: 100% good / 110% better / 120% best |
| Health-gate block rate | Blocked ÷ signals fired | Near 0% means the gate is not running |
| Post-expansion 12-month retention | GRR of accounts that expanded vs those that did not | **The single most important diagnostic here.** If expanded accounts retain worse, you are selling prematurely |
| Downgrade rate on expanded accounts | Downgrade ARR ÷ expansion ARR, trailing 12m | Rising means over-selling |

Report the last two every quarter whether or not anyone asks. They are the only two numbers
that tell you whether the expansion program is building revenue or borrowing it from next year.
