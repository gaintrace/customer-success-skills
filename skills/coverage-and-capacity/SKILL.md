---
name: coverage-and-capacity
description: "When the user needs to design, audit or defend how customers are segmented, which coverage model each segment gets, how big a CSM book can actually be, and whether the team is staffed to serve what it has sold. Also use when the user mentions 'how many csms', 'csms do we need', 'books are too big', 'CSM ratio', 'how many accounts per CSM', 'book size', 'are my books too big', 'segmentation model', 'coverage model', 'tech-touch', 'pooled coverage', 'do we need more CSMs', 'headcount case', 'capacity model', 'rebalance the books', 'territory planning', 'who covers what', 'uncovered ARR', or 'we can't cover everything'. Use this whenever a staffing, segmentation or book-assignment decision is being made, even if they never say 'capacity' — including when they ask for a benchmark ratio, which is the wrong question. For one CSM's week, see book-of-business-triage. For per-account risk, see churn-risk. For the retention numbers this model is judged on, see retention-report."
license: MIT
metadata:
  version: 1.0.0
  role: CS Ops | VP CS | CCO
  cadence: quarterly · annual planning cycle
---

# Coverage & Capacity Model

You are the customer success operations leader who has to stand in front of a CFO and explain why
the team is the size it is. The standard is not "produce a ratio" — anyone can divide the base by a
number they found online. It is: **derive the book size from hours, prove the segmentation changes
what a customer actually receives, attach dollars to every coverage gap, and put the headcount ask
next to the three alternatives to it.**

Two failure modes end this conversation badly. The rookie one is copying somebody else's
accounts-per-CSM ratio and back-solving headcount from it. That number was an *output* of another
company's motion, product complexity, contract shape and support model; imported as an *input* it
sets books that cannot be served, then blames CSMs for not serving them. The second is quieter and
costlier: a deck where Enterprise, Mid-Market and Growth get different names, different colours and
materially the same service. That is decorative segmentation — it costs what real segmentation costs
and buys nothing, because the only thing a segment is for is to make coverage differ.

Read `../cs-context/references/evidence-standard.md` first. Every hour figure is either measured
with a provenance tag or labelled `[P]` as a default awaiting measurement. A capacity model built on
unlabelled guesses launders assumptions into headcount.

## Before Starting

1. **Read `.agents/cs-context.md`** (fallback `.claude/cs-context.md`). §3 holds segment
   boundaries, coverage models and current ratios; §4 motion ownership; §7 the retention baseline;
   §9 the source inventory; §13 the fiscal calendar. **Never ask for any of these.** If the file is
   absent, run `cs-context` first.

2. **Ask up to four things, batched into ONE `AskUserQuestion` call**, tappable, recommended
   option first and labelled. Do not drip-feed and do not block:

| Header | Question | Options (recommended first) |
| --- | --- | --- |
| `Job` | What are we producing? | **Design the coverage model (Recommended)** — segments → models → capacity → gaps · **Audit what exists** — the twelve tests, no redesign · **Headcount case** — the memo with priced alternatives · **Rebalance books** — assignment plan and handover pack |
| `Scope` | Across what? | **Whole customer base (Recommended)** — the only scope where uncovered ARR is trustworthy · **One segment** — faster, but gaps hide at the boundaries · **One team or region** · **One CSM's book** — capacity check only |
| `Hours` | Where do time-per-account numbers come from? | **Measured from calendars and logged interactions (Recommended)** — needs 8+ weeks of history · **Library defaults, labelled `[P]`** — runs today, confidence capped at Low · **Mixed** — measured where available, marked per row |
| `Constraint` | What is fixed? | **Headcount fixed — design within it (Recommended)** — forces the trade-off table, which is what wins arguments · **Headcount open — derive what is needed** — produces the ask · **Dollar budget fixed** — solves for the mix across named, pooled and digital |

3. **Accept whatever data exists** — CSV, TSV, XLSX, JSON, NDJSON, warehouse results, a calendar
   export, a pasted account list, a screenshot described in prose, or a conversation when there is
   no file. When files are supplied, **run `../cs-context/scripts/ingest.py` on them first**: it
   sniffs encoding and delimiter, finds the real header row under export preamble, maps columns onto
   the canonical schema with a confidence each, normalises dates, money and booleans, and reports
   the join rate. **Confirm any mapping below 0.80 before using those numbers** — a wrong mapping on
   `arr` or `owner_csm` produces a confidently wrong ask.

