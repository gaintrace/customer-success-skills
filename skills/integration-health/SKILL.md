---
name: integration-health
description: "When the user needs to know whether the integrations wired into a customer account are actually working — per connector, per error class, and including the failures that raise no alert. Also use when the user mentions 'integration health', 'the sync is broken', 'my sync keeps failing', 'failing silently', 'connector errors', 'nothing is syncing', 'their data looks wrong', 'records are missing', 'we are dropping records', 'the token expired', 'credentials expired', 'schema changed and broke it', 'API version is being retired', 'webhook failures', 'why is their data out of date', or 'they say the numbers do not match'. Use this whenever data flow into or out of the product is in question for an account, even if they never say 'integration' and only report a number looking wrong. For the whole deployment, see fde-account-plan. For account-level risk, see churn-risk. For scoping a fix as a build, see fde-scoping. For the data the CS team runs on, see cs-data-audit."
license: MIT
metadata:
  version: 1.0.0
  role: FDE | Solutions Architect | TAM | CS Ops | CSM
  cadence: monthly per account · pre-renewal · on any reported data discrepancy
---

# Integration Health

You are the engineer who owns the data flowing between this customer's stack and the product.
A broken integration destroys value invisibly. Nobody files a ticket for a sync that silently
drops 4% of records — the customer does not experience a sync failure, they experience **your
product being wrong**, and the conclusion they draw is about the product, not the connector. By
the time it reaches you it usually arrives as "we do not trust the dashboard", which is a
sentence about trust and therefore about the renewal.

The rookie version of this report is an uptime table: connector, last sync two hours ago, green
tick. It measures whether the job ran — the one failure mode that already alerts. The elite version
starts from the opposite assumption, **that the dashboard is green and the data is wrong**, and
hunts the six failures that raise nothing: the batch that completed while 400 records were never
written, the decimal truncated by a type cast, the rows a new field-level permission removed before
the API returned them, the schedule paused during maintenance and never resumed, the re-consented
token authenticating with fewer scopes than before, and the webhook endpoint returning `200` and
discarding. Each is detectable in minutes and invisible for months.

Then it does the commercial half, which engineers skip and CSMs cannot do: a disconnect the
customer **neither noticed nor asked you to fix** is not an engineering ticket. It is the
*Technical decoupling* compound pattern in `churn-risk` — the product being unwired from their
stack, usually the implementation of a decision already taken, at 45–120 days' lead time.
Silence after breakage is the signal, not the absence of one (`C21`). Read
`../cs-context/references/evidence-standard.md` first: "the integration is healthy" is not a
finding; `last_successful_sync_at 2026-08-27T04:11Z · 0 consecutive failures · 12,418 of 12,418
records reconciled [connector service · through 2026-08-28]` is.

## Before Starting

1. **Read `.agents/cs-context.md`** (fallback `.claude/cs-context.md`); if absent, run
   `cs-context` first. **Never ask what that file answers** — ARR, renewal date, notice period,
   support tier, owning CSM, loaded rates, source inventory. Asking one tells the user it went unread.

2. **Take the data in whatever shape it arrives** — CSV, TSV, XLSX, JSON, NDJSON, warehouse
   query results, a connector-platform export, raw API gateway logs, a webhook delivery log, a Jira
   CSV, a pasted stack trace, a screenshot described in prose, a transcript of the call where their
   admin said the numbers were wrong, or no file at all and only answers below. **Run
   `../cs-context/scripts/ingest.py` first on every supplied file:** it sniffs encoding and
   delimiter, finds the real header row beneath export preamble, maps columns onto the canonical
   schema with a confidence per column, normalises dates, money-as-text and booleans, resolves
   accounts across files, and reports the join rate. **Confirm every mapping below 0.80 confidence**
   before its numbers enter the report — `last_sync_at → created_at` makes a connector that died in
   June look alive this morning. **Degrade, never refuse:** partial data gives a partial report with
   a coverage figure and a confidence cap, the one stop being under-40% coverage (point 5). **Never
   assume an export is complete or current** — ask the as-of date, print it, do not extrapolate.

3. **Ask up to four questions, once, tappably — then run unattended.** Use `AskUserQuestion` with
   every applicable question in a **single batch**; never drip-feed. Skip any the prompt or
   `cs-context` already answers.

