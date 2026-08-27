# Practitioner Craft

> The tacit layer. What gets taught in expensive rooms — negotiation training, executive
> coaching, Challenger and MEDDPICC workshops, the things a senior CSM learns from losing a
> $2M account and never forgets — and almost never appears in written CS content.
>
> **This file is not for reciting.** Nothing here should be quoted in an output. Every entry
> exists to be *implemented as a mechanism* — a required field, a forced ordering, a template
> slot that cannot be left empty, a refusal condition. Craft that lives in prose gets skipped
> under time pressure. Craft that lives in a template gets performed.
>
> Each entry is: **the principle** · **why it is true** · **the mechanism that forces it**.

**Contents**
- [Discovery and conversation](#discovery-and-conversation)
- [Political reading](#political-reading)
- [Commercial craft](#commercial-craft)
- [Value and the internal sell](#value-and-the-internal-sell)
- [Risk reading](#risk-reading)
- [Delivering hard things](#delivering-hard-things)
- [Operating discipline](#operating-discipline)
- [Implementation index](#implementation-index)

---

## Discovery and conversation

### C1 · Ask about the last time, never about "generally"
People narrate a specific memory accurately and generalise inaccurately. "How's adoption going?"
gets a social answer; "walk me through the last time this got in your way" gets a fact.

**Mechanism** — `pre-call-brief` §10 and `../../pre-call-brief/references/discovery-questions.md` reject any question
in the form *how is X going / are you happy with X / any feedback*. Every generated question
must contain a specific anchor: a time, an event, a named team, or a named artifact.

### C2 · The third answer is the real one
The first answer is rehearsed, the second is considered, the third is true. "And what else?"
asked twice is the highest-yield sequence in discovery.

**Mechanism** — question sets carry a follow-up column, not just questions. `post-call-followup`
grades a discovery answer as thin when only one exchange occurred on the account's central
issue, and surfaces it as an open question rather than a finding.

### C3 · Say the number, then stop talking
The instinct after stating a price, a date or a hard fact is to soften it. Softening invites
negotiation against yourself. The silence does the work.

**Mechanism** — `renewal-negotiation` and `exec-escalation-comms` templates put the number as
the final sentence of its paragraph. Justification precedes the number, never follows it. The
leak scan flags any hedging clause appearing after a price or a date in the same paragraph.

### C4 · Label the emotion before answering the content
"It sounds like the rollout pace is the thing that's actually frustrating." Naming the state
lowers it; arguing the facts raises it. This is why escalations that open with an explanation go
badly and ones that open with an acknowledgement do not.

**Mechanism** — every difficult-conversation template opens with an acknowledgement slot that
precedes the substance slot, and the acknowledgement must restate the customer's own words.
A draft that opens with context or explanation fails the pre-send checklist.

### C5 · Get them to say the number
An ROI figure you assert is a vendor claim. The same figure in the customer's own words is
internal evidence they will repeat in a budget meeting you are not in.

**Mechanism** — `value-case` and `qbr-builder` carry a **Customer-stated** column beside every
benefit line, with the quote, the speaker and the date. A benefit with no customer-stated form
is marked *vendor-asserted* and may not lead the artifact.

### C6 · Never ask a question you already know the answer to
It signals you did not read your own systems, and it wastes the one thing a call gives you that
data cannot — their reasoning.

**Mechanism** — the clarification protocol's "never ask what you can read" table, extended into
every discovery question set: a question is rejected if the answer exists in the account data.

---

## Political reading

### C7 · Signer, decider and influencer are three people
The person who signs is often not the person who decides, and neither may be the person whose
opinion actually moves the decision. Treating them as one is how a renewal is lost after a
positive call with the wrong person.

**Mechanism** — `stakeholder-map` and `pre-call-brief` carry three separate named fields:
`signs` · `decides` · `influences`. When they resolve to one person, that is flagged as a
concentration risk, not a simplicity. When any is `UNKNOWN`, it appears in the brief's warning
block, because walking into a renewal without knowing who decides is the finding.

### C8 · The mobiliser beats the champion
The most enthusiastic contact is frequently not the one who can build internal consensus. The
person who can is often more skeptical, more senior, and less pleasant to deal with.

**Mechanism** — `stakeholder-map` scores **internal mobilising capacity** separately from
sentiment: has this person moved a decision through their org before, do others cite them, do
they control budget or headcount. A high-sentiment contact with low mobilising capacity is
labelled a *supporter*, not a champion, and does not satisfy the champion requirement anywhere
in the library.

### C9 · Pre-wire every decision
Nothing should be decided for the first time in a group meeting. Every attendee's position is
known beforehand, and the meeting ratifies rather than debates.

**Mechanism** — `qbr-builder` and `pre-call-brief` require a **pre-wire status** per decision:
who has been spoken to, what they said, what remains unresolved. A QBR carrying an unwired
decision is flagged as at risk of derailment before it is generated, and the recommendation is
to pre-wire or drop the item.

### C10 · Never let procurement become your only live thread
Once the conversation is exclusively commercial, price is the only remaining variable.

**Mechanism** — `renewal-negotiation` tracks days since the last *business* (non-commercial)
conversation. Past 21 days with procurement active, the artifact raises re-opening a business
thread as a required action before any concession is discussed.

### C11 · Find the blocker early and engage, do not route around
An unaddressed detractor surfaces at the worst possible moment, usually in the approval step.

**Mechanism** — `stakeholder-map` requires an explicit disposition for every negative
stakeholder — *convert · contain · bypass* — with the risk of each stated. "Unknown" is not an
allowed disposition on an account inside its renewal window.

---

## Commercial craft

### C12 · Never concede without trading
A concession given freely resets the baseline and teaches the customer that asking works. Every
concession buys something: term, volume, timing, a reference, a case study, payment terms, an
expansion commitment.

**Mechanism** — the concession ladder table has a **What we get** column that **cannot be
empty**. `renewal-negotiation` refuses to output a concession row without a paired ask, and the
validator treats an empty cell in that column as an error, not a gap.

### C13 · Announce the uplift, do not ask for it
Price increases communicated as a decision with a rationale land. The same increase framed as a
request invites a counter before the conversation starts.

**Mechanism** — the uplift communication template is declarative. Any interrogative
construction in the price paragraph ("would you be open to", "how do you feel about", "is there
room for") fails the pre-send scan.

### C14 · Test authority before conceding
"If I could get that approved, is this something you could sign this quarter?" A concession
given to someone without signing authority is spent twice.

**Mechanism** — `renewal-negotiation` gates the concession ladder on `signs` being known and
present in the conversation. Where it is not, the recommended next action is the authority test,
not the concession.

### C15 · A verbal yes is not a yes until paper moves
The gap between agreement and signature is where renewals die — legal, security, procurement,
PO issuance, vendor onboarding.

**Mechanism** — `renewal-prep` will not place a renewal in Commit on verbal agreement alone.
The forecast category rubric requires an observable paper-process event. `renewal-forecast`
carries the same entry criteria.

### C16 · The real competitor is no-decision
Most renewals are not lost to a rival; they are lost to inertia, a reorg, a budget freeze or a
deprioritisation. Competitive positioning against a named rival is often solving the wrong problem.

**Mechanism** — the loss-reason taxonomy in `churn-postmortem` treats *no decision / deprioritised
/ budget removed* as first-class causes with their own root-cause branches, and the renewal risk
register scores decision-process risk separately from competitive risk.

---

## Value and the internal sell

### C17 · The real deliverable is your champion's internal business case
CSMs who win renewals write the justification their champion presents to their own finance
team. The artifact that matters is the one you never attend the meeting for.

**Mechanism** — `qbr-builder` and `value-case` emit a **champion's internal one-pager** as a
distinct artifact, in the champion's voice, framed for their internal audience — not a copy of
our deck. It carries their objective, their number, and the ask in their words.

### C18 · Never present value you did not agree to measure in advance
Retrospective metrics look chosen. A number agreed at kickoff and reported at renewal is evidence.

**Mechanism** — `success-plan` requires a baseline with a source and a date before a goal may be
written, and `qbr-builder` marks any benefit line lacking a pre-agreed baseline as
*retrospective — weaker evidence*, ordered below agreed metrics.

### C19 · One number, not twelve
A dashboard invites debate about which metric matters. A single number, chosen with them,
carries a decision.

**Mechanism** — the QBR value section permits **one headline number**. Supporting metrics live
in an appendix. A deck with a metrics wall in the value slot fails the quality bar.

### C20 · Give the champion a win to carry
People advocate internally for things that make them look good. A champion needs something to
present as their own success.

**Mechanism** — the internal one-pager (C17) has a required **credit** slot naming what the
champion's team achieved, framed as their result rather than the product's.

---

## Risk reading

### C21 · Silence is louder than complaint
A customer who stops raising issues has usually stopped expecting resolution. Rising complaint
is engagement; the collapse afterwards is the signal.

**Mechanism** — implemented as the *Quiet quit* compound pattern and the U-shaped support
sub-score, where zero tickets scores as risk rather than health.

### C22 · Watch the calendar, not the meeting
Acceptance latency, reschedule count and who accepts predict disengagement earlier and more
reliably than anything said in the meeting itself.

**Mechanism** — `interaction` carries acceptance latency and reschedule count. Two consecutive
reschedules by the economic buyer fires a relationship signal independent of usage. `pre-call-brief`
surfaces the reschedule history in the warning block.

### C23 · The renewal is decided in months two to four
First-year outcomes are set during onboarding, not during the renewal conversation. A renewal
plan starting at T-90 on a failed implementation is negotiating from a position already lost.

**Mechanism** — `onboarding-plan` opens the risk record at the value gate rather than at go-live,
and the *Failed launch* pattern in `churn-risk` carries a 180–365 day lead time so it fires
during onboarding rather than at renewal.

### C24 · The customer who negotiates hardest is engaged; the one who does not is the risk
A quiet, agreeable renewal from a disengaged account is more dangerous than a difficult one.

**Mechanism** — `churn-risk` scores *frictionless renewal on a low-engagement account* as a risk
combination rather than a clean outcome; `renewal-forecast` requires evidence of engagement
before Commit, not merely absence of objection.

### C25 · Never let the renewal be the year's first commercial conversation
Raising commercial terms cold, inside the notice window, converts a relationship conversation
into a negotiation.

**Mechanism** — `renewal-prep`'s T-180 gate requires a commercial touch on record. Where none
exists, the plan inserts one before T-120 as a prerequisite, and R11 (value first, ask second)
prevents attaching it to bad news.

---

## Delivering hard things

### C26 · Bad news by voice, early in the week, early in the day
Email removes tone and gives the reader time to escalate before you can respond. Friday
afternoon news compounds over a weekend with no one available.

**Mechanism** — `exec-escalation-comms` and `save-play` recommend channel and timing explicitly,
and any written artifact for genuinely bad news is generated as a *follow-up to a call*, never
as the first notification.

### C27 · Regulate down, do not match
Matching an angry customer's energy escalates. The lower register de-escalates and signals control.

**Mechanism** — the difficult-conversation register bans exclamation marks, superlatives and
enthusiasm; the customer-voice checklist requires plain full stops and short sentences in any
draft where sentiment is negative.

### C28 · Apologise once
A second apology asks the customer to absolve you, which makes your feelings their problem.

**Mechanism** — implemented as R20; the pre-send scan flags a second apology construction in the
same message.

### C29 · Lead with the miss
Opening with good news when the quarter went badly tells the customer you did not notice.

**Mechanism** — `qbr-builder` orders "what went wrong" before "what went well", and the deck
outline refuses to generate without a populated shortfall slide when any success-plan milestone
was missed.

---

## Operating discipline

### C30 · Nothing lives in your head for more than two weeks
Undocumented context is lost at the first holiday, reorg or resignation, and it is exactly the
context nobody can reconstruct.

**Mechanism** — `post-call-followup` writes an internal note on every interaction; the handover
variant of `pre-call-brief` has an explicit "what the previous owner knew that is not written
down" section listing unanswerable items as gaps.

### C31 · Touch the top decile weekly regardless of health
Green accounts go red between reviews, and the largest ones do it most expensively.

**Mechanism** — `book-of-business-triage` reserves capacity for the top ARR decile before
allocating any remaining hours by risk, rather than allocating purely by score.

### C32 · Write down the accounts you chose not to work
An unwritten decision to skip is indistinguishable from an oversight and repeats silently.

**Mechanism** — R14; the "Not worked this cycle" table with reasons and revisit dates.

---

## Implementation index

Where each principle is enforced. A principle with no mechanism is not implemented — it is
decoration, and it belongs in this column as a gap.

| Skill | Enforces |
| --- | --- |
| `pre-call-brief` | C1 · C6 · C7 · C9 · C22 · C30 |
| `stakeholder-map` | C7 · C8 · C11 |
| `renewal-negotiation` | C3 · C10 · C12 · C13 · C14 |
| `renewal-prep` | C15 · C25 |
| `renewal-forecast` | C15 · C24 |
| `qbr-builder` | C5 · C9 · C17 · C18 · C19 · C20 · C29 |
| `value-case` | C5 · C17 · C18 |
| `success-plan` | C18 |
| `churn-risk` | C21 · C22 · C23 · C24 |
| `churn-postmortem` | C16 |
| `onboarding-plan` | C23 |
| `save-play` | C26 · C27 |
| `exec-escalation-comms` | C3 · C4 · C26 · C27 · C28 |
| `post-call-followup` | C2 · C30 |
| `book-of-business-triage` | C31 · C32 |
| `proactive-outreach` | C1 · C4 · C27 |
