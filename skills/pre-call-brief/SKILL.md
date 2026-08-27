---
name: pre-call-brief
description: "When the user has a customer conversation coming up and needs to walk in prepared. Also use when the user mentions 'prep me for', 'brief me on', 'I have a call with', 'meeting with', 'call tomorrow', 'what do I need to know', 'account brief', 'call prep', 'one-pager on', 'catch me up', 'who am I talking to', 'who has to say yes on their side', 'I know nothing about them', or 'I'm covering for'. Use this whenever a customer conversation is imminent, even if they don't ask for a brief and only mention the meeting in passing. For the QBR deck itself, see qbr-builder. For what to send afterwards, see post-call-followup. For risk depth, see churn-risk. For who is in the room, see stakeholder-map."
license: MIT
metadata:
  version: 1.1.0
  role: CSM | AM | FDE | VP CS | CCO
  cadence: per-meeting
---

# Pre-Call Account Brief

You are preparing a senior customer success leader to walk into a customer conversation
knowing more about the account than the customer expects, and more about the *objective* than
the customer's own team has articulated. The brief is read in the five minutes before the
call. Everything in it must survive that constraint.

The rookie version is a data dump in chronological order. The elite version answers four
questions in the first fifteen seconds — **what is this call for, who has to say yes, what
could go wrong, and what am I trying to walk out with** — and supports each with evidence the
CSM can quote out loud without checking a second screen.

Read `../cs-context/references/evidence-standard.md` first. Anything you cannot source is
marked `UNKNOWN — requires X`, never guessed: a brief with an invented number is worse than no
brief, because it gets said out loud to the customer.

## Before Starting

1. **Read `.agents/cs-context.md`** (fallback `.claude/cs-context.md`). If absent, run
   `cs-context`. Never ask for anything that file already answers — ARR, renewal date, notice
   period, segment boundaries, owning CSM, fiscal year, or which systems are connected.

2. **Establish the meeting by reading it, not by asking.** Account, date, duration, type,
   attendees on both sides, organiser, stated agenda — and the invite's own audit trail: sent,
   accepted, declined, rescheduled, by whom and when. That trail is the input to the calendar
   signals in Step 4, not administrative detail. The full read-it/ask-it table, the intake
   batch with its option text, and the file-handling rules are in `references/brief-intake.md`
   — read it **before you ask the user anything**.

3. **Every missing input resolves exactly one of three ways** — **read it** from the data,
   `cs-context` or the invite; **ask it** only when two likely answers produce a materially
   different brief; or **mark it** `UNKNOWN — requires <source>`. Filling a gap with a
   plausible value is not one of the three: a brief is read out loud, and an invented number
   gets quoted to the customer by the person who trusted it.

   Ask with `AskUserQuestion`, **all four questions in a single batch** — meeting type, prep
   time, what they want to walk out with, and what data you can work from. Two to four
   mutually exclusive options each, recommended first and labelled, one line under each saying
   what it changes. Skip any the invite or `cs-context` already answers. **Never block:** if
   the batch goes unanswered, run on the four defaults, state them in one line under the
   title, and give each one an Assumption Register row with a concrete consequence.

4. **Take the data in whatever shape it arrives** — CSV, TSV, XLSX, JSON, NDJSON, warehouse
   results, a pasted transcript, a forwarded thread, a screenshot described in prose, or
   nothing but answers to those four questions. Run `../cs-context/scripts/ingest.py` on every
   supplied file first, **confirm every column mapping below 0.80 confidence** before its
   numbers reach the brief, **degrade rather than refuse** — a coverage figure and a capped
   confidence beat an error, and the only stop condition is coverage under 40% — and **never
   assume an export is current**: ask the as-of date, print it under the title, and do not
   extrapolate past it.

5. **Classify the meeting type — it changes the order, the depth and which sections carry the
   brief.** Eight variants with their lead sections, depth and failure mode are specified in
   `references/brief-by-meeting-type.md`; read it now rather than after drafting — routine
   check-in · QBR/EBR (pair `qbr-builder`) · renewal (`renewal-prep`) · escalation
   (`save-play`) · expansion (`expansion-finder`) · new stakeholder intro · technical review
   (`fde-account-plan`) · handover or covering, which is full depth plus the §6a gap list.
   Depth follows Q2: the One-Pager alone for ≤10 minutes, the Full Brief otherwise.

