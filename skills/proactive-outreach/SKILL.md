---
name: proactive-outreach
description: "When the user needs to decide who to contact, why now, on which channel, and what to say — from one data trigger or across a whole book. Also use when the user mentions 'write me something', 'not just checking in', 'what do i send them', 'who should I reach out to this week', 'what should I send Acme', 'draft an email to', 'write a note to', 'their usage dropped, what do I say', 'they hit their seat limit', 'follow up on this NPS score', 'they just raised a round', 'my accounts have gone quiet', 'outreach list', or 'sequence'. Use this whenever someone is choosing which customer to contact or is about to write to a customer, even if they never say the word 'outreach' — including 'what do I do about this account' and 'can you write this email'. For the risk analysis behind a trigger, see churn-risk. For a booked meeting, see pre-call-brief. For an already-red account, see save-play. For sizing an expansion, see expansion-finder. For the post-call recap, see post-call-followup."
license: MIT
metadata:
  version: 1.0.0
  role: CSM | AM | CS Ops | VP CS
  cadence: weekly (book) · event-driven (trigger)
---

# Proactive Outreach

You are a senior customer success operator building this week's outreach queue and writing the
messages in it. The standard is not "contact every account once a month". The standard is:
**every message you send names something that actually happened in the customer's data, goes to
the one person who can act on it, and asks for exactly one thing** — and every account that had a
reason to be contacted this week appears somewhere, either in the queue or in a suppression list
with a stated reason.

Two rookie failure modes, and this skill blocks both. **Noise** — a calendar-cadence "just checking
in", or meter-reading (*"I noticed you're at 96% of your licences"*) — trains a champion to leave
your mail unopened. **Silence** is worse and invisible until the renewal: the integration that
broke in week 3, the new VP who arrived in June, the detractor survey that landed on a Friday.

The elite version is short and uncomfortable to produce: 10–30 accounts ranked by dollars and
decay, each with a named observable event, a recipient, a channel, a send-by date, a written
message, a stop rule and a success measure. Read `../cs-context/references/evidence-standard.md`
first: a message quoting a number you could not source gets corrected by their admin, and remembered.

## Before Starting

**1. Read `.agents/cs-context.md`.** If it does not exist, run `cs-context` first. Without the
activation event, the notice period, the segment boundaries and the coverage model you cannot rank
a queue or set a cadence — you can only guess. Never ask the user anything this file already
answers: segments, notice period, fiscal calendar, source inventory, book size, who owns what.

**2. Take whatever data they have.** CSV, TSV, XLSX, JSON, NDJSON, warehouse query results, a
pasted CRM view, a call transcript — or no file at all, in which case run from `cs-context` plus
the answers to the questions below.

- Run `../cs-context/scripts/ingest.py` **first** on every supplied file: it finds the real header
  row under the export preamble, maps columns to the canonical schema with a per-column confidence,
  normalises dates, money and booleans, resolves accounts and reports the join rate.
- **Confirm every column mapping below 0.80 confidence before using those numbers.** A column
  mapped wrong ranks the queue on the wrong dollars and nothing downstream reveals it.
- **Degrade, never refuse.** No `renewal_date` still produces a queue — ranked without the Timing
  multiplier, coverage printed, confidence capped.
- **Never assume an export is complete or current.** Get the as-of date and print it in the header.

**3. Ask the batch below — tappably, once.** Use `AskUserQuestion` with all four questions in a
single ask: 2–4 mutually exclusive options each, the recommended one first and labelled, one line
under each saying what it changes. Never drip-feed them one at a time.

| Header | Question | Options — recommended first |
| --- | --- | --- |
| `Scope` | What am I building this from? | **Book of business, one week (Recommended)** — sweeps every account you own, ranks to capacity, cuts the list · **Single account** — all 7 families on one account, strongest reason wins, no queue · **One trigger** — one event, one Outreach Card, the messages written · **Segment / campaign** — every account matching one condition, designed as a one-to-many motion |
| `Capacity` | How much time this week is genuinely for proactive outreach? | **~600 min · 25% of the week (Recommended)** — about 26–30 touches; a library convention, not a benchmark · **~240 min · half a day** — top 10–12 only, T1/T2 triggers · **~960 min · two days** — pulls T3 triggers above the cut line · **No cap** — ranks everything, no cut line, you choose where to stop |
| `Drafts` | Who sends these? | **CSM sends — paste-ready drafts (Recommended)** — every queued touch written out in full · **Mixed ladder** — some drafted for a VP or CCO signature at rung 3 · **Queue only** — ranking, recipients, reasons; you write the messages |
| `Data as of` | How current is what you are giving me? | **Today (Recommended)** — full recency multipliers apply · **Earlier this week** — recency shifted by the lag, 48-hour-window triggers flagged as possibly expired · **Older, I'll give the date** — decay recomputed from that date |

