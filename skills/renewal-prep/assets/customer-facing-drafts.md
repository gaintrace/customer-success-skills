# Customer-Facing Drafts for a Renewal

> The three things in a renewal plan that a customer actually reads. Everything else in the
> plan — bands, ATR, forecast category, the register — is internal and stays internal.
>
> Read `../../cs-context/references/customer-voice.md` before editing any of these. The rules
> below are the renewal-specific application of it, not a replacement for it.

**Contents**
- [The three drafts and when each is due](#the-three-drafts-and-when-each-is-due)
- [The three binding rules](#the-three-binding-rules)
- [The renewal firewall — what never crosses](#the-renewal-firewall--what-never-crosses)
- [Draft 0 — Commercial-context conversation, when C25 fires (before T-120)](#draft-0--commercial-context-conversation-when-c25-fires-before-t-120)
- [Draft 1 — Courtesy notice-deadline letter (T-120, repeated T-90)](#draft-1--courtesy-notice-deadline-letter-t-120-repeated-t-90)
- [Draft 2 — Written-intent question (T-75)](#draft-2--written-intent-question-t-75)
- [Draft 3 — Bridge-extension request (T-7, or rescue)](#draft-3--bridge-extension-request-t-7-or-rescue)
- [Formatting rules inside the fence](#formatting-rules-inside-the-fence)
- [Pre-send checklist](#pre-send-checklist)

---

## The drafts and when each is due

| # | Draft | Due | Purpose | Never contains |
| --- | --- | --- | --- | --- |
| 0 | Commercial-context conversation *(only when C25 fires — no commercial touch on record in 12 months)* | Before T-120 | Stop the renewal being the year's first commercial conversation | A price, an uplift, a renewal date, or any attachment to an apology or a miss (R11) |
| 1 | Courtesy notice-deadline letter | T-120, repeated T-90 | Make sure the customer knows their own decision date before it passes | Any suggestion that we think they might leave |
| 2 | Written-intent question | T-75 | Get intent in writing, in their words, from the economic buyer | The forecast category the answer will set |
| 3 | Bridge-extension request | T-7, or on entry to rescue | Buy paper time at current terms without reopening price | That the paper path has negative slack because we started late |

One more artifact — the proposal itself — is produced by the commercial process, not by this
skill. This skill decides its date and its sequence (value at T-150/T-120, price at T-90) and
supplies the value evidence it rests on. Draft 0 is conditional: it exists only on accounts where
the T-180 gate found no commercial touch on record, and where it exists it is a **prerequisite**,
not an option — the T-120 price decision does not issue until it has been held.

## The three binding rules

Every word of every draft in this file is bound by three rules. They come from `../SKILL.md` Step 10
and they are not negotiable per-draft — a draft that breaks one of them is rewritten, not softened.

**1. Warmth is specificity, not adjectives.** Banned in every draft: "just checking in",
"touching base", "circling back", "hope you're well", "as per my last email", "reaching out",
"we value your partnership", "let me know your thoughts", "at your earliest convenience",
"drive adoption", "leverage". The test: could this sentence go to any of forty customers? Then
rewrite it around something only this account's data could produce — the number they validated,
the date they gave you, the words they used in the EBR. Adjectives are what a draft reaches for
when it has nothing specific to say; the fix is not a warmer adjective, it is a fact.

**2. The disclosure firewall (R18).** Health band, risk band or score, ATR, ARR at risk,
exposure, forecast category, readiness and MEDDPICC-R scores, paper-movement status, save play,
war room, coverage tier, champion-departure inferences, competitor intelligence and any
assessment of a named person **never** reach the customer in any wording, however softened. The
notice-deadline letter states a date and a clause; it never states why we care. The table in the
next section gives the translation for each item — what goes instead, rather than a blank.

**3. The copy block.** Every draft sits inside a fenced `text` block below the §12 divider,
formatted for an email client — plain text, blank lines between paragraphs, `•` bullets, no
markdown headings, no pipe tables, no `**` bold. **No unfilled placeholder inside the fence:** if
a name or date is unavailable, drop that sentence and raise `UNKNOWN — requires X` above the
divider. A block containing `[Name]` is not send-ready. Full formatting rules are below under
*Formatting rules inside the fence*.

## The renewal firewall — what never crosses

Renewal work generates more internal-only language per page than anything else in CS, and
every one of these has reached a customer somewhere:

| Internal | Why it can never be sent | What goes instead |
| --- | --- | --- |
| Health band, risk band, risk score | Tells the customer we were grading them and did not say so | Nothing. The observation underneath it, phrased as a question |
| ATR, ARR at risk, exposure, dollars at risk | Prices the relationship in our terms | The line items on the order form, which they can verify |
| Forecast category (Commit / Best Case / At Risk) | Our internal call on their decision | Nothing |
| Readiness score, MEDDPICC-R score | An assessment of them and of us | Nothing |
| Save play, war room, escalation tier | Reveals a machine they did not know existed | The specific thing being done, with a named owner and a date |
| "Champion", "economic buyer", "blocker", "single-threaded" | Assessments of named people | Their actual role and name |
| Champion-departure inferences ("we saw Jamie left") | An inference stated as fact | "Who's picking up the work Jamie was leading?" |
| Competitive intelligence they did not tell us | Reveals surveillance | "If you're looking at other options I'd rather be in that conversation than outside it" |
| Coverage tier, book size, tech-touch, pooled | Tells them what they are worth to us | Nothing |
| "Auto-renew is on so we're fine" | Wins a term the customer did not intend to buy | The decision date, plainly stated |

**The notice-deadline letter states a date and a clause. It never states why we care.** The
moment it explains our interest in the date, it becomes a retention email.

## Draft 0 — Commercial-context conversation, when C25 fires (before T-120)

**Due:** before T-120, and only when the T-180 gate found no commercial touch on record inside 12
months. **To:** the economic buyer or budget holder — never the champion as a proxy. **Purpose:**
so that the renewal is not the first commercial conversation of the year.

**Two conditions bind this draft, and both are refusals, not preferences.**

1. **R11 · Value first, ask second — never both.** Do not send this inside 14 days either side of
   an apology, an outage, a service credit, a missed milestone or any delivered miss. Move it,
   record the deferral and the new date in §6 of the plan, and never merge the two conversations.
   An ask attached to an apology reads as leverage and is remembered for years.
2. **No price in this message.** This conversation establishes commercial context — how the year
   went, what changes next year, when their budget line is set. The number arrives at T-90 with the
   proposal (Step 7). A price in this note collapses the two conversations back into one and
   forfeits the whole point of holding it early.

Open on something only this account's data could produce, name the agenda in their terms, and make
one dated ask. Nothing about the renewal outcome, the forecast, or why we are asking now.

```text
Hi <first name>,

<One specific, dated fact about their year with us that they would recognise as theirs — a
volume their team moved, a process they changed, a number their own person quoted.>

Your team's <year / fiscal year> plan is being set around now, and I'd rather understand it
before it's set than react to it afterwards. Half an hour on three things:

• what changed in <their function> this year, and what that means for next
• where <our product area> sits in the <next FY> plan
• when your budget line for it gets fixed, and who signs it off

No proposal in this one — I'll bring numbers to the next conversation, not this one.

Do either of these work: <day, date, time> or <day, date, time>?

<Name>
```

**Pre-send check specific to this draft:** no price, no uplift percentage, no renewal date, no
mention of notice or the contract term — those belong to Drafts 1 and 2. If the last 14 days
contain a miss, this draft does not go out today.

## Draft 1 — Courtesy notice-deadline letter (T-120, repeated T-90)

The most under-used artifact in renewals and the one that most reliably buys goodwill. A
customer who discovers their own notice window after it closed remembers it for years.

**Structure:** one specific thing their team achieved · the dates and the clause, flat · an
explicit "nothing needs deciding now" · one small dated ask.

````
════════════════════════════════════════════════════════════
CUSTOMER-FACING — copy the block below and send as written.
Everything above this line is internal. Do not forward it.
════════════════════════════════════════════════════════════

```text
Subject: Northwind agreement — the decision date is 3 Nov

Hi Dana,

Your dispatch team took on-time dispatch from 87% to 96% between March and
June, which is the number Sara said she'd judge this on when we started.

Two dates worth having in your calendar. The agreement runs to 1 February
2027. Section 7.2 asks either side for 90 days' notice, so the practical
decision date is 3 November — 68 days from today. Nothing needs deciding
now, and I'd rather you had the date from me than found it later.

If it's useful I'll put the March-to-June numbers into one page you can
send to Sara. Twenty minutes on Thursday or Friday and I'll have it done.

Thanks,

Jo
```
````

**What makes this version work.** It opens on their number, not our need. It states the clause
without arguing from it. It says out loud that no decision is being asked for, which is the
sentence that stops the letter reading as pressure. The ask is small, dated and useful to them.

**What the rejected versions did.** "I wanted to touch base ahead of your upcoming renewal" —
no content, and it makes the renewal the subject. "We'd hate to see you go" — invents a doubt
the customer did not have. "Per section 7.2 of the MSA, notice must be served" — correct and
cold; it opens a contract mid-relationship.

## Draft 2 — Written-intent question (T-75)

The exit criterion for the T-75 gate is *intent captured in writing, in the customer's words*.
Verbal intent from a champion is not the artifact. Ask the person who owns the budget line.

````
════════════════════════════════════════════════════════════
CUSTOMER-FACING — copy the block below and send as written.
Everything above this line is internal. Do not forward it.
════════════════════════════════════════════════════════════

```text
Subject: One question before the 3 Nov date

Hi Sara,

Short one. Between the proposal on 5 August and the 3 November decision
date, the only thing I still need from your side is a yes or a no on the
shape of it.

Is there anything that would prevent continuing at the terms we sent — on
your side or ours? A budget line that hasn't been set, a review I haven't
accounted for, or something we haven't delivered.

If the answer is "nothing I know of", one line back is enough and I'll
build the paperwork around your close week. If there is something, I'd
rather have it now than in October.

Thanks,

Jo
```
````

**Rules.** Ask it once, in writing, to the person with the budget. Ask for the obstacle, not
for a commitment — "is there anything that would prevent…" gets an honest answer where "can we
count on the renewal?" gets a polite one. Record the reply **verbatim**; a paraphrase in the
CRM is how a soft answer becomes a hard forecast. Never state or hint at what the answer will
do to the forecast.

## Draft 3 — Bridge-extension request (T-7, or rescue)

A bridge extension buys paper time at current terms. It is prepared *before* it is needed —
drafted and internally approved at T-30, sent only if required. Asking for it with a draft
already attached reads as competence; asking for it cold at T-3 reads as panic.

````
════════════════════════════════════════════════════════════
CUSTOMER-FACING — copy the block below and send as written.
Everything above this line is internal. Do not forward it.
════════════════════════════════════════════════════════════

```text
Subject: 30-day extension at current terms — draft attached

Hi Dana,

Your security review and the PO are both still open, and neither of them
is going to clear before 3 November. That's a scheduling problem, not a
commercial one, and I don't want it to force a decision either of us
would make differently with two more weeks.

Attached is a 30-day extension at your current terms — same price, same
scope, new end date of 3 December. It's already approved on our side and
it needs one signature on yours.

Two things that would make the underlying paperwork land faster:

  • The security questionnaire back to your InfoSec lead — I've filled
    in every section we can answer, so it should be a review not a build
  • Confirmation of who raises the PO, so I can send them the order form
    directly rather than through you

If the extension isn't the right instrument, tell me and I'll work to
whatever your legal team prefers.

Thanks,

Jo
```
````

**Rules.** Name the mechanical cause (an open review, an unsigned PO), never the commercial one
and never our own late start. Attach the draft. Keep price and scope untouched — a bridge that
reopens terms is a renegotiation with a deadline attached. State the new end date explicitly.

## Formatting rules inside the fence

| Do | Not |
| --- | --- |
| Plain text with a blank line between paragraphs | Markdown headings — they arrive as literal `##` |
| `•` bullets indented two spaces | Nested markdown lists |
| Real dates written the way the customer writes them | `[Date]`, `<date>`, `[Account]` |
| Real names, taken from the decision map | `[Name]`, "the champion", "your team lead" |
| Numbers the customer can verify in their own systems | Any number from our scoring |
| One fence per artifact, with a one-line label above it | Two messages crammed into one fence |
| A dated, specific ask in the last paragraph | "Let me know your thoughts" |

**Placeholders are a failure, not a courtesy.** If a name or a date is genuinely unavailable,
do not emit `[Name]` inside the block. Emit the block without that sentence and raise the gap
above the divider as `UNKNOWN — requires X`. A block containing a placeholder is not send-ready,
and the most common way an unedited template reaches a customer is that it looked finished.

## Pre-send checklist

- [ ] Runs the leak scan in `customer-voice.md` — no `risk`, `health`, `score`, `band`,
      `forecast`, `commit`, `ATR`, `exposure`, `save`, `play`, `tier`, `churn`, `retention`
- [ ] No forecast category, readiness score or MEDDPICC-R element appears in any wording
- [ ] Every number is one the customer can verify in their own systems or gave us themselves
- [ ] Every named person is on the thread or was named by the customer; no assessment of anyone
- [ ] Every inference is phrased as a question, not a claim
- [ ] The notice-deadline letter states the date and the clause and does not argue from them
- [ ] The intent question asks for the obstacle, not for a commitment
- [ ] The bridge extension names a mechanical cause and leaves price and scope untouched
- [ ] The commercial-context note (Draft 0) carries no price, uplift, renewal date or notice
      language, and is not being sent inside 14 days of an apology, outage, credit or miss (R11)
- [ ] Every commitment inside the block has an internally-agreed owner and a real date
- [ ] Nothing in the banned phrasebook appears
- [ ] Zero unfilled slots inside the fence
- [ ] Forward test: safe if this reaches their CFO, their procurement lead and a competitor
