# MEDDPICC-R — MEDDPICC Adapted to Renewals

> The qualification layer for Step 3 of `renewal-prep`. Read before scoring a renewal, and
> again before any Commit call. Nine elements, scored 0/1/2, 18 points, three hard gates.

**Contents**
1. [Why renewals need their own version](#1-why-renewals-need-their-own-version)
2. [The nine elements](#2-the-nine-elements)
3. [Scoring, gates and forecast mapping](#3-scoring-gates-and-forecast-mapping)
4. [The question bank](#4-the-question-bank)
5. [False twos — how scores get inflated](#5-false-twos--how-scores-get-inflated)
6. [Worked example](#6-worked-example)
7. [Mapping the decision process](#7-mapping-the-decision-process)
8. [Source notes](#8-source-notes)

---

## 1. Why renewals need their own version

MEDDPICC was built for new business. The canonical eight elements are Metrics, Economic Buyer,
Decision Criteria, Decision Process, Paper Process, Implicate the Pain, Champion and
Competition — with Paper Process defined as "the series of steps that follow the Decision
Process in how you will go from Decision to signature", the phase where "most deals get lost"
(MEDDICC, meddicc.com, accessed 2026).

Four things change when the customer already owns the product:

| Change | Consequence for qualification |
| --- | --- |
| The pain may already be solved | "Identify Pain" becomes *is the pain still owned by someone who feels it?* A solved pain with a departed owner is not a reason to renew. |
| Metrics are provable, not projected | You are no longer selling a forecast. You are producing evidence — and if you cannot, you are negotiating on price alone. |
| The paper process has a **deadline the contract sets** | Paper Process absorbs the notice window. A renewal whose notice deadline is unknown is unforecastable at any score. |
| "Do nothing" means cancellation, not delay | In new business, no decision means the status quo. In a renewal, no decision inside the notice window can mean the contract lapses. Competition must include do-nothing, in-house build, and consolidation into a suite the customer already owns. |

One element is added: **V — Value Realised**, which asks whether the product is embedded
deeply enough that stopping is expensive. Metrics is what the customer *got*. Value Realised
is what it would *cost them to stop*. Renewals turn on the second more often than the first.

---

## 2. The nine elements

Scoring for every element: **0 = unknown · 1 = asserted · 2 = evidenced by an artifact.**
An artifact is something a third party could open: a logged meeting, an email, a document, a
contract clause, a system field with a date. A rep's confidence is a 1, permanently.

### M — Metrics

| | |
| --- | --- |
| **Renewal question** | What did they buy this for, and can we show it happened in *their* numbers? |
| **Artifact for 2/2** | A written, customer-acknowledged outcome or ROI summary dated within 12 months, in the customer's metrics |
| **1/2 looks like** | Our usage dashboard, our savings estimate, our case-study language |
| **Disqualifier** | No agreed metrics ⇒ you are negotiating on price only, and procurement will win that |
| **Gates** | Commit |

### E — Economic Buyer

| | |
| --- | --- |
| **Renewal question** | Who owns the budget line *this fiscal year*, and when did we last have a business conversation with them? |
| **Artifact for 2/2** | A logged meeting with the economic buyer within 90 days |
| **1/2 looks like** | The champion says they will handle it; the EB is on the org chart but not in any interaction record |
| **Disqualifier** | EB not identified, or last contact >90 days |
| **Gates** | **Commit is impossible without EB contact.** Hard gate. |

The budget owner changes more often than the org chart does. Re-verify at T-180 and again at
T-90; a reorg between them is normal, not exceptional.

### D — Decision Criteria

| | |
| --- | --- |
| **Renewal question** | On what basis will they decide to continue — and has "consolidate" or "do nothing" become a real option since last time? |
| **Artifact for 2/2** | A written criteria list, in their words, with the person who stated it and the date |
| **1/2 looks like** | "They're happy with us" |
| **Disqualifier** | Criteria unknown at T-90 |
| **Gates** | Commit |

### D — Decision Process

| | |
| --- | --- |
| **Renewal question** | Who else must approve — IT, security, finance, data privacy, procurement? Is there a vendor-consolidation review in flight? |
| **Artifact for 2/2** | A mapped approval chain with names, steps and expected durations |
| **1/2 looks like** | "It goes to procurement" |
| **Disqualifier** | Process unknown at T-90 |
| **Gates** | Commit |

### P — Paper Process

| | |
| --- | --- |
| **Renewal question** | Notice window date · auto-renew status · signing entity · PO required · legal re-review · security re-review · expected cycle time for each |
| **Artifact for 2/2** | Contract clause references **plus** a dated paper plan with owners on both sides (see `paper-process.md`) |
| **1/2 looks like** | The renewal date from the CRM and an assumption that last year's process repeats |
| **Disqualifier** | **Notice window unknown ⇒ the renewal is unforecastable.** No category above At Risk. |
| **Gates** | **All categories above At Risk.** Hard gate. |

### I — Identified Pain

| | |
| --- | --- |
| **Renewal question** | What breaks for them if they stop, and does the person who feels it still work there? |
| **Artifact for 2/2** | A named consequence with a named owner who has stated it |
| **1/2 looks like** | A pain statement from the original sales cycle, three years old |
| **Disqualifier** | Pain owner departed and not replaced |
| **Gates** | Most Likely |

### C — Champion

| | |
| --- | --- |
| **Renewal question** | Still employed, still in the role, still willing to advocate — and have we tested that? |
| **Artifact for 2/2** | The champion took an internal action on our behalf: booked the EB, forwarded the business case, chased procurement, defended the line item |
| **1/2 looks like** | Someone who replies to our emails warmly and has never done anything internally |
| **Disqualifier** | Champion untested or departed |
| **Gates** | Commit. Hard gate. |

A champion who has never been asked to do something internal is a **coach**, not a champion.
The test is cheap: ask for one specific internal action with a date. Their response is the
score.

### C — Competition

| | |
| --- | --- |
| **Renewal question** | What is the named alternative — a competitor, an in-house build, consolidation into a suite they already own, or doing nothing? |
| **Artifact for 2/2** | Named alternative with its current status and where it sits in their process |
| **1/2 looks like** | "No competitor mentioned" — absence of evidence recorded as evidence of absence |
| **Disqualifier** | Competitive evaluation discovered inside T-60 with no plan ⇒ auto At Risk |
| **Gates** | Auto-demotion trigger |

### V — Value Realised *(the renewal addition)*

| | |
| --- | --- |
| **Renewal question** | Is it embedded in a workflow they cannot cheaply stop? Adoption breadth, integration depth, data gravity, admin dependency |
| **Artifact for 2/2** | Usage evidence from the last 30 days, measured not assumed, plus a quantified switching cost |
| **1/2 looks like** | "Usage is healthy" with no window, no metric, no comparison |
| **Disqualifier** | Usage flat or declining with no explanation |
| **Gates** | Commit |

---

## 3. Scoring, gates and forecast mapping

```
Total = Σ (nine elements × 0/1/2)          max 18
Commit requires: total ≥ 15  AND  E = 2  AND  P = 2  AND  C = 2
```

The three hard gates exist because they are the three failures that produce a confident
Commit and a lost renewal: nobody spoke to the budget owner, nobody knew the deadline, and
the advocate was never tested.

| MEDDPICC-R | Highest defensible forecast category | What to do this week |
| --- | --- | --- |
| 15–18 with E, P, C at 2 | Commit | Execute the paper path; nothing else is blocking |
| 15–18 with a hard gate below 2 | Most Likely | Close the failed gate. It is the whole plan |
| 11–14 | Most Likely | Name the two lowest elements and put a dated owner on each |
| 6–10 | Best Case at T-90+, At Risk inside T-60 | Manager owns the plan; weekly inspection |
| 0–5 | At Risk | You do not know this renewal. Treat it as discovery, not negotiation |

Score at T-120, refresh at T-90, T-60 and T-30. **The interesting number is the movement**,
not the level: a score that has not moved between T-90 and T-60 means nothing happened.

---

## 4. The question bank

Ask these of the customer. Questions you answer internally are audit items, not qualification.

**Metrics**
- What were you measuring before us, and what number was it?
- What is that number today, and who on your side owns it?
- When your CFO reviews this line item, what do they want to see?
- If you had to defend this spend in one sentence, what would it be?
- Which of the outcomes we agreed to at the start is furthest from where you wanted it?

**Economic Buyer**
- Whose budget does this come out of this year — the same as last year?
- Who signs a contract of this size, and what is their approval limit?
- What would make this an easy yes for them, and what would make it a fight?
- Has that person changed since we last renewed?

**Decision Criteria**
- What has to be true for this to continue for another year?
- Has anything changed internally about how software spend gets justified?
- Is there a mandate to reduce the number of vendors?

**Decision Process**
- Walk me through what happens between you deciding and a signature.
- Who else has to approve — security, privacy, IT, finance, procurement?
- What is the longest step in that chain, and how long did it take last time?
- Are there dates in your calendar that this has to land before?

**Paper Process**
- Is there a notice or cancellation clause we should both have in front of us?
- Does this need a PO, and who raises it?
- Do you re-run security or vendor risk review at renewal, or only at first purchase?
- Which paper entity signs, and has that changed?
- Does anything about the MSA need to change this time?

**Identified Pain**
- What happens on the Monday after this stops working?
- Who would notice first, and what would they do?
- Is the person who originally had this problem still in the role?

**Champion**
- Who else internally needs to hear this before the decision?
- Would you be willing to take the business case to <EB> before the <date> deadline?
- What is the internal objection you expect, and how do you plan to answer it?

**Competition**
- Is anyone internally proposing an alternative, including building it?
- Are you consolidating into a platform you already pay for?
- What would doing nothing look like for you?

**Value Realised**
- Which teams would be affected if access stopped tomorrow?
- What have you built on top of us — integrations, reports, workflows?
- How long would it take you to stand up a replacement?

---

## 5. False twos — how scores get inflated

| Pattern | Why it is a 1, not a 2 | The fix |
| --- | --- | --- |
| "We met the EB at the kickoff two years ago" | Contact, not a business conversation, and outside 90 days | Book a business conversation; score 1 until it is logged |
| Value summary we wrote and emailed | Customer-acknowledged is the standard, not customer-received | Ask them to correct it. A correction is an acknowledgement |
| "Procurement is easy here" | Assertion about a process nobody mapped | Name the steps and the durations |
| "No competitor in play" | Absence of evidence | Ask the do-nothing and consolidation questions explicitly, then score |
| Champion who forwards our emails | Forwarding is not advocacy | Ask for one dated internal action and score the response |
| Notice window copied from the CRM | CRM contract fields are hand-maintained | Cite the clause in the executed contract |
| Usage "healthy" | No metric, window or comparison | `usage_daily.core_actions` last 30d vs prior 30d, with a provenance tag |
| Pain from the original sales cycle | Pain owners move | Re-verify the owner is in role |

**Rule:** if two people would score an element differently from the same evidence, the
evidence is not an artifact and the score is a 1.

---

## 6. Worked example

Northwind Logistics · ATR $480k · `D` = 2026-11-03 · scored 2026-08-27.

| Element | Score | Evidence | Gap and how it closes |
| --- | --- | --- | --- |
| M Metrics | 2 | Outcome summary acknowledged by the VP Ops 2026-06-18: dispatch cycle 41 min → 24 min | — |
| E Economic buyer | 1 | CFO named; last business conversation 2026-03-02 (178 days) | Book a 30-min business conversation by 2026-09-10 · owner: CSM |
| DC Decision criteria | 2 | Written criteria from the VP Ops, 2026-06-18 | — |
| DP Decision process | 1 | Signer known; security and privacy steps unmapped | Map both by 2026-09-05 · owner: Renewal Manager |
| PP Paper process | 0 | Notice window taken from the CRM, not the contract | Pull the executed MSA today · owner: Renewal Manager |
| I Identified pain | 2 | VP Ops stated the consequence, 2026-06-18 | — |
| C Champion | 1 | Responsive, never tested | Ask them to take the business case to the CFO by 2026-09-10 |
| Co Competition | 2 | In-house build proposed by their platform team; status: scoping | — |
| V Value realised | 1 | Usage referenced but not measured in the last 30 days | Pull `core_actions` 30d vs prior 30d by 2026-09-01 |
| **Total** | **12/18** | **Commit gate: FAIL** — total <15 and E, PP, C all below 2 | Highest defensible category: **Most Likely** |

Three of the four actions above cost less than an hour each. That is the usual finding: the
gap between a 12 and a 16 is rarely effort, it is that nobody was scored on it.

---

## 7. Mapping the decision process

Step 5 of `renewal-prep`. The DP and PP elements above are scored from this map, and a 2 on
either requires that the map exists as an artifact — **produce the map, not a description of
it.** Renewals are lost in the approval chain more often than in the relationship, and the
approval chain is the part of the account nobody maintains between cycles.

| What to capture | Detail | Why it decides the renewal |
| --- | --- | --- |
| **Who signs** | Name, title, signing authority limit, legal entity, e-signature route | An unnamed signer at T-30 is the commonest single cause of a slip. An uplift that crosses an authority limit routes to someone who has never heard of us |
| **Who can block** | Security, privacy, IT architecture, finance, procurement — each with the step they own and its duration | These functions hold a veto and no upside: nothing good happens to them if the renewal closes. Handle them early or not at all; there is no late version of this conversation that goes well |
| **The budget cycle** | Fiscal year, when the line for next term is set, freeze windows, which dollar threshold triggers which approver | A renewal landing three weeks after budgets lock is a downsell conversation whatever the relationship looks like — and an uplift can push the line into a new approval tier, adding an approver nobody planned for |
| **What happened last cycle** | Days from first contact to signature, who slowed it, what was conceded, what was promised for this cycle | The best available predictor of this cycle's shape, and almost never written down. Recover it from the prior `opportunity` record, the executed order form's dates, and the email thread that closed it |
| **Consolidation or rationalisation programs in flight** | Named program, sponsor, stage, which categories are in scope | Auto-escalates as a portfolio decision, not an account one. Account-level relationship work does not reach the person running it, and competing on price against a consolidation mandate loses twice |

**A first renewal has no precedent — say so, and widen the band.** The absence of a prior cycle
is a real finding about confidence, not a blank to be filled with the average customer.

**The map's failure mode is plausibility.** Every row above is easy to fill in from what the
champion told you, and a map built entirely from one person's account of their own organisation
scores 1, never 2. A 2 needs at least one row corroborated by a second source: a second contact,
a procurement email, a portal record, the prior cycle's dates.

---

## 8. Source notes

| Claim | Basis | Type |
| --- | --- | --- |
| The eight canonical MEDDPICC elements and their definitions, including Paper Process as the steps from decision to signature and the phase where most deals are lost | MEDDICC (meddicc.com), accessed 2026 | Primary source for the framework |
| The renewal-specific interpretation of each element, the added V, and the artifact standard | Library research pack, adapted from published renewal-review practice | Practitioner convention |
| Scoring 0/1/2 to 18 points, Commit at ≥15 with E, P, C at 2 | Operating convention from the library research pack | Rule of thumb — calibrate the threshold against your own closed renewals once you have four quarters of data |
| "Notice window unknown ⇒ unforecastable" | Structural, not statistical: you cannot forecast a decision whose deadline you do not know | Logical constraint |

The 15/18 threshold is a starting governance line, not a measured predictor. Once you have
four quarters of closed renewals, plot MEDDPICC-R at T-90 against realised outcome and move
the threshold to where your own data puts it.