## How This Skill Works

Always assembled in this order, because it is the order a person needs them:
**Objective → The room and who has to say yes → Pre-wire status → Relationship and calendar →
Commercial posture → Product reality → Open commitments → Support & delivery → Risks and
openings → Objections → What to ask → What to walk out with → The talk track.**

**The One-Pager is Brief mode and it is the default** — emitted first, complete on its own,
readable in the five minutes before the call; the full brief follows underneath it. Every
section is populated or explicitly marked absent. Nothing is dropped for being empty: "no open
escalations" is a fact the CSM needs to know they can rely on.

---

## Step 1 — Fix the objective before gathering anything

Write the meeting objective in one sentence, in this form:

> By the end of this call, **<named person>** will have **<agreed to / committed to / understood>**
> **<specific thing>**, and we will have scheduled **<next step>** for **<date>**.

If the objective cannot be written this way, the meeting has no purpose and the brief says so —
that is a finding. "Build the relationship" is not an objective; "Sanjay agrees to introduce us
to the Finance team lead by 12 Sept" is. Everything gathered from here is filtered by: *does
this help achieve the objective, or prevent it being derailed?* Anything that does neither goes
in the appendix or nowhere.

## Step 2 — The room: attendees, and who has to say yes

For each customer attendee: name, title, role (economic buyer / champion / coach / admin /
power user / blocker / technical evaluator / procurement), influence, sentiment, tenure, when we
last spoke and about what, their stated priorities quoted with a date, and **anything they asked
for that we have not delivered** — that last one is the trap. Flag anyone new explicitly: a new
attendee is the single most common reason a prepared call goes sideways.

Then, separately from the role column, fill **three named fields**. The signer is often not the
decider, and neither is reliably the person whose opinion moves the decision; treating them as
one is how a renewal is lost after a positive call with the wrong person.

| Field | The question it answers | Evidence that counts |
| --- | --- | --- |
| `signs` | Whose signature goes on the order form, and who raises the PO | Signature block of the executed contract · delegation-of-authority threshold · procurement confirmation |
| `decides` | Who chooses whether the spend continues, and can kill it alone | Budget line ownership · a decision they already made on this line · procurement naming them as requester |
| `influences` | Whose opinion moves `decides` | Cited by name in others' emails · attends their internal review · wrote the requirements |

Each field prints **a person's name** or `UNKNOWN — requires <specific source>`. A title, a
team, a blank cell or `TBD` is invalid output. `signs` and `decides` hold one name each; two
contending candidates means `UNKNOWN` plus both names, because "one of these two" is not
knowing. Three mechanical consequences, all computed rather than judged:

- **Two or three fields resolving to one person → print the concentration**, in §1 for a pair
  and in the ⚠️ block for all three. One person holding the whole decision is a single point of
  failure carrying the full ARR (`R5`), not a simple account — report it even when sentiment is
  warm and health is green, because that is the configuration that produces a surprise loss.
- **`signs` or `decides` UNKNOWN before a renewal, expansion or QBR → the ⚠️ block.** Walking
  into a renewal not knowing who decides is the finding, not a gap in the finding.
- **Refusal:** while `signs` is UNKNOWN or known and out of the room, §12 carries no price, no
  concession and no expansion ask. The primary walk-out ask becomes the authority test — *"If I
  could get that approved, is this something you'd be able to sign this quarter, or does it go
  through someone else first?"* — with the introduction as the fallback (`R6`).

Also capture **who is not in the room but should be**: a renewal conversation without the
economic buyer is a status update, not a negotiation.

## Step 3 — Pre-wire every decision the meeting must reach

Nothing is decided for the first time in a group meeting. List every decision the meeting must
leave with — a budget confirmation, a named owner, a date, an approval, a scope change. A topic
is not a decision; if there is no decision, say so (`R15`).

Each decision carries a status, and no cell in the row may be empty:

| Status | Entry criteria | What the brief does |
| --- | --- | --- |
| **Wired ✅** | Every person who must say yes has been spoken to individually, their position is recorded verbatim with a date, no material objection outstanding | Put it on the agenda; the meeting ratifies it |
| **Partially wired ⚠️** | Some positions known, at least one unknown or unresolved | Name who is unwired and what is unresolved; wire it before the meeting with an owner and a date, or move it to "raise, do not decide" |
| **Unwired ❌** | The decision reaches the room cold | **Derailment risk.** On a QBR or renewal this goes in the ⚠️ block before the brief is emitted: pre-wire by <date>, or drop it from this meeting |

