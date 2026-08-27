# Capacity Math

> The full derivation: how many hours a CSM actually has in a year, how many hours an account
> actually needs, and therefore how large a book can be. Read before quoting any ratio, and again
> whenever someone proposes a book size without showing their arithmetic.
>
> This file works at the **annual, organisational** grain — designing books and headcount. For one
> CSM's **weekly** allocation inside an already-set book, use
> `../../book-of-business-triage/references/capacity-model.md`; the two are deliberately different
> models and must not be conflated.
>
> Evidence labels: `[M]` measured with a named study · `[V]` vendor or first-party operating model ·
> `[P]` practitioner convention · `[A]` academic.

**Contents**
1. [The derivation, line by line](#1-the-derivation-line-by-line)
2. [Loaded cost per hour](#2-loaded-cost-per-hour)
3. [Auditing internal load](#3-auditing-internal-load)
4. [Role variants](#4-role-variants)
5. [The motion catalogue by segment](#5-the-motion-catalogue-by-segment)
6. [Reactive hours from actuals](#6-reactive-hours-from-actuals)
7. [Book size, and three worked examples](#7-book-size-and-three-worked-examples)
8. [Sensitivity — what to measure first](#8-sensitivity)
9. [The multi-period model](#9-the-multi-period-model)
10. [Anti-patterns](#10-anti-patterns)
11. [Evidence register](#11-evidence-register)

---

## 1. The derivation, line by line

| Line | Item | Default | How to get the real number | Common error |
| --- | --- | --- | --- | --- |
| **A** | Calendar hours | 2,080 | Contracted hours × 52. Part-time roles pro-rate here and nowhere else | Using hours *worked*. Planning against 50-hour weeks institutionalises the overrun and hides the deficit |
| **B** | − PTO, public holidays, shutdown | −160 | The actual policy from HR, plus the country's public holidays, plus any company shutdown | Using the statutory minimum when the policy is more generous, or ignoring that a global team has different holiday counts by country |
| **C** | − Sick and unplanned absence | −40 | Trailing-12-month HR actuals, per team | Setting it to zero. It is never zero, and pretending otherwise transfers the error to the CSM |
| **D** | **= Paid working hours** | **1,880** | A − B − C | — |
| **E** | − Internal load | −627 | §3 — a four-week calendar audit. Default is one third of D `[P]` | Counting only meetings. Note-writing, CRM upkeep and interview loops are the largest unlogged internal costs |
| **F** | **= Customer-facing hours** | **1,253** | D − E | — |
| **G** | × Realisation factor | × 0.85 | §3.3 — measure locally `[P]` | Applying it twice: padded estimates *and* a factor |
| **H** | **= Effective customer hours per FTE per year** | **≈1,065** | F × G | Publishing F as capacity and treating the shortfall as an individual performance issue |

**H is the denominator for every ratio in this library.** A CSM has roughly a thousand customer
hours a year. Every cadence entitlement, every business review, every escalation is a claim on that
number, and the sum of the claims either fits or it does not.

**Line H per week.** With 46 working weeks (52 − 4 PTO − 2 holiday/shutdown), H ÷ 46 ≈ **23 hours a
week of effective customer time**. If a weekly plan routinely allocates much more than that, line E
is under-counted.

---

## 2. Loaded cost per hour

```
C (loaded annual cost) = OTE × loading factor
c (per customer hour)  = C ÷ H
```

| Input | Default | Source |
| --- | --- | --- |
| CSM OTE, US | $140,000 (median base $105,000) | RepVue self-reported panel, Aug 2026 `[M — self-reported, no disclosed sampling method]` |
| Loading factor | 1.25–1.40 | Employer tax, benefits, tooling seats, workspace, management overhead `[P]` |
| H | 1,065 | §1 |

At OTE $140,000 and a 1.30 loading factor: **C = $182,000**, **c ≈ $171 per customer-facing hour**.

Substitute your own comp band and loading factor before using this externally. The number that
matters is not $171, it is that **you have one at all** — without it, every cadence debate is
conducted in hours, which nobody outside CS can price.

---

## 3. Auditing internal load

### 3.1 The four-week calendar audit

Four consecutive weeks, every CSM in the segment (or a random 5, whichever is smaller). Export the
calendar and classify every block:

| Bucket | Includes | Goes to |
| --- | --- | --- |
| **Customer-facing** | Any block where a customer is present, plus the prep, follow-up and write-up attached to it | D − E, i.e. counted in F |
| **Internal recurring** | 1:1s, team meetings, forecast calls, pipeline review, enablement, all-hands, on-call handover | E |
| **Internal ad hoc** | Deal reviews, escalation stand-ups without the customer, product feedback sessions | E |
| **Administrative** | CRM and CS-platform upkeep, notes not attached to a specific call, expenses, tooling | E |
| **Hiring** | Interview panels, debriefs, scorecards | E |
| **Unclassifiable** | Focus blocks, "work time" | Split by asking; do not assume |

Then: `E = (internal hours in 4 weeks ÷ 4) × 46`.

**Expect the audit to surprise you upward.** Calendar-invisible work — notes, CRM hygiene, Slack —
is the largest under-count. Add a one-question daily log for the audit period ("hours today on work
with no calendar entry and no customer present") and include it in E.

### 3.2 What does not belong in E

| Item | Where it goes | Why |
| --- | --- | --- |
| PTO and holidays | Line B | Annualising them into E hides which weeks are short |
| Travel time | Attached to the motion it serves, in F | An onsite is not a 60-minute meeting |
| Post-incident war rooms with the customer present | F | It is customer work, however unwelcome |
| Post-incident internal reviews | E | It is not |
| Training and certification | E if recurring; a one-off project line if not | — |

### 3.3 Measuring the realisation factor

```
Realisation factor = Σ hours of planned work actually completed ÷ Σ hours planned for it,
                     over the trailing 4 weeks
```

Count an item complete only if its success measure was recorded; a call that happened but was never
logged did not deliver the motion.

| Observed | Reading | Action |
| --- | --- | --- |
| ≥0.90 | Estimates are padded, or the plan is under-filled | Tighten estimates; allocate more |
| 0.80–0.89 | Normal for a named book | Use the measured value |
| 0.65–0.79 | Fragmentation is eating the week | Consolidate into longer blocks; move internal load off them |
| <0.65 | The plan is decorative | Stop tuning the factor; the book is structurally oversized |

**Why 0.85 is a default and not a finding.** The underlying loss is well measured — Microsoft's 2025
Work Trend Index (M365 telemetry through 15 Feb 2025 plus a 31,000-respondent survey across 31
markets) found interruptions **every two minutes during core hours**, **117 emails and 153 chat
messages per weekday**, **57% of meetings ad hoc**, and **48% of employees describing their work as
chaotic and fragmented** `[M]`. Gloria Mark's UC Irvine interruption research is the standard
academic reference for resumption lag `[A, via secondary summaries]`. None of that yields 0.85. It
yields "the loss is real and material". Write "commonly set at 0.85 `[P]`", never "research shows".

---

## 4. Role variants

Lines E and G are not constants across roles. Recompute when the **role** changes, not when the book
changes.

| Role | E (annual) | G | H | Notes |
| --- | --- | --- | --- | --- |
| **Named enterprise CSM** | 627 | 0.85 | 1,065 | Meeting-heavy; scheduled motions dominate |
| **Named mid-market CSM** | 627 | 0.85 | 1,065 | The library default |
| **Pooled CSM** | 560 | 0.85 | 1,122 | Fewer forecast calls; far higher reactive share within F. Pass this to `../scripts/capacity.py` as `effective_hours_override` on the segment |
| **Digital / programme owner** | 750 | 0.88 | 961 | E is higher because content, automation upkeep and journey QA are internal work. Their F goes to programme building, not accounts |
| **Player-coach (0.5 management)** | 940 | 0.85 | 799 | Do not assign a full named book against this H |
| **New hire, months 0–3** | 1,130 | 0.80 | 600 | Ramp, shadowing and enablement are the job |
| **New hire, months 4–6** | 800 | 0.82 | 886 | — |
| **On-call rotation week** | +8 h that week | 0.75 that week | — | Treat as a reactive week; do not plan high-return work into it |

Values `[P]`, derived by adjusting the default profile. Measure your own; the *shape* is the point —
a player-coach has roughly 75% of a CSM's customer hours, and a first-quarter hire has roughly 56%.

---

## 5. The motion catalogue by segment

Hours are **end to end** — pull, prep, delivery, follow-up, write-up. Per-motion durations come from
`../../book-of-business-triage/references/play-durations.md`; this table is the annual *entitlement*
each segment consumes, before the complexity multiplier.

| Motion | Instances/yr | Hours each | Enterprise | Mid-Market | Growth | Scale (pooled) |
| --- | --- | --- | --- | --- | --- | --- |
| Executive business review | ent 4 · mm 2 · gr 1 · sc 0 | 8.0 | 32.0 | 16.0 | 8.0 | 0 |
| Operational cadence call | ent 8 · mm 4 · gr 2 · sc 0 | 1.25 | 10.0 | 5.0 | 2.5 | 0 |
| Success-plan refresh | ent 4 · mm 2 · gr 1 · sc 0 | 2.0 | 8.0 | 4.0 | 2.0 | 0 |
| Renewal motion | 1 | ent 5.5 · mm 3.0 · gr 3.0 · sc 0.5 | 5.5 | 3.0 | 3.0 | 0.5 |
| Async value snapshot | ent 2 · mm 2 · gr 2 · sc 4 | 1.25 · sc 0.3 | 2.5 | 2.5 | 2.5 | 1.2 |
| Stakeholder mapping refresh | ent 2 · mm 1 · gr 0 · sc 0 | 1.5 | 3.0 | 1.5 | 0 | 0 |
| Product-feedback submission | ent 4 · mm 2 · gr 1 · sc 0 | 0.5 | 2.0 | 1.0 | 0.5 | 0 |
| **Scheduled subtotal** | | | **63.0** | **33.0** | **18.5** | **1.7** |
| Reactive (§6) | | | 12.0 | 6.0 | 4.0 | 2.0 |
| Onboarding amortised (§7) | | | 6.7 | 3.2 | 1.6 | 0.4 |
| **Base required h/account/yr** | | | **81.7** | **42.2** | **24.1** | **4.1** |

All instance counts and hour values `[P]`. **Replace the entitlement column with your own published
tier commitments before running this** — the entitlement is a policy decision, not a benchmark, and
copying this table is the same error as copying a ratio.

Apply the complexity multiplier last: `required = base × complexity_multiplier`
(`segmentation.md` §2.3). An enterprise segment with a mean complexity score of 2.4 carries a
multiplier of 1.30 and therefore **106.2 hours per account per year**.

---

## 6. Reactive hours from actuals

Reactive work is not an estimate if you have ticket and interaction data.

```
Reactive hours per account per year ≈
      ( tickets_12m × mean CSM minutes per ticket )
    + ( escalations_12m × mean CSM hours per escalation )
    + ( unscheduled interactions_12m × mean hours per interaction )
```

| Input | How to get it | Default `[P]` |
| --- | --- | --- |
| Mean CSM minutes per ticket | Time-tracking if available; otherwise a two-week sample where CSMs log it | 12 min for tickets the CSM touches; most tickets never reach a CSM — count only those that do |
| Mean CSM hours per escalation | Sample the last 10 escalations end to end | 9.0 h first week, 2.0 h per additional week open |
| Unscheduled interactions | `interaction` rows not linked to a scheduled motion | 0.4 h each |

**Size the segment's reserve at the P75, not the mean.** The cost of under-sizing is asymmetric:
under-size it and every busy quarter destroys the plan; over-size it and some capacity goes
unallocated, which the weekly triage reclaims. And check the distribution — reactive load is usually
concentrated, with a small number of accounts generating most of it. If the top decile carries more
than half the reactive hours, that is a **complexity-index finding**, not a capacity finding, and it
belongs in book assignment.

---

## 7. Book size, and three worked examples

```
Sustainable accounts per CSM = H ÷ required hours per account per year
Sustainable ARR per CSM      = that × mean ARR per account
Required FTE (segment)       = accounts in segment ÷ sustainable accounts per CSM
Onboarding amortisation      = ( onboarding hours × new accounts/yr ) ÷ accounts in segment
```

### 7.1 Enterprise, named

Inputs: 48 accounts, $32.0M ARR (mean $667k), complexity mean 2.4 → ×1.30, onboarding 40 h,
8 new accounts/year, H = 1,065.

```
Onboarding amortised = (40 × 8) ÷ 48                      = 6.7 h
Base required        = 63.0 + 12.0 + 6.7                  = 81.7 h
With complexity      = 81.7 × 1.30                        = 106.2 h
Sustainable accounts = 1,065 ÷ 106.2                      = 10.0
Sustainable ARR/CSM  = 10.0 × 667,000                     = $6.7M
Required FTE         = 48 ÷ 10.0                          = 4.8
Cost to serve        = 106.2 × $171                       = $18,160 per account
                     = $18,160 ÷ $667,000                 = 2.7% of segment ARR
```

Verdict: **servable at 4.8 FTE**, and 2.7% cost-to-serve sits comfortably inside an 81% gross margin
`[Benchmarkit 2025, CY2024 · M]`. If current staffing is 4.0 FTE, the deficit is 0.8 FTE — carry that
into `headcount-case.md`.

### 7.2 Mid-market, named

Inputs: 210 accounts, $18.9M ARR (mean $90k), complexity mean 1.6 → ×1.20, onboarding 20 h,
34 new accounts/year.

```
Onboarding amortised = (20 × 34) ÷ 210                    = 3.2 h
Base required        = 33.0 + 6.0 + 3.2                   = 42.2 h
With complexity      = 42.2 × 1.20                        = 50.6 h
Sustainable accounts = 1,065 ÷ 50.6                       = 21.0
Sustainable ARR/CSM  = 21.0 × 90,000                      = $1.9M
Required FTE         = 210 ÷ 21.0                         = 10.0
Cost to serve        = 50.6 × $171 = $8,653  →  9.6% of the $90k mean ARR
```

Verdict: 10.0 FTE required. If the team is 6, the deficit is 4.0 FTE — and 9.6% cost-to-serve on
this segment is already at the edge of what SaaS Capital's 9%-of-ARR CS-plus-support median implies
for a *whole* base `[M]`. That is the signal that the mid-market entitlement is too rich for the
ACV, and the honest options are: cut the entitlement, raise the price, or move the bottom of the
segment to pooled. All three belong in the options table; none of them is "work harder".

### 7.3 Scale, pooled

Inputs: 1,240 accounts, $14.9M ARR (mean $12k), 3 pooled CSMs, pooled H = 1,122.

```
Required h/account   = 4.1 (no complexity uplift applied at this tier)
Sustainable accounts = 1,122 ÷ 4.1                        = 274 per pooled CSM
Capacity at 3 FTE    = 823 accounts
Shortfall            = 1,240 − 823                        = 417 accounts, ≈ $5.0M ARR
Required FTE         = 1,240 ÷ 274                        = 4.5   → gap 1.5 FTE
```

Verdict: **structurally short by 1.5 FTE, or 417 accounts need a genuine digital programme.** The
honest arithmetic is the pooled sweep cycle: at the maintenance share of pooled hours, a full
proactive sweep of 413 accounts per CSM takes months, not weeks. Publish the cycle time and promise
that cadence — see `coverage-models.md` §4. Promising monthly proactive contact on this book is
named-CSM cosplay, and customers discover it within one cycle.

---

## 8. Sensitivity

Vary one input ±10%, hold the rest, and record the effect on book size and required FTE. Whatever
moves most is what you measure first — this table is a measurement plan, not decoration.

Worked on the mid-market example (baseline 21.0 accounts/CSM, 10.0 FTE):

| Input varied | At −10% | At +10% | Book-size swing | Priority to measure |
| --- | --- | --- | --- | --- |
| **Complexity multiplier** | 23.4 acc · 9.0 FTE | 19.1 acc · 11.0 FTE | **20.2%** | **1st** — the largest single swing, and the input most often assumed rather than computed |
| **Realisation factor (G)** | 18.9 acc · 11.1 FTE | 23.1 acc · 9.1 FTE | **20.0%** | **2nd** — hardest to measure honestly; label it a default until you have four weeks |
| **Internal load (E)** | 22.1 acc · 9.5 FTE | 20.0 acc · 10.5 FTE | 10.0% | 3rd — cheapest to measure, since a calendar audit settles it in four weeks |
| **EBR hours (8.0 each, 2/yr)** | 21.8 acc · 9.6 FTE | 20.2 acc · 10.4 FTE | 7.6% | 4th — one motion, easy to time, and entitlement is a policy lever you control |
| **Reactive hours** | 21.3 acc · 9.9 FTE | 20.7 acc · 10.1 FTE | 2.9% | 5th — computable from ticket data you already hold |
| **Onboarding volume** | 21.2 acc · 9.9 FTE | 20.9 acc · 10.1 FTE | 1.6% | 6th |

The lesson generalises: **the complexity multiplier and the realisation factor dominate, and both
are the inputs teams assume rather than measure.** Timing the number of EBRs precisely while
guessing the complexity multiplier is measuring the wrong thing carefully.

`../scripts/capacity.py` runs this sweep across all segments automatically and prints the range.

Always report the model as a **range**, not a point: "10.0 FTE required, 9.0–11.1 across the
sensitivity band, driven mainly by complexity and realisation, neither of which we have measured."

---

## 9. The multi-period model

Books are not static. Project forward for the planning year:

```
Accounts(t)      = Accounts(t−1) + new logos(t) − churned logos(t)
Required FTE(t)  = Σ over segments [ Accounts_segment(t) ÷ sustainable accounts per CSM ]
Available FTE(t) = current − attrition(t) + hires reaching productivity by t
Gap(t)           = Required FTE(t) − Available FTE(t)
```

| Input | Where it comes from | Note |
| --- | --- | --- |
| New logos | Sales plan by segment | Use the plan, and also the trailing-12-month actual. Show both |
| Churned logos | Trailing-12-month logo retention by segment | Logo, not dollar — headcount is driven by account count |
| CSM attrition | HR trailing 24 months | Never zero. Backfills need the same ramp allowance as growth hires |
| Hire ramp | `headcount-case.md` §3 | A hire starting in month 9 contributes almost nothing to that year |

**The lag is the point.** A hire approved in November who starts in February and ramps over six
months contributes roughly a third of an FTE to that calendar year. Headcount asks that ignore the
lag arrive exactly one planning cycle too late, every cycle.

---

## 10. Anti-patterns

| Anti-pattern | Correction |
| --- | --- |
| Planning against 2,080 hours | Plan against H ≈ 1,065 |
| Setting E from a convention and never auditing it | Four-week calendar audit; E is the input with the second-largest swing |
| Costing motions at invite length | End-to-end duration including pull, prep, follow-up and write-up |
| Assuming hours scale with ARR | Apply the complexity multiplier; it is the single largest sensitivity |
| Applying the realisation factor twice | Honest estimates × a measured factor. Pick one |
| Copying the motion catalogue in §5 as if it were a benchmark | Replace it with your own published entitlements; it is a policy decision |
| A point estimate for required FTE | Report the sensitivity range and name the two drivers |
| Ignoring ramp in the headcount plan | A February hire delivers roughly a third of a year; model it |
| Reusing this file for a CSM's weekly plan | Different grain; use `../../book-of-business-triage/references/capacity-model.md` |
| Treating reactive load as uniform across accounts | Check the distribution; concentration is a complexity finding for book assignment |
| Quoting $171 per hour externally without substituting local comp | Recompute C and c from your own bands |

---

## 11. Evidence register

| Claim | Value | Source | Year | Label |
| --- | --- | --- | --- | --- |
| Interruptions every 2 minutes in core hours · 117 emails and 153 chat messages per weekday · 57% of meetings ad hoc · 48% describe work as chaotic and fragmented | as stated | Microsoft Work Trend Index — M365 telemetry through 15 Feb 2025 plus a 31,000-respondent survey across 31 markets | 2025 | `[M]` |
| Resumption lag after interruption ≈ half an hour | as stated | Gloria Mark, UC Irvine, via widely cited secondary summaries | 2005–2008 | `[A]`, secondary |
| CSM compensation | $105,000 median base · $140,000 median OTE, US | RepVue self-reported panel | Aug 2026 | `[M]`, self-reported |
| Subscription gross margin | 81% median (total 77%, professional services 30%) | Benchmarkit 2025 SaaS Performance Metrics, CY2024 | 2025 | `[M]` |
| CS + Support spend | 9% of ARR median; 10% at $3–5M ARR | SaaS Capital, *2026 Spending Benchmarks*, Mar 2026, 1,000+ companies | 2026 | `[M]` |
| ARR per FTE, company-wide | $193k median; $200k at $50–100M ARR; $300k above $100M | 2026 Aleph × Benchmarkit, CY2025 | 2026 | `[M]` |
| Revenue per employee | $141,125 median (prior year $129,724) | SaaS Capital 2026, 1,000+ companies | 2026 | `[M]` |
| Lines A–H defaults, role variants, motion catalogue, reactive defaults, loading factor, realisation factor 0.85 | as stated | Practitioner convention used by this library | — | `[P]` |
| Play durations | see file | `../../book-of-business-triage/references/play-durations.md` | — | `[P]` |

**Never present a `[P]` value as a benchmark.** Write "commonly set at 0.85", not "research shows
0.85". And no accounts-per-CSM benchmark appears here: the point of this file is that the number is
computed, not looked up.
