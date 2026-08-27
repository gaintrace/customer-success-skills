# The Normalised CS Schema

> Every skill in this library reasons over these nine entities. Map your sources into this
> shape once, in `cs-context`, and every downstream skill works without re-deriving joins.

**Contents**
1. [Design rules](#1-design-rules)
2. [Entities](#2-entities)
3. [Identity resolution](#3-identity-resolution)
4. [Derived measures](#4-derived-measures-computed-not-stored)
5. [Reference SQL](#5-reference-sql)
6. [Mapping worksheet](#6-mapping-worksheet)

---

## 1. Design rules

- **Account is the grain of every CS decision.** Users, tickets and events roll up to it. If
  a source cannot be rolled up to an account, it cannot be used for account-level risk.
- **Everything is dated.** No field without an as-of date or an event timestamp.
- **Money is stored in a single reporting currency** with the FX rate date recorded.
- **Nulls are not zeros.** `usage_daily.active_users = 0` means measured-and-empty;
  `NULL` means not-measured. Conflating them creates false-red accounts.
- **Store the decision date, not just the effect date.** Churn on 2026-12-31 that was decided
  on 2026-09-14 is a September event for prediction purposes. This one distinction determines
  whether a churn model is learning anything or just memorising the notice period.

---

## 2. Entities

### `account`

| Field | Type | Notes |
| --- | --- | --- |
| `account_id` | string | Canonical ID. Choose one source of truth (usually CRM) and map everything to it. |
| `name` | string | |
| `crm_id`, `billing_id`, `product_org_id`, `support_org_id` | string | The foreign keys into each source. Store them all. |
| `segment` | enum | Uses the dollar boundaries from `cs-context` §3 |
| `arr` | decimal | Current annualised recurring revenue, reporting currency |
| `arr_as_of` | date | |
| `owner_csm`, `owner_am` | string | |
| `status` | enum | `active` `at_risk` `churned` `won_back` `trial` |
| `start_date` | date | First paid day — drives tenure and cohort |
| `tenure_days` | int | Derived |
| `industry`, `employee_count`, `country` | string/int | Firmographic; refresh quarterly |
| `is_internal` | bool | Test/sandbox/employee accounts. **Exclusion rule must be documented.** |
| `parent_account_id` | string | For subsidiaries and multi-entity enterprises |

### `contact`

| Field | Type | Notes |
| --- | --- | --- |
| `contact_id`, `account_id` | string | |
| `email`, `name`, `title` | string | |
| `role` | enum | `economic_buyer` `champion` `coach` `admin` `power_user` `user` `blocker` `technical_evaluator` `procurement` |
| `influence` | 1–5 | |
| `sentiment` | enum | `advocate` `positive` `neutral` `negative` `hostile` `unknown` |
| `is_active` | bool | |
| `last_seen_product` | date | From product analytics |
| `last_interaction` | date | Email/call/meeting, whichever is latest |
| `email_status` | enum | `ok` `soft_bounce` `hard_bounce` — hard bounce is the single strongest departure signal |
| `departed_at` | date | When departure was detected |

### `subscription`

| Field | Type | Notes |
| --- | --- | --- |
| `subscription_id`, `account_id` | string | |
| `product`, `plan`, `tier` | string | Multi-product companies need one row per product |
| `term` | enum | `monthly` `annual` `multi_year` |
| `start_date`, `end_date` | date | |
| `renewal_date` | date | The date the renewal decision lands |
| `notice_period_days` | int | |
| **`opt_out_deadline`** | date | `renewal_date − notice_period_days`. **The most operationally important date in CS and the one most often missing.** |
| `auto_renew` | bool | |
| `auto_renew_changed_at` | timestamp | A change here is a near-certain risk signal |
| `seats_purchased`, `seats_provisioned` | int | Distinguish contracted from deployed |
| `usage_entitlement`, `usage_consumed` | decimal | For metered plans |
| `arr` | decimal | |
| `discount_pct`, `discount_expires` | decimal/date | Expiring discounts drive renewal friction |
| `uplift_pct` | decimal | Contracted escalator |
| `is_ramped` | bool | Ramp deals distort NRR — flag them |

### `usage_daily` (account × day rollup — the workhorse)

| Field | Type |
| --- | --- |
| `account_id`, `date` | string, date |
| `active_users` | int |
| `sessions` | int |
| `core_actions` | int — the activation-event count from `cs-context` §5 |
| `feature_breadth` | int — distinct features touched |
| `api_calls` | int |
| `data_volume` | decimal |
| `admin_actions` | int |
| `integrations_active` | int |

### `usage_event` (raw, for drill-down)

`event_id · account_id · contact_id · event_name · timestamp · properties(json)`

### `ticket`

| Field | Notes |
| --- | --- |
| `ticket_id`, `account_id`, `contact_id` | |
| `created_at`, `first_response_at`, `resolved_at` | Compute FRT and TTR |
| `priority`, `status`, `type` | `type` ∈ `bug` `question` `feature_request` `incident` `escalation` |
| `sla_breached` | bool |
| `satisfaction` | enum + free text |
| `sentiment` | −1..1, from text |
| `reopened_count` | int — a reopen is worth more than a new ticket |
| `linked_issue_id` | Jira/Linear key |

### `interaction`

Every human touch, one row. This table is what makes relationship analysis possible.

| Field | Notes |
| --- | --- |
| `interaction_id`, `account_id` | |
| `type` | `email` `call` `meeting` `slack` `qbr` `onsite` `webinar` `survey` |
| `direction` | `inbound` `outbound` |
| `timestamp` | |
| `internal_participants`, `customer_participants` | arrays of contact_id — **the multithreading measure** |
| `response_latency_hours` | For inbound replies to our outbound |
| `sentiment` | −1..1 |
| `commitments` | array of `{who, what, due}` — extracted from notes/transcripts |
| `summary`, `source_ref` | |

### `opportunity`

| Field | Notes |
| --- | --- |
| `opportunity_id`, `account_id` | |
| `type` | `renewal` `expansion` `cross_sell` `new` |
| `stage`, `forecast_category` | Forecast category must map to the rubric in `renewal-forecast` |
| `amount`, `close_date`, `probability` | |
| `created_at`, `stage_changed_at` | Stage age is a stall signal |
| `competitor` | string |
| `loss_reason`, `loss_reason_detail` | |

### `invoice`

| Field | Notes |
| --- | --- |
| `invoice_id`, `account_id` | |
| `issued_at`, `due_at`, `paid_at` | `paid_at − due_at` is days-late, a real commercial signal |
| `amount`, `status` | `paid` `open` `overdue` `disputed` `uncollectible` |
| `payment_failures` | int |
| `payment_method_status` | `valid` `expiring` `expired` `removed` |

### `churn_event` (labels — required for any predictive work)

| Field | Notes |
| --- | --- |
| `account_id` | |
| **`decision_date`** | When the customer decided/notified. **Use this as the label date.** |
| `effective_date` | When service actually ended |
| `type` | `full_churn` `downgrade` `partial_seat_reduction` `non_renewal` `involuntary` |
| `arr_lost` | decimal |
| `primary_reason`, `secondary_reason` | From a fixed taxonomy — free text destroys analysis |
| `was_savable` | bool + rationale |
| `earliest_detectable_signal`, `earliest_detectable_date` | Populated by `churn-postmortem`; this is how the risk model improves |

---

## 3. Identity resolution

Resolving product users to accounts is where CS data pipelines break. Record the rule and
its exceptions in `cs-context` §10.

**Resolution ladder — try in order, stop at first hit:**

1. Explicit `org_id` / `workspace_id` / `tenant_id` sent by the product → CRM account mapping table
2. CRM contact email exact match
3. Email domain match against `account.domains[]`
4. Billing customer ID → CRM account
5. Manual override table

**Known breakage, and what it does to your numbers:**

| Case | Effect | Handling |
| --- | --- | --- |
| Free-email users (gmail.com) at a paying account | Under-counts active users → false red | Explicit contact mapping; never domain-match free providers |
| Multi-domain enterprises (acme.com, acme.co.uk, acmegroup.com) | Splits one account into several → understates ARR and health | Maintain `account.domains[]` |
| Agencies/consultants using the product for a client | Attributes usage to the wrong account | Flag `is_external_collaborator` |
| Subsidiaries with separate contracts | Rolls up incorrectly | `parent_account_id` and decide the reporting grain |
| Employees testing in production | Inflates usage → false green | `is_internal` exclusion rule |
| Shared/service accounts | One "user" hides ten humans | Flag; exclude from per-seat utilisation |
| Post-acquisition domain change | Looks like total usage collapse | Watch for domain migrations before declaring churn risk |

**Record the join rate.** Below 90%, note it. Below 80%, usage-derived risk scores must be
labelled Low confidence — the missing users are not randomly distributed.

---

## 4. Derived measures (computed, not stored)

| Measure | Formula |
| --- | --- |
| Licence utilisation | `distinct_active_users_30d / seats_purchased` |
| Provisioning gap | `seats_purchased − seats_provisioned` |
| Stickiness | `DAU / MAU` (account-level) |
| Usage trend | slope of `core_actions` over trailing 8 weeks ÷ mean, i.e. normalised slope |
| Usage delta | `mean(core_actions, last 30d) / mean(core_actions, prior 30d) − 1` |
| Adoption breadth | `distinct_features_used_30d / features_in_plan` |
| Engagement recency | `today − max(interaction.timestamp)` |
| Multithreading depth | count of distinct `customer_participants` across interactions in 90d |
| Buyer-side engagement | interactions in 90d where participants include an `economic_buyer` or `champion` |
| Reply latency trend | 30d mean `response_latency_hours` vs prior 90d mean |
| Support load | `tickets_30d / seats_purchased` |
| Escalation density | `escalations_90d / tickets_90d` |
| Days to opt-out | `opt_out_deadline − today` |
| Days to renewal | `renewal_date − today` |
| Payment health | count of `payment_failures` 180d + mean days-late |
| Time-to-first-value | `first_activation_event_date − start_date` |

---

## 5. Reference SQL

Warehouse-agnostic; adjust date functions. Written against the entity names above.

**Usage decay — accounts whose core action volume dropped ≥40% in 30 days**

```sql
WITH w AS (
  SELECT account_id,
         AVG(CASE WHEN date >= CURRENT_DATE - 30 THEN core_actions END) AS cur,
         AVG(CASE WHEN date >= CURRENT_DATE - 60
                   AND date <  CURRENT_DATE - 30 THEN core_actions END) AS prev
  FROM usage_daily
  WHERE date >= CURRENT_DATE - 60
  GROUP BY account_id
)
SELECT a.name, a.arr, w.prev, w.cur,
       ROUND((w.cur - w.prev) / NULLIF(w.prev,0) * 100, 1) AS pct_change
FROM w JOIN account a USING (account_id)
WHERE w.prev > 0 AND w.cur / w.prev <= 0.60 AND a.is_internal = FALSE
ORDER BY a.arr DESC;
```

**Renewals in the opt-out window, with health context**

```sql
SELECT a.name, a.arr, s.renewal_date, s.opt_out_deadline,
       s.opt_out_deadline - CURRENT_DATE AS days_to_opt_out,
       s.auto_renew, s.auto_renew_changed_at,
       ROUND(u.active_30d::numeric / NULLIF(s.seats_purchased,0), 2) AS utilisation
FROM subscription s
JOIN account a USING (account_id)
LEFT JOIN (
  SELECT account_id, COUNT(DISTINCT contact_id) AS active_30d
  FROM usage_event WHERE timestamp >= CURRENT_DATE - 30 GROUP BY 1
) u USING (account_id)
WHERE s.renewal_date BETWEEN CURRENT_DATE AND CURRENT_DATE + 180
ORDER BY s.opt_out_deadline;
```

**Seat expansion candidates — utilisation ≥85% and healthy support posture**

```sql
SELECT a.name, a.arr, s.seats_purchased, u.active_30d,
       ROUND(u.active_30d::numeric / NULLIF(s.seats_purchased,0), 2) AS utilisation,
       t.open_escalations
FROM subscription s
JOIN account a USING (account_id)
JOIN (SELECT account_id, COUNT(DISTINCT contact_id) active_30d
      FROM usage_event WHERE timestamp >= CURRENT_DATE - 30 GROUP BY 1) u USING (account_id)
LEFT JOIN (SELECT account_id, COUNT(*) open_escalations FROM ticket
           WHERE type='escalation' AND status <> 'closed' GROUP BY 1) t USING (account_id)
WHERE u.active_30d::numeric / NULLIF(s.seats_purchased,0) >= 0.85
  AND COALESCE(t.open_escalations,0) = 0
ORDER BY a.arr DESC;
```

**Single-threaded accounts — one contact carrying the whole relationship**

```sql
SELECT a.name, a.arr, COUNT(DISTINCT cp) AS distinct_contacts_90d
FROM interaction i
CROSS JOIN LATERAL UNNEST(i.customer_participants) AS cp
JOIN account a ON a.account_id = i.account_id
WHERE i.timestamp >= CURRENT_DATE - 90
GROUP BY a.name, a.arr
HAVING COUNT(DISTINCT cp) <= 1
ORDER BY a.arr DESC;
```

**Silence — no interaction in 45+ days, weighted by ARR**

```sql
SELECT a.name, a.arr, MAX(i.timestamp)::date AS last_touch,
       CURRENT_DATE - MAX(i.timestamp)::date AS days_silent
FROM account a LEFT JOIN interaction i USING (account_id)
WHERE a.status = 'active' AND a.is_internal = FALSE
GROUP BY a.name, a.arr
HAVING COALESCE(CURRENT_DATE - MAX(i.timestamp)::date, 999) >= 45
ORDER BY a.arr DESC;
```

**ARR bridge for a period**

```sql
SELECT
  SUM(CASE WHEN movement='new'         THEN arr_delta ELSE 0 END) AS new_arr,
  SUM(CASE WHEN movement='expansion'   THEN arr_delta ELSE 0 END) AS expansion,
  SUM(CASE WHEN movement='contraction' THEN arr_delta ELSE 0 END) AS contraction,
  SUM(CASE WHEN movement='churn'       THEN arr_delta ELSE 0 END) AS churn,
  SUM(CASE WHEN movement='reactivation'THEN arr_delta ELSE 0 END) AS reactivation
FROM arr_movement
WHERE effective_date BETWEEN :period_start AND :period_end;
```

---

## 6. Mapping worksheet

Fill one row per source in `cs-context` §9.

| Source | Entity it feeds | Account key it uses | Refresh latency | History depth | Lossy in what way |
| --- | --- | --- | --- | --- | --- |
| Salesforce | account, contact, opportunity, subscription | `Account.Id` | 15 min | since 2021 | Contract fields hand-maintained; `AutoRenew__c` often stale |
| Stripe | subscription, invoice | `customer.metadata.sf_account_id` | real-time | since 2022 | Seat changes not always mirrored to CRM |
| Amplitude | usage_event, usage_daily | `group:account_id` | hourly | 24 months | Anonymous events unattributed |
| Zendesk | ticket | `organization_id` | 5 min | since 2020 | Org mapping missing for ~8% of tickets |
| Gmail | interaction | domain match | real-time | 12 months | Only CSM mailboxes connected |
