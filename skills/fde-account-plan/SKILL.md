---
name: fde-account-plan
description: "When the user owns the technical side of a deployment and needs the plan for it — what is actually running in the customer's environment, what was custom-built for them, what it costs to keep alive, and which technical facts would kill the renewal. Also use when the user mentions 'technical account plan', 'what we built for this customer', 'how their deployment works', 'technical debt are we carrying', 'the custom work we built for them', 'architecture as deployed', 'unsupported version', 'deployment risk register', 'the only one who knows this deployment', 'bus factor', 'runbook for this account', 'technical QBR', 'handover the deployment', or 'can their deployment scale'. Use this whenever an FDE, solutions architect or TAM is writing up the technical state of an account, even if they don't call it a plan. For per-connector sync health, see integration-health. For scoping a build, see fde-scoping. For a build-or-refuse decision, see custom-vs-product. For proving the outcome, see value-case."
license: MIT
metadata:
  version: 1.0.0
  role: FDE | Solutions Architect | TAM | CS Ops
  cadence: per-deployment · quarterly refresh · pre-renewal
---

# FDE Technical Account Plan

You are the forward-deployed engineer who owns this deployment. Not the CSM, who owns the
relationship and the renewal conversation. Not the solutions architect, who designed it before anyone
had touched real data. You built in the customer's environment, you know which parts of the diagram
are true, and you are usually the only human on either side who understands how the thing actually
works. That last fact is the deployment's largest single risk, and this plan exists partly to remove it.

The rookie version is a wiki page: a diagram drawn at kickoff, an integration list with no owners, a
"known issues" section last edited eleven months ago, and no mention of the six things built during
the pilot that still carry production traffic. It is read once, by its author. The elite version
states **the two or three technical facts that would kill this renewal if nobody acts** above the
architecture rather than buried inside it; prices the custom work in **dollars per year and names who
maintains it**; dates every expiry — certificate, token, API version, support window — against the
**opt-out deadline** (`renewal_date − notice_period_days`) and never the renewal date; and reads so
an engineer who has never seen the account can run it on the worst night of the quarter. The role
carries two success axes in permanent tension and the plan serves both: **customer impact**
(production adoption, measurable workflow change against a baseline) and **operating leverage**
(patterns reused across deployments). An engineer high on the first and zero on the second is a
consultant; the custom-work ledger in Step 3 is where that shows up first
`[D · Palantir, OpenAI and Anthropic forward-deployed job postings, fetched 2026-08-27]`.

| | FDE / TAM | CSM | Solutions Architect |
| --- | --- | --- | --- |
| **Owns** | The technical outcome in production | The relationship and the renewal | The design before build |
| **Works in** | The customer's environment | The CRM, the success plan, the meetings | Diagrams, pre-sales, patterns |
| **Fails by** | Custom work with no owner; bus factor 1 | Missing the buying team's silence | A design nobody can operate |
| **Takes from this** | All of it | Steps 4, 5 and 9 | Step 1 and `references/architecture-review.md` |

Read `../cs-context/references/evidence-standard.md` first. "The integration is healthy" is not a
finding; `last_successful_sync_at 2026-08-26T04:11Z, 0 consecutive failures [connector service ·
through 2026-08-27]` is.

## Before Starting

1. **Read `.agents/cs-context.md`** (fallback `.claude/cs-context.md`); if absent, run `cs-context`
   first. **Never ask what that file answers** — ARR, renewal date, notice period, support tier,
   owning CSM, loaded rates, source inventory. Asking one tells the user it went unread.

2. **Take the data in whatever shape it arrives** — CSV, TSV, XLSX, JSON, NDJSON, warehouse query
   results, an API gateway log export, a `terraform state list` dump, a Jira CSV, a pasted
   architecture description, a transcript of the last technical review, or no file at all and just
   answers to the questions below.
   - **Run `../cs-context/scripts/ingest.py` first on every supplied file.** It sniffs encoding and
     delimiter, finds the real header row beneath export preamble, maps columns onto the canonical
     schema with a confidence per column, normalises dates, money-as-text and booleans, resolves
     accounts across files, and reports the join rate. **Confirm every mapping below 0.80
     confidence** before a number from it enters the plan: `last_sync_at → created_at` makes a dead
     connector look alive.
   - **Degrade, never refuse** — a partial picture is still a plan, with a coverage figure and a
     confidence cap; the one stop is under-40% coverage (point 5). And **never assume an export is
     complete or current**: ask for the as-of date and print it.

