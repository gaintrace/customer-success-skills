# Variant Library — unplanned failures

> Five complete, send-ready notes for the things that go wrong without warning. Every one is
> filled — real names, numbers and dates, no placeholders — because a template with `[Name]` in
> it is a trap: the most common way an unedited draft reaches a customer is that it looked
> finished. **Planned changes** — price, EOL, tier, a departing CSM — are in
> `planned-change-notices.md`, because they are announcements rather than failures and almost
> every rule about them differs.
>
> **All names, accounts and figures are fictional.** Replace every value. What transfers is the
> shape: which section carries the weight, what the note refuses to say, and the sentence most
> people get wrong.
>
> The seven-section spine (`note-structures.md`) is identical across every variant in both
> files. **The variant changes what fills the slots, never which slots exist.**
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
[1 · Outage, cause unknown](#1--outage-cause-unknown-first-note) ·
[2 · Missed delivery date](#2--missed-delivery-date) ·
[3 · Broken verbal commitment](#3--broken-verbal-commitment) ·
[4 · Security incident](#4--security-incident-the-relationship-note) ·
[5 · We got it wrong](#5--we-got-it-wrong) ·
[What every variant refuses](#what-every-variant-refuses) ·
[Variant selector](#variant-selector)

---

## 1 · Outage, cause unknown (first note)

**Sev** S1 · **Send** phone first, note within 60 minutes of confirmed impact · **From** the
incident lead or a VP, CSM on the thread · **Carries the weight** S4 (timestamps) and S7

The hardest note to send and the one that pays for itself. S6 is **omitted** — prevention before
diagnosis is a guess wearing a control's clothing.

```text
Subject: Reconciliation Job Failures

Dana,

Your nightly reconciliation jobs did not run last night. They failed at 01:04 BST and
have not run since; they are still failing now.

Three jobs are confirmed affected — 4411, 4412 and 4413. I am checking whether a fourth
was, and I will have a confirmed count by 14:00 BST rather than give you a number I have
to correct. Your API traffic, the portal and the archive were not affected at any point.

We do not yet know the cause. I am not going to speculate, because being wrong about it
in writing costs you more than waiting until 14:00 does.

  01:22 - our on-call team was paged and confirmed the failure is ours, not a data
          problem on your side
  02:40 - we stopped the scheduled retries so they stop queueing behind each other
  03:15 - our database team took ownership; Sam Okafor is leading it

Nothing is needed from you, and please do not re-run the jobs by hand. The retries are
paused and a manual run would queue behind them. We will re-run them for you once the
cause is closed.

Next update at 12:30 BST, whether or not there is news.

Jo Whitfield
+44 7700 900412
```

**Why it works:** the unknown is bounded by a clock time, they are given an instruction so they
do not invent an expensive one, and nothing in it will have to be retracted.
**Most people get the third paragraph wrong.** "We believe this may be related to a caching
layer" feels more helpful and is the line that gets quoted back for a year.

---

## 2 · Missed delivery date

**Sev** S2 · **Send** phone **before the date passes**, note the same day · **From** the CSM, or
whoever set the date · **Carries the weight** S5 (the new date) and S6

The failure mode is timing, not wording: this note is sent the moment the slip is known, never
on the date itself. A date missed silently and explained afterwards costs a multiple of a date
moved eight days early.

```text
Subject: SSO Rollout Date

Marcus,

We are going to miss the 22 August date for the SSO rollout. The new date is 12
September, and I would rather tell you now than on the 22nd.

What that costs you: the 340 users you were migrating in the 25 August window stay on
username-and-password for three more weeks, and your security review moves out of the
August cycle. If that review date is the harder constraint, tell me and we will
re-sequence around it rather than around our build.

The cause is ours. We scoped the SAML attribute mapping against your test directory;
your production directory carries two attributes we did not test for. We found it in
staging on the 14th, which is later than we should have.

  14 Aug - the mismatch was found in staging
  15 Aug - we rebuilt the mapping against a copy of your production directory
  18 Aug - regression pass started; it is what sets the 12 September date

What we have committed to:

  - Ravi Menon, our delivery lead, owns 12 September. He confirmed it in writing and
    will tell me the day it moves if it moves.
  - Me - a written re-plan with the migration windows, by Thursday 21 August.
  - Me - confirmation on Friday 5 September that the regression pass is clean, so you
    get a week's warning if it is not.

What changes: we now build the attribute mapping against a copy of the production
directory on every deployment. That is what would have caught this in July.

I will update you on Friday 5 September whether or not there is news.

Ana Silveira
+1 415 555 0148
```

**The sentence most people get wrong:** "we are working to recover the date." Either you have
recovered it or you have not. Offering to try converts one bad conversation into two.

---

## 3 · Broken verbal commitment

**Sev** S2 · **Send** phone, from **the person who made the commitment** · **Carries the weight**
S3 (ownership) and S5

The only variant where naming an individual is correct — and the individual is **you**. The
whole note is the sentence "I said it and I did not deliver it," said once, without decoration.

```text
Subject: The Audit Log Export

Priya,

On our call on 3 July I told you we would have the audit-log export to you by the end of
August. We will not, and I should have told you three weeks ago when I knew.

What that means for you: the SOC 2 evidence pack for your November audit has a gap where
the export was going to sit. The closest thing we can give you now is a raw event dump
in JSON for the same period - it satisfies the retention requirement but not the
readable format your auditor asked for.

That was my commitment and I did not keep it. I made it before checking with the
engineering owner, which is the mistake.

What I can commit to now, having checked:

  - Me - the raw JSON dump for the 12-month period, by Friday 5 September. That one is
    mine to give and it will be there.
  - Me - a written answer from our product team on whether the formatted export is being
    built, by Thursday 11 September. That answer may be no, and if it is no I will tell
    you it is no rather than leave it open.

I am not going to give you a date for the formatted export today, because I do not own
that date and giving you a second one I cannot keep would be worse than not having one.

Ravi Menon
+44 7700 900318
```

**Why it works:** it names the promise, dates it, and admits the lateness of the disclosure —
the second failure, and the one the customer noticed. Then it refuses to repeat the mistake in
the same note. **Most people get wrong:** "we should be able to get you something by end of
September" — ungated, unowned, and it makes the third conversation worse than the first two.

---

## 4 · Security incident (the relationship note)

**Sev** S1 · **Send** per legal and security direction · **From** per legal · **Carries the
weight** S7

**This skill does not draft the notification.** Legal and security own that wording — it is a
regulated instrument with statutory content requirements. What follows is the **relationship
note that sits beside it**: human to human, who is holding this, when they hear from us next.

The clocks (`cadence-and-severity.md` §10): GDPR Art. 33, **72 hours** to the supervisory
authority from awareness, phased reporting permitted; Art. 34, affected individuals without
undue delay where risk is high; SEC Item 1.05, **four business days** from a materiality
determination for US registrants `[L]`. **Your contract is frequently shorter than all three.**

```text
Subject: Security Incident - Your Account

Marcus,

You will have received the formal notification from our security team at 09:00 this
morning. This note is from me, so you have a person rather than a process.

What I can tell you that the notification does not: I have been in the incident room
since 06:40, our CISO Elena Vasquez is running it, and your account is confirmed
in-scope rather than possibly in-scope. That is why you were in the first wave.

I am not going to characterise the cause. Our security team has not confirmed it, and
anything I say before they do is a guess about your data.

What is happening now:

  06:40 - the affected credentials were revoked across all tenants
  07:15 - your workspace was isolated from the affected service path
  08:30 - forensic imaging started; your account is in the first tranche

What I have committed to:

  - Elena Vasquez, our CISO - scope confirmation for your account specifically, by
    17:00 GMT today.
  - Me - a call with you and whoever you want in the room, at any hour you name in the
    next 48, including outside working hours.

Your legal and security teams will want the formal channel, which is staffed
continuously. Use me for everything else.

Next update from me at 17:00 GMT today, whether or not there is news.

Jo Whitfield
+44 7700 900412
```

**Three refusals:** say nothing about scope security has not confirmed (an undercount here is a
second notifiable event); do not characterise the cause; give the human line anyway — the formal
notification says what happened to their data, this one says who is holding it.

---

## 5 · We got it wrong

**Sev** S2 (S1 if they have acted on it) · **Send** phone, immediately, from whoever gave the
wrong information · **Carries the weight** S2 (the corrected number) and S3

The variant nobody wants to write: our advice, our number or our recommendation was wrong and
the customer acted on it. Speed is everything — the cost compounds every day they keep acting on
the wrong figure.

```text
Subject: Corrected Savings Figure

Sarah,

The annualised savings number I gave you on 12 June was wrong. I said $840,000. The
correct figure is $505,000, and I am sorry - that was my error and you have been
carrying it into your planning for eleven weeks.

What was wrong: I annualised the March-to-May run rate without adjusting for March
including your year-end reprocessing, which is a one-off spike. Taking March out gives
the $505,000. The workings are attached so your finance team can check them rather than
take my word for it a second time.

What that changes for you: the headcount case you built on the June number does not
carry at $505,000. I do not know what you have already committed internally, and that is
the part I most want to talk through.

What I have already done:

  12:20 today - pulled the figure from every deck we have shared with you, including
                the June QBR pack
  13:40 today - our finance team re-ran the model against 18 months rather than 3,
                which is what produced the $505,000

What I have committed to:

  - Me - the full workings, with the March adjustment isolated, by 09:00 tomorrow.
  - Me - a session with you and your finance lead at any time you name this week.
  - Elena Vasquez, our VP CS - joins that session, so you hear from someone above me
    that we know how this happened.

I am not going to argue that $505,000 is still a good number. It may well be. Today is
the correction, not the case.

Ana Silveira
+1 415 555 0148
```

**Why it works:** both numbers are in the first paragraph; the apology is one sentence attached
to the specific error; the methodology is handed over so they can verify rather than trust; and
the last paragraph refuses to defend the value case in the same note as the correction (`R11`),
which is what makes the correction believable. **Most people get wrong:** "we have refined our
methodology and issued revised figures" — a press release, and every reader hears it as one.

---

## What every variant refuses

Nine notes, nine contexts, one set of refusals. None of these appears in any block above, and
none may appear in a note this skill produces.

| Refusal | Rule |
| --- | --- |
| No individual is named as the cause — except the sender, in variant 3 | `note-structures.md` §2 |
| No blame of the customer, even where the facts would support it | |
| No speculation about a cause that is not confirmed | |
| No commitment that has not passed the five gates | `R19` |
| No roadmap date — variant 6 says plainly "I do not have a date for it" | `R19` |
| No credit, discount, term or renewal ask anywhere in an escalation note | `R11` |
| No health band, risk language, ARR at risk, forecast or save-play language | `R18` |
| No internal jargon — no "P1", no "sev-2", no "war room", no "escalated internally" | |
| No second apology, and no apology at all in variants 5, 6, 7 and 8 | `R20`, `C28` |
| No exclamation marks, no superlatives, no emoji | `C27` |
| No unfilled placeholder inside any copy block | `../../cs-context/references/customer-voice.md` |

---

## Variant selector

| What happened | Variant | Sev | First channel | Sender | Window |
| --- | --- | --- | --- | --- | --- |
| Service is down or degraded, cause unknown | 1 | S1 | Phone | Incident lead or VP | 60 min from confirmed impact |
| A date we set will be missed | 2 | S2 | Phone | CSM or the delivery lead | The moment the slip is known |
| Something we said verbally will not happen | 3 | S2 | Phone | The person who said it | Same day |
| Data or credentials exposed | 4 | S1 | Per legal | Per legal | Contract clause · GDPR 72h · SEC 4 business days |
| Our advice, number or recommendation was wrong | 5 | S2–S1 | Phone | Whoever gave it | Immediately |

Planned changes — price, EOL, support tier, a departing CSM — are in
`planned-change-notices.md`, with their own selector and notice-period table.

**When an unplanned failure collides with a planned change** — an outage during a price-increase
window, a missed date mid-sunset-migration — send them as **separate notes on separate days**,
unplanned first. Bundling bad news lets the customer discount both, and it makes the planned
change read as an apology, which is exactly what `R11` exists to prevent.
