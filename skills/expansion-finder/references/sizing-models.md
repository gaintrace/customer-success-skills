# Expansion Sizing and Ranking Models

> Read this whenever you put a number on an expansion opportunity. Every model is worked end to
> end with real intermediate values, so a reviewer can audit the arithmetic rather than trust
> it. `../scripts/size_expansion.py` implements all of it — change the constants there and the
> tables here together.

**Contents**
1. [The universal sizing frame](#1-the-universal-sizing-frame)
2. [Three sizes: floor, base, ceiling](#2-three-sizes-floor-base-ceiling)
3. [Model A — Seat expansion](#3-model-a--seat-expansion)
4. [Model B — Tier upgrade on a metered plan](#4-model-b--tier-upgrade-on-a-metered-plan)
5. [Model C — Cross-sell with no usage history](#5-model-c--cross-sell-with-no-usage-history)
6. [Model D — Consumption commit](#6-model-d--consumption-commit)
7. [Discount and close-rate conventions](#7-discount-and-close-rate-conventions)
8. [The ranking model](#8-the-ranking-model)
9. [Timing fit and the opt-out deadline](#9-timing-fit-and-the-opt-out-deadline)
10. [Portfolio roll-up](#10-portfolio-roll-up)
11. [What invalidates a size](#11-what-invalidates-a-size)

---

## 1. The universal sizing frame

```
Effective unit price   p_eff = account.arr ÷ current contracted units
Opportunity ARR              = Δ units × p_eff × (1 − expected discount)     [seat, cross-sell]
                             = target tier ARR − current tier ARR            [tier upgrade]
                             = proposed commit ARR − current committed ARR    [consumption commit]

Ranked value = Opportunity ARR × propensity × timing fit × relationship readiness
                              × health gate × value factor
Throughput   = Ranked value ÷ estimated CSM hours to close
```

| Rule | Why |
| --- | --- |
| Use `p_eff`, not list price, for same-SKU volume | The customer already has a rate. Quoting list on an add-on starts a discount fight you did not need |
| Never size a cross-sell from list price alone | Anchor units to a countable customer-side quantity — people in the function, entities managed, transactions processed |
| Every input carries a provenance tag | `[Salesforce · Subscription.seats_purchased · 2026-08-26]`. A number without a source cannot survive the customer's own admin checking it |

---

## 2. Three sizes: floor, base, ceiling

Compute all three; present the middle one.

| Size | Definition | When it is the right answer |
| --- | --- | --- |
| **Floor** | Units that remove today's constraint — blocked users only | The customer is cost-constrained, or the buyer needs the smallest defensible ask to clear approval this cycle |
| **Base** | Projected units at the renewal date, from the trailing 3-month net-new slope | **The default.** Defensible from their own trend line |
| **Ceiling** | Base plus one quarter of forward growth, plus a buffer | Only when a second independent family corroborates the growth (headcount, a new workspace, a funded hiring plan) |

Recommending Ceiling on a single-family signal loses the deal to procurement scrutiny: they
rebuild your model, find the unsupported quarter, and discount the whole case.

---

## 3. Model A — Seat expansion

### 3.1 Inputs

| Input | Value | Source |
| --- | --- | --- |
| `subscription.seats_purchased` | 250 | Salesforce · Subscription.seat_count · 2026-08-26 |
| `account.arr` | $312,500 | Salesforce · Account.ARR · 2026-08-26 |
| `p_eff` | **$1,250/seat/yr** | 312,500 ÷ 250 |
| Active users, 30d | 236 | Amplitude · distinct actors with ≥1 core_action · through 2026-08-24 |
| Access-denied events, 60d | 41 events / **18 distinct blocked users** | Auth log · `seat_limit_reached` · 2026-06-26 → 2026-08-24 |
| Net new active users / month, trailing 3m | **+9** | Amplitude |
| Renewal date / notice period | 2027-01-24 / 60 days | Salesforce · Contract |
| **Opt-out deadline** | **2026-11-25 (90 days out)** | renewal_date − notice_period_days |
| List price at the 300+ seat tier | $1,150/seat | Price book v4 · 2026-07-01 |
| Health | Secure, TTFV verified, no open P1 | churn-risk 2026-08-26 |

### 3.2 Constraint and runway

```
Utilisation = 236 ÷ 250                    = 94.4%
Headroom    = 250 − 236                    = 14 seats
Runway      = 14 ÷ 9                       = 1.6 months
```

They exhaust the pool roughly **3.4 months before the renewal** — the independent urgency in
the conversation, true whether or not you sell anything.

### 3.3 Three sizes

```
Months to renewal = 150 ÷ 30.4             = 4.93
Floor    = 18 blocked users                                     → 18 seats
Base     = ceil(236 + 9 × 4.93) − 250 = ceil(280.4) − 250       → 31 seats
Ceiling  = ceil(236 + 9 × 7.93) − 250 = ceil(307.4) − 250       → 58 seats
```

**Recommend 31 (Base).** Move to 58 only if headcount growth or a new workspace corroborates the forward quarter.

### 3.4 Two commercial structures — present both

| Structure | Mechanics | Year-1 cash | ARR after | ARR delta |
| --- | --- | --- | --- | --- |
| **A. Mid-term add-on, co-termed at the current rate** | 31 × $1,250 × (5/12 remaining) = **$16,146** now; the renewal writes 281 seats at $1,250 | $16,146 | $351,250 | **+$38,750 (+12.4%)** |
| **B. Early renewal repriced to the 300-seat tier** | New 12-month term today at 300 × $1,150 = $345,000; term resets from today | $345,000 | $345,000 | **+$32,500 (+10.4%)** |

**Choose B** when the new seat count crosses a volume tier, you want to reset the term or
attach a multi-year with a capped escalator, and the customer values a lower unit-price
narrative. **Choose A** when the renewal is inside six months and the current effective rate
favours you. Never let them discover afterwards that B existed and was not offered.

### 3.5 Customer-side value case

```
Hours saved per active user per week   = 3.2      [their own value study, 2026-03, validated by VP Ops]
Loaded hourly cost                     = $62      [their figure, same study]
Working weeks per year                 = 46
Annual value per active user           = 3.2 × 62 × 46          = $9,126
Cost per seat                          = $1,250
ROI multiple                           = 9,126 ÷ 1,250          = 7.3×
Payback                                = (1,250 ÷ 9,126) × 12   = 1.6 months

Value blocked today (18 denied users)  = 18 × 9,126             = $164,268 / yr
Cost to unblock                        = 18 × 1,250             = $22,500 / yr
Net annualised value forgone           = $141,768
```

Every input above is **theirs**, dated, and attributed to a named person. If any is yours, the
case is a vendor estimate and must say so.

**The sentence that closes it:** *"Eighteen named people on your team were denied access 41
times in the last 60 days. At the productivity rate your own team validated in March, that is
about $164k of annualised value sitting behind a $22.5k line item — and separately, you exhaust
the pool in about six weeks regardless."*

### 3.6 Vendor-side ranking

```
Opportunity ARR   = $38,750
Propensity        = 0.55    (T2 constraint + 2 additional independent families)
Timing fit        = 0.90    (90 days to opt-out — proposal window)
Relationship      = 1.00    (exec sponsor met 21 days ago)
Health gate       = 1.00    (Secure)
Value factor      = 1.00    (validated outcome 34 days old)
Ranked value      = 38,750 × 0.55 × 0.90 × 1.00 × 1.00 × 1.00 = $19,181
Est. CSM hours    = 6
Throughput        = 19,181 ÷ 6 = $3,197 per CSM-hour
```

---

## 4. Model B — Tier upgrade on a metered plan

### 4.1 Inputs

| Input | Value |
| --- | --- |
| Current tier | $60,000/yr, includes 1.0M API calls/month |
| Current overage rate | $0.002 per call |
| Target tier | $96,000/yr, includes 5.0M calls/month |
| Target overage rate | $0.0012 per call |
| Current usage | 1.6M calls/month |
| Observed growth, trailing 6m | 12% month over month |
| Months left in term | 7.1 |

### 4.2 Compute the indifference point first

```
Tier delta            = 96,000 − 60,000            = $36,000 / yr = $3,000 / month
Overage equal to it   = 3,000 ÷ 0.002              = 1.5M calls / month
Indifference usage    = 1.0M included + 1.5M       = 2.5M calls / month
```

At today's 1.6M/month the honest answer is **stay on the current tier**. Say so out loud — that
sentence is what makes §4.3 land.

### 4.3 Trajectory crossing

```
Months to reach 2.5M at 12% MoM = ln(2.5 ÷ 1.6) ÷ ln(1.12) = 0.4463 ÷ 0.1133 = 3.9 months
```

They cross the indifference point in ~4 months, **inside the current term**. "Stay put" becomes
"upgrade now", and the reason is arithmetic rather than persuasion.

### 4.4 Twelve-month total cost

| Month | Usage (M) | Current-tier overage | Target-tier overage |
| --- | --- | --- | --- |
| 1 | 1.79 | $1,584 | $0 |
| 2 | 2.01 | $2,014 | $0 |
| 3 | 2.25 | $2,496 | $0 |
| 4 | 2.52 | $3,035 | $0 |
| 5 | 2.82 | $3,639 | $0 |
| 6 | 3.16 | $4,316 | $0 |
| 7 | 3.54 | $5,074 | $0 |
| 8 | 3.96 | $5,923 | $0 |
| 9 | 4.44 | $6,874 | $0 |
| 10 | 4.97 | $7,939 | $0 |
| 11 | 5.57 | $9,131 | $679 |
| 12 | 6.23 | $10,467 | $1,480 |
| **Total overage** | | **$62,493** | **$2,159** |

```
Current tier 12m total = 60,000 + 62,493 = $122,493
Target tier 12m total  = 96,000 +  2,159 =  $98,159
Customer saving        =                    $24,334  (19.9%)
```

### 4.5 The two-sided read

| Perspective | Effect |
| --- | --- |
| **Customer** | Saves $24,334 and gains budget predictability. A genuine win |
| **Vendor — billings** | Year-1 billings **fall $24,334**. A rep paid on billings will resist this deal |
| **Vendor — committed ARR** | $60,000 → $96,000: **+$36,000, +60%** |
| **Vendor — revenue quality** | $62,493 of volatile, disputable overage becomes contracted, forecastable ARR |
| **Vendor — risk** | Overage surprises are a leading cause of renewal escalations. Removing them protects GRR |

If your comp plan pays on billings rather than committed ARR, this correct recommendation is
punished by the plan. Name that in the internal artifact — a compensation problem, not a deal
problem, and it degrades expansion quality until it is fixed.

### 4.6 Guardrails

- Re-run monthly. If observed growth falls below the rate that crosses indifference inside the
  remaining term, **withdraw the recommendation in writing**.
- Offer a burst or true-forward clause instead of a tier jump when growth is spiky, not trending.
- Never model growth beyond the contract term in the customer-facing version.

---

## 5. Model C — Cross-sell with no usage history

```
Cross-sell ARR = list_price(SKU, size band) × (1 − expected discount) × attach_units

attach_units from ONE of:
  (a) peer cohort median attach ratio (units of SKU B per unit of SKU A), cohort n ≥ 20
  (b) the customer's own stated scope — headcount in the target function, entities to manage

P(attach) prior = base attach rate × association lift(A,B)      [cap 0.60 for a first-time SKU]
```

### 5.1 Worked

| Input | Value | Source |
| --- | --- | --- |
| SKU list price | $650 per managed entity per year | Price book v4 |
| Countable anchor | 60 entities in their Compliance function | Their org chart, confirmed by the champion 2026-08-14 |
| Expected discount | 20% (standard for a first attach at this band) | Discount policy |
| Cohort base attach rate | 0.31 | Own ownership matrix, n=44 accounts, same vertical ±1 ARR band |
| Association lift {A,B} → C | 2.1× | Market-basket rules, refreshed 2026-07 |

```
Gross ARR    = 650 × 60                 = $39,000
Net of 20%   = 39,000 × 0.80            = $31,200
P(attach)    = min(0.60, 0.31 × 2.1)    = 0.60  (capped)
Expected     = 31,200 × 0.60            = $18,720
```

**Never present a peer statistic that could identify a single customer**, and never build a
cohort under 20 accounts. "Of the 44 companies in your vertical and revenue band on our
platform, 31 run this alongside what you have" is earned. "Most customers your size buy this"
is a sales line.

### 5.2 Propensity vs uplift
A propensity model estimates `P(buy | X)` and over-prioritises accounts that would have
expanded anyway, spending CSM capacity on sure things. An uplift model estimates
`P(buy | contacted) − P(buy | not contacted)` and targets incremental revenue. With a year of
outcomes and any holdout discipline, rank on uplift; until then the §8 tier priors are the
honest approximation and must be labelled as priors.

---

## 6. Model D — Consumption commit

Converting recurring overage into committed volume is the least-understood expansion motion: it
usually *lowers* year-1 billings while raising committed ARR.

```
Committed ARR delta = proposed commit ARR − current committed ARR
Billings delta      = proposed commit ARR − (current committed ARR + trailing 12m overage)
Effective unit rate = proposed commit ARR ÷ committed units
Discount vs today   = 1 − (effective unit rate ÷ current effective rate)
```

### 6.1 Worked
| Input | Value |
| --- | --- |
| Current committed ARR | $96,000 |
| Trailing 12-month overage | $51,200 |
| Proposed commit | $138,000 |

```
Committed ARR delta = 138,000 − 96,000              = +$42,000 (+43.8%)
Billings delta      = 138,000 − (96,000 + 51,200)   = −$9,200
Customer: $9,200 cheaper than last year, no surprise line items
Vendor:   $51,200 of volatile revenue becomes contracted and forecastable
```

**Structure the commit with a true-forward, not a true-up.** A true-forward raises the commit
for the remaining term when consumption exceeds it; a true-up bills retroactively and is the
most reliable way to create a procurement escalation. Pair it with a capped escalator and an
explicit burst allowance.

---

## 7. Discount and close-rate conventions

Use your own numbers. These are placeholders, with the field that replaces each one.

| Convention | Placeholder | Replace with |
| --- | --- | --- |
| Discount on a same-SKU add-on | 0% — the customer already has a rate | Actual `p_eff`; deviations need deal-desk approval |
| Discount on a first-time SKU attach | Your published policy for the size band | Discount policy document |
| Volume tier break | Whatever the price book says | Price book version and date |
| Close rate by signal tier | The §8 priors | Your closed-won rate per tier, n ≥ 30 per motion |
| Cycle time by motion | 7–21d seat · 30–90d tier · 60–180d cross-sell · 90–270d consolidation | Median `opportunity.close_date − created_at` by `opportunity.type` |

Never present a discount without a named get: term length, a multi-year commit, a reference, a
case study, or an expansion attach. A give without a get is a price cut the next renewal will
treat as the new baseline.

---

## 8. The ranking model

```
Ranked value = Opportunity ARR × Propensity × Timing fit × Relationship readiness
                               × Health gate × Value factor
Throughput   = Ranked value ÷ estimated CSM hours to close
```

| Factor | Values | Source of the value |
| --- | --- | --- |
| **Propensity** | T1 0.60 · T2 0.45 · T3 0.30 · T4 0.20 · T5 0.12 · T6 0.10, plus 0.05 per additional independent family, cap 0.75 | Practitioner priors. Replace with observed win rates, n ≥ 30 per motion, and cite the sample |
| **Timing fit** | §9 table, computed from the opt-out deadline | Contract fields |
| **Relationship readiness** | 1.00 exec sponsor met ≤90d · 0.85 champion only · 0.70 buyer mapped but cold · 0.50 single-threaded | `interaction.customer_participants`, `contact.role` |
| **Health gate** | 1.00 Secure · 0.60 Watch · 0.00 At Risk and below, or any hard block | `churn-risk` band |
| **Value factor** | 1.00 if a customer-validated outcome is <120 days old · 0.70 otherwise, and the motion becomes value-first | `last_value_artifact_date` |

**Rank by Throughput, not by Opportunity ARR.** A $30k opportunity closable in 4 hours
($7,500/hr) outranks a $120k one needing 40 hours ($3,000/hr) unless capacity is idle.
Tie-break on higher Opportunity ARR, then the earlier opt-out deadline. Cap each CSM at **5–8
active expansion opportunities** — beyond that follow-through collapses (practitioner rule of
thumb, not measured).

---

## 9. Timing fit and the opt-out deadline

`opt_out_deadline = subscription.renewal_date − subscription.notice_period_days`.

| Days to opt-out | Fit | What is allowed |
| --- | --- | --- |
| >270 | 0.60 | Name the expansion attached to the next milestone. Do not price it |
| 150–270 | 0.85 | Whitespace refresh, value evidence assembled, ramp/discount pre-brief |
| 90–150 | **1.00** | Open the expansion conversation, separately from renewal terms |
| 45–90 | 0.90 | Proposal delivered; co-term decision made |
| 30–45 | 0.60 | Last window for a co-termed add-on |
| 0–30 | 0.20 | No new asks. Anything new here reads as pressure timed to the notice deadline |
| Past opt-out, pre-renewal | 0.30 | Terms are set. Hold |
| T+0 to T+60 post-renewal | 0.90 | The reset window — the "you're only asking because of the renewal" objection is gone |

**Co-term** when the deadline is inside 120 days, the motion is same-SKU volume, and no volume
tier break is crossed. **Run separately** when the deadline is >150 days out, the buyer differs,
a different SKU is involved, or the renewal carries any risk signal. **Wait** during any
cooldown in `qualification.md` §5.

---

## 10. Portfolio roll-up

For a book or segment, report all four lines. Reporting only the first is what makes an
expansion forecast miss.

| Line | Computation | What it is for |
| --- | --- | --- |
| **Gross expansion ARR identified** | Σ Opportunity ARR of qualified opportunities | The ceiling |
| **Risk-adjusted expansion ARR** | Σ Ranked value | What belongs in a forecast |
| **ARR withheld by the health gate** | Σ Opportunity ARR of refused candidates | Proof the gate ran, and the size of the adoption problem behind it |
| **Unsized** | Count and named missing fields | The instrumentation backlog |

Feed the risk-adjusted line into `renewal-forecast` as the expansion component of the ARR
bridge. Never the gross line — it gets treated as pipeline and then missed.

---

## 11. What invalidates a size

Re-run the model and, where the answer changes, **withdraw the recommendation in writing**.
Withdrawing a recommendation you can no longer support is the cheapest credibility available.

| Event | Effect on the size |
| --- | --- |
| Net-new-user velocity falls below the trailing 3-month rate | Base shrinks; recompute before the proposal is sent |
| Observed metered growth falls below the indifference-crossing rate | The tier recommendation becomes "stay". Say so |
| Blocked users turn out to be service accounts or external collaborators | Floor collapses; the T2 signal was false |
| Health band drops below Secure/Watch, or a Sev-1 or escalation opens | Gate or cooldown applies. The opportunity closes rather than pauses |
| Price book changes | Every list-price-based size is stale until re-run |
| The customer announces layoffs or a budget freeze | Hard block. Re-test in 90 days |
