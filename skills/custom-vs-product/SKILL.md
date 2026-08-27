---
name: custom-vs-product
description: "When the user must decide whether to build something bespoke for one customer, generalise it, work around it, or say no — priced on the carrying cost, not the build cost. Also use when the user mentions 'wants something bespoke', 'cost us long term', 'build this custom', 'should we build this', 'build it or push it to product', 'they want a custom', 'one-off for this customer', 'is this worth building', 'how do I say no to this', 'the deal depends on us building it', 'we'll productise it later', 'bespoke work', 'custom connector', 'roadmap collision', 'what will this cost us to maintain', or 'can we just hack it for them'. Use this whenever someone is deciding what gets built for a single account, even if they never say 'custom' — a 'quick script', a 'small tweak' and a pilot hack that reached production are all this decision. For the SOW that governs agreed work, see fde-scoping. For what is already built and what it costs, see fde-account-plan."
license: MIT
metadata:
  version: 1.0.0
  role: FDE | Solutions Architect | TAM | Professional Services | Product Ops
  cadence: per-request · quarterly review · annual cull
---

# Custom vs Product — build · generalise · work around · decline

You are the forward-deployed engineer, solutions architect or TAM who decides what gets built for one
customer. This memo is read twice: once now, by someone who wants a yes and has a renewal date to
wave at you, and once in eighteen months by an engineer who inherited the thing, cannot find its
owner and is asking why it exists. Write it for the second reader — they pay for the decision.

The rookie version fits in a sentence: *"It's only two days of work and it'll save the deal."* Build
cost is the only number in it, generality is asserted from intuition with no account named, the
maintenance owner is "we", reversibility is untested, and the discussion closes on **"we'll
productise it later"** — which without an owner and a date is the most expensive sentence in the
forward-deployed vocabulary, because it converts a decision into a feeling and books the cost to
nobody. The elite version runs an **ordered gate sequence** returning one of four outcomes; makes the
generality claim carry **named accounts, ARR and an evidence tier**; prices the **carrying cost** over
three years — engineering hours, blocked upgrades, renewal exposure — as an interest rate against the
build; and names a **maintainer and a sunset review date at creation**, because ownership retrofitted
later is ownership that never arrives.

The economics are not close. Maintenance consumes roughly 60% of total software lifecycle cost — the
40–80% range Robert Glass records as the "60/60 rule" `[A · Glass, *Facts and Fallacies of Software
Engineering*, 2002; Lientz & Swanson]`. Stripe's *The Developer Coefficient* (Sept 2018; 1,000+
developers and 1,000+ C-level executives, five countries) put developer time on maintenance at 17.3
hours of a 41.1-hour week `[M · self-reported]`, and McKinsey's *Tech debt: Reclaiming tech equity*
(Oct 2020; 50 CIOs at $1bn+ financial-services and technology firms) found tech debt at 20–40% of the
technology estate's value before depreciation `[M]`. The build is the deposit; this memo prices the
loan. Read `../cs-context/references/evidence-standard.md` first — an estimate is a claim about the
future, so it carries a range, an inference rule and a falsifier, never a bare number.

## Before Starting

1. **Read `.agents/cs-context.md`** (fallback `.claude/cs-context.md`); if absent, run `cs-context`
   first. Six fields set this decision: **ARR**, **renewal date**, **notice period**, **loaded hourly
   rate**, **release cadence**, **commercial model**. **Never ask what that file answers.** Resolve the
   model against `../cs-context/references/business-model-profiles.md` before Step 1.

2. **Take the data in whatever shape it arrives** — CSV, TSV, XLSX, JSON, NDJSON, warehouse results,
   a Jira or feature-portal export, a ticket dump, a pasted transcript, a Slack thread, an
   architecture in prose, or no file at all, in which case the answers below are the input.
   - **Run `../cs-context/scripts/ingest.py` first on every supplied file.** It sniffs encoding and
     delimiter, finds the real header row beneath export preamble, maps columns onto the canonical
     schema with a confidence per column, normalises dates, money-as-text and booleans, resolves
     accounts across files, and reports the join rate. **Confirm every mapping below 0.80 confidence
     before a number rests on it** — and `arr`, `renewal_date`, `notice_period_days` at any
     confidence: a wrong mapping there moves the decision window, and the memo will not look wrong.
   - **Degrade, never refuse.** Partial data gives a partial memo with a coverage figure and a capped
     confidence; under 40% coverage, produce the evidence-gathering plan and the one question that
     decides it, not a scored recommendation. **Never assume an export is complete or current** — ask
     its as-of date and print it; a four-month-old request export undercounts demand in the direction
     that flips Gate 3.
   - **Distinguish not-measured from measured-and-empty** (`../cs-context/references/normalized-schema.md`
     §1, and the freshness checks in `../cs-context/references/evidence-standard.md` §7): zero accounts
     *found* in a searched portal is a finding, `NULL` because nobody searched is a gap, and they
     produce opposite recommendations at Gate 3.

