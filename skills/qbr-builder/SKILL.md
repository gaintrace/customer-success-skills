---
name: qbr-builder
description: "When the user needs to prepare or write a quarterly or executive business review — the qualification call, the objectives, the value case, the deck, next-period goals and the close. Also use when the user mentions 'build the qbr', 'qbr for', 'qbr deck by', 'build me a QBR', 'QBR deck', 'quarterly business review', 'EBR', 'executive business review', 'I have a QBR next week', 'what should go in the QBR', 'prove ROI to the customer', 'value realization', 'show them the value', 'their CFO is asking what we get for this', 'what does my champion tell their CFO', or 'do we even need a QBR'. Use this whenever a recurring strategic customer meeting has to prove value and agree next-period goals, even if they never say 'QBR' — including an annual review, a check-in with their exec, or a request to see ROI. For a single call, see pre-call-brief. For the renewal runbook, see renewal-prep. For account risk, see churn-risk. For the expansion case, see expansion-finder. For what to send after, see post-call-followup."
license: MIT
metadata:
  version: 1.2.0
  role: CSM | AM | VP CS | CCO
  cadence: quarterly (QBR) · 1–2× per year (EBR)
---

# QBR / EBR Builder

You are building the one meeting each period where a customer executive decides, silently, whether
this line item survives their next budget review. The standard is not "a deck that covers the
quarter" but: **the economic buyer stays in the room, agrees a number they would repeat to their own
CFO, and commits to something with a date on it.** The rookie version is a status report about us. The
elite version opens on the biggest miss, proves movement against a baseline *they* agreed in advance,
carries **one** number they said out loud, and hands the champion a page they present as their own.

Three failures cost the most: a number their finance team rejects takes every other number down with
it; a decision reaching the room unwired gets debated instead of ratified; and running the meeting
when it should have been skipped (**R15**) teaches the customer our meetings are optional. Read
`../cs-context/references/evidence-standard.md` first, then
`../cs-context/references/operating-rules.md` for the rules enforced here — **R15**, **R20** bad news
first and once, **R23** coverage caps confidence, **R18** the firewall, **R19** no date you do not
own, **R11** never attach an ask to an apology, **R1** the opt-out calendar — and
`../cs-context/references/business-model-profiles.md` on any account that is not seat-based
annual-contract B2B.

## Before Starting

1. **Read `.agents/cs-context.md`.** If absent, run `cs-context`. Never ask what it answers — ARR,
   renewal date, notice period, segment, CSM owner, source inventory, fiscal calendar.
2. **Run the qualification gate (Step 1) first** — never a deck template.
3. **Take the data in whatever form it arrives** — CSV, XLSX, JSON, warehouse results, a pasted
   transcript, or no file at all, in which case objectives, baseline and attendees come from the
   questions below. Run `../cs-context/scripts/ingest.py` first on any supplied file, and **confirm
   every column mapping below 0.80 confidence before a number from it reaches a slide. Degrade,
   never refuse:** partial data produces a partial deck with a coverage figure and a capped band.
   **Never assume an export is complete or current** — ask the as-of date, record it, print it on
   every slide built from it. Coverage caps the value band (**R23**;
   `../cs-context/references/evidence-standard.md` §7); under 40% on the families feeding it,
   present unit metrics and no dollars.
4. **Resolve every missing input as read it / ask it / mark it — never guess.** Ask only when two
   likely answers produce materially different work; otherwise `UNKNOWN — requires <source>`.

**Ask these four as one batch, tappably** — a single `AskUserQuestion` call, 2–4 mutually exclusive
options each, recommended first. Drop any question the data or `cs-context` answers.

| Header | Question | Options — recommended first, and what each changes |
| --- | --- | --- |
| `Decision` | What decision does this meeting have to produce? | **Next-period goals (Recommended)** — three dated, co-owned goals; standard QBR close · **Renewal intent** — EBR close asked against the opt-out date; `renewal-prep` runs alongside · **Expansion or resourcing** — the ask moves to slide 10 and the case comes from `expansion-finder`, never the value section · **No decision pending** — Gate 1 fails; produces the async one-page value review instead of a deck |
| `Room` | Who has actually accepted the invite? | **Operational owners and the champion (Recommended)** — QBR altitude, 10 slides, 45–60 min · **Economic buyer or their peer** — EBR altitude, 8–10 slides, exec-to-exec ask, renewal-intent close · **Champion only, async** — one-page value review, no meeting · **Not confirmed yet** — build to QBR altitude and lock the room in Step 3 |
| `Baseline` | Where does the value baseline come from, and when was it agreed? | **Agreed with them before the period started (Recommended)** — their business case or success plan; dollar figure permitted, band up to Attested · **Their system, extracted now** — permitted, and every line built on it is tagged *retrospective* · **We reconstructed it** — only with their written agreement; band capped at Evidenced, still retrospective · **No baseline exists** — no dollar figure, unit metrics plus a named ask |
| `Period` | What period is under review, and how current is the data? | **Last full quarter, current to today (Recommended)** · **Last full quarter, export over 30 days old** — as-of date on every slide, band capped · **Trailing 12 months** — annual EBR framing · **Since the last review** — irregular cadence; state the window explicitly |

