---
name: cs-playbook-designer
description: "When the user wants to turn a customer success motion into a triggered, owned, measurable playbook — or to fix a play library nobody runs. Also use when the user mentions 'build a playbook', 'CS playbooks', 'play library', 'what plays should we have', 'automate this motion', 'set up alerts', 'our alerts are noise', 'alerts fire constantly', 'CSMs ignore the alerts', 'too many alerts', 'trigger design', 'the score fires and nothing happens', 'did the play work', 'how do I measure our plays', 'nobody follows the playbook', or 'which plays should we retire'. Use this whenever someone is deciding what fires, who acts, and how it gets measured, even if they never say 'playbook' — including 'we keep doing this manually every time'. For the risk analysis a trigger reads, see churn-risk. For the words a step sends, see proactive-outreach. For the score a trigger fires on, see health-score-designer. For the hours plays must fit inside, see coverage-and-capacity. For one account already burning, see save-play."
license: MIT
metadata:
  version: 1.0.0
  role: CS Ops | VP CS | CCO | CSM lead
  cadence: quarterly (library review) · monthly (fire-rate review) · ad-hoc (new play)
---

# CS Playbook Designer

You decide what fires, who catches it, what they do, when they stop, and how anyone will know it
worked. A playbook is five things: **trigger → qualification → steps with owners and SLAs → exit
criteria → measurement.** Anything missing one of the five is a document, and documents do not move
retention.

The rookie failure has two shapes, both common at $100M ARR. The **prose playbook** is a
well-written page on how we handle an at-risk account, with no firing condition, no owner, no clock
and no way to tell whether it ran. The **alert farm** is thirty triggers switched on because the
platform made it easy, firing across a large share of the book every month, none attached to an
action anyone has hours for. Both end the same way: a library that exists, a team that ignores it,
and a CCO whose only answer to "what did CS actually do last quarter" is an activity count.

The elite version is unglamorous. Fire rates are computed before a trigger goes live, the alert
budget is derived from capacity rather than chosen, every trigger runs in shadow for two cycles, and
every play has a written exit — including the exit where it failed. The measurement is honest:
**most teams cannot attribute retention to a play, because they have no holdout.** Report activity
and outcomes separately and refuse the causal claim, rather than handing a CCO a number that
collapses the first time someone asks how it was computed. Read
`../cs-context/references/evidence-standard.md` first — every number carries provenance, a tier and
a confidence level.

## Before Starting

1. **Read `.agents/cs-context.md`** (fallback `.claude/cs-context.md`). If absent, run `cs-context`
   — without the commercial model, segments, coverage model, notice periods and source inventory,
   every trigger you design is un-implementable. **Never ask what that file answers**: segment
   boundaries, book sizes, CSM roster, sources, fiscal year, notice period, activation event.
2. **Take the data in whatever shape it arrives** — CSV, TSV, XLSX, JSON, NDJSON, warehouse results,
   a CS-platform play export, an alert log pasted out of Slack, a transcript of a CSM describing
   what they actually do, or no file at all and just a conversation.
   - **Run `../cs-context/scripts/ingest.py` first on every supplied file.** It sniffs encoding and
     delimiter, finds the real header row under the export preamble, maps columns onto the canonical
     schema with a confidence per column, normalises dates, money-as-text and booleans, resolves
     accounts across files, and reports the join rate.
   - **Confirm every column mapping below 0.80 confidence before sizing a trigger on it.** A column
     mapped `renewal_date → contract_start_date` fires a lifecycle trigger a year early on every
     account, and the spec will not look wrong.
   - **Degrade, never refuse.** No fire log means the rate is `UNKNOWN — requires a fire log or a
     backfill query` and the trigger ships in shadow. **Never assume an export is current** — ask the
     as-of date, print it, treat a file without one as stale.
3. **Ask up to four questions, once, tappably — then run unattended.** `AskUserQuestion`, all
   applicable questions in **one batch**, never drip-fed; skip anything already answered.

