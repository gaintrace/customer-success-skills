# Customer-Facing Blocks

> Every block below is send-ready as written once the `<...>` slots are filled with real names,
> numbers and dates. A block containing an unfilled slot is **not** send-ready — drop the sentence
> and raise the gap above the divider as `UNKNOWN — requires X`.
>
> Formatted for an email client, not a markdown renderer: plain text, a blank line between
> paragraphs, `•` bullets, no headings, no pipe tables, no `**` bold.
>
> **Run the leak scan in `../../cs-context/references/customer-voice.md` over every block before
> sending** (`R18`). Nothing here may contain a health score, risk band, ARR at risk, exposure,
> forecast category, the words "save play" or "war room", competitor intelligence they did not
> raise, or any assessment of a named person.
>
> Banned everywhere: "just checking in", "touching base", "circling back", "hope you're well",
> "as per my last email", "reaching out", "we value your partnership", "at your earliest
> convenience", "drive adoption", "leverage", "align", "ensure success". The test: could this
> sentence go to any of forty customers? Then rewrite it.

---

## The header every block carries

No block is emitted without this line above its fence. On a block classed `bad`, `Call placed`
and `outcome` have no valid empty value — the written block is the **follow-up to a call**, never
the first notification (`C26`). With no call on record, the voicemail line and the two-line
scheduling note in `../references/difficult-register.md` go out instead, and the withholding is
stated above the divider.

```
News class: bad · Register: regulated · Call placed 2026-09-01 09:40 Europe/London
by Priya Raman (VP CS) · outcome: connected
```

The call is placed in the computed slot — **Monday–Wednesday, 08:00–11:30 in the recipient's
timezone**, at least 12 hours out. Friday, any slot after 15:00 local, and the day before a
customer holiday are refused; a deviation is written with its compensating control.

`Register: regulated` is computed, not chosen: severity Critical, notice served, an escalation
live, the class `bad`, or a negative last inbound message. In that register a block carries **no
exclamation mark, no emoji, no superlative, no intensifier, no sentence over 25 words and at most
one apology** — a breach is regenerated, not softened (`C27`, `R20`). The rejection list, the
sentence arithmetic and 24 rewrites: `../references/difficult-register.md`.

---

## 1 · Commitment confirmation — within 24 hours of the war-room call

`News class: bad` (it carries a decline) · `Register: regulated` · `Call placed` = the war-room call itself; this block confirms only what was said on it.

Sent by the DRI to everyone who was in the room.

```text
Subject: <Account> — <the decision>, and who owes what

Hi <first name>,

<The one specific thing they told us was wrong, in their words.>

What we are committing to, with names and dates:

  • <owner> — <action> — <date>
  • <owner> — <action> — <date>

What I am not committing to: <the declined item>, and the nearest thing
we can actually do is <alternative>. I would rather say that now than
give you a date I cannot hold.

What I need from your side: <named person> — <action> — <date>.

I will come back to you on <date> whether or not it is finished.

<Name>
```

---

## 2 · Checkpoint update — every cadence interval, news or no news

`News class: neutral` — **`bad` the moment it reports a slip**, and then it follows a call. `Register: regulated` while the escalation is live.

Silence during a live problem does more damage than the problem. Send it on the day you said, even
when the answer is "no change".

```text
Subject: <Account> — <topic>, <date> update

<First name> — the weekly update, on time whether or not there is news.

Done since last week:
  • <owner> — <what shipped or completed> — <date>

Still open:
  • <owner> — <what> — now expected <date>. <One sentence on why it moved,
    if it moved.>

Nothing needed from you this week. <Or: the one thing, with a date.>

Next update <date>.

<Name>
```

---

## 3 · Named-owner remediation — the defect pattern note

`News class: bad` — it is an RCA on our own failure. `Register: regulated`. Call first; this goes within two hours of it.

For RC4. The highest-trust message a CSM can send, because it names a pattern support cannot see,
assigns a human, commits to a date, and asks for nothing.

```text
Subject: <Ticket pattern / the specific system>

<First name> — <N> tickets from your team since <date> (<ticket ids>).
Individually they look unrelated. They are not: they all trace back to
<the root cause, in plain language>.

What has changed: <engineer name> owns the root cause, targeting <date>.
<Workaround> holds until then, and I have briefed support so your team
does not have to re-explain it on every ticket.

I will come back to you on <date> whether or not it is fixed. Nothing
needed from you.

<Name> · <direct line>
```

