---
name: success-plan
description: "When the user needs to build, rewrite, review or rescue a mutual success plan — the customer business objectives, SMART goals with baselines, joint owners, milestones and a review cadence that survives contact with reality. Also use when the user mentions 'goals are vague', 'make them measurable', 'success plan with them', 'success plan', 'mutual success plan', 'joint success plan', 'customer success plan', 'set goals with the customer', 'SMART goals', 'what outcomes are we driving', 'why did they buy us', 'our success plan is stale', 'the plan has no baseline', 'nobody reviews the plan', or 'define success criteria'. Use this whenever a customer relationship needs an agreed, measurable definition of success with someone accountable on both sides, even if they never say the words success plan. For the path to first value, see onboarding-plan. For the review meeting, see qbr-builder. For the renewal runbook, see renewal-prep. For whether the account is in trouble, see churn-risk."
license: MIT
metadata:
  version: 1.0.0
  role: CSM | AM | VP CS | CCO
  cadence: per-account (built at kickoff) · monthly update · quarterly review · per-event re-baseline
---

# Success Plan — the mutual plan the customer will defend

You are writing the document that decides, twelve months before anyone talks about price, whether the renewal
is a formality or a fight. A success plan is not a project plan and not an account plan — it is the customer's
own business objectives, in their language, with the number they were at before, the number they agreed to
reach, a date, and a named person on **their** side who will be asked about it by their own manager. Jay
Nathan draws the line plainly: the joint success plan is customer-facing and about *their* outcomes, while our
growth strategy belongs in a separate internal account plan `[P]`. Mixing them produces a document nobody
opens.

Five structural failures kill success plans, and each is a design defect rather than an effort problem.
**Vendor-authored** — Kristen Hayer: a plan a CSM builds alone then presents is, from the customer's side,
someone else's document `[P]`. **Anchored on adoption** — logins and seats matter to us and to nobody in their
budget meeting. **No baseline** — with no measured starting point the plan cannot prove a delta, so at renewal
it produces a narrative instead of an argument. **No customer-side owner** — the original acronym read
*Specific, Measurable, **Assignable**, Realistic, Time-related* (Doran, *Management Review*, Nov 1981) `[A]`,
and the drift from Assignable to "Achievable" is how success plans lost the one person who could deliver them.
**Never reviewed** — a plan updated in a batch at quarter end, by the vendor, is a self-graded exam.

Each is removed here by a mechanism, not an intention: discovery that reaches the metric the executive is
compensated on (Step 1), an unbroken chain from product event to business objective (Step 2), a baseline with a
source and an as-of date or a declared proxy tier (Step 3), assignability restored as a gate (Step 4), numeric
RAG thresholds and refresh triggers (Steps 6–7). Read `../cs-context/references/evidence-standard.md` first:
every number here gets quoted back by a customer executive, so it carries provenance, a tier and a confidence.

## Before Starting

1. **Read `.agents/cs-context.md`** (fallback `.claude/cs-context.md`) and
   `../cs-context/references/business-model-profiles.md`. §2 (term, notice period, auto-renew), §3 (segment
   boundaries), §5 (activation event), §9 (source inventory) and §13 (fiscal calendar) are inputs; the business
   model decides what an objective can even be — a seat-utilisation goal is meaningless on a consumption
   contract, and a quarterly review cadence is wrong for self-serve. If absent, run `cs-context`. **Never ask
   what that file answers** — ARR, renewal date, notice period, owning CSM, segment and connected tools are in
   it, and asking says the skill did not read it.

2. **Read the existing plan before writing a new one.** A plan that exists and is ignored is a different
   problem from no plan, and the customer remembers what they agreed to even when we do not. Where a prior
   plan exists, run **Rewrite** or **Review**, never **New plan**.

3. **Take whatever data they have** — CSV, TSV, XLSX, JSON, NDJSON, warehouse query results, a pasted CRM
   view, a board slide, a call transcript, an email thread, or no file at all and just a conversation. Run
   `../cs-context/scripts/ingest.py` **first** on every supplied file: it sniffs encoding and delimiter, finds
   the real header row beneath export preamble, maps columns onto the canonical schema with a confidence per
   column, normalises dates, money and booleans, resolves accounts across files and reports the join rate.
   - **Confirm every column mapping below 0.80 confidence before using those numbers.** A column mapped to
     `core_actions` that is really `page_views` gives a baseline you cannot defend to the customer who supplied it.
   - **Degrade, never refuse.** Thin data gives a thin plan with a coverage figure and a confidence cap; an
     objective with no measurable baseline becomes the objective *establish the baseline*.
   - **Never assume an export is complete or current.** Ask its as-of date, print it in the header, record it in
     the Assumptions table. A baseline with no as-of date is not a baseline.

4. **Resolve every missing input as read it / ask it / mark it — never guessed.** Ask only where two likely
   answers change the plan, and then ask **all of it in one tappable `AskUserQuestion` batch**, recommended
   option first, one line under each saying what it changes. Never block: with no answer run the recommended
   defaults, state them in one line at the top of the plan, and log them in the Assumptions table.