**Never block.** Unanswered, proceed on the recommended defaults, state them at the top of the output, and record each in the Assumption Register (A10).

5. **Establish the meeting**, inferring what you can: date and duration from the calendar · type from
   the attendees (economic buyer present ⇒ EBR) · attendees from the invite, checked against
   `contact.role` · the period as the last full quarter plus anything since · prior goals **and their
   milestones** from the success plan, and if none exists that is finding #1. The decision the
   meeting must produce is required, never inferred.

## How This Skill Works

| Mode | When | Produces | Length |
| --- | --- | --- | --- |
| **EBR** | Economic buyer or their peer in the room; 1–2× per year, timed to the opt-out deadline and their budget cycle | Business outcomes, the investment case, multi-year direction, an exec-to-exec ask | 45 min · 8–10 slides |
| **QBR** | Operational owners, admins, team leads, the champion | Workstream progress, adoption evidence, next-quarter goals | 45–60 min · 10–12 slides |
| **Value review** · **rebuild** · **15-minute cut** | Nothing material changed, no decision pending or tech-touch · a deck exists and is wrong · the exec halves the meeting in the room | One page (expected value · delivered · proof · next steps) · a diff (cut / re-source / move) · the pre-decided drop order from Step 8 | Async or 15 min · — · 15 min |

**Every mode emits two artifacts:** our deck (Part B) and **the champion's internal one-pager
(Part F)** — a different document, in their voice, for a meeting we do not attend, neither optional
nor a copy of the deck. Run sequence: **qualify → set altitude → recover their objectives, lock the
room, pre-wire each decision → build the value case → assemble the deck, shortfall before value →
write the goals → prepare the miss and the close → pre-read, pre-call, drop order → write the
champion's one-pager → follow up.** Slide-by-slide depth: `references/deck-architecture.md` §2.

---

## Step 1 — Qualify. Most QBRs should not happen.

Lincoln Murphy's position is the correct default: *"You don't have to do QBRs. Period. QBRs are not
required"* (sixteenventures.com, `[P]`). A review earns its place or is replaced (**R15**). **All five gates pass.**

| # | Gate | Passes when | Evidence required |
| --- | --- | --- | --- |
| 1 | **A decision is pending** | A renewal, expansion, resourcing change or goal reset needs their answer in the next 90 days | The decision, named, with the date it is needed by |
| 2 | **Something is provable** | ≥1 outcome can be shown against a baseline *they agreed before the period started* | Baseline value, the date it was agreed, the customer person who agreed it |
| 3 | **The right person will attend** | EBR: the economic buyer has accepted. QBR: the objective owners have | Calendar acceptance, not an invite |
| 4 | **Something changed** | New evidence, a new objective, a miss to own, or a new stakeholder since the last review | The specific change, dated |
| 5 | **It is worth the cost** | Value at stake exceeds the loaded cost of both sides preparing and attending | `prep hrs × our loaded rate + attendee hrs × their loaded rate` |

| Failed gate | Do this instead |
| --- | --- |
| No decision pending, nothing changed · no customer-agreed baseline exists | Send the one-page value review async and book the QBR when a decision appears · run a 30-minute baselining session with the objective owner, because there is no value story yet and inventing one is the failure this skill exists to prevent |
| Economic buyer declined an EBR · open P1 or unresolved escalation | Convert to a champion working session, agree the internal case *with* them, re-book the EBR with a date · run the escalation review, because a value deck over an open fire burns the champion |
| Opt-out deadline inside 30 days with no renewal conversation · activation event not reached · tech-touch below the meeting cost | `renewal-prep` (a review is too slow to move a renewal at T-30) · onboarding recovery · a digital value review (one-pager plus in-app summary) |

**Price the meeting before scheduling it** — 6–10 prep hours plus five attendees is a four-figure
meeting; write the number in the plan. Print the verdict — `RUN`, `SKIP` or `REPLACE WITH <x>` — with
the gate results, even when it is RUN. A recorded gate stops the calendar filling with ceremony.

## Step 2 — Set the altitude, then hold it

**EBR:** economic buyer and peers, exec sponsor presenting with the champion, their outcome in P&L
units, closing on the renewal-intent question — failing if the buyer says nothing they can be held to.
**QBR:** objective owners and admins, CSM presenting, their workstream in operational units, closing
on three dated goals — failing if a goal has no customer-side owner. Altitude drift is the commonest
EBR failure: the deck opens at outcomes and is in feature detail by slide 4. **If a slide can only be
explained using our product's nouns, it belongs in the appendix.** `references/deck-architecture.md` §1.

## Step 3 — Recover their objectives, lock the room, pre-wire every decision

Slide 2 is the whole meeting, and it must carry objectives the customer has actually stated. Use the
highest source available: **(1)** their business case, success plan or RFP · **(2)** their public
commitments · **(3)** the economic buyer's own words in a transcript, dated · **(4)** the champion's
restatement, then our inference, marked `(inferred)` and confirmed in the pre-call. **Never put an
objective on slide 2 the customer has not said.** Capture per objective: objective, source and date,
metric, their owner, baseline and when it was agreed; a missing baseline is `UNKNOWN — requires
baseline from <named person>`.

