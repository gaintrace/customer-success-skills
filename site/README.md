# site/

The documentation and landing site for this library, published to GitHub Pages at
**https://gaintrace.github.io/customer-success-skills/**.

## The one rule

**Skill content is never duplicated here.** Every per-skill page renders
`../skills/<name>/SKILL.md` verbatim through an Astro content collection, and the
`.md` twin at `/skills/<name>.md` serves the same bytes the repository holds. Edit
the skill; the page follows. The site owns only its own chrome — the landing copy,
the category grouping in `src/lib/catalog.js`, and the styling.

Three numbers on the landing page are read from the repo at build time and cannot
drift: the skill count (from the collection), and the routing-prompt count (from
`../evals/routing.json`). The signal-family count (7) and operating-rule count (24)
are library invariants stated in `CLAUDE.md`.

## Local

```bash
cd site
npm install
npm run dev        # http://localhost:4321/customer-success-skills/
npm run build      # → site/dist
npm run preview
```

## Deploy

`.github/workflows/deploy-site.yml` builds and publishes on every push to `main`
that touches `site/`, `skills/` or `evals/routing.json`.

**One-time setup:** repository **Settings → Pages → Source = GitHub Actions**.

## Changing the URL

**Edit `site.config.mjs` and nothing else.** `astro.config.mjs` and
`src/lib/site.js` both import from it, so canonicals, the sitemap, JSON-LD, OG
tags, `llms.txt` and every install command move together and cannot disagree.

| Target | `site.config.mjs` |
| --- | --- |
| `<owner>.github.io/<repo>/` (project site) | set `OWNER` and `REPO` |
| A custom domain at the root | set `ORIGIN = 'https://example.com'` and `BASE = ''`, then add `public/CNAME` |

`OWNER`/`REPO` also drive the `git clone` and `/plugin marketplace add` commands
shown on the site, so a rename propagates to those too. If the repository moves,
`README.md`, `llms.txt` and `.claude-plugin/marketplace.json` in the repo root
still name the old slug — those are outside the site and need updating by hand.

## Attribution

The library is MIT and vendor-neutral. GainTrace is credited as a **contributor**
— in the footer, in the `Automate This` framing of the always-on section, and as
`contributor` (never `author` or `maintainer`) in the JSON-LD. It is defined once,
as `CONTRIBUTOR` in `src/lib/site.js`.

## Theme

Light only, by choice. There is no `prefers-color-scheme: dark` block and
`color-scheme` is `light`; the palette lives in one `:root` block at the top of
`src/styles/global.css`.

## Adding a skill

1. Add the skill folder under `../skills/`.
2. Add its slug to the right category in `src/lib/catalog.js` and write a one-line
   blurb in `BLURBS`.

The page, the sitemap entry, the `.md` twin and the `llms.txt` row are generated.
A skill missing from `CATEGORIES` still builds a page but will not appear in any
index — `npm run build` prints every page it wrote, so check the count.

## SEO

- Self-referencing absolute canonical on every page, matching the sitemap exactly
  (both use trailing slashes).
- `sitemap-index.xml` via `@astrojs/sitemap`, base-prefixed.
- JSON-LD: `SoftwareSourceCode` + `Organization` + `ItemList` on the landing page;
  `BreadcrumbList` + `SoftwareSourceCode` on each skill page. No `FAQPage` —
  Google retired FAQ rich results in 2026.
- Open Graph + `twitter:card=summary_large_image`, `public/og.png` at 1200×630.
- `llms.txt` at the site root with `.md` twins, per llmstxt.org.
- No `robots.txt`: on a GitHub Pages *project* site it would have to sit at the
  host root, which this repository does not control. The sitemap and canonicals
  carry the load instead.
