# The Difficult Register — voice first, and regulate down

> Read this **before drafting any customer-facing block classed `bad`**, and whenever the last
> inbound message from the customer was angry, curt or cold.
>
> Two mechanisms live here, and they fail together. The first decides **how and when** hard news
> reaches a person (`C26`). The second decides **what register** it is written in once it does
> (`C27`). Neither is a style preference. Both are enforced as rejection conditions in
> `../SKILL.md` Step 6, in the Quality Bar, and in the header every block carries above its fence.
>
> The reason they belong in one file: the moment a save play goes badly, the instinct is to write
> rather than call, and to write warmly rather than plainly. Both instincts are wrong, and they
> arrive at the same moment.

**Contents**
- [Part 1 — The voice-first gate (C26)](#part-1--the-voice-first-gate-c26)
  - [Classing the block](#classing-the-block)
  - [The gate](#the-gate)
  - [The slot arithmetic](#the-slot-arithmetic)
  - [Worked slots](#worked-slots)
  - [The call itself](#the-call-itself)
  - [Call outcomes and what each one emits](#call-outcomes-and-what-each-one-emits)
  - [The two blocks that exist before the call](#the-two-blocks-that-exist-before-the-call)
- [Part 2 — The regulated register (C27)](#part-2--the-regulated-register-c27)
  - [When the register is regulated](#when-the-register-is-regulated)
  - [The rejection list](#the-rejection-list)
  - [Sentence arithmetic](#sentence-arithmetic)
  - [Twenty-four rewrites](#twenty-four-rewrites)
  - [The anger script](#the-anger-script)
  - [A full before and after](#a-full-before-and-after)
- [The pre-emit check](#the-pre-emit-check)

---

# Part 1 — The voice-first gate (C26)

Email removes tone and hands the reader unlimited time to escalate before you can answer. A
decline read at 16:40 on a Friday is forwarded to their VP at 16:55, discussed without you all
weekend, and by Monday it is a position rather than a problem. The same sentence said on a
Tuesday morning call is a conversation, and the written version that follows it two hours later
is a record of something already understood.

## Classing the block

Every customer-facing block this skill emits is classed before it is drafted. The class is a
field, not a judgement made at send time.

| Class | What it covers | Delivery |
| --- | --- | --- |
| **`bad`** | A decline (`R19`) · a missed or slipped date · an RCA on our own failure · a refused concession · a price rise · acknowledging notice · confirming an exit · telling them a save has ended | Call first, always. The written block is the follow-up |
| **`neutral`** | A checkpoint update with no movement · a plan · an export · a scheduling note · a handover introduction | Email on the day promised |
| **`good`** | A commitment we can now make · a fix landed · a structure they asked for and got | Email; a call adds nothing they need |

Ambiguity resolves **upward**. A checkpoint update that reports a slip is `bad`, not `neutral`,
because the slip is the content and the update is the wrapper.

## The gate

**A `bad` block is not emitted until `Call placed` is filled.** The header above every fence
carries four fields, and three of them have no valid empty value on a `bad` block:

```
News class: bad · Register: regulated · Call placed 2026-09-01 09:40 Europe/London
by Priya Raman (VP CS) · outcome: connected
```

| Field | Valid values | Empty is allowed when |
| --- | --- | --- |
| `News class` | `bad` · `neutral` · `good` | Never |
| `Register` | `regulated` · `plain` | Never |
| `Call placed` | `<date> <HH:MM> <IANA timezone>` | Class is `neutral` or `good` |
| `outcome` | `connected` · `voicemail+SMS` · `no answer` · `refused` | Class is `neutral` or `good` |

With no call on record the skill emits the call script, the voicemail line and the two-line
scheduling note **instead of** the bad-news email, and states above the divider:

> **Written notification withheld (`C26`).** <Name> has not yet spoken to <contact>. The decline
> is delivered on the call at <slot>; the confirming block is generated within two hours of it.

This is a refusal, not a delay. A save play that emails a decline because the call was hard to
book has already spent the relationship it was trying to keep.

## The slot arithmetic

```
delivery_slot = earliest T such that
    weekday(T, recipient_tz)  ∈ {Mon, Tue, Wed}
    time(T, recipient_tz)     ∈ [08:00, 11:30]
    T                         ≥ now + 12h
    T                         ∉ customer_holiday ∪ (customer_holiday − 1 business day)
```

| Refused outright | Why |
| --- | --- |
| Any Friday | The news compounds over a weekend with nobody available to answer it |
| Any slot after 15:00 recipient-local | Their day ends before yours can respond to what it starts |
| The day before a customer holiday or their quarter close | You are handing them something they cannot act on and cannot forget |
| A calendar invite whose title names the subject | The title delivers the news before the caller does — title it `<Account> · <caller name>` |

**Thursday** is used only when `decision_runway` leaves no earlier legal slot. **Where no legal
slot exists inside the runway**, take the earliest available time and write the deviation into
the plan's `Rules deviated from` row with its compensating control, both of which are required:

1. The caller stays reachable until close of business in the recipient's timezone, and says so on
   the call: "I am at this number until six your time."
2. A second contact on the account is briefed the same day, so the news is not sitting with one
   person over a weekend.

**Timezone unknown** → write `UNKNOWN — requires the contact's timezone` and schedule to the
account HQ's business hours. Do not infer a timezone from an email signature's country code and
then treat the inference as observed.

## Worked slots

| Now (recipient-local) | Runway | Computed slot | Note |
| --- | --- | --- | --- |
| Thu 2026-09-03, 14:00 | 41 days | **Mon 2026-09-07, 08:00** | Friday refused; Monday morning is the first legal slot |
| Mon 2026-09-07, 09:00 | 31 days | **Tue 2026-09-08, 08:00** | Today's window closes inside the 12-hour minimum |
| Fri 2026-09-11, 10:00 | 4 days | **Fri 2026-09-11, 13:00** | Deviation: runway leaves no legal slot. Caller reachable to 18:00; second contact briefed today |
| Wed 2026-09-09, 07:00 | 60 days | **Wed 2026-09-09, 08:00** | Same day, legal window, 12-hour rule waived only because the slot is not sooner than the notice the recipient needs — record it |

The fourth row is the one people get wrong. The 12-hour minimum exists so the caller has prepared,
not so the customer is warned. Where the caller is already prepared and the news is already late,
the earlier slot is right and the shortened notice is written down.

## The call itself

Sixty seconds decide it. The order is fixed:

1. **Name the subject in the first sentence.** "I am calling about the 12 September date."
2. **Say the thing.** No preamble, no context, no explanation before the fact.
3. **Stop talking.** The silence is theirs to use, and interrupting it converts a fact into a
   negotiation with yourself (`C3`).
4. **Take the response before answering it.** Reflect their words back before responding to the
   content.
5. **One owner, one date, one next contact.** "Sam owns it. 12 October. I call you Thursday
   whether or not it has moved."

Never: open with "how are you", ask for the meeting before saying why, deliver it to voicemail
in full, or let the call end without a next contact date.

## Call outcomes and what each one emits

| Outcome | What is emitted, and when |
| --- | --- |
| **connected** | The confirming block, within 2 hours for Critical, same day otherwise. It confirms **only what was said on the call** — nothing new arrives in writing that the person did not hear first |
| **voicemail+SMS** | The voicemail line (below), then a two-line scheduling note. The full written news waits for a second attempt; two failed attempts inside 24 hours converts the note into the full block with the attempts logged |
| **no answer** | Second attempt at the next legal slot. After two, escalate the caller one level and try their mobile |
| **refused** — they decline the call | The full written block goes, in the regulated register, opening with the fact that they asked for it in writing |

## The two blocks that exist before the call

Neither contains the news. That is the point of them.

**Voicemail — say this, and nothing more:**

```text
<First name>, it is <name> from <company>, Tuesday morning. I need fifteen
minutes with you today about the 12 September date. I am at <number> until
six your time, and I will try you again at two if I have not heard back.
```

**The scheduling note — two lines, sent immediately after the voicemail:**

```text
Subject: Fifteen minutes today

<First name> — I left you a voicemail. I need fifteen minutes today about
the 12 September date, and I would rather say it to you than write it.

I am on <number> until six. If today is impossible, 08:30 or 09:15 tomorrow.

<Name>
```

Note what is absent: the news, an apology, an explanation, and any word that hints at the
content. A scheduling note that says "unfortunately we have some difficult news" has delivered
the news badly and forfeited the call.

---

# Part 2 — The regulated register (C27)

Matching an angry customer's energy escalates it. Dropping below it de-escalates and signals
control — the reader concludes the situation is held by someone who is not frightened of it.
Enthusiasm in a difficult thread reads as not having understood the situation, and an exclamation
mark reads as a person performing calm rather than possessing it.

## When the register is regulated

Computed, not chosen. `Register: regulated` whenever **any** of these is true:

- Severity is Critical, or notice has been served
- An escalation is live, or the play's class is `bad`
- The last inbound message from the customer is negative — a complaint, a refusal, a threat to
  leave, a demand for escalation, or a one-line reply to a long message
- We are apologising, declining, or reporting our own miss

Otherwise `Register: plain`. There is no third setting, and warmth is not the opposite of
regulated — the regulated register is warm through specificity, exactly as everything else in
`../../cs-context/references/customer-voice.md`.

## The rejection list

Mechanical. A draft that hits any of these is **regenerated, not softened** — softening leaves
the shape of the original visible, and the reader sees the edit.

| # | Rejected | Regenerate as |
| --- | --- | --- |
| 1 | Any `!` | A full stop |
| 2 | Any emoji | Nothing |
| 3 | "excited", "thrilled", "delighted", "amazing", "fantastic", "wonderful", "great news" | The verb, plain: "I will", "we are", "here is" |
| 4 | Intensifiers: very, really, hugely, incredibly, extremely, absolutely, massively, totally, super | Delete the adverb. The sentence is stronger without it |
| 5 | "happy to", "love to", "more than happy to" | "I will" |
| 6 | Any sentence over 25 words | Split at the first conjunction |
| 7 | A mean sentence length above 20 words | Split the three longest |
| 8 | A second apology for the same thing | One apology, then what changes (`R20`) |
| 9 | Opening with context, explanation or defence | Their own words back, then the fact (`C4`) |
| 10 | "unfortunately", "regrettably", "sadly" | Delete. The fact carries its own weight |
| 11 | "just", "simply", "quickly" as softeners | Delete |
| 12 | A question mark on anything that is not the single ask | Full stop |
| 13 | Hedges: "hopefully", "we think", "should be able to", "aiming to" | A date and an owner, or "I will not give you a date I cannot hold" (`R19`) |
| 14 | Any word from the banned phrasebook in `customer-voice.md` | Its replacement there |

## Sentence arithmetic

Short sentences are the mechanism, not the aesthetic. They are checkable:

- **Longest sentence ≤ 25 words.** One breach is one regeneration.
- **Mean ≤ 20 words** across the block.
- **First sentence ≤ 15 words.** It carries the subject and nothing else.
- **One clause per sentence** wherever the fact allows it. "The fix lands 12 October. Sam owns
  it." beats "Sam is now the owner and is targeting 12 October for the fix, which we believe is
  achievable."
- **Paragraphs ≤ 3 sentences.** A wall of text in a difficult thread reads as a defence.

## Twenty-four rewrites

| Matched (wrong) | Regulated (right) |
| --- | --- |
| "Thanks so much for your patience!" | "You have waited three weeks. Here is where it is." |
| "We're really excited to share an update!" | "An update on the 12 September date." |
| "I completely understand your frustration!" | "You said the third slip would decide this. This is the third slip." |
| "We're absolutely committed to making this right." | "Sam owns it. 12 October. I call you Thursday either way." |
| "Great news — we think we should be able to get this to you soon!" | "The fix lands 12 October." |
| "I'm so sorry, and again, I really do apologise for all of this." | "I am sorry. I will not say that again." |
| "Unfortunately we're not able to accommodate that at this time." | "We are not going to build that. The nearest thing we can do is <X>." |
| "Hopefully that helps!" | "Tell me if that does not cover it." |
| "We're working hard on it and hope to have news shortly." | "It is being worked. No date exists yet, and I will not invent one." |
| "That's a really great question!" | "I do not know. I will have the answer by Thursday." |
| "As you can appreciate, these things take time." | "It has taken eleven weeks. That is longer than we said." |
| "We value your partnership enormously." | "You pushed us on the audit log and you were right." |
| "I just wanted to quickly follow up on this!" | "Following up on the 12 September date." |
| "Let me know if you have any questions at all!" | "If 12 October is too late for your close, tell me on the call." |
| "We're thrilled to offer you a 15% discount." | "We can hold the price flat for two years. In return we need the signature by 14 October." |
| "Our team is super focused on this right now." | "Two engineers are on it. Sam is the one you email." |
| "I hope this finds you well!" | *(delete — start with the subject)* |
| "There may have been some miscommunication on our side." | "We told you 12 September and we did not deliver it." |
| "I'd love to jump on a quick call!" | "Fifteen minutes, Tuesday 08:30 or 09:15." |
| "We totally hear you and are absolutely on it." | "Understood. Here is what changes today." |
| "Rest assured this is our top priority!" | "It is the only thing Sam is working on this week." |
| "Apologies again for any inconvenience caused." | *(delete — the second apology)* |
| "We're confident you'll be delighted with the result." | "You will be able to check it yourself on 12 October. I will send the build number." |
| "Please don't hesitate to reach out!" | "I am on <number> until six your time." |

## The anger script

When the last inbound message is angry, the order is fixed and the register is regulated. Four
moves, in this order, and never a fifth:

1. **Mirror.** Their words, not yours. "You said this is the third time you have had to chase
   the same thing." Nothing else in the first paragraph.
2. **The fact.** One sentence, no explanation attached to it.
3. **What we own.** One apology maximum (`R20`, `C28`), then the owner and the date, or the plain
   statement that no date exists.
4. **One ask, small.** A time, or a yes/no. Not "let me know your thoughts".

Never: explain before mirroring, apologise twice, ask for anything commercial in the same message
(`R11`), or end with a question mark on anything except the ask.

## A full before and after

**Before — matched, enthusiastic, and it will make the account worse:**

```text
Hi Dana!

Thanks so much for your patience on this one — I know it's been a bit of a
journey! I wanted to reach out with a quick update: the team has been
working really hard and has made some great progress, and while we're not
quite there yet, we're absolutely confident we'll have something fantastic
for you very soon. I'm so sorry again for the delay, and I really do
apologise for any inconvenience this has caused.

In the meantime, I'd love to jump on a quick call to discuss next steps and
also touch on the renewal, which I know is coming up!

Let me know if you have any questions at all!
```

Nine breaches: three exclamation marks, four superlatives, two apologies, a 44-word sentence, a
hedge with no date, a commercial ask attached to an apology (`R11`), and a first line that says
nothing. It also arrived as the first notification, which is the `C26` breach that outranks all
of them.

**After — regulated, and sent within two hours of the call:**

```text
Subject: 12 September date

Dana — you said the third slip would decide this, and this is the third
slip. I am sorry.

The fix now lands 12 October. Sam Okafor owns it and is on it full time.
You will get the build number from me on the day it ships, and a call from
me every Thursday until then whether or not there is news.

I am not raising the renewal until this is closed.

If 12 October is too late for your close, say so and I will take it to our
VP Engineering this week.

Priya · <direct line>
```

Longest sentence: 24 words. Mean: 15. One apology. No exclamation marks, no superlatives, no
intensifiers. The renewal is explicitly deferred rather than attached (`R11`). Every commitment
has an owner and a date, and the one that does not exist is not invented (`R19`).

---

## The pre-emit check

Run before any block leaves the skill. A single failure regenerates the block.

- [ ] `News class` is set, and ambiguity resolved upward
- [ ] On a `bad` block, `Call placed` carries a date, a time, a timezone, a named caller and an outcome — or the block is withheld and the withholding is stated (`C26`)
- [ ] The slot is Monday–Wednesday, 08:00–11:30 recipient-local, ≥12 hours out
- [ ] No Friday, no post-15:00 slot, no day before a customer holiday — or the deviation is written with both compensating controls
- [ ] The calendar invite title does not name the subject
- [ ] `Register` is set, and `regulated` wherever the trigger conditions fire
- [ ] Zero `!`, zero emoji, zero superlatives, zero intensifiers
- [ ] Longest sentence ≤ 25 words; mean ≤ 20; first sentence ≤ 15
- [ ] Exactly one apology at most, and it is not the second one for this thing (`R20`)
- [ ] Opens with their words, not with context or defence
- [ ] No commercial ask anywhere in a block classed `bad` (`R11`)
- [ ] The leak scan in `../../cs-context/references/customer-voice.md` has been run (`R18`)
- [ ] No `<...>` slot left unfilled