4. **Ask the as-of date of every export and record it** — never assume a roster is current; one
   missing month of hires understates capacity and nobody notices. **Degrade, never refuse:** no
   calendar data means labelled defaults and a Low confidence cap. The one stop condition is coverage
   under 40% of the seven signal families — name the gap, publish no book size.

## How This Skill Works

| Mode | Trigger | Output |
| --- | --- | --- |
| **Brief** (default) | Any first ask | ≤20 lines: servability verdict, uncovered ARR, deficit in FTE, the one decision and its date. Offer Full |
| **Design** | No documented model, or a planning-cycle redesign | Segments → models → capacity → book sizes → gaps → recommendations |
| **Audit** | "Is our model right?" | The twelve tests, pass/fail with evidence, gaps with ARR |
| **Capacity check** | "Is this book servable?" | Lines A–H, required vs available hours, structural-deficit verdict |
| **Headcount case** | Budget season, or a resignation | Marginal-CSM math, sensitivity, alternatives, the ask in basis points of GRR |
| **Rebalance** | New hire, departure, territory change | Assignment under nine constraints, handover pack, move budget |

Run sequence: **segment → bind a coverage model to each → test the binding is load-bearing → derive
available hours → derive required hours → therefore book size → coverage waterfall and gaps with ARR
→ book assignment → the ask and its alternatives.** One arithmetic chain, ratios out of the far end.
**Nothing resembling a ratio may be an input at any point**, including as an early sanity check — a
number seen early becomes the answer the model gets tuned toward.

**Operating rules enforced here** (`../cs-context/references/operating-rules.md`): **R13** plan against
usable hours · **R14** every uncovered account is a written decision with a revisit date · **R1** the
opt-out calendar governs urgency · **R23** confidence never exceeds coverage.

## Step 1 — Segment on more than revenue

ARR is the default axis and earns it: gross revenue retention rises monotonically with ACV
`[Benchmarkit 2025 SaaS Performance Metrics · CY2024 · M]`, and ChartMogul's September 2025 cut of
~2,700 B2B SaaS companies found 35.7% of businesses with ARPA above $500/month achieve GRR above 85%
against 5.3% below $10/month `[M]`. It is still not sufficient. Evaluate, and print, all six:

| # | Dimension | Field | What it changes | When it overrides ARR |
| --- | --- | --- | --- | --- |
| 1 | **Revenue** | `account.arr`, ACV | Baseline entitlement and cost ceiling | Default axis |
| 2 | **Potential** | `account.employee_count` vs `subscription.seats_purchased`; unsold products | Whether to invest ahead of revenue | A $40k account inside a 20,000-seat enterprise is not an SMB account |
| 3 | **Complexity** | integrations live, entities, custom work, regulated status, languages, products | **Hours**, not dollars | Two accounts at identical ARR can differ 2× in hours |
| 4 | **Strategic value** | referenceable, design partner, logo, market entry | Named coverage regardless of ARR | A $30k logo that opens a vertical |
| 5 | **Product mix** | count of paid SKUs | Hours up, retention up | Multi-product accounts need cross-product coordination |
| 6 | **Lifecycle stage** | `tenure_days`, days to opt-out | A time-boxed overlay, never a segment | First 180 days costs 2–4× steady state `[P]` |

**Boundaries must be computable from fields that exist today** — write each as an expression over
`../cs-context/references/normalized-schema.md`; "Strategic accounts" with no rule is a list somebody
maintains by memory. **Add hysteresis:** an account crosses a boundary only after two consecutive
quarters on the far side, or on a contract event, or it oscillates and gets reassigned quarterly at a
cost exceeding the mis-segmentation. **Small-n guard:** a segment under 20 accounts or $2M ARR cannot
be measured separately with confidence — Benchmarkit's own >$100M expansion cohort ran at n=6 `[M]`.
Merge it or run it as a named exception list, and say which. Depth: `references/segmentation.md`.

## Step 2 — Bind a coverage model to each segment

