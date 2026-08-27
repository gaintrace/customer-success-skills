---
name: exec-escalation-comms
description: "When something has broken, slipped, or is about to change, and it has to go in writing to a customer executive — a note that will be forwarded, unedited, to people you have never met. Also use when the user mentions 'we had an outage', 'write the note to their exec', 'I need to tell them we missed the date', 'escalation email', 'how do I tell them', 'we broke it', 'incident update', 'RCA for the customer', 'price increase letter', 'end of life notice', 'sunsetting a feature', 'I promised something we cannot deliver', 'apology email', 'their CTO is furious', or 'this is going to their board'. Use this whenever bad news has to travel outward in writing, even if they never say 'escalation' — a status update, a missed date and a price change are the same artifact under different names. For the war room and the save decision behind it, see save-play. For the risk read, see churn-risk. For price and terms, see renewal-negotiation. For a normal call recap, see post-call-followup."
license: MIT
metadata:
  version: 1.0.0
  role: CSM | AM | FDE | VP CS | CCO
  cadence: per-incident · per-announcement
---

# Executive Escalation Comms

You are writing a note that will be forwarded to people you have never met. It will land in
their CIO's inbox with two words of preamble, get pasted into a procurement thread six weeks
later, and be read aloud in a meeting you are not in. It carries your name and it outlives the
incident. **Every rule here follows from that one fact.**

The rookie version writes only to the addressee, hedges the cause because it is not confirmed,
uses the passive voice to avoid naming who did what, promises a fix date nobody in engineering
agreed to, and waits three days for certainty before sending anything. Each feels careful.
Together they produce the artifact that loses the account: the customer learns the failure and
the vendor's evasiveness in the same document, and the second is what they remember. The elite
version goes out **before** the cause is known, says plainly what is and is not yet understood,
quantifies the damage in the customer's own units, names one human against every commitment,
and states the exact time of the next update — then hits it.

Read `../cs-context/references/customer-voice.md` before drafting and
`../cs-context/references/evidence-standard.md` before quantifying anything. Craft codes `C3`
`C4` `C26` `C27` `C28` from `../cs-context/references/practitioner-craft.md` are enforced as
template slots and refusal conditions, not advice. Every run produces two artifacts — internal
and customer — never the same document with words removed.

## Before Starting

1. **Read `.agents/cs-context.md`** (fallback `.claude/cs-context.md`). If absent, run
   `cs-context`. **Never ask for anything that file already answers** — ARR, renewal date,
   notice period, segment, owning CSM, escalation ladder, source inventory. Asking mid-incident
   is the fastest way to be closed.

2. **Take the input in whatever shape it arrives** — CSV, TSV, XLSX, JSON, NDJSON, warehouse
   results, a pasted Slack thread, an incident timeline, a Jira export, a status-page history, a
   transcript of the call where you promised the thing, or nothing but the user describing what
   happened. Run `../cs-context/scripts/ingest.py` on every supplied file first: it sniffs
   encoding and delimiter, finds the real header under export preamble, maps columns onto the
   canonical schema with a confidence per column, normalises dates, money and booleans, resolves
   accounts across files, and reports the join rate. **Confirm every column mapping below 0.80
   confidence before a number from it reaches the note** — a mis-mapped affected-tenant column
   puts a wrong blast radius in a document that gets forwarded to a regulator. **Degrade, never
   refuse:** "3 of your jobs failed; I am confirming whether a fourth did" beats silence while
   you check. **Never assume an export is current** — ask its as-of date and print it.

3. **Ask up to four questions, once, tappably — then draft unattended.** Use `AskUserQuestion`
   with every applicable question in a **single batch**. Skip any that `cs-context`, the thread
   or the user's own prompt already answers.

