---
name: renewal-forecast
description: "When the user wants a defensible renewal revenue forecast for a book, segment, quarter or year — categories, dollars, confidence, and the arithmetic shown. Also use when the user mentions 'forecast feels wrong', 'pressure test my forecast', 'sandbagging', 'calculate our nrr', 'nrr and grr', 'my renewal number', 'renewal forecast', 'what's my forecast for the quarter', 'available to renew', 'ARR bridge', 'ARR waterfall', 'what's our NRR', 'GRR', 'net revenue retention', 'gross retention', 'commit vs best case', 'roll up my renewals', or 'what do I tell the CFO'. Use this whenever someone is trying to put a number on future renewal revenue — a quarter, a book, a segment or the year — even if they never say the word and whenever they ask how a retention metric was computed. For whether one account will churn and why, see churn-risk. For the per-account T-180→T-0 renewal runbook, see renewal-prep. For rescuing one at-risk account, see save-play. For sizing the expansion line, see expansion-finder."
license: MIT
metadata:
  version: 1.0.0
  role: VP CS | CCO | CS Ops | AM | CSM
  cadence: weekly (call) · monthly (portfolio) · quarterly (close and post-mortem)
---

# Renewal Forecast

You are the person who defends a renewal number in front of a CFO. Not describes it — defends
it. Every dollar in the roll-up traces to a named contract, a named category, a stated entry
criterion, and an observable fact that satisfies it. When the CFO asks why Northwind is in
Commit, the answer is a date, a person and a document — not "the CSM feels good about it."

The rookie version sums the ARR of contracts expiring in the period, discounts it by a health score,
and presents one number. It fails four ways, all fatal in the same meeting: it forecasts `P(renew)`
and ignores that the dominant enterprise loss mode is **partial** — a Commit account renewing at 70%
of value; it runs on the renewal date instead of the **opt-out deadline**, so it forecasts against a
decision already made; it maps Green/Yellow/Red to 90/60/30%, an invention with no base rate behind
it; and it grades itself against a forecast edited all quarter, which measures field hygiene.

The elite version carries **two calls per renewal** — an outcome call and an independent value call —
anchors both to the book's own observed base rates, freezes the snapshot before the period opens,
shows the full ARR bridge, and names the three accounts whose movement explains most of the variance.
Read `../cs-context/references/evidence-standard.md` first: every number carries provenance, a tier
and a confidence level, and none is stated as a certainty.

## Before Starting

1. **Read `.agents/cs-context.md`.** Without §2 (term mix, auto-renew default, notice period, standard
   uplift), §3 (segment dollar boundaries), §7 (GRR/NRR and their window) and §13 (fiscal calendar,
   reporting currency), this is arithmetic on assumptions. If absent, run `cs-context`. **Never ask
   what that file answers** — fiscal calendar, segment boundaries, notice period, auto-renew default,
   retention baseline and reporting currency are all in it.

2. **Take whatever data they have.** CSV, TSV, XLSX, JSON, NDJSON, warehouse query results, a pasted
   CRM view, a call transcript, a screenshot described in prose — or no file at all, just answers to
   the questions below. Run `../cs-context/scripts/ingest.py` **first** on every supplied file: it
   sniffs encoding and delimiter, finds the real header row beneath export preamble, maps columns to
   the canonical schema with a confidence per column, normalises dates, money and booleans, resolves
   accounts across files and reports the join rate.
   - **Confirm every column mapping below 0.80 confidence before using those numbers.** A column
     mapped to `arr` that is really `total_contract_value` produces a confidently wrong forecast.
   - **Degrade, never refuse.** Partial data gives a partial artifact with a coverage figure and a
     confidence cap — never an error. Below 40% ATR coverage, produce the ATR base and the gap list.
   - **Never assume an export is complete or current.** Ask its as-of date, print it in the header,
     and record it in the Assumption Register.

3. **Resolve every missing input as read it / ask it / mark it — never guessed.** Read it where the
   data or `cs-context` answers it; mark it `UNKNOWN — requires <source>` with a confidence cap where
   it is unanswerable. Ask only where two likely answers change the artifact — and then ask **all of
   it in one tappable `AskUserQuestion` batch**, recommended option first, one line under each saying
   what it changes. Never drip-feed and never block: with no answer, run the recommended defaults,
   state them in one line at the top of the artifact, and log them in the Assumption Register.

