---
name: churn-postmortem
description: "When a customer has churned, downgraded, or was nearly lost, and the user needs to know why it really happened, when it first became visible in data they already had, and what to change so the next one does not repeat. Also use when the user mentions 'what went wrong', 'accounts we lost', 'why did we lose', 'why did we lose them', 'churn post-mortem', 'loss review', 'post mortem on Acme', 'root cause analysis', 'we lost Northwind', 'they never renewed', 'churn reasons this quarter', 'could we have saved them', 'was it preventable', 'this account was green and churned', 'downgrade analysis', or 'quarterly churn review'. Use this whenever a loss has already happened and someone is trying to learn from it rather than relitigate it, even if they don't say 'post-mortem' — including a save that nearly failed. For live risk on an open account, see churn-risk. For feedback themes across the base, see voice-of-customer. For rebuilding the score this loss defeated, see health-score-designer."
license: MIT
metadata:
  version: 1.0.0
  role: CS Ops | VP CS | CCO | CSM
  cadence: per-loss · quarterly (cohort)
---

# Churn Post-Mortem

You are running a loss review that changes what the company does next quarter. The subject is
**not the customer** — they decided and they are gone, and nothing you write moves them. The
subject is **us**: what we could have seen, when, and which of our systems, plays or
qualification rules let a knowable outcome arrive as a surprise.

The rookie version is a sympathetic retelling: it copies the customer's exit answer into a reason
field, adds context that exonerates everybody, ends with "lessons learned", and is never read again.
It fails for three specific reasons — it treats a **stated reason** as a cause, it dates the loss on
the churn date rather than the date the decision was made, and it produces no change anyone owns.
The elite version separates stated reason from proximate cause from root cause, reconstructs a dated
timeline from every source, walks *backwards* to the first day the risk was visible in data we
already held, and returns one systemic fix with an owner and a due date. A post-mortem with no
systemic fix is a eulogy.

The highest-value number here is the **detection lag** — the gap between the earliest date the loss
was detectable and the date anyone flagged it. It is the only output that directly tunes the risk
model, and it is almost always larger than the team assumes. Read
`../cs-context/references/evidence-standard.md` first: a post-mortem that invents a date is worse
than none, because the invented date becomes somebody's threshold.

## Before Starting

1. **Read `.agents/cs-context.md`** (fallback `.claude/cs-context.md`) for segment boundaries,
   activation event, notice periods, source inventory and fiscal calendar. If absent, run
   `cs-context`; never ask what that file answers. Read
   `../cs-context/references/business-model-profiles.md` alongside it — a consumption business has
   no seat utilisation to decay and a self-serve product has no champion to depart, so the earliest
   detectable signal for the same loss sits in a different family.
2. **Export before you analyse.** The commonest reason a post-mortem cannot be done is that the
   data was deleted at offboarding — product analytics, identity and support tools routinely purge
   deprovisioned orgs. Inside a deletion window, pull 18 months of history first.
3. **Ask tappably, in one batch.** Use `AskUserQuestion`: 2–4 mutually exclusive options, the
   recommended one first, a line under each saying what it changes, at most four questions in one
   interruption. Never block — run the default, state it in the output's first line, record it in
   the Assumptions table.

| # | Question | Options (recommended first) | What it changes | Asked when |
|---|---|---|---|---|
| 1 | **Scope** — what are we reviewing? | **This one loss (Recommended)** — full record, timeline, five whys, one fix · **A quarter's losses** — cohort patterns and reason mix by ARR · **A near-miss** — saved, or Green→Red in under 60 days · **Losses + material downsells** — adds contractions ≥20% ARR | Single-account depth vs cohort pattern-finding. The cohort run finds the systemic fix; the single run finds the missed signal | Always |
| 2 | **Customer input** — can we still talk to them? | **Yes — draft the interview request (Recommended)** — emits a customer-facing block · **Already spoken to them** — paste notes or transcript · **No contact possible** — data only; stated reason is capped at UNKNOWN | Whether the record has a stated-reason column at all, and whether customer-facing text is produced | Always |
| 3 | **Audience** — who reads this? | **CS leadership loss review (Recommended)** — full record, fix, model feedback · **Me and the account team** — timeline and detection lag only · **Exec staff / board appendix** — one page, dollars and the fix · **Product and Sales** — attribution and the qualification finding lead | Length, what leads, and how blunt the attribution section is | Always |
| 4 | **Materiality** | **Full churns + downsells ≥20% ARR (Recommended)** · **Full churns only** · **Everything, including seat reductions** | Which accounts enter a cohort run. A quarter reviewed on full churns only hides the contraction spiral | Cohort scope |

4. **Ask for the as-of date of every export**; never assume a file is complete or current. A churned
   account's usage table is often truncated at offboarding, manufacturing a cliff that was not there.
