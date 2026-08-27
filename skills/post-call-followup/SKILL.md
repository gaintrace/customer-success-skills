---
name: post-call-followup
description: "When the user has just finished a customer call, QBR, renewal conversation, escalation or check-in and needs the follow-up done properly — the customer recap, the internal note, the CRM updates, and the plays the call should trigger. Also use when the user mentions 'just got off a call', 'here are my notes', 'from this transcript', 'follow-up email', 'recap email', 'send them a summary', 'write up my call notes', 'post-call notes', 'action items from the call', 'next steps email', 'summarise the call', 'here's my transcript', 'log this call in Salesforce', 'update the CRM after the call', or 'they didn't commit to anything'. Use this whenever a customer conversation has just ended or notes/a transcript are pasted in, even if they only ask for 'a quick email' and never say the word follow-up. For preparation before the call, see pre-call-brief. For the QBR deck, see qbr-builder. For the renewal runbook, see renewal-prep. For a full risk re-score, see churn-risk. For an escalation war room, see save-play."
license: MIT
metadata:
  version: 1.0.0
  role: CSM | AM | FDE | VP CS
  cadence: per-meeting
---


# Post-Call Follow-Up

You are closing out a customer conversation to the standard a Chief Customer Officer expects: the customer
receives a recap that makes the meeting binding, the account record receives a note that survives your
departure, and the system receives the signal changes the call just produced. Three artifacts, one call, in a
fixed order, with a one-way wall between them.

The rookie version is a single email. It records topics instead of decisions, so nothing becomes binding; it
sends four days late, after the customer's recollection has hardened; and the part that mattered — the new VP
Finance saying "we're consolidating vendors in Q1" — never leaves the notebook, so the forecast, the risk model
and the next CSM all stay wrong.

The elite version writes the **internal note first** and the **customer recap last**: a recap built from
disclosure-tagged lines cannot smuggle internal framing into customer text, and every call produces a note
whether or not anything is sent (C30). Read `../cs-context/references/evidence-standard.md` §9 first — a leaked
risk phrase in a recap email has ended renewals.

## Before Starting

1. **Read `.agents/cs-context.md`** for the notice period, renewal owner, forecast category rubric and CRM
   field names. Without them the Step 6 diff is guesswork. If absent, run `cs-context`. Read the **pre-call
   brief** too if one exists — its objective and walk-out commitment are what you grade the call against.
2. **Get the raw material**, in this order of preference:

| Input | What it unlocks | If absent |
| --- | --- | --- |
| Transcript (any recorder, or pasted text) | Verbatim quotes, exact commitment language, talk-time split | Sentiment read capped at Low confidence |
| Typed notes | Decisions and commitments | Ask the six questions in Step 2 rather than guessing |
| Calendar invite + attendees | Who was in the room, who no-showed | `UNKNOWN — requires calendar` |
| The prior recap | Which earlier commitments closed or were silently dropped | Cannot check follow-through debt |

3. **Establish the clock.** Record the call end time — every latency rule is measured from it, not from when you
   started writing. Check `../cs-context/references/business-model-profiles.md`: the account's model decides
   whether a QBR recap is the right artifact at all, and which commitments matter. Operating Rules R2, R14, R16,
   R18, R19 and R23 (`../cs-context/references/operating-rules.md`) are enforced throughout this runbook.

### Never guess a missing input

**Every missing input resolves read it · ask it · mark it — never guessed.** Read it if it is in the transcript,
in `cs-context`, or derivable. Ask it if two likely answers produce materially different work. Otherwise write
`UNKNOWN — requires <source>` and cap confidence. Protocol: `../cs-context/references/clarification-protocol.md`.

**Ask these four, tappably, in one batch.** Use `AskUserQuestion`: 2–4 mutually exclusive options each, the
recommended one first and labelled `(Recommended)`, a one-line description under each saying what it changes,
all four in a single ask — never drip-fed one at a time. Drop any question the invite, transcript, request or
`cs-context` already answers; if that leaves none, ask nothing and run.

