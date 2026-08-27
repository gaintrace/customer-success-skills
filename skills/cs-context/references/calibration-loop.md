# The Calibration Loop

> Every weight, threshold and band probability shipped with this library was chosen by a human
> with an opinion. That is a legitimate starting point and an illegitimate ending point.
>
> This file describes how the library stops being a well-argued prior and becomes a measured
> model of **your** book — and, just as importantly, what you are allowed to say before that
> has happened.

**Contents**
- [What you may claim, and when](#what-you-may-claim-and-when)
- [The loop](#the-loop)
- [Building the labelled dataset](#building-the-labelled-dataset)
- [Running a calibration](#running-a-calibration)
- [Reading the output](#reading-the-output)
- [Choosing the threshold](#choosing-the-threshold)
- [When calibration says no](#when-calibration-says-no)
- [Keeping it current](#keeping-it-current)

---

## What you may claim, and when

| State | You may say | You must NOT say |
| --- | --- | --- |
| **No calibration** | "At Risk" · "riskier than these other accounts" · "3 of 7 families negative" · a rank | Any probability. Any expected-value figure derived from one. "60% likely to churn" |
| **Calibrated, non-monotonic** | The individual signal findings | Any band probability — the ordering itself is broken |
| **Calibrated, monotonic, ≥8 per band** | "Accounts in this band renewed 61% of the time across 320 accounts and 77 events (calibration of 2026-08-28)" | A probability without the sample size and date attached |

An **ordering** needs far less evidence than a **probability**, and it is what a CSM actually
acts on — they work down a list. Most of the value in this library is available with no
calibration at all. What is not available is the confident-sounding decimal.

## The loop

```
   churn-risk scores accounts  ──────────────►  accounts are worked, renewals land
            ▲                                              │
            │                                              ▼
   .agents/cs-calibration.json  ◄────  calibrate.py  ◄──  outcomes recorded with
   (observed band rates,               (band rates,        DECISION dates and
    fitted weights, cutoff)             AUC, lift,         frozen family scores
            ▲                           threshold)                │
            │                                                     │
            └──────  churn-postmortem: detection lag  ◄───────────┘
                     tunes signal lead times in the signal library
```

Three inputs feed it and each is a discipline, not a script:

1. **Freeze scores before the outcome.** Snapshot every account's family sub-scores at T-90,
   T-180 and T-270 relative to its renewal. Without a frozen snapshot there is nothing to
   calibrate against, and reconstructing scores after the fact leaks the answer into the features.
2. **Record the decision date, not the contract end date.** A customer who churns on 31 December
   having decided on 14 September is a September event. Getting this wrong produces a model that
   has learned your notice period and nothing else.
3. **Use a closed reason taxonomy.** Free-text churn reasons make the postmortem side of the loop
   impossible.

## Building the labelled dataset

One row per account per snapshot date.

```json
{
  "account_id": "ACME",
  "arr": 148000,
  "scored_at": "2025-06-01",
  "decision_date": "2025-08-14",
  "outcome": "churned",
  "arr_after": 0,
  "families": {"usage": 72, "commercial": 90, "relationship": 65,
               "support": 30, "sentiment": null, "billing": 10, "firmographic": 0}
}
```

| Field | Rule |
| --- | --- |
| `scored_at` | Must be strictly before `decision_date`. The script excludes rows that are not and tells you which — that exclusion list is itself a finding about your data |
| `decision_date` | When they decided or served notice. Not the contract end |
| `outcome` | `renewed` · `churned` · `downgraded`. Downgrades count as events — contraction is the leading edge of churn, not a separate thing |
| `arr_after` | Enables dollars-at-risk-captured, which is the metric leadership actually cares about |
| `families` | `null` for a family with no data. **Never zero** — zero means measured-and-clean and will bias the fit toward calling gaps healthy |

Twelve months and 100+ accounts with 30+ events is the realistic minimum. Below that the script
refuses and tells you what to collect.

## Running a calibration

```bash
python3 skills/cs-context/scripts/calibrate.py history.json --capacity 25
python3 skills/cs-context/scripts/calibrate.py history.json --capacity 25 --write
```

`--capacity` is the number of accounts your team can genuinely work per cycle. It is the input
that sets the alert threshold, and it matters more than any statistical criterion — see below.

`--write` produces `.agents/cs-calibration.json`, which `churn-risk` and `renewal-forecast` read
in preference to the library defaults.

## Reading the output

| Section | What to look for | The bad outcome |
| --- | --- | --- |
| **Observed rate by band** | The Δ column against the library defaults | A large negative Δ in High Risk / Critical means the model over-calls risk and CSMs will learn to ignore it |
| **Monotonicity** | Rates must rise across bands | Non-monotonic means the model mis-orders accounts. Stop. Do not publish probabilities. Usually one family is scored backwards or a signal leaks post-decision information |
| **AUC** | ≥0.70 useful · 0.60–0.70 weak · <0.60 not usable | Below 0.60 the ordering is close to random and the whole model needs rebuilding, not tuning |
| **Lift at top decile** | How much better than chance the top 10% is | Below ~1.5× there is little point prioritising by score |
| **ARR captured in top decile** | The number for leadership | A high event-capture rate with low ARR capture means the model finds small churn and misses large |
| **Brier** | Against the no-skill baseline printed beside it | Worse than baseline means the band probabilities are actively misleading |
| **Fitted weights** | The *moves*, not the values | A family moving more than ±10 usually means it is measured badly, not that it matters more |

Accuracy is deliberately never reported. At a 15% base rate, predicting "renews" for everything
is 85% accurate and completely worthless.

## Choosing the threshold

The threshold is not a statistical decision. It is a capacity decision.

You can work N accounts a cycle. Sort by score, take the top N, and read off the precision that
results. If precision is below roughly 30%, CSMs stop believing the alerts, and an alerting
system nobody believes is worse than none — it produces the appearance of coverage while the
real risk goes unworked. At that point you raise the cutoff and work fewer, better accounts;
you do not lower the bar to look thorough.

Optimising F1 instead will hand you a threshold that generates more alerts than your team can
action, which is the most common way a health-score rollout fails.

## When calibration says no

The script blocks below 100 accounts or 30 events, and it is right to. What to do instead:

- Keep using the model as an **ordering**, and say so explicitly in every artifact.
- Never state a probability. Bands only.
- Start the snapshot discipline now — the constraint is almost never model quality, it is that
  nobody froze the scores twelve months ago.
- Run `churn-postmortem` on every loss. Its detection-lag output improves the signal library's
  lead times immediately, without needing a calibration sample.

## Keeping it current

| Cadence | Action |
| --- | --- |
| **Every loss** | `churn-postmortem` → detection lag → update lead times in the signal library |
| **Quarterly** | Re-run `calibrate.py`. Weights drift with pricing, packaging and segment mix |
| **Annually** | Full refit, and re-examine whether the seven families are still the right decomposition |
| **On any pricing or packaging change** | Re-run immediately — the commercial family's meaning has changed |
| **On a segment-mix shift** | Calibrate per segment. A blended model across an SMB tail and an enterprise book fits neither |

Record the calibration date and sample size wherever a probability is published. A number
without them is back to being an opinion with a decimal point.
