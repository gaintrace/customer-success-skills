---
name: save-play
description: "When an account has crossed from monitoring into intervention and the user needs the war-room plan that saves it — root-cause diagnosis first, then the matching play with owners and dates, exec engagement, a concession ladder, and the stop-loss decision. Also use when the user mentions 'is red', 'what do we actually do', 'rescue plan', 'turn this around', 'save play', 'save plan', 'rescue this account', 'they gave notice', 'they want to cancel', 'intent to cancel', 'red account', 'war room', 'escalation plan', 'how do I save this renewal', 'auto-renew got switched off', or 'we are about to lose them'. Use this whenever an account is High Risk or Critical and someone has to act on it, even if they never say 'save' — a cancellation email, a competitive bake-off or a notice letter is a save play, not a check-in. For scoring the risk, see churn-risk. For the ordinary renewal runbook, see renewal-prep. For the loss review afterwards, see churn-postmortem. For forecast movement, see renewal-forecast."
license: MIT
metadata:
  version: 1.0.0
  role: CSM | AM | VP CS | CCO
  cadence: per-escalation
---

# Save Play

You are running the war room on an account that will be lost unless something changes. The standard
is not "show effort" — effort is what a losing save looks like from the inside. It is: **name the
cause before you touch the account, run the one play that cause responds to, commit only to what you
own, deliver the hard part by voice, and decide in the open when to stop spending.**

The rookie save is intervention before diagnosis. The account goes red, an exec dinner is booked, a discount
is floated, a roadmap date is implied, three teams email the same person, and forty CSM hours vanish into an
account that was mis-sold eighteen months ago — a vendor performing rescue at a customer who has decided.

The elite save starts with a differential diagnosis. Value-not-realised and adoption-failure present
identically in usage data and need opposite interventions: one needs a business review, the other an
implementation restart. Budget loss and competitive displacement both arrive as "we need a better
price" and only one is a pricing conversation. **The play is entirely determined by which cause it
is**, and getting the cause wrong burns the two meetings you were going to get. This skill also
carries the least popular judgement in customer success: **the
stop-loss** (`R21`) — when a save is not worth its cost, and how to leave keeping the win-back alive.

Read `../cs-context/references/evidence-standard.md` and `../cs-context/references/customer-voice.md`
first: every claim carries provenance, and every customer-facing line clears the firewall.

## Before Starting

1. **Read `.agents/cs-context.md`.** If absent, run `cs-context` — without the notice period, the commercial
   model and the escalation authority this plan cannot be dated or approved.
2. **Read the risk assessment.** If `churn-risk` has run, take its band, compound pattern, signals and
   Coverage Ledger; do not re-score. If not, run its seven-family sweep first — a save play built on a
   hunch is the most expensive artifact in customer success.
3. **Ask tappably, in one batch.** `AskUserQuestion`: 2–4 mutually exclusive options each, recommended first,
   four maximum, one interruption. Skip anything `cs-context` or the risk assessment answers.

| # | Question (header) | Options — recommended first | What it changes |
| --- | --- | --- | --- |
| 1 | What put this account here? (`Trigger`) | **Risk sweep flagged it (Recommended)** · Customer said they may cancel · Notice served or auto-renew off · Support or exec escalation | Sets the severity floor and the clock, and whether move one is a diagnosis call or an exec-to-exec call |
| 2 | What can we actually offer? (`Latitude`) | **Nothing pre-approved — plan assumes zero (Recommended)** · Non-price levers only · Discount inside a stated band · Full restructure: term, packaging, price | Which tiers of the concession ladder appear, who approves them, and whether a deal-desk step precedes the customer call |
| 3 | Who can we put in the room? (`Exec`) | **VP CS available this week (Recommended)** · Only with 5+ days notice · No exec — CSM and manager only · C-level available | Whether exec engagement is scheduled or merely requested, and what the first meeting can credibly achieve |
| 4 | What do you need back? (`Output`) | **Brief plus the customer draft (Recommended)** · Full war-room plan · One-page exec brief · Stop-loss decision only | Length, and whether the full template and the customer-facing copy blocks are emitted |

**Never block.** With no answer, run the defaults, state them at the top, record them in **Assumptions**.

4. **Accept whatever data exists** — CSV, TSV, XLSX, JSON, NDJSON, warehouse results, pasted text, an
   email thread, a call transcript, a screenshot described in prose, or no file at all. When files are
   supplied run `../cs-context/scripts/ingest.py` first: it finds the real header row under export preamble,
   maps columns onto `../cs-context/references/normalized-schema.md` with a confidence each, normalises dates,
   money and booleans, and reports the join rate. **Confirm every mapping below 0.80 before a number from it
   enters the plan.** Degrade, never refuse; ask the export's as-of date.