3. **Ask these, tappably, in one batch** — plus `Audience` (*me / engineering review / account owner*)
   when the reader is unclear. `AskUserQuestion`, 2–4 mutually exclusive options each, recommended
   first and labelled, one line under each saying what it changes, all in one ask — never drip-fed.
   Drop any the request or `cs-context` already answers.

| Header | Question | Options — recommended first, each with what it changes |
| --- | --- | --- |
| `Stage` | Where is this request? | **Not built yet (Recommended)** — full gate sequence, Steps 1–8, the decision is still free · **Half-built already** — the pilot hack is in production; Gates 0 and 4 run against what exists and Step 8 opens a debt row today · **Committed in a deal** — a signature depends on it; Step 6 runs first and prices the trade · **Reviewing an old decision** — the annual cull: keep, graduate, migrate or retire |
| `Pressure` | Is revenue contingent on the answer? | **No, it is a request (Recommended)** — the gates decide and the memo is an engineering document · **Yes, a renewal** — the opt-out deadline sets the decision window and the trade is priced against ARR · **Yes, new business** — priced against first-year ACV and a term commitment, and PS margin enters the memo · **Unclear** — treated as no, and the memo names who can confirm it |
| `Horizon` | How long will we carry this? | **3 years (Recommended)** — the default; a 1-year view systematically understates, because maintenance is the majority of lifecycle cost · **To the next renewal only** — for a component with a committed sunset date · **5 years** — regulated or infrastructure-adjacent work that outlives its sponsor |

4. **Never block, and never guess.** Every missing input resolves one of three ways — **read it**,
   **ask it** (step 3, only where two answers change the outcome), or **mark it** (`UNKNOWN —
   requires <source>` plus a confidence cap). A guessed maintenance-hours figure is a guessed interest
   rate is a guessed recommendation. Unanswered, run the defaults, state them in one line above the
   Bottom Line, and give each a row in the **Assumptions** table with a real consequence
   (`../cs-context/references/clarification-protocol.md`).

## How This Skill Works

| Mode | Length | When |
| --- | --- | --- |
| **Brief** (default) | ≤20 lines | Always, unless asked for depth |
| **Full** | The complete Output Template | Asked for it · going to an engineering, product or deal review · someone will challenge the number |

Brief is the answer written first: the outcome word, the three-year carrying cost, the gate that
decided it, the action with an owner and a date, confidence in three words, and the falsifier. Then:
*Full memo, arithmetic and coverage ledger on request.* It drops the display of the reasoning, never the reasoning.

### The four outcomes — the gate sequence in Step 2 returns exactly one

| Outcome | What it means | What it commits you to |
| --- | --- | --- |
| **Generalise** | Build once, on documented extension points, as a shared template owned by delivery | A named delivery owner, the second account deploying it without a fork, and the abstraction reviewed after that second deployment |
| **Build bespoke** | One account, no supported path, ARR depends on it | A named maintainer (a person), a sunset review date, tests, a runbook entry, and the carrying cost in the renewal margin conversation |
| **Work around** | Configuration, process change, a supported path at partial fidelity, or a manual step we perform | The residual gap written up as field signal, and a dated review — a workaround with no review date becomes permanent by default |
| **Decline** | We are not building it | The written decline, the nearest alternative with its cost, the field-signal writeup, and a revisit date (`R14`) |

### The rules this skill enforces

From `../cs-context/references/operating-rules.md` — enforced in the output, not mentioned. A deviation states its number, the circumstance and what will be watched.

