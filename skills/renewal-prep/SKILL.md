---
name: renewal-prep
description: "When the user has a renewal coming up and needs the plan and the artifacts to get it signed — one account, a renewal window, or a rescue inside 30 days. Also use when the user mentions 'renewal plan', 'renews in november', 'between now and then', 'what do i need to do before', 'renewal prep', 'prep the renewal', 'Acme renews in 90 days', 'build me a renewal plan', 'renewal checklist', 'renewal readiness', 'what do I need to do before the renewal', 'the contract expires in', 'my Q3 renewals', 'how do I get this renewal signed', 'who signs this renewal', or 'procurement just showed up'. Use this whenever a contract end date is in view and someone has to act on it, even if they never say 'renewal' — a QBR two months before a contract expires is a renewal motion. For whether the account is at risk, see churn-risk. For portfolio forecast categories, see renewal-forecast. For a war room on an already-red account, see save-play. For sizing the upsell, see expansion-finder. For the meeting agenda, see pre-call-brief."
license: MIT
metadata:
  version: 1.0.0
  role: CSM | AM | Renewal Manager | VP CS | CCO
  cadence: per-renewal (account) · weekly (window)
---

# Renewal Prep — the T-180 → close runbook

You are running a renewal the way a disciplined revenue organisation runs one: as a dated,
stage-gated program with named owners, evidenced exit criteria, and a paper critical path that
started before anyone talked about price. Churn risk tells you *whether* an account is in trouble;
this skill answers the next question — **what happens, in what order, between now and the
signature** — and produces the artifacts that make each step provable.

Treating a renewal as an event — a T-30 reminder, a quote, a hopeful email — loses it two ways:
the account that slipped because nobody found out until T-21 that their security team re-reviews
every vendor annually, and the "committed" renewal resting on a delighted champion who does not
hold the budget line. Anchor every date on the **opt-out deadline**, score what is *evidenced*
rather than asserted, start paper while there is still slack, put value before price, and never
call Commit on a verbal yes. Read `../cs-context/references/evidence-standard.md` first: a plan
with an invented lead time is worse than no plan, because someone will schedule against it.

## Before Starting

1. **Read `.agents/cs-context.md`.** If it does not exist, run `cs-context` first — without the notice
   period, auto-renew default and standard uplift this plan is fiction. Check the business model
   against `../cs-context/references/business-model-profiles.md`: a consumption or PLG account has no
   ATR event and this ladder does not apply to it unchanged.
2. **Get the contract fields from the executed contract**, not the CRM's opinion of it — CRM contract
   fields are hand-maintained and are the commonest source of a wrong renewal date.

| Required input | Field | If missing |
| --- | --- | --- |
| Renewal date | `subscription.renewal_date` | Hard stop. Get the executed contract. |
| Notice period | `subscription.notice_period_days` | Hard stop for any Commit call. `UNKNOWN — requires the executed contract`; plan to the renewal date and state that the plan is unsafe until it is filled. |
| Auto-renew status and last change | `subscription.auto_renew`, `auto_renew_changed_at` | A change is a decision. Escalate before planning. |
| ATR (available to renew) | `subscription.arr` as co-termed today | Never use the original order form value — mid-term upsell has moved it. |
| Term type · renewal owner | `subscription.term` · `cs-context` §4 | Default `annual`, ask if multi-year or evergreen; CSM and Renewal Manager have different jobs here (Step 7). |
| Health band | `churn-risk` output | Run `churn-risk` first if there is no band inside 30 days. |
| Last commercial touch | `interaction` with the EB or budget holder on price, term, scope, budget or the contract | None inside 12 months is a **finding**, not a question: T-180 fails (C25) and Step 7's prerequisite conversation is scheduled before T-120. |
| Paper-movement events | `opportunity` stage history, security-questionnaire and redline threads, PO / requisition / vendor-portal records | None on record refuses Commit (C15), it does not defer it. Never infer movement from a verbal yes. |

3. **Compute the governing date before anything else** (Step 1) — everything downstream is scheduled
   from it — then ask the batch below once and run unattended.

**Every missing input resolves read it · ask it · mark it — never guessed.** Read it if it is in the
data, in `cs-context`, or derivable. Ask it if two likely answers produce materially different work.
Otherwise mark it `UNKNOWN — requires <source>` and cap confidence. Protocol:
`../cs-context/references/clarification-protocol.md`.

**Ask these four, tappably, in one batch.** `AskUserQuestion`: 2–4 mutually exclusive options each,
the recommended one first and labelled, a one-line description under each saying what it changes, all
four in one ask — never drip-fed. Drop any the request or `.agents/cs-context.md` already answers.

