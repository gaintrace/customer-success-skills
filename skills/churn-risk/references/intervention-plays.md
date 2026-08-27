# Intervention Plays

> The play follows the **compound pattern**, not the risk score. Two accounts at 72/100 with
> different patterns need opposite actions — one needs an engineer, the other needs a CFO
> conversation, and running the wrong one costs you the account faster than doing nothing.
>
> Every play below specifies: the trigger, the objective, the sequence with owners and
> windows, what we can and cannot commit, the working/failing signals, and the exit criteria.
> A play without exit criteria runs forever and consumes a CSM's quarter.

**Contents**
1. [Play selection](#1-play-selection)
2. [Capacity: how many plays can actually run](#2-capacity-how-many-plays-can-actually-run)
3. [The plays](#3-the-plays)
4. [Commitment discipline](#4-commitment-discipline)
5. [Measuring whether plays work](#5-measuring-whether-plays-work)

---

## 1. Play selection

| Pattern matched | Play | Owner | Window |
| --- | --- | --- | --- |
| Decapitation | [Champion recovery](#champion-recovery) | VP CS + CSM | 48 hours to first outreach |
| Exit preparation | [Competitive re-bid](#competitive-re-bid) | VP CS + AE | Same week |
| Quiet quit | [Re-onboard](#re-onboard) | CSM + Support lead | 7 days |
| Buyer disconnect | [Buyer re-engagement](#buyer-re-engagement) | CSM | 14 days |
| Regime change | [Exec re-justification](#exec-re-justification) | VP CS / CCO | 30 days |
| Technical decoupling | [Technical rescue](#technical-rescue) | FDE / Solutions | 72 hours |
| Failed launch | [Implementation restart](#implementation-restart) | VP CS + Services | 14 days |
| Consolidation target | [Sell the acquirer](#sell-the-acquirer) | AE + VP CS | 30 days |
| Shelfware | [Right-size and redeploy](#right-size-and-redeploy) | CSM + AM | Before T-90 |
| Budget squeeze | [Structure for survival](#structure-for-survival) | AM + Finance | Before T-60 |
| Value vacuum | [Forced value review](#forced-value-review) | CSM | Before the budget cycle |
| Death by a thousand tickets | [Named-owner remediation](#named-owner-remediation) | Support lead + Eng | 7 days |
| Contraction spiral | [Break the cycle](#break-the-cycle) | AM + VP CS | Before T-120 |
| Frictionless renewal `[C24]` | [Engagement proof](#engagement-proof) | CSM + AM | 60 days from signature |
| Two consecutive economic-buyer reschedules `[C22]` (floor 60, fires with no usage decline) | [Calendar escalation](#calendar-escalation) | VP CS | 5 working days |
| First term, no activation by day 60 `[C23]` | [Implementation restart](#implementation-restart) — **and the renewal plan is withheld** | VP CS + Services | 14 days |
| No pattern, band ≥ At Risk | [Diagnostic conversation](#diagnostic-conversation) | CSM | 14 days |
| Two or more P0 patterns | Stop scoring — open a `save-play` war room today | VP CS | Same day |

**Rule:** run one primary play. Stacking three plays on one account produces three
half-executed interventions and a customer who feels managed rather than helped.

---

## 2. Capacity: how many plays can actually run

A play is not free. Before assigning them, check the arithmetic — this is where risk lists
become theatre.

| Play class | Realistic CSM hours | Notes |
| --- | --- | --- |
| Diagnostic conversation | 2–3 | Prep, call, follow-up |
| Re-onboard | 6–10 | Ticket root-cause analysis is the expensive part |
| Buyer re-engagement | 4–6 | |
| Forced value review | 8–12 | Baseline reconstruction dominates |
| Champion recovery | 10–15 | Spread over 30 days, plus exec time |
| Right-size and redeploy | 8–12 | Plus AM time on the commercial restructure |
| Implementation restart | 20–40 | Effectively a second onboarding |
| Competitive re-bid | 25–40 | Plus AE and exec time |
| Technical rescue | 5–10 CSM + 10–20 engineering | Engineering time is the constraint, not CSM time |
| Engagement proof | 3–5 | One meeting, but the hard part is getting the economic buyer into it |
| Calendar escalation | 1–2 CSM + 1 VP | Cheapest play in the list, and the earliest |

A CSM with a 40-account book and roughly 25 usable hours a week can sustain **two to three
active plays** alongside cadence work. If the risk list has nine accounts, six of them are not
getting a play — decide which six deliberately and write it down. See
`book-of-business-triage`. An undeclared decision to skip an account is how accounts get
skipped for a quarter.

---

## 3. The plays

### Champion recovery

**Trigger:** Decapitation. **Objective:** a named successor who can state the business
objective in their own words, plus a second engaged contact, within 30 days.

| # | Action | Owner | By | Expected effect | Success measure |
| --- | --- | --- | --- | --- | --- |
| 1 | Confirm departure — check bounce body, domain migration, LinkedIn, product admin logs | CSM | +24h | Avoids escalating on a mailbox quota error | Departure confirmed or disconfirmed with evidence |
| 2 | Identify the successor from admin logs, ticket ownership, org data | CSM | +48h | A person to address, not a title | Named individual |
| 3 | Exec-to-exec outreach to the most senior known contact — from our VP/CCO, not the CSM | VP CS | +48h | Signals the account matters; opens a door the CSM cannot | Reply within 7 days |
| 4 | Discovery with the successor, assuming zero inherited context | CSM | +14d | Rebuilds the business case with its new owner | Successor states an objective |
| 5 | Reset the success plan with the successor as owner | CSM | +21d | Gives them something to defend at renewal | Signed or agreed plan |
| 6 | Engage a second contact so the account is not single-threaded again | CSM | +30d | Removes the recurrence | ≥2 engaged contacts |
| 7 | Open a risk record that persists to renewal regardless of how step 4 goes | CSM | +48h | Prevents a good first meeting from closing the risk prematurely | Record open at T-90 review |

**Do not** ask "who has replaced Jamie?" as the opening move. It tells the customer we were
dependent on one person and had no other relationship — which is true, and is exactly the
impression to avoid reinforcing.

**Working:** successor attends a meeting within 21 days and can state the objective.
**Failing:** no successor after 30 days, delegation to a junior, or two cancelled meetings.
**Exit:** ≥2 engaged contacts including one with budget influence, and a reset success plan.

---

### Competitive re-bid

**Trigger:** Exit preparation. **Objective:** be included in the review with a defined process
and timeline — or learn quickly that we are not, and pivot.

1. **Verify the auto-renew change with the account owner within 24 hours** — it may be our own
   re-papering. Skipping this is how teams burn credibility on a false alarm. — CSM, +24h
2. Escalate to commercial leadership and the exec sponsor the same week. — VP CS, +5d
3. Ask directly and without defensiveness: *"We noticed the auto-renew flag changed on 2 August
   — are you running a review? If so, we'd like to be part of it properly."* — VP CS, +5d
4. Prepare the value case and two alternative commercial structures **before** the meeting. — AM, +7d
5. Establish the decision process: who decides, on what criteria, by when. — AE, +14d
6. Run it as a competitive deal — see `renewal-negotiation`. — AM

**Working:** they confirm a review and give us a process. **Failing:** evasion, contact
restricted to procurement, or a refusal to schedule — at which point move to `save-play`
§stop-loss and a managed exit that preserves win-back.

**The honest note:** a customer preparing to leave respects being asked directly and loses
respect for a vendor that pretends not to have noticed. Pretending is the more common choice
and the worse one.

---

### Re-onboard

**Trigger:** Quiet quit. **Objective:** usage recovers to ≥70% of baseline within 45 days.

1. **Before contacting them,** cluster the tickets from the spike period and find the shared
   root cause. Arriving without having read their tickets confirms their conclusion that
   nobody was listening. — CSM + Support lead, +3d
2. Determine whether the root cause was fixed, worked around, or simply abandoned. — Support lead, +3d
3. Reach out with the fix or the workaround in hand — not with a question, and not with
   "checking in". — CSM, +7d
4. Run a working session, not a check-in: screens shared, their data, their workflow. — CSM, +14d
5. Re-establish a cadence and a next milestone. — CSM, +14d

**Working:** usage recovers; a new ticket arrives (paradoxically good — they are engaging).
**Failing:** meeting declined or rescheduled twice; usage flat 45 days after the session.

---

### Buyer re-engagement

**Trigger:** Buyer disconnect. **Objective:** the budget-holding team returns to ≥50% of
baseline, or the budget formally moves with a named new economic buyer.

1. Segment usage by the contracted department and quantify the gap precisely. — CSM, +3d
2. Build a value story on the *buyer's* original objective, not the growing team's activity.
   Be honest if their number is bad — arriving with a good aggregate number they know is not
   theirs destroys credibility. — CSM, +7d
3. Meet the economic buyer directly. — CSM, +14d
4. In parallel, convert the growing team into a second champion base. — CSM, +30d
5. If the use case has genuinely moved, drive a formal budget transfer with the new team's
   leader as the economic buyer. — AM, +45d

---

### Exec re-justification

**Trigger:** Regime change. **Objective:** a meeting with the new executive within 30 days at
which we re-earn the decision.

1. Confirm the exec change and their remit. — CSM, +3d
2. Assemble the ROI evidence pack — bring it to the *first* meeting. A second meeting "to
   gather data" wastes the only window you have. — CSM, +10d
3. Request the meeting through the champion, framed as "you didn't make this decision and we'd
   like to re-earn it". — VP CS, +14d
4. Present business outcomes, not features or history. — VP CS, +30d
5. Establish their objective and rebuild the success plan around it. — CSM, +45d

**Working:** the meeting happens and they name an objective. **Failing:** contact restricted
to procurement, or no exec meeting after 60 days.

---

### Technical rescue

**Trigger:** Technical decoupling. **Objective:** the integration is restored and API volume
recovers within 14 days.

1. Ask whether the disconnect was intentional — one email, before escalating. — CSM, +24h
2. Assign a named engineer, not a CSM check-in. — FDE lead, +72h
3. Offer to fix it at our cost and on our time. — FDE, +72h
4. Run the integration health review from `fde-account-plan`. — FDE, +14d
5. Instrument monitoring so the next silent failure is caught by us, not by nobody. — FDE, +30d

**The diagnostic:** if they wanted it working, why did they not tell us it was broken? A
declined offer of a free fix is confirmatory — escalate commercially.

---

### Implementation restart

**Trigger:** Failed launch — **fired by the onboarding gate at day 60 of the first term, not at
T-90** `[C23]`. **Objective:** the activation event fires under a re-baselined plan.

**Refusal that comes with this play:** while the activation event has never fired, no renewal
plan is written for this account and it is not handed to `renewal-prep`. Every commercial move
made from an implementation that never delivered is a concession, because the customer knows
what they did not get. The artifact prints the withholding and the unlocking milestone.

1. Honest assessment of what failed and who owned each blocked task — ours and theirs. — CSM + Services, +7d
2. Executive sponsor secured on both sides. — VP CS, +14d
3. Re-baselined go-live with a written mutual commitment. — Services, +14d
4. Consider a contract restart or a no-charge extension rather than approaching the renewal on
   a failed implementation. The renewal ask on a project that never delivered is a conversation
   you lose. — AM, +21d
5. Weekly milestone tracking with exec visibility. — Services, ongoing

---

### Sell the acquirer

**Trigger:** Consolidation target. **Objective:** an engaged stakeholder on the acquirer side
within 30 days.

1. Map the acquirer's buying centre and their current stack. — AE, +14d
2. Check whether acquirer-domain users are appearing in the product — that inverts the pattern
   into an expansion opportunity. — CSM, +7d
3. Build a consolidation-onto-us case with migration support offered. — AE + FDE, +21d
4. Approach the acquirer directly; do not rely on the acquired champion, whose influence is at
   its lowest immediately post-close. — AE, +30d

---

### Right-size and redeploy

**Trigger:** Shelfware. **Objective:** a smaller, healthier contract with a live second use
case and a longer term.

1. Quantify the gap: contracted seats vs active users, contracted use cases vs live ones. — CSM, +7d
2. Confirm the account is past 180 days from go-live so ramp is not the explanation. — CSM, +7d
3. Raise it first, voluntarily, well before T-90. A reduction you propose buys goodwill and a
   term; a reduction they propose at T-30 buys nothing. — AM, T-120
4. Trade the seat reduction for a use-case expansion and a longer term. — AM, T-90
5. Open a risk record for the next cycle before closing the downsell (see Contraction spiral). — CSM, at close

---

### Structure for survival

**Trigger:** Budget squeeze. **Objective:** retain the logo with a restructured agreement and a
documented path back up.

1. Confirm the external evidence — do not act on a rumour. — CSM, +7d
2. Lead with "how do we make this survivable for you", not with a discount. A discount offered
   before understanding the constraint is usually the wrong size and permanently reprices the
   account. — AM, +14d
3. Present structures: term restructure, extended payment terms, tier down with a documented
   path up, or a pause with data retained. — AM, +21d
4. Optimise for GRR-preserving downsell over logo loss. — AM
5. Set a review date to revisit the step back up. — CSM, at close

---

### Forced value review

**Trigger:** Value vacuum. **Objective:** a quantified value statement the champion agrees to
and can repeat internally.

1. Attempt to state their business objective and the movement against it, with a source. If
   you cannot, neither can they — that is the finding. — CSM, +3d
2. Reconstruct or establish a baseline (see `success-plan` §baseline capture). — CSM, +14d
3. Quantify what has changed, showing the arithmetic and the assumptions. — CSM, +21d
4. Get the customer to state the number themselves. A number they say is worth ten you say. — CSM, +30d
5. Schedule the review **before** their budget cycle, not after. — CSM, per their fiscal calendar

---

### Named-owner remediation

**Trigger:** Death by a thousand tickets. **Objective:** repeat-issue count falls and CSAT
recovers.

1. Aggregate 180 days of ticket history per account — repeats, total TTR, reopens, who is filing. — Support lead, +3d
2. Assign a named engineering owner with committed dates. — Eng manager, +7d
3. Weekly closure tracking visible to their exec. — Support lead, weekly
4. Offer the fix before offering a credit. A credit without a fix reads as buying silence. — CSM
5. If dates slip a second time, escalate to `save-play` — the problem is now trust, not tickets. — VP CS

---

### Break the cycle

**Trigger:** Contraction spiral. **Objective:** utilisation rises on the reduced base and a
growth case exists — or the account is deliberately moved to a lower-cost coverage tier.

1. Compare the last three renewal outcomes and confirm the trend is monotonic. — AM, +7d
2. Re-run discovery as if this were a new account: objective, owner, what would justify growth. — CSM, +30d
3. If no growth case exists, decide explicitly whether this account belongs in a lower-cost
   tier — see `coverage-and-capacity`. Continuing to spend named-CSM hours on a shrinking base
   is a decision; make it consciously. — VP CS, T-120

---

### Diagnostic conversation

**Trigger:** band ≥ At Risk with no compound pattern matched. **Objective:** find out what is
actually happening before choosing a play.

The honest default. When the data says risk but not why, the correct action is to ask — with
a specific observation, not a general enquiry.

> "I noticed the team's activity in the reporting module dropped off in July after running
> steady since March. I'd rather ask than assume — did something change on your side, or is
> something not working?"

One specific observation, one open question, no pitch. Then re-run `churn-risk` with what you
learn and select a real play.

---

### Engagement proof

**Trigger:** Frictionless renewal `[C24]`. **Objective:** the economic buyer states the objective
and the number in their own words, inside 60 days of the signature.

The renewal closing without an argument is the trigger, not the all-clear. Open the risk record
for the next cycle on the day this one signs.

1. Count the negotiation events on the close — counters, redlines, procurement contacts, term
   arguments — and record the count in the account card. Zero is the finding. — CSM, +3d
2. Book one meeting with the economic buyer whose only agenda is their objective for the coming
   term. Not a QBR, not a thank-you. — AM, +21d
3. Have them state the number. A number they say is worth ten that you say, and it becomes the
   baseline the next renewal is defended with. — CSM, at the meeting
4. Agree a measured baseline with a source and a date for the new term. — CSM, +45d
5. Withhold every expansion ask until a second contact is engaged (`R8`). State the withholding
   in the artifact. — AM, ongoing

**Working:** the buyer meets and names an objective; a second contact engages; a baseline exists.
**Failing:** no buyer meeting inside 60 days. The renewal that just closed was a default —
carry this account into the next cycle as At Risk from T-180 rather than as a retained logo.

---

### Calendar escalation

**Trigger:** two consecutive reschedules or declines by the economic buyer `[C22]`. Fires on the
calendar alone — no usage decline required, and healthy usage does not offset it.

Withdrawal reaches the calendar before it reaches the product, and long before it reaches a
conversation. The cheapest and earliest play in this file.

1. Confirm the pattern from the calendar record: acceptance latency against the account's own
   baseline, reschedule count over 90 days, and who accepted last. — CSM, +2d
2. Rule out the innocent explanations first — a quarter-end, a leave period, an assistant now
   triaging, an internal reorg. One email answers this. — CSM, +2d
3. If unexplained, the third invitation comes from our VP, not the CSM, and carries a specific
   reason to attend rather than a cadence slot. — VP CS, +5d
4. If the VP invitation is also declined or rescheduled, stop inviting and treat the account as
   relationship-severed: escalate to `save-play` and re-thread through a second contact. — VP CS, +14d

**Working:** the buyer accepts and attends within 14 days; acceptance latency returns to baseline.
**Failing:** a third reschedule, or acceptance passed down to a delegate outside the buying centre.

---

## 4. Commitment discipline

The fastest way to lose an at-risk account permanently is to make a commitment you do not
control and then miss it.

| Never commit | Instead |
| --- | --- |
| A roadmap date you do not own | "I'll get you a written answer from product by Friday, including if the answer is no" |
| A fix without an engineering owner having agreed it | Name the owner or do not name a date |
| A discount before understanding the constraint | Understand the constraint first; the right structure is usually not a discount |
| "We'll make this right" | A specific action, an owner and a date |
| A commitment on a call without writing it down within 24 hours | See `post-call-followup` |

Every commitment made during a play goes into the commitment log and appears at the top of the
next `pre-call-brief`. A broken promise to an at-risk account is not recoverable by a second
promise.

---

## 5. Measuring whether plays work

| Metric | Definition | Caveat |
| --- | --- | --- |
| Play completion rate | Plays reaching their exit criteria ÷ plays opened | A low rate usually means capacity, not effort |
| Time to first action | Trigger date → first customer-facing action | The single most controllable variable |
| Band migration | Accounts moving band within 90 days of a play | Use the health migration matrix in `retention-report` |
| Save rate | At-risk accounts renewing ÷ at-risk accounts | Meaningless without a control |
| Retained ARR | Dollars, not logos | The number leadership actually wants |

**On attribution.** You cannot claim a play saved an account without a control. Accounts that
receive plays are selected precisely because they look salvageable, which biases every naive
comparison upward. If you want a defensible number, hold out a random subset of matched
at-risk accounts and compare — and if you will not do that, report activity and outcomes
separately rather than asserting causality. See `cs-playbook-designer` §measurement.