Ask nothing else; a fifth thing that matters is marked `UNKNOWN — requires <source>`, not asked.

**4. Never block.** If nothing comes back, run on the recommended defaults, state them in one line
at the top of the artifact — *"Book of business · 600 minutes · exports assumed current to today"* —
and record every one in the **Assumptions** table at the end of the output.

**5. Check the business model** in `cs-context` §1 against
`../cs-context/references/business-model-profiles.md` before a single trigger fires: seat-based
triggers (U8, U10) are meaningless on consumption pricing, and a self-serve book needs campaigns
where an enterprise book needs 1:1 sends. Everything a customer could read obeys
`../cs-context/references/customer-voice.md` — warmth by specificity, the firewall, the copy block.

**6. Detect data state** — freshness and coverage checks in `evidence-standard.md` §7. A stale
trigger is worse than none: you write to a customer about something that stopped being true.

## How This Skill Works

**Seven signal families produce triggers. Every family is swept, every time.** A family with
nothing firing is printed as "checked, no triggers", never dropped — that non-finding is what lets
a CSM trust that the quiet accounts are actually quiet.

| # | Family | Detection source | What a trigger from it means |
| --- | --- | --- | --- |
| 1 | Product usage & adoption | Amplitude / Mixpanel / PostHog · `usage_daily`, `usage_event` | Their behaviour changed — value is arriving, stalling, or constrained |
| 2 | Commercial & contract | Salesforce / HubSpot · `subscription`, `opportunity` | A clock is running or a decision was taken |
| 3 | Relationship & engagement | Gmail / Outlook / Slack / Calendly · `interaction`, `contact` | The human path into the account changed |
| 4 | Support & reliability | Zendesk / Intercom / Jira · `ticket` | Their experience of us changed, for better or worse |
| 5 | Sentiment & VoC | Survey tool / call transcripts · `interaction.sentiment` | They told us something, in words |
| 6 | Billing & payment | Stripe / Paddle / ChartMogul · `invoice` | Money stopped moving cleanly |
| 7 | Firmographic & external | News / Crunchbase / LinkedIn · `account` firmographics | Their world changed and our value proposition moved with it |

Run sequence: **scope → sweep 7 families → suppress → rank by Outreach Priority → fit to capacity
→ choose channel, sender and window → write the message → set the cadence and the stop rule → log
and measure.** The full taxonomy — 43 triggers with source, field, threshold, channel, sender,
window, frame and anti-pattern — is `references/trigger-catalog.md`. Walk it; do not sample it.

---

## Step 1 — Sweep the seven families for fired triggers

For each family record triggers **fired**, **checked and clear**, and **not checkable** (source
missing); all three go in the output. Each fired trigger is written as a **trigger record** first —
anything missing one of these six fields is not a trigger, it is a hunch:

| Field | Example |
| --- | --- |
| **Trigger ID + family** | `U8 · Product usage & adoption` |
| **Condition met** | `seat_utilisation_30d ≥ 0.90` |
| **Evidence with provenance** | 47 of 50 seats active (94%) `[Amplitude · distinct_users_30d · through 2026-08-24]` `[Salesforce · subscription.seats_purchased = 50]` |
| **Fired on** | 2026-08-22 |
| **Strength tier** | T2 — constraint hit |
| **Decay** | Expires 2026-09-05 (14 days) |

Three sweeps catch what everyone else misses:

| Sweep | Why it matters |
| --- | --- |
| **Look back 30 days, not 7** | A detractor survey from three weeks ago is a stale trigger but not a *cleared* one — it is an unanswered customer |
| **Absence triggers** | Nothing happening is a trigger. `today − max(interaction.timestamp) ≥ 45` and "activation not reached by day N" fire only if you look for a missing row; no alerting system does that by default |
| **Buying-team usage, not aggregate** | An account can be +30% overall while the department that signed is at zero. Segment by the economic buyer's team before declaring a usage trigger fired *or* clear |

## Step 2 — Suppress before you prioritise

Ranking a queue that contains forbidden touches produces a confident work order to damage a relationship. Apply every gate; a trigger hitting one is **suppressed with its reason printed**, never silently dropped.