| Header | Question | Options — recommended first |
| --- | --- | --- |
| `Situation` | What kind of bad news is this? | **Unplanned failure — outage, degradation, missed date, broken commitment (Recommended)** · the seven-section note with a live update clock — **Planned change we are announcing** · price, EOL, tier, coverage; notice-period arithmetic runs and `R1` gates the send date — **We got it wrong** · our advice, our number, our decision was wrong and they acted on it — **Security or data incident** · legal and security own the wording; this skill drafts the relationship note that sits beside theirs, never the notification itself |
| `Stage` | Where are you in it? | **First note — cause not yet known (Recommended)** · the highest-value note and the one most often skipped — **Update — live and moving** · cadence note, sent whether or not there is news — **Resolution** · the closure note and what it must not claim — **Written review after closure** · timeline, cause, prevention, and the receipt on what changed |
| `Reach` | Who receives it? | **One named account, to their executive (Recommended)** · a single note, exec register, CSM on the thread — **Tiered — top accounts individually, the rest by list** · the individual notes go a day earlier, never the same hour — **Everyone affected, one note** · lowest-common-denominator wording; assume it reaches a competitor |
| `Authority` | What is actually agreed internally? | **Nothing yet — I need the internal brief first (Recommended)** · the customer note carries no commitment until the internal version has been agreed — **Agreed, and every owner has said yes to their date** · commitments may be stated — **Agreed, owners not confirmed** · every unconfirmed commitment is stripped from the customer note, not softened (`R19`) |

4. **Never block, and never guess.** Every missing input resolves one of three ways — **read
   it** (derive it, show the derivation), **ask it** (step 3, only where two answers change the
   note), or **mark it** (`UNKNOWN — requires <source>`). A plausible substituted number becomes
   a fabricated one the moment the note is forwarded. Unanswered, draft on the defaults, state
   them above the divider, and give each a row in the **Assumptions** table.

5. **Detect state.** Run `scripts/update_clock.py` where there is an incident timeline or a
   planned effective date — it computes the next update time, whether one is overdue, the impact
   arithmetic with its working, and per-account notice compliance against
   `renewal_date − notice_period_days`. Then run the coverage sweep in Step 1.

## How This Skill Works

### Output mode — Brief by default

| Mode | Length | Contains | When |
| --- | --- | --- | --- |
| **Brief** (default) | The note plus ~10 lines | The send-ready customer block, the send instructions (channel · sender · timing), the committed next-update time, and any commitment stripped under `R19` | Always, unless asked for depth |
| **Full** | The complete Output Template | Internal exec brief, coverage ledger, assumptions, cadence plan, prevention register | Asked for it · an exec is being briefed · a war room is open · someone will challenge the wording |

Brief **is the note**, written first and send-ready — not a summary of Full. It obeys every
evidence rule; what it drops is the display of the reasoning. End with:
*Internal brief, coverage ledger and cadence plan on request.*

### The rules this skill enforces

| Rule | Enforced how |
| --- | --- |
| **R19 · No Date You Do Not Own** | The five-gate commitment ladder in Step 4. A date whose named owner has not agreed it is **removed** from the customer note, and the removal is printed above the divider |
| **R20 · Bad News First, Once** | The Situation section is sentence one. The second-apology scan in Step 5 refuses a draft containing two |
| **R18 · The Firewall** | Health band, risk score, ARR at risk, exposure, forecast category, save play, war room, coverage tier, champion inferences, competitor intelligence and any assessment of a named person — ours or theirs — reach the customer in no wording |
| **R11 · Value First, Ask Second — Never Both** | No commercial ask, renewal mention, expansion opening or upsell appears in any note this skill emits. A concession attached to an apology reads as leverage and is remembered for years |
| **R1 · The Opt-Out Calendar** | Planned changes are gated on `renewal_date − notice_period_days` per account, not the renewal date and not a single global notice period |
| **R23 · The Coverage Cap** | Confidence never exceeds coverage. Below 60% the note may not state a blast-radius figure at all — it states what is known and when the rest will be known |
| **R3 · The 48-Hour Champion Rule** | Its mirror: when the departure is **ours**, the note goes out before the last working day, from the departing person, with the successor named |

Craft mechanisms: `C3` the number is the last sentence of its paragraph, unsoftened · `C4` the
acknowledgement slot precedes the substance and restates their own words · `C26` genuinely bad
news follows a call · `C27` register regulates down · `C28` one apology.

### Business model changes what "bad news" even is

Resolve the profile from `../cs-context/references/business-model-profiles.md` first. A
consumption business apologising for seat downtime, or a self-serve business writing an
exec-to-exec note to an account with no executive, is the recognisable shape of generic output.
What changes per model is in `references/cadence-and-severity.md` §6.

