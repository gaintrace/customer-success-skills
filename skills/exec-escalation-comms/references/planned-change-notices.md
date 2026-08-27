# Planned Change Notices

> Four complete, send-ready notes for the things that are not broken. A price increase, a
> product retirement, a reduced support entitlement and a departing CSM are **announcements**,
> not failures, and almost every rule about them differs from the unplanned variants in
> `variant-library.md`.
>
> Three differences drive the rest:
>
> | | Unplanned failure | Planned change |
> | --- | --- | --- |
> | **Register** | Ownership — "that was our miss" | Declarative — announce the decision, do not ask for it (`C13`) |
> | **Apology** | One, attached to a number and a completed action | **None.** Apologising for a decision invites a negotiation about whether it should stand |
> | **The clock** | Severity sets it — hours | The notice period sets it — months, and it is gated per account on `renewal_date − notice_period_days` (`R1`) |
>
> **All names, accounts and figures are fictional.** Replace every value.
>
> **Every fenced block below is customer-facing.** When one is emitted it goes beneath the
> divider, verbatim, exactly as `../assets/escalation-note-template.md` specifies:
>
> ```
> ════════════════════════════════════════════════════════════
> CUSTOMER-FACING — copy the block below and send as written.
> Everything above this line is internal. Do not forward it.
> ════════════════════════════════════════════════════════════
> ```

