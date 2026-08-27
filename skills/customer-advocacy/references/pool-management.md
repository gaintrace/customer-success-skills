# Advocate Pool Management

> Capacity, rotation, coverage cells, fatigue measurement, the register, and how to recover a
> burned advocate. The premise: **the advocate pool is a finite, depleting, replenishable asset**,
> and over-asking a good reference is a real relationship risk — and a churn signal in itself.
>
> Defaults marked `[P]` are library conventions, not measured benchmarks. Replace them with your
> own observed decline rates once you have twelve months of register data.

**Contents**
[Why a pool needs managing](#why-a-pool-needs-managing) · [Capacity](#capacity-the-spend-limits) ·
[Coverage cells](#coverage-cells-the-supply-side) · [Rotation](#rotation-who-goes-next) ·
[Fatigue](#fatigue-measured-not-felt) · [The register](#the-register) ·
[Job runbooks](#job-runbooks) · [Recovering a burned advocate](#recovering-a-burned-advocate) ·
[Advocacy as a retention signal](#advocacy-as-a-retention-signal) ·
[Programme metrics](#programme-metrics-and-the-attribution-problem)

---

## Why a pool needs managing

Demand for references is continuous and supply is not. Left unmanaged, three things happen in
order, and they happen to every programme that has not built the controls:

1. **Concentration.** The four customers who said yes first get asked for everything, because they
   are the ones the desk remembers.
2. **Silent depletion.** Their replies slow, then shorten, then stop. Nobody records this, because
   nothing was ever recorded.
3. **Attribution failure.** When one finally declines, it is filed as a scheduling problem — not
   as the relationship signal it is.

`[V]` UserEvidence reports that **53% of sellers say a lack of relevant customer evidence has
slowed or negatively impacted their sales process** — a demand-side pressure that makes the
concentration failure feel like diligence at the time.

The controls below exist so the depletion is visible before the decline.

---

## Capacity: the spend limits

An advocacy ask is a withdrawal. Set the overdraft limit before the request arrives, not while
someone is waiting on an answer.

| Control | Default `[P]` | Rationale | Override when |
| --- | --- | --- | --- |
| Asks per customer per rolling 12 months | **3** across all rungs | Past three, declines rise and reply latency lengthens before anyone names it fatigue | Customer-initiated asks are free and do not count |
| Sales reference calls per customer per year | **4**, max **1 per quarter** | Highest repeat demand, lowest visible reward — their manager never sees the cumulative cost | Never; this is the burn rung |
| Minimum rest between any two asks | **45 days** | Recovery, and it mechanically forces rotation | A milestone opens a 14-day window and the last ask was rung 1 |
| Separation from any commercial ask | **14 days either side** (`R11`) | An ask next to an upsell reads as leverage, permanently | Never |
| Open asks per customer at any time | **1** (`R17`) | Two open asks is how a yes becomes a silence | Never |
| Advance notice before a scheduled commitment | **5 working days** | Below that you are asking for a favour, not making a request | Their own urgency |
| Advocates per coverage cell | **≥3** | Below three, one holiday empties the cell and the same person gets called | — |

**Rungs are not equal withdrawals.** Weight them when counting against the annual cap:

| Rung | Cost against the 3-per-year cap |
| --- | --- |
| 1 Survey | 0 — an input, not a spend |
| 2 Testimonial · 3 Review · 4 Logo | 0.5 each |
| 5 Case study · 6 Webinar | 1.0 each |
| 7 Conference | 1.5 |
| 8 Reference call | 0.5 per call, counted separately against the 4/year limit |
| 9 Advisory board · 10 Co-development | Excluded — governed by their own term, and members are exempt from the general cap for the duration |

---

## Coverage cells: the supply side

A pool is not a list, it is a **grid**. The unit of supply is the cell a prospect's question falls
into, and a pool of twelve advocates who all look alike has one cell filled and eleven empty.

**Cell definition:** `segment × industry × use case × buyer persona`. Add `deployment shape` where
it materially changes the story (on-prem vs multi-tenant, single vs multi-entity).

| Cell | Advocates | Status | Nearest candidate |
| --- | --- | --- | --- |
| Enterprise × logistics × intercompany close × Ops exec | 3 | ✅ Covered | — |
| Enterprise × logistics × intercompany close × CFO | 1 | ⚠️ Thin | Kestrel — CFO engaged, readiness 71, 60 days from rung 5 |
| Mid-market × manufacturing × inventory sync × IT | 0 | ❌ Empty | Verdanta — readiness 68, D5 clears 2026-11-02 |

**Target ≥3 per cell**, because one holiday, one reorg and one open Sev-1 will take out two.
**Report the empty cells in every artifact** — an empty cell is a measurable revenue drag, and it
is the only piece of this analysis that tells the business where to invest in advocacy supply.

**Recruit against the gap, not against enthusiasm.** The right question at a quarterly pool review
is not "who else likes us?" but "which cell is empty, and which two accounts are 90 days from
filling it?"

---

## Rotation: who goes next

```
Routing score = (readiness / 100) × fit − recency_penalty − fatigue_penalty

fit             = 1.0 exact cell · 0.7 adjacent cell (same persona, near use case)
                  · 0.4 same segment only · 0.0 no match — do not route
recency_penalty = 0.5 if last ask < 45 days · 0.25 if 45–90 days · 0 beyond
fatigue_penalty = 0.5 if two of four fatigue observables are trending wrong
```

Rank descending and route the top eligible candidate. **Never rank by willingness** — the most
willing advocate is the one you are about to burn, and willingness is the last tiebreak, not the
first filter.

**Fit 0.0 means decline the request.** Telling a seller "no suitable reference in that cell, here
is what I can offer instead" is a legitimate answer and a far better one than routing a mismatch:
the prospect hears a customer describing a different product, and the advocate is spent for
nothing. Give the seller the alternatives — an anonymised outcome summary, a review-site profile
filtered to their segment, a peer intro that is not a reference call — and log the unfilled
request against the supply ratio.

---

## Fatigue: measured, not felt

Four observables per advocate per quarter. **Two of four trending wrong means rest the advocate**
and record it; three means freeze them for two quarters and open the repair path.

| Observable | Measure | Trending wrong when |
| --- | --- | --- |
| **Reply latency to advocacy asks** | Median hours to first reply on advocacy threads, vs their own baseline on all threads | ≥2× their own baseline, or ≥5 working days |
| **Declines in trailing 12 months** | Count from the register | ≥1 |
| **Enthusiasm delta** | Length and specificity of their reply, first ask vs latest | Latest reply is under half the length, or has become logistics-only |
| **Delegation drift** | Who answers | The ask is being redirected to someone more junior, or to a shared mailbox |

**Latency against their own baseline, not against an average.** An executive who takes three days
to answer everything has not become fatigued by taking three days to answer this.

**Delegation drift is the earliest of the four** and the most often misread as helpfulness. A
champion who forwards your reference request to their analyst has stopped treating it as something
they personally do — which is a relationship signal before it is a fatigue signal
(`stakeholder-map`).

---

## The register

One row per **ask**, written when the ask is **sent**, not when it is answered. An unlogged ask is
how one customer gets asked twice in a fortnight by two teams.

| Field | Notes |
| --- | --- |
| `account_id`, `contact_id` | From `../../cs-context/references/normalized-schema.md` |
| `rung` | 1–10 |
| `asked_by`, `asked_on` | The human and the date |
| `channel` | Email, call, in-QBR |
| `outcome` | `accepted` · `declined` · `withdrawn` · `no_response` · `deferred` |
| `outcome_on`, `decline_reason` | Free text is acceptable here; the pattern matters more than the taxonomy |
| `delivered_on` | The date the act actually happened — accepted is not delivered |
| `cost_weight` | From the rung table above |
| `next_eligible_on` | Computed: `max(last_ask + 45d, cap reset)` |
| `fit_cells` | The cells this advocate covers |
| `approval_owner`, `approval_expires` | Theirs, with the date the permission lapses |
| `what_we_gave_back` | The currency delivered, and when. **Blank here is a debt** |

**`what_we_gave_back` is the field that keeps the pool alive.** A programme that records only what
it took from customers is a programme that will run out of them. Review the blank rows at every
quarterly pool review and clear them before asking anyone for anything new.

**`approval_expires`** prevents the most common legal failure: a logo or quote still published
under a permission that lapsed with the contract term or with the departure of the person who gave
it. Re-confirm annually, and on any champion change.

Emit and maintain it with `../assets/advocacy-register.md`; compute caps, rotation scores and
next-eligible dates with `../scripts/advocacy_score.py`.

---

## Job runbooks

| Job | Sequence | Output |
| --- | --- | --- |
| **Fill a named request** | Fit cell → eligible set → disqualifiers → rotation score → top candidate + one backup → ask written → register | Shortlist, the ask, the decline path if fit is 0.0 |
| **Build the pool** | Score the book → disqualifiers → ladder ceiling per account → map to cells → name the empty cells and the nearest candidates | Register, coverage grid, recruitment list |
| **Pool health check** | Caps consumed → fatigue on all four observables → declines and withdrawals in 12 months → blank `what_we_gave_back` rows → cells that went thin | Rest list, repair list, supply gaps |
| **Repair** | Diagnose the burn → freeze → deliver with no ask → return control → re-open at the freeze date at one rung lower | The repair note, a dated freeze, a revised cap |

---

## Recovering a burned advocate

Four burns. They look identical from the outside and need different repairs; diagnosing the wrong
one makes it worse, because the apology names something that was not the problem.

| Burn | What happened | Tell | The repair |
| --- | --- | --- | --- |
| **Over-asked** | Too many asks, too close together, usually across teams who could not see each other | Latency rising, replies shortening, still saying yes | Stop and say why. Name the count out loud. Freeze ≥90 days. Return with a **cap they set** |
| **Mismatched** | Sent into a call outside their cell — a hostile prospect, a use case they do not run, a question they could not answer | One bad call, then declines | Apologise for the specific call, not for asking. Show the fit rule you have added. Next ask is a rung lower and inside their cell |
| **Unrewarded** | They gave repeatedly and got nothing back | Blank `what_we_gave_back` rows | Deliver the currency first, with no ask attached and no mention of a future one. Then wait a full quarter |
| **Exposed** | Something published they did not approve, a quote out of context, their name where they expected anonymity | Cold, formal, sometimes their legal team | Take it down the same day. Then the note — no ask for at least two quarters, and give them approval rights over anything of theirs still live |

**Five rules for every repair:**

| Rule | Why |
| --- | --- |
| Name it in the first sentence (`R20`) | They already know. Leading with anything else says you did not notice |
| Apologise once | A second apology asks them to absolve you, which makes your feelings their job |
| Attach no ask, in any form | "Let me know if you'd ever want to..." is an ask |
| Hand back control — a cap, a veto, approval rights, dates they choose | The burn was a loss of control. Returning it is the repair |
| State the freeze with a date, and keep it | A freeze you break at week six confirms the original problem |

**Exposure is the one burn that is often unrecoverable.** Treat prevention as the control: nothing
publishes without written approval of the final version, and approvals expire.

---

## Advocacy as a retention signal

The register is a relationship instrument, not just a scheduling tool. Read it in both directions.

| Observation | Read as | Action |
| --- | --- | --- |
| **Agreed, then withdrew** | **P0.** Something changed that no survey has caught. A customer who publicly bound themselves and then unbound has revised their view | Run `churn-risk` this week. Do not re-ask. Do not ask them why in the same message as anything else |
| A previously willing advocate declines with no reason | Champion standing has changed, or an internal issue exists we cannot see | One question, no ask attached: "has something changed I should know about?" |
| Decline rate rising across a segment or cohort | A product, support or pricing problem ahead of the survey curve — advocacy declines lead NPS movement | Route to `voice-of-customer` as a cohort finding, not an account one |
| An advisory board member resigns mid-term | P0, same as a withdrawal, with an executive attached | `churn-risk` plus exec-to-exec contact inside 48 hours (`R3`) |
| They accept but ask to see the questions first | Governance, not reluctance | Send them. This advocate is strengthening |
| They volunteer an ask you did not make | The strongest positive signal in the register | Log it, take it, and do not immediately stack a second |

**Why withdrawal is stronger evidence than a survey.** A survey response costs nothing and is
often given to be polite. Agreeing to speak to a prospect is a public, personal commitment; taking
it back means the customer has reassessed something they had already decided. That is a revision
of position, and revisions are rarer and more informative than opinions.

---

## Programme metrics and the attribution problem

| Metric | Definition | Honest reading |
| --- | --- | --- |
| **Customer-sourced pipeline** | Opportunity $ where the source field records a referral or introduction from an existing customer | The most defensible number the programme produces. Attributable, auditable, and it belongs to advocacy |
| **Advocacy-influenced pipeline** | Opportunity $ where an advocacy act touched the cycle | Real, useful, and **never added to sourced**. Report side by side, sum neither |
| **Advocacy rate** | Customers with ≥1 advocacy act in TTM ÷ eligible customers | An input measure. Rising rate with a falling supply ratio means you are asking the same people more |
| **Reference supply ratio** | Requests fulfilled ÷ requests received | The measurable drag. A falling ratio is a business problem before it is a CS one |
| **Decline rate** | Declines ÷ asks, trailing 12 months, by segment | The pool's leading health indicator. Track the trend, not the level |
| **Cell coverage** | Cells with ≥3 advocates ÷ total cells | Where to invest in supply |

**The confounding caveat, stated every time.** Advocates are selected for health, so "accounts
that gave a reference retain better" is confounded: you chose your healthiest customers. Match the
comparison on segment, ARR band, tenure and prior-period health, or report it as correlational and
say so. `[P]` The same methodological warning applies to any "customers with QBRs retain better"
claim, and for the same reason.

**The late-cycle attribution trap.** A reference call placed in week nine of a twelve-week cycle
takes credit in the CRM for a deal that was substantially won in week three. A review read before
the prospect ever identified themselves gets no credit at all. `[M]` TrustRadius / Pavilion's
*2024 B2B Buying Disconnect* (2,164 buyers, 243 vendors) found **78% of buyers selected products
they had heard of before research began — 86% of enterprise buyers**, which is exactly the
influence that never appears in a source field.

Report influence as influence. Claim causation only where you ran a holdout, and say so when you
did not.
