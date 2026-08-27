---
name: renewal-negotiation
description: "When money, terms or leverage are on the table at a renewal and the user has to decide what to ask for, what to trade, and what to refuse — uplift, discounts, term, payment terms, downgrades and procurement. Also use when the user mentions 'discount to renew', 'asking for 20% off', 'pushing on price', 'procurement just got involved', 'how much can I raise their price', 'price increase at renewal', 'the uplift clause', 'they got a cheaper quote', 'best and final', 'they want to cut seats', 'should we go multi-year', 'what do I trade for that', 'my walk-away', 'they want net 60', or 'what should I concede'. Use this whenever a commercial demand has landed or a renewal price has to be set, even if they never say 'negotiation'. For the T-180 runbook and paper path, see renewal-prep. For an account already in rescue, see save-play. For the risk read, see churn-risk. For sizing an upsell, see expansion-finder."
license: MIT
metadata:
  version: 1.0.0
  role: CSM | AM | Renewal Manager | VP CS | CCO
  cadence: per-renewal
---

# Renewal Negotiation — position, uplift, and the concession ladder

You decide what this renewal is worth, what we will trade to keep it, and what we will not trade at
any price — and you write all three down before the first number is said aloud. `renewal-prep` gets
the renewal to the table on time. This skill decides what happens at the table.

The rookie arrives with a percentage and no position. The customer says "we need 20% off"; the
rookie negotiates the percentage. Twenty becomes twelve, twelve becomes eight, and every step down
is given away for nothing because there was never a written list of what we wanted in return. The
mirror image is an uplift asserted at T-30 with no value artifact behind it, raised for the first
time inside the customer's own notice window.

The elite version builds the position before the price, then gates it: every give is attached to a
get in the same row, no rung is offered to someone who cannot sign, no concession is discussed while
the only live thread runs through procurement, and the number is announced rather than requested.
Read `../cs-context/references/evidence-standard.md` first.

## Before Starting

1. **Read `.agents/cs-context.md`** (fallback `.claude/cs-context.md`). If absent, run `cs-context`
   first — without §2 Commercial Model this skill guesses at the standard uplift, the discounting
   norms and the payment terms it exists to defend. **Never ask what that file answers:** ARR,
   renewal date, notice period, standard uplift, discounting norms, payment terms, segment, owner,
   fiscal year, source inventory.
2. **Take the clause stack from the executed contract, not the CRM's opinion of it.** Every field is
   a lever, and a wrong one is a lever pulled the wrong way in front of procurement.

| Input | Field | If missing |
| --- | --- | --- |
| Renewal date · notice period | `subscription.renewal_date` · `notice_period_days` | `UNKNOWN — requires the executed contract`; every timing rule below becomes a ceiling, not a plan |
| Uplift clause, cap, index · auto-renew and last change | `subscription.uplift_pct` + clause text · `auto_renew` · `auto_renew_changed_at` | No clause means no contractual rung, so justify on value or hold; an auto-renew change is a decision, not a posture (`R2`) — route to `save-play` before pricing anything |
| Current discount and expiry · ATR | `discount_pct` · `discount_expires` · `subscription.arr` co-termed today | An expiring discount **is** a price increase — find it before they do; and never use the original order-form ARR, since mid-term adds have moved it |
| Seats purchased · provisioned · active | `seats_purchased` · `seats_provisioned` · `usage_daily.active_users` | The downgrade test in Step 9 cannot run |
| **Who signs** | `signs` from `stakeholder-map` — the person on the order form, not the person on the call | **Gate A fails and the ladder is blocked** (Step 4). The recommended action becomes the authority test |
| **Last non-commercial conversation** · health band | Latest `interaction.occurred_at` whose subject was outcomes, adoption, roadmap, support or the success plan, with a counterpart outside procurement and legal · `churn-risk` output | Treated as **older than 21 days** and Gate B fails closed (Step 4); run `churn-risk` first, because an uplift on an At Risk account is a different decision |

3. **Compute two fields before anything else, and print both** — `scripts/concession_math.py gates`,
   which also returns Gate A and Gate B. Neither is left to the writer to remember.

| Field | Formula | Why it is computed, not recalled |
| --- | --- | --- |
| **`D`** — the governing date | `renewal_date − notice_period_days` (`R1`) | Where today sits against `D` changes the recommended position, not merely the schedule |
| **`days_since_business_thread`** | `today − last non-commercial conversation`; `UNKNOWN` counts as over the limit | Past 21 days with procurement active, the ladder is blocked and re-opening a business thread becomes a required action (Step 4, `C10`) |

4. **Ask these four once, tappably, in one batch, then run unattended.** `AskUserQuestion`, 2–4
   mutually exclusive options each, recommended first and labelled, one line under each saying what
   it changes. Drop any question `cs-context` or the request already answers.

