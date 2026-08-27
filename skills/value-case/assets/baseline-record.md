# Baseline Record — <Account> · <value driver>

**One record per value driver.** A record missing a required field does not produce a dollar
figure; it produces a task. Store this next to the success plan, not in an email thread.

| Field | Required | Value |
| --- | --- | --- |
| `account` · `value_driver` | ✅ | |
| `metric_name` | ✅ | |
| `unit` · `direction` (↑ better / ↓ better) | ✅ | |
| `baseline_value` | ✅ | |
| `baseline_period` (≥3 comparable periods) | ✅ | |
| `statistic` (mean / median) and why | ✅ | |
| `periods_excluded` and why | — | |
| `baseline_source` (system · object · filter) | ✅ | |
| `stored_query` | ✅ | |
| `pulled_by` (name, and whether customer or us) | ✅ | |
| `pulled_on` | ✅ | |
| **`rung`** (B1 instrumented · B2 their system · B3 attested estimate · B4 proxy) | ✅ | |
| `estimate_method` (verbatim, if rung B3) | ✅ for B3 | |
| `proxy_source` · `haircut_applied` (if rung B4) | ✅ for B4 | |
| `measurement_owner_customer` (re-runs it) | ✅ | |
| `unit_economics` · `unit_economics_source` | ✅ for a dollar figure | |
| `range_supplied` — and confirmation the **low end** was used | ✅ if a range | |
| `target_value` · `target_date` | ✅ | |
| `attribution_pct` · `attribution_level` (A1–A4) · `set_by` · `set_on` | ✅ for a dollar figure | |
| **`design`** (D1 matched cohort · D2 phased · D3 hold-out · D4 seasonality-controlled · D5 none) | ✅ | |
| `comparison_group` (if D1–D3) | ✅ for D1–D3 | |
| `known_confounders` (list, with dates) | ✅ | |
| `expected_lag` before the metric moves | — | |
| `system_retention_window` | — | |
| `last_validated` · `validated_by` | ✅ | |

---

## Measurement log

Re-run the stored query each quarter. Report movement in both directions.

| Date | Value | Run by | Δ vs baseline | Notes / anything that changed |
| --- | --- | --- | --- | --- |
| | | | | |

---

## Change log

A redefinition applied silently is indistinguishable from moving the goalposts.

| Date | What changed | Agreed by | Prior figures affected | New baseline (if re-based) |
| --- | --- | --- | --- | --- |
| | | | | |

---

## Band this record permits

| Rung + design + unit economics | Band | What you may state |
| --- | --- | --- |
| B1/B2 + D1–D3 + their unit economics + attested α | **Measured** | The dollar figure, as theirs, in a finance review or board pack |
| B2/B3 + their unit economics + attested α | **Attested** | The dollar figure with the attester's name on it |
| B2/B3 + our unit economics (with their written agreement) or D4 | **Evidenced** | A range, not a point. No headline dollar in a finance review |
| B4 proxy, or attribution level A4 | **Indicative** | **No dollar figure.** Unit metrics only, plus the named ask that would fix it |

Print the band, the rung and the design on every artifact this record feeds.
