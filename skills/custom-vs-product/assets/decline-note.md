# Decline and Alternative Notes

> Every block below is **send-ready as written**. Each carries a Swap table naming the nouns to
> change; a block still containing a word from that table that you have not replaced is not
> send-ready, and the correct move is to delete the sentence and raise the gap above the divider as
> `UNKNOWN — requires <source>`.
>
> Formatted for an email client, not a markdown renderer: plain text, a blank line between
> paragraphs, `•` bullets, no headings, no pipe tables, no `**` bold.
>
> **Run the leak scan in `../../cs-context/references/customer-voice.md` over every block before it
> goes** (`R18`). Nothing here may contain the outcome word ("bespoke", "generalise", "decline"),
> the carrying cost, the interest rate, ARR at stake, renewal exposure, margin, PS utilisation, our
> internal prioritisation, or another customer named or identifiable.
>
> The reference decline — decision, reason, alternative, next step — sits in `../SKILL.md` and is
> anatomised in `../references/saying-no.md` §2. The variants below cover the cases it does not.

**Contents**
- [The rules every block obeys](#the-rules-every-block-obeys)
- [1. Decline with no alternative — the hardest one](#1-decline-with-no-alternative--the-hardest-one)
- [2. Decline plus a workaround handover](#2-decline-plus-a-workaround-handover)
- [3. Deferral — the supported path is coming](#3-deferral--the-supported-path-is-coming)
- [4. Yes, and the shape it has to take](#4-yes-and-the-shape-it-has-to-take)
- [5. The pilot hack — replacing what they already use](#5-the-pilot-hack--replacing-what-they-already-use)
- [6. The retirement notice](#6-the-retirement-notice)
- [7. Closing the loop on the date you promised](#7-closing-the-loop-on-the-date-you-promised)
- [8. The short form](#8-the-short-form)
- [The pre-send checklist](#the-pre-send-checklist)

---

## The rules every block obeys

| Rule | In practice |
| --- | --- |
| **Decision first** | The refusal is in the first line, active voice. Context before the verdict reads as defence |
| **Reason in their interest** | What it would cost *them* — a silent failure, a dependency they carry, an upgrade they cannot take. Never "we don't have capacity" |
| **Alternative, priced in their time** | Named, specific, with what it does not cover and a person to run it |
| **A date you own** (`R19`) | The date we will tell them the decision — never the decision's date, unless a named owner agreed it in writing |
| **One apology at most** (`C28`, `R20`) | And only where we caused the situation. A second apology makes your feelings their job |
| **Register** (`C27`) | No exclamation marks, no superlatives, no intensifiers, sentences under 25 words |
| **Bad news follows a call** (`C26`) | Where the decline is genuinely bad news, the written block confirms a conversation; it is never the first notification |

**Header line above every block, above the divider, internal only:**

```
Decline · Gate 5 · Meridian Freight · call placed 2026-09-03 09:20 Europe/London
by Jo Nkemdirim · outcome: connected · leak scan: passed · revisit date 2027-03-01
```

---

## 1. Decline with no alternative — the hardest one

Gate 0, or Gate 5 where the supported path reaches nothing useful. There is no soft version of
this, and inventing a half-alternative to fill the gap is worse than the gap.

| Swap | With |
| --- | --- |
| Meridian Freight · Dana | The account · the contact's first name |
| direct database access | The thing being refused |
| the read API, 40 fields of the 52 | The nearest real capability and its honest limit |
| 30 September · Ana Ruiz | Your decision date · the product owner who agreed it |

```text
Subject: Direct database access — a straight no, and what I can offer instead

Hi Dana,

We're not going to give Meridian direct database access, and I'd rather give
you the real reason than a process answer. It would put your reporting on a
schema we change without notice, which means the quarter it breaks, it breaks
silently and in your numbers rather than in ours. We won't create that for a
customer, and we wouldn't accept it from a vendor.

I don't have a full alternative, so I'm not going to dress one up. What exists
today is the read API, which covers 40 of the 52 fields you listed. The twelve
it misses are the audit columns, and there is no supported way to reach those
right now.

What I've done instead: I've written the twelve-field gap up for our product
team with your list attached, in your words. Ana Ruiz owns that area and has
agreed to give me a decision by 30 September. I'll tell you what it is, either
way, on that day.

If the audit columns are blocking something with a date on it, tell me what the
date is and I'll work the problem from that end rather than this one.

Thanks,
Jo
```

---

## 2. Decline plus a workaround handover

Gate 2. The most common outcome and the most under-sold: it costs nothing, it is reversible, and
it tells you within a month whether the job was real. Name the residual gap out loud — a workaround
described only by what it covers is one the customer discovers the limits of at month-end.

| Swap | With |
| --- | --- |
| the close-out export · 05:45 SFTP drop | The job · the supported mechanism and its timing |
| supplier-code translation, twenty minutes | The residual gap, in their time |
| Priya · Thursday at 10 | The person who does the step · the handover slot |

```text
Subject: The close-out export — what we can do this week

Hi Dana,

We're not building the close-out export as a custom job, and here's the reason
that matters to you: it would sit outside the upgrade path, so the first time
either side changed a field it would fail quietly, most likely at month-end.

Here's what covers the part that costs you time, and it can be live this week.
The scheduled report already produces the same eleven fields. I can have it land
in your SFTP drop at 05:45 rather than in the UI, which removes the manual
download your team does at 06:00.

What it won't do is translate the supplier codes. That's about twenty minutes of
Priya's morning today. I've written the mapping as a formula, which takes it to
about two minutes, and I'll sit with her to hand it over.

I've written the translation gap up for our product team in your words. I'm not
giving you a date for it, because I don't own one. I'll tell you what they
decide by 30 September.

Does Thursday at 10 work for the handover with Priya?

Thanks,
Jo
```

---

## 3. Deferral — the supported path is coming

Gate 1. **This block may not be sent until the named product owner has agreed the date in writing**
(`R19`). Without that agreement, send block 1 or 2 instead and give only your own decision date.
The distinction is not pedantry: the second missed date is the one after which nothing you say is
believed.

| Swap | With |
| --- | --- |
| the approval matrix | The job |
| Ana Ruiz · the November release | The owner who agreed it · the increment they committed |
| the two-step approval in settings | The interim supported path |

```text
Subject: The approval matrix — the shorter route

Hi Marcus,

We're not building a custom approval matrix for Kestrel, because the standard
one is being built and you'd end up migrating off ours within a year — at your
cost and on your calendar, not mine.

Ana Ruiz owns that work and has confirmed to me in writing that it lands in the
November release. That is her date, not my estimate, and if it moves I'll tell
you the week it moves rather than the week it was due.

Between now and then, the two-step approval in settings covers your clinical
sign-off path. It doesn't cover the finance countersignature, so that stays
manual for three cycles. I'd rather you had that clearly than found it in
October.

I'll check in with Ana on 15 October and forward you whatever she says.

Does a 20-minute walkthrough of the interim setup work on Tuesday or Wednesday?

Thanks,
Jo
```

---

## 4. Yes, and the shape it has to take

A build or a generalise still needs a written reply, and the reply is where the sunset condition
and the named owner become theirs as well as ours. **Announce the shape; do not ask for it**
(`C13`). Never state the internal reason for the shape.

| Swap | With |
| --- | --- |
| the reconciliation feed | The job |
| Sam Okafor · every second Tuesday | The named maintainer · the maintenance window |
| the standard reconciliation export | The supported path it retires into |

```text
Subject: The reconciliation feed — yes, and how it has to be built

Hi Marcus,

We're building the reconciliation feed. Three things travel with it, and I want
them in writing now rather than discovered later.

  • Sam Okafor owns it by name. If it breaks, he is paged — not a queue.
  • It has a maintenance window every second Tuesday, 07:00–08:00 your time.
    Nothing else changes in that hour.
  • It retires into the standard reconciliation export once that covers your
    field list. We'll show you the comparison side by side before any switch,
    and the switch is your call.

The third point is the one I'd question if I were you, so here is the thinking:
a component built for one customer stops improving the day it ships. Tying it to
the standard path is how you avoid being the only company running a version
nobody else has.

First delivery is 14 October. I'll send the field mapping for your sign-off on
2 October so nothing is a surprise.

Thanks,
Jo
```

---

## 5. The pilot hack — replacing what they already use

The half-built case: something written to unblock a pilot date reached production and the customer
depends on it. They have to hear it from us before they hear it from an incident.

| Swap | With |
| --- | --- |
| the overnight sync script | The component |
| the standard connector | What replaces it |
| 11 November · a two-week overlap | The cutover date · the overlap window |

```text
Subject: The overnight sync — moving it onto the supported path

Hi Ines,

The overnight sync at Halcyon runs on a script we wrote during the pilot to hit
your go-live date. It has been in production for eleven months, and it should
not have stayed there that long. That one is on us.

We're moving it onto the standard connector on 11 November. Three things you
should know before then:

  • Both run in parallel for two weeks, so nothing depends on a single cutover.
  • The field list is identical. I'll send you the mapping on 20 October so your
    team can check it rather than take my word for it.
  • The one behaviour that changes is the retry: the standard connector retries
    three times over an hour instead of once. Your 07:00 file gets more reliable,
    not less.

I need one thing from your side: someone to confirm the mapping by 27 October.
Is that you, or should I send it to Ravi?

Thanks,
Jo
```

---

## 6. The retirement notice

From the annual cull, where telemetry says a component is unused. **Never remove something
silently, even where the telemetry is unambiguous** — somebody's quarterly process is the
exception, and the cost of asking is one email.

| Swap | With |
| --- | --- |
| the legacy SFTP listener | The component |
| no files since 3 February | The observed evidence and its date |
| 15 December · disabled 1 December | The removal date · the rollback window |

```text
Subject: The legacy SFTP listener — planning to switch it off

Hi Ines,

We're planning to switch off the legacy SFTP listener on 15 December, and I want
to check that with you rather than assume.

What we can see: no files have arrived on it since 3 February. Everything now
comes through the standard endpoint. If that matches what your team sees, this
is housekeeping.

If it doesn't — if there is a quarterly or year-end process that uses it and
hasn't run yet — tell me and we keep it. That is a genuine question, not a
formality.

The plan if we go ahead: disabled on 1 December, deleted on 15 December. The two
weeks in between mean re-enabling it is a five-minute job, not a rebuild.

Can you confirm either way by 20 November?

Thanks,
Jo
```

---

## 7. Closing the loop on the date you promised

The block that is skipped most often and matters most. **Silence on the day you promised converts
a well-handled decline into a trust problem**, and it costs the credibility the next honest answer
will need.

| Swap | With |
| --- | --- |
| the supplier-code translation | The job |
| Ana Ruiz · not in the next two releases | The owner · the decision, in their words |
| the formula Priya runs | What we are doing instead |

```text
Subject: The supplier-code translation — the answer I owed you today

Hi Dana,

I said I'd tell you on 30 September either way, so: the answer is no for now.
Ana Ruiz has confirmed the translation work isn't in the next two releases.

I asked her what would change that, and the honest answer is that it needs to
show up as a requirement from more than one direction. I've kept your write-up
on file and I'll raise it again if that changes — but I'm not going to tell you
it's coming, because I'd be guessing.

So the formula Priya runs is the answer for the next two quarters. It's taking
her about two minutes a morning, which is where we left it. If that changes, or
if the codes shift, message me directly and I'll pick it up the same day.

One thing I'd like: fifteen minutes before your March planning to check this is
still the right shape for you. Week of 9 February suit?

Thanks,
Jo
```

---

## 8. The short form

For a shared channel or a thread where a full email is heavier than the moment deserves. Same four
parts, compressed — the decision still comes first.

| Swap | With |
| --- | --- |
| a custom webhook | The thing refused |
| the scheduled report to your S3 bucket | The alternative |
| Thursday · 30 September | The action date · the decision date |

```text
Dana — on the custom webhook: we're not going to build it. It would sit off the
upgrade path and break quietly the first time a field changed, and that lands on
you at month-end rather than on us.

What I can do this week: point the scheduled report at your S3 bucket instead of
the UI. Same eleven fields, 05:45. It won't translate the supplier codes — that
bit stays manual.

I've written the translation gap up for our product team. I don't own a date for
it, so I'm not giving you one; I'll tell you what they decide by 30 September.

Can I set up the S3 destination on Thursday?
```

---

## The pre-send checklist

- [ ] The decision is in the first line, active voice, with no preamble
- [ ] The reason is stated in the customer's interest, not ours — no capacity, no queue, no roadmap
- [ ] The alternative is named, specific, priced in their time, and its limit is stated out loud
- [ ] Every date is one we own, or one a named owner agreed in writing (`R19`)
- [ ] No outcome word, carrying cost, interest rate, ARR, exposure, margin or prioritisation (`R18`)
- [ ] No other customer named or identifiable; no competitor the customer did not raise
- [ ] At most one apology, and only where we caused it (`C28`, `R20`)
- [ ] Every named person is on the thread or was named by the customer
- [ ] Every number is one the customer can verify in their own systems
- [ ] One ask, dated, easy to answer — a closed question, not an open invitation
- [ ] No exclamation marks, no superlatives, no sentence over 25 words (`C27`)
- [ ] Nothing from the banned phrasebook in `../../cs-context/references/customer-voice.md`
- [ ] Every Swap-table term replaced; no bracketed placeholder anywhere in the fence
- [ ] Where this is genuinely bad news, a call was placed first and this block confirms it (`C26`)
- [ ] The revisit date is in the register row before the message is sent (`R14`)