Run sequence: **sweep the facts → set severity and the clock → find the cause or say you have
not → gate every commitment → decide the apology → write the internal version → write the
customer note → leak scan → schedule the closure and the receipt.**

## Step 1 — Sweep the facts before choosing a frame

The note is only as good as the seven-family sweep under it. Walk all seven, every time, and
record what came back **clear** as well as what fired — "no other customer of yours was
affected" is a fact the reader needs, not an omission.

| Family | What it supplies to this note |
| --- | --- |
| Product usage & adoption | The blast radius in **their** units — which of their workflows, jobs, users, tenants. The only credible impact statement |
| Commercial & contract | ARR, renewal date, **opt-out deadline**, SLA and credit terms, notice clause. Gates a planned change (`R1`); never appears in the customer note |
| Relationship & engagement | Who receives it, who is on the thread, who is furious, who has gone quiet, which of their execs has been dragged in |
| Support & reliability | Ticket IDs, SLA breaches, prior occurrences of this same failure. **A repeat changes the note more than the failure does** |
| Sentiment & VoC | Their own words about this — from the ticket, the call, the survey. Quote them back (`C4`) |
| Billing & payment | Whether a credit is contractually owed, already issued, or offered discretionarily |
| Firmographic & external | Whether their customers, their regulator or their auditors sit downstream of this. It changes the severity, and it is the family most often skipped |

**Below 60% coverage, no blast-radius number goes in the note** — state what is known and when
you will know the rest.

## Step 2 — Set severity, and start the clock

Severity comes from **the customer's ability to work**, never from our engineering effort or
our embarrassment. Definitions, cadence table and notice periods: `references/cadence-and-severity.md`.

| Sev | The customer's position | First note within | Update floor | Sender |
| --- | --- | --- | --- | --- |
| **S1** | A core workflow is unavailable with no workaround, data is exposed or lost, or their own customers are affected | 60 min of confirmed impact | Hourly | VP+ or the incident lead, CSM on the thread |
| **S2** | A core workflow is degraded, or a workaround exists that costs them hours | 4 business hours | Twice daily | CSM, countersigned by their manager |
| **S3** | A non-core function is affected and the workaround is cheap | Same business day | Daily | CSM |
| **S4** | Nothing is broken; something is changing that will cost them | Per the notice table | As stated in the first note | Per variant |

**Send the update even when there is nothing new.** This is the rule practitioners break first
and regret most. *"No change since 14:00; still on the database layer; next update 16:00"* costs
sixty seconds and preserves the customer's belief that someone is holding the situation. Silence
for two cycles reads as loss of control, and the customer fills the gap by escalating to someone
who knows less than you do. Status-page practice converges on the same floor: a 30-minute
baseline for a major outage and an explicit instruction never to go silent — say so, and state
the next update time, even when the update is that nothing changed `[P, PagerDuty status-page
guidance, accessed 2026-08]`. `scripts/update_clock.py` computes it and flags an overdue update.

## Step 3 — Write the cause honestly, or say you do not have it

**Waiting for certainty is the most damaging choice available.** The first note goes out before
the cause is known: the customer's exec is already being asked what happened, and the only
question is whether their answer comes from you or from a status page. An honest unknown sent
now buys more credibility than a complete note two days later. What it says:

| Slot | Written as | Never |
| --- | --- | --- |
| What is broken | The specific capability, named in their words | "Some customers are experiencing issues" |
| Who is affected | Their scope, and explicitly what is **not** affected | Silence about the boundary, which they read as "everything" |
| Cause | "We do not yet know the cause, and I will not speculate — being wrong about it costs you more than waiting an hour does." | "We believe this may be related to…" |
| What is happening now | Named team, named lead, what they are doing | "We are investigating" |
| What they should do | The workaround, or an explicit "nothing — do not re-run the jobs" | Nothing, leaving them to guess |
| Next update | An exact clock time in **their** timezone | "as soon as we know more" |

Once known, write the cause **in the active voice with the actor named as us** — never an
individual (Step 8). "A schema migration ran without a lock check. That was our change and our
miss" buys back more credibility than three paragraphs of architecture. The passive alternative
— "an issue occurred", "the migration was executed" — is what William Safire called the
*passive-evasive* and political scientist William Schneider named the **past exonerative
tense**: it admits a fault while deleting the party responsible, and it is transparent to every
executive who has read one before.

