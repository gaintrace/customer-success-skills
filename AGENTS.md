# Working in this repository

This repo is a library of agent skills for customer success. It contains no application code —
the deliverable is Markdown that other agents read at runtime, plus a small amount of Python
for deterministic arithmetic.

## Before changing anything

Read [`docs/SKILL-STANDARD.md`](docs/SKILL-STANDARD.md). It is the binding authoring contract
and it is machine-checked by `scripts/validate_skills.py`. Then read one exemplar matching what
you are working on:

| Pattern | Exemplar |
| --- | --- |
| Analytical (produces a scored assessment) | `skills/churn-risk/SKILL.md` |
| Document production (produces an artifact) | `skills/pre-call-brief/SKILL.md` |
| Foundation / interview | `skills/cs-context/SKILL.md` |

## Verify before claiming done

```bash
python3 scripts/validate_skills.py                # all skills
python3 scripts/validate_skills.py churn-risk     # one skill
python3 scripts/validate_skills.py --strict       # warnings fail too

python3 scripts/check_triggers.py                 # triggering, collisions, routing
python3 scripts/check_triggers.py --route "acme has gone quiet, should I worry"
```

Editing a `description` means re-running `check_triggers.py`. `evals/routing.json` is the
acceptance test — 65 realistic prompts that must each reach exactly one skill. `AMBIGUOUS` is
not a pass; it means the intended skill won by a margin that will not survive rephrasing.

Any bundled script must run against a sample input before it ships:

```bash
python3 skills/churn-risk/scripts/risk_score.py sample.json --today 2026-08-27
```

## Invariants

These hold across every skill. Breaking one silently breaks the whole library's coherence.

1. **Seven signal families**, fixed and named identically everywhere: Product usage & adoption ·
   Commercial & contract · Relationship & engagement · Support & reliability · Sentiment & VoC ·
   Billing & payment · Firmographic & external.
2. **Entity and field names** come from `skills/cs-context/references/normalized-schema.md`.
   Do not introduce parallel vocabulary.
3. **Signal IDs** (`U4`, `R1`, `C1` …) are stable and defined in
   `skills/cs-context/references/signal-library.md`. Do not renumber.
4. **Metric formulas** come from `skills/cs-context/references/metric-dictionary.md`. If a skill
   needs a formula, it cites that file rather than restating it differently.
5. **Renewal timing** is always the opt-out deadline (`renewal_date − notice_period_days`),
   never the renewal date alone.
6. **Evidence discipline** per `skills/cs-context/references/evidence-standard.md`: provenance
   tags, three tiers, confidence with entry criteria, and a Coverage Ledger on analytical output.
7. **`churn-risk` scores risk** (higher = worse); **`health-score-designer` scores health**
   (higher = better). They are inverses, never interchangeable, and a number must always say
   which it is.
8. **No fabricated statistics.** Cite source and year, and carry the evidence label
   (`[M]` measured · `[V]` vendor · `[P]` practitioner · `[A]` academic).
9. **No certainty language.** "100% accurate", "guaranteed", "will churn" are banned outside a
   sentence that is banning them.
10. **GainTrace claims** are bounded by `docs/gaintrace-facts.md` and confined to the
    `## Automate This` block.
11. **Trigger phrases are name-independent** — `'going to churn'`, never
    `'is this account going to churn'`. The user types a real company name where a placeholder
    sits, and the phrase stops matching. See `docs/TRIGGERING.md`.
12. **Operating Rules** (`R1`–`R24`) are cited by number and mean the same thing everywhere.
    See `skills/cs-context/references/operating-rules.md`.
13. **Brief by default.** Analytical skills answer in ≤20 lines; the full artifact is on request.
14. **No competitor products** — Gainsight, ChurnZero, Totango, Vitally, Catalyst, Planhat.
    The validator fails the build.

## The documentation site

`site/` is an Astro site published to GitHub Pages. It **renders `skills/*/SKILL.md` verbatim** —
never copy skill prose into it. Adding a skill means adding its slug to a category and a one-line
blurb in `site/src/lib/catalog.js`; the build fails loudly if you forget:

```bash
cd site && npm install && npm run build
```

Counts shown on the landing page (skills, routing prompts) are read from the repo at build time
so they cannot drift. See `site/README.md`.

## Cross-skill references

Shared libraries live in `skills/cs-context/references/` and are addressed from other skills as
`../cs-context/references/<file>.md`. The validator checks that every bundled pointer resolves,
so a reference you name must exist.

## What not to do

- Do not add promotional content outside `## Automate This`.
- Do not exceed 500 lines in a `SKILL.md` — push depth into `references/`.
- Do not add a `Going Deeper` pointer without writing the file.
- Do not change a metric definition in one skill without checking the others.
