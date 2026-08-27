# Deal Structures

> Multi-year, ramps, annual opt-outs, price protection, co-terms, termination for convenience,
> payment timing and downgrades — what each one is worth, what it costs, what to hold, and what it
> does to the forecast.
>
> Evidence labels: `[M]` measured · `[V]` vendor/practitioner publication · `[P]` practitioner
> convention. Every dollar figure below is a formula; run `../scripts/concession_math.py` for this
> account's numbers.

**Contents**
[1. Choosing a structure](#1-choosing-a-structure) · [2. Multi-year](#2-multi-year) ·
[3. Ramps](#3-ramps) · [4. Price protection](#4-price-protection) · [5. Payment timing](#5-payment-timing) ·
[6. Switching cost](#6-switching-cost) · [7. Downgrades and right-sizing](#7-downgrades-and-right-sizing) ·
[8. Co-terms and stubs](#8-co-terms-and-stubs) · [9. Termination for convenience](#9-termination-for-convenience) ·
[10. What each structure does to the forecast](#10-what-each-structure-does-to-the-forecast) ·
[11. Failure modes](#11-failure-modes)

---

## 1. Choosing a structure

| Structure | What we get | What they get | Choose it when | The trap |
| --- | --- | --- | --- | --- |
| **1-year with escalator** | Annual price movement, annual leverage, annual value conversation | Flexibility | Default. Healthy account, working relationship, no reason to lock | Annual negotiation cost, and an annual chance to lose |
| **Multi-year, single term** | Committed ARR; no ATR event in the intervening years | A rate lock and one less procurement cycle a year | Stable use case, budget certainty on their side, an escalator you have written in dollars | Risk concentrated on one date, and the value conversation disappears unless you schedule it |
| **Multi-year with annual opt-out** | Very little | Everything: a rate lock with no commitment | Almost never — and only if the price reflects that it is an annual deal | **Not a multi-year.** Every anniversary is its own renewal event with its own `D` (`R1`) |
| **Ramp** | Adoption-matched revenue and a larger year-3 base | A lower entry cost while they roll out | Genuinely staged adoption with observable milestones | A ramp with no milestone is a discount with a delay |
| **Co-term** | One paper cycle, one approval, one date to manage | One number to approve | An expansion inside 90 days of `D` (`R12`) | One large number to negotiate against instead of two small ones to approve |
| **Restructure** | A baseline that matches how they actually use the product | A unit price that reflects volume | Usage has outgrown the entitlement, or packaging no longer fits | Presenting it as a penalty rather than a right-sizing |
| **Right-sized renewal** | The logo, the reference, a recovery path, a base at list | A contract that matches reality | Genuine over-entitlement (Step 7 of `../SKILL.md`) | Taking the reduction silently, without trading it |

**The default is the one-year deal with a contracted escalator.** Move off it only when the structure
buys something specific: a term in exchange for a rate hold, a ramp that matches a real rollout, or a
co-term that removes a procurement cycle. "Multi-year is better" is not a reason; multi-year revenue
that was bought with a 15% discount and an annual opt-out is worse than the annual deal it replaced.

---

## 2. Multi-year

### 2.1 What a multi-year is actually worth

| To us | To them |
| --- | --- |
| Removes one or two renewal events, each of which carries real loss probability | Rate certainty for budgeting |
| Removes one or two procurement cycles and their paper cost | Fewer internal approval cycles |
| Locks the escalator in writing, so future increases are arithmetic rather than negotiation | Protection from above-escalator increases |
| Increases the cost of switching mid-term | Sometimes a genuine discount |

The value to us is concentrated in **avoided loss probability and avoided cycle cost**, not in the
headline TCV. A three-year deal at a 12% discount has to avoid enough churn risk to pay for 12% —
which it may well do on an account with a stable use case, and will not on an account you were going
to keep anyway.

### 2.2 Write the schedule in dollars

```
Year 1   $412,000
Year 2   $432,600
Year 3   $454,200
```

**Not** "Year 1 $412,000, escalating annually at the greater of CPI or 4%." A formula is an argument at
every anniversary: their finance team will compute a different index on a different date and you will
spend two weeks of a renewal-free year litigating arithmetic. Dollars are unambiguous, they invoice
cleanly, and they make the deal's total visible to both sides at signature — which is a fairness
argument in your favour, not against it.

### 2.3 Multi-year with annual opt-out

Buyer-side analysis suggests the genuine incremental discount for a 2–3 year commitment is small —
single-digit percentage points — while multi-year commitments *with annual opt-outs* are sometimes
traded for far larger reductions in aggressive deals `[V]`. Note the asymmetry that creates: you have
given a multi-year discount for a one-year commitment.

**The rule:** an opt-out multi-year is an annual deal for every purpose that matters.

- **Price it** as an annual deal, at the annual rate.
- **Forecast it** as an annual deal — every anniversary enters ATR (`renewal-forecast`).
- **Staff it** as an annual deal: three `D` dates, three notice windows, three value conversations.
- **Say so in the room:** "If you need the annual exit, that's fine — it's then a one-year price with
  a three-year paper. The multi-year rate goes with a multi-year commitment."

Teams that book opt-out multi-years as multi-years over-report GRR and under-staff the account, and
both errors surface at the first anniversary they forgot to prepare for.

### 2.4 What to hold in a multi-year

| Hold | Why |
| --- | --- |
| The escalator, written in dollars | Otherwise the base flatlines for three years |
| Audit and true-up rights | Three years is long enough for usage to outgrow entitlement twice |
| An annual business review commitment, from both sides | A multi-year without a scheduled value conversation is a three-year gap in the relationship, and the churn arrives at the end of it |
| The right to reprice on a material scope change | Their acquisition should not silently triple your usage at year-1 pricing |

---

## 3. Ramps

A ramp is a scheduled step-up in price, volume or scope across a term: Year 1 $80k, Year 2 $100k,
Year 3 $120k. Used well it matches revenue to a real rollout. Used badly it is a discount with a delay.

| Requirement | Why | If absent |
| --- | --- | --- |
| **A real rollout plan** with named teams and dates | The ramp is supposed to track adoption | It is a discount, and should be priced as one |
| **An observable milestone per step** | You need to know whether the ramp is on track before the step lands | The year-2 step becomes a renegotiation |
| **The step is contracted, not optional** | Otherwise the customer is buying a one-year deal with an option | Forecast it as year-1 revenue only |
| **A named owner on their side for each step** | Rollouts stall when nobody owns them | The steps slip and the ramp is renegotiated downward |

**Booking.** Contracted step-ups are expansion, tagged as contracted ramp — do not let them inflate the
renewal-rate denominator (`renewal-forecast`). **Watch for:** a ramp that has slipped twice is telling
you the adoption assumption was wrong. Fix the rollout, or reset the ramp honestly at the next
renewal — do not let it quietly become a three-year discount nobody chose.

---

## 4. Price protection

A cap on future increases: "no more than CPI", "no more than 5%", "no increase in year 1".

**It is a concession, and it is the one teams most often give away without costing.** Price protection
transfers inflation and repricing risk from the customer to you, for the length of the protection.

| If they ask for | Give it in exchange for | And attach |
| --- | --- | --- |
| A cap for the coming term | A signature date, or reference rights | An end date on the cap |
| A cap for the full multi-year | Term length **and** prepayment or a larger commitment | A floor as well as a ceiling — a collar, not a cap |
| A cap on everything including add-ons and overages | Push back: this removes pricing on the growth part of the account | If conceded, a named review date |
| A cap that survives into successor terms | Refuse. This is the uplift-clause category — VP+ only | — |

**Cap the cap.** A protection clause needs three things to be safe: a **floor** (so it is a collar),
a **named index and measurement date** (so it is computable), and an **end date** (so it expires).
Missing any one of them, it is an open-ended commitment made by someone who will not be here for it.

---

## 5. Payment timing

The cheapest rung on the ladder, and the one most often thrown away for free.

```
Cost of extending payment terms by d days:   ARR × (d / 365) × cost_of_capital
Value of prepayment of p months:             ARR × (p / 12) × cost_of_capital
```

At a 10% cost of capital, moving a $500k account from Net 30 to Net 60 costs about **$4,100 a year**.
That is 0.8% of ARR — against a 5% discount at $25,000. It is, dollar for dollar, the most efficient
thing you can give, and it lands with a procurement team as a genuine concession because working
capital is something they are measured on.

| Move | Typical value to them | Cost to us | Get to attach |
| --- | --- | --- | --- |
| Net 30 → Net 45/60 | Real, and reportable | `ARR × d/365 × r` | A named signature date |
| Quarterly → annual upfront | Costs them | Saves us the same formula | A rate hold, or a discount rung you were going to give anyway |
| Full-term prepay on a multi-year | Costs them a lot | Saves us a lot | Rungs 6–7 open here — this is what prepayment is *for* |
| Milestone-based invoicing | Administrative friction for both | Cash-flow drag plus billing complexity | Rarely worth it; prefer a shorter term |

**Never** trade payment timing and a discount in the same breath. They are separate rungs and the
customer will take both if you offer them together.

---

## 6. Switching cost

The strongest number in a competitive renewal, and it must be built from **their** figures. A market
average is worse than nothing: procurement dismantles it in one question and you lose the argument you
would otherwise have won.

```
Switching cost (one-time, their side)
  = integration rebuild   Σ over live integrations of (their eng-days × their loaded day rate)
  + data migration        historical records to move, retention obligations, history that will not move
  + retraining            trained users × hours to competence × their loaded hourly cost
  + parallel run          months of running both systems × (both licence lines + the ops overhead)
  + process rewrite       documented workflows, approvals and reports to rebuild and re-certify
  + risk cost             the failure mode during cutover, in their language, priced by them
```

| Input | Where it comes from | If unavailable |
| --- | --- | --- |
| Live integrations | Your own integration telemetry, plus their stack diagram | Count what you can see and say the count is a floor |
| Their eng-day rate | Ask. Engineering leaders will usually give a range | `UNKNOWN — requires their loaded day rate`; present days, not dollars |
| Trained users | Users with ≥90 days of activity, from `usage_daily` | Use active users and label it a floor |
| Records under management | Your own object counts | Always available; use it |
| Reports and workflows built | Their admin console; ask the admin | Ask the admin — they will know, and they will usually be your best advocate on this point |

**How to use it.** Once, plainly, in one sentence, with the workings available if asked. "Before we
talk about the gap in the numbers — the eleven integrations, the four years of history and the 340
trained users are the part that doesn't move." Then stop. Repeating a switching-cost figure converts a
fact into a threat, and a threat converts a price conversation into a principle conversation, which
you lose.

**What it is not.** It is not a reason for them to stay. It is a reason for the comparison to be
honest. If the alternative is genuinely better for them after switching cost, the answer is a managed
exit (`R21`), not a bigger number.

---

## 7. Downgrades and right-sizing

The five-test diagnosis lives in `../SKILL.md` Step 7. This section covers the structure once you have
decided the request is genuine.

### 7.1 Structure the reduction

| Move | Why |
| --- | --- |
| **Right-size to real usage plus a named growth buffer** | Not to the number they asked for, which is usually round and arbitrary. "You're at 311 active against 500 contracted — let's do 350, which gives you room for the two hires you mentioned" |
| **Trade the reduction** | A smaller contract at list is frequently worth more than a larger one at 15% off. Removing an expiring discount as part of a right-size is a legitimate, honest ask |
| **Keep entitlement above the point where the use case breaks** | A downgrade that breaks the workflow is a deferred churn wearing a renewal's clothes. If 350 seats means the approval chain no longer works, say so |
| **Put the recovery path in the paper** | A pre-agreed unit price for adds during the term, so growing back costs them nothing to start and no new negotiation |
| **Keep the term** | A reduction is a reasonable moment to ask for length; they are getting a lower number and can afford to give one |
| **Book it correctly** | Contraction, `value_delta_reason = seat_reduction` — never a flat renewal. Misbooking this is how GRR lies to a board |

### 7.2 Why taking it is usually right

Median B2B SaaS gross revenue retention was **84%** in the 2026 Benchmarkit B2B SaaS & AI-native
metrics report (FY2025 data), down from 88%, with the 75th percentile at 91% `[V]`. Most of that
erosion is contraction, not logo loss — seat rationalisation from leaner teams rather than competitive
defeat. A book that fights every reduction converts recoverable contraction into unrecoverable churn,
and loses the reference with it.

**The honest framing to the customer:** "You're paying for 500 and using 311. I'd rather fix that than
have you notice it in eighteen months and lose trust in everything else I've told you."

### 7.3 When it is not genuine

Three or more tests on the negotiation-move side means it is a price negotiation wearing a downgrade's
clothes. Answer it with the ladder, not the seat count: "Happy to look at the number. Before I do —
your active usage is 480 against 500 contracted, so a seat reduction would take capacity you're using.
What's actually driving the target?"

---

## 8. Co-terms and stubs

| Instrument | What it does | When |
| --- | --- | --- |
| **Co-term** | Aligns an expansion to the existing renewal date, usually by a pro-rated stub | Expansion inside 90 days of `D` (`R12`) — one paper cycle instead of two competing for the same procurement capacity |
| **Stub term** | A short partial term to align dates | Aligning a subsidiary, or moving a renewal out of a customer's budget freeze |
| **Separate paper** | Expansion runs on its own cycle and its own date | Expansion outside 90 days of `D` — two small numbers to approve beat one large number to negotiate |

**Never use a stub to move a renewal inside a quarter for our own number.** It is visible, it is
transparently self-serving, and it costs more in credibility than the quarter is worth.

---

## 9. Termination for convenience

| | |
| --- | --- |
| **Default position** | None. A subscription with unrestricted TfC is a monthly contract with an annual invoice |
| **If unavoidable** | Cap it: a termination fee expressed as a percentage of the remaining term, a notice period at least as long as the standard notice window, and no exercise before onboarding cost is recovered |
| **Common buyer-side counter** | An early-termination fee capped at a share of remaining contract value, or an exit ramp — "terminable for convenience after year 1 with 60 days' notice" `[V]` |
| **What it changes downstream** | The deal forecasts as annual, not multi-year, and the ARR is not committed for the term. Say this internally when the deal is booked, not at the first anniversary |
| **What to get for it** | Term length, prepayment, or a higher rate. TfC is a real option with a real value; charge for it |

---

## 10. What each structure does to the forecast

Send this to whoever owns the forecast when the deal is booked, not at the anniversary.

| Structure | ATR treatment | Booking |
| --- | --- | --- |
| 1-year with escalator | Full ARR into ATR at the renewal date | Uplift is expansion, not renewal revenue |
| Multi-year, single term | ATR = $0 in intervening years; full ARR at the end date | Risk concentrated; flag it in the portfolio view |
| Multi-year with annual opt-out | **Every anniversary enters ATR** | Treat as annual for retention maths and for staffing |
| Ramp | Contracted step-ups are expansion, tagged as ramp | Do not let ramp steps inflate the renewal-rate denominator |
| Co-term | One renewal event at the aligned date | The stub is partial-period revenue, not a renewal |
| Right-sized renewal | ATR at the pre-reduction ARR; the delta is contraction | `value_delta_reason = seat_reduction` |
| Discounted renewal | ATR at the pre-discount ARR; the delta is contraction | `value_delta_reason = discount_concession` |

Two of these are where gross retention is most commonly overstated: booking an opt-out multi-year as a
multi-year, and booking a right-sized or discounted renewal as flat. Both are honest mistakes with the
same effect — a retention number that reports a decision nobody made.

---

## 11. Failure modes

| Failure | What it looks like | Correction |
| --- | --- | --- |
| Multi-year bought with a discount you would not otherwise give | 15% for three years on an account that was going to renew anyway | Price the avoided loss probability and the avoided cycle cost. If it does not cover the discount, the deal is worse than the annual one |
| Opt-out multi-year booked as multi-year | GRR overstated, account under-staffed | Three `D` dates, three notice windows, forecast as annual (`R1`) |
| Escalator written as a formula | An argument at every anniversary | Dollars per year on the order form |
| Ramp with no milestone | A discount with a delay | Observable milestone per step, with a named owner on their side |
| Price protection given free | The concession nobody costed | Trade it for term or prepayment; floor it, index it, expire it |
| Payment terms traded alongside a discount | Both given in one breath | Separate rungs, separate meetings |
| Market-average switching cost | "Migrations cost around $300k" | Their integrations, their rates, their users — or `UNKNOWN` |
| Switching cost repeated | A fact turned into a threat | Say it once, offer the workings, stop |
| Downgrade taken silently | A smaller contract, nothing received | Every reduction buys something: term, list pricing, references, a recovery clause |
| Downgrade booked as flat | GRR reports a decision nobody made | Contraction, with the reason code |
| TfC conceded to close | An annual deal with multi-year paperwork | Cap the fee, cap the notice, price the option |
| Stub used to pull a renewal into our quarter | Transparent and self-serving | Do not |
