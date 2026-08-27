# Negotiation Debrief — within five working days, signed or lost

> Internal. Never leaves the building. The concession log is next cycle's opening position, and
> the gate log is the only way anyone finds out that the ladder was climbed with the wrong person
> in the room.

```markdown
# Negotiation Debrief — <Account> · <signed | lost | right-sized> · <date>

**Outcome:** <final ARR> vs opening position <ARR> vs walk-away <ARR>. <One sentence on what
decided it.>

## 1. The gates — did we earn the right to climb the ladder?
| Gate | Status at first concession | Evidence | If FAIL, what it cost |
|---|---|---|---|
| A · Authority (`C14`) | PASS / FAIL | `signs` = <name>, in the conversation on <date> | <e.g. rung 4 offered to a non-signer on 12 Sept, re-offered to Dana on 3 Oct from the lower base> |
| B · Business thread (`C10`) | PASS / FAIL | `days_since_business_thread` = <n> at first concession | <e.g. 47 days; every conversation after 2 Sept was about price> |

## 2. The concession log — every rung offered, taken or not
| Date | Rung | What we gave | **What we got** | Papered? | Taken? | Approver |
|---|---|---|---|---|---|---|

**A row with an empty What-we-got cell is the finding, not a gap** (`C12`). Count them and say
the number out loud: `<n>` of `<m>` concessions were donations.

**Annual cost of what was given:** $<x> (2 s.f.) · **Lifetime cost over assumed tenure:** $<y>
(`scripts/concession_math.py discount`).

## 3. What we refused, and what happened
| What was asked | Why refused | Their response | Would we refuse it again |
|---|---|---|---|

## 4. The comms — did the number land as a decision?
| Draft | Sent | `pre_send_scan.py` result before sending | Hits |
|---|---|---|---|
| Uplift notification | <date> | PASS / FAIL | <e.g. C3 — softener after the price, caught and rewritten> |
| Discount response | <date> | | |

Where any draft went out without the scan, say so. The scan is the record that the number was
announced rather than requested (`C13`) and that nothing followed it (`C3`).

## 5. The precedent set
<What is now the floor for next cycle: the discount, the payment terms, the clause conceded, and
who inside their organisation now knows it. A precedent travels — inside their org and outward
through procurement networks.>

## 6. Timing and lead times we mis-estimated
| Workstream | Assumed | Actual | Correction for next cycle |
|---|---|---|---|

## 7. The one change before next cycle
<One. Not five. Named, owned and dated.>
**Owner:** <name> · **By:** <date> · **How we will know it worked:** <observable>
```

## Feeding it forward

| Goes to | What it carries |
| --- | --- |
| `renewal-forecast` | The delta reason codes and the booked category — a right-size booked as a flat renewal breaks GRR |
| `churn-postmortem` | On a loss: the concession log, the gate log and the cause code |
| `renewal-prep` | The corrected paper lead times for the next `D` calculation |
| Next cycle's Step 1 | The precedent, which is the real opening number whatever the price list says |