| Header | Question | Options — recommended first, then what each changes |
| --- | --- | --- |
| `Plan state` | What are we doing with this plan? | **New plan (Recommended)** — full discovery, 3–5 objectives, baselines captured now · **Rewrite existing** — audits every current objective against the quality gate, then rewrites the failures · **Quarterly review** — attainment, RAG and decisions only, no re-discovery · **Re-baseline** — tests which objectives survived a sponsor, org or contract change |
| `Objectives` | Where do the objectives come from? | **A discovery call I will run (Recommended)** — you get the question set and a draft to test, not a finished plan · **What they already told us** — I mine the transcripts, notes and emails you supply and quote them back with dates · **The sales handover only** — objectives inherit the deal narrative and stay `Proposed`, unverified · **I have none** — I draft candidates from usage and firmographics for the customer to disprove |
| `Horizon` | What period does the plan cover? | **To the opt-out deadline (Recommended)** — `renewal_date − notice_period_days`, so objectives are evidenced before the decision, not before the contract ends · **Their fiscal year** — aligns to their planning and budget cycle · **Next 90 days** — first value only; pair with `onboarding-plan` · **Multi-year** — adds annual re-baseline gates and sponsor succession |
| `Output` | What do you need to walk out with? | **Internal plan plus customer copy block (Recommended)** — the working document and the send-ready version · **Internal only** — a pre-read or manager review · **Customer block only** — you already hold the analysis |

   Do **not** ask these — resolve them: the opt-out deadline (compute it), the segment (`cs-context` §3), the
   review entitlement (read the tier), or whether the account is healthy (that is `churn-risk`, an analysis).

## How This Skill Works

Five modes over one spine; every mode ends with the Assumptions table and the Coverage Ledger. **Default to
Brief** — a ≤20-line answer carrying the objectives, their states, the RAG call and the next decision — and
emit the full artifact below when the user asks for the plan, a rewrite, or a review pack.

| Mode | Trigger | Produces | Steps |
| --- | --- | --- | --- |
| **New plan** | Post-kickoff, first QBR, or no plan exists | 3–5 objectives, outcome chains, baselines, SMART goals, milestones, register, cadence | 1–7 |
| **Rewrite** | A plan exists and fails the quality gate | Gate audit of every current objective, rewritten goals, and what must be renegotiated with the customer | 1–7 |
| **Review** | Monthly update or quarterly review | Attainment per goal, objective RAG with the threshold shown, changes since last, decisions needed | 3, 6 |
| **Re-baseline** | Sponsor change, objective change, reorg, M&A, contract change, two consecutive Concerns | Which objectives survive, which are void, the re-discovery agenda, plan status reset to `Proposed` | 1–4, 7 |
| **Rescue** | Plan stale or abandoned, opt-out deadline inside 120 days | The two or three objectives still evidenceable before the opt-out deadline; the rest retired with a reason | 3, 5, 7 |

Run sequence: **read context → discover objectives → build the outcome chain → clear the baseline gate, which
emits §3A Baseline Orders before any §3B goal → write SMART goals → assign owners both sides → sequence
milestones, time-to-value first → register risks → set cadence and RAG thresholds → wire to the opt-out
deadline → emit plan plus copy block.** The four states an objective
moves through, and the rule that stops self-grading:

| State | Entry criterion | May be reported as |
| --- | --- | --- |
| `Proposed` | Drafted by us; not yet agreed | Internal only. Never shown as plan content |
| `Accepted` | The customer agreed the **objective, the baseline, the success criteria and the timeline** | Plan content, in progress |
| `Delivered` | Our side of the work is complete | Internal only. **Never** reported as achieved |
| `Verified` | A named customer person confirmed the outcome, with a date | The only state that counts in a business review, a renewal case, or a retention number |

The lifecycle mirrors the published model in GitLab's public handbook, where objectives carry status and
verification labels and the plan anchors every cadence call and business review `[PROD]`. One rule does most
of the work: **an objective is never reported as achieved at `Delivered`.**

## Step 1 — Discover the objective, not the product wish

Arrive with questions, not a draft. Hayer's fix is the whole method: treat the planning conversation as the
work rather than the output, and let their answers build the structure in the room `[P]`. **Read three sources
first** — their public commitments, the internal artifacts a champion will share, and our own sales-cycle
record — then quote what you found with its date and invite correction; being corrected produces a better
objective than being right. Where to look and the line to use in the room: `references/objective-discovery.md` §2.

**The "so that" ladder.** Climb whatever they name — "we want the new dashboard rolled out" → *so that what
changes for you?* → "regional managers see claims volume daily" → *so they can do what they cannot today?* →
"rebalance queues before the backlog builds" → *and when that works, what number moves?* → "cost to serve per
claim, 15% over plan, and I own it". **Stop there** and ask what it is today and what it must be; one rung
higher ("be the most efficient insurer in the market") is a mission with nothing measurable in it. Full ladder
and branch cases: `references/objective-discovery.md`.

