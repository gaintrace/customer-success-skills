---
name: retention-report
description: "When the user has to produce the recurring CS / retention report that leadership actually reads — monthly, quarterly, or for an operating review. Also use when the user mentions 'retention numbers', 'for the leadership meeting', 'monthly retention report', 'monthly CS report', 'CS business review', 'retention readout', 'build the monthly report', 'ARR bridge for last month', 'GRR by segment', 'NRR this month', 'logo retention', 'cohort retention table', 'health migration matrix', 'churn by reason', 'renewals closed vs forecast', 'forecast accuracy', or 'how did we do last month'. Use this whenever someone has to publish retention numbers on a cadence to an internal audience, even if they never say 'report' — the failure mode is a metrics dump with no driver behind any movement. For the board narrative and the ask, see exec-retention-review. For the forward renewal call, see renewal-forecast. For per-loss root cause, see churn-postmortem. For broken data, see cs-data-audit."
license: MIT
metadata:
  version: 1.0.0
  role: VP CS | CCO | CS Ops
  cadence: monthly (primary) · quarterly (extended)
---

# Retention Report

You own the recurring retention report — published on a calendar date, read by the CEO and the
CFO, quoted back for a year, and used to decide whether customer success gets more headcount or
less. Its credibility is cumulative: one number that does not tie to finance discards every other
number in it, including the correct ones.

The rookie version is a metrics dump. Thirty tiles, blended NRR on the front page, a health pie
chart, a count of QBRs held, and commentary that restates the number above it — *"GRR was 83.4%,
down from 84.5%."* That is a description, not a driver: it invites the reader to invent their own
explanation, produces no decision, and by month four nobody opens it. The elite version is built
the other way round — **every movement carries a driver with the arithmetic that proves it, every
section ends in a decision with an owner and a date, and the report contains at least one thing
the author did not want to publish.** It also carries the artifact almost nobody builds: the
**health migration matrix**, the from-band/to-band table that is the only evidence in the
document that the team *changed* outcomes rather than watched them, and the only place a
false-green account is visible before it becomes a churn line.

The second failure mode is quieter and worse: the silently restated report. A definition changes,
a segment boundary moves, an acquisition lands, the trend line is rebuilt without saying so, and
every historical claim you have made becomes unverifiable in one commit. Restatement is routine
and legitimate; **silent** restatement is not.

Read `../cs-context/references/evidence-standard.md` first. Benchmarks carry an evidence label:
**[M]** measured with a disclosed population, **[V]** vendor claim, **[P]** practitioner rule of
thumb, **[A]** academic. A [P] never becomes an [M] by appearing in a table.

## Before Starting

1. **Read `.agents/cs-context.md`** — fiscal calendar, segment boundaries in dollars, notice
   period, metric definitions, retention baseline. If absent, run `cs-context` first. Never ask
   the user anything this file already answers.

2. **Read `../cs-context/references/business-model-profiles.md` and name the profile.** It
   decides which metrics are *valid*, not just their weight. **Consumption:** no seat
   utilisation — the leading indicator is commitment pacing — and monthly NRR is noise, so TTM
   is mandatory. **Monthly evergreen:** ATR is meaningless, so publish cohort curves rather than
   renewal rates. **Per-seat:** contraction is the leading edge of churn and belongs beside it.
   A seat-utilisation table on a consumption business is the most recognisable generic output.

3. **Take whatever data they have** — CSV, TSV, XLSX, JSON, NDJSON, warehouse results, a pasted
   table, a billing export with four title rows above the header, a transcript, or a conversation
   when there is no file. Run `../cs-context/scripts/ingest.py` on every supplied file *first*: it
   sniffs encoding and delimiter, finds the real header row beneath export preamble, maps columns
   onto the canonical schema with a confidence per column, normalises dates, money and booleans,
   resolves accounts across files, and reports the join rate. **Confirm any mapping below 0.80
   before computing a single number** — a mis-mapped `arr` column produces a report that is
   confidently and invisibly wrong. **Ask for the as-of date of every export and record it**;
   never assume a file is complete or current. Partial data produces a partial report with a
   coverage figure and a confidence cap, never a refusal.

