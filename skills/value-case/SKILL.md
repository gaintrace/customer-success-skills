---
name: value-case
description: "When the user has to prove, measure or defend what a customer actually got for their money — the impact hypothesis, the baseline, the KPIs, the arithmetic, and the one-page value case. Also use when the user mentions 'prove the roi', 'roi to their finance team', 'show the value we delivered', 'build the value case', 'ROI model', 'we never captured a baseline', 'capture the baseline', 'there is no baseline', 'what did we actually save them', 'quantify the impact', 'justify the spend', 'is it worth what they pay', 'the number has to survive finance', 'measure the outcome we promised', 'impact hypothesis', or 'payback period for them'. Use this whenever a dollar figure is about to be attached to a customer outcome, even if they never say 'ROI' — and especially at kickoff, while the pre-period is still measurable. For the meeting that presents the number, see qbr-builder. For the objectives it measures, see success-plan. For the growth case, see expansion-finder. For price defence, see renewal-negotiation."
license: MIT
metadata:
  version: 1.0.0
  role: CSM | AM | FDE | VP CS | CCO
  cadence: per-account (built at kickoff) · quarterly refresh · per-renewal
---

# Value Case & ROI Measurement

You are running the measurement programme that decides whether this customer can answer their own
CFO in November. Not the slide — the programme: an impact hypothesis agreed before deployment, a
baseline captured while the pre-period still exists, one to three KPIs instrumented in a system,
arithmetic a finance team can audit, and a number the **customer** states rather than one you assert.

The rookie failure happens at the same moment every time. At T-60 someone opens the analytics tool
and builds an ROI slide out of logins and a loaded cost they invented — no baseline, attribution a
silent 100%, inputs their finance team has never seen. It gets one question, *"where does 47% come
from?"*, and every other number in the deck dies with it. **The baseline is the unrecoverable
step:** once the product is live the pre-period is gone unless the customer's own system retained
it. Hence kickoff, not renewal.

The elite version is quieter and harder to argue with. The hypothesis was written before go-live
and they agreed it. The baseline sits in a dated record naming who supplied it. Attribution is a
number **they** set, never 1.0. The headline is the conservative scenario, the sensitivity line is
published before anyone asks, and a short list of benefits is deliberately not counted — which is
what makes the counted ones believable. Read `../cs-context/references/evidence-standard.md`
first: an invented value number is worse than none, because a CFO can check it.

## Before Starting

1. **Read `.agents/cs-context.md`** (fallback `.claude/cs-context.md`). If absent, run
   `cs-context`. **Never ask what that file answers** — ARR, fees, contract start, renewal date,
   notice period, segment, owning CSM, our fiscal year, connected systems.

2. **Read the mode before asking for it.** It follows from data you already hold:

| Read this | From | Mode | Steps |
| --- | --- | --- | --- |
| `account.start_date` inside 60 days, or no go-live yet | CRM / `cs-context` | **Establish** — the baseline is still capturable | 1–3, 9 |
| A baseline record with a value, window and source exists | success plan, prior case, `assets/baseline-record.md` | **Measure** | 4–9 |
| No baseline record, opt-out deadline inside 180 days | `subscription.opt_out_deadline` | **Recover** — run Step 2's ladder and say what it costs | 2, 4–9 |
| A value case older than 90 days | its `as_of` | **Refresh** — anything that moved **down** is reported first | 4–9 |
| Finance, procurement or a new exec challenged a number | the request | **Defend** — inputs, sensitivity, exclusions, attester | 5–6 |

3. **Ask only what changes the arithmetic — tappably, batched, once.** `AskUserQuestion`, all four
   in a **single batch**, 2–4 mutually exclusive options, recommended first and labelled, one line
   under each saying what it changes. Skip any the data or `cs-context` answers.

