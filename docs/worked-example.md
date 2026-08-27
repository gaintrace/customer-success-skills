# A Worked Example

> What the library actually produces. This is a complete `churn-risk` output for a four-account
> renewal window, written to the standard in [`SKILL-STANDARD.md`](SKILL-STANDARD.md) and the
> [Evidence Standard](../skills/cs-context/references/evidence-standard.md).
>
> Read it for the mechanics, not the numbers: how provenance is attached, how a healthy-looking
> account gets escalated anyway, how gaps are declared instead of hidden, and how ranking is
> done by dollars and deadlines rather than by score.
>
> The scoring arithmetic below is reproducible:
> `python3 skills/churn-risk/scripts/risk_score.py skills/churn-risk/assets/sample-accounts.json --today 2026-08-27`
>
> And the band probabilities it uses are replaceable with your own observed rates:
> `python3 skills/cs-context/scripts/calibrate.py history.json --capacity 25 --write`

---

## What you get by default — Brief

This is the whole output unless you ask for more. Twenty lines, one recommendation, and the
thing that would prove it wrong.

> **Renewal window · $1.12M assessed · $410k at risk (37%) · 2 accounts escalating regardless of score**
>
> **1. Delta Systems — High Risk. $310k. Decide in 5 days.**
> A P1 has been open 19 days past SLA `[Zendesk · #48211 · as-of 2026-08-26]`, seats were cut
> 25% in March `[Salesforce · Asset.Quantity]`, and invoices have slipped from 4 to 22 days
> late `[Stripe · 180d]`. Three separate pressures, one direction.
> **Do:** Priya opens the exec call and names an engineering owner by **28 Aug**.
>
> **2. Acme Corp — Critical. $148k. Decide in 6 days.**
> Auto-renew was switched off on 2 Aug `[Salesforce · Contract.AutoRenew__c]` and the champion's
> email has hard-bounced since 11 Aug. The score is irrelevant — a decision has been made.
> **Do:** Marcus runs exec-to-exec outreach by **28 Aug**, after verifying in 24h that the flag
> change was not our own re-papering.
>
> **3. Beta Industries — Watch band, escalating anyway. $620k.**
> RevOps, who signed and hold the budget, went from 22 active users to 4 since May, while the
> account total rose 18% because Marketing grew `[Amplitude · distinct_users_30d]`. Aggregate
> health reads green; the buying team has left.
> **Do:** Jo meets Dana Osei (VP RevOps) by **10 Sept** with RevOps' own numbers, not the account total.
>
> Confidence: high on Delta and Beta (7/7 families), high on Acme (6/7 — no VoC source).
> **What would change this:** RevOps back above 12 weekly actives; Delta's P1 closing with a
> committed date; confirmation that Acme's auto-renew change was ours.
>
> *Full analysis, coverage ledger and workings on request.*

Five accounts, ninety seconds, three named actions with dates. The rest of this page is what
`Full` produces when someone is going to challenge it — a QBR, a board pack, a forecast review.

---

# Churn Risk Assessment — renewals through 2027-02-28 · 2026-08-27
**Internal document.** Contains risk language that must never be sent to a customer.

## Bottom Line

$406,900 of $1.12M assessed ARR is at risk on an exposure-weighted basis (36%), concentrated in
two accounts whose opt-out deadlines fall inside the next week. **Delta Systems is the single
most urgent** — five days to opt-out, an open P1 past 14 days, and a seat reduction already
taken this term; Priya Raman (VP CS) owns the exec call, due 2026-08-28. Beta Industries looks
healthy on every aggregate metric and is escalating anyway: the team that holds the budget has
stopped using the product while the account total grew.

| | |
|---|---|
| ARR assessed | $1,120,000 across 4 accounts |
| ARR at risk (exposure-weighted) | $406,900 (36.3%) |
| Critical / High / At Risk / Watch / Secure | 1 / 1 / 0 / 1 / 1 |
| Accounts escalating regardless of score (P0 pattern) | 2 |
| Most urgent | Delta Systems — open P1 + seat reduction + 5 days to opt-out — Priya Raman — by 2026-08-28 |
| Assessment confidence | **Medium** — 3 of 4 accounts at ≥86% coverage, 1 at 56% |
| Weight profile | enterprise (annual contracts, notice periods, named champions) |

## Priority Table

Ranked by Action Priority = Exposure × Urgency × Savability. **Not** by score — Delta outranks
Acme despite a lower score, because it carries twice the ARR at a similar deadline.

| # | Account | ARR | Band | Score | P0 | Pattern | Days to opt-out | Exposure | Priority | Owner | Next action (by) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Delta Systems | $310,000 | High Risk | 81.7 | | Death by a thousand tickets · Budget squeeze · Contraction spiral | **5** | $186,000 | $279,000 | Priya Raman | Exec call + named eng owner — 2026-08-28 |
| 2 | Acme Corp | $148,000 | Critical | 85.0 | ⚠ | Decapitation · Quiet quit | **6** | $125,800 | $226,440 | Marcus Bell | Exec-to-exec outreach — 2026-08-28 |
| 3 | Beta Industries | $620,000 | Watch | 34.7 | ⚠ | Buyer disconnect | 72 | $93,000 | $128,340 | Jo Nkemdirim | Meet the economic buyer — 2026-09-10 |
| 4 | Gamma Ltd | $42,000 | Secure | 13.0 | | — | 80 | $2,100 | $2,415 | pooled | Cadence touch — 2026-09-15 |