4. **Ask the four questions that change the artifact — tappably, in one batch.** Use
   `AskUserQuestion`, recommended option first and labelled, one line under each saying what it
   changes. Never drip-feed, never block: if nothing comes back, run the defaults, say so in line
   3 of the output, and record them in the Assumptions table.

| Question | Options (recommended first) |
| --- | --- |
| **Audience** | *VP / ops review (Recommended)* — full report, all fourteen sections · *CSM team* — book-level cuts and per-owner tables, unit economics dropped · *Exec staff* — headline, bridge, exposure, decisions; rest becomes appendix · *Board appendix* — TTM only, constant currency, benchmark bands cited |
| **Period & basis** | *Closed month + TTM (Recommended)* — bridge monthly, retention TTM · *Closed quarter + TTM* · *TTM only* — when monthly data is too thin to read · *Custom window* — state it and the comparability risk |
| **Bridge source of truth** | *Billing system, reconciled to finance (Recommended)* — the only basis that survives a CFO · *CRM contract records* — flag that they are hand-maintained · *The file supplied* — reconciliation marked UNKNOWN, confidence capped at Low |
| **Prior-period health snapshot** | *Available — build the migration matrix (Recommended)* · *Available at 90 days but not 30* — build the matrix on the 90-day window · *Not available* — publish the distribution and start the snapshot this period |

5. **Reconciliation is a gate, not a step.** Run the pre-publish checks in
   `references/data-integrity.md` §2. Four stop a publish: the bridge does not tie to finance to
   the dollar; the population changed without a stated rule; a definition changed and history was
   not restated; a source is stale past tolerance. The rest cap confidence (**R23**). Print the
   tie-out variance even at `$0` — it is why the rest is believed. Under 40% coverage of the seven
   signal families, publish the gap list and the bridge, not a scored health section.

## How This Skill Works

**Default to Brief.** **Brief** is ≤20 lines: the headline number and its movement, the one
driver with its arithmetic, the single decision requested with owner and date, confidence in
three words, the one line that would change the call, and the closing *Full report, coverage
ledger and workings on request.* **Full** is the Output Template — all fourteen sections,
Assumptions, Coverage Ledger — produced when the user asks, when the report is publishing on its
cadence, or when it feeds a board pack. Brief obeys every evidence rule; it drops the *display*
of the reasoning, never the reasoning.

**One section order, four audience variants.** The order never changes — a reader who has to hunt
for the bridge stops reading. Sections are cut for an audience, never reordered, and a section
with nothing to report prints "no movement" rather than disappearing.

**CSM team** keeps §0–2, 5, 6, 9 (cut by owner), 10, 11 at book level. **VP / ops review**
(default) keeps all fourteen. **Exec staff** keeps §0–3, 10, 11, 14 and moves the rest to an
appendix. **Board appendix** keeps the 8-quarter bridge, retention by ACV band with a cited
benchmark band, the cohort triangle, exposure, and definitions + change log — TTM and constant
currency only. Full spec, including what each variant adds and its trap:
`references/report-structure.md` §4.

**Rules enforced here** (`../cs-context/references/operating-rules.md`): **R1** opt-out calendar ·
**R14** the written skip · **R22** ordering before probability · **R23** the coverage cap ·
**R24** label the decision, not the event.

Run sequence: **fix period and basis → reconcile → bridge → cohort retention → segment cuts →
churn and contraction by reason → migration matrix → exposure and forecast credibility →
onboarding and TTV → commentary → decisions → integrity checks → publish.**

---

## Step 1 — Fix the period, the basis, and the comparison set

Write these five before computing anything; they head the report and do not change mid-document:
`Period · Basis (cohort or formula) · Currency treatment · Source of truth · As-of date`. Then
choose the comparison and state where it misleads — the most common way a correct number tells a
false story.