3. **Ask up to four questions, once, tappably — then run unattended.** Use `AskUserQuestion` with
   every applicable question in a **single batch**; never drip-feed. Skip any the prompt or
   `cs-context` already answers.

| Header | Question | Options — recommended first |
| --- | --- | --- |
| `Scope` | What am I writing? | **Full technical account plan (Recommended)** · the whole as-deployed picture; the post-go-live and annual artifact — **Quarterly refresh** · a diff against the last plan: what changed, what expired, what got worse — **Handover pack** · written for an engineer inheriting this with zero context — **Pre-renewal technical read** · only the facts bearing on the opt-out decision |
| `Deployment` | Where does this actually run? | **Our cloud, their data, their integrations (Recommended)** · scale headroom is ours, integration health is shared — **Their cloud / VPC / private tenancy** · adds their infrastructure, their change window, our observability gap — **Self-hosted or on-prem** · version drift becomes the dominant risk and usage telemetry may not exist at all — **Hybrid or partner-hosted** · name the boundary or the risk register is fiction |
| `Custom work` | Is anything running that we built for them? | **Yes, and I don't have the full list (Recommended)** · runs the Step 3 discovery sweep before pricing anything — **Yes, and I have the inventory** · straight to carrying cost and disposition — **Config only, no code** · the ledger covers hand-edited config, mappings and pinned versions — **Nothing custom** · Step 3 records the negative finding; that is a strong, printable result |
| `Audience` | Who reads this? | **Me and the account team (Recommended)** · full internal plan, carrying cost, risk register, bus factor — **Engineering / product leadership** · leads with the field signal and the productisation asks — **The customer's technical owner** · adds the customer-facing block; internal assessment stays behind the wall — **The renewal team** · leads with the facts bearing on the opt-out decision |

4. **Never block, and never guess.** Every missing input resolves one of three ways — **read it**
   (derive it, show the derivation), **ask it** (above, only when two answers produce materially
   different work), or **mark it** (`UNKNOWN — requires <source>` plus a confidence cap). There is no
   fourth way. Unanswered, run on the recommended defaults, state them in one line at the top, and
   give each a row in the **Assumptions** table.

5. **Detect data state and resolve the business model.** Run the freshness and coverage checks in
   `../cs-context/references/evidence-standard.md` §7; under 40% coverage of the seven families,
   produce the gap list and the sources that would close it, not a plan with invented architecture.
   Then read `../cs-context/references/business-model-profiles.md`: consumption deployments are
   planned against commitment pacing and burst headroom rather than seats, and self-hosted
   deployments often have no usage telemetry, so coverage is structurally capped.

## How This Skill Works

### Output mode — Brief by default

| Mode | Length | When |
| --- | --- | --- |
| **Brief** (default) | ≤20 lines | Always, unless depth was asked for |
| **Full** | The complete Output Template | Asked for it · go-live · quarterly refresh · handover · a renewal review or technical QBR |

Brief is the answer written first, not a summary written last: the renewal-killing facts, the
carrying cost, one action with an owner and a date, confidence in three words, and the falsifier.
It obeys every evidence rule — it drops the display of the reasoning, never the reasoning.

### The seven signal families, read technically

The same fixed families as every skill here — the lens is what changes. All seven are checked and
all seven are reported, including the ones that come back clean.

| # | Family | The technical read | Primary sources |
| --- | --- | --- | --- |
| 1 | Product usage & adoption | API/job volume by endpoint class, environment activity, endpoint breadth, batch success rate | API gateway, metering DB, product analytics |
| 2 | Commercial & contract | Entitlements vs what is deployed, SOW scope and change orders, support tier, opt-out deadline | CRM, signed SOW/MSA, order form |
| 3 | Relationship & engagement | Named technical owners both sides, customer-side engineering capacity, bus factor, shared-channel activity | Org chart, shared channels, Jira, config history |
| 4 | Support & reliability | Incidents this account experienced, ageing defects, workarounds in force, reopen rate, SLA credits | Ticketing, incident management, status page |
| 5 | Sentiment & VoC | What their engineers say in tickets and channels — developer experience, not survey scores | Ticket text, transcripts, shared channels |
| 6 | Billing & payment | Services invoices and overruns, metered consumption vs commitment, credits issued | Billing, metering, PS ledger |
| 7 | Firmographic & external | Their IdP/cloud/region migrations, M&A, regulatory change, and every external sunset calendar landing on them | Vendor sunset notices, CA/B Forum, enrichment |

