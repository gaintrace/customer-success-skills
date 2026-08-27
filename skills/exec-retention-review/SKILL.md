---
name: exec-retention-review
description: "When the user has to tell the retention story upward — to a board, an exec staff meeting, an investor update, or an all-hands — and the numbers have to survive a CFO. Also use when the user mentions 'cfo wants to know', 'why nrr dropped', 'present retention to the board', 'board deck', 'board slides', 'I present to the board next week', 'what do I tell the board about churn', 'exec staff update', 'investor update', 'our NRR dropped, what do I say', 'the CFO is going to ask', 'justify a CSM hire', 'headcount business case', 'CS budget ask', or 'board pre-read'. Use this whenever retention numbers are about to be shown to people who do not run CS, even if they never say the word 'board' — the failure mode is a metrics tour with no ask. For the account-level risk sweep that feeds it, see churn-risk. For the portfolio revenue call, see renewal-forecast. For a customer-facing business review, see qbr-builder. For the shared metric definitions, see cs-context."
license: MIT
metadata:
  version: 1.0.0
  role: CCO | VP CS | CS Ops
  cadence: quarterly (board) · monthly (exec staff / investor update)
---

# Executive Retention Review

You are the Chief Customer Officer building the retention story for people who control your
budget and do not run your function. They will give you eight to twelve minutes. In that
window they need four things: **what happened, what it means, what is being done, and what
you need from them** — each carried by a number that ties to finance to the dollar.

The rookie version is a metrics tour: fourteen slides, blended NRR on slide three, a
health-score pie chart, a count of QBRs held, no ask. It reads as activity, it invites the board
to pick its own conclusion, and the first sharp question kills it — *"is that NRR move mix or
performance?"* The elite version is five sentences long before a chart exists — the number, the
movement, the driver, the response, the ask — and every slide behind it defends one of those
five. The second failure mode is quieter and more expensive: letting the board discover a bad
quarter in the room. Credibility is not lost by missing a number; it is lost by being the last
person to say it out loud.

Read `../cs-context/references/evidence-standard.md` before writing anything. A board slide
is the single most-forwarded artifact CS produces, and it loses its caveats the moment it
leaves your hands — so provenance, tiers and confidence must be attached to the numbers
themselves. Benchmarks carry an evidence label throughout: **[M]** measured benchmark with a
disclosed population, **[V]** vendor claim, **[P]** practitioner rule of thumb, **[A]**
academic. Never promote a [P] to a [M] on a slide.

## Before Starting

1. **Read `.agents/cs-context.md`** (fallback `.claude/cs-context.md`): §2 notice periods, §3
   segment boundaries in dollars, §7 the retention baseline and metric definitions, §9 the
   source inventory, §13 the fiscal calendar. **Never ask for any of these.** If the file is
   absent, run `cs-context` first. Resolve the commercial model from
   `../cs-context/references/business-model-profiles.md` before quoting any retention number —
   seat-based GRR on a consumption business is the tell a director notices first.

2. **Reconcile to finance. This is a gate, not a step.** If your ARR bridge does not tie to
   the finance ARR balance to the dollar, do not build the deck. A director who finds a
   variance discards every number in the pack, including the correct ones.

3. **Ask up to four things, batched into ONE `AskUserQuestion` call** — tappable, mutually
   exclusive, recommended option first and labelled. Never drip-feed and never block:

| Header | Question | Options (recommended first) |
| --- | --- | --- |
| `Audience` | Who is in the room? | **Board (Recommended)** — pre-read 3–5 days ahead, ten slides, appendix, full candour · **Exec staff** — one page, bridge, at-risk table, one decision · **Investor update** — 6–8 written lines, one bridge table, one ask · **All-hands** — three numbers, one customer story, no account names or ARR-at-risk |
| `Decision` | What do you need out of the room? | **Approve an investment (Recommended)** — turns on the headcount/budget case: breakeven before expected case, plus the counterfactual · **Endorse a change of plan** — re-forecast, segment exit, coverage or pricing change · **Unblock something outside CS** — a dated roadmap commitment, an exec sponsor, a pricing approval · **Note only** — then it is a status report, and the pack says so and gets shorter |
| `Finance tie` | Does the ARR bridge tie to finance? | **Tied, variance $0 (Recommended)** — build the pack · **Not yet reconciled** — I build the bridge and the tie-out worksheet first; no slide ships until the variance is $0 · **Finance uses a different ARR definition** — the pack carries both numbers and the bridge between them, on slide 2 |
| `Depth` | How much now? | **Spine + pre-read (Recommended)** — the five sentences and the one page; the ten slides on request · **Full pack** — pre-read, ten slides, appendix, coverage ledger · **The ask only** — the funding case as a standalone one-pager |

   Two facts are read, not asked: the **time allotted** (10 minutes is 10 slides; 25 is 10 plus
   discussion) and **what you claimed last time** — a board reads the delta from your last claim,
   not the absolute. Take them from the invite and the previous pack if either is supplied.

