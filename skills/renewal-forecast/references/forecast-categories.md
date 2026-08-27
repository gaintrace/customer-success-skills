# Forecast Categories — entry criteria, demotion, base rates, calibration

> Read this whenever you are categorising a renewal, defending a Commit, setting the base rates
> a roll-up is weighted by, or being asked to turn a health score into a probability.

**Contents**
- [1. What a category is, and what it is not](#1-what-a-category-is-and-what-it-is-not)
- [2. Who may set each category, and every auto-demotion trigger](#2-who-may-set-each-category-and-every-auto-demotion-trigger)
- [3. The artifact that satisfies each criterion](#3-the-artifact-that-satisfies-each-criterion)
- [4. Category ceilings by time-to-renewal](#4-category-ceilings-by-time-to-renewal)
- [5. Building your own base rates](#5-building-your-own-base-rates)
- [6. Calibrating a health score to a probability](#6-calibrating-a-health-score-to-a-probability)
- [7. Category anti-patterns](#7-category-anti-patterns)

---

## 1. What a category is, and what it is not

A forecast category is a **statement about the evidence**, not a statement about feeling. It
compresses "here is what we have observed about this renewal" into one word so a roll-up can be
summed. That only works if the word means the same thing in every book, which is why every
category below is defined by artifacts that either exist or do not.

Two properties follow, and both are load-bearing:

- **A category already encodes probability.** Weighting a category by a second probability
  double-discounts it. Pick one mechanism — entry criteria, or a calibrated model — never both.
- **A category says nothing about value.** Commit means "this renews", not "this renews at
  100% of ATR". The value call is separate and independently entered (SKILL.md Step 4).

Categories describe outcome. Base rates describe how often each category has historically been
right *in your book*. The forecast is the pair.

## 2. Who may set each category, and every auto-demotion trigger

Permission matters because the failure mode is social: the person carrying the number is the
person least able to demote it. Demotion is therefore **automatic and mechanical**, and does not
require the owner's agreement.

| Category | May be set by | May be removed by | Auto-demotion triggers (any one fires) |
| --- | --- | --- | --- |
| **Closed/Won** | Deal desk / finance, on receipt of paper | Finance only, on cancellation | Countersignature rescinded; invoice voided; entity dissolved |
| **Commit** | Owner, **countersigned by the forecast owner (manager)** in the call | Any of: owner, manager, deal desk, automation | Economic-buyer contact ages past 30 days · renewal date slips ≥14 days · a second open dependency appears · order form withdrawn or unissued inside T-45 · sponsor departs · called value drops below quoted value · an open P1 is filed |
| **Most Likely** | Owner | Owner or manager | A second named dependency appears · the mitigation date passes with the dependency open · no usage evidence in the last 30 days · buying-group contact ages past 45 days |
| **Best Case** | Owner | Owner or manager | The named risk materialises (→ At Risk) · the named break lands (→ Most Likely) · T-30 arrives with the risk unresolved (→ re-called, never held) |
| **At Risk** | Owner, CSM, support, or automation on a risk signal | **Manager only**, and only against a landed save plan | Notice received (→ Closed/Lost) · opt-out deadline passes unaddressed (stays, exposure held) |
| **Omitted** | Ops / deal desk | Ops / deal desk | Renewal date moves back into the period · the M&A entity re-signs |
| **Closed/Lost** | Deal desk on receipt of notice | Finance only | Notice retracted in writing |

**The two structural gates.** Commit requires a logged conversation with the **economic buyer** —
the person who owns the budget line *this* year, not the champion who owns the workflow. And no
category above At Risk survives past the opt-out deadline without paper: past that date the
decision has already been taken, whatever the CRM says.

**Manager countersignature on Commit** is the single highest-yield process control in this file.
It converts Commit from a private opinion into a two-person claim, and it is what makes commit
leakage (§5) a measurable coaching signal rather than noise.

## 3. The artifact that satisfies each criterion

"Evidenced" means a reviewer who does not trust you can open something. This is the accepted list.

| Criterion | Satisfied by | **Not** satisfied by |
| --- | --- | --- |
| Economic buyer confirmed ≤30d | Calendar event with them on it + notes, a call recording, or an email thread they replied to | A champion saying "she's on board" · a LinkedIn title · a meeting they were invited to and skipped |
| Price, term, quantity agreed in writing | Email confirming the three, a redlined order form, a quote acknowledged in writing | A verbal on a call with no follow-up note sent to the customer |
| Order form / PO in motion | Order form issued from the quoting system, a PO number, a signature-request event | "Procurement has it" with no artifact |
| No open customer-side blocker | Explicit written confirmation, or an issue log with every item closed | Silence |
| Date unchanged ≥2 weeks | The CRM field history | The current value of the field |
| Value call = quoted value | The quote total matching `opportunity.amount` | A round number |
| One named dependency + dated mitigation | A task with an owner and a due date | "Waiting on legal" |
| Usage evidence ≤30d | A query result with the metric, window and value | "They're using it" |
| Risk record (At Risk) | Cause code, ARR exposure, first-detected date, save owner, dated plan, exec sponsor | A red health band with no record |

If the artifact does not exist, the criterion is not met. Write
`UNKNOWN — requires <the artifact>` and let the category fall. A missing artifact is a finding
about the process, and the count of Commit rows failing a named criterion is usually the most
useful number in the whole review.

## 4. Category ceilings by time-to-renewal

Time-to-renewal is measured to the **opt-out deadline**, never the renewal date.

| Window | Ceiling | Reason |
| --- | --- | --- |
| Before T-91 | **Most Likely** | Nothing is contractually settled this far out. The exception: a signed multi-year with no decision point, or a notice window already lapsed — those are contractual, so Commit (or Closed/Won) is correct and the ceiling does not apply |
| T-90 → T-46 | **Commit**, if all six criteria hold | The window in which paper genuinely moves |
| T-45 → T-31 | Commit only **with** an issued order form | Commit without paper inside six weeks is a hope, not a call |
| T-30 → T-1 | Best Case is **re-called**, to Most Likely or At Risk | "Best Case" a month out is an unmade decision |
| Past the opt-out deadline, unsigned | **At Risk**, automatically | The customer's decision window has closed without a decision reaching you |

Ceilings are not pessimism. They stop the roll-up from carrying certainty it has not earned yet,
and they make the T-90 vintage a real prediction rather than a copy of the T-30 one.

## 5. Building your own base rates

A base rate is the fraction of ATR in a category that actually closed won, measured over your own
closed history. It is the number the human call must beat, and it is the only defensible weight.

**Method.**

1. Take the **frozen** snapshot at a fixed vintage (T-90 is the useful one) for each of the last
   4–8 closed quarters. Never the edited end-of-quarter version.
2. For each category bin, compute both rates:
   - **Outcome rate** = ATR that closed won ÷ ATR in the bin
   - **Value realisation** = retained ARR (uplift excluded, capped at ATR) ÷ ATR that closed won
3. Require **≥30 renewal events per bin**. Below that the rate is noise; report the pooled rate
   across adjacent bins and say you pooled.
4. Recompute quarterly. Publish the window and the event count beside every rate, always:
   `Commit 96.4% (T-90 vintage, FY25 Q1–FY26 Q2, n=214)`.
5. Segment separately where the motion differs — Enterprise and self-serve renewals do not share
   a base rate, and pooling them hides both.

**Derived diagnostics from the same table.**

| Diagnostic | Formula | What it tells you |
| --- | --- | --- |
| Commit hit rate | Commit ARR closed won ÷ Commit ARR called | Whether Commit means one thing across the team |
| Commit leakage | 1 − hit rate, split into lost vs downsold | Above 5%, the entry criteria are not being enforced |
| Best Case conversion | Best Case ARR closed won ÷ Best Case ARR called | Above 70%, Best Case is being used as a sandbag for Commit |
| Save rate | At-Risk ARR retained ÷ At-Risk ARR identified | Only meaningful segmented by cause code |
| Dispersion | Standard deviation of the category rate across quarters | The width of the downside scenario, not a guess |

Until you have this table, **state bands, not point probabilities**, and say the rates are
uncalibrated. A weighted roll-up built on invented rates is a fabricated number with arithmetic
around it.

## 6. Calibrating a health score to a probability

A health score is an **ordinal ranking**. A probability is a **cardinal claim about frequency**.
Mapping Green/Yellow/Red to 90/60/30% converts one into the other by assertion, and it is the most
common fabricated number in customer success.

**Six reasons the mapping fails.**

| # | Failure | What it does to the forecast |
| --- | --- | --- |
| 1 | **Ordinal → cardinal** | The score ranks accounts correctly and still has no idea what 70 means in percent |
| 2 | **Base-rate neglect** | If 94% of your renewals close won, a "60% likely" yellow account is wildly pessimistic against the book's own base rate |
| 3 | **Committee-set weights** | Weights chosen in a workshop encode opinion about importance, not measured predictive power |
| 4 | **Treatment effect** | Red accounts get save motions. The observed churn rate of red accounts is the rate *after intervention*, so using it as an untreated probability under-forecasts risk on any account you do not work |
| 5 | **Feature leakage** | Scores that include "renewal likelihood", CSM sentiment, or an open save play are partly reading the answer. Calibrate only on features observable at the snapshot date |
| 6 | **Drift** | A score calibrated on last year's product and pricing decays. Re-check calibration every quarter |

**The calibration procedure.**

1. **Freeze features at T-90** for every closed renewal in the last 4–8 quarters. Nothing observed
   after the snapshot date may enter, or the backtest measures hindsight.
2. **Attach the outcome label** — renewed / churned, and separately the retained ratio.
3. **Bin by score decile** and plot observed renewal rate against predicted. This is the
   reliability diagram, and it is the whole diagnosis in one picture.
4. **Fit the calibration line.** Intercept ≈ 0 and slope ≈ 1 means the score is calibrated.
   Slope < 1 means it is over-confident at the extremes — the usual finding.
5. **Fix it with Platt scaling** (a logistic regression of the outcome on the raw score) or
   isotonic regression when you have ≥1,000 events. Both output a probability; neither invents one.
6. **Score it with Brier**, and compare against the base-rate baseline `p(1−p)`. A model that
   cannot beat "always predict the base rate" is not usable in a forecast, however good its ranking.
7. **Publish the window, the event count and the Brier skill score** beside any probability you
   then use. Recalibrate quarterly.

Until steps 1–7 have run, the honest output is a **band** — "Commit-eligible", "at risk" — plus the
category base rates from §5. Not a percentage.

## 7. Category anti-patterns

| Anti-pattern | Correction |
| --- | --- |
| Commit set on a champion conversation | The economic buyer owns the budget line; the champion owns the workflow. Log the buyer or it is not Commit |
| Commit held past T-45 with no order form | Demote on the call. Paper or Most Likely |
| Best Case used as a place to park upside | Best Case conversion >70% means it was Commit; the bias scan will find it |
| At Risk with no risk record | At Risk is a record — cause code, exposure, first-detected, save owner, dated plan, exec sponsor — or it is just a colour |
| Re-deriving risk inside the forecast | `churn-risk` owns the band and the override floors. Consume them |
| Demoting only when the owner agrees | Demotion triggers are mechanical. Consent is not one of the inputs |
| A category set once and never re-tested | Every trigger in §2 is checked at every call, on every row |
| Weighting a category by a health score | Double discount. One mechanism only |
| Base rates borrowed from an industry report | Your book's rates, your window, your event count — or bands |
