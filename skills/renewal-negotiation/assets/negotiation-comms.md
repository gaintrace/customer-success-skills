# Negotiation Comms — the five drafts

> Emitted at Step 10. Only the draft due now goes in the pack; all five live here.
> Every draft below has been run through `../scripts/pre_send_scan.py` and exits 0.
>
> **Before any of these is written**, run `scripts/concession_math.py gates`. Where Gate A fails,
> Draft 2's authority-test paragraph is the whole reply. Where Gate B fails, **Draft 0 goes first
> and no commercial reply leaves until the business meeting is booked** (`C10`).

**The firewall (`R18`).** Never in customer text, in any wording: the walk-away, the ladder rung
or the word "concession", the approval band, health or risk band, revenue at risk, exposure,
forecast category, save play, coverage tier, the precedent note, competitor intelligence they did
not raise, or any assessment of a named person on their side.

**The two construction rules**, both mechanical, both scanned:

- **`C13` · Announce, do not ask.** No question mark and no request construction in the paragraph
  that carries the price.
- **`C3` · Say the number, then stop.** Justification precedes the number. The number is the last
  thing in its paragraph. Nothing follows it.

Questions are legitimate — the authority test in Draft 2 is one. They live in their own
paragraph, away from the number.

---

## Draft 0 — the business-thread re-opener

**Due when Gate B fails: procurement is active and `days_since_business_thread` is over 21.**
Goes to the economic buyer, not to procurement. Copy procurement in — the rule is a second
thread, not a secret one. Contains no price, no terms and no ask.

════════════════════════════════════════════════════════════
CUSTOMER-FACING — copy the block below and send as written.
Everything above this line is internal. Do not forward it.
════════════════════════════════════════════════════════════

```text
Subject: Your ops team's numbers since the March rollout

Hi Dana,

Separate from the paperwork Priya and I are working through — your ops team went from
11 weekly users in March to 34 last week, and they are now running the weekend
reconciliation in the tool rather than in the spreadsheet Marcus built.

I would like 30 minutes with you and Marcus on what you want that to look like in Q1.
Two things I want to put in front of you: the three teams that have not started, and the
audit-log rollout that is still open on the plan.

Thursday 2pm or Monday 10am both work my end.

Jo
```

---

## Draft 1 — the uplift notification

**Due at T-90, alongside the proposal.** Never inside the notice window for the first time
(`R1`). Justification first, number last, notice date named in plain words.

════════════════════════════════════════════════════════════
CUSTOMER-FACING — copy the block below and send as written.
Everything above this line is internal. Do not forward it.
════════════════════════════════════════════════════════════

```text
Subject: Northwind 2027 term — pricing and your notice date

Hi Dana,

Two things changed since we set the current price. Your named users went from 180 to 264
between January and July, and the audit-log export your security team asked for in March
shipped in May and now runs on every Okta sync. The annual fee for the 2027 term is
$514,000.

That takes effect on 1 March 2027. Your notice deadline under the current agreement is
1 December 2026, and I am putting it in writing so it sits on your calendar rather than
mine.

The order form and the per-team usage detail sit behind the number. I have held Thursday
11am and Friday 9am to walk through either with you and Priya.

Jo
```

---

## Draft 2 — response to a discount request

**Structure: acknowledge · authority test · the counter with its trade · the date · the next
step.** The authority test is its own paragraph and comes *before* the number (`C14`). The
counter names what we get in the same breath as what we give (`C12`).

════════════════════════════════════════════════════════════
CUSTOMER-FACING — copy the block below and send as written.
Everything above this line is internal. Do not forward it.
════════════════════════════════════════════════════════════

```text
Subject: Re: 2027 renewal — where I can and cannot go

Hi Priya,

Thanks for putting the number on the table plainly. It makes this faster for both of us.

One question before I take anything to our commercial team. If I could get a number
approved, is this something Dana could sign this quarter?

On the substance: twenty points is not a number I have, and I would rather say that now
than spend three weeks arriving at it. What I do have is structure. On a 24-month term
paid annually in advance, the 2027 fee is $442,000.

That structure is what makes the number work, so the two move together. The figure stands
until 30 September, when our order forms are cut for the March term.

I am sending the per-team usage report separately so you and Dana are working from the
same numbers I am.

Jo
```

---

## Draft 3 — response to a downgrade request

**Send this only after the five downgrade tests in Step 9.** Where the request is genuine
right-sizing, take it well: right-size to real usage plus a named buffer, trade the reduction,
and put the recovery path in the paper.

════════════════════════════════════════════════════════════
CUSTOMER-FACING — copy the block below and send as written.
Everything above this line is internal. Do not forward it.
════════════════════════════════════════════════════════════

```text
Subject: Re: seat count for the 2027 term

Hi Dana,

You are right that the count is wrong. 264 seats are provisioned and 171 have signed in
during the last 60 days, and the gap is almost all in the two teams that moved to
Manchester.

Here is what I would do rather than cut to 171. Right-size to 190, which covers today plus
the twelve people Marcus is hiring into ops before April, so you are not raising a change
order in month three. On a 24-month term the 2027 fee is $362,000.

Two things I would like in the same paper. Any seats you add during the term come in at
that same per-seat rate rather than at list, and we schedule the quarterly review with
Marcus so the count gets checked before it drifts again.

I will have the revised order form to you Thursday.

Jo
```

---

## Draft 4 — the best-and-final / artificial-deadline response

**A best-and-final is conditional on a named signature date and a named get, or it is simply a
lower price.** Where the deadline appears in no contract, re-anchor on the date that does exist.

════════════════════════════════════════════════════════════
CUSTOMER-FACING — copy the block below and send as written.
Everything above this line is internal. Do not forward it.
════════════════════════════════════════════════════════════

```text
Subject: Re: best and final by Friday

Hi Priya,

I can give you a final number. It comes with two conditions, and I want to be straight
that they are conditions rather than preferences.

The first is a signature date. The second is the 24-month term we discussed on Tuesday.
With both of those, the 2027 fee is $442,000.

On Friday: that date is not in either of our agreements. The date that is in yours is
1 December, which is your notice deadline for the March term, and there are eleven weeks
between the two. If the eleven weeks are genuinely needed on your side, a 60-day extension
at current terms is available and I would rather do that than have either of us work to a
date neither contract mentions.

Tell me which of the two you want and I will have paper out the same day.

Jo
```

---

## The pre-send routine

1. Save the fence contents to a file.
2. `python3 scripts/pre_send_scan.py draft.txt` — exit 0, or rewrite. Softening a hit leaves the
   shape of it visible.
3. Run the eight-step leak scan in `../../cs-context/references/customer-voice.md`.
4. Read the first three lines aloud. If they sound like a vendor, rewrite them.
5. Check every slot is filled. A block containing `[Name]` is not send-ready — drop the sentence
   and raise `UNKNOWN — requires X` above the divider instead.
