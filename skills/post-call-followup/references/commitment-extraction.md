# Commitment Extraction and Follow-Through

> How to tell a commitment from a courtesy, how to phrase it so it binds, what to do when the
> customer will not confirm it, and how to make sure the thing you wrote down actually happens.

**Contents**
1. [What counts as a commitment](#1-what-counts-as-a-commitment)
2. [The grade ladder](#2-the-grade-ladder)
3. [Reading a transcript — the linguistic markers](#3-reading-a-transcript--the-linguistic-markers)
4. [Phrasing it back so it binds](#4-phrasing-it-back-so-it-binds)
5. [When the customer will not confirm](#5-when-the-customer-will-not-confirm)
6. [The follow-through system](#6-the-follow-through-system) — including thin answers and unwritten interactions
7. [Commitments we make — the internal gate](#7-commitments-we-make--the-internal-gate)
8. [Commitment debt as a metric](#8-commitment-debt-as-a-metric)

**Evidence convention:** `[M]` measured benchmark · `[V]` vendor-analysed · `[P]` practitioner
rule of thumb · `[D]` derived here from stated inputs.

---

## 1. What counts as a commitment

A commitment passes all three parts. Missing any one makes it a **courtesy statement**, and
recording a courtesy statement as a commitment is the most common way a follow-up email
becomes fiction that the customer then has to correct.

| Part | Passes | Fails | Why it matters |
| --- | --- | --- | --- |
| **Actor** | A named individual | "we", "the team", "someone", "engineering", "procurement" | An unnamed owner is an unowned action — the same failure as a team-wide alert, where everyone assumes someone else has it `[P]` |
| **Act** | An observable, verifiable action — send, approve, provision, schedule, introduce, sign, test, confirm, decide | "look into", "think about", "explore", "consider", "keep in mind", "have a chat about" | You cannot chase "explore". You can chase "send" |
| **Anchor** | A calendar date, or an event with a date attached | "soon", "shortly", "next few weeks", "after the holidays", "once things settle" | Without a date there is no moment at which the commitment is late, so it is never late |

**The verb test.** If you cannot write a sentence beginning *"On <date> I will check whether
<person> has…"*, it is not a commitment. Write the sentence. If it does not complete, downgrade.

**Joint accountability.** Lincoln Murphy's framing is the operating principle: customer success
"is about ensuring your customers know where they fit in and holding them accountable"
(sixteenventures `[P]`). Customer-side commitments are not favours you extract; they are the
customer's half of a relationship that only produces outcomes if both halves happen. Recording
them is not pushiness, it is the mechanism.

---

## 2. The grade ladder

| Grade | Language pattern | Binding | Action | Goes in the recap? |
| --- | --- | --- | --- | --- |
| **A** | First person + specific act + explicit date: "I'll send the security doc by Friday 5 Sept" | Yes | Log verbatim with the speaker and timestamp | Yes, as stated |
| **B** | Plural or hedged actor, soft date: "We can get that over next week" | Partial | Assign a named person and a specific date; state the assumption so it can be corrected | Yes, with your assigned name and date |
| **C** | Intent without an act or a date: "Let me look into that" | No | Convert into an open question with a dated response request, or drop it | Only as an open question |
| **D** | Evaluation, not action: "That sounds useful", "Makes sense", "Interesting" | No | Log as sentiment evidence. **Never** as a commitment | No |
| **E** | Silence following an ask | No | Log in extraction bucket 6 (asked-for and not given) | No — but it changes the Relationship & engagement family |

**The Grade B trap.** Grade B is where most damage happens, because it *feels* agreed. The
correct handling is to convert it in the recap with a named person and a date **and to say you
are doing so**, which gives the customer a cheap way to correct you and converts silence into
agreement. Converting a Grade B silently — writing "Priya will send it Wednesday" when Priya
said "we'll get that over next week" — is a fabrication that the customer will notice.

**The Grade D trap.** "That sounds great" after a proposal is the single most over-read signal
in customer success. It is an expression of politeness under time pressure, not a decision.
Recording it as agreement produces a QBR deck asserting a commitment the customer never made.

---

## 3. Reading a transcript — the linguistic markers

Search the transcript for these patterns before reading it end to end. They surface almost all
commitments and most of the risk language.

| Marker | Pattern to search | What it usually is |
| --- | --- | --- |
| First-person future | "I'll", "I will", "I'm going to", "let me get" | Grade A or B commitment |
| Delegated future | "I'll ask X to", "X will", "we'll have someone" | Grade B — the named X may not know |
| Conditional | "if we can", "assuming", "once we've", "provided that" | A dependency, not a commitment — log the dependency separately |
| Deflection | "let me look into", "I'll come back to you on", "leave that with me" | Grade C — needs a dated response request |
| Politeness | "that sounds", "makes sense", "interesting", "good to know" | Grade D — sentiment only |
| Deadline language | "by", "before", "end of", "ahead of the" | Attach to the nearest commitment; this is your anchor |
| Internal process | "board", "budget cycle", "procurement", "security review", "legal" | A gate on the decision path — belongs in Section B |
| Decision language | "we've decided", "we're going with", "we've stopped" | A decision, not a commitment — bucket 1 |
| Competitor language | "we're also looking at", "comparing", "the other vendor", "consolidating" | Fires the shadow-evaluation trigger the same day |
| Departure language | "my last week", "handing over", "moving teams", "backfilling" | Stakeholder change — fires `stakeholder-map` |

**Talk-time context.** Where the transcript tool provides it, record the talk ratio. It is not
a commitment signal, but a call where you spoke 70% of the time and obtained two Grade-A
commitments is a different call from one where they spoke 60% and committed to the same two
things — the second is durable, the first is compliance.

**Multithreading context.** Gong Labs' analysis of 1.8M opportunities reports that 77% of deals
involve multiple contacts, closed-won deals carry roughly twice as many buyer contacts as lost
ones, and multithreading is associated with a 130% higher win rate on deals over $50K
(Gong Labs, 2025 `[V]` — vendor-analysed sales data, not a CS retention study). Read across:
**who commits matters as much as what is committed.** Two Grade-A commitments from a single
contact is a thinner result than one Grade-A commitment each from two.

---

## 4. Phrasing it back so it binds

Four rules, applied to every commitment before it enters the recap.

| Rule | Bad | Good |
| --- | --- | --- |
| **Name the human** | "Procurement will confirm the PO requirement" | "Dan Petrov will confirm whether a PO is required" |
| **Use their verb, not yours** | "Aisha to align on term length" | "Aisha will decide 12 vs 24 months" |
| **Date it to a weekday** | "by end of month" | "by Fri 3 Oct" |
| **State what it unblocks** | "Send the report formats" | "Send the report formats — stops us building the wrong output" |

**Confirm by default.** Ask for correction, not confirmation:

> "I've recorded the security questionnaire coming back from Priya by Thu 11 Sept — tell me if
> that date needs to move."

This works for a structural reason: correction is a lower-effort reply than confirmation, and
it converts silence from ambiguity into agreement. Asking "can you confirm?" hands a busy
stakeholder a task they can defer indefinitely, and their deferral erases the commitment.

**What it unblocks is not decoration.** A commitment with a consequence attached is chaseable
without sounding like nagging: "the 6 Oct start depends on this" is a reason, where "just
following up on this" is a request for attention. Every Grade A and B commitment in a customer
recap carries its unblock.

**Never invent the date.** If no date can be inferred and the customer did not give one, write
`UNKNOWN — <person> to set a date by <our date>` and make supplying the date your own
commitment. A guessed date presented as theirs is a fabrication under the evidence standard.

---

## 5. When the customer will not confirm

A commitment that is neither confirmed nor corrected is not an administrative gap. It is data
about the relationship, and the ladder below is designed to produce that data on a schedule
rather than leaving it to whoever remembers to chase.

| Step | When | What you send | What it tests |
| --- | --- | --- | --- |
| **0. Recap** | Within 24h of call end | Confirm-by-default phrasing, one ask | Whether they read it at all |
| **1. Consequence nudge** | T+3 business days, no reply | One line naming the consequence, not the ask: *"The 6 Oct site-4 start needs the training window confirmed — is that still achievable at your end?"* | Whether the consequence matters to them |
| **2. Reduce and offer** | T+7 business days | Shrink the commitment to the smallest version that still unblocks us, and offer to do the work: *"If the full list is hard, one name is enough to start."* | Whether the blocker is capacity or intent |
| **3. Change channel** | T+10 business days | Not another email. A call, a Slack Connect message, or a message to a second contact if one exists | Whether the channel was the problem |
| **4. Route as a signal** | T+10 with the opt-out deadline inside 60 days, or any two consecutive ladders unanswered | Stop chasing. Update the Relationship & engagement family, run `churn-risk`, and escalate to the renewal owner | Whether this is an admin problem or a relationship problem |

**Hard rules for the ladder:**

- **Never re-send the same recap.** A resend says the first one did not matter.
- **Each step is shorter than the last.** Length reads as pressure.
- **Do not stack asks.** If a new ask has arisen since the call, it starts its own ladder.
- **Step 4 is a routing decision, not a stronger email.** Three unanswered follow-ups on an
  account with a renewal inside 60 days is a risk signal, and it belongs in the risk model, not
  in your inbox.
- **Single-threaded accounts skip step 3.** There is no second contact, and that absence is
  itself the finding — log it and run `stakeholder-map`.

**When they explicitly decline.** Record the decline verbatim, with the date and the reason if
given, and stop. A declined ask that is re-raised without new evidence damages the relationship
and teaches the customer that "no" does not work on you. Note the decline in the internal note
so the next person does not re-pitch it. Re-raise only when something material has changed, and
say what changed.

---

## 6. The follow-through system

A commitment ledger that is not scheduled is a written record of your own failure. The system
has four parts.

### 6.1 Every commitment becomes a dated task

| Field | Rule |
| --- | --- |
| Owner | Exactly one named person. Never a team, never two people |
| Due | A business-day date, computed from the call date — not "next week" |
| Chase 1 | Due − 2 business days for our commitments (an internal reminder before it is late); Due + 1 for theirs |
| Chase 2 | Due + 3 business days (theirs only) |
| Escalate | Due + 7 business days, to the account owner |
| Exit criteria | The observable thing that proves it is done — "the document is in their inbox", not "sent" |
| Linked to | The `interaction` record for the call, so the commitment survives a CSM change |

`../scripts/followup_schedule.py` computes all of these from the commitment list and the call
date, skipping weekends, so the dates are deterministic and identical every time the skill runs.

### 6.1a Three things enter the schedule, not one

The commitment ledger is the obvious one. Two more carry a date and an owner in exactly the
same way, and both are dropped by every rushed follow-up.

| What | Where it comes from | Owner | Due | Closed by |
| --- | --- | --- | --- | --- |
| **Commitment** (Grade A/B) | Extraction buckets 2 and 3 | The named actor | Business-day date from the call | The exit criteria being observable |
| **Follow-up on a thin answer** (`exchanges` = 1) | Note block 9 | Always us — never the customer | The next scheduled conversation, or a dated ask if none is booked | The question being asked out loud and a second answer recorded, which increments `exchanges` |
| **Unwritten interaction** (past 14 days with no note) | Note block 10 | Always us | 2 business days | The note existing in the account record |

**The follow-up carries its words, not its topic.** The task text is the sentence you will say
— *"And what else is driving the Q1 freeze?"* — so that whoever picks the account up can ask it
without reconstructing your reasoning. A task reading "dig into the budget" is not scheduled
work, it is a note to yourself, and it will produce another one-exchange answer.

**A thin answer never ages into a fact.** If the follow-up task closes without a second
exchange, `exchanges` stays at 1 and the line stays in block 9. Time does not upgrade evidence.

### 6.2 Our commitments are tracked more aggressively than theirs

Asymmetric on purpose. A missed commitment by us is a trust event; a missed commitment by them
is a signal. Ours get an internal chase **before** the due date; theirs get one after.

### 6.3 The weekly sweep

Once a week, across the whole book:

| Check | Threshold | Action |
| --- | --- | --- |
| Our commitments overdue | Any | Close it today or send a dated re-commit — never let it age silently |
| Their commitments overdue >5 business days | Any | Run the §5 ladder from the current step |
| Accounts with ≥3 overdue commitments either way | Any | Relationship & engagement signal; check against the renewal calendar |
| Recaps not sent within 24h | Any | Repair form (`recap-templates.md` §10), and log the latency |
| Commitments with no exit criteria | Any | They cannot be closed; rewrite or delete them |
| Accounts with no written note in 14 days | Any | Write the note today from whatever you have; list what can no longer be reconstructed as `UNKNOWN — requires <person>` rather than inventing it |
| Thin answers (`exchanges` = 1) open ≥ 2 cycles on the central issue | Any | The question is not being asked. Put it first on the next call agenda, or accept the account's central issue is undiscovered and say so in the risk record |

### 6.4 Closing the loop in the next recap

The first line of every subsequent recap for the account states the status of the previous
recap's commitments. This does two things: it makes the ledger visible to the customer without
a chase, and it makes your own misses visible to you before they become a pattern. A success
plan or commitment record only has meaning through "the cadence of returning to it"
(The Success League, 2026 `[P]`).

---

## 7. Commitments we make — the internal gate

Never put a commitment in a customer recap that you have not confirmed internally. A recap is
a written promise on behalf of your company.

| Commitment type | Gate before it goes in writing |
| --- | --- |
| A date from engineering | The named engineer or their lead has agreed to the date. Otherwise write `UNKNOWN — I owe you a date by <our date>` |
| A price, discount, or term | Within your approval authority, or approved. Otherwise: "I'll come back with a formal quote by <date>" |
| A roadmap item | Never commit to unreleased functionality by date. Commit to telling them the status by a date |
| A support or SLA change | The support lead has agreed and can staff it |
| An executive's time | That executive has accepted the invite |
| A credit or commercial remedy | Finance and your manager have approved the shape, even if not the number |
| A contractual change (sunset date, entitlement, notice) | Legal or deal desk has confirmed it. This ends up in a contract dispute if it is wrong |

**The substitution rule.** When the gate is not cleared, do not omit the topic — that reads as
avoidance. Substitute a commitment you *can* make, which is almost always a commitment to
provide the answer by a date. "I owe you a date by Friday" is a real commitment with a real
owner; "we'll look into it" is not.

---

## 8. Commitment debt as a metric

Commitment debt is the count and age of overdue commitments, weighted by the ARR of the
accounts they sit on. It is a leading indicator that is entirely within your control, which
makes it unusually useful.

| Measure | Formula | Read |
| --- | --- | --- |
| Open debt (ours) | Count of our commitments past due | >3 per CSM is a capacity problem, not a discipline problem `[P]` |
| Debt age | `today − due_date`, max across open items | An item 14+ days overdue will not be recovered by chasing; re-commit with a new date and say so |
| ARR under debt | Σ ARR of accounts with ≥1 of our overdue commitments | The dollars exposed to a trust event |
| Their-side stall rate | Their overdue ÷ their total commitments, per account | ≥50% on an account with a renewal inside 90 days is a Relationship & engagement signal, not an admin issue |
| Recap latency | Median hours from call end to recap sent | Track per CSM; the 24-hour rule is `[P]`, so treat this as a process control, not a benchmark |

**Where it feeds.** ARR under debt and their-side stall rate both feed the Relationship &
engagement family in `churn-risk`. A CSM with high commitment debt is not producing a
relationship signal; they are producing noise in one, and their accounts will read healthier
than they are.
