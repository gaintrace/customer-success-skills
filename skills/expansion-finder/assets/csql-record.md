# CSQL Record — CS → Sales handoff template

> **INTERNAL.** This is the record that turns a qualified expansion opportunity into a CRM
> opportunity. A CSQL without linked signal evidence is an opinion with a dollar figure
> attached; Sales will reject it, and they will be right to.
>
> Emit one per opportunity. Field names map to `../references/qualification.md` §8.

---

## CSQL — <Account name> · <motion> · <date>

| Field | Value |
| --- | --- |
| `csql_id` | <id> |
| `account_id` / CRM account | <id> · <name> |
| `account_arr` | $<current ARR> |
| `segment` | <segment, per cs-context §3 dollar boundaries> |
| `motion_type` | seat / tier / cross_sell / commit |
| `sku` | <SKU or tier being proposed> |
| `created_by` / `created_at` | <CSM name> · <date> |

### Evidence — the signals that fired

| `signal_id` | Signal | Tier | Evidence (system · field · window) | Age (days) |
| --- | --- | --- | --- | --- |
| | | | | |

**Independent families represented:** <N of 7> — <list them>.
**Combination rule satisfied:** <yes — one T1/T2/T3 / yes — two T4 + one T5 / **no, do not route**>.

### Health gate

| Check | Result | Evidence |
| --- | --- | --- |
| Health band | <Secure / Watch> | <source · date> |
| Hard blocks evaluated | <none fired / list> | <evidence per block> |
| Cooldowns active | <none / list with expiry date> | |
| `health_gate_passed` | **<true / false>** | <one-line reason> |

If `health_gate_passed = false`, this record is not routed. It is filed with the refusal
paragraph and a re-test date.

### Qualification

| Gate | Status | Evidence | Fix · owner · by |
| --- | --- | --- | --- |
| 1. Constraint is countable | | | |
| 2. Customer-side owner feels it | | | |
| 3. Economic buyer mapped | | | |
| 4. Value proven within 120 days | | | |
| 5. Budget path exists | | | |

### Sizing

| | Units | Unit price | Discount | Opportunity ARR |
| --- | --- | --- | --- | --- |
| `opportunity_arr_floor` | | | | $ |
| `opportunity_arr_base` **(recommended)** | | | | $ |
| `opportunity_arr_ceiling` | | | | $ |

**Arithmetic:** <every intermediate number, one line per step>
**For tier motions — indifference point:** <usage level> · current <level> · crosses in <N>
months · **honest recommendation: <upgrade / stay>**
**For commit motions — billings delta:** <$> · **committed ARR delta:** <$>

### Ranking

| Factor | Value | Basis |
| --- | --- | --- |
| Propensity | | <tier prior + N independent families> |
| Timing fit | | <days to opt-out> |
| Relationship readiness | | <sponsor met ≤90d / champion only / cold / single-threaded> |
| Health gate | | <band> |
| Value factor | | <days since validated outcome> |
| **Ranked value** | **$** | product of the above × Opportunity ARR |
| `csm_hours_estimate` | | |
| **Throughput** | **$ / CSM-hour** | ranked value ÷ hours |

### Relationship and timing

| Field | Value |
| --- | --- |
| `economic_buyer_contact_id` | <id> · <name, title> · last contact <date> |
| Champion | <name, title> · <status> |
| Introduction path (if the buyer is not mapped) | <named introducer> · <requested by date> |
| `renewal_date` | <date> |
| `notice_period_days` | <N> |
| **`opt_out_deadline`** | **<date>** · `days_to_opt_out` <N> |
| Timing decision | co-term / run separately / defer to <date> — <rationale> |

### Value evidence

| Field | Value |
| --- | --- |
| `value_evidence_url` | <link to the artifact delivered before the ask> |
| `value_evidence_date` | <date> · <N> days old |
| Validated by | <their name, title> |

### Action plan

| # | Action | Owner | By | Expected effect | Success measure |
| --- | --- | --- | --- | --- | --- |
| 1 | | | | | |
| 2 | | | | | |
| 3 | | | | | |

### Disposition — completed by Sales

| Field | Value |
| --- | --- |
| `accepted_at` / `rejected_at` | |
| Rejection reason (if rejected) | <qualification gap / sizing / timing / ownership / other> |
| CRM opportunity id | |
| `closed_at` · outcome | won / lost + reason |
| Closed ARR vs `opportunity_arr_base` | $ vs $ — variance <%> |

> Rejections are data, not friction. If Sales rejects more than ~30% of CSQLs, the
> qualification criteria are wrong — review `../references/qualification.md` §3 before
> reviewing the reps.
