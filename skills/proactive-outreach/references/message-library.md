# The Message Library

> 21 complete, sendable messages, each showing exactly which data points it must pull in and where each one comes
> from. Copy the shape, never the sentences: a message reused verbatim across two accounts fails the swap test in
> `email-craft.md` §7.

**Contents**
1. [How to read a message](#1-how-to-read-a-message)
2. [Product usage & adoption — M1–M7](#2-product-usage--adoption)
3. [Commercial & contract — M8–M9](#3-commercial--contract)
4. [Relationship & engagement — M10–M13](#4-relationship--engagement)
5. [Support & reliability — M14–M15](#5-support--reliability)
6. [Sentiment & VoC — M16–M17](#6-sentiment--voc)
7. [Billing & payment — M18](#7-billing--payment)
8. [Firmographic & external — M19–M21](#8-firmographic--external)

---

## 1. How to read a message

Every placeholder is written as:

```
[LABEL · source system · normalised field · window]
```

If you cannot fill a placeholder from a real source, **do not fill it**: write `UNKNOWN — requires
<source>` in the artifact's Evidence table and cut the sentence that needed it. A message with an
invented number gets forwarded to their admin, checked, and remembered.

Field names come from `../../cs-context/references/normalized-schema.md`. Word counts are body only.
Every message obeys `email-craft.md`: 1–4 word lowercase subject, first line never begins with "I"
or "We", one ask, one exit.

**Register.** Each message below is `Standard` or **`Regulated`**. Regulated messages — M6, M14,
M16, M18, M20 here — obey `email-craft.md` §11: slot order acknowledgement → substance → ask, zero
exclamation marks, no superlatives, every sentence ≤ 20 words, one apology at most. The register is
computed from the trigger (SKILL.md Step 6), never chosen while writing.

**Customer-voiced Regulated messages — M14 and M16 — cannot be written without a verbatim.** If no
sentence of theirs exists in a ticket, a survey free-text or a transcript, the message is not sent:
the trigger is held under gate `C4 · acknowledgement source` and you retrieve the quote or phone
them. A paraphrase of someone's complaint, returned to them, makes it worse.

**Anchors.** Every ask names a date or window, an event, a team or an artifact (`email-craft.md`
§6.1). If your fill-in leaves a question with no anchor — "how's it going", "any feedback" — the
message is not ready. Rewrite the ask from the Evidence table.

---

## 2. Product usage & adoption

### M1 · U1 Usage drop — email · CSM → the team lead whose team dropped · window 7d · 71 words

> **Subject:** `the export job`
>
> [TEAM · Salesforce · contact.title / department mapping]'s scheduled exports went from [PRIOR_VOLUME · Amplitude
> · usage_daily.core_actions · mean/week, prior 30d] a week to [CURRENT_VOLUME · Amplitude ·
> usage_daily.core_actions · mean/week, last 30d] after [CHANGE_DATE · our release log or their config change ·
> date].
>
> Three explanations usually: the work moved somewhere else, someone left, or something broke on our side. The
> third one is ours to fix and I'd rather find out now than at your [QUARTER_END · cs-context §13 · fiscal
> calendar].
>
> Which is it? One word is enough.

**Fails if:** "your usage is down" with no team, metric, window or change date — or if you never checked whether *our* release caused it.

### M2 · U3 High-value feature never adopted — in-app first, email second · window 45d

**In-app (22 words), shown to `role = admin` only:**

> [FEATURE_NAME] cuts [OUTCOME_METRIC · their success plan · stated objective] — most teams set it up in under ten
> minutes. Show me how →

**Email follow-up, CSM → admin (68 words):**

> **Subject:** `the four day close`
>
> Back in [DATE · interaction.summary · the meeting or email where they said it] you said the goal was closing the
> month in [TARGET · their words, quoted] rather than [BASELINE · their words, quoted].
>
> [FEATURE_NAME] is the part of this that does that, and it's included in [PLAN · Salesforce · subscription.plan]
> — nobody on your side has switched it on [ZERO_USE_WINDOW · Amplitude · usage_event.event_name = X · 90d, count
> 0].
>
> Want me to set it up with [ADMIN_NAME] on a 20-minute call, or send the two-step version?

**Fails if:** the email is about the feature rather than about the outcome they already named.

### M3 · U4 New admin provisioned — Slack Connect · CSM → the new person, cc the inviter · window 14d · 3 lines

> Welcome [NAME · product analytics · contact.name · first_seen_product within 7d] 👋
>
> Two things worth knowing on day one: [ACCOUNT] has been on [PRODUCT] since [START · Salesforce ·
> subscription.start_date], and the thing your team uses it for most is [TOP_WORKFLOW · Amplitude ·
> usage_event.event_name · top by volume, 90d].
>
> If you want the 15-minute version of how it's set up here, say the word — otherwise I'll stay out of your way.

**Fails if:** a generic onboarding drip that ignores the 14 months of account history they just inherited.

### M4 · U6 Milestone reached — email · CSM → champion, cc exec sponsor · window 14d · 79 words

> **Subject:** `the four day close`
>
> [MONTH]'s close ran in [ACTUAL · their system or ours · the metric they defined] against the [BASELINE · success
> plan · their stated starting point] you started from in [BASELINE_DATE] — the target [SPONSOR_NAME] set when
> this was approved.
>
> [SUPPORTING_METRIC · Amplitude · usage_daily.core_actions · window] sits behind it: [SECOND_DATA_POINT].
>
> The next milestone on the plan is [NEXT_MILESTONE · success plan], and the one thing standing in its way is
> [BLOCKER · observed]. Want 20 minutes to decide whether that's worth doing this quarter?

**Fails if:** you congratulate them on *our* metric. Send inside the 14-day momentum window `[P]` or it becomes history.

### M5 · U7 Activation not reached by day N — phone first, email if no answer · window 21d

**Phone opener (say this, then stop talking):**

> "[NAME], you signed on [START_DATE] and the [ACTIVATION_EVENT · cs-context §5] still hasn't run. That's normally
> one of three things — the data connection, an approval, or nobody's had time. Which one is it?"

**Email fallback (61 words):**

> **Subject:** `the connector`
>
> [DAYS · today − subscription.start_date] days in and [ACTIVATION_EVENT · cs-context §5 · usage_event count = 0]
> hasn't run yet — the last thing logged was [LAST_STEP · usage_event.event_name · max timestamp] on
> [LAST_STEP_DATE].
>
> That step usually stalls on [COMMON_BLOCKER], which takes us about [FIX_DURATION] to clear from our side if you
> can get [REQUIRED_ACCESS] approved.
>
> Can I book [DAY] to finish it, or is the timing wrong?

**Fails if:** you send "how's onboarding going?" They are stuck. Asking is not helping.

### M6 · U9 Integration broken — Slack Connect, else phone · window 48h · 3 lines · **Regulated · we-found-it**

> [INTEGRATION_NAME] has been failing since [BREAK_TIME · integration logs · integration_disconnected or
> auth-failure events · timestamp] — [FAILURE_COUNT] failed syncs, which means [DOWNSTREAM_EFFECT · what stopped
> working for them].
>
> Cause is [CAUSE · observed], fix is [FIX], and [OWNER] has it. ETA [ETA · committed, not estimated].
>
> Nothing needed from you unless [REQUIRED_ACTION], in which case I'll call.

**Fails if:** you wait for them to report it. They attribute the lost days to you either way; the only variable is who found it first. Slot 1 is the break and what stopped working for them — the cause comes after it, never before (C4). No exclamation marks, no "we're on it!" (C27).

### M7 · U10 Shelfware — right-size offer · email · CSM or AM → economic buyer · window 45d · 74 words

> **Subject:** `worth right-sizing?`
>
> [SEATS · Salesforce · subscription.seats_purchased] seats are contracted and [ACTIVE · Amplitude ·
> distinct_users_30d · 30d] have been used in the last 30 days — [GAP] sitting idle for [DURATION · usage_daily ·
> sustained window].
>
> Two honest options before [OPT_OUT · subscription.opt_out_deadline]: bring the unused [GAP] onto the platform,
> which takes about [EFFORT] and I can run it, or reduce the count at renewal and stop paying for them.
>
> Which do you want to plan for?

**Fails if:** you hide it and hope the renewal closes first — their procurement runs the same report.

### M8 · C1 Opt-out courtesy notice, T−120 — email · CSM → champion, cc economic buyer · window 14d · 76 words

> **Subject:** `november deadline`
>
> [ACCOUNT]'s agreement renews on [RENEWAL · Salesforce · subscription.renewal_date], and the notice deadline
> before that is [OPT_OUT · subscription.opt_out_deadline] — [DAYS · opt_out_deadline − today] days out. Flagging
> it in writing so it isn't a surprise from either direction.
>
> Two things worth settling before then: the [SEAT_DELTA · subscription.seats_purchased change · date] added in
> [MONTH], and whether [OPEN_ITEM · success plan or ticket] landed the way you needed.
>
> Half an hour in [WEEK], or would you rather I send the written summary first?

**Fails if:** you let the window pass quietly so it auto-renews. Real leverage, and the fastest way to lose a reference account and the renewal two years out.

### M9 · C2 Discount expiring — email · AM → economic buyer · window 45d · 71 words

> **Subject:** `the february rate`
>
> The [DISCOUNT_PCT · Salesforce · subscription.discount_pct] discount on [ACCOUNT]'s agreement runs out on
> [EXPIRY · subscription.discount_expires], which puts the [RENEWAL_DATE] renewal at [LIST_ANNUAL] rather than
> [CURRENT_ANNUAL] if nothing changes.
>
> Raising it now rather than in the negotiation, because your finance team will find it either way and I'd rather
> we both had the same number.
>
> Want the two structures that keep it flat, or the honest version of why the rate moved?

**Fails if:** their finance team finds the cliff first. That conversation starts from distrust.

### M10 · R1 Champion departure — email · CSM → next-most-senior known contact · window 48h · 69 words

> **Subject:** `covering for jamie`
>
> Mail to [DEPARTED · contact.email · email_status = hard_bounce · bounce date] came back undeliverable this week,
> so it looks like [FIRST_NAME] has moved on.
>
> Three things they were carrying that shouldn't drop: [ITEM_1 · commitment log · interaction.commitments],
> [ITEM_2], and the [RENEWAL_OR_MILESTONE · subscription.opt_out_deadline] on [DATE].
>
> Who's picking those up? Happy to run through the current state with whoever it is — 20 minutes, no prep needed
> on your side.

**Fails if:** you speculate about why they left, or email the bounced address again. Send in
parallel with M11 when the account warrants exec cover — that pairing is a rung 1 + rung 3 pair,
not an escalation over time (`cadence-design.md` §5).

### M11 · R2 Exec sponsor change — email drafted for the VP CS to send · VP CS → the new leader · window 7d · 82 words

> **Subject:** `what you inherited`
>
> [PREDECESSOR_NAME] brought [PRODUCT] into [ACCOUNT] in [START · subscription.start_date] to [ORIGINAL_OBJECTIVE
> · their words from the original business case, quoted with the date].
>
> Where that stands today: [OUTCOME_METRIC_1 · their units · with baseline and current] and [OUTCOME_METRIC_2].
> [ADOPTION · Amplitude · distinct_users_30d] people across [TEAM_COUNT] teams use it weekly.
>
> New leaders inherit line items without the context behind them. Twenty minutes to give you that context — or the
> one-page version by email if that's more useful. Either is fine.
>
> [VP_NAME], VP Customer Success

**Fails if:** it assumes the new leader knows what you are. They do not, and their default in a
first quarter is to review every line item nobody explained to them. The two-message shape — VP CS
email first, then the CSM email — is a practitioner convention `[P]`, and the reason it is ordered
that way is that the new sponsor has no relationship to spend, so the title is doing the work of
the introduction. Copy the structure; no reply-rate claim attached to it is worth quoting.

### M12 · R3 Silence, 60 days — email touch 1 · CSM → champion · window 30d · 66 words

> **Subject:** `two things`
>
> Two months since we last spoke, and two things moved in that time that you'd probably want to know about.
>
> [CHANGE_1 · e.g. usage: PRIOR → CURRENT · Amplitude · usage_daily · 60d] and [CHANGE_2 · e.g. a shipped request,
> a resolved escalation, a new user cohort · source · date].
>
> The first one is the reason I'm writing — [ONE_LINE_IMPLICATION].
>
> Worth 20 minutes, or is quiet the right setting for now? Both are fine answers.

**Fails if:** it opens with "just checking in" or apologises for the silence. The message is what changed inside the silence.

### M13 · The permission close — email touch 3, any cadence · CSM → same recipient · 54 words

> **Subject:** *(reply in the existing thread — no new subject)*
>
> Three weeks of no reply usually means this isn't near the top of the list, which is a completely fine answer and
> more useful to me than a maybe.
>
> [THE_FACT · restated in one clause] is still true, so it stays on my list either way. Reply "later" and I'll
> stop raising it until something changes. Reply "wrong person" and I'll find the right one.
>
> Nothing needed otherwise.

**Fails if:** it says "circling back", "bumping this" or "third attempt" — or if we owe them something, where the outstanding commitment is the message.

---

## 5. Support & reliability

### M14 · S1 Escalation resolved — email · CSM → the person who escalated, cc their manager · window 14d · 84 words · **Regulated · customer-voiced**

> **Subject:** `what changed`
>
> "[VERBATIM · Zendesk · the sentence they wrote when they escalated, quoted exactly]" — that was
> [ESCALATOR_NAME] on [DATE · ticket.escalated_at].
>
> [TICKET_ID · Zendesk · ticket_id] closed on [RESOLVED · ticket.resolved_at] after [DURATION · resolved_at −
> created_at] and [REOPEN_COUNT · ticket.reopened_count] reopens. That was longer than it should have been. The
> reason was [HONEST_CAUSE].
>
> Two things changed on our side so it doesn't repeat: [FIX_1] and [FIX_2 · with owner and date].
>
> What I still owe you is [OUTSTANDING_COMMITMENT · interaction.commitments], by [COMMITTED_DATE].
>
> Still open from [ESCALATION_WINDOW · dates] that I've missed — [NAMED_WORKSTREAM · the thing their team was
> doing while it was broken] in particular?

**Fails if:** it contains a commercial ask. The cooldown is 14 days after a Sev-1 and 30 days after
an escalation closes `[P]` — asking inside that window reads as extraction. It also fails if it
opens on the ticket rather than on their sentence: no verbatim on record means the message is held
under gate `C4 · acknowledgement source`, not written from our summary of what they meant.

### M15 · S3 Ticket requesting a higher-tier capability — email · CSM → the requester, cc the admin · window 7d · 73 words

> **Subject:** `sso`
>
> [REQUESTER_NAME] asked support for [CAPABILITY · Zendesk · ticket body, quoted] on [DATE · ticket.created_at] —
> the answer they got was that it isn't in [PLAN · Salesforce · subscription.plan], which is technically right and
> not very helpful.
>
> What it would actually take: [WHAT_IT_INVOLVES], and the reason it matters for you specifically is
> [THEIR_STATED_DRIVER · their words from the ticket].
>
> Want the number and the two ways to structure it, or should I loop in [AE_NAME] directly?

**Fails if:** it is routed silently to Sales and a cold AE calls three days later. The requester asked *you* — this is the highest-intent trigger in the catalog.

---

## 6. Sentiment & VoC

### M16 · V1 NPS detractor — phone if a number exists, email otherwise · CSM → the respondent · window 24h · 64 words · **Regulated · customer-voiced**

> **Subject:** `your survey answer`
>
> "[VERBATIM · survey tool · their free-text response, quoted exactly]" — that was [RESPONDENT_NAME]'s answer on
> [DATE · survey response timestamp], and it deserves a real reply rather than an automated one.
>
> On [ISSUE_1], [WHAT_WE_WILL_CHANGE] by [DATE · committed]. On [ISSUE_2], [HONEST_ANSWER — including "we are not
> going to fix that, and here is why"].
>
> Fifteen minutes this week to go through [ISSUE_1] and [ISSUE_2] properly so I get the rest right?

**Fails if:** it is an autoresponder — a detractor who gets a "sorry to hear that" template has now been ignored twice. Close the loop even when the answer is that you will not fix it. No verbatim on record means no message: hold it under gate `C4 · acknowledgement source` and phone them instead (C4). Zero exclamation marks, no "really appreciate the feedback" (C27).

### M17 · V3 NPS promoter — email · CSM → the respondent, cc champion · window 14d · 57 words

> **Subject:** `your nine`
>
> "[VERBATIM · survey tool · free text, quoted]" — thank you, and specifically thank you for
> [THE_SPECIFIC_THING_THEY_NAMED].
>
> One ask, and only one: [CHOOSE EXACTLY ONE — an introduction to [ADJACENT_TEAM · CRM · unengaged department], 20
> minutes for a written case study, or a reference call for a company in [THEIR_VERTICAL]].
>
> No if the timing's wrong — it won't change anything on my side.

**Fails if:** it stacks an advocacy ask and an expansion ask. Ask separation is 14 days minimum `[P]`, and the momentum window is 14 days.

---

## 7. Billing & payment

### M18 · B2 Invoice overdue 30 days — email · CSM → champion, not the AP inbox · window 14d · 59 words · **Regulated · we-found-it**

> **Subject:** `invoice 4471`
>
> Invoice [INVOICE_ID · Stripe · invoice_id] from [ISSUED · invoice.issued_at] is [DAYS_LATE · today −
> invoice.due_at] days past due — [AMOUNT · invoice.amount]. Every invoice before it cleared on time
> [PAYMENT_HISTORY · Stripe · invoice.paid_at vs due_at · 12 prior invoices].
>
> Two possibilities: it's stuck in a process, or somebody put a hold on it. Both are fine to say out loud, and the
> second one I'd much rather hear from you than work out later.
>
> Which is it?

**Fails if:** it goes to collections before anyone asks the champion. A first late payment after eleven clean quarters is a commercial signal, not an administrative one.

---

## 8. Firmographic & external

### M19 · X1 Funding round — email · CSM → champion · window 30d · 62 words

> **Subject:** `your series c`
>
> Congratulations on the [ROUND · Crunchbase or press · round name and amount] — announced [DATE].
>
> Rounds usually come with a hiring plan, and the practical version of that here is [CURRENT_SEATS · Salesforce ·
> subscription.seats_purchased] seats with [HEADROOM · seats_purchased − distinct_users_30d] spare.
>
> Not asking for anything today. What's the shape of the next two quarters, so I can make sure the setup doesn't
> become the bottleneck?

**Fails if:** it proposes an expansion. Everyone else in their inbox did that on the same morning, which is exactly why restraint works.

### M20 · X3 Layoffs or restructuring — email · CSM → economic buyer · window 30d · 68 words · **Regulated · we-found-it**

> **Subject:** `cost per close`
>
> Saw the news on [EVENT · press · date]. Not going to pretend to know what it means internally.
>
> What it usually means for a line item like this one is a per-dollar review, so here is our side of it in
> advance: [OUTCOME · their units · with baseline and current] for [ANNUAL_COST · Salesforce · subscription.arr],
> which works out at [UNIT_ECONOMIC · derived · show the arithmetic].
>
> If right-sizing is the right call, I'd rather help you do it properly than defend the number. Want the workings?

**Fails if:** it is an adoption message. Their problem is cost; an adoption nudge says you did not read the news.

### M21 · X7 Peer success story — email · CSM → champion · window 60d · 70 words

> **Subject:** `how [PEER] did it`
>
> [PEER_COMPANY · with their permission, or anonymised as "a [SIZE] [VERTICAL] company"] had the same
> [SHARED_CONSTRAINT] you described in [DATE · interaction.summary · quoted].
>
> What they changed: [SPECIFIC_MECHANISM — the actual configuration or process, not the outcome]. Result was
> [RESULT · their number, with the window].
>
> Of the [N · your own cohort data · state n] companies in [THEIR_VERTICAL · account.industry] on the platform,
> [K] run it this way.
>
> Worth 20 minutes with the person who built it there?

**Fails if:** it says "most customers your size buy X". Social proof without a stated mechanism is a pitch — name the mechanism or do not send.

---

## Cross-reference

| Need | Go to |
| --- | --- |
| The trigger's condition, channel, sender, window and anti-pattern | `trigger-catalog.md` |
| Subject-line patterns, the first-line rule, CTA ranking, banned phrases | `email-craft.md` |
| The same message at four altitudes (practitioner → CFO) | `email-craft.md` §8 |
| Touch spacing, escalation ladder, stop rules, holdout design | `cadence-design.md` |
| Provenance, evidence tiers, internal vs customer-facing language | `../../cs-context/references/evidence-standard.md` |