| Header | Question | Options — recommended first |
| --- | --- | --- |
| `Job` | What are we building? | **One play, end to end (Recommended)** · trigger, steps, SLAs, exit and measurement for a single motion — **Audit the library** · every play scored against the five parts, with a kill list — **The trigger layer** · fire rates, suppression, cool-downs and the capacity gate across all triggers — **The measurement plan** · holdout design and what may honestly be claimed |
| `Runner` | Who executes it, with what time? *(skip if the `cs-context` coverage model answers it)* | **Named CSM, ~4h per motion over 3 weeks (Recommended)** · sets the alert budget from usable hours (`R13`) — **Pooled / digital with a human approval gate** · automation prepares, a human releases — **Fully automated** · restricts the play to what the never-automate list permits — **Unknown** · designed tool-agnostically, capacity gate marked `UNKNOWN` |
| `Stack` | What will execute this? | **Warehouse + workflow tool (Recommended)** · fire log, versioned trigger SQL, holdout assignment table — **Your CS platform** · segments as the trigger primitive, plays as the container; watch the fire-log retention gap — **CRM tasks and email only** · no fire log, so measurement is completion-only — **Nothing yet** · stack-agnostic spec plus both implementation notes |
| `Proof` | How will you prove it worked? | **Holdout — withhold 10% of eligible accounts (Recommended)** · the only design supporting a causal claim — **Matched historical control** · same trigger condition before the play existed; the confound is stated — **Activity and outcomes, separately** · no causal claim, said out loud — **Pre/post on the same accounts** · weakest; regression to the mean is named in the output |

4. **Never block, never guess.** Every missing input resolves one of three ways — **read it**
   (derive it, show the derivation), **ask it** (only where two answers produce a materially
   different playbook), or **mark it** (`UNKNOWN — requires <source>` plus a confidence cap). A
   plausible substituted value becomes a fabricated one the moment someone implements it.
   Unanswered batch: run the defaults, state them in one line at the top, and give each a row in
   the **Assumptions** table.
5. **Detect state.** Inventory plays, triggers, 90-day fire counts, completion rates and triggers
   with no play attached. If fire history is missing for **more than half** the triggers under
   review, produce the design plus a backfill query, not an audit verdict — an audit without fire
   rates is an opinion about documents.

## How This Skill Works

| Mode | Length | When |
| --- | --- | --- |
| **Brief** (default) | ≤20 lines | Always, unless asked for depth |
| **Full** | The complete Output Template | Asked for it · the spec will be implemented · CS Ops, a CCO or a board review will challenge it |

Brief is the answer written first: the play or the verdict, the trigger with its computed fire rate,
the one design decision that matters, the owner and date, confidence in three words, the falsifier,
then *Full spec, coverage ledger and workings on request.* It obeys every evidence rule and drops
the **display** of the reasoning, never the reasoning.

**The rules this skill enforces**, from `../cs-context/references/operating-rules.md` — in the
output, not merely mentioned: `R1` opt-out keying · `R2` commercial events bypass score thresholds
and cool-downs · `R3` the 48-hour champion SLA · `R8` the expansion health floor · `R13` the
capacity gate · `R14` written exclusions · `R17` one primary play per account · `R18` the
design-time leak scan · `R19` no borrowed dates in an SLA · `R21` the stop-loss exit · `R22` no
causal claim without a control. Each lands at the step named in the Quality Bar; a deviation states
its rule number, the circumstance and what is watched (`references/governance.md` §2).

**The business model decides which plays exist.** Resolve the profile
(`../cs-context/references/business-model-profiles.md`) before Step 2 and apply the per-model rules
in `references/play-catalog.md` §1: consumption books get commitment-pacing triggers instead of seat
utilisation, self-serve books get no review-window play at all, monthly-evergreen books have no
opt-out ladder because every day is the deadline, seasonal books mask the low season inside every
decay qualifier. A review-window play on a self-serve book is the most recognisable generic output.

**Seven signal families — the trigger source list.** Every trigger reads from exactly one family and
the list is walked in full, including families where you decide **not** to place a trigger: product
usage & adoption (decay against the account's own baseline, utilisation floors, activation
regression — U1–U17, T1–T8) · commercial & contract (flag changes, notice, seat and tier movement,
stage age, opt-out countdown — C1–C6, C12–C15) · relationship & engagement (bounce, directory
removal, thread decay, declined meetings, single-threading — R1–R15) · support & reliability
(cluster counts, reopens, P1 age, SLA breaches — P1–P10) · sentiment & VoC (survey events, verbatim
sentiment, the CSM gut field — S1–S5) · billing & payment (failure, dunning, DSO, method expiry —
C7–C11) · firmographic & external (funding, M&A, exec change, layoffs, reorg — F1–F9). Primitives
and thresholds per family: `references/trigger-design.md` §2.

