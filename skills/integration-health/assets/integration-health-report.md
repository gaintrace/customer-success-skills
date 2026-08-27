# Integration Health — <Account> · <YYYY-MM-DD>

**Internal document.** Criticality, priority arithmetic, severity bands, ARR exposure and the
renewal read never go to the customer, in any wording (`R18`). The customer-facing block is written
separately from `customer-integration-note.md`.

**Run on:** <scope: this account, every connector / one connector / a book or segment /
post-incident> · <trigger: routine or pre-renewal sweep / the customer says the data is wrong /
a connector is visibly failing / a deadline is coming> · evidence <connector logs + record counts
both sides / connector status only / their side only / nothing yet> · **data as-of <YYYY-MM-DD>** ·
<one line naming any default taken rather than answered>

---

## Brief — emit this first, always

````markdown
**<Account> — <N> connectors · <R> red / <A> amber / <G> green · <X> records unaccounted for · earliest deadline <date> (<N> days).**

**1. <Connector> — <severity>.** <What is failing and what it costs them, with provenance.>
**Do:** <Owner, side> <action> by <date>.
**2. <Connector> — <severity>.** <One sentence, with provenance.> **Do:** <Owner, side> <action> by <date>.

**Silent failures found:** <S-codes, or "none of the six — reconciliation clean over <window>">.
**Customer told:** <what, by whom, by when — or "nothing to disclose; counts reconciled">.

Confidence: <level> (<n>/7 families). **What would change this:** <2–3 observable events>.

*Full report, coverage ledger and workings on request.*
````

---

## Bottom line

<Three sentences. The connector that matters. The records unaccounted for and over what window.
The single most urgent action, with its named owner and date.>

| | |
|---|---|
| Connectors inventoried / red / amber / green | N / a / b / c |
| Records unaccounted for · silent failures found | X of Y (<Z>%) over <window> · <S-codes, or none of six> |
| Earliest hard deadline | <date> — <credential expiry / API sunset / opt-out> — <N> days |
| Opt-out deadline | <date> = `renewal_date <date> − notice_period_days <N>` (`R1`) |
| ARR on workflows behind a red connector | $X |
| Report confidence | High / Medium / Low — <criteria met, and the coverage cap that bounds it> |

---

## 1. Connector inventory

Every connector, including middleware, customer-built scripts and retired-but-live pilots.
**Print the negatives** — "no customer-built scripts against the public API in 90 days of gateway
logs" is a finding.

| Connector | Direction | Systems | Auth | Cred expires | Frequency | Records/day | Owner (ours) | Owner (theirs) | Workflow it feeds | If it stops |
|---|---|---|---|---|---|---|---|---|---|---|
| | inbound / outbound / bidirectional | A → B | oauth2 / api_key / mtls / svc key | <date or `UNKNOWN — requires <console>`> | | | <name> | <name> | | |

**Swept and not found:** <middleware platforms checked · customer-built scripts · retired
connectors still holding credentials — name what was checked and what came back empty.>
**Added to `fde-account-plan`'s inventory this sweep:** <what that plan did not have.>

---

## 2. Health dimensions

Eight per connector, every time. A dimension with no data reads `UNKNOWN — requires <source>` and
never reads Green. Severity is the **worst** band, not an average.

| Connector | Freshness | Errors by class | p50 / p95 vs budget | Throughput | Partial failure | Schema drift | Deprecation | Cred runway | Worst band |
|---|---|---|---|---|---|---|---|---|---|
| | <ratio × expected> | auth <n> · rate <n> · valid <n> · schema <n> · transient <n> · perm <n> | <ms / ms vs ms> | <ratio ×> | <unaccounted / expected> | <identical / additive / removal> | <version, sunset, days> | <days, ratio × lead> | Red / Amber / Green / UNKNOWN |

