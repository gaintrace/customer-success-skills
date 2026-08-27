# Coverage Change Notes — customer-facing blocks

> A coverage change is one of the few internal decisions a customer experiences directly. These are
> the send-ready blocks for the three cases that occur, plus the rules that keep them from leaking.
>
> Read `../../cs-context/references/customer-voice.md` before editing any of them.

---

## The firewall, applied to coverage

**Never appears in customer-facing text, in any wording, however softened:** tier · book · pool ·
pooled · tech-touch · digital touch · coverage model · cost to serve · ARR · segment · "your account
no longer qualifies" · "accounts of your size" · headcount · capacity · any reason grounded in what
they spend.

| Internal | What the customer gets |
| --- | --- |
| "Moving to pooled coverage" | The new route to help, the response time attached to it, and what stays with a named person |
| "Below the named-CSM ARR floor" | *(never — the economics are not translatable)* |
| "Rebalancing for territory coverage" | "Sam is taking this on, and here is why they are the right fit" — said live by the outgoing CSM |
| "Reducing EBR entitlement from 4 to 2" | Two dates, already booked, plus the written summary that fills the gap |
| "We are short-staffed" | *(never — it is our problem, not theirs, and it invites them to plan around it)* |

**Three rules that decide whether this lands.**

1. **Lead with what genuinely improves.** There is almost always something real: a faster first
   response, cover during leave, specialists on product questions. If there is honestly nothing
   better, do not invent it — say what stays the same and who to contact.
2. **Name what stays with a human.** The renewal, the escalation path, the live project.
3. **Never dress a reduction as an upgrade.** Customers recognise it immediately, and the
   credibility cost is larger than whatever the change saved.

**Before sending, run the leak scan** in `../../cs-context/references/customer-voice.md`: vocabulary,
numbers the customer can verify, named people, inference phrased as a question, commitments with
internally-agreed owners, and the forward test.

**No placeholders.** Every block below is filled with real values in the example. If a name or date
is genuinely unavailable, delete that sentence and raise the gap above the divider as
`UNKNOWN — requires X`. A block containing `[Name]` is not send-ready.

---

## Block 1 — Named coverage moves to a shared team

Use when an account moves from a named CSM to a pooled or digital model. Send it from the outgoing
CSM, at least three weeks before the change, and hold a fifteen-minute call first if the ARR
warrants it.

````
════════════════════════════════════════════════════════════
CUSTOMER-FACING — copy the block below and send as written.
Everything above this line is internal. Do not forward it.
════════════════════════════════════════════════════════════

```text
Subject: Your Northwind support setup from 1 October — faster answers

Hi Dana,

From 1 October, questions from your team go to success@ourcompany.com rather than
to me directly, with a first response inside four working hours. Our median this
year has been about a day and a half.

What that changes for you:

  • Anyone on your team can raise something. Today it routes through Marcus and
    stalls whenever he is on leave.
  • Product and billing questions reach someone who works on them every day.
  • The October upgrade session and the quarterly usage summary are unchanged.

Staying with me: your March renewal, the SSO rollout, and anything that needs a
decision rather than an answer. I am on the first two sessions so nothing has to
be re-explained.

Anything you would rather keep coming straight to me? Tell me before Friday and I
will set it up that way.

Thanks — I know October is your close month.

Jo
```
````

**Why it works:** it opens with the concrete mechanism, quantifies the improvement with a number the
customer can check against their own experience, names what does not change, keeps a human attached
to the commercial conversation, and offers a small, dated way to push back. No tier, no economics, no
apology.

---

## Block 2 — CSM reassignment

Use for a rebalance, a resignation or a territory change. Send it **after** the live three-way
introduction, never instead of it. From the outgoing CSM.

````
════════════════════════════════════════════════════════════
CUSTOMER-FACING — copy the block below and send as written.
Everything above this line is internal. Do not forward it.
════════════════════════════════════════════════════════════

```text
Subject: Priya is taking over from me on Northwind — from 15 September

Hi Dana,

Following our call on Tuesday: Priya Raman picks up Northwind from 15 September.

Priya has spent two years on manufacturing accounts here and has run the exact
multi-entity rollout you are part-way through — the intercompany step you and I
kept circling is one she has solved twice.

She already has: the Q3 close timings, the open question on audit-log export that
Ravi is checking, and the March renewal date with your 60-day notice on it. She
will not ask you to explain the last eighteen months.

Your first session with Priya is Thursday 18 September at 2pm — same slot we use.
I am on that call, then I step back.

It has been a genuinely good three years. You pushed us on the export limits and
you were right; that work shipped because of you.

Jo
```
````

**Why it works:** it names the successor's specific relevance rather than praising them generically,
proves continuity by listing three things already transferred, keeps the existing meeting slot,
and closes with something true and particular rather than a thank-you formula. Critically, it does
**not** say "due to a territory realignment" — the customer does not care and it invites the
question of whether they were downgraded.

---

## Block 3 — Cadence reduces, named coverage stays

Use when business-review frequency or cadence-call frequency changes but the named CSM does not.
The failure here is silence: cadence quietly stops and the customer notices at renewal.

````
════════════════════════════════════════════════════════════
CUSTOMER-FACING — copy the block below and send as written.
Everything above this line is internal. Do not forward it.
════════════════════════════════════════════════════════════

```text
Subject: Northwind reviews for 2027 — two live sessions, plus a monthly summary

Hi Dana,

Planning next year's rhythm with you. Two live reviews rather than four: 12 March
and 10 September, both already in your calendar, both an hour.

Between them you get a written summary on the first Tuesday of each month —
usage by team, what changed, and anything I think you should look at before it
becomes a problem. That is new, and it is more frequent than the quarterly deck.

The reason for two rather than four: last year's June and December sessions ran
twenty minutes and neither produced a decision. The March and September ones both
did — March set the multi-entity plan, September moved the renewal timing.

If something needs an hour in between, ask and you have it. Nothing about how you
reach me changes.

Does 12 March still work, or should I move it clear of your close week?

Jo
```
````

**Why it works:** it gives a reason grounded in the customer's own meeting history rather than in our
capacity, it replaces what it removes with something more frequent, it keeps the door open, and it
ends with a closed question that is easy to answer. It never mentions hours, cost or entitlement.

---

## What not to send

| Draft | Why it fails |
| --- | --- |
| "As part of a segmentation review, your account has been moved to our scaled coverage model." | Names the model and the review. Reads as "you were downgraded", because you were |
| "We're excited to announce an enhanced digital-first experience!" | Dresses a reduction as an upgrade. Customers decode this in one read and remember it |
| "Due to capacity constraints we're consolidating coverage." | Our problem, presented as theirs. Invites them to plan for less |
| "Your new CSM will reach out shortly to schedule an introduction." | No name, no date, no reason to be reassured. The handover has already failed |
| "Nothing will change." | Something will change. Saying otherwise costs the trust you need when it does |
| Silence | The most common approach, and the worst. The customer discovers it when they need something |