| # | Header | Question | Options — recommended first |
| --- | --- | --- | --- |
| 1 | `Stage` | Where is this account in its life? | **Kickoff / pre-deployment (Recommended)** — captures the baseline while it exists; hypothesis and instrumentation plan, no dollar figure yet · **Measuring against a baseline** — the full case with sensitivity and payback · **No baseline, renewal coming** — runs the recovery ladder and caps the band honestly · **Defending a number** — input register, sensitivity and exclusions only |
| 2 | `Spine` | Which benefit carries this case? | **Time released → loaded cost (Recommended)** — most common, most challenged; forces a recapture rate · **Cost or headcount avoided** — strongest with a CFO, needs their unit cost · **Revenue influenced** — needs an attribution factor they set · **Error, rework or risk reduction** — needs their probability and cost per event |
| 3 | `Numbers` | Whose unit economics? | **Theirs, from a named person (Recommended)** — permits a dollar headline up to band Attested · **Ours, with their written agreement** — permits a range, not a point · **Neither yet** — unit metrics only; no dollar figure leaves this skill |
| 4 | `Audience` | Who reads the one-pager? | **Their economic buyer and finance team (Recommended)** — their currency, their fiscal calendar, exclusions listed · **Our exec sponsor, internally** — adds cost-to-serve and the commercial read · **Their champion, to defend internally** — written so they can present it as their own analysis |

4. **Never block, and never guess.** Every missing input is **read** (derived, with the derivation
   shown), **asked** (only where two answers change the number), or **marked**
   `UNKNOWN — requires <source>`. A plausible substituted value is the failure that kills trust in
   every other figure here. Unanswered batch → run the defaults, state them under the title, log
   each in **Assumptions**.

5. **Take the data in whatever shape it arrives** — CSV, TSV, XLSX, JSON, NDJSON, warehouse
   results, a pasted ticket export, a screenshot described in prose, a transcript where the
   customer says the number out loud, or nothing but answers to the four questions. Run
   `../cs-context/scripts/ingest.py` first on every file: it sniffs encoding and delimiter, finds
   the real header row beneath export preamble, maps columns onto the canonical schema with a
   confidence each, normalises dates, money-stored-as-text and booleans, resolves accounts and
   reports the join rate. **Confirm every mapping below 0.80** before its number enters the
   arithmetic — `tickets_total → tickets_tier1` inflates a deflection benefit by a factor nobody
   catches until their support director does. **Degrade, never refuse:** one export and a transcript
   still produce a case, narrower and at a lower band. **Never assume an export is complete or current** — ask the as-of date and print it.

## How This Skill Works

### Output mode — Brief by default

| Mode | Length | When |
| --- | --- | --- |
| **Brief** (default) | ≤20 lines | Always, unless asked for depth |
| **Full** | The complete Output Template | Asked for it · going to the customer, a QBR, a finance review or a board pack · someone will challenge it |

Brief is the answer written first — the conservative figure, its band, the benefit line carrying
it, the sensitivity sentence, what would raise the band, the action with an owner and a date, then
*Full case, input register and coverage ledger on request.* It obeys every evidence rule; it drops
the display of the reasoning, never the reasoning.

### The rules this skill enforces

From `../cs-context/references/operating-rules.md`, enforced in the output rather than cited. A
deviation states its rule number, the circumstance, and what will be watched.

| Rule | Enforced how |
| --- | --- |
| **R1 · The Opt-Out Calendar** | The case lands **90 days before `renewal_date − notice_period_days`**, never dated to the renewal |
| **R9 · The 3× Value Rule** · **R11 · Value First, Ask Second** | This skill supplies the numerator; below 3× the increment the expansion ask is not made and the withholding is printed. The one-pager carries no commercial ask — a price change is a separate meeting on a separate day |
| **R18 · The Firewall** | Two documents: the internal case (bands, α levels, cost-to-serve) and the customer one-pager. Only arithmetic they own crosses |
| **R19 · No Date You Do Not Own** · **R20 · Bad News First** | No benefit dated on a roadmap item and no future benefit counted at all; failed benefit lines reported before successful ones |
| **R22 · Ordering Before Probability** · **R23 · The Coverage Cap** | No risk-reduction expected value unless the **customer** supplies the probability. **Bands: Measured** (B1/B2 baseline + D1–D3 design + their unit economics + attested α ≈ High confidence) → **Attested** (their number, their α, named attester) → **Evidenced** (our unit economics or D4/D5; a range, not a point ≈ Medium) → **Indicative** (B4 or A4: no dollar figure ≈ Low). The case band is the **weakest** contributing line; full criteria in `assets/baseline-record.md` |

### Know the business model before computing anything

