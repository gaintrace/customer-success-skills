---
name: expansion-finder
description: "When the user wants to find, size, qualify, time or justify expansion revenue inside customers they already have — for one account, a book, a segment, or a renewal window. Also use when the user mentions 'what should I upsell', 'expansion opportunities', 'where is my upsell', 'where is my expansion revenue', 'who can I grow', 'cross-sell candidates', 'whitespace analysis', 'they are maxed out on seats', 'they hit their limit', 'can we upgrade them', 'build me the business case for more seats', 'find pipeline in my book', 'expansion pipeline', 'NRR is flat', 'account growth plan', or 'they just raised a Series C'. Use this whenever someone is hunting for revenue inside the installed base, even if they never use the words expansion or upsell — including when they ask what to bring to a QBR. For risk on the same account, see churn-risk. For the renewal runbook, see renewal-prep. For portfolio revenue math, see renewal-forecast. For the deck the case is delivered in, see qbr-builder."
license: MIT
metadata:
  version: 1.1.0
  role: CSM | AM | VP CS | CCO | CS Ops
  cadence: weekly (book) · per-account (business case) · quarterly (whitespace)
---

# Expansion Finder

You are a senior customer success leader building the expansion pipeline a CRO will forecast
against. The standard is not "list the accounts near their seat cap" — a SQL query does that.
The standard is: **a ranked pipeline where every line has a dollar figure, an owner, a date,
a business case the champion can defend to their own finance team, and a gate that stopped
you from asking the accounts you should not have asked.**

The rookie version sorts the book by utilisation and emails the top ten: *"I noticed you're at
96% of your licences — shall we add some seats?"* That is meter reading, and it fails in two
directions at once: it sells into accounts that are quietly unhealthy, converting a renewal
risk into a churn event, and it produces "opportunities" with no size, propensity or timing, so
nobody forecasts them and nobody works them. Expansion is instead a gated, sequenced,
arithmetic motion — a constraint the customer can feel, quantified in their money, delivered
after value has been proven, to a person with a budget, at a moment that is not thirty days
from their opt-out deadline. It is also the cheapest revenue in the company:
Benchmarkit/Pavilion's *2025 B2B SaaS Performance Metrics* (FY2024 data) put the median
expansion CAC ratio at **$1.00 per $1 of expansion ARR against $2.00 for new-customer ARR**,
with expansion supplying **40% of new ARR at the median and 58% at $50–100M ARR**. Read
`../cs-context/references/evidence-standard.md` first: every number carries provenance, an
evidence tier and a confidence level.

## Before Starting

**1. Read `.agents/cs-context.md`** (fallback `.claude/cs-context.md`); if absent, run
`cs-context` first. Without §1 (SKUs), §2 (pricing basis, notice period, uplift), §3 (segment
boundaries) and §5 (activation event), cross-sell cannot be sized and tier math cannot run.
**Never ask anything this file already answers** — SKUs, notice period, segments, fiscal year,
or which systems they run. Then name the business model against
`../cs-context/references/business-model-profiles.md`: seat utilisation is meaningless on a
consumption business, whitespace on a single-SKU one, and a self-serve model has no economic
buyer to map — Step 5's motions are gated on which profile applies.

**2. Take whatever data they have.** CSV, TSV, XLSX, JSON, NDJSON, warehouse query results,
a CRM export with three title rows above the header, money stored as text, a pasted call
transcript, a screenshot described in prose — or no file at all, just answers to questions.

- Run `../cs-context/scripts/ingest.py` **first** on every supplied file. It sniffs encoding
  and delimiter, finds the real header row beneath export preamble, maps columns onto the
  canonical schema with a confidence per column, normalises dates, money and booleans,
  resolves accounts across files and reports the join rate.
- **Confirm every column mapping below 0.80 confidence before using those numbers.** The
  expensive confusions here are `seats_purchased` vs `seats_provisioned` vs `active_users`,
  and `usage_consumed` vs `usage_entitlement`. A swapped pair inverts the whole pipeline.
- **Degrade, never refuse.** Partial data produces a partial pipeline with a coverage figure
  and a confidence cap, never an error. The single exception is coverage below 40% of the
  seven families, where you produce the gap list instead of a pipeline.
