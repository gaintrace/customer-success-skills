# The Headcount and Budget Case

> The arithmetic for a CS hire, the coverage gap it closes, the ARR it protects, the breakeven
> save rate, and the counterfactual you must state before you are asked for it.

**Contents**
1. [The shape of an ask that gets funded](#1-the-shape-of-an-ask-that-gets-funded)
2. [Step 1 — Measure the coverage gap](#2-step-1--measure-the-coverage-gap)
3. [Step 2 — Size the book bottom-up](#3-step-2--size-the-book-bottom-up)
4. [Step 3 — Quantify the ARR the gap exposes](#4-step-3--quantify-the-arr-the-gap-exposes)
5. [Step 4 — The breakeven save rate](#5-step-4--the-breakeven-save-rate)
6. [Step 5 — The honest counterfactual](#6-step-5--the-honest-counterfactual)
7. [Step 6 — The alternatives you must have costed](#7-step-6--the-alternatives-you-must-have-costed)
8. [The one-page ask](#8-the-one-page-ask)
9. [Objections and answers](#9-objections-and-answers)
10. [Worked example](#10-worked-example)
11. [Reference points, with their evidence labels](#11-reference-points-with-their-evidence-labels)

---

## 1. The shape of an ask that gets funded

| Element | Rule | Why |
| --- | --- | --- |
| **One number at the top** | The fully loaded cost and the ARR it protects, in the first line | A CFO is deciding whether to keep reading |
| **A measured gap, not a ratio** | "62 accounts holding $14.2M have no named coverage" beats "we are above the benchmark ratio" | There is no current Grade-A public ARR-per-CSM benchmark — every published range is a CS-platform content aggregation [P]. A ratio argument invites a ratio counter-argument |
| **A claimed effect that is a delta, not a total** | Claim the improvement attributable to coverage, never the whole retained base | Claiming the total is the fastest way to lose the argument |
| **A breakeven stated before the expected case** | "This pays for itself at a 1.9% improvement in GRR on the uncovered book" | Breakeven is falsifiable. Expected case is a forecast, and forecasts are discounted |
| **The counterfactual, unprompted** | What you will do if the answer is no, and what it costs | Conceding the weakest point is what makes the rest credible |
| **A kill criterion** | "If uncovered-book GRR has not moved 150bps by <date>, I will not ask again" | Almost nobody offers this. It converts a spend into an experiment |

---

## 2. Step 1 — Measure the coverage gap

Do not begin with a ratio. Begin with the **ARR coverage waterfall**, which is the number a
board has usually never been shown.

| Coverage tier | Definition | ARR | % of ARR | Accounts | GRR (TTM) |
| --- | --- | ---: | ---: | ---: | ---: |
| Named 1:1 | A specific CSM owns the account and has a cadence | | | | |
| Pooled | A team owns the segment; no individual ownership | | | | |
| Digital / tech-touch | Automated lifecycle only | | | | |
| **Uncovered** | No named owner, no pool, no programme | | | | |

**"Uncovered ARR" is the disclosure.** Then add the second table — the one that turns a
coverage number into a risk number:

| Cut | Question it answers |
| --- | --- |
| Uncovered ARR renewing inside the next two quarters, **by opt-out deadline** | How much of the gap is already time-critical |
| Uncovered ARR in the top-20 by account size | Whether the gap intersects concentration risk |
| Touch coverage: `accounts with a logged meaningful touch in 90d / assigned accounts` | Whether the *named* book is real. Below ~70% in a named tier, the book is oversized regardless of its ARR [P] |
| GRR of covered vs uncovered books, same segment, same period | The empirical basis for the entire ask |

That last row is the argument. If covered and uncovered books retain identically, you do not
have a coverage case — you have a different problem, and you should say so rather than ask.

---

## 3. Step 2 — Size the book bottom-up

Ratios are the output of this calculation, never the input.

```
Available customer-facing hours per CSM per year
    = annual working hours
    − internal meetings, reporting, admin, enablement, escalation overhead

Accounts a CSM can carry at tier T
    = available customer-facing hours ÷ hours per account per year at tier T
```

Common working assumptions — **replace every one with a time study of your own team** [P]:

| Input | Typical planning assumption | Note |
| --- | --- | --- |
| Annual working hours per CSM | ~2,000 | Before any deduction |
| Share of time available for customers | roughly two-thirds; one-third internal | A widely used planning split [P] |
| High-touch account | ~40 hours/account/year | Quarterly business reviews, success planning, escalations |
| Mid-touch account | ~12 hours/account/year | Half-yearly reviews, monthly async |
| Low-touch / digital | ~2 hours/account/year | Exception handling only |

The ranges in circulation are a weak sanity check on the output, never a substitute for
it — none is a measured benchmark, so none belongs on a slide as a peer number:

| Reference | Value | Source · year | Label |
| --- | --- | --- | --- |
| Current circulating ranges (ENT $2.5–4M, MM $1.5–2.5M, SMB pooled $1–1.8M) | — | CS-platform content aggregations, 2025–26 | [P] |
| The "$1M ARR per CSM" convention | — | Industry folklore from early CS | [P] — explicitly criticised as context-free by practitioners |

**The empirical ceiling beats every published ratio.** Plot book size per CSM against GRR and
expansion for your own team. The book size at which retention starts degrading is your
practical ceiling, and it is defensible in a way that no external number is.

---

## 4. Step 3 — Quantify the ARR the gap exposes

Three numbers, in this order:

| # | Number | Formula |
| --- | --- | --- |
| 1 | **ARR in the gap** | Uncovered ARR (+ ARR in named books above the empirical ceiling) |
| 2 | **ARR in the gap renewing in the decision window** | Filter (1) to accounts whose **opt-out deadline** falls within the planning horizon |
| 3 | **Expected loss differential** | `ARR in the gap × (GRR_covered − GRR_uncovered)` for the same segment and period |

Number 3 is the honest measure of what coverage is worth. It is a **differential**, which is
why it survives scrutiny: you are not claiming credit for the retained base, only for the gap
between two books you can both observe.

If you cannot observe both books — because everything is covered, or nothing is — say
`UNKNOWN — requires a covered/uncovered GRR split` and fall back to the breakeven framing in
§5, which does not require the differential to be known.

---

## 5. Step 4 — The breakeven save rate

The strongest form of a CS headcount ask, because it does not require a forecast.

```
Fully loaded cost of the hire
    = base + variable + benefits/taxes + tooling + allocated management
      (a common planning multiple is 1.25–1.4× base [P] — use your finance team's actual rate)

Gross profit on retained ARR
    = ARR × subscription gross margin
      (median subscription gross margin 81%, CY2024, N=76 [M — Benchmarkit 2025])

Breakeven ARR that must be retained
    = fully loaded cost ÷ subscription gross margin

Breakeven improvement in GRR on the covered book
    = breakeven ARR ÷ ARR the hire will cover

Breakeven save rate on at-risk ARR
    = breakeven ARR ÷ at-risk ARR in the hire's book
```

State it as a sentence: *"This hire pays for itself if it improves gross retention on a
$14.2M uncovered book by 129 basis points, or equivalently if it saves 8.4% of the $2.2M
currently at risk in that book. Our covered books retain 340 basis points better than our
uncovered books in the same segment, so the breakeven is roughly a third of the observed
differential."*

**Payback framing for a CFO.** Express it in months: `fully loaded annual cost ÷ (monthly
gross profit on the incremental retained ARR)`. A CS hire that pays back inside 12 months on
breakeven assumptions is an easy approval; one that needs 24 months needs a strategic
argument as well as an arithmetic one.

**Do not use LTV in the ask.** LTV is definitionally unstable — the same company can produce
$655k naive, $530k gross-margin-adjusted, and $301k discounted [M — worked example, cs-metrics
reference] — and any LTV quoted without its formula is unreviewable. Use retained gross profit.

---

## 6. Step 5 — The honest counterfactual

Every ask is compared against doing nothing. Write the comparison yourself, in three parts,
and resist inflating it — an inflated counterfactual is detectable and it discredits the
whole case.

| Part | What to write | Failure mode |
| --- | --- | --- |
| **What does not get done** | The specific accounts, segment or programme that stays uncovered, named | "We'll be stretched" |
| **What the exposure becomes** | The ARR in the gap and its opt-out-deadline profile over the horizon | Implying every uncovered dollar is lost |
| **What you will do instead, at zero cost** | The reprioritisation you will actually make — usually pulling coverage off a lower-value segment, and its cost | Claiming there is no plan B. There always is, and the CFO knows it |

The strongest sentence in a headcount case is usually the concession: *"If the answer is no, I
will move the 42 Mid-Market accounts under $40k ARR to the digital programme and cover the
uncovered Enterprise book with the existing team. That closes the Enterprise gap and opens a
$3.1M Mid-Market gap, which I judge the better trade — but it is a trade, not a solution, and
Mid-Market GRR is the number I expect to pay for it."*

---

## 7. Step 6 — The alternatives you must have costed

Bring these before you are asked. Being the person who already priced the cheaper option is
what makes the expensive option credible.

| Alternative | When it is genuinely better | What it costs you |
| --- | --- | --- |
| **Digital / pooled coverage** | Long tail where cost-to-serve approaches segment gross-margin contribution | Slower risk detection, no relationship depth; expansion typically suffers before retention does |
| **Re-tiering the book** | Coverage is misallocated rather than insufficient | Nothing in cash; the displaced segment's retention is the bill |
| **Automation / tooling** | Detection is the gap, not capacity | Implementation time; tooling does not run a save conversation |
| **Onboarding FTE instead of a CSM** | Churn is front-loaded — hazard concentrated in the first 90–180 days | Nothing, if the hazard curve supports it. Front-loaded and back-loaded churn need opposite investments |
| **Support headcount instead** | Reliability or response time is the reason code on the losses | Nothing, if the reason codes support it — and it is a stronger case than a CSM if they do |

**Cost-to-serve gate.** If a segment's fully loaded CS + Support cost exceeds its gross-margin
contribution, no amount of headcount fixes it and asking for some damages your credibility.
Reference: CS + Support spend runs at a median **9% of ARR** across 1,000+ private B2B SaaS
companies [M — SaaS Capital 2026 Spending Benchmarks], 10% at $3–5M ARR, with equity-backed
companies spending roughly 2× bootstrapped ones.

---

## 8. The one-page ask

```markdown
## Ask: <N> <role> · $<fully loaded cost> · decision needed by <date>

**The gap.** <X> accounts holding $<Y>M have no named coverage. $<Z>M of that renews on an
opt-out deadline inside the next two quarters.

**The evidence.** Covered books in the same segment retain <a> bps better than uncovered
books over the same period (<covered GRR>% vs <uncovered GRR>%, TTM, n=<n> accounts each).

**Breakeven.** $<cost> ÷ <gross margin>% = $<breakeven ARR> of retained ARR, which is a
<bps> bps improvement on the $<Y>M book, or a <s>% save rate on the $<r>M currently at risk
in it. That is <fraction> of the observed covered/uncovered differential.

**Expected case.** <band, not a point estimate> — $<low>–$<high> of retained ARR in the first
full year, on the assumption that <named assumption>.

**Counterfactual.** If no: <what does not get done> · <exposure> · <the zero-cost trade and
what it costs>.

**Kill criterion.** If <metric> has not moved <threshold> by <date>, I will not renew this ask.

| # | Action | Owner | By | Cost | Expected effect | Success measure | Review date |
|---|---|---|---|---|---|---|---|
| 1 | | | | $ | | | |
```

---

## 9. Objections and answers

| Objection | Answer that works | Answer that loses |
| --- | --- | --- |
| "Can't the existing team absorb it?" | Touch coverage in the named tier is <x>% — below 70% the book is already oversized [P]. Here is the time study | "The team is at capacity" |
| "Why not automate it?" | Automation closes detection, not the save conversation. Here is the reason-code mix: <x>% of at-risk ARR is champion loss or value-not-realised, both of which require a human | "Tooling won't work" |
| "What did the last hire deliver?" | The cohort delta attributable to their book, with the confounders named | The total retained ARR of their book |
| "Everyone says they need heads" | The covered/uncovered GRR differential is measured, not asserted, and here is the breakeven | Benchmark ratios |
| "Can we do it next quarter?" | The opt-out-deadline profile: $<Z>M of the exposed ARR decides before then. Delay does not defer the exposure, it removes the chance to act on it | "It's urgent" |
| "Prove it worked afterwards" | The kill criterion and the review date, offered before you are asked | Silence |
| "That's above the 9% CS spend benchmark" | Whether the benchmark's population matches yours (it includes Support; equity-backed companies run ~2× bootstrapped [M]) — then the cost-to-serve-by-segment table | Disputing the benchmark without the segment table |

---

## 10. Worked example

`../scripts/headcount_case.py` computes all of this deterministically. Sample inputs and outputs:

| Input | Value |
| --- | --- |
| Uncovered ARR | $14,200,000 |
| Uncovered accounts | 62 |
| Uncovered ARR with opt-out deadline inside 2 quarters | $5,400,000 |
| At-risk ARR in the uncovered book | $2,200,000 |
| GRR, covered book (same segment, TTM) | 91.4% |
| GRR, uncovered book (same segment, TTM) | 88.0% |
| Subscription gross margin | 81% |
| Fully loaded cost per CSM | $185,000 |
| Heads requested | 2 |

| Output | Value | Arithmetic |
| --- | --- | ---: |
| Fully loaded cost | $370,000 | 2 × $185,000 |
| Breakeven retained ARR | $456,790 | $370,000 ÷ 0.81 |
| Breakeven GRR improvement on the book | 322 bps | $456,790 ÷ $14,200,000 |
| Breakeven save rate on at-risk ARR | 20.8% | $456,790 ÷ $2,200,000 |
| Observed covered/uncovered differential | 340 bps | 91.4% − 88.0% |
| Expected retained ARR at the observed differential | $482,800 | $14,200,000 × 0.034 |
| Expected gross profit | $391,068 | $482,800 × 0.81 |
| Simple payback | 11.4 months | $370,000 ÷ ($391,068 ÷ 12) |
| Margin of safety | 5.7% | (340 − 322) ÷ 322 |

**How to say it:** *"Breakeven is 322 basis points on a $14.2M uncovered book. The measured
differential between our covered and uncovered books in the same segment is 340 basis points.
That is a 5.7% margin of safety, which is thin — so I am asking for two heads, not four, and
the kill criterion is that uncovered-book GRR moves 150 basis points by 31 March or I do not
come back for the next two."*

Note what makes this credible: the margin of safety is **thin**, and saying so is what makes
the rest of the analysis believable.

---

## 11. Reference points, with their evidence labels

| Figure | Value | Source · year · population | Label |
| --- | --- | --- | --- |
| CS + Support spend | 9% of ARR median; 10% at $3–5M ARR; equity-backed ~2× bootstrapped | SaaS Capital, *2026 Spending Benchmarks*, 1,000+ private B2B SaaS | [M] |
| Subscription gross margin | 81% median (N=76) | Benchmarkit, *2025 B2B SaaS Performance Metrics Benchmarks*, CY2024 | [M] |
| Expansion CAC ratio vs new CAC ratio | $1.00 (N=21) vs $2.00 (N=73) | Benchmarkit 2025, CY2024 | [M] |
| Companies that compute expansion CAC ratio | <20% | Benchmarkit 2025 | [M] |
| ARR per FTE (company-wide) | $240k at $50–100M ARR; $283,379 above $100M (N=174) | Benchmarkit 2025, CY2024 | [M] |
| ARR per CSM / accounts per CSM | **No Grade-A public benchmark exists — none is cited here** | — | — |
| Current ARR-per-CSM ranges | ENT $2.5–4M, MM $1.5–2.5M, SMB pooled $1–1.8M | CS-platform content aggregations, 2025–26 | [P] |
| CSM time split | ~two-thirds customer-facing, one-third internal | Widely used planning convention; consistent with `R13 · The Capacity Truth` | [P] |
| Hours per account by tier | 40 / 12 / 2 per year (high / mid / low touch) | ORM Technologies capacity model, 2026 — explicitly illustrative | [P] |
| Touch-coverage floor for a named tier | ~70% | Practitioner rule of thumb | [P] |
| Fully loaded cost multiple on base salary | 1.25–1.4× | Planning convention | [P] |

**No current Grade-A public benchmark for ARR per CSM exists.** Any current-year figure you
see quoted is an aggregation of vendor content. Use ratios as an internal capacity constant,
build the ask on your own covered/uncovered differential, and say which is which.