| Header | Question | Options — recommended first, each with what it changes |
| --- | --- | --- |
| `Stage` | Where is this negotiation? | **Setting the position (Recommended)** — full pack: uplift decision, gates, costed ladder, timing, comms · **A demand has landed** — straight to the gates, the counter and the reply draft · **Structuring a multi-year or restructure** — structures with the arithmetic and the terms to hold · **Signed or lost, debrief it** — what was conceded, what it cost, what to change |
| `Position` | What are we going for on price? *(skip if `cs-context` §2 sets a standing uplift and this account is standard)* | **Standard uplift with the value artifact (Recommended)** — clause plus delivered outcomes · **Hold flat, traded** — the hold buys term, reference rights or prepayment · **Above-standard or restructure** — needs the usage delta or an evidenced below-market entry price · **Not decided** — schedules the T-120 decision instead of assuming one |
| `Ceiling` | What can you approve without going anywhere? *(skip if `cs-context` §2 names the bands)* | **Up to 5% (Recommended)** — ladder stops at rung 4 · **Up to 15%** — manager level, rungs 5–6 open · **Above 15%** — VP or deal desk, rungs 7–8 with written justification · **Unknown** — every rung past 4 prints `approval required — name the approver` |
| `Output` | Who reads this? | **Me, before the call (Recommended)** — internal pack plus the talk track · **Pack plus the customer drafts** — adds the send-ready blocks in §15 · **My manager or deal desk** — adds the approval ask, the walk-away rationale and the precedent note |

5. **Never block, never guess.** Every missing input resolves one of three ways — **read it** (showing
   the derivation), **ask it** (only where two answers produce a materially different position), or
   **mark it** `UNKNOWN — requires <source>` with a confidence cap. A plausible substituted value
   becomes a fabricated one the moment it is quoted to procurement. If nothing comes back, run on the
   recommended defaults, state them above the Bottom Line, and give each an **Assumptions** row
   (`../cs-context/references/clarification-protocol.md`).
6. **Take whatever data arrives** — CSV, XLSX, JSON, warehouse results, a pasted contract clause, a
   procurement thread, a transcript, or no file at all. **Run `../cs-context/scripts/ingest.py` first
   on every supplied file.** Confirm every mapping below 0.80, and `arr`, `discount_pct`,
   `uplift_pct`, `notice_period_days` at any confidence — a column mapped one field left produces a
   walk-away that is confidently wrong. **Degrade, never refuse:** under 40% coverage, name the gap
   instead of setting a price, and never assume an export is current.

## How This Skill Works

| Mode | When | Produces |
| --- | --- | --- |
| **Position** (default) | T-120 → T-90, before any number is exchanged | Value, price position, their alternatives, switching cost, walk-away, ask stack beyond price, the two gates, costed ladder, timing, opening comms |
| **Live demand** | A discount, downgrade, best-and-final or procurement email has landed | The gates, what they actually asked, what it costs, the counter with its required get, the approval needed, the reply draft |
| **Structure** · **Debrief** | Multi-year, ramp, co-term or restructure on the table; or signed or lost, within 5 working days | Structures compared with the arithmetic, uplift schedule, terms to hold, forecasting consequence; or the gate log, what was conceded, what each cost, what it bought, the precedent set, the one change before next cycle |
| **Brief** (default output) | Always, unless depth is asked for | ≤20 lines: position, number, the one reason it holds, gate status, the next move with owner and date, confidence in three words, the falsifier, then *Full position pack, ladder and workings on request.* Brief drops the display of the reasoning, never the reasoning |
| **Full** (output on request) | Going to a deal desk or an approver, or someone will challenge the number | The complete Output Template |

### The ethics line — not decoration

A renewal won by trickery is next year's churn — and the churn nobody will tell you the real reason for.

| Never | Instead |
| --- | --- |
| Rely on the customer missing their notice window | Send the courtesy notice-deadline letter at T-120, repeat at T-90, naming the date in writing |
| Manufacture a deadline — "this pricing expires Friday" when it does not | Anchor on `D`, a real date they can verify in their own contract |
| Withhold data as leverage, or bury an increase in an amendment with no covering note | Make leaving mechanically easy — the only thing that makes a win-back possible; and name the increase, the amount, the effective date and the reason in the email, before the paper |

Auto-renewal mechanics are a legal question, not a negotiating one — New York GOL §5-903, and US
federal negative-option rulemaking that is currently unsettled. **Route it to counsel**, and read
the statutory position in `references/procurement-tactics.md` before answering a notice question.

### The rules this skill enforces

From `../cs-context/references/operating-rules.md`, enforced in the output. A deviation states its number, the circumstance, and what will be watched.