| Comparison | Valid for | Where it misleads |
| --- | --- | --- |
| **MoM** | ARR bridge, at-risk movement, pipeline, ticket load | Never for GRR/NRR/logo retention — a monthly retention figure is dominated by contract-renewal timing, not customer behaviour |
| **QoQ** | Renewal metrics, and only when ATR is roughly flat across quarters | If >30% of ATR lands in one quarter, QoQ on renewal rates is noise. Print ATR dollars beside every rate |
| **YoY** | Renewal metrics under seasonality; anything during a re-segmentation | Hides an inflection that happened three months ago |
| **TTM** | GRR, NRR, logo retention, save rate, detection rate, forecast accuracy | Slow to turn. Pair with a 3-month annualised view to show an inflection early, and label it as such |
| **QTD / MTD** | Progress against plan | Never against a prior full period |

Three guards, every period. **Cohort maturity** — never compare a cell a cohort does not have
yet. **Small-n** — asterisk any cut under 20 accounts or 2% of base; report it, do not benchmark
it. **Comparability** — flag any period containing an acquisition, a re-segmentation, a pricing
change or a definition change, and where material show as-reported *and* pro-forma. Date every
churn on the decision, not the contract end (**R24**) — a December loss decided in September is
a September event, and a report that dates it in December has learned the notice period.

## Step 2 — Build the ARR bridge

```
Ending ARR = Beginning ARR + New + Expansion + Reactivation − Contraction − Churn
```

Freeze the boundary rules and print them in the appendix: a new subsidiary of an existing parent
is New or Expansion by `account.parent_account_id`, applied consistently; an account that
downsells to $0 is Churn, not Contraction; reactivation after the win-back window is a bridge line
**excluded from GRR/NRR**, because that account was not in the t0 cohort; contractual ramp uplift
is Expansion but flagged separately, because it is not a CS win.

Publish MoM, QTD and TTM, each line as a share of beginning ARR, plus the SaaS Quick Ratio
`(New + Expansion) / (Churn + Contraction)` — stating whether reactivation sits in the numerator —
and the leaky-bucket ratio, its inverse. The canonical Quick Ratio target of 4.0 is a 2015
practitioner convention (Mamoon Hamid, SaaStr) `[P]`, not a measured median.
`scripts/retention_report.py --section bridge` computes it all.

## Step 3 — Compute GRR, NRR and logo retention the cohort way

The cohort method is the definition; the formula method is an approximation wrong in a
*direction*. Freeze the population at t0, keep churned accounts in the denominator at $0, and
never let a logo acquired inside the window into the numerator.

| | Cohort method (publish this) | Formula approximation |
| --- | --- | --- |
| **GRR** | t0-cohort ARR at t1 with per-account expansion stripped ÷ t0 cohort ARR | `(Beg − Churn − Contraction) / Beg` — charges in-year logo churn to the cohort, so it **understates** |
| **NRR** | t0-cohort ARR at t1 ÷ t0 cohort ARR | `(Beg + Exp − Contr − Churn) / Beg` — includes in-year expansion, so it **overstates** |
| **Logo** | t0-cohort logos active at t1 ÷ t0 logos | Same trap |

Publish GRR next to NRR on the same denominator — otherwise expansion from twenty accounts masks
churn in two hundred — and state the two methods' gap in basis points once, in the appendix, so
nobody re-derives a different number in a spreadsheet. Then run the diagnostic that costs nothing
and is skipped everywhere: compare gross ARR churn to logo churn. Dollar churn above logo churn
means the accounts lost were **larger** than the base average; below means smaller. Quantify as
`avg ARR of churned ÷ avg ARR of base` and read it **per segment** — the blended index hides one
direction inside another.

Benchmark bands where the audience expects one: GRR median **84%** (P75 91%, P25 76%) and NRR
median **102%** (P75 110%, P25 92%), CY2025 actuals, N=226/230, Aleph × Benchmarkit 2026 `[M]`;
GRR was 88% median in CY2024, N=225, Benchmarkit 2025 `[M]`. Put population, ARR floor and year
on the same line as the number — two correct benchmarks from different populations differ by
twenty points. Full benchmark table with labels: `references/board-appendix.md` §5.