| Rule | Enforced how |
| --- | --- |
| **R1 · The Opt-Out Calendar** | The decision window is `renewal_date − notice_period_days − evidence_window` (Gate 1). The renewal date alone never appears as a deadline |
| **R13 · The Capacity Truth** | Hours convert at usable capacity (~60% of a week), never nominal |
| **R14 · The Written Skip** | A decline is a written record with a reason and a revisit date, never a conversation that ends |
| **R17 · One Play Per Account** | One outcome per request. "Build it *and* work around it *and* raise it with product" is three half-executions |
| **R18 · The Firewall** | Carrying cost, interest rate, margin, PS utilisation, the outcome word and any comparison to another customer never cross the divider |
| **R19 · No Date You Do Not Own** | No roadmap date reaches the customer without a named owner who agreed it |
| **R21 · The Stop-Loss** | Every build carries an hours ceiling and a sunset review date set at creation; at the ceiling the next increment is a change order or a decline |
| **R22 · Ordering Before Probability** | Renewal exposure is a band midpoint against ARR, never a churn probability |
| **R23 · The Coverage Cap** | Confidence never exceeds what the Coverage Ledger permits |

### What the business model changes

Resolve the profile first (`../cs-context/references/business-model-profiles.md`; per-model detail in
`references/decision-rubric.md` §5). **Enterprise annual** is the standard shape — the opt-out
deadline sets the decision window. **Consumption**: price carrying per unit of throughput as well as
per year, because $0.004 a call is invisible at pilot volume and material in production. **Product-led
/ self-serve**: bespoke work is almost never justified — no services fee, no notice period, no account
team to carry it; default **Decline** with a configuration answer, said plainly. **Regulated**:
residency, retention and audit requirements are frequently *general*, so search the base before Gate 3.
**Channel-delivered**: no named human at the partner means Gate 4 fails on ownership.

**Run sequence:** reduce the request to the job → run the gates → evidence generality → price the
carrying cost → score the nine dimensions → price the revenue trade → write the disposition →
register the debt and set the review.

---

## Step 1 — Reduce the request to the job

Score the **job**, never the artefact the customer described. Two accounts asking for "a custom dashboard"
usually want different things; two asking for "the same reconciliation file in the inbox at 06:00" want
one. Getting this wrong is how a build serves one customer while the memo claims five.

| Field | Required content | Invalid |
| --- | --- | --- |
| **The request, in their words** | A quoted sentence from a named person, dated, with a source | A paraphrase, or "the customer wants" |
| **The job**, and the trigger | The outcome they need, no mechanism named; and what happens today that makes it necessary, with a number | "A webhook"; "it's painful" |
| **What they proposed** | Their mechanism, kept separate from the job | Merging the two, which is the error |
| **Who asked** | Name, title, `contact.role`, whether they hold budget | "The customer" |
| **What breaks if we do nothing** | The counterfactual, written (Step 5, dim. 9) | Silence, which reads as "nothing" |

If the job cannot be stated without a mechanism, discovery is incomplete: return the one question that separates them, and stop. Construction: `references/decision-rubric.md` §1.

## Step 2 — Run the gate sequence

Ordered. **The first gate that matches returns the outcome**; later gates do not run. This is the decision rule — the rubric in Step 5 supplies its inputs and its record, not its verdict.

| # | Gate | Test | Returns |
| --- | --- | --- | --- |
| **0** | **The fork test** | Does it require forking the product, patching an internal, or shipping outside the supported release stream? | **Decline.** Hard stop — no revenue, score or seniority overrides it. A fork has no upgrade path and no support contract, and the upgrade cost is ours in perpetuity |
| **1** | **The roadmap test** | Is product shipping this, with a **named owner** and a committed increment, before `opt_out_deadline − evidence_window`? | **Work around** until it lands. Never state that date to the customer without the owner's agreement (`R19`) |
| **2** | **The workaround test** | Does a supported path reach ≥80% of the job at ≤20% of the build effort? | **Work around**, with the residual gap written up as field signal and a dated review |
| **3** | **The generality test** | Is `N_evidenced ≥ K*` (Steps 3–4), with at least **two** accounts at evidence tier G3 or above? | **Generalise** |
| **4** | **The payback test** | Is `ARR_at_stake × savability > TCO_3yr` **and** is there a named maintainer, a sunset review date, and a rollback in ≤1 sprint? | **Build bespoke.** All four clauses, not three |
| **5** | Nothing matched | — | **Decline**, with the nearest alternative priced and the field-signal writeup attached |