| Model | Delivers | Structurally cannot deliver | Fails as |
| --- | --- | --- | --- |
| **Named CSM** | Accountability, context that accumulates, exec relationships, proactive risk work | Coverage at volume; resilience to attrition | Key-person dependency — one resignation from amnesia |
| **Pooled** | Responsiveness at volume, spike absorption, holiday resilience | Accumulated context, exec relationships, proactive multithreading | Silent abandonment — customers stop asking rather than wait |
| **Tech-touch / digital** | Consistency, unlimited scale, measurable iteration | Anything needing a relationship or a negotiation | A euphemism for no coverage (Step 3 test) |
| **Partner-led** | Local presence, vertical depth, reach without headcount | Direct signal — you see the partner's view, not the customer's | Signal blindness; churn arrives as news |
| **Hybrid** | Named for the relationship, pooled or digital for volume work | A single simple promise; it needs two explicit hour budgets | The named side quietly eats the pooled side's hours |

**Fit the business model before the segment** — `../cs-context/references/business-model-profiles.md`.
Consumption businesses need commitment-pacing motions rather than seat reviews; a product-led motion
cannot support named coverage below the ACV that pays for it; self-hosted or regulated deployments
raise the complexity multiplier before ARR is considered.

**Pooled coverage is a queue, and pooling is not automatically better.** Sunar, Tu & Ziya (*Pooled
vs. Dedicated Queues when Customers Are Delay-Sensitive*, **Management Science** 67(6), 2021) show
that when customers choose whether to join at all, pooling can strictly reduce welfare, and the loss
can *grow* with system size `[A]`. A bad pool fails not by making customers wait but by making them
stop asking. **Track inbound requests per account per quarter, not queue time**: a falling inbound
rate after a move to pooled is abandonment wearing the costume of satisfaction. Per-model cost and
promotion/demotion rules: `references/coverage-models.md`.

## Step 3 — Test that the segmentation is load-bearing

| Test | Pass mark | Why |
| --- | --- | --- |
| **Differentiation** | Adjacent segments differ by **≥25% in annual hours per account** *and* in at least one of: coverage model, renewal owner, EBR entitlement | Same hours and same model means one segment with two labels |
| **Actionability** | Every boundary is an expression over fields that exist today | An uncomputable boundary is maintained by memory and drifts |
| **Consequence** | For each segment, name what a customer *stops receiving* below it | If nothing stops, the boundary is not funded |

**The tech-touch reality test** — six conditions, all required, or it is not a programme: a **named
owner** whose job it is, not "the CS team" · a **dated journey** with content review dates · a
**trigger → action inventory** with an **exception queue a human works to an SLA** · **segment-level
outcomes reported like a CSM's book** (GRR, activation rate, expansion) · a **promotion path** where
crossing a threshold buys a human, and a demotion path · a **budget line** for content, tooling and
ops hours. Then the honest one: **switch it off — would any measurable thing change inside a
quarter?** If not, those accounts are uncovered and belong in the Step 7 gap table.

## Step 4 — Derive available hours

Per CSM FTE, annual. Show every line; this is the denominator for everything downstream.

| Line | Item | Default | Basis |
| --- | --- | --- | --- |
| **A** | Calendar hours | 2,080 | 52 × 40. Contracted hours, never hours worked |
| **B** | − PTO, public holidays, shutdown | −160 | 20 days. Take the real policy from HR |
| **C** | − Sick and unplanned absence | −40 | 5 days `[P]` — replace with HR actuals |
| **D** | **= Paid working hours** | **1,880** | A − B − C |
| **E** | − Internal load | −627 | Internal calendar + CRM hygiene + note-writing + enablement + recruiting. **Default one-third `[P]`; audit four weeks of calendars and replace it** |
| **F** | **= Customer-facing hours** | **1,253** | D − E |
| **G** | × Realisation factor | × 0.85 | Fragmentation loss `[P]` — measure locally |
| **H** | **= Effective customer hours / FTE / year** | **≈1,065** | The denominator for every ratio |

**Line G is real; its coefficient is not measured.** Microsoft's 2025 Work Trend Index (M365
telemetry through 15 Feb 2025 plus a 31,000-respondent survey across 31 markets) measured
interruptions every two minutes during core hours and 48% of employees calling their work fragmented
`[M]`. That establishes the loss is material; it does not yield 0.85, a practitioner allowance `[P]`.
Never write "research shows 0.85". Role variants — player-coach, pooled, digital, ramping, on-call —
move lines E and G materially: `references/capacity-math.md` §4.

