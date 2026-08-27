# Data Integrity and the Publish Gate

> Run this before every edition. Twenty-two checks, four of which stop the publish outright.
>
> The instant a CFO finds a variance, the entire report is discarded — including the correct
> numbers. Integrity work is not overhead on the report; it is the reason anyone acts on it.

**Contents**
- [1. The reconciliation ladder](#1-the-reconciliation-ladder)
- [2. The twenty-two pre-publish checks](#2-the-twenty-two-pre-publish-checks)
- [3. Faults that survive a clean-looking export](#3-faults-that-survive-a-clean-looking-export)
- [4. Population discipline](#4-population-discipline)
- [5. The restatement protocol](#5-the-restatement-protocol)
- [6. Definition change log](#6-definition-change-log)
- [7. When the data will not support the report](#7-when-the-data-will-not-support-the-report)

---

## 1. The reconciliation ladder

Reconcile upward. Each rung must tie before the next is attempted; a break at rung 2 makes
everything above it unverifiable.

| Rung | Tie | Tolerance | If it breaks |
| --- | --- | --- | --- |
| 1 | Billing subscriptions → billing ARR rollup | $0 | Billing extract is incomplete or filtered. Re-pull |
| 2 | Billing ARR → finance ARR balance | $0 | Do not publish. The delta is almost always a definition difference (services, one-time fees, signed-not-live) — find it, name it, and write it into the definitions page |
| 3 | Finance ARR → the bridge's ending ARR | $0 | An arithmetic or classification error inside the bridge. Check the Contraction/Churn boundary first |
| 4 | Bridge beginning ARR → prior period's published ending ARR | $0 | A restatement has occurred. Label it (§5); never let it pass silently |
| 5 | CRM contract records → billing subscriptions | ≤2% of accounts | Report the join rate. Above 2%, do not use CRM fields for anything quantitative this edition |
| 6 | Product analytics accounts → billing accounts | ≥90% join rate | Below 90%, note it. Below 80%, usage-derived health is **Low confidence** — the unjoined accounts are not randomly distributed |
| 7 | Support org IDs → accounts | ≥90% | Below that, the support section is directional and must say so |

**Rung 2 is the gate.** ARR that does not reconcile to the general ledger's recognised revenue
is the single fastest way to lose the room: reporting one set of numbers to the board and
another in the GL erodes credibility the moment someone asks which one is real.

---

## 2. The twenty-two pre-publish checks

**Blocking — the report does not publish** ⛔

| # | Check | Why |
| --- | --- | --- |
| 1 | Bridge ties to finance ARR at $0 variance | Rung 2 above |
| 2 | Beginning ARR equals the prior period's published ending ARR, or a restatement is labelled | A silent restatement invalidates every trend line you have ever published |
| 3 | Every definition change since the last edition is logged and history is restated | Trend lines built on two definitions are not trend lines |
| 4 | No contributing source is stale past its tolerance (see §3) without being marked | A number true six weeks ago will be quoted as current |

**Capping — publish, but with a stated confidence cap** ⚠️

| # | Check | Cap if it fails |
| --- | --- | --- |
| 5 | GRR ≤ 100% for every segment and the blend | A GRR above 100% is a calculation bug — expansion has leaked into the numerator |
| 6 | Logo retention ≤ 100% everywhere | New logos have leaked into the cohort |
| 7 | Cohort membership frozen at t0 in the query, not filtered at read time | The single most flattering error in retention analysis |
| 8 | Churned accounts remain in the retention denominator at $0 | Survivor bias |
| 9 | Reactivation excluded from the GRR/NRR numerator | Win-backs are new revenue, not retained revenue |
| 10 | Bridge components sum to the ending balance without a plug | A plug line is an unexplained variance wearing a name |
| 11 | Contraction and churn are mutually exclusive; no account appears in both | Down-to-$0 is Churn, and double-counting it inflates both lines |
| 12 | Multi-product accounts netted at account level before classification | Otherwise SKU A expansion and SKU B contraction both book, double-counting movement |
| 13 | Currency: constant-currency basis stated, FX rate date recorded | An FX move attributed to customer behaviour |
| 14 | Account population reconciled to prior period (see §4) | A population change presented as a business result |
| 15 | `is_internal` exclusion rule documented and applied identically to both periods | Employee and sandbox accounts inflating usage and logo counts |
| 16 | Every rate has its numerator and denominator printed | "Churn improved to 4.1%" beside a base that shrank 20% |
| 17 | Every cell under 20 accounts or 2% of base is asterisked | Small-n noise read as a trend |
| 18 | Immature cohort cells blank, not zero | A blank means *does not exist*; a zero means *lost everything* |
| 19 | Health bands unchanged between t0 and t1, or t0 restated under the new bands | A migration matrix across re-cut bands measures the re-cut |
| 20 | Forecast snapshots are immutable and vintage-dated | Grading a field edited all quarter measures field hygiene, not forecasting |
| 21 | Churn dated on the decision date, not the contract end date (R24) | Any model built on it learns the notice period |
| 22 | Reason-code `other` below 15% of coded churn ARR | The taxonomy is broken; fix before publishing the mix |

Record the result of all twenty-two in the working file, not just the failures. Next month's
author needs to know check 12 was run and passed.

---

## 3. Faults that survive a clean-looking export

The export opens, the columns look right, the totals are plausible, and the numbers are wrong.

| Fault | How it presents | How to catch it |
| --- | --- | --- |
| **Money as text** | XLSX from finance with `$1,240.00 ` including a trailing space; sums silently to 0 or concatenates | `ingest.py` reports the parsed type per column; check the ARR column's confidence and its min/max |
| **Export preamble** | Three title rows above the real header; the first data row becomes the header | `ingest.py` locates the real header row; verify the mapped column names are field names, not values |
| **Mixed date formats** | `03/04/2026` meaning both 3 April and 4 March in the same column | Check the day/month distribution: if no value above 12 appears in the first position, the column is ambiguous. Ask; never guess |
| **Silent truncation** | The row count is a round number: 1,000 / 5,000 / 65,536 | Compare the account count to the prior period and to the billing system |
| **Timezone boundary** | A month-end churn lands in the wrong month; the bridge misses by one account | Check that period boundaries are applied in a single stated timezone |
| **Duplicate rows from a join fan-out** | ARR total is a clean multiple of the true value | Count distinct `account_id` and compare to row count |
| **A filter left on** | A segment is missing entirely; the total looks plausible | Reconcile the account count by segment against the prior period |
| **Deleted-record semantics** | Churned accounts absent from the export rather than present with `status='churned'` | If churn count is 0 on a base with known losses, the export is filtered to active |
| **Stale sync** | Every number correct as of eleven days ago | Compare `max(updated_at)` per source against its expected latency |
| **Currency mixing** | EUR contracts summed as USD | Check for a currency column; if absent, ask whether the export is already normalised |
| **Parent/child double count** | ARR exceeds the finance balance by exactly one large customer's subsidiaries | Roll up on `parent_account_id` and compare both totals |
| **Free-email domain matching** | Product users at a paying account unmatched, so usage reads near zero | Check the join rate for the specific accounts that look dead |

**Source staleness tolerances** (from `../../cs-context/references/evidence-standard.md` §7):
product usage 3 days · billing 7 days · support tickets 2 days · CRM 7 days · email/calendar
3 days · survey 90 days · transcripts 45 days · firmographic 30 days. Past tolerance, mark the
number stale in the report; do not extrapolate it forward.

---

## 4. Population discipline

The base changes for legitimate reasons and for illegitimate ones. The report must be able to
tell them apart, and the reader must not have to.

Publish this table whenever the account count moves by more than 1%:

| Movement | Accounts | ARR | Rule applied | Legitimate? |
| --- | --- | --- | --- | --- |
| Opening population | | | | |
| + New logos | | | `account.start_date` in period | Yes |
| + Reactivations | | | Outside the win-back window | Yes |
| − Churn | | | `arr = 0` at period end | Yes |
| ± Reclassified internal | | | `is_internal` rule, documented | Only with the rule stated |
| ± Parent/child roll-up change | | | `parent_account_id` change | Only if both periods are restated |
| ± Re-segmentation | | | New ACV boundary | Requires a pro-forma view |
| ± Acquisition | | | Acquired book added | Show as-reported and organic |
| Closing population | | | | |

Rules that hold every period:

- The `is_internal` exclusion rule is written down once and applied identically to both periods.
  Changing it mid-year without restating is a restatement whether or not you call it one.
- Reclassifying a parent/child relationship changes logo counts and ACV bands, and therefore
  moves every rate that uses either. Restate both periods.
- An acquisition means every rate needs an organic view beside the as-reported one, for at least
  four quarters. A blended NRR spanning an acquisition is not comparable to anything, including
  itself.

---

## 5. The restatement protocol

Restatement is routine and legitimate. **Silent** restatement destroys the credibility of every
number the function has ever published — including the ones that never changed.

**When a restatement is required**

| Trigger | Restate |
| --- | --- |
| A metric definition changed | All periods shown in any trend, minimum eight |
| A segment boundary moved | All periods, plus a pro-forma bridge between old and new segmentation |
| Health bands were re-cut | Both t0 and t1 of every migration matrix shown |
| A data error is found in a published number | The affected period and everything derived from it |
| An acquisition closed | Four quarters, as-reported and organic |
| A source was replaced | All periods sourced from the old system, with the join rate stated |

**The protocol**

1. **Publish the restatement as its own labelled line**, never as a quietly corrected number.
   Use `../assets/restatement-notice.md`.
2. **State the size and the direction.** "TTM GRR restated from 84.1% to 83.4%, −70bps."
3. **State the cause in one sentence**, without euphemism. "Twelve accounts reclassified from
   Contraction to Churn after a review found they had reached $0 ARR mid-term."
4. **State what changes downstream.** Which decisions were made on the old number, and whether
   any of them would have been different.
5. **State what prevents recurrence**, with an owner and a date.
6. **Keep the old number visible** in the change log for at least four periods. Erasing it is
   what makes people suspect the new one.

**The one thing never to do:** restate a number upward without the same ceremony you would give
a downward restatement. A favourable correction published quietly is the fastest way to teach
the room that the numbers move to suit the narrative.

---

## 6. Definition change log

Maintained in the appendix, dated, append-only. One row per change, never edited afterwards.

| Date | Metric | Old definition | New definition | Reason | Periods restated | Effect on the current period | Owner |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2026-04-01 | GRR | Formula method | Cohort method | Formula method understates by charging in-year logo churn to the cohort | 8 quarters | +110bps | CS Ops |
| 2026-06-01 | At-risk | Health band ≤ At Risk | Declared state with written entry/exit criteria | Band-derived at-risk cannot be saved or exited, so save rate was meaningless | 2 quarters | At-risk ARR −$2.1M; save rate now computable | VP CS |

Rules: no change lands mid-quarter without the restatement in the same edition; two definition
changes in one edition are a signal that the metric set is unstable and should be frozen for a
year; every change names the decision it improves, or it is churn for its own sake.

---

## 7. When the data will not support the report

Degrade; do not refuse, and do not fabricate a substitute.

| Situation | What to publish |
| --- | --- |
| No finance ARR balance to tie to | The bridge, marked `Reconciliation: UNKNOWN — requires the finance ARR balance as at <date>`, with confidence capped at Low and every retention figure labelled provisional |
| No prior-period health snapshot | Distribution only, plus a one-line note that the snapshot starts this period and the first matrix publishes next period. Never reconstruct bands retrospectively from current data — it produces a matrix that shows what the score would have said, not what it did say |
| Coverage below 40% of the seven signal families | The gap list and the bridge. No scored health section, no at-risk figure |
| Product analytics join rate below 80% | Usage-derived sections marked Low confidence, with the join rate printed. Do not extrapolate the unjoined accounts |
| Reason codes missing on more than 30% of churned ARR | Publish the churn total and the named losses; publish the reason mix as coverage-limited, with the covered share stated, and put "code the backlog" in §14 with an owner and a date |
| One segment has fewer than 20 accounts | Report it, asterisk it, and do not benchmark it or draw a trend through it |
| A source is stale past tolerance | Print the number with its staleness attached: `[Salesforce · Contract · last sync 2026-08-11, 15d stale]`. Never carry the prior period forward silently |

In every case the rule is the same: name the gap, state what it would take to close it, cap
confidence, and publish what you do have. A partial report published on time with its gaps
declared is worth more than a complete report published late — and infinitely more than a
complete-looking report with a benchmark standing in for a missing number.