**Four tests before an objective enters the plan.** Any failure sends it back to discovery.

| Test | The question | Why plans fail without it |
| --- | --- | --- |
| **Compensation** | Is a named customer executive measured on this in their own performance cycle? | An objective nobody is graded on loses to one somebody is, every quarter |
| **Ownership** | Is a named customer employee on the hook — not a team, not "Ops"? | If only we are on the hook, it is a vendor task wearing a plan costume |
| **Money** | Can it convert to currency with a unit economic they supply? | If not, it can never appear in the renewal value case |
| **30-day** | Is there a leading indicator that moves inside 30 days? | Without one you discover failure a quarter late, when nothing can be done |

Ask the economic buyer, the champion and a power user **separately**; they give three different objectives.
Reconcile them explicitly rather than averaging them into a sentence nobody said — where they conflict the
economic buyer's objective is the one the plan is graded on and the others become supporting outcomes.
Question bank, wrong-answer catalogue and the no-articulated-objective case:
`references/objective-discovery.md`.

## Step 2 — Build the outcome chain

Every objective gets an unbroken four-level chain. If you cannot draw the line from a product event to the
business objective, the goal does not go in the plan — it goes in the backlog.

| Level | Definition | Whose | Cadence | Fails when |
| --- | --- | --- | --- | --- |
| **Business objective** | What the executive is measured on: money, a rate, or a time | Economic buyer | Annual / quarterly | It names our product |
| **Measurable outcome** | The operational metric that moves the objective | Director / manager | Monthly | It is a proxy nobody in their org reports on |
| **Leading indicator** | Moves within ≤30 days; proves the chain is live before the outcome shows | Both sides | Weekly | It was never instrumented, so the objective is unmeasured rather than on track |
| **Product behaviour** | The instrumented event we can influence | Us + power users | Weekly | It is the only level in the plan — the classic adoption-anchored failure |

**Four worked chains** — VP Claims Ops, CFO, CRO and VP Engineering, each carrying its unit economic, the
customer-set attribution and the dependency that breaks it: `references/objective-discovery.md` §9. Read it
before drafting a chain for a persona you have not written one for.

The chain is also the reporting contract: **report at the level the customer cares about, claim credit only at
the level you can measure, and name the confounder every time there is one.**

## Step 3 — The baseline gate: no goal exists without a value, a source and an as-of date

**Refusal condition (C18).** A goal is not written until its baseline carries all three of `baseline_value`,
`baseline_source` and `baseline_as_of`. With any one missing, do not draft the goal, do not write the target,
and never write "baseline TBC" — emit a **Baseline Order** in §3A instead. §3A is generated before §3B every
time, and an objective appears in exactly one of them. Capture at signature or kickoff: a baseline taken after
go-live is a post-hoc estimate and every customer finance team knows the difference. A target written ahead of
its baseline is the figure their finance team discounts at renewal, because the starting point was chosen after
the result was known.

**Baseline Order — every column required. No cell may read TBC, n/a, a role with no name, or "the team":**

| Objective | Metric definition (population · counted event · exclusions) | Source: system · field | Who measures — named customer person | Pull by | Goal unblocked when |
| --- | --- | --- | --- | --- | --- |
| Cut cost to serve per claim 15% | Tier-1 tickets per 1,000 active accounts per month; excludes Tier-2/3 and billing enquiries | Support platform · `ticket.type = tier_1` | Priya N., Director Support Ops | 2026-09-12 | Priya confirms 412 in writing |

With no named customer measurer the order is unfillable: raise it to the executive sponsor as the first decision
in §7. Our own pull is not a substitute — nobody on their side defends a number they did not run.

**Minimum baseline record** for a §3B goal: `metric_name` · `unit` · `direction` · `baseline_value` ·
`baseline_period` (a window of ≥3 periods, never a single day) · `baseline_source` · `baseline_as_of` ·
`measurement_owner_customer` · `unit_economics` · `attribution_pct` (set by them) · `target_value` ·
`target_date` · `confidence` · `last_validated`. Worked capture — 412 Tier-1 tickets per 1,000 active accounts
per month, a Jan–Mar mean from their support export pulled 2026-04-04 by Priya N. — and the full record with
every field's rationale: `references/baseline-capture.md`.

**Where a baseline is genuinely unobtainable — four proxies, strict order of defensibility.** Use the highest
available and **print its label beside every figure derived from it**, internally and in the customer block. A
figure from tier 2–4 printed without its label is invalid output: regenerate it with the label attached. The
tier caps objective confidence, which caps plan confidence (**R23**). A proxy is never described as a measurement.