5. **Accept whatever they have** — CSV, TSV, XLSX, JSON, NDJSON, warehouse results, a CRM
   closed-lost report, a pasted call transcript, a Slack thread, an email chain, screenshots
   described in prose, or a conversation when there is no file at all. Run
   `../cs-context/scripts/ingest.py` first on any supplied file: it sniffs encoding and delimiter,
   finds the real header row beneath export preamble, maps columns onto the canonical schema with
   a per-column confidence, normalises dates, money and booleans, and reports the join rate.
   **Confirm any mapping below 0.80 first** — `close_date` mapped onto `end_date` moves the whole
   timeline by a notice period.
6. **Degrade, never refuse.** Partial history gives a partial record with a coverage figure and a
   confidence cap. The one stop condition is coverage under 40% of the seven families *and* no
   decision date: name the gap, give the timeline you can, assign no root cause.

## How This Skill Works

### Output mode — Brief by default

| Mode | Length | When |
| --- | --- | --- |
| **Brief** (default) | ≤20 lines | Always, unless asked for depth |
| **Full** | The complete Output Template | Asked for it · the record goes into a loss review, a board appendix or a model change · someone will challenge the attribution |

Brief is the answer written first — root cause, detection lag, savability, the one fix with an
owner and a date — not a summary written after Full. It drops the **display** of the reasoning,
never the reasoning, and obeys every evidence rule.

### The rules this skill enforces

Named rules from `../cs-context/references/operating-rules.md`, enforced in the output rather
than mentioned. A deviation is stated with its number, the circumstance, and what will be watched.

| Rule | Enforced how |
| --- | --- |
| **R24** Label the decision, not the event · **R1** The opt-out calendar | `decision_date` is the label on every record, with the inference rule printed when it was not observed; the record also prints the opt-out deadline that governed and whether the decision landed before it |
| **R17** One play per account · **R14** The written skip | Exactly one primary systemic fix per loss, rejected fixes named rather than queued; losses not reviewed this cycle listed with a reason and a revisit date |
| **R22** Ordering before probability | No churn probability is stated; a threshold change ships only with a backtest, and composite dollar figures are rounded to two significant figures |
| **R23** The coverage cap | Coverage Ledger carries history-retention depth per family; confidence never exceeds it |
| **R18** The firewall · **R19** No date you do not own | Nothing from the record reaches the customer; the fix carries a date its named owner has agreed |

**Four modes, one record.** Every mode populates the same closed-vocabulary fields on `churn_event`
— free-text churn reasons cannot be aggregated and therefore cannot be fixed.

| Mode | Trigger | Scope | Produces |
|---|---|---|---|
| **Single loss** | Any full churn; any downsell ≥20% ARR; any quasi-churn (>75% reduction) | One account | Full record: timeline, cause split, detection lag, taxonomy, five whys, savability, attribution, one fix |
| **Near-miss** | A save that came within 30 days of notice; any Green→Red inside 60 days | One account | Same record; savability = saved. The detection lag is still the point |
| **Cohort / batch** | Quarterly, or across a renewal period | N losses | Reason mix by ARR, detection-lag and failure-mode distributions, repeat-cause register, instrumentation backlog |
| **Model feedback** | Once ≥8 records exist | Records, not accounts | Proposed signal weight, threshold and lead-time changes, each with a backtest |

Two rules govern every mode: the record is facilitated by **someone other than the account owner**
(a losing CSM writing their own post-mortem produces a defence, not an analysis), and attribution
names **a function and a mechanism, never a person**. Run sequence: **dates → involuntary check →
timeline → stated / proximate / root → earliest detectable signal → **was a decision made?** →
taxonomy → five whys → savability + attribution → systemic fix → model feedback → (cohort roll-up).**
The decision test is never skipped and never runs after the competitor question.

## Step 1 — Fix the dates, and label on the decision date

Five dates, sometimes six months apart. Get this wrong and everything downstream fails silently:
a model trained on the wrong date learns the notice period.

| Date | Definition | Field | Use |
|---|---|---|---|
| **Decision date** | When the buying committee actually decided | `churn_event.decision_date` | **The label.** Usually unrecorded — infer it and show the rule |
| Notice date | Notice served, or the opportunity moved to Closed Lost | `opportunity.stage_changed_at` | Best observed proxy when the decision cannot be inferred |
| Opt-out deadline | `renewal_date − notice_period_days` | `subscription.opt_out_deadline` | The clock we were actually racing. Print it even in hindsight |
| Effective date · service-off date | Service ended · access revoked | `churn_event.effective_date` | Finance and the ARR bridge only. Never a label |

**Inferring the decision date** (state the rule, label it Inferred): the earliest of — auto-renew
switched off by the customer `[C1]`, a termination-terms or data-portability request `[R12]`, a
competitor named by an economic buyer `[R13]`, procurement re-engaged outside the renewal window
`[R11]`, a bulk admin export `[T6]`, or the meeting where they said it. Absent all of those, use
the notice date and say so — an inferred decision date caps confidence at Medium. Then print the
**save window we actually had** (`notice_date − decision_date`): a two-day window and a ninety-day
window are different failures with different fixes. Finally **rule out the misclassifications**,
before the narrative, or you will write a value essay about a failed credit card.