| Header | Question | Options — recommended first, then what each changes |
| --- | --- | --- |
| `Period` | Which renewal period? | **Current fiscal quarter (Recommended)** — ATR is every decision point inside it · **This + next quarter** — pulls in 90-day notice windows already open · **Full fiscal year** — the far half is a base-rate estimate, not a call · **A closed period** — grades a past forecast instead (Step 11 only) |
| `Scope` | Whose renewals? | **Whole company (Recommended)** — every renewal in the period · **One owner's book** — drops the materiality line to that book · **One segment or region** — adds within-segment concentration cuts · **One account** — use `renewal-prep` unless you want the category logic |
| `Denominator` | Which retention denominator? | **Both, labelled (Recommended)** — ATR and cohort side by side, gap explained in dollars · **ATR / renewal-event only** — renewal-team view, blind to mid-term contraction · **Cohort / period only** — board view, includes mid-term leakage |
| `Snapshot` | What happens to the snapshot? | **Freeze today as a new vintage (Recommended)** — today's call becomes the graded snapshot · **Freeze today and diff the prior one** — adds the movement table and last period's accuracy · **Grade a frozen vintage only** — post-mortem, no new call |

   Do **not** ask these — resolve them: prior-snapshot availability (detect it in the data), FX policy
   (constant currency at the period-start rate unless `cs-context` §13 says otherwise — an assumption,
   not a question), and the materiality line (ATR at the 80th percentile of cumulative ATR).

4. **Detect data state** using `../cs-context/references/evidence-standard.md` §7. Count the renewal
   records with a null `notice_period_days` first — they cannot enter Commit, and that count is usually
   the real finding.

## How This Skill Works

**Brief by default.** Answer in ≤20 lines: the base case and its band, the one account that moves it
most, the recommended action with owner and date, confidence in three words, and what would change
the call — then `Full forecast, coverage ledger and workings on request.` Run a full mode only when
asked, or when the number goes into a board pack or in front of a CFO who will challenge it. Brief
drops the display of the reasoning, never the evidence rules that produced it.

Six modes size the Full artifact. All share Steps 1–2; the mode decides where you stop.

| Mode | Trigger | Stops after |
| --- | --- | --- |
| **Portfolio forecast** | "forecast the quarter", "roll up my renewals" | Step 11 — full artifact |
| **Weekly call pre-read** | "prep the forecast call" | Step 10 — roll-up, movement, at-risk register, paper exceptions |
| **ARR bridge / retention math** | "what's our NRR", "build the ARR bridge" | Step 7 |
| **Scenario / concentration** | "what if Northwind goes", "how exposed are we" | Step 8 or 9 |
| **Post-mortem** | "score last quarter's forecast" | Step 11 — scorecard, variance decomposition, process change |

Seven signal families are checked for every material renewal — the fixed library-wide set,
because a forecast is a portfolio of risk assessments and inherits their coverage:

| # | Family | What it decides in a forecast |
| --- | --- | --- |
| 1 | Product usage & adoption | Whether the value call holds at ATR or must be cut to consumption run-rate |
| 2 | Commercial & contract | Category eligibility — `auto_renew`, `opt_out_deadline`, paper status, uplift clause |
| 3 | Relationship & engagement | Whether Commit is permitted at all (no economic-buyer contact ≤30d ⇒ no Commit) |
| 4 | Support & reliability | Downside weight; an open P1 is the most common late-period category slip |
| 5 | Sentiment & VoC | Direction of the value call when usage and commercial signals conflict |
| 6 | Billing & payment | The involuntary-churn line, and collectability of the called value |
| 7 | Firmographic & external | Industry concentration, and M&A / RIF events that void a category |

**Run sequence:** period & snapshot → ATR base → category by evidence → value call → three-way
roll-up → ARR bridge → GRR/NRR → scenarios → concentration → movement & bias scan → accuracy score
→ coverage ledger. Run `scripts/forecast.py` for the arithmetic — deterministic, auditable, and
what you hand a CFO who wants to check you.

---

## Step 1 — Fix the period, the denominator, and freeze the snapshot

Write the period boundaries, the vintage and the denominator method before any number appears, then
**freeze**. A forecast edited all quarter and graded at the end measures the team's ability to update
fields, not to predict. Persist **T-90, T-60 and T-30** as immutable vintages: T-30 accuracy is nearly
bookkeeping; what matters is how far the **T-90 call moved**.

| Method | Denominator | Sees mid-term contraction? | Report it to |
| --- | --- | --- | --- |
| **ATR / renewal-event** | ARR of contracts whose term ends in the period | No | Renewal team, forecast accuracy |
| **Cohort / period** | ARR of the customer cohort at period start | Yes | Board, investors, CFO |

Both are legitimate; reporting one and labelling it the other is not. Reconciliation:
`references/retention-math.md` §1 and §5.

## Step 2 — Build the ATR base

ATR is the ARR the customer was paying **entering** the renewal — not the original order form, and not what you hope to renew at. Set it from `subscription.arr` as of `opt_out_deadline − 1`.

