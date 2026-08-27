# Playbook Spec — <play name>

> Emit this verbatim, with every field filled or explicitly marked
> `UNKNOWN — requires <source>`. A blank cell and a deliberate blank look identical three months
> later, and only one of them is a decision.
>
> **Internal document.** Everything above §8 contains capacity, risk and measurement language that
> must never reach a customer.

| Field | Value |
|---|---|
| Play ID | `PB-___` |
| Version · effective from | v_._ · <date> |
| Category | risk / adoption / onboarding / expansion / lifecycle / advocacy / administrative |
| Purpose, one sentence | <what changes for the **customer**, not for us> |
| Play owner (role) | <role, never a person> |
| Run owner (role) | <role resolved to a person at fire time> |
| Business-model applicability | <annual / consumption / PLG / monthly evergreen / all> |
| Modelled volume | <n>/month · <x>% of the eligible book |
| State | proposed / shadow / live / suspended / deprecated / archived |

---

## 1. Trigger

| Part | Definition |
|---|---|
| **Detect** | Source: <system> · Field: `<object.field>` · Computation: <formula> · Comparison window: <n>d · Baseline window: <n>d, excluding the most recent <n>d · Threshold: <value> · Evaluation frequency: <daily / weekly> |
| **Qualify** | Segment: <> · ARR floor: $<> · Tenure floor: <n>d · Lifecycle stage: <> · Health band: <> · Business-model mask: <> · Seasonality mask: <> · Instrumentation guard: <on/off> |
| **Route** | Owner role: <> · Precedence rank: <n> · Record written: `play_run` · Notification: <channel> |
| **Act** | Play: `PB-___` · SLA from fire: <n>h · First step: <> |

**Eligible population:** <n> accounts (<total> minus <exclusions, itemised>).
**Fire rate:** <x>% of eligible accounts per 30 days (<n> accounts) `[<source> · <window>]`.
**Band verdict:** healthy / acceptable-if-cheap / segment-not-trigger / report.
**Shadow period:** <start> → <end>. **False-fire rate on a 20-fire sample:** <y>%
— or `UNKNOWN — requires a shadow run`.
**Overlap with live plays:** <x>% of fires already covered by <play IDs>.

## 2. Suppression

Every guard listed. Write `none` where one does not apply — an omitted guard is
indistinguishable from a forgotten one.

| Guard | Rule | Rationale |
|---|---|---|
| Cool-down | <n> days, or `none (commercial-event class, R2)` | |
| Mutual exclusion (`R17`) | Suppress when a play of rank ≤ <n> is active | |
| Blackout | Open escalation · active save · live negotiation · incident +72h · onboarding in flight | |
| Instrumentation guard | Suppress if <source> volume < 70% of its trailing median in the window | |
| Health gate (`R8`) | <band floor>, or `n/a — not an expansion or advocacy play` | |
| Seasonality mask | <months / customer-specific low season> | |

## 3. Steps

| # | Action | Owner role | SLA from fire | Human/auto | Expected effect | Success measure |
|---|---|---|---|---|---|---|
| 1 | | | | | | |
| 2 | | | | | | |
| 3 | | | | | | |
| 4 | | | | | | |

**Breach behaviour:** at <n>h past SLA, notify <role>; at <n>h, <what changes — reassignment,
escalation tier, or automatic exit>.
**Never-automate check:** <which steps touch the never-automate list, and why each is human>.

## 4. Exit criteria

| Exit | Condition | Window | What happens next |
|---|---|---|---|
| **Success** | | <n> days from fire | Close, log the outcome, release the mutex |
| **Failure** | | <n> days from fire | Close, log the reason, <escalate / hand to `save-play`> |
| **No longer eligible** | Trigger condition resolved, or account state changed | continuous | Close as suppressed. Stop sending |
| **Stop-loss (`R21`)** | Spend ceiling $<> or exit date <>, save-category plays only | | Managed exit, win-back record opened |

## 5. Measurement

