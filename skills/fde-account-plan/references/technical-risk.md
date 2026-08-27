# The Deployment Risk Register

> The risks that end deployments, categorised so the organisational ones cannot hide behind the
> technical ones, dated against the opt-out deadline so the commercial consequence is visible, and
> banded rather than given a fake probability.
>
> Evidence labels: `[M]` measured · `[V]` vendor research · `[P]` practitioner standard ·
> `[A]` academic, standards body or regulation.

**Contents**
- [The register format](#the-register-format)
- [The eight categories](#the-eight-categories)
- [Single points of failure](#single-points-of-failure)
- [Key-person risk on both sides](#key-person-risk-on-both-sides)
- [Unsupported versions and deprecated APIs](#unsupported-versions-and-deprecated-apis)
- [Unmigrated data](#unmigrated-data)
- [Expiring credentials](#expiring-credentials)
- [Compliance obligations as dated risk](#compliance-obligations-as-dated-risk)
- [Impact bands and ranking](#impact-bands-and-ranking)
- [Technical risk becomes renewal risk](#technical-risk-becomes-renewal-risk)
- [Working the register](#working-the-register)
- [Anti-patterns](#anti-patterns)

---

## The register format

One row per risk. Nine columns, and the last two are the ones most registers omit and most need.

| Column | Rule |
| --- | --- |
| **Risk** | A sentence with a subject and a failure. Not "integration risk" — "the WMS connector's service-account secret expires and the nightly reconciliation stops" |
| **Category** | One of the eight below. Forces organisational risk into the open |
| **Impact band** | Critical / High / Medium / Low, by the table in [Impact bands](#impact-bands-and-ranking). Never a probability (`R22`) |
| **Early-warning signal** | The observable that fires *before* the risk matures, and where it is observed |
| **Owner** | A named human, and which side. "The team" is not an owner |
| **Mitigation** | The specific work, not a posture |
| **Trigger date** | The date by which the mitigation must start, not the date the risk matures |
| **Before opt-out?** | Whether the trigger date falls before `renewal_date − notice_period_days` (`R1`) |
| **Status** | Open / mitigating / accepted / closed. An **accepted** risk needs the name of who accepted it |

Compute the dates with `../scripts/expiry_calendar.py`, which subtracts a per-class lead time from
each maturity date and reports whether the result lands before the opt-out deadline.

## The eight categories

Categorisation is not filing. **Most implementation failures are organisational rather than
technical** — no customer-side engineering capacity, competing priorities, an unnamed data owner —
and a register with only technical categories will show a green deployment right up to the point
where nothing gets done.

| Category | What lives here | Early-warning signal | Typical mitigation |
| --- | --- | --- | --- |
| **Technical** | SPOFs, no rollback, no observability across the boundary, unrepaired disconnects | Absence alerts; retry-exhaustion counts; a synthetic transaction failing | Redundant path, tested rollback, absence alerting |
| **Version** | Unsupported release, deprecated API in use, pinned snapshot with a retirement date | Version drift against the published sunset calendar; `Deprecation` response headers | Dated upgrade with a named customer-side owner and a window |
| **Data** | Unmigrated legacy data, undocumented transformations, broken lineage, schema drift with no contract test | Row-count deltas, null-rate spikes, failed contract tests | Contract-test the schema; document lineage; finish the migration |
| **Credential** | Expiring certificate, OAuth refresh token, service-account secret, API key with no rotation owner | Days-to-expiry from the calendar; auth-error class counts | Named rotation owner, automated renewal, an alert at lead time |
| **Key person** | Bus factor 1 — **ours and theirs, as separate rows** | One name on every config change and every incident | Runbook, recorded walkthrough, a second engineer on the rota; a named second contact their side |
| **Organisational** | No named customer-side owner, engineering capacity committed elsewhere, a change freeze crossing the cutover | Slipped customer-side dependencies; a shared channel going quiet; reschedules | Re-anchor with a named owner; move the window; escalate to the exec sponsor |
| **Compliance** | Lapsed evidence, subprocessor notice due, a residency constraint the architecture does not honour | Report period end dates; a data flow crossing a region boundary | Start the paper at T-90 (`R7`); fix the flow or amend the contract |
| **Commercial** | Carrying cost above threshold, entitlement/deployment mismatch, a workaround they pay to tolerate | Ledger share of ARR; contracted-vs-deployed delta | Disposition plan to the account owner; renegotiate or retire |

## Single points of failure

Enumerate rather than recall. Every deployment has at least two of these, and the exercise is
worth an hour once a quarter.

| SPOF | The question that exposes it | Usual fix |
| --- | --- | --- |
| One credential shared by every flow | If this secret is rotated wrongly, what stops? | Per-flow credentials with separate rotation dates |
| One scheduled job with no dead-man alert | If it silently stops, who notices and when? | Absence alerting, not error alerting |
| One person who can deploy | Who deploys when they are on leave? | Two named deployers, both having deployed |
| One network path | What is the alternative route, and has it carried traffic? | A tested secondary path, or an accepted risk with a name against it |
| One region | What is the failover, and when was it exercised? | Documented RTO/RPO, or an explicit acceptance |
| One hand-maintained file everything reads | Who edits it, and what happens on a typo? | Move it into the supported path; contract-test it |
| One customer-side approver | Who approves a change when they are unavailable? | A named delegate agreed in advance |

**Alerting on absence is the single highest-value change in most deployments.** Error-rate alerts
never fire when nothing is being sent, which is exactly the failure that goes unnoticed longest.

## Key-person risk on both sides

Compute the bus factor from **authorship and incident history** — who has changed config and
answered pages — rather than from the org chart. The truck-factor literature does exactly this from
authorship concentration: Avelino et al.'s Degree-of-Authorship algorithm, and the comparative
evaluation in Jabrayilzade et al., *Bus Factor In Practice*, ICSE-SEIP 2022 `[A]`. The practical
version:

```
For the last 12 months, per person:
  config/code changes to this deployment · incidents acknowledged · runbook entries authored
Bus factor = the smallest number of people whose removal leaves no one who has
             touched a critical component.
```

| Side | What bus factor 1 means | Response |
| --- | --- | --- |
| **Ours** | A delivery risk. Work stops when one person is unavailable, and handover is reconstruction | Runbook, recorded walkthrough, a second engineer who has actually run a change |
| **Theirs** | A **churn** risk with a 90–365 day lead time. That person is the deployment's only internal advocate; their departure removes the memory of why it was bought | A named second technical contact, a shared runbook, and a relationship above them (`R5`) |

Never average the two. They have different mechanisms, different owners and different remedies.
Champion departure is signal `R1` in `../../cs-context/references/signal-library.md` and carries a
48-hour exec response (`R3`) — the technical plan's contribution is knowing, in advance, exactly
what only that person knows.

**The question that populates this section:** ask every engineer on both sides, "what would break
if you were unavailable for a month?" Write the answers into the register verbatim.

## Unsupported versions and deprecated APIs

An unsupported version is not a hygiene item; it is a dated failure with a support contract that
has already ended. Retirements are real and enforced — Salesforce retired platform API versions
7.0–20.0 in Summer '22 and 21.0–30.0 in Summer '25, after which calls fail with `410 GONE`,
`500 UNSUPPORTED_API_VERSION` or `400 InvalidVersion` `[D · Salesforce Help]`.

| Finding | Band | Why |
| --- | --- | --- |
| Calling an API version with a published retirement date inside the term | **Critical** if the date precedes the opt-out deadline | The failure is scheduled, not probabilistic |
| Running a release outside its support window | **High** | No security fixes, and no support path during an incident |
| ≥2 major versions behind with no upgrade activity in 180 days | **Medium** | Signal `T4`; weak alone, decisive in combination |
| A pinned model or runtime snapshot with a retirement date and no eval regression gate | **High** | Behaviour changes silently at the pin's end of life |

Read deprecation off the wire where you can: `RFC 9745` defines the `Deprecation` response header
(Standards Track, March 2025) and `RFC 8594` defines `Sunset` (Informational, May 2019) `[A]`.
Planning: `upgrade-planning.md`.

## Unmigrated data

The migration everyone declares finished at go-live and nobody finishes.

| Check | Finding if it fails |
| --- | --- |
| Is any legacy source still authoritative for any field? | Two sources of truth; reconciliation is now permanent work |
| Is the legacy system still receiving writes? | The migration is not done, whatever the plan says |
| Is there a documented lineage from source to their reports? | Undocumented transformation — a `data` debt row |
| Is there a contract test on the source schema? | A schema change breaks them silently |
| Is historical data in the new system, or only new records? | Their year-on-year reporting will fail at the worst moment |

## Expiring credentials

Every credential is a dated failure with a name on it. The window for handling them is contracting:
CA/Browser Forum ballot SC-081v3, adopted 11 April 2025, takes the maximum public TLS certificate
validity from 398 days to 47 days in stages between March 2026 and March 2029 `[A]`. Manual
certificate renewal stops being viable inside that schedule.

| Credential | Record | Lead time before expiry |
| --- | --- | --- |
| Public TLS certificate | Issuer, expiry, renewal automation, owner | 30 days |
| Mutual-TLS client certificate | Both sides' expiry dates — they differ | 30 days |
| OAuth refresh token | Rotation policy, absolute expiry, re-consent path | 21 days |
| Service-account secret | Scope, expiry, who can rotate on the customer's side | 21 days |
| Signing key | Rotation procedure, key-ID handling on both sides | 30 days |

**The standard failure is not the expiry, it is the rotation.** Deleting the old secret before the
new one is deployed creates an outage window between the two. Rotate additively: create, deploy,
verify, then remove.

## Compliance obligations as dated risk

| Obligation | The dated element |
| --- | --- |
| SOC 2 / ISO evidence | Report period end; a gap between periods is a finding at their next audit |
| Penetration test | Validity window their security team accepts |
| DPA and residency | Any architecture change that moves data across the boundary it names |
| Subprocessor changes | GDPR Article 28(2) requires the controller to be informed of intended changes with a genuine opportunity to object; the Regulation sets **no fixed notice period**, so the contract sets it — read the contract, do not assume 30 days `[A]` |
| Breach notification | The contractual window, and who starts the clock on our side |

Anything maturing before the opt-out deadline is a renewal dependency and starts at T-90 (`R7`).

## Impact bands and ranking

Bands, never probabilities, unless a backtest exists (`R22`).

| Band | Entry criteria |
| --- | --- |
| **Critical** | Production stops, data is lost or exposed, or a contractual obligation is breached — and the trigger date has passed or falls inside 30 days |
| **High** | A core workflow degrades or a renewal dependency is missed; trigger date inside 90 days |
| **Medium** | Recoverable degradation, or added toil; trigger date inside 180 days |
| **Low** | Contained, with a workaround; trigger beyond 180 days |

Rank by `impact band × days-to-trigger`, ascending on days. State the tie-break: **when two rows
share a band, the one whose trigger date falls before the opt-out deadline outranks the one that
does not.** Ranking by band alone puts a distant Critical above an imminent High, which is how
registers stop being work queues.

## Technical risk becomes renewal risk

The translation the account team needs. Each row maps to a signal in
`../../cs-context/references/signal-library.md`, so `churn-risk` can consume it directly.

| Technical state | Signal | Renewal consequence |
| --- | --- | --- |
| Integration disconnected >30 days, unrepaired, unreported | `T2` | Near-certain if unrepaired; the value stopped and nobody missed it |
| API call volume on critical endpoints below 0.60 of baseline | `T1` | 60–150 day lead; check for efficiency work first — batching cuts calls while raising value |
| SSO / IdP decoupling | `T5` | 30–90 day lead, near certain; escalate the *check* within 24 hours |
| Bulk export by a non-routine admin | `T6` | 15–90 day lead; combined with a commercial signal it is exit preparation |
| Webhook endpoint auto-disabled, no remediation ticket | `T3` | 45–120 day lead |
| ≥2 Sev1 incidents in 180 days that the account experienced | `T8` | Converts to churn only alongside an unresolved sentiment signal |
| Customer-side technical owner departed, unreplaced | `R1` | 90–365 day lead; 48-hour exec response (`R3`) |
| Carrying cost above 5% of ARR | — | A margin problem discovered at the renewal instead of before it |

Integration depth correlates with retention in vendor research — ProfitWell's integrations study
reports roughly 10–15% higher retention with at least one integration and 18–22% with four or more,
and Crossbeam (n=526) reports users with integrations roughly 58% less likely to churn `[V]`. Both
are directional and self-selected; use them to argue for integration repair priority, never as
measured causal effects.

## Working the register

| Practice | Detail |
| --- | --- |
| **One primary workstream per quarter** (`R17`) | Three parallel remediations produce three half-migrations |
| **Written skip** (`R14`) | Anything not worked this quarter is listed with a reason and a revisit date |
| **Accepted risks carry a name** | "Accepted by <person>, <date>, revisit <date>" — acceptance without a name is avoidance |
| **Closed rows stay visible for one cycle** | So the register shows movement, not just backlog |
| **Trigger dates are reviewed at every refresh** | Dates move when the renewal date moves; recompute against the opt-out deadline every time |

## Anti-patterns

| Anti-pattern | Correction |
| --- | --- |
| "Integration risk — medium" | A sentence with a subject and a failure, plus its early-warning signal |
| Probability × impact scoring on made-up probabilities | Bands and days-to-trigger; no probability without a backtest (`R22`) |
| Only technical categories | Organisational risk is the most common cause of implementation failure and needs its own rows |
| One bus-factor number | Ours and theirs, separately; they have different mechanisms and remedies |
| Dating a risk against the renewal date | Date it against `renewal_date − notice_period_days` (`R1`) |
| Risks with no early-warning signal | If nothing can be observed before it matures, it is a fear, not a risk |
| An owner who is a function | Functions do not get paged; people do |
| Accepting a risk with no name and no revisit date | Acceptance is a decision and needs an owner |
| Treating an undated obligation as distant | Undated is unmeasured — write `UNKNOWN — requires the expiry date` |