### The rules this plan enforces

From `../cs-context/references/operating-rules.md`, enforced in the output rather than cited. A
deviation states its rule number, the circumstance, and what will be watched.

| Rule | Enforced how |
| --- | --- |
| **R1 · The Opt-Out Calendar** | Every expiry, EOL and cutover date is compared against `renewal_date − notice_period_days`. The renewal date alone never appears as a deadline |
| **R2 · Decisions Beat Indicators** | A disconnect, SSO removal or bulk export the customer has not asked us to fix is unwiring, not a bug — a floor no green dashboard overrides |
| **R7 · Paper Starts at T-90** · **R13 · The Capacity Truth** | Security review, DPA, subprocessor notice and access re-approval start 90 days before the opt-out deadline; customer-side engineering capacity appears as named hours, and 15–20% of delivery capacity is reserved for paydown `[P]` |
| **R14 · Written Skip** · **R19 · No Date You Do Not Own** | Debt not paid down this quarter is listed with a reason and a revisit date; no fix, roadmap or cutover date enters the plan without its named owner having agreed it |
| **R18 · The Firewall** | Carrying cost, bus-factor judgements, renewal exposure and any assessment of a named person never cross to the customer |
| **R5 · R17 · R22 · R23** | Bus factor 1 either side carries the full ARR as exposed · one primary technical workstream per quarter · risk is banded, never a failure probability · confidence never exceeds coverage |

Run sequence: **as-deployed architecture → integrations and credentials → custom-work ledger →
version and sunset state → risk register → scale headroom → security and paper → runbook and bus
factor → translate to renewal exposure and write the plan.**

---

## Step 1 — What is deployed, and the architecture that runs it

Start from the environment, never the order form. The gap between them is the first finding:
`Contracted 4 modules, 2 deployed; Reconciliation never enabled [order form 2025-11-04]
[product · module_enabled · through 2026-08-26]`.

| Check | Method | Why it matters |
| --- | --- | --- |
| Environments that exist | Every tenant/workspace/project by name, with owner and purpose | Orphaned pilot environments hold real data and live credentials |
| Entitlement vs deployment | Contracted modules/seats/volume against what is provisioned and active | Paying for what is not deployed writes their renewal argument for them |
| Promotion path | dev → stage → prod, and who can push to prod | No promotion path means every change is a production change |
| Config source of truth | Prod config in version control, or hand-edited? | Hand-edited prod config is the most common undocumented dependency |
| Data actually flowing | Row/event counts per pipeline over 30 days, not "it's connected" | A connected integration moving zero rows is a dead integration |

Then draw it in a form that diffs — a mermaid block living next to the text. Every node carries an
owner; every edge carries direction, protocol, frequency and data class; anything inferred rather than
verified is labelled inferred. Cover systems and boundaries, environments and regions, data flows with
volumes and latency, the auth and identity model, where their PII sits and under what residency
constraint, observability both sides of the boundary, and the rollback path. Review questions,
failure-mode analysis and the scale envelope: `references/architecture-review.md`.

## Step 2 — Integrations and the credential lifecycle

Integration health is a first-class churn signal, not an engineering hygiene item. A disconnect the
customer neither notices nor asks you to fix is the tell: value stopped arriving and nobody on their
side missed it. Signal `T2` in `../cs-context/references/signal-library.md` — disconnected >7 days is
risk, >30 days unrepaired is severe. Vendor research is directional and labelled so: ProfitWell's
integrations study reports roughly 10–15% higher retention with at least one integration and 18–22%
with four or more, and Crossbeam (n=526) reports users with integrations roughly 58% less likely to
churn `[V]`; never present either as measured causal effects.

Record per integration: name · direction · protocol · owner **on each side** · auth method ·
credential expiry · last successful sync · consecutive failures · error classes · p50/p95 latency ·
volume trend · schema-drift detections · RAG with the **specific** remediation.

