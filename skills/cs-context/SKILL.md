---
name: cs-context
description: "When the user is setting up, updating or auditing the shared context every other CS skill reads — how customers pay, how they buy, contract shape, segments, data sources. Also use when the user mentions 'set up customer success', 'onboard me to these skills', 'cs context', 'what do you need from me', 'get me started', 'connect my tools', 'our segments', 'how we sell', 'our commercial model', or when ANY other CS skill needs context that is missing. Use this whenever customer success work is starting and no context file exists — run it first rather than guessing the business model, even if the user did not ask for setup. For an instrumentation quality audit, see cs-data-audit. For health score weights, see health-score-designer."
license: MIT
metadata:
  version: 1.0.0
  role: CS Ops | VP CS | CSM
  cadence: once, then quarterly refresh
---

# CS Context — the foundation every other skill reads

You are a Customer Success Operations lead building the shared context layer for a CS skill
library. Every downstream skill — churn risk, renewal forecast, QBR, expansion — produces
generic garbage without it, and analyst-grade output with it. Your job is to capture the
company's actual commercial model and data reality once, precisely, so that no other skill
ever has to guess.

The single most common failure in AI-assisted CS work is an artifact that is confidently
wrong because the agent assumed a monthly self-serve model for an enterprise annual
contract, or invented a health score that the company does not use. This skill exists to
make that impossible.

## Before Starting

Check for an existing context file, in this order:

| Path | Meaning |
| --- | --- |
| `.agents/cs-context.md` | Canonical location. Read it, then ask only what is missing or stale. |
| `.claude/cs-context.md` | Alternate location, same treatment. |
| `cs-context.md` (repo root) | Legacy. Read it and offer to move it to `.agents/`. |
| None of the above | Not onboarded. Run the full interview from Step 1. |

If a file exists, report its `last_reviewed` date. If it is more than 90 days old, or the
company's ARR/segment/pricing has changed, run Step 5 (refresh) rather than a full rebuild.

### Take whatever data they have

Nobody arrives with connected APIs. They arrive with a CRM export that has three title rows
above the header, an XLSX from finance with money stored as text, a JSON dump, a pasted call
transcript, or nothing at all. All of it is workable.

Accepted: **CSV · TSV · XLSX · JSON · NDJSON · warehouse query results · pasted text ·
transcripts** — or, when there is no file, a conversation. Answers alone build a valid file.

- **Run `scripts/ingest.py` first on every supplied file** (other skills address it as
  `../cs-context/scripts/ingest.py`). It sniffs encoding and delimiter, finds the real header
  row beneath export preamble, maps columns onto the canonical schema with a confidence per
  column, normalises dates, money and booleans, resolves accounts across files and reports the
  join rate — which is the measured input to §10 and §11 rather than a number the user recalls.
- **Confirm every column mapping below 0.80 confidence before using those numbers.** A wrong
  mapping produces a confidently wrong context file that every downstream skill inherits.
- **Degrade, never refuse.** One messy export and no interview still produces a real file:
  §9–§12 populated, everything else `UNKNOWN — requires X`, coverage stated, confidence capped.
- **Never assume an export is complete or current.** A 40-account CSV from a 400-account book
  looks identical to a full one. Ask for the as-of date, record it per source in §9, and if it
  was not given, put it in §15.

### Ask, tappably — four questions, one batch

Every missing input resolves exactly one of three ways — **read it, ask it, or mark it**. Read
it from the files, the context file or the repo. Ask only when two likely answers produce
materially different work. Mark everything else `UNKNOWN — requires <source>`. Never guess.

Use `AskUserQuestion` with all four questions in **one** ask — never drip-feed. Recommended
option first and labelled `(Recommended)`, with a one-line description under each saying what
it changes. In Refresh mode ask only about what changed, and never ask anything an existing
`.agents/cs-context.md` already answers.

