# Customer Recap — emit verbatim

> Customer-facing. Assembled only from lines tagged `SHARE` or `TRANSLATE` in Step 4.
> Emit it exactly as laid out below: the divider first, then **one** ```text fence containing
> nothing but send-ready text. Formatted for an email client, not a markdown renderer — plain
> text, a blank line between paragraphs, `•` bullets, aligned columns where a table is
> unavoidable, no markdown headings, no pipe tables, no `**`.
>
> **No unfilled placeholders inside the fence.** Every `<...>` below is a slot you fill or a
> sentence you delete. If a name or a date is genuinely unavailable, drop that sentence and
> raise `UNKNOWN — requires X` *above* the divider. A block containing `[Name]` is not
> send-ready, and a template that looked finished is the commonest way one reaches a customer.
> Run the Step 9 leak scan before emitting. Full standard:
> `../../cs-context/references/customer-voice.md`.

---

## Distribution — record this above the divider, not inside the fence

**To:** everyone who attended, including their silent attendees
**Cc:** only people already in the thread, plus your exec if the email names them as an owner
**Send by:** call end + 24 hours — same day for renewal and expansion, 4 hours for escalation

---

## The block

````
════════════════════════════════════════════════════════════
CUSTOMER-FACING — copy the block below and send as written.
Everything above this line is internal. Do not forward it.
════════════════════════════════════════════════════════════

```text
Subject: <account name + the single decision made or the thing owed>

Hi <first name>,

<Opening line. One sentence. The single most useful thing that came out of the
call. Not "thanks for your time". Not a summary of the agenda. Not starting
with "I".>

Decided today:
  • <Something that is settled now and was open before the call.>
  • <Decision.>

  <Delete this whole block if nothing was decided. Never manufacture one.>

Who owes what:
  • <Their named person> — <observable action in their verb>, <weekday + date>
  • <Your named person> — <observable action>, <weekday + date>

  <Grade A and B commitments only. A named human in every line — never "the
  team". A calendar date in every line — never "next week". If you assigned a
  name or a date the customer did not state, add the sentence below so they
  can correct it.>

  <"I've put names and dates against the two we left open — tell me if either
  needs to move.">

Still open:
  • <The unanswered question, in plain terms> — <named person>, by <date>

  <Include questions you asked and did not get answered, phrased neutrally.
  Delete the block only if there are genuinely none.>

Next session: <day date time> or <day date time>. <One line on the purpose.>

<Sign-off, first name. One ask maximum, already stated above.>
```
````

---

## Before you emit — the leak scan

Delete or rewrite any hit. Softening is not a fix; it leaves the shape of the internal language
visible.

| Scan for | Examples |
| --- | --- |
| Risk vocabulary | risk, at-risk, churn, escalation, save, red, health score, exposure, tier |
| Forecast vocabulary | commit, best case, close date, forecast, pipeline, quota |
| Dollars not agreed on the call | ARR, exposure, a discount you have not been approved to offer |
| Characterisation of their people | "since Dana has been disengaged", "your procurement team is slow" |
| Third parties they did not name | Competitors, partners, other customers |
| Ungraded commitments | Anything that was "that sounds interesting" on the call |
| Someone not on the thread | Any sentence about a person who was not in the room |
| Second ask | Count the asks. More than one and the extras move to the next conversation |
| Banned warmth filler | "just checking in", "touching base", "circling back", "hope you're well", "as per my last email", "reaching out", "we value your partnership", "let me know your thoughts", "at your earliest convenience", "drive adoption", "leverage" |
| Unfilled placeholder | Any `<...>` or `[...]` still inside the fence |
| Markdown that will not survive | `**bold**`, `##` headings, pipe tables |

## Variants

| Situation | Change | Detail |
| --- | --- | --- |
| More than 48h late | Name the lateness in line 1; ask for correction rather than confirmation | `../references/recap-templates.md` §10 |
| They committed to nothing | Our commitments only, plus one dated low-cost ask | §11 |
| The call went badly | Internal note and escalation first; named approver; 2–4h cool-down; acknowledge, do not defend | §6 |
| Renewal | Lead with the **opt-out deadline**, not the renewal date | §5 |
| QBR | Lead with their objectives in their numbers, including the one that is behind | §4 |
| Technical review | Defect list with issue keys; `UNKNOWN` for any date engineering has not agreed | §8 |
| New or difficult relationship | Adjust the register before adjusting the structure | §15 |