**Latency budgets used, and where each came from:** <their deadline, per connector — never a
generic SLO.>
**Where `expected` for throughput came from:** <SOW figure / customer-stated volume / trailing
28-day median for that weekday — say which, because the choice changes the finding.>

---

## 3. Silent-failure sweep

All six on every connector. Every cell reads `clear` / **`FOUND`** / `UNKNOWN — requires <source>`.
**No blanks** — a blank cell is indistinguishable from a check nobody ran.

| Connector | S1 batch | S2 coercion | S3 filtered | S4 paused | S5 scope | S6 webhook | Evidence |
|---|---|---|---|---|---|---|---|
| | | | | | | | <query, log or count, with its window> |

**Extended sweep** (`../references/silent-failures.md` §S7–S9), where the connector class warrants it:

| Connector | S7 pagination | S8 window/DST | S9 upsert key | Evidence |
|---|---|---|---|---|
| | | | | |

### Reconciliation workings

Show the arithmetic. Name the level run — L1 run · L2 day · L3 entity · L4 field — and never report
"no data loss" from L1 alone.

| Connector | Window (UTC, half-open) | Level | Expected | Submitted | Succeeded | Failed | Unprocessed | Residual | Shortfall | Unaccounted | Recoverable? |
|---|---|---|---|---|---|---|---|---|---|---|---|
| | `[start, end)` | L1 / L2 / L3 / L4 | | | | | | | | | yes / no / `UNKNOWN` |

`submitted = succeeded + failed + unprocessed` → residual · `expected = submitted` → shortfall ·
`unaccounted = max(0, residual) + max(0, shortfall)`.

**Where reconciliation was not possible:** `UNKNOWN — requires record counts at both ends for
<window>`, and the confidence cap it forces. Never "no data loss detected" for "loss was not
measurable".

---

## 4. Credential calendar

One row per credential, not per connector. Full lifecycle in
`../references/credential-lifecycle.md`.

| Credential | System | Granted to | Scopes required / granted | Expires | Days to opt-out then | Rotation lead | Rotation owner (side) | Last rehearsed |
|---|---|---|---|---|---|---|---|---|
| | | <service account, or **a person** — flag it> | <list> / <list> | <date> | <+/− N days vs opt-out> | <N d> | <name (ours/theirs)> | <date or `UNKNOWN — never rehearsed`> |

**Dormancy:** <any credential whose provider revokes on inactivity, with the window, and whether
`expected_interval_days > dormancy_window_days ÷ 2` makes a keep-alive mandatory.>
**Ownership audit:** <credentials resolving to a named human rather than a service account; the
offboarding consequence for each.>

---

## 5. Deprecation runway

| Connector | Version in use | Vendor policy | Sunset date | Before opt-out? | Migration owner (side) | Cutover window |
|---|---|---|---|---|---|---|
| | | <hard retirement / date-based, no forced migration / rolling N versions / `UNKNOWN — requires the policy in writing`> | <date> | yes / no | <name (side)> | <date, ≥30 days before opt-out or after signature> |

**`Deprecation` and `Sunset` headers observed:** <values logged, per connector — or "not logged;
first remediation is to log them" (`RFC 9745`, `RFC 8594`).>
**Strictest vendor in their stack:** <name and date — this sets the exposure clock, not the average.>

---

## 6. Ranked remediation

Ranked by `Impact × Severity × Urgency`, where `Impact = workflow_tier × blast_band ×
detectability`. **Tie-break in order:** earlier hard deadline, then higher ARR dependent on the
workflow, then higher blast band. Cut to workable hours (`R13`).

| # | Connector | Severity | Customer impact in their terms | Fix | Effort | Elapsed | Owner (side) | By | Agreed? | Expected effect | Success measure | Detector left behind |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | | | | | ≤2h / ≤1d / ≤1w | <N d> | <name (side)> | <date> | yes (`R19`) | | | |

**Arithmetic, top three:**

