# Attribution — Contribution, Not Cause

> You changed one input to a system you do not control, run by people you do not manage, during
> a year in which many other things also changed. Every sentence in a value case has to be true
> at that level of claim. This file is about the difference between a sentence that survives a
> finance review and one that ends the conversation.
>
> Evidence labels: `[M]` measured · `[V]` vendor-published · `[P]` practitioner convention ·
> `[A]` academic.

**Contents**
- [1. The claim you are actually entitled to make](#1-the-claim-you-are-actually-entitled-to-make)
- [2. The attribution ladder A1–A4](#2-the-attribution-ladder-a1a4)
- [3. Difference-in-differences](#3-difference-in-differences)
- [4. The confounder checklist](#4-the-confounder-checklist)
- [5. Sentence structures that survive a finance review](#5-sentence-structures-that-survive-a-finance-review)
- [6. Getting the customer to set α](#6-getting-the-customer-to-set-)
- [7. The attribution register](#7-the-attribution-register)
- [8. When attribution cannot be established](#8-when-attribution-cannot-be-established)
- [9. Failure modes](#9-failure-modes)

---

## 1. The claim you are actually entitled to make

| You observed | You may claim | You may not claim |
| --- | --- | --- |
| Usage rose and their metric improved | That both happened, with dates | That one caused the other |
| Their metric improved and a comparable untreated team's did not | The difference, as attributable | The whole movement |
| The customer says it was mostly you | Their stated share, with their name on it | A different share you prefer |
| A cost line was removed from their budget | The removal, in full | Anything about the counterfactual — it already happened |

**Contribution language is not hedging.** "We contributed 70% of a 3.5-day improvement, and here
is who set that figure" is a stronger claim than "we saved you 3.5 days", because it is one the
reader can check and therefore one they can repeat. Vagueness is hedging; a bounded, sourced
share is precision.

The corollary: **α is never 1.0.** A silent 100% is the first thing a finance reviewer tests,
and finding it reclassifies the whole document from analysis to sales collateral in one sentence.
The only exception is a cash-releasing event with no other possible cause — a contract they
cancelled because the capability now lives in your product — and even there, write down why no
other cause exists.

## 2. The attribution ladder A1–A4

| Level | Evidence | Permits | Typical α range | How to write it |
| --- | --- | --- | --- | --- |
| **A1** | Treated vs untreated group over the same window (designs D1–D3 in `baseline-methods.md`) | A dollar figure at the difference-in-differences value | Implied by the arithmetic, not chosen | "Fell 31% in the teams using it and 4% in the teams without, same quarter, same definition" |
| **A2** | Pre/post with a stated counterfactual and every known confounder named | A dollar figure, with the confounders printed beside it | 0.4–0.8 | "Improved 3.5 days. Two other changes ran in the same period; both are named below" |
| **A3** | Customer-attested share, set by them in writing | A dollar figure at their α, with their name on it | Whatever they say | "Priya attributes 70% here and 30% to the knowledge-base rewrite" |
| **A4** | Correlation only — usage rose, the metric moved | **No dollar claim** | — | "Usage rose 3× and the metric improved 22%. We have not established what share is ours" |

**A1 beats A3 on rigour; A3 beats A1 on portability.** A customer-set share travels through an
organisation because the customer's own name is on it. Where you can produce both, produce both:
run the difference-in-differences and then ask them to confirm the share it implies. That
combination is the strongest artifact this skill can produce.

## 3. Difference-in-differences

**(treated change) − (untreated change over the same window).** The strongest read available
without a formal study, and cheap when a phased rollout already exists.

| Step | Do | Check |
| --- | --- | --- |
| 1 | Choose the comparison group | Same function, similar size and workload mix, similar pre-period level |
| 2 | Fix one metric definition for both | A different query for each group invalidates the whole comparison |
| 3 | Fix one window for both | Same calendar dates, covering the same seasonal ground |
| 4 | Compute each group's change | Percentage and absolute, both |
| 5 | Subtract | The difference is the claim; the treated group's own change is not |
| 6 | Test the assumption | Were the two groups moving in parallel *before* the intervention? If they were diverging already, the comparison is contaminated |

**Regression to the mean is the trap.** The most extreme group in a pre-period tends to move
toward the middle regardless of any intervention, purely because the two measurements are not
perfectly correlated `[A]`. If you chose the treated group *because* they were the worst
performer, some of their improvement was always going to happen. Say so, or choose a comparison
group with a similar pre-period level and let the design handle it.

**When there is no untreated group, an interrupted time series is the fallback:** model the
pre-period trend, project it forward, and compare. It requires enough pre-period points to
establish a trend, and it is only as good as the seasonality in the model — a misspecified
seasonal term biases the counterfactual and therefore the estimate `[A]`. Report it as A2, never
as A1.

## 4. The confounder checklist

Walk this every time, and record the answers even when they are "none". A confounder the
customer names that you did not is worse than a confounder you both knew about.

| Category | Ask | Why it matters |
| --- | --- | --- |
| **Their other programmes** | "What else changed for this team in the period?" | Process rewrites, training, a new manager, a Lean project |
| **Other vendors** | "Did anything else go live that touches this workflow?" | The adjacent tool that also claims the same saving |
| **Headcount** | "Did the team grow or shrink?" | A rate metric handles this; a count metric does not |
| **Volume and mix** | "Did the work itself change?" | Easier cases arriving looks exactly like better throughput |
| **Seasonality** | "Where does this sit in your calendar?" | See `baseline-methods.md` §8 |
| **Pricing or packaging** | "Did anything change commercially?" | A price change alters their volume, which alters every rate |
| **Reorg** | "Is this the same team it was?" | Same label, different people, incomparable series |
| **Measurement** | "Did the definition or the tooling change?" | Better detection can make a true improvement look like a decline |
| **Regulation or market** | "Anything external?" | Sector-wide movement is not your effect |

Print the ones that apply next to the benefit line. Two named confounders and a stated α reads
as rigour. Zero named confounders reads as not having looked.

## 5. Sentence structures that survive a finance review

| Do not write | Write | Why the second survives |
| --- | --- | --- |
| "We saved you 4,100 hours." | "Your close moved from 9 days to 5.5. Of the 3.5 days, Priya attributes 70% here and 30% to the reconciliation rewrite." | Names the observable, the share and the person |
| "Our platform reduced tickets 31%." | "Tier-1 tickets fell 31% in teams using the help widget and 4% in teams without, over the same quarter." | Contains its own counterfactual |
| "This drove $1.2M in revenue." | "Deals using the workflow closed 9 days faster. At the 40% attribution you set, that is $480k on last year's volume." | Gross and attributed, with the setter named |
| "ROI is 4.2×." | "On the conservative case — 40% attribution, 50% recapture — ROI is 2.1×; central is 4.2×." | Leads with the number that survives challenge |
| "Value delivered: $2.6M." | "$18.40 per ticket avoided × 141,000 tickets. Your cost per ticket, your ticket count." | Invites verification instead of belief |
| "Adoption is up, so the programme is working." | "Adoption rose from 41% to 78%. The business metric has not moved yet; the lag on this driver was estimated at two quarters." | Separates the input from the outcome |
| "The improvement is thanks to the platform." | "Three things changed in that period. Here they are, and here is the share the team's own director assigns to each." | Pre-empts the question rather than losing to it |
| "We estimate a 30% efficiency gain." | "They measured 31% in Claims. We have not measured Billing and are not claiming it." | Refuses to extend a measurement past its evidence |

**The rehearsal test.** Read each sentence and ask: *if their CFO asked "where does that number
come from?", is the answer already in the sentence?* If not, rewrite it until it is. A number
whose source lives in a footnote is a number that will be challenged out loud.

## 6. Getting the customer to set α

The single highest-return move in the whole skill, and it takes one question.

| Move | Say | What it produces |
| --- | --- | --- |
| **Frame it as fairness, not modesty** | "I do not want to claim credit for the work your team did. How would you split this?" | A share they own, and goodwill |
| **Offer a starting point they can push against** | "I would have said two-thirds us, one-third the process change — does that match how you see it?" | An anchored, quick answer instead of a blank page |
| **Ask for the other causes by name** | "What else moved this number?" | The confounder list, from the person who knows |
| **Write it back to them** | "So: 70% here, 30% to the knowledge-base rewrite. Correct me if that is wrong." | A dated written record, which is what the artifact cites |
| **Never argue upward** | If they say 40%, use 40% | The number's value comes from being theirs. Negotiating it destroys the thing that made it useful |

**Who to ask.** The person who owns the metric, not the person who signed the contract. The
owner knows what else changed; the signer knows what they were told. Where they differ, use the
owner's number and tell the signer whose it is.

## 7. The attribution register

One row per benefit line. This table is what a Defend-mode run leads with.

| # | Benefit | Level | Basis | α | Set by | Date · medium | Confounders named |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Tier-1 deflection | A1 | Claims live 2026-04, Billing not live until 2027-01; same query both | 0.70 implied | Difference-in-differences | 2026-08-24 · computed | KB rewrite Feb–May; pricing change 2026-06-01 |
| 2 | Claims cycle time | A3 | Their Controller's split | 0.70 | J. Alvarez, Controller | 2026-08-14 · email | Reconciliation rewrite Q1 |
| 3 | Retired tool | — | Contract cancelled 2026-05-31; capability replaced | 1.00 | Cash-releasing; no counterfactual required | 2026-06-02 · their procurement record | — |
| 4 | Invoice exceptions | A2 | Pre/post, no comparison group available | 0.50 | Us, disclosed as ours | 2026-08-24 | New approval step added March |

Row 3 shows the one legitimate α = 1.0: a cash event with no alternative cause, and the reason
written down. Row 4 shows the honest form of a weak level — α set by us, **said to be** set by
us, at a deliberately conservative value.

## 8. When attribution cannot be established

Say it, make it actionable, and refuse to fake it. This is `4G`: decisive about the gap.

> **Attribution unestablished for the onboarding-time line — A4.** Onboarding time fell from 14
> days to 6 over the same period that two other changes landed: the new starter checklist (March)
> and the team's move under a different director (May). We have no untreated group and no
> customer-set share, so **we are not putting a dollar figure on this line.** What would close
> it: Devin's team keeps the old process for the Southern region through Q4, which gives a
> comparison group by January — or Devin states a share, which takes ten minutes.

What that paragraph does: names the level, names the confounders, refuses the number, and gives
two concrete routes with owners. Compare it with *"onboarding improvements may also have
contributed"*, which commits to nothing and gives the reader nothing to do.

**The commercial argument for refusing.** A line you decline to monetise costs you one number in
one artifact. A line their finance team disproves costs you every number in every artifact,
including the correct ones — and the correct ones are usually the majority.

## 9. Failure modes

| Failure | Correction |
| --- | --- |
| Silent 100% attribution | State α with its level; the only 1.0 is a cash event with the reason written down |
| α set by us and presented as theirs | Name the setter on the artifact; ours caps the band at Evidenced |
| Gross movement presented as attributed | Report both, side by side, always |
| Confounders discovered by the customer | Ask "what else changed?" at capture time and record the answer |
| Comparing groups that were already diverging | Check parallel pre-trends before claiming a difference-in-differences |
| Treating the worst-performing team as the treated group without saying so | Name the regression-to-the-mean risk `[A]` or match on pre-period level |
| Attribution claimed across a reorg, a pricing change or a seasonal peak | Name the event, or do not claim across it |
| A4 correlation converted into a dollar figure | A4 produces no dollar claim, in any wording |
| Negotiating a customer's α upward | Use their number. Its value is that it is theirs |
| Attribution set once and never revisited | Re-attest on sponsor change and at every quarterly refresh |
