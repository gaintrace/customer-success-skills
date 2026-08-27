# Renewal Plan — <Account> · ATR $<X> · <segment>
**Internal.** Contains risk and pricing language that must never be sent to the customer.
Prepared <date> by <name>. Next review <date>.

## Bottom Line
<3 sentences: ATR at stake, the governing date and days remaining, the single action that
most changes the outcome, and who owns it. If paper slack is negative, it belongs here.>

| | |
|---|---|
| ATR | $X [<system> · <field> · as-of <date>] |
| Renewal date `R` | <date> (<N> days) |
| Notice period | <N> days [<contract> · §<clause>] |
| **Opt-out deadline `D`** | **<date> (<N> days)** — the governing date |
| Auto-renew | on / off / `UNKNOWN — requires the executed contract` · last changed <date> |
| Stage now · gates missed | <gate>, <N> days in · <n> missed: <list> |
| Commercial touch on record (C25) | <date · person · what was discussed> · <N> days since — or **NONE IN 12 MONTHS**, prerequisite fires |
| Paper movement (C15) | <event · date · source> — or **NONE ON RECORD**, Commit refused |
| Readiness | X/20 · MEDDPICC-R X/18 |
| Health band | <band> from `churn-risk` <date> |
| Max forecast category | <category> — <the rule that caps it: days-to-`D` ceiling, MEDDPICC-R gate, or `C15 — verbal only, no paper movement`> |
| Confidence | High / Medium / Low — <criteria met> |

## 1. Gate Audit
| Gate | Date | Status | Exit-criteria artifact | If missed: recovery |
|---|---|---|---|---|
| T-180 | | Passed / Missed / N/A | | |
| T-150 | | | | |
| T-120 | | | | |
| T-90 | | | | |
| T-75 | | | | |
| T-60 | | | | |
| T-45 | | | | |
| T-30 | | | | |
| T-14 | | | | |
| T-7 | | | | |
| T-0 | | | | |

## 2. MEDDPICC-R
| Element | Score | Evidence / artifact | Gap and how it closes |
|---|---|---|---|
| M — Metrics | /2 | | |
| E — Economic buyer | /2 | | |
| D — Decision criteria | /2 | | |
| D — Decision process | /2 | | |
| P — Paper process | /2 | | |
| I — Identified pain | /2 | | |
| C — Champion | /2 | | |
| C — Competition | /2 | | |
| V — Value realised | /2 | | |
| **Total** | **X/18** | Commit gate: ≥15 with E, P, C at 2 → **PASS / FAIL** | |

## 3. Renewal Readiness
| # | Dimension | Score | Evidence | What moves it to 2 | Owner | By |
|---|---|---|---|---|---|---|
| 1 | Value evidence captured | /2 | | | | |
| 2 | Executive sponsor contact | /2 | | | | |
| 3 | Multithreading depth | /2 | | | | |
| 4 | Health band | /2 | | | | |
| 5 | Budget confirmed | /2 | | | | |
| 6 | Decision process mapped | /2 | | | | |
| 7 | Procurement path known | /2 | | | | |
| 8 | Competitive position | /2 | | | | |
| 9 | Uplift justified | /2 | | | | |
| 10 | Paper path known | /2 | | | | |
| | **Total** | **X/20** | Advance gate: ≥16 with 1, 2, 6, 10 at 2 → **PASS / FAIL** | | | |

## 4. Decision Process
| Role | Name | Title | Step they own | Duration | Last contact | Status |
|---|---|---|---|---|---|---|
| Signer | | | | | | |
| Economic buyer | | | | | | |
| Champion | | | | | | |
| Security approver | | | | | | |
| Legal | | | | | | |
| Procurement | | | | | | |
| Finance / budget owner | | | | | | |

**Budget cycle:** <fiscal year end, when the line is set, freeze windows>
**Last cycle:** <days from first contact to signature, who slowed it, what was conceded>
**Not yet identified:** <named gaps, written as `UNKNOWN — requires X`, each with a dated owner>

## 5. Value Evidence Pack
**Original business case (their words, <date>):** "<quote>"

| Outcome | Baseline | Current | Delta | $ value | Their validator | Source |
|---|---|---|---|---|---|---|
| | | | | | | |
| | | | | | | |
| | | | | | | |

**Switching cost:** <integrations · records under management · trained users · embedded
workflows · reports built · re-procurement effort>
**What is not working:** <the honest section — issue, impact, committed fix, owner, date>
**Customer has stated the value number:** yes / no — <quote and date, or the dated plan to obtain it>

## 6. Commercial Position
| Item | Position | Justification rung | Approval needed | Walk-away |
|---|---|---|---|---|
| Uplift | | | | |
| Term | | | | |
| Scope / seats | | | | |
| Payment terms | | | | |

**Concessions available, each with its required get:**
| Rung | Give | Required get | Approval |
|---|---|---|---|
| | | | |

**Commercial touch on record (C25):** <date · person · subject> — or NONE IN 12 MONTHS, in which
case the prerequisite row below is mandatory and the price decision waits for it.
**Prerequisite conversation:** <date · owner · agenda, scheduled before T-120>
**R11 clear:** yes / no — <the apology, outage, credit or miss inside 14 days either side, and the
date the touch moved to. Never merged with the bad news.>