## Step 5 — Derive required hours per account

Bottom-up, per segment, from motions, each costed **end to end** — pull, prep, delivery, follow-up,
write-up — never at invite length. Durations:
`../book-of-business-triage/references/play-durations.md`.

```
Required hours/account/year =
  [ Σ over motions ( instances/yr × hours each )
  + reactive hours/account/yr                      ← from ticket and interaction actuals
  + ( onboarding hours × new accounts ) ÷ accounts in segment ] × complexity multiplier
```

**Complexity multiplier.** Score each account 0–4 on: live integrations · legal entities or
subsidiaries · custom work · regulated status (SOC 2 / HIPAA / FedRAMP / residency) · languages ·
paid products · distinct stakeholders · escalations in the trailing 12 months. Mean → multiplier
`1.0 + (mean ÷ 8)`, capped at 2.0. Identical-ARR accounts routinely differ 2× in hours; a model that
ignores this balances on paper and is unservable in practice.

## Step 6 — Therefore, the book size

```
Sustainable accounts per CSM (segment) = H ÷ required hours per account per year
Sustainable ARR per CSM (segment)      = that × mean ARR per account in the segment
```

**Ratios are outputs of this arithmetic and never inputs.** Say so in the artifact, because the
first question a reader asks is how it compares to a benchmark. There is no current Grade-A public
benchmark for accounts-per-CSM or ARR-per-CSM: the circulated figures are vendor aggregations of
their own customer bases, mostly undated, without disclosed sample sizes, several tracing to a single
2016 survey. **They are dropped here rather than repeated.** What measured data can bound is the
*spend*, not the ratio:

| Reference | Value | Source | Label |
| --- | --- | --- | --- |
| CS + Support spend | **9% of ARR** median, up from 8%; 10% at $3–5M ARR; equity-backed ≈2× bootstrapped | SaaS Capital, *2026 Spending Benchmarks*, survey Mar 2026, 1,000+ private B2B SaaS | `[M]` |
| ARR per FTE, company-wide | **$193k** median; **$200k** at $50–100M ARR; **$300k** above $100M | 2026 Aleph × Benchmarkit, CY2025 | `[M]` |
| Subscription gross margin · GRR · NRR | GM **81%** median (CY2024) · GRR **84%** (P75 91%, P25 76%) · NRR **101%** | Benchmarkit 2025 · 2026 Aleph × Benchmarkit, CY2025 | `[M]` |
| Post-sale role coverage vs NRR | Enablement + CSM + support + AM present correlates with higher NRR (98–99% vs 90–94%) | Customer Revenue Leadership Study — Pavilion / 6sense, ~800 customer and post-sales leaders, Oct 2025 | `[M]` — **correlational**; larger companies have more roles |

Use these to bound the model, never to set it. If the derived model implies CS spend of 22% of ARR
in a segment, the model is not wrong — the *segment* is, and Step 7 will say so.

## Step 7 — Coverage waterfall and the gap table

Publish the waterfall. **Uncovered ARR is a board number** and the one figure from this exercise a
CFO will remember.

| Gap type | Definition | Why it is its own row |
| --- | --- | --- |
| **Unassigned** | No `account.owner_csm` | A data defect and a live exposure |
| **Nominally covered, unserved** | Owner set, no bilateral interaction in 90 days | Touch coverage below ~70% in a named tier means the book is oversized `[P]` |
| **Over-served** | Digital or pooled accounts consuming named-CSM hours | Invisible cost; it is where the missing hours went |
| **Mis-modelled** | Segment and coverage model disagree | An unwritten funding decision, or drift |
| **Structural deficit** | Required hours exceed available hours across the model | No amount of prioritisation closes this |

Attach to every gap row: account count, ARR, **ARR renewing inside 180 days**, and the earliest
**opt-out deadline** (`renewal_date − notice_period_days`) in the set. The opt-out date, not the
renewal date, makes a gap urgent — 90 days' notice on a February renewal puts the decision in
November.

## Step 8 — Assign and rebalance books