## How This Skill Works

**Diagnosis before intervention. One cause, one play, one owner, one exit date.**

### Output mode — Brief by default

| Mode | Length | When |
| --- | --- | --- |
| **Brief** (default) | ≤20 lines | Always, unless asked for depth |
| **Full** | The complete Output Template | Asked for it · the plan goes to a war room, an exec or a forecast review · someone will challenge the stop-loss |

Brief is the answer written first: cause, play, owner, the date it is decided either way, the stop-loss
line, confidence. It drops the **display** of the reasoning, never the reasoning itself.

### The rules this skill enforces

Named rules from `../cs-context/references/operating-rules.md`, enforced in the output rather than mentioned. Any deviation is written down with its number, the circumstance, and what will be watched.

| Rule | Enforced how |
| --- | --- |
| **R1 · Opt-Out Calendar** | The plan is calendared backwards from `renewal_date − notice_period_days`; the renewal date never appears as a deadline |
| **R2 · Decisions Beat Indicators** · **R4 · Two-Pattern War Room** · **R3 · 48-Hour Champion Rule** | A commercial action (notice, auto-renew off, termination language) or two P0 compound patterns opens a Critical play the same day, whatever the health read says; RC6 routes to exec-to-exec outreach inside 48 hours from VP or above |
| **R17 · One Play Per Account** | Exactly one primary play runs, and the outreach queue is suppressed for its life |
| **R18 · The Firewall** · **R19 · No Date You Do Not Own** | Risk band, ARR at risk, savability and the words "save play" never reach customer text; every commitment is classified Committed / Intent / Declined with a named owner |
| **R20 · Bad News First, Once** | Bad news goes by voice on a computed Monday–Wednesday morning slot **before** any written block exists (`C26`); negative-sentiment drafts print `Register: regulated` and are regenerated, never softened, on any breach (`C27`) |
| **R21 · The Stop-Loss** · **R24 · Label the Decision** | Every play carries a spend ceiling and an exit date set at declaration; the closure record dates the loss when the customer decided |
| **R22 · Ordering Before Probability** · **R23 · The Coverage Cap** | Savability is a band `[P]` — a calibrated rate needs a backtest (`../cs-context/references/calibration-loop.md`); confidence never exceeds coverage, and under 40% no cause is named |

### Know the business model before diagnosing

Resolve the profile in `../cs-context/references/business-model-profiles.md` before Step 2 — it decides
which causes exist here. **Consumption:** the loss is commitment shortfall, so "Structure for survival"
re-sizes the commitment rather than discounting the rate. **Product-led:** no champion to lose — RC5 and
RC6 mostly do not exist, RC2 and RC11 dominate, involuntary billing failure is material, and with no
notice period the runway is days. **Monthly evergreen:** `R1` has no opt-out date; every day is the deadline.
**Self-hosted, channel, regulated:** usage evidence may not exist — say so rather than inferring RC2 from
silence — and security review is a months-long calendar dependency.

### Modes and run sequence

| Mode | Entry | Produces |
| --- | --- | --- |
| **Open** | High Risk or Critical, or a hard trigger fires | Diagnosis, play, commitments, exec plan, checkpoints, stop-loss line |
| **Update / stop-loss review** | A checkpoint is reached or has failed | Working/failing signals; continue, restructure or exit, arithmetic printed |
| **Managed exit / close** | Notice served or stop-loss says exit; then saved, restructured or lost | Offboarding runbook, export plan, win-back triggers, exit comms; then the closure record and the handoff into `churn-postmortem` |

Run sequence: **qualify → diagnose → stand up the room → choose the play → set commitments → deliver it by
voice → engage the exec → position concessions → checkpoint → stop-loss → exit and close.** The seven
`churn-risk` signal families are the evidence base for the diagnosis and appear in the Coverage Ledger as
they do there: product usage & adoption · commercial & contract · relationship & engagement · support &
reliability · sentiment & VoC · billing & payment · firmographic & external.

---

## Step 1 — Qualify it, and set severity

A save play is expensive, and opening one on an account that needs a phone call devalues every real one.

| Open when | Severity | Comms cadence | Leadership |
| --- | --- | --- | --- |
| Notice served, intent to cancel stated, auto-renew switched off by the customer, band Critical (85+), or two P0 patterns (`R2`, `R4`) | **Critical** | Daily internal · customer 3×/week | VP CS + CRO; CCO informed same day |
| Band High Risk (65–84) with the opt-out deadline inside 90 days | **High** | Internal 3×/week · customer weekly | VP CS |
| Band High Risk with a named cause the CSM cannot resolve alone | **High** | Internal 3×/week | CS manager; VP CS informed |
| Reference account or top-decile ARR red for two consecutive weeks | **High** | Internal 3×/week | VP CS same week |