| Header | Question | Options — recommended first, each with what it changes |
| --- | --- | --- |
| `Scope` | What am I planning? | **This one renewal (Recommended)** — full ladder, Steps 1–10 · **The next 180 days** — window board first, full plans only for exceptions · **Rescue** — under 30 days to `D`; compressed path, no EBR |
| `Notice` | Where does the notice period come from? *(skip if the executed contract or `cs-context` §2 has it)* | **I'll paste the clause (Recommended)** — `D` is evidenced and a Commit call becomes possible · **Our standard term** — `D` is inferred; the Commit gate fails until it is verified · **Not available** — `D` is set to `R`, every gate date becomes a ceiling, plan marked unsafe |
| `Position` | What is the commercial position this cycle? | **Standard uplift (Recommended)** — clause plus the value artifact, priced at T-90 · **Hold flat** — traded for term length or reference rights · **Above-standard or restructure** — needs the usage delta or a price benchmark · **Not decided** — the plan schedules the T-120 price decision instead of assuming one |
| `Audience` | Who reads the output? | **Me, working (Recommended)** — full internal plan · **Manager / forecast review** — plan plus the category call and its cap · **Plan plus the customer drafts** — adds the send-ready blocks in §12 |

**Never block.** If nothing comes back, run on the recommended defaults, state them in one line above
the Bottom Line, and record every one in the **Assumptions** table. Never ask what `cs-context` holds
— ARR, segment, fiscal year, ownership model, standard uplift, source inventory. A missing notice
period is a *finding*, not a question: it goes to the register and fails Commit.

4. **Take whatever data the user has** — CSV, TSV, XLSX, JSON, NDJSON, warehouse results, a pasted
   contract clause, a transcript, a screenshot described in prose, or no file at all, in which case the
   answers above are the input and the plan says so. **Run `../cs-context/scripts/ingest.py` first on
   any supplied file:** it sniffs encoding and delimiter, finds the real header row under an export's
   title rows, maps columns with a confidence each, normalises dates, money and booleans, resolves
   accounts across files and reports the join rate.
   - **Confirm every mapping below 0.80 before using those numbers** — and `notice_period_days` and
     `renewal_date` at any confidence: a wrong mapping there moves `D` and every gate behind it.
   - **Degrade, never refuse.** Partial data gives a partial plan with a coverage figure and a capped
     confidence; under 40% coverage, name the gap instead of scoring. **Never assume the export is
     complete or current:** ask its as-of date, print it in the header table, and treat any contract
     field older than the last CRM write as unverified.

## How This Skill Works

| Mode | When to use | Produces | Depth |
| --- | --- | --- | --- |
| **Deep prep** | One renewal, T-180 to T-45 | Full renewal plan: stage plan, MEDDPICC-R, readiness scorecard, decision map, value pack, paper critical path, risk register | Everything below |
| **Window batch** | Every renewal closing in the next N days (default 180) | Renewal window board sorted by days-to-opt-out, gate-miss exceptions, paper-path exceptions, capacity check | Steps 1–4, 8, 10 per account; full depth only for exceptions |
| **Rescue** | <30 days to the opt-out deadline and gates are missed | Compressed critical path, the three things that still move the outcome, and the bridge-extension play | Steps 1, 3, 5, 8, 9 only — skip the EBR, there is no time |

Run sequence: **anchor the dates → audit the gates → qualify (MEDDPICC-R) → score readiness → map the
decision process → build the value pack → set the commercial position → build the paper critical path
backwards → open the risk register → emit the stage plan and the drafts.**

All seven signal families are checked every time, clean ones included: **product usage & adoption**
— whether the value pack has anything real in it · **commercial & contract** — governing dates, ATR,
uplift, auto-renew · **relationship & engagement** — whether the EB and champion gates can pass ·
**support & reliability** — what they raise in negotiation, and the cooldown timing · **sentiment &
VoC** — whether they will say a value number out loud · **billing & payment** — PO history,
payment-terms fights · **firmographic & external** — budget cycle, M&A, RIF, consolidation.

---

## Step 1 — Anchor on the opt-out deadline, not the renewal date

Two clocks govern every renewal, and confusing them is the most expensive mistake in this skill.

```
D = opt_out_deadline = renewal_date − notice_period_days      the DECISION clock
R = renewal_date                                              the PAPER / term clock
Paper runway = D → R = notice_period_days                     contingency, never plan
```