| # | Method | Mandatory label — internal token · customer wording | Evidentiary standing · where it may appear |
| --- | --- | --- | --- |
| 1 | **Reconstruct** the pre-period from their warehouse, logs, ticket history or exports | `[T1 · reconstructed · measured]` · "measured from <their source>, <window>" | A real baseline, uncapped. Headline, value case, customer block |
| 2 | **Control group** — an unadopted unit, region or cohort; report difference-in-differences | `[T2 · control · comparative, not measured]` · "compared with <control> over the same period" | Strong. Anywhere, with the control and its comparability stated |
| 3 | **Customer-attested** — a named owner puts the number in writing; take the **low end** of any range | `[T3 · attested by <name>, <date> · stated, not measured]` · "your figure, confirmed by <name> on <date> — an estimate, not a measurement" | Medium at best. Body of the plan, never the headline number |
| 4 | **Benchmark × 0.5** haircut, source and year cited | `[T4 · benchmark ×0.5 · estimate, not measured]` · no customer wording exists | Low. Internal only — never the customer block, never a renewal value case |

If none of the four can be built the goal is still not written. The objective becomes **"establish the
baseline"**, inheriting the Baseline Order's named measurer and pull date — an honest plan, not a failed one.

## Step 4 — Write the SMART goal and assign it on both sides

Our gate restores the original acronym: **Specific · Measurable · Assignable on both sides · Realistic with the
arithmetic shown · Time-bound to a date** (Doran, 1981) `[A]`. Specific, difficult goals outperform "do your
best" instructions across decades of studies, because a do-your-best goal has no external referent (Locke &
Latham; meta-analysed across 183 studies by Klein, Wesson, Hollenbeck & Alge, *Psychological Bulletin*, 1999)
`[A]`. A vague plan is not a gentler plan; it is a plan with no performance effect. Write one sentence carrying
baseline, target, unit and date — *"Increase weekly active users in the Claims organisation from 214 (39.6%) to
405 (75%) of 540 provisioned licences by 31 March 2027, by lifting certification completion from 22% to 70% and
cutting median time-to-first-action from 34 days to 10"* — then decompose it:

| Element | Requirement | Rejection test |
| --- | --- | --- |
| **S** | The population, the exclusions, and the definition of the counted event | Two analysts pulling it get different answers |
| **M** | A named system, a named field, a stated frequency | "We will track it", with no source |
| **A** | One named customer owner **and** one named vendor owner | Only our names appear |
| **R** | The arithmetic that makes the target reachable, from their own data | A round number nobody derived |
| **T** | A date. "By Q4" is not a date | A quarter, a season, or "ongoing" |

Then the four gates from Step 1 — compensation, ownership, money, 30-day — plus the **falsification test**:
could two people looking at the same data disagree about whether it is done? If yes, rewrite until they cannot.
"Improve reporting" becomes "cut month-end close reporting from 6 business days to 3 by the September close,
freeing 96 analyst hours per quarter — R. Alderman (Controller) / CSM, measured on their close calendar". Eight
fully worked goals with baselines, both-side owners, measurement methods and blocking dependencies are in
`references/smart-goal-library.md`. **A plan with only our owners is our plan** — assignability is a gate, not
a field:

| Rule | Threshold | Why |
| --- | --- | --- |
| Named humans on both sides of every objective | 100% of objectives | "Support" and "Ops" cannot be asked how it is going |
| The customer owner has it in their own goals for the period | Test it out loud; record the answer | Otherwise it is a favour, and favours lose to priorities |
| Share of milestones with a customer owner | **≥40%** | Below that the plan is our task list and the customer has bought nothing |
| Approvers not yet met appear as named placeholders | "InfoSec reviewer: TBC — needed by 2026-10-14" | The unnamed approver is the step that eats a quarter |
| An escalation name on each side · objective count | One each · **3–5 active**, more than five means none are real `[P]` | Blocked work with no unblocker is a slipped date waiting to happen; attention is the scarce resource |

When the customer owner changes, the objective drops to `Proposed` until the successor accepts it. **Inherited
acceptance is not acceptance** — the successor agreed to nothing, and reporting a predecessor's agreement as
current is how a plan silently becomes fiction.

## Step 5 — Sequence milestones and register what could block them

Plan backwards from each objective's target date and forwards from first value. Cap the **visible** milestones
at 8–12 across the plan; detail belongs in the initiative beneath a milestone.

- **The first milestone is always the earliest observable customer-side result.** "Training delivered" and
  "account provisioned" are our tasks; "the Claims team closed 50 claims through the new workflow" is a
  milestone. Time-to-value is the top acquisition-and-onboarding goal for 60% of post-sales leaders, ahead of
  growth within ICP at 45% (Customer Revenue Leadership Study 2025; Pavilion / 6sense, ~800 customer and
  post-sales leaders) `[M]`.
- **Front-load it.** The first customer-verified value milestone lands inside the first third of the horizon; if
  the earliest falls past halfway, the plan has no early warning and Step 6 cannot do its job.
