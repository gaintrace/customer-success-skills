# Baseline Capture

> A success plan with no baseline cannot prove a delta, and a plan that cannot prove a delta
> produces a narrative at renewal instead of an argument. This file covers when to capture, what a
> baseline record must contain, the four proxy methods when none exists, how to run a
> difference-in-differences comparison, and how a baseline's quality caps what you may claim.
>
> Evidence labels: `[M]` measured · `[PROD]` published production configuration · `[V]` vendor ·
> `[P]` practitioner · `[A]` academic.

**Contents**
- [0. The refusal condition and the Baseline Order](#0-the-refusal-condition-and-the-baseline-order)
- [1. Capture timing](#1-capture-timing)
- [2. The baseline record](#2-the-baseline-record)
- [3. Choosing the window](#3-choosing-the-window)
- [4. The four proxies](#4-the-four-proxies)
- [5. Difference-in-differences](#5-difference-in-differences)
- [6. Unit economics and attribution](#6-unit-economics-and-attribution)
- [7. Benefit classes — never mix them in one number](#7-benefit-classes--never-mix-them-in-one-number)
- [8. Baseline confidence and what it permits](#8-baseline-confidence-and-what-it-permits)
- [9. Re-baselining and the changelog](#9-re-baselining-and-the-changelog)
- [10. Failure modes](#10-failure-modes)
- [11. Worked capture](#11-worked-capture)

---

## 0. The refusal condition and the Baseline Order

**A goal may not be written without a baseline carrying a value, a source and an as-of date.** Not
"should not" — may not. Where any one of the three is absent, the correct output is not a softer
goal, a goal with a blank baseline cell, or a goal annotated "baseline TBC". It is a **Baseline
Order**: a statement of what must be measured, out of which system, by which named person on the
customer's side, by which date. The SMART goal is then written when the number arrives, and not
before.

The reason is evidentiary, not procedural. A target chosen before the starting point is known was
chosen in the knowledge of nothing, and a starting point reconstructed after the target was set was
chosen in the knowledge of the result. Both produce a delta the customer's finance team is right to
discount. The order of operations *is* the evidence.

### The Baseline Order record

Every field required. `TBC`, `n/a`, a role with no name, or a team name invalidates the order.

| Field | Required | Example | Why the order fails without it |
| --- | --- | --- | --- |
| `objective_ref` | Yes | O1 — cut cost to serve per claim 15% | Ties the order to the goal it is blocking |
| `metric_definition` | Yes | Tier-1 tickets per 1,000 active accounts per month; excludes Tier-2/3 and billing enquiries | Two analysts must not be able to pull different numbers |
| `source_system_field` | Yes | Support platform · `ticket.type = tier_1` | An unnamed source is not auditable a year later |
| `window_rule` | Yes | 3 complete months, decided before the pull (§3) | A window chosen after seeing the result is unfalsifiable |
| `measured_by_customer` | Yes | Priya N., Director Support Ops | Nobody on their side defends a number they did not run |
| `pull_by` | Yes | 2026-09-12 | An order with no date is a wish |
| `unblocked_when` | Yes | Priya confirms the figure in writing | Names the event that lets the goal be written |
| `escalation_if_unfilled` | Yes | Raised to D. Okafor (VP Claims Ops) as decision 1 in §7 on 2026-09-15 | An unfillable order is a sponsor decision, not a gap to absorb |

### What the plan looks like while an order is open

The objective sits at `Proposed`. §3A of the plan carries the order; §3B carries no row for it. The
plan's Bottom Line prints the count of orders outstanding and the earliest `pull_by`. The objective
is Watchpoint at best in any review, because an unmeasured objective is not the same as a healthy
one. Where the order cannot be filled at all, the objective is rewritten as *establish the baseline*,
inheriting the order's named measurer and date as its own owner and target date.

**Never substitute our own pull for theirs on a business metric.** We may run the extract; their
named owner confirms the number in writing, and that confirmation is what closes the order. A
baseline the customer has not confirmed is a vendor claim wearing a measurement's clothes.

---

## 1. Capture timing

| When | What you get | Verdict |
| --- | --- | --- |
| At contract signature or kickoff | A true pre-state, measured before anything changed | **Correct.** Capture here |
| During implementation | A partly-changed state; some effects already landed | Usable only with the contamination named on the artifact |
| At go-live | Not a baseline. The intervention has begun | Reconstruct backwards or use a proxy |
| At the renewal | A reconstruction under time pressure, argued in front of the person you need to convince | The worst position in customer success |

**The rule:** capture the baseline in week 1, before the first configuration change. If no baseline
exists, *establishing it* becomes the first objective, with an owner and a date. That is an honest
plan, not a failed one.

**Ask for the as-of date on every export.** A baseline whose window you cannot state is not a
baseline. Record the pull date and who pulled it, because both will be asked about a year later.

---

## 2. The baseline record

One record per value driver. An objective missing any required field stays `Proposed`.

| Field | Required | Example | Why it matters |
| --- | --- | --- | --- |
| `value_driver` | Yes | Support ticket deflection | Groups goals under an objective |
| `metric_name` | Yes | Tier-1 tickets per 1,000 active accounts per month | Ambiguity here reappears as a dispute later |
| `metric_unit` · `direction` | Yes | count · ↓ | Prevents a "reduction" being read as a rise |
| `baseline_value` | Yes | 412 | The number the delta is measured from |
| `baseline_period` | Yes | 2026-01-01 → 2026-03-31, 3-month mean | A window, never a single day |
| `baseline_source` | Yes | Support export, `ticket.type = tier_1`, pulled 2026-04-04 | Auditable by them |
| `baseline_method` | Yes | Reconstructed / control / attested / benchmark × haircut | Caps the claim; see §4 |
| `measurement_owner_customer` | Yes | Priya N., Director Support Ops | The person who re-runs it monthly |
| `measurement_cadence` | Yes | Monthly, by the 5th | Missing cadence is why plans go quiet |
| `unit_economics` | If monetised | $18.40 fully loaded per Tier-1 ticket, customer-supplied | Converts the metric to currency |
| `unit_economics_source` | If monetised | Their finance team, stated 2026-08-14, low end of a $18.40–$22 range | Named attester, low end |
| `target_value` · `target_date` | Yes | 290 · 2026-12-31 | A number and a date |
| `attribution_pct` · `attribution_set_by` | If monetised | 70% · Priya N. | The customer sets it, not us |
| `confidence` | Yes | High / Medium / Low, with the criterion | See §8 |
| `last_validated` | Yes | 2026-08-14 | Staleness is visible |
| `exclusions` | Where they exist | Entity 6 excluded, ERP migration in Q3 | Named exclusions beat a quietly better number |

---

## 3. Choosing the window

| Metric behaviour | Window | Reason |
| --- | --- | --- |
| Weekly operational counts | 12 weeks, mean | Absorbs single-week noise |
| Monthly financial or process metrics | 3 complete periods | One period is an anecdote |
| Seasonal metrics | The same period last year **and** the trailing 3 periods | Otherwise the season does the work and takes the credit |
| Rare events (incidents, audit findings) | 12 months, count | Rates on small denominators are unstable |
| Anything measured during a known anomaly | Exclude the anomaly, name the exclusion | An unnamed exclusion looks like a manipulated number |

**Two guards.** Never pick the window after seeing which window flatters the result — decide the
rule first and write it down. And never use a period containing a confounding event (reorg, pricing
change, migration, peak season) without naming the confounder on the artifact.

---

## 4. The four proxies

Use the highest tier available. Every figure derived from a tier 2–4 baseline carries its label
**wherever it appears** — internal plan, review pack, value case and customer block. A figure printed
without its label is invalid output and is regenerated with the label attached. A proxy is never
described as a measurement, and the tier caps objective confidence, which caps plan confidence
(**R23**).

| Tier | Internal token, printed beside the figure | Customer wording | May appear in |
| --- | --- | --- | --- |
| 1 | `[T1 · reconstructed · measured]` | "measured from <their source>, <window>" | Headline, value case, customer block — no cap |
| 2 | `[T2 · control · comparative, not measured]` | "compared with <control> over the same period" | Anywhere, with the control and its comparability stated |
| 3 | `[T3 · attested by <name>, <date> · stated, not measured]` | "your figure, confirmed by <name> on <date> — an estimate, not a measurement" | Body of the plan and the value case, labelled. Never the headline number |
| 4 | `[T4 · benchmark ×0.5 · estimate, not measured]` | none exists | Internal only. Never the customer block, never a renewal value case |

A tier 3 or 4 baseline does not close a Baseline Order — it holds the place while the order runs. Keep
the order open, keep its `pull_by` date, and replace the proxy with the measurement when it lands.

### Tier 1 — Reconstruct

Rebuild the pre-period from their own systems: warehouse tables, application logs, ticket history,
ERP exports, spreadsheet archives, email records of the manual process.

| Step | Detail |
| --- | --- |
| 1 | Identify a system that was running before the change and still holds history |
| 2 | Agree the query definition with their measurement owner **before** running it |
| 3 | Run it for the chosen window and share the raw extract, not just the summary |
| 4 | Have their owner confirm the number in writing, with a date |

This is a real baseline and carries no cap. Most "we have no baseline" situations are actually
"nobody has looked" situations, and this tier resolves them.

### Tier 2 — Control group

A business unit, region, product line or cohort that has not adopted, measured over the same window.

| Requirement | Test |
| --- | --- |
| Comparable population | Similar size, mix and process. State how you established comparability |
| Same measurement source | Both sides pulled from the same system with the same definition |
| Stated release plan | Say when the control will be released, and hold to it |
| Named confounders | Anything affecting one side and not the other |

The strongest substitute for a true counterfactual that a CSM can produce without a formal study.
Report it as difference-in-differences (§5).

### Tier 3 — Customer-attested estimate

A named owner puts a number in writing. Rules: **use the low end** of any range they give, capture
it in writing rather than from memory of a call, name the attester and the date on the artifact,
and re-confirm it at each review because attested numbers drift.

Cap: Medium confidence at best. It may appear in a value case, labelled, with the attester named.

### Tier 4 — External benchmark with an explicit haircut

Apply a stated haircut (0.5 is a defensible default), label it an estimate on the artifact, and cite
the benchmark's source and year. It never enters a renewal value case as a measured figure and it
never becomes the number in the headline.

**If none of the four is available:** the objective becomes *establish the baseline*, with an owner,
a date and a method. Write that objective; do not write a target with no starting point.

---

## 5. Difference-in-differences

The comparison that survives a CFO. Where a control exists, report the change in the adopted group
minus the change in the non-adopted group over the same window.

```
DiD = (adopted_after − adopted_before) − (control_after − control_before)
```

| Element | Requirement |
| --- | --- |
| Same window both sides | Any offset invalidates it |
| Same metric definition both sides | Confirm the query, not the label |
| Pre-period parallel trend | Show 3 pre-periods for both groups; if they were already diverging, say so and discount |
| Population sizes | Print n for both sides. Small controls produce noisy answers |
| Confounders | Anything affecting one group only, named on the artifact |

**Worked shape.** Adopted regions: 26.9% → 34.2% win rate (+7.3pts). Control regions: 27.4% → 29.1%
(+1.7pts). DiD = +5.6pts. State it as "+5.6 points against a matched control over the same two
quarters, n=488 adopted and n=852 control", and state the confounder: a pricing change on 1 January
affects both groups but not necessarily equally.

---

## 6. Unit economics and attribution

**Unit economics come from the customer.** Ask during discovery, in the customer's own terms: cost
per ticket, cost per claim, fully loaded hourly rate, average deal value, revenue per store, cost of
a day of delay. Take the low end of any range. Name the person who supplied it.

Where a loaded rate must be constructed, state the construction: base salary plus benefits, payroll
tax and allocated overhead, divided by annual productive hours — practitioner defaults are a
1.25–1.40 loaded multiplier and roughly 1,880 productive hours a year `[P]`. Say which you used.

**Attribution is set by the customer, stated as a number, and shown on the artifact.** "Priya sets
our contribution at 70%" is defensible; a silent 100% is not. Any metric with two or more plausible
drivers is presented twice: gross movement and attributed movement.

**Productivity benefits need a recapture rate.** Hours returned to staff become cash only if the
time is redeployed or a hire is avoided. Forrester's Total Economic Impact studies apply a 50%
recapture rate for general employees and 75% for help-desk professionals, and risk-adjust benefit
estimates downward — 10% in the 2025 study of Glean — to reflect the likelihood that estimates meet
projections and continue to be tracked `[M]`. Use 50% as the default; anything above 75% needs a
headcount-avoidance argument in writing.

---

## 7. Benefit classes — never mix them in one number

| Class | Definition | In the headline? |
| --- | --- | --- |
| **Hard / cash-releasing** | Money that leaves the budget and does not come back — retired contracts, cancelled requisitions | **Yes** |
| **Cost avoidance** | A cost that would have been incurred and was not; margin protected without a budget line moving | Yes, labelled and separated |
| **Productivity / time saved** | Hours returned; cash only with an explicit recapture rate | Yes, recapture- and risk-adjusted |
| **Revenue influenced** | Revenue with several causes; requires a customer-set attribution factor | Yes, at the attributed figure only |
| **Risk / compliance** | Expected value of an avoided loss | Only where the customer supplies the probability |
| **Soft / experience** | Satisfaction, morale, brand | **No.** Adjacent panel, un-monetised |

The headline number contains hard, cost avoidance, recapture-adjusted productivity and attributed
revenue only. Mixing a soft benefit into it is the fastest way to lose a finance audience.

---

## 8. Baseline confidence and what it permits

| Confidence | Entry criteria | What you may claim |
| --- | --- | --- |
| **High** | Tier 1 or 2 method · source system named and still live · window ≥3 periods · customer owner confirmed the number in writing | A quantified outcome in the value case, with the delta stated |
| **Medium** | Tier 3, or Tier 1 with a short window or one confounder | A quantified outcome, labelled as attested or caveated, with the attester named |
| **Low** | Tier 4, or a reconstruction the customer has not confirmed | Direction only. No currency figure in the headline |
| **Insufficient** | No method available | No claim. The objective is *establish the baseline* |

Baseline confidence caps objective confidence, which caps plan confidence. Confidence never exceeds
what coverage permits (**R23**).

---

## 9. Re-baselining and the changelog

Re-baseline when: their metric definition changes · the source system is replaced · a reorganisation
changes the population · the objective itself changes · an acquisition changes the denominator · the
executive sponsor changes and restates the objective.

Every change writes a row. Without this table a plan can be quietly improved into meaninglessness.

| Date | Field changed | From | To | Reason | Agreed by (customer) |
| --- | --- | --- | --- | --- | --- |

**Two rules.** Never revise a baseline or a target upward mid-flight without naming the input that
changed and the customer person who agreed it. And never carry a previous period's value forward
silently — either re-measure, or mark the period `UNKNOWN — requires <source>`.

---

## 10. Failure modes

| Failure | What it produces | Guard |
| --- | --- | --- |
| A goal written with the baseline left blank or marked TBC | A target nobody can prove was reached, and a renewal argued on narrative | The goal is not written. A Baseline Order is raised instead (§0) |
| A proxy figure printed without its tier label | An estimate read as a measurement by the next person to quote it | The label travels with the figure everywhere, including the customer block (§4) |
| Single-day baseline | A number chosen by luck | A window of at least 3 periods |
| Window picked after seeing results | An unfalsifiable claim | Decide the rule first, in writing |
| Baseline captured after go-live and called a baseline | An understated delta at best, a fabricated one at worst | Reconstruct, or label it a post-change estimate |
| No measurement owner on the customer side | The metric stops being pulled by month 3 | A named person and a cadence, in the record |
| Unit economic supplied by us | An ROI number the customer does not believe | It comes from them, at the low end, with a name |
| Silent 100% attribution | A number a CFO discounts entirely | Customer-set percentage, printed |
| Soft benefits inside the headline | The whole figure is discounted | Adjacent un-monetised panel |
| Metric definition drifts between periods | An untraceable trend | Changelog row, every change |
| Confounder unmentioned | The claim collapses when someone else notices | Name it before they do |
| Benchmark used as a measurement | A fabricated claim with a citation attached | Haircut, label, never in the headline |

---

## 11. Worked capture

**Account:** fictional insurer. **Objective:** cut cost to serve per claim by 15% in FY27.

| Step | What happened |
| --- | --- |
| 1 · Objective agreed | "Cost to serve per claim, 15% over plan, and I own it" — D. Okafor, 2026-08-14, quoted from their Q2 shareholder letter |
| 2 · Value driver chosen | Tier-1 support deflection, the largest controllable component of cost to serve |
| 3 · Metric defined with their owner | Tier-1 tickets per 1,000 active accounts per month; excludes Tier-2/3 and billing enquiries; agreed with Priya N. before the pull |
| 4 · Method selected | Tier 1, reconstruct — their support platform holds 3 years of history |
| 5 · Window chosen | 2026-01-01 → 2026-03-31, 3-month mean; Q2 excluded because a platform migration inflated volume, and the exclusion is printed |
| 6 · Value | 412 per 1,000 active accounts per month |
| 7 · Confirmed | Priya N. confirmed the extract by email, 2026-04-08 |
| 8 · Unit economic | $18.40 fully loaded per Tier-1 ticket, supplied by their finance team, low end of an $18.40–$22 range |
| 9 · Attribution | 70%, set by Priya; the remainder to their knowledge-base rewrite |
| 10 · Target derived | 31% observed deflection on 3 covered surfaces × 63% topic coverage ⇒ 105–160 ticket reduction band; target 290 set at the low end |
| 11 · Confidence | High — Tier 1 method, live source, 3-period window, customer-confirmed in writing |
| 12 · Cadence | Monthly by the 5th, re-run by Priya, reviewed with the CSM fortnightly while the rollout is open |
