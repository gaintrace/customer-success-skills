# Note Structures — the seven sections, and the four notes that follow

> Read this **every time a note is drafted.** `../SKILL.md` Step 7 names the seven-section spine;
> this file is the anatomy under each section — what fills the slot, which field supplies it,
> the sentence that proves it, and the test that says it has failed. It then covers the four
> notes the spine produces — the **first note under uncertainty**, the **update**, the **closure
> note**, the **written review** — plus the **prevention receipt** nobody remembers.
>
> Evidence labels are load-bearing: `[M]` measured · `[V]` vendor · `[P]` practitioner ·
> `[A]` academic · `[L]` legal or regulatory primary text. Rules `R1`–`R24` live in
> `../../cs-context/references/operating-rules.md`; craft codes `C1`–`C32` in
> `../../cs-context/references/practitioner-craft.md`.

**Contents** — [1. Why seven, why this order](#1-why-seven-and-why-this-order) ·
[2. Section anatomy](#2-section-anatomy) · [3. First note under uncertainty](#3-the-first-note-under-uncertainty) ·
[4. The update](#4-the-update--the-heartbeat) · [5. Closure note](#5-the-closure-note) ·
[6. Written review](#6-the-written-review) · [7. Prevention receipt](#7-the-prevention-receipt) ·
[8. Subject lines, length, layout](#8-subject-lines-length-and-layout) ·
[9. Pre-emit check](#9-the-pre-emit-check)

---

## 1. Why seven, and why this order

The order is not stylistic. It is the order in which a **forwarded reader with no context**
absorbs the event: what happened → what it cost me → why → what you did → what you will do →
whether it recurs → when I hear from you again. Each re-ordering fails a different reader.

| Re-ordering | The reader it breaks, and how |
| --- | --- |
| Context or a greeting above S1 | Their CIO, reading two lines on a phone, forwards it to procurement asking "is this the outage?" |
| Root cause above impact | Their ops lead argues architecture instead of checking their own exposure |
| Prevention above actions taken | Their exec reads a promise where evidence should be, and discounts the rest |
| Next-update time moved to the footer | Everyone escalates over your head, because they cannot see when you will speak again |
| S4 merged with S5 | Their programme manager banks a commitment as delivered, and finds out at the worst moment |

This is the **BLUF** discipline — conclusion and required action in the first sentence, not at
the end of a build-up `[P, US Army memorandum standard (Bottom Line Up Front)]` — and it is
`R20 · Bad News First, Once` and `C29 · Lead with the miss` in one shape. The spine is identical
for an outage, a missed date, a price rise and an EOL: **the variant changes what fills the
slots, never which slots exist.** Nine filled versions: `variant-library.md` (five unplanned
failures) and `planned-change-notices.md` (four announced changes).

---

## 2. Section anatomy

### S1 · Situation

**The job:** give a stranger the whole event in one sentence, so nobody has to ask what this is
about. Four slots: an **active verb** with us as the actor; the **capability in their words**,
not our service name (`events.event_name`, their own ticket text); the **window** in their
timezone (`customer_impact_confirmed_at` → `resolved_at`); and one clause **bounding the scope**
(`units_affected`). **One sentence, no greeting above it**, twenty-five words the working
ceiling — past that, a second fact has crept in that belongs in S2.

```text
Your nightly reconciliation job failed on three consecutive runs between 27 and 29
August, and no other part of your account was affected.
```

**Failed when:** it opens with context, a greeting, an apology or a defence, or the reader must
reach the second paragraph to learn what happened.

### S2 · Impact, quantified

**The job:** remove the customer's need to compute their own exposure, and prove you did the
work of finding out. Fixed order: **their units** (jobs, claims, tenants, orders — never uptime %, never an SLA
percentage) → **their hours**, with the arithmetic visible (`../scripts/update_clock.py` prints it)
→ **money**, only where they can verify the rate and rounded to two significant figures →
**the explicit boundary**, what was *not* affected, which is the most-skipped line in the note.

`C3` governs the last line: **the number is the final sentence of its paragraph, unsoftened.** No
"we appreciate this is frustrating" after it — a hedge after a number negotiates against you.

```text
1,840 claims could not be filed on the 28th. 61 of them needed manual rework once the
job was re-run, which we estimate at 22 hours of your team's time at the two-person
staffing you described in June. Your API traffic, the portal and the March–July
archives were not affected at any point.
```

**Coverage gate.** Below 60% coverage across the seven families (`R23`) **no blast-radius figure
appears at all**, and the replacement is not silence:

```text
Three of your jobs failed. I am still confirming whether a fourth did, and I will have
a confirmed count by 14:00 today. I would rather give you that number once.
```

**Failed when:** the number is in our units; the money figure has no arithmetic; a total is
stated from partial data; or the boundary clause is missing, which reads as "everything".

### S3 · Root cause

**The job:** buy back credibility — a vendor that can name its own cause can be believed about
the fix. Two legal forms only: the known cause in the **active voice with "we" as the actor**, or
the **honest unknown with the time you will know.** Phrasebook and passive-voice tests:
`accountability-language.md` §2–§3.

```text
A schema migration ran against the reporting database without a lock check. That was
our change and our miss.
```

**Failed when:** passive voice hides the actor ("an issue occurred", "the migration was
executed"); an individual is named on either side; or speculation is offered as fact. That
passive form is what Safire called the *passive-evasive* and what political analyst William
Schneider named the **past exonerative tense** — it admits fault while deleting the party
responsible `[P, Safire, *Safire's Political Dictionary*; term coined by W. Schneider]`.

### S4 · Actions taken, with timestamps

**The job:** convert "we are on it" into evidence. **The timestamps are the whole point.** Line
shape is `<HH:MM their tz> — <completed past-tense verb> <object>`, three to five lines; six
means the incident is being narrated rather than reported.

**Failed when:** any line is undated, or any verb is progressive ("we are investigating", "we
have been working to"). Progressive verbs belong in S7, attached to a clock time.

### S5 · Actions committed, owner + date

**The job:** the only part they will check later. Every line carries **one named human, one
calendar date, one observable outcome**, and a line that failed any of the five gates in
`../SKILL.md` Step 4 is **removed, not softened**, its removal printed above the divider (`R19`).

What replaces a failed line: **no named owner** → nothing, the sentence is deleted ·
**owner has not agreed the date** → a decision date you own ("I will have an answer from our
platform lead by Thursday, including if the answer is no") · **outside their authority** →
nothing, until their manager approves it, escalated internally *before* sending ·
**a roadmap or release-train date** → a decision date, or a clear no with the nearest
alternative · **commercial content** → nothing; it routes to `renewal-negotiation` (`R11`).

```text
By Tue 2 Sep, Sam Okafor (our VP Engineering) has the lock-check validation in the
deploy pipeline; he has confirmed that date in writing.
By Fri 5 Sep, I will have an answer from our platform team on the retry backstop,
including if the answer is no.
```

**Failed when:** it contains "the team", "engineering", "shortly", "in the coming weeks", or
anything that failed a gate.

### S6 · Prevention

**The job:** answer the question the executive is actually asking — *does this recur?* It fixes
**the class of failure**, not this instance. "We re-ran your three jobs" is S4. "No migration
reaches a production database without a lock check, enforced in the pipeline rather than in a
runbook" is S6.

| Prevention that counts | Prevention that does not |
| --- | --- |
| A control enforced by a system | A control enforced by remembering |
| A test that fails the build | A checklist item added |
| Something the customer can observe — an alert they receive, a status-page component | An internal process change they can never verify |

**Failed when:** it restates the fix, or it is a promise with no receipt date. Every S6 line
gets a row in the prevention register with a **receipt due** date (§7).

### S7 · Next update, exact time

**The job:** the single line that decides whether they escalate over your head.

```text
Next update at 16:00 BST today, whether or not there is news.
```

| Required | Banned |
| --- | --- |
| An exact clock time | "shortly", "as soon as we know more", "later today" |
| Their timezone, named | Our timezone, or none |
| The "whether or not there is news" clause | An implied update conditional on progress |
| On a closure note: the date the written review lands | Nothing at all |

**Failed when:** it is missing, vague, or — worst — stated and then missed. A missed
self-imposed update is a second incident, and it is the one they remember.

---

## 3. The first note under uncertainty

**The highest-value note in this skill, and the one most often skipped.** It goes out inside the
severity window (`cadence-and-severity.md` §2) with the cause explicitly unknown, because their
exec is already being asked what happened and the only open question is whether the answer comes
from you or from a status page.

Two published practices converge on the same instruction: communicate early, communicate often,
and own the problem rather than describe it `[P, Atlassian Statuspage incident-communication
guidance, accessed 2026-08]`; and post on the stated cadence even when the content is "no new
information", with the next update time in every message `[P, incident.io incident-communication
best practices, accessed 2026-08]`. The uncertainty note keeps all seven sections; S3 and S5
change shape:

S1, S4 and S7 are unchanged — the timestamps carry the whole weight here. S2 gives what is
confirmed plus what is still being counted and when the count lands. S3 is the refusal to
speculate, with the time you will know. S5 is usually one line, and it is a **decision** date,
not a fix date. **S6 is omitted**: prevention offered before the cause is known is a guess
dressed as a control.

```text
Subject: Reconciliation job failures — Meridian Health

Dana,

Your nightly reconciliation job has failed on its last two runs, starting 03:10 BST on
28 August, and it is still failing now.

Three jobs are confirmed affected. I am checking whether a fourth was, and I will have
a confirmed count by 14:00 BST today rather than give you a number I have to correct.

We do not yet know the cause, and I am not going to speculate — being wrong about it in
writing costs you more than waiting two hours does.

09:41 — we confirmed the failure is ours, not a data problem on your side
10:05 — we stopped the scheduled retries so they stop consuming your queue
10:30 — our database team took ownership; Sam Okafor is leading it

Nothing is needed from your side. Please do not re-run the jobs manually; the retries
are paused and a manual run will queue behind them.

Next update at 12:30 BST, whether or not there is news.

Jo Whitfield
+44 7700 900412
```

It is honest about the unknown, bounds it with a clock time, gives them an instruction, and
costs the sender nothing to retract.

---

## 4. The update — the heartbeat

**Send it whether or not there is news** — the rule practitioners break first and regret most.
Silence for two cadence cycles reads as loss of control, and the customer fills the gap by
escalating to someone who knows less than you do. The no-news update has a fixed four-part shape
and takes sixty seconds to write:

```text
No change since 14:00. Still on the database layer; Sam's team has ruled out the
replica lag and is now on the migration path. Nothing needed from you.

Next update at 16:00 BST.
```

Four parts: **"no change since `<last update time>`"**, which confirms the previous note was the
last true state · **what was ruled out** since then, the only honest progress available when
nothing is fixed · **what they should do**, usually nothing, which stops them inventing work ·
**the next exact time**, non-negotiable.

**The cadence plan is pre-written at first-note time**, with the "what it says if nothing has
changed" column filled in advance — a column filled in advance is a column that gets sent.
`../scripts/update_clock.py` computes the schedule from `severity` and `updates_sent_at` and exits 1
when one is overdue. **Never** use an update to introduce a commitment that has not passed the
Step 4 gates: updates are where unagreed dates leak, because the sender is tired and wants to
give good news.

---

## 5. The closure note

**Due within one business day of resolution.** It is not the written review, and the difference
is the discipline: **the closure note states only what is now true. It does not claim the class
of failure is solved** — that claim belongs to the review, and its evidence to the receipt.
Per section: S1 what is now working and since when · S2 the **final** confirmed figure,
superseding every interim number, with the correction named if it moved · S3 the cause in the
active voice · S4 the fix, timestamped · S5 what remains open with owner and date · S6 one line
on the class fix and its receipt date · S7 the date the written review lands, and from whom.

```text
Subject: Reconciliation jobs — resolved, and what happens next

Dana,

Your reconciliation job ran clean at 02:10 BST this morning and has run clean since.

The final confirmed count is four jobs, not three — the fourth was the 29 August retry
I told you at 14:00 yesterday I was still checking. 1,840 claims were delayed and 61
needed manual rework.

The cause was a schema migration we ran against the reporting database without a lock
check. That was our change and our miss.

23:40 (28 Aug) — migration rolled back
01:55 (29 Aug) — the four jobs re-run and verified against your row counts
09:15 (29 Aug) — retries re-enabled

Still open: Sam Okafor has the pipeline lock-check gate landing by Tue 2 Sep, and I
will confirm the day it ships rather than at the next review.

Worth checking your side: the 61 reworked claims carry a 29 August timestamp rather
than the 28th, which will show in your daily volume report for that date.

The written review reaches you by Fri 5 Sep, from me.

Jo Whitfield
+44 7700 900412
```

**The line most people omit** is "worth checking your side" — the difference between a vendor
announcing its own recovery and a vendor thinking about the customer's next week.

---

## 6. The written review

**Due within five business days of resolution for S1 and S2** `[P, practitioner convention;
published incident-review guidance converges on a 48–72h draft and a final with owned action
items inside 7–10 days]`. A document, not an email body, read by people never on the thread.

| # | Part | Content and rule |
| --- | --- | --- |
| 1–2 | Header · Timeline | Account, incident reference, severity, author, one-line summary; then one row per event in UTC **and** their timezone, detection → resolution |
| 3 | Impact for **this** customer | Their units, their hours, the final figure and every correction to earlier ones (`R23`) |
| 4 | Cause | Contributing causes, active voice, **no individual indicted** — blameless in the SRE sense `[P, Google SRE Book, postmortem culture]` |
| 5–6 | What we did · What changes | Timestamped, including what did not work; then the class fix with owner, date and how the customer sees it landed (`R19` gates every date) |
| 7 | What we are **not** changing | The thing they expect and will not get, said plainly. The section that earns the rest |
| 8 | Receipt schedule | The date each prevention item is reported back, unprompted (§7) |

**Blameless is not a courtesy; it is what makes the honest version safe to write.** A review that
can indict an individual is one whose contributors edit the truth before it reaches the page,
which is how a customer ends up reading a fiction. The frame assumes people acted on the
information, tools and constraints available at the time, then examines the system conditions
`[P, Google SRE Book]`. **The detection gap is mandatory** — "broke 03:10, alerted 03:12, we knew
09:12" is the most uncomfortable row in the timeline and the one an executive reads first.

**Security and data incidents:** this review never replaces, precedes or contradicts the
notification legal and security own. Under GDPR the controller notifies the supervisory authority
without undue delay and, where feasible, within **72 hours** of becoming aware, phased reporting
allowed where full information is not yet available; notifying affected individuals is a
separate, high-risk-triggered duty `[L, Regulation (EU) 2016/679, Arts. 33–34]`. This skill
drafts the **relationship note that sits beside** those, never the notification.

---

## 7. The prevention receipt

**Prevention promised and never reported is indistinguishable from prevention never done.** Every
S6 line gets a prevention-register row at first-note time with a receipt date, and on that date
the receipt goes out **unprompted**, whether or not anyone asked:

```text
Dana — the pipeline lock-check gate I committed to on 29 August went live on 2
September. Every schema migration now fails the build unless it declares a lock
strategy; there is no manual step left to forget.

The evidence is unsatisfying, because it is an absence: the gate has blocked two
migrations since it landed, both ours, both caught before deploy.

Nothing needed from you.

Jo
```

Sent by the person who made the commitment, not a mailing list; on the promised date, not at the
next scheduled call; carrying what shipped, how they can observe it, and what it has caught
since. **If it slipped, the receipt still goes out on the promised date** with the slip, the new
date and the owner — a slipped receipt sent on time costs a fraction of a silent one. Downstream,
the register becomes the shortfall section of the next review (`qbr-builder`, `C29`).

---

## 8. Subject lines, length and layout

Two to five words, a noun phrase, no question mark, no exclamation mark, no "URGENT" — read in a
preview pane by someone deciding whether to forward it.

| Situation | Subject | Situation | Subject |
| --- | --- | --- | --- |
| First note | `Reconciliation job failures — Meridian Health` | Missed date | `Q4 migration date — we are moving it` |
| Update | `Reconciliation jobs — 12:30 update` | Price change | `Your 2027 renewal pricing — 90 days' notice` |
| Closure | `Reconciliation jobs — resolved, and what happens next` | EOL | `Legacy export API — retirement date and your migration` |
| Written review | `Reconciliation jobs — written review, 29 August` | We got it wrong | `The seat-count advice we gave you in June was wrong` |

**Never** put the severity code, the incident ID alone, "P1" or "action required" in the subject:
`INC-4471` is our filing system, not their problem, and it belongs in the footer where their
support team can quote it. Word ceilings: **first note 180** (read on a phone by someone walking into a meeting) ·
**update 60** (longer implies news that is not there) · **closure 220** (it carries a correction
and an open item) · **written review 2 pages** (past two, the reader stops before the prevention
section) · **internal exec brief 1 page** (if it needs two, the escalation is not understood yet).

Formatting inside the fence, per `../../cs-context/references/customer-voice.md`: plain text, a
blank line between paragraphs, `•` bullets indented two spaces, no markdown headings, no pipe
tables, no `**`, one fence per artifact.

**The forwarding budget:** assume two words of preamble above it. No pronoun whose antecedent is
in a previous email, no "as discussed", no "the issue", every proper noun spelled out once. A
sentence that stops making sense when the thread above it is deleted has failed.

---

## 9. The pre-emit check

- [ ] S1 is one sentence, active, no greeting above it, and readable by a stranger; S3 is active voice with "we" as the actor, or an explicit unknown with a clock time, and no individual is named on either side
- [ ] S2 leads in their units; any money figure shows its arithmetic and is rounded to two significant figures; the boundary clause names what was **not** affected; and no blast-radius total appears below 60% coverage (`R23`)
- [ ] Every S4 line carries a timestamp and no progressive verb; every S5 line carries one name, one date and one observable outcome, and every stripped line is printed above the divider with the gate it failed (`R19`)
- [ ] S6 fixes the class, not the instance, and has a receipt date; S7 is an exact clock time in their timezone with the "whether or not there is news" clause
- [ ] At most one apology, attached to a number, a completed action and a named next date (`R20`, `C28`)
- [ ] Closure note scheduled at resolution + 1 business day; written review at + 5 for S1/S2; every prevention receipt dated
- [ ] Word count inside the ceiling; formatted for an email client, not a renderer; forward test then the eight-step leak scan in `../../cs-context/references/customer-voice.md`