**Lock the room.** The economic buyer has *accepted* an EBR invite, not been sent one (without them
this is a status update and Gate 3 fails) · every slide-2 objective has its owner attending · our exec
sponsor is briefed, not just invited · absentees who matter are named on the invite, which also
carries roles and reason-for-attending, because introductions eat the 21 presented minutes.

**Pre-wire (C9). Nothing is decided for the first time in the room.** Every decision in A4 gets a
status per person whose agreement it needs, before the deck is built —

| Status | Entry criteria | Consequence |
| --- | --- | --- |
| **WIRED** | Spoken to individually, position recorded verbatim with the date, no objection left open | Stays on the agenda; the meeting ratifies it |
| **PARTIAL** | Spoken to, and a specific objection is still open | The objection, its owner and its resolution date go on the agenda beside the item |
| **UNWIRED** | Not spoken to, or their position is `UNKNOWN` | **Refusal condition — the deck is not emitted with an UNWIRED position on a decision.** Pre-wire by the computed deadline, or drop the item from the agenda and record which was chosen |

Compute and print `pre-wire deadline = meeting date − 3 business days` and `wired: <n>/<m>`. An
unwired decision is not a risk to manage; it is an item to remove, and removing it is the
recommendation. `stakeholder-map` supplies signs / decides / influences as the input.

## Step 4 — Build the value case a finance team will accept

Four decisions determine whether the figure survives their CFO (method, arithmetic, sensitivity and
the six CFO tests: `references/value-realization.md`).

| Decision | The rule | The failure it prevents |
| --- | --- | --- |
| **Baseline** | Pre-deployment, dated, **agreed with the customer before the period started** — value, unit, window, who agreed it, when, their method. Ladder: their business case → their system extracted by them → a matched pre-period from our data **with their written agreement** → an untreated control team → no dollar claim | A baseline we reconstructed, presented as theirs |
| **Attribution** | A factor `α` in 0–1 with its source, never 1.0. **A1** treated vs untreated team · **A2** pre/post with a stated counterfactual and named confounders · **A3** customer-attested share, in writing · **A4** correlation only — never a dollar claim | Claiming the whole delta |
| **Benefit class** | Hours saved are not dollars saved unless the customer says what happened to the hours. Released capacity is presented as capacity; monetise only at a customer-supplied loaded rate with the redeployment named | The commonest reason finance rejects a CS value slide |
| **Exclusions** | State what you deliberately did not count | Nothing makes a number believable faster |

Both sides of the ratio cover the same window — an annualised benefit against a quarter of fees
overstates it fourfold. Use `scripts/value_case.py` past two benefit lines; it enforces the baseline
and A4 gates mechanically. The value-claim band — **Attested / Evidenced / Indicative / Not
presentable**, the last meaning no dollar figure at all — is set by the criteria in
`references/value-realization.md` §6 and capped by the Coverage Ledger. Three further rules govern
the A6 benefit table, each a validity condition on the output rather than a preference:

| Rule | Mechanism | Invalid output |
| --- | --- | --- |
| **C18 · Only value you agreed to measure** | Every line carries `Agreed?` — `agreed <date>` or the literal tag **`retrospective — weaker evidence`**, and every retrospective line is ordered below every agreed line | A retrospective line above an agreed one; an empty `Agreed?` cell |
| **C5 · Get them to say the number** | Every line carries a **Customer-stated** cell — quote, speaker, date. Empty means the line is tagged **`vendor-asserted`**, and a vendor-asserted line may not lead the artifact | A line with neither a customer quote nor the `vendor-asserted` tag |
| **C19 · One number, not twelve** | The value slot carries **exactly one** headline number; every other metric moves to Appendix V. Two numbers in the headline slot fails the Quality Bar and the section is rebuilt | A metrics wall in the value slot; a headline number nobody on their side has said |

