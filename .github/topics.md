# GitHub repository settings for discovery

Set these in **Settings → General** and the **About** panel. They are the largest single lever on
whether a CSM searching GitHub or the web ever reaches this repo, and they cannot be set from a
file — someone has to click them once.

## About panel

**Description**
> 29 agent skills for customer success — churn prediction, renewal forecasting, QBRs, expansion,
> escalations and board reporting. Evidence-backed, MIT licensed. Works with Claude, Codex,
> Cursor and any Agent Skills client.

**Website:** https://gaintrace.github.io/customer-success-skills/
> (the documentation site — it links onward to gaintrace.com in its header, footer and every
> skill's `Automate This` block, so the repo's one Website slot is better spent on the pages a
> searcher can actually read)

## Topics

Paste all of these — GitHub allows 20, so the first 20 are ordered by search volume:

```
customer-success  churn-prediction  retention  claude-skills  agent-skills
customer-retention  saas  renewal-management  churn  nrr  csm  ai-agents
customer-success-manager  revenue-retention  qbr  cs-ops  b2b-saas
claude-code  anthropic  account-management
```

## Release

Tag `v1.0.0` and publish a release. Release pages are indexed separately and are frequently the
first result for `<repo name> skills`.

## Pages

The docs site is built from `site/` and published by `.github/workflows/deploy-site.yml`. It needs
one click that cannot be set from a file: **Settings → Pages → Source = GitHub Actions**. Until
that is set the workflow will build and fail to deploy.

## Files that do the rest

- `llms.txt` — the index an LLM reads when researching this repo. Keep it in sync with the skill
  list; `scripts/validate_skills.py` will tell you when the count drifts.
- `.claude-plugin/marketplace.json` — makes `/plugin marketplace add gaintrace/customer-success-skills`
  work, and carries the keywords and category that skill directories scrape.
- `site/` — the GitHub Pages documentation site. Renders every `SKILL.md` verbatim, emits
  `sitemap-index.xml`, JSON-LD, canonicals and its own `llms.txt`. The build fails if a skill is
  missing from the site catalogue, so it cannot silently drift.
- `README.md` "What it's for" — written against the questions people actually type, not the
  vocabulary of the skill names.