## Step 4 — Gate every commitment before it is written

This is what separates a note that holds up from one that creates the second, worse
conversation. **Every commitment passes five gates. One that fails any gate is removed from the
customer note, not softened.**

| # | Gate | Evidence required | If it fails |
| --- | --- | --- | --- |
| 1 | **Named owner** | One human's name and role — not a team, not "engineering" | Strip the sentence |
| 2 | **They have agreed** | That person said yes to **this** date, in writing, with a timestamp | Strip it, or downgrade to a date you own: *"I will have an answer from Sam by Thursday, including if the answer is no"* |
| 3 | **Authority** | The commitment sits inside their remit, or their manager approved it | Escalate internally before sending, not after |
| 4 | **A date we own** (`R19`) | Not a roadmap date, not a release train we do not control | Replace the delivery date with a **decision** date |
| 5 | **No commercial content** (`R11`) | It changes no entitlement, SLA, price or term | Route to `renewal-negotiation`. A credit or concession offered inside an escalation becomes the expected response to every future one |

**"It's on the roadmap" is the kindest-sounding sentence in customer success and the most
damaging** (`R19`). A clear no with reasoning and the nearest alternative preserves more trust
than a soft yes that turns out false. Print every stripped commitment above the divider.

## Step 5 — Decide the apology deliberately

An apology is a tool with a narrow range, not a default courtesy, and the evidence separates
two cases cleanly. **Competence failures — we tried and failed — take an apology**: trust is
repaired more successfully by apology where the violation concerns competence `[A, Kim, Ferrin,
Cooper & Dirks 2004, *Journal of Applied Psychology* 89(1)]`. **Integrity questions where we are
not at fault take a denial**, per the same study — a reflexive apology for something you did not
do gets quoted back in the negotiation and converts a disagreement into an admission. Three
further constraints, all opinionated and all defensible:

1. **Once, in one sentence, and never again** (`R20`, `C28`). A second apology asks the customer
   to absolve you, which makes your feelings their job.
2. **An apology travels attached to three things or not at all**: their number, a completed
   action with a timestamp, and a named next date. Alone it is a request for absolution.
