# QBR / EBR Deck Architecture

> The slide-by-slide specification. Read it whenever you build or rebuild a business-review
> deck. Every slide here has one job; a slide that cannot state its job is cut.

**Contents**
1. [The three altitudes](#1-the-three-altitudes)
2. [The 45-minute executive review — full specification](#2-the-45-minute-executive-review--full-specification)
3. [Slide detail and headline patterns](#3-slide-detail-and-headline-patterns)
4. [Variants: 60-minute QBR, 90-minute onsite EBR, 15-minute cut, async value review](#4-variants)
5. [Chart and table rules](#5-chart-and-table-rules)
6. [What must never appear](#6-what-must-never-appear)
7. [The appendix](#7-the-appendix)
8. [Build order and the pre-flight check](#8-build-order-and-the-pre-flight-check)
9. [Source register](#9-source-register)

---

## 1. The three altitudes

| | **EBR** | **QBR** | **Value review** |
| --- | --- | --- | --- |
| Room | Economic buyer + peers; our exec sponsor | Objective owners, admins, champion | Champion, often async |
| Cadence | 1–2× per year, timed to the opt-out deadline and their budget cycle | Quarterly for named-CSM segments | Monthly or off-quarter |
| Length · slides | 45 min · 8–10 | 45–60 min · 10–12 | 15 min or async · 1 |
| Unit of discussion | Their business outcome, in P&L units | Their workstream, in operational units | One outcome vs baseline vs target |
| Who carries the value case | Our exec sponsor, champion co-presenting | CSM | CSM |
| Product content | Only where a named gap blocks a named objective | Named workflows, still tied to objectives | None |
| The close | Renewal-intent question, asked aloud, logged verbatim | Three dated goals with named owners | One next step with a date |
| Success test | The buyer says something they can be held to | Every goal has a customer-side owner | The champion forwards it unedited |
| Failure test | Altitude drifts into feature detail by slide 4 | It becomes a status report | It becomes a newsletter |

This split is a **convention this library adopts**, not a measured finding: EBRs are
senior-leadership, strategic and annual-to-biannual; QBRs are operational, tactical and
quarterly. Use it because it makes the altitude decision explicit, not because a study
established it. The one-page value review is the alternative for everything else, structured
as **expected value → value delivered → proof of value → next steps**, with proof written as
*baseline → current → target* (framework by Angeline Gavino, *CS RevSpeak*, 13 Feb 2026 —
practitioner `[P]`).

**The altitude test.** Read each slide's headline aloud. If it can only be understood by
someone who knows our product's nouns, it is a QBR slide at best and an appendix slide more
likely. An EBR slide's headline works for a CFO who has never logged in.

---

## 2. The 45-minute executive review — full specification

Presented minutes total 21 of 45. The remaining 24 are discussion, and that ratio is the
point. The failure mode of the data-dense deck is a room that stays polite and disengaged,
and a meeting that ends with no decision, no commitment and nothing different afterwards. A
review where we talk for 40 of the 45 minutes has failed regardless of what was on the
slides.

| # | Slide | Min (present · discuss) | Purpose | Required content | Data source (entity · field) | The "so what" it must answer | Failure mode |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Purpose, agenda, and the decision | 2 · 0 | Buy the next 43 minutes | The one decision we are asking for, the four sections, the timings, who presents what | The internal plan; `opportunity.type`, `subscription.opt_out_deadline` | Why is this worth 45 minutes of my day? | An agenda with no decision named — the room disengages in slide 1 |
| 2 | Your objectives, in your words | 1 · 2 | Prove we know what they are trying to do | 3–4 objectives, quoted, each with its source and date and the metric it is measured by | Their business case, success plan, earnings call, transcripts; `interaction.summary` | Do these people understand my problem? | Objectives we wrote. The room does not recognise them and nothing after this recovers |
| 3 | Progress against them | 3 · 5 | Show movement, honestly | One row per objective: baseline → current → target → status → owner. Include the one that went backwards | Customer-supplied baseline; `usage_daily`, their own systems | Am I further along than I was? | A metric with no baseline; or every row green, which nobody believes |
| 4 | **What fell short** | 2 · 3 | Bank trust before anything is claimed | Our misses first, then theirs, then external. Each with what it cost them in their units | `ticket` (P1, `sla_breached`, `reopened_count`), `invoice.status`, the commitment log | Are these people straight with me? | A miss they raise before we do; a miss with no owner and no date; an empty slide on a quarter that missed a milestone |
| 5 | What we are changing | 2 · 1 | Convert the miss into a commitment | 2–3 commitments, each with owner, date, expected effect and how they will know | The internal plan | Will next quarter actually be different? | "We are improving our processes" — a commitment with no observable |
| 6 | **Value delivered: one number** | 4 · 4 | Give them the number they will repeat internally | **One** headline figure, its band, the benefit lines with `Agreed?` and Customer-stated, the assumption register, what was excluded | `../references/value-realization.md`; `../scripts/value_case.py` | What did we get for the money? | A metrics wall; a number with hidden inputs; a figure nobody on their side has said |
| 7 | Adoption evidence, by team | 2 · 3 | Make the value claim checkable | Active users and core actions **split by team**, including the buyer's team; breadth vs plan; entitlement position | `usage_daily.active_users`, `core_actions`, `feature_breadth`; `subscription.seats_purchased` | Is that number real, or an artifact? | Aggregate usage that hides a dead buying team; vanity metrics |
| 8 | Roadmap relevant to their objectives | 2 · 2 | Show our direction is their direction | Only items that move an objective from slide 2. Real dates, or the words "no date" | Product roadmap, filtered | Is where you are going where I need to go? | The full roadmap. Dates we cannot hold. Items nobody in the room asked for |
| 9 | Next-period goals, co-owned | 2 · 3 | Get shared, dated ownership | Three SMART goals: baseline, target, both owners, date, measurement source, dependency | `../references/smart-goals.md` | What are we both signing up for? | Goals with only our name on them; more than three |
| 10 | Asks, commitments both ways, the date | 1 · 1 | Close | What we commit to, what we are asking for, the next meeting date agreed in the room | Parts C and D of the output template | What happens on Monday? | An implied ask; "I'll follow up" instead of a date |

**Section timing at a glance:** context and objectives 0:00–0:05 · progress 0:05–0:13 · honesty and
change 0:13–0:21 · value 0:21–0:29 · evidence 0:29–0:34 · forward plan 0:34–0:43 · close 0:43–0:45.

**The order is load-bearing, not stylistic (C29, R20).** The shortfall slide is generated first and
sits before the value slide. Opening on good news after a bad quarter tells the customer you did not
notice; hearing the miss from us first makes everything after it credible. **Refusal condition:**
compute `milestones_missed` from the success plan — where it is ≥ 1 and slide 4 is empty, the deck
is not emitted.

**Stop-and-ask points.** Build one explicit question into slides 2, 3, 4, 6 and 9. Silence at a
stop-and-ask point is data: it usually means the slide is not about them.

| Slide | The question to ask out loud |
| --- | --- |
| 2 | "Is this still the right list, and is the ranking right?" |
| 3 | "Which of these is furthest from where you wanted it?" |
| 4 | "What have we missed that has cost you time this quarter?" |
| 6 | "Would your finance team accept these inputs? Which one would they challenge?" |
| 9 | "Which of these three will you not be able to resource?" |

---

## 3. Slide detail and headline patterns

**Every headline is an assertion, not a topic.** "Q3 Usage" is a topic. "Finance is now the
heaviest user of the platform — and that is where your close-cycle gain came from" is an
assertion. The topic version makes the audience do the analysis; the assertion version puts our
conclusion on the record where they can disagree with it.

| Slide | Topic headline (wrong) | Assertion headline (right) |
| --- | --- | --- |
| 2 | "Your 2026 Objectives" | "Three objectives, unchanged since January — close cycle, audit readiness, headcount leverage" |
| 3 | "Progress Update" | "Two of three objectives moved; audit readiness did not, and we own why" |
| 4 | "Challenges" | "We missed the September integration date by 6 weeks and it cost your team ~120 hours" |
| 5 | "Our Commitments" | "Three changes, each with a named owner and a date inside this quarter" |
| 6 | "ROI Summary" | "Three and a half days out of your close — the number Jamie put on it on 14 August" |
| 7 | "Adoption Metrics" | "Finance went from 4 to 22 weekly users; Legal has not started" |
| 8 | "Product Roadmap" | "Two shipping items move your audit-readiness objective; nothing else on our roadmap does" |
| 9 | "Next Quarter" | "Three goals, each with an owner on your side and a date" |
| 10 | "Next Steps" | "We are asking for one introduction and one decision, both by 15 October" |

**Slide 3 construction.** One table, one row per objective, five columns: objective · baseline
(value, date, who supplied it) · current (value, date, source) · target · status. Status is one
of `ahead` / `on track` / `behind` / `blocked` / `not started`, never a colour alone. **Include
the objective that went backwards.** A slide where every row is green reads as a slide that was
edited, not measured.

**Slide 4 construction.** Order is fixed: **our misses → their blockers → external factors.**
Reversing it, or opening with theirs, reads as blame-shifting even when it is accurate. Each row:
what happened · what it cost them, in their units · why · what we already changed. Cap at three
rows; more than three and this is an escalation review, not a business review. This slide is built
before slide 6 and carries no commercial ask (**R11**).

**Slide 6 construction.** One headline figure at the top, the benefit lines beneath it, the
assumption register in the same visual field — not an appendix — and one line naming what was
excluded. Three constraints decide whether the slide is valid:

| Constraint | Rule | Invalid |
| --- | --- | --- |
| **One number (C19)** | Exactly one headline figure; every supporting metric moves to the appendix | A metrics wall, which starts a debate about which metric counts instead of a decision |
| **Agreed above retrospective (C18)** | Every line carries `Agreed?`; a baseline not agreed before the period started is tagged `retrospective — weaker evidence` and ordered below every agreed line | A retrospective line above an agreed one, or an empty `Agreed?` cell |
| **Customer-stated leads (C5)** | Every line carries the quote, speaker and date, or the tag `vendor-asserted`; vendor-asserted lines never lead | A figure we assert, at the top of the slide, that nobody on their side has said |

Where no customer-stated line exists, the slide carries the unit metric, no dollar figure, and the
ask for who can put a number on it and by when. If the band is `Not presentable`, the same applies.
Never a dollar figure without a customer-agreed baseline.

**Slide 9 construction.** Three goals, no more. Each goal is one row of the Part C table. If a
goal's dependency sits on their side, the dependency is stated on the slide with its own date —
a goal whose dependency is invisible fails silently and is then argued about next quarter.

---

## 4. Variants

### 4.1 The 60-minute QBR (operational room)

Insert after slide 5, keep everything else:

| Extra slide | Min | Content | So what |
| --- | --- | --- | --- |
| 5b — Workstream status | 4 | Each active workstream: owner, state, next milestone, blocker | Where does my team's work actually stand? |
| 5c — Support and reliability detail | 4 | Ticket volume by type, FRT/TTR against target, top three recurring issues with fixes | Is using this getting easier or harder? |
| 8b — Enablement and onboarding | 4 | New users onboarded, sessions run, upcoming training, unonboarded teams named | Who on my side is still not equipped? |

### 4.2 The 90-minute onsite EBR

Do not lengthen slides; add working time. Structure: 45-minute deck as specified · 20-minute
working session on the hardest objective (whiteboard, no slides) · 15-minute roadmap and
direction discussion led by their questions · 10-minute close and commitments. The working
session is the reason to be in the room; if it is not on the agenda, run it remotely instead
and save both sides the travel.

### 4.3 The 15-minute cut

Decide this before the meeting, in the internal plan. Cutting live, CSMs drop the ask and keep
the evidence, which is exactly backwards.

| Min | Keep | Why it survives |
| --- | --- | --- |
| 0–1 | Slide 2, objectives | Establishes we are not here to demo |
| 1–4 | Slide 4, condensed to the one miss and its commitment | It goes first even in the cut (**C29**) |
| 4–8 | Slides 3 + 6 merged: progress and the one number with its assumptions | This is the meeting |
| 8–12 | Slide 9, three goals | The forward ask |
| 12–15 | Slide 10, the ask and the date | The close |

Dropped and sent: agenda, adoption detail, roadmap, the "what we are changing" detail beyond the
single commitment. Say what you are dropping and when it will arrive — an unannounced cut looks
like unpreparedness.

### 4.4 The async one-page value review

Four blocks, one page, no attachments:

| Block | Content | The sentence pattern |
| --- | --- | --- |
| Expected value | The outcome they said they wanted, with its date and business reason | "You wanted to <outcome> by <date> so you could <business reason>" |
| Value delivered | Movement in their units, not our adoption metrics | "<metric> moved from <baseline> to <current> against a target of <target>" |
| Proof of value | Baseline → current → target, with the source of each | "Measured in <their system>, baseline supplied by <name> on <date>" |
| Next steps | The risk, the ask, and a focused 90-day plan with owners and dates | "One ask: <ask>, from <name>, by <date>" |

(Structure after the one-page value review framework, Angeline Gavino, *CS RevSpeak*,
Feb 2026 — practitioner `[P]`.)

---

## 5. Chart and table rules

| Rule | Why |
| --- | --- |
| One chart per slide, maximum | Two charts means the slide has two jobs |
| Every axis labelled with its unit and window | An unlabelled trend line is decoration |
| Baseline drawn as a reference line, not implied | The baseline *is* the argument |
| Split by team wherever the buyer's team exists as a segment | Aggregate usage is the single commonest false-green in a value story |
| No dual-axis charts | They can be made to show anything, and finance readers know it |
| No index-to-100 charts in an EBR | It hides the absolute number, which is what a CFO wants |
| Tables beat charts for anything with more than two dimensions | Scannable, comparable, and it forces completeness |
| Provenance under every figure: `[system · field · window]` | The caveat has to travel with the number |
| Round to the precision you can defend | "$412,000" invites a challenge that "$410K" does not |

---

## 6. What must never appear

| Never | Why | Instead |
| --- | --- | --- |
| A feature tour | Nobody in the room bought features | Name a feature only where it closes a stated objective gap |
| Our roadmap as the main content | It is our plan, not their outcome | ≤1 slide, filtered to their objectives, real dates or "no date" |
| Vanity usage metrics — logins, page views, sessions, total events | No budget was ever defended with a login count | Metrics tied to a slide-2 objective, split by team |
| A health score | An internal construct; it starts an argument about our model instead of their outcomes | The observable underneath it |
| Internal risk language — "at risk", "save play", "ARR at risk", "churn", "red account" | Leaked risk language has ended renewals | It does not exist in customer-facing material at any altitude |
| 40 slides | Attention is the constraint, not information | 10 slides plus an appendix nobody has to open |
| A number the champion has not already seen | Surprises get contested in the room instead of accepted | The pre-call |
| Our org chart, our funding news, our company update | Not their outcome | Omit; put it in the follow-up email if it matters |
| Screenshots of our UI | They have the UI | Only where a screenshot evidences a specific claim |
| An NPS or CSAT score presented as account sentiment | It is one person's score, and it decays past 90 days | Quote the person, with the date |
| A pricing, uplift, or upsell slide inside the value section | It converts the value case into a pretext | A separate meeting, or the last five minutes with explicit permission |
| A second headline number in the value slot | Two numbers means the room argues about which one counts | One number, chosen with them; the rest in the appendix (**C19**) |
| A benefit line with no customer-stated form, leading the slide | A figure we assert is a vendor claim; the same figure in their words is internal evidence | The quote, the speaker and the date beside the number; otherwise the line is `vendor-asserted` and cannot lead (**C5**) |
| A retrospective benefit presented as the plan | Numbers chosen after the fact look chosen | Tag it `retrospective — weaker evidence`, order it below agreed lines, and agree next period's baselines now (**C18**) |
| Our deck forwarded to the champion as their internal case | It reads as vendor material in a room we are not in | The champion's one-pager, in their voice (**C17**, `../assets/champion-onepager.md`) |
| A decision presented for the first time in the room | Unwired decisions get debated, not ratified | A pre-wire status per person per decision; unwired items are pre-wired or dropped (**C9**) |
| "Thank you for your partnership" as slide 1 or slide 10 | It occupies the two highest-attention slots with nothing | Slide 1 is the decision; slide 10 is the ask |
| A slide with no owner for its follow-up | Every forward-looking claim needs a person | Owner and date on the slide itself |

---

## 7. The appendix

The appendix exists so that the main deck can be short, not so that the deck can be long. Rules:

- Nothing in the appendix is presented. If you plan to present it, it is not appendix material.
- Appendix slides carry the same provenance standard as main slides — they get forwarded too.
- Standard contents: full ticket and escalation log for the period · full usage detail by team
  and feature · the complete value-case working with every assumption · prior-period goals and
  their outcomes · glossary of any metric on slide 3 · the change log for anything we shipped
  that affects them.
- Prior-period goals belong in the appendix **and** on slide 3 as the status column. Burying
  last quarter's unmet goals only in the appendix is the most-noticed omission in a QBR.

---

## 8. Build order and the pre-flight check

Build in this order. Building slide 1 first produces a deck about us.

`objectives (2) → shortfall (4) → changes (5) → value (6) → progress (3) → evidence (7) → goals (9)
→ roadmap filter (8) → close (10) → agenda (1) → appendix`

The shortfall is built **before** the value section, not merely placed before it. Building the value
case first produces a shortfall slide written to survive alongside it.

**Pre-flight, before the pre-read goes out:**

- [ ] Every slide headline is an assertion that survives being read alone
- [ ] Every objective on slide 2 is quoted, sourced and dated
- [ ] Slide 3 contains at least one row that did not go well
- [ ] Slide 4 opens with our miss, not theirs, and is populated wherever a milestone was missed
- [ ] Slide 6 carries exactly one headline number, with the register and exclusions beside it
- [ ] Every benefit line carries `Agreed?` and Customer-stated; no vendor-asserted line leads
- [ ] Slide 7 splits by team, and the buyer's team is named
- [ ] Slide 8 contains no roadmap item that does not move a slide-2 objective
- [ ] Slide 9 has exactly three goals, each with a customer-side owner
- [ ] Slide 10 states the ask in one sentence and proposes a date
- [ ] Presented minutes ≤ half the meeting length
- [ ] No item from §6 appears anywhere, appendix included
- [ ] Every figure carries `[system · field · window]`
- [ ] The champion has seen slides 2, 6 and 9 and supplied the quote behind the headline number
- [ ] The champion's internal one-pager is written, with a populated credit slot (**C17**, **C20**)

---

## 9. Source register

| Source | Supplies | Type |
| --- | --- | --- |
| Angeline Gavino (*CS RevSpeak*), *Ditch your 30-slide deck* (13 Feb 2026) | The one-page value review structure; *baseline → current → target* as the proof pattern | Practitioner `[P]` |
| CSM Practice, *QBR mistakes to avoid* (retrieved as a secondary citation; primary not verified) | Agenda discipline, planning with the champion, two-way engagement, "call for a decision", follow-up | Practitioner `[P]` |
| Lincoln Murphy, *A QBR is NOT Required for Customer Success* (sixteenventures.com) | The qualification default; Desired Outcome = Required Outcome + Appropriate Experience | Practitioner `[P]` |
| G.T. Doran, *Management Review* 70(11), 1981, pp. 35–36 | SMART, and the original **A = Assignable** | Primary `[S]` |
| This library's own convention | The EBR / QBR / value-review altitude split; the 21-of-45 presented-minutes budget; the ten-slide architecture | Convention, not a finding |
| `../../../docs/SKILL-STANDARD.md` §5 | Output standards: BLUF, tables over prose, owner/date on every recommendation, dollars | Library standard |

**Not verified, do not cite as measured:** the McKinsey "2.5× more likely to renew with
strong executive engagement" figure, the Salesforce 87% "trusted advisor" figure and the
Oracle 72% "information overload delays decisions" figure. All three reach this library only
as secondary citations inside marketing material; the primary sources were not retrievable.
Separately, the widely repeated claim that holding regular business reviews roughly doubles
renewal likelihood has been **removed from this skill**: no retrievable primary study
supports it, and the comparison is confounded in both directions — healthy accounts accept
reviews and unhealthy ones decline them.
