# Cohort Loss Review — template

> Emit verbatim for a quarter or a renewal period. Every table is **ARR-weighted**: count-weighting
> hides that the large losses have different causes from the small ones. Internal document.

---

# Loss Review — <period> · <N> losses · $<X> ARR
**Internal document.** Contains risk and attribution language that must never reach a customer.
**Run on:** <period> · materiality <threshold> · facilitator <name> · data as-of <date>.

## Bottom Line
<Four sentences: what the quarter lost, the one cause carrying the most ARR, the median detection
lag, and the single decision this review is asking for.>

| Losses reviewed | Median detection lag | Savable (C+D) | Not savable (A+B) | Repeat causes |
|---|---|---|---|---|
| N · $X ARR · <a>% of period churn by ARR | <N> d (P90 <N> d) | <%> of lost ARR | <%> | <N> causes, $X ARR |

## 1. Decision-process vs competitive — reported before any reason table
The real competitor is no-decision. This table is emitted first so the quarter's reason mix is
read against it rather than instead of it. `../scripts/detection_lag.py` computes both shares.

| Class | Accounts | ARR lost | % of lost ARR | Median decision-process score | Median competitive score |
|---|---|---|---|---|---|
| **No-decision family** (`no-decision` · `deprioritised` · `budget-freeze` · `orphaned-renewal` · `budget-loss`) | | | | | |
| `competitive-displacement` — replacement confirmed twice | | | | | |
| `competitor_claimed` only — never confirmed | | | | | |
| Everything else | | | | | |

**Records with no named decision owner** (`decision_owner_vacancy_days` UNKNOWN): <n> of <N>,
$<X> ARR. That count is the argument for the field existing on live accounts.

**The tell:** a competitive share larger than the no-decision share is coding drift, not a market
finding. Re-test every competitive record against the two-source bar before accepting it, and
report what moved to `competitor_claimed`.

## 2. Reason mix by ARR
| `primary_reason` | Accounts | ARR lost | % of lost ARR | Median detection lag | Median tenure | vs prior quarter |
|---|---|---|---|---|---|---|
| **Total** | | | 100% | | | |

**Any-mention mix** (primary + secondary), which usually differs and shows the unfixed contributors:
| Reason | Records mentioning it | ARR touched |
|---|---|---|

## 3. Detection
| Metric | This period | Prior | What it decides |
|---|---|---|---|
| Median / P90 detection lag | | | The window each play must fit inside |
| Median recognition lag | | | The size of the detection problem, in days |
| Median action lag | | | The size of the capacity problem, in days |
| Flagged **after** the decision | <N> of <N> | | Whether "we intervene early" is true |
| Health-score false-negative rate (Green at T−90) | <%> | | Whether the score is worth keeping |

**Failure-mode distribution** — whether to spend on data, tooling, routing or capacity
| Mode | Accounts | ARR | % of lost ARR | Implied investment |
|---|---|---|---|---|
| `absent` · `uninstrumented` · `unalerted` · `unrouted` · `unactioned` · `undetectable` | | | | |

## 4. Savability
| Verdict | Accounts | ARR | % of lost ARR | Owning function |
|---|---|---|---|---|
| A — should never have been sold | | | | Sales / RevOps |
| B — not savable, exogenous | | | | — |
| C — savable, we did not see it | | | | CS Ops / data |
| D — savable, we saw it and it did not work | | | | CS leadership |

**A+B <%> · C+D <%>.** <Apply the honesty check out loud: above 60% in A+B, either qualification
is broken or the coding is. State which, with evidence.>

## 5. Origin vs surface
| `origin_stage` | Accounts | ARR | Most common `surfaced_stage` | Owning function |
|---|---|---|---|---|
| sales-qualification · onboarding · adoption · value-realisation · renewal-execution | | | | |

## 6. Repeat-cause register — the accountability loop
| Cause | Appearances | ARR lost (cumulative) | Fix promised | Owner | Due | Shipped? |
|---|---|---|---|---|---|---|

**On its third appearance with the fix unshipped:** escalate to the CCO with cumulative ARR
attached. Do not propose a second fix for a cause whose first fix never shipped.

## 7. Instrumentation backlog
| Signal | Appearances as earliest-detectable | ARR behind it | Failure mode | Owner | Effort |
|---|---|---|---|---|---|

## 8. Health-score false negatives
| Account | ARR | Band at T−90 | Score | What the score missed | Routed to |
|---|---|---|---|---|---|

## 9. Decisions
| # | Decision | Owner | By | Validation | Alert budget / workload impact |
|---|---|---|---|---|---|
| 1 | | | | | |
| 2 | | | | | |
| 3 | | | | | |

**Not doing:** <rejected proposals and why.>

## 10. Not reviewed this cycle
| Account | ARR | Why not reviewed | Revisit by |
|---|---|---|---|

### Assumptions
| # | Assumption | Why it was needed | If wrong |
|---|---|---|---|

### Coverage Ledger
| Signal family | Records with this family available | Status | Notes |
|---|---|---|---|
| Product usage & adoption | <n> of <N> | ✅/⚠️/❌ | |
| Commercial & contract | | | |
| Relationship & engagement | | | |
| Support & reliability | | | |
| Sentiment & VoC | | | |
| Billing & payment | | | |
| Firmographic & external | | | |

**Coverage: X / 7 (Y%) → confidence capped at <level>.** Interview response rate <%>, covering
<%> of lost ARR — state it beside every reason table, because an unrepresented half of the ARR
changes the mix.
Blind spots: <which families are thin across the cohort and what that hides.>
