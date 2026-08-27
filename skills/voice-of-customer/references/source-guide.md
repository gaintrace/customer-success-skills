# The Channel Source Guide

> Every feedback channel is a biased instrument pointed at a self-selected population. This file
> says what each one measures, what it systematically distorts, and the sentence you must attach
> before quoting a number from it.

**Contents**
1. [The instrument principle](#1-the-instrument-principle)
2. [Channel register](#2-channel-register)
3. [Solicited instruments — NPS, CSAT, CES, in-app](#3-solicited-instruments)
4. [Response bias — the mechanisms and their corrections](#4-response-bias)
5. [Unsolicited and observed channels](#5-unsolicited-and-observed-channels)
6. [Loss channels — exit interviews, win/loss, downgrade reasons](#6-loss-channels)
7. [Customer Advisory Board](#7-customer-advisory-board)
8. [Triangulation rules](#8-triangulation-rules)
9. [Staleness](#9-staleness)
10. [Source register and excluded claims](#10-source-register-and-excluded-claims)

**Evidence labels** — carried through from the research pack and never blurred:
`[M]` measured benchmark from a named study with sample and period · `[V]` vendor or platform
data, methodology usually unpublished · `[P]` practitioner rule of thumb, no published
measurement · `[A]` academic or peer-reviewed.

---

## 1. The instrument principle

Three questions before any channel's number enters a readout:

1. **Who was asked?** The invited population, its size, and how it was chosen.
2. **Who answered?** The respondents, the response rate by count *and* by ARR, and the role mix.
3. **What is the unit?** A person, a ticket, an interaction, or an account. Mixing units is the
   most common arithmetic error in VoC work — an account-level claim built from person-level
   responses over-weights whichever account had the most talkative users.

A channel that cannot answer all three does not produce a number. It produces verbatims, which
are still valuable — code them, attribute them, and mark the theme's evidence as
qualitative-only.

**Nothing is pooled.** A support CSAT of 4.6/5 and a relationship NPS of 22 do not average.
They are different questions asked of different people at different moments about different
things. Triangulate at theme level (§8), never at score level.

---

## 2. Channel register

| Channel | Solicited? | Unit | Population it reaches | Best at | Worst at |
| --- | --- | --- | --- | --- | --- |
| **Relationship NPS** | Yes | Person → account | Whoever is on the contact list | Tracking a named respondent's trajectory over time | Representing an account, or a base, from a low response rate |
| **Transactional CSAT** | Yes | Interaction | People who just had an interaction | Judging one interaction type (support, onboarding) | Anything about the relationship or the product |
| **CES** | Yes | Interaction | Same as CSAT | Post-support and post-onboarding effort | Relationship measurement — it was never designed for it |
| **In-app micro-survey** | Yes | Session | Active users only, by definition | Feature-level reaction while the memory is fresh | Anyone who has stopped using the product — the exact population you need |
| **Support ticket text** | No | Ticket | Anyone with a problem *and* the willingness to file | Volume, specificity, reproducibility, severity | Silent dissatisfaction; accounts steered to Slack or email |
| **Call transcripts** | No | Interaction | Whoever attends meetings | Unfiltered severity-3 material and the buyer's own language | Accounts with no meetings; recording-consent gaps |
| **Unsolicited email** | No | Interaction | The motivated minority | Escalation-grade material | Anything proportional — one sender can dominate a quarter |
| **Churn exit interview** | Yes | Account | Whoever is left after the decision | Confirming the *decision path* and who made it | The **cause** — see §6, this is the most misleading channel in CS |
| **Win/loss interview** | Yes | Deal | Buyers willing to speak post-decision | Competitive positioning and evaluation criteria | Small samples; interviewer identity changes the answers |
| **Sales-loss notes** | No | Opportunity | The rep's own account | Speed | Objectivity — reps rarely record "I lost on discovery" |
| **Community / idea portal** | No | Post | Power users and enthusiasts | Depth, workarounds, and cross-account confirmation | Representativeness — vote counts favour organised users |
| **Review sites (G2, Peer Insights)** | Semi | Review | Incentivised or campaign-recruited reviewers | Competitive framing and public objections | Sentiment level — review campaigns select for promoters |
| **CAB** | Yes | Session | Your largest, most invested customers | Strategy, roadmap direction, willingness to co-develop | The mainstream and the unhappy — the CAB is a survivor cohort |
| **Social / analyst mentions** | No | Post | Public commenters | Early warning on a public failure | Volume-to-meaning ratio |

**Print every row, including channels you do not have.** An absent channel is a finding, and it
belongs in the Coverage Ledger, not in a footnote.

---

## 3. Solicited instruments

### 3.1 Relationship NPS

| Field | Detail |
| --- | --- |
| **Question** | "How likely are you to recommend us to a colleague?" 0–10 |
| **Computation** | `% promoters (9–10) − % detractors (0–6)`; passives (7–8) count in the denominator only |
| **Valid cadence** | Twice a year per respondent; never more often than quarterly per person |
| **Benchmarks** | B2B Software & SaaS average **41** `[V · Retently NPS benchmarks, 2026 · platform data, industries with >10 clients, ≥10,000 surveys]`. B2B median ≈**38** `[V · Survicate, reported secondhand]`. 2026 median ≈**30** `[V · SurveySparrow, reported secondhand]`. Working read: medians cluster **30–41**; treat >40 as above median and >50 as strong `[V/P]` |
| **Valid use** | The **trajectory of a named respondent**, and the detractor ratio within an account |
| **Invalid use** | A company-level score reported as "the voice of the base" without its response rate and ARR coverage |

**What the literature actually says.** Reichheld's 2003 *Harvard Business Review* article "The
One Number You Need to Grow" claimed the recommend question was the best available predictor of
return business and word of mouth. Keiningham et al. (2007, *Journal of Marketing*) tested that
longitudinally and questioned whether NPS reliably predicts revenue growth `[A]`. Hayes (2008,
*Quality Progress*) found the recommend question "does not measure anything different from other
conventional loyalty-related questions" `[A]`. The practical conclusion is not that NPS is
worthless — it is that **the level is a weak predictor and the transition is the signal**: a
promoter who becomes a detractor, or a named respondent dropping ≥3 points, carries far more
information than the aggregate.

Buffer's public NPS-vs-churn analysis found 0-scorers churned most, 1–6 clustered similarly, and
7–10 churned least — i.e. the promoter/passive/detractor cut is coarser than the data warrants
`[V]`. The LSE study frequently cited for a ~0.24 correlation between NPS and revenue growth
circulates almost entirely secondhand; **do not quote it as a benchmark.**

**Mandatory caveat sentence** (copy and fill):

> NPS **<score>** from **<n>** respondents at **<m>** accounts, a **<r>%** response rate covering
> **$<X>** of **$<Y>** in-scope ARR (**<z>%**). Respondents skew **<role mix>**. This is the
> score of the people who answered; the **<100−z>%** of ARR that did not answer is not
> represented here.

### 3.2 CSAT

| Field | Detail |
| --- | --- |
| **Computation** | `responses rated 4–5 (or ≥8/10) ÷ total responses × 100` |
| **Valid cadence** | Transactional, per interaction |
| **Benchmarks** | Cross-industry average ≈**78/100**, >80 good, top quartile ≥86 `[P]`. B2B SaaS support CSAT ≈**68%** (Enterprise 72–75%, SMB 60–65%) `[P]` — **this conflicts with other sources reporting ≈80%.** CSAT benchmarks are unreliable across sources; benchmark against your own trailing 12 months instead |
| **Ceiling effect** | CSAT compresses at the top. Most scales are effectively 3-point in practice (bottom box / middle / top box), so a move from 4.6 to 4.4 can be a large real change. Report **bottom-box count**, not just the mean — two 1-star ratings inside 60 days is a stronger signal than a 0.2 mean drop |
| **Invalid use** | Treating support CSAT as relationship health. It measures the interaction, and high-volume accounts simply have more chances to be dissatisfied |

### 3.3 CES

| Field | Detail |
| --- | --- |
| **Question** | "How easy was it to <complete the task>?" typically 1–7 |
| **Benchmarks** | Medians cluster **4.8–5.6** on a 7-point scale; B2B software support 5.4–5.8; top quartile ≥6.2 `[P]` |
| **Valid use** | Post-support and post-onboarding. CES is the strongest of the three at predicting repurchase for **service** interactions |
| **Invalid use** | As a relationship metric. It has no construct validity outside a specific task |
| **Trap** | Question-wording drift. Change the wording and the series breaks; version the question text alongside the taxonomy version |

### 3.4 In-app micro-surveys

Highest response rates of any solicited instrument, and the most structurally biased: they can
only reach people who are still using the product. **The population you most need to hear from —
accounts whose usage has collapsed — is definitionally excluded.** Pair every in-app programme
with an out-of-app instrument for accounts below a usage floor, or state in the readout that
disengaged accounts are unrepresented.

---

## 4. Response bias

| Mechanism | Who it over-represents | Who it under-represents | Correction |
| --- | --- | --- | --- |
| **Self-selection** | People with an extreme experience, good or bad | The satisfied-but-indifferent middle | Report bottom-box and top-box counts separately; expect bimodality and do not describe the mean as "sentiment" |
| **Availability** | Daily power users, admins | Economic buyers and executive sponsors | Report **role mix**. Survey the buying committee, not only the daily user — a B2B renewal is decided by people who rarely open an in-app survey |
| **Recency** | Anyone who just had an interaction | Accounts with no recent touch | Report days-since-last-interaction for respondents vs non-respondents |
| **Relationship capture** | Accounts with an attentive CSM who chases responses | Unowned, pooled and tech-touch accounts | Report response rate by coverage model; a CSM-chased response is not a random draw |
| **Channel reach** | Whoever the instrument can physically reach (in-app → active users) | The disengaged | Pair in-app with email; state the exclusion |
| **Language / region** | The primary-language, primary-timezone base | Everyone else | Report response rate by region |
| **Survey selection (integrity risk)** | Whoever the sender chose | Whoever they avoided | Sampling rules owned by Ops, not by CSMs; track response rate as its own measure `[P]` |

**Correcting for composition.** Post-stratification reweights respondent scores so segment ARR
shares match the base:

```
ARR-weighted score = Σ_segments ( ARR_share_of_segment × mean_score_within_segment )
Minimum cell size  = 5 responses per segment; below that, print UNKNOWN for that segment
```

State the limitation every time: **this corrects observable composition only.** It cannot correct
the unobservable difference between people who answer and people who do not, and it produces a
false sense of rigour if presented without that sentence. Qualtrics puts the general principle
plainly — a low response rate "may reflect bias in terms of who took the survey", and there is no
agreed universal threshold at which a response rate becomes acceptable `[V · Qualtrics response-rate
guidance, accessed 2026]`. So do not publish a pass/fail threshold; publish the gap.

**Sentiment coverage is the master number.**
`ARR of accounts with ≥1 feedback record in trailing 12 months ÷ in-scope ARR`. Below roughly
**50% ARR coverage**, the sentiment section of a report is anecdote rather than measurement
`[P]`. Print it in the Bottom Line block, not in an appendix.

**The Silent ARR table is mandatory.** It is the only part of a VoC readout that describes the
population everyone else ignores:

| Segment | Accounts with zero feedback (12m) | ARR | % of segment ARR | Renewals ≤120d | ARR at those renewals |
| --- | --- | --- | --- | --- | --- |

Silence is a derived absence metric — nothing generates a row for it, so a scheduled computation
must. Pair it with `churn-risk`: an account that has said nothing in twelve months and is inside
its opt-out window is not neutral, it is unmeasured.

---

## 5. Unsolicited and observed channels

### 5.1 Support ticket text

The highest-volume, highest-specificity feedback most companies own and never read as feedback.

| Use it for | Do not use it for |
| --- | --- |
| Repeat-issue clustering (≥3 tickets in one cluster in 180 days) | Sentiment level — ticket text is negative by construction |
| Reopen reasons — a reopen carries more information than a new ticket | Account-level satisfaction |
| Feature requests with the use case attached (`ticket.type = feature_request`) | Volume as a health proxy — high volume also correlates with high adoption |
| Severity assessment, because tickets describe consequences concretely | Anything about accounts that file no tickets |

**The bimodal rule:** both extremes are risk. Zero tickets in twelve months often means nobody is
using the product; a high sustained rate indicates friction `[P]`. Build it as a two-sided flag,
never as "fewer tickets = healthier".

### 5.2 Call transcripts

Where severity-3 material lives, because people say in a meeting what they will not type into a
form. Conversation-intelligence research reports that a small minority of communications contain an
actionable signal — Sturdy AI puts it at roughly **17% of communications**, drawn from a corpus
of 31.1M conversations `[V · Sturdy AI, secondhand; primary publication not verified]`. Treat
that as directional motivation for reading transcripts, not as a benchmark to reproduce.

Coding rules: code the customer's words, not the CSM's summary; attribute the mention to the
speaker's `contact.role`; and record whether the economic buyer was in the room, because a
severity-3 statement made by an admin and one made by the buyer carry different weight in §8
ranking.

### 5.3 Unsolicited email and shared Slack channels

Rich and radically disproportionate. One motivated sender can generate a quarter's worth of
mentions. **Cap mentions at one per account per channel per theme per period** before counting —
this single rule prevents the loudest-customer failure at the arithmetic level rather than by
willpower.

### 5.4 Community, idea portals and review sites

| Channel | What it is genuinely good for | The distortion |
| --- | --- | --- |
| Community / forum | Confirming a theme exists across accounts, and capturing the workaround customers invented | Vote counts reward organised users, not large ones. Never rank by upvotes |
| Idea portal | Linking a request to an account and an ARR value | Portals collect *solutions*; recode every entry to the underlying problem before it enters the taxonomy |
| G2 / Gartner Peer Insights | The public objection a prospect will read, and competitive framing in the customer's own words | Review campaigns recruit promoters; the level is a marketing artifact, the text is not |

Public reviews belong in the **Firmographic & external** family, not in Sentiment & VoC — they
are the outside world's read, and they are the version your prospects and your customer's
procurement team will see.

---

## 6. Loss channels

### 6.1 Churn exit interviews — why they are systematically misleading

This is the most-trusted and least-reliable channel in customer success. Five compounding
mechanisms, all pointing the same way:

| Mechanism | Effect on the answer |
| --- | --- |
| **Post-decision rationalisation** | The reason is constructed *after* the decision to justify it. You are collecting a narrative, not a cause |
| **Face-saving** | "Too expensive" is blameless and ends the conversation. "We never got it working" implicates the customer's own team as much as yours |
| **Wrong respondent** | The person available at wind-down is usually the admin managing the exit, not the economic buyer who decided |
| **Wrong window** | The decision was made 3–12 months earlier. You are asking about a period the respondent is not recalling |
| **Interviewer identity** | The customer is answering the vendor they are leaving. Politeness suppresses the specific and the critical |

Net effect, consistent across practitioner accounts: **stated churn reasons over-report price and
under-report "we never got it working"** `[P]`.

**How to use it anyway.** Exit interviews are strong evidence about the **decision path** — who
decided, when, what alternatives were considered, what would have changed it — and weak evidence
about cause. So:

1. Record `churn_event.primary_reason` as the customer stated it, verbatim, unaltered.
2. Reconstruct the timeline separately (`churn-postmortem`) and record `assessed_cause` with its
   evidence. Never overwrite one with the other.
3. Report both columns in every register row that draws on loss data.
4. Run the what-would-have-to-be-true test (SKILL.md Step 7) on every "price" answer. Compare the
   citing accounts' adoption against the renewed cohort. If adoption is materially lower, price
   is the language and value is the cause.

### 6.2 Win/loss interviews

Better than exit interviews on two axes: the buyer has less to lose by being candid, and the
interview is often conducted by a third party rather than the account owner, which removes the
politeness suppression. Vendors in this category (Clozd is the named example) publish customer
outcomes rather than methodology research — e.g. a customer reporting that **60% of their loss
interviews contained clear signals for future re-engagement** `[V · Clozd customer case study]`.
Use figures like that as motivation, never as a benchmark.

Practical rules: interview both wins and losses (losses-only produces a distorted picture of your
own strengths), record the buyer's decision criteria in their words, and code loss themes into
the **same taxonomy** as retention themes — a competitive gap that loses new deals and a feature
gap that loses renewals are frequently the same theme, and splitting them across two systems is
how a company funds neither.

### 6.3 Sales-loss notes and downgrade reasons

`opportunity.loss_reason` is fast and close to useless as written — reps select from a picklist
under time pressure and rarely record their own execution as the cause. Treat a picklist loss
reason as an **unverified claim** requiring a second source before it enters a theme's evidence.
Downgrade and seat-reduction reasons are more reliable, because a downgrade is a considered act
with a paper trail; capture them at the point of the change, not at the next renewal.

---

## 7. Customer Advisory Board

| Good for | Bad for |
| --- | --- |
| Direction — is this the right problem to solve at all | Prioritisation across the base |
| Strategy-level reaction to roadmap themes | Anything about SMB, new customers, or the unhappy |
| Recruiting design partners and co-development | Sentiment measurement of any kind |

The CAB is a **survivor cohort**: large, invested, well-served customers who accepted an
invitation. Every theme that comes out of a CAB session must be re-tested against the coded
corpus before it enters the register, and CAB-only themes are labelled as such. A theme with
strong CAB support and no mentions anywhere else is a hypothesis, not a finding.

---

## 8. Triangulation rules

A theme is **confirmed** when it appears in ≥2 independent channels across ≥3 accounts. Channels
are independent when they reach different populations — a support ticket and a support CSAT
comment about the same ticket are one channel, not two.

| Evidence state | Label in the register | What you may recommend |
| --- | --- | --- |
| ≥3 channels, ≥5 accounts, ≥2 segments | **Confirmed** | An irreversible investment (roadmap commit, staffing change) |
| 2 channels, ≥3 accounts | **Supported** | A reversible action (research spike, doc fix, targeted outreach) |
| 1 channel, or <3 accounts | **Anecdotal** | Investigation only. Name the test that would promote it |
| CAB or exec-escalation only | **Unreplicated** | Re-test against the corpus before routing |

---

## 9. Staleness

| Feedback type | Treat as current for | Then |
| --- | --- | --- |
| Survey response (NPS/CSAT/CES) | 90 days | Historical fact, not current signal — a six-month-old NPS describes a past state |
| Call transcript | 45 days | Re-confirm before quoting to an executive |
| Support ticket text | 90 days for themes; indefinitely for repeat-issue clustering | — |
| Exit interview | Never expires as a record; never current as a signal | It describes an account that has already gone |
| Community / review post | 180 days | Public posts stay visible long after they stop being true |

**The respondent-departure rule.** If the respondent has left the company
(`contact.email_status = hard_bounce`, or `departed_at` set), their score is **void, not neutral**
— remove it from the current-period aggregate and say you did. A promoter score belonging to a
departed champion has been the single most reassuring number on many accounts that churned.

---

## 10. Source register and excluded claims

| Source | Type | Year | What it supports here |
| --- | --- | --- | --- |
| Reichheld, *The One Number You Need to Grow*, Harvard Business Review | Origin article | 2003 | The NPS construct and its original claim |
| Keiningham, Cooil, Andreassen, Aksoy, *Journal of Marketing* | `[A]` peer-reviewed | 2007 | Longitudinal challenge to NPS as a predictor of revenue growth |
| Hayes, *Quality Progress* | `[A]` peer-reviewed | 2008 | Recommend question is not distinct from other loyalty questions |
| Krippendorff, content-analysis reliability convention | `[A]` methodological standard | — | α ≥ 0.800 publish · 0.667–0.800 tentative · <0.667 discard |
| Retently, NPS benchmarks | `[V]` platform data | 2026 | B2B Software & SaaS average NPS 41; ≥10,000 surveys, industries with >10 clients |
| Survicate; SurveySparrow NPS benchmarks | `[V]` secondhand | 2025–26 | B2B median ≈38; 2026 median ≈30 |
| Bain & Company, Net Promoter System | `[V]` practitioner framework | ongoing | Inner loop / outer loop; closing the loop with customers |
| *Customer Revenue Leadership Study* (Pavilion / 6sense, ≈800 customer and post-sales leaders) | `[M]` industry survey | 2025 | 73% of CS leaders say their health score does not reliably predict churn |
| Enterpret | `[V]` vendor | 2026 | Adaptive vs fixed taxonomy framing; multi-source feedback unification |
| Clozd customer case studies | `[V]` vendor | 2026 | Win/loss programme outcomes; third-party interviewer practice |
| Sturdy AI research (secondhand; primary publication not located) | `[V]` vendor research | 2023–25 | ≈17% of communications contain a signal; 31.1M-conversation corpus |
| Buffer open NPS/churn analysis | `[V]` public company data | — | Detractor band is coarser than the 0–6 cut implies |
| Qualtrics, response-rate guidance | `[V]` vendor guidance | accessed 2026 | Low response rate implies bias; no agreed universal threshold |
| Kristen Hayer, *The 7 Components of a Health Score* | `[P]` practitioner | 2017 | "One NPS score by itself isn't enough"; CSM assessment as a component |
| Lincoln Murphy, *Desired Outcome / Success Milestones* | `[P]` practitioner | ongoing | Churn as symptom; the value path as the coding lens |

### Claims deliberately excluded — do not cite

| Claim | Why excluded |
| --- | --- |
| "VoC leaders see 41% faster revenue growth, 49% faster profit growth, 51% better retention (Forrester 2024)" | Circulated secondhand through vendor glossaries; the primary Forrester publication is not verifiable. Do not cite it at all — not with a caveat, not as directional |
| "Strong VoC initiatives produce a 55% boost in retention (Aberdeen)" | No year, no methodology, secondhand only |
| "LSE found a 0.24 correlation between NPS and revenue growth" | Cited almost entirely secondhand; primary study not located |
| Any single "the average B2B SaaS survey response rate is X%" figure | Sources are mutually inconsistent and none publish methodology. Report **your own** response rate; do not benchmark it |
| "NPS predicts churn" as a general statement | The peer-reviewed record does not support it. The defensible claim is that a **transition** in a named respondent's score is a signal |
