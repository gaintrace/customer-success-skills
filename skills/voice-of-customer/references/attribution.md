# Revenue Attribution, Trend Math and Routing

> A theme without dollars is a request. This file holds the attribution rules, the splits that
> make a theme actionable, the trend arithmetic that separates a growing theme from a noisier
> quarter, the ranking formula, and the routing matrix that decides who owns each theme.

**Contents**
1. [What each number is allowed to claim](#1-what-each-number-is-allowed-to-claim)
2. [Attribution rules](#2-attribution-rules)
3. [The four splits](#3-the-four-splits)
4. [Trend and emergence math](#4-trend-and-emergence-math)
5. [Ranking](#5-ranking)
6. [Routing matrix](#6-routing-matrix)
7. [Sizing the fix and the cost of not fixing](#7-sizing-the-fix-and-the-cost-of-not-fixing)
8. [Attribution errors that get a register rejected](#8-attribution-errors)

---

## 1. What each number is allowed to claim

The fastest way to lose an exec staff's trust is to present attributed ARR as revenue at risk.
Label every column exactly, and print this legend under the register.

| Number | Definition | May be described as | Must never be described as |
| --- | --- | --- | --- |
| **Attributed ARR** | Σ `account.arr` for accounts with ≥1 primary-coded mention | "Revenue of the accounts raising this" | "Revenue at risk" or "the size of the opportunity" |
| **Risk-weighted ARR** | Σ (`account.arr` × band probability) | "Exposure-weighted, using rules-based band midpoints" | "Expected loss" or a calibrated forecast |
| **Renewal exposure** | Σ `account.arr` where `opt_out_deadline ≤ today + 120d` | "Revenue that decides within the window" | "Revenue that will churn over this theme" |
| **Realised loss** | Σ `churn_event.arr_lost` where the theme is a stated or assessed reason | "ARR already lost with this theme cited" | "ARR lost because of this theme" — unless the assessed cause agrees with the stated one |
| **Reach** | accounts mentioning ÷ accounts in scope | "Share of accounts raising it" | "Share of customers affected" — non-mentioners are unmeasured, not unaffected |

Band probabilities come from `churn-risk`: Secure .05 · Watch .15 · At Risk .35 · High .60 ·
Critical .85. These are **stated probabilities of a rules-based model, not calibrated forecasts.**
Print that sentence under any table that uses them. If the health model has been backtested
against actual renewal outcomes, replace the midpoints with the observed rates and cite the
backtest.

---

## 2. Attribution rules

| # | Rule | Why |
| --- | --- | --- |
| 1 | **Account grain.** Attribution sums `account.arr` once per account per theme, regardless of mention count | Otherwise a single account with twelve tickets carries twelve times its ARR |
| 2 | **Primary code only.** Secondary codes never attract ARR | Secondary attribution double-counts the base — the sum of theme ARR would exceed total ARR, and a reviewer will notice |
| 3 | **Use ARR as of the period end**, with `arr_as_of` recorded | Mid-period ARR changes make the register unreconcilable against finance |
| 4 | **Exclude `account.is_internal = true`** | Employee and sandbox accounts inflate every theme, usually the technical ones |
| 5 | **Churned accounts are attributed at their ARR at churn**, in a separate `realised loss` column, never in Attributed ARR | Mixing live and dead revenue in one column makes the total meaningless |
| 6 | **Anonymous mentions carry no ARR.** Record them, count them in reach as UNKNOWN, attribute nothing | An unattributable review cannot fund a roadmap decision |
| 7 | **Multi-entity accounts attribute at the contracting grain** (`parent_account_id` where the contract sits) | Subsidiary-level attribution understates enterprise themes, which is exactly the theme class that matters most |
| 8 | **Print the unattributed share** — mentions with no resolvable account, as a count and a % of mentions | Below 90% attribution the register's dollar figures are a floor, and the reader must know that |

**Worked attribution**

```
Theme INT-02 (integration unreliable), Q3 FY26

Accounts mentioning (deduped, primary code only):
  Acme Corp        ENT   $480,000   band At Risk (.35)   opt-out 2026-10-14
  Northwind        ENT   $310,000   band Watch   (.15)   opt-out 2027-02-01
  Brightline       MM    $ 92,000   band High    (.60)   opt-out 2026-09-30
  Vector Labs      MM    $ 74,000   band Secure  (.05)   opt-out 2027-05-20
  Pellet.io        SMB   $ 18,000   band At Risk (.35)   opt-out 2026-11-02

Attributed ARR    = 480,000 + 310,000 + 92,000 + 74,000 + 18,000        = $974,000
Risk-weighted ARR = 168,000 + 46,500 + 55,200 + 3,700 + 6,300           = $279,700
Segment split     = ENT $790,000 (81%) · MM $166,000 (17%) · SMB $18,000 (2%)
Band split        = At Risk $498,000 · High $92,000 · Watch $310,000 · Secure $74,000
Renewal exposure (opt-out ≤ today + 120d, today = 2026-08-27):
                    Acme 2026-10-14 ✓ · Brightline 2026-09-30 ✓ · Pellet.io 2026-11-02 ✓
                  = 480,000 + 92,000 + 18,000                          = $590,000
```

The reading is not "this theme is worth $974k". It is: *five accounts raised it, 81% of the
attributed revenue is Enterprise, and $590k of it decides inside the next four months.* That is a
sentence a CFO can act on.

---

## 3. The four splits

Print all four for every theme in the register. Each answers a different executive question.

| Split | Question it answers | How it changes the decision |
| --- | --- | --- |
| **Segment** (ENT/MM/SMB by ARR) | "Who is asking — the ones who pay us, or the volume?" | An ENT-weighted theme goes to Product with a named renewal list. An SMB-volume theme usually goes to Docs, Support deflection, or packaging |
| **Health band** | "Are these accounts already leaving, or are they healthy and telling us early?" | Healthy accounts raising a theme are the most credible signal you get — they have no incentive to exaggerate. At Risk accounts raising it may be constructing a justification |
| **Role** (`contact.role`) | "Did the person who signs the contract say this?" | Admin-only themes rarely survive budget scrutiny. Economic-buyer mentions justify a roadmap slot on their own |
| **Tenure** (`account.tenure_days`) | "Is this an onboarding failure or a maturity ceiling?" | <180 days concentrates in ONB and ADP and is a CS/enablement fix. >2 years concentrates in CAP and REP and is a roadmap fix |

**The pairing that matters most.** Cross segment with health band. A theme raised by $4M of
Enterprise ARR sitting in Secure and Watch is a roadmap investment with a long runway. The same
dollar figure sitting in High and Critical is a save motion, and the roadmap will not arrive in
time — that theme routes to CS and Sales, not to Product, and the honest recommendation is a
commercial one.

---

## 4. Trend and emergence math

### 4.1 Share of voice

Raw counts rise when collection rises. The comparable unit is:

```
share_t = mentions_theme_t / mentions_total_t
```

Report both raw counts and share. When they disagree — count up, share down — the theme is
**shrinking relative to everything else**, and the corpus grew. Say that.

### 4.2 The emergence screen

Three conditions, all required:

| Condition | Threshold | Purpose |
| --- | --- | --- |
| Minimum volume | ≥5 mentions across ≥3 accounts in the current period | Below this, growth is noise |
| Relative share change | `share_now / share_prior − 1 ≥ 0.50` | Removes corpus-growth artifacts |
| Absolute share change | `share_now − share_prior ≥ 0.02` | Removes tiny-base percentage explosions |

Then compute the two-proportion screen:

```
p_pool = (x_now + x_prior) / (n_now + n_prior)
z      = (share_now − share_prior) / sqrt( p_pool × (1 − p_pool) × (1/n_now + 1/n_prior) )
```

Flag at |z| ≥ 2.0. **Label it a screen, not a significance test.** Mentions are not independent
draws — one account can produce several, collection is not randomised, and the two periods share
accounts. The z-value is a consistent way to rank candidates for attention; it does not license
the word "significant".

### 4.3 Classification

| Status | Condition |
| --- | --- |
| **Emerged** | ≥5 mentions now, <3 in the prior period |
| **Growing** | All three emergence conditions met, and present in the prior period |
| **Flat** | Share change within ±50% relative |
| **Fading** | `share_now / share_prior − 1 ≤ −0.35` with ≥5 mentions in the prior period |
| **Resolved** | Fading, plus a shipped fix, plus ≥60 days of post-ship mention data, plus ≥1 `polarity = praise` mention post-ship |
| **Newly visible** | Growth attributable to a channel added this period. **Not growth** — a measurement change |

The newly-visible label is the honest answer to the most common way a VoC readout misleads. If
you connected call transcripts this quarter and severity-3 capability themes tripled, the world
did not change; your instrument did. Compute the counterfactual: recompute share **excluding the
new channel** and report both.

### 4.4 The post-ship check

The only defensible answer to "didn't we fix this?":

```
mentions per 30 days, 90 days before ship  →  mentions per 30 days, days 30–90 after ship
```

Exclude the first 30 days post-ship — adoption of a fix lags its release, and the pre-fix backlog
is still arriving. If mentions do not fall, the fix addressed a different problem from the one
the theme describes, which is a coding finding as much as a product one: run the split test.

---

## 5. Ranking

```
Intensity    = mean(severity) / 2                     # 1.0 → 0.5, 2.0 → 1.0, 3.0 → 1.5
Trajectory   = emerged 1.4 · growing 1.2 · flat 1.0 · fading 0.8 · newly visible 1.0
Tractability = addressable this quarter 1.2 · this year 1.0 · structural / won't-fix 0.5

Theme Priority = Risk-weighted ARR × Intensity × Trajectory × Tractability
```

Tie-break, in order: (1) fewest days to the nearest opt-out deadline among mentioning accounts;
(2) higher Enterprise ARR share; (3) higher count of economic-buyer mentions. State which
tie-break you used.

**Worked ranking**

| Theme | Risk-wtd ARR | Mean sev | Intensity | Trajectory | Tract. | Priority | Rank |
| --- | --- | --- | --- | --- | --- | --- | --- |
| INT-02 integration unreliable | $279,700 | 2.4 | 1.20 | growing 1.2 | 1.2 | **$483,322** | 1 |
| CAP-01 missing capability, value path | $412,000 | 2.8 | 1.40 | flat 1.0 | 0.5 | **$288,400** | 3 |
| SUP-02 resolution quality | $196,000 | 2.1 | 1.05 | emerged 1.4 | 1.2 | **$345,744** | 2 |
| ONB-03 enablement gap | $88,000 | 1.6 | 0.80 | fading 0.8 | 1.2 | **$67,584** | 4 |

Arithmetic check on row 1: `279,700 × 1.20 × 1.2 × 1.2 = 483,321.6`. Note the inversion —
SUP-02 at $345,744 outranks CAP-01 at $288,400 despite less than half the risk-weighted
ARR, because it is tractable this quarter and CAP-01 is structural. That inversion is the point
of the formula: **a large problem you will not fix this year should not consume the roadmap slot
that a smaller, fixable one could use.** Report CAP-01 anyway, in §7 "Not Doing", with the reason
and the reconsider trigger — burying it is how the same theme reappears every quarter unowned.

Then cut the list at N, the capacity-gate number.

---

## 6. Routing matrix

One accountable owner per theme. Other functions are **consulted** and named as such.

| Destination | Owns themes where… | The packet must contain | SLA to a decision | "Done" looks like |
| --- | --- | --- | --- | --- |
| **Product** | The capability is absent, hard, or wrong (CAP, ADP, REP, INT, ADM) | Attributed + risk-weighted ARR · segment and band splits · the job-to-be-done in the customer's words · current workaround and its cost · 3 verbatims with account, role and date · renewal exposure table · what would change if fixed | 2 weeks to accept/decline/defer | A roadmap item with a target release, or a written decline with a reason routed back to §7 |
| **Engineering** | Reliability, performance, data integrity, regressions (REL) | Incident or ticket IDs · affected accounts and ARR · frequency and duration · the customer-visible consequence · SLA breaches | 5 business days | A tracked defect with a severity and a committed date |
| **Support** | Response, resolution, escalation, context loss (SUP) | Repeat-contact drivers with cluster sizes · reopen rate for the cluster · deflection candidates · the macro or doc that is missing | 1 week | A staffing, process, macro or knowledge-base change with a measured before/after |
| **CS** | Onboarding, enablement, coverage, commitments, value evidence (ONB, ACC, ROI) | Account list with owner and health band · what was promised and by whom · which success-plan milestone is affected · time-to-value against target | 1 week | A named play per account with owner and date, plus a process change if it recurs |
| **Sales** | The expectation was set in the sale (ONB-04, ROI-04, CAP where scope was oversold) | The specific claim made, its source (recording, deck, email), the accounts affected, and the ARR | 2 weeks | A change to the qualification or handover checklist, evidenced by the next cohort |
| **Pricing / Packaging** | The complaint is about the boundary of a plan, not the product (PRC, CAP-02) | Which capability sits in which tier · the accounts blocked by the boundary · the ARR on each side of it · competitive comparison if held | Quarterly pricing cycle | A packaging decision, or a documented decision to hold and why |
| **Docs / Education** | The capability exists and was not found or understood (ADP-03, REP-04, ONB-03) | The exact question customers asked, verbatim · search terms used · the article that should have answered it | 1 week | Published content, with search-to-answer and ticket-deflection measured after |
| **Exec staff** | Attributed ARR exceeds the escalation threshold **and** no function has accepted ownership, or the fix crosses more than two functions | Everything above, plus the decision options with cost and consequence for each, and a recommendation | Next staff meeting | A named owner and a funded decision. Exec staff exists to assign ownership, not to admire the problem |

**Routing rules**

1. A theme routed to two owners is routed to nobody. Pick one; name the consulted functions.
2. Route the **assessed cause**, not the stated reason. A "too expensive" theme whose assessed
   cause is value non-realisation routes to CS, not to Pricing, and the packet says why.
3. CAP-02 (gated by plan) always routes to Pricing, never to Product. The capability exists.
4. A theme with no owner after one full period escalates to exec staff automatically. Unowned
   themes do not age out; they accumulate.
5. Every routed theme carries **action · owner · date · expected effect · success measure**.

---

## 7. Sizing the fix and the cost of not fixing

Executives will ask both. Prepare both, and mark the ones you cannot compute.

**Cost of not fixing** — computed, with the arithmetic shown:

```
Renewal exposure         = Σ arr where opt_out_deadline ≤ today + 120d          (computed)
Support load             = tickets in the theme's cluster × loaded cost/ticket  (computed if
                           cost/ticket is known; else UNKNOWN — requires Support finance)
Expansion suppressed     = Σ opportunity.amount for open expansion opps on mentioning accounts
                           whose stage has not advanced in 60d                  (computed)
Deal impact              = Σ opportunity.amount for lost deals citing the theme (computed from
                           opportunity.loss_reason, flagged as an unverified rep-entered field)
```

**Cost to fix** is the owning function's estimate. Never invent it. Write
`UNKNOWN — requires <function> estimate` and put the estimate request in the routing packet with
a date. An analyst-invented engineering estimate is the fastest way to have an entire register
discarded.

**The ratio is a prompt, not an answer.** Present exposure alongside the owner's cost estimate
and let the owner make the call. VoC's job is to make the trade-off visible with honest numbers
on both sides, not to arbitrate it.

---

## 8. Attribution errors

| Error | Effect | Correction |
| --- | --- | --- |
| Counting mentions instead of accounts | The loudest customer wins | Rule 1 — account grain |
| Attributing ARR on secondary codes | Theme ARR exceeds total ARR | Rule 2 — primary only |
| Presenting attributed ARR as ARR at risk | The register is dismissed the first time someone checks | §1 legend, printed under the table |
| Using the renewal date instead of the opt-out deadline | Exposure is understated and the window has already closed | `renewal_date − notice_period_days` |
| Ranking by mention count | SMB volume outranks Enterprise severity | §5 formula |
| Ignoring tractability | The register is topped by a theme nobody will fix, every quarter | Tractability multiplier, and §7 "Not Doing" |
| Comparing raw counts across periods | A bigger corpus reads as a worsening product | Share of voice |
| Calling a z-value significant | The claim does not survive a statistician in the room | Label it a screen |
| Dropping unattributable mentions silently | The dollar totals look more complete than they are | Print the unattributed share |
| Attributing churned ARR into the live column | The total cannot be reconciled with finance | Separate `realised loss` column |

---

## 9. Sentiment × behaviour patterns

Join each respondent account's sentiment to `usage_daily` and its commercial state. **The
disagreements are the output** — the agreements tell you nothing you did not already know.

| Pattern | What it looks like | Reading | Action |
| --- | --- | --- | --- |
| **Hollow promoter** | NPS 9–10, core actions down ≥40% over 8 weeks | The score belongs to a person, not the account — often a sponsor who likes you and no longer uses you | Treat sentiment as expired; run `churn-risk` |
| **Expanding detractor** | NPS 0–6, seats or consumption up | The complaint is real and they are stuck with you. Highest-value fix target; the goodwill is already spent | Route the theme with the retention argument; close the loop personally |
| **Silent grower** | Zero feedback, usage and seats up | Fine today, invisible tomorrow. No relationship equity and no warning system | Add to the outreach list; do not count as healthy sentiment |
| **Loud small** | Many mentions, low ARR, low severity | Volume is not weight. Check whether the loudest account is one person | Rank by ARR, not mention count |
| **Quiet large** | High ARR, one mention, severity 3 | The most under-weighted pattern in every register | Escalate; one enterprise severity-3 mention outranks fifty severity-1 SMB mentions |
| **Praise-then-leave** | Positive survey, then auto-renew off or notice served | Sentiment lost to a commercial decision made elsewhere | Commercial action wins the tiebreak (`R2`); evidence-standard §8 |

Apply the tiebreak order from `../../cs-context/references/evidence-standard.md` §8 when signals
conflict: commercial actions > economic-buyer relationship > buying-team usage > aggregate usage >
sentiment scores. **Sentiment is last.** State the rule you applied, every time.

