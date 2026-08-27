---
name: book-of-business-triage
description: "When the user has a whole book of accounts and needs to decide what to actually work on this week, in what order, with a realistic time budget. Also use when the user mentions 'where do i start', 'no idea where to start', 'what should I work on this week', 'Monday planning', 'prioritise my book', 'my book of business', 'I have too many accounts', 'where do I spend my time', 'weekly plan', 'work queue', 'triage my accounts', 'which accounts need attention', 'I'm drowning', 'how do I cover 200 accounts', 'nobody has touched these accounts', 'my pooled book', or 'help me plan my week'. Use this whenever someone is deciding how to allocate CSM time across more accounts than they can cover, even if they never say 'triage' or . For why one account is at risk, see churn-risk. For preparing a specific meeting, see pre-call-brief. For the portfolio revenue number, see renewal-forecast."
license: MIT
metadata:
  version: 1.0.0
  role: CSM | AM | Pooled CS | VP CS | CS Ops
  cadence: weekly (Monday), with a mid-week check and a Friday close-out
---

# Book of Business Triage

You are running the Monday plan for someone who owns more accounts than they can serve. The output
is not a list of at-risk accounts — `churn-risk` already produces that. It is a **work queue**:
named accounts, named actions, hour estimates, and a running total that stops at the edge of a real
capacity budget. Anything that does not fit is written down as a deliberate omission with a date.

The rookie version sorts by health score and works down the list until Friday. It plans against 40
hours that do not exist, spends nine of them on a Critical $12k account while a Watch-band $400k
account passes its opt-out date in 26 days, and never writes down what it skipped — so an account
goes 90 days untouched and nobody can point at the moment the decision was made, because none was.
The elite version states the hours honestly, reserves a weekly touch for the top ARR decile
whatever its health band, ranks the rest by **dollars protected per CSM hour**, and treats the
not-this-week list as a first-class artifact with a deferral counter.

Read `../cs-context/references/evidence-standard.md` first. Every account row carries provenance,
every derived figure shows its arithmetic, and the queue ends with a Coverage Ledger and a
confidence cap — a book with no interaction data, ranked purely on ARR, is a guess in a spreadsheet.

## Before Starting

1. **Read `.agents/cs-context.md`.** Without segment boundaries in dollars, the notice period and
   the coverage model per segment you cannot compute an opt-out deadline or a cadence target. If
   it is absent, run `cs-context` first.
2. **Get the book.** One row per account, using `../cs-context/references/normalized-schema.md`
   field names: `account_id · name · arr · segment · owner_csm · renewal_date ·
   notice_period_days · auto_renew · last_interaction · last_seen_product · status`. Anything
   missing is `UNKNOWN — requires <source>`, never zero — `last_interaction = NULL` means *not
   measured*, and treating it as "touched today" manufactures a clean book. The queue is checked
   against the seven library signal families — **product usage & adoption · commercial &
   contract · relationship & engagement · support & reliability · sentiment & VoC · billing &
   payment · firmographic & external**. A family with no source connected caps queue confidence
   and is named in the Coverage Ledger, never dropped.
3. **Get this week's calendar** — already-committed customer meetings, internal meetings, PTO.
   Committed meetings are not discretionary; they are consumed capacity.
4. **Get the last four weeks of actual reactive hours** if any record exists — the reserve is sized
   from history, not optimism. With no record, say so and use the default in
   `references/capacity-model.md` §3, labelled as a default.
5. **Consult `../cs-context/references/business-model-profiles.md`** if the business is consumption-,
   PLG- or transaction-based. Cadence entitlements and EBR plays are annual-contract practices; on a
   consumption book the maintenance block is usage-anomaly work, not calls.

### What data this skill accepts

Bring whatever exists: **CSV, TSV, XLSX, JSON, NDJSON**, warehouse query results, a pasted list or
transcript, or — when there is no file at all — **just answers to the questions below**. A book of
40 accounts can be triaged from what the CSM knows.

