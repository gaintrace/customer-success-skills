# Internal Versions — the exec brief, the ledger, and what never crosses

> Read this **before writing the customer note**, every time. The internal version is written
> first because `../SKILL.md` Step 4 has nothing to gate against otherwise: a commitment ledger with
> no agreed owners produces a customer note with no commitments, which is the correct outcome and
> a surprising one to discover at send time.
>
> Two artifacts live here. The **exec brief** is one page, written to be forwarded to an
> executive unedited, and it asks for exactly one decision. The **commitment ledger** is the
> working record behind Step 4 and it outlives the incident. Neither is ever shown, sent,
> pasted, screen-shared or read aloud to the customer (`R18`).
>
> Evidence labels: `[M]` measured · `[V]` vendor · `[P]` practitioner · `[A]` academic.
> Emit with `../assets/internal-exec-brief.md`.

**Contents** — [1. Why internal first](#1-why-internal-first) ·
[2. The one-page brief](#2-the-one-page-brief) · [3. The one ask](#3-the-one-ask) ·
[4. The commitment ledger](#4-the-commitment-ledger) ·
[5. Exposure without false precision](#5-exposure-without-false-precision) ·
[6. What we are not telling them yet](#6-what-we-are-not-telling-them-yet) ·
[7. The stop-loss](#7-the-stop-loss) · [8. The firewall](#8-the-firewall) ·
[9. Distribution](#9-distribution) · [10. Worked example](#10-worked-example) ·
[11. Checklist](#11-checklist)

---

## 1. Why internal first

**The customer note carries no commitment that has not already been agreed internally.** That
sentence is the whole reason for the ordering. Written the other way round, the sequence is:
draft a helpful note → send it → discover on Thursday that nobody owns Tuesday's date → send a
second note correcting the first. The second missed date is the one after which nothing you say
is believed (`R19`).

| Written first | Consequence |
| --- | --- |
| **Internal** | Every date in the customer note has a name against it and a written yes. Stripped commitments are known *before* the customer reads a promise |
| Customer | The gates run against nothing. "Engineering is on it" ships, and the correction costs more than the incident |

The two documents are **never the same document with words removed.** The customer note is
written from source facts — the incident record, the usage export, their own ticket text — not
from the internal brief. Copying a well-phrased internal line across the wall is the single most
common leak, and it happens precisely because the line was well phrased.

---

## 2. The one-page brief

**One page. If it needs two, the escalation is not understood yet.** An executive reads the first
table and the ask; everything else exists so their first question has an answer.

| Field | What goes in it | Failure form |
| --- | --- | --- |
| **Account · ARR · renewal · opt-out (days)** | `name` · `$X` · `renewal_date` · **`renewal_date − notice_period_days` and the days remaining** | The renewal date alone. The opt-out date is the real deadline (`R1`) |
| **What happened** | Three bullets, each a dated fact, no adjectives | A narrative. An exec reading a story is an exec reconstructing a timeline |
| **Evidence** | 2–3 data points with provenance tags `[system · field · as-of]` | Assertions. "Usage has collapsed" without a number is an opinion |
| **Impact on them** | Their units, then hours, then money with the arithmetic | Our units. Uptime percentages do not survive contact with an executive |
| **Impact on us** | Exposure scenario (§5), other accounts on the same defect, reference status | A single ARR number with no scenario attached |
| **Why now** | What forces the timeline — the opt-out date, their board meeting, their regulator, a competitor's evaluation window | "It's urgent." Urgency without a date is a feeling |
| **What we have tried** | Dated, with outcomes, including what failed | A list of activity. Outcomes are the point |
| **What we owe them** | Any commitment of ours currently overdue, with the date it was promised — or "nothing outstanding" | Omitting it. It sits **above** the ask, because an exec should know what we already failed to do before being asked for more |
| **The one ask · decision by · owner** | §3 | Three asks, which is zero asks |
| **Stop-loss** | §7 | Absent, which is how a save runs until the money runs out |
| **Not telling the customer yet** | §6 | Absent, which means nobody has decided; it is being withheld by accident |

**Health band, risk score and matched pattern belong here and only here.** They come from
`churn-risk` and they inform our decision. They have no customer-facing form in any wording
(`R18`).

---

## 3. The one ask

**An escalation with no named ask and no decision date is a notification.** It wastes the
executive's attention and trains them to skim the next one.

| A real ask | Not an ask |
| --- | --- |
| "Approve Sam Okafor for four engineering days this week, at the cost of the Q4 connector slipping one sprint." | "Join a call." |
| "Call their CTO before Thursday. Script attached; the one thing you must commit to is the 2 September gate." | "Please advise." |
| "Authorise waiving the September consumption overage we caused — $18k — so I can state the correction in the closure note." | "We need exec support." |
| "Decide by Friday whether we are keeping this account past the 30 September stop-loss." | "Let me know your thoughts." |

Every ask carries **the trade**: what we give up if the answer is yes. An executive who is not
told the cost will discover it later and will discount the next brief accordingly.

| Ask shape | Use when |
| --- | --- |
| **Decision** — "yes or no by Friday" | The path is clear and needs authority |
| **Resource** — "four engineering days, named person" | The path is clear and needs capacity |
| **Presence** — "call their CTO, this script, this one commitment" | Their side has escalated above our sender's register |
| **Authority** — "latitude up to $X, in exchange for Y" | A commercial move is required. **The move itself runs in `renewal-negotiation`, never in the escalation note** (`R11`) |

**"If yes" and "if no" are both written out.** A brief that describes only the good branch is
asking for approval, not a decision.

---

## 4. The commitment ledger

The working record behind `../SKILL.md` Step 4. It is filled **before** the customer note is
drafted, and it is the artifact that survives the incident — six weeks later it is the only
place that remembers what was promised.

| # | Commitment | Owner | Agreed? (source + timestamp) | Date | Gate result | In the note? |
|---|---|---|---|---|---|---|
| 1 | Pipeline lock-check gate blocks any migration without a lock strategy | Sam Okafor, VP Eng | Yes — Slack #inc-4471, 2026-08-29 11:20 | Tue 2 Sep | **Pass 1–5** | Yes |
| 2 | Retry backstop so a failed job re-queues without operator action | Sam Okafor, VP Eng | No — asked 11:20, no reply | Fri 5 Sep | **Fail gate 2** | No → downgraded to a decision date I own |
| 3 | Row-count reconciliation report shared each morning until closure | Jo Whitfield, CSM | Yes — self, 2026-08-29 09:50 | Daily to closure | **Pass 1–5** | Yes |
| 4 | Waive the September consumption overage caused by our retries | Dan Reeve, CFO | Pending — asked 2026-08-29 12:05 | Decision by Mon 1 Sep | **Fail gate 5** | No — commercial (`R11`), routes to `renewal-negotiation` |

**Rules the ledger enforces:**

1. **A row reading "Fail" cannot read "In the note: yes".** This is the whole mechanism. If the
   two columns disagree, the note is wrong, not the ledger.
2. **"Agreed" requires a source and a timestamp.** A remembered corridor conversation is not
   agreement. "Sam said it was fine" fails gate 2 as surely as silence does.
3. **Every failed row produces a line above the divider** in the customer artifact naming the
   commitment, the gate it failed and who must agree it. The customer never sees it; the person
   who has to chase Sam does.
4. **The downgrade ladder is recorded, not implied** — delivery → decision → investigation →
   refusal → deleted (`accountability-language.md` §6). A row that moved down a rung says which
   rung and why.
5. **The ledger outlives the note.** Row 1's promised date becomes the prevention receipt due
   date, and the receipt goes out unprompted whether or not anyone remembers asking.

---

## 5. Exposure without false precision

ARR at risk is a **scenario, not a number**. Written as a bare figure it gets repeated in a
forecast review as though someone measured it.

| Write | Never |
| --- | --- |
| "Full churn: **$620k**, decided at the 7 November opt-out. Partial: a downsell of the two affected business units, **~$180k**, more likely on current evidence." | "$620k at risk" |
| "Reference status: they are our named logistics reference; a public withdrawal costs two named deals in Q4." | "Reputational risk" |
| "Four other accounts run the same nightly pattern; **~$310k** combined. None has reported a failure and none has been told." | "Other customers may be affected" |

Round every composite to **two significant figures** (`$180k`, not `$179,400`) — a composite
stated to the dollar implies a measurement nobody took. State probability as a **band**, never a
percentage, unless a backtest exists (`R22`).

**The other-accounts line is mandatory and is the one most often skipped.** If four accounts sit
on the same defect, that is a portfolio decision an executive is entitled to make, and it changes
whether this is one note or a tiered announcement (`cadence-and-severity.md` §7).

---

## 6. What we are not telling them yet

A named section, with three columns: **what, why, and when that changes.** A withheld fact with
no revisit date is not a decision — it is a leak waiting for the moment nobody chose.

| Withheld | Why | Disclosed when |
| --- | --- | --- |
| Four other accounts hit the same defect | Their identity is not ours to share, and the count alone invites a question we will not answer | Never as identities. The count goes in the written review if they ask |
| The 12 August internal ticket that predates their incident | We are confirming whether it is the same defect | **In the written review on 5 Sep, either way.** If it is the same defect, this becomes a repeat and the note changes more than the failure did |
| That the fix requires a version upgrade they have deferred twice | It reads as blame today; it is a real constraint on their timeline | On the 2 Sep call, framed as our sequencing problem, not their deferral |

**Legitimate reasons to withhold:** it is another customer's information; it is not yet confirmed
and would have to be retracted; legal or security own the disclosure and have not cleared it;
it is our internal assessment and has no customer-facing form (`R18`).

**Illegitimate reasons:** it is embarrassing; it might annoy them; it is being handled and they
do not need to know; the CSM would rather deliver it in person next month. Each of those is a
disclosure that will happen later, worse, and without your framing.

---

## 7. The stop-loss

`R21`: **every save has a spend ceiling and an exit date.** The escalation brief carries it even
when nobody wants to write it down, because the alternative is a save that consumes the hours
which would have protected three healthy accounts and ends badly anyway.

| Field | Example |
| --- | --- |
| **Spend ceiling** | 12 engineering days and 6 CSM days to 30 September |
| **Exit date** | 30 September, one week before their 7 November opt-out minus paper time (`R7`) |
| **Exit condition** | No exec meeting held by 15 September, **or** the 2 Sep gate slips twice, **or** they decline the written review |
| **What exit looks like** | Managed handover to `save-play` §graceful-exit, win-back preserved, reference relationship protected |

The stop-loss is reviewed at each ledger update and **only an executive may extend it.** A CSM
extending their own stop-loss is the mechanism by which it stops existing.

---

## 8. The firewall

Nothing in this file crosses. Not softened, not hinted at, not translated (`R18`).

| Internal line | Customer-facing form |
| --- | --- |
| "Health band Red; matched pattern *Death by a thousand tickets*" | *(None. No wording exists.)* |
| "ARR at risk $620k; exposure scenario full churn" | *(None.)* |
| "Forecast moved to Best Case" · "save play open" · "war room" | *(None.)* |
| "Their CTO is the blocker; the champion has no internal weight" | *(None. Every assessment of a named person is internal-only)* |
| "Pre-approved latitude: 8% for a two-year term" | *(None in this note. It moves to `renewal-negotiation`, in a separate conversation, in a different week — `R11`)* |
| "Four other accounts affected" | "Two other accounts were affected" only where a count is genuinely needed. Never an identity, never a description |
| "Escalated internally; P1 aged 19 days" | "Sam Okafor owns this from 10:30 today, and you will hear from me every hour until it is closed." |

**The mechanical guards**, because the leak is usually a mechanism failure rather than a
judgement failure:

- The customer block is written from source facts, never by editing an internal paragraph.
- The internal header sits **above** the divider in every artifact this skill emits, and the
  divider text says "do not forward it".
- Calendar invites, shared-channel messages and file names carry neutral titles. A shared Slack
  Connect channel is read by the customer, because it is.
- Every attachment's **columns** are checked before it is sent. A usage export with a
  `health_score` column has ended relationships that the incident had not.

---

## 9. Distribution

| Audience | Gets | Channel |
| --- | --- | --- |
| The named executive being asked | The one-page brief | Email or a doc link, **not** a Slack paste that loses the divider |
| The incident lead and DRI | Brief + ledger | The incident channel |
| The CSM and their manager | Brief + ledger + the customer draft | Internal channel |
| Finance / legal / security | The brief only, where the ask touches them | Their own channel |
| **Anyone in a shared channel with the customer** | **Nothing** | — |

**Never paste the brief into a channel the customer can join, and never forward an internal
thread to the customer.** Start a new email. The reply-below-the-fold leak is the one that
survives every good intention.

---

## 10. Worked example

```markdown
# Escalation — Meridian Health · S1 · 2026-08-29 · first note
**Internal.** Do not forward. **Data as-of 2026-08-29.**

| Field | Value |
|---|---|
| Account · ARR · renewal · **opt-out (days)** | Meridian Health · $620k · 2027-02-05 · **2026-11-07 (70)** |
| What happened | 2026-08-28 03:10 — nightly reconciliation job failed · 08:55 — their ops lead raised it, before our alerting · 09:41 — we confirmed the cause is ours |
| Evidence | 4 failed runs `[warehouse · events.event_name='recon_job_failed' · through 2026-08-29]` · 1,840 delayed claims `[their export · as-of 2026-08-29]` · prior occurrence 2026-05-14, same job `[Zendesk · ticket 88214]` |
| Impact on them · on us | 1,840 claims delayed, 61 reworked, ~22 h of their team · full churn $620k at the 7 Nov opt-out; partial ~$180k downsell more likely; they are our named logistics reference |
| Why now · what we have tried | Their board meets 12 September and their COO has asked for a written cause · rollback 23:40 (worked), retries paused 10:05 (worked), alerting review (open, no owner) |
| **What we owe them** | The May RCA promised on 2026-05-20 and never sent. This is a repeat, and they know it |
| **The one ask · by · owner** | Sam Okafor for 4 engineering days this week, at the cost of the Q4 connector slipping one sprint · decide by 2026-08-30 · Priya Raman (CCO) |
| Stop-loss · not telling them yet | 12 eng + 6 CSM days to 30 Sep; exit if no exec meeting by 15 Sep · the 12 Aug internal ticket, until we confirm it is the same defect — disclosed in the 5 Sep review either way |
```

The line that makes this brief work is **"what we owe them"**. An executive who reads "the May
RCA was promised and never sent" understands the account in one line, and every decision after
it is better.

---

## 11. Checklist

- [ ] One page. Opt-out date and days remaining, not just the renewal date (`R1`)
- [ ] Every fact dated; every number carries a provenance tag; every gap reads `UNKNOWN — requires X`
- [ ] Exposure written as a scenario, rounded to two significant figures, with other affected accounts counted
- [ ] Exactly **one** ask, with a named executive, a decision date, the trade, and both the "if yes" and "if no" branches
- [ ] "What we owe them" present and sitting above the ask, or an explicit "nothing outstanding"
- [ ] Commitment ledger complete; no row reads "Fail" and "In the note: yes"; every failed row is printed above the divider in the customer artifact (`R19`)
- [ ] Stop-loss has a ceiling, an exit date and an exit condition (`R21`)
- [ ] "Not telling them yet" has a reason and a disclosure date for every row
- [ ] Nothing from this file appears in the customer note in any wording (`R18`); the customer block was written from source facts, not by editing an internal line
- [ ] Distribution list checked; nothing pasted into a shared channel; attachment columns checked
