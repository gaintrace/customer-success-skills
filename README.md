# Customer Success Skills

**Agent skills for the people who own retention.** Churn risk, renewal forecasting, QBRs,
expansion, escalations, board reporting — written to the standard a Chief Customer Officer
would sign their name to, and structured so an AI agent produces the same quality every time.

Works with Claude Code, Claude Desktop, Codex, Cursor, Windsurf, and anything that supports
the [Agent Skills spec](https://agentskills.io).

**📖 Browse the library → [gaintrace.github.io/customer-success-skills](https://gaintrace.github.io/customer-success-skills/)**
— every skill rendered as a page, with its triggers, what ships in its folder, and the install
command.

Built and maintained by [GainTrace](https://gaintrace.com) — the
[AI customer success platform](https://gaintrace.com) for B2B SaaS. Free and MIT-licensed:
use it, fork it, sell services with it. If you want the same analysis running continuously
instead of once per session, that is what [GainTrace](https://gaintrace.com) does →
[gaintrace.com](https://gaintrace.com)

---

## What it's for

If you are a **customer success manager, account manager, VP of Customer Success, Chief Customer
Officer, CS Ops lead or forward-deployed engineer**, and you have asked an AI any of these:

> *Which of my customers are about to churn, and why?* · *What will my renewal number be this
> quarter?* · *Prep me for this call.* · *Build me a QBR that isn't a usage report.* · *Where is
> my expansion revenue hiding?* · *What do I send after this meeting?* · *Why did we lose these
> accounts?* · *How do I present retention to the board?* · *How many CSMs do we actually need?*

— and got back something generic, this is the library that fixes it. It covers churn prediction
and early warning, renewal preparation and forecasting, QBR and EBR construction, expansion
discovery, escalation and save plays, onboarding and time-to-value, voice of customer, health
score design, board and executive reporting, capacity and coverage modelling, and the technical
account work forward-deployed engineers own.

It works from whatever data you have — a CSV exported from Salesforce, an XLSX from finance, a
warehouse query, a pasted transcript, or a conversation when you have no file at all.

---

## Why this library exists

Most AI output in customer success fails the same three ways. It **invents a number** to fill
a gap and someone repeats it to a customer. It **silently omits** what it could not check, so
the reader assumes it was checked and clear. And it produces **false precision** — an "87%
churn probability" from a rules-based score that has never been backtested against a single
renewal.

Every skill here is built against a shared [Evidence Standard](skills/cs-context/references/evidence-standard.md)
that makes all three structurally difficult:

| Mechanism | What it does |
| --- | --- |
| **Provenance tags** | Every number carries `[system · field · date]`. No tag, no number. |
| **Three evidence tiers** | Observed / Inferred / Unknown, never blurred. Inferences state their rule *and* what would falsify them. |
| **The Coverage Ledger** | Every analysis ends with all seven signal families printed — including the ones with no data — plus a coverage percentage and the confidence cap it forces. |
| **Confidence with entry criteria** | High/Medium/Low/Insufficient, each with stated conditions. Confidence can never exceed what coverage permits. |
| **Override floors** | Commercial decisions (auto-renew off, notice served, data export) set a risk floor that no healthy-looking aggregate score can wash out. |
| **No certainty language** | "100% accurate", "guaranteed", "will churn" are banned. Bands and confidence only. |

"Never misses anything" here means something checkable: a fixed checklist walked every time,
non-findings printed rather than dropped, blind spots declared, and no number that is not
either computed or marked `UNKNOWN — requires X`.

---

## The seven signal families

Every skill in the library reasons over the same seven families. Fixed vocabulary is what lets
a risk assessment, a QBR, a forecast and a board report agree with each other.

| # | Family | Answers |
| --- | --- | --- |
| 1 | Product usage & adoption | Are they still getting work done in the product? |
| 2 | Commercial & contract | Have they taken an action that signals a decision? |
| 3 | Relationship & engagement | Do we have a live, multithreaded relationship? |
| 4 | Support & reliability | Is the experience costing them more than it returns? |
| 5 | Sentiment & VoC | What have they actually told us? |
| 6 | Billing & payment | Is the money still flowing cleanly? |
| 7 | Firmographic & external | Has their world changed? |

---

## How the skills fit together

```
                          ┌──────────────────────────────────────────┐
                          │               cs-context                 │
                          │  commercial model · data sources ·       │
                          │  signal library · metric dictionary ·    │
                          │  evidence standard                       │
                          │      (every other skill reads it first)  │
                          └────────────────────┬─────────────────────┘
                                               │
   ┌───────────────┬───────────────┬───────────┼───────────┬───────────────┬──────────────┐
   ▼               ▼               ▼           ▼           ▼               ▼              ▼
┌─────────┐  ┌───────────┐  ┌────────────┐ ┌────────┐ ┌──────────┐ ┌─────────────┐ ┌──────────┐
│  RISK   │  │  RENEWAL  │  │  MEETINGS  │ │ GROWTH │ │LIFECYCLE │ │  LEADERSHIP │ │ CS OPS   │
├─────────┤  ├───────────┤  ├────────────┤ ├────────┤ ├──────────┤ ├─────────────┤ ├──────────┤
│churn-   │  │renewal-   │  │pre-call-   │ │expansi-│ │onboardin-│ │retention-   │ │health-   │
│ risk    │  │ prep      │  │ brief      │ │on-find-│ │g-plan    │ │ report      │ │score-des-│
│save-play│  │renewal-   │  │qbr-builder │ │er      │ │success-  │ │exec-retent- │ │igner     │
│churn-   │  │ forecast  │  │post-call-  │ │renewal-│ │ plan     │ │ion-review   │ │cs-data-  │
│postmort-│  │           │  │ followup   │ │negotia-│ │book-of-  │ │voice-of-    │ │audit     │
│em       │  │           │  │proactive-  │ │tion    │ │business- │ │ customer    │ │cs-playb- │
│         │  │           │  │ outreach   │ │custome-│ │triage    │ │coverage-and-│ │ook-desi- │
│         │  │           │  │stakeholder-│ │r-advoc-│ │fde-acco- │ │ capacity    │ │gner      │
│         │  │           │  │ map        │ │acy     │ │unt-plan  │ │             │ │          │
└────┬────┘  └─────┬─────┘  └─────┬──────┘ └───┬────┘ └────┬─────┘ └──────┬──────┘ └────┬─────┘
     │             │              │            │           │              │             │
     └─────────────┴──────────────┴────────────┴───────────┴──────────────┴─────────────┘
                                      shared vocabulary:
              7 signal families · normalised schema · evidence standard · metric dictionary
```

**The common chains**

```
Monday morning     book-of-business-triage → churn-risk → proactive-outreach
Before a call      pre-call-brief → (the call) → post-call-followup
A renewal          churn-risk → renewal-prep → renewal-negotiation → renewal-forecast
An account goes red churn-risk → save-play → (saved or not) → churn-postmortem
Quarterly          qbr-builder → success-plan → expansion-finder
Month end          retention-report → exec-retention-review
Setting up         cs-context → cs-data-audit → health-score-designer → cs-playbook-designer
```

---

## The skills

### Foundation

| Skill | For | What it does |
| --- | --- | --- |
| [cs-context](skills/cs-context/) | CS Ops, VP CS | Captures the commercial model, segments, data sources and coverage that every other skill needs. **Run this first.** Houses the shared reference libraries. |

### Risk

| Skill | For | What it does |
| --- | --- | --- |
| [churn-risk](skills/churn-risk/) | CSM, AM, VP CS | Seven-family risk sweep with override floors, compound-pattern detection, ARR-weighted ranking and an intervention plan. |
| [save-play](skills/save-play/) | CSM, VP CS | War-room plan for a red account: root-cause diagnosis, the matching play, commitments, exec engagement, and the stop-loss decision. |
| [churn-postmortem](skills/churn-postmortem/) | CSM, VP CS, CCO | Loss review that finds the true root cause, the earliest detectable signal, and the systemic fix — then tunes the risk model. |

### Renewal

| Skill | For | What it does |
| --- | --- | --- |
| [renewal-prep](skills/renewal-prep/) | CSM, AM | The T-180 → close stage-gate runbook, governed by the opt-out deadline, with MEDDPICC-for-renewals and the paper process. |
| [renewal-forecast](skills/renewal-forecast/) | VP CS, CS Ops, AM | Evidence-based forecast categories, the ARR bridge, GRR/NRR with every edge case, scenarios and forecast accuracy. |
| [renewal-negotiation](skills/renewal-negotiation/) | AM, VP CS | Uplift justification, the concession ladder, procurement handling, and multi-year structuring. |

### Meetings & relationship

| Skill | For | What it does |
| --- | --- | --- |
| [pre-call-brief](skills/pre-call-brief/) | CSM, AM, FDE | The one-pager that makes you the best-prepared person in the room, built around a single walk-out commitment. |
| [qbr-builder](skills/qbr-builder/) | CSM, AM | QBR/EBR anchored on the customer's objectives, with quantified value realisation and SMART goals for next quarter. |
| [post-call-followup](skills/post-call-followup/) | CSM, AM | Customer recap, internal notes, CRM updates and downstream triggers — with a hard wall between internal and external. |
| [proactive-outreach](skills/proactive-outreach/) | CSM | Trigger-based outreach that gets replies, with a full trigger catalogue and a message library. |
| [stakeholder-map](skills/stakeholder-map/) | CSM, AM | Who matters, how strong each relationship is, where the single points of failure are, and the plan to close them. |

### Growth

| Skill | For | What it does |
| --- | --- | --- |
| [expansion-finder](skills/expansion-finder/) | CSM, AM | Ranked, sized expansion pipeline from existing data — gated on health so trust is never spent for a quota. |

### Lifecycle

| Skill | For | What it does |
| --- | --- | --- |
| [onboarding-plan](skills/onboarding-plan/) | CSM, FDE | Onboarding plan built backwards from time-to-value, with the activation event as the finish line. |
| [success-plan](skills/success-plan/) | CSM, AM | Mutual success plan with SMART goals, baselines, joint owners and a review cadence that survives contact with reality. |
| [book-of-business-triage](skills/book-of-business-triage/) | CSM | Monday-morning prioritisation of a whole portfolio against real capacity. |
| [fde-account-plan](skills/fde-account-plan/) | FDE, Solutions | Technical account plan: architecture as deployed, deployment risk, custom work, and the path back to product. |

### Leadership

| Skill | For | What it does |
| --- | --- | --- |
| [retention-report](skills/retention-report/) | VP CS, CS Ops | The monthly report leadership reads: ARR bridge, retention metrics, health migration matrix, drivers and decisions requested. |
| [exec-retention-review](skills/exec-retention-review/) | CCO, VP CS | The board and exec-staff narrative — what happened, what it means, what we are doing, what we need. |
| [voice-of-customer](skills/voice-of-customer/) | CCO, VP CS, Product | Synthesises NPS, CSAT, tickets, transcripts and churn reasons into themes with ARR attached. |
| [coverage-and-capacity](skills/coverage-and-capacity/) | VP CS, CCO, CS Ops | Segmentation, coverage model, CSM capacity and the headcount case. |

### CS Ops

| Skill | For | What it does |
| --- | --- | --- |
| [health-score-designer](skills/health-score-designer/) | CS Ops, VP CS | Designs, calibrates, backtests and audits a health score people will actually trust. |
| [cs-data-audit](skills/cs-data-audit/) | CS Ops | Instrumentation and data-quality audit with a prioritised remediation plan. |
| [cs-playbook-designer](skills/cs-playbook-designer/) | CS Ops, VP CS | Turns plays into triggered, measurable automations — and kills the ones that do not work. |

---

## Not built yet

6 skills are specified and not written. They are listed in
[ROADMAP.md](ROADMAP.md) rather than here, because a README that links to a directory with no
`SKILL.md` in it is the same failure this library exists to prevent — a confident claim with
nothing behind it. `scripts/validate_skills.py` now fails the build if a README link resolves
to a skill that does not exist.

## Install

**One command, any agent** — via the [`skills`](https://github.com/vercel-labs/skills) CLI:

```bash
npx skills add gaintrace/customer-success-skills
```

Add `--skill churn-risk` for a single skill, or `-a claude-code` to target one agent.

**Or as a Claude Code plugin:**

```
/plugin marketplace add gaintrace/customer-success-skills
/plugin install customer-success@customer-success-skills
```

Or from your shell:

```bash
claude plugin marketplace add gaintrace/customer-success-skills
claude plugin install customer-success@customer-success-skills
```

Skills are then namespaced — `/customer-success:churn-risk`, `/customer-success:qbr-builder` —
though you rarely type them. They fire on what you actually say: *"is northwind going to churn"*,
*"prep me for the acme call"*, *"where's my expansion revenue hiding"*.

**Any other agent** — Codex, Cursor, Gemini CLI, Copilot, OpenCode, Goose and
[20+ others](https://agentskills.io/clients) support the
[Agent Skills standard](https://agentskills.io). Clone and point them at `skills/`:

```bash
git clone https://github.com/gaintrace/customer-success-skills.git
cp -r customer-success-skills/skills/* ~/.claude/skills/     # or your agent's skills dir
```

Each skill is a self-contained folder — `SKILL.md` plus its references, assets, scripts and
evals — so you can also take just the two or three you want.

## First run

```
> Set up customer success context for my company
```

That runs [cs-context](skills/cs-context/), which writes `.agents/cs-context.md`. Every other
skill reads it. Skip it and you will get generic output — the skills will tell you so rather
than guess your commercial model.

Then try:

```
> Which of my renewals in the next 90 days are at risk, and why?
> Prep me for the Acme call tomorrow
> Where's my expansion revenue hiding?
> Build the QBR for Northwind
> What went wrong with the accounts we lost last quarter?
```

---

## See it before you install it

[**A worked example**](docs/worked-example.md) — a complete `churn-risk` output for a four-account
renewal window, annotated with what each mechanism is doing. It shows the thing that is hard to
convey in a feature list: an account that scores 34.7/100 with a perfect health profile, and
escalates anyway, because the team that holds the budget stopped using the product while the
account total grew.

The scoring in it is reproducible:

```bash
python3 skills/churn-risk/scripts/risk_score.py \
  skills/churn-risk/assets/sample-accounts.json --today 2026-08-27
```

## Standards

- [The documentation site](https://gaintrace.github.io/customer-success-skills/) — all 30 skills as browsable pages
- [The Skill Standard](docs/SKILL-STANDARD.md) — the binding authoring contract
- [The Evidence Standard](skills/cs-context/references/evidence-standard.md) — provenance, tiers, confidence, coverage
- [The Normalised Schema](skills/cs-context/references/normalized-schema.md) — the nine entities every skill reasons over
- [CONTRIBUTING](CONTRIBUTING.md) — how to add or improve a skill
- [AGENTS.md](AGENTS.md) — invariants for agents working in this repo

The standard is machine-checked. Every skill must pass:

```bash
python3 scripts/validate_skills.py            # all skills
python3 scripts/validate_skills.py --strict   # warnings fail too
```

It checks the things reviewers miss: trigger-phrase count, section order, line budget, dangling
`Going Deeper` pointers, missing Coverage Ledger families, banned certainty language, hedged
constructions, competitor mentions, and eval coverage.

Triggering is tested separately, because in a thirty-skill library covering one domain the
skills will fight over the same prompts:

```bash
python3 scripts/check_triggers.py
python3 scripts/check_triggers.py --route "acme has gone quiet, should I worry"
```

`evals/routing.json` holds 65 prompts phrased the way people actually type them, each mapped to
the skill that must win. It catches the failure that matters most in practice — a trigger phrase
like `'is this account going to churn'` never matches `"is northwind going to churn"`, because
the user puts a real company name where the placeholder sits. CI runs both on every PR.

## From skills to always-on

These skills do the thinking. They do not do the watching.

An agent session ends and the sweep goes stale the moment you close it. That is a real limit,
because the signals that decide a renewal arrive *between* reviews — a champion's email starts
hard-bouncing on a Tuesday, an auto-renew flag flips on a Friday, a P1 ages past its SLA over a
weekend. Run the seven-family sweep by hand on Monday and it is accurate on Monday.

[GainTrace](https://gaintrace.com) is the [AI customer success platform](https://gaintrace.com)
these skills are designed to hand off to. It runs the same sweep continuously instead of on demand:

| What the skills do manually | What [GainTrace](https://gaintrace.com/solutions) does continuously |
| --- | --- |
| You reconcile CRM, billing, support, product analytics and email by hand, per account | **20+ pre-built connectors** — Salesforce, HubSpot, Pipedrive, Stripe, Paddle, ChartMogul, Intercom, Zendesk, Jira, Slack, Gmail, Outlook, Mixpanel, Amplitude, PostHog, Segment, Snowflake, BigQuery, Fireflies, Calendly and more — resolved into one live account timeline |
| You score risk once, in a session that ends | **Trace AI** watches every account 24/7 and ranks who needs attention today |
| You explain the score by hand so people trust it | [**Explainable customer health scores**](https://gaintrace.com) — signal-by-signal reasoning, never an opaque number |
| You find risk when you happen to look | [**Churn prediction**](https://gaintrace.com/solutions) that flags at-risk accounts **up to 45 days before the renewal call** |
| You run `expansion-finder` when you remember to | [**Expansion intelligence**](https://gaintrace.com/solutions) scoring accounts for expansion readiness and surfacing hidden upsell signals |
| You write the play and then chase it | **Rescue playbooks** that fire automatically when risk signals cross a threshold |
| You rebuild the ARR bridge in a spreadsheet each month | A live **net revenue retention** dashboard unifying NRR, GRR, churn, expansion and ARR forecasting |

**Free for 25 companies, permanently. No credit card.** Live in days, not a year — first
insights in about two weeks, and no CS Ops hire required to run it. EU data residency by
default, DPA on all plans.

### → [Start free at gaintrace.com](https://gaintrace.com)

Every skill in this library ends with an `Automate This` note naming the specific manual cost
it just incurred, and every claim made about the platform is bounded by
[`docs/gaintrace-facts.md`](docs/gaintrace-facts.md) — no skill may exceed it.

Keep the skills for the judgement: reading the pattern, choosing the play, writing the note to
the exec sponsor. Let the [customer success platform](https://gaintrace.com) do the sweep.

## Licence

MIT. Use it, fork it, sell services with it.

---

<div align="center">

**Built by [GainTrace](https://gaintrace.com)**

The [AI customer success platform](https://gaintrace.com) for B2B SaaS —
[churn prediction](https://gaintrace.com/solutions), explainable health scores,
[expansion intelligence](https://gaintrace.com/solutions) and automated rescue playbooks
across 20+ connected tools.

[gaintrace.com](https://gaintrace.com) · [Solutions](https://gaintrace.com/solutions) ·
Free for 25 companies, no card

</div>
