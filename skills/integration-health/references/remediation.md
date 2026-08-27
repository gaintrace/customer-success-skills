# Remediation and the Deprecation Runway

> Steps 6 and 7 in full: the fix that works per error class and per silent-failure code, how effort
> is banded and where a fix stops being a fix and becomes a scoped build, the backfill decision, the
> detector that has to survive the fix, and how a cutover gets a date the customer's change process
> will actually honour.
>
> Evidence labels: `[M]` measured · `[V]` vendor-published · `[P]` practitioner convention ·
> `[A]` standard or peer-reviewed · `[D]` primary product documentation, with the fetch date.

**Contents**

[1 The remediation row](#1-the-remediation-row) · [2 Effort banding](#2-effort-banding-and-the-line-where-a-fix-becomes-a-build) · [3 Fix patterns by error class](#3-fix-patterns-by-error-class) · [4 Fix patterns by silent-failure code](#4-fix-patterns-by-silent-failure-code) · [5 The backfill decision](#5-the-backfill-decision) · [6 Retry, idempotency and the dead-letter path](#6-retry-idempotency-and-the-dead-letter-path) · [7 The detector spec](#7-the-detector-spec) · [8 Cutover, rehearsal and rollback](#8-cutover-rehearsal-and-rollback) · [9 The deprecation runway](#9-the-deprecation-runway) · [10 Negotiating the change window](#10-negotiating-the-change-window) · [11 Sequencing and deferral](#11-sequencing-and-deferral) · [12 Traps](#12-traps) · [13 Finished when](#13-finished-when)

---

## 1. The remediation row

A remediation is not a sentence describing an intention. It is a row, and a row missing any of
these columns is not ready to be worked.

| Column | Rule |
| --- | --- |
| `connector` · `severity` | From Step 2. Severity is the worst of the eight dimensions, never an average |
| `customer_impact` | In **their** units — records, reports, hours, invoices. "Validation errors at 0.6%" is not an impact; "412 opportunities missing from your pipeline report for seventeen days" is |
| `fix` | The specific change, not the category. "Add a unique constraint on `external_id` at the destination", not "improve data quality" |
| `effort_band` | §2 — one of ≤2h · ≤1d · ≤1w · >1w |
| `elapsed_days` | Calendar wait for their people and change windows. Tracked **separately** from effort, because it is what actually sets the date |
| `owner` + side | A named person, on the correct side. Not a team |
| `by_date` + `agreed_by` | No date enters the plan without its named owner having agreed it (`R19`) |
| `expected_effect` | A number with a direction: "unaccounted records per run 24 → 0" |
| `success_measure` | How we will know in a week, observable without asking anyone |
| `detector_left_behind` | §7. A remediation with no detector is a repeat incident with a date on it |
| `deferred_reason` + `revisit_date` | For everything cut from this cycle (`R14`) |

---

## 2. Effort banding, and the line where a fix becomes a build

**Effort is the named owner's hands-on hours**, including rehearsal, verification and building the
detector. **Elapsed is the wait** — their admin's diary, a change window, a security review. The
two are recorded separately, and a plan that confuses them promises Tuesday for work that cannot
start until the following month.

| Band | Meaning | Includes | Where it goes |
| --- | --- | --- | --- |
| **≤2h** | Do it now, in this sweep | Config change, credential rotation with overlap, a threshold, adding a detector | Done before the report is sent, and reported as done |
| **≤1 day** | This week | A permission fix, a schema contract test, a pagination fix, a backfill of a bounded window | The ranked list, top |
| **≤1 week** | This cycle, one at a time (`R17`) | Receiver rework for durable acks, an upsert re-key, a connector version upgrade | The ranked list, cut at the capacity line |
| **>1 week** | **Leaves this report** | A new connector, a re-architecture, anything needing a product change | `fde-scoping` — SOW, acceptance criteria, change control. Say so explicitly rather than carrying a fantasy estimate |

**Cut the list to workable hours, not to the number of red connectors (`R13`).** Usable engineering
time is roughly 60% of nominal, so one engineer across a two-week cycle is `2 × 40 × 0.6 ≈ 48
hours`. Rank by `Impact × Severity × Urgency` (Step 5), walk down accumulating effort, and cut where
the cumulative crosses 48. Everything below the line gets a `deferred_reason` and a `revisit_date`
(`R14`) — and a line stating what is watched meanwhile, because a deferred connector still needs
its detector.

**The banding trap.** "The fix is twenty minutes" is usually the code change alone. The consumer
sweep, the verification run, the backfill and the detector are the other six hours, and they are
what makes the difference between a fix and the same incident in November.

---

## 3. Fix patterns by error class

Every class from Dimension 2 has one fix that works and at least one that looks like a fix and is
not. Retrying is the most common wrong answer: it helps exactly one of the six classes.

| Class | The fix | The wrong fix | Effort | Owner side | Detector left behind |
| --- | --- | --- | --- | --- | --- |
| **Auth** | Rotate or re-consent from a service account (`credential-lifecycle.md` §9), then assert scopes at every refresh | Retrying — it cannot succeed, and repeated failures trip lockout or rate limits | ≤2h ours, 14d elapsed | Theirs (admin) + ours | Any auth error >0, continuous |
| **Rate limit** | Read `Retry-After`, back off with full jitter (§6), persist the request so it is retried rather than dropped; then raise the quota or lower the call rate | Tighter retry loops, or more workers — both queue the client against itself | ≤1d | Ours | `429` rate >1% of calls, 7d · any record dropped rather than retried |
| **Validation** | Cluster the rejections by cause, fix the mapping or the source value, quarantine rather than discard, then backfill (§5) | Suppressing the error and letting the batch complete — this is how `S1` is born | ≤1d per cause | Ours + theirs (data) | Validation >0.1% of records; and every quarantined record counted |
| **Schema** | Pin a field contract, test it per run, then negotiate the change with a named owner their side | "Ignore unknown fields" — additive changes survive, removals and type narrowings do not | ≤1d contract, ≤1w mapping | Ours + theirs | Field set and types vs contract, per run |
| **Transient** | Idempotent retry with full jitter and a cap; a dead-letter path for anything past the cap | Infinite retry with no DLQ, which converts a transient failure into permanent loss when the queue drains | ≤1d | Ours | Sustained >5% over 7d; DLQ depth >0 |
| **Permanent** | Reconcile which target objects vanished, restore or re-map, and ask their side what changed | Deleting our record to match, before establishing whether the deletion was intended | ≤1d, elapsed by their answer | Theirs | Any `404`/`403` on a previously valid target |

**Auth errors are a relationship finding as well as a technical one.** A revoked scope or a deleted
integration user means someone their side changed access without telling us. The fix is the
rotation; the follow-up is the notification path, so the next change arrives as an email rather
than as an outage.

**Validation is where records die one at a time.** The batch completes, the job is green, and the
rejected records are real records that do not exist downstream. Always cluster: a single dominant
cause is a dated schema or picklist change and takes one fix; a scatter across many causes is data
quality their side and takes a conversation, not a patch.

---

## 4. Fix patterns by silent-failure code

Codes are defined in `silent-failures.md`. Backfill decisions are in §5.

| Code | The fix | Backfill? | Effort | Detector left behind |
| --- | --- | --- | --- | --- |
| `S1` partial batch drop | Fetch and persist per-record results every run; make the identity `submitted = succeeded + failed + unprocessed` a hard gate that fails the run | Yes — the failed and unprocessed sets are the list | ≤1d | Residual ≠ 0 on any run |
| `S2` coerced type | Widen the destination type, or make the transformation explicit and documented | Yes, for the affected range — values are wrong, not missing | ≤1d | Nightly checksums on money, quantity and identifier fields; `MAX(LENGTH)` vs column width |
| `S3` filtered records | Restore the permission or field on the integration user; pin the expected column set | Yes — re-extract the window | ≤2h + elapsed | Column-set assertion per run; **delta** in filtered counts, never the absolute |
| `S4` paused, not failed | Resume, and add the resume step to the maintenance runbook so a pause cannot outlive the maintenance | Yes — every missed window | ≤2h | `runs_observed ÷ runs_expected` over 24h, hourly |
| `S5` reduced scope | Re-consent with the full scope from a service account; pin `scopes_required` into config | Yes, if reads returned partial results | ≤2h + 14d elapsed | Scope-set assertion at every refresh + one canary read per scope |
| `S6` webhook 200-and-discard | Ack only after durable persistence: verify signature, dedupe on the provider's event ID, write raw to a durable queue, return `2xx`, then process asynchronously `[P]` | Yes, inside the provider's replay window (§5) | ≤1w | Emitted vs materialised event IDs, daily; any `4xx` we return |
| `S7` pagination truncated | Cursor pagination on an immutable key with an explicit termination condition; assert pages × page size ≥ the API's reported total | Yes — re-extract | ≤1d | Reported total vs rows written, per run |
| `S8` window shift | Store and query UTC; half-open intervals `[start, end)` so windows tile exactly | Yes — the gap windows | ≤1d | Window-tiling assertion: every record falls in exactly one processed window |
| `S9` upsert key collision | Unique constraint on the external ID at the destination so a collision errors instead of overwriting; then re-key | Yes — and re-extract the overwritten records, which are not recoverable from the destination | ≤1w | Uniqueness assertion before every load, failing the run |

**Every one of these fixes changes what the run does on failure.** That is the point: the silent
class becomes loud. Expect the first week after a fix to surface errors that were always there, and
say so in advance to whoever watches the alerts — an unannounced increase in alarms reads as the
fix having broken something.

---

## 5. The backfill decision

Five questions, in order. A "no" at any point changes the plan rather than stopping it.

| # | Question | If no |
| --- | --- | --- |
| 1 | Are the records still available at source for that window? | The loss is permanent. Say so, with the count and window, and move to disclosure (Step 8) |
| 2 | Is the write idempotent, or is there a unique key to upsert on? | Fix `S9` first. A backfill onto a non-unique key creates duplicates on top of losses |
| 3 | Will downstream aggregates double-count a replay? | Backfill into a quarantine table, reconcile, then promote in one transaction |
| 4 | Does the replay trigger side effects — notifications, invoices, payments, webhooks out? | Replay with side effects disabled, or reconstruct state directly. Never re-fire customer-visible events for a data fix |
| 5 | Is the provider's replay window still open? | Re-query the source API by ID range instead of replaying delivery |

**Replay windows are provider-set and short.** One payments provider retries a failed delivery for
up to three days with exponential backoff in live mode, and allows a manual resend for 15 days from
the Dashboard or 30 days via CLI `[D · Stripe webhooks documentation, fetched 2026-08-28]`. One
commerce platform retries up to 8 times over 4 hours and removes the subscription after repeated
failures in a 24-hour period, after which nothing is queued at all
`[D · Shopify developer documentation, "Troubleshooting webhooks", fetched 2026-08-28]`. **Establish
the window before planning the backfill**, because past it the only path is a re-query of the source
API — a different job, with a different effort band.

**The backfill procedure.** Bound the window in UTC and state it · extract by ID, not by count ·
load into quarantine · reconcile at L3 (entity level) against the source · promote · re-run the
reconciliation and record the residual · state the verified count in the disclosure. Any backfill
above 100,000 records or crossing a billing boundary is banded ≤1w and needs a named approver on
both sides.

---

## 6. Retry, idempotency and the dead-letter path

**Retry only the two classes that self-heal.** Auth, validation, schema and permanent errors are
permanent by definition; retrying them consumes rate limit and delays the human who has to act.

**Full jitter, not fixed backoff.** Synchronised clients retrying on the same schedule re-converge
and produce a second load spike; randomising the whole interval spreads them
`[P · AWS Architecture Blog, "Exponential Backoff And Jitter"]`, and AWS SDK standard retry mode
implements exponential backoff with jitter by default `[D · AWS SDKs and Tools reference guide,
fetched 2026-08-28]`.

```
sleep = random_between(0, min(cap, base × 2 ** attempt))     # full jitter
respect Retry-After where the provider sends it — it overrides the formula
attempts ≤ 5, cap ≤ 60s, then dead-letter                    # library default [P]
```

**Idempotency is what makes retry safe.** Send a client-generated key on every mutating request and
have the receiver return the first result for a repeat. One payments provider treats a request as an
idempotent replay for **24 hours** on the same key, accepts keys up to 255 characters and recommends
v4 UUIDs `[D · Stripe API reference, "Idempotent requests", fetched 2026-08-28]`. Beyond that window
a reused key is a new request — so a backfill run 48 hours later duplicates unless the destination
has its own unique constraint (`S9`).

**A dead-letter path is not a log line.** It stores the full payload, the error, the attempt count
and the timestamp; it has a replay command; it has a named owner; and its depth is alarmed above
zero. A DLQ nobody drains is a queue where records go to be forgotten with a stack trace attached.

---

## 7. The detector spec

Every remediation ships its monitor. Specify it as a row, not as a sentence.

| Field | Example |
| --- | --- |
| `detector_id` | `sfdc-opps-recon` |
| Watches | `records_expected_24h − records_succeeded_24h` per run |
| Threshold | Any unaccounted record — an absolute, not a percentage |
| Window | Per run |
| Fires to | Jo Nkemdirim (ours, connector owner); after 2 misses, the data owner |
| Cadence | Continuous |
| Catches | `S1`, `S3`, `S6`; Dimension 5 |
| False-positive budget | ≤1 per month. Above that, the threshold is wrong and the detector will be muted by a human within a fortnight |
| `added_on` · reviewed | 2026-08-28 · at each monthly sweep |

**Three rules that decide whether a detector survives contact with an on-call rota.** Alert on the
**delta** where a steady state exists — a filter that has always removed 200 rows a day hides the
day it removes 900. Alert on **absence** as well as failure — schedule adherence is the only
detector that sees a job which never started (`S4`). And **route to a named person on the correct
side**, because a credential expiry that pages our engineer at 03:00 still needs their admin at 09:00.

---

## 8. Cutover, rehearsal and rollback

Any fix above the ≤1d band gets these five, written before the window is booked.

| Element | The standard |
| --- | --- |
| **Rehearsal** | In a sandbox or staging tenant, with the elapsed time measured. A rollback time is a measured number or it is a hope |
| **Dual-run** | Old and new paths write in parallel for one full business cycle, reconciled at L3. This is the only way to prove a migration lost nothing |
| **Kill switch** | A config flag that reverts without a deploy. If reverting needs a release, the rollback time is the release time |
| **Rollback criteria** | Stated in advance as numbers: "residual >0 on any run, or p95 above budget for 30 minutes, or any auth error → roll back". Deciding in the window is deciding under pressure |
| **Verification window** | One full cycle of the slowest job the change touches — including the weekly and monthly ones. A cutover verified over a weekday misses the Sunday reconciliation |

**Verify against their numbers, not ours.** A migration is complete when the customer's own count
matches, for a window they chose. Anything else is our system agreeing with itself.

---

## 9. The deprecation runway

**Read deprecation off the wire.** `RFC 9745` defines the `Deprecation` response header (Standards
Track, March 2025) along with a `deprecation` link relation pointing at the migration documentation,
and `RFC 8594` defines `Sunset` (Informational, May 2019) `[A]`. Log both on every response and
alert weekly on any new value; a client logging neither learns about the retirement from a `410`.

**Record the vendor's own policy beside the date — the runway differs by an order of magnitude.**

| Vendor policy | Notice | What it means for the plan |
| --- | --- | --- |
| Microsoft Graph | A version or GA API is declared deprecated **at least 24 months** before removal `[D · Microsoft Learn, "Versioning, support, and breaking change policies for Microsoft Graph", fetched 2026-08-28]` | Two renewal cycles of runway. Plan it, do not rush it |
| Google APIs | Google states it will strive to give **one year** of notice before breaking changes on covered APIs `[D · Google Developers Blog, deprecation policy]` | One cycle. It fits inside a normal roadmap only if detected on the announcement |
| Stripe | Date-based versioning: monthly releases are backward-compatible, breaking changes land in twice-yearly named releases, and there are no forced migrations `[D · docs.stripe.com/sdks/versioning, fetched 2026-08-28]` | No cliff, but drift accumulates until a needed feature is unreachable from the pinned version |
| Salesforce | Hard retirement with a date — versions 21.0–30.0 now fail `410 GONE` (REST), `500 UNSUPPORTED_API_VERSION` (SOAP), `400 InvalidVersion` (Bulk) `[D · Salesforce Help, fetched 2026-08-28]` | A dated cliff. Everything is measured back from it |
| Small vendor or customer-built middleware | Usually none published | `UNKNOWN — requires the vendor's versioning policy in writing`. This is a procurement question, not an engineering one |

**The runway arithmetic.** The customer's exposure clock is set by the **strictest** vendor in their
stack, so compute per connector and take the minimum.

```
opt_out_deadline   = renewal_date − notice_period_days                                  (R1)
migration_deadline = sunset_date − verification_window_days − rollback_buffer_days
start_by           = migration_deadline − effort_days − elapsed_days − change_wait_days
paper_starts       = opt_out_deadline − 90 days      # security review, new scopes, MSA (R7)
```

**The scheduling rule, and it is a hard one: never cut over inside the notice window.** A migration
in the fortnight the customer is forming a renewal view is a self-inflicted risk event on the worst
possible date. Land it **at least 30 days before the opt-out deadline**, or after signature — and if
the sunset falls inside the window, that is the finding, escalated the same week.

```
Worked example — Northwind Logistics
renewal 2027-02-05 · notice 90d  → opt_out_deadline           2026-11-07
Salesforce v52.0 sunset                                        2027-06-30   (after opt-out)
Decision: cut over ≥30 days before opt-out, or after signature
Chosen:   cutover window 2026-10-01, effort ≤1w, elapsed 21d → start_by     2026-09-10
Rejected: January 2027 — inside the notice window, and inside their year-end freeze
```

---

## 10. Negotiating the change window

A date is not a date until the named owner on the correct side has agreed it (`R19`). Three rules
make that agreement likely rather than hopeful.

**Offer windows, do not request one.** Three specific slots, all outside their freeze periods, all
of which work our end. A request for "a window in October" comes back in three weeks as a question.

**Know their freeze calendar before asking**, and record it in `cs-context` so nobody asks twice.

| Freeze | Typical shape | The consequence of ignoring it |
| --- | --- | --- |
| Month-end and quarter-end close | Last 3 working days plus the first 2 | The finance team's own reporting depends on the connector you are changing |
| Their peak trading period | Retail Q4, tax season, term start, renewals season | Change control will refuse, correctly |
| Year-end / audit | Weeks around their fiscal year-end | Auditors need reproducible data; a schema change mid-audit is a finding on their side |
| Release or code freeze | Published internally, rarely shared | Ask for the calendar once, annually |

**State what is unavailable, for how long, and who is needed** — never that some downtime may be
required. Then send the ask itself, written to `../../cs-context/references/customer-voice.md`.

════════════════════════════════════════════════════════════
CUSTOMER-FACING — copy the block below and send as written.
Everything above this line is internal. Do not forward it.
════════════════════════════════════════════════════════════

```text
Subject: Booking the opportunity sync upgrade — 90 minutes, three dates

Hi Marcus,

The Salesforce API version the sync uses retires on 30 June. I'd like the
upgrade done in October rather than next spring, so it's well clear of your
year-end and there's room to roll back without anyone rushing.

What it involves:

  • Ninety minutes. The sync pauses and queues, so nothing is lost — the
    pipeline dashboard shows last night's numbers until it finishes.
  • From you: nothing on the night. I need twenty minutes with a Salesforce
    admin the week before to confirm the new permission set.
  • From me: a rehearsal in your sandbox the week before, then both the old
    and the new path writing in parallel for a week afterwards so we can
    compare record counts against your own before switching the old one off.
  • If it goes wrong, we revert with a config flag in about ten minutes.
    That's a number I've measured in the sandbox, not an estimate.

Three windows that work my end, all clear of your month-end:

  Thursday 1 October, 19:00
  Thursday 8 October, 19:00
  Thursday 15 October, 19:00

Which one? If your change process needs a form from me, send it over and
I'll fill it in rather than adding it to your list.

Jo
```

---

## 11. Sequencing and deferral

**One primary workstream per account (`R17`).** Three half-executed remediations produce three
half-fixed connectors and a customer who experiences a vendor in disarray.

**The order of operations, which is not the priority order.** Priority decides *which connector*;
this decides *what happens first on it*:

1. **Stop the loss** — pause the job, disable the bad rule, quarantine rather than discard. A
   connector that is dropping records is better stopped than left running while a fix is written.
2. **Restore the flow** — the smallest change that gets correct records moving again.
3. **Backfill** (§5), verified against their counts.
4. **Leave the detector** (§7). Before the ticket closes, not after.
5. **Fix the structure** — the contract test, the unique constraint, the ownership change. This is
   the step that gets skipped, and skipping it is why the same incident returns with a new date.

**Deferral is a decision and it is written down (`R14`, `C32`).** Every connector cut from the cycle
carries: why not, what is watched meanwhile, the revisit date, and what changes if it is still
deferred at the next sweep. "Not enough hours" is a legitimate reason; an empty row is not.

---

## 12. Traps

| Trap | Correction |
| --- | --- |
| Ranking the fix list by error volume | Rank by `Impact × Severity × Urgency` (Step 5). The noisy connector feeding a report nobody opens loses to the quiet one behind a contracted workflow |
| Closing the fix when the errors stop | The errors stopping is not the records arriving. Close on a clean reconciliation over a full cycle, not on a clean error log |
| A fix with no detector | The same failure returns silently with a new date. The detector is part of the fix, not follow-up work |
| Backfilling before fixing the key | Duplicates on top of losses, and now the aggregates are wrong in two directions |
| Retrying a validation or schema error | It cannot succeed. Quarantine, cluster, fix the cause, then replay the quarantine |
| An effort estimate that is the code change only | Add the consumer sweep, the verification run, the backfill and the detector — usually 3–4× the code time |
| A cutover date inside the notice window | Land it ≥30 days before the opt-out deadline or after signature (§9) |
| A date agreed with "their team" | `R19` — a named person, on the correct side, who has said yes |
| Announcing our deprecation instead of planning it | Notice given, migration guide, named owner each side, a window inside their freeze calendar, dated against the opt-out deadline (`R1`, `R7`) |
| Telling the customer the detector exists because they missed the failure | The detector is stated as what we now do. Who noticed is internal, permanently (`R18`) |

---

## 13. Finished when

- [ ] Every remediation row carries action · owner and side · agreed date · effort band · elapsed · expected effect · success measure · detector
- [ ] Effort and elapsed are separate numbers, and anything >1 week is handed to `fde-scoping` rather than estimated optimistically
- [ ] The list is cut to workable hours (`R13`), and everything below the line has a reason and a revisit date (`R14`)
- [ ] Each fix names the class or S-code it addresses, and no permanent-error class is being retried
- [ ] The backfill decision ran all five questions, the replay window was established before planning, and the verified count is stated
- [ ] Every fixed connector leaves a detector with a threshold, a named recipient on the correct side, a cadence and a false-positive budget
- [ ] Any change above ≤1d has a rehearsal, a dual-run, a kill switch, numeric rollback criteria and a verification window covering the slowest job it touches
- [ ] Deprecation is recorded per connector with the vendor's own policy, dated against `renewal_date − notice_period_days`, and no cutover lands inside the notice window
- [ ] The change-window ask offers three dated slots outside their freeze calendar, states what is unavailable and for how long, and carries no internal language (`R18`)
