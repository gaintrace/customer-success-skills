# Advocacy Register — <team or book> · as-of <date>

**Internal.** Contains readiness scores, fatigue calls and assessments of named people. It is
never sent to a customer, never attached to a deal, and never shared outside the account team and
customer marketing (`R18`). When customer marketing needs the shortlist, send columns
1–4 of §1 only.

---

## 1. The pool

One row per **advocate** (a person), not per account.

| # | Account | Advocate | Title | Fit cells | Readiness | Ceiling | Asks (12mo) | Ref calls (yr) | Last ask | Next eligible | Fatigue |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | | | | | /100 | rung N | x / 3 | x / 4 | | | ok / rest / freeze |

`Ceiling` is the lowest of: the readiness band's ceiling, every disqualifier's ceiling, and the
business model's ceiling. `Next eligible` = `max(last_ask + 45d, cap reset date)`.

## 2. Ask log

One row per **ask**, written when it is **sent**. Never backfilled from memory.

| # | Date sent | Account | Advocate | Rung | Asked by | Channel | Outcome | Outcome date | Delivered | Cost weight | What we gave back | Given on |
|---|---|---|---|---|---|---|---|---|---|---|---|---|

Outcome ∈ `accepted` · `declined` · `withdrawn` · `no_response` · `deferred`.
**A blank `What we gave back` is a debt.** Clear every blank row before the next ask to that
person.

## 3. Approvals on file

| Account | Permission | Scope (exact placements) | Granted by | Granted on | Expires | Evidence |
|---|---|---|---|---|---|---|

Permissions expire with the contract term and with the departure of the person who gave them.
Re-confirm annually and on any champion change. A logo or quote still published under a lapsed
permission is a contract breach, not a marketing error.

## 4. Coverage cells

| Cell (segment × industry × use case × persona) | Advocates | Status | Nearest candidate | Ready by |
|---|---|---|---|---|

Target **≥3 advocates per cell**. Report every cell under three — an empty cell is a measurable
revenue drag and the only line in this document that tells the business where to invest.

## 5. Rest and repair list

| Advocate | Account | Reason | Burn type | Freeze until | Owed to them | Owner |
|---|---|---|---|---|---|---|

Burn type ∈ `over-asked` · `mismatched` · `unrewarded` · `exposed` · `not burned — routine rest`.

## 6. Declines and withdrawals — 12 months

| Date | Account | Advocate | Rung | Reason given | Read as | Routed to | Owner | Closed |
|---|---|---|---|---|---|---|---|---|

**Every `withdrawn` row opens a `churn-risk` run in the same week.** A previously agreed reference
that is taken back is a P0 relationship signal, not a scheduling problem.

## 7. Unfilled requests

| Date | Requested by | Cell needed | Why unfilled | What we offered instead | Days open |
|---|---|---|---|---|---|

Feeds the reference supply ratio (`requests fulfilled ÷ requests received`) and names the cells to
recruit into next quarter.

## 8. Period summary

| | |
|---|---|
| Advocates in pool · Ready / With limits | |
| Cells covered (≥3) / total cells | |
| Asks sent · accepted · declined · withdrawn | |
| Decline rate (TTM) vs prior period | |
| Reference supply ratio | |
| Customer-sourced pipeline (attributable) | $ |
| Advocacy-influenced pipeline (**reported separately, never summed**) | $ |
| Advocates rested or frozen this period | |
| Open debts (blank `What we gave back`) | |

**Attribution note, included every period:** advocates are selected for health, so any comparison
of their retention against the base is confounded. Match on segment, ARR band, tenure and
prior-period health, or report it as correlational.

## 9. Assumptions

| # | Assumption | Why it was needed | If wrong |
|---|---|---|---|

One row per default taken, each with a concrete consequence. Delete the section only if nothing
was assumed.
