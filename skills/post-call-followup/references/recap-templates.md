# Customer Recap Templates

> Section C only. Everything in this file is customer-facing text. Nothing here may contain a
> health band, a risk phrase, a dollar figure that was not agreed on the call, a forecast
> category, or a comment about the customer's own people. Assemble every line from a `SHARE`
> or `TRANSLATE` tag produced in Step 4 of `../SKILL.md`.
>
> **Every example below is written the way it must be emitted:** inside a ```text fence, below
> the `CUSTOMER-FACING` divider, formatted for an email client and not a markdown renderer —
> plain text, a blank line between paragraphs, `•` bullets, aligned columns where a table is
> unavoidable, no markdown headings, no pipe tables, no `**`, and no unfilled placeholders. See
> `../../cs-context/references/customer-voice.md` for the divider text and the full standard.

**Contents**
1. [The universal skeleton](#1-the-universal-skeleton)
2. [Meeting-type variant matrix](#2-meeting-type-variant-matrix)
3. [Worked example — routine check-in](#3-worked-example--routine-check-in)
4. [Worked example — QBR](#4-worked-example--qbr)
5. [Worked example — renewal conversation](#5-worked-example--renewal-conversation)
6. [Worked example — escalation, after a call that went badly](#6-worked-example--escalation-after-a-call-that-went-badly)
7. [Worked example — expansion](#7-worked-example--expansion)
8. [Worked example — technical review](#8-worked-example--technical-review)
9. [Worked example — first call with a new stakeholder](#9-worked-example--first-call-with-a-new-stakeholder)
10. [The repair form — more than 48 hours late](#10-the-repair-form--more-than-48-hours-late)
11. [The zero-commitment recap](#11-the-zero-commitment-recap)
12. [Subject line bank](#12-subject-line-bank)
13. [Phrase bank — write this, not that](#13-phrase-bank--write-this-not-that)
14. [Distribution rules](#14-distribution-rules)
15. [Register by relationship](#15-register-by-relationship)
16. [Working from what you were actually given](#16-working-from-what-you-were-actually-given)

---

## 1. The universal skeleton

```text
Subject: <account + the decision made or the thing owed>

Hi <first name>,

<Opening line: the single most useful thing that came out of the call. One sentence.>

Decided today:                    ← drop the whole block if nothing was decided
  • <decision>

Who owes what:                    ← one line per commitment: who, what, when
  • <Named person> — <observable action>, <weekday + date>

Still open:
  • <question> — <named person>, by <date>

Next session: <two dated, timed slots>. <Purpose in one line.>

<Sign-off, first name. One ask maximum, already stated above.>
```

**Length target.** Gong Labs' analysis of 1M+ executive sales cycles reports open rates
declining as subject lines lengthen (1–4 words performs best) and reply rates dropping sharply
past 100 words, best-performing emails at 50–100 words (Gong Labs, 2026 `[V]` — vendor-analysed
and drawn from cold outbound, so directional rather than a benchmark). Keep prose under ~200
words; carry detail in tables, which do not read as length.

**Evidence convention:** `[M]` measured · `[V]` vendor-analysed · `[P]` practitioner rule of
thumb · `[D]` derived here from stated inputs.

---

## 2. Meeting-type variant matrix

| Type | Recap leads with | Mandatory extra block | Latency | Cc | Most common failure |
| --- | --- | --- | --- | --- | --- |
| **Routine check-in** | The one thing that changed since last time | Status of the previous recap's commitments | 24h | Nobody new | Turning a 20-minute call into a 600-word essay |
| **QBR / EBR** | Progress against the objectives *they* stated, in their numbers | Objective-by-objective table with the metric, target and current value | 24h | Their exec sponsor (they invited them to the meeting; keep them in the thread) | Leading with your product metrics instead of their business outcomes |
| **Renewal** | Price, term, quantity and the paper path, in writing | The dates: quote validity, **opt-out deadline**, signature target | **Same day** | Their procurement contact only once they have joined the conversation | Naming the renewal date and not the opt-out deadline |
| **Escalation** | What went wrong, in their words | Fix plan: what, who, by when, and how they will know | **4 hours** | Your exec sponsor by name, so the customer sees the escalation is real | Defending the facts inside the apology |
| **Expansion** | The business case in their numbers | Scope, commercial shape, and the decision path with named approvers | Same day | Their finance or procurement contact only if they asked for it | Sending pricing nobody asked for |
| **Technical review** | The architecture decision that was made | Defect table with Jira/Linear keys, owners and committed dates | 24h | Their technical lead and yours | Committing an engineering date the engineer did not agree to |
| **First call, new stakeholder** | What they inherit and what we already owe them | A three-line history: what was bought, why, and what has been delivered | 24h | The person who introduced them | Making them read a history that assumes context they do not have |

**The two rules that hold across all seven:**

1. **Latency is measured from call end**, not from when you sat down to write.
2. **One ask.** If the call generated three asks, the other two go in the internal note and
   into the next conversation. A recap with three asks gets none of them answered.

---

## 3. Worked example — routine check-in

*Northwind Logistics · $84k ARR · monthly check-in with Priya Raman (Ops Director, champion)
and Tom Weir (admin). Objective from the pre-call brief: Finance's first three users
provisioned by end of September.*

```text
Subject: Northwind — Finance starts 15th, next steps

