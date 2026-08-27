# The Renewal Stage-Gate Ladder

> The full detail behind Steps 1, 2, 4 and 10 of `renewal-prep`. One gate per section:
> objective, owner, required inputs, artifact produced, exit criteria, and what to do when
> the gate is missed. Read §1 and §2 on every run.

**Contents**
1. [The two clocks](#1-the-two-clocks)
2. [The gate ladder](#2-the-gate-ladder)
3. [Renewal readiness scoring criteria](#3-renewal-readiness-scoring-criteria)
4. [Timeline variants by contract type](#4-timeline-variants-by-contract-type)
5. [Gate-miss recovery](#5-gate-miss-recovery)
6. [Rescue mode — inside T-30](#6-rescue-mode--inside-t-30)
7. [Running a renewal window](#7-running-a-renewal-window)
8. [Worked example — a 90-day notice period](#8-worked-example--a-90-day-notice-period)
9. [Escalation triggers — the full armed set](#9-escalation-triggers--the-full-armed-set)
10. [Source notes](#10-source-notes)

---

## 1. The two clocks

```
D = opt_out_deadline = renewal_date − notice_period_days     DECISION clock
R = renewal_date                                             PAPER / term clock
Paper runway = D → R = notice_period_days                    contingency, not plan
```

| Rule | Why it exists |
| --- | --- |
| Gates T-180 … T-0 are offsets from **D** | The customer's cheap exit closes at D. Every date that matters to the *decision* is measured against it. |
| T-0 **is** D | The day intent must be confirmed in writing, or notice is served. |
| T+7 and T+30 are offsets from **R** | Reconciliation and new-term kickoff attach to the term boundary, not the decision. |
| Target countersignature by **D** | The D→R runway is insurance against a slip. A plan that budgets it has already spent it. |
| `notice_period_days = 0` ⇒ D = R | No runway. Every paper lead time has to fit before the renewal date itself. |
| `notice_period_days` UNKNOWN ⇒ no Commit call | You cannot forecast a decision whose deadline you do not know. Pull the executed contract. |

**Send the courtesy notice-deadline letter at T-120 and again at T-90**, in writing, naming
the date. It costs nothing, it forces the conversation onto your timeline rather than theirs,
and it removes any question of winning a term the customer did not intend to buy. A renewal
retained because the customer missed their own window is a reference lost and a fight two
years out.

---

## 2. The gate ladder

Offsets below are the enterprise / annual profile (ACV ≥ $100k). Compress per §4.
"Max category" is the highest renewal forecast category the gate permits.

### T-270 — Strategic pre-work *(multi-year, multi-entity or procurement-heavy only)*

| | |
| --- | --- |
| **Objective** | Establish which legal entity signs and what the paper reality is, before anyone plans a conversation. |
| **Owner** | CSM + AM |
| **Required inputs** | Executed contract, prior order forms, entity/billing records |
| **Artifact** | Contract fact sheet: `renewal_date`, `notice_period_days`, `auto_renew`, `signing_entity`, `governing_law`, `uplift_clause_pct`, `po_required_flag`, `annual_optout_dates[]` |
| **Exit criteria** | Every field above populated and verified **against the executed contract**, not the CRM |
| **Max category** | Most Likely |
| **If missed** | Do it at T-180 and accept that the paper critical path starts with less slack. |

### T-180 — Open the renewal record

| | |
| --- | --- |
| **Objective** | Know what this renewal is worth, what state the account is in, and whether the people who bought it still work there. |
| **Owner** | CSM |
| **Required inputs** | Contract fact sheet, `churn-risk` output, original business case, `contact` records for economic buyer and champion |
| **Artifact** | Renewal record with ATR co-termed as of today, health band snapshot, value-realisation baseline, stakeholder map |
| **Exit criteria** | ATR stated with provenance · risk band computed · economic buyer and champion both verified as still employed and in role · original business case recovered or explicitly marked `UNKNOWN — requires X` · **a commercial touch on record (C25):** a dated, logged conversation with the EB or budget holder inside the last 12 months in which price, term, scope, budget or the contract itself was discussed |
| **Max category** | Most Likely |
| **If missed** | Compress into T-150. Never skip the champion/EB liveness check — a departure discovered at T-60 is a different renewal. **No commercial touch on record is a separate miss:** insert a commercial-context conversation before T-120 as a prerequisite to the price decision, owned and dated, and hold it under R11 — never on the back of an apology, an outage, a credit or a missed milestone. Raising terms cold inside the notice window converts a relationship conversation into a negotiation, and the customer prices it that way for the rest of the cycle. |

### T-150 — Book the executive business review

| | |
| --- | --- |
| **Objective** | Get a date in the diary with the person who owns the budget line. |
| **Owner** | CSM |
| **Required inputs** | Stakeholder map, adoption gap analysis, expansion hypothesis with a number |
| **Artifact** | EBR on the calendar, accepted by the economic buyer; draft value evidence pack |
| **Exit criteria** | EBR accepted by the EB, not by a proxy · adoption gap analysis complete · expansion hypothesis drafted with a dollar figure (proposing it is a later decision) |
| **Max category** | Most Likely |
| **If missed** | Two declined EBR invitations from the EB is a risk-register row with cause code `eb_absent`, not a scheduling problem. |

### T-120 — Deliver the EBR and set the price position

| | |
| --- | --- |
| **Objective** | Show the value in their numbers, ask the renewal-intent question out loud, and decide internally what you will ask for. |
| **Owner** | CSM (value) + Renewal Manager and deal desk (price) |
| **Required inputs** | Value evidence pack, usage evidence ≤30 days old, uplift ladder position, prior-cycle history |
| **Artifact** | Delivered EBR · renewal intent captured verbatim in the CRM · internal price decision · first courtesy notice-deadline letter sent |
| **Exit criteria** | EBR delivered with documented outcomes the customer did not dispute · the question *"Is there anything that would prevent renewal at [date]?"* asked and the answer recorded verbatim · uplift rung chosen internally with its evidence · notice-deadline letter sent · **the C25 commercial touch held, if T-180 fired the prerequisite** — the price decision does not issue until it has |
| **Max category** | Most Likely (Commit only where a signed multi-year is already in place) |
| **If missed** | Ask the intent question in writing this week. It is the cheapest question in the whole ladder and the most often skipped. |

### T-90 — Proposal out, paper process mapped

| | |
| --- | --- |
| **Objective** | Put the commercial terms in writing and discover every process step between here and a signature. |
| **Owner** | Renewal Manager / AM, CSM supporting |
| **Required inputs** | Price decision, decision-process map, procurement contact, MEDDPICC-R draft |
| **Artifact** | Written proposal · paper plan (§`paper-process.md`) with named owners and dates · completed MEDDPICC-R · second courtesy notice-deadline letter |
| **Exit criteria** | Proposal delivered in writing · every paper workstream classified required/not-required/unknown with an owner · MEDDPICC-R complete with E, P and C evidenced · human and model forecast reconciled |
| **Max category** | **Commit becomes available — and only with a paper-movement event on record (C15, `paper-process.md` §11). Verbal agreement alone caps at Most Likely.** |
| **If missed** | The paper map is the non-negotiable half. Deliver it even if the proposal slips — you cannot schedule what you have not mapped. |

### T-75 — Written confirmation of intent

| | |
| --- | --- |
| **Objective** | Obtain, in writing, that the customer is not issuing notice. |
| **Owner** | Renewal Manager |
| **Required inputs** | Proposal, notice-deadline letters, EB contact |
| **Artifact** | Email, portal message or logged call confirming intent to continue — or notice received |
| **Exit criteria** | Written confirmation of intent, or notice received and `save-play` opened |
| **Max category** | Commit, if confirmed **and** a paper-movement event is on record (C15). Written intent plus an empty paper-movement ledger is Most Likely, not Commit |
| **If missed** | This is the single action with the largest effect on the outcome. If it has not happened by T-45, it becomes the top line of the plan and escalates to VP CS. |

### T-60 — Negotiation opens

| | |
| --- | --- |
| **Objective** | Surface every objection while there is still time to trade rather than concede. |
| **Owner** | Renewal Manager |
| **Required inputs** | Concession ladder with pre-approved gets, competitive position, switching-cost evidence |
| **Artifact** | Objection log with cause codes · legal redlines opened if any · security review started |
| **Exit criteria** | Every open objection has a named owner and a date · concession ladder approved to the rung you expect to reach · no unnamed blockers remain |
| **Max category** | Commit |
| **If missed** | Compress T-60 and T-45 into one week and drop the expansion ask. A renewal and an expansion negotiated in the same compressed window usually loses both. |

### T-45 — Order form issued

| | |
| --- | --- |
| **Objective** | Move from discussion to a document that can be signed. |
| **Owner** | Renewal Manager + deal desk |
| **Required inputs** | Agreed price, term, scope; internal discount approval; billing entity |
| **Artifact** | Order form or quote issued · approvals routed · uplift and term positions locked |
| **Exit criteria** | Order form issued · discount approvals obtained at the correct authority level · uplift and term no longer open |
| **Max category** | Commit |
| **If missed** | Issue the order form with the open item flagged rather than waiting for it to close. A document in the customer's hands starts their internal clock. |

### T-30 — Name the signer, raise the PO

| | |
| --- | --- |
| **Objective** | Convert "they're going to renew" into a named human with signing authority and a dated path. |
| **Owner** | Renewal Manager |
| **Required inputs** | Approval chain, procurement contact, PO requirements |
| **Artifact** | Named signer with an expected signature date · PO number or written confirmation none is required |
| **Exit criteria** | Signer named · PO raised or confirmed unnecessary · anything still in Best Case re-called to Most Likely or At Risk |
| **Max category** | Commit only — Best Case is not a valid call inside T-30 |
| **If missed** | An unnamed signer at T-30 is the most common cause of a slipped renewal. Escalate the same day. |

### T-14 — Daily tracking

| | |
| --- | --- |
| **Objective** | Remove the small administrative failures that cost whole quarters. |
| **Owner** | Renewal Manager + Finance |
| **Required inputs** | Signature workflow status, billing entity, tax and e-invoicing details, PO number |
| **Artifact** | Contract in the signature workflow with validated billing data |
| **Exit criteria** | Document in signature routing · billing entity, tax ID and invoicing route validated · PO attached where required |
| **Max category** | Commit |
| **If missed** | Check the document is with the right person. A signature request sitting with someone without authority is invisible and common. |

### T-7 — Executive-to-executive

| | |
| --- | --- |
| **Objective** | Either the document is signed, or an approved alternative path exists. |
| **Owner** | VP CS / CRO |
| **Required inputs** | Status of every open item, bridge-extension terms pre-approved |
| **Artifact** | Executive contact made · 30-day bridge extension at current terms drafted and approved internally |
| **Exit criteria** | In signature, **or** an approved extension path, **or** re-called to At Risk with a written explanation |
| **Max category** | Commit or At Risk — nothing in between |
| **If missed** | Do not let T-0 arrive with no decision and no extension. The extension is prepared before it is needed, not after. |

### T-0 — The opt-out deadline

| | |
| --- | --- |
| **Objective** | The decision is locked in writing, or notice has been served. |
| **Owner** | Renewal Manager |
| **Required inputs** | Everything above |
| **Artifact** | Signed order form, written confirmation of intent, or served notice |
| **Exit criteria** | One of the three exists and is filed |
| **Max category** | Closed, Commit (signature pending inside the runway), or Closed Lost |
| **If missed** | If the deadline passes with no notice served, the term has rolled. Confirm the new dates in writing before doing anything else, and open the renewal record for the new term the same week. |

### R-0 / T+7 / T+30 — Close, reconcile, restart

| Gate | Owner | Artifact | Exit criteria |
| --- | --- | --- | --- |
| **R-0** | Finance | Countersigned document filed; new term booked | ARR bridge line assigned (new product / increased product / product decrease / churned product / churned customer) |
| **T+7** | RevOps | Variance record against the frozen forecast snapshot | Called vs closed reconciled; cause of any delta recorded |
| **T+30** | CSM | New-term success plan; next renewal record opened with its own `D` | Success plan exists; next EBR scheduled; expansion window T+0→T+60 assessed |

---

## 3. Renewal readiness scoring criteria

Score 0 = absent · 1 = asserted or partial · 2 = evidenced by an artifact. 20 points.

| # | Dimension | 0 | 1 | 2 |
| --- | --- | --- | --- | --- |
| 1 | Value evidence captured | No outcome documented in 12 months | Outcomes we computed, not customer-validated | ≥3 quantified outcomes in the customer's own metrics, validated by a named person on their side, dated ≤12 months |
| 2 | Executive sponsor contact | No EB identified, or last contact >180 days | EB identified; last business conversation 90–180 days | Business conversation with the EB logged within 90 days |
| 3 | Multithreading depth | 1 contact carries the relationship | 2 contacts, one function | ≥3 distinct `interaction.customer_participants` over 90 days spanning ≥2 functions |
| 4 | Health band | At Risk or worse, or an override floor fired | Watch | Secure, no override floor fired |
| 5 | Budget confirmed | Unknown | Assumed to exist | Named budget line for the new term confirmed by the EB or their finance partner |
| 6 | Decision process mapped | Unknown | Signer known, approvers not | Every approver named with their step and expected duration |
| 7 | Procurement path known | Unknown | Contact known, requirements not | Portal, buyer contact, required documents and their current status all recorded |
| 8 | Competitive position | Unknown | Alternative suspected | Named alternative with status, plus quantified switching cost |
| 9 | Uplift justified | No position, or no commercial touch on record in 12 months (C25) | Position chosen, evidence not assembled | Rung chosen with the artifact that supports it (see SKILL.md Step 7), on an account with a commercial touch on record inside 12 months |
| 10 | Paper path known | Unknown | Workstreams listed, no lead times | Every workstream has a measured lead time, an owner on both sides, and a latest start date |

**Gates.** Advance past T-60 requires **≥16/20 with dimensions 1, 2, 6 and 10 at 2**. Below
**12/20 at T-60** the renewal enters the risk register with cause code `paper_stall` or
`value_not_evidenced` regardless of health band — unpreparedness is a risk in its own right.

**Readiness does not open Commit on its own.** 20/20 with an empty paper-movement ledger is still
Most Likely (C15, `paper-process.md` §11): readiness measures our work, and Commit measures theirs.

---

## 4. Timeline variants by contract type

| Contract type | Ladder change | The trap it avoids |
| --- | --- | --- |
| Annual, ACV ≥ $100k | Full ladder; add T-270 if multi-entity or procurement-heavy | Enterprise paper cycles do not fit inside 90 days |
| Annual, mid-market ($25k–100k) | Multiply every offset by ~0.5 (T-180 → D-90d). Same gates, same exit criteria | Running an enterprise ladder on a book of 40 renewals means running none of them |
| Annual, SMB / tech-touch (<$25k) | Multiply by ~0.33. Automate T-180 and T-120 as lifecycle motions; human touch from T-45 | Spending an EBR on ARR that cannot repay it |
| Monthly / evergreen | No ATR event. Rolling 90-day cadence; `D` = the next cancellation-effective date under the cancellation clause | Applying event-based renewal management to continuous churn |
| Quarterly / short term (<6 months) | Multiply by ~0.35. Pre-clear the paper process **once** and reuse the cleared position each term | A 45-day paper path inside a 90-day term consumes half the relationship |
| Multi-year, single decision point | Full ladder in the final year; a health gate at each anniversary; ramp pre-briefs | Treating intervening years as no-risk. Risk is concentrated, not absent |
| **Multi-year with annual opt-out** | **Every anniversary is a full renewal event with its own `D` and its own ladder** | Reporting three renewal events as one and missing three notice windows |
| Multi-year with contracted ramp | Full ladder plus a step-up pre-brief 90 days before each increase takes effect | An unbriefed ramp step is the most avoidable renegotiation trigger there is |
| Auto-renew, fixed renewal term | Full ladder. The real risk date is `D`, not `R` | Forecasting to the end date on a contract whose decision lands three months earlier |
| Fixed term, no auto-renew | Full ladder plus an affirmative-signature dependency at T-45 | Assuming silence means continuation. It means expiry |

---

## 5. Gate-miss recovery

**Never skip a gate — compress it.** The exit criteria are what make the next stage possible;
skipping the value gate does not save time, it relocates the failure to T-30.

| Gate missed | Compress into | Recovery move | What you accept |
| --- | --- | --- | --- |
| T-270 / T-180 | T-150 | Pull the executed contract today; run the champion/EB liveness check before anything else | Paper path starts with less slack |
| T-150 | T-120 | Ask the intent question by email rather than waiting for an EBR slot | Weaker value delivery; the EBR becomes a proposal call |
| T-120 | T-90 | Deliver value evidence in writing with the proposal, clearly sequenced ahead of price in the document | Price lands sooner than value; expect more objections |
| T-90 | T-75 | Map paper first, proposal second — the map is the half you cannot recover later | Negotiation starts without a full objection log |
| T-75 | T-60 | Ask for written confirmation of intent in the negotiation opener | You negotiate without knowing if you are in a renewal or a save |
| T-60 | T-45 | Drop the expansion ask entirely; negotiate the renewal alone | Expansion moves to the T+0→T+60 window |
| T-45 | T-30 | Issue the order form with open items flagged rather than waiting | Redlines and signature overlap |
| T-30 | T-14 | Escalate to the EB the same day to name the signer | Bridge extension becomes likely |
| T-14 / T-7 | — | Executive-to-executive contact plus a pre-approved 30-day extension | The renewal closes late; forecast category moves |

**Two consecutive missed gates transfers ownership of the plan to the CS manager and drops
the forecast category one step.** This is the mechanism that turns a quiet slip into a
visible one while it is still recoverable.

---

## 6. Rescue mode — inside T-30

When fewer than 30 days remain to `D` and the gates behind you are missed, most of the
ladder is unreachable. Run this instead, in order, and stop pretending the rest exists.

| # | Move | Owner | Inside |
| --- | --- | --- | --- |
| 1 | Recompute `D` from the executed contract. Confirm whether you are inside the notice window already | Renewal Manager | Same day |
| 2 | One written question to the EB: is anything preventing renewal on `<date>`? | CSM + Renewal Manager | 24h |
| 3 | Assemble the thinnest credible value artifact — one outcome, customer-validated, with provenance | CSM | 48h |
| 4 | Map only the paper workstreams that are **required and serial**. Ignore the rest | Renewal Manager | 48h |
| 5 | If the serial path exceeds days-to-`D`, open the bridge extension now — 30–60 days at current terms | Deal desk | 72h |
| 6 | Drop every expansion ask. Re-open at T+0→T+60 | CSM | Immediately |
| 7 | Hold the uplift unless it is contractual and already communicated | Renewal Manager | Immediately |
| 8 | Open a risk-register row with cause code `paper_stall` or `procurement_late` and a VP owner | CS manager | 24h |

**The bridge extension is a legitimate outcome, not a failure.** A 30-day extension at current
terms removes an artificial deadline that neither side chose and converts a forced concession
into a normal negotiation. Prepare it before you need it; asking for one at T-2 reads as panic.

---

## 7. Running a renewal window

| Cadence | Attendees | Scope |
| --- | --- | --- |
| Weekly renewal stand-up (45 min) | CSM, Renewal Manager, Finance and Legal as needed | Everything closing inside 60 days of `D`, plus every At Risk account regardless of date |
| Weekly forecast review (60 min) | VP CS, CS managers, RevOps | Roll-up, category movement, accuracy against the frozen snapshot |
| Monthly portfolio review | CS org + RevOps + Finance | The full 180-day rolling `D` window |

Sort the board by **days to `D`**, never by renewal date, and never by ARR alone. Review
exceptions only: a missed gate, negative paper slack, readiness <16/20, or a category change.
Sixty minutes covers roughly fifteen accounts at three to four minutes each.

**Capacity is a gate too.** If the window holds more renewal motions than the team can run,
name what is being dropped to tech-touch and who approved it. An at-risk list longer than
capacity is a wish list.

**The board.** Window Batch mode emits this above any individual plan, then full plans only for the
exceptions named beneath it.

```markdown
## Renewal Window Board — <N> renewals · $<X> ATR · <window>
| # | Account | ATR | `D` | Days to `D` | Notice | Stage | Gates missed | Readiness | MEDDPICC-R | Paper slack | Paper moved (C15) | Commercial touch (C25) | Category | Owner | Next action (by date) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
**Exceptions requiring a full plan this week:** <a missed gate, negative paper slack, readiness <16/20, Commit refused under C15, or no commercial touch on record in 12 months>
**Capacity check:** <renewals in the window> vs <motions the team can run> — if the first exceeds the second, name what is dropped and who approved it.
```

`Paper moved (C15)` carries the qualifying event and its date, or `none`; `Commercial touch (C25)`
carries the days since the last one, or `none in 12 months`. Both are sortable, and both are the
columns that separate a renewal that will close from one that is only expected to.

---

## 8. Worked example — a 90-day notice period

Renewal date 2027-02-01, notice period 90 days, ACV $480k, enterprise profile, today 2026-08-27.

```
D = 2027-02-01 − 90d = 2026-11-03      68 days away
R = 2027-02-01                        158 days away
Paper runway D→R = 90 days (contingency)
```

| Gate | Date | Status on 2026-08-27 |
| --- | --- | --- |
| T-180 | 2026-05-07 | Passed or missed — audit required |
| T-150 | 2026-06-06 | Passed or missed — audit required |
| T-120 | 2026-07-06 | Passed or missed — audit required |
| T-90 | 2026-08-05 | **22 days overdue** |
| T-75 | 2026-08-20 | **7 days overdue** |
| T-60 | 2026-09-04 | Open, 8 days out |
| T-0 | 2026-11-03 | Open, 68 days out |
| R-0 | 2027-02-01 | 158 days out |

A team scheduling from `R` would believe it was at T-158 with everything ahead of it. It is in
fact past two gates. With a serial paper path of 80 days measured from prior renewals, slack
against `D` is **−12 days**: the paper process as planned cannot finish before the customer's
cheap exit closes. That single number is the top line of the plan.

Reproduce with:

```
python3 scripts/renewal_calendar.py --account "Northwind Logistics" \
  --renewal-date 2027-02-01 --notice-days 90 --atr 480000 \
  --segment enterprise --today 2026-08-27 \
  --paper "security_review=30,legal_redlines=21,order_form=5,signature_workflow=10,po_issuance=14"
```

---

## 9. Escalation triggers — the full armed set

**This is the armed set — the full thirteen.** `../SKILL.md` Step 9 carries only the six that fire
most often; the other seven live here. Arm every one that applies and print its state in §11 of
the plan, including the ones that have not fired — an unfired trigger printed as unfired is the
record that it was checked. Rows 10 and 11 below are reported as a single combined row in the
plan, and rows 6 and 7 are summarised there as "low MEDDPICC-R" and "two consecutive gates
missed".

| Trigger | Escalate to | Within | What changes |
| --- | --- | --- | --- |
| Notice of non-renewal received | VP CS + CRO | Same day | `save-play`; forecast to Closed Lost pending the save |
| Auto-renew switched off | VP CS | 24h | `save-play`; category drops to At Risk |
| Competitive evaluation, RFP or vendor-consolidation program found inside T-60 | VP CS / CCO | 48h | Auto At Risk; compete on switching cost, not price |
| Economic buyer departed with no replacement in 30 days, or a budget freeze / RIF / down-round announced | VP CS | 5 business days | Sponsor re-mapping, or re-scope to value-per-dollar — this is not an adoption problem |
| Opt-out deadline inside 45 days, no written confirmation of intent | VP CS | 24h | The action with the largest effect on the outcome; nothing outranks it |
| MEDDPICC-R <10/18 or readiness <12/20 at T-60 | CS manager | Next forecast call | Manager owns the plan; weekly inspection |
| Two consecutive gates missed | CS manager | Next forecast call | Category drops one step |
| P1 open >14 days with executive visibility inside T-90 | VP CS + VP Eng | 48h | Commercial ask pauses until closure + cooldown |
| Procurement first appears inside T-30 | Deal desk | 24h | Re-call to Most Likely at best; propose a 30–60 day extension at current terms |
| Serial paper path exceeds days remaining to `D` | Deal desk + Legal | 48h | Parallelise or open the bridge extension now |
| Order form unsigned at T-7 | VP CS / CRO | Same day | Executive-to-executive; bridge extension prepared |
| Verbal yes logged, no paper-movement event 14 days later | Renewal Manager | 21 days | Category capped at Most Likely with the reason printed (C15); register row, cause code `verbal_only`; the next action is a paper-process ask — named person, named document, date — never another value conversation. See `paper-process.md` §11 |
| No commercial touch with the economic buyer or budget holder inside 12 months at T-180 | CS manager | 5 business days | T-180 fails on C25; the commercial-context conversation is booked before T-120 and the price decision waits for it, held under R11 — never attached to an apology, outage, credit or miss. See `commercial-position.md` §4 |

A trigger that fires and is not escalated inside its window is itself a register row, owned by
the person who missed it. The point of the window is that it is short enough to be inconvenient.

---

## 10. Source notes

| Claim | Basis | Type |
| --- | --- | --- |
| Start at 90–120 days for standard annual contracts; 180 days for enterprise above ~$100k | Practitioner guidance converges here across CS and procurement sources (2026) | Practitioner rule of thumb — **not** a measured benchmark |
| Compress ~50% for mid-market; replace early gates with automated motions for tech-touch | Practitioner operating convention | Rule of thumb |
| 30 / 60 / 90 days are the near-universal notice windows; 30 days is the most common in standardised SaaS agreements, 60–90 days typical in negotiated enterprise agreements | Contract-market guides, 2026 | Practitioner guidance, not survey data |
| Forecast-category ceilings by time-to-renewal (Commit unavailable before T-90) | Forecast governance convention documented in the library research pack | Rule of thumb |
| "The strongest predictor of renewal is an executive-sponsor business conversation in the last 90 days" | Widely repeated practitioner claim; **no primary study located** | Treat as a hypothesis to test on your own data |
| Timeline shapes for multi-year with annual opt-out, ramps and evergreen contracts | Contract-clause taxonomy | Structural, not statistical |

Replace every timing default in this file with your own measured cycle times as soon as you
have ten closed renewals to measure. A borrowed default that fits nobody is the most
expensive kind of precision.