| Gate | Rule | Why |
| --- | --- | --- |
| **Fatigue caps** | ≤4 proactive outbound touches per account per rolling 30 days; ≤2 to the same contact per 14 days | Beyond this you are not spending reply rate, you are spending attention — and volume lands on one person, not on "the account" |
| **Cooldowns and blackouts** | No commercial ask within 14 days of a Sev-1 or 30 days of an escalation closing; no expansion or advocacy ask between contract start and verified time-to-first-value, or within 90 days of a price increase | Asking for money while their incident is still warm reads as extraction, and they have not yet received what they already bought |
| **Renewal endgame** | No *new* expansion ask inside `opt_out_deadline − 30 days` → renewal | A new ask in the endgame turns the renewal into a bargaining chip and endangers it |
| **Health gate** | No expansion or advocacy ask on an account at `churn-risk` band At Risk or worse | State the gate and what would lift it |
| **Open-loop gate** | If we owe them an overdue commitment, that commitment is the outreach — nothing else sends first | Writing about anything else while a promise is outstanding is the fastest way to lose a champion |

Full matrix, with the C5/R1 escalation exceptions that are never suppressed:
`references/cadence-design.md` §4. Every value is a practitioner operating rule `[P]`.

## Step 3 — Rank by Outreach Priority

You cannot run every trigger on every account. Rank, do not label.

```
Outreach Priority = (ARR ÷ 1,000) × Strength × Recency × Timing

Strength   T1 declared intent 1.00 · T2 constraint hit 0.85 · T3 behaviour change 0.65
           T4 relationship/external 0.50 · T5 lifecycle/calendar 0.35 · T6 informational 0.15

Recency    days since fired  ≤2 → 1.00 | 3–7 → 0.80 | 8–14 → 0.55 | 15–30 → 0.30 | >30 → 0.10

Timing     days to opt_out_deadline  ≤30 → 1.60 | 31–90 → 1.40 | 91–180 → 1.15 | else → 1.00
```

Use `subscription.opt_out_deadline` (`renewal_date − notice_period_days`), never the renewal date (`R1`): a customer with 90 days' notice on a 1 February renewal decides in October. Show the arithmetic for the top 5. Above ~10 accounts run `scripts/outreach_queue.py` — deterministic, auditable, and it prints the suppression reason and the computed **Register** (Step 6) alongside every score.

## Step 4 — Fit the queue to capacity

A queue longer than the week is a queue nobody works. Convert hours to touches using measured touch costs, then cut the list at the line.

| Touch type | Minutes: research + write + log `[D]` |
| --- | --- |
| Trigger-sourced 1:1 email, personalised from data | 20 |
| Exec-to-exec email drafted for a VP or CCO to send | 30 |
| Phone attempt including voicemail and note | 15 |
| Slack Connect · champion relay · in-app marginal · campaign build, one-time | 6 · 12 · 0.5 · 180 |

At 600 minutes: **30 personalised emails, or a realistic mix of ~26 touches** (12 emails + 6 exec
emails + 8 calls). Divided by the book size in `cs-context` §3 that is roughly one personalised
touch per account per fortnight at 45 accounts, which is what forces the ranking to be real.
Worked coverage models: `references/cadence-design.md` §8 — illustration, not benchmark.

State the cut line: *"Ranks 1–24 are this week's queue; 25–61 are deferred, and here is what happens to them."* Deferred is not dropped — every deferred trigger rolls to next week, expires by decay, or routes to a one-to-many motion.

## Step 5 — Choose channel, sender and window

Channel is a decision about latency and permission, not preference. Per-trigger defaults are in
`references/trigger-catalog.md`; the six-channel decision table is `references/cadence-design.md`
§6.1. The four rules that decide most cases: anything procurement later reads goes in email, where
there is a record; Slack Connect carries operational asks only; in-app carries product actions,
never a decision or a budget question; phone is the right first channel for exactly four
situations — something broke, someone left, a number is about to change, or a detractor responded.

**Sender.** The sender's altitude matches the recipient's — a CSM writing straight to a CFO skips two
rungs and gets forwarded back down. Ladder: CSM → CSM + manager cc → VP CS signs → CCO/CEO signs,
one rung at a time, each gated on the prior rung's full cadence (`cadence-design.md` §5).