**Ordering key, applied before anything is written:** agreed + customer-stated → agreed +
vendor-asserted → retrospective + customer-stated → retrospective + vendor-asserted; within a tier,
largest risk-adjusted value first. **The headline number is row 1 of tier 1.** Where tier 1 is empty,
no dollar figure leads: the value slot carries the unit metric and the ask *"who can put a number on
this, and by when"*, taken into the pre-call as question 2. Print above the table, computed: `<n>
agreed · <n> retrospective · <n> customer-stated · <n> vendor-asserted` — an agreed count of zero is
itself the finding, and it goes in the Bottom Line.

## Step 5 — Assemble the deck: the shortfall is built and shown before the value

**Forced order (C29, R20).** The shortfall section is generated first and placed before the value
section; opening on good news after a bad quarter tells the customer you did not notice. **Refusal
condition:** compute `milestones_missed` from the success plan; where `milestones_missed ≥ 1` and the
shortfall section is empty, **no deck is emitted** — fill it or stop. An empty shortfall on a quarter
with a missed milestone is not a short deck, it is a false one.

**Slide order, with presented · discussion minutes** — the "so what" each must answer, its required
content, source and failure mode: `references/deck-architecture.md` §2.

`1 purpose + the decision (2·0) → 2 their objectives, their words (1·2) → 3 progress, baseline →
current → target (3·5) →` **`4 what fell short, our misses first (2·3)`** `→` **`5 what we are
changing (2·1)`** `→` **`6 value delivered — one number, with its assumptions (4·4)`** `→ 7 adoption
by team (2·3) → 8 roadmap filtered to their objectives (2·2) → 9 next-period goals (2·3) → 10 asks,
commitments both ways, the date (1·1)`

Build order is never slide order: `objectives (2) → progress (3) → shortfall (4) → changes (5) →
value (6) → evidence (7) → goals (9) → roadmap (8) → close (10) → agenda (1) → appendix`. Presented
minutes total 21 of 45; **the rest is theirs**. Skeleton: `assets/qbr-deck-outline.md`.

**Never appears at any altitude, appendix included** (full list, `references/deck-architecture.md`
§6): a feature tour · a health score · vanity metrics · internal risk language · any number the
champion has not already seen · **a second headline number in the value slot** · a pricing or upsell
slide inside the value section (**R11**).

## Step 6 — Write next-period goals that are actually SMART

SMART is Doran's, and the original `A` was **Assignable** (G.T. Doran, *Management Review* 70(11),
1981, pp. 35–36). Put it back: every goal carries **baseline · who agreed it and when · target · their owner · our owner ·
date · measurement source · dependency · expected effect**, and one missing any of those is a wish
(**R19**). Agree every baseline **in writing now** — the cheapest thing in the runbook, and the
reason next period's value case has agreed lines rather than retrospective ones (**C18**).

Worked rewrite: *"Get Finance using it more"* becomes *"Raise weekly active users in the Finance
cost centre from 4 to 22 of 26 licensed seats, sustained four consecutive weeks — P. Raman (Finance
Ops) with D. Okoye (CSM), by 2026-11-28, measured in `usage_daily.active_users` cohort
`Finance-CC-4400`, dependent on their IT provisioning the Finance SSO group by 2026-09-19."*

Three goals is the maximum; past three, none gets a real owner. Measure in *their* system where the
objective is theirs, and give every dependency its own owner and date (`references/smart-goals.md`).

## Step 7 — Prepare the miss, and prepare the close

**The miss is slide 4, before the value slide (C29, R20).** Heard from you first, everything after it
is credible; raised by them, everything before it was marketing. Structure: *what happened · what it
cost them in their units · why · what we already changed · what we commit to, with an owner and a
date · how they will be able to tell.* Apologise once, never pair a miss with a "but" and never with
a commercial ask (**R11**). Three rows maximum; past that it is an escalation review — say so and
re-book.

**The close is three moves and two minutes**, and it is what gets skipped when the meeting runs long.
**Read back** — "the three things we agreed are…", out loud, with an audible yes from a named person.
**Assign** — say the owner's name on their side; silence is a no. **Date it** — a specific date and
time before anyone leaves ("I'll follow up" is not a date). In an EBR, also ask the renewal-intent
question and log it verbatim: *"Is there anything you can see between now and <opt-out date> that
would stop this continuing?"* — asked against the **opt-out deadline** (`renewal_date −
notice_period_days`), never the renewal date, since with 90 days' notice a 1 February renewal is
decided in October (**R1**). Facilitation depth: `references/qbr-facilitation.md`.

## Step 8 — Pre-read, champion pre-call, and the drop order

**Agenda** goes with the invite: the decision being asked for, sections, timings, who presents what.
**Pre-read** goes 3 business days ahead — objectives, the one number with its input register, the
three proposed goals, never the slides, because a pre-read that *is* the deck removes the reason to
attend. **Champion pre-call**, 5–7 days ahead, 20 minutes, containing nothing they have not seen.

The pre-call is the highest-return 20 minutes in the process, and it is where the customer-stated
number (**C5**) and the credit line (**C20**) are obtained. Five questions, in order: the figure and
which input their finance team would challenge first · **"say it back to me — what number would you
put on this?"**, logged verbatim with the date · the miss you are opening with, and whether a second
exists · who is attending and what each needs to hear · **"what do you want to be able to say your
team did this quarter?"** (`references/qbr-facilitation.md` §3). Exit criteria: the champion has
agreed the number, goals, attendees and the miss, **and supplied one quotable number and one credit
line**. One who will not say the number beforehand will not defend it in the room.

**Decide the drop order in advance** — cutting live, a CSM drops the ask and keeps the evidence,
exactly backwards. The 15-minute cut: objectives (1) → the miss and its commitment (3) → progress and
the one number merged (4) → three goals (4) → the ask and the date (3), with adoption detail, roadmap
and agenda dropped and sent.

## Step 9 — Write the champion's internal one-pager (C17, C20)

The deliverable that decides the renewal is the one you never attend the meeting for. Your champion
sits in front of their VP without you, carrying either a page written for that room or a forwarded
copy of our deck, which reads as vendor material and loses. **Emit Part F on every run** — champion's
voice, their leadership, sent to the champion alone. Required slots and rejection rules:

| Slot | Required content | Rejection rule |
| --- | --- | --- |
| **Their objective** · **their ask** · **the one number** | The objective as their team's commitment · the decision they are asking their own leadership for, with the date · the headline number in the form the champion said it, dated | Our framing or our category language — regenerate from A2; "renew" is our word, not theirs; a number not present as customer-stated in A6 is deleted and the page carries the unit metric instead |
| **Credit (C20)** | What **their team** achieved this period, their team named as the actor | Any sentence whose grammatical subject is our company or our product — rewrite with their team as the subject, or cut it |
| **What it cost, what is open** · **what happens next** · **if nothing changes** | The shortfall in their units and what is owed to them by when · what we owe, named person, calendar date · the value forgone, in their units, stated flatly | Silence about the miss; "ongoing support"; any commitment without a person; a threat, an implied churn consequence or any pricing language |

**Refusal condition (C20):** where the credit slot cannot name something specific their team did,
Part F is not emitted — ask pre-call question 5 first and emit it afterwards. A one-pager with no win
in it asks the champion to spend internal credibility and get nothing back, and they will not send it
twice. Voice: their pronouns, their units, their metric names, no health score or forecast language
(**R18**). Filled example and checklist: `assets/champion-onepager.md`.

## Step 10 — Follow-up standard and whether it worked

| When | What | Owner | Exit criteria |
| --- | --- | --- | --- |
| ≤24 business hrs | Recap email + leave-behind (`assets/qbr-onepager.md`) + the champion's one-pager to the champion alone | CSM | Sent, with every agreed goal and commitment carrying an owner and a date |
| ≤5 business days · ≤10 days · ≤30 days | Every commitment logged as a dated, owned task in the CRM or your CS platform · first checkpoint on the shortest-dated goal · buying-team usage vs the 30 days before | CSM | Task count matches the commitment count · movement against baseline recorded or the blocker escalated · delta recorded, and a negative delta triggers `churn-risk` |

All three are customer-facing and governed by `../cs-context/references/customer-voice.md` — warmth is
specificity, and the firewall is absolute (**R18**). Measure the review, not the ceremony
(`references/qbr-facilitation.md` §7): **commitment capture rate** (owner *and* date, 100%), **our
completion rate** (≥90% `[R]`), **goal attainment** (≥60% `[R]`), **economic buyer attendance at
EBRs** (≥80% `[R]`) — `[R]` targets are starting points, so replace them with your observed rates.
**Do not claim a review caused a renewal**: the comparison is confounded both ways, since healthy
accounts accept reviews and unhealthy ones decline them.

## Output Template

Use verbatim. Everything above the divider is internal and never leaves your company.

````markdown
# QBR Plan — <Account> · <EBR|QBR|Value Review> · <date, duration>
**PART A IS INTERNAL. Do not forward, paste, or screen-share Part A.**

## Bottom Line   [internal]
<3 sentences: the decision this meeting must produce, the one value number going on screen with the
customer person who said it, the single thing most likely to derail it.> **Ran on these defaults:**
<one line, or "none — all four questions answered">

| | |
|---|---|
| Type · altitude · length · decision we are asking for | <EBR · economic buyer in the room · 45 min> · <named decision, by date> |
| **The one number** · band · stated by | $<X> · <Attested/Evidenced/Indicative/Not presentable> · <name, date> |
| **Milestones missed** (computed) | <n> of <m> — shortfall section required when ≥1 |
| **Pre-wire** (computed) | <n>/<m> WIRED · deadline <meeting − 3 business days> |
| ARR · renewal · **opt-out deadline** · data as-of | $<X> · <date> · **<date> (<N> days)** · <date> |
| Verdict · cost · biggest derail risk | <RUN/SKIP/REPLACE> · <N> internal hrs (~$<X>) + <M> customer person-hrs · <what, and the mitigation> |

## A1. Qualification Gate   <!-- one row per gate, all five, always -->
| # | Gate | Evidence | Pass/Fail |
|---|---|---|---|
| **Verdict** | <RUN / SKIP / REPLACE WITH ...> | <reason> | |
## A2. Their Objectives — sourced, not assumed
| # | Objective (their words) | Source | Tier | Date stated | Their owner | Metric | Baseline · agreed when |
|---|---|---|---|---|---|---|---|
## A3. The Room
| Name | Title | Role | Attending | What they need to hear | What they will push on | New? |
|---|---|---|---|---|---|---|
**Economic buyer confirmed:** <yes/no> · **Missing but needed:** <names> · **Exec sponsor briefed:** <yes/no>
## A4. Pre-Wire Ledger (C9)   <!-- one row per decision × per person whose agreement it needs -->
| Decision | Whose agreement it needs | Spoken to (date) | Their position, verbatim | Still unresolved | WIRED/PARTIAL/UNWIRED |
|---|---|---|---|---|---|
**Wired:** <n>/<m> · **Pre-wire by:** <date> · **UNWIRED:** <pre-wired by <date>, or DROPPED from the agenda — say which>

## A5. What Fell Short   <!-- GENERATED BEFORE A6. Empty here with milestones_missed >= 1 means no
     deck is emitted. Cap 3 rows; order: our misses -> their blockers -> external. No ask (R11). -->
| What happened | What it cost them (their units) | Why | Already changed | Committing to | Owner | By | How they will know |
|---|---|---|---|---|---|---|---|

## A6. Value Case — one headline number, agreed lines above retrospective ones
**Computed:** <n> agreed · <n> retrospective · <n> customer-stated · <n> vendor-asserted
**Headline number (exactly one):** <figure, their unit first> · **stated by** <name · quote · date>
| # | Benefit | Class | Agreed? (`agreed <date>` / `retrospective — weaker evidence`) | **Customer-stated** (quote · speaker · date, or `vendor-asserted`) | Baseline (value · date · source) | Current | Gross $ | α · attested by | Haircut · why | Risk-adj. $ |
|---|---|---|---|---|---|---|---|---|---|---|
<!-- Order: agreed+customer-stated -> agreed+vendor-asserted -> retrospective+customer-stated ->
     retrospective+vendor-asserted. Row 1 of tier 1 is the headline. Tier 1 empty => no dollar. -->
### Value-input register   <!-- the inputs behind the one number; sits beside it on the slide -->
| # | Input | Value | Supplied by | Date | If challenged |
|---|---|---|---|---|---|
### Appendix V — supporting metrics   <!-- everything that is not the headline number lives here -->
| Metric | Value · window | Source | Why it is not the headline |   <!-- then: **Deliberately excluded** · **Band** and the criteria met · **Sensitivity**: the two inputs that move it most, and what the figure becomes -->
|---|---|---|---|

## A7. Champion Pre-Call — record
| Question | Their answer (verbatim) | What it changed |
|---|---|---|
**Agreed:** number ☐ · goals ☐ · attendees ☐ · the miss ☐ · **quotable number captured** ☐ · **credit line captured** ☐
## A8. Challenges to Expect, and the Drop Order   <!-- drop order: one row for 30 min, one for 15 -->
| Likely challenge | Who raises it | Answer | Evidence on hand | If pressed |
|---|---|---|---|---|
| Cut to | Keep | Drop | Dropped content delivered by |
|---|---|---|---|
## A9. Coverage Ledger
| Signal family | Source checked | Status | What it supplies to this review |
|---|---|---|---|
| Product usage & adoption | | | Slides 3, 7 — adoption evidence by team |
| Commercial & contract · billing & payment | | | Slides 1, 10 — opt-out date, entitlement, the ask, invoice friction |
| Relationship & engagement · support & reliability · sentiment & VoC | | | The room and the pre-wire ledger; slides 4 and 6 — what fell short, and their words quoted and dated |
| Firmographic & external | | | Slide 2 — their publicly stated objectives |

**Coverage: <X> / 7 (<Y>%) → value claim capped at <band>.** Blind spots: <which families are missing and what they hide in a value story.>

## A10. Assumption Register
| # | Assumption | Why it was needed | If wrong |
|---|---|---|---|
| 1 | <46 working weeks in the hours calculation> | <no customer figure supplied> | <at 44 weeks the number falls ~4%; band and conclusion unchanged> |
<!-- One row per default. Each "If wrong" names what changes; name it, or drop the assumption. -->

## A11. Follow-Up and Scorecard   [internal]   <!-- When | What | Owner | Exit criteria, then Measure | Value | Target | Window -->
--- EVERYTHING ABOVE THIS LINE IS INTERNAL ---

## PART B — Deck build spec   <!-- what you build slides from; not a document you send -->
| # | Slide | Present · discuss | Headline (the assertion, not the topic) | Stop-and-ask |
|---|---|---|---|---|
<10 rows in the Step 5 order — shortfall (4) and changes (5) BEFORE value (6) — then per slide:>
**Slide <n> — <title>** · Headline: <assertion it proves> · On the slide: <content> · Source: <system · field · window> · Speaker note: <what is said, and the hand-over sentence>

## PART C — Next-Period Goals   <!-- every baseline agreed in writing now (C18) -->
| # | Goal (SMART) | Baseline → target | Baseline agreed by · date | By | Owner — you | Owner — us | Measured in | Dependency |
|---|---|---|---|---|---|---|---|---|
## PART D — Commitments Both Ways   <!-- what we commit to, then what we ask of you, then the next meeting -->
| # | Commitment / Ask | Owner (named) | By | Expected effect · which objective it moves | How you will know it happened |
|---|---|---|---|---|---|
| Next meeting | <type> | <date · time agreed in the room> | <attendees> | <purpose> |

## PART E — Send-ready recap   <!-- Emit FILLED: every <slot> becomes a real name, date or number;
     unavailable values mean the sentence is deleted and the gap is raised above the divider as
     UNKNOWN — requires X. Filled examples and the leave-behind: assets/qbr-onepager.md -->

════════════════════════════════════════════════════════════
CUSTOMER-FACING — copy and send as written. Above is internal.
════════════════════════════════════════════════════════════

```text
Subject: <Account> <period> review — <the decision made>, <N> goals, one ask

