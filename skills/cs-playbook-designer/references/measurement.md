# Measuring a Playbook

> The uncomfortable finding first: **for almost every individual play, a CS team cannot honestly
> claim a retention effect.** The samples are too small, the assignment is not random, and the
> accounts entering a play were selected because they were worse than average. What a team *can*
> do is measure whether the motion ran, whether the behaviour it targeted moved, and report
> retention as observed rather than attributed. That is a smaller claim and a defensible one.
>
> Evidence labels: `[M]` measured · `[V]` vendor default · `[P]` practitioner · `[A]` academic ·
> `[D]` derived arithmetic. Anything unlabelled is a convention of this library, not a benchmark.

**Contents**
1. [Three layers, never blended](#1-three-layers-never-blended)
2. [Activity metrics](#2-activity-metrics)
3. [Designing the leading outcome](#3-designing-the-leading-outcome)
4. [Why retention attribution is hard](#4-why-retention-attribution-is-hard)
5. [The holdout](#5-the-holdout)
6. [Matched historical control](#6-matched-historical-control)
7. [Pre/post, and what it cannot show](#7-prepost-and-what-it-cannot-show)
8. [Sample size and power](#8-sample-size-and-power)
9. [Sentences you may and may not write](#9-sentences-you-may-and-may-not-write)
10. [The quarterly play report](#10-the-quarterly-play-report)
11. [Measurement errors that recur](#11-measurement-errors-that-recur)
12. [Sources](#12-sources)

---

## 1. Three layers, never blended

| Layer | Question | Evidence needed | Claim it supports |
| --- | --- | --- | --- |
| **Activity** | Did the motion run as designed? | The fire log alone | "The play ran on 61 accounts; 74% reached a defined exit" |
| **Leading outcome** | Did the behaviour we intervened on move? | Per-account baseline + window | "Weekly actives recovered to ≥70% of baseline on 38 of 61" |
| **Retention delta** | Did we cause the renewal? | A control arm | Nothing at all, without one |

Blending them produces the sentence that destroys a CS team's credibility with a CFO: *"our save
play delivered $1.4M of retained ARR"* — a number built by summing the ARR of every account that
ran the play and happened to renew, most of which would have renewed anyway.

**Report the three layers as three rows, in this order, always.** The ordering matters: activity
first tells the reader what was actually done, and it is the only layer that is unambiguous.

## 2. Activity metrics

| Metric | Formula | Target | What a bad number means |
| --- | --- | --- | --- |
| **Fire count** | distinct accounts with ≥1 fire in the period | inside the designed band | Outside the band → the qualifier drifted or the book changed |
| **Completion rate** | runs reaching a defined exit ÷ runs started | ≥ 60% | Below 60% for two cycles is a kill criterion: the play is wrong, or capacity is |
| **Step drop-off** | runs completing step *n* ÷ runs completing step *n−1* | no step below 70% | The step where it falls off is the step that is too expensive or too vague |
| **Cycle time — response** | `first_human_touch_at − fired_at` | inside the SLA | The single best predictor of whether a team trusts its own alerts |
| **Cycle time — resolution** | `exited_at − fired_at` | inside the designed window | Longer than the window means the exit criteria are not being applied |
| **SLA attainment** | steps with `sla_met` ÷ steps due | ≥ 85% | Below that, either the SLA is wrong or the owner role is under-staffed |
| **Suppression rate** | fires suppressed ÷ fires raised | < 30% | Above 30% the trigger is mostly firing on accounts it should not evaluate |
| **False-fire rate** | sampled fires a human would not have wanted ÷ sample | ≤ 20% | The number that decides whether CSMs keep opening the alerts |
| **Orphan count** | live triggers with no attached play | **0** | Every orphan is alert-fatigue exposure with no upside |

**Measure execution quality, not just completion.** A run marked complete where nobody spoke to
the customer is a closed task, not a motion. Pair completion rate with the response cycle time; a
play with 95% completion and a 9-day response time is being closed retrospectively.

**Score process before results while a play is new** — when a team is learning a play, hold them
to whether they followed it; shift to results once the habit is formed
`[P · Kristen Hayer, The Success League]`.

## 3. Designing the leading outcome

The leading outcome is the behaviour the play exists to move. It is chosen at design time, before
the first fire, and it obeys four rules:

| Rule | Why | Bad → good |
| --- | --- | --- |
| **Measured against the account's own baseline** | Accounts differ by an order of magnitude | "WAU above 15" → "WAU above 70% of this account's pre-decay median" |
| **Inside a stated window** | An outcome with no window cannot fail | "adoption recovers" → "within 45 days of fire" |
| **Observable without asking the customer** | Otherwise the measurement depends on the intervention | "they feel supported" → "a second contact replied in-thread" |
| **Different from the trigger** | Otherwise you are measuring the trigger resolving itself | Trigger `WAU < 0.70`; outcome `WAU ≥ 0.70` is circular. Use a **different** metric or a **durability** condition: ≥0.70 sustained for four consecutive weeks |

The fourth rule is the one most often broken and it silently inflates every play's success rate,
because decayed metrics regress upward on their own.

**Leading outcomes are where the statistical power actually is.** They move further than renewal
rates, they move sooner, and several are continuous rather than binary — so they reach
significance at sample sizes a real book produces. This is the practical answer to §8.

## 4. Why retention attribution is hard

Four mechanisms, each sufficient on its own to invalidate a naive treated-vs-untreated comparison.

| Mechanism | What it does | The tell |
| --- | --- | --- |
| **Selection** | Accounts enter the play *because* they are worse. Treated accounts have lower baseline renewal odds by construction | Untreated accounts renew better, and someone concludes the play is harmful |
| **Regression to the mean** | Metrics selected for being extreme move back toward normal with no intervention | Every pre/post read shows improvement, including for plays that did nothing |
| **The intervention breaks the prediction** | A good CS org acts on the score, which changes the outcome. Saved high-risk accounts appear as false positives `[A]` | A model with perfect precision is a model nobody acted on |
| **Survivorship in the denominator** | Accounts that churned mid-play get dropped from the analysis | Completion rate and renewal rate both look excellent |

**Propensity is not uplift.** Ranking by "who is likely to churn" systematically prioritises
accounts that would have churned regardless and accounts that would have renewed regardless;
uplift formulations estimate `P(renew | treated) − P(renew | untreated)` and target the accounts
where the play changes the answer `[A · uplift/causal targeting literature, e.g. Sapru,
"Guardrailed Uplift Targeting", arXiv:2512.19805, 2025; cost-sensitive uplift modelling for
cross-sell, Neural Computing and Applications, Springer, 2024]`. Every uplift method requires a
control group. **Build the holdout first; the modelling is the easy part.**

## 5. The holdout

The only design that supports a causal claim, and it costs less than teams fear.

| Parameter | Default | Reasoning |
| --- | --- | --- |
| **Share withheld** | 10% of qualifying fires | Small enough that leadership will approve it, large enough to detect a large effect |
| **Randomisation point** | At fire time, not at account level | Account-level assignment leaks: the same account fires different plays |
| **Unit** | The fire, keyed to `account_id` for the period, so an account is not treated for one play and held out for another in the same week | Prevents contamination between plays |
| **Duration** | Two full renewal cycles, minimum | One cycle cannot separate the play's effect from the year |
| **Exclusions** | Critical band · ARR above a stated ceiling · any account in an open escalation | Ethical and commercial guardrail |
| **Logging** | `holdout_assignment` (fire_id, account_id, arm, assigned_at, seed) | Without the seed the assignment is unauditable |
| **Who may see it** | CS Ops. Not the CSM owning the account | A CSM who knows an account is held out will work it anyway, which is human and destroys the arm |

**State the exclusion's effect on the estimate, every time.** Excluding Critical-band and top-ARR
accounts means the measured effect is the effect **on the treatable middle**, and it will
understate the value of the play on the accounts you most care about. That sentence goes in the
spec, not in a footnote.

**The honest objection, answered.** "We can't withhold help from a customer at risk." True for
Critical accounts, which is why they are excluded. For the middle of the book, the alternative to
a holdout is not more help — it is spending the same hours with no idea whether they worked, for
years. A 10% holdout for two cycles is the cheapest information a CS org can buy.

**The holdout arm is the binding constraint on power.** At a 10% share, the holdout accumulates
ten times slower than the treated arm, so the time-to-significance is set by the holdout. A 50/50
split reaches an answer roughly five times faster — `../scripts/play_sizing.py` prints both.

## 6. Matched historical control

When a holdout is genuinely refused, the second-best design: find accounts that met the trigger
condition **before the play existed**, and compare.

| Step | Detail |
| --- | --- |
| 1. Backfill the trigger | Run the trigger definition against history for the 12–24 months before launch. These are your candidate controls |
| 2. Match | On ARR band, segment, tenure band, product mix, and **the trigger's own severity** (how far past the threshold) |
| 3. Restrict the window | Controls from more than 24 months back are a different product and a different team |
| 4. Compare outcomes at the same horizon | Renewal at the first opt-out date after the fire, not "ever renewed" |
| 5. State the confounds | Product changes, pricing changes, team changes, market conditions — name them, do not wave at them |

**The confound sentence is mandatory**: *"Controls are drawn from FY25, before the onboarding
redesign shipped; some of the difference is that change rather than this play."* A matched control
without a named confound is a holdout claim wearing a disguise.

## 7. Pre/post, and what it cannot show

Pre/post on the same accounts is the weakest design and the most commonly used. It can show:

- **That the metric moved** — useful, and worth reporting.
- **How fast it moved** — useful for setting the exit window.

It cannot show that the play caused the movement, because the accounts were selected for being
extreme and extreme values regress. If pre/post is all you have, write it as:

> Weekly actives on the 61 accounts that ran `PB-R01` recovered from a mean of 41% of baseline at
> fire to 78% at day 45. **No control arm exists, so some of this recovery would have happened
> anyway; regression to the mean alone typically explains part of a rebound from a selected
> extreme.** The holdout starting 2026-10-01 will size that share.

That paragraph is publishable. "Our decay play recovered adoption by 37 points" is not.

## 8. Sample size and power

Two-proportion normal approximation, two-sided α = 0.05. Run
`python3 ../scripts/play_sizing.py --power-table` to regenerate.

| Base renewal rate | Detect +2pp | +5pp | +10pp | +15pp |
| --- | --- | --- | --- | --- |
| 70% | 8,080 | 1,251 | 294 | 121 |
| 80% | 6,039 | 906 | 199 | 76 |
| 90% | 3,213 | 435 | — | — |

*Accounts **per arm**, power 0.80.*

Read the first two columns and the consequence is unavoidable: **a play firing on 20 accounts a
month, with a 10% holdout, needs decades to detect a 5-point renewal improvement.** The worked
sample library in `../scripts/sample-library.json` returns exactly that — 34 years for the
usage-decay play at a 10% holdout, 7 years at a 50/50 split, and 489 years for the
commercial-event play whose whole value is that it almost never fires `[D]`.

Three legitimate responses, in order:

1. **Power the leading outcome instead.** A continuous metric with a larger effect reaches
   significance at a fraction of the sample.
2. **Pool plays into a programme-level test.** The question "does having a triggered risk library
   change retention" is answerable when one play's question is not — randomise at the level of the
   **whole library** across a segment, not per play.
3. **Report activity and outcomes and make no causal claim.** This is the default and it is not a
   failure. It is what the evidence supports.

**Do not report accuracy on a rare event.** At a 3% churn base rate, predicting "renew" for
everyone scores 97% `[A]`. Where discrimination must be reported, use precision and capture at
your actual capacity, and dollar capture in the top decile — the version a CCO reviews
(`trigger-design.md` §4). Under class imbalance, precision-recall is the correct threshold-free
summary, not ROC `[A · Saito & Rehmsmeier, 2015]`.

## 9. Sentences you may and may not write

| Never write | Write instead |
| --- | --- |
| "This play saved $340k" | "23 accounts carrying $340k ran this play; 19 renewed. Assignment was not randomised, so this is an ordering, not an effect" |
| "The play improved retention by 8 points" | "Treated 88%, holdout 80%, n=61 and n=7. The holdout arm is far too small to separate 8 points from noise — see the power table" |
| "Adoption recovered because of the play" | "Adoption recovered on 38 of 61; the holdout will size how much of that would have happened anyway" |
| "94% play success rate" | "74% reached a defined exit; of those, 62% hit the leading outcome inside the window" |
| "Our alerts have 90% accuracy" | "Precision at our working capacity of 45 accounts was 27%; dollar capture in the top decile was 49%" |
| "The library drove NRR from 104% to 109%" | "NRR moved from 104% to 109% over the same period the library ran. No control exists; here is what else changed in that window" |
| "Most teams see a 20% lift from playbooks" | Delete it. There is no such measured benchmark; do not invent one |

**The general rule:** every sentence containing a causal verb — *saved, drove, improved, caused,
delivered* — requires a control arm behind it. Without one, use *observed, coincided with,
ran on, reached*.

## 10. The quarterly play report

One page per library. This is what goes to the CCO.

```markdown
# Play Library Report — <quarter>

## Activity
| Play | Fires | % of book | Completion | Median response (SLA) | SLA attainment | False-fire |
|---|---|---|---|---|---|---|

## Leading outcomes
| Play | Outcome measured | Window | Hit | Missed | Not yet due |
|---|---|---|---|---|---|

## Retention — observed, not attributed
| Play | Accounts | ARR | Renewed | Trigger-eligible, not run | Renewed | Control design |
|---|---|---|---|---|---|---|

**Claims permitted this quarter:** <the exact sentences, or "none — no play reached power">.
**Holdouts running:** <play, share, start date, accounts accumulated, months to power>.

## Changes
| Play | Change | Version | Reason | Measurement window reset? |
|---|---|---|---|---|

## Kill list
| Play | Criterion hit | Archived to |
|---|---|---|
```

Retention appears in a table headed **observed, not attributed**, with the control-design column
visible. That column is what stops the number being lifted into a board slide without its caveat.

## 11. Measurement errors that recur

| Error | Correction |
| --- | --- |
| Summing the ARR of every account that ran a play and renewed | That is the ARR of accounts that renewed, not the effect of the play |
| Comparing treated accounts to the whole book | The book was not selected for being at risk; treated accounts were |
| Dropping accounts that churned mid-play | They are the outcome. Keep them in the denominator |
| Measuring the trigger's own metric as the outcome | Use a different metric, or require durability over four weeks |
| A holdout the CSM can see | Hold it in CS Ops; a visible holdout is not a holdout |
| Restarting the measurement window without a version bump | Two different plays measured as one |
| Reporting a rate with no denominator | "74% completion" needs "of 61 runs started" |
| Quoting a benchmark with no segment, year and sample | "Median GRR 88%" alone is not a fact; the source, year and n are part of the number |
| Reading a first-cycle result as the answer | One cycle cannot separate the play from the year |

## 12. Sources

| Source | Year | What it grounds | Label |
| --- | --- | --- | --- |
| Customer Revenue Leadership Study, Pavilion / 6sense and partners — 793 senior customer growth leaders | 2026 | NRR and GRR plateaued in 2025 after declining 2022–2024; post-sale execution is where the revenue question now sits | `[M]` |
| Benchmarkit, B2B SaaS Performance Metrics Benchmarks (CY2024 actuals, N=225) | 2025 | Median GRR 88%; GRR is best analysed by ACV band | `[M]` |
| Saito & Rehmsmeier, precision-recall vs ROC under class imbalance | 2015 | Why PR-AUC, not ROC, is the threshold-free summary for a rare event | `[A]` |
| Peduzzi et al., events-per-variable rule | 1996 | The sample-size floor for any model fitted on churn outcomes | `[A]` |
| Sapru, "Guardrailed Uplift Targeting", arXiv:2512.19805 | 2025 | Uplift targeting requires a randomised control; propensity targeting mis-allocates effort | `[A]` |
| Cost-sensitive uplift modelling for cross-sell, *Neural Computing and Applications* (Springer) | 2024 | Uplift formulations outperform propensity classifiers on customer profit | `[A]` |
| Kristen Hayer, The Success League — building CS playbooks | 2024–2026 | Score process while a play is new, results once the habit is formed | `[P]` |
| Lincoln Murphy, Sixteen Ventures — success milestones | 2024–2026 | Customer milestones (business outcomes) versus functional milestones as the trigger for advocacy plays | `[P]` |
| GitLab public handbook — CSM escalations | accessed 2026-08 | The deterministic DRI order and the four-tier severity/communication matrix | `[M]` |

**Two figures deliberately not carried here.** A widely-circulated alert-volume statistic
("~45 alerts per CSM per week") and a "playbooks reduced time-to-value by 30%" claim both trace to
single-vendor blog posts with no disclosed sample. The alert-budget number in this library is
derived arithmetically from usable hours instead (`R13`, `../scripts/play_sizing.py`), which is
auditable; the time-to-value claim is simply dropped.