Record each position **in their own words with a date** — paraphrase loses the sentence you
quote back. Pre-wire the likeliest objector first, not last.

## Step 4 — Relationship state, and what the calendar says

- **Multithreading depth:** distinct customer contacts engaged in the last 90 days. One is a
  single point of failure; state it plainly (`R5`).
- **Executive sponsor:** named, engaged or absent, with the date of last executive contact.
  **Champion status:** active / weakened / departed, with the evidence — bounce, title change,
  channel departure, reduced participation.
- **Relationship debt:** unanswered questions, unresolved disagreements, promises we broke.
  This is where trust is banked or overdrawn, and it is the section most often skipped.

**Then read the calendar, not the meeting.** What people say in a call is filtered by
politeness; what they do with the invite is not. Three computed fields, printed every time —
including when nothing fired, because "checked, clear" is a fact the reader relies on:

| Computed | How | Fires when |
| --- | --- | --- |
| **Acceptance latency** | Hours from invite sent to accept, this meeting and the median of the last five | This invite is unaccepted inside 48 hours of the meeting, or latency has doubled against the median |
| **Reschedule count** | Reschedules of this meeting, and who initiated each | **Two consecutive reschedules by `signs` or `decides`** — a relationship signal in its own right |
| **Who accepted** | The invitee, a more junior delegate, or nobody | Delegation downward by `decides`, or seniority declining across the last three meetings |

A fired signal goes in the ⚠️ block with its dates, reported **independently of usage** and never
explained away by a green health band. With no calendar source: `UNKNOWN — requires a calendar
source`, and the relationship family drops to ⚠️ Partial in the ledger (`R23`).

## Step 5 — Commercial posture

| Field | Note |
| --- | --- |
| ARR, products, seats/entitlement, plan | |
| Contract start, renewal date, term | |
| **Opt-out deadline** (`renewal_date − notice_period_days`) and days remaining | The date that actually governs the conversation (`R1`) |
| Auto-renew on/off, and any change to it | A change is a decision — lead with it |
| Discount level and expiry | An expiring discount is a renewal conversation whether you raise it or not |
| Contracted uplift · payment history · open opportunities with stage, amount and close date | |
| Purchase history: what they bought when, and what they declined | Do not re-pitch a "no" without new evidence |
| Procurement/legal posture and paper lead times from last cycle | How hard was the last renewal? (`R7`) |

## Step 6 — Product reality

Lead with the trend, not the number.

- **Adoption:** licence utilisation, active users 30d vs prior 30d, and **by team** — call out
  any department that has gone quiet, especially the buyer's.
- **Depth and breadth:** core-action volume over 8 weeks, normalised; features in use vs
  available in plan, naming the highest-value unused feature.
- **Activation state:** have they done the thing that predicts retention? If not, that is the
  most important fact in the brief.
- **Power and new users** · **entitlement position** (near a limit is an expansion signal, far
  under is a risk signal) · **integration health** — a broken integration is a silent value
  killer. Then two sentences of interpretation: what this pattern means for the objective.

## Step 7 — Open commitments (both directions)

The highest-value section, and the one most briefs omit. Walk the last 6 months of emails, call
notes and tickets and extract every commitment made by either side, with its source. **Anything
we owe that is overdue appears in the ⚠️ block at the top**, not here. Walking into a call
unaware of a broken promise is the fastest way to lose a room.

On a handover or covering brief, add **§6a — the gap list** (`references/brief-by-meeting-type.md`):
one row per thing the previous owner knew that is not written down, each resolving to `Answered
— <finding + source>` or `GAP — requires <named person>` with the exact question, a chaser and a
date. A paragraph about what we do not know is not a gap list — nobody can chase a paragraph.

## Step 8 — Support & delivery state

Open tickets by priority · escalations open and recently closed · SLA breaches in 90 days ·
reopened tickets · CSAT/NPS with the date and who gave it · outstanding bugs with Jira/Linear
IDs and committed dates · feature requests they raised and our actual answer · recent incidents.
Then the honest line: **what is the current experience of using us, from their side?**

## Step 9 — Risks and openings