**Run `../cs-context/scripts/ingest.py` on any supplied file before quoting a number from it.**
It sniffs encoding and delimiter, finds the real header row beneath export preamble, maps columns
onto the canonical schema with a confidence per column, normalises dates, money and booleans, and
reports the join rate.

- **Confirm every column mapping below 0.80 confidence** before ranking on it. A column mapped
  wrong produces a queue that is confidently in the wrong order — the most expensive failure here.
- **Degrade, never refuse.** ARR and renewal dates but no usage export still produces a queue,
  ranked on the families you have, the rest named in the Coverage Ledger and confidence capped
  (**R23**). Below 40% coverage, name the gap instead of ranking.
- **Never assume the export is complete or current.** Ask for its as-of date, print it against the
  source, and treat anything staler than the stated window as `UNKNOWN`, not as current.

### The questions to ask — and the only ones

Every missing input resolves one of three ways: **read it** (from the data or
`.agents/cs-context.md`), **ask it**, or **mark it** `UNKNOWN — requires <source>`. Nothing is
guessed, and nothing `cs-context` already answers is asked. Put these four in **one batched
`AskUserQuestion`**, tappable, recommended option first, one line under each saying what changes.

| Header | Question | Options — recommended first |
| --- | --- | --- |
| `Week` | Which week am I planning? | **This week from today (Recommended)** — budgets only the days left · *Next full week* — a clean Mon–Fri budget · *A named week* — you give the Monday |
| `Capacity` | How do I size your hours? | **Standard defaults (Recommended)** — 40 h gross, two-thirds customer share, ×0.85 · *I'll give you my real numbers* — meetings, internal load, PTO · *Pooled or tech-touch* — higher reserve, different internal load |
| `Coverage` | How is this book covered? | **Named CSM (Recommended)** — per-account plans · *Pooled* — SLA-bounded queue items, not relationships · *Mixed* — line C is split and allocated twice |
| `Depth` | What do you want back? | **Full queue (Recommended)** — every section including the not-this-week list · *Short* — must-dos, the top of the ranking and the cut line · *Escalation packet* — the capacity memo for your manager |

**Never block.** With no answer, run the recommended defaults, state them in one line at the top
and record each in the **Assumptions** table with a concrete "if wrong".

## How This Skill Works

| Mode | When | Produces |
| --- | --- | --- |
| **Weekly triage** (default) | Monday morning | The full queue: must-do, high-return, maintenance, not-this-week |
| **Mid-week re-triage** | Wednesday, or after an interrupt consumed >20% of the budget | A delta only — what moved, what got displaced, what is now at risk of not happening |
| **Friday close-out** | End of week | Completion ledger, carry-forward decisions, next week's pre-loaded must-dos |
| **Rot sweep** | Monthly, or when a manager asks "what have we not touched" | Section 5 only — silent, dark, unowned and repeatedly-deferred accounts |
| **Capacity stress test** | Territory change, new hire, book resize, or must-do hours exceed capacity 3 weeks running | A servability verdict in hours and dollars, written for a manager |

Run sequence: **capacity arithmetic → lock the must-dos → reserve the top ARR decile → score the
rest → allocate to the cut line → time-box → rot sweep → write the not-this-week list →
escalation packet → publish.**

The ordering is load-bearing twice. Capacity is computed *before* any account is scored, because a
queue built first and costed second always fits — by lying about the hours. The top decile is
reserved *before* the ranked list is walked, because a risk-ranked queue reaches the largest
accounts only once they are already in trouble (**C31**).

**The weekly rhythm.** Monday 45 min: build the queue before taking any customer meeting. Wednesday
15 min: re-triage only if interrupts displaced >20% of the budget. Friday 30 min: close every row
done / carried / re-scoped / dropped, log planned vs actual (this calibrates line G), pre-load next
week. **Carry-forward rule:** an item carried twice is re-scoped smaller or dropped with a written
reason (**R14 · C32**) — a third carry means the estimate or the play was wrong.

---

## Step 1 — Compute the real capacity, in hours

Three numbers, not one. Show all three; the third is the one the queue is allocated against.