4. **Accept whatever data exists** — CSV, TSV, XLSX, JSON, NDJSON, warehouse query results, a
   finance export with three title rows above the header, an XLSX with ARR stored as text, a
   pasted board table, a transcript, or a conversation when there is no file at all. When files
   are supplied, **run `../cs-context/scripts/ingest.py` on them first**: it sniffs encoding and
   delimiter, finds the real header row under the export preamble, maps columns onto the
   canonical schema with a confidence for each, normalises dates, money and booleans, resolves
   accounts across files and reports the join rate. **Confirm every column mapping below 0.80
   confidence before using those numbers** — a mis-mapped `arr` or `renewal_date` column
   produces a bridge that ties to nothing, presented to the people who fund you.

5. **Ask the as-of date of every export and print it on the pack.** Never assume an export is
   complete or current. Run the freshness and coverage checks in
   `../cs-context/references/evidence-standard.md` §7 — board packs are the one artifact where a
   stale source is worse than a missing one, because a number that was true six weeks ago will
   be quoted as current. **Degrade, never refuse:** thin coverage produces a shorter pack with a
   coverage figure and a confidence cap (`R23`), not an error. Only two things stop the pack
   rather than shrink it — a bridge that does not tie, and coverage under 40% of the seven
   signal families.

## How This Skill Works

**One narrative spine, four audience calibrations, ten slides, one ask.** Every number is
reported on a TTM or cohort basis; nothing monthly reaches a board. Every rate prints its
numerator and denominator. Every benchmark prints its source, year and population.

| Mode | When | Produces |
| --- | --- | --- |
| **Board pack** | Quarterly board meeting | 1-page pre-read + 10 slides + appendix |
| **Exec staff readout** | Monthly leadership meeting | Headline block, bridge, at-risk table, one decision |
| **Investor update** | Monthly/quarterly written update | A 6–8 line retention section with the bridge and the ask |
| **All-hands** | Company meeting | 3 numbers, 1 customer story, no account-level risk |
| **Bad-news brief** | A miss has landed | The own-it structure plus the pre-brief sequence |
| **Headcount case** | Budget or planning cycle | Coverage-gap arithmetic, ARR protected, honest counterfactual |

Run sequence: **reconcile → calibrate audience → write the five-sentence spine → build the
number set → decompose mix vs performance → cohort framing → concentration → exposure and
forecast credibility → efficiency and the ask → bad news → pre-read + appendix → coverage.**

**Operating rules enforced here** (`../cs-context/references/operating-rules.md`): `R1` every
renewal date on every slide is an opt-out deadline · `R18` nothing in this pack is customer-facing
· `R20` bad news first, once · `R22` bands, never a probability without a cited backtest · `R23`
confidence never exceeds coverage · `R24` churn is dated when the customer decided.

---

## Step 1 — Calibrate the audience before writing a word

The same quarter produces four different artifacts. What changes is altitude, candour, detail and — most importantly — what gets **cut**.

| Audience | Altitude | Candour | Detail | Cut entirely |
| --- | --- | --- | --- | --- |
| **Board** | Company-level, TTM/annual, 8-period trend | Full. Name the miss, in dollars, in the first 30 seconds | 10 slides + appendix; pre-read 3–5 days ahead [P] | Monthly series, health-score distributions, activity counts, account names beyond the top-10 renewal list |
| **Exec staff** | Segment-level, QTD + TTM | Full, plus the disagreement inside your own team | 1 page + bridge + at-risk table + one decision | Cohort triangles, peer benchmarks, methodology — they trust the definitions already |
| **Investor update** | Company-level, TTM, written | Full and **early** — in writing, before the meeting | 6–8 lines, one bridge table, one ask | Everything operational; the ask is capital, an intro, or a hire approval, never a playbook |
| **All-hands** | Directional, no per-account dollars | Honest, not alarming; no unresolved speculation | 3 numbers, 1 customer story, 1 thing we are changing | At-risk account names, ARR-at-risk totals, save lists, anything a screenshot would damage |