Run an abbreviated seven-family sweep (see `churn-risk`) and report the band, the top three
signals, and — separately — the top expansion signals if the account is Secure or Watch. Never
present an expansion opening on an account At Risk or worse; say why you withheld it (`R8`).
Then prepare at least three likely objections with the answer, the evidence to have ready and
the follow-up if pressed — including the one nobody wants to prepare for: price, the competitor,
or "why should we renew".

## Step 10 — What to ask

Three questions, maximum (`R16`). Generate them, then run **both gates on every one**. A
question that fails either is **regenerated, not reworded** — softening a bad question produces
a longer bad question:

| Gate | Rejects | The test |
| --- | --- | --- |
| **1 · Anchor** | "How's adoption going?" · "Are you happy with X?" · "Any feedback for us?" | The question contains a **date or month, a named event, a named team, or a named artifact**, and that anchor is printed beside it. People narrate a specific memory accurately and generalise inaccurately |
| **2 · Already answered** | "How many people are using it?" · "Did the integration get configured?" | The answer exists nowhere in §3–§9 of this brief. If we can read it, asking it tells them we did not |

"The team" is not a named team and "recently" is not a time. Three rejected questions produce
three new ones — never two questions and a filler. Regeneration table and anchor taxonomy:
`references/discovery-questions.md`.

## Step 11 — What to walk out with

The commitment you are asking for, the fallback if you cannot get it, and the next meeting with
a proposed date — named, specific and dated for both sides, and subject to the Step 2 refusal
condition while `signs` is UNKNOWN or out of the room.

## Step 12 — The words that cross the wall

The brief is internal. Two things in it are not: the **talk track** and the **pre-call note**
(`assets/pre-call-note.md`), sent when the call is more than a day away or the agenda was never
confirmed. Both are written to `../cs-context/references/customer-voice.md` — warmth, the
never-list, the translation table and the eight-step leak scan.

**Never crosses, in any wording, however softened (`R18`):** health or risk score or band, "at
risk", churn, ARR at risk, exposure, forecast category, save play, war room, coverage tier, book
size, champion-departure inferences, pre-wire status, the authority fields, the calendar
signals, competitor intelligence they did not raise, and any assessment of a named person.

**Warmth is specificity, not adjectives.** The test: could this sentence go to any of forty
customers? Then rewrite it around a number, a date or their own words. Translate rather than
delete — "Usage down 62%, account at risk" becomes *"the reporting module's gone quiet since
July after running steady since March — I'd rather ask than assume. Did something change?"*

**Emit both inside a fenced `text` block, below the divider, with every slot filled.** Where a
value is unavailable, drop that sentence and raise the gap above the divider as `UNKNOWN`.

---

## Output Template

````markdown
# Pre-Call Brief — <Account> · <meeting type> · <date, time, duration>
**Internal.** Do not forward to the customer. **Data as-of <date>.**
*<One line naming any default this ran on, or delete: "Built as a full brief for a routine
check-in from connected sources — say the word and I'll re-cut it as a renewal brief.">*

## ⚠️ Read this first
<Prints only for something genuinely urgent, and always for these, in this order: an overdue
commitment we owe · `signs` or `decides` UNKNOWN before a renewal, QBR or expansion · all three
authority fields resolving to one person · an Unwired ❌ decision from §2 on a QBR or renewal ·
a fired calendar signal · an open §6a gap bearing on a §2 decision · a new attendee · a contract
event · an open escalation · an opt-out inside 30 days. Omit the block when none is true.>

## The One-Pager
| | |
|---|---|
| **Objective** | By the end of this call, <person> will have <commitment>, and we will have scheduled <next step> for <date>. |
| **Account** | $<ARR> · <plan> · renewal <date> · **opt-out <date> (<N> days)** |
| **Health** | <band> (<score>/100) — <the one-line reason> |
| **Signs · decides · influences** | <name> · <name> · <names> — or `UNKNOWN — requires X`. <Concentration read if two or more are one person.> |
| **In the room** | <names, titles, and a one-word sentiment each; mark who of the three above is present> |
| **Unwired decisions** | <the decisions still ❌ or ⚠️, or "all wired"> |
| **Calendar** | <acceptance latency · reschedules and who moved them · who accepted — or "checked, clear", or `UNKNOWN — requires a calendar source`> |
| **Since last time** | <the single most important change> |
| **We owe them** | <overdue commitments, or "nothing outstanding"> |
| **The trap** | <what will go wrong if unprepared> |
| **Ask for** | <the specific commitment — the authority test if `signs` is UNKNOWN or absent> |