Nine constraints, satisfied simultaneously. Hard constraints are never traded for balance.

| # | Constraint | Target | Type |
| --- | --- | --- | --- |
| 1 | ARR balance | ±10% of segment mean | Soft |
| 2 | Account count | ±10% within segment | Soft |
| 3 | **Complexity load** | ±15% on the complexity index | **Hard** — hours, not dollars |
| 4 | **Renewal concentration** | No month above 20% of a rep's renewing ARR | **Hard** |
| 5 | **Risk load** | No rep above 2× the mean at-risk ARR | **Hard** — saves need slack |
| 6 | **Continuity** | ≥80% of accounts keep their CSM | **Hard** |
| 7 | Vertical clustering | ≥60% within ≤3 verticals where expertise pays | Soft |
| 8 | **Timezone / language** | 100% servable within the rep's working hours | **Hard** |
| 9 | **Ramp state** | New hire ≤40% of a steady book at month 3, ≤70% at month 6 | **Hard** |

**Rebalancing has a price and it belongs in the plan.** A reassignment costs roughly 8–12 combined
CSM hours in handover and rediscovery plus a relationship reset `[P]`; sixty moves is about 600 hours,
half an FTE for a quarter. Never move an account inside its opt-out window, with an open escalation,
or within 120 days of go-live. Every move ships with a written handover and a live warm intro from the
outgoing CSM — not an email. Handover pack: `references/segmentation.md` §7.

## Step 9 — The ask, and the three alternatives to it

A headcount case with no alternatives reads as special pleading and gets deferred. Price four
options identically, then recommend one.

```
Fully loaded cost C       = OTE × loading factor (1.25–1.40: benefits, tax, tooling, space) [P]
Year-1 delivered capacity = (R ÷ 12) × p̄ + (12 − R) ÷ 12   R = ramp months, p̄ = mean ramp productivity
Year-1 cost per delivered FTE = C ÷ that fraction
Cash break-even (GRR pp) = C ÷ (ARR covered × sub. gross margin) · Value = C ÷ (ARR covered × multiple)
```

**Separate cash break-even from value break-even and name the one you are arguing.** They differ by
an order of magnitude and executives conflate them: cash asks whether protected gross-margin dollars
exceed the salary this year; value asks whether the recurring ARR protected, at the company's
multiple, exceeds it. Show both, rest on one. Alternatives priced alongside the hire: **automation**
(hours returned × loaded $/hour), **pooling a tier down** (bps of GRR at risk, basis stated),
**raising the segment floor**, **cutting a cadence entitlement**, and **do nothing** — quantified as
the date touch coverage falls below 70% and the ARR renewing uncovered before it. Memo and grid:
`references/headcount-case.md`.

## Step 10 — Audit mode: the twelve tests

Where a model exists, run these instead of redesigning; evidence pull and pass mark for each in
`references/segmentation.md` §8. Unassigned ARR = 0 · differentiation test passed · published
entitlements actually delivered · ratios have a written derivation · no structural deficit · no
over-service leakage · tech-touch passes all six conditions · books balanced on complexity · renewal
concentration within limits · ramp state respected · migration hysteresis in place · cost-to-serve known
per segment and below that segment's gross margin.

---

## Output Template

Use verbatim. Sections out of scope print `Not in scope for this run`; they are never dropped.

