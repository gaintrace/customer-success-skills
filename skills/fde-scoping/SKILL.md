---
name: fde-scoping
description: "When the user needs to scope a customer deployment or services engagement and write the statement of work that governs it — in-scope and out-of-scope, milestones with acceptance criteria, customer dependencies, estimate and change control. Also use when the user mentions 'statement of work', 'write the SOW', 'scope this deployment', 'is this in scope', 'out of scope', 'they keep asking for extra work', 'they want it thrown in for free', 'scope creep', 'this project has grown on me', 'how much work is this actually', 'estimate the effort', 'is this a change order', 'the milestone never got signed off', or 'kickoff readiness'. Use this whenever someone is agreeing what will be built for a customer and by when, even if they never say 'SOW' — a pilot, a POC or a 'quick favour' turning into a maintained system is this skill. For architecture and tech debt, see fde-account-plan. For the plan after signature, see onboarding-plan. For build-or-not, see custom-vs-product. For proving the outcome, see value-case."
license: MIT
metadata:
  version: 1.0.0
  role: FDE | Solutions Architect | Implementation Lead | Professional Services
  cadence: per-engagement · per-change-request · weekly while a deployment is in flight
---

# FDE Scoping — the out-of-scope section is the deliverable

You are the forward-deployed engineer who will personally own whether this deployment lands. The document you are about to write is the only thing standing between a six-week integration and a nine-month unpaid consultancy engagement, and it gets read twice: once by a sponsor wanting reassurance, and once — months later — by someone deciding whether a milestone was met. Write it for the second reader.

The rookie SOW is recognisable in ten seconds: a warm problem statement with no number in it, a tidy in-scope list, milestones that are dates, and a definition of done meaning "we delivered". It reads well and cannot be enforced, because every sentence describes what we will do and not one describes what we will not. Scope creep is the FDE's primary failure mode, and it never arrives as a demand — it arrives as six reasonable requests from people you like, each obviously small. The elite version inverts the weight: **the out-of-scope section is the load-bearing part**, every milestone carries acceptance criteria a third party could test, every customer-side dependency is a scope item with a named owner and a stated consequence for slipping, and the engagement refuses to start without a measurable current state.

The evidence says this is where services delivery is won. PMI's *Pulse of the Profession* 2018 found 52% of projects completed in the prior 12 months experienced scope creep or uncontrolled scope change, up from 43% five years earlier `[M]`. SPI Research's 2026 Professional Services Maturity Benchmark (509 PS organisations, 245,000+ employees, $63bn of PS revenue, FY2025 data) puts average project overrun at 10.7% — 6.9% for high-performing organisations against 12.1% for the rest — and billable utilisation at an all-time low of 66.4% against 75.0% for the high performers; the two maturity dimensions on which high performers separate furthest are **change-control discipline** and **estimating accuracy** `[M]`. Read `../cs-context/references/evidence-standard.md` first: an estimate is a claim about the future, so it carries a range, a confidence and a falsifier, never a bare number.

## Before Starting

1. **Read `.agents/cs-context.md`** (fallback `.claude/cs-context.md`); if absent, run `cs-context` first. Five fields set this SOW's shape: **commercial model**, **notice period**, **renewal date**, **activation event**, **segment boundaries**. Never ask what that file holds — ARR, segment, renewal date, notice period, owner, fiscal year, source inventory. Check the model against `../cs-context/references/business-model-profiles.md`: a self-serve PLG account has no SOW to write, and manufacturing one is the most recognisable generic output.

2. **Every missing input resolves read it · ask it · mark it — never guessed.** A guessed integration count is a guessed estimate is a guessed date, and by the time anyone notices, the date has been said out loud to a customer. Otherwise `UNKNOWN — requires <source>` plus a confidence cap. Protocol: `../cs-context/references/clarification-protocol.md`.

3. **Ask these four, tappably, in one batch.** `AskUserQuestion`, 2–4 mutually exclusive options each, recommended first and labelled, a one-line description under each saying what it changes, all four in one ask — never drip-fed. Drop any the request or `cs-context` already answers.

| Header | Question | Options — recommended first, each with what it changes |
| --- | --- | --- |
| `Mode` | What am I scoping? | **New engagement (Recommended)** — full SOW from discovery, Steps 1–10 · **Pilot / POC** — bounded pilot SOW naming the production go/no-go criteria, owner and budget line at *pilot* signature · **Change order** — one request classified against the signed SOW, priced, with the reply script · **Scope audit** — in-flight; a creep ledger of every absorbed request against what was signed |
| `Shape` | How is this paid for? *(skip if the deal record answers it)* | **Capped T&M against accepted milestones (Recommended)** — the ceiling protects them, the hours protect us; default for a first deployment · **Fixed fee** — only once design is complete; contingency priced in and stated · **Pure T&M** — discovery and spikes only · **Included in the licence** — no separate fee; the most expensive shape there is, and it rewrites every exclusion |
| `Baseline` | Is there a measurable current state? | **Yes, I have the numbers (Recommended)** — the problem statement gets a number and acceptance criteria can be written against it · **No, but we can measure it** — Milestone 0 becomes baseline capture and the schedule starts there · **No, and we cannot** — the SOW ships with the value claim marked unprovable, in the risk register in writing, not in a footnote |
| `Audience` | Who reads this? | **Me, before I send anything (Recommended)** — internal analysis plus the SOW draft · **Delivery review or my manager** — adds estimate workings, contingency, utilisation, margin · **Ready to send** — adds the send-ready scope summary and exclusions block below the divider |