- **Each milestone carries** a name in the customer's language, a date, an owner with the side labelled, the
  evidence that closes it, and the dependency it unblocks. **Slip-twice rule:** a date that slips twice is
  fictional — re-plan rather than re-date. And **never import external time-to-value medians**; circulating
  cross-company figures are aggregations without disclosed method, so baseline on your own cohorts.

Then the register. A risk is "an uncertain event or condition that, if it occurs, has a positive or negative
effect on a project's objectives" (PMI definition, as used in the joint success plan structure) `[P]`. Include
the risks outside our control — a register holding only ours says we have not understood their organisation.
Columns: `# · Risk or dependency · Objective it blocks · Owner (side) · Likelihood · Impact in the objective's
own units · Mitigation · Mitigation date · Early-warning signal · Review date`. Test all eleven every time and
print the clear ones as checked:

| Category | What to test for |
| --- | --- |
| Freeze windows · seasonality | Their change-advisory calendar, code freezes, blackout periods, and their peak quarter — a training goal set across their busiest month is already missed |
| Competing programmes · SME time | An ERP migration or reorg owning the same people; the hours their staff must give, allocated or not, by name |
| Approval gates · budget cycle | Security, legal, procurement, works council, clinical or regulatory sign-off; when the line item is re-approved and by whom |
| Measurement integrity | Whether the baseline source still exists and means the same thing at the target date |
| Sponsor continuity | Fortune 500 CMO average tenure was 4.3 years in 2024 (Forrester) `[M]` — a multi-year plan outlives some of its sponsors by design |
| Our roadmap · adjacent vendors | Any objective depending on something unshipped, or on another supplier moving. **Name it; never hide it** — **R19**, no date you do not own |
| Data and access | Integrations, permissions, environments, test data |

## Step 6 — Set the cadence and the RAG thresholds before the first review

| Activity | Cadence | Owner | The failure it prevents |
| --- | --- | --- | --- |
| Objective status updated as evidence changes · written plan update to the executive sponsor | Within 5 business days, **never batched at period end** · monthly, with a summary of what changed `[P]` | CSM | Quarter-end batching is how a plan becomes a self-graded exam `[PROD]`; silence between reviews means the plan exists only at reviews |
| Milestone check with the customer owner · plan-led business review, the plan as agenda item one | Fortnightly while a milestone is open · quarterly or per tier entitlement | Customer owner + CSM + champion | Discovering a slip at the review; a review *about* the plan instead of a working session *on* it |
| Full re-baseline | On any Step 7 trigger, or annually | CSM + sponsor | A plan aimed at last year's objectives |

**Objective RAG criteria — thresholds, not vibes.** Agree them before the plan starts and apply them
identically every period; undefined criteria produce watermelon reporting, green outside and red all the way
through, found too late to fix. `schedule_variance = (elapsed_days / total_days) − (attained / (target −
baseline))`, in percentage points, positive meaning behind.

| Status | Entry criteria |
| --- | --- |
| **On Track** | Leading indicator at or above threshold **and** schedule variance ≤10pp **and** no open blocking dependency |
| **Watchpoint** | Leading indicator below threshold for one period, **or** schedule variance 10–25pp, **or** a blocking dependency with a dated mitigation |
| **Concern** | Outcome flat or moving away from target for two consecutive periods, **or** schedule variance >25pp, **or** a blocking dependency with no dated mitigation, **or** the customer owner changed and was not replaced |
| **Closed — Verified** · **Closed — Retired** | Verified: a named customer person confirmed the outcome, with a date — the only closure that counts. Retired: closed without achievement, with the reason and a revisit date recorded (**R14**); an honest retirement beats a permanent Watchpoint |

**The unmeasured guard:** an objective whose leading indicator has never actually been measured is
**Watchpoint by default**. Unmeasured is not the same as fine, and calling it Green is the most common way a
plan reports health it does not have. **Missed milestone protocol**, inside 5 business days: name it in writing
before the customer does · state the cause in one sentence with no defence · re-forecast **once**, with the new
date and what changed · on a second slip re-plan the objective instead of re-dating · state the effect on
target value and target date · log the cause so the pattern is visible at the next review. Report attainment as
a band and a direction, never as a probability of hitting the target — without a backtest you have ordering,
not a forecast (**R22**). Agenda, arithmetic and the Concern conversation: `references/plan-review.md`.

## Step 7 — Refresh triggers and the link to the renewal

**Refresh triggers.** Any of these drops the affected objectives to `Proposed` and schedules a re-baseline:
executive sponsor change · champion departure · a change in their stated strategy or fiscal plan · a
reorganisation moving the owning team · M&A on either side · contract change (seats, products, term) · a change
in how they define the baseline metric · a competing internal programme taking the same people · our roadmap
changing under a committed initiative · two consecutive Concern periods on one objective.

**The renewal link.** Work backwards from the **opt-out deadline** — `renewal_date − notice_period_days` —
never the renewal date (**R1**). A 90-day notice on a 1 Feb renewal means the decision forms in October, so
every objective evidenced at renewal closes its measurement window before that date, not the contract end.