---

## 4 · Successor introduction — from the VP CS, within 48 hours (RC6)

`News class: neutral` · `Register: plain`. No call precedes it — there is no relationship yet to call into.

No meeting request. The ask is information, and the agenda is handed to them.

```text
Subject: Introduction

<First name> — I run Customer Success at <company>. <Departed contact>
sponsored our work with <account> since <year>, so with the change I
wanted you to hear from me directly rather than find us in a renewal
notice.

Where things stand: <the one outcome metric, in their units, with the
period>. The next commercial date is <renewal date>.

I do not need a meeting. I need to know what you want this to deliver,
so we can re-point it. <CSM name> and I are both on this thread, and my
mobile is below.

<Name> · <direct line>
```

---

## 5 · Successor handover — from the CSM, two to four days later (RC6)

`News class: neutral` · `Register: plain`.

```text
Subject: <Account> handover

<First name> — following <VP name>'s note. I am the day-to-day.

Three things <departed contact> and I had in flight:

  • <item>
  • <item>
  • <item>

Two of them need a decision from someone in your seat before <date>.

I have written them up in one page — no pitch, just the decisions and
what happens if they slip. Want me to send it, or walk you through it in
twenty minutes?

<Name> · <direct line>
```

---

## 6 · Meeting request after notice or stated intent to cancel

`News class: bad` — it acknowledges notice. `Register: regulated` · `Call placed` required: the VP CS phones first and this follows within two hours.

Sent by the VP CS within two hours of the call, never as the first notification (`C26`). The
"including leaving as planned" option is what makes the meeting acceptable; a request that refuses to
accept the loss gets no meeting.

```text
Subject: <the contract end date, written plainly>

<First name> — I have your <date> notice, and the reason on record is
<their reason, in their words>.

I am not going to ask you to reconsider in an email. I am asking for 30
minutes to do two things: get the real reason on the record so we fix it
for the next customer, and put three options in front of you — including
leaving as planned, with us running the migration cleanly. If the answer
is still no after that, I will take it and run the offboarding properly.

<Two real date and time options.>

<Name> · <direct line>
```

---

## 7 · Offboarding plan — sent within five days of the confirmed decision

`News class: neutral` — the decision is already theirs. `Register: regulated`.

```text
Subject: <Account> offboarding — dates and your data

<First name> — here is how we will make leaving straightforward.

Your data:
  • Full export in <format>, delivered by <date> — everything your team
    created, including attachments, history and configuration
  • Schema documentation with it, so it loads somewhere else cleanly
  • Read-only access until <date>, after your subscription ends

Decommissioning, so nothing breaks quietly in your stack later:
  • <integration> disconnected — <owner> — <date>
  • <SSO / API keys / webhooks> — <owner> — <date>

Billing: final invoice <date>, covering through <date>. <Any credit or
proration, stated plainly.>

<Name on their side> — the only thing I need from you is confirmation
that the export opens and looks complete, by <date>.

<Name>
```

---

## 8 · The closing note — no pitch, a real door

`News class: neutral` · `Register: regulated`. It names our own miss, so every rejection rule applies and the single apology is spent here.

```text
Subject: Thank you

<First name> — <specific thing their team did well with us, named, with
the period>. That was genuinely good work and I would say so to anyone
who asked.

We did not get <the thing we got wrong> right, and I am not going to
dress that up. <One sentence on what changed internally because of it,
if something did.>

Everything is exported and the offboarding is closed out. If <the
specific thing that would have to change> ever changes, I will send you
one note and nothing else. And if you land somewhere new and want a
second opinion on anything, my number is below regardless of what you
are running.

<Name> · <direct line>
```

---

## 9 · Win-back — one note, at a real trigger

`News class: neutral` · `Register: regulated`. They left angry; the register does not reset because time passed.

Send once. Then honour the promise to stop.

```text
Subject: <the thing that changed, two or three words>

<First name> — you left in <month> because of <the reason, plainly>. I
am not going to pretend that was a misunderstanding; it was real.

<What changed> shipped on <date>. That specific thing is fixed.

No pitch and no meeting request. If it is relevant, reply and I will
send you a sandbox. If not, I will not send another one of these.

<Name>
```