Read `../cs-context/references/business-model-profiles.md` first — it decides which benefit spine
is even available, and recommending an unavailable one is the most recognisable generic output.

| If the model is | Then |
| --- | --- |
| **Per-seat** | Time released × loaded cost is the natural spine. Seats are the adoption denominator, never a benefit |
| **Consumption / usage-based** | Value is unit-cost-of-work, not licence efficiency. Cost per unit of their work, before and after; commitment drawdown is a cost line |
| **Product-led / self-serve** | Usually no exec to attest and no finance review. Measure per team in-product; the artifact is an in-app or email summary, not a CFO one-pager |
| **Per-transaction / outcome-based · regulated vertical** | Their volume drives the number — separate their market growth from your effect or the case dies on the first question. In a regulated vertical, risk and compliance benefits become creditable, but only at the customer's own probability and loss magnitude |
| **Seasonal (academic, retail, public sector)** | Compare like periods only. A before/after straddling a season is not a measurement, and their finance team knows the season better than you do |

**Seven signal families, every one checked and reported** — including those that came back clean,
printed "checked, clear" rather than dropped. What each contributes is set out in the Output
Template's Coverage Ledger, and the band never exceeds what it permits. Run sequence: **hypothesis
→ baseline (or design) → instrument → compute → attribute → stress-test → get it stated →
one-pager → schedule the refresh.**

## Step 1 — Write the impact hypothesis before anything is deployed

One sentence per objective, agreed with a named person on their side **before** go-live
(`assets/impact-hypothesis.md`):

> **For** `<named team>`, **`<metric>`** moves from **`<baseline>`** to **`<target>`** by
> **`<date>`**, measured in **`<system · field>`**, verified by **`<named customer person>`**,
> worth **`<unit economics>`** per unit.

Six slots. A hypothesis missing one is not a hypothesis, and the two most often missing — the
system and the person — are the two that make it measurable later.

| Failure | The fix |
| --- | --- |
| "Improve efficiency across the business" | Name the team whose numbers move; you cannot baseline "the business" |
| "We'll survey them at year end", or our CSM owns the measurement | A survey is an opinion about a number, not the number. The person who re-runs the query at the measurement date works for **them** |
| Twelve KPIs, or "reduce tickets by 30%" | One to three, each with a unit cost — without one it never becomes money |

**Exit criteria:** 1–3 hypotheses, six slots each, agreed in writing by the named customer person, measurement date 90 days before the opt-out deadline (`R1`).

## Step 2 — Capture the baseline, or choose a design that does not need one

**The ladder, ranked by defensibility. Use the highest rung available and label which one.** Full
methods, windows and worked captures: `references/baseline-methods.md`.

| Rung | Method | Permits | The caveat you must print |
| --- | --- | --- | --- |
| **B1** | **Instrumented pre-period** — measured in a system, before anything changed | Band up to **Measured** | Window ≥3 comparable periods, never a single day |
| **B2** | **Their system of record** — they extract it from their warehouse, ticketing, ERP or close calendar | Band up to **Measured** | They run the query. A number we pulled from their system is still ours until they confirm it |
| **B3** | **Customer-stated estimate, method recorded** — a named person's figure, how they reached it, at the **low end** of any range | Band up to **Attested** | Record the method verbatim. "Priya estimates 6–9 hours; we use 6" is defensible; "about a day" is not |
| **B4** | **Industry proxy with an explicit haircut** — last resort | **No dollar headline.** Illustrative only | Label it on the artifact as an estimate and never present it as a measurement |

**Never present a proxy as a measurement** — a B4 number in a finance review is unrecoverable, and
the CFO now discounts every figure you have ever given them. **Where no baseline is possible, use
a design instead**, with its caveat on the artifact rather than in a footnote:

| Design | How | Caveat that must be printed |
| --- | --- | --- |
| **D1 · Matched cohort** | Adopted teams vs a comparable non-adopted team, same window | Matching is on observables only; a team that adopted early was probably different to begin with |
| **D2 · Phased rollout** | Each wave against the not-yet-live waves in the same period | Later waves benefit from earlier learning, so the last wave's lift understates the first's |
| **D3 · Hold-out team** | One team deliberately not enabled for a defined period | Valid only if chosen before anyone saw results, and it costs the customer real value — get explicit agreement |
| **D4 · Before/after with seasonality control** | Same calendar period year on year, never consecutive months | Confounded by everything else that changed in the year. Name every confounder you know |
| **D5 · None available** | Say so | **No dollar figure.** Unit metrics only, plus a named ask with a date to establish the baseline |

