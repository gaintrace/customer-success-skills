# Loop-Close Notes — inner loop and outer loop

> Two customer-facing templates. Everything inside a fence is written for a customer to read.
> No internal risk language, no ARR figures, no health bands, no theme codes, no risk vocabulary
> (`R18 · The Firewall`). Read `../../cs-context/references/customer-voice.md` before writing
> either one.
>
> **Every `<angle-bracket slot>` below is a slot you fill, not text you emit.** The block you
> hand the user contains real names, real dates and real numbers, or it omits that sentence and
> the gap is raised above the divider as `UNKNOWN — requires X`. A fence containing a
> placeholder is not send-ready, and the most common way an unedited template reaches a
> customer is that it looked finished.

---

## 1. Inner loop — individual reply to a detractor or a severity-3 mention

Target: 48 hours from the response `[P]`. From the named account owner, not from a shared inbox.
One clarifying question maximum — this is an acknowledgement, not a survey.

````
════════════════════════════════════════════════════════════
CUSTOMER-FACING — copy the block below and send as written.
Everything above this line is internal. Do not forward it.
════════════════════════════════════════════════════════════

```text
Subject: Following up on what you told us on <date>

Hi <first name>,

You said "<short verbatim quote, their words>" in the <instrument> on <date>.
That is specific enough to act on, so I want to check I have it right before
I take it anywhere internally: <one clarifying question, specific enough
that a one-line answer is useful>.

Here is what happens either way:

  • <specific action> — <owner>, by <date>
  • <specific action> — <owner>, by <date>

I'll come back to you on <date> with where each of those landed, including
if the answer is no.

<name>
<title>
```
````

**Rules**

| Rule | Why |
| --- | --- |
| Quote them back, in their words | Proves the response was read by a person |
| One clarifying question, not three | A detractor who just told you something is wrong will not fill in another form |
| Name a date for your own follow-up | The follow-up is the loop; the acknowledgement is not |
| Never open with a defence or an explanation | The explanation goes in the follow-up, after you have understood the complaint |
| Never bundle a renewal, an upsell, or a reference request | Combining them converts an apology into a sales call |
| Record `loop_closed_at` and log an `interaction` | An unrecorded closure cannot be counted, and the closure rate is a published metric |

**Promoter variant.** For a 9–10 from an economic buyer or admin: thank them, then make the
**advocacy** ask (reference call, review, case study). Send within 7–14 days; the window expires
at 90 days `[P]`. **Never make the expansion ask in the same conversation** — separate them by at
least two weeks and hand the expansion path to `expansion-finder`.

---

## 2. Outer loop — the "you said / we did" note to the base

Sent to **everyone who received the survey, respondents and non-respondents alike** — the
non-respondents are the population whose response rate you are trying to recover. Within 30 days
of the readout, same quarter, always.

````
════════════════════════════════════════════════════════════
CUSTOMER-FACING — copy the block below and send as written.
Everything above this line is internal. Do not forward it.
════════════════════════════════════════════════════════════

```text
Subject: What you told us this quarter, and what changed because of it

Hi <first name>,

<N> of you gave us feedback between <date> and <date> — in surveys, support
tickets, calls, and directly by email. Here is what came through most often
and what has happened since.

WHAT WE HEARD

  • <Theme, in customers' language> — raised by <rough scale, e.g. "about a
    third of the teams who responded">
  • <Theme> — <rough scale>
  • <Theme> — <rough scale>

WHAT WE SHIPPED

  • <theme> — <the specific change>, released <date>
  • <theme> — <the specific change>, released <date>

WHAT WE ARE WORKING ON NOW

  • <theme> — <the committed work>, expected <quarter>

WHAT WE ARE NOT DOING RIGHT NOW, AND WHY

  • <theme> — not planned for <year>. <Honest reason: competing priorities,
    a technical constraint, or a different direction we have chosen.>
    We will look at it again <trigger or date>.

If your team raised something that is not here, reply to this email and it
reaches me directly. The next round of this note goes out in <month>.

<name>
<title>
```
````

**Rules**

| Rule | Why |
| --- | --- |
| Section 4 — "what we're not doing" — is mandatory | It is the section nobody writes, and the reason customers stop responding. A no is survivable; silence is not |
| Rough scale, never internal figures | "About a third of teams who responded" — never ARR, never account counts by segment, never health bands |
| Themes in the customer's language | Internal theme codes and category names never appear |
| Ship dates are real dates | A "we shipped" claim that turns out to be a beta destroys the next three notes |
| Send to non-respondents too | They are the population whose response rate you are trying to recover |
| Same quarter as the readout | A "you said / we did" note arriving six months later reads as an admission that nothing happened for five of them |
| No commitments the owning function has not made | Every forward-looking row traces to a routed theme with a named owner and a date (`R19`) |

**Reuse.** This note is the strongest QBR slide the company owns — hand it to `qbr-builder`
rather than rebuilding a value narrative from usage charts.

---

## 3. Before either note leaves — the leak scan

Run `../../cs-context/references/customer-voice.md` §"The leak scan" over the fenced block.
The VoC-specific hits, in order of how often they happen:

| Leak | Where it comes from | The fix |
| --- | --- | --- |
| "You're one of our at-risk accounts" | The register's health band bleeding into the greeting | Never reference a band, a score or a risk word in any wording |
| "$180k of ARR raised this" | Rough scale replaced with the attribution figure | "About a third of the teams who responded" |
| "THEME-14 · Reporting latency" | Internal theme codes copied from the register | The customer's own language for the problem |
| "We escalated this internally" / "we opened a save play" | Internal process language that sounds reassuring | What will happen, who owns it, by when |
| "We noticed <name> has left" | A champion-departure inference stated as fact | "Who's picking up the work <name> was leading?" |
| "Several other customers raised this too" | Third-party disclosure | Rough scale of *this* survey only |
| "Just checking in on your feedback" | Filler opener | Quote them back in the first line |

Banned in both notes, without exception: *just checking in* · *touching base* · *circling back* ·
*hope you're well* · *as per my last email* · *reaching out* · *we value your partnership* ·
*let me know your thoughts* · *at your earliest convenience* · *drive adoption* · *leverage*.
The test: could this sentence have gone to any of forty customers? Then rewrite it.
