# Value One-Pager — the customer artifact

**This is the only page in the value case a customer ever sees.** It is a different document
from the internal case, not a redacted version of it (`R18`). Nothing crosses except arithmetic
the customer owns.

## What crosses, and what never does

| Crosses | Never crosses, in any wording |
| --- | --- |
| Their metric, their baseline, their current value, their source | Health score or band, risk band, "at risk" |
| Their unit economics, named as theirs | ARR at risk, exposure, forecast category |
| The attribution split they set, with their name on it | Save play, war room, coverage tier, book size |
| The conservative figure, the cost they paid, the payback | Our cost-to-serve or gross margin on the account |
| The sensitivity sentence and the exclusions list | Competitor intelligence they did not raise |
| Their own words about the outcome | Any assessment of a named person on their side |
| One question about next period's target | Any commercial ask (`R11`) |

Run the leak scan in `../../cs-context/references/customer-voice.md` before this leaves.

## Formatting rules

- Their currency, their fiscal period names, their units — per store, per claim, per rep, per ticket
- Plain text: blank lines between paragraphs, `•` bullets, no markdown headings, no pipe tables, no `**` bold
- **No unfilled slots.** A block containing `<name>` is not send-ready. If a value is genuinely
  unavailable, delete that sentence and raise the gap internally as `UNKNOWN — requires X`
- One page. If it needs two, the second one is an appendix they did not ask for
- Prefer *"$18.40 per ticket × 141,000 tickets"* to *"$2.6M value delivered"*

---

════════════════════════════════════════════════════════════
CUSTOMER-FACING — copy the block below and send as written.
Everything above this line is internal. Do not forward it.
════════════════════════════════════════════════════════════

```text
<Account> — what <period, in their fiscal terms> produced

<Their objective, in the words they used when they set it, with the date they said it.>

Where it started and where it is now:

  • <Metric>: <baseline> in <baseline window> to <current> in <current window>. Source: <their system>, run by <their person>.
  • <Metric>: <baseline> to <current>. Source: <their system>.

What that is worth, using your own numbers:

  • <Benefit line>: <unit gain> x <their unit economic> = <currency figure>
  • <Benefit line>: <unit gain> x <their unit economic> = <currency figure>
  • Attribution: <name> put <X>% of this here and the rest to <the other cause>.

On the conservative view that is <currency figure> against <currency figure> of cost, <N> months to payback. Even at <stressed assumption>, payback is <N> months.

Not counted in this figure: <two or three specific items>. Inputs validated by <name, title, date>.

<One question, with a date, about the next period's target.>

<Sign-off>, <Your first name>
```

---

## Worked example — filled, send-ready

```text
Northwind — what FY26 produced

In October you said the thing you would judge this on was getting shipper support cost per account down without adding people to the queue.

Where it started and where it is now:

  • Tier-1 tickets: 412 per 1,000 shipper accounts in Jan-Mar, down to 284 in Apr-Jun. Source: your helpdesk, the tier_1 shipper queue, run by Priya.
  • Claims close: 9.0 working days in Q1 to 5.5 in Q3. Source: your close calendar.

What that is worth, using your own numbers:

  • Ticket deflection: 128 fewer per 1,000 accounts x $18.40 your loaded cost per ticket = $404,400 across 141,000 tickets
  • Claims close: 3.5 days x 26 people x your $68 loaded hourly, at 50% of the time redeployed = $48,400
  • Attribution: Priya put 70% of the ticket movement here and 30% to your knowledge-base rewrite. Jorge set the close split at 70/30 with the reconciliation project.

On the conservative view that is $285,000 against $252,000 of cost, 8.9 months to payback. Even at 40% attribution and none of the time redeployed, payback is 15 months.

Not counted in this figure: the knowledge-base rewrite's own contribution, the two integrations your team built and maintains, and anything in FY27. Inputs validated by Priya Nandakumar, Director of Support Ops, 14 August 2026.

Billing goes live in January and is the only queue still at the old numbers. Worth setting a target for it before your planning cycle closes on 30 September?

Thanks, Jo
```

**What makes that block work:** every number has a source and an owner, the attribution is
theirs and named, the conservative figure leads, the sensitivity line is volunteered, the
exclusions are specific, and the question is small, dated, and about their next decision rather
than our next sale. There is no adjective anywhere in it.