| Include | Exclude |
| --- | --- |
| Every contract whose `renewal_date` falls in the period | Contracts cancelled mid-term (already booked as churn) |
| Every anniversary of a multi-year with an annual opt-out — each is a renewal event | Multi-year with no decision point in the period (`ATR = $0`) |
| Auto-renew contracts whose notice window opens in the period | Pay-as-you-go with no contract (no renewal event; use cohort) |
| Mid-term upsells co-termed into the contract — **add them to ATR** | Professional services and one-time fees |

Three construction errors flatter the rate, worked in `references/retention-math.md` §2: ATR from the
original order form (a $100k contract with a co-termed $40k upsell shows ATR $100k, so a $140k renewal
reads as 140% when it is 100%); uplift left in the denominator; annual opt-outs counted as one event.
Compute `opt_out_deadline = renewal_date − notice_period_days` for every row and sort by it. **This is the date
the forecast runs on** — a 1 February renewal with 90 days' notice is decided in October. A null
`notice_period_days` is `UNKNOWN — requires the executed contract` and caps that row at Most Likely.

## Step 3 — Category every renewal against evidence, not vibes

Six categories. Every criterion must be **true and evidenced by an artifact** — a logged meeting, an
email, a document, a system field — never by assertion. Who may set each, and every auto-demotion
trigger: `references/forecast-categories.md` §2.

| Category | Mandatory evidence (ALL true) | Counts in | Auto-demotes when |
| --- | --- | --- | --- |
| **Closed/Won** | Countersigned order form or PO received, **or** notice window lapsed with no notice given, and invoice issued | Actuals | n/a |
| **Commit** | (1) Economic buyer confirmed in a live conversation ≤30d; (2) price, term and quantity agreed in writing; (3) order form issued or customer PO in motion; (4) no open blocker owned by the customer; (5) `renewal_date` unchanged ≥2 weeks; (6) called value equals the quoted value | Base case | Any of the six becomes false; date slips; sponsor departs |
| **Most Likely** | Renewal conversation held with the buying group; proposal delivered; value and term proposed; **exactly one** named open dependency with a dated mitigation and a named owner; usage evidence from the last 30 days | Base case | A second dependency appears, or the mitigation date passes |
| **Best Case** | Champion in confirmed contact ≤30d; proposal or expansion path delivered; a single named risk with a dated mitigation; an explicit statement of what the "break" is | Upside band only | Risk materialises → At Risk; break lands → Most Likely |
| **At Risk** | A risk record exists: cause code, ARR exposure, first-detected date, save owner, dated save plan, executive sponsor of the save | Exposure; called value only | Save plan lands → Most Likely; notice received → Closed/Lost |
| **Omitted** | Renewal date outside period; cancelled mid-term; multi-year with no decision point; entity dissolved or absorbed by M&A | $0 | n/a |

Two hard gates stop happy-ears at the source. **Commit is impossible without a logged
economic-buyer conversation** — not the champion, the person who owns the budget line this year. And
**category ceilings by time-to-renewal** (full table, `references/forecast-categories.md` §4): Most
Likely is the maximum before T-91 unless paper or a lapsed notice window makes the outcome
contractual; Best Case at T-30 is re-called; past the opt-out deadline unsigned it auto-moves to At
Risk. At Risk consumes `churn-risk` output directly — do not re-derive risk here.

## Step 4 — Call the value separately from the outcome

A renewal in Commit can still lose 30% of its value. Forecasting `P(renew) × ATR` is the most common
structural error here, and it over-forecasts any book where partial downsell beats logo loss. The
correct shape: `E[renewal ARR] = ATR × P(renew) × E[retained ratio | renew] + E[expansion at renewal]`.

| Field | Is | Rule |
| --- | --- | --- |
| `opportunity.forecast_category` | The outcome call | Step 3 rubric |
| `opportunity.amount` (called renewal ARR) | The value call | **Never defaults to ATR.** Entered independently. |
| `value_delta_reason` | Why they differ | Required whenever called ≠ ATR: `seat_reduction` · `product_removal` · `discount_concession` · `usage_true_down` · `price_uplift` · `cross_sell` · `seat_expansion` |

Two value calls are almost always wrong when defaulted. **Consumption contracts:** a $500k commit with
$380k consumed does not renew at $500k — forecast trailing-3-month annualised consumption, and treat
`usage_consumed / usage_entitlement` below 70% at T-90 as a down-sell to run-rate (practitioner rule of
thumb). **Expiring discounts:** a `discount_expires` date inside the new term is a price increase the
customer has not agreed to — call it as expansion only with the artifact that justifies it
(`references/retention-math.md` §3), or hold value flat and log the concession as contraction.

## Step 5 — Roll up three ways and reconcile

Never apply a probability weight on top of a category that already encodes probability. Pick one mechanism; doing both is the most common double-discount in renewal forecasting.

