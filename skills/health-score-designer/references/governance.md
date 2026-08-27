# Governing the Score

> Read when writing Step 11, planning a rescore, or answering "why did my account change band
> overnight and nobody told me?"

**Contents**
- [The governance objects](#the-governance-objects)
- [§1 — Versioning](#1--versioning)
- [§2 — Rescore and migration comms](#2--rescore-and-migration-comms)
- [§3 — Refresh cadence](#3--refresh-cadence)
- [§4 — Anti-gaming](#4--anti-gaming)
- [§5 — Never compensate on the score](#5--never-compensate-on-the-score)
- [§6 — The quarterly review agenda](#6--the-quarterly-review-agenda)

---

## The governance objects

| Object | Rule | Consequence of skipping it |
| --- | --- | --- |
| **Owner** | One named person in CS Ops. Not a committee, not a team, not a working group | A score with no owner drifts, breaks quietly, and dies over about three quarters |
| **Versioning** | Semantic — §1 | Nobody can say which model produced last quarter's numbers |
| **Change control** | Champion/challenger — the new config runs in shadow for one full renewal cycle before it drives a single play | You find out the new weights are worse by losing accounts |
| **Rescore comms** | Migration matrix published *before* the rescore lands — §2 | Trust destroyed once, permanently |
| **Refresh** | §3 | Either a frozen score or a score that cannot be backtested |
| **Coverage** | Track "% of ARR-bearing accounts with a valid score". GitLab carried >95% as a company-level yearly goal | A score covering 60% of the book cannot forecast retention |
| **Volatility** | Track the share of accounts changing band per month | High band churn means cliff-edged transforms or noisy inputs, and CSMs stop believing band changes |
| **Escalation** | A documented route for "this score is wrong about my account" that produces either an override with an expiry or a model finding | CSMs route around the tool instead of improving it |

## §1 — Versioning

| Change | Bump | Requires |
| --- | --- | --- |
| Dimensions added or removed · the label or horizon changed · archetype changed | **major** | Full re-backtest, restated history or a stated discontinuity, migration matrix, CSM comms |
| Weights changed | **minor** | Re-backtest, migration matrix |
| Thresholds or band cuts moved | **patch** | Migration matrix, and history restated or the change dated in every trend chart |

**Every version keeps its spec and its backtest, permanently.** A version whose backtest cannot
be produced is a version whose numbers cannot be defended, and the request always arrives during
a board meeting rather than before one.

**Freeze weights for a full renewal cycle before judging them.** Re-weighting monthly makes
backtesting impossible, because every backtest is then run against a different score.

## §2 — Rescore and migration comms

A silent rescore is the fastest way to lose a CS team. On the morning a CSM's account moves from
Green to Red with no explanation, they learn that the number is arbitrary — and that lesson does
not un-learn.

**The sequence, in order:**

| # | Step | Timing |
| --- | --- | --- |
| 1 | Publish the migration matrix — old band × new band, counts and ARR | ≥1 week before cutover |
| 2 | Send each CSM the list of *their* accounts that move, with the reason per account | ≥1 week before |
| 3 | Hold one 30-minute session: what changed, why, and what to do with the accounts that moved | Before cutover |
| 4 | Cut over. Keep the old score computing in parallel | Day 0 |
| 5 | Review disagreements between old and new on the accounts that moved most | Day 30 |
| 6 | Retire the old score | Day 90 |

**The migration matrix:**

| Old ↓ / New → | Green | Yellow | Red | Insufficient | Total | ARR |
|---|---|---|---|---|---|---|
| Green | | | | | | |
| Yellow | | | | | | |
| Red | | | | | | |

**Read-outs required before cutover:** how many accounts move ≥2 bands (if it is more than ~5%,
the change is a major and the comms need to be heavier); which CSM is most affected; and whether
any account moves Red→Green purely because a dimension went NA. That last one is a bug every
time.

## §3 — Refresh cadence

| Object | Cadence | Why not more often |
| --- | --- | --- |
| **Composite score** | Daily | Faster than daily invites reacting to noise; the consecutive-period rule already costs a week of lead time |
| **Score history** | Retained **forever**, never overwritten | It is the only asset that makes validation possible, and it cannot be recovered retroactively |
| **Calibration map** (score → probability) | Quarterly | It absorbs base-rate drift, which is what actually moves |
| **Band cuts** | Quarterly | Moving them mid-quarter breaks every trend chart in the business |
| **Weights** | Semi-annually, or after one full renewal cycle | See §1 — monthly re-weighting makes backtesting impossible |
| **Full redesign** | Annually, or on a pricing / product / segment change | A redesign costs a quarter of trust; do not spend it on a hunch |

**Off-cycle triggers that override the calendar:** a pricing model change, a new product line
that changes what adoption means, a segment redefinition, a PSI above 0.25, or three consecutive
false-greens sharing a single failure pattern.

## §4 — Anti-gaming

Goodhart's law applies the moment the score is tied to compensation, QBR review, or CSM
performance management. Every one of these has happened in a real CS org.

| Gaming route | What it looks like | Control |
| --- | --- | --- |
| **Sentiment inflation** | Everyone's accounts are Green sentiment | Mandatory written justification, timestamped. Publish per-CSM sentiment-vs-outcome calibration: a CSM whose Greens churn at 3× the average is miscalibrated, not unlucky |
| **Routine overrides** | The tool is right; the CSM disagrees; the override becomes habit | Cap at ≤10% of portfolio per quarter, expiry date on every override, and a monthly list of overrides that were later vindicated or not |
| **Contact stuffing** | Twelve contacts added the week before the score runs | Require **persona coverage** plus a two-way interaction inside 90 days. Count personas, not contacts |
| **Meeting theatre** | A recurring internal calendar hold counted as engagement | Require external attendees from target personas |
| **Ticket suppression** | Discouraging customers from filing, to keep the support dimension green | U-curve the support dimension — zero tickets scores 60, not 100 |
| **Threshold surfing** | Effort targeted at accounts one point below a band edge | Continuous transforms underneath, bands only at the display layer |
| **Value-event inflation** | The definition of a "value event" quietly widens | Version the event taxonomy. A taxonomy change is a **major** score version |

**The tell that gaming is happening:** score distribution improves while retention does not. Plot
them on the same axis every quarter. If the score is rising and GRR is flat, the score is being
managed rather than the customers.

## §5 — Never compensate on the score

Compensate on **retention and expansion outcomes**. Use the score to allocate attention.

The moment the score is the target, it stops being a measurement — and unlike most Goodhart
failures, this one is invisible for two or three quarters because the score genuinely improves
before the outcomes fail to follow.

There is a claim in circulation that heavily weighting CSM sentiment is associated with *worse*
retention. It is a blog assertion with unpublished methodology `[V]`, so do not cite it as
evidence. Test it directly instead: you already have per-CSM sentiment-vs-outcome calibration
from §4, which answers the question on your own book with your own data.

## §6 — The quarterly review agenda

Ninety minutes, one owner, the same six items every time. The point of a fixed agenda is that
the uncomfortable items cannot be crowded out by the interesting ones.

| # | Item | Artifact |
| --- | --- | --- |
| 1 | **Unforecast churn** — every account Green at quarter start that churned | One written post-mortem each. These are defects in the model, not in the CSM |
| 2 | Migration matrix for the quarter | Predictive lift (Red loss rate ÷ Green loss rate), recovery rate from Red, degradation rate from Green |
| 3 | Drift: PSI, band volatility, staleness rate, score coverage | `calibration.md` §7 thresholds |
| 4 | Does-anyone-act-on-it, all six tests | `audit-checklist.md` |
| 5 | Per-CSM sentiment calibration | §4 |
| 6 | Open overrides and their expiries | §4 |

**Close every review by naming the single change with the largest expected effect on
discrimination, its owner and its date** — or by stating that no change is warranted this
quarter, which is a legitimate and under-used outcome.
