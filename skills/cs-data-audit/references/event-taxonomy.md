# Event Taxonomy Audit — is the thing that predicts retention actually being measured?

> A company can spend $80k a year on product analytics and still be unable to answer "did this
> customer do the thing that makes them stay?" This file is the procedure for finding out,
> and for pricing the fix.

**Contents**
1. [The core action — define it before auditing anything](#1-the-core-action--define-it-before-auditing-anything)
2. [Instrumentation coverage across surfaces](#2-instrumentation-coverage-across-surfaces)
3. [Naming and the tracking plan](#3-naming-and-the-tracking-plan)
4. [Untyped, unplanned and anonymous volume](#4-untyped-unplanned-and-anonymous-volume)
5. [Property completeness on the events that matter](#5-property-completeness-on-the-events-that-matter)
6. [Taxonomy versioning and the fleet-decay test](#6-taxonomy-versioning-and-the-fleet-decay-test)
7. [The minimum event contract for CS](#7-the-minimum-event-contract-for-cs)
8. [Scoring the domain](#8-scoring-the-domain)
9. [Fix menu, ranked](#9-fix-menu-ranked)

---

## 1. The core action — define it before auditing anything

`cs-context` §5 asks for the **activation event**: the single action that, once a customer does
it, predicts they stay. If that field says `UNKNOWN`, the taxonomy audit has a different job —
it is now a definition exercise, and the audit reports that as its top finding.

### The validation test

A core action is only a core action if it separates retained from churned cohorts. Test it:

```sql
-- Do retained accounts perform the candidate core action more than churned ones did,
-- measured at the same point in their lifecycle (T-180 relative to renewal/churn decision)?
WITH pit AS (
  SELECT a.account_id,
         CASE WHEN c.account_id IS NOT NULL THEN 'churned' ELSE 'retained' END AS outcome,
         COALESCE(c.decision_date, s.renewal_date) - 180                       AS snapshot_date
  FROM account a
  JOIN subscription s USING (account_id)
  LEFT JOIN churn_event c USING (account_id)
  WHERE COALESCE(c.decision_date, s.renewal_date) BETWEEN CURRENT_DATE - 730 AND CURRENT_DATE
)
SELECT p.outcome,
       COUNT(*)                                        AS accounts,
       ROUND(AVG(u.core_actions_28d), 1)               AS mean_core_actions_28d,
       ROUND(PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY u.core_actions_28d), 1) AS median
FROM pit p
JOIN LATERAL (
  SELECT SUM(core_actions) AS core_actions_28d
  FROM usage_daily d
  WHERE d.account_id = p.account_id
    AND d.date BETWEEN p.snapshot_date - 28 AND p.snapshot_date
) u ON TRUE
GROUP BY p.outcome;
```

| Result | Verdict |
| --- | --- |
| Retained median ≥2× churned median at T−180 | The candidate is a real core action. Instrument it properly and score on it |
| Medians within ~20% of each other | It is an activity, not a value event. Keep looking |
| Cannot run the query — no `churn_event.decision_date` | **The taxonomy audit is blocked by the label audit.** Say so; fix labels first |

**The rookie core action is `login` or `page_view`.** Presence is not value. If the "core
action" is a login, every depth signal in the library measures whether the customer opened the
tab, which is why usage-based risk scores built on logins routinely fail to discriminate.

**Breadth must be measured against a curated core-feature set, not the full catalog.** Pendo's
*2019 Feature Adoption Report* (615 Pendo subscriptions with more than one year of tenure) found
roughly 80% of features are rarely or never used, and about 12% of features drive roughly 80% of
daily usage volume `[M]`. Measuring "features used ÷ features shipped" therefore produces a
number that is low for everyone and discriminates nothing.

---

## 2. Instrumentation coverage across surfaces

The core action must fire from **every** path a customer can take to perform it. A gap here
produces silent, structural under-measurement on whichever customer segment prefers that path.

| Surface | How the gap appears | Detection |
| --- | --- | --- |
| Web app | Usually instrumented | Baseline |
| Mobile app | Mobile-heavy accounts look dormant | Compare event mix per account against known mobile adoption |
| Public API | API-first customers show near-zero usage — often your most technical, highest-value accounts | Join API-gateway logs to `account_id`; count accounts with API traffic and no product events |
| Embedded / white-label | Whole OEM segment invisible | Check whether embedded sessions emit at all |
| SSO-initiated sessions | Session-start events bypassed; login counts collapse | Compare IdP assertions to `session_start` counts |
| Batch / scheduled jobs | Automation-heavy accounts look inactive despite high value delivered | Count `workflow_run`-class events separately from human sessions |
| Server-side vs client-side | Ad-blockers and privacy browsers suppress client events for some populations | Compare server-side counts to client-side counts for the same action |

```sql
-- Accounts with API traffic but no product events: the classic invisible-power-user cohort
SELECT a.name, a.arr, g.api_calls_30d
FROM account a
JOIN (SELECT account_id, SUM(api_calls) AS api_calls_30d FROM usage_daily
      WHERE date >= CURRENT_DATE - 30 GROUP BY 1) g USING (account_id)
LEFT JOIN (SELECT DISTINCT account_id FROM usage_event
           WHERE timestamp >= CURRENT_DATE - 30) e USING (account_id)
WHERE g.api_calls_30d > 0 AND e.account_id IS NULL AND a.is_internal = FALSE
ORDER BY a.arr DESC;
```

Every account on that list is a false-red waiting to happen. Report the count and the ARR.

---

## 3. Naming and the tracking plan

### The convention

Segment's published guidance is the **object-action framework**: choose the objects (Product,
Application, Report), then the actions performed on them (Viewed, Installed, Published), and
name events `Object Action` — e.g. `Product Viewed`, `Application Installed`. Its casing
recommendation is Proper Case for events and `snake_case` for properties `[V — Segment/Twilio,
"Naming conventions for clean data"]`.

The specific convention matters less than **having one and conforming to it**. Measure:

```
naming_conformance = distinct event names matching the convention ÷ distinct event names
```

| Conformance | Reading |
| --- | --- |
| ≥90% | Healthy. Fix the stragglers with a rename map |
| 60–90% | Two or three teams instrumented independently. Reconcile before building anything on top |
| <60% | There is no taxonomy, only accumulated events. A rewrite is cheaper than a reconciliation |

**The anti-pattern with the worst blast radius** is embedding variables in event names —
`Sign Up - jake@acme.com`, `Report Published - Q3` — which Segment's guidance calls out
explicitly. It produces unbounded distinct event names, breaks every aggregation, and is
usually the cause of a >60% conformance failure. Variables belong in properties.

### The tracking plan

A tracking plan is a versioned document (or a schema registry) listing, per event: name,
description, when it fires, required properties, property types, and allowed values.

| Check | Pass | Why |
| --- | --- | --- |
| It exists | Yes/No | Without it, "unplanned volume" is undefined and nothing below is measurable |
| It has a named owner | Yes | Unowned plans decay within two releases |
| It is versioned with a change log | Yes | Renames must be datable, or §6 is impossible |
| It is enforced at ingest, not just documented | Warn or block on violations | A document nobody validates against is a wish |
| Required properties include `account_id` on every event | Yes | Everything in CS is account-grained |

---

## 4. Untyped, unplanned and anonymous volume

Three different problems that get conflated. Measure them separately.

| Measure | Definition | Pass | What its failure costs |
| --- | --- | --- | --- |
| **Unplanned volume** | Events received whose name is not in the tracking plan ÷ total events | ≤5% | Every unplanned event is unanalysable and may be duplicating a planned one under a different name |
| **Unattributed volume** | Events with a null or unresolvable `account_id` ÷ total events | ≤10% | Directly reduces the volume join rate; see `identity-resolution.md` §2 |
| **Anonymous share** | Events not attributable to a person profile ÷ total events | Measured and explained | Pre-login and marketing-site traffic is legitimately anonymous; anonymous events *inside* the authenticated product are a bug |

Platforms distinguish these natively — PostHog, for example, separates identified events
(attributable to a person profile) from anonymous ones, and separates autocaptured interactions
from deliberately instrumented custom events `[V — PostHog docs, Events]`. Report the split.

**Autocapture is not instrumentation.** Autocaptured clicks and pageviews are useful for
exploration and near-useless for CS scoring, because they are not stable across UI changes — a
button moves and the "event" disappears. A taxonomy whose core action is an autocaptured
selector will break silently at the next redesign. If autocapture carries the core action, that
is a finding, and the fix is a deliberate custom event.

---

## 5. Property completeness on the events that matter

Do not audit property completeness across all events. Audit it on the handful the library
actually consumes.

| Event class | Required properties | Consumed by |
| --- | --- | --- |
| Core action | `account_id`, `user_id`, `timestamp`, `environment`, feature/surface key | Every depth and decay signal |
| Seat/entitlement events (`seat_limit_reached`, `invite_blocked`, `user_invited`) | `account_id`, `inviter_id`, `invitee_email`, `timestamp` | Expansion sizing — the highest-yield expansion signal and the one most often missing |
| Metered usage snapshot (daily) | `account_id`, `meter_key`, `value`, `included_qty`, `timestamp` | Consumption pacing; commit-utilisation risk |
| Integration lifecycle (`integration_connected`, `sync_failed`) | `account_id`, `integration_key`, `connected_by`, `timestamp` | Technical risk signals — high precision, low volume |
| Identity/provisioning (`user_created`, `user_deactivated`, `sso_enabled`) | `account_id`, `user_id`, `timestamp` | Deprovisioning-burst detection, one of the strongest late signals |
| Admin/config (`workflow_disabled`, `automation_paused`, `data_exported`) | `account_id`, `actor_id`, `scope`, `timestamp` | Migration-behaviour detection |

Report per-event property completeness as a percentage, and name any event where `account_id`
is optional. An optional `account_id` on a core event is a defect, not a configuration choice.

---

## 6. Taxonomy versioning and the fleet-decay test

**The failure this prevents:** a release renames `report_published` to `Report Published`,
nobody backfills, and every account's core-action volume drops to zero on the same day. The risk
model fires "zero core-action usage for 30 consecutive days" — an override floor of 75 in
`churn-risk` — across the entire book at once.

### The test

```sql
-- Fleet decay vs account decay in the same window.
-- If the fleet moved with the accounts, suspect instrumentation, not customers.
WITH per_account AS (
  SELECT account_id,
         SUM(core_actions) FILTER (WHERE date >= CURRENT_DATE - 28)                      AS cur,
         SUM(core_actions) FILTER (WHERE date >= CURRENT_DATE - 56
                                     AND date <  CURRENT_DATE - 28)                      AS prev
  FROM usage_daily WHERE date >= CURRENT_DATE - 56 GROUP BY 1
)
SELECT
  ROUND(100.0 * SUM(cur) / NULLIF(SUM(prev),0) - 100, 1)                     AS fleet_pct_change,
  COUNT(*) FILTER (WHERE prev > 0 AND cur < 0.6 * prev)                      AS accounts_down_40pct,
  COUNT(*)                                                                   AS accounts_total
FROM per_account;
```

| Fleet change | Accounts down ≥40% | Reading |
| --- | --- | --- |
| ≈0% | A handful | Real, account-specific decay. Trust the signals |
| −35% | Most of the book | **Instrumentation event.** Check the deploy log for that date before escalating anything |
| −35% | A handful | Real, concentrated decay — likely a segment-wide or seasonal effect. Check the segment cut |

### Versioning requirements

| Requirement | Why |
| --- | --- |
| Every rename recorded with a date and the old→new mapping | Makes historical series joinable across the rename |
| Deprecations announced with a sunset date, both names emitted during overlap | Prevents the cliff entirely |
| A `taxonomy_version` property on events, or a dated schema registry | Lets an analyst know which rules applied to a given date range |
| Analytics on the release checklist | The cheapest control in this file; costs one checkbox |

---

## 7. The minimum event contract for CS

If these are not emitted, large parts of the library cannot operate. This is the instrumentation
ask that goes into the remediation plan, with the specific downstream capability each one buys.

| Event | Required properties | Unlocks |
| --- | --- | --- |
| Core action (named per `cs-context` §5) | `account_id`, `user_id`, `timestamp`, `environment` | Depth, decay, activation, time-to-value |
| `user_invited` / `user_created` / `user_deactivated` | `account_id`, `actor_id`, `subject_id`, `timestamp` | Provisioning stop and deprovisioning burst |
| `seat_limit_reached` / `invite_blocked` | `account_id`, `attempted_user_email`, `inviter_id`, `timestamp` | Seat-expansion sizing |
| Daily account rollup | `active_users_30d`, `contracted_seats`, `core_actions`, `feature_breadth_90d`, `integrations_active` | Utilisation, breadth, stickiness — the whole usage family |
| `integration_connected` / `sync_failed` | `account_id`, `integration_key`, `timestamp` | Technical risk signals |
| `data_exported` (bulk) | `account_id`, `actor_id`, `scope`, `row_count`, `timestamp` | Migration-behaviour override floor |
| `sso_enabled` / `scim_enabled` | `account_id`, `timestamp` | Deployment maturity; deprovisioning visibility |
| `milestone_completed` | `account_id`, `milestone_key`, `verified_by`, `timestamp` | Value realisation, success-plan tracking, QBR evidence |

**Sequence the core action and the seat events first.** They are the two with the largest
downstream footprint, and both are irreversible — an event you do not emit today is history you
cannot reconstruct.

---

## 8. Scoring the domain

Feeds the **fidelity** dimension of the product-usage family in `audit-procedures.md` §9.

| Sub-check | Weight | Full marks |
| --- | --- | --- |
| Core action defined and validated against outcomes (§1) | 30% | Validated, retained ≥2× churned at T−180 |
| Surface coverage (§2) | 20% | All surfaces emit; zero accounts in the API-only list |
| Naming conformance + tracking plan exists and is enforced (§3) | 20% | ≥90% conformance, plan enforced at ingest |
| Unplanned ≤5% and unattributed ≤10% (§4) | 20% | Both inside threshold |
| Versioning and the fleet-decay control (§6) | 10% | Change log exists; the test runs automatically |

Report the sub-scores, not just the total — the fix list follows directly from which sub-check
failed.

---

## 9. Fix menu, ranked

| # | Fix | Effort (person-days) | Irreversible if deferred? | Unlocks |
| --- | --- | --- | --- | --- |
| 1 | Define the core action and validate it against retained-vs-churned cohorts | 2 ops + 1 analyst | No, but everything else waits on it | The entire usage signal family |
| 2 | Instrument the core action on every surface | 5–15 eng | **Yes** | Depth, decay, activation, TTV |
| 3 | Emit `seat_limit_reached` / `invite_blocked` | 2–4 eng | **Yes** | Seat-expansion sizing |
| 4 | Write the tracking plan for the ~15 events CS consumes (not the whole product) | 3 ops | No | Makes unplanned volume measurable |
| 5 | Add `account_id` as a required property on core events | 2 eng | **Yes** | Cuts unattributed volume directly |
| 6 | Daily account-level rollup table | 3 eng | No — recomputable from raw events | Utilisation, breadth, all trend measures |
| 7 | Fleet-vs-account decay control on a schedule | 1 eng | No | Prevents fleet-wide false reds |
| 8 | Rename map + change log for existing events | 2 ops | No | Historical series survive renames |
| 9 | Enforce the plan at ingest (warn, then block) | 3 eng | No | Stops new drift |
| 10 | Full taxonomy rewrite across the product | 20–60 eng | No | **Usually premature.** Do items 1–5 first and re-measure |

**Item 10 is the trap.** A full taxonomy rewrite is the most commonly proposed and least
commonly justified fix in this domain. CS needs roughly fifteen events, not four hundred. Scope
the plan to the events the library consumes, ship those, and let the rest of the catalog stay
messy until a decision depends on it.
