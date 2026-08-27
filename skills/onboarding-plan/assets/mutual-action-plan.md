# Asset — Mutual Action Plan (customer-facing)

The MAP is the customer-facing half of the phase plan built in SKILL.md Step 4. It is **not** the
internal plan with the sensitive rows deleted — it is a separate document, built from the same
dates, that a customer can hold their own colleagues to.

Three properties make a MAP work, and a document missing any one of them is a status report:

| Property | Test |
| --- | --- |
| **Both sides carry rows** | If every owner is a vendor name, it is our task list and the customer will treat it as ours |
| **Every row has a named human and a date** | "Customer IT" is not an owner. "Priya Raman, 12 Sept" is |
| **The finish line is their outcome, not our go-live** | The last row is the result they bought, attested by them — not "project closed" |

Length: 8–12 rows for a guided implementation, up to 25 for white-glove. A 60-row MAP is a project
plan that has been forwarded to a customer, and it will not be read twice.

## What must be filled before it is send-ready

| Slot | Source | If missing |
| --- | --- | --- |
| Their outcome, in their words | Handover field 8 / kickoff | Do not send. Without it the MAP is a checklist |
| The metric, its current value, who measures it | Baseline record, `../references/kickoff.md` §5 | Make row 1 "agree the number" and date it |
| Named owner per row, both sides | Step 4 phase plan | Replace the row with "name the owner", dated this week |
| Real dates | Backwards schedule from G-day, SKILL.md Step 1 | Do not send an undated MAP |

No `<slot>` survives into the fenced block. If a value is genuinely unavailable, delete that row
and raise the gap above the divider as `UNKNOWN — requires X`.

## The disclosure firewall applies

**Never in the MAP, in any wording:** the value gate as a gate, float or "no absorption", the mode
name, stall signal names, "stalled", "at risk", services hours, burn ratio, ARR, the opt-out
deadline or notice period, the coverage tier, and any assessment of a person. The internal plan
says *float is 4 days, one slip breaks it*; the MAP says *this sequence has no slack after 3
October, so the two items before it matter more than they look*. Same fact, no internal freight.

Full rules and the leak scan: `../../cs-context/references/customer-voice.md`.

---

════════════════════════════════════════════════════════════
CUSTOMER-FACING — copy the block below and send as written.
Everything above this line is internal. Do not forward it.
════════════════════════════════════════════════════════════

```text
Northwind + Acme — plan to a five-day close
Agreed at kickoff, 11 September. Live version lives in the shared folder.

Where we're heading
  April close took 11 days. July took 9. You want under 5 by the January
  close, and Marcus measures it. Everything below is scheduled backwards
  from that.

Live and running for Finance: 6 November.
First close on the new process: January, with December as the dry run.

What has to happen, in order

  1  Close timings for April and July written down
     Marcus (Northwind)          Fri 12 Sept          DONE

  2  Sandbox tenant + ERP read credentials
     Priya (Northwind)           Fri 19 Sept

  3  Chart of accounts mapping agreed
     Sam (Acme) drafts, Marcus signs off    Fri 26 Sept

  4  ERP connection built and syncing clean for 5 days
     Sam (Acme)                  Fri 10 Oct
     Needs 2 and 3 done. This is the one with no slack after 3 October.

  5  Two Northwind admins trained and signed off
     Jo (Acme) runs it, Dana names the second admin  Wed 15 Oct
     One admin is not enough — if the second name isn't set by 26 Sept,
     tell me and we'll re-sequence rather than discover it in October.

  6  Historic 24 months migrated, counts reconciled
     Sam (Acme) migrates, Marcus reconciles and signs off  Fri 24 Oct

  7  Finance team session (14 people) + your internal announcement
     Dana announces w/c 20 Oct, Jo runs the session Tue 28 Oct

  8  Live for Finance
     Both sides                  Thu 6 Nov

  9  December close run on the new process, timed
     Marcus                      w/c 5 Jan

 10  Five-day close confirmed, in writing, by Marcus
     Marcus                      Fri 30 Jan

Still open
  • Whether intercompany is in scope for January or moves to Q2.
    Dana and Ravi decide by 3 October.

If anything on your side is going to move, the earliest you can tell me
is worth more than the apology later. Row 4 is the one that hurts.

Jo
```

---

## Running it after it is sent

- **Update it in the shared location, never by re-sending.** A MAP that arrives as a new
  attachment every fortnight stops being a shared artifact and becomes our reporting.
- **Change a date with the customer, in writing, within 5 business days of the slip** — not at the
  next scheduled call. Silent re-baselining is what manufactures a first-renewal argument.
- **Read the ownership split every week** (`../references/stall-detection.md` §5). A MAP where the
  overdue rows are all on one side is telling you which conversation to have.
