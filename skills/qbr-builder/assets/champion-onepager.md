# The Champion's Internal One-Pager — Part F

> The artifact that decides the renewal, written for a meeting you are not in. Your champion
> sits in front of their VP Finance or their finance business partner and either carries a page
> written for that room or forwards our deck — which reads as vendor material and loses.
>
> **This is not a subset of Part B.** Different audience, different voice, different ask. Ours
> argues that we delivered; theirs argues that *their team* delivered and should keep going.
> Send it to the champion alone, editable, with no branding of ours on it.
>
> Governed by `../../cs-context/references/customer-voice.md`. Run the leak scan before it
> leaves your outbox — no health score, risk band, ARR at risk, forecast category, save play,
> coverage tier or assessment of any named person.

**Contents**
1. [The seven required slots](#1-the-seven-required-slots)
2. [The credit slot — the one that decides whether it gets sent](#2-the-credit-slot)
3. [Voice rules and the rewrite table](#3-voice-rules-and-the-rewrite-table)
4. [Filled worked example](#4-filled-worked-example)
5. [Pre-send checklist](#5-pre-send-checklist)

---

## 1. The seven required slots

None may be left empty. An empty slot is not a shorter page; it is a page that fails in the room.

| # | Slot | Required content | Source in the plan |
| --- | --- | --- | --- |
| 1 | **Their objective** | The objective as their team's commitment, in their words | A2, tier 1–3 only |
| 2 | **Credit** | What *their team* achieved this period, their team as the actor | A7, pre-call question 5 |
| 3 | **The one number** | The single headline figure, in the form the champion said it, dated | A6 headline row, customer-stated cell |
| 4 | **What didn't land** | The shortfall in their units, what is already fixed, what is owed and by when | A5 |
| 5 | **Their ask** | The decision they are asking their own leadership for, and the date they need it | A4 pre-wire ledger |
| 6 | **What happens next** | What we owe, named person, calendar date | Part D |
| 7 | **If nothing changes** | The value forgone, in their units, stated flatly | A6 roll-up, cost of inaction |

**One number only (C19).** Slot 3 carries one figure and at most one unit metric beneath it.
Every supporting metric stays in Appendix V of our deck. A finance reader given four numbers
picks the weakest one to argue with, and the champion loses the meeting on our behalf.

**Never invent slot 3 (C5).** If no customer-stated number exists in A6, the page carries the
unit metric and no dollars, and the ask changes to *"we need a number on this before the
planning round"*. A figure the champion has not said is a figure they cannot defend when their
VP turns and asks where it came from.

---

## 2. The credit slot

**Refusal condition (C20): no credit line, no one-pager.** Where you cannot name something
specific their team did, do not emit Part F. Ask the pre-call question first —

> *"When your VP asks what changed this quarter, what do you want to be able to say your team
> did?"*

— and write the page afterwards. A one-pager with no win in it asks the champion to spend
internal credibility on our behalf and hands them nothing back. They send that page once.

The credit must be **checkable by someone who was there**. "Your team did a great job" is not
credit; "your FP&A team rebuilt the reconciliation step and cut two days out of it before we
shipped anything" is credit, because their VP can verify it and the champion can be proud of it.

| Test | Passes | Fails |
| --- | --- | --- |
| Who is the subject of the sentence? | Their team, or a named person on their side | Our product, our team, "the platform" |
| Could their VP verify it? | Yes — a named artifact, meeting, migration or number | No — an adjective |
| Would the champion say it out loud about themselves? | Yes | It reads as flattery, or as our claim |

---

## 3. Voice rules and the rewrite table

Their pronouns, their units, their metric names, their date format. No superlatives, no
adjectives standing in for numbers, no sentence that only a vendor would write.

| Rejected | Why | Rewritten |
| --- | --- | --- |
| "The platform reduced close time by 3.5 days" | Our product is the subject | "We took 3.5 days out of the month-end close" |
| "We're delighted with the partnership" | Vendor language in their mouth | Delete. It carries nothing to their VP |
| "Significant efficiency gains were achieved" | Adjective in place of a number, and no actor | "My team runs the close in 5.5 days instead of 9.0" |
| "Our vendor missed the September integration" | Blame, and it makes the champion look badly advised | "The September integration landed six weeks late; it cost us about 120 hours across two closes. It is fixed, and Sam owns it end to end now" |
| "Renew the contract" | Our ask, our word | "Keep the Finance licence line in the FY27 plan, and add Legal in Q1" |
| "Risk of churn if we don't proceed" | Internal risk language, and a threat | "If Legal stays on the manual process we keep the two-day audit lag we flagged in March" |
| "ROI of 1.34x" | Our arithmetic, and one number too many for their room | "We are getting back more than we put in, on our own loaded rate — the working is in the appendix if Finance wants it" |

---

## 4. Filled worked example

Champion: J. Alvarez, Controller. Audience: their VP Finance, ahead of the FY27 planning round.
Nothing below has a slot left in it, and nothing below has our company as the subject of a
sentence.

````
════════════════════════════════════════════════════════════
FOR THE CHAMPION — their voice, their ask. To them alone, editable.
════════════════════════════════════════════════════════════

```text
Finance close programme — where we got to, and what I need for FY27

WHAT WE SET OUT TO DO

  We committed in the January plan to getting the month-end close under
  six working days by the December close, so the team stops losing the
  first week of every quarter to reconciliation.

WHAT MY TEAM DID

  Priya's team rebuilt the reconciliation step and moved 14 of the 22
  manual checks into the tool before any of the new reporting went live.
  Our FP&A team extracted and signed off both the November 2025 baseline
  and the June 2026 figure, so the numbers below are ours, not a vendor's.
  Rachel's group ran the Legal data-retention review in three weeks
  against a six-week estimate.

WHERE IT GOT TO

  We took 3.5 days out of the month-end close: 9.0 working days in
  November 2025, 5.5 in June 2026, against a target of 6.0.

  Finance seats in weekly use went from 4 to 22 of the 26 we hold.

WHAT DIDN'T LAND

  The September integration arrived six weeks late and cost us roughly
  120 hours of manual reconciliation across two closes. The cause was a
  schema change on their side that we were not told about. That is fixed:
  schema changes now come to Marcus a fortnight ahead, and Sam owns the
  integration end to end. Legal is not started — that is the ask below.

WHAT I'M ASKING FOR

  Keep the Finance licence line in the FY27 plan at its current level,
  and approve the Legal extension by 15 October so we can onboard the
  12 users before the Q1 close.

WHAT HAPPENS NEXT

  Dami Okoye sends the two saved report templates by 3 October, and the
  FY27 planning input in our format by 17 October. Ade Nwosu runs the
  Legal onboarding sessions, first one 14 November.

IF WE DON'T

  Legal stays on the manual process, which is where the two-day audit lag
  I raised in March comes from, and the December close goes back to
  needing the first week of January to clear.
```
````

Why it works: their team is the subject of every sentence in the credit block · one number,
in their unit, with the baseline and the target beside it · the miss is stated before the
number and carries an owner · the ask is a decision with a date, phrased the way their VP
grants things · the last block is a consequence in their units, not a threat in ours.

---

## 5. Pre-send checklist

- [ ] **C20** — the credit slot names something specific their team did, with their team as the
      subject. If it cannot, this page is not sent
- [ ] **C5** — the number in "where it got to" appears in A6 as customer-stated, with the
      speaker and the date. No customer-stated form means no number on this page
- [ ] **C19** — exactly one headline figure, and at most one unit metric beneath it
- [ ] **C29** — "what didn't land" appears above "what I'm asking for", and it is populated
      wherever a success-plan milestone was missed
- [ ] **C18** — any figure whose baseline was not agreed before the period started is either
      dropped from this page or stated as a measurement taken afterwards
- [ ] No sentence has our company, our product or "the platform" as its grammatical subject
- [ ] No health score, risk band, ARR at risk, forecast, save play or coverage language (**R18**)
- [ ] Every commitment carries a named person and a calendar date (**R19**)
- [ ] Their date format, their metric names, their team names — checked against A2 and A3
- [ ] No branding, footer, logo or template furniture of ours anywhere on the page
- [ ] Sent to the champion **alone**, in an editable format, with one line saying they should
      change anything that does not sound like them