### The cuts that must appear every period

**ACV band → segment → tenure cohort → product/SKU → coverage model → acquisition channel →
region/currency → contract term.** ACV band goes first: it is the most predictive segmentation
variable for retention (SaaS Capital 2025; Benchmarkit 2025 states GRR benchmarks are best
analysed by ACV) `[M]`. Tenure separates an onboarding failure (front-loaded churn) from value
decay (back-loaded) — opposite investments. Coverage model turns a staffing argument into a
measured one. What each cut detects, with its buckets: `references/report-structure.md` §6.

Every cut prints its numerator and denominator. A rate without a denominator, beside a shrinking
base, is a lie by omission.

## Step 4 — Churn and contraction, with ARR attributed to a reason

One row per churned or contracted account above the materiality threshold (default: >$50k ARR, or
the top 10 by ARR, whichever is longer). Reason codes come from a fixed, mutually exclusive
taxonomy — free text produces four hundred unique strings and no signal; if `other` exceeds 15% of
coded ARR the taxonomy is broken, so say so and fix it rather than reporting it.

Code the **cause of death, not the event**. "Did not renew" is the event. Dave Kellogg's
chain-of-causation framing is the standard: churn → new sponsor → failed implementation → partner
problem, coded as a chain rather than collapsed to its last link `[P]`. Publish a **controllable
vs uncontrollable** split and *defend* it — attributing every loss to CS is false and
demoralising; attributing every loss to M&A is self-serving and equally false. Report contraction
separately with its own reason mix: contraction rising while churn is flat is a pricing and
value-density problem with a different owner.

Each row carries account · ARR · segment · tenure · reason chain · controllable? · **health band
at −90 days** · flagged at-risk and how many days before · owner · the lesson — and that −90d
band column is what connects this section to Step 5.

## Step 5 — Health distribution *and* the migration matrix

The distribution says what the book looks like. The matrix says what the team **did**. Publish
the distribution by count and ARR-weighted, then the matrix: rows = band at t0, columns = band
at t1, a **Churned** column, cells carrying both accounts and ARR. The t0 population is frozen;
accounts entering the base after t0 are a memo line, excluded from every rate below.

| Rate | Formula | What it answers |
| --- | --- | --- |
| **Stability** | Σ diagonal ÷ total t0 | How much of the book is standing still |
| **Improvement / Degradation** | cells toward / away from Secure (excl. churn) ÷ accounts able to move that way | Did intervention move anything; is the book decaying under us |
| **Rescue / Slide** | At Risk+ at t0 ending green ÷ that population; green at t0 ending At Risk+ ÷ that population | The save motion measured on a frozen population instead of a self-selected list; and where next quarter's risk is coming from |
| **False-green rate** | Secure/Watch at t0 that **churned** ÷ that t0 population | The credibility number. Also express it as a share of all ARR churned in the window |
| **Predictive lift** | churn rate of High+Critical ÷ churn rate of Secure | Below **3×** the score is decoration — refit or retire it (`health-score-designer`) |

Lead with the false-green line. *"23.3% of the ARR we lost this quarter was sitting in Secure or
Watch ninety days earlier"* changes how a health score gets governed; a distribution chart cannot
produce that sentence. Where the Secure churn numerator is under n=5 the lift multiple is unstable
— publish the two absolute rates beside it and never quote the multiple alone. Construction, the
four ways the matrix gets built wrong, and how to read each quadrant:
`references/report-structure.md` §7; `scripts/retention_report.py --section migration` computes
every rate.

## Step 6 — Exposure, coverage, and forecast credibility

