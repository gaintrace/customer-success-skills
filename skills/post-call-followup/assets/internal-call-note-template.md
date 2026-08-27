# Internal Call Note — emit verbatim

> **INTERNAL. Never send, forward or paste any part of this into a customer channel.**
> Written **before** the customer recap. Paste into the CRM activity record and link it to the
> `interaction` row for this call.

---

# Call Note — <Account> · <meeting type> · <date, call end time>

**Attendees — theirs:** <name, title, role> · <…>
**Attendees — ours:** <name, role>
**No-shows / late / early departures:** <who, and when — or "none">
**Recording:** <link, or "notes only — sentiment confidence capped at Low">
**Objective grade:** Achieved / Partially — <gap> / Not achieved — <why> / No objective was set
**Last written note on this account:** <date> · <N> days ago · <M> interactions since with no note
<Computed, never estimated. Past 14 days, block 10 is mandatory and lists one row per unwritten
interaction. Where the account history is unavailable, write
`UNKNOWN — requires the account's interaction history` and treat block 10 as mandatory anyway.>

## 1. What happened
<Observed only. No interpretation. Agenda covered, who spoke, what was shown, time split,
what you did not reach.>

## 2. What was said → what it likely meant
| Quote (verbatim + timestamp) | Who said it | `exchanges` | Inference | Rule applied | What would falsify it |
|---|---|---|---|---|---|

<`exchanges` is required on every row and must be **≥ 2**. A line with one exchange on the
account's central issue is not a finding — move it to block 9. An empty `exchanges` cell
invalidates the block.>

## 3. Sentiment read
| Person | Read | Evidence (quote + time) | Prior read | Change |
|---|---|---|---|---|

**Sentiment confidence:** High / Medium / Low — <criteria met>

## 4. Stakeholders
| Name | Title | Role (schema enum) | New / changed / departed | Influence 1–5 | Evidence |
|---|---|---|---|---|---|

**Named but not present:** <who, and what authority they appear to hold>
**Not in the room but should have been:** <names, or "none">

## 5. Competitive intelligence
| Vendor named | Exact quote | Who said it | Evaluation stage | Confidence |
|---|---|---|---|---|

<Or: "None mentioned — checked, clear.">

## 6. Signal family deltas
| Family | Change from this call | Direction ↑/↓/none | Evidence | Feeds |
|---|---|---|---|---|
| Product usage & adoption | | | | churn-risk |
| Commercial & contract | | | | renewal-forecast |
| Relationship & engagement | | | | churn-risk |
| Support & reliability | | | | save-play |
| Sentiment & VoC | | | | churn-risk |
| Billing & payment | | | | renewal-prep |
| Firmographic & external | | | | expansion-finder |

<Untouched families print "No change — not covered on this call". Never delete a row.>

## 7. What this contradicts in the account plan
| Account plan assumption | What the call showed | So what changes (owner + date) |
|---|---|---|

<Or: "Nothing contradicted the plan.">

## 8. Commitment ledger
| # | Owner | Action | Due | Grade | Expected effect | Success measure | Source (quote + time) |
|---|---|---|---|---|---|---|---|

**Asked for and not given:** <what we requested and did not get an answer to — or "none">
**Commitment debt carried into this call:** <N overdue · oldest D days · covering $ARR>

## 9. Open questions and thin answers
| # | Question / thin answer | Who owes the answer | `exchanges` | Follow-up to ask (verbatim) | Owner | Due |
|---|---|---|---|---|---|---|

<Every extraction-bucket-4 line, and every bucket-5 fact on the central issue that got only one
exchange, lands here. Both `exchanges` and the follow-up are required — the follow-up is the
literal sentence you will say next time ("And what else is driving the Q1 freeze?"), never a
topic ("dig into the freeze"). A row missing either cell is invalid, not a draft. Nothing in
this block may appear as a finding in block 2, as evidence in the CRM diff, or as a decision in
the customer recap. Or: "None — every central-issue line reached two or more exchanges.">

## 10. Not written down anywhere else
| What I know | How I know it | Why it was never written | Where it is being written now | Owner | Due |
|---|---|---|---|---|---|

<The context that exists only in your head: the aside before the call started, why a name is
never mentioned, the history the previous owner told you, the thing you would say if you were
handing this account over tomorrow. Empty is not a valid value. Write
"None — blocks 1–9 carry everything I know about this account" only when that is literally true.
Past 14 days since the last written note, add one row per unwritten interaction; where it can no
longer be reconstructed, write `UNKNOWN — requires <person>` and log it as a gap rather than
inventing the content.>

---

## Disclosure tags applied
| Class | Count | Notes |
|---|---|---|
| `SHARE` | | Goes to the customer verbatim |
| `TRANSLATE` | | Customer-safe counterpart written for each |
| `INTERNAL` | | Never leaves this record |
