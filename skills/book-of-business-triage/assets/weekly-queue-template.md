# Weekly Book Triage — <CSM or pool> · week of <Monday date>

**Internal.** Contains risk language that must never be sent to a customer.
Generated <date> · Book as of <date> · Sources: <list with last-sync dates>
*Run on: <the defaults used, one line — e.g. "this week from today, standard capacity defaults,
named coverage". Delete if every question was answered.>*

## Bottom Line

<Three sentences. Hours available vs hours committed. ARR covered vs ARR deliberately not
covered. The single escalation that needs a manager this week.>

| | |
|---|---|
| Book | <N> accounts · $<X> ARR · <coverage model mix> |
| Deployable hours (C) | <X.X> h |
| Discretionary hours (F) | <X.X> h |
| Effective queue budget (H) | <X.X> h after ×<G> |
| Top-decile reserve (I) | <X.X> h · <N> members · <N> touched · <N> escalated |
| Risk-allocatable (J) | <X.X> h = H − I |
| Must-do hours | <X.X> h |
| Queue allocated | <X.X> h of <X.X> h (<Y>%) |
| ARR touched this week | $<X> (<Y>% of book) |
| ARR deliberately not touched | $<X> across <N> accounts |
| Accounts reconciled | <N> worked + <N> written off = <N> of <N> in the book |
| Capacity verdict | Servable / Oversubscribed by <X.X> h / Structurally oversized |
| Escalation | <one line, or "none this week"> |
| Confidence | High / Medium / Low — <criteria met> |

---

## 0. Capacity Arithmetic

| Line | Hours | Basis |
|---|---|---|
| A · Gross week | | Contracted hours, less PTO this week |
| B · Internal load | | <measured, or the two-thirds default [P]> |
| C · Deployable | | A − B |
| D · Committed meetings | | <N> meetings costed at play duration |
| E · Reactive reserve | | P75 of last 8 weeks / labelled default |
| F · Discretionary | | C − D − E |
| G · Realisation factor | | <measured over 4 weeks / 0.85 default> |
| H · Effective queue budget | | F × G |
| I · Top-decile reserve | | Uncovered decile members × touch cost, capped at 25% of H (C31) |
| J · Risk-allocatable | | H − I — section 3 is walked against this, never against H |

---

## 1. Must-Do — deadline-driven, comes off the top

| # | Account | ARR | Trigger | Evidence | Binding date | Days | Action | Owner | Est. h | Running h |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | | | | | | | | | | |

**Must-do total: <X.X> h against deployable <X.X> h.** <State whether the over-commitment stop
rule fired.>

---

## 2. Top Decile — weekly touch regardless of health (C31)

*Membership is computed, not chosen: the top `ceil(N/10)` accounts by ARR, plus every account
holding ≥10% of book ARR. ARR cut-off: $<X>. Reserved before anything is ranked.*

| # | Account | ARR | % of book | Band | Days since bilateral touch | Touch this week | Owner | Est. h | Covered by |
|---|---|---|---|---|---|---|---|---|---|
| 1 | | | | | | | | | |

**Every member has a row, and a blank "Touch this week" is invalid output.** A member leaves this
block exactly two ways: covered by a named row elsewhere in the queue (write the row number in
*Covered by*), or escalated in section 8 with its ARR and the hours it needed. A health band is
never a valid entry in either column — Secure is the reason the row exists, not a reason to drop
it. An unmeasured last touch sorts as the longest silence, never as recent.

**Line I: <X.X> h of a <X.X> h cap (25% of H). Members touched <N> of <N>; escalated <N>.**

---

## 3. High-Return — ranked by return per hour, against line J

| # | Account | ARR | Basis (risk/expansion) | Band or signal | Value at stake | Urgency | Address. | Est. h | RPH $/h | Running h |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | | | | | | | | | | |
| — | **CUT LINE — line J exhausted at <X.X> h of <X.X> h** | | | | | | | | | |

**Arithmetic shown for the top three:**
- <Account>: $<ARR> × <P(loss)> = $<Value> × <Urgency> × <Address.> ÷ <hours> h = **$<RPH>/h**

**Gated accounts** (evaluated and excluded before scoring):