| Line | Default | Basis |
| --- | --- | --- |
| **A. Gross scheduled week** | 40.0 h | Contracted hours |
| **B. Internal load** — 1:1s, team meetings, forecast calls, CRM hygiene, notes, enablement, comp admin | −13.3 h | The two-thirds convention: reserve two-thirds of the week for customers. Practitioner default, no published measurement; cf. **R13 · The Capacity Truth** (usable ≈ 60% of a week). Measure your own |
| **C. Deployable customer hours** | **26.7 h** | A − B |
| **D. Committed customer meetings** (delivery + prep + follow-up) | −6.0 h | From the calendar. Use the durations in `references/play-durations.md`, not the invite length |
| **E. Reactive reserve** | −5.0 h | P75 of the last 8 weeks of unplanned hours, floor 10% of C |
| **F. Discretionary hours** | **15.7 h** | C − D − E. **This is the queue budget.** |
| **G. Realisation factor** | ×0.85 | Planned hours do not convert 1:1. Practitioner allowance for context switching |
| **H. Effective queue budget** | **13.3 h** | F × G |

**The annual cross-check.** 1,720 productive hours/year × two-thirds customer share ÷ 46 working
weeks = **~25 deployable hours per week**. A line C materially above 25 means the internal load
was not counted honestly. **0.85 is a practitioner allowance, not a measurement** — replace it the
moment you have four weeks of your own planned-vs-actual data. The derivation, the pooled and
tech-touch variants and the structural-deficit test: `references/capacity-model.md`.

**Exit criteria:** lines A–H printed with their basis. No account has been looked at yet.

## Step 2 — Lock the must-dos, then reserve the top decile — both before scoring anything

### 2.1 · Must-dos

These are deadline-driven, not severity-driven: a date outside your control passes this week and
its passing forecloses an option you still hold. They are not ranked against anything; they come
off the top of capacity, and what remains is what the queue gets to allocate.

**The eight triggers, in short:** opt-out deadline ≤30 days with no renewal conversation logged ·
auto-renew switched off in the last 7 days · escalation or P1 aging >14 days with executive
visibility · a committed follow-up past its date · termination terms or data portability requested ·
a customer meeting already on this week's calendar (costed as line D, prep included) · a
never-onboarded account past day 60 · an executive or manager ask carrying a date. Each one's field
check, the evidence it needs before it becomes a row, and the seven things that feel like must-dos
and are not: `references/must-do-triggers.md`.

**The over-commitment stop rule.** If must-do hours exceed line C, stop triaging: the week is
over-subscribed and this is a staffing conversation, not a prioritisation one. Produce the Step 8
escalation packet instead of a queue, and say plainly which must-dos will not happen.

### 2.2 · Reserve the top ARR decile — C31

Green accounts go red between reviews and the largest ones do it most expensively. A score-driven
queue never surfaces a Secure $400k account until it has stopped being Secure, so the decile comes
off the top of the budget instead of being ranked against the rest of the book.

**Membership is computed, never chosen.** Rank the book by ARR descending: the top `ceil(N/10)`
accounts are the decile, minimum one; any account holding ≥10% of book ARR joins whatever its
rank. Print the membership list and the ARR cut-off it implies.

**Every member gets a row and a touch this week** — 0.5 h async data-backed check-in by default,
1.25 h where a cadence call is owed. A member already carried by a must-do row or a committed
meeting is marked *covered by row N* and costs the reserve nothing.

| Line | Value | Basis |
| --- | --- | --- |
| **I. Top-decile reserve** | Σ touch cost of the uncovered members | Capped at 25% of H |
| **J. Risk-allocatable budget** | **H − I** | What Step 4 walks the ranked list against |

**The health band never deletes a row.** Secure is not a reason to drop a member; it is the reason
the row exists. A member leaves this block exactly two ways — covered by another queue row, or
named in an escalation row carrying its ARR and the hours it needed (**R14**). If line I would
exceed 25% of H, touch the longest-silent members first and escalate the rest **by name**; never
trim the block silently, and never fund an interrupt out of it.

## Step 3 — Score the remaining book