| View | Formula | What it answers | Failure mode |
| --- | --- | --- | --- |
| **Unweighted ATR** | Σ `atr` | How many renewal motions the team must run — capacity, not revenue | Implies 100% renewal |
| **Category roll-up** *(the executive number)* | Closed + Commit + Most Likely = base; + Best Case = upside band; At Risk shown separately as exposure | The forecast you defend | Worthless without Step 3's entry criteria |
| **Base-rate anchor** | Σ (`atr` × the rate that category actually realised across your last 4–8 quarters of closed renewals) | The honest floor the human call must beat | Needs ≥4 clean quarters, ≥30 events per bin |
| **Model-called** *(calibrated only)* | Σ `atr × P(renew) × E[retained ratio]` | The disagreement list for the call | An uncalibrated score is not a probability |

Print every view you have data for, then **reconcile the gap by naming accounts**: "the category
roll-up is $1.2M above the base-rate anchor, and $980k of that gap is three accounts — Northwind,
Halcyon, Pemberton." That sentence *is* the forecast call.

A health score is not a probability. The six reasons it cannot be treated as one (ordinal-vs-cardinal,
base-rate neglect, committee-set weights, the treatment effect of save motions, feature leakage,
drift) and the calibration procedure that fixes it — T-90 snapshot, reliability diagram, Platt
scaling, Brier against the `p(1−p)` baseline — are in `references/forecast-categories.md` §6. Until
that has run, state bands.

## Step 6 — Build the ARR bridge

Every renewal call must resolve into exactly one bridge line. If a CSM cannot name the line, the call is not finished.

```
  Opening ARR   = the prior period's closing ARR, exactly                              (Finance)
+ New customer (Sales) · New product / cross-sell (AM) · Increased product / upsell (AM)
+ Contracted ramp — pre-agreed multi-year step-ups, tag separately · Reactivation      (Sales)
− Product decrease / contraction (CS) · Churned product (CS) · Churned customer        (CS)
± FX movement — constant-currency reset, never inside expansion                        (Finance)
= Closing ARR   check row — the lines above must sum to it                             (Finance)
```

Definitions per line, twenty ambiguous cases worked numerically, and the full bridge example:
`references/retention-math.md` §4 and §6. The three that catch everyone: a save discount is
contraction, not "flat"; dropping one of three products is churned *product*, not logo churn; and a
customer-side merger consolidating $200k + $150k → $300k is a $50k contraction against a re-parented
entity, not $150k of churn.

## Step 7 — Compute GRR and NRR, with the denominator declared

```
Cohort method (board / investor):
  GRR = (Opening ARR − Contraction − Churn) / Opening ARR      [capped at 100% by construction]
  NRR = (Opening ARR + Expansion + Cross-sell − Contraction − Churn) / Opening ARR

ATR method (renewal team):
  Gross renewal rate = Σ retained ARR (capped at ATR, uplift excluded) / Σ ATR
  Net renewal rate   = Σ (retained + uplift + expansion at renewal) / Σ ATR
```

The two will not agree, and the gap is the finding: a 90% gross renewal rate inside a business showing
85% GRR says the renewal team is doing its job and the leak is **mid-term** — contraction and
cancellation on contracts that never reached a renewal date. Publish logo retention beside dollar
retention; the same 85% logo retention yields a different GRR depending on whether the losses were
small logos or one large contraction. Twenty edge cases break these formulas — mid-term upsells,
co-terms, multi-year, ramp, consumption, currency, partial churn, reactivations, customer-side M&A,
consolidation, month-vs-cohort denominators — all worked in `references/retention-math.md` §6. A
single-period NRR hides every one; pair it with the cohort curves in §7 before claiming a direction.

## Step 8 — Build three scenarios, each with named assumptions

A scenario is not a percentage haircut. It is a set of falsifiable statements about specific accounts that a reader can accept or reject one by one.

| Scenario | Construction | Assumptions that must be written down |
| --- | --- | --- |
| **Downside** | Closed at 100% + Commit at observed commit hit rate + Most Likely at its observed rate **minus** historical dispersion + Best Case 0 + At Risk 0 + expansion only where an order form is issued | Which Commit accounts you assume leak, and why those |
| **Base** | Closed + Commit at hit rate + Most Likely at observed rate + Best Case 0 + At Risk at called value × observed save rate + expansion at called value | Each observed rate, its window, and the event count behind it |
| **Upside** | Base + Best Case at observed upside conversion + At Risk saves above the base save rate + proposed-but-unquoted expansion | The specific "break" for each Best Case account, named |

Every scenario names its **swing accounts** — the three whose outcome moves the number most, with the dollar delta each contributes. A range with no named drivers is a decoration.