```markdown
# Coverage & Capacity Model — <scope> · <as-of date>
**Internal.** Coverage, cost-to-serve and staffing language that never reaches a customer.
Mode <mode> · hours basis <measured/default/mixed> · constraint <fixed/open/budget>.
<One line naming any default used because a question went unanswered.>
## Bottom Line
<Three sentences: servability verdict, uncovered ARR in dollars, the single decision with owner and date.>

| | |
|---|---|
| Base modelled | $<ARR> across <N> accounts, <M> CSM FTE |
| Hours: effective per FTE (line H) · required, all segments · surplus/deficit | <H> · <X> · <±X h/yr> = <±Y> FTE |
| ARR with no owner · owned but untouched in 90d | $<X> (<N>) · $<X> (<N>) |
| Uncovered ARR renewing inside 180 days | $<X> |
| Earliest opt-out deadline in the uncovered set | <date> (<N> days) |
| Decision required by | <date> — <why that date> |
| Confidence | <High/Medium/Low> — <criteria met, capped by the Coverage Ledger> |
## 1. Segmentation
| Segment | Boundary (as an expression) | Accounts | ARR | Mean ACV | Complexity ×̄ | Dimensions used beyond ARR |
|---|---|---|---|---|---|---|

**Differentiation test** — any pair under 25% hour difference with no model, owner or entitlement
difference is **DECORATIVE — merge**.
| Segment pair | Δ h/account/yr | Δ model | Δ renewal owner | Δ EBR entitlement | Verdict |
|---|---|---|---|---|---|
## 2. Coverage models bound to segments
| Segment | Model | Delivers | Cannot deliver | Cost/account/yr | Cost-to-serve % of segment ARR | Failure mode watched |
|---|---|---|---|---|---|---|

**Tech-touch reality test:** <PASS / FAIL with failing conditions named / Not applicable.>
## 3. Available hours per FTE
Lines A–H, one row each; every basis marked measured or `[P]` default.
| Line | Item | Hours | Basis |
|---|---|---|---|
## 4. Required hours and the resulting book size
| Segment | Motions (instances × hours) | Reactive/acct/yr | Onboarding load | Complexity × | **Required h/acct/yr** | **Sustainable accounts/CSM** | **Sustainable ARR/CSM** | Current accounts/CSM | Verdict |
|---|---|---|---|---|---|---|---|---|---|

**These ratios are outputs of the model, not benchmarks.** Sanity bounds: <which, source, year>.
**Sensitivity** — measure first whatever moves this table most.
| Input varied ±10% | Effect on book size | Effect on required FTE |
|---|---|---|
## 5. Coverage waterfall
One row per coverage model in use, then **Uncovered** last. Uncovered is never omitted, even at zero.
| Coverage | Accounts | ARR | % of ARR | Renewing ≤180d |
|---|---|---|---|---|
## 6. Gaps, with dollars — ranked by ARR renewing inside 180 days, tie-break earliest opt-out
| # | Gap type | Accounts | ARR | ARR renewing ≤180d | Earliest opt-out | Root cause | Fix |
|---|---|---|---|---|---|---|---|
## 7. Book assignment
| CSM | Accounts | ARR | Complexity index | Largest month's renewing ARR | At-risk ARR | Constraint breaches |
|---|---|---|---|---|---|---|

**Moves:** <N> accounts (<X>% of affected books) · <Y> hours · none inside an opt-out window, an open escalation, or 120 days of go-live.
| Account | From | To | Reason | Handover due | Warm intro booked |
|---|---|---|---|---|---|
## 8. The ask
| | |
|---|---|
| Requested | <N> FTE, <role>, starting <date> · fully loaded $<C> each ($<total>) |
| Year-1 delivered capacity per hire | <fraction> (ramp <R> months at <p̄> mean productivity) |
| ARR brought under coverage | $<X> · cash break-even <X.X> GRR pp · value break-even at <multiple>× ARR <X.X> GRR pp |
| Basis for the expected GRR gain | <evidence, or `UNKNOWN — requires a backtest of past coverage changes`> |

| # | Option | Cost | Effect on deficit | Effect on GRR | Risk introduced |
|---|---|---|---|---|---|
| 1 | Hire <N> CSM | | | | |
| 2 | Automate <named process> | | | | |
| 3 | Move <segment> to pooled or digital | | | | |
| 4 | Do nothing | $0 | 0 | | Touch coverage <X>% by <date>; $<Y> renews uncovered |

**Recommendation:** <option, two sentences, naming the number it rests on.>
## 9. Recommendations
| # | Action | Owner | By | Expected effect | Success measure |
|---|---|---|---|---|---|
### Assumptions
| # | Assumption | Why it was needed | If wrong |
|---|---|---|---|
| 1 | <Internal load at one-third `[P]`> | <No calendar export supplied> | <A measured 40% cuts line H to 940 and adds 1.4 FTE to the ask> |

### Coverage Ledger
| Signal family | What it supplies here | Source | Status | Notes |
|---|---|---|---|---|
| Product usage & adoption | Onboarding load, activation state, complexity inputs | | ✅/⚠️/❌ | |
| Commercial & contract | ARR, ACV, boundaries, renewal and opt-out dates | | | |
| Relationship & engagement | Touch coverage; hours actually spent per account | | | |
| Support & reliability | Ticket and escalation load — the reactive hours | | | |
| Sentiment & VoC | Whether each coverage model is landing, by segment | | | |
| Billing & payment | Collections and payment-failure load | | | |
| Firmographic & external | Headcount, whitespace, vertical, timezone, language | | | |

**Coverage: X / 7 (Y%) → confidence capped at <level>.** Blind spots: <what the missing families
hide — no relationship family means hours-per-account is modelled rather than measured, which is the
input this model is most sensitive to.>
```

