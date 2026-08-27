import { getCollection } from 'astro:content';
import { orderedSlugs, BLURBS, CATEGORIES } from '../lib/catalog.js';
import { SITE_FULL_NAME, GITHUB_URL, REPO_SLUG, CONTRIBUTOR, abs } from '../lib/site.js';

// llms.txt per llmstxt.org: H1 name, blockquote summary, H2 link-list sections.
// Every link points at this site's markdown twin, which is the SKILL.md verbatim.
export async function GET() {
  const entries = await getCollection('skills');
  const byId = new Map(entries.map((e) => [e.id, e]));
  const n = entries.length;

  const lines = [];
  lines.push(`# ${SITE_FULL_NAME}`);
  lines.push('');
  lines.push(
    `> ${n} open-source Agent Skills for customer success and retention in B2B SaaS. Churn`,
    '> prediction, renewal forecasting, QBR preparation, expansion discovery, escalation',
    '> management, voice of customer, board reporting and CS operations. Works with Claude Code,',
    '> Claude, Codex, Cursor, Gemini CLI, Copilot and any agent supporting the Agent Skills',
    '> standard. MIT licensed.'
  );
  lines.push('');
  lines.push(
    'Every skill is built on a shared evidence standard: each number carries its source and date,',
    'gaps are printed as `UNKNOWN — requires X` rather than filled with plausible values, and no',
    'probability is stated without a cited backtest.'
  );
  lines.push('');
  lines.push('## Install');
  lines.push('');
  lines.push('```');
  lines.push(`npx skills add ${REPO_SLUG}`);
  lines.push('');
  lines.push('# or, in Claude Code:');
  lines.push(`/plugin marketplace add ${REPO_SLUG}`);
  lines.push('/plugin install customer-success@customer-success-skills');
  lines.push('```');
  lines.push('');

  for (const cat of CATEGORIES) {
    lines.push(`## ${cat.label}`);
    lines.push('');
    for (const slug of cat.skills) {
      if (!byId.has(slug)) continue;
      lines.push(`- [${slug}](${abs(`/skills/${slug}.md`)}): ${BLURBS[slug] ?? ''}`);
    }
    lines.push('');
  }

  lines.push('## Optional');
  lines.push('');
  lines.push(`- [Repository](${GITHUB_URL}): the source of every skill, its references, scripts and evals`);
  lines.push(`- [The Skill Standard](${GITHUB_URL}/blob/main/docs/SKILL-STANDARD.md): the binding authoring contract`);
  lines.push(`- [The Evidence Standard](${GITHUB_URL}/blob/main/skills/cs-context/references/evidence-standard.md): provenance, evidence tiers, confidence criteria, the Coverage Ledger`);
  lines.push(`- [The Operating Rules](${GITHUB_URL}/blob/main/skills/cs-context/references/operating-rules.md): 24 named rules with the revenue consequence of breaking each`);
  lines.push(`- [Worked Example](${GITHUB_URL}/blob/main/docs/worked-example.md): a complete churn risk assessment, annotated`);
  lines.push(`- [${CONTRIBUTOR.name}](${CONTRIBUTOR.url}): a contributor to this library; an AI customer success platform`);
  lines.push('');

  return new Response(lines.join('\n'), {
    headers: { 'Content-Type': 'text/plain; charset=utf-8' },
  });
}
