# Asset — Kickoff agenda (customer-facing)

Emitted at the end of Phase 0, sent 3+ business days before the kickoff so the customer can
prepare rather than react. Everything on this page is written to be read by the customer.

**Before you emit it, fill every slot below.** A block containing `<value>` is not send-ready, and
the most common way an unedited template reaches a customer is that it looked finished. If a value
is genuinely unavailable, **delete the sentence that needed it** and raise the gap above the
divider as `UNKNOWN — requires X`. Do not send the slot.

| Slot | Where it comes from | If it is missing |
| --- | --- | --- |
| Customer + attendee first names | Handover fields 3–7 (`../references/handover.md`) | Do not send. A kickoff agenda addressed to nobody specific fails on arrival |
| The outcome in their words | Handover field 8, or the champion's own sentence from the sales cycle | Ask the AE before the send. This is the one line the agenda exists for |
| The metric and its current value | Baseline record (`../references/kickoff.md` §5) | Drop the sentence; ask for the number as the first agenda item instead |
| Go-live target date | G-day, from SKILL.md Step 1 | Do not send a date you have not computed |
| Named owners on their side | Handover fields 9–13 | Drop the row and make naming them agenda item 2 |
| Prep asks | Phase 0 exit criteria | — |

## The disclosure firewall applies to this document

The kickoff agenda is the first thing that leaks, because it is written while the internal plan is
still open in the next tab. **None of the following appears here, in any wording:** the value gate
as a gate, float, the mode name (white-glove / tech-touch / guided), the stall signals, services
hours or burn, ARR, the opt-out deadline, the coverage tier, or any assessment of a person named in
the handover. Say "our target for you to be live and getting the result" — never "the value gate".

---

════════════════════════════════════════════════════════════
CUSTOMER-FACING — copy the block below and send as written.
Everything above this line is internal. Do not forward it.
════════════════════════════════════════════════════════════

```text
Subject: Northwind kickoff, Thu 11 Sept 2pm — agenda and the two things I need first

Hi Dana,

You told Marcus in July that the thing you'd judge this on is the monthly
close: eleven days in April, and you want it under five by the January
close. That's what this plan is built backwards from, so the agenda is
short and it's mostly about your side of it.

Thursday 11 September, 2:00–3:00pm UK. Teams link is on the invite.

Who I've got coming:
  • You and Marcus (Finance)
  • Priya Raman (your IT, for the SSO and the ERP connection)
  • Me, and Sam Okafor who'll do the build

What we'll settle, in this order:

  1. The number (10 min) — we write down what the close takes today and
     who on your side owns measuring it. Everything else is scheduled
     from that.
  2. Owners (10 min) — one named person on your side for access, one for
     the data, one for the sign-off. They can be the same person, but we
     need to know that on Thursday, not in October.
  3. The plan (20 min) — we're targeting live by 6 November so the
     January close runs on it with a month to spare. I'll walk the
     sequence and where it's tight.
  4. How we escalate (10 min) — who you call when something is stuck,
     and who I call.
  5. Your internal announcement (10 min) — who tells the Finance team
     this is happening, when, and what the deadline is for them.

Two things before Thursday, both small:

  • The April and July close timings, however rough. A number you
    scribbled counts. Without it we're arguing about improvement in
    January with no starting point.
  • Whether Priya can get us a sandbox tenant and the ERP read
    credentials — if that needs a ticket in your system, raising it this
    week saves us about ten days later.

If either of those is going to be hard, tell me now rather than
Thursday and I'll build the plan around it.

Thanks — I know September is not a quiet month for you.

Jo
```

---

## After the kickoff

The agenda is not the record. Within one business day, send the confirmed version of what was
actually agreed — the number, the named owners, the dates, and anything left open — using the
same rules. That document is what `../references/kickoff.md` §5 calls the baseline record, and the
customer-facing half of it is the only thing they will refer back to in six months.

Warmth, register and the leak scan: `../../cs-context/references/customer-voice.md`.
