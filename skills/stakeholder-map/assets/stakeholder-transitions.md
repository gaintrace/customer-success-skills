# Stakeholder Transitions — customer-facing drafts

> Four moments where a stakeholder map produces something a customer reads: a contact has gone
> quiet or left, a new stakeholder has arrived, we need a second relationship, and we need to
> confirm the structure we inferred. Each draft below is fully written — no placeholders — and
> is shown with the internal reasoning it must never contain.
>
> Read `../../cs-context/references/customer-voice.md` before adapting any of these. The leak
> scan is not optional; these are the exact drafts where internal language slips through,
> because they are written in the same session as the exposure arithmetic.

**Contents** — [The firewall for this skill](#the-firewall-for-this-skill) ·
[1. Suspected departure](#1-suspected-departure--the-successor-request) ·
[2. New stakeholder](#2-new-stakeholder--the-introduction) ·
[3. Second contact](#3-second-contact--the-introduction-request) ·
[4. Confirming structure](#4-confirming-the-structure-we-inferred) ·
[Pre-send checklist](#pre-send-checklist)

---

## The firewall for this skill

Everything this skill computes is INTERNAL-ONLY. There is no softened wording that makes any
of it sendable.

| Internal | Reaches the customer as |
| --- | --- |
| Coverage score, depth, breadth, height | *Never.* Not as "we'd like broader engagement" either — that is the same sentence with a coat on |
| Champion risk score, departure exposure, ARR at risk | *Never* |
| "Single-threaded", "multithreading", "coverage gap" | *Never* |
| Influence and sentiment scores, `role_confidence`, blocker/detractor labels | *Never.* No assessment of a named person, in any wording |
| `mobilising_capacity`, the M1–M3 tests, "supporter" (`C8`) | *Never.* "Supporter" reads as a compliment and is a judgement that they cannot move their own organisation. The M-tests are asked as questions about how the last decision got made — never described |
| A blocker disposition — `convert`, `contain`, `bypass` (`C11`) | *Never*, and `bypass` least of all: the word describes going around a named person. What reaches them is a direct answer to their specific objection, in writing |
| `signs` / `decides` / `influences` and any `CONCENTRATION` finding (`C7`) | *Never as a map.* Ask it forward instead: "when we get to the renewal, who signs, and does anyone approve before it reaches them?" |
| A departure inferred from a bounce | A question about who is picking up the work — never a statement that we noticed someone left |
| Role labels (`economic_buyer`, `champion`, `procurement`) | *Never.* These are our categories for their people |
| An inferred reporting line | "Here's how I've understood it — is that right?" Never asserted |

**The one legitimate translation** is from a structural observation to a question about their
work. "We are single-threaded on Marcus" becomes "who else on your side should be in this?" —
and it is a genuine question, asked because we do not know, not a manoeuvre.

---

## 1. Suspected departure — the successor request

**When.** A departure signal has fired and the disconfirming tests in `../references/champion-risk.md`
§3 did not clear it. Send within 48 hours, to the most senior contact you have who is *not* the
departed person.

**The trap.** "We noticed Marcus has left" states something you inferred from a bounce. It
tells the customer we monitor their staff, and if the inference is wrong it is embarrassing in
both directions. Ask about the work, never about the person.

````text
Subject: Northwind — who's picking up the RevOps rollout?

Hi Dana,

My last two emails to Marcus haven't landed, so I want to make sure the
rollout doesn't stall while I work out where to send things.

Where it stands:

  • 34 of the 40 RevOps seats are live; the last six are waiting on the
    Finance approval step Marcus was arranging with your team.
  • The Q3 close ran in four days against eleven in April — the number
    Marcus said you'd judge this on.
  • One open item from us: the intercompany export fix, which Sam on our
    side has scheduled for 11 September.

Two things would help:

  • Who should I work with on the remaining six seats?
  • Is there anything about the approval step I should know before I
    chase it?

Happy to do this in fifteen minutes on Thursday or Friday if that's
easier than email.

Thanks,
Jo
````

| Slot | Fill from | If you cannot fill it |
| --- | --- | --- |
| Senior contact's name | The most senior `verified` contact who is not the departed person | Do not send to a distribution list; find a person first |
| Two or three concrete facts about the work | Usage, tickets, the success plan — facts they can verify in their own systems | Remove the bullet; never pad with a generic statement of value |
| The open item **we** owe | The commitment log | Say so plainly if there is one and it is late |
| The named person on our side and a real date | Only a commitment already agreed internally | Remove the line |

---

## 2. New stakeholder — the introduction

**When.** A new name has appeared with authority — a successor, a new executive, a reorg
arrival. Send in the first five days, with something attached that is useful to someone with
zero context.

**The trap.** Sending the previous stakeholder's success plan. A new stakeholder hears a list
of what we delivered as an invoice, and a list of what their predecessor agreed as an
obligation they did not sign up to. Ask first.

````text
Subject: Northwind + our team — a one-page catch-up before we meet

Hi Ravi,

You've picked up RevOps at a point where a few things are mid-flight, so
here's the short version rather than a deck.

Where things stand:

  • 34 of 40 seats are live across RevOps; six are waiting on a Finance
    approval step.
  • Your Q3 close ran in four days. In April it took eleven.
  • Two things are open on our side: an intercompany export fix, due from
    us on 11 September, and the reporting change your team asked for in
    June, which we have not scheduled yet and I owe you a date on.

What I don't know yet is what you're being measured on, and whether the
objectives set in January are still the right ones. I'd rather ask than
assume — they may not be yours.

Twenty minutes on Tuesday or Wednesday? I'll bring the current numbers
and no slides.

Thanks,
Jo
````

| Slot | Fill from | If you cannot fill it |
| --- | --- | --- |
| What is mid-flight | Success plan, open tickets, the commitment log | Remove the bullet rather than write a vague one |
| The thing **we** owe and have not scheduled | The commitment log — include it even when it is unflattering, because they will find it | Never omit a late commitment; the omission is what damages the relationship |
| The predecessor's objectives | The success plan | Say the objectives were set with their predecessor and ask whether they still hold |

**Never in this email:** the predecessor's name framed as a departure, anything about the
renewal, any reference to the account's history as a list of our achievements.

---

## 3. Second contact — the introduction request

**When.** Depth is below the band target and you have identified a named second contact from
data (see `../references/coverage-plays.md` §2). Ask the champion to make the introduction —
with the name and the reason already supplied, so it costs them one line.

````text
Subject: Quick intro to Tom on the marketing ops side?

Hi Marcus,

Tom Iyer's team has become the heaviest user of the approvals workflow
since June — more volume than RevOps now runs through it. I've never
spoken to him.

There's a batching feature his usage pattern suggests he'd want and
probably hasn't found, and I'd rather show him than have him work
around it.

Would you introduce us, or would you rather I go direct? Either is
fine — I just didn't want to appear in his inbox out of nowhere.

Thanks,
Jo
````

| Slot | Fill from | If you cannot fill it |
| --- | --- | --- |
| The named person and their function | Usage, ticket or invite data | Do not ask "who else should I speak to?" — that makes your coverage gap their homework |
| The specific observation about their usage | `usage_daily` / `usage_event`, segmented | Without a specific observation there is no reason to meet, so do not send it |
| The offer that is in it for them | The unused capability, the fix, the benchmark | Find one before sending |

---

## 4. Confirming the structure we inferred

**When.** Before the renewal window, not inside it. A sanitised structure view may be shared —
names, titles and who on our side works with whom. Nothing else from the map goes with it.

````text
Subject: Making sure I've got your side right

Hi Marcus,

Before we get into renewal planning, I want to check I've understood how
this sits on your side, because I'd rather be corrected now than assume.

Here's my understanding:

  • Dana owns the budget for this.
  • You run it day to day, with Ana on the admin side.
  • Rae in procurement gets involved close to the renewal date.
  • I don't know who handles security review — I don't think we've met
    anyone on that side.

Two questions:

  • Is that roughly right?
  • When this comes round in February, who else has to nod?

No rush — whenever you're next replying.

Thanks,
Jo
````

| Slot | Fill from | If you cannot fill it |
| --- | --- | --- |
| The structure lines | Only `verified` and `evidenced` roles, in plain language | State the gap as a gap, as the fourth bullet does — that is the highest-yield line in the email |
| The renewal month | `subscription.renewal_date` | Ask the question without the month rather than guessing |

**Note the phrasing.** "Dana owns the budget" is a plain description of work, not the label
`economic_buyer`. "I don't know who handles security review" invites the answer, and being
straightforwardly ignorant about a gap is more credible than pretending to have a full picture.

---

## Pre-send checklist

- [ ] No coverage score, depth, risk score, exposure figure or dollar amount appears
- [ ] No role label from our taxonomy appears, in any wording
- [ ] No assessment of any named person appears
- [ ] Nothing inferred is stated as fact; every inference is phrased as a question
- [ ] Every number is one the customer can verify in their own systems
- [ ] Every commitment named has an internally agreed owner and a real date
- [ ] No unfilled slot remains anywhere inside the fence
- [ ] Formatted for an email client — plain text, blank lines between paragraphs, `•` bullets,
      no markdown headings, no pipe tables, no `**` bold
- [ ] The first line is specific to this account and contains no filler
- [ ] One ask, dated, easy to say yes to
- [ ] Forward test: this reads acceptably if forwarded to their CFO