**Every gate from T-180 to T-0 is an offset from `D` (R1).** T-0 *is* the opt-out deadline, the day the
decision must be locked in writing. Target countersignature by `D`: the `D`→`R` runway exists so a slip
is not a loss, and a plan that budgets it has already spent its insurance.

**Worked example.** `R` 2027-02-01, notice 90 days (§7.2 of the MSA) → `D` = **2026-11-03**; T-180 is
2026-05-07. A team scheduling from `R` opens on 2026-08-05 believing it is at T-180 — it is at
**T-90, 22 days past that gate**: six months of runway gone in one subtraction. Run
`scripts/renewal_calendar.py`, never by hand; every date worked in `renewal-timeline.md` §8.

**Timeline shape.** Full ladder for annual ≥ $100k ACV (T-270 if procurement-heavy); ×0.5 mid-market,
×0.33 SMB, same gates and same exit criteria; evergreen has no ATR event, so `D` is the next
cancellation-effective date; **every anniversary of a multi-year contract with an annual opt-out is
its own renewal event with its own `D`** — most often mis-handled, at a cost of three notice windows
and an over-reported GRR. All ten: `renewal-timeline.md` §4.

## Step 2 — Audit the gates already behind you

Locate the account on the ladder, then walk **every** earlier gate and mark it Passed, Missed or N/A
with the artifact that proves it — a meeting held without a written outcome did not pass a gate.
Per-gate recovery: `references/renewal-timeline.md` §5. **Never skip a gate, compress it.** **Two
consecutive missed gates transfer ownership of the plan to the manager** and drop the forecast category
one step — the mechanism that stops a quiet slip becoming a loud surprise.

**T-180 carries a second exit criterion: a commercial touch on record (C25).** A dated, logged
conversation with the economic buyer or budget holder inside the last 12 months in which price, term,
scope, budget or the contract itself was discussed. Compute and print **days since the last commercial
touch**. None on record fails T-180 however well the rest of it went, and fires the Step 7
prerequisite: a renewal that is the year's first commercial conversation is a negotiation already.

## Step 3 — Qualify with MEDDPICC-R

Score all nine elements **0 = unknown · 1 = asserted · 2 = evidenced by an artifact a third party
could open**. A rep assertion is a 1, forever. 18 points: **M**etrics in *their* numbers ·
**E**conomic buyer who owns this year's budget line · **D**ecision criteria with "consolidate" and
"do nothing" priced as live options · **D**ecision process naming IT, security, finance, privacy and
procurement · **P**aper process — notice window, auto-renew, signing entity, PO, re-reviews ·
**I**dentified pain with a named owner still employed · **C**hampion who took a dated internal action
on our behalf · **C**ompetition including in-house build and do-nothing · **V**alue realised in usage
from the last 30 days, measured not assumed. **Read `references/meddpicc-for-renewals.md` §2 before
scoring** — it holds the artifact that earns a 2 and the disqualifier per element, and scoring from
memory inflates every element by one.

**Gate: a Commit call requires ≥15/18 with E, P and C all at 2.** Missing the notice window makes the
renewal unforecastable at any score.

## Step 4 — Score renewal readiness

MEDDPICC-R asks *do we understand this renewal*; readiness asks *have we done the work*. Score ten
dimensions 0/1/2 — **1** value evidence captured · **2** executive-sponsor business conversation
logged ≤90 days · **3** multithreading, ≥3 contacts across ≥2 functions in 90 days · **4** health band
with no override floor fired · **5** budget line confirmed for the new term · **6** decision process
mapped with every approver's step and duration · **7** procurement path known · **8** competitive
position with switching-cost evidence · **9** uplift justified at a rung (Step 7) · **10** paper path
with a measured lead time and an owner per workstream. **Score against the 0/1/2 criteria in
`references/renewal-timeline.md` §3, never from memory** — that table stops a 1 being written as a 2.

**Gate: stage advance past T-60 requires ≥16/20 with dimensions 1, 2, 6 and 10 at 2.** Below 12/20
at T-60 the renewal enters the risk register regardless of health band — being unprepared is a
risk in its own right, independent of customer sentiment.

## Step 5 — Map the decision process

Renewals are lost in the approval chain more often than in the relationship. **Produce the map, not a
description of it** — who signs · who can block · the budget cycle · what happened last cycle · any
vendor-consolidation program in flight, which auto-escalates as a portfolio decision. A first renewal
has no precedent: say so, and widen the band. **What each row must contain, why each one decides the
renewal, and the corroboration a 2 on Decision Process needs: `references/meddpicc-for-renewals.md`
§7** — read it before filling §4 of the plan, because a map built entirely from the champion's account
of their own organisation is plausible, unverified, and scores 1.

