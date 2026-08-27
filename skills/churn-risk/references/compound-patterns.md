# Compound Risk Patterns

> Single signals have poor precision. Named compounds are where the predictive power lives —
> and an additive weighted scorecard systematically **under-ranks** them, because each
> component sits below its own firing threshold while the combination is decisive.
>
> Signal IDs (`U4`, `R1`, `C1` …) refer to `../../cs-context/references/signal-library.md`.
> Joint probabilities are prioritisation conventions `[P]` unless labelled `[M]` or `[V]`;
> never present them as measured churn probabilities.

**Contents**

P0 — escalate regardless of the weighted score:
[Decapitation](#decapitation) · [Exit preparation](#exit-preparation) · [Quiet quit](#quiet-quit) ·
[Buyer disconnect](#buyer-disconnect) · [Regime change](#regime-change) ·
[Technical decoupling](#technical-decoupling) · [Failed launch](#failed-launch) ·
[Consolidation target](#consolidation-target)

P1 — work in priority order:
[Shelfware](#shelfware) · [Budget squeeze](#budget-squeeze) · [Value vacuum](#value-vacuum) ·
[Death by a thousand tickets](#death-by-a-thousand-tickets) · [Contraction spiral](#contraction-spiral) ·
[Frictionless renewal](#frictionless-renewal)

Craft codes (`../../cs-context/references/practitioner-craft.md`) enforced here:
`[C21]` Quiet quit · `[C23]` Failed launch's firing point · `[C24]` Frictionless renewal.

[How to use this file](#how-to-use-this-file) · [Pattern interactions](#pattern-interactions)

---

## How to use this file

Each pattern has five parts, and you need all five:

| Part | Why |
| --- | --- |
| **Composition** | The exact signals that must be present. Two of three is a partial match — report it as such rather than forcing it. |
| **Confirming test** | The extra check that raises a partial match to a confirmed one. |
| **Disconfirming test** | The innocent explanation. Run it *before* escalating. Skipping this is how CS teams train their own organisation to ignore them. |
| **The play** | What to actually do, with the owner and the window. |
| **Working / failing signals** | What tells you within two weeks whether the play is landing. |

**Partial matches are reported, not suppressed.** "Two of the three Decapitation components
present; exec sponsor status UNKNOWN — requires a CRM contact-role audit" is a useful finding.
Silently discarding it is not.

---

## Decapitation

**P0 · lead time 90–270 days · the highest-strength relationship compound in enterprise**

| | |
| --- | --- |
| **Composition** | R1 champion departure + R4 single-threaded + R2 no exec sponsor |
| **Why it compounds** | The only person who understood the value is gone, and the structure that could transfer that understanding does not exist. Vendor data puts standalone champion departure at roughly 51% 12-month churn `[V]`; single-threading removes the recovery path entirely. |
| **Confirming test** | Was the departed contact the sole customer participant on ≥50% of interactions in the last 180 days? Were they the signatory or the named contact on the contract? |
| **Disconfirming test** | A hard bounce is not a departure. Check for a domain migration (do other contacts at the same domain also bounce?), a mailbox quota rejection, an out-of-office in the bounce body, and a forwarding address. Check LinkedIn and the customer's website before asserting departure. Also check whether a successor has already appeared in product or ticket data under a new email. |
| **The play** | 48-hour window. (1) Exec-to-exec outreach from our VP/CCO to their most senior known contact — not from the CSM, and not asking "who replaced Jamie". (2) Identify the successor from product admin logs, ticket ownership and org data. (3) Re-establish the business case from scratch with the successor: assume zero inherited context and zero inherited goodwill. (4) Reset the success plan with them as the owner. (5) Open a risk record that persists to the renewal regardless of how the first meeting goes. |
| **Working** | A successor is named and attends a meeting within 21 days; they can state the business objective in their own words; a second contact is engaged. |
| **Failing** | No named successor after 30 days; the successor delegates to a junior; the first meeting is cancelled twice. |

**The most common error:** treating this as a relationship-refresh task for the CSM. A champion
departure at an enterprise account is a commercial event and belongs on the leadership's list
the same week it is detected.

---

## Exit preparation

**P0 · lead time 30–120 days · effectively confirmatory**

| | |
| --- | --- |
| **Composition** | T6 bulk data export / full API extraction + C1 auto-renew off + R11/R12 procurement or termination-terms enquiry |
| **Why it compounds** | Three independent systems agreeing on intent. Any one has an innocent explanation; all three simultaneously do not. |
| **Confirming test** | Was the export performed by an admin rather than a scheduled job? Is it a first-of-its-kind volume for this account? Did the auto-renew change originate from the customer rather than from our own re-papering? |
| **Disconfirming test** | Recurring export schedules, audit season, a compliance or legal hold, a data-warehouse integration being built, and — critically — **auto-renew switched off by our own team for re-papering a multi-year or restructured deal**. Verify the auto-renew change with the account owner within 24 hours. Do not skip this because the signal is strong; a false Exit-preparation escalation is expensive in internal credibility. |
| **The play** | Treat it as a competitive re-bid, not a save. Same week: escalate to commercial leadership and the exec sponsor. Ask directly and without defensiveness — "we noticed the auto-renew flag changed; are you running a review?" A customer preparing to leave respects being asked and loses respect for a vendor that pretends not to have noticed. Prepare the value case and the alternative structures before the meeting, not during it. |
| **Working** | They confirm a review and agree to include us in it with a defined process and timeline. |
| **Failing** | Evasion, delegation to procurement only, or a refusal to schedule. At that point the play shifts from save to `save-play` §stop-loss and a managed exit that preserves win-back. |

---

## Quiet quit

**P0 · lead time 60–150 days · the most common quiet churn · enforces `[C21]`**

| | |
| --- | --- |
| **Composition** | P2 ticket spike then silence + U1/U7 usage decay + Z1 no bilateral interaction |
| **Why it compounds** | The customer tried, hit friction, stopped asking, and then stopped using. This is disengagement, not dissatisfaction — which is precisely why no complaint ever arrives and why satisfaction-based health scores read green throughout. Rising complaint is engagement; the collapse afterwards is the signal `[C21]`. |
| **Scored, not remembered** | The support family is U-shaped: zero tickets in 90 days on an account above 20 seats scores **risk 40, never 0** (`scoring-model.md` §2.4), and a spike-then-collapse scores 85. The mechanism is the sub-score, not the CSM noticing that it went quiet. |
| **Confirming test** | Cluster the tickets from the spike period. Do they share a root cause? Was that root cause ever resolved, or did the tickets simply stop? Ticket volume falling to zero within 30 days of an unresolved cluster is the tell. |
| **Disconfirming test** | The issue was genuinely fixed (check resolution notes and whether usage recovered), the team went on a seasonal break, or a heavy-usage project ended on schedule. Also check whether a single power user was generating all the tickets and all the usage — one person's holiday is not an account signal. |
| **The play** | Root-cause the original ticket cluster before making contact — arriving without having read their tickets confirms their conclusion that nobody was listening. Then re-onboard rather than re-sell: a working session, not a check-in. Bring the fix or the workaround, not a question. |
| **Working** | Usage recovers to ≥70% of the pre-decay baseline within 45 days; a new ticket arrives (paradoxically a good sign — they are engaging again). |
| **Failing** | Meeting declined or repeatedly rescheduled; usage flat after the session. |

---

## Buyer disconnect

**P0 · lead time 90–200 days · the classic false-green**

| | |
| --- | --- |
| **Composition** | Aggregate account usage flat or growing **while** usage by the department that holds the budget falls ≥50% |
| **Why it compounds** | Every aggregate-usage health score reads this account as healthy. The org that signed the contract and defends the line item has stopped using the product; the growth is coming from a team with no budget authority. At renewal, the budget holder is asked to justify a spend they no longer experience. |
| **Confirming test** | Segment `usage_daily` by the department or cost centre named on the contract or in the original business case. Compare that segment's trend against the account aggregate. Then check whether the economic buyer or champion appears in `interaction` in the last 90 days. |
| **Disconfirming test** | A deliberate, planned migration of the use case to another team (check for a stated rollout plan or a success-plan milestone). A reorg that moved the same people under a different department code — check headcount continuity, not just the label. |
| **The play** | Re-engage the budget-holding team specifically, with a value story built on *their* original objective, not the growing team's usage. In parallel, convert the growing team into a second champion base so the renewal has two constituencies. Bring the buyer a number that describes their own team's outcome, and be honest if that number is bad. |
| **Working** | The buyer's team returns to ≥50% of baseline, or the budget formally moves to the growing team with that team's leader as the new economic buyer. |
| **Failing** | The buyer's team stays at zero and no budget transfer is agreed. That is a renewal with no internal advocate — escalate to `save-play`. |

---

## Regime change

**P0 · lead time 90–365 days**

| | |
| --- | --- |
| **Composition** | F2 new CIO/CFO/functional exec + R11 procurement re-engagement + R13 competitor named |
| **Why it compounds** | A new executive runs a vendor consolidation review as a matter of course. Vendor data suggests roughly 65% of accounts experiencing an executive change do not renew `[V]`. Incumbency is worth less than usual because the new exec has no ownership of the original decision. |
| **Confirming test** | Did the exec change occur within the last two quarters? Has the review been mentioned, or has procurement asked for a contract summary, spend history, or usage report? |
| **Disconfirming test** | A routine annual procurement audit that touches every vendor, an insurance or compliance refresh, or a promotion of an existing internal ally (which is the opposite signal). |
| **The play** | Get in front of the audit rather than responding to it. Within 30 days: a briefing for the new exec built on business outcomes and quantified value, not on features or history. Explicitly acknowledge that they did not make this decision and offer to re-justify it. Bring the ROI evidence pack to the first meeting; a second meeting to "gather data" wastes the only window you have. |
| **Working** | A meeting with the new exec is held; they name an objective; we are included in the review with a defined process. |
| **Failing** | Contact restricted to procurement; no exec meeting after 60 days. |

---

## Technical decoupling

**P0 · lead time 45–120 days · high precision, low volume**

| | |
| --- | --- |
| **Composition** | T2 integration disconnected >30 days + T1 API call decline + T5 SSO removed or changed |
| **Why it compounds** | The product is being unwired from the customer's stack. This is usually the *implementation* of a decision already made, not a precursor to one. |
| **Confirming test** | Was the disconnect initiated by them, and did they not ask us to fix it? An integration that breaks and generates a support ticket is a support problem. One that breaks silently and stays broken is a decision. |
| **Disconfirming test** | A credential rotation, a security policy change, an IdP migration for reasons unrelated to us, an infrastructure move, or a planned upgrade window. Ask before escalating — the answer takes one email. |
| **The play** | Immediate technical escalation with a named engineer, not a CSM check-in. Offer to fix it at our cost and on our time. Pair with `fde-account-plan` for the integration health review. The diagnostic question is simple: if they wanted it working, why did they not tell us it was broken? |
| **Working** | They accept help and the integration is restored within 14 days; API volume recovers. |
| **Failing** | The offer of help is declined or deferred. Treat a declined free fix as confirmatory and escalate commercially. |

---

## Failed launch

**P0 · lead time 180–365 days · predicts the first renewal · enforces `[C23]`**

**Firing point: day 60 of the first term, not T-90.** The renewal is decided in months two to
four, while the implementation is still recoverable. This pattern is evaluated by the onboarding
gate in `../SKILL.md` Step 1 — which runs *before* any renewal-window scope filter — so a first-term
account whose renewal is 300 days away still enters the assessment. Waiting for the renewal
window to open means opening the risk record after the decision has been taken.

| | |
| --- | --- |
| **Composition** | U9 TTFV overrun >2× + U10 milestones slipped + U11 services overrun + Z4 account gone dark |
| **Why it compounds** | First-year churn is disproportionately an onboarding failure rather than a product failure `[P]`. Time-to-value is the variable the whole first year turns on: an account that never reached the activation event has no evidence to defend the line item with, and no habit to fall back on when the champion is busy. |
| **Confirming test** | Has the activation event ever fired? Not go-live — the activation event. Who owns each blocked task: us or them? |
| **Disconfirming test** | A complex, engaged deployment with high services burn *and* the activation event achieved is investment, not risk. Genuine customer-side delay (a merger, a hiring freeze, a competing internal project) changes accountability but does **not** reduce churn risk — record it honestly rather than using it as an excuse. |
| **The play** | Executive-sponsored recovery plan with a re-baselined go-live date and a written mutual commitment. Consider a contract restart or an extension at no charge rather than approaching the renewal on a failed implementation. Pair with `onboarding-plan` for the re-plan. |
| **Refusal `[C23]`** | While the activation event has never fired, **no renewal plan is written and the account is not handed to `renewal-prep`**. A T-90 plan on a failed implementation is negotiating from a position already lost — the customer knows what they did not get, and every commercial move from there is a concession. The artifact prints `Renewal plan status: withheld — activation never fired` and names the milestone that unlocks it. |
| **Working** | The activation event fires; the re-baselined milestone is met; the customer's project owner re-engages. |
| **Failing** | A second re-baseline; the customer's project owner is reassigned; no activation by day 120. |

---

## Consolidation target

**P0 · lead time 90–540 days**

| | |
| --- | --- |
| **Composition** | F1 customer acquired or merged + R13 competitor named + T5 SSO moved to the acquirer's IdP |
| **Why it compounds** | Post-acquisition, the acquirer's existing stack wins by default. Nobody has to decide against you; they simply have to not decide for you. |
| **Confirming test** | Does the acquirer use a competing product? Has the SSO domain or IdP changed to the acquirer's? Have new users appeared from the acquirer's email domain? |
| **Disconfirming test** | An acquisition where our product is the surviving standard, or where the acquired entity is being run independently. Check whether the acquirer's usage is *growing* on our platform — that inverts the pattern into an expansion opportunity. |
| **The play** | Map the acquirer's buying centre within 30 days and sell to the acquirer, not the acquired. The acquired champion's influence is at its lowest point immediately post-close; do not rely on it. Build a case around consolidation *onto* us, with migration support offered. This is the one P0 pattern where the upside case is as large as the downside. |
| **Working** | A meeting with an acquirer-side stakeholder; acquirer-domain users appearing in product. |
| **Failing** | No acquirer contact after 60 days; acquired-side usage declining while no acquirer-side usage appears. |

---

## Shelfware

**P1 · lead time 180–365 days · the most expensive pattern to ignore**

| | |
| --- | --- |
| **Composition** | U4 seat utilisation <0.5 + U6 narrow adoption breadth + V3 a contracted use case never went live |
| **Why it compounds** | Money is being spent on nothing, and this survives only while the buyer is not looking. A Regime change (F2) or a Budget squeeze (F3/F4) makes them look. |
| **Confirming test** | Compare contracted seats against distinct 30-day active users, and compare contracted use cases in the original business case against use cases actually live. Is the account past 180 days from go-live (so ramp is not the explanation)? |
| **Disconfirming test** | Accounts under 180 days from go-live are ramping, not dying — score them on `failed launch` criteria instead. Floating vs named licensing, shared service accounts, and deliberately over-bought seats for a phased rollout all inflate the apparent gap. Check the rollout plan before calling it shelfware. |
| **The play** | Right-size and redeploy — trade a seat reduction for a use-case expansion and a longer term. A voluntary, structured downsell that lands a new use case is a far better outcome than defending a number that will be cut anyway and losing the account's trust in the process. Never close a downsell without opening a risk record for the next cycle (see Contraction spiral). |
| **Working** | The second use case goes live; utilisation on the reduced seat count exceeds 0.7. |
| **Failing** | The customer takes the seat reduction and declines the use-case work. |

---

## Budget squeeze

**P1 · lead time 60–270 days · exogenous**

| | |
| --- | --- |
| **Composition** | F3 layoffs + F4 financial distress + C8 DSO deterioration + U14 deprovisioning burst |
| **Why it compounds** | The value is real; the affordability is not. Adoption plays do not work on this pattern, and running one signals that you are not paying attention to their situation. |
| **Confirming test** | Is there corroborating external evidence (news, filings, headcount data, a down round)? Are invoices being paid later than the account's own historical pattern? |
| **Disconfirming test** | A single late invoice is an AP process issue, not distress. Deprovisioning that matches a planned consolidation onto fewer, better-utilised seats is healthy. Check whether the layoffs touched the department that uses us. |
| **The play** | Optimise for GRR-preserving downsell over logo loss. Term restructure, extended payment terms, a tier down with a documented path back up, or a temporary pause with data retained. Lead with "how do we make this survivable for you" rather than with a discount — a discount offered before understanding the constraint is usually the wrong size and permanently reprices the account. |
| **Working** | A restructured agreement is signed; the logo is retained; a path back up is documented with a review date. |
| **Failing** | No engagement on restructure options; invoices go unpaid past 60 days. |

---

## Value vacuum

**P1 · lead time 180–365 days**

| | |
| --- | --- |
| **Composition** | V2 no ROI evidence captured + R6 no QBR in two quarters + R2 exec sponsor disengaged |
| **Why it compounds** | There is nothing to defend the line item with when the budget conversation happens. Usage may be fine; the account is still at risk, because nobody on their side can articulate what it bought. |
| **Confirming test** | Can you, right now, state the customer's business objective and the measured movement against it, with a source? If not, neither can they. |
| **Disconfirming test** | A high-usage, low-touch account in a segment that legitimately does not receive QBRs is not this pattern — it is a coverage-model question. Check the segment's designed cadence before firing. |
| **The play** | Force a value review before the budget cycle, not after. Establish or reconstruct a baseline (see `success-plan` §baseline capture), quantify what has changed, and get the customer to state the number themselves — a number they say is worth ten that you say. Pair with `qbr-builder`. |
| **Working** | A quantified value statement exists that the champion has agreed to and can repeat; an exec meeting is held. |
| **Failing** | No baseline can be reconstructed and the customer declines to help build one. |

---

## Death by a thousand tickets

**P1 · lead time 60–180 days**

| | |
| --- | --- |
| **Composition** | P3 repeat issue ≥3 occurrences + P5 P1 ageing + S2 CSAT decline + P9 a blocking feature request rejected |
| **Why it compounds** | Accumulated unresolved friction. Peer-reviewed escalation research shows this must be measured cumulatively per customer rather than per ticket `[A]` — no single ticket looks bad enough to escalate, and the sum is fatal. |
| **Confirming test** | Aggregate ticket history per account over 180 days: repeat issues, total time-to-resolution, reopen count, and whether the same person is filing them. Reopens are worth more than new tickets. |
| **Disconfirming test** | High ticket volume with high resolution rates and stable CSAT is engagement, not risk. A single frustrated admin is not an account signal — check whether the friction is reaching decision-makers. |
| **The play** | A named engineering owner, committed dates, and weekly closure tracking visible to their exec. The apology matters less than the mechanism. Do not offer a credit before offering a fix; a credit without a fix reads as buying silence. |
| **Working** | Repeat issue count falls; CSAT recovers; the customer stops copying their exec on tickets. |
| **Failing** | Dates slip a second time. At that point escalate to `save-play` — the risk is now trust, not tickets. |

---

## Contraction spiral

**P1 · lead time ~365 days**

| | |
| --- | --- |
| **Composition** | C3 seat reduction at the last renewal + U4 utilisation falling further + C5 term shortened |
| **Why it compounds** | Each cycle removes another block of ARR and another block of internal advocacy. Downsell at one renewal is among the strongest available predictors of churn at the next `[P]`. |
| **Confirming test** | Compare the last three renewal outcomes. Is ARR monotonically declining? Did the term shorten (multi-year → annual → monthly)? |
| **Disconfirming test** | A one-time right-sizing after an over-sold initial contract, followed by stable or growing utilisation, is a correction rather than a spiral. Look at utilisation *after* the reduction — if it went up, the account is healthier than before. |
| **The play** | Break the cycle deliberately rather than accepting a smaller renewal again. Re-run discovery as if this were a new account: what is the objective now, who owns it, what would justify growth. If no growth case exists, decide explicitly whether this account belongs in a lower-cost coverage tier — see `coverage-and-capacity`. |
| **Working** | Utilisation rises on the reduced base; a new use case or team is identified. |
| **Failing** | A third consecutive reduction. Reclassify the account and manage it accordingly rather than spending named-CSM hours on a shrinking base. |

---

## Frictionless renewal

**P1 · lead time 90–365 days · enforces `[C24]` · the pattern that looks like a win**

| | |
| --- | --- |
| **Composition** | Renewal agreed or closing with **zero negotiation events** — no counter, no redline, no procurement involvement, no discount fought for — **plus** relationship-family risk ≥50 or engaged contacts below the segment target (R4) **plus** no customer-stated value (V2) |
| **Why it compounds** | The customer who negotiates hardest is engaged. Negotiation costs the buyer political capital, and they spend it on things they intend to keep using. A renewal nobody contested, from an org where nobody accepts a meeting and nobody can state what the product did, is not agreement — it is a line item renewing on autopilot inside a budget nobody has examined this year. It survives exactly until someone examines it: a new CFO, a cost review, a reorg. This is why it is scored as a **band floor rather than an escalation**: the risk is to the *next* cycle, not this one. |
| **Confirming test** | Count the negotiation events on the last close: counters, redline rounds, procurement contacts, discount requests, term arguments. Zero is the trigger. Then check whether anyone on their side can state the objective in their own words, and whether the economic buyer attended anything in the last 180 days. |
| **Disconfirming test** | A genuinely simple commercial relationship with high engagement — a small ACV, a standard order form, an enthusiastic and active user base — is not this pattern. Neither is a multi-year agreement mid-term, where there is nothing to negotiate. Nor is a self-serve motion, where there is no negotiation to have friction in: record `not-applicable — self-serve`. The test is engagement, never the ease of the paperwork. |
| **The play** | [Engagement proof](intervention-plays.md) before the next cycle. Do not celebrate the close; open a risk record for the next renewal on the day this one signs. Get one meeting with the economic buyer inside 60 days whose only purpose is to have them state the objective and the number. If that meeting cannot be booked, the renewal that just closed was a default, and the following one will not be. **No expansion ask runs on this account** until engagement is re-established (`R8`). |
| **Working** | The economic buyer takes a meeting and states an objective in their own words; a second contact engages; a baseline is agreed for the next term. |
| **Failing** | No buyer meeting inside 60 days; the account renews a second time with nobody able to say what it is for. Reclassify and treat the next renewal as At Risk from T-180. |

**The most common error:** reporting this account as a clean win in the retention number and
moving on. It is the inverse of the difficult renewal everyone worries about — the difficult one
has an owner on the customer's side, and this one does not.

---

## Pattern interactions

Patterns are not mutually exclusive, and the combinations matter.

| Combination | Reading |
| --- | --- |
| Decapitation + Regime change | The champion left *because* of the regime change. Treat as one event; the successor is likely aligned with the new exec's agenda, not the old one. |
| Exit preparation + Consolidation target | The acquirer's decision has already been made and is being implemented. Save probability is low; pivot to a graceful exit that preserves the acquirer relationship for a future sale. |
| Shelfware + Budget squeeze | The most savable combination in the list, and the one most often lost by defending the original number. Right-size early and voluntarily. |
| Quiet quit + Death by a thousand tickets | Sequential, not parallel — the tickets came first. Fix the root cause before any relationship play; outreach without a fix confirms their conclusion. |
| Failed launch + Decapitation | Near-terminal for a first renewal. Escalate to exec sponsorship immediately and consider a restart rather than a renewal. |
| Buyer disconnect + Value vacuum | Nobody with budget authority experiences the product and nobody can quantify it. Highest-priority `value vacuum` variant. |
| Frictionless renewal + Value vacuum | The account renewed and nobody on their side can say why. Highest-conviction next-cycle loss in the list; open the risk record at signature, not at T-180. |
| Frictionless renewal + Shelfware | The uncontested renewal is why nobody noticed the unused seats. Right-size voluntarily this term rather than defending the number at the next one. |
| Failed launch + Frictionless renewal | A first renewal that closed without argument on an implementation that never activated. The customer has already decided; they simply have not paid the cost of the conversation yet. Treat as P0. |
| Three or more P0 patterns | Stop scoring and open a `save-play` war room the same day. The score is no longer the useful artifact. |