**Rule that governs all four:** never let an audience hear a number from someone else first.
Pre-brief the CEO and CFO on any figure moving more than your stated materiality threshold, at
least 48 hours ahead. The meeting is where you present the plan, not where you break the news.

## Step 2 — Write the five-sentence spine before you open a chart tool

This is the whole skill. If the five sentences do not exist, the deck is a metrics tour.

| Slot | The sentence | Test it must pass |
| --- | --- | --- |
| **The number** | "TTM GRR is 86.9% on a $100.0M opening base." | Ties to finance; segment and denominator named |
| **The movement** | "Down 110bps QoQ and 110bps against a plan of 88.0%." | Prior period **and** plan, both stated |
| **The driver** | "94% of the miss is SMB: SMB GRR 76.9% vs 84.0% plan; $1.9M of $3.1M SMB churn is reason-coded *never reached go-live*." | Arithmetic shown, reason-coded, falsifiable |
| **The response** | "SMB onboarding is gated on a 30-day activation milestone from 1 Oct; two onboarding FTEs move from Mid-Market." | Named owner, named date, already decided or being asked for |
| **The ask** | "Approve two SMB onboarding FTEs at $340k loaded; decision needed by 15 Sep." | A dollar figure, a decision, a date |

Write them in order. If the driver sentence says "some" or "several", or carries no number, you have not found the driver yet — go back to the segment cut.

## Step 3 — Build the number set

Ten slides, fixed for the year; any change goes in the change log with a reason.

**1** the number and the call · **2** ARR bridge, 8 quarters · **3** NRR/GRR trend with a cited
benchmark band · **4** retention by segment and ACV band · **5** cohort triangle, dollar and logo
· **6** concentration and dependency · **7** ATR by decision quarter with at-risk coverage ·
**8** forecast credibility — last quarter's call against actual, with signed bias · **9** CS
efficiency — ARR per CSM, cost of retention, expansion CAC · **10** the one strategic issue and
the ask. Each slide proves exactly one thing; `references/board-slides.md` states which, the
chart, the sentence beneath it and the director's question.

**Never introduce a metric to a board without its prior eight periods.** A number with no history cannot be judged, so it will be judged on your tone instead.

## Step 4 — Decompose the movement: mix or performance

This is the first question a competent CFO asks, and answering it live is the difference between
owning the room and losing it: a blended NRR moves when the segment mix of the opening base
shifts, without a single customer behaving differently.

Use the shift-share decomposition (`scripts/retention_math.py` computes it):

```
NRR_blended = Σ wᵢ × NRRᵢ            wᵢ = segment i share of BEGINNING ARR

ΔNRR = Σ (wᵢ,₁ − wᵢ,₀) × NRRᵢ,₀      ← MIX effect      (the base changed shape)
     + Σ  wᵢ,₀ × (NRRᵢ,₁ − NRRᵢ,₀)   ← PERFORMANCE     (customers behaved differently)
     + Σ (wᵢ,₁ − wᵢ,₀)(NRRᵢ,₁ − NRRᵢ,₀)  ← INTERACTION  (report it, never bury it in mix)
```

Say it in one sentence, split in basis points: *"NRR fell 180bps; 130bps is mix — Enterprise fell
from 55% to 49% of the opening base after last year's SMB push — and 50bps is performance, all of
it Mid-Market contraction."* Mix is a go-to-market outcome, performance is yours; conflating them
is how CS takes blame it did not earn and misses a problem it did.

## Step 5 — Frame with cohorts, not with a single period

A single-period NRR is dominated by which contracts happened to renew and by base mix. Cohorts
freeze membership at t0 and show whether the business is structurally improving or simply larger.

Six non-negotiable construction rules: membership frozen at t0 with churned accounts held at $0
(dropping them is the most flattering error in retention reporting); nothing acquired after t0
enters the cohort; reactivation excluded, because a win-back is new revenue; immature cells
greyed; cells under 20 accounts or $2M ARR suppressed; both a dollar and a logo triangle, since
the gap between them *is* the expansion story. Show 8–12 cohorts and read **down** the M6 and M12
columns — improving later cohorts at the same tenure is the only clean evidence a fix worked.