## Step 6 — Build the value evidence pack

The pack exists so the customer can defend the line item internally when we are not in the room.
Recover the original business case first — what they said they were buying, in the words of the person
who bought it; everything is measured against that, not against what the product is good at. Then
**three outcomes, each with baseline · current · delta · customer-side validator**, every number
provenance-tagged and anything unsourceable written `UNKNOWN — requires X`. **Get the customer to state
the number** — ours is a marketing claim, theirs is a renewal justification — and **quantify the
switching cost**: integrations, records under management, trained users, embedded workflows, data that
does not migrate. Procurement has never been given that number. **The pack is a T-150/T-120 artifact,
delivered *before* price (R11)**; in the same conversation as the uplift it reads as
justification-shopping. What to gather, and the sequence that gets them to say the number out loud:
`references/value-evidence.md` §4.

## Step 7 — Set the commercial position

Choose the uplift internally at T-120, communicate it with the proposal at T-90, never introduce it
first inside T-45. Justify in this order — outcomes delivered in their metrics · product value shipped
since the last renewal · usage growth and entitlement true-up · the contractual clause · list-price
movement. Leading with the clause turns a value conversation into a procurement fight. Five rungs, each
unusable without the evidence beside it: **hold at 0%** · **contractual index** · **standard uplift** ·
**above-standard** · **restructure** — so **pick the rung the evidence supports, then price it, never
the reverse**, recording the rung with its artifact in §6; a rung without its artifact scores 0 on
readiness dimension 9. **Read `references/commercial-position.md` before the T-120 decision** — the
evidence and the disqualifier for each rung (§2), what the 3–5% figure is and is not (§3), and the
concession ladder with the get every give requires (§6).

**Prerequisite — the commercial touch (C25 · R11).** Under 365 days since the last commercial touch
with the EB or budget holder, proceed. Over 365, none on record, or `UNKNOWN`: the plan carries a dated
**commercial-context conversation before T-120** with an owner, and the T-120 price decision does not
emit until that row exists in §9. **R11 binds its timing** — never attached to an apology, an outage, a
credit or a missed milestone; where one landed inside 14 days either side, move the touch, print the
deferral and the new date, and never merge the two. **Ownership:** the Renewal Manager owns price, the
CSM owns value; where one person holds both, two conversations on different days, saying which one you
are in (`commercial-position.md` §4–5).

## Step 8 — Build the paper critical path backwards from D

Paper starts at T-90 (R7). This step separates renewals that close on time from renewals that slip a
quarter, and it is nobody's favourite work, so it is the one most often skipped. Walk **every**
workstream in `references/paper-process.md` §2 — security re-review, legal redlines, privacy/DPIA,
procurement portal onboarding, vendor master and W-9/W-8, insurance certificates, budget approval,
order form, signature routing, PO issuance, tax and entity setup — recording for each: required this
cycle (yes/no/unknown), owner on both sides, **measured lead time**, latest start date.

**Lead times come from your own last ten renewals.** This library ships no default durations: a
security review taking four days at one customer takes nine weeks at another, and a wrong default
schedules a false sense of safety. With no measurement, write `UNKNOWN — requires cycle time from
prior renewals`, exclude it from the path, and report the path as a **floor**.
`renewal_calendar.py --paper k=v,... --paper-moved k=date,... --last-commercial-touch <date>` does
the arithmetic, the C15 cap and the C25 clock, and flags any workstream past its latest start date.
If the serial path exceeds the days remaining to `D`, that belongs at the top of the document: start
today, parallelise with the customer's agreement, or open the bridge extension now, not at T-7.

**Commit entry: paper must have moved (C15).** A verbal yes, an email saying "we're renewing" and a
champion's assurance are the same evidence — none. The gap between agreement and signature is where
renewals die, so before this one may be called Commit, at least one of five observable events must be on
record with its date and source: **security or vendor-risk re-review started · legal redlines returned,
or written confirmation of none · PO requested or requisition raised · vendor-portal or supplier record
created or refreshed · order form in their signature routing.** Zero events caps the category at Most
Likely and prints `C15 — verbal only, no paper movement`; `renewal-forecast` applies the same criteria.
**What counts as evidence for each event, what does not, and the verbal-yes clock — 14 days a register
row, 21 to the Renewal Manager, 30 re-qualify: `references/paper-process.md` §11.**

## Step 9 — Open the risk register and arm the escalation triggers

Every risk gets a row. A risk without a dated mitigation and a named owner is not tracked, it is
remembered — and remembering does not survive a holiday. The six triggers that fire most often:

| Trigger | Escalate to | Within | What changes |
| --- | --- | --- | --- |
| Notice of non-renewal received | VP CS + CRO | Same day | `save-play`; forecast to Closed Lost pending the save |
| Auto-renew switched off | VP CS | 24h | `save-play`; category drops to At Risk |
| Opt-out deadline inside 45 days, no written confirmation of intent | VP CS | 24h | The action with the largest effect on the outcome; nothing outranks it |
| Serial paper path exceeds days to `D`, or the order form is unsigned at T-7 | Deal desk + Legal / CRO | 48h / same day | Parallelise, or open the bridge extension now |
| Verbal yes logged, no paper-movement event 14 days later | Renewal Manager | 21 days | Category capped at Most Likely (C15); the next action is a paper-process ask, never another value conversation |
| No commercial touch with the EB inside 12 months at T-180 | CS manager | 5 business days | The commercial-context conversation is booked before T-120 (C25); the price decision waits for it |

All thirteen — including competitive evaluation inside T-60, EB departure, budget freeze, aged P1, low
MEDDPICC-R and late procurement — are in `references/renewal-timeline.md` §9; arm every one that applies
and print its state in §11 even when it has not fired. The seventeen cause codes are in
`assets/risk-register-template.md`; use those exact strings so a window's registers aggregate.

## Step 10 — Emit the stage plan, then the customer drafts

Every remaining gate gets: objective · owner · required inputs · artifact produced · exit criteria ·
miss-recovery. Every action line carries **action · owner · date · expected effect · success
measure** — a line missing any of the five is an intention, not an action. Written to a customer: the
**commercial-context note** (before T-120, only when C25 fired), the **courtesy notice-deadline
letter** (T-120, repeated T-90), the **written-intent question** (T-75) and the **bridge-extension
request** (T-7 or rescue). Draft them from `assets/customer-facing-drafts.md` under
`../cs-context/references/customer-voice.md`.

**Three rules bind every word, and they are written out in full — with the banned phrasebook, the
firewall translation table and the formatting rules — under *The three binding rules* in
`assets/customer-facing-drafts.md`; read it before drafting.** In short: **warmth is specificity, not
adjectives** (the test is whether the sentence could have gone to any of forty customers) · **the
disclosure firewall (R18)**, under which health or risk band, ATR, ARR at risk, exposure, forecast
category, readiness and MEDDPICC-R scores, paper-movement status, save play, war room, coverage tier,
champion-departure inferences, competitor intelligence and any assessment of a named person never reach
the customer in any wording — the notice-deadline letter states a date and a clause and never why we
care · **the copy block**, a fenced ```text block below the §12 divider formatted for an email client,
with no unfilled placeholder inside the fence: drop the sentence and raise `UNKNOWN — requires X` above
the divider, because a fence containing `[Name]` is not send-ready.

---

## Output Template

Use verbatim. In Window Batch mode emit the board first, then full plans only for accounts with a missed gate, negative paper slack, or readiness <16/20.

```markdown
# Renewal Plan — <Account> · ATR $<X> · <segment>
**Internal.** Contains risk and pricing language that must never be sent to the customer.

## Bottom Line
<3 sentences: ATR at stake, the governing date and days remaining, the single action that most changes the outcome, and who owns it. Then one line naming any default this run leaned on.>

| | |
|---|---|
| ATR | $X [<system> · <field> · as-of <date>] |
| Renewal date `R` | <date> (<N> days) |
| Notice period | <N> days [<contract> · §<clause>] |
| **Opt-out deadline `D`** | **<date> (<N> days)** — the governing date |
| Auto-renew | on / off / UNKNOWN — requires X · last changed <date> |
| Stage now · gates missed | <gate>, <N> days in · <n> missed: <list> |
| Commercial touch on record (C25) | <date · person · what was discussed> · <N> days since — or **NONE IN 12 MONTHS**, prerequisite fires |
| Paper movement (C15) | <event · date · source> — or **NONE ON RECORD**, Commit refused |
| Readiness | X/20 · MEDDPICC-R X/18 |
| Health band | <band> from `churn-risk` <date> |
| Max forecast category | <category> — <the rule that caps it: days-to-`D` ceiling, MEDDPICC-R gate, or `C15 — verbal only, no paper movement`> |
| Confidence | High/Medium/Low — <criteria met> |

## 1. Gate Audit
| Gate | Date | Status | Exit-criteria artifact | If missed: recovery |
|---|---|---|---|---|