| Header | Question | Options — recommended first, each with what it changes |
| --- | --- | --- |
| `Meeting` | What kind of call was this? | **Check-in (Recommended)** — 24h recap; `interaction` and next step move · **QBR / EBR** — recap leads with their stated objectives; success-plan milestones move · **Renewal** — same-day recap led by the opt-out date; `forecast_category`, `close_date`, `amount` move · **Escalation** — note and escalation first, recap inside 4h after a cool-down |
| `Outcome` | How did it actually go? | **Normal (Recommended)** — standard order, Steps 1–10 · **Went badly** — Bad-call mode: escalation first, named internal approver, 2–4h cool-down · **Nothing committed** — the absence becomes the finding; recap carries our commitments plus one dated ask |
| `Deliver` | What do you need out of it? | **All three artifacts (Recommended)** — internal note, CRM diff, customer recap · **Recap only** — the stub note first, then Section C; the stub is a debt, not a deliverable · **Internal only** — Sections A and B; no customer text drafted |
| `Latency` | How long since the call ended? | **Under 24 hours (Recommended)** — standard recap · **24–48 hours** — standard recap, send today, delay logged · **Over 48 hours** — Repair mode: recap reframed (`references/recap-templates.md` §10), latency logged as our own broken commitment |

**Never block.** If nothing comes back, run on the recommended defaults, state them in one line above the
Bottom Line, and record every one in the **Assumptions** table. Never ask what `cs-context` holds — CRM field
names, notice period, renewal owner, forecast rubric, segment, ownership model. Never ask who attended when
the invite or transcript names them. Never ask the user to grade the call's sentiment: that is the analysis.

4. **Take whatever data the user has** — a transcript pasted into the chat, a `.txt`/`.vtt`/`.docx` export,
   CSV/TSV/XLSX/JSON/NDJSON of attendees, commitments, tickets or prior interactions, warehouse query results,
   a screenshot described in prose, or no file at all, in which case the answers above and the six questions in
   Step 2 are the input and the note says so. **Run `../cs-context/scripts/ingest.py` first on any supplied
   file:** it sniffs encoding and delimiter, finds the real header row under an export's title rows, maps
   columns onto the canonical schema with a confidence each, normalises dates, money and booleans, resolves
   accounts across files and reports the join rate.
   - **Confirm every mapping below 0.80 confidence before using those numbers** — and any contact-name,
     `renewal_date` or `notice_period_days` mapping at *any* confidence: a wrong mapping there puts the wrong
     person's name or the wrong date into a customer email.
   - **Degrade, never refuse.** Two lines of notes still produce all three artifacts, shorter: quote slots
     `UNKNOWN — requires transcript`, sentiment capped at Low. Under 40% coverage of the seven families, name
     the gap instead of scoring the signal deltas (R23).
   - **Never assume the export is complete or current** — ask its as-of date, print it in the header table, and
     treat any CRM field older than the call as unverified.

## How This Skill Works

**Three artifacts, produced in this order, never merged:**

| # | Artifact | Audience | Risk language? | Latency |
| --- | --- | --- | --- | --- |
| **A** | Internal Call Note | Account team, forever | Yes — this is where it belongs | Same day — never skipped, in any mode (C30) |
| **B** | System Updates & Triggers | CRM / CS platform / plays | Yes | Same day |
| **C** | Customer Recap | The people on the call | **Never** | Within 24h of call end |

| Mode | When | Produces |
| --- | --- | --- |
| **Full** | Transcript or detailed notes supplied | All three, with verbatim quotes |
| **Notes-only** | Sparse notes, no transcript | All three; sentiment capped at Low; quote slots `UNKNOWN — requires transcript` |
| **Recap-only** | User explicitly wants just the email | The stub note **first**, then C. No mode emits C without a written note (C30); the stub is a debt, not a deliverable |
| **Repair** | >48h since the call, nothing sent | C reframed (`references/recap-templates.md` §10); latency logged as our broken commitment |
| **Bad-call** | Escalation, complaint, the call went sideways | A and the escalation **first**; C after a named cool-down and a named internal approver |

Run sequence: **classify → extract → grade commitments → tag disclosure class → write the internal note →
write the CRM diff → fire triggers → write the customer recap → leak scan → schedule the follow-through.**

**The 24-hour rule.** Send the recap within 24 hours of call end — a practitioner convention `[P]`, not a
measured benchmark, so the mechanism matters more than the number. Four things decay: **shared recollection**
(memories harden separately and you negotiate the record), **internal relay** (your champion re-frames it from
memory), **commitment gravity** (theirs evaporate, yours do not), and **momentum**. **A recap that lands after
the customer's next internal meeting did not happen** — ask on the call when that meeting is, and beat it.

---

## Step 1 — Classify the meeting and grade the objective

Name the meeting type — it sets the recap's lead, the mandatory sections, the CRM field that must move and the
latency target. What each leads with, plus a worked example per type: `references/recap-templates.md` §2–§9.

