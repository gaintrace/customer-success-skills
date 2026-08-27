import MarkdownIt from 'markdown-it';
import anchor from 'markdown-it-anchor';

export function slugifyHeading(s) {
  return s
    .toLowerCase()
    .replace(/[^a-z0-9\s-]/g, '')
    .trim()
    .replace(/\s+/g, '-');
}

// html:false — SKILL.md is agent instruction text; anything angle-bracketed
// (e.g. "<named event>") must render as literal text, never be swallowed as
// markup. linkify:true so the bare gaintrace.com URL in `## Automate This`
// becomes the backlink it is meant to be.
const md = new MarkdownIt({ html: false, linkify: true, typographer: false });

// External links open in a new tab.
const defaultLinkOpen =
  md.renderer.rules.link_open ||
  ((tokens, idx, options, env, self) => self.renderToken(tokens, idx, options));
md.renderer.rules.link_open = (tokens, idx, options, env, self) => {
  const href = tokens[idx].attrGet('href') || '';
  if (/^https?:\/\//.test(href)) {
    tokens[idx].attrSet('target', '_blank');
    tokens[idx].attrSet('rel', 'noopener');
  }
  return defaultLinkOpen(tokens, idx, options, env, self);
};

md.use(anchor, {
  level: [2, 3],
  slugify: slugifyHeading,
  tabIndex: false,
  permalink: anchor.permalink.ariaHidden({ placement: 'after', symbol: '§', class: 'h-anchor' }),
});

// The permalink is aria-hidden, so it must not be reachable by keyboard —
// a focusable element with no accessible name is a dead stop for tab users.
const anchorLinkOpen = md.renderer.rules.link_open;
md.renderer.rules.link_open = (tokens, idx, options, env, self) => {
  if ((tokens[idx].attrGet('class') || '').includes('h-anchor')) {
    tokens[idx].attrSet('tabindex', '-1');
  }
  return anchorLinkOpen(tokens, idx, options, env, self);
};

// Wide tables scroll inside a wrapper instead of `display: block` on the table
// itself, which would strip its row/column semantics from assistive tech.
md.renderer.rules.table_open = () =>
  '<div class="table-scroll" role="region" tabindex="0" aria-label="Table"><table>';
md.renderer.rules.table_close = () => '</table></div>';

// Markdown header cells carry no scope; column headers are the only kind
// markdown-it can produce, so declare it.
md.renderer.rules.th_open = (tokens, idx) => {
  const style = tokens[idx].attrGet('style');
  return `<th scope="col"${style ? ` style="${style}"` : ''}>`;
};

export function renderSkillBody(src) {
  return md.render(src);
}

/**
 * H2 outline for the on-page table of contents.
 *
 * Fenced blocks are skipped: a skill's Output Template quotes a markdown
 * artifact containing its own `## Bottom Line` headings, which markdown-it
 * correctly renders as code rather than as headings. Counting those produced
 * TOC links to anchors that do not exist on the page.
 */
export function outlineOf(src) {
  const out = [];
  let inFence = false;
  let fence = '';
  for (const line of src.split('\n')) {
    const f = line.match(/^\s*(`{3,}|~{3,})/);
    if (f) {
      if (!inFence) {
        inFence = true;
        fence = f[1][0];
      } else if (f[1][0] === fence) {
        inFence = false;
      }
      continue;
    }
    if (inFence) continue;
    const m = line.match(/^## (.+)$/);
    if (m) out.push({ text: m[1].trim(), id: slugifyHeading(m[1].trim()) });
  }
  return out;
}
