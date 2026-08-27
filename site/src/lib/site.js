// Facts the site states about itself.
// The deployed URL comes from site.config.mjs — the single source of truth
// shared with astro.config.mjs. Do not hard-code a URL here.
import { ORIGIN, BASE as URL_BASE, OWNER, REPO, GITHUB_URL as REPO_URL } from '../../site.config.mjs';

export const SITE_URL = ORIGIN;
export const BASE = URL_BASE;
export const SITE_NAME = 'Customer Success Skills';
/** The qualifier that makes the name say what the library is for. */
export const SITE_TAGLINE = 'for AI agents';
/** The full name, used in titles, JSON-LD and llms.txt. */
export const SITE_FULL_NAME = `${SITE_NAME} ${SITE_TAGLINE}`;
export const GITHUB_OWNER = OWNER;
export const GITHUB_REPO = REPO;
export const GITHUB_URL = REPO_URL;
/** `owner/repo`, as the plugin install commands spell it. */
export const REPO_SLUG = `${OWNER}/${REPO}`;
export const LICENSE = 'MIT';

// GainTrace contributes to this library. It does not own it.
export const CONTRIBUTOR = {
  name: 'GainTrace',
  url: 'https://gaintrace.com',
  solutionsUrl: 'https://gaintrace.com/solutions',
};

/** Prefix an internal path with the deploy base. Always pass a leading slash. */
export function href(path) {
  return `${BASE}${path}`;
}

/** Absolute URL for canonical / og / JSON-LD. */
export function abs(path) {
  return `${SITE_URL}${BASE}${path}`;
}

/**
 * Meta descriptions are truncated by search engines around 155-160 characters.
 * Build one from a lead sentence plus an optional suffix, appending the suffix
 * only when it fits and trimming at a word boundary rather than mid-word.
 */
export function metaDescription(lead, suffix = '', limit = 155) {
  const clean = (t) => t.replace(/\s+/g, ' ').trim();
  let out = clean(lead);
  if (suffix && out.length + 1 + clean(suffix).length <= limit) {
    out = `${out} ${clean(suffix)}`;
  }
  if (out.length <= limit) return out;
  const cut = out.slice(0, limit - 1);
  const at = cut.lastIndexOf(' ');
  return `${(at > limit * 0.6 ? cut.slice(0, at) : cut).replace(/[\s,;:—-]+$/, '')}…`;
}