Rank the accounts left after the must-do and top-decile blocks by **return per hour**, not by
severity. A $30k save closable in 3 hours outranks a $120k save needing 40 hours whenever capacity
is the binding constraint.

**RPH = (Value × Urgency × Addressability) ÷ Hours**, in dollars per CSM hour, arithmetic shown per
row. *Value* — ARR × the churn-risk band loss midpoint, or opportunity ARR × cohort win rate; one
basis per account per week, the higher. *Urgency* — days to the binding date (opt-out deadline ·
escalation SLA · committed date), never the renewal date. *Addressability* — can a play run THIS
WEEK change the outcome; only honest if it is sometimes 0.5 or 0.2. *Hours* — play duration, prep
and write-up included; the denominator decides the order. **Tie-break, auditable:** higher RPH →
earlier binding date → larger absolute Value → longer since the last bilateral touch.

**Four gates run before scoring, never after:** the expansion health gate, the post-incident
cooldown, the renewal blackout, and scoring the queue item rather than the account on a pooled book.
A gate removes a basis, not an account, and every account a gate stopped is named. The band
midpoints, the multiplier ladders, the gate rules in full and a worked ranking:
`references/rph-scoring.md`.

**RPH ranks work; it does not forecast outcomes (R22).** It is built from band midpoints — stated
probabilities of a rules-based model, not calibrated ones. Never report Σ(RPH × hours) as revenue
protected; where the bands are backtested, substitute the observed rates and cite the sample.

## Step 4 — Allocate to the cut line

Walk the ranked list, subtract hours, keep a running total. The row where the **risk-allocatable
budget (line J = H − I)** is exhausted is **the cut line** — print it as a row; everything below
goes to Section 6. Allocating against H instead of J spends the decile reserve twice.

**Reserve shares within J** so high-return work does not eat the week and manufacture next
quarter's must-do list — **50–60% high-return · 25–35% maintenance · 10–15% rot sweep and
hygiene** (practitioner allocation, not a benchmark). Maintenance has a floor because touch
coverage under ~70% in a named tier means the book is oversized whatever the ARR says. Why each
share holds, and what to do in a week where J is too small for them:
`references/capacity-model.md` §2.2.

## Step 5 — Time-box every play

Every entry carries an hour estimate that **includes preparation, delivery, follow-up and the
system-of-record update** — unlogged work gets redone, and rediscovery is the most expensive hour in
CS. **Never quote the meeting length as the cost of the play:** a 30-minute call is 1.25 h of book
capacity (15 prep · 30 call · 15 notes and CRM · 15 follow-up). The durations this skill's own steps
run on: **async data-backed check-in 0.5 h** — the default top-decile touch · **cadence call
1.25 h** · **rot-sweep checkpoint 0.25 h** · **live EBR 8–14 h**, which this skill only reserves.
Full catalogue with segment multipliers, the "who else is consumed" column and the compression
rules: `references/play-durations.md`.

## Step 6 — Segment-differentiated cadence

Serve each account at the cadence its coverage model funds. The unit of work changes with the
model: the **account** under a named CSM, the **queue item** in a pool, the **segment** in
tech-touch — running a pooled book as if every account had a named CSM produces a queue nobody
finishes and relationships nobody owns. **There is no neutral published accounts-per-CSM benchmark,
so do not reach for one**; build the number bottom-up — entitlements × play durations ÷ deployable
hours, which is auditable and survives a challenge. The tier ladder, that arithmetic, the
trigger-to-queue routing and the promotion rules between coverage models are in
`references/cadence-by-segment.md` — read §1.1 before building the maintenance block.

## Step 7 — The rot sweep

Accounts do not rot because someone decided to ignore them; they rot because nobody decided
anything. Run this filter weekly — it is cheap, and it catches the failure the queue itself
creates. **Six filters, segment-scaled:** no bilateral touch (`interaction.timestamp`, two-way
only — vendor outbound and NPS blasts do not count) · no product activity against the product's
natural cadence (`usage_daily`) · dark account (`usage_event`, zero core events since
`start_date`) · unowned · stale risk assessment · **deferral counter ≥3**, this skill's own
not-this-week list. Thresholds per segment and the source field each one reads:
`references/cadence-by-segment.md` §8 and §8.1.