**Contents** —
[1 · Price increase](#1--price-increase) ·
[2 · Product sunset / EOL](#2--product-sunset--eol) ·
[3 · Support tier change](#3--support-tier-change) ·
[4 · Departing CSM](#4--departing-csm) ·
[The notice clock](#the-notice-clock) ·
[What every planned notice refuses](#what-every-planned-notice-refuses)

---

## 1 · Price increase

**Sev** S4 · **Send** call the top decile on day −1, then the note · **From** the CSM to the
champion; a CCO or CFO letter to the economic buyer · **Carries the weight** S2 (their number)

**`C13` governs the register: announce the uplift, do not ask for it.** Any interrogative in the
price paragraph — "would you be open to", "how do you feel about" — fails the pre-send scan.
**`R1` governs the date:** the announcement lands before this account's opt-out deadline, not
merely before the renewal. Run `../scripts/update_clock.py` first; a negative margin moves the
effective date, never the notice. **Recipients:** champion **and** billing contact **and**
economic buyer — the payer must never learn a price change from an invoice.

```text
Subject: Pricing Change 1 March

Marcus,

Our list pricing goes up 7% on 1 March 2027. For Northwind that means $620,000 becomes
$663,400 at your 5 February renewal, and I wanted that number in front of you from me,
in writing, before it appears on a quote.

Your notice window opens on 7 November, so you have this 90 days before you have to do
anything with it.

What changed on our side this year: the audit-log export, the incremental sync that took
your nightly load from four hours to fifty minutes, and SOC 2 Type II. You use the first
two. The third matters to your procurement team rather than to you.

Two things I can do, and I would rather do them now than at T-30:

  - Phase it - 3.5% on 5 February 2027 and the balance on 5 February 2028.
  - Fix it - hold the current rate for three years on a multi-year term.

If you need to take this to Sarah Chen or to finance, tell me what they will need and I
will write it in their language rather than mine.

I am on +44 7700 900412 this week and next.

Jo Whitfield
```

**Most people get the opener wrong:** "I wanted to give you a heads up on some changes to our
packaging." The number belongs in sentence one. A cushion in front of a price increase reads as
embarrassment about the price, and embarrassment invites a negotiation.

---

## 2 · Product sunset / EOL

**Sev** S4 · **Send** call every account that uses the feature; email the rest · **From** product and CS jointly · **Weight** S2 (their exposure) and S5 (the migration)

Notice for a GA product: **12 months** is the enterprise-cloud norm — Google Cloud's published
deprecation policy commits to at least 12 months for GA services `[V, accessed 2026-08]`.
**Name the gap honestly:** a sunset notice claiming perfect parity is the fastest way to lose the
account, because the customer discovers otherwise during the migration you asked them to run.

```text
Subject: Legacy Export API Retirement

Ana,

We are retiring the v1 export API on 30 September 2027. That is twelve months' notice.

Your exposure: 14 of your workflows and 3 scheduled jobs call v1 today, averaging 41,000
calls a month. Doing nothing means those break on 30 September 2027. Your v2 traffic -
about 60% of your total - is unaffected.

The replacement is the v2 export endpoint, which covers about 90% of what you do on v1
today. The gap is the XML response format; v2 returns JSON only. I am not going to tell
you it is equivalent, because it is not yet. Our product team has XML on the v2 roadmap
and I do not have a date for it, so plan on converting rather than on waiting.

What we will do:

  - Ravi Menon, our delivery lead - a migration assessment naming every one of your 14
    workflows and the change each needs, at no cost, delivered by 15 October 2026.
  - Ravi - a sandbox with v2 and your data shape, available from 1 November 2026.
  - Me - a written confirmation six months out, on 30 March 2027, of what is still on
    v1 in your account, so nothing surprises either of us in September.

What I need from you: one name on your side by 17 October 2026 - whoever owns the
integrations - so Ravi has somebody to work with.

Jo Whitfield
+44 7700 900412
```

**Most people get wrong:** "v2 is a drop-in replacement." Almost never true, and they find out
mid-migration, on your timetable.

---

## 3 · Support tier change

**Sev** S4 · **Send** call every account using the tier heavily, then the note · **From** VP
Support and the CSM · **Carries the weight** S2

The trap is framing a takeaway as an improvement. Customers read "streamlined support
experience" correctly and instantly, and the framing costs more than the change does.

```text
Subject: Support Hours Change

Priya,

From 1 December our Premium tier moves from 24/7 phone coverage to 24/5, Monday to
Friday. Weekend phone support ends. This is a reduction, and I am not going to describe
it as anything else.

What it means for you specifically: you raised 43 tickets in the last six months and 4
of them came in at a weekend, all on Saturdays, all P2. Under the new tier those four
would have been email-only until Monday 08:00 - an average wait of 31 hours against the
2 hours you got.

Two options, and I would rather put both in front of you now than have you find the
change in a renewal quote:

  - Weekend Critical add-on - weekend phone coverage for P1 only, $18,000 a year. Your
    four tickets were P2, so this would not have covered them; I would rather say that
    than sell it to you.
  - Named escalation contact - our weekend on-call manager's direct line for genuine
    production-down situations. No charge, and it is what I would take here.

Your renewal is 14 March and your notice window opens 14 January, so this is in front of
you before you decide anything.

Elena Vasquez, our VP Support, is on Thursday's call if you want to push on this with
someone who can change it.

Jo Whitfield
+44 7700 900412
```

**Why it works:** it sizes the change from their own ticket history, and it talks them out of the
paid option that would not have helped them. That credibility is worth more than the add-on.

---

## 4 · Departing CSM

**Sev** S4 · **Send** call, from **the departing person**, before their last working day ·
**Carries the weight** S5 (the handover)

`R3` in mirror image: when the departure is **ours**, the note goes out before the last day, from
the person leaving, with the successor named and a date already in the calendar. Announced
afterwards by a manager, it reads as a departure the customer was not trusted with. **No
apology** — a normal event framed as a failure invites the customer to treat it as one.

```text
Subject: Handover to Ana Silveira

Dana,

I am leaving the company on 19 September, and Ana Silveira takes over your account from
15 September. I wanted you to hear it from me with two weeks to spare rather than from a
calendar invite.

Ana and I have three sessions booked before the 19th to go through the account. What
she will already know when you meet her:

  - The reconciliation job history, including the August incident and the lock-check
    gate that shipped on 2 September.
  - That your close week is the first five working days of the month, and that nothing
    ships into it.
  - The audit-log export commitment, its status, and that it is the one thing still
    outstanding from me to you.
  - Your February renewal, the 7 November notice date, and where pricing had got to.

Three things I have written down for her that are in no system: that Sarah Chen signs
but Marcus decides; that you have asked twice for the quarterly summary to arrive before
your board pack rather than after, and we have twice failed to do it; and that you would
rather have a short honest update than a long polished one.

Ana has put thirty minutes in your calendar for Wednesday 17 September so you meet her
while I am still here. Move it if it is wrong - she will work around your week.

It has been three years. The audit-log work happened because you pushed us on it.

Jo Whitfield
```

**Why it works:** the paragraph naming the two things we have repeatedly got wrong. In a handover
note that tells the customer the successor was told the truth — the only question they have.

---

## The notice clock

Two clocks run at once and **the shorter one governs**: the policy period for the change type,
and each account's opt-out deadline (`R1`). Run `../scripts/update_clock.py` over the account list
before choosing an announcement date — it returns days-of-notice given against required, plus
the per-account margin between the announcement and `renewal_date − notice_period_days`.

| Change | Notice | Source |
| --- | --- | --- |
| Price increase | **90 days minimum**, and before every affected account's opt-out deadline | AWS Marketplace requires sellers to give existing customers **90 days' notice** of annual price changes, and a change applies to an auto-renewal only if made at least 90 days before it `[V, AWS Marketplace seller documentation, accessed 2026-08]` |
| Product sunset / EOL (GA) | **12 months** | Google Cloud's published deprecation policy commits to at least 12 months for GA services; Google Distributed Cloud commits to a **minimum of one year's** notice of a breaking change `[V, Google Cloud documentation, accessed 2026-08]` |
| API / version deprecation | 6–12 months, with a hard cutoff date stated at announcement | `[P]` |
| Support tier or SLA change | 60–90 days | `[P]` |
| Feature moved between plan tiers | 90 days, and **only to accounts that use it** | `[P]`. Mass-mailing a takeaway to customers who do not use the feature manufactures churn risk from nothing |
| Departing CSM | Before the last working day; 10 business days is the practical floor | `[P]`. Announced afterwards it reads as a departure the customer was not trusted with |

**A negative margin moves the effective date, never the notice.** Shortening notice to hit a
revenue date converts a commercial decision into a trust event, and the trust event costs more
than the quarter does.

**Recipients are tiered, not broadcast.** Top decile, any account inside its opt-out window, any
reference customer and any account with a live escalation get a call on **day −1** — never the
same hour as the list send (`C26`). Anything touching money reaches the champion **and** the
billing contact **and** the economic buyer; the payer must never learn a price change from an
invoice.

---

## What every planned notice refuses

| Refusal | Rule |
| --- | --- |
| No apology for the decision — it invites a negotiation about whether the decision stands | `C13` |
| No interrogative in the price paragraph: no "would you be open to", no "how do you feel about" | `C13` |
| No framing of a takeaway as an improvement — "streamlined support experience" is read correctly and instantly | |
| No claim of parity a migration will disprove; name the gap before they find it | |
| No roadmap date for the gap, however much you want to soften the news | `R19` |
| No commercial ask attached — this note announces, it does not negotiate | `R11` |
| No health band, risk language, ARR at risk, forecast or save-play language | `R18` |
| No send after the account's opt-out window has closed | `R1` |
| No unfilled placeholder inside any copy block | `../../cs-context/references/customer-voice.md` |
| No exclamation marks, no superlatives, no emoji | `C27` |

**When a planned change collides with a live incident**, send them on separate days and send the
incident note first. Bundling lets the customer discount both, and it makes the announcement
read as an apology — exactly what `R11` exists to prevent.