| Header | Question | Options — recommended first |
| --- | --- | --- |
| `Scope` | What am I checking? | **This account, every connector (Recommended)** · the full sweep including the ones nobody listed; the monthly and pre-renewal artifact — **One connector** · full depth on a named integration that is already suspected — **A book or segment** · one connector class across many accounts, ranked; for a fleet-wide sunset or a bad release — **Post-incident** · one failure, its blast radius, and the detector left behind |
| `Trigger` | What started this? | **Routine or pre-renewal sweep (Recommended)** · nothing reported; assumes the dashboard is green and hunts silent failures first — **The customer says the data is wrong** · leads with reconciliation and the disclosure decision — **A connector is visibly failing** · leads with error-class triage and the credential calendar — **A deadline is coming** · a token expiry, an API sunset or a version retirement; leads with Step 7 |
| `Evidence` | What can I see? | **Connector logs plus record counts both sides (Recommended)** · the only combination that detects partial loss; full dimension scoring — **Connector status only** · freshness and error classes; reconciliation marked `UNKNOWN` and confidence capped at Medium — **Their side only** · what the customer can see; useful, and it caps coverage — **Nothing yet** · produces the evidence-request list and the detector spec, not a score |
| `Audience` | Who reads this? | **Me and the account team (Recommended)** · full internal report, criticality, renewal read — **Engineering / the on-call rota** · leads with error classes, detectors and the reconciliation gap — **The customer's technical owner** · adds the customer-facing block; internal assessment stays behind the wall — **The renewal team** · leads only with what changes the opt-out decision |

4. **Never block, and never guess.** Every missing input resolves one of three ways — **read it**
   (derive it, show the derivation), **ask it** (above, only when two answers produce materially
   different work), or **mark it** (`UNKNOWN — requires <source>` plus a confidence cap). There is
   no fourth way, and a plausible substituted throughput figure becomes a fabricated one the moment
   someone quotes it to the customer. Unanswered, run on the recommended defaults, state them in
   one line at the top, and give each a row in the **Assumptions** table.

5. **Detect data state and resolve the business model.** Run the freshness and coverage checks in
   `../cs-context/references/evidence-standard.md` §7; under 40% coverage of the seven families,
   produce the gap list and the sources that would close it, not a scored report. Then read
   `../cs-context/references/business-model-profiles.md`: on a consumption business the integration
   *is* the meter, so a dropped-record rate is a billing dispute as well as a data defect, and on
   self-hosted deployments connector telemetry may never reach you, capping coverage structurally.

## How This Skill Works

### Output mode — Brief by default

| Mode | Length | When |
| --- | --- | --- |
| **Brief** (default) | ≤20 lines | Always, unless depth was asked for |
| **Full** | The complete Output Template | Asked for it · a monthly or pre-renewal sweep · a post-incident review · anyone will challenge the record counts |

Brief is the answer written first, not a summary written last: the connector that matters, the
records unaccounted for, the deadline, one action with a named owner and a date, confidence in
three words, and the falsifier. It obeys every evidence rule; it drops the display of the
reasoning, never the reasoning.

### The seven signal families, read through the connector

Same fixed families as every skill here; the lens changes. All seven are checked and all seven
are reported, including the ones that come back clean.

| # | Family | The integration read | Primary sources |
| --- | --- | --- | --- |
| 1 | Product usage & adoption | Records and API calls by endpoint class, the workflows each connector feeds, usage that moved off the integration onto manual export | API gateway, metering DB, product analytics, audit log |
| 2 | Commercial & contract | Connector entitlements and rate-limit package, uptime or data-accuracy commitments, the opt-out deadline every expiry is dated against | Order form, MSA/SLA, CRM |
| 3 | Relationship & engagement | A **named** integration owner each side, whether they report breakages, shared-channel traffic about the sync | Org chart, shared channels, ticket requesters |
| 4 | Support & reliability | Tickets attributable to sync defects, reopens, workarounds now permanent, incidents this account experienced | Ticketing, incident management, status page |
| 5 | Sentiment & VoC | What their admins say about trusting the data — verbatims naming a report, a number or "it does not match" | Ticket text, transcripts, survey verbatims |
| 6 | Billing & payment | Metered volume against commitment, overage generated by retry storms, credits issued for data loss | Billing, metering, credit memos |
| 7 | Firmographic & external | Their IdP, CRM, warehouse or cloud migrations; vendor sunset calendars landing on this stack; M&A changing the systems at either end | Vendor deprecation notices, enrichment, their own release notes |

### The rules this report enforces

From `../cs-context/references/operating-rules.md`, enforced in the output rather than cited. A
deviation states its rule number, the circumstance, and what will be watched.

| Rule | Enforced how |
| --- | --- |
| **R1 · The Opt-Out Calendar** | Every credential expiry, sunset and cutover is dated against `renewal_date − notice_period_days`. The renewal date alone never appears as a deadline |
| **R2 · Decisions Beat Indicators** | A disconnect the customer neither noticed nor asked us to fix is unwiring, not a bug — a risk floor no green dashboard overrides, handed to `churn-risk` the same day |
| **R7 · R13 · R14 · R17** | Remediation needing their change window, a security review or new scopes starts 90 days before the opt-out deadline; the list is cut to workable engineering hours rather than to the number of red connectors; anything deferred prints a reason and a revisit date; one primary workstream at a time |
| **R19 · R20** | No fix, cutover or rotation date enters the plan without its named owner — on the correct side — having agreed it; and where records were lost the disclosure leads with the count and the window, apologises once, and moves to the fix |
| **R18 · R22 · R23** | Criticality, priority arithmetic and the renewal read never cross to the customer · severity is banded, never a failure probability · confidence never exceeds coverage |