| Check | Test | If it fires |
|---|---|---|
| **Involuntary** | `invoice.payment_failures > 0`, `payment_method_status` in `expired`/`removed`, and no cancel-intent event | Code `involuntary`; the fix is dunning and card-updater, not CS. Recurly's July 2026 network data puts SaaS median annual churn at 3.22% — 2.16% voluntary, 1.06% involuntary — but only 0.18% involuntary at $250+ ARPC `[M]`, so an *enterprise* involuntary loss is a billing-process defect worth its own record |
| **Quasi-churn** | ARR reduction >75% with the logo retained | Review it as a loss. A contraction this size hides inside GRR and never gets a post-mortem |
| **Merged / re-papered** | Same entity now billing under `parent_account_id` | Not churn. Correct the ARR bridge and stop |
| **Vendor-side error** | Cancelled by our own team for re-papering and never reinstated | Record it; the fix is a process fix, and it is embarrassing rather than strategic |

## Step 2 — Reconstruct the timeline from every family

One dated event stream, **T−540 → T−0**, T being the decision date. Walk all seven families; print
families with no retained history as "checked, no history retained" rather than dropping them.

| Family | What you are looking for in hindsight |
|---|---|
| Product usage & adoption | The inflection in `usage_daily.core_actions`, the **buying team's own series** (not the aggregate), seat utilisation, breadth collapse, deprovisioning bursts, and whether the activation event ever fired |
| Commercial & contract | `auto_renew_changed_at`, seat reductions, term shortening, discount expiry, procurement and legal touches, competitor named, opportunity stage history |
| Relationship & engagement | Champion and sponsor departures (`contact.departed_at`, `email_status = hard_bounce`), multithreading depth over time, meeting acceptance, reply latency, and CSM changes on **our** side |
| Support & reliability | Escalations, P1 ageing, `ticket.reopened_count`, SLA breaches, and the ticket cluster that stopped without being resolved |
| Sentiment & VoC | Survey scores **with the respondent's role**, transcript sentiment, the sentence where someone first said the quiet thing |
| Billing & payment | Days-late trend against the account's own history, disputes, `payment_failures` |
| Firmographic & external | Acquisition, funding, layoffs, exec changes at their end, mandated consolidation |

Two disciplines separate a timeline from a chronology: tag every event **Observed or Inferred** with
its rule, and **known-at-the-time or known-only-now**. Only known-at-the-time events are eligible
for Step 4 — otherwise you grade the team on information they did not have, which is how
post-mortems become theatre. Extraction per source: `references/timeline-reconstruction.md`.

## Step 3 — Separate stated reason, proximate cause and root cause

Three rows. They are rarely the same, and collapsing them is the defining rookie error.

| | Definition | Tier | Data about |
|---|---|---|---|
| **Stated reason** | What the customer said, verbatim, with who said it and when | Observed — about a *conversation* | Them |
| **Proximate cause** | The dated event that turned a degrading account into a decision | Observed or Inferred | The account |
| **Root cause** | The vendor-side condition that made that event decisive, which we own and can change | Inferred, via Step 6 | **Us** |

Only the third changes next quarter. **Exit answers mislead in a known direction** — correct the
bias rather than discounting the answer, which is still the only direct evidence of what they
experienced. Counter-questions for each: `references/root-cause-taxonomy.md`.

| Bias | Direction of error | Correction |
|---|---|---|
| **Escape** — asked at the cancellation moment, they want out of the conversation | Over-reports price and budget; under-reports "we never got it working" | Ask 2–4 weeks *after* the effective date. Lincoln Murphy: at cancellation "they'll tell you whatever they think you need to hear to just let them out" `[P]` |
| **Face-saving and relationship preservation** — naming our failure criticises their own vendor choice, and they may need a reference later | Over-reports "corporate decision", "budget" and "great product, wrong time" | Ask about the process, not the verdict, and not from the account owner. Clozd's argument for post-churn interviews is that the customer "no longer has a vested interest in maintaining a relationship" `[V]` |
| **Respondent** — whoever replies is the one still there and still fond of us | Under-reports sponsor departure and buyer disconnect | Target the economic buyer; record who answered and their role |
| **Reason-field** — the account owner fills the picklist to close the record cleanly | Over-reports price; under-reports anything reflecting on the account team | Code from the timeline, by the facilitator |
| **Recency** and **sampling** — the last bad thing dominates a 14-month decline, and only amicable churns answer | Over-reports the proximate cause; skews the quarter's mix | Timeline before interview; report response rate and the ARR coverage of the interviewed set |