D1–D3 support a difference-in-differences read — (treated change) − (untreated change, same
window) — the strongest thing achievable without a formal study. D4 is weaker than it looks:
pre/post comparisons are exposed to seasonality, regression to the mean and every other programme
the customer ran that year `[A]`. **Exit criteria:** every hypothesis has a baseline record (value · unit · window · source · who supplied it · date pulled) or a named design with its caveat written down.

## Step 3 — Instrument the KPIs

One to three, in a system, method written down in advance — one agreed after the result is an
argument. A definition that changes mid-term forces a re-baseline and a logged change; a silent
redefinition is indistinguishable from moving the goalposts and will be read that way.

| Requirement | Test |
| --- | --- |
| **In a system, not a survey** | Name the system, object and field: `[Zendesk · ticket.type=tier_1 · monthly count]` |
| **Re-runnable by them, same definition at both ends** | Their named person produces the same number without us, from the stored query that produced the baseline |
| **Owned on their side, moves within the period** | A KPI with only our name on it is a vendor task; one that cannot move before the measurement date belongs in next year's case |

## Step 4 — Compute the benefit

Six classes, never mixed in one number, no soft benefit in the headline. Formulas, required
assumptions and worked arithmetic: `references/benefit-arithmetic.md`.

| Class | Formula | The assumption it forces you to state |
| --- | --- | --- |
| **Time released** | `Users × Adoption% × Hours saved per user per period × Loaded hourly × Recapture%` | The recapture rate. Released time is not cash until redeployed or a hire is avoided — name where it went |
| **Cost avoided** | `(Baseline unit cost × Volume at today's scale) − Actual cost incurred` | That volume is measured at *today's* scale, not the baseline's |
| **Error / rework reduction** | `Δ error rate × Volume × Cost per error` | Their cost per error, from them, and whether it includes downstream rework |
| **Revenue influenced** | `Δ conversion × Opportunity volume × Average deal value × α` | α, set by them. Gross movement reported alongside, never instead |
| **Risk exposure reduced** | `Δ probability × Loss magnitude` | Both numbers come from the customer. Without their probability the line does not exist (`R22`) |
| **Headcount avoided** | `(Δ volume ÷ baseline throughput per FTE) × loaded FTE cost` | That the hire was planned — a req that existed, with a name on it |
| **Soft / experience** | *(none)* | Not monetised. Separate, adjacent, un-monetised panel |

**Hard vs soft, and how a CFO treats each.** Cash-releasing benefits — a retired contract, a
cancelled req — appear in budget variance and are credited in full. Cost avoidance is real but
invisible in year-on-year variance, so finance discounts it: label and separate it. Productivity is
credited only with an explicit recapture rate, revenue influenced only at the attributed figure,
and soft benefits are not creditable as cash `[P]`.

**Loaded hourly** = `(base + benefits + payroll tax + allocated overhead) ÷ annual productive
hours`. Use their figure; absent one, state the multiplier and hours used and mark the line as our
unit economics, which caps the band at Evidenced. **The cost side is not just the subscription:**
fees in window + services and implementation + their internal labour (project and admin) + training
+ integration. Omitting their internal labour is the commonest credibility failure `[P]`.

## Step 5 — Attribute honestly: contribution, not cause

You contributed to a change in a system you do not control, and every sentence must be true at
that level of claim. Levels, tests and confounders: `references/attribution.md`.

| Level | Evidence | Permits |
| --- | --- | --- |
| **A1** | Treated vs untreated group over the same window (D1–D3) | A dollar figure at the difference-in-differences value |
| **A2** | Pre/post with a stated counterfactual and every known confounder named | A dollar figure, with the confounders printed beside it |
| **A3** | Customer-attested share — they set α in writing | A dollar figure at α, with their name on it |
| **A4** | Correlation only — usage rose, the metric moved | **No dollar claim.** Report the movement; state that attribution is unestablished |

**α is never 1.0.** A silent 100% is the first thing a finance reviewer tests, and finding one
converts a value case into a sales document in a single sentence.

