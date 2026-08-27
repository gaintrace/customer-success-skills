# The Decision Room

> Three readings the brief must make before it makes any other: **who has to say yes**,
> **whether they already have**, and **what their calendar has been doing about us**.
>
> All three are mechanical. None of them is a judgement call the writer gets to skip because
> the account felt healthy. Each has a field in the Output Template that has no valid empty
> value.

**Contents**
[Signs · decides · influences](#signs--decides--influences) · [Concentration](#concentration) ·
[When a field is UNKNOWN](#when-a-field-is-unknown) · [The authority test](#the-authority-test) ·
[Pre-wire status](#pre-wire-status) · [Running a pre-wire](#running-a-pre-wire) ·
[Calendar signals](#calendar-signals) · [Worked example](#worked-example)

---

## Signs · decides · influences

The person who signs is often not the person who decides, and neither is reliably the person
whose opinion moves the decision. A renewal lost after three positive calls is almost always a
renewal where those three were treated as one.

The role column in §1 (champion, admin, power user, procurement) is a *description of the
relationship*. It is not the authority read. Fill these three separately, by name.

| Field | The question it answers | Evidence that counts | Evidence that does not |
| --- | --- | --- | --- |
| `signs` | Whose signature goes on the order form, and who raises the PO | The signature block on the last executed contract · a delegation-of-authority threshold from procurement · "I'll sign it" in writing | A senior title · the person who signed three years ago · the person who forwards the DocuSign |
| `decides` | Who chooses whether the spend continues, and can kill it alone | Budget line ownership · a decision they already made on this line (an upgrade, a downgrade, a tool they cut) · procurement naming them as requester | Enthusiasm · meeting attendance · being our main contact |
| `influences` | Whose opinion moves `decides`, for or against | Cited by name in others' emails ("let me check with Dana") · attends their internal review · wrote the requirements · owns the team that would absorb the work of switching | Volume of contact with us · seniority alone |

Each field prints **a person's name**, or `UNKNOWN — requires <specific source>`. A title
(`"the VP of RevOps"`), a team (`"Finance"`), a blank cell, or `TBD` is invalid output — a name
is the thing that can be met, and everything else is a way of not answering.

`influences` may hold more than one name. `signs` and `decides` hold exactly one each; if two
names contend for either, the field is `UNKNOWN` plus both candidates, because "one of these
two" is not knowing.

**Sentiment travels with the name.** A `decides` who is neutral-to-negative is a different
account from a `decides` who is our champion, and the brief must say which.

---

## Concentration

Collapsing to one person is not a simple account. It is a single point of failure with a good
mood attached.

| Reading | What it means | What the brief does |
| --- | --- | --- |
| **Three names** | Normal. The decision has a structure and the structure is known. | Nothing extra. |
| **Two of three are the same person** | Partial concentration. Common and workable, but one departure removes two of the three. | Print `PARTIAL CONCENTRATION — <name> is both <field> and <field>` in §1 and name the second relationship to build, with a date. |
| **All three the same person** | `CONCENTRATION RISK`. One resignation, one reorg, one parental leave from zero decision path. `R5` puts the full ARR at risk until a second relationship exists. | Print it in the ⚠️ block. The walk-out ask includes an introduction to a second person on the decision path. |
| **All three UNKNOWN** | We have a relationship with users and no relationship with the decision. | ⚠️ block, and the meeting's objective is rewritten to be the authority mapping itself. |

Concentration is reported even when health is green and sentiment is warm. Especially then —
a warm single thread is the configuration that produces a surprise non-renewal.

---

## When a field is UNKNOWN

`UNKNOWN` is a legitimate output and a bad state. The brief marks it, prints where it would be
found, and — before a renewal, expansion or QBR — raises it into the ⚠️ block. Walking into a
renewal not knowing who decides **is** the finding; it is not a gap in the finding.

Look here before marking it, in this order:

1. **The last executed contract** — signature block, entity, title. Answers `signs` outright in
   most cases.
2. **The original opportunity record** — who was the economic buyer, who approved, what the
   approval chain was.
3. **Procurement's own words from the last cycle** — "this needs Dana's sign-off" is a
   verified `decides`.
4. **Reply-chain topology** — who gets added to a thread when money is mentioned, and who goes
   quiet when it is not.
5. **Their org chart, public filings, LinkedIn title changes** — weakest, and only ever
   `inferred`, never `observed`.

If all five are exhausted, print `UNKNOWN — requires <the specific source>`: *"UNKNOWN —
requires the executed 2025 order form (not in the CRM) or a direct question to Priya."*
Never substitute the most senior attendee.

---

## The authority test

A concession, a price, or an expansion ask spent on someone who cannot sign is spent twice —
once with them, and again with whoever actually decides, who now starts from the discounted
number.

**Refusal condition.** Where `signs` is `UNKNOWN`, or known and not in the room, the brief does
not put a price, a concession or an expansion ask in the walk-out slot. The primary ask becomes
the authority test:

> "If I could get that approved, is this something you'd be able to sign this quarter — or does
> it go through someone else first?"

It is one sentence, it is asked early rather than at the end, and it is answered by everyone
including people who do have authority. The fallback ask is the introduction: *"who else needs
to be comfortable with this before it's signed?"*

`R6` is the sibling rule at forecast level: no enterprise renewal enters Commit without an
executive-sponsor meeting in the last two quarters. A brief that cannot name `signs` is a brief
for a call that cannot advance a forecast category.

---

## Pre-wire status

**Nothing is decided for the first time in a group meeting.** A well-run meeting ratifies
positions that are already known; a badly-run one discovers them in front of an audience, where
disagreement is expensive to reverse because it was public.

A **decision** is anything the meeting must leave with that changes what someone does: a budget
confirmation, a named owner, a date, an approval, an escalation closed, a scope change. A topic
is not a decision. "Discuss the roadmap" is not a decision. If the meeting has no decision, say
so — that is `R15` territory and the meeting may not need to exist.

For every decision, the brief carries a status:

| Status | Entry criteria | What the brief does with it |
| --- | --- | --- |
| **Wired ✅** | Every person who must say yes has been spoken to individually, their position is recorded in their own words with a date, and no material objection is outstanding. | Put it on the agenda. The meeting ratifies it. |
| **Partially wired ⚠️** | Some positions known, at least one unknown or unresolved. | Name who is unwired and what is unresolved. Either wire it before the meeting — with a named owner and a date — or move the item to "raise, do not decide". |
| **Unwired ❌** | The decision reaches the room cold. | **Derailment risk.** On a QBR or renewal this goes in the ⚠️ block before the brief is emitted, with the recommendation: pre-wire it by <date>, or drop it from this meeting and take it separately. |

Every decision row prints four things and none may be empty: **the decision**, **who must say
yes**, **the status**, and **what is unresolved** (`—` only where the status is Wired).

An unwired decision is not made safe by being important. The two failure shapes are equally
common: the decision that gets refused in public and cannot be revisited for a quarter, and the
decision that gets nodded through by people who had not thought about it and unwinds by email
the following week.

---

## Running a pre-wire

Short, individual, and before the meeting. Not a meeting about the meeting.

| Step | The words |
| --- | --- |
| **State the decision** | "On Thursday I'm going to ask the group to agree the three Q4 measures." |
| **Ask their position, not their permission** | "Before I do — where do you land on that?" |
| **Surface the objection now** | "What would make you push back on it in the room?" |
| **Agree the public position** | "So on Thursday, you're comfortable if I present it as agreed?" |
| **Record it verbatim** | Their words, with the date, into §2. Paraphrase loses the sentence you will quote back. |

Pre-wire the person most likely to object **first**, not last. If they cannot be wired, the item
comes off the agenda; carrying it in anyway makes the objection an event rather than a
conversation.

---

## Calendar signals

Acceptance latency, reschedule count and who accepted predict disengagement earlier and more
reliably than anything said in the meeting itself. What people say in a call is filtered by
politeness. What they do with the invite is not.

| Computed field | How it is computed | Fires when | What it means |
| --- | --- | --- | --- |
| **Acceptance latency** | Hours from invite sent to accept, for this meeting and the median of the last five with this account | This invite is unaccepted inside 48 hours of the meeting, **or** latency has doubled against the median | The meeting is being kept as an option, not a commitment |
| **Reschedule count** | Reschedules of this meeting, and who initiated each | **Two consecutive reschedules by `signs` or `decides`** | A relationship signal in its own right, independent of usage. Their calendar is telling you the meeting has lost its place in the queue |
| **Who accepted** | Accepted by the invitee · delegated to a more junior attendee · nobody | Delegation downward by `decides`, or a declining seniority trend across the last three meetings | The account is being handed off internally before it is handed off to us |

Three rules govern how these are reported:

1. **They are printed every time**, including when nothing fired — "checked, clear" is a fact the
   reader needs to be able to rely on.
2. **A fired signal is never explained away by a green health band.** Usage and calendar are
   independent families; a healthy product footprint with a buyer who has moved the meeting twice
   is exactly the account that surprises people.
3. **No calendar source, no invention.** `UNKNOWN — requires a calendar source (Google Calendar,
   Outlook or a scheduling tool)`, and the relationship family in the Coverage Ledger drops to
   ⚠️ Partial, which caps confidence under `R23`.

Two reschedules by a practitioner is a busy practitioner. Two by the person who decides is the
signal. The distinction is why the fields are read against `signs` and `decides` by name rather
than against "the customer".

---

## Worked example

```
### 1. Attendees and Decision Authority

| Field | Person | Basis | In the room? | Confidence |
|---|---|---|---|---|
| **signs** | Dana Osei (CFO) | Signature block, executed order form 2025-02-11 [Salesforce · Contract.SignedBy · 2025-02-11] | No | Observed |
| **decides** | Dana Osei (CFO) | Owns the line; cut two tools in the Jan review [Gong · call 2026-01-19] | No | Observed |
| **influences** | Marcus Bell (VP Ops), Priya Raman (Head of Data) | Both cited by Dana in the Jan review; Marcus wrote the requirements | Yes (both) | Observed |

⚠️ **PARTIAL CONCENTRATION — Dana Osei is both signer and decider, and is not in the room.**
Second relationship to build on the decision path: Marcus Bell, by 12 Sept (owner: Jo).
```

```
### 2. Pre-Wire Status

| Decision | Who must say yes | Status | Their position, in their words | Unresolved |
|---|---|---|---|---|
| Three Q4 success measures | Marcus Bell | Wired ✅ | "Fine with those three, as long as the data one isn't on my team." [email · 2026-08-21] | — |
| Named owner per measure | Marcus Bell, Priya Raman | Partially wired ⚠️ | Marcus agreed. Priya not spoken to. | Whether Priya's team takes the data measure — the exact thing Marcus fenced off |
| Finance-team expansion scoping date | Dana Osei | Unwired ❌ | Not spoken to since 2026-01-19 | Everything. **Derailment risk** — pre-wire with Dana by 4 Sept or drop it from Thursday and take it separately |
```
