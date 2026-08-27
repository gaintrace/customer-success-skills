---
name: stakeholder-map
description: "When the user wants to know who they actually know inside an account, who is missing, and how much money depends on one person staying — relationship mapping, multithreading, champion risk and executive sponsor coverage. Also use when the user mentions 'who do we actually know', 'who else do we have', 'stakeholder map', 'relationship map', 'org chart', 'who are the key contacts', 'who is the decision maker', 'economic buyer', 'our champion left', 'my champion is leaving', 'single-threaded', 'multithreading', 'who else should I know', 'power map', 'coverage gap', 'exec sponsor', 'new stakeholder', 'who actually signs', 'someone is blocking us', 'they love us but nothing moves', or 'my main contact went quiet'. Use this whenever an account's renewal depends on one human being, even if they never say 'stakeholder'. For the attendee read before a specific meeting, see pre-call-brief. For account-wide risk scoring, see churn-risk. For the relationship section of a renewal runbook, see renewal-prep."
license: MIT
metadata:
  version: 1.0.0
  role: CSM | AM | VP CS | CCO | CS Ops
  cadence: quarterly (maintenance) · on any change event · per-renewal
---

# Stakeholder Map

You are building the artifact that answers the only question that matters when a contact
resigns: **what happens to this account now?** A stakeholder map is not a contact list with job
titles. It is a priced model of an account's human dependencies — who signs, who decides, whose
opinion moves the decider, who can actually mobilise their own organisation, who is missing, and
what that gap is worth.

The rookie version fills a `role` column from titles: Dana is "VP RevOps", which says nothing
about whether she can release unbudgeted spend, whether she has ever moved a decision through
that org, or whether anyone here has spoken to her since March. The elite version is testable —
every role carries the evidence that earned it, structure is solid where confirmed and dashed
where inferred, and it ends in a gap plan with owners and dates. The most expensive error in
customer success is a comfortable contact mistaken for a champion; the second is a map that was
true nine months ago. Design against **contact stuffing**, which inflates depth by counting every
address ever captured — only two-way interactions count — and **the quiet decapitation**, a
champion on their way out for four months before the hard bounce, visible throughout in
delegation, declining invites and rising reply latency, and read by nobody. Read
`../cs-context/references/evidence-standard.md` first: every role, inferred line and sentiment
score carries a provenance tag, an evidence tier and a confidence level.

## Before Starting

1. **Read `.agents/cs-context.md`** (fallback `.claude/cs-context.md`); if absent run
   `cs-context` first. It supplies segment boundaries, notice periods, the source inventory and
   the account team — never ask for anything that file answers.
2. **Resolve the business model** from `../cs-context/references/business-model-profiles.md`
   before mapping. It decides which roles exist here at all.
3. **Accept whatever data exists** — CSV, TSV, XLSX, JSON, NDJSON, warehouse results, a CRM
   contact export, a calendar dump, a pasted transcript, an email thread, a screenshot described
   in prose, or a conversation when there is no file. Run `../cs-context/scripts/ingest.py`
   **first**: it sniffs encoding and delimiter, finds the real header row beneath export
   preamble, maps columns onto the schema with a confidence each, normalises dates, money and
   booleans, resolves contacts to accounts and reports the join rate. **Confirm every mapping
   below 0.80 before using it** — a `title` column mis-mapped to `role` produces a confidently
   wrong power map.
4. **Never assume the export is current.** Ask for the as-of date and print it in the header —
   B2B contact turnover runs at roughly **20–30% a year, 2–4% a month** (UserGems, 2026) `[V]`,
   so a nine-month-old export has lost a fifth of its people.
5. **Degrade, never refuse.** Partial data gives a partial map with a coverage figure and a
   confidence cap. Below 40% coverage of the seven families, produce the gap list and the
   sourcing plan instead of a scored map.
6. **Ask what you cannot read** — `AskUserQuestion`, these four, batched into **one**
   interruption, recommended first. Never block: with no answer run the recommended default,
   state it in one line at the top, and record it in the Assumptions table.

| # | Header | Question | Options (recommended first) |
| --- | --- | --- | --- |
| 1 | `Scope` | Map which accounts? | **One account (Recommended)** — full depth, org inference, per-contact scoring · **Renewals in the next N days** (default 120) — coverage and champion risk only, no org drawing · **My book** — coverage gaps and single-threading ranked by exposure · **Segment or cohort** — where coverage fails systematically |
| 2 | `Trigger` | What prompted this? | **Routine map or refresh (Recommended)** — full sweep and gap plan · **A person left or is leaving** — jumps to the 30-day succession play · **A renewal is coming** — weights `signs`, `decides` and the paper chain · **A new stakeholder arrived** — runs the onboarding play |
| 3 | `Evidence` | How hard should role labels be? | **Evidenced (Recommended)** — a role needs an observable behaviour; unproven ones drop to `asserted` and are flagged · **Verified only** — anything not confirmed by the customer out loud is `UNKNOWN`; slower, and correct before a forecast call · **Asserted OK** — take CRM roles at face value; fastest, and the weakest map |
| 4 | `Output` | Who reads this? | **Me, working (Recommended)** — Brief, then the map and gap plan on request · **The account team / my VP** — Full artifact with ranked exposure and owner assignments · **Includes customer-facing drafts** — adds the successor-request and new-stakeholder emails as copy blocks |