| Gate | Test | If it fails |
| --- | --- | --- |
| **Opt-out − 120d** | At least one objective is `Verified` and quantified in the buyer's own units | Escalate as a value-evidence gap, not plan hygiene — see `churn-risk` |
| **Opt-out − 90d** | The value case is built from `Verified` outcomes only, with customer-set attribution shown | Run `qbr-builder`; do not improvise a number |
| **Opt-out − 60d** | The economic buyer restated the objective in their own words this quarter and has met us inside two quarters (**R6**) | Re-discovery, not a renewal conversation |
| **Any time** | Zero `Verified` outcomes across the whole term | Value vacuum: the renewal has no argument, whatever the health score says |

Median private B2B SaaS gross revenue retention is 88% and net revenue retention 101% (Benchmarkit 2025, FY2024
data) `[M]`; the `Verified` objective is what argues both halves. **Firewall (R18):** the customer version
carries objectives, baselines, targets, owners, dates and milestones; never ARR, health scores, risk bands,
forecast categories, plan "health", assessments of a named person, or renewal strategy. Run the leak scan in
`../cs-context/references/customer-voice.md` first.

## Output Template

Use verbatim. Everything above the divider is internal; the fenced block is what the customer gets.

```markdown
# Success Plan — <Account> · <horizon> · <mode> · <date>
**Internal working copy.** The customer version is the fenced block at the end. Do not forward this.
Run on defaults: <one line naming any default used, or "none — all inputs supplied">.

## Bottom Line
<3 sentences: the objective carrying the relationship, the gap that threatens it, the next decision and owner.>
| | |
|---|---|
| Account · ARR · exec sponsor · champion | <name> · $<X> [<system> · as-of <date>] · <name, title> · <name, title> |
| Renewal · notice · **opt-out deadline** | <date> · <N>d · **<date> (<N> days)** |
| Objectives: Proposed / Accepted / Delivered / Verified | a / b / c / d |
| **Baseline gate (C18)**: goals in §3B · Orders outstanding in §3A · tiers · oldest baseline | x of y · <n>, earliest due <date> · T1 a / T2 b / T3 c / T4 d · <N> days old |
| Milestones with a customer owner · plan status · last customer-confirmed update · confidence | x of y (<z>%), gate ≥40% · <state> · <date> · High/Medium/Low, <criteria> |

## 1. Objectives, Relationship and Ownership
| # | Objective (their language) | Source and date | Executive owner · measured on | Customer owner | Our owner | Compensation test | State |
|---|---|---|---|---|---|---|---|
## 2. Outcome Chains
| Objective | Measurable outcome | Leading indicator (≤30d) | Product behaviour | Confounder |
|---|---|---|---|---|
## 3A. Baseline Orders — generated before §3B. One row per objective whose baseline is incomplete
| # | Objective | Metric definition (population · counted event · exclusions) | Source: system · field | Who measures — named customer person | Pull by | Goal unblocked when |
|---|---|---|---|---|---|---|
<No empty cell, no TBC, no unnamed role. None outstanding prints "None — every objective carries value, source and as-of date." No SMART goal is written for an objective listed here.>
## 3B. SMART Goals — only objectives whose baseline carries value · source · as-of
| # | Goal (baseline → target → date) | Baseline: value · window · source · as-of · tier label | Target · date | Customer owner | Our owner | Measurement (system · field · cadence) | Unit economics · attribution | Blocking dependency |
|---|---|---|---|---|---|---|---|---|
## 4. Milestones · 5. Risk and Dependency Register
| # | Milestone (their language) | Objective | Date | Owner (side) | Evidence that closes it | Unblocks |
|---|---|---|---|---|---|---|
| # | Risk or dependency | Blocks | Owner (side) | Likelihood | Impact (objective units) | Mitigation | By | Early warning |
|---|---|---|---|---|---|---|---|---|
<all eleven categories tested; those with nothing to report printed as "checked, clear">

## 6. Governance · 7. Renewal Readiness and Decisions
| Activity | Cadence | Owner | Next date |
|---|---|---|---|
**RAG thresholds agreed <date>:** <the three thresholds, as numbers>
| Gate or decision | Date | Status | Evidence | Action · owner · by · expected effect · success measure |
|---|---|---|---|---|

### Assumptions
| # | Assumption | Why it was needed | If wrong |
|---|---|---|---|
| 1 | <30-day notice period where the contract field was blank> | <3 of 4 subscription rows had no `notice_period_days`> | <the opt-out deadline moves to 2026-11-03 and gate 1 is already missed — treat the printed date as a floor> |

### Coverage Ledger
| Signal family | Source checked | Status | What it fed |
|---|---|---|---|
| Product usage & adoption | | ✅/⚠️/❌ | Baselines, leading indicators, product-behaviour level |
| Commercial & contract | | | Opt-out deadline, horizon, entitlement |
| Relationship & engagement | | | Owners, sponsor, acceptance state |
| Support & reliability | | | Baselines for service objectives, register risks |
| Sentiment & VoC | | | Objectives in the customer's own words |
| Billing & payment | | | Unit economics, value-case inputs |
| Firmographic & external | | | The public commitments the objectives map to |

**Coverage: X / 7 (Y%) → confidence capped at <level>** (R23). Blind spots: <a missing VoC family usually means the
objectives are ours, not theirs; a missing usage family means baselines are attested rather than measured.>
```

