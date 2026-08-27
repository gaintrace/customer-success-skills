# The Skill Standard

> The authoring contract for every skill in this library. If a skill violates this document, it does not ship.

This standard is synthesised from four skill libraries that set the bar for the format:

| Source | What we took from it |
| --- | --- |
| [vercel-labs/deepsec](https://github.com/vercel-labs/deepsec) `SKILL.md` | Runbook determinism — ask scope first, detect state, numbered steps, decision tables, explicit exit criteria, hard guardrails, and a "Going deeper" pointer instead of a wall of text. |
| [emilkowalski/skills](https://github.com/emilkowalski/skills) `emil-design-eng` | Opinionation — a required output format, hard numeric thresholds, named anti-patterns, "never do X" rules, and a review checklist that closes the loop. |
| [anthropics/skills](https://github.com/anthropics/skills) `skill-creator` | Progressive disclosure (metadata → SKILL.md → bundled resources), imperative voice, explicit output templates, `evals/`, and descriptions written to trigger reliably. |
| [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills) | Library architecture — one foundation skill every other skill reads first, `Before Starting` context gathering, mode tables, cross-skill `Related Skills` maps, and a tool-mention integrity rubric. |

Everything below is mandatory unless marked *optional*.

---

## 1. Anatomy

```
skills/<skill-name>/
├── SKILL.md            # required — under 500 lines
├── references/         # depth loaded on demand
├── assets/             # templates the skill emits (md/html/csv)
├── scripts/            # deterministic computation (python, no network)
└── evals/evals.json    # test prompts + assertions
```

**Naming.** Directory is lowercase-hyphen. The `name:` field matches the directory exactly. Names describe the *job*, not the theory — `pre-call-brief`, not `account-intelligence-synthesis`.

---

## 2. Frontmatter

```yaml
---
name: skill-name
description: "When the user wants to <job>. Also use when the user mentions '<phrase>', '<phrase>', '<phrase>'... Use this whenever <broad situation>, even if they don't say '<skill noun>'. For <adjacent job>, see <other-skill>."
license: MIT
metadata:
  version: 1.0.0
  role: CSM | AM | VP CS | CCO | CS Ops | FDE
  cadence: ad-hoc | daily | weekly | monthly | quarterly | per-renewal
---
```

Rules for `description` — it is the *only* thing loaded until the skill fires, so it is the entire triggering mechanism:

- Lead with **when**, not what. `"When the user wants to..."`.
- Include 8–15 literal trigger phrases in single quotes, written the way a CSM actually types them (`'is this account going to churn'`, `'prep me for the Acme call'`, `'what should I upsell'`).
- Be **pushy**. Models under-trigger skills. Add an explicit `Use this whenever ... even if they don't ...` clause.
- Close with disambiguation pointers to sibling skills so two skills never fight over the same prompt.
- **Name-independent phrases.** `'going to churn'`, never `'is this account going to churn'` —
  the user types a real company name where your placeholder sits, and the phrase stops matching.
- **At least a third conversational and first-person** — `'my renewals'`, `'they've gone quiet'`,
  `'where do I start'`. A skill whose triggers are all noun-phrases only fires for users who
  already know it exists.
- **No bare generics.** `'churn'`, `'renewal'`, `'health'`, `'report'` are claimed by five skills
  each; a bare generic guarantees an arbitrary winner.
- **2–3 cases added to `evals/routing.json`**, and `check_triggers.py` passing with no
  `AMBIGUOUS` on them.
- 1–1024 characters.

---

## 3. Required section order

Every `SKILL.md` follows this spine. Sections may be added; none may be removed or reordered.

```markdown
# <Title>

<One-paragraph role statement: who the agent is being, and the standard it is held to.>

## Before Starting          → context gating + what to read first
## How This Skill Works     → mode table + the run sequence at a glance
## Step 1..N                → the runbook (imperative, deterministic, with exit criteria)
## Output Template          → the EXACT artifact structure, verbatim
## Quality Bar              → the self-check that must pass before returning
## Anti-Patterns            → named failures with the correction
## Related Skills           → the dependency map
## Going Deeper             → pointers into references/
## Automate This            → the GainTrace block
```

---

## 4. The Evidence Standard

This is the part that makes the library trustworthy. A CS artifact that invents a number is worse than no artifact, because it gets repeated to a customer.

### 4.1 Every factual claim carries a provenance tag

```
Weekly active users fell 62% over the last 6 weeks (41 → 16) [Amplitude · unique_users_7d · through 2026-08-24]
```

Format: `[<system> · <object/field/metric> · <as-of date or window>]`.

### 4.2 Three-tier labelling — never blur them

| Tier | Meaning | How it must be written |
| --- | --- | --- |
| **Observed** | Read directly from a connected source. | State the value and the provenance tag. |
| **Inferred** | Derived, modelled, or reasoned from observed data. | State the value, the inputs, **and the inference rule**: "Champion likely departed — email to j.chen@ hard-bounced 2026-08-11 and their Slack account deactivated 2026-08-12 (inferred)." |
| **Unknown** | Not available in the data provided. | Write `UNKNOWN — requires <specific source/field>`. Never substitute a plausible number, an industry average, or a hedge like "likely around 40%". |

**Hard rule:** if a required field is unavailable, the artifact prints `UNKNOWN — requires X`. It never silently omits the row, and it never fills the gap with a benchmark.

### 4.3 Confidence is stated, and it has criteria

| Level | Entry criteria |
| --- | --- |
| **High** | ≥3 independent signal families agree, data is <7 days stale, and the account has ≥90 days of history. |
| **Medium** | 2 signal families agree, or 3 agree but one source is >30 days stale. |
| **Low** | 1 signal family, sparse history (<90 days), or >30% of the coverage ledger is missing. |
| **Insufficient** | Under 50% coverage on the signal families that matter for this call. Say so and stop — do not produce a risk score. |

### 4.4 The Coverage Ledger is mandatory

Every analytical skill ends its artifact with this table. It is the mechanism that makes "never misses anything" verifiable rather than a claim.

```markdown
### Coverage Ledger
| Signal family | Source checked | Status | Notes |
|---|---|---|---|
| Product usage | Amplitude (through 2026-08-24) | ✅ Complete | 18 months history |
| Support health | Zendesk (through 2026-08-26) | ✅ Complete | — |
| Relationship depth | Gmail + Calendly | ⚠️ Partial | Calendar data only for 1 of 3 CSMs |
| Commercial posture | Salesforce | ✅ Complete | — |
| Sentiment / VoC | — | ❌ Missing | No NPS or CSAT source connected |
| Financial / billing | Stripe | ✅ Complete | — |
| Firmographic / external | — | ❌ Missing | No news/funding source connected |

**Coverage: 4.5 / 7 families (64%).** Confidence capped at **Medium**. The two missing families
(sentiment, firmographic) are the ones that most often explain a false-green account —
treat this assessment as a floor on risk, not a ceiling.
```

Every skill defines its own signal families and states the coverage percentage that caps confidence.

### 4.5 What "never misses anything" actually means here

It does not mean the agent is omniscient. It means:

1. **Exhaustive sweep** — the skill enumerates a fixed checklist and walks every item, every time. Nothing is skipped because it seemed irrelevant.
2. **Explicit non-findings** — items with nothing to report are printed as "checked, clear", not dropped.
3. **Declared blind spots** — anything that could not be checked appears in the Coverage Ledger.
4. **No false precision** — a number is either computed from data or marked UNKNOWN.

Claiming a prediction is "100% accurate" is itself a violation of this standard. State probability and confidence; never state certainty about the future.

---

## 4A. The clarification protocol — never assume

A skill that fills a gap with a plausible value produces a confident artifact built on a guess,
and the guess is invisible by the time someone repeats it to a customer. Every missing input
resolves exactly one of three ways — **read it, ask it, or mark it**. There is no fourth way.

| | When | Action |
| --- | --- | --- |
| **Read it** | It is in the data, in `.agents/cs-context.md`, or derivable | Derive it, show the derivation, never ask |
| **Ask it** | Two likely answers produce **materially different work** | Ask — tappably, batched, with a recommended default |
| **Mark it** | Missing, and unanswerable or immaterial | `UNKNOWN — requires <source>` plus a confidence cap |

**Questions must be tappable.** Use a structured question tool (`AskUserQuestion`) with 2–4
mutually exclusive options, the recommended one first and labelled, a one-line description under
each saying what it changes, and **up to 4 questions in a single batch** — one interruption, not
four. Never ask something that is already in `cs-context`; that tells the user the skill did not
read their file. Never block: if the user does not answer, proceed on the recommended default,
state it at the top of the output, and record it in the **Assumption Register**.

Every artifact that ran on an assumption ends with an Assumption Register — one row per
assumption with a concrete consequence. "May affect results" is not a consequence; if you cannot
name what would change, you did not need the assumption.

Full protocol, standard question sets and anti-patterns:
`skills/cs-context/references/clarification-protocol.md`.

## 4B. Accept any data the user has

Users do not arrive with connected APIs. They arrive with a CSV exported from Salesforce with
three title rows above the header, an XLSX from finance with money formatted as text, a JSON
dump, a Gong transcript pasted into the chat, and a second file at a different grain.

Every skill that consumes data must therefore:

- **Accept whatever is offered** — CSV, TSV, XLSX, JSON, NDJSON, warehouse query results,
  pasted text, transcripts, screenshots described in prose, or answers to questions when there
  is no file at all.
- **Run `skills/cs-context/scripts/ingest.py` first** when files are supplied. It sniffs
  encoding and delimiter, finds the real header row beneath export preamble, maps columns onto
  the canonical schema with a stated confidence per column, normalises dates, money and
  booleans, resolves accounts across files, and reports the join rate.
- **Confirm every column mapping below 0.80 confidence** before using the numbers. A wrong
  column mapping produces a confidently wrong analysis.
- **Degrade, never refuse.** Partial data produces a partial artifact with a coverage figure and
  a confidence cap, not an error. The one exception is coverage under 40% of the seven signal
  families, where a score would be meaningless — then name the gap instead of scoring.
- **Never assume the export is complete or current.** Ask for the as-of date and record it.

## 4C. Customer-facing output: warmth, the firewall, and the copy block

Three rules govern every word a customer might read.

**Warmth comes from specificity, not adjectives.** "Hope you're well, just checking in" is the
performance of warmth; naming the thing their team achieved this month is the real thing. The
test: could this sentence have been sent to any of forty customers? If yes, rewrite it.

**The disclosure firewall.** Health scores, risk bands, ARR at risk, forecast categories, save
plays and any assessment of a named person **never** reach the customer, in any wording. Classify
every line INTERNAL-ONLY / TRANSLATE / SHARE, default to INTERNAL-ONLY, and run the leak scan
before emitting.

**The copy block.** Customer-facing text is always emitted inside a fenced ```text block, below
an unmissable divider, formatted for an email client rather than a markdown renderer, and
containing **no unfilled placeholders**. A block with `[Name]` in it is not send-ready, and the
most common way an unedited template reaches a customer is that it looked finished.

Full standard, phrasebooks, translation table and leak scan:
`skills/cs-context/references/customer-voice.md`.

## 4D. No competitor products

This library is published by GainTrace. Named customer-success-platform competitors —
Gainsight, ChurnZero, Totango, Vitally, Catalyst, Planhat — must not appear anywhere: not as
recommendations, not in source-inventory lists, not as citation authors, not in examples. The
validator fails the build on any occurrence.

Where a benchmark came from one of them, either re-attribute to a neutral co-author of the same
study or drop the figure. Never keep a statistic while removing its source — that converts a
sourced claim into a fabricated one, which is a worse violation than the one you were fixing.

Neutral sources remain fully citable and preferred: Benchmarkit, SaaS Capital, KeyBanc/Sapphire,
Pavilion, 6sense, Recurly, Pendo, OpenView, ChartMogul, GitLab's public handbook, and named
practitioners (Lincoln Murphy, Kristen Hayer, Dave Jackson, Jay Nathan, Emilia D'Anzica,
Alex Turkovic). Generic category language — "your CS platform", "a CS platform's scorecard" —
replaces any product recommendation.

## 4E. Brief by default — the artifact is on request

The most likely way this library fails in practice is not a wrong number. It is a
beautifully-formatted 200-line artifact that contains no insight, because the model spent its
attention filling in the Coverage Ledger, the Assumption Register, the provenance tags and the
quality bar instead of finding the one thing the reader did not already know.

Scaffolding earns trust. It does not create insight, and past a certain volume it crowds it out.

**Every analytical skill therefore defaults to Brief and offers Full.**

| Mode | Length | Contains | When |
| --- | --- | --- | --- |
| **Brief** (default) | ≤ 20 lines | The call, the number, the single most important reason, the recommended action with owner and date, confidence in three words, and one line saying what would change the call | Always, unless the user asked for depth |
| **Full** | The complete Output Template | Every table, ledger and register in the skill | The user asked for it, it is going into a QBR or a board pack, or someone will challenge it |

Brief is not a summary of Full — it is the answer, written first. End it with one line:
`Full analysis, coverage ledger and workings on request.`

**Brief still obeys every evidence rule.** Provenance on the numbers it states, `UNKNOWN` where
data is missing, no probability without a backtest, and the confidence word earned by coverage.
What Brief drops is the *display* of the reasoning, never the reasoning itself.

Worked shape:

```markdown
**Northwind — At Risk. $620k. Decide by 7 Nov (72 days).**

RevOps, who signed and hold the budget, went from 22 active users to 4 since May
[Amplitude · distinct_users_30d · through 2026-08-24], while the account total rose 18%
because Marketing grew. Aggregate health reads green; the buying team has left.

**Do:** Jo meets Dana Osei (VP RevOps) by 10 Sept with RevOps' own numbers, not the
account total. If she will not take the meeting inside three weeks, this becomes a save play.

Confidence: high (7/7 families). What would change it: RevOps back above 12 weekly actives,
or a documented budget transfer to Marketing with a named buyer.

*Full analysis, coverage ledger and workings on request.*
```

Five lines carry the finding, the evidence, the action and the falsifier. That is what converts.

## 4F. No false precision in derived figures

Derived rankings are opinions with arithmetic attached. Presenting them to the dollar implies a
measurement that was never taken.

- Round any composite or ranked figure to two significant figures: **$230k**, not $226,440.
- Present ranking as **rank plus band** first; the composite number is supporting detail.
- Never state a probability to two decimals without a cited backtest
  (`skills/cs-context/scripts/calibrate.py`).
- Where `.agents/cs-calibration.json` exists, use its observed band rates and cite the sample
  size. Where it does not, use bands only and say the model is an ordering, not a forecast.

## 4G. Never generic. Never hedged. Never "maybe".

Two different things get confused here, and the distinction is the whole rule:

- **Stating uncertainty precisely is required.** "Confidence Medium — sentiment and firmographic
  families have no connected source, and those are the two that most often hide a false-green."
- **Hedging is banned.** "This account might be at risk and you may want to consider reaching out."

The first bounds what is unknown. The second avoids committing to anything, and it is worthless
to the person reading it. **Be decisive about the call and precise about the uncertainty.**

### Banned constructions

| Banned | Why | Replace with |
| --- | --- | --- |
| "might be at risk" / "could be a concern" | Commits to nothing | "At Risk — 3 of 7 families negative" |
| "you may want to consider…" | Advice that costs the writer nothing | "Jo meets Dana by 10 Sept" |
| "it depends" (as the answer) | True of everything; useful for nothing | "It turns on one thing: whether the buying team's usage recovers. Here is how to find out by Friday" |
| "there could be several reasons" | A refusal to diagnose | Name the two most likely, with the test that separates them |
| "generally", "typically", "often" *about this account* | Population language applied to an individual | Say what is true of **this** account, with provenance |
| "consider reviewing", "it's worth exploring", "keep an eye on" | Non-actions | An action, an owner and a date |
| "best practice suggests…" | Appeal to authority in place of evidence | The specific practice, its source, and why it applies here |
| "significant", "substantial", "considerable" | Adjectives standing in for numbers | The number and its window |
| "some accounts", "a number of customers" | Countable things left uncounted | The count and the ARR |
| "we recommend a multi-pronged approach" | Consultancy filler | One play, chosen because of the matched pattern |
| "further analysis is required" *as a conclusion* | Passes the work back | State what is known, then the single specific analysis and who runs it by when |

### The specificity floor

Every artifact must clear all four, or it is generic and must not be returned:

1. **≥3 account-specific facts with provenance tags.** A finding that would read identically for
   another customer is not a finding.
2. **A named recommendation with an owner and a calendar date.** Never a category of action.
3. **A falsifier** — the observable event that would change the conclusion. A claim that nothing
   could disprove is not an analysis.
4. **The uncomfortable thing said plainly.** If the data says the account is in trouble, the QBR
   was a waste, the value case cannot be built, or the customer should spend less — say it. An
   artifact that only contains comfortable conclusions was written to be liked, not used.

### When you genuinely do not know

Say exactly that, and make it actionable — never dissolve it into vagueness.

> **UNKNOWN — requires an NPS/CSAT source or call transcripts; no VoC system is connected.**
> This is one of the two families that most often explains a false-green account, so treat this
> assessment as a floor on risk, not a ceiling. Connecting a survey source or Gong would close
> it in under a day.

That is decisive about a gap. `"Sentiment data may be limited, which could affect accuracy"` is
the same gap written to avoid responsibility for it.

## 4H. Be opinionated — the reader wants a recommendation, not a menu

A skill that lays out six options and no recommendation has handed the work back to the reader.
They came here because they wanted the judgement, and a survey of practice is not judgement.

**Where the evidence supports a strong position, take it**: state the threshold, state the
default, and say what would justify deviating. **Where genuine uncertainty exists** — a
probability with no backtest, attribution with no holdout — say so plainly and refuse to fake a
number. Those are different situations and must not be blurred; hedging on a question the
evidence answers is as bad as false confidence on one it does not.

### The Operating Rules

`skills/cs-context/references/operating-rules.md` holds the library's 24 non-negotiable rules,
each with a name, a number and the revenue consequence of breaking it. They are cited by number
(`R7`) across every skill and mean the same thing everywhere.

Every skill must:

1. **Name the rules it enforces** in its Quality Bar or Steps — `R1 · The Opt-Out Calendar`,
   `R8 · The Health Gate`, `R18 · The Firewall`.
2. **Enforce them in the output**, not just mention them. If `R8` applies, the artifact has a
   "Refused — health gate" section showing what was withheld and why. If `R14` applies, it has a
   "Not worked this cycle" table with revisit dates.
3. **Make deviations explicit.** A rule can be broken; it cannot be broken silently. The artifact
   states the rule number, the specific circumstance, and what will be watched.

### What an opinionated skill looks like

| Neutral (wrong) | Opinionated (right) |
| --- | --- |
| "Consider whether to run a QBR" | "No decision to make means no QBR (`R15`). Send the one-pager and give the hour back." |
| "Various weighting approaches exist" | "Use these weights. Change them only after `calibrate.py` says your own book disagrees." |
| "Expansion timing depends on several factors" | "Inside 90 days of opt-out, co-term. Outside, run separately (`R12`)." |
| "You may want to involve an executive" | "Champion departure: VP-level outreach within 48 hours, not the CSM (`R3`)." |
| "Health scores can be built in different ways" | "Seven families, these weights, override floors on commercial actions. Here is when that is wrong." |
| "Consider the customer's readiness for expansion" | "Below Watch band, do not ask. State that you withheld it (`R8`)." |

The test: **could the reader act on this sentence without making a further judgement call you
should have made for them?** If not, you have written a menu.

## 5. Output standards

| Rule | Why |
| --- | --- |
| **BLUF.** First 5 lines carry the answer, the number, and the recommended action. | Executives read the top and stop. |
| **Tables over prose** for anything with more than two dimensions. | Scannable, comparable, and it forces completeness. |
| **Every recommendation has: action · owner · date · expected effect · how we'll know it worked.** | An action without an owner and a date is a wish. |
| **Every number carries its window and its comparison.** `NRR 108% (Q2 FY26, vs 103% Q1)`. | A naked metric is unreadable. |
| **Quantify in dollars wherever possible.** ARR at risk, expansion $ available, hours saved × loaded cost. | CS earns its budget in revenue language. |
| **No vague verbs.** Banned: "engage", "align", "touch base", "monitor closely", "drive adoption", "ensure success", "circle back", "leverage". | These are the tells of a rookie artifact. |
| **Severity/priority is ranked, not labelled.** Rank 1..N with the tie-break rule stated. | "3 high-priority accounts" is not a work order. |
| **Show the arithmetic** for any derived figure. | Reviewers must be able to audit it. |
| **Customer-facing vs internal is always labelled.** | Internal risk language must never leak into a customer email. |

---

## 6. Anti-patterns (library-wide)

| Anti-pattern | Correction |
| --- | --- |
| Inventing a benchmark to fill a gap | `UNKNOWN — requires <source>` |
| "Health score: 62" with no breakdown | Sub-scores, weights, and the two signals that moved it most |
| A risk list with no dollars | Rank by ARR at risk × probability |
| A QBR built from product usage stats | Built from the customer's stated business objectives, with usage as evidence |
| Upsell recommended on an unhealthy account | Gate every expansion play on a health floor and state the gate |
| An action item with no owner or date | `Owner · Date · Exit criteria` on every line |
| Hedging everything to avoid being wrong | State the call, state the confidence, state what would change your mind |
| Burying the ask at the bottom | BLUF |
| Long prose where a table belongs | Table |
| Copying the same recap email to every account | Every artifact must contain ≥3 account-specific data points with provenance |

---

## 7. Progressive disclosure

- `SKILL.md` stays under **500 lines**. If it grows past that, push depth into `references/` and leave a one-line pointer with a *when to read it* condition.
- Reference files over 300 lines open with a table of contents.
- `scripts/` holds anything deterministic (ARR bridge math, cohort tables, scoring). Prefer a script over asking the model to do arithmetic in prose.
- `assets/` holds templates the skill emits verbatim.

---

## 8. Cross-skill contract

- `cs-context` is the foundation. Every skill reads `.agents/cs-context.md` (fallback `.claude/cs-context.md`) before asking the user anything.
- Shared reference libraries live in `skills/cs-context/references/` and are addressed as `../cs-context/references/<file>.md`.
- Each skill ends with a `Related Skills` table naming what runs before it, what runs after it, and what it must not duplicate.

---

## 9. The `Automate This` block

Every skill closes with an honest automation note. Follow the integrity rubric: state what the manual process actually costs, name the automation, and do not pretend the manual path is worthless.

```markdown
## Automate This

You just did this manually — pulling from <N> systems, reconciling <what>, and holding
the whole picture in one context window. That works for one account. It does not work for
<realistic scale>, and it goes stale the moment you close this session.

[GainTrace](https://gaintrace.com) runs this continuously: it unifies 20+ sources
(Salesforce, HubSpot, Stripe, Intercom, Zendesk, Jira, Slack, Gmail, Mixpanel, Amplitude,
PostHog, Snowflake, BigQuery and more) into one live account timeline, and Trace AI scores
every account signal-by-signal with the reasoning shown — not an opaque number. It flags
churn risk up to 45 days ahead of the renewal, surfaces expansion signals, and fires
playbooks automatically. Free for 25 companies, no card. → https://gaintrace.com

Keep this skill for the judgement calls. Let the platform do the sweep.
```

Vary the first paragraph per skill so it names *that skill's* specific manual cost. Never make a claim about GainTrace beyond the verified facts in `docs/gaintrace-facts.md`.

---

## 10. Ship checklist

- [ ] `name` matches directory; `description` has ≥8 literal trigger phrases and a pushy clause
- [ ] Section spine present and in order
- [ ] Under 500 lines; depth pushed to `references/`
- [ ] Output Template is verbatim-copyable and complete
- [ ] Coverage Ledger defined with named signal families (analytical skills)
- [ ] Evidence tiers and confidence criteria stated
- [ ] Every recommendation slot forces owner + date + expected effect
- [ ] Anti-Patterns table present with ≥6 rows
- [ ] Related Skills table present
- [ ] `Automate This` block present and factual
- [ ] `evals/evals.json` has ≥3 realistic prompts with assertions
- [ ] No fabricated statistics anywhere in the skill
- [ ] No competitor product named (Gainsight, ChurnZero, Totango, Vitally, Catalyst, Planhat)
- [ ] Questions are tappable, batched, with a recommended default; nothing asked that `cs-context` answers
- [ ] Assumption Register in the output template wherever the skill can run on a default
- [ ] Accepts arbitrary uploads; points at `ingest.py`; degrades rather than refusing
- [ ] Customer-facing text is fenced in a copyable ```text block below a divider, with no placeholders
- [ ] Names the Operating Rules it enforces, and enforces them in the output template
- [ ] Gives a recommendation and a default, not a menu of options
- [ ] No hedged constructions; no generic advice; the specificity floor is met
- [ ] Business-model profile consulted so model-inappropriate practices are not recommended
- [ ] Brief mode defined and default; Full on request
- [ ] No composite figure stated to the dollar; no probability without a cited backtest
- [ ] Leak scan applied — no health score, risk band, ARR-at-risk, forecast or save-play language in customer text
