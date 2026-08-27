# Trigger Design

> A trigger is not a filter you switch on. It is a commitment to spend a person's attention every
> time it fires, and that commitment has to be sized before the switch is flipped.
>
> Signal IDs (`U4`, `R1`, `C1` …) refer to `../../cs-context/references/signal-library.md`.
> Entity and field names are from `../../cs-context/references/normalized-schema.md`.
> Numbers here are labelled `[M]` measured · `[V]` vendor default · `[P]` practitioner ·
> `[A]` academic · `[D]` derived arithmetic. Anything unlabelled is a design convention of this
> library, not a benchmark — do not repeat it as a statistic.

**Contents**
1. [The four parts of a trigger](#1-the-four-parts-of-a-trigger)
2. [Trigger primitives by signal family](#2-trigger-primitives-by-signal-family)
3. [Fire-rate maths and the eligible population](#3-fire-rate-maths-and-the-eligible-population)
4. [Precision and capture at a fixed capacity](#4-precision-and-capture-at-a-fixed-capacity)
5. [The qualification layer](#5-the-qualification-layer)
6. [Suppression: cool-downs, exclusion, blackout](#6-suppression-cool-downs-exclusion-blackout)
7. [The twelve false-fire guards](#7-the-twelve-false-fire-guards)
8. [Shadow mode and the promotion gate](#8-shadow-mode-and-the-promotion-gate)
9. [Trigger lifecycle states](#9-trigger-lifecycle-states)
10. [The fire log](#10-the-fire-log)
11. [Worked example — sizing a usage-decay trigger](#11-worked-example--sizing-a-usage-decay-trigger)
12. [Anti-patterns](#12-anti-patterns)

---

## 1. The four parts of a trigger

Keep them separate in the spec. Merging detection and qualification is how a trigger ends up
firing on the whole book with no way to tell which clause caused it.

| Part | Fields it must specify | Failure when it is skipped |
| --- | --- | --- |
| **Detect** | `source` · `object.field` · computation · comparison window · baseline window · threshold · evaluation frequency | A threshold with no window is not a threshold. "Usage down 30%" means nothing without "against this account's trailing 90-day median, measured over 14 days" |
| **Qualify** | Segment · ARR floor · tenure floor · lifecycle stage · health band · business-model mask · seasonality mask · instrumentation guard | Firing on trials, internal accounts, accounts in week 3 of onboarding, and every account at once during a tracking outage |
| **Route** | Owner role · precedence rank against live plays · the record written (`play_run`) · notification channel | Two owners means none. An alert with no written record cannot be measured |
| **Act** | The play ID · the SLA from fire · the first step | A trigger with no attached action is a report. Publish it as a list instead |

**Detection is cheap; qualification is where precision is bought.** Loosen detection so the recall
is high, then buy precision back with qualifiers you can name and audit. The reverse — a tight,
clever detection rule with no qualifiers — produces a trigger nobody can debug when it misfires.

**Baselines are per-account, never global.** An account that has always run 4 weekly actives is not
in decay at 4. Every decay trigger compares an account against its own trailing baseline, with the
most recent 14 days excluded from that baseline so the decay does not dilute its own reference.

---

## 2. Trigger primitives by signal family

Thresholds below are **starting points to be re-tuned on your own fire log**, not benchmarks.
The `Expected fire rate` column is the band a healthy trigger should land in; anything above it
means the qualifier is too loose for your book.

### Family 1 — Product usage & adoption

| Signal | Computation | Starting threshold | Windows | Expected fire rate | Primary false fire |
| --- | --- | --- | --- | --- | --- |
| `U2` WAU decay | `wau_7d / median(wau_7d, trailing 90d excl. last 14d)` | < 0.70 for 2 consecutive weeks | 7d / 90d | 1–3%/mo | Public holidays; one power user on leave |
| `U4` Seat utilisation floor | `distinct_active_30d / seats_purchased` | < 0.60 watch, < 0.40 act | 30d | 2–5%/mo | Phased rollouts; accounts under 180 days old |
| `U7` Core-action depth | normalised slope of `core_actions` over 8 weeks | slope < −0.25 | 8w | 2–4%/mo | A project ending on schedule |
| `U8` Activation regression | account had the activation event, then zero in 30d | any occurrence | 30d | <1%/mo | Event renamed in the product; check the tracking plan first |
| `U13`/`U14` Provisioning stop / deprovisioning burst | `seats_provisioned` delta | −10% in 30d | 30d | <1%/mo | Licence clean-up after a migration |
| `T2` Integration disconnect | `integrations_active` drops and stays down | >7 days down | 7d | <1%/mo | Planned maintenance; credential rotation |
| `T6` Bulk export | admin-initiated export volume vs account's own history | first-of-kind volume | 30d | <0.5%/mo | Scheduled jobs; audit season; a warehouse build |

**Buying-team segmentation is a qualifier, not a separate trigger.** Where department attribution
exists, every usage trigger evaluates the contracted department separately from the account
aggregate; the aggregate alone is the single most common false-green.

### Family 2 — Commercial & contract

| Signal | Computation | Threshold | Expected fire rate | Note |
| --- | --- | --- | --- | --- |
| `C1` Auto-renew flag off | `subscription.auto_renew` false→true transition on `auto_renew_changed_at` | any change | <0.5%/mo | **Exempt from every cool-down and score gate (`R2`)**. Verify within 24h that the change was not our own re-papering |
| `C2` Notice served | notice record or termination clause invoked | any | <0.3%/mo | Hands straight to `save-play` |
| `C3` Seat reduction | `seats_purchased` delta mid-term | ≤ −25% | <1%/mo | Partial churn already happened |
| `C13` Renewal stage stagnation | `opportunity.stage_changed_at` age vs the stage's own median | > 2× median | 1–3%/mo | Needs at least 30 closed opportunities to set the median |
| Opt-out countdown | `opt_out_deadline − today` crosses 180/120/90/60 | each crossing, **once** | fixed by book shape | **Never the renewal date (`R1`)**. Each rung carries a behavioural qualifier |
| `C15` Commitment pacing | `consumed / (commitment × elapsed_term_fraction)` | < 0.70 | 2–4%/mo | Consumption books only; replaces `U4` entirely |

### Family 3 — Relationship & engagement

| Signal | Computation | Threshold | Expected fire rate | Note |
| --- | --- | --- | --- | --- |
| `R1` Champion departure | `contact.email_status = hard_bounce` on a contact with `role ∈ {champion, economic_buyer}` | any | <1%/mo | 48-hour SLA, VP-or-above sender (`R3`). **Never automated** |
| `R4` Single-threading | distinct `customer_participants` in 90d | ≤1 (enterprise ≤2) | 3–8%/mo | High volume — pair with an ARR floor or run as a quarterly list, not an alert |
| `R7` Reply latency | 30d mean `response_latency_hours` vs prior 90d | > 2× | 2–4%/mo | Holiday periods; a new contact learning the thread |
| `R11` Procurement re-engagement | inbound from a procurement or legal domain/role | any | <0.5%/mo | Commercial-event class — exempt from cool-down |
| `Z1` Silence | `today − max(interaction.timestamp)` | ≥45d on a covered account | 5–15%/mo | Usually a **list**, not an alert, unless qualified by ARR and renewal proximity |

### Family 4 — Support & reliability

| Signal | Computation | Threshold | Expected fire rate | Note |
| --- | --- | --- | --- | --- |
| `P1` Ticket cluster | `ticket_count_7d` per account, normalised per 100 seats | ≥3 in 7 days | 2–5%/mo | Normalise or every large account fires every week |
| `P2` Spike then silence | cluster followed by zero tickets in the next 30d, with the cluster unresolved | pattern match | <1%/mo | The strongest quiet-churn precursor; needs the resolution field |
| `P3` Repeat issue | same `linked_issue_id` or root cause ≥3 times | ≥3 in 90d | 1–2%/mo | Requires a usable root-cause field, not free text |
| `P5` P1 ageing | open `priority=urgent` age | >14 days | <1%/mo | Escalation-class; exempt from cool-down |

### Family 5 — Sentiment & VoC

| Signal | Computation | Threshold | Expected fire rate | Note |
| --- | --- | --- | --- | --- |
| `S1` Detractor response | survey score | 0–6 | bounded by response rate | 24-hour SLA. Route by respondent role, not by score alone |
| `S1` Promoter response | survey score | 9–10 | bounded by response rate | Advocacy queue; gate on health (`R8`) before any ask |
| `S2` CSAT trajectory | 90d mean vs prior 90d | −1 point or more | 1–3%/mo | Needs ≥3 responses per window or it is noise |
| `S4` CSM gut field | manual flag | any change to negative | <1%/mo | The cheapest high-precision signal most teams already have and do not route |

### Family 6 — Billing & payment

| Signal | Computation | Threshold | Expected fire rate | Note |
| --- | --- | --- | --- | --- |
| `C10` Dunning entered | `invoice.status = overdue` + failed attempts | 2 failed attempts | 1–3%/mo | Fully automatable first touch |
| `C9` Payment method expiring | `payment_method_status` | `expiring` within 30d | 1–2%/mo | Pure administrative; automate end to end |
| `C8` DSO deterioration | mean days-late this 90d vs prior 180d | +10 days | 1–2%/mo | Compare the account to **its own** history, never to a portfolio mean |

### Family 7 — Firmographic & external

| Signal | Threshold | Expected fire rate | Note |
| --- | --- | --- | --- |
| `F2` Exec change at the customer | any CIO/CFO/functional-exec change | <1%/mo | Exec-to-exec, never automated |
| `F1` Acquisition / merger | any | <0.5%/mo | Long lead time; opens a consolidation-risk record |
| `F3` Layoffs / RIF | any reported | <1%/mo | Budget-class, not adoption-class — do not send an adoption nudge into a layoff |
| `F4` Funding round | any | <1%/mo | Expansion-class; still gated on health (`R8`) |

---

## 3. Fire-rate maths and the eligible population

```
eligible_accounts = accounts passing the qualifier, excluding is_internal, trials,
                    churned, and any population listed under "Not covered this cycle" (R14)

fire_rate_30d     = distinct accounts with ≥1 fire in a 30-day window ÷ eligible_accounts
alerts_per_CSM_wk = (fire_rate_30d × eligible_accounts) ÷ 4.33 ÷ CSM_count
```

| Fire rate (30d) | Reading | What to do |
| --- | --- | --- |
| ≤ 2% | Healthy. Genuinely exceptional accounts | Ship it |
| 2–5% | Acceptable **only if the action is cheap** — a task, an in-app nudge, a templated send | Ship it with the cheap action; do not attach a 4-hour motion |
| 5–15% | This is a segment, not a trigger | Tighten the qualifier, or convert to a weekly list |
| > 15% | This is a report | Publish the list. Page nobody |

**Count distinct accounts, not fires.** A trigger that fires daily on the same 40 accounts looks
like 1,200 events and is really 40 problems. Every fire-rate number in a spec is distinct accounts
in a 30-day window.

**Two triggers with the same root cause are one trigger.** Before adding one, run the overlap:
what share of its fires are already covered by a live play in the same 30 days? Above 60% overlap,
merge them rather than shipping both — the second one only adds noise and a second owner.

---

## 4. Precision and capture at a fixed capacity

At a fixed capacity `K` — the accounts a team can actually work in a period — only three numbers
matter, and none of them is model accuracy `[A]`:

| Metric | Formula | The question it answers |
| --- | --- | --- |
| **Precision @ K** | `true positives in top K ÷ K` | Of the accounts we worked, how many were real? Determines whether CSMs keep opening the alerts |
| **Capture @ K** | `true positives in top K ÷ all true positives` | What share of the problem did we even see? |
| **Dollar capture @ K** | `Σ ARR of true positives in top K ÷ Σ ARR of all true positives` | The only version a CCO reviews |

**Rank by expected loss, not by score.** A 12% risk on $800k outranks a 60% risk on $40k. Publish
two orderings when the team disagrees about which matters — by probability and by `ARR × p` — and
make the second the default for the review.

**Never report accuracy on a rare event.** At a 3% base rate, "predict renew for everyone" scores
97% `[A]`. Refuse the metric explicitly when asked for it.

---

## 5. The qualification layer

Eight qualifiers. Every trigger spec lists all eight, writing `none` where one does not apply —
an omitted qualifier is indistinguishable from a forgotten one.

| Qualifier | Default | Why |
| --- | --- | --- |
| **Segment** | All covered segments | A play designed for enterprise firing on a self-serve book produces work nobody has hours for |
| **ARR floor** | The floor at which the action pays for itself: `hours_per_motion × loaded_hourly_cost × 3` | Below it, use a pooled or digital motion |
| **Tenure floor** | 180 days for any decay trigger | Accounts under 180 days are ramping, not dying — they belong to onboarding plays |
| **Lifecycle stage** | Exclude onboarding and trial | An adoption nudge to an account mid-implementation reads as not knowing who they are |
| **Health band** | Expansion and advocacy plays: Secure or Watch only (`R8`) | Selling into an unhealthy account converts a recoverable risk into a churn |
| **Business-model mask** | Per `business-model-profiles.md` | Seat utilisation on a consumption book measures nothing |
| **Seasonality mask** | Suppress the account's known low season | A trigger that fires on every account every August teaches the team to ignore it |
| **Instrumentation guard** | Suppress if the source had a collection gap > 6h in the window | A tracking outage reads as a usage collapse across the whole book at once |

**The ARR floor is arithmetic, not a feeling.** If a motion costs four hours and the loaded hourly
cost is $95, the motion costs about $380; at a 3× coverage ratio it should not run on accounts
below roughly $1.1k of exposure. Compute it per play and print it.

---

## 6. Suppression: cool-downs, exclusion, blackout

### Cool-downs by play category

| Category | Default cool-down | Rationale |
| --- | --- | --- |
| Risk | 30 days | Shorter than the motion length means two open runs on one account |
| Adoption | 60 days | Adoption changes slowly; a 30-day re-fire is the same conversation |
| Onboarding | 14 days | Short cycle, high urgency, short memory |
| Expansion | 90 days | A second ask inside a quarter reads as a quota problem |
| Lifecycle | Once per rung per term | The T-90 rung fires once, not every day for 30 days |
| Advocacy | 180 days | Asking the same customer twice a year is the ceiling |
| Administrative | 7 days | Payment and entitlement issues recur legitimately |
| **Commercial-event class** | **None (`R2`)** | Auto-renew off, notice served, procurement engaged, bulk export — decisions, not indicators |

### Mutual exclusion

One primary play per account (`R17`). Precedence, highest first:

```
commercial event > risk > onboarding > adoption > expansion > advocacy > administrative
```

Administrative plays are the exception that may run **alongside** a primary play — a failed payment
still needs fixing during a save — but they never page the same owner in the same week.

### Blackout windows

| Blackout | Suppresses | Duration |
| --- | --- | --- |
| Open escalation | Adoption, expansion, advocacy, lifecycle nudges | Until the escalation closes + 14 days |
| Active save play | Everything except commercial-event class | Until the save exits |
| Live renewal negotiation | Expansion (unless co-terming, `R12`), advocacy | Until signature |
| Incident affecting this account | Everything automated | 72 hours after resolution |
| Onboarding in flight | All adoption and risk decay plays | Until the go-live milestone |

---

## 7. The twelve false-fire guards

Run every one before a trigger is promoted out of shadow. Each has ended a real team's trust in
its own alerts.

| # | Guard | What it catches |
| --- | --- | --- |
| 1 | **Instrumentation gap** | A tracking outage or SDK change reading as a usage collapse. Check event-volume continuity for the whole book before believing one account |
| 2 | **Identity resolution break** | A domain migration or SSO change orphaning users, so an account looks abandoned |
| 3 | **Seasonality** | Academic summers, retail freezes, public-sector year end |
| 4 | **Single power user** | One person's holiday moving an account-level metric |
| 5 | **Planned migration** | A deliberate, agreed move of a use case to another team |
| 6 | **Ramp period** | Accounts under 180 days scored against a steady-state baseline |
| 7 | **Shared/service accounts** | One login hiding ten humans, wrecking per-seat utilisation |
| 8 | **Internal accounts** | Employee and sandbox orgs inflating or deflating the book |
| 9 | **Our own re-papering** | An auto-renew flag we switched off for a restructured deal |
| 10 | **Product rename** | An event or feature renamed, so adoption reads as zero |
| 11 | **Bounce that is not a departure** | Mailbox full, out-of-office, domain migration — check for a forwarding address before asserting `R1` |
| 12 | **Resolved-then-fired** | The condition cleared between evaluation and send. Re-check at send time, not only at detect time |

Guard 12 is the one most often missing, and it is the one customers notice: a message about a
problem they fixed last week tells them nobody is actually watching.

---

## 8. Shadow mode and the promotion gate

A new trigger writes to `trigger_fire` with `mode = 'shadow'` for **two review cycles** and pages
nobody. It is promoted only when all five hold:

| Gate | Threshold |
| --- | --- |
| Fire rate inside the designed band | Yes, for both cycles |
| Modelled intake fits the capacity budget with existing live plays | Yes (`R13`) |
| False-fire rate on a manual sample of 20 fires | ≤ 20% |
| Overlap with any live play | < 60% of fires |
| Owner role named, and that role currently staffed | Yes |

Failing any gate: retune once, run one more cycle, then abandon. A trigger that cannot pass in
three cycles is telling you the signal is not there.

**Sampling for the false-fire rate:** take 20 fires at random, and for each ask a human who knows
the account "would you have wanted to be interrupted for this?" Record the answer. That question,
not a model metric, is what the CSM is going to be making next quarter anyway.

---

## 9. Trigger lifecycle states

| State | Meaning | Who may change it |
| --- | --- | --- |
| `proposed` | Specified, not implemented | Author |
| `shadow` | Firing to the log only | CS Ops |
| `live` | Firing to owners | CS Ops, after the promotion gate |
| `suspended` | Temporarily off — owner vacant, source broken, seasonal | CS Ops or the owning lead |
| `deprecated` | Superseded; still logging for one cycle to confirm the successor covers it | CS Ops |
| `archived` | Off, with its spec and change log retained | Never deleted |

---

## 10. The fire log

Without this table there is no fire rate, no completion rate, no cycle time and no measurement.
Build it before the first trigger goes live; retro-fitting it is far more expensive.

| Table | Grain | Key fields |
| --- | --- | --- |
| `trigger_def` | one row per trigger version | `trigger_id`, `version`, `play_id`, `sql_or_rule`, `state`, `effective_from`, `author` |
| `trigger_fire` | one row per account per trigger per fire | `fire_id`, `trigger_id`, `trigger_version`, `account_id`, `fired_at`, `mode`, `qualified`, `suppressed_by`, `payload` |
| `play_run` | one row per run | `run_id`, `fire_id`, `play_id`, `play_version`, `account_id`, `owner_role`, `owner_user`, `started_at`, `first_human_touch_at`, `exited_at`, `exit_reason` |
| `play_step_run` | one row per step per run | `run_id`, `step_no`, `due_at`, `completed_at`, `sla_met`, `automated` |
| `holdout_assignment` | one row per fire | `fire_id`, `account_id`, `arm` (`treated`/`holdout`), `assigned_at`, `randomisation_seed` |

**Log suppressed fires too.** `suppressed_by` is how you discover that a trigger has been silently
muted by a blackout for two quarters, which looks identical to a trigger that never fires.

---

## 11. Worked example — sizing a usage-decay trigger

Book: 640 active accounts, 8 CSMs, enterprise annual contracts. Proposed trigger: WAU decay.

```
Detect     wau_7d / median(wau_7d, trailing 90d excl. last 14d) < 0.70,
           two consecutive weekly evaluations
Qualify    segment ∈ {enterprise, mid-market} · ARR ≥ $25k · tenure ≥ 180d ·
           lifecycle = steady-state · seasonality mask = none · instrumentation guard on
Route      owner_csm, precedence rank 2 (risk), writes play_run
Act        play PB-R01 usage-decay rescue, SLA 48h to first human touch
```

| Step | Arithmetic | Result |
| --- | --- | --- |
| Eligible population | 640 − 74 (below ARR floor) − 38 (tenure < 180d) − 11 (internal/trial) | **517** |
| Backfilled fires, last 90 days | 61 distinct accounts | 20.3/month |
| Fire rate | 20.3 ÷ 517 | **3.9%** — inside the 2–5% band, but only for a cheap action |
| Intake per CSM | 20.3 ÷ 4.33 ÷ 8 | **0.59 alerts/CSM/week** |
| Capacity budget | 40h × 0.60 usable × 25% proactive = 6h/wk; motion 4h over 3 weeks → 4.5 concurrent → **1.5/week** | Fits, with room for one more play |
| Overlap with the live churn-risk escalation | 7 of 61 fires already covered | 11% — no merge needed |

Verdict: promote to shadow. Re-check the false-fire rate on 20 sampled fires before going live —
the two guards most likely to bite here are seasonality (guard 3) and single power user (guard 4).

Had the fire rate come back at 11%, the correct move is **not** to ship it and hope: tighten the
ARR floor to $50k, or drop the threshold to 0.60, and re-size.

---

## 12. Anti-patterns

| Anti-pattern | Correction |
| --- | --- |
| A threshold with no window or baseline | Every decay compares the account to its own trailing baseline, with the recent period excluded |
| Counting fires instead of distinct accounts | 1,200 events on 40 accounts is 40 problems |
| Shipping a trigger straight to live | Two cycles in shadow, then the promotion gate |
| A global baseline for a per-account metric | Accounts differ by an order of magnitude; compare each to itself |
| Two triggers on the same root cause | Run the overlap; above 60%, merge |
| No cool-down | The same account paged weekly until the CSM filters the sender |
| A cool-down on an auto-renew flag change | Commercial events are exempt (`R2`) |
| Suppressed fires not logged | You cannot tell a muted trigger from a dead one |
| Firing on accounts under 180 days | Ramping is not dying; that is an onboarding play |
| Believing a usage collapse before checking the tracking plan | Guard 1, every time — it fires across the whole book at once |
| A trigger with no named owner role | Route to a role, and suspend when that role is vacant |
| Sending after the condition resolved | Re-check at send time, not only at detect time (guard 12) |
