# Expansion Business Case — One-Pager Template

> **CUSTOMER-FACING.** Everything below this heading is written for the customer's champion to
> forward without editing. Read `../../cs-context/references/customer-voice.md` before writing a
> word of it, and emit it **below the divider**, never in the same block as internal analysis:
>
> ```
> ════════════════════════════════════════════════════════════
> CUSTOMER-FACING — copy the block below and send as written.
> Everything above this line is internal. Do not forward it.
> ════════════════════════════════════════════════════════════
> ```
>
> **Three rules, all of them hard.**
>
> **1 · No unfilled placeholders.** Every `<…>` is replaced with a real value before this leaves
> your hands. A page containing `<champion name>` is not send-ready, and the most common way an
> unedited template reaches a customer is that it looked finished. If a value is genuinely
> unavailable, delete that row or that sentence and raise the gap *above* the divider as
> `UNKNOWN — requires <source>`. Never write an estimate where a measurement belongs — `Not
> measured` is an acceptable cell value; a plausible-looking number is not.
>
> **2 · The disclosure firewall.** None of this appears here in any wording, however softened:
> health score or band, risk score or band, ARR at risk, exposure, propensity, ranked value, CSM
> hours, throughput, forecast category, save play, coverage tier, book size, competitor
> intelligence, champion-departure inferences, how the signal was detected, or any assessment of
> a named person. Every figure on the page must be one the customer can verify in their own
> systems or one they gave you. Run the leak scan in `customer-voice.md` before sending.
>
> **3 · Warmth is specificity, not adjectives.** Banned: "just checking in", "touching base",
> "circling back", "hope you're well", "as per my last email", "reaching out", "we value your
> partnership", "let me know your thoughts", "at your earliest convenience", "drive adoption",
> "leverage". The test — could this sentence go to any of forty customers? Then rewrite it.
>
> **If this is sent as an email body rather than an attached document,** convert it inside a
> fenced ```text block formatted for an email client: plain text, a blank line between
> paragraphs, `•` bullets indented two spaces, no markdown headings, no pipe tables (align
> columns with spaces), no `**` bold. Delete this instruction block before sending.

---

# <Product / SKU> — proposal for <Customer>
**Prepared for <champion name, title> · <date> · Prepared by <your name, title>**

## 1. The outcome you are pursuing

> "<Their goal, quoted verbatim>"
> — <name, title>, <date, meeting or email>

## 2. What has been delivered so far

| Outcome | Baseline | Today | Change | Validated by |
| --- | --- | --- | --- | --- |
| <outcome 1> | <value, date> | <value, date> | <delta> | <their name, title, date> |
| <outcome 2> | | | | |
| <outcome 3> | | | | |

<One sentence naming which of these matters most to the goal in §1.>

## 3. The constraint

<N> <people / units / requests> <were blocked / exceeded the allotment / were denied> <M>
times between <start date> and <end date>. <One sentence on what work did not get done as a
result.>

| Measure | Value | Where you can see it yourself |
| --- | --- | --- |
| <Blocked people / units over allotment> | <N> | <their admin console path> |
| <Current usage vs entitlement> | <X of Y> | <path> |
| <Time until the limit is reached at the current rate> | <N weeks> | <derivation> |

## 4. What the gap is worth

| Input | Value | Source |
| --- | --- | --- |
| <Value per unit per period> | <value> | <their study / their rate card, date, validator> |
| <Loaded cost basis> | <value> | <their finance rate card, date> |
| Annual value per <unit> | <value> | <arithmetic> |
| Cost per <unit> | <value> | <contract / price book> |
| **Return multiple** | **<X>×** | annual value ÷ cost |
| **Payback** | **<N> months** | (cost ÷ annual value) × 12 |
| Annual value currently forgone | <value> | <constrained units> × <annual value per unit> |
| Cost to remove the constraint | <value> | <constrained units> × <cost per unit> |
| **Net annual value forgone** | **<value>** | difference |

## 5. Your options

| Option | Structure | Cost to you over 12 months | What it changes | What it costs you |
| --- | --- | --- | --- | --- |
| **A** | <structure, quantity, rate, term> | <$> | <effect> | <trade-off> |
| **B** | <structure, quantity, rate, term> | <$> | <effect> | <trade-off> |
| **Do nothing** | No change | <current $> | Nothing changes | <the constraint continues; quantified> |

<For a metered or tier decision, state the indifference point here:>
> The two options cost the same at <usage level> per <period>. You are at <current level>
> today, and on your current trajectory you reach the crossover in <N> months. <If they are
> below it and will not cross inside the term, the recommendation is to stay — say so here.>

## 6. Recommendation

**<Option letter>: <quantity> <units> at <rate>, effective <date>.**

Not <other option>, because <one specific reason tied to their situation, not to your
preference>.

## 7. What would change this recommendation

- If <observable condition> falls below <threshold>, <this option stops paying back inside the
  term> — we will re-run the numbers on <date> and tell you if that happens.
- If <second condition>, <consequence and the alternative>.
- <Third risk and its guardrail.>

## 8. To approve this

| | |
| --- | --- |
| Approver | <name, title> |
| Approval threshold | <$ limit, and who is needed above it> |
| Documents required | <PO / order form / security review / DPA amendment / none> |
| Budget timing | <which fiscal line, and the date it locks> |
| Proposed decision date | <date> |

---

## Appendix — where every number comes from

| Figure | System | Object · field | Window | You can verify it at |
| --- | --- | --- | --- | --- |
| | | | | |

**Assumptions**

| Assumption | Value | Whose number | If it is wrong |
| --- | --- | --- | --- |
| | | | |

**Peer comparison** (only if the cohort has ≥20 accounts and no single customer is identifiable)

> Of the <N> companies in <vertical> at <ARR band> on our platform, <M> run <SKU> alongside
> what you have. <One sentence on why that is relevant to the goal in §1.>