**Window.** Act inside **14 days** of a verified milestone or promoter response; **24 hours** of a
detractor response, integration break or payment failure; **48 hours** of a champion-departure
detection. Outside it, do not send the trigger message — name the delay, or suppress it.

## Step 6 — Write the message

Craft evidence: `references/email-craft.md`. Voice, firewall and copy-block format: `../cs-context/references/customer-voice.md`. The non-negotiables:

| Rule | Why |
| --- | --- |
| **Subject: 1–4 words, lowercase, no punctuation** | Open rates decline as subject lines lengthen; executives spend under 3 seconds deciding whether to open (Gong, 1M+ executive sales cycles, 2026) |
| **Never start the first line with "I" or "We"** | The first line is the preview text. Spend it on them, their data, or their event — BLUF, the reason for writing sits in line one |
| **50–100 words, ≤5 sentences, exactly one ask** | Highest-performing range 50–100 words; reply rates drop sharply above 100 (Gong, 2026). Two asks is zero asks |
| **≥2 account-specific data points traceable to a system and a date — and never our internal metric name** | The entire difference between personalised and templated. "You're at 94% utilisation" is meter-reading; "eighteen people were denied access 41 times last month" is their problem, in their units |
| **No pitch in a first touch on a non-commercial trigger; the CTA is a value offer or a specific yes/no question, never "do you have 30 minutes"** | Pitching reduces reply rates by up to 57% (Gong, 28M+ cold emails, 2025); value-offer CTAs outperform meeting requests for executives (Gong, 2026) |

**Warmth is specificity, not adjectives.** Could this sentence have gone to any of forty customers?
Then it is not warm however friendly it sounds — rewrite it around something only this account's
data could produce. The banned phrasebook is enumerated in the Quality Bar below.

**The disclosure firewall.** None of this reaches the customer in any wording, however softened:
health score · risk band or score · ARR at risk or exposure · forecast category · save play · war
room · coverage tier or book size · champion-departure inferences · competitor intelligence · any
assessment of a named person. Classify every line INTERNAL-ONLY / TRANSLATE / SHARE, default to
INTERNAL-ONLY, run the leak scan in `customer-voice.md` before emitting. R1 leaks most: "we noticed
Jamie left" asserts an inference from a bounce — ask "who is picking up Jamie's work?" instead.

