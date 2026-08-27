# Data Source Map

> Where every customer success signal actually lives: the tool, the object, the field, and the
> gotcha. Read this when you need to extract a signal from a specific system, or when you are
> mapping a new source into the normalised schema.
>
> Pair with `normalized-schema.md` (the target shape and the reference SQL) and
> `signal-library.md` (what each extracted field means for risk).
>
> **Before trusting any field below, check two things:** when the source last synced, and
> whether the field is system-maintained or hand-maintained. Hand-maintained CRM contract
> fields — renewal date, notice period, auto-renew flag, champion designation — are the most
> commonly stale data in customer success, and every one of them governs a decision.

---


**Purpose.** Runtime reference for an agent extracting customer-success signal from real systems. For every tool: the objects/tables, the exact field names, the CS signal each yields, API/query notes, and the gotchas that silently corrupt analysis.

**Verification legend** (applied per row/section):
- `[V]` = field name/enum verified against the vendor's own API reference during this research pass (Aug 2026). URL in §12.
- `[K]` = from prior model knowledge of the API; plausible and widely used, but **not** re-verified in this pass. Treat as "check before hard-coding."
- `[ROT]` = practitioner rule-of-thumb threshold, not a measured benchmark. Never present as a statistic.
- `[BM]` = measured benchmark with named source + year.

**Non-negotiable rule for the agent:** never emit a health score, churn-risk claim, or renewal forecast until §11 (Data Quality Gate) has been run and its output reported alongside the analysis. An unqualified number computed on 40%-covered, 3-weeks-stale usage data is worse than no number.

---

**Contents**

