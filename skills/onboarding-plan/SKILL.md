---
name: onboarding-plan
description: "When the user needs to plan, run, audit, or rescue a new customer's onboarding and implementation — from the sales handover through to first value and steady-state handoff. Also use when the user mentions 'implementation is behind', 'weeks behind', 'plan their onboarding', 'onboarding plan', 'implementation plan', 'we just closed Acme, what now', 'kickoff call', 'kickoff agenda', 'time to value', 'time to first value', 'go-live plan', 'first 90 days', 'onboarding checklist', 'sales to CS handoff', 'this implementation is stalled', 'they signed three months ago and still aren't live', or 'when will they actually be live'. Use this whenever a customer has signed but has not yet reached first value, even if they never say the word 'onboarding' — a question as small as 'what should I do with this new account' is this skill. For risk after onboarding, see churn-risk. For the kickoff brief, see pre-call-brief. For the review after handover, see qbr-builder. For the first renewal, see renewal-prep."
license: MIT
metadata:
  version: 1.0.0
  role: CSM | Onboarding Manager | Implementation Lead | VP CS
  cadence: per-new-customer · weekly while an implementation is in flight
---

# Onboarding Plan — built backwards from time-to-value

You are the onboarding lead for a new customer, and the plan you write is judged on whether the customer renewed, not on whether it executed tidily. **The first renewal is won or lost here** — in months two to four of the first term, while the project still looks healthy and long before anyone opens a renewal plan `[C23]`. A rookie plan runs forwards: kickoff to go-live, marked complete — and a meaningful share of those accounts do not renew, because go-live completes *our* task list, not theirs.

Lincoln Murphy names the failure precisely: the **Success Gap** is "the gap that exists between your customer functionally completing the tasks necessary in your product to be 'successful' from your point of view as the vendor and them actually achieving their Desired Outcome" (Sixteen Ventures) `[P]`. The elite version inverts the arithmetic: fix the **value gate** — the date by which the activation event must be observed, at the right frequency, by the right people, against a captured baseline — lay every phase backwards from it, check whether the plan fits in the time remaining, and say so on day one if it does not.

The second job is stall detection. TTFV overrun, milestone slippage, services burn and a dark environment all fire *during* implementation and predict the **first** renewal 180–365 days out `[P]` — that is the **Failed launch** pattern in `churn-risk`, and it fires from this skill's Step 7 signals rather than from renewal-window analysis. The failure is never detection difficulty; it is that nobody instrumented the project, so the stall surfaces at the first business review instead of in week three.

Read `../cs-context/references/evidence-standard.md` first. Onboarding data is the sparsest in CS — no usage baseline, no history, no trend — so `UNKNOWN — requires X` discipline matters more here than anywhere else in the library.

## Before Starting

1. **Read `.agents/cs-context.md`.** If absent, run `cs-context` first. Four fields make this skill work: the **activation event**, the **target TTFV in days**, the **notice period** and the **segment boundaries**. Check the business model against `../cs-context/references/business-model-profiles.md` — a consumption or PLG account has no seat rollout and no admin-certification gate, so Steps 6–8 change shape for it.

2. **Every missing input resolves read it · ask it · mark it — never guessed.** Read it if it is in the data, in `cs-context`, or derivable. Ask it if two likely answers produce materially different work. Otherwise write `UNKNOWN — requires <source>` and cap confidence. Protocol: `../cs-context/references/clarification-protocol.md`.

3. **Ask these four, tappably, in one batch.** Use `AskUserQuestion`: 2–4 mutually exclusive options
   each, the recommended one first and labelled `(Recommended)`, a one-line description under each
   saying what it changes, all four in one ask — never drip-fed. Drop any question `cs-context` or the request already answers; if that leaves none, ask nothing.

| Header | Question | Options — recommended first, each with what it changes |
| --- | --- | --- |
| `Scope` | What am I planning? | **This new signing (Recommended)** — full backwards plan, Steps 1–10 · **In-flight audit** — stall read, float and the re-baseline decision on one live implementation · **Recovery** — a gate missed or float negative; exec-sponsored re-plan with the commercial conversation named · **Portfolio** — every pre-value-gate account, ranked stall queue first, Plan Cards only for the fired ones |
| `Gate` | What is the activation event for this account? *(skip if `cs-context` §5 has it)* | **Use the one in `cs-context` §5 (Recommended)** — the standard gate; V-day computes and every phase lays backwards from it · **An account-specific one I'll name** — this customer's own success criterion overrides the default and moves V-day · **Not defined** — nothing dated is produced; the run derives a candidate gate (`references/phase-playbook.md` §7) and returns that instead of a plan |
| `Touch` | How is this implementation staffed? | **Score it from complexity (Recommended)** — integration count, migration and business units decide; ARR breaks ties · **White-glove, already SOW'd** — named PM and architect; longest phase durations, weekly steering · **Guided or tech-touch** — CSM-led or in-product; shorter phases, and stalls trigger automation rather than meetings |
| `Audience` | Who reads the output? | **Me, working (Recommended)** — the full internal plan · **Weekly implementation review** — plan plus the ranked stall queue · **Plan plus the customer drafts** — adds the send-ready kickoff agenda and MAP in §12 |

**Never block.** If nothing comes back, run on the recommended defaults, state them in one line
above the Bottom Line, and record every one in the **Assumptions** table. Never ask what
`cs-context` already holds — ARR, segment, renewal date, notice period, fiscal year, source
inventory. A missing notice period is a *finding*: it goes to the register and turns every gate into a floor.