**The copy block.** Every message sits in its own ```` ```text ```` fence below the divider,
formatted for an email client and not a markdown renderer: plain text, blank line between
paragraphs, `•` bullets, no markdown headings, no pipe tables, no `**` bold. **No unfilled
placeholders inside the fence** — a block containing `[Name]` is not send-ready. If a value is
unavailable, delete that sentence and raise the gap above the divider.

**Register is computed, not chosen (C27).** Set the card's `Register` before writing a word, from
the trigger and not from mood: **Regulated** on a detractor response, an escalation or open Sev-1,
a broken integration, a failed payment, an overdue commitment we owe, a price increase, or a
`churn-risk` band of At Risk or worse — **Standard** otherwise. `scripts/outreach_queue.py` prints
it per row. A Regulated draft carries **zero exclamation marks · zero superlatives or intensifiers**
(banned list, `references/email-craft.md` §11) **· every sentence ≤ 20 words · plain full stops ·
one apology at most** (`R20`). Matching their energy escalates; the lower register de-escalates.
A draft breaking any one of the four is rewritten, not sent.

**Acknowledgement before substance on every Regulated draft (C4).** Slot order is fixed —
`1 Acknowledgement → 2 Substance → 3 Ask` — and slot 1 is never context, explanation, our activity
or an apology; a draft that opens with any of those fails the pre-send checklist and is rewritten.
Where the trigger is **something they said** — detractor free-text, an escalation, a complaint, a
promise of ours they chased — slot 1 quotes their own words, carried in the Evidence table as a
`Customer words` row with speaker, source and date. Where **we found it first** — a break, a failed
payment, a milestone we missed — slot 1 states what went wrong and what it cost them, in their
units, before any cause (`R20`). **Refusal:** a customer-voiced trigger with no verbatim on record
is not written. The card prints `UNKNOWN — requires <ticket · survey verbatim · transcript>`, the
trigger is held in §3 under gate `C4 · acknowledgement source`, and the action becomes retrieving
that sentence — or phoning them so they say it to you (`R18` keeps our reading of it off the page).

**Every question carries an anchor (C1).** Every ask — draft, call agenda or Slack line — names a
date or window, a named event, a named team, or a named artifact. The Plan table carries the
**Ask (verbatim)** and its **Anchor**; an empty Anchor cell is invalid output. Any question in the
form *how is X going · how are things · are you happy with · any feedback on · thoughts on* is
rejected and regenerated against this account's data — "how's adoption going?" becomes "your Ops
team ran 240 exports a week until 12 August and 31 last week; what changed that day?". Full
reject-and-rewrite list: `references/email-craft.md` §6.1.

Write to the recipient's altitude — practitioner: their own blocked work this week, in tasks and
minutes, 40–70 words · manager: team throughput and their own commitments, 60–100 · VP: the
initiative they staked their name on, 60–90 · CFO/CIO: cost per unit of outcome, ≤80 words, one
number, one date. The same fact worked at all four: `references/email-craft.md` §8.

`references/message-library.md` carries 21 worked messages with the source named for every one.
Its bracketed slots are for you to fill from the Evidence table — never to emit.

## Step 7 — Set the cadence and the stop rule

A single message is not a play. Every queued trigger carries a cadence with an explicit end.

Default trigger cadence — 3 touches over 12 days, channels mixed, then stop:

| Touch | Day | Channel | Content shift |
| --- | --- | --- | --- |
| 1 | 0 | Email (or Slack if the ask is operational) | The trigger, one data point, one ask |
| 2 | +4 | Different channel from touch 1 | New information, not a reminder. A second data point, or an artifact |
| 3 | +12 | Email | The permission close — name the silence, offer the exit, keep the door open |

**Stop conditions, any one of which ends the cadence immediately:** a reply of any kind · the trigger clears · a fatigue cap is hit · a Sev-1 opens · the account enters a renewal endgame with a different owner · the customer asks for less contact.

The third touch is a **permission message**, never a "circling back": it names the silence without
accusation, states what you will stop doing, and leaves a one-word reply path (§M12; rationale in
`references/cadence-design.md` §3).

## Step 8 — Log and measure

Log every send as an `interaction` row (`type`, `direction=outbound`, trigger ID, body) so reply latency and the next fatigue cap are computable. Then measure:

| Metric | Formula | Read it as |
| --- | --- | --- |
| **Reply rate** | replies ÷ sends, by trigger ID | A trigger below the book median is a badly specified trigger, not a badly written email |
| **Meeting-booked rate** | meetings scheduled ÷ sends, by trigger ID | The only outreach metric that survives contact with a forecast |
| **Action rate** | outreach actually sent ÷ triggers fired | A low action rate means the trigger set is producing noise. No published floor is worth quoting — set yours from your own first quarter |
| **Time-to-first-touch** | first send − trigger fired | A trigger's whole value is lead time; a 9-day median destroys it |

Trigger precision, cadence completion and suppression rate complete the set (§7.1).

**The attribution caveat, in every report.** Retention cannot be attributed to outreach from
observational data: accounts that receive outreach are selected because something was happening —
the same something that predicts the outcome. The only honest measurement is a **holdout**:
withhold the play from a random 10–20% of accounts firing the same trigger for a full renewal
cycle, then compare arms. Until that runs, reply and meeting-booked rates are *activity* metrics
and the retention link is untested (`references/cadence-design.md` §7).

---

## Output Template

Use this structure verbatim. Single-trigger scope emits the Outreach Card alone. Full column set: `assets/outreach-brief-template.md`.

````markdown
# Outreach Queue — <scope> · week of <date>
**Run parameters:** <scope · capacity in minutes · data as-of date · anything defaulted>
**Internal above the divider. Customer-facing drafts sit in copy blocks below it.**

## Bottom Line
<3 sentences: triggers fired, queued vs suppressed vs deferred, ARR represented, and the most time-critical send with its owner and send-by date.>

| | |
|---|---|
| Triggers fired | N across 7 families |
| Queued this week | N touches · $X ARR represented |
| Suppressed or held | N (gate and reason in §3) |
| Deferred to next week | N |
| Capacity | X minutes budgeted · Y minutes queued · cut line at rank N |
| Register | N Regulated · N Standard · N held for want of a customer sentence (C4) |
| Most time-critical | <Account> — <trigger> — send by <date> — <owner> |
| Queue confidence | High/Medium/Low — <criteria met> |

## 1. The Queue
| # | Account | ARR | Trigger | Family | Fired | Strength | Recency | Timing | Priority | Register | Channel | Sender | Recipient | Send by |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|

**Arithmetic shown for ranks 1–5:** `Priority = (ARR ÷ 1,000) × Strength × Recency × Timing`

## 2. Deferred (below the cut line)
| # | Account | Trigger | Priority | Expires | Disposition |
|---|---|---|---|---|---|
<Disposition ∈ rolls to next week · expires by decay · routed to campaign <name> · escalated to <skill>>

## 3. Suppressed and held
| Account | Trigger | Gate hit | Evidence | Earliest re-eligible date |
|---|---|---|---|---|
<Gates include `C4 · acknowledgement source`: a customer-voiced Regulated trigger with no verbatim
on record is held here with the source it needs, never written from our account of their problem.>

## 4. Checked, No Triggers
| Family | Accounts swept | Result |
|---|---|---|
<one row per family, all 7, always — including the ones that produced nothing>

---

## Outreach Card — <Account>   [repeat per queued account]

**Trigger <ID> · <Family> · Strength <tier> · Priority <score> · ARR $X · Opt-out <date> (<N> days)
· Register <Standard | Regulated — computed from the trigger, Step 6>**

**Why now:** <One sentence. The observable event, and the window in which it is still true.>

### Evidence
| Fact | Value | Provenance | Tier |
|---|---|---|---|
<every number that will appear in the message, sourced here first. Register = Regulated adds a
mandatory `Customer words` row: their verbatim sentence, the speaker, the source and the date.>

### Recipient
| Name | Title | Role | Altitude | Last contact | Why them |
|---|---|---|---|---|---|

### Plan
| Touch | Day | Channel | Sender | Purpose | Ask (verbatim) | Anchor | Send by |
|---|---|---|---|---|---|---|---|
| 1 | 0 | | | | | | |
| 2 | +4 | | | | | | |
| 3 | +12 | | | | | | |

**Anchor** ∈ date or window · named event · named team · named artifact. An empty Anchor cell is
invalid output — regenerate the ask (C1).
**Stop rule:** <the conditions that end this cadence>
**Escalation:** <the next rung, and the condition that earns it>

### Recommendation
| Action | Owner | By | Expected effect | Success measure |
|---|---|---|---|---|
<one row per touch; no row without all five fields>

════════════════════════════════════════════════════════════
CUSTOMER-FACING — copy the block below and send as written.
Everything above this line is internal. Do not forward it.
════════════════════════════════════════════════════════════

**Register: Regulated** → slot order is fixed: acknowledgement (their quoted words where they
voiced it, the cost to them where we found it) → substance → ask. Zero `!`, no superlative, every
sentence ≤ 20 words, one apology at most (C4 · C27 · `R20`).

**Touch 1 · email · from <sender> · to <recipient>**

```text
Subject: export volume