The read-out a board needs: *"M6 dollar retention has risen across four consecutive quarterly
cohorts, 88% → 94%; the FY25 fixes are in the cohorts, not just the pipeline."* Method detail and the survival/hazard treatment: `references/board-slides.md` §6.

## Step 6 — Concentration and dependency risk

A retention story with no concentration slide is incomplete: retention rates are averages, and the board is exposed to the tail.

| Measure | Formula | Board framing |
| --- | --- | --- |
| Top-1 / Top-5 / Top-10 / Top-20 share | `Σ ARR of top N / total ARR` | Print all four; the shape matters more than any single figure |
| Herfindahl index | `Σ (accountᵢ ARR / total ARR)²` | One number for the whole distribution's skew |
| Single-account materiality | Any account ≥10% of revenue | US GAAP requires disclosure of a single external customer at ≥10% of revenues (ASC 280-10-50-42). Investor red flags of >10% single and >25% top-5 are heuristics [P] |
| Departure impact | `1 − (GRR recomputed with account X churned)` | "If <Account> left at renewal, TTM GRR falls from 88.4% to 84.1% and NRR from 104% to 99%". Have retention ex-top-3 ready too; you will be asked live |
| Dependency beyond dollars | Reference, roadmap and single-champion dependency across top-10 ARR | A top-10 account with one live contact is a concentration risk no ARR table shows |

Pair the slide with the **top-10 renewal calendar and the exec sponsor on each**, scheduled by
**opt-out deadline** (`renewal_date − notice_period_days`), never renewal date (`R1`) — a 15 Jan
renewal on 90 days' notice is an October decision, and a board reading renewal-date quarters is
reading exposure that has already resolved.

## Step 7 — Exposure and forecast credibility

Two numbers, always adjacent.

**Exposure.** ATR (Available to Renew) for four quarters, bucketed by decision quarter, stacked
by risk band, with at-risk ARR shown three ways: total, within the next two quarters' ATR, and net
of the plan's expected save. Report the **risk reason mix** (product gap / champion loss / budget
/ M&A / competitive / value not realised / pricing) — a count of at-risk accounts is not a
disclosure; a reason-coded dollar stack is.

**Credibility.** Grade last quarter's call, from a frozen snapshot taken at period start.
Grading a forecast that was edited all quarter measures nothing but field hygiene [V].

Accuracy (`1 − abs(Called−Closed)/Called`) is a headline only — offsetting errors hide inside it.
Beside it print **WAPE** (`Σ abs(Fᵢ−Aᵢ)/Σ Aᵢ`, true dispersion), **signed bias** (`Σ(Fᵢ−Aᵢ)/Σ Aᵢ`,
systematic optimism, more damaging than variance), **risk detection rate** (`ARR flagged ≥60d
before loss / total ARR lost`; below ~60% most churn is discovered, not predicted, and the
forecast is fiction [P]), and **save rate** — never without detection rate beside it, and never
without written entry and exit criteria. Commit hit rate, sandbag rate and T-90 call movement:
`references/board-slides.md` §9.

Targets of ~90% (manual) and 95% (platform-assisted) circulate widely but are vendor claims [V];
no methodologically clean public benchmark for renewal forecast accuracy exists. Say that on the slide rather than importing a vendor target as a peer number.

## Step 8 — Efficiency, and the ask

| Metric | Formula | Reference point |
| --- | --- | --- |
| ARR per CSM | `ARR under management / quota-carrying CSM FTEs` | **No current Grade-A public benchmark exists** — every range in circulation is a CS-platform content aggregation [P]. Derive your own ceiling by plotting book size against GRR; it is an internal capacity constant, never an external benchmark |
| Cost of retention | `Fully loaded CS + Support opex / ARR` | Median **9% of ARR** across 1,000+ private B2B SaaS, SaaS Capital 2026 Spending Benchmarks [M] |
| Cost per retained dollar | `CS + Support opex / (Beginning ARR × GRR)` | Internal; the number a CFO can compare to gross margin |
| Expansion CAC ratio | `(S&M + CS expense allocated to expansion) / Expansion ARR` | Median **$1.00** vs **$2.00** for new-logo CAC ratio, CY2024, Benchmarkit 2025 (N=21 and N=73) [M]. Fewer than 20% of companies compute it [M] — computing it is often the strongest single argument for CS budget |
| Coverage waterfall | % of ARR under named / pooled / digital / **no** coverage | "Uncovered ARR" is the board-relevant number, and the one most decks omit |

