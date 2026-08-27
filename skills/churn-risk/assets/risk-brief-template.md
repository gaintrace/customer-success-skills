# Churn Risk Assessment — <scope> · <date>
**Internal document.** Contains risk language that must never be sent to a customer.

## Bottom Line

<Three sentences. Total ARR at risk, how many accounts, and the single most urgent action
with its owner and date. An executive reads this and stops; make it sufficient.>

| | |
|---|---|
| ARR assessed | $X across N accounts |
| ARR at risk (exposure-weighted) | $X (Y% of assessed) |
| Critical / High / At Risk / Watch / Secure | a / b / c / d / e |
| Accounts escalating regardless of score (P0 pattern) | n |
| Most urgent | <Account> — <reason> — <owner> — by <date> |
| Assessment confidence | High/Medium/Low — <the criteria met> |
| Weight profile used | enterprise / plg / consumption |

## Priority Table

Ranked by Action Priority = Exposure × Urgency × Savability. Not by score.

| # | Account | ARR | Band | Score | P0 | Pattern | Days to opt-out | Exposure | Priority | Owner | Next action (by date) |
|---|---|---|---|---|---|---|---|---|---|---|---|

## Not worked this cycle

<The accounts that scored but will not receive a play, and why. An undeclared decision to
skip an account is how accounts get skipped for a quarter. Name them.>

| Account | ARR | Band | Reason not worked | Revisit by |
|---|---|---|---|---|

---

## Account Card — <Account>

**Risk <score>/100 · <Band> · Confidence <level> · ARR $X · Renewal <date> · Opt-out <date> (<N> days)**

**The call:** <One paragraph. What is happening, why, and what happens if nothing changes.
State it plainly — hedging every clause to avoid being wrong makes the artifact useless.>

### Required reads — no valid empty value

Four fields a rushed review drops first. Each is filled or reads `UNKNOWN — requires <source>`.
A card missing a row is invalid output, not a short card.

| Field | Value |
|---|---|
| Calendar (`C22`) — acceptance latency vs baseline | <median days, and the multiple of baseline> |
| Calendar (`C22`) — reschedules / declines, last 90d | <n> · <consecutive by the economic buyer? yes/no> |
| Calendar (`C22`) — who accepts | <named person and role: economic buyer / champion / delegate / nobody> |
| Negotiation friction (`C24`) | contested / routine / frictionless / not-applicable — self-serve |
| First term (`C23`) — days since contract start | <n> · gate run before the renewal-window filter? yes |
| First term (`C23`) — activation event | <date it fired, or **NEVER**> |
| Renewal plan status (`C23`) | written / **withheld — activation never fired**; unlocking milestone <name> |
| Support silence (`C21`) — tickets last 90d | <n> · <spike-then-collapse? yes/no> · scored <risk>, never 0 |

### Signals fired
| Family | Signal (ID) | Evidence | Tier | Lead time |
|---|---|---|---|---|

### Checked and clear
| Family | What was checked | Result |
|---|---|---|

### Not checkable
| Family | What is missing | What it would take |
|---|---|---|

### Override floors applied
| Trigger | Evidence | Floor | Disconfirming test run? |
|---|---|---|---|

### Compound patterns matched
| Pattern | Priority | Composition observed | Implication |
|---|---|---|---|

### Contradictions
| Signal A | Signal B | Reading | Tiebreak rule applied |
|---|---|---|---|

### Score breakdown
| Family | Risk | Weight | Contribution | Top driver |
|---|---|---|---|---|
| **Weighted (renormalised over N families)** | | | **X** | |
| **After pattern bonus** | | | **Y** | |
| **After floors** | | | **Z** | |

### Priority arithmetic
```
Exposure        = ARR $X × band probability P   = $E
Urgency         = <days to opt-out> days        = U
Savability      = <category>                    = S
Action Priority = E × U × S                     = $A
```

### Intervention plan
| # | Action | Owner | By | Expected effect | Success measure |
|---|---|---|---|---|---|

**Play selected:** <name> — because the matched pattern is <pattern>, not because the score is <n>.

**Withheld:** <expansion openings withheld under `R8`, or the renewal plan withheld under `C23`,
with the condition that would release it. Print "none withheld" rather than omitting this line.>

### What would change this assessment
1. <A specific observable event that would move the band down>
2. <A specific observable event that would move it up>
3. <The data we do not have that would most change the read>

### Coverage Ledger
| Signal family | Source checked | Status | Notes |
|---|---|---|---|
| Product usage & adoption | | ✅/⚠️/❌ | |
| Commercial & contract | | | |
| Relationship & engagement | | | |
| Support & reliability | | | |
| Sentiment & VoC | | | |
| Billing & payment | | | |
| Firmographic & external | | | |

<Relationship is Partial at best where no calendar source is connected — the three `C22` fields
above must read `UNKNOWN — requires a calendar source`, never be omitted.>

**Coverage: X / 7 (Y%) → confidence capped at <level>.**
Blind spots: <which families are missing and what those specific gaps typically hide —
say which direction the error runs.>

---

*Band probabilities are stated midpoints of a rules-based model, not calibrated forecasts.
Replace them with observed renewal rates once backtested, and cite the backtest.*
