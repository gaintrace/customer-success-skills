# Relationship Map — rendering spec and template

> The map is emitted as monospaced ASCII inside a fenced block so it renders legibly in a
> terminal, in a CRM note field, in a Markdown file and in a Slack message. No image, no
> Mermaid, no HTML — the map has to survive being pasted into a text box by a CSM in a hurry.

**Contents** — [Legend](#legend) · [Layout rules](#layout-rules) · [Blank template](#blank-template) ·
[Worked example](#worked-example) · [Narrow fallback](#narrow-fallback-under-72-columns) ·
[Roster table](#the-roster-table-that-sits-under-the-map) · [Rules](#rules)

---

## Legend

Print this immediately beneath every map. A map without its legend is decoration.

```text
● verified role   ◐ evidenced role   ○ asserted role   ✗ departed or inactive
▲ blocker/detractor            ⚠ needs action this cycle
[S] signs   [D] decides   [I] influences   — the authority triangle, marked separately (C7)
(sup) supporter — warm, mobilising capacity ≤1, scores 0.0 on the champion slot (C8)
─── confirmed reporting line   ┊┊┊ inferred reporting line
←  our owner for this relationship
infl 1–5 influence (evidence-based)   sent −2…+2 sentiment   mob n/3 mobilising capacity
2-way = days since last two-way interaction   "—" = never   "?" = UNKNOWN, source not connected
```

**The triangle is marked on the map and stated in the header.** A person carrying two marks
prints `CONCENTRATION 2/3`; three marks prints `CONCENTRATION 3/3 — single point of authority`.
A field with nobody holding it prints as a named missing row, never as an absence.

## Layout rules

| Rule | Why |
| --- | --- |
| Four bands, top to bottom: **exec / budget**, **champion / day-to-day**, **operating**, **paper chain** | Reads as a power structure, not an alphabetical list |
| The paper chain sits in its own box, not in the hierarchy | Procurement and legal are process participants, not levels |
| One line per person for identity, one for scores | Two-line cells stay readable at 78 columns |
| Our owner appears to the right of each person, with the date of their last touch | The coverage gap is visible in the same glance as the relationship |
| Confirmed lines `───`, inferred lines `┊┊┊` | The whole credibility of the artifact rests on this distinction |
| Missing roles are printed as a named row, never as an empty box | An absent security reviewer is a finding |
| `[S]` / `[D]` / `[I]` are placed independently, even when they land on one person | The map is the first place a concentration becomes visible (`C7`) |
| A warm contact who fails the mobilising test renders `(sup)`, never `champion` | The champion band must not fill with people who cannot move a decision (`C8`) |
| Every `▲` carries its disposition in the roster — `convert` / `contain` / `bypass` | A detractor drawn without a disposition is decoration (`C11`) |
| Total width ≤ 78 columns | Survives a terminal, a Slack message and a CRM note field |
| Every date is absolute (`2026-08-22`), never relative | "Last month" is unreadable three weeks later |

## Blank template

```text
<ACCOUNT NAME> · $<ARR> ARR · renewal <YYYY-MM-DD> · opt-out <YYYY-MM-DD> (<N>d)
Coverage <n>/4 · depth <n> · breadth <n> · height <band> · champion risk <n>/10
SIGNS <name | UNKNOWN — requires X> · DECIDES <…> · INFLUENCES <…> · <concentration>
Data as-of <YYYY-MM-DD> · map generated <YYYY-MM-DD>

  THEIR SIDE                                              OURS
  ────────────────────────────────────────────────────    ─────────────────────
  ┌─ EXEC / BUDGET ──────────────────────────────────┐
  │ <mark><tri> <name>   <title>        <role>       │ ←  <our owner, title>
  │   infl <n> · mob <n>/3 · sent <n> · 2-way <n>d   │    last touch <date>
  └──────────────────────────┬───────────────────────┘
                             │ <stated | inferred>
  ┌─ CHAMPION / DAY-TO-DAY ──┴───────────────────────┐
  │ <mark><tri> <name>   <title>   <role | (sup)>    │ ←  <our owner, title>
  │   infl <n> · mob <n>/3 · sent <n> · 2-way <n>d   │    last touch <date>
  └──────────────────────────┬───────────────────────┘
                             ┊ <stated | inferred>
  ┌─ OPERATING ──────────────┴───────────────────────┐
  │ <mark><tri> <name>   <title>        <role>       │ ←  <our owner | unowned>
  │   infl <n> · mob <n>/3 · sent <n> · 2-way <n>d   │    last touch <date>
  └──────────────────────────────────────────────────┘

  ┌─ PAPER CHAIN ────────────────────────────────────┐
  │ <mark><tri> <name>   <title>        <role>       │ ←  <our owner | unowned>
  │   <one-line note: when they appear, whether met>  │
  └──────────────────────────────────────────────────┘

  MISSING ROLES: <role> · <role> · <role>
  BLOCKERS: <name> ▲ <convert | contain | bypass> · <name> ▲ <TEST — what to find out, by>
```

## Worked example

```text
NORTHWIND LOGISTICS · $620,000 ARR · renewal 2027-02-05 · opt-out 2026-11-07 (71d)
Coverage 3.0/4 · depth 4 · breadth 2 · height vp · champion risk 2/10
SIGNS Nadia Farouk · DECIDES Dana Osei · INFLUENCES Marcus Bell · no concentration
Exposure ~$17k · closable by multithreading ~$7.1k
Data as-of 2026-08-26 · map generated 2026-08-28

  THEIR SIDE                                              OURS
  ────────────────────────────────────────────────────    ─────────────────────
  ┌─ EXEC / BUDGET ──────────────────────────────────┐
  │ ●[D] Dana Osei       VP RevOps      econ_buyer   │ ←  Priya Raman, VP CS
  │   infl 5 · mob 3/3 · sent ? · 2-way 71d          │    last touch 2026-03-12 ⚠
  │   sentiment last set 2026-01-22 — stale, nulled  │
  └──────────────────────────┬───────────────────────┘
                             │ stated on 2026-01-22 call
  ┌─ CHAMPION / DAY-TO-DAY ──┴───────────────────────┐
  │ ◐[I] Marcus Bell     Dir RevOps     champion     │ ←  Jo Nkemdirim, CSM
  │   infl 4 · mob 2/3 · sent +1 · 2-way 6d          │    last touch 2026-08-22
  │   M1 2025 security exception · M2 cited by two   │
  │   ⚠ delegating since 2026-06 · invite accept 45% │
  └──────────────────────────┬───────────────────────┘
                             ┊ inferred (thread position)
  ┌─ OPERATING ──────────────┴───────────────────────┐
  │ ● Ana Ruiz           RevOps Analyst admin        │ ←  Jo Nkemdirim, CSM
  │   infl 2 · mob 0/3 · sent +1 · 2-way 11d         │    last touch 2026-08-17
  │ ◐▲ Priya Nayar       Dir IT Sec     tech_eval    │ ←  Jo Nkemdirim, CSM
  │   infl 4 · mob 2/3 · sent −1 · 2-way 41d         │    last touch 2026-07-18
  │   ▲ convert · SSO group-sync before go-live      │
  │ ○ Tom Iyer           Mktg Ops Lead  power_user   │ ←  unowned  ⚠
  │   infl 2 · mob  ? · sent ? · 2-way — · asserted  │    never contacted
  └──────────────────────────────────────────────────┘

  ┌─ PAPER CHAIN ────────────────────────────────────┐
  │ ●[S] Nadia Farouk    VP Finance     procurement  │ ←  unowned  ⚠
  │   signed 2026-02-05 order form · notices clause  │    2-way 169d
  │ ○ Rae Lindqvist      Procurement    procurement  │ ←  unowned  ⚠
  │   first appeared 2025-11, 90d before last renewal│    never met
  └──────────────────────────────────────────────────┘

  MISSING ROLES: exec sponsor (theirs) · second champion
  BLOCKERS: Priya Nayar ▲ convert — risk: slow, and a failed convert hardens a
    security veto publicly · Jo Nkemdirim by 2026-09-26
```

**How to read this one.** The champion risk score is 2/10 and the account is still the wrong
shape. Depth 4 and breadth 2 miss the ≥$500k band targets of 7 and 4. The triangle is split
three ways — Nadia signs, Dana decides, Marcus influences — which is the healthy case, and the
reason to check it is that the person who signs has had one interaction in 169 days and nobody
owns her. Marcus earns the champion label on M1 and M2 rather than on warmth, and he is still
showing two of the five leading departure indicators from `../references/champion-risk.md` §2 —
delegation since June and a 45% invite acceptance rate — neither of which the score captures,
which is why the map prints them and the score does not stand alone. Dana is `verified` but has
had no two-way interaction in 71 days and our own VP has not spoken to her since March: a
verified decider with no live executive relationship is the shape that produces a renewal
decided by procurement. Priya Nayar is the only detractor on record; her disposition is
`convert` with the risk written down, because she holds a security veto and `bypass` is not
available against her at any point. Tom Iyer sits in the growing function with nobody owning the
relationship and is the cheapest available breadth. The gap is priced at ~$7.1k closable against
~$17k of exposure — small in absolute terms, and that is the argument for doing it now rather
than at T−30. Composites are reported at two significant figures (`R22`).

## Narrow fallback (under 72 columns)

When the target surface is narrow — a phone, a CRM sidebar, a Slack thread on mobile — drop the
boxes and keep the structure.

```text
NORTHWIND LOGISTICS · $620k · opt-out 2026-11-07 (71d) · coverage 3.0/4
depth 4 · breadth 2 · height vp · champion risk 2/10 · closable ~$7.1k
S Nadia Farouk · D Dana Osei · I Marcus Bell · no concentration

EXEC/BUDGET
  ●[D] Dana Osei · VP RevOps · econ_buyer · mob 3/3 · 2-way 71d ⚠
    ours: Priya Raman (VP CS), last 2026-03-12
  |  stated
CHAMPION
  ◐[I] Marcus Bell · Dir RevOps · mob 2/3 · 2-way 6d · delegating ⚠
    ours: Jo Nkemdirim (CSM), last 2026-08-22
  :  inferred
OPERATING
  ● Ana Ruiz · RevOps Analyst · admin · mob 0/3 · 2-way 11d
  ◐▲ Priya Nayar · Dir IT Sec · tech_eval · convert · 2-way 41d
  ○ Tom Iyer · Mktg Ops Lead · power_user · mob ? · 2-way — · unowned ⚠
PAPER CHAIN
  ●[S] Nadia Farouk · VP Finance · signed 2026-02-05 · 2-way 169d ⚠
  ○ Rae Lindqvist · Procurement · never met ⚠

MISSING: exec sponsor (theirs) · second champion
BLOCKERS: Priya Nayar ▲ convert · Jo by 2026-09-26
```

## The roster table that sits under the map

The map shows structure; the roster carries the evidence. Both are required — the map alone
invites a reader to trust a picture.

```markdown
| # | Name | Title | Role | Tri | Conf. | Infl. | Mob | Sent. | Last 2-way | Depth 180d | Strength | Our coverage | Evidence for the role · M-tests fired · disposition |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Marcus Bell | Dir RevOps | champion | [I] | evidenced | 4 | 2/3 | +1 | 6d | 14 | 86.2 | Jo Nkemdirim · current | Presented our Q1 results to his leadership 2026-02-18 without us in the room · M1 (2025 security exception, 3 weeks), M2 (cited by two colleagues) |
| 2 | Ana Ruiz | RevOps Analyst | admin | — | verified | 2 | 0/3 | +1 | 11d | 9 | 71.2 | Jo Nkemdirim · current | Holds the admin role; provisioned 34 seats in 2026 |
| 3 | Dana Osei | VP RevOps | economic_buyer | [D] | verified | 5 | 3/3 | ? | 71d | 2 | 70.0 | Priya Raman · stale | Confirmed budget ownership on the 2026-01-22 call · M1, M2, M3 |
| 4 | Priya Nayar ▲ | Dir IT Security | technical_evaluator | — | evidenced | 4 | 2/3 | −1 | 41d | 3 | 57.5 | Jo Nkemdirim · current | Requested SOC 2 and the pen-test report 2026-06-02 · **convert** — risk: slow, and a failed convert hardens a security veto publicly · Jo by 2026-09-26 |
| 5 | Nadia Farouk | VP Finance | procurement | [S] | verified | 3 | 1/3 | ? | 169d | 1 | 35.0 | unowned | Signed the 2026-02-05 order form; named in the MSA notices clause |
| 6 | Rae Lindqvist | Procurement Mgr | procurement | — | asserted | 3 | ? | ? | — | 0 | 20.0 | unowned | On the 2025 renewal paper thread only |
| 7 | Tom Iyer | Mktg Ops Lead | power_user | — | asserted | 2 | ? | ? | — | 0 | 10.0 | unowned | Top-decile core actions; no interaction on record |

Reproduce every figure in that table with
`python3 ../scripts/stakeholder_score.py ../scripts/sample-account.json --today 2026-08-28 --explain NORTHWIND`.
Dana's sentiment renders `?` rather than `0` because it was last set on 2026-01-22 and is past
the 90-day staleness rule; her strength is renormalised over the three dimensions with data.
Rae and Tom show `mob ?` because no M-test has been run on them — untested is UNKNOWN, and an
untested contact can never be promoted to champion (`C8`).
```

**The triangle here is split three ways** — Nadia signs, Dana decides, Marcus influences — which
is the healthy case. Compare `--explain DELTA`, where `signs` is unknown 19 days from the opt-out
deadline: coverage is capped at 2/4, the champion slot scores 0.0 because Sam Okafor is a
supporter, and the procurement `bypass` is refused because he holds a veto.

## Rules

- **No unfilled slot ever leaves the skill.** Every `<...>` in the blank template is replaced
  or the row is removed and the gap is stated as `UNKNOWN — requires <source>`.
- **The map is internal.** It contains role assessments, influence scores, sentiment and our
  own coverage failures. None of it goes to the customer in any form. A sanitised version
  showing only names, titles and our owner may be shared to confirm structure — nothing else.
- **Dates, not durations, in the header.** `2-way 71d` inside a cell is fine because the header
  carries the generation date; a map pasted somewhere without its header becomes unreadable.
- **Sentiment older than 90 days renders as `?`**, not as its last value.
- **Marks are earned.** `●` means the customer said it out loud or the person did the thing.
  Promoting an `○` to a `●` because the map looks better is the failure this notation exists
  to prevent.
