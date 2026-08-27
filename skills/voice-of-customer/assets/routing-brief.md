# Routing Brief — emit verbatim, one per routed theme

> The packet a theme carries when it leaves CS. Each destination needs different evidence to act;
> sending the same packet to everyone is why routed themes stall. Internal document.

```markdown
# Routing Brief — <THEME-CODE> <theme name>
**To:** <destination function> · **Accountable owner proposed:** <name>
**Consulted:** <functions> · **From:** <VP CS> · **Date:** <date> · **Decision due:** <date>

## The ask
<One sentence. The decision type from readout-structure.md §5, the owner, and the date.>

## Why this, why now
| | |
|---|---|
| Accounts raising it | <n> (<reach>% of in-scope accounts) |
| Attributed ARR | $<X> — revenue of the accounts raising it, **not** revenue at risk |
| Risk-weighted ARR | $<Y> (rules-based band midpoints, not a calibrated forecast) |
| Renewal exposure ≤120d | $<Z> across <n> accounts, earliest opt-out <date> |
| Segment split | ENT $<a> · MM $<b> · SMB $<c> |
| Health band split | Secure $<a> · Watch $<b> · At Risk $<c> · High $<d> · Critical $<e> |
| Economic-buyer mentions | <n> |
| Trend | <status> — share of voice <now>% vs <prior>%, z = <value> (screen only) |
| Evidence strength | <Confirmed / Supported / Anecdotal> across <n> channels |

## The job to be done, in the customer's words
> "<verbatim>" — <account>, <role>, <date> [<source ref>]
> "<verbatim>" — <account>, <role>, <date> [<source ref>]
> "<verbatim>" — <account>, <role>, <date> [<source ref>]

## Current workaround and its cost
<What customers do today instead, and what it costs them — hours, headcount, error rate, or
delay. Quantified where the customer quantified it; `UNKNOWN — requires X` where they did not.>

## Assessed cause
**Stated as:** <customer language> · **Assessed cause:** <evidence-backed>
<The what-would-have-to-be-true test and its result.>

## What changes if this is fixed
| Expected effect | How we would know | Measured when |
|---|---|---|

## Cost to fix
`UNKNOWN — requires <function> estimate` · **Requested by <date>**

## Decision requested
- [ ] Accept — target: <release / quarter / date>
- [ ] Decline — reason: <> (routes to the "Not Doing" section and to the customers who raised it)
- [ ] Defer — until: <date>, because: <>
```

---

## What each destination needs — the differences that matter

| Destination | Lead with | Must include | Will reject the brief without |
| --- | --- | --- | --- |
| **Product** | The job to be done in the customer's words | ARR splits, workaround cost, renewal exposure, 3 verbatims | A problem statement that is actually a feature request |
| **Engineering** | Reproduction and blast radius | Ticket/incident IDs, frequency, duration, affected ARR, SLA breaches | Steps to reproduce or the failing records |
| **Support** | The cluster and its repeat rate | Cluster size, reopen rate, deflection candidates, the missing macro or article | A measurable before/after |
| **CS** | The account list | Owner, health band, success-plan milestone affected, what was promised and by whom | A named play per account with a date |
| **Sales** | The specific claim made in the sale | The source of the claim (recording, deck, email), accounts affected, ARR | Evidence the claim was actually made — not an inference |
| **Pricing** | The boundary, not the product | Which capability sits in which tier, ARR on each side, competitive comparison | The revenue on both sides of the boundary |
| **Docs / Education** | The exact question customers asked | Verbatim questions, search terms used, the article that should have answered | Deflection measurement plan |
| **Exec staff** | The unowned decision | Everything above, plus 2–3 options with cost and consequence, and a recommendation | A recommendation. Exec staff assigns ownership; it does not diagnose |

## Rules

1. **One accountable owner.** Consulted functions are named as consulted. A theme with two owners
   has none.
2. **Route the assessed cause, not the stated reason.** A "too expensive" theme whose assessed
   cause is value non-realisation goes to CS, and the brief explains the reasoning.
3. **Capability gated by plan goes to Pricing, never to Product.** The capability exists.
4. **Never invent the cost to fix.** `UNKNOWN — requires <function> estimate`, with a date on the
   request.
5. **A decline is an outcome, not a failure.** Route it to the "Not Doing" section with a reason
   and a reconsider trigger, and tell the customers who raised it.
6. **Unowned after one full period → exec staff automatically.** Unowned themes accumulate; they
   do not age out.
