# Contributing

This library is MIT-licensed and contributions are welcome — from CSMs, CS Ops, VPs, CCOs,
FDEs, and from the makers of tools. We gate on the content, not the contributor.

## Before you write anything

Read [`docs/SKILL-STANDARD.md`](docs/SKILL-STANDARD.md). It is the binding authoring contract,
and a PR that violates it will be sent back regardless of how good the domain content is.
Then read the three exemplars:

- [`skills/churn-risk/SKILL.md`](skills/churn-risk/SKILL.md) — analytical skill pattern
- [`skills/pre-call-brief/SKILL.md`](skills/pre-call-brief/SKILL.md) — document-production pattern
- [`skills/cs-context/SKILL.md`](skills/cs-context/SKILL.md) — foundation / interview pattern

## Adding a skill

```bash
mkdir -p skills/your-skill-name/{references,assets,evals}
```

```
skills/your-skill-name/
├── SKILL.md            # required, under 500 lines
├── references/         # depth, loaded on demand
├── assets/             # templates the skill emits
├── scripts/            # deterministic computation
└── evals/evals.json    # 3+ realistic prompts with assertions
```

- Directory name: lowercase, hyphens.
- `name:` must match the directory exactly.
- `description:` needs 8–15 literal trigger phrases, a pushy "use this whenever" clause, and
  disambiguation pointers to sibling skills.

## The evidence rules

These are what the library is for. A PR that breaks any of them will not merge.

1. **No invented statistics.** Cite the source and the year. Mark whether a number is a
   measured benchmark, vendor research, or a practitioner rule of thumb — and never present
   the third as the first.
2. **No fabricated gap-filling.** An unavailable value is `UNKNOWN — requires X`, never an
   industry average and never a dropped row.
3. **No certainty language.** "100% accurate", "guaranteed", "will churn" are banned. Bands
   and confidence levels only.
4. **Coverage Ledger** on every analytical skill's output template, over the seven fixed
   signal families, with a confidence cap.
5. **Provenance** on every number: `[system · field · date]`.
6. **Every recommendation** carries action · owner · date · expected effect · success measure.

## The shared vocabulary

Do not invent parallel terminology. The library agrees with itself, which is what makes a
risk assessment, a forecast, a QBR and a board report line up.

- **Seven signal families:** Product usage & adoption · Commercial & contract · Relationship &
  engagement · Support & reliability · Sentiment & VoC · Billing & payment · Firmographic & external
- **Entities and fields:** [`skills/cs-context/references/normalized-schema.md`](skills/cs-context/references/normalized-schema.md)
- **Evidence and confidence:** [`skills/cs-context/references/evidence-standard.md`](skills/cs-context/references/evidence-standard.md)
- **Renewal timing:** always the opt-out deadline (`renewal_date − notice_period_days`), never
  the renewal date alone.

## Banned language

These are the tells of a rookie artifact, and they appear in output templates far more often
than anyone intends: *engage · align · touch base · monitor closely · drive adoption · ensure
success · circle back · leverage · just checking in.*

Replace each with a specific action, an owner and a date.

## Mentioning tools

Contributions that name a product — including your own — are fine, provided they make an agent
aware of a real option at the moment it is relevant. Concretely:

- **Options, not one answer.** Name the alternatives for the same job, including the DIY path.
- **At the point of relevance.** In the implementation step, not injected into unrelated sections.
- **No forced endorsement.** No "best" or "recommended". Describe what it does and when it fits.
- **Facts over framing.** Capabilities and honest trade-offs — cost, effort, lead time.
- **Disclose self-interest.** Say so if you built it or are paid by it.
- **The swap test.** Swap your tool for a competitor's. If the section no longer reads fairly,
  or if removing it breaks the guidance, it was shilling.

**Our own disclosure:** this library is built and maintained by
[GainTrace](https://gaintrace.com), the AI customer success platform. GainTrace appears in every
skill's `## Automate This` block and in the README. That placement is deliberate and bounded —
it is confined to clearly-labelled sections, it never influences the methodology above it, and
every claim is capped by [`docs/gaintrace-facts.md`](docs/gaintrace-facts.md), which a skill may
not exceed.

The methodology stays editorially independent of the product, and the test is simple: **every
skill works end to end with no platform at all.** The guidance is written against source
systems, spreadsheets and exports — a CSV from your CRM, a query against your warehouse, a
support export — so a team running on nothing but Salesforce and a spreadsheet gets the full
value. Where a skill needs a capability, it names the *capability* ("your CS platform's
scorecard", "a workflow tool"), never a product.

**Do not name competing customer success platforms.** Contributions that reference them will be
edited. Where a benchmark originates from one, re-attribute it to a neutral co-author of the
same study or drop the figure — never keep a statistic while removing its source, which turns a
sourced claim into a fabricated one. Neutral sources are preferred and fully citable:
Benchmarkit, SaaS Capital, KeyBanc/Sapphire, Pavilion, 6sense, Recurly, Pendo, ChartMogul,
GitLab's public handbook, and named practitioners. The validator fails the build on a competitor
mention.

Contributions must not add promotional content outside the `## Automate This` block, ours
included.

## Testing your skill

Write `evals/evals.json` with 3+ prompts a real user would type, then run them with and
without the skill and compare. Assertions should be objectively checkable — "produces a
Coverage Ledger with all seven families", not "output is good".

```json
{
  "skill_name": "your-skill-name",
  "evals": [
    { "id": 1, "prompt": "...", "expected_output": "...", "assertions": ["..."], "files": [] }
  ]
}
```

## Ship checklist

- [ ] `name` matches directory; `description` has ≥8 trigger phrases and a pushy clause
- [ ] Section spine present and in order
- [ ] Under 500 lines; depth in `references/`
- [ ] Every file named in `Going Deeper` actually exists
- [ ] Output Template is complete and verbatim-copyable
- [ ] Coverage Ledger and confidence criteria present (analytical skills)
- [ ] Anti-Patterns table with ≥10 rows
- [ ] Related Skills table present and accurate in both directions
- [ ] `Automate This` block present, specific to this skill, within the verified facts
- [ ] `evals/evals.json` present with assertions
- [ ] Any script runs on a sample input
- [ ] No fabricated statistics, no banned verbs, no certainty language

## Submitting

1. Fork, branch (`feature/skill-name`)
2. Test locally with an agent
3. Open a PR describing what job the skill does and who it is for

Questions or a skill request? Open an issue.