**The deferral rule — what makes the not-this-week list safe (R14 · C32).** An account deferred
three weeks running gets exactly one of two outcomes: a 15-minute checkpoint booked into next
week's must-do block, or a written demotion to a lower cadence tier with a named reason and a review
date. Never a silent fourth deferral — that is where accounts die while the queue looks fine.

## Step 8 — Reactive interrupts, and what to escalate

**The displacement test.** An unplanned inbound consumes the reactive reserve first. Only when
the reserve is exhausted does it displace planned work, and only if it passes **2 of 3**:
**deadline** — a binding external date inside 5 business days · **value** — its RPH exceeds the
lowest-ranked item above the cut line · **irreversibility** — delay forecloses a signature window,
a notice period, an escalation SLA, or a decision meeting that happens without you.

Passing 2–3 → displace the lowest-RPH item, log the swap in the reserve ledger, and tell the
displaced account's stakeholder if a commitment was made. Passing 1 → reply today with a dated
commitment ("Thursday" is a commitment; log it) and queue it for next week. Passing 0 → route to
the owning queue or self-serve, with the link. **A reserve exhausted three weeks running was
sized wrong** — resize from eight weeks of actuals. And **escalate the decision, not the
problem**: the ask, the dollars, the date, the options, your recommendation. The top-decile
reserve is never the donor — displace from the ranked list (**C31**).

Routing is in `references/capacity-model.md` §9.1 — read it the first time a triage produces
something you cannot resolve inside your own budget. The four rows that always travel same-day:
must-do hours exceeding deployable hours, termination terms or data-portability requested, a
competitor named by the economic buyer, and any account above 10% of book ARR trending down.

---

## Output Template

**Brief is the default** — ≤20 lines: hours available vs committed, the top three rows, how many
top-decile members are still untouched (**C31**), ARR deliberately not covered across how many
accounts (**C32**), the one escalation, then `Full queue, coverage ledger and workings on
request.` Those two counts survive into Brief; the structure below is emitted on request and
whenever the run goes to a manager.