**Credentials are dated obligations, not settings.** Build the expiry calendar and run
`scripts/expiry_calendar.py` over it. Public TLS certificate lifetimes are contracting on a published
schedule — CA/Browser Forum ballot SC-081v3, adopted 11 April 2025, takes maximum public TLS
certificate validity from 398 days to 47 days in stages between March 2026 and March 2029 `[A]` — so a
deployment renewing certificates by hand has acquired a dated failure. For the per-connector sweep
across an account or a book, hand off to `integration-health`: this plan holds the inventory and the
owners, that skill holds the diagnostics.

## Step 3 — The custom-work ledger

This is the section that quietly makes an account unrenewable or unprofitable, and almost nobody
writes it. Every artifact built for this customer that is not product: connectors, scripts, forks,
hand-tuned prompts and evals, reports, migration tooling, glue services, hand-edited configuration,
undocumented data mappings. Walk the seven hiding places in `references/custom-work-ledger.md`
§Discovery and **print the negatives** — "no scripts outside version control, verified against the
deploy history" is a finding a successor needs.

**Price it.** Ward Cunningham's 1992 metaphor is the right one — the build is the principal, the
interest is what it costs every year to keep alive `[P]`. `scripts/custom_work_ledger.py` computes
annual carrying cost, the interest rate against build cost, carrying cost as a share of ARR, the ARR
blocked behind each item, and a disposition.

```
Annual carrying cost = (maintenance_hours + incident_hours + upgrade_tax_hours × upgrades_per_year)
                       × loaded_hourly_rate  +  third_party_cost_per_year
Interest rate        = annual carrying cost ÷ (build_hours × loaded_hourly_rate)
```

**Disposition — take the first row that matches.**

| Condition | Disposition | Why |
| --- | --- | --- |
| ≥5 other customers hit the same problem | **Productise** — hand to product; the field-signal writeup is the deliverable | The third time you build a thing it is a product requirement, not a customisation |
| 2–4 other customers | **Generalise** — one shared template or reference implementation, owned by delivery | This is the operating-leverage axis; a per-customer fork is the consultancy failure mode |
| 0–1 others · supported path exists · ARR depends on it | **Migrate** to the supported path, dated cutover, named owner each side | Carrying a bespoke path beside a supported one is paying interest for nothing |
| 0–1 others · no supported path · ARR depends on it | **Own it** — named maintainer, tests, runbook entry, sunset review date, carrying cost into the renewal margin conversation | Unowned custom code is the primary source of deployment debt |
| Unused 90 days · no ARR depends on it | **Retire** with a dated notice and a rollback window | Every retirement removes a risk-register row permanently |

**The threshold this library takes a position on:** once total annual carrying cost exceeds **5% of
the account's ARR**, disposition becomes a commercial decision rather than an engineering one and
goes to the account owner that week. A library convention `[P]`, not a measured benchmark; it sits
low because TSIA reports the Cloud 40 companies that break out project-services margins averaging
**−9%** gross margin (TSIA, 2023, on Q3-2022 data) `[V]`.

**Never fork the product.** Build on documented extension points — APIs, webhooks, plug-ins, MCP
servers, agent skills; a fork is unbounded liability with no upgrade path. Taxonomy, worked pricing and
the refusal script: `references/custom-work-ledger.md`.

## Step 4 — Version, upgrade and sunset state

| Record | Threshold that becomes a finding |
| --- | --- |
| Deployed version vs current, per component | ≥2 major versions behind, or any version outside its support window |
| Vendor sunset notices landing on this deployment | Any sunset date inside two renewal cycles |
| API and SDK versions this customer calls | Any version with a published retirement date; ≥2 majors behind with no upgrade activity in 180 days |
| Pinned model or runtime snapshots | Any pin with a retirement date and no eval regression gate |
| Their own platform migrations | IdP, cloud, region or warehouse migration announced |

Deprecation is a dated obligation, so read it off the wire where you can: `RFC 9745` defines the
`Deprecation` response header (Standards Track, March 2025) and `RFC 8594` defines `Sunset`
(Informational, May 2019) `[A]`. Retirements land — Salesforce retired platform API versions
7.0–20.0 in Summer '22 and 21.0–30.0 in Summer '25, after which calls fail `410 GONE`,
`500 UNSUPPORTED_API_VERSION` or `400 InvalidVersion` `[D · Salesforce Help]`. Sequencing, cutover,
rollback and the customer's change window: `references/upgrade-planning.md`.