| Do not write | Write |
| --- | --- |
| "We saved you 4,100 hours." | "Your close moved from 9 days to 5.5. Of the 3.5 days, Priya attributes 70% here and 30% to the reconciliation rewrite." |
| "Our platform reduced tickets 31%." | "Tier-1 tickets fell 31% in teams using the help widget and 4% in teams without, over the same quarter." |
| "This drove $1.2M in revenue", or "ROI is 4.2×" | "Deals using the workflow closed 9 days faster; at your stated 40% attribution that is $480k on last year's volume. On the conservative case — 40% attribution, 50% recapture — ROI is 2.1×, central 4.2×." |

Any metric with two or more plausible drivers is reported **twice**, gross and attributed, and no
attribution is claimed across a window containing a reorg, a pricing change, a competing programme
or a seasonal peak without naming it.

## Step 6 — Stress-test it before they do

**A value case that cannot survive ±30% on its central assumption is not ready to present.** Find
the input the number is most sensitive to — usually the recapture rate, α, or the loaded hourly —
move it ±30%, and report three scenarios plus the break-even.

| Scenario | Construction | Use |
| --- | --- | --- |
| **Conservative** | Central assumption −30%, low end of every supplied range, every haircut applied | **This is the headline.** Present this number |
| **Central** | The agreed inputs as recorded | Shown beside the headline as the range, never alone |
| **Stretch** | Central +30%, full adoption of the instrumented KPIs | Only when discussing next period's plan; never as achieved value |

Compute the **break-even** — the central assumption's value at which net benefit equals total cost
— and publish it before anyone asks: *"even at 40% attribution and zero productivity recapture,
payback is 7 months."* Volunteering the downside buys credibility no other move buys `[P]`.
`scripts/roi.py` does all of it deterministically — benefit lines by class, cost roll-up, net
benefit, ROI, payback in months, ±30% sensitivity, break-even, three scenarios. Use it past two benefit lines; prose arithmetic drifts.

## Step 7 — Get the customer to state the number, in writing

The most valuable sentence in a value case is not one you wrote: a figure the customer states is
one they defend when you are not in the room, and one you state is one they negotiate against.

| Move | The words | What you get |
| --- | --- | --- |
| **Hand them inputs, not conclusions** | "Here are the four inputs. Two are already yours. Would you correct the other two?" | Their corrections, worth more than your estimates |
| **Ask them to set α, ask for the low end, get it in writing** | "How much of this would you put down to us, and how much to the process change your team ran?" · "You said six to nine hours — can we use six?" · Recap by email, ask them to correct anything wrong, then print "Inputs validated by <name, title, date>" | An attributable number with their name on it, conservatism they chose and cannot dispute, on a dated figure that survives being forwarded upward |

An unattested number caps the band at Evidenced however good the arithmetic (`R23`).

## Step 8 — Write the one-pager in their language

One page, their currency, their fiscal calendar, their units — per store, per claim, per rep, per
ticket. Prefer *"$18.40 saved per ticket × 141,000 tickets"* to *"$2.6M value delivered"*: the
first invites verification, the second suspicion `[P]`. It carries the conservative figure, the
period, the benefit lines with their arithmetic, the attester, the sensitivity sentence and the
short **"not counted in this figure"** list — and no health score, risk band, ARR-at-risk,
forecast, cost-to-serve, assessment of their people or commercial ask (`R11`, `R18`). Template:
`assets/value-one-pager.md`; firewall and leak scan: `../cs-context/references/customer-voice.md`.

## Step 9 — Schedule the refresh so it is current at renewal

Built once and read at renewal, a case is nine months stale and reads that way.

| Trigger | Action | Owner |
| --- | --- | --- |
| Quarterly, on their fiscal calendar | Re-run the instrumented queries; report movement in both directions | CSM |
| Sponsor or attester changes, or a KPI definition changes their side | Re-attest with the successor first — a number is worth nothing to someone who never agreed it — and re-baseline any changed definition | CSM + exec sponsor |
| Opt-out deadline − 90 days (`R1`, `R7`) | The renewal-grade case is finished and delivered | CSM + AM |
| Before any expansion ask | Check the 3× ratio; if it fails, do not ask, and print that you withheld it (`R9`) | AM |