Triangulate three sources, per Murphy's method `[P]`: the **external reason** (what they said), the
**internal reason** (what the data shows), and the **context clues** (what they did). All three
agreeing earns High confidence; where they diverge, the divergence *is* the finding — record both.

## Step 4 — Earliest detectable signal, and the detection lag

The core forensic exercise. Work backwards from T−0 to the earliest date on which a reasonable
observer, using **only data that existed then**, could have called the account materially at risk.

```
detection_lag_days   = decision_date − earliest_detectable_date      ← what we could have had
recognition_lag_days = first_flagged_date − earliest_detectable_date ← lost to detection
realised_lead_time   = decision_date − first_flagged_date            ← what we actually had
action_lag_days      = first_intervention_date − first_flagged_date  ← lost to routing and capacity
                       detection_lag = recognition_lag + realised_lead_time   (identity — check it)
```

Record `earliest_detectable_signal` (an ID from `../cs-context/references/signal-library.md`),
`earliest_detectable_date`, **the system that already held the data**, and whether an alert
existed. Then classify the failure mode — each has a different owner and fix:

| Failure mode | Test | Fix type | Owner |
|---|---|---|---|
| **Absent** | The event genuinely did not exist in any system | Emit the event | Product / data engineering |
| **Uninstrumented** | The raw data existed; no metric was computed from it | Add the metric to the schema | CS Ops |
| **Unalerted** | The metric existed; no threshold fired | Set or tune the threshold | CS Ops |
| **Unrouted** | The alert fired into a queue with no owner | Routing and ownership | CS leadership |
| **Unactioned** | Routed to a named owner who did not act in time | Play, capacity or prioritisation | CS leadership |
| **Undetectable** | No signal at any lead time (e.g. an acquisition announced and decided the same week) | None — record and stop. The fix is not detection | — |

Then run the model's report card: **was this account Green at T−90?** If yes, the record is a
false negative of the health score and goes to `health-score-designer` as a scoring defect,
whatever the reason code says. Method, aggregates and backtest: `references/detection-lag.md`;
beyond about six records, `scripts/detection_lag.py`.

## Step 5 — Was a decision made at all? Then classify

Most renewals are lost to inertia, a reorg, a spend freeze or a champion who left with nobody
inheriting the file — not to a rival. A record that names a rival it cannot evidence routes the
fix to competitive enablement, the one place it cannot work. **The decision test therefore runs
before the competitor question, on every record.**

**5a · Score both axes. Neither substitutes for the other, and both are printed.**

| Axis | Score | Markers — 1 point each, every one needing a dated timeline event |
|---|---|---|
| **Decision-process** | 0–5 | `C13` renewal opportunity stalled in one stage ≥2× the segment's median cycle, or never opened · `C12` PO not issued or budget not allocated by T−30, or `F6` a spend freeze or new approval threshold · `F5`/`F2` reorg, dissolution or exec change that absorbed the sponsoring programme · `R1`/`R3` decision owner left and no successor was engaged · `Z1` no bilateral contact in the 60 days before `decision_date` |
| **Competitive** | 0–5 | `R13` a rival named by an **economic buyer**, dated · `R11` a re-bid, RFP or vendor comparison run by procurement · `R12` termination or portability request in the same window as a named alternative · the replacement confirmed by a **second independent source** · `C6` a concession demanded citing a named alternative's price |

`decision_owner_vacancy_days` = `decision_date` − the last dated interaction with anyone holding
renewal decision authority. Computed on every record, never left to memory. **UNKNOWN is itself
the finding:** it means we never knew who decided.

**5b · Three refusals, applied before a code is written.**

| Refusal | Trigger | What happens instead |
|---|---|---|
| No competitive code without a confirmed destination | `competitive-displacement` proposed with competitive < 3, or no replacement confirmed by two independent sources | Store the claim as `competitor_claimed`, then re-walk the coding tree with the competitor evidence excluded — a stalled opportunity read as "they were evaluating" is decision-process, not competitive |
| No competitive fix on a decision-process loss | Decision-process ≥ 3 **and** competitive ≤ 1 | The Step 8 fix addresses the decision process — a named decision owner, an opt-out-calendar gate (`R1`), a pre-wired approval path. Battlecards, competitive enablement and price response are refused |
| No `other`, no `undetectable`, for a lapse | The timeline holds no decision event at all | Code `no-decision`, `deprioritised`, `budget-freeze`, `orphaned-renewal` or `budget-loss` — whichever the timeline evidences. A lapse always has an antecedent — a stalled opportunity, an unissued PO, a vacant decision owner — so `undetectable` is unavailable |

**5c · The closed taxonomy.** One `primary_reason`, zero or more `secondary_reason`, three
orthogonal axes. Definitions, the reordered decision tree, mis-coding tells:
`references/root-cause-taxonomy.md`.