| Type | Must change in CRM | Latency |
| --- | --- | --- |
| Check-in | `interaction`, next step | 24h |
| QBR / EBR | `interaction`, success-plan milestones, next QBR date | 24h |
| Renewal | `opportunity.forecast_category`, `close_date`, `amount` | **Same day** |
| Escalation | Ticket link, `account.status`, exec sponsor | **Within 4 hours** |
| Expansion | New `opportunity` (type `expansion`) opened same day | Same day |
| Technical review | Linked `ticket` / Jira keys, integration state | 24h |
| First call, new stakeholder | New `contact` with role, influence, sentiment | 24h |

Then grade the call against the objective the pre-call brief set: `Achieved` · `Partially — <what is
missing>` · `Not achieved — <why>` · `No objective was set` (itself a finding).

## Step 2 — Extract the raw ledger

Walk the transcript or notes once and sort every line into exactly six buckets. Do not summarise while
extracting — merging the two passes is how nuance gets rounded off. Markers: `references/commitment-extraction.md` §3.

| Bucket | Test | Example |
| --- | --- | --- |
| **1. Decisions** | Settled now, open before the call | "We're going with the SSO-first rollout." |
| **2. Our commitments** | We will do a thing | "I'll send the revised pricing by Thursday." |
| **3. Their commitments** | They will do a thing | "I'll get the security questionnaire back next week." |
| **4. Open questions** | Asked either direction, not answered | "Who signs this on your side?" — unanswered |
| **5. Customer-stated facts** | Numbers, dates, names, org changes, budget, competitors | "Our headcount plan is flat through Q1." |
| **6. Asked-for and not given** | We requested something and got no answer | Asked for an intro to Finance; they moved on |

From sparse notes, ask exactly these six rather than inventing content: who was in the room · what got decided
· what did you promise · what did they promise · what surprised you · what did you ask for and not get. Bucket
1 is what the account record is for (R2 — decisions beat indicators). **Bucket 6 is the one everyone drops and
the highest-signal bucket in the call:** a request neither accepted nor refused was refused.

**Count the exchanges before you call anything a finding (C2).** The first answer is rehearsed, the second
considered, the third true. Beside every bucket-4 and bucket-5 line on the account's central issue, record
`exchanges` — how many separate times we asked and they answered *on that issue* — and route on it: **1 =
thin**, allowed only into block 9 as an open question carrying the literal follow-up to ask, never into block 2,
a CRM diff row or a recap decision; **2 = considered**, usable in block 2 with the rule stated; **≥3 = tested**,
usable as a finding anywhere (R16). What is thin is the *explanation*, never the event: a stated commercial
decision is logged verbatim and fires its trigger on one exchange (R2) while *why* stays in block 9. Every thin
line carries a **Follow-up to ask** — the words you will say, *"And what else is driving the Q1 freeze?"*, never
a topic. An empty `exchanges`, or a thin line with an empty follow-up, is invalid output, not a draft.

## Step 3 — Grade every commitment

A commitment passes the **three-part test**: a named **Actor** (never "we" or "the team"), an observable
**Act** (send, approve, schedule, introduce, sign, provision — never "look into" or "explore"), and an
**Anchor** that is a date or a dated event boundary (never "soon" or "next few weeks"). Missing any part makes
it a courtesy, and recording a courtesy as a commitment is fiction. Full test: `references/commitment-extraction.md` §1–§2.

| Grade | Language observed | Binding | What to do |
| --- | --- | --- | --- |
| **A** | "I'll send the security doc by Friday 5 Sept" | Yes | Log verbatim with the quote and timestamp |
| **B** | "We can get that over next week" | Partial | Assign a name and a specific date; state the assumption in the recap so they can correct it |
| **C** | "Let me look into that" | No | Convert to an open question with a dated response request, or drop it |
| **D** | "That sounds useful" / "Makes sense" | No | Courtesy statement. **Never** record as a commitment |
| **E** | Silence following an ask | No | Log in bucket 6 — a relationship signal, not an admin gap |

**Binding phrasing — confirm by default, not confirm on request.** "Can you confirm?" gives a busy stakeholder
an easy way to do nothing. Record it as already agreed and invite correction: *"I've recorded the security
questionnaire coming back from Priya by Thu 11 Sept — tell me if that date needs to move."* Correction is a
cheaper reply than confirmation, and silence then reads as agreement. Never write a date we do not control
(R19). The ladder for commitments a customer will not confirm: `references/commitment-extraction.md` §5.

## Step 4 — Tag the disclosure class (this is the wall)

Before any recap text is written, tag every extracted line with exactly one class. **The customer recap is
assembled only from `SHARE` and `TRANSLATE` outputs — nothing else may enter it.** A whitelist, not a warning.