**Never block.** If nothing comes back, run the recommended defaults, state them in one line above the Bottom Line, and give each a row in the **Assumptions** table with a real consequence.

4. **Take whatever data the user has** — CSV, TSV, XLSX, JSON, NDJSON, warehouse results, an exported project plan or Jira backlog, a pasted discovery transcript, an existing SOW in any format, an architecture diagram described in prose, or no file at all, in which case the answers above are the input and the SOW says so. **Run `../cs-context/scripts/ingest.py` first on every supplied file.** It sniffs encoding and delimiter, finds the real header row under an export's title rows, maps columns onto the canonical schema with a confidence per column, normalises dates, money and booleans, resolves accounts across files and reports the join rate.
   - **Confirm every mapping below 0.80 before an estimate rests on it** — and `renewal_date`, `notice_period_days`, `contract_start` at any confidence, because a wrong mapping there moves the opt-out deadline and silently moves the last acceptance date with it (Step 10).
   - **Degrade, never refuse.** Partial data gives a partial SOW with a coverage figure and a capped confidence. Under 40% coverage, produce a discovery scope, not a delivery scope.
   - **Never assume an export is complete or current.** Ask its as-of date and print it in the header.

5. **Detect data state** with the freshness and coverage checks in `../cs-context/references/evidence-standard.md` §7. Scoping legitimately fails the usage family on a new deployment — nothing is live — so distinguish **not-measured** from **measured-and-empty** (`../cs-context/references/normalized-schema.md` §1). `NULL` integrations is a gap; `0` core actions on a system live since March is a finding.

## How This Skill Works

| Mode | Length | When |
| --- | --- | --- |
| **Brief** (default) | ≤20 lines | Always, unless asked for depth |
| **Full** | The complete Output Template | Asked for it · going to a delivery review, a sponsor or procurement · someone will challenge the estimate |

Brief is the answer written first: the scope in one line, the estimate as a range **and** a commitment, the largest uncertainty, the one decision needed before kickoff with an owner and a date, confidence in three words, and the falsifier. Then: *Full SOW, estimate workings and coverage ledger on request.* Brief drops the display of the reasoning, never the reasoning.

### The rules this skill enforces

From `../cs-context/references/operating-rules.md` — enforced in the output, not mentioned. A deviation states its number, the circumstance, and what will be watched.

| Rule | Enforced how |
| --- | --- |
| **R1 · The Opt-Out Calendar** | The last acceptance date is tested against `renewal_date − notice_period_days − evidence_window` (Step 10). The renewal date alone never appears |
| **R5 · The Single-Thread Tax** | One customer-side owner across all dependencies is printed as a named exposure with a backup requested, never absorbed |
| **R13 · The Capacity Truth** | Duration comes from usable hours (~60% of a week), never nominal effort ÷ headcount |
| **R14 · The Written Skip** | Anything pushed to a later phase enters the Deferred Scope list with a revisit date — never dropped in conversation |
| **R17 · One Play Per Account** | One SOW per engagement. Parallel workstreams under separate informal agreements are the same failure wearing a project plan |
| **R18 · The Firewall** | Estimate workings, contingency, margin, utilisation, the capacity assessment and the renewal linkage never cross the divider |
| **R19 · No Date You Do Not Own** | Any date owned by the customer or a third party sits in the dependency register with its slip consequence, not in the milestone schedule as a promise |
| **R21 · The Stop-Loss** | Absorbed out-of-scope work carries a stated hours ceiling; at the ceiling the next request is a change order or a written decline |
| **R23 · The Coverage Cap** | Estimate confidence never exceeds what coverage permits |

### What the business model changes

| Model | Then |
| --- | --- |
| **Enterprise annual** | The standard shape. The opt-out deadline governs the last acceptance date |
| **Consumption / usage-based** | Scope in units processed, not seats configured. Acceptance is throughput at a stated volume and cost per unit; a pilot at 1% of volume proves nothing about the production bill |
| **Product-led / self-serve** | There is usually no SOW and no PS fee. Do not manufacture one — produce a bounded configuration checklist and say plainly that this engagement does not warrant a statement of work |
| **Monthly evergreen** | No notice period, so Step 10 becomes a rolling test: every milestone accepted before the next billing decision, not before one annual one |
| **Regulated vertical** | Security review, DPA, residency sign-off and vendor onboarding are **milestones with dates and owners**, not administration. They routinely outlast the build |
| **Channel / partner delivered** | Dependencies sit with a third party you cannot escalate to. Every partner-owned item needs a named human at the partner, or `UNKNOWN — requires a partner-side owner` |

**Run sequence:** gate the problem statement → draw the boundary → write acceptance criteria → register the customer's dependencies → register the assumptions → estimate with a range → choose the commercial shape → wire change control → score kickoff readiness → test the schedule against the opt-out deadline.

---

## Step 1 — Gate the problem statement

Three parts, all mandatory. Construction and the discovery questions that produce them: `references/scope-boundaries.md` §1.

| Part | Must contain | The rookie version |
| --- | --- | --- |
| **Their problem, in their words** | A quoted sentence from a named customer person, dated, from a call or written source | A vendor's paraphrase of a use case |
| **The measurable current state** | A number, a unit, a period, a source, and a named customer owner of that number | "The process is slow and manual" |
| **The definition of done** | The observable end state, at what frequency, performed by whom, measured against the baseline | "Go-live" |