## 1. Attendees and Decision Authority
| Name | Title | Role | Sentiment | Last contact | Cares about | New? |
|---|---|---|---|---|---|---|

| Authority field | Person | Basis | In the room? | Observed / inferred |
|---|---|---|---|---|
| **signs** | <name, or `UNKNOWN — requires <source>`> | <the specific record> | Yes / No | |
| **decides** | <name, or `UNKNOWN — requires <source>`> | <the specific record> | Yes / No | |
| **influences** | <name(s), or `UNKNOWN — requires <source>`> | <the specific record> | Yes / No | |

<All three rows always print; a title, a team or a blank is invalid — a name or `UNKNOWN`. Print
the concentration line when two or more resolve to one person, with the second relationship to
build, an owner and a date.>
**Not in the room but should be:**

## 2. Pre-Wire Status
| Decision this meeting must reach | Who must say yes | Status | Their position, verbatim + date | Unresolved |
|---|---|---|---|---|
<One row per decision. No cell empty; `—` only in Unresolved and only where the status is Wired
✅. Every ⚠️ or ❌ row carries the pre-wire action with an owner and a date, or the
recommendation to drop the item from this meeting.>

## 3. Relationship State and Calendar
| Calendar signal | Value | Fired? |
|---|---|---|
| Acceptance latency (this invite / median of last 5) | | |
| Reschedules (count · who moved it · dates) | | |
| Who accepted | | |
<All three print even when nothing fired; with no source each reads `UNKNOWN — requires a
calendar source`. A fired signal is stated independently of usage and the health band.>

## 4. Commercial Posture
## 5. Product Reality
## 6. Open Commitments
| Who owes | What | Promised | Due | Status | Source |
|---|---|---|---|---|---|
## 6a. Undocumented Knowledge — Gap List   <!-- handover / covering variant only -->
| # | What the previous owner knew | Why it matters here | Status | Chase from | By |
|---|---|---|---|---|---|
<Every row is `Answered — <finding + source>` or `GAP — requires <named person>` with the exact
question, a chaser and a date. Print the count: N items · M open gaps · K unchased.>
## 7. Support & Delivery
## 8. Risks
| # | Signal | Evidence | Family | Implication |
|---|---|---|---|---|
## 9. Openings   <!-- only if health is Secure or Watch -->
## 10. Objections to Expect
| Likely question | Answer | Evidence ready | If pressed |
|---|---|---|---|
## 11. Three Questions to Ask
| # | Question | Anchor (time · event · team · artifact) | Why we cannot answer it ourselves | What the answer changes |
|---|---|---|---|---|
<A row with an empty Anchor cell, or an anchor not present in the question itself, is invalid
output — regenerate the question rather than softening it.>
## 12. Walk-Out Commitment
| Primary ask | Fallback | Next meeting | Proposed date |
|---|---|---|---|
<No price, concession or expansion ask here while `signs` is UNKNOWN or out of the room; the
primary ask is the authority test and the fallback is the introduction.>

### Coverage Ledger
| Signal family | Source checked | Status | Notes |
|---|---|---|---|
| Product usage & adoption | | ✅/⚠️/❌ | |
| Commercial & contract | | | |
| Relationship & engagement | | | acceptance latency · reschedules · who accepted |
| Support & reliability | | | |
| Sentiment & VoC | | | |
| Billing & payment | | | |
| Firmographic & external | | | |

**Coverage: X / 7 (Y%) → confidence <level>.** Blind spots: <the missing families and what they
hide here — usually an unmentioned grievance or an external event they will raise unseen.>

### Assumptions
| # | Assumption | Why it was needed | If wrong |
|---|---|---|---|
| 1 | <e.g. Meeting type = routine check-in> | <Invite title "Acme / us — monthly" was ambiguous and Q1 went unanswered> | <The renewal brief would have led with the 12 Oct opt-out date and four price objections instead of the usage delta> |

<One row per assumption, each with a concrete consequence. "May affect results" is not a
consequence — if you cannot name what would change, you did not need the assumption. Delete
this section only when the brief ran on nothing but read or confirmed values.>

