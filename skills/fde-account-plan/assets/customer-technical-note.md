# Customer-Facing Technical Notes

> The four notes a forward-deployed engineer actually sends, written to the standard in
> `../../cs-context/references/customer-voice.md`. Each sits inside a fenced block, formatted for
> an email client rather than a markdown renderer, with no unfilled placeholders.
>
> **Before sending anything here, run the leak scan.** These notes carry dates, asks and decisions.
> They never carry carrying cost, interest rate, disposition words ("retire", "productise"), risk
> bands, bus factor, renewal exposure, or any assessment of a named person (`R18`).

**Register.** Engineers discount marketing language instantly and permanently. Precise, specific,
version numbers and dates, no adjectives. Warmth here is accuracy: proving you know their system
better than they expected is the whole effect.

---

## 1. The dependency ask — dates that need an owner on their side

Use after the plan is written, when obligations mature before the opt-out deadline and the work is
theirs. One ask, dated, easy to answer.

════════════════════════════════════════════════════════════
CUSTOMER-FACING — copy the block below and send as written.
Everything above this line is internal. Do not forward it.
════════════════════════════════════════════════════════════

```text
Subject: Northwind deployment — three dates that need an owner your side

Hi Marcus,

Three things on the deployment have dates attached. Two need someone on
your side, and one is mine.

  • The service account the warehouse sync uses has a credential that stops
    working on 14 October. Rotating it takes about twenty minutes and needs
    admin on the Snowflake role. Give me a name and I'll send them the exact
    steps, including the order — new secret first, old one removed after, so
    there's no gap.

  • You're on release 4.2. Support for 4.x ends 31 January. Moving to 5.1
    needs a two-hour window with reporting paused, and I'd rather do it in
    November than in January. Any Thursday evening that month works my end.

  • Mine: the mutual TLS certificate on the carrier EDI endpoint expires on
    30 September. I've moved it onto automated renewal, so there's nothing
    for you to do, but you'll see a certificate change in your logs that
    evening and I didn't want it to be a surprise.

Can you give me a name for the credential rotation by Friday? The upgrade
window can wait until we talk on the 9th.

Thanks,
Jo
```

---

## 2. Refusing a custom build

Decision first, reason in their interest second, nearest alternative third. Never soften it with a
roadmap date nobody has agreed (`R19`), and never send it in the same conversation as an apology or
an ask (`R11`).

════════════════════════════════════════════════════════════
CUSTOMER-FACING — copy the block below and send as written.
Everything above this line is internal. Do not forward it.
════════════════════════════════════════════════════════════

```text
Subject: The bulk-approve endpoint — what we can and can't do

Hi Priya,

On the bulk-approve API: we're not going to build it as a one-off for
Northwind, and I want to give you the real reason rather than a soft no.

A custom endpoint would sit outside the upgrade path. Every release we ship,
someone has to check whether it still behaves, and the first time either
side changes a schema it breaks quietly — usually at month-end, which is
exactly when you'd notice. You'd be carrying that, not us.

What we can do today gets you the same result. The batch endpoint takes 500
records per call, so your 1,840 pending approvals are four calls rather than
one. I've written it up with sample requests and a script your team can run
as-is — attached. On the volumes you showed me last week that's under two
minutes end to end.

If the four-call shape is genuinely a problem rather than an annoyance, tell
me why and I'll take it to our product team as a requirement rather than as
a favour. That's a slower path and I can't promise an outcome, but it's the
honest one.

Does the attached script cover what you need?

Jo
```

---

## 3. The upgrade window request

Sent once the version state has a date on it. Specific about what is unavailable, who is needed and
for how long — never "some downtime may be required".

════════════════════════════════════════════════════════════
CUSTOMER-FACING — copy the block below and send as written.
Everything above this line is internal. Do not forward it.
════════════════════════════════════════════════════════════

```text
Subject: Booking the 5.1 upgrade — two hours, three options

Hi Marcus,

Support for release 4.x ends on 31 January, so I'd like the upgrade done in
November and settled well before your year-end.

What it involves:

  • Two hours, reporting paused. Ingest keeps running and queues, so nothing
    is lost — the depot dashboards are blank until it finishes.
  • From you: someone with admin on the identity provider available on a
    call for the first twenty minutes, in case the SAML app needs
    re-consent. Realistically that's Sam for half an hour.
  • From me: everything else, plus a rehearsal in your staging environment
    the week before so we're not discovering anything on the night.
  • If it goes wrong we roll back to 4.2 in about twenty-five minutes. I've
    run that rollback in staging, so it's a tested number rather than an
    estimate.

Three windows that work my end:

  Thursday 6 November, 19:00
  Thursday 13 November, 19:00
  Thursday 20 November, 19:00

I've deliberately kept all of them clear of your month-end. Which one?

One thing to flag: the reconciliation connector we built during the pilot
needs a small change to work on 5.1. That's a day of my time and it's in the
plan either way — mentioning it so the timeline makes sense to you.

Jo
```

---

## 4. Confirming the technical plan after a review

The follow-up after a technical account review. Decisions, owners, dates — and the open question
named rather than smoothed over.

════════════════════════════════════════════════════════════
CUSTOMER-FACING — copy the block below and send as written.
Everything above this line is internal. Do not forward it.
════════════════════════════════════════════════════════════

```text
Subject: Northwind technical review — what we agreed, and the one open item

Hi Marcus, Priya,

Thanks for the two hours. Writing down what we agreed so we're working from
the same list.

Decided:

  • 5.1 upgrade on Thursday 13 November, 19:00. Sam available for the first
    twenty minutes.
  • The account-code mapping moves onto the standard mapping table before
    the upgrade, so it stops needing a manual edit every time your GL
    changes. A day of my time, an hour of Priya's.
  • The SFTP drop-folder path gets switched off on 30 September. Nothing has
    used it since the API path went live in May 2025, and I'll disable it
    two weeks before deleting anything, so there's a way back.

Who owes what:

  • Marcus — a name for the warehouse credential rotation, by Friday
  • Priya — twenty minutes to confirm the GL account codes, week of 8 Sept
  • Me — the mapping migration plan, Thursday 4 September

Still open: whether the depot throughput numbers should come from your
warehouse or from us. You wanted to check with Ravi how his team uses them
before we decide. No rush before the 9th.

Growth note, so it isn't a surprise later: your carrier event volume is up
about 60% since March. At that rate you reach the top of what we've load
tested around March next year. Nothing to do today — I'd rather raise it now
than during a peak week.

Next session: Thursday 9 October, 14:00.

Jo
```

---

## What each note deliberately does not say

| Internal fact | Why it stays internal | What crossed instead |
| --- | --- | --- |
| The ledger carries $88k/yr, 9% of ARR | Cost-to-serve is our commercial position, not theirs (`R18`) | "A day of my time and an hour of Priya's" |
| The mapping file is a `Migrate` disposition | Disposition language is internal vocabulary | "So it stops needing a manual edit" |
| Bus factor 1 on their side is Marcus | An assessment of a named person never crosses | The ask for a named second person, framed as convenience |
| The upgrade is a renewal-critical fact | Renewal framing turns an engineering conversation into a commercial one | "Settled well before your year-end" |
| Scale headroom is a High-band risk row | Risk bands never cross | "You reach the top of what we've load tested around March" |