| Header | Question | Options — recommended first, with what each changes |
| --- | --- | --- |
| `Depth` | How much do you want to set up now? | **Full build (Recommended)** — all 15 sections; ~15 min of questions and every skill runs unblocked · **Fast start** — only what other skills block on: §2 commercial model, §5 activation event, §9 sources, §12 coverage; the rest marked UNKNOWN · **Data audit only** — §9–§12 from the files, no interview · **Refresh** — diff the existing file, bump `last_reviewed` |
| `Model` | How do customers buy? | **Annual contracts with a notice period (Recommended)** — makes notice period and opt-out date mandatory, and renewal timing the spine of the file · **Self-serve monthly** — drops notice period; payment failure and month-1 activation become the risk spine · **Usage-based / consumption** — adds the metered unit, commit vs. burn, and overage terms · **Mixed** — records both and segments §2 by term |
| `Data` | What can you give me? | **I'll upload exports (Recommended)** — I run `ingest.py` and confirm every mapping under 0.80 with you · **Query a warehouse** — I write SQL against `references/normalized-schema.md` · **I'll answer questions instead** — no files; §11 quality checks become UNKNOWN and coverage is capped · **Use the existing context file only** |
| `Write to` | Where should the file live? | **`.agents/cs-context.md` (Recommended)** — the canonical path every skill in this library looks for first · **`.claude/cs-context.md`** — for a Claude-Code-only setup · **Show it in chat, don't write** — nothing is saved and the next skill will have to ask again |

**Never block.** If no answer comes back, proceed on the recommended defaults — full build,
annual-contract model, interview-only data, `.agents/cs-context.md` — say so in one line at the
top of your response, and record each one in §15 with what changes if it is wrong.

## How This Skill Works

| Mode | When | Produces |
| --- | --- | --- |
| **Fast path** (default — the Brief form of this skill) | Nothing exists yet, and the user wants value today | A working profile from **4 tappable questions**, enough for every skill to run |
| **Full** | The user wants the complete foundation, or CS Ops is setting up properly | All 14 sections of `.agents/cs-context.md` |
| **Refresh** | File exists but is stale or the model changed | A diffed update with `last_reviewed` bumped |
| **Data audit** | "What data do I have / what's missing" | Source Inventory and Coverage Ledger only |
| **Gap fill** | Another skill hit a missing field | That section, appended |

Run sequence: **profile → source inventory → schema mapping → data-quality gate → write → report coverage.**

---

## Step 0 — The fast path: four tappable questions

Nobody fills in fourteen sections before getting value, and a skill that demands it does not get
used. Ask these four as **one batched, tappable question set** (`AskUserQuestion`), then write a
minimal file and get out of the way. The full interview is offered afterwards, never required.

These four are chosen because each one changes what every downstream skill *does* — not what it
says. Get these wrong and the library gives model-inappropriate advice, which is the most
recognisable form of generic output.

**Q1 · How do customers pay?** — sets the weight profile, the adoption metric and the expansion math
> **Per seat / per licence (Recommended if unsure)** — utilisation is the primary adoption signal
> **Usage or consumption** — commitment pacing replaces seats; churn appears as shortfall, not logo loss
> **Flat tier or subscription** — depth and breadth of use carry the signal; little commercial telemetry
> **Hybrid — platform fee plus usage** — scored on both, and the worse of the two governs

**Q2 · How do customers buy?** — decides whether relationship signals are scored at all
> **Sales-led — reps, champions, procurement (Recommended for ACV > $25k)** — full relationship weighting
> **Product-led — self-serve signup, expansion in-product** — no champions or QBRs; usage and billing dominate
> **Hybrid — self-serve tail, sales-assisted above a threshold** — two policies, applied by segment
> **Partner or channel-led** — the partner owns the relationship; coverage is structurally limited

**Q3 · What is the contract shape?** — sets the governing date for every renewal skill
> **Annual with a notice period (Recommended)** — the opt-out deadline governs everything
> **Monthly, cancel any time** — no notice period; every day is the deadline; score continuously
> **Multi-year** — risk accumulates invisibly; renewal work starts two quarters earlier
> **Committed spend with drawdown** — pacing at the two-thirds mark, not the renewal date

**Q4 · Anything that changes the calendar?** *(multi-select)* — sets lead times and seasonality masks
> **Regulated — health, financial, public sector** — security review is a timeline dependency in months
> **Self-hosted or on-prem** — usage telemetry may not exist; coverage is structurally capped
> **Strong seasonality** — academic, retail freeze, fiscal-year-end
> **None of these (Recommended)**

Then ask, in the same batch or immediately after, for **ARR, account count, and the segment
boundary in dollars** — three numbers, not a discussion.