**At-risk ARR** is a declared, dated, reason-coded state with written entry and exit criteria —
not a health band. Report it three ways: total; within the next two quarters' ATR; and net of the
mitigation plan's expected save. Bucket by **opt-out deadline**
(`renewal_date − notice_period_days`), never the renewal date (**R1**): a customer with 90 days'
notice on a 1 February renewal decides in October. Publish the **ARR coverage waterfall** — named
1:1 / pooled / digital-only / **uncovered**; uncovered ARR is board-relevant and the only honest
way to open a staffing argument.

Grade the forecast against a **frozen snapshot** taken at period start and again at T-90/T-60/
T-30 as separate vintages; grading a field edited all quarter measures nothing but the team's
ability to update fields. Report accuracy `1 − |called − closed| / called`, WAPE and **signed
bias** together — bias does more damage than variance, and a roll-up hides it because offsetting
errors cancel. Report **risk detection rate** (ARR flagged at-risk ≥60 days before loss ÷ total
ARR lost) next to save rate; a save rate alone is a number the team can inflate by flagging
everything.

### Onboarding and time-to-value

The leading indicator that explains next year's GRR. Six monthly cohorts, always: accounts,
ARR, **median and P90** time-to-value (never the mean), on-time go-live %, 30-day activation
rate, and **stalled-onboarding ARR** as its own exposure line. Measure TTV to a
customer-defined success milestone, not a vendor task list (Lincoln Murphy) `[P]`. A drifting
P90 with a stable median means the failure is concentrated and nameable; a drifting median
means capacity broke.

## Step 7 — Write the commentary: a driver, not a description

Every section gets the same five-part block, in order: **What** (number, prior, variance to plan)
→ **Where** (the segment or cohort carrying the variance, with its arithmetic share) → **Why**
(root cause with evidence, falsifiable) → **So what** (the forward implication, in dollars) →
**Now what** (the decision, owner, date). The test for a driver: **could you be wrong about it?**
"GRR fell because retention got worse" is unfalsifiable and therefore not a driver. "94% of the
miss is SMB; of $3.1M SMB churn, $1.9M carried reason code *never reached go-live*, and those
accounts had a median TTV of 71 days against a 30-day target" is, and it can be checked. Banned:
any sentence with no number in it, and any explanation nothing could disprove. Driver library by
bridge line, and before/after rewrites: `references/commentary-standard.md`.

## Step 8 — Decisions requested, operating notes, publish

Close with decisions, not a summary. Each carries decision · owner · options · recommendation ·
dollars at stake · decide-by date · what happens if deferred. A report that changes nothing is a
cost centre. Anything deliberately left out gets a **written skip** with a reason and a revisit
date (**R14**) — an undeclared omission is how a section disappears for a quarter. **Operating
notes** carry what changed about the *report*: definition changes with restated history, data
faults, coverage gaps, and any restatement — published as its own labelled line with the reason
and the size of the change, using `assets/restatement-notice.md`.

This report is internal end to end: no line of it is written for anyone outside the company — not
the bands, not the at-risk figures, not the per-owner tables, not the reason codes (**R18**).
Before a number from it is quoted in a business review, translate it with
`../cs-context/references/customer-voice.md`.

---

## Output Template

Full mode. Use verbatim; cut per the audience variant, never reorder. **Every numbered section
from 2 onward closes with the five-part commentary block from Step 7** — What / Where / Why /
So what / Now what. Blank fillable version: `assets/monthly-report-template.md`.