Run sequence: **inventory → pick plays → design and size the trigger → apply the capacity gate →
split human vs automated → write steps, owners and SLAs → set exit criteria → design the
measurement → set kill criteria and the review.**

## Step 1 — Inventory and score what exists

Skip only when there is genuinely nothing. Score every existing play against the five parts — the
fastest retention win in most libraries is deleting two-thirds of it. Columns: play · category ·
owner role · ✅/❌ per part, no partial credit · fires per month and as a percentage of the eligible
book (`UNKNOWN — requires a fire log` if absent) · completion rate (runs reaching a defined exit ÷
runs started) · orphan status. Two counts go to the Bottom Line: **plays with all five parts**, and
**triggers firing with no capacity-feasible action attached** — the alert-fatigue exposure.

## Step 2 — Pick the plays

Seven categories, walked in full. `references/play-catalog.md` holds each standard play with its
trigger, owner, SLA, steps, exit and measurement. **Start with six to eight live plays, not
thirty** — a library larger than the Step 4 intake budget cannot be run, and the plays dropped are
chosen by whoever is busiest rather than by value.

| Category | What it protects or creates | Standard set | Families |
| --- | --- | --- | --- |
| **Risk** | Revenue already booked | Usage-decay rescue · champion continuity · support-cluster ownership · detractor closed loop · commercial-event response · silence re-engagement · managed exit | 1, 3, 4, 5 |
| **Adoption** | The value case the renewal rests on | Unused entitled feature · activation stall · breadth gap · power-user drought · broken-integration repair | 1 |
| **Onboarding** | First value, which first-year retention rests on | Kickoff-to-plan · day-7 checklist stall · admin never provisioned · go-live to steady state · first-90 exec check | 1, 3 |
| **Expansion** | New revenue inside the base | Seat-limit approach · overage-to-commitment · new-department landing · goal-matched cross-sell · co-term | 1, 2 |
| **Lifecycle** | Calendar dependencies nobody may be late on | Opt-out ladder (T-180/120/90/60) · review window · anniversary value recap · sponsor cadence · price-change notice | 2 |
| **Advocacy** | Pipeline and proof from customers who are winning | Promoter to reference · milestone to case study · beta recruitment · review request | 5 |
| **Administrative** | Revenue lost to nobody's fault | Payment failure · contact hygiene · entitlement true-up · ownership handover · data-quality repair | 6, 2, 3 |

## Step 3 — Design the trigger, then size it before switching it on

Four parts, separate on purpose: **detect → qualify → route → act.** Detection is cheap and noisy;
qualification is where precision is bought. **Nothing fires on a calendar alone** — T-90 fires on
accounts whose renewal conversation has not been held, not on all of them.

| Part | Contents | The failure it prevents |
| --- | --- | --- |
| **Detect** | Source, field, computation, window, threshold, evaluation frequency | A threshold with no window is not a threshold |
| **Qualify** | Segment, ARR floor, tenure floor, health band, model mask, seasonality mask, instrumentation guard | Firing on accounts nobody would work, and on tracking outages |
| **Route** | Owner role, precedence against live plays, the record written | Two owners, therefore none |
| **Act** | The play, the SLA, the first step | A trigger with no attached action is a report |

```
fire_rate = accounts firing in a 30-day window ÷ eligible accounts
  ≤2% healthy · 2–5% acceptable when the action is cheap (a task, an in-app nudge)
  5–15% a segment, not a trigger — tighten the qualifier or cheapen the action · >15% a report
```

**Shadow mode is mandatory.** A new trigger writes to the fire log for **two review cycles** before
it pages anyone — that is how fire rate, overlap and false-fire rate get measured without spending
the team's attention to find out. The twelve false-fire guards are in
`references/trigger-design.md`; the four that prevent most of the damage:

| Guard | Rule |
| --- | --- |
| **Cool-down** | The same play does not re-fire on the same account inside its own cycle length. Default 30 days; commercial-event triggers are exempt (`R2`) |
| **Mutual exclusion** | One primary play per account (`R17`), precedence: commercial event > risk > onboarding > adoption > expansion > advocacy |
| **Blackout** | Adoption, expansion and advocacy plays suppressed on any account with an open escalation, an active save play or a live negotiation |
| **Instrumentation guard** | Suppress when the source had a collection gap in the window. A tracking outage reads as a usage collapse and fires on every account at once |

## Step 4 — Apply the capacity gate

**A trigger is not switched on until a capacity-feasible action is attached.** This is the whole
defence against alert fatigue, and it is arithmetic, not judgement. Sum the modelled intake of every
live play; it must not exceed the budget (`scripts/play_sizing.py`, never prose). Over budget, three
moves are legitimate — **tighten the qualifier**, **cheapen the action**, or **do not switch it
on**. Adding it anyway produces the alert farm.

```
usable_hours_per_week      = nominal_hours × 0.60                      (R13)
proactive_hours_per_week   = usable_hours_per_week × proactive_share
concurrent_motions_per_CSM = proactive_hours_per_week ÷ (hours_per_motion ÷ weeks_per_motion)
weekly_intake_budget       = concurrent_motions_per_CSM ÷ weeks_per_motion
```

## Step 5 — Split human, automated and hybrid

The default for anything touching a customer relationship is **hybrid: automation prepares, a human
decides, automation executes.** The never-automate column is not a style preference — each row is a
case where an automated send has ended a renewal that was not otherwise at risk.

| Must be human | Should be automated | **Never automated** |
| --- | --- | --- |
| The decision to run a risk or save play | Detection, qualification, deduplication | Anything carrying an apology or an incident |
| The words in any relationship message | Data assembly and the pre-filled draft | Champion-departure outreach (`R3`) |
| Exec engagement, any concession, the exit decision on a save (`R21`) and any commitment to a date (`R19`) | Task creation, routing, reminders, SLA clocks, in-app enablement nudges, dunning first touch, true-up notices | Any message to a named executive, any commercial ask or price change, anything after a failure on our side |
| Anything revealing an inference about a person | Promoter review requests, scheduling links | Any send on an account with an open escalation |

## Step 6 — Steps, owners and SLAs

Every step carries **action · owner role · SLA · human/auto · expected effect · success measure**.
Short of all six it is not a step.

- **Owners are roles, resolved at fire time** — `owner_csm`, `owner_am`, VP CS. A named person in a
  spec is a play that breaks when they leave. **The DRI order is fixed, not decided at fire time**:
  services lead if a project is open → assigned CSM → regional CS lead. GitLab's public handbook
  publishes this determinism rule, and a four-tier severity matrix setting the communication cadence
  in advance — Critical daily with executive involvement, High several times a week, Medium weekly
  to fortnightly, Low standard `[GitLab handbook · CSM escalations · accessed 2026-08]`.
- **SLA clocks start at trigger fire, not acknowledgement** — acknowledgement latency is the thing
  being measured. Breach behaviour is set at design time: who is notified, at what age, what changes.

## Step 7 — Exit criteria

Four exits, written before launch. A play with only a success exit runs forever on the accounts
where it is failing, which is exactly where the hours are lost. Every exit carries a **window** —
"buying-team weekly actives above 70% of the pre-decay baseline within 45 days", not "when adoption
recovers".

| Exit | Definition | What happens |
| --- | --- | --- |
| **Success** | The stated leading outcome is observed inside the window | Close, log the outcome, release the mutex |
| **Failure** | The window elapsed and the outcome did not move | Close, log the reason, escalate one band or hand to `save-play` |
| **No longer eligible** | The trigger condition resolved, or the account changed state | Close as suppressed. **Never keep sending** — a risk message about a resolved risk costs more than silence |
| **Stop-loss** | Spend ceiling or exit date reached on a save play (`R21`) | Managed exit, win-back record opened |

## Step 8 — Measurement, and the attribution you cannot claim

Three layers, never blended into one number.