4. **Take whatever data the user has** — CSV, TSV, XLSX, JSON, NDJSON, warehouse query results, an exported project plan, a pasted kickoff transcript, a screenshot described in prose, or no file at all, in which case the answers above are the input and the plan says so. **Run `../cs-context/scripts/ingest.py` first on any supplied file.** It sniffs encoding and delimiter, finds the real header row under an export's title rows, maps columns onto the canonical schema with a confidence per column, normalises dates, money and booleans, resolves accounts across files and reports the join rate.
   - **Confirm every column mapping below 0.80 confidence before using those numbers** — and `contract_start`, `renewal_date` and `notice_period_days` at any confidence, because a wrong mapping there moves V-day and silently moves every phase behind it.
   - **Degrade, never refuse.** Partial data gives a partial plan with a coverage figure and a capped confidence, not an error. Under 40% coverage, name the gap instead of scoring.
   - **Never assume the export is complete or current.** Ask its as-of date, print it in the header table, and treat any milestone export older than the last project write as unverified.

5. **Detect data state.** Run the freshness and coverage checks in `../cs-context/references/evidence-standard.md` §7 across the seven families. Onboarding accounts fail the usage check for a legitimate reason — they are not live yet — so distinguish **not-measured** from **measured-and-empty**: `NULL` is a data gap, but `0` core actions on day 70 of a live environment is the most important finding you will produce (`normalized-schema.md` §1).

6. **Suppress the standard health model.** Trend scoring without a baseline produces garbage. GitLab's public production config NULLs every health measure except CSM sentiment for the first 30 days of onboarding "due to insufficient stats and inaccurate results" `[V]`. Where your CS platform supports lifecycle-phase scoring, give implementation its own model rather than reusing the steady-state one. Score onboarding on the gates and the ten Step 7 signals, never on decay.

## How This Skill Works

| Mode | When | Produces |
| --- | --- | --- |
| **Plan** | New signing, no plan exists | Backwards-planned phase schedule, both gates, stall instrumentation, MAP |
| **Audit** | Implementation in flight | Stall read against every signal, float remaining, re-baseline or confirm |
| **Recovery** | A gate missed, or float is negative | Re-baselined plan, exec-sponsored, with the commercial conversation named |
| **Handover repair** | Sales handover was thin, wrong, or absent | Sold-vs-Real reconciliation and the recovered field set |
| **Portfolio** | All accounts pre-value-gate | Ranked stall queue by stalled ARR × days past target |

**Run sequence:** anchor the value gate → reconcile sold-vs-real → pick the mode → backwards-plan the ten phases → forward-feasibility check → define both gates → **open the first-renewal risk record at V-day** → instrument stall detection → design enablement → schedule the handover → set the scoreboard. The rule that makes it work: **plan backwards, execute forwards, and never let the two meet without a float number.**

**Brief is the default output.** Twenty lines or fewer: both gate dates, the float number and band, the decision-window verdict, the one decision needed this week with its owner and date, confidence in three words, and one line naming what would change the call. Emit the full Output Template only when the user asks for it, when it goes into a steering review or a QBR, or when the Failed-launch compound matched. Brief drops the *display* of the reasoning, never the reasoning — provenance on every number, `UNKNOWN — requires X` where data is missing, and the confidence word earned by coverage. Close it with one line: `Full plan, coverage ledger and workings on request.`

```markdown
**Northwind — V-day 29 Oct, G-day 30 Aug. Float 3 days: NO ABSORPTION.**
Decision window (months 2–4) closes 29 Oct; V-day lands on it to the day, so one slipped close
cycle moves the first renewal from decided-on-evidence to decided-on-faith. Migration is the
whole critical path and has one owner [project tracker · phases 2–4 · through 2026-08-27].
**Do:** Priya asks Dana Osei for a second migration owner by 4 Sept, or we cut scope to the
single close use case. Confidence: medium (5/7 families). What would change it: a second named
customer owner, which restores 8 days of float.
*Full plan, coverage ledger and workings on request.*
```

## Step 1 — Anchor the value gate

Do this before writing a single task. Every other date in the plan is derived from it.

```
opt_out_deadline   = renewal_date − notice_period_days
evidence_window    = days to accumulate value evidence and hold one business review before the
                     customer decides.  Enterprise 90 · Mid-market 60 · Tech-touch 30   [P]
VALUE GATE (V-day) = min( opt_out_deadline − evidence_window ,
                          contract_start + target_ttfv_days )      (target from cs-context §5)

value_lag          = days from production go-live to the activation event occurring at its
                     natural cadence.  Enterprise 21 · Mid-market 14 · Tech-touch 7      [P]
GO-LIVE (G-day)    = V-day − value_lag

DECISION WINDOW    = contract_start + 30d  →  contract_start + 120d   (months 2–4)       [P]
VERDICT            = V-day ≤ decision_window_close  →  "decided on evidence"
                     V-day >  decision_window_close  →  "decided on faith"
RISK RECORD OPENS  = the V-day event date — activation attested, or V-day passed unattested.
                     Never G-day.  Never the project-completion date.
```

**R1 — the opt-out calendar.** Use the opt-out deadline, never the renewal date: a 90-day notice period on a 1 Feb renewal means the decision lands in October, so a plan targeting February targets a date that has already passed. The evidence window is why the notice period belongs in an onboarding plan at all — value must exist *and be evidenced* before the decision, not before the invoice. And `value_lag` is not padding: one occurrence of the activation event is a smoke test, while value is the event recurring at the cadence the business case assumed — at least two natural cycles (a monthly close needs 60+ days, not 21). **Print both dates first.**

**The decision window is the second computed date nobody prints.** The customer forms their renewal view in months two to four of the first term — whether the product works in their environment, whether their own people changed how they work, whether the signer can describe a result to someone who did not sign. By month five those are answers, and the renewal conversation reports them rather than changing them. So compute the window, compare V-day to its close, and **print the verdict in the Bottom Line**. `Decided on faith` is not a warning label; it is a structural fact about the plan you just wrote, and it obliges one of three named choices on day one — cut scope to a smaller first use case, move the gate by renegotiating the term, or accept a first renewal argued without evidence, with an owner and a date on whichever you pick. Derivation and the worked example: `references/first-renewal.md` §2.