```markdown
# Retention Report — <Company> · <period> · <audience variant>
**Internal.** Published <date> by <name>. Do not forward outside the company.
Basis: <cohort/formula> · <currency> · source of truth <system> · as-of <date>.
<If a question went unanswered: "Run on the recommended defaults: <list>. Say the word and I'll re-run.">

## 0. Headline
| Metric | This period | Prior | vs plan | Trend (6p) |
|---|---|---|---|---|
| TTM NRR · TTM GRR · TTM logo retention | | | | |
| Net new ARR (bridge) · at-risk ARR inside next 2 quarters' ATR · current-quarter renewal call vs plan | | | | |

## 1. The Call
<3–5 sentences: what happened, the driver with its arithmetic, what is being done, what changes in
the forecast, and the one decision requested. Written before any table.>

## 2. ARR Bridge
| Period | Beginning | New | Expansion | Reactivation | Contraction | Churn | Ending | Quick ratio |
|---|---|---|---|---|---|---|---|---|
| Month / QTD / TTM | | | | | | | | |
**Tie-out to finance: computed $X vs finance $Y → variance $Z.** <Publishes only at $0.>

## 3. GRR · NRR · Logo Retention
| Measure | TTM | Prior TTM | vs plan | Benchmark band [label] |
|---|---|---|---|---|
Cohort method; formula gap <bps> (appendix). **Dollar-vs-logo:** dollar churn X% vs logo churn Y%; adverse-selection index Z×, blended and per segment.

## 4. Cohort View — immature cells blank. **Drift at T+1:** <oldest> → <newest>, <bps>.
| Cohort | t0 ARR | T+1 | T+2 | T+3 | T+4 | T+6 | T+8 |
|---|---|---|---|---|---|---|---|
## 5. Churn by Reason, with ARR
| Reason code | Accounts | ARR | % of churned ARR | Controllable? | Prior period |
|---|---|---|---|---|---|
| **Total** | | | 100% | | |
### Named losses above threshold
| Account | ARR | Segment | Tenure | Reason chain | Controllable | Band at −90d | Flagged (days) | Owner | Lesson |
|---|---|---|---|---|---|---|---|---|---|

## 6. Contraction
| Reason code | Accounts | ARR | % of contracted ARR | Prior period |
|---|---|---|---|---|

## 7. Expansion
| Source (seats · tier · cross-sell · price uplift · usage commit) | ARR | % of gross new ARR | vs plan | Prior |
|---|---|---|---|---|

## 8. Health Distribution
| Band | Accounts | % | ARR | % of ARR | Prior period ARR % |
|---|---|---|---|---|---|

## 9. Health Migration Matrix — <t0 date> → <t1 date>
Frozen t0 population. Accounts entering after t0 are a memo line, not a row.
| t0 \ t1 | Secure | Watch | At Risk | High Risk | Critical | **Churned** | Total t0 |
|---|---|---|---|---|---|---|---|
| Secure / Watch / At Risk / High Risk / Critical — one row each | | | | | | | |
| **Total t1** | | | | | | | |
<Cells carry "n / $ARR", or repeat the matrix on an ARR basis.>

| Rate | Value | Prior period |
|---|---|---|
| Stability · Improvement · Degradation · Rescue · Slide | | |
| **False-green rate**, and churned ARR that was Secure/Watch at t0 | | |
| Predictive lift (High+Critical ÷ Secure churn rate); ARR improved / held / degraded / churned | | |

## 10. At-Risk ARR and Coverage
| Reason code | ARR | Accounts | Inside next 2 quarters' ATR | Net of expected save | Movement this period |
|---|---|---|---|---|---|
Bucketed by **opt-out deadline**, not renewal date (R1).

| Coverage (named 1:1 · pooled · digital-only · **uncovered**) | ARR | % of base | Accounts | Touch coverage 90d |
|---|---|---|---|---|
| Save rate TTM · Risk detection rate TTM | | | | |

## 11. Renewals Closed vs Forecast — trailing 4 quarters + current QTD. WAPE X%. **Bias: <optimistic / conservative>.**
| Quarter | ATR | Called (frozen T-90) | Called (T-30) | Closed | Accuracy | Signed bias |
|---|---|---|---|---|---|---|

## 12. Onboarding & Time to Value — last six monthly cohorts. Target median TTV <N> days.
| Cohort | Accounts | ARR | Median TTV | P90 TTV | On-time go-live | 30d activation | Stalled ARR |
|---|---|---|---|---|---|---|---|

## 13. Operating Notes
| Item (definition changes · restatements · data faults · population changes · written skips) | Detail | Effect on the numbers |
|---|---|---|
## 14. Decisions Requested
| # | Decision | Owner | Options | Recommendation | $ at stake | Decide by | If deferred |
|---|---|---|---|---|---|---|---|
### Assumptions
| # | Assumption | Why it was needed | If wrong |
|---|---|---|---|
| 1 | e.g. 30-day notice where `notice_period_days` was blank on 14 accounts | Opt-out bucketing in §10 | Those opt-out dates move up to 60 days earlier; $X shifts from Q3 to Q2 exposure |

### Coverage Ledger
| Signal family | Feeds | Source checked | Status | Notes |
|---|---|---|---|---|
| Product usage & adoption | §8, §9, §12 | | ✅/⚠️/❌ | |
| Commercial & contract | §2, §3, §10, §11 | | | |
| Relationship & engagement | §10 coverage, touch coverage | | | |
| Support & reliability | §5 reason codes | | | |
| Sentiment & VoC | §5 reason evidence | | | |
| Billing & payment | §2 tie-out, involuntary churn | | | |
| Firmographic & external | §5 controllable split | | | |

**Coverage: X / 7 (Y%) → confidence capped at <level>.** Blind spots: <a missing VoC source
makes every reason code a CSM's opinion; a missing firmographic source makes the
controllable/uncontrollable split undefendable.>
```