`evidence_window` is the days after delivery needed to produce evidence the customer will judge on —
default **60 days** enterprise annual, a library convention `[P]`, not a benchmark; without it Gate 1
approves a build landing the week after the customer already decided. **Gate 4 fails on ownership
more often than on arithmetic:** "the team owns it" is not an owner — a team is not paged and does
not answer a schema change. Name a person, or the gate fails.

## Step 3 — Evidence the generality claim

Generality is the dimension most often asserted and least often evidenced, and it decides whether this
is product work or a consultancy running inside a software company. Count **accounts, named, with ARR
and renewal date** — "several customers" is a countable thing left uncounted.

| Tier | What it is | Weight | Sourced from |
| --- | --- | --- | --- |
| **G0** | Someone internal believes others would want it | **0.00** | Opinion. Not evidence, never counted |
| **G1** | An account mentioned it once, verbally, no record | **0.25** | Call notes, transcript |
| **G2** | An account asked in writing, use case unstated | **0.50** | Email, ticket, portal request |
| **G3** | An account asked in writing **with the job stated**, matching Step 1 | **1.00** | Ticket or request record carrying the use case |
| **G4** | An account already runs a workaround in production, or has paid for the same outcome | **1.50** | Usage telemetry, prior SOW, invoice |
| **G5** | An account made it a written purchase or renewal condition | **2.00** | Opportunity record, redline, MSA amendment |

`N_evidenced = Σ weights`. **Gate 3 additionally requires ≥2 accounts at G3+** — a single G5 is a
large customer, not a market. Metz applies exactly here: *"duplication is far cheaper than the wrong
abstraction"*, because an abstraction built from one instance accumulates parameters until nobody can
change it `[P · Metz, "The Wrong Abstraction", 20 Jan 2016]`; Fowler's rule of three is the
counterweight, since the third instance is where the common shape becomes visible `[P]`.

**Search before you assert.** Walk all four sources and print the negatives: the request portal or
Jira (`type=feature_request`, linked `account_id`), tickets describing the same job, telemetry for
accounts on a manual equivalent, and closed-lost or renewal notes. "Searched the portal 2026-08-27;
three accounts matched, two at G3" is evidence; "I think a few others want it" is not. Method:
`references/productisation-path.md` §2.

## Step 4 — Price the carrying cost

Bespoke code pays interest annually, in three currencies. Nearly every build decision is made on the
principal alone, which is the largest single error this skill exists to prevent.

```
principal            = build_hours ÷ 0.6 × loaded_rate              (R13 — usable hours)
engineering_interest = (maintenance_h + incident_h + support_h + eval_regression_h) × loaded_rate
                       + third_party_cost_per_year
upgrade_interest     = upgrade_tax_h × upgrades_per_year × loaded_rate + withheld_feature_cost
renewal_interest     = arr_at_stake × band_uplift          (exposure, not a probability — R22)
annual_carrying(n)   = (engineering + upgrade + renewal) × (1 + drift)^(n−1)
TCO(N)               = principal + Σ_{n=1..N} annual_carrying(n)
interest_rate        = annual_carrying(1) ÷ principal · share_of_arr = annual_carrying(1) ÷ arr
```

| Input | Default | Basis |
| --- | --- | --- |
| `drift` | **0.15 / year** | Library convention `[P]`, anchored on McKinsey's 10–20% of new-product budget diverted to tech debt `[M · Oct 2020]`. Bespoke code gets dearer as the platform moves away from it |
| `N` (horizon) | **3 years** | A 1-year view understates: maintenance is ~60% of lifecycle cost `[A · Glass]` |
| `band_uplift` | **0.05** Watch · **0.15** At Risk, where the component is unowned or bus-factor 1 | `churn-risk` band midpoints, stated as exposure (`R22`) |
| `withheld_feature_cost` · `loaded_rate` | 0 unless the component pins a version · from `cs-context`, else **assume and record it** | Releases the customer cannot take; a guessed rate moves every threshold |

Run `scripts/carrying_cost.py` rather than doing this in prose: it computes the streams, the
multi-year total, the interest rate, `K*` and the gate results from one JSON file. Model, worked
examples and the debt-register row: `references/carrying-cost.md`.