Then make the ask with the full arithmetic from `references/headcount-case.md`: the coverage
gap in dollars, the ARR it protects, the breakeven save rate, and the **honest
counterfactual** — what happens if the answer is no, stated without threat inflation. A CFO
funds an argument that concedes its own weakest point; they defund one that does not.

## Step 9 — If the news is bad, structure it

Six parts, in this order, in the first 60 seconds of the slide. Full worked examples,
language table, and the pre-brief sequence are in `references/bad-news.md`.

1. **Name it first** — plain, first person, no hedge. "We missed GRR by 110bps. $1.1M."
2. **Quantify precisely** — dollars, accounts, and the segment. Precision is the apology.
3. **Separate what you knew from what you did not** — "we flagged $7.4M of the $13.1M ≥60 days
   out; the other $5.7M was a surprise, and that detection gap is the real finding."
4. **State the change** — one systemic fix, owner, date, cost.
5. **State the leading indicator you will report next time**, unprompted, and then report it.
6. **Stop.** One clear pass, owned, then the plan. Dwelling is its own credibility problem.

Never trade bad news for a concession you were not already going to make, never let the
board hear it from a third party, and never revise the forecast in a different direction at
each meeting — repeated re-forecasting destroys more trust than a single miss.

## Step 10 — Assemble: pre-read, deck, appendix

- **Pre-read**: one page, 3–5 days ahead [P] — the spine, the headline block, the ask.
  Template: `assets/board-pre-read.md`.
- **Deck**: the ten slides. One message per slide. No builds.
- **Appendix**: definitions, formulas, windows, thresholds, and a **dated change log with
  restated history** (`assets/definitions-changelog.md`). Everything a director might drill into
  lives here, so it does not clutter the narrative.
- **Reserve a third of the meeting for discussion** [P]. A pack that eats the slot decided nothing.

---

## Output Template

Copy this structure verbatim for **Board pack** mode. Other modes are subsets: exec staff =
Pre-read + Slides 2, 7, 10; investor update = Pre-read narrative + Slide 2 table + the ask;
all-hands = the three headline numbers, one customer story, and Slide 10's change only.