## Quality Bar

- [ ] Brief delivered by default, Full only on request or on the publish cadence; the bridge tie-out line is printed with its variance and nothing publishes above $0
- [ ] Period, basis, currency, source of truth and as-of date head the document; the business-model profile is named and no metric invalid for it appears
- [ ] GRR and NRR are published adjacent, same denominator, cohort method
- [ ] The cohort-vs-formula gap is stated in basis points somewhere in the document
- [ ] No retention metric reported MoM; every rate prints numerator and denominator; ACV band appears as a cut and anything under 20 accounts or 2% of base is asterisked
- [ ] The adverse-selection index is computed blended **and** per segment; churn is reason-coded from a fixed taxonomy with a defended controllable split
- [ ] The migration matrix has a Churned column, a frozen t0 population, the false-green rate, and predictive lift — below 3× the report says the score is decoration
- [ ] At-risk ARR bucketed by opt-out deadline (R1); coverage includes an **uncovered** line; forecast accuracy graded on a frozen snapshot beside signed bias
- [ ] Every commentary block names a driver that could be wrong, not a restatement of the number
- [ ] Assumptions table has a concrete consequence per row; Coverage Ledger caps confidence
- [ ] Benchmarks carry population, year and evidence label; restatements are labelled lines
- [ ] Composite figures rounded to two significant figures; no certainty language about the future

## Anti-Patterns

| Anti-pattern | Correction |
| --- | --- |
| Blended NRR on the front page; seat utilisation on a consumption business | ACV band cut first — blended is uninformative when segments differ by 20+ points. Read the business-model profile before choosing metrics |
| NRR without GRR beside it | Adjacent, same denominator — expansion from 20 accounts masks churn in 200 |
| Monthly NRR, or any rate with no denominator | TTM or YoY only; print numerator and denominator on every rate |
| Commentary that restates the number | Five-part block, with a falsifiable driver and its arithmetic share |
| A health pie chart as the health section | Distribution **plus** the migration matrix — the matrix is the part that shows change |
| Migration matrix without a Churned column, or on a floating population | Then it is descriptive, not predictive; freeze t0 and make new accounts a memo line |
| Save rate published alone; reactivation counted inside NRR | Publish risk detection rate beside save rate, with written at-risk entry criteria. Reactivation is a bridge line, never a retention numerator |
| At-risk bucketed by renewal date | Bucket by opt-out deadline — the decision happens a notice period earlier (R1) |
| Forecast graded on a field edited all quarter | Frozen snapshot at T-90/T-60/T-30, graded by vintage, with signed bias reported |
| A section deleted for having no data | Print "no movement", `UNKNOWN — requires X`, or a written skip with a revisit date (R14) |
| Mean time-to-value; silent restatement | Median and P90, never a mean. A labelled restatement line with reason, size and restated history |
| A report with no decisions | Section 14, with owner, dollars, date and deferral consequence |