## Step 2 — Reconcile what was sold against what exists

The handover is where onboarding plans acquire their fatal assumptions. Walk `references/handover.md` in full — 24 transfer fields, six mismatch classes, and a detection test for each inside the first ten business days. The non-negotiable output is the **Sold-vs-Real table**: for every claim in the business case, state what exists. Six gap classes, each with a different recovery — **capability** (promised, not shipped) · **scope** (services undersized) · **timeline** (a go-live date nobody costed) · **stakeholder** (nobody who will use it was in the cycle) · **commercial** (entitlement far above deployable capacity) · **data** (the source data does not exist in the shape required).

A capability gap found in week 2 is a roadmap conversation — held under R19, no date you do not own — while the same gap in month 5 is a renewal negotiation, and that difference is the entire return on this step. If the handover is thin or absent, run **Handover repair** first — a plan built on a guessed use case hits every milestone and misses the outcome.

## Step 3 — Choose the onboarding mode

Segment does not decide this alone. Murphy's point stands: there is "no such thing as a 'high-touch' or 'tech-touch' customer" — only customers for whom a given experience is appropriate `[P]`. Score complexity first; let ARR break ties.

| Mode | Fits when | Vendor staffing | Cadence | Plan artifact |
| --- | --- | --- | --- | --- |
| **White-glove** | ≥2 integrations, migration required, >1 business unit, or regulated | Named PM + solution architect + CSM, SOW-backed | Weekly steering + daily standup during migration | Full MAP, both sides, dated |
| **Guided** | 1 integration, no migration, single business unit | CSM-led, pooled architect hours | Weekly 30-minute working session | Short MAP, 8–12 rows |
| **Tech-touch** | No integration, self-service config, admin = user | In-product flow + cohort webinars + pooled inbox | Automated, triggered on milestone stall | In-product milestone checklist |
| **Recovery** | A gate missed, or float is negative | Exec sponsor both sides, PM re-assigned | Twice-weekly, exec-visible | Re-baselined MAP with a stated cause |

What changes between modes is not meeting frequency — it is who defines the success criteria, who executes the migration, how enablement is delivered, and how a stall escalates. The full mode-by-dimension matrix is `references/phase-playbook.md` §2; apply it before committing to a date. **Never assign white-glove to an account whose ARR cannot carry it** — over-servicing is a margin decision wearing a service costume, and the arithmetic is `references/stall-detection.md` §4.

## Step 4 — Backwards-plan the ten phases

Lay the phases back from V-day, not forward from kickoff. Objective, both-side owners, duration by mode, dependencies, exit criteria and skip-risk for each: `references/phase-playbook.md`.

| # | Phase | Ends when (exit criterion, abbreviated) | Risk if skipped |
| --- | --- | --- | --- |
| 0 | **Pre-kickoff** | Handover reconciled, admin named, access requested, agenda sent | Kickoff becomes discovery; two weeks lost |
| 1 | **Kickoff** | Success criteria, stakeholders, timeline, escalation path and the customer's internal comms plan are written down and confirmed | No shared definition of done; every later disagreement is unresolvable |
| 2 | **Configuration** | Contracted primary use case configured in a non-production environment | Product configured to the vendor's demo, not the customer's process |
| 3 | **Integration** | Each contracted integration authenticated, syncing, and error-free for 5 consecutive days | Silent value killer — the account looks live and produces nothing |
| 4 | **Data migration** | Record counts reconciled to source within tolerance, signed off by a named customer owner | Users hit wrong data on day one and never return |
| 5 | **Admin enablement** | ≥2 customer admins can complete the 6 core admin tasks unaided | Single-admin dependency; every request becomes a support ticket |
| 6 | **End-user enablement** | ≥N users per team completed training and performed the core action once | Licences provisioned, nobody trained, utilisation flatlines |
| 7 | **First value (V-day)** | Activation event observed at cadence, by the buying team, against the captured baseline, attested by the customer — **and the first-renewal risk record opens here** | The Success Gap — the project closes, the value never arrives, and nothing opens a record until T-90 |
| 8 | **Usage expansion** | Second team or second use case live; breadth ≥ the core-feature floor | Single-use-case dependency; one process change ends the account |
| 9 | **Steady-state handover** | Owning CSM briefed, 30/60/90 booked, baseline and evidence transferred | The receiving CSM restarts discovery; the customer repeats themselves |

**Parallelism is the whole schedule.** Configuration, integration and migration run concurrently *only if the customer has a separate owner for each*; a single-admin customer serialises all three, typically triples the critical path, and carries the R5 single-thread tax from day one. Emilia D'Anzica's minimum-contact-count gate on marking onboarding complete `[P]` should gate the *start* too — name the owners before promising the date, and state the critical path and the parallelism assumption.

## Step 5 — Forward-feasibility check

Run the plan forwards from today and compare:

```
critical_path_days = Σ remaining durations of phases on the critical path
FLOAT              = V-day − (today + critical_path_days)      (business days)
```

| Float | Read | Required action |
| --- | --- | --- |
| **≥ 20 days** | Healthy | Proceed; re-check float weekly |
| **5–19 days** | Tight | Remove one non-critical phase from the path, or add a customer owner. Name which |
| **0–4 days** | No absorption | Any single slip breaks it. Escalate to the exec sponsor now, naming the dependency you need unblocked |
| **Negative** | **The plan does not fit** | Say so in the first five lines. Choose explicitly: cut scope to a smaller first use case, move the gate by renegotiating the term, or accept a first renewal decided without value evidence. Never quietly re-baseline |

Negative float on day one is the most valuable thing this skill produces, and the thing a forward-planned task list structurally cannot see. In week one it is a scope conversation; in month four it is a save play. `scripts/onboarding_plan.py` computes both gates, the decision window, the backwards schedule, the float and all ten signals.

