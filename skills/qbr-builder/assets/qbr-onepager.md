# Leave-Behind and ≤24-Hour Recap — customer-facing

> Two of the three customer-facing artifacts. The third is the champion's internal one-pager,
> which is a different document for a different audience: `champion-onepager.md`.

> Two artifacts, both customer-facing, both governed by
> `../../cs-context/references/customer-voice.md`. Run the leak scan before either leaves
> your outbox: no health score, no risk band, no ARR at risk, no forecast category, no save
> play, no coverage tier, no assessment of a named person.
>
> The specification tables below use `<...>` slots. **Nothing with a slot in it gets sent.**
> The worked examples in the fenced blocks show what a filled, send-ready artifact looks
> like. If a value is genuinely unavailable, delete the sentence — never send `[Name]`.

---

## Part 1 — The one-page leave-behind

Four blocks, one page, no attachments. This is also the whole artifact when the
qualification gate says REPLACE and the review becomes an async value review.

| # | Block | Content | Sentence pattern |
| --- | --- | --- | --- |
| 1 | **Expected value** | The outcome they said they wanted, with its date and business reason | "You wanted to `<outcome>` by `<date>` so you could `<business reason>`" |
| 2 | **What didn't go well** | The miss, in their units, with what changed and who owns it | "We missed `<commitment>` by `<gap>`. It cost you `<their unit>`. `<Name>` owns it now" |
| 3 | **Value delivered** | Movement in **their** units, not our adoption metrics | "`<metric>` moved from `<baseline>` to `<current>` against a target of `<target>`" |
| 4 | **Proof** | Baseline → current → target, with the source of each and who agreed it | "Measured in `<their system>`, baseline agreed by `<name>` on `<date>`" |
| 5 | **Next steps** | The three goals, the one ask, owners and dates | "One ask: `<ask>`, from `<name>`, by `<date>`" |

**The order is fixed (C29, R20): block 2 comes before block 3.** Opening on the numbers after a
quarter that missed something tells the reader you did not notice. Where any success-plan
milestone was missed, block 2 is required and the page is not sent without it.

Rules: one page. Their metric before our metric. Every number verifiable in a system they own.
**One headline number (C19)** — supporting metrics go in the deck appendix, not here. Where the
headline number exists in the customer's own words, quote them with the date (**C5**). No dollar
figure unless the band is Evidenced or better, and where a figure appears the assumptions appear
with it.

````
════════════════════════════════════════════════════════════
CUSTOMER-FACING — copy the block below and send as written.
Everything above this line is internal. Do not forward it.
════════════════════════════════════════════════════════════

```text
Northwind Logistics — FY26 review summary
Prepared for J. Alvarez and P. Raman · data as of 24 Aug 2026

WHAT YOU SET OUT TO DO

  You wanted the month-end close under six working days by the December
  close, so Finance could stop losing the first week of every quarter to
  reconciliation.

WHAT DIDN'T GO WELL

  We missed the September integration date by six weeks. It cost your
  team roughly 120 hours of manual reconciliation across two closes. The
  cause was on our side — a schema change we did not flag. Since then
  every schema change goes to Marcus a fortnight ahead, and Sam owns the
  integration end to end. Legal has not started.

WHERE IT GOT TO

  3.5 days out of the month-end close: 9.0 working days in November 2025
  to 5.5 in June 2026, against a target of 6.0.

  Jamie put it this way on 14 August: "we took three and a half days out
  of the close, and about two of those we would not have got on our own."
  The number is from your own close calendar; your FP&A team extracted
  both the November 2025 baseline, agreed in the January plan, and the
  June 2026 figure.

  Supporting detail — Finance weekly seats 4 -> 22 of 26, permissions
  tickets 31 -> 12 a month — is in the appendix of the deck, along with
  the loaded-rate working, the 0.7 attribution factor and what we did not
  count.

WHAT WE AGREED FOR NEXT QUARTER

  • Finance to 22 of 26 weekly seats, held four weeks
    You: P. Raman   Us: D. Okoye   By 28 Nov
    Needs: your IT provisioning the Finance SSO group by 19 Sept

  • December close at 5.5 days or better
    You: J. Alvarez   Us: D. Okoye   By 31 Dec
    Needs: two saved report templates from us by 3 Oct

  • Legal onboarded — 12 users through their first workflow
    You: R. Whitfield   Us: A. Nwosu   By 14 Nov
    Needs: Legal's data-retention review closed by 10 Oct

  One ask from us: twenty minutes with your VP Finance before the FY27
  planning round, so the plan is written in your terms rather than ours.
  J. Alvarez is setting it up for the week of 20 October.

Next review: Thursday 15 January, 2pm.
```
````

