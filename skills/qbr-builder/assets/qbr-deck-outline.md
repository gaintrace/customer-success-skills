# QBR / EBR Deck Skeleton — copy and fill

> Internal working document. Every `<...>` placeholder and every `<!-- comment -->` is
> deleted before the deck is built. Full slide-by-slide specification, variants and the
> pre-flight check: `../references/deck-architecture.md`.
>
> Build order is **not** slide order. Build: objectives (2) → **shortfall (4)** → changes (5) →
> value (6) → progress (3) → evidence (7) → goals (9) → roadmap filter (8) → close (10) →
> agenda (1) → appendix. Building slide 1 first produces a deck about us.
>
> **The shortfall slide is built before the value slide and sits before it in the deck (C29,
> R20), and where any success-plan milestone was missed the deck is not emitted without it.**

**Account:** `<name>` · **Type:** `<EBR | QBR | value review>` · **Date:** `<date, duration>`
**Presenter(s):** `<who presents which section>` · **As-of date for all data:** `<date>`
**The one decision this meeting must produce:** `<decision, and the date it is needed by>`
**Pre-wire status:** `<n>/<m>` positions WIRED · unwired items are pre-wired by `<date>` or dropped
**Milestones missed this period:** `<n>` — slide 4 is required and populated when this is ≥ 1

Every headline below is an **assertion**, not a topic. If the headline survives being read
alone, out of the deck, it is a headline. If it needs the slide to make sense, rewrite it.

---

## Slide 1 — Purpose, agenda, and the decision

- **Headline:** `<the decision we are asking for, in one sentence>`
- **On the slide:** the decision · the four sections with timings · who presents what
- **Source:** the internal plan; `subscription.opt_out_deadline`
- **Present · discuss:** 2 · 0
- **Speaker note:** *"We're here to agree `<three things>` and to get your answer on
  `<the decision>`. I'll take twenty minutes; the rest is yours. Stop me anywhere."*
- **Hand-over:** straight into slide 2. No thank-you slide, no company update.

## Slide 2 — Your objectives, in your words

- **Headline:** `<e.g. "Three objectives, unchanged since January — close cycle, audit readiness, headcount leverage">`
- **On the slide:** 3–4 objectives, **quoted**, each with source, date stated, the metric,
  their owner, and the baseline
- **Source:** their business case, success plan, earnings call, transcript `interaction.summary`
- **Present · discuss:** 1 · 2
- **Stop-and-ask:** *"Is this still the right list, and is the ranking right?"*
- **Hard rule:** nothing on this slide that the customer has not said. Anything inferred was
  confirmed by the champion in the pre-call and is now theirs.

| # | Objective (their words) | Source · date | Metric | Their owner | Baseline |
|---|---|---|---|---|---|
| 1 | `<quote>` | `<doc/call · date>` | `<metric>` | `<name>` | `<value · date · who supplied it>` |

## Slide 3 — Progress against them

- **Headline:** `<e.g. "Two of three objectives moved; audit readiness did not, and we own why">`
- **On the slide:** one row per objective — baseline → current → target → status → owner.
  **Include the one that went backwards.** Prior-period goals appear here as the status column
- **Status values:** `ahead` / `on track` / `behind` / `blocked` / `not started` — never a colour alone
- **Present · discuss:** 3 · 5
- **Stop-and-ask:** *"Which of these is furthest from where you wanted it?"*

| Objective | Baseline (value · date · supplied by) | Current (value · date · source) | Target | Status | Owner |
|---|---|---|---|---|---|

## Slide 4 — What fell short

- **Headline:** `<e.g. "We missed the September integration date by 6 weeks and it cost your team ~120 hours">`
- **Order is fixed:** our misses → their blockers → external factors
- **Each row:** what happened · what it cost them, in their units · why · what we already changed
- **Source:** `ticket` (P1, `sla_breached`, `reopened_count`), `invoice.status`, the commitment log
- **Present · discuss:** 2 · 3
- **Stop-and-ask:** *"What have we missed that has cost you time this quarter?"*
- **Cap: three rows.** More than three and this is an escalation review — say so and re-book.
- **Required:** where any success-plan milestone was missed this slide must be populated, and
  it is built before slide 6. No commercial ask appears on it or after it in the same breath (**R11**).

## Slide 5 — What we are changing

- **Headline:** `<e.g. "Three changes, each with a named owner and a date inside this quarter">`
- **On the slide:** 2–3 commitments, each with owner, date, expected effect, and how they will know
- **Present · discuss:** 2 · 1
- **Never:** "we are improving our processes" — a commitment with no observable

## Slide 6 — Value delivered: one number

- **Headline:** `<the figure in their unit first, the dollar second — e.g. "3.5 days out of the close, worth ~$265K on your team's own loaded rate">`
- **On the slide:** **exactly one headline number** · its band · the benefit lines with their
  `Agreed?` and **Customer-stated** columns · **the assumption register in the same visual
  field** · one line naming what was excluded
