# Detection Lag

> The one output of a loss review that changes the risk model. Everything else in a post-mortem
> explains the past; this measures how much warning the organisation actually had and where the
> warning was lost. Teams consistently guess this wrong in the same direction — they assume the
> signal appeared weeks before the decision, and it is usually months, sitting in a system they
> already paid for.

**Contents**
- [1. The four lags](#1-the-four-lags)
- [2. The method](#2-the-method)
- [3. What counts as detectable](#3-what-counts-as-detectable)
- [4. The six failure modes](#4-the-six-failure-modes)
- [5. The health-score report card](#5-the-health-score-report-card)
- [6. Aggregate outputs](#6-aggregate-outputs)
- [7. Turning lag into thresholds](#7-turning-lag-into-thresholds)
- [8. The backtest protocol](#8-the-backtest-protocol)
- [9. A worked calculation](#9-a-worked-calculation)
- [10. Traps](#10-traps)

---

## 1. The four lags

Four dates, four intervals, one identity that must hold. If it does not, one of the dates is wrong.

```
earliest_detectable_date ──► first_flagged_date ──► first_intervention_date ──► decision_date

detection_lag_days   = decision_date − earliest_detectable_date       what we could have had
recognition_lag_days = first_flagged_date − earliest_detectable_date  lost to detection
realised_lead_time   = decision_date − first_flagged_date             what we actually had
action_lag_days      = first_intervention_date − first_flagged_date   lost to routing and capacity

detection_lag = recognition_lag + realised_lead_time
```

| Interval | What a big number means | Who owns shrinking it |
| --- | --- | --- |
| **Detection lag** | The loss was knowable a long time before it happened. Large is *good news* — it means the warning existed | Nobody. It is a measurement, not a target |
| **Recognition lag** | The warning existed and nobody saw it. This is the number to attack | CS Ops and data |
| **Realised lead time** | The window the team actually worked with. Compare it to the play's required window | CS leadership |
| **Action lag** | Flagged, then nothing happened for N days | CS leadership — routing, capacity, prioritisation |

**A negative realised lead time** — flagged after the decision — is not an edge case. It is common,
and it should be reported as its own count in the quarterly pack, because a team that believes it
is intervening early while half its losses were flagged post-decision is optimising the wrong end
of the process.

## 2. The method

Six steps, run **backwards**. Forwards you find the story you already believe; backwards you find
the first date the evidence supports.

| # | Step | Detail |
| --- | --- | --- |
| 1 | Build the full timeline | `timeline-reconstruction.md`. Do not shortcut to "the obvious signal" |
| 2 | Filter to `known_then = Yes` | Only facts that existed in a system we owned, on the day they happened |
| 3 | Walk backwards from T−0 | At each event ask: *using only what existed on this date, would a competent reviewer have called this account materially at risk?* |
| 4 | Stop at the first Yes | That date is `earliest_detectable_date`. Record the signal ID, the system that held it, and whether a threshold existed |
| 5 | Compute the four lags | Check the identity. A mismatch means a date is wrong — fix the date, not the arithmetic |
| 6 | Classify the failure mode | §4. This determines who owns the fix |

**The "competent reviewer" test needs a floor, or it drifts.** Use this one: the account would
have been called at risk if, on that date, **either** a single override-floor trigger from
`churn-risk` Step 3 had fired, **or** two of the seven families were simultaneously negative on
their own published thresholds in `../../cs-context/references/signal-library.md`. Anything softer
and every account is detectable at signature; anything harder and nothing is detectable until
notice is served.

## 3. What counts as detectable

| Situation | Detectable? | Failure mode |
| --- | --- | --- |
| A metric existed, was computed, and crossed a published threshold | Yes | `unalerted` or later |
| The raw data existed in a source we owned; nobody computed a metric from it | Yes | `uninstrumented` |
| The data existed in a source we could have connected but had not | Yes | `uninstrumented` — an unconnected source is a choice, not an absence |
| The event was public (funding, layoffs, an exec change announced) | Yes, from the announcement date | `uninstrumented` if no enrichment source is connected |
| The fact was internal to the customer and never surfaced anywhere | No | `undetectable` |
| We learned it at the exit interview and there was no proxy in the data | No | `undetectable` |
| A champion departure discovered afterwards, but the hard bounce was in the CRM at the time | **Yes** — the bounce is the detectable form | `unalerted` |

The last row is the one that decides most records. The question is never "did we know?" but
"**was it in something we owned?**" That distinction is what turns a post-mortem into an
instrumentation backlog instead of a set of regrets.

## 4. The six failure modes

Each mode has a different owner, a different fix, and a different cost to close. Getting the mode
wrong sends the fix to the wrong function, where it dies.

| Mode | Definitive test | Fix type | Owner | Typical cost to close |
| --- | --- | --- | --- | --- |
| **`absent`** | The event does not exist in any system, ours or a connectable third party | Emit the event — product instrumentation | Product / data engineering | Weeks to a quarter |
| **`uninstrumented`** | Raw data existed; no metric, no field, no report computed it | Add the metric to the schema and the scorecard | CS Ops | Days |
| **`unalerted`** | The metric existed and was visible; no threshold fired | Set or tune the threshold | CS Ops | Hours |
| **`unrouted`** | An alert fired into a dashboard, digest or channel with no named owner | Assign ownership and a response SLA | CS leadership | Days |
| **`unactioned`** | Routed to a named owner who did not act inside the play's required window | Play design, capacity, or prioritisation | CS leadership | A planning cycle |
| **`undetectable`** | No signal at any lead time in any system | None. Record and stop | — | — |

**The distribution across a quarter is the investment decision**, and most organisations guess it
wrong. A quarter dominated by `absent`/`uninstrumented` is a data problem and buying another tool
will not help; a quarter dominated by `unactioned` is a capacity problem and adding signals makes
it worse. Report the distribution ARR-weighted, not count-weighted.

**`undetectable` is unavailable to the no-decision family** (`no-decision`, `deprioritised`,
`budget-freeze`, `orphaned-renewal`, `budget-loss`). A renewal that lapsed always leaves a dated
antecedent: a renewal opportunity stalled in one stage (C13), a PO never issued (C12), a decision
owner who left with no successor (R1/R3), sixty days with no bilateral contact (Z1). Reaching for
`undetectable` there is how the largest recoverable class of loss gets recorded as weather. The
mode is almost always `unalerted` — nobody watched opportunity stagnation — or `unrouted` — nobody
owned the empty chair. See `root-cause-taxonomy.md` §3a.

`unactioned` deserves particular honesty: it is the most damning mode and the most commonly
recoded as something softer. If the alert fired, was routed to a named person, and the play did
not run inside its window, the mode is `unactioned` even when the person had good reasons. The
reasons belong in the attribution table; the mode belongs to the data.

## 5. The health-score report card

Every record answers one more question, independent of everything above.

> **What band was this account in 90 days before the decision date?**

| `health_at_t90` | Reading | Routing |
| --- | --- | --- |
| Green / Secure | A **false negative of the scoring model**. The model said fine and the account was already deciding | `health-score-designer` as a scoring defect, regardless of reason code |
| Yellow / Watch | The model saw something and under-weighted it. Check which family carried the signal and what its weight was | Weight review after ≥3 corroborating records |
| Red / At Risk or worse | The model worked. The failure, if any, is downstream — `unrouted` or `unactioned` | CS leadership, not the model |

Two aggregates follow from this column and both belong in the quarterly pack:

- **False-negative rate** = churned accounts Green at T−90 ÷ all churned accounts. If churned
  accounts were reliably Green at T−90, the score is decorative and the correct response is to
  rebuild it, not to add a play.
- **Predictive lift** = churn rate of Red accounts ÷ churn rate of Green accounts, from the health
  migration matrix in `retention-report`. Lift and false-negative rate move independently; a model
  can have good lift and still miss the large losses, which is the case that costs the most.

## 6. Aggregate outputs

Maintained per quarter, ARR-weighted throughout. `../scripts/detection_lag.py` computes all of these.

| Output | Definition | What it decides |
| --- | --- | --- |
| **Median and P90 detection lag by `primary_reason`** | Days from earliest detectable to decision | The intervention window each play must fit inside. A play needing 60 days cannot serve a reason whose P90 lag is 45 |
| **Median recognition lag** | Days from detectable to flagged | The size of the detection problem, in days |
| **Median action lag** | Days from flagged to first intervention | The size of the capacity problem, in days |
| **Negative realised lead time count** | Losses flagged after the decision | The credibility check on "we intervene early" |
| **Failure-mode distribution** | ARR by mode | Whether to invest in data, tooling, routing or capacity |
| **Instrumentation backlog** | Signals appearing as `earliest_detectable_signal` ≥3 times and still uninstrumented, ranked by ARR behind them | The CS Ops roadmap, in priority order, with a dollar figure attached |
| **False-negative rate** | Green at T−90 ÷ all losses | Whether the health score is worth keeping |
| **Repeat-cause register** | Causes appearing ≥2 times with the fix promised, its owner, its due date and whether it shipped | The accountability loop. Usually the most uncomfortable table in the pack |

Report **median and P90, never the mean** — the distribution is long-tailed and one 500-day
sponsor-loss record drags a mean far above anything actionable.

## 7. Turning lag into thresholds

The whole point. Rules that keep this honest rather than reactive:

| Rule | Why |
| --- | --- |
| **Never change a weight, threshold or lead time on N=1** (`R22`) | One loss is an anecdote with a date on it. A single record may add a signal to a watch list; it may not move the model |
| **≥3 records with the same failure mode** before a change ships | Three is the practical floor at which a pattern is distinguishable from a coincidence in a book of any size |
| **Set the alert threshold inside the P90 lag, not the median** | A threshold tuned to the median misses the slower half of exactly the reason it was built for |
| **Every proposed change carries a backtest** | §8. A threshold that would have fired on the losses *and* on forty healthy renewals is not a threshold, it is a pager |
| **State the alert budget** | New alerts per CSM per week. If the change adds more than about two, it will be ignored within a month and the model will be blamed |
| **Cumulative, not point-in-time, for support and relationship signals** | The University of Victoria / IBM escalation study (arXiv:1901.01344, 2019) found escalation likelihood must be modelled by aggregating ticket history per customer rather than scoring tickets in isolation `[A]`. The same holds for silence and for multithreading: persistence beats intensity |
| **Log the change** | Date, records behind it, backtest result, owner. A threshold nobody can explain gets reverted by the next person |

Change proposals take one shape:

| Change | Current | Proposed | Evidence | Backtest | Alert budget | Owner | By |
| --- | --- | --- | --- | --- | --- | --- | --- |
| New signal: multithread depth ≤1 for 90 days as an independent flag | Not scored | Hard flag, overrides a healthy usage score | 4 of the last 9 losses; median detection lag 214 d | 12 months of churn plus a control set of 60 renewals | +1.2 alerts/CSM/week | CS Ops | 30 days |

## 8. The backtest protocol

A change validated only against losses will fire on everything. The control set is not optional.

| Step | Detail |
| --- | --- |
| 1. Assemble the loss set | Every record in the last 12 months, labelled on `decision_date` |
| 2. Assemble the **control set** | Renewals that completed in the same window, matched roughly on segment and ARR band. At least 3× the loss set |
| 3. Replay the proposed rule as of T−90 | Features cut off at the observation date, never at the renewal date. This is the single most common backtest error and it makes any rule look excellent |
| 4. Count the four outcomes | Losses caught, losses missed, renewals falsely flagged, renewals correctly quiet |
| 5. Convert to work | Falsely flagged renewals × the play's hours = the cost. Losses caught × ARR × an assumed save rate = the benefit. State the assumed save rate as an assumption, do not bury it |
| 6. Decide with the asymmetry stated | A false positive costs a couple of CSM hours; a false negative costs the ARR. Precision and recall should not be weighted equally, and the report must say what weighting was used `[P]` |
| 7. Publish bands, not probabilities | Without calibration you have an ordering, not a forecast (`R22`). See `../../cs-context/references/calibration-loop.md` |

Report the result in one line the reader can argue with: *"Fires on 7 of 9 losses at a median 148
days before decision, and on 11 of 60 control renewals — about 1.2 extra alerts per CSM per week."*

## 9. A worked calculation

From the fragment in `timeline-reconstruction.md`. Decision 2026-05-14, effective 2026-08-31.

```
earliest_detectable_date = 2025-03-21   sponsor departure (R1) + multithread depth 1 (R4)
                                        both in the CRM the week they happened
first_flagged_date       = 2026-05-23   first internal message naming the account as at risk
first_intervention_date  = 2026-06-02   exec outreach attempted
decision_date            = 2026-05-14

detection_lag   = 2026-05-14 − 2025-03-21 = 419 days
recognition_lag = 2026-05-23 − 2025-03-21 = 428 days
realised_lead   = 2026-05-14 − 2026-05-23 =  −9 days      ← flagged after the decision
action_lag      = 2026-06-02 − 2026-05-23 =  +10 days

identity check: 428 + (−9) = 419 ✓
```

**Reading.** Fourteen months of warning existed inside the CRM. The account was flagged nine days
*after* the decision was administered, so the realised lead time was negative and no play could
have worked at the point it was chosen. The failure mode is `unalerted`, not `unactioned` — the
team acted within ten days of noticing; nothing told them to notice. The fix therefore belongs to
CS Ops (a multithread-depth threshold and a champion-departure flag), not to the CSM, and the
attribution table should reflect that even though the CSM owned the account throughout.

Note also what the numbers do **not** license: the account was Green at T−90 on the current
score, so the record is also a scoring defect and goes to `health-score-designer` — but on its own
it justifies adding the signal to a watch list, not re-weighting the model. That needs two more
records with the same mode.

## 10. Traps

| Trap | Consequence | Correction |
| --- | --- | --- |
| Choosing the most dramatic signal as "earliest detectable" | Understates the lag, flatters the team | Walk backwards to the *first* qualifying date, not the most memorable one |
| Counting hindsight facts as detectable | Manufactures a lag nobody could have used | `known_then = Yes` filter, applied before anything else |
| Using the churn date instead of the decision date | Every lag inflates by the notice period | `R24`. The lag is measured to the decision |
| No `first_flagged_date` recorded anywhere | Recognition lag becomes uncomputable and the whole analysis stalls | Reconstruct from the risk record, forecast-category change, or the first internal message. Then start recording it |
| Truncating the usage series at offboarding | An artificial cliff that reads as the signal | Truncate at `decision_date`; note the export's as-of date |
| Tuning a threshold to the median lag | Misses the slower half of the reason it was built for | Tune inside the P90 |
| Backtesting on losses only | A rule that fires on everything and is ignored within a month | Control set of renewals, ≥3× the loss set |
| Cutting features at the renewal date | Leakage. The backtest looks superb and the live rule does nothing | Cut features at the observation date, T−90 |
| Averaging lags | One long sponsor-loss record dominates | Median and P90, ARR-weighted |
| Treating `unactioned` as `unrouted` because the person had reasons | The capacity problem never gets named or funded | Mode from the data; reasons in the attribution table |
