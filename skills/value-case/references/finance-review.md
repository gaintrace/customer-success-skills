# Surviving the Finance Review

> A value case is not finished when it is written. It is finished when it survives a room
> containing somebody paid to disbelieve it. This file is the rehearsal: the questions that get
> asked, the answers that work, the numbers that get discounted, and the six ways a good case
> dies anyway.
>
> Evidence labels: `[M]` measured · `[V]` vendor-published · `[P]` practitioner convention ·
> `[A]` academic.

**Contents**
- [1. Who is actually in the room](#1-who-is-actually-in-the-room)
- [2. The twelve questions](#2-the-twelve-questions)
- [3. What finance discounts, and by how much](#3-what-finance-discounts-and-by-how-much)
- [4. The definitions they already use](#4-the-definitions-they-already-use)
- [5. Sensitivity and break-even](#5-sensitivity-and-break-even)
- [6. The exclusions list](#6-the-exclusions-list)
- [7. Presentation formats that land](#7-presentation-formats-that-land)
- [8. Procurement, and the new executive](#8-procurement-and-the-new-executive)
- [9. Six ways a good case dies](#9-six-ways-a-good-case-dies)
- [10. The rehearsal](#10-the-rehearsal)

---

## 1. Who is actually in the room

| Person | What they are optimising | What convinces them | What loses them |
| --- | --- | --- | --- |
| **Economic buyer** | Their own credibility for having bought it | A number they can repeat without you present | Anything they cannot defend from memory |
| **Finance business partner** | Not being embarrassed in a budget review | Inputs traced to their own systems | A source they have never heard of |
| **The metric owner** | Their team's numbers being represented fairly | Their own query and their own attribution split | Your version of their operational reality |
| **Procurement** | Price, term, and comparability | Cost per unit of their work | Value language with no unit denominator |
| **A new executive** | Deciding what to keep | Payback in months and what breaks if it stops | The history of a decision they did not make |

Write to the finance business partner and the metric owner. The others are convinced by those
two being convinced.

Post-sale execution is where most B2B software revenue now sits: **74% of participants report
that most of their revenue comes from existing customers** (Pavilion / 6sense Customer Revenue
Leadership Study, ~793 senior customer growth leaders, 2025–26) `[V]`. That is the argument for
why this conversation is worth an hour of a CFO's time — and why arriving without a defensible
number is expensive.

## 2. The twelve questions

Prepare an answer to each. Six of them will be asked.

| # | The question | The answer that works | The answer that loses |
| --- | --- | --- | --- |
| 1 | "Where did the baseline come from?" | "Your helpdesk, `ticket.type = tier_1`, pulled by Priya on 4 April — a three-month mean, not one day." | "From our analytics." |
| 2 | "Who says it was you?" | "Priya set the split at 70/30 by email on 14 August. The 30% is your knowledge-base rewrite." | "The improvement follows our deployment." |
| 3 | "What else changed that year?" | Names two confounders before being asked, with dates | "Nothing material." |
| 4 | "Whose cost per hour is that?" | "Yours, from your 2025 support cost model. Low end of the range you gave." | "Industry standard for a knowledge worker." |
| 5 | "Hours saved — saved to do what?" | "Two FTE-equivalents moved to the audit-readiness programme. That is why recapture is 50% rather than zero." | "It frees the team up." |
| 6 | "Does this include what we spent?" | "Fees, services, your 410 project hours and 0.2 FTE of admin. Total $252k." | Subscription fees only |
| 7 | "What if the attribution is half that?" | "Payback moves from 8.9 to 15 months and it is still positive. Break-even is at 31%." | "We think 70% is conservative." |
| 8 | "Why should I believe next year's number?" | "Same query, same owner, same definition — stored, and re-run quarterly. Here is the last four quarters." | "We'll build a new model." |
| 9 | "What did you leave out?" | The exclusions list, unprompted | "This is the full picture." |
| 10 | "Is any of this soft?" | "None of it is in the total. The soft panel is separate and un-monetised." | Soft benefits inside the headline |
| 11 | "What happens if we stop?" | The specific mechanism that reverts, with the metric that would move and how fast | "You'd lose the value." |
| 12 | "Did this number go up since last time?" | "Yes — because the volume denominator grew from 96k to 141k tickets. Same unit cost, same α." | An upward revision with no named input change |

**Question 9 is the one that decides the room.** Volunteering what you did not count is what
makes what you did count believable `[P]`.

## 3. What finance discounts, and by how much

| Benefit class | Their instinct | How to survive it |
| --- | --- | --- |
| **Cash-releasing** | Accepted in full | Have the contract number or the requisition ID |
| **Cost avoided** | Discounted — it never appears in year-on-year variance | Show the volume growth explicitly: their cost stayed flat while their work grew |
| **Productivity** | Heavily discounted unless recapture is explicit | Name the redeployment or the avoided hire. Without one, expect the whole line to be struck |
| **Revenue influenced** | Discounted to the attributed figure, then discounted again for optimism | Lead with gross and attributed together; use their α; never argue it upward |
| **Risk reduced** | Rejected unless the probability is theirs | Their register, or drop the line (`R22`) |
| **Soft** | Not credited at all | Keep it out of the total; keep it in the room as their words |

The pattern: finance credits money that moved and discounts money that would have moved. Build
the headline out of the first category wherever it exists — one retired contract is worth more
in that room than three times its value in released hours.

## 4. The definitions they already use

Use these words, in these senses `[V]`:

```
ROI      = (Benefits − Costs) / Costs
Payback  = the point at which cumulative net benefit equals the initial investment
PV       = present value of discounted costs and benefits at the discount rate
NPV      = present value of discounted future net cash flows
```

| Convention | Value | Note |
| --- | --- | --- |
| Discount rate | 10% in Forrester TEI; organisations typically use 8–16% `[V]` | Ask theirs. Asking is itself a credibility move |
| Risk adjustment | Applied downward, to reflect the likelihood that estimates meet projections and are tracked over time `[V]` | Show it as a line, not as a quiet reduction |
| Initial investment | Time 0, undiscounted; everything else discounts at year end `[V]` | |

**Do not import an ROI multiple from a published study as evidence about this customer.** A TEI
figure is a measurement of a composite organisation in someone else's study; here it is a proxy,
subject to the `B4` rule in `baseline-methods.md`.

## 5. Sensitivity and break-even

**A value case that cannot survive ±30% on its central assumption is not ready to present.**

| Step | Do |
| --- | --- |
| 1 | Identify the driver the total is most sensitive to — usually recapture, α, or the loaded hourly. Move each ±30% and see which moves the total most |
| 2 | Build three scenarios: **Conservative** (driver −30%, low end of every range, all haircuts), **Central** (as recorded), **Stretch** (driver +30%) |
| 3 | Present the **conservative** number as the headline. Central and stretch are the range around it, never the claim |
| 4 | Compute the break-even: the driver value at which net benefit equals total cost |
| 5 | Write one sentence and put it in the customer artifact unprompted |

> "Even at 40% attribution and zero productivity recapture, payback is 15 months. Break-even on
> attribution is 31%."

Sensitivity and scenario analysis are standard in board-level investment memos, so a case
arriving without them reads as unfinished to anyone with a finance background `[P]`. Volunteering
the downside is the highest-return move available: it buys credibility that cannot be bought any
other way `[P]`.

`../scripts/roi.py` computes all of this — three scenarios, payback, break-even, and a
one-driver ±30% sweep — deterministically, so the numbers in the deck match the numbers in the
appendix.

## 6. The exclusions list

Short, specific, and on the artifact. Three to five items.

| Good exclusion | Why it helps |
| --- | --- |
| "Their knowledge-base rewrite's independent contribution" | Shows you separated a confounder rather than absorbing it |
| "Two integrations their engineering team built and maintains" | Concedes value they created themselves |
| "Any FY27 benefit" | Refuses to project past the term |
| "Every soft benefit — those are listed separately, un-monetised" | Shows the discipline |
| "Onboarding-time improvement — attribution unestablished" | Shows a line was refused on principle |

Avoid exclusions that are really disclaimers ("subject to change", "estimates only"). An
exclusion names a specific thing you could have counted and chose not to.

## 7. Presentation formats that land

| Format | Why it works |
| --- | --- |
| **Payback in months** | The most portable number in the document; it survives being repeated by someone who never saw the workings |
| **Per unit of their business** | "$18.40 per ticket × 141,000 tickets" beats "$2.6M value delivered" — the first invites verification, the second invites suspicion `[P]` |
| **Their currency and fiscal calendar** | A number in the wrong fiscal frame gets re-derived by their analyst, and re-derived wrong |
| **One headline, dated, with the window on it** | "FY26, 1 Oct 2025 – 30 Sep 2026" removes the first ambiguity anyone reaches for |
| **The formula in a footnote with every input's source** | Turns "trust me" into "check me" |
| **Their words for their objective** | Kristen Hayer's point: measure in the customer's language, against business outcomes rather than activity dashboards `[P]` |

And the framing that decides whether you are invited back: give the economic buyer something
they can paste into their own board or vendor-performance deck. An executive who can reuse your
page will reuse you.

## 8. Procurement, and the new executive

**Procurement** is not evaluating value; it is evaluating comparability and price. Give them a
unit denominator — cost per ticket, per claim, per shipment, per rep — because that is the form
in which they can compare you with an alternative. A value case with no denominator gets reduced
to its annual fee, which is the only number they can compare.

**A new executive** has no ownership of the original decision and every incentive to run a
consolidation review. What works with them, in order:

| Order | What to lead with |
| --- | --- |
| 1 | Payback in months, and the date the measurement was taken |
| 2 | The name of the person inside their organisation who validated the inputs |
| 3 | What specifically reverts if it stops, and how fast |
| 4 | What is not counted |
| 5 | The history — four quarters of the same query, not a new model |

Do not lead with the relationship, the history of the account, or how long you have worked
together. None of it is evidence to someone who was not there.

## 9. Six ways a good case dies

| Death | Mechanism | Prevention |
| --- | --- | --- |
| **The unsourced input** | One number has no name on it; every other number is now suspect | Input register, attester named, one source per input |
| **The silent 100%** | α was never stated, so it was 1.0 | α with its level, always, never 1.0 |
| **The missing cost** | Their internal labour was omitted; their finance partner adds it in the room | Full cost inventory, including their project and admin hours |
| **The upward revision** | The figure grew since last quarter with no explanation | Name the input that changed, or leave the number where it was |
| **The proxy** | An industry benchmark, discovered in a footnote, presented as a measurement | Print the rung next to every number |
| **The wrong fiscal frame** | Your quarters, their year; the analyst re-derives it and gets a different answer | Their calendar, their currency, the window on the page |

Five of the six are unforced. That is the point of the pre-return audit.

## 10. The rehearsal

Twenty minutes before it matters. Read the artifact aloud and stop at every number.

- [ ] Every figure: can I say where it came from without looking?
- [ ] Every derived figure: can I show the arithmetic in one line?
- [ ] The headline: is it the **conservative** scenario?
- [ ] The sensitivity sentence: is it on the page, unprompted?
- [ ] The exclusions: three to five, specific, not disclaimers?
- [ ] α: stated, levelled, never 1.0, and named to a person where it is A3?
- [ ] The cost side: does it include their labour, services and training?
- [ ] Windows: benefit and cost cover the same period?
- [ ] The bad news: is the missed line reported before the successful ones (`R20`)?
- [ ] The firewall: no health band, risk language, ARR-at-risk, forecast or cost-to-serve on the customer page (`R18`)?
- [ ] The ask: is there none? A value case carries no commercial ask (`R11`)
- [ ] The next date: is the refresh scheduled, with an owner, before I leave the room?

If a question stops you, that is the question they will ask. Fix it before, not during.