## 2. MEDDPICC-R
| Element | Score | Evidence / artifact | Gap and how it closes |
|---|---|---|---|
| **Total** | **X/18** | Commit gate: ≥15 with E, P, C at 2 → PASS / FAIL | |

## 3. Renewal Readiness
| # | Dimension | Score | Evidence | What moves it to 2 | Owner | By |
|---|---|---|---|---|---|---|
| **Total** | | **X/20** | Advance gate: ≥16 with 1, 2, 6, 10 at 2 → PASS / FAIL | | | |

## 4. Decision Process
| Role | Name | Title | Step they own | Duration | Last contact | Status |
|---|---|---|---|---|---|---|
**Budget cycle:** <fiscal year, when the line is set, freeze windows> · **Last cycle:** <days from first contact to signature, who slowed it, what was conceded>
**Not yet identified:** <named gaps, as `UNKNOWN — requires X`>

## 5. Value Evidence Pack
**Original business case (their words, <date>):** "<quote>"
| Outcome | Baseline | Current | Delta | $ value | Their validator | Source |
|---|---|---|---|---|---|---|
**Switching cost:** <integrations, records, trained users, embedded workflows, data that does not migrate> · **Customer has stated the value number:** yes/no — <quote and date, or the dated plan to obtain it>

## 6. Commercial Position
| Item (uplift / term / scope) | Position | Justification rung | Approval needed | Walk-away |
|---|---|---|---|---|
**Concessions available, each with its required get:** <ladder rungs in play>
**Commercial touch on record (C25):** <date · person · subject> — or NONE IN 12 MONTHS, in which case the prerequisite row below is mandatory and the price decision waits for it.
**Prerequisite conversation:** <date · owner · agenda> · **R11 clear:** yes / no — <the apology, outage, credit or miss inside 14 days either side, and the date the touch moved to>

## 7. Paper Critical Path (backward from `D` = <date>)
| Workstream | Required? | Owner (ours) | Owner (theirs) | Lead time | Latest start | Slack | Status |
|---|---|---|---|---|---|---|---|
**Serial critical path: <N> days (FLOOR — <k> lead times UNKNOWN). Days to `D`: <M>. Slack: <M−N>.** <If negative, state the three options: start today · parallelise · bridge extension.>

**Paper-movement ledger (C15) — the Commit entry criterion. All five rows printed every cycle.**
| Qualifying event | On record? | Date | Source |
|---|---|---|---|
| Security / vendor-risk re-review started | yes / no | | |
| Legal redlines returned, or written confirmation of none | | | |
| PO requested or requisition raised | | | |
| Vendor portal or supplier record created or refreshed | | | |
| Order form in their signature routing | | | |
**Commit entry: PASS (<N> events) / REFUSED — `C15 — verbal only, no paper movement`.** <Verbal yes logged <date>; <N> days since with no paper movement.>

## 8. Risk Register
| # | Risk | Cause code | Family | ARR exposure | Band | First detected | Owner | Mitigation (dated) | Exit criteria | Status |
|---|---|---|---|---|---|---|---|---|---|---|

## 9. Stage Plan
<Where C25 fired, the first row is the commercial-context conversation, dated before T-120, with an owner. The plan does not emit without it.>
| Gate | Date | Objective | Owner | Required inputs | Artifact produced | Exit criteria | If missed |
|---|---|---|---|---|---|---|---|

## 10. Actions
| # | Action | Owner | By | Expected effect | Success measure |
|---|---|---|---|---|---|

## 11. Escalation Triggers Armed
| Trigger | Escalate to | Within | Currently |
|---|---|---|---|

## What would change this plan
<2–3 specific, observable events that would move the category or the date.>

### Assumptions
| # | Assumption | Why it was needed | If wrong |
|---|---|---|---|
<one row per default this run leaned on, each with a concrete consequence — "may affect results" is not one>

