# The Decision Rubric

> Four outcomes, an ordered gate sequence that returns exactly one, and nine dimensions with
> anchors concrete enough that two engineers score the same request the same way.
>
> The gates **decide**. The rubric supplies their inputs and the auditable record. A scorecard that
> produces a number and no decision has handed the work back to the reader.
>
> Evidence labels: `[M]` measured · `[V]` vendor research · `[P]` practitioner standard ·
> `[A]` academic, standards body or regulation · `[D]` primary document.

**Contents**
- [1. Reducing the request to the job](#1-reducing-the-request-to-the-job)
- [2. The gate sequence in full](#2-the-gate-sequence-in-full)
- [3. The nine dimensions — anchors](#3-the-nine-dimensions--anchors)
- [4. Contradictions and tie-breaks](#4-contradictions-and-tie-breaks)
- [5. What the business model changes](#5-what-the-business-model-changes)
- [6. The decision record](#6-the-decision-record)
- [7. Reviewing a past decision](#7-reviewing-a-past-decision)
- [8. Anti-patterns](#8-anti-patterns)

---

## 1. Reducing the request to the job

Every downstream number depends on this reduction. Score the **job** — the outcome the customer
needs — not the **artefact** they described. Customers propose mechanisms because mechanisms are
easier to say than outcomes, and a vendor who builds the proposed mechanism has outsourced its
architecture to someone with no view of the product.

| Layer | Example, same account | Why it matters |
| --- | --- | --- |
| **Artefact** (what they asked for) | "A webhook that fires when an order closes" | Specific to their current stack; changes when their stack changes |
| **Mechanism** (how they imagine it) | Push, real-time, JSON | An implementation preference, often inherited from another vendor |
| **Job** (the outcome) | "Finance knows an order closed before the 06:00 reconciliation" | Stable. Two accounts with different artefacts may share this |
| **Trigger** (why now) | "Nine of last month's 22 exceptions were found a day late" | The number that makes the counterfactual real |

### The five discovery questions

Ask one, then stop talking (`R16` — three per call; these are the three that matter plus two
follow-ups when the answer is thin).

| # | Question | What a good answer contains |
| --- | --- | --- |
| 1 | "What happens today, and who does it?" | A named person, a frequency, a duration |
| 2 | "What goes wrong when it does not happen?" | A consequence with a number or a named incident |
| 3 | "Who notices if we do nothing?" | A role, ideally the economic buyer — if nobody notices, the counterfactual is "nothing" |
| 4 | "Is there a date this has to work by, and whose date is it?" | A date with an owner. A date they invented is not a constraint |
| 5 | "What have you tried?" | The workaround already in production — this is G4 evidence for §3 dimension 1 |

### The reduction test

**Write the job on one line without naming a technology.** If you cannot, discovery is incomplete
and the correct output is the single question that separates the candidates, not a scored memo.

| Written as | Reduced to |
| --- | --- |
| "They want a custom dashboard" | "The regional managers need yesterday's exception count without asking Ops for it" |
| "They want an API endpoint" | "Their ERP needs to know a shipment was accepted within five minutes" |
| "They want SSO with our IdP" | UNKNOWN — this one is already a job; SSO is the outcome, not the mechanism |
| "They want us to build a connector to Acme WMS" | "Stock counts in our system match the WMS by 07:00 each day" |

The third row matters: not every request needs reducing. Forcing a reduction on a request that is
already a job produces a vaguer statement, not a better one.

---

## 2. The gate sequence in full

Ordered. The first gate that matches returns the outcome; later gates do not run and are printed
as "not reached". Reasoning about a later gate after an earlier one matched is how a Decline gets
argued into a Build.

### Gate 0 — the fork test

**Test:** does delivering this require forking the product, patching an internal, running a
modified build, or depending on an undocumented interface?

**Returns: DECLINE.** This is the one gate no evidence overrides. A fork has no upgrade path and no
support contract; every future release becomes a merge, and the merge is ours forever. The correct
response is not "we will maintain the fork carefully" — it is to find the extension point, or to
decline and route the gap to product.

| Counts as a fork | Does not |
| --- | --- |
| A modified build shipped to one customer | A documented plugin, webhook, MCP server, sub-agent or skill |
| A patched internal class or private API | A published API at a supported version |
| A schema change in a shared table | A customer-owned table in their own schema |
| A pinned dependency the platform has moved off | A supported version pin inside the support window |

### Gate 1 — the roadmap test

**Test:** is product shipping this, with a **named owner** and a committed increment, before
`opt_out_deadline − evidence_window`?

**Returns: WORK_AROUND** until it lands. Both clauses are required: a roadmap item with no named
owner is a wish, and a date after the decision window is a date the customer will never see.
**Never state the date to the customer without that owner's agreement** (`R19`) — "it's on the
roadmap" is the kindest-sounding sentence in customer success and the most damaging.

The decision window is `renewal_date − notice_period_days − evidence_window` (`R1`), not the
renewal date. `evidence_window` defaults to **60 days** for enterprise annual — the time needed
after delivery to produce evidence the customer will judge on. A library convention `[P]`.

### Gate 2 — the workaround test

**Test:** does a supported path reach **≥80% of the job at ≤20% of the build effort**?

**Returns: WORK_AROUND**, with the residual 20% written up as field signal and a dated review.

Workarounds are systematically under-chosen because they feel like a lesser answer. They are the
highest-return outcome available: no principal, near-zero interest, reversible in an afternoon, and
they surface whether the job was real. Four shapes, in order of preference:

| Shape | Example | Carrying cost |
| --- | --- | --- |
| **Configuration** | An existing report scheduled to a different destination | Zero |
| **Process change on their side** | A named person runs a two-minute step | Zero to us; must be agreed with that person by name |
| **Supported path at partial fidelity** | Hourly instead of real-time | Zero |
| **We perform the manual step** | We run a monthly reconciliation for them | Real, recurring, and it belongs in the ledger like any build |

The fourth shape is a build wearing different clothes. Price it as one.

### Gate 3 — the generality test

**Test:** `N_evidenced ≥ K*` **and** at least two accounts at tier G3 or above.

**Returns: GENERALISE.** Both clauses. The sum alone can be reached by four G1s, which is four
opinions. Evidence tiers, the search method and `K*`: `productisation-path.md` §2 and
`carrying-cost.md` §5.

### Gate 4 — the payback test

**Test, all four clauses:**

1. `ARR_at_stake × savability > TCO(N)` — the build pays for itself against the revenue it holds.
2. A **named maintainer** — a person, not a team. A team is not paged.
3. A **sunset review date** — a calendar date, set now, ≤12 months out.
4. **Rollback in ≤1 sprint** — a two-way door (§3 dimension 6).

**Returns: BUILD_BESPOKE.** Missing any clause fails the gate. In practice clause 2 fails most
often, and it is the clause people are most tempted to wave through, because naming a maintainer
means someone's next quarter changes.

`savability` mirrors `churn-risk` §6: addressable root cause 1.2, partially addressable 1.0,
structural 0.5. Use 1.0 when unknown and record it in the Assumptions table.

### Gate 5 — nothing matched

**Returns: DECLINE**, with the nearest alternative priced and the field-signal writeup attached. A
decline reached by exhausting the gates is a stronger decline than one reached by instinct, because
you can show which gate it failed and what would change it.

---

## 3. The nine dimensions — anchors

Score 0–4. Even numbers are anchored below; 1 and 3 are the halfway points. Every score carries its
evidence, or reads `UNKNOWN — requires <source>`.

| # | Dimension | 0 | 2 | 4 |
| --- | --- | --- | --- | --- |
| 1 | **Generality (evidenced)** | `N_evidenced` < 1, or every row is G0/G1 | 1–2, at least one at G3 | ≥ `K*`, with ≥2 accounts at G3+ |
| 2 | **Strategic fit** | Contradicts a stated product direction, or serves a segment we are exiting | Adjacent — neither on nor against the direction | On the stated direction, and a named PM will say so in writing |
| 3 | **Roadmap collision** | Product ships it inside the decision window, owner named | On the roadmap, no owner or no increment | Not planned, and the PM confirms it is not planned |
| 4 | **Build effort** | > 6 usable weeks, or the estimate has no design behind it | 1–6 usable weeks | ≤ 1 usable week, on a documented extension point |
| 5 | **Annual maintenance burden** | Interest rate > 100%, or carrying > 5% of account ARR | 30–100% | < 30%, and no third-party cost |
| 6 | **Reversibility** | One-way door: their data model, their trained workflow, or their downstream systems depend on it | Reversible within a quarter with notice | Rollback in ≤1 sprint, flag-guarded, no customer-visible schema |
| 7 | **Who carries the upgrade cost** | Us, on every release, forever | Us, at each major version | Nobody — it rides the supported path unchanged |
| 8 | **Revenue at stake** | No ARR contingent on it | Contingent, but only verbally | A written purchase or renewal condition with a named signer |
| 9 | **Counterfactual if we decline** | They leave, and the loss would be attributable to this | They complain, escalate, and stay | They accept the workaround and say so |

### Notes on the dimensions people get wrong

**Dimension 2 — strategic fit is not "would this be nice".** The anchor at 4 requires a named PM to
say so in writing, because "strategically aligned" is the easiest sentence in the memo to write and
the hardest to check. Absent that, score 2.

**Dimension 3 — a roadmap item with no owner scores 4, not 0.** Counter-intuitive and correct: an
unowned roadmap item does not reduce your risk of building this, it just makes the internal
conversation more comfortable.

**Dimension 5 — carrying above 5% of account ARR makes this a commercial decision, not an
engineering one.** It goes to the account owner that week and into the renewal margin conversation.
The threshold is a library convention `[P]`, set low because services attached to a subscription
are structurally unprofitable: TSIA reports project-based services at product companies averaging
gross margins in the mid-30s, and the TSIA Cloud 40 companies that break out project-services
margins average **−9%** (TSIA, published 2023 on Q3-2022 data) `[V]`.

**Dimension 6 — reversibility is about the customer, not the codebase.** Deleting the code is
easy. Undoing a schema their finance team reconciles against, or a workflow forty staff were
trained on, is not. Bezos's distinction is the frame: a two-way door is decided fast on ~70% of the
information; a one-way door is decided slowly and deliberately `[P · Amazon 2015 shareholder
letter]`. A build that changes their data model is a one-way door wearing a two-week estimate.

**Dimension 7 — "who carries the upgrade cost" is the question that predicts the five-year
number.** Maintenance is roughly 60% of total software lifecycle cost, and enhancement rather than
defect repair is about 60% of that maintenance `[A · Glass, *Facts and Fallacies of Software
Engineering*, 2002; Lientz & Swanson]`. A component that adds hours to every upgrade compounds; one
that rides the supported path does not.

**Dimension 9 — write it, always.** An unwritten counterfactual is read as "nothing happens", which
makes every decline look free. Write the actual sentence: *"Dana escalates to her CFO, the January
renewal opens with this on the table, and the two other accounts running the manual workaround stay
on it."*

---

## 4. Contradictions and tie-breaks

Real requests produce conflicting inputs. Surface them; do not average them.

| Conflict | Tie-break | Why |
| --- | --- | --- |
| High ARR at stake, low generality | Gate 4, not Gate 3 | Money justifies **owning** something explicitly. It never justifies calling one customer a market |
| High generality, low ARR at stake | Gate 3 | Generality is the product argument; ARR is the services argument. They answer different questions |
| The champion is adamant, the economic buyer has not mentioned it | Score dimension 8 as 0 until it is written | A request carried by one contact with no second voice is one person's opinion (`R5`) |
| Product says "we might do it next year" | Dimension 3 scores 4 | No owner, no increment, no gate |
| Engineering says two days, the estimate has no design | Dimension 4 scores 0 | A concept-stage estimate carries a 0.5×–2× range; see `../../fde-scoping/references/estimation.md` |
| A workaround exists but the customer has rejected it | Re-run Gate 2 on the *job*, not the artefact | Customers reject mechanisms, not outcomes. Ask which part of the outcome the workaround misses |
| Two accounts asked for the same artefact, different jobs | `N_evidenced` counts **one** | The reduction in §1 is what stops this becoming a wrong Generalise |

**The evidence order**, mirroring `../../cs-context/references/evidence-standard.md` §8: written
commercial conditions > production workarounds observed in telemetry > written requests with the
job stated > verbal requests > internal opinion. State which rule you applied.

---

## 5. What the business model changes

| Model | What changes | What does not apply |
| --- | --- | --- |
| **Enterprise annual** | Standard shape. The opt-out deadline sets the decision window; carrying cost enters the renewal margin conversation | — |
| **Consumption / usage-based** | Price carrying per unit of throughput as well as per year. Add a 10× volume row: a bespoke path at $0.004/call is invisible at pilot volume and material in production | Seat-based ARR-at-stake arithmetic; use committed spend or trailing 90-day revenue |
| **Product-led / self-serve** | Default **Decline** with a configuration answer, said plainly. No services fee, no notice period, no account team to carry it | Gates 3 and 4 rarely reach a build. Do not manufacture an SOW |
| **Monthly evergreen** | No notice period, so the decision window is the next billing cycle. A horizon above one year needs a stated reason | `R1`'s notice-period arithmetic |
| **Regulated vertical** | Residency, retention, audit and export requirements are frequently **general**. Search the base before Gate 3 — the same requirement usually sits unasked in every regulated account | "Only this customer needs it" as a default assumption |
| **Channel / partner delivered** | The maintainer may sit at a partner you cannot page. No named human at the partner fails Gate 4 clause 2 | Internal escalation paths in the runbook entry |

---

## 6. The decision record

One page, written whatever the outcome, stored with the account. It exists so the decision is not
re-litigated from memory in six months by someone who was not there.

| Field | Content |
| --- | --- |
| Request, job, trigger | From §1, with the customer's words quoted and dated |
| Outcome and gate | The word, and the gate that returned it |
| Numbers | Principal, `TCO(N)`, interest rate, share of ARR, `N_evidenced`, `K*` |
| Rubric | All nine scores with evidence |
| Decision window | `renewal_date − notice_period_days − evidence_window`, with the date |
| Disposition | Graduation Contract (five fields) or the written decline with a revisit date |
| Falsifier | The 2–3 observable events that would flip a named gate |
| Assumptions | One row each, with a concrete consequence |

**A decline without a revisit date is not a decision, it is an ending** (`R14`). Give it a date —
usually the next annual cull, or the next renewal, whichever is sooner.

---

## 7. Reviewing a past decision

Run this when the `Stage` answer is *reviewing an old decision*, and once a year on every live
component (the annual cull, `carrying-cost.md` §6).

| Step | What you are testing |
| --- | --- |
| 1 | Re-run the gates with **today's** numbers — ARR moves, the supported path ships, the sponsor leaves |
| 2 | Compare actual carrying hours against the estimate. Record the ratio; it calibrates the next estimate |
| 3 | Check the Graduation Contract: did the owner stay? Did the product counterpart decide by the date? |
| 4 | Check `N_evidenced` again — a bespoke build that now has three G3 accounts behind it is a graduation, not a debt row |
| 5 | Return one of: **keep** (with a new review date), **graduate**, **migrate** to the supported path, **retire** |

**A component that cleared Gate 4 at $800k ARR does not clear it at $300k.** The commonest failure
of the review is treating the original decision as settled because it was made carefully.

---

## 8. Anti-patterns

| Anti-pattern | Correction |
| --- | --- |
| Scoring the artefact the customer described | Reduce to the job first (§1). Two "custom dashboards" are usually two jobs |
| Running the gates out of order, or revisiting an earlier one after a later match | First match returns the outcome. Print the rest as "not reached" |
| Treating an unowned roadmap item as a reason to wait | No owner, no increment, no gate. Dimension 3 scores 4 |
| A total rubric score used as the decision | The gates decide. The score is the record and the tie-break input |
| "Strategically important account" as a dimension | It is not one. Size justifies owning something explicitly (Gate 4), never skipping a gate |
| Scoring reversibility on how hard the code is to delete | Score it on what the customer's systems and staff now depend on |
| A counterfactual left implicit | Write the sentence. Implicit reads as "nothing happens" |
| Declining without a revisit date | `R14`. A decline is a written record with a date |
| Re-deciding from memory a year later | The decision record (§6), then §7 with today's numbers |