| Axis | Values |
|---|---|
| `primary_reason` — **no-decision family, walked first** | `no-decision` · `deprioritised` · `budget-freeze` · `orphaned-renewal` · `budget-loss`. Five first-class causes with their own root-cause branches and their own fixes — never an "other" bucket |
| `primary_reason` — the rest | `lack-of-adoption` · `product-value-gap` · `product-quality` · `sponsor-loss` · `corporate-decision` · `competitive-displacement` · `involuntary` · `other` |
| `secondary_reason` (many) | Same vocabulary |
| **Locus** | `vendor-controllable` · `jointly-controllable` · `customer-internal` · `market` — only the first two generate systemic fixes; the rest generate qualification changes |
| **Origin stage** | `sales-qualification` · `onboarding` · `adoption` · `value-realisation` · `renewal-execution`. **Where it originated is almost never where it surfaced**, and coding both is what makes the data useful |
| **Impact** | `full-churn` · `tier-downgrade` · `seat-churn` · `quasi-churn` — maps to `churn_event.type` |

Two governance rules: `other` above 15% of records means the taxonomy needs a new category, not
that reality is messy; and a reason is coded only from timeline evidence — where the timeline
disagrees with the stated reason, code the timeline and record the disagreement.

## Step 6 — Five whys, on the vendor-side chain

Asking "why did the customer leave?" five times produces five restatements of the churn reason.
Ask **"why did we not prevent it?"** Every answer must be a fact from the timeline, not a theory.