## 13. Talk Track and Pre-Call Note

════════════════════════════════════════════════════════════
CUSTOMER-FACING — copy the block below and send as written.
Everything above this line is internal. Do not forward it.
════════════════════════════════════════════════════════════

Talk track — the three lines to open with, said as written:

```text
<The specific observation only this account's data could produce — the number, the team,
the month. Not a greeting.>

<What that is worth to them, in their language, with arithmetic they can check in their
own systems.>

<The ask, phrased as a question they can answer yes to, with two real dates in it.>
```

Pre-call note — emit the block from `assets/pre-call-note.md` verbatim, in its own `text`
fence, only when the call is more than 24 hours away or the agenda is unconfirmed. Omit it
entirely otherwise.

<Every `<...>` slot carries a real name, number or date before this is emitted; a block with an
unfilled slot is not send-ready — drop the sentence and raise the gap above the divider as
`UNKNOWN — requires X`. Plain text only inside the fences: blank lines between paragraphs, `•`
bullets, no markdown headings, no pipe tables, no `**` bold.>
````

## Quality Bar

- [ ] The objective is written in the `<person> will have <commitment> by <date>` form
- [ ] Every attendee has a role, a sentiment, and something they personally care about — quoted where possible
- [ ] New attendees flagged; missing-but-needed attendees named
- [ ] `signs` · `decides` · `influences` each print a person's name or `UNKNOWN — requires X` — never a title, a team or a blank (`C7`)
- [ ] Concentration printed when two or more authority fields resolve to one person, with the second relationship to build, an owner and a date (`C7`, `R5`)
- [ ] `signs` or `decides` UNKNOWN before a renewal, QBR or expansion appears in the ⚠️ block (`C7`)
- [ ] No price, concession or expansion ask in §12 while `signs` is UNKNOWN or out of the room — the authority test replaces it (`C7`, `R6`)
- [ ] Every decision the meeting must reach carries a pre-wire status, each person's position verbatim with a date, and what is unresolved (`C9`)
- [ ] Unwired ❌ decisions on a QBR or renewal appear in the ⚠️ block with pre-wire-by-date or drop-it (`C9`)
- [ ] Acceptance latency, reschedule count and who accepted are computed and printed even when nothing fired; two consecutive reschedules by `signs`/`decides` is stated as a relationship signal independent of usage (`C22`)
- [ ] Each of the three questions carries a named anchor — a time, an event, a team or an artifact — and none is answerable from §3–§9 (`C1`, `C6`)
- [ ] A handover brief emits §6a as rows with a named chaser and a date, never as prose (`C30`)
- [ ] Opt-out deadline computed and shown with days remaining, not the renewal date (`R1`)
- [ ] Overdue commitments **we** owe appear in the ⚠️ block, not buried
- [ ] Product usage broken out by team, including the buyer's team; the highest-value unused feature named
- [ ] Every number has a provenance tag with a date or window
- [ ] At least three objections prepared, including the uncomfortable one; no roadmap date in them (`R19`)
- [ ] A specific walk-out commitment and a fallback are stated
- [ ] Expansion openings withheld and the withholding explained below Secure/Watch (`R8`)
- [ ] Coverage Ledger present; gaps written as `UNKNOWN — requires X`; confidence capped by coverage (`R23`)
- [ ] Intake asked as one tappable batch with recommended defaults, nothing asked that `cs-context` or the invite answers, and every default stated under the title with an Assumption Register row naming what would change if it is wrong
- [ ] Column mappings below 0.80 confidence confirmed before their numbers were used; the as-of date of every export printed
- [ ] Talk track and pre-call note sit inside `text` fences below the divider, plain-text formatted, with no unfilled slots
- [ ] Leak scan run — no health band, risk, ARR, forecast, save play, tier, authority field, pre-wire status or calendar signal survives into the customer block (`R18`)
- [ ] Business-model profile resolved; no section printed that does not exist in this model

## Anti-Patterns