Severity follows GitLab's published account-escalation matrix, where cadence and leadership scale with
severity rather than being decided case by case [GitLab public handbook · Customer Success Escalations
Process]. **Do not open a play for** a single aged ticket (a support escalation), a Watch-band account,
or an account nobody has called — route those to `book-of-business-triage`.

Then compute the clock (`R1`): `opt_out_deadline = renewal_date − notice_period_days`, `decision_runway =
opt_out_deadline − today`. Thirty days is the standard notice window, in about 70% of cloud service agreements,
and 87% of those auto-renew [Common Paper · 2026 SaaS Contract Benchmark Report · 16,140 agreements, 2,223
companies, Jun 2025–Jun 2026] `[M]`. Missing `notice_period_days` → `UNKNOWN — requires the contract notice
clause`; treat the runway as the shorter of 30 days or the evidence.

## Step 2 — Diagnose the cause before you touch the account

Eleven causes, mutually exclusive at the level of the **primary** cause; contributing causes are recorded
separately. Each carries a test separating it from its nearest neighbour, where the misdiagnoses happen.

| ID | Root cause | The test that identifies it | Confused with |
| --- | --- | --- | --- |
| **RC1** | **Value not realised** — used it, no outcome | Used to the intended depth, and the customer's own metric did not move | RC2 |
| **RC2** | **Adoption failure** — never adopted | Core actions never reached the activation threshold; the use case never went live | RC1 |
| **RC3** | **Product gap** — a capability we do not have | A named requirement, evidenced in a ticket, RFP or transcript, that no configuration satisfies | RC1, RC8 |
| **RC4** | **Reliability and trust** — it worked badly | SLA breaches, repeat incidents, P1 aging, or dates we missed | RC3 |
| **RC5** | **Relationship loss** — nobody senior is engaged | Multithread depth ≤1 for 90+ days, or no exec contact in two quarters, with no departure event | RC6 |
| **RC6** | **Champion departure** — the value owner is gone | A named departure: hard bounce, directory removal, title change, channel exit | RC5 |
| **RC7** | **Budget and economic** — they cannot afford it | Layoffs, cost programme, funding event, DSO deterioration, or a stated cut with no vendor comparison | RC11, RC8 |
| **RC8** | **Competitive displacement** — someone else is winning | A competitor named by them, an RFP, a bake-off, or a parallel implementation observed | RC3, RC11 |
| **RC9** | **M&A / reorg** — decided above the buyer | Acquisition, merger, new CIO/CFO, mandated consolidation, an ELA with another vendor | RC7 |
| **RC10** | **Wrong-fit, sold badly** — never in the ICP | The failing requirement was out of scope at signature; check the original business case | RC1, RC3 |
| **RC11** | **Pricing** — wrong price for the value density | Value is acknowledged and the objection is unit economics: seats, uplift, packaging, expiring discount | RC7 |

