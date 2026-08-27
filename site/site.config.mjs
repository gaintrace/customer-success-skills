// ────────────────────────────────────────────────────────────────────────────
// The ONLY place the deployed URL is defined.
// astro.config.mjs and src/lib/site.js both read from here, so the canonical
// URLs, sitemap, JSON-LD, OG tags and llms.txt can never disagree.
//
// To move the site, change OWNER / REPO (and ORIGIN for a custom domain).
// Nothing else in the codebase needs editing.
// ────────────────────────────────────────────────────────────────────────────

/** GitHub org or user that hosts the repository. */
export const OWNER = 'gaintrace';

/** Repository name. Also the URL sub-path on a GitHub Pages project site. */
export const REPO = 'customer-success-skills';

/**
 * Scheme + host, no trailing slash.
 * GitHub Pages project site:  `https://${OWNER}.github.io`
 * Custom domain:              'https://example.com'  (then set BASE to '')
 */
export const ORIGIN = `https://${OWNER}.github.io`;

/**
 * URL sub-path, no trailing slash. '' means the site lives at the root.
 * On a project site this must be `/${REPO}`.
 */
export const BASE = `/${REPO}`;

export const GITHUB_URL = `https://github.com/${OWNER}/${REPO}`;