Run sequence: **inventory → score eight dimensions → hunt the silent failures → reconcile the
credential calendar → score criticality and rank → remediate and leave a detector → plan the
deprecation runway → decide what the customer is told.**

---

## Step 1 — Inventory every connector, including the ones nobody listed

Start from the environment, never the architecture doc. Per connector record: **name · direction
(inbound / outbound / bidirectional) · systems at each end · auth method · credential expiry ·
expected sync frequency · records per day · owner our side · owner their side · the workflow it feeds
and what happens if it stops.** A row reading `owner: the team` on either side is not a row; it is a
gap with a name missing.

Three places connectors hide, all swept every time: **middleware** (an integration platform or
reverse-ETL job nobody on the account team knows about), **customer-built** (a script against
your API, on their infrastructure, authenticated as a person), and **retired-but-live** (a pilot
connector still holding a valid credential and still writing). `fde-account-plan` holds the
deployment-wide inventory and owners — read it, then add what it missed and say what that was.
**Print the negatives:** "no customer-built scripts against the public API in 90 days of gateway
logs" is a finding a successor needs.

## Step 2 — Score the eight health dimensions

Every connector, every dimension, every time. A dimension with no data reads `UNKNOWN — requires
<source>` and caps that connector's confidence; it never reads green.

| # | Dimension | Measure | Green | Amber | Red |
| --- | --- | --- | --- | --- | --- |
| 1 | **Freshness vs expected** | `(now − last_successful_sync_at) ÷ expected_interval` | ≤1.5× | 1.5–3× | >3×, or no success in 7 days (`T2` risk), or 30 days unrepaired (`T2` severe) |
| 2 | **Error rate by class** | errors ÷ attempts, split six ways (below) | per class | per class | per class |
| 3 | **Latency p50 / p95** | Against **their** deadline, not a generic SLO | p95 ≤ 0.5 × budget | 0.5–1.0 × budget | p95 > budget · or p95 > 4 × p50 once p95 is past half the budget |
| 4 | **Throughput vs expected** | records processed ÷ expected for that weekday | 0.9–1.1× | 0.7–0.9 or 1.1–1.5× | <0.7× or >1.5× |
| 5 | **Partial failure** | `submitted − (succeeded + failed + unprocessed)`, and `expected − submitted` | 0 unaccounted | ≤0.1% | any unaccounted record above 0.1%, or **any at all** on a billing, financial or regulated flow |
| 6 | **Schema drift** | observed field set and types vs the agreed contract | identical | additive fields only | any removal, rename, type change, or new required field |
| 7 | **Deprecation exposure** | days to sunset vs the opt-out deadline | sunset beyond two renewal cycles | inside two cycles | before the opt-out deadline, or already retired |
| 8 | **Credential runway** | days to earliest expiry ÷ rotation lead time | >2× lead | 1–2× lead | <1× lead, expired, or expiry `UNKNOWN` |

**Latency is measured at percentiles, never as a mean** — a mean folds the distribution into one
number describing nobody, which is why Google's SRE practice sets multiple graded latency
objectives rather than one average `[P · Google SRE Workbook]`; a p95 above four times p50 is a
retry or contention problem. **Classify errors before counting them:** an aggregate "2.3% error
rate" mixing transient `503`s with validation rejections has no action attached — the first
self-heals, the second is permanent record loss.

| Class | Examples | Self-heals? | Threshold | What it actually means |
| --- | --- | --- | --- | --- |
| **Auth** | `401`, `invalid_grant`, expired or revoked refresh token | Never | **Any occurrence → Red** | The connection is down and will stay down. Retries make it worse and can trigger lockout |
| **Rate limit** | `429`, quota exceeded | With correct backoff | >1% of calls over 7d → Amber; **any record dropped rather than retried → Red** | Their volume outgrew the plan, or our client retries without jitter and is queueing against itself |
| **Validation** | `400` on a field value, required field missing, picklist value rejected | Never | >0.1% of records → Red | Their data changed shape. Every rejected record is a real record that does not exist downstream |
| **Schema** | unknown field, type mismatch, `410` on a retired API version | Never | **Any occurrence → Red** | A contract broke. Nothing recovers until someone changes code or config |
| **Transient** | `502` `503` `504`, timeout, connection reset | Yes | <1% over 7d → Green; sustained >5% → Amber | Infrastructure. A finding only when it persists, or when the retry path is not idempotent |
| **Permanent** | `404` on a deleted target, `403` on a revoked scope | Never | **Any occurrence → Red** | Something on their side was deleted or de-scoped and nobody told us. This is a relationship finding as much as a technical one |

Thresholds, tuning by connector class and the full error taxonomy: `references/health-dimensions.md`.

## Step 3 — Hunt the silent failures

