# RPH Scoring

> How the ranked section of the queue is scored: the return-per-hour formula, how each of its four
> terms is computed, the tie-break, the gates that must run before scoring rather than after, and
> the hard limit on what the number may be used to claim. Read whenever Step 3 ranks a book, and
> before reporting any figure derived from it.

**Contents**
1. [Why return per hour, not severity](#1-why-return-per-hour-not-severity)
2. [The formula](#2-the-formula)
3. [The four terms](#3-the-four-terms)
4. [The tie-break](#4-the-tie-break)
5. [Gates that run before scoring](#5-gates-that-run-before-scoring)
6. [What RPH is not — R22](#6-what-rph-is-not--r22)
7. [Worked example](#7-worked-example)
8. [Anti-patterns](#8-anti-patterns)
9. [Evidence register](#9-evidence-register)

---

## 1. Why return per hour, not severity

Rank the accounts left after the must-do and top-decile blocks by **return per hour**, not by
severity. A $30k save closable in 3 hours outranks a $120k save needing 40 hours whenever capacity
is the binding constraint — and in a book of this shape, capacity is always the binding
constraint. Severity ranking answers "which account is worst"; the week needs the answer to
"which hours protect the most dollars", and those are different questions with different orders.

The failure severity ranking produces is specific and repeatable: the top of the list fills with
large, structurally-doomed accounts that consume the week and change nothing, while a column of
mid-sized, genuinely addressable accounts sits below the cut line for a quarter. Addressability is
in the formula precisely to stop that.

---

## 2. The formula

```
RPH = (Value × Urgency × Addressability) ÷ Hours          [dollars per CSM hour]
```

Show the arithmetic for every scored row. A ranking whose inputs are not visible cannot be
challenged, and a ranking that cannot be challenged is not evidence — it is an assertion with a
number attached.

---

## 3. The four terms

| Term | How it is computed |
| --- | --- |
| **Value** | *Risk basis:* ARR × P(loss) at churn-risk band midpoints — Secure .05 · Watch .15 · At Risk .35 · High .60 · Critical .85. *Expansion basis:* opportunity ARR × cohort win rate (`UNKNOWN` if none). One basis per account per week, the higher — two reasons produce two half-plays and neither lands |
| **Urgency** | Days to the binding date (opt-out deadline · escalation SLA · committed date): ≤14 → 1.6 · 15–30 → 1.4 · 31–60 → 1.2 · 61–90 → 1.05 · 91–180 → 0.9 · >180 → 0.75 |
| **Addressability** | Can a play run THIS WEEK change the outcome? 1.2 adoption, enablement, relationship, support unblock — levers we hold · 1.0 pricing, budget, third party · 0.5 structural (acquired, shut down, product gap off the roadmap) · 0.2 blocked (awaiting customer, cooldown or blackout window) |
| **Hours** | From `play-durations.md`, including follow-up and the CRM write-up |

**Value — the one-basis rule.** An account with both a risk and an expansion reason to be worked
gets scored on the higher of the two and worked on that basis only. Running both in one week is
how a CSM arrives at a call with a save narrative and a price increase and delivers neither
credibly. Note the second basis in the row; it becomes next week's candidate.

**Value — band midpoints are not probabilities.** The five midpoints are the stated outputs of a
rules-based band model, not calibrated likelihoods. They exist to order work, and §6 governs what
may be said about any figure built from them. Where the bands have been backtested against actual
outcomes, substitute the observed rates and cite the sample size.

**Urgency — one binding date per account.** Use the earliest of the opt-out deadline, an
escalation SLA and a dated commitment. Where an account has none of the three, it has no binding
date: score it at 0.75 rather than inventing one. A book where most accounts land in the ≤14 or
15–30 buckets usually has a data problem — the dates are being read from renewal dates instead of
opt-out deadlines (**R1**).

**Addressability — the honesty term.** This is where a triage stops being wishful. The 0.5 and
0.2 levels are not verdicts on the account; they are statements about *this week*. An account
scored 0.2 because it is inside a post-incident cooldown returns to 1.2 the day the cooldown ends,
and the row should say so in *What would promote it* on the not-this-week list. An account scored
0.5 for a structural reason usually belongs in an escalation rather than in next week's queue.

**Hours — the denominator decides the order.** Because Hours divides, a 20% estimation error moves
rows across the cut line more readily than a 20% error in Value. Cost every row at play duration
with prep, follow-up and the write-up included, and use the measured medians from
`play-durations.md` §7 as soon as you have eight instances of your own.

---

## 4. The tie-break

**Stated so it is auditable:** higher RPH → earlier binding date → larger absolute Value → longer
since the last bilateral touch.

The last term is deliberate. Two accounts identical on the first three are separated by which one
has been ignored longer, which is the only tie-break that does not quietly favour the accounts
already receiving attention.

---

## 5. Gates that run before scoring

Gates run **before** scoring, not after. A gated account is not scored and then discarded; it is
never scored on that basis at all, and the gate that stopped it is named in the artifact so the
omission is visible.

| Gate | Rule |
| --- | --- |
| Health gate on expansion | No account scores on an expansion basis while its churn-risk band is At Risk or worse, onboarding is incomplete, time-to-first-value is unmet, a P1 is open, or an invoice is >30 days past due. Selling into dissatisfaction converts a renewal risk into a churn certainty |
| Post-incident cooldown | No commercial ask within 14 days of a Sev-1, or 30 days of an escalation closing |
| Renewal blackout | No new expansion ask inside T−30 to renewal; it reads as a squeeze and endangers the renewal itself |
| Pooled books | Score the *queue item*, not the account — see `cadence-by-segment.md` §4 |

**A gate removes a basis, not an account.** An At Risk account gated out of the expansion basis is
still scored on the risk basis, and usually scores well there. The gate changes what you do with
the hour, not whether the account gets one.

**Name every gated account.** The list of accounts the gates stopped is part of the output. It is
also the most useful thing the queue produces for a sales counterpart, who would otherwise read
the absence of an expansion play as an absence of opportunity.

---

## 6. What RPH is not — R22

**RPH ranks work; it does not forecast outcomes.** It is built from band midpoints — stated
probabilities of a rules-based model, not calibrated ones. Never report Σ(RPH × hours) as revenue
protected; where the bands are backtested, substitute the observed rates and cite the sample.

Three specific claims the number cannot support:

| Claim | Why it fails | Say instead |
| --- | --- | --- |
| "This week's queue protects $340k" | Σ(Value) is ARR weighted by uncalibrated midpoints, and it assumes every play succeeds | "The queue covers accounts holding $340k in ARR, ranked by expected return per hour" |
| "Account A is 60% likely to churn" | .60 is a band midpoint, not a measured rate for this account | "Account A sits in the High band; the band's assumed loss rate is .60, which is a modelling convention, not a measurement" |
| "We saved $X by working the top of the queue" | No counterfactual exists — the accounts you worked and the accounts you skipped are not comparable populations | Report what was worked, what was deliberately not, and the observed renewal outcomes when they arrive |

**When RPH may be reported as a dollar figure at all:** only as *ARR covered* and *ARR
deliberately not covered*, which are sums of actual contract values and carry no probability.
Those two figures are what belong in the Bottom Line and in `renewal-forecast`.

---

## 7. Worked example

A mid-market book, four accounts left after the must-do and top-decile blocks, line J = 9.0 h.

| Account | ARR | Band | Basis | Value | Binding date | Urgency | Address. | Hours | RPH |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Northwind | $48k | At Risk | Risk | 48,000 × .35 = 16,800 | Opt-out in 22 d | 1.4 | 1.2 (adoption gap, we hold the lever) | 3.0 | **$9,408/h** |
| Cobalt | $180k | Watch | Risk | 180,000 × .15 = 27,000 | Opt-out in 74 d | 1.05 | 1.0 (budget pressure) | 4.0 | **$7,088/h** |
| Meridian | $95k | High | Risk | 95,000 × .60 = 57,000 | No binding date | 0.75 | 0.5 (acquired, integration frozen) | 6.0 | **$3,563/h** |
| Alder | $60k | Secure | Expansion | 25,000 opp × .40 win = 10,000 | Quarter end, 40 d | 1.2 | 1.2 | 2.5 | **$5,760/h** |

Ranked: Northwind $9,408 → Cobalt $7,088 → Alder $5,760 → Meridian $3,563. Running hours: 3.0 →
7.0 → 9.5. **The cut line falls inside Alder** at 9.0 h — re-scope Alder to a 2.0 h version or
push it to next week and say which in the row; Meridian goes to the not-this-week list.

Three things to read off this example:

- **Meridian is the largest loss exposure in the table and ranks last.** That is the formula
  working, not failing: 6 hours against a frozen integration changes nothing this week.
  Addressability 0.5 plus no binding date is an escalation candidate, not a queue row.
- **Cobalt outranks Meridian on a lower band** because ARR and hours both favour it. Severity
  ranking would have inverted these two and spent the better part of a day on the wrong one.
- **Alder only scores because it passed the health gate** — Secure band, onboarding complete, no
  open P1, no blackout (40 days to quarter end is not within T−30 of a renewal). Had any of those
  failed, Alder would not appear on an expansion basis at all.

---

## 8. Anti-patterns

| Anti-pattern | Correction |
| --- | --- |
| Ranking by health score or band | Rank by (Value × Urgency × Addressability) ÷ Hours |
| Scoring an account on both bases in one week | One basis, the higher; note the other for next week |
| Reporting Σ(RPH × hours) as revenue saved or protected | RPH ranks work; report ARR covered and ARR not covered instead (**R22**) |
| Quoting a band midpoint as an account's churn probability | It is a modelling convention. Say so, or substitute a backtested rate with its sample |
| Scoring from the renewal date | The opt-out deadline, `renewal_date − notice_period_days` (**R1**) |
| Applying the gates after ranking | Gates run first; a gated account is named, not silently dropped |
| Addressability 1.2 on everything | The term is only honest if it is sometimes 0.5 or 0.2 |
| Estimating Hours by feel | Play duration from `play-durations.md`; the denominator decides the order |
| Hiding the arithmetic | Show Value, Urgency, Addressability, Hours and RPH per row, or the ranking cannot be challenged |

---

## 9. Evidence register

| Claim | Value | Source | Year | Label |
| --- | --- | --- | --- | --- |
| Churn-risk band loss midpoints | .05 / .15 / .35 / .60 / .85 | This library's `churn-risk` band definitions; stated outputs of a rules-based model | — | `[P]` |
| Urgency multipliers by days to binding date | 1.6 / 1.4 / 1.2 / 1.05 / 0.9 / 0.75 | Practitioner calibration for this library | — | `[P]` |
| Addressability levels | 1.2 / 1.0 / 0.5 / 0.2 | Practitioner calibration for this library | — | `[P]` |
| Post-Sev-1 cooldown before a commercial ask | 14 days | Practitioner | — | `[P]` |
| Post-escalation-close cooldown | 30 days | Practitioner | — | `[P]` |
| Renewal expansion blackout | T−30 to renewal | Practitioner | — | `[P]` |
| Past-due invoice threshold for the health gate | >30 days | Practitioner; aligns with the billing signal family | — | `[P]` |

**Label key:** `[M]` measured benchmark with a named neutral study · `[P]` practitioner rule of
thumb, no published measurement · `[A]` academic. Every multiplier and midpoint above is `[P]` —
a defensible ordering device, never a forecast. Replace each with your own backtested rate as soon
as you have the outcomes to backtest against.