## 7. Paper Critical Path (backward from `D` = <date>)
| Workstream | Required? | Owner (ours) | Owner (theirs) | Lead time | Latest start | Slack | Status |
|---|---|---|---|---|---|---|---|
| Security / vendor-risk re-review | | | | | | | |
| Privacy / DPIA / sub-processor | | | | | | | |
| Legal redlines | | | | | | | |
| Order form issued | | | | | | | |
| Signature routing | | | | | | | |
| Requisition → PO | | | | | | | |
| Procurement portal onboarding | | | | | | | |
| Vendor master / W-9 / bank | | | | | | | |
| Insurance certificates | | | | | | | |
| Budget line confirmed | | | | | | | |
| Tax / entity / e-invoicing | | | | | | | |
| Accessibility / diversity docs | | | | | | | |

**Serial critical path: <N> days (FLOOR — <k> lead times UNKNOWN). Days to `D`: <M>. Slack: <M−N>.**
<If slack is negative: state the three options — start today · parallelise with the customer's
agreement · open the bridge extension now.>

**Paper-movement ledger (C15) — the Commit entry criterion. All five rows printed every cycle,
including the ones that are `no`. Evidence per event: `../references/paper-process.md` §11.**

| Qualifying event | On record? | Date | Source |
|---|---|---|---|
| Security / vendor-risk re-review started | yes / no | | |
| Legal redlines returned, or written confirmation of none | | | |
| PO requested or requisition raised | | | |
| Vendor portal or supplier record created or refreshed | | | |
| Order form in their signature routing | | | |

**Commit entry: PASS (<N> events on record) / REFUSED — `C15 — verbal only, no paper movement`.**
<Verbal yes logged <date>; <N> days since with no paper movement. At 14 days this is a register row
with cause code `paper_stall`; at 21 it escalates to the Renewal Manager and the next action is a
paper-process ask, not another value conversation.>

## 8. Risk Register
<Use `../assets/risk-register-template.md`.>

## 9. Stage Plan
<Where C25 fired, the first row is the commercial-context conversation, dated before T-120, with a
named owner. The plan does not emit without it.>

| Gate | Date | Objective | Owner | Required inputs | Artifact produced | Exit criteria | If missed |
|---|---|---|---|---|---|---|---|
| | | | | | | | |

## 10. Actions
| # | Action | Owner | By | Expected effect | Success measure |
|---|---|---|---|---|---|
| 1 | | | | | |
| 2 | | | | | |
| 3 | | | | | |

## 11. Escalation Triggers Armed
| Trigger | Escalate to | Within | Currently |
|---|---|---|---|
| Notice of non-renewal received | VP CS + CRO | Same day | not fired |
| Auto-renew switched off | VP CS | 24h | not fired |
| Competitive evaluation / RFP / consolidation inside T-60 | VP CS / CCO | 48h | not fired |
| EB departed with no replacement in 30 days, or budget freeze / RIF announced | VP CS | 5 business days | not fired |
| Opt-out deadline inside 45 days with no written confirmation of intent | VP CS | 24h | |
| MEDDPICC-R <10/18 or readiness <12/20 at T-60 | CS manager | Next forecast call | |
| Two consecutive gates missed | CS manager | Next forecast call | |
| P1 open >14 days with executive visibility inside T-90 | VP CS + VP Eng | 48h | |
| Procurement first appears inside T-30 | Deal desk | 24h | |
| Serial paper path exceeds days remaining to `D` | Deal desk + Legal | 48h | |
| Order form unsigned at T-7 | VP CS / CRO | Same day | |
| Verbal yes logged, no paper-movement event 14 days later (C15) | Renewal Manager | 21 days | |
| No commercial touch with the EB inside 12 months at T-180 (C25) | CS manager | 5 business days | |

## 12. Customer-Facing Drafts
<Only the draft(s) due at the current gate. Full versions in `../assets/customer-facing-drafts.md`.
Omit this section entirely when nothing is due. Everything above this line is internal.>

════════════════════════════════════════════════════════════
CUSTOMER-FACING — copy the block below and send as written.
Everything above this line is internal. Do not forward it.
════════════════════════════════════════════════════════════

**<Draft name — notice-deadline letter / intent question / bridge extension> — due <date>, to <recipient>**

```text
<Send-ready text, formatted for an email client: plain text, a blank line between
paragraphs, • bullets, no markdown headings, no pipe tables, no bold. Opens on
something only this account's data could produce. One dated ask. Every slot filled
before emission — a fence still containing [Name] is not send-ready. If a value is
genuinely unavailable, drop that sentence and raise UNKNOWN — requires X above the
divider.>
```

## What would change this plan
<2–3 specific, observable events that would move the category or the date.>

### Assumptions
<Every default this run leaned on. One row each, with a concrete consequence.
"May affect results" is not a consequence — if you cannot name what would change,
you did not need the assumption.>

| # | Assumption | Why it was needed | If wrong |
|---|---|---|---|
| 1 | 90-day notice period | `notice_period_days` blank in the export; `cs-context` §2 standard applied | `D` could be up to 60 days earlier than shown — treat every gate date as a ceiling and the Commit gate as failed |
| 2 | | | |

### Coverage Ledger
| Signal family | Source checked | Status | Notes |
|---|---|---|---|
| Product usage & adoption | | ✅ / ⚠️ / ❌ | |
| Commercial & contract | | | |
| Relationship & engagement | | | |
| Support & reliability | | | |
| Sentiment & VoC | | | |
| Billing & payment | | | |
| Firmographic & external | | | |

**Coverage: X / 7 (Y%) → confidence capped at <level>.**
Blind spots: <which families are missing and what a renewal plan typically gets wrong without them.>