```
1. <connector>  workflow_tier <n> × blast_band <n> × detectability <n> = Impact <n>
                Impact <n> × Severity <n> × Urgency <n.nn> = <n.n>   [deadline <date>, <N> days]
2. …
3. …
Tie-break applied: <which rule, between which rows>
```

**Capacity line:** <usable hours this cycle = engineers × weeks × 40 × 0.6> — rows 1–<n> fit;
everything below moves to section 7.

### Detectors now in place

| Detector | Watches | Threshold that fires | Fires to (name, side) | Cadence | Catches |
|---|---|---|---|---|---|
| | | | | | <S-code / dimension> |

---

## 7. Not remediated this cycle (`R14`) · Checked and clear

| Connector | Why not | Revisit | What we watch meanwhile |
|---|---|---|---|
| | <reason — "not enough hours" is legitimate; an empty cell is not> | <date> | <detector still running> |

| Family | What was checked | Result |
|---|---|---|
| | | checked, nothing found |

---

## 8. Renewal read — internal only, permanently

Never crosses to the customer in any wording (`R18`). Feeds `churn-risk`.

| Signal | Value this sweep | Feeds |
|---|---|---|
| `T1` API call decline | <%, window — check `distinct_endpoints` and `records_processed`, not request count> | Technical decoupling |
| `T2` integration disconnected | <days unrepaired, per connector> | Technical decoupling · risk floor |
| `T3` webhook failure rate | <%, window> | Technical decoupling |
| `T5` SSO / IdP change | <what changed, when, who initiated> | Technical decoupling · Consolidation target |

**Did any disconnect go unreported by the customer, and for how long?**
<Plain answer. A break they neither noticed nor asked us to fix is unwiring, not a bug (`R2`,
`C21`) — hand it to `churn-risk` the same day.>

**ARR on workflows behind a red connector:** $<X> · **Opt-out deadline:** <date> (<N> days).

---

## Coverage Ledger

| Signal family | Source checked | Status | Notes |
|---|---|---|---|
| 1 Product usage & adoption | API gateway · metering DB · product analytics · audit log | | |
| 2 Commercial & contract | Order form · MSA/SLA · CRM | | |
| 3 Relationship & engagement | Org chart · shared channels · ticket requesters | | |
| 4 Support & reliability | Ticketing · incident management · status page | | |
| 5 Sentiment & VoC | Ticket text · transcripts · survey verbatims | | |
| 6 Billing & payment | Billing · metering · credit memos | | |
| 7 Firmographic & external | Vendor deprecation notices · enrichment · their release notes | | |

**Coverage: X / 7 (Y%) → confidence capped at <level>** (`R23`).
**Blind spots:** <which families are missing, and what those gaps hide in an integration review —
e.g. with no sentiment source, a customer who has already stopped trusting the data is invisible
here, so this assessment is a floor on risk rather than a ceiling.>

---

## Assumptions

| # | Assumption | Why it was needed | If wrong |
|---|---|---|---|
| 1 | | | <the concrete consequence: which rows move band, which dates move> |
| 2 | | | |
| 3 | | | |

**Ingest mappings below 0.80 confidence, confirmed with the user:** <column → field, per file — or
"none below 0.80".>

---

## Customer-facing output

Emit only when the audience is the customer's technical owner, or a disclosure is due. Draft it from
`customer-integration-note.md`, written to `../../cs-context/references/customer-voice.md`, and run
the leak scan before it leaves this document.

**Crosses the wall:** what broke, the record count and the window in their units, what is fixed,
what needs a named owner their side and by when, the monitoring now in place.
**Never crosses (`R18`):** criticality, priority arithmetic, severity bands, ARR exposure, the
renewal read, and any observation about who on their side did or did not notice.

**Disclosure decision:** <disclose / nothing to disclose — counts reconciled clean over <window>> ·
**Owner:** <name> · **By:** <date> · **Channel:** <call then written follow-up, for anything the
customer will read as bad news (`C26`)>.