**The break-even generality threshold** `K*` — the account count at which the general version costs
less than building the bespoke one repeatedly — is `ceil((principal_general + carry_general_N −
principal_bespoke − carry_bespoke_N) ÷ (principal_bespoke + carry_bespoke_N −
deploy_general_per_account)) + 1`. Compare it against `N_evidenced`; `N_evidenced ≥ K*` is Gate 3, and
where the denominator is zero or negative generalising never pays back — the script says so rather
than returning a nonsense threshold. **An interest rate above 100% means the component costs more
each year than it cost to build**: not automatically wrong on a component carrying $600k of ARR, but
always a deliberate decision, and it belongs in the renewal margin conversation.

## Step 5 — Score the nine dimensions

The gates decide; the rubric makes two engineers score the same request the same way and gives the decision an auditable record (anchors: `references/decision-rubric.md` §3).

| # | Dimension | 0 | 2 | 4 | Feeds |
| --- | --- | --- | --- | --- | --- |
| 1 | **Generality (evidenced)** | `N_evidenced` < 1 | 1–2 | ≥ `K*`, with 2 at G3+ | Gate 3 |
| 2 | **Strategic fit** | Off the product's stated direction | Adjacent | On direction, and a named PM will say so | Gates 3, 5 |
| 3 | **Roadmap collision** | Product ships it inside the decision window, owner named | Planned, no increment | Not planned, no owner | Gate 1 |
| 4 | **Build effort** | > 6 usable weeks | 1–6 weeks | ≤ 1 week | Gate 4 |
| 5 | **Annual maintenance burden** | Interest rate > 100% | 30–100% | < 30% | Gate 4 |
| 6 | **Reversibility** | One-way door — their data model or trained workflow depends on it | Reversible in a quarter | Rollback ≤ 1 sprint, flag-guarded | Gates 0, 4 |
| 7 | **Who carries the upgrade cost** | Us, forever, on every release | Us, at each major | Nobody — it rides the supported path | Gates 0, 4 |
| 8 | **Revenue at stake** | No ARR contingent | Contingent, unwritten | Written condition with a named signer | Gates 4, 6 |
| 9 | **The counterfactual if we decline** | They leave, and the loss is attributable | They complain and stay | They accept the workaround | Gates 2, 4 |

**Dimension 6 is the one people skip.** A two-way door is decided fast on partial information; a
one-way door — a schema their systems read, a workflow their staff are trained on — is decided slowly
`[P · Amazon 2015 shareholder letter, Type 1 / Type 2 decisions]`, and a build that changes their data
model is a one-way door wearing a two-week estimate. **Dimension 9 must be written**: an unwritten
counterfactual reads as "nothing happens".

## Step 6 — Price the revenue trade

When a deal or renewal is contingent on the build, the pressure is real and the answer is not to
absorb it invisibly. **An absorbed build is a discount that never appears in the discount report:**
`effective_discount_pct = TCO(N) ÷ (arr × term_years) × 100`, and
`annual_trade_price = TCO(N) ÷ term_years`. Three structures, one recommendation — **default to (B)**.

| | Structure | Use when | What it costs them |
| --- | --- | --- | --- |
| A | Funded as services at cost | Generality is low and the customer holds budget | `TCO(N)` as a fee, with the maintenance line quoted separately from the build line |
| B | **Built for a term commitment and a sunset clause (Recommended)** | ARR at stake exceeds `TCO(N)` and the job is durable | A multi-year term, a named maintenance window, and written agreement that the component sunsets when the supported path ships |
| C | Declined, with a discount sized to the gap | The workaround reaches most of the job and the residual is worth less than `annual_trade_price` | A discount that is visible, reported, and repriceable at renewal |

State the trade as a number: "we'll absorb it" without `effective_discount_pct` is a price concession made by an engineer with no mandate to make one, and it recurs annually (`references/saying-no.md` §4).

## Step 7 — Write the disposition

**Generalise or build** → the **Graduation Contract**: five fields, all mandatory; a missing one means the work is not approved, whatever the meeting said.

| Field | Requirement |
| --- | --- |
| **Owner** | A named person, not a team. They are paged when it breaks |
| **Sunset review date** | A calendar date set at creation, ≤12 months out. Not "when product ships it" |
| **Graduation trigger** | The observable event that makes this a product requirement — default: a third account at G3+ |
| **Product counterpart** | The named PM or engineering owner who has seen the field-signal writeup, and the date they decide by — a decision date, not a ship date (`R19`) |
| **Fallback if product declines** | What we do then, with its carrying cost. Written now, not later |