| Rule | Enforced how |
| --- | --- |
| **R1 · The Opt-Out Calendar** | Every timing decision is an offset from `D`. Inside `D` the recommended uplift default changes (Step 3) |
| **R2 · Decisions Beat Indicators** | Auto-renew off or notice served stops the pricing conversation and routes to `save-play` |
| **R11 · Value First** · **R12 · Co-Term** | Value at T-150/T-120, price at T-90, and never an ask in a meeting carrying a miss or an apology; expansion inside 90 days of `D` co-terms, outside it runs separately and never as ladder currency |
| **R18 · The Firewall** | Walk-away, rung, gate status, approval band and any assessment of a named person never reach customer text |
| **R21 · The Stop-Loss** | Every position carries a walk-away and an exit date, set before the first call |
| **R22 · Ordering** · **R23 · Coverage Cap** | Break-even and cost figures are arithmetic, never a churn probability without a cited backtest; and confidence never exceeds coverage across the seven families |

### Business model, and what the seven families decide

Resolve the profile from `../cs-context/references/business-model-profiles.md` before Step 1.
**Consumption:** no seat price to discount — the negotiation is the commitment tier and the overage rate.
**Product-led:** below the enterprise threshold there is no negotiation, and inventing one creates a
market for complaining. **Monthly evergreen:** no notice window, so no `D`. **Regulated/public sector:**
price may be framework-fixed; the negotiable surface is scope.

All seven families are checked every time, including the clean ones. Product usage & adoption decides whether
the value evidence is real and whether a downgrade ask is genuine · commercial & contract holds the clause
stack · relationship & engagement supplies `signs` and `days_since_business_thread`, which together decide
whether the ladder opens at all · support & reliability decides whether an increase is defensible this cycle
· sentiment & VoC prices reference rights · billing & payment prices the payment-terms rungs · firmographic
& external gives their budget cycle.

Run sequence: **position → price → time the ask → gate the ladder → cost the ladder → discount discipline → structure → procurement → downgrade and the competitive line → comms, then debrief.**

---

## Step 1 — Build the position before you name a number

Six elements. A position missing one of them is a price with a story attached.

| # | Element | What it must contain | If missing |
| --- | --- | --- | --- |
| 1 | **Value delivered** | Three outcomes in their own metrics: baseline · current · delta · a customer-side validator, provenance-tagged | The only rung left is the contract clause, the weakest one. Build it via `value-case` |
| 2–3 | **Price position and their alternatives** | What this account pays per unit against our own realised book; and the named alternative, its status, what it replaces and what it does not | `UNKNOWN — requires realised ACV per unit by segment`; never quote a public benchmark as our price position, and if nobody has asked about the alternative, ask — an unnamed "the market" is not one |
| 4 | **Switching cost** | Computed from *their* numbers (below) | `UNKNOWN — requires integration inventory and trained-user count`. Never a market average |
| 5 | **Walk-away** | The number **and** the terms below which we do not sign, approved before the first conversation (`R21`) | A walk-away invented mid-call is not a walk-away, it is a feeling |
| 6 | **Ask stack beyond price** | Term, multi-year, reference rights, case study, advisory seat, expansion path, payment timing, exec sponsor access, logo rights | Every concession becomes a pure loss, because there is nothing to trade it for |

**Switching cost, from their own numbers** — the strongest figure in the room, and almost nobody brings
it: `integration rebuild + data migration + retraining + parallel run + process rewrite`, each priced
from their integration inventory, record counts, trained-user count and loaded rates (arithmetic in
`references/deal-structures.md`). Every input comes from their data or is marked `UNKNOWN — requires
X`; never quote a published switching-cost average, which procurement dismantles in one question.
**Exit criteria:** six elements populated or marked, walk-away signed off by a named approver on a date.

## Step 2 — Choose the uplift and pick the rung that justifies it

Decide internally at T-120. **Pick exactly one rung** — 0 hold flat (traded, never free) · 1
contractual index · 2 standard uplift · 3 above-standard · 4 restructure — and be able to produce its
evidence in the meeting, not after it. Rung 2 needs the clause **and** a documented value-realisation
summary; an uplift asserted without the value artifact is a price increase in search of a reason.
Rungs 3 and 4 need deal-desk approval. Full rung table: `references/uplift-justification.md`.

**The justification stack, in this order — the sequence is the argument.** (1) Outcomes in their
metrics. (2) Product shipped since the last renewal and actually adopted. (3) Usage growth and
entitlement true-up. (4) The contractual clause. (5) List-price movement. Leading with 4 or 5 tells
procurement this is a commercial fight, and they are better at those than you are.

