# Customer Integration Notes

> The five notes an integration review actually produces, written to the standard in
> `../../cs-context/references/customer-voice.md`. Each sits inside a fenced block, formatted for an
> email client rather than a markdown renderer, with **no unfilled placeholders**.
>
> **Run the leak scan before sending anything here.** These notes carry counts, dates and asks.
> They never carry a severity band, a criticality score, priority arithmetic, ARR, the renewal read,
> or any observation about who on the customer's side noticed — or did not (`R18`).

**Register.** The reader is an engineer or an admin. Precise, specific, IDs and dates, no
adjectives. Warmth here is accuracy: proving you know their system better than they expected is the
whole effect. Marketing language is discounted instantly and permanently by this audience.

**The four rules these notes are built on**

| Rule | In practice |
| --- | --- |
| **Lead with the loss (`R20`, `C29`)** | The count and the window are in the first two sentences. Never after the explanation |
| **Apologise once (`R20`, `C28`)** | One apology, then the fix. A second asks the customer to absolve you |
| **Never write "no data was affected" unless you reconciled** | Write what you measured, with the window. `UNKNOWN` is honest; a reassurance you cannot support is not |
| **Bad news goes by voice first (`C26`)** | For anything above a few hundred records or touching money, call, then send the note as the written follow-up — early in the week, early in the day |

---

## 1. The disclosure — records lost, counted, backfilled

Send after the count is verified against their own numbers, never before. Lead with what was
missing and over what window; the cause comes second because it matters less to them than the size.

════════════════════════════════════════════════════════════
CUSTOMER-FACING — copy the block below and send as written.
Everything above this line is internal. Do not forward it.
════════════════════════════════════════════════════════════

```text
Subject: Carrier status events — 1,806 missed between 29 July and 11 August, now replayed

Hi Priya,

Between 29 July and 11 August, 1,806 of the 42,190 carrier status events
sent to us were accepted and then never written. For those fourteen days
the depot dashboard showed 1,806 shipments as still in transit after they
had actually been delivered. Sorry — we should have caught this in the
first 48 hours.

What happened: our receiver confirmed each event before saving it. When
carrier volume spiked on 29 July the internal queue filled, and events that
arrived while it was full were confirmed and dropped. Your carrier's log
showed 100% delivery success throughout, because from their side delivery
had succeeded.

What has been done:

  • All 1,806 events replayed from the carrier's own delivery log and
    written. I checked the replayed set against your carrier reconciliation
    report for the same fortnight — 42,190 events both ends, matched on
    event ID, no duplicates.
  • The receiver now saves the event before confirming it, so a full queue
    slows deliveries instead of losing them.
  • A nightly check compares events received against events written and
    stops the job if the two differ by one. It has run clean since 19
    August.

The affected shipments are listed in the attached CSV by consignment
number, in case anything downstream needs re-running your end.

One thing worth deciding together: your carrier keeps replayable delivery
history for 30 days. If a gap like this ever runs longer than that, the
events are gone rather than delayed. Twenty minutes to talk through how far
back you would want us to be able to rebuild?

Jo
```

---

## 2. The scheduled migration that lost nothing

The second worked example. A completed cutover with a clean reconciliation. The temptation is to
say "no data was lost"; write the measurement instead, because a customer who has been burned once
reads an unsupported reassurance as the same thing twice.

════════════════════════════════════════════════════════════
CUSTOMER-FACING — copy the block below and send as written.
Everything above this line is internal. Do not forward it.
════════════════════════════════════════════════════════════

```text
Subject: Opportunity sync moved to the new Salesforce API — counts matched both sides

Hi Marcus,

The opportunity sync moved to the new Salesforce API version on Thursday
evening, in the 90-minute window we booked. It finished 22 minutes early
and there is nothing for you to do.

What I checked, rather than assumed:

  • Both the old and the new path wrote in parallel for seven days before
    the switch. Over that week, 29,411 opportunities came through each
    path — the same 29,411, matched on record ID, no gaps and no
    duplicates.
  • Amount, close date and stage were compared field by field on all
    29,411. Every value matched, including the two-decimal amounts that
    used to round on the old path.
  • Since the switch, the nightly reconciliation has run seven times and
    the counts have closed each night: records sent equals records written.

Two changes you will notice:

  • The nightly load finishes around 03:40 instead of 04:11, so your 06:00
    reports have a wider margin than before.
  • Rejected records now appear in the sync log with the reason, instead of
    being counted only as a total. If a picklist value changes again, you
    will see which records it hit on the first morning.

The old API version stays available to us until 30 June next year, but the
old path is now off and I would rather not switch it back on unless
something surfaces. If anything looks wrong in this week's pipeline
numbers, tell me and I will reconcile that specific report against your
own count the same day.

Jo
```

---

## 3. The interim note — the count is not known yet

Sent when the customer has raised a discrepancy and the reconciliation is not finished. The
discipline: say what is known, what is not, what is being done, and the date the number arrives.
Never fill the gap with a reassurance.

════════════════════════════════════════════════════════════
CUSTOMER-FACING — copy the block below and send as written.
Everything above this line is internal. Do not forward it.
════════════════════════════════════════════════════════════