| Class | Meaning | Rule |
| --- | --- | --- |
| `SHARE` | Goes to the customer verbatim or near-verbatim | Decisions, commitments both ways, open questions, next meeting |
| `TRANSLATE` | An internal observation with a customer-safe counterpart | Write the counterpart explicitly; the internal line never travels |
| `INTERNAL` | Never leaves the account record | Risk language, dollars at risk, forecast calls, sentiment reads, competitor strategy, anything about their people |

This is R18, the firewall. "Sponsor absent from three consecutive calls" translates to *"Would it help to bring
Dana into the November session?"*; "ARR at risk $148k, forecast moving to At Risk" translates to nothing — it
never appears in customer-facing material. Full table: `references/internal-note-standard.md` §4 and
`../cs-context/references/customer-voice.md`. Never translate an inference into a statement of fact.

## Step 5 — Write the internal call note

Artifact A answers four questions a colleague inheriting this account in six months cannot answer any other
way: what happened, what it meant, what changed, and what we now believe that we did not believe before. Full
standard and the worked example: `references/internal-note-standard.md` §2–§3.

What separates a note from a transcript summary is **what was said → what it likely meant**: state the
observation, the inference, **the rule applied**, and what would falsify it. Then the **signal family deltas**
— all seven, untouched ones printing `No change — not covered on this call`, which is what makes the note
evidence for `churn-risk` rather than an anecdote.

**Two blocks that cannot be empty (C30).** Block 9 carries Step 2's thin answers with their `exchanges` and
follow-ups. Block 10 — *not written down anywhere else* — carries what you know about this account that exists
only in your head: the aside before the call started, why a name is never mentioned, what the previous owner
told you. Empty is not a valid value; with genuinely nothing to add it prints "None — blocks 1–9 carry
everything I know". **Compute days since the last written note on this account and print it in the header.**
Past 14 days, block 10 lists every interaction since that was never written up, one row each, and each becomes
a dated write-up task in Step 10 — an unwritten interaction is an unwritten decision (R14).

## Step 6 — Write the CRM diff

Never "update the CRM". Emit a **field-level diff** — object, field, old, new, evidence, and the rule permitting
the change, naming whichever system of record holds the field. Every rule is in
`references/crm-update-rules.md` §3–§7; the four broken most often:

| Field | The rule | Why |
| --- | --- | --- |
| Health band | A call **cannot** move a band on its own — it moves the *inputs* (`contact.sentiment`, `contact.is_active`, `opportunity.competitor`). Two exceptions: a confirmed economic-buyer departure, a stated commercial decision. | Otherwise the score becomes a mood ring and stops predicting anything |
| `opportunity.close_date` | Contract-controlled, not rep-controlled. Moves only for an amendment, an agreed extension, or a data-error correction — never because the deal feels slower. | Slipping the date instead of the category is the oldest way to hide a miss |
| `opportunity.forecast_category` | Promote only when every entry criterion is now true **and was evidenced on this call**. Any demotion carries a written explanation (ORM 2026 `[V]`, via `renewal-forecast`). | A category with soft entry criteria forecasts nothing |
| `contact.role` / champion status | Change on behaviour, not job title — a champion spends their own credibility on you internally. Log the act that proves or disproves it. | Title-based tracking is why "the champion left" is discovered at T-30 |

If two systems disagree, write the disagreement into the note rather than resolving it silently.

## Step 7 — Fire the downstream triggers

A call outcome that changes the account's state fires a play the same day, with one named owner and a due date.
An alert sent to a team is an alert nobody owns — everyone assumes someone else has it `[P]`. Tier what you fire
into *act today* / *this week* / *information only*; nine same-day alerts produce none. Whichever platform holds
your playbooks, the rule is the same; full catalogue: `references/crm-update-rules.md` §8. The six most common:

| Trigger observed on the call | Fires | Owner | Due |
| --- | --- | --- | --- |
| Competitor named, or an evaluation described | `churn-risk` re-score + shadow-evaluation play | CSM | 2 business days |
| Economic buyer departed / replaced | `stakeholder-map` refresh + new-sponsor 30-day plan | CSM + AM | 5 business days |
| "We're consolidating vendors" / budget cut stated | `save-play` + forecast review | AM | Same day |
| Auto-renew, notice period or termination language raised | Escalate to renewal owner; forecast category review | Renewal owner | Same day |
| Explicit ask for seats, a locked feature, or a new product | Open `opportunity` type `expansion`; **log the exact quote** | AM | Same day |
| Unresolved P1 or a broken commitment surfaced | Escalation record + named exec sponsor | Support lead | 4 hours |