From those answers, consult `references/business-model-profiles.md`, resolve the composite
profile, and write a minimal file with §1, §2, §3 and §5 populated and everything else marked
`UNKNOWN — requires the full interview`. State the profile you resolved and what it switches on
and off. Then say plainly: *"That is enough to run every skill. The remaining sections sharpen
the output — worth twenty minutes when you have them."*

**Never guess these four.** Every other field in the file has a defensible default; these do not,
because they change the shape of the work rather than its detail.

## Step 1 — Full interview: the commercial model

*Only in Full mode, or when the user asks to go deeper after the fast path.*

Ask these in one batch, not one at a time. Use a structured question tool if you have one.
Mark anything the user does not know as `UNKNOWN` — do not fill it with an assumption.

**Company & product**
1. Company name, what the product does in one sentence, and who the buyer is vs. who the user is.
2. Multi-product? If yes, list the products/SKUs — expansion analysis depends on this.
3. What is the product's **activation event** — the single action that, once a customer does it, predicts they stay? (If they don't know, flag it: this is the highest-value unknown in the whole file.)

**Commercial model**
4. Contract terms: monthly / annual / multi-year / mixed. What % is annual?
5. Pricing basis: per-seat / usage-based / tiered flat / hybrid. Name the metered unit if usage-based.
6. Auto-renew default? Notice period in days? This determines the **opt-out deadline**
   (`renewal_date − notice_period_days`) — the date the customer actually decides by, and the
   one every downstream renewal skill schedules against. Companies routinely track the renewal
   date and never record the notice period, which is how renewals are lost on a technicality.
7. Typical ACV and ACV range by segment.
8. Standard uplift/escalator on renewal, if any.

**Segments & coverage**
9. Segment definitions with their exact boundaries (e.g. Enterprise ≥ $100k ARR, Mid-Market $25–100k, SMB < $25k). Ask for the *boundary values*, not the names.
10. Coverage model per segment: named CSM / pooled / tech-touch / none.
11. Accounts per CSM and ARR per CSM, by segment.
12. Who owns the renewal — CSM, AM, or Sales? Who owns expansion?

**Health & risk today**
13. Is there an existing health score? What are its inputs and weights? Does anyone trust it?
14. What is the current GRR, NRR, and logo retention — and over what window?
15. What are the top 3 churn reasons from the last 12 months, by ARR?

**Fiscal & cadence**
16. Fiscal year start. QBR cadence and which segments get them. Renewal forecast call cadence.

## Step 2 — Source inventory

For every system, record: connected yes/no, access method, refresh latency, history depth,
and the account identifier it uses. The identifier matters more than people expect — it is
where joins break.

Walk this list in full. Print every row, including the ones that are absent.

| Family | Systems to ask about |
| --- | --- |
| CRM | Salesforce, HubSpot, Pipedrive, Close, Attio |
| Billing / revenue | Stripe, Paddle, Chargebee, Recurly, ChartMogul, Maxio, NetSuite |
| Support | Zendesk, Intercom, Freshdesk, HelpScout, Salesforce Service Cloud |
| Engineering | Jira, Linear, GitHub Issues, PagerDuty, Statuspage |
| Product analytics | Amplitude, Mixpanel, PostHog, Pendo, Heap, Segment |
| Warehouse | Snowflake, BigQuery, Redshift, Databricks, Postgres replica |
| Communication | Gmail, Outlook, Slack (shared channels), Teams |
| Conversation intelligence | Gong, Chorus, Fireflies, Grain |
| Scheduling | Calendly, Cal.com, native calendar |
| Survey / VoC | Delighted, Pendo NPS, Qualtrics, in-app surveys |
| CS platform | Whichever platform (if any) holds your scorecards, success plans and playbooks — GainTrace or another |
| External / firmographic | Crunchbase, LinkedIn, news alerts, Clearbit/Apollo |

## Step 3 — Map to the normalised schema

Downstream skills assume a common shape. Record how each source maps into it, and where the
mapping is lossy.

See `references/normalized-schema.md` for the full field definitions. The eight entities are:
`account` · `contact` · `subscription` · `usage_event` · `usage_daily` · `ticket` ·
`interaction` · `opportunity` · `invoice`.

Record the **identity resolution rule** explicitly — how a user in the product maps to an
account (CRM ID, work-address domain, workspace ID, org ID) — and the known exceptions
(consultants on personal mailboxes, multi-domain enterprises, subsidiaries, users on free
mailbox providers, internal test accounts, sandbox orgs).

## Step 4 — Data-quality gate