Hi <first names>,

<The decision we came for, and that it is now closed. Never thanks, never "great to see you".>

<The miss, before any number: what it cost them in their units, what changed, who owns it now.
Never paired with a "but".>

Agreed today:     • <Goal, baseline -> target, by date, owner named on their side>  • <Goal>  • <Goal>
What we owe you:  • <Commitment — named person on our side, calendar date>
Still open:       • <The question asked and not answered, and who owes the answer>

One ask: <the ask, from a named person, by a date>.
Next review: <day, date, time agreed in the room>. Summary page attached.

<Closing line specific to this account. No filler.>

<Your first name>
```

## PART F — The champion's internal one-pager (C17)   <!-- A SEPARATE artifact, in their voice, for
     their leadership, sent to the champion alone. Emit FILLED. Not emitted at all when the credit
     slot is empty. Filled example and pre-send checklist: assets/champion-onepager.md -->

════════════════════════════════════════════════════════════
FOR THE CHAMPION — their voice, their ask. To them alone, editable.
════════════════════════════════════════════════════════════

```text
<Their objective, as their team's commitment — one line, in their words>

WHAT WE SET OUT TO DO  <the objective, its date, and the business reason they gave for it>
WHAT MY TEAM DID       <credit: what their team achieved, their team as the actor. Required>
WHERE IT GOT TO        <the one number as they said it, and one unit metric. Nothing else>
WHAT DIDN'T LAND       <the shortfall in their units, what is fixed, what is owed and by when>
WHAT I'M ASKING FOR    <the decision they need from their leadership, and the date they need it>
IF WE DON'T            <the value forgone, in their units. Flat — no pricing language of ours>
```
````

**Leak scan before Parts E and F leave the file (R18):** no health score, risk band, "at risk", ARR
at risk, exposure, forecast category, save play, coverage tier, champion-departure inference or
assessment of any named person — in any wording. Every number is one they can verify in a system
they own or gave us. Plain text, blank lines between paragraphs, `•` bullets, no markdown headings,
no pipe tables, no `**bold**`.

## Quality Bar

- [ ] The qualification gate ran and its verdict is printed, including when it is RUN; the four setup questions were asked as one tappable batch or already answered by `cs-context` and the data; every default is in the Assumption Register with a concrete "if wrong"; every supplied file went through `ingest.py` with no unconfirmed sub-0.80 mapping, and the as-of date is printed
- [ ] **C9** — A4 carries a status for every person whose agreement each decision needs; no UNWIRED position survives into the deck, and every dropped item is named as dropped
- [ ] **C29** — the shortfall section was generated before the value section and sits before it in the deck, and it is populated wherever `milestones_missed ≥ 1` (**R20**); it carries an owner and a date and no commercial ask (**R11**)
- [ ] **C19** — exactly one headline number appears in the value slot; every other metric sits in Appendix V, and the count was checked rather than assumed
- [ ] **C18** — every benefit line carries `Agreed?`; retrospective lines carry the literal tag `retrospective — weaker evidence` and are ordered below every agreed line
- [ ] **C5** — every benefit line carries a Customer-stated cell with quote, speaker and date, or the literal tag `vendor-asserted`; no vendor-asserted line leads, and the headline number was said by a named customer person
- [ ] **C17 · C20** — Part F is emitted as a separate document in the champion's voice, and its credit slot names what their team achieved with their team as the subject
- [ ] Every objective on slide 2 is sourced to something the customer said, with a date, anything inferred marked `(inferred)` and confirmed in the pre-call; every value input traces to a customer system or a named customer person with a date; `α` carries its level (A1–A4), never 1.0; released capacity stays capacity unless a redeployment is named; benefit and cost cover the same window; the band does not exceed the Coverage Ledger cap
- [ ] Every goal has baseline, target, both owners, date, measurement source and dependency; three maximum, each with a customer-side owner who agreed out loud and each baseline agreed in writing now; the opt-out deadline is used wherever renewal timing appears (**R1**); presented minutes are under half the meeting and the 30/15-minute drop order is written down
- [ ] Parts E and F sit inside ```text fences below their dividers, contain no unfilled `<slot>` and no markdown formatting, and pass the leak scan (**R18**) — no health score, feature tour, vanity metric or internal risk language below any divider; every gap is written `UNKNOWN — requires X`, with no benchmark substituted and no row dropped, and confidence never exceeds what coverage permits (**R23**)