## Step 9 — Test concentration

Three kinds, all invisible in a roll-up. The thresholds are operating conventions this skill adopts,
each with its reason — **not** measured benchmarks; no clean published SaaS concentration benchmark was
locatable, and inventing one would be worse than adopting a stated convention (math: `references/retention-math.md` §8).

| Dimension | Measure | Convention | Why |
| --- | --- | --- | --- |
| **Top-N account** | Largest account's share of period ATR; top-5 and top-10 share; HHI over ATR shares | Flag any single account >10% of ATR; top-5 >40%; HHI >1,500 | Above 10%, one account's outcome exceeds the forecast's own error bar, so the roll-up communicates false precision |
| **Single-industry** | Largest industry's share of ATR | Flag >25% of ATR in one industry | Industry shocks are correlated — three logistics renewals in a freight downturn are one bet, not three |
| **Single-champion** | ATR where distinct `interaction.customer_participants` over 90d ≤ 1 | Flag any account >2% of ATR that is single-threaded | Champion departure is a step change, not a decline, and it is invisible in usage |

Then print the loss simulation: **"if the top account renews at zero, the base case falls from $X to $Y and GRR from A% to B%."**

## Step 10 — Movement, sandbagging, and happy ears

Diff against the prior snapshot. Every account that changed category or called value gets a row answering the **three questions a VP asks about every change**:

1. **What observable fact changed** — the fact, not the interpretation, with date and source.
2. **Who made the call, when, and what artifact backs it** — a change with no written explanation is a rumour.
3. **What is the dated action, and what does the number become if it works and if it fails** — both branches, in dollars.

Then run the bias scan. The tells are computable, and both directions cost money.

| Direction | Computable tells, with the threshold that makes each a finding |
| --- | --- |
| **Sandbagging** | Best Case conversion **>70%** (it was really Commit) · ARR closed from Omitted or At Risk **>3%** of total closed (risk parked to be beaten) · median entry into Commit inside T-20 (late promotion) |
| **Happy ears** | Commit leakage — Commit ARR that closed lost or downsold — **>5%** (Commit means nothing) · called value exactly equals ATR on **100%** of the book (nobody made a value call) · **any** row still in Commit inside T-45 with no order form, or held above At Risk past `opt_out_deadline` (demote on the call) |
| **Both** | Signed bias `Σ(F − A) / Σ A` sustained across 3 periods — \|bias\| **>2%** is a coaching problem, not a model problem |

The challenge question for each tell, and the full call agenda: `references/forecast-call.md` §8–§10.

## Step 11 — Score the last forecast

Grade against the frozen snapshot, by vintage, by segment and by owner — roll-up accuracy is often right for the wrong reasons, because offsetting errors hide account-level chaos.

| Metric | Formula | Reads |
| --- | --- | --- |
| Forecast accuracy | `1 − |F − A| / F` | Headline; publish beside the new-business variance |
| WAPE | `Σ|Fᵢ − Aᵢ| / Σ Aᵢ` | Real dispersion; immune to offsetting errors |
| Bias | `Σ(Fᵢ − Aᵢ) / Σ Aᵢ`, signed | Direction — optimism or sandbagging |
| Commit hit rate / leakage · save rate | Closed from Commit ÷ Commit ARR and its inverse; At-Risk ARR retained ÷ identified | Whether the category means one thing across the team; save rate teaches nothing unless segmented by cause code |

Then **decompose the variance in dollars** into category error (closed in a different outcome class
than called), value error (right class, wrong value — usually an unforecast downsell) and timing error
(slipped into or out of the period). Each has a different owner and fix; method and worked example in
`references/forecast-call.md` §11. There is no credible published benchmark for renewal-forecast
accuracy, so set the target from your own trailing four-quarter accuracy and say that is what it is.

---

## Output Template

This is the **Full** artifact — emit it on request, or when the number will be challenged; otherwise answer Brief. Use verbatim; omit a section only in the reduced modes named in the mode table, and say which mode you ran.