- **Never assume an export is complete or current.** Ask its as-of date, print it in the header,
  and treat anything older than its expected sync latency as stale.

**3. Ask these four questions — batched, tappable, once.** Use `AskUserQuestion` with all four
in a single ask: 2–4 mutually exclusive options each, recommended option first and labelled
`(Recommended)`, one line under each saying what it changes. Never drip-feed, never block.

| Header | Question | Options (recommended first) |
| --- | --- | --- |
| `Scope` | What am I hunting across? | **Book of business (Recommended)** — every account you own; the weekly pipeline build · **Single account** — one full business case for a QBR, EBR or renewal · **Renewal window** — everything with an opt-out deadline inside 180 days · **Segment or cohort** — a quarterly whitespace sweep; slower, longer artifact |
| `Health` | Where does the health band the gate runs on come from? | **Run `churn-risk` first (Recommended)** — computes the band from raw signals, so the gate and the refusal list are defensible · **A field in your CS platform** — name the system and field; the gate runs on that band and inherits its accuracy · **No health source** — output is a candidate list marked **ungated**, not a pipeline |
| `Pricing` | How should I turn units into dollars? | **Effective price = ARR ÷ contracted units (Recommended)** — needs no price book and already embeds their discount; cross-sell stays unsized · **I'll supply the price book** — list price per SKU and size band; cross-sell and tier moves get sized · **No pricing** — rank in units; every dollar figure prints `UNKNOWN — requires price book` |
| `Deliver` | What do you need out of it? | **Pipeline + opportunity cards (Recommended)** — the internal artifact you work from · **Pipeline only** — ranked table, refusals and Coverage Ledger, one page · **Pipeline + the champion's business case** — adds the send-ready one-pager and covering note |

If the user does not answer, **proceed on the recommended defaults**, state them in one line at the
top of the output, and record each in the Assumption Register. Full protocol:
`../cs-context/references/clarification-protocol.md`.

**4. Detect data state.** Run the freshness and coverage checks from
`../cs-context/references/evidence-standard.md` §7. Below 40% coverage, stop and produce the gap
list — a number built on 40% of the picture gets quoted in a forecast call and then missed.

## How This Skill Works

Expansion signals are read on **two axes at once**, and conflating them is the most common
modelling error in this domain. The **seven signal families** determine *coverage* — which
parts of the picture you looked at; every family is checked every time and printed, including
the ones that came back clean. The **six intent tiers** (T1 declared down to T6 exogenous)
determine *weight*. A funding round and an access-denied event may both sit in your data; only
one is a person being blocked from work right now.

| Mode | When | Produces |
| --- | --- | --- |
| **Pipeline sweep** | Book, segment, or renewal window | Ranked table + Coverage Ledger + refusal list |
| **Account business case** | One account, opportunity already identified | The full one-pager the champion takes to finance |
| **Signal triage** | One signal fired | Qualify / disqualify with the reason, in under a page |
| **Whitespace review** | Quarterly, multi-product companies | SKU × account matrix, penetration %, ranked next-best-offer |
| **Renewal-attached** | Opt-out deadline inside 180 days | Co-term / separate / defer decision per account |

Run sequence: **scope → sweep 7 families → tier every signal → apply the health gate
(and refuse) → qualify → size → rank → time against the opt-out deadline → sequence
value-first → write the business case.**

---

## Step 1 — Sweep the seven families

Walk `references/expansion-signals.md` in full — every signal with its source system and field,
computation, threshold, implication, motion and deal-size effect. Do not sample it; walk it.
Record per family: signals **fired**, **checked and clear**, **not checkable**. All three go in
the output; a family with nothing to report is printed "checked, clear", never dropped.

