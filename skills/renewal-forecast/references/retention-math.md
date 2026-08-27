# Retention Math — denominators, the ATR base, the bridge, and every edge case

> Read this when building the ARR bridge, computing GRR or NRR, hitting any case where the
> formula is ambiguous, drawing cohort curves, or computing concentration.
>
> Most retention arguments are not disagreements about the business. They are two people using
> two different denominators and neither one saying which.

**Contents**
- [1. The two denominators](#1-the-two-denominators)
- [2. Building the ATR base, and the three errors that flatter it](#2-building-the-atr-base-and-the-three-errors-that-flatter-it)
- [3. Uplift, escalators and expansion at renewal](#3-uplift-escalators-and-expansion-at-renewal)
- [4. The ARR bridge, line by line](#4-the-arr-bridge-line-by-line)
- [5. Reconciling the ATR and cohort methods in dollars](#5-reconciling-the-atr-and-cohort-methods-in-dollars)
- [6. Twenty edge cases, worked](#6-twenty-edge-cases-worked)
- [7. Cohort curves, and why a single-period NRR hides everything](#7-cohort-curves-and-why-a-single-period-nrr-hides-everything)
- [8. Concentration math](#8-concentration-math)

---

## 1. The two denominators

| | **ATR / renewal-event method** | **Cohort / period method** |
| --- | --- | --- |
| Denominator | ARR of contracts whose decision point falls in the period | ARR of the customer cohort at period start |
| Question it answers | "Of what came up for renewal, how much did we keep?" | "Of what we had, how much did we still have?" |
| Sees mid-term contraction | **No** — a contract that shrank in month 4 never reached a renewal event | **Yes** |
| Sees mid-term cancellation | No | Yes |
| Denominator moves with term length | Yes — a book on 3-year terms has one third the annual ATR | No |
| Audience | Renewal team, forecast accuracy, capacity planning | Board, investors, CFO, cohort analysis |
| Cap | Gross renewal rate caps at 100% by construction (uplift excluded) | GRR caps at 100% by construction |

Both are legitimate. Reporting one and labelling it the other is not, and it is the single most
common error in a retention deck. Declare the method beside every number:
`GRR 88.4% (cohort, FY26 Q3)` · `gross renewal rate 94.1% (ATR, FY26 Q3, n=61 events)`.

**Formulas.**

```
Cohort method (board / investor):
  GRR = (Opening ARR − Contraction − Churn) / Opening ARR
  NRR = (Opening ARR + Expansion + Cross-sell − Contraction − Churn) / Opening ARR

ATR method (renewal team):
  Gross renewal rate = Σ retained ARR (capped at ATR, uplift excluded) / Σ ATR
  Net renewal rate   = Σ (retained + uplift + expansion at renewal)     / Σ ATR

Logo retention = logos retained / logos that reached a decision point
```

Publish logo retention beside dollar retention, always. The same 85% logo retention produces very
different dollar outcomes depending on whether the lost logos were small or one of them was 12% of
the book — and only the pair tells you which happened.

## 2. Building the ATR base, and the three errors that flatter it

**ATR is the run-rate ARR the customer was paying entering the decision.** Set it from
`subscription.arr` as of `opt_out_deadline − 1`. Not the original order form. Not the quoted renewal.

### Error 1 — ATR taken from the original order form

A customer signs at $100k. In month 7 they add $40k of seats, co-termed into the same contract.
They renew at $140k.

| | ATR | Retained | Rate | Reads as |
| --- | --- | --- | --- | --- |
| Wrong (order form) | $100,000 | $140,000 | **140%** | A blowout expansion quarter |
| Right (run-rate at opt-out) | $140,000 | $140,000 | **100%** | A flat renewal, which is what happened |

The $40k was already booked as expansion in month 7. Counting it again at renewal books the same
dollar twice, and it is why some books show a net renewal rate that finance cannot reconcile.

### Error 2 — contractual uplift left in the denominator

A $200k contract with a 5% annual escalator renews at $210k with no other change.

- Gross renewal rate uses ATR $200,000 and retained **$200,000** → 100%. The escalator is excluded.
- Net renewal rate uses ATR $200,000 and $210,000 → 105%. The $10k appears on the **price uplift**
  bridge line, tagged as expansion.

Putting the $210k in both numerator and denominator (ATR $210k) produces 100% and quietly deletes
$10k of expansion from the bridge. Putting $210k over $200k in the *gross* rate manufactures 105%
gross retention, which is impossible by construction and immediately discredits the deck.

### Error 3 — annual opt-outs on a multi-year counted as one event

A 3-year contract with an annual opt-out is **three renewal events**, one per anniversary. Counted
as one event at year 3, two decision points vanish from ATR — and with them, two chances to churn.

| Contract shape | Renewal events | ATR in a given year |
| --- | --- | --- |
| 1-year, auto-renew, 60-day notice | 1 per year | Full ARR |
| 3-year, annual opt-out | 3, one per anniversary | Full ARR each year |
| 3-year, no decision point until end | 1, at month 36 | **$0** in years 1 and 2 |
| Evergreen / no term | 0 | $0 — use the cohort method for these accounts |

### Membership rules

| Include in ATR | Exclude from ATR |
| --- | --- |
| Every contract whose `renewal_date` falls in the period | Contracts already cancelled mid-term (booked as churn when it happened) |
| Every annual opt-out anniversary of a multi-year | Multi-year with no decision point in the period (`ATR = $0`) |
| Auto-renew contracts whose notice window opens in the period | Pay-as-you-go with no contract — no renewal event |
| Mid-term upsells co-termed into the contract | Professional services, one-time fees, overage true-ups |

### The date the forecast runs on

```
opt_out_deadline = renewal_date − notice_period_days
```

A 1 February renewal with 90 days' notice is decided in October. Sort the whole book by this date,
not by renewal date. A null `notice_period_days` is `UNKNOWN — requires the executed contract`, caps
that row at Most Likely, and belongs in the coverage ledger — the count of nulls is usually the real
finding of a first forecast run.

## 3. Uplift, escalators and expansion at renewal

| Instrument | Where it lands | Gross rate | Net rate |
| --- | --- | --- | --- |
| Contractual escalator (CPI, fixed %) | Price uplift → **Increased product ARR** | Excluded | Included |
| List-price increase the customer accepted | Increased product ARR | Excluded | Included |
| Seats added at renewal | Increased product ARR | Excluded | Included |
| A new product added at renewal | New product ARR (cross-sell) | Excluded | Included |
| A discount granted to close the renewal | **Product decrease ARR** (contraction) | Reduces it | Reduces it |
| An expiring discount that raises the price | Increased product ARR — **only if the customer agreed in writing**. Otherwise hold value flat and log the concession | Excluded | Included when agreed |

An expiring discount is the trap. A `discount_expires` date inside the new term is a price increase
the customer has not agreed to. Forecasting the uplift because the contract technically allows it is
how a book carries phantom expansion into a quarter.

## 4. The ARR bridge, line by line

Every renewal resolves into exactly **one** bridge line. If the owner cannot name the line, the call
is not finished.

| # | Line | Sign | Definition | Owner |
| --- | --- | --- | --- | --- |
| 0 | Opening ARR | = | Must equal the prior period's closing ARR **exactly**. If it does not, stop and reconcile before anything else | Finance |
| 1 | New customer ARR | + | Logos not present in the prior period | Sales |
| 2 | New product ARR | + | Cross-sell — a product they did not previously have | AM |
| 3 | Increased product ARR | + | Upsell — seats, tier, volume, price uplift | AM |
| 4 | Contracted ramp ARR | + | Pre-agreed multi-year step-ups. **Tag separately** — it is contractual, not sold this period | — |
| 5 | Reactivation ARR | + | A previously churned logo returning | Sales |
| 6 | Product decrease ARR | − | Contraction — fewer seats, lower tier, retention discount | CS |
| 7 | Churned product ARR | − | A product removed entirely; the customer remains | CS |
| 8 | Churned customer ARR | − | Full logo loss; total ARR → 0 | CS |
| 9 | FX movement | ± | Constant-currency reset. **Never inside expansion** | Finance |
| 10 | Closing ARR | = | Check row — lines 0–9 must sum to it | Finance |

**Worked example — FY26 Q4**

```
  Opening ARR                                        $42,800,000
+ New customer ARR          Sales, 9 logos              $610,000
+ New product ARR           cross-sell, 4 accounts      $125,000
+ Increased product ARR     upsell + uplift             $242,000
+ Contracted ramp ARR       3 multi-year step-ups       $120,000
+ Reactivation ARR          1 logo returning             $35,000
− Product decrease ARR      contraction, 6 accounts     $140,000
− Churned product ARR       1 product removed            $24,000
− Churned customer ARR      2 logos                     $680,000
± FX movement               constant-currency reset     −$45,000
= Closing ARR                                        $43,043,000   ✓ reconciles
```

Two failure tests on this table. **The check row must reconcile to the dollar** — a bridge that
does not sum is not a rounding issue, it is a missing or double-counted deal. And **ramp must be
tagged**: a quarter carried by contracted step-ups looks like an expansion quarter and is not one,
because nobody sold it and it will not repeat unless someone does.

## 5. Reconciling the ATR and cohort methods in dollars

The two methods will not agree. The gap is not an error — it is the finding.

```
Period ARR loss (cohort)              =  contraction + churn                    $200,000 + $680,000
Loss at a renewal event (ATR)         =  Σ (ATR − retained) over events                    $644,000
Mid-term loss                         =  cohort loss − renewal-event loss                  $236,000
```

**Reading it.** A 94% gross renewal rate sitting inside a business showing 88% GRR says the renewal
team is doing its job and the leak is **mid-term** — contraction and cancellation on contracts that
never reached a decision point. That is a different problem with a different owner: mid-term leakage
is an adoption and support problem, not a renewal-motion problem, and no amount of renewal coaching
touches it.

The inverse — GRR healthy, renewal rate poor — says the book erodes at the decision point, which is
a motion, packaging or pricing problem.

Always publish the reconciliation line. "Renewal-event loss $644k + mid-term loss $236k = period
loss $880k" ends the argument about which number is right, because both are.

## 6. Twenty edge cases, worked

| # | Case | Treatment |
| --- | --- | --- |
| 1 | Mid-term upsell, co-termed | Booked as expansion when it happens; **added to ATR** at the next renewal. Never counted twice |
| 2 | Mid-term upsell on its own 12-month term | Its own renewal event, on its own date. Two ATR rows for one customer |
| 3 | Co-term shortening a contract | ATR is the run-rate at the new opt-out date; the stub period is not a separate loss |
| 4 | Multi-year, no decision point in period | ATR $0. It cannot churn at a renewal and must not dilute the rate |
| 5 | Multi-year with annual opt-out | One renewal event per anniversary, full ARR each time |
| 6 | Contracted ramp step-up | Its own bridge line. Not expansion sold this period, not renewal uplift |
| 7 | Consumption contract, $500k commit, $380k consumed | Forecast trailing-3-month annualised consumption. Below 70% entitlement at T-90, call the down-sell |
| 8 | Consumption overage in the prior year | Overage is not ARR. Exclude from ATR; if it recurs, it belongs in a raised commit, not in retention |
| 9 | Currency: EUR contract, USD reporting | Fix the rate at period start; the FX delta goes on line 9, never inside expansion |
| 10 | Partial churn — 100 seats to 60 | Contraction (product decrease), not churn. The logo is retained |
| 11 | Product churn — 1 of 3 products dropped | Churned **product**, not logo churn. Logo retention unaffected |
| 12 | Downgrade to a free tier | Logo churn for ARR purposes (ARR → 0); track separately as a downgrade for cohort curves |
| 13 | Reactivation within the same period | Reactivation line. Never nets against churn — netting hides both |
| 14 | Customer-side M&A: $200k + $150k → $300k | **$50k contraction** against a re-parented entity, not $150k churn. Re-parent first, then measure |
| 15 | Customer-side M&A, acquirer is not a customer | Churn of the acquired logo, with cause code `acquisition`. Note it — it is not addressable |
| 16 | Contract consolidation, no value change | Zero. Consolidation is an administrative event; if it shows a number, the mapping is wrong |
| 17 | Entity dissolved | Churn, cause `insolvency`. Omitted from ATR only if the dissolution precedes the period |
| 18 | Renewal slipping out of the period | Timing error in the variance decomposition. The ATR moves with it; do not book it as churn |
| 19 | Auto-renew with a lapsed notice window | Closed/Won at the lapse date, not the renewal date. The decision was made by silence |
| 20 | Retention discount to save a deal | Contraction, `value_delta_reason = discount_concession`. A saved logo at 80% of value is a 20% loss, not a flat renewal |

**Month-vs-cohort denominators.** A monthly NRR computed on the opening ARR of each month and then
compounded is not the same number as an annual cohort NRR, and the two diverge fastest in books with
seasonality. Pick one, state it, and never compound one to compare against the other.

## 7. Cohort curves, and why a single-period NRR hides everything

A single-period NRR is a scalar summarising a distribution. Two books with identical 104% NRR:

- Book A: every account renews flat, one account triples.
- Book B: broad 8% expansion across the base, no outliers.

Book A's NRR is one account's outcome. Book B's is a property of the product. They forecast
completely differently, and the scalar cannot tell them apart.

**Draw the curves.** Group accounts by the quarter they started, and plot each cohort's retained ARR
as a percentage of its own starting ARR against months since start.

| What the shape says | Reading |
| --- | --- |
| Curve dips then recovers above 100% | Land-and-expand working; early churn is an onboarding problem, not a product one |
| Curve flattens above 100% and stays | The strongest shape — durable net expansion |
| Curve declines steadily | Value decays with tenure; a renewal motion will not fix it |
| Recent cohorts below older ones at the same age | Something changed in ICP, packaging or onboarding. Find the quarter it changed |
| One cohort diverging sharply | Check for a single large account or a pricing change in that quarter |

Pair every headline NRR with: the **median** account's net change (the mean is dominated by the top
account), the share of expansion coming from the top 5 accounts, and the cohort curve for the last
eight quarters. Then, and only then, claim a direction of travel.

## 8. Concentration math

| Measure | Formula | Convention adopted by this skill |
| --- | --- | --- |
| Top-1 share | Largest account ATR ÷ total ATR | Flag > 10% |
| Top-5 / Top-10 share | Σ top N ATR ÷ total ATR | Flag top-5 > 40% |
| HHI | Σ (each account's ATR share × 100)² across the book | Flag > 1,500 |
| Industry share | Largest industry's ATR ÷ total ATR | Flag > 25% |
| Single-threaded ATR | Σ ATR where distinct `interaction.customer_participants` over 90 days ≤ 1 | Flag any account > 2% of ATR |

These thresholds are **operating conventions, not measured benchmarks** — no clean published SaaS
concentration benchmark was locatable, and inventing one would be worse than adopting a stated
convention. Each has a reason: above 10%, one account's outcome exceeds the forecast's own error bar,
so the roll-up communicates a precision it does not have; correlated industry exposure means three
renewals in one downturn are one bet, not three; and champion departure is a step change that is
invisible in usage until after it happens.

**Always print the zero-out simulation**, because a share is abstract and a dollar is not:

> If Northwind ($840k, 27.6% of ATR) renews at zero, the base case falls from $2.23M to $1.39M and
> the gross renewal rate from 78.9% to 51.3%.