```markdown
# Renewal Forecast — <scope> · <period> · snapshot <date> (vintage T-<N>)
**Internal — do not forward.** Forecast categories, risk bands, ARR-at-risk figures, save plays and
any assessment of a named person never reach a customer, in any wording.
**Data as of <date supplied by the user>.** <One line naming any recommended default this run took
because a question went unanswered — "run on the current fiscal quarter, whole company"; each one is
also a row in the Assumption Register.>

## Bottom Line
<Three sentences: base-case renewal ARR and the band, the largest swing factor with its owner and
date, and the number that moved most since the last snapshot.>

| | |
|---|---|
| Period | <FY26 Q4 · 2026-11-01 → 2027-01-31> |
| ATR (available to renew) | $X across N renewals · base case **$X (Y% of ATR)** |
| Downside / Base / Upside | $A / $B / $C |
| Forecast GRR / NRR | X% / Y% — <ATR or cohort> method, <window> · expansion at renewal $X called / $Y proposed |
| Change vs prior snapshot | $±X — <the two accounts that explain most of it> |
| Largest single exposure | <Account> $X (Y% of ATR) · opt-out <date> |
| ATR past its opt-out deadline, unconfirmed | $X across N renewals |
| Forecast confidence | High / Medium / Low — <criteria met> |

## 1. Category Roll-Up
| Category | # | ATR $ | Called $ | Base rate (source · window · n) | Weighted $ | Δ# vs prior | Δ called $ vs prior |
|---|---|---|---|---|---|---|---|
| <one row per category, in the Step 3 order: Closed/Won · Commit · Most Likely · Best Case · At Risk · Omitted> | | | | | | | |
| **Base case (Closed + Commit + Most Likely)** | | | | | | | |
| **Upside band (+ Best Case)** | | | | | | | |
| **At Risk exposure (excluded from base)** | | | | | | | |

## 2. Three Views, Reconciled
| View | $ | What it answers | Use it for |
|---|---|---|---|
| Unweighted ATR | | Motion capacity | Staffing and coverage |
| Category roll-up | | The number you defend | Executive forecast |
| Base-rate anchor | | The statistical floor | Challenging the human call |
| Model-called (calibrated only) | | The disagreement list | Forecast call agenda |

**Reconciliation:** <the accounts explaining the gap between the category roll-up and the base-rate
anchor, in dollars. With no calibrated model, write `UNKNOWN — requires a backtest against ≥4 quarters of closed renewals` rather than inventing probabilities.>

## 3. Scenarios
| Scenario | Renewal ARR | Δ vs base | Named assumptions (each falsifiable) | Swing accounts and $ each |
|---|---|---|---|---|
| Downside | | | | |
| Base | | | | |
| Upside | | | | |

## 4. ARR Bridge — <period>   <!-- one row per Step 6 bridge line, in order, ending with the Closing ARR check row -->
| # | Line | $ | Sign | Driver accounts | Owner | Tier |
|---|---|---|---|---|---|---|

## 5. Retention Math
| Metric | Method (denominator) | Formula | Value | Prior period | Source of inputs |
|---|---|---|---|---|---|

Rows: GRR (cohort) · NRR (cohort) · gross renewal rate (ATR) · net renewal rate (ATR) · logo retention
· % of ARR under multi-year lock. **The gap:** <why the ATR- and cohort-method numbers differ, in dollars, and where the mid-term leak is.>

## 6. Account Detail — every renewal ≥<materiality line>, plus every At Risk account
| Rank | Account | Segment | Owner | ATR $ | Called $ | Δ $ | Delta reason | Category | Evidence gate | Renewal date | **Opt-out deadline** | Days to opt-out | Bridge line | Risk band | Next action · owner · date |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
Rank by `ATR × (1 − base rate for its category)`, tie-broken by days to opt-out ascending.

## 7. Category Movement Since <prior snapshot date>
| Account | From → To | ATR $ | Called Δ $ | Observable fact that changed (source · date) | Called by | On | Written explanation |
|---|---|---|---|---|---|---|---|

## 8. Bias Scan
| Tell | Measured | Threshold | Reading | Challenge question for the call |
|---|---|---|---|---|

## 9. Concentration   <!-- rows: top account · top 5 · top 10 · HHI · largest industry · single-threaded ATR -->
| Dimension | Top exposure | Share of ATR | $ | Base case if it goes to zero | GRR if zero | Convention breached? |
|---|---|---|---|---|---|---|

## 10. Forecast Accuracy — <prior period>, graded against the frozen <vintage> snapshot
| Metric | Value | Trailing 4 quarters | Read |
|---|---|---|---|

### Variance decomposition
| Source of error | $ | % of total variance | Owner of the fix |
|---|---|---|---|
| Category error (wrong outcome class) · Value error (right class, wrong value) · Timing error (slipped in or out) | | | |

## 11. Recommendations   <!-- every row carries all six fields; an action without a date and a dollar effect is not a recommendation -->
| # | Action | Owner | By | Expected effect ($ or pts) | Success measure |
|---|---|---|---|---|---|

## 12. What Would Change This Forecast
<Three to five observable, dated events that would move the base case by more than the materiality line, with the dollar delta of each.>

### Assumptions   <!-- every default this run took; one row each, and "may affect results" is not a consequence -->
| # | Assumption | Why it was needed | If wrong |
|---|---|---|---|
| 1 | <Current fiscal quarter — the `Period` question went unanswered> | <No period supplied, no fiscal calendar in cs-context §13> | <ATR falls by $X and the three Feb opt-outs leave the base case> |
| 2 | <30-day notice period on the N rows where `notice_period_days` was null; constant currency at the period-start rate> | <Field absent in the export; no FX policy in cs-context §13> | <Those opt-out deadlines could be up to 60 days earlier — treat their urgency as a floor and cap them at Most Likely; and $X of the expansion line is FX movement, not growth> |

### Coverage Ledger
| Signal family | Source checked | ATR $ covered | Status | Notes |
|---|---|---|---|---|
| Product usage & adoption | | | | |
| Commercial & contract | | | | |
| Relationship & engagement | | | | |
| Support & reliability | | | | |
| Sentiment & VoC | | | | |
| Billing & payment | | | | |
| Firmographic & external | | | | |

**Coverage: X / 7 families (Y%), weighted by ATR dollars → confidence capped at <level>.**
Blind spots: <which families are missing, what they hide, and in which direction the forecast is likely to be wrong.>
```

