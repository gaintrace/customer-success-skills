# Brief Variants by Meeting Type

> The ten-section spine in `../SKILL.md` is constant. What changes by meeting type is the
> **order**, the **depth**, and the **three or four sections that carry the meeting**. This
> file specifies those, plus the one thing each meeting type most often gets wrong.

**Contents**
[Routine check-in](#routine-check-in) · [QBR / EBR](#qbr--ebr) · [Renewal conversation](#renewal-conversation) ·
[Escalation](#escalation) · [Expansion](#expansion) · [New stakeholder intro](#new-stakeholder-intro) ·
[Technical review](#technical-review) · [Handover / covering](#handover--covering) ·
[First call after a bad quarter](#first-call-after-a-bad-quarter) · [Cross-cutting rules](#cross-cutting-rules)

---

## Routine check-in

**Length: one page. The failure mode: having nothing to say, and saying it anyway.**

| Lead with | Depth |
| --- | --- |
| 1. Since-last-time delta — the single most important change | Full |
| 2. Open commitments, ours first | Full |
| 3. One observation worth their time | Full |
| 4. Everything else | Reference only |

A check-in with no agenda is the meeting customers quietly stop attending. The brief must
supply **one specific, data-grounded observation** the customer does not already know — a
team that started using a feature, a usage pattern that changed, a ticket trend, a peer
benchmark. If the brief cannot produce one, it should say so and recommend cancelling or
converting the meeting rather than filling thirty minutes.

**Objective form:** *"By the end of this call, Priya will have told us whether the Finance
rollout is still happening this quarter, and we will have scheduled the enablement session
for a date in October."*

---

## QBR / EBR

**Length: full brief, plus the deck. The failure mode: preparing the deck and not the room.**

| Lead with | Depth |
| --- | --- |
| 1. Attendees — especially who is new and who is senior | Full, with each person's stated priority quoted |
| 2. Their stated business objectives and the movement against each | Full — this is the meeting |
| 3. Value evidence with the arithmetic | Full |
| 4. Where we fell short, stated before they raise it | Full |
| 5. The asks — theirs and ours | Full |
| 6. Product usage | Evidence for §2, not a section of its own |

Pair with `qbr-builder` for the deck. The brief's distinct job is the **room**: who is
attending, what each of them personally needs to hear, who will object, and who has to say
yes for the next-period plan to be real.

**Nothing is decided here for the first time.** Every decision the QBR must reach carries a
pre-wire status in §2 — who has been spoken to, what they said in their own words, what is
unresolved. An **Unwired ❌** decision on a QBR agenda is printed in the ⚠️ block as a
derailment risk before the brief is emitted, with one of two recommendations: pre-wire it by a
named date, or drop it from this meeting and take it separately. A surprise in front of a
customer's own exec is refused in public and cannot be revisited for a quarter.

The champion pre-brief is the first pre-wire, not a courtesy. If it has not happened, that is
an unwired agenda, not a scheduling detail.

**Objective form:** *"By the end of this QBR, Marcus (VP Ops) will have agreed to the three
Q4 success measures and named an owner on his side for each, and we will have a date for the
Finance-team expansion discussion."*

---

## Renewal conversation

**Length: full brief. The failure mode: preparing the price and not the decision process.**

| Lead with | Depth |
| --- | --- |
| 1. **Opt-out deadline and days remaining** | Full — this governs everything |
| 2. Commercial posture: auto-renew, discount expiry, uplift, last cycle's difficulty | Full |
| 3. Decision process: `signs` · `decides` · `influences` by name, who blocks, budget cycle, procurement path | Full — a renewal brief with `signs` or `decides` UNKNOWN prints it in the ⚠️ block and opens with the authority test |
| 4. Value evidence, in their terms | Full |
| 5. Risk band and the specific signals | Full |
| 6. Competitive position | Full |
| 7. Objections — especially price | Full, minimum four prepared |

Pair with `renewal-prep` for the runbook and `renewal-negotiation` for the commercial
position. The brief's distinct job is knowing, before the call, **what has to be true for
them to sign and who has to make it true**.

Two things this brief must always contain and often does not: the **paper process lead times**
(security review, MSA redlines, PO issuance, vendor portal) and **what happened at the last
renewal** — how hard it was, what was conceded, and what was promised.

**Objective form:** *"By the end of this call, Dana will have confirmed the budget is approved
and named the procurement contact, and we will have agreed the paper timeline against a
2 September opt-out date."*

---

## Escalation

**Length: full brief. The failure mode: leading with explanation instead of accountability.**

| Lead with | Depth |
| --- | --- |
| 1. Timeline of the failure — dated, factual, no framing | Full |
| 2. What we owe them and what is overdue | Full |
| 3. What we can commit to, with named owners | Full |
| 4. What we cannot commit to, and why | Full |
| 5. Who is in the room on both sides and their sentiment | Full |
| 6. Everything else | Minimal — this meeting has one subject |

Pair with `save-play`. The brief must contain the **honest chronology first** — every date, every
missed SLA, every promise made and broken. Anything that reads as a defence in the brief will
read as a defence in the room, and that is how escalations become churn.

**Never bring a commitment to an escalation that has not been agreed internally first.** The
brief must state, for each commitment, who inside our company has agreed to it. A commitment
made in the room and retracted afterwards ends the relationship.

**Objective form:** *"By the end of this call, Ken will have accepted the remediation plan
with the three committed dates, and we will have agreed a weekly 15-minute checkpoint until
the P1 is closed."*

---

## Expansion

**Length: full brief. The failure mode: pitching before the value case is established.**

| Lead with | Depth |
| --- | --- |
| 1. Health band — and whether the health gate is passed | Full. **If the account is At Risk or worse, the brief recommends postponing the expansion conversation and says why** |
| 2. Value already delivered, quantified | Full |
| 3. The signal driving the expansion case (utilisation, limit, new team, feature-gate hits) | Full, with the arithmetic |
| 4. The sized opportunity and the business case | Full |
| 5. Who has budget authority for the increment — often not the current buyer | Full |
| 6. Timing relative to the renewal and opt-out dates | Full |

Pair with `expansion-finder`. The brief's distinct job is confirming that the **value ask has
been earned** and that the person who can approve the increment will be in the room.

**Objective form:** *"By the end of this call, Sofia will have agreed to introduce us to the
Finance team lead, and we will have a date for a scoping session before the 14 October
budget submission."*

---

## New stakeholder intro

**Length: medium. The failure mode: assuming inherited context and goodwill.**

| Lead with | Depth |
| --- | --- |
| 1. What they inherited: the contract, the history, the open items | Full |
| 2. What they were not part of: the original decision, the promises made | Full |
| 3. Who they replaced and what that person cared about | Full |
| 4. What is currently broken or overdue | Full |
| 5. What we want from the relationship | Full |

Assume **zero inherited context and zero inherited goodwill.** A new stakeholder did not make
the buying decision and owes it nothing. The brief should prepare a re-justification, not a
status update — see `churn-risk` Regime change and `save-play` §exec re-justification.

**Objective form:** *"By the end of this call, Alex will have stated what they are measured on
this year, and we will have agreed one thing we can help with in the next 60 days."*

---

## Technical review

**Length: full brief. The failure mode: a business brief handed to an engineering audience.**

| Lead with | Depth |
| --- | --- |
| 1. Integration health and any silent failures | Full |
| 2. Open defects with Jira/Linear IDs and committed dates | Full |
| 3. Version, upgrade state, and anything unsupported | Full |
| 4. Custom work in place and who maintains it | Full |
| 5. Performance and scale headroom | Full |
| 6. Technical stakeholders and who approves change windows | Full |
| 7. Commercial | One line |

Pair with `fde-account-plan`. Engineering audiences detect and discount hand-waving instantly.
Every claim needs an ID, a version number, or a measurement.

---

## Handover / covering

**Length: everything, plus an explicit unknowns section. The failure mode: not knowing what you don't know.**

Include every section at full depth, then emit **§6a — Undocumented Knowledge: Gap List**.

This is a list, not a paragraph. A prose section describing what we do not know is not a gap
list, because nobody can chase a paragraph. Every row resolves to exactly one of two values,
and the section prints its own count: **`N items · M open gaps · K unchased`**.

| Value | Written as |
| --- | --- |
| **Answered** | `Answered — <the finding>` plus the source and date it was read from |
| **Gap** | `GAP — requires <named person>` plus the exact question to ask them, a chaser, and a date |

A gap with no named person, no date, or no exact question is invalid output. "Ask Sam about the
discount" is not an exact question; *"Why was the 18% discount approved in Feb 2025, and was
anything promised in exchange?"* is.

| # | What the previous owner knew | Why it matters on this call | Where to look first | Status |
| --- | --- | --- | --- | --- |
| 1 | Why the discount was given, and against what | It sets the floor for the renewal number | Opportunity notes, approval chain, the executed order form | |
| 2 | What was promised verbally and never written | A commitment we do not know about is one we will break in the room | Call transcripts, email threads, the last QBR deck | |
| 3 | Who dislikes us, and why | An unknown detractor surfaces in the approval step | Sentiment in transcripts, escalation history, who stopped attending | |
| 4 | Who actually signs and who actually decides | `signs`/`decides` inherited as UNKNOWN is the finding, not a gap in the finding | Executed contract signature block, procurement thread | |
| 5 | The real reason the stalled rollout stalled | The status note and the reason are rarely the same thing | Notes, tickets, meeting cadence, the team that went quiet | |
| 6 | What we got wrong at the last renewal | It is the objection you will be asked to answer without knowing it exists | Renewal debrief, concession log, the previous owner | |
| 7 | Standing agreements about cadence, channel and escalation path | Breaking an unwritten norm in week one costs more than the norm was worth | Recurring invites, Slack channel history | |

**Any open gap that bears on a decision in §2 is copied into the ⚠️ block** — a covering CSM
walking into a pre-wired decision without the previous owner's context derails it in the room.
Every open gap carries a named chaser and a date, and the handover conversation is booked as a
walk-out commitment in §12, not left as an intention.

A covering CSM walking in unaware of a verbal promise is the most common way a covered account
is damaged, and it is entirely a documentation failure — nothing in the account data records a
promise that was made out loud.

---

## First call after a bad quarter

**Length: full brief. The failure mode: opening with good news.**

Order: the miss → the cause → what changed → what we are asking them to do differently → then
everything else. Open with the miss. A customer who has had a bad quarter with you knows it,
and hearing the good news first tells them you either did not notice or hoped they had not.

---

## Cross-cutting rules

| Rule | Applies to |
| --- | --- |
| The ⚠️ block appears only for something genuinely urgent — an overdue commitment we owe, a new attendee, a contract event, an open escalation, an opt-out deadline inside 30 days | All |
| Overdue commitments **we** owe always precede anything else, regardless of meeting type | All |
| Product usage is broken out by team, including the buyer's team | All |
| Three questions maximum. More than three means none get asked properly | All |
| A named walk-out commitment and a fallback | All |
| Expansion openings withheld below the health gate, with the withholding stated | All |
| Marked internal; no risk language phrased as if customer-facing | All |
| The talk track and any pre-call note sit inside a `text` fence below the customer-facing divider, with every slot filled | All |
| Every default the brief ran on is stated under the title and carries an Assumption Register row with a concrete consequence | All |
| The as-of date of every export is printed; nothing is extrapolated past it | All |
| `signs` · `decides` · `influences` each print a name or `UNKNOWN — requires X`; never a title, never blank | All |
| Two or three of the authority fields resolving to one person prints as a concentration risk, never as simplicity (`R5`) | All |
| No price, concession or expansion ask in the walk-out slot while `signs` is UNKNOWN or out of the room — the authority test replaces it | All |
| Every decision the meeting must reach carries a pre-wire status; Unwired decisions are pre-wired by a named date or dropped | All, mandatory on QBR and renewal |
| Acceptance latency, reschedule count and who accepted are printed even when nothing fired; two consecutive reschedules by `signs` or `decides` is a relationship signal reported independently of usage | All |
| The three questions each carry a named anchor, and none is answerable from the brief's own sections | All |

---

## Output hygiene — all variants

| Anti-pattern | Correction |
| --- | --- |
| Aggregate usage only | Break out by team; the buyer's team is the one that matters |
| Listing every open ticket | The two that will come up in the room, plus a count of the rest |
| "Sentiment: positive" with no source | Quote them, with a date and where the quote came from |
| A brief that takes 20 minutes to read | One-Pager on top, detail below — the One-Pager is the part that gets read |
| A section deleted because it was empty | "No open escalations" is a fact the reader needs to be able to rely on; mark it checked and clear |
| The ⚠️ block printed on every brief | A permanent warning is not a warning. It prints for the listed conditions and is otherwise omitted |