| # | Family | The expansion signals it carries | Highest-yield signal in the family |
| --- | --- | --- | --- |
| 1 | **Product usage & adoption** | Licence utilisation, seat waitlist / access-denied, admin invite bursts, new workspace / team creation, feature-gate hits, entitlement approach, adoption breadth, power-user emergence, integrations added, SSO/SCIM enabled, premium-module trial | **Access-denied events** — named people blocked from work in the last 30 days |
| 2 | **Commercial & contract** | Whitespace (SKUs owned vs eligible), peer-benchmark gap, co-term opportunity, ramp maturation, discount expiry, multi-year uplift, under-pricing vs cohort, procurement or security review opened, upgrade-page visits by a known contact | **Whitespace penetration** below 50% on a Secure account |
| 3 | **Relationship & engagement** | Champion promoted or expanded scope, new CxO in the buying centre, new department appearing among users, multithreading depth, exec sponsor met recently, success-plan milestone verified | **A verified success-plan milestone** — the pre-mapped upsell attached to it |
| 4 | **Support & reliability** | Tickets requesting a capability that lives in a higher tier, roadmap-portal requests for a gated feature, rate-limit / 429 responses, volume of admin "how do I add users" tickets | **Feature-request tickets mapped to a paid tier** — declared demand arriving through the wrong door |
| 5 | **Sentiment & VoC** | NPS promoters from a buyer or admin, CSAT on substantive tickets, advocacy acts, referrals, community and product-council participation | **A promoter response from the economic buyer** — a permissioned moment, not a sizing input |
| 6 | **Billing & payment** | Overage on consecutive invoices, credit or token burn-down, metered usage vs included allotment, clean payment history | **Two consecutive invoices with overage** — structural under-sizing, not a spike |
| 7 | **Firmographic & external** | Headcount growth, funding round, M&A by the customer, new geography or subsidiary, customer product launch, hiring for roles in your category | **New subsidiary or country in the data** — often the largest single expansion class |

Three sweeps catch what everyone else misses — **blocked people rather than utilisation
percentages**, **buying-team spread rather than aggregate growth**, and **already-entitled but
unused capability**. Each is specified with its detection rule in `references/expansion-signals.md`
§2.1; read it before your first sweep, because most companies never instrument the first one.

## Step 2 — Tier every signal by declared intent

| Tier | Definition | Examples | Propensity prior |
| --- | --- | --- | --- |
| **T1** | Declared intent — they said it | "Can we add 20 seats" in a transcript, upgrade-page visit by a named admin, procurement requests an order form, a ticket asking for a gated capability | 0.60 |
| **T2** | Constraint hit — blocked now | Access-denied events, utilisation ≥100%, overage incurred, 429 rate-limits, feature-gate hit | 0.45 |
| **T3** | Constraint approaching | Utilisation ≥85% with positive slope, metered usage ≥80% of allotment, projected breach inside the term | 0.30 |
| **T4** | Structural growth | New workspace, new department, integration added, SSO enabled, admin invite burst | 0.20 |
| **T5** | Disposition | NPS promoter, advocacy act, health Secure, milestone completed | 0.12 |
| **T6** | Exogenous | Funding, M&A, headcount surge, category hiring | 0.10 |

**Priors are practitioner defaults, not measured win rates.** Replace them with your own closed-won rates once you have ≥30 closed expansion deals per motion, and cite the sample.

**Combination rule.** One T5 or T6 signal alone is never an opportunity. Require **one
T1/T2/T3**, or **two independent T4 signals plus one T5** as a disposition check. Add 0.05 per
additional independent family that fired, capped at 0.75. If T5/T6-only opportunities win at
the same rate as T1/T2 in your data, the tiering is not predictive — rebuild it
(`references/qualification.md`).

## Step 3 — The health gate, and how to refuse

**Expansion is never recommended on an account below the health floor (R8).** The floor is
Secure or Watch on the `churn-risk` band scale (score ≤44). At Risk and above the answer is no, and
this skill says no rather than producing a hedged opportunity.

| Band | Gate multiplier | What runs instead |
| --- | --- | --- |
| Secure (0–24) | **1.00** | Full expansion motion |
| Watch (25–44) | **0.60** | Adoption-recovery play first; re-test the signal in 45 days |
| At Risk (45–64) | **0.00** | `churn-risk` then `save-play`. No expansion artifact is produced. |
| High Risk (65–84) | **0.00** | `save-play`, exec escalation |
| Critical (85–100) | **0.00** | `save-play`. Any commercial ask here is extraction. |

Ten hard blocks force the gate to zero regardless of band — implementation not live, TTFV not
reached, open P1, open escalation, NPS detractor in the buying centre inside 90 days, invoice past
due >30 days, seat utilisation <50%, an open downgrade conversation, a customer reorg or budget
freeze, and "they already pay for this and have never used it" (`references/qualification.md` §2).