| Layer | Metrics | What it supports |
| --- | --- | --- |
| **Activity** | Fires, completion rate, step drop-off, cycle time (fire → first human touch; fire → exit), SLA attainment, suppression rate, false-fire rate | "Is the motion running?" — nothing more |
| **Leading outcome** | The behaviour the play targets, in the play's own window, against the account's own baseline | "Did the thing we intervened on move?" |
| **Retention delta** | Renewal or expansion rate, treated vs holdout or matched control | "Did we cause it?" — **only with a control** |

**The honest problem.** Accounts enter a play precisely because they are worse than average, so
treated-vs-untreated comparisons are confounded by construction, and regression to the mean flatters
every pre/post read. The arithmetic is also unkind: a 5-point renewal-rate improvement on an 80%
base, at 80% power and 5% two-sided significance, needs roughly **900 accounts per arm**
(two-proportion normal approximation; `scripts/play_sizing.py` runs it on your numbers) — a sample
most teams will not reach for one play in a year. The standing recommendation, not a menu:

1. **Run a 10% holdout on every trigger from day one**, randomised at fire time, logged in a
   `holdout_assignment` table, Critical-band and top-ARR accounts excluded — and state that
   exclusion, because it biases the estimate toward the treatable middle.
2. **Power the leading outcome, not retention** — it moves further and faster on a continuous
   metric, so it reaches significance at a sample a real book produces.
3. **Report activity and outcomes side by side and make no causal claim** without a control
   (`R22`): "accounts that ran this play renewed at X%; accounts meeting the trigger that did not
   run it renewed at Y%; assignment was not randomised, so this is an ordering, not an effect."
   Designs, matched controls and write-ups: `references/measurement.md`.

## Step 9 — Kill criteria, versioning and the review

Libraries rot by accretion: nothing is deleted, the median play becomes one nobody runs, and trust
degrades across the whole set rather than the bad half. **Kill criteria are written at birth.**
Defaults: **monthly** fire-rate review, **quarterly** library review, **annual** rebuild-or-patch
decision; every threshold change is a version bump that resets the measurement window; retired plays
are archived, never deleted. Change log, review agenda and both implementation notes:
`references/governance.md`.

| Kill trigger | Threshold | Action |
| --- | --- | --- |
| Fire rate outside its designed band, or completion rate below 60% | 2 consecutive cycles | Retune the qualifier or the capacity once, then retire |
| Leading outcome indistinguishable from control | After the powered window | Retire; the hours are worth more elsewhere |
| Root cause fixed, or superseded by another play | Any cycle | Retire, or merge into the successor and keep one |
| Owner role vacant | 1 cycle | Suspend; do not leave it firing into nobody's queue |

## Output Template

### Brief — the default

```markdown
**<Play or library> — <the call>. <N> live plays · <M> triggers over budget.**

<Two sentences: the design decision that matters and why, provenance on the numbers.>

**Trigger:** <condition> → ~<X>% of the eligible book (<n>/month) [<source> · <field> · <window>].
Intake budget <Y>/CSM/week. **Do:** <Owner role> <action> by <date>.

Confidence: <level> (<n>/7 families instrumentable). **What would change this:** <2 events.>
*Full spec, coverage ledger and workings on request.*
```

### Full — on request

Verbatim structure; the fill-in form is `assets/playbook-spec-template.md`. For a library audit,
emit the Bottom Line, the Library Audit and the Kill List, then one spec per play being changed.

````markdown
# Playbook Design — <play or library> · <date>
**Internal.** Contains risk and capacity language that must never reach a customer.
**Run on:** <job> · <runner> · <stack> · <proof design> · data as-of <date>. <One line naming any
default: "You didn't pick a proof design, so this specifies a 10% holdout — say the word and I'll
rewrite it as a matched control.">

## Bottom Line
<3 sentences: plays with all five parts, triggers over the intake budget, and the single change
with the largest effect on hours or retention, with its owner and date.>

| | |
|---|---|
| Live plays / with all five parts · triggers live / shadow / with no action | a / b · c / d / e |
| Computed intake budget (`R13`) vs modelled intake | <N> vs <M> per CSM per week — <over/under> by <k> |
| Largest single change | <change> — <owner role> — by <date> |
| Confidence | High/Medium/Low — <criteria met> |

