# Statement of Work — template

> **This is a customer-facing document.** Nothing internal belongs in it: no three-point estimate
> or σ, no contingency percentage, no loaded cost, margin or utilisation, no kickoff-gate score,
> no creep ledger, no assessment of their engineering capacity or of any named person, no opt-out
> deadline, no ARR, no risk or health language (`R18`).
>
> **Fill every `<slot>` or delete the sentence that needed it.** A SOW containing `<date>` is not
> a SOW; it is a draft that looked finished. Anything genuinely unavailable is raised in the
> internal artifact as `UNKNOWN — requires X`, never left as a placeholder here.
>
> Order matters: exclusions come **before** the fee, and section 3 is read aloud on the scoping
> call. An exclusion the sponsor heard is agreed; one they read in an appendix is a surprise.

---

# Statement of Work
**<Vendor legal entity>** and **<Customer legal entity>**
SOW reference **<SOW-nnn>** · under **<MSA reference and date>** · issued **<date>**

| | |
|---|---|
| Engagement | <engagement name> |
| Vendor delivery owner | <name, title, email> |
| Customer delivery owner | <name, title, email> |
| Customer commercial approver | <name, title> |
| Executive sponsors | <vendor name, title> · <customer name, title> |
| Planned start · planned completion | <date> · <date> |
| Commercial shape | <capped time and materials against accepted milestones / fixed fee / time and materials / included in subscription> |

---

## 1. Why we are doing this

<One paragraph, in their language, opening with the problem as they described it.>

> "<direct quote>"
> — <name>, <title>, <date>, <source: scoping call / email / workshop>

**Where things stand today.** <Metric> is currently **<value> <unit> per <period>**, measured from
<source> over <window>. <Named customer person, title> owns that measurement and will re-measure
it at the points set out in section 4.

**What done looks like.** <Observable end state>, occurring <cadence>, performed by <who>,
measured against the figure above.

---

## 2. What we will deliver

| # | Deliverable | What it does for you | Milestone |
|---|---|---|---|
| 1 | <deliverable> | <outcome in their language, not features> | M<n> |
| 2 | | | |
| 3 | | | |

**Volume and scale this is built for:** <peak volume>, <concurrency>, <retention/history depth>,
<regions/environments>.

**Named integrations:** <exact list — never "your stack">.

---

## 3. What is not included

Everything below is deliberately outside this SOW so the timeline and the fee are dependable.
None of it is off the table — each line says how it gets done if you want it.

| # | Area | What we do | Where the line falls | How the other side gets done |
|---|---|---|---|---|
| 1 | Data cleanup | Load your records as they stand on the agreed extract date, using the mapping in Appendix B | Duplicated, conflicting or owner-less records are not remediated | Your admin resolves them; we send the exact list within 3 days of the first load, and we can quote the cleanup separately |
| 2 | Changes inside your other systems | Configure everything on our side and supply the precise change list | Changes inside <CRM / IdP / warehouse / ERP> are made by your team | Your admin executes them; we join the call while it happens |
| 3 | Training | <N> admin sessions and <N> end-user sessions of <length>, recorded | Additional cohorts and repeat sessions | Booked as a separate half-day at any point |
| 4 | Interface | Configure the standard console with your fields and naming | New screens, branded portals and embedded views | Scoped separately once you have seen the team use the standard one |
| 5 | Historical data | Migrate <N> months of history | Anything older | Quoted as an add-on once you have decided whether the reports need it |
| 6 | Environments | One non-production and one production environment | Further tenants, regions or DR environments | Quoted per environment |
| 7 | Code your team writes | Support everything we build and the documented extension points | Scripts, jobs and partner-written integrations you author | Yours to maintain; we review on request and warn you before any release that changes an interface you depend on |
| 8 | Performance beyond the stated envelope | Build for the volumes in section 2 | Sustained load beyond them | Re-scoped when you need it |
| 9 | Third parties we do not contract with | Work with <named third parties only> | Obtaining access or changes from others | You hold the relationship; we will supply whatever technical detail helps |
| 10 | Production on-call | Support to the published service levels | Named-engineer standby outside those hours | Available as a separate retainer |
| 11 | Regulatory attestation | Provide evidence about our product and its controls | Certifying your deployment | Your auditor, with our full support |
| 12 | Changes made outside the agreed configuration | Restore to the agreed configuration | Diagnosing changes made outside it | Chargeable at the rates in section 8 |

