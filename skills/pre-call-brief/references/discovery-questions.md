# Discovery Questions

> Three per call. Not ten. Three questions asked properly, with silence after each one, move a
> relationship further than a list nobody gets through.
>
> **The test for a good question:** the customer can answer it and we cannot. Anything we could
> answer from our own data is a status question dressed as discovery, and asking it tells the
> customer we did not read our own systems before the call.

**Contents**
[The test](#the-test) · [The two gates](#the-two-gates) · [Anchors](#anchors) ·
[Regeneration table](#regeneration-table) · [By objective](#by-objective) · [By persona](#by-persona) ·
[By situation](#by-situation) · [Asking well](#asking-well) · [Banned questions](#banned-questions)

---

## The test

| Question | Verdict |
| --- | --- |
| "How's the rollout going?" | ❌ We can see the rollout in our own data |
| "Which team is furthest behind on the rollout, and what's blocking them?" | ✅ Only they know the blocker |
| "Are you happy with the product?" | ❌ Unanswerable in a way that helps anyone |
| "Of the three outcomes you named in January, which is furthest from where you wanted it?" | ✅ Specific, answerable, and it surfaces the real gap |
| "Any feedback for us?" | ❌ Puts the work on them and produces politeness |
| "What's the thing you've stopped bothering to tell us about?" | ✅ Names the category of feedback that never gets given |
| "Do you have budget for next year?" | ❌ Closed, and they will say yes |
| "When your CFO reviews this line item in November, what number will they want to see?" | ✅ Surfaces the real decision criterion |

---

## The two gates

Every generated question passes both gates before it reaches the brief. A question that fails
either is **regenerated, not reworded** — softening a bad question produces a longer bad
question. Three rejected questions produce three new ones; the brief never returns two questions
and a filler.

| Gate | What it rejects | The test | Why |
| --- | --- | --- | --- |
| **1 · Anchor** | "How's adoption going?" · "Are you happy with the product?" · "Any feedback for us?" · "How's the team finding it?" | The question contains at least one **anchor**: a date or month, a named event, a named team, or a named artifact. The anchor is printed beside the question in the brief. | People narrate a specific memory accurately and generalise inaccurately. "Generally" gets a social answer; "the last time" gets a fact. |
| **2 · Already answered** | "How many people are using it?" · "Did the integration get set up?" · "Are you still using the reporting module?" | The answer does not exist anywhere in the assembled brief. If a section of the brief answers it, the question is dead. | Asking what we can read says we did not read our own systems, and it spends the one thing a call gives us that data cannot — their reasoning. |

A question that passes gate 1 can still fail gate 2: *"Which teams got onto the new dashboard
after the June release?"* has an anchor and is answerable from product analytics. Rewrite it to
ask for the reasoning behind the fact rather than the fact: *"The Ops team got onto the new
dashboard after the June release and Finance didn't — what's different about how Finance works?"*

---

## Anchors

Four kinds count. Nothing else does.

| Anchor | Weak | Anchored |
| --- | --- | --- |
| **A time** — a month, a quarter, a dated event, "the last time" | "recently" | "since the July release" · "walk me through the last time this got in your way" |
| **An event** — a launch, an incident, a reorg, a board meeting, a renewal | "when things changed" | "after the 14 June outage" · "in the reorg you mentioned in March" |
| **A named team** — the department, not "the team" | "the users" | "the Finance team" · "Priya's analysts" |
| **A named artifact** — a report, a dashboard, a workflow, a ticket, a document | "the tool" | "the weekly exec report" · "the reconciliation workflow" · "the board deck you build in January" |

"The team" is not a named team. "Recently" is not a time. A question whose only specificity is
the customer's own company name is unanchored.

---

## Regeneration table

The rejected form, why it fails, and the same intent asked properly. Match the intent, take the
right-hand column.

| Rejected | Fails | Regenerated | Anchor |
| --- | --- | --- | --- |
| "How's adoption going?" | Gate 1 and gate 2 | "Which team hasn't got going since the March rollout, and what's in their way?" | Time + team |
| "Are you happy with the reporting?" | Gate 1 | "Walk me through the last time you built the monthly board report — where did it get slow?" | Event + artifact |
| "Any feedback for us?" | Gate 1 | "What's the thing your team has stopped bothering to tell us about?" | Named behaviour, not a general invitation |
| "How's the rollout going?" | Gate 2 | "Ops finished the rollout in May and Finance stalled — what's different about Finance?" | Time + two named teams |
| "Do you have budget for next year?" | Gate 1, and it is closed | "When Dana reviews this line in November, what number does she want to see next to it?" | Time + named person |
| "Are you still planning the expansion?" | Gate 1 | "What would have to be true by the October budget submission for the Finance team to come on?" | Event + team |
| "How was the incident handled?" | Gate 2 — we have the ticket | "After the 14 June outage, what did you have to tell your own stakeholders?" | Event |

---

## By objective

### To surface risk you cannot see

- "What would have to go wrong for this to not be renewed?"
- "If you had to cut one vendor this year, where would we rank and why?"
- "What's the thing your team complains about that never makes it into a support ticket?"
- "Who on your side would be the hardest to convince to keep this?"
- "What's changed on your side in the last quarter that we probably don't know about?"

### To surface value that has not been captured

- "What can your team do now that they couldn't twelve months ago?"
- "If this went away tomorrow, what breaks first?"
- "How would you describe what this does, to someone in your finance team?"
- "What number moved that you'd attribute to this, even partly?"

### To surface expansion

- "What would have to be true for you to bring the Finance team onto this next quarter?"
- "Which team asks you for access that you haven't given them yet?"
- "What are you still doing manually that surprises you?"
- "Where does this workflow hand off to something else, and what breaks at that handoff?"

### To surface the decision process

- "Who else has to be comfortable with this before it's signed?"
- "What did last year's renewal look like internally — was it straightforward?"
- "What's your budget cycle, and when does the number get locked?"
- "If you said yes today, what happens next on your side?"

### To surface the stakeholder map

- "Who else on your side would notice if this stopped working?"
- "Who's the person you'd want in the room for a quarterly review?"
- "Who was involved in the original decision who's still here?"

---

## By persona

| Persona | They are measured on | Ask about |
| --- | --- | --- |
| **Practitioner / end user** | Their own throughput and friction | "Walk me through the last time this got in your way." |
| **Team lead / manager** | Their team's output and their own visibility | "What does your manager ask you about that this could answer?" |
| **Director / VP** | A functional metric and a budget | "What's the number on your scorecard this year that this touches?" |
| **CFO / Finance** | Cost, risk, predictability | "How does a spend like this get justified in your process?" |
| **CIO / CTO** | Consolidation, security, integration burden | "Where does this sit in your consolidation plans?" |
| **Procurement** | Terms, leverage, precedent | "What does a straightforward renewal look like from your side?" |
| **Security / compliance** | Exposure and auditability | "What in our current setup would you flag in an audit?" |

Altitude matters more than seniority. A VP asked a practitioner question disengages; a
practitioner asked a strategy question guesses.

---

## By situation

### The account has gone quiet

One specific observation, one open question. Not "checking in".

> "Your team's activity in the reporting module dropped off in July after running steady since
> March. I'd rather ask than assume — did something change on your side, or is something not
> working?"

### A new stakeholder

- "What are you being measured on this year?"
- "What have you inherited here that you'd change?"
- "What do you already know about us — good and bad?"

### After a failure on our side

- "What did this cost you, actually?"
- "What would you need to see from us to stop worrying about it?"
- "Who else on your side is watching this, and what have they been told?"

### At renewal

- "What would make this an easy yes?"
- "What's the version of this conversation you're dreading?"
- "If the answer were no, what would the reason be?"

### Before an expansion ask

- "What's working well enough that you'd want more of it?"
- "Who's asked you for this that you've had to say no to?"

---

## Asking well

| Rule | Why |
| --- | --- |
| **Ask one question, then stop talking.** | The second half of the answer arrives after the silence. Filling it is the most common way a good question is wasted. |
| **Do not stack.** | "How's adoption going — and did you see the new release — and are we still on for October?" gets one answer to the easiest part. |
| **Follow the answer, not the list.** | The prepared third question is disposable if the second one opened something real. |
| **Ask about the specific, not the general.** | "The Finance team" beats "the team". A date beats "recently". |
| **Write the answer down verbatim.** | Their words go in the QBR, the success plan and the renewal case. Paraphrasing loses the language that persuades their colleagues. |
| **Ask the uncomfortable one last.** | It needs the trust the first two built. |

---

## Banned questions

| Banned | Why | Replace with |
| --- | --- | --- |
| "Just checking in — how's everything going?" | No content, no answer worth having | A specific observation and one question about it |
| "Do you have any questions for me?" | Puts the work on them | "The thing I'd want to know in your position is X — is that right?" |
| "Are you happy with the product?" | Politeness generator | "What's the one thing you'd change?" |
| "Is there anything else we can help with?" | Closes rather than opens | "What are you working on this quarter that we're not part of?" |
| "How's the team finding it?" | We can see this in the data | "Which team hasn't got going yet, and what's in the way?" |
| "Did you get my email?" | Wastes the opening of a live conversation | Assume not; restate the substance in one sentence |
| "Would you be interested in upgrading?" | An ask with no value case in front of it | Establish the value first, then make a specific, sized proposal |