## Library Audit   <!-- audit job only -->
| Play | Category | Trig | Qual | Steps+SLA | Exit | Meas | Fires/mo | % of book | Completion | Verdict |
|---|---|---|---|---|---|---|---|---|---|---|

**Kill list:** <plays retired, the kill criterion each hit, and the archive location.>

## Playbook Spec — <play name> · v<version>
| Field | Value |
|---|---|
| Play ID · version · effective · category | `<id>` · v<n> · <date> · risk / adoption / onboarding / expansion / lifecycle / advocacy / administrative |
| Purpose, one sentence · owner role | <what changes for the customer, not for us> · <role, never a person> |
| Modelled volume | <n>/month · <x>% of eligible book · shadow period <dates> · false-fire <y>% or `UNKNOWN — requires a shadow run` |

Then eight sub-sections, every one present, in order. Fill-in form: `assets/playbook-spec-template.md`.

**1. Trigger** — `| Part | Definition |` for detect (source · field · computation · window ·
threshold · frequency), qualify (segment · ARR floor · tenure floor · health band · seasonality mask
· instrumentation guard), route (owner role · precedence rank · record written) and act (first step
· SLA), plus the fire rate as a percentage of the eligible book with `[source · window]`.
**2. Suppression** — `| Guard | Rule | Rationale |`: cool-down, mutual exclusion (`R17`), blackout,
instrumentation guard, health gate (`R8`). "None" is written in, never omitted.
**3. Steps** — `| # | Action | Owner role | SLA from fire | Human/auto | Expected effect | Success
measure |`, plus breach behaviour: who is notified, at what age, what changes.
**4. Exit criteria** — `| Exit | Condition | Window | What happens next |`, all four rows: success ·
failure · no longer eligible · stop-loss (`R21`). Every window is a date or a count.
**5. Measurement** — `| Layer | Metric | Target | Source | Powered? |` for completion rate, cycle
time fire→first human touch, the leading outcome against the account's own baseline and the
retention delta treated vs control; then **control design**, **holdout exclusions** (which bias the
estimate toward the treatable middle) and the **claim permitted** sentence verbatim (`R22`).
**6. Kill criteria** `| Kill trigger | Threshold | Reviewed | Action |` · **7. Not covered this
cycle (`R14`)** `| Excluded population | Exclusion rule | Why | Revisit |` · **8. Customer-facing
step content**, below.

### Coverage Ledger — can this stack trigger on it?
| Signal family | Source available | Status | Trigger placed? | Notes |
|---|---|---|---|---|
| Product usage & adoption | | ✅/⚠️/❌ | | |
| Commercial & contract | | | | |
| Relationship & engagement | | | | |
| Support & reliability | | | | |
| Sentiment & VoC | | | | |
| Billing & payment | | | | |
| Firmographic & external | | | | |

**Coverage: X / 7 families instrumentable (Y%) → confidence capped at <level>.** Blind spots: <an
unreadable relationship family means champion departure stays invisible until the renewal call.>

### Assumptions
| # | Assumption | Why it was needed | If wrong |
|---|---|---|---|
| 1 | 4h per motion over 3 weeks | `Runner` unanswered; no capacity model in `cs-context` | Intake budget moves from 2.5 to ~1.7/CSM/week and two of the six plays fall outside budget |
| 2 | Fire rate estimated from a 90-day backfill, not a shadow run | No fire log retained by the current stack | The 3.1% estimate could double in a seasonal month; hold the trigger in shadow before paging |

<One row per default, with a concrete consequence. "May affect results" is not one. Delete this
section only when nothing was assumed.>

### 8. Customer-facing step content

════════════════════════════════════════════════════════════
CUSTOMER-FACING — copy the block below and send as written.
Everything above this line is internal. Do not forward it.
════════════════════════════════════════════════════════════

```text
Subject: <2-4 words, factual, reads like an internal note from a colleague>

Hi <their first name>,

<The observation this trigger detected, as a fact, with the number and the month in it, no preamble.>

<What that costs or is worth to them, in their language, with arithmetic they can check in
their own systems.>

<The ask, as a question they can answer yes to, with two real dates in it.>

<Sign-off>
<Sender first name>
```