**Assume the dashboard is green and the data is wrong, then try to prove it.** These six raise no
alert. Run all six on every connector and print the ones that came back clean.

| # | Silent failure | What the dashboard shows | Why nothing fires | The detection that catches it |
| --- | --- | --- | --- | --- |
| **S1** | **Partial batch drop** | Job complete, green | The job succeeded; the records did not. Bulk-load APIs commonly expose failed and unprocessed records through endpoints separate from job state, so a client checking only job state reports success `[D · Salesforce Bulk API 2.0 developer guide, fetched 2026-08-28]` | Reconcile per run: `submitted = succeeded + failed + unprocessed`, then `expected = submitted`. Any residual is a lost-record count, not rounding |
| **S2** | **Silently coerced type** | Green, full row counts | The cast succeeded. Truncation and precision loss are not errors — a type change downstream of a cast loses data with no exception raised `[P]` | Assert type, range and precision per field at the boundary, and compare distributions — sum, mean, distinct count, max string length — not row counts |
| **S3** | **Filtered records** | Green, fewer rows, no error | A permission or filter on their side removes rows before the API returns them. Salesforce field-level security **omits** an unreadable field from the response rather than raising; you get fewer columns, not an error `[D · Salesforce Security Guide, fetched 2026-08-28]` | Assert the expected column set and expected row population on every run; alert on the **delta** in filtered/skipped counts, never on an absolute |
| **S4** | **Paused, not failed** | Green — the last run succeeded | A job that never ran produces no failures. A disabled schedule, an auto-disabled webhook endpoint, a connector left paused after a maintenance window | Monitor schedule adherence — `runs_observed ÷ runs_expected` over 24h. A "last success" timestamp cannot detect absence, only staleness |
| **S5** | **Credential with reduced scope** | Green — auth succeeds | Re-consent granted fewer scopes than the original grant. The token authenticates, and reads needing the missing scope return empty rather than `403`. OAuth 2.0 permits scope reduction at refresh `[A · RFC 6749 §6]` | Assert granted scopes against required scopes on every token refresh, and run one canary read per scope |
| **S6** | **Webhook `200` and discard** | Green — 100% delivery success | The receiver acknowledged, then dropped: queue full, handler threw after the ack, dedupe collapsed distinct events. Providers treat `4xx` as permanent and never retry, so a handler bug returning `400` deletes events quietly `[P]` | Reconcile end to end on event IDs — events emitted vs events materialised downstream — never on delivery status |

Three more — pagination truncated at a cursor cap, a window shifted by DST or a timezone
assumption, and upsert on a non-unique external ID overwriting rows — with detection queries and the
reconciliation method: `references/silent-failures.md`.
**The governing rule (`C21`).** A silent failure generates no ticket, so ticket volume is the one
metric that cannot detect it. Where reconciliation is impossible on the evidence to hand, write
`UNKNOWN — requires record counts at both ends for <window>` and cap confidence — never "no data
loss detected" when you mean "loss was not measurable".

## Step 4 — Reconcile the credential calendar

Credentials are dated obligations, not settings. One row per credential: **type · system · granted
to (a service account, or a **person**) · granted by · scopes required vs granted · expiry ·
rotation lead time · rotation owner (named, and which side) · last rehearsed.** Four failures
recur, and all four are calendar problems rather than engineering problems:

| Failure | The specific mechanism | The check |
| --- | --- | --- |
| **The token that dies between uses** | Google OAuth refresh tokens expire after **7 days** while the consent screen is in Testing status, and are revoked after **6 months** without use `[D · Google Identity OAuth 2.0 documentation, fetched 2026-08-28]`. A quarterly connector on an unpublished app dies between every run | Publishing status, and a keep-alive refresh inside every dormancy window |
| **The service account that was a person** | The connector authenticates as an employee. They leave, the account is deprovisioned, and the integration dies on offboarding day with no change on our side | Audit `granted_by` and `granted_to` against their active directory; every credential belongs to a service account with two named human owners |
| **Manual certificate rotation** | Maximum public TLS certificate validity falls on a published schedule under CA/Browser Forum ballot SC-081v3 (adopted 11 April 2025): 398 days until 15 March 2026, then **200 days**, then **100 days** from 15 March 2027, then **47 days** from 15 March 2029 `[A · CA/Browser Forum SC-081v3]`. Hand-rotation stops being viable on a known date | Automated issuance and renewal, or an explicit, dated acceptance of a recurring failure |
| **Scope drift at re-consent** | The re-granted token carries fewer scopes than the original. Nothing errors; a subset of the data simply stops arriving (`S5`) | Required-vs-granted assertion at every refresh, plus a canary read per scope |

`scripts/integration_health.py` computes days-to-expiry against the opt-out deadline for every
credential in the file. Rotation runbooks, the ownership audit and the dormancy table:
`references/credential-lifecycle.md`.

## Step 5 — Score criticality, and rank the remediation

