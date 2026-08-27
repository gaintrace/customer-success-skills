# Champion Risk

> A champion leaves in two stages. The first is a decision they made months ago and told
> nobody about, and it is visible in behaviour the whole time. The second is a hard bounce,
> and by then the average vendor has 48 hours of goodwill and no context.
>
> This file covers both stages: the leading indicators with their thresholds and their false
> positives, the confirmation set for a departure that already happened, and the day-by-day
> 30-day succession play. Signal IDs (`R1`, `R4`, `Z1`) refer to
> `../../cs-context/references/signal-library.md`.

**Contents**
- [1. What the numbers say, and how far to trust them](#1-what-the-numbers-say-and-how-far-to-trust-them)
- [2. Leading indicators — months before the bounce](#2-leading-indicators--months-before-the-bounce)
- [3. Confirmation — a departure that already happened](#3-confirmation--a-departure-that-already-happened)
- [4. The champion risk score](#4-the-champion-risk-score)
- [5. Pricing the exposure](#5-pricing-the-exposure)
- [6. The 30-day succession play](#6-the-30-day-succession-play)
- [7. The executive-change variant](#7-the-executive-change-variant)
- [8. The promotion case — the one that inverts](#8-the-promotion-case--the-one-that-inverts)
- [9. Working and failing signals](#9-working-and-failing-signals)
- [10. Anti-patterns](#10-anti-patterns)

---

## 1. What the numbers say, and how far to trust them

| Finding | Source | Label | How to use it |
| --- | --- | --- | --- |
| ~51% of accounts churn within 12 months of a champion departure | Sturdy AI, conference presentation; methodology unpublished | `[V]` | As a planning multiplier for ranking, never as a stated churn probability |
| ~65% of accounts experiencing an executive change do not renew | Sturdy AI, same source | `[V]` | Escalate an executive change harder than a champion departure |
| Acting within the first 48 hours associated with being ~33% more likely to renew | Sturdy AI, same source | `[V]` | Justifies the 48-hour clock in §6, which is the operationally useful part |
| 20–30% of B2B contacts change job per year; 2–4% per month | UserGems, 2026 | `[V]` | The base rate for `p_departure` before any account-specific evidence |
| Organisations with >80% of projects carrying actively engaged executive sponsors reported 76% project success vs 46% where fewer than half did | PMI, Pulse of the Profession | `[A]` | The argument for an exec sponsor programme, made to your own leadership |

**Treat every `[V]` figure above as directional.** They are vendor findings without published
methodology. They are good enough to rank accounts and to justify a 48-hour clock; they are
not good enough to put a percentage in front of a customer, and they are not a substitute for
backtesting your own churn outcomes against your own departure events. When you have that
backtest, replace these numbers and cite it.

## 2. Leading indicators — months before the bounce

Each is measured **against the contact's own baseline**, never against a fixed population
threshold. A person who has always replied in three days has not disengaged by replying in
three days.

### 2.1 Title change

| | |
| --- | --- |
| **Detection** | Enrichment or job-change feed · `contact.title` history · email signature change · a new title in a meeting introduction |
| **Threshold** | Any change. A lateral move out of the function that owns us is as significant as a departure |
| **Lead time** | 30–180 days to full disengagement |
| **Reading** | Three cases, and they are not the same. **Promotion within the buying centre** → influence up, engagement down; recruit their successor as the operator and keep them as sponsor. **Lateral move out of our function** → their vested interest is gone even though they are still employed. **Title inflation with no scope change** → usually nothing |
| **False positive** | Company-wide title harmonisation after a merger or a levelling exercise. Check whether several contacts changed on the same date |
| **Action** | Confirm the scope change out loud on the next call. "Does this still sit with you, or has it moved?" costs one sentence |

### 2.2 Reduced participation

| | |
| --- | --- |
| **Detection** | `interaction` count per contact per 90d against their own trailing 12-month mean |
| **Threshold** | ≥50% decline sustained over two consecutive months, with no seasonal explanation |
| **Lead time** | 60–180 days |
| **False positive** | A genuine project ending, parental leave, a quarter-end crunch, or the account simply reaching steady state. Check whether *their* team's usage also fell — if usage held and participation dropped, it is them, not the account |
| **Action** | Move one working session into their calendar with a concrete deliverable attached. Attendance is the test, not the reply |

### 2.3 Delegation of routine work

| | |
| --- | --- |
| **Detection** | A new name appears on threads the champion used to answer · ticket submissions transfer to a junior · they reply "looping in X" more than once in 60 days |
| **Threshold** | ≥2 delegations of work they previously did themselves, inside 60 days |
| **Lead time** | 60–150 days — often the **earliest** reliable indicator, and the most ignored |
| **Reading** | Delegation is ambiguous on its own and decisive in combination. Paired with a title change it is a handover. Paired with declining acceptance it is disengagement |
| **False positive** | Healthy scaling — they hired someone and are giving them the work. Distinguish by whether the champion still attends the strategic conversations. If they delegate the routine *and* the strategic, that is not scaling |
| **Action** | Onboard the delegate properly (see `coverage-plays.md` §5) and treat them as a champion candidate. Either reading produces the same first move, which is why this indicator is safe to act on early |

### 2.4 Calendar decline rate

| | |
| --- | --- |
| **Detection** | Calendar `responseStatus` per contact: accepted / declined / no response, plus reschedules |
| **Threshold** | Acceptance below 60% over 90 days, or ≥2 consecutive declines or no-shows. ≥3 is severe |
| **Lead time** | 60–180 days |
| **False positive** | A different calendar system that under-reports responses; an assistant now triaging their diary; a genuinely brutal quarter. Weight the **trend** over the level |
| **Action** | Change the meeting, not the frequency. A 15-minute session with one decision in it is accepted far more often than a 45-minute review |

### 2.5 Email reply latency

| | |
| --- | --- |
| **Detection** | `interaction.response_latency_hours`, median per contact over 60 days against their own prior 90-day median |
| **Threshold** | >2.0× their own baseline, or median >72h where it was <24h |
| **Lead time** | 45–150 days |
| **False positive** | Our email started going to spam — check delivery and open telemetry before concluding anything. Also holidays, and a change in their inbox tooling |
| **Action** | Test the channel, not the person: if a Slack Connect message or a phone call gets a same-day answer, the relationship is intact and the channel is broken |

### 2.6 The composite that matters

Any **two** of the above, present simultaneously on the same contact, is worth more than any
one of them at a severe level. The characteristic pre-departure pattern is *delegation +
declining acceptance*, with latency rising quietly underneath. Aggregate account health is
green throughout, because none of this is account-level data.

## 3. Confirmation — a departure that already happened

| Signal | Strength | Field | Disconfirming test — run it first |
| --- | --- | --- | --- |
| Hard bounce (DSN 5.1.1 / 5.1.10) | **Near-certain** | `contact.email_status = hard_bounce` | Do other contacts at the same domain also bounce? (Domain or MX migration.) Is there an out-of-office in the bounce body? A forwarding address? A quota rejection is a soft bounce, not a departure |
| Auto-reply naming a successor | **Near-certain** | Bounce body / auto-responder text | None needed — this is the best possible outcome. Capture the successor's name immediately |
| SSO or product account deactivated | Strong | `contact.last_seen_product` plus an admin deprovisioning event | A licence reclamation exercise, or a role change within the same company |
| Removed from the shared Slack Connect channel | Strong | Channel membership event | A workspace migration or channel cleanup |
| Ticket ownership reassigned in bulk | Strong | `ticket.contact_id` reassignments | A support-process change on their side |
| Job-change feed / enrichment flag | Strong | Enrichment `job_change_detected` | Feeds lag and misfire; corroborate with one other signal before acting on it alone |
| Calendar invites auto-declining | Moderate | `responseStatus = declined` on every future occurrence | Out-of-office set for leave |
| AP or invoice contact silently changed | Moderate | `invoice` contact history | A routine finance reorg |

**The standard for asserting departure.** Two independent signals, or one near-certain signal
with its disconfirming test run and recorded. Write it as an inference with its rule:

> **Champion departure (inferred).** Email to m.bell@ hard-bounced 2026-08-11
> `[Gmail · delivery status]`; their product account was deprovisioned 2026-08-12
> `[Amplitude · contact.last_seen_product]`; they were the sole customer participant on 7 of
> the last 9 interactions `[interaction · 180d]`. **Rule:** hard bounce + directory removal +
> sole primary contact ⇒ departure, not absence. **Falsified by:** an out-of-office in the
> bounce body, a forwarding address, or a domain migration affecting other contacts.

## 4. The champion risk score

Score 0–10, cap at 10. **≥6 means act this week; a hard bounce means act today.**

| Factor | Points | Field / detection | Note |
| --- | --- | --- | --- |
| Hard bounce on the champion or economic buyer | 4 | `contact.email_status` | Treat as confirmed departure until disproven |
| Single-threaded — depth ≤1 two-way in 90d | 3 | `interaction.customer_participants` | Structural, not personal. The recovery path is what is missing |
| No observed internal advocacy in 180d | 2 | `advocacy_events = 0` | The only evidence that separates champion from coach |
| Asked for an introduction to the economic buyer; declined or deflected | 2 | Recorded on the interaction | The MEDDICC champion test `[P]` |
| Title or employer change detected | 2 | Enrichment feed, `contact.title` history | See §2.1 for which of the three cases applies |
| Login gap ≥3× their own median inter-login interval **and** ≥14 days absolute | 2 | `contact.last_seen_product` | Baseline-relative by design; a fixed threshold misfires on every low-frequency persona `[P]` |
| Customer reorg, acquisition or budget-owner change announced | 2 | News, `account.parent_account_id`, CRM | Pairs with §7 |

**Bands**

| Score | Band | Response |
| --- | --- | --- |
| 0–2 | Stable | Note it; re-check at the next QBR |
| 3–5 | Watch | Add a second contact this month; put the introduction test on the next call agenda |
| 6–7 | Act this week | Run §6 from day 1 as a precaution, without asserting a departure |
| 8–10 | Act today | Run §6 in full; escalate to the account team and to leadership the same day |

**Print every factor, fired or not.** A score of 4 that shows which six factors did *not* fire
is a useful artifact. A bare "4/10" is not.

**The score deliberately excludes the §2 leading indicators**, because delegation, acceptance
rate and reply latency are trend readings rather than confirmable events, and putting them in
the score would make it drift with sampling noise. They are handled by a separate rule instead:

> **Two or more §2 leading indicators present simultaneously on the same contact escalates to
> the "act this week" response regardless of the score.**

This is why the map prints the indicators as annotations next to the contact and the score
prints beside them. A champion at 2/10 who has been delegating since June and is accepting 45%
of invites is the exact case the score alone would miss.

## 5. Pricing the exposure

```
p_departure(h)  = 0.20 × (h / 365) × risk_multiplier            [base rate: UserGems 2026, V]
                  risk_multiplier by champion risk score:
                    0–3 → 0.75 · 4–5 → 1.5 · 6–7 → 2.5 · 8–10 → 4.0
                  result capped at 0.95
p_loss          = 0.51                                          [Sturdy AI, V]
structural      = depth 1 → 1.00 · depth 2 → 0.60 ·
                  depth 3–4 → 0.35 · depth ≥5 with a verified economic buyer → 0.20   [P]

Departure exposure ($) = ARR × p_departure(h) × p_loss × structural
Value of closing the gap = exposure at current depth − exposure at the band's target depth
```

**Worked example.** $620,000 ARR, 12-month horizon, champion risk 6, depth 3. Show the
arithmetic, report the headline at **two significant figures** (`R22` / SKILL-STANDARD §4F).

```
p_departure = 0.20 × 1.00 × 2.5            = 0.50
exposure    = 620,000 × 0.50 × 0.51 × 0.35 = $55,335   → report ~$55k
at depth 1  = 620,000 × 0.50 × 0.51 × 1.00 = $158,100  → report ~$160k
at depth 5  = 620,000 × 0.50 × 0.51 × 0.20 = $31,620   → report ~$32k
moving from depth 3 to depth 5             = $23,715   → report ~$24k
already banked by not being depth 1        = $102,765  → report ~$100k
```

The line to take to a leadership review: the account carries ~$55k of priced human dependency,
and ~$24k of it is closable by two introductions. Reproduce every figure with
`python3 ../scripts/stakeholder_score.py ../scripts/sample-account.json --today 2026-08-28 --explain DELTA`,
which prints each factor, fired or clear, and every multiplication.

**What this is not.** It is not a churn forecast, and the output must never be described as
one (`R22`). It is a consistent ranking device built on two vendor probabilities and one
convention ladder, and its whole value is that it applies the same arithmetic to every account.
Separately, `R5 · The Single-Thread Tax` applies at depth 1: the account's **full ARR** is
flagged at-risk to `churn-risk`. Exposure ranks the work; the tax governs the risk register.

## 6. The 30-day succession play

The clock starts at detection, not at confirmation. Running this on a false positive costs one
awkward sentence; not running it on a true positive costs the account.

| Day | Action | Owner | Exit criteria |
| --- | --- | --- | --- |
| 0 | Run the disconfirming tests in §3 and record the result | CSM | Departure asserted or ruled out, in writing |
| 0 | Freeze outbound sequences to that contact; nothing automated should email a departed person | CS Ops | Sequences paused |
| 0–1 | Reach the departing champion directly where they still respond — their personal channel, not the corporate mailbox. Ask two things: what changed, and who is picking this up | CSM | A named successor, or a definite no |
| 1–2 | Exec-to-exec outreach from our VP/CCO to the most senior known contact. **Not** from the CSM, and not phrased as "who replaced Marcus" | Our exec sponsor | Meeting requested |
| 1–3 | Identify the successor from data, in parallel: admin logs, ticket ownership reassignments, meeting organisers, new names on threads. Re-resolve `signs` and `decides` separately — a departure frequently moves one and not the other (`role-taxonomy.md` §3B) | CSM | Two candidate names with evidence; the triangle re-stated or marked UNKNOWN |
| 3–5 | Reconstruct the account file as if for a handover: business case, baseline, objectives, what was promised, what is outstanding | CSM | A one-page brief that assumes zero inherited context |
| 5–10 | First meeting with the successor. **Assume zero inherited context and zero inherited goodwill.** Do not present the old success plan; ask for their objectives, which may be entirely different from their predecessor's | CSM | They state an objective in their own words |
| 10–15 | Re-baseline: rewrite the success plan around the objective *they* stated, with a measure and a date | CSM | Plan agreed, not merely sent |
| 10–20 | Rebuild to ≥2 champions, **scored on mobilising capacity** (`role-taxonomy.md` §3A), not on who is warmest. The championless state is structural; replacing one person with one person recreates it, and replacing them with a supporter leaves the champion slot scoring 0.0 | CSM + AM | Depth ≥ the band target, and ≥2 contacts at `mobilising_capacity` ≥ 2 |
| 20–30 | Executive touch on the new relationship — ours to theirs, with a business-outcome briefing rather than a product update | Our exec sponsor | Meeting held |
| 30 | Re-run the map. Open a risk record that persists to the opt-out deadline regardless of how well the first meeting went | CSM | Record open at the next renewal review |

**The last row is the one teams skip.** A good first meeting with a successor feels like the
risk has closed. It has not: the risk is the missing history, and history takes two quarters
to rebuild. Keep the record open until the successor has attended a QBR and can state the
value in their own words.

**Never do these three things.** Do not ask the customer's org "who replaced X?" as your
opening — it advertises that we found out from a bounce. Do not send the departed person's
successor the old QBR deck. Do not open with a renewal ask; the first meeting buys the right
to a second one.

## 7. The executive-change variant

An economic-buyer or executive-sponsor change is a different event from a champion departure
and is scored harder — roughly 65% of accounts experiencing one do not renew (Sturdy AI) `[V]`.
A new executive runs a vendor consolidation review as a matter of routine, and incumbency is
worth less than usual because they have no ownership of the original decision.

| Difference | Champion departure | Executive change |
| --- | --- | --- |
| What is lost | Advocacy and product context | Budget ownership and the original decision rationale |
| Who acts | CSM, with exec support | Our executive, with CSM support |
| Window | 48 hours to first contact | 30 days to a briefing, before procurement starts the audit |
| The move | Re-multithread and re-baseline | Re-justify: acknowledge explicitly that they did not make this decision, and offer to make the case again |
| The mistake | Waiting for the bounce | Responding to the audit instead of getting in front of it |

Bring the quantified value evidence to the **first** meeting. A second meeting "to gather
data" wastes the only window you have, and new executives spend most of their discretionary
budget early in their tenure.

## 8. The promotion case — the one that inverts

A champion promoted **within** the buying centre is the best thing that can happen to an
account, and the standard departure play is wrong for it.

| | Departure | Promotion inside the buying centre |
| --- | --- | --- |
| Their influence | Gone | Higher |
| Their engagement | Gone | Lower — they now delegate |
| Correct move | Succession play | Convert them to executive sponsor; onboard their delegate as the new operating champion |
| The failure | Missing it | Treating the drop in engagement as disengagement and running a save play on a promoted ally |

Distinguish them with one question on the next call, and check whether the delegate arriving
on threads reports to the promoted contact — if they do, this is a promotion, not an exit.

## 9. Working and failing signals

Two weeks after starting the play, you should be able to say which of these is true.

| Working | Failing |
| --- | --- |
| A successor is named and attends a meeting within 21 days | No named successor after 30 days |
| The successor states the business objective in their own words | The successor delegates the relationship to someone junior |
| A second contact is engaged and two-way | Depth still 1 |
| Meetings are accepted at the previous rate | The first meeting is cancelled twice |
| Product usage in the champion's own team holds | The team's usage falls with the champion's departure — the value was personal, not organisational |

If the failing column dominates at day 30, this is no longer a relationship problem. Escalate
to `save-play` and treat it as a commercial event.

## 10. Anti-patterns

| Anti-pattern | Correction |
| --- | --- |
| Waiting for the hard bounce | Watch delegation, acceptance rate and latency against each contact's own baseline |
| A fixed login-gap threshold for every persona | Baseline-relative: ≥3× their own median inter-login interval and ≥14 days |
| Asserting departure from a bounce alone | Run the disconfirming tests and record them; a domain migration bounces everyone |
| Replacing one champion with one champion | Rebuild to ≥2. The championless state is structural |
| Presenting the predecessor's success plan to the successor | Re-discover their objectives; they may be completely different |
| Opening the successor relationship with a renewal ask | The first meeting buys the right to the second |
| Closing the risk after a good first meeting | Keep the record open to the opt-out deadline; the missing history takes two quarters |
| Running the succession play on a promotion | Check whether influence went up; convert them to sponsor instead |
| Quoting the 51% figure to a customer | It is unpublished vendor research. It ranks accounts internally; it does not go in an email |
| Emailing "we noticed Marcus left" | Ask who is picking up the work. Never state what you inferred from a bounce |
| Letting an automated sequence keep emailing a departed contact | Freeze sequences at detection, day 0 |
