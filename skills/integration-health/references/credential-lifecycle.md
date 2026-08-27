# Credential Lifecycle

> Every token, key, certificate and scope on this account, treated as a **dated obligation**
> rather than a setting. Read this for any connector that authenticates, which is all of them.
>
> Evidence labels: `[M]` measured · `[V]` vendor-published · `[P]` practitioner convention ·
> `[A]` standard or peer-reviewed · `[D]` primary product documentation, with the fetch date. A lead
> time labelled `[P]` is a library convention — change it when your own rotation history disagrees.

**Contents**

[1 How to use this file](#1-how-to-use-this-file) · [2 The credential register](#2-the-credential-register--one-row-per-credential) · [3 What each type does at expiry](#3-what-each-credential-type-does-at-expiry) · [4 The dormancy table](#4-the-dormancy-table--credentials-that-die-from-disuse) · [5 Lead time and the opt-out arithmetic](#5-rotation-lead-time-and-the-arithmetic-against-the-opt-out-deadline) · [6 The ownership audit](#6-the-ownership-audit--the-service-account-that-was-a-person) · [7 Scope drift](#7-scope-drift--required-versus-granted) · [8 The certificate schedule](#8-the-certificate-schedule-that-ends-hand-rotation) · [9 Four rotation runbooks](#9-four-rotation-runbooks) · [10 Rehearsal](#10-rehearsal--the-field-most-registers-leave-blank) · [11 Traps and false positives](#11-traps-and-false-positives) · [12 What crosses to the customer](#12-what-crosses-to-the-customer) · [13 Finished when](#13-the-credential-section-is-finished-when)

---

## 1. How to use this file

A credential does not degrade. It works, and then on a specific day it does not, and that day was
knowable months earlier — so every credential finding is a calendar finding, and Dimension 8 in
`health-dimensions.md` scores runway rather than strength.

| Position this file takes | Consequence of ignoring it |
| --- | --- |
| **An undated credential is unmeasured, not distant.** A blank `credential_expires` scores Red | The connector that dies first is the one nobody could date |
| **A credential held by a person is one resignation from an outage** | The integration stops on their offboarding day, with no change our side and no error we caused |
| **Dormancy kills low-frequency connectors** | A quarterly extract on a 90-day inactivity window dies between every run; the first symptom is a missing quarter |
| **Granted scope is asserted, never assumed** | `S5` — the token authenticates, reads come back empty, every dashboard stays green |

**Run `../scripts/integration_health.py` first.** It computes days-to-expiry, the runway band and
the comparison against `renewal_date − notice_period_days`. This file covers what it cannot compute
— ownership, dormancy, rehearsal — which are the fields that actually break.

---

## 2. The credential register — one row per credential

One row per credential, not per connector: a single connector routinely holds three — an OAuth
grant, a webhook signing secret, a TLS client certificate — with three expiry dates and three owners.

| Field | Where it comes from | Blank means |
| --- | --- | --- |
| `credential_id` · `connector` · `system` · `type` | Your register, Step 1 inventory, §3 | A credential with no connector is an orphan — investigate before rotating it |
| `credential_granted_to` | IdP, connected-app record, key metadata | **Red.** The most common blank, and what §6 exists for |
| `granted_by` | Consent record, audit log | Nobody can say who authorised the access their security team will ask about |
| `scopes_required` / `scopes_granted` | Connector config / token introspection or the refresh response | `S5` is undetectable |
| `credential_expires` | Provider console, certificate, key metadata | Red band, and that connector's confidence is capped |
| `dormancy_window_days` | §4 | Assume none only where the provider publishes none |
| `rotation_lead_days` | §5 defaults | Script default 21 `[P]` — say that the default was used |
| `rotation_owner_ours` / `rotation_owner_theirs` | Named people, agreed in writing | A date nobody agreed to (`R19`) |
| `last_rotated_at` / `last_rehearsed_at` | Change record / §10 | The rotation has never been performed, or never tested |
| `days_to_opt_out_at_expiry` | Derived: `credential_expires − (renewal_date − notice_period_days)` | — |

Those field names are read directly by `../scripts/integration_health.py`; keep them. **A row whose
`rotation_owner_theirs` reads "their IT team" is not a row** — it is a gap with a job title where a
name belongs, and it is why a 20-minute rotation takes six weeks.

---

## 3. What each credential type does at expiry

The question that decides the runbook is not how long it lasts. It is **whether expiry is loud**
and **whether two can be valid at once** — an overlap window is the difference between a rotation
and an outage.

| Type | Typical life | At expiry | Loud? | Overlap? | Lead `[P]` |
| --- | --- | --- | --- | --- | --- |
| OAuth access token | 5–60 min | Refreshed automatically | Only if refresh fails | n/a | — |
| OAuth refresh token | Policy-set; §4 | `invalid_grant` on every call | Loud — Red on first occurrence | No; re-consent is a break | 14 d |
| API key / secret | Until revoked | `401` on every call | Loud | Yes — two live keys | 7 d |
| Service-account key | 90 d – never | `401`, or `403` if the account was disabled | Loud | Yes | 14 d |
| Webhook signing secret | Until rolled | Verification fails; events are retried, then abandoned | **Quiet — presents as `S6`** | Yes — dual-secret window | 7 d |
| TLS / mTLS certificate | 1–2 y, falling; §8 | Handshake fails; clients refuse the connection | Loud | Yes, if both chains are trusted | 30 d, or 0 with ACME |
| SAML / IdP signing certificate | 1–3 y | SSO breaks for every user at once (`T5`) | Loud and public | Yes — IdPs stage two | 45 d |
| SSH / SFTP key · PAT | Until revoked · 30–365 d | Connection refused · `401` | Loud | Yes | 7 d |
| Database password | Policy-set | Connection refused mid-run | Loud, and mid-batch | Yes, with a second grant | 21 d |
| Shared secret in a config file | Never expires | Never fails — it leaks instead | **Silent, permanently** | Yes | Rotate on discovery |

**The two quiet rows are where the money is.** A signing secret that no longer verifies produces
deliveries the provider retries and then abandons, indistinguishable from `S6` on the dashboard and
recoverable only inside the provider's replay window. A secret with no expiry is not low-risk — it
is a credential with no calendar entry, so nothing ever prompts a review of who holds it.

---

## 4. The dormancy table — credentials that die from disuse

A credential can be inside its expiry date and dead anyway, because the provider revokes on
inactivity. This is the mechanism behind the quarterly connector that has never run twice in a row.

| Provider policy | Window | What kills it | Source |
| --- | --- | --- | --- |
| Google OAuth, consent screen in **Testing** | **7 days** | Every issued refresh token expires after 7 days regardless of use | `[D · Google Identity OAuth 2.0 documentation, fetched 2026-08-28]` |
| Google OAuth, published app | **6 months** unused | The refresh token is revoked; a cap of 50 live refresh tokens per account per client also invalidates the oldest first | `[D · Google Identity OAuth 2.0 documentation, fetched 2026-08-28]` |
| Microsoft Entra ID refresh token | **90 days** inactive (`MaxInactiveTime`) | Revoked on inactivity, and separately on password reset, admin revocation or a Conditional Access change. Refresh and session lifetimes stopped being configurable through token lifetime policy on 30 January 2021 | `[D · Microsoft Learn, "Configurable token lifetimes" and "Refresh tokens in the Microsoft identity platform", fetched 2026-08-28]` |
| Salesforce connected app, "expire if not used for *X*" | Sliding, admin-set | Each use restarts the clock; a gap longer than *X* kills it. The other three policies are valid-until-revoked (default), immediately-expire, and expire-after-a-fixed-period | `[D · Salesforce Help, "Manage OAuth Access Policies for a Connected App", fetched 2026-08-28]` |
| Webhook subscription auto-removal | One major commerce platform retries a failed delivery up to **8 times over 4 hours** and removes the subscription after repeated failures in a 24-hour period | The *subscription* disappears — no auth error is ever raised | `[D · Shopify developer documentation, "Troubleshooting webhooks", fetched 2026-08-28]` |

**The test, and it is arithmetic:**

```
keepalive_required = expected_interval_days > (dormancy_window_days ÷ 2)
```

A quarterly job (91 days) against a 180-day window: 91 > 90, so **a keep-alive refresh is
mandatory** — one scheduled refresh a month, logged, with its own freshness check. A monthly job
(30 days) against a 90-day window passes at rest and fails the first time the job is paused for
eight weeks: `S4` and dormancy compound, turning a recoverable pause into a re-consent that needs
their admin. **Record `dormancy_window_days` on every OAuth row**, including where the answer is
"none published" — write that rather than leaving it blank.

---

## 5. Rotation lead time, and the arithmetic against the opt-out deadline

**Lead time is hands-on work plus the wait for the people and windows it needs**, and the second
term dominates. A rotation that takes eleven minutes takes three weeks when it needs a named admin
their side, a change ticket and a Thursday evening.

| Credential | Lead `[P]` | What sets it |
| --- | --- | --- |
| API key, PAT, SSH key · OAuth re-consent, service-account key | 7 d · 14 d | Our change process only · finding the right admin their side, their cloud IAM approval |
| Database password | 21 d | Coordinated grant, connection-pool drain |
| mTLS / public TLS certificate | 30 d | Issuance, trust-store distribution, a change window |
| SAML / IdP signing certificate | 45 d | Their identity team, a window, and a rollback plan for every user at once |

Four figures, computed on every row and printed as arithmetic:

```
opt_out_deadline       = renewal_date − notice_period_days                        (R1)
days_to_expiry         = credential_expires − as_of_date
runway_ratio           = days_to_expiry ÷ rotation_lead_days                      → Dimension 8
days_to_opt_out_at_exp = credential_expires − opt_out_deadline     (negative = expires first)
```

Bands are Dimension 8's: Green `runway_ratio ≥ 2`, Amber 1–2, **Red under 1, expired, or `UNKNOWN`**.

**Worked example — why the band alone is not the finding.**

```
Account            Northwind Logistics · renewal 2027-02-05 · notice 90 d
opt_out_deadline   2027-02-05 − 90 d       = 2026-11-07   (71 days from as-of 2026-08-28)
Credential         Salesforce OAuth refresh token · "Salesforce opportunities -> platform"
days_to_expiry     2026-10-14 − 2026-08-28 = 47 days
runway_ratio       47 ÷ 21                 = 2.24         → Dimension 8 GREEN
days_to_opt_out    2026-10-14 − 2026-11-07 = −24 days     → expires 24 days BEFORE they decide
credential_granted_to  m.torres@northwind.example         → a person, not a service account
```

Green on runway, and still the second-ranked remediation on the account: it expires inside the
notice window, so a failed rotation lands in the fortnight where the customer is forming a renewal
view, and it is held by an individual whose departure ends the sync without warning. **Rank on the
pair — runway and ownership — never on the band alone.**

---

## 6. The ownership audit — the service account that was a person

The most common credential defect in this library's field notes, and the cheapest to fix before it
fires. **The standard:** every credential is held by a **service account**, with **two named
humans** — primary and backup — on the **correct side**. Two, because one is the problem you were
fixing. Named, because `R19` forbids a rotation date nobody agreed to.

| Ownership failure | How it presents | The check |
| --- | --- | --- |
| Personal user token | `credential_granted_to` contains a human name | Diff it against their directory every sweep |
| Departed employee | The connector dies on a Tuesday, no change either side | Ask their IT for the leaver list; diff against the register |
| Contractor or partner account | Access ends with a statement of work nobody told us about | Record the contract end date beside the expiry date |
| Shared mailbox or generic login | MFA prompts nobody sees; consent nobody can re-give | Move to a service account before any other remediation on that connector |
| Consent granted by a leaver | The token lives, and nobody can re-consent when it dies | Audit `granted_by` separately from `credential_granted_to` |
| One admin holds every credential | Bus factor 1 their side, invisible until annual leave | Count distinct owners; one name on three or more credentials is a finding |

```sql
-- Every credential a person can take with them when they leave
SELECT c.credential_id, c.connector, c.credential_granted_to, c.granted_by, c.credential_expires
FROM   credential_register c
LEFT   JOIN customer_directory d ON lower(d.email) = lower(c.credential_granted_to)
WHERE  d.email IS NOT NULL OR c.credential_granted_to IS NULL   -- resolves to a human, or to nobody
ORDER  BY c.credential_expires;
```

**The offboarding test, once per sweep.** For each credential: *if the person in
`credential_granted_to` resigned tomorrow with normal notice, when does this connector stop, and who
finds out first?* Where the honest answer is "the customer, from a wrong number in a report", that
connector scores detectability 2 in the Step 5 ranking and the finding is ownership, not runway.

---

## 7. Scope drift — required versus granted

OAuth 2.0 permits the authorisation server to issue a token whose scope differs from the one
requested, and requires it to tell the client when it does, through the `scope` parameter on the
response `[A · RFC 6749 §3.3]`. A client that never reads that field cannot tell a full grant from a
reduced one — and a reduced grant fails silently, because reads needing the missing scope return
empty rather than `403`. That is `S5` in `silent-failures.md`.

**The assertion, on every refresh rather than on a schedule:**

```
missing = set(scopes_required) − set(scopes_granted)
if missing:  fail the run, page the credential owner, name the missing scopes
```

An empty diff is not proof of health. Pair it with **one canary read per scope** — a query known to
return at least one row.

| Cause of a reduced grant | Detection | Fix |
| --- | --- | --- |
| Re-consent through a UI that dropped an optional scope | Set assertion at refresh | Re-consent with the full list, from a service account |
| Their admin narrowed a permission set or profile | Canary read returns zero where it returned rows yesterday | Restore the permission on the integration user; pin the required set into a contract test |
| A field-level permission removed one field, not the object | Column-set assertion (`S3`) — the scope check cannot see this | Run both assertions, always |
| Policy change on their IdP or app-governance tool | Scopes present, tokens short-lived, refreshes failing | Their security team owns it; the fix is an exception with a named approver |
| A security review deliberately reduced the grant | It is in their change log | Do **not** quietly restore it. Remove the dependent feature and say which reporting stops |

**Log the granted scope set on every refresh, with a timestamp.** Without it, "when did this stop
arriving?" has no answer and the reconciliation window cannot be bounded.

---

## 8. The certificate schedule that ends hand-rotation

Maximum public TLS certificate validity is on a published, phased reduction under CA/Browser Forum
ballot **SC-081v3**, adopted 11 April 2025 `[A · CA/Browser Forum, Ballot SC-081v3]`:

| From | Max validity | Rotations/year | What it does to a manual process |
| --- | --- | --- | --- |
| Today | 398 days | ~1 | A calendar reminder works |
| **15 March 2026** | **200 days** | ~2 | A calendar reminder mostly works |
| **15 March 2027** | **100 days** | ~4 | Manual rotation becomes a recurring quarterly outage risk |
| **15 March 2029** | **47 days** | ~8 | Hand-rotation has stopped being viable |

Domain-control-validation reuse periods fall on the same ballot, reaching 10 days by 2029, so the
re-validation step shortens alongside the certificate `[A]`.

**The decision this forces is binary.** Either the certificate moves to automated issuance and
renewal (ACME, or the platform's managed equivalent) with a monitored expiry, or someone signs a
**dated acceptance of a recurring failure** naming the date the manual process stops working for
that connector. No third option survives 2027, and writing the acceptance down is what turns an
oversight into a decision (`R14`).

**Machine credentials and human passwords rotate on different principles — do not merge them.**
Symmetric and signing keys carry bounded cryptoperiods so a compromise has an end date
`[A · NIST SP 800-57 Part 1 Rev. 5]`; memorised human secrets should **not** be forced to change on
a calendar, only on evidence of compromise `[A · NIST SP 800-63B]`. A customer security team
quoting the second at you while you ask about the first is answering a different question — say
which one you are asking.

---

## 9. Four rotation runbooks

Every runbook states its rollback; a rotation without one is a change window with a coin toss in it.
Effort is our hands-on time, elapsed is the calendar wait for their people and windows.

### R-A · OAuth re-consent, moving a person's grant to a service account

**Effort ≤2h ours (theirs ~20 min) · elapsed 14 d.** Needs a named admin their side with authority
to create an integration user, and `scopes_required` in writing.

1. Create the integration user their side; record the new `credential_granted_to`.
2. Grant exactly `scopes_required` — an over-scoped integration user is what their next security
   review opens with.
3. Authorise the connector as the new account in a sandbox or second instance; one canary read per scope.
4. Cut over the connector config, keeping the old grant **live**.
5. Verify one full run, the identity closing (`submitted = succeeded + failed + unprocessed`) and
   granted scopes equal to required. Then revoke the old grant and record `last_rotated_at`.

**Rollback:** repoint at the old grant, available until step 6 — which is why step 6 is last.
**It worked when** the person named in the old grant loses platform access and the sync keeps running.

### R-B · Keys and secrets, two-live overlap (API key · service-account key · SSH key)

**Effort ≤2h · no downtime.** Needs a provider that allows two live credentials, which is most.

1. Issue the second key on the **same** service account — a new account means new grants and a new
   failure surface. Revoke nothing yet.
2. Deploy it to **every** consumer; the forgotten batch job is the outage.
3. Verify in the provider's usage view: new key non-zero and old key **zero** across a full business
   cycle, weekly and monthly jobs included.
4. **Disable** the old key — do not delete it. A disabled key is re-enabled in seconds. Delete after
   one more full cycle and record `last_rotated_at`.

**Rollback:** re-enable at step 4. **Trap:** revoking at step 2 because the dashboard showed no
traffic on a Tuesday, when the reconciliation job runs on Sundays.

### R-C · Webhook signing secret, dual-secret window

**Effort ≤2h · no downtime if the order is right.** One payments provider keeps the previous secret
valid for **up to 24 hours** after a roll and signs with both `[D · Stripe webhooks documentation,
fetched 2026-08-28]`.

1. Roll with a **delayed** expiry on the old secret, never an immediate one.
2. Deploy the receiver verifying against both secrets.
3. Verify zero signature failures across a full window, and the emitted-vs-materialised event-ID
   reconciliation (`silent-failures.md` §S6) clean over the same window.
4. Let the old secret expire; remove it from the receiver.

**Rollback:** the old secret is live until step 4. **Trap:** immediate expiry at step 1 — in-flight
deliveries fail verification, are retried, then abandoned on the provider's schedule. Check the
receiver's clock: verification commonly enforces a timestamp tolerance (5 minutes by default at one
major provider `[D]`), so clock drift reads as a compromised secret.

### R-D · TLS or mTLS certificate

**Effort ≤1d · downtime 0–5 min.** Needs a change window and the trust-store owner named both sides.

1. Issue at least `rotation_lead_days` before expiry, checking the **intermediate** chain and not
   only the leaf — an expiring intermediate fails identically and is missed twice as often.
2. Stage to the trust store; restart nothing yet.
3. Cut over in the window, one node at a time behind the load balancer where the topology allows.
4. Verify handshakes from a client outside your network, the served expiry date, and freshness back
   inside band after one full interval. Then remove the old certificate from the trust store.

**Rollback:** restore the previous certificate and restart — under five minutes, and rehearse it
(§10) so that number is measured rather than hoped for.

---

## 10. Rehearsal — the field most registers leave blank

`last_rehearsed_at` is the difference between a runbook and a document. Rehearse in a sandbox or a
non-production tenant and record three things: **elapsed time, who was needed, and what the runbook
got wrong.** Every rehearsal finds at least one wrong step `[P]` — usually a consumer nobody listed.

| Credential class | Rehearse | Why that cadence |
| --- | --- | --- |
| Anything Red or Amber on Dimension 8 | Before the rotation, every time | The cost of a surprise is an outage inside the notice window |
| SAML / IdP signing certificate | Twice a year | It fails for every user at once and the rollback is public |
| TLS on a manual process | Every rotation until automated | The interval is shortening on the §8 schedule |
| OAuth grants held by a person | At the ownership fix, then never — the fix removes the class | Rehearsing a defect costs more than removing it |

A Red-band credential with a blank `last_rehearsed_at` enters the report as
`UNKNOWN — rotation never rehearsed`, and gets a wider window than its effort band suggests.

---

## 11. Traps and false positives

| Apparent finding | Innocent explanation | The check that separates them |
| --- | --- | --- |
| Auth errors overnight | A rotation performed correctly, mid-window | Did a successful auth follow inside the rotation window? Check the change record |
| "Credential expires 2027" | The *access* token's lifetime was read, not the grant's | Read the grant, the connected-app policy and the certificate — three different dates |
| Token valid, reads empty | Reduced scope (`S5`), or a field-level permission (`S3`) | Scope-set assertion plus canary read; then diff the column set |
| "No expiry" | Valid-until-revoked is a policy, not immortality: a password reset, an admin revocation or a Conditional Access change ends it `[D · Microsoft Learn, fetched 2026-08-28]` | Record the revocation triggers beside the expiry |
| SSO change read as decoupling | An IdP migration unrelated to us | Ask, in one email, and record the answer. An unanswered, unreported break is the `T2` finding — not the break itself |

---

## 12. What crosses to the customer

**Crosses:** the credential, its expiry, what stops working, what you need from them, and how long
it takes. **Never crosses (`R18`):** the runway band, the criticality score, the renewal read, and
any observation about the person whose name is on the token. Written to
`../../cs-context/references/customer-voice.md`; run the leak scan first. The ownership ask below is
the one worth getting right, because it asks a customer to change something that works today.

════════════════════════════════════════════════════════════
CUSTOMER-FACING — copy the block below and send as written.
Everything above this line is internal. Do not forward it.
════════════════════════════════════════════════════════════

```text
Subject: The Salesforce sync token expires 14 October — 20 minutes to make it permanent

Hi Marcus,

The token your Salesforce sync uses stops working on 14 October. Rotating it
as it stands takes twenty minutes; moving it to an integration user takes the
same twenty minutes and removes the expiry entirely, so I'd rather do that
once than book this again in the spring.

Your end: create an integration user in Salesforce with API access and read
on Opportunity — I'll send the exact permission set, which is three lines and
nothing broader than the sync already uses — then authorise the connector as
that user while I watch the first run.

What changes for you: the sync stops depending on any one person's account,
so it keeps running through leave, laptop rebuilds and role changes. Today
it's authorised under your own login, so a password reset on your account
stops the nightly load. I'll keep the current authorisation live until the
new one has run a full night successfully, so nothing goes dark.

Thursday 11 September or Tuesday 16 September, twenty minutes? If neither
works, give me a name and I'll send them the steps.

Jo
```

---

## 13. The credential section is finished when

- [ ] Every credential has its own row — not every connector, every credential
- [ ] `credential_expires` is a date or `UNKNOWN — requires <console>`; no row reads Green on a blank
- [ ] `credential_granted_to` resolves to a service account, and two named humans own the rotation, on the correct side
- [ ] `scopes_required` and `scopes_granted` are both recorded and diffed, with one canary read per scope
- [ ] `dormancy_window_days` recorded per OAuth grant, and `keepalive_required` computed against the run interval
- [ ] Every expiry compared against `renewal_date − notice_period_days`, arithmetic shown (`R1`)
- [ ] Every rotation carries a runbook, a rollback, an effort band, an elapsed estimate, and a rehearsal date or an explicit `UNKNOWN — never rehearsed`
- [ ] Certificates on a manual process carry either an automation plan or a dated, named acceptance of the §8 schedule (`R14`)
- [ ] Nothing in the customer-facing block names a band, a score, a renewal date or a person's reliability (`R18`)