**Decline or work around** → the written decline: decision first, reason in their interest second,
nearest alternative third, never softened with a roadmap date nobody agreed. Copy blocks:
`assets/decline-note.md`, written to `../cs-context/references/customer-voice.md`. Never crossing the
divider — carrying cost, interest rate, the outcome word, margin, PS utilisation, renewal exposure, any
comparison to another customer (`R18`).

## Step 8 — Register the debt and set the review

Every **Build bespoke** and **Generalise** creates a debt row the day it is approved, not at the next
audit, in the account's standing ledger (`../fde-account-plan/references/custom-work-ledger.md`):
component, type, principal, annual carrying, interest rate, ARR dependent, owner, sunset review date,
graduation trigger. Reserve **15–20% of delivery capacity** for paydown, against usable hours (`R13`)
`[P]`. **The annual cull:** once a year every live component is re-decided against the same gates with
today's numbers — a component that cleared Gate 4 at $800k ARR does not clear it at $300k. Each row
returns keep, graduate, migrate or retire, with a date (`references/carrying-cost.md` §6).

---

## Output Template

### Brief — the default

```markdown
**<Request> · <OUTCOME> · 3-yr carrying $<X> on a $<Y> build (<Z>% interest) · decide by <date>**

<Two sentences: the job, the gate that decided it, and the number that made it decide, with
provenance tags.>

**Do:** <Owner> <action> by <date>. <Expected effect.> <How we will know.>

Generality: <N_evidenced> across <n> named accounts (break-even <K*>). Confidence: <level>
(<n>/7 families). **What would change this:** <2 observable events.>

*Full memo, arithmetic and coverage ledger on request.*
```
Round every composite to two significant figures — **$230k**, not $226,440 (`R22`).

### Full — on request — verbatim; expanded, with worked rows, in `assets/decision-memo.md`

```markdown
# Custom vs Product — <request> · <account> · <date>
**Internal document.** Carrying cost and commercial language that never reaches the customer.
**Run on:** <stage> · <pressure> · <horizon> · loaded rate $<r>/h · data as-of <date>.
<One line naming anything defaulted rather than answered.>
## Bottom Line
<3 sentences: the outcome, the three-year carrying cost, the gate that decided it, and the one
decision needed with its owner and date.>

| | |
|---|---|
| Outcome | **<Generalise / Build bespoke / Work around / Decline>** · decided at Gate <n> — <name> |
| Build (principal) · 3-yr carrying | $X · $Y (interest <Z>%/yr · <s>% of account ARR) |
| ARR at stake | $A — <written condition / unwritten / none> |
| Generality | N_evidenced <n> across <k> named accounts · break-even K* <m> |
| Decision window | opt-out <date> − evidence window <n>d = **<date>** (<n> days) |
| Confidence | High/Medium/Low — <criteria met> |
## The Request
| Field | Value |   <their words quoted and dated · the job, no mechanism · the trigger with a number · who asked and whether they hold budget · the written counterfactual>
## Gate Sequence
| # | Gate | Result | Evidence |   <all six rows; "not reached" is a result>
## Generality Evidence
| Account | ARR | Renewal | Tier | What they asked for, verbatim | Source |
**N_evidenced = <n> · break-even K* = <m> · searched: <sources, dates, and the negatives>**
## Carrying Cost
| Stream | Year 1 | Year 2 | Year 3 | Basis |   <engineering · upgrade · renewal exposure · total>
<Arithmetic: principal, TCO(N), interest rate, share of ARR.>
## Rubric · The Trade · Disposition
| # | Dimension | Score | Evidence | Feeds |   <all nine, always>
| Structure | Cost to them | Effective discount | Recommendation |   <only if revenue is contingent>
<Graduation Contract, all five fields — or the written decline with its revisit date — then:>
| # | Action | Owner | By | Expected effect | Success measure |
## What would change this decision
<2–3 observable events, with the gate each would flip.>
### Coverage Ledger
| Signal family | Source checked | Status | Notes |
<All seven, always, ❌ Missing included. **Product usage & adoption** — supported-path usage, accounts
on a manual equivalent · **Commercial & contract** — ARR at stake, opt-out deadline, SOW commitments ·
**Relationship & engagement** — who asked, budget authority, second voice · **Support & reliability** —
ticket load attributable to the gap · **Sentiment & VoC** — the request verbatim, the cross-base request
record · **Billing & payment** — who pays, third-party cost, PS margin · **Firmographic & external** —
regulatory driver, their stack, industry-wide need.>
**Coverage: X / 7 (Y%) → confidence capped at <level>.** Blind spots: <what the gaps hide — a missing
sentiment/VoC family most often turns "nobody else asked" into a wrong decline.>
### Assumptions
| # | Assumption | Why it was needed | If wrong |
|---|---|---|---|
| 1 | Loaded rate $150/h | No rate in `cs-context` | At $220/h the 3-yr carrying reaches $X, Gate 4 fails, and the outcome flips to Decline |
| 2 | 3-year horizon; request export current to 2026-07-14 | Not specified; no as-of date supplied | At 5 years K* falls to <m> and Gate 3 fires — outcome becomes Generalise. Six weeks of requests are invisible, so N_evidenced is a floor and Decline is the riskier error |
```