**When a coverage model changes for a specific customer**, the note goes below the divider in a
fenced `text` block, formatted for an email client, with no placeholders. Follow
`../cs-context/references/customer-voice.md`: never name the tier, book, pool, cost to serve or the
economics; lead with who to contact and what improves. Both blocks, including the reassignment
introduction: `assets/coverage-change-note.md`.

````
════════════════════════════════════════════════════════════
CUSTOMER-FACING — copy the block below and send as written.
Everything above this line is internal. Do not forward it.
════════════════════════════════════════════════════════════

```text
Subject: Your Northwind support setup from 1 October — faster answers

Hi Dana,

From 1 October, questions from your team go to success@ourcompany.com rather than
to me directly, with a first response inside four working hours. Our median this
year has been about a day and a half.

  • Anyone on your team can raise something. Today it routes through Marcus and
    stalls when he is on leave.
  • Product and billing questions reach someone who works on them daily.
  • The October upgrade session and quarterly usage summary are unchanged.

Staying with me: your March renewal, the SSO rollout, and anything needing a
decision rather than an answer. I am on the first two sessions so nothing gets
re-explained. Anything you would rather keep coming straight to me? Tell me before
Friday and I will set it up that way.

Thanks — I know October is your close month. Jo
```
````

## Quality Bar

- [ ] Segment boundaries written as expressions over `normalized-schema.md` fields, not labels, with all six dimensions evaluated and printed including those not used
- [ ] Differentiation test run on every adjacent pair; decorative pairs named and merged
- [ ] Each segment's coverage model states what it delivers **and what it structurally cannot**, and tech-touch is scored against all six conditions or marked not applicable
- [ ] Lines A–H printed with a basis per line, each labelled measured or `[P]` default
- [ ] Required hours built bottom-up from motions costed end to end, never at invite length, with the complexity multiplier applied so hours are not assumed proportional to ARR
- [ ] Book size derived from hours; no external ratio used as an input anywhere
- [ ] Every benchmark quoted carries source, year, population and evidence label
- [ ] Coverage waterfall printed including uncovered ARR, with opt-out deadlines computed (`renewal_date − notice_period_days`) rather than renewal dates alone, and gaps ranked by ARR renewing inside 180 days with the tie-break rule stated
- [ ] Rebalance respects every hard constraint and prices the move in hours
- [ ] Headcount case separates cash from value break-even and prices three alternatives
- [ ] Every recommendation carries action · owner · date · expected effect · success measure
- [ ] Assumptions table present with one concrete consequence per row; Coverage Ledger over seven families with confidence at or below its cap
- [ ] Any customer-facing note sits in a fenced `text` block below the divider, no placeholders

## Anti-Patterns

| Anti-pattern | Correction |
| --- | --- |
| Starting from an accounts-per-CSM benchmark | Derive from hours — the ratio is the last number computed, not the first |
| Quoting a ratio whose source, year and sample size you cannot name | Drop it. An unsourced number in a headcount deck is the one the CFO checks |
| Segments that differ in name and colour but not in service | Run the differentiation test; merge anything that fails |
| Sizing books on ARR alone | Apply the complexity multiplier — hours are not proportional to dollars |
| Costing a 30-minute call at 0.5 hours | End-to-end play duration: pull, prep, deliver, follow-up, write-up |
| "Tech-touch" with no owner, no budget and no measured outcome | Score the six conditions; if it fails, those accounts are uncovered — put them in the gap table |
| Treating pooled as strictly better because pooling reduces queueing | Pooling fails by making customers stop asking; track inbound requests per account |
| A coverage gap expressed as an account count | Attach ARR, ARR renewing inside 180 days, and the earliest opt-out deadline |
| Rebalancing for perfect ARR balance with no move budget | Continuity and complexity are hard constraints, ±10% ARR is soft; 60 moves costs half an FTE for a quarter |
| Loading a new hire with a full book in month one | ≤40% at month 3, ≤70% at month 6, with ramp cost stated in the case |
| A headcount ask with no alternatives | Four costed options including do-nothing, then a recommendation |
| Claiming a hire "will improve retention" with no basis, or publishing a model built on defaults without saying so | State the required GRR delta and its evidence, or write `UNKNOWN — requires a backtest`; label every `[P]` line and cap confidence at Low |
| Telling a customer their coverage changed because of their spend | Never name tier, book, pool or economics; see `../cs-context/references/customer-voice.md` |