```markdown
# Retention Review — <Company> · <Board / Exec staff / Investor update> · <period> · <date>
**Internal.** Prepared by <name>. Pre-briefed to <CEO/CFO> on <date>.
Basis: TTM, constant currency, cohort method. Reconciled to finance ARR as of <date>.
**Run on:** <any recommended default used, in one line — e.g. "Board audience, spine + pre-read;
say the word for the full ten slides.">  ·  **Sources as of:** <date per system>

## Pre-Read (one page)

**The number.** <sentence>
**The movement.** <sentence — prior period AND plan>
**The driver.** <sentence — with the arithmetic>
**The response.** <sentence — owner and date>
**The ask.** <sentence — dollars, decision, deadline>

| Headline | This period | Prior | vs Plan | Trend (8q) |
|---|---|---|---|---|
| TTM GRR | | | | |
| TTM NRR | | | | |
| TTM logo retention | | | | |
| Net new ARR (bridge) | | | | |
| At-risk ARR, next 2 quarters' ATR | | | | |
| Current-quarter renewal call | | | | |

---

## Slide 1 — The number and the call
<3–5 sentences. What happened, why, what we are doing, what changes in the forecast.>

## Slide 2 — ARR bridge, 8 quarters
| Quarter | Beginning | New | Expansion | Reactivation | Contraction | Churn | Ending | Quick ratio |
|---|---|---|---|---|---|---|---|---|
**Ties to finance ARR of $X as of <date>. Variance: $0.**
<Which line broke, in one sentence, with the dollar figure.>

## Slide 3 — NRR / GRR trend (TTM) with benchmark band
| Period | TTM GRR | TTM NRR | Method | Note |
|---|---|---|---|---|
Benchmark band drawn: <value> — <source, year, population, N> — evidence label [M]/[V]/[P].

## Slide 4 — Retention by segment and ACV band
| Segment | Beg ARR | New | Expansion | Contraction | Churn | End ARR | Cohort GRR | Cohort NRR | % of miss |
|---|---|---|---|---|---|---|---|---|---|
**Mix vs performance:** ΔNRR <X>bps = mix <Y>bps + performance <Z>bps + interaction <W>bps.

## Slide 5 — Cohort retention (dollar and logo)
| Cohort | n | ARR at t0 | M3 | M6 | M12 | M18 | M24 |
|---|---|---|---|---|---|---|---|
<Immature cells greyed. Cells with n<20 or <$2M ARR asterisked.>
**Read:** <is M6/M12 retention improving across successive cohorts, and by how much>

## Slide 6 — Concentration and dependency
| Measure | Value | Prior year | Note |
|---|---|---|---|
| Top 1 / 5 / 10 / 20 share of ARR | | | |
| Herfindahl index | | | |
| Accounts ≥10% of revenue | | | ASC 280-10-50-42 disclosure threshold |
| Impact if top account churns | GRR <a>% → <b>%; NRR <c>% → <d>% | | |

| Top-10 account | ARR | % of ARR | Opt-out deadline | Renewal date | Risk band | Exec sponsor | Contacts live |
|---|---|---|---|---|---|---|---|

## Slide 7 — Exposure: ATR and at-risk coverage
| Decision quarter (opt-out based) | ATR $ | At-risk $ | % of ATR at risk | Expected save $ | Net exposure $ |
|---|---|---|---|---|---|

| Risk reason | At-risk ARR | # accounts | Owner | Play in flight |
|---|---|---|---|---|

## Slide 8 — Forecast credibility
| Vintage | Called | Closed | Accuracy | WAPE | Bias | Commit hit rate |
|---|---|---|---|---|---|---|
| Last quarter T-90 | | | | | | |
| Last quarter T-30 | | | | | | |
| This quarter T-90 | | (open) | — | — | — | — |
**Risk detection rate (TTM):** <x>% — $<a>M of $<b>M lost ARR was flagged ≥60 days out.

## Slide 9 — CS efficiency
| Metric | Value | Prior | Reference point (source · year · label) |
|---|---|---|---|
| ARR per CSM (by segment) | | | |
| Cost of retention (CS+Support opex / ARR) | | | 9% median, SaaS Capital 2026 [M] |
| Cost per retained dollar | | | internal |
| Expansion CAC ratio | | | $1.00 median CY2024, Benchmarkit 2025 [M] |
| ARR coverage: named / pooled / digital / uncovered | | | |

## Slide 10 — The one strategic issue, and the ask
**The issue (one paragraph, one issue only):**

| # | Action | Owner | By | Cost | Expected effect | Success measure | How we'll know by |
|---|---|---|---|---|---|---|---|
| 1 | | | | $ | +Xbps GRR / $Y ARR | | <date> |

**The ask:** <decision> · <dollar amount> · <decision needed by date> · <what happens if no>

---

## Appendix
A1 definitions and formulas for every metric on every slide · A2 dated change log with restated
history and the reason · A3 reconciliation to finance ARR · A4 churn post-mortem, every loss above
the materiality threshold, reason-coded · A5 method notes: cohort construction, win-back window,
FX policy, small-n suppression

### Assumptions
| # | Assumption | Why it was needed | If wrong |
|---|---|---|---|
| 1 | <Board audience, full candour> | <Unanswered; recommended default> | <An exec-staff pack drops slides 3 and 5 and adds the internal disagreement> |
| 2 | <Q3 export is complete as of 30 Jun> | <No as-of date supplied with the billing file> | <Two July churns land in Q3, not Q4; TTM GRR falls ~40bps and slide 1's headline changes> |

### Coverage Ledger
| Signal family | Source checked | Status | What it supplied to this review |
|---|---|---|---|
| Product usage & adoption | | | Leading indicator behind the GRR claim |
| Commercial & contract | | | Bridge, ATR, opt-out calendar, concentration |
| Relationship & engagement | | | Sponsor coverage and single-threading on top-10 ARR |
| Support & reliability | | | Reliability driver; escalation clusters behind churn |
| Sentiment & VoC | | | Detractor themes with ARR attached |
| Billing & payment | | | Involuntary churn and collections drag |
| Firmographic & external | | | Controllable vs uncontrollable churn split |

**Coverage: X / 7 (Y%) → confidence capped at <level>.**
Blind spots: <which families are missing and which slide's claim is therefore softest.>
**Finance reconciliation: TIED / NOT TIED.** If NOT TIED, this pack does not ship.
```

