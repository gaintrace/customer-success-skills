# The Board Appendix

> What changes when the retention report goes to a board, an investor or a diligence process —
> and what to leave out.
>
> This is the **appendix**, not the narrative. The narrative — five sentences, one strategic
> issue, one ask — belongs to `exec-retention-review`. This file covers the exhibits that sit
> behind it and have to survive a director who benchmarks for a living.

**Contents**
- [1. What changes for a board audience](#1-what-changes-for-a-board-audience)
- [2. The six exhibits](#2-the-six-exhibits)
- [3. The definitions page](#3-the-definitions-page)
- [4. Benchmark citation rules](#4-benchmark-citation-rules)
- [5. The benchmark table](#5-the-benchmark-table)
- [6. Questions a director asks of the appendix](#6-questions-a-director-asks-of-the-appendix)
- [7. What to leave out](#7-what-to-leave-out)
- [8. Diligence mode](#8-diligence-mode)

---

## 1. What changes for a board audience

| Dimension | Operating report | Board appendix |
| --- | --- | --- |
| **Period basis** | Month + QTD + TTM | TTM or annual only. Never a single month |
| **Currency** | Reporting currency | Constant currency, with the FX basis stated |
| **History** | Prior period + trend | Eight periods minimum on every exhibit |
| **New metrics** | Introduced as needed | Never introduced without eight prior periods beside it |
| **Segmentation** | Every cut in §6 of `report-structure.md` | ACV band primary; two cuts maximum per exhibit |
| **Benchmarks** | Optional | Expected, and cited on the exhibit itself with population and year |
| **Named accounts** | Yes, in the loss table | Only in the top-10 renewal calendar and concentration exhibit |
| **Health scores** | Central | Only as evidence for exposure, never as the metric itself — a board cannot audit an internal score |
| **Restatements** | Operating note | On the exhibit, in the footer, every time |
| **Definitions** | Appendix | Mandatory page, with a dated change log |

The single biggest calibration error is bringing operating altitude to a board. The migration
matrix, the reason-code mix and the per-owner cuts are excellent internal instruments and they
are noise in a board pack — a director cannot act on a rescue rate. What travels upward is the
bridge, the retention trend with its benchmark band, the cohort triangle, the exposure and the
concentration.

---

## 2. The six exhibits

| # | Exhibit | Content | Why a board needs it |
| --- | --- | --- | --- |
| A1 | **ARR bridge, 8 quarters** | Beginning · new · expansion · reactivation · contraction · churn · ending, with NRR/GRR overlaid | Shows flow, not stock. It is the only exhibit that answers "which line broke" |
| A2 | **Retention by ACV band, TTM** | GRR and NRR per band, 8 periods, peer benchmark band drawn in and cited | Boards benchmark. Give them the citation so they do not use a worse one |
| A3 | **Cohort retention triangle, dollar basis** | 8–12 acquisition cohorts, immature cells greyed | The exhibit that proves whether the business is structurally improving. Nothing else does |
| A4 | **Renewal exposure and concentration** | Next-4-quarter ATR by quarter; top-10 ARR share; named top-10 renewal status | Risk disclosure. Top-10 concentration above **25%** is board-level (a standard operating threshold `[P]`) |
| A5 | **Forecast credibility** | Trailing 8 quarters: called (frozen) vs closed, accuracy and signed bias | Determines how much weight the board puts on every forward number in the pack |
| A6 | **Definitions and change log** | §3 below | The exhibit that makes the other five auditable |

Exhibits A1–A5 each carry one sentence beneath them. Not a paragraph — one sentence, naming the
movement and its driver. If an exhibit needs three sentences it is two exhibits.

---

## 3. The definitions page

Mandatory. It is the shortest exhibit and the one that most often prevents a bad meeting.

| Field | Content |
| --- | --- |
| **ARR** | What counts and what does not: recurring subscription only; excludes professional services, one-time fees, hardware, non-recurring overage. State whether signed-not-yet-live is included — if it is, the metric is CARR and must be labelled CARR |
| **GRR** | Cohort method, formula written out, window, and the fact that expansion above each account's t0 ARR is stripped |
| **NRR** | Cohort method, formula written out, window; explicitly states that new logos and reactivation are excluded |
| **Logo retention** | Cohort method; the exclusion policy for trials, freemium and zero-usage accounts |
| **ATR** | Contracts with a renewal or expiry date inside the period. Not total ARR |
| **Segment / ACV band** | The dollar boundaries, and the date they were last changed |
| **Win-back window** | The number of days after which a returning account is New rather than Reactivation |
| **At-risk** | The written entry and exit criteria, and who can set the state |
| **Health bands** | Score ranges, and the date the thresholds last moved |
| **Currency** | Constant currency basis and the FX rate date |
| **Change log** | Dated, append-only. Every definition change, its reason, the periods restated, and the effect in basis points |

A board pack without this page invites the board to assume a definition, and the assumed one is
usually the most favourable — which is worse for you than the true one, because it sets an
expectation you did not choose.

---

## 4. Benchmark citation rules

| Rule | Why |
| --- | --- |
| **Population, ARR floor, ACV mix and year on the same line as the number** | Two correct benchmarks from different populations differ by twenty points |
| **Label the evidence tier**: [M] measured with disclosed methodology · [V] vendor claim · [P] practitioner convention · [A] academic | A [P] presented as an [M] to a board is the kind of error that gets remembered |
| **Never present a [P] as "the benchmark"** | The 3:1 LTV:CAC rule and the 4.0 Quick Ratio are conventions, not measured medians |
| **Draw the band, not the point** | P25/median/P75 shows where you sit. A single median invites a pass/fail reading of a distribution |
| **Do not benchmark private against public without normalising** | Private CAC payback uses New Customer ARR; public "implied" payback uses Net New ARR. They are different metrics |
| **Do not benchmark a renewal rate against a GRR benchmark** | Gross renewal rate uses the ATR denominator and is structurally lower. Different metric, different benchmark |
| **State when no clean benchmark exists** | For renewal forecast accuracy and ARR-per-CSM there is no current, methodologically disclosed public benchmark. Say so and use your own trailing periods |

---

## 5. The benchmark table

Reproduce only the rows relevant to the exhibit, with the label attached.

| Metric | Value | Population | Source · year | Label |
| --- | --- | --- | --- | --- |
| GRR median | 84% (P75 91%, P25 76%) | B2B SaaS + AI-native, N=226, CY2025 actuals | Aleph × Benchmarkit, 2026 | [M] |
| GRR median | 88% | Private B2B SaaS, N=225, CY2024 actuals | Benchmarkit, 2025 | [M] |
| GRR, usage-based pricing | 92% (P25 88%, P75 96%) | Private B2B SaaS, CY2024 | Benchmarkit, 2025 | [M] |
| GRR, best-in-class MM/ENT | ~95% | B2B SaaS, $250k ARR floor | ChartMogul, 2025 | [M] |
| NRR median | 102% (P75 110%, P25 92%) | B2B SaaS + AI-native, N=230, CY2025 | Aleph × Benchmarkit, 2026 | [M] |
| NRR median | 101% | Private B2B SaaS, N=228, CY2024 | Benchmarkit, 2025 | [M] |
| NRR, hybrid subscription + usage | 110% | Private B2B SaaS, CY2024 | Benchmarkit, 2025 | [M] |
| NRR / GRR, bootstrapped | 103% / 91% median (P90 117.9% / 100%) | Bootstrapped private B2B SaaS, $3–20M ARR, 1,000+ companies | SaaS Capital, 2026 | [M] |
| NRR median | 82% (P75 97%) | ~2,700 B2B SaaS, $250k ARR floor — self-serve skew, **not comparable** to the survey populations above | ChartMogul, 2025 | [M] |
| Expansion ARR as % of gross new ARR | 40% median; 58% at $50–100M ARR | Private B2B SaaS, N=81, CY2024 | Benchmarkit, 2025 | [M] |
| Subscription gross margin | 81% median | N=76, CY2024 | Benchmarkit, 2025 | [M] |
| CS + support spend | 9% of ARR median | 1,000+ private B2B SaaS, survey Mar 2026 | SaaS Capital, 2026 | [M] |
| B2B SaaS annual logo churn | 3.5% (2.6% voluntary + 0.8% involuntary) | Subscription network, card-billed skew — a category error for enterprise B2B | Recurly, 2025 | [M] |
| SaaS Quick Ratio target | 4.0 | — | Mamoon Hamid, SaaStr, 2015 | [P] |
| LTV:CAC target | 3:1 | — | David Skok, Matrix Partners, c.2010 | [P] |
| Renewal forecast accuracy target | 90–95% | — no disclosed methodology | Vendor claims | [V] |

The ChartMogul and Benchmarkit NRR medians — 82% and 102% — are both correct, for different
populations. Putting them on the same axis without saying so is the most common benchmarking
error in SaaS reporting.

---

## 6. Questions a director asks of the appendix

| Question | Where the answer lives | The trap |
| --- | --- | --- |
| "Is that NRR mix or performance?" | The shift-share decomposition in `commentary-standard.md` | Answering "both" without the basis-point split |
| "What is GRR?" (after you led with NRR) | A2, adjacent by construction | Having to compute it in the room |
| "Does this tie to the financials?" | A1 footer, tie-out line | Any answer other than "$0 variance as at <date>" |
| "What is the denominator on that renewal rate?" | A4, ATR printed beside every rate | Quoting a renewal rate against a GRR benchmark |
| "How many customers is that?" | Every exhibit prints n | Rates without counts |
| "Which cohorts are getting worse?" | A3, read down a column | Presenting a cohort average across unlike ages |
| "How much is the top ten?" | A4 | Not having the Herfindahl or the ex-top-10 retention ready |
| "How accurate was last quarter's call?" | A5 | Accuracy without signed bias |
| "Did anything change in how you calculate this?" | A6 change log | An unlogged change discovered in the room |
| "What would you have to believe for this to get worse?" | The narrative, not the appendix | Having no answer, which reads as not having modelled the downside |

---

## 7. What to leave out

| Leave out | Why |
| --- | --- |
| The migration matrix | Excellent internally, unactionable for a director. Its *output* — the false-green rate — can appear as one sentence in the narrative |
| Per-CSM anything | Board-level personnel detail invites the wrong conversation and damages the internal instrument |
| Health score construction | A board cannot audit an internal score. Use it only as evidence for exposure |
| Activity metrics | QBRs held, touches logged, tickets closed. None are results |
| Any single month | Renewal timing dominates; it will be quoted as a trend |
| A metric with no history | Show eight periods or hold it |
| More than two cuts on one exhibit | It stops being read |
| Your own vendor's marketing benchmarks | Cite the measured studies, or state that no clean benchmark exists |

---

## 8. Diligence mode

When the appendix is going into a data room rather than a board meeting, three things change.

1. **Everything must be reproducible from source.** Ship the queries and the extract dates
   alongside the exhibits. A diligence team will rebuild your bridge; make it easy and it becomes
   a credibility event rather than a risk.
2. **Cohort files, not summaries.** Provide the account-level cohort table — `account_id`,
   `cohort_date`, `arr_t0`, `arr_t1`, `status` — with identifiers pseudonymised. Diligence teams
   discount summary retention numbers by default and stop discounting when they can recompute.
3. **Definition differences from GAAP revenue, written out.** ARR is a non-GAAP operating metric.
   State the reconciliation to recognised revenue, or the first analyst who computes it will
   arrive at a different number and treat yours as the unexplained one.

The failure mode in diligence is not a bad number; it is a number nobody can rebuild. A
defensible 83.4% beats an unverifiable 88%.