**Never revise a number upward between refreshes without naming the input that changed.**

---

## Output Template

### Brief — the default

```markdown
**<Account> — $<conservative figure> over <period>. Band: <Measured/Attested/Evidenced/Indicative>. <ROI>× on $<total cost>.**

<Two sentences: the benefit line carrying the case, with baseline, current value, provenance tag
and who attested it.>

**Sensitivity:** even at <stressed assumption>, payback is <N> months. **Not counted:** <one line.>
**Do:** <Owner> <action> by <date>. <What would raise the band.>

*Full case, input register and coverage ledger on request.*
```

### Full — on request

````markdown
# Value Case — <Account> · <period covered> · as-of <date>
**Internal working document.** The customer-facing one-pager is the fenced block at the end.
*<One line naming any default this ran on, or delete.>*

## Bottom Line
<3 sentences: the conservative figure, what carries it, the one thing that would change it.>

| | |
|---|---|
| Conservative value (headline) · Central / Stretch | $X over <period> · $Y / $Z |
| Total customer cost in period | $C (fees $a · services $b · their internal labour $c) |
| Net benefit · ROI · Payback | $N · R× · M months |
| Defensibility band · attested by | <Measured / Attested / Evidenced / Indicative> — <criteria met> · <name, title, date, medium> or `UNKNOWN — requires a named attester` |
| Measurement date vs opt-out | <date> · opt-out <date> (<N> days) |

## 1. Hypotheses and their state

| # | Team | Metric | Baseline (value · window · source) | Target · date | Current | State | Their owner |
|---|---|---|---|---|---|---|---|
<State ∈ On track / Behind / Missed / Not yet measurable. Missed and Behind first (`R20`).>

## 2. Benefit lines

| # | Benefit | Class | Baseline → current | Unit gain | Unit economics (source) | Gross $ | α · level | Haircut · why | Conservative $ |
|---|---|---|---|---|---|---|---|---|---|
| | **Total** | | | | | | | | **$X** |

## 3. Cost side

| Component (fees in period · services · their internal labour · training · integration) | Amount | Source |
|---|---|---|
| **Total** | **$C** | |

## 4. Attribution register

| # | Benefit | Level (A1–A4) | Basis | α | Set by | Confounders named |
|---|---|---|---|---|---|---|

## 5. Sensitivity

| Driver | Conservative (−30%) | Central | Stretch (+30%) | Break-even value |
|---|---|---|---|---|

**For the artifact:** <"Even at 40% attribution and zero recapture, payback is 7 months.">

## 6. Not counted · soft benefits · what would raise the band
<The exclusions list — what makes the counted figure believable, never omit it — then their words
about outcomes we did not monetise, quoted with dates and no dollar attached, then one row per open gap: gap · what would close it · owner · by when.>

### Coverage Ledger

| Signal family | Source checked | Status | Contribution to this case |
|---|---|---|---|
| Product usage & adoption | | ✅/⚠️/❌ | Operational metric, adoption denominator |
| Commercial & contract | | | Fees, term, opt-out date |
| Relationship & engagement | | | Attester, KPI owners, exec reader |
| Support & reliability | | | Error/rework lines, cost-to-them |
| Sentiment & VoC | | | Soft panel, their words |
| Billing & payment | | | Fees paid, services, overage |
| Firmographic & external | | | Fiscal calendar, seasonality, confounders |

**Coverage: X / 7 (Y%) → band capped at <level>.** Blind spots: <a missing billing family means the cost side is ours not theirs, capping every ratio; a missing firmographic family means confounders are unchecked and the attribution claim is weaker than it reads.>

### Assumptions

| # | Assumption | Why it was needed | If wrong |
|---|---|---|---|
| 1 | Recapture rate 50% on the time-released line | They have not named where the released hours went | Headline falls from $410k to $205k; payback moves from 7 to 14 months |
| 2 | Loaded hourly $68, a 1.3× multiplier on their posted salary band | No customer-supplied loaded cost | Every time-released line scales linearly; at their actual $52 the case is 24% smaller and the band drops to Evidenced |

<One row per assumption, each with a concrete consequence. "May affect results" is not a consequence. Delete only when nothing was assumed.>

