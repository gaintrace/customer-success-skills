# The Risk Scoring Model

> How each of the seven signal families is scored 0–100 **risk** (higher = worse), how the
> families combine, and how to defend the model when someone challenges it.
>
> Note the polarity. `churn-risk` scores **risk**; `health-score-designer` scores **health**.
> They are inverses (`health ≈ 100 − risk`) but not interchangeable, because the override
> floors and the compound-pattern escalation have no health equivalent. Always state which
> one a number is.
>
> Labels: `[PROD]` = a published production configuration · `[M]` measured · `[V]` vendor ·
> `[P]` practitioner rule of thumb · `[DESIGN]` = a design choice in this library, defensible
> but not measured. Calibrate `[DESIGN]` values against your own outcomes before trusting them.

**Contents**
1. [Principles](#1-principles)
2. [Family-level rubrics](#2-family-level-rubrics)
3. [Weight profiles](#3-weight-profiles)
4. [Combination, renormalisation and floors](#4-combination-renormalisation-and-floors)
5. [Worked example](#5-worked-example)
6. [Calibrating and defending the model](#6-calibrating-and-defending-the-model)
7. [Business-model profiles — what each one changes](#7-business-model-profiles--what-each-one-changes)

> **Craft codes.** `[C21]` silence over complaint · `[C22]` calendar over content ·
> `[C23]` the renewal is decided in months 2–4 · `[C24]` frictionless is not clean.
> Definitions in `../../cs-context/references/practitioner-craft.md`. They appear below as
> scored components and floors, never as advice.

---

## 1. Principles

| Principle | Why |
| --- | --- |
| **Score relative to the account's own baseline, not an absolute threshold.** | A weekly-cadence account that stays weekly is healthy. A daily account that drops to weekly is churning. Absolute floors on relative metrics are the most common defect in CS scoring. |
| **Use medians, not means, over trailing windows.** | Survives holidays, outages and single-week spikes without smoothing away real decline. |
| **Return `UNKNOWN`, not zero, when there is not enough data.** | Requiring `base ≥ 20 events` before computing a trend prevents a spurious −100% on a low-volume account. |
| **Renormalise over measured families.** | Treating a missing family as zero risk is how a data gap manufactures a green account. |
| **Cap any single family's influence.** | No family above 25% of the composite in the enterprise profile — otherwise the score is a proxy for one metric wearing seven hats. |
| **Require at least one relationship family and one value family.** | A composite driven entirely by usage can be satisfied by a single power user and tells you nothing about whether anyone will sign. |
| **Zero is not always good.** | Zero support tickets is disengagement, not health. Several sub-scores are U-shaped, not monotonic. |
| **Ramp accounts are scored differently.** | Suppress usage-decay scoring for accounts under 90 days past go-live; score them on onboarding criteria instead. |
| **Explainability is a requirement, not a nicety.** | A score without a reason code is ignored, and an ignored score is worse than none — it creates the appearance of coverage. |

---

## 2. Family-level rubrics

Each family produces a 0–100 risk sub-score. Sub-scores are computed from the signals in
`../../cs-context/references/signal-library.md`; the IDs below refer to that file.

### 2.1 Product usage & adoption

| Component | Formula | Risk mapping |
| --- | --- | --- |
| **Usage trend** (U7 core actions) | `base = median(weekly core_actions, wk t-12…t-5)`; `recent = median(wk t-3…t)`; `trend = (recent − base) / max(base, ε)`. Require `base ≥ 20` events or return `UNKNOWN`. | `trend ≥ +0.10 → 0` · `−0.10…+0.10 → 25` · `−0.25…−0.10 → 50` · `−0.50…−0.25 → 75` · `< −0.50 → 100` |
| **Licence utilisation** (U4) | `util = active_users_30d / seats_purchased` | `≥0.90 → 0` · linear to `0.50 → 100`. GitLab's published config uses ≥90% as a seat-expansion trigger and <75% as seat-reduction risk, explicitly excluding accounts still onboarding `[PROD]` |
| **Active-user penetration** | `UMAU_ratio = unique_monthly_active_users / billable_users` | `≥0.80 → 0` · linear to `0.30 → 100` `[PROD]` |
| **Adoption breadth** (U6) | `(value features used ≥1× in 30d) / (entitled value features)` where the value-feature list is 5–12 features derived from a retention-vs-feature analysis, **not** from the full catalogue | `≥0.60 → 0` · linear to `0.20 → 100`; fewer than 3 features used → floor of 60 |
| **Activation state** (U8) `[C23]` | Has the activation event from `cs-context` §5 ever fired? Has it fired in the last `2 × historical median interval`? | Never fired past day 90 → **100**. **Never fired past day 60 in a first term → 90 and Failed launch fires immediately**, regardless of how far the renewal is. Regressed → 75. Current → 0 |
| **First-term day count** `[C23]` | `days_since_contract_start`, computed for every account inside its first term before any renewal-window filter is applied | Not scored directly — it is the **gate**. Days 60–120 with no activation is the window in which the first renewal is actually decided; a risk record opened at T-90 instead is opened after the decision |
| **Buying-team usage** | The same trend computation, restricted to the department named in the contract or original business case | Scored separately and reported separately. Never averaged into the aggregate — that is the mechanism that hides Buyer disconnect |

**Family sub-score** = max(usage trend, activation) weighted 0.5, plus mean(utilisation,
penetration, breadth) weighted 0.5. Using `max` on the first pair is deliberate: an account
that has never activated is at risk regardless of how its trend looks.

### 2.2 Commercial & contract

Largely **decision** signals rather than indicators, which is why this family carries the
highest weight in the enterprise profile and why most of the override floors live here.

| Component | Risk |
| --- | --- |
| Auto-renew switched off (C1) | 100 — and it fires an override floor |
| Notice served / termination language requested (R12) | 100 — floor |
| Seat reduction ≥25% during the term (C3) | 85 |
| Term shortened at last renewal (C5) | 70 |
| Procurement re-engaged outside a renewal window (R11) | 70 |
| Competitor named in any channel (R13) | 60 |
| Discount expiring at this renewal with no value case built | 55 |
| Days to opt-out < 30 with no renewal conversation held | 100 — floor |
| Days to opt-out 30–90 with no renewal conversation held | 60 |
| Downgrade requested | 75 |
| **Negotiation friction `frictionless`** `[C24]` — renewal agreed or closing with no counter, no redline, no procurement involvement — **and** relationship-family risk ≥50 or engaged contacts below the segment target | **30 band floor (Watch)** and the Frictionless renewal pattern. Never 0 |
| Negotiation friction `contested` — counters, redlines, procurement pressure, a fought discount | 0–15. Argument is engagement. A customer who negotiates hard has a stake in the outcome |
| None of the above, opt-out > 120 days out, conversation on track | 0–15 |

**Negotiation friction is a required field on every account**, valued `contested` /
`routine` / `frictionless` / `UNKNOWN — requires <CRM opportunity or CLM history>`. It is the
only field in this family that can *lower* nothing and only ever raises the floor: an
uncontested close is scored as an absence of stakeholders, not as agreement `[C24]`.

Take the **maximum**, not the mean. Commercial signals are events; averaging an auto-renew
switch-off against a clean payment history is meaningless.

### 2.3 Relationship & engagement

| Component | Formula | Risk mapping |
| --- | --- | --- |
| **Engagement recency** (Z1) | `s = 100 × (1 − exp(−ln2 × days_since_bilateral_touch / HL))` where `HL` = the segment's expected cadence in days | At exactly one cadence period the score is 50 — a clean, defensible anchor. GitLab's published tiers: Priority-1 green ≤35d, yellow 36–60, red >60; Priority-2 green ≤65, yellow 66–90, red >90 `[PROD]` |
| **Multithreading** (R4) | `engaged_contacts_90d / target`, where target = Enterprise 6 · Mid-Market 3 · SMB 2 `[DESIGN]`. "Engaged" means ≥1 *two-way* interaction | `≥1.0 → 0`, linear to `0 → 100`. **Require persona coverage as well as count** — economic buyer + champion/admin + end user. A count without persona coverage is trivially gamed by adding low-value contacts |
| **Champion status** (R1) | active / weakened / departed | departed → 100 · weakened → 60 · active → 0 |
| **Exec sponsor** (R2) | Named and met in the last two quarters? | absent → 80 · named but not met → 50 · engaged → 0 |
| **Reply latency trend** | 30d mean vs prior 90d mean | >2× slower → 60 · 1.5–2× → 35 · stable → 0 |
| **QBR cadence** (R6) | Held per the segment's designed cadence? | Two consecutive missed → 70 · one missed → 40 · on cadence → 0 |
| **Acceptance latency** (R5) `[C22]` | `median(accept_timestamp − invite_timestamp)` over L90, against the account's own L365 baseline | >3× baseline or >5 days where it was <1 → 70 · 1.5–3× → 40 · at baseline → 0. Requires ≥4 invitations or `UNKNOWN` |
| **Reschedule count** (R5) `[C22]` | `reschedules + declines` on scheduled meetings over L90, and whether any two were **consecutive** | ≥2 consecutive by the economic buyer → **fires the 60 floor on its own, with no usage decline required** · ≥3 by anyone → 70 · 2 by anyone → 45 · 0–1 → 0 |
| **Who accepts** (R5) `[C22]` | The seniority of the person who actually accepts, named. Delegation down the org chart is the earliest reliable withdrawal signal | Economic buyer accepts → 0 · champion only → 30 · delegate below the buying centre → 60 · nobody accepts, meeting held with our side only → 85 |

**Family sub-score** = max(champion status, exec sponsor) weighted 0.5 + mean(recency,
multithreading, latency, QBR) weighted 0.5. Again `max` on the first pair: a departed champion
is not offset by good meeting hygiene.

Only count **bilateral** interactions. Outbound emails nobody answered are not engagement, and
counting them is how a relationship score stays green through a year of silence.

**The calendar three-tuple is mandatory output** `[C22]`: acceptance latency · reschedule count
(90d) · who accepts, named. Score the calendar before scoring anything said in the meeting —
acceptance latency, reschedule count and who accepts predict disengagement earlier and more
reliably than transcript sentiment, because a customer withdrawing politely still answers the
question in the room. Where no calendar source is connected, print
`UNKNOWN — requires a calendar source (Google Workspace / Microsoft 365)` for all three and
mark the relationship family Partial in the Coverage Ledger. Never omit the line.

### 2.4 Support & reliability

Three refinements over raw ticket counts, all of them necessary:

1. **Normalise per 100 seats** — `tickets_norm = tickets_30d / (seats / 100)` — or every large account is red.
2. **Zero tickets is not green** `[C21]`. Score as a U-curve, not monotonically: 0 tickets → risk 40 · healthy band → 0 · heavy volume → 80. Silence is louder than complaint — a customer who stops raising issues has usually stopped expecting resolution, and the collapse after the spike is the signal, not the spike.
3. **Prefer higher-signal features over volume**: reopen rate, P1 count in trailing 90d, age of the oldest open ticket, distinct escalation events, CSAT trend on resolved tickets.

| Component | Risk |
| --- | --- |
| Open P1 >14 days with exec visibility (P5) | 100 — floor |
| Repeat issue ≥3 occurrences (P3) | 80 |
| Reopen rate >20% over 90d | 70 |
| SLA breach in the last 90d | 60 |
| Blocking feature request rejected (P9) | 55 |
| Ticket volume spike then collapse within 30d (P2) `[C21]` | 85 — and it is the Quiet quit trigger, tested before the account is read as stabilised |
| Zero tickets in 90d on an account with >20 seats `[C21]` | 40 — never 0. A quiet quarter is scored as disengagement until the resolution notes say otherwise |
| Normalised volume in the healthy band, no escalations, CSAT stable | 0–15 |

### 2.5 Sentiment & VoC

| Component | Risk |
| --- | --- |
| NPS detractor (0–6) within 90 days | 80 |
| NPS passive (7–8) within 90 days | 40 |
| NPS promoter (9–10) within 90 days | 0 |
| CSAT trend declining across ≥3 resolved tickets | 60 |
| Any survey response older than 90 days | Treat as **UNKNOWN**, not as its original value |
| Negative sentiment in call transcripts or email threads (labelled inference) | 55 |
| CSM sentiment (human input) | Constrain to red/amber/green with a **mandatory written justification and timestamp**. Free-form 1–10 sliders produce uncalibrated noise across CSMs |

Two cautions on sentiment. GitLab's production config gives CSM sentiment a hard veto — red
sentiment forces the overall score red `[PROD]`. TSIA has asserted the opposite, that heavily
weighting CSM sentiment correlates with *worse* retention because bias masks real signals —
that is a blog assertion with unpublished methodology, so treat it as a hypothesis to test
against your own outcomes, not a fact. This library's default weight for sentiment is
deliberately low (9) with no veto, and the resolution is empirical: backtest both.

Also: a single detractor in an account with two respondents is not an account NPS. Require
≥3 responses or ≥20% of active users, whichever is smaller, before scoring the family at all.

### 2.6 Billing & payment

| Component | Risk |
| --- | --- |
| Invoice disputed or unpaid >60 days | 90 |
| DSO deteriorating vs the account's own history (C8) | 65 |
| Repeated payment failures (≥2 in 180d) | 70 |
| Payment method expired or removed | 60 |
| Single late payment | 20 |
| Clean history | 0 |

For SMB and PLG this family matters far more than the enterprise weight suggests — Recurly's
subscription-network data shows involuntary churn of 1.30% monthly at $10–25 ARPC against
0.18% at $250+ `[M]`. Use the PLG profile.

### 2.7 Firmographic & external

| Component | Risk |
| --- | --- |
| Customer acquired or merged (F1) | 70 |
| Executive change in the buying centre (F2) | 65 |
| Layoffs affecting the using department (F3) | 70 |
| Financial distress: down round, missed filings, credit downgrade (F4) | 75 |
| Hiring freeze or headcount decline | 40 |
| Growth: funding, headcount growth, new product launch | 0 — and it flags to `expansion-finder` |
| No external events detected | 0, but only if a source is actually connected — otherwise `UNKNOWN` |

The commonest error here is scoring this family 0 when no external data source exists. If
nothing is connected, the family is **Missing**, not clean, and it must appear that way in the
Coverage Ledger.

---

## 3. Weight profiles

| Family | Enterprise / annual | PLG / monthly | Consumption / usage-based |
| --- | --- | --- | --- |
| Product usage & adoption | 22 | 35 | 30 |
| Commercial & contract | 25 | 15 | 20 |
| Relationship & engagement | 20 | 10 | 15 |
| Support & reliability | 12 | 13 | 12 |
| Sentiment & VoC | 9 | 10 | 8 |
| Billing & payment | 7 | 12 | 10 |
| Firmographic & external | 5 | 5 | 5 |

**Choosing a profile.** Enterprise/annual where there is a notice period, a procurement
function and a named champion — commercial actions are decisions and outweigh usage dips.
PLG/monthly where the product *is* the relationship, cancellation is self-service and
instantaneous, and involuntary churn is material. Consumption where the metered unit is the
revenue, so consumption pacing replaces seat utilisation as the primary leading metric and
"churn" often appears as commitment reduction rather than logo loss.

Segment-mixed books: score each account with its own profile. Do not average the profiles.

---

## 4. Combination, renormalisation and floors

```
1. family_risk[f]  ∈ [0,100] or UNKNOWN,  for each of the 7 families
2. weighted        = Σ(family_risk[f] × weight[f]) / Σ(weight[f] where family_risk[f] ≠ UNKNOWN)
3. after_patterns  = min(weighted + 10 × min(patterns_matched, 2), 100)
4. final           = max(after_patterns, highest override floor that fired)
5. band_floor      = Watch if Frictionless renewal matched  →  final = max(final, 30)   [C24]
6. escalate        = true if any P0 compound pattern matched, regardless of `final`
7. gate            = first term and no activation by day 60  →  Failed launch fires now,
                     and no renewal plan is written for this account                    [C23]
8. coverage        = measured_families / 7   →   confidence cap
```

Step 2's renormalisation is the important one. If sentiment and firmographic are both missing,
the divisor is 86, not 100 — the remaining families carry proportionally more weight rather
than the gaps quietly voting "healthy".

Step 5 is a **band floor, not a score floor**: it does not claim the account is at 30 risk, it
forbids reporting it Secure. An uncontested renewal from an org with no engaged contacts is the
absence of anyone with a stake, and the additive score reads that absence as calm `[C24]`.

Step 6 exists because steps 2–4 are additive, and additive models under-rank compounds by
construction. The pattern escalation is the correction.

Step 7 is a **refusal**, not a score. Where the activation event has never fired inside the
first term, the artifact withholds the renewal plan and names the unlocking milestone. A T-90
renewal plan on a failed implementation negotiates from a position already lost `[C23]`.

**Bands**

| Score | Band | Midpoint used for exposure |
| --- | --- | --- |
| 0–24 | Secure | 0.05 |
| 25–44 | Watch | 0.15 |
| 45–64 | At Risk | 0.35 |
| 65–84 | High Risk | 0.60 |
| 85–100 | Critical | 0.85 |

These midpoints are `[DESIGN]` stated probabilities of a rules-based model. They are **not**
calibrated forecasts and must be presented as bands until backtested. Once you have backtested
against ≥100 renewal outcomes, replace them with the observed renewal rate per band and cite
the backtest — see §6.

---

## 5. Worked example

Acme Corp · $148,000 ARR · renewal 2026-11-01 · 60-day notice · enterprise profile · today 2026-08-27.

**Opt-out deadline:** 2026-11-01 − 60 = **2026-09-02 — six days away.** This governs everything.

**Required reads** (filled before any family is scored — omission reads as clean):

| Field | Value |
| --- | --- |
| Calendar `[C22]` | acceptance latency 9 d against a 2 d baseline (4.5×) · 3 reschedules in 90 d, **2 of them consecutive by the economic buyer** · last acceptance by a delegate outside the buying centre |
| Negotiation friction `[C24]` | `routine` — one term question, no counter. Not frictionless, so no band floor |
| First term `[C23]` | not a first term — gate not applicable, and that is printed rather than omitted |
| Support silence `[C21]` | 14 tickets in June, 0 since 12 July — spike then collapse, scored 85 |

The two consecutive buyer reschedules fire the **60 floor on their own**. They are redundant
here because auto-renew is already off at 85 — but on the same account three months earlier,
with usage still healthy, they were the only thing that would have fired.

| Family | Evidence | Sub-score | Weight | Contribution |
| --- | --- | --- | --- | --- |
| Commercial & contract | Auto-renew off 2026-08-02 `[Salesforce · Contract.AutoRenew__c]`; opt-out in 6 days, no renewal conversation held | 90 | 25 | 24.7 |
| Product usage & adoption | Core actions median 41/wk → 16/wk over 8 weeks (−61%) `[Amplitude · core_actions]`; utilisation 43% (86/200 seats) | 72 | 22 | 17.4 |
| Relationship & engagement | Champion j.chen@ hard-bounced 2026-08-11; 1 engaged contact in 90d; no exec sponsor | 65 | 20 | 14.3 |
| Support & reliability | 2 P1s breached SLA in July, both still open | 30 | 12 | 4.0 |
| Sentiment & VoC | No VoC source connected | **UNKNOWN** | — | — |
| Billing & payment | Clean; one invoice 4 days late in March | 10 | 7 | 0.8 |
| Firmographic & external | No events detected; Crunchbase connected | 0 | 5 | 0.0 |
| | | | **Σ 91** | **Weighted 61.1** |

Renormalised over 91 of 100 weight (sentiment missing).

Patterns matched: **Decapitation** (P0) and **Quiet quit** (P0) → +20 (cap) → **81.1**
Override floors fired: auto-renew off → **85**; opt-out <30d with no conversation → **70**
Highest floor **85** > 81.1 → **final 85 · Critical**

```
Exposure        = $148,000 × 0.85                     = $125,800
Urgency         = 6 days to opt-out                   = 1.5
Savability      = addressable (relationship + value)  = 1.2
Action Priority = 125,800 × 1.5 × 1.2                 = $226,440
```

**Coverage 6 / 7 (86%) → confidence High.** Blind spot: sentiment. Missing VoC most often
hides a grievance that predates the usage decline, so the diagnosis may be understating cause
even though the band is right.

**Escalate regardless** — two P0 patterns. This account goes to `save-play` today, not to next
week's review.

---

## 6. Calibrating and defending the model

You will be challenged on this model, usually by someone who has been burned by a health score
before. The defensible answers:

| Challenge | Answer |
| --- | --- |
| "Where did the weights come from?" | Stated defaults, published as `[DESIGN]`, with a profile per commercial model. They are a starting point to be replaced by weights derived from your own outcomes — see `health-score-designer` §7 for the three legitimate derivation methods. |
| "Why should I believe the 85?" | You should not believe the number; you should read the six lines under it. Every contribution, floor and pattern is printed with its evidence. A score you cannot audit is a score you should not act on. |
| "Your score said green and they churned." | Run the account through §5 of `../../cs-context/references/signal-library.md` §14 (false-positive traps) and §12 of `health-scoring`. The two structural causes of false-green are aggregate-usage masking (fixed by the buying-team split) and missing families voting healthy (fixed by renormalisation). Then feed it to `churn-postmortem` and update the lead times. |
| "Is 85 an 85% probability?" | No. It is a band midpoint of a rules-based model. Until backtested it is an ordering, not a forecast. |
| "How would you know if this model were wrong?" | Backtest: freeze features at T−90/T−180/T−270 relative to each account's renewal date, score, and compare against the actual outcome. Report PR-AUC and lift at the top decile — never accuracy, which is meaningless at 5–20% base rates. Precision must be high enough that CSMs act on the alerts; below roughly 30% they stop reading them `[P]`, at which point the system is worse than nothing. |

Recalibrate weights quarterly and retrain fully once a year. Signal weights drift with product
changes, pricing changes and segment mix `[P]`.

The baseline this model competes against is not a better model — it is the widely reported
experience of CS teams whose health score did not predict the churn that happened. That
experience is why every number here is printed with its derivation: a score nobody can audit
is abandoned the first time it misses, and the audit trail is what survives the miss.

---

## 7. Business-model profiles — what each one changes

Resolve this **before Step 1** of `../SKILL.md`, from
`../../cs-context/references/business-model-profiles.md`. It decides which signals mean anything
and — more importantly — which standard practices **do not apply**, because recommending them is
the most recognisable form of generic output.

| If the model is | Then |
| --- | --- |
| **Consumption / usage-based** | Commitment pacing (`consumed / (commitment × elapsed_term_fraction)`) replaces licence utilisation entirely. Churn appears as **shortfall, not logo loss**. Separate recurring from episodic volume — a backfill is not health. Use the `consumption` weight profile |
| **Product-led / self-serve** | There is often no champion, no exec sponsor and no QBR. Scoring their absence manufactures risk. Relationship weight drops to 10, billing rises — involuntary churn is material. No notice period exists, so detection must be pre-emptive in days. Use `plg` |
| **Monthly evergreen** | R1 does not apply as written: there is no opt-out deadline, every day is one. Score continuously on 7/14-day windows |
| **Self-hosted / on-prem / channel** | Usage telemetry may not exist at all. Coverage is structurally capped — say so rather than faking a usage read |
| **Regulated vertical** | Security review and vendor-risk cycles are renewal-timeline dependencies measured in months. Fold them into urgency |
| **Seasonal (academic, retail, public sector)** | Mask the known low season before firing any decay signal. Scoring a normal summer as risk burns credibility with the CSM who knows better |

Two craft codes survive every profile, because they are structural rather than motion-specific:

| Code | Holds everywhere because |
| --- | --- |
| `[C22]` calendar over content | Even a PLG account with no QBR has invitations, acceptances and reschedules the moment a human meeting exists. Where no meetings exist at all, print `UNKNOWN — requires a calendar source` rather than scoring the family clean |
| `[C23]` months 2–4 decide the first renewal | Time-to-value governs every model. On monthly evergreen the gate tightens rather than relaxes — the window is days 20–60, not 60–120 |

`[C24]` is suppressed on self-serve, where there is no negotiation to have friction in: record
`negotiation_friction: not-applicable — self-serve` rather than `frictionless`, and score
engagement from usage instead. `[C21]` inverts nowhere: zero support contact is scored as
disengagement in every profile, and in PLG it is the *only* relationship signal available.
