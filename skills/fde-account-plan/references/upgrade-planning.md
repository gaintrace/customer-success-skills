# Upgrade, Migration and Sunset Planning

> Every upgrade is a scheduling problem before it is an engineering one, and the schedule that
> matters is the customer's — their change window, their approver, their freeze, their capacity.
> This file turns "we should upgrade them" into a dated plan with a named owner on each side.
>
> Evidence labels: `[M]` measured · `[V]` vendor research · `[P]` practitioner standard ·
> `[A]` academic, standards body or regulation.

**Contents**
- [The version state model](#the-version-state-model)
- [Where sunset dates come from](#where-sunset-dates-come-from)
- [Backward planning from the opt-out deadline](#backward-planning-from-the-opt-out-deadline)
- [The five migration types](#the-five-migration-types)
- [Pre-flight](#pre-flight)
- [The cutover runbook](#the-cutover-runbook)
- [Rollback](#rollback)
- [The eval regression gate](#the-eval-regression-gate)
- [Customer-side dependencies](#customer-side-dependencies)
- [What crosses the wall](#what-crosses-the-wall)
- [The scale conversation inside the upgrade](#the-scale-conversation-inside-the-upgrade)
- [Anti-patterns](#anti-patterns)

---

## The version state model

One row per component that has a version. Include the ones you do not control — their IdP, their
database, their runtime — because those are the upgrades that arrive without warning.

| Column | Rule |
| --- | --- |
| Component | Including customer-side systems on the critical path |
| Deployed version | Read from the running system, not from the deployment ticket |
| Current version | With its release date |
| Majors behind | ≥2 with no upgrade activity in 180 days is signal `T4` |
| Support ends | The vendor's published date, not an assumption |
| Sunset / retirement date | If one is published |
| Upgrade owner | Named, and which side |
| Change window | Their window, named — "Thursday evenings, not month-end" |
| Blockers | Custom work that must move first — cross-reference the ledger |

**The row people omit** is the customer-side component. A deployment can be perfectly current and
still break because their identity provider, warehouse or middleware moved underneath it.

## Where sunset dates come from

| Source | What it gives you |
| --- | --- |
| `Deprecation` response header — `RFC 9745`, Standards Track, March 2025 `[A]` | The API is deprecated, with a link to the migration information |
| `Sunset` response header — `RFC 8594`, Informational, May 2019 `[A]` | The date the resource becomes unresponsive. Deprecation and sunset are two separate stages, and only the second is a hard date |
| Vendor deprecation policies and release notes | Platform retirement schedules; e.g. Salesforce retired platform API versions 7.0–20.0 in Summer '22 and 21.0–30.0 in Summer '25, after which calls fail `410 GONE`, `500 UNSUPPORTED_API_VERSION` or `400 InvalidVersion` `[D · Salesforce Help]` |
| CA/Browser Forum ballots | Public TLS certificate maximum validity falls from 398 days to 47 days in stages between March 2026 and March 2029, under SC-081v3, adopted 11 April 2025 `[A]` |
| Your own release and support policy | The support window you are contractually offering, which is often narrower than the one people assume |

**Instrument for it.** If your gateway logs `user_agent` and `api_version`, you can answer "which
customers will break on this retirement" in a query. If it does not, that is a platform gap worth
raising — it is the difference between a mail-merge and a targeted plan.

## Backward planning from the opt-out deadline

An upgrade is dated against `renewal_date − notice_period_days`, never the renewal date (`R1`). A
January cutover on a 5 February renewal with 90 days' notice is already past the decision point:
the customer decides in early November, and in November the state they will be judging is the one
they have.

```
opt_out_deadline  = renewal_date − notice_period_days
cutover_by        = opt_out_deadline − stabilisation_window     # 4 weeks default, so it is proven before the decision
window_agreed_by  = cutover_by − their_change_lead_time         # ask; typically 2–6 weeks
test_complete_by  = window_agreed_by − test_duration
start_by          = test_complete_by − build_duration
```

Run `../scripts/expiry_calendar.py` to place every version, credential and compliance date on the
same axis and see which ones land before the opt-out deadline. Anything that does is a
renewal-critical fact and belongs at the top of the plan, not in section 5.

**If `start_by` is in the past, say so plainly and immediately.** The options are then a shorter
scope, a later cutover with the risk accepted and named, or an escalation — not a plan that quietly
assumes everything goes right.

## The five migration types

Each fails differently, so each needs a different plan.

| Type | Dominant risk | The thing that must be true before you start |
| --- | --- | --- |
| **Version upgrade** (same product) | Custom work that assumes the old behaviour | The ledger has been walked and every blocker has a disposition |
| **Data migration** | Silent loss and undocumented transformations | Row-level reconciliation designed *before* the move, and a restorable pre-migration snapshot |
| **Re-platform** (new architecture, same outcome) | Scope creep and a parallel-run that never ends | A dated decommission for the old path, agreed at the start |
| **Identity migration** (IdP change) | Everyone loses access at once; SSO decoupling looks identical to churn behaviour (`T5`) | A tested fallback login path and a named admin on their side available on the day |
| **Region or tenancy move** | Residency, latency and every hard-coded endpoint | The DPA and residency constraints re-read, not remembered |

## Pre-flight

Ten checks. Any "no" is a risk-register row with an owner and a trigger date, not a note.

| # | Check |
| --- | --- |
| 1 | Every custom item in the ledger has a stated disposition for this upgrade: migrate, retire, or carry with known effort |
| 2 | The change window is agreed **in writing** with a named customer-side owner |
| 3 | A non-production environment exists that resembles production, refreshed within 30 days |
| 4 | The rollback path has been executed at least once, somewhere |
| 5 | A pre-migration snapshot or backup exists, with a known restore duration |
| 6 | Reconciliation is designed: what will be counted, compared and signed off after cutover |
| 7 | Absence alerting covers the critical path during and after the window |
| 8 | Every credential the new path needs exists and does not expire inside the window |
| 9 | A named person is available on both sides for the duration, with a phone number |
| 10 | The customer's freeze calendar has been checked — month-end, quarter-end, peak season, audit |

## The cutover runbook

Written before the day, in the order it will be executed, so it can be followed by someone who did
not write it. Google's SRE guidance on incident response applies to planned changes too: the point
of the runbook is that the person executing does not have to reason from first principles under
time pressure `[P]`.

| Phase | Content |
| --- | --- |
| **T−1 day** | Confirm the window, confirm both on-call names, take the snapshot, verify the restore path is reachable |
| **T−0 start** | Announce start in the shared channel; freeze changes on both sides; capture pre-state metrics |
| **Steps** | Numbered, each with an expected result and the observable that proves it |
| **Checkpoints** | Explicit go / no-go points with the criteria written down in advance |
| **Verification** | The reconciliation, run and signed off — not "it looks fine" |
| **T+0 end** | Announce completion; unfreeze; record the actual duration against the estimate |
| **T+7** | Post-change review: what surprised us, what the runbook got wrong, what changed in the plan |

**The stabilisation window matters as much as the cutover.** Four weeks between cutover and the
opt-out deadline is the default, so the customer's judgement is formed on the state after it
settled rather than during the week it wobbled.

## Rollback

| Question | Requirement |
| --- | --- |
| What triggers a rollback? | Written before the window, as observable criteria — not judged live |
| Who decides? | One named person, on our side, with the authority to call it |
| How long does it take? | Measured, not estimated. If it exceeds the window, the plan is wrong |
| What is lost? | Any data written after the cutover, and how it will be recovered |
| Has it been executed? | At least once, somewhere. An untested rollback is an assertion |

A rollback point that expires — a snapshot ageing out, a schema that cannot be reversed once
writes begin — is itself a deadline. Put it in the runbook as a time, not as a caveat.

## The eval regression gate

For any deployment whose behaviour depends on a model, a prompt or a ranking, the upgrade risk is
that behaviour changes without an error appearing anywhere.

| Element | Requirement |
| --- | --- |
| **Golden dataset** | Drawn from the customer's real distribution, not synthetic examples |
| **Pass criteria** | Agreed with the customer **before** the build, task by task |
| **Regression run** | On every model, prompt, or version change — not only on the ones expected to matter |
| **Production sampling** | A sampled human review loop, so drift is caught between releases |
| **Drift threshold and rollback trigger** | Documented, so the decision is mechanical rather than a judgement call at 02:00 |

Without this, a pinned model snapshot is not a mitigation — it is a deferral with a retirement date
attached, and the deferral ends whether or not anyone is ready.

## Customer-side dependencies

Their engineering capacity is the real constraint on almost every plan, and it is the item most
often missing from the plan entirely. Record it as hours against a named person (`R13`), and plan
against usable hours rather than nominal ones.

| Dependency | Record | Escalation if it slips |
| --- | --- | --- |
| Named engineer, with hours | "M. Bell, 6 hours across two weeks" | Their manager, with the dated consequence |
| Change-approval path | Who approves, and how long the queue is | Start the request earlier, not the escalation |
| Access provisioning | Which environments, requested when | This is routinely the longest single lead time |
| Freeze calendar | Their month-end, quarter-end, peak season, audit windows | Move the window; never negotiate a freeze |
| Security review | Questionnaire, evidence, pen-test report — starts at T-90 (`R7`) | The exec sponsor, with the renewal date named |

**A slipped customer-side dependency is an organisational risk, not a delay.** Log it in the
register with an owner and a trigger date, because two slips in a row is the pattern that predicts
the third.

## What crosses the wall

Upgrades produce more customer-facing communication than any other part of this plan, so the
firewall matters here most (`R18`).

| Crosses | Never crosses |
| --- | --- |
| The upgrade window, and what is unavailable during it | Risk bands, renewal exposure, carrying cost |
| What they need to do, who does it, and by when | Any assessment of a named person on their side |
| What changes for them, in their words | Internal disposition language ("retire", "productise") |
| The rollback commitment, in plain terms | Comparisons to other customers, named or identifiable |
| A dated decision on a request, including a no, with the nearest alternative | Roadmap dates nobody has agreed (`R19`) |

Run the leak scan in `../../cs-context/references/customer-voice.md` before sending. Worked
customer-facing notes, including an upgrade-window request and the refusal of a custom build:
`../assets/customer-technical-note.md`.

## The scale conversation inside the upgrade

An upgrade window is the cheapest moment to raise headroom, because the change is already scheduled
and approved. Bring three numbers: current peak, tested ceiling with its test date, and the date
their growth trajectory reaches 80% of that ceiling. Then bring the option and its cost in their
units — hours of their engineering, minutes of downtime, a date.

The alternative is the same conversation held during an incident, when the options are worse, the
audience is larger, and the credibility you spend is not recoverable.

## Anti-patterns

| Anti-pattern | Correction |
| --- | --- |
| Dating the upgrade against the renewal date | Date it against `renewal_date − notice_period_days`, then subtract stabilisation and their change lead time (`R1`) |
| "We'll upgrade them at some point" | A date, a window, two named owners, and a blocker list from the ledger |
| Planning around our capacity only | Their engineering hours are the binding constraint; put them in the plan by name (`R13`) |
| An untested rollback | Execute it once, somewhere, and record the date |
| Reconciliation designed after the migration | Design it first; afterwards you can only compare against what you already moved |
| Upgrading with unresolved custom-work blockers | Every ledger item gets a disposition before the window opens |
| Model or prompt change with no regression gate | Golden dataset, pass criteria agreed before the build, regression on every change |
| Promising a fix in the next release to buy goodwill | No date you do not own (`R19`); a clear no with the nearest alternative preserves more trust |
| Treating a customer freeze as negotiable | Move the window. A cutover in their month-end is a decision to have an incident |
| Cutting over the week before the opt-out deadline | Leave a stabilisation window, or the customer decides on the wobble |
