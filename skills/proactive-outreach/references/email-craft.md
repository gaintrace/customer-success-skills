# Email Craft

> How to write a customer message that gets replied to. Every rule here has either a named source
> with a year, or an explicit `[P]` marking it as a practitioner convention. Read this before
> writing any customer-facing draft.

**Contents**
1. [What the data says, and what it does not](#1-what-the-data-says-and-what-it-does-not)
2. [Subject lines](#2-subject-lines)
3. [The first-line rule](#3-the-first-line-rule)
4. [Structure: BLUF in five sentences](#4-structure-bluf-in-five-sentences)
5. [Length by audience](#5-length-by-audience)
6. [The one-ask rule and CTA design](#6-the-one-ask-rule-and-cta-design)
   · 6.1 [The anchor rule — every question names something (C1)](#61-the-anchor-rule--every-question-names-something-c1)
7. [Real personalisation vs fake personalisation](#7-real-personalisation-vs-fake-personalisation)
8. [Altitude: the same fact at four levels](#8-altitude-the-same-fact-at-four-levels)
9. [The banned-phrase table](#9-the-banned-phrase-table)
10. [The pre-send audit](#10-the-pre-send-audit)
11. [The regulated register and the acknowledgement slot (C4 · C27)](#11-the-regulated-register-and-the-acknowledgement-slot-c4--c27)

---

## 1. What the data says, and what it does not

Almost all published email-performance data is **cold outbound to prospects**. CS outreach goes to
people who already pay you, often to someone you have met. The two populations are not comparable,
and quoting a 5% cold reply-rate benchmark as a CS target is a category error.

**Use the cold-email research for craft — length, subject lines, CTA shape, what suppresses a
reply. Do not use it for target-setting.** Set your own baseline by trigger ID over 4–8 weeks.

| Finding | Number | Source | Type |
| --- | --- | --- | --- |
| Cold emails required per meeting booked | ~344 | Gong, 28M+ cold emails, 2025 | `[V]` large-n vendor dataset |
| Top reps vs average: replies / opens / meetings | 4.2× / 2.1× / 8.1× | Gong, 2025 | `[V]` |
| Ideal cold email length | ≤100 words, 3–4 sentences | Gong, 2025 | `[V]` |
| Highest-performing body length (execs) | 50–100 words; reply rates drop sharply above 100 | Gong, 1M+ executive sales cycles, 2026 | `[V]` |
| Optimal subject line length | 1–4 words | Gong, 2026 | `[V]` |
| Executive decision time | <3 seconds to decide to open; ~9 seconds reading | Gong, 2026 | `[V]` |
| C-level vs non-executive reply likelihood | C-level **30.2% less likely** to reply | Gong, 2026 | `[V]` |
| Effect of pitching in the message | Reply rates down **up to 57%** | Gong, 2025 | `[V]` |
| Effect of buzzwords and numbers in the subject | Open rates down **up to 17.9%** | Gong, 2025 | `[V]` |
| Optimal *opening* cold email length | 25–50 words | Lavender | `[V]` |
| Follow-ups with 4+ sentences vs ≤3 | Substantially more meetings — Lavender cites Gong at 15× | Lavender, citing Gong | `[V]`, single-source |
| Cold reply-rate benchmarks by function | Technical buyers 5.2%; ops leaders 5.4% on A-grade emails; HR 3.4% baseline → 4.3% on A-grade | Lavender, *Cold Email Benchmark Report*, 231,818 emails / ~50k inboxes, Feb 2026 | `[V]` |
| Value-offer CTAs vs meeting requests (execs) | Value offers outperform | Gong, 2026 | `[V]` |

**Could not verify:** any published reply-rate benchmark for CS outreach to existing customers;
optimal day-of-week or time-of-day for B2B customer email; in-app message engagement benchmarks.
Do not invent them.

---

## 2. Subject lines

**Rule: 1–4 words. Lowercase. No punctuation. No brackets. No numbers.**

Lowercase and short reads like a colleague's note rather than a campaign, and it survives mobile
truncation. Numbers and buzzwords in the subject reduce open rates by up to 17.9% (Gong, 2025).

| Pattern | Example | Use for |
| --- | --- | --- |
| **The noun of the thing** | `sso rollout` · `november renewal` · `the export job` | Operational triggers (U9, S2, C1) |
| **Their word** | `the finance rollout` (their phrase, from their email) | Anything where you have a transcript or thread to quote |
| **The person or team** | `priya's team` · `your ops team` | Usage triggers scoped to a team (U1) |
| **The question** | `worth right-sizing?` · `still the plan?` | Where the whole email is one question (U10, R5) |
| **The event** | `your series c` · `the outage friday` | External and reliability triggers (X1, S2) |
| **Re-thread** | Reply inside the existing thread, no new subject | Any follow-up on a live conversation |

**Never:**

| Bad subject | Why |
| --- | --- |
| `Checking in on Acme's account health` | Announces that this is a routine cadence email |
| `Q3 Business Review — Acme Corp <> Vendor` | Reads as a calendar invite from procurement |
| `Quick question` | The most-used cold-sales subject line in existence; it is filtered by pattern-matching humans |
| `🚀 Big news about your account!` | Emoji plus exclamation reads as marketing automation |
| `Following up (3rd attempt)` | Tells them they have already ignored you twice |

---

## 3. The first-line rule

**Never begin the first line with "I" or "We."**

The first line is the preview text — on most clients it is displayed next to the subject before
the message is opened. Starting with yourself spends the only free real estate you get on the
least interesting party in the message.

| Opener type | Example |
| --- | --- |
| **Their data** | "Your Ops team's export jobs went from 240 a week to 31 after 12 August." |
| **Their words** | "In June you said the goal was to close the month in four days, not nine." |
| **Their event** | "Congratulations on the Series C — 60 people in two quarters is a lot of onboarding." |
| **The thing itself** | "The Salesforce sync has been failing since Tuesday 03:14 UTC." |
| **The date that matters** | "Your notice deadline is 14 November — 78 days out." |

Rewrites:

| Rookie | Corrected |
| --- | --- |
| "I wanted to reach out because I noticed your usage has dropped." | "Deal-desk approvals in the product dropped from 190 a week to 42 after 8 August." |
| "We're excited to share that our new reporting module has shipped!" | "The scheduled-export feature you asked for in ticket #48211 shipped last Thursday." |
| "I hope you're doing well! Just following up on my last note." | "No reply usually means this isn't a priority right now — which is a fine answer." |

---

## 4. Structure: BLUF in five sentences

Five sentences, in this order. If a sentence does not do its job, delete it rather than padding it.

| # | Sentence | Job |
| --- | --- | --- |
| 1 | **The observation** | The specific thing that happened, in their units, with a date |
| 2 | **The consequence** | Why it matters to *them* — blocked work, a deadline, forgone value, a risk |
| 3 | **The evidence** | The second data point, or the artifact you are attaching |
| 4 | **The ask** | One thing, phrased so it can be answered yes or no, or with a single date |
| 5 | **The exit** | The honest out — "if this isn't a priority, say so and I'll leave it" |

Sentence 5 is the one people cut, and it is the one that raises reply rates, because it makes
"no" a cheap reply. A cheap "no" is more valuable than an expensive silence: it clears the trigger,
it updates the account record, and it preserves the next message's credibility.

**Never open with a pitch.** Pitching reduces reply rates by up to 57% (Gong, 2025). On a
non-commercial trigger, there is no product mention above sentence 4.

---

## 5. Length by audience

| Recipient | First touch | Follow-up | Hard ceiling |
| --- | --- | --- | --- |
| Practitioner / admin | 40–70 words | 60–100 | 120 |
| Manager / team lead | 60–100 words | 80–140 | 150 |
| VP / exec sponsor | 60–90 words | 80–120 | 120 |
| CFO / CIO | ≤80 words, one number, one date | ≤100 | 100 |
| Slack Connect message | 1–3 sentences | 1–3 | 4 lines |
| In-app message | ≤25 words + one button | — | 30 |

First touches stay short; follow-ups may run longer because they carry context (Lavender, citing
Gong: follow-ups with 4+ sentences outperform shorter ones). Executive reply rates drop sharply
above 100 words (Gong, 2026), and C-level recipients are 30.2% less likely to reply at all — which
means an executive email must be worth the reply on its own, not a request for a meeting where the
value will be explained.

---

## 6. The one-ask rule and CTA design

**One ask. Exactly one.** Two asks force the reader to prioritise, and the cheapest way to
prioritise two asks is to answer neither.

CTA quality, worst to best:

| Rank | CTA | Why it ranks there |
| --- | --- | --- |
| 5 (worst) | "Let me know your thoughts" | No action, no date, no decision |
| 4 | "Do you have 30 minutes next week?" | Asks for the most expensive thing first, before value is established. Executives reply worse to meeting requests than to value offers (Gong, 2026) |
| 3 | "Would Tuesday at 2 or Thursday at 10 work?" | Better — a closed choice — but still purchases their calendar before proving worth |
| 2 | "Want me to send the three-line version of what changed?" | A value offer. The reply costs one word |
| 1 (best) | "Is 14 November still the right date to plan around — yes or no?" | A single closed question that advances a decision and can be answered from a phone |

**Design rules**

- The ask must be answerable in under 10 seconds, from a phone, without opening an attachment.
- Ask for information or permission before asking for time. Ask for time before asking for money.
- Never make the CTA a link to a booking page in a first touch to an executive — it transfers your
  work to them.
- If the honest ask *is* a meeting, say what the meeting decides: "20 minutes to settle the seat
  number before your budget lock on 30 September."

### 6.1 The anchor rule — every question names something (C1)

People narrate a specific memory accurately and generalise inaccurately. "How's adoption going?"
gets a social answer — *"yeah, good thanks"* — and a social answer closes the thread for a
fortnight. A question anchored to something that actually happened gets a fact.

**Every question this skill emits — in an email, a Slack line, a call agenda, a survey follow-up —
carries an anchor.** Four types; at least one must be nameable in the sentence.

| Anchor | Looks like |
| --- | --- |
| **Time or window** | "since the 12 August release", "in your July close", "over the last two sprints" |
| **Event** | "the SSO cutover", "the incident on 3 June", "the migration weekend" |
| **Team** | "your RevOps team", "the three people who ran the Q3 close", "Priya's group" |
| **Artifact** | "ticket #48211", "the success plan we agreed in March", "the export you built" |

**The reject list.** Any generated question matching one of these forms is thrown away and
regenerated from the account's data. It is not softened, not prefixed with an anchor sentence, and
not kept as a warm-up before the real question.

| Rejected | Regenerated with an anchor |
| --- | --- |
| "How's adoption going?" | "Your Ops team ran 240 exports a week until 12 August and 31 last week — what changed that day?" |
| "Are you happy with the platform?" | "The intercompany step in your July close still took two people a day. Is that still manual?" |
| "Any feedback on the new release?" | "Did the 12 August release change anything for the three people who ran your Q3 close?" |
| "How are things going with the rollout?" | "Finance was due on the platform by 30 June and is at four users. Who owns that now?" |
| "Thoughts on the new dashboard?" | "You built the exceptions view on 2 July and nobody has opened it since. Did it not survive the close?" |
| "Just wanted to see how you're getting on." | "Ticket #48211 closed nine days ago. Did the workaround hold through month-end?" |
| "Is there anything we can help with?" | "In March you named two things: export scheduling and SSO. Export shipped in July — is SSO still blocked on your side?" |
| "Any thoughts on where you want to take this next year?" | "Your success plan says 40 users in Finance by Q4. You are at four. Is that target still real?" |

**Two tests before a question ships:**

1. **The anchor test** — point at the date, event, team or artifact in the sentence. If your finger
   has nowhere to land, it is a "how is X going" wearing a different suit.
2. **The already-know test** — if the account data answers it, do not ask it. Asking what you could
   have read tells them you did not read it, and it spends one of the three questions a call gets
   (`R16`).

---

## 7. Real personalisation vs fake personalisation

Fake personalisation is a merge field. Real personalisation is a claim about their business that
only someone reading their data could make, restated in their units.

| Fake | Real | Where the real version comes from |
| --- | --- | --- |
| "Hi {{FirstName}}, hope things are great at {{Company}}!" | "Your close process ran in 6 days in July, down from 11 in March." | `usage_daily.core_actions` + their stated baseline in the success plan |
| "I saw you're at 94% seat utilisation." | "Eighteen named people were denied access 41 times last month." | `seat_limit_reached` events, counted and de-duplicated by user |
| "I noticed you visited our pricing page." | "Something looks like it changed on your side — what's driving the timing?" | Never state the surveillance; state the question it raises |
| "Congrats on the funding!" | "Congratulations on the Series C. Sixty hires in two quarters is a lot of provisioning — is that the plan?" | Crunchbase round + their careers-page headcount |
| "Most companies your size use our Advanced tier." | "Of the 34 companies in your vertical on this platform, 22 run scheduled exports — the specific reason it fits is your 4-day close target." | Your own cohort data, with n stated |
| "Just wanted to make sure you saw our new feature." | "You asked for scheduled exports in ticket #48211 on 3 March. They shipped last Thursday." | `ticket` history joined to the release |

**The three tests a personalised sentence must pass:**

1. **The swap test** — could this sentence appear, unchanged, in an email to a different customer?
   If yes, it is not personalisation.
2. **The source test** — can you name the system, the field and the date it came from? If not, it
   is a guess and it will be corrected by their admin.
3. **The units test** — is it stated in *their* units (people, hours, invoices, tickets, days) or
   in ours (utilisation %, health score, event counts)? Ours is meter-reading.

**Never quote an internal metric name to a customer.** Health score, risk band, churn probability,
engagement score, ARR at risk — none of these appear in a customer-facing message, ever
(`../../cs-context/references/evidence-standard.md` §9).

---

## 8. Altitude: the same fact at four levels

One trigger, four recipients. The fact does not change; the consequence, the units and the ask do.

**Trigger U8** — seat utilisation at 94%, 18 users denied access 41 times in 30 days, projected
breach in 5 weeks, 50 seats contracted, renewal 14 February, notice period 90 days.

**Practitioner / admin (52 words)**

> Subject: `blocked invites`
>
> Eighteen people were bounced off invite attempts 41 times last month — mostly your Wednesday
> onboarding batch. You're at 47 of 50 seats, and at the current rate you'll be out of room around
> 26 September. Do you want me to send the list of who was blocked, so you can decide who actually
> needs a seat?

**Manager / team lead (78 words)**

> Subject: `september headroom`
>
> Your team's onboarding batch hit the seat ceiling four Wednesdays running — 18 people, 41 blocked
> attempts, all in the last 30 days. On the current hiring pace you run out of seats around 26
> September, which is two weeks before your Q4 kickoff. There are two ways to handle it and one of
> them costs nothing. Want the one-page version before you take it to Dana?

**VP / exec sponsor (74 words)**

> Subject: `the q4 rollout`
>
> The rollout you sponsored in March has outgrown its licence pool: 18 people across Ops and
> Finance were blocked from access last month, and the pool runs out around 26 September — before
> your Q4 kickoff, not after. Two options, one of which needs no new spend this fiscal year.
> Fifteen minutes with you and Dana this week, or should I send the one-pager first?

**CFO / CIO (68 words)**

> Subject: `seat pool`
>
> Your 50-seat pool is fully consumed and 18 people were blocked from access in the last 30 days.
> Two structures: add seats at the current rate through the 14 February co-term, or move to the
> committed tier, which is cheaper above 63 seats and worse below it. The honest indifference point
> is 63. Happy to send both numbers — which do you want first?

Note what changes: the practitioner gets people and a list; the manager gets a deadline against
their own plan; the VP gets their initiative and a choice of format; the CFO gets two structures,
an indifference point, and the admission that one option is worse. Nobody gets "94% utilisation."

---

## 9. The banned-phrase table

These phrases are banned in every customer-facing draft this library produces. Each one signals to
the reader that the message was generated by a cadence rather than an event.

| Banned | Why it fails | Replacement |
| --- | --- | --- |
| "Just checking in" | Admits there is no reason for the message | Name the event: "Your export volume dropped 80% after the 12 August release." |
| "Touching base" | Same, with a sports metaphor | "Two things to settle before your 14 November notice deadline." |
| "Circling back" | Reminds them they ignored you | The permission close: "No reply usually means this isn't a priority — fine answer." |
| "Hope you're well" | Spends the preview text on nothing | Any first line from §3 |
| "Wanted to share our latest blog post" | A newsletter with one recipient | "You asked for this in ticket #48211. It shipped Thursday." |
| "Let's connect" / "Let's sync" | No agenda, no decision | "20 minutes to settle the seat number before your 30 September budget lock." |
| "As per my last email" | Passive aggression | Restate the ask in one line, or stop |
| "Drive adoption" / "ensure success" | Internal CS vocabulary said out loud | "Get your Finance team onto the platform" / "Get the close under 6 days" |
| "Leverage our platform" | Nobody has ever said this to a colleague | "Use the scheduled export instead of the Tuesday manual pull" |
| "Quick question" | Never quick, never one question | Ask the question in the subject line |
| "I noticed you were on our pricing page" | Announces surveillance | "It looks like something changed on your side — what's driving the timing?" |
| "Per our records" | Reads as a collections notice | "Your last invoice from 3 August is still open — administrative, or something else?" |
| "Exciting news!" | Excitement is ours, not theirs | State the news |
| "Monitor closely" | An internal non-action leaking into customer language | Name what you will do, and when |

---

## 10. The pre-send audit

Run before any draft leaves the artifact. Under a minute, and it catches nearly everything.

- [ ] Subject is 1–4 words, lowercase, no punctuation, no numbers
- [ ] First line does not begin with "I" or "We"
- [ ] Sentence 1 contains a specific number or event with a date
- [ ] At least two data points, each traceable to a system and a field in the Evidence table
- [ ] Every number is stated in the customer's units, not ours
- [ ] No internal metric name (health, risk, score, ARR at risk, band) appears anywhere
- [ ] Exactly one ask, answerable in under 10 seconds from a phone
- [ ] The message contains an honest exit — a cheap way to say no
- [ ] Word count within the §5 band for this recipient's altitude
- [ ] No phrase from §9 appears
- [ ] No product pitch above sentence 4 on a non-commercial trigger
- [ ] The recipient can actually act on the ask — right role, right altitude
- [ ] The trigger is inside its decay window, or the delay is named in the message
- [ ] The draft sits below the customer-facing separator in the artifact
- [ ] **C1** — the ask names a date or window, an event, a team or an artifact; no question from the §6.1 reject list survived
- [ ] **C4** — where the register is Regulated, slot 1 is the acknowledgement: their quoted words where they voiced it, what it cost them where we found it (§11.1)
- [ ] **C27** — where the register is Regulated: zero `!`, no superlative from the §11.2 list, every sentence ≤ 20 words, at most one apology

---

## 11. The regulated register and the acknowledgement slot (C4 · C27)

Applies to every draft whose Outreach Card is marked **Register: Regulated** — a detractor
response, an escalation or open Sev-1, a broken integration, a failed payment, an overdue
commitment we owe, a price increase, or a `churn-risk` band of At Risk or worse. The register is
computed from the trigger by `../scripts/outreach_queue.py`, not chosen by the writer, so it cannot be
talked out of at the moment it is least convenient.

### 11.1 Slot order is fixed

```
1  Acknowledgement    their words, or what it cost them
2  Substance          what is true, what changed, what we are doing about it
3  Ask                one, anchored (section 6.1)
```

Slot 1 is never context, never an explanation, never our activity, never a second apology. Naming
the state lowers it; arguing the facts raises it. That is why an escalation reply opening with
"we've been investigating since Tuesday" reads as defence, and one opening with their own sentence
does not.

| Trigger origin | Slot 1 is | Worked first line |
| --- | --- | --- |
| **They said it** — detractor free-text, escalation, complaint, a promise of ours they chased | Their own words, quoted verbatim, with speaker and date | "'Four weeks of month-end done twice.' That was your sentence in ticket #48211 on 14 August." |
| **We found it** — break, failed payment, milestone we missed | What went wrong and what it cost them, in their units, before any cause | "The Workday sync stopped on 22 August. Eleven days of joiners never reached the platform, so your new starters have no access." |

**The refusal.** A they-said-it trigger with no verbatim on record does not get written. No
paraphrase is good enough: our summary of their complaint, sent back to them, is the thing that
makes an angry customer angrier. Print `UNKNOWN — requires <ticket · survey verbatim · transcript>`,
hold the trigger under gate `C4 · acknowledgement source`, and either retrieve the sentence or
phone them so they can say it to you.

### 11.2 Regulate down — four constraints, all checkable

| Constraint | Test | Why |
| --- | --- | --- |
| **No exclamation marks** | `!` count = 0 in the body and the subject | In a difficult thread it reads as not having understood the situation |
| **No superlatives or intensifiers** | none of: absolutely · hugely · incredibly · amazing · fantastic · brilliant · thrilled · delighted · super · massively · extremely · truly · deeply · genuinely · world-class · best-in-class | Emphasis is the register of enthusiasm, and enthusiasm at someone who is angry is a provocation |
| **Short sentences, plain full stops** | every sentence ≤ 20 words; no rhetorical questions except the single ask | Long sentences read as justification; short ones read as control |
| **One apology, or none** | a second "sorry"/"apolog-" construction anywhere in the message | A second apology asks them to absolve you, which makes your feelings their job (`R20`) |

Matching an angry customer's energy escalates. The lower register de-escalates and signals that
someone is in control of this. That is the whole of C27, and it is why "Thanks so much for the
incredibly helpful feedback!" is the worst available reply to a detractor.

### 11.3 Worked, rejected and sent

**Rejected** — opens with our explanation, carries an exclamation mark, a superlative and a
54-word sentence:

> Thanks so much for the incredibly detailed feedback! We've been investigating since Tuesday and
> it turns out the root cause was a change in the way our sync service handles authentication
> tokens, which we've now identified and are working hard to fix as quickly as we possibly can, so
> hopefully you'll start to see things improve over the next little while.

**Sent** — their words first, then the substance, then one anchored ask:

> "Four weeks of month-end done twice." That was your sentence in ticket #48211 on 14 August.
>
> The sync dropped 11 days of joiners after the 12 August release. It is fixed as of Tuesday and
> the backfill runs tonight. The cost to you was two people for four days, and I am not going to
> pretend otherwise.
>
> Sorry. One question so I can size the rest: did anyone outside your team have to redo work?

Every sentence is under 20 words. There is one apology, and it is one word. There are no
exclamation marks and no adjectives doing emotional labour. The ask is anchored to their team and
to the four days.