## Not worked this cycle

Nothing was skipped in a window this small. In a full book, the accounts that scored but will
not receive a play are listed here with the reason and a revisit date — an undeclared decision
to skip an account is how accounts get skipped for a quarter.

---

## Account Card — Beta Industries

Included here rather than Acme because it is the instructive one: **every aggregate metric is
healthy and the account is escalating anyway.**

**Risk 34.7/100 · Watch · Confidence High · ARR $620,000 · Renewal 2027-02-05 · Opt-out 2026-11-07 (72 days)**

**The call:** Beta's aggregate usage is up 18% quarter on quarter and its NPS is 9, but the
Revenue Operations team that signed the contract and holds the budget has gone from 22 active
users to 4 since May, while the growth is entirely in Marketing — a team with no line-item
authority for this spend. At the February renewal, the person asked to approve $620,000 will
be approving a product their own team no longer uses. The score says Watch; the pattern says
escalate, and the pattern is right.

### Signals fired
| Family | Signal (ID) | Evidence | Tier | Lead time |
|---|---|---|---|---|
| Product usage & adoption | Buying-team usage decay (U2, segmented) | RevOps active users 22 → 4 since 2026-05-01 `[Amplitude · distinct_users_30d, group=revops · through 2026-08-24]` | Observed | 90–200d |
| Relationship & engagement | Buyer-side engagement (Z1) | No interaction with an economic-buyer or champion contact since 2026-06-18 `[Gmail + Calendly · interaction · 70 days]` | Observed | 60–150d |
| Relationship & engagement | Exec sponsor not met (R2) | Last exec-level contact 2026-03-12, two quarters ago `[Salesforce · Event]` | Observed | — |

### Checked and clear
| Family | What was checked | Result |
|---|---|---|
| Commercial & contract | Auto-renew, notice, seat count, discount expiry, procurement activity, competitor mentions | Auto-renew on; no changes since contract start `[Salesforce · Contract · through 2026-08-26]` |
| Support & reliability | Ticket volume normalised per 100 seats, P1s, reopens, SLA, CSAT trend | 3.1 tickets/100 seats/month, within the healthy band; no P1s in 180d; reopen rate 6% `[Zendesk · through 2026-08-26]` |
| Sentiment & VoC | NPS, CSAT, transcript sentiment | NPS 9 on 2026-07-02 from the Marketing lead — **note: not from the buying team**, see Contradictions `[Delighted · through 2026-08-01]` |
| Billing & payment | Invoice status, DSO vs own history, payment method | Clean; zero late payments in 24 months `[Stripe · through 2026-08-27]` |
| Firmographic & external | Funding, M&A, layoffs, exec changes, headcount | Series C closed 2026-06-30; headcount +14% — flagged to `expansion-finder`, not a risk `[Crunchbase · through 2026-08-25]` |

### Not checkable
None. All seven families had a connected source.

### Override floors applied
None fired. Verified individually: auto-renew on, no termination language, no bulk export, core
usage non-zero, economic buyer present in the org (though not engaged), opt-out 72 days out with
a renewal conversation scheduled, no seat reduction, no competitor named, no ageing P1.

### Compound patterns matched
| Pattern | Priority | Composition observed | Implication |
|---|---|---|---|
| **Buyer disconnect** | P0 | Aggregate usage +18% QoQ while RevOps (the contracted department) fell 82% | The health score is measuring the wrong population. Escalate regardless of band. |

### Contradictions
| Signal A | Signal B | Reading | Tiebreak rule applied |
|---|---|---|---|
| Aggregate usage +18% QoQ `[Amplitude]` | RevOps usage −82% `[Amplitude, segmented]` | Growth is in Marketing (34 of 38 active users), a team with no budget authority for this line item. Product-level health masks buyer-level risk. | **Buying-team usage over aggregate usage** (evidence-standard §8, rule 3 over rule 4) |
| NPS 9, 2026-07-02 | The respondent is the Marketing lead, not the economic buyer | The score belongs to a person, not the account, and to the wrong person. Do not treat it as account sentiment. | Sentiment ranks last in the tiebreak order |

