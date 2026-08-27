# The First Renewal — the risk record, the decision window, and the handoff

> Read this when you reach Step 6 and are about to open the account's risk record, when float
> goes negative and you need to know what you are actually trading away, and whenever someone
> proposes marking an implementation complete at go-live.
>
> The first renewal is not decided in the renewal conversation. It is decided in months two to
> four of the first term `[C23]`, while the implementation is still running and while everyone
> involved still believes the project is going well. A renewal plan opened at T-90 on an
> implementation that never produced the outcome is negotiating from a position that was lost
> two quarters earlier and never written down.
>
> This file is the mechanism that stops that. It defines one record, one date it may open on,
> and one handoff.

**Contents**
1. [Two events, not one](#1-two-events-not-one)
2. [The decision window — months 2 to 4](#2-the-decision-window--months-2-to-4)
3. [The first-renewal risk record](#3-the-first-renewal-risk-record)
4. [Opening states and what each one obliges](#4-opening-states-and-what-each-one-obliges)
5. [The Failed-launch handoff to churn-risk](#5-the-failed-launch-handoff-to-churn-risk)
6. [Refusals](#6-refusals)
7. [Worked example](#7-worked-example)

---

## 1. Two events, not one

Go-live and first value are different events, with different owners, different evidence and
different dates. Every implementation that was "delivered on time" and churned at month
fourteen conflated them.

| | **Go-live (G-day)** | **Value gate (V-day)** |
| --- | --- | --- |
| The question | Is the product in production doing the contracted job? | Did the customer get the outcome they bought? |
| Owner | Vendor implementation lead | The customer's named business owner |
| Who can attest it | We can | Only they can |
| What it closes | Our task list | The onboarding |
| What it opens | Nothing | **The first-renewal risk record** |

The rule this file exists to enforce: **the risk record opens at V-day, never at G-day.** A
record opened at go-live is a record about our delivery, and it will read green while the
customer's side of the Success Gap is still empty. A record opened at V-day is a record about
their outcome, and it is the only one that predicts the renewal.

The second rule: **V-day closes the onboarding.** Not G-day, not the last completed milestone,
not the project-plan percentage. An implementation at 100% of its task list with V-day
unattested is not complete — it is `LIVE, NOT VALUED`, which is a named state with an owner and
a date, not a rounding error.

---

## 2. The decision window — months 2 to 4

The customer forms their renewal view long before they express it, and long before the notice
window opens. Three things are settled in months two to four of a first term:

1. Whether the thing they bought works in their environment (configuration and integration).
2. Whether their own people changed how they work (enablement and rollout).
3. Whether the person who signed can describe a result to someone who did not sign.

By month five those are answers, not questions, and the renewal conversation reports them rather
than changing them.

```
decision_window_open   = contract_start + 30d      # month 2
decision_window_close  = contract_start + 120d     # month 4          [P]
```

`[P]` — a practitioner planning window, not a published benchmark. Replace it with your own
first-term cohort history the moment you have 20+ first renewals with a dated activation event;
until then state that it is `[P]` every time you print it.

**The verdict that must be printed.** Compare V-day to the close of the window:

| Condition | Verdict | What the plan must then say |
| --- | --- | --- |
| `V-day ≤ decision_window_close` | **Decided on evidence** | The renewal view forms with the activation event already recurring. Proceed. |
| `V-day > decision_window_close` | **Decided on faith** | The customer forms their renewal view before value exists. Say so in the first five lines on day one, name which of the three levers is being pulled — cut scope to a smaller first use case, move the gate by renegotiating the term, or accept a first renewal argued without evidence — and put an owner and a date on it. |
| `V-day` not computable | **UNKNOWN — requires the activation event and either the opt-out deadline or `target_ttfv_days`** | No verdict is invented. The gap is the finding. |

"Decided on faith" is not a warning label; it is a structural fact about the plan that was just
written, and it is worth more on day one than any status report in month five. In week one it is
a scope conversation. In month five it is a save play.

---

## 3. The first-renewal risk record

One record per first-term account. It is internal, it never leaves the building (R18), and it
carries these fields. A field with no value is written `UNKNOWN — requires <source>`; the row is
never dropped and never filled with a plausible value.

| Field | Rule |
| --- | --- |
| `opened_at` | **The V-day event date** — the date the activation event was attested, or the date V-day passed unattested. Never G-day. Never the project-completion date. |
| `opening_state` | One of `VALUED` · `LIVE, NOT VALUED` · `NOT LIVE` (§4). No fourth value. |
| `record_owner` | The named person who owns this account's first renewal from V-day forward — normally the receiving CSM. A team name is not an owner. |
| `first_renewal_decision_date` | `renewal_date − notice_period_days` (R1). The renewal date itself is never written in this field. |
| `decision_window` | `contract_start + 30d` → `contract_start + 120d`, and whether V-day falls inside it. |
| `value_evidence` | The attested activation event: what fired, how many cycles, performed by whom, against which baseline, attested by whom, on what date. Or `UNKNOWN — requires <source>`. |
| `baseline_ref` | Pointer to the kickoff baseline record (`../references/kickoff.md` §5). A record with no baseline cannot produce value evidence at renewal and says so here. |
| `open_gaps` | Every unresolved Sold-vs-Real row, with its gap class and dated resolution. |
| `signals_at_close` | The Step 7 signal set as it stood at V-day — fired, clear and not-checkable — carried forward, not recomputed later from memory. |
| `handoff_to` | `churn-risk` (always), plus `save-play` where §5 fires. Named with the date the receiving skill takes the account. |

**The record is opened once.** It is not re-opened at T-90, and a renewal plan that starts by
opening a fresh risk record has thrown away the two quarters of evidence that explain the
outcome. `renewal-prep` and `qbr-builder` read this record; they do not replace it.

---

## 4. Opening states and what each one obliges

| State | Condition | The record opens with | Obligation |
| --- | --- | --- | --- |
| **VALUED** | Activation event observed at cadence for ≥2 cycles, by the buying team, against the captured baseline, attested in writing by the named customer owner | Green, with `value_evidence` populated and the baseline delta stated | Steady-state handover proceeds (Step 9). `expansion-finder` is unblocked from here, subject to R8 and R9 |
| **LIVE, NOT VALUED** | G-day evidence complete, V-day unattested on or after V-day | Amber, `value_evidence` = `UNKNOWN — requires the attested activation event` | The onboarding does **not** close. The account stays with the onboarding lead, the value gate is re-dated once, in writing, with the cause named, and the customer's business owner is asked for the attestation criterion directly |
| **NOT LIVE** | G-day evidence incomplete on or after V-day | Red, with the blocking phase and its owner named | Exec-sponsored recovery (Step 3, Recovery mode). Run the §5 handoff test before any renewal or expansion motion |

**Amber and red are not a reason to withhold the record.** They are the reason it exists. The
worst version of this failure is a first-term account with no risk record at all, because the
implementation never reached the event that was supposed to open one.

---

## 5. The Failed-launch handoff to churn-risk

The *Failed launch* compound pattern lives in `churn-risk`, and it fires from **this skill's**
instrumentation, not from renewal-window analysis. The signals are the same signals under two
sets of names:

| This skill (Step 7) | `churn-risk` | What it measures |
| --- | --- | --- |
| **S2** TTFV overrun | **U9** | `actual_elapsed / target_ttfv_days` > 2.0, or no value event by day 90 |
| **S1** Milestone slippage | **U10** | ≥2 milestones overdue, or cumulative slip > 30d |
| **S8** Services burn ratio | **U11** | `hours_burned / hours_sold` > 1.3, or ≥2 change orders |
| **S6** Dark account | **Z4** | Zero qualifying core events since `contract_start`, past day 60 |

Lead time is **180–365 days, and it predicts the first renewal specifically.** That is the whole
point: the pattern is designed to fire during the implementation, not at T-90. `churn-risk` also
fires it independently at its day-60 gate — first term, activation event never observed — which
is the same finding arriving from the other direction.

**The handoff payload**, written into the risk record and passed to `churn-risk` verbatim:

```
pattern            Failed launch (P0)
fired_on           <date the fourth signal crossed>
signals            S2 <value> · S1 <value> · S8 <value> · S6 <value>   → U9 · U10 · U11 · Z4
lead_time          180–365 days to the first renewal decision
decision_date      <opt_out_deadline>
account_state      NOT LIVE | LIVE, NOT VALUED
play               Exec-sponsored recovery with a re-baselined go-live and a stated cause.
                   Consider a term restart or extension, not a renewal ask.
withheld           Renewal motion · expansion ask (R8) — with the reason stated, not omitted
```

**What must not happen when this fires:** a normal renewal motion. The account is not a renewal
that needs better positioning; it is an implementation that has not delivered, and running a
commercial conversation over it converts a recoverable services problem into a churn. R11 binds
here too — the recovery conversation and any commercial ask are different meetings.

---

## 6. Refusals

This skill refuses to emit, in every mode:

1. **A risk record opened at G-day.** The date is wrong and the record is about the wrong event.
   Where the two dates coincide in a plan, that is a planning error to fix, not a shortcut.
2. **"Onboarding complete" on an unattested V-day.** The status is `LIVE, NOT VALUED`, with the
   named customer owner and the date the attestation was asked for.
3. **A steady-state handover section with no risk record above it.** The receiving CSM inherits
   the record or the handover has not happened — it has only been scheduled.
4. **An expansion recommendation before the record opens `VALUED`** (R8, and R9's 3× rule cannot
   be evaluated without value evidence). State that it was withheld and why.
5. **A quiet re-baseline.** Moving V-day is a decision with an owner, a date and a stated cause,
   written into the record (R14). A silently moved gate is the mechanism that manufactures
   first-renewal churn, because it removes the only date that would have exposed the problem.
6. **A renewal probability.** Ordering and bands only, until `calibrate.py` has a first-term
   cohort to backtest against (R22).

---

## 7. Worked example

Northwind. `contract_start` 2026-07-01 · `renewal_date` 2027-06-30 · `notice_period_days` 60 ·
`target_ttfv_days` 120 · activation event: monthly close completed in the platform, two
consecutive cycles.

```
opt_out_deadline       2027-05-01      (renewal − 60d, R1)
evidence_window        60d  [P]        (mid-market)
V-day candidates       opt_out − evidence  = 2027-03-02
                       start + target_ttfv = 2026-10-29   ← earlier, so V-day = 2026-10-29
value_lag              60d              (two monthly close cycles, not the 14d default)
G-day                  2026-08-30

decision_window        2026-07-31  →  2026-10-29
V-day vs window        2026-10-29 = the close of the window, to the day
verdict                DECIDED ON EVIDENCE — with zero margin. One slipped close cycle moves
                       the renewal view to faith. Float is the whole story on this account.

risk_record.opened_at  2026-10-29 (V-day), whichever state it lands in
```

Read that last line as the plan's real deadline. The float number in Step 5 is not a project
metric — it is the number of business days between this implementation and a first renewal
argued without evidence.
