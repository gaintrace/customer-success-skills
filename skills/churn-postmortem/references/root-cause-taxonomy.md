# The Root-Cause Taxonomy

> Free-text churn reasons cannot be aggregated, and anything that cannot be aggregated cannot be
> fixed. A quarter of losses coded in prose produces forty stories and zero decisions. This file
> is the closed vocabulary, the disambiguation rules that stop two people coding the same loss
> differently, and the crosswalk from what the customer said to what the timeline shows.
>
> Evidence labels: `[M]` measured · `[V]` vendor-published · `[P]` practitioner · `[A]` academic.

**Contents**
- [1. The three-part cause](#1-the-three-part-cause)
- [2. Fields, and the `churn_event` extensions](#2-fields-and-the-churn_event-extensions)
- [3. `primary_reason` — the thirteen values](#3-primary_reason--the-thirteen-values)
- [3a. The no-decision family, and the two-axis score](#3a-the-no-decision-family-and-the-two-axis-score)
- [4. `secondary_reason` — the compound rule](#4-secondary_reason--the-compound-rule)
- [5. The three axes: locus, origin stage, impact](#5-the-three-axes-locus-origin-stage-impact)
- [6. The coding decision tree](#6-the-coding-decision-tree)
- [7. Exit answers: the full bias table](#7-exit-answers-the-full-bias-table)
- [8. Stated reason → likely true reason](#8-stated-reason--likely-true-reason)
- [9. Mis-coding tells](#9-mis-coding-tells)
- [10. Governance](#10-governance)
- [11. Reason → family → what changes](#11-reason--family--what-changes)

---

## 1. The three-part cause

Every loss carries three separable things. Coding them into one field is the most common way a
loss-review dataset becomes useless.

| | Question it answers | Where it comes from | Tier | What it is evidence about |
| --- | --- | --- | --- | --- |
| **Stated reason** | What did the customer say? | Interview, cancellation form, the meeting where they told us | Observed — about a *conversation* | Their account of their decision |
| **Proximate cause** | What event converted a degrading account into a decision? | The timeline, within ~90 days of `decision_date` | Observed or Inferred | The account |
| **Root cause** | What condition on our side made that event decisive? | Five whys on the vendor-side chain | Inferred | **Us** |

`primary_reason` codes the **root cause**, not the stated reason. Where the two disagree, both are
recorded and the disagreement is itself a finding — a quarter in which the stated reason and the
coded reason agree on more than about 70% of records usually means the coder is reading the
survey, not the timeline.

## 2. Fields, and the `churn_event` extensions

`churn_event` in `../../cs-context/references/normalized-schema.md` already carries
`decision_date`, `effective_date`, `type`, `arr_lost`, `primary_reason`, `secondary_reason`,
`was_savable`, `earliest_detectable_signal` and `earliest_detectable_date`. This skill populates
those and adds the extensions below. **They extend the canonical entity; they do not create a
parallel vocabulary.**

| Field | Type | Notes |
| --- | --- | --- |
| `notice_date` | date | Notice served, or the opportunity moved to Closed Lost. The observed proxy when `decision_date` must be inferred |
| `decision_date_basis` | enum | `observed` · `inferred_autorenew` · `inferred_termination_request` · `inferred_competitor_named` · `inferred_procurement` · `inferred_export` · `proxy_notice_date` |
| `save_window_days` | int | `notice_date − decision_date`. How long we had once it was visible |
| `first_flagged_date` | date | First time anyone recorded the account as at risk anywhere |
| `first_intervention_date` | date | First action taken beyond recording it |
| `failure_mode` | enum | `absent` · `uninstrumented` · `unalerted` · `unrouted` · `unactioned` · `undetectable` |
| `locus` | enum | `vendor-controllable` · `jointly-controllable` · `customer-internal` · `market` |
| `origin_stage` | enum | `sales-qualification` · `onboarding` · `adoption` · `value-realisation` · `renewal-execution` |
| `surfaced_stage` | enum | Same vocabulary. Almost never equal to `origin_stage` |
| `health_at_t90` | enum + int | The band and score 90 days before `decision_date`. `green` here is a scoring defect |
| `stakeholder_change_involved` | bool + role | Champion or economic-buyer departure inside the window |
| `competitor` | string | Named **and confirmed by two independent sources**, or `none` / `in-house` / `no-replacement` |
| `competitor_claimed` | string | A rival named but never confirmed. This field exists so an unevidenced claim has somewhere to go that is not `competitor` |
| `decision_process_score` | int 0–5 | Count of decision-process markers present (§3a). Required on every record |
| `competitive_score` | int 0–5 | Count of competitive markers present (§3a). Required on every record |
| `active_decision_evidence` | list of dated events | The observable proof that the customer ran a decision. An empty list forces the no-decision family |
| `decision_owner_vacancy_days` | int or UNKNOWN | `decision_date` − last dated interaction with anyone holding renewal decision authority. `UNKNOWN` means no decision owner was ever identified, which is the finding |
| `systemic_fix`, `fix_owner`, `fix_due`, `fix_shipped` | text/date/bool | Mandatory. A post-mortem with no systemic fix is a eulogy |
| `facilitator` | string | Must differ from `account.owner_csm` |

**Trigger rule.** A record is required for every full churn, every downsell ≥20% of ARR, every
quasi-churn (>75% reduction with the logo retained), and every loss that was Green at T−90
regardless of size. Materiality thresholds below 20% are a local choice; the ≥20% floor is not,
because contraction that never gets reviewed is how a base shrinks without anyone deciding to
let it `[P]`.

## 3. `primary_reason` — the thirteen values

Adapted from GitLab's published risk-reason vocabulary in its public handbook `[P]`, which is
worth adopting closely because each definition carries its own disambiguation rule; extended with
`competitive-displacement` and `involuntary`, which most vocabularies fold into the wrong place,
and with the four no-decision values, which most vocabularies do not have at all.

**The no-decision family is walked first** — `no-decision`, `deprioritised`, `budget-freeze`,
`orphaned-renewal`, `budget-loss`. Each is a first-class cause with its own root-cause branch and
its own fix. None of them is an `other`, and none of them is a competitive loss.

| Value | Definition | Disambiguation — the line that decides it | Timeline evidence required | Mis-coding tell |
| --- | --- | --- | --- | --- |
| **`no-decision`** | The renewal lapsed. Nobody on the customer side ran a decision — no evaluation, no meeting, no owner, no argument against us | The absence of a decision event, not the presence of a reason. If anyone weighed us and chose otherwise, this is the wrong code | `active_decision_evidence` empty; C13 opportunity stalled or never opened; C12 no PO; no dated meeting where the renewal was discussed | Coded `other` because "they just went quiet" felt like no reason at all. Silence about a renewal is a reason with a date on it |
| **`deprioritised`** | The initiative the product served was shelved, paused or absorbed by a reorg. The product was not the subject of the decision | Their programme stopped, not their opinion of us. If the programme continued without us, it is `competitive-displacement` or `product-value-gap` | F5 reorg or department dissolution, F2 exec change, a named programme paused or deferred, project owner reassigned | Coded `corporate-decision`, which implies a policy. A deprioritisation has no policy, only an empty slot in someone's quarter |
| **`budget-freeze`** | Spend controls, a hiring or spend freeze, or a new approval threshold blocked a renewal nobody argued against | The money still exists; it stopped being spendable. Where the line item was structurally removed, that is `budget-loss` | F6 budget-cycle or freeze evidence, C12 PO not issued, a new signature threshold, procurement citing a control | Coded `budget-loss`, which sends the fix to segment strategy. A freeze is a paper-timing fix: `R7`, earlier, with the threshold known |
| **`orphaned-renewal`** | The champion or decision owner left, and **nobody on the customer side inherited the decision** | `sponsor-loss` is *we* lost our advocate and a decision still happened. This is *they* lost the owner and no decision happened at all | R1 departure, R3 no named sponsor, `decision_owner_vacancy_days` large or UNKNOWN, no successor engaged, C13 opportunity stalled from the departure date | Collapsed into `sponsor-loss`, which hides that the renewal was never argued. The fix differs: succession and a named decision owner, not multithreading alone |
| **`lack-of-adoption`** | Never adopted the product or the contracted feature set, so never experienced value | If they did not adopt **because they saw no value in what they did use**, it is `product-value-gap`. This code is for *never got going* | Activation event never fired, or fired and never repeated; `usage_daily.core_actions` never reached a steady state; V3 (contracted use case never went live) | Coded on an account with 14 months of steady usage — that is not non-adoption, it is value decay |
| **`product-value-gap`** | Used the product and did not get the outcome; capability did not meet the requirement | "Used and unimpressed" — distinct from "never used". If the capability existed and they could not reach it, that is `lack-of-adoption` | Sustained usage then decline; a named unmet requirement in tickets, transcripts or the success plan; V2 (no ROI evidence) | The catch-all. If more than a third of a quarter's ARR lands here, the coder is using it as a synonym for "we lost" |
| **`product-quality`** | Used it; defects, performance or availability made it unreliable | Quality ≠ capability. A missing feature is `product-value-gap`; a feature that breaks is this | P1/P2 history, repeat issues (P3), SLA breaches, incident records touching this account | Coded from a single loud escalation with no ticket-history support |
| **`sponsor-loss`** | Champion or economic buyer left, changed remit, or went unresponsive, and the relationship was never re-established | The most under-coded reason in most organisations. Code it whenever R1 fires inside the window **and** no successor was engaged, even when another reason also applies | `contact.departed_at`, `email_status = hard_bounce`, multithread depth ≤1, no buyer-side interaction in 90 days | A quarter with zero `sponsor-loss` records. Departures happen; a zero means nobody looked |
| **`budget-loss`** | Business contraction, headcount reduction, or the line item was structurally removed | **Explicitly not a competitive loss.** If the money went to another vendor, code `competitive-displacement`; if it was frozen rather than removed, code `budget-freeze` | External evidence: layoffs, filings, down round; DSO deterioration; deprovisioning burst matching headcount | The face-saving code. Used to make a loss nobody's fault. Requires external corroboration to stand |
| **`corporate-decision`** | Top-down mandate — ELA, single-provider policy, platform standardisation | Not driven by our gaps or their adoption. If a gap gave the mandate its argument, that gap is the `secondary_reason` | A named policy, an announced consolidation, procurement contact confirming a mandate | Coded from a rumour relayed by a mid-level contact |
| **`competitive-displacement`** | Replaced by a named alternative, including an in-house build | Requires a named replacement **confirmed by two independent sources** and a competitive score ≥3 (§3a). Below that bar the claim goes to `competitor_claimed` and the record codes from the no-decision family | R13 competitor named, a re-bid or RFP, the replacement confirmed at interview | Coded because a competitor was mentioned once, eight months earlier, by a junior user |
| **`involuntary`** | Payment failure, card expiry, or a billing-process defect ended the subscription | Nothing to do with satisfaction. Rule this out first, before any narrative | `invoice.payment_failures`, `payment_method_status`, dunning history, no cancel-intent event | Coded as voluntary because the customer never complained — they never knew |
| **`other`** | Genuinely outside the above | Requires a written justification and is reviewed quarterly | — | Share above 15% means the taxonomy needs a new category, not that reality is messy |

**Involuntary is bigger than teams assume, and smaller at the top of the market.** Recurly's
July 2026 network data reports SaaS median annual churn of 3.22% — 2.16% voluntary and 1.06%
involuntary — while enterprise SaaS above $250 ARPC shows 3.54% overall with only 0.18%
involuntary `[M]`. Read that as: in a self-serve or SMB base roughly a third of losses may be a
billing problem wearing a satisfaction costume; in an enterprise base an involuntary loss is a
process defect rare enough to deserve its own review.

## 3a. The no-decision family, and the two-axis score

Most renewals are not lost to a rival. They are lost to inertia, a reorg, a spend freeze, or a
champion who left with nobody picking up the file. Competitive positioning against a named rival
is, most of the time, solving a problem the account did not have — and a competitive code sends
the fix to enablement, which cannot move a renewal nobody was arguing about.

So the record scores two axes separately, and prints both. **A high competitive score does not
lower the decision-process score, and vice versa** — they are different failures with different
owners, and collapsing them into one "risk" is what produces the battlecard nobody reads.

### The markers — one point each, every one needing a dated timeline event

| # | Decision-process marker | Evidence it needs |
| --- | --- | --- |
| 1 | Renewal opportunity stalled in one stage for ≥2× the segment's median cycle, or was never opened (C13) | `opportunity.stage_changed_at` history, or the absence of an opportunity record |
| 2 | PO not issued or budget not allocated by T−30 (C12), **or** a spend freeze or new approval threshold (F6) | Procurement email, a named control, the PO record |
| 3 | Reorg, department dissolution or exec change that absorbed the sponsoring programme (F5, F2) | An announcement, an org-chart change, a project owner reassigned |
| 4 | The decision owner left and no successor was engaged (R1, R3) | `contact.departed_at`, hard bounce, no successor interaction on record |
| 5 | No bilateral contact in the 60 days before `decision_date` (Z1) | Last two-way interaction, dated |

| # | Competitive marker | Evidence it needs |
| --- | --- | --- |
| 1 | A rival named by an **economic buyer**, dated (R13) | The transcript line, the ticket, the email — with the speaker's role |
| 2 | A re-bid, RFP or formal vendor comparison run by procurement (R11) | The request, the scoring sheet, the vendor list |
| 3 | Termination or data-portability request in the same window as a named alternative (R12) | Both events, dated, inside 90 days of each other |
| 4 | The replacement confirmed by a **second independent source** | The customer at interview, a public reference, a job posting or tooling change naming it |
| 5 | A concession demanded citing a named alternative's price (C6) | The number they quoted, and where it came from |

### Reading the pair

| Decision-process | Competitive | What it is | Where the fix goes |
| --- | --- | --- | --- |
| ≥3 | ≤1 | A renewal nobody decided | Decision-process: a named decision owner on the account, a T−180 opt-out-calendar gate (`R1`), a pre-wired approval path with procurement (`R7`). **Competitive enablement is refused** |
| ≥3 | ≥3 | A stalled renewal a rival then walked into | Both, in order: the decision process first, because it created the opening |
| ≤1 | ≥3 | A genuine bake-off we lost | Competitive: the re-bid play, enablement, the gap ranked by lost ARR |
| ≤1 | ≤1 | Neither axis is evidenced | Nothing has been established yet. Go back to the timeline before coding anything |

### The three refusals

1. **`competitive-displacement` below the bar.** Competitive score <3, or no replacement confirmed
   by two independent sources: store the claim in `competitor_claimed`, code from the no-decision
   family, and say in the record that the destination was never confirmed. A single competitor
   mention by a junior user eight months out is not a displacement.
2. **No competitive fix on a decision-process loss.** Decision-process ≥3 with competitive ≤1: the
   Step 8 fix must be a decision-process fix. Battlecards, competitive enablement and price
   response are unavailable, because none of them puts a name against the decision.
3. **No `other`, no `undetectable`, for a lapse.** A renewal that lapsed always has an antecedent —
   a stalled opportunity, an unissued PO, a vacant decision owner, sixty silent days. Code
   `no-decision`, `deprioritised`, `budget-freeze`, `orphaned-renewal` or `budget-loss`, and assign
   a real failure mode.

### `decision_owner_vacancy_days`

`decision_date` − the last dated interaction with anyone holding renewal decision authority.
Computed on every record from the timeline, never recalled. Three readings:

| Value | What it means | What it changes |
| --- | --- | --- |
| 0–30 | A decision owner was live and engaged | The loss was decided, not defaulted. Look for a real cause |
| >90 | The decision was made by an empty chair | `orphaned-renewal` or `no-decision`, and the fix is succession, not adoption |
| `UNKNOWN` | We never identified who held the decision | The finding itself. Route to `stakeholder-map`; a renewal run without a named decider is the defect |

## 4. `secondary_reason` — the compound rule

Losses are compound. A single-valued reason field compresses a Decapitation-plus-Value-vacuum
into whichever code the coder happened to reach for.

| Rule | Detail |
| --- | --- |
| Zero or more values, same vocabulary | No cap, but each one needs its own timeline evidence |
| Never restate the primary | `product-value-gap` primary with `product-value-gap` secondary is a coding error |
| `sponsor-loss` is recorded whenever it applies | Even when it is not primary. It is the most frequently omitted contributor and the aggregate is what justifies a multithreading threshold |
| Order matters | List secondaries in the order they appear on the timeline — that ordering is what reveals origin vs surface |
| Reported separately in aggregates | Report primary-only mix **and** any-mention mix. They tell different stories, and the gap between them is where the unfixed contributors live |

## 5. The three axes: locus, origin stage, impact

| Axis | Value | Meaning | What it generates |
| --- | --- | --- | --- |
| **Locus** | `vendor-controllable` | We could have changed the outcome unilaterally | A systemic fix |
| | `jointly-controllable` | Required us and them | A systemic fix plus a joint-accountability change (success plan, mutual plan) |
| | `customer-internal` | Their reorg, their budget, their politics | A qualification or coverage change, not a fix |
| | `market` | Consolidation, category shift, macro | Strategy input. Track the rate; fix nothing |
| **Origin stage** | `sales-qualification` | Sold outside the ICP, or a requirement never in scope | Sales and deal-desk gates |
| | `onboarding` | Never reached the activation event; go-live overran | Onboarding exit criteria |
| | `adoption` | Went live, never broadened or deepened | Adoption plays and instrumentation |
| | `value-realisation` | Adopted, but the outcome was never measured or proven | Baseline capture, QBR content |
| | `renewal-execution` | Value existed; the renewal was run badly or late | Renewal runbook and the opt-out calendar |
| **Impact** | `full-churn` · `tier-downgrade` · `seat-churn` · `quasi-churn` | Maps to `churn_event.type` | Which retention metric the loss lands in |

**Origin is almost never where it surfaced.** A loss that surfaces at `renewal-execution` and
originated at `sales-qualification` produces a *sales* fix; coding only the surface produces a
renewal-process fix that cannot work. Code both, and report the origin mix separately — it is
usually the single most surprising table in the quarterly pack.

## 6. The coding decision tree

Walk it in order. The first branch that matches wins the `primary_reason`; everything else that
applies becomes a `secondary_reason`.

```
1. Was there a cancel-intent event, or only a payment failure?
     payment failure only ......................... involuntary        → stop

--- the no-decision family: walked BEFORE any competitor question ---

2. Is `active_decision_evidence` empty -- no evaluation, no meeting, no owner,
   no argument against us?
     yes ......................................... no-decision
3. Was the programme we served shelved, paused or absorbed by a reorg?
     yes ......................................... deprioritised
4. Did a spend freeze or a new approval threshold block it, with the
   line item still nominally in place?
     yes ......................................... budget-freeze
5. Did the decision owner leave with nobody on their side inheriting the
   decision (decision_owner_vacancy_days > 90, or UNKNOWN)?
     yes ......................................... orphaned-renewal
6. Did the budget line disappear structurally, with external corroboration?
     yes ......................................... budget-loss

--- everything else ---

7. Is there a named replacement, confirmed by two independent sources,
   with competitive_score >= 3?
     yes ......................................... competitive-displacement
     named but unconfirmed ....................... record competitor_claimed; the claim
                                                  wins nothing. Re-walk steps 2-6 with the
                                                  competitor evidence excluded, then go on
                                                  to step 8
8. Was there a top-down mandate, policy or ELA naming the standard?
     yes ......................................... corporate-decision
9. Did the champion or economic buyer leave/disengage with no successor
   engaged, and a decision was still made?
     yes ......................................... sponsor-loss
10. Did they use it, and were the defects or outages the complaint?
     yes ......................................... product-quality
11. Did they use it, and did the capability not meet the requirement?
     yes ......................................... product-value-gap
12. Did they never get going -- activation never fired, use case never live?
     yes ......................................... lack-of-adoption
13. None of the above, with a written justification ... other
```

**Why the order changed.** Asking "who did they choose?" before "did they choose?" is how a
lapsed renewal becomes a competitive loss and the fix becomes a battlecard. Steps 2–6 are the
no-decision family: five first-class causes, each with its own root-cause branch, none of them an
`other` bucket. Nothing reaches step 7 until the timeline has been searched for a decision and
none was found to exist.

Three overrides on the tree. **Step 9 is recorded as a secondary whenever it applies**, even when
a later branch takes the primary. **Step 6 requires corroboration**: a customer saying "budget"
without layoffs, filings, deprovisioning or DSO movement is a stated reason, not a coded one. And
**step 13 is unavailable to a lapse** — where no decision event exists, one of steps 2–6 is the
answer, however unsatisfying it feels to write down.

## 7. Exit answers: the full bias table

Post-churn feedback is worth collecting — Clozd's argument is that it is often the most honest
feedback available "because the customer no longer has a vested interest in maintaining a
relationship" `[V]`. But it is honest and *biased*, which are different things. Correct for the
direction rather than discounting the answer.

| Bias | Mechanism | Direction of error | Counter-question that works |
| --- | --- | --- | --- |
| **Escape** | Asked at the cancellation moment, the customer wants out of the conversation. Lincoln Murphy: "they'll tell you whatever they think you need to hear to just let them out" `[P]` | Over-reports price and budget; under-reports "we never got it working" | Ask 2–4 weeks after the effective date: "when you look back, what was the first month you thought this probably wasn't going to work?" |
| **Face-saving** | Naming our failure means criticising their own vendor choice, in front of a vendor | Over-reports `corporate-decision` and `budget-loss` | "Walk me through how the decision got made — who raised it first, and when?" Process questions are safe to answer honestly |
| **Relationship preservation** | They may need a reference, a re-hire, or a favour | Over-reports "great product, wrong time" | Interviewer is not the account owner. State plainly that the contract is closed and nothing is being sold |
| **Respondent** | The person who replies is the one still there and still fond of us | Under-reports `sponsor-loss` and buyer disconnect | Target the economic buyer by name; record who answered and their role on the record |
| **Reason-field** | The account owner fills the picklist to close the record cleanly — price is the answer that reflects on nobody | Over-reports price; under-reports anything touching the account team | The facilitator codes from the timeline. The owner's picklist entry is stored as `stated_reason`, never as `primary_reason` |
| **Recency** | The last bad thing dominates the account of a fourteen-month decline | Over-reports the proximate cause as the root cause | Build the timeline first, then ask about specific dated events rather than "why" |
| **Single-cause** | The form takes one value | Compresses compounds into whichever code came first | `primary_reason` + `secondary_reason`, and report both mixes |
| **Sampling** | Only amicable churns answer | Skews the whole quarter's reason mix toward polite reasons | Report interview response rate **and** the ARR coverage of the interviewed set beside every reason table |
| **Interviewer** | An account owner hears confirmation of what they already believed | Reinforces the existing reason mix quarter after quarter | Rotate facilitators; a third party for the largest losses |

## 8. Stated reason → likely true reason

Not a decoder ring — a list of the tests to run before accepting the stated reason at face value.

| They said | What it often is | The test on the timeline |
| --- | --- | --- |
| "Too expensive" | `product-value-gap` — the price was the same on the day they signed | Was there value evidence (V2)? Did they renew at this price before? Did they buy something else instead? |
| "Budget was cut" | `budget-loss` if corroborated; otherwise `product-value-gap` | Layoffs, filings, DSO deterioration, deprovisioning matching headcount. No corroboration → not budget |
| "We're consolidating vendors" | `corporate-decision` or `competitive-displacement` | Is there a named surviving standard? Did procurement or a new exec appear (R11/F2)? |
| "We built it in-house" | `competitive-displacement` (`in-house`) with a `product-value-gap` secondary | What did the build replace — the whole product or one workflow we never delivered? |
| "We didn't have the resources to use it" | `lack-of-adoption`, origin `onboarding` | Did the activation event ever fire? Whose tasks were blocked — ours or theirs? |
| "It didn't do what we needed" | `product-value-gap` — but check whether it *could* and they never found it | Feature breadth vs plan; was the requirement in the original business case (V4 value drift)? |
| "There was a reorg" | `sponsor-loss` first; `corporate-decision` only with a policy | Who left, when, and was a successor ever engaged? |
| "We just weren't using it" | `lack-of-adoption` or `product-value-gap` depending on whether they ever started | Did usage ever reach a steady state, or never start? That single question splits the two codes |
| "Support was a nightmare" | `product-quality` if the tickets support it; `sponsor-loss` if one person's patience ran out | Repeat issues (P3), reopens, P1 ageing, CSAT trend, and whether it reached decision-makers |
| "We just never got round to it" / "it slipped" | `no-decision` — a lapse, not a verdict | Was an opportunity ever opened? C13 stage history, and whether any meeting on the renewal exists |
| "It's on hold" / "the project got paused" | `deprioritised` | Which programme stopped, when, and who reassigned its owner (F5, F2) |
| "There's a spend freeze" / "it needs CFO sign-off now" | `budget-freeze` if the line item survives; `budget-loss` if it was removed | The control itself: the new threshold, the freeze memo, C12 PO status. A freeze is a `R7` paper-timing fix |
| "We're between owners" / "nobody has picked this up" | `orphaned-renewal` | `decision_owner_vacancy_days`; who left, when, and whether any successor ever interacted with us |
| Nothing — they went silent | `no-decision` or `orphaned-renewal` first, then `lack-of-adoption` or `sponsor-loss`; never `other` | Silence is a finding: Z1/Z4 with the date the last bilateral interaction happened, and whether a decision owner existed at all |

## 9. Mis-coding tells

Run these against any quarter's records. Each is a signature of coding drift rather than reality.

| Tell | What it usually means | Correction |
| --- | --- | --- |
| Price/budget above ~30% of records | Reason-field and escape bias, not a pricing problem | Recode from timelines; compare stated vs coded mix |
| Zero `sponsor-loss` in a quarter | Nobody checked contact departures | Run the departure sweep across all losses before coding any |
| `other` above 15% | The vocabulary is missing a category | Cluster the `other` records; propose one new value with a definition and a disambiguation rule |
| Stated and coded reason agree >70% of the time | The coder is reading the survey | Re-code a sample blind from timelines only and compare |
| `origin_stage` always equals `surfaced_stage` | Origin is not being analysed at all | Every record must answer "where did this start?" separately |
| >60% coded not-savable (A or B) | Bad qualification, or defensive coding | Report A+B and C+D separately and defend the split `[P]` |
| Every record coded by the account owner | Structural defensiveness | `facilitator ≠ account.owner_csm`, enforced as a field |
| `competitive-displacement` share above the no-decision family's share | Almost always coding drift. Named rivals are memorable; empty chairs are not | Re-test every competitive record against the two-source confirmation bar. Unconfirmed ones move to `competitor_claimed` |
| Zero records in the no-decision family across a quarter | Nobody asked whether a decision happened | Re-code from `active_decision_evidence`: how many losses had no evaluation, no meeting and no named decider? |
| `decision_owner_vacancy_days` absent or UNKNOWN on most records | The renewal decider was never identified while the account was alive | A `stakeholder-map` gap, not a post-mortem gap. Report the count; it is the strongest argument for the field existing |
| Reason mix stable for four quarters while ARR churn moves | The codes are decorative | Audit ten records against their timelines |

## 10. Governance

| Question | Answer |
| --- | --- |
| Who codes? | A facilitator — CS Ops or a manager who did not own the account. The owner contributes evidence and reviews, and may dissent on the record |
| When? | Within 30 days of the decision date, while the customer will still talk and while the data still exists |
| Who assigns savability? | The facilitator, never the owner. Distribution is reported quarterly |
| What if the owner disagrees? | Record the dissent in one line with its reasoning. Do not average two codes into a third |
| Can `primary_reason` change later? | Yes, once, if the interview or new evidence contradicts the timeline. Log the change, the date and why — a silently re-coded record destroys trend analysis |
| Vocabulary changes? | Quarterly only, with a restatement of the prior four quarters under the new vocabulary. Adding a category mid-quarter breaks every trend line |
| `other` budget | 15% of records. Above it, the review is of the taxonomy, not of the losses |
| Can `other` absorb a lapse? | No. Where the timeline holds no decision event the record codes into the no-decision family. `other` is for causes outside the vocabulary, not for causes that felt like an absence |
| Who signs off a `competitive-displacement`? | The facilitator, against the two-source bar and `competitive_score` ≥3. An unconfirmed rival is stored in `competitor_claimed` and reported separately, so the competitive share of the quarter stays honest |

## 11. Reason → family → what changes

The point of coding is routing. Each reason has a home family in
`../../cs-context/references/signal-library.md` and an owning skill.

| `primary_reason` | Home signal family | Signals that should have fired | Where the fix goes |
| --- | --- | --- | --- |
| `lack-of-adoption` | Product usage & adoption | U8 activation regression, U9 TTFV overrun, V3 use case never live, Z4 dark account | `onboarding-plan` — exit criteria and activation gates |
| `product-value-gap` | Sentiment & VoC + value realisation | V2 no ROI evidence, V4 value drift, V5 buyer cannot articulate value | `qbr-builder` and Product, ranked by lost ARR |
| `product-quality` | Support & reliability | P3 repeat issue, P5 P1 ageing, S2 CSAT decline, P9 blocking request rejected | Engineering, with the ARR attached |
| `sponsor-loss` | Relationship & engagement | R1 champion departure, R2 sponsor disengagement, R4 single-threading, Z1 silence | `churn-risk` override floors and a multithreading threshold |
| `no-decision` | Commercial & contract | C13 opportunity stagnation, C12 PO not issued, Z1 silence | `renewal-prep` — a named decision owner and a T−180 opt-out-calendar gate (`R1`) |
| `deprioritised` | Firmographic & external | F5 reorg, F2 exec change, V1 unmet milestones | `success-plan` — re-anchor to a programme that survived, or downsell deliberately |
| `budget-freeze` | Commercial & contract | F6 budget cycle, C12 PO not issued, R11 procurement | `renewal-prep` — paper starts at T−90 (`R7`) with the approval threshold known in advance |
| `orphaned-renewal` | Relationship & engagement | R1 champion departure, R3 no named sponsor, C13 stagnation | `stakeholder-map` — a named decision owner per account, and 48-hour exec-to-exec succession (`R3`) |
| `budget-loss` | Firmographic & external | F3 layoffs, F4 financial distress, C8 DSO deterioration, U14 deprovisioning | Segment strategy and downsell-over-logo-loss policy |
| `corporate-decision` | Firmographic & external | F2 exec change, R11 procurement re-engagement | Exec relationship coverage above an ARR threshold |
| `competitive-displacement` | Commercial & contract | R13 competitor named, R11/R12 procurement and termination terms, C1 auto-renew off | Competitive enablement and the re-bid play |
| `involuntary` | Billing & payment | Payment failures, `payment_method_status`, dunning outcomes | Billing operations — dunning, retries, card updater |
| `other` | — | — | Taxonomy review |
