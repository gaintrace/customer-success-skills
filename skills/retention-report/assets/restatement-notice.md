# Restatement Notice — Template

> Emit verbatim into §13 Operating Notes whenever a previously published number changes.
>
> Restatement is routine and legitimate. **Silent** restatement destroys the credibility of every
> number the function has ever published, including the ones that never moved. The ceremony below
> is identical whether the correction is favourable or unfavourable — a quiet upward restatement
> teaches the room that the numbers move to suit the narrative.

---

## The block

```markdown
### ⚠️ Restatement — <metric>, <periods affected>

| | |
|---|---|
| **What changed** | <metric> for <period(s)> restated from **<old value>** to **<new value>** |
| **Size and direction** | <±X bps> / <±$Y> — <favourable / unfavourable> |
| **Cause** | <One sentence, no euphemism. What was wrong and how it was found.> |
| **Periods restated** | <n> periods, <first> through <last> |
| **Downstream effect** | <Which other published figures move, and by how much.> |
| **Decisions made on the old number** | <Name them. State whether any would have been different.> |
| **Prevention** | <The control that stops recurrence> — owner <name>, in place by <date> |
| **Old value retained in** | Change log, appendix A6, visible for the next <n> periods |
```

---

## Worked example

```markdown
### ⚠️ Restatement — churned ARR, FY26 Q4

| | |
|---|---|
| **What changed** | FY26 Q4 churned ARR restated from **$2,240k** to **$2,410k** |
| **Size and direction** | +$170k churn; TTM GRR restated 85.3% → 85.1%, **−20 bps** — unfavourable |
| **Cause** | Three Mid-Market accounts were booked as Contraction in Q4. A review of mid-term ARR balances found all three had reached $0 ARR before the contract end date, which makes them Churn under the boundary rule published in the definitions page |
| **Periods restated** | 1 period — FY26 Q4. TTM series recomputed for 4 periods |
| **Downstream effect** | FY26 Q4 contraction restated $1,180k → $1,010k. Logo retention FY26 Q4 restated 90.2% → 89.9%. Segment: all three accounts are Mid-Market; MM GRR restated 81.9% → 81.4% |
| **Decisions made on the old number** | The Q1 coverage plan assumed Mid-Market GRR above 82% and left 14 MM accounts in the pooled tier. At 81.4% those accounts sit below the named-coverage threshold. That decision is being revisited in §14 |
| **Prevention** | Monthly reconciliation of accounts with `arr = 0` against their contract end date, added to the pre-publish checklist as check 11 — owner Dana Osei, in place from the 2026-09-07 edition |
| **Old value retained in** | Change log, appendix A6, visible through the 2026-12 edition |
```

---

## Rules

| Rule | Why |
| --- | --- |
| Publish as its own labelled block, never as a quietly corrected number | A corrected number with no notice is indistinguishable from an error nobody caught |
| State size **and** direction, in the metric's own units and in basis points | "Restated" without a magnitude tells the reader nothing about whether to care |
| One sentence of cause, without euphemism | "A methodology refinement" is how a reader learns to distrust the next twelve editions |
| Name the decisions made on the old number | This is the part everyone skips, and it is the part that matters. If none would have changed, say that explicitly |
| Prevention carries an owner and a date | Otherwise it is an apology, not a control |
| Keep the old value visible for at least four periods | Erasing it is what makes people suspect the new one |
| Apply the identical ceremony to a favourable restatement | Asymmetric disclosure is the fastest way to lose the room permanently |
| Never restate mid-quarter without publishing it in the same edition | A trend line silently rebuilt between editions is worse than no trend line |

## When a restatement is required

| Trigger | Restate |
| --- | --- |
| A metric definition changed | All periods shown in any trend, minimum 8 |
| A segment or ACV boundary moved | All periods, plus a pro-forma bridge between old and new segmentation |
| Health bands were re-cut | Both t0 and t1 of every migration matrix shown |
| A data error is found in a published number | The affected period and everything derived from it |
| An acquisition closed | 4 quarters, as-reported and organic |
| A source system was replaced | All periods sourced from the old system, with the join rate stated |