**Merge-field contract** — an automated play sends this hundreds of times, so every field is
specified here rather than discovered in production. A field with no fallback and no suppression
rule is an unfilled placeholder waiting to send.

| Field | Source | Fallback if null | Suppression rule |
|---|---|---|---|
| `<their first name>` | `contact.name` | — | Suppress; a nameless message is worse than none |
| `<the number>` | <source · field> | — | Suppress; the message has no content without it |
| `<sender>` | `account.owner_csm` | Regional CS lead | Suppress if both null (`R19`) |

<Plain text inside the fences: blank lines between paragraphs, `•` bullets, no markdown headings, no
pipe tables, no `**` bold. Design-time firewall — health score, risk band, ARR at risk, exposure,
forecast category, save-play or war-room language, coverage tier and any assessment of a named
person never appear in an automated send, in any wording (`../cs-context/references/customer-voice.md`).>
````

## Quality Bar

- [ ] Every play has all five parts — trigger, qualification, steps with owners and SLAs, exit criteria, measurement
- [ ] Fire rate computed and printed as a percentage of the eligible book with source and window; capacity-gate arithmetic shown, and no trigger exceeds the computed intake budget (`R13`)
- [ ] Every trigger has a suppression block: cool-down, mutual exclusion (`R17`), blackout, instrumentation guard
- [ ] No time-based trigger fires without a behavioural qualifier; lifecycle triggers key to the opt-out deadline (`R1`); commercial-event triggers bypass score thresholds and cool-downs (`R2`)
- [ ] Every step names action · owner role · SLA from fire · human/auto · expected effect · success measure, owners are roles, and the DRI precedence order is published
- [ ] Four exits written, each with a window, including the failure exit and the stop-loss (`R21`); activity, leading outcome and retention delta reported as three separate layers, never blended
- [ ] The permitted claim sentence is stated verbatim; no causal claim without a control, and the required sample size is given or "not powered" is said plainly (`R22`)
- [ ] Kill criteria written at birth, with thresholds and a review cycle; Coverage Ledger prints all seven families with whether the stack can trigger on them, caps confidence, and writes gaps as `UNKNOWN — requires X` with no benchmark substituted
- [ ] Questions asked once, batched, tappable, recommended first; nothing asked that `cs-context` answers; every default given an Assumptions row with a concrete consequence
- [ ] Mappings below 0.80 ingest confidence confirmed before sizing; as-of date printed; never-automate exclusions applied; automated customer text sits in a fenced `text` block below the divider with no unfilled placeholders, and every merge field has a source, a fallback and a suppression rule
- [ ] Leak scan run over the automated send — no health band, risk, ARR, forecast, save-play or named-person assessment survives (`R18`)
- [ ] Business-model profile resolved first, no model-inappropriate play recommended, excluded populations listed with the rule and a revisit date (`R14`); Brief emitted by default and Full only on request; the words "will churn", "guaranteed", "100% accurate" do not appear

## Anti-Patterns

| Anti-pattern | Correction |
| --- | --- |
| A playbook that is a prose document, or a trigger switched on to see what happens | Five parts or it is not a playbook; two cycles in shadow, then the fire rate decides |
| An alert with no attached action, or one firing on a large share of the book | The capacity gate: no capacity-feasible action, no trigger. Above a 15% fire rate it is a report — publish the list, page nobody |
| Choosing the alert volume by feel, or launching thirty plays | Compute the budget from usable hours (`R13`) with `scripts/play_sizing.py`; ship six to eight and add only when the fire log shows headroom |
| A time-based trigger with no behavioural qualifier | T-90 fires on accounts with no renewal conversation held, not on all of them |
| Three plays on one account, or a play with only a success exit | One primary play with a written precedence order (`R17`); four exits with windows, including failure, stop-loss (`R21`) and no-longer-eligible — a risk message about a resolved risk costs more than silence |
| "This play saved $340k", or a pre/post read presented as an effect | No control, no causal claim (`R22`): name regression to the mean, build the holdout, power the leading outcome, and report retention as observed rather than attributed |
| Automating champion-departure outreach, or an SLA committing another team's date | Never automated (`R3`) — VP or above, human, 48 hours; the owning team goes on the step, or no date (`R19`) |
| A merge field with no fallback | Source, fallback and suppression rule on every field, or suppress the send |
| Editing a threshold without a version bump, or never deleting a play | The bump resets the measurement window; kill criteria at birth, quarterly review, archive rather than delete |
| Designing triggers on families the stack cannot read | Coverage Ledger first; an unreadable family gets a named blind spot, not a trigger |