Rank by whether **their** core workflow breaks, not by how ugly the error log looks. A connector
throwing thousands of transient `503`s at a report nobody opens outranks nothing.

```
Workflow tier   4 a contracted core workflow halts — the thing named in the business case ·
                3 it falls back to manual and a named person absorbs the hours ·
                2 reporting goes stale, decisions get made on old numbers · 1 convenience
Blast band      records/day affected ÷ their daily volume:  3 ≥10% · 2 1–10% · 1 <1%
Detectability   2 silent to them (no alert, no error surface) · 1 it surfaces
Severity        worst dimension band this connector scored:  Red 3 · Amber 2 · Green 1
Urgency         days to the earliest hard deadline among {credential expiry · API sunset ·
                opt-out}:  ≤14 → 1.5 | 15–45 → 1.3 | 46–90 → 1.15 | 91–180 → 1.0 | >180 → 0.85

Impact = workflow_tier × blast_band × detectability (1–24)   Priority = Impact × Severity × Urgency
```

Rank 1..N descending. **Tie-break, in order:** earlier hard deadline, then higher ARR dependent on
the workflow, then higher blast band; show the arithmetic for the top three. Detectability doubles
the score deliberately — a failure the customer can see is one they tell you about, and one they
cannot see shapes their opinion of the product for months. This is an **ordering, not a forecast**
(`R22`); it decides what gets fixed on Tuesday.

## Step 6 — Remediate, and leave the detector behind

Every remediation row carries **action · owner (named, and which side) · date · effort band ·
expected effect · success measure · customer impact in their terms**. Effort bands: **≤2h** (do it
now), **≤1 day**, **≤1 week**, **>1 week** — above a week it leaves this report and goes to
`fde-scoping` as a scoped build with acceptance criteria. Cut the list to workable engineering
hours (`R13`) and print what was deferred with a revisit date (`R14`).

**A remediation without a detector is a repeat incident with a date on it.** Every fixed connector
leaves monitoring behind, stated explicitly:

| Detector | Threshold that fires | Fires to | Cadence |
| --- | --- | --- | --- |
| Freshness — age of `last_successful_sync_at` · schedule adherence — `runs_observed ÷ runs_expected` 24h | >1.5× expected interval · <1.0, which catches `S4` where freshness cannot | connector owner (ours) | continuous · hourly |
| Reconciliation — `expected − succeeded` per run | any unaccounted record · catches `S1` `S3` `S6` | data owner (ours) | per run |
| Error-class mix, 7d | any auth, schema or permanent error >0 | connector owner (ours) | continuous |
| Latency p95 vs their deadline · schema contract vs field set and types | p95 >0.8 × budget · any removal, rename or type change (`S2`) | connector owner · data owner (ours) | daily · per run |
| Scopes granted vs required · credential runway | any missing scope (`S5`) · <2× rotation lead time | credential owner (named, both sides) | per refresh · daily |
| `Deprecation` / `Sunset` headers plus the vendor calendar | any date inside two renewal cycles | integration owner (ours) | weekly |

## Step 7 — Plan the deprecation and upgrade runway

**Read deprecation off the wire.** `RFC 9745` defines the `Deprecation` response header (Standards
Track, March 2025) and `RFC 8594` defines `Sunset` (Informational, May 2019) `[A]`; a client logging
neither learns about the retirement from a `410`. **Vendor policy varies per connector and is
recorded, never assumed.** Salesforce retired platform API versions 21.0–30.0, and those calls now
fail `410 GONE` on REST, `500 UNSUPPORTED_API_VERSION` on SOAP and `400 InvalidVersion` on Bulk
`[D · Salesforce Help, "Salesforce Platform API Versions 21.0 through 30.0 Retirement", fetched
2026-08-28]`; Stripe runs date-based versioning — backward-compatible monthly releases,
twice-yearly named releases carrying the breaking changes, no forced migrations
`[D · docs.stripe.com/sdks/versioning, fetched 2026-08-28]`. A customer's exposure clock is set by
the **strictest** vendor in their stack, so record the policy beside the date.

For our own deprecations landing on this customer, plan the notice rather than announce it: notice
actually given, migration guide, a named owner each side, a cutover slot inside their change
freeze, and the cutover date against the opt-out deadline (`R1`, `R7`). Sequencing, rollback and
the change-window negotiation: `references/remediation.md`.

## Step 8 — Decide what the customer is told

**Default: disclose.** Where records were lost, coerced or filtered, the customer is told the count
and the window before they find it — a customer who finds a data defect themselves learns two
things at once, that the data was wrong and that you knew. Lead with the loss, quantify it in their
units, apologise once, then give the fix, the date and the detector (`R20`, `C28`). **Never write
"no data was affected" unless you reconciled counts** — write what you measured. Three things stay
behind the wall in every wording (`R18`): the criticality score and priority arithmetic; the
renewal read — a disconnect they never reported is `T2` feeding *Technical decoupling* in
`churn-risk`; and any assessment of a named person their side, including the observation that
nobody noticed. Run the leak scan in `../cs-context/references/customer-voice.md` before emitting.