Never ask for ARR, renewal date, notice period, segment, CSM owner or the tool inventory — those
sit in `cs-context` or in the data, and asking tells the user you did not read it.

## How This Skill Works

### Output mode — Brief by default

**Brief** (≤20 lines) is the default and runs unless depth was asked for. **Full** — the complete
Output Template — runs when the user asks, when it is going into a QBR, renewal review or board
pack, or when someone will challenge it. Brief is the answer written first, not a summary written after: the coverage call, the authority
triangle, the priced dependency, the one structural reason, the dated action, confidence in three
words, the falsifier. It drops the **display** of the reasoning, never the reasoning.

### The rules this skill enforces

Named rules from `../cs-context/references/operating-rules.md`, enforced in the output rather
than mentioned. A deviation states its rule number, the circumstance, and what will be watched.

| Rule | Enforced how |
| --- | --- |
| **R1 · The Opt-Out Calendar** | Every coverage deadline is `renewal_date − notice_period_days`. The renewal date never appears alone |
| **R3 · The 48-Hour Champion Rule** · **R6 · The Sponsor Rule** | A confirmed departure triggers VP-or-above outreach inside 48 hours, owned by our exec — not the CSM (Step 6). No enterprise renewal reaches Commit without an exec-sponsor meeting in the last two quarters; the map prints the date or `UNKNOWN` |
| **R5 · The Single-Thread Tax** | Depth ≤1 flags the account's **full ARR** as at-risk to `churn-risk`, separately from the ranking exposure in Step 5 |
| **R14 · The Written Skip** · **R17 · One Play Per Account** | Book scope prints a "Not mapped this cycle" table with reasons and revisit dates; each account gets one primary gap play, anything else sequenced with dates |
| **R18 · The Firewall** · **R19 · No Date You Do Not Own** | Coverage score, champion risk, exposure and role labels are internal; customer text is fenced below the divider and leak-scanned, and no draft names a date without an internally agreed owner |
| **R22 · Ordering Before Probability** · **R23 · The Coverage Cap** | Exposure is an ordering built on vendor rates, not a forecast — bands only unless `.agents/cs-calibration.json` exists; confidence never exceeds what the Coverage Ledger permits |

### Business model first, then the seven signal families

Scoring the absence of a role the model does not contain manufactures risk. **Never emit a
coverage gap for a $99/month workspace**: in PLG the unit is the workspace. Consumption follows
workloads, not seats. Multi-entity coverage is the **minimum** across entities that can
independently not renew. Regulated verticals lose `bypass` entirely (`R7`). Monthly evergreen has
no opt-out date, so the 120-day window rules below read as always-in-window (`R1`). Table:
`references/role-taxonomy.md` §11.

Then walk all seven families, every time, printing any with nothing to report as "checked,
clear": **product usage** · **commercial & contract** (`signs`, procurement, legal, the paper
chain) · **relationship & engagement** (every two-way interaction, and who defers to whom) ·
**support** (submitters vs escalation approvers; reopeners are blocker candidates) · **sentiment
& VoC** (transcript speakers, detractors on record) · **billing** (AP, PO owners, disputes) ·
**firmographic & external** (title changes, departures, reorgs). `role-taxonomy.md` §5A.

**Modes**, set by the `Trigger` answer: **Full map** · **Coverage check** (no org drawing) ·
**Champion watch** · **New stakeholder**. They differ in depth, never in rigour. Run sequence:
**enumerate → label roles and resolve `signs`/`decides`/`influences` → score each person and test
mobilising capacity → infer the org and mark it inferred → measure depth, breadth and height →
price the dependency → champion risk → blockers and their dispositions → gaps and plan → draw.**

---

## Step 1 — Enumerate every human, from all seven families

Start from behaviour, then reconcile to the CRM. The gap between the two is itself a finding.