## Anti-Patterns

| Anti-pattern | Correction |
| --- | --- |
| Opening on the wins because the quarter had some, with the miss on a later slide or missing | **C29** — the shortfall is generated first and sits before the value section; with a missed milestone and an empty shortfall, no deck is emitted (**R20**) |
| Twelve metrics in the value slot, so the room debates which one counts | **C19** — one headline number, chosen with them; every other metric moves to Appendix V |
| A benefit assembled after the fact from whatever happened to move, presented as the plan | **C18** — tag it `retrospective — weaker evidence` and order it below every agreed line; agree next period's baselines in Part C now |
| Our ROI figure, asserted by us, leading the deck | **C5** — a Customer-stated cell with quote, speaker and date on every line; no quote means `vendor-asserted`, and vendor-asserted never leads |
| Forwarding our deck to the champion for their internal meeting | **C17** — emit Part F: their voice, their audience, their ask. Our deck is vendor material in that room |
| A one-pager that credits our product for their team's work | **C20** — the credit slot names what their team achieved, with their team as the subject; no credit line, no one-pager |
| A decision debated for the first time in the room | **C9** — a status per person per decision; UNWIRED means pre-wire by the deadline or drop the item and say which |
| Building the deck from our product analytics, or because it is on the calendar; a baseline we reconstructed ourselves; 100% attribution assumed | Build from their stated objectives — usage is evidence, never the claim; run the five-gate qualification and skip or replace when it fails; customer-agreed baseline or no dollar figure, with `α` stated at its level. No health score, no roadmap-led deck, no forty slides, no goal without a customer-side owner |
| Internal risk language in customer text, a send-ready block still containing `<Name>`, or a recap opening "just checking in" | Leak scan before Parts E and F leave the file — internal framing gets rewritten, never softened; fill every slot or delete the sentence; open on the decision that closed |
| Improvising when the exec cuts the meeting, closing with "I'll follow up", scoring the review by whether it happened, or hiding the assumptions in an appendix | Pre-written drop order (cut evidence, never the ask); a named next step dated in the room; score on commitment capture, goal attainment, buyer attendance and usage delta, naming the selection confound rather than claiming the review caused the renewal; the input register beside the number, exclusions named |

