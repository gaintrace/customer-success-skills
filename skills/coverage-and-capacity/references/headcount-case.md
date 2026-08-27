# The Headcount Case

> How to ask for CSM headcount in a way a CFO can approve: what the hire actually costs, how much
> capacity it delivers in year one, how many points of retention it has to buy to pay for itself,
> and the three alternatives that must be priced next to it. Read in budget season, on any
> resignation, and before any conversation that starts "we need more people".
>
> Evidence labels: `[M]` measured with a named study · `[V]` vendor or first-party operating model ·
> `[P]` practitioner convention · `[A]` academic.

**Contents**
1. [What is actually being decided](#1-what-is-actually-being-decided)
2. [The cost of a CSM](#2-the-cost-of-a-csm)
3. [Ramp, and year-one delivered capacity](#3-ramp-and-year-one-delivered-capacity)
4. [Cash break-even and value break-even](#4-cash-break-even-and-value-break-even)
5. [Worked: enterprise vs mid-market](#5-worked-enterprise-vs-mid-market)
6. [Counting expansion, honestly](#6-counting-expansion-honestly)
7. [The four options, priced](#7-the-four-options-priced)
8. [Solve for the indifference point](#8-solve-for-the-indifference-point)
9. [Quantifying do-nothing](#9-quantifying-do-nothing)
10. [The memo](#10-the-memo)
11. [CFO objections and the answers](#11-cfo-objections-and-the-answers)
12. [Anti-patterns](#12-anti-patterns)
13. [Evidence register](#13-evidence-register)

---

## 1. What is actually being decided

Not "does CS deserve more people". The CFO is deciding between four uses of the same money, and the
CS case loses by default when it arrives as one option with an emotional argument attached.

Three framing errors sink most CS headcount asks:

| Error | Why it fails | Fix |
| --- | --- | --- |
| Arguing from workload | Every function is busy. Busy is not a budget argument | Argue from retained gross margin and protected ARR |
| One option, no alternatives | Reads as special pleading, and invites the CFO to invent the alternatives themselves — badly | Present four costed options, recommend one |
| Conflating cash and value break-even | The two differ by roughly an order of magnitude; being caught mixing them ends the meeting | State both, name the one the case rests on |

Timing matters as much as content. Kristen Hayer's published planning calendar puts customer-data
review in July, tools in August, metrics and goals in September, hiring and comp in October, budget
in November, and communication in December `[P — practitioner operating calendar]`. A headcount case
that arrives in January is arguing about a number that was set in November.

---

## 2. The cost of a CSM

```
C = OTE × loading factor
```

| Component | Default | Note |
| --- | --- | --- |
| OTE | $140,000 (median base $105,000) | RepVue self-reported US panel, Aug 2026 `[M — self-reported, no disclosed sampling method]`. Use your own band; geography moves this 30%+ |
| Loading factor | **1.30** (range 1.25–1.40) `[P]` | Employer tax and benefits, tooling seats, workspace, recruiting amortisation, management overhead |
| **C** | **$182,000** | |
| Effective customer hours, H | 1,065 | `capacity-math.md` §1 |
| **Loaded cost per customer hour, c** | **≈$171** | The number that prices every cadence decision |

Get the loading factor from Finance rather than assuming it. Asking is also a tactic: a case built on
Finance's own cost basis is much harder to argue with than one built on yours.

---

## 3. Ramp, and year-one delivered capacity

A hire is not an FTE on day one, and a case that pretends otherwise gets corrected in the meeting.

```
Year-1 delivered capacity  = (R ÷ 12) × p̄ + (12 − R) ÷ 12
Year-1 cost per delivered FTE = C ÷ that fraction
```

| Input | Default `[P]` | Basis |
| --- | --- | --- |
| R — months to full productivity | 6 | Named mid-market or enterprise coverage. Practitioner convention; measure yours from the last five hires |
| p̄ — mean productivity across the ramp | 0.45 | Consistent with the role variants in `capacity-math.md` §4 (≈0.56 of H in months 0–3, ≈0.83 in months 4–6) |

At R = 6, p̄ = 0.45: **year-1 delivered capacity = 0.725 FTE**, so **year-1 cost per delivered FTE =
$182,000 ÷ 0.725 = $251,034**.

| Variant `[P]` | R | p̄ | Year-1 delivered | Year-1 cost / delivered FTE |
| --- | --- | --- | --- | --- |
| Pooled or digital hire (playbook-driven) | 3 | 0.55 | 0.89 | $204,494 |
| Named mid-market | 6 | 0.45 | 0.725 | $251,034 |
| Named enterprise / regulated / multi-product | 9 | 0.40 | 0.55 | $330,909 |
| Internal transfer from support or sales | 8 | 0.50 | 0.667 | $272,864 |
| External hire with same-vertical CS experience | 4 | 0.55 | 0.85 | $214,118 |

**Two things this table pays for.** First, hiring earlier in the year is worth real money — a hire
starting in month 9 delivers roughly 0.08 FTE that year. Second, the ramp variance across hire
profiles is larger than most comp differences, which is a recruiting argument as much as a finance
one.

**Backfills carry the same ramp.** A resignation costs the ramp again, plus the handover cost of
8–12 hours per account `[P]`. On a 21-account mid-market book that is 170–250 hours of pure
rediscovery, roughly $29,000–43,000 at $171/hour, before any capacity gap. Attrition is a capacity
input, not an HR footnote.

---

## 4. Cash break-even and value break-even

Two different questions. Both belong in the memo; the case rests on one of them.

```
Cash break-even  (GRR pp) = C ÷ ( ARR covered × subscription gross margin )
Value break-even (GRR pp) = C ÷ ( ARR covered × ARR multiple )
```

| | Cash break-even | Value break-even |
| --- | --- | --- |
| **Question** | Do the gross-margin dollars protected this year exceed the salary this year? | Does the recurring ARR protected, at the company's valuation multiple, exceed the salary? |
| **Uses** | Subscription gross margin — 81% median `[Benchmarkit 2025, CY2024 · M]` | The company's own ARR multiple, from Finance. Never a market average |
| **Right for** | Cash-constrained companies, profitability targets, bootstrapped businesses | Growth-stage companies where retained ARR compounds into enterprise value |
| **Failure** | Understates a CSM's value: retained ARR recurs, salary does not | Overstates it: enterprise value is not payroll |

**Both are year-one framings by default.** In steady state, replace `C` with `C` and the delivered
capacity with 1.0; for year one, use the year-1 cost per delivered FTE from §3 and say which you
used. A memo that silently mixes the two is the one that gets sent back.

---

## 5. Worked: enterprise vs mid-market

Using the book sizes from `capacity-math.md` §7, C = $182,000, year-1 cost $251,034, gross margin
81% `[M]`, and an ARR multiple of 5× taken from Finance.

| | Enterprise | Mid-market |
| --- | --- | --- |
| ARR under coverage per CSM | $6,688,000 | $1,891,000 |
| Gross-margin dollars covered | $5,417,000 | $1,532,000 |
| **Cash break-even, steady state** | **3.4 GRR pp** | **11.9 GRR pp** |
| **Cash break-even, year 1** | **4.6 GRR pp** | **16.4 GRR pp** |
| **Value break-even at 5× ARR** | **0.5 GRR pp** | **1.9 GRR pp** |
| Value break-even, year 1 | 0.8 GRR pp | 2.7 GRR pp |

Reproduce with `python3 ../scripts/capacity.py ../scripts/sample_org.json`.

Read this carefully, because it is the most useful table in the file.

1. **The enterprise hire is defensible on either framing.** Half a point of GRR on a $6.7M book is
   a plausible claim; 3.4 points is ambitious but arguable.
2. **The mid-market hire is not defensible on cash.** Nobody moves GRR by 11.9 points by adding one
   CSM, and claiming it destroys the credibility of everything else in the memo. On value it needs
   1.9 points, which is arguable — so **the mid-market case must be argued on value, and you must
   say so**.
3. **If neither framing works, the answer is not a hire.** It is a coverage-model change, a price
   change, or a raised segment floor. Say that out loud; proposing it yourself is what makes the
   rest of the memo credible.

For context on the size of the retention numbers being moved: the 2026 Aleph × Benchmarkit
benchmarks (CY2025 data) put private B2B SaaS **GRR at an 84% median, 91% at the 75th percentile and
76% at the 25th** `[M]`. A claim to move GRR by several points is a claim to move a quartile.

---

## 6. Counting expansion, honestly

A CSM who sources expansion adds revenue as well as protecting it. Count it only under three
conditions, all required:

1. The company **credits expansion to a source** and the CSM appears as that source in the CRM.
2. There is **at least four quarters of history** for CSM-sourced expansion in this segment.
3. You report the **conversion rate**, not the pipeline. Sourced opportunities are not revenue.

```
Expansion ARR needed to cover cash cost = C ÷ subscription gross margin
                                        = $182,000 ÷ 0.81 = $224,691
```

On a $1.9M mid-market book that is **11.8% net expansion in-year from one CSM's sourcing**, which is
a high bar. On a $6.7M enterprise book it is **3.4%** — plausible. Expansion is a real part of the
case at enterprise and a weak one at mid-market, and the arithmetic says so before anyone's opinion
does.

If the three conditions are not met, write `UNKNOWN — requires source-credited expansion history`
and build the case on retention alone. Inventing an expansion contribution is the single fastest way
to lose the next headcount argument as well as this one.

---

## 7. The four options, priced

Every case carries these four, costed identically. Recommend one.

| # | Option | Cost | Capacity effect | Retention effect | Risk introduced |
| --- | --- | --- | --- | --- | --- |
| 1 | **Hire** N CSM | `N × C`, plus ramp | `N × year-1 delivered` this year, `N` thereafter | The break-even points from §4 | Ramp lag; a bad hire costs a year |
| 2 | **Automate** a named process | Tooling + implementation hours | Hours returned ÷ H = FTE equivalent | Neutral if the process is genuinely mechanical | Automating a process that was carrying judgement |
| 3 | **Move a tier down a model** | $0 direct; releases FTE | (hours before − hours after) × accounts ÷ H | Estimated GRR loss on that cohort — **or the indifference point, §8** | Silent abandonment; a cohort that stops asking |
| 4 | **Do nothing** | $0 | 0 | §9 | Touch coverage falls; uncovered ARR renews |

**Option 2 must name the process and show the hours.** "AI will make us more efficient" is not an
option, it is a hope. A real version:

> Business-review deck assembly currently takes 2.5 hours per review; the mid-market tier runs 2
> reviews per account per year across 210 accounts = **1,050 hours = 0.99 FTE at H = 1,065**.
> Automating data assembly (leaving narrative and recommendations with the CSM) removes an estimated
> 70% of that: **735 hours = 0.69 FTE**, against tooling of $X and 80 hours of implementation.

**Option 3 must show the released capacity in FTE.** A real version:

> The 70 mid-market accounts below $40k ARR ($2.1M total) move from named (50.6 h/account/yr) to
> pooled (4.1 h). Released: `70 × 46.5 = 3,255 hours = 3.06 FTE`, against a GRR risk on $2.1M of ARR
> that we have not measured — see §8 for what that loss would have to be before this option is worse
> than the hire.

---

## 8. Solve for the indifference point

You will usually not have a measured estimate of what pooling a cohort costs in retention. **Do not
guess it.** Solve for the value at which the decision flips, and hand the CFO the question instead
of a fabricated answer.

```
Indifference GRR loss = ( cost of the option you are comparing against )
                        ÷ ( cohort ARR × subscription gross margin )
```

Worked, comparing "hire 1 CSM" against "pool the bottom 70 mid-market accounts":

```
Indifference = $182,000 ÷ ( $2,100,000 × 0.81 )
             = $182,000 ÷ $1,701,000
             = 10.7 GRR percentage points
```

**Pooling this cohort would have to cost more than 10.7 points of GRR before it is worse than one
hire** — and pooling releases 3.06 FTE, not one. Stated that way the decision is obvious, it is
honest about what is unknown, and it hands the CFO a question they can actually answer: *do we
believe moving sub-$40k accounts to a pooled model costs more than ten points of retention?*

Then commit to measuring it: cohort the moved accounts, track GRR against a matched cohort that
stayed named, and report at two and four quarters. That commitment is what converts an assumption
into evidence for next year's case — and it is the difference between a team that argues from
benchmarks forever and one that argues from its own history.

---

## 9. Quantifying do-nothing

Do-nothing is never free, and it is the option the memo must price most carefully, because it is
the one that happens by default.

| Consequence | How to quantify it |
| --- | --- |
| Touch coverage decays | Project accounts-with-a-bilateral-touch-in-90d forward at the current required-vs-available ratio. State the date it crosses 70% `[P]` |
| Uncovered ARR renews | Sum ARR whose **opt-out deadline** (`renewal_date − notice_period_days`) falls before that date, among accounts that will not be touched |
| Entitlements go undelivered | Business reviews owed minus deliverable at current capacity, ARR-weighted |
| Risk work goes unworked | At-risk ARR (from `churn-risk`) in the segments with the deficit, and the share that will reach its opt-out date without an intervention |
| Attrition of the team itself | Sustained overload has a resignation cost: ramp again, plus 8–12 hours per account of handover `[P]` |

Write it as a dated sentence, not an adjective:

> Without a change, mid-market touch coverage falls below 70% by 2026-11-15 on current trend. **$4.1M
> of ARR sits in the untouched set, of which $900,000 passes its opt-out deadline before 2027-01-31.**
> Two of those accounts are already At Risk, totalling $310,000.

---

## 10. The memo

```markdown
# Coverage capacity — decision required by <date>
**To:** <CFO / CRO> · **From:** <name> · **Date:** <date>

**Ask:** <one sentence — headcount, a coverage-model change, or a budget reallocation.>

| | |
|---|---|
| Segment(s) | <name> · <N> accounts · $<ARR> |
| Effective customer hours per FTE (line H) | <H> — <measured / labelled default> |
| Required hours | <X> · available <Y> · **deficit <Z> h/yr = <F> FTE** |
| Sensitivity range on the deficit | <F_low> – <F_high> FTE, driven by <the two largest inputs> |
| Touch coverage today | <Y>% (threshold 70%) · trailing 90 days |
| Uncovered ARR | $<X>, of which $<Y> renews inside 180 days |
| Earliest opt-out deadline in the uncovered set | <date> |
| **Decision needed by** | <date — tied to that opt-out deadline> |

## What is not happening
| Work owed | Owed per year | Delivered TTM | Gap | ARR affected |
|---|---|---|---|---|

## The arithmetic
| | |
|---|---|
| Fully loaded cost per CSM | $<C> (OTE $<x> × <loading>) — basis: <Finance / assumption> |
| Year-1 delivered capacity per hire | <fraction> (ramp <R> months at <p̄>) → $<Y1 cost> per delivered FTE |
| ARR under coverage per CSM in this segment | $<X> |
| Cash break-even | <X.X> GRR pp steady state · <Y.Y> pp year 1 |
| Value break-even at <multiple>× ARR | <X.X> pp steady state · <Y.Y> pp year 1 |
| **This case rests on** | <cash / value> — <one sentence why> |
| Evidence for the retention gain | <cohort comparison, prior coverage change, or `UNKNOWN — requires a backtest`> |

## Options
| # | Option | Cost | Capacity effect | Retention effect | Risk |
|---|---|---|---|---|---|
| 1 | Hire <N> CSM | | | | |
| 2 | Automate <named process, with the hours shown> | | | | |
| 3 | Move <cohort> to <model> | $0; releases <F> FTE | | Indifference point: <X.X> GRR pp | |
| 4 | Do nothing | $0 | 0 | | <dated consequence> |

**Recommendation:** <option>, because <the number it rests on>.

**What we will measure to prove or disprove this:** <cohort, metric, review dates at 2 and 4 quarters.>

### Assumptions
| # | Assumption | Why it was needed | If wrong |
|---|---|---|---|
```

---

## 11. CFO objections and the answers

| Objection | Weak answer | Strong answer |
| --- | --- | --- |
| "Everyone says they're short-staffed" | "Our books are bigger than the benchmark" | "Here is line H, here are the required hours, here is the deficit and its sensitivity range. The benchmark is not part of the argument" |
| "Can't AI absorb this?" | "Partly" | "Yes, for <named process> — that is option 2, worth <F> FTE at a tooling cost of $<X>. It does not absorb <the judgement work>, which is where the deficit is" |
| "What's the ROI?" | "Better retention" | "Cash break-even is <X> GRR points, value break-even is <Y>. This case rests on <which>, and here is the evidence for the gain — or here is the explicit statement that we do not have it yet" |
| "Why not just use the cheaper model?" | "Quality would suffer" | "That is option 3 and it releases <F> FTE. It becomes worse than the hire only if it costs more than <indifference> GRR points, and we have committed to measuring that" |
| "Prove the last hire paid for itself" | Anecdote | Cohort comparison: the accounts that gained coverage against a matched cohort that did not, at two and four quarters. If you never set it up, say so and set it up now |
| "Take it from next year's budget" | Acceptance | "Then the decision date is <opt-out deadline>. $<X> of ARR renews before a hire starting in <month> reaches productivity" |
| "Your ratio looks fine against industry" | Defensiveness | "There is no current public benchmark for accounts-per-CSM with a disclosed sample and date. Ours is computed — here is the derivation" |

---

## 12. Anti-patterns

| Anti-pattern | Correction |
| --- | --- |
| Asking on workload | Argue in retained gross margin and protected ARR |
| One option | Four, priced identically, with a recommendation |
| Ignoring ramp | Year-1 delivered capacity and cost per delivered FTE |
| Mixing cash and value break-even | State both, name the one the case rests on |
| Guessing what pooling costs in retention | Solve for the indifference point and commit to measuring it |
| Counting expansion with no source-credit history | `UNKNOWN — requires source-credited expansion history` |
| Do-nothing priced at zero | A dated consequence with ARR and an opt-out deadline attached |
| A point estimate for the deficit | A range with the two dominant sensitivities named |
| Quoting an accounts-per-CSM benchmark as support | It has no current source with a disclosed sample; derive the number instead |
| Arriving in January | The budget was set in November; work the planning calendar |
| No measurement plan | Name the cohort, the metric and the review dates before the money is spent |

---

## 13. Evidence register

| Claim | Value | Source | Year | Label |
| --- | --- | --- | --- | --- |
| CSM compensation | $105,000 median base · $140,000 median OTE, US | RepVue self-reported panel | Aug 2026 | `[M]`, self-reported |
| Subscription gross margin | 81% median | Benchmarkit 2025 SaaS Performance Metrics, CY2024, N=76 | 2025 | `[M]` |
| GRR distribution | 84% median · P75 91% · P25 76% | 2026 Aleph × Benchmarkit, CY2025, N=226 | 2026 | `[M]` |
| NRR median | 101–102% | 2026 Aleph × Benchmarkit, CY2025 | 2026 | `[M]` |
| CS + Support spend | 9% of ARR median; equity-backed ≈2× bootstrapped | SaaS Capital, *2026 Spending Benchmarks*, Mar 2026, 1,000+ companies | 2026 | `[M]` |
| ARR per FTE, company-wide | $193k median; $300k above $100M ARR | 2026 Aleph × Benchmarkit, CY2025 | 2026 | `[M]` |
| Fuller post-sale role coverage correlates with higher NRR (≈98–99% vs 90–94%) | as stated | Customer Revenue Leadership Study — Pavilion / 6sense, ~800 customer and post-sales leaders | Oct 2025 | `[M]`, correlational |
| Annual planning calendar (data July · tools August · metrics September · hiring October · budget November) | as stated | Kristen Hayer, practitioner operating calendar | — | `[P]` |
| Loading factor 1.25–1.40 · ramp R and p̄ by profile · handover cost 8–12 h/account · touch-coverage floor 70% | as stated | Practitioner convention used by this library | — | `[P]` |

**Deliberately absent:** any accounts-per-CSM or ARR-per-CSM benchmark, and any figure for the
retention gain a CSM produces. No reachable source states either with a disclosed sample and date.
The first is replaced by the derivation in `capacity-math.md`; the second is replaced by the
indifference point in §8 and a commitment to measure it.
