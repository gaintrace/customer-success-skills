# Escalation Note — emit verbatim

> The customer-facing artifact. Emit the header above the divider, then the divider, then the
> fenced block. **Nothing above the divider is forwardable. Everything below it is send-ready as
> written** — no unfilled slot, no editorial note, no internal language.
>
> Slot names map to `../../cs-context/references/normalized-schema.md`. Every `<...>` carries a
> real name, number or date before this is emitted. Where a value is genuinely unavailable,
> **drop that sentence** and raise the gap above the divider as `UNKNOWN — requires <source>`.
> A block containing a placeholder is not send-ready.

---

## Internal header — above the divider

```markdown
**<account.name> · <S1|S2|S3|S4> · <variant> · <first note | update n | closure | review>**
**Send:** <channel> · from <sender name and role> · by <exact time, customer timezone> ·
call first: <yes — who and when, or no — why not> (`C26`) ·
**committed next update:** <exact clock time, customer timezone>
**Stripped under `R19`:** <each commitment removed, the gate it failed, and who must agree it
before it can be added — or "none: every commitment has a named owner who agreed the date in
writing">
**Coverage:** <X>/7 families (<Y>%) → <confidence>. <If below 60%: "no blast-radius figure
stated; the note gives the confirmed count and the time the full count lands.">
*<One line naming any default this ran on, or delete this line.>*
```

---

## The divider — reproduce exactly

```
════════════════════════════════════════════════════════════
CUSTOMER-FACING — copy the block below and send as written.
Everything above this line is internal. Do not forward it.
════════════════════════════════════════════════════════════
```

---

## The note — full form (first note or closure)

````
```text
Subject: <2–5 words, noun phrase, no question mark, no exclamation, no severity code,
no ticket ID>

<contact.name>,

<S1 · SITUATION — one sentence. Active verb, us as the actor, the capability in their
words, the window in their timezone, and a clause bounding the scope. No greeting above
it, no context, no apology, no defence.>

<S2 · IMPACT — their units first: jobs, claims, users, tenants, orders. Then their hours
with the arithmetic visible. Then money only if they can verify the rate, rounded to two
significant figures. Then the explicit boundary: what was NOT affected. The number is the
last sentence of its paragraph and nothing softens it (`C3`).>

<S3 · ROOT CAUSE — one of exactly two forms. Known: active voice, actor is "we", then the
ownership sentence. Unknown: the refusal to speculate plus the clock time you will know.
Never a named individual, never the customer, never a third party as a shield.>

<S4 · ACTIONS TAKEN — one line per action, each opening with a timestamp in their
timezone. Completed past-tense verbs only. Three to five lines.>
  <HH:MM tz> - <what was completed>
  <HH:MM tz> - <what was completed>
  <HH:MM tz> - <what was completed>

<S5 · ACTIONS COMMITTED — one line per commitment, each carrying one named human, one
calendar date and one observable outcome. Every line has passed all five gates in
SKILL.md Step 4. A line that failed a gate is deleted here and printed above the divider.>
  - <Name, role> - <what> - <date>
  - <Name, role> - <what> - <date>

<S6 · PREVENTION — what stops the CLASS of failure, not this instance. A control enforced
by a system, not by remembering. Where this is a repeat, say so before they do. Where you
cannot prevent it, say that plainly and give the realistic target. Omit this section
entirely on a first note where the cause is unknown.>

<S7 · NEXT UPDATE — an exact clock time in their timezone, with the "whether or not there
is news" clause. On a closure note this becomes the date the written review lands and who
sends it.>

<sender name>
<direct line>
```
````

---

## The note — update form

Four parts, sixty seconds, sent on the committed time whether or not there is news.

````
```text
Update <n> — <HH:MM, their timezone>.

<"No change since <last update time>" — or the one thing that changed.>

<What was ruled OUT since the last update. When nothing is fixed, this is the only honest
progress available.>

<What they should do. Usually "nothing needed from you." Never leave it blank — a customer
with no instruction invents one.>

Next update at <HH:MM tz>, whether or not there is news.
```
````

---

## The note — prevention receipt

Sent unprompted on the promised date, by the person who made the commitment.

````
```text
<contact.name> — <what shipped>, which I committed to on <date of the commitment>, went
live on <date>. <One sentence on what it now makes impossible.>

<How they can observe it working, and what it has caught since it landed.>

<"Nothing needed from you." — or the one thing that is.>

<sender first name>
```
````

Where the commitment **slipped**, the receipt is still sent on the promised date. It states the
slip, the new date, and the owner. A slipped receipt sent on time costs a fraction of a silent
one.

---

## Formatting rules inside the fence

Written for an email client, not a markdown renderer
(`../../cs-context/references/customer-voice.md`).

| Do | Not |
| --- | --- |
| Plain text; a blank line between paragraphs | Markdown headings — they arrive as literal hashes |
| `-` bullets indented two spaces, with a blank line before and after the list | Nested lists |
| Timestamps at line-start: `01:22 - <verb>` | Timestamps buried mid-sentence |
| Their timezone, named | Our timezone, or none |
| Real names, real dates, real numbers | `[Name]`, `[Date]`, `[Account]` |
| One fence per artifact, one artifact per fence | Two messages crammed into one block |
| A direct line in the signature | A no-reply address |
| Plain full stops | Exclamation marks, superlatives, emoji (`C27`) |

---

## Pre-emit gate

Do not emit until every line is true.

- [ ] Sentence one is the situation, and it survives being read with the thread above it deleted
- [ ] Impact leads in their units; the boundary of what was **not** affected is stated
- [ ] Any money figure shows its arithmetic and is rounded to two significant figures
- [ ] No blast-radius total where coverage is below 60% (`R23`)
- [ ] Root cause is active voice with "we" as the actor, or an explicit unknown with a clock time
- [ ] No individual named as the cause on either side; the customer is not blamed
- [ ] Every S4 line carries a timestamp; no progressive verbs outside S7
- [ ] Every S5 line carries a name, a date and an observable outcome, and passed all five gates
- [ ] No roadmap date, no "on the roadmap", no feature promise (`R19`)
- [ ] No credit, discount, term, renewal or expansion language (`R11`)
- [ ] Zero or one apology; any apology carries the number, a completed action and a next date
- [ ] Firewall scan run: no `risk` · `health` · `score` · `forecast` · `ARR` · `exposure` ·
      `save` · `tier` · `war room` · `P1` · `sev` (`R18`)
- [ ] Subject is a 2–5 word noun phrase with no severity code and no ticket ID
- [ ] Zero unfilled `<...>` slots anywhere inside the fence
- [ ] Forward test passed against their CFO, procurement lead, regulator and a competitor
