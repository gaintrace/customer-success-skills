# Remediation Planning — ranking the fixes, sequencing the waves, funding the work

> An audit that ends with a list of problems is a complaint. An audit that ends with a ranked,
> costed plan and a two-page ask is a budget line. This file is how you get from one to the
> other.

**Contents**
1. [The ranking formula and how to fill it in](#1-the-ranking-formula-and-how-to-fill-it-in)
2. [Worked ranking example](#2-worked-ranking-example)
3. [The standing quick-win list](#3-the-standing-quick-win-list)
4. [Expensive fixes that are usually not worth it yet](#4-expensive-fixes-that-are-usually-not-worth-it-yet)
5. [Sequencing into waves](#5-sequencing-into-waves)
6. [The CFO conversation](#6-the-cfo-conversation)
7. [The CTO conversation](#7-the-cto-conversation)
8. [Governance after the sprint](#8-governance-after-the-sprint)

---

## 1. The ranking formula and how to fill it in

```
Priority = B × D × (1 + 0.1 × U) × C ÷ E
```

| Term | Definition | How to source it |
| --- | --- | --- |
| **B** — Blast radius | Total ARR governed by the decisions this gap degrades | Sum the ARR column of the Decision Set table (Step 1) across every decision that consumes the broken field |
| **D** — Degradation | 1.0 the decision cannot be made · 0.6 it can be made but confidence is capped · 0.3 it adds noise without changing the call | Judgement, but stated per row and defensible |
| **U** — Unlocks | Count of downstream decisions or skills the fix unblocks, capped at 5 | Read straight off the Downstream Confidence Caps table (`audit-procedures.md` §10) |
| **C** — Irreversibility | 1.5 if delay permanently destroys data · 1.0 otherwise | See the test below |
| **E** — Effort | Person-days, engineering + ops + CS combined, including the review that follows | Ask the owning team. Round up |

### The irreversibility test

Set `C = 1.5` if and only if: **if we do this in twelve months instead of today, will we have
lost twelve months of data we can never recover?**

| Gap | C | Why |
| --- | --- | --- |
| Core action not instrumented | 1.5 | Events not emitted cannot be backfilled |
| Health-score history overwritten in place | 1.5 | No stored history, no backtest, ever, for that period |
| `churn_event.decision_date` not captured at the moment of notice | 1.5 | Reconstructable from email archaeology only, and only for a while |
| Seat-limit / invite-blocked events not emitted | 1.5 | Same as any un-emitted event |
| `notice_period_days` wrong in CRM | 1.0 | The contracts still exist; correct them any time |
| Duplicate accounts | 1.0 | Merge whenever |
| Metric definitions undocumented | 1.0 | Write them down whenever |
| Domain list incomplete | 1.0 | Backfillable from the CRM |

`C` is the term that overrides intuition. A gap with a small blast radius but `C = 1.5` should
usually be scheduled ahead of a larger, reversible one — because the reversible one costs the
same in twelve months and the irreversible one costs twelve months of history.

### Rules of use

- **Never sort by E ascending.** That is how a team spends two quarters on the easiest work.
- **Print the arithmetic** in the report. A rank without its inputs is a preference.
- **Recompute B when the decision set changes.** B is not a property of the gap; it is a
  property of what the company decides using it.
- **Cap U at 5** so a fix that touches everything does not swamp the ranking on breadth alone.
- **Do not fabricate B.** If the ARR governed by a decision is unknown, write
  `UNKNOWN — requires the renewal calendar` and rank the row provisionally, flagged.

---

## 2. Worked ranking example

Illustrative figures for a $40M-ARR B2B SaaS with 620 accounts. **Every number below is an
example, not a benchmark** — B, E and the decision-set ARR are company-specific by construction.

| Gap | B | D | U | C | E | Priority | Rank |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `notice_period_days` missing/wrong on 31% of ARR | $12.4M | 1.0 | 3 | 1.0 | 6 | 2,687k | **1** |
| Core action not instrumented on mobile + API | $18.0M | 0.6 | 4 | 1.5 | 12 | 1,890k | **2** |
| `churn_event.decision_date` not captured | $40.0M | 0.6 | 3 | 1.5 | 3 | 15,600k | — see note |
| Health-score history overwritten in place | $40.0M | 0.6 | 2 | 1.5 | 2 | 21,600k | — see note |
| Product→account join rate 71% | $28.0M | 0.6 | 4 | 1.0 | 10 | 2,352k | 3 |
| Churn reasons free text | $40.0M | 0.3 | 2 | 1.0 | 1 | 14,400k | — see note |
| No NPS/CSAT source connected | $40.0M | 0.3 | 2 | 1.0 | 25 | 576k | 6 |
| Duplicate accounts in top decile (7 pairs) | $6.2M | 0.6 | 2 | 1.0 | 2 | 2,232k | 4 |
| Metric definitions undocumented | $40.0M | 0.3 | 3 | 1.0 | 4 | 3,900k | 5 |

**Reading the note rows.** Three fixes score enormously because `E` is tiny — one to three days
— and `B` is the whole book. That is the formula working as intended, not a bug: capturing a
decision date, closing the reason picklist and switching score history from overwrite to append
are each a day or two of admin work that unblock everything downstream and are irreversible if
deferred. They are not "rank 1" in a sequencing sense; **they are the quick wins, and they ship
in week one alongside whatever else is running.** Sequence them first and rank the substantive
engineering work behind them.

That is the practical convention: **anything scoring above ~10,000k with E ≤ 3 goes to the
quick-win wave rather than into the ranked queue.** Say so in the report so the ranking does not
look manipulated.

---

## 3. The standing quick-win list

These are available at almost every company, cost days rather than quarters, and several are
irreversible if deferred. Offer them as a single week-one bundle with one owner.

| # | Fix | Effort | C | Unlocks | Success measure |
| --- | --- | --- | --- | --- | --- |
| 1 | Store `opt_out_deadline` as a derived field (`renewal_date − notice_period_days`) rather than computing it ad hoc | 0.5 day | 1.0 | Renewal calendar, forecast Commit entry, every renewal skill | Field present and non-null wherever both inputs exist |
| 2 | Backfill `notice_period_days` from the executed contracts of the top 50 accounts by ARR | 3 days | 1.0 | Same as 1, on the ARR that matters | Top-50 census 100% document-verified |
| 3 | Convert `churn_event.primary_reason` to a required closed picklist, with "Other" requiring free text | 1 day | 1.0 | Root-cause prioritisation; controllable/uncontrollable split | "Other" ≤10% of the next quarter's churns |
| 4 | Add `decision_date` to the churn object and require it at close | 1 day | **1.5** | All lead-time analysis; any future churn model | ≥90% populated on churns closed after go-live |
| 5 | Switch health-score and usage rollups from overwrite to daily append (`score_history` table) | 2 days | **1.5** | Backtesting, drift detection, trend and velocity measures | One row per account per day, retained indefinitely |
| 6 | Write and apply the internal/test account exclusion rule | 1 day | 1.0 | Removes a systemic false-green | Rule documented; `is_internal` populated 100% |
| 7 | Publish the metric definitions document with a version number and change log | 3 days | 1.0 | Ends the two-systems-disagree argument permanently | GRR/NRR reproduce to ≤0.5pp against the document |
| 8 | Build `account.domains[]` for the top 100 accounts by ARR | 2 days | 1.0 | Multi-domain and post-acquisition handling | Join rate re-measured and reported |
| 9 | Flag shared/service identities and external collaborators on `contact` | 3 days | 1.0 | Correct per-seat utilisation | Utilisation recomputed; threshold crossings reported |
| 10 | Deduplicate accounts in the top ARR decile | 2 days | 1.0 | Correct ARR, segment assignment, cohort membership | Zero duplicates in the top decile |
| 11 | Add an `auto_renew_changed_at` timestamp and an alert on any change | 1 day | **1.5** | The single strongest commercial risk signal becomes detectable | Change events captured and routed within 24h |
| 12 | Add analytics to the release checklist (renames and deprecations logged) | 0.5 day | 1.0 | Prevents fleet-wide false reds | Change log has entries after the next two releases |

Total: roughly **20 person-days**. Present it as one bundle with one owner and one done-by date.
A twenty-day ask that unblocks eight downstream capabilities is an easy yes; the same twelve
items presented separately across three teams is twelve chances to say not this quarter.

---

## 4. Expensive fixes that are usually not worth it yet

Saying this out loud is what makes the rest of the plan credible. A remediation plan that asks
for everything gets funded for nothing.

| Fix | Typical cost | Why not yet | Revisit when |
| --- | --- | --- | --- |
| **Full CDP / identity-graph deployment** | 40–100+ person-days plus licence | It resolves identifiers you are already emitting. If the product does not send `org_id`, a CDP inherits the same ambiguity at higher cost | `org_id` is emitted on ≥90% of volume and the join rate is still <90% |
| **Retroactive event backfill** | Usually impossible | Events never emitted cannot be recovered. Proposing it signals the plan was not read | Never. Start emitting and state that history begins today |
| **Enterprise MDM programme** | Quarters | Solves a governance problem you do not have at 620 accounts | Multi-entity M&A makes the account grain genuinely ambiguous across systems of record |
| **CRM migration to fix field hygiene** | Quarters, plus a year of disruption | A migration copies your data quality into a new system. The fields are wrong because nobody owns them, and that travels | The CRM is being replaced for other reasons anyway — then piggyback the field cleanup |
| **A churn ML model** | 30–60 person-days plus ongoing | Gated by labels, not by modelling skill. A gradient-boosted model wants ≥1,000 labelled renewal outcomes with ≥150 negatives and ≥18 months of point-in-time history `[P]`; a hand-fit logistic regression wants roughly 10–20 events per predictor, so 8 predictors means 80–160 *churn events* [Peduzzi et al. 1996 `[A]`, with the Riley et al. 2019 correction] | The label audit (§6 of `audit-procedures.md`) passes L2, L8 and L9, and the counts clear the table in §6.3 |
| **Real-time streaming pipeline** | 20–40 person-days | The decisions run weekly. Real-time data feeding a weekly meeting buys nothing | A play must fire inside minutes — for example, a seat-limit-reached trigger routed to sales |
| **Buying a CS platform to fix the data** | Licence plus 20–40 days of implementation | A platform inherits your join rate, your labels and your contract fields. Implementation on broken inputs produces an expensive version of the same wrong numbers | The quick-win bundle has shipped and coverage is ≥60% — then a platform compounds good inputs instead of laundering bad ones |
| **Rewriting the whole product event taxonomy** | 20–60 person-days | CS consumes roughly fifteen events. Scope to those | The fifteen are shipped and a product decision needs the rest |

**How to say it.** "We are deliberately not doing X yet, because it costs Y and buys nothing
until Z is true. We will revisit at Z." That sentence is what a CFO remembers about the whole
document, because it is the only part that demonstrates you are not simply asking for
everything.

---

## 5. Sequencing into waves

| Wave | Window | Contents | Gate to advance |
| --- | --- | --- | --- |
| **0 — Stop the bleeding** | Week 1 | Every `C = 1.5` item that costs ≤3 days: decision date, score-history append, auto-renew change capture, closed reason list, analytics on the release checklist | All irreversible-loss items are capturing data, even if imperfectly |
| **1 — Quick wins** | Weeks 1–4 | The rest of the §3 bundle | Coverage re-measured; opt-out deadline computable on ≥95% of ARR |
| **2 — The top-ranked engineering item** | Weeks 3–10 | Usually core-action instrumentation or the identity fix, whichever ranked higher | Join rate ≥90% on all three measures, or core action emitting on all surfaces |
| **3 — Structural** | Quarter 2 | Rollup tables, ingest enforcement, the missing signal family with the best ratio | Family score ≥80 on the target family |
| **4 — Re-audit** | Day 90 | Re-run the audit in Re-audit mode; report the score delta per family | Coverage improved as forecast, or the plan is revised with the reason |

**Wave 0 exists because of the C factor.** Its items are cheap, unglamorous, and each one is a
year of data if you start today rather than next quarter. Run it in parallel with everything
else; it needs one person for a week, not a project.

**Every wave has a gate stated as an observable measurement**, not as "done". A wave whose exit
criterion is "the fix is complete" cannot be verified; one whose criterion is "join rate ≥90% on
all three measures" can.

---

## 6. The CFO conversation

### Lead with forecast error, not data quality

A CFO does not fund data quality. They fund forecast accuracy, revenue protection and audit
defensibility. Translate every finding before it reaches the page.

| What the audit found | What the CFO hears |
| --- | --- |
| "31% of subscriptions have no `notice_period_days`" | "$12.4M of ARR renews on a date we cannot verify, and 19 of those renewals cannot legitimately be called Commit" |
| "Join rate is 71%" | "Utilisation — the input we use to size renewals and expansions — is computed on 71% of users, and the missing ones cluster at our largest accounts" |
| "Churn reasons are free text" | "We cannot tell the board which of last year's $3.1M of churn was addressable" |
| "GRR varies 2.4pp between systems" | "Two of our reports disagree on retention by 2.4 points. Whichever number the board saw, one of them is wrong" |
| "No stored score history" | "We cannot demonstrate whether our health score has ever predicted anything" |

### The three numbers

1. **ARR forecast on inputs that failed a test.** Not the whole book — the specific subset.
2. **ARR whose renewal decision has no computable opt-out date.** This is the number that moves
   people, because it is a governance failure, not an analytics one.
3. **Cost of the fix set against the ARR of one missed save.** If the quick-win bundle is 20
   days and a mid-market account is $95k, the bundle pays for itself if it prevents a fifth of
   one churn. Say the arithmetic out loud; do not imply it.

### The tier table

Always three tiers. Always state what stays broken in each.

| Tier | Cost | What it buys | ARR it de-risks | What stays broken |
| --- | --- | --- | --- | --- |
| **Minimum** | ~20 person-days, no engineering | Opt-out deadlines computable, churn labels usable going forward, definitions documented, score history accruing | The renewal calendar and next year's ability to analyse this year | Usage data stays partial; no predictive work |
| **Standard** | + ~25 engineering days | Core action instrumented on all surfaces; join rate above 90% | Utilisation-driven renewal and expansion sizing | Sentiment family still absent |
| **Complete** | + ~30 days and a VoC tool | Sentiment family connected; coverage above 80%; High confidence available | The full seven-family read | Nothing material — revisit annually |

Recommend one tier explicitly. A menu with no recommendation is a decision handed back.

### What not to do

- Do not open with a table of null rates. Open with the decision being made wrong.
- Do not present the audit as evidence anyone failed. Data decays; it is nobody's fault and
  everybody's problem.
- Do not promise accuracy. Promise that a specific decision moves from unsupported to supported,
  at a stated confidence band.
- Do not quote a retention benchmark without its population, sample size and year.

---

## 7. The CTO conversation

Different currency entirely: engineering days, ongoing burden, and critical path.

| Item | Eng days | One-off or ongoing | What it blocks | Not engineering work |
| --- | --- | --- | --- | --- |
| Emit `account_id` on core events | 2 | One-off | Everything account-grained | — |
| Instrument core action on mobile + API | 12 | One-off, then release-checklist discipline | Depth, decay, activation, TTV | — |
| `seat_limit_reached` / `invite_blocked` | 3 | One-off | Seat-expansion sizing | — |
| Daily account rollup table | 3 | Ongoing (a scheduled job with an owner) | Utilisation, breadth, trend | — |
| Tracking-plan enforcement at ingest | 3 | Ongoing | Stops new drift | Writing the plan itself is ops |
| Domain-migration watcher | 2 | Ongoing | Prevents fleet-wide false reds | — |
| Score-history append table | 2 | Ongoing | Backtesting, calibration | — |
| Contract field backfill | 0 | — | Opt-out deadlines | **All of it — ops and CS, not engineering** |
| Reason picklist and required fields | 0 | — | Root-cause analysis | **CRM admin** |
| Metric definitions document | 0 | — | Metric disputes | **Finance and CS Ops** |

**Lead with the last three rows.** Roughly two thirds of a typical CS data remediation plan is
not engineering work at all. Showing that first makes the engineering ask small, specific and
credible — and it is true, which is why it works.

Then name the critical path: what cannot start until this lands, and which quarter it slips to
if it does not.

---

## 8. Governance after the sprint

A remediation plan with no governance produces the same audit again in eighteen months.

| Control | Cadence | Owner | Cost |
| --- | --- | --- | --- |
| The field register (§3 of `audit-procedures.md`) encoded as automated tests — dbt's `not_null` / `unique` / `accepted_values` / `relationships`, with `warn_if` and `error_if` thresholds | Every pipeline run | Data | 1 day to set up, ~0 to run |
| Freshness monitors with auto-NA rather than carry-forward | Daily | Data | 1 day |
| Join-rate published on an internal dashboard | Weekly | CS Ops | 0.5 day |
| Tracking-plan change review on the release checklist | Per release | Product | ~0 |
| Contract-field spot audit: 10 random accounts | Quarterly | CS Ops | 0.5 day per quarter |
| Metric definitions change log reviewed | Quarterly | Finance + CS Ops | 0.5 day per quarter |
| Full re-audit in Re-audit mode | Annual | CS Ops | 3–5 days |
| Coverage published as a company metric | Monthly | CS Ops | ~0 once instrumented |

**Coverage is a governance metric, not an analytics one.** GitLab tracked ">95% of customers
have a health score" as a company-level yearly goal [GitLab Handbook · Customer Health Scoring,
`[PROD-CONFIG]`]. A score that covers 60% of the book cannot forecast retention, and the only
way that stays visible is to publish the coverage number next to the score every month.

**Name an owner for the data layer.** The most common root cause behind every finding in this
audit is that no single person is accountable for the mapping between systems. That is a
zero-cost fix and it is the one most often left out of remediation plans.