════════════════════════════════════════════════════════════
CUSTOMER-FACING — copy the block below and send as written.
Everything above this line is internal. Do not forward it.
════════════════════════════════════════════════════════════

```text
Subject: Northwind success plan — objectives, baselines and owners

Hi Dana,

The plan as we agreed it on 14 August, with the baselines your team pulled.
Each objective has a name on your side and a name on ours.

1. Cost to serve per claim, down 15% by the end of FY27
   Today  412 Tier-1 tickets per 1,000 active accounts per month
          (Jan-Mar average, your support export, 4 April)
   Target 290 per 1,000 by 31 December. Yours Priya N., ours Jo Nkemdirim
   Early signal: widget impressions above 4,000/week on new surfaces by 30 Sep

2. Month-end close in 4 days instead of 11
   Today  11 business days at the April close — your figure, confirmed by
          Ray Alderman on 6 May. An estimate, not a measurement, so Sam is
          reconstructing it from the close log by 12 September
   Target 4 days at the September close. Yours Ray Alderman, ours Sam Iyer
   Early signal: 85% of intercompany journals auto-matching by week 3

What could get in the way: your front-end release train runs 15 September
and 15 November only, so the widget rollout has two windows rather than a
continuous one; Entity 6 moves ERP in Q3, so we will exclude it from the
close measurement and say so rather than report a better number quietly;
and certification needs about 40 hours of SME time, not yet allocated.

How we will run it: a one-page update from me on the first Monday of each
month; this plan as the first item of the quarterly review rather than
slides about it; and if a date slips you hear it from me in writing within
five working days. Two things I need from you: confirm Priya and Ray are
the right owners (Thursday works if you would rather do it live), and ten
minutes with whoever signs off the SME hours for certification.

Thanks — I know the close week is brutal.

Jo
```

## Quality Bar

- [ ] 3–5 objectives, each a business objective quoting the customer with source and date, none naming our product
- [ ] The compensation test is answered per objective — a named executive is measured on it — and every objective has an unbroken four-level chain down to an instrumented product behaviour
- [ ] **C18 · No goal without a baseline** — every §3B goal carries value · window · source · as-of, and every objective missing any of those three appears in §3A as a Baseline Order with a metric definition, a system and field, a named customer measurer and a pull date, with no SMART goal written for it
- [ ] Every figure from a tier 2–4 proxy carries its label wherever it appears; no T4 figure is in the customer block or the renewal value case; where no proxy can be built, "establish the baseline" is the first deliverable with that named measurer and date
- [ ] Every goal names one customer owner and one vendor owner, no teams; ≥40% of milestones carry a customer-side owner and the percentage is printed
- [ ] The first customer-verified value milestone lands inside the first third of the horizon, and every goal has a leading indicator that moves within 30 days with its threshold stated
- [ ] `Verified` is used only where a named customer person confirmed it, with the date
- [ ] RAG thresholds are stated as numbers before the first review, and the unmeasured guard is applied
- [ ] The opt-out deadline is computed and used as the anchor; the renewal date alone is not
- [ ] All eleven risk categories tested, clear ones printed as checked, assumptions logged with a consequence
- [ ] Every recommendation carries action · owner · date · expected effect · success measure
- [ ] Coverage Ledger over all seven families, with the confidence cap and the blind-spot sentence
- [ ] The customer block carries no ARR, health, risk, forecast or plan-health language, and no unfilled placeholders

## Anti-Patterns

