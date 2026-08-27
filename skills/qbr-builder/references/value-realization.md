# Value Realization — the number a finance team will accept

> Read this before any dollar figure reaches a slide, a one-pager or an email. A value
> number the customer's finance team rejects takes every other number in the deck down with
> it, and the rejection is almost never about the arithmetic — it is about the baseline, the
> attribution, or what the hours actually became.

**Contents**
1. [The four decisions](#1-the-four-decisions)
2. [Baselines](#2-baselines)
3. [Attribution](#3-attribution)
4. [Benefit classes and the arithmetic](#4-benefit-classes-and-the-arithmetic)
5. [The assumption register](#5-the-assumption-register)
6. [Bands, exclusions and how to present the number](#6-bands-exclusions-and-how-to-present-the-number)
7. [The six tests a CFO applies](#7-the-six-tests-a-cfo-applies)
8. [Worked example](#8-worked-example)
9. [Failure modes](#9-failure-modes)

---

## 1. The four decisions

Everything else is bookkeeping. These four decide whether the figure survives contact with
the customer's finance team.

| Decision | The rule | The failure it prevents |
| --- | --- | --- |
| **Baseline** | Pre-deployment, dated, **agreed with the customer before the period started**. Record value, unit, window, who agreed it, when, and their method | A baseline we reconstructed, presented as theirs — and value chosen after the fact |
| **Attribution** | A factor `α` in 0–1 with its level (A1–A4) and its source. Never 1.0 | Claiming the whole delta |
| **Benefit class** | Hours saved are not dollars saved unless the customer says what happened to the hours | The commonest reason finance rejects a CS value slide |
| **Exclusions** | State what you deliberately did not count | Nothing makes a number believable faster |

Run `../scripts/value_case.py` past two benefit lines. It enforces the baseline gate and the
A4 gate mechanically, so a line that cannot carry a dollar claim never quietly acquires one.

Three further rules govern the *shape* of the benefit table, and each is a validity condition
on the artifact rather than a preference. They are enforced in `qbr-builder` Part A6.

| Rule | Mechanism | Invalid output |
| --- | --- | --- |
| **C18 · Only value you agreed to measure** | Every line carries `Agreed?` — `agreed <date>`, or the literal tag `retrospective — weaker evidence`. Retrospective lines are ordered **below** every agreed line | An `Agreed?` cell left blank; a retrospective line above an agreed one |
| **C5 · Get them to say the number** | Every line carries a **Customer-stated** cell: quote, speaker, date. Empty means the line is tagged `vendor-asserted`, and a vendor-asserted line may not lead | A benefit line with neither a customer quote nor the `vendor-asserted` tag; a vendor-asserted figure at the top of the slide |
| **C19 · One number, not twelve** | The value slot carries **exactly one** headline number. Every other metric moves to the appendix | A metrics wall; a headline figure nobody on their side has said |

**Ordering key**, applied before anything is written: agreed + customer-stated → agreed +
vendor-asserted → retrospective + customer-stated → retrospective + vendor-asserted; within a
tier, largest risk-adjusted value first. **The headline number is row 1 of tier 1.** Where tier 1
is empty, no dollar figure leads: the slot carries the unit metric and the ask *"who can put a
number on this, and by when"*.

A number a customer said is worth more than a better number we calculated, because the customer
repeats theirs in the budget meeting we are not in. Retrospective metrics look chosen; a number
agreed at kickoff and reported at renewal is evidence. And a dashboard invites an argument about
which metric matters, where a single number carries a decision.

---

## 2. Baselines

**The baseline is the argument.** The delta is arithmetic; the baseline is the claim. A
customer challenges the baseline, never the multiplication.

### The baseline ladder — use the highest rung available

| Rung | Source | Dollar claim permitted? | `Agreed?` tag | What to record |
| --- | --- | --- | --- | --- |
| 1 | **Their business case or signed success plan** | Yes — band up to Attested | `agreed <date>` | The document, its date, its author |
| 2 | **Their own system, extracted by them, agreed before the period started** | Yes — band up to Attested | `agreed <date>` | System, extraction date, the person who ran it |
| 2b | **Their own system, extracted now** | Yes | `retrospective — weaker evidence` | The extraction, and why no baseline was agreed in advance |
| 3 | **A matched pre-period from our data, with their written agreement it is the baseline** | Yes — band capped at Evidenced | `retrospective` unless the agreement predates the period | The agreement itself (email is enough), plus the window |
| 4 | **An untreated control team inside their organisation** | Yes — band capped at Evidenced | `retrospective` | Which team, why it is comparable, what differs |
| 5 | **Nothing** | **No dollar claim.** Unit metrics only | — | The ask: who can supply the baseline, and by when |

**A reconstructed baseline is not their baseline until they say so.** Sending "we measured
your pre-deployment close cycle at 9.0 days — does that match your records?" and getting a
one-line yes moves rung 5 to rung 3. That email is the single highest-leverage artifact in
the whole value case, and it takes four minutes to send.

### Baseline hygiene

| Rule | Why |
| --- | --- |
| Pre-deployment, not pre-QBR | A baseline taken after go-live already contains our effect |
| Same unit, same definition, same population as the current figure | The commonest silent error: baseline over 6 teams, current over 4 |
| A window, not a point | One month is noise. Use the same window length on both ends |
| Seasonality named where it exists | A close cycle in December is not a close cycle in July |
| Written down at kickoff, not reconstructed at review time | The baseline that no longer exists is the usual reason there is no value story |
| A missing baseline is a finding, not a blank | `UNKNOWN — requires baseline from <named person>` on the slide |

---

## 3. Attribution

`α` is the share of the observed delta that our product caused. It is never 1.0, because
something else always contributed: a process change, a new hire, a seasonal effect, a
reorganisation, or simple regression to the mean.

| Level | Method | Typical defensible `α` | May carry a dollar claim? |
| --- | --- | --- | --- |
| **A1** | Treated vs untreated team, same period, same organisation | 0.6–0.9 | Yes |
| **A2** | Pre/post with a stated counterfactual and named confounders | 0.4–0.7 | Yes |
| **A3** | The customer states the share, in writing | Whatever they said | Yes — quote them |
| **A4** | Correlation only; no counterfactual, no control | — | **No.** Present the correlation, claim nothing |

**Name the confounders out loud.** "Two of six teams changed their process independently in
April, so we have haircut this line by 10%" is the sentence that converts a sceptical CFO
into a supportive one. Concealing the confounder and being asked about it does the reverse.

**The haircut** is separate from `α` and covers known-but-unquantified drag: partial-period
adoption, a team that churned mid-quarter, a measurement change. State the reason with the
number, every time. A haircut with no reason is decoration.

**A3 is the strongest rung and the easiest to get.** Ask the champion in the pre-call: *"Of
the 3.5 days you took out of the close, how much of that would you put down to us?"* Their
answer, in an email, is worth more than any model we can build.

---

## 4. Benefit classes and the arithmetic

| Class | What it is | May be stated in dollars when | Presented as |
| --- | --- | --- | --- |
| **time_released** | Hours no longer spent | The customer supplies a loaded rate **and** names what the hours became | Capacity, unless a redeployment is named |
| **cost_avoided** | A cost that would have been incurred | The avoided cost is on a real invoice, quote or approved plan | Dollars, with the counterfactual document named |
| **revenue_influenced** | Revenue the customer attributes in part to us | A3 attribution in writing | Influenced revenue, never "generated" |
| **risk_reduced** | An exposure lowered | A quantified exposure exists (fine schedule, audit finding, contractual penalty) | Exposure × probability delta, with both stated |

### The arithmetic

```
Annual hours released = users_affected × hours_saved_per_user_per_week
                        × working_weeks_per_year × adoption_rate
Gross value           = annual_hours_released × fully_loaded_hourly_cost   (their rate)
Risk-adjusted value   = gross_value × α × (1 − haircut)
Customer cost         = fees in period + their internal cost (admin FTE, integration, training)
Net value             = Σ risk-adjusted benefits − customer cost
Value ratio           = Σ risk-adjusted benefits ÷ customer cost           (state as "×")
Payback (months)      = customer cost ÷ (Σ risk-adjusted benefits ÷ 12)
Cost of inaction      = annualised value forgone (blocked users, unadopted workflows)
```

**Both sides cover the same window.** Benefit arithmetic annualises hours, so the cost side
is the annual fee — comparing an annualised benefit to a quarter of fees inflates the ratio
by four, and it is the error a finance reader spots first.

**Working weeks, not 52.** 46 is a defensible default for a salaried knowledge worker after
holiday, public holidays and sickness; whatever you use, state it.

**Adoption rate is measured, not assumed.** It is active users ÷ users_affected over the
same window, from the usage data, with its provenance tag.

**Include their internal cost.** A value ratio that ignores the admin FTE they assigned, the
integration work they paid for and the training days they lost is a ratio the CFO will
correct in the room. Ask for it; if they will not supply it, say the ratio is a ceiling.

### Cost avoided and revenue influenced

Cost avoided needs a **document**: the quote for the tool they did not buy, the requisition
they cancelled, the contractor invoice that stopped. "They would have hired two people" is
not cost avoided unless the two roles were approved and then withdrawn.

Revenue influenced is always **influenced**, never generated, and always partial. The
honest sentence pattern is: *"Your team attributes roughly a fifth of the Q2 win-rate change
to faster quote turnaround — on your numbers, that is about $X. We have not counted it in
the ratio."* Naming it and excluding it is stronger than counting it and being challenged.

---

## 5. The assumption register

Every value case ships with the register **beside the number, in the same visual field** —
not in an appendix. Assumptions in the appendix read as concealment; assumptions next to the
figure read as rigour, and they pre-empt the challenge.

```markdown
| # | Assumption | Value | Supplied by | Date | If challenged |
|---|---|---|---|---|---|
| 1 | Fully loaded hourly cost, Finance team | $68 | K. Osei, Finance Ops | 2026-08-12 | Their number, not ours — we asked and used what they gave us |
| 2 | Working weeks per year | 46 | Our default | — | At 44 the figure falls ~4%; the conclusion is unchanged |
| 3 | Attribution α = 0.7 (A2) | 0.7 | Pre/post, confounders named | 2026-08-14 | At α = 0.5 the ratio is 1.0× — still positive, and we would say so |
| 4 | Adoption rate 0.80 | 0.80 | `usage_daily`, Q3 window | 2026-06-30 | Observed, not assumed — the query is in the appendix |
```

Rules: one row per assumption; the "if challenged" column names **what the number becomes**,
not "may vary". Any assumption whose plausible alternative flips the sign of the conclusion
belongs on the slide itself, not in the register.

---

## 6. Bands, exclusions and how to present the number

| Band | Criteria | What goes on the slide |
| --- | --- | --- |
| **Attested** | Customer baseline + attribution attested in writing + their loaded cost | The figure, stated as theirs, register beside it |
| **Evidenced** | Baseline from a customer system, attribution A1/A2, at most one estimated input | The figure, with the estimated input named on the slide |
| **Indicative** | Two or more estimated inputs, or A3 with nothing in writing | "Indicative, on these assumptions" — and show them |
| **Not presentable** | No customer baseline, or A4 attribution | **No dollar figure.** Unit metric only, plus the ask for the baseline |

The band is also capped by the Coverage Ledger: a value case cannot be Attested when the
families feeding it are under 70% covered, and under 40% coverage the deck presents unit
metrics and no dollars at all.

**Exclusions.** List three to five things you deliberately did not count, on the slide. It
is the cheapest credibility in the deck and it removes the reader's main defence, which is
to assume you counted everything favourable.

**Presentation rules**

| Rule | Why |
| --- | --- |
| **One headline number on the slide** — everything else in the appendix | Two numbers means the room argues about which one counts instead of deciding (**C19**) |
| **The headline number carries its quote, speaker and date** | An asserted figure is a vendor claim; the same figure in their words is internal evidence (**C5**) |
| Round to the precision you can defend — `$410K`, not `$412,431` | False precision invites the challenge you cannot win |
| Show the ratio **and** the payback | Different readers care about different ones |
| Lead with their unit, follow with the dollar | "Three and a half days out of the close" lands before "$264K" |
| Never present a ratio without the cost side visible | A ratio with a hidden denominator reads as a trick |
| If the ratio is under 1.0×, say so first | They already know. Saying it first is the only way to keep the room |
| Provenance under every figure: `[system · field · window]` | The caveat travels with the number |

---

## 7. The six tests a CFO applies

Rehearse the answer to each before the meeting. They are asked in roughly this order.

| # | The test | What passes |
| --- | --- | --- |
| 1 | **Where did the baseline come from?** | A named person on their side, a date, and a method |
| 2 | **What else changed in that period?** | The confounders, named by you first, with the haircut applied |
| 3 | **What happened to the hours?** | A named redeployment, or the claim presented as capacity rather than cash |
| 4 | **Is this our number or yours?** | Their rate, their system, their extraction — or an honest "ours, and here is why" |
| 5 | **What did you leave out?** | The exclusions list, unprompted |
| 6 | **What would make this smaller?** | The sensitivity: the two inputs that move it most, and what the figure becomes |

Test 6 is the one that separates a value case from a marketing slide. Have the downside
number ready: *"At α = 0.5 instead of 0.7 this is 1.0× rather than 1.34×. It is still
positive, and I would still be here."*

---

## 8. Worked example

Run `python3 scripts/value_case.py --demo --explain` for the full trace. Summary:

| Line | Class | Baseline | α · level | Gross | Risk-adj. | Band |
| --- | --- | --- | --- | --- | --- | --- |
| Month-end close cycle | time_released | 9.0 working days, 2025-11-30, their close calendar (customer) | 0.7 · A2, attested by email | $420,403 | $264,854 | Attested |
| Permissions support load | time_released | 31 tickets/month, reconstructed by us | 0.6 · A2, not attested | $15,180 | $7,742 | Indicative |
| Quote turnaround → win rate | revenue_influenced | none | 0.4 · A4 | — | **suppressed** | Not presentable |

Roll-up: risk-adjusted benefit $272,596 · customer cost $204,000 (fees $180,000 + their
internal cost $24,000) · net $68,596 · **1.34×** · payback 9.0 months · **band Indicative**,
because line 2 carries a reconstructed baseline, an estimated loaded rate and no named
redeployment.

The third line is the instructive one. There is a real correlation and it is worth
mentioning out loud — but with no baseline and A4 attribution it carries no dollars, and it
appears in the exclusions rather than in the ratio.

---

## 9. Failure modes

| Failure | What it looks like | Correction |
| --- | --- | --- |
| Reconstructed baseline presented as theirs | "Your close took 11 days before us" — from our data, never confirmed | Get the one-line email agreement, or drop to unit metrics |
| Attribution of 1.0 | The whole delta claimed | State `α` with its level; nothing is ever entirely us |
| Hours converted straight to cash | "We saved you $412K" from 6,000 hours | Capacity released, monetised only with a customer rate and a named redeployment |
| Annualised benefit against quarterly fees | A 4× overstatement nobody notices until the CFO does | Same window on both sides |
| Assumptions in the appendix | The register is on slide 24 | Beside the number, same visual field |
| A ratio with no cost side | "3.2× return" with no denominator on screen | Show fees and their internal cost |
| Counting a benefit the customer already told you was not ours | The champion said the reorg drove it; the slide claims it anyway | Ask in the pre-call, and remove what they disown |
| No exclusions | Everything favourable counted, nothing named as excluded | Three to five exclusions, on the slide |
| A metrics wall in the value slot | Nine numbers, and the room picks the weakest to argue with | One headline number, chosen with them; the rest in the appendix (**C19**) |
| A figure nobody on their side has said | The champion cannot defend it when their VP asks where it came from | Get it in the pre-call, verbatim, with the date; otherwise mark the line `vendor-asserted` and do not let it lead (**C5**) |
| A benefit assembled after the fact from whatever moved | Retrospective metrics look chosen, because they were | Tag it `retrospective — weaker evidence`, order it below agreed lines, and agree next period's baselines now (**C18**) |
| Precision theatre | `$412,431.60` | Round to what you can defend |
| A different number each quarter for the same benefit | The method changed silently | Freeze the method; changes go in a stated changelog line |