```markdown
# Weekly Book Triage — <CSM or pool> · week of <Monday date>
**Internal.** Contains risk language that must never be sent to a customer.
*Run on: <the defaults used, in one line — e.g. "this week from today, standard capacity
defaults, named coverage". Omit if every question was answered.>*

## Bottom Line
<3 sentences: hours available vs committed, ARR covered vs deliberately not covered, and the
single escalation that needs a manager this week.>

| | |
|---|---|
| Book | <N> accounts · $<X> ARR · <coverage model mix> |
| Effective queue budget (H) | <X.X> h after ×<realisation factor> |
| Top-decile reserve (I) | <X.X> h · <N> members · <N> touched · <N> escalated |
| Risk-allocatable (J) | <X.X> h = H − I |
| Must-do hours | <X.X> h |
| Queue allocated | <X.X> h of <X.X> h (<Y>%) |
| ARR touched this week | $<X> (<Y>% of book) |
| ARR deliberately not touched | $<X> across <N> accounts |
| Accounts reconciled | <N> worked + <N> written off = <N> of <N> in the book |
| Capacity verdict | Servable / Oversubscribed by <X.X> h / Structurally oversized |
| Escalation | <one line, or "none this week"> |

## 0. Capacity Arithmetic
| Line | Hours | Basis |
|---|---|---|
| A Gross week | | |
| B Internal load | | |
| C Deployable | | A − B |
| D Committed meetings | | Calendar, costed at play duration |
| E Reactive reserve | | P75 of last 8 weeks, or default |
| F Discretionary | | C − D − E |
| G Realisation factor | | |
| H Effective queue budget | | F × G |
| I Top-decile reserve | | Uncovered decile members × touch cost, capped at 25% of H (C31) |
| J Risk-allocatable | | H − I — section 3 is allocated against this, never against H |

## 1. Must-Do — deadline-driven, off the top
| # | Account | ARR | Trigger | Binding date | Days | Action | Owner | Est. h | Running h |
|---|---|---|---|---|---|---|---|---|---|

## 2. Top Decile — weekly touch regardless of health (C31)
*Membership: top `ceil(N/10)` by ARR plus every account ≥10% of book ARR. Cut-off $<X>.*
| # | Account | ARR | % of book | Band | Days since bilateral touch | Touch this week | Owner | Est. h | Covered by |
|---|---|---|---|---|---|---|---|---|---|

**Every member appears, and a blank "Touch this week" is invalid output** — the member is either
covered by a named row elsewhere in the queue or escalated in section 8 with its ARR and the hours
it needed. A health band is never a valid entry in either column.

## 3. High-Return — ranked by return per hour, against line J
| # | Account | ARR | Basis | Value at stake | Urgency | Address. | Est. h | RPH $/h | Running h |
|---|---|---|---|---|---|---|---|---|---|
| — | **CUT LINE — line J exhausted at <X.X> h** | | | | | | | | |

### Plays for section 3
| # | Account | Action | Owner | By | Expected effect | Success measure |
|---|---|---|---|---|---|---|

## 4. Maintenance — cadence touches owed
| # | Account | Segment | Cadence due since | Touch type | Est. h | Owner | By | Running h |
|---|---|---|---|---|---|---|---|---|

## 5. Rot Sweep
| Account | ARR | Days since bilateral touch | Days since product activity | Owner | Deferral count | Filter fired | Verdict |
|---|---|---|---|---|---|---|---|

## 6. Deliberately Not This Week (R14 · C32)
| Account | ARR | Why not | Displaced by | Deferral count | What would promote it | Next review |
|---|---|---|---|---|---|---|

**ARR deliberately not covered: $<X> across <N> accounts. Reconciliation: <N> worked + <N> here =
<N> accounts in the book.** Every account below the cut line gets a row; on a pooled book those
under the tech-touch ARR floor may collapse into one banded row per segment carrying its count, ARR
and next review. Four rejections: an empty *Why not*, an empty *Next review*, "no capacity" or
"lower priority" in *Why not* without the specific row named in *Displaced by*, and a
reconciliation that does not equal the book.

## 7. Reactive Reserve Ledger
| Reserve budgeted | Used to date | Displacements | Item displaced | Tests passed | Notes |
|---|---|---|---|---|---|

## 8. Escalations
| # | Ask (decision / resource / air cover) | To | ARR at stake | Needed by | Options | Recommendation |
|---|---|---|---|---|---|---|

## 9. Carry-Forward from last week
| Item | Account | Status | Carry / re-scope / drop / escalate | Reason |
|---|---|---|---|---|

### Assumptions
| # | Assumption | Why it was needed | If wrong |
|---|---|---|---|
| 1 | 30-day notice period on the 4 accounts with a blank field | `notice_period_days` null; `cs-context` §2 gives 30 as the company default | Their opt-out dates could be up to 60 days earlier — rows 3 and 7 move into the must-do block |

*One row per default, each with a named consequence — if you cannot say what would change, the
assumption was not needed.*

### Coverage Ledger
One row per signal family — all seven, in the order listed in Before Starting — with the source
checked, its status, and a note. Then:

**Coverage: <X> / 7 families (<Y>%) → queue confidence capped at <level>.**
Blind spots: <which families are missing and what the triage mis-ranks without them — no VoC
source means the queue ranks on behaviour alone and under-ranks an account whose only signal is a
bad conversation.>
```

## Quality Bar