```text
Subject: The weekly revenue figure — what I know so far, and when I will have the number

Hi Priya,

You are right that the warehouse figure for week commencing 17 August is
lower than your finance number. I do not yet know by how many records, and
I would rather tell you that than give you a figure I cannot stand behind.

What I know now:

  • The hourly job ran all 168 times last week and reported success each
    time, so this is not a job that stopped.
  • The row counts leaving us and the row counts landing in Snowflake match
    for Monday to Wednesday. Thursday and Friday are where the gap opens.
  • Thursday 20 August is also the day a new required field appeared on
    your order object, which is the first thing I am checking.

What I am doing, and when:

  • Extracting the record IDs on both sides for 20 and 21 August and
    diffing them, so the answer is a list of specific records rather than
    a difference between two totals. That runs tonight.
  • You will have the count, the window and the cause from me by 16:00 on
    Thursday 3 September, whether or not the fix is ready by then.

If the finance number is being used for anything that closes before
Thursday, tell me now and I will prioritise the Friday range first.

Jo
```

---

## 4. Something changed on their side — asking without accusing

Every inference is phrased as a question. "You removed a permission" asserts something you inferred;
the version below asks, and it is the one that gets an answer the same day.

════════════════════════════════════════════════════════════
CUSTOMER-FACING — copy the block below and send as written.
Everything above this line is internal. Do not forward it.
════════════════════════════════════════════════════════════

```text
Subject: Two fields stopped arriving from Salesforce on 12 August — was that intentional?

Hi Marcus,

Since 12 August the opportunity sync has stopped receiving two fields it
used to get: Forecast_Category and Renewal_Owner__c. The records still
arrive, the sync still reports success, and those two columns are now empty
for everything created since that date — about 2,900 opportunities.

Salesforce does not raise an error when an integration user loses read
access to a field. It returns the record without the field, which is why
nothing flagged it and why I am asking rather than telling.

Two possibilities, and you will know which straight away:

  • A permission set or profile change on 12 August that removed those
    fields from the integration user. If so, restoring the read permission
    fixes it and I will re-extract the 2,900 records that came through
    without them.
  • A deliberate decision to stop sharing those fields. Equally fine — in
    that case I will remove the two columns from the pipeline view so
    nobody is looking at a blank field and wondering, and tell you which
    two reports change as a result.

Which of the two is it? If it is the first, twenty minutes with whoever
manages the integration user's permission set gets it back, and I have the
exact field names ready to send.

I have also added a check that compares the fields we expect against the
fields we receive on every run, so the next change like this shows up the
same morning rather than three weeks later.

Jo
```

---

## 5. Our own retirement, landing on them

Notice given, not announced. A migration guide, a named owner each side, a window outside their
freeze calendar, and a date that sits clear of their year-end.

════════════════════════════════════════════════════════════
CUSTOMER-FACING — copy the block below and send as written.
Everything above this line is internal. Do not forward it.
════════════════════════════════════════════════════════════

```text
Subject: We are retiring the v1 webhook payload on 31 March 2027 — what Northwind needs to do

Hi Marcus, Priya,

We are retiring the v1 webhook payload on 31 March 2027. Northwind uses it
for carrier status events, so this one lands on you, and I would rather
give you seven months than the three months the notice period requires.

What changes: v2 sends the same events with three additional fields and
one renamed field — carrier_ref becomes carrier_reference. Everything else
is identical, and both versions run in parallel until the retirement date,
so there is no cutover moment.

What it needs from you: one change to the field name in whatever consumes
the payload. On the code you showed me in June, that is a single line. I
have attached the migration guide with a side-by-side example and a test
endpoint you can point at today.

Owners, so this does not drift:

  • Mine — the test endpoint, the guide, and a check the week after you
    switch to confirm event counts match on both versions.
  • Yours — a name for whoever makes the change. Priya, is this Ravi's
    team or yours?

Timing: I would suggest February or March 2027, after your year-end and
with a month of margin before the retirement. I have deliberately kept it
away from your December peak, and there is no need to touch it before
Christmas.

Nothing breaks between now and then, and I will send one reminder in
January rather than a monthly nag.

Jo
```

---

## What these notes deliberately do not say

| Internal fact | Why it stays internal | What crossed instead |
| --- | --- | --- |
| The connector scored Red on partial failure, priority 43.2 | Bands and priority arithmetic never cross (`R18`, `R22`) | "1,806 of 42,190 events, between 29 July and 11 August" |
| $620k of ARR sits behind this workflow | Our commercial position, not theirs | Nothing. The count is the argument |
| The opt-out deadline is 7 November | Renewal framing turns an engineering conversation into a commercial one | "After your year-end, with a month of margin" |
| Their team never reported the outage — `T2`, feeding the renewal read | An observation about who noticed is internal, permanently (`R2`, `C21`) | The detector, stated as what we now do |
| The credential is held by a named individual, which is a bus-factor finding | An assessment of a named person never crosses | "The sync stops depending on any one person's account" |
| This account is on a save play / has an open risk record | Never, in any wording | Nothing |

---

## Pre-send checklist

- [ ] The count and the window are in the first two sentences, in the customer's units
- [ ] One apology, not two — and none at all where nothing was lost
- [ ] Every number is one the customer can verify in their own systems
- [ ] Every inference is a question, not a claim
- [ ] Nothing was reconciled "clean" that was not actually measured — `UNKNOWN` with a date is the honest alternative
- [ ] Every commitment has an internally agreed owner and a real date (`R19`)
- [ ] Vocabulary scan run: no risk, health, score, band, priority, forecast, ARR, renewal, save, tier, escalation language
- [ ] No assessment of any named person, including who did or did not notice
- [ ] Formatted for an email client — plain text, blank lines between paragraphs, no markdown headings or pipe tables
- [ ] No placeholders anywhere inside the fence; the block is send-ready as written
- [ ] For anything above a few hundred records or touching money or invoices: called first, sent second (`C26`)