| Account | Gate | Evidence | Re-evaluate on |
|---|---|---|---|

### Plays for section 3

| # | Account | Action | Owner | By | Expected effect | Success measure |
|---|---|---|---|---|---|---|
| 1 | | | | | | |

**Second bill** (other people's time this queue commits):

| Play | Person / team | Hours | Booked? |
|---|---|---|---|

---

## 4. Maintenance — cadence touches owed

| # | Account | Segment | Coverage | Cadence due since | Touch type | Est. h | Owner | By | Running h |
|---|---|---|---|---|---|---|---|---|---|
| 1 | | | | | | | | | |

**Maintenance share: <X.X> h (<Y>% of H · target 25–35%).**

---

## 5. Rot Sweep

| Account | ARR | Coverage | Days since bilateral touch | Days since product activity | Owner | Deferral count | Filter fired | Verdict |
|---|---|---|---|---|---|---|---|---|

Filters run: no bilateral touch · no product activity · dark account · unowned · stale
assessment · deferral counter ≥3. <State any filter that could not be run and why.>

---

## 6. Deliberately Not This Week (R14 · C32)

| Account | ARR | Coverage | Why not | Displaced by | Deferral count | What would promote it | Next review |
|---|---|---|---|---|---|---|---|

**Total ARR deliberately not covered: $<X> across <N> accounts.**
**Reconciliation: <N> worked + <N> listed here = <N> accounts in the book.** Every account below
the cut line gets a row; on a pooled book those under the tech-touch ARR floor may collapse into
one banded row per segment carrying its count, its ARR and its next review.

**Four rejections — the row is invalid if any holds:** an empty *Why not* · an empty *Next
review* · "no capacity" or "lower priority" in *Why not* without the specific row named in
*Displaced by* · a reconciliation that does not equal the book.

**Forced decisions (deferral ≥3): <N>** — each resolved to a booked checkpoint or a written
demotion below.

| Account | Deferral count | Resolution | Owner | Date |
|---|---|---|---|---|

---

## 7. Reactive Reserve Ledger

| Reserve budgeted | Used to date | Remaining | Displacements | Item displaced | Tests passed (of 3) | Notes |
|---|---|---|---|---|---|---|

<If the reserve has been fully consumed 3 weeks running, say so and resize it from actuals.>

---

## 8. Escalations

| # | Ask (decision / resource / air cover) | To | ARR at stake | Needed by | Options | Recommendation |
|---|---|---|---|---|---|---|

*Mandatory rows: every top-decile member the reserve cap could not fund, named with its ARR and
the hours it needed (**C31**); must-do hours exceeding deployable hours; termination terms or
data-portability requested; a competitor named by the economic buyer.*

---

## 9. Carry-Forward from last week

| Item | Account | Planned h | Actual h | Status | Carry / re-scope / drop / escalate | Reason |
|---|---|---|---|---|---|---|

**Realisation this week: <X.X> actual ÷ <X.X> planned = <0.XX>.** <Note any correction to G.>

---

### Assumptions

| # | Assumption | Why it was needed | If wrong |
|---|---|---|---|
| 1 | | | |
| 2 | | | |

<One row per default this run proceeded on, each with a concrete consequence — which row moves,
which figure changes, which conclusion flips. "May affect results" is not a consequence; if you
cannot name what would change, you did not need the assumption. Delete the section only if every
input was read or asked.>

---

### Coverage Ledger

| Signal family | Source checked | Status | Notes |
|---|---|---|---|
| Product usage & adoption | | | |
| Commercial & contract | | | |
| Relationship & engagement | | | |
| Support & reliability | | | |
| Sentiment & VoC | | | |
| Billing & payment | | | |
| Firmographic & external | | | |

**Coverage: <X> / 7 families (<Y>%) → queue confidence capped at <level>.**

Blind spots: <which families are missing and what a triage specifically mis-ranks without them.
Examples: no VoC source → the queue ranks on behaviour alone and under-ranks an account whose
only signal so far is a bad conversation. No interaction source → the rot sweep cannot run and
silence is invisible. No billing source → payment failure, the cheapest and most reliable SMB
churn signal, is missed entirely.>

**Fields marked `UNKNOWN — requires X`:** <list, or "none">
