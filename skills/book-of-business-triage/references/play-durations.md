# Play Durations

> What each CS play actually costs in CSM hours, so a weekly queue fits the week. Read whenever
> you are costing a queue row. Every figure here is a **practitioner calibration `[P]`** — a
> defensible starting point, not a measured benchmark. Replace each one with your own measured
> median as soon as you have eight instances.

**Contents**
1. [The costing rule](#1-the-costing-rule)
2. [Master duration catalogue](#2-master-duration-catalogue)
3. [Segment and complexity multipliers](#3-segment-and-complexity-multipliers)
4. [Other people's time — the hidden second bill](#4-other-peoples-time--the-hidden-second-bill)
5. [Compression rules — what you may cut and what you may not](#5-compression-rules)
6. [The six estimation errors](#6-the-six-estimation-errors)
7. [Measuring your own durations](#7-measuring-your-own-durations)
8. [Duration against return — the shape of a good queue](#8-duration-against-return)
9. [Anti-patterns](#9-anti-patterns)
10. [Evidence register](#10-evidence-register)

---

## 1. The costing rule

**A play's duration is the total book capacity it consumes, end to end.** It always includes
five components, and omitting any of them is how a 12-hour queue turns into a 19-hour week.

| Component | Typically | Why it is not optional |
| --- | --- | --- |
| **Pull** — assemble the data the play needs | 15–60 min | Walking into a call without the usage trend produces a status meeting |
| **Prep** — decide the objective and the ask | 10–30 min | An objective written as "<person> will have <commitment> by <date>" is the difference between a call and a chat |
| **Delivery** — the meeting, the message, the session | as scheduled | — |
| **Follow-up** — the recap with commitments, owners and dates | 15–45 min | The commitment log is the asset; the call is the event |
| **Write-up** — notes, CRM/CS-platform fields, health adjustment, next step | 10–20 min | Unlogged work gets redone. Rediscovery is the most expensive hour in CS |

> **Never quote the invite length as the cost.** A 30-minute cadence call is **1.25 hours** of
> book capacity. A 60-minute business review is **6–14 hours**. The gap between these two
> statements is the entire reason weekly plans fail.

---

## 2. Master duration catalogue

All figures are CSM hours for a mid-market, named-coverage account, English-language, single
product, no travel. Apply §3 multipliers for anything else.

### 2.1 Asynchronous plays

| Play | Hours | Pull | Prep | Deliver | Follow-up | Write-up | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Templated nudge (no personalisation) | 0.1 | — | — | 0.1 | — | — | Only honest if the template already exists |
| Async check-in, data-backed | 0.5 | 0.2 | 0.1 | 0.1 | — | 0.1 | The workhorse of a pooled book. One usage fact, one question, one ask |
| Written value snapshot (1 page) | 1.25 | 0.5 | 0.25 | 0.25 | — | 0.25 | Substitute for a QBR on a tech-touch account |
| Commitment chase (overdue item) | 0.25 | — | 0.1 | 0.1 | — | 0.05 | Cheap and high-return; never defer it |
| Stakeholder intro request | 0.4 | 0.1 | 0.15 | 0.1 | — | 0.05 | The first step of every re-multithread |
| Rot-sweep checkpoint | 0.25 | 0.1 | — | 0.1 | — | 0.05 | One targeted question, one logged answer |
| Post-incident written apology + plan | 1.5 | 0.5 | 0.5 | 0.25 | — | 0.25 | Needs facts checked with support/engineering first |

### 2.2 Calls

| Play | Hours | Composition |
| --- | --- | --- |
| Cadence call, 30 min | **1.25** | 0.25 pull + 0.25 prep + 0.5 call + 0.25 follow-up/write-up |
| Cadence call, 60 min | **2.0** | 0.25 + 0.25 + 1.0 + 0.5 |
| Discovery / re-discovery call | 2.0 | Heavier prep, lighter data pull |
| New-stakeholder introduction | 1.75 | Includes history reconstruction the new contact was not part of |
| Renewal conversation, mid-market annual | **3.0** | Brief (0.75) + call (1.0) + internal pricing alignment (0.5) + order-form chase (0.75) |
| Renewal conversation, enterprise | 5.5 | Adds procurement/legal coordination |
| Escalation day-one response | **2.5** | Timeline reconstruction (1.0) + customer comms (0.5) + internal owner assignment (0.5) + write-up (0.5) |
| Escalation ongoing, per week while open | 2.0 | Standing update cadence; the cost that surprises people |
| Save-play kickoff (Critical account) | 4.0 | Internal war-room prep, plan, exec brief |
| Executive sponsor re-engagement call | 2.5 | Exec-level prep is not the same as CSM-level prep |
| Handover call (to a new owner) | 1.5 | Plus 1.0 of written handover — see 2.5 |

### 2.3 Working sessions

| Play | Hours | Notes |
| --- | --- | --- |
| Adoption reset working session | **4.5** | Usage pull by team (1.0) + agenda and materials (1.0) + 60-min session (1.0) + written 30-day plan (1.0) + write-up (0.5) |
| Onboarding kickoff | 5.0 | Includes internal handoff from Sales and the success-plan draft |
| Feature enablement / training session | 3.0 | Assumes existing materials; +2.0 to build them |
| Integration unblock session (with an SE) | 3.0 | CSM hours only; consumes SE hours too — see §4 |
| Success-plan build or re-baseline | 4.0 | The artifact renewals are argued from |
| Champion-departure re-multithread | **3.5** | Map (0.5) + intro requests (0.5) + two discovery calls (2.0) + write-up (0.5) |

### 2.4 Business reviews

| Play | Hours | Notes |
| --- | --- | --- |
| Automated value snapshot (tech-touch) | 0.25 | Review and release; the build is a program cost, not an account cost |
| Templated QBR from live data (growth tier) | 4.0 | Deck generated, then edited; 60-min delivery |
| Operational QBR, mid-market | 6.0 | Prep 2.5 + alignment 0.5 + delivery 1.0 + follow-up 1.0 + write-up 1.0 |
| **Live EBR, enterprise** | **8–14** | Practitioner range covering prep, internal alignment calls, delivery and follow-up `[P]`. Use 11 as the planning midpoint |
| EBR with onsite travel | 14–24 | Travel is capacity, not overhead |

**The agenda is the delivery hour only.** However you structure the 60 minutes in the room, the
other 7–13 hours — prep, the internal alignment call, follow-up and the write-up — are the reason
business reviews must be *reserved* in the plan weeks ahead, never squeezed into the week they
occur. A business review booked on Monday for Thursday is a status call with a deck.

### 2.5 Commercial and expansion

| Play | Hours | Notes |
| --- | --- | --- |
| CSQL handoff to sales | **1.0** | Evidence assembly (0.5) + CRM record (0.25) + warm intro (0.25). A CSQL without linked signal records is an opinion |
| Expansion business case | **5.0** | Sizing (1.5) + value evidence (1.5) + materials (1.0) + internal pricing check (1.0) |
| Seat true-up conversation | 2.0 | Disclose over-consumption within 5 business days of detection, with the value it produced |
| Price-increase pre-brief | 2.5 | Always separate from a business review |
| Multi-year / co-term restructure | 4.0 | Needs deal desk; long calendar tail |
| Contract admin (order form, PO chase, signature) | 1.0 | Per cycle, and it always takes longer than it should |

### 2.6 Internal and hygiene

| Play | Hours | Notes |
| --- | --- | --- |
| Weekly triage itself (this skill) | 0.75 | Monday plan |
| Mid-week re-triage | 0.25 | Only when >20% of the budget was displaced |
| Friday close-out | 0.5 | Completion ledger and carry-forward decisions |
| Written handover pack | 1.0 | Plus the 1.5-hour handover call |
| Risk review prep for a manager | 1.0 | Per weekly review |
| CRM hygiene sweep | 0.5 | Per week; if it is more, the fields are wrong, not the CSM |
| Churn post-mortem | 3.0 | Non-negotiable after any loss above the segment threshold |

---

## 3. Segment and complexity multipliers

Apply multiplicatively, and cap the compound multiplier at **2.5×** — beyond that the estimate
is fiction and the play should be re-scoped or staged.

| Factor | Condition | Multiplier |
| --- | --- | --- |
| Segment | Tech-touch / pooled | ×0.6 |
| | Mid-market named | ×1.0 |
| | Enterprise named | ×1.5 |
| | Strategic / top 5–10% ARR | ×2.0 |
| Stakeholders | 1–2 on the call | ×1.0 |
| | 3–5 | ×1.2 |
| | 6+ or multi-department | ×1.5 |
| Products | Single | ×1.0 |
| | Multi-product | ×1.3 |
| Relationship state | Established | ×1.0 |
| | New stakeholder, or first contact in >120 days | ×1.4 |
| | Post-escalation | ×1.5 |
| Data readiness | Dashboard exists | ×1.0 |
| | Manual pull required | ×1.4 |
| | Identity join is broken for this account | ×1.8 |
| Language / timezone | Same | ×1.0 |
| | Interpreter or >6h offset | ×1.3 |
| Travel | Remote | ×1.0 |
| | Onsite | +6 to +16 h flat, not a multiplier |

**Worked.** An enterprise adoption reset for a multi-product account with six stakeholders and
a broken usage join: 4.5 × 1.5 × 1.5 × 1.3 × 1.8 = 23.7 h → **capped at 4.5 × 2.5 = 11.25 h**,
and the cap is itself the finding: this is not a single play, it is a two-week project. Stage
it — fix the join first (its own row), then run the session.

---

## 4. Other people's time — the hidden second bill

A queue that only counts CSM hours will book work that other teams cannot absorb, and the play
stalls at 80% complete. Record the second bill on any row that needs it, and check it before
committing a date.

| Play | Also consumes | Typical | Booking lead time |
| --- | --- | --- | --- |
| Integration unblock session | Solutions engineer | 3–6 h | 1 week |
| Escalation day-one | Support lead + engineering triage | 4–10 h | Same day |
| Live EBR | Exec sponsor (ours) | 1.5–2 h | 3 weeks |
| | Product marketing / analyst for data | 2–4 h | 1 week |
| Expansion business case | Deal desk / pricing | 1–2 h | 3 days |
| | AE | 2–4 h | 1 week |
| Renewal, enterprise | Legal | 2–5 h | 2 weeks |
| Save play (Critical) | CS leadership + exec sponsor | 3–6 h | Same week |
| Churn post-mortem | Product + Sales + Support | 3 h total | 2 weeks |

**Rule.** If the second bill needs a person who cannot be booked inside the play's deadline,
the play does not go above the cut line this week. Put the *booking request* above the cut
line instead — 0.25 h — and the play in next week's queue. A half-run play is worse than a
deferred one, because it consumes the customer's goodwill without delivering the outcome.

---

## 5. Compression rules

Capacity pressure is constant, so the question is not whether to compress but what compresses
safely.

| Component | Safe to compress | Never compress | Why |
| --- | --- | --- | --- |
| Pull | ✅ Use a saved view or a standing dashboard | The buying-team breakout | Aggregate usage is the most common false-green |
| Prep | ✅ Reuse the last brief and diff it | The one-sentence objective | Without it the call has no ask |
| Delivery | ✅ 60 → 30 minutes with a tighter agenda | Exec attendance on an EBR | No executive, no EBR — downgrade it to a QBR instead |
| Follow-up | ⚠️ Bullet form, same day | The commitment list with owners and dates | The commitment log is the durable asset |
| Write-up | ⚠️ Fields only, prose later | The next-step date and the health change | An account with no next step is an account that will rot |

**The five legitimate compressions**, in the order to reach for them:

1. **Batch the pull.** One data pull covering ten accounts costs less than ten pulls. Saves
   0.15–0.3 h per account.
2. **Convert synchronous to asynchronous.** A cadence call (1.25 h) becomes a data-backed
   written check-in (0.5 h). Acceptable for maintenance; not for anything with a commercial ask.
3. **Template the artifact, personalise the evidence.** Every artifact must still carry at
   least three account-specific data points with provenance, or it is a mail merge.
4. **Merge adjacent plays.** A cadence call plus a commitment chase is one call, not two rows.
5. **Stage the play.** A 12-hour play becomes a 2-hour scoping step this week and a booked
   block next week. This is compression of *this week*, not of the play.

**The two illegitimate ones:** dropping the follow-up (the customer experiences this as being
ignored after being asked questions), and dropping the write-up (the next person to touch the
account pays for it, and often that person is you in six weeks).

---

## 6. The six estimation errors

| # | Error | Signature | Correction |
| --- | --- | --- | --- |
| 1 | **Invite-length costing** | Queue hours ≈ meeting minutes | Use §2 |
| 2 | **Omitting the write-up** | The plan fits; Friday does not | Write-up is 10–20 min of every play |
| 3 | **Assuming materials exist** | "Training session, 3 h" with no deck | +2.0 h to build; make it its own row |
| 4 | **Ignoring the second bill** | Play stalls waiting for an SE | §4, and book the person first |
| 5 | **Costing the happy path** | Every renewal takes exactly 3.0 h | Use the median of your own last eight, not the fastest |
| 6 | **Serial-play blindness** | Three plays for one account in one week | Sequence them; a customer can absorb roughly one substantive ask per fortnight |

---

## 7. Measuring your own durations

Eight instances of a play type is enough to replace the `[P]` figure here with a local median.

```
Local duration = median( actual end-to-end hours for the last 8 instances )
Spread         = P90 ÷ median      # if >2.0, the play is not one play — split it
```

**Logging method that survives contact with a busy week:** at the Friday close-out, record one
line per completed queue row — play type, account, planned hours, actual hours. Nothing else.
Eight weeks of that produces a calibrated catalogue, a measured realisation factor
(`capacity-model.md` §4), and the evidence for a capacity conversation.

| Local median vs this file | Reading |
| --- | --- |
| Consistently 20%+ lower | Either your accounts are simpler, or the write-up is not happening. Check the CRM |
| Within ±20% | Use the local figure |
| Consistently 50%+ higher | Look for a systemic tax: a broken data join, a missing template, an approval loop |

---

## 8. Duration against return

Return per hour is what ranks the queue, so the duration is half of every ranking decision.
The pattern below is the reason a severity-ranked queue underperforms a throughput-ranked one.

| Play | Hours | Illustrative value at stake | RPH ($/h) | When it wins |
| --- | --- | --- | --- | --- |
| Commitment chase | 0.25 | $18,000 (Watch, $120k ARR × .15) | 72,000 | Almost always. Cheapest row in CS |
| Async check-in | 0.5 | $9,000 | 18,000 | Maintenance on a pooled book |
| Cadence call | 1.25 | $21,000 | 16,800 | Named mid-market maintenance |
| CSQL handoff | 1.0 | $14,000 (expansion $40k × .35 win) | 14,000 | Health gate passed |
| Renewal conversation | 3.0 | $84,000 (At Risk, $240k × .35) | 28,000 | Inside the opt-out window |
| Adoption reset | 4.5 | $84,000 | 18,667 | Root cause is adoption and it is addressable |
| Expansion business case | 5.0 | $30,000 ($100k × .30 win) | 6,000 | Only when capacity is not the binding constraint |
| Live EBR | 11.0 | $210,000 (High, $350k × .60) | 19,091 | Strategic tier, booked weeks ahead |
| Save-play kickoff | 4.0 | $297,500 (Critical, $350k × .85) | 74,375 | Top of the queue, every time |

Values above are illustrative arithmetic, not outcomes. The read: **the cheapest plays and the
most expensive accounts both rise to the top, and mid-cost mid-value work is what gets cut.**
That is the correct behaviour under a hard capacity constraint, and it is exactly what a
severity-sorted list gets wrong.

---

## 9. Anti-patterns

| Anti-pattern | Correction |
| --- | --- |
| Costing a call at its invite length | Play duration, all five components |
| A queue row with no hour estimate | Every row is costed or it is not a row |
| "Quick call" | There is no quick call; there is a 1.25-hour play |
| Booking an EBR in the week it happens | Reserve 8–14 hours across the two to four weeks before it |
| Counting only CSM hours | Record the second bill and book that person first |
| Dropping the follow-up to make the week fit | Compress the pull and the prep instead |
| Running three plays on one account in one week | One substantive ask per fortnight; sequence the rest |
| Using this file's numbers forever | Replace each with your own median at eight instances |
| Presenting these durations as benchmarks | They are `[P]` practitioner calibrations |
| Treating the RPH column above as revenue | It ranks work; it does not forecast outcomes |

---

## 10. Evidence register

| Claim | Value | Source | Year | Label |
| --- | --- | --- | --- | --- |
| Live EBR fully loaded cost | 8–14 CSM hours (prep, alignment, delivery, follow-up) | Practitioner consensus recorded in CS operating guidance | — | `[P]` |
| Pre-read lead time | 48 hours before the review | Practitioner consensus | — | `[P]` |
| Business-review runway | 2–4 weeks of preparation | Practitioner consensus | — | `[P]` |
| Disclose over-consumption within 5 business days of detection | 5 days | Practitioner rule against the "true-up ambush" | — | `[P]` |
| Post-Sev-1 cooldown before a commercial ask | 14 days | Practitioner | — | `[P]` |
| Every other duration in §2 | as stated | Practitioner calibration for this library | — | `[P]` |

**Label key:** `[M]` measured benchmark with a named neutral study · `[P]` practitioner rule of
thumb, no published measurement · `[A]` academic. Nothing in §2 is a measured benchmark. Say "commonly costed at", never
"research shows".