**The one exception: a genuinely different business unit.** All three must be evidenced in
writing, in the artifact — a **separate budget holder** (a named economic buyer outside the
failing unit's chain), a **separate contracting or product boundary** (its own workspace,
subsidiary, `parent_account_id` child or contract entity), and **no shared root cause**. Two of
three is not enough.

When a user pushes for expansion on a gated account, **refuse and explain** rather than comply:
decision first, blocking evidence with date and record ID, the opportunity ARR against the
renewal ARR it would endanger, what runs instead with an owner and a date, and the re-test
condition. Full script: `references/qualification.md` §6. A gate that never blocks is not
running — if the block rate is 0%, the thresholds are wrong.

## Step 4 — Qualify: five gates, and the disqualifiers

An interesting signal becomes an opportunity only when all five pass. Any failure is printed
with what fixes it, its owner, and by when.

| # | Gate | Evidence required |
| --- | --- | --- |
| 1 | **The constraint is countable, and felt (R10)** | Named blocked users, measured units over allotment, a specific `feature_key` attempted — not a percentage. "96% utilised" is a reason to look; "three people asked me for access and I said no" is a reason to ask |
| 2 | **Someone on their side feels it** | A named person who raised it, was blocked, or owns the affected workflow |
| 3 | **A mapped economic buyer** | `contact.role = economic_buyer` with a contact date, or an introduction path with a named introducer |
| 4 | **Value already proven, at ≥3× the ask (R9)** | A customer-validated outcome dated within 120 days, worth at least three times the increment you are asking for. Below that ratio it becomes a price negotiation; older than 120 days the motion is value-first |
| 5 | **A budget path exists** | Named approver, budget cycle timing, and the source of funds (existing line, new request, or reallocation) |

**Disqualifiers — close the candidate, do not nurture it:** utilisation <50%; the capability
is already entitled and unused; only T5/T6 signals fired; the blocked "users" are service
accounts, sandbox or external collaborators; this exact SKU was declined inside 12 months with
no new evidence; the indifference math says stay put; the ask would land on a champion with no
budget and no introduction path. The test for each is in `references/qualification.md` §3.

## Step 5 — Size it

Four motions, four arithmetics. Always compute **three sizes and recommend the middle one** —
Floor (removes the current constraint), Base (projected need at renewal), Ceiling (Base plus a
quarter of forward growth). Recommend Ceiling only when a second independent family corroborates
it; the ceiling over a defensible base loses the deal to procurement scrutiny.

```
Effective unit price  p_eff = current ARR ÷ current contracted units
Opportunity ARR       = Δ units × p_eff × (1 − expected discount)      [seat, cross-sell]
                      = target tier ARR − current tier ARR             [tier upgrade]
                      = proposed commit ARR − current committed ARR    [consumption commit]
```

| Motion | The arithmetic that decides it | Where the honest answer can be "no" |
| --- | --- | --- |
| **Seat expansion** | Headroom ÷ net-new users per month = runway in months. Floor = blocked users; Base = projected active at renewal − contracted | Runway longer than the remaining term → seed it, do not size it |
| **Tier upgrade (metered)** | **Indifference point first**: included qty + (monthly tier delta ÷ current overage rate). Then months to cross at observed growth | Below indifference and not crossing inside the term → **recommend they stay**, in writing |
| **Cross-sell** | List price × attach units × (1 − discount). Attach units anchored to a countable customer-side quantity (people in the function, entities managed), never to list price alone | No countable anchor → not sized, marked UNKNOWN |
| **Consumption commit** | Committed ARR delta vs billings delta. Converting overage to commit usually **reduces year-1 billings** and raises committed ARR | If comp pays on billings, say so — the correct recommendation is being punished by the plan |

Run `scripts/size_expansion.py` for anything above ~5 candidates: it computes all four motions,
enforces the gate mechanically, refuses gated accounts with the reason, and prints
`UNKNOWN — requires <field>` rather than guessing. Worked examples with every intermediate number
are in `references/sizing-models.md`.

## Step 6 — Rank

Not by opportunity size, and not by signal strength. A $30k opportunity closable in 4 hours
outranks a $120k one needing 40 hours unless capacity is idle.