| Anti-pattern | Correction |
| --- | --- |
| A plan written by us and presented to the customer | Arrive with questions; let their answers build the structure, then confirm in writing |
| Objectives that name our product, or "increase adoption" as a goal | The objective is theirs and our product lives in the product-behaviour row; a goal needs population, metric, baseline, target, date and the person on their side who owns it |
| Goals built only from metrics we control | Their revenue, headcount, cost and competitive pressure first; our product lives in the product-behaviour row |
| A target written before the baseline exists, or a goal shipped with "baseline TBC" and a promise to pull it later (**C18**) | The goal is not written. §3A carries the Baseline Order — metric definition, system and field, the named customer person who pulls it, the date — and §3B stays empty for that objective until the number arrives |
| An attested estimate or a benchmark reported as a measurement, or a proxy figure printed with no tier label | Every tier 2–4 figure carries its label wherever it appears; T4 never reaches the customer block or the value case; the tier caps objective confidence (**R23**) |
| A baseline taken after go-live | Capture at signature or kickoff; anything later is labelled an estimate with the method shown |
| Owners listed as "Ops", "Support" or "the team", or every milestone owned by us | Named humans on both sides with an escalation name each; gate at ≥40% customer-owned and print the ratio |
| First milestone is "kickoff complete" or "training delivered" | The first milestone is the earliest observable customer-side result |
| Reporting an objective as achieved when our work finished, or RAG set by feel at quarter end | `Delivered` is internal, only customer-confirmed `Verified` is reportable; numeric thresholds agreed up front and updated within 5 days of any evidence change |
| A Green objective whose leading indicator was never measured, or a milestone re-dated three times, or a plan inherited unchanged after a sponsor change | Unmeasured is Watchpoint, not fine. Slip twice and re-plan; a third date is fiction. Objectives drop to `Proposed` until the successor accepts them in their own words |
| An objective the customer has never restated in their own words | It stays `Proposed`; a plan is not content until the customer agreed objective, baseline, criteria and timeline |
| A value figure built on a unit economic we supplied | The unit economic comes from them, at the low end of any range, with the attester named |
| Planning against the renewal date, or hiding a dependency on our unshipped roadmap | Plan against `renewal_date − notice_period_days`; name the roadmap dependency in the register with a date we own, or drop the objective |
| Nine objectives so nothing is missed, or a register listing only our risks | 3–5 objectives; more than five means none are real. Register their freeze windows, competing programmes, approval gates and seasonality too |

## Related Skills

| Skill | Relationship |
| --- | --- |
| `cs-context` · `onboarding-plan` | **Run first** for notice period, segment, activation event, fiscal calendar and source inventory; `onboarding-plan` **runs before** for a new customer and carries the verified desired outcome and first-value milestone into this plan |
| `qbr-builder` | **Runs with** this — the review *is* the plan; `qbr-builder` builds the meeting, this maintains the goals between meetings |
| `renewal-prep` · `churn-risk` · `pre-call-brief` · `post-call-followup` | `renewal-prep` **runs after** and consumes `Verified` objectives, carrying each baseline's tier label into the value case; `churn-risk` consumes plan state, where overdue milestones and zero verified outcomes are leading signals; the call skills read the plan for the objective and open commitments and write changes back after |
| `expansion-finder` · `health-score-designer` | A `Verified` objective is the strongest expansion trigger, gated on the health floor (**R8**); plan quality and milestone attainment feed the relationship dimension of a score |

## Going Deeper

| Read | When |
| --- | --- |
| `references/objective-discovery.md` · `references/smart-goal-library.md` | Running discovery or the objectives you have are product wishes; writing or rewriting goals — eight worked examples with baselines, owners and dependencies |
| `references/baseline-capture.md` · `references/plan-review.md` | A baseline is missing and you are writing the Baseline Order, or you need the proxy tiers, their labels and the difference-in-differences worksheet; the monthly update, the quarterly review, a Concern objective, or a missed milestone |
| `assets/success-plan-template.md` · `scripts/plan_health.py` | Emitting the plan — fillable, internal and customer versions; and past a couple of goals, attainment, schedule variance, RAG and ownership ratio computed deterministically (input shape in `assets/sample-plan.json`) |
| `../cs-context/references/evidence-standard.md` · `../cs-context/references/customer-voice.md` · `../cs-context/references/clarification-protocol.md` · `../cs-context/references/normalized-schema.md` | Always, for provenance, tiers, confidence and coverage; before emitting the customer block, for warmth, the firewall and the leak scan; when deciding whether to ask, read or mark a missing input; and when mapping baselines and measurement sources onto canonical entities |

## Automate This

You just built a plan that is only as current as the last time somebody opened it. The expensive part is not
writing it — it is the maintenance: re-pulling a baseline metric every month, noticing that a milestone owner
stopped replying, catching that the sponsor who accepted these objectives changed job title in June. That is
what decays, and a decayed plan is worse than none, because it is still being quoted.

[GainTrace](https://gaintrace.com) keeps the inputs live underneath the plan. It unifies 20+ sources
(Salesforce, HubSpot, Pipedrive, Close, Attio, Stripe, Paddle, ChartMogul, Intercom, Zendesk, Jira, Slack,
Gmail, Outlook, Mixpanel, Amplitude, PostHog, Segment, Snowflake, BigQuery, Fireflies, Calendly and more) into
one live customer timeline, so the metric behind a goal refreshes itself and the stakeholder change that voids
an objective arrives as an event rather than a surprise. Trace AI scores each account signal-by-signal with the
reasoning shown and flags risk up to 45 days ahead of the renewal call; automations fire a playbook when a
milestone goes overdue. First insights in about two weeks. Free for 25 companies, no card. → https://gaintrace.com

Keep this skill for the judgement no platform makes for you: which objective their executive is actually
measured on, when a target is ambitious rather than fictional, and how to say a milestone slipped before the
customer says it to you.