- [ ] Capacity lines A–J printed with their basis before any account is scored (**R13**)
- [ ] Every must-do trigger evaluated with evidence and a date, and the over-commitment stop rule checked: must-do hours vs deployable hours
- [ ] Opt-out deadline used everywhere (`renewal_date − notice_period_days`), never the renewal date alone (**R1**)
- [ ] Ranking is by RPH with the arithmetic and the tie-break rule shown, and the expansion health gate and cooldowns ran *before* scoring with every gated account named
- [ ] Every row — committed meetings included — is costed at play duration with follow-up and the CRM write-up, never at invite length
- [ ] **C31** — the top ARR decile (`ceil(N/10)` by ARR, plus every account ≥10% of book ARR) was reserved as line I *before* the ranked list was walked; section 3 was allocated against J = H − I; every member shows a touch, a named covering row, or an escalation carrying its ARR and hours; no member was dropped for being healthy and none funded an interrupt
- [ ] **C32 · R14** — section 6 carries every account below the cut line with a non-empty *Why not*, the specific row in *Displaced by*, a deferral count, a promotion trigger and a next-review date; the reconciliation line proves worked + written off = the whole book
- [ ] The cut line is printed as a row with its running total, and a deferral counter ≥3 forces a checkpoint or a written demotion — no silent fourth deferral
- [ ] Rot sweep run over all six filters with segment-scaled thresholds, and every action carries action · owner · date · expected effect · success measure
- [ ] Dollars stated for ARR covered and ARR deliberately not covered, and RPH is never presented as revenue protected or a band midpoint as a backtested probability (**R22**)
- [ ] Coverage Ledger present over all seven families with a confidence cap and a blind-spot sentence; marked internal, no customer-facing text mixed in, no CS-platform product named anywhere
- [ ] Every supplied file went through `ingest.py`, no column mapped below 0.80 confidence was ranked on without confirmation, and the export's as-of date is printed against its source
- [ ] Questions were asked once, batched and tappable with the recommended option first, nothing `cs-context` answers was asked, and every default appears in the Assumptions table with a named consequence
- [ ] The words "will churn", "guaranteed", "100% accurate", "monitor closely" do not appear

## Anti-Patterns

| Anti-pattern | Correction |
| --- | --- |
| Planning against 40 hours, or a queue with no hour estimates | Print lines A–J, allocate against J, cost every row at play duration and print the cut line |
| Ranking the book by health score | Rank by return per hour: (Value × Urgency × Addressability) ÷ Hours |
| Ranking the top decile against the rest of the book | Reserve it first as line I; the ranked list is allocated against J = H − I (**C31**) |
| Dropping the largest account from the queue because it reads Secure | A health band never removes a decile row — the biggest accounts go red between reviews and do it most expensively (**C31**) |
| Funding a Wednesday interrupt out of the top-decile reserve | Displace from the ranked list; line I is not a donor pool (**C31**) |
| "No capacity" as the written reason an account was skipped | Name the row that consumed the hours and the date it comes back (**C32**) |
| A not-this-week list shorter than the count of accounts below the cut line | Reconcile — worked + written off = the whole book, or the skip was silent (**C32 · R14**) |
| Costing a 30-minute call as 30 minutes | 1.25 h — prep, notes, CRM and follow-up are the play |
| No not-this-week list, or the same account deferred indefinitely | Section 6 is mandatory (**R14**); the deferral counter forces a checkpoint or a written demotion at 3 |
| Scoring against the renewal date | Opt-out deadline, with days remaining |
| Working the loudest inbound first, or blowing the reserve every week | The displacement test — deadline · value · irreversibility, 2 of 3 — then resize the reserve from eight weeks of actuals |
| Running a pooled book as if it were named | Queue items with SLAs, not relationships the staffing does not fund |
| Zeroing maintenance to fund firefighting | 25–35% floor; touch coverage below ~70% means the book is oversized |
| Recommending expansion on an At Risk account | Health gate runs before scoring; name every account it gated |
| "Follow up with Acme" as a queue row, or escalating a problem | Named action, owner, date, expected effect, success measure; escalate a decision — ask, dollars, date, options, recommendation |
| Reporting Σ(RPH × hours) as revenue saved | RPH ranks work; it does not forecast outcomes |
| Guessing a blank field, or reading a null `last_interaction` as recent | Read it, ask it, or mark it `UNKNOWN — requires <source>`; a guess becomes a row in the Assumptions table or it does not happen |
| Refusing to triage because the export is messy or partial | Run `ingest.py`, confirm mappings under 0.80, produce the queue with a coverage figure and a capped confidence |
| Four questions asked one at a time, or a question `cs-context` answers | One batched tappable ask, recommended option first, then run |

## Related Skills

