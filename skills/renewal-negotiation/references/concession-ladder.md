# The Concession Ladder

> Every rung, what it costs, what it must buy, who approves it, and the sentence that attaches the
> give to the get. Plus the never-concede register, and how to give something once without repricing
> the relationship forever.
>
> Evidence labels: `[M]` measured · `[V]` vendor/practitioner publication · `[P]` practitioner
> convention. Dollar costs here are formulas; run `scripts/concession_math.py ladder` for this
> account's numbers.

**Contents**
[0. The two gates](#0-the-two-gates) · [1. The one rule](#1-the-one-rule) · [2. The ladder](#2-the-ladder) ·
[2b. The What-we-get catalogue](#2b-the-what-we-get-catalogue) · [3. Costing each rung](#3-costing-each-rung) ·
[4. The scripts](#4-the-scripts) · [5. Never-concede register](#5-never-concede-register) ·
[6. One-time without repricing](#6-one-time-without-repricing) · [7. Reading their constraint](#7-reading-their-constraint) ·
[8. Ladder discipline](#8-ladder-discipline) · [9. The concession log](#9-the-concession-log) ·
[10. Failure modes](#10-failure-modes)

---

## 0. The two gates

Run both before any rung is priced. Both fail closed, both print in the pack with their evidence
whether they pass or fail, and both are computed rather than recalled:

```
python3 ../scripts/concession_math.py gates --signs "Dana Osei" --signer-present yes \
  --last-business-conversation 2026-07-02 --procurement-active yes --today 2026-08-28
```

### Gate A · Authority (`C14`)

| | |
| --- | --- |
| **Passes when** | `signs` names a person **and** that person is in the conversation, or has confirmed in writing the terms they will sign |
| **Fails when** | `signs` is `UNKNOWN`, or the person in the conversation is a messenger for someone who has not seen the terms |
| **On failure** | Every `Offer?` cell in the ladder reads `BLOCKED — Gate A`. The recommended action is the authority test, not the concession |
| **Why** | A concession given to someone without signing authority is spent twice: once with the person who cannot sign, and again with the person who can, who now opens from your reduced number |

**The authority test, said before any rung is priced:**

> "If I could get that approved, is this something you could sign this quarter?"

Where `signs` is `UNKNOWN` the question is *who*, not *whether*:

> "Before I take a number to our deal desk — who signs the order form on your side, and are they
> behind the figure you have asked me for?"

"I would still need to take it to Dana" is a **blocked gate, not a soft yes.** It is also useful
information, delivered cheaply: you now know the negotiation you thought you were in is a rehearsal.

### Gate B · Business thread (`C10`)

| | |
| --- | --- |
| **Passes when** | `days_since_business_thread ≤ 21`, or procurement is not active |
| **Fails when** | Procurement is active and the only live thread with the account is commercial |
| **On failure** | Every `Offer?` cell reads `BLOCKED — Gate B`. The first action is a dated, non-commercial meeting with the economic buyer, before any concession is discussed |
| **Why** | When the only conversation is about price, price is the only variable left. The value case cannot be made in a thread whose subject line is a quote number |

`days_since_business_thread` = today − the latest `interaction.occurred_at` whose subject was
outcomes, adoption, roadmap, support or the success plan, with a counterpart **outside procurement
and legal**. `UNKNOWN` counts as over the limit.

### The three re-opening plays

Pick one. Each is a named meeting with a subject drawn from their own data, and **none of them
mentions price.** The commercial reply goes out once the meeting is **booked** — it does not have to
have happened. Copy procurement in: the rule is a second thread, not a secret one.

| Play | Use it when | The subject line is | The ask |
| --- | --- | --- | --- |
| **The delta** | Usage has moved measurably on one team since the last conversation | That team's numbers, and what they are now doing differently | 30 minutes on what they want it to look like next quarter |
| **The open milestone** | A success-plan item is due, slipped or has just landed | The milestone by name, its date, and what remains | 30 minutes to re-set the plan with them as owner |
| **The shipped ask** | Something they asked for has shipped since the last renewal | The feature, the date it went live, and who on their side has used it | 20 minutes to walk their admin through it |

**What disqualifies a re-opener:** a price in it, a paperwork question in it, a subject line that
could have gone to forty customers, or a meeting request with no named person and no proposed dates.
The send-ready form of all three is Draft 0 in `../assets/negotiation-comms.md`.

---

## 1. The one rule

**Every give is attached to a get, in the same sentence, before the give is spoken.**

Not "let me see what I can do and I'll come back" — that is a give with the get postponed, and the get
never arrives, because by the time you come back the concession is the baseline. The construction is:

> "We can do **X** if you can do **Y** by **<date>**."

Three properties make it work. It is conditional, so nothing has been given yet. It is specific, so
there is no ambiguity about what was agreed. It is dated, so it expires. A concession without all
three is a donation with a covering note.

**The corollary:** if you cannot name a get, you are not ready to make the give. Go back to the ask
stack (Step 1, element 6) and pick one.

---

## 2. The ladder

Ordered by what it costs *us*, cheapest first. Climb one rung at a time.

| # | Give | Costs us | Required get | Approver |
| --- | --- | --- | --- | --- |
| 1 | **Payment terms** — Net 30 → Net 45 or 60 | Working capital only: `ARR × days/365 × cost of capital` | Signature by a named date | CSM / RM |
| 2 | **Waive or reduce the uplift** | The uplift, compounded forward on the base | 24- or 36-month term, or a two-year price lock in our favour | RM |
| 3 | **Enablement, training credits, premium-support trial, advisory-board seat** | Delivery hours at internal cost, not list | Exec sponsor meeting **plus** a written success plan with named owners | Manager |
| 4 | **0–5% discount** | 0–5% of ARR, permanently unless papered as one-time | Named signature date **plus** reference rights — e.g. two reference calls a quarter, one case study a year | Rep / RM |
| 5 | **5–10% discount** | 5–10% of ARR, compounding | Multi-year commitment **or** increased scope/seats | Manager |
| 6 | **10–15% discount** | 10–15% of ARR, compounding | Multi-year **plus** prepayment (annual or full-term upfront) | Manager / Director |
| 7 | **15–25% discount** | 15–25% of ARR, compounding | Multi-year **plus** prepay **plus** expanded scope **plus** logo and case-study rights | VP |
| 8 | **>25%, or any unprecedented term** | Margin, and the precedent for every account procurement talks to | Strategic justification, a board-visible logo, or a documented displacement threat | C-level / deal desk exception |

Approval bands of roughly 0–5% rep, 5–15% manager, 15–25% VP, and >25% or unprecedented terms at
executive level are a commonly published deal-desk convention `[V]`. **Replace them with your own
matrix from `cs-context` §2** — the point is not these numbers, it is that a number exists and that
crossing it requires a named human.

### Rungs 1–3 are the ones that matter

Most renewals that end in a discount could have ended at rung 1, 2 or 3. Three reasons teams skip them:

1. **They feel too small to offer.** They are not. Net 60 on a $500k account is real money to a
   procurement team measured on working capital, and it costs you a fraction of a discount point.
2. **The customer asked in percentage terms**, so the CSM answers in percentage terms. The customer
   asked in percentage terms because that is the only unit they were offered.
3. **Nobody costed them**, so they look like "nothing" rather than "cheap". Cost them once, in dollars,
   and rung 1 stops being a throwaway.

---

## 2b. The What-we-get catalogue

**`C12` — every ladder row and every counter row carries a non-empty What-we-get cell.** A row
without one is **invalid output**, not incomplete output: delete the row or name the get. There is
no `—` and no `n/a`.

Four constructions are ways of writing "nothing" that read as something:

| Not a get | Why it fails |
| --- | --- |
| **Goodwill, or the relationship** | Unpaperable, unmeasurable, and it cannot be shown to an approver |
| **"They renew"** | The renewal is what you are already selling. It cannot also be the payment for the discount that sells it |
| **"They stop asking"** | You bought quiet for a year and set next year's floor while doing it |
| **An expansion inside 90 days of `D`** | It co-terms by `R12`. Using it as ladder currency trades a thing you were owed anyway |

**The catalogue** — what is actually available, roughly in order of how easily a customer can say yes:

| Get | What it is worth to us | How to phrase the ask |
| --- | --- | --- |
| **A named signature date** | Cycle certainty, and it ends the drift | "…if we can get signature by the 14th" |
| **Term length (24/36 months)** | Removes one or two renewal events and their loss probability | "…on a 24-month term" |
| **Prepayment (annual or full-term)** | `ARR × months/12 × cost of capital`, and it removes collections risk | "…with the first year prepaid" |
| **Reference rights** | Named pipeline value; ask sales what a reference call is worth | "…two reference calls a quarter" |
| **A case study, with logo rights** | Reusable, and it survives the champion leaving | "…one case study a year, with your logo" |
| **An executive sponsor meeting, dated** | Repairs Gate A and Gate B at once | "…and thirty minutes with Dana before the end of the month" |
| **A written success plan with named owners** | The artifact next year's value case is built from | "…and we agree the plan for the year in writing" |
| **Scope or seats at list** | Revenue, and it re-anchors the unit price | "…if we take the Finance team on at list" |
| **Removal of an expiring discount** | Restores the base | "…and the transition credit comes off as planned" |
| **An advisory-board seat** | Costs hours, buys roadmap credibility and a live relationship | "…and you join the customer advisory board" |
| **A co-term that simplifies next cycle** | One paper cycle instead of two | "…and we align the add-on to the same date" |
| **Retention of the notice window, auto-renew, uplift clause and audit rights** | Next year's leverage — often the quietest and most valuable get of all | "…and the renewal terms stay as they are" |

**Costing a get.** A get is worth naming only if you can say what it is worth or what it prevents.
Two reference calls a quarter is worth what your sales team pays for a reference. A 24-month term is
worth the loss probability of the renewal you no longer run, plus the cycle cost. If you cannot say
either, you have named an activity, not a get.

---

## 3. Costing each rung

Run `scripts/concession_math.py ladder --arr <A> --tenure <n> --cost-of-capital <r> --uplift <u>`.
The formulas it uses:

| Rung | Annual cost | Lifetime cost (tenure `n`, uplift `u`) |
| --- | --- | --- |
| 1 · Payment terms `d` extra days | `ARR × d/365 × r` | Recurs each year: `× n` |
| 2 · Uplift waiver | `ARR × u` | `ARR × ((1+u)^n − 1)` — the base never catches up |
| 3 · Services/credits | Internal delivery cost of the hours, **not** list price | Usually one-off; recurring only if you promised it every year |
| 4–8 · Discount `k` | `ARR × k` | `ARR × k × n`, plus the escalator forgone on the discounted portion |

**Two costing errors that recur.**

- **Costing services at list.** A $20k training package that costs you 6 delivery days is not a $20k
  concession, and pricing it as one makes it look far more generous than it is — to you. To the
  customer it is worth what it does for them, which may be more than $20k or nothing at all.
- **Costing a discount for one year.** Discounts are annuities. A 10% discount on $300k across a
  four-year expected tenure is $120k before the escalator effect, and the escalator effect is real:
  every future uplift applies to the reduced base.

**Round the lifetime figure to two significant figures when you state it** (`§4F`) — `$120k`, not
`$121,447`. It rests on an assumed tenure, and stating it to the dollar implies a measurement nobody
took.

---

## 4. The scripts

Say these out loud. They are short on purpose; the pause after them does the work.

| Situation | Say |
| --- | --- |
| **Opening a demand** | "Before I price anything — what's driving the number? Is it the budget line, the timing of when it lands, or the scope?" |
| **Rung 1** | "We can move you to Net 60 if we can get signature by the 14th." |
| **Rung 2** | "I can hold your rate flat for the coming term if we go 24 months. That's the trade — flat rate for term length." |
| **Rung 3** | "I can put a two-day enablement session and a quarter of premium support in, if we can get thirty minutes with whoever owns this outcome and agree a written plan for the year." |
| **Rung 4** | "Five percent works if we sign by the 14th and I can put you down for two reference calls a quarter." |
| **Rung 5–6** | "Ten percent is available on a 36-month term with the first year prepaid. On a one-year deal it isn't." |
| **They ask for more, again** | "I've moved once. What moves on your side if I look at this again?" |
| **They will not name a get** | "I can't take a number back to my side without something attached to it. What's easiest for you to give?" |
| **They cite a competitor price** | "Send me what's in that quote and I'll compare like for like. If it genuinely covers the same scope, that's a real conversation — I just can't price against a number I can't see." |
| **Refusing a never-concede term** | "That one I can't do at any level — it isn't a pricing decision, it's a term that changes every other agreement we have. Here's what I can do instead." |
| **Closing a concession** | "So: <give>, in exchange for <get>, signed by <date>. I'll put exactly that in the order form and send it today." |

**After a concession, stop talking.** The most expensive seconds in a renewal are the ones a nervous
rep fills by sweetening an offer that had not yet been refused.

---

## 5. Never-concede register

Print this every run, even when nothing has been requested. Its value is that it is decided in advance.

### Never without VP+ approval — these four set *next year's* leverage

| Term | Why it is on the list | What it costs when given |
| --- | --- | --- |
| **The notice window** | Shortening it removes your ability to detect a decision in time to act on it | The next churn arrives with no lead time. `R1` stops working for this account |
| **The auto-renew clause** | Removing it converts every renewal into an affirmative sale | Full ATR at risk every term, and a forecast that cannot reach Commit |
| **The uplift clause** | Without it, every future increase is a fresh negotiation from zero | The base flatlines; compounding works against you for the life of the account |
| **Audit and true-up rights** | Without them, over-use is unpriceable | Under-licensing becomes free, and the restructure rung disappears |

Their loss is invisible for a full cycle, which is exactly why they need a named approver rather than
a judgement call at 6pm on the last day of the quarter.

### Never at any level

| Term | Why |
| --- | --- |
| **MFN / most-favoured-nation pricing** | Binds every future deal you do with anyone, and makes this customer a party to negotiations they are not in |
| **Unlimited liability** | Uninsurable, and no commercial upside can price it |
| **Termination for convenience with no fee and no notice** | The contract becomes a monthly deal with an annual invoice. Price it as monthly or refuse it |
| **Source-code escrow** | Deal-desk exception only, never a rep-level give |
| **Unmetered usage on a metered product** | Removes the unit economics entirely and cannot be undone at renewal |
| **An SLA credit regime you cannot operate** | You will breach the promise you invented to close, which is worse than the discount you avoided |
| **A permanent base reprice dressed as a one-time credit** | The single most common way a "one-time" concession becomes a new list price. §6 is the guard |
| **A roadmap or fix date nobody has agreed internally** (`R19`) | The second missed date costs more than this deal |

---

## 6. One-time without repricing

A concession is one-time only if all six of these are true. Miss one and you have a new price with an
optimistic note attached.

| # | Requirement | The wording that satisfies it |
| --- | --- | --- |
| 1 | **List price stated and unchanged** on the order form | "Annual subscription: $412,000" appears at list, before any credit |
| 2 | **The concession is a named credit line with an end date** | "Q1 transition credit: −$20,600. Applies to the term ending 31 January 2028" |
| 3 | **Snap-back language in the same document** | "Fees for any subsequent term revert to the then-current list price plus the escalator in §7.2" |
| 4 | **A get, named in the same paper** | "In consideration of a 24-month term and two customer reference calls per quarter" |
| 5 | **The words "one-time" in the covering email**, not only the contract | The email is what gets forwarded to their finance team, and it is what they will quote back |
| 6 | **Logged with a reason code** | `value_delta_reason = discount_concession`, per `../../cs-context/references/normalized-schema.md` |

**Why the credit-line form beats a percentage.** A 5% discount folded into the unit price is invisible
by next cycle: the new unit price simply *is* the price, and there is nothing on the paper to expire.
A named credit against a stated list price is visible, dated, and self-cancelling. The customer sees
the same net number either way; you keep an anchor.

**Preference order when something must be given:**

```
payment timing  →  scope or entitlement  →  a term-limited credit  →  a percentage off the base
       cheapest                                                            permanent by default
```

**The precedent, stated plainly.** The discount you approve is the floor they negotiate from next
cycle. It travels inside their organisation — the person who got it tells the person who did not — and
outward, through procurement networks and benchmarking services whose entire business is collecting
what vendors actually accepted. Practitioner analyses of subscription cohorts report discount-acquired
customers showing higher price sensitivity and weaker lifetime value than full-price cohorts `[P]`;
treat that as directional and settle it on your own book by comparing GRR and expansion rate for
discounted versus undiscounted accounts.

---

## 7. Reading their constraint

Roughly half of price demands are not about price. Diagnose before pricing.

| Their words | Likely constraint | The cheap answer | The expensive answer you would otherwise give |
| --- | --- | --- | --- |
| "We need to get this under $400k" | A budget line already approved at $400k | Move $12k of services to next fiscal year; keep the subscription rate | A 4% discount, permanently |
| "We can't sign before April" | Budget period, not price | Co-term to April with a stub; hold the rate | A discount to make Q1 work |
| "Procurement needs to show a saving" | Their internal scorecard | Give a documented saving that is not the subscription rate: waived services, extended terms, bundled training | A rate cut that recurs forever |
| "This is more than we can justify" | Missing value evidence, not missing budget | Build the value artifact and re-present. This is a rung-0-or-2 problem, not a rung-4 one | A discount that confirms the price was inflated |
| "We're only using half of it" | Over-entitlement | Right-size, and trade the reduction (Step 7 of `../SKILL.md`) | A discount on seats they will still not use |
| "Another vendor quoted 30% lower" | Possibly true, of a different scope | Scope-normalise, then price switching cost from their numbers | Matching a number whose scope you never saw |

**The question that opens all of these:** *"Before I price anything — what's driving the number? Is it
the budget line, the timing of when it lands, or the scope?"* Ask it first, every time. It costs
nothing and it is the single highest-yield sentence in this file.

---

## 8. Ladder discipline

| Rule | Why | The failure it prevents |
| --- | --- | --- |
| **One rung per meeting** | Two rungs in one meeting tells them the ladder has more rungs | The slide from 20% to 12% to 8% with nothing received |
| **Never open at the walk-away** | An opening equal to the floor is an ultimatum with extra steps | Having nowhere to go, then going there anyway |
| **Never move without a get** | See §1 | Every give becomes the new baseline |
| **Never trade against yourself** | If they have not refused, do not improve | Bidding against silence |
| **Log every rung offered, not only accepted** | An offered rung is next year's floor whether or not it was taken | Next cycle opening 10% below this cycle's close |
| **Escalate on terms, not on price** | Price has a matrix; unprecedented terms need judgement | A rep conceding an MFN clause because it "wasn't about money" |
| **Stop when the walk-away is reached** (`R21`) | The walk-away is a decision made calmly in advance | Discovering your floor was soft, in front of procurement |

**Walk-away discipline.** The walk-away has two halves and both are binding: a number *and* a set of
terms. An account that meets the number while demanding an MFN clause is below the walk-away. Write
both halves down, get them approved, and take them into the room on paper.

---

## 9. The concession log

One row per concession offered — accepted or not. Keep it with the account, not in someone's inbox;
its whole value is that it survives the person who made the trade.

| Field | Notes |
| --- | --- |
| Date · cycle | Which renewal |
| Rung | 1–8, from §2 |
| Give (exact wording) | As it appeared in the paper |
| Annual cost $ · lifetime cost $ | From `concession_math.py`; lifetime rounded to 2 s.f. |
| Get, and whether it was delivered | The unenforced get is the commonest silent loss — reference calls agreed and never scheduled |
| Approver and date | The named human |
| Offered but not accepted? | Yes/no — these still set next year's floor |
| Snap-back present? | Yes/no, with the clause reference |
| Reason code | `discount_concession`, `seat_reduction`, `price_uplift`, per the normalised schema |

**Two reports this log makes possible**, both of which change behaviour:

1. **Realised concession rate by segment and by rep** — what your book actually gives away, against
   what the matrix says it should.
2. **Get-delivery rate** — the share of gets that were actually collected. It is usually low, and it
   is the cheapest revenue in the business: reference calls, case studies and advisory seats already
   agreed and never scheduled.

---

## 10. Failure modes

| Failure | What it looks like | Correction |
| --- | --- | --- |
| Negotiating the percentage | 20 → 12 → 8, nothing received | Diagnose the constraint (§7), then climb from rung 1 |
| The postponed get | "Let me see what I can do" | Conditional, specific, dated — in the same sentence as the give |
| Two rungs in a meeting | 5% *and* Net 60 offered together | One rung, then silence |
| Bidding against silence | Improving an offer that was never refused | Ask what they think of the current one |
| Services costed at list | "$20k of enablement" that costs six days | Cost at internal delivery cost; describe at customer value |
| One-year discount maths | "It's only $30k" | Lifetime cost, plus the escalator forgone on the reduced base |
| The unpapered "one-time" | A percentage folded into the unit price | All six requirements in §6, or it is permanent |
| The uncollected get | Reference calls agreed, never scheduled | Get-delivery rate in the concession log, reviewed quarterly |
| Never-concede terms given under deadline | MFN accepted at 6pm on the last day | The register is decided in advance precisely so that 6pm has nothing to decide |
| A concession discussed with the customer before it was approved | "I think we can probably do ten" | Never float an unapproved number. It is now the floor |
| The CSM conceding to preserve the relationship | Price given to avoid an uncomfortable conversation | RM owns price, CSM owns value; run the two conversations on different days |