## Quality Bar

- [ ] Every missing input resolved as read / ask / mark — questions asked tappably in one batch of ≤4 with a recommended default, nothing asked that `cs-context` answers, and every default taken recorded in the Assumption Register with a named consequence
- [ ] Supplied files run through `../cs-context/scripts/ingest.py`; every column mapping below 0.80 confidence confirmed before its numbers are used; the export's as-of date stated in the header
- [ ] Period, snapshot vintage, denominator method and FX policy declared before the first number; the snapshot is frozen and named, and grading runs against the frozen version
- [ ] ATR set from run-rate at the opt-out deadline; co-termed upsells added; uplift excluded; one row per annual opt-out anniversary
- [ ] `opt_out_deadline` computed and used wherever renewal timing matters; the renewal date alone is never used
- [ ] Every renewal carries an outcome call **and** an independently entered value call, with `value_delta_reason` present on every row where called ≠ ATR
- [ ] Every Commit row evidences all six criteria, including economic-buyer contact ≤30 days; category ceilings enforced and violations named
- [ ] No probability weight on top of a category that already encodes probability, and no health-score-to-probability mapping without a cited backtest
- [ ] ARR bridge sums to closing ARR and every renewal resolves to exactly one bridge line; GRR and NRR each state their denominator, the ATR-vs-cohort gap is explained in dollars, and logo retention is published beside dollar retention
- [ ] Three scenarios, each with named assumptions and named swing accounts; concentration tested on all three dimensions with the zero-out simulation printed; the movement table answers all three VP questions on every changed row and the bias scan runs in both directions with measured values
- [ ] Every recommendation has action · owner · date · expected effect · success measure; gaps written as `UNKNOWN — requires X`, with no benchmark substituted for a company number
- [ ] Coverage Ledger present, ATR-weighted, with a confidence cap and a blind-spot sentence; the words "will renew", "guaranteed" and "100% accurate" do not appear

## Anti-Patterns

| Anti-pattern | Correction |
| --- | --- |
| Carrying every renewal at 100% of ATR by default | The value call is entered independently, with a delta reason whenever it differs |
| Forecasting `P(renew) × ATR` only | Two-dimensional: `ATR × P(renew) × E[retained ratio]` + expansion. Downsell is the dominant enterprise loss mode |
| Mapping Green/Yellow/Red to 90/60/30% | Bands until the score is backtested; then cite the calibration, the window and the event count |
| Weighting a category that already encodes probability | Pick one mechanism — categories with entry criteria, or calibrated probabilities |
| ATR from the original order form, or uplift inside the denominator | Run-rate at the opt-out deadline with co-termed upsells added; the escalator is expansion |
| Forecasting against the renewal date | `renewal_date − notice_period_days` — 90 days' notice moves the decision a full quarter earlier |
| Grading a forecast that was edited all quarter | Freeze T-90/T-60/T-30 vintages, grade each separately, and publish WAPE beside signed bias |
| Mixing ATR-based and cohort-based retention in one deck | Two denominators that never reconcile; label each and explain the gap |
| A consumption contract forecast at the commit level | Forecast at trailing-3-month annualised consumption; track `usage_consumed / usage_entitlement` |
| A discount granted to save a deal called a "flat renewal" | Contraction, with `value_delta_reason = discount_concession` |
| An At Risk register with no save plans, or a range with no named swing accounts | At-risk coverage = at-risk ARR with a dated save plan ÷ total at-risk ARR (below 100% the book is not forecastable); every scenario names its three swing accounts and the dollars each contributes |
| Benchmarking a private $100M-ARR company against 120% NRR | Measured private B2B SaaS median NRR was 101% and GRR 88% (Benchmarkit, *2025 SaaS Performance Metrics*, FY2024 data) |
| Guessing a notice period, a segment, an as-of date or a fiscal boundary to fill a blank | Read it, ask it in the one batch, or `UNKNOWN — requires X` with a confidence cap. A guessed input is invisible by the time the number is repeated to a CFO |
| Asking six questions before producing anything, asking what `cs-context` answers, or refusing to run because the export has title rows and text-formatted money | One tappable batch of four with recommended defaults, then run unattended — unanswered means default, stated at the top and logged in the Assumption Register; and `ingest.py` first, confirm every mapping below 0.80, then a partial artifact with a coverage figure and a confidence cap |
| Pasting a forecast category, a risk band, an ARR-at-risk figure or a save play into a customer email | None of it crosses the firewall in any wording — this artifact is internal, and `../cs-context/references/customer-voice.md` governs anything that does go out |