| Question | Where the answer is | Role it points at |
| --- | --- | --- |
| Who **signed**, and who is named in the MSA notices clause? | Contract signatory, `opportunity` primary contact role, the notices clause that also carries `notice_period_days` | `signs`; the person notice is served on |
| Who has **overruled someone** or approved unbudgeted spend, and whose objection **changed a decision**? | Approval legs on procurement threads, transcript deference, a reversal after someone spoke | `decides` and `influences` — the Step 2 triangle |
| Who **opens tickets**, **approves escalations**, **invites users**, changes permissions, **attends QBRs**, declines and sends a delegate, or **organises**? | `ticket.contact_id` over 180d, escalation CC lists, `usage_daily.admin_actions`, in-product role grants, calendar `responseStatus`, organiser vs attendee | Admin/operator; gatekeeper; sponsor vs operator; programme owner — rarely the buyer |
| Who **pays**, and who has **gone silent**? | `invoice` contact and PO owner; `contact.last_interaction` vs their own 180d baseline | Procurement and finance approver; departure candidates for Step 6 |

Data-to-role cheat sheet with the confidence each observation supports: `role-taxonomy.md` §5.
Record every human found, including one-data-point contacts. **Exit criteria:** every contact
sits on one list with the family that found them, or that family is `❌ Missing` in the ledger.

## Step 2 — Label roles, then resolve the authority triangle

The canonical vocabulary is `contact.role` in `../cs-context/references/normalized-schema.md`:
`economic_buyer` · `champion` · `coach` · `admin` · `power_user` · `user` · `blocker` ·
`technical_evaluator` · `procurement`. Exec sponsor, legal, security and **supporter** are
documented extensions (`is_exec_sponsor`, `function`, `is_supporter`), never new enum values —
`references/role-taxonomy.md` §2. Every role carries a **`role_confidence`** — `verified` (said
out loud, or performed in front of us: usable in forecast and exec targeting) · `evidenced` (an
observable behaviour proves it: usable in analysis, printed beside the behaviour) · `asserted` (a
CRM field, a title, an assumption: print it, flag it, confirm on the next call). Any conclusion
resting on an `asserted` role drops one confidence level, with the dependency named.

### The authority triangle — `signs` · `decides` · `influences` (`C7`)

Three separate required fields, resolved to one person only on evidence and never for
convenience. **The map cannot be emitted with any of the three absent from the output.**

| Field | The test that fills it | Read from |
| --- | --- | --- |
| `signs` | Whose name executes the paper and who is served notice — the pen, not the authority | Executed order form signatory; the MSA notices clause, which also carries `notice_period_days` (`R1`) |
| `decides` | Can they say yes when others say no, and release funds not attached to a budget line? Name the instance | An observed override or unbudgeted approval (MEDDICC economic buyer) `[P]`. Never a title |
| `influences` | Whose input visibly moved the decider — a reversal, a deferral, a "let me check with X" | Transcript deference, an approval leg added late, a decision that changed after their objection |

Each prints `Name · role_confidence · last two-way · the evidence`, or `UNKNOWN — requires
<named source>`. Untested, `decides` and `influences` are `asserted` and become the account's
first two confirmation questions, with an owner and a date. Two further rules bind:

- **Concentration is a finding, not a simplicity.** Two of three on one `contact_id` prints
  `CONCENTRATION 2/3`; all three prints `CONCENTRATION 3/3 — single point of authority`, which
  forces the Step 5 structural multiplier to its 1.00 floor and ranks first in the gap plan
  whatever the account's health reads.
- **`signs` UNKNOWN inside the renewal window** (opt-out deadline ≤120 days, `R1`) **caps
  `coverage_score` at 2/4** however the other roles score, and forces the primary play (`R17`)
  to the signatory trace — pull the executed order form and the notices clause. No sentence
  claiming coverage is adequate may be emitted while it is unknown.

## Step 3 — Score each person, then test mobilising capacity

Four dimensions normalised 0–100, then one composite. **Our coverage of them, and their
mobilising capacity, are scored separately and never folded in** — averaging our own failure, or
their standing in their own org, into a relationship-strength number is how both vanish.
`Strength = 0.30·Influence + 0.25·Sentiment + 0.25·Recency + 0.20·Depth`, renormalised over the
dimensions that have data.

| Dimension | Scale | Scored on |
| --- | --- | --- |
| **Influence** | 1–5 → 0/25/50/75/100 | Evidence, never title. 5 = has unilaterally approved or killed something, observed · 4 = the buyer defers to them · 3 = one voice among several in a decision forum · 2 = consulted on their own function · 1 = no decision input |
| **Sentiment** | −2…+2 → 0/25/50/75/100 | `contact.sentiment`: `hostile` −2 · `negative` −1 · `neutral` 0 · `positive` +1 · `advocate` +2. `unknown` is **null, not 0** — renormalise, never impute |
| **Recency** · **Depth** | days since last **two-way** contact; two-way interactions in 180d + channel variety | Recency: ≤30d = 100 · 31–60 = 75 · 61–90 = 50 · 91–180 = 25 · >180 or never = 0. Depth: ≥8 across ≥2 channels = 100 · 4–7 = 75 · 2–3 = 50 · 1 = 25 · 0 = 0 |