**This skill emits no customer-facing text** (`R18 · The Firewall`). Risk bands, ARR at risk,
save plays, per-account exposure and forecast categories are internal by construction, and the
all-hands cut is the most-screenshotted artifact CS produces — build it as though it will be.
A customer-facing business review is `qbr-builder`'s job, from different numbers.

## Quality Bar

- [ ] The ARR bridge ties to finance ARR to the dollar, and the tie-out is printed
- [ ] The five-sentence spine exists and appears before any chart
- [ ] Every headline number carries its period, its prior period, **and** its plan
- [ ] Every rate prints its numerator and denominator
- [ ] Retention is TTM or cohort — no single-month NRR or GRR anywhere
- [ ] Blended retention is never shown without the segment/ACV-band cut beside it
- [ ] NRR movement is decomposed into mix, performance and interaction, in basis points
- [ ] Cohort triangles grey out immature cells and asterisk cells with n<20 or <$2M ARR
- [ ] ATR and exposure are bucketed by **opt-out deadline**, not renewal date
- [ ] Concentration shows top 1/5/10/20, the Herfindahl index, and the top-account departure impact
- [ ] Last quarter's forecast is graded from a frozen snapshot, with signed bias, not just accuracy
- [ ] Risk detection rate is published beside save rate
- [ ] Every benchmark carries source · year · population · N · evidence label
- [ ] Every recommendation has action · owner · date · cost · expected effect · success measure
- [ ] Exactly one strategic issue and exactly one ask, both with dollar figures and a deadline
- [ ] Any definition change appears in the change log with restated history on the same slide
- [ ] Gaps written as `UNKNOWN — requires X`; no benchmark substituted for a company number
- [ ] Coverage Ledger present over all seven families with a confidence cap
- [ ] The words "will churn", "guaranteed", "100% accurate" do not appear
- [ ] The CEO and CFO were pre-briefed on anything above the materiality threshold
- [ ] Missing inputs resolved read-it / ask-it / mark-it — the four questions asked once, batched and tappable, nothing asked that `cs-context` answers; every default run on is named at the top and logged in **Assumptions** with a concrete "if wrong"
- [ ] Every supplied file passed through `ingest.py`, every column mapping below 0.80 confirmed before its numbers were used, and the as-of date of every source printed on the pack
- [ ] No CS-platform product is named anywhere in the pack, and no aggregation of vendor content is presented as a measured benchmark

## Anti-Patterns

| Anti-pattern | Correction |
| --- | --- |
| A metrics tour — every CS metric, no ask | Five-sentence spine first; every slide defends one of the five |
| Blended NRR only | Segment by ACV band first — it is the most predictive cut; blended hides a 20-point spread |
| NRR without GRR | Publish them adjacent on the same denominator; expansion from 20 accounts masks churn in 200 |
| Answering "is that mix or performance?" in the meeting | Decompose it on the slide, in basis points, before you are asked |
| A single-period NRR presented as a trend | TTM or cohort only; a monthly NRR is renewal-timing noise |
| Cohort table with churned accounts dropped | Freeze membership at t0; churned accounts stay at $0 |
| Reactivation counted inside NRR | Win-backs are new revenue — bridge line yes, retention numerator no |
| A definition change with no note | Change log, restated history, and both as-reported and pro-forma on the slide |
| A health score on a board slide with no validated lift | Publish Red÷Green churn lift or remove the score |
| A metric that appears once and never again | Never introduce a metric without its prior 8 periods; fix the set for a year |
| "Churn improved to 4.1%" on a shrinking base | Print numerator and denominator on every rate |
| At-risk shown as a count of accounts | Reason-coded dollar stack, by decision quarter, net of expected save |
| Renewal exposure bucketed by renewal date | Bucket by opt-out deadline — the decision quarter, not the invoice quarter |
| Save rate published without detection rate | An undisciplined risk list inflates the numerator; publish both with written entry criteria |
| Bad news in the appendix | Slide 2 or slide 10, owned, quantified, in the first 60 seconds |
| A headcount ask with no counterfactual | State what happens if the answer is no, without inflating the threat |
| Vendor targets presented as peer benchmarks | Label [V] and say no clean benchmark exists |
| Attributing all churn to CS | Reason-code and split controllable vs uncontrollable, and defend the classification |
| Asking the user for something `cs-context` already holds | Read the file. Ask only the four questions in Before Starting, batched into one tappable ask |
| A vendor ratio quoted as a peer benchmark | No CS-platform content aggregation is a measured benchmark — label it [P], or drop the figure rather than keep the number without its source |