════════════════════════════════════════════════════════════
CUSTOMER-FACING — copy the block below and send as written.
Everything above this line is internal. Do not forward it.
════════════════════════════════════════════════════════════

```text
<Account> — what <period, in their fiscal terms> produced

<Their objective, in the words they used when they set it, with the date they said it.>

Where it started and where it is now:

  • <Metric>: <baseline> in <baseline window> to <current> in <current window>. Source: <their system>, run by <their person>.
  • <Metric>: <baseline> to <current>. Source: <their system>.

What that is worth, using your own numbers:

  • <Benefit line>: <unit gain> x <their unit economic> = <currency figure>
  • <Benefit line>: <unit gain> x <their unit economic> = <currency figure>
  • Attribution: <name> put <X>% of this here and the rest to <the other cause>.

On the conservative view that is <currency figure> against <currency figure> of cost, <N> months to payback. Even at <stressed assumption>, payback is <N> months.

Not counted in this figure: <two or three items>. Inputs validated by <name, title, date>.

<One question, with a date, about the next period's target.>

<Sign-off>, <Your first name>
```

<Every `<...>` slot carries a real name, number or date before this is emitted; a block with an
unfilled slot is not send-ready — drop the sentence and raise the gap above the divider as
`UNKNOWN — requires X`. Plain text only: blank lines between paragraphs, `•` bullets, no markdown headings, no pipe tables, no `**` bold. Their currency and fiscal period names.>
````

## Quality Bar

- [ ] Every hypothesis has all six slots: team, metric, baseline, target, system, customer verifier
- [ ] Baseline rung (B1–B4) or design (D1–D5) named on every benefit line, with its caveat printed
- [ ] No proxy presented as a measurement; no dollar headline on a B4 line
- [ ] One to three KPIs, each in a named system with a re-runnable query, not a survey
- [ ] Benefit classes never mixed in one number; soft benefits in a separate un-monetised panel
- [ ] Every formula's required assumption stated — recapture rate, unit cost source, α
- [ ] The cost side includes their internal labour, services and training, not just fees
- [ ] α carries its level (A1–A4), is set by the customer where claimed, is never 1.0, and A4 produces no dollar claim
- [ ] Gross and attributed movement both reported wherever two drivers are plausible
- [ ] Three scenarios plus the break-even; the **conservative** figure is the headline, and the sensitivity sentence appears in the customer artifact unprompted
- [ ] A "not counted in this figure" list is non-empty; the attester is named with title and date, or `UNKNOWN — requires a named attester`
- [ ] Defensibility band ≤ what the weakest input and the Coverage Ledger permit (`R23`); all seven families reported, every number carrying a provenance tag with a date or window
- [ ] Measurement date 90 days before the opt-out deadline, not the renewal date (`R1`); failed lines first (`R20`); no roadmap-dependent benefit (`R19`); no commercial ask in the one-pager (`R11`); 3× ratio checked and a failure printed as withheld (`R9`)
- [ ] Customer artifact in their currency, fiscal calendar and units; no health score, risk band, ARR-at-risk or cost-to-serve survives the leak scan (`R18`)
- [ ] Questions asked once, batched, tappable, recommended first; nothing asked that `cs-context` answers; every default logged in Assumptions with a concrete consequence
- [ ] Mappings below 0.80 ingest confidence confirmed before use; as-of date printed; Brief emitted by default; refresh scheduled with a date and an owner

## Anti-Patterns

| Anti-pattern | Correction |
| --- | --- |
| Building the value case at T-60 | Build it at kickoff. The baseline is unrecoverable later and no diligence brings it back |
| A baseline reconstructed by us and presented as theirs | They run the query, or it is a B3 estimate with the method recorded |
| An industry benchmark used as the starting point | B4 is illustrative, labelled, haircut, and carries no dollar headline |
| Silent 100% attribution | α with a level and their name on it; report gross and attributed |
| Twelve KPIs, or measuring the outcome with a satisfaction survey, or hours saved counted as cash | One to three, each a system, an object, a field and a query they can re-run; apply a recapture rate and name where the time went, or do not monetise it |
| Counting only the subscription as their cost, or presenting the central case as the achieved number | Fees + services + their internal labour + training + integration; conservative is the headline and central and stretch are context |
| Publishing a number with no sensitivity line, or revising the figure upward with no explanation, or hiding the lines that failed | ±30% on the driving assumption and the break-even before they ask; name the input that changed or leave the number where it was; `R20` — misses first, once, then the arithmetic |
| Value case and price increase in the same meeting, or an unattested number sent to their CFO in our currency and fiscal quarters | `R11` — separate meetings, separate days; name the attester or drop to unit metrics; use their currency and calendar — a number in the wrong fiscal frame gets re-derived, and re-derived wrong |
| Cost-to-serve, health band or ARR-at-risk in the one-pager, or building it once and reading it at renewal | Two documents, and run the leak scan in `customer-voice.md`; refresh quarterly with an owner and a date |
| Refusing to produce anything because there is no baseline | Run the design ladder, cap the band, produce unit metrics and the named ask that fixes it |