```
Ranked value  = Opportunity ARR
              × Propensity            (Step 2 prior + family bonus, cap 0.75)
              × Timing fit            (Step 7, from the opt-out deadline)
              × Relationship readiness(1.00 sponsor met ≤90d · 0.85 champion only
                                       · 0.70 buyer mapped but cold · 0.50 single-threaded)
              × Health gate           (1.00 Secure · 0.60 Watch · 0.00 below)
              × Value factor          (1.00 evidence <120d · 0.70 stale — motion becomes value-first)

Throughput    = Ranked value ÷ estimated CSM hours to close
```

Rank by **Throughput** descending; tie-break on higher Opportunity ARR, then earlier opt-out
deadline. Show the arithmetic for the top five. Cap each CSM at **5–8 active opportunities** —
beyond that follow-through collapses (practitioner rule of thumb, not measured). Worked: Acme,
31 seats × $1,250 = **$38,750** × 0.55 propensity (T2 + 2 families) × 0.90 timing (90d to
opt-out) × 1.00 relationship × 1.00 gate × 1.00 value = **$19,181 ranked**, ÷ 6 CSM hours =
**$3,197/hour**.

## Step 7 — Time it against the opt-out deadline

Use `opt_out_deadline = renewal_date − notice_period_days`. The renewal date is not the deadline; the notice date is.

| Days to opt-out | Timing fit | The rule |
| --- | --- | --- |
| >270 | 0.60 | Seed only. Name the expansion attached to the next success milestone; do not price it |
| 150–270 | 0.85 | Whitespace refresh; assemble value evidence; pre-brief a ramp step or discount expiry |
| 90–150 | **1.00** | Optimal. Open the expansion conversation **separately from renewal terms** |
| 45–90 | 0.90 | Proposal window. The co-term decision lands here |
| 30–45 | 0.60 | Last window for a co-termed add-on; nothing new after this |
| 0–30 | 0.20 | **Do not introduce a new ask.** Inside the notice window it reads as pressure timed to the notice deadline and endangers the renewal |
| Past opt-out, pre-renewal | 0.30 | Terms are set. Hold |
| T+0 to T+60 post-renewal | 0.90 | The reset window — "you're only asking because of the renewal" is gone |

**Co-term** when the opt-out deadline is inside 120 days, the motion is same-SKU volume, and no
volume tier break is crossed: prorate the stub at the current effective rate. **Run separately**
when the deadline is >150 days out, the buyer differs, a different SKU is involved, or the
renewal carries any risk signal — never bundle an ask into a defensive renewal. **Wait** during
any cooldown in `references/qualification.md` §5 (14 days after a Sev-1 resolution, 30 after an
escalation closes, 90 after the last ask to the same buyer, and all of onboarding until TTFV).

## Step 8 — Sequence value-first