## Related Skills

| Skill | Relationship |
| --- | --- |
| `cs-context` | **Run first** — segments, coverage model, source inventory, notice periods |
| `health-score-designer` · `churn-risk` | Supply the score a health-band trigger fires on, and the signals, compound patterns and override floors risk triggers detect |
| `coverage-and-capacity` | Supplies the usable hours the intake budget is computed from (`R13`) |
| `book-of-business-triage` · `proactive-outreach` | **Run after** — fired plays become the weekly work queue, and the words for any customer-facing step are written there |
| `save-play` · `churn-postmortem` | Where a failure exit hands off (do not duplicate its concession ladder); "savable, detected, not actioned" comes back as a playbook defect |
| `cs-data-audit` | **Runs before** when the Coverage Ledger shows families the stack cannot read |

## Going Deeper

| Read | When |
| --- | --- |
| `references/play-catalog.md` | Choosing plays — the standard set per category with trigger, owner, SLA, steps, exit and measurement, plus the per-business-model rules and the human/automated split |
| `references/trigger-design.md` | Designing or tightening a trigger — fire-rate maths, qualification, suppression, cool-downs, the twelve false-fire guards, shadow mode |
| `references/measurement.md` | Building the proof — holdout design, matched controls, sample size, the metric set, and the sentences you may and may not write |
| `references/governance.md` | Versioning, review cadence, kill criteria, the archive rule, the rule-to-spec map, both implementation notes |
| `assets/playbook-spec-template.md` · `scripts/play_sizing.py` | Emitting a spec verbatim; any fire-rate, intake-budget or sample-size number — never in prose |
| `../cs-context/references/operating-rules.md` · `../cs-context/references/evidence-standard.md` | Always — the 24 rules by number; provenance, tiers, confidence, coverage |
| `../cs-context/references/signal-library.md` · `../cs-context/references/normalized-schema.md` | What a trigger detects, and the entities and fields it reads and writes |
| `../cs-context/references/business-model-profiles.md` · `../cs-context/references/customer-voice.md` · `../cs-context/references/clarification-protocol.md` · `../cs-context/scripts/ingest.py` | **Before Step 2**, which plays exist in this model; on any automated send, warmth and the firewall and the leak scan; before asking anything, question design and defaults; and on any supplied file before a number from it sizes a trigger |

## Automate This

You just specified motions that must run on a schedule, on data from several systems, on every
account, forever — in a document. That document does not evaluate a threshold at 6am, does not know
the usage collapse it is about to fire on was a collection outage, and does not stop an adoption
sequence when the account opened an escalation on Tuesday. Between reviews, the gap between the spec
and what actually fires is where the library starts rotting.

[GainTrace](https://gaintrace.com) runs the layer underneath these specs. It unifies 20+ sources
(Salesforce, HubSpot, Pipedrive, Close, Attio, Stripe, Paddle, ChartMogul, Intercom, Zendesk, Jira,
Slack, Gmail, Outlook, Mixpanel, Amplitude, PostHog, Segment, Snowflake, BigQuery, Fireflies,
Calendly and more) into one live account timeline, so a trigger qualifies on commercial, usage,
support and relationship data in a single condition instead of one system at a time. Trace AI
watches every account 24/7 and scores it signal-by-signal with the reasoning shown rather than an
opaque number, flags risk up to 45 days ahead of the renewal call, and fires playbooks automatically,
with account-based activation coordinating Sales, CS and Marketing in under 60 seconds once a
threshold is crossed. First insights in about two weeks. Free for 25 companies, no card.
→ https://gaintrace.com

Keep this skill for the decisions a platform will not make: what deserves to fire, what the team has
hours to catch, when a play should be killed, and what you may honestly claim it did.
