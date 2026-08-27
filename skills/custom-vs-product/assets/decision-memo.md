# The Decision Memo

> The Full artifact from `../SKILL.md`, expanded with the rows that get skipped under time
> pressure and a complete worked example. **Brief is the default; this is emitted on request, or
> when the decision goes to an engineering, product or deal review.**
>
> This memo is read twice: once now, by someone who wants a yes and has a renewal date to wave at
> you, and once in eighteen months by an engineer who inherited the component, cannot find its
> owner and is asking why it exists. **Write it for the second reader.**
>
> **Internal document.** Carrying cost, interest rate, share of ARR, the outcome word, margin, PS
> utilisation, renewal exposure and any comparison to another customer never cross the divider
> (`R18`). The customer-facing block at the bottom is the only part that leaves the building, and
> its variants live in `decline-note.md`.

**Contents**
- [1. How to use this file](#1-how-to-use-this-file)
- [2. The Brief — the default](#2-the-brief--the-default)
- [3. The Full memo — emitted verbatim](#3-the-full-memo--emitted-verbatim)
- [4. Worked example — Meridian Freight](#4-worked-example--meridian-freight)
- [5. Field notes — what makes each row valid](#5-field-notes--what-makes-each-row-valid)
- [6. The pre-return audit](#6-the-pre-return-audit)

---

## 1. How to use this file

1. Run `../scripts/carrying_cost.py <request>.json` first. Every number below comes from it; a
   memo with hand-arithmetic in it will disagree with the script within a week.
2. Fill the Brief. If nobody asks for more, that is the deliverable.
3. On request, emit §3 verbatim with the slots filled. **Delete no row.** A row with no data reads
   `UNKNOWN — requires <source>`; a deleted row is indistinguishable from a row that was clear.
4. Round every composite to two significant figures — **$110k**, not $107,340 (`R22`).
5. Print all six gates, including the ones that did not run. "Not reached" is a result.
6. Print all seven coverage families, including the missing ones, and cap confidence at what they
   permit (`R23`).

**Slots use `<angle brackets>` and every one must be filled or replaced with `UNKNOWN — requires
<source>` before the memo is returned.** The customer-facing block is the exception: a placeholder
inside it means the block is not send-ready and the sentence is deleted instead.

---

## 2. The Brief — the default

````markdown
**<Request> · <OUTCOME> · 3-yr carrying $<X> on a $<Y> build (<Z>% interest) · decide by <date>**

<Two sentences: the job, the gate that decided it, and the number that made it decide, with
provenance tags.>

**Do:** <Owner> <action> by <date>. <Expected effect.> <How we will know.>

Generality: <N_evidenced> across <n> named accounts (break-even <K*>). Confidence: <level>
(<n>/7 families). **What would change this:** <2 observable events.>

*Full memo, arithmetic and coverage ledger on request.*
````

---

## 3. The Full memo — emitted verbatim

````markdown
# Custom vs Product — <request> · <account> · <date>
**Internal document.** Carrying cost and commercial language that never reaches the customer.
**Run on:** <stage> · <pressure> · <horizon> · loaded rate $<r>/h · data as-of <date>.
<One line naming anything defaulted rather than answered, or "Nothing defaulted.">

## Bottom Line
<Three sentences: the outcome, the three-year carrying cost, the gate that decided it, and the one
decision needed with its owner and date.>

| | |
|---|---|
| Outcome | **<Generalise / Build bespoke / Work around / Decline>** · decided at Gate <n> — <name> |
| Build (principal) · 3-yr carrying | $<X> · $<Y> (interest <Z>%/yr · <s>% of account ARR) |
| ARR at stake | $<A> — <written condition / unwritten / none> |
| Generality | N_evidenced <n> across <k> named accounts · break-even K* <m> |
| Decision window | opt-out <date> − evidence window <n>d = **<date>** (<n> days) |
| Confidence | <High / Medium / Low> — <criteria met> |

## The Request
| Field | Value |
|---|---|
| Their words | "<quoted sentence>" — <name>, <title>, <date> [<source>] |
| The job | <the outcome they need, no mechanism named> |
| The trigger | <what happens today that makes it necessary, with a number> |
| What they proposed | <their mechanism, kept separate from the job> |
| Who asked | <name, title, contact.role, holds budget yes/no> |
| If we do nothing | <the written counterfactual — never left blank> |

## Gate Sequence
| # | Gate | Result | Evidence |
|---|---|---|---|
| 0 | Fork test | <clear / MATCH → DECLINE> | <extension point named, or what would have to be forked> |
| 1 | Roadmap test | <clear / MATCH → WORK AROUND / not reached> | <named owner + increment date vs decision window> |
| 2 | Workaround test | <clear / MATCH → WORK AROUND / not reached> | <fidelity % of the job at % of build effort> |
| 3 | Generality test | <clear / MATCH → GENERALISE / not reached> | <N_evidenced vs K*, accounts at G3+> |
| 4 | Payback test | <clear / MATCH → BUILD BESPOKE / not reached> | <all four clauses, each pass/fail> |
| 5 | Nothing matched | <→ DECLINE / not reached> | <gate n returned the outcome> |

## Generality Evidence
| Account | ARR | Renewal | Tier | What they asked for, verbatim | Source |
|---|---|---|---|---|---|
| <account> | $<arr> | <date> | <G0–G5> | "<quote>" — <name>, <date> | <system + record id> |

**N_evidenced = <n> · break-even K* = <m>**
**Searched:** <source (date, terms)> × 4. **Not found:** <the negatives, explicitly>.
**Coverage <n>/4 sources → N_evidenced is a <point estimate / floor>.**

## Carrying Cost
| Stream | Year 1 | Year 2 | Year 3 | Basis |
|---|---|---|---|---|
| Engineering | $<x> | $<x> | $<x> | <hours × rate + third-party> |
| Upgrade | $<x> | $<x> | $<x> | <tax hours × upgrades/yr × rate + withheld> |
| Renewal exposure | $<x> | $<x> | $<x> | ARR at stake × <band> midpoint — exposure, not a probability |
| **Total carrying** | **$<x>** | **$<x>** | **$<x>** | drift <d>%/yr |

Principal $<p> (<h>h ÷ 0.6 usable × $<r>) · **TCO(<N>) $<t>** · interest rate <z>%/yr ·
<s>% of account ARR. <One line on what the interest rate means at this account's size.>

## Rubric
| # | Dimension | Score | Evidence | Feeds |
|---|---|---|---|---|
| 1 | Generality (evidenced) | <0–4> | <N_evidenced vs K*> | Gate 3 |
| 2 | Strategic fit | <0–4> | <named PM in writing, or score 2> | Gates 3, 5 |
| 3 | Roadmap collision | <0–4> | <owner + increment, or none> | Gate 1 |
| 4 | Build effort | <0–4> | <usable weeks, and whether a design exists> | Gate 4 |
| 5 | Annual maintenance burden | <0–4> | <interest rate, share of ARR> | Gate 4 |
| 6 | Reversibility | <0–4> | <what of theirs depends on it> | Gates 0, 4 |
| 7 | Who carries the upgrade cost | <0–4> | <us every release / us at majors / nobody> | Gates 0, 4 |
| 8 | Revenue at stake | <0–4> | <written condition + signer, or unwritten> | Gates 4, 6 |
| 9 | Counterfactual if we decline | <0–4> | <the written sentence> | Gates 2, 4 |

## The Trade — only where revenue is contingent
| Structure | Cost to them | Effective discount | Recommendation |
|---|---|---|---|
| A · Services at cost | $<TCO> as a fee, maintenance quoted separately | — | <chosen / not chosen, one clause why> |
| B · Term + sunset clause | <term> years, maintenance window, sunset condition | <pct>% | **<Recommended>** |
| C · Decline + discount | <pct>% off renewal | <pct>% | <chosen / not chosen> |

`annual_trade_price` $<x>/yr · `effective_discount_pct` <pct>% of contracted ARR over <n> years.

## Disposition
**Graduation Contract** — all five, or the work is not approved:
| Field | Value |
|---|---|
| Owner | <named person, not a team> |
| Sunset review date | <calendar date, ≤12 months> |
| Graduation trigger | <observable event — default: a third account at G3+> |
| Product counterpart | <named PM> — decides by <date> |
| Fallback if product declines | <what we do, with its carrying cost> |
| Hours ceiling (`R21`) | <n>h cumulative, then a change order or a decline |

*(Decline or work around instead: the written decline, its reason, the alternative priced, the
field-signal link, and the revisit date <date>.)*

| # | Action | Owner | By | Expected effect | Success measure |
|---|---|---|---|---|---|
| 1 | <action> | <person> | <date> | <what changes> | <observable> |

## What would change this decision
| Observable event | Gate it flips | New outcome |
|---|---|---|
| <event> | <n> | <outcome> |

### Coverage Ledger
| Signal family | Source checked | Status | Notes |
|---|---|---|---|
| Product usage & adoption | <source, as-of> | <✅/⚠️/❌> | supported-path usage, accounts on a manual equivalent |
| Commercial & contract | <source, as-of> | <✅/⚠️/❌> | ARR at stake, opt-out deadline, SOW commitments |
| Relationship & engagement | <source, as-of> | <✅/⚠️/❌> | who asked, budget authority, second voice |
| Support & reliability | <source, as-of> | <✅/⚠️/❌> | ticket load attributable to the gap |
| Sentiment & VoC | <source, as-of> | <✅/⚠️/❌> | the request verbatim, the cross-base request record |
| Billing & payment | <source, as-of> | <✅/⚠️/❌> | who pays, third-party cost, PS margin |
| Firmographic & external | <source, as-of> | <✅/⚠️/❌> | regulatory driver, their stack, industry-wide need |

**Coverage: <X> / 7 (<Y>%) → confidence capped at <level>.**
Blind spots: <what the gaps hide — a missing sentiment/VoC family most often turns "nobody else
asked" into a wrong decline>.

### Assumptions
| # | Assumption | Why it was needed | If wrong |
|---|---|---|---|
| 1 | <assumption> | <what was missing> | <the threshold that moves, the gate that flips, the new outcome> |
````

---

## 4. Worked example — Meridian Freight

Every figure below is reproducible: `python3 ../scripts/carrying_cost.py ../assets/sample-request.json`.

```markdown
# Custom vs Product — nightly close-out export · Meridian Freight · 2026-08-27
**Internal document.** Carrying cost and commercial language that never reaches the customer.
**Run on:** not built yet · no revenue contingency · 3-year horizon · loaded rate $150/h ·
data as-of 2026-08-27.
Defaulted rather than answered: loaded rate, drift (0.15), evidence window (60d).

## Bottom Line
Generalise. Four named accounts want the same job and the general version breaks even at two, so
this is product work mis-filed as a bespoke request. The general build costs $60k of principal
against $160k over three years — 2.5× the bespoke principal at less than half the interest rate.
Decision needed by 2026-11-01: Jo Nkemdirim confirms Ana Ruiz (PM Integrations) as product
counterpart with a decision date, or the build proceeds as delivery-owned.

| | |
|---|---|
| Outcome | **Generalise** · decided at Gate 3 — Generality test |
| Build (principal) · 3-yr carrying | $60k · $96k (interest 46%/yr · 2.8% of account ARR) |
| ARR at stake | $240k — unwritten; Dana Osei has not made it a renewal condition |
| Generality | N_evidenced 4.0 across 4 named accounts · break-even K* 2 |
| Decision window | opt-out 2026-12-31 − evidence window 60d = **2026-11-01** (66 days) |
| Confidence | Medium — 4.5/7 families; no billing or firmographic source connected |

## Gate Sequence
| # | Gate | Result | Evidence |
|---|---|---|---|
| 0 | Fork test | clear | Runs on the documented scheduled-report extension point; no internal patched |
| 1 | Roadmap test | clear | No named product owner and no committed increment [Jira · roadmap board · 2026-08-27] |
| 2 | Workaround test | clear | Supported path reaches 65% of the job at 8% of effort — fidelity below the 80% bar |
| 3 | Generality test | **MATCH → GENERALISE** | N_evidenced 4.0 ≥ K* 2; 3 accounts at G3+ |
| 4 | Payback test | not reached | Gate 3 returned the outcome |
| 5 | Nothing matched | not reached | Gate 3 returned the outcome |

## Generality Evidence
| Account | ARR | Renewal | Tier | What they asked for, verbatim | Source |
|---|---|---|---|---|---|
| Meridian Freight | $980k | 2027-03-31 | G3 | "we need the close-out file in the drop at 06:00 with supplier codes already translated" — Dana Osei, VP Ops, 2026-08-14 | Portal REQ-4412 |
| Northwind Logistics | $420k | 2027-01-31 | G4 | Runs a nightly manual translation in a spreadsheet; no request filed | Telemetry + ticket #31908 |
| Cedar Rail | $260k | 2026-12-15 | G3 | "the codes come out raw and finance has to remap them" — Tomas Reyes, Controller, 2026-06-02 | Portal REQ-3980 |
| Halcyon Distribution | $150k | 2027-07-01 | G2 | Asked for "a better export" in a QBR; job not stated | QBR notes 2026-05-19 |

**N_evidenced = 4.0 · break-even K* = 2**
**Searched 2026-08-27:** portal (terms "close-out export", "supplier code", "code translation") ·
Zendesk 12 months, same terms · telemetry, export-then-reupload pattern, 90 days · closed-lost and
renewal notes, 8 quarters. **Not found:** no closed-lost record mentions it; no partner request log
accessible. **Coverage 3.5/4 sources → N_evidenced is a floor.**

## Carrying Cost — generalised variant
| Stream | Year 1 | Year 2 | Year 3 | Basis |
|---|---|---|---|---|
| Engineering | $13,200 | $15,180 | $17,457 | 88h × $150 (maintenance 52 · incidents 16 · support 12 · eval 8) |
| Upgrade | $2,400 | $2,760 | $3,174 | 4h × 4 upgrades × $150; rides the extension point |
| Renewal exposure | $12,000 | $13,800 | $15,870 | $240k at stake × 0.05 Watch midpoint — exposure, not a probability |
| **Total carrying** | **$28k** | **$32k** | **$37k** | drift 15%/yr |

Principal $60,000 (240h ÷ 0.6 usable × $150) · **TCO(3) $160k** · interest rate 46%/yr · 2.8% of
account ARR. The bespoke alternative is cheaper to build ($24k) and costs 100%/yr to carry — in
year one it costs exactly what it cost to build, and it serves one account.

## Rubric
| # | Dimension | Score | Evidence | Feeds |
|---|---|---|---|---|
| 1 | Generality (evidenced) | 4 | N_evidenced 4.0 ≥ K* 2, three accounts at G3+ | Gate 3 |
| 2 | Strategic fit | 2 | Adjacent to the integrations direction; no PM has confirmed in writing | Gates 3, 5 |
| 3 | Roadmap collision | 4 | Not planned; no owner and no increment on the board | Gate 1 |
| 4 | Build effort | 2 | 240h ≈ 6 usable weeks, against a written design | Gate 4 |
| 5 | Annual maintenance burden | 2 | 46% interest, 2.8% of account ARR — inside the 5% commercial threshold | Gate 4 |
| 6 | Reversibility | 2 | Their finance team reconciles against the file layout; reversible in a quarter with notice | Gates 0, 4 |
| 7 | Who carries the upgrade cost | 4 | Rides the supported scheduled-report path unchanged | Gates 0, 4 |
| 8 | Revenue at stake | 2 | $240k contingent, stated verbally by Dana Osei, not written | Gates 4, 6 |
| 9 | Counterfactual if we decline | 2 | "Dana escalates to her CFO, the March renewal opens with this on the table, and Northwind stays on the manual spreadsheet." | Gates 2, 4 |

## Disposition
**Graduation Contract**
| Field | Value |
|---|---|
| Owner | Jo Nkemdirim, Delivery Engineering |
| Sunset review date | 2027-06-30 |
| Graduation trigger | A fifth account at G3+, or two deployments completed without a fork |
| Product counterpart | Ana Ruiz, PM Integrations — decides by 2026-10-15 |
| Fallback if product declines | Own it in delivery: $28k/yr carrying, 46% interest, re-decided at the 2027-06-30 cull |
| Hours ceiling (`R21`) | 320h cumulative, then a change order or a decline |

| # | Action | Owner | By | Expected effect | Success measure |
|---|---|---|---|---|---|
| 1 | Send the field-signal request to Ana Ruiz with all four accounts | Jo Nkemdirim | 2026-09-03 | Product decision date fixed inside the window | Written reply naming a decision date |
| 2 | Confirm the Northwind manual process is the same job, not the same artefact | Jo Nkemdirim | 2026-09-10 | Northwind's G4 confirmed or re-tiered | Call note with the job stated in their words |
| 3 | Send Dana the decline-plus-alternative note and book Priya's handover | Jo Nkemdirim | 2026-09-04 | Manual 06:00 download removed this month | SFTP delivery at 05:45 confirmed for 5 consecutive days |

## What would change this decision
| Observable event | Gate it flips | New outcome |
|---|---|---|
| Ana Ruiz commits an increment with a date before 2026-11-01 | 1 | Work around until it lands |
| Northwind's manual process turns out to serve a different job | 3 | N_evidenced 2.5 vs K* 2 with 2 at G3+ — Gate 3 still fires, but on a one-account margin |
| Dana makes it a written renewal condition | 8 → 4 | Trade priced under `saying-no.md` §4 rather than absorbed |

### Coverage Ledger
| Signal family | Source checked | Status | Notes |
|---|---|---|---|
| Product usage & adoption | Product telemetry, through 2026-08-26 | ✅ Complete | Export-then-reupload pattern searched, 90 days |
| Commercial & contract | CRM, through 2026-08-27 | ✅ Complete | ARR, renewal, 90-day notice all present |
| Relationship & engagement | Email + calendar, through 2026-08-26 | ⚠️ Partial | Dana holds budget; no second voice at Meridian engaged in 90 days (`R5`) |
| Support & reliability | Ticket system, 12 months | ✅ Complete | 14 tickets across 3 accounts tagged to the gap |
| Sentiment & VoC | Request portal + QBR notes | ✅ Complete | All four requests carry verbatim text |
| Billing & payment | — | ❌ Missing | No source connected; third-party cost assumed $0 |
| Firmographic & external | — | ❌ Missing | No industry-wide driver checked; a regulatory driver would raise every tier |

**Coverage: 4.5 / 7 (64%) → confidence capped at Medium.**
Blind spots: with no firmographic source, an industry-wide driver behind these four requests is
invisible, and that is the gap that most often understates generality.

### Assumptions
| # | Assumption | Why it was needed | If wrong |
|---|---|---|---|
| 1 | Loaded rate $150/h | No rate in `cs-context` | At $220/h the general TCO(3) reaches $210k and K* stays 2, so the outcome holds — but year-one carrying becomes 3.6% of Meridian's ARR and crosses the 5% commercial threshold at any account below $700k, which is Cedar Rail and Halcyon both |
| 2 | Deploy 16h per account | No second deployment run yet | K* holds at 2 up to 200h per deployment; at 240h it becomes 3 and Gate 3 fires on a one-account margin; at 430h generalising never pays back and the choice becomes bespoke or decline |
| 3 | Request export current to 2026-08-27 | As-of date confirmed by the portal | If stale, N_evidenced is a floor and Decline is the riskier error |
```

---

## 5. Field notes — what makes each row valid

| Row | Valid | Invalid — return the memo |
| --- | --- | --- |
| Their words | A quoted sentence, a named person, a title, a date, a source record | "The customer wants…" — a paraphrase loses the framing the product team needs |
| The job | The outcome, with no mechanism named | "A webhook." If the job cannot be stated without a mechanism, discovery is incomplete: return the one question that separates them and stop |
| The trigger | A number — exceptions per month, minutes per morning, people affected | "It's painful" |
| Counterfactual | A written sentence naming who does what | Blank, which every reader interprets as "nothing happens" |
| Gate rows | All six, with the ones after the match printed "not reached" | A subset. Reasoning about a later gate after an earlier match is how a Decline becomes a Build |
| Generality rows | Named account, ARR, renewal date, tier, verbatim ask, source record | "Several customers" · an unnamed row · a tier with no source |
| Search line | Four sources, each with a date and its search terms, plus the negatives | "Searched the portal" with no terms, no date, no negatives |
| Carrying cost | Three streams × the full horizon, drift stated, arithmetic shown | A single annual number, or a total with no streams |
| Renewal exposure | `arr_at_stake × band_uplift`, labelled exposure | A churn percentage (`R22`) |
| Rubric | All nine scored, each with evidence or `UNKNOWN — requires <source>` | Eight rows. Dimensions 6 and 9 are the two that get dropped |
| Graduation Contract | Five fields plus the hours ceiling; owner is a person | An owner that is a team; a sunset of "when product ships it" |
| Actions | Action · owner · date · expected effect · success measure | "Follow up with product" |
| Coverage Ledger | Seven families, ❌ rows included, with the blind spot named | Five families and a confidence of High |
| Assumptions | A threshold that moves and the gate it flips | "May affect results" |

---

## 6. The pre-return audit

- [ ] Every number in the memo came from `carrying_cost.py`, not from prose arithmetic
- [ ] Composites rounded to two significant figures (`R22`)
- [ ] All six gate rows printed; Gate 0 evaluated explicitly and outranks revenue
- [ ] `N_evidenced` **and** `K*` both stated, and the ≥2-accounts-at-G3+ clause checked separately
- [ ] Four search sources named with dates, terms and the negatives printed
- [ ] Renewal exposure labelled exposure, never a probability
- [ ] All nine rubric dimensions scored, including reversibility and the written counterfactual
- [ ] Decision window computed as `renewal_date − notice_period_days − evidence_window` (`R1`)
- [ ] Graduation Contract complete with a person as owner and a calendar sunset date, or the
      written decline with a revisit date (`R14`)
- [ ] Debt-register row opened the same day the outcome is Build bespoke or Generalise
- [ ] Seven coverage families printed, confidence capped at what they permit (`R23`)
- [ ] Assumptions table present with a concrete consequence per row, or an explicit "none taken"
- [ ] No slot left as `<...>`; every gap reads `UNKNOWN — requires <source>`
- [ ] The customer-facing block sits below the divider, in a `text` fence, with no placeholders,
      and carries no carrying cost, interest rate, outcome word or comparison to another
      customer (`R18`), and no roadmap date without a named owner who agreed it (`R19`)