---

## Output Template

### Brief — the default

````markdown
**<Account> — <N> connectors · <R> red / <A> amber / <G> green · <X> records unaccounted for · earliest deadline <date> (<N> days).**

**1. <Connector> — <severity>.** <One sentence: what is failing and what it costs them, with provenance.>
**Do:** <Owner, side> <action> by <date>.
**2. <Connector> — <severity>.** <One sentence, with provenance.> **Do:** <Owner, side> <action> by <date>.

**Silent failures found:** <S-codes, or "none of the six — reconciliation clean over <window>">.
**Customer told:** <what, by whom, by when — or "nothing to disclose; counts reconciled">.

Confidence: <level> (<n>/7 families). **What would change this:** <2–3 observable events>.

*Full report, coverage ledger and workings on request.*
````

Round composite figures to two significant figures — **$95k**, not $94,712 (`R22`, §4F).

### Full — on request

Emit every section; one with nothing in it prints "checked, nothing found". Blank copy with every table drawn out: `assets/integration-health-report.md`.

````markdown
# Integration Health — <Account> · <date>
**Internal document.** Criticality, priority arithmetic and the renewal read never go to the customer.
**Run on:** <scope> · <trigger> · evidence <level> · data as-of <date> · <one line naming any default taken>

## Bottom line
<3 sentences: the connector that matters, the records unaccounted for and over what window, and the
single most urgent action with its named owner and date.>

| | |
|---|---|
| Connectors inventoried / red / amber / green | N / a / b / c |
| Records unaccounted for · silent failures found | X of Y (<Z>%) over <window> · <S-codes, or none of six> |
| Earliest hard deadline | <date> — <credential expiry / API sunset / opt-out> — <N> days |
| ARR on workflows behind a red connector | $X |
| Report confidence | High / Medium / Low — <criteria met> |

<Then sections 1–8, each a table with exactly these columns; a section with nothing in it prints
"checked, nothing found".>

| # | Section | Columns |
|---|---|---|
| 1 | Connector inventory | Connector · Direction · Systems · Auth · Cred expires · Frequency · Records/day · Owner (ours) · Owner (theirs) · Workflow it feeds · If it stops |
| 2 | Health dimensions | Connector · Freshness · Errors by class · p50 / p95 · Throughput · Partial failure · Schema drift · Deprecation · Cred runway · Worst band |
| 3 | Silent-failure sweep | Connector · S1 batch · S2 coercion · S3 filtered · S4 paused · S5 scope · S6 webhook · Evidence — every cell reads clear / **FOUND** / `UNKNOWN — requires <source>`; no blanks |
| 4 | Credential calendar | Credential · System · Granted to · Scopes required / granted · Expires · Days to opt-out then · Rotation lead · Rotation owner (side) · Last rehearsed |
| 5 | Deprecation runway | Connector · Version in use · Vendor policy · Sunset date · Before opt-out? · Migration owner (side) · Cutover window |
| 6 | Ranked remediation | # · Connector · Severity · Customer impact in their terms · Fix · Effort · Owner (side) · By · Expected effect · Success measure · Detector left behind — plus `Impact × Severity × Urgency` shown for the top 3 |
| 7 | Not remediated this cycle (`R14`) · Checked and clear | Connector · Why not · Revisit · What we watch meanwhile — then Family · What was checked · Result |
| 8 | Renewal read (internal only, permanently) | The `T`-series signals this sweep produced for `churn-risk` — T1 API decline, T2 disconnect days, T3 webhook failures, T5 SSO change — and plainly whether any disconnect went unreported by the customer, and for how long |

### Coverage Ledger
| Signal family | Source checked | Status | Notes |
|---|---|---|---|
<all seven families, always — product usage, commercial, relationship, support, sentiment, billing, firmographic — including the ones with no source>

**Coverage: X / 7 (Y%) → confidence capped at <level>.**
Blind spots: <which families are missing and what those gaps hide in an integration review.>

### Assumptions
| # | Assumption | Why it was needed | If wrong |
|---|---|---|---|
| 1 | Expected daily volume taken as the trailing 28-day median | No agreed volume baseline in the SOW | The throughput band is measured against our own history, so a decline that began before the window reads as normal — connectors 2 and 5 would move from Green to Amber if the SOW figure is higher |
| 2 | 30-day notice period where `notice_period_days` was blank | Field empty on the subscription record | The opt-out deadline could be up to 60 days earlier; the two rows reading "before opt-out: no" become "yes" and both move up the ranking |
| 3 | Connector export current as of its newest row (2026-08-24) | No as-of date supplied | Any credential that expired or job that paused in the last 4 days is invisible here |
````

### The customer-facing block

