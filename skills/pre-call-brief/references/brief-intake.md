# Brief Intake

> What to read before you ask, what to ask when reading is not enough, and what to do with a
> file someone exported badly. Read this **before asking the user anything** — the fastest way
> to tell a CSM the skill did not read their systems is to ask them something the calendar
> invite already answered.

**Contents**
[Read it before you ask](#read-it-before-you-ask) · [The three ways](#the-three-ways) ·
[The intake batch](#the-intake-batch) · [When the batch goes unanswered](#when-the-batch-goes-unanswered) ·
[Files](#files)

---

## Read it before you ask

| Field | Read it from | If it is not there |
| --- | --- | --- |
| Account | the request | ask — the one field with no usable default |
| Date / time / duration | the next calendar event matching that account | assume the next working day and record the assumption |
| Meeting type | the invite title and body | ask (Q1 below) |
| Attendees, both sides | the calendar invite | reconstruct from the last 90 days of threads and label it inferred |
| Who is running it | the organiser field | the user |
| Invite audit trail: sent, accepted, declined, rescheduled, by whom and when | the calendar event's own history | `UNKNOWN — requires a calendar source` — and the relationship family drops to ⚠️ Partial |
| Who is on the invite but has not responded | the attendee response status | treat as unaccepted, not as accepted |
| Stated agenda | the invite body | "none supplied" — which is itself a finding, not a blank |
| Who signs and who decides | the executed contract's signature block, the opportunity approval chain, procurement threads | `UNKNOWN — requires <the specific record>`, and it goes in the ⚠️ block before a renewal, QBR or expansion |

The invite audit trail is not administrative detail. It is the input to the calendar signals in
§3 — see `decision-room.md`.

---

## The three ways

Every missing input resolves exactly one of three ways. There is no fourth.

| | When | Action |
| --- | --- | --- |
| **Read it** | It is in the data, in `cs-context`, in the invite, or derivable from them | Derive it, show the derivation, never ask |
| **Ask it** | Two likely answers produce a **materially different brief** | Ask — tappably, batched, with a recommended default |
| **Mark it** | Missing, and unanswerable or immaterial to this call | `UNKNOWN — requires <source>`, plus a confidence cap |

Filling a gap with a plausible value is not one of the three. A brief is read out loud; an
invented number is quoted to the customer by the person who trusted it.

---

## The intake batch

One `AskUserQuestion` call, up to four questions, mutually exclusive options, the recommended
one first and labelled, one line under each saying what it changes. One interruption, not four.
Skip any question the invite or `cs-context` already answers.

| # | Header | Question | Options — recommended first |
| --- | --- | --- | --- |
| 1 | `Meeting` | What kind of conversation is this? | **Routine check-in (Recommended)** — short brief led by the since-last-time delta · **QBR / EBR** — full brief led by their stated business objectives; pair with `qbr-builder` · **Renewal** — full brief led by the opt-out date and the decision path · **Escalation** — full brief led by a dated failure chronology |
| 2 | `Prep time` | How long have you got to read this? | **Full brief, one-pager on top (Recommended)** — ~10 minutes · **One-pager only** — one screen, for 5 minutes before the call · **Full brief plus talk track** — adds the words to say and the pre-call note |
| 3 | `Walk out with` | What are you trying to leave the call holding? | **The next commitment on the current plan (Recommended)** — optimises for one dated yes · **A renewal or budget confirmation** — adds decision path, paper lead times, price objections · **An introduction or expansion opening** — adds the value case and the budget holder, gated on health · **Repaired trust after a failure** — leads with what we owe and what we can commit |
| 4 | `Data` | What can I work from? | **Connected sources plus anything I upload (Recommended)** — `ingest.py` runs over the files · **I'll paste exports or a transcript** — same path, pasted rather than uploaded · **I'll answer questions instead** — no files; built from `cs-context` and your answers, confidence capped at Low · **Context file only** — fastest and thinnest |

**Never ask who the attendees are** when the invite lists them, **never ask the renewal date**
when `cs-context` holds it, and **never ask what the meeting is about** when the invite body
says so. Each of those spends the user's attention proving the skill did not look.

---

## When the batch goes unanswered

Run. Do not wait, and do not produce a thinner brief in protest.

1. Take the four recommended defaults.
2. State them in one line under the title: *"Built as a full brief for a routine check-in from
   connected sources — say the word and I'll re-cut it as a renewal brief."*
3. Put each one in the Assumption Register with a **concrete** consequence — the section that
   would have led instead, the figure that would be wrong, the gate that would have applied.

"May affect results" is not a consequence. If you cannot name what would change, the assumption
was not load-bearing and does not need a row.

---

## Files

Accept whatever arrives: CSV, TSV, XLSX, JSON, NDJSON, warehouse query results, a pasted call
transcript, a forwarded email thread, a screenshot described in prose — or nothing at all but
the answers to the four questions above.

Run `../../cs-context/scripts/ingest.py` on every supplied file **before quoting a number from
it**. It sniffs encoding and delimiter, finds the real header row beneath the three title rows a
CRM report puts above it, maps columns onto the canonical schema with a stated confidence per
column, normalises dates, money stored as text and booleans, resolves accounts across files, and
reports the join rate.

| Rule | Why |
| --- | --- |
| **Confirm every column mapping below 0.80 confidence** before its numbers reach the brief | A mis-mapped column produces a confidently wrong brief that gets read out loud on the call |
| **Degrade, never refuse** — one stale export and a transcript still produce a brief, with a coverage figure and a capped confidence | The only stop condition is coverage under 40% of the seven families, where a score would be meaningless |
| **Never assume an export is complete or current** — ask the as-of date and print it under the title | An export pulled three weeks ago cannot see the auto-renew flag that flipped last Tuesday |
| **Nothing is extrapolated past the as-of date** | Treat anything past the staleness table in `../../cs-context/references/evidence-standard.md` §7 as stale, and say so rather than trending through it |

---

## Anti-patterns

| Anti-pattern | Correction |
| --- | --- |
| Asking the user something `cs-context` or the calendar invite already answers | Read both first; ask only what changes the brief |
| Four questions asked one at a time | One tappable batch, recommended defaults, then run |
| Blocking because a question went unanswered | Proceed on the default, state it under the title, log it in the Assumption Register |
| Refusing to brief because the export is messy or partial | Run `ingest.py`, state coverage, cap confidence, brief anyway |
| Reading numbers from a column mapped at 0.6 confidence | Confirm the mapping first — a wrong column is read out loud on the call |
| Treating an unanswered invite as an accepted one | Unresponded is unaccepted, and it is an input to the calendar signals |
