# Benefit Arithmetic

> Every dollar in a value case comes from one of six formulas, and each formula forces one
> assumption you must state out loud. The arithmetic is not the hard part — stating the
> assumption is, because it is the thing a finance team will test.
>
> Evidence labels: `[M]` measured · `[V]` vendor-published · `[P]` practitioner convention ·
> `[A]` academic. Forrester's Total Economic Impact studies are commissioned by vendors; their
> *methodology definitions* are stable and widely used, and are cited here as `[V]` unless a
> specific published figure is being quoted.

**Contents**
- [1. The measurement chain](#1-the-measurement-chain)
- [2. Six benefit classes and how a CFO treats each](#2-six-benefit-classes-and-how-a-cfo-treats-each)
- [3. Time released](#3-time-released)
- [4. Cost avoided](#4-cost-avoided)
- [5. Error and rework reduction](#5-error-and-rework-reduction)
- [6. Revenue influenced](#6-revenue-influenced)
- [7. Risk exposure reduced](#7-risk-exposure-reduced)
- [8. Headcount avoided](#8-headcount-avoided)
- [9. Loaded cost, properly derived](#9-loaded-cost-properly-derived)
- [10. Haircuts and risk adjustment](#10-haircuts-and-risk-adjustment)
- [11. The double-counting map](#11-the-double-counting-map)
- [12. The cost side](#12-the-cost-side)
- [13. ROI, payback, NPV](#13-roi-payback-npv)
- [14. A full worked case](#14-a-full-worked-case)
- [15. Failure modes](#15-failure-modes)

---

## 1. The measurement chain

```
Product telemetry → Operational metric → Business metric → Financial metric → Their priority
(seats activated) → (tickets deflected) → (cost per ticket) → ($ cost avoided) → ("support cost
                                                                per shipment down 15%")
```

If you cannot draw an unbroken line from the chart to the right-hand column, the chart does not
belong in the value case. Every break in the chain is a place their CFO will stop reading.

Dave Jackson's definition is the most usable one available: measurable customer value is **how
much your product and enablement contributes to improving the KPIs of the key roles you serve**
`[P]`. Note the two constraints built into it — *contributes*, not causes, and *the KPIs of a
role*, not a metric your product happens to emit.

## 2. Six benefit classes and how a CFO treats each

| Class | Definition | CFO treatment | In the headline? |
| --- | --- | --- | --- |
| **Hard / cash-releasing** | Money that leaves the budget and does not come back — a retired contract, a cancelled requisition | Shows up in the P&L and in budget variance | **Yes, in full** |
| **Cost avoided** | A cost that would have been incurred and was not; protects margin without a budget line moving | Real, but invisible in year-on-year variance, so finance discounts it | Yes, **labelled and separated** |
| **Time released / productivity** | Hours returned to staff. Becomes cash only if redeployed or a hire is avoided | Credible only with an explicit recapture rate | Yes, **recapture-adjusted** |
| **Revenue influenced** | Revenue where your product is one of several causes | Requires an attribution factor set by the customer | Yes, **at the attributed figure, never gross** |
| **Risk / compliance** | Expected value of an avoided loss | Accepted where the probability has an evidence base **they** supplied | Only with their probability |
| **Soft / experience** | Satisfaction, morale, "fewer angry escalations" | Not creditable as cash | **No — separate panel** |

**The rule:** the headline contains hard + cost avoided + recapture-adjusted productivity +
attributed revenue. Soft benefits get a named, adjacent, un-monetised panel. Mixing them is the
fastest way to lose a CFO `[P]`.

## 3. Time released

```
Benefit = Users × Adoption% × Hours saved per user per period × Loaded hourly × Recapture%
```

| Input | Where it comes from | If you cannot source it |
| --- | --- | --- |
| `Users` | Their headcount in the named team, not licences sold | Use provisioned-and-active users and say so |
| `Adoption%` | Distinct active users ÷ users in the team, measured, 30-day window | `UNKNOWN` — and without it the line is not computable |
| `Hours saved per user` | Their time study, their estimate at the low end, or a before/after cycle-time measurement | `UNKNOWN — requires a timed comparison or an attested estimate` |
| `Loaded hourly` | Theirs. See §9 | Ours, stated as ours, which caps the band at Evidenced |
| `Recapture%` | Where the time went — a named redeployment or an avoided hire | Default 50%, stated as an assumption with its consequence |

**The recapture rate is the assumption this formula forces.** Released time is not cash until
somebody either does something else with it or is not hired. Forrester's TEI studies apply
**50% for general employees** and up to **75% for help-desk professionals** in the same study,
on the reasoning that the average employee uses about half of returned time productively `[V]`.
Use 50% as the default. Anything above 75% needs an explicit headcount-avoidance argument, and
at that point you should be computing §8 instead.

**Worked:**

```
26 users in the Claims team × 0.85 adoption × 1.4 hours/week × 46 working weeks
  = 1,423 hours released
1,423 × $68 loaded hourly (customer-supplied) = $96,764 gross
× 0.50 recapture                              = $48,382
× 0.70 attribution (α, set by their Controller) = $33,867
× 0.90 (10% haircut: two teams changed process independently in April)
                                              = $30,481 conservative
```

Note the order: recapture, then attribution, then haircut. Each is a separate, named,
challengeable step, which is exactly what makes the last number defensible.

## 4. Cost avoided

```
Cost avoided = (Baseline unit cost × Volume at today's scale) − Actual cost incurred
```

**The assumption this forces: volume at *today's* scale, not the baseline's.** The whole point
of a cost-avoidance claim is that the customer grew and their cost did not. If you apply the
baseline unit cost to the baseline volume you have computed nothing.

| Check | Why |
| --- | --- |
| Is the unit cost theirs? | A unit cost we estimated makes this a modelled figure, not an avoided cost |
| Does it include everything? | A "cost per ticket" that excludes tooling and supervision understates and will be corrected upward by them — which is the good direction to be wrong in |
| Is the volume growth real? | If their volume fell, this line is negative and you report it (`R20`) |

**Worked:** baseline $18.40 per Tier-1 ticket; volume grew from 96,000 to 141,000 tickets/year;
actual support cost this year $2.19M. `(18.40 × 141,000) − 2,190,000 = $404,400 avoided`, before
attribution.

## 5. Error and rework reduction

```
Benefit = Δ error rate × Volume × Cost per error
```

| Input | The trap |
| --- | --- |
| `Δ error rate` | Detection improved at the same time. If you also gave them better error visibility, the *found* error rate can rise while the *true* rate falls. Say which you are measuring |
| `Volume` | At today's scale, as in §4 |
| `Cost per error` | Theirs, and confirm whether it includes downstream rework, customer credits, and the investigation time — most first answers do not |

**Worked:** invoice exception rate fell from 3.1% to 1.4% on 74,000 invoices; their cost per
exception is $41 (their figure, includes the credit and the two-touch rework).
`0.017 × 74,000 × $41 = $51,578` gross.

## 6. Revenue influenced

```
Revenue influenced = Δ conversion × Opportunity volume × Average deal value × α
Cycle-time revenue = (Days saved ÷ 365) × Annual revenue on affected deals × α
Retention protected = Accounts retained above baseline × ARR per account × Gross margin %
```

**The assumption this forces: α, set by them.** Revenue has many parents. Report the gross
movement and the attributed movement side by side, always — a gross number presented alone
reads as a claim to have caused it.

**Retention protected is the line most often overstated.** Use gross margin, not revenue, and
use "above baseline" — retention that was already happening is not a benefit.

## 7. Risk exposure reduced

```
Expected value = Δ probability × Loss magnitude
```

**Both numbers come from the customer.** If they will not supply a probability, this line does
not exist — `R22`, and it is not negotiable. A vendor-supplied probability of a customer's own
risk event is a fabricated number wearing a decimal point.

Where the customer can supply it, this class is disproportionately powerful in regulated
verticals, because their risk function already maintains the figures and will recognise the
framing. Ask for their register, not for a guess.

## 8. Headcount avoided

```
Headcount avoided = (Δ volume ÷ baseline throughput per FTE) × fully loaded FTE cost
```

**The assumption this forces: the hire was actually planned.** A requisition that existed, with
a name, a budget line and an approval — not "they would have needed more people eventually".

| Evidence that makes this credible | Evidence that does not |
| --- | --- |
| A cancelled or unfilled req, named, with its budget | "The team would have grown" |
| A hiring plan the customer wrote before go-live | Our extrapolation of their headcount curve |
| Their finance lead confirming the line was removed | The manager's opinion |

When this line is real it is the strongest available, because it is cash-releasing. When it is
inferred, it is the weakest, because their HR data contradicts it in one query.

## 9. Loaded cost, properly derived

```
Loaded hourly = (base salary + benefits + payroll tax + allocated overhead) ÷ annual productive hours
```

| Input | Convention | Label |
| --- | --- | --- |
| Loaded multiplier over base salary | 1.25–1.40× | `[P]` |
| Annual productive hours | 1,880 (2,080 − PTO and holidays); 1,720 for heavy-meeting roles | `[P]` |
| Generic knowledge worker, fully burdened | $40/hour in Forrester's 2025 TEI of Glean | `[M]` as published in that study; it is **their** cohort, not yours |
| Help-desk professional, fully burdened | $80,000/year in the same study | `[M]`, same caveat |

**Order of preference:** their published rate → their finance team's figure on request → their
posted salary band × a stated multiplier ÷ stated hours → a published figure, labelled as a
proxy and haircut. Only the first two permit a **Measured** or **Attested** band. Presenting our
estimate of their labour cost as theirs is the same category of error as presenting a proxy as a
measurement.

## 10. Haircuts and risk adjustment

Volunteering conservatism buys credibility that cannot be bought any other way `[P]`. Apply a
haircut and **print the reason**, not just the percentage.

| Situation | Typical haircut | Reason to print |
| --- | --- | --- |
| Another programme touched the same teams | 10–25% | Name the programme and its dates |
| Adoption measured on a partial period | 10% | State the period covered |
| The metric definition changed mid-term | 15–25% | Name the change and the date |
| Estimates that will not be tracked forward | 10% | Forrester's TEI risk adjustment is applied downward for exactly this — the likelihood that estimates meet projections and the likelihood they are tracked over time `[V]` |
| A customer-supplied range | Use the low end instead of a haircut | Double-discounting looks like manipulation in the other direction |

Never apply an unexplained haircut. "We were conservative" is not a reason; "we removed 10%
because their knowledge-base rewrite ran across the same quarter" is.

## 11. The double-counting map

The commonest way a value case inflates is not a wrong number — it is the same benefit counted
twice under two names.

| Pair | The overlap | The fix |
| --- | --- | --- |
| Time released **and** headcount avoided | The avoided hire is the redeployment of the released time | Count one. If you count headcount avoided, set recapture to 0 on the same population |
| Cost avoided **and** error reduction | Fewer errors is often *why* the unit cost fell | Decompose the unit cost, or count the error line and drop it from the cost-avoided calculation |
| Revenue influenced **and** retention protected | A retained account that also expanded appears in both | Count expansion once, in whichever line the customer set α for |
| Time released across two teams | A hand-off saved once is often booked by both teams | Measure the end-to-end cycle, not each team's local saving |
| Cost avoided **and** tool retirement | The retired tool's licence often sits inside the baseline unit cost | List retired contracts separately and remove them from the unit cost |

**Test before roll-up:** for each pair of lines, ask "could the same hour, ticket, dollar or deal
appear in both?" If yes, decompose or drop one. Then print the exclusions.

## 12. The cost side

Omitting the customer's internal labour is the commonest credibility failure in a value case,
and it is the one their finance team spots first `[P]`.

| Component | Include | Source |
| --- | --- | --- |
| Subscription fees in the measurement window | Always | `invoice` / `subscription.arr` pro-rated to the window |
| Services, implementation, migration | Always | Statement of work; see `../../fde-scoping/SKILL.md` |
| Their internal project labour | Always | Their project hours × their loaded rate |
| Their ongoing admin labour | Always | The named admin's FTE fraction |
| Training and enablement time | Always | Attendee-hours × loaded rate |
| Integration and infrastructure | Always | Their engineering hours, plus any hosting or middleware |
| Our support and CSM cost | **Never** — this is our cost-to-serve, and it is internal-only (`R18`) | — |

Match the window: a 12-month benefit against 12 months of cost. A benefit annualised from one
good quarter, set against a full year of fees, is a number that inverts under scrutiny.

## 13. ROI, payback, NPV

Standard definitions, used because their finance team already uses them `[V]`:

```
ROI      = (Benefits − Costs) / Costs
Payback  = the point at which cumulative net benefit equals the initial investment
PV       = present value of discounted costs and benefits at the discount rate
NPV      = present value of discounted future net cash flows
```

| Convention | Value | Note |
| --- | --- | --- |
| Discount rate | 10% in Forrester TEI; organisations typically use 8–16% `[V]` | Ask their finance team for theirs — asking is itself a credibility move |
| Initial investment | Sits at time 0, undiscounted | Everything else discounts at year end |
| Multi-year cases | Only where the contract term supports it | Never project a benefit past the current term without saying so |

**Present payback in months.** It is the single most portable number in a value case, because it
survives being repeated by someone who did not read the workings.

## 14. A full worked case

**Northwind Logistics · FY26 (2025-10-01 → 2026-09-30) · as-of 2026-08-24**

| # | Benefit | Class | Baseline → current | Gross | Recapture | α (level) | Haircut | Conservative |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Tier-1 deflection | Cost avoided | 412 → 284 per 1,000 accounts | $404,400 | — | 0.70 (A1) | 10% | $254,772 |
| 2 | Claims cycle time | Time released | 9.0 → 5.5 days | $96,764 | 0.50 | 0.70 (A3) | 10% | $30,481 |
| 3 | Retired reconciliation tool | Hard | 1 contract | $34,000 | — | 1.00 — cash, no attribution needed | 0 | $34,000 |
| 4 | Invoice exceptions | Error reduction | 3.1% → 1.4% | $51,578 | — | 0.50 (A2) | 20% | $20,631 |
| | **Total conservative** | | | | | | | **$339,884** |

| Cost side | Amount |
| --- | --- |
| Subscription fees in window | $180,000 |
| Implementation services | $26,000 |
| Their internal project labour (410 h × $68) | $27,880 |
| Their admin (0.2 FTE × $92k loaded) | $18,400 |
| **Total** | **$252,280** |

```
Net benefit = 339,884 − 252,280 = $87,604
ROI         = 87,604 / 252,280  = 0.35 → 1.35× return
Payback     = 252,280 / (339,884 / 12) = 8.9 months
```

**Excluded from this figure:** their knowledge-base rewrite's independent contribution; two
integrations their engineering team built and maintains; any FY27 benefit; every soft benefit.

Note line 3: a retired contract is cash-releasing, needs no attribution factor, and is worth
more in a finance review than three times its value in productivity. Look for it first.

## 15. Failure modes

| Failure | Correction |
| --- | --- |
| Hours saved presented as dollars saved | Recapture rate, named redeployment, or do not monetise |
| Our loaded-cost estimate presented as theirs | Label it ours; the band caps at Evidenced |
| Benefit window and cost window differ | Match them, or annualise both and say so |
| The same saving counted in two lines | Run the double-counting map before roll-up |
| An unexplained haircut | Print the reason next to the percentage |
| Soft benefits inside the total | Separate panel, no dollar figure |
| A multi-year projection on a one-year contract | Report the current term; note the projection separately if at all |
| Cost-to-serve included in the customer's cost | That is our number and it is internal-only (`R18`) |
| Rounding a composite to the dollar | Two significant figures on any derived headline (`§4F`) |
| Risk-reduction expected value with our probability | Their probability or no line (`R22`) |
