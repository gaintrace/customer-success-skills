# Acceptance Criteria

> A deliverable is a thing we hand over. An **accepted deliverable** is a thing a named person on
> the customer's side has said, in writing, does what the SOW said it would. Only the second
> closes a milestone, releases a payment, and survives being cited at a renewal.
>
> Evidence labels: `[M]` measured · `[V]` vendor · `[P]` practitioner rule · `[A]` academic.

**Contents**
1. [Deliverable vs accepted deliverable](#1-deliverable-vs-accepted-deliverable)
2. [The three properties](#2-the-three-properties)
3. [The criterion form](#3-the-criterion-form)
4. [Criterion library by milestone type](#4-criterion-library-by-milestone-type)
5. [Deemed acceptance](#5-deemed-acceptance)
6. [Disputed acceptance](#6-disputed-acceptance)
7. [Criteria that never close](#7-criteria-that-never-close)
8. [Acceptance and the renewal](#8-acceptance-and-the-renewal)
9. [Anti-patterns](#9-anti-patterns)

---

## 1. Deliverable vs accepted deliverable

| | Deliverable | Accepted deliverable |
| --- | --- | --- |
| Who decides it exists | Us | A named person on their side |
| Evidence | We say it is done | Written acceptance, or the deemed-acceptance clock expiring |
| Effect on the schedule | The next task can start | The milestone closes |
| Effect on revenue | None | The invoice can be raised; the revenue can be recognised |
| Effect at the renewal | "We delivered it" — contestable | "You accepted it on 14 March" — not contestable |
| Effect on the estimate | None | Contingency for that package can be released |

**Track acceptance status, never delivery status.** A weekly report that says "6 of 8 milestones
delivered" hides the only number that matters: how many are accepted. `delivered_at`,
`acceptance_due`, `accepted_at`, `accepted_by`, `acceptance_state` ∈
`pending · accepted · deemed_accepted · rejected · disputed` — five fields, and they turn a
project status meeting into a two-minute read.

**Delivered-but-unaccepted is a live risk, not a formality.** Age it. Anything past its deemed
window that has neither been accepted nor rejected means the acceptor has disengaged, is unable
to test, or disagrees and has not said so. All three are worth knowing in week three rather than
at the review.

---

## 2. The three properties

Every criterion is **observable, testable and signed**. Missing any one, it will not close.

| Property | Definition | The question that tests it | Fails as |
| --- | --- | --- | --- |
| **Observable** | Someone who did not build it can see whether it is true | "Could a new starter on their team check this without asking us?" | "The integration is working" |
| **Testable** | There is a named test, a named tester, a data set and a threshold — all agreed **before** the build | "What is the number, and who runs it?" | "Performance is acceptable" |
| **Signed** | A named customer role accepts in writing within N business days of the delivery notice, or it is deemed accepted | "Whose name is in the acceptor column?" | "The team is happy with it" |

**The before-the-build rule is the whole game.** A criterion agreed before work starts is a
specification. The same sentence written after delivery is a negotiation, and the party holding
the invoice always loses it. Attach criteria to the SOW as an exhibit at signature; if a
criterion cannot be written yet because the design is not settled, say so explicitly and make
"criteria agreed for milestone N" a dated dependency in its own right.

---

## 3. The criterion form

```
Given   <the customer's own data, volume or condition>
When    <named tester> performs <specific action> in <named environment>
Then    <observable result> at <threshold>
Verified by <named person, role, customer side> within <N> business days of the delivery notice.
```

| Element | Rule | Why |
| --- | --- | --- |
| Given | Their data, not ours; state the volume and the period it came from | A criterion that passes on our fixture and fails on their data has tested nothing |
| When | One action, one environment, named | "The system works" spans a hundred actions and closes on none |
| Then | A number with a unit and a comparison | "Faster" and "reliable" are unenforceable in both directions |
| Threshold | Agreed before build, recorded in the exhibit | Otherwise the threshold is set by whoever is most disappointed |
| Verified by | A person and a role, never a team | Teams do not sign |
| Within N | Default 5 business days `[P]` | An acceptance process with no clock is a veto |

**Worked example**

> Given the 4,812 supplier invoices your AP team received in February, when Priya Raman (AP
> Manager) runs the reconciliation report in production, then at least 97% of invoices carry a
> matched PO and the median approval time is under 8 hours, against the four-week baseline of 31
> hours. Verified by Priya Raman (AP Manager) within 5 business days of the delivery notice.

Three things make it work: their February data, one named person doing one named thing, and a
threshold that was written down in January.

---

## 4. Criterion library by milestone type

Adapt the numbers; keep the shape. Thresholds marked `[P]` are this library's defaults, not
measured benchmarks.

| Milestone type | Acceptance criterion pattern | Threshold defaults `[P]` | Typical acceptor |
| --- | --- | --- | --- |
| **Environment and access** | Named users authenticate to the named environment via the agreed identity path and reach the application without a manual step | 100% of the named users, on their own devices | Their IT lead |
| **Configuration** | The contracted primary use case is configured and a named business user completes it end to end on their own data without vendor assistance | One clean end-to-end pass, unaided, observed | Their process owner |
| **Integration** | The connector authenticates, syncs on the agreed schedule and completes with zero unhandled errors for N consecutive days on production volume | 5 consecutive days, error rate <0.5%, p95 latency under the stated figure | Their integration owner |
| **Data migration** | Record counts, control totals and a named sample reconcile to source within tolerance | Counts exact; monetary control totals within 0.1%; a 50-record sample field-level exact | Their data owner |
| **Model / agent behaviour** | Against a golden set drawn from their own distribution and frozen before the build, task-level pass rate meets the threshold, and the failure classes are the ones agreed | Golden set ≥200 records from their last quarter; pass rate agreed pre-build; no failure in the named unsafe classes | Their process owner plus their risk reviewer |
| **Reporting / analytics** | A named report returns figures that reconcile to their existing source of truth for the same period | Within 0.5%, or the variance is explained and accepted | Their analyst |
| **Performance / scale** | The stated peak volume processes within the stated window at the stated concurrency | 2× stated peak, sustained for the stated window | Their platform owner |
| **Security / compliance** | Their review is closed with no open findings above the agreed severity | Their reviewer's written sign-off | Their security reviewer |
| **Admin enablement** | Two named admins each complete the six core admin tasks unaided, observed | Two admins, never one; all six tasks | Their admin lead |
| **End-user enablement** | ≥70% of trained users perform the core action at least once within 14 days of their session | 70% / 14 days | Their team lead per team |
| **Runbook / handover** | Their on-call engineer resolves a seeded failure using only the runbook, without contacting us | One seeded failure, resolved unaided | Their on-call lead |
| **Production rollout (V-day)** | The activation event occurs at its natural cadence, performed by the buying team, over at least two cycles, measured against the captured baseline | Two full cycles; the buying team, not only the admin | Their named business owner |

**Two rules that apply across the whole library.** First, the acceptor for a value-bearing
milestone is a **business** owner, not an IT owner — IT accepts that it works, and only the
business can accept that it is worth having. Second, for anything measured against a model or a
threshold, the test set is **frozen before the build**; a golden set assembled after delivery is
a set assembled to pass.

---

## 5. Deemed acceptance

Without a clock, acceptance is a veto held by whoever is busiest. With one, it is a process.

| Element | Default `[P]` | Note |
| --- | --- | --- |
| Review window | **5 business days** from written delivery notice | Milestone-based contracts commonly use a 5-business-day review window `[P]` |
| Trigger | A written delivery notice naming the milestone, the criteria and where to test | Verbal handover does not start the clock |
| Outcome if silent | Deemed accepted | Stated in the SOW at signature, never introduced later |
| Rejection requirement | In writing, citing **which criterion** failed and how | A rejection that cites no criterion is not a rejection |
| Re-delivery | New notice, new clock, half the original window for the re-test | Prevents an unbounded loop |
| Extension | One extension of up to 5 business days, on request, in writing | Grant it readily; it costs nothing and it buys the clause's legitimacy |

**How to introduce it without sounding like a lawyer.** Say what it is for:

> "We will send a short delivery note for each milestone saying what to test and where. If we
> have not heard back in five working days we will assume it is fine and move on — mostly so
> nothing sits waiting on someone's inbox. If anything fails, just tell us which criterion and
> we will fix it and re-send."

**Never invoke it silently.** On day 4, send a one-line reminder naming the deadline. Deeming a
milestone accepted without a reminder is technically clean and relationally expensive, and it is
the kind of thing a customer remembers at the renewal.

---

## 6. Disputed acceptance

| Situation | What it usually means | The move |
| --- | --- | --- |
| Rejected, citing a criterion that did fail | The system works as specified minus a defect | Fix, re-deliver, new clock. No change order |
| Rejected, citing something not in the criteria | The criteria were incomplete, or expectations moved | Say so plainly, accept the milestone against the written criteria, and raise the gap as a change order — same day, no argument about who was right |
| Rejected with no criterion cited | The acceptor cannot test, or is unhappy about something else | Ask which criterion, in writing. If none comes back in 3 days, escalate one level. This is a relationship signal, not a delivery signal |
| Silence past the window | The acceptor has disengaged or lacks the access to test | Reminder on day 4; on day 6 offer to run the test with them; escalate to the sponsor on day 8 before invoking the clause |
| Accepted verbally, never in writing | Nobody wants to be the one who signed | Send a summary email: "Confirming milestone 3 accepted on 14 March per criteria 3.1–3.3." Silence on that mail is the written record |
| Acceptor left the company | The commonest cause of a stranded milestone | Re-name the acceptor in writing within 5 days, re-issue the delivery notice, restart the clock |

**The rule that keeps disputes small: never bundle.** One milestone, one notice, one clock. A
bundled "phase 1 acceptance" covering nine deliverables gives the reviewer one thing to reject
and nine things to reject it for, and it strands all nine.

---

## 7. Criteria that never close

Each of these appears in real SOWs and none of them can be tested. The correction is the same
shape every time: name the data, the actor, the threshold and the acceptor.

| Non-criterion | Why it never closes | Replace with |
| --- | --- | --- |
| "Customer is satisfied" | Satisfaction is a mood, and it is measured after the invoice | A threshold on their data |
| "Works as expected" | Whose expectation, recorded where | The specified behaviour, with the number |
| "Successfully deployed" | Deployment is our task, not their outcome | Named users performing the named action in production |
| "Demo completed" | A demo is a performance by us | Their tester, their data, unaided |
| "Documentation delivered" | Delivered ≠ usable | Their engineer resolves a seeded failure using only the runbook |
| "Training completed" | Attendance is not capability | ≥70% of trained users perform the core action within 14 days |
| "Go-live" | A date, not a state | The activation event at cadence over two cycles |
| "Integration is live" | Live and working are different | 5 error-free days at production volume |
| "Data migrated" | Migrated and reconciled are different | Counts, control totals and a field-level sample |
| "Performance is acceptable" | Unenforceable in both directions | Stated volume, stated window, stated concurrency |
| "Model performs well" | No set, no threshold, no failure classes | Frozen golden set from their distribution, pre-agreed pass rate |
| "Sign-off from the team" | Teams do not sign | One named person and their role |

**Why the milestone stays open.** The reviewer has no stated basis on which to accept and none on
which to reject, so they do neither. The next milestone starts anyway because the schedule says
so, the invoice is not raised because finance needs the acceptance, and six weeks later nobody
can reconstruct whether it was done. The engagement then carries a growing tail of open
milestones, each of which is a small dispute waiting for a trigger — and the trigger is usually
the renewal.

---

## 8. Acceptance and the renewal

An unaccepted milestone is three problems wearing one label.

| Problem | Who feels it | When |
| --- | --- | --- |
| Unrecognised revenue | Finance | At period close, every period it stays open |
| An unproven value claim | The FDE and the CSM | At the business review, when the value case cites work nobody accepted |
| An open dispute | The sponsor | In the week they decide whether to renew |

**The scheduling rule (`R1`).** The last value-bearing milestone must be *accepted* before
`renewal_date − notice_period_days − evidence_window`, not merely delivered before it. Acceptance
takes a review window plus a re-delivery loop plus the acceptor's holiday, so budget 15 business
days between the last delivery and the last acceptance `[P]`.

**Hand acceptance state to the renewal skills.** `renewal-prep` and `churn-risk` should be told
about anything delivered-but-unaccepted for more than 30 days: it correlates with an acceptor who
has disengaged, and a disengaged acceptor inside the opt-out window is a finding regardless of
how green the usage data looks. What crosses to the customer is **never** the risk framing — the
firewall (`R18`) holds here as everywhere. Internally: *"milestone 4 unaccepted for 34 days,
acceptor unresponsive, opt-out in 51 days."* To the customer: *"Milestone 4 has been with you
since 12 March — can I run the test with you on Thursday so we can close it out?"*

---

## 9. Anti-patterns

| Anti-pattern | Correction |
| --- | --- |
| Criteria written after delivery | Written before build, attached to the SOW as an exhibit |
| Acceptance assigned to "the customer" | One named person and their role, per milestone |
| Acceptance assigned to an IT owner for a value milestone | IT accepts that it works; the business accepts that it is worth having |
| One bundled acceptance for a whole phase | One milestone, one notice, one clock |
| No deemed-acceptance window | An acceptance process with no clock is a veto |
| Invoking deemed acceptance silently | Reminder on day 4, offer to test together on day 6, escalate on day 8 |
| Rejection accepted with no criterion cited | Ask which criterion, in writing, within 3 days |
| A golden set assembled after delivery | Frozen before the build, drawn from their own distribution |
| Tracking "delivered" in the status report | Track `accepted_at` and the age of anything unaccepted |
| Re-delivery with no new clock | New notice, new clock, half window for the re-test |
| Acceptor leaves and the milestone sits | Re-name the acceptor within 5 days and re-issue the notice |
| Last milestone delivered just before the opt-out deadline | Accepted, not delivered, with 15 business days of headroom `[P]` |