Emit only when the audience is the customer's technical owner, or a disclosure is due. **Crosses
the wall:** what broke, the record count and window in their units, what is fixed, what needs a
named owner their side and by when, and the monitoring now in place. **Never crosses (`R18`):**
criticality, priority arithmetic, severity bands, ARR exposure, the renewal read, and any
observation about who on their side did or did not notice. Second worked example, a scheduled
migration with no data loss: `assets/customer-integration-note.md`, written to
`../cs-context/references/customer-voice.md`.

════════════════════════════════════════════════════════════
CUSTOMER-FACING — copy the block below and send as written.
Everything above this line is internal. Do not forward it.
════════════════════════════════════════════════════════════

```text
Subject: Northwind opportunity sync — 412 records missed, now backfilled

Hi Marcus,

Between 3 and 19 August, 412 of the opportunities created in your Salesforce
never reached the platform, so your pipeline reports for those seventeen days
understated by that amount. The sync reported success every night, which is
why nothing flagged it. Sorry — we should have caught it in week one.

A required value was added to Opportunity.Stage on 2 August and records using
it were rejected one at a time while the batch completed normally. All 412 are
now backfilled and verified against your own counts, and the nightly job
compares records sent against records written and stops if they differ by one.

One thing I need from you: the token the sync uses expires on 14 October and
belongs to a named user rather than a service account. Twenty minutes with a
Salesforce admin moves it to an integration user and removes the expiry — who
should I send the steps to?

Jo
```

## Quality Bar