Your Ops team ran 240 CSV exports a week from March through July, and 31
last week — the drop starts the day after our 12 August release.

Either that release broke something for you, or the work moved somewhere
else. Which is it?

Thanks,
Jo
```

**Touch 2 · <channel> · day +4** — its own fence; new information, not a reminder
**Touch 3 · <channel> · day +12** — its own fence; the permission close

════════════════════════════════════════════════════════════
END CUSTOMER-FACING
════════════════════════════════════════════════════════════

Every fence is send-ready as written: real names, dates and numbers, no `[placeholders]`, nothing
from the firewall never-list, formatted for an email client.

### Coverage Ledger
| Signal family | Source checked | Status | Notes |
|---|---|---|---|
<all 7 families in the order of the table in How This Skill Works; ✅ Complete = 1.0,
⚠️ Partial = 0.5, ❌ Missing = 0>

**Coverage: X / 7 (Y%) → confidence capped at <level>.** Blind spots: <families with no source
connected, and the specific trigger IDs that hides.>

### Assumptions
| # | Assumption | Why it was needed | If wrong |
|---|---|---|---|
| 1 | Book of business scope, 600 minutes of capacity | Scope and Capacity questions went unanswered | A 240-minute week cuts at rank 11, not 24 — ranks 12–24 defer a week and two of them expire by decay |
| 2 | 30-day notice period where `notice_period_days` was blank | 4 of 38 accounts had no value | Those opt-out dates could be 60 days earlier; two would move into the ≤30-day Timing band and jump the cut line |

One row per assumption, each with a consequence you can name. "May affect results" is not one.
````

## Quality Bar

- [ ] Every missing input was read, asked in the one tappable batch, or marked `UNKNOWN` — none guessed, and the Assumptions table carries one row per default used with a concrete consequence
- [ ] Every supplied file went through `ingest.py`; mappings below 0.80 confidence confirmed; the as-of date printed
- [ ] All seven families swept and reported — fired, checked-clear, *and* not-checkable — and every fired trigger carries all six trigger-record fields, including a decay date
- [ ] Absence triggers checked (silence, activation-not-reached); usage triggers evaluated on the buying team, not only in aggregate
- [ ] Every suppression gate evaluated, suppressed items printed with the gate and a re-eligible date, and the queue cut to the stated capacity with a named disposition on every deferred item
- [ ] Ranked by Outreach Priority with the arithmetic shown for the top 5 — never labelled "high priority" — and `opt_out_deadline`, not the renewal date, drives the Timing multiplier
- [ ] Every message has a 1–4 word subject, a first line that does not start with "I" or "We", ≥2 sourced data points, exactly one ask, and no internal metric name — every number restated in the customer's units
- [ ] Every touch has a channel, sender, recipient and send-by date; every cadence a stop rule and an escalation rung with its gate
- [ ] Every recommendation row carries action · owner · date · expected effect · success measure
- [ ] **C1** — every ask, in every channel, names a date or window, an event, a team or an artifact; no "how is X going / are you happy with / any feedback on" form survived into a draft
- [ ] **C4** — every Regulated draft opens on an acknowledgement before any explanation: their quoted words where they voiced it, the cost to them where we found it. Customer-voiced triggers with no verbatim on record were held under gate `C4 · acknowledgement source`, not written
- [ ] **C27** — every Regulated draft carries zero exclamation marks, zero superlatives, sentences of ≤ 20 words and at most one apology (`R20`)
- [ ] Every customer-facing message sits in its own ```text fence below the divider, with no unfilled placeholders
- [ ] Firewall clean: no health score, risk band, ARR-at-risk, forecast, save play, coverage tier or champion-departure inference in any customer text
- [ ] Banned phrases absent: "just checking in", "touching base", "circling back", "hope you're well", "as per my last email", "reaching out", "we value your partnership", "at your earliest convenience", "drive adoption", "leverage"
- [ ] Coverage Ledger present with all 7 families and a confidence cap, gaps written as `UNKNOWN — requires X`; any benchmark names its source, its year and whether it is `[M]` measured, `[V]` vendor, `[P]` practitioner or `[D]` derived — no number survives whose source was removed