3. **Containment beats compensation.** B2B service-failure research finds auxiliary resources
   that shrink the magnitude of the failure elicit recovery more reliably than limited monetary
   compensation, and that response speed is the provider's most effective lever `[A, Hübner,
   Wagner & Kurpjuweit 2018, *J. Business & Industrial Marketing* 33(3), 43 informants]`. Offer
   the engineer, the migration, the manual re-run — before you offer a credit.

Temper the expectation: the service-recovery-paradox meta-analysis finds the effect positive on
**satisfaction** but non-significant on repurchase intention, word of mouth and corporate image
`[A, de Matos, Henrique & Rossi 2007, *J. Service Research* 10(1)]`. A recovered failure is a
return to neutral, not an asset. Decision table, and where an apology reads as weakness:
`references/accountability-language.md` §4.

## Step 6 — Write the internal version first

The internal version is written first, always — it is where the commitments get agreed, and
Step 4 has nothing to gate against otherwise. One page; if it needs two, the escalation is not
understood yet. Spec and worked examples in `references/internal-versions.md`.

What it carries that the customer note **never** does: ARR at risk with the specific scenario
(full churn or a downsell of $X), the opt-out deadline and days remaining, the health band and
matched pattern, the pre-approved commercial latitude and what we get for it, the relationship
read on named people, the stop-loss, what we are deliberately not telling the customer yet and
why, and the **one decision required** — from a named executive, by a date. An escalation with
no named ask and no decision date is a notification.

## Step 7 — Write the customer note in the seven-section spine

Seven sections, in this order, every time — the order in which a forwarded reader with no
context can absorb it. Each does one job.

| # | Section | The job it does | It has failed when |
| --- | --- | --- | --- |
| 1 | **Situation** | Gives a stranger the whole event in one sentence, so nobody has to ask what this is about | It opens with context, a greeting, an apology or a defence |
| 2 | **Impact, quantified** | Removes the customer's need to compute their own exposure, and proves you did the work of finding out | It is stated in our units — uptime %, SLA percentages — instead of their jobs, their users, their hours |
| 3 | **Root cause** | Buys back credibility: a vendor that can name its own cause can be believed about the fix | Passive voice, an individual named, or speculation offered as fact |
| 4 | **Actions taken, with timestamps** | Converts "we are on it" into evidence. The timestamps are the whole point | Undated verbs — "we have been working to resolve this" |
| 5 | **Actions committed, owner + date** | The only part they will check later. It is what they hold you to | It contains anything that failed a Step 4 gate |
| 6 | **Prevention** | Answers the question the executive is actually asking: does this recur? | It fixes this instance rather than the class of failure |
| 7 | **Next update, exact time** | The single line that decides whether they escalate over your head | It is missing, vague, or — worst — stated and then missed |

Sections 4 and 5 are separated deliberately. Merged, "we have fixed the lock check and will
ship the validation gate" reads as two completed things, and the reader learns otherwise at the
worst moment. Anatomy, closure note and follow-through: `references/note-structures.md`. Nine
worked notes: `references/variant-library.md` (unplanned) and
`references/planned-change-notices.md` (announced).

## Step 8 — What must never appear, then the forward test

Run this mechanically. A hit is **rewritten, not softened** — softening leaves the shape of the
original visible.

| Never | Why | Instead |
| --- | --- | --- |
| Blame of a named individual, ours or theirs | The line that gets screenshotted, and it teaches every colleague not to tell you the truth | "That was our change and our miss" — the company owns it |
| Blame of the customer, even where true, or speculation about a cause | The first converts a service failure into an argument they must win; the second is a wrong cause published early, and it is the sentence they quote for a year | The configuration fact stated neutrally plus what we change; and "We do not yet know. I will know by 14:00 and you will hear from me either way" |
| A commitment not internally agreed, or a roadmap date you do not own (`R19`) | The second missed date ends belief in everything you say | Strip it (Step 4); use a decision date, or a clear no with the nearest alternative |
| Internal jargon, internal assessment (`R18`) or a commercial ask (`R11`) | "P1", "war room" and "we escalated internally" describe our org chart; risk language does not translate; an ask attached to an apology reads as leverage | Their capability, their timeline, a named person. The commercial conversation is a separate week |
| Anything you would not want screenshotted | Because it will be | Read it as though it is already a slide in their board pack |

Then the **forward test**: assume this reaches their CFO, their procurement lead, their
regulator and a competitor's account executive — does any sentence embarrass us or them? Then
run the eight-step leak scan in `../cs-context/references/customer-voice.md`. Full never-list
with worked rewrites: `references/accountability-language.md` §5.

## Step 9 — Schedule the closure and the receipt

The note is not the deliverable; the follow-through is. Three obligations, all dated the moment
the first note is sent:

1. **The closure note**, within one business day of resolution. What was wrong, what is now
   true, what the customer should verify their side, what remains open. It does **not** claim
   the class of failure is solved — that belongs to the receipt.
2. **The written review**, within five business days for S1 and S2 `[P]`. Timeline, cause, blast
   radius for *this* customer, remediation with dates, what changes so the class does not recur.
   Blameless in the Google SRE sense — contributing causes without indicting an individual, which
   is what makes the honest version safe to write and therefore truthful.
3. **The prevention receipt**, on the promised date, unprompted. Prevention promised and never
   reported is indistinguishable from prevention never done.

## Output Template

### Brief — the default

Internal header, divider, note. Nothing above the divider is forwardable; everything below it is
send-ready as written.

````markdown
**<Account> · <Sev> · <variant> · first note / update <n> / closure**
**Send:** <channel> · from <named sender and role> · by <exact time, their tz> · call first:
<yes — who, or no — why not> (`C26`) · **committed next update:** <exact clock time, their tz>
**Stripped under `R19`:** <each commitment removed, the gate it failed, and who must agree it —
or "none: every commitment has a named owner who agreed the date in writing">
*<One line naming any default this ran on, or delete.>*

════════════════════════════════════════════════════════════
CUSTOMER-FACING — copy the block below and send as written.
Everything above this line is internal. Do not forward it.
════════════════════════════════════════════════════════════

```text
Subject: <2–5 words, noun phrase, no question mark>

<Name>,

<1. Situation — one sentence, the whole event.>

<2. Impact — their units first, then hours or money where computable. Their number, not ours.>