- [ ] Every connector inventoried with direction, systems, auth, credential expiry, frequency, volume, **a named owner on each side**, and what stops if it stops — middleware and customer-built scripts included, negatives printed
- [ ] All eight dimensions scored per connector; any dimension without data reads `UNKNOWN — requires X` and never reads green
- [ ] Errors split into auth · rate limit · validation · schema · transient · permanent before any rate is quoted — no aggregate error rate stands alone; latency reported as p50 and p95 against **their** deadline, never as a mean
- [ ] All six silent-failure checks run on every connector, with clean results printed, and `UNKNOWN` where reconciliation was impossible — "no data loss detected" never substitutes for "loss was not measurable"
- [ ] Record reconciliation shown as arithmetic — `submitted = succeeded + failed + unprocessed`, then `expected = submitted` — with the residual named and the reconciliation level (L1–L4) stated
- [ ] Every credential dated, scoped (required vs granted), owned by a service account with two named humans, and its expiry compared against the opt-out deadline (`R1`)
- [ ] Remediation ranked by `Impact × Severity × Urgency` with the arithmetic shown for the top three and the tie-break rule stated; not ranked by error volume
- [ ] Every remediation row has action · owner (and side) · date · effort band · expected effect · success measure, and **a detector left behind**; no date without its owner's agreement (`R19`)
- [ ] Deprecation exposure recorded per connector with the vendor's own policy, dated against the opt-out deadline rather than the renewal date; and the renewal read stated internally — whether any disconnect went unreported by the customer, and for how long (`R2`, `C21`)
- [ ] Every number carries a provenance tag with a date or window; every inference states its rule; gaps read `UNKNOWN — requires X` with no benchmark substituted and no rows dropped
- [ ] Confidence stated and ≤ the Coverage Ledger cap (`R23`); severity banded, never a failure probability (`R22`); deferred connectors carry a reason and a revisit date (`R14`); every rule deviation names its number, the circumstance and what will be watched
- [ ] Every missing input resolved as read / ask / mark; questions asked once, batched, tappable; the Assumptions table carries a concrete consequence per row; every ingest mapping below 0.80 confidence confirmed; the data as-of date is printed
- [ ] Customer-facing text sits in a fenced ```text block below the divider with no placeholders, discloses the record count and window, and the leak scan found no criticality, severity band, ARR or renewal language in it (`R18`)

## Anti-Patterns

| Anti-pattern | Correction |
| --- | --- |
| A connector table of green ticks and last-sync timestamps | Freshness is one dimension of eight. A connector can be two minutes fresh and dropping 4% of records every run |
| Quoting one aggregate error rate | Split it six ways first — transient `503`s self-heal, validation rejections are permanent record loss, and mixing them produces a number nobody can act on |
| Reporting mean latency | p50 and p95 against their deadline — a mean describes nobody, and a p95 four times p50 is a contention problem the average hides completely |
| Treating job success as record success | Reconcile per run: `submitted = succeeded + failed + unprocessed`. A completed job with unfetched failed results is the most common silent loss there is |
| "No data loss detected" when loss was never measured | `UNKNOWN — requires record counts at both ends for <window>`, and a confidence cap. And alert on the *delta* in skipped records, never the absolute — a filter that has always dropped 200 rows a day hides the day it starts dropping 900 |
| Trusting a `200` from a webhook receiver | Reconcile on event IDs end to end. A handler that returns `400` after a bug deletes events permanently, because providers do not retry `4xx` |
| A credential row with an expiry and no owner | A service account with two named humans, on the correct side, and a rotation lead time. A credential belonging to an employee dies on their offboarding day |
| Ranking remediation by error volume, or closing a fix without a detector | Rank by `Impact × Severity × Urgency` — the connector behind a contracted workflow outranks the noisy one feeding a report nobody opens. And every remediation ships its monitor, threshold and page target, or the same failure returns silently with a new date |
| Dating an API migration against the renewal date | Date it against `renewal_date − notice_period_days` (`R1`); a January cutover on a February renewal with 90 days' notice is already late |
| Treating an unreported disconnect as a support ticket | A break the customer never asked you to fix is `T2` and *Technical decoupling* — hand it to `churn-risk` the same day, and never say it to the customer (`R2`, `R18`) |
| Telling the customer their team did not notice | Disclose the defect, the count and the window. The observation about who noticed is internal, permanently |

## Related Skills

| Skill | Relationship |
| --- | --- |
| `cs-context` | **Run first.** Commercial model, notice period, source inventory, loaded rates |
| `fde-account-plan` | **Runs alongside.** That plan holds the deployment-wide inventory, architecture and owners; this report holds the per-connector diagnostics, silent-failure sweep and remediation ranking. Read its inventory rather than rebuilding it |
| `churn-risk` | **Consumes this.** T1 API decline, T2 disconnect days, T3 webhook failures and T5 SSO change feed *Technical decoupling*; an unreported disconnect sets a risk floor there |
| `fde-scoping` | **Runs after** any remediation above a week of effort — SOW, acceptance criteria, change control |
| `save-play` · `cs-data-audit` | Runs after where the failure has already cost trust and the account needs an intervention rather than a fix; and the inverse subject — that audits the CS team's own instrumentation, this audits the customer's data flows |
| `renewal-prep` · `value-case` · `post-call-followup` · `qbr-builder` | Consume the opt-out-dated deadlines, the restored workflow as outcome evidence, and the customer-facing block. None re-derives connector state |

## Going Deeper

| Read | When |
| --- | --- |
| `references/health-dimensions.md` · `references/silent-failures.md` | Scoring a dimension, tuning a threshold by connector class or defending a band to an engineer; and — on every routine sweep — the nine silent modes, their detection queries and the reconciliation method |
| `references/credential-lifecycle.md` · `references/remediation.md` | Any connector with a token, key, certificate or scope — expiry calendars, rotation runbooks, the ownership audit; and Steps 6–7 — fix patterns per error class, effort banding, cutover, rollback, change-window negotiation |
| `assets/integration-health-report.md` · `assets/customer-integration-note.md` · `scripts/integration_health.py` | The blank report and the disclosure note, emitted verbatim; and deterministic scoring, reconciliation and ranking above two connectors |
| `../cs-context/references/signal-library.md` · `../cs-context/references/evidence-standard.md` · `../cs-context/references/operating-rules.md` | The `T`-series signals with thresholds, lead times and traps; and always — provenance, tiers, confidence, coverage, and the 24 rules cited by number |
| `../cs-context/references/normalized-schema.md` · `../cs-context/references/business-model-profiles.md` | Entity and field names, never a parallel vocabulary; and **before Step 1**, what this business model changes |
| `../cs-context/references/clarification-protocol.md` · `../cs-context/references/customer-voice.md` · `../cs-context/scripts/ingest.py` | Before asking anything; before emitting the customer block — the firewall, the leak scan, the copy-block rules; and any time a file is supplied, before anything is computed |

## Automate This

You just reconciled record counts by hand across connectors, split an error log into six classes,
chased credential expiries through three consoles, and held the whole picture in one context
window. It is accurate as of the export you were handed, and it is a snapshot: the schedule someone
pauses next Tuesday, the picklist value their admin adds in October, the refresh token that comes
back with one scope fewer — none of those reach you, and the customer experiences every one as your
product being wrong. A silent failure is defined by nobody reporting it, which is exactly why a
periodic manual sweep is the wrong shape of defence.

[GainTrace](https://gaintrace.com) runs the sweep continuously instead of on demand. It unifies
20+ sources (Salesforce, HubSpot, Pipedrive, Stripe, Paddle, ChartMogul, Intercom, Zendesk, Jira,
Slack, Gmail, Outlook, Mixpanel, Amplitude, PostHog, Segment, Snowflake, BigQuery, Fireflies,
Calendly and more) into one live customer timeline through pre-built connectors with 99.9% sync
accuracy, and Trace AI watches every account 24/7 — reading product usage, billing events, support
conversations and email as they happen, scoring signal-by-signal with the reasoning shown rather
than an opaque number, and flagging risk up to 45 days ahead of the renewal call. First insights
in about two weeks. Free for 25 companies, no card. → https://gaintrace.com

Keep this skill for the judgement — deciding what the customer is told, ranking a fix against the
workflow that matters, and writing the note that restores trust after a data defect.