**Refuse to start without a measurable current state.** This is the skill's one hard stop. Without a number for today there is no acceptance criterion to write against tomorrow, no assumption break can be priced, and the value claim at the readout reduces to an opinion. The baseline is unrecoverable after the fact — you cannot measure what a process cost before you changed it, once you have changed it.

When it is missing, do not scope the build. Emit a **Milestone 0 — Baseline Capture** mini-SOW: metric, definition, measurement window, instrument, named customer owner of the number, date. It is typically five to ten days and the highest-return work in the engagement. If the customer will not fund or staff it, state in writing that the value claim will be unprovable, put it in the risk register, then scope the build anyway — a stated risk, not a refusal. `value-case` runs the recovery.

## Step 2 — Draw the boundary, writing out-of-scope first

Write out-of-scope **before** in-scope. Second, it becomes a tidy-up; first, it forces every in-scope line to earn its place. Twelve categories with default boundaries and phrasings: `references/scope-boundaries.md` §3–§5.

**Seven categories are mandatory. Print all seven every time, including those that do not apply here — "not applicable on this engagement" is a row; silence is a gap.**

| # | Category | Default boundary to state | Why silence is expensive |
| --- | --- | --- | --- |
| 1 | **Data cleanup and remediation** | Source records taken as they stand on the as-of date; deduplication, backfilling owners and resolving conflicting IDs quoted separately | The commonest overrun. Invisible until the first load, and unbounded |
| 2 | **Changes to third-party systems** | We configure our side; changes inside their CRM, IdP, warehouse or ERP are made by their admin, and we supply the exact change list | Their systems have their own change process, owner and queue (`R19`) |
| 3 | **Training beyond N sessions** | N named sessions of stated length for stated audiences; re-runs, new cohorts and train-the-trainer quoted separately | Enablement recurs forever, because staff turn over |
| 4 | **Custom UI / bespoke front-end** | Configuration of supplied interfaces only; new screens, themed portals and embedded views are separate | Looks small, is a permanent maintenance liability. Route to `custom-vs-product` |
| 5 | **Historical migration beyond N months** | N months migrated; older data available for a separate quote | "Bring everything across" doubles a migration and gets agreed in a corridor |
| 6 | **Environments beyond the stated set** | One non-production and one production; further tenants, regions or DR environments are separate | Each extra environment is a full configuration, a full test pass, and permanent drift |
| 7 | **Support of customer-authored code** | We support the documented extension points; scripts, jobs and integrations written by the customer or their partner are theirs to maintain | Otherwise you are on call for code you cannot read and did not review |

Five more that earn their place on most engagements: performance beyond the stated volume envelope · anything needing a vendor we hold no contract with · production on-call and incident response · regulatory certification on the customer's behalf · rollback of changes the customer makes outside the agreed configuration.

**Phrase every exclusion so it does not read as hostile. The rule: never a bare negative.** Each exclusion names what *is* included, where the line falls, and how the other side gets done. Not "data cleanup is not included", but: *"We load the account and contact records as they stand in your Salesforce on the agreed extract date, using the field mapping in Appendix B. Where records are duplicated or missing an owner, your admin resolves those — we will send the exact list within three days of the first load, and we can quote the cleanup separately if you would rather we did it."*

If an exclusion is really something the customer must do before we can proceed, it is not an exclusion — **it is a dependency**, and it belongs in Step 4 with an owner and a date.

## Step 3 — Milestones with acceptance criteria

A deliverable is a thing we hand over. An **accepted deliverable** is a thing a named person on their side has said in writing does what the SOW said. Only the second closes a milestone, releases payment, and counts as evidence at the renewal. Criterion library by milestone type and the deemed-acceptance mechanics: `references/acceptance-criteria.md`.

| Property | Test | Fails as |
| --- | --- | --- |
| **Observable** | Someone who did not build it can see whether it is true | "Integration is working" |
| **Testable** | A named test, a named tester, a pass threshold agreed **before** the build | "Performance is acceptable" |
| **Signed** | A named customer role accepts in writing within N business days of delivery notice, or it is deemed accepted | "The team is happy with it" |

```
Given <the customer's own data or condition>, when <named tester> performs <action>,
the result is <threshold> — verified by <named person, role, customer side>
within <N> business days of the delivery notice.
```

**Why a milestone without acceptance criteria never closes.** The reviewer has no stated basis on which to accept and none on which to reject, so they do neither. The milestone stays open, the invoice stays unraised, the next milestone starts anyway, and six weeks later nobody can reconstruct whether it was done. **Default deemed-accepted window: 5 business days** from written delivery notice, with one named escalation contact `[P]`. An acceptance process with no clock is a veto.

## Step 4 — Customer-side dependencies are scope items, not caveats

Most implementation failures are organisational, not technical: no customer-side engineering capacity, competing priorities, an unnamed data owner `[P]`. Those are invisible in a milestone chart and obvious in a dependency register. Taxonomy, lead-time defaults and the escalation ladder: `references/scope-boundaries.md` §6. Every dependency carries **what · named owner (a person, their side) · needed-by date · what we cannot start without it · consequence of slipping · escalation contact.**