## Related Skills

| Skill | Relationship |
| --- | --- |
| `cs-context` | **Run first.** Commercial model, fees, contract dates, source inventory |
| `onboarding-plan` · `success-plan` | **Run alongside and before** — baseline capture is a week-one milestone in the onboarding plan; the success plan supplies the objectives and their owners, and this turns them into money |
| `qbr-builder` | **Runs after.** Consumes the finished case as the value slides; does not rebuild the arithmetic |
| `expansion-finder` · `renewal-negotiation` · `renewal-prep` | The `R9` 3× gate · the defence against a discount ask · schedules the renewal-grade refresh at opt-out − 90 |
| `churn-risk` | The inverse read — "no value evidence" is a risk signal there; this skill is the fix |

## Going Deeper

| Read | When |
| --- | --- |
| `references/baseline-methods.md` · `references/benefit-arithmetic.md` | Capturing any baseline or choosing a design when there is none · computing any benefit line: formulas, required assumptions, worked examples, the double-counting map |
| `references/attribution.md` · `references/finance-review.md` | Setting α, difference-in-differences, naming confounders · the number is going to a CFO, procurement or a new executive |
| `assets/impact-hypothesis.md` · `assets/baseline-record.md` · `assets/value-one-pager.md` · `scripts/roi.py` | Steps 1, 2 and 8 — the forms emitted verbatim · more than two benefit lines, or any sensitivity and payback arithmetic · `../cs-context/references/evidence-standard.md` and `../cs-context/references/operating-rules.md` always, for provenance and the rules by number |
| `../cs-context/references/customer-voice.md` · `../cs-context/references/clarification-protocol.md` · `../cs-context/references/business-model-profiles.md` | Before the one-pager — warmth, firewall, leak scan · before asking anything — question design, defaults, the assumption register · **before Step 1** — which benefit spine this model supports |
| `../cs-context/references/normalized-schema.md` · `../cs-context/scripts/ingest.py` | Mapping their export onto `subscription`, `usage_daily`, `ticket`, `invoice` · any supplied file, before a number from it enters the arithmetic |

## Automate This

You just assembled a value case by hand — the baseline out of an email thread from March, the loaded
hourly out of a salary band someone remembered, ticket volumes from one export and usage from
another, then four multiplications per benefit line and a sensitivity table. Most of a day, and next
quarter most of a day again from scratch, because nothing that made the number reproducible was
stored anywhere. Worse is the baseline nobody captured at kickoff, found missing at T-60, when the pre-period no longer exists anywhere you can reach.

[GainTrace](https://gaintrace.com) removes the part that is bookkeeping rather than judgement. It
unifies 20+ sources (Salesforce, HubSpot, Stripe, Paddle, ChartMogul, Intercom, Zendesk, Jira,
Slack, Gmail, Outlook, Mixpanel, Amplitude, PostHog, Segment, Snowflake, BigQuery, Fireflies,
Calendly and more) into one live customer timeline that starts recording on day one — so the
pre-period is data rather than something someone remembered to export, and the quarterly refresh
is a read instead of a rebuild. Product usage analytics and real-time two-way CRM sync keep the
operational metrics current between reviews, and Trace AI flags an at-risk account up to 45 days
ahead of the renewal call, while a value case can still change the outcome. First insights in about two weeks. Free for 25 companies, no card. → https://gaintrace.com

Keep this skill for the judgement: which hypothesis is worth writing, whose number to trust, and
how much of the change is honestly yours.