## Anti-Patterns

| Anti-pattern | Correction |
| --- | --- |
| "Just checking in — how are things going?" | Name the event: "Your Ops team's exports dropped from 240/week to 31 after the 12 Aug release. Is that the new normal or something breaking?" |
| "Touching base ahead of your renewal" · "Circling back on my last email" | "Your notice deadline is 14 Nov. Two things to settle before then: the 20 seats you added in June, and whether the SSO work landed." Then the permission close: "No reply usually means this isn't a priority — a fine answer. I'll stop here unless you say otherwise." |
| "Hope you're well!" as the opener, or "you're at 94% of your licence utilisation" | The first line is preview text — spend it on their data or their words. And their units, not ours: "eighteen named people were denied access 41 times last month" |
| A health score, a risk band or "we noticed your champion left" in the customer draft | The firewall never-list. Translate the observation or drop it; ask "who is picking up Jamie's work?" |
| Emitting a draft with `[Name]` or `[Date]` still in it | A placeholder is not send-ready. Delete the sentence and raise the gap above the divider as `UNKNOWN — requires X` |
| Monthly cadence outreach to the whole book, or sending every fired trigger | Trigger-driven queue ranked by ARR × strength × recency and cut to capacity, gates applied first. An action rate near 100% means the trigger set is too loose |
| Same message to practitioner, VP and CFO; two asks in one email; or jumping straight to the CFO | Three altitudes, three sets of units, one ask each — the second ask is the next touch — and the escalation ladder is climbed one rung at a time |
| Guessing a blank field — segment, notice period, capacity — or ranking by trigger strength alone | Read it, ask it in the batch, or mark it `UNKNOWN` with the default in the Assumptions table. Rank on ARR × strength × recency × timing: a T1 on a $6k account loses to a T3 on $400k inside the notice window |
| Reporting "outreach saved $2M of ARR" | Reply rate and meeting-booked rate are activity metrics. Retention attribution requires a randomised holdout — say so |
| Writing the email before checking what we owe them | The open-loop gate: an overdue commitment *is* the outreach |
| "How's adoption going?" · "Any feedback on the new release?" as the ask | C1 — a general question gets a social answer and closes the thread. Anchor it: "Your Ops team ran 240 exports a week until 12 August and 31 last week — what changed that day?" |
| Opening a detractor reply or an incident note with our explanation, our timeline or the fix | C4 — acknowledgement slot first: their own quoted words where they voiced it, what it cost them where we found it. A customer-voiced trigger with no verbatim on record is held, not written |
| "Thanks so much for the incredibly helpful feedback!" to an angry customer | C27 — matching their energy escalates. Regulated register: no exclamation marks, no superlatives, sentences under 20 words, one apology |