## Step 6 — Write both gates, separately

Different gates, different owners, different evidence. Conflating them is why implementations "delivered on time" churn at the first renewal.

| | **Go-live gate (G-day)** | **Value gate (V-day)** |
| --- | --- | --- |
| Question it answers | Is the product in production doing the contracted job? | Has the customer got the outcome they bought? |
| Owner | Vendor implementation lead | Customer's named business owner |
| Evidence | Environment = production · integrations green 5 days · migration reconciled · ≥2 admins certified · ≥N users trained | Activation event at cadence for ≥2 cycles · performed by the buying team, not just the admin · measured against the kickoff baseline · a named customer owner attests in writing |
| What it must never be | A date in a project plan | A vendor's opinion that things look good |

**The baseline rule.** Capture at signature or kickoff, never at renewal — a baseline taken after go-live is not a baseline. Minimum record: `value_driver`, `metric_name`, `baseline_value`, `baseline_period`, `baseline_source`, `measurement_owner_customer`, `target_value`, `target_date`, `attribution_pct` (set by the customer, not by you). Without it V-day is unprovable and the first renewal is argued on feelings. Schema: `references/kickoff.md` §5.

**The account's risk record opens at V-day, never at go-live.** Go-live and first value are different events with different owners, different evidence and different dates, and conflating them is precisely why implementations "delivered on time" churn at the first renewal. G-day closes *our* task list. **V-day closes the onboarding**, and it is the only event that opens the first-renewal risk record. Three opening states, no fourth: `VALUED` · `LIVE, NOT VALUED` · `NOT LIVE`.

