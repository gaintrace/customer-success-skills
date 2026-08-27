# The Value Evidence Pack

> Step 6 of `renewal-prep`. What to gather, how to quantify it, and how to get the customer
> to state the number themselves — because the pack exists to be used in a room you are not in.

**Contents**
1. [What the pack is for](#1-what-the-pack-is-for)
2. [Recovering the original business case](#2-recovering-the-original-business-case)
3. [The four value classes and how to quantify each](#3-the-four-value-classes-and-how-to-quantify-each)
4. [Getting the customer to state the number](#4-getting-the-customer-to-state-the-number)
5. [Quantifying switching cost](#5-quantifying-switching-cost)
6. [The artifact standard](#6-the-artifact-standard)
7. [Sequencing against the price conversation](#7-sequencing-against-the-price-conversation)
8. [Anti-patterns](#8-anti-patterns)
9. [Worked example](#9-worked-example)

---

## 1. What the pack is for

The renewal is defended in a meeting you are not invited to — a budget review, a vendor
rationalisation session, a conversation between the champion and the CFO. The pack's only job
is to survive that room without you in it.

That constraint sets the standard:

| Requirement | Because |
| --- | --- |
| Numbers in **their** metrics, not ours | "12,400 core actions" means nothing to a CFO. "Dispatch cycle 41 → 24 minutes" does |
| A named person on their side who validated each number | An unvalidated number gets challenged and the whole pack loses credibility with it |
| Every figure traceable to a system, a field and a date | A business case their own admin cannot reproduce is a liability |
| Baseline, current, delta — always all three | A current-state number with no baseline is a fact, not an outcome |
| One page for the executive; the maths in an appendix | The person defending it has ninety seconds |

**A value pack is not a usage report.** Usage evidences the outcome; it is not the outcome.
If the only thing you can show is that people log in, you have not built a value pack, you
have built an activity report — and activity reports lose to price.

---

## 2. Recovering the original business case

Everything is measured against what they said they were buying, not against what the product
turned out to be good at. Recover it before you gather anything.

| Source | What to look for |
| --- | --- |
| Original `opportunity` record and close notes | The stated problem, the stated metric, the stated target |
| The first order form and any statement of work | Scope actually contracted, which bounds what you can claim |
| Onboarding and implementation documents | Success criteria agreed at kickoff, and the dates promised |
| The first success plan | Milestones, owners and target dates as originally set |
| Early email threads with the buyer | Their words. Quote these; do not paraphrase them |
| Prior QBR or EBR decks | Outcomes previously agreed, and anything previously disputed |

If the business case cannot be recovered, write `UNKNOWN — requires the original opportunity
record or the buyer's own statement` and make recovering it a dated action. Do not substitute
a plausible one; a business case you invented will be corrected by the customer in the worst
possible room.

**Where the buyer has changed since purchase**, the original case still matters but the
current EB did not sign it. Recover the original, then re-baseline against the new buyer's
stated objective — and say explicitly which of the two you are measuring against.

---

## 3. The four value classes and how to quantify each

Every credible outcome falls into one of four classes. Use the customer's own inputs for
every variable; where you must use an assumption, label it as one and put it in the appendix
where they can change it.

### Class 1 — Hard cost removed

Money that used to leave the business and no longer does.

```
Annual value = (units_before × unit_cost_before) − (units_after × unit_cost_after)
```

| Evidence needed | Where it comes from |
| --- | --- |
| The line item that shrank or disappeared | Their finance system, or a stated figure from their team |
| The before and after quantities | Their records; ours only corroborate |
| Whether the saving was actually banked | The person who owns the budget line — a cost "saved" that nobody removed is not a saving |

The strongest class and the rarest. If you have one of these, it leads the pack.

### Class 2 — Cost avoided / capacity released

Work that no longer takes as long, or headcount that did not have to be added.

```
Annual value = hours_saved_per_period × periods_per_year × fully_loaded_hourly_cost
```

| Trap | Correction |
| --- | --- |
| Using an hourly rate we invented | Ask them for their loaded cost, or use a rate they supply. Label it as their input |
| Counting hours nobody would have spent | Only count work that genuinely happened before |
| Claiming released capacity as cash | Say "capacity released", not "cost saved", unless a role was genuinely not backfilled. Overclaiming here is how packs lose credibility |

State it as **capacity released** by default and let the customer upgrade it to cash if they
choose to. They frequently will, and it is far more powerful when it comes from them.

### Class 3 — Revenue enabled or protected

Revenue that exists, arrives faster, or stops leaking.

```
Annual value = incremental_units × contribution_per_unit
            or  (cycle_days_before − cycle_days_after) / cycle_days_before × revenue_at_risk
```

Attribution is the whole difficulty. Never claim the full revenue number. State the mechanism
and let them assign the share: *"deal cycle fell from 46 to 31 days across 240 deals — what
share of that would you attribute to this?"* A customer-assigned attribution percentage is
defensible in their budget meeting; ours is not.

### Class 4 — Risk and compliance

Exposure reduced, audits passed, incidents prevented, obligations met.

```
Expected annual value = P(event) × cost_of_event  −  cost_of_control
```

Hardest to quantify and often the most persuasive, because the buyer already knows the cost
of the event. Where probability cannot be sourced, do not invent one: state the exposure and
the control, and mark the probability `UNKNOWN — requires their risk register`. An honest
qualitative statement about a real obligation beats a fabricated expected value.

---

## 4. Getting the customer to state the number

A number we assert is a marketing claim. The same number in their mouth is a budget
justification. Run this sequence — usually inside the EBR at T-150 or T-120.

| # | Step | The move | What you are listening for |
| --- | --- | --- | --- |
| 1 | Establish the baseline | "Before you had this, how long did `<process>` take / how many `<units>` did you handle / what did `<line item>` cost?" | A number from them, with a unit. Write it down verbatim |
| 2 | Establish the present | "What is that number today?" | Their measurement, not ours. If they do not measure it, that is itself a finding |
| 3 | Let them name the delta | "So that is `<before>` to `<after>` — is that right?" | A confirmation. Do not compute the percentage for them yet |
| 4 | Ask what the delta is worth **in their terms** | "What does that difference mean for your team — is it hours, headcount, cycle time, cost?" | The conversion. This is the sentence you are running the whole meeting for |
| 5 | Ask for the money | "If you had to put a number on that for your CFO, what would you say?" | Their figure. It will often be more conservative than yours — use theirs anyway |
| 6 | Write it back and ask for a correction | "Here is what I heard — `<summary>`. Where have I got this wrong?" | A correction *is* an acknowledgement. Silence is not |
| 7 | Put their name on it | The summary goes in a document listing them as the source, dated | The artifact that scores 2/2 on MEDDPICC-R Metrics |

**Why step 6 works.** People decline to endorse a claim and readily correct one. Asking
"where have I got this wrong?" gets engagement from someone who would have ignored "does this
look right?", and the resulting document is jointly authored rather than vendor-authored.

**If they cannot state a number**, that is the most important finding in the renewal — not a
gap in your pack. It means nobody on their side has quantified the value, which means nobody
can defend it in a budget review. The action is to help them build the measurement now, and
the renewal is at risk until they can. Record it in the risk register with cause code
`value_not_evidenced`.

**Language to avoid, and what to use instead**

| Do not say | Say |
| --- | --- |
| "You're getting great ROI" | "You told us dispatch time went from 41 to 24 minutes — what is that worth across 3,000 dispatches a month?" |
| "Usage is up 30%" | "Eleven more people in Operations used this last month than in March, and none of them were trained by us" |
| "Most customers see 20% savings" | "What would you need to see to say this paid for itself?" |
| "We've delivered a lot of value" | "Which of the three outcomes from January is furthest from where you wanted it?" |

---

## 5. Quantifying switching cost

Procurement compares your price to an alternative's price. Switching cost is the number that
comparison omits, and nobody has given it to them.

| Component | How to count it | Source |
| --- | --- | --- |
| Integrations built | Count of live connections, and what each one feeds | `usage_daily.integrations_active`; their engineering team |
| Data under management | Records, volume, and how much history does not migrate | Product analytics; their admin |
| Trained users | Distinct active users × hours to competence | `usage_daily.active_users`; their enablement lead |
| Embedded workflows | Named processes that route through the product, and what happens if they stop | Their process owners |
| Reports and dashboards built | Count, and who consumes them | Product admin console |
| Custom configuration | Fields, rules, permissions, automations built over the term | Product admin console |
| Parallel-run period | Weeks both systems must run during a migration | Their IT, from a prior migration if they have one |
| Re-procurement effort | Their own security review, legal review and onboarding cost for a new vendor | Their procurement — ask; the number is usually larger than you expect |

Present it as a **one-time cost and an elapsed time**, not as a threat. "Standing up a
replacement looks like roughly `<N>` weeks of elapsed time and `<X>` of internal effort — here
is how we counted it. Worth having in the comparison." A switching-cost statement that reads
as a threat converts a champion into an adversary; the same numbers offered as an input to
their analysis are welcome.

---

## 6. The artifact standard

The pack is one page plus an appendix.

| Section | Content | Length |
| --- | --- | --- |
| 1. The outcome they were pursuing | Their stated goal, quoted, with the person and date | 2 lines |
| 2. Value delivered | 3 quantified outcomes: baseline · current · delta · $ value · their validator | Table, 3 rows |
| 3. Adoption evidence | Who uses it, which teams, trend over the term — supporting §2, not replacing it | 3 lines + 1 chart |
| 4. What is embedded | Switching-cost components as counts, not adjectives | Table |
| 5. What is not working | The honest one. Anything missed, late or unresolved, with the plan and date | 3 lines |
| 6. The forward objective | Their next stated goal and what it needs | 3 lines |
| Appendix | Every calculation, with system, field and query date for each input | As needed |

**Section 5 is not optional.** A pack with no problems in it is read as marketing and
discounted entirely. Naming the two things that went wrong, with dated remediation, is what
makes the other four sections believable — and the customer already knows about them.

**Data lineage rule:** every number in the one-page section must be reproducible from the
appendix by the customer's own admin. If they cannot reproduce it, do not print it.

---

## 7. Sequencing against the price conversation

| Gate | What happens | Why the order matters |
| --- | --- | --- |
| T-180 | Baseline captured; original business case recovered | You cannot show a delta without a baseline you recorded before you needed it |
| T-150 | Pack drafted; EBR booked with the economic buyer | |
| T-120 | **Pack delivered at the EBR.** Customer states the number. Uplift decided *internally* | Value lands as an independent fact, before any commercial ask exists |
| T-90 | Proposal delivered, referencing the value the customer stated at T-120 | The uplift now rests on something they said, not something you claim |
| T-60 | Negotiation. The pack is the answer to price objections, not a new argument | |
| Inside T-45 | **Never introduce value evidence for the first time here** | Arriving with new value evidence alongside a price ask reads as justification-shopping, and it is treated that way |

The gap between T-120 and T-90 is doing real work. Value delivered in the same conversation
as a price increase is heard as a sales argument. The same value delivered four weeks earlier
is heard as a status report — and it is still in the room when the price arrives.

---

## 8. Anti-patterns

| Anti-pattern | Correction |
| --- | --- |
| Value stated in product metrics | Convert to their business metric, or do not state it |
| One outcome, asserted by us | Three, customer-validated, with a named validator each |
| An ROI multiple with no inputs shown | Show every input, its source and its date, in the appendix |
| Loaded hourly rate we chose | Their rate, or labelled as an assumption they can change |
| Claiming released capacity as cash saved | "Capacity released" unless a role was genuinely not backfilled |
| Claiming full attribution for revenue | State the mechanism; ask them to assign the share |
| A pack with no problems in it | Section 5 names what went wrong, with dated remediation |
| Switching cost used as a threat | Offered as an input to their comparison |
| Delivering value evidence with the price | Value at T-120, price at T-90 |
| Reusing last year's pack with new dates | The baseline moves each term; so does the buyer |
| "They know the value, we don't need to write it down" | The person defending the line item is not the person who knows |

---

## 9. Worked example

Northwind Logistics · ATR $480k · pack delivered at the T-120 EBR, 2026-07-06.

**Original business case (VP Operations, 2025-01-14):** *"We need dispatch decisions made in
under half an hour without adding two more coordinators."*

| Outcome | Baseline | Current | Delta | Value (their figure) | Validator | Source |
| --- | --- | --- | --- | --- | --- | --- |
| Dispatch cycle time | 41 min (Jan 2025) | 24 min (Jun 2026) | −17 min (−41%) | "Two coordinator hires we didn't make" ≈ $186k/yr | R. Okafor, VP Ops, 2026-06-18 | Their WMS report + our workflow logs |
| Exception rework | 312 /mo | 118 /mo | −62% | 340 hours/mo released; they declined to convert to cash | R. Okafor, 2026-06-18 | Their ticketing system |
| On-time dispatch rate | 87% | 96% | +9 pts | Contract penalty exposure reduced; amount `UNKNOWN — requires their contract terms` | S. Berg, Logistics Dir, 2026-06-20 | Their carrier scorecard |

**What is embedded:** 4 live integrations (WMS, TMS, SSO, data warehouse) · 18 months of
dispatch history · 61 trained users across 3 sites · 9 saved reports consumed by their
weekly ops review · 2 workflows their carriers depend on.

**What is not working:** the Q1 API latency incident cost them three days of manual dispatch
and is unresolved for their overnight window — fix committed for 2026-09-30, owner named.

**The number, in their words** (R. Okafor, 2026-06-18): *"It's the two coordinators we didn't
hire. Call it a hundred and eighty."*

That sentence is the renewal. It is quoted in the proposal at T-90, it is what the champion
carries into the budget review, and it is worth more than any figure the vendor could have
produced — including a larger one.