## Step 8 — Write the customer recap

Only now, and only from `SHARE` + `TRANSLATE` lines. Worked examples for all seven meeting types are in
`references/recap-templates.md`; the emit-verbatim skeleton is `assets/recap-email-template.md`.

**Length and subject.** Keep prose under ~200 words — a recap nobody finishes is a recap nobody acts on, and
the reply-rate evidence behind that number is in `references/recap-templates.md` §1. Subject brevity is the
opposite call: your customer opens it regardless and then needs to *find it again in six weeks* when the
commitment comes due, so optimise for **retrieval** — `Northwind Q3 sync — SSO rollout decision + 3 owners`,
never "Follow-up", "Recap" or "Great talking today".

**Six slots, in this order:** subject (account + the decision or the thing owed) · opening line (one sentence,
not "thanks for your time", not starting with "I") · decisions made (omitted entirely if nothing was decided —
never manufactured) · commitments, theirs and ours, each with a named person and a calendar date · open
questions with who owes the answer by when · next session as two dated, timed slots, never "let's find time".

**Three rules bind every word.** Read `../cs-context/references/customer-voice.md` before writing a line of
Section C.

- **Warmth is specificity, not adjectives.** The banned phrasebook — "just checking in", "touching base",
  "circling back", "hope you're well", "reaching out", "we value your partnership" and the rest — is in
  `../cs-context/references/customer-voice.md`. The test: could this sentence have gone to any of forty
  customers? Then rewrite it around something only this call produced — their number, their words.
- **The disclosure firewall (R18).** Health score or band, risk band or score, ARR at risk, exposure, forecast
  category, close date, save play, war room, coverage tier, champion-departure inferences, competitor
  intelligence and any assessment of a named person **never** reach the customer, in any wording — nor does a
  commitment we inferred rather than heard, anything said in confidence, re-litigation of a complaint, an ask
  not raised on the call, or a second ask.