- **Source:** `../references/value-realization.md`; `../scripts/value_case.py`
- **Present · discuss:** 4 · 4
- **Stop-and-ask:** *"Would your finance team accept these inputs? Which one would they challenge?"*
- **One number, not twelve (C19).** Every supporting metric moves to the appendix. A metrics
  wall here invites a debate about which metric counts instead of a decision.
- **Agreed above retrospective (C18).** A benefit whose baseline was not agreed before the
  period started is tagged `retrospective — weaker evidence` and ordered below every agreed line.
- **Customer-stated leads (C5).** The headline figure carries the quote, the speaker and the
  date. A line with no customer-stated form is `vendor-asserted` and may not lead the slide;
  where no customer-stated line exists, the slide carries the unit metric and the ask for the
  number instead.
- **If the band is Not presentable:** no dollar figure. Unit metrics, plus an explicit ask for
  the baseline and who can supply it.
- **Have ready, unasked:** the downside number. *"At α = 0.5 rather than 0.7 this is `<X>`."*

## Slide 7 — Adoption evidence, by team

- **Headline:** `<e.g. "Finance went from 4 to 22 weekly users; Legal has not started">`
- **On the slide:** active users and core actions **split by team, including the buyer's team**;
  breadth against plan; entitlement position (seats used vs purchased)
- **Source:** `usage_daily.active_users`, `core_actions`, `feature_breadth`, `subscription.seats_purchased`
- **Present · discuss:** 2 · 3
- **Never:** aggregate usage that hides a dead buying team; logins, page views, total events

## Slide 8 — Roadmap relevant to their objectives only

- **Headline:** `<e.g. "Two shipping items move your audit-readiness objective; nothing else on our roadmap does">`
- **On the slide:** only items that move a slide-2 objective. Real dates, or the words "no date"
- **Present · discuss:** 2 · 2
- **Never:** the full roadmap; dates we do not own; items nobody in the room asked for

## Slide 9 — Next-period goals, co-owned

- **Headline:** `<e.g. "Three goals, each with an owner on your side and a date">`
- **On the slide:** exactly three SMART goals — baseline, target, both owners, date,
  measurement source, dependency (with **its own** owner and date)
- **Source:** `../references/smart-goals.md`
- **Present · discuss:** 2 · 3
- **Stop-and-ask:** *"Which of these three will you not be able to resource?"*

| # | Goal | Baseline → target | By | Owner — you | Owner — us | Measured in | Dependency |
|---|---|---|---|---|---|---|---|

## Slide 10 — Asks, commitments both ways, and the date

- **Headline:** `<e.g. "We're asking for one introduction and one decision, both by 15 October">`
- **On the slide:** what we commit to · what we are asking for · the next meeting date
- **Present · discuss:** 1 · 1
- **The close:** read back → assign by name → date it, before anyone leaves
- **EBR only:** ask the renewal-intent question against the **opt-out deadline** and log the
  answer verbatim: *"Is there anything you can see between now and `<opt-out date>` that
  would stop this continuing?"*
- **Never:** a thank-you slide in this slot; an implied ask; "I'll follow up" instead of a date

---

## Appendix — nothing here is presented

Full ticket and escalation log · full usage detail by team and feature · the complete
value-case working with every assumption · prior-period goals and their outcomes · glossary
for any metric on slide 3 · change log for anything we shipped that affects them.

Appendix slides carry the same provenance standard as main slides. They get forwarded too.

---

## Pre-flight — tick before the pre-read goes out

- [ ] Every headline is an assertion that survives being read alone
- [ ] Every objective on slide 2 is quoted, sourced and dated
- [ ] Slide 3 contains at least one row that did not go well
- [ ] Slide 4 (shortfall) opens with our miss, not theirs, and is populated wherever a
      success-plan milestone was missed — the deck is not emitted otherwise (**C29**)
- [ ] Slide 6 carries **exactly one** headline number, with its assumption register and
      exclusions in the same visual field (**C19**)
- [ ] Every benefit line on slide 6 carries `Agreed?` and **Customer-stated**; retrospective
      lines sit below agreed ones and no vendor-asserted line leads (**C18**, **C5**)
- [ ] Slide 7 splits by team, and the buyer's team is named
- [ ] Slide 8 contains no roadmap item that does not move a slide-2 objective
- [ ] Slide 9 has exactly three goals, each with a customer-side owner
- [ ] Slide 10 states the ask in one sentence and proposes a date
- [ ] Presented minutes ≤ half the meeting length
- [ ] No health score, no risk language, no feature tour, no vanity metric — appendix included
- [ ] Every figure carries `[system · field · window]` and a shared as-of date
- [ ] The champion has seen slides 2, 6 and 9, and supplied the quote behind the headline number
- [ ] The champion's internal one-pager (Part F) is written and ready to send — a distinct
      document in their voice with a populated credit slot (`champion-onepager.md`)
- [ ] Every `<placeholder>` and every `<!-- comment -->` has been deleted