### Score breakdown
| Family | Risk | Weight | Contribution | Top driver |
|---|---|---|---|---|
| Relationship & engagement | 45 | 20 | 9.0 | No buyer-side contact in 70 days |
| Product usage & adoption | 30 | 22 | 6.6 | Buying-team decay, offset by aggregate growth |
| Commercial & contract | 20 | 25 | 5.0 | Clean, but no renewal conversation held yet |
| Sentiment & VoC | 20 | 9 | 1.8 | Respondent is not the buyer |
| Support & reliability | 15 | 12 | 1.8 | — |
| Firmographic & external | 10 | 5 | 0.5 | — |
| Billing & payment | 0 | 7 | 0.0 | — |
| **Weighted (7 of 7 families)** | | **100** | **24.7** | |
| **After pattern bonus (+10)** | | | **34.7** | Buyer disconnect |
| **After floors** | | | **34.7** | None fired |

### Priority arithmetic
```
Exposure        = $620,000 × 0.15 (Watch midpoint)   = $93,000
Urgency         = 72 days to opt-out                 = 1.15
Savability      = addressable (relationship + value) = 1.20
Action Priority = 93,000 × 1.15 × 1.20               = $128,340
```

### Intervention plan
**Play: Buyer re-engagement** — selected because the matched pattern is Buyer disconnect, not
because the score is 34.7.

| # | Action | Owner | By | Expected effect | Success measure |
|---|---|---|---|---|---|
| 1 | Segment usage by department and quantify the RevOps gap precisely | Jo Nkemdirim | 2026-08-31 | A number the buyer will recognise as theirs | Written analysis with per-team actives |
| 2 | Build the value story on RevOps' original objective from the 2025 business case — including the honest statement that their number is bad | Jo Nkemdirim | 2026-09-04 | Removes the credibility risk of arriving with Marketing's growth figure | One-page value memo |
| 3 | Meet Dana Osei (VP RevOps, economic buyer) directly | Jo Nkemdirim | 2026-09-10 | Establishes whether the use case moved or died | Meeting held; objective stated in her words |
| 4 | Convert the Marketing lead into a second champion with budget influence | Jo Nkemdirim | 2026-09-30 | Two constituencies at renewal instead of one absent one | Marketing lead attends the Q4 review |
| 5 | If the use case has genuinely moved, drive a formal budget transfer with Marketing's leader as the new economic buyer | Amara Diallo (AM) | 2026-10-15 | The renewal has an owner who uses the product | Budget owner confirmed in CRM |
| 6 | Open a risk record persisting to the 2026-11-07 opt-out regardless of how step 3 goes | Jo Nkemdirim | 2026-08-28 | A good first meeting does not close the risk prematurely | Record open at the T-90 review |

### What would change this assessment
1. **Down:** RevOps active users return above 12 (55% of baseline) for four consecutive weeks.
2. **Down:** A documented budget transfer to Marketing with a named economic buyer who uses the product.
3. **Up:** Dana Osei declines or defers the September meeting twice — that converts this to a Value vacuum and moves the band to At Risk.

### Coverage Ledger
| Signal family | Source checked | Status | Notes |
|---|---|---|---|
| Product usage & adoption | Amplitude (through 2026-08-24) | ✅ Complete | 26 months history; department segmentation available |
| Commercial & contract | Salesforce (through 2026-08-26) | ✅ Complete | Notice period verified against the signed MSA, not the CRM field |
| Relationship & engagement | Gmail, Calendly, Slack Connect (through 2026-08-27) | ✅ Complete | All three account-team mailboxes connected |
| Support & reliability | Zendesk (through 2026-08-26) | ✅ Complete | Jira linked for escalated tickets |
| Sentiment & VoC | Delighted (through 2026-08-01) | ✅ Complete | Only 2 respondents — below the ≥3 threshold, so scored but flagged |
| Billing & payment | Stripe (through 2026-08-27) | ✅ Complete | — |
| Firmographic & external | Crunchbase (through 2026-08-25) | ✅ Complete | — |

**Coverage: 7 / 7 (100%) → confidence High.**
Blind spots: none structural. The one caveat is the VoC sample size — two respondents, neither
of them the economic buyer — so sentiment is reported but carries no weight in the call.

---

## What this example is demonstrating

| Mechanism | Where to see it |
| --- | --- |
| **Provenance on every number** | Every figure carries `[system · field · date]` |
| **Evidence tiers kept separate** | "Observed" throughout; no inference is dressed as a measurement |
| **The false-green caught** | Beta scores 34.7 and escalates anyway, because the P0 pattern overrides the band |
| **Buying-team usage separated from aggregate** | The Contradictions table, and the tiebreak rule that resolved it |
| **Opt-out deadline governs, not the renewal date** | Beta renews in February and decides in November |
| **Non-findings printed** | "Checked and clear" is a section, not an omission |
| **Ranking by dollars and deadlines** | Delta outranks Acme despite a lower score; the arithmetic is shown |
| **Confidence tied to coverage** | Gamma's 56% coverage caps it at Low and says which families are missing |
| **Play follows the pattern, not the score** | Buyer re-engagement, chosen because of Buyer disconnect |
| **Every action has an owner, a date and a measure** | The intervention table has no row without all five columns |
| **Falsifiability stated** | "What would change this assessment" names three observable events |
| **No false precision** | Bands and midpoints, explicitly labelled as a rules-based ordering rather than a forecast |