*Delete no row. Where a category does not apply, write "Not applicable — this engagement includes
no <migration / third-party integration / …>".*

---

## 4. Milestones and how they are accepted

A milestone closes when the named person below confirms the acceptance criterion is met.

| M | Milestone | Acceptance criterion | Who tests | Who accepts | Target date |
|---|---|---|---|---|---|
| 1 | <name> | Given <their data/condition>, when <tester> performs <action> in <environment>, the result is <threshold> | <name, title> | <name, title> | <date> |
| 2 | | | | | |
| 3 | | | | | |

**How acceptance works.** We send a short delivery note for each milestone saying what to test and
where. If we have not heard back within **<5> working days** the milestone is treated as accepted,
mostly so nothing sits waiting in an inbox. If something does not meet a criterion, tell us which
one and we will fix it and re-send. Need longer? Ask and we will extend once, by up to five
working days.

---

## 5. What we need from you

These are the things only your team can do. Each one blocks the work named beside it, so if a date
moves, the milestones behind it move by the same number of days.

| # | What we need | Your owner | Needed by | What it blocks | If it slips |
|---|---|---|---|---|---|
| 1 | <service account / VPC access / SSO registration> | <name, title> | <date> | M<n> | M<n> and everything after it move day for day |
| 2 | <sample extract and schema documentation> | <name, title> | <date> | M<n> | " |
| 3 | <field mapping sign-off> | <name, title> | <date> | M<n> | " |
| 4 | <named tester and named acceptor available> | <name, title> | <date> | M<n> | " |
| 5 | <PO / DPA / security review> | <name, title> | <date> | Start | " |

**Your team's time.** This plan assumes **<N> hours per week** of <name, title> between <date> and
<date>, agreed with <manager name> on <date>. If that changes, tell us early — it is the single
thing most likely to move the finish date.

**Escalation.** If something is stuck, we will say so in writing the day it is due, again after
three days, and raise it to <customer sponsor name> after five. Nothing will be a surprise.

---

## 6. What we are assuming

If any of these turns out differently, we will tell you within two working days, with what it
changes and what the options are.

| # | Assumption | If it turns out otherwise |
|---|---|---|
| 1 | <e.g. the ERP extract matches the sample shared on <date>> | <e.g. mapping work increases by around a week; we would come back with options before doing anything> |
| 2 | | |
| 3 | | |

---

## 7. Changing the scope

Things change, and asking is not a problem. This is simply how we keep the dates honest.

- Anything small — under **<N> hours** — we absorb and note it, so you can see the running total.
- Anything larger, or anything that changes a deliverable or an acceptance criterion, we write up
  as a one-page change order the same day, with the effort, the fee effect and which dates move.
- Change orders under <value> are agreed between <vendor delivery owner> and <customer delivery
  owner>; above it, <customer commercial approver> signs.
- If a date moves because something on your side is waiting, we issue a schedule note — dates
  only, no change to the fee — so the record is clear for both of us.

---

## 8. Fees and payment

| | |
|---|---|
| Shape | <capped time and materials against accepted milestones / fixed fee / T&M> |
| <Ceiling / Fixed fee> | **<currency amount>** |
| Rates (for changes and for work beyond the ceiling) | <role: rate> · <role: rate> |
| Invoicing | On acceptance of each milestone, per the schedule below |
| Expenses | <policy; pre-approved in writing, at cost> |
| Payment terms | <N> days from invoice date |

| Milestone | Amount | Invoiced on |
|---|---|---|
| M1 | <amount> | Acceptance of M1 |
| M2 | <amount> | Acceptance of M2 |

*Where the shape is capped time and materials: we bill actual hours to the ceiling above and will
never exceed it without a signed change order. If we come in under, you pay the lower figure.*

---

## 9. Agreed

| | Vendor | Customer |
|---|---|---|
| Name | <name> | <name> |
| Title | <title> | <title> |
| Date | <date> | <date> |

---

## Appendix A — Environments and access

<Environment names, URLs, identity path, who has access to what.>

## Appendix B — Field mapping

<Source field → target field, transformation, owner of the decision.>

## Appendix C — Changes required in your systems

<Exact list, per system, with the person on your side who will make each one.>
