# Audit Procedures — the per-domain checks, pass criteria and SQL

> The runbook behind `cs-data-audit`. Every check here is specified as:
> what it measures · how to compute it · what passes · what its failure blocks.
> Field names are from `../../cs-context/references/normalized-schema.md`. Do not invent parallel names.

**Contents**
1. [The six quality dimensions](#1-the-six-quality-dimensions)
2. [Source inventory checks](#2-source-inventory-checks)
3. [Field completeness and validity register](#3-field-completeness-and-validity-register)
4. [Freshness](#4-freshness)
5. [Null-versus-zero and pipeline-outage detection](#5-null-versus-zero-and-pipeline-outage-detection)
6. [The churn-label audit](#6-the-churn-label-audit)
7. [Contract data — the document test](#7-contract-data--the-document-test)
8. [Metric integrity](#8-metric-integrity)
9. [Coverage scoring bands](#9-coverage-scoring-bands)
10. [Downstream confidence caps](#10-downstream-confidence-caps)
11. [Evidence labels used in this file](#11-evidence-labels-used-in-this-file)

---

## 1. The six quality dimensions

Test vocabulary taken from the **UK Government Data Quality Framework** (Government Analysis
Function / Office for National Statistics), which defines six dimensions with published
definitions. Using a named public framework rather than an invented one matters when a CTO
asks where the rubric came from.

| Dimension | Published definition | CS example of failure | How this audit tests it |
| --- | --- | --- | --- |
| **Completeness** | "The degree to which records are present" | 31% of accounts have no `notice_period_days` | ARR-weighted null rate per field (§3) |
| **Uniqueness** | "The degree to which there is no duplication in records" | One enterprise present as three accounts across domains | Duplicate scan on top ARR decile (§2) |
| **Consistency** | "The degree to which values in a data set do not contradict other values representing the same entity" | CRM says 200 seats, billing says 260 | Two-system agreement matrix (§8) |
| **Timeliness** | "The degree to which the data is an accurate reflection of the period that they represent" | Usage table last written 9 days ago | Observed p50/p95 lag vs expected latency (§4) |
| **Validity** | "The degree to which the data is in the range and format expected" | `primary_reason` = "cust said too $$$" | Enum/range/format tests (§3) |
| **Accuracy** | "The degree to which data matches reality" | `notice_period_days` = 30 on a contract that says 90 | Document sampling (§7) — the only dimension no automated test can reach |

**The dimension people forget is accuracy.** Completeness, validity and timeliness are all
computable from the database alone. Accuracy requires leaving the database. That is why §7
exists and why an audit that never opens a contract is not an audit.

---

## 2. Source inventory checks

| # | Check | Method | Pass | Failure consequence |
| --- | --- | --- | --- | --- |
| S1 | Reachable | Can you query it today without a ticket? | API or warehouse access | An audit on exports is a point-in-time snapshot; cap audit confidence at Medium |
| S2 | Account key present | Every row carries a key that resolves to `account.account_id` | 100% of rows | Source cannot support account-level decisions at all |
| S3 | ARR coverage | `ARR of accounts present in the source ÷ total ARR` | ≥95% | Any portfolio number from this source is partial; state the % on every use |
| S4 | Account coverage | `accounts present ÷ active accounts` | ≥95% | Report both S3 and S4 — a gap between them means the missing accounts are large or small, and which one matters |
| S5 | History depth | `today − min(date)` | ≥12 months for trend/cohort work; ≥90 days for any trend claim | Below 90 days, no trend claims; below 12 months, no cohort work |
| S6 | Duplicates | Accounts under two IDs, same legal entity | 0 in the top ARR decile | Splits ARR, understates health, double-counts logos |
| S7 | Internal exclusion | A documented, applied rule for `account.is_internal` | Rule written and applied | Employee testing inflates usage → false green on exactly the accounts you watch most |
| S8 | Owner named | A human accountable for the mapping | Named | Unowned pipelines drift silently; this is the cheapest fix in the audit |

**S3 vs S4 diagnostic.** If account coverage is 95% and ARR coverage is 68%, the missing 5% of
accounts hold 32% of revenue — the source is missing your enterprise base, usually because
those accounts are on a self-hosted or private deployment that does not phone home. That is a
different finding, and a much more expensive one, than a source missing the SMB tail.

```sql
-- S3/S4 together, per source (swap the subquery for the source under test)
SELECT COUNT(*)                                                   AS accounts_total,
       COUNT(*) FILTER (WHERE src.account_id IS NOT NULL)         AS accounts_in_source,
       ROUND(100.0 * COUNT(*) FILTER (WHERE src.account_id IS NOT NULL)/COUNT(*),1)          AS pct_accounts,
       SUM(a.arr)                                                 AS arr_total,
       ROUND(100.0 * SUM(a.arr) FILTER (WHERE src.account_id IS NOT NULL)/NULLIF(SUM(a.arr),0),1) AS pct_arr
FROM account a
LEFT JOIN (SELECT DISTINCT account_id FROM usage_daily WHERE date >= CURRENT_DATE - 90) src
       ON src.account_id = a.account_id
WHERE a.status = 'active' AND a.is_internal = FALSE;
```

---

## 3. Field completeness and validity register

Run every row. ARR-weight the completeness figure — an unweighted null rate flatters you,
because the fields missing on your largest accounts are the ones that were negotiated.

| Entity.field | Dimension | Test | Pass | What its failure blocks |
| --- | --- | --- | --- | --- |
| `account.arr` + `arr_as_of` | Completeness, Timeliness | Not null; `arr_as_of` within 31 days | 100% / ≥95% | Every dollar figure in the library |
| `account.segment` · `start_date` | Validity, Completeness | In the `cs-context` §3 enum; `start_date` not null | ≥99% / ≥98% | Segment cuts, benchmark comparison, tenure, cohorts, ramp suppression |
| `account.is_internal` · `parent_account_id` | Completeness | Not null with a documented rule; parent set wherever one exists | 100% / top-50 review | False-green from employee usage; subsidiary roll-up and ARR double-count |
| `contact.role` | Validity | In the 9-value enum | ≥80% of contacts at accounts >$50k | Champion/economic-buyer analysis; multithreading |
| `contact.email_status` · `last_seen_product` | Completeness | Populated from the mail system and product analytics | ≥90% / ≥85% | Champion-departure detection; buying-team usage separation |
| `subscription.renewal_date` | Completeness, Accuracy | Not null; document-tested (§7) | 100% / ≥95% accurate | Renewal calendar |
| `subscription.notice_period_days` | Completeness, Accuracy | Not null; document-tested | ≥95% ARR / ≥90% accurate | **`opt_out_deadline` — the date every renewal skill schedules against** |
| `subscription.opt_out_deadline` | Completeness | Derived and stored, not computed ad hoc | 100% where the two inputs exist | Forecast Commit entry |
| `subscription.auto_renew` + `auto_renew_changed_at` | Completeness, Timeliness | Not null; change timestamps captured | 100% / captured | The single strongest commercial risk signal |
| `subscription.seats_purchased` vs `seats_provisioned` | Consistency | Both present, reconciled to billing | ≥95% | Licence utilisation, the strongest downsell predictor |
| `subscription.discount_pct` / `discount_expires` / `uplift_pct` | Completeness | Populated where the clause exists | ≥90% | Renewal price position and uplift floor |
| `subscription.is_ramped` | Completeness | Flagged | 100% of ramp deals | Ramp step-ups inflate NRR with no retention motion; unflagged, they corrupt the bridge |
| `usage_daily.core_actions` | Completeness | Non-null on every account-day since instrumentation | ≥95% of account-days | All depth/decay signals |
| `usage_daily.active_users` | Validity | Null ≠ 0 (§5) | No synthetic-zero dates | False-red accounts |
| `ticket.created_at`/`first_response_at`/`resolved_at`; `type`, `priority` | Completeness, Validity | Present; in enum | ≥95% / ≥98% | FRT, TTR, SLA analysis; escalation density; support-scar pattern |
| `interaction.customer_participants` | Completeness | Non-empty array | ≥80% of logged interactions | Multithreading depth — this field is what makes relationship analysis possible |
| `interaction.direction` | Validity | `inbound`/`outbound` | 100% | One-way outbound counted as engagement is a classic false-green |
| `invoice.due_at`, `paid_at`, `payment_failures` | Completeness | Present | ≥98% / ≥95% | Days-late as a commercial signal; involuntary-churn analysis |
| `opportunity.forecast_category` | Validity | Maps to the renewal-forecast rubric | ≥98% | Forecast integrity |
| `churn_event.*` | See §6 | | | See §6 |

**Test pattern.** These map one-to-one onto dbt's four built-in generic data tests —
`not_null`, `unique`, `accepted_values`, `relationships` — with severity configured as
`warn_if` / `error_if` thresholds. If the company already runs dbt, this register becomes a
`schema.yml` and the audit becomes continuous rather than annual. Say so in the remediation
plan; it is usually a one-day fix with permanent value.

---

## 4. Freshness

Expected latencies are the table in `../../cs-context/references/evidence-standard.md` §7.
Measure **observed** lag, not the vendor's claim.

```sql
SELECT 'usage_daily' AS src, MAX(date)::date AS last_row, CURRENT_DATE - MAX(date)::date AS days_stale FROM usage_daily
UNION ALL SELECT 'ticket', MAX(created_at)::date, CURRENT_DATE - MAX(created_at)::date FROM ticket
UNION ALL SELECT 'interaction', MAX(timestamp)::date, CURRENT_DATE - MAX(timestamp)::date FROM interaction
UNION ALL SELECT 'subscription', MAX(updated_at)::date, CURRENT_DATE - MAX(updated_at)::date FROM subscription;
```

| Grade | Criterion | Effect on downstream |
| --- | --- | --- |
| Fresh | p95 lag inside expected latency | No cap |
| Lagging | ≤2× expected | Note the lag on every claim from this source |
| Stale | Past the stale-beyond threshold | Cap that family's contribution at Medium |
| Dead | No write in 30 days | Family scores 0 on freshness; treat as Missing until restored |

**Auto-NA rather than carry-forward.** GitLab's published health-scoring configuration expires
stale measures rather than showing the last known value: product-usage measures go to NA after
**60 days** without data, support measures after **30 days**, and CSM sentiment is stale at
**90 days** and forced to NA at **120** [GitLab Handbook · Customer Health Scoring · production
config, `[PROD-CONFIG]`]. Their stated reason is that showing nothing beats showing outdated
data. Recommend the same rule; a frozen green score on a dead feed is the most dangerous
artifact in customer success.

---

## 5. Null-versus-zero and pipeline-outage detection

`0` is measured-and-empty. `NULL` is not-measured. A pipeline that writes `0` on failure
manufactures false-red accounts across the whole book on the same day — which is also how you
detect it.

```sql
-- A day on which almost every account reports exactly zero is an outage, not a customer event
SELECT date, COUNT(*) AS accounts,
       COUNT(*) FILTER (WHERE core_actions = 0) AS zero_accounts,
       ROUND(100.0 * COUNT(*) FILTER (WHERE core_actions = 0)/COUNT(*),1) AS pct_zero
FROM usage_daily WHERE date >= CURRENT_DATE - 180 GROUP BY date
HAVING COUNT(*) FILTER (WHERE core_actions = 0) > 0.80 * COUNT(*) ORDER BY date;
```

| Finding | Reading | Action |
| --- | --- | --- |
| Isolated days >80% zero | Pipeline outage | Backfill or NULL those dates; never let them enter a baseline |
| Weekend/holiday clusters | Real, and expected in B2B | Apply the seasonality mask before firing decay signals |
| One account at zero, others normal | Real customer signal | Leave it; this is the signal you want |
| Zeros starting on a deploy date and never recovering | Instrumentation break | Fix the emitter; treat the pre-break baseline as the reference |

---

## 6. The churn-label audit

The highest-value ten minutes in the whole audit. Run all ten.

### 6.1 The checks

| # | Check | Method | Pass | What its failure blocks |
| --- | --- | --- | --- | --- |
| L1 | A `churn_event` row exists for every ARR→0 event | Reconcile against the ARR bridge | 100% | Churn count itself is wrong |
| L2 | `decision_date` captured separately from `effective_date` | Null rate; median gap | ≥90% populated; gap ≈ notice period | **All lead-time analysis; any churn model** |
| L3 | `primary_reason` from a fixed taxonomy | % from list; % "Other" | ≥95% on-list, "Other" ≤10% | Root-cause prioritisation; controllable/uncontrollable split |
| L4 | `type` distinguishes churn from downgrade | Enum populated | 100% | Honest GRR; downgrades hidden inside "retained" |
| L5 | Severe contraction flagged | ARR drop >50% flagged even where the logo stayed | Flag exists | Your biggest failures are invisible to post-mortems |
| L6 | Involuntary separated from voluntary | Both classes present with non-trivial counts | Both present | Dunning ROI; see §6.2 |
| L7 | `arr_lost` present and ties to finance | Sum vs the bridge's churn line | Variance ≤1% | Any dollar statement about churn |
| L8 | Point-in-time feature history stored | Score/feature snapshots at T−180/−120/−90/−60/−30 exist and are immutable | Exists | Backtesting, drift detection, calibration — **non-recoverable if not started** |
| L9 | Leakage fields named | A written exclusion list | Exists | An honest backtest |
| L10 | `was_savable` classified with a rationale | Populated | ≥80% | Save-rate denominators; capacity planning |

### 6.2 The involuntary-churn calibration test

Recurly's subscription-network data reports SaaS monthly churn of **3.22%**, decomposed as
**2.16% voluntary and 1.06% involuntary** — and involuntary churn falls with ARPC, from 1.30%
at the low end to 0.18% at the high end [Recurly Research · *Churn Rate Benchmarks* · figures
current to Jul 2026, `[M]` platform data].

Roughly a third of subscription churn in that population is payment failure. So:

| Your involuntary share | Reading |
| --- | --- |
| ~0% | The labels are wrong. Payment-failure cancellations are being coded as voluntary churn, or as nothing |
| Materially non-zero, no dunning programme | A real and usually cheap revenue recovery — quantify it and hand it to billing |
| High and rising in a low-ACV segment | Consistent with the ARPC gradient above; a card-update and retry problem, not a CS problem |

Do not present the 1.06% as your expected rate — it is one platform's population, and your ACV
mix moves it. Use it as a smell test on the labels, which is what it is good for.

### 6.3 Label sufficiency for modelling

Do not promise a model the labels cannot support.

| Ambition | Minimum | Source |
| --- | --- | --- |
| Weighted rubric, no calibration | 5–8 fields drawn from CRM + support + billing | Library convention (`health-score-designer`) — under five inputs is a single metric in costume, over eight cannot be explained to a CSM `[P]` |
| Hand-fit logistic regression | ~10–20 **events** per predictor variable — 8 predictors means 80–160 *churn events*, not 80 accounts | Peduzzi et al. 1996 (EPV rule) `[A]`; Riley et al., *Statistics in Medicine* 2019 showed EPV rules are unreliable and derived closed-form minimums accounting for prevalence and shrinkage — use theirs when the decision is expensive `[A]` |
| Gradient-boosted model | ≥1,000 labelled renewal outcomes, ≥150 negatives, ≥18 months history, a point-in-time feature store | Practitioner rule of thumb `[P]` |
| Probability calibration layer | ≥500 held-out outcomes for Platt scaling; ≥1,000 for isotonic | `[P]`, from the standard result that isotonic overfits on small samples |

**Cold-start protocol** when no labels exist: ship the rubric, instrument everything, and record
score history from day one. Do not fit weights from data until one full renewal cycle has
closed. In the interim, validate against proxy labels — downsell events, support escalations,
sponsor departures, auto-renew-disabled flags.

### 6.4 The leakage exclusion list

Anything that only exists because the outcome already happened. Name these explicitly in the
audit; a backtest that includes them produces a spectacular AUC and a useless production model.

`churn_event.primary_reason` · `renewal_status` · cancellation-request ticket type ·
"will churn" flags · `opportunity.stage = Closed Lost` · `opportunity.loss_reason` ·
CSM sentiment recorded after notice was served · any CRM field restated after the decision date.

The subtle one is sentiment. Where a sentiment rule recomputes on a short cycle — GitLab's runs
every two hours `[PROD-CONFIG]` — the field is contaminated within hours of the churn
conversation, so a snapshot taken "at T−30" from a live table is not a T−30 snapshot at all.
This is why L8 requires immutable stored history rather than a query against current state.

---

## 7. Contract data — the document test

### 7.1 Procedure

1. **Census the top 20 accounts by ARR.** No sampling at the top; these are the ones a wrong
   notice period actually costs you.
2. **Stratified random sample below that**: 25 minimum, 100 if the top-20 census fails.
   Stratify by ARR decile so the sample is not all SMB.
3. For each: pull the executed contract and any amendments from the CLM, e-signature archive
   or shared drive. Read the term, the notice clause, the auto-renew clause, the uplift clause,
   the discount and its expiry, and the seat count **as amended**.
4. Compare to the CRM/billing field. Record match / mismatch / field-empty.
5. Report per-field accuracy with a confidence interval, and list the mismatches by account and
   ARR — the list is more persuasive than the rate.

### 7.2 Sample size and what it buys you

95% confidence interval half-width for a proportion, normal approximation
`1.96 × sqrt(p(1−p)/n)`, computed at the worst case `p = 0.5`:

| n | ± half-width at p=0.5 | What it can distinguish |
| --- | --- | --- |
| 25 | ±19.6pp | Catastrophic (<60%) from acceptable. Not 88% from 95% |
| 50 | ±13.9pp | A coarse grade |
| 100 | ±9.8pp | "Roughly 90%" — enough for a remediation decision |
| 200 | ±6.9pp | A defensible published figure |
| 384 | ±5.0pp | The conventional ±5pp survey standard |

At observed accuracies far from 0.5 the interval narrows — at `p = 0.9`, `n = 25` gives
±11.8pp. `scripts/audit_score.py --ci` computes the exact figure for your observed rate.
**Always print n and the interval.** "Notice period is 84% accurate" with no n is the same
class of error as a benchmark with no population.

### 7.3 The derived field that matters most

```sql
-- Opt-out deadline computability, ARR-weighted
SELECT COUNT(*) AS subs,
       COUNT(*) FILTER (WHERE renewal_date IS NULL)       AS no_renewal_date,
       COUNT(*) FILTER (WHERE notice_period_days IS NULL) AS no_notice_period,
       SUM(arr) FILTER (WHERE renewal_date IS NULL OR notice_period_days IS NULL) AS arr_not_computable
FROM subscription WHERE end_date >= CURRENT_DATE;
```

Report `arr_not_computable` as a headline number. Every skill in this library schedules against
`opt_out_deadline = renewal_date − notice_period_days`, never the renewal date — a customer with
90 days' notice on a 1 February renewal decides in October. A subscription whose opt-out deadline
cannot be computed cannot legitimately enter a Commit forecast category.

**Prevalence context:** 30/60/90 days before renewal is the near-universal notice set, with 30
days most common in standardised SaaS agreements and 60–90 typical in negotiated enterprise
agreements [contract-market guides, 2026 `[V]`]. If your CRM shows a single value on every row,
that is a default someone typed once, not a fact — treat it as a failed accuracy test until the
documents say otherwise.

---

## 8. Metric integrity

### 8.1 Reproduce before you report

| Metric | Reproduce from | Tolerance | If it fails |
| --- | --- | --- | --- |
| GRR | Cohort frozen at t0; churned members stay in the denominator at $0; expansion excluded from the numerator | ≤0.5pp | Stop reporting until reconciled |
| NRR | Same cohort; expansion included; reactivation **excluded** | ≤0.5pp | Same |
| Logo retention | Logo count on the same frozen cohort | ≤1pp | Same |
| ARR bridge | new · expansion · contraction · churn · reactivation summing to the period ARR delta | ≤0.5% | The bridge is where every retention number is born; fix it first |
| ATR | ARR with a contractual renewal date inside the period — not total ARR | Exact | Multi-year contracts make total-ARR denominators understate churn severity |

### 8.2 The definition checklist

A metric definition is not documented until it answers all eight. Version it, date it, and keep
a change log — a silent definition change destroys every trend line retroactively.

1. Cohort method or formula method? (Cohort is the definition; the formula is an approximation.)
2. Denominator: ATR or beginning-period ARR?
3. Is reactivation in the numerator? (It should be a bridge line, not retention.)
4. Are multi-year contracts in ATR only in their renewal year, and are annual opt-outs treated
   as renewal events?
5. Are contracted ramp step-ups tagged separately from sales-won expansion?
6. Professional services and one-time fees excluded?
7. Constant currency, and when does the rate reset?
8. Which segment cut is primary? (ACV band is the most predictive cut for retention.)

### 8.3 Two-system agreement

```sql
SELECT a.account_id, a.name, a.arr AS crm_arr, b.arr AS billing_arr, w.arr AS warehouse_arr,
       ABS(a.arr - b.arr) / NULLIF(GREATEST(a.arr, b.arr),0) AS crm_vs_billing_var
FROM account a
LEFT JOIN billing_arr_snapshot b USING (account_id)
LEFT JOIN warehouse_arr_snapshot w USING (account_id)
WHERE ABS(a.arr - COALESCE(b.arr,a.arr)) / NULLIF(GREATEST(a.arr, COALESCE(b.arr,a.arr)),0) > 0.05
ORDER BY a.arr DESC;
```

Pass: fewer than 2% of accounts vary by more than 5%, **and** a source of truth is named per
field rather than per system. In practice the CRM owns contract terms, billing owns invoiced
amounts, and the warehouse owns nothing — it reflects whichever it loaded last. Write that
ruling down.

### 8.4 Benchmark anchoring, if asked

| Metric | Value | Population | Source / year | Type |
| --- | --- | --- | --- | --- |
| Median GRR | 88% | Private B2B SaaS, N=225 | Benchmarkit, *2025 B2B SaaS Performance Metrics Benchmarks*, CY2024 | `[M]` |
| Median NRR | 101% | Private B2B SaaS, N=228 | Benchmarkit 2025, CY2024 | `[M]` |
| GRR, usage-based pricing | 92% (P25 88, P75 96) | Private B2B SaaS | Benchmarkit 2025 | `[M]` |
| NRR, ACV $25–50k | Median 102%, P75 111%, P25 97% | Private B2B, by ACV band | SaaS Capital, *2025 Retention Benchmarks* | `[M]` |
| Health scores that reliably predict churn | 73% of CS leaders say theirs does **not** | ≈800 customer and post-sales leaders | *Customer Revenue Leadership Study* — Pavilion / 6sense, 2025 | `[M]` self-reported |

Never benchmark a private company against the 120% NRR figure that circulates from large public
companies. State population, sample size and year on every quote, or do not quote it.

---

## 9. Coverage scoring bands

Five dimensions per family, 0–20 each, summing to 0–100.

| Dimension | 20 | 15 | 10 | 5 | 0 |
| --- | --- | --- | --- | --- | --- |
| **Presence** | Connected source, API or warehouse access | Connected, export-only | Manual/partial | Ad-hoc, unowned | No source |
| **Account coverage** (% of ARR-bearing accounts) | ≥95% | 85–95% | 70–85% | 50–70% | <50% |
| **Field completeness** (required fields populated) | ≥90% | 75–90% | 60–75% | 40–60% | <40% |
| **Freshness** (observed p95 vs expected latency) | Inside | ≤2× | ≤5× | Past stale threshold | No write in 30d |
| **Fidelity** (family-specific, below) | ≥90% | 80–90% | 65–80% | 50–65% | <50% |

**Fidelity is measured differently per family** — this is what stops the score from being a
paperwork exercise:

| Family | Fidelity measure |
| --- | --- |
| Product usage & adoption | ARR join rate (§ identity-resolution.md §2) × taxonomy conformance |
| Commercial & contract | Document-test accuracy (§7) on `renewal_date`, `notice_period_days`, `auto_renew` |
| Relationship & engagement | % of interactions with a non-empty `customer_participants` array and a correct `direction` |
| Support & reliability | % of tickets with a resolvable `account_id` and a valid `type`/`priority` |
| Sentiment & VoC | Response rate × % of responses attributable to a named `contact_id` with a role |
| Billing & payment | Reconciliation variance to finance, inverted (1 − variance) |
| Firmographic & external | % of accounts with `industry`, `employee_count` refreshed inside 90 days |

Family score → ledger status: **≥80 ✅ Complete (1.0) · 40–79 ⚠️ Partial (0.5) · <40 ❌ Missing (0)**.
Coverage = Σ status ÷ 7. Confidence cap per `evidence-standard.md` §4.

---

## 10. Downstream confidence caps

Publish this table. It is the contract between the audit and every other skill in the library.

| Skill | Families required | Hard gate | Effect of failing the gate |
| --- | --- | --- | --- |
| `churn-risk` | All 7; weighted on usage, commercial, relationship | Commercial family <40, or overall coverage <40% | Produce the gap list, not a score |
| `renewal-forecast` | Commercial, billing | `opt_out_deadline` null on >10% of ARR | Those subscriptions cannot enter Commit |
| `expansion-finder` | Usage, commercial, billing | `seats_purchased`/entitlement completeness <90% | No sizing; qualitative signals only |
| `health-score-designer` | Any 4 families + stored score history | L8 fails (no immutable history) | Rubric only — no calibration, no backtest, and say so |
| `churn-postmortem` | Commercial + labels | L2 fails (`decision_date` absent) | Reasons only; no lead-time or earliest-detectable-signal analysis |
| `pre-call-brief` | Relationship, support, usage | Relationship family <40 | Brief must state that stakeholder data is unverified |
| `qbr-builder` | Usage, sentiment + outcome baselines | No baseline captured at onboarding | Value claims are unsupportable; report activity, not ROI |
| `coverage-and-capacity` | Commercial + account coverage | S3 ARR coverage <90% | Ratios are computed on a partial book; state the % |

---

## 11. Evidence labels used in this file

| Label | Meaning |
| --- | --- |
| `[M]` | Measured benchmark from a named study with a stated sample and period |
| `[V]` | Vendor research or product documentation — operationally specific, method usually unpublished |
| `[P]` | Practitioner rule of thumb — widely used, not measured. Never present as a statistic |
| `[A]` | Academic or peer-reviewed |
| `[PROD-CONFIG]` | A published production configuration from a named company |

Carry these labels into the audit report. "Commonly configured at X" and "measured at X in
population Y" are different sentences, and a CFO can tell.