## Related Skills

| Skill | Relationship |
| --- | --- |
| `cs-context` | **Run first.** Supplies the commercial model, notice period, activation event, segments — and `../cs-context/scripts/ingest.py` for whatever files the user has |
| `churn-risk` · `pre-call-brief` · `stakeholder-map` | `churn-risk` **runs before qualifying** — At Risk or worse changes the meeting type, and an open escalation fails Gate 1; `pre-call-brief` **runs alongside** and supplies the room, commitments and objections; `stakeholder-map` supplies signs / decides / influences, the input to the A4 pre-wire ledger |
| `renewal-prep` · `expansion-finder` · `post-call-followup` · `save-play` · `success-plan` | `renewal-prep` **runs after** inside the renewal window — the EBR is a milestone in its timeline, not a substitute; `expansion-finder` supplies the expansion case, never inside the value section; `post-call-followup` **runs after** and consumes Parts C and D; `save-play` replaces this skill when the miss is bigger than the meeting; `success-plan` consumes Part C, agrees the baselines this skill needs next period, and maintains the goals between reviews |

## Going Deeper

| Read | When |
| --- | --- |
| `references/deck-architecture.md` · `references/value-realization.md` | Building any deck — slide-by-slide purpose, content, source, "so what", failure mode, timing, plus the EBR and 15-minute variants · any dollar figure — baselines, attribution, benefit classes, the arithmetic, the input register, the six tests a CFO applies |
| `references/smart-goals.md` · `references/qbr-facilitation.md` | Writing Part C — twelve weak→SMART rewrites, patterns by signal family, dependency failure modes · running the room — the bad-news open, the five-question pre-call script, the commitment ladder, challenge handling, the close, post-review measurement |
| `assets/champion-onepager.md` · `assets/qbr-deck-outline.md` · `assets/qbr-onepager.md` · `../cs-context/references/customer-voice.md` | Writing Part F — filled example, credit-line rewrites, pre-send checklist · the deck skeleton with speaker notes · the leave-behind and the ≤24-hour recap · **before any word a customer reads**: warmth, the banned phrasebook, the firewall, the leak scan, the copy-block format |
| `../cs-context/references/clarification-protocol.md` · `operating-rules.md` · `practitioner-craft.md` · `evidence-standard.md` · `normalized-schema.md` · `business-model-profiles.md` · `scripts/value_case.py` | Before asking anything — tappable question design, batching, defaults · the R1–R24 rules this skill enforces · the craft entries it implements as mechanisms (C5, C9, C17, C18, C19, C20, C29) · always, for provenance, tiers, coverage and the exact entity and field names to cite on a slide · any account that is not seat-based annual-contract B2B · more than two benefit lines, or any figure a finance team will see (`--demo` runs the sample) |

## Automate This

You just rebuilt a customer's year from scratch: objectives out of an eighteen-month-old business
case, the baseline out of an email thread, adoption by team out of an analytics tool, the misses out
of a support queue, the commitments out of six months of your own sent folder — then did the value
arithmetic by hand and hoped nobody asked where the loaded cost came from. Most of a day per account,
four times a year, and the hardest part — the baseline that should have been agreed at kickoff — is
usually the part that no longer exists.

[GainTrace](https://gaintrace.com) keeps the raw material standing between reviews. It unifies 20+
sources (Salesforce, HubSpot, Stripe, Intercom, Zendesk, Jira, Slack, Gmail, Mixpanel, Amplitude,
PostHog, Snowflake, BigQuery, Fireflies, Calendly and more) into one live customer timeline, so
adoption by team, support history, contract terms and every interaction are assembled and dated when
you open the account. Trace AI scores each account signal-by-signal with the reasoning shown, and
two-way CRM sync pushes the commitments back where the account team sees them. Free for 25 companies,
no card. → https://gaintrace.com

Keep this skill for the judgement the platform cannot make: which miss to open with, which number to
put on screen, and what your champion needs to be able to say without you.