| Layer | Metric | Target | Source | Powered? |
|---|---|---|---|---|
| Activity | Completion rate | ≥60% | `play_run` | n/a |
| Activity | Cycle time, fire → first human touch | ≤ SLA | `play_run` | n/a |
| Activity | SLA attainment | ≥85% | `play_step_run` | n/a |
| Activity | False-fire rate | ≤20% | 20-fire sample | n/a |
| Leading outcome | <behaviour, vs the account's own baseline, in a stated window> | | | <n per arm> |
| Retention delta | Renewal rate, treated vs control | | | <n per arm, or **not powered**> |

**Control design:** 10% holdout randomised at fire time / matched historical control / none — no
causal claim made.
**Holdout exclusions:** <Critical band, ARR above $<>>, which biases the estimate toward the
treatable middle.
**Months to power at the current fire rate:** <n> — from `../scripts/play_sizing.py`.
**Claim permitted, verbatim (`R22`):**

> <The exact sentence anyone may write about this play's effect. Where there is no control:
> "Accounts that ran this play renewed at X%; accounts meeting the trigger that did not run it
> renewed at Y%. Assignment was not randomised, so this is an ordering, not an effect.">

## 6. Kill criteria

| Kill trigger | Threshold | Reviewed | Action |
|---|---|---|---|
| Fire rate outside the designed band | 2 consecutive cycles | Monthly | Retune once, then retire |
| Completion rate below 60% | 2 consecutive cycles | Quarterly | Fix capacity or retire |
| Leading outcome indistinguishable from control | After the powered window | Quarterly | Retire |
| Root cause fixed, or superseded | Any cycle | Quarterly | Retire or merge |
| Owner role vacant | 1 cycle | Monthly | Suspend |
| Never fired | 2 quarters live | Quarterly | Retire |

## 7. Not covered this cycle (`R14`)

| Excluded population | Exclusion rule | Why | Revisit |
|---|---|---|---|
| | | | |

## 8. Customer-facing step content

Only where a step sends something. Where every step is internal, write
`No customer-facing content — steps 1–4 are internal` and delete the block below.

════════════════════════════════════════════════════════════
CUSTOMER-FACING — copy the block below and send as written.
Everything above this line is internal. Do not forward it.
════════════════════════════════════════════════════════════

```text
Subject: <2-4 words, factual, reads like an internal note from a colleague>

Hi <their first name>,

<The observation this trigger detected, stated as a fact, with the number and the month in
it, and no preamble.>

<What that costs or is worth to them, in their language, with arithmetic they can check in
their own systems.>

<The ask, phrased as a question they can answer yes to, with two real dates in it.>

<Sign-off>
<Sender first name>
```

**Merge-field contract.** An automated play sends this hundreds of times, so every field is
specified here rather than discovered in production. A field with no fallback and no suppression
rule is an unfilled placeholder waiting to send.

| Field | Source | Fallback if null | Suppression rule |
|---|---|---|---|
| `<their first name>` | `contact.name` | — | Suppress the send |
| `<the number>` | `<system · field>` | — | Suppress the send |
| `<the month>` | derived from the trigger window | — | Suppress the send |
| `<sender first name>` | `account.owner_csm` | Regional CS lead | Suppress if both null (`R19`) |

**Leak scan (`R18`) — confirm each before this play goes live:**

- [ ] No health score, risk score or band, in any wording
- [ ] No ARR at risk, exposure, forecast category or renewal probability
- [ ] No play, sequence, save-play or war-room language
- [ ] No coverage tier, book size or segment label
- [ ] No inference about a named person ("we noticed X left", "since your champion moved on")
- [ ] No competitor intelligence the customer did not raise
- [ ] No date the sender does not own (`R19`)
- [ ] Every sentence fails the forty-customer test — it could not be sent to any other account
- [ ] Plain text only: blank lines between paragraphs, `•` bullets, no headings, no tables, no bold

Written to `../../cs-context/references/customer-voice.md`.

---

## Change log

| Version | Effective | Author | Change | Reason | Measurement window reset |
|---|---|---|---|---|---|
| 1.0 | | | Launch | — | n/a |

## Rule deviations

| Rule | Circumstance that makes it wrong here | What will be watched |
|---|---|---|
| | | |

<Delete this section only when the play deviates from nothing. A rule broken on the record is a
judgement call; a rule broken silently is the thing the rule existed to prevent.>
