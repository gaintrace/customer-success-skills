# The Eight Health Dimensions

> Thresholds, tuning by connector class, and the trap that makes each dimension read green when it
> should not. Every band in `../SKILL.md` Step 2 is defined here, with the reason it sits where it does.
>
> Evidence labels: `[M]` measured · `[V]` vendor-published · `[P]` practitioner convention ·
> `[A]` standard or peer-reviewed · `[D]` primary product documentation, with the fetch date.
> A threshold labelled `[P]` is a **library convention chosen deliberately**, not a measurement —
> change it when your own incident history disagrees, and record that you did.

**Contents**

1. [How to use this file](#1-how-to-use-this-file)
2. [Connector classes — the unit thresholds are tuned to](#2-connector-classes--the-unit-thresholds-are-tuned-to)
3. [Dimension 1 · Freshness vs expected](#3-dimension-1--freshness-vs-expected)
4. [Dimension 2 · Error rate by class](#4-dimension-2--error-rate-by-class)
5. [Dimension 3 · Latency p50 / p95](#5-dimension-3--latency-p50--p95)
6. [Dimension 4 · Throughput vs expected](#6-dimension-4--throughput-vs-expected)
7. [Dimension 5 · Partial failure and the reconciliation identity](#7-dimension-5--partial-failure-and-the-reconciliation-identity)
8. [Dimension 6 · Schema drift](#8-dimension-6--schema-drift)
9. [Dimension 7 · Deprecation exposure](#9-dimension-7--deprecation-exposure)
10. [Dimension 8 · Credential runway](#10-dimension-8--credential-runway)
11. [Rolling up to a severity band](#11-rolling-up-to-a-severity-band)
12. [False positives worth knowing](#12-false-positives-worth-knowing)

---

## 1. How to use this file

Each dimension has four parts, and a score without all four is not defensible:

| Part | Why it exists |
| --- | --- |
| **The measure** | The exact arithmetic, so two people scoring the same connector get the same band |
| **The bands** | Green / Amber / Red with numbers, not adjectives |
| **The tuning** | What changes the threshold — connector class, business model, contractual commitment |
| **The trap** | The innocent explanation that must be excluded before escalating. Skipping this is how an integration report loses its audience |

**A dimension with no data is `UNKNOWN`, never Green.** The absence of an error log is not the
absence of errors. Every `UNKNOWN` caps that connector's confidence and appears in the Coverage
Ledger, because the whole argument of this report is that green dashboards conceal things.

---

## 2. Connector classes — the unit thresholds are tuned to

Thresholds are meaningless without the class. A five-minute webhook and a weekly roster extract
fail differently and should not share a freshness rule.

| Class | Typical interval | What "late" costs | Freshness multiplier | Latency budget comes from |
| --- | --- | --- | --- | --- |
| **Event / webhook** | seconds | The workflow stalls in real time; a human is waiting | 1.5× interval, floor 15 min | The human's tolerance in the UI — usually 2–5 s end to end |
| **Near-real-time poll** | 1–15 min | Records arrive out of order or late into a live queue | 1.5× interval | The queue's own SLA, or the next downstream job's start time |
| **Hourly batch** | 60 min | A report is an hour stale; usually invisible | 2× interval | The next hour's window; overlap is the failure |
| **Nightly batch** | 1440 min | Someone opens a report at 08:00 and it is yesterday's | 1.25× interval (a nightly job has one chance) | The business start time minus job duration |
| **Weekly / monthly extract** | 7–30 d | Nobody notices for a cycle; the most common home for `S4` | 1.1× interval | The reporting deadline it feeds |
| **Reverse-ETL / warehouse push** | 15–60 min | Downstream models compute on stale inputs and the error compounds | 2× interval | The dbt run it precedes |

**The rule for setting a latency budget:** it comes from **their** deadline, never from a generic
percentile target. "p95 under 500 ms" means nothing; "the record must be in the warehouse before
the 06:00 model run" is a budget. Where no deadline exists, write
`UNKNOWN — requires the downstream deadline this connector feeds` and score latency as UNKNOWN.

---

## 3. Dimension 1 · Freshness vs expected

**Measure.** `(now − last_successful_sync_at) ÷ expected_interval`, where `now` is the collection
time of the evidence — not the moment you are reading it, and not the newest row in the file unless
you say so.

| Band | Threshold | Reading |
| --- | --- | --- |
| Green | ≤1.5× expected interval (class multiplier above) | Running |
| Amber | 1.5–3× | One or two runs missed; check the scheduler before the code |
| Red | >3× expected | Broken, not late |
| Red · `T2` risk | No successful sync in **7 days** | Signal `T2` in `../../cs-context/references/signal-library.md` |
| Red · `T2` severe | **30 days** unrepaired | Near-certain technical decoupling. Escalate commercially the same day |

**Tuning.** A nightly job gets 1.25×, because it has one attempt per day and a missed run is a
missed day. A five-minute webhook gets a 15-minute floor so ordinary jitter does not page anyone.

**Traps.**

| Trap | What to check |
| --- | --- |
| `last_successful_sync_at` updated by a heartbeat rather than by data | Does the timestamp move when zero records move? If so it measures liveness, not sync |
| The job ran and processed nothing | Freshness Green with throughput at zero is `S4` or `S3`, not health |
| Timezone or DST on a scheduled window | An hour appears and disappears twice a year; see `silent-failures.md` §S8 |
| A retry updating the timestamp before the write commits | Reconcile, do not trust the marker |
| Your own outage | A connector stale because *we* were down is our incident, not their decoupling. Check the status page before writing the renewal read |

---

## 4. Dimension 2 · Error rate by class

**The rule that makes this dimension useful: classify before you count.** A single blended error
rate averages a class that self-heals with a class that permanently destroys records, and the
average is actionable for neither.

| Class | Typical codes and shapes | Retry helps? | Band threshold | What it actually means |
| --- | --- | --- | --- | --- |
| **Auth** | `401`, `invalid_grant`, `invalid_token`, expired or revoked refresh token, expired client secret | Never — and retrying can trip lockout | **Any occurrence → Red** | The connection is down and stays down until a human acts |
| **Rate limit** | `429`, `quota_exceeded`, provider-specific throttles | Yes, with `Retry-After` and jittered backoff | >1% of calls over 7 d → Amber · **any record dropped instead of retried → Red** | Their volume outgrew the plan, or the client retries without jitter and queues against itself. Without jitter, clients resynchronise and generate more `429`s `[P]` |
| **Validation** | `400` on a field value, required field missing, picklist or enum value rejected, referential integrity | Never — the record is wrong for the target | >0.1% of records → Red | Their data changed shape. Each rejection is a real record that does not exist downstream |
| **Schema** | unknown field, type mismatch, `410 GONE` on a retired API version | Never | **Any occurrence → Red** | A contract broke. Nothing recovers without a code or config change |
| **Transient** | `502` `503` `504`, timeouts, connection reset, deadlock | Yes | <1% over 7 d → Green · sustained >5% → Amber | Infrastructure. A finding only when it persists, or when the retry path is not idempotent |
| **Permanent** | `404` on a deleted target, `403` on a revoked scope or removed object permission | Never | **Any occurrence → Red** | Something on their side was deleted or de-scoped and nobody told us. As much a relationship finding as a technical one |

**Why `429` gets its own row rather than living under transient.** A rate limit that is retried
correctly costs latency; a rate limit that is *not* retried costs records, and the two look
identical in a blended rate. Log every `429`, alert above a frequency threshold, and persist the
failed request so it can be retried rather than dropped `[P]`.

**Why validation sits at 0.1% and not 1%.** On a 20,000-record daily sync, 1% is 200 records a day
and 6,000 a month — enough to make a customer's report visibly wrong while the connector stays
green. 0.1% is the level at which a human still has a chance of reconciling the difference by hand.
This is a library convention `[P]`; tighten it to zero on billing, financial and regulated flows.

**Traps.** A retry storm inflates every rate because attempts rise faster than errors — compute
error rate over **distinct records**, not over attempts, whenever retries are in play. And an error
budget consumed entirely by one noisy endpoint is not an account-level finding; break the rate down
by endpoint class before escalating.

---

## 5. Dimension 3 · Latency p50 / p95

**Measure.** p50 and p95 of end-to-end time from source event to durable write downstream, against
**their** deadline.

| Band | Threshold |
| --- | --- |
| Green | p95 ≤ 0.5 × budget |
| Amber | p95 between 0.5 and 1.0 × budget |
| Red | p95 > budget · or p95 > 4 × p50 **and** p95 past half the budget |

**Never report a mean.** An average folds the distribution into a number that describes nobody:
the median is the typical experience and the tail is where the failures live, which is why Google's
SRE guidance recommends multiple graded latency objectives — for example 90% of requests under one
threshold and 99% under a looser one — rather than a single average `[P · Google SRE Workbook]`.

**The tail-ratio rule.** `p95 > 4 × p50` means a minority of records take a different code path:
retries, lock contention, cold starts, a pagination boundary, or one shard behaving differently.
It is worth investigating **only once the tail is material against the budget** — a connector at
p50 90 ms / p95 480 ms against a 2 s budget is fast and jittery, not broken, and flagging it trains
people to ignore the amber.

**Traps.**

| Trap | Correction |
| --- | --- |
| Measuring at the API boundary instead of end to end | Measure to the durable write the customer's workflow reads. Our `200` is not their data |
| Sampling only successful requests | Timeouts are the slowest requests and are usually excluded. Report the exclusion |
| A p95 computed across all connectors | Percentiles do not average. Compute per connector, per endpoint class |
| Comparing p95 across a release boundary | State the release. A latency step change with no code change is an infrastructure or volume change |

---

## 6. Dimension 4 · Throughput vs expected

**Measure.** `records_succeeded ÷ records_expected` for the same weekday.

| Band | Threshold |
| --- | --- |
| Green | 0.9–1.1× |
| Amber | 0.7–0.9× or 1.1–1.5× |
| Red | <0.7× or >1.5× |

**Where `expected` comes from, in priority order.** Take the first available and **say which you
used** — the choice changes the finding:

1. The volume stated in the SOW or order form. Contractual, and the only source that can show a
   decline that started before your observation window.
2. The customer's own stated volume, dated and attributed.
3. The trailing 28-day median **for that weekday**. Self-referential: a decline that began 40 days
   ago reads as normal. Record it as an assumption with that consequence.

**A high band is a finding too.** Throughput at 1.6× is a replay, a duplicate feed, an upsert key
collision, or a backfill nobody announced. Duplicates corrupt aggregates as effectively as losses.

**Traps.** Seasonality (month-end, quarter-end, their close week, their peak trading period);
a genuine business decline on their side, which is a `churn-risk` finding rather than an
integration defect; and a deliberate filter change that reduced volume by design — check the change
log on both sides before scoring.

---

## 7. Dimension 5 · Partial failure and the reconciliation identity

The dimension the rest of the report exists to protect. Two identities, both checked every run:

```
submitted  = succeeded + failed + unprocessed        ← residual = records whose fate is unknown
expected   = submitted                               ← shortfall = records never offered at all
unaccounted = max(0, residual) + max(0, shortfall)
```

| Band | Threshold |
| --- | --- |
| Green | `unaccounted = 0` |
| Amber | ≤0.1% of expected |
| Red | >0.1% of expected — **or any unaccounted record at all** on a billing, financial or regulated flow |

**Why the identity and not the job status.** Bulk-load APIs commonly report job state separately
from record outcomes: Salesforce Bulk API 2.0 exposes successful, failed and unprocessed record
results through their own endpoints, so a job can reach a completed state while thousands of
records failed, and a client that checks only job state reports success
`[D · Salesforce Bulk API 2.0 developer guide, fetched 2026-08-28]`.

**Four levels of reconciliation, in increasing strength.** Run the highest one the evidence allows,
and name the level you ran.

| Level | What it compares | Catches | Cost |
| --- | --- | --- | --- |
| **L1 · run** | Counts within one run, using the identity above | `S1` partial batch drop | Free — the numbers are already in the log |
| **L2 · day** | Source count for a date window vs destination count | `S3` filtered records, `S4` paused jobs | One query each side |
| **L3 · entity** | Source IDs minus destination IDs, as a set | Everything L2 catches, plus which records | A join; needs a stable external ID |
| **L4 · field** | Field-level checksums, sums and distinct counts on the matched set | `S2` type coercion, truncation, precision loss | Highest; run it on money, quantity and identifier fields at minimum |

**Never report "no data loss" from an L1 reconciliation.** L1 proves the job's own arithmetic is
consistent. It cannot see records that were never offered. State the level:
"reconciled at L1; L2 not possible — `UNKNOWN — requires source counts for 2026-08-03 → 08-19`."

---

## 8. Dimension 6 · Schema drift

Schema drift is a source-side change to fields, types or semantics that reaches the pipeline
without coordination. Undetected, it is a leading cause of silent data corruption — dropped or
renamed fields load as nulls, and type changes truncate rather than error, so the pipeline keeps
running while the numbers are wrong `[P]`.

| Change | Band | Why |
| --- | --- | --- |
| Field added, not required | Amber | Additive and usually safe; confirm intent, because it often signals a workflow change upstream |
| Field removed or renamed | **Red** | Downstream reads null. Renames are worse than removals — the old name silently returns nothing rather than erroring |
| Type widened (int → bigint, varchar → text) | Amber | Safe downstream, unsafe upstream if the destination is narrower |
| Type narrowed, or precision reduced | **Red** | Truncation. See `S2` in `silent-failures.md` |
| Nullability added to a previously required field | **Red** | Aggregates change meaning with no error anywhere |
| New required field on the target | **Red** | Every record without it is rejected one at a time while the batch completes |
| New enum / picklist value | **Red** | The single most common cause of one-record-at-a-time validation failure |
| Cardinality change (one-to-one becomes one-to-many) | **Red** | Joins fan out and counts inflate; this is the drift that shows up as throughput >1.5× |

**Detection.** Compare the observed field set and types against a declared contract on every run,
not on a schedule — a schema registry or contract test enforces compatibility rules and makes the
change visible at the boundary rather than in a report three weeks later `[P]`. Where no contract
exists, that is itself the first remediation: write it, from the current observed schema, and date it.

---

## 9. Dimension 7 · Deprecation exposure

| Band | Threshold |
| --- | --- |
| Green | Sunset beyond two renewal cycles |
| Amber | Sunset inside two renewal cycles |
| Red | Sunset **before the opt-out deadline**, or the version is already retired |

**Read it off the wire.** `RFC 9745` defines the `Deprecation` HTTP response header (Standards
Track, March 2025) and `RFC 8594` defines `Sunset` (Informational, May 2019) `[A]`. Log both on
every response; a client that ignores them learns about the retirement from a `410`.

**Record the vendor's policy, not a generic assumption.** The exposure differs by an order of
magnitude between policies:

| Policy shape | Example | What it means for the runway |
| --- | --- | --- |
| **Hard retirement with a date** | Salesforce retired platform API versions 21.0–30.0; calls now fail `410 GONE` (REST), `500 UNSUPPORTED_API_VERSION` (SOAP), `400 InvalidVersion` (Bulk) `[D · Salesforce Help, "Salesforce Platform API Versions 21.0 through 30.0 Retirement", fetched 2026-08-28]` | A dated cliff. Plan the migration against the opt-out deadline, not the sunset |
| **Date-based versioning, no forced migration** | Stripe pins an account to a dated version; monthly releases are backward-compatible and twice-yearly named releases carry the breaking changes `[D · docs.stripe.com/sdks/versioning, fetched 2026-08-28]` | No cliff, but drift accumulates. The risk is a pinned version so old that a needed feature is unreachable |
| **Rolling window (N most recent versions)** | Common in platform APIs | The clock restarts every release. Track releases per year, not the sunset date |
| **Undocumented** | Small vendors and customer-built middleware | `UNKNOWN — requires the vendor's versioning policy in writing`. This is a procurement question, not an engineering one |

**A customer's exposure clock is set by the strictest vendor in their stack**, so the runway is the
minimum across connectors, not the average.

---

## 10. Dimension 8 · Credential runway

| Band | Threshold |
| --- | --- |
| Green | Days to expiry ≥ 2× rotation lead time |
| Amber | 1–2× lead time |
| Red | Under the lead time · expired · or expiry `UNKNOWN` |

**An undated credential is unmeasured, not distant.** The default rotation lead is 21 days `[P]` —
enough to find the owner, get a change window and rehearse. Certificates on a customer's change
control routinely need 30.

Full lifecycle — expiry calendars, dormancy, the service-account ownership audit, scope drift, and
the certificate-validity schedule that removes hand-rotation as an option on a published date:
`credential-lifecycle.md`.

---

## 11. Rolling up to a severity band

**Severity is the worst band across the eight dimensions.** Not an average, and not a weighted
score. One Red dimension makes a connector Red, because each of the eight describes a different way
the customer's data can be wrong and they do not compensate for each other: perfect latency does not
offset 488 lost records.

`UNKNOWN` scores as Red for ranking (`BAND_SCORE` in `../scripts/integration_health.py`) and prints
as UNKNOWN in the table. That is deliberate and it is the conservative direction: an unmeasured
dimension on a connector feeding a contracted workflow is a reason to look, not a reason to relax.

Criticality, urgency and the remediation ranking that consumes this severity are in `../SKILL.md`
Step 5; the fix patterns are in `remediation.md`.

---

## 12. False positives worth knowing

Run these before escalating anything. An integration report that cries wolf twice is not read a
third time.

| Apparent finding | Innocent explanation | The check that separates them |
| --- | --- | --- |
| Freshness Red | Our own outage, or their planned maintenance window | Status page both sides; their change calendar |
| Throughput collapse | Their business is genuinely quieter — end of a project, a seasonal trough, a team on leave | Compare against the same weekday last year and against their own headcount or activity in other connectors |
| Throughput spike | An announced backfill or historical import | Change log both sides; check whether IDs are new or re-sent |
| API call decline | Customer efficiency work — batching, caching, polling replaced by webhooks — which reduces calls while increasing value | Check `distinct_endpoints` and `records_processed`, not request count (signal `T1` trap) |
| Validation errors | A one-off bad import on their side, already corrected | Is the error rate falling on its own? Cluster the rejections by cause |
| Auth error | A credential rotation done properly, mid-window | Did a successful auth follow within the rotation window? |
| Schema drift | A sandbox or test environment sampled instead of production | Confirm the tenant ID in the sample |
| Integration disconnected | An IdP, cloud or region migration unrelated to us | Ask. One email. Then record the answer — and note that a customer who does not answer, and does not ask you to fix it, is the `T2` finding, not the disconnect |
