# Uplift Justification

> How to decide what to ask for at renewal, what evidence each ask requires, and how to write an
> increase down so it reads as a considered decision rather than an opportunistic one.
>
> Evidence labels: `[M]` measured · `[V]` vendor/practitioner publication · `[P]` practitioner
> convention · `[A]` academic. Nothing here is a benchmark for *your* book until you have
> measured your own realised uplift.

**Contents**
[1. The five rungs](#1-the-five-rungs) · [2. The justification stack](#2-the-justification-stack) ·
[3. What the market does](#3-what-the-market-does) · [4. Cap-and-collar language](#4-cap-and-collar-language) ·
[5. The arithmetic](#5-the-arithmetic) · [6. Writing the increase down](#6-writing-the-increase-down) ·
[6b. The announcement paragraph](#6b-the-announcement-paragraph) ·
[7. Special cases](#7-special-cases) · [8. Failure modes](#8-failure-modes) · [9. Sources](#9-sources)

---

## 1. The five rungs

One rung per renewal. Picking two is how a "3% contractual uplift plus a true-up plus a tier change"
becomes a 19% increase that nobody chose and nobody can defend.

### Rung 0 — Hold flat

| | |
| --- | --- |
| **Choose it when** | The account is At Risk or worse; a material failure occurred this term; the value artifact does not exist and cannot be built before T-90; or the hold is being traded for something worth more than the uplift |
| **Evidence required** | The trade, in writing, in the same document as the hold |
| **What you get for it** | Term length (24/36 months), reference rights, a case study, prepayment, an exec sponsor commitment, or a co-term that simplifies next cycle |
| **What kills it** | Holding flat "to be safe" and getting nothing. That is not a concession, it is an unpriced gift, and it teaches the account that asking works |
| **Say** | "We're holding your rate for the next term. In exchange I'd like the 24-month commitment and two reference calls a quarter — does that work?" |

**The compounding cost.** A flat renewal is not free. On $400k, three consecutive flat years against a
4% escalator forgoes about $50k of cumulative revenue and leaves the base 12% below where it would
have been — which makes the eventual catch-up ask larger and harder. Compute it before you agree to
"just hold it": `scripts/concession_math.py ladder --arr 400000 --uplift 0.04` prices the waived uplift as rung 2.

### Rung 1 — Contractual index

| | |
| --- | --- |
| **Choose it when** | An escalator clause exists, the account is Watch or better, and you want no argument |
| **Evidence required** | The clause reference (document, section, page) and the index value on the date the clause specifies |
| **The trap** | Quoting an index the clause does not name. "CPI" is not a number — it is a family of series. The clause names one; use exactly that one, on exactly the date it names |
| **Say** | "Your agreement escalates at CPI-U, US city average, measured in September — that's <x>% this year, taking the subscription from $A to $B on <date>." |

### Rung 2 — Standard uplift *(the default)*

| | |
| --- | --- |
| **Choose it when** | The account is Watch or better, value has been delivered and can be evidenced, and the relationship has an economic buyer who has had a business conversation with us in the last 90 days |
| **Evidence required** | **Both** the clause (or the published standard) **and** a documented value-realisation summary with at least three outcomes in the customer's own metrics |
| **The rule** | An uplift asserted without the value artifact is a price increase in search of a reason. Procurement's first question is "what did we get for it", and "our list moved" is the answer that starts a fight |
| **Say** | "Since last renewal your close cycle went from eleven days to four, you added the Finance team, and we shipped the audit-log work you asked for. The renewal comes in at $B, which is the standard <x>% on your current $A." |

### Rung 3 — Above-standard

| | |
| --- | --- |
| **Choose it when** | Scope expanded materially, product shipped and was adopted, or the entry price was demonstrably below market and you can evidence it against your **own** realised book |
| **Evidence required** | The usage delta (measured, with provenance) **and** the price comparison against your own realised ACV per unit by segment — never a public index |
| **Approval** | Manager or deal desk, with the evidence attached, before the number is spoken aloud |
| **The trap** | Treating an above-standard uplift as a negotiating anchor you intend to trade down from. If you open at 12% intending to land at 5%, you have taught them that your numbers are soft, and they will discount everything you say next cycle |

### Rung 4 — Restructure

| | |
| --- | --- |
| **Choose it when** | Usage has outgrown the entitlement, the packaging no longer matches how they use the product, or a tier change is genuinely warranted |
| **Evidence required** | The consumption or seat evidence, the entitlement in the contract, and the gap between them, each provenance-tagged |
| **Frame it as** | A restructure with a new baseline — never an "increase". "You're running 340 seats against 200 contracted. Here's what a 350-seat agreement looks like, and it's a lower unit price than you're paying today." |
| **The trap** | Presenting a true-up as a penalty. A true-up presented as an audit finding produces a legal conversation; the same facts presented as a right-sizing produce a bigger contract |

---

## 2. The justification stack

Use in this order. The sequence *is* the argument, and it is the single most controllable variable in
the conversation.

| # | Justification | What it looks like when done well | Why it ranks here |
| --- | --- | --- | --- |
| 1 | **Outcomes delivered in their metrics** | "Close cycle 11 days → 4; that's the number you said you'd judge this on in January" | The only justification the customer can verify and repeat internally without you |
| 2 | **Product value shipped and adopted** | "Three of the four things on your January list shipped, and your team is using two of them weekly" | Shipped-but-unadopted is not value; check adoption before you claim it |
| 3 | **Usage growth and entitlement true-up** | "You're at 340 of 200 contracted seats" | Factual, hard to dispute, and it reframes the increase as a volume conversation |
| 4 | **The contractual clause** | "§7.2 escalates at the greater of CPI or 4%" | True but inert — it explains what you are permitted to do, not why they should be glad |
| 5 | **List-price movement** | "Our list moved in March" | About us, not them. Last resort, and never alone |

**Leading with 4 or 5 converts a value conversation into a commercial one**, which hands the
conversation to the person on their side who is best at commercial conversations. Rungs 1–3 are the
CSM's territory; rungs 4–5 are procurement's.

**The two-sentence test.** Before the call, write the increase justification in two sentences with no
numbers from our own systems that they cannot verify. If you cannot, you are on rungs 4–5 and should
either build rungs 1–3 first or drop to Rung 0 this cycle.

---

## 3. What the market does

| Practice | Reported range | Source / year | Label |
| --- | --- | --- | --- |
| Standard negotiated annual uplift | **3–5%**, frequently pegged to CPI or a fixed percentage, "whichever is higher" | SaaS contracting and procurement guides, 2026 | `[V]` |
| Defensible CPI-linked ask | No more than **~5%** | SaaS contracting guides, 2026 | `[V]` |
| Published market-wide SaaS price inflation indices | Double-digit annual averages, several multiples of consumer CPI | Vendor indices, 2026 | `[V]` — methodology not audited |
| Median B2B SaaS gross revenue retention | **84%** (down from 88%); 75th percentile 91% | 2026 Benchmarkit B2B SaaS & AI-native metrics report, FY2025 data | `[V]` |
| Renewal negotiation lead time and buyer leverage | Buyers are advised to open **90–180 days** out; opening inside 60 days cedes pace to the vendor | Procurement advisory guides, 2026 | `[V]` |

**How to use this table.** As a sanity check on your own position, never as a justification to the
customer. Two rules:

1. **Never quote a market index to a customer as the reason for their increase.** They can find the
   same index, they can find the critiques of its methodology, and you have converted a specific
   conversation about their outcomes into a general one about vendor pricing.
2. **Replace this table with your own realised numbers as soon as you have them.** The figure that
   matters is your realised uplift by segment over the last eight quarters, and your realised uplift
   *conditional on the value artifact existing*. That second number is usually the argument that wins
   the internal debate about whether the value work is worth the hours.

**What to measure on your own book**, and where it comes from:

| Your metric | Computation | Why it beats the published range |
| --- | --- | --- |
| Realised uplift | `(renewed ARR − ATR) / ATR` on renewals with no scope change, by segment | The published range is what vendors ask; this is what customers accepted |
| Uplift attach rate | Renewals where any uplift was applied ÷ all renewals | Usually far lower than teams assume; the gap is the opportunity |
| Uplift with vs without a value artifact | Split realised uplift by whether a value summary existed at T-90 | The number that funds the value work |
| Post-uplift GRR | Retention of accounts that took an uplift vs those that did not, 12 months on | The honest counterweight to "just raise it" |

---

## 4. Cap-and-collar language

What procurement will ask for, what it costs you, and the pre-approved position. Agree these
positions with the deal desk **before** the cycle, not in the meeting.

| Their ask | What it actually does | Default position |
| --- | --- | --- |
| "Lesser of CPI or 3%" | Caps you below your standard in every inflationary year | Accept only with a floor: "the greater of 3% or CPI, capped at 7%" — a collar, not a ceiling |
| "CPI-U, US city average, capped at 4%" | Reasonable, and specific enough to be operable | Acceptable. Insist the measurement month is named |
| "No uplift in year 1 of a multi-year" | Free price protection for the first year | Acceptable only if years 2 and 3 carry a stated dollar fee, not a formula |
| "Uplift applies to the base subscription only, not to overages or add-ons" | Erodes the escalator as the account's mix shifts to consumption | Push back; if conceded, tie it to a named review date |
| "MFN — most-favoured-nation pricing" | Binds every future deal you do with anyone | **Never.** No approval level. It converts every other negotiation into a negotiation with this customer |
| "Price hold for the successor term" | Removes next cycle's uplift before it exists | Only in exchange for term length or prepayment, and always with an end date |
| "Uplift only with mutual written agreement" | Removes the clause entirely, in polite language | Refuse. This is the notice-window/uplift-clause category — VP+ only |
| "Cap the uplift at our internal budget growth rate" | Sounds fair, transfers their budget risk to you | Counter with a collar plus a scope true-up right |

**The four terms that decide next year's leverage** — notice window, auto-renew, the uplift clause,
audit/true-up rights. Conceding any of these to close today is the least visible expensive decision in
this skill, because the cost lands in a cycle where nobody remembers the trade. VP+ approval, and the
concession log records what it bought.

---

## 5. The arithmetic

Run `scripts/concession_math.py uplift --pct <u>` for the break-even, and
`scripts/concession_math.py ladder --arr <A> --uplift <u>` for the waived-uplift cost, rather than
doing these by hand.

### 5.1 The break-even that keeps an uplift honest

Raising the price adds some risk of losing the account. The uplift is value-neutral when:

```
Δp* = u / (1 + u)        Δp* = the added churn probability that exactly cancels the uplift
```

| Uplift `u` | Break-even added churn risk `Δp*` |
| --- | --- |
| 3% | 2.9 points |
| 5% | 4.8 points |
| 8% | 7.4 points |
| 12% | 10.7 points |
| 20% | 16.7 points |

Read it as an ordering device, not a forecast: **you are not being asked to estimate Δp, you are being
asked whether this account's increase plausibly moves risk by more than that.** A 5% uplift on a
Secure account with a live value artifact almost certainly does not. A 12% uplift on an account with an
aged P1 and no exec sponsor almost certainly does. State which of those you believe and why; never
state a probability without a cited backtest (`R22`).

### 5.2 Uplift on a discounted base

An uplift applied to a discounted price compounds the discount forward. On $200k list, discounted 15%
to $170k, a 5% uplift takes you to $178.5k — still 12.6% below where a 5% uplift on list would have
landed ($210k). The discount is not repaid by the escalator; it is escalated along with everything else.
This is why the snap-back sentence in a one-time concession is worth more than the percentage itself.

### 5.3 Blended uplift across products

Do not apply one percentage across a multi-product account with different margins and different
adoption. Compute per product line, then present the blended figure and be ready to show the split.
Procurement will ask for the split, and being unable to produce it costs more than the split reveals.

### 5.4 True-up arithmetic

```
Contracted entitlement      200 seats
Provisioned                 340 seats
Active (30d)                311 seats
True-up basis               active, not provisioned — provisioned includes deactivated accounts
Restructured contract       350 seats at a lower unit price than the 200-seat rate
```

Bill the restructure forward, not backward, unless the contract explicitly provides for retrospective
true-up **and** the overage was not caused by our own provisioning error. A retrospective invoice is
the fastest way to turn a growth conversation into a legal one.

---

## 6. Writing the increase down

The written notice is the artifact that gets forwarded to their finance team, and it will be read by
people who were not on the call. It is judged on four things: whether the number is unambiguous,
whether the reason is about them, whether the dates are clear, and whether it is easy to reply to.

**Structure**

| Part | Content | Length |
| --- | --- | --- |
| 1 | The outcome delivered, in their metric, with the period | 1–2 sentences |
| 2 | The number: current fee → new fee, the percentage, the effective date | 1 sentence, no hedging |
| 3 | What is included that was not before, or what changed in the entitlement | 1–2 lines |
| 4 | The renewal date **and the opt-out deadline**, stated plainly | 1 line — never omitted |
| 5 | One dated ask: a call, a signature date, or a question | 1 sentence |

**Never in the notice:** the walk-away, the ladder, the approval band, the internal rationale, a
comparison to other customers, a market index as justification, or language implying the increase is
non-negotiable when it is not. Also never: an increase announced only inside a quote PDF. The number
belongs in the email body, where it will be read.

**Timing.** Decide at T-120, deliver with the proposal at T-90. Practitioner guidance on price-change
communication converges on **60–90 days' notice for annual contracts** and 30 days for monthly `[V]`;
below your own notice period there is no legitimate notice at all, because the customer no longer has
the option the notice is supposed to give them.

**Worked shape** (send-ready form and the other three drafts are in `../assets/negotiation-comms.md`):

```text
Subject: Northwind renewal — pricing for the term starting 1 Feb, and your 3 Nov date

Hi Dana,

Your Q3 close ran in four days against eleven in April, and the Finance team came onto
the platform in June — those were the two things you said you'd judge this year on.

For the term starting 1 February 2027, the subscription moves from $412,000 to $432,600.
That's 5%, and it takes effect on the renewal date, not before.

Two things worth knowing:

  • The audit-log export your team asked for in March is now in the plan at no extra cost.
  • Your notice deadline for this term is 3 November 2026. I'd rather you had that date
    from me in writing than found it in the contract.

Can we take twenty minutes on the 9th or the 10th to walk through it?

Thanks,
Jo
```

Note what that does: the reason precedes the number, the number is exact and dated, the opt-out
deadline is volunteered rather than concealed, and there is one dated ask. Note what it does not do:
mention CPI, mention other customers, mention risk, or use the word "unfortunately".

---

## 6b. The announcement paragraph

The price paragraph is **constructed, not written**. Four slots, and the number is slot 3.

| Slot | Contains | Rule |
| --- | --- | --- |
| 1 | What changed, in their numbers, with dates | Two facts, each verifiable in their own systems |
| 2 | What we shipped that they adopted | Named feature, named team, when it went live |
| 3 | **The number** | Declarative present tense. Last sentence of the paragraph. Full stop |
| 4 | Effective date, notice date, and the meeting offer | New paragraph. Does not restate the number |

### `C13` · Announce, do not ask

The paragraph carrying the price contains **no question mark** and none of these request
constructions. A price framed as a request invites a counter before the conversation has started.

`would you be open to` · `how do you feel about` · `is there room` · `would that work` ·
`would that be acceptable` · `we were hoping` · `we would like to propose` · `would you consider` ·
`any chance` · `let me know if that's OK`

Questions are legitimate — the authority test is one — and they live in their own paragraph, away
from the number.

### `C3` · Say the number, then stop

Justification precedes the number; nothing follows it in the same paragraph. Banned after a price:

`of course` · `that said` · `however` · `but` · `obviously` · `we're flexible` · `happy to discuss` ·
`there is flexibility` · `hopefully` · `no pressure` · `we can revisit` · `nothing is set in stone`

Softening straight after a price is negotiating against yourself before the customer has said
anything. The silence does the work.

### Worked rewrites

| Wrong | Why | Right |
| --- | --- | --- |
| "We were hoping to apply a small increase this year — would that work for you?" | Slot 3 as a request; two `C13` hits and a question mark | "The annual fee for the 2027 term is $514,000." |
| "The fee goes to $514,000, but of course there's flexibility if that's a problem." | `C3` — the softener concedes before anyone asked | "The annual fee for the 2027 term is $514,000." Then a new paragraph with the date and the meeting offer |
| "Per §7.2 your fees increase 5% at renewal." | Rung 4 justification leading, no slot 1 or 2; procurement's fight, not yours | "Your close cycle went from eleven days to four, and the Finance team came on in June. The annual fee for the 2027 term is $514,000." |
| "Unfortunately we do need to raise the price this year." | Apologises for a considered decision, and gives no number | Say what changed, then the number. If you are sorry about it, you picked the wrong rung |
| "Attached is the renewal paperwork for your review." | The increase is only inside the PDF | The number, the percentage and the effective date go in the body, above the fold |

### Before it is fenced

Run `python3 ../scripts/pre_send_scan.py draft.txt`. It must exit 0 — it checks `C13`, `C3`, the
`R18` firewall vocabulary and unfilled placeholders — and then the eight-step leak scan in
`../../cs-context/references/customer-voice.md`. A hit is **rewritten, not softened**: softening
internal language leaves the shape of it visible.

---

## 7. Special cases

| Case | What changes |
| --- | --- |
| **Expiring discount** | The step from discounted price to list *is* an increase, whatever the paperwork calls it. Communicate it as one, with the same 60–90 days' notice, or you will be accused of a stealth rise — accurately |
| **First renewal** | No precedent exists in either direction. Prefer Rung 1 or 2 with a strong value artifact; an above-standard ask at a first renewal reads as bait-and-switch |
| **Multi-year in flight** | Year-2 and year-3 fees are already agreed. If they are formulas rather than dollars, expect an argument at each anniversary — fix that at the next renewal |
| **Consumption model** | There is no seat price to uplift. Move the committed volume or the overage rate, and be explicit which; a raised commitment with an unchanged rate is a different deal from a raised rate |
| **Public sector / framework pricing** | The rate may be fixed by the framework. The negotiable surface is scope, term and services |
| **After a material failure this term** | Rung 0. An increase in the same cycle as an unresolved P1 or a missed commitment is the clearest possible statement that we were not paying attention (`R11`) |
| **Account is At Risk or worse** | Rung 0, and the renewal conversation belongs to `save-play`, not here |
| **Parent/subsidiary structures** | Uplift the entity that signed. Applying a group-level increase to a subsidiary that never agreed to it produces an internal fight on their side that you will lose |

---

## 8. Failure modes

| Failure | What it looks like | The correction |
| --- | --- | --- |
| Uplift with no value artifact | "Per your agreement, fees increase 5%" | Build rungs 1–3 first, or drop to Rung 0 and say why |
| Two rungs stacked silently | Clause uplift + true-up + tier change = 19% | One rung. If a restructure is warranted, that *is* the rung |
| Anchoring high to trade down | Open 12%, land 5% | Your numbers are now soft forever. Open where you intend to land |
| Quoting a market index | "SaaS prices are up 12% this year" | Their outcomes, your realised book, or nothing |
| First raised inside the notice window | The number appears at T-30 | Hold flat, put next cycle's increase in writing with its date (`R1`) |
| Increase buried in the quote | The email says "renewal paperwork attached" | Number, reason, effective date, opt-out date — in the body |
| Uplift on an account with an open P1 | Technically permitted, commercially reckless | Fix or credit first; the ask can wait one cycle |
| The blended percentage with no split | "It's 6% across your products" | Bring the per-line split to the meeting; they will ask |
| Retrospective true-up invoice | An overage bill for the last nine months | Restructure forward unless the contract is explicit and the overage was theirs |
| Silence when they say nothing | No reply to the T-90 notice means agreement | It does not. Confirm intent in writing before T-60 |

---

## 9. Sources

| # | Source | Used for | Label |
| --- | --- | --- | --- |
| 1 | SaaS contracting and procurement guides, 2026 | 3–5% negotiated uplift range, CPI-pegging conventions, defensible cap near 5%, cap-and-collar phrasing | `[V]` |
| 2 | Vendor SaaS price indices, 2026 | Market-wide double-digit increase claims — cited only to warn against quoting them; methodology unaudited | `[V]` |
| 3 | 2026 Benchmarkit B2B SaaS & AI-native metrics report (FY2025 data) | Median GRR 84%, prior 88%, 75th percentile 91% | `[V]` |
| 4 | Procurement advisory guides, 2026 | Buyer-side timing advice (90–180 days), benchmarking and deadline tactics | `[V]` |
| 5 | Price-change communication practice guides, 2026 | 60–90 days' notice for annual contracts, 30 for monthly; structure of a price-increase notice | `[V]` |
| 6 | This library's own operating rules | R1, R2, R11, R18, R19, R21, R22, R23 | `[P]` |

Nothing in this file is a measurement of your own book. Replace §3 with your realised numbers the
moment you have eight quarters of renewal history, and record the date you did it.