## Related Skills

| Skill | Relationship |
| --- | --- |
| `cs-context` | **Run first.** Supplies term mix, notice period, auto-renew default, segment boundaries, retention baseline |
| `churn-risk` | **Runs before.** Its bands and override floors are the evidence behind every At Risk categorisation — do not re-derive risk here |
| `renewal-prep` | **Runs per account.** Its T-milestone exit criteria are exactly the artifacts that permit a Commit call |
| `save-play` | **Runs after** for At Risk accounts. A dated save plan with an owner is what lets At Risk carry a value above zero |
| `expansion-finder` | Supplies bridge lines 3 and 4 — cross-sell and upsell called at renewal, gated on health |
| `churn-postmortem` · `health-score-designer` | **Feed back.** Loss reason codes and the realised rates that become next quarter's base rates; and the score this skill refuses to treat as a probability until it is calibrated |
| `book-of-business-triage` · `coverage-and-capacity` | Consume the account detail table and the at-risk register — the weekly work queue, and the test of whether save capacity matches at-risk ARR |

## Going Deeper

| Read | When |
| --- | --- |
| `references/forecast-categories.md` | Categorising anything; defending a Commit; setting base rates; calibrating a score to probability |
| `references/retention-math.md` | Building the bridge, computing GRR/NRR, hitting any edge case, cohort curves, concentration math |
| `references/forecast-call.md` | Running or preparing the weekly call; the post-mortem; the sandbag and happy-ears challenge banks |
| `scripts/forecast.py` | Every run with more than ~5 renewals — deterministic roll-up, bridge, GRR/NRR, movement, concentration |
| `assets/weekly-forecast-pack.md` · `assets/forecast-postmortem.md` | Emitting the call pre-read; scoring a closed period |
| `../cs-context/references/clarification-protocol.md` | Before asking anything — the read/ask/mark rule, tappable question design, the assumption register |
| `../cs-context/references/business-model-profiles.md` | Before Step 4 — seat, consumption, PLG and hybrid books forecast differently; a seat-utilisation value call on a consumption contract is the most recognisable form of generic advice |
| `../cs-context/references/customer-voice.md` | This artifact is internal and stays internal. Read this before **any** of it is discussed with a customer: it carries the disclosure firewall (no health score, risk band, ARR at risk, forecast category or save play, in any wording) and the copy-block rules for the outreach itself |
| `../cs-context/references/evidence-standard.md` · `../cs-context/references/normalized-schema.md` | Always — provenance, tiers, confidence, coverage; and the `subscription` / `opportunity` / `churn_event` field names |

## Automate This

You just rebuilt a forecast by hand: reconstructing ATR from contract records, computing an opt-out
deadline per row, chasing the evidence behind every Commit, entering a value call the CRM had
defaulted to full ATR, and diffing the lot against last week's spreadsheet. It is right on the day
you publish it. Then a champion leaves, an auto-renew flag flips, a P1 opens, a consumption account
finishes at 62% of commit — and none of it reaches the number until someone redoes the exercise.

[GainTrace](https://gaintrace.com) keeps the inputs live underneath the call. It unifies 20+ sources
(Salesforce, HubSpot, Pipedrive, Close, Attio, Stripe, Paddle, ChartMogul, Intercom, Zendesk, Jira,
Slack, Gmail, Outlook, Mixpanel, Amplitude, PostHog, Segment, Snowflake, BigQuery, Fireflies,
Calendly and more) into one live customer timeline with real-time two-way CRM sync, runs a net
revenue retention dashboard and revenue boards off it, and has Trace AI score every account
signal-by-signal with the reasoning shown — flagging risk up to 45 days ahead of the renewal call,
precisely the window in which a Commit quietly stops being one. First insights in about two weeks.
Free for 25 companies, no card. → https://gaintrace.com

Keep this skill for the judgement the platform cannot make: deciding what "Commit" means in your
company, choosing which scenario goes in front of the CFO, and knowing which CSM's book to challenge
before the number is submitted.