Hi Priya,

The useful thing from today was that Finance can start on the 15th rather than
waiting for the Q4 freeze, which pulls the whole rollout forward by about six
weeks.

Decided today:
  • Finance starts with 3 users on the existing plan, not a separate workspace.
  • The custom routing rules stay as they are until after the Finance pilot.

Who owes what:
  • Tom — the three Finance user emails for provisioning, Wed 3 Sept
  • You — confirm the Finance pilot with Marcus, Fri 5 Sept
  • Me — provision the accounts, send the starter guide and book the Finance
    kickoff, Thu 4 Sept (one working day after Tom's list)

Still open: whether Finance needs the approval workflow on from day one. Marcus
owes that one, via you, by Fri 5 Sept.

Next session: Tue 30 Sept 10:00 or Wed 1 Oct 14:00 — 20 minutes on how the
Finance pilot went and whether to widen it.

Sam
```

**Why this passes.** 118 words. Four commitments, each with a named human and a calendar date;
the open question has an owner and a date; two dated slots; one ask. Nothing about health,
risk or renewal. **Tagged `INTERNAL`:** Priya is the only contact with sustained activity —
Tom logged in twice in 60 days and Marcus has never been in a meeting. That single-threading
read belongs in the note and fires a `stakeholder-map` refresh.

---

## 4. Worked example — QBR

*Halcyon Health · $310k ARR · Q2 review with Dana Osei (VP Clinical Ops, economic buyer),
Ken Larsson (champion) and two managers.*

```text
Subject: Halcyon Q2 review — sites 4 and 5 decision + 4 owners

Hi Dana,

The clearest result from the quarter is that the three sites running the new
intake flow cut average intake time from 14 minutes to 9. The two sites still on
the old flow have not moved, which is what makes the Q3 decision straightforward.

Against the objectives you set in January:

  Objective                        Target     Where it is now
  Cut intake time                  10 min     9 min at 3 sites, 14 at 2 sites
  Reduce chart-review rework       -25%       -18%
  One reporting view across sites  Live Q2    Live since 14 May, 4 of 5 sites

Decided today:
  • Sites 4 and 5 move to the new intake flow in Q3, site 4 starting 6 October.
  • Chart-review rework gets a working session, not another dashboard.

Who owes what:
  • Ken — confirm site 4's clinical lead and their October training window,
    Fri 12 Sept. That locks the 6 Oct start.
  • You — approve 2 hours of clinical time per site for training, Fri 19 Sept.
    That removes what stalled sites 4 and 5 in Q1.
  • Me — site-4 rollout plan with the training agenda, Wed 17 Sept, so Ken has
    something to circulate.
  • Me — run the chart-review working session, week of 6 Oct, day Ken picks.

Still open: whether site 5 follows in November or waits for January. You said
you would decide after the site-4 result — Fri 24 Oct works if that holds.

Next session: Thu 6 Nov 09:00 or Fri 7 Nov 13:00 — the site-4 result and the
Q4 view.

Ravi
```

**Why this passes.** It opens on *their* metric. The objectives table uses the targets they set
in January and shows the one that is behind (−18% against −25%) rather than hiding it — you
are better off in the conversation about a difficult metric than pretending it is not
happening (The Success League, 2026 `[P]`). Dana, the economic buyer, carries exactly one
commitment, and it is the one that unblocks everything else. **Tagged `INTERNAL`:** Dana joined
12 minutes late and left before the roadmap; last year she stayed the full hour — a
sponsor-attention delta for the Relationship & engagement family, not a line in the email.

---

## 5. Worked example — renewal conversation

*Orbital Systems · $196k ARR · renewal 2027-01-31 · notice 60 days → **opt-out deadline
2026-12-02**. Aisha Bello (VP Engineering, economic buyer) and Dan Petrov (procurement).*

```text
Subject: Orbital renewal — terms, and the 2 Dec notice date

Hi Aisha,

To put the timing in one place: the current term ends 31 Jan 2027 and your
notice window closes 2 Dec 2026, so the decision needs to be made before then
rather than in January.

What we talked through:

                  Current      Proposed
  Term            12 months    24 months
  Seats           240          300
  Annual value    $196,000     $228,000 on 24 months / $241,000 on 12
  Uplift          -            4% at month 12 on the 24-month term

Who owes what:
  • Me — formal quote covering both options, valid 30 days, Wed 10 Sept. That
    starts your procurement clock.
  • Dan — confirm whether a 24-month term needs a new security review,
    Fri 12 Sept. That decides whether we need 4 weeks or 1.
  • You — decide 12 vs 24 months, Fri 3 Oct. That leaves 8 weeks before 2 Dec.
  • Dan — confirm the signatory and whether a PO is needed, Fri 3 Oct. Those
    are the two things that usually add a fortnight.

Still open: whether the 60 extra seats land in one block or in two phases.
Yours to call, by Fri 3 Oct.

Next session: Tue 7 Oct 11:00 or Wed 8 Oct 15:00 — 30 minutes to close out
terms.

Ravi
```

**Why this passes.** The **opt-out deadline** leads, not the renewal date. Both commercial
options are stated so procurement has something to compare, and every date works backwards
from 2 Dec. Nothing about forecast category, risk band, or our walk-away position — that is
Section B. **Tagged `INTERNAL`:** Aisha said "we're consolidating tooling across engineering in
Q1" — a consolidation trigger firing a same-day `save-play` and forecast review, and the single
most important thing said on the call. It does not go in the email.

---

## 6. Worked example — escalation, after a call that went badly

*Meridian Retail · $128k ARR · call following a 5-day outage of the nightly sync. Carla Nunes
(Director of Data, champion) was visibly angry: "this is the third time this year". Internal
note and escalation written first; 3-hour cool-down; VP CS approved the text before send.*

```text
Subject: Meridian — what we're changing after the sync failure

Hi Carla,

You told us this is the third sync failure this year, and that your team spent
two days rebuilding reports that should have been ready on Monday. That is a
fair account of what happened and I am not going to add to it.

What we are changing:
  • Root cause write-up for all three incidents, including the two we closed
    without one — Marcus Bell, our Support Director, by Fri 5 Sept. You get
    the document.
  • Sync failures alert you directly, not only us — Marcus, Fri 12 Sept. You
    will receive a test alert that day.
  • Weekly sync-health summary until 31 Oct, then we decide together whether
    to continue — me, first one Mon 8 Sept.
  • Marcus joins our monthly call until end of October — already booked, he is
    on the 30 Sept invite.

Still open: whether the two days of rebuild work needs a commercial
conversation. That one is mine to come back on, by Fri 12 Sept, once the root
cause write-up is done.

Next session: Tue 9 Sept 10:00 or Wed 10 Sept 16:00 — 20 minutes on the root
cause document.

Sam
```

**Why this passes.** It repeats her words back before anything else, and does not explain what
went wrong technically — that is the root-cause document, not the apology. Every remedy has a
named human, a date and an observable proof. The commercial question is raised by us and dated
rather than left for her to raise.

| Rule | Applied here |
| --- | --- |
| Internal note and escalation first | Both written before the email |
| Named internal approver · cool-down inside 24h | VP CS reviewed; 3 hours |
| No defence of the factual record | The word "however" does not appear |
| No new ask · exec named in the text | The only question is one we owe her; Marcus Bell by name and title |

---

## 7. Worked example — expansion

*Vantage Analytics · $64k ARR · health band Secure · prompted by the customer asking on a
check-in, "can we add the compliance module for the EU team".*

```text
Subject: Vantage — compliance module for the EU team, scoped

Hi Lena,

You asked about the compliance module for the EU team, so here is what it looks
like against the numbers you gave me: 18 EU users, the two audit reports you
named, and a January go-live to be ready for the March audit.

  Scope        Compliance module, 18 EU users, retention and access-log reports
  Commercial   Add-on to the existing agreement, co-terminous with 30 Jun
  Timing       3 weeks to configure; a January start leaves 8 weeks before
               the March audit

Who owes what:
  • Me — scoped pricing for 18 users, co-terminous, Thu 4 Sept. That gives you
    a number for the budget conversation.
  • You — confirm the report formats your auditor accepts, and who signs an
    add-on, Fri 12 Sept. That stops us building the wrong output and decides
    whether this is a 2-week or a 6-week path.

Still open: whether the EU team needs SSO through your existing IdP on day one.
You and your IT lead, by Fri 19 Sept.

Next session: Wed 17 Sept 09:30 or Thu 18 Sept 15:00 — 30 minutes on the
pricing and the January plan.

Ravi
```

**Why this passes.** The expansion was **declared by the customer** — the highest-grade
expansion signal there is; log the exact quote and open the opportunity the same day.
Everything sits in their numbers (18 users, their auditor, their March deadline), not in
feature names. Health band was Secure before this was written; on an At Risk account this
email does not get sent at all.

---

## 8. Worked example — technical review

*Corvus Freight · $172k ARR · quarterly technical review with their platform team.* Only the
blocks that differ from the skeleton are shown; the rest is standard.

```text
Subject: Corvus — webhook-first decision + v1 sunset date

Hi Jonas,

The decision from today is that you go webhook-first for shipment events and
keep polling only for the nightly reconciliation, which removes the rate-limit
problem your team hit in July.

Decided today:
  • Shipment events move to webhooks; nightly reconciliation stays on the
    batch API.
  • The v1 endpoints stay available to you until 30 Jun 2027 — confirming that
    in writing here.

Open defects:
  ENG-4471  Duplicate webhook delivery on retry
            Committed Fri 26 Sept, in progress, confirmed by our engineering
            lead on the call today
  ENG-4502  Timezone offset on the reconciliation export
            Committed Fri 17 Oct, scheduled
  ENG-4388  Bulk export timeout above 500k rows
            No committed date yet — I owe you one by Fri 5 Sept

Who owes what:
  • Me — the committed date for ENG-4388 from engineering, Fri 5 Sept, so you
    can plan the Q4 migration.
  • You — webhook endpoint and retry policy, Fri 12 Sept. We configure the
    sandbox by Wed 17 Sept once we have it.

Next session: Thu 2 Oct 14:00 or Fri 3 Oct 10:00 — sandbox walkthrough.

Ravi
```

**Why this passes.** Every defect carries a Jira key. The one without a committed engineering
date is written as `UNKNOWN` plus a dated commitment from us to supply it — never a guessed
date, because a guessed engineering date is the fastest way to lose a technical buyer. The v1
sunset date is confirmed in writing: exactly the kind of thing agreed on a call and disputed a
year later.

---

## 9. Worked example — first call with a new stakeholder

*Kestrel Media · $92k ARR · the champion left; Nadia Haq inherited the account and this is her
first call with us.* The variant is the **history block**, which no other meeting type carries.

```text
Subject: Kestrel — where things stand, and the two we owe you

Hi Nadia,

Since you have picked this up mid-stream, here is the short version of what you
have inherited and the two things we owe you.

Where this came from:
  • Kestrel bought the platform in March 2025 to cut the campaign reporting
    cycle from 5 days to 1. Reporting now runs same-day for the 4 brands that
    are on it.
  • Two brands, Halo and Ridge, were never onboarded. That paused in November
    when Jamie moved teams and has not restarted.

What we owe you, both by Fri 5 Sept:
  • A one-page summary of what each of the 4 live brands uses.
  • The Halo/Ridge onboarding plan Jamie and I drafted in October, unchanged.

What I would like from you: tell me which of the two to look at first — or that
neither is a priority this quarter, which is a perfectly good answer. By
Fri 12 Sept.

Next session: Wed 17 Sept 11:00 or Thu 18 Sept 15:00 — 30 minutes on whichever
you pick.

Sam
```

**Why this passes.** It assumes no context, names the paused work rather than waiting for her
to find it, and offers "neither is a priority this quarter" as an acceptable answer — which is
what makes a first ask answerable rather than a test. One ask.

---

## 10. The repair form — more than 48 hours late

Do not send the standard recap late and hope nobody notices. The lateness is itself a broken
commitment. Two changes: **name it in the first line, once, without a paragraph of apology**,
and **re-open the commitments rather than asserting them** — after 48 hours you no longer have
a shared record, so ask for correction explicitly rather than confirm-by-default.

```text
Subject: Halcyon — notes from Tuesday

Hi Dana,

This should have reached you Wednesday. Notes below — tell me where my version
differs from yours.

<the standard blocks, unchanged>

Where I have a date and you do not remember agreeing to one, my date is wrong,
not yours. Send me the correction.

Ravi
```

Log the latency in Section B as a broken commitment we owe and increment the account's
commitment-debt counter. Three overdue recaps is a follow-through problem that shows up in
renewals long before it shows up in a health score.

---

## 11. The zero-commitment recap

When the customer agreed to nothing, the recap gets **shorter**, not longer. Padding it with
the asks they declined converts a soft no into a written no.

```text
Subject: <Account> — notes from today

Hi <first name>,

Short note from today so we both have the same record.

What I'm doing:
  • <our commitment>, <weekday + date>
  • <our commitment>, <weekday + date>

One thing I'd like from you: <the smallest ask that still unblocks us>, by
<date>.

Next session: <two dated, timed slots>.

<First name>
```

| Rule | Why |
| --- | --- |
| Our commitments only in the table | Recording an ask they declined as a commitment is a fabrication |
| Exactly one ask, and make it the cheapest one | A customer who declined five asks will decline six |
| Still propose two dated slots | The next meeting is the only commitment worth chasing here |
| Log the absence in Section A | Zero commitments is a Relationship & engagement signal, and it fires a 3-business-day dated ask (Step 7) |
| Never write "let me know if you have any questions" | It converts a no-commitment call into a no-commitment email |

---

## 12. Subject line bank

1–4 words plus the account or the decision. Lowercase after the account name reads as a note,
not a campaign.

| Meeting | Subject | | Meeting | Subject |
| --- | --- | --- | --- | --- |
| Check-in | `Northwind — next steps` | | Expansion | `Vantage — compliance module` |
| QBR | `Halcyon Q2 review — decisions` | | Technical | `Corvus — architecture decisions` |
| Renewal | `Orbital renewal — terms and dates` | | New stakeholder | `Kestrel — where things stand` |
| Escalation | `Meridian — what we're changing` | | Repair / zero-commitment | `Halcyon — notes from Tuesday` · `Ashford — notes` |

**Never:** `Following up` · `Touching base` · `Great speaking with you!` · `Recap of our call
on Tuesday 26th August 2026 regarding the Q3 rollout` (long) · `Quick question` (it isn't).

---

## 13. Phrase bank — write this, not that

| Rookie | Write instead | Why |
| --- | --- | --- |
| "Thanks for your time today!" | "The useful thing from today was <X>." | The first line is the only line some readers see |
| "As discussed, we'll come back to you on pricing." | "I'll send scoped pricing for 18 users by Thu 4 Sept." | Named actor, observable act, calendar date |
| "The team will look into it." | "Marcus Bell will send the root-cause write-up by Fri 5 Sept." | "The team" is nobody |
| "Please confirm the above." | "I've recorded X by <date> — tell me if that needs to move." | Correction is a cheaper reply than confirmation |
| "Let me know your availability." | "Tue 7 Oct 11:00 or Wed 8 Oct 15:00?" | Two options is a decision; open availability is a task |
| "We want to make sure you're getting value." | "Sites 4 and 5 are still at 14 minutes against your 10-minute target." | Their number, their target |
| "Your renewal is coming up on 31 Jan." | "Your notice window closes 2 Dec, so the decision lands before then." | The opt-out deadline is the real date |
| "Sorry you've had a poor experience." | "You told us this is the third sync failure this year, and your team lost two days." | Their account, in their words |
| "Let me know if you have any questions!" | <Delete. End on the ask or the next session.> | It invites nothing and dilutes the one ask |

---

## 14. Distribution rules

| Question | Rule |
| --- | --- |
| **To** | Everyone who was on the call, including their side's silent attendees |
| **Cc** | Only people the customer already has in the thread, plus your own exec when the recap names them as an owner |
| Adding someone new | Never in a recap — introduce them in a separate note with a reason. A recap is not the place to widen the room |
| Their exec sponsor / your manager | Cc their exec only if they attended or were already in the thread; an exec who was not there reads as escalation. Never Cc your manager by default — it changes how the customer replies |
| Internal forwarding · reply-all | Forward the internal note, never the recap. Keep commitments in the original thread; a new subject line orphans the record |

---

## 15. Register by relationship

The structure of a recap is fixed. The register is not, and getting it wrong costs more than a
clumsy sentence — an over-warm email after a bad call reads as not having listened, and a formal
one to a two-year champion reads as a handover. Read this when the relationship is new, senior,
or difficult; the library-wide version with sentence-level rewrites is
`../../cs-context/references/customer-voice.md`.

| Relationship | Register | Sign-off | The specific trap |
| --- | --- | --- | --- |
| **Established** (>6 months, regular contact) | Conversational, first names, one line of personality | "Thanks," | Over-familiarity in a thread they will forward to their CFO |
| **New** (first 90 days, or a new stakeholder) | Friendly, measured, no shorthand, acronyms spelled out | "Best," / "Thanks," | Assuming context they do not have — they were not part of the original decision |
| **Executive** (VP+, or a forwarded audience) | BLUF, no preamble, decisions and outcomes, half the length | "Best," | Burying the ask under the recap |
| **Difficult** (friction surfaced, escalation, complaint) | Direct, plain, zero excess apology, no hedging verbs | "Thanks," | Cheerfulness — it reads as not having heard them |
| **Multi-party** (several attendees, mixed seniority) | Write to the most senior reader; put detail in aligned columns the rest can scan | "Best," | Addressing the friendliest person rather than the decision-maker |
| **Technical** (engineers, admins, security) | Precise, issue keys and version numbers, no adjectives | "Thanks," | Marketing language — this audience discounts it instantly and permanently |

Two rules survive every register:

- **Match their energy, do not exceed it.** A call that surfaced friction gets an email that
  names the friction. Writing around it creates a credibility gap the customer notices
  immediately, and it is the fastest way to lose a difficult account's trust.
- **Match their length.** Three bullets of notes become a short email. Padding a thin call into
  six paragraphs tells the customer you are performing effort rather than reporting substance,
  and it buries the one thing that mattered.

If the user overrides the register — "make it warmer", "this one is formal" — follow the
override and say you have.

---

## 16. Working from what you were actually given

Read this when the input is thin, or when you are tempted to fill a template. Every row degrades
rather than refusing: a short honest recap beats a complete invented one.

| Input | How to mine it | The trap |
| --- | --- | --- |
| **Full transcript** | Pull, never quote at length. Hunt four things: stated commitments, stated concerns, stated wins, open questions. **Weight the last third** — action items are set at the end, and the opening is small talk and re-orientation | Recapping the discussion. They were there |
| **Bullet notes** | Take them at face value and keep the email proportionate. Mark inferred owners and dates explicitly so they can be corrected | Inventing detail to fill the template |
| **Sparse notes** (2–4 lines) | Write a short email. Grade every commitment; most will be Grade C and belong in Open questions, not Commitments | Producing a confident recap from thin evidence |
| **Nothing but memory** | Say so. Ask for the two or three specifics that make the email worth sending — who committed to what, and by when | A generic recap, which is worse than none |
| **Recording, no transcript** | Do not guess. `UNKNOWN — requires the transcript` on every quote slot, and cap the sentiment read at Low | Fabricating a quote |
| **A file at the wrong grain** (attendee list, ticket export, CRM dump) | Run it through `../../cs-context/scripts/ingest.py`, confirm any column mapped below 0.80 confidence, and use it only for the fields it actually covers | Treating a partial export as the full record of the call |
