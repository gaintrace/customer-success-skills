# Stall Detection — thresholds, traps, escalation ladders, and the scoreboard

> Read this when instrumenting Step 7 at kickoff, at every weekly implementation review, and
> whenever a signal fires and you need to know what it actually means before acting on it.
>
> Onboarding is the one lifecycle stage where the leading signals are unambiguous and the lead
> times are long. TTFV overrun, milestone slippage, services burn and a dark environment all fire
> *during* implementation and predict the **first** renewal 180–365 days out. The failure is never
> detection difficulty. It is that nobody instrumented the project, so the stall surfaces at the
> first business review instead of in week three.

**Contents**
1. [The instrumentation contract](#1-the-instrumentation-contract)
2. [The ten signals in full](#2-the-ten-signals-in-full)
3. [False-positive traps](#3-false-positive-traps)
4. [The burn-ratio pairing rule](#4-the-burn-ratio-pairing-rule)
5. [Vendor-side slip vs customer-side slip](#5-vendor-side-slip-vs-customer-side-slip)
6. [Compound patterns](#6-compound-patterns)
7. [Cohort construction and the scoreboard](#7-cohort-construction-and-the-scoreboard)
8. [The weekly review runbook](#8-the-weekly-review-runbook)

---

## 1. The instrumentation contract

Three rules, set at kickoff, before any signal can be trusted.

| Rule | Why it exists |
| --- | --- |
| **Every signal is defined and wired before Phase 1 ends** | A threshold invented in month three is a rationalisation of a stall already visible in week two |
| **Every signal is evaluated weekly and reported — fired, checked-and-clear, or not-checkable** | A signal silently dropped because "it didn't seem relevant" is the mechanism by which a sweep stops being a sweep |
| **`NULL` is not `0`** | An account with no usage pipe is not an account with no usage. `NULL` is a coverage gap and goes to the ledger; `0` core actions on day 70 of a live production environment is the most important finding you will produce |

The provenance discipline in `../../cs-context/references/evidence-standard.md` applies unchanged.
Thresholds below are marked `[P]` — practitioner planning rules calibrated on implementation
portfolios, not published benchmarks. Replace them with your own cohort history the moment you
have 20+ completed implementations; until then, state that they are `[P]` every time you use one.

---

## 2. The ten signals in full

### S1 — Milestone slippage

| | |
| --- | --- |
| **Computation** | `% milestones overdue`, `cumulative_slip_days` (sum of days each completed milestone landed past its baselined due date, plus days-overdue on open ones) |
| **Fire threshold** | ≥2 milestones overdue **or** cumulative slip >30 days `[P]` |
| **Read** | Slip is compounding when the *rate* rises: 4 days slipped in week 2, 9 in week 4, 21 in week 6 is a plan that has stopped describing reality |
| **Escalation** | Re-plan with the customer, in writing, within 5 business days. A re-plan that is not written down and countersigned is a hope |
| **Do not** | Re-baseline silently. The whole value of the number is that it accumulates across re-plans — reset it and you lose the only evidence that the account is structurally late |

### S2 — TTFV overrun

| | |
| --- | --- |
| **Computation** | `actual_elapsed_days / target_ttfv_days` (target from `cs-context` §5) |
| **Fire threshold** | >1.5× → risk; >2.0× → severe; no value event by day 90 → severe `[P]` |
| **Read** | Green milestone adherence alongside a 2× TTFV overrun is diagnostic on its own: the milestones are measuring vendor tasks, not customer outcomes |
| **Escalation** | Severe: exec-sponsored recovery with a re-baselined go-live and a named cause. Not a "check-in" |

### S3 — Blocked-task ownership

| | |
| --- | --- |
| **Computation** | Share of overdue tasks whose owner is customer-side |
| **Fire threshold** | ≥60% customer-side for 2 consecutive weeks |
| **Read** | This is a resourcing or authority problem on their side, not an engagement problem. The admin usually *cannot* do the thing, rather than will not |
| **Escalation** | Go to the exec sponsor with the specific named blocker and the decision needed. Never escalate a customer-side block to the customer-side person it is blocking |

### S4 — Unresponsive admin

| | |
| --- | --- |
| **Computation** | Days since the last **bilateral** touch — a customer reply, a joined meeting, or a product action. Exclude one-way vendor outbound entirely |
| **Fire threshold** | Two missed cadence periods: white-glove 10 business days, guided 10, tech-touch 21 `[P]` |
| **Read** | Silence during implementation is rarely disinterest. It is usually a reorg, a competing internal project, or an admin who has been told to stop |
| **Escalation** | Multithread the same week: the sponsor **and** a second named contact. Do not send a fourth follow-up to the same inbox |

### S5 — Environment never in production

| | |
| --- | --- |
| **Computation** | `prod_events / total_events` across the measurement window |
| **Fire threshold** | <0.20 after day 90 post-go-live `[P]` |
| **Read** | The project record says live; the telemetry says sandbox. The project record is wrong |
| **Escalation** | Technical escalation. Treat go-live as **not achieved**, regardless of what the project status field says, and recompute float from today |

### S6 — Dark account

| | |
| --- | --- |
| **Computation** | Zero qualifying core events since `contract_start` |
| **Fire threshold** | >60 days from contract start `[P]` · strength: **near-certain** |
| **Read** | The highest-precision signal in the set. It has almost no false-positive mode once the telemetry pipe is confirmed connected — which is exactly why confirming the pipe is step one |
| **Escalation** | Same-week exec-to-exec. Not a nurture email |

### S7 — No new users provisioned

| | |
| --- | --- |
| **Computation** | `new_users_L30` against the rollout plan's per-team schedule |
| **Fire threshold** | Zero new users in 30 days while `seat_utilisation < 0.85` |
| **Read** | The rollout has stalled at the pilot team. Name the team that has not started and its lead — "adoption is low" is not a finding, "Finance has provisioned 0 of 40 and Priya has not scheduled the session" is |
| **Escalation** | To the rollout owner named at kickoff, with the specific team and the specific date it was due |

### S8 — Services burn ratio

| | |
| --- | --- |
| **Computation** | `hours_burned / hours_sold`; `scope_change_count` |
| **Fire threshold** | >1.3× sold hours, or ≥2 change orders `[P]` |
| **Read** | **Never read alone.** See §4 — burn is only interpretable against activation |
| **Escalation** | Depends entirely on the pairing. Margin conversation, recovery, or coverage fix |

### S9 — Use case never live

| | |
| --- | --- |
| **Computation** | Has the account ever performed the core action of the use case that was sold? |
| **Fire threshold** | Never, by day 90 post-go-live `[P]` · strength: **near-certain** |
| **Read** | Almost always traceable to a gap already logged in the Sold-vs-Real table and then not worked |
| **Escalation** | Re-open Sold-vs-Real. The recovery is whichever gap class it belongs to, not a training session |

### S10 — Kickoff-to-config stall

| | |
| --- | --- |
| **Computation** | `config_complete_date − kickoff_date` against the mode default (`phase-playbook.md` §2) |
| **Fire threshold** | >2× the mode default |
| **Read** | Configuration is blocked on a decision nobody has been asked to make — a field taxonomy, a permissions model, an approval chain the customer has not settled internally |
| **Escalation** | Name the decision, name who can make it, and put a date on it. Do not offer more configuration help |

---

## 3. False-positive traps

Every trap below has produced a wrong escalation on a healthy account. Check the trap before you
act on the signal.

| Signal | The trap | The check that clears it |
| --- | --- | --- |
| S1 | Milestones were baselined against a date the customer never agreed to | Was the plan countersigned? An unagreed date cannot slip |
| S2 | `target_ttfv_days` is a segment default nobody applied to this account's complexity | Recompute the target from the mode and the integration count before calling overrun |
| S3 | One customer owner covering three workstreams looks like disengagement | Check the owner count. A single-admin customer serialises everything by design (`phase-playbook.md` §3) |
| S4 | Bilateral touch missed because the thread moved to a shared Slack channel or the sponsor's inbox | Widen the touch definition to every channel before firing |
| S5 | Telemetry pipe points at sandbox; production is instrumented separately or not at all | Confirm the pipe before concluding the environment is dark |
| S6 | The events table was never connected for this account | `NULL` is a coverage gap, not a zero. It goes to the ledger, not to the exec |
| S7 | Seats were deliberately bought ahead of a phase-2 rollout with a dated plan | Is there a dated rollout schedule? Then it is on plan, not stalled |
| S8 | High burn on a complex deployment is investment, not risk | §4. Always |
| S9 | A second use case went live first and delivers real value | Ask whether the *sold* outcome is still the outcome they want, then fix Sold-vs-Real |
| S10 | Configuration is complete but the completion date was never written back | Check the environment, not the field |

Two general rules. **A signal that cannot be computed is reported as not-checkable, never as
clear** — the missing pipe is itself the finding. And **no signal is escalated on a single weekly
observation** except S6 and S9, which are near-certain and where waiting a week costs a week.

---

## 4. The burn-ratio pairing rule

The commonest misread in onboarding analytics is treating high services burn as risk. On a
complex, involved deployment it is investment. Burn is only interpretable against activation.

| Burn | Activation | Read |
| --- | --- | --- |
| >1.3× | Achieved | **Healthy but unprofitable.** A margin problem and a scoping problem. Not a churn signal, and escalating it as one damages a good account |
| >1.3× | Not achieved | **Severe.** Money spent, no outcome. This is the `Failed launch` compound pattern in §6 |
| ≤1.0× | Not achieved by day 60 | **Severe and quiet.** Nobody is working the account. Usually a vendor-side coverage gap, not customer disengagement — check the assigned PM's book before assuming anything about the customer |
| ≤1.0× | Achieved early | **Model account.** Capture the configuration and the sequence; it is a reusable pattern and the cheapest content your onboarding motion will ever get |

The margin frame behind the top row: professional services run a 30% median gross margin, and
services above roughly 15–20% of total revenue pulls total gross margin below the 77% median
(Benchmarkit 2025 SaaS Performance Metrics, CY2024, N=38/196) `[M]`. Over-servicing an account
whose ARR cannot carry it is a margin decision wearing a service costume.

---

## 5. Vendor-side slip vs customer-side slip

In the data they are identical — a milestone past its due date. They are opposite problems with
opposite plays, and conflating them is why implementation reviews produce no decisions.

| | Vendor-side slip | Customer-side slip |
| --- | --- | --- |
| **Looks like** | Config, integration or migration tasks late | Access, data, decisions, scheduling or sign-off late |
| **Usual cause** | Under-resourced implementation, competing accounts, a defect | One owner covering everything, or no authority to decide |
| **Play** | Add vendor resource, or cut scope. Say which, this week | Escalate to the exec sponsor with the named decision |
| **Never** | Escalate our own resourcing gap to the customer | Send another chase to the person who is already blocked |

Tag every task with the side that owns it at the moment it is created. That single tag turns the
overdue list into a work order. Report the split in the Step 7 table every week:
`vendor-side n · customer-side n · shared n`.

---

## 6. Compound patterns

Single signals inform. Compounds decide.

| Pattern | Match condition | Lead time | The play |
| --- | --- | --- | --- |
| **Failed launch** | S2 + S1 + S8 + S6 co-occurring | 180–365 days, predicting the **first** renewal | Exec-sponsored recovery with a re-baselined go-live and a stated cause. Consider a term restart, not a renewal ask. Do **not** run a normal renewal motion on it |
| **Pilot trap** | S7 + S9, activation achieved by the pilot team only | 90–180 days | The rollout owner, the named next team, and a dated session. The account is healthy and one process change from worthless |
| **Phantom go-live** | S5 + green project status | Immediate | Recompute float from today with go-live unachieved, and correct the project record before anyone reports on it |
| **Quiet abandonment** | S4 + S3 with burn ≤1.0× | 60–120 days | Multithread and check the vendor-side book. Silence on both sides usually means neither side has an owner |
| **Decision deadlock** | S10 + S3 | 30–90 days | Name the unmade decision and the person who can make it. More configuration help makes this worse |

A compound match is stated in the artifact as matched or not-matched, always — including
not-matched. That is what makes the sweep verifiable rather than asserted.

---

## 7. Cohort construction and the scoreboard

### The metrics

| Metric | Definition | How to read it |
| --- | --- | --- |
| **TTFV** | Days from contract start to the first completed **success milestone** — a customer-defined outcome, not a vendor task (Murphy's success-milestone basis) `[P]` | Median **and P90**. P90 is where the churn lives |
| **TTV / time-to-live** | Days from contract start to production go-live with the contracted use case | The gap between TTV and TTFV *is* the Success Gap, in days |
| **Onboarding cycle time** | Decomposed: signature→kickoff, kickoff→config-complete, config→go-live, go-live→adoption-threshold | The longest segment is the real bottleneck, and it is rarely the one people complain about |
| **Milestone adherence** | `% completed on or before due date`, plus cumulative slip days | Green adherence with a blown TTFV means the milestones measure the wrong things |
| **Services burn ratio** | `hours_burned / hours_sold` | Read only against activation (§4) |
| **Activation rate by cohort** | `accounts reaching the activation event within N days / accounts in the cohort` | 30/60/90-day cohorts, benchmarked against your own history |
| **Stalled-onboarding ARR** | ARR in accounts >X days past target go-live | A named at-risk category on the revenue report — the number that buys onboarding headcount |

### Cohort construction

| Rule | Why |
| --- | --- |
| **Cohort on `contract_start` month, never on go-live month** | Cohorting on go-live silently excludes every account that never went live, which is the population you are trying to measure |
| **Keep accounts in their cohort until they reach the event or churn** | Removing a stalled account "because it is not representative" is how a motion looks fine while it is failing |
| **Never mix modes in one cohort** | White-glove and tech-touch have different physics; a blended median describes no account that exists |
| **State the cohort's n on every figure** | A median over 4 accounts is an anecdote with a decimal point |
| **Censor honestly** | Accounts still inside the window are `in progress`, not `failed` and not excluded. Report `n reached / n in cohort / n still in window` |

### Two integrity rules

**Benchmark against your own cohort baseline, not a published TTV median.** The cross-company TTFV
figures circulating online are content-marketing numbers with no disclosed method, no cohort
definition and no censoring rule. Your own last four quarters is a better comparator than any of
them, and it is the only one you can act on.

**Never report a mean.** Onboarding durations have a long right tail. The mean hides exactly the
accounts that will not renew — median and P90, every time, with the n.

---

## 8. The weekly review runbook

Fifteen minutes per account in flight, same order every week.

1. **Recompute float** (`V-day − (today + remaining critical path)`) and state the band. If the band
   changed since last week, that is the first sentence.
2. **Walk all ten signals.** Fired / checked-and-clear / not-checkable. No skipping.
3. **Split the overdue list** vendor-side vs customer-side (§5) and act on the split, not the total.
4. **Check the compounds** in §6, including the ones that did not match.
5. **Confirm the value gate is still the right gate.** A changed business priority on the customer's
   side moves V-day; discovering that in month four is a save play, discovering it in week five is
   a conversation.
6. **One decision, one owner, one date.** A review that ends without one did not happen.
7. **Write the float number and the fired-signal names into the account record**, not into a
   document nobody will open. The next reviewer needs the series, not this week's snapshot.

Anything customer-facing that comes out of this review — a revised plan, a chase, a re-baseline
note — goes through `../../cs-context/references/customer-voice.md` first. Float, burn ratio, stall
signal names, "stalled", "at risk" and the ranked queue are internal vocabulary and never reach the
customer in any wording.