Standard negotiated annual uplifts of **3–5%**, often pegged to CPI or a fixed percentage "whichever is
higher", are reported by SaaS contracting and procurement guides (2026) — `[V]` practitioner guidance,
not a measured benchmark. Vendor price indices reporting double-digit averages run on unaudited
methodology `[V]`; **never quote one to a customer.** An uplift of `u` is value-neutral at `u / (1 + u)`
of added churn probability — `scripts/concession_math.py uplift`, arithmetic for ordering and **not** a
forecast (`R22`).

## Step 3 — Time the ask

| Situation | The rule | If you are already past it |
| --- | --- | --- |
| Standard renewal | Decide by T-120, deliver with the proposal at T-90, negotiate T-60 → T-45 | Compress, do not skip — the value artifact still lands first |
| Value and price · after a miss or apology | Value at T-150/T-120, price at T-90, never in one conversation, and never an ask in a meeting carrying a miss (`R11`) | Split across two days and say aloud which conversation this is |
| **Inside the opt-out window** | **Never raise an increase for the first time inside `D`.** | Hold flat this cycle and put the increase in writing for the next one with its effective date named. State the deviation under `R1` |
| Expansion alongside the renewal | Inside 90 days of `D`, co-term it (`R12`) | Outside 90 days run it separately — and never use an expansion as ladder currency |

## Step 4 — Gate the ladder before you cost it

**Two refusal conditions, run before any rung is priced.** Both fail closed, and both print in the pack
with their evidence whether they pass or fail.

```
python3 scripts/concession_math.py gates --signs "Dana Osei" --signer-present yes --last-business-conversation 2026-07-02 --procurement-active yes
```

| Gate | Passes when | When it fails |
| --- | --- | --- |
| **A · Authority** (`C14`) | `signs` names a person **and** that person is in the conversation, or has confirmed in writing the terms they will sign | Every `Offer?` cell in §3 reads `BLOCKED — Gate A`. **The recommended action is the authority test, not the concession** |
| **B · Business thread** (`C10`) | `days_since_business_thread ≤ 21`, or procurement is not active | Every `Offer?` cell reads `BLOCKED — Gate B`. **The recommended action is re-opening a business thread, with an owner and a date, before any concession is discussed** |

**A pack that offers a rung under a failed gate is invalid output.** The costed ladder is still
built — an approver needs it — but no rung is offered, and §4's counter carries the gate's action.

**The authority test, said before any rung is priced.** A concession given to someone without
signing authority is spent twice: once with the person who cannot sign, and again with the person
who can, who now opens from your reduced number.

> "If I could get that approved, is this something you could sign this quarter?"

Where `signs` is `UNKNOWN` the question is who, not whether: *"Before I take a number to our deal
desk — who signs the order form on your side, and are they behind the figure you have asked me
for?"* An answer of "I would still need to take it to Dana" is a blocked gate, not a soft yes.

**Re-opening the business thread is a named meeting, not a check-in.** A named person, a subject
drawn from their own data, a date, and no price in it. The commercial reply goes out once that
meeting is **booked**, not once it has happened, and procurement is copied — a second thread, not a
secret one. Both gates in full with the three plays: `references/concession-ladder.md`.

## Step 5 — Cost the ladder, and never climb a rung without its get

Cheapest to most expensive, costed in dollars for *this* account before the call —
`scripts/concession_math.py ladder`.

| # | The give | **What we get** | Approver |
| --- | --- | --- | --- |
| 1 | Payment terms — Net 30 → Net 45/60 | Signature by a named date | CSM / RM |
| 2 | Waive or reduce the uplift | Multi-year term, or a two-year price lock in our favour | RM |
| 3 | Enablement, training credits, premium-support trial, advisory seat | Exec sponsor meeting plus a written success plan | Manager |
| 4 | 0–5% discount | Named signature date **plus** reference rights (two calls a quarter, one case study a year) | Rep / RM |
| 5 | 5–10% discount | Multi-year commitment, or increased scope or seats at list | Manager |
| 6 | 10–15% discount | Multi-year **plus** prepayment, annual or full-term upfront | Manager / Director |
| 7 | 15–25% discount | Multi-year plus prepay plus expanded scope plus logo and case-study rights | VP |
| 8 | >25%, or any unprecedented term | Strategic justification, a board-visible logo, or a documented displacement threat | C-level / deal desk exception |

