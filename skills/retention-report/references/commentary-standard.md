# The Commentary Standard

> Every movement needs a **driver**, not a description. This file is the difference between a
> report that gets read and one that gets filed.
>
> A description restates the number the reader can already see. A driver names the mechanism,
> the population it acted on, and the share of the variance it explains — and it can be wrong,
> which is what makes it worth writing.

**Contents**
- [The five-part block](#the-five-part-block)
- [The driver test](#the-driver-test)
- [Driver library, by bridge line](#driver-library-by-bridge-line)
- [Quantifying "where" — the share-of-variance arithmetic](#quantifying-where--the-share-of-variance-arithmetic)
- [Mix versus performance](#mix-versus-performance)
- [Banned sentences](#banned-sentences)
- [Before and after](#before-and-after)
- [Commentary length by section](#commentary-length-by-section)
- [Writing the uncomfortable one](#writing-the-uncomfortable-one)

---

## The five-part block

Every section from §2 onward closes with exactly this, in this order. No free-form paragraphs.

| Part | What it must contain | Failure mode it prevents |
| --- | --- | --- |
| **What** | The number, the prior period, the variance to plan | A number with no anchor |
| **Where** | The segment, cohort, product or owner carrying the variance, with its arithmetic share | "Retention is down" applied to a book where one segment moved and the rest did not |
| **Why** | The root cause, with evidence, stated so it could be disproved | Hypothesis presented as diagnosis |
| **So what** | The forward implication, in dollars, over a stated horizon | A finding with no consequence |
| **Now what** | The decision or ask, with an owner and a date | A report that changes nothing |

Worked, in five sentences:

> **What.** TTM GRR 83.4%, down 110bps QoQ and 260bps against a plan of 86.0%.
> **Where.** 71% of the miss is SMB: SMB GRR 69.5% against a plan of 80.0%, on a $12.2M t0 base;
> Enterprise (88.2%) and Mid-Market (81.0%) are within 100bps of plan.
> **Why.** Of $3.10M SMB cohort churn, $1.86M carries reason code `never_went_live`, and those
> accounts had a median TTV of 71 days against a 30-day target — median TTV for SMB cohorts rose
> from 44 to 61 days between February and June as onboarding headcount stayed flat while SMB new
> logos grew 34%.
> **So what.** At the current SMB cohort hazard, FY27 SMB GRR lands at 70–73%, a further $1.1M
> ARR drag against plan, and the 2026-Q1 and Q2 cohorts are already tracking 750bps below the
> 2024-Q3 cohort at the same tenure.
> **Now what.** Gate SMB onboarding on a 30-day activation milestone and move two onboarding
> FTEs from Mid-Market. Owner: VP Onboarding. Decision needed by 2026-09-12, before Q4 hiring
> closes.

---

## The driver test

**Could you be wrong about it?** If nothing could disprove the sentence, it is not a driver.

| Sentence | Driver? | Why |
| --- | --- | --- |
| "GRR fell because retention got worse" | No | Restates the metric in different words |
| "Churn was elevated this quarter" | No | An adjective standing in for a number |
| "We saw increased competitive pressure" | No | No population, no count, no test |
| "Two of the four Enterprise losses named the same competitor in their loss debrief, both in the FS vertical, both citing the audit-log gap" | Yes | Falsifiable: read the debriefs, count the mentions |
| "SMB churn is concentrated in accounts that never reached go-live: $1.86M of $3.10M" | Yes | Falsifiable: recount the reason codes |
| "Expansion is soft because the sales team is distracted" | No | Unfalsifiable, and it blames a population instead of naming a mechanism |
| "Expansion fell $410k QoQ; $380k of that is the two ramp deals that stepped up last quarter and do not repeat" | Yes | Falsifiable: check the two contracts |

Second test: **would the sentence read identically next month with different numbers?** If yes,
it is boilerplate. Delete it.

---

## Driver library, by bridge line

For each line, the questions that produce a real driver, in the order to ask them. Stop at the
first one that explains more than half the variance, and say how much it explains.

### Churn moved

| Ask | Where to look | What it rules in |
| --- | --- | --- |
| Is it concentrated in one segment, ACV band, or tenure bucket? | Segment cut, tenure cut | A segment-specific mechanism, not a book-wide one |
| Is it one or two accounts, or many? | Named-loss table, top-10 share of churned ARR | A concentration event vs a systemic one. Two losses at $600k each is not a trend |
| What is the reason mix, and how did it move? | Reason code table vs prior period | Which function owns the fix |
| Controllable or not? | Controllable split | Whether this is a CS result or an exogenous one |
| Were they flagged? How long before? | Risk detection rate; band at −90d | Whether this is a delivery failure or a detection failure — different fixes |
| Which cohort did they come from? | Cohort triangle | Whether it is an acquisition-quality problem that predates CS |
| Did anything change 6–12 months before the loss? | Onboarding metrics for that cohort, release notes, pricing changes | The upstream cause, which is usually where the fix lives |

### Contraction moved

Seat reductions vs tier downgrades vs negotiated discount vs de-scoped products — decompose
first, because they have different owners. Then: is utilisation falling ahead of the reduction
(a value problem), or is headcount falling at the customer (an exogenous one)? Contraction
rising while churn is flat means value density, not churn.

### Expansion moved

Decompose into seats · tier · cross-sell · price uplift · usage commit before writing anything.
Then strip out **contractual ramp step-ups**, which are pre-signed and are not a CS win; a
quarter that looks strong on ramp and weak on new expansion is a warning, not a result. Check
whether expansion is concentrated in accounts that also carry risk — expansion into an unhealthy
account is a contraction next year.

### New moved

Not CS's line, but it changes every retention denominator. If new-logo mix shifted toward a
lower-retaining segment, next year's blended GRR falls without any CS performance change. Say so
explicitly — it is the single most common way a CS org is blamed for a go-to-market decision.

### Reactivation moved

Report it, exclude it from retention, and separate win-back from budget cuts (which come back)
from win-back after a product gap (which usually does not). A rising reactivation line beside a
rising churn line is a revolving door, not a recovery.

### A retention rate moved but the bridge did not

The population changed. Check: accounts added or removed from the base, an `is_internal`
reclassification, a parent/child roll-up change, a re-segmentation. This is a data event, not a
business event, and publishing it as a business event is how a report loses a CFO permanently.

---

## Quantifying "where" — the share-of-variance arithmetic

Never write "mostly SMB". Compute it.

```
Total variance          = actual − plan                       (in ARR, not in points)
Segment s contribution  = (actual_s − plan_s)
Share of variance       = (actual_s − plan_s) / (actual − plan)
```

Worked: plan GRR 86.0% on a $92.6M base implies retained $79.64M; actual retained $77.23M;
variance −$2.41M. SMB planned to retain $9.76M (80.0% of $12.2M) and retained $8.48M: −$1.28M,
which is **53%** of the total variance on **13%** of the base. Mid-Market contributed −$0.86M
(36%), Enterprise −$0.27M (11%).

Say it as: *"SMB is 13% of the base and 53% of the miss."* That single sentence does more work
than the whole table above it.

For a rate expressed in points, convert to dollars first. Segment rates are not additive and
averaging them is wrong; a 10-point SMB move on 13% of the base is a 1.3-point blended move.

---

## Mix versus performance

The question a CFO asks about any blended retention movement: *is that mix or performance?* Have
the decomposition ready before the meeting.

```
ΔNRR_total = Σ w_i,t0 × ΔNRR_i        (performance — segments got better or worse)
           + Σ Δw_i × NRR_i,t0        (mix — the base shifted between segments)
           + Σ Δw_i × ΔNRR_i          (interaction — report separately, never fold into mix)
```

Where `w_i` is segment i's share of the opening base. Report all three in basis points, show
that they reconcile to the total movement, and name which dominates.

**Why it matters:** a mix-driven NRR decline is a go-to-market outcome — the base shifted toward
a lower-retaining segment — and the CS org may have improved every segment while the blended
number fell. A performance-driven decline is CS's own result. Presenting the first as the second
is a failure of analysis; presenting the second as the first is a failure of character.

`../../exec-retention-review/scripts/retention_math.py --section mix` computes it.

---

## Banned sentences

| Banned | Why | Write instead |
| --- | --- | --- |
| "We will continue to monitor" | Not an action; nobody can tell later whether it happened | "Weekly review of the 14 accounts in the SMB stall list. Owner: <name>. First readout 12 Sept" |
| "Focus on adoption" | A category, not a play | "Two onboarding FTEs move to SMB; go-live gate at 30 days" |
| "Engage proactively" | Verb with no object, no owner, no date | The specific outreach, to whom, by when |
| Any sentence with no number in it | It cannot be checked, so it cannot be wrong, so it carries no information | Add the number and its window |
| Any explanation that cannot be falsified | It is a story, not a finding | Name the test that would disprove it |
| "Elevated", "significant", "substantial" | Adjectives standing in for numbers | The number and its comparison |
| "Some accounts", "a number of customers" | Countable things left uncounted | The count and the ARR |
| "Trending in the right direction" | Direction without magnitude or horizon | "+180bps over three periods; at this rate plan is met in Q3 FY27" |
| "Due to a combination of factors" | A refusal to rank causes | The two largest, with their shares of variance |
| "As expected" | Hides whether the expectation was ever written down | "Against the 84.0% we called at T-90" |

---

## Before and after

| Before | After |
| --- | --- |
| "GRR declined slightly this quarter due to elevated churn in the SMB segment." | "TTM GRR 83.4%, −110bps QoQ. SMB is 13% of the base and 53% of the $2.41M variance to plan; Enterprise and Mid-Market are within 100bps." |
| "We saw strong expansion performance driven by the enterprise team." | "Expansion $11.1M TTM, +$1.4M YoY. $0.9M of the increase is three cross-sell deals in Enterprise; $0.5M is contractual ramp step-ups that do not repeat next year." |
| "Health scores improved across the book." | "Improvement rate 25.2% against 16.5% degradation; net ARR band-movement +$12.1M toward Secure. But 23.3% of the ARR churned in the window was Secure or Watch ninety days earlier, so the score is moving without discriminating at the top end." |
| "Onboarding is taking longer than we would like." | "Median SMB TTV 61 days in the June cohort against a 30-day target, up from 44 days in February. P90 is 147 days. $1.65M of ARR is in accounts past their target go-live." |
| "The forecast was broadly accurate." | "94.4% mean accuracy across four quarters, but every quarter was called high: signed bias +6.0%. The problem is bias, not dispersion, and it is a category-definition problem in Commit." |
| "Churn was driven by a few large accounts." | "Four losses account for $2.1M of $3.0M churned ARR. Three are `m_and_a`, tagged uncontrollable; the fourth is `never_went_live` at $480k and is the one to learn from." |

---

## Commentary length by section

| Section | Words | Why |
| --- | --- | --- |
| §1 The Call | 80–120 | It is the whole report for most readers |
| §2 Bridge | 60–100 | One line moved; name it and its share |
| §3 Retention | 80–120 | Two rates, both cut by segment |
| §4 Cohorts | 40–80 | One finding: is drift present, and where |
| §5 Churn | 100–150 | The longest, because it carries the reason mix and the lessons |
| §6–8 | 40–60 each | One movement, one driver |
| §9 Migration matrix | 80–120 | The false-green line, the rescue rate, and what they imply |
| §10–12 | 60–90 each | Exposure, credibility, leading indicator |

Anything longer is being used to hide the absence of a finding. Anything shorter has skipped
either the *why* or the *now what*.

---

## Writing the uncomfortable one

Every edition should contain at least one thing the author did not want to publish. Four rules,
in order:

1. **First, not buried.** If the miss is the story, it goes in §1. A reader who finds bad news
   on page nine stops trusting pages one to eight.
2. **Own the part that is yours, name the part that is not, and do not blur the boundary.**
   "Three of the four losses are M&A consolidation, which we could not have changed. The fourth
   we could have: it was flagged Secure at −90 days and it should not have been."
3. **Bring the change with the news.** Bad news plus a dated change with an owner reads as
   command; bad news alone reads as a request for absolution.
4. **Say what you will report next time, unprompted.** Naming the leading indicator you will be
   graded on next month is the cheapest credibility available, and it is the thing that converts
   a bad quarter into a trusted function.

The failure this prevents is the report that only contains comfortable conclusions — which was
written to be liked rather than used, and which the room stops reading the second time a number
it never mentioned shows up in the forecast.