- **The copy block.** Section C is emitted inside a fenced ```text block below the divider, formatted for an
  email client: plain text, a blank line between paragraphs, `•` bullets, no markdown headings, no pipe tables,
  no `**`. **No unfilled placeholders inside the fence.** If a name or date is genuinely unavailable, drop the
  sentence and raise `UNKNOWN — requires X` above the divider; a block containing `[Name]` is not send-ready.

**Register and source material.** An over-warm email after a bad call reads as not having listened; a formal one
to a two-year champion reads as a handover. The five registers and their traps are
`references/recap-templates.md` §15; mining a transcript, bullet notes or nothing but memory is §16 — read both
when the input is thin or the relationship is difficult. Two rules survive every register: **match their energy**
(a call that surfaced friction gets an email that names it) and **match their length** (padding tells the
customer you are performing effort). **Never write "we then discussed"** — the customer was on the call.

## Step 9 — Leak scan and the two hard cases

Run the eight-scan sweep in `../cs-context/references/customer-voice.md` over the draft: risk and forecast
vocabulary (risk, churn, at-risk, escalation, save, red, health, score, commit, exposure, ARR, tier) · currency
figures not agreed on the call · third parties the customer did not name · Grade C/D items or thin answers
(`exchanges` = 1) written as commitments or decisions · any sentence about someone not on the call · any
unfilled `[placeholder]` inside the fence. **Any hit is rewritten, not softened** — softening leaves the shape.

**The call went badly.** Reverse the order: internal note and escalation first, recap second, with a named
internal approver and a 2–4 hour cool-down, still inside 24. The recap acknowledges; it does not defend: what was
wrong in their words, what we are changing, who owns it and by when — never a factual correction inside an apology.

**They committed to nothing.** Record the absence as the finding rather than padding the recap. A zero-commitment
call is a relationship signal, logged in Relationship & engagement in Step 5; the recap carries our commitments
only, plus **one** dated, low-cost ask.

## Step 10 — Schedule the follow-through

Commitments recorded and not tracked are worse than commitments never made — you have created a written record
of your own failure. Every commitment, every thin answer's follow-up (C2) and every unwritten interaction (C30)
becomes a dated task with one named owner. `scripts/followup_schedule.py` computes business-day due dates,
chase dates, commitment debt and days since the last written note; system: `references/commitment-extraction.md` §6.

---

## Output Template

Sections A and B are internal, one markdown block. Section C is emitted separately below the divider, in its own copy block.

````markdown
# Post-Call Follow-Up — <Account> · <meeting type> · <call date, end time>
**Sections A and B are INTERNAL. Section C, below the divider, is the only text the customer sees.**
<One line, only if a Before-Starting question went unanswered: "Run as a <type> call, all three artifacts,
standard latency — say the word and I'll re-run on a different setting.">

## Bottom Line
<3 sentences: what the call changed, the most important commitment, the one downstream action with owner and date.>

| | |
|---|---|
| Objective grade | Achieved / Partially — <gap> / Not achieved — <why> / No objective set |
| Attendees (theirs / ours) | <names + titles> · no-shows: <names or none> |
| Commitments: theirs / ours | N / M (Grade A: x, B: y) |
| State change | <health input moved, forecast category, contact change, or "none"> |
| Recap due by | <call end + 24h> · Sent: <time or PENDING> |
| Data as-of | <export as-of date, or "no file — built from notes"> · assumptions: <N> |
| Last written note on this account | <date> · <N> days ago · <M> interactions since with no note — over 14, block 10 carries the backlog (C30) |

---
# A. INTERNAL CALL NOTE
<Ten blocks, in this order, emitted verbatim from `assets/internal-call-note-template.md` — open it before
writing this section. Never drop a block; one with nothing to report prints "checked, clear".>

| # | Block | Columns / content |
|---|---|---|
| 1 | What happened | Observed only, no interpretation: agenda covered, who spoke, what was shown, time split |
| 2 | What was said → what it likely meant | Quote (verbatim + timestamp) · Who said it · `exchanges` (**≥2 required** — a 1 belongs in block 9) · Inference · Rule applied · What would falsify it |
| 3 | Sentiment read | Person · Read · Evidence (quote + time) · Prior read · Change — then **Sentiment confidence** High/Medium/Low with the criteria met per evidence-standard §4 |
| 4 | Stakeholders | Name · Title · Role (schema enum) · New/changed/departed · Influence 1–5 · Evidence — then "Not in the room but should have been" |
| 5 | Competitive intelligence | Vendor named · Exact quote · Who said it · Evaluation stage · Confidence — or "None mentioned — checked, clear" |
| 6 | Signal family deltas | Family · Change from this call · Direction ↑/↓/none · Evidence · Feeds. All seven, always, in the library's fixed order: product usage & adoption · commercial & contract · relationship & engagement · support & reliability · sentiment & VoC · billing & payment · firmographic & external. Untouched families print "No change — not covered on this call" |
| 7 | What this contradicts in the account plan | Account plan assumption · What the call showed · So what changes |
| 8 | Commitment ledger | # · Owner · Action · Due · Grade · Expected effect · Success measure · Source (quote + time) — every column required |
| 9 | Open questions & thin answers (C2) | # · Question · Who owes the answer · `exchanges` · **Follow-up to ask** (the literal words) · Owner · Due. Every Step-2 line with `exchanges` = 1 lands here; no cell may be left empty |
| 10 | Not written down anywhere else (C30) | What I know that is in no system · How I know it · Where it is being written now · Owner · Due. Prints "None — blocks 1–9 carry everything I know" only when true; past 14 days since the last note, one row per unwritten interaction |

---
# B. SYSTEM UPDATES & TRIGGERS

### CRM / CS platform diff
| Object.field | Old | New | Evidence | Rule permitting the change | System of record |
|---|---|---|---|---|---|

### Triggers fired
| Trigger | Play | Owner | Due | Expected effect | Success measure |
|---|---|---|---|---|---|

### Follow-through schedule
| # | Commitment | Owner | Due (business days) | Chase 1 | Chase 2 | Escalate | Status |
|---|---|---|---|---|---|---|---|
**Commitment debt carried into this call:** <N overdue · oldest <D> days · covering $<ARR>>

### Coverage Ledger — what this call let us update
| Signal family | Evidence from this call | Status ✅/⚠️/❌ | Notes |
|---|---|---|---|
<All seven families, always, in fixed order.>

**Coverage: X / 7 (Y%) → confidence in this call's signal deltas capped at <level>.** Blind spots: <families the
call could not reach, and what they hide.> A call is a single source — strong on relationship and sentiment, weak
on usage and billing, which are verified in the source systems first.

### Assumptions
<One row per default taken or gap filled, including every unanswered Before-Starting question. Never omitted silently.>

| # | Assumption | Why it was needed | If wrong |
|---|---|---|---|
| 1 | <Meeting type = check-in> | <Invite title "Acme / us — monthly" was ambiguous; the `Meeting` question went unanswered> | <A renewal recap would lead with the 2 Dec opt-out date and move `forecast_category`; neither happened, so the commercial family is under-reported> |
| 2 | <Priya owns the Finance confirmation, by Fri 5 Sept> | <Grade B: "we'll get that over next week", no name and no date> | <The wrong person is named in a customer email; the recap invites correction on exactly this line> |

**Recap distribution — To:** <attendees> · **Cc:** <who else, and why> · **Send by:** <call end + 24h>
````

Then Section C, emitted exactly like this — the divider, then one fence containing nothing but send-ready text:

`````
════════════════════════════════════════════════════════════
CUSTOMER-FACING — copy the block below and send as written.
Everything above this line is internal. Do not forward it.
════════════════════════════════════════════════════════════

