# The Paper Process

> Step 8 of `renewal-prep`. Procurement, legal, security, finance and signature — the
> workstreams that consume calendar time nobody budgeted. Missing these is the most common
> avoidable renewal slip, and the only one that is entirely within your control.

**Contents**
1. [The rule about lead times](#1-the-rule-about-lead-times)
2. [Workstream catalog](#2-workstream-catalog)
3. [Building the critical path](#3-building-the-critical-path)
4. [Measuring your own lead times](#4-measuring-your-own-lead-times)
5. [Security and vendor-risk re-review](#5-security-and-vendor-risk-re-review)
6. [Legal redlines](#6-legal-redlines)
7. [Procurement](#7-procurement)
8. [PO, budget and billing mechanics](#8-po-budget-and-billing-mechanics)
9. [The bridge extension](#9-the-bridge-extension)
10. [Gate checklists](#10-gate-checklists)
11. [What counts as a paper-movement event (C15)](#11-what-counts-as-a-paper-movement-event-c15)

---

## 1. The rule about lead times

**This library ships no default durations.** A vendor security review takes four days at one
customer and nine weeks at another; a PO is same-day at a 200-person company and three weeks
at a bank. A borrowed default does not reduce uncertainty, it hides it behind a number that
looks like a measurement — and someone will schedule against it.

| Situation | What to write |
| --- | --- |
| You measured it on this customer's last renewal | The measured value, with the date it was measured |
| You measured it across your last ten renewals in this segment | The median, with n and the segment |
| You have never measured it | `UNKNOWN — requires cycle time from prior renewals`, excluded from the critical path |
| The workstream is not required this cycle | `Not required — <evidence>`. Print the row; do not drop it |

When any serial workstream is UNKNOWN, the critical path is reported as a **floor**, never as
an estimate: "serial critical path ≥ 47 days (3 lead times unknown)". A floor that says
"at least" is honest. A total that quietly omits three workstreams is not.

---

## 2. Workstream catalog

Walk every row, every renewal. Classify each **required / not required / unknown** with the
evidence for the classification.

| # | Workstream | Chain | What triggers it | What it needs from you | Owner (ours) | Owner (theirs) |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Security / vendor-risk re-review | serial | Annual vendor review policy; any change of scope, sub-processor, region or data class | Security package, questionnaire responses, current certifications, pen-test summary, architecture diagram | Security / trust team | InfoSec, third-party risk |
| 2 | Privacy / DPIA / sub-processor approval | parallel | New sub-processor, new data category, new region, AI or model-training terms | Updated DPA, sub-processor list, transfer mechanism, retention schedule | Legal / privacy | DPO, privacy counsel |
| 3 | Legal redlines | serial | Any change to the MSA, SLA, liability cap, indemnity, term or termination clauses | Redline positions, fallback ladder, prior-cycle precedent | Legal / deal desk | Legal counsel |
| 4 | Order form issued and internally approved | serial | Agreed price, term and scope | Quote, discount approval at the right authority tier, billing entity | Deal desk | — |
| 5 | Customer signature routing | serial | Order form issued | Correct signer, correct entity, correct e-signature route | Renewal Manager | Signer, legal ops |
| 6 | Requisition → PO number | serial | PO-required customers | Quote, vendor number, cost centre, correct entity | Renewal Manager | Requester, budget owner, procurement |
| 7 | Procurement portal / supplier onboarding | parallel | First use of a portal, or a portal migration | Portal registration, catalogue entry, supplier profile refresh | Renewal Manager | Procurement ops |
| 8 | Vendor master, W-9 / W-8, bank verification | parallel | New entity, changed banking details, dormant supplier record | Tax forms, bank letter, callback verification | Finance | AP, supplier master |
| 9 | Insurance certificates (COI) | parallel | Contractual insurance requirements; annual refresh | Current certificates naming the correct insured entity | Finance / legal ops | Risk, procurement |
| 10 | Budget line confirmed for the new term | parallel | Every renewal | The number, early enough to land in their planning cycle | CSM + Renewal Manager | Budget owner, finance |
| 11 | Tax, entity and e-invoicing setup | parallel | Cross-border, entity change, e-invoicing mandates | VAT/GST identifiers, invoicing route, PO-on-invoice rules | Finance | AP |
| 12 | Accessibility / supplier-diversity documentation | parallel | Public sector, education, large enterprise programs | VPAT, diversity questionnaires, ESG forms | Compliance | Procurement |

**Serial** workstreams sit on the critical path in the order listed: a security clearance
usually gates legal sign-off, which gates the order form, which gates signature, which gates
the PO. **Parallel** workstreams do not gate each other, but each still needs its own runway
and any one of them can stop a signature on its own.

---

## 3. Building the critical path

Work **backwards from `D`** (the opt-out deadline), never forwards from today.

```
latest_start(last serial item)   = D − lead(last)
latest_start(previous item)      = latest_start(next) − lead(previous)
latest_start(parallel item)      = D − lead(item)
serial_critical_path             = Σ lead(serial items)
slack                            = (D − today) − serial_critical_path
```

`scripts/renewal_calendar.py --paper security_review=30,legal_redlines=21,...` does this and
flags every workstream whose latest start date has already passed.

| Slack | Reading | Action |
| --- | --- | --- |
| > 21 days | Healthy | Start the serial chain now; it costs nothing to be early |
| 0 to 21 days | Tight | No workstream may wait for another to "probably" finish. Start all parallel items today |
| < 0 days | **The renewal cannot close on this path** | Top line of the plan. Three options only: start today, parallelise with the customer's agreement, or open the bridge extension |

Negative slack is a finding, not a risk. It is arithmetic that has already happened. Report it
in the Bottom Line of the renewal plan, not in an appendix.

**Parallelising requires the customer's agreement**, because it usually means asking their
legal team to redline while security is still open, or asking procurement to pre-register the
supplier before terms are final. Both are normal requests; neither happens if you do not ask.

---

## 4. Measuring your own lead times

Do this once, then refresh quarterly. It takes about two hours and it is the highest-return
two hours in renewal operations.

**The ten-renewal audit.** Take your last ten closed renewals in each segment. For each,
recover these timestamps from email, the CRM and the contract record:

| Measure | From | To |
| --- | --- | --- |
| Security review | Questionnaire received | Written clearance |
| Legal redlines | First redline received | Final agreed text |
| Order form | Internal approval requested | Order form issued |
| Signature | Order form sent | Countersigned |
| PO | Requisition raised | PO number issued |
| Procurement onboarding | Portal invitation | Supplier active |
| Budget confirmation | Number first given to the budget owner | Line confirmed |

Record **median and 80th percentile** per segment, with n. Plan against the 80th percentile,
not the median: the median is what happens when nothing goes wrong, and the point of a
critical path is the case where something does.

| Output | Where it goes |
| --- | --- |
| Median and p80 per workstream per segment, with n | `.agents/cs-context.md` §13, refreshed quarterly |
| The single longest workstream | The thing to start first on every renewal, permanently |
| Any workstream with n < 5 | Keep as UNKNOWN. Five observations is not a distribution |

Where a customer has renewed before, **their** history beats your segment median. Use it.

---

## 5. Security and vendor-risk re-review

Ask at T-90, not at T-30: *"Do you re-run security or vendor risk review at renewal, or only
at first purchase?"* Many enterprises re-review annually and nobody tells the vendor, because
on their side it is routine.

**Have the pack assembled before you are asked.** Assembling it under time pressure is where
the weeks go.

| Item | Notes |
| --- | --- |
| Current certifications and audit reports | Check expiry dates — an expired report restarts the review |
| Completed standard questionnaires | Keep prior answers so responses stay consistent between cycles |
| Penetration test summary | Most reviews accept a summary; few need the full report |
| Architecture and data-flow diagram | Where data lives, who processes it, which regions |
| Sub-processor list | Any change since last cycle is the most common trigger for a new review |
| DPA and transfer mechanism | Current version, signed |
| Incident history and notification commitments | Answer before it is asked if there was an incident in the term |
| Business continuity and disaster recovery summary | |
| AI / model-training terms | Increasingly a separate review track with its own approver |

**Triggers that turn a routine re-review into a full one:** new sub-processor, new data
region, a change in data categories processed, an incident during the term, a new AI feature,
or a change in the customer's own compliance obligations. Any of these discovered at T-30 is
a bridge-extension conversation.

---

## 6. Legal redlines

| Term | Typical customer ask | Position |
| --- | --- | --- |
| Liability cap | Raise above fees paid | Trade against term length or prepayment; know your pre-approved ceiling before T-60 |
| Termination for convenience | Add, or shorten notice | **Never concede without VP+ approval.** It converts an annual contract into a monthly one |
| Notice window | Extend in their favour | Guard it. It is the mechanism that gives you a renewal cycle at all |
| Auto-renew clause | Remove | Guard it. Removing it makes every future term an affirmative sale |
| Uplift clause | Cap, index to CPI, or remove | Cap-and-collar is normal; removal is not. Trade a cap for term length |
| Audit / true-up rights | Remove | Guard it. Without it, entitlement drift is unrecoverable |
| Data deletion and return | Tighten timelines | Usually cheap to concede; check operational reality first |
| AI / model-training terms | Add restrictions | Have a standard position drafted before it is asked; drafting it live costs two weeks |
| MFN pricing | Add | Escalate. It constrains every future deal, not just this one |

**The four terms never traded without VP+ approval:** the notice window, the auto-renew
clause, the uplift clause, and audit/true-up rights. Each one determines your position at the
*next* renewal, which is why they are cheap to give and expensive to have given.

**Precedent is your fastest lever.** A redline already accepted with another customer of
similar size closes faster than a novel position, because it needs no new internal approval.
Keep the accepted-precedent list where the deal desk can find it.

---

## 7. Procurement

| Situation | Reading | Play |
| --- | --- | --- |
| Procurement appears at T-90 or earlier | Healthy | Give them everything at once: current pricing, usage and entitlement report, security package, insurance certificates, tax and entity data, and the MSA redlines already accepted elsewhere |
| Procurement appears inside T-30 | Late — a tactic, or an internal failure on their side | Expect a slip. Re-call to Most Likely at best and propose a 30–60 day extension at current terms to remove the artificial deadline |
| Vendor-consolidation or rationalisation program | Portfolio decision, not an account decision | Auto-flag At Risk. Executive sponsor required. Compete on switching cost, integration depth and data gravity — not on price |
| "We have quotes 30% lower" | Standard benchmarking tactic | Ask for a scope-normalised comparison. Reframe on total cost including migration, retraining and integration rebuild |
| "Send your best and final" at T-14 | Deadline squeeze | Best-and-final is conditional on a named signature date and a named get |
| A 24–48 hour expiring offer, from either side | Artificial urgency | Do not use it and do not respond to it. Anchor on the notice deadline, which is a real date |

**Ownership:** the Renewal Manager owns procurement; the CSM stays in the value conversation.
A CSM who negotiates price cannot be the customer's advocate at the next renewal.

**What procurement actually needs from you**, usually in this order: a scope-normalised price
comparison against the current term, a usage and entitlement report showing what is consumed,
a switching-cost statement, the security package, and clean paper. Four of those five you can
have ready at T-90 without being asked.

---

## 8. PO, budget and billing mechanics

| Item | The question to ask at T-90 | Why it slips |
| --- | --- | --- |
| PO required? | "Does this need a PO, and who raises it?" | Discovered at T-14, when the requester is on leave |
| Budget cycle | "When does the budget line for this get set, and is there a freeze window?" | A renewal landing three weeks after budgets lock becomes a downsell |
| Approval thresholds | "What dollar value changes who has to approve?" | An uplift crosses a threshold and adds an approver nobody planned for |
| Fiscal year boundary | "Does your fiscal year end between now and the renewal?" | Year-end freezes, purchase-order cutoffs and re-budgeting all cluster here |
| Entity and billing address | "Is the signing entity the same as last time?" | M&A and restructures change entities silently |
| Invoicing route | "Does the invoice go through a portal, and does it need the PO number on it?" | Invoices bounce, collections chase, and the relationship pays for it |
| Payment terms | "Are your standard terms changing?" | A Net 30 → Net 60 request late in the cycle is a concession you could have traded |

**Sequence the budget question early.** Confirming the budget line at T-120 is a
conversation; confirming it at T-30 is a negotiation, because by then the number is fixed and
anything above it has to displace something else.

---

## 9. The bridge extension

A short extension at current terms, typically 30–60 days, that moves the deadline without
changing the commercial position.

| Use it when | Do not use it when |
| --- | --- |
| The paper critical path cannot finish before `D` | The customer has not decided — an extension will not manufacture a decision |
| Procurement arrived late through no fault of the customer | You are using it to avoid a difficult conversation |
| A security or legal review is genuinely mid-flight | It would be the second extension. Two extensions is a save-play, not a paper problem |
| A budget cycle boundary falls badly | |

**Prepare it at T-45, offer it at T-14 if needed.** Pre-approved terms, a fixed end date, no
price change, and an explicit statement that the commercial terms already agreed carry over.
Asking for an extension at T-2 reads as panic; offering one at T-14 with the paperwork
already drafted reads as competence — and it is the same request.

---

## 10. Gate checklists

**At T-90 — the paper map is complete when you can answer all of these**

- [ ] Is a security or vendor-risk re-review required this cycle? Evidence for the answer
- [ ] Is a privacy/DPIA review required? Has anything changed in sub-processors, regions or data classes?
- [ ] Does the MSA need any change, and who raises it first
- [ ] Which legal entity signs, and has it changed
- [ ] Who signs, and what is their approval limit
- [ ] Is a PO required, who raises it, and how long did it take last time
- [ ] Which procurement portal, and is our supplier record current
- [ ] Are tax forms, bank details and insurance certificates current
- [ ] When is the budget line set, and is there a freeze window
- [ ] What is the measured lead time for every workstream above, or is it `UNKNOWN`

**At T-45 — the paper path is on track when**

- [ ] Every serial workstream has started or has slack against its latest start date
- [ ] Every parallel workstream has an owner on both sides and a date
- [ ] Order form issued with open items explicitly flagged rather than held
- [ ] Bridge extension drafted and pre-approved internally

**At T-14 — the close is clean when**

- [ ] Document is with the named signer, at the correct entity, on the correct e-signature route
- [ ] PO number attached, or written confirmation none is required
- [ ] Billing entity, tax identifiers and invoicing route validated by Finance
- [ ] Countersignature owner identified and available on the target date

---

## 11. What counts as a paper-movement event (C15)

**The Commit entry criterion for a renewal.** A verbal yes, an email saying "we're renewing" and
a champion's assurance are the same evidence — none. The gap between agreement and signature is
where renewals die, and it is the only stretch of the cycle in which everyone involved believes
the deal is already done. Before a renewal may be called Commit, **at least one of the five
events below must be on record with its date and its source.** Zero events caps the category at
Most Likely and prints the reason `C15 — verbal only, no paper movement`. `renewal-forecast`
applies the same entry criteria, so a renewal that fails here fails there.

Print all five rows every cycle, including the ones that are `no`. The empty rows are the ask
list for the next conversation.

| # | Qualifying event | What counts as evidence | What does **not** count |
| --- | --- | --- | --- |
| 1 | Security or vendor-risk re-review **started** | A questionnaire received, a portal task assigned to us, a dated request for the security package, a scheduled review call with their InfoSec team | "They said security usually reviews us in Q4"; a review we started internally with no request from them |
| 2 | Legal redlines returned, **or** written confirmation that there are none | A marked-up document, a redline summary email, or a written "no changes from our side" from counsel or the contract owner | A champion's belief that legal will not have comments; silence after we sent the MSA |
| 3 | PO requested or requisition raised | A PO number, a requisition ID, a screenshot or forward of the requisition, a procurement email asking for the quote in their format | "They're raising the PO this week"; our own internal quote |
| 4 | Vendor portal or supplier record created or refreshed | A portal invitation, a supplier-record confirmation, a tax-form or bank-verification request, a catalogue entry updated | Our own portal login from last year with no activity on it this cycle |
| 5 | Order form in **their** signature routing | An e-signature notification showing it sent to the signer, a forwarded routing confirmation, a dated note from their legal ops | An order form we issued and they have not acknowledged; "it's with the signer" with no artifact |

**Why these five.** Each one costs the customer something to do — a person's time, a system
record, an internal approval — and none of them happens by accident or out of politeness. That
is the entire test: an event nobody would perform unless a renewal were genuinely proceeding.
Enthusiasm is free, and free signals do not discriminate.

**The verbal-yes clock.** Where a verbal yes is logged, print the number of days since it with
no paper movement:

| Days since the verbal yes with no movement | What happens |
| --- | --- |
| 0–13 | Normal. Named next paper ask, with a date and an owner |
| 14 | Risk-register row opens, cause code `verbal_only`, owner named |
| 21 | Escalates to the Renewal Manager. Category capped at Most Likely |
| 30 | Treat the verbal yes as withdrawn for forecasting purposes and re-qualify Step 3 — something changed on their side that nobody told us about |

**The next action after a stalled verbal yes is always a paper-process ask, never another value
conversation.** The customer has already agreed on value; repeating the value case answers a
question nobody asked and hides the real blocker, which is almost always an approval nobody has
named. Ask the smallest concrete question that produces an artifact: *"Who raises the PO on your
side, and what do they need from us?"*

**Where a renewal genuinely requires no paper** — auto-renew on, no PO, no re-review, no order
form — that is itself a finding, evidenced with the clause and the prior cycle's record, and it
is written into the ledger as `Not required — <evidence>`. A renewal with no paper path is the
easiest one in the book and the one most likely to be discovered wrong at T-14.

**That is the one case that opens Commit with an empty ledger:** auto-renew already past a
*confirmed* notice window, where the contract is the paper that moved and the clause reference plus
the confirmed notice date is the evidence. Everything else — including a customer who "always
renews", and including auto-renew on an unverified notice period — needs a row with a date in it.

**Computing it.** `../scripts/renewal_calendar.py` takes the ledger as input and applies the cap, so the
entry criterion is arithmetic rather than a judgement made under deadline pressure:

```
python3 scripts/renewal_calendar.py --renewal-date 2026-11-01 --notice-days 30 \
    --paper-moved security_review=2026-08-20,po_requested=2026-08-25 \
    --verbal-yes 2026-08-01 --last-commercial-touch 2026-03-12
```

Valid event keys: `security_review`, `redlines_returned`, `po_requested`, `vendor_portal`,
`signature_routing`. An event key supplied without a date is rejected rather than accepted — an
event with no date is not evidence. With nothing supplied the script prints the five-row ledger
empty, `Commit entry REFUSED`, the capped ceiling, and the calendar ceiling it would otherwise have
allowed, so the gap between what the calendar permits and what the evidence supports is visible on
one line.

**Why a ledger and not a judgement call.** Every one of these five events is observable in a system,
dateable, and attributable to a named person on the customer's side. That is the whole point: the
question *"has this renewal actually started moving?"* stops being a matter of how the last call
felt and becomes a row that is either filled in or empty.