- [1. The target shape](#1-the-target-shape)
- [2. CRM — Salesforce](#2-crm-salesforce)
- [3. CRM — HubSpot](#3-crm-hubspot)
- [4. Billing & Revenue](#4-billing-revenue)
- [5. Support — Zendesk & Intercom](#5-support-zendesk-intercom)
- [6. Product Analytics — Mixpanel / Amplitude / PostHog / Segment](#6-product-analytics-mixpanel-amplitude-posthog-segment)
- [7. Communications — Slack, Email, Meetings, Calls](#7-communications-slack-email-meetings-calls)
- [8. Product Feedback & Engineering — Jira / Linear / Pendo / Appcues](#8-product-feedback-engineering-jira-linear-pendo-appcues)
- [9. Warehouse Layer — Snowflake / BigQuery](#9-warehouse-layer-snowflake-bigquery)
- [10. Identity Resolution](#10-identity-resolution)
- [11. Data Quality Gate — Run Before Any Analysis](#11-data-quality-gate-run-before-any-analysis)
- [12. Example SQL — Six Core CS Queries](#12-example-sql-six-core-cs-queries)
- [13. Signal → Source Priority Matrix](#13-signal-source-priority-matrix)
- [14. Source Register](#14-source-register)

---

## 1. The target shape

Every source below is mapped into the nine entities defined in
[`normalized-schema.md`](normalized-schema.md) — `account` · `contact` · `subscription` ·
`usage_daily` · `usage_event` · `ticket` · `interaction` · `opportunity` · `invoice` ·
`churn_event`. That file is the single definition of the field names, the identity-resolution
ladder and the reference SQL; this file is only concerned with **where each field comes from
in each tool, and what goes wrong on the way**.

The mapping worksheet at the end of `normalized-schema.md` is where you record the result
for your own stack.

## 2. CRM — Salesforce

Standard field API names verified against the Salesforce Object Reference (v254, Summer '26) `[V]`.

### 2.1 Objects → signals
| Object | Fields | CS signal |
|---|---|---|
| `Account` | `Id`, `Name`, `Website`, `ParentId`, `OwnerId`, `Type`, `Industry`, `NumberOfEmployees`, `LastActivityDate`, `AnnualRevenue` `[K]` | Hierarchy for roll-up; `LastActivityDate` = relationship staleness; `ParentId` is the #1 cause of double-counted ARR |
| `Opportunity` | `StageName`, `Amount`, `CloseDate`, `Probability`, `Type`, `IsClosed`, `IsWon`, `ForecastCategory`, `ForecastCategoryName`, `ExpectedRevenue`, `TotalOpportunityQuantity`, `NextStep`, `ContractId`, `LastActivityDate`, `LastStageChangeDate`, `HasOpenActivity`, `HasOverdueTask`, `PushCount` `[V]` | Renewal/expansion pipeline. `PushCount` = number of times `CloseDate` slipped — the single best leading indicator of a soft renewal. `HasOverdueTask=true` + `Type='Renewal'` + close date <60d = execution risk |
| `OpportunityFieldHistory` | `Field`, `OldValue`, `NewValue`, `CreatedDate` `[K]` | Reconstructs stage regression and amount reductions. Only populated for fields with history tracking enabled (max 20 fields/object) |
| `Contract` | `Status`, `StatusCode`, `StartDate`, `EndDate`, `ContractTerm`, `AccountId`, `ContractNumber`, `ActivatedDate`, `CompanySignedDate`, `CustomerSignedDate`, `OwnerExpirationNotice`, `SpecialTerms` `[V]` | True renewal date; `OwnerExpirationNotice` = notice-period window (often 30/60/90 days) — **the real deadline is `EndDate` minus notice period**, not `EndDate` |
| `Case` | `Status`, `Priority`, `Origin`, `Type`, `Reason`, `IsEscalated`, `IsClosed`, `ClosedDate`, `AccountId`, `ContactId`, `AssetId`, `EntitlementId`, `SlaStartDate`, `SlaExitDate`, `MilestoneStatus`, `ParentId`, `Subject`, `SuppliedEmail` `[V]` | Support load, escalation count, SLA breach (`MilestoneStatus='Violated'`), `Reason` distribution reveals product vs. training vs. billing pain |
| `Asset` | `AccountId`, `Product2Id`, `Status`, `Quantity`, `InstallDate`, `UsageEndDate`, `Price`, `LifecycleStartDate`, `LifecycleEndDate`, `CurrentQuantity`, `CurrentAmount` `[K]` | Product-level entitlement when Salesforce is the subscription system of record (Revenue Cloud/CPQ). `CurrentQuantity` vs `Quantity` = seat drift |
| `Task` / `Event` | `WhatId`, `WhoId`, `AccountId`, `ActivityDate`, `Status`, `Subject`, `Type`, `CallDurationInSeconds`, `IsClosed`, `TaskSubtype`, `EventSubtype`, `DurationInMinutes` `[K]` | Touch cadence, overdue commitments, meeting frequency. `WhatId` may point to Opportunity — must walk to Account |
| `ContactRole` / `OpportunityContactRole` | `Role`, `IsPrimary` `[K]` | Multi-threading depth and buyer identification |
| Custom renewal objects | Commonly `Renewal__c`, `Subscription__c`, `SBQQ__Subscription__c` (Salesforce CPQ), `blng__…` (Billing) `[K]` | In CPQ shops, `SBQQ__Subscription__c.SBQQ__Quantity__c`, `SBQQ__SubscriptionEndDate__c`, `SBQQ__RenewalQuantity__c` carry the true seat/term picture |

### 2.2 Query notes
- SOQL relationship traversal: `SELECT Id, Account.Name, Account.Parent.Name FROM Opportunity WHERE Type='Renewal' AND CloseDate = NEXT_N_DAYS:90` — date literals (`NEXT_N_DAYS:n`, `LAST_N_DAYS:n`, `THIS_FISCAL_QUARTER`) avoid timezone math but resolve in the **org's** timezone, not UTC. `[K]`
- Bulk API 2.0 for >50k rows; REST `queryMore` otherwise. Field-level security silently omits fields your integration user can't see — this returns *fewer columns*, not an error. Always assert expected column set. `[K]`
- `Type` picklist on Opportunity is org-configurable. `'Renewal'` is a *convention*, not a standard value. Discover actual values via Describe (`/services/data/vXX.X/sobjects/Opportunity/describe`) rather than assuming. `[K]`

### 2.3 Gotchas
1. **CRM `Amount` ≠ ARR.** It is often TCV on multi-year deals, or blank when line items drive the number (`HasOpenActivity`/`HasOpportunityLineItem`). Prefer the billing system for revenue.
2. **`LastActivityDate` only updates from logged Tasks/Events.** If the team lives in Gmail without Einstein Activity Capture / logging, this field is a fiction. Cross-check against actual email data (§7).
3. **Closed-won renewal opportunities are often created *after* the renewal closes**, so pipeline coverage looks artificially thin 90 days out.
4. **Deleted records** sit in the Recycle Bin for 15 days and reappear in `queryAll`. Use `IsDeleted = false`. `[K]`
5. **Currency:** in multi-currency orgs, `Amount` is in the record currency (`CurrencyIsoCode`); `ConvertCurrency(Amount)` or the `DatedConversionRate` object is needed for comparable totals.

---

## 3. CRM — HubSpot

Internal property names verified against HubSpot's default-property docs `[V]`.

| Object | Key properties (internal names) | CS signal |
|---|---|---|
| Companies | `name`, `domain`, `hs_object_id`, `lifecyclestage`, `hubspot_owner_id`, `num_associated_contacts`, `notes_last_contacted`, `notes_last_updated`, `hs_last_sales_activity_timestamp`, `hs_num_open_deals`, `createdate`, `hs_lastmodifieddate`, `annualrevenue`, `numberofemployees` `[K for the last six]` | Account master, relationship recency, contact breadth |
| Deals | `dealstage`, `pipeline`, `amount`, `closedate`, `dealtype` (default values `New Business` / `Existing Business`), `hs_deal_stage_probability`, `hs_forecast_amount`, `hs_is_closed_won`, `hs_lastmodifieddate`, `notes_last_contacted`, `hs_acv`, `hs_arr`, `hs_mrr`, `hs_tcv`, `engagements_last_meeting_booked`, `num_associated_contacts`, `days_to_close` `[V]` | Renewal/expansion pipeline. `hs_arr`/`hs_mrr`/`hs_acv`/`hs_tcv` require Sales Hub Pro/Enterprise — **null on Starter tiers**, a very common silent gap |
| Tickets | `hs_pipeline`, `hs_pipeline_stage`, `hs_ticket_priority`, `hs_ticket_category`, `subject`, `content`, `source_type`, `time_to_close`, `time_to_first_agent_reply`, `hs_resolution`, `createdate`, `closed_date`, `hubspot_owner_id`, `hs_num_times_contacted`, `hs_last_message_received_at` `[V]` | Support burden, responsiveness, SLA state (`Due soon` / `Overdue` / `SLA completed on time` / `SLA completed late`) `[V]` |
| Contacts | `email`, `lifecyclestage`, `hs_lead_status`, `hs_email_last_reply_date`, `hs_email_bounce`, `hs_last_sales_activity_timestamp`, `associatedcompanyid` `[K]` | Champion activity, departure signal via bounce |
| Engagements | `hs_engagement_type` (`EMAIL`,`CALL`,`MEETING`,`NOTE`,`TASK`), `hs_timestamp`, `hs_meeting_outcome`, `hs_call_duration`, `hs_email_direction` `[K]` | Touch cadence, meeting outcomes (`SCHEDULED`/`COMPLETED`/`NO_SHOW`/`CANCELED`) |

**API/query notes.** CRM v3: `GET /crm/v3/objects/{companies|deals|tickets}` with `?properties=a,b,c` — **properties not explicitly requested are not returned**, and history requires `propertiesWithHistory`. `POST /crm/v3/objects/deals/search` supports `filterGroups` (AND within a group, OR across groups), max 5 groups × 6 filters, and returns max 10,000 records per query — paginate by sorting on `hs_lastmodifieddate` and windowing. Associations use the v4 API (`/crm/v4/objects/{objectType}/{id}/associations/{toObjectType}`). `[K]`

**Gotchas.** (a) HubSpot deal stages are pipeline-scoped — the same stage *label* has different `dealstage` internal IDs across pipelines; always join through the pipelines API. (b) `lifecyclestage` never moves backward automatically; a churned customer often still reads `customer`. (c) Search API is eventually consistent — records may take seconds to minutes to be searchable after write.

---

## 4. Billing & Revenue

### 4.1 Stripe `[V — docs.stripe.com/api, fetched Aug 2026]`
| Object | Fields | CS signal |
|---|---|---|
| `subscription` | `status` (`incomplete`, `incomplete_expired`, `trialing`, `active`, `past_due`, `canceled`, `unpaid`, `paused`), `cancel_at_period_end`, `cancel_at`, `canceled_at`, `cancellation_details{comment, feedback, reason}`, `collection_method` (`charge_automatically`/`send_invoice`), `days_until_due`, `discounts[]`, `items.data[].quantity`, `items.data[].price`, `items.data[].current_period_start/end`, `pause_collection`, `pending_update`, `schedule`, `trial_start`, `trial_end`, `start_date`, `ended_at`, `metadata` | Voluntary-churn intent (`cancel_at_period_end=true` is the highest-precision churn signal that exists); seat change via `items.data[].quantity`; involuntary risk via `past_due`/`unpaid`; `cancellation_details.feedback` gives self-reported reason |
| `invoice` | `status` (`draft`,`open`,`paid`,`uncollectible`,`void`), `attempt_count`, `attempted`, `next_payment_attempt`, `auto_advance`, `collection_method`, `due_date`, `amount_due`, `amount_paid`, `amount_remaining`, `amount_overpaid`, `total`, `subtotal`, `billing_reason` (`subscription_create`, `subscription_cycle`, `subscription_update`, `subscription_threshold`, `manual`, `quote_accept`, `upcoming`, `automatic_pending_invoice_item_invoice`), `status_transitions{finalized_at, paid_at, voided_at, marked_uncollectible_at}`, `last_finalization_error`, `discounts[]`, `period_start`, `period_end`, `parent` | Dunning depth (`attempt_count` ≥ 2 = active involuntary-churn risk); `billing_reason='subscription_update'` marks mid-term expansion/contraction; `uncollectible` = write-off |
| `payment_intent` | `status`, `last_payment_error{code, decline_code, message}`, `amount`, `next_action` `[K]` | Decline reason drives the play: `insufficient_funds` → retry timing; `card_declined`/`expired_card` → card-update outreach; `do_not_honor` → bank contact |
| `customer` | `id`, `email`, `name`, `balance`, `delinquent`, `metadata`, `invoice_settings.default_payment_method` `[K]` | `delinquent=true` = one or more unpaid invoices |
| Events / webhooks | `customer.subscription.updated`, `customer.subscription.deleted`, `customer.subscription.paused`, `invoice.payment_failed`, `invoice.payment_action_required`, `charge.dispute.created` `[K]` | Real-time triggers |

**Critical Stripe gotchas.**
1. **Period fields moved.** In current API versions `current_period_start` / `current_period_end` are on the **subscription item** (`items.data[].current_period_start`), not the top-level subscription. Code written against older versions silently reads `null`. `[V — confirmed in the Aug 2026 Subscription object example]`
2. **`invoice.subscription` moved** under `invoice.parent` (subscription details). The Aug 2026 invoice example has no top-level `subscription` key. `[V]`
3. `canceled_at` on a `cancel_at_period_end` subscription is the timestamp of the *update request*, not the end of the period. Use `cancel_at`/`ended_at` for the effective date. `[V — explicit in Stripe docs]`
4. `pause_collection` does **not** change `status`; a paused-collection subscription still reads `active`. A separate `status='paused'` exists only for trials that end without a payment method. `[V]`
5. `attempt_count` increments only for automatic retries; manual attempts after the first don't advance the retry schedule. `[V]`
6. All amounts are integers in the smallest currency unit. ChartMogul likewise returns cents. Zero-decimal currencies (JPY, KRW) break naive `/100`.

### 4.2 Paddle Billing `[V]`
`subscription.status` ∈ `active`, `canceled`, `past_due`, `paused`, `trialing`. Key fields: `customer_id`, `business_id`, `currency_code`, `started_at`, `first_billed_at`, `next_billed_at`, `paused_at`, `canceled_at`, `collection_mode`, `discount`, `current_billing_period{starts_at, ends_at}`, `billing_cycle`, `scheduled_change{action, effective_at, resume_at}`, `items[]{price, quantity, status, recurring, previously_billed_at, next_billed_at}`, `management_urls`, `custom_data`.

**Signal:** `scheduled_change.action = 'cancel'` is Paddle's equivalent of Stripe's `cancel_at_period_end` — the pending-churn flag. `scheduled_change.action='pause'` with a `resume_at` is a softer risk signal. `items[].quantity` deltas = seat expansion/contraction. `custom_data` is where most teams stash their internal `account_id` — check it first for identity resolution.

**Gotchas:** Paddle Classic and Paddle Billing are different APIs with different object shapes; confirm which is in use. Paddle is a Merchant of Record, so its `transactions` include tax the vendor never recognizes as revenue — never use gross transaction amount as ARR.

### 4.3 ChartMogul `[V]`
| Endpoint | Returns | CS signal |
|---|---|---|
| `GET /v1/metrics/all` | Per-interval: `date`, `mrr`, `arr`, `customer-churn-rate`, `mrr-churn-rate`, `ltv`, `customers`, `asp`, `arpa`, plus `*-percentage-change`; summary block with current/previous | Portfolio trend |
| `GET /v1/metrics/mrr` | `date`, `mrr`, `percentage-change`, **`mrr-new-business`, `mrr-expansion`, `mrr-contraction`, `mrr-churn`, `mrr-reactivation`** | The MRR movement waterfall — the correct decomposition for NRR/GRR analysis |
| `GET /v1/customers`, `/v1/customers/{uuid}/subscriptions`, `/v1/invoices`, `/v1/activities` | Source + calculated data | Per-account movement history |

Params on metrics endpoints: `start-date`, `end-date` (required, ISO-8601), `interval` (`day`/`week`/`month` default/`quarter`/`year`), `geo`, `plans`, `filters`. **All monetary values are integers in cents.**

**Gotchas:** ChartMogul's `mrr-churn` is *revenue lost from cancellations only*; downgrades land in `mrr-contraction`. Conflating the two overstates churn. Reactivation MRR is excluded from new business — a portfolio with heavy win-back will look flat on new business while growing. Metrics are recomputed on import; a backfill changes historical numbers, so cache with a `computed_at`.

### 4.4 Revenue signal precedence
When systems disagree, use this order: **billing system > revenue analytics (ChartMogul) > CRM contract object > CRM opportunity amount > spreadsheet.** Record which one you used in the output.

---

## 5. Support — Zendesk & Intercom

### 5.1 Zendesk `[V — developer.zendesk.com, fetched Aug 2026]`
| Object | Fields | CS signal |
|---|---|---|
| `ticket` | `status` (`new`,`open`,`pending`,`hold`,`solved`,`closed`), `custom_status_id`, `priority` (`urgent`,`high`,`normal`,`low`), `type` (`problem`,`incident`,`question`,`task`), `requester_id`, `assignee_id`, `organization_id`, `tags[]`, `custom_fields[]{id, value}`, `via{}`, `satisfaction_rating{}`, `due_at`, `created_at`, `updated_at` | Volume, severity mix, tag-based theme detection. `type='problem'` with many linked `incident` tickets = systemic defect hitting many accounts |
| `ticket_metrics` | `reply_time_in_minutes`, `first_resolution_time_in_minutes`, `full_resolution_time_in_minutes`, `agent_wait_time_in_minutes`, `requester_wait_time_in_minutes`, `on_hold_time_in_minutes`, `replies`, `reopens`, `assignee_stations`, `group_stations`, `assigned_at`, `initially_assigned_at`, `solved_at`, `status_updated_at`, `latest_comment_added_at` | **`reopens` ≥ 2 and `group_stations` ≥ 3 are the strongest ticket-level dissatisfaction predictors** (`[ROT]` — practitioner heuristic, not a published benchmark). `requester_wait_time_in_minutes` is the customer's felt pain |
| `satisfaction_ratings` | `score` (stored: `offered`, `unoffered`, `good`, `bad`; filterable: also `received`, `received_with_comment`, `received_without_comment`, `good_with_comment`, `good_without_comment`, `bad_with_comment`, `bad_without_comment`), `comment`, `reason`, `reason_id`, `ticket_id`, `requester_id`, `assignee_id`, `group_id`, `created_at` | CSAT; `bad_with_comment` rows are the highest-value qualitative corpus in the whole stack |
| `organizations` | `id`, `name`, `domain_names[]`, `tags[]`, `organization_fields{}` | Account join key — see §10 |
| SLA | SLA policy metrics exposed on tickets and in Explore; breach state is derived from the policy's target vs. the metric | SLA breach count per account per quarter |

**Notes.** `reply_time_in_minutes` and friends carry both **calendar** and **business** hour variants — mixing them across accounts on different schedules produces nonsense. Incremental export (`/api/v2/incremental/tickets.json?start_time=`) is the only sane way to sync at volume; it can return the same record more than once (dedupe on `id` + `generated_timestamp`). `updated_at` changes only on ticket *events*, so a ticket edited via a side-conversation may not move it. Closed tickets become immutable after 28 days (archived) and drop out of some search endpoints.

### 5.2 Intercom `[V]`
| Object | Fields | CS signal |
|---|---|---|
| `conversation` | `state` (`open`,`closed`,`snoozed`), `open`, `read`, `priority`, `waiting_since`, `snoozed_until`, `tags[]`, `sla_applied`, `contacts`, `teammates`, `custom_attributes`, `source{type, delivery_method, author, body}` | Live support pressure; `waiting_since` is literally "how long has the customer been waiting on us" |
| `conversation.conversation_rating` | `rating`, `remark`, `created_at`, `updated_at`, `contact`, `teammate` | In-product CSAT (1–5 scale) |
| `conversation.statistics` | `time_to_assignment`, `time_to_admin_reply`, `time_to_first_close`, `time_to_last_close`, `median_time_to_reply`, `first_contact_reply_at`, `first_admin_reply_at`, `first_close_at`, `last_close_at`, `count_reopens`, `count_assignments`, `count_conversation_parts`, `handling_time`, `adjusted_handling_time` | Responsiveness and thrash |
| `contact` | `last_seen_at`, `signed_up_at`, `last_contacted_at`, `last_replied_at`, `last_email_opened_at`, `email`, `custom_attributes`, `companies` `[K for several]` | `last_seen_at` is a cheap, high-coverage per-user activity proxy when you have no product analytics |
| `company` | `company_id`, `name`, `monthly_spend`, `session_count`, `user_count`, `last_request_at`, `custom_attributes`, `plan` `[K]` | Account-level activity fallback |

**Gotchas.** Intercom `priority` semantics differ from ticket-system priority (it is closer to a boolean priority flag than a 5-level severity) — confirm the values in the target workspace before mapping `[flagged: not fully verified]`. `last_seen_at` only updates when the Messenger loads, so it measures *app-open*, not *feature use*; it overstates engagement for users who idle with a tab open and understates for API-only integrations. Search API (`POST /conversations/search`) is required for anything beyond a chronological list, and cursor pagination is capped — window by `updated_at`.

---

## 6. Product Analytics — Mixpanel / Amplitude / PostHog / Segment

### 6.1 The account-level problem
All three analytics tools are user-centric by default. B2B CS needs **account-level** aggregation, which requires the group/account feature to be configured *at instrumentation time*. If it wasn't, you must join events to accounts in the warehouse via `user_id → contact → account` (§10), and you inherit every identity bug.

| Tool | Account mechanism | Key fields | Limits |
|---|---|---|---|
| PostHog `[V]` | Group analytics; `posthog.group(groupType, groupKey, properties)`; events carry `$groups` / `$group_0..$group_4` | `$groups`, group properties, `$group_set` `[K for exact event property names]` | **Max 5 group types per project**; all identified events count toward billing once enabled `[V]` |
| Mixpanel `[V]` | Group Analytics: designate an event property as a group key (e.g. `company_id`) instead of `distinct_id`; group profiles with their own property set; a group key can be marked the "B2B Company Key" for company DAU/WAU/MAU and retention | group key event property; group profiles | Paid add-on on Growth/Enterprise `[V]` — **frequently not purchased, so the feature silently doesn't exist in the workspace** |
| Amplitude `[K — not re-verified]` | Accounts / Groups: `groups` object on events, `group_properties`, Group Identify API | `groups`, `group_properties`, `group_type`, `group_value` | Group-type count is capped (commonly cited as 5); account-level reporting is a paid capability |

### 6.2 Signals worth extracting (any tool)
| Signal | How to compute | Threshold guidance |
|---|---|---|
| Weekly active users per account (WAU) | Distinct `contact_id` with ≥1 `is_value_event` in trailing 7d | Report as a *ratio to licensed seats*, never absolute |
| **License utilization** | `seats_active_30d / seats_licensed` | `<40%` at renewal −90d is the most common downsell precursor `[ROT]` |
| Breadth | Distinct `event_name` in `event_category='core_value'` per account per 30d | Single-feature accounts churn disproportionately `[ROT]` |
| Depth trend | 28d value-events vs. prior 28d, as % change | `≤ −30%` sustained 2 consecutive periods = decay flag `[ROT]` |
| Admin/power-user concentration | Share of account events from top 1 user | `>70%` = key-person risk `[ROT]` |
| Time-to-first-value | Days from `account.created_at` to first `is_value_event` | Track distribution, set the threshold from your own cohort data — do not import someone else's number |
| Retention curve | Account-level N-day retention by signup cohort | Flattening point defines your "activated" definition |
| Feature-flag exposure | Flag payload per group/user | Confounds any usage change — must be controlled for |

### 6.3 Segment `[V for group traits]`
- `identify(userId, traits)` → person-level; `group(groupId, traits)` → **the join that ties a user to an account**; `track(event, properties)` → behavior; `page`/`screen`.
- Reserved group traits: `address`, `avatar`, `createdAt`, `description`, `email`, `employees`, `id`, `industry`, `name`, `phone`, `website`, `plan`.
- Group call payload fields: `type`, `userId`, `anonymousId`, `groupId`, `traits`, `context`, `integrations`, `timestamp`.
- **Gotcha:** the `group` call is optional and frequently never implemented. Without it, downstream destinations have no account dimension at all — check for its presence before promising account-level analysis. Also: `timestamp` vs `originalTimestamp` vs `receivedTimestamp` vs `sentAt` differ; warehouse tables usually expose all four, and choosing wrong shifts events across day boundaries.

---

## 7. Communications — Slack, Email, Meetings, Calls

### 7.1 Slack (shared channels) `[V for conversation fields]`
| Source | Fields | CS signal |
|---|---|---|
| `conversations.list` | `id`, `name`, `is_shared`, `is_ext_shared`, `is_org_shared`, `is_pending_ext_shared`, `is_private`, `is_archived`, `num_members`, `created`, `purpose{value, creator, last_set}`, `topic{}` | `is_ext_shared=true` identifies Slack Connect customer channels; `is_pending_ext_shared` = invite sent, not accepted (an onboarding stall) |
| `conversations.members` | member ids | **Member-count decline is a departure/disengagement signal.** Snapshot weekly; you cannot get history retroactively |
| `conversations.history` / `.replies` | `ts`, `user`, `text`, `thread_ts`, `reply_count`, `reactions`, `subtype` | Message volume trend; **response latency** = customer msg `ts` → next internal-user msg `ts`; thread depth |
| `users.info` | `is_bot`, `team_id`, `deleted`, `profile.email` | Exclude bots; `team_id ≠ our team_id` identifies the customer side; `deleted=true` on a customer member = departure |

**Gotchas.** `conversations.list` defaults to `limit=100`, max 1000, cursor-paginated. Free/Pro Slack plans truncate message history (90 days on Free), so "message volume declined" may be a retention-policy artifact. Bot and workflow messages inflate volume — filter `subtype` and `bot_id`. Channel membership snapshots must be stored yourself; there is no historical membership API.

### 7.2 Email — Gmail API `[V]` and Microsoft Graph `[V]`
| Field | Gmail | Microsoft Graph | CS signal |
|---|---|---|---|
| Thread key | `threadId` | `conversationId` (+ `conversationIndex` for position) | Groups a conversation |
| Timestamp | `internalDate` (epoch ms) | `receivedDateTime` / `sentDateTime` | Recency, latency |
| Participants | `payload.headers` (`From`,`To`,`Cc`,`Reply-To`) | `from`, `sender`, `toRecipients`, `ccRecipients`, `replyTo` | Multi-threading breadth; exec presence |
| Read state | `labelIds` contains `UNREAD` | `isRead` | Weak signal (our mailbox, not theirs) |
| Draft | `labelIds` contains `DRAFT` | `isDraft` | Exclude from latency math |
| Importance | — | `importance` (`low`/`normal`/`high`), `inferenceClassification` (`focused`/`other`) | |
| Headers | `payload.headers` | `internetMessageHeaders` (**requires `$select`**) | Bounce detection, `Auto-Submitted`, `X-Failed-Recipients` |
| Preview | `snippet` | `bodyPreview` (first 255 chars) | Cheap sentiment input without pulling full bodies |
| Sync | `historyId` + `users.history.list` | **delta query** on messages | Incremental sync |

**Derived signals.**
| Signal | Computation | Threshold |
|---|---|---|
| Reply latency | median(customer reply ts − our outbound ts) per account, trailing 90d | Doubling vs. the account's own 12-month baseline is the signal; absolute hours vary wildly by segment `[ROT]` |
| Reply rate decay | replies received / outbound sent, trailing 60d vs prior 60d | `<0.25` and falling = relationship cooling `[ROT]` |
| **Hard bounce = departure** | NDR/DSN message (`Auto-Submitted: auto-replied`, status codes `5.1.1` / `5.1.10`) referencing a known contact address | A hard bounce on the economic buyer or champion is a **P1 event** — the single cheapest high-precision churn signal in the stack |
| Out-of-office / delegation | `Auto-Submitted: auto-generated` + phrases naming a successor | Early departure warning before the bounce |
| Thread staleness | days since last message on any thread with the account | `>45d` on an account with a renewal inside 120d = coverage gap `[ROT]` |
| Multi-threading | distinct external addresses in threads, trailing 180d | `≤1` = single-threaded, the classic pre-churn state `[ROT]` |

**Gotchas.** Gmail `q` uses Gmail search operator syntax and matches on *indexed* content — it is not a substitute for structured filtering. `internalDate` is the message's internal creation time, which for imported mail is not the send time. Graph `internetMessageHeaders` is read-only and omitted unless `$select`-ed. Both APIs are per-mailbox: coverage equals the set of mailboxes you have consent for, so "no email activity" often means "we don't have that rep's mailbox," not "no contact." **Always report email coverage % (mailboxes connected / reps on the account).** Privacy: content access usually needs explicit legal sign-off; prefer metadata-only (headers, timestamps, participants) unless sentiment is specifically authorized.

### 7.3 Conversation intelligence — Gong / Chorus / Fireflies `[K — API details NOT re-verified this pass]`
| Signal | Typical field/concept | Use |
|---|---|---|
| Talk ratio | Gong interaction stats `talkRatio` (rep share of talk time) | Rep talk share `>65%` on a discovery/QBR call = we're presenting, not listening `[ROT]` |
| Longest monologue / longest customer story | `longestMonologue`, `longestCustomerStory` | Engagement quality |
| Interactivity / patience | `interactivity`, `patience` | Conversational health |
| Competitor mentions | Trackers / keyword trackers | Any competitor mention on a renewal-cycle call is a P1 flag |
| Next-step commitments | Transcript extraction; Gong "next steps" | Missing next step at end of a renewal call is a strong slip predictor `[ROT]` |
| Attendee list & seniority | Call participants + CRM contact roles | Exec disengagement: exec attended prior QBR, absent this one |
| Sentiment | Vendor sentiment or LLM-scored transcript | Use as a *trend* per account, never as an absolute |

**Endpoints (verify before use):** Gong `POST /v2/calls/extensive`, `GET /v2/calls/transcript`, `/v2/stats/interaction`, `/v2/stats/activity`; Fireflies GraphQL (`transcript`, `sentences`, `summary`, `ai_filters`); Chorus/ZoomIQ via Zoom Revenue Accelerator. Gong enforces per-second and daily API quotas and requires calls to be processed before transcripts exist (lag of minutes to hours). **Recording consent varies by jurisdiction — two-party-consent states and EU/GDPR contexts may make transcript analysis non-permissible; check before use.**

### 7.4 Scheduling — Calendly / Cal.com `[K — NOT re-verified]`
| Object | Fields | Signal |
|---|---|---|
| Calendly scheduled event | `uri`, `name`, `status` (`active`/`canceled`), `start_time`, `end_time`, `event_type`, `invitees_counter{total, active, limit}`, `cancellation{canceled_by, reason, canceler_type}` | Meeting cadence; **`canceler_type='invitee'` = customer-initiated cancellation, a materially stronger signal than our own reschedule** |
| Calendly invitee | `email`, `status`, `no_show` (object; present when marked), `rescheduled`, `cancel_url`, `questions_and_answers`, `tracking` | No-show tracking |
| Cal.com booking | `status` (`accepted`/`pending`/`cancelled`/`rejected`), `startTime`, `attendees[]`, `cancellationReason`, `rescheduled` | Same signals, OSS stack |

**Derived:** meetings per quarter vs. the account's segment norm; consecutive customer-initiated cancellations (`≥2` = escalate `[ROT]`); no-show rate trailing 180d; days since last completed meeting vs. days to renewal. **Gotcha:** `no_show` is only populated when a human marks it — coverage is usually poor, so a 0% no-show rate almost always means "nobody tracks this," not "everyone shows."

### 7.5 Zoom `[V for endpoints; rate limits NOT verified]`
`/past_meetings/{meetingUUID}/participants` → `name`, `user_email`, `join_time`, `leave_time`, `duration`; `/users/{userId}/meetings`; `/report/meetings/*`; `/meetings/{id}/recordings` (+ `recordings/analytics_summary`). Signal: actual attendance vs. invited (a meeting that happened with 1 of 4 invited customer stakeholders is a disengagement event), and dwell time (joined for 8 minutes of a 60-minute QBR). Report endpoints require paid plans and have bounded lookback windows; `meetingUUID` must be double-URL-encoded when it contains `/` or `//`.

---

## 8. Product Feedback & Engineering — Jira / Linear / Pendo / Appcues

### 8.1 Jira `[K — JQL specifics not re-verified]`
Account linkage is almost never native. The three real patterns: (1) JSM `organizations` field, (2) a custom field `cf[NNNNN]` holding the CRM account id, (3) labels/components as a proxy (lossy). Useful JQL: `project = SUP AND labels = "acct-acme" AND status != Done ORDER BY created DESC`; `issue in linkedIssues("SUP-123")`; `"Time to Resolution" = breached()` (JSM SLA). Fields: `issuetype`, `priority`, `status`, `statusCategory`, `resolution`, `resolutiondate`, `created`, `updated`, `duedate`, `votes`, `watchers`, `components`, `labels`, `reporter`. **Signal:** open P1/P2 bugs per account, age of oldest open bug, count of customer-linked feature requests, votes/watchers as demand weight. **Gotcha:** custom field IDs differ per Jira instance; resolve via `/rest/api/3/field` — never hard-code `cf[10023]`.

### 8.2 Linear `[V]`
Linear models **Customer** natively: `name`, `domain`, `logo`, `revenue`, `tier`, `size`, `status`, `owner`, plus `domains` and `externalIds` for matching. **Customer requests** link a customer's ask to an Issue or Project, carry the original message, source link, requester name, timestamp, and an importance flag. GraphQL exposes customers and requests (filterable by customer name, count, status, tier, revenue, size). Sync: **Intercom is real-time; Zendesk, Front, Salesforce, Slack, and Asks sync on a ~12-hour cycle** `[V]` — so Linear customer data can be up to half a day stale.

**Signal:** ARR-weighted feature demand (`SUM(customer.revenue)` over open requests per issue) is the correct input to a roadmap-influence conversation in a QBR; open request count per account measures unmet need.

### 8.3 Pendo / Appcues `[K — API endpoints NOT re-verified]`
Pendo sources typically available through the Aggregation API (`POST /api/v1/aggregation`, body with `requestId` + `pipeline` + a `source`): `events`, `pageEvents`, `featureEvents`, `trackEvents`, `guideEvents`, `pollEvents`, `npsEvents`, `visitors`, `accounts`. Fields commonly present: `visitorId`, `accountId`, `day`, `numEvents`, `numMinutes`, `guideId`, `guideStepId`, `type` (`guideSeen`/`guideAdvanced`/`guideDismissed`/`guideSnoozed`), `pollId`, `npsRating`. Appcues exposes flow/checklist events and NPS via its API and webhooks.

**Signal:** guide dismissal rate (high dismissal on an onboarding guide = friction), checklist completion % as a hard onboarding-progress metric, in-app NPS with verbatim, and `numMinutes` as a time-in-product proxy. **Gotchas:** Pendo `accountId` is whatever the snippet passes — frequently the *user's* email or a team id, not the CRM account; verify the metadata contract. Guide "seen" fires on render, not read. In-app NPS is heavily biased toward power users (they're the ones in the app), so it systematically over-reports for at-risk accounts where nobody logs in.

---

## 9. Warehouse Layer — Snowflake / BigQuery

### 9.1 Expected tables
| Table | Grain | Key columns |
|---|---|---|
| `accounts` | 1 row/account | `account_id`, `crm_account_id`, `billing_customer_id`, `name`, `primary_domain`, `segment`, `owner_csm_id`, `parent_account_id`, `is_test`, `created_at` |
| `contacts` | 1 row/person | `contact_id`, `account_id`, `email`, `email_domain`, `role`, `is_active`, `departed_at` |
| `subscriptions` | 1 row/subscription version (SCD2) | `subscription_id`, `account_id`, `status`, `term_start`, `term_end`, `mrr_usd`, `seats_licensed`, `auto_renew`, `cancel_scheduled`, `valid_from`, `valid_to`, `is_current` |
| `mrr_movements` | 1 row/account/month | `account_id`, `month`, `movement_type` (`new`,`expansion`,`contraction`,`churn`,`reactivation`), `mrr_delta_usd` |
| `events` | 1 row/event | `event_id`, `account_id`, `contact_id`, `event_name`, `event_ts`, `is_value_event`, `properties` |
| `usage_daily` | 1 row/account/day | `account_id`, `activity_date`, `active_users`, `value_events`, `distinct_features`, `sessions`, `minutes`, `_loaded_at` |
| `tickets`, `interactions`, `opportunities`, `invoices` | per §1 | |
| `health_scores` | 1 row/account/day | `account_id`, `score_date`, `score`, `component_scores` (json), `model_version` |

### 9.2 Modeling rules
- `usage_daily` must be **densified** (a row per account per day with zeros), not sparse. Sparse tables make `AVG()` lie by omitting the zero days — this is the most common silent error in CS analytics.
- Subscriptions as SCD2 with `valid_from`/`valid_to`/`is_current`; otherwise you cannot answer "what was their ARR six months ago."
- Store `_loaded_at` and `_source_extracted_at` on every table. Staleness checks (§11) are impossible without them.
- Warehouse-specific: BigQuery — partition `events` on `DATE(event_ts)` and cluster on `account_id`; unpartitioned scans of an events table are the classic cost incident. Snowflake — cluster large event tables on `(account_id, event_ts)`; use `QUALIFY ROW_NUMBER() OVER (…)` for dedupe (BigQuery also supports `QUALIFY`).
- Timezone: store UTC; do date bucketing in a stated reporting timezone via an explicit conversion (`CONVERT_TIMEZONE('UTC','America/New_York', ts)` in Snowflake; `DATE(ts, 'America/New_York')` in BigQuery). Mixing UTC-bucketed usage with local-bucketed billing shifts "last activity" by up to a day.

---

## 10. Identity Resolution

### 10.1 Resolution ladder (apply in order; stop at first confident match)
| Rank | Rule | Confidence | Notes |
|---|---|---|---|
| 1 | Explicit foreign key stored at write time (Stripe `metadata.account_id`, Paddle `custom_data.account_id`, Segment `groupId`, PostHog group key) | Highest | Always look for this first; it is the only rule that doesn't degrade |
| 2 | Deterministic id crosswalk table maintained by the business (`crm_account_id ↔ billing_customer_id ↔ product_org_id`) | High | Must be tested for 1:1-ness |
| 3 | Exact email match to a known `contact.email` | High | Normalize first (§10.3) |
| 4 | Corporate email **domain** match to `account.primary_domain` or `domain_aliases` | Medium | Fails on the cases in §10.2 |
| 5 | Normalized company-name fuzzy match (lowercase, strip `inc/llc/ltd/gmbh/sa/plc/co`, strip punctuation, then trigram/Jaro-Winkler ≥ 0.92) | Low | Human review required; never auto-merge |
| 6 | Shared Slack Connect `team_id` → account mapping | Medium | Good for Slack-native orgs |
| 7 | IP/ASN or enrichment reverse-lookup | Very low | Do not use for revenue-affecting decisions |

### 10.2 Domain-matching pitfalls (each one has burned a real CS team)
1. **Free/consumer domains** — `gmail.com`, `outlook.com`, `yahoo.com`, `qq.com`, `proton.me`, plus disposable domains. Matching on these merges thousands of unrelated accounts into one. Maintain a blocklist and **never** match rank-4 on a blocklisted domain.
2. **Subsidiaries & rebrands** — one legal account, many domains (`acme.com`, `acme.co.uk`, `acmelabs.io`). Requires `domain_aliases`.
3. **Shared parent, separate contracts** — the opposite failure: two independently-contracted business units on the same domain get merged, destroying per-contract renewal tracking. Resolve with `parent_account_id` hierarchy, not domain collapse.
4. **Agencies, MSPs, and resellers** — the paying entity's domain ≠ the using entity's domain. Model `payer_account_id` separately from `using_account_id`.
5. **Plus-addressing and dots** — `first.last+test@acme.com`. Gmail ignores dots and everything after `+`; most other providers do not. Store both raw and normalized.
6. **Contractor/personal addresses on real accounts** — a genuine champion using a personal address will be dropped by a strict blocklist. Rescue via rank-1/rank-3 matching.
7. **Mergers & acquisitions** — domain redirects to the acquirer, breaking historical matching. Keep aliases with `valid_from`/`valid_to`.
8. **Email case and Unicode** — lowercase the domain always; the local part is technically case-sensitive per RFC but treat as case-insensitive in practice and document the choice.
9. **Non-transitive merges** — chained fuzzy matches (A~B, B~C ⇒ A~C) create giant bogus clusters. Cap merge cluster size and require a deterministic anchor in every cluster.

### 10.3 Normalization functions to apply before any match
`lower(trim(email))`; split on last `@`; domain → lowercase, strip trailing `.`, strip leading `www.`; strip `+suffix` from local part (record that you did); company name → lowercase, NFKD-normalize, strip legal suffixes and punctuation, collapse whitespace. **Store the raw value alongside the normalized one, always.**

### 10.4 Resolution quality metrics to report
`match_rate` (events with a resolved `account_id` / all events), `unmatched_revenue_usd`, `ambiguous_matches` (email matching >1 account), `orphan_contacts`, `cluster_size_p99`. If `match_rate < 0.90`, account-level usage analysis is not trustworthy — say so in the output.

---

## 11. Data Quality Gate — Run Before Any Analysis

Fail loudly. Each check returns PASS / WARN / FAIL plus the measured value. Thresholds below are `[ROT]` operating defaults for a $100M+ ARR B2B SaaS stack — tune to the environment, but never skip the check.

| # | Check | Measure | WARN | FAIL | Why it matters |
|---|---|---|---|---|---|
| 1 | **Usage freshness** | `now() − max(usage_daily.activity_date)` | >2 days | >5 days | A stalled pipeline looks exactly like a churning customer |
| 2 | **Per-source freshness** | `now() − max(_source_extracted_at)` per system | >24h | >72h | One dead connector poisons one component of the score |
| 3 | **Usage coverage** | accounts with ≥1 usage row in last 30d / active subscriptions | <90% | <75% | Missing instrumentation reads as zero usage |
| 4 | **Identity match rate** | §10.4 | <95% | <90% | |
| 5 | **CRM–billing reconciliation** | \|ARR_crm − ARR_billing\| / ARR_billing | >2% | >5% | Determines which system you can quote |
| 6 | **Duplicate accounts** | accounts sharing normalized name or primary domain | >1% | >3% | Splits one customer's signal in half |
| 7 | **Test/internal accounts excluded** | Rows matching: own domain; name contains `test`,`demo`,`sandbox`,`qa`,`staging`,`[internal]`; Stripe `livemode=false`; Salesforce sandbox org id; `is_test=true` | any unexcluded | any in top-50 by ARR | Internal accounts are hyper-active and skew every model |
| 8 | **Null rate on critical fields** | `renewal_date`, `arr_usd`, `owner_csm_id`, `seats_licensed`, `segment` | >2% | >10% | Nulls silently drop rows from `WHERE` clauses |
| 9 | **Partial-period contamination** | Current month/week included in a trend | any | any in a "% change" figure | A month-to-date bar next to full months always shows a fake decline. Either exclude the partial period or annotate it |
| 10 | **Timezone consistency** | All timestamps UTC at rest; one declared reporting tz | mixed | mixed on joined tables | |
| 11 | **Currency normalization** | All amounts converted at a stated FX date; zero-decimal currencies handled | unstated FX | mixed currencies summed | |
| 12 | **Seat data sanity** | `seats_active_30d ≤ seats_licensed` | violations >1% | >5% | Violations mean the seat join is wrong |
| 13 | **Event-volume anomaly** | Daily total events vs. trailing-28d median | ±30% | ±50% | Catches tracking regressions and double-fires |
| 14 | **Late-arriving data** | Rows with `event_ts < _loaded_at − 48h` | >1% | >5% | Mobile/offline SDKs backfill; recompute windows must account for it |
| 15 | **Deleted/merged records** | Salesforce `IsDeleted`, HubSpot merged ids, Zendesk archived tickets | present | present in join keys | |
| 16 | **Survey response bias** | NPS/CSAT respondents / eligible accounts | <20% | <10% | Below ~10% you have anecdotes, not a metric |
| 17 | **Score staleness** | `now() − max(health_scores.score_date)` | >1 day | >7 days | |
| 18 | **Schema drift** | Expected column set present per source | missing optional | missing required | Salesforce FLS and HubSpot `properties=` both drop columns silently, without erroring |

**Output contract.** Every analysis must carry a header block: `as_of` timestamp, reporting timezone, currency + FX date, account coverage %, identity match rate, list of FAILed checks, and the systems actually used. Suppress any metric whose inputs failed a check, and say which metric was suppressed and why.

---

## 12. Example SQL — Six Core CS Queries

ANSI-ish SQL; noted where Snowflake vs. BigQuery syntax differs.

### 12.1 Renewal risk board — 120-day horizon, all signals joined
```sql
WITH horizon AS (
  SELECT s.account_id, s.subscription_id, s.term_end AS renewal_date,
         s.arr_usd, s.seats_licensed, s.auto_renew, s.cancel_scheduled,
         DATEDIFF('day', CURRENT_DATE, s.term_end) AS days_to_renewal
  FROM subscriptions s
  WHERE s.is_current AND s.status IN ('active','past_due','trialing')
    AND s.term_end BETWEEN CURRENT_DATE AND DATEADD('day', 120, CURRENT_DATE)
),
usage AS (
  SELECT account_id,
         SUM(CASE WHEN activity_date >= DATEADD('day',-30,CURRENT_DATE) THEN value_events END)  AS ve_30d,
         SUM(CASE WHEN activity_date BETWEEN DATEADD('day',-60,CURRENT_DATE)
                                         AND DATEADD('day',-31,CURRENT_DATE) THEN value_events END) AS ve_prior_30d,
         MAX(CASE WHEN activity_date >= DATEADD('day',-30,CURRENT_DATE) THEN active_users END)  AS peak_active_users_30d,
         MAX(activity_date) AS last_active_date
  FROM usage_daily
  WHERE activity_date >= DATEADD('day',-60,CURRENT_DATE)
  GROUP BY account_id
),
support AS (
  SELECT account_id,
         COUNT(*)                                              AS tickets_90d,
         COUNT_IF(is_escalated)                                AS escalations_90d,
         COUNT_IF(sla_breached)                                AS sla_breaches_90d,
         AVG(CASE WHEN csat_score IS NOT NULL THEN csat_score END) AS avg_csat_90d
  FROM tickets
  WHERE created_at >= DATEADD('day',-90,CURRENT_DATE)
  GROUP BY account_id
),
touch AS (
  SELECT account_id,
         MAX(occurred_at)                                              AS last_touch_at,
         MAX(CASE WHEN exec_present THEN occurred_at END)              AS last_exec_touch_at,
         COUNT(DISTINCT CASE WHEN occurred_at >= DATEADD('day',-180,CURRENT_DATE)
                             THEN external_participant_ids END)        AS threads_180d
  FROM interactions
  GROUP BY account_id
)
SELECT a.name, h.renewal_date, h.days_to_renewal, h.arr_usd,
       ROUND(u.peak_active_users_30d / NULLIF(h.seats_licensed,0), 2)          AS seat_utilization,
       ROUND((u.ve_30d - u.ve_prior_30d) / NULLIF(u.ve_prior_30d,0), 2)        AS usage_trend_pct,
       DATEDIFF('day', u.last_active_date, CURRENT_DATE)                       AS days_since_active,
       DATEDIFF('day', t.last_touch_at, CURRENT_DATE)                          AS days_since_touch,
       DATEDIFF('day', t.last_exec_touch_at, CURRENT_DATE)                     AS days_since_exec_touch,
       s.tickets_90d, s.escalations_90d, s.sla_breaches_90d, s.avg_csat_90d,
       h.auto_renew, h.cancel_scheduled,
       (CASE WHEN h.cancel_scheduled THEN 40 ELSE 0 END
      + CASE WHEN u.peak_active_users_30d / NULLIF(h.seats_licensed,0) < 0.40 THEN 20 ELSE 0 END
      + CASE WHEN (u.ve_30d - u.ve_prior_30d) / NULLIF(u.ve_prior_30d,0) < -0.30 THEN 15 ELSE 0 END
      + CASE WHEN DATEDIFF('day', t.last_touch_at, CURRENT_DATE) > 45 THEN 10 ELSE 0 END
      + CASE WHEN s.escalations_90d > 0 THEN 10 ELSE 0 END
      + CASE WHEN s.avg_csat_90d < 0.70 THEN 5 ELSE 0 END)                     AS risk_points
FROM horizon h
JOIN accounts a ON a.account_id = h.account_id AND NOT a.is_test
LEFT JOIN usage u   ON u.account_id = h.account_id
LEFT JOIN support s ON s.account_id = h.account_id
LEFT JOIN touch t   ON t.account_id = h.account_id
ORDER BY risk_points DESC, h.arr_usd DESC;
```
*Weights above are an illustrative `[ROT]` starting point, not a fitted model. Calibrate against your own churned-cohort base rates before presenting scores as probabilities.*

### 12.2 Net revenue retention and gross revenue retention (cohort-correct)
```sql
WITH base AS (
  SELECT account_id, SUM(mrr_usd) AS mrr_start
  FROM subscriptions
  WHERE valid_from <= DATEADD('month',-12,DATE_TRUNC('month',CURRENT_DATE))
    AND (valid_to IS NULL OR valid_to > DATEADD('month',-12,DATE_TRUNC('month',CURRENT_DATE)))
    AND status IN ('active','past_due')
  GROUP BY account_id
),
now_ AS (
  SELECT account_id, SUM(mrr_usd) AS mrr_now
  FROM subscriptions
  WHERE is_current AND status IN ('active','past_due')
  GROUP BY account_id
)
SELECT
  SUM(b.mrr_start)                                            AS starting_mrr,
  SUM(COALESCE(n.mrr_now,0))                                  AS ending_mrr_same_cohort,
  ROUND(SUM(COALESCE(n.mrr_now,0)) / NULLIF(SUM(b.mrr_start),0), 4)                    AS nrr,
  ROUND(SUM(LEAST(COALESCE(n.mrr_now,0), b.mrr_start)) / NULLIF(SUM(b.mrr_start),0),4) AS grr,
  SUM(GREATEST(COALESCE(n.mrr_now,0) - b.mrr_start, 0))       AS expansion_mrr,
  SUM(GREATEST(b.mrr_start - COALESCE(n.mrr_now,0), 0))       AS contraction_and_churn_mrr,
  COUNT(*)                                                    AS cohort_accounts,
  COUNT_IF(COALESCE(n.mrr_now,0) = 0)                         AS logos_churned
FROM base b LEFT JOIN now_ n USING (account_id);
```
Key correctness points: NRR is computed on a **fixed cohort** present 12 months ago (no new logos in the numerator); GRR caps each account at its starting MRR so expansion cannot mask churn.

### 12.3 Usage decay detection with statistical guardrails
```sql
WITH weekly AS (
  SELECT account_id, DATE_TRUNC('week', activity_date) AS wk,
         SUM(value_events) AS ve, MAX(active_users) AS au
  FROM usage_daily
  WHERE activity_date >= DATEADD('week',-13,CURRENT_DATE)
    AND activity_date <  DATE_TRUNC('week', CURRENT_DATE)   -- exclude partial week (QC #9)
  GROUP BY 1,2
),
stats AS (
  SELECT account_id,
         AVG(CASE WHEN wk >= DATEADD('week',-4, DATE_TRUNC('week',CURRENT_DATE)) THEN ve END)  AS ve_recent_4w,
         AVG(CASE WHEN wk <  DATEADD('week',-4, DATE_TRUNC('week',CURRENT_DATE)) THEN ve END)  AS ve_baseline_9w,
         STDDEV(CASE WHEN wk < DATEADD('week',-4, DATE_TRUNC('week',CURRENT_DATE)) THEN ve END) AS ve_sd_baseline,
         COUNT(DISTINCT wk) AS weeks_observed
  FROM weekly GROUP BY 1
)
SELECT s.account_id, a.name, sub.arr_usd,
       ROUND(s.ve_recent_4w,1) AS recent, ROUND(s.ve_baseline_9w,1) AS baseline,
       ROUND((s.ve_recent_4w - s.ve_baseline_9w)/NULLIF(s.ve_baseline_9w,0),3) AS pct_change,
       ROUND((s.ve_recent_4w - s.ve_baseline_9w)/NULLIF(s.ve_sd_baseline,0),2) AS z_score
FROM stats s
JOIN accounts a  ON a.account_id = s.account_id AND NOT a.is_test
JOIN subscriptions sub ON sub.account_id = s.account_id AND sub.is_current
WHERE s.weeks_observed >= 10                    -- enough history to trend
  AND s.ve_baseline_9w >= 20                    -- suppress low-volume noise
  AND (s.ve_recent_4w - s.ve_baseline_9w)/NULLIF(s.ve_baseline_9w,0) <= -0.30
  AND (s.ve_recent_4w - s.ve_baseline_9w)/NULLIF(s.ve_sd_baseline,0) <= -1.5
ORDER BY sub.arr_usd DESC;
```
The `weeks_observed` and `ve_baseline_9w` floors and the z-score gate are what separate a real decay alert from a noisy small-account false positive.

### 12.4 Champion departure / single-threading risk
```sql
WITH contact_state AS (
  SELECT c.account_id, c.contact_id, c.email, c.role,
         c.email_bounce_status, c.last_product_seen_at, c.last_inbound_reply_at,
         GREATEST(COALESCE(c.last_product_seen_at,'1970-01-01'),
                  COALESCE(c.last_inbound_reply_at,'1970-01-01')) AS last_signal_at
  FROM contacts c
)
SELECT a.name, s.arr_usd, s.term_end AS renewal_date,
       COUNT(*)                                                                  AS known_contacts,
       COUNT_IF(cs.last_signal_at >= DATEADD('day',-90,CURRENT_DATE))            AS active_contacts_90d,
       COUNT_IF(cs.role IN ('champion','economic_buyer','exec_sponsor'))         AS key_contacts,
       COUNT_IF(cs.role IN ('champion','economic_buyer','exec_sponsor')
                AND cs.last_signal_at < DATEADD('day',-60,CURRENT_DATE))         AS dormant_key_contacts,
       COUNT_IF(cs.email_bounce_status = 'hard')                                 AS hard_bounces,
       COUNT_IF(cs.email_bounce_status = 'hard'
                AND cs.role IN ('champion','economic_buyer'))                    AS key_contact_departures
FROM contact_state cs
JOIN accounts a      ON a.account_id = cs.account_id AND NOT a.is_test
JOIN subscriptions s ON s.account_id = cs.account_id AND s.is_current AND s.status='active'
GROUP BY a.name, s.arr_usd, s.term_end
HAVING COUNT_IF(cs.last_signal_at >= DATEADD('day',-90,CURRENT_DATE)) <= 1   -- single-threaded
    OR COUNT_IF(cs.email_bounce_status='hard' AND cs.role IN ('champion','economic_buyer')) > 0
ORDER BY s.arr_usd DESC;
```

### 12.5 Onboarding / time-to-first-value cohort
```sql
SELECT DATE_TRUNC('month', a.created_at)                                     AS cohort_month,
       COUNT(*)                                                              AS accounts,
       COUNT_IF(a.first_value_date IS NOT NULL)                              AS activated,
       ROUND(COUNT_IF(a.first_value_date IS NOT NULL)/NULLIF(COUNT(*),0),3)  AS activation_rate,
       MEDIAN(DATEDIFF('day', a.created_at, a.first_value_date))             AS median_ttfv_days,
       PERCENTILE_CONT(0.90) WITHIN GROUP (
         ORDER BY DATEDIFF('day', a.created_at, a.first_value_date))         AS p90_ttfv_days,
       COUNT_IF(a.first_value_date IS NULL
                AND a.created_at < DATEADD('day',-60,CURRENT_DATE))          AS stalled_over_60d
FROM accounts a
WHERE NOT a.is_test
  AND a.created_at >= DATEADD('month',-12, DATE_TRUNC('month',CURRENT_DATE))
  AND a.created_at <  DATE_TRUNC('month', CURRENT_DATE)     -- exclude partial month (QC #9)
GROUP BY 1 ORDER BY 1;
```

### 12.6 Data-quality gate (run first; emit as a header block)
```sql
SELECT 'usage_freshness_days' AS check_name,
       DATEDIFF('day', MAX(activity_date), CURRENT_DATE)::STRING AS value,
       CASE WHEN DATEDIFF('day', MAX(activity_date), CURRENT_DATE) > 5 THEN 'FAIL'
            WHEN DATEDIFF('day', MAX(activity_date), CURRENT_DATE) > 2 THEN 'WARN'
            ELSE 'PASS' END AS status
FROM usage_daily
UNION ALL
SELECT 'usage_coverage_pct',
       ROUND(100.0 * COUNT_IF(u.account_id IS NOT NULL)/NULLIF(COUNT(*),0),1)::STRING,
       CASE WHEN 100.0*COUNT_IF(u.account_id IS NOT NULL)/NULLIF(COUNT(*),0) < 75 THEN 'FAIL'
            WHEN 100.0*COUNT_IF(u.account_id IS NOT NULL)/NULLIF(COUNT(*),0) < 90 THEN 'WARN'
            ELSE 'PASS' END
FROM subscriptions s
LEFT JOIN (SELECT DISTINCT account_id FROM usage_daily
           WHERE activity_date >= DATEADD('day',-30,CURRENT_DATE)) u USING (account_id)
WHERE s.is_current AND s.status IN ('active','past_due')
UNION ALL
SELECT 'duplicate_account_groups', COUNT(*)::STRING,
       CASE WHEN COUNT(*) > 0 THEN 'WARN' ELSE 'PASS' END
FROM (SELECT LOWER(primary_domain) d FROM accounts WHERE NOT is_test AND primary_domain IS NOT NULL
      GROUP BY 1 HAVING COUNT(*) > 1)
UNION ALL
SELECT 'null_renewal_date_pct',
       ROUND(100.0*COUNT_IF(term_end IS NULL)/NULLIF(COUNT(*),0),1)::STRING,
       CASE WHEN 100.0*COUNT_IF(term_end IS NULL)/NULLIF(COUNT(*),0) > 10 THEN 'FAIL'
            WHEN 100.0*COUNT_IF(term_end IS NULL)/NULLIF(COUNT(*),0) > 2  THEN 'WARN'
            ELSE 'PASS' END
FROM subscriptions WHERE is_current AND status='active'
UNION ALL
SELECT 'seat_sanity_violations_pct',
       ROUND(100.0*COUNT_IF(seats_active_30d > seats_licensed)/NULLIF(COUNT(*),0),1)::STRING,
       CASE WHEN 100.0*COUNT_IF(seats_active_30d > seats_licensed)/NULLIF(COUNT(*),0) > 5 THEN 'FAIL'
            WHEN 100.0*COUNT_IF(seats_active_30d > seats_licensed)/NULLIF(COUNT(*),0) > 1 THEN 'WARN'
            ELSE 'PASS' END
FROM subscriptions WHERE is_current;
```
*(Snowflake syntax: `COUNT_IF`, `DATEADD`, `DATEDIFF`, `::STRING`. BigQuery: use `COUNTIF`, `DATE_ADD/DATE_DIFF`, `CAST(x AS STRING)`, and `PERCENTILE_CONT(...) OVER ()`.)*

---

## 13. Signal → Source Priority Matrix

When multiple systems can answer the same question, use the highest-precedence available source and record which one you used.

| CS signal | 1st choice | 2nd | 3rd | Never use |
|---|---|---|---|---|
| Current ARR / MRR | Billing (Stripe/Paddle) | ChartMogul | CRM Contract | CRM Opportunity `Amount` |
| Renewal date | CRM `Contract.EndDate` (minus `OwnerExpirationNotice`) | Billing `term_end` | Opportunity `CloseDate` | Spreadsheet |
| Explicit churn intent | Stripe `cancel_at_period_end` / Paddle `scheduled_change.action='cancel'` | Opportunity stage `Closed Lost` | Verbal in call | Health score |
| Licensed seats | Billing `items[].quantity` | CPQ subscription object | CRM custom field | Sales rep memory |
| Active users | Product analytics group-level DAU/WAU | Warehouse `usage_daily` | Intercom `last_seen_at` | Login count alone |
| Feature adoption breadth | Product analytics events | Pendo feature events | — | Page views |
| Support pain | Zendesk `ticket_metrics` + `satisfaction_ratings` | Intercom `statistics` | CRM `Case` | Ticket count alone |
| Product defect exposure | Jira/Linear customer-linked issues | Zendesk `type='problem'` clusters | — | |
| Relationship health | `interaction` table (email + meetings + Slack) | CRM `LastActivityDate` | CSM opinion | |
| Champion departure | Email hard bounce | Slack member removal | CRM contact `Inactive` flag | |
| Sentiment | Call transcript + ticket verbatims + survey verbatims (triangulated) | Single-source sentiment score | — | Emoji reactions |
| Executive engagement | Meeting attendee lists (Zoom/Calendly/Gong) | Email participants | — | |

---

## 14. Source Register

| # | Source | Fetched | What it verified |
|---|---|---|---|
| 1 | docs.stripe.com/api/subscriptions/object | Aug 2026 | Subscription fields, status enums, item-level period fields, `cancellation_details`, `pause_collection` semantics |
| 2 | docs.stripe.com/api/invoices/object | Aug 2026 | Invoice fields, `status`/`billing_reason` enums, `attempt_count`, `next_payment_attempt`, `parent` restructure |
| 3 | developer.zendesk.com/api-reference/ticketing/tickets/tickets | Aug 2026 | Ticket status/priority/type enums, `satisfaction_rating`, `custom_status_id` |
| 4 | developer.zendesk.com/.../ticket_metrics | Aug 2026 | All `*_in_minutes` metrics, `replies`, `reopens`, `assignee_stations`, `group_stations` |
| 5 | developer.zendesk.com/.../satisfaction_ratings | Aug 2026 | `score` stored vs. filterable values |
| 6 | developers.intercom.com — Conversation model | Aug 2026 | `state`, `waiting_since`, `statistics.*`, `conversation_rating.*`, `sla_applied` |
| 7 | dev.chartmogul.com/reference/retrieve-all-key-metrics | Aug 2026 | `/v1/metrics/all` params and response fields |
| 8 | dev.chartmogul.com/reference/retrieve-mrr | Aug 2026 | `/v1/metrics/mrr` movement fields; cents |
| 9 | developer.paddle.com/api-reference/subscriptions/overview | Aug 2026 | Subscription fields, status enums, `scheduled_change` |
| 10 | knowledge.hubspot.com — default deal properties | Aug 2026 | `dealstage`, `dealtype`, `hs_arr/mrr/acv/tcv` (Pro/Ent gating) |
| 11 | knowledge.hubspot.com — default ticket properties | Aug 2026 | Ticket internal property names, SLA status labels |
| 12 | developer.salesforce.com Object Reference v254 — Opportunity | Aug 2026 | Opportunity standard fields incl. `PushCount`, `LastStageChangeDate`, `HasOverdueTask` |
| 13 | developer.salesforce.com Object Reference v254 — Contract | Aug 2026 | Contract fields incl. `OwnerExpirationNotice` |
| 14 | developer.salesforce.com Object Reference v254 — Case | Aug 2026 | Case fields incl. `MilestoneStatus`, `SlaStartDate`, `EntitlementId` |
| 15 | posthog.com/docs/product-analytics/group-analytics | Aug 2026 | 5-group-type limit; billing implication |
| 16 | docs.mixpanel.com — Group Analytics | Aug 2026 | Group key model, group profiles, B2B Company Key, paid add-on |
| 17 | github.com/segmentio/segment-docs — spec/group.md | Aug 2026 | Full reserved group-trait table |
| 18 | docs.slack.dev/reference/methods/conversations.list | Aug 2026 | `is_ext_shared` family, `num_members`, pagination limits |
| 19 | learn.microsoft.com/graph/api/resources/message | Aug 2026 | Full message property table, `internetMessageHeaders` `$select` requirement, delta query |
| 20 | developers.google.com/workspace/gmail/api — users.messages | Aug 2026 | `threadId`, `labelIds`, `internalDate`, `historyId`, list params |
| 21 | linear.app/docs/customer-requests | Aug 2026 | Customer object attributes; **Intercom real-time vs. 12-hour sync for Zendesk/Front/Salesforce/Slack/Asks** |
| 22 | developers.zoom.us/docs/api/meetings | Aug 2026 | Participant and recording endpoints/fields |
| 23 | saas-capital.com/research | Aug 2026 | `[BM]` SaaS Capital 2026 growth benchmarks: median private B2B SaaS growth **22%** (down from **25%** in 2024); **7.3%** of companies flat or negative in 2025 |

**Sources:** [Stripe Subscription](https://docs.stripe.com/api/subscriptions/object) · [Stripe Invoice](https://docs.stripe.com/api/invoices/object) · [Zendesk Tickets](https://developer.zendesk.com/api-reference/ticketing/tickets/tickets/) · [Zendesk Ticket Metrics](https://developer.zendesk.com/api-reference/ticketing/tickets/ticket_metrics/) · [Zendesk Satisfaction Ratings](https://developer.zendesk.com/api-reference/ticketing/ticket-management/satisfaction_ratings/) · [Intercom Conversation](https://developers.intercom.com/docs/references/rest-api/api.intercom.io/conversations/conversation) · [ChartMogul All Metrics](https://dev.chartmogul.com/reference/retrieve-all-key-metrics) · [ChartMogul MRR](https://dev.chartmogul.com/reference/retrieve-mrr) · [Paddle Subscriptions](https://developer.paddle.com/api-reference/subscriptions/overview) · [HubSpot Deal Properties](https://knowledge.hubspot.com/properties/hubspots-default-deal-properties) · [HubSpot Ticket Properties](https://knowledge.hubspot.com/tickets/hubspots-default-ticket-properties) · [Salesforce Opportunity](https://developer.salesforce.com/docs/atlas.en-us.254.0.object_reference.meta/object_reference/sforce_api_objects_opportunity.htm) · [Salesforce Contract](https://developer.salesforce.com/docs/atlas.en-us.object_reference.meta/object_reference/sforce_api_objects_contract.htm) · [Salesforce Case](https://developer.salesforce.com/docs/atlas.en-us.254.0.object_reference.meta/object_reference/sforce_api_objects_case.htm) · [PostHog Group Analytics](https://posthog.com/docs/product-analytics/group-analytics) · [Mixpanel Group Analytics](https://docs.mixpanel.com/docs/data-structure/advanced/group-analytics) · [Segment Group Spec](https://raw.githubusercontent.com/segmentio/segment-docs/develop/src/connections/spec/group.md) · [Slack conversations.list](https://docs.slack.dev/reference/methods/conversations.list) · [Microsoft Graph message](https://learn.microsoft.com/en-us/graph/api/resources/message) · [Gmail users.messages](https://developers.google.com/workspace/gmail/api/reference/rest/v1/users.messages) · [Linear Customer Requests](https://linear.app/docs/customer-requests) · [Zoom Meetings API](https://developers.zoom.us/docs/api/meetings/) · [SaaS Capital Research](https://www.saas-capital.com/research/)