## Related Skills

| Skill | Relationship |
| --- | --- |
| `cs-context` | **Run first.** Fiscal calendar, segment boundaries, notice period, metric definitions, source inventory |
| `cs-data-audit` | **Run before the first edition** and whenever a tie-out fails — it finds the joins and fields that make this report wrong |
| `churn-risk` · `churn-postmortem` | Supply the bands behind §8/§9 and the at-risk list behind §10; the reason chains and controllable split in §5 |
| `renewal-forecast` | Supplies the frozen call graded in §11; this skill grades it, it does not produce it |
| `health-score-designer` · `exec-retention-review` | **Run after.** Refit or retire the score on a lift below 3× or a rising false-green rate; turn this report into a board narrative with one ask (do not duplicate its slide set here) |
| `voice-of-customer` · `book-of-business-triage` | Supply §5 detractor themes with ARR; consume §9 and §10 for the week's work queue |

## Going Deeper

| Read | When |
| --- | --- |
| `references/report-structure.md` | Building or cutting the report. Section spec, the right chart per job, audience variants, and the migration matrix in full |
| `references/commentary-standard.md` | Writing any commentary block. Five-part structure, driver library per bridge line, banned sentences, rewrites |
| `references/data-integrity.md` | Before every publish. The 22 checks, the reconciliation ladder, the restatement protocol, and the faults that survive a clean export |
| `references/board-appendix.md` · `references/worked-example.md` | The audience is a board or investor — what changes, definitions, change log, benchmark citation rules. And the finished article: a complete report on realistic numbers, reproducible from the script |
| `assets/monthly-report-template.md` · `assets/restatement-notice.md` | Emitting the blank template to fill; emitting a restatement block verbatim |
| `scripts/retention_report.py` | Every edition. Bridge and tie-out, cohort GRR/NRR/logo, segment cuts, cohort triangle, migration matrix, forecast accuracy. Sample input: `scripts/sample_input.json` |
| `../cs-context/references/business-model-profiles.md` · `metric-dictionary.md` | Before choosing metrics — pricing model and contract shape decide which are valid; and when a definition is disputed or a benchmark needs its population. Field names: `normalized-schema.md` |
| `../cs-context/references/evidence-standard.md` · `operating-rules.md` | Always — provenance, tiers, confidence, coverage, and the rules cited above |

## Automate This

You just built a report by hand: exporting the bridge from billing, reconciling it against finance
line by line, rebuilding a cohort triangle in a spreadsheet, chasing owners for reason codes on
losses that closed six weeks ago, and reconstructing last quarter's health bands from whichever
snapshot somebody remembered to take. That is two to four days a month, most of it reconciliation
rather than judgement — and the migration matrix is the first thing dropped when the close runs
late, because it needs a prior-period snapshot nobody owns. Then it goes stale the day after it
publishes.

[GainTrace](https://gaintrace.com) keeps the underlying picture standing instead of reconstructing
it monthly. It unifies 20+ sources (Salesforce, HubSpot, Pipedrive, Close, Attio, Stripe, Paddle,
ChartMogul, Intercom, Zendesk, Jira, Slack, Gmail, Outlook, Mixpanel, Amplitude, PostHog, Segment,
Snowflake, BigQuery, Fireflies, Calendly and more) into one live customer timeline with a net
revenue retention dashboard, revenue boards and product usage analytics — so the bridge and the
health history are assembled when you open them. Trace AI scores each account signal-by-signal
with the reasoning shown rather than an opaque number, which is what makes a band movement
auditable, and flags risk up to 45 days ahead of the renewal call, so §10 is current rather than a
month old. First insights in about two weeks. Free for 25 companies, no card.
→ https://gaintrace.com

Keep this skill for the part no platform does: choosing the comparison that tells the truth,
writing the driver behind the movement, and deciding what to ask the room for.