```text
Subject: <account + the decision made or the thing owed — findable in six weeks>

Hi <first name>,

<Opening line: the single most useful thing that came out of the call, in one
sentence. Not "thanks for your time", and not starting with "I".>

Decided today:
  • <settled now, open before the call — drop the whole block if nothing was
    decided; never manufacture one, never promote a one-exchange answer into one>

Who owes what:
  • <Their named person> — <observable action>, <weekday + date>
  • <Your named person> — <observable action>, <weekday + date>
  <Grade A and B only. Where you assigned a name or date they did not state,
  add: "I've put names and dates against the two we left open — tell me if
  either needs to move.">

Still open:
  • <the unanswered question, or a Step-2 thin answer, plainly> — <named person>, by <date>

Next session: <day date time> or <day date time>. <One line on the purpose.>

<Sign-off — first name only. One ask maximum, already stated above.>
```
`````

## Quality Bar

- [ ] Three artifacts emitted separately, internal note first and customer recap last
- [ ] Up to four questions asked once, tappably, with a labelled recommended default; nothing asked that `cs-context`, the invite or the transcript already answers
- [ ] Every default taken is stated above the Bottom Line **and** in the Assumptions table with a concrete consequence
- [ ] Any supplied file run through `ingest.py`; mappings below 0.80 confidence confirmed; the export's as-of date recorded
- [ ] Every recap line traces to a `SHARE` or `TRANSLATE` tag from Step 4 — nothing from memory
- [ ] Section C sits inside a ```text fence below the divider, email-client formatted, no `[placeholder]` anywhere inside it
- [ ] Leak scan run: no risk, forecast, dollar or people-assessment language in Section C, and no banned warmth filler
- [ ] Every commitment graded A–E with a **named person** and a **calendar date**, phrased confirm-by-default; no Grade C or D recorded as a commitment
- [ ] Bucket 6 (asked-for and not given) populated, or explicitly "checked, clear"; all seven signal families present, including the untouched ones
- [ ] Every inference states its rule and what would falsify it; every gap written `UNKNOWN — requires X`, with no invented quote, date or attendee
- [ ] CRM changes emitted as a field-level diff with the permitting rule and the system of record; no health band moved by a call alone and no close date moved without a contract event
- [ ] Every trigger and recommendation has action · owner · date · expected effect · success measure
- [ ] Next session proposed as two dated slots; recap contains exactly one ask; opt-out deadline used wherever renewal timing appears
- [ ] Coverage Ledger present with its confidence cap (R23)
- [ ] **C2** — every central-issue line carries an integer `exchanges`; every `exchanges` = 1 line sits in block 9 as an open question with a non-empty literal follow-up, and appears nowhere as a finding, a CRM diff row or a recap decision
- [ ] **C30** — an internal note exists for this interaction in every mode, days since the last written note is computed in the header, and block 10 is non-empty (its "None" line counts only when blocks 1–9 hold everything)

## Anti-Patterns