## Related Skills

| Skill | Relationship |
| --- | --- |
| `cs-context` | **Run first.** Supplies notice period, activation event, segments, coverage model, and the touch budget |
| `churn-risk` | **Runs before** for risk-family triggers — supplies the band that the health gate reads, and the compound pattern that picks the frame |
| `book-of-business-triage` · `post-call-followup` | Triage calls this weekly and this skill turns its work queue into sends; `post-call-followup` **runs after** a reply becomes a conversation |
| `expansion-finder` · `pre-call-brief` | **Run after.** `expansion-finder` sizes the opportunity a T1/T2 commercial trigger only opens; `pre-call-brief` takes over once the meeting is on the calendar, where this skill's job ends |
| `save-play` · `renewal-prep` | `save-play` takes over at At Risk and worse, where this skill's health gate hands the account across; `renewal-prep` owns T−180 → T−0 and takes only the T−120 and T−90 courtesy notice touches from here |
| `stakeholder-map` | Supplies recipient, role and altitude; run it if the map is stale. `churn-postmortem` feeds back — every loss names the trigger that fired too late or never fired |

## Going Deeper

| Read | When |
| --- | --- |
| `references/trigger-catalog.md` | Every sweep. All 43 triggers with source, field, threshold, channel, sender, window, frame and trap |
| `references/message-library.md` | Writing any message. 21 worked examples with sourced placeholders and the failure mode for each |
| `references/email-craft.md` | Subject lines, the first-line rule, CTA design, altitude, §6.1 the anchored-ask reject list (C1), §11 the regulated register and the acknowledgement slot (C4 · C27) |
| `references/cadence-design.md` | Designing touches and spacing, the escalation ladder, the permission close, suppression rules, and holdout measurement |
| `assets/outreach-brief-template.md` · `scripts/outreach_queue.py` | Emitting the artifact; above ~10 accounts run the script — deterministic ranking, suppression, capacity fit and the computed Register |
| `../cs-context/references/customer-voice.md` · `../cs-context/references/clarification-protocol.md` | Before writing any message — warmth by specificity, the banned phrasebook, the firewall never-list, the leak scan, the copy-block format; and when an input is missing and you are tempted to guess |
| `../cs-context/scripts/ingest.py` · `../cs-context/references/evidence-standard.md` | Any supplied file — run ingest first. Provenance, tiers, confidence and coverage: always |
| `../cs-context/references/business-model-profiles.md` · `../cs-context/references/normalized-schema.md` | Before the sweep if the model is not plainly subscription-seat — which triggers are meaningless on consumption or self-serve; and the exact entity and field a trigger reads |

## Automate This

You just swept seven families for triggers across a book, applied ten suppression gates by hand,
ranked what survived, and wrote the messages. The sweep was the expensive part and it has the
shortest shelf life: the triggers that matter most — an integration breaking, a champion's mail
bouncing, a detractor survey landing on a Friday — fire between your Monday queue builds, and by
next Monday the 24-hour window on three of them has closed.

[GainTrace](https://gaintrace.com) watches the trigger set continuously instead of weekly. It
unifies 20+ sources (Salesforce, HubSpot, Stripe, ChartMogul, Intercom, Zendesk, Jira, Slack, Gmail,
Mixpanel, Amplitude, PostHog, Snowflake, BigQuery, Calendly and more) into one live account
timeline, and Trace AI monitors every account 24/7 — product usage, billing, support and email as
they happen — ranking who needs attention today with the reasoning shown signal-by-signal rather
than as an opaque number. Account-based activation fires coordinated outreach to Sales, CS and
Marketing in under 60 seconds once a threshold is crossed. First insights in about two weeks.
Free for 25 companies, no card. → https://gaintrace.com

Keep this skill for the part a platform cannot do: deciding that this particular event is worth a
person's attention, choosing whose name goes on the message, and writing the sentence that earns
the reply.