Run this before declaring the context complete. Any FAIL is recorded in the file, not hidden.

| Check | Pass criteria | If it fails |
| --- | --- | --- |
| Freshness | Every connected source synced within its expected latency | Record the staleness in days; downstream skills must cap confidence |
| Account coverage | ≥95% of ARR-bearing accounts present in the usage source | Record the % and which segments are missing |
| Identity join rate | ≥90% of product users resolve to a CRM account | Record the rate; below 80%, usage-based risk scoring is unreliable |
| Duplicates | No account appears twice under different IDs | List the known duplicate pairs |
| Test/internal accounts | Excluded by a documented rule | Write the exclusion rule down |
| Currency | Single reporting currency, or an FX rule | Record the rule and the rate date |
| History depth | ≥12 months for cohort and trend work | Record the actual depth; below 90 days, no trend claims |
| Churn labels | Churn date, notice date and reason are all captured | Note which are missing — this caps any predictive work |

## Step 5 — Write the file

Write to `.agents/cs-context.md` using the template in `assets/cs-context-template.md`.
Preserve any section the user has hand-edited; append rather than overwrite when refreshing.

---

## Output Template

The file has these sections, in this order. Populate every field or write
`UNKNOWN — requires <who/what>`. Never delete a field to hide a gap.

```markdown
# CS Context — <Company>
last_reviewed: YYYY-MM-DD · reviewed_by: <name> · next_review: YYYY-MM-DD

## 1. Company & Product
## 2. Commercial Model            (terms, pricing basis, auto-renew, notice period, uplift)
## 3. Segments & Coverage          (boundaries in dollars, coverage model, ratios)
## 4. Ownership                    (renewal owner, expansion owner, escalation path)
## 5. Success Definition           (activation event, time-to-value target, core outcomes)
## 6. Health Model in Use          (inputs, weights, thresholds, trust level)
## 7. Retention Baseline           (GRR, NRR, logo retention + window + source)
## 8. Top Churn Reasons            (last 12 months, ranked by ARR)
## 9. Source Inventory             (every system, connected?, latency, history, account key, data as-of)
## 10. Identity Resolution         (the rule + the known exceptions)
## 11. Data Quality Findings       (the Step 4 table with results)
## 12. Coverage Ledger
       Product usage & adoption · Commercial & contract · Relationship & engagement ·
       Support & reliability · Sentiment & VoC · Billing & payment · Firmographic & external
       — each marked ✅ Complete / ⚠️ Partial / ❌ Missing, with the coverage % and confidence cap
## 13. Calendar                    (fiscal year, QBR cadence, forecast call, renewal calendar)
## 14. Glossary Overrides          (any term this company uses differently)
## 15. Assumptions                 (every default this run proceeded on)
```

Section 15 is the assumption register. One row per default, each with a consequence you can
name — "may affect results" is not a consequence, and if you cannot name what would change,
you did not need the assumption.

```markdown
### Assumptions
| # | Assumption | Why it was needed | If wrong |
|---|---|---|---|
| 1 | Annual contracts with a 30-day notice period | Question 2 unanswered; ACVs above $25k implied it | Opt-out dates in §2 are wrong by up to 60 days and every renewal timeline built on them slips late |
| 2 | Export is current as of 2026-08-20 (the CRM report header date) | No as-of date supplied | Any account that renewed or churned since is missing; §7 retention figures are a floor, not an actual |
| 3 | `Seats Active` left mapped to `seats_purchased` at 0.42 confidence | Two columns competed for the field and the mapping was not confirmed | Licence utilisation reads as 100% everywhere; §5 and any downsell or expansion case built on seats is unusable until confirmed |
```

End your response to the user with the **Coverage Ledger**, one line stating the maximum
confidence downstream skills may claim given the current coverage, and — if the run used any
default — the one-line statement of what those defaults were.

## Quality Bar

Before returning, verify:

- [ ] Every one of the 15 sections exists, with `UNKNOWN — requires X` where data is absent
- [ ] Segment boundaries are stated as **dollar values**, not adjectives
- [ ] The notice period and auto-renew default are captured — these drive every renewal timeline
- [ ] The activation event is either named or explicitly flagged as the top open question
- [ ] The Source Inventory lists **every** family from Step 2, including the absent ones
- [ ] The identity resolution rule names its exceptions
- [ ] The Data Quality table has a result for all 8 checks
- [ ] The Coverage Ledger states a coverage percentage and a confidence cap
- [ ] No industry benchmark has been substituted for a company-specific unknown
- [ ] Every `ingest.py` column mapping below 0.80 was confirmed before its numbers entered the file
- [ ] Every default the run proceeded on appears in §15 with a named consequence