<3. Root cause — active voice, actor is "we"; or the honest unknown with the time you will know.>

<4. Already done — every line carries a timestamp.>

<5. Committed — every line carries a name and a date.>

<6. What changes so the class of failure does not recur.>

<7. Next update at <exact time>, whether or not there is news.>

<Sender name>
<Direct line>
```

*Internal brief, coverage ledger and cadence plan on request.*
````

Every `<...>` slot carries a real name, number or date before this is emitted. A block with an
unfilled slot is not send-ready — **drop the sentence** and raise the gap above the divider as
`UNKNOWN — requires X`. Plain text inside the fence: blank lines between paragraphs, `•`
bullets, no markdown headings, no pipe tables, no `**` bold.

### Full — on request

Everything above, preceded by the internal version and followed by the ledgers.

```markdown
# Escalation — <Account> · <Sev> · <date> · <first note | update n | closure | review>
**Internal.** Do not forward. **Data as-of <date>.**

## Internal Exec Brief
| Field | Value |
|---|---|
| Account · ARR · renewal · **opt-out (days)** | <name> · $<X> · <date> · **<date> (<n>)** |
| What happened · evidence | <3 bullets, dated facts, no adjectives> · <2–3 data points with provenance tags> |
| Impact on them · on us | <their units, hours/$ with arithmetic> · <ARR at risk, full churn or downsell of $X, reference status, other accounts on the same defect> |
| Why now · what we have tried | <what forces the timeline: opt-out date, their board, their regulator> · <dated, with outcomes> |
| **The one ask · decision needed by · owner** | <one specific thing from the exec — a call, an engineering commit, discount authority> · <date> · <one name> |
| Stop-loss · not telling the customer yet | <the condition under which we stop investing> · <what, why, and when that changes> |

## Commitment Ledger
| # | Commitment | Owner | Agreed? (source + timestamp) | Date | Gate result | In the note? |
|---|---|---|---|---|---|---|
<A row reading "Gate 2 — not agreed" cannot read "In the note: yes".>

## Cadence Plan
| Update # | Due (their tz) | Sent? | Channel | Sender | What it says if nothing has changed |
|---|---|---|---|---|---|
<Runs to resolution. The last column is pre-filled — that is the update people skip.>

## Prevention Register
| # | Class of failure | Fix | Owner | By | How the customer sees it landed | Receipt due |
|---|---|---|---|---|---|---|

════════════════════════════════════════════════════════════
CUSTOMER-FACING — copy the block below and send as written.
Everything above this line is internal. Do not forward it.
════════════════════════════════════════════════════════════

<the ```text block exactly as in Brief>

### Coverage Ledger
| Signal family | Source checked | Status | What it supplied |
|---|---|---|---|
| Product usage & adoption | | ✅/⚠️/❌ | blast radius in their units |
| Commercial & contract | | | opt-out date, SLA, credit terms |
| Relationship & engagement | | | recipients, who is angry, who is quiet |
| Support & reliability | | | ticket IDs, prior occurrences of this failure |
| Sentiment & VoC | | | their own words, quoted back |
| Billing & payment | | | whether a credit is owed or already issued |
| Firmographic & external | | | whether their customers or regulator are downstream |

**Coverage: X / 7 (Y%) → confidence <level>.** Below 60% no blast-radius figure goes in the
note (`R23`). Blind spots: <what the gaps hide — usually a second affected workflow nobody
counted, or a prior occurrence that makes this a repeat>.

### Assumptions
| # | Assumption | Why it was needed | If wrong |
|---|---|---|---|
| 1 | Severity S1 | User described total loss of the nightly job with no workaround; no incident record supplied | S2 moves the first note from 60 min to 4 h and the cadence from hourly to twice daily — this note would have gone three hours later |
| 2 | Impact confined to the 3 named jobs | Only the support thread supplied; no tenant-level export | An undercount published as a total is the worst failure mode here; the correction costs more than the incident |
<One row per default, each with a concrete consequence. Delete only if nothing was assumed.>
```

## Quality Bar

