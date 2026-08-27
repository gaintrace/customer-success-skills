# Pre-Call Note

> The short message sent **before** the call, when the call is more than 24 hours away or the
> agenda was never confirmed. Omit it entirely when the call is inside 24 hours and the agenda
> is already agreed — a note that adds nothing is a small withdrawal from the relationship.
>
> Customer-facing. Everything in the brief above the divider stays internal: no health band, no
> risk language, no ARR, no forecast, no authority field, no pre-wire status, no calendar
> signal. See `../../cs-context/references/customer-voice.md`.

Emit inside a fenced `text` block, below the customer-facing divider, plain-text formatted for
an email client: blank lines between paragraphs, `•` bullets, no markdown headings, no pipe
tables, no `**` bold.

```text
Subject: <Account> <weekday> — <the one decision on the table>

Hi <their first name>,

<The specific observation, one sentence, no preamble.>

Three things I'd like to get through on <weekday>:

  • <item>
  • <item>
  • <item>

<The one thing you need from them, with a date.>

<Sign-off>
<Your first name>
```

## Rules

| Rule | Test |
| --- | --- |
| **Every slot is filled with a real name, number or date before emitting** | A block containing `<their first name>` is not send-ready, and the most common way an unedited template reaches a customer is that it looked finished |
| **A gap is dropped, never guessed** | Delete the sentence and raise the gap above the divider as `UNKNOWN — requires X` |
| **The subject line names the decision, not the meeting** | "Northwind Thursday — the Q4 measures and who owns each" beats "Catch-up" |
| **The observation opens it** | No greeting-as-content. The first sentence carries a number, a team or a date that only this account's data could produce |
| **Three items, maximum** | A five-item agenda in a thirty-minute call is a list of things that will not happen |
| **The ask has a date in it** | "Could you confirm by Tuesday whether Priya's team takes the data measure?" — not "let me know your thoughts" |
| **It reads as one person writing to one person** | If the sentence could go to any of forty customers, rewrite it around their number, their team or their own words |

## Anti-patterns — the talk track and the note

| Anti-pattern | Correction |
| --- | --- |
| A talk track opening with "just checking in" | A specific observation with a number and a date in it |
| A health band, ARR at risk, a risk signal or a save play appearing in the talk track | Translate it — see `../../cs-context/references/customer-voice.md`; some lines have no customer-facing form at all |
| A send-ready block still containing an unfilled slot | Fill it, or drop the sentence and raise the gap above the divider as `UNKNOWN — requires X` |
| A note that restates the agenda the invite already carries | Send nothing. A message that adds nothing is a small withdrawal from the relationship |