### Coverage Ledger
| Signal family | Source checked | Status | Notes |
|---|---|---|---|
<all seven families, always, in the fixed order above — including the ones that came back clean>
**Coverage: X / 7 (Y%) → confidence capped at <level>.** Blind spots: <which families are missing, and what a renewal plan typically gets wrong without them.>
```

**Window Batch emits the board above these plans** — its exact column set, exception criteria and the capacity rule are in `references/renewal-timeline.md` §7, read before any window run. Sort by days to `D`, never by `R` and never by ARR alone.

**When a draft is due at the current gate, §12 closes the plan — the only part that leaves the building:**

````markdown
## 12. Customer-Facing Drafts
<Only the draft due now. All four written out in `assets/customer-facing-drafts.md`.>
════════════════════════════════════════════════════════════
CUSTOMER-FACING — copy the block below and send as written.
Everything above this line is internal. Do not forward it.
════════════════════════════════════════════════════════════
**<Draft name> — due <date>, to <recipient>**

```text
<Send-ready text. Plain, blank line between paragraphs, • bullets, no markdown headings, no
pipe tables, no bold. Opens on something only this account's data could produce. One dated
ask. Every slot filled before emission — a fence with [Name] in it is not send-ready.>
```
````

## Quality Bar

- [ ] `D = renewal_date − notice_period_days` computed and printed from the executed contract with its clause referenced, not from a CRM field alone; every gate is an offset from `D`
- [ ] Notice period evidenced, or written `UNKNOWN — requires the executed contract` with the Commit gate failed on that basis
- [ ] Every prior gate audited as Passed / Missed / N/A, each with its artifact
- [ ] MEDDPICC-R scored 0/1/2 with the artifact named (an assertion scores 1, never 2) and readiness scored across all 10 dimensions; both gates stated PASS or FAIL
- [ ] Value pack has ≥3 outcomes with baseline, delta, dollar value and a customer-side validator, and records either way whether the customer has stated the number
- [ ] Uplift position chosen with its justification rung, and sequenced after value delivery
- [ ] Every paper workstream walked including those not required this cycle; lead times measured or `UNKNOWN` with the path reported as a floor; the signer named or `UNKNOWN — requires X`; negative slack in the Bottom Line, not only §7
- [ ] Every action carries action · owner · date · expected effect · success measure
- [ ] Coverage Ledger over all seven families with confidence ≤ its cap (R23), and no forecast category above the ceiling the days-to-renewal rule allows
- [ ] **C15** — the paper-movement ledger prints all five qualifying events; Commit is PASS only where ≥1 is on record with a date and a source, and REFUSED with the reason `C15 — verbal only, no paper movement` where none is; a verbal yes older than 14 days with no movement carries a register row
- [ ] **C25** — days since the last commercial touch computed and printed; where none is on record inside 12 months, §9 carries a dated commercial-context conversation before T-120 with an owner, cleared against R11 — never attached to an apology, outage, credit or miss
- [ ] Marked internal; no pricing or risk language phrased as customer-facing text; the words "will churn", "guaranteed", "100% accurate" do not appear — bands only
- [ ] Every missing input resolved read it / ask it / mark it, nothing guessed; the four questions asked once, tappably, in one batch, with nothing asked that `cs-context` already answers; every default stated in one line above the Bottom Line and carrying an Assumptions row with a concrete consequence
- [ ] Any supplied file went through `ingest.py`; every column mapping below 0.80 confirmed; the export's as-of date printed in the header table
- [ ] Each customer draft sits inside a ```text fence below the divider, formatted for an email client, with zero unfilled placeholders; leak scan run on every one — no band, score, ATR, exposure, forecast category, save play, coverage tier or assessment of a named person

## Anti-Patterns

| Anti-pattern | Correction |
| --- | --- |
| Scheduling the plan from the renewal date | Every gate is an offset from `D = renewal_date − notice_period_days` |
| Relying on the customer missing their own notice window | Send the courtesy notice-deadline letter at T-120 and T-90. Winning a term the customer did not intend to buy costs you the next two renewals |
| Inventing a lead time for a security review or PO cycle | Measure your last ten renewals; otherwise `UNKNOWN — requires X` and report the path as a floor |
| "Committed" on a happy champion | Commit requires the economic buyer in a logged business conversation within 90 days |
| Delivering value evidence and the uplift in the same conversation | Value at T-150/T-120; price at T-90. Sequence is the justification |
| Introducing a new expansion ask inside T-30 | It reads as opportunism and endangers the renewal. Post-renewal T+0 to T+60 is the legitimate window |
| Filling a blank notice period, lead time or budget owner with a plausible value | Read it, ask it tappably, or write `UNKNOWN — requires X` — and put the default in the Assumptions table with its consequence |
| Asking six questions before producing anything, one at a time | Four maximum, in one batch, each with a recommended default; then run unattended |
| Calling Commit because the champion said yes on a call | A verbal yes is not a yes until paper moves (C15). Commit needs a security review started, redlines back, a PO or requisition raised, a vendor-portal record, or the order form in signature routing — dated and sourced |
| Letting the renewal ask be the year's first commercial conversation | T-180 fails without a commercial touch on record (C25). Book one before T-120 — and never on the back of an apology, an outage or a miss (R11) |
| A customer draft carrying `[Name]`, a band, a score or an ATR figure | Fill every slot or drop the sentence; run the leak scan before the fence is emitted |