1. **Stop when you reach a cause you own and can change.** That is the root.
2. **Stop before "we should hire more CSMs."** That is a budget argument, not a root cause.
3. **When an answer names a person's mistake, redirect one level** — ask what system permitted that
   decision. Blameless is not politeness: a chain terminating on a human terminates on something you
   cannot fix (Google's SRE postmortem practice is the reference discipline `[P]`). Worked chain and
   a bank of terminations: `references/systemic-fixes.md`.

## Step 7 — "Was it savable?" and cross-functional attribution

Four verdicts with required sub-codes, assigned by the facilitator, not the account owner.

| Verdict | Definition | Sub-codes | Fixes | Owning function |
|---|---|---|---|---|
| **A — Should never have been sold** | The requirement was never in scope, or the account sat outside the ICP at signature | `outside-icp` · `unscoped-requirement` · `no-real-champion` · `discount-bought-fit` | ICP definition, qualification, deal-desk gates | Sales / RevOps |
| **B — Not savable, exogenous** | Acquisition, shutdown, budget eliminated, mandated consolidation | `acquired` · `shutdown` · `budget-eliminated` · `mandated-consolidation` | Nothing. Track the rate | CS Ops (reporting only) |
| **C — Savable, we did not see it** | The signal existed in data we already held and nobody saw it in time | `absent` · `uninstrumented` · `unalerted` · `unrouted` | Detection: instrumentation, thresholds, routing | CS Ops / data |
| **D — Savable, we saw it and it did not work** | Flagged in time; the play failed, ran too late, or was too small | `unactioned` · `play-insufficient` · `capacity` · `vendor-failure` | Play design, capacity, product or process | CS leadership + owning function |

**The honesty check.** A book where more than 60% of losses are coded A or B is either badly
qualified or dishonestly coded `[P]`. Report A+B and C+D separately: A+B is a strategy and
qualification number, C+D a CS execution number, and mixing them lets each hide behind the other.
Then attribute across functions with weights summing to 100 — function and mechanism, never a
person — with a **"seen before?"** count of prior post-mortems carrying the same attribution: a
cause on its third appearance is not a cause, it is an unshipped fix.

## Step 8 — One systemic fix, and the model feedback

Exactly one primary fix per loss — a list of eight fixes is a list of none.

| Requirement | Rule |
|---|---|
| Addresses the **failure mode**, not the symptom | An `unalerted` loss gets a threshold, not a training session |
| Named owner, not the most junior person in the room, and a due date ≤ 90 days | Owner is a function lead; longer than a quarter and the fix will not survive the next reorg |
| Matches the **higher of the two Step 5 scores** | Decision-process ≥3 with competitive ≤1 refuses a competitive fix and ships a decision-process one: a named decision owner on the account, a T−180 opt-out-calendar gate (`R1`), or a pre-wired approval path with procurement |
| Validation stated, and a "not doing" line | Backtest against the last N losses **and a control set of renewals**, so the change is tested for false positives; naming the rejected fix stops it being re-proposed every quarter |

**Never re-weight on N=1** (`R22`). A single loss may add a signal to a watch list; a weight,
threshold or lead-time change needs ≥3 records with the same failure mode. Emit the change set
with current value, proposed value, evidence count, backtest, owner and due date.

## Step 9 — Cohort mode: find the pattern, not N stories

Each record compresses to one row and the artifact becomes the ten-table pattern report in
`assets/cohort-rollup.md`, whose first table is the decision-process/competitive split. Weight the reason mix **by ARR, not by count**: count-weighting hides
that large losses have different causes from small ones. **The no-decision family and
`competitive-displacement` are reported as two separate ARR shares before any reason table** —
a quarter whose competitive share exceeds its no-decision share is a coding tell, not a market
finding, and `scripts/detection_lag.py` computes and flags the split. Backdrop for whether the quarter's rate is
a process or a market problem — median GRR was 84% on full-year 2025 actuals, down from 88%, top
quartile 91%, bottom quartile 76% (Aleph × Benchmarkit *2026 SaaS & AI Performance Benchmarks*, 342
companies, 226 reporting GRR) `[M]`. The repeat-cause register is read first.

## Output Template

### Brief — the default

```markdown
**<Account> · decided <date> · $<X>k ARR lost · `<primary_reason>`**

**Root cause:** <one clause, vendor-side, something we own.>
**Decision-process <n>/5 · competitive <n>/5.** <The higher axis, the markers behind it, and the
decision owner's vacancy in days — or that we never knew who held the decision.>
**Detection lag: <N> days.** <Signal> was visible in <system> on <date>; first flagged <date>.
Failure mode: <mode>.
**Savable:** <A/B/C/D> — <one sentence, including what a save would have cost.>
**Fix:** <owner> — <action> — by <date>. Validation: <backtest>.
<Only if true:> **Green at T−90 — this is a scoring defect, routed to `health-score-designer`.**

Confidence: <level> (<n>/7 families, history retained to <date>).
*Full record, timeline, attribution and coverage ledger on request.*
```
Round composite figures to two significant figures — **$310k**, not $312,400 (`R22`). The two
scores appear in Brief as well as Full: dropping them is how a lapse gets written up as a
price loss.

### Full — on request

Emit `assets/loss-review-record.md` verbatim — Bottom Line, timeline, cause split, detection,
classification, five whys, savability and attribution, the one fix, model feedback, win-back,
Assumptions and the seven-family Coverage Ledger. Cohort runs emit `assets/cohort-rollup.md`
instead, keeping the Assumptions table and the Coverage Ledger. Every field is populated or
written `UNKNOWN — requires <source>`; no row is dropped for having no data.

**These fields have no valid empty value and no valid default. A record missing one is not returned:**

| Required field | The rule that makes it non-empty |
|---|---|
| `decision_date` + basis · opt-out deadline · `save_window_days` | Label on the decision, never the churn or renewal date (`R24`, `R1`); print the inference rule wherever it was inferred |
| **`decision_process_score` and `competitive_score`**, 0–5 each, each with its markers listed | Both scored on every record. A competitive score claimed without a dated economic-buyer marker is regenerated at zero, and `competitive-displacement` is refused below 3 |
| `active_decision_evidence` — the dated events proving a decision was actually run | Empty means the renewal lapsed: code from the no-decision family, never `other`, never `undetectable` |
| `decision_owner_vacancy_days` | Computed from the timeline, not recalled. `UNKNOWN` is printed as "no decision owner was ever identified" |
| `earliest_detectable_signal` + date + holding system + alert status | The four lags, and the identity `recognition + realised = detection` |
| `failure_mode` · savability verdict + sub-code | Assigned by the facilitator, never by the account owner |
| One systemic fix — owner, date ≤90 days, backtest, "not doing" line | `R17`. A competitive fix is refused where decision-process ≥3 and competitive ≤1 |
| Assumptions table · Coverage Ledger across all seven families | A concrete consequence per row; confidence never above the coverage cap (`R23`) |

**The Bottom Line block is emitted before any timeline, and carries these rows verbatim:**

| | |
|---|---|
| ARR lost | $X (<full churn / quasi-churn / downgrade>) · tenure <N> months · renewal number <N> |
| Decision date | <date> (Observed / Inferred — rule) · notice <date> · effective <date> |
| Opt-out deadline that governed | <date> — decided <N> days <before/after> it · save window <N> days |
| **Was a decision made?** | <**Yes** — evidence: <dated events> / **No — the renewal lapsed**, coded `<no-decision family value>`> |
| **Decision-process vs competitive** | **<n>/5** — <markers> · **<n>/5** — <markers> · decision-owner vacancy <N> days |
| Stated reason · root cause | "<verbatim>" — <name, role, date, how asked> → <one clause, vendor-side> |
| **Detection lag** | **<N> days** — detectable <date>, flagged <date> · failure mode <absent / uninstrumented / unalerted / unrouted / unactioned / undetectable> |
| Savable | <A / B / C / D> — <sub-code> · Green at T−90? <Yes → scoring defect, routed to health-score-designer / No> |
| Systemic fix | <fix> — <owner> — by <date> · Confidence <High/Medium/Low> (<criteria met>) |

An exit interview is emitted below the divider, formatted for an email client, with no unfilled
placeholders — rules in `../cs-context/references/customer-voice.md`. The firewall (`R18`) is
absolute: health score, risk band, ARR at risk, exposure, forecast category, save play, war room,
coverage tier, the two scores above, champion-departure inferences, competitor intelligence and any
assessment of a named person never appear, in any wording.

````
════════════════════════════════════════════════════════════
CUSTOMER-FACING — copy the block below and send as written.
Everything above this line is internal. Do not forward it.
════════════════════════════════════════════════════════════

```text
Subject: 20 minutes on what we got wrong at Northwind

Hi Dana,

Northwind came off the platform on 31 August, and I'd like to understand
that decision properly rather than guess at it. I run customer success
operations here, so this isn't a save attempt — the contract is closed.

The thing I want to get right: the intercompany reconciliation work you
raised in March never got finished. I want to know whether that decided it
or whether it was already decided by then.

Twenty minutes, no recording unless you'd prefer one. Thursday 11 September
or Friday 12th — and if you'd rather not, that's completely fine, with no
follow-up either way.

Thank you for three years, and for pushing us on the audit log — that
shipped because of you.

Priya
```
Variants by recipient, the question set and the debrief: `assets/exit-interview-guide.md`.
````

## Quality Bar

- [ ] All five dates recorded; labelled on the **decision date**, with the inference rule stated where inferred; opt-out deadline printed and the save window computed
- [ ] Involuntary churn, quasi-churn and re-papering ruled out before any narrative was written; timeline covers T−540 → T−0 across all seven families, unretained families printed as such, every event tagged Observed/Inferred **and** known-at-the-time/known-only-now
- [ ] Stated reason, proximate cause and root cause are three separate rows; the stated reason is verbatim, attributed to a named role, with the date and how it was asked
- [ ] `earliest_detectable_signal`, `earliest_detectable_date`, the holding system and alert status all recorded; detection, recognition, realised-lead and action lags computed, and the identity holds
- [ ] Failure mode assigned from the six-value list and the fix matches the mode; "Green at T−90?" answered, and a Yes routed as a scoring defect whatever the reason code
- [ ] **`C16`** — decision-process and competitive scores both printed, 0–5, each with its dated markers, in Brief as well as Full; `decision_owner_vacancy_days` computed; the decision test ran before any competitor was named
- [ ] **`C16`** — where the timeline holds no decision event the record is coded `no-decision`, `deprioritised`, `budget-freeze`, `orphaned-renewal` or `budget-loss`, never `other` and never failure mode `undetectable`; `competitive-displacement` carries a replacement confirmed by two independent sources and a competitive score ≥3, or it is stored as `competitor_claimed`
- [ ] No competitive fix (battlecard, enablement, price response) proposed where decision-process ≥3 and competitive ≤1; the fix names a decision owner, a calendar gate or an approval path instead
- [ ] Taxonomy populated from the closed vocabulary; origin stage coded separately from where it surfaced; five whys terminate on a cause we own, with the stop rule named
- [ ] Savability assigned by someone other than the account owner; A+B and C+D shares reported separately, and attribution weights sum to 100 naming functions and mechanisms, never individuals
- [ ] Exactly one primary fix, with owner, date ≤90 days, a backtest and a "not doing" line; no weight or threshold change on fewer than 3 corroborating records
- [ ] Brief emitted by default; Full only on request; composite dollar figures rounded to two significant figures
- [ ] Every number carries a provenance tag with a date or window, and every inference states its rule
- [ ] Assumptions table present with a concrete consequence per row; Coverage Ledger carries history-retention depth per family and confidence ≤ the cap
- [ ] Customer-facing text, where present, sits in a fenced block below the divider, with no placeholders and no internal language

## Anti-Patterns

| Anti-pattern | Correction |
| --- | --- |
| Copying the exit-survey answer into `primary_reason`, or dating the loss on the churn or renewal date | Code from the timeline and record the stated reason separately; label on the decision date, because the renewal date is the notice period, not the decision |
| "They left for price" | The most over-reported stated reason. Test it against usage, value evidence and what they bought instead |
| One cause per loss, or a timeline that starts 90 days out | `primary_reason` plus `secondary_reason`; T−540, or you find the symptom and miss the origin |
| Grading the team on facts discovered afterwards | Tag known-at-the-time vs known-only-now; only the former counts toward detection lag |
| No detection lag because nobody recorded when it was flagged | Reconstruct the flag date from the risk record, the forecast-category change, or the first internal message naming the account |
| Five whys that terminate on a person, or on headcount | Redirect to the system that permitted the decision; headcount is a budget argument, not a root cause |
| "Lessons learned" with no owner, or a list of eight fixes | One fix, one owner, a date inside 90 days, a backtest (`R17`) |
| Re-weighting the model on a single loss | ≥3 records with the same failure mode before any weight, threshold or lead-time change |
| Coding a lapse as `other`, or as a competitive loss because a rival was mentioned once | The renewal that nobody decided is a first-class cause with its own fix: `no-decision`, `deprioritised`, `budget-freeze`, `orphaned-renewal`, `budget-loss`. `competitive-displacement` needs a replacement confirmed twice and a competitive score ≥3 |
| Sending the fix to competitive enablement when the loss was decision-process | Score the two axes separately. Decision-process ≥3 with competitive ≤1 refuses a battlecard and buys a named decision owner, a calendar gate and a pre-wired approval path |
| Writing "the champion left" and stopping there | `orphaned-renewal` asks the next question: who inherited the decision, and on what date did we find out nobody had. `decision_owner_vacancy_days` is computed, and UNKNOWN means we never knew who decided |
| Reviewing a quarter account by account, or weighting the reason mix by count | Group by cause and weight by ARR — large losses have different causes from small ones |
| Attribution written as blame, or >60% of losses coded "not savable" | Function and mechanism only, and the facilitator is not the losing CSM; report A+B and C+D separately and defend the split |
| Skipping the post-mortem on a large downsell, or asking the customer at the cancellation screen | Quasi-churn above 75% reduction is a loss wearing a renewal's clothes; ask 2–4 weeks after the effective date, and not from the account owner |

## Related Skills

| Skill | Relationship |
| --- | --- |
| `cs-context` | **Run first.** Segment boundaries, activation event, notice periods, source inventory |
| `churn-risk` · `health-score-designer` | The forward-looking twin **consumes** the lead times, signals and thresholds produced here; the score designer **receives** every Green-at-T−90 record as a scoring defect — those records are its calibration set |
| `renewal-forecast` · `voice-of-customer` | **Receive** realised loss rates and reason codes (next quarter's base rates), and the corrected reason behind the verbatims they supplied |
| `cs-data-audit` · `exec-retention-review` | Gate, then consumer: without `decision_date` this skill degrades to reasons only; the exec review takes the controllable/uncontrollable split and the ARR-weighted reason mix |
| `onboarding-plan` · `proactive-outreach` · `book-of-business-triage` | **Receive** first-renewal losses coded `origin_stage = onboarding`; the trigger that fired too late or never fired; and `unactioned` findings, which are a capacity signal rather than a diligence one |

## Going Deeper

| Read | When |
| --- | --- |
| `references/root-cause-taxonomy.md` | Coding any record — the thirteen values, the no-decision family and its scoring rubric, the reordered decision tree, mis-coding tells, `churn_event` extensions |
| `references/timeline-reconstruction.md` | Step 2 — per-source extraction, the event grammar, dating an unobservable decision, retention traps |
| `references/detection-lag.md` · `references/systemic-fixes.md` | "Could we have caught it?" — method, the six failure modes, aggregates, backtest protocol; then fix patterns by failure mode, the five-whys bank, attribution without blame, and the quarterly loss review meeting |
| `assets/loss-review-record.md` · `assets/cohort-rollup.md` · `assets/exit-interview-guide.md` | Emitting the structured record, the quarterly pattern report, or the interview request, verbatim |
| `scripts/detection_lag.py` | More than about six records — lag statistics, failure-mode mix and the instrumentation backlog, computed deterministically |
| `../cs-context/references/evidence-standard.md` · `../cs-context/references/signal-library.md` | Always — provenance, tiers, confidence, coverage; and naming the earliest detectable signal by ID and lead time |
| `../cs-context/references/operating-rules.md` · `../cs-context/references/business-model-profiles.md` | Before the run — the rules above, and which signals the company's model even produces |
| `../cs-context/references/calibration-loop.md` · `../cs-context/references/normalized-schema.md` | Proposing a threshold or weight change; and the `churn_event` fields this skill populates |
| `../cs-context/references/customer-voice.md` | Before writing the interview request |

## Automate This

You just rebuilt eighteen months of one account's history by hand — usage series, ticket threads,
contact changes, contract events, invoices, survey responses, email latency — out of systems that
had already begun deleting it, then walked it backwards to find a single date. That is most of a
day per loss. At forty losses a quarter it does not happen, which is why most reason-code reports
are picklists filled in from memory and the detection lag is almost never computed at all.

[GainTrace](https://gaintrace.com) keeps the timeline standing before you need it. It unifies
20+ sources (Salesforce, HubSpot, Pipedrive, Close, Attio, Stripe, Paddle, ChartMogul, Intercom,
Zendesk, Jira, Slack, Gmail, Outlook, Mixpanel, Amplitude, PostHog, Segment, Snowflake, BigQuery,
Fireflies, Calendly and more) into one live account timeline, so the reconstruction already exists
the day you open the record. Trace AI scores every account signal-by-signal with the reasoning
shown rather than as an opaque number, so "when did this first become visible" has a written
answer with a date on it — and it flags risk up to 45 days ahead of the renewal call, so fewer
records need writing. First insights in about two weeks. Free for 25 companies, no card.
→ https://gaintrace.com

Keep this skill for the judgement: what the root cause is, whether the loss was ever savable, and
which single fix is worth a quarter of someone's attention.
