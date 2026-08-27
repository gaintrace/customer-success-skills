# The Expansion Business Case

> Read this when writing the one-pager the champion takes to their own finance team. The
> audience is not your customer contact — it is the person on their side who has never met you
> and will approve or reject a line item on the strength of this page alone.

**Contents**
1. [Who actually reads this](#1-who-actually-reads-this)
2. [The eight-section structure](#2-the-eight-section-structure)
3. [The ROI arithmetic](#3-the-roi-arithmetic)
4. [The assumptions register](#4-the-assumptions-register)
5. [Presenting options, including "do nothing"](#5-presenting-options-including-do-nothing)
6. [Data lineage](#6-data-lineage)
7. [The approval path](#7-the-approval-path)
8. [Language rules](#8-language-rules)
9. [The value-first sequence](#9-the-value-first-sequence)
10. [Review checklist](#10-review-checklist)

---

## 1. Who actually reads this

| Reader | What they are looking for | What kills it for them |
| --- | --- | --- |
| **Your champion** | Something they can forward without editing, that will not embarrass them | Vendor language, unsourced numbers, anything they would have to defend on your behalf |
| **The economic buyer** | The outcome, the cost, the payback period | A feature list |
| **Their finance partner** | Whether the numbers are reproducible and where the assumptions are | Round numbers with no derivation; a benefit case built entirely from vendor estimates |
| **Their procurement** | The commercial structure, the term, and what happens at renewal | An option set with only one option |

Write for the finance partner. The champion forwards it; the buyer skims it; finance is the
one who checks the arithmetic. A business case whose numbers the customer's own admin cannot
reproduce from their own systems is a liability, not an asset.

---

## 2. The eight-section structure

One page for the executive version. The appendix carries the math.

| § | Section | Content | Length |
| --- | --- | --- | --- |
| 1 | **The outcome you are pursuing** | Their stated goal, quoted verbatim, with the date and the person who said it | 2 lines |
| 2 | **Value delivered to date** | Three quantified outcomes: baseline, current, delta, and the customer-side person who validated each | Table, 3 rows |
| 3 | **The constraint** | The signal expressed as blocked people, blocked work, or forgone value — with raw counts and the date range | 3 lines + 1 chart |
| 4 | **The gap, quantified** | Annual value forgone vs cost to close it; ROI multiple; payback in months | Table |
| 5 | **Options** | ≥2 commercial structures **plus "do nothing"**, each with its 12-month total cost to the customer and the indifference point | Table |
| 6 | **Recommendation** | One option, one quantity, one price, one date — and why not the others | 3 lines |
| 7 | **Risks and guardrails** | What could make this the wrong call, and the trigger that would withdraw it | 3 bullets |
| 8 | **Approval path** | Named approver, required artifacts, budget-cycle timing | 3 lines |
| — | **Appendix** | Full arithmetic, data lineage (system · field · query date), cohort definitions with n | As needed |

Section 2 comes before section 3 for a reason. A constraint presented before value has been
evidenced reads as a sales problem; the same constraint presented after reads as a business
problem you happen to be able to solve.

---

## 3. The ROI arithmetic

The case is built in **their** units, from **their** validated numbers. Any input that is
yours must be labelled as a vendor estimate on the page, not in a footnote.

```
Annual value per unit   = quantity saved per unit per period × their loaded rate × periods/yr
Cost per unit           = p_eff (or list × (1 − discount)) for the proposed units
ROI multiple            = annual value per unit ÷ cost per unit
Payback (months)        = (cost per unit ÷ annual value per unit) × 12
Value forgone today     = constrained units × annual value per unit
Cost to remove it       = constrained units × cost per unit
Net annual value forgone= value forgone − cost to remove
```

### Worked, in the customer's own numbers

| Input | Value | Whose number | Date validated |
| --- | --- | --- | --- |
| Hours saved per active user per week | 3.2 | Theirs — internal time study | 2026-03-14, validated by Dana Osei, VP Operations |
| Loaded hourly cost | $62 | Theirs — Finance standard rate | 2026-01, FY26 rate card |
| Working weeks per year | 46 | Theirs — after PTO and holidays | 2026-01 |
| Blocked users, 60 days | 18 distinct | Ours — auth logs, reproducible in their admin console | 2026-06-26 → 2026-08-24 |
| Cost per seat | $1,250 | Contract — `p_eff` = ARR ÷ seats | 2026-08-26 |

```
Annual value per active user = 3.2 × 62 × 46      = $9,126
ROI multiple                 = 9,126 ÷ 1,250      = 7.3×
Payback                      = (1,250 ÷ 9,126)×12 = 1.6 months
Value forgone (18 blocked)   = 18 × 9,126         = $164,268 / yr
Cost to remove it            = 18 × 1,250         = $22,500 / yr
Net annual value forgone     =                      $141,768
```

**Three ways this arithmetic goes wrong**, and the correction:

| Failure | Correction |
| --- | --- |
| The hours-saved figure is a vendor benchmark | Use their study, or run one with them. If neither exists, state the case in *units of blocked work* and let them price it |
| The loaded rate is the salary, not the loaded cost | Ask Finance for the loaded rate; the difference is typically material and using the wrong one is the first thing they will catch |
| Value is claimed for all users rather than the constrained ones | The case is about the units that are blocked or about to be, not the whole population |

---

## 4. The assumptions register

Every business case has assumptions. Hiding them is what makes a case fragile; listing them
with an owner is what makes it survive scrutiny.

| Assumption | Value | Whose | Sensitivity | If it is wrong |
| --- | --- | --- | --- | --- |
| Hours saved per user per week | 3.2 | Theirs, 2026-03 | ±1.0 h moves ROI from 5.0× to 9.6× | Case still clears 3× at the low end; state that |
| Loaded hourly cost | $62 | Theirs, FY26 | ±$10 moves payback 1.4→2.0 months | Immaterial to the decision |
| Net-new-user velocity | 9/month | Ours, trailing 3m | If it halves, Base drops 31 → 16 seats | Recommendation drops to Floor; say so in advance |
| Blocked users are all real employees | 18 | Ours, auth logs | If 4 are service accounts, forgone value drops to $127,764 | Verify with their admin before sending |
| Growth continues at the trailing rate | 12% MoM | Ours, trailing 6m | Below 8% the tier upgrade stops paying back inside the term | Guardrail: withdraw the recommendation in writing |

**Publish the sensitivity, not just the point estimate.** A case that states "at half the
assumed velocity this is still a 3.4× return" is far harder to reject than one that states a
single number.

---

## 5. Presenting options, including "do nothing"

Always ≥2 structures **plus the null option**, each with the 12-month total cost to the
customer. The null option is not a courtesy — it is the thing that makes the other two
credible, because it proves you ran the arithmetic that could have cost you the deal.

| Option | Structure | 12-month cost to them | What they get | What they give up |
| --- | --- | --- | --- | --- |
| **A** | 31 seats added mid-term, co-termed at the current rate | $16,146 this term, $351,250 at renewal | 18 blocked people unblocked now; headroom to the renewal | Rate stays at $1,250; no volume tier benefit |
| **B** | Early renewal at 300 seats, repriced to the 300+ tier | $345,000, new 12-month term from today | $1,150/seat, 19 seats of headroom, term reset | Term restarts; budget lands this quarter |
| **Do nothing** | No change | $312,500 | Nothing changes | The pool exhausts in ~6 weeks; 18 people stay blocked; $141,768 of net annual value forgone continues |

**The indifference point belongs on the page.** For metered upgrades, state the usage level at
which the two options cost the same, and where they sit today relative to it. If they are
below it, the honest recommendation is to stay — write that down. That single sentence is
what makes every later recommendation from you credible.

---

## 6. Data lineage

Every number in the executive section traces to a system, a field and a date in the appendix.

| Figure in §3–§4 | System | Object · field | Query window | Reproducible by them? |
| --- | --- | --- | --- | --- |
| 18 blocked users | Auth / provisioning log | `seat_limit_reached` · distinct `attempted_user_email` | 2026-06-26 → 2026-08-24 | Yes — admin console → Access log |
| 236 active users | Product analytics | distinct actors with ≥1 core action, 30d | through 2026-08-24 | Yes — Admin → Usage report |
| 250 contracted seats | CRM | `subscription.seats_purchased` | as of 2026-08-26 | Yes — their signed order form |
| $1,250 per seat | Derived | `account.arr` ÷ `subscription.seats_purchased` | 2026-08-26 | Yes |
| 3.2 hours / user / week | **Theirs** | Internal time study | 2026-03-14 | Their own document |

If a row cannot be marked "reproducible by them", either find a source that can be, or move
the figure out of the executive section and into the appendix as an estimate.

---

## 7. The approval path

Three lines, and they are the three that determine whether this closes on time.

| Field | Example | Why it matters |
| --- | --- | --- |
| **Named approver and threshold** | "Dana Osei approves to $50k; above that, CFO sign-off" | Determines whether Option A or B is even reachable this quarter |
| **Required artifacts** | "PO required; security re-review not required for a seat add; updated order form" | Each missing artifact is a week |
| **Budget-cycle timing** | "FY27 planning locks 2026-11-01; a mid-term add-on draws from the FY26 line" | Determines co-term vs early renewal more often than the arithmetic does |

Ask for all three explicitly. "What would have to happen on your side for this to be approved
before the end of October?" gets a better answer than any inference from the org chart.

---

## 8. Language rules

| Never write | Write instead |
| --- | --- |
| "I noticed you were on our pricing page" | "Something seems to have changed on your side — what is driving the timing?" |
| "You're at 96% of your licences" | "Eighteen named people were denied access 41 times last month" |
| "We'd love to grow the partnership" | "You exhaust the pool in about six weeks; here are two ways to handle it" |
| "Most customers your size buy X" | "Of the 44 companies in your vertical and revenue band on our platform, 31 run X alongside what you have — here is the specific reason it fits your Q3 goal" |
| "This is a great deal if you sign this quarter" | "Here is the indifference point. Below it you should stay where you are" |
| "Let's schedule time to discuss expansion" | "Can Dana approve $16k from the FY26 line, or does this need to wait for FY27 planning?" |

Two structural rules:

- **The customer-facing one-pager and the internal artifact are separate documents.** Health
  bands, propensity, ranked value, churn language and CSM-hour estimates never appear in the
  customer-facing file. If they must appear in the same response, separate them with
  `--- CUSTOMER-FACING BELOW THIS LINE ---` and restate the warning.
- **Do not name the telemetry.** Signals time the outreach; they do not justify it aloud. The
  customer should hear about their blocked colleagues, not about your event stream.

---

## 9. The value-first sequence

The order the case is *delivered* in, as opposed to the order it is written in. Each step
completes before the next begins; skipping any one turns the conversation into a price
negotiation, because the customer is being asked to fund something whose value is still
theoretical to them.

| # | Step | Proof required before advancing |
| --- | --- | --- |
| 1 | Evidence of delivered value | A quantified outcome the **customer** validated — their baseline, their number, their attribution — dated within 120 days |
| 2 | Confirm their forward goal | Their stated next objective, in their words, in the success plan |
| 3 | Surface the constraint as their fact | "Eighteen people were blocked 41 times", not "you're at 94% utilisation" |
| 4 | Quantify the gap | Value forgone per year vs cost to close it, with the ROI multiple and payback in months |
| 5 | Present options including "do nothing" | ≥2 structures plus the honest null option, with the indifference point |
| 6 | Ask | A specific quantity, price, structure and date |
| 7 | Confirm the procurement path | Named approver, required documents, budget cycle |

Steps 1–2 are the customer's material; steps 3–5 are yours; steps 6–7 are the transaction. If
you cannot complete step 1 from the customer's own validated numbers, the motion is not an ask
— it is a value-proof engagement, and the ask waits.

---

## 10. Review checklist

Before the one-pager leaves your hands:

- [ ] §1 quotes their goal verbatim, with a date and a named person
- [ ] §2 has three outcomes, each with baseline, current, delta and a customer-side validator
- [ ] §3 states the constraint in people or units, with raw counts and a date range
- [ ] §4 shows the ROI multiple and payback, computed from **their** numbers
- [ ] §5 has ≥2 structures plus "do nothing", each with a 12-month cost to them
- [ ] The indifference point is stated where a metered upgrade is involved
- [ ] §6 names one option, one quantity, one price, one date, and why not the others
- [ ] §7 names the guardrail that would withdraw the recommendation
- [ ] §8 names the approver, the artifacts and the budget-cycle timing
- [ ] Every executive-section figure appears in the lineage table and is reproducible by them
- [ ] Every assumption appears in the register with its sensitivity
- [ ] No internal language: no health band, no propensity, no ranked value, no CSM hours
- [ ] No unsourced benchmark, and no vendor estimate presented as their number