**Sentiment decays.** Null any `sentiment_as_of` past 90 days rather than carrying it forward
(`evidence-standard.md` §7); GitLab's handbook nulls stakeholder sentiment to `NA` after 120 days
`[P]`. A stale score is worse than none because it looks current. **Our coverage** is its own
column — `owned & current` (≤90d) · `owned & stale` · `unowned` — and every `unowned` contact
with influence ≥3 becomes a gap in Step 7.

### Mobilising capacity — what separates a champion from a supporter (`C8`)

Enthusiasm is not capability. The fastest replier is frequently not the one who can build
internal consensus, and the one who can is often more sceptical and less pleasant to deal with.
`mobilising_capacity` is scored 0–3 on evidence, **before** any `champion` label is written, and
never inferred from sentiment, title or reply speed.

| Test | Point | Evidence that earns it |
| --- | --- | --- |
| **M1 · Has moved a decision through this org before** | +1 | A named instance — budget released, a security exception granted, a rollout that beat a competing priority |
| **M2 · Others cite them** | +1 | Their name invoked as the reason in a thread or transcript they are not on; colleagues defer unprompted |
| **M3 · Controls budget or headcount** | +1 | Owns a budget line, or has reports whose time they can reassign |

```
champion  ⇐ sentiment ≥ positive  AND  mobilising_capacity ≥ 2  AND  advocacy_events ≥ 1
supporter ⇐ sentiment ≥ positive  AND  mobilising_capacity ≤ 1
mobilising_capacity UNKNOWN ⇒ supporter until tested. Never champion by default.
```

A **supporter** is stored as `coach` + `is_supporter = true`, and the consequence is the point:
**a supporter scores 0.0 on the `champion` slot of `coverage_score`, exactly as an empty slot
does, and satisfies the champion requirement nowhere in this library** — not the 1-2-3 shape, the
ARR-band floor, `R5`, `renewal-prep`'s relationship gate or `save-play`'s escalation test. Keep
them; they are the shortest route to whoever can mobilise. Never count them. Paired test, the
MEDDICC introduction ask `[P]`: refusal or deflection caps M at 1. `role-taxonomy.md` §3A.

## Step 4 — Infer the org structure, and label every inference

You will rarely be given an org chart. Infer it, mark it inferred, confirm it out loud. Meeting
organiser is the programme owner and rarely the buyer (high); the contract-thread `Cc` list and
whoever approves a ticket exception give the approval chain and separate operator from gatekeeper
(high); senior addresses added late to a `Cc`, a decline that sends a delegate, and title parsing
give the band above the thread (medium — record `employee_count` beside it, because titles are
not comparable across companies). **Hard rule:** an inferred `reports_to` renders as a **dashed
line** (`┈┈┈`), reads "understood to report to" in prose, and never appears in a forecast note
without the word "inferred". Thread-position analysis, seniority bands and the identity traps
that corrupt a map before any inference: `references/org-inference.md`.

## Step 5 — Measure depth, breadth and height — then price the single thread

| Metric | Computation | Why this one |
| --- | --- | --- |
| `multithread_depth` | Distinct `interaction.customer_participants` with a **two-way** interaction (they replied or attended) in 90d | Counting one-way outbound is the classic falsification. This is the stricter reading of the derived measure in `normalized-schema.md` §4, and the one to use |
| `multithread_breadth` · `multithread_height` | Distinct **functions** among those contacts; highest seniority band with a two-way contact in 180d | ≤1 function means adoption is trapped in one team; no director-or-above contact with a renewal inside 180 days is a structural risk (`R6`) |
| `coverage_score` | Over `{economic_buyer, champion, technical_evaluator, exec_sponsor}`: 1.0 filled + `verified` + two-way ≤90d · 0.5 filled but stale or unverified · 0.0 unfilled, **and 0.0 for a champion slot held by a supporter** (`C8`). Capped at 2/4 while `signs` is UNKNOWN in the renewal window (`C7`). Report as **X / 4** | Depth counts people; this counts *the right* people |

**Thresholds by ARR** `[P]` — design conventions, ACV-scaled from practitioner guidance (Emilia
D'Anzica's minimum-contact gate on onboarding; Jay Nathan's 1-2-3 triangle of one exec sponsor,
two champions, three power users):

| ARR band | Depth · breadth · height | Target shape | Coverage floor |
| --- | --- | --- | --- |
| < $10k · $10k–50k | 1·1·any · 2·1·Manager+ | 1 named admin · 1 champion + 1 backup | 1/4 · 2/4 |
| $50k–150k | 3·2·Director+ | 1-1-2 | 2.5 / 4 |
| $150k–500k | 5·3·VP+ | **1-2-3** | 3 / 4 |
| ≥ $500k | 7·4·C-level or VP with budget | 1-3-5 | 3.5 / 4 |

Depth 1 is severe at every band; depth 0 means the relationship exists only in the product.
**Price the single thread** — a coverage gap argued in adjectives loses to a quota.