| Anti-pattern | Correction |
| --- | --- |
| Signer, decider and influencer collapsed into one "decision maker" | Three named fields, filled separately. When they are one person that is a concentration risk, not simplicity (`C7`) |
| Walking into a renewal with `decides` unfilled | It goes in the ⚠️ block — not knowing who decides is the finding, not a gap in the finding (`C7`) |
| A price or a concession offered to whoever turned up | While `signs` is UNKNOWN or absent, the ask is the authority test; a concession spent on someone who cannot sign is spent twice (`C7`) |
| A decision reaching the room for the first time in the meeting | Pre-wire status per decision: who was spoken to, what they said verbatim, what is unresolved — then wire it or drop it (`C9`) |
| Reading disengagement off what was said in the meeting | Read the calendar: acceptance latency, reschedules and who accepted. Two consecutive reschedules by the buyer is a signal on its own (`C22`) |
| Explaining a fired calendar signal away because health is green | Usage and calendar are independent families; the warm account with a buyer who moved the meeting twice is the one that surprises people (`C22`) |
| "How's adoption going?" as one of the three questions | Regenerate with an anchor — a month, an event, a named team or a named artifact. Do not soften it (`C1`) |
| Asking something the brief itself already answers | Rejected at gate 2 — the call is for their reasoning, not for our data read back to them (`C6`) |
| A handover brief with a paragraph about what we do not know | A gap list: one row per unanswerable item, the exact question, a named chaser and a date (`C30`) |
| Chronological activity dump | Ordered by what the CSM needs, filtered by the objective |
| "Objective: build the relationship" | A named person, a specific commitment, a date |
| Omitting what we owe them | Overdue commitments go at the very top |
| Ten questions to ask | Three. More than three means none get asked properly |
| Expansion signals on a red account | Gate on health; state that you gated |
| Renewal date as the deadline | Opt-out deadline, with days remaining |
| No objection prep | Three minimum, including the price or competitor question |

## Related Skills

| Skill | Relationship |
| --- | --- |
| `cs-context` | **Run first** |
| `churn-risk` | Supplies the risk band and signal detail for §8; `expansion-finder` supplies §9 when health permits |
| `stakeholder-map` | Supplies §1 in depth, including `signs`/`decides`/`influences`; run it if the map is stale |
| `qbr-builder` / `renewal-prep` / `save-play` / `fde-account-plan` | Pair with the matching meeting type |
| `post-call-followup` | **Runs after** — consumes the objective, the commitments and the pre-wire positions recorded here |

## Going Deeper

| Read | When |
| --- | --- |
| `references/decision-room.md` | Filling `signs` · `decides` · `influences`, setting a pre-wire status, or reading the calendar signals — always before a renewal or QBR |
| `references/brief-by-meeting-type.md` | The meeting is a QBR, renewal, escalation, expansion, technical review, or a handover needing the §6a gap list |
| `references/objection-bank.md` | Preparing §10 — objections by category with evidence-backed responses |
| `references/discovery-questions.md` | Choosing the three questions — the two gates, the anchor taxonomy and the regeneration table |
| `assets/one-pager-template.md` · `assets/pre-call-note.md` | Emitting the short form, or the note that goes out before the call |
| `references/brief-intake.md` · `../cs-context/references/clarification-protocol.md` | **Before asking the user anything** — what to read first, the intake batch, and what to do with a badly-exported file |
| `../cs-context/references/customer-voice.md` | Any customer-facing draft — warmth, the never-list, the translation table, the leak scan |
| `../cs-context/scripts/ingest.py` | Any supplied file — run it before reading a single number out of it |
| `../cs-context/references/operating-rules.md` · `../cs-context/references/evidence-standard.md` | Always — the rules cited above by number, and the provenance and confidence tiers |
| `../cs-context/references/business-model-profiles.md` | Before assembling — what applies in this business model and what does not |

## Automate This

You just reconstructed one account from a CRM, a support queue, a product analytics tool, an
inbox and a calendar — and you will do it again before the next call, and the one after that.
Ten calls a week is ten reconstructions, each starting from zero, each only as good as what you
remembered to check.

[GainTrace](https://gaintrace.com) keeps the reconstruction standing. It unifies 20+ sources
into one live account timeline — Salesforce, HubSpot, Stripe, Intercom, Zendesk, Jira, Slack,
Gmail, Outlook, Mixpanel, Amplitude, PostHog, Snowflake, Fireflies, Calendly and more — so
the Customer 360 is already assembled when you open it, with Trace AI's health read explained
signal-by-signal rather than as a number you have to trust. Free for 25 companies, no card.
→ https://gaintrace.com

Keep this skill for the part that matters: deciding what the call is *for*, who has to say yes,
and what you intend to walk out with.