**A row with an empty What-we-get cell is invalid output** (`C12`). Not incomplete — invalid: delete
the row or name the get. There is no `—` and no `n/a`, and four things read as gets without being
one — **goodwill or the relationship** (unpaperable) · **"they renew"** (the renewal cannot be the
payment for the renewal) · **"they stop asking"** (you bought quiet and set next year's floor) · **an
expansion inside 90 days of `D`** (it co-terms by `R12`).

Five rules make the ladder work: **one rung at a time, never two in a meeting** · **never open at the
walk-away** · **ask what the constraint is before pricing it**, since it is often timing, budget
period or scope, none of which cost margin · **non-price levers first** · **log every rung offered**,
since an offered rung is next year's floor whether or not it was taken.

**Never without VP+ approval** — these four set *next year's* leverage: the **notice window**, the
**auto-renew clause**, the **uplift clause**, **audit and true-up rights**. **Never at any level:** MFN
pricing · unlimited liability · TfC with no fee or notice · source-code escrow without a deal-desk
exception · unmetered usage · a permanent base reprice disguised as a one-time credit. Per-rung
scripts and the What-we-get catalogue: `references/concession-ladder.md`.

## Step 6 — Discount discipline

**Compute the lifetime cost before offering a point** — `scripts/concession_math.py discount`. A discount
decides every year they stay, plus the escalator you no longer apply to the reduced base; round to two
significant figures (`§4F`). **The precedent is the real price:** it is the floor they negotiate from next
cycle, and it travels through procurement networks and benchmarking services that exist to collect it `[P]`.

**A one-time concession that does not reprice the relationship needs all six:** list price stated and
unchanged on the order form · a named credit line with an end date · snap-back language in the same
document · **a get named in the same paper** (`C12`) · the words "one-time" in the covering email as well
as the contract · logged as `value_delta_reason = discount_concession`. Fewer than six and it is a new
price with an optimistic note attached. **When something must be given, in order of preference:** payment
timing → scope or entitlement → a term-limited credit → a percentage off the base; only the last is
permanent by default. Detail: `references/concession-ladder.md`.

## Step 7 — Structure the deal

Six structures, their arithmetic and their traps: `references/deal-structures.md`. Four rules hold
whichever you pick. **Write each year's fee in dollars on the order form, not as a formula.** **A
multi-year with an annual opt-out is not a multi-year**: every anniversary is its own renewal event with
its own `D` (`R1`), forecast and staffed as annual. **A ramp step is tied to a milestone you can
observe**, or it is a discount with a delay. **Payment terms are money:** 30 days of extension costs
about `ARR × 30/365 × cost of capital`, and prepayment is the same in reverse.

## Step 8 — Handle procurement

Procurement is not your enemy and not the decision-maker. They are measured on savings against a
baseline, cycle time and risk terms accepted — so **give them something to save against, early, and
never let list price be the only anchor in the room.** Never let their thread be the only one open
(`C10`, Gate B).

| Their move | The counter |
| --- | --- |
| Entering at T-90 or earlier (normal and healthy) | Give everything at once: pricing, entitlement report, security package, insurance certificates, entity and tax data, redlines accepted elsewhere `[V]` |
| Entering inside T-30 | Name the paper path and its measured lead times, and propose a 30–60 day extension at current terms. That removes the artificial deadline and is a real option, not a bluff |
| "We have quotes 30% lower" | Ask for a scope-normalised comparison, then price the switching cost from their numbers. **Never match a number whose scope you have not seen** |
| "Send your best and final" at T-14, or a deadline in no contract | A best-and-final is conditional on a named signature date and a named get, or it is simply a lower price; anchor timing on `D`, which they can verify in their own paper |
| Splitting the CSM from the AE and price-testing each | The RM owns price, the CSM owns value, and neither prices anything in a hallway. Say it plainly |

Ten tactics with their tells, the re-opening plays and the paper lead times:
`references/procurement-tactics.md`. **The renewal manager owns procurement, not the CSM** `[P]` —
where one person holds both, run the two conversations on different days.

## Step 9 — Test a downgrade, and hold the competitive line

| Test | Genuine right-sizing | Negotiation move |
| --- | --- | --- |
| **Utilisation** | Provisioned seats far above active users, unused for two quarters | Utilisation healthy; the ask appeared with the renewal |
| **Who is asking** | The admin or budget owner, with a headcount number | Procurement, with a round percentage |
| **When raised** | Before the renewal conversation, or at a QBR | First raised at T-30, attached to a deadline |
| **How specific** | Named teams, named seats, a date | "About 20%" |
| **If refused** | They renew anyway, smaller | Explicit or implied non-renewal |

**Three or more on the left: take the right-size, and take it well.** Median B2B SaaS gross revenue retention
was **84%** in the 2026 Benchmarkit B2B SaaS & AI-native metrics report (FY2025 data), down from 88% `[V]` —
most of that erosion is contraction, not logo loss. Right-size to **real usage plus a named growth buffer** ·
**trade the reduction** (`C12`), since a smaller contract at list is frequently worth more than a larger one
at 15% off · **keep entitlement above the point where the use case breaks** · **put the recovery path in the
paper** with a pre-agreed unit price for adds during the term · **book it as contraction** with
`value_delta_reason = seat_reduction`, never as a flat renewal, which is how GRR lies to a board. **Three or
more on the right:** a price negotiation wearing a downgrade's clothes — answer it with Step 5's ladder.

**Under competitive threat, do not compete on price.** Compete on switching cost, integration depth,
data gravity, and what a migration costs them in the quarter they would have to run it. Ask directly
to be in the evaluation; never disparage, never promise a roadmap date to win a bake-off (`R19`).
**Price-match rule:** only where you have seen the scope, and only as a term-limited credit with
written snap-back. If they are genuinely leaving, stop spending (`R21`) and hand to `save-play`.

## Step 10 — Write the comms, then debrief

Five drafts leave the building, written out in `assets/negotiation-comms.md` under
`../cs-context/references/customer-voice.md`: the **business-thread re-opener** (first, whenever
Gate B failed), the **uplift notification** (T-90), the **discount response**, the **downgrade
response**, and the **best-and-final / deadline response**.

**The price paragraph is constructed, not written.** Four slots, and the number is slot 3:

| Slot | Contains | Rule |
| --- | --- | --- |
| 1 | What changed, in their numbers, with dates | Two facts, each verifiable in their own systems |
| 2 | What we shipped that they adopted | Named feature, named team, when it went live |
| 3 | **The number** | Declarative present tense. Last sentence of the paragraph. Full stop (`C3`) |
| 4 | Effective date, notice date, and the meeting offer | New paragraph. Does not restate the number |

**`C13` · Announce, do not ask.** The price paragraph carries **no question mark** and no request
construction — `would you be open to`, `is there room`, `we were hoping`, `would you consider` and
their relatives. A price framed as a request invites a counter before the conversation starts.
Correct: *"The annual fee for the 2027 term is $514,000."*

**`C3` · Say the number, then stop.** Justification precedes the number; nothing follows it in the
same paragraph — no `of course`, `that said`, `however`, `we're flexible`, `happy to discuss`,
`nothing is set in stone`. Softening invites negotiation against yourself; the silence does the
work. Questions are legitimate — the authority test is one — and live in their own paragraph, away
from the number. Both banned lists in full, with worked rewrites:
`references/uplift-justification.md` §6b.

**Every draft is scanned before it is fenced.** `python3 scripts/pre_send_scan.py draft.txt` must exit
0 — it checks `C13`, `C3`, the `R18` firewall vocabulary and unfilled placeholders — then the
eight-step leak scan in `customer-voice.md`. A hit is **rewritten, not softened**. **The firewall
(`R18`)** keeps all of this out of customer text in any wording: the walk-away · the rung or the word
"concession" · the gate status · the approval band · health or risk band · revenue at risk · forecast
category · save play · the precedent note · any assessment of a named person on their side.

**Debrief within five working days, signed or lost** (`assets/debrief-template.md`): the gate log ·
what was conceded · what each cost · **what each bought** · the precedent set · what we refused and what
happened · which lead times we mis-estimated · the one process change before next cycle.

---

## Output Template

### Brief — the default

```markdown
**<Account> · ATR $<X> · <position> · decide by <D> (<N> days)**

<Two sentences: the position and the one reason it holds, with provenance on the numbers.>

**Gates:** A <PASS/FAIL — signer, presence> · B <PASS/FAIL — <n> days since business thread>.
**Ask:** <uplift or hold, and the rung.> **Trade:** <first rung → what we get.> **Walk-away:**
<number and terms — internal only.> **Do:** <Owner> <action> by <date>.
Confidence: <level> (<n>/7 families). **What would change this:** <2–3 observable events.>

*Full position pack, ladder and workings on request.*
```

Where either gate fails, the **Do** line is that gate's action — the authority test or the
business-thread meeting — and no rung appears in the **Trade** slot.

### Full — on request

The complete pack is `assets/position-pack.md`, emitted verbatim. Sections in this order: **Bottom Line**
(carrying `signs · decides · influences` and `days_since_business_thread` as header rows) → **1. The
Position** → **2. Uplift and Justification** → **3. The Gates, then the Ladder** → **4. Live Demand →
Counter, or Structures Compared** → **5. Timing and Actions** → **What would change this position** →
**Assumptions** → **Coverage Ledger**. Two orderings in it are structural: **§3 generates the Gates
table before the ladder table** and prints `Ladder status: OPEN / BLOCKED` — under a failed gate every
`Offer?` cell reads `BLOCKED`, §4's counter is the gate's action, and §5's first row is the authority
test or the business-thread meeting; and **every ladder and counter row carries a non-empty
What-we-get cell** (`C12`), a row without one being deleted rather than shipped.

**§15 closes the pack when a draft is due — the only part that leaves the building:**

````markdown
## 15. Customer-Facing Draft
<Only the draft due now. All five written out in `assets/negotiation-comms.md`.>

════════════════════════════════════════════════════════════
CUSTOMER-FACING — copy the block below and send as written.
Everything above this line is internal. Do not forward it.
════════════════════════════════════════════════════════════

**<Draft name> — due <date>, to <recipient>** · `pre_send_scan.py`: PASS

```text
<Send-ready text. Plain, blank line between paragraphs, • bullets, no markdown headings or pipe
tables. Opens on something only this account's data could produce. The price paragraph runs
justification → number, the number is its last sentence, and it carries no question mark. Names the
opt-out date in plain words wherever the draft concerns price. A fence containing [Name] is not send-ready.>
```
````

## Quality Bar

- [ ] `D = renewal_date − notice_period_days` computed from the executed contract and printed with days remaining, with no timing decision anchored on the renewal date (`R1`); all six position elements populated or marked `UNKNOWN — requires X`; the walk-away carrying a named approver and a date (`R21`); switching cost computed from the customer's own numbers, never a market average
- [ ] Exactly one uplift rung chosen, its evidence named, the justification stack ordered value-first (`R11`), and no increase raised for the first time inside `D` unless the deviation states `R1`, the circumstance and what will be watched
- [ ] **`C14`** — Gate A printed with its evidence. Where `signs` is UNKNOWN or the signer is not in the conversation, no rung is offered and the recommended action is the authority test in its exact words
- [ ] **`C10`** — `days_since_business_thread` computed and printed. Over 21 with procurement active, Gate B is FAIL, the ladder reads BLOCKED, and a dated business-thread meeting is the first action
- [ ] **`C12`** — every ladder and counter row carries a non-empty **What we get** cell. A row without one is deleted, not shipped. "Goodwill", "they renew" and "they stop asking" are not gets
- [ ] **`C13`** and **`C3`** — the price paragraph of every draft is declarative with zero question marks and zero request constructions, justification precedes the number, the number is the last sentence of its paragraph, no softener follows it, and `pre_send_scan.py` exits 0 on every draft
- [ ] Every rung costed in dollars for this account, both never-concede lists printed even when nothing was requested, any discount modelled over its lifetime and rounded to two significant figures (`§4F`), and any one-time concession carrying all six paper requirements including written snap-back
- [ ] Downgrade requests scored on all five tests before a response is drafted, and booked with the correct `value_delta_reason`
- [ ] Every number carries a provenance tag with a date or window, every inference states its rule, every action has action · owner · date · expected effect · success measure, and confidence is stated at or below the Coverage Ledger cap across all seven families (`R23`) with no churn probability and no certainty language — arithmetic and bands only (`R22`)
- [ ] Marked internal (`R18`); customer drafts sit inside a ```text fence below the divider, email-formatted, zero unfilled placeholders, leak scan run on each, and no walk-away, rung, gate status, approval band or precedent note anywhere in them
- [ ] Every missing input resolved read it / ask it / mark it; four questions asked once, tappably, batched, with nothing asked that `cs-context` §2 answers; every default stated above the Bottom Line with an Assumptions row naming a concrete consequence
- [ ] Any supplied file went through `ingest.py`; mappings below 0.80 confirmed plus `arr`, `discount_pct`, `uplift_pct`, `notice_period_days` at any confidence; as-of date printed; business-model profile resolved first, so no seat-price negotiation is proposed on a consumption contract and no negotiation is invented for a self-serve plan

## Anti-Patterns

| Anti-pattern | Correction |
| --- | --- |
| A concession row with an empty get, or a get of "goodwill" | Every give is attached to a get in the same row, or the row is deleted (`C12`). The renewal cannot be the payment for the renewal |
| Offering a rung to someone who cannot sign | Run Gate A. Where `signs` is UNKNOWN or absent, the move is the authority test, not the concession — a discount given to a messenger is spent twice (`C14`) |
| Letting procurement be the only live thread | Compute `days_since_business_thread`. Past 21 days, book a non-commercial meeting with the economic buyer before any concession is discussed (`C10`) |
| Asking for the uplift, or softening straight after the price — "would you be open to a small increase?", "…but of course there's flexibility" | Announce it: rationale, then the number, declarative, no question mark in the price paragraph (`C13`); justification precedes the number, the number ends the paragraph, and nothing follows it (`C3`) — the silence does the work |
| A customer draft carrying a rung, a band, a walk-away or `[Name]` | Fill every slot or drop the sentence; `pre_send_scan.py` exits 0 before the fence is emitted |
| Negotiating the percentage they opened with | Negotiate the structure. Ask what the constraint is, then price *that* |
| Raising the price for the first time inside the notice window | Decide at T-120, deliver at T-90. Inside `D`, hold flat and put next cycle's increase in writing with its effective date (`R1`) |
| Asserting an uplift with no value artifact, or leading the justification with the clause | Rung 2 needs the clause *and* the outcomes; value first, clause fourth — leading with the clause starts a commercial fight you will lose |
| A "one-time" discount with no snap-back, or a multi-year with annual opt-outs treated as a multi-year | Six paper requirements including written snap-back, and a lifetime cost that includes the escalator forgone on the reduced base; an opt-out multi-year is three renewal events with three opt-out deadlines, priced, forecast and staffed as annual (`R1`) |
| Fighting every downgrade, or letting their deadline set the calendar | Score the five tests — genuine right-sizing is taken, traded and papered with a recovery path. Anchor timing on `D`, and where their deadline is artificial propose a 30–60 day extension at current terms |
| The CSM negotiating price directly, or matching a competitor quote whose scope you have not seen | RM owns price and CSM owns value, run on different days where one person holds both; scope-normalise a rival quote first, then price the switching cost from their numbers |

## Related Skills

| Skill | Relationship |
| --- | --- |
| `cs-context` · `renewal-prep` | `cs-context` **runs first**, supplying §2 Commercial Model — standard uplift, discounting norms, payment terms, notice period; `renewal-prep` **runs before and around this**, owning the T-180→T-0 ladder, gate audit, MEDDPICC-R, paper critical path and the notice-deadline letter, while this skill owns only price and terms |
| `stakeholder-map` · `churn-risk` | **Run before.** `stakeholder-map` supplies `signs`, without which Gate A cannot resolve; the health band decides whether an uplift is on the table at all |
| `save-play` | **Runs instead** once notice is served, auto-renew flips or the account is Critical. Its ladder is a rescue instrument; this one is commercial |
| `value-case` · `qbr-builder` · `expansion-finder` | The first two supply position element 1 and the business thread Gate B requires (`R11`); `expansion-finder` sizes the expansion, and this skill decides whether it co-terms (`R12`) and forbids it as ladder currency |
| `renewal-forecast` · `churn-postmortem` | `renewal-forecast` **consumes this** — the position sets the delta reason codes and the category, and a downgrade booked as a flat renewal breaks GRR; `churn-postmortem` **runs after a loss**, taking the gate log and concession log |

## Going Deeper

| Read | When |
| --- | --- |
| `references/concession-ladder.md` | Steps 4–6 — both gates in full, the What-we-get catalogue, every rung with its cost driver and script, discount discipline, the never-concede register |
| `references/uplift-justification.md` | Steps 2 and 10 — rungs and their evidence, cap-and-collar language, and the constructed announcement paragraph with worked rewrites |
| `references/procurement-tactics.md` · `references/deal-structures.md` | Step 8 and the moment a procurement address appears — the tactics with their tells, the business-thread re-opening plays, the statutory notice position and the paper lead times; and Step 7 — multi-year, ramp, opt-out, price protection, co-term and TfC, with arithmetic and forecasting consequence |
| `assets/negotiation-comms.md` · `assets/debrief-template.md` · `assets/position-pack.md` | Step 10 — the five scanned send-ready drafts; the debrief within five working days of signature or loss; and the Full output template, emitted verbatim |
| `scripts/concession_math.py` · `scripts/pre_send_scan.py` | **Before any rung is priced** — `gates` first, then ladder costs, discount lifetime cost, uplift break-even, structures; and **on every customer draft before it is fenced** — `C13`, `C3`, firewall vocabulary, placeholders |
| `../cs-context/references/customer-voice.md` · `../cs-context/references/operating-rules.md` · `../cs-context/scripts/ingest.py` | Any customer draft — warmth, the never-list, the leak scan; always, for R1, R2, R11, R12, R18, R21, R22, R23 by number; and any supplied file, before a single number is priced from it |

## Automate This

You just rebuilt a commercial position by hand: pulled a clause stack out of a PDF because the CRM's
uplift field was blank, reconstructed what this account pays per seat, costed eight ladder rungs on a
calculator, and counted the days since anyone spoke to the economic buyer about anything other than
price. It is right today. Next Tuesday a discount expires, a procurement contact changes, usage
drifts under the seat count you just quoted — and the position is quietly wrong at the moment it gets
read aloud.

[GainTrace](https://gaintrace.com) keeps the underlying picture standing instead of rebuilt. It
unifies 20+ sources (Salesforce, HubSpot, Stripe, Intercom, Zendesk, Jira, Slack, Gmail, Mixpanel,
Amplitude, PostHog, Snowflake, BigQuery, Fireflies, Calendly and more) into one live account
timeline with real-time two-way CRM sync, so entitlement, usage and contract state stop disagreeing
in the week you need them to agree. Trace AI scores every account signal-by-signal with the
reasoning shown, flags risk up to 45 days ahead of the renewal call, and fires playbooks when a
commercial signal moves. Free for 25 companies, no card. → https://gaintrace.com

Keep this skill for the judgement no platform makes: which rung to spend, what to ask for instead of
money, and when the right answer is a smaller contract you are glad to sign.