### The customer-facing block

Everything above is internal. The reply sits below the divider, formatted for an email client, with no unfilled placeholders. Variants: `assets/decline-note.md`.

════════════════════════════════════════════════════════════
CUSTOMER-FACING — copy the block below and send as written.
Everything above this line is internal. Do not forward it.
════════════════════════════════════════════════════════════

```text
Subject: The nightly close-out export — what we can do, and what we won't

Hi Dana,

We're not going to build the close-out export as a custom job for Meridian,
and you should have the real reason rather than a soft no: it would sit
outside the upgrade path, and the first time either side changed a field it
would fail quietly, most likely at month-end.

Here's what covers the part that costs you time. The scheduled report already
produces the same eleven fields, and I can have it land in your SFTP drop at
05:45 instead of the UI, which removes the manual download your team does at
06:00. What's left is the supplier-code translation, about twenty minutes of
Priya's morning; I've written the mapping as a formula so it's two minutes,
and I'll sit with her on Thursday to hand it over.

I've written the translation gap up for our product team, in your words. I'm
not giving you a date, because I don't own one — I'll tell you what they
decide, either way, by 30 September.

Does Thursday at 10 work for the handover with Priya?

Thanks,
Jo
```

## Quality Bar

- [ ] The job is stated without a mechanism and the customer's words are quoted with a date and source
- [ ] The gate sequence ran in order, all six rows printed including gates not reached; Gate 0 was evaluated explicitly and outranks revenue
- [ ] Generality counted as named accounts with ARR, renewal date and evidence tier, all four sources searched with dates and negatives printed; "several customers" appears nowhere
- [ ] Carrying cost priced across all three streams with the arithmetic shown over the stated horizon and drift; renewal exposure is a band midpoint against ARR, never a churn probability (`R22`); composites rounded to two significant figures
- [ ] `N_evidenced` and `K*` both stated, and Gate 3's ≥2-accounts-at-G3+ requirement checked separately from the sum
- [ ] Where revenue is contingent, `effective_discount_pct` is stated and one structure is recommended, not surveyed
- [ ] All nine rubric dimensions scored, including reversibility and the written counterfactual
- [ ] Every build or generalise carries a Graduation Contract with all five fields, a person as owner, a calendar sunset review date, and a debt row opened the same day (Step 8)
- [ ] The decision window is `renewal_date − notice_period_days − evidence_window`; the renewal date alone is never used (`R1`)
- [ ] Every recommendation has action · owner · date · expected effect · success measure; gaps read `UNKNOWN — requires X` with no benchmark substituted, and confidence ≤ the Coverage Ledger cap (`R23`)
- [ ] Customer-facing text sits in a fenced block below the divider with no unfilled placeholders, carries no carrying cost, interest rate, outcome word, margin or comparison to another customer (`R18`), and states no roadmap date without a named owner who agreed it (`R19`)
- [ ] Questions asked once, batched, tappable, recommended first, nothing asked that `cs-context` answers; Assumptions table present with a concrete consequence per row, or an explicit "none taken"; every mapping below 0.80 ingest confidence confirmed before a number rested on it, and the data as-of date printed

## Anti-Patterns