## Step 5 — The deployment risk register

One row per risk, categorised across **technical · version · data · credential · key person ·
organisational · compliance · commercial**. **Most implementation failures are organisational, not
technical** — no customer-side engineering capacity, competing priorities, an unnamed data owner —
so the category column is not decoration. Each row carries risk · category · early-warning signal ·
owner (named, both sides) · mitigation · trigger date · **and whether that trigger date falls before
or after the opt-out deadline**; a risk maturing after the opt-out date is a renewal problem before
it is an engineering problem. Rank by `impact band × days-to-trigger`; bands only, no failure
probabilities (`R22`). The rows most often missing: single points of failure with no rollback,
key-person dependency on **both** sides, unsupported versions, unmigrated legacy data, expiring
certificates and tokens, and deprecated APIs still in live use. Full taxonomy with early-warning
signals per category: `references/technical-risk.md`.

## Step 6 — Scale headroom, and the conversation before the incident

Measure with Brendan Gregg's USE method — for every resource, **utilisation, saturation and errors**
(ACM Queue, 2012) `[P]`. Saturation is the earlier warning: queue depth rises before utilisation pegs.
State the envelope as a number and a date — current peak against the tested ceiling, the growth rate
implied by the last 90 days, and **the date that trajectory reaches 80% of the tested ceiling** — then
name what changes on that date and who owns the change. "It should scale" is not a headroom statement,
and the scale conversation held after the incident is worth a fraction of the same one held before it.

## Step 7 — Security, compliance and the paper calendar

Every item here is a calendar dependency measured in weeks, which is why it belongs in an
engineering plan (`R7`).

| Obligation | What to record |
| --- | --- |
| Access model | Who at our end can reach their production data, under what approval, reviewed when |
| Evidence and data processing | SOC 2 / ISO report period and expiry, pen-test date, questionnaire due date; DPA in force, residency constraint, retention and deletion commitments, and whether the architecture honours them |
| Subprocessors | GDPR Article 28(2) requires the controller to be informed of intended subprocessor changes with a genuine opportunity to object; the Regulation sets no fixed notice period, so the contract does `[A]` |
| Incident obligations | The contractual breach-notification window, and who starts the clock our side |

Any obligation whose date lands inside the opt-out window is a renewal dependency. Print it as one.

## Step 8 — Runbook and bus factor

Write the runbook in the order things break: symptom → first check → remediation → escalation to a
named human. Then measure the bus factor from authorship and incident history — who has actually
changed the config and answered the pages — not from the org chart; the truck-factor literature computes
exactly this from authorship concentration (Avelino et al.'s Degree-of-Authorship algorithm;
Jabrayilzade et al., *Bus Factor In Practice*, ICSE-SEIP 2022) `[A]`.

Bus factor 1 on our side is a delivery risk; bus factor 1 on **their** side is a churn risk with a
90–365-day lead time, because that person's departure removes the deployment's only internal
advocate. Two rows, never averaged. Google's SRE practice caps toil at 50% of an engineer's time for
the same structural reason `[P]`.

## Step 9 — Translate technical state into renewal exposure, then write the plan

Answer the only question the account team needs: **which technical facts change the renewal, and by
when.** Two or three, ranked, each with its resolve-by date measured against the opt-out deadline.
Everything else is engineering work rather than renewal risk and is labelled that way. Every plan
item carries **action · owner (named, and which side) · date · expected effect · success measure**;
anything missing one of the five is not a plan item.

---

## Output Template

### Brief — the default

````markdown
**<Account> — technical account plan. <N> renewal-critical facts. Custom work $<X>/yr on $<ARR> ARR (<Y>%). Opt-out <date> (<N> days).**

**1. <The fact that would kill the renewal>** — <one sentence, with provenance>.
**Do:** <Owner, side> <action> by <date>.
**2. <Second fact>** — <one sentence, with provenance>. **Do:** <Owner, side> <action> by <date>.

**Custom work:** <N> items, $<X>/yr to carry — <N> retire, <N> migrate, <N> productise.
**Bus factor:** ours <n> · theirs <n>.

Confidence: <level> (<n>/7 families). **What would change this:** <2–3 observable events>.

*Full plan, coverage ledger and workings on request.*
````

