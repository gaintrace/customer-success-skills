# Change Control

> Change control is not paperwork that protects the vendor. It is the mechanism that lets you say
> yes to a good idea without either lying about the date or quietly paying for it yourself.
>
> SPI Research's 2026 Professional Services Maturity Benchmark (509 PS organisations, FY2025
> data) identifies **change-control discipline** as one of the two maturity dimensions on which
> high-performing organisations separate furthest from the rest — the same firms running 6.9%
> project overrun against 12.1% `[M]`. PMI's *Pulse of the Profession* 2018 found 52% of projects
> experienced scope creep or uncontrolled scope change in the prior 12 months, against 43% five
> years earlier `[M]`.
>
> Evidence labels: `[M]` measured · `[V]` vendor · `[P]` practitioner rule · `[A]` academic.

**Contents**
1. [How creep actually happens](#1-how-creep-actually-happens)
2. [The classification tree](#2-the-classification-tree)
3. [Triggers and thresholds](#3-triggers-and-thresholds)
4. [The approval matrix](#4-the-approval-matrix)
5. [The creep ledger](#5-the-creep-ledger)
6. [Reply scripts](#6-reply-scripts)
7. [Change order anatomy](#7-change-order-anatomy)
8. [Schedule change orders](#8-schedule-change-orders)
9. [Anti-patterns](#9-anti-patterns)

---

## 1. How creep actually happens

Not as a demand. As six reasonable requests from people you like, each obviously small, each
arriving in a different channel, none of which anybody wrote down.

| Vector | What it sounds like | Why it lands | The guard |
| --- | --- | --- | --- |
| **The corridor ask** | "While you're in there, could you…" | Said in person, to the engineer, mid-task | Everything goes in the ledger before it goes in the branch |
| **The scope-adjacent bug** | "This doesn't work" — for something never in scope | Framed as a defect, so refusing it looks defensive | Check the criterion. If it is not in the criteria, it is a change |
| **Criterion drift** | "When we said 5 days error-free, we meant under load" | The criterion moved after the build started | Criteria frozen at signature; a change to one is trigger 1 |
| **The helpful engineer** | Our own person says yes to be useful | The fastest and most common vector, and nobody logs it | One line in the ledger. Praise the instinct, log the hour |
| **The new stakeholder** | Someone who was not in the scoping call arrives with requirements | They are not wrong; they were just absent | Route through the sponsor, not through the backlog |
| **Environment drift** | "Also, can it work in our UAT tenant?" | An extra environment sounds like a setting | Category 6 exclusion, priced |
| **The pilot that grew** | Pilot users start using it for real work | Success looks like scope | Production criteria written at pilot signature |
| **Silent absorption** | Nothing is said; the team works late | Invisible until the date slips | The absorbed-hours ceiling (`R21`) |

**The recurrence test**, applied at the moment of the ask: *if this request arrived every month,
would we still absorb it?* If no, it is a change order now — while it is small, while the
relationship is warm, and while nobody has to be told they were wrong.

---

## 2. The classification tree

Run in order. Stop at the first that answers.

| # | Question | If yes |
| --- | --- | --- |
| 1 | Is it a defect against a **signed acceptance criterion**? | Not a change. Fix it, re-deliver, new clock. No fee, no argument |
| 2 | Is it required for a **defined in-scope outcome** to occur at all? | Not a change — it was always implied by the outcome. Absorb, log it, and fix the SOW language for next time |
| 3 | Does it change a **signed acceptance criterion**? | Change order, always, regardless of size |
| 4 | Is it a **new deliverable**? | Change order, always |
| 5 | Does it live **inside a system we do not control**? | Not scope at all — dependency (`scope-boundaries.md` §6), with an owner and a slip consequence |
| 6 | Would a **second customer** want the identical thing? | Route to `custom-vs-product` before pricing it. The answer changes what you build |
| 7 | Is the effort **above the Step 8 threshold**, or is it recurring? | Change order |
| 8 | Anything else | Absorb **and log it** in the creep ledger |

**Rows 1 and 2 matter as much as rows 3 and 4.** A change-control process that classifies genuine
defects as changes destroys its own legitimacy in one move, and the customer stops engaging with
it for the requests that really are changes.

---

## 3. Triggers and thresholds

| # | Trigger | Threshold | Fee effect |
| --- | --- | --- | --- |
| 1 | A new deliverable, or a change to a signed acceptance criterion | Always, any size | Priced |
| 2 | An assumption in the register proven false | Where the recorded delta exceeds row 3 | Priced |
| 3 | Additional effort | **> 8 hours, or > 5% of remaining budget — whichever is smaller** `[P]` | Priced |
| 4 | A date moves because a customer dependency slipped | Always | **None** — schedule only (§8) |

**Scale the row-3 threshold to the engagement**, and write the number into the SOW so it is never
argued mid-delivery:

| Engagement size | Absorb threshold `[P]` | Absorbed-hours ceiling (`R21`) `[P]` |
| --- | --- | --- |
| < 100 hours | 2 hours | 6 hours |
| 100–400 hours | 8 hours | 20 hours |
| 400–1,000 hours | 16 hours | 40 hours |
| > 1,000 hours | 24 hours, or 1% of remaining budget | 3% of total effort |

**The ceiling is the point of `R21`.** Absorbing small requests is good practice and good
relationship management, right up until it is unbounded. At the ceiling, the next request is a
change order or a written decline — and the conversation is easy, because the ledger shows what
has already been given.

---

## 4. The approval matrix

Named in the SOW at signature, so the question is never asked mid-engagement.

| Change size `[P]` | Our approver | Their approver | Turnaround target |
| --- | --- | --- | --- |
| Under the absorb threshold | Delivery lead (log only) | None | Same day |
| Absorb threshold → 5% of fee | Delivery lead | Their named delivery owner | 2 business days |
| 5–15% of fee | Delivery manager | Their named commercial approver | 3 business days |
| Over 15% of fee, or any date change past a contractual milestone | Services leadership | Their executive sponsor | 5 business days |
| Anything touching the fee ceiling in a capped shape | Services leadership + account owner | Their commercial approver | 5 business days |
| Anything touching security, data residency or PII handling | Security owner, in writing | Their security reviewer | Their board's cadence — assume weeks |

**Two rules.** Approval is *written* — a reply to the change order email counts, a verbal "sounds
fine" does not, and the person recording it should be the one who benefits least from
ambiguity. And **the approver is named, not roled**: "their PMO" is not an approver, and finding
out who is takes three days you will not have.

---

## 5. The creep ledger

The single highest-return artifact in this file, and the cheapest. One row per absorbed request.

| Column | Example |
| --- | --- |
| Date | 2026-09-14 |
| Request | Add the finance cost-centre field to the sync |
| Requested by | Marcus Bell, Data Lead |
| Channel | Slack, direct to engineer |
| Classified as | Absorb (tree row 8) |
| Hours | 3 |
| Cumulative absorbed | 14 of 20 ceiling |
| Note | Third field addition; if a fourth arrives, raise as a CO |

**Report the cumulative figure at every internal delivery review, and once to the customer at the
mid-point** — not to bill it retroactively, which is the one move that turns goodwill into
resentment, but to make the pattern visible while it is still cheap:

> "For context, we have picked up about fourteen hours of extra requests along the way and they
> have not been a problem. We are near the point where the next one starts to affect the date, so
> I would rather flag it now than surprise you in three weeks."

That sentence is the entire mechanism. It converts an invisible transfer into a shared fact, it
gives the customer the chance to prioritise, and it makes the eventual change order expected
rather than defensive.

**Read the ledger for pattern, not just total.** Three or more requests in the same category
means the SOW's boundary in that category was drawn wrong, and the fix is the next SOW's default,
not this one's invoice.

---

## 6. Reply scripts

### 6.1 Yes, and that is a change — the four moves

| Move | Do | Never |
| --- | --- | --- |
| **1. Say yes to the outcome, unconditionally** | "Yes — that is worth doing." | Lead with "that's out of scope" |
| **2. Name the trade specifically** | "It is about a week, and it lands on top of milestone 3." | "That may impact the timeline" |
| **3. Offer the choice, not the invoice** | Three options: add and move the date · swap for something scoped and unwanted · park for phase 2, written up today | A price with no alternatives |
| **4. Put it in writing the same day, small** | Three lines, one page maximum | A re-negotiation of the whole SOW |

Full example, to a data lead who asked in a channel:

```text
Yes, worth doing — the cost-centre field is the thing that makes the finance report
usable, and I would rather have it in.

It is about a week of work and it sits on top of milestone 3, so there are three
ways to play it:

  • Add it and milestone 3 moves from 12 to 19 October.
  • Swap it for the batch export we scoped in March, which nobody has asked
    about since. Same date, no change in fee.
  • Park it for phase 2 — I will write it up today so it does not get lost.

Which of those works best for you? I will send a one-pager for whichever you pick
so it is on the record and nobody is guessing later.
```

Note what is absent: no apology, no contract language, no defensiveness, and no implication that
they did something wrong by asking. **The change order is never the thing that damages the
relationship. The surprise is.**

### 6.2 No — and here is what you get instead

Reserved for requests that are unbounded, that fork the product, or that create something nobody
will own. Say no in the first line (`R20`), give the reasoning, leave them something.

```text
We are not going to build the custom portal — not as a cost thing, but because it
would sit outside the upgrade path and you would end up carrying it every release.

What we can do instead is configure the standard console with your fields and your
naming, which covers the three things you showed me on Tuesday, and I will raise the
embedded-view request with our product team with your name on it.

If the portal is genuinely the deciding factor, say so and we will talk about it
properly rather than me quietly hoping it goes away.
```

Never say "it's on the roadmap" unless it is, with a date the named owner has agreed (`R19`).
It is the kindest-sounding sentence in this work and the most damaging.

### 6.3 Not yet — the deferral that actually gets revisited

A deferral with no date is a decline that nobody has admitted to. Write it into the Deferred
Scope table (`R14`) with a revisit date and an owner, and say so:

```text
Parking this until after go-live rather than dropping it — it goes on the deferred
list with a review on 14 November, and I will bring it back then whether or not
anyone chases me.
```

### 6.4 The one you must not send

A silent yes. Absorbing without logging is not generosity; it is an undeclared transfer that
surfaces six weeks later as a missed date, and the customer — who never knew it was a favour —
experiences it as a delivery failure.

---

## 7. Change order anatomy

One page. Template: `../assets/change-order-template.md`.

| Section | Content | Why it is there |
| --- | --- | --- |
| Reference | CO number, parent SOW, date | It must be findable in twelve months |
| Requested by | Named person, date, channel | Anchors the change to a real ask |
| What changes | The deliverable, in one paragraph, in their language | The section they will actually read |
| Acceptance criterion | Given/when/then, tester, acceptor, deemed window | A change order without a criterion re-creates the original problem |
| Effort | Hours, three-point where the change is non-trivial | Consistency with the SOW's method |
| Fee effect | Amount, or "no fee change — absorbed against contingency", or "schedule only" | Never left blank |
| Schedule effect | Which milestones move, and to when | The half the customer cares about most |
| Dependencies created | Anything new they must supply, with owner and date | New scope brings new dependencies |
| Assumptions | Any new assumption, with its delta | Feeds the register |
| Approval | Two names, two dates | Per §4 |

**Same day, or it is a dispute.** A change order raised the day of the request is
administration. The identical document raised three weeks later, for work already done, is a
bill for a favour, and it is remembered.

---

## 8. Schedule change orders

The most-skipped and most useful instrument in the set: **no fee change, dates only, issued
whenever a customer-side dependency slips.**

| Property | Value |
| --- | --- |
| Trigger | Any dependency past its needed-by date by more than 3 business days `[P]` |
| Fee effect | None |
| Content | The dependency, its owner, the date it was needed, the date it landed or its current status, the milestones that move and their new dates |
| Approval | Delivery leads both sides |
| Purpose | The record shows **why** the date moved, at the time, in neutral language |

Without it, a delivery date slips and the reason lives in someone's memory. Six months later at
the renewal the customer remembers a late project, and the FDE remembers waiting five weeks for
a service account — and only one of those recollections is written down.

Write it without blame. Not *"the customer failed to provide access"* but:

```text
Milestone 2 moves from 3 to 17 October. The service account request (raised
14 September, ticket INF-4471) is still open with your infrastructure team, and the
integration work cannot start until it lands. Everything downstream shifts by the
same amount. Nothing else changes and there is no change in fee.

If it would help, I am happy to join the call with your infra team — sometimes it
moves faster when we can answer the security questions live.
```

Neutral, dated, sourced, and it ends with an offer of help. That is a document you can send to a
sponsor without either side losing face, and it is the document that makes the renewal
conversation possible.

---

## 9. Anti-patterns

| Anti-pattern | Correction |
| --- | --- |
| "That's out of scope" as the first sentence | Say yes to the outcome first, then name the trade and offer the choice |
| Classifying a genuine defect as a change | Tree row 1. One misclassification destroys the process's legitimacy |
| A change order raised weeks after the work | Same day, three lines. Later, it is a bill for a favour |
| Verbal approval accepted | Written. A reply to the email counts; "sounds fine" in a corridor does not |
| Approver recorded as a role, not a person | Name both approvers in the SOW at signature |
| Absorbing with no log | The creep ledger. Five absorbed favours is a change order nobody raised |
| An absorbed-work policy with no ceiling | `R21` — state the ceiling in hours; at the ceiling it is a CO or a written decline |
| Billing the creep ledger retroactively | Never. It exists to make the pattern visible, not to invoice the past |
| A change order with no acceptance criterion | It re-creates the original problem one layer down |
| A deferral with no revisit date | `R14` — Deferred Scope table, date and owner, or admit it is a decline |
| "It's on the roadmap" when it is not | `R19`. A clear no with the nearest alternative preserves more trust than a soft yes |
| A date moving with no schedule change order | Issue it. Neutral, dated, sourced — it is what makes the renewal conversation possible |
| The same category appearing three times in the ledger | The boundary was drawn wrong. Fix the next SOW's default, not this one's invoice |
| Change control introduced after the first dispute | Triggers, thresholds and approvers are in the SOW at signature or they are unenforceable |
