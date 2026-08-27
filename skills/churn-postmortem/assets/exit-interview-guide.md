# The Post-Churn Interview

> The one direct source of evidence about what the customer experienced, and the one most often
> wasted. Wasted three ways: asked at the wrong moment, asked by the wrong person, and asked "why
> did you leave?" — which produces a reason rather than a chronology.
>
> Read `../../cs-context/references/customer-voice.md` before writing anything here. Everything
> below the divider in each block is send-ready as written; a block containing a bracket is not.

**Contents**
- [1. When, and who asks](#1-when-and-who-asks)
- [2. The request](#2-the-request)
- [3. The question set](#3-the-question-set)
- [4. Running it](#4-running-it)
- [5. The firewall in an exit conversation](#5-the-firewall-in-an-exit-conversation)
- [6. What to record](#6-what-to-record)
- [7. When they say no](#7-when-they-say-no)

---

## 1. When, and who asks

| Decision | Rule | Why |
| --- | --- | --- |
| **When** | 2–4 weeks after the **effective date**, not at cancellation | At the cancellation moment the customer wants out of the conversation. Lincoln Murphy's framing is that they will say whatever they think you need to hear to let them out `[P]`. Afterwards, the incentive is gone |
| **Who asks** | Anyone but the account owner — CS Ops, a CS leader, or a third party for the largest losses | The owner hears confirmation of what they already believed, and the customer softens the answer to protect them. Clozd's case for post-churn interviews rests on the customer having no remaining stake in the relationship `[V]`; an account owner in the room restores one |
| **Whom to ask** | The **economic buyer** first, then the champion or admin. Record who answered and their role | Respondent bias runs one direction: whoever is still there and still fond of you under-reports sponsor loss and buyer disconnect |
| **How long** | Twenty minutes, and end at twenty | The ask is small on purpose. A thirty-minute request converts far worse and the last ten minutes add nothing |
| **Recording** | Offer, do not assume. Take notes either way | An unrecorded honest answer beats a recorded careful one |
| **Preparation** | Build the timeline **first** | Arriving with dated events turns "why did you leave" into "was the March reconciliation thing the deciding factor, or was it already decided?" — a question they can answer precisely |

**Never combine the interview with a win-back attempt.** The moment a save appears, every
remaining answer is negotiation. Win-back is a separate conversation, months later, with a
different opener.

## 2. The request

Three variants. Each is send-ready as written; swap the specifics for the account's own. **If a
specific is genuinely unavailable, delete that sentence rather than leaving a bracket** — a block
with a placeholder in it is the most common way an unedited template reaches a customer.

**A. Standard — from CS Ops or a CS leader, 2–4 weeks after the effective date.**

````
════════════════════════════════════════════════════════════
CUSTOMER-FACING — copy the block below and send as written.
Everything above this line is internal. Do not forward it.
════════════════════════════════════════════════════════════

```text
Subject: 20 minutes on what we got wrong at Northwind

Hi Dana,

Northwind came off the platform on 31 August, and I'd like to understand
that decision properly rather than guess at it. I run customer success
operations here, so this isn't a save attempt — the contract is closed.

The thing I want to get right: the intercompany reconciliation work you
raised in March never got finished. I want to know whether that decided it
or whether it was already decided by then.

Twenty minutes, no recording unless you'd prefer one. Thursday 11 September
or Friday 12th — and if you'd rather not, that's completely fine, with no
follow-up either way.

Thank you for three years, and for pushing us on the audit log — that
shipped because of you.

Priya
```
````

**B. Executive — where the loss was above the segment's ARR threshold, sent by a VP or the CCO.**

````
════════════════════════════════════════════════════════════
CUSTOMER-FACING — copy the block below and send as written.
Everything above this line is internal. Do not forward it.
════════════════════════════════════════════════════════════

```text
Subject: Where we lost this — 20 minutes with you

Hi Marcus,

You moved off us at the end of Q2 after four years. I'd rather hear the
account of that from you than assemble it from our own records, which will
be flattering and incomplete.

I'm not asking you to reconsider. I'm asking because two other customers in
manufacturing are on the same path we put you on, and I'd like to change it
before they get there.

Twenty minutes in the next fortnight, whenever suits. I'll come with a
timeline of what we did and when, so you can correct it rather than
reconstruct it.

Best,
Amara
VP Customer Success
```
````

**C. Involuntary — the subscription lapsed on a payment failure and they may not know why.**

````
════════════════════════════════════════════════════════════
CUSTOMER-FACING — copy the block below and send as written.
Everything above this line is internal. Do not forward it.
════════════════════════════════════════════════════════════

```text
Subject: Your account closed on a card failure — that was our fault

Hi Sam,

Your subscription ended on 12 August because three payment attempts failed
against a card that expired in July, and our notices went to an address
that had bounced since May. You did not choose this, and we should have
caught it.

Two things. Your data is retained until 11 October, so nothing is lost if
you want it back. And whether or not you come back, I'd like ten minutes on
what would have reached you — we clearly got the notice path wrong and
you're not the only one.

Either way, here's the export link so the data is in your hands rather than
ours: https://app.example.com/exports/northwind-2026-08

Sam
```
````

## 3. The question set

Ten questions, asked in this order. The order matters more than the wording: chronology before
verdict, and their words before yours.

| # | Question | What it is for |
| --- | --- | --- |
| 1 | "When did you personally first think this probably wasn't going to continue?" | The single best route to `decision_date`. Ask for a month; most people can give one |
| 2 | "What was happening around then?" | The proximate cause, in their words, before you name any candidate |
| 3 | "Who else was part of the decision, and when did they get involved?" | The buying committee, and whether procurement or a new exec arrived first |
| 4 | "What were you hoping this would do for you when you bought it?" | The original desired outcome — often different from what our record says it was |
| 5 | "How close did it get to that?" | The gap, in their measure. A number here is worth more than any of ours |
| 6 | "What's replacing it?" | `competitor`, including "nothing" and "a spreadsheet", which are findings |
| 7 | "Was there a point where we could have changed the outcome? What would we have had to do?" | Their savability read. Frequently contradicts ours, in both directions |
| 8 | "What did we do that was actually useful?" | Guards against a review that learns only what to stop doing |
| 9 | "If you were running our customer success team, what one thing would you change?" | The most productive question in the set. It gives them the vendor's chair, which people enjoy and answer generously |
| 10 | "Anything I should have asked and didn't?" | Catches the thing the timeline could never have shown |

**Ask one, then stop talking** (`R16`). The second half of the answer arrives after the silence.
Do not defend, do not explain, and do not correct their recollection even where the timeline
disagrees — record the disagreement and use it later.

## 4. Running it

| Do | Not |
| --- | --- |
| Open with the timeline: "here's what I think happened, in dates — correct me" | Open with "so, why did you leave?" |
| Use their words back to them, exactly | Paraphrase into vendor vocabulary |
| Ask about process and sequence | Ask them to judge our people |
| Let a silence run for five seconds | Fill it |
| Say plainly at the start that nothing is being sold | Leave the possibility hanging, which makes every answer strategic |
| Note the exact wording of the reason they give | Summarise it into a picklist value during the call |
| End at twenty minutes even mid-flow — and ask to continue another time | Overrun, which makes the next request harder for everyone |

## 5. The firewall in an exit conversation

Everything in `../../cs-context/references/customer-voice.md` Part 2 applies, with three additions
specific to a loss.

| Never say | Why | Instead |
| --- | --- | --- |
| Anything about health scores, risk bands, ARR at risk, forecast categories, save plays or coverage tiers | They learn you were grading them and never said so | Talk about what happened, in dates |
| "We noticed your champion left" | An inference stated as a fact, about a named person | "Who ended up owning this after Jamie?" |
| "We flagged this internally in March" | Invites the obvious question about why they heard nothing until June | Say what you are changing, not what you knew |
| Any assessment of one of their people | Ends the conversation and travels further than you expect | Ask about roles and sequence, never about individuals |
| Another customer's name or situation | Tells them exactly how you will describe them next week | Speak only about them |

## 6. What to record

| Field | Rule |
| --- | --- |
| `stated_reason` | **Verbatim.** One sentence in their words, in quotation marks, with the date and the speaker's role |
| `decision_date_stated` | Their answer to question 1, alongside the inferred date. Record the gap — it measures how long administration lagged the decision |
| Savability, their view | Their answer to question 7, kept separate from our verdict |
| Replacement | `competitor` — named, `none`, `in-house`, or `no-replacement` |
| Quotes worth keeping | Two or three, dated and attributed by role. These are what make the quarterly pack land |
| Respondent and role | Every quote and score belongs to a person, not to the account |
| Response rate | Interviews completed ÷ interviews requested, and the ARR share covered. Printed beside every reason table |

The interview **informs** the coding; it does not perform it. `primary_reason` is coded from the
timeline by the facilitator, and where the two disagree, both are recorded and the disagreement is
the finding.

## 7. When they say no

Roughly half will not answer, and the half that does is not a random sample — it skews toward
amicable losses, which biases the whole quarter's reason mix toward polite reasons. Two rules:
**report the response rate and its ARR coverage** beside every reason table, and **do not chase**.
One request, one gentle reminder after a week, then stop. A second chase converts a neutral exit
into a bad one, and the record is finished without them:

> `stated_reason`: **UNKNOWN — interview declined 2026-09-14.** Coded from timeline evidence only;
> confidence capped at Medium.