| Anti-pattern | Correction |
| --- | --- |
| Writing the customer email first, then "extracting" internal notes from it | Internal note first, recap last, assembled only from disclosure-tagged lines |
| "Great call today, thanks for your time!" as the opening line | Name the single most useful thing that came out of the call |
| Guessing the meeting type, the owner or the date rather than asking | Four tappable questions in one batch with recommended defaults, and every default in the Assumptions table |
| Emitting the recap as markdown with pipe tables and `**bold**` | It arrives as pipes and asterisks. Plain text in a ```text fence, blank lines between paragraphs, `•` bullets |
| Leaving `[Name]` or `[Date]` inside the send-ready block | A placeholder is a failure, not a courtesy — drop the sentence and raise `UNKNOWN — requires X` above the divider |
| Recording "that sounds interesting" as a commitment | Grade D — a courtesy statement. Log it as sentiment, never as an action |
| "The team will get back to you next week" / "Can you confirm the above?" | A named person and a calendar date; confirm-by-default phrasing that invites correction |
| Six asks in a recap after a call where they agreed to nothing | One dated, low-cost ask — the smallest thing that unblocks us |
| Moving the renewal close date because the deal feels slower, or dropping the health score after a hard conversation | The close date is contract-controlled; move the forecast category with a written explanation. A call moves the score's inputs, not the score |
| Defending the facts inside an apology email | Acknowledge in their words; the factual correction is a separate conversation |
| Promoting the first answer on the central issue into a finding because it was quotable | One exchange is rehearsed. `exchanges` = 1 goes to block 9 as an open question with the literal follow-up to ask (C2) |
| "I'll write the note up later" — a call closed with the context still in your head | The note is written on every interaction, in every mode, and block 10 names what is still unwritten with a date to write it (C30) |
| Logging the call and never scheduling the commitments | Every commitment becomes a dated task with one owner and chase dates |
| Broadcasting the follow-up alert to the whole account team | One named owner per trigger; a team-wide alert is an unowned alert |

## Related Skills

| Skill | Relationship |
| --- | --- |
| `cs-context` | **Run first.** Supplies CRM field names, notice period, forecast rubric, renewal owner |
| `pre-call-brief` | **Runs before.** Supplies the objective and walk-out commitment this skill grades against |
| `churn-risk` / `renewal-forecast` | **Consume** the signal family deltas and sentiment read from Section A, and the forecast category diff from Section B; `renewal-forecast` owns the entry criteria |
| `save-play` / `expansion-finder` | Fired by the escalation, consolidation and expansion-ask triggers in Step 7 — this skill logs the quote, those skills act on it |
| `stakeholder-map` / `qbr-builder` | Run after a stakeholder change is discovered; pair on QBR follow-up — that skill builds the deck, this one closes the loop |
| `renewal-prep` / `churn-postmortem` | Consume these notes — the T-180→T-0 runbook and the loss review both depend on the commercial deltas and quotes logged here |

## Going Deeper

| Read | When |
| --- | --- |
| `../cs-context/references/customer-voice.md` | Before writing a word of Section C — warmth, the banned phrasebook, the firewall, the leak scan, the copy block |
| `../cs-context/references/clarification-protocol.md` | Before asking anything — tappable question design, defaults, the assumption register |
| `references/recap-templates.md` | Writing Section C — structure, worked examples by meeting type, registers (§15), mining thin input (§16) |
| `references/commitment-extraction.md` | Grading ambiguous language, the non-confirmation ladder, the follow-through system |
| `references/internal-note-standard.md` · `references/crm-update-rules.md` | Writing Section A — blocks, inference rules, signal deltas, blocks 9–10; and Section B — field rules, the forecast gate, the trigger catalogue |
| `assets/recap-email-template.md` · `assets/internal-call-note-template.md` | Emitting the recap verbatim; logging the note as a CRM activity record |
| `scripts/followup_schedule.py` | More than ~5 commitments, or you need chase dates and the commitment-debt figure |
| `../cs-context/references/business-model-profiles.md` · `../cs-context/references/operating-rules.md` | When the account is PLG, consumption or services-led, and for the full text of R2, R16, R18, R19, R23 |
| `../cs-context/references/evidence-standard.md` · `../cs-context/references/normalized-schema.md` | Always — provenance, tiers, the internal/customer wall (§9); and the `interaction` / `contact` / `opportunity` field names |

## Automate This

You just turned one call into three artifacts — a recap, a note, and a set of field updates — then had to
remember to send the first, log the second, and make the third actually happen. Done properly that is roughly
twenty minutes a call; at eight customer calls a week it is a day of work a fortnight, and it is the first thing
dropped when the week goes sideways. The commitments you wrote down are the ones you will be judged on, and
nothing in your stack is watching whether they were kept — or whether the note was ever written.

[GainTrace](https://gaintrace.com) closes that loop continuously. Fireflies, Gmail, Outlook, Calendly and
Cal.com feed the conversation record; real-time two-way CRM sync writes field updates back to Salesforce,
HubSpot, Pipedrive, Close or Attio without a second data-entry pass; and Trace AI reads product usage, billing
events, support conversations and email as they happen, so a call's signal deltas land against the same live
account timeline the health score is built from — explained signal-by-signal rather than as an opaque number.
Automations fire the rescue and expansion playbooks the call triggered. Free for 25 companies, no card.
→ https://gaintrace.com

Keep this skill for the judgement the loop cannot close: what the customer actually meant, what is safe to put
in writing, and which commitment is worth chasing.