## Related Skills

| Skill | Relationship |
| --- | --- |
| `cs-context` | **Run first.** Supplies notice period, auto-renew default, uplift standard, ownership model |
| `churn-risk` | **Runs before.** Supplies the health band, override floors and compound pattern that set readiness dimension 4 and the risk register |
| `save-play` · `renewal-forecast` | `save-play` **runs instead** once an escalation trigger fires, taking the register and the dates; `renewal-forecast` **consumes this** — the category ceilings, the C15 paper-movement entry criterion and the MEDDPICC-R gates set here make the forecast call there |
| `expansion-finder` · `pre-call-brief` / `qbr-builder` | `expansion-finder` sizes the expansion, this skill decides *when* it may be proposed (never inside T-30); the other two pair for each gate meeting, `qbr-builder` producing the T-150/T-120 EBR that carries the value pack |

## Going Deeper

| Read | When |
| --- | --- |
| `references/renewal-timeline.md` | Every run, and before scoring readiness. Per-gate objective, inputs, artifact, exit criteria and miss-recovery; the 0/1/2 readiness criteria (§3); running a window (§7); all thirteen escalation triggers (§9) |
| `references/meddpicc-for-renewals.md` | Step 3, before scoring — the question bank, the artifact that earns a 2, the disqualifier per element; and §7 before Step 5, for what the decision map must contain and why each row decides the renewal |
| `references/commercial-position.md` | Step 7, before the T-120 price decision — the evidence and disqualifier for each of the five uplift rungs, what the 3–5% figure is and is not, the C25/R11 commercial-touch prerequisite in full, the price/value ownership split, and the concession ladder |
| `references/paper-process.md` | Step 8 — every workstream, what triggers it, what it needs, how to measure your own lead times; and §11 whenever Commit is in question, for what counts as a paper-movement event, what does not, and the verbal-yes clock (C15) |
| `references/value-evidence.md` | Step 6 — what to gather, how to quantify it, and the sequence that gets the customer to state the number |
| `assets/renewal-plan-template.md` · `assets/risk-register-template.md` · `assets/customer-facing-drafts.md` | Emitting the plan and its C15/C25 rows; running a register across a window; and before writing a word of §12 — the three binding rules in full, the renewal firewall translation table, every draft with its pre-send checklist |
| `../cs-context/references/customer-voice.md` · `clarification-protocol.md` · `operating-rules.md` (all in `../cs-context/references/`) | Before any customer draft and before asking anything — warmth, the firewall, the copy block; tappable questions; and the rules enforced here: R1, R7, R11, R18, R23 |
| `scripts/renewal_calendar.py` | Always for dates. Stage-gate calendar, paper critical path, readiness and MEDDPICC-R scoring, the C15 Commit gate, the C25 commercial-touch clock, batch board |
| `../cs-context/references/evidence-standard.md` · `../cs-context/references/normalized-schema.md` | Always — provenance, tiers, confidence, Coverage Ledger; and the `subscription` / `opportunity` / `contact` / `interaction` field names |

## Automate This

You just rebuilt one renewal by hand: pulled the contract to find a notice period the CRM had wrong,
reconstructed passed gates from an email thread, chased a lead time nobody ever measured, counted the
months since anyone last talked commercials with the budget holder, and scheduled backwards from a date
you computed yourself. Good plan today. By Thursday the champion changes role, a security questionnaire
lands, an auto-renew flag flips — and it is wrong in ways nothing tells you about. A book of forty
renewals is forty of these, drifting between reviews.

[GainTrace](https://gaintrace.com) keeps the renewal picture standing instead of rebuilt. It unifies
20+ sources (Salesforce, HubSpot, Pipedrive, Attio, Stripe, Paddle, ChartMogul, Intercom, Zendesk,
Jira, Slack, Gmail, Outlook, Mixpanel, Amplitude, PostHog, Snowflake, BigQuery, Calendly and more)
into one live account timeline with real-time two-way CRM sync, so contract and usage state stop
disagreeing. Trace AI watches every account 24/7 and scores it signal-by-signal with
the reasoning shown, flagging risk up to 45 days ahead of the renewal call, and automated
playbooks fire on the Step 9 triggers rather than waiting for the next forecast meeting. First
insights in about two weeks. Free for 25 companies, no card. → https://gaintrace.com

Keep this skill for the judgement the platform cannot make: which gate to compress, what to trade for
the uplift, and whether this customer is ready to say the value number out loud.