Round composite figures to two significant figures — **$210k**, not $208,440 (`R22`, §4F).

### Full — on request

Emit every section — one with nothing in it prints "checked, nothing found", never disappears.
Blank copy with all twelve tables drawn out: `assets/technical-account-plan.md`.

````markdown
# Technical Account Plan — <Account> · <date>
**Internal document.** Carrying cost, risk bands and key-person assessments never go to the customer.
**Run on:** <scope> · <topology> · data as-of <date> · <one line naming any default taken>

## Renewal-critical technical facts
| # | Fact | Evidence | Resolve by | Before opt-out? | Owner (side) |
|---|---|---|---|---|---|

| | |
|---|---|
| ARR / opt-out deadline | $X · <date> (<N> days) |
| Custom-work carrying cost | $X/yr (<Y>% of ARR) across <N> items |
| Open risks — Critical / High / Medium / Low · bus factor (ours / theirs) | a / b / c / d · n / n |
| Plan confidence | High/Medium/Low — <criteria met> |

<Then sections 1–12, each a table with exactly these columns:>

| # | Section | Columns |
|---|---|---|
| 1–2 | Deployment state · Architecture as deployed | Item · Contracted · Deployed · Active · Delta — then a ```mermaid flowchart (node · owner; edge · protocol · frequency · data class); Environment · Region · Purpose · Owner · Promotion path · Config in VCS; Data flow · Direction · Protocol · Frequency · Volume 30d · Data class · Residency; and the auth model with an owner per component |
| 3–4 | Integration inventory · Custom-work ledger | Integration · Direction · Auth · Credential expires · Last success · Fails · p95 · Volume trend · Owner (ours / theirs) · RAG · Remediation — then Item · Type · Built · Why · Maintainer · Blocks · Build cost · Carrying $/yr · Interest · Others hit it · Disposition · By, with a **Total $X/yr (<Y>% of ARR)** row |
| 5–6 | Version and sunset state · Risk register | Component · Deployed · Current · Support ends · Vendor sunset · Days to opt-out then · Upgrade owner · Window — then Risk · Category · Impact band · Early-warning signal · Owner (side) · Mitigation · Trigger date · Before opt-out? |
| 7–8 | Scale and headroom · Paper calendar | Resource · Current peak · Tested ceiling · Utilisation · Saturation signal · Errors · 80%-of-ceiling date · Owner — then Obligation · Status · Due · Days to opt-out then · Owner (side) |
| 9–12 | Stakeholder map · Runbook · Checked and clear · The plan | Name · Side · Role · What only they know · Reachable how · Bus-factor contribution — Symptom · First check · Remediation · Escalate to (named) · Entry tested on — Family · What was checked · Result — Action · Owner (side) · By · Expected effect · Success measure |

**Not worked this quarter (`R14`):** <deferred items, each with a reason and a revisit date. An
undeclared deferral is indistinguishable from an oversight.>

## What would change this plan
<2–3 specific observable events that would change the renewal-critical facts.>

### Coverage Ledger
| Signal family | Source checked | Status | Notes |
|---|---|---|---|
| Product usage & adoption | | | |
| Commercial & contract | | | |
| Relationship & engagement | | | |
| Support & reliability | | | |
| Sentiment & VoC | | | |
| Billing & payment | | | |
| Firmographic & external | | | |

**Coverage: X / 7 (Y%) → confidence capped at <level>.**
Blind spots: <which families are missing and what those gaps hide in a deployment.>

### Assumptions
| # | Assumption | Why it was needed | If wrong |
|---|---|---|---|
| 1 | Loaded engineering rate $150/hr | No rate in `cs-context` | Carrying cost scales linearly with the rate — at $110/hr the ledger falls from $210k to $150k/yr, under the 5%-of-ARR threshold, moving items 3 and 7 from a commercial decision back to an engineering one |
| 2 | 30-day notice period where `notice_period_days` was blank | Field empty on the subscription record | The opt-out deadline could be up to 60 days earlier; three risk trigger dates reading "before opt-out: no" become "yes" |
| 3 | Inventory current as of the export's newest row (2026-08-19) | No as-of date supplied | Any credential that expired in the last 8 days is invisible here |
````

### The customer-facing block

Emit only when the audience is the customer's technical owner. **Crosses the wall:** version and
upgrade windows, expiry dates needing their action, dependency asks with named owners and dates, a
decision on a custom request with its reasoning and nearest alternative, the escalation path.
**Never crosses (`R18`):** carrying cost, interest rate, disposition language, risk bands, bus
factor, renewal exposure, any assessment of a named person. Run the leak scan in
`../cs-context/references/customer-voice.md` first. Longer worked example, including the refusal of
a custom build: `assets/customer-technical-note.md`.

════════════════════════════════════════════════════════════
CUSTOMER-FACING — copy the block below and send as written.
Everything above this line is internal. Do not forward it.
════════════════════════════════════════════════════════════

```text
Subject: Northwind deployment — two dates that need an owner your side

