# Identity Resolution Audit — measuring the join, cataloguing the breakage, pricing the damage

> Every usage-derived number in customer success is multiplied by the join rate. A 68% join
> rate does not make your utilisation chart 68% right — it makes it wrong in a specific,
> non-random direction, because the users who fail to resolve are concentrated in the largest
> and most complex accounts.

**Contents**
1. [The resolution ladder](#1-the-resolution-ladder)
2. [Measuring the join rate — three numbers, not one](#2-measuring-the-join-rate--three-numbers-not-one)
3. [The breakage catalogue](#3-the-breakage-catalogue)
4. [Quantifying the damage](#4-quantifying-the-damage)
5. [Duplicates and the entity grain](#5-duplicates-and-the-entity-grain)
6. [Internal, test and sandbox exclusion](#6-internal-test-and-sandbox-exclusion)
7. [Fix menu, ranked](#7-fix-menu-ranked)
8. [What to write in the report](#8-what-to-write-in-the-report)

---

## 1. The resolution ladder

Try in order, stop at first hit, and **record which rung resolved each user** — the distribution
across rungs is itself a finding.

| Rung | Rule | Precision | Notes |
| --- | --- | --- | --- |
| 1 | Explicit `org_id` / `workspace_id` / `tenant_id` emitted by the product, mapped to `account.product_org_id` | Highest | The only rung that is deterministic by construction. If most of your volume resolves here, identity is a solved problem and the remaining rungs are edge cases |
| 2 | `contact.email` exact match | High | Breaks on aliases, plus-addressing, and shared inboxes |
| 3 | Email domain match against `account.domains[]` | Medium | Requires a maintained domain list; **never apply to free-email providers** |
| 4 | `billing_id` → CRM account | High | Good for account-level facts, useless for user-level ones |
| 5 | Manual override table | Exact by definition | Must have an owner and a review date, or it becomes archaeology |

**Rung distribution diagnostic**

| Pattern | Reading |
| --- | --- |
| >80% on rung 1 | Healthy. Audit the remainder and move on |
| Majority on rung 3 | Fragile. Every domain change, subsidiary and consultant is a silent error |
| Anything on rung 3 matching gmail.com / outlook.com / yahoo.com / icloud.com / proton.me | A bug, not a rule. One free-email match can attach an entire consumer population to one account |
| Rung 5 carrying >5% of ARR | The override table has become the pipeline. Fix rung 1 |

---

## 2. Measuring the join rate — three numbers, not one

They diverge, and **the divergence is the finding**.

```
User join rate   = distinct product users resolving to an account ÷ all distinct product users
Volume join rate = events carrying a resolved account_id ÷ all events
ARR join rate    = ARR of accounts with ≥1 resolved user in 30d ÷ total ARR of active accounts
```

```sql
-- User and volume join rates over the last 90 days
SELECT
  COUNT(DISTINCT contact_id)                                              AS users_all,
  COUNT(DISTINCT contact_id) FILTER (WHERE account_id IS NOT NULL)        AS users_resolved,
  ROUND(100.0 * COUNT(DISTINCT contact_id) FILTER (WHERE account_id IS NOT NULL)
              / NULLIF(COUNT(DISTINCT contact_id),0), 1)                  AS user_join_rate,
  COUNT(*)                                                                AS events_all,
  COUNT(*) FILTER (WHERE account_id IS NOT NULL)                          AS events_resolved,
  ROUND(100.0 * COUNT(*) FILTER (WHERE account_id IS NOT NULL)
              / NULLIF(COUNT(*),0), 1)                                    AS volume_join_rate
FROM usage_event
WHERE timestamp >= CURRENT_DATE - 90;

-- ARR join rate
SELECT ROUND(100.0 * SUM(a.arr) FILTER (WHERE u.account_id IS NOT NULL)
                   / NULLIF(SUM(a.arr),0), 1) AS arr_join_rate
FROM account a
LEFT JOIN (SELECT DISTINCT account_id FROM usage_event
           WHERE timestamp >= CURRENT_DATE - 30 AND account_id IS NOT NULL) u
       ON u.account_id = a.account_id
WHERE a.status = 'active' AND a.is_internal = FALSE;
```

### Reading the divergence

| Pattern | What it means | What to do |
| --- | --- | --- |
| User rate high, volume rate low | A small number of very active unresolved users — usually API keys, service accounts or an integration partner | Attribute the service accounts; they are often your biggest customers' automation |
| Volume rate high, user rate low | Many low-activity unresolved users — trial signups, free-email evaluators, consultants | Lower priority for risk scoring, higher priority for PLG expansion analysis |
| ARR rate below both | The unresolved users sit at your **large** accounts | Highest-severity finding in the domain. Enterprise deployments with SSO or private hosting often stop emitting identifiable users entirely |
| All three ≥95% | Move on. Spend the effort on labels instead | |

### Pass criteria and the confidence consequence

| Level | All three rates | Consequence |
| --- | --- | --- |
| Pass | ≥90% | No cap from this domain |
| Caution | 80–90% | Note the rate on every usage-derived claim; cap the usage family's fidelity score |
| Fail | <80% | Usage-derived risk scores are **Low confidence** at best. State plainly that the unresolved users are not randomly distributed |
| Severe | <60% | Do not publish per-account utilisation at all. Publish the join rate instead — it is the more useful number |

---

## 3. The breakage catalogue

Walk all seven, every audit. Print the ones measured at zero — "checked, none found" is a
result the reader needs.

| # | Case | How to detect it | Direction of error | Metric it distorts | Standard fix |
| --- | --- | --- | --- | --- | --- |
| B1 | **Free-email users at a paying account** | Unresolved users whose domain is a public mailbox provider, whose activity overlaps a known account's workspace | **Under-counts active users → false RED** | Licence utilisation, WAU/MAU, active-user penetration | Explicit `contact` mapping. Never domain-match a free provider |
| B2 | **Multi-domain enterprises** (acme.com, acme.co.uk, acmegroup.com) | Cluster unresolved domains by shared workspace/org id or by contact overlap; check CRM for similarly named accounts | **Splits one account into several → understates ARR, splits health, breaks segment assignment** | ARR per account, segment boundaries, utilisation, NRR cohorting | Maintain `account.domains[]`; add a review step at contract signature |
| B3 | **Agencies and consultants using the product for a client** | One user active across many `product_org_id`s; email domain matches neither party's account | **Attributes usage to the wrong account — inflates one, deflates another** | Everything downstream of usage, in both directions | `contact.is_external_collaborator` flag; exclude from per-seat utilisation, include in engagement |
| B4 | **Subsidiaries with separate contracts** | Accounts sharing a domain root or a parent in the enrichment source, with distinct `subscription` rows | **Rolls up incorrectly — either double-counts ARR or hides a churning subsidiary inside a healthy parent** | ARR, logo counts, cohort membership, GRR | `account.parent_account_id` plus an explicit decision on reporting grain, written down |
| B5 | **Employees testing in production** | Internal email domain; usage patterns clustered on weekdays with admin actions; accounts created by staff | **Inflates usage → false GREEN, on exactly the accounts you demo most** | Utilisation, activity trend, activation rate | `account.is_internal` with a documented rule; exclude everywhere, including in the denominator |
| B6 | **Shared / service accounts** | One `contact_id` with implausible session counts, concurrent sessions from multiple IPs, or a generic local part (`ops@`, `admin@`, `integrations@`) | **One "user" hides many humans → overstates per-seat utilisation, understates seat need** | Licence utilisation, seat-expansion sizing, per-user depth | Flag and exclude from per-seat utilisation; count separately as service identities |
| B7 | **Post-acquisition domain change** | A sharp drop in resolved users for one account coinciding with a rise in unresolved users on a new domain | **Looks like total usage collapse → false RED and a wasted save motion** | Every usage signal at once, catastrophically | Watch for domain migrations before declaring churn risk; add the new domain to `account.domains[]` |

**B7 is the one that burns CSMs.** A customer acquired in March migrates mailboxes in June, and
in July your risk model reports a 100% usage collapse on a happy, expanding account. Before any
"zero usage for 30 days" override floor fires, check whether an equivalent volume of unresolved
activity appeared on a new domain in the same window. That single check should be automated —
it is a two-line addition to the risk pipeline and it prevents the most embarrassing false red
in the library.

---

## 4. Quantifying the damage

Descriptions do not get funded. Recomputation does.

### The procedure

1. Take a **20-account sample** where the case applies, stratified by ARR.
2. Apply the fix by hand on those 20 (map the contacts, merge the domains, exclude the service
   accounts).
3. Recompute the affected metric before and after.
4. Report the **median delta**, the number of accounts that **cross a decision threshold**, and
   the **ARR attached to those crossings**.

### The template sentence

> **B6 shared/service accounts.** 34 accounts, $2.9M ARR. Licence utilisation is *overstated*
> by a median 11pp (0.71 → 0.60 recomputed on a 20-account sample). Nine accounts cross the
> 0.60 seat-reduction threshold once corrected, carrying $780k ARR — nine expansion
> conversations that should have been renewal-defence conversations.
> Fix: flag service identities on `contact`, exclude from per-seat utilisation. Effort: 3 days.

### Decision thresholds to test crossings against

These are the thresholds downstream skills actually act on, so a crossing is a changed decision,
not a changed number.

| Metric | Threshold | Consequence of crossing |
| --- | --- | --- |
| Licence utilisation | <0.60 | Seat-reduction risk at renewal |
| Licence utilisation | <0.40 | Churn risk |
| Licence utilisation | ≥0.85 | Seat-expansion candidate |
| Active-user decay ratio (`L28 ÷ 90d baseline`) | <0.70 for 2 consecutive periods | Usage-decay risk signal fires |
| Zero core-action days | 30 consecutive | Override floor 75 in `churn-risk` |
| Multithreading depth (90d) | ≤1 contact | Single-threaded flag |

Note the thresholds themselves: the seat-utilisation bands and decay ratios above are the
commonly configured practitioner values used across the CS tooling market `[P]`, not measured
benchmarks. They are the right thresholds to test crossings against **because they are the ones
your team acts on**, not because they are empirically derived. Say so.

---

## 5. Duplicates and the entity grain

```sql
-- Candidate duplicates: same normalised name or shared domain, both active
SELECT a1.account_id, a1.name, a1.arr, a2.account_id, a2.name, a2.arr
FROM account a1
JOIN account a2
  ON a1.account_id < a2.account_id
 AND (LOWER(REGEXP_REPLACE(a1.name,'[^a-z0-9]','','gi'))
      = LOWER(REGEXP_REPLACE(a2.name,'[^a-z0-9]','','gi'))
   OR a1.domains && a2.domains)
WHERE a1.status = 'active' AND a2.status = 'active'
ORDER BY GREATEST(a1.arr, a2.arr) DESC;
```

Pass: **zero duplicates in the top ARR decile.** Below that, record the count and move on —
deduplicating the long tail is expensive and changes no decision.

**Grain decisions to write down**, because they cannot be inferred and every downstream number
depends on them:

| Question | Options | Consequence of the choice |
| --- | --- | --- |
| Do subsidiaries roll up to the parent for retention reporting? | Roll up · Report separately · Both, with a flag | Changes GRR, logo counts and cohort membership |
| Is health scored at account or at deployment/instance? | Account · Instance, with a designated primary | Multi-instance customers otherwise score on whichever instance updated last |
| Is a multi-product customer one account or several? | One account, several `subscription` rows | Several accounts double-counts logos and breaks NRR |
| Are trial and paid the same account? | Same, with `status` transitions | Separate accounts destroys tenure and time-to-value |

---

## 6. Internal, test and sandbox exclusion

The exclusion rule must be **written, applied and testable**. Unwritten rules get reapplied
differently by every analyst.

| Pattern | Rule | Trap |
| --- | --- | --- |
| Employee email domain | `contact.email` domain ∈ company domains → exclude from customer usage | Employees who are also genuine users of a self-serve tier |
| Sandbox/test orgs | `usage_event.properties.environment <> 'production'` | Products that never emit an environment property — instrument it |
| Demo accounts | Named list, reviewed quarterly | Demo accounts that were converted to real paying customers and never reclassified |
| Partner/reseller accounts | `account.type = 'partner'` | Their end-customer usage may be your real signal; decide and document |

Failure here is a **false-green generator**: internal traffic inflates exactly the accounts your
team touches most, which are your reference accounts and your renewals-at-risk.

---

## 7. Fix menu, ranked

Ranked by decision value per unit of effort, not by ease.

| # | Fix | Effort (person-days) | Irreversible if deferred? | Unlocks |
| --- | --- | --- | --- | --- |
| 1 | Emit `org_id` / `workspace_id` on every product event and map it to `account.product_org_id` | 5–15 eng | **Yes** — un-emitted events cannot be backfilled | Rung 1 resolution; ends the whole class of problem |
| 2 | Build and own `account.domains[]` for the top 100 accounts by ARR | 2 ops | No | B2, B7; multi-domain and migration handling |
| 3 | Flag service identities and external collaborators on `contact` | 3 ops | No | B3, B6; correct per-seat utilisation |
| 4 | Write and apply the internal/test exclusion rule | 1 ops | No | B5; removes a systemic false-green |
| 5 | Deduplicate the top ARR decile | 2 ops | No | Correct ARR, segment assignment, cohort membership |
| 6 | Domain-migration watcher: alert when unresolved volume on a new domain rises as a known account's resolved volume falls | 2 eng | No | B7; prevents the most damaging false red |
| 7 | Set `parent_account_id` on all known subsidiary structures | 2 ops | No | B4; correct roll-up |
| 8 | Full CDP / identity-graph deployment | 40–100+ | No | **Usually premature** — see below |

**Fix 1 first, always**, even when its blast radius looks smaller than a fix further down. Every
day without it is a day of history you cannot reconstruct. Everything else on this list can be
applied retroactively to data you already hold.

**On fix 8.** A customer data platform resolves identifiers you are already emitting. If rung 1
is missing, a CDP inherits the same ambiguity and charges you for it. Sequence it after fix 1
and after the tracking plan exists, or it becomes an expensive re-implementation of rung 3.

---

## 8. What to write in the report

The identity section of the audit report must contain, in this order:

1. The three join rates, with the SQL window used.
2. The rung distribution.
3. The divergence reading (§2), stated as a sentence about which accounts are unresolved.
4. The full seven-row breakage catalogue, including zero-count rows.
5. For every non-zero case: detected count, accounts affected, **ARR affected**, direction of
   error, metric distorted, and the recomputed damage from a 20-account sample.
6. The duplicate count in the top ARR decile and the grain decisions (§5).
7. The internal-exclusion rule, quoted verbatim from wherever it is written — or
   `UNKNOWN — requires a documented exclusion rule` if it is not written anywhere.
8. The ranked fix list with effort and the irreversibility flag.

**The sentence that must appear if any rate is below 80%:**

> Product-to-account resolution is at <X>%. The unresolved users are not randomly distributed —
> they are concentrated in <the pattern you observed>. Every usage-derived figure in this
> library is therefore a floor, not a measurement, and confidence on the product-usage family
> is capped at Low until resolution exceeds 80%.