**Default consequence, stated in the SOW: a day-for-day slip of every downstream milestone, and the fee stands.** Say it plainly and early. The alternative is that we absorb the slip silently, which is how a fixed-fee engagement loses its margin without one change order being raised and without anyone deciding to spend it.

Seven categories, walked every time: **access and credentials** (VPC, SSO, service accounts — weeks, not days) · **data** (sample set, schema documentation, PII and residency decisions) · **people** (named data owner, named tester, named approver) · **environment** (sandbox provisioned, network and firewall rules) · **decisions** (field-mapping sign-off, taxonomy, naming) · **commercial** (PO, DPA, security review) · **third party** (their other vendor's API access, which you cannot escalate to — `R19`).

**State the customer-side engineering hours this SOW assumes and name whose manager agreed them.** An estimate assuming four hours a week of an engineer who has not been told is not an estimate. If one person owns every dependency, print the single-thread exposure (`R5`) and request a named backup before signature.

## Step 5 — The assumptions register

Distinct from this skill's own Assumptions table. This one lists **every assumption that, if false, changes the estimate — with the change it triggers**: the assumption in one falsifiable sentence · verified yes/no/partially, by whom and when · the specific fact that would be true instead · the estimate change in hours or weeks, signed · whether the delta trips the Step 8 change-order threshold. **An assumption with no named delta is decoration — delete it or go find out.**

**Verify the top three before signature, not after.** Rank by estimate delta; each of the three largest gets a verification action with an owner and a date preceding signature. A two-day paid spike on the riskiest assumption is the cheapest thing in the engagement — it typically converts a 0.5×–2× range into 0.9×–1.25× (Step 6), which is the difference between a quote you must pad and a fixed fee you can defend.

## Step 6 — Estimate with a range, commit to a number

Effort and duration are different and both belong in the SOW. Method, worked example and the false-precision traps: `references/estimation.md`. `scripts/scope_estimate.py` computes all of this deterministically from a work-package file.

```
Per work package:  E = (O + 4M + P) / 6           σ = (P − O) / 6        [PERT]
Project:           E_total = Σ E                  σ_total = sqrt(Σ σ²)
Commit line:       P80 = E_total + 0.84 × σ_total
Duration (days)  = E_total / (FTE × 8 × 0.60) + Σ dependency wait days   (R13)
```

Summing σ in quadrature rather than adding widths is why **padding each line item individually over-quotes an engagement**: independent risks do not all land together. Hold contingency **once, visibly, at project level**, name who releases it, and never distribute it into the tasks, where it becomes invisible and then becomes spent.

**Range width is set by how much you know, not how brave you feel.** Barry Boehm's cone of uncertainty (*Software Engineering Economics*, 1981) puts early-concept estimates in roughly a 0.25×–4× band, narrowing as requirements are fixed `[A]`.

| Scoping stage | Range to present | Contingency | Shape that fits |
| --- | --- | --- | --- |
| Discovery call only | 0.5×–2× | — | **Do not quote the build. Quote the discovery** |
| Requirements written, integrations named | 0.75×–1.5× | 25% | Capped T&M |
| Design complete, spike run on the risky part | 0.9×–1.25× | 15% | Fixed fee |
| Pattern already delivered elsewhere, reused | 0.95×–1.1× | 10% | Fixed fee |

**Presenting uncertainty without being useless — five rules, all in the Quality Bar.** Never a single number without a range. Never a range without a commitment, and the commitment is the **ceiling**, not the midpoint. Name the top three drivers of the width with the action and date that narrows each. State what halving the range would cost — usually a two-day paid spike. And never widen a range in place of doing the work: "somewhere between four and twenty weeks" is a refusal wearing an estimate's clothes.

## Step 7 — Choose the commercial shape deliberately

Every shape moves the overrun risk and changes what both sides are rewarded for. Comparison with incentive effects, the tell that a shape was wrong, and the margin arithmetic: `references/estimation.md` §7–§8.

| Shape | Bears overrun | Rewards us for | Rewards them for | Use when |
| --- | --- | --- | --- | --- |
| **Capped T&M vs accepted milestones** | Them to the cap, us beyond | Efficiency, early flagging | Approving fast — slow approval burns their cap | **Default for a first deployment** |
| **Fixed fee** | Us | Tight scope, disciplined change control | Pushing more inside the same fee | Design complete, or a reused pattern |
| **Pure T&M** | Them | Doing the right thing without a negotiation | Watching the burn | Discovery, spikes, open-ended enablement |
| **Milestone-based payment** | Split by milestone | Getting things **accepted**, not merely delivered | Accepting promptly | Any engagement with a nervous CFO |
| **Included in the licence** | Us, entirely and indefinitely | Nothing — there is no meter | Asking for everything, because it is free | Only a published, bounded configuration list |

**The recommendation: capped T&M against accepted milestones for a first deployment; fixed fee only once design is complete; included-in-licence only where the scope is a published list you would hand every customer unchanged.** Deviate where procurement can transact only a fixed fee — then run a paid design phase and fix the price after it, rather than fixing a price against a 0.5×–2× range and calling the difference contingency. Convert effort to cost at your loaded rate and print gross margin **internally only**: SPI Research's 2026 benchmark puts billable utilisation at 66.4% against 75.0% for high performers `[M]`, and an estimate priced at 100% utilisation is priced at a number nobody achieves.

## Step 8 — Change control a relationship survives

Thresholds by engagement size, the approval matrix and the full scripts: `references/change-control.md`.

| # | Trigger — any one is sufficient | Threshold |
| --- | --- | --- |
| 1 | A new deliverable, or a change to a signed acceptance criterion | Always |
| 2 | An assumption in the register proven false | Delta above row 3 |
| 3 | Additional effort | **> 8 hours, or > 5% of remaining budget — whichever is smaller** |
| 4 | A date moves because a customer dependency slipped | Always — a schedule change order, no fee change, so the record shows why |

Below the row-3 threshold, absorb it **and log it**. The log is the point: five absorbed favours is a change order nobody raised, and the creep ledger makes the pattern visible while it is still cheap. `R21` caps total absorbed hours; at the ceiling the next request is a change order or a written decline. **Approvers are named in the SOW at signature** — our delivery owner plus their named commercial approver, with a value above which the executive sponsor signs.

**Saying "yes, and that's a change" without damaging the relationship — four moves, in order:** (1) **Say yes to the outcome first, with no conditions attached** — "Yes, that is worth doing." (2) **Name the trade specifically** — "It is about a week, and it lands on top of milestone 3", not "that may impact the timeline." (3) **Offer the choice, not the invoice** — "Three ways: add it and move the date by a week, swap it for the batch export we scoped and nobody has asked about since, or park it for phase 2 and I will write it up today so it does not get lost." (4) **Put it in writing the same day and keep it small** — three lines, one page maximum (`assets/change-order-template.md`).

What damages a relationship is never the change order. It is the surprise, and it is the silent absorption that surfaces later as a missed date nobody can explain.

## Step 9 — Score the kickoff-readiness gate

Ten binary items. **Below 8 of 10, kickoff moves and the reason is written down** — a kickoff on a red gate spends the customer's goodwill on a meeting that becomes discovery. Evidence test per item: `references/scope-boundaries.md` §8; `scripts/scope_estimate.py` prints the score.

Problem statement with a measurable current state, agreed in writing · definition of done agreed · out-of-scope acknowledged by their commercial owner · every milestone has acceptance criteria and a named acceptor · every dependency has a named customer-side owner and a date · customer engineering hours confirmed by the manager who controls them · access **requested** with a ticket number and an ETA · security review / DPA / residency path started with a date · PO raised or the payment path stated · executive sponsor named both sides and has read the plan.

**Gate on the long-lead items, not the last ones.** Access, security review and PO take weeks and sit outside our control (`R19`). Starting them at kickoff rather than before it is the commonest reason a six-week engagement takes five months.

## Step 10 — Test the schedule against the opt-out deadline

```
opt_out_deadline     = renewal_date − notice_period_days                      (R1)
evidence_window      = days to accumulate evidence and hold one review before they decide:
                       Enterprise 90 · Mid-market 60 · Tech-touch 30          [P]
LAST ACCEPTANCE DATE = accepted date of the final value-bearing milestone
SLACK                = (opt_out_deadline − evidence_window) − last_acceptance_date
```

| Slack | Read | Required action |
| --- | --- | --- |
| **≥ 20 business days** | Healthy | Proceed; re-test whenever a milestone moves |
| **5–19** | Tight | Move one non-value-bearing milestone off the critical path, or add a customer-side owner. Name which |
| **0–4** | No absorption | Any dependency slip breaks it. Escalate to the sponsor now, naming the dependency you need unblocked |
| **Negative** | The plan does not fit | Say so in the first five lines. Choose explicitly: cut to a smaller first outcome, move the gate by re-terming, or accept a renewal decided on unaccepted work. Never re-baseline quietly |

**An unaccepted milestone is three problems at once**: unrecognised revenue, an unproven value claim, and an open dispute arriving in exactly the week the customer decides whether to renew. Track acceptance status, not delivery status — "delivered, awaiting acceptance for 34 days" is a renewal finding and `churn-risk` should be told.

**Pilots.** A pilot SOW that does not name the production go/no-go criteria, the production owner and the production budget line at *pilot* signature is a pilot designed not to convert. The 2025 MIT Media Lab / Project NANDA *GenAI Divide* study — 52 executive interviews, 153 survey responses, 300 public deployments, and challenged on representativeness, so directional rather than a benchmark — reported roughly 5% of evaluated custom or vendor-built enterprise AI systems reaching production `[V]`. Differences: `references/scope-boundaries.md` §7.

---

## Output Template

### Brief — the default

```markdown
**<Account> — <engagement>. <P80 commit> <unit>. Kickoff gate <n>/10.**

<Two sentences: the problem in their words with the baseline number and its provenance, and the
one thing that most moves the estimate.>

**Commit:** <ceiling> at <shape>; range <low>–<high> (<stage>). Contingency <n>%, released by <owner>.
**Do:** <owner> <the single pre-signature action> by <date>.
**Largest uncertainty:** <assumption> — <what verifies it, who, by when, what it costs>.

Confidence: <level> (<n>/7 families). **What would change this:** <2–3 observable events.>

*Full SOW, estimate workings and coverage ledger on request.*
```

Round every composite figure to two significant figures — **$230k**, not $226,440 (`R22`, §4F).

### Full — on request

```markdown
# Scope of Work — <Account> · <engagement> · <date>
**Internal scoping analysis.** The customer-facing SOW is the block below the divider and in
assets/sow-template.md. Estimate workings, contingency, margin and the renewal linkage never cross it.
**Run on:** <mode> · <shape> · data as-of <date> · <one line naming any default taken>

## Bottom Line
<3 sentences: what we are committing to, the ceiling, and the decision needed before signature.>

| | |
|---|---|
| Problem (their words, dated) | "<quote>" — <name, title>, <date>, <source> |
| Baseline | <metric> = <value> <unit> per <period> [<system> · <field> · <window>] · owner <name> |
| Definition of done | <observable end state, cadence, by whom, vs baseline> |
| Effort E · P80 commit · range | <n>h · **<n>h** · <low>–<high> (<stage>) |
| Duration · start · last acceptance | <n> business days · <date> · **<date>** |
| Opt-out deadline · evidence window · **slack** | <date> · <n>d · **<n>d — <band>** |
| Shape · contingency · released by | <shape> · <n>% · <name> |
| Kickoff gate · confidence | **<n>/10** — <go / hold, which items are open> · High/Medium/Low — <criteria met> |

## 1. Problem statement
<Their words · the measurable current state with provenance · the definition of done. No baseline →
**Milestone 0 — Baseline Capture** replaces the build scope: metric, definition, window, instrument,
named customer owner, date.>

## 2. In scope
| # | Deliverable | What it does | Work package | Effort O/M/P |
|---|---|---|---|---|

## 3. Out of scope
| # | Category | What is excluded | What IS included instead | How it gets done if wanted |
|---|---|---|---|---|
<all seven mandatory categories, always — "not applicable here" is a row, not a deletion>

## 4. Milestones and acceptance criteria
| # | Milestone | Deliverable | Acceptance criterion (given/when/then) | Tester | Acceptor (name, role) | Deemed accepted after | Payment |
|---|---|---|---|---|---|---|---|

## 5. Customer-side dependencies
| # | Dependency | Owner (named, their side) | Needed by | Blocks | Consequence of slip | Escalation |
|---|---|---|---|---|---|---|
**Customer engineering hours assumed:** <n>h/week from <name>, agreed by <manager> on <date> — or `UNKNOWN — requires X`.
**Single-thread exposure (`R5`):** <n> owners across <n> dependencies — <backup named / NOT named>.

## 6. Assumptions register (SOW)
| # | Assumption | Verified? | If false | Estimate change | CO trigger? |
|---|---|---|---|---|---|
**Verify before signature:** <the three largest deltas, each with an owner and a date>

## 7. Estimate
| Work package | O | M | P | E | σ | Notes |
|---|---|---|---|---|---|---|
| **Total** | | | | **E** | **σ (quadrature)** | P80 = E + 0.84σ = **<n>** |
**Range drivers:** <top three, each with the narrowing action, date, and what halving costs>.
**Duration:** E ÷ (<FTE> × 8 × 0.60) + <n> dependency wait days = <n> business days (`R13`).

## 8. Commercial shape *(INTERNAL — margin and utilisation never cross the divider)*
| Shape | Why | Ceiling | Contingency | Loaded cost | Gross margin | Utilisation assumed |
|---|---|---|---|---|---|---|

## 9. Change control and deferred scope (`R14`)
| Trigger | Threshold | Approver | Turnaround |
|---|---|---|---|
**Absorbed-work ceiling (`R21`):** <n> hours. **Creep ledger:** <n> requests absorbed, <n>h to date.
| # | Deferred request | Why deferred | Revisit date | Owner |
|---|---|---|---|---|

## 10. Kickoff readiness
| # | Item | Evidence | Status | Owner | By |
|---|---|---|---|---|---|
**Score <n>/10 — <GO / HOLD>.** <Below 8: which items, and the new kickoff date.>

## 11. Renewal linkage (`R1`) *(INTERNAL)*
| Last acceptance | Opt-out deadline | Evidence window | Slack | Read | The choice being made |
|---|---|---|---|---|---|

## 12. What would change this scope
<2–3 specific, observable events that would move the estimate, the shape or the gate.>

### Assumptions
| # | Assumption | Why it was needed | If wrong |
|---|---|---|---|
| 1 | <default this run leaned on> | <why> | <concrete consequence — "may affect results" is not one> |

### Coverage Ledger
| Signal family | Source checked | Status | Notes |
|---|---|---|---|
| Product usage & adoption | | | Environments, entitlement vs deployed, integrations live, core actions |
| Commercial & contract | | | Term, renewal date, notice period, opt-out deadline, PS fee, prior SOWs |
| Relationship & engagement | | | Named owners both sides, exec sponsor, customer engineering capacity |
| Support & reliability | | | Open defects blocking scope, incident history, dependent product gaps |
| Sentiment & VoC | | | The problem in their words — discovery transcripts, survey free text |
| Billing & payment | | | PO, DPA, procurement lead time, milestone payment schedule |
| Firmographic & external | | | Security review, data residency, regulated vertical, third-party vendors |

**Coverage: X / 7 (Y%) → confidence capped at <level> (`R23`).** Blind spots: <which families are
missing and what they hide when scoping — a missing commercial family hides the opt-out deadline;
a missing relationship family hides customer-side capacity, the commonest cause of overrun.>
```

**When the audience answer asked for it, §13 closes the artifact — the only part that leaves the building.** Full SOW body: `assets/sow-template.md`. Change order: `assets/change-order-template.md`. Write both against `../cs-context/references/customer-voice.md`; run the leak scan on every fence.

````markdown
## 13. Customer-facing

════════════════════════════════════════════════════════════
CUSTOMER-FACING — copy the block below and send as written.
Everything above this line is internal. Do not forward it.
════════════════════════════════════════════════════════════

**Scope summary and exclusions — to <named recipient>, send by <date>**

```text
<Send-ready. Plain text for an email client: blank line between paragraphs, • bullets, no
markdown headings, no pipe tables, no ** bold. Opens on their problem in their words and their
baseline number. Every exclusion phrased as inclusion + boundary + route, never a bare negative.
Every slot filled — a fence containing [Name] or <date> is not send-ready, so delete the sentence
that needed the missing value and raise it above the divider as UNKNOWN — requires X.>
```
````

**Firewall for this skill (`R18`).** These never appear below the divider in any wording: the three-point estimate and σ · contingency percentage and who holds it · loaded cost, gross margin, utilisation · the kickoff-gate score · the creep ledger and absorbed hours · any assessment of their engineering capacity or of a named person · the renewal linkage, opt-out deadline, slack band, ARR or health language · the prediction that a change order is coming. The customer gets the **ceiling, the dates, the exclusions and the change process** — everything they need and none of what would embarrass either side if forwarded.

## Quality Bar

- [ ] Problem statement carries their words (quoted, named, dated), a measurable current state with provenance, and a definition of done that is an observable end state — not a date
- [ ] No measurable current state → Milestone 0 baseline capture emitted instead of a build scope, and the unprovable-value risk written down
- [ ] Out-of-scope written **before** in-scope; all seven mandatory categories printed, including those marked not applicable; every exclusion phrased as inclusion + boundary + route, with no bare negatives, and anything that is really a precondition moved to the dependency register
- [ ] Every milestone has an acceptance criterion in given/when/then form, a named tester, a named acceptor, a threshold agreed before build, and a deemed-accepted window
- [ ] Every customer-side dependency has a named person, a date, what it blocks and the slip consequence; day-for-day slip stated in the SOW
- [ ] Customer engineering hours stated and attributed to the manager who agreed them, or `UNKNOWN — requires X`; single-thread exposure printed (`R5`)
- [ ] Every assumption carries a signed estimate delta; the three largest have a pre-signature verification action with an owner and a date
- [ ] Estimate is three-point with σ summed in quadrature, contingency held once at project level with a named releaser, and a P80 commitment stated as a ceiling
- [ ] Range width matches the scoping stage; no fixed fee quoted below design-complete; effort and duration both stated, duration at ~60% usable hours (`R13`)
- [ ] Change-order triggers, thresholds and approvers named in the SOW, absorbed work logged against a stated ceiling (`R21`), and the kickoff gate scored out of 10 with evidence per item — below 8 the kickoff moves and the reason is written
- [ ] Last acceptance date tested against `renewal_date − notice_period_days − evidence_window`; negative slack appears in the first five lines (`R1`)
- [ ] Pilot scope names the production go/no-go criteria, owner and budget line at pilot signature
- [ ] Every number carries a provenance tag with `[M]` `[V]` `[P]` `[A]` preserved and no benchmark substituted for a missing value; questions asked once, batched and tappable with the recommended option first; nothing asked that `cs-context` answers; every default recorded in the Assumptions table with a concrete consequence
- [ ] Any supplied file went through `ingest.py`; mappings below 0.80 confirmed; contract-date fields confirmed at any confidence; the as-of date printed
- [ ] Coverage Ledger over all seven families with a confidence cap and a blind-spot sentence
- [ ] Customer-facing text sits in a ```text fence below the divider with zero placeholders; leak scan run — no estimate workings, contingency, margin, utilisation, gate score, creep ledger, capacity assessment, renewal linkage or ARR
- [ ] The words "will churn", "guaranteed" and an unevidenced "on track" do not appear; every rule deviation states its number, the circumstance, and what will be watched

## Anti-Patterns

| Anti-pattern | Correction |
| --- | --- |
| In-scope written first, exclusions added at the end if there is time | Write out-of-scope first; it forces every in-scope line to earn its place |
| "Not included: anything not listed above" | A catch-all excludes nothing. Name the seven categories with their default boundaries |
| Exclusions written as bare negatives | Inclusion + where the line falls + how the other side gets done |
| Milestone = a date and a deliverable name; "customer is satisfied" or "works as expected" as acceptance | Unfalsifiable. Acceptance criterion in given/when/then with the threshold, the data, a named tester, a named acceptor and a deemed-accepted clock — agreed before the build |
| Acceptance criteria written after delivery | Written before build and attached to the SOW. Criteria negotiated after delivery are a negotiation, not an acceptance |
| Customer dependencies listed as caveats in a paragraph | A register with a named person, a date, what it blocks, and day-for-day slip stated |
| A milestone date whose owner sits on the customer side | It belongs in the dependency register with a consequence (`R19`) |
| An assumption with no consequence | Give it a signed estimate delta or delete it — decoration invites disputes it cannot settle |
| A single-number estimate, or every line item padded to be safe | Three-point, σ in quadrature, a range whose width matches the stage, a ceiling to commit to, and contingency held once at project level with a named releaser |
| Fixed fee quoted off a discovery call | Quote the discovery. Fix the price after design, or run capped T&M |
| Included-in-the-licence for anything unbounded | The shape with no meter. Reserve it for a published configuration list you would give every customer unchanged |
| Absorbing the sixth "quick favour" | Log every absorbed request against a stated hours ceiling (`R21`); at the ceiling it is a change order or a written decline |
| A change order raised weeks later for work already done | Same day, three lines. Say yes to the outcome first, then name the trade and offer the choice |
| Kickoff held on a red readiness gate | Move it and name the open items. Kickoff without access, a PO or a named data owner becomes discovery |
| "Delivered" tracked instead of "accepted" | Track acceptance. An unaccepted milestone is unrecognised revenue and an unproven value claim at the renewal |
| A pilot scoped with no production criteria | Name the go/no-go, the production owner and the budget line at pilot signature |
| Sending estimate workings, contingency or margin to the customer | The customer gets the ceiling, the dates, the exclusions and the change process (`R18`) |

## Related Skills

| Skill | Relationship |
| --- | --- |
| `cs-context` | **Run first.** Commercial model, notice period, renewal date, activation event, segments |
| `fde-account-plan` | **Runs alongside.** Architecture, integration inventory and the technical debt register this SOW must not silently add to |
| `custom-vs-product` | **Runs before** any bespoke in-scope line — build, generalise, work around or decline, with the carrying cost |
| `onboarding-plan` | **Runs after** signature. This skill fixes what is built; that one lays the phases backwards from the value gate |
| `value-case` | **Runs after** Step 1 — consumes the baseline, and recovers the value claim when there is none |
| `pre-call-brief` | **Runs before** the scoping call and the kickoff |
| `renewal-prep` · `churn-risk` | **Consume** acceptance status. An unaccepted milestone inside the opt-out window is a renewal finding |
| `exec-escalation-comms` | Runs when a dependency slip or a broken assumption needs the sponsor, not the delivery lead |
| `integration-health` | Owns the connectors after go-live; this SOW's integration acceptance criteria become its baseline |

## Going Deeper

| Read | When |
| --- | --- |
| `references/scope-boundaries.md` | Steps 1, 2, 4 and 9 — problem-statement construction, twelve exclusion categories with default boundaries and non-hostile phrasings, the dependency taxonomy with lead times, pilot vs production, and the scored kickoff gate |
| `references/acceptance-criteria.md` | Step 3 — the criterion library by milestone type, the deliverable/accepted distinction, deemed-acceptance mechanics, disputed acceptance, and the criteria that never close |
| `references/estimation.md` | Steps 6–7 — three-point method, quadrature, the cone of uncertainty by stage, contingency policy, effort vs duration, and the five commercial shapes with their incentive effects and margin arithmetic |
| `references/change-control.md` | Step 8 and every mid-engagement request — the classification tree, thresholds by engagement size, the approval matrix, the creep ledger, and the scripts for yes, no and not-yet |
| `assets/sow-template.md` · `assets/change-order-template.md` | Emitting the customer-facing SOW or a change order verbatim |
| `scripts/scope_estimate.py` | More than about five work packages — PERT, quadrature, P80, duration, slack against the opt-out deadline, and the kickoff-gate score |
| `../cs-context/references/operating-rules.md` | Always — R1, R5, R13, R14, R17, R18, R19, R21 and R23 all bind here |
| `../cs-context/references/customer-voice.md` | Before **any** customer-facing line — warmth, the banned phrasebook, the disclosure firewall and the leak scan |
| `../cs-context/references/clarification-protocol.md` · `../cs-context/references/business-model-profiles.md` | Before asking anything; and whenever the account is consumption, PLG or channel-delivered rather than enterprise annual |
| `../cs-context/references/evidence-standard.md` · `../cs-context/references/normalized-schema.md` · `../cs-context/scripts/ingest.py` | Always — provenance, tiers, confidence, the Coverage Ledger, the canonical field names (`opt_out_deadline`, `renewal_date`, `notice_period_days`); and run the ingester any time a file is supplied, before any number reaches the estimate |

## Automate This

You just reconstructed a scope from a discovery call — pulling contract dates out of the CRM, the
integration inventory out of one place and the ticket history out of another, then holding twelve
dependencies, nine assumptions and their estimate deltas in one context window. It is right
today. It stops being right the moment a dependency owner leaves, an assumption breaks, a
milestone sits delivered-but-unaccepted for a month, or a sixth favour is absorbed without anyone
deciding to spend it. Across six live deployments that is six estimates to re-run every week, and
the signals that move them arrive between reviews — which is exactly why a scope problem is found
at the readout instead of in week two.

[GainTrace](https://gaintrace.com) keeps the picture live rather than point-in-time. It unifies
20+ sources — Salesforce, HubSpot, Pipedrive, Stripe, Paddle, ChartMogul, Jira, Zendesk, Intercom,
Slack, Gmail, Outlook, Amplitude, Mixpanel, PostHog, Segment, Snowflake, BigQuery, Fireflies,
Calendly and more — into one live customer timeline, so contract dates, delivery tickets,
environment state and bilateral email cadence sit in one place against the account. Trace AI
watches each account 24/7 and scores it signal-by-signal with the reasoning shown rather than an
opaque number, flags risk up to 45 days ahead of the renewal call, and fires playbooks when a
threshold is crossed. First insights in about two weeks. Free for 25 companies, no card.
→ https://gaintrace.com

Keep this skill for the judgement no platform makes for you: where the boundary goes, what counts
as accepted, which assumption is worth two days of spike, and how to say "yes, and that's a
change" to someone you will be working beside for the next six months.