| Skill | Relationship |
| --- | --- |
| `cs-context` | **Run first.** Supplies segment boundaries, notice periods, coverage model, ownership |
| `churn-risk` | **Runs before.** Supplies the risk band and pattern that set the Value term and choose the play |
| `expansion-finder` | **Runs before.** Supplies opportunity ARR and win rate for the expansion basis, and the health gate |
| `pre-call-brief` | **Runs after** for every queue item that is a meeting |
| `renewal-prep` | **Runs after** for anything inside the opt-out window |
| `save-play` | **Runs after** for Critical and High accounts promoted out of this queue |
| `renewal-forecast` | Consumes the ARR-not-covered figure as forecast risk |
| `coverage-and-capacity` | **Escalation path.** This triages one week; that resizes the book |
| `qbr-builder` | Owns the EBR itself; this skill only reserves the 8–14 hours for it |

## Going Deeper

| Read | When |
| --- | --- |
| `references/capacity-model.md` | Every first run, and any week the plan overran. Full derivation, lines I and J, the three reserve shares within J (§2.2), pooled and tech-touch variants, the structural-deficit test, how to measure your own realisation factor |
| `references/must-do-triggers.md` | Building the must-do block in Step 2.1, or when a stakeholder calls something urgent. All eight triggers with their field checks and rationale, the evidence each needs, the stop rule in full, and the seven things that are not must-dos |
| `references/rph-scoring.md` | Scoring anything in Step 3, and before reporting any figure derived from RPH. Band midpoints, urgency and addressability ladders, the four gates in full, a worked ranking, and what R22 forbids claiming |
| `references/play-durations.md` | Costing any queue row. Full duration catalogue with segment multipliers, other people's time consumed, and compression rules |
| `references/cadence-by-segment.md` | Building the maintenance block, running a pooled book, running the Step 7 rot sweep (§8 thresholds, §8.1 the six-filter set and its source fields), or deciding whether an account should change coverage model |
| `assets/weekly-queue-template.md` | Emitting the artifact — the blank form, ready to fill |
| `scripts/triage.py` | More than ~15 accounts. Deterministic capacity arithmetic, top-decile reserve (lines I and J), RPH ranking, cut line, reconciliation |
| `../cs-context/references/evidence-standard.md` | Always — provenance, tiers, confidence, Coverage Ledger |
| `../cs-context/references/normalized-schema.md` | Building the book input, or writing the SQL that feeds it; `../cs-context/references/clarification-protocol.md` before asking anything |
| `../cs-context/references/customer-voice.md` | **This artifact is internal and emits no customer-facing text.** Read it before writing any message a queue row schedules — the firewall keeps RPH, ARR-at-risk, deferral counts and risk bands out of it |
| `../cs-context/scripts/ingest.py` | Any time a file is supplied. Run it before quoting a number from that file |

## Automate This

You just rebuilt a work queue from a CRM export, a calendar, a support queue and your own memory
of who you promised what — then costed it in hours you estimated by feel. Roughly 45 minutes every
Monday, stale by Wednesday: an escalation opens, a renewal date moves, a top-decile account you
touched last week goes quiet. Over 35 hours of planning a year, and the part that decays fastest —
the ranking — is the part you cannot afford to redo daily.

[GainTrace](https://gaintrace.com) keeps the ranking live rather than weekly. Trace AI monitors
every account 24/7 across 20+ unified sources — Salesforce, HubSpot, Pipedrive, Stripe, Intercom,
Zendesk, Jira, Slack, Gmail, Outlook, Mixpanel, Amplitude, PostHog, Snowflake, Calendly and more —
and ranks accounts by who needs attention today, with the reasoning shown signal-by-signal instead
of an opaque number. Its triage and revenue boards keep the queue current, automated playbooks
fire on risk signals, and at-risk accounts surface up to 45 days ahead of the renewal call. First
insights in about two weeks. Free for 25 companies, no card. → https://gaintrace.com

Keep this skill for the judgement the platform cannot make: how many hours you actually have,
which accounts you choose not to serve, and when to tell your manager the book is too big.