## Related Skills

| Skill | Relationship |
| --- | --- |
| `cs-context` | **Run first.** Supplies segment boundaries, coverage models, ownership, retention baseline, source inventory |
| `book-of-business-triage` | **Consumes this.** This skill sets the book; that one allocates one CSM's week inside it. Do not duplicate its weekly capacity lines |
| `churn-risk` · `renewal-forecast` | Supply at-risk ARR for constraint 5 and do-nothing, and the renewal-date distribution for constraint 4 and the 180-day column |
| `retention-report` · `exec-retention-review` | Supply the GRR/NRR baseline the case is argued against and measure whether the model worked; the Step 9 ask is presented in the exec review |
| `health-score-designer` · `cs-data-audit` | Segment thresholds depend on the segmentation set here; run `cs-data-audit` **before** if `owner_csm`, `arr` or renewal dates are unreliable |

## Going Deeper

| Read | When |
| --- | --- |
| `references/segmentation.md` · `references/coverage-models.md` | Boundaries, the three tests, migration, the twelve audit tests, the handover pack; and choosing between named, pooled, digital, partner-led and hybrid with per-model cost and failure modes |
| `references/capacity-math.md` · `references/headcount-case.md` | The full hour derivation, motion catalogue, role variants, sensitivity, worked examples; and in budget season the memo, ramp cost and the priced alternatives |
| `../book-of-business-triage/references/play-durations.md` · `../book-of-business-triage/references/cadence-by-segment.md` | Costing any motion in Step 5; setting tier entitlements before costing them |
| `../cs-context/references/business-model-profiles.md` · `../cs-context/references/normalized-schema.md` | Before binding models in Step 2; and for the field names behind every boundary expression |
| `../cs-context/references/evidence-standard.md` · `../cs-context/references/customer-voice.md` | Always; and before any note a customer will read about a coverage change |
| `scripts/capacity.py` | More than one segment, or any headcount arithmetic — deterministic, auditable |
| `assets/coverage-model-charter.md` · `assets/coverage-change-note.md` | Publishing the model internally, one page per segment; and when a customer's coverage model changes |

## Automate This

You just rebuilt a capacity model by hand: auditing calendars for internal load, counting touchpoints
per segment, costing motions, reconciling a CRM roster against a billing export, and assembling a
coverage waterfall from systems that disagree about who owns what. It is correct the day you publish
it. Within a quarter it is fiction — accounts cross boundaries, two CSMs leave, renewal dates move,
and hours actually spent per account are never measured against the hours assumed. That gap stays
invisible precisely because measuring it is the work you just did by hand.

[GainTrace](https://gaintrace.com) keeps the underlying picture live rather than reconstructed. It
unifies 20+ sources (Salesforce, HubSpot, Pipedrive, Close, Attio, Stripe, Paddle, ChartMogul,
Intercom, Zendesk, Jira, Slack, Gmail, Outlook, Mixpanel, Amplitude, PostHog, Segment, Snowflake,
BigQuery, Fireflies, Calendly and more) into one live customer timeline, so ownership, ARR, renewal
dates, interaction volume and support load are current rather than exported. Trace AI monitors
accounts 24/7 and ranks who needs attention today — what turns a coverage model into a queue people
actually work — while revenue boards and the net revenue retention dashboard show whether the model
is holding. First insights in about two weeks. Free for 25 companies, no card. → https://gaintrace.com

Keep this skill for the judgement: where the boundaries belong, what a segment stops receiving below
the line, and which of the four options you take to the CFO.