---

## Part 2 — The ≤24-hour recap email

Sent within 24 business hours of the review, to everyone who attended — including the silent
attendees — and to anyone named as an owner. Not a forward of an internal thread; a new
email.

| Slot | Rule |
| --- | --- |
| **Subject** | The account plus the single decision made. Not "QBR recap" |
| **Opening line** | The most useful thing that came out of the meeting. Never thanks, never "great to see you" |
| **The miss** | Before the agreed list and before any number (**C29**). What it cost them in their units, what changed, who owns it. Never paired with a "but", never with a commercial ask (**R11**) |
| **What we agreed** | Only things that are settled now and were open before. Never manufacture a decision |
| **Who owes what** | A named human and a calendar date in every row. Never "the team", never "next week" |
| **Still open** | The questions asked and not answered, phrased neutrally |
| **Next session** | The date agreed in the room, or two concrete options |
| **Attached** | The leave-behind. Not the deck, unless they asked for it |

**Grade the commitments before writing.** Only rungs 4 and 5 of the commitment ladder go in
as agreed (`../references/qbr-facilitation.md` §5). Anything softer either gets converted by
asking one question, or is written as an open item — never promoted silently into the recap.

````
════════════════════════════════════════════════════════════
CUSTOMER-FACING — copy the block below and send as written.
Everything above this line is internal. Do not forward it.
════════════════════════════════════════════════════════════

```text
Subject: Northwind FY26 review — Legal rollout agreed, three goals, one ask

Hi Jamie, Priya, Rachel,

The decision we came for: Legal joins the rollout this quarter, with
Rachel owning it on your side. That was the one open question and it is
now closed.

On the September miss: six weeks late cost your team around 120 hours
across two closes. Sam owns the integration end to end now, and you will
get a schema-change note before anything moves.

Agreed today:

  • Legal onboarded — 12 users through their first workflow by 14 Nov.
    Rachel owns it; Ade runs the sessions.
  • Finance to 22 of 26 weekly seats, held four weeks, by 28 Nov.
    Priya owns it; needs your IT to provision the SSO group by 19 Sept.
  • December close at 5.5 working days or better.
    Jamie owns it; we owe you two report templates by 3 Oct.

What we owe you:

  • Two saved report templates — Dami, by 3 Oct
  • Schema-change notice a fortnight ahead, every time — Sam, standing
  • The FY27 planning input in your format — Dami, by 17 Oct

Still open:

  • Whether the audit-log export is in scope for Q1. Jamie was going to
    check with Ravi — no rush before the 15th.

One ask: twenty minutes with your VP Finance before FY27 planning, so
the plan is written in your terms. Jamie is setting it up for the week
of 20 October.

Next review: Thursday 15 January, 2pm. Summary page attached.

Thanks — the close-week timing was tight and you made it work.

Dami
```
````

---

## Pre-send checklist

- [ ] The first line is specific to this account and contains no filler
- [ ] Nothing from the banned phrasebook appears (`customer-voice.md` Part 1)
- [ ] Every number is one they can verify in a system they own, or one they gave us
- [ ] Every commitment has a named human and a calendar date
- [ ] Every inference is phrased as a question, not a claim
- [ ] No health score, risk band, ARR at risk, forecast, save play, tier or coverage language
- [ ] No assessment of any named person, on either side
- [ ] Formatted for an email client: plain text, blank lines between paragraphs, `•` bullets,
      no markdown headings, no pipe tables, no `**bold**`
- [ ] Every `<slot>` filled or its sentence deleted — no placeholders survive
- [ ] The miss appears before the numbers, and is present wherever a milestone was missed (**C29**)
- [ ] One headline number only; supporting metrics are in the deck appendix (**C19**)
- [ ] Where a customer-stated form of the number exists, it is quoted with the speaker and date (**C5**)
- [ ] The champion's internal one-pager went out too, to the champion alone (`champion-onepager.md`)
- [ ] Recipient line checked last, deliberately