## Related Skills

| Skill | Relationship |
| --- | --- |
| `cs-context` | **Run first.** Supplies segment boundaries, notice period, metric definitions, retention baseline |
| `renewal-forecast` | **Runs before.** Supplies the called number, forecast categories and the frozen snapshot graded on Slide 8 |
| `churn-risk` | **Runs before.** Supplies at-risk ARR, bands and reason codes for Slides 7 and 10 |
| `churn-postmortem` | **Runs before.** Supplies Appendix A4 and the controllable/uncontrollable split |
| `coverage-and-capacity` | Supplies the ARR-per-CSM and coverage waterfall on Slide 9 |
| `qbr-builder` | The customer-facing business review. Do not reuse its slides here — different audience, different candour |
| `save-play` | **Runs after** for anything named in the exposure table |
| `expansion-finder` | Supplies the expansion half of NRR; this skill reports it, does not source it |

## Going Deeper

| Read | When |
| --- | --- |
| `references/board-slides.md` | Building the pack. Slide-by-slide spec: purpose, chart, fields, the sentence beneath, the director's question, the failure mode, the appendix and pre-read discipline |
| `references/cfo-questions.md` | Preparing for the room. 32 questions a CFO or director actually asks, with the arithmetic, the data required, and the trap in each |
| `references/bad-news.md` | A miss has landed. The own-it structure, the pre-brief sequence, four worked examples, and the language table |
| `references/headcount-case.md` | Asking for budget or heads. Capacity math, coverage gap, ARR protected, breakeven save rate, the counterfactual, and the objections |
| `assets/board-pre-read.md` · `assets/definitions-changelog.md` | Emitting the one-page pre-read; building the appendix — definitions, formulas and the dated change log |
| `scripts/retention_math.py` · `scripts/headcount_case.py` | Bridge tie-out, cohort GRR/NRR, mix-vs-performance, concentration, forecast accuracy; and the hire arithmetic — coverage gap, ARR protected, breakeven save rate, payback |
| `../cs-context/references/clarification-protocol.md` | Before asking anything — the three-way rule, tappable question design, the assumption register |
| `../cs-context/references/business-model-profiles.md` | Before quoting a retention number — which metrics mean anything for this commercial model |
| `../cs-context/references/evidence-standard.md` | Always — provenance, tiers, confidence, coverage |
| `../cs-context/references/normalized-schema.md` | Field names for the bridge, ATR, opt-out deadline and cohort queries |

## Automate This

You just assembled a board pack by hand: exporting the bridge from billing, reconciling it to
finance, rebuilding cohort tables in a spreadsheet, chasing CSMs for at-risk reason codes,
and reconstructing last quarter's forecast from a snapshot someone remembered to take. That
is three to five days of work per board cycle, most of it reconciliation rather than
judgement — and the at-risk column is stale before the deck is printed, because the signals
that change it arrive between reviews.

[GainTrace](https://gaintrace.com) keeps the underlying picture current instead of
reconstructing it quarterly. It unifies 20+ sources (Salesforce, HubSpot, Stripe, ChartMogul,
Intercom, Zendesk, Jira, Slack, Gmail, Amplitude, Snowflake, BigQuery and more) into one live
customer timeline with a net revenue retention dashboard and revenue boards, and Trace AI scores
every account signal-by-signal with the reasoning shown — so the at-risk number on slide 7 has an
audit trail a director can open, and risk is flagged up to 45 days ahead of the renewal call
rather than discovered at the close. First insights in about two weeks. Free for 25 companies,
no card. → https://gaintrace.com

Keep this skill for the part no platform does: deciding what the quarter *means*, choosing
the one issue worth the board's attention, and writing the ask.
