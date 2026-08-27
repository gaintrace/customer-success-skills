# Internal Exec Brief — emit verbatim

> **Internal only. Never forwarded to a customer, in whole or in part, in any wording.**
>
> Written **before** the customer note, always — it is where every commitment gets agreed, and
> without it the five gates in `../SKILL.md` Step 4 have nothing to gate against. One page. If it
> needs two, the escalation is not understood yet.
>
> It exists to convert an incident into **a decision by a named executive on a named date.** An
> escalation with no ask and no decision date is a notification, and the executive who reads
> three of those stops reading the fourth.
>
> Field specs, the five gates and the escalation ladder: `../references/internal-versions.md`.

---

## The brief

```markdown
# Escalation — <account.name> · <S1|S2|S3|S4> · <date> · <first note | update n | closure | review>
**Internal. Do not forward.** Data as-of <date>. Author <name>.

| Field | Value |
|---|---|
| Account · ARR · renewal · **opt-out (days)** | <name> · $<arr> · <renewal_date> · **<renewal_date − notice_period_days> (<n> days)** |
| Severity · type | <S1–S4> · <service failure \| missed delivery \| broken commitment \| value not realised \| sponsor loss \| product gap \| commercial change \| security> |
| What happened | • <dated fact><br>• <dated fact><br>• <dated fact> |
| Evidence | <2–3 data points, each with a provenance tag `[system · field · date]`, including one customer verbatim with its date> |
| Impact on them | <their units> · <hours, with the arithmetic> · <money, rounded, at a rate they gave us> |
| Impact on us | <ARR at risk **and the scenario** — full churn, or a downsell of $<X>> · <reference status> · <other accounts on the same defect> · <renewal cohort exposure> |
| Why now | <what forces the timeline — the opt-out date, their board, their regulator, their budget cycle, a competitive evaluation window> |
| What we have tried | <dated, with outcomes, **including what did not work**> |
| **The one ask** | <ONE thing only this executive can provide — a peer-level call on a named date, an engineering commitment that competes with roadmap, a commercial exception outside the CSM's band, a policy exception, a decision not to build, or authorisation of the stop-loss> |
| **Decision needed by** | <date, justified by "Why now" — never "ASAP"> |
| Owner | <one name — the DRI, not a team> |
| Stop-loss (`R21`) | <the condition under which we stop investing, and what a managed exit looks like — or "n/a: recoverable service failure, not a save"> |
| Not telling the customer yet | <what, why, and **the date that hold expires**. A hold with no expiry is a decision not to tell them> |
```

---

## Commitment ledger

Filled **before** the customer note is drafted. A row reading `Gate 2 — not agreed` cannot read
`In the note: yes`. That is the whole mechanism.

```markdown
| # | Commitment | Owner | Agreed? (source + timestamp) | Date | Gate result | In the note? |
|---|---|---|---|---|---|---|
| 1 | <what> | <name, role> | <Slack/email/ticket ref + timestamp, quoted> | <date> | Pass | Yes |
| 2 | <what> | <name, role> | <asked <date>, no reply> | — | **Fail — gate 2** | **No.** Re-ask; add only when agreed |
| 3 | <what> | — | — | — | **Fail — gate 5 (commercial)** | **No.** Routes to `renewal-negotiation` (`R11`) |
```

| Gate | Question | If it fails |
| --- | --- | --- |
| 1 · Named owner | One human's name and role — not a team, not "we" | Strip the sentence |
| 2 · They have agreed | Did that person say yes to **this** date, in writing, with a timestamp? | Strip it, or downgrade to a decision date you own |
| 3 · Authority | Is it inside their remit, or has their manager approved? | Escalate internally **before** sending |
| 4 · A date we own (`R19`) | Ours to schedule, or a roadmap / release-train date? | Replace the delivery date with a decision date |
| 5 · No commercial content (`R11`) | Does it change an entitlement, SLA, price or term? | Route to `renewal-negotiation` |

---

## Cadence plan

The last column is filled **now**, not at 16:00 under pressure. A column filled in advance is a
column that gets sent.

```markdown
| Update # | Due (their tz) | Sent? | Channel | Sender | What it says if nothing has changed |
|---|---|---|---|---|---|
| 1 | <time> | ☐ | <channel> | <name> | <the pre-written no-news text> |
| 2 | <time> | ☐ | <channel> | <name> | <the pre-written no-news text> |
```

Run `python3 ../scripts/update_clock.py <incident.json> --now <ISO timestamp>` to compute the
schedule from severity and the updates actually sent. Exit code 1 means an update is overdue.

---

## Prevention register

```markdown
| # | Class of failure | Fix | Owner | By | How the customer sees it landed | Receipt due |
|---|---|---|---|---|---|---|
| 1 | <the class, not the instance> | <a control enforced by a system, not by remembering> | <name> | <date> | <what they can observe> | <date> |
```

Every row's receipt goes out **unprompted** on its date, from the person who made the
commitment. A slipped receipt sent on time costs a fraction of a silent one. Downstream this
register becomes the shortfall section of the next review (`qbr-builder`, `C29`).

---

## Escalation trigger — does an executive get this at all?

Escalate to executive level when **any** of these is true. All four are about authority, not
temperature:

- The customer's own executives are engaged — seniority asymmetry reads as indifference.
- The resolution needs a decision the CSM cannot make: a policy exception, a commercial
  structure, an engineering commitment, a decision not to build.
- The economic buyer has left or changed role (`R3`).
- Severity is S1, or two P0 risk patterns are matched on the account (`R4`).

Two supplementary triggers worth adopting `[P]`: any account in the top ARR decile red for two
consecutive weeks goes to a weekly executive review, and **any stated intent to cancel gets a
same-day executive notification regardless of ARR.**

An executive is the most expensive and least renewable resource in an escalation — roughly one
per account per year before the path stops meaning anything. The question is never "would an
exec help?" but "what decision needs someone with authority the CSM does not have?"

---

## What must not appear, even here

The internal brief is not a private space. It is forwarded internally, quoted in QBR prep,
pasted into a channel with forty people in it, and — in a dispute — produced.

| Never | Instead |
| --- | --- |
| Blame of a named colleague | The system or process gap. Blameless applies internally first, or the timeline you get is not true |
| Blame of a named person at the customer | Their role, and what it means for the plan |
| Speculation presented as fact | Label the inference and give its rule (`../../cs-context/references/evidence-standard.md` §3) |
| A number with no provenance | The tag, or `UNKNOWN — requires <source>` |
| A legal characterisation — "we are liable", "this is a breach" | Facts and dates. Legal decides what they mean |
| A concession described as offered when it was only discussed | What was actually said, verbatim, with a timestamp |

---

## Pre-emit gate

- [ ] Fits on one page
- [ ] The opt-out date is computed and shown with days remaining, not the renewal date alone (`R1`)
- [ ] Every number carries a provenance tag; every gap reads `UNKNOWN — requires <source>`
- [ ] "Impact on us" states the **scenario**, not just a figure — full churn or a downsell of $X
- [ ] "Why now" names the thing that forces the timeline
- [ ] "What we have tried" includes what did not work
- [ ] Exactly **one** ask, and only this executive can satisfy it
- [ ] The decision date is a date, and it is justified by "Why now"
- [ ] One named owner, not two
- [ ] "Not telling the customer yet" has an expiry date, or reads "nothing withheld"
- [ ] The commitment ledger is complete, and no failed-gate row appears in the customer note
- [ ] The cadence plan's no-news column is filled in advance
- [ ] Every prevention row has a receipt date in a named person's calendar
- [ ] No colleague and no customer contact is blamed anywhere in the document
