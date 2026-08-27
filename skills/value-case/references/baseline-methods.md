# Baseline Methods

> The baseline is the one input in a value case that cannot be recovered later. Everything else
> — the loaded cost, the attribution factor, the recapture rate, the exclusions list — can be
> renegotiated with the customer at any point. The pre-period cannot. Once the product is live,
> the "before" exists only where somebody's system happened to retain it.
>
> Evidence labels: `[M]` measured · `[V]` vendor-published · `[P]` practitioner convention ·
> `[A]` academic. Never present a `[P]` default or a `[V]` benchmark as a measurement of *this*
> customer.

**Contents**
- [1. Why this is the unrecoverable step](#1-why-this-is-the-unrecoverable-step)
- [2. Capture timing — the calendar](#2-capture-timing--the-calendar)
- [3. The baseline record](#3-the-baseline-record)
- [4. The defensibility ladder: B1–B4](#4-the-defensibility-ladder-b1b4)
- [5. Choosing the window](#5-choosing-the-window)
- [6. Counterfactual designs: D1–D5](#6-counterfactual-designs-d1d5)
- [7. Difference-in-differences, worked](#7-difference-in-differences-worked)
- [8. Seasonality control](#8-seasonality-control)
- [9. Recovery — no baseline, and the renewal is coming](#9-recovery--no-baseline-and-the-renewal-is-coming)
- [10. Re-baselining and the changelog](#10-re-baselining-and-the-changelog)
- [11. Failure modes](#11-failure-modes)
- [12. A full worked capture](#12-a-full-worked-capture)

---

## 1. Why this is the unrecoverable step

Three facts, in order of how much damage they do:

| Fact | Consequence |
| --- | --- |
| Most operational systems retain detail for 90 days to 13 months | By month 14 the pre-period is not "hard to get", it is gone |
| The people who knew the "before" leave | A baseline that lived in one manager's head departs with them, and their successor has no reason to believe your number |
| A number reconstructed after the fact is negotiable | A dated pre-period record is a fact. An estimate produced at T-60 is an opening position, and their finance team treats it as one |

The industry framing is blunt and worth repeating to a CSM who is tempted to skip it: the
business case that won the deal usually dies at close, so the renewal team starts with no
baseline and no agreed metric to point at `[P]`. The fix is not a better slide later; it is a
captured record now.

**The rule:** an objective with no baseline is not an objective yet. Its first milestone is
*establish the baseline*, with an owner and a date, and that milestone belongs in the onboarding
plan (`../../onboarding-plan/SKILL.md`) in week one.

## 2. Capture timing — the calendar

| Moment | What is capturable | What is already lost |
| --- | --- | --- |
| **Pre-signature** | Everything. Their own diligence usually produced numbers already — ask for the business case | Nothing |
| **Signature → kickoff** | Their systems, unchanged. The ideal window: they are motivated and the product has changed nothing | Nothing |
| **Kickoff → go-live** | Their systems, still unchanged; ours has no history yet | Nothing, provided nobody has changed process in anticipation |
| **Go-live + 30 days** | Their retained history, if the retention window covers the pre-period | Anything their system rolled off |
| **Go-live + 6 months** | Usually only aggregates and a customer estimate | Detail, segmentation, the ability to match cohorts on pre-period behaviour |
| **T-60 before renewal** | An estimate, a control group, or nothing | The measurement |

**Capture the baseline at signature or kickoff, never at renewal.** A baseline captured after
go-live is a post-hoc estimate, and every customer finance team knows the difference `[P]`.

## 3. The baseline record

One record per value driver. An objective missing any required field stays in a proposed state
and does not appear in a dollar figure. Emit `../assets/baseline-record.md` verbatim.

| Field | Required | Example | Why it matters |
| --- | --- | --- | --- |
| `value_driver` | ✅ | Support ticket deflection | The business thing, not the feature |
| `metric_name` | ✅ | Tier-1 tickets per 1,000 active accounts per month | Rate metrics survive their growth; absolute counts do not |
| `unit` · `direction` | ✅ | count · ↓ | Direction prevents an improvement being read as a decline |
| `baseline_value` | ✅ | 412 | |
| `baseline_period` | ✅ | 2026-01-01 → 2026-03-31, 3-month mean | Never a single day, never a single week |
| `baseline_source` | ✅ | Their helpdesk export, `ticket.type = tier_1`, pulled 2026-04-04 | The query, not the tool name |
| `pulled_by` | ✅ | Priya N. (customer) or J. Okafor (us) | Decides the rung: theirs is B2, ours is B1 only if instrumented |
| `measurement_owner_customer` | ✅ | Priya N., Director of Support Ops | The person who re-runs it at the measurement date |
| `unit_economics` · `source` | ✅ for a dollar figure | $18.40 loaded per Tier-1 ticket, customer-supplied, low end of their $18.40–$24 range | Without it the line can never become money |
| `target_value` · `target_date` | ✅ | 290 by 2026-12-31 | |
| `attribution_pct` · `set_by` | ✅ for a dollar figure | 70%, set by Priya N., email 2026-08-14 | Never 1.0, never set by us |
| `rung` / `design` | ✅ | B2 (their system of record) | Printed on the artifact |
| `known_confounders` | ✅ | Their knowledge-base rewrite ran Feb–May | Named now, so it cannot be discovered by their CFO later |
| `retention_window` | recommended | 13 months | Tells you when reconstruction stops being possible |
| `last_validated` | ✅ | 2026-08-14 | A baseline nobody has confirmed in a year is a historical claim |

## 4. The defensibility ladder: B1–B4

Use the highest rung available. **Label the rung on the artifact**, every time.

### B1 · Instrumented pre-period

Measured in a system, before anything changed, by us or by them.

| | |
| --- | --- |
| **How** | Instrument the metric before go-live, or extract it from a system that was already recording. Store the query. |
| **Permits** | Band up to **Measured**, and a dollar headline |
| **Requires** | ≥3 comparable periods (three months, three quarters, three close cycles). A single period cannot distinguish a level from a fluctuation |
| **Failure mode** | Instrumenting *our* product's telemetry and calling it a baseline. Our telemetry starts at zero by construction; that is not a "before", it is an absence |
| **Tell the customer** | "We are recording this before we change anything, so the number at renewal is a measurement rather than an argument." |

### B2 · Their system of record

They extract it from their warehouse, helpdesk, ERP, CRM or close calendar.

| | |
| --- | --- |
| **How** | Give them the metric definition; **they** run the query and send the result. Record who ran it and when |
| **Permits** | Band up to **Measured** |
| **The distinction that matters** | A number *we* pulled out of *their* system is still ours until they confirm it in writing. Confirmed, it is B2; unconfirmed, it is B1-with-our-name-on-it and caps at Evidenced |
| **Failure mode** | Accepting a screenshot with no query behind it. At the measurement date nobody can reproduce it, and the delta becomes unverifiable |
| **Tell the customer** | "Run it your way and send me the number — I would rather use yours than mine." |

### B3 · Customer-stated estimate, method recorded

A named person's figure, with the method they used, at the low end of any range.

| | |
| --- | --- |
| **How** | Ask *how* they arrived at it, and write the method down verbatim next to the number |
| **Permits** | Band up to **Attested** — never **Measured** |
| **The low-end rule** | Always use the bottom of a supplied range. "Priya estimates 6–9 hours; we use 6" is defensible. Using 9 makes every later number suspect `[P]` |
| **Good method note** | "Six hours: she timed the Thursday reconciliation twice in March and rounded down" |
| **Bad method note** | "About a day, she thought" |
| **Failure mode** | Recording the number and losing the method, which turns a defensible estimate into an unsourced one at the next refresh |

### B4 · Industry proxy with an explicit haircut

Last resort. Illustrative only.

| | |
| --- | --- |
| **How** | Name the published source and year, apply a stated haircut (a 50% haircut is the usual practitioner default `[P]`), and label the line **estimate** on the artifact |
| **Permits** | **No dollar headline.** It may size a hypothesis or frame a conversation. It may not appear as delivered value |
| **Failure mode** | The proxy quietly becomes the number. Six months later nobody remembers it was a benchmark, and their CFO discovers it in a footnote |
| **Tell the customer** | "This is an industry figure, not yours. It tells us the size of the prize; it does not tell us what you got. Here is what we would need to measure it properly." |

**The hard rule: never present a proxy as a measurement.** This is the single most expensive
mistake available in this skill, because the loss is not the number — it is every future number.

## 5. Choosing the window

| Question | Rule |
| --- | --- |
| **How long?** | Three comparable periods minimum. For anything with a monthly cycle, three months; for a close process, three closes; for an annual cycle, the same calendar quarter last year |
| **Mean or median?** | Median where the metric has spikes (incidents, campaigns, quarter-end). State which you used |
| **Which periods to exclude?** | Any period containing a known one-off — a migration, an outage, a strike, a peak season — and **say you excluded it**. A silently trimmed window is indistinguishable from cherry-picking |
| **Rate or count?** | Rate wherever their business is growing. "Tickets per 1,000 accounts" survives a 40% headcount increase; "tickets per month" does not |
| **Whose data grain?** | The team named in the hypothesis, not the account. Account aggregates hide the team the value was promised to |

## 6. Counterfactual designs: D1–D5

A baseline tells you what changed. A design tells you what would have happened anyway. Where
both exist you have a defensible claim; where only a baseline exists you have a before/after,
which is weaker than it feels.

| Design | Set-up | Strength | The caveat that must be printed |
| --- | --- | --- | --- |
| **D1 · Matched cohort** | Compare adopted teams with a comparable non-adopted team over the same window. Match on size, function, workload mix and pre-period level | Strong | Matching is on observables only. A team that adopted early was probably more motivated, better resourced, or already improving |
| **D2 · Phased rollout** | Measure each wave against the not-yet-live waves in the same calendar period | Strong, and free — it is how most rollouts already work | Later waves inherit earlier learning, so their lift understates the first wave's. Report the earliest wave separately |
| **D3 · Hold-out team** | One comparable team deliberately not enabled for a defined period | Strongest available outside a formal study | Only valid if the hold-out was chosen **before** anyone saw results. It costs the customer real value, so it requires explicit agreement and a defined end date |
| **D4 · Before/after with seasonality control** | Same calendar period year on year, never consecutive months | Weak but common | Confounded by everything else that changed in the year. Name every confounder you know of, and expect them to name one you did not |
| **D5 · None available** | Say so | — | **No dollar figure.** Unit metrics only, plus a named ask with a date to establish the baseline |

**Choosing between them:** if any part of the customer is not yet live, you have D2 for free —
use it. If the rollout is complete but the org has comparable untreated units, you have D1. D3
only exists if you asked for it before launch, which is why this skill runs at kickoff. D4 is
the fallback, not the plan.

## 7. Difference-in-differences, worked

The strongest read a CSM can produce without a formal study: **(treated change) − (untreated
change over the same window)**.

| | Pre-period (Q1) | Current (Q3) | Change |
| --- | --- | --- | --- |
| Claims team (adopted, D1) | 412 tickets / 1,000 accounts | 284 | **−128 (−31%)** |
| Billing team (not adopted) | 388 | 372 | −16 (−4%) |
| **Difference-in-differences** | | | **−112 per 1,000 accounts, or −27 points** |

The claim is then: *"Tier-1 tickets fell 31% in the Claims team and 4% in Billing over the same
quarter, on the same definition. The 27-point difference is what we are claiming."* This is
defensible in a finance review because it names what would have happened anyway and subtracts it.

**Before you use it, check three things:** the two groups used the same metric definition; no
other programme touched only one of them; and the pre-period levels were close enough that
regression to the mean is not doing the work — the most extreme group in a pre-period tends to
move toward the middle regardless of any intervention `[A]`.

## 8. Seasonality control

| Trap | What it does | Control |
| --- | --- | --- |
| Consecutive-month comparison across a season boundary | Manufactures a gain or a loss the product had nothing to do with | Compare the same calendar period year on year |
| Academic, retail, public-sector and fiscal-year cycles | The customer's own calendar dominates the metric | Get their fiscal calendar into `cs-context` and use it for every window |
| Their end-market cycle (per-transaction models) | Their volume moves, and the metric moves with it | Report your share of their volume, or normalise by their volume |
| A go-live timed to a quiet period | Flatters every early reading | State the go-live date against their calendar and re-measure across a peak before claiming anything |

Where the year-on-year comparison is unavailable, say so and drop the band. Extrapolating across
a season is the fastest way to produce a number their operations lead will contradict in the room.

## 9. Recovery — no baseline, and the renewal is coming

Work down this list and stop at the first rung that is available. Then state which rung you
landed on, in the artifact, in plain words.

| Order | Move | Realistic time | Band it permits |
| --- | --- | --- | --- |
| 1 | **Reconstruct from their retained history** — ask what their retention window is before assuming it is gone | 3–10 days, mostly theirs | Measured, if they run it |
| 2 | **Find an untreated unit** — a region, a business unit, a team that never adopted | 1–3 days | Measured on the difference, not the level |
| 3 | **Ask the objective owner to state it, with the method** | One 30-minute call | Attested |
| 4 | **Ask the original buyer for the business case they built** — it usually contains their own pre-period numbers | One email | Attested, and it has the advantage of being their own words |
| 5 | **Proxy with a haircut** | Immediate | Indicative only — no dollar headline |
| 6 | **None** | — | Unit metrics, plus the ask |

**What to say when you land on rung 5 or 6.** Say it plainly; it is more credible than a
manufactured figure, and it converts into a decision:

> "We do not have a defensible before-picture for this, so I am not going to put a dollar figure
> on it — you would be right not to trust it. Here is what we can show: [unit metrics]. And here
> is the twenty-minute job that fixes it for next year: [named person] runs [query] against
> [system] and we hold it as the baseline from that date."

That is `4G` — decisive about the gap — and it is the sentence that gets baselines captured.

## 10. Re-baselining and the changelog

| Trigger | Action | Effect on the case |
| --- | --- | --- |
| Their metric definition changes | Re-baseline on the new definition and keep both series | Prior claims stay valid on the old definition; do not restate them silently |
| A reorg moves the team | Re-baseline on the new team boundary, or track the same headcount | Head-count continuity, not the label, is what makes the series comparable |
| Attester or sponsor departs | Re-attest with the successor before the next artifact | Band drops to Evidenced until they confirm |
| Contract, packaging or scope changes | Re-baseline the affected drivers | Cost side changes too — recompute payback |
| Annual | Refresh the record and `last_validated` | Prevents a two-year-old estimate being presented as current |

Keep a changelog with the date, what changed, who agreed it, and which prior figures it affects.
**A redefinition applied silently is indistinguishable from moving the goalposts**, and the
customer will read it that way even when it was innocent.

## 11. Failure modes

| Failure | Why it happens | Correction |
| --- | --- | --- |
| No baseline at all | Nobody owned it at kickoff | Make it a week-one milestone with a named customer owner |
| A single day or week as the baseline | Easy to pull | ≥3 comparable periods, mean or median stated |
| Our telemetry used as the "before" | It is the data we can reach | Our product's history starts at zero. That is an absence, not a baseline |
| Baseline pulled by us, presented as theirs | Speed | Have them run it, or label it ours and cap the band |
| The high end of a supplied range | It makes a better slide | Always the low end `[P]` |
| Window straddling a season | Nobody checked their calendar | Year-on-year comparison, and get the fiscal calendar into `cs-context` |
| Confounders discovered by the customer | We never asked | Ask "what else changed for this team in that period?" at capture time and record the answer |
| Account-level baseline for a team-level promise | Aggregates are easier to get | Baseline the team named in the hypothesis |
| Baseline never re-validated | No refresh cadence | `last_validated` field plus the quarterly refresh in Step 9 |
| Proxy silently promoted to a measurement | The label was in a footnote | Print the rung next to the number, on every artifact |

## 12. A full worked capture

**Account:** Northwind Logistics · **Driver:** Tier-1 support deflection · **Captured:** 2026-04-04

| Field | Value |
| --- | --- |
| `metric_name` · `unit` · `direction` | Tier-1 tickets per 1,000 active shipper accounts per month · count · ↓ |
| `baseline_value` · `baseline_period` | **412** · 2026-01-01 → 2026-03-31, 3-month mean (Jan 401, Feb 419, Mar 416) |
| `baseline_source` | Their helpdesk export, `ticket.type = tier_1 AND queue = shipper_support`, pulled 2026-04-04 |
| `pulled_by` · `rung` | Priya N., Director of Support Ops (customer) · **B2** |
| `unit_economics` | $18.40 fully loaded per Tier-1 ticket — customer-supplied, low end of their $18.40–$24 range, method: their 2025 support cost model |
| `target_value` · `target_date` | 290 by 2026-12-31 |
| `attribution_pct` · `set_by` | 70% · Priya N., email 2026-08-14 — remainder to their knowledge-base rewrite |
| `design` | **D2 · phased rollout** — Claims live 2026-04, Billing not live until 2027-01 |
| `known_confounders` | Their knowledge-base rewrite (Feb–May 2026); a pricing change on 2026-06-01 that reduced shipper volume ~6% |
| `retention_window` · `last_validated` | 13 months · 2026-08-14 |

**What this record buys.** At the measurement date, Priya re-runs one stored query. The claim
becomes: *"Tier-1 tickets fell from 412 to 284 per 1,000 accounts in Claims, and from 388 to 372
in Billing, which is not yet live. The 27-point difference at $18.40 a ticket, at the 70% you
set, is the figure."* Every number in that sentence has a name and a date on it — which is what
makes it survive a finance review.