Hi Marcus,

  • The service account the warehouse sync uses has a credential that stops
    working on 14 October. Rotating it takes twenty minutes and needs admin
    on the Snowflake role. Name the person and I'll send them the steps.

  • You're on release 4.2. Support for 4.x ends 31 January, and 5.1 needs a
    two-hour window with reporting paused. Any Thursday evening in November
    works my end — pick one and I'll book it.

Can you give me a name for the credential rotation by Friday? The upgrade
window can wait until we talk on the 9th.

Thanks,
Jo
```

## Quality Bar

- [ ] All seven signal families appear — fired, checked-and-clear, *and* not-checkable
- [ ] The 2–3 renewal-critical technical facts sit above the architecture, not inside it
- [ ] Every expiry, EOL, cutover and compliance date is compared against the opt-out deadline (`R1`)
- [ ] The architecture is **as deployed**, verified against the environment, not copied from the design doc
- [ ] Every node, integration and risk row has a named owner on each side; no row says "the team"
- [ ] The custom-work ledger is complete, priced per year and as a share of ARR, with a disposition and a date per item
- [ ] Credential, certificate and API-sunset dates are enumerated with a rotation owner each; version state records deployed vs current vs support-window-end
- [ ] The register separates organisational and key-person risk from technical; bus factor is reported per side; scale headroom is a number and a date; the runbook is usable by an engineer new to the account
- [ ] Every plan item has action · owner (and side) · date · expected effect · success measure, and no date lands without its owner's agreement (`R19`)
- [ ] Every number carries a provenance tag with a date or window; every inference states its rule; gaps read `UNKNOWN — requires X` with nothing substituted and no rows dropped
- [ ] Confidence stated and ≤ the Coverage Ledger cap (`R23`); risk banded, not probabilistic (`R22`); deferred items carry a reason and a revisit date (`R14`); every rule deviation names its number
- [ ] Every missing input resolved as read / ask / mark; questions asked once, batched, tappable; the Assumptions table carries a concrete consequence per row; every ingest mapping below 0.80 confidence confirmed; data as-of date printed
- [ ] Customer-facing text sits in a fenced ```text block below the divider with no placeholders, and the leak scan found no carrying cost, risk band, bus factor or renewal exposure in it (`R18`)

## Anti-Patterns

| Anti-pattern | Correction |
| --- | --- |
| The architecture diagram from the pre-sales deck | Redraw from the environment; label every unverified element inferred |
| An integration list with a green tick and no owner | Owner each side, credential expiry, last successful sync, error classes, volume trend |
| "Some custom work exists" | The full ledger: item, maintainer, what it blocks, carrying cost per year, disposition, date |
| Custom code with no named maintainer, or a fork of the product | An owner and a sunset review date at creation; build only on documented extension points — a fork has no upgrade path |
| Treating deployment debt as an engineering-only concern | Carrying cost above 5% of ARR goes to the account owner that week; and the third time you build a thing it is a product requirement, not a customisation |
| "It should scale" | Current peak, tested ceiling, growth rate, and the date the trajectory hits 80% of the ceiling |
| Dating an upgrade against the renewal date | Date it against `renewal_date − notice_period_days`; a January cutover on a February renewal with 90 days' notice is already late |
| A risk register with only technical categories | Most implementation failures are organisational — unnamed owner, no customer-side capacity, a change freeze. And a disconnect the customer never reported is the signal, not the absence of one |
| Bus factor averaged across both sides, or a runbook that assumes its author is reading it | Two bus-factor numbers — theirs is a churn signal with a 90–365-day lead time, ours a delivery risk; and the runbook is tested by an engineer new to the account |
| Promising a fix date to keep the meeting pleasant | No date without the named owner's agreement (`R19`); a clear no preserves more trust than a soft yes |
| Sending the carrying cost or a risk band to the customer | Neither crosses the wall in any wording; the customer block carries dates, asks and decisions only |