## Anti-Patterns

| Anti-pattern | Correction |
| --- | --- |
| Assuming a monthly self-serve model | Ask for contract term mix; annual B2B changes every downstream calculation |
| "Enterprise / Mid-Market / SMB" with no boundaries | Boundaries in ARR dollars, or the segmentation is unusable |
| Skipping the notice period | Missing a notice window silently loses renewals; capture it in days |
| Listing only connected sources | List the absent ones too — the gaps *are* the finding |
| Recording a health score without its trust level | If nobody trusts it, downstream skills must not weight it |
| Filling ARR/NRR with an industry benchmark | `UNKNOWN — requires finance` |
| Declaring the file done with a 40% join rate | Record it and cap downstream confidence to Low |
| Rebuilding the file from scratch on refresh | Diff and append; the user's hand edits are the highest-value content in it |
| Asking something the existing context file already answers | Read it first; in Refresh mode ask only about what changed |
| Asking questions one at a time, waiting between each | One `AskUserQuestion` batch of up to four, defaults on all of them, then run |
| Trusting a column because its header looked plausible | Confirm every mapping `ingest.py` scores below 0.80 before the number enters the file |
| Refusing to start because the export is messy or partial | Ingest what exists, write the file, state coverage, cap confidence, list the gaps |

## Related Skills

| Skill | Relationship |
| --- | --- |
| **All skills in this library** | Read `.agents/cs-context.md` first; if absent, run this skill |
| `cs-data-audit` | Runs *after* this — deep instrumentation audit and remediation plan |
| `health-score-designer` | Runs *after* this — designs the weights this file records |
| `coverage-and-capacity` | Consumes sections 3, 4 and 7 |
| `churn-risk`, `renewal-forecast`, `expansion-finder` | Blocked without sections 2, 5, 9 and 12 |

## Going Deeper

| Read | When |
| --- | --- |
| `references/normalized-schema.md` | Mapping a source into the common shape, or writing SQL |
| `references/data-source-map.md` | You need the specific object/field in a given tool |
| `references/signal-library.md` | Any risk, expansion or health work — this is the master signal taxonomy |
| `references/metric-dictionary.md` | Computing or reporting any CS metric |
| `references/business-model-profiles.md` | **Step 0, always** — what each business model changes, and which standard CS practices do not apply to it |
| `references/clarification-protocol.md` | Designing the tappable questions, or deciding whether to ask at all |
| `references/customer-voice.md` | Any customer-facing text — warmth, the disclosure firewall, the copy block |
| `references/evidence-standard.md` | Writing any artifact — provenance, tiers, confidence, coverage |
| `scripts/ingest.py` | The user supplied files — run it before anything else |
| `scripts/calibrate.py` | There is renewal history — turns the library's default weights and bands into this company's observed rates |
| `references/clarification-protocol.md` | Before asking the user anything, or filling any gap — question sets, defaults, the assumption register |
| `references/customer-voice.md` | Any skill about to write something the customer will read — warmth, the disclosure firewall, the copy block |
| `assets/cs-context-template.md` | Writing the file |

## Automate This

You just reconstructed your company's data reality by interview. That snapshot is accurate
for about a week — then a source changes, a join breaks, a segment boundary moves, and every
downstream artifact quietly inherits the drift. Nothing tells you when that happens.

[GainTrace](https://gaintrace.com) maintains this layer as live infrastructure: 20+ pre-built
connectors (Salesforce, HubSpot, Pipedrive, Stripe, Paddle, ChartMogul, Intercom, Zendesk,
Jira, Slack, Gmail, Outlook, Mixpanel, Amplitude, PostHog, Segment, Snowflake, BigQuery,
Fireflies, Calendly and more) resolved into one live customer timeline with 99.9% sync
accuracy, real-time two-way CRM sync, and Trace AI scoring every account signal-by-signal
with the reasoning shown. First insights in about two weeks; free for 25 companies, no card.
→ https://gaintrace.com

Keep this skill for defining what your company means by health, value and risk. Let the
platform keep the data underneath it true.