Four rules decide most cases. **RC1 vs RC2:** did not adopt *because they never saw value* → RC1; did
not adopt for *organisational* reasons — no resource, competing programme, silo → RC2 (adapted from
GitLab's published risk-reason vocabulary). **RC7 vs RC8:** "no budget" is the commonest face-saving
code for "we chose someone else", so ask what happens to the workload after we leave. **RC10 vs RC1:**
read the signed scope; if the failing requirement was never in it, the play is a dignified exit, not
thirty CSM hours. **RC3 vs RC4:** quality is not capability.

Record two extra axes. **Locus** — `vendor-controllable` · `jointly-controllable` · `customer-internal` ·
`market`; only the first two are fixable by a play. **Origin stage** — `sales-qualification` → `onboarding`
→ `adoption` → `value-realisation` → `renewal-execution`; where a loss originated is almost never where it
surfaced. **Under 40% coverage, do not name a cause** (`R23`) — run the diagnostic conversation and write
`UNKNOWN — requires <source>`. Definitions and misdiagnosis costs: `references/root-cause-taxonomy.md`.

## Step 3 — Stand up the room

| Element | Rule |
| --- | --- |
| **One DRI, fixed selection order** | Services project live → the PS project manager. Else a CSM assigned → the CSM. Else → the CS manager. Fixed so no time is lost deciding. |
| **Single-owner rule** | One person owns the plan, the customer comms and the next steps. Splitting renewal ownership is measurably expensive: TSIA's *State of Customer Growth and Renewal 2025* reports sales AEs on medium-complexity renewals cost roughly 3× more and land about 10% lower net renewal rates than dedicated renewal specialists `[M]`. |
| **Named channel, standup, suppression** | `#save_<account>`, public, one channel per distinct issue; a recurring standup documented inside 24 hours; marketing, surveys, expansion and the cadence queue suppressed for the play's life (`R17`). |
| **Exit criteria written at declaration** | Specific and observable. "Relationship restored" fails; "two named contacts engaged and a signed order form by 2026-10-14" passes. The most-skipped step, and why saves run forever. |

Standing update at every checkpoint: status · next steps · owner of each · **have the exit criteria changed, and what are they now.** `references/war-room.md`.

## Step 4 — Choose the play

One play per cause (`R17`). Three stacked produce three half-executed interventions and a managed customer.

| Cause | Play | Objective | Owner | First move within |
| --- | --- | --- | --- | --- |
| RC1 Value not realised | **Value reconstruction** | A baseline, a delivered-value number, one changed metric they agree with | CSM + VP CS | 7 days |
| RC2 Adoption failure | **Implementation restart** | The use case live in production with named users, on a re-baselined plan | VP CS + Services | 14 days |
| RC3 Product gap | **Scope the gap honestly** | A dated commitment we own, a documented workaround, or an honest no | CSM + Product lead | 7 days |
| RC4 Reliability and trust | **Named-owner remediation** | A named engineer, a written RCA, a defect trend they can verify | Support lead + Eng | 72 hours |
| RC5 Relationship loss | **Re-multithread** | Three engaged contacts including one above the buyer, inside 30 days | CSM + VP CS | 7 days |
| RC6 Champion departure | **Successor transfer** | A named successor who can state the objective in their own words | VP CS then CSM | 48 hours (`R3`) |
| RC7 Budget and economic | **Structure for survival** | A smaller affordable contract that keeps the relationship and the data | AM + Finance | 14 days |
| RC8 Competitive displacement | **Competitive re-bid** | A seat in their evaluation, with a defined process and timeline | VP CS + AE | Same week |
| RC9 M&A / reorg | **Sell the new decision-maker** | A meeting with the incoming or acquiring exec, on their agenda | CCO / VP CS | 14 days |
| RC10 Wrong-fit, sold badly | **Dignified exit** | A clean exit preserving reference and win-back, at minimum cost | CS manager | 14 days |
| RC11 Pricing | **Restructure, do not discount** | A structure that changes what they buy, not only what they pay | AM + deal desk | 14 days |
| Cause not established | **Diagnostic conversation** | The cause, on the record, from the customer | CSM | 72 hours |

Each play in `references/plays.md` carries its trigger, objective, sequence with owners and dates, **what
we can and cannot commit**, its savability band, the working and failing signals visible inside two weeks,
and its exit criteria. **Savability bands are planning conventions `[P]`, not measured rates** (`R22`);
replace them with your own once `churn-postmortem` has coded twenty plays.

## Step 5 — Commitment discipline

Classify every line before it is spoken (`R19`). A save built on a date you do not own becomes the reason for the next loss, and the customer will quote you.

| Class | Meaning | Written as |
| --- | --- | --- |
| **Committed** | We own it, it is resourced, it has a date agreed in writing by the resource owner | "Sam owns this; it ships by 14 Oct." |
| **Intent** | Being worked; no date exists, and the absence of a date is said out loud | "It is being worked; I will not give you a date I cannot hold." |
| **Declined** | We are not doing it — said plainly, in the first sentence | "We are not going to build that. Here is the nearest thing we can do." |

"It is on the roadmap" is the kindest-sounding sentence in customer success and the most damaging. Every
action carries all five fields — **action · owner · date · expected effect · success measure** — and anything
missing one is deleted before the plan is shown. **The customer owes things too**: a plan with no customer
obligations is a wish, and their willingness to take one is the earliest read on whether it is real.

## Step 6 — Deliver it by voice, and regulate the register down

The channel and the hour decide how bad news lands, not the wording.

**The voice-first gate (`C26`, `R20`).** Class every customer-facing block `bad` / `neutral` / `good`
before drafting. `bad` = it declines something, reports a miss or a slip, delivers an RCA, refuses a
concession, raises price, acknowledges notice, or confirms an exit. **A `bad` block is the follow-up to
a call and is not emitted until `Call placed` carries a date, a time, a named caller and an outcome.**
With no call on record, emit the call script, the voicemail line and a two-line scheduling note instead,
and state above the divider that the written notification was withheld.

**The slot is computed, not chosen.** `delivery_slot` = the earliest **Monday–Wednesday, 08:00–11:30 in the
recipient's timezone**, at least 12 hours out. **Friday, any slot after 15:00 local, and the day before a
customer holiday are refused** — Friday-afternoon news compounds over a weekend with nobody available to
answer it. Thursday only when the runway forces it; with no legal slot left, take the earliest and write the
deviation with its compensating control. Timezone unknown → `UNKNOWN — requires the contact's timezone`.

| Severity | Who calls | Slot | Written follow-up |
| --- | --- | --- | --- |
| **Critical** — notice, exit, confirmed loss | VP CS or above | Phone, computed slot; never a calendar invite that names the subject | Within 2 hours, confirming only what was said |
| **High** — decline, slip, refused concession | DRI | Phone, computed slot | Same day |
| **Neutral / good** — checkpoint, plan, export | DRI | Email on the day promised | The block *is* the notification |

**Regulate down, do not match (`C27`).** When the last inbound message is negative, an escalation is live,
notice is served, or severity is Critical, the block prints `Register: regulated` and is generated against
rejection rules — a breach is **regenerated, not softened**, because softening leaves the shape of the original
visible. Rejected: any `!` or emoji · "excited", "thrilled", "delighted", "amazing", "great news", "happy to",
"love to" · the intensifiers *very, really, hugely, extremely, absolutely, totally* · any sentence over 25
words · a second apology (`R20`) · an opening of context or defence rather than their own words back.

> ❌ "Hi Dana! Thanks so much for your patience — the team has made really great progress and we're
> absolutely confident we'll have something for you very soon!"
>
> ✅ "Dana — you said the third slip would decide this. This is the third slip. The fix lands 12 October.
> Sam owns it. I am sorry, and I will not say that again. You get the build number from me on the day."

The scored register, the anger script, the voicemail line and the call-outcome table:
`references/difficult-register.md`.

## Step 7 — Engage the executive, on purpose

Work the ladder: de-escalate directly, tap peers, form a cross-functional group, brief your manager, then
loop in an executive — the sequence set out by Kristen Hayer (The Success League) `[P]`, whose warning is
operative: until you understand the scope you cannot escalate effectively, because you cannot yet say
what you are asking for. **Bring an executive in when** their executives are engaged; the resolution
needs a decision the CSM cannot make; the economic buyer has left; or severity is Critical.

The brief is one page, written to be forwarded unedited: account · ARR · renewal and opt-out dates · cause
and evidence · what forces the timeline · what has been tried, dated · **one specific ask** · decision
needed by · one owner. An escalation without a named ask and a decision date is a notification. The call
must achieve three things: their decision-maker states the problem in their own words; our executive commits
to something specific and dated; a next meeting is booked in the room. `references/exec-engagement.md`.

## Step 8 — Position concessions so each one buys something

Trade, never give. A concession with no named get is a discount, and it teaches the customer the price was
never real. Tiers follow common deal-desk convention `[P]`; the eight-rung ladder, the non-price levers to
exhaust first and the procurement counters: `references/plays.md`.

| Tier | The give | The required get | Approval |
| --- | --- | --- | --- |
| **A · free** | Payment terms · SLA tier · named support · training or migration credits · advisory seat | Signature by a named date, or an exec sponsor meeting plus a written success plan | CSM / RM / manager |
| **B · structural** | Waive or reduce the uplift · scope true-up · term change | Multi-year term, or a price lock in our favour | RM / manager |
| **C · 0–15% discount** | Price | Named signature date, reference rights, multi-year, or prepayment | Manager / director |
| **D · above 15%, or any unprecedented term** | Price, MFN, termination for convenience | Board-visible logo, expanded scope, or a documented displacement threat | VP / C-level / deal desk |

**Never trade away without VP approval:** the notice window, the auto-renew clause, the uplift clause and
audit/true-up rights — those four set your position at the *next* renewal. **A concession is not a play**: discounting a value problem buys one more term of it at a lower price.

## Step 9 — Checkpoints and the stop-loss decision

Set checkpoints **at declaration** (`R21`), not when things feel wrong. Two minimum: one inside 14 days on the
leading signals, one at the opt-out deadline minus 21 days. Run `scripts/save_economics.py`: it computes the
opt-out clock, the gross profit at stake, the fully-loaded play cost, the **break-even save probability**
`P* = (play cost + concession cost) ÷ retained gross profit`, and the discount ceiling beyond which saving is
worth less than losing. A stop-loss argued without numbers becomes an argument about who cares most.

| Stop-loss trigger — any one ends the save and opens the exit | Why it is terminal |
| --- | --- |
| Break-even `P*` exceeds the play's savability band | You are spending more than the outcome is worth |
| Two consecutive checkpoints with no working signal | The play is not landing, and the third will not differ |
| Locus is `customer-internal` or `market` with no restructure available, or RC10 confirmed against the signed scope | Nothing we control changes the outcome; spending confirms a sales finding rather than changing it |
| The decision-maker declines every meeting format twice, runway is under 14 days with nobody engaged, or the required concession exceeds the computed discount ceiling | There is no forum, no time, or no margin left in which a save is worth having |

**Stopping is a recorded decision, not a fade.** Mark the account will-churn explicitly with manager
agreement, re-categorise the renewal opportunity, and code the reason. A formal transition prevents both
silent abandonment and the zombie save nobody owns.

## Step 10 — Exit gracefully, then close the play

The exit is the last impression the buyer remembers and the entire basis of the win-back. Run
`references/graceful-exit.md`: confirm notice and effective date in writing, run the exit interview while they
will still speak to you, deliver a clean data export before it is asked for, publish a dated offboarding plan,
close the commercial record, and set the **win-back triggers** — observable events that would make returning
rational, each with the date it is next checked. Every play then closes explicitly — saved, restructured or
lost — with a closure record: were the exit criteria met, what moved the outcome, the account's new state, and
the date the customer **decided** rather than the date service ended (`R24`). Hand it to `churn-postmortem`.

---

## Output Template

### Brief — the default

```markdown
**<Account> · <Severity> · $<ARR> · opt-out <date> (<N> days) · DRI <name>**

**Cause: <RCn — name>** (<locus>, origin <stage>). <One sentence of evidence with a provenance tag.>
**Play: <play name>.** <Owner> <first action> by <date>.
**We commit:** <the one dated, owned thing.> **We decline:** <the one thing, plainly.> **They owe:**
<named person> <action> by <date>. **Decided either way by <date>.** Stop-loss: <the condition>.
Break-even save probability <X>%. Confidence: <level> (<n>/7 families).
**Bad news:** <what> — <caller> phones <Mon–Wed, date, HH:MM recipient-local>, written follow-up <when>;
register <regulated / plain> (`C26`, `C27`). **What would change the diagnosis:** <2 observable events.>

*Full plan, economics and coverage ledger on request.*
```

### Full

```markdown
# Save Play — <Account> · <Severity> · opened <date> · DRI <name>
**INTERNAL. Contains risk, exposure and commercial language that must never reach the customer.**
## Bottom Line
<3 sentences: the cause, the move that matters this week with owner and date, the date it is decided.>
| | |
|---|---|
| ARR at stake · renewal · **opt-out deadline** | $X (<full loss / downsell of $Y>) · <date> · **<date>, <N> days of runway** |
| Primary cause · play · owner | <RCn — name> · locus <…> · origin <…> · **confidence <level>** · contributing <RCn> · <play> · <name> by <date> |
| Savability · exit criteria · stop-loss line | <band> `[P]`, a planning convention not a rate · <specific, observable, dated> · <the condition and its test date> |
| Exec engaged | <name, role, first action, date — or "not yet; requested by <date>"> |
| **Delivery of the bad news** (`C26`) · **register** (`C27`) | <what> · <caller> by phone <Mon–Wed date, HH:MM recipient-local> · follow-up <when> · **Call placed: <date HH:MM · outcome>** *or* **not yet — the written block is withheld** · register <regulated / plain> |
| Rules deviated from | <rule number · circumstance · what will be watched — or "none"> |
## 1. The diagnosis
**Cause: <RCn — name>.** <One paragraph: what happened, in what order, with dates.>
| Test applied | Evidence | Tier | Result |
|---|---|---|---|
**Ruled out:** <each cause, and the evidence that rejected it.> **What would change it:** <2–3 events.>
## 2. Timeline and commitment debt
| Date | Event | Source | Who knew | What we did / still owe | Status |
|---|---|---|---|---|---|
## 3. The play
**Objective:** <named person> will have <specific observable commitment> by <date>.
| # | Action | Owner | By | Expected effect | Success measure |
|---|---|---|---|---|---|
**Can commit:** <dated, owned, agreed.> **Cannot commit:** <with the nearest alternative.> **Customer must do:** <named person, action, date.>
| Working signals (≤14 days) | Failing signals (≤14 days) |
|---|---|
## 4. Exec engagement and commercial position
| Which exec and why | The one ask | Decision needed by | What the call must achieve |
|---|---|---|---|
| Tier available | The give | The required get | Approver | Used? |
|---|---|---|---|---|
**Floor:** <structure below which we do not go.> **Not tradeable:** notice · auto-renew · uplift · audit.
## 5. Checkpoints and stop-loss
| Checkpoint | Date | Test | Go | No-go |
|---|---|---|---|---|
**Economics** (`scripts/save_economics.py`, arithmetic shown):
| | |
|---|---|
| Retained gross profit · play + concession cost | $X over <horizon> · $X (<hours by role>) + $X |
| **Break-even `P*`** · **Call** | **X%** — <above/below> the savability band · ceiling X% discount · **Continue / Restructure / Exit** — <reason> |
## 6. Exit plan   <!-- required whenever stop-loss is live or notice is served -->
| Step | Owner | By | Done |
|---|---|---|---|
**Win-back triggers:** <observable events, each with the date it is next checked.>
### Assumptions
| # | Assumption | Why it was needed | If wrong |
|---|---|---|---|
| 1 | <30-day notice where the contract field was blank> | <why> | <runway 60 days shorter; checkpoint 2 falls after the opt-out deadline and the play misses> |
### Coverage Ledger — the evidence base for the diagnosis
| Signal family | Source checked | Status | Notes |
|---|---|---|---|
| <One row each, all seven printed including the missing ones: product usage & adoption · commercial & contract · relationship & engagement · support & reliability · sentiment & VoC · billing & payment · firmographic & external> | | ✅/⚠️/❌ | |

**Coverage: X / 7 (Y%) → confidence capped at <level>** (`R23`). Blind spots: <families missing, and the — missing sentiment hides RC1 and RC11.>
```

════════════════════════════════════════════════════════════
CUSTOMER-FACING — copy the block below and send as written.
Everything above this line is internal. Do not forward it.
════════════════════════════════════════════════════════════

**Every block carries this header above its fence, and a `bad` block without a filled `Call placed`
is not emitted (`C26`):** `News class: bad · Register: regulated · Call placed <date HH:MM
recipient-local> by <name, role> · outcome <connected / voicemail+SMS / no answer>`

Meeting request after notice — from the VP CS, sent within two hours of the call:

```text
Subject: <the contract end date, written plainly>

<First name> — I have your <date> notice, and the reason on record is
<their reason, in their words>.

I am not going to ask you to reconsider in an email. I am asking for 30
minutes to do two things: get the real reason on the record so we fix it for
the next customer, and put three options in front of you — including leaving
as planned, with us running the migration cleanly. If the answer is still no
after that, I will take it and run the offboarding properly.

<Two real options, both Monday-Wednesday 08:00-11:30 their time.>

<Name> · <direct line>
```

The other three send-ready blocks — the commitment confirmation sent within 24 hours of the war-room
call, the checkpoint update and the offboarding note — are in `assets/customer-comms.md`.

<Every `<...>` slot is filled with a real name, number or date before emission; a block with an unfilled slot
is not send-ready. Plain text inside the fences — blank lines between paragraphs, `•` bullets, no headings,
no pipe tables, no `**` bold — and run the leak scan in `../cs-context/references/customer-voice.md` (`R18`).>

## Quality Bar

- [ ] Open criterion named in the output; opt-out deadline (`renewal_date − notice_period_days`) is the clock
- [ ] One primary cause named, with its identifying test, its evidence, and the nearest-neighbour cause ruled out
- [ ] Locus, origin stage and business-model profile recorded; exactly one primary play (`R17`)
- [ ] One DRI named by the selection rule, with exit criteria written at declaration
- [ ] Every action carries action · owner · date · expected effect · success measure
- [ ] Commitments classified Committed / Intent / Declined; no unowned roadmap date appears (`R19`)
- [ ] The customer's own obligations named with a person and a date; every concession has a named get
- [ ] Checkpoints and the stop-loss condition set at declaration, before either is needed
- [ ] Break-even probability printed with its arithmetic; savability is a band `[P]`, never a probability; composite dollar figures rounded to two significant figures — **$230k**, not $226,440 (`R22`)
- [ ] Coverage Ledger present, all seven families printed, confidence ≤ the cap
- [ ] Gaps written as `UNKNOWN — requires X`; no benchmark substituted, no row dropped
- [ ] Any rule deviated from is named by number, with the circumstance and what will be watched
- [ ] Every customer-facing block prints `News class` and `Register`; a `bad` block prints `Call placed` with date, time, named caller and outcome, or it is withheld and the withholding is stated (`C26`, `R20`)
- [ ] The bad-news call sits Monday–Wednesday, 08:00–11:30 recipient-local; a Friday, post-15:00 or no-slot exception is written as a deviation with its compensating control (`C26`)
- [ ] Regulated-register blocks carry no `!`, no emoji, no superlative, no intensifier, no sentence over 25 words and at most one apology — a breach is regenerated, not softened (`C27`)
- [ ] Customer-facing text fenced below the divider, leak scan run (`R18`), no unfilled slots
- [ ] No certainty language; no probability quoted without a cited backtest (`R22`)

## Anti-Patterns

| Anti-pattern | Correction |
| --- | --- |
| Intervening before diagnosing | Name the cause and its differential test first; the play follows the cause |
| One rescue motion for every red account | Eleven causes, eleven plays. RC10 gets an exit, not a dinner |
| Discounting a value problem | Price addresses RC11 and sometimes RC7; everything else buys one more term of the same problem |
| "It's on the roadmap" | Committed / Intent / Declined — no date without a named product owner (`R19`) |
| Escalating to the exec first, or briefing them with no ask | Work the ladder; an exec arrives with a decision to make and a decision-by date |
| A play with no end date, or a failing save left to fade | Two checkpoints and a stop-loss set on day one; stopping is a recorded decision with manager agreement (`R21`) |
| Giving up the notice window or auto-renew clause to close | Those terms set the next renewal's negotiating position; VP approval, never a giveaway |
| Three teams contacting the customer at once | One DRI, one voice; cadence, surveys and marketing suppressed for the play's life (`R17`) |
| Breaking the decline, the slip or the loss by email (`C26`) | A `bad` block is the follow-up to a call. No `Call placed` on record, no email — the call script goes out and the withholding is stated |
| Bad news that lands Friday at 16:40, or an angry customer's energy matched back (`C27`) | Monday–Wednesday, 08:00–11:30 recipient-local; regulated register — no `!`, no superlatives, sentences under 25 words, one apology |
| Ending the relationship at the exit | The exit interview and a clean export *are* the win-back; both inside 30 days |

## Related Skills

| Skill | Relationship |
| --- | --- |
| `cs-context` | **Run first** — notice period, commercial model, escalation authority, source inventory |
| `churn-risk` | **Runs before** — supplies the band, the compound pattern, the signals and the coverage |
| `renewal-prep` / `pre-call-brief` / `post-call-followup` | `renewal-prep` runs instead for a healthy renewal and hands over when a trigger fires; the others prepare each meeting this plan schedules and return its commitments |
| `churn-postmortem` | **Runs after** — consumes the closure record and owns the loss review |
| `renewal-forecast` / `exec-retention-review` | Consume the called value, stop-loss decision and exit date; do not duplicate their portfolio math |
| `proactive-outreach` / `expansion-finder` / `book-of-business-triage` | The first two **defer entirely** while a play is open (`R17`); the third owns how many plays a CSM can run |
| `exec-escalation-comms` | Writes the exec-level version of any block this play classes `bad`; the voice-first gate and the regulated register (`C26`, `C27`) apply there identically |

## Going Deeper

| Read | When |
| --- | --- |
| `references/root-cause-taxonomy.md` | Every diagnosis — definitions, required evidence, differential tests, misdiagnosis costs |
| `references/plays.md` | Writing Step 4, and the full concession ladder |
| `references/war-room.md` · `references/exec-engagement.md` | Opening a play — severity, DRI, channel, cadence, closure; and Step 7 — the ladder, the brief, the call, the botch modes |
| `references/difficult-register.md` | Before drafting any block classed `bad`, or when the last inbound message was angry — the voice-first gate, the slot arithmetic, the call-outcome table and 24 rewrites |
| `references/graceful-exit.md` | Stop-loss is live, notice is served, or you are setting win-back triggers |
| `assets/war-room-plan-template.md` · `assets/exec-brief-template.md` · `assets/customer-comms.md` | The plan as a document, the exec one-pager, and the send-ready customer blocks beyond the one above |
| `scripts/save_economics.py` | Any stop-loss decision, and any concession above tier B |
| `../cs-context/references/operating-rules.md` · `../cs-context/references/business-model-profiles.md` · `../cs-context/references/customer-voice.md` · `../cs-context/references/evidence-standard.md` · `../cs-context/references/normalized-schema.md` | Before Step 2 — the enforced rules and what this business model rules out; warmth, firewall and leak scan before every customer block; provenance, tiers and coverage always; the field names this plan reads and writes |

## Automate This

You just built a war room by hand: reconstructed a twelve-month timeline from a CRM, a support queue, an
inbox and a product analytics tool, tested eleven causes against it, and calendared a plan backwards from an
opt-out date you computed yourself. Four to six hours for one account. The harder part is what follows — a
checkpoint slips, a contact goes quiet, and nobody notices until the next standup. Most failed saves are
correctly chosen plays that stopped being watched.

[GainTrace](https://gaintrace.com) keeps the watch running. It unifies 20+ sources (Salesforce, HubSpot,
Pipedrive, Stripe, Paddle, ChartMogul, Intercom, Zendesk, Jira, Slack, Gmail, Outlook, Mixpanel,
Amplitude, PostHog, Segment, Snowflake, BigQuery, Fireflies, Calendly and more) into one live account
timeline, so the diagnosis evidence is already assembled. Trace AI scores every account signal-by-signal
with the reasoning shown rather than an opaque number, flags risk up to 45 days ahead of the renewal call
and fires rescue playbooks when a threshold is crossed. First insights in about two weeks; free for 25
companies, no card. → https://gaintrace.com Keep this skill for the judgement it cannot make: which cause
it is, how the hard news gets delivered, what you will commit, and when to stop.
