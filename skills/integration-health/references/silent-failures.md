# Silent Failures

> The nine ways a customer's data goes wrong while every dashboard stays green. None of them
> generates an alert, and none of them generates a ticket — which is why ticket volume is the one
> metric that cannot detect them (`C21`).
>
> Evidence labels: `[M]` measured · `[V]` vendor-published · `[P]` practitioner convention ·
> `[A]` standard or peer-reviewed · `[D]` primary product documentation, with the fetch date.

**Contents**

- [Why this class of failure is different](#why-this-class-of-failure-is-different)
- [The sweep — run all nine, print the clean ones](#the-sweep--run-all-nine-print-the-clean-ones)
- [S1 · Partial batch drop](#s1--partial-batch-drop)
- [S2 · Silently coerced type](#s2--silently-coerced-type)
- [S3 · Filtered records](#s3--filtered-records)
- [S4 · Paused, not failed](#s4--paused-not-failed)
- [S5 · Credential with reduced scope](#s5--credential-with-reduced-scope)
- [S6 · Webhook 200-and-discard](#s6--webhook-200-and-discard)
- [S7 · Pagination truncated](#s7--pagination-truncated)
- [S8 · Window shifted by timezone or DST](#s8--window-shifted-by-timezone-or-dst)
- [S9 · Upsert key collision](#s9--upsert-key-collision)
- [The reconciliation method](#the-reconciliation-method)
- [What to say, and what never to say](#what-to-say-and-what-never-to-say)

---

## Why this class of failure is different

A loud failure has three properties that make it easy: it stops, it alerts, and someone reports it.
A silent failure has none of them. The job keeps running, the monitor stays green, and the customer
does not file a ticket — because from where they sit there is no failure to report. There is a
number that looks wrong.

That produces three consequences worth stating plainly:

| Consequence | Why it matters commercially |
| --- | --- |
| **The customer blames the product, not the connector** | "Your reporting is unreliable" is a conclusion about the product, and it is the kind that survives a fix |
| **Detection latency is measured in months** | The gap between onset and discovery is usually bounded only by when someone happens to check a number by hand |
| **It compounds into the renewal quietly** | By the time it surfaces, the position is "we already stopped trusting it", which is a trust conversation rather than a bug |

Poor data quality is expensive at organisation scale — Gartner's widely-cited figure, from its 2020
Magic Quadrant reference survey of 154 customers, puts the average cost at roughly **$12.9 million
a year** `[V · Gartner, 2020]`. Treat that as directional context for why a customer reacts the way
they do, never as an estimate of a specific defect's cost. The cost of *this* defect is computed
from the records affected and the workflow they feed, or it is `UNKNOWN`.

---

## The sweep — run all nine, print the clean ones

| Code | Failure | Primary detector | Cheapest evidence |
| --- | --- | --- | --- |
| `S1` | Partial batch drop | Run-level identity | The job log you already have |
| `S2` | Silently coerced type | Field-level checksums | One query per numeric/text field |
| `S3` | Filtered records | Expected column set + row population | Source vs destination count |
| `S4` | Paused, not failed | Schedule adherence | Scheduler history |
| `S5` | Credential with reduced scope | Granted vs required scopes | The token introspection response |
| `S6` | Webhook 200-and-discard | End-to-end event-ID reconciliation | Emitted vs materialised event IDs |
| `S7` | Pagination truncated | Page count vs total count | The API's own total, where it returns one |
| `S8` | Window shifted by timezone or DST | Boundary record census | Count records at the window edges |
| `S9` | Upsert key collision | Distinct external IDs vs rows written | One `GROUP BY` |

**Print the clean results.** "S2 clear — field-level checksums matched on amount, quantity and
external_id over 2026-08-01 → 08-28" is a finding. Dropping the row makes the sweep unverifiable,
which defeats its purpose.

---

## S1 · Partial batch drop

| | |
| --- | --- |
| **What happens** | The job completes. A subset of records inside it never lands, usually rejected one at a time on a validation or referential rule |
| **What the dashboard shows** | Job status complete. Freshness green. Error count often zero, because per-record rejections are held in a separate result set |
| **Why nothing fires** | Job state and record outcomes are different objects. Bulk-load APIs expose successful, failed and unprocessed records through their own endpoints, so a client that reads only job state reports success `[D · Salesforce Bulk API 2.0 developer guide, fetched 2026-08-28]` |
| **Detection** | The run identity: `submitted = succeeded + failed + unprocessed`. Any residual is a lost-record count |
| **Confirming test** | Fetch the failed and unprocessed result sets explicitly and cluster them by cause. A single dominant cause is a schema or validation change with a date; a scatter is usually data quality on their side |
| **Disconfirming test** | Records legitimately filtered by design (an agreed exclusion rule), and records that succeeded on a retry within the same window — reconcile on distinct IDs, not on counts, when retries are in play |
| **The fix** | Fetch and persist per-record results on every run; backfill the identified records; add the identity as a hard gate that fails the run |
| **The detector left behind** | Reconciliation per run — `expected − succeeded` — alerting on any unaccounted record, not on a percentage |

```sql
-- L1: does the run's own arithmetic close?
SELECT run_id, submitted,
       succeeded + failed + unprocessed              AS accounted,
       submitted - (succeeded + failed + unprocessed) AS residual
FROM   connector_run
WHERE  started_at >= CURRENT_DATE - 30
  AND  submitted <> succeeded + failed + unprocessed
ORDER  BY residual DESC;
```

---

## S2 · Silently coerced type

| | |
| --- | --- |
| **What happens** | A value is cast at the boundary and loses information: a decimal truncated to an integer, a long string cut at a column width, a timestamp reduced to a date, a large integer overflowing into a float |
| **What the dashboard shows** | Green, with full row counts. Row counts are the metric that cannot see this |
| **Why nothing fires** | The cast succeeded. Truncation and precision loss are not errors — a column type change can truncate or lose data with no exception raised, so the pipeline keeps running while the numbers are wrong `[P]` |
| **Detection** | Field-level checks: type and range assertions at the boundary, plus distribution comparison — `SUM`, `AVG`, `COUNT(DISTINCT)`, `MAX(LENGTH(...))` — between source and destination on the matched set |
| **Confirming test** | Does the destination `SUM` differ from the source `SUM` by less than one row's worth per row? That is rounding, not loss. Does `MAX(LENGTH(field))` sit exactly on a column width? That is truncation |
| **Disconfirming test** | A deliberate, documented transformation — currency conversion, rounding to cents, a defined truncation. Check the mapping document before calling it a defect |
| **The fix** | Widen the destination type or make the transformation explicit and documented; re-extract the affected range |
| **The detector left behind** | Nightly checksum on money, quantity and identifier fields, plus a `MAX(LENGTH)` assertion against every text column width |

**Where it hides most often:** money stored as text and cast on load; identifiers longer than the
destination column, which truncate into *collisions* rather than into nulls; and timestamps that
lose their time component and then break a windowed join.

---

## S3 · Filtered records

| | |
| --- | --- |
| **What happens** | Rows or fields are removed on the source side before the API ever returns them — a sharing rule, a field-level permission, a view filter, a record-type restriction |
| **What the dashboard shows** | Green, fewer rows, no error |
| **Why nothing fires** | Filtering is not an error condition. Salesforce field-level security **omits** an unreadable field from the response rather than raising: a field with Read = false is returned as null in SOQL and excluded from responses, so an integration user missing a permission gets *fewer columns*, not an error `[D · Salesforce Security Guide, fetched 2026-08-28]` |
| **Detection** | Assert the expected column set on every response, and the expected row population for the window. Alert on the **delta** in skipped/filtered counts, never on an absolute |
| **Confirming test** | Run the same query as an unrestricted user and diff the result. If the difference is a permission, the row count changes with the identity, not with the data |
| **Disconfirming test** | A deliberate filter change on their side, or a genuine drop in source volume. Check their change log and compare against a second connector reading the same objects |
| **The fix** | Restore the permission or the field on a named integration user; re-extract the window; pin the required column set into a contract test |
| **The detector left behind** | Column-set assertion per run, plus L2 day-level source-vs-destination counts |

**Why the delta and not the absolute.** A filter that has always removed 200 rows a day is
invisible in an absolute threshold set above 200. The day it starts removing 900 is the signal, and
only a delta alarm sees it.

---

## S4 · Paused, not failed

| | |
| --- | --- |
| **What happens** | The job does not run. A schedule disabled during maintenance, a webhook endpoint auto-disabled after a failure streak, a connector left paused after a migration, a workflow deactivated by a person who then left |
| **What the dashboard shows** | Green — the last run succeeded. Every metric describes that run |
| **Why nothing fires** | A job that never ran produces no failures. Absence is not an event |
| **Detection** | Schedule adherence: `runs_observed ÷ runs_expected` over 24 hours (and over 30 days for weekly and monthly jobs). A "last success" timestamp measures staleness, never absence |
| **Confirming test** | Compare the scheduler's own history against the declared schedule, and check for an `endpoint_disabled_at` or `paused_at` value with an actor attached — who paused it, and when |
| **Disconfirming test** | An agreed pause — a migration freeze, a contract suspension, a seasonal shutdown. It should be in a change record; if it is not, that is the finding |
| **The fix** | Resume, backfill the missed windows, and add a resume step to the maintenance runbook so the pause cannot outlive the maintenance |
| **The detector left behind** | Schedule-adherence alarm, hourly for sub-daily jobs and daily for weekly ones. This is the only detector that catches a job which never started |

**The highest-risk home for `S4` is the weekly or monthly extract**, because one missed run is a
whole cycle and the freshness threshold for a weekly job is seven days wide.

---

## S5 · Credential with reduced scope

| | |
| --- | --- |
| **What happens** | A token is re-issued with fewer scopes than the original grant — a re-consent that dropped an optional scope, an admin narrowing a permission set, a policy change on their identity provider |
| **What the dashboard shows** | Green — authentication succeeds |
| **Why nothing fires** | The credential is valid. Reads that need the missing scope return empty or partial results rather than `403`, and empty is indistinguishable from "no records this window" |
| **Detection** | Assert `scopes_granted ⊇ scopes_required` on every token refresh — the OAuth 2.0 framework permits an issued token's scope to be narrower than requested, so the client must inspect what it actually received `[A · RFC 6749 §3.3]` — and run one canary read per scope |
| **Confirming test** | Introspect the token, or read the `scope` field on the refresh response, and diff it against the required set. Then run a read known to return rows and confirm it does |
| **Disconfirming test** | A deliberate scope reduction agreed as part of a security review. Then the fix is to remove the dependent feature, not to restore the scope quietly |
| **The fix** | Re-consent with the full required scope, using a service account rather than a person; then pin the required scope list into the connector's configuration |
| **The detector left behind** | Scope assertion on every refresh, plus a per-scope canary read on a daily schedule |

Related: a credential that is valid but held by a departing employee — see
`credential-lifecycle.md` §The service account that was a person.

---

## S6 · Webhook 200-and-discard

| | |
| --- | --- |
| **What happens** | The receiver acknowledges an event and never materialises it: the queue was full, the handler threw after the ack, a dedupe key collapsed distinct events, or a bug returns a `4xx` the provider treats as final |
| **What the dashboard shows** | 100% delivery success on the provider's side |
| **Why nothing fires** | Delivery status is the sender's view. Providers deliver at-least-once and retry on failure, but treat `4xx` responses as permanent and do not retry them — so a handler bug returning `400` deletes events with no error visible anywhere `[P]` |
| **Detection** | End-to-end reconciliation on **event IDs**: events emitted vs events materialised downstream, for the same window. Never on delivery status |
| **Confirming test** | Take the provider's delivery log for a window, extract the event IDs, and left-join against the destination. The unmatched set is the loss, by ID |
| **Disconfirming test** | Events legitimately discarded by an agreed filter, and duplicates correctly deduplicated — dedupe *should* reduce the count, so compare distinct IDs, not rows |
| **The fix** | Ack only after durable persistence: verify signature, deduplicate on the event ID, write the raw event to a durable queue, return `200`/`202`, then process asynchronously `[P]`. Replay the unmatched IDs |
| **The detector left behind** | Daily emitted-vs-materialised event-ID reconciliation, and an alarm on any `4xx` returned by our own receiver |

**Two adjacent traps.** A handler that takes longer than the provider's timeout is marked failed
and retried even though it succeeded — which produces duplicates, not losses, and needs
idempotency rather than a fix to the handler. And a dedupe key that is not the provider's event ID
will collapse genuinely distinct events; dedupe on the ID the provider guarantees stable across
retries `[P]`.

---

## S7 · Pagination truncated

| | |
| --- | --- |
| **What happens** | The client stops early — a cursor cap, a fixed maximum page count, a loop that exits on an empty page while the API paginates sparsely, or an offset-based pager racing concurrent writes |
| **What the dashboard shows** | Green, with a plausible record count. It is always plausible, which is the difficulty |
| **Detection** | Compare pages consumed against the API's own total count where it returns one; otherwise reconcile at L2 (day-level source vs destination counts) |
| **Confirming test** | Re-run the extract with a page-count ceiling removed and diff. If the count changes, the pager was the limit |
| **Disconfirming test** | An intentional cap for a smoke test or a rate-limit strategy. It should be configuration with a name, not a constant in a loop |
| **The fix** | Cursor-based pagination with an explicit termination condition, and a run-level assertion that pages consumed × page size ≥ reported total |
| **The detector left behind** | Assert the API's reported total against rows written, per run |

**Offset pagination over a changing table loses and duplicates rows simultaneously** — a record
inserted between page 3 and page 4 shifts the window. Prefer a stable cursor ordered on an
immutable key.

---

## S8 · Window shifted by timezone or DST

| | |
| --- | --- |
| **What happens** | The extract window is computed in one timezone and the source stores another. On DST transitions an hour is read twice or not at all; across timezones a whole day's boundary records move |
| **What the dashboard shows** | Green, with a count that is off by a fraction of a day |
| **Detection** | Count records at the window boundaries — the first and last hour of each window — and compare consecutive windows for overlap and gap. Two windows should tile exactly |
| **Confirming test** | Look at the transition dates specifically. A gap or a duplicate concentrated on a clock-change weekend is conclusive |
| **Disconfirming test** | A genuine quiet hour overnight. Compare against the same hour on adjacent days |
| **The fix** | Store and query in UTC, convert only at display, and use half-open intervals `[start, end)` so windows tile without overlap |
| **The detector left behind** | A window-tiling assertion: every record's timestamp falls in exactly one processed window |

---

## S9 · Upsert key collision

| | |
| --- | --- |
| **What happens** | An upsert runs on an external ID that is not unique — blank, defaulted, truncated (`S2`), or unique only within a scope the pipeline ignores. Distinct source records overwrite one another |
| **What the dashboard shows** | Green, with **fewer** destination rows than source rows and no errors at all |
| **Detection** | `COUNT(*)` vs `COUNT(DISTINCT external_id)` on the source, and rows written vs distinct keys on the destination |
| **Confirming test** | Group the source by the upsert key and look for groups above one. Any group above one is a guaranteed overwrite |
| **Disconfirming test** | A deliberate deduplication where the key genuinely identifies the entity and the last write should win — then the count difference is intended, and should be documented |
| **The fix** | A unique constraint on the external ID at the destination, so a collision errors instead of overwriting; then re-key and re-extract |
| **The detector left behind** | A uniqueness assertion on the upsert key before every load, failing the run rather than warning |

```sql
-- Does the upsert key actually identify a record?
SELECT external_id, COUNT(*) AS rows_sharing_key
FROM   source_extract
WHERE  extracted_at >= CURRENT_DATE - 7
GROUP  BY external_id
HAVING COUNT(*) > 1
ORDER  BY 2 DESC;
```

---

## The reconciliation method

The order to work in, and the exit condition for each step.

| Step | Do | Exit condition |
| --- | --- | --- |
| 1 | Fix the window. State it, in UTC, half-open, and use the same one on both sides | Both queries name the identical interval |
| 2 | Count at the source, unrestricted by the integration user's permissions | A number with a provenance tag |
| 3 | Count at the destination for the same window | A number with a provenance tag |
| 4 | If they differ, move to entity level: extract IDs both sides and diff the sets | A list of missing IDs, not a difference |
| 5 | Cluster the missing IDs by a common attribute — date, record type, owner, field value | A named cause, or an explicit "no common attribute; cause `UNKNOWN`" |
| 6 | For matched records, run field-level checks on money, quantity and identifier fields | Checksums match, or a named field with a named discrepancy |
| 7 | Write the loss statement: count, window, cause, and whether the affected records are recoverable | A sentence a customer could read, with no internal language in it |

**The output of a reconciliation is a count and a window, or it is `UNKNOWN`.** There is no third
answer, and "we believe no data was lost" is not one of them.

---

## What to say, and what never to say

| Never write | Write instead |
| --- | --- |
| "No data loss detected" | "Reconciled at L2 for 2026-08-03 → 08-19: 412 records missing of 71,340 expected" — or "`UNKNOWN — requires source counts for that window`" |
| "A small number of records" | The count |
| "Some records may have been affected" | The count and the window, or the reason the count cannot be produced and what would produce it |
| "The integration is healthy" | The eight dimension bands, and the reconciliation level you ran |
| "The customer did not notice" *(to the customer)* | Nothing. This is an internal observation and it stays internal (`R18`) — it is also the `T2` signal, and it belongs in the renewal read |
| "It has been fixed" | What was fixed, what was backfilled, what was verified against their counts, and the detector now in place |

The disclosure decision, the leak scan and the copy block: `../SKILL.md` Step 8 and
`../../cs-context/references/customer-voice.md`.
