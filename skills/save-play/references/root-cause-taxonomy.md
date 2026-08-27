# Root-Cause Taxonomy

> Eleven causes. The play is entirely determined by which one it is, so this file exists to stop
> you choosing the wrong one — and every cause below is defined by the test that separates it from
> its nearest neighbour, not by a description you could nod along to.
>
> A cause is **primary** if removing it would have changed the outcome. Everything else is
> contributing, and contributing causes are recorded, not acted on. One primary cause, one play
> (`R17`).
>
> Evidence labels: `[M]` measured with a named study · `[V]` vendor/industry research ·
> `[P]` practitioner convention, never a benchmark · `[A]` academic · `[PROD]` a company's
> published production process. Field names come from
> `../../cs-context/references/normalized-schema.md`.

**Contents**
- [How to use this file](#how-to-use-this-file)
- [The eleven causes](#the-eleven-causes) — [RC1](#rc1--value-not-realised) · [RC2](#rc2--adoption-failure) ·
  [RC3](#rc3--product-gap) · [RC4](#rc4--reliability-and-trust) · [RC5](#rc5--relationship-loss) ·
  [RC6](#rc6--champion-departure) · [RC7](#rc7--budget-and-economic) · [RC8](#rc8--competitive-displacement) ·
  [RC9](#rc9--ma-and-reorg) · [RC10](#rc10--wrong-fit-sold-badly) · [RC11](#rc11--pricing)
- [The differential matrix](#the-differential-matrix)
- [The diagnostic conversation](#the-diagnostic-conversation)
- [Evidence requirements by cause](#evidence-requirements-by-cause)
- [Locus and origin stage](#locus-and-origin-stage)
- [Recording the diagnosis](#recording-the-diagnosis)
- [Anti-patterns](#anti-patterns)

---

## How to use this file

Each cause has eight parts. You need all eight before the diagnosis is safe to act on.

| Part | Why it exists |
| --- | --- |
| **Definition** | What the cause actually is, in one sentence a customer would recognise |
| **Identifying test** | The positive test. A specific, checkable condition — not a vibe |
| **Confirming evidence** | The fields and records that must be present, named |
| **Disconfirming test** | The innocent explanation. Run it *before* committing the play |
| **Nearest neighbour** | The cause it is most often confused with, and the rule that separates them |
| **Locus · origin** | Who can fix it, and where in the lifecycle it began |
| **Savability** | A planning band `[P]`, never a probability (`R22`) |
| **Misdiagnosis cost** | What it costs to treat this cause as its neighbour — the reason this file exists |

**Savability bands** are ordinal planning conventions, used to rank where to spend hours. They
are not measured rates and must never be presented as the chance of saving this account. Replace
them with your own observed rates by cause once `churn-postmortem` has coded twenty closed plays.

| Band | Means | Plan accordingly |
| --- | --- | --- |
| **High** | The cause is inside our control and there is runway to act | Fund the play fully; expect to win most of these |
| **Moderate** | Inside our influence, but it needs the customer to invest too | Fund it; require a customer obligation before spending |
| **Low** | Mostly outside our control; a restructure is more likely than a save | Time-box hard; go to a restructure early |
| **Structural** | Not savable as sold | Do not spend. Restructure or exit, and take the finding to the owning function |

The taxonomy's spine is GitLab's published risk-reason vocabulary `[PROD]`, which is unusual in
carrying a disambiguation clause inside each definition. RC3, RC9, RC10 and RC11 are added
because their plays differ materially, and collapsing them into "product gap" or "budget" hides
the two findings a CCO most needs: bad qualification, and price/value density.

---

## The eleven causes

### RC1 · Value not realised

| | |
| --- | --- |
| **Definition** | They used the product roughly as intended and the outcome they bought did not arrive. |
| **Identifying test** | Core-action volume reached and sustained the activation threshold (`usage_daily.core_actions`), **and** the customer's own success metric — the one in the success plan or original business case — did not move. |
| **Confirming evidence** | An agreed baseline and target from the success plan; the current value of that metric, measured the same way; ≥2 quarters of sustained usage. If no baseline exists, that absence is itself the finding. |
| **Disconfirming test** | Was value delivered but never *measured*, or measured and never *shown*? An account that got the outcome and cannot see it is not RC1 — it is a reporting failure, and the play is a value review, which is cheap. Also check whether the metric moved for the buying team specifically. |
| **Nearest neighbour** | **RC2.** They did not adopt *because they never saw value* → RC1. They did not adopt for organisational reasons — no internal resource, competing programme, a silo — → RC2 `[PROD]`. |
| **Locus · origin** | jointly-controllable · `value-realisation` (often seeded at `sales-qualification` when the outcome was never agreed) |
| **Savability** | **Moderate** — high if a baseline exists, low if it must be reconstructed after the fact |
| **Misdiagnosis cost** | Treated as RC2 you run an implementation restart on a team that has already implemented. They read it as the vendor not listening, and you lose the meeting you needed for the value conversation. |

**The trap.** Value not realised is the most over-claimed and under-evidenced cause in customer
success, because it sounds like nobody's fault. Before coding RC1, produce the number. If you
cannot produce it, the honest code is `UNKNOWN — requires the success-plan baseline`.

### RC2 · Adoption failure

| | |
| --- | --- |
| **Definition** | The use case never went live, or went live and never reached the population that was supposed to use it. |
| **Identifying test** | `usage_daily.core_actions` never sustained the activation threshold; or `subscription.seats_provisioned` far below `seats_purchased`; or a contracted use case with no production events at all. |
| **Confirming evidence** | Activation event definition from `cs-context` §5; time from `subscription.start_date` to first value event; onboarding milestone status; provisioned vs purchased seats; feature breadth against a **curated core set**, never the full catalogue — most features in any product are rarely used, and breadth measured against the whole catalogue is noise [Pendo · Feature Adoption Report 2019 · 615 subscriptions with >1yr tenure: ~80% of features rarely or never used, ~12% driving ~80% of usage] `[M]`. |
| **Disconfirming test** | A deliberately phased rollout that is on schedule. Check the plan before calling a low number a failure. Also check whether usage moved to an API or embedded surface that does not emit the login event. |
| **Nearest neighbour** | **RC1** (see above), and **RC10** — if the reason they cannot adopt is that the product was never capable of their workflow, it is RC10 or RC3, not RC2. |
| **Locus · origin** | jointly-controllable · `onboarding` |
| **Savability** | **High** with ≥60 days of runway; **Low** inside 30 days — a restart needs time the renewal does not have |
| **Misdiagnosis cost** | Treated as RC1 you spend two weeks building a value story about a product nobody used, and the customer's answer is "we never got it running", which you should have known. |

### RC3 · Product gap

| | |
| --- | --- |
| **Definition** | A specific capability they need that we do not have and cannot configure around. |
| **Identifying test** | A named requirement, evidenced in a ticket, RFP response, transcript or email, for which no configuration, integration or workaround produces an acceptable result — confirmed by someone who could build the workaround if it existed. |
| **Confirming evidence** | `ticket.type = feature_request` with the requirement stated; a solutions-engineering or product opinion on record; the requirement's presence in the original business case or its arrival after it. |
| **Disconfirming test** | Ask whether the requirement is genuinely blocking or merely preferred, and what they do today without it. A "gap" they have lived with for two years is rarely the reason they are leaving; something else changed. |
| **Nearest neighbour** | **RC4** — quality is not capability. A feature that exists and breaks is RC4 and is fixable. **RC8** — a gap named only after a competitor demo is usually RC8 wearing RC3's clothes. |
| **Locus · origin** | vendor-controllable · `sales-qualification` if it was in scope at signature, `value-realisation` if their need changed |
| **Savability** | **Low** without a date we own; **Moderate** with a committed, resourced date inside their decision window |
| **Misdiagnosis cost** | Treated as RC1 you argue value at someone who has a concrete blocking requirement, which reads as evasion. Treated casually it produces the single most damaging sentence in customer success — an implied roadmap date nobody owns (`R19`). |

### RC4 · Reliability and trust

| | |
| --- | --- |
| **Definition** | They used it, and the experience was defective: outages, defects, performance, or commitments we missed. |
| **Identifying test** | Any of — SLA breaches in the last 90 days (`ticket.sla_breached`), a repeat issue with ≥3 occurrences, a P1 aged past 14 days, reopen rate above the account's own baseline, or two or more dates we set and missed. |
| **Confirming evidence** | Ticket IDs with dates and priorities; incident records affecting this account; the commitment ledger showing our misses. Read ticket history **cumulatively per customer**, not ticket by ticket — escalation risk is a property of accumulated history, not of any single ticket [University of Victoria / IBM · arXiv:1901.01344 · 2019] `[A]`. GitLab publishes 16+ tickets per month as a red-tier indicator and 6–15 as a yellow-tier warning `[PROD]`; treat those as one company's operating thresholds, not an industry benchmark. |
| **Disconfirming test** | Normalise ticket volume per 100 seats and against the account's own history. A large account with more tickets is not necessarily a suffering account. Check whether the tickets are questions (adoption) or defects (reliability) — they point at different causes. |
| **Nearest neighbour** | **RC3.** Broken ≠ absent. |
| **Locus · origin** | vendor-controllable · `adoption` or `value-realisation` |
| **Savability** | **Moderate to High** — reliability is the most recoverable cause, because a visible fix with a named owner produces trust faster than any other intervention |
| **Misdiagnosis cost** | Treated as RC5 you send relationship outreach to people who are angry about a specific unfixed thing, and the outreach itself becomes evidence that you were not listening. |

### RC5 · Relationship loss

| | |
| --- | --- |
| **Definition** | Nobody senior on their side is engaged with us any more, and no single departure explains it. |
| **Identifying test** | Multithread depth ≤1 for 90+ days (distinct `interaction.customer_participants` in the window), **or** no executive-level contact in two quarters, **with no `contact.departed_at` event** to explain it. |
| **Confirming evidence** | Interaction counts by contact and seniority over 180 days; reply-latency trend; meeting acceptance rate; QBR/EBR attendance. |
| **Disconfirming test** | A quiet quarter is not disengagement — check their fiscal calendar, a known project freeze, and whether we went quiet first. Count our own outbound before concluding they did. |
| **Nearest neighbour** | **RC6.** A departure event makes it RC6, which is a step change and needs a 48-hour response (`R3`). Absent a departure it is RC5, which is a gradual decline and needs a 30-day re-multithreading plan. |
| **Locus · origin** | jointly-controllable · `renewal-execution` |
| **Savability** | **Moderate** — an account with one engaged contact carries its full ARR at risk until a second relationship exists (`R5`) |
| **Misdiagnosis cost** | Treated as RC1 you build a value deck for an audience that will not attend the meeting. The deck is not the problem; the empty room is. |

### RC6 · Champion departure

| | |
| --- | --- |
| **Definition** | The specific person who owned the value on their side has left, changed role, or gone unresponsive, and no successor has taken it on. |
| **Identifying test** | A named departure: `contact.email_status = hard_bounce`, directory or SSO deactivation, a title change, removal from a shared channel — **plus** that contact having been the sole customer participant on ≥50% of interactions in the last 180 days. |
| **Confirming evidence** | The bounce record with its date; identity-provider or admin-log evidence; contract signatory or named-contact status; interaction share. |
| **Disconfirming test** | A hard bounce is not a departure. Check for a domain migration (do other contacts at the same domain also bounce?), a mailbox quota rejection, an out-of-office in the bounce body, and a forwarding address. Check whether a successor has already appeared in product admin logs under a new address. |
| **Nearest neighbour** | **RC5** (see above). |
| **Locus · origin** | customer-internal trigger, jointly-controllable response · `renewal-execution` |
| **Savability** | **Moderate** if a successor is engaged inside 30 days; **Low** after 60 days of no named successor |
| **Misdiagnosis cost** | Treated as RC5 you run a 30-day plan on a 48-hour problem. The successor forms their opinion of us from whoever reaches them first, and that window closes quickly. |

### RC7 · Budget and economic

| | |
| --- | --- |
| **Definition** | The value is real and they can no longer afford it — a contraction, cost programme, funding event or headcount reduction. **Explicitly not a competitive loss** `[PROD]`. |
| **Identifying test** | An external economic event (layoffs, funding failure, restructuring, a stated cost-reduction programme) **and** no evidence of a vendor comparison, RFP or replacement tool. |
| **Confirming evidence** | Firmographic events with dates and sources; `invoice` days-late trend and payment failures; deprovisioning bursts affecting other tools as well as ours; a stated budget instruction, quoted. |
| **Disconfirming test** | Ask what happens to the workload after we leave. "It moves to <named tool>" is RC8. "It goes back to spreadsheets" is genuinely RC7. This one question resolves the most common misdiagnosis in the taxonomy. |
| **Nearest neighbour** | **RC8** and **RC11.** Budget is the most common face-saving code, because it lets both sides avoid the harder conversation. |
| **Locus · origin** | customer-internal or market · exogenous |
| **Savability** | **Low as sold, Moderate as restructured** — the play is a smaller contract that keeps the relationship and the data, not a discount on the same contract |
| **Misdiagnosis cost** | Accepting RC7 at face value on an RC8 loss means you never compete, you code the loss wrongly, and product never learns what it lost to. Budget-coded churn that is really competitive churn is how a CS organisation stops improving. |

### RC8 · Competitive displacement

| | |
| --- | --- |
| **Definition** | Someone else is winning the seat: an evaluation, an RFP, a bake-off, or a parallel implementation already underway. |
| **Identifying test** | A competitor named by them in a ticket, transcript, email or `opportunity.competitor`; an RFP or vendor review announced; or observed parallel implementation (integration disconnections, data export, a second tool appearing in their stack). |
| **Confirming evidence** | The exact quote with speaker and date; procurement re-engagement; export activity by an admin rather than a scheduled job. |
| **Disconfirming test** | Mentioning a competitor is not an evaluation. Establish stage: awareness, active evaluation, or decided. Ask directly — "if you are looking at other options, I would rather be part of that conversation than outside it." A customer preparing to leave respects being asked. |
| **Nearest neighbour** | **RC3** (a gap named only after a demo) and **RC7** (budget as cover). |
| **Locus · origin** | jointly-controllable · `renewal-execution`, though the vulnerability usually originated at `value-realisation` |
| **Savability** | **Moderate** if the evaluation has not been scored; **Low** once a decision has been socialised internally |
| **Misdiagnosis cost** | Treated as RC11 you discount into a competitive loss, which converts a lost renewal into a lost renewal at a lower price and teaches your own team that discounting does not work. |

### RC9 · M&A and reorg

| | |
| --- | --- |
| **Definition** | A decision taken above the buyer — an acquisition, a merger, a new executive, or a mandated consolidation. |
| **Identifying test** | A corporate event (acquisition, merger, new CIO/CFO/functional exec) **plus** either procurement re-engagement or a stated consolidation/ELA mandate. |
| **Confirming evidence** | The corporate announcement with date and source; the incoming executive's name and start date; SSO or identity migration to an acquirer domain; a stated rationalisation programme. Vendor rationalisation is an active pressure: organisations run 305 SaaS applications on average (median 240), and 61% of leaders report cutting projects because of unplanned SaaS cost increases [Zylo · 2026 SaaS Management Index] `[V]`. |
| **Disconfirming test** | Not every acquisition ends a contract. Check whether the acquirer already owns a competing tool, and whether our buyer survived the reorg with the same remit. |
| **Nearest neighbour** | **RC7.** A consolidation mandate is a corporate decision, not a budget shortfall — the money exists and is being redirected. |
| **Locus · origin** | customer-internal · exogenous |
| **Savability** | **Low** — the play is to sell the incoming decision-maker, on their agenda, and to be honest internally that most of these are lost |
| **Misdiagnosis cost** | Treated as RC5 you invest in a relationship with people who no longer decide. The only relationship that matters is with someone you have not met. |

### RC10 · Wrong-fit, sold badly

| | |
| --- | --- |
| **Definition** | The customer's requirement was never in scope; the account would have reached this point regardless of anything CS did. |
| **Identifying test** | The requirement they are failing on is absent from the signed scope and from the original business case, and was known — or knowable — at signature. |
| **Confirming evidence** | The order form and scope; the original business case or discovery notes; the date the requirement was first raised relative to `subscription.start_date`. |
| **Disconfirming test** | Did their need change after signature? A requirement that emerged in year two is RC3, not RC10, and the finding belongs to product rather than sales. |
| **Nearest neighbour** | **RC1** and **RC3.** The separating question is always: was this in scope when they signed? |
| **Locus · origin** | vendor-controllable, but **not by CS** · `sales-qualification` |
| **Savability** | **Structural** — do not spend. Run a dignified exit and route the finding to sales leadership with the ARR attached |
| **Misdiagnosis cost** | Treating RC10 as RC1 or RC2 is the single most expensive error in this taxonomy: thirty to forty CSM hours on an account that was never savable, while three healthy accounts go unworked. It also suppresses the qualification finding, so the same deal is sold again next quarter. |

### RC11 · Pricing

| | |
| --- | --- |
| **Definition** | The value is acknowledged and the price is wrong for the density of that value: seats, uplift, packaging, or an expiring discount. |
| **Identifying test** | The customer states, in their own words, that the product works and the economics do not — and there is a specific number, ratio or clause they object to. |
| **Confirming evidence** | The quote; `subscription.discount_pct` and `discount_expires`; `uplift_pct`; licence utilisation or consumption pacing; the effective unit price now versus at signature. |
| **Disconfirming test** | Price objections are the default language for every other cause. Before coding RC11, confirm the product works and confirm no competitor and no budget event. If value has not been demonstrated, the objection is RC1 in commercial clothing. |
| **Nearest neighbour** | **RC7.** Cannot afford it (RC7) versus not worth this much (RC11). Different plays: one restructures the contract, the other restructures the packaging. |
| **Locus · origin** | vendor-controllable · `sales-qualification` or `renewal-execution` |
| **Savability** | **High** — structure is the most flexible lever available, and the one that costs least when traded rather than given |
| **Misdiagnosis cost** | Treated as RC1 you argue value at someone who has already conceded it, which wastes the only meeting you have. Treated with a plain discount you fix the number and leave the packaging wrong, so the same conversation returns next renewal with less room. |

---

## The differential matrix

The pairwise question that separates each confusable pair. Run the one that applies before
committing a play.

| Pair | The question that resolves it | If yes | If no |
| --- | --- | --- | --- |
| RC1 / RC2 | Did core-action volume ever sustain the activation threshold? | RC1 | RC2 |
| RC1 / RC3 | Is there a named capability that no configuration satisfies? | RC3 | RC1 |
| RC1 / RC11 | Do they agree the product delivered, and object only to the number? | RC11 | RC1 |
| RC2 / RC10 | Was the failing requirement in the signed scope? | RC2 | RC10 |
| RC3 / RC4 | Does the capability exist and behave badly, or not exist? | Exists → RC4 | Absent → RC3 |
| RC3 / RC8 | Was the gap raised before, or only after, a competitor conversation? | Before → RC3 | After → RC8 |
| RC4 / RC5 | Is there an unresolved defect cluster with our name on it? | RC4 | RC5 |
| RC5 / RC6 | Is there a dated departure event for a specific person? | RC6 | RC5 |
| RC7 / RC8 | What happens to the workload after we leave? | A named tool → RC8 | Nothing / manual → RC7 |
| RC7 / RC9 | Is the money gone, or being redirected by a mandate? | Redirected → RC9 | Gone → RC7 |
| RC7 / RC11 | Would a 20% smaller contract solve it? | RC7 | RC11 |
| RC9 / RC5 | Does our buyer still hold the decision after the reorg? | RC5 | RC9 |
| RC10 / RC3 | Was the requirement knowable at signature? | RC10 | RC3 |

**When two causes both fit**, the tiebreak order follows the evidence standard's contradiction
rule: commercial actions beat relationship state, which beats buying-team usage, which beats
aggregate usage, which beats sentiment. State the rule you applied.

---

## The diagnostic conversation

When coverage is under 40%, or when the differential matrix does not resolve, the play is one
call whose entire purpose is to establish the cause. It is not a check-in and it is not a pitch.

The sequence below is a de-escalation technique from Lauren Costella-Reber, relaying Daren Baird
of Griffin-Hill `[P]`. Its purpose is to move the customer from defending a decision to
describing a problem, which is the only state in which a real cause surfaces.

| # | Move | What it sounds like |
| --- | --- | --- |
| 1 | **Validate without agreeing** | "It makes complete sense that you want to make the best decision for your team." Not "I'd be upset too" — that is agreement with a conclusion you have not tested. |
| 2 | **Ask permission, then open questions** | "Do you mind if I ask a few questions? Can you expand on that? Tell me more about how that affects the team." |
| 3 | **Reflect back** | "I captured A, B and C — did I hear that right?" |
| 4 | **Surface everything else** | "What other problems are you hitting with us?" Repeat until they say there are no more. **This is the highest-yield step**: it converts one complaint into a full inventory at the moment they are most willing to talk. |
| 5 | **Isolate and rank** | Read each issue back; ask which matters most to them. |
| 6 | **Solve the top one, with a date** | Owner, step, date, next meeting booked on the call and confirmed by email. |

Three questions that separate causes faster than anything else, asked plainly:

1. "If we were not here next year, what would your team do instead?" → separates RC7 from RC8.
2. "When you signed, what did you expect to be different by now?" → separates RC1 from RC10.
3. "Is this a thing we broke, or a thing we never had?" → separates RC4 from RC3.

---

## Evidence requirements by cause

The minimum a diagnosis needs before it can carry a play. Anything missing is written
`UNKNOWN — requires <source>` and caps confidence (`R23`).

| Cause | Minimum evidence | Family it lives in | If missing |
| --- | --- | --- | --- |
| RC1 | Success-plan baseline + current value of the same metric | Sentiment & VoC, Product usage | Confidence Low; run a value review before choosing a play |
| RC2 | Activation threshold + core-action series + provisioned vs purchased seats | Product usage & adoption | Cannot distinguish from RC1; run the diagnostic conversation |
| RC3 | The requirement quoted, with a solutions or product opinion on record | Support & reliability | Do not code RC3 from a sales anecdote |
| RC4 | Ticket IDs, priorities, SLA flags, our missed dates | Support & reliability | The account cannot be safely told "we know what went wrong" |
| RC5 | Interaction counts by contact and seniority, 180 days | Relationship & engagement | Multithread depth is unknown; treat single-threading as the floor (`R5`) |
| RC6 | Departure event with date and source | Relationship & engagement | Do not assert departure from a bounce alone |
| RC7 | Dated external economic event + absence of a vendor comparison | Firmographic & external | Cannot separate from RC8; ask the workload question |
| RC8 | Competitor named by them, with the quote and date | Commercial & contract | Coding a competitive loss as budget destroys the product feedback loop |
| RC9 | Corporate event + incoming exec named | Firmographic & external | The play has no target; the meeting cannot be requested |
| RC10 | Signed scope + original business case | Commercial & contract | You will spend a save budget on an unsavable account |
| RC11 | The objected-to number, and the effective unit price then and now | Billing & payment, Commercial | Any concession is unanchored |

---

## Locus and origin stage

Two axes recorded on every diagnosis. They decide who can act and who owns the systemic fix.

| Locus | Meaning | What it permits |
| --- | --- | --- |
| `vendor-controllable` | We caused it and we can fix it | A full play, and a systemic fix owned outside CS |
| `jointly-controllable` | Needs both sides to invest | A play **gated on a customer obligation** |
| `customer-internal` | Their organisation changed | A restructure or an exit; no amount of CS effort changes it |
| `market` | Exogenous | Track the rate; if exogenous losses exceed roughly a quarter of the total, the segment strategy is the problem, not the saves `[P]` |

| Origin stage | Owns the systemic fix | Typical causes |
| --- | --- | --- |
| `sales-qualification` | Sales leadership | RC10, some RC3, some RC11 |
| `onboarding` | Services / onboarding lead | RC2 |
| `adoption` | CS | RC2, RC4 |
| `value-realisation` | CS + Product | RC1, RC3 |
| `renewal-execution` | CS + AM | RC5, RC6, RC8, RC11 |

**Where a loss originated is almost never where it surfaced.** A renewal lost to a competitor in
month 34 that began as an onboarding failure in month 2 is coded RC8 primary with origin
`onboarding` — and the fix belongs to onboarding.

---

## Recording the diagnosis

Write these fields on the account so `churn-postmortem` can aggregate them. Free text cannot be
aggregated, and a cause that cannot be aggregated cannot be fixed.

| Field | Values |
| --- | --- |
| `primary_risk_reason` | RC1–RC11, single value |
| `contributing_reasons` | RC1–RC11, multi |
| `risk_impact` | `full_churn` · `tier_downgrade` · `seat_reduction` · `sentiment_only` · `competitor` |
| `locus` | `vendor-controllable` · `jointly-controllable` · `customer-internal` · `market` |
| `origin_stage` | `sales-qualification` · `onboarding` · `adoption` · `value-realisation` · `renewal-execution` |
| `diagnosis_confidence` | High / Medium / Low / Insufficient, with the coverage fraction |
| `diagnosis_evidence` | The provenance-tagged records the identifying test used |
| `ruled_out` | The causes tested and the evidence that rejected each |
| `decision_date` | When the **customer** decided, not when service ended (`R24`) |

---

## Anti-patterns

| Anti-pattern | Correction |
| --- | --- |
| Coding a cause from the customer's stated reason alone | The stated reason is evidence, not a diagnosis. Run the identifying test |
| "Budget" on an account with a competitor in the transcript | Ask the workload question; code RC8 and route the loss to product and pricing |
| Two or three primary causes | One primary, the rest contributing. If you cannot choose, the diagnosis is not finished |
| Skipping the disconfirming test because the signal is strong | A false escalation is expensive in internal credibility, and you only get a few |
| Coding RC1 with no baseline | `UNKNOWN — requires the success-plan baseline`. An unmeasured outcome is not a failed outcome |
| Calling a hard bounce a departure | Domain migration, quota rejection, out-of-office, forwarding address — check all four first |
| Free-text reasons | Enums only. Free text cannot be aggregated and therefore never gets fixed |
| Coding RC10 to avoid a hard conversation with CS leadership | RC10 is a sales-qualification finding with an ARR figure attached. It is meant to be uncomfortable, and it is meant to be rare |
| Diagnosing from aggregate usage | Segment by the buying team. An account can be growing overall while the team that signed has stopped |
| Recording the cause and not the origin stage | Cause tells you the play; origin tells you the systemic fix. Both, every time |
