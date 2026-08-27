# The Position Pack — the Full output template, verbatim

> Emitted only when Full is asked for, when the pack is going to a deal desk or an approver, or
> when someone will challenge the number. **Brief is the default** (`§4E`) and lives in `../SKILL.md`.
>
> Internal throughout. The only part that leaves the building is §15, and it leaves inside a fence.

Two rules are structural rather than stylistic, and both are enforced below:

- **§3 gates before rungs.** The Gates table is generated before the ladder table. A rung offered
  under a failed gate is invalid output (`C14`, `C10`).
- **Every ladder and counter row carries a non-empty What-we-get cell** (`C12`). A row without one
  is deleted, not shipped.

---

```markdown
# Negotiation Position — <Account> · ATR $<X> · <mode>
**Internal.** Contains walk-away, gate status, ladder and precedent language that must never reach
the customer. **Data as-of <date>.** <One line naming any default this ran on.>

## Bottom Line
<3 sentences: the position, the number, the single move that most changes the outcome, and its owner.>

| | |
|---|---|
| ATR | $X [<system> · <field> · as-of <date>] |
| Renewal `R` · **Opt-out `D`** | <date> · **<date> (<N> days)** — the governing date |
| Auto-renew · current discount and expiry | on/off, changed <date> · <%> to <date> — an expiring discount is itself an increase |
| Uplift clause · cap · index | <%> · <cap> · <CPI/fixed/greater-of> [<contract> §<clause>] |
| **Signs · decides · influences** | <name> · <name> · <name> — `UNKNOWN` on `signs` fails Gate A |
| **Days since last business conversation** | **<n>** [<system> · `interaction.occurred_at` · as-of <date>] · procurement active: yes/no |
| Position this cycle · walk-away | Rung <0–4> <name> · $X and <terms>, approved by <name> on <date> |
| Health band · confidence | <band> from `churn-risk` <date> · High/Medium/Low — <criteria met> |

## 1. The Position
| # | Element | Content | Source / tier | Gap |
|---|---|---|---|---|
<Six rows: value delivered · price position · their alternatives · switching cost · walk-away ·
ask stack beyond price. Add a row naming their constraint — budget period, scope, timing, or
genuinely price — and whether the economic buyer is reachable without procurement's permission.>

## 2. Uplift and Justification — Rung <n>, <name>. Ask <%> → $<new ARR>
| Order | Justification | Evidence held | Producible on demand? |
|---|---|---|---|
<Five rows in the fixed order: outcomes in their metrics · product shipped and adopted · usage
growth and true-up · the contractual clause · list-price movement. Value first, clause fourth.>

**Break-even:** an uplift of <u> is value-neutral at <u/(1+u)> of added churn probability —
arithmetic for ordering the decision, not a forecast (`R22`).

## 3. The Gates, then the Ladder
| Gate | Status | Evidence | Action if FAIL |
|---|---|---|---|
| A · Authority (`C14`) | PASS / FAIL | `signs` = <name>; in the conversation on <date> | Authority test, in its exact words — <Owner>, by <date> |
| B · Business thread (`C10`) | PASS / FAIL | <n> days since <date>; procurement active <yes/no> | Book <named meeting · named person · named subject> — <Owner>, by <date> |

**Ladder status: OPEN / BLOCKED — Gate <A/B>.** When BLOCKED, every `Offer?` cell below reads
`BLOCKED — Gate <A/B>` and §4's counter is the gate's action, not a rung.

| # | Give | Annual cost $ | Lifetime cost $ (assumed tenure <n>y) | **What we get** | Approver | Offer? |
|---|---|---|---|---|---|---|

<Every row's **What we get** cell is filled. A row with an empty cell is deleted, not shipped
(`C12`). "Goodwill", "the relationship", "they renew", "they stop asking" and an expansion inside
90 days of `D` are not gets.>

**Never without VP+:** notice window · auto-renew clause · uplift clause · audit and true-up rights.
**Never at any level:** MFN · unlimited liability · TfC with no fee or notice · source-code escrow
without a deal-desk exception · unmetered usage on a metered product · an SLA credit we cannot
operate · a permanent base reprice dressed as a one-time credit. <Printed every run, requested or
not.>

## 4. Live Demand → Counter, or Structures Compared   <!-- whichever mode applies -->
| What they asked | What it costs us | The counter | **What we get** | Approval | Reply due |
|---|---|---|---|---|---|

| Structure | Yr1 | Yr2 | Yr3 | Total | Effective annual rate | Terms to hold | Forecast consequence |
|---|---|---|---|---|---|---|---|

## 5. Timing and Actions
| Milestone / action | Owner | By (offset from `D`) | Expected effect | Success measure |
|---|---|---|---|---|

<When Gate B failed, the first row is the business-thread meeting, dated before any commercial
reply. When Gate A failed, the first row is the authority test.>

## What would change this position
<2–3 specific, observable events that would move the rung, the walk-away or the structure.>

### Assumptions
| # | Assumption | Why it was needed | If wrong |
|---|---|---|---|
| 1 | Standard-uplift position (rung 2) | `Position` unanswered; `cs-context` §2 sets a standing uplift | Hold-flat removes the T-90 proposal step and trades the hold for a 24-month term instead |
| 2 | 4-year expected tenure in the discount projection | No cohort retention curve supplied | Lifetime cost of rung 5 moves ±$<x> per year of tenure; rungs 4 and 5 can invert |
| 3 | Last business conversation taken from the newest logged interaction (<date>) | No interaction export beyond <date> | An unlogged review inside the last 21 days opens Gate B and unblocks the ladder this week |

### Coverage Ledger
| Signal family | Source checked | Status | Notes |
|---|---|---|---|
| Product usage & adoption | | ✅/⚠️/❌ | |
| Commercial & contract | | | |
| Relationship & engagement | | | `signs` and `days_since_business_thread` both come from here |
| Support & reliability | | | |
| Sentiment & VoC | | | |
| Billing & payment | | | |
| Firmographic & external | | | |

**Coverage: X / 7 (Y%) → confidence capped at <level>** (`R23`). Blind spots: <a commercial gap
produces a wrong clause stack; a relationship gap fails both gates closed, which is the correct
behaviour and still a gap.>
```

---

## §15 — the customer-facing draft

Appended only when a draft is due. Skeleton and rules: `../SKILL.md` Output Template. The five drafts
themselves: `../assets/negotiation-comms.md`. Every fence is scanned with
`../scripts/pre_send_scan.py` and exits 0 before it is emitted.
