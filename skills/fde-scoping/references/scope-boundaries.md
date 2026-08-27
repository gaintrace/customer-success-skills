# Scope Boundaries

> Where the line goes, how to say where it goes without sounding like a supplier defending a
> contract, and the two registers — dependencies and readiness — that decide whether the line
> holds once delivery starts.
>
> Evidence labels: `[M]` measured · `[V]` vendor research · `[P]` practitioner rule ·
> `[A]` academic. A `[P]` threshold is a default this library holds, not a benchmark. Never
> present one as a measured figure.

**Contents**
1. [The problem statement](#1-the-problem-statement)
2. [The definition of done](#2-the-definition-of-done)
3. [The exclusion taxonomy — twelve categories](#3-the-exclusion-taxonomy--twelve-categories)
4. [How to phrase an exclusion](#4-how-to-phrase-an-exclusion)
5. [Boundary decision tests](#5-boundary-decision-tests)
6. [Customer-side dependencies](#6-customer-side-dependencies)
7. [Pilot vs production](#7-pilot-vs-production)
8. [The kickoff-readiness gate](#8-the-kickoff-readiness-gate)
9. [Anti-patterns](#9-anti-patterns)

---

## 1. The problem statement

Three parts. A SOW missing any one of them cannot be enforced, because there is nothing to test
a deliverable against.

| Part | Field | Test it must pass |
| --- | --- | --- |
| Their problem, in their words | `problem_quote`, `quote_source`, `quote_author`, `quote_date` | A named person said it, on a dated call or in writing. A paraphrase fails |
| The measurable current state | `metric_name`, `baseline_value`, `unit`, `period`, `baseline_source`, `measurement_owner_customer` | A number the customer would recognise as theirs, with an owner on their side |
| The definition of done | `end_state`, `cadence`, `performed_by`, `measured_against` | §2 below |

### The discovery questions that produce it

Ask one, then stop talking (`R16` — three questions per call, not ten).

| # | Question | What it produces | The tell that you have it |
| --- | --- | --- | --- |
| 1 | "Walk me through the last time this went wrong. What did it cost you?" | The problem in their words plus an anchor number | They name a week, a person and a consequence |
| 2 | "How would you know, six months from now, that this was worth doing?" | The definition of done, in their frame | They name a metric before they name a feature |
| 3 | "What number do you report on this today, and where does it come from?" | The baseline, its source and its owner | They can name the report and who runs it |
| 4 | "Who has to change how they work for this to land?" | The adoption population — and usually a dependency | They name teams, not systems |
| 5 | "What did you try before this?" | The failure mode to design around | They describe a previous project, not a product |

### When the baseline does not exist

Not a reason to stop; a reason to change what you are scoping. Emit **Milestone 0 — Baseline
Capture** instead of the build scope.

| Field | Example |
| --- | --- |
| `metric_name` | Hours from invoice receipt to approved-for-payment |
| `definition` | Median across all supplier invoices, excluding disputed |
| `measurement_window` | Four consecutive weeks, ending before any configuration change |
| `instrument` | Their ERP audit log export, weekly, or a 40-invoice hand sample if the log is unavailable |
| `measurement_owner_customer` | Named person on their finance ops team, agreed by their controller |
| `date` | The date the four weeks close, which is the earliest possible SOW start |

Typical cost: five to ten working days `[P]`. If they will not fund or staff it, write one line
into the risk register — *"No pre-change baseline exists; the value claim at the review will rest
on the customer's own recollection of the current state"* — and scope the build anyway. That is a
stated risk, not a refusal. `value-case` handles reconstruction afterwards, at lower confidence.

---

## 2. The definition of done

"Done" is not a date and not a demo. Four fields, and each of them is testable.

| Field | Good | Fails as |
| --- | --- | --- |
| **End state** | Approved invoices post to the ERP without a human touching the approval queue | "The integration is live" |
| **Cadence** | Every business day, across at least two full weekly cycles | "It worked in the demo" |
| **Performed by** | Their AP team of six, in production, on their own logins | "Our engineer ran it" |
| **Measured against** | Median approval time, against the four-week baseline of 31 hours | "Everyone is happy with it" |

**The vendor-done / customer-done split.** Vendor-done is our task list complete. Customer-done is
their outcome occurring at cadence, performed by their people, measured against their baseline.
A SOW that only defines vendor-done delivers on time and gets challenged at the first review; the
gap between the two dates is the number `onboarding-plan` calls the Success Gap. State both.

---

## 3. The exclusion taxonomy — twelve categories

**The first seven are mandatory in every SOW, including where they do not apply.** Print
"Not applicable — this engagement has no data migration" as a row. A deleted row is
indistinguishable from an oversight six weeks later, and it is the oversight the customer will
assume.

| # | Category | Default boundary | The request that arrives | Cost if unstated |
| --- | --- | --- | --- | --- |
| 1 | **Data cleanup and remediation** | Records taken as they stand on the agreed extract date; the field mapping is fixed in an appendix | "Can you dedupe while you're in there?" | Unbounded. The commonest overrun, and invisible until the first load |
| 2 | **Changes to third-party systems** | We configure our side and supply the exact change list; their admin executes changes inside their CRM, IdP, warehouse or ERP | "Just add the field for us" | Their change process, their queue, their outage window — none of which you control (`R19`) |
| 3 | **Training beyond N sessions** | N sessions of stated length for stated audiences, delivered once | "Can we do one more for the new starters?" | Recurs forever; staff turn over and the request never closes |
| 4 | **Custom UI / bespoke front-end** | Configuration of supplied interfaces only | "Could it look like our portal?" | Permanent maintenance liability, and it breaks on every upgrade. Route to `custom-vs-product` |
| 5 | **Historical migration beyond N months** | N months migrated; older data quoted separately | "While we're at it, bring across the archive" | Doubles a migration and gets agreed in a corridor |
| 6 | **Environments beyond the stated set** | One non-production plus one production | "Can we have a UAT tenant too?" | A full configuration, a full test pass and permanent drift per environment |
| 7 | **Support of customer-authored code** | The documented extension points are supported; their scripts, jobs and partner-written integrations are theirs | "Our script broke after your release" | On call for code you cannot read and did not review |
| 8 | **Performance beyond the stated envelope** | Named peak volume, concurrency and latency target | "It's slow now that we've turned on all regions" | Re-architecture priced as a bug fix |
| 9 | **Anything requiring a vendor we do not contract with** | Named third parties only | "Can you get their API turned on?" | You take responsibility for a queue you cannot join |
| 10 | **Production on-call and incident response** | Support runs to the published SLA; named-engineer on-call is separate | "Can you be on the bridge Saturday?" | Unbounded, unstaffed, and it becomes the expectation |
| 11 | **Regulatory certification or attestation** | We supply evidence about our product; certifying their deployment is theirs or their auditor's | "Can you sign this attestation?" | Liability far exceeding the fee |
| 12 | **Rollback of customer-made changes** | We restore to the agreed configuration; diagnosing changes made outside it is chargeable | "It broke after someone changed something" | Unpaid forensics on a system you no longer recognise |

### Where the category boundary sits — the defaults

Each of these appears as a number in the SOW. Set it deliberately; a blank is read as "unlimited".

| Boundary | Default `[P]` | Raise it when | Lower it when |
| --- | --- | --- | --- |
| Training sessions | 2 admin + 2 end-user | Multi-region rollout, or >100 seats | Tech-touch, or the product ships in-app enablement |
| Historical migration | 12 months | A regulated retention obligation names longer | Reporting only needs the current period |
| Environments | 1 non-prod + 1 prod | Regulated change control mandates UAT | Single-team pilot |
| Integrations | The named list, no substitutions | — | Always name them; "their stack" is not a list |
| Volume envelope | 2× the stated peak | Known seasonal spike | Consumption pricing already caps it |
| Concurrent users | Provisioned seats | — | — |
| Named custom components | Zero, unless listed with an owner and a sunset date | `custom-vs-product` returned build | — |

---

## 4. How to phrase an exclusion

**Never a bare negative.** A bare negative reads as a supplier protecting itself, and it invites
the customer to test the line rather than accept it. Every exclusion has three parts:

```
<what IS included, specifically>  ·  <where the line falls>  ·  <how the other side gets done>
```

| Category | Hostile | Right |
| --- | --- | --- |
| Data cleanup | "Data cleanup is not included." | "We load the records as they stand in your Salesforce on the agreed extract date, using the mapping in Appendix B. Where records are duplicated or missing an owner, your admin resolves those — we will send the exact list within three days of the first load, and we can quote the cleanup separately if you would rather we did it." |
| Third-party changes | "Changes to customer systems are out of scope." | "We configure everything on our side. The two Salesforce fields this needs are listed in Appendix C — your admin creates them, and we will be on the call while it happens." |
| Training | "Only 2 sessions included." | "Two admin sessions and two end-user sessions, recorded so new starters can watch them later. If you would like live sessions for later cohorts, we run those as a separate half-day." |
| Custom UI | "No custom UI." | "You get the standard console, configured with your fields and your naming. A branded embedded view is a different piece of work — worth talking about once you have seen how the team uses the standard one." |
| Migration depth | "Only 12 months of history." | "Twelve months comes across, which covers your current reporting year. The archive is a straightforward add-on and we can price it once you have decided whether the reports need it." |
| Customer code | "We don't support customer code." | "We support everything we build and the documented extension points. Scripts your team writes stay yours — we will review them on request and we will tell you before any release that changes an interface you depend on." |

**Three tone rules.** Write exclusions in the same register as the rest of the SOW, not in legal
voice — a paragraph that changes register signals that you expect a fight. Put the exclusions
*before* the fee, not in an appendix after it. And say them out loud on the scoping call: an
exclusion the sponsor heard is agreed, and an exclusion they read in clause 7.3 is a surprise.

**The one exclusion to state twice.** Whichever category this customer has already asked about
informally goes in the SOW *and* in the covering note. It is the one that will come back.

---

## 5. Boundary decision tests

When a request sits on the line, run these in order and stop at the first that answers.

| # | Test | If yes |
| --- | --- | --- |
| 1 | Is it required for the defined outcome to occur at cadence? | In scope. Anything the outcome depends on is in scope by definition, or the outcome is not deliverable |
| 2 | Does it live inside a system we do not control? | Dependency, not scope. Owner, date, slip consequence (`R19`) |
| 3 | Would a second customer want the identical thing? | Route to `custom-vs-product` before agreeing it — the answer changes what you build, not just what you charge |
| 4 | Does it create something someone must maintain after we leave? | In scope only with a named owner and a sunset review date recorded at creation |
| 5 | Is it bounded — can you name what "finished" looks like? | If not, it cannot be in scope at a fixed fee. Move it to T&M or exclude it |
| 6 | Is it under the Step 8 absorb threshold and non-recurring? | Absorb and log it in the creep ledger |
| 7 | Anything else | Out of scope, phrased per §4, with the route to buying it |

**The recurrence test.** A one-off favour and a recurring obligation look identical the first
time. Ask: if this request arrived monthly, would we still absorb it? If no, it is a change order
now, while it is small and nobody is annoyed — not in month four, when it is a pattern.

---

## 6. Customer-side dependencies

Most implementation failures are organisational, not technical `[P]`: no customer-side
engineering capacity, competing priorities, an unnamed data owner. None of those appear on a
milestone chart. All of them appear in this register.

| Category | Typical items | Lead time `[P]` | The failure signature |
| --- | --- | --- | --- |
| **Access and credentials** | VPC/network access, SSO app registration, service account, API key, IP allow-list | 2–6 weeks in enterprise; longer in regulated | Requested at kickoff instead of before it |
| **Data** | Sample extract, schema documentation, PII classification, residency decision, retention rules | 1–3 weeks | The sample is synthetic and nothing like production |
| **People** | Named data owner, named tester, named approver, named admin (two, never one) | Immediate to name, weeks to free up | One person named for all four roles |
| **Environment** | Sandbox provisioned, firewall rules, load balancer, DNS, certificate | 1–4 weeks | Provisioned but not reachable from where we work |
| **Decisions** | Field mapping sign-off, taxonomy, naming convention, error-handling policy | Days, if the decider is identified | Nobody has been asked, so nobody is late |
| **Commercial** | PO raised, DPA executed, security review, vendor onboarding | 3–12 weeks; regulated verticals longer | Started after signature rather than before |
| **Third party** | Their other vendor's API access, their SI's availability, their auditor's window | Unbounded — you cannot escalate | Treated as ours to chase |

### Register columns

`# · dependency · owner (named person, customer side) · owner's manager · needed by · what it
blocks · consequence of slip · escalation contact · status · last chased`

**Default consequence, printed in the SOW:** a day-for-day slip of every downstream milestone,
with the fee unchanged. Absorbing the slip silently is how a fixed-fee engagement loses its
margin without a single change order being raised.

### The capacity line

One line that prevents more overruns than any other in the document:

> *"This plan assumes N hours per week of <named customer engineer>'s time between <date> and
> <date>, agreed with <their manager> on <date>."*

Without it you have priced someone else's availability at zero. If it cannot be agreed, mark
`UNKNOWN — requires confirmation from <manager>` and treat every dependent date as a floor rather
than a commitment.

### Single-threading (`R5`)

Count distinct named customer owners across the register. One owner across all categories is a
single-threaded engagement: one resignation, one reorganisation or one holiday away from a stop.
Print the exposure, request a named backup for the top three dependencies before signature, and
if none is given, say what happens instead — usually that those dates become estimates.

### Escalation ladder

| Days past due | Move | Who |
| --- | --- | --- |
| 0 | Written note in the shared channel naming the blocked milestone | Delivery lead |
| 3 | Direct message to the owner offering to do the part we can do | Delivery lead |
| 5 | Email to the owner's manager, copying our sponsor, stating the slip in days | Delivery lead |
| 10 | Sponsor-to-sponsor, with the revised date and the choice being made | Our exec sponsor (`exec-escalation-comms`) |
| 15 | Schedule change order issued; work re-sequenced or paused | Delivery lead + commercial approver |

Escalate on the schedule, not on the mood. An escalation that arrives at day 15 with no prior
written trace reads as an ambush; one that arrives on day 5 as the third step of a stated ladder
reads as professionalism.

---

## 7. Pilot vs production

A pilot answers one question. A production deployment runs a workflow every day. Scoping them
identically produces a pilot that succeeds and converts to nothing.

Directional context, not a benchmark: the 2025 MIT Media Lab / Project NANDA *GenAI Divide*
study — 52 executive interviews, 153 survey responses, 300 public deployments, and publicly
challenged on representativeness — reported roughly 5% of evaluated custom or vendor-built
enterprise AI systems reaching production `[V]`.

| | **Pilot** | **Production** |
| --- | --- | --- |
| Purpose | Answer one question, either way | Run the workflow at cadence |
| Success | The question answered — a "no" is a successful pilot | Adoption at cadence by named users, measured against baseline |
| Data | Sampled or masked, if it is representative | Real data, real volume, real edge cases |
| Environment | Sandbox | Production with a rollback path |
| Acceptance | A measurement against a threshold agreed before the build | Sustained production use over a stated window |
| Users | A named handful | The full population, with enablement |
| Exclusions | Everything except the question | Named per §3 category |
| Commercial | Small fixed fee, or at our cost with the conversion terms written | Capped T&M or fixed fee |
| Duration | 2–6 weeks `[P]` | Per the estimate |

**The four clauses a pilot SOW must carry, at pilot signature and not later:**

1. **The question, in falsifiable form.** "Can the model classify these invoices at ≥92% accuracy
   against a 500-record golden set drawn from your own last quarter?" — not "evaluate the fit".
2. **The go/no-go criteria**, with the threshold and who measures it.
3. **The named production owner and the production budget line.** A pilot with no budget line
   behind it is an unfunded evaluation, and it converts at the rate unfunded evaluations convert.
4. **The conversion path** — what happens on a "yes" (dates, shape, next SOW) and what happens on
   a "no" (data returned or deleted, environment decommissioned, no obligation either side).

**Pilot scope discipline.** Only what answers the question is in scope. SSO, historical
migration, custom reporting, integrations beyond the one under test and end-user enablement are
all excluded from a pilot by default — and the exclusion is easy to phrase, because their absence
is the point: *"The pilot runs on a sampled extract so we can answer the accuracy question in
three weeks rather than three months. Everything about the production shape — SSO, the full
history, your reporting — belongs to the deployment SOW, and we will scope it while the pilot runs
so there is no gap."*

---

## 8. The kickoff-readiness gate

Ten binary items, scored before the kickoff invitation goes out. **Below 8, the kickoff moves and
the reason is written down.** A kickoff held on a red gate spends the sponsor's goodwill on a
meeting that turns into discovery, and the second kickoff never gets the same attendance.

| # | Item | Evidence that satisfies it | Commonly fails because |
| --- | --- | --- | --- |
| 1 | Problem statement with a measurable current state | A number, its source, its owner, agreed in writing | Nobody asked for the number |
| 2 | Definition of done agreed | §2's four fields, confirmed by the sponsor | "Go-live" was accepted as an answer |
| 3 | Out-of-scope acknowledged | Their commercial owner has replied to the SOW naming the exclusions | Exclusions sat in an appendix nobody opened |
| 4 | Every milestone has acceptance criteria and a named acceptor | The milestone table, with names in the acceptor column | Acceptance was left to "the team" |
| 5 | Every dependency has a named customer-side owner and a date | The register, with no blank owner cells | Owners named as teams, not people |
| 6 | Customer engineering hours confirmed | The manager who controls that time has agreed it in writing | Assumed from an engineer's enthusiasm |
| 7 | Access **requested** | A ticket number and an ETA — not access granted, just requested | Left until week one |
| 8 | Security review / DPA / residency path started | A date and a named reviewer on their side | Treated as paperwork rather than a milestone |
| 9 | PO raised or payment path stated | PO number, or the named route and its owner | Procurement engaged after signature |
| 10 | Executive sponsor named both sides, and has read the plan | A reply from the sponsor, not a forward | Sponsor is a name on a slide |

**Gate on the long-lead items first — 7, 8 and 9.** They take weeks, sit outside our control
(`R19`), and cannot be compressed by working harder. Starting them at kickoff instead of before
it is the single commonest reason a six-week engagement takes five months.

**Scoring and what to do with it**

| Score | Read | Action |
| --- | --- | --- |
| 10 | Ready | Kick off |
| 8–9 | Ready with named gaps | Kick off; the open items appear on the kickoff agenda with owners and dates |
| 5–7 | Not ready | Move kickoff. Run a 30-minute readiness call instead, close items 1–6, then re-score |
| ≤4 | Nothing to kick off | Return to scoping. Kicking off here manufactures a slip that will be attributed to delivery |

---

## 9. Anti-patterns

| Anti-pattern | Correction |
| --- | --- |
| Problem statement written from the sales deck | It must contain a sentence the customer said, attributed and dated |
| "The current process takes too long" | A number, a unit, a period, a source and an owner — or Milestone 0 |
| Exclusions in an appendix after the fee | Before the fee, and said out loud on the call |
| A single catch-all exclusion clause | Twelve categories, seven of them mandatory, each with its boundary number |
| Bare negatives | Inclusion + boundary + route (§4) |
| Boundary numbers left blank | A blank reads as unlimited. State N sessions, N months, N environments |
| Dependencies written as prose caveats | The register, with named people and slip consequences |
| Dependency owner recorded as a team | Teams do not miss deadlines; people do. Name the person and their manager |
| Customer engineering time assumed | The capacity line, agreed by the manager who controls it |
| Escalating only when frustrated | The stated ladder, on the stated days |
| Pilot scoped like a small production deployment | One question, sampled data, and the four conversion clauses |
| Pilot with no production budget line | An unfunded evaluation. Name the owner and the line at pilot signature |
| Kickoff booked because the sponsor is free that week | Score the gate first. Below 8, move it and say why |
| Access, PO and security review started at kickoff | They are the long-lead items. They start before the gate is scored |