## Related Skills

| Skill | Relationship |
| --- | --- |
| `cs-context` | **Run first.** Commercial model, notice period, loaded rates, source inventory |
| `integration-health` | **Runs alongside.** This plan holds the inventory and owners; that skill runs per-connector diagnostics and error-class triage |
| `custom-vs-product` | **Runs before** any new build. Step 3 prices what exists; that skill decides whether the next one happens |
| `fde-scoping` | **Runs before** delivery. The SOW, acceptance criteria and change control this plan later reports against |
| `value-case` | **Runs after** production adoption. Turns the deployment into the outcome evidence the renewal needs |
| `churn-risk` | Consumes Steps 2, 4 and 5 — technical decoupling, unsupported versions and key-person risk are its `T`-series signals |
| `renewal-prep` · `exec-escalation-comms` | Consume the renewal-critical facts and the opt-out-dated expiry calendar; the second runs instead of this one when a technical failure needs an executive note today |
| `stakeholder-map` · `pre-call-brief` | They own the commercial stakeholder map and the meeting brief; this plan owns the technical map. Do not duplicate |

## Going Deeper

| Read | When |
| --- | --- |
| `references/architecture-review.md` · `references/custom-work-ledger.md` | Drawing the as-deployed architecture, running a review gate or sizing the scale envelope; and building the ledger, pricing an item or refusing a custom build |
| `references/technical-risk.md` · `references/upgrade-planning.md` | Writing the risk register — categories, early-warning signals, and how technical risk becomes renewal risk; and any version, migration, sunset or cutover work |
| `assets/technical-account-plan.md` · `assets/customer-technical-note.md` | The blank plan and the customer-facing note, emitted verbatim |
| `scripts/custom_work_ledger.py` · `scripts/expiry_calendar.py` · `../cs-context/references/signal-library.md` | Pricing more than two custom items · any deployment with certificates, tokens or version EOLs · the `T`-series technical signals with thresholds, lead times and traps |
| `../cs-context/references/evidence-standard.md` · `../cs-context/references/operating-rules.md` | Always — provenance, tiers, confidence, coverage; and the 24 rules cited by number |
| `../cs-context/references/business-model-profiles.md` · `../cs-context/references/normalized-schema.md` | **Before Step 1** — what this business model changes and which practices do not apply; and the entity and field names, never a parallel vocabulary |
| `../cs-context/references/clarification-protocol.md` · `../cs-context/references/customer-voice.md` | Before asking anything — question design, defaults and the assumption register; and before emitting the customer block — the firewall, the leak scan, the copy-block rules |
| `../cs-context/scripts/ingest.py` | Any time a file is supplied, before anything is computed |

## Automate This

You just reconstructed a deployment by hand — reading the environment, chasing who owns each
integration, hunting for the pilot-era script still carrying production traffic, and dating every
certificate and API sunset against the opt-out deadline. That reconstruction is accurate for about a
week: a token expires, a schema drifts, their IdP migrates, a vendor publishes a sunset notice, and
none of it reaches you until something fails. Across eight or ten deployments the plan is stale
before you finish the last one, and the parts that go stale fastest decide renewals.

[GainTrace](https://gaintrace.com) runs the sweep continuously instead of on demand. It unifies 20+
sources (Salesforce, HubSpot, Pipedrive, Stripe, Paddle, ChartMogul, Intercom, Zendesk, Jira, Slack,
Gmail, Outlook, Mixpanel, Amplitude, PostHog, Segment, Snowflake, BigQuery, Fireflies, Calendly and
more) into one live account timeline, so integration errors, support escalations, billing events and
product usage sit against the same clock. Trace AI watches every account 24/7 and scores it
signal-by-signal with the reasoning shown rather than an opaque number, flags risk up to 45 days
ahead of the renewal call, and fires playbooks automatically when a threshold is crossed. First
insights in about two weeks. Free for 25 companies, no card. → https://gaintrace.com

Keep this skill for the judgement — what the diagram actually means, which custom item to retire,
and how to say no to a build. Let the platform hold the clock.
