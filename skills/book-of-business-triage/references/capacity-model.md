# The Capacity Model

> How many hours a CSM actually has, how to measure them rather than assume them, and how to
> prove to a manager that a book is too big. Read before the first triage run, and again any
> week the plan overran by more than 20%.

**Contents**
1. [Why capacity is computed before any account is scored](#1-why-capacity-is-computed-before-any-account-is-scored)
2. [The eight lines — plus lines I and J, and the three reserve shares](#2-the-eight-lines)
3. [Sizing the reactive reserve from actuals](#3-sizing-the-reactive-reserve-from-actuals)
4. [Measuring your own realisation factor](#4-measuring-your-own-realisation-factor)
5. [Variants: named, pooled, tech-touch, player-coach, ramping](#5-variants)
6. [The annual model and the structural-deficit test](#6-the-annual-model-and-the-structural-deficit-test)
7. [Worked example — a 40-account mid-market named book](#7-worked-example--a-40-account-mid-market-named-book)
8. [Worked example — a 220-account pooled book](#8-worked-example--a-220-account-pooled-book)
9. [The capacity stress-test memo](#9-the-capacity-stress-test-memo)
10. [Capacity anti-patterns](#10-capacity-anti-patterns)
11. [Evidence register](#11-evidence-register)

---

## 1. Why capacity is computed before any account is scored

A queue built first and costed second always fits. The costing step becomes a negotiation with
the plan you already wrote, and the plan always wins — so the hours get shaved, the follow-up
gets dropped from the estimate, and by Wednesday the week has quietly become reactive again.

Computing the budget first makes the cut line an arithmetic outcome rather than a judgement
call. That is the entire point: the CSM is not deciding whether to abandon an account, they are
observing that the budget ran out at row 11 and then deciding what to do about row 12.

The second reason is escalation. A manager cannot act on "I'm slammed". They can act on
"must-do work is 31.5 hours against 26.7 deployable, for the fourth week running, and here are
the three accounts totalling $310k that will not be touched."

---

## 2. The eight lines

| Line | Name | How to get it | Common error |
| --- | --- | --- | --- |
| **A** | Gross scheduled week | Contracted hours. Use 40 unless the role is formally part-time | Using actual hours worked. Planning against 52 hours institutionalises the overrun |
| **B** | Internal load | Sum the recurring internal calendar: 1:1, team meeting, forecast call, pipeline review, enablement, all-hands. Add CRM hygiene, note-writing not attached to a specific call, expense/admin, recruiting loops | Counting only meetings. Note-writing and CRM upkeep are the largest unlogged internal cost |
| **C** | Deployable customer hours | A − B | — |
| **D** | Committed customer meetings | Every customer meeting already on this week's calendar, costed at its **play duration** from `play-durations.md`, not its invite length | Costing a 30-minute call at 0.5 h. It is 1.25 h |
| **E** | Reactive reserve | §3 below | Setting it to zero because "this week looks quiet" |
| **F** | Discretionary hours | C − D − E | — |
| **G** | Realisation factor | §4 below. Default 0.85 | Applying it twice — once as a factor and again as padded estimates |
| **H** | Effective queue budget | F × G. **The number the queue is allocated against** | Reporting F as the budget and treating the overrun as a personal failing |

**The two-thirds anchor for line B.** This library's default is to reserve **two-thirds of the
week for customers and one-third for internal load**, which gives B = 13.3 h on a 40-hour week.
It is a practitioner convention with no published measurement `[P]`, and it sits alongside
library Operating Rule **R13 · The Capacity Truth**, which puts usable time at roughly 60% of a
week. Neither is a benchmark. Measure your own line B from four weeks of your recurring internal
calendar the moment you can, and state in the artifact which of the two you used.

**Line B is not fixed across roles.** A player-coach carrying a team lead responsibility, a CSM
on an on-call rotation, and a CSM in a heavy-hiring quarter all have materially different
internal loads. Recompute B when the role changes, not when the book changes.

### What does not belong in any line

| Item | Where it goes | Why |
| --- | --- | --- |
| PTO, holidays, company shutdown | Subtract from A for that specific week | Annualising PTO into B hides which weeks are short |
| Training and certification | B, if recurring; a must-do row if it is a one-off with a date | — |
| Travel time | D, attached to the meeting it serves | An onsite is not a 60-minute play |
| Interviewing candidates | B | It is real work and it is not customer work |
| Post-incident war rooms | E, the reactive reserve — that is what the reserve is for | Moving them to D pretends they were planned |

### 2.1 Lines I and J — the top-decile reserve, and what the ranked queue is allocated against

Two lines sit below H in a triage run and are not part of the generic capacity model, because they
exist to enforce Operating Rule **C31** rather than to describe a week:

| Line | Value | Basis |
| --- | --- | --- |
| **I** | Top-decile reserve | Σ touch cost of the top-ARR-decile members not already covered by a must-do row or a committed meeting, capped at 25% of H |
| **J** | Risk-allocatable budget | **H − I** — the number the ranked list is walked against |

**Allocating against H instead of J spends the decile reserve twice**, which is the single most
common arithmetic error in a triage run and is invisible until Thursday.

### 2.2 Allocating line J — the three reserve shares

Walk the ranked list, subtract hours, keep a running total; the row where line J is exhausted is
the cut line. Within J, reserve shares so that high-return work does not eat the whole week and
manufacture next quarter's must-do list. **Practitioner allocation, not a benchmark `[P]`:**

| Category | Target share of line J |
| --- | --- |
| High-return (risk or expansion with a named play) | 50–60% |
| Maintenance (cadence touches owed by segment) | 25–35% |
| Rot sweep and hygiene | 10–15% |

**Why maintenance has a floor.** Touch coverage — logged bilateral touch in 90 days ÷ assigned
accounts — under ~70% in a named tier means the book is oversized whatever the ARR says
(practitioner rule; the measure is defined in §6.3). Zero maintenance for four weeks and the
must-do list grows for a quarter: every account that goes untouched long enough eventually
produces a deadline, and deadlines come off the top of the following weeks' capacity. The
maintenance share is not generosity toward healthy accounts — it is what keeps the must-do block
small enough that the ranked queue still has hours to allocate.

**Why the rot-sweep share is small but never zero.** At 0.25 h per checkpoint, 10–15% of a
13-hour budget funds five to eight checkpoints — enough to keep the silent tail from compounding.
It is the cheapest line in the model and the first one cut under pressure, which is exactly why it
is written down as a share rather than left to what is left over.

**When the shares do not apply.** In a week whose must-do block already consumes most of line C,
J is small and the shares distort — 30% of 2 hours is not a maintenance programme. Below roughly
6 hours of J, state the shares as a target for a normal week, allocate what is actually there to
the highest-RPH rows, and note in the artifact that maintenance was suspended and for how long.
Three suspended weeks running is a §6 structural-deficit signal, not a scheduling accident.

---

## 3. Sizing the reactive reserve from actuals

The reserve is the hours consumed by work that arrives without being planned: inbound customer
questions, escalations, ad-hoc internal asks, incident response, "quick calls".

**Method — P75 of the last eight weeks.**

1. Each Friday, log one number: hours spent this week on work that was not in Monday's queue.
2. After eight weeks, take the 75th percentile of those eight numbers.
3. Floor it at 10% of line C. A reserve below that is a rounding error, not a reserve.
4. Recompute quarterly, or immediately after a structural change (a new product launch, an
   acquisition, a support-team reduction).

**Why P75 rather than the mean.** The cost of an under-sized reserve is asymmetric. Under-size
it and every busy week destroys the plan and the CSM stops trusting the queue. Over-size it and
some capacity goes unallocated — which the mid-week check can reclaim. Plan for a bad-but-not-
worst week.

**Worked:**

| Week | Unplanned hours |
| --- | --- |
| 1 | 3.0 |
| 2 | 7.5 |
| 3 | 4.0 |
| 4 | 11.0 |
| 5 | 5.5 |
| 6 | 4.5 |
| 7 | 6.0 |
| 8 | 5.0 |

Sorted: 3.0, 4.0, 4.5, 5.0, 5.5, 6.0, 7.5, 11.0. P75 (nearest-rank, ⌈0.75 × 8⌉ = 6th value)
= **6.0 h**. Floor check: 10% of C (26.7) = 2.7 h. Reserve = **6.0 h**.

**No history? Use the default and label it.** 5.0 h on a named enterprise/mid-market book,
7.5 h on a pooled book, 3.0 h on a tech-touch exception queue `[P — practitioner default, not
a benchmark]`. Print it as a default in the artifact so the first eight weeks of logging
produce a visible correction.

**The exhaustion rule.** If the reserve is fully consumed three weeks running, it is
mis-sized — resize from actuals. If it is consumed by the *same account* three weeks running,
that is not reactive work, it is an unacknowledged escalation. Promote it to the must-do block
with an owner and an end date, or escalate it.

---

## 4. Measuring your own realisation factor

Planned hours do not convert to delivered work at 1:1. The gap comes from task resumption,
partial blocks that are too short to start anything, and estimates that omit the write-up.

**Method.**

```
Realisation factor = Σ(hours of queue items actually completed) ÷ Σ(hours planned for them)
                     over the last 4 weeks
```

Count an item as completed only if its success measure was recorded. A call that happened but
was never logged did not deliver the play.

| Observed factor | Reading | Action |
| --- | --- | --- |
| ≥0.90 | Estimates are padded, or the queue is under-filled | Tighten estimates; add one more row above the cut line |
| 0.80–0.89 | Normal for a named book | Use the measured value |
| 0.65–0.79 | Fragmentation is eating the week | Consolidate: block two 3-hour windows; move the internal load off them |
| <0.65 | The plan is decorative | Stop tuning the factor. Run the structural-deficit test (§6) |

**Why 0.85 is the default and what it is not.** It is a practitioner allowance `[P]`. The
underlying mechanism is well measured — Microsoft's 2025 Work Trend Index (M365 telemetry
through 15 Feb 2025 plus a 31,000-respondent survey across 31 markets) found interruptions
**every two minutes during core hours, 275 per day**, **117 emails and 153 Teams messages per
weekday**, **57% of meetings ad hoc**, and **48% of employees describing their work as chaotic
and fragmented** `[M]`. Gloria Mark's interruption research at UC Irvine is the standard
academic citation for a resumption lag of roughly half an hour and task switching every few
minutes `[A — widely summarised in secondary sources]`. None of this yields 0.85. It yields
"the loss is real and material"; the coefficient must be measured locally.

---

## 5. Variants

| Coverage model | A | B | D typical | E default | Notes |
| --- | --- | --- | --- | --- | --- |
| **Named enterprise** | 40 | 13.3 | 8–14 h | 5.0 | Meeting-heavy; D dominates. Line C is often fully consumed by 6 accounts |
| **Named mid-market** | 40 | 13.3 | 5–8 h | 5.0 | The model in the SKILL default |
| **Pooled** | 40 | 12.0 | 2–4 h | 7.5 | Lower internal load (fewer forecast calls), much higher reactive share. Queue SLAs replace per-account plans |
| **Tech-touch / digital** | 40 | 16.0 | 0–2 h | 3.0 | B is higher because content, automation upkeep and journey QA are internal work. Discretionary hours go to program building, not accounts |
| **Player-coach** | 40 | 20.0 | 4–6 h | 5.0 | Half the week is management. Do not run a full named book on this line C |
| **New hire, weeks 1–8** | 40 | 24.0 | 2–4 h | 3.0 | Ramp, shadowing and enablement are the job. Assign ≤40% of a steady-state book |
| **On-call week** | 40 | 13.3 | as scheduled | 12.0 | Treat as a reactive week: do not plan high-return work you will not get to |

**Hybrid books.** A CSM carrying 12 named accounts and a 90-account pooled tail runs **two
budgets**, not one. Split line C explicitly — e.g. 60/40 — and allocate each separately, or the
named accounts will silently consume the pooled hours and the tail will rot. Write the split
into the artifact.

---

## 6. The annual model and the structural-deficit test

### 6.1 Annual deployable hours

```
Annual productive hours          1,880   (2,080 − PTO and holidays)          [P]
Heavy-meeting role               1,720   (use this for a CSM)                [P]
× customer share                 × 2/3   (two-thirds convention, R13)        [P]
= annual deployable hours        ≈ 1,147
÷ working weeks                  ÷ 46    (52 − 4 PTO − 2 holiday/shutdown)
= deployable hours per week      ≈ 25.0
```

This is the sanity check on line C. A weekly line C much above 25 means line B is
under-counted. It also means: **a full-time CSM has roughly 1,150 customer hours a year to
spend.** Every cadence decision in `cadence-by-segment.md` is a claim on that number.

### 6.2 Required hours — bottom-up from cadence

```
Required annual hours = Σ over accounts of ( planned touches/yr × hours per touch )
                        + Σ ( expected reactive hours per account per year )
Required weekly hours = Required annual hours ÷ 46
Structural deficit    = Required weekly hours − line C
```

Run this quarterly, and immediately on any territory change.

| Deficit | Verdict | Action |
| --- | --- | --- |
| ≤0 | **Servable** | Nothing. Consider whether the cadence is under-ambitious |
| 0 to +15% of C | **Tight** | Absorb with cadence discipline; watch touch coverage |
| +15% to +40% | **Oversubscribed** | Demote a tier of accounts to a lower coverage model, in writing, with the ARR named |
| >+40% | **Structurally oversized** | Escalate with §9. No amount of prioritisation closes this; it is a headcount or coverage-model decision |

### 6.3 The corroborating measure: touch coverage

```
Touch coverage = accounts with a logged bilateral touch in the last 90 days ÷ assigned accounts
```

Below **~70%** in a named-coverage tier, the book is oversized regardless of what the ARR-per-
CSM figure says `[P]`. This is the measure to bring to a manager, because it is observable in
the CRM and is not a matter of opinion.

### 6.4 External reference points — use to sanity-check, never to justify

| Reference | Value | Source | Year | Label |
| --- | --- | --- | --- | --- |
| Accounts per CSM | **No neutral published benchmark exists.** Build it bottom-up from §6.2 | — | — | — |
| ARR per CSM | **No neutral published benchmark exists.** Derive it from your own book | — | — | — |
| CS + Support spend | 9% of ARR median; 10% at $3–5M ARR; equity-backed ≈2× bootstrapped | SaaS Capital Spending Benchmarks (survey Mar 2026, 1,000+ private B2B SaaS) | 2026 | `[M]` |
| ARR per FTE (company-wide) | $200k at $50–100M ARR · $300k above $100M | Benchmarkit 2025 SaaS Performance Metrics | CY2024 | `[M]` |

The honest reading: there is **no current independent benchmark for accounts-per-CSM**, and the
widely-quoted figures circulating in the market are either vendor marketing or a decade old,
predating digital CS, PLG at scale and current tooling. Do not import one. Use the bottom-up
model in §6.2 as the argument, and the two spend benchmarks above as the only external context
worth citing — they are what a CFO will recognise anyway.

---

## 7. Worked example — a 40-account mid-market named book

**Inputs.** 40 accounts, $3.8M ARR, annual contracts, 60-day notice, named coverage. Week of
31 Aug 2026. No PTO. Four customer meetings already booked (two 30-min cadence calls, one
60-min renewal conversation, one 60-min escalation review).

**Capacity**

| Line | Value | Working |
| --- | --- | --- |
| A | 40.0 | — |
| B | 13.3 | Two-thirds rule; internal calendar audit came to 12.8, rounded to the anchor |
| C | **26.7** | 40.0 − 13.3 |
| D | 6.5 | 1.25 + 1.25 (cadence calls) + 2.0 (renewal conversation) + 2.0 (escalation review) |
| E | 6.0 | P75 of last 8 weeks (§3 worked example) |
| F | **14.2** | 26.7 − 6.5 − 6.0 |
| G | 0.85 | No local measurement yet — default, labelled |
| H | **12.1** | 14.2 × 0.85 |

**Must-do check.** Must-do rows total 9.0 h (one opt-out inside 30 days, one auto-renew flip,
one overdue commitment). 9.0 < 26.7, so the stop rule does not fire. But note that must-do
(9.0) plus committed meetings (6.5) is 15.5 h of the 26.7 deployable — **58% of the week is
already spoken for before a single discretionary decision is made.** That is the normal state
of a named book and it is why the queue is short.

**Allocation of H = 12.1 h**

| Category | Target share | Hours |
| --- | --- | --- |
| High-return | 50–60% | 7.0 |
| Maintenance | 25–35% | 3.6 |
| Rot sweep + hygiene | 10–15% | 1.5 |

Seven high-return hours buys roughly: one adoption reset (4.5) plus one champion re-multithread
(3.5) — which is already 8.0 and overruns. So it buys one adoption reset plus two async
data-backed check-ins (0.5 each) plus one CSQL handoff (1.0) = 6.5, leaving 0.5. **This is the
real shape of a week**, and it is why ranking by return per hour rather than by severity is not
a stylistic preference.

**Structural check.** Cadence for 40 mid-market accounts at 8 touches/year × 1.25 h = 400 h,
plus 12 renewal motions × 3.0 h = 36 h, plus 20 business reviews × 6.0 h = 120 h, plus reactive
6.0 × 46 = 276 h. Total ≈ **832 h** against ~1,147 annual deployable. Deficit is negative —
**servable**, with roughly 315 hours of slack for escalations, expansion and the unexpected.
That is a well-sized book.

---

## 8. Worked example — a 220-account pooled book

**Inputs.** Two pooled CSMs covering 220 SMB/low-mid accounts, $2.4M ARR total. Monthly and
annual mix. No named ownership.

**Capacity, per CSM**

| Line | Value | Working |
| --- | --- | --- |
| A | 40.0 | — |
| B | 12.0 | Fewer forecast calls than a named book |
| C | **28.0** | — |
| D | 3.0 | Scheduled sessions only; most contact is queue-driven |
| E | 7.5 | Pooled default — inbound is the job |
| F | **17.5** | — |
| G | 0.85 | — |
| H | **14.9** | — |

**The pooled arithmetic that matters.** 220 accounts ÷ 2 CSMs = 110 accounts each. At H = 14.9
discretionary hours, a 0.5-hour async touch each gives every account **one proactive contact
every 15 weeks** — before any of that capacity goes to risk work. That is the honest number,
and it is the number that decides the coverage model.

```
Weeks to cycle the book = accounts per CSM ÷ (H ÷ hours per async touch)
                        = 110 ÷ (14.9 ÷ 0.5) = 110 ÷ 29.8 = 3.7 weeks per full sweep
```

— if *all* discretionary hours went to sweeping, which they cannot, because risk and expansion
work must be funded. At the 25–35% maintenance share, the sweep takes **11–15 weeks**.

**Verdict.** A 110-account pooled book can sustain a triggered-touch model with a quarterly
automated sweep. It cannot sustain a promise of proactive human contact more than roughly
quarterly. Promising more is named-CSM cosplay; see `cadence-by-segment.md` §5.

---

## 9. The capacity stress-test memo

When the structural deficit exceeds +15% of line C, produce this. It is written for a manager
and it asks for a decision, not for sympathy.

```markdown
# Capacity Stress Test — <CSM or pool> · <date>

**Ask:** <one sentence — a headcount decision, a coverage-model change, or a book resize.>

| | |
|---|---|
| Book | <N> accounts · $<X> ARR |
| Deployable hours/week (C) | <X.X> |
| Required hours/week (bottom-up) | <X.X> |
| Structural deficit | <X.X> h/week (<Y>% of C) |
| Touch coverage, trailing 90d | <Y>% (threshold ~70%) |
| Weeks the deficit has run | <N> |
| ARR not covered at current cadence | $<X> across <N> accounts |
| ARR renewing in the next 180 days inside the uncovered set | $<X> |

## What is not happening
| Work type | Owed per year | Delivered TTM | Gap |
|---|---|---|---|

## Options
| # | Option | Cost | Effect on deficit | Risk introduced |
|---|---|---|---|---|
| 1 | Demote <segment> to pooled | 0 | −<X.X> h/wk | <N> accounts lose named contact; $<X> ARR |
| 2 | Add 0.5 FTE | $<X> loaded | −<X.X> h/wk | Ramp lag <N> weeks |
| 3 | Cut business-review cadence from <a> to <b> | 0 | −<X.X> h/wk | Value evidence thins before renewals |
| 4 | Do nothing | 0 | 0 | Touch coverage falls to <Y>% by <date>; <N> accounts pass the silence threshold |

**Recommendation:** <option, and why, in two sentences.>
**Decision needed by:** <date, tied to the earliest opt-out deadline in the uncovered set.>
```

---

## 9.1 Escalation routing — who hears about what

Read this when a triage produces something you cannot resolve inside your own budget. Escalate
the **decision**, never the problem: every row below travels with the ask, the dollars, the date,
the option set and your recommendation.

| Situation | Handle alone | Escalate to manager | Escalate to exec |
| --- | --- | --- | --- |
| Must-do hours exceed deployable hours | — | ✅ Same day, with the list of what will not happen | — |
| Single account >10% of book ARR trending down | — | ✅ | ✅ if opt-out ≤60 d |
| Competitor named by the economic buyer, or a re-bid | — | ✅ | ✅ |
| Termination terms or data-portability requested | — | ✅ Within 24 h | ✅ |
| Concession beyond your authority | — | ✅ | Per approval matrix |
| P1 aging >14 d with no committed fix date | — | ✅ | ✅ at 21 d |
| Cross-functional dependency with no owner | — | ✅ | — |
| A top-decile-ARR account deferred 3 weeks running | — | ✅ | — |
| Routine cadence slip on a tech-touch account | ✅ Log it | — | — |
| Book structurally oversized (deficit ≥4 weeks) | — | ✅ With the capacity stress test | ✅ At planning cycle |

Anything not on this list is handled alone and logged. A manager who hears everything stops
hearing anything.

---

## 10. Capacity anti-patterns

| Anti-pattern | What it looks like | Correction |
| --- | --- | --- |
| **Planning against gross hours** | A 40-hour queue | Allocate against line H |
| **Zero reserve on a quiet week** | "Nothing's on fire, I'll fill the week" | The reserve is for the fire you cannot see on Monday |
| **Invite-length costing** | A 30-minute call booked as 0.5 h | Play duration includes prep, notes, CRM and follow-up |
| **Annualising PTO into line B** | A constant B every week | Subtract PTO from A in the weeks it occurs |
| **Double-counting the realisation factor** | Padded estimates *and* ×0.85 | Pick one: honest estimates × measured factor |
| **Treating hours worked as capacity** | Line A = 52 | Institutionalises the overrun and hides the deficit |
| **One budget for a hybrid book** | Named and pooled accounts in one pool of hours | Split line C explicitly and allocate separately |
| **Benchmarking instead of measuring** | "The industry says 100–250 for mid-market, so we're fine" | There is no neutral accounts-per-CSM benchmark; build bottom-up (§6.2) and argue from your own hours |
| **Reporting "I'm slammed"** | No numbers | §9 memo: deficit in hours, uncovered ARR, four costed options |
| **Letting the reserve absorb an escalation for weeks** | Same account eating the reserve every week | It is not reactive work; promote it to must-do with an end date |

---

## 11. Evidence register

| Claim used in this file | Value | Source | Year | Label |
| --- | --- | --- | --- | --- |
| Reserve two-thirds of the week for customers, one-third internal; build capacity bottom-up from touchpoint counts | 2/3 | Practitioner convention for this library; cf. Operating Rule R13 (usable ≈ 60% of a week) | — | `[P]` |
| Accounts per CSM by segment | *No neutral published benchmark — figure deliberately not carried* | — | — | — |
| ARR per CSM by segment | *No neutral published benchmark — figure deliberately not carried* | — | — | — |
| CS + Support spend as % of ARR | 9% median (10% at $3–5M ARR); equity-backed ≈2× bootstrapped | SaaS Capital 2026 Spending Benchmarks, N>1,000 | 2026 | `[M]` |
| ARR per FTE | $200k ($50–100M ARR) · $300k (>$100M) | Benchmarkit 2025 SaaS Performance Metrics, CY2024 | 2025 | `[M]` |
| Interruptions every 2 min / 275 per day; 117 emails and 153 chat messages per weekday; 57% of meetings ad hoc; 48% describe work as fragmented | as stated | Microsoft Work Trend Index — M365 telemetry through 15 Feb 2025 + 31,000-respondent survey, 31 markets | 2025 | `[M]` |
| Resumption lag after interruption ≈ half an hour; task switching every few minutes | as stated | Gloria Mark, UC Irvine — via widely-cited secondary summaries | 2005–2008 | `[A]`, secondary |
| Annual productive hours | 1,880 (1,720 heavy-meeting) | Practitioner default | — | `[P]` |
| Live EBR fully loaded cost | 8–14 CSM hours | Practitioner | — | `[P]` |
| Touch-coverage floor for a named tier | ~70% in 90 days | Practitioner | — | `[P]` |
| Realisation factor | 0.85 | Practitioner allowance; measure locally | — | `[P]` |
| Reactive reserve defaults (5.0 named · 7.5 pooled · 3.0 tech-touch) | as stated | Practitioner default | — | `[P]` |

**Label key:** `[M]` measured benchmark with a named study · `[V]` vendor guidance or research ·
`[P]` practitioner rule of thumb, no published measurement · `[A]` academic.

**Never present a `[P]` value as a benchmark.** Write "commonly set at 0.85", not "research
shows 0.85".