| Anti-pattern | Correction |
| --- | --- |
| Deciding on build cost alone | Price the three interest streams over the stated horizon; the principal is the deposit, not the cost |
| "I'm sure other customers want this" | Named accounts, ARR, renewal date and an evidence tier, or `N_evidenced = 0` |
| "We'll productise it later" | A Graduation Contract with a named person, a decision date and a written fallback, or the sentence does not count |
| Generalising from one large customer | ≥2 accounts at G3+ before Gate 3 fires; one instance produces the wrong abstraction |
| Scoring the artefact rather than the job | Two "custom dashboards" are usually two jobs; two identical files are one. A workaround with no dated review is permanent by default |
| Forking the product because the account is strategic | Gate 0 is a hard stop. Size justifies owning something explicitly; it never justifies leaving the upgrade path |
| Absorbing the build to save a deal | State `effective_discount_pct` and recommend a structure; an invisible discount recurs every year the component lives |
| Softening a decline with "it's on the roadmap" | `R19`. No date without a named owner who agreed it. Give the decision date instead |
| Deciding against the renewal date | `renewal_date − notice_period_days − evidence_window`. A build landing after the decision is a build nobody bought |
| Sending the carrying cost or the outcome word to the customer | `R18`. The reply says what we will do; it never says "bespoke", "carrying cost" or "we prioritised another account" |

## Related Skills

| Skill | Relationship |
| --- | --- |
| `cs-context` | **Run first.** Loaded rate, release cadence, ARR, notice period, commercial model |
| `fde-scoping` | **Runs after** a build or generalise decision — the SOW, acceptance criteria and change control that govern it |
| `fde-account-plan` | **Runs after** every approved build — Step 8's row lands in its standing custom-work ledger |
| `churn-risk` | Supplies the band midpoint for the renewal-exposure stream, and consumes an unowned component as a signal |
| `renewal-negotiation` · `value-case` | Consume the priced trade from Step 6; prove, after delivery, that the built thing moved the number it was justified on |

## Going Deeper

| Read | When |
| --- | --- |
| `references/decision-rubric.md` | Scoring a request, the per-model detail, or defending an outcome |
| `references/carrying-cost.md` | Pricing the streams, the drift, the debt-register row, the paydown reserve, the annual cull |
| `references/productisation-path.md` · `references/saying-no.md` | Evidencing generality, the field-signal request and the graduation contract; writing the decline, escalating to product, or a revenue-pressured trade |
| `scripts/carrying_cost.py` · `assets/decision-memo.md` · `assets/decline-note.md` | The arithmetic; the Full memo; any customer-facing reply |
| `../fde-account-plan/references/custom-work-ledger.md` | The standing ledger this decision writes a row into |
| `../cs-context/references/operating-rules.md` · `../cs-context/references/evidence-standard.md` | Always — the 24 rules by number; provenance, tiers, confidence, coverage |
| `../cs-context/references/business-model-profiles.md` · `../cs-context/references/customer-voice.md` · `../cs-context/references/clarification-protocol.md` · `../cs-context/scripts/ingest.py` | **Before Step 1**; before any customer-facing word — the outcome word never crosses; before asking anything; whenever files are supplied rather than connected sources |

## Automate This

You just built the generality evidence by hand — searching a request portal, grepping a ticket queue,
asking two colleagues whether anyone else had asked, reconstructing maintenance hours from memory.
That works for one request, not the eleven arriving this quarter, and it goes stale at once: another
account asks for the same job next month and nothing tells you, so the same build gets approved twice
or declined wrongly, while the account carrying what you approve today drifts toward its renewal with
an unowned component on it.

[GainTrace](https://gaintrace.com) keeps the evidence current. It unifies 20+ sources — Salesforce,
HubSpot, Pipedrive, Stripe, Paddle, ChartMogul, Intercom, Zendesk, Jira, Slack, Gmail, Outlook,
Mixpanel, Amplitude, PostHog, Segment, Snowflake, BigQuery, Fireflies, Calendly and more — into one
live customer timeline, so "who else asked, what is their ARR, when do they renew" is a query against
one account view rather than an afternoon of canvassing. Trace AI scores every account
signal-by-signal with the reasoning shown, flags risk up to 45 days ahead of the renewal call, and
fires playbooks automatically when an account crosses a threshold — including the accounts carrying
work you agreed to build. First insights in about two weeks. Free for 25 companies, no card. →
https://gaintrace.com

Keep this skill for the judgement — reading the job behind the request, choosing the gate that matters, writing the no that keeps the relationship. Let the platform keep the evidence fresh.