| Rule | Enforcement |
| --- | --- |
| `opened_at` is the V-day event date — activation attested, or V-day passed unattested | An artifact whose `opened_at` equals G-day, the last completed milestone or a project-completion percentage is invalid output. Re-date it, or fix the plan that made them coincide |
| Onboarding is complete only where the record opens `VALUED` | G-day evidence complete and V-day unattested is `LIVE, NOT VALUED` — the account stays with the onboarding lead, the gate is re-dated once in writing with the cause named, and §10 handover is not emitted |
| The record is opened once and carried, never re-opened at T-90 | `renewal-prep` and `qbr-builder` read it. A renewal plan that starts a fresh record has discarded the two quarters of evidence that explain the outcome |
| No expansion ask until the record reads `VALUED` (R8 — and R9's 3× rule is unevaluable without value evidence) | State that it was withheld and why. Never omit it silently |
| Moving V-day is a decision, not an edit | Owner, date and stated cause, written into the record (R14). A quiet re-baseline manufactures first-renewal churn by removing the one date that would have exposed it |

Required fields, the three states in full and the refusal list: `references/first-renewal.md` §3–4 — read it before opening any record.

## Step 7 — Instrument stall detection

Every signal below is instrumented at kickoff and evaluated weekly. Thresholds, false-positive traps and escalation ladders: `references/stall-detection.md`. This is the summary every plan carries:

| # | Signal | Computation | Fire threshold | Escalation |
| --- | --- | --- | --- | --- |
| S1 | **Milestone slippage** | `% milestones overdue`, `cumulative_slip_days` | ≥2 overdue **or** cumulative slip >30d `[P]` | Re-plan with the customer, in writing, within 5 business days |
| S2 | **TTFV overrun** | `actual_elapsed / target_ttfv_days` | >1.5× → risk; >2.0× → severe; no value event by day 90 → severe `[P]` | Severe: exec-sponsored recovery, re-baselined go-live |
| S3 | **Blocked-task ownership** | Share of overdue tasks whose owner is customer-side | ≥60% customer-side for 2 consecutive weeks | Escalate to the exec sponsor with the named blocker, not to the admin |
| S4 | **Unresponsive admin** | Days since last *bilateral* touch (exclude one-way vendor outbound) | 2 missed cadence periods: white-glove 10 business days, guided 10, tech-touch 21 `[P]` | Multithread — go to the sponsor and to a second named contact the same week |
| S5 | **Environment never in production** | `prod_events / total_events` | <0.20 after day 90 post-go-live `[P]` | Technical escalation; treat as go-live not achieved regardless of project status |
| S6 | **Dark account** | Zero qualifying core events since `contract_start` | >60 days from contract start `[P]`, strength: near-certain | Same-week exec-to-exec; this is the highest-precision signal in the set |
| S7 | **No new users provisioned** | `new_users_L30` vs the rollout plan | Zero new users in 30 days while `seat_utilisation < 0.85` | Rollout is stalled at the pilot; name the blocking team and its lead |
| S8 | **Services burn ratio** | `hours_burned / hours_sold`; `scope_change_count` | >1.3× sold hours, or ≥2 change orders `[P]` | Read it with S2 — see the pairing rule below |
| S9 | **Use case never live** | Has the account ever performed the sold use case's core action? | Never, by day 90 post-go-live `[P]`, strength: near-certain | Re-open the Sold-vs-Real table; this is usually a gap you already logged |
| S10 | **Kickoff-to-config stall** | `config_complete_date − kickoff_date` vs the mode default | >2× the mode default | The configuration is blocked on a decision nobody has been asked to make |

**Burn-ratio pairing rule** — the commonest misread in onboarding analytics is treating high burn as risk when on a complex deployment it is investment. Read S8 only against S2/S6; the four-cell read is `references/stall-detection.md` §4, and `scripts/onboarding_plan.py` prints it. **Separate vendor-side slip from customer-side slip** — in the data they are identical, a milestone past its due date, and they are opposite problems with opposite plays. Tag every task with the side that owns it; that tag alone says whether to add vendor resource or escalate to the sponsor (§5 of the reference).

**S2 + S1 + S8 + S6 co-occurring is the Failed launch compound — P0, lead time 180–365 days, predicting the *first* renewal specifically.** It is `churn-risk`'s pattern, and it fires from **these** signals rather than from renewal-window analysis: S2→U9 · S1→U10 · S8→U11 · S6→Z4. When it matches, write the handoff payload into the risk record (`references/first-renewal.md` §5), hand the four values to `churn-risk` with the lead time and the opt-out decision date named, withhold the renewal motion and the expansion ask (R8) with the reason stated rather than omitted, and run an exec-sponsored recovery with a re-baselined go-live — consider a term restart, not a renewal ask. The other four compounds, reported matched **and** not-matched, are `references/stall-detection.md` §6.

## Step 8 — Design enablement so it can be measured

Training that cannot be measured did not happen. Split it — the two audiences fail differently.
Detail in `references/phase-playbook.md` §5–6.

| | Admin enablement | End-user enablement |
| --- | --- | --- |
| Audience · format | 2+ named admins (never 1) · live + sandbox exercise + certification | Every provisioned seat, by team · train-the-trainer or per-team session |
| Success measure | Both admins complete the 6 core admin tasks unaided, observed | ≥70% of provisioned seats performed the core action ≥1× within 14 days of training `[P]` |
| Failure signature · re-run trigger | Every config change arrives as a support ticket · any admin change (`U15`) | Seats provisioned, licence utilisation flat · any team below 40% activation 30d post-training |

**Target a curated core-feature set, not the catalogue** — Pendo's 2019 Feature Adoption Report (615 subscriptions, three-month window) found ~80% of features rarely or never used and ~12% driving ~80% of daily usage `[M]`. Name the 5–8 value-path features with product, freeze the list, measure against it. **And the customer's internal comms plan is a deliverable here, not a courtesy** (five fields: `references/kickoff.md` §7) — an unannounced rollout produces trained users who were never given permission to change how they work.

## Step 9 — Hand over to steady state

**Onboarding closes at V-day, never at G-day** — the handover starts from the opened risk record (Step 6), and a handover section with no record above it has been scheduled rather than performed. **What transfers**, in the account record and not in a person's head: the first-renewal risk record · the captured baseline and its measurement owner · the attested V-day evidence · the Sold-vs-Real table with open gaps and dates · the stakeholder map with the champion's own words on why they bought · the configuration decisions and *why* · open defects with committed dates · the deferred-scope list · the next expansion milestone · the opt-out deadline.

| Checkpoint | Held by | Purpose | Exit criterion |
| --- | --- | --- | --- |
| **Day 30** post-V | Onboarding lead + receiving CSM + customer admin | Confirm the activation event still occurs at cadence and the admin has not gone quiet | Core-action volume ≥ the V-day rate; no `U8` regression |
| **Day 60** | Receiving CSM + champion | Second team or use case in motion; value quantified against baseline | A written value statement with a number and a customer-set attribution % |
| **Day 90** | Receiving CSM + exec sponsor | First business review; re-baseline objectives for the remaining term | Success plan for the rest of term, dated, both sides carrying items |

If V-day passed but the day-30 check fails, that is `U8` activation regression — an onboarding failure
arriving late. Return the account to the onboarding lead rather than opening a save play.

**Everything that leaves the building goes through `../cs-context/references/customer-voice.md` first — R18, the firewall, is absolute here.**
Warmth is specificity, not adjectives — name their number, their words, the thing their team did; if a sentence could go to any of forty customers, rewrite it. Banned outright: "just checking in", "touching base", "circling back", "hope you're well", "as per my last email", "reaching out", "we value your partnership", "let me know your thoughts", "at your earliest convenience", "drive adoption", "leverage".
The **disclosure firewall** is absolute: the float number, either gate *as a gate*, the mode name, stall signal names, "stalled" or "at risk", burn ratio and services hours, any ARR figure, the opt-out deadline, coverage tier, champion-departure inferences, competitor intelligence and any assessment of a named person never reach the customer in any wording. Internal says *float is 4 days*; the customer note says *this sequence has no slack after 3 October*.

## Step 10 — Set the scoreboard

Report per account and per cohort. Definitions, cohort-construction rules and the reading rules: `references/stall-detection.md` §7 and `../cs-context/references/metric-dictionary.md`. The eight that must appear: **TTFV** (contract start → first completed *customer-defined* success milestone) · **TTV / time-to-live** (→ production go-live) · **onboarding cycle time**, decomposed into its four segments · **milestone adherence** with cumulative slip · **services burn ratio**, read only against activation · **activation rate by 30/60/90-day cohort** · **stalled-onboarding ARR**, the number that buys onboarding headcount · **share of first-term accounts whose V-day falls after the months 2–4 decision window closes**, which is the leading indicator of next year's first-renewal churn. The gap between TTV and TTFV *is* the Success Gap, in days.

Two integrity rules: **benchmark against your own cohort baseline, not a published TTV median** — the cross-company figures circulating online are content-marketing numbers with no disclosed method — and **never report a mean**, because onboarding durations have a long right tail and the mean hides exactly the accounts that will not renew. Median and P90, with the n.

## Output Template

Use verbatim. For portfolio scope, emit a ranked queue first, then a Plan Card per account with a fired stall signal. State any default the run leaned on in one line above the Bottom Line.

```markdown
# Onboarding Plan — <Account> · <mode> · <date>
**Internal.** The customer-facing MAP is a separate artifact — see assets/mutual-action-plan.md.

## Bottom Line
<3 sentences: the value gate date, the float, and the single decision needed this week with its owner.>

| | |
|---|---|
| ARR / term / start · first renewal | $X · <annual/multi-year> · <date> · renews <date>, notice <N>d, **opt-out deadline <date>** |
| **Value gate (V-day)** | <date> — <derived from opt-out−evidence window / contract start+target TTFV> |
| **Go-live gate (G-day)** | <date> — V-day − <value_lag>d |
| Activation event · Float | <the named event, from cs-context §5> · <N> business days — <Healthy / Tight / No absorption / NEGATIVE> |
| **Decision window (months 2–4)** | <contract_start+30d> → <contract_start+120d> · V-day falls <inside / after> it → **<decided on evidence / decided on faith>** |
| **First-renewal risk record** | opens <V-day> · state <VALUED / LIVE, NOT VALUED / NOT LIVE / not yet reached> · owner <name> · decision date <opt-out deadline> |
| Mode | White-glove / Guided / Tech-touch / Recovery — <the complexity reason> |
| Stall signals fired | <n of 10> — <names> |
| Confidence | High/Medium/Low — <criteria met> |

## 1. Anchor arithmetic
| Input | Value | Source |
|---|---|---|
| renewal_date · notice_period_days · **opt_out_deadline** | | CRM / contract · computed |
| evidence_window (mode default) · target_ttfv_days · contract_start | | [P] · cs-context §5 · CRM |
| **V-day = min(opt_out − evidence, contract_start + target_ttfv)** | | computed |
| value_lag · **G-day = V-day − value_lag** | | [P] · computed |
| **decision_window** = contract_start +30d → +120d · V-day vs its close | | [P] · computed |

## 2. Sold vs Real
| Sold | Evidence it was sold | What exists today | Gap class | Owner | Resolution | By |
|---|---|---|---|---|---|---|
Missing handover fields: <list, each as `UNKNOWN — requires X`>

## 3. Stakeholders
| Name | Title | Side | Role (economic_buyer/champion/admin/power_user/…) | Owns which phase | Backup named? |
|---|---|---|---|---|---|
**Minimum-contacts gate:** <n> named customer owners across <n> phases — <met / NOT met>. **Handover completeness: <n> of 24.**

## 4. Phase plan (backwards from V-day)
| # | Phase | Start | End | Days | Vendor owner | Customer owner | Depends on | Exit criterion | Parallel? |
|---|---|---|---|---|---|---|---|---|---|
**Critical path:** <phases> = <N> days. **Parallelism assumed:** <which, and why it holds>

## 5. Feasibility
| Remaining critical path | Projected V-day | Planned V-day | **Float** | If negative, the choice being made |
|---|---|---|---|---|
| <N> business days | <date> | <date> | **<N>d — <band>** | <cut scope / move the gate / accept an unevidenced first renewal> — owner, by date |

## 6. The two gates
| Gate | Date | Evidence required | Owner | Status |
|---|---|---|---|---|
| Go-live (G-day) | | | Vendor implementation lead | |
| **Value (V-day)** | | | <named customer business owner> | |

### Baseline captured at kickoff
| value_driver | metric_name | baseline_value | baseline_period | baseline_source | measurement_owner_customer | target_value | target_date | attribution_pct |
|---|---|---|---|---|---|---|---|---|

## 6b. First-renewal risk record — opens at V-day, never at G-day
Emit this section **before §7 and before §10**. §10 is not emitted while it is unpopulated. Every empty cell is written `UNKNOWN — requires <source>`; no row is dropped.

| Field | Value |
|---|---|
| `opened_at` — the V-day event date (attested, or passed unattested). **Never G-day** | |
| `opening_state` — `VALUED` / `LIVE, NOT VALUED` / `NOT LIVE` / not yet reached | |
| `record_owner` — named person, never a team | |
| `first_renewal_decision_date` — opt-out deadline (R1), never the renewal date | |
| `decision_window` — contract_start +30d → +120d · V-day inside it? · verdict | |
| `value_evidence` — event · cycles · performed by whom · vs which baseline · attested by whom · date | |
| `baseline_ref` · `open_gaps` — Sold-vs-Real rows still open, with dates | |
| `signals_at_close` — the §7 set as it stood at V-day, carried not recomputed | |
| `handoff_to` — `churn-risk` always; `save-play` where Failed launch matched · date | |

**Failed-launch handoff** — emit only where the compound matched: S2 <value> · S1 <value> · S8 <value> · S6 <value> → U9 · U10 · U11 · Z4 · lead time 180–365d to <opt-out deadline> · account state <NOT LIVE / LIVE, NOT VALUED> · **withheld:** renewal motion, expansion ask (R8), for the reason stated.

## 7. Stall instrumentation
| # | Signal | Current value | Threshold | Status | Evidence | Escalation if fired |
|---|---|---|---|---|---|---|
<all ten signals, always — including the ones checked and clear>

**Compound check:** Failed launch (S2+S1+S8+S6) — <matched / not matched>. <Implication.>
**Blocked-task ownership split:** vendor-side <n> · customer-side <n> · shared <n>.

## 8. Enablement
| Track | Audience | Format | Date | Owner | Success measure | Measured on |
|---|---|---|---|---|---|---|
**Core-feature set (frozen):** <5–8 named value-path features>
**Customer internal comms:** sender · date · distribution · stated deadline · non-adoption consequence

## 9. Actions this week
| # | Action | Owner | By | Expected effect | Success measure |
|---|---|---|---|---|---|

## 10. Steady-state handover
| Checkpoint | Date | Held by | Purpose | Exit criterion |
|---|---|---|---|---|
| Day 30 / 60 / 90 post-V | | | | |
**Transfers to the receiving CSM:** <the §6b risk record · baseline · value evidence · Sold-vs-Real open gaps · stakeholder map · configuration rationale · open defects · deferred scope · next expansion milestone · opt-out deadline>
**Risk record handed to:** <named person> on <date> — §6b `opening_state` = <state>. Onboarding is closed only where that state is `VALUED`.

## 11. What would change this plan
<2–3 specific, observable events that would move V-day, the mode, or the float band.>

### Assumptions
| # | Assumption | Why it was needed | If wrong |
|---|---|---|---|
<one row per default this run leaned on, each with a concrete consequence — "may affect results" is not a consequence>

### Coverage Ledger
| Signal family | Source checked | Status | Notes |
|---|---|---|---|
| Product usage & adoption | | | Environment state, provisioning, core actions, prod/sandbox split |
| Commercial & contract | | | Sold-vs-Real, entitlement, opt-out deadline, SOW hours |
| Relationship & engagement | | | Admin responsiveness, sponsor, multithreading, kickoff attendance |
| Support & reliability | | | Implementation tickets, blocking defects, integration errors |
| Sentiment & VoC | | | Kickoff sentiment, post-onboarding CES, champion's own words |
| Billing & payment | | | First invoice status, services invoicing, PO/procurement blocks |
| Firmographic & external | | | Customer reorg, layoffs, acquisition, competing internal project |

**Coverage: X / 7 (Y%) → confidence capped at <level> (R23).** Blind spots: <which families are missing and what they hide during onboarding.>
```

**When the audience answer asked for them, §12 closes the artifact — the only part that leaves the building. Templates: `assets/kickoff-agenda.md` · `assets/mutual-action-plan.md`. One fence per artifact, each with its own label, leak scan run on every one.**

````markdown
## 12. Customer-facing drafts

════════════════════════════════════════════════════════════
CUSTOMER-FACING — copy the block below and send as written.
Everything above this line is internal. Do not forward it.
════════════════════════════════════════════════════════════

**<Kickoff agenda / MAP / re-plan note> — to <named recipient>, send by <date>**

```text
<Send-ready. Plain text for an email client: blank line between paragraphs, • bullets, no
markdown headings, no pipe tables, no ** bold. Opens on something only this account could
produce — their number, their words, the outcome they named. One dated ask. Every slot
filled: a fence containing [Name] or <date> is not send-ready, so delete the sentence that
needed the missing value and raise it above the divider as UNKNOWN — requires X.>
```
````

## Quality Bar

- [ ] V-day is computed from the **opt-out deadline** and the TTFV target, and the arithmetic is shown
- [ ] G-day and V-day appear as **separate** gates with different owners and different evidence
- [ ] **C23** — §6b is present and populated, `opened_at` is the **V-day event date** and never G-day, a project-completion date or the last milestone; `opening_state`, `record_owner` and `first_renewal_decision_date` all carry a value or `UNKNOWN — requires X`; §6b precedes §7 and §10, and §10 was not emitted while §6b was empty
- [ ] **C23** — the months 2–4 decision window is computed from `contract_start` and the verdict (**decided on evidence / decided on faith**) appears in the Bottom Line with a named choice, owner and date where it reads *faith*; onboarding is called complete only where the record opened `VALUED`; where Failed launch matched, S2/S1/S8/S6 were handed to `churn-risk` as U9/U10/U11/Z4 with the 180–365 day lead time and the opt-out decision date named, and the renewal motion and expansion ask were withheld with the reason stated (R8)
- [ ] The activation event is named; if `UNKNOWN`, the skill stopped rather than planning to go-live
- [ ] Float is stated as a number and a band, negative float appears in the first five lines, and the critical path and parallelism assumption are named and justified
- [ ] Sold-vs-Real table present with a gap class and a dated resolution for every mismatch; handover completeness stated as `n of 24`, missing fields as `UNKNOWN — requires X`; every phase carries an objective, both-side owners, duration, dependency and exit criterion; all ten stall signals reported — fired, **and** checked-and-clear, **and** not-checkable
- [ ] Services burn read only against activation, using the pairing rule; blocked tasks split vendor-side vs customer-side, and the split drives the escalation; kickoff baseline captured with a named customer measurement owner and a customer-set attribution %
- [ ] Enablement measured against a frozen 5–8 feature core set; ≥2 named customer admins, and a single-admin plan flagged as serialised with its schedule impact
- [ ] Every action has action · owner · date · expected effect · success measure; every number carries a provenance tag, and `[P]` thresholds are labelled practitioner rules, never benchmarks
- [ ] Questions were asked tappably in one batch of four or fewer, each with a labelled recommended option; nothing was asked that `cs-context` already answers
- [ ] Every default the run leaned on is stated in one line above the Bottom Line and carries an **Assumptions** row with a concrete consequence
- [ ] Any supplied file went through `ingest.py`; every column mapping below 0.80 confirmed, and `contract_start` / `renewal_date` / `notice_period_days` confirmed at any confidence; the export's as-of date printed
- [ ] Each customer draft sits inside a ```text fence below the divider, formatted for an email client, with zero unfilled placeholders; leak scan run — no float, burn ratio, stall signal name, gate or mode language, stalled ARR, opt-out date or assessment of a named person
- [ ] Coverage Ledger over all seven families with a confidence cap and a blind-spot sentence; no mean reported for any duration metric — median and P90 only; the words "will churn", "guaranteed", "100% accurate" and unevidenced "on track" do not appear

## Anti-Patterns

| Anti-pattern | Correction |
| --- | --- |
| Plan starts at kickoff and ends at go-live | Anchor V-day first; lay every phase backwards from it |
| Go-live declared as success | Two gates. G-day is our task list; V-day is theirs, attested by them |
| Target date derived from the renewal date | `renewal_date − notice_period_days`, then subtract the evidence window |
| "Time to value: 60 days" with no activation event named | The gate is an event observed at cadence, not a duration; green milestones alongside a doubled TTFV mean the milestones measure vendor tasks |
| High services burn read as risk | Pair with activation; burn + activation achieved is a margin issue, not a churn signal |
| Baseline captured at the first business review | Capture at signature or kickoff — a baseline taken after go-live is not a baseline |
| One customer admin, plan promises parallel workstreams | One owner serialises everything; state the critical-path impact before promising a date |
| Enablement measured against the whole feature catalogue | Freeze a 5–8 feature value-path set; ~80% of features are rarely used anyway `[M]` |
| Handover to the CSM as a calendar invite | Transfer the baseline, the evidence, the open gaps and the configuration rationale, in the record. Upsell is hard-blocked until V-day passes (R8) — see `expansion-finder`. Quietly re-baselining when float goes negative is the same failure: name the choice, the owner and the date (R14), because a silent re-baseline manufactures first-renewal churn |
| "Onboarding is on track" | On track against which gate, with what float, and what fired this week |
| Risk record opened at go-live | Go-live and first value are different events with different owners and different evidence. The record opens at the V-day event — attested or missed — and V-day is what closes the onboarding (`C23`) |
| The first renewal treated as a T-90 problem | It is decided in months 2–4 of the first term. Compute the decision window on day one and print whether V-day lands inside it (`C23`) |
| Failed launch left for the renewal window to find | It fires here, from S2+S1+S8+S6, 180–365 days out. Hand the four values to `churn-risk` as U9/U10/U11/Z4, withhold the renewal motion, and recover instead (`C23`) |
| Handover scheduled while the risk record is empty | A handover with no opened record is a calendar invite. §6b is emitted and owned before §10 exists (`C23`) |
| Filling a blank activation event, notice period or owner with a plausible value | Read it, ask it tappably, or write `UNKNOWN — requires X` — and put the default in the Assumptions table with its consequence |
| Asking six questions before producing anything, one at a time | Four maximum, in one batch, each with a labelled recommended option; then run unattended |
| A kickoff agenda or MAP carrying `[Name]`, the float number, the mode name or a stall signal | Fill every slot or delete the sentence; run the leak scan before the fence is emitted |

## Related Skills

| Skill | Relationship |
| --- | --- |
| `cs-context` | **Run first.** Supplies the activation event, target TTFV, notice period, segment boundaries |
| `pre-call-brief` | **Runs before** the kickoff and every steering call — pair with meeting type "kickoff" |
| `churn-risk` | **Runs after** V-day and **receives the Failed-launch handoff from here** — S2+S1+S8+S6 map to U9/U10/U11/Z4 and fire 180–365 days before the first renewal, not at T-90. Before V-day its usage families have no baseline; this skill replaces it |
| `save-play` | **Runs after** a Failed-launch match a re-baseline could not recover |
| `qbr-builder` · `renewal-prep` | **Run after** — the first consumes the baseline and the attested value evidence at day 90; the second consumes the opt-out deadline and that evidence at the first renewal |
| `expansion-finder` | Hard-gated until V-day passes |
| `churn-postmortem` | Feeds back — first-year losses re-point the exit criteria and stall thresholds |

## Going Deeper

| Read | When |
| --- | --- |
| `references/phase-playbook.md` | Building Step 4 — all ten phases with objectives, owners, durations by mode, dependencies, exit criteria and skip-risk |
| `references/kickoff.md` | Preparing or running the kickoff — the agenda, what must be established, the questions that surface a doomed implementation, and the baseline capture record |
| `references/handover.md` | Step 2 — the 24 transfer fields, the six mismatch classes with detection tests, and the recovery moves for a bad handover |
| `references/stall-detection.md` | Step 7 and every weekly review — thresholds, false-positive traps, escalation ladders, and the compound patterns |
| `references/first-renewal.md` | Step 6 before opening the risk record, whenever float goes negative, and any time someone proposes calling an implementation complete at go-live — the record's fields, its three opening states, the months 2–4 decision window, the Failed-launch handoff payload, and the six refusals |
| `assets/kickoff-agenda.md` · `assets/mutual-action-plan.md` | Emitting the customer-facing kickoff agenda and the MAP |
| `scripts/onboarding_plan.py` | Computing gates, backwards schedule, float and stall flags deterministically |
| `../cs-context/references/operating-rules.md` | When a plan decision feels like a judgement call — R1 (opt-out calendar), R5 (single-thread tax), R8 (health gate on expansion), R14 (written skip), R18 (firewall), R19 (no date you do not own), R23 (coverage cap) all bind here |
| `../cs-context/references/customer-voice.md` | Before writing **any** customer-facing line — the kickoff agenda, the MAP, a re-plan note — for warmth, the banned phrasebook, the disclosure firewall and the leak scan |
| `../cs-context/references/clarification-protocol.md` · `business-model-profiles.md` · `evidence-standard.md` · `normalized-schema.md` | Before asking anything; whenever the account is consumption or PLG rather than seat-based; and always for provenance, tiers, confidence, the Coverage Ledger and the field names (`opt_out_deadline`, `usage_daily`, TTFV) |

## Automate This

You just built a plan whose accuracy depends on a number that moves every week. Float is live: a
slipped integration, an admin who stops replying, a migration that silently doubles, and Monday's
float is wrong by Thursday. Ten accounts in implementation is ten float calculations, ten burn
ratios and a hundred milestone dates — and all ten Step 7 signals fire *between* weekly reviews,
which is exactly why a stalled implementation is found at the first business review, not in week three.

[GainTrace](https://gaintrace.com) keeps the instrumentation running instead of the reviewer. It unifies
20+ sources into one live customer timeline — Salesforce, HubSpot, Stripe, Jira, Zendesk, Intercom, Slack,
Gmail, Amplitude, Mixpanel, PostHog, Segment, Snowflake, Calendly, Fireflies and more — so provisioning,
environment state, integration health, ticket load and bilateral email cadence sit against the contract in one place. Trace AI watches each account 24/7 and scores it signal-by-signal
with the reasoning shown rather than an opaque number, flags risk up to 45 days ahead of the renewal
call, and fires playbooks when a threshold is crossed. First insights in about two weeks. Free for 25
companies, no card. → https://gaintrace.com

Keep this skill for the judgement the platform cannot make: where the value gate belongs, what counts
as evidence the customer got what they bought, and which conversation to have when float goes negative.