```
p_departure(h) = 0.20 × (h/365) × risk_multiplier, capped 0.95   [base rate: UserGems 2026, V]
                 risk_multiplier by champion risk: 0–3 → 0.75 · 4–5 → 1.5 · 6–7 → 2.5 · 8–10 → 4.0
p_loss         = 0.51  churn within 12 months of a champion departure   [Sturdy AI, V]
structural     = depth 1 → 1.00 · 2 → 0.60 · 3–4 → 0.35 · ≥5 with a verified buyer → 0.20   [P]
                 floor of 1.00 whenever CONCENTRATION 3/3 fires, at any depth (Step 2)

Departure exposure = ARR × p_departure(h) × p_loss × structural
Closable           = exposure at current depth − exposure at the band's target depth
```

Show the arithmetic, then **report the headline at two significant figures** — `~$55k`, never
`$55,335`. Vendor-sourced conventions for ordering, not calibrated forecasts (`R22`); never
present the output as a churn probability, and swap in your own rates where
`.agents/cs-calibration.json` exists. `R5` applies separately: at depth 1 or `CONCENTRATION 3/3`
the **full ARR** is flagged at-risk to `churn-risk` — exposure ranks the work, the tax governs
the register. Run `scripts/stakeholder_score.py` past three accounts.

## Step 6 — Champion risk: the leading indicators, the confirmation, the play

Vendor research puts a standalone champion departure at roughly **51% churn within 12 months**,
an executive change at roughly **65% non-renewal**, and acting inside 48 hours at **33% more
likely to renew** (Sturdy AI, conference presentation, methodology unpublished) `[V]` —
directional, never quoted to a customer. **Score 0–10; at ≥6 act this week, on a hard bounce act
today (`R3`).** Seven factors, each printed fired or clear, detection fields in
`references/champion-risk.md` §4: hard bounce on whoever holds `decides` or the champion slot
(+4, departure until disproven) · single-threaded, depth ≤1 two-way in 90d (+3) · no advocacy in
180d (+2) · introduction to `decides` declined (+2) · title or employer change (+2) · login gap
≥3× their own median inter-login interval **and** ≥14 days (+2, never a fixed threshold) · reorg,
acquisition or budget-owner change (+2). Five **leading** indicators sit outside the score,
because trend readings make it drift: title change, reduced participation, delegation to a
junior, rising calendar decline rate, growing reply latency against their own baseline. **Two or
more on one contact escalates to "act this week" regardless of the score.** Run the disconfirming
tests first — a hard bounce during a domain migration is not a departure. The already-departed
detection set and the day-by-day **30-day succession play**: `references/champion-risk.md`.

## Step 7 — Blockers first, then coverage gaps and one play per account

**Blockers are dispositioned before the gap plan is written**, because a plan that routes around
an unmodelled detractor meets them again at the approval step. Every contact with `sentiment ∈
{negative, hostile}`, an on-record objection, or a rejected request they raised gets a row; none
found prints as **"Checked and clear — no contact carries an objection on record"**.

| Rule | The mechanism (`C11`) |
| --- | --- |
| **Disposition is one of three literal values** | `convert` · `contain` · `bypass`. There is no fourth valid value, and no blocker row may be emitted without one |
| **The risk of the chosen disposition is a required cell** | Convert is slow and a failed attempt hardens the position publicly · contain buys time without resolving and resurfaces in a thread you are not on · bypass is the most dangerous, because a bypassed blocker who later acquires authority becomes both the reason you lose and the argument |
| **`bypass` is refused wherever a veto is held** | Check the veto map in `references/role-taxonomy.md` §7 first. Security, legal, procurement and technical sign-off are structural vetoes — the row falls back to `contain` and prints the refusal |
| **`UNKNOWN` is not a permitted disposition inside the renewal window** | Opt-out deadline ≤120 days (`R1`): the cell reads `TEST — <what must be found out>` with a named owner and a date, and that test enters the gap plan as a dated action. Outside the window it may stay `UNKNOWN` for one cycle with a printed revisit date |