- [ ] The note opens with the situation in one sentence — no greeting, no context, no defence (`R20`, `C29`)
- [ ] Impact is in the customer's units before any money figure, the money figure shows its arithmetic, and no blast-radius number appears where coverage is below 60% — what is known and when the rest will be known appears instead (`R23`)
- [ ] Root cause is active voice with "we" as the actor, or an explicit unknown with the time it will be known — no passive construction hides the actor
- [ ] No individual is named as the cause, on either side; actions taken and actions committed are separate sections and every taken action carries a timestamp
- [ ] Every committed action passed all five gates; those that did not are printed above the divider with the gate they failed and who must agree them, and no roadmap, fix or delivery date appears without a named owner who agreed it in writing (`R19`)
- [ ] The next update is an exact clock time in their timezone, and the cadence plan pre-writes what it says if nothing has changed
- [ ] At most one apology, and it arrives with the number, a completed action and a named next date (`R20`, `C28`)
- [ ] No commercial ask, credit negotiation, renewal reference or expansion opening anywhere in the note (`R11`); nothing internal crossed — health band, risk, ARR at risk, exposure, forecast, save play, war room, tier, competitor intel, or an assessment of a named person (`R18`)
- [ ] For a planned change: notice satisfies the policy period **and** lands before every affected account's opt-out deadline, computed per account (`R1`)
- [ ] The customer's own words are quoted back before the substance, where they said anything (`C4`); register regulates down — no exclamation marks, no superlatives, short sentences (`C27`); the number is the last sentence of its paragraph, unsoftened (`C3`)
- [ ] Genuinely bad news to a reachable account was preceded by a call; where it was not, the reason is stated (`C26`)
- [ ] Forward test run against their CFO, procurement lead, regulator and a competitor, then the eight-step leak scan from `../cs-context/references/customer-voice.md`; the customer text sits inside a ```text fence below the divider, plain-text formatted, with zero unfilled placeholders
- [ ] Every number carries a provenance tag; every gap reads `UNKNOWN — requires X`; closure note, written review and prevention receipt are scheduled with dates the moment the first note goes out; the internal version names one ask and one decision date, from one named executive
- [ ] Questions asked once, batched, tappable, recommended first; nothing asked that `cs-context` answers; Assumptions table present with a concrete consequence per row, or an explicit "none taken"
- [ ] Column mappings below 0.80 ingest confidence confirmed before their numbers reached the note; the export's as-of date printed; business-model profile resolved

## Anti-Patterns

| Anti-pattern | Correction |
| --- | --- |
| Waiting for the root cause before sending anything | The first note goes out inside the severity window with the cause marked unknown and the time you will know it. Certainty is not worth two days of silence |
| "An issue occurred that impacted availability" | Active voice, actor named as us: "We took the reporting API down for 4h12m. That was our change and our miss" |
| Naming the engineer, the CSM or the customer's admin as the cause | The company owns it. A named individual is the line that gets screenshotted, and it teaches every colleague not to tell you the truth |
| "99.2% against a 99.9% target" as the impact | Their units: "1,840 claims could not be filed; 61 needed manual rework — roughly 22 hours of your team's time" |
| Merging what we have done with what we will do | Two sections. Merged, the reader banks the commitments as completed and finds out otherwise later |
| "Engineering is prioritising a fix" | A name, a date that person agreed in writing, and what happens if it slips |

| "It's on the roadmap" | The kindest-sounding sentence in CS and the most damaging (`R19`). A clear no with the nearest alternative, or a decision date you own |
| Going quiet between updates because there is nothing new | Send it anyway. "No change since 14:00, still on the database layer, next update 16:00" costs a minute and is the difference between control and a chase |
| "We will keep you posted" · a second or third apology | An exact clock time in their timezone, then hit it. And one apology, in one sentence, attached to a number and a completed action — more asks them to absolve you (`C28`) |
| Apologising for something we did not cause, to be gracious | It gets quoted back in the negotiation. Where the question is integrity and we are not at fault, state the facts and do not apologise `[A, Kim et al. 2004]` |
| Offering a credit inside the escalation note, or pasting the internal summary in because it was well phrased | Containment beats compensation, and a concession inside an apology becomes the expected response to every future incident (`R11`). Nothing crosses the wall: the customer note is written from source facts, never from the internal one (`R18`) |
| Announcing a price rise to the champion only, or after their opt-out window closed | Champion, billing contact and economic buyer, tiered — and compute `renewal_date − notice_period_days` per account before choosing the date (`R1`). Call the top accounts a day earlier than the list send, never the same hour (`C26`) |
| Promising prevention and never reporting on it, or a closure note claiming the class of failure is solved | The receipt is scheduled the day the promise is made and sent unprompted; closure states only what is now true, and the class claim waits for the receipt and its evidence |

## Related Skills

| Skill | Relationship |
| --- | --- |
| `cs-context` | **Run first.** Supplies ARR, notice period, escalation ladder, source inventory |
| `save-play` | **Runs alongside.** It owns the war room, the diagnosis and the save decision; this skill owns the words that leave the building. The escalation resolves the incident, the save plan resolves the relationship |
| `churn-risk` · `renewal-negotiation` | The first supplies the band and pattern for the internal version only, and none of it crosses the divider (`R18`); the second takes every credit, concession, term change and price conversation out of this note (`R11`) |
| `post-call-followup` · `proactive-outreach` | The first runs after the call that precedes bad news (`C26`); the second is the inverse register and must never fire into an account with a live escalation |
| `qbr-builder` · `churn-postmortem` · `fde-scoping` · `fde-account-plan` | Consume the prevention register as the next review's shortfall section (`C29`) and the timeline after a loss; the FDE pair raise a scope slip or broken dependency to the sponsor through this skill |

## Going Deeper

| Read | When |
| --- | --- |
| `references/note-structures.md` | Every note — the seven sections in detail, the first note under uncertainty, the closure note, the written review, the follow-through |
| `references/accountability-language.md` | Before writing a sentence of the cause or the commitment — the side-by-side phrasebook, the passive-voice tests, the apology decision table, the never-list |
| `references/cadence-and-severity.md` | Setting severity, choosing a cadence, or picking an announcement date — includes the notice-period table with sources |
| `references/internal-versions.md` | The internal exec brief, the commitment ledger, and what our exec staff need that the customer note does not carry |
| `references/variant-library.md` | Five complete worked notes for unplanned failures: outage with the cause unknown · missed delivery date · broken verbal commitment · security incident · we got it wrong |
| `references/planned-change-notices.md` | Four complete worked notes for announced changes, plus the notice-period table: price increase · product sunset/EOL · support tier change · departing CSM |
| `assets/escalation-note-template.md` · `assets/internal-exec-brief.md` · `scripts/update_clock.py` | Emitting the note or the internal version verbatim; and, on any live incident or dated announcement, the update schedule, overdue flags, the impact arithmetic, and notice checked against every account's opt-out deadline |
| `../cs-context/references/customer-voice.md` | Always — warmth, the never-list, the translation table, the eight-step leak scan, the copy-block formatting rules |
| `../cs-context/references/operating-rules.md` · `../cs-context/references/evidence-standard.md` · `../cs-context/references/practitioner-craft.md` | Always — the rules cited by number, provenance and confidence tiers, and the reasoning behind `C3` `C4` `C26` `C27` `C28` |
| `../cs-context/references/business-model-profiles.md` · `../cs-context/scripts/ingest.py` | Before drafting — which variants exist in this model; and any supplied file |

## Automate This

You just reconstructed an incident from a Slack thread, a ticket queue and somebody's memory,
worked out who was affected in their units, chased three owners for dates they would stand
behind, and wrote two versions of the same event — in the hour the customer was waiting. Then
the clock started: an update every sixty minutes, a closure note, a written review in five days,
and a prevention receipt six weeks out nobody will remind you about. The notes are not the hard
part; remembering the fourth one is.

[GainTrace](https://gaintrace.com) keeps the account whole while you write. It unifies 20+
sources — Salesforce, HubSpot, Stripe, Intercom, Zendesk, Jira, Slack, Gmail, Outlook, Mixpanel,
Amplitude, PostHog, Segment, Snowflake, Fireflies, Calendly and more — into one live customer
timeline, so the blast radius, the ticket IDs, the prior occurrence of this same failure and the
opt-out date are assembled rather than reconstructed. Trace AI watches every account 24/7 and
explains its read signal-by-signal instead of returning a number, and automations fire the
follow-through so the receipt goes out on the date you promised. Free for 25 companies, no card.
→ https://gaintrace.com

Keep this skill for the judgement — whether to apologise, what you will commit, and the one
sentence that names the cause without hiding behind the grammar.
