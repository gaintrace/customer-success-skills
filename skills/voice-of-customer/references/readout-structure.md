# The Quarterly VoC Readout

> The register is the analysis. The readout is the decision meeting. This file holds the
> architecture, the executive question bank with prepared answers, the decision menu, the
> closed-loop mechanics, and the metrics that judge the programme itself.

**Contents**
1. [What the readout is for](#1-what-the-readout-is-for)
2. [Architecture and time allocation](#2-architecture-and-time-allocation)
3. [Why representativeness goes first](#3-why-representativeness-goes-first)
4. [The executive question bank](#4-the-executive-question-bank)
5. [The decision menu](#5-the-decision-menu)
6. [Handling the three standard challenges](#6-handling-the-three-standard-challenges)
7. [Closing the loop](#7-closing-the-loop)
8. [Cadence](#8-cadence)
9. [Measuring the programme itself](#9-measuring-the-programme-itself)
10. [Readout anti-patterns](#10-readout-anti-patterns)

---

## 1. What the readout is for

Not to report sentiment. Not to prove CS is listening. The readout exists to **move a fixed
number of themes from unowned to owned, with a date on each** — and to tell the base what
happened to the feedback they gave you.

Judge it by one test: *how many named owners left the room with a dated commitment they did not
have when they walked in?* Zero is a failed readout no matter how good the analysis was. If the
capacity gate said the receiving functions could absorb four themes, four owners is the target.

A secondary purpose, usually undervalued: the readout is where the company decides what it is
**not** going to do, on the record, so that CS can tell customers honestly rather than deferring
the answer for another quarter.

---

## 2. Architecture and time allocation

For a 45-minute exec staff slot. Scale proportionally for 30 or 60.

| # | Section | Minutes | Purpose | Who talks |
| --- | --- | --- | --- | --- |
| 1 | **Bottom line + the ask** | 3 | Top themes, ARR attached, the decisions being requested | VP CS |
| 2 | **Who spoke and who did not** | 4 | The representativeness statement and Silent ARR | VP CS |
| 3 | **Theme register** | 8 | The ranked table, read top-down; do not narrate every row | VP CS |
| 4 | **Top themes, one card each** | 12 | Evidence, symptom vs cause, renewal exposure, the decision requested | VP CS, then the proposed owner responds |
| 5 | **Disagreements — say vs do** | 4 | The accounts where sentiment and behaviour conflict | VP CS |
| 6 | **Decisions** | 10 | Owner and date on each theme, live in the room | Exec staff |
| 7 | **Not doing, and why** | 3 | The themes below the cut, with reconsider triggers | VP CS |
| 8 | **Loop closure scorecard + instrument health** | 1 | Last quarter's commitments and the survey programme's own health | VP CS |

**Rules of construction**

- Section 6 is the meeting. Sections 1–5 exist to make it possible. If the clock is under
  pressure, cut section 3 to the top five rows, never section 6.
- Every theme card fits on one screen. If it does not, the theme needs the split test.
- Verbatims are read aloud, in the customer's words, with the account and date. A quoted customer
  changes a room in a way a bar chart does not — but three verbatims, not fifteen.
- No section presents sentiment without behaviour beside it. That is section 5's whole job, and
  it is the section most likely to be cut for time and most likely to change a decision.
- The prior quarter's decisions appear in section 8 with their status. A programme that never
  reports back on its own commitments teaches the room that commitments are optional.

---

## 3. Why representativeness goes first

Because after the first number is on screen, nobody re-evaluates the sample. Put the sample
first and every subsequent number is read correctly.

**The opener, filled in:**

> This quarter we coded **<N>** mentions from **<M>** accounts representing **$<X>** of **$<Y>**
> in-scope ARR — **<Z>%** coverage. Respondents skew **<role mix>** and **<segment skew>**.
> **$<S>** of ARR across **<A>** accounts has given us no feedback of any kind in twelve months,
> and **$<R>** of that decides inside the next 120 days. Everything below is what the accounts
> that spoke are telling us; it is not a measurement of the base.

Three numbers make this concrete and each has a decision attached:

| Number | Decision it drives |
| --- | --- |
| ARR coverage % | Whether the sentiment section is evidence or anecdote. Below ~50% ARR coverage it is anecdote `[P]` — say so and cap confidence |
| Silent ARR with renewals ≤120d | An outreach work order for CS, not a footnote |
| Role mix | Whether the themes carry weight with the people who sign contracts, or only with daily users |

---

## 4. The executive question bank

Prepare every one of these. They arrive in roughly this order, and an unprepared answer to any of
them costs the register its credibility for the rest of the meeting.

| Question | What they are really asking | The prepared answer | Evidence to have ready |
| --- | --- | --- | --- |
| "How many customers is this?" | Is this a pattern or an anecdote | Accounts and ARR, never mention count | Reach %, account list, segment split |
| "Which customers?" | Do I know these names, and do they matter | The named accounts, largest ARR first, with health band | Theme card evidence table |
| "Is this new, or have we always had it?" | Am I being shown a trend or a snapshot | Share of voice this period vs prior, with the classification | Movers table, z-screen with its caveat |
| "Didn't we fix this?" | Was my last investment wasted | The post-ship mention curve, days 30–90 after release | Ship date, mention rate before and after |
| "Is this just the loud ones?" | Am I being lobbied | The per-account cap rule, plus the segment and ARR splits | Attribution rules §2, rule 4 |
| "What happens if we don't?" | Quantify the downside | Renewal exposure by opt-out deadline, plus suppressed expansion | Exposure table with dates |
| "What would it cost to fix?" | Can I afford it | The owning function's estimate, or `UNKNOWN — requires <function> estimate` with a date | Never an analyst-invented estimate |
| "Do the customers who complain actually use it?" | Is this credible | The behaviour cross-check for the mentioning accounts | Usage per seat vs the renewed cohort |
| "What does Sales hear?" | Does this cost us new business too | Win/loss themes coded into the same taxonomy | Loss-reason cross-tab |
| "Why is our NPS down?" | Give me one cause | Refuse the single cause. Give the respondent-mix change, the theme composition change, and any departed respondents removed | Response rate and role mix, both periods |
| "What do you want from me?" | The ask | One sentence: the decision, the owner you are proposing, and the date | The decision row, pre-drafted |

**The two answers you must be willing to give.** "We do not know, and here is what it would take
to find out" — and "the data does not support that." Both raise the register's credibility. A
confident guess destroys it the first time someone checks.

---

## 5. The decision menu

A readout that requests "attention" gets attention and nothing else. Every theme arrives with a
specific decision type, pre-drafted so the room only has to say yes, no, or defer-until.

| Decision type | Requested of | Shape of the ask |
| --- | --- | --- |
| **Roadmap commit** | Product | "Accept CAP-01 into the H2 roadmap with a target release; owner <name>, decision by <date>" |
| **Defect prioritisation** | Engineering | "Raise REL-03 to P1 with a committed fix date; owner <name>" |
| **Support capacity or process change** | Support | "Fund N hours of macro and knowledge work against the SUP-02 cluster; measure reopen rate at 60 days" |
| **Packaging change** | Pricing | "Move capability X out of the Enterprise tier, or confirm it stays and CS communicates that; decision at the <date> pricing cycle" |
| **Enablement / docs investment** | Education | "Publish the three articles answering the exact questions in ADP-03; measure ticket deflection at 60 days" |
| **Named save motion** | CS | "Run the save play on the four At Risk accounts citing INT-02 before their opt-out dates" |
| **Sales process change** | Sales | "Add the scope check to the handover checklist; measure ONB-04 mentions in the next new-customer cohort" |
| **Stop asking** | VP CS | "Retire the monthly in-app survey; response rate has fallen from X% to Y% and loop closure is Z%" |
| **Explicit decline** | Any | "We are not fixing CAP-04 this year. CS will tell the six accounts who raised it, with the reason, by <date>" |

The explicit decline is the most valuable row on the page and the one most often left blank. An
undecided theme returns next quarter with more mentions, more ARR and less credibility for the
programme that keeps raising it.

---

## 6. Handling the three standard challenges

**"This is just the loudest customers."** Answer with mechanism, not assertion: mentions are
capped at one per account per channel per theme per period, attribution is at account grain, and
ranking is by risk-weighted ARR. Then show the segment split. If the theme genuinely is
concentrated in a handful of accounts, say so — a theme raised by three accounts worth $2M is
still a real problem, just a different one, and it routes to CS rather than to the roadmap.

**"We already knew this."** Two honest responses depending on the facts. If it is a known theme:
show the trend and the ARR that has accumulated since it was last raised, and ask why it is still
unowned — that is the finding. If it is genuinely new information to some of the room and not to
others, that is an internal routing failure worth naming.

**"Sentiment is fine, though."** This is where section 5 earns the meeting. Show the hollow
promoters — accounts scoring 9–10 with core actions down 40% — and the expanding detractors. Then
state the tiebreak rule from `../../cs-context/references/evidence-standard.md` §8: commercial
actions beat relationship, relationship beats usage, usage beats sentiment. **Sentiment is the
weakest signal in the stack**, and a register built on it alone deserves the challenge.

---

## 7. Closing the loop

Two loops, after Bain's Net Promoter System framing: the **inner loop** is the frontline acting
on individual feedback; the **outer loop** is the cross-functional team fixing root causes the
frontline cannot reach `[V · Bain]`.

### 7.1 Inner loop — back to the individual

| Trigger | Owner | Target | Content | Recorded in |
| --- | --- | --- | --- | --- |
| Detractor response (0–6) | CSM | 48 hours `[P]` | Acknowledge, ask one clarifying question, name the next step and a date | `feedback_mention.loop_closed_at` + an `interaction` row |
| Any severity-3 mention | CSM | 48 hours | As above, plus escalation to the account's health review | Same, plus `churn-risk` input |
| Bottom-box CSAT on a substantive ticket | Support lead | 24 hours | Reopen or explain the resolution; never close silently | Ticket + mention |
| Promoter (9–10) from an economic buyer or admin | CSM | 7–14 days, expires at 90 `[P]` | Thank, then the **advocacy** ask — reference, review, case study | Mention + advocacy record |

**Never make the expansion ask in the same conversation as the advocacy ask.** Separate them by
at least two weeks. Combining them converts a goodwill moment into a sales call and costs you
both.

### 7.2 Outer loop — back to the base

Sent to **everyone surveyed, respondents and non-respondents alike.** The non-respondents are
the population whose response rate you are trying to recover, and a note that reaches only the
people who already engaged compounds the response bias instead of correcting it.

Structure of the note (template in `../assets/loop-close-note.md`):

1. What we heard — the top themes, in customers' language, with rough scale ("raised by X% of
   accounts that responded"), never internal ARR figures.
2. What we did — shipped, with dates. This is the section that earns the next response rate.
3. What we are doing next — committed, with a quarter.
4. **What we are not doing, and why.** The section nobody writes. Customers forgive a no; they
   do not forgive silence, and silence is indistinguishable from not listening.
5. How to reach us about it.

Timing: within 30 days of the readout. Same quarter, always — a "you said / we did" note that
arrives six months later reads as an admission that nothing happened for five of them.

### 7.3 The loop-closure scorecard

```
Inner-loop closure rate = closed within SLA / eligible responses
Outer-loop completion   = periods with a published note / periods run
Median days to close    = median(loop_closed_at − occurred_at) for eligible mentions
```

| Rate | Reading | Action |
| --- | --- | --- |
| ≥80% | Working | Publish it; it is the strongest evidence the programme is real |
| 50–80% | Under-resourced | Reduce survey volume before adding any new instrument |
| <50% | Extractive | **Recommend suspending collection.** You are spending goodwill and returning nothing, and response rates fall accordingly |

Loop closure is also the best QBR material the company owns. "You raised this in March, here is
what shipped in June" is a stronger slide than any usage chart — hand it to `qbr-builder`.

---

## 8. Cadence

| Activity | Cadence | Owner | Output |
| --- | --- | --- | --- |
| Mention coding | Continuous or weekly batch | CS Ops | Coded corpus |
| Severity-3 escalation | Within 48 hours of the mention | CSM | Account escalation, `churn-risk` input |
| Inner-loop closure | Per SLA above | CSM / Support | `loop_closed_at` populated |
| Pulse (register + movers) | Monthly | CS Ops | Short register, emergence flags |
| Full readout | Quarterly | VP CS | This document's artifact |
| Outer-loop note | Quarterly, ≤30 days after the readout | VP CS | Published customer note |
| Reliability audit (alpha) | Every coding period | CS Ops | Alpha with sample size |
| Taxonomy version review | Quarterly (themes) / annually (categories) | CS Ops + Product Ops | Version bump and change log |
| Instrument review | Semi-annually, or before any new survey | VP CS | Capacity gate, fatigue check, retire/keep decision |

**Relationship survey timing.** Twice a year per respondent, never more often than quarterly, and
never inside 30 days of a renewal conversation — a survey sent during a negotiation collects
negotiating positions, not sentiment.

---

## 9. Measuring the programme itself

A VoC programme with no metrics on itself has no defence when its budget is questioned.

| Metric | Formula | What good looks like |
| --- | --- | --- |
| **Sentiment ARR coverage** | ARR with ≥1 feedback record in 12m ÷ in-scope ARR | Rising; below ~50% the programme cannot claim to represent the base `[P]` |
| **Themes routed with a named owner** | routed with owner ÷ themes above the cut | 100%. Anything less is an unowned backlog |
| **Decision latency** | median(days from readout to owner's accept/decline) | Inside the SLA in the routing matrix |
| **Theme resolution rate** | themes classified resolved ÷ themes routed 2+ periods ago | The programme's actual output |
| **Inner-loop closure rate** | §7.3 | ≥80% |
| **Outer-loop completion** | §7.3 | 100% of periods |
| **Coding reliability** | Krippendorff's alpha | ≥0.800 `[A]` |
| **Response rate trend, per instrument** | period over period | Falling response rates are the leading indicator of a programme customers have stopped believing in |
| **Unattributed mention share** | mentions with no account ÷ mentions | <10%; above that, dollar figures are a floor |

**The credibility test.** Take the accounts that churned this quarter and check what the register
said about them 90 days earlier. If their themes were in the register and unrouted, the programme
worked and the company did not act. If their themes were absent, the listening has a gap — and
the Silent ARR table usually says where.

---

## 10. Readout anti-patterns

| Anti-pattern | Correction |
| --- | --- |
| Opening with the NPS number | Open with who spoke, whose voice is missing, and the ARR each represents |
| A wall of verbatims | Three per theme, chosen for ARR and severity, read aloud with account and date |
| Themes with no owner proposed | Pre-draft the owner and the date; the room's job is to confirm or reassign, not to invent |
| Twenty themes presented | The capacity-gate number, and only that. The rest go in "Not Doing" |
| No "Not Doing" section | It is the section that lets CS answer customers honestly |
| Sentiment scores with no behaviour | Section 5, never cut for time |
| Last quarter's decisions unreported | Section 8 — a programme that does not track its own commitments teaches the room to ignore them |
| An analyst-invented cost-to-fix | `UNKNOWN — requires <function> estimate`, with the request dated |
| "Customers want better reporting" | Which accounts, how much ARR, which segment, which severity, which use case, and what breaks if it stays |
| Presenting the z-value as significance | It is a screen on dependent samples. Say so on the slide |
| A readout with no customer-facing follow-through | The outer-loop note, within 30 days, including the declines |