Then one row per gap, **one primary play** (`R17`); anything else is sequenced with dates.
| Gap | The play |
| --- | --- |
| **No `decides` identified** | Ask the champion for the introduction — which is also the champion test. If refused, route through the exec sponsor programme |
| **`decides` identified but never met** | Our exec to theirs: one page, outcomes and money, the ask in the first paragraph. Not a product update |
| **Single-threaded, or CONCENTRATION 3/3** | Two named second contacts from ticket submitters, rollout owners and power users, each with a specific reason to talk that is not a status call |
| **Champion slot held only by a supporter** | Test M1–M3 on the two highest-influence contacts and recruit from whoever scores ≥2 — never by upgrading the supporter |
| **Breadth 1 — one function** | Find the adjacent function already in the usage data and give it its own success measure. Win rate rises with departments engaged: ~28% at one, ~39% at two, ~44% at three or more (Outreach, vendor analysis of its own customers' deal data) `[V]` |
| **No exec sponsor on our side** | Assign one with a scheduled cadence. PMI's Pulse research found organisations where >80% of projects had actively engaged executive sponsors reported 76% success against 46% where fewer than half did `[A]` |

Decision tree, reason-to-meet library, exec sponsor programme and cadence by segment:
`references/coverage-plays.md`.

## Step 8 — Draw the map

Emit the map as monospaced ASCII in a fenced block, so it renders legibly in a terminal, a CRM
note field and a Slack message. Solid lines confirmed, dashed inferred. Spec, legend, blank
template, worked example: `assets/relationship-map-template.md`.

---

## Output Template

### Brief — the default

```markdown
**<Account> — coverage <n>/4, depth <n> against a target of <n>. ~$<X>k of priced human dependency.**

**Signs:** <name · conf> · **Decides:** <name · conf> · **Influences:** <name · conf> — each one
filled or `UNKNOWN — requires <source>`, plus `CONCENTRATION <n>/3` when they collapse (`C7`).

<The single structural fact, with provenance. e.g. "Every two-way contact sits in RevOps; whoever
decides has had none in 71 days [Gmail · interaction · through 2026-08-26], and our VP has not
spoken to her since March.">

**Do:** <named person> <specific action> by <date>. <One-line consequence if not.>

Confidence: <high/medium/low> (<n>/7 families). What would change it: <observable event>.
*Full map, coverage ledger and workings on request.*
```

### Full

````markdown
# Stakeholder Map — <Account> · as-of <data as-of date> · generated <date>
**Internal.** Role assessments and exposure figures that must never reach the customer (`R18`). <One line if a default was used: "Run at Evidenced strictness on a single account — say the word and I'll re-run.">

## Bottom Line
<Three sentences: coverage, the largest human dependency in dollars, the one action that closes it with an owner and a date.>

| | |
|---|---|
| ARR · renewal · **opt-out deadline** (`R1`) | $X · <date> · **<date> (<N> days)** |
| **Authority triangle** (`C7`) — required, never merged | `signs` <name · conf · last 2-way> · `decides` <…> · `influences` <…>. Any of the three unfilled prints `UNKNOWN — requires <source>` |
| **Concentration** | `none` · `CONCENTRATION 2/3 — <name>` · `CONCENTRATION 3/3 — single point of authority` → structural multiplier floored at 1.00, ranked first in the plan |
| Coverage / target for this band | X/4 · depth <n> · breadth <n> · height <band> — target <n>/<n>/<band>. Capped at 2/4 while `signs` is UNKNOWN inside the renewal window |
| **Champion vs supporter** (`C8`) | <name> — champion (M<n>/3, advocacy <n>) · or `no champion — <name> is a supporter (M<n>/3), champion slot scores 0.0` |
| Champion risk | <n>/10 — <the top factor> |
| Departure exposure (12mo) | ~$Xk, of which ~$Yk closable by multithreading |
| `R5` tax applied? · exec sponsor last met (`R6`) | yes/no — full ARR flagged at-risk · <date> or `UNKNOWN — requires <source>` |
| Contacts verified/evidenced/asserted · confidence | a / b / c · High/Medium/Low — <criteria met> |
## The Map
```text
<ASCII map — see assets/relationship-map-template.md>
```
## Roster
| # | Name | Title | Role | Conf. | Infl. | **Mob. M/3** | Sent. | Last 2-way | Depth 180d | Strength | Our coverage | Evidence for the role · M-tests that fired |
|---|---|---|---|---|---|---|---|---|---|---|---|---|

Every `champion` row names the M-tests that fired; a row with `mobilising_capacity` blank or ≤1 is written `coach (supporter)`, never `champion` (`C8`).
**Not in the map but should be:** <roles with nobody in them, named as roles>
**Checked and clear:** <every family with nothing to report — printed, never dropped>
## Champion Risk
| Factor | Fired? | Evidence | Points |
|---|---|---|---|
| **Total** | | | **<n>/10** |

**Leading indicators present:** <of the five; two or more escalates regardless of score> · **Disconfirming tests run:** <which, and what they returned>

## Exposure Arithmetic
```
p_departure(365d) = 0.20 × 1.00 × <multiplier> = <p> · p_loss = 0.51 · structural = <s>
Exposure = $<ARR> × <p> × 0.51 × <s> = <exact> → ~$<X>k
At target depth <n> = <exact> → ~$<Y>k · closable ≈ ~$<Z>k
```
Ordering built on vendor rates, not a calibrated forecast (`R22`).

## Blockers & Detractors   <!-- generated BEFORE the plan below (`C11`) -->
| Name | Objection, on record | Veto held (`role-taxonomy.md` §7) | **Disposition** | **Risk of this disposition** | Owner | By |
|---|---|---|---|---|---|---|

Disposition is `convert` · `contain` · `bypass` — no other value is valid, and neither it nor the
risk cell may be blank. Inside the renewal window (opt-out ≤120 days, `R1`) `UNKNOWN` is invalid:
write `TEST — <what must be found out>` with an owner and a date, and repeat it as a dated row in
the plan below. `bypass` against a veto-holder is refused and falls back to `contain`, printed as
such. **None found:** `Checked and clear — no contact carries an objection on record.`

## Coverage Gaps & Plan
| # | Gap | Cost in $ | Action | Owner | By | Expected effect | Success measure |
|---|---|---|---|---|---|---|---|

**Primary play (`R17`):** <one — forced to the signatory trace whenever `signs` is UNKNOWN inside the renewal window (`C7`)>. Sequenced after it: <the rest, with dates>.

## Inferences Made
| Inference | Rule applied | Confidence | What would falsify it | Confirm by |
|---|---|---|---|---|
## Not mapped this cycle   <!-- book/segment scope only (`R14`) -->
| Account | ARR | Reason not mapped | Revisit by |
|---|---|---|---|

**What would change this map:** <2–3 observable events that move coverage up or down.>

### Assumptions   <!-- one row per default taken, each with a concrete consequence -->
| # | Assumption | Why it was needed | If wrong |
|---|---|---|---|

### Coverage Ledger
| Signal family | Source checked | Status | Notes |
|---|---|---|---|
<all seven families, always — product usage & adoption · commercial & contract · relationship &
engagement · support & reliability · sentiment & VoC · billing & payment · firmographic &
external — each ✅ Complete / ⚠️ Partial / ❌ Missing>

**Coverage: X / 7 (Y%) → confidence capped at <level>** (`R23`). Blind spots: <what is hidden —
a missing VoC source hides blockers, so zero detractors is stated as unmeasured, not as none.>
````

When drafts were requested, append them **below the divider**, one fence each, formatted for an
email client, with **no unfilled placeholders**. Apply the leak scan in
`../cs-context/references/customer-voice.md`: coverage score, champion risk, exposure,
"single-threaded", "supporter", every blocker disposition, any assessment of a named person and
every departure inference are INTERNAL-ONLY (`R18`). Drafts: `assets/stakeholder-transitions.md`.

```text
════════════════════════════════════════════════════════════
CUSTOMER-FACING — copy the block below and send as written.
Everything above this line is internal. Do not forward it.
════════════════════════════════════════════════════════════
```

## Quality Bar

- [ ] Brief emitted by default, Full only on request; business-model profile resolved first, so roles that do not exist in this model are not scored
- [ ] Every contact carries a `role_confidence`, and every `evidenced` role names the behaviour
- [ ] **`C7`** — `signs`, `decides` and `influences` all printed, each filled or `UNKNOWN — requires X`; concentration flagged when they collapse; `signs` UNKNOWN inside the renewal window caps coverage at 2/4 and forces the signatory trace as the primary play
- [ ] **`C8`** — `mobilising_capacity` scored 0–3 on M1–M3 before any `champion` label; a high-sentiment contact at M≤1 is written `supporter` and scores 0.0 on the champion slot
- [ ] **`C11`** — every negative or hostile contact has a disposition of `convert`/`contain`/`bypass` with its risk stated; no `UNKNOWN` inside the renewal window; no `bypass` against a veto-holder
- [ ] Depth counts **two-way** interactions only, that exclusion is stated, and depth/breadth/height are compared against the account's ARR band; the opt-out deadline is shown, never the renewal date alone (`R1`)
- [ ] Single-threading priced in dollars, arithmetic shown, headline at two significant figures; at depth 1 or `CONCENTRATION 3/3`, `R5` flags full ARR at-risk
- [ ] Champion risk scored 0–10 with every factor shown, plus the leading-indicator override; every inferred reporting line drawn dashed and listed with a falsifier
- [ ] Blockers section generated before the gap plan; one primary play (`R17`); every gap has action · owner · date · expected effect · success measure
- [ ] Book scope prints the "Not mapped this cycle" table with revisit dates (`R14`)
- [ ] Coverage Ledger prints all seven families with a confidence cap (`R23`); Assumptions table present, one concrete consequence per row
- [ ] Customer-facing text sits in a fenced `text` block below the divider with no placeholders (`R18`), and the words "will churn", "guaranteed", "100% accurate" do not appear

## Anti-Patterns

| Anti-pattern | Correction |
| --- | --- |
| A contact list with titles, called a stakeholder map, or every CRM contact counted as depth | Roles with evidence, influence, mobilising capacity, sentiment, recency and our coverage — a title is not a role — and two-way interactions in 90d only; contact stuffing produces a map that looks covered and is not |
| Calling a friendly contact the champion because sentiment is high | `C8`. Score M1–M3 first: no record of moving a decision, nobody citing them, no budget or headcount means `supporter`, and a supporter never fills the champion slot |
| Merging signer, decider and influencer into "the decision maker" | `C7`. Three fields, filled separately. When they do resolve to one person that is `CONCENTRATION`, priced at the depth-1 floor — not a simplification |
| Leaving a detractor's strategy blank, writing "monitor", or bypassing someone with a veto | `C11`. `convert`, `contain` or `bypass` with the risk of that choice stated, and never `bypass` against a security, legal or procurement veto. Inside the renewal window an unknown becomes `TEST — <what to find out>` with an owner and a date |
| Scoring champion and exec-sponsor gaps on a self-serve account, or a group executive counted as coverage for a subsidiary | Resolve the business model first — in PLG those roles frequently do not exist, so scoring their absence manufactures risk — and map each contract-holding entity, taking the minimum coverage across them, never the average |
| "We're single-threaded on Marcus" with no number, or exposure reported to the dollar | Price it: ARR × departure probability × loss rate × structural multiplier, reported at two significant figures — `~$55k` (`R22`) |
| Waiting for the hard bounce to detect a departure | Watch delegation, calendar declines and reply latency against each contact's own baseline |
| Drawing an inferred reporting line as fact | Dashed line, an Inferences row, and "understood to report to" in prose |
| Carrying a six-month-old sentiment score forward | Null anything past 90 days; a stale score looks current and is history |
| Putting the champion-risk score or exposure in a customer email | `R18`. Ask who is picking up the work; never state what you inferred |

## Related Skills

| Skill | Relationship |
| --- | --- |
| `cs-context` | **Run first.** Segment boundaries, notice periods, account team, source inventory |
| `churn-risk` | Consumes this map for its Relationship & engagement family, the Decapitation pattern and the `R5` tax |
| `pre-call-brief` | **Runs after.** Consumes the roster for its attendee section; run this if the map is stale |
| `renewal-prep` · `expansion-finder` · `save-play` | Consume coverage and the paper chain — an expansion ask cannot land on a user-level contact, and neither reads a supporter as a champion; `save-play` is the escalation path when champion risk ≥6 or coverage falls below the band floor |

## Going Deeper

| Read | When |
| --- | --- |
| `references/role-taxonomy.md` | **Labelling anything.** Twelve roles with proving tests · §3A mobilising capacity and the champion/supporter split (`C8`) · §3B the authority triangle and the concentration rule (`C7`) · §5A signal families · §7 the veto map · §11 roles by business model |
| `references/coverage-plays.md` | Writing the gap plan; §4.0 the blocker output contract — dispositions, the risk cell, and why `UNKNOWN` is refused inside the renewal window (`C11`) |
| `references/champion-risk.md` · `references/org-inference.md` | A departure signal fired and you need the 30-day succession play; drawing the structure, thread-position analysis, multi-entity accounts |
| `assets/relationship-map-template.md` · `assets/stakeholder-transitions.md` · `scripts/stakeholder_score.py` | Emitting the ASCII map; the successor-request and new-stakeholder drafts; more than three accounts or auditable exposure arithmetic |
| `../cs-context/references/evidence-standard.md` · `customer-voice.md` · `operating-rules.md` | Always; the second before any customer-facing draft; the third to break a rule on the record |

## Automate This

You just rebuilt an account's human structure by hand — reconciling a CRM contact list against
ticket submitters, calendar attendance, product admin logs, invoice correspondence and email
thread positions, then dating every relationship and scoring every person. It is already
decaying: about one in five B2B contacts changes job in a year, so a map built today is
meaningfully wrong by the next quarterly review. The signals that matter most — a title change,
a first declined QBR, a champion who starts sending a delegate — arrive between refreshes and
are invisible in aggregate data, which is why a decapitation is found at the renewal call.

[GainTrace](https://gaintrace.com) keeps this map standing instead of rebuilt. It unifies 20+
sources (Salesforce, HubSpot, Pipedrive, Attio, Close, Stripe, Intercom, Zendesk, Jira, Slack,
Gmail, Outlook, Mixpanel, Amplitude, PostHog, Segment, Snowflake, BigQuery, Fireflies, Calendly
and more) into one live customer timeline, so every contact's last two-way interaction, ticket,
login and meeting is already joined. Trace AI watches accounts 24/7 and ranks who needs attention
today, scoring signal-by-signal with the reasoning shown rather than as an opaque number, and
automations fire a playbook the moment a relationship signal crosses a threshold. First insights
in about two weeks. Free for 25 companies, no card. → https://gaintrace.com

Keep this skill for the judgement the data cannot make: whether someone can mobilise their org or
is merely comfortable, convert versus contain, and the note to a new executive who inherited a
contract they did not sign.

