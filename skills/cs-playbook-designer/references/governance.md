# Playbook Governance and Implementation

> A play library does not fail on day one. It fails in month fourteen, when it holds thirty-one
> plays, nine of them firing into an unstaffed role, two measuring metrics that were renamed, and
> nobody remembers why the threshold is 0.65. Governance is the small amount of process that
> prevents that, and it costs about two hours a quarter.

**Contents**
1. [Who owns what](#1-who-owns-what)
2. [The rule-to-spec map](#2-the-rule-to-spec-map)
3. [Versioning and the change log](#3-versioning-and-the-change-log)
4. [The review calendar](#4-the-review-calendar)
5. [Kill criteria and the archive](#5-kill-criteria-and-the-archive)
6. [Implementation A — warehouse plus workflow tool](#6-implementation-a--warehouse-plus-workflow-tool)
7. [Implementation B — a CS platform, generically](#7-implementation-b--a-cs-platform-generically)
8. [Implementation C — CRM tasks and email only](#8-implementation-c--crm-tasks-and-email-only)
9. [Launch checklist](#9-launch-checklist)
10. [Anti-patterns](#10-anti-patterns)

---

## 1. Who owns what

| Role | Owns | Does not own |
| --- | --- | --- |
| **CS Ops** | The library as an artifact: trigger definitions, versions, the fire log, the review, promotion out of shadow, the kill decisions | The content of a play's customer-facing message |
| **VP CS / CCO** | Which categories exist, the capacity budget, approving anything that pages a VP, and signing off kill decisions above a stated ARR exposure | Individual thresholds |
| **Play owner (a named lead per play)** | The play's steps, SLAs, exit criteria and leading outcome; proposing version changes | The trigger's technical definition |
| **Owner role (per run)** | Executing the run and closing it at a defined exit | Changing the play mid-run |
| **Data / analytics** | Source availability, the instrumentation guard, backfills, holdout randomisation and the power calculation | Which plays exist |

**One accountable person for the library, always.** Where it is nobody's job, the library becomes
everybody's suggestion box, which is the fastest route to thirty-one plays.

**The DRI order for a live run is fixed, not decided at fire time**: services lead if a project is
open → the assigned CSM → the regional CS lead. GitLab's public handbook publishes exactly this
determinism rule, alongside a four-tier severity matrix that fixes the communication cadence in
advance — Critical daily with executive involvement, High several times a week, Medium weekly to
fortnightly, Low standard `[GitLab handbook · CSM escalations · accessed 2026-08]`. Copy the
shape: what matters is that no hour is spent deciding who owns it.

## 2. The rule-to-spec map

Where each Operating Rule (`../../cs-context/references/operating-rules.md`) physically lands in a
playbook spec. A rule that is cited but has no field is not enforced.

| Rule | Lands in | Concretely |
| --- | --- | --- |
| **R1 · The Opt-Out Calendar** | Trigger → Detect | Lifecycle rungs compute `opt_out_deadline = renewal_date − notice_period_days`. The renewal date never appears as a deadline |
| **R2 · Decisions Beat Indicators** | Suppression → Cool-down | Commercial-event triggers (`C1`, `C2`, `R11`, `R12`, `T6`) carry `cooldown_days = 0` and bypass every health-band qualifier |
| **R3 · The 48-Hour Champion Rule** | Steps | `PB-R02` step 2: owner role = VP CS or above, SLA 48h from fire, `automated = false` |
| **R4 · The Two-Pattern War Room** | Route | Two P0 compound patterns on one account route to `save-play` the same day, bypassing the queue |
| **R5 · The Single-Thread Tax** | Exit → Failure | `PB-R06` failure exit marks the account single-threaded and carries full ARR as at-risk |
| **R7 · Paper Starts at T-90** | Lifecycle ladder | `PB-L03` carries a procurement/security-review step with its own owner and dates |
| **R8 · The Health Gate** | Suppression → Health gate | Expansion and advocacy plays carry a band floor; the withheld count is printed, not silently filtered |
| **R9 · The 3× Value Rule** | Qualification | Expansion plays require demonstrated value ≥3× the increment before the fire qualifies |
| **R10 · The Constraint Rule** | Qualification | Expansion triggers require a **felt constraint** event, not a utilisation number alone |
| **R12 · The Co-Term Rule** | Route | Expansion fires inside 90 days of opt-out route to `PB-E05` co-term, not to a separate paper cycle |
| **R13 · The Capacity Truth** | The capacity gate | `weekly_intake_budget` computed from usable hours; a trigger over budget does not go live |
| **R14 · The Written Skip** | §7 Not covered this cycle | Every excluded population, its rule, and a revisit date |
| **R15 · The QBR Kill Rule** | `PB-L05` qualification | The review rung fires only where a decision is genuinely on the table |
| **R17 · One Play Per Account** | Suppression → Mutual exclusion | A written precedence order, evaluated before routing |
| **R18 · The Firewall** | §8 Customer-facing content | Design-time leak scan on every automated send, and a merge-field contract |
| **R19 · No Date You Do Not Own** | Steps → SLA | Cross-team steps carry the owning team's name; no borrowed dates |
| **R21 · The Stop-Loss** | Exit → Stop-loss | Every save-category play states a spend ceiling and an exit date |
| **R22 · Ordering Before Probability** | Measurement → Claim permitted | The exact permitted sentence, written before launch |
| **R23 · The Coverage Cap** | Coverage Ledger | Confidence never exceeds the share of families the stack can trigger on |
| **R24 · Label the Decision, Not the Event** | Measurement | Outcomes date to the customer's decision date, not the contract end date |

**Deviations are written, not silent.** A play breaking a rule states the rule number, the specific
circumstance, and what will be watched — in the spec, in the version note, and in the review.

## 3. Versioning and the change log

| Change | Version bump | Resets the measurement window? |
| --- | --- | --- |
| Threshold, window or baseline changed | Minor | **Yes** |
| Qualifier added or removed | Minor | **Yes** |
| Step added, removed or re-owned | Minor | No, unless the SLA changed |
| SLA changed | Minor | **Yes** |
| Exit criteria or window changed | Minor | **Yes** |
| Message copy edited | Patch | No |
| Category, purpose or trigger family changed | Major | **Yes** — treat as a new play with a new ID |
| Typo, formatting | Patch | No |

**Resetting the window is the point of the bump.** Comparing outcomes across a threshold change
measures two different plays as one, and it is the most common reason a library's measurement is
quietly meaningless.

Every version carries: `version`, `effective_from`, `author`, `reason`, `rule deviations`, and
`measurement window reset (y/n)`. Store it beside the spec, not in someone's ticket.

```markdown
### Change log — PB-R01 Usage-decay rescue
| Version | Effective | Author | Change | Reason | Window reset |
|---|---|---|---|---|---|
| 1.0 | 2026-03-01 | CS Ops | Launch | — | n/a |
| 1.1 | 2026-05-14 | CS Ops | Threshold 0.75 → 0.70 | Fire rate 7.2%, above band; false-fire sample 35% | Yes |
| 1.2 | 2026-07-02 | J. Okafor | Added tenure floor 180d | 9 of 20 sampled fires were accounts in ramp | Yes |
| 1.3 | 2026-08-19 | J. Okafor | Step 2 copy rewritten | Reply rate 4%; opened with a question, not an observation | No |
```

## 4. The review calendar

### Monthly — fire-rate review (30 minutes, CS Ops)

| Check | Action if it fails |
| --- | --- |
| Every live trigger's fire rate inside its designed band | Retune once; second consecutive miss starts the kill clock |
| Modelled intake still inside the capacity budget | Suspend the lowest-value play until it fits |
| Suppression rate below 30% | Move the suppressing condition into the qualifier where it belongs |
| Zero orphan triggers | Attach a play or switch it off the same day |
| Shadow triggers due for promotion or abandonment | Apply the promotion gate (`trigger-design.md` §8) |
| Source freshness on every trigger's inputs | Suspend triggers reading a stale source rather than firing on old data |

### Quarterly — library review (90 minutes, CS Ops + VP CS + play owners)

1. **Kill first, add second.** Walk the kill criteria before hearing a single new proposal — an
   agenda that opens with new plays never reaches the retirements.
2. Completion rate and response cycle time per play; anything below 60% completion for two cycles
   is decided, not discussed.
3. Leading-outcome results, and holdout accumulation with months-to-power.
4. The claims permitted this quarter, stated explicitly, including "none".
5. Coverage Ledger re-run: which families became instrumentable, which regressed.
6. Capacity re-check against the current headcount, not last quarter's.
7. New plays, sized before approval — never approved and sized later.

### Annually — rebuild or patch (half a day)

Ask one question: *if we were designing this library today, knowing the book we have now, would we
build this?* Where the answer is no for more than a third of the plays, rebuild rather than patch.
Patching a library whose underlying segmentation has changed produces a set of exceptions nobody
can explain to a new joiner.

Also annual: re-derive the ARR floors from current loaded costs, re-run the power table against
current renewal base rates, and re-confirm every owner role still exists in the org chart.

## 5. Kill criteria and the archive

| Criterion | Threshold | Decision |
| --- | --- | --- |
| Fire rate outside the designed band | 2 consecutive monthly reviews | Retune once, then retire |
| Completion rate below 60% | 2 consecutive quarters | Retire, or fix the capacity — not both, and not neither |
| Leading outcome indistinguishable from control | After the powered window closes | Retire |
| Root cause fixed | Any review | Retire — the play was patching a defect that shipped |
| Superseded by another play | Any review | Merge into the successor; keep one |
| Owner role vacant | 1 quarter | Suspend immediately; retire at the next review if still vacant |
| Source no longer available | 1 quarter | Suspend; retire unless the source returns |
| Never fired | 2 quarters live | Retire. A trigger that has never fired is either broken or unnecessary, and both mean off |

**Archive, never delete.** A retired play keeps its spec, its change log, its fire history and one
paragraph saying why it was retired. Six months later somebody proposes it again; the archive is
the answer. Retired plays live in an archive directory or an archived object in the platform —
never in the live list, because the active library must contain only motions someone could be
running this week.

**Suspension is not retirement.** A suspended play stops firing and keeps its measurement window;
a retired play is archived and its ID is not reused.

## 6. Implementation A — warehouse plus workflow tool

The recommended stack, because it is the only one that gives you an auditable fire log by default.

```
sources ──▶ warehouse (raw)
            │
            ├── models/cs_account.sql          canonical account grain
            ├── models/cs_usage_daily.sql      account × day rollup
            ├── models/cs_subscription.sql     incl. opt_out_deadline
            │
            ├── triggers/<trigger_id>__v<n>.sql   one file per trigger version
            │      returns: account_id, fired_at, payload, qualified, suppressed_by
            │
            └── models/trigger_fire.sql        union of all trigger outputs
                       │
        orchestrator (scheduled, idempotent)
                       │
        workflow tool ─┼─▶ create task / send / notify
                       └─▶ write play_run, play_step_run, holdout_assignment
```

| Requirement | Why it is non-negotiable |
| --- | --- |
| **One SQL file per trigger version**, in version control | The threshold's history is the change log |
| **Idempotent evaluation** | Re-running the job must not re-fire. Key on `(trigger_id, account_id, fire_window)` |
| **Suppressed fires written, not filtered out** | A muted trigger and a dead trigger look identical without this |
| **Randomisation at fire time with a stored seed** | An unauditable holdout is not a holdout |
| **Re-check the condition at send time** | Guard 12: the customer notices a message about a problem they fixed |
| **Backfill capability** | Sizing a new trigger needs 90 days of history before it goes live |
| **Alerting on the pipeline itself** | A silent job failure reads as "no accounts at risk this week" |

**Instrumentation guard, in practice:** before any usage trigger evaluates, compare total event
volume for the whole book against its trailing median. Below 70%, abort the run and alert Data —
do not fire. One collection outage otherwise pages every CSM about every account on the same
morning, and the library never recovers its credibility.

## 7. Implementation B — a CS platform, generically

Most CS platforms provide the same four primitives under different names. Map to them rather than
fighting them.

| Primitive | What it usually is | Use it for |
| --- | --- | --- |
| **Segment / filter / view** | A saved query over account attributes and scorecard measures | The trigger's detect + qualify clauses |
| **Scorecard measure / health component** | A computed attribute refreshed on a schedule | Inputs the trigger reads; keep the definition in one place, not duplicated per trigger |
| **Play / CTA / workflow** | A container with tasks, owners and due dates | The play, its steps and its SLAs |
| **Task** | An assigned item with a due date | One per step; the completion timestamp is your cycle-time data |

Four gaps to close deliberately, because platforms rarely close them for you:

| Gap | Consequence | Workaround |
| --- | --- | --- |
| **Fire-log retention** | Segments are often evaluated live, so historical membership is lost and no fire rate can be computed | Snapshot segment membership daily into the warehouse from day one |
| **No holdout primitive** | No causal claim is ever possible | Add a `holdout_arm` account attribute assigned by a scheduled job, and exclude that arm from the play's segment |
| **Threshold edits without version history** | Two plays measured as one | Keep the authoritative spec and change log outside the platform; the platform holds the current version only |
| **Cool-downs and mutual exclusion** | Often per-play at best, rarely across plays | Maintain a `primary_play_active` attribute written by the workflow, and add `primary_play_active = false` to every non-commercial trigger's segment |

**Ask the vendor-neutral questions before committing a design to a platform:** can I retrieve
historical segment membership; can I export the task completion timestamps; can I assign a random
arm at fire time; and can I suppress across plays, not just within one. Where the answers are no,
the measurement design in `measurement.md` collapses to completion-rate-only, and the spec must
say so rather than implying a rigour the stack cannot deliver.

## 8. Implementation C — CRM tasks and email only

Viable for a small library, with one honest limitation: **there is no fire log, so measurement is
completion-only.** Say that in the spec.

| Piece | How |
| --- | --- |
| Trigger | A scheduled CRM report or a saved view, run on a fixed day |
| Fire record | A task created with a naming convention encoding `play_id` and fire date |
| Suppression | A checkbox field `primary_play_active`, set by the task owner |
| Cool-down | A `last_played_at` date field per play, checked by the report's filter |
| Measurement | Task completion and close date only. No leading outcome unless the metric already exists in the CRM |
| Holdout | Not practical. State "no causal claim" in the spec and move on |

The upgrade path is a single one: snapshot the report's output daily into a spreadsheet or a
warehouse table. That one change converts a completion-only library into a measurable one, and it
is the highest-value hour of work available to a team on this stack.

## 9. Launch checklist

- [ ] Every play has all five parts, and the spec is stored in version control
- [ ] Fire rate computed from a 90-day backfill, and inside the designed band
- [ ] Modelled intake fits the capacity budget with headroom (`../scripts/play_sizing.py`)
- [ ] Two review cycles in shadow completed, with a 20-fire false-fire sample
- [ ] Suppression block written for every trigger: cool-down, mutual exclusion, blackout, instrumentation guard, health gate
- [ ] Owner role named for every step, and that role currently staffed
- [ ] Four exits written, each with a window
- [ ] Leading outcome chosen, and different from the trigger's own metric
- [ ] Holdout assignment job running, seeded and logged, before the first live fire
- [ ] The permitted claim sentence written down before anyone can be tempted to write a different one
- [ ] Kill criteria and review cadence recorded
- [ ] Automated sends leak-scanned, with a merge-field contract and a suppression rule per field
- [ ] Coverage Ledger printed, with the confidence cap and the named blind spots
- [ ] Excluded populations listed with the rule and a revisit date

## 10. Anti-patterns

| Anti-pattern | Correction |
| --- | --- |
| Nobody owns the library | One accountable owner, named, with the review on their calendar |
| Adding plays before retiring any | Kill first on the quarterly agenda, add second |
| Editing a threshold in the platform UI | Change the spec, bump the version, reset the window, then edit |
| A review that never kills anything | Every quarter retires at least the plays that hit a criterion, or the criteria are decorative |
| Deleting a retired play | Archive with the reason; it will be proposed again |
| Approving a new play, then sizing it | Size first. An unsized approval is a commitment to unknown hours |
| Holding measurement inside the platform only | Snapshot to the warehouse; platform history is usually not retained |
| A holdout the account team can see | CS Ops holds it |
| Treating suspension as retirement | Suspension keeps the window and the ID; retirement archives both |
| Governance documented but not calendared | Two meetings in the calendar, or none of this happens |