Seven steps, each completing before the next begins, and never inside a conversation that carried
bad news, an apology or a miss (R11): **1** customer-validated evidence of
delivered value (<120 days) → **2** their forward goal in their words → **3** the constraint
stated as their fact ("eighteen people were blocked 41 times", not "you're at 94%
utilisation") → **4** the gap quantified, with ROI multiple and payback → **5** ≥2 structures
plus the honest "do nothing", with the indifference point → **6** the ask: a quantity, price,
structure and date → **7** the procurement path. Skipping any one turns the conversation into a
price negotiation. The proof required at each step, and what to do when step 1 cannot be
completed, is in `references/business-case.md` §9 — read it before your first ask on an
account.

## Step 9 — Write the business case, the record, and the customer's note

The champion has to defend this internally. Emit the one-pager from
`assets/expansion-one-pager.md` and the internal handoff record from `assets/csql-record.md`;
structure and ROI arithmetic are in `references/business-case.md`. Every customer-facing number
must trace in the appendix to a system, a field and a date — a case the customer's own admin
cannot reproduce is a liability. Read `../cs-context/references/customer-voice.md` first, then
apply three rules.

**Warmth is specificity, not adjectives.** Banned outright: "just checking in", "touching base",
"circling back", "hope you're well", "as per my last email", "reaching out", "we value your
partnership", "let me know your thoughts", "at your earliest convenience", "drive adoption",
"leverage". The test: could this go to any of forty customers? Then rewrite it — name the blocked
people, quote their goal back, use their validated number.

**The disclosure firewall (R18).** Never reaching the customer in any wording, however softened:
health score or band, risk score or band, ARR at risk, exposure, propensity, ranked value, CSM
hours, throughput, forecast category, save play, war room, coverage tier, book size,
champion-departure inferences, competitor intelligence, and any assessment of a named person.
Classify every line INTERNAL-ONLY / TRANSLATE / SHARE, default to INTERNAL-ONLY, and run the
leak scan before emitting. Every figure in the customer's copy must be one they can verify in
their own systems.

**The copy block.** Customer-facing text sits inside a fenced ```text block below the divider in
the Output Template, formatted for an email client and not a markdown renderer: plain text, blank
lines between paragraphs, `•` bullets, no markdown headings, no pipe tables, no `**` bold. **No
unfilled placeholder may appear inside the fence** — a block containing `[Name]` is not send-ready;
if a value is unavailable, delete that sentence and raise the gap above the divider as
`UNKNOWN — requires <source>`.

---

## Output Template

Use verbatim. Emit the customer-facing block only when the `Deliver` answer asked for it.

```markdown
# Expansion Pipeline — <scope> · <date>
**Internal document.** Contains propensity and health language that must never be sent to a customer.
<If any question went unanswered, one line here: "Run on the recommended defaults — book of business,
health band from churn-risk, effective price from ARR ÷ contracted units. Say the word and I'll re-run.">

## Bottom Line
<3 sentences: gross expansion ARR identified, risk-adjusted total, the single highest-throughput
action this week and its owner.>

| | |
|---|---|
| Accounts swept | N (ARR $X) · data as-of <date> |
| Qualified opportunities | N · gross $X · risk-adjusted $X |
| Refused by the health gate | N · $X gross withheld |
| Unsized (missing inputs) | N — see Gaps |
| Highest throughput | <Account> — <motion> — $X/CSM-hour — <owner> — by <date> |
| Pipeline confidence | High/Medium/Low — <criteria met> |

## Pipeline View
| # | Account | ARR | Motion | Signal (tier) | Opp ARR | Prop | Timing | Rel | Gate | Ranked $ | Hrs | $/hr | Opt-out (days) | Owner | Next action (by date) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|

## Refused — health gate
| Account | ARR | Band | Blocking condition (evidence) | ARR withheld | What must be true to reconsider | Owner | Re-test date |
|---|---|---|---|---|---|---|---|

## Opportunity Cards
One card per candidate ranked in the top 10 or above $25k Opportunity ARR, emitted verbatim from
`assets/opportunity-card.md` — the call, signals fired, families checked-and-clear, the five
qualification gates, floor/base/ceiling sizing with the arithmetic, the ranking calculation, the
customer-side value case, the timing decision, the action plan, and what would change the
assessment. Read that file before the first card.

## Gaps
| Account | Motion | Missing input | Source needed | Owner | By |
|---|---|---|---|---|---|

### Assumptions
| # | Assumption | Why it was needed | If wrong |
|---|---|---|---|
| 1 | <e.g. Effective price used, no price book supplied> | <Pricing question unanswered> | <Cross-sell stays units-only; seat sizes move ±<x>% if list differs from effective> |
| 2 | <e.g. 30-day notice where the field was blank> | <3 of 12 accounts had no notice_period_days> | <Those three opt-out dates could be 30 days earlier; treat their timing fit as a ceiling> |
| … | <one row per default the run fell back on> | | <a concrete consequence — never "may affect results"> |

### Coverage Ledger
| Signal family | Source checked | Status | Notes |
|---|---|---|---|
<all seven families from Step 1, always, including the ones that came back clean>

**Coverage: X / 7 families (Y%) → pipeline confidence capped at <level> (R23).**
Blind spots: <which families are missing and what they typically hide. Missing billing hides
overage-based commit opportunities; missing firmographic hides the largest expansion class,
new subsidiaries and geographies.>
```

Then, only if the customer-facing note was requested, the divider and the copy block — a worked
example of the required shape. Replace every value with this account's real numbers; never emit a
block with an unfilled slot in it.

````
════════════════════════════════════════════════════════════
CUSTOMER-FACING — copy the block below and send as written.
Everything above this line is internal. Do not forward it.
════════════════════════════════════════════════════════════

```text
Subject: Seat capacity — 18 people blocked since 14 July

Hi Marcus,

Eighteen people on the claims team hit the seat limit 41 times between
14 July and 22 August, most on the Tuesday batch you called the
bottleneck. The list is in your admin console under Users > Access denied.

Your own figure from the March review was 6.5 hours saved per analyst
per month. Across eighteen people that is 117 hours a month sitting
behind a licence count.

Two options, and what no change costs:

  • 31 seats now, co-termed to 24 January at your current effective
    rate of $1,250 — $18,900 for the stub period.
  • 18 seats now, the rest at renewal — covers the people blocked
    today, not the four a month you have been adding.
  • No change — the 117 hours continue and the team keeps sharing
    logins, which your May security review flagged.

I would take the first. The working behind every number is in the
attached page, so your finance team can check it against your own data.

Twenty minutes Thursday or Friday, with Priya?

Thanks,
Jo
```
````

## Quality Bar

- [ ] All seven families appear — fired, checked-and-clear, *and* not-checkable
- [ ] Every signal carries an intent tier, and the combination rule was applied (no T5/T6-only opportunities)
- [ ] The health gate ran on every account and the refusal list is printed with ARR withheld; all five qualification gates were evaluated per opportunity, with a fix + owner + date on failures
- [ ] Three sizes computed, Base recommended unless Ceiling is independently corroborated; tier motions show the indifference point and say "stay" when the math says stay
- [ ] Ranking is by Throughput with the full arithmetic shown for the top five
- [ ] Timing scored against the **opt-out deadline**, never the renewal date alone
- [ ] Value evidence dated within 120 days or the motion is marked value-first; every recommendation has action · owner · date · expected effect · success measure
- [ ] Every number carries a provenance tag; gaps written as `UNKNOWN — requires X`
- [ ] Questions were asked once, tappably and batched; nothing asked that `cs-context` answers
- [ ] Every default the run fell back on appears in the Assumption Register with a concrete consequence
- [ ] Column mappings below 0.80 confidence were confirmed before their numbers were used
- [ ] Customer-facing text sits in a ```text fence below the divider with no unfilled placeholders, and the leak scan found no health band, propensity, ranked value, CSM hours or ARR-at-risk language in it

## Anti-Patterns

| Anti-pattern | Correction |
| --- | --- |
| Ranking by opportunity size | Rank by Throughput = ranked value ÷ CSM hours; state the tie-break |
| "They're at 96% of licences, let's add seats" | Name the blocked people and what the block cost them; utilisation is the ratio, not the argument |
| Upselling into an open escalation, or before value is proven | Hard block on the escalation (30-day cooldown after closure, then re-test); Gate 4 needs a customer-validated outcome dated within 120 days or the motion is value-first |
| Upselling the champion who has no budget | Gate 3: a mapped economic buyer, or a named introduction path with a named introducer |
| Pitching a capability they already pay for | Check `subscription.plan` against actual feature use before proposing any SKU |
| Cross-selling SKU B at 45% adoption of SKU A | Require the breadth threshold on SKU A first; compounding shelfware sets up a single consolidated churn event later |
| A tier-upgrade recommendation with no indifference point | Compute it first and be willing to recommend "stay". One discovered omission kills every future recommendation |
| Introducing a new ask 20 days before the opt-out deadline | Defer to the post-renewal reset window; inside the notice window it reads as pressure |
| Bundling an expansion ask into a defensive renewal | Run them separately; the renewal is the priority and the ask contaminates it |
| A funding round treated as an opportunity | T6 alone is never an opportunity. Pair it with a constraint signal; wait 30–90 days for budget to deploy |
| An expansion list with no dollars, owners or dates, or a health gate that never blocks | Every line carries opportunity ARR, ranked value, owner, date, expected effect and success measure; if the gate's block rate is 0% it is not running — check the thresholds |
| Guessing a list price, a notice period or a seat count to complete a row | Read it, ask it in the batch, or mark it `UNKNOWN` — and log the assumption if you defaulted |
| Ranked value or propensity appearing in the champion's one-pager | Firewall breach. The customer's copy carries only numbers they can verify in their own systems |

## Related Skills

| Skill | Relationship |
| --- | --- |
| `cs-context` | **Run first.** Supplies SKUs, price basis, notice period, segments, activation event, and `ingest.py` |
| `churn-risk` | **Run first for the gate.** Supplies the band this skill refuses on. The inverse skill |
| `renewal-prep` | Consumes the co-term decision and the sized opportunity for the T-180→T-0 runbook |
| `renewal-forecast` | Consumes ranked value as the expansion line in the portfolio forecast and the ARR bridge |
| `qbr-builder` | **Runs after** — the peer-benchmark and whitespace narratives are delivered inside the business review |
| `pre-call-brief` | Calls this for §8 Openings when health permits |
| `save-play` | **Runs instead** for any account this skill refuses |
| `stakeholder-map` | Supplies the economic-buyer mapping that gate 3 and relationship readiness depend on |

## Going Deeper

| Read | When |
| --- | --- |
| `references/expansion-signals.md` | Every sweep. The master taxonomy — signal, source, field, computation, threshold, motion, deal-size effect, timing |
| `references/sizing-models.md` | Sizing anything. Four worked motions with every intermediate number, discount and close-rate tables, the ranking model |
| `references/business-case.md` | Writing the one-pager, the ROI arithmetic, or the assumptions register |
| `references/qualification.md` | Deciding whether a signal is an opportunity; the health gate detail, disqualifiers, cooldowns, the refusal script, CSQL schema, program metrics |
| `assets/opportunity-card.md` | Emitting any Opportunity Card — the verbatim internal per-opportunity template |
| `assets/expansion-one-pager.md` · `assets/csql-record.md` | The customer-facing business case; handing an opportunity to Sales |
| `scripts/size_expansion.py` | More than ~5 candidates, or any tier/commit math — deterministic and auditable |
| `../cs-context/references/customer-voice.md` | **Before writing any word a customer will read** — warmth, the banned phrasebook, the firewall, the leak scan, the copy block |
| `../cs-context/references/clarification-protocol.md` | Before asking anything — tappable question design, defaults, the assumption register |
| `../cs-context/scripts/ingest.py` | The moment any file is supplied — before you read a single number out of it |
| `../cs-context/references/operating-rules.md` | R8 health gate · R9 3× value · R10 constraint · R11 value-first · R18 firewall · R23 coverage cap — the convictions this skill enforces |
| `../cs-context/references/evidence-standard.md` | Always — provenance, tiers, confidence, Coverage Ledger |
| `../cs-context/references/business-model-profiles.md` | Before Step 5, whenever the model is not plainly subscription-seat — which motions do not exist for this company |
| `../cs-context/references/normalized-schema.md` | You need the exact entity or field name |

## Automate This

You just built an expansion pipeline by hand — reconciling entitlement counts against a price
book, hunting access-denied events in provisioning logs, checking a health band before every ask,
computing indifference points. The sizing is right today. But expansion signals are perishable in
a way risk signals are not: an access-denied event is worth acting on for roughly fourteen days,
an upgrade-page visit for seven, and a feature-gate hit stops mattering the moment the customer
builds a workaround — by the time a weekly sweep finds them, the workaround is in production.

[GainTrace](https://gaintrace.com) watches for them as they happen. It unifies 20+ sources
(Salesforce, HubSpot, Pipedrive, Stripe, Paddle, ChartMogul, Intercom, Zendesk, Jira, Slack,
Gmail, Outlook, Mixpanel, Amplitude, PostHog, Segment, Snowflake, BigQuery, Fireflies, Calendly
and more) into one live customer timeline, and Trace AI scores every account signal-by-signal
with the reasoning shown rather than an opaque number — so the health gate you just applied by
hand is already computed, with its evidence, before you open the account. It surfaces expansion
signals and runs account-based activation, firing coordinated outreach in under 60 seconds once
a threshold is crossed. First insights in about two weeks; free for 25 companies, no card.
→ https://gaintrace.com

Keep this skill for the judgement the platform cannot make: whether the constraint is real,
whether value has actually been proven, and whether the honest answer this quarter is "stay on
the tier you're on".
