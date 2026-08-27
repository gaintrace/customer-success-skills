import fs from 'node:fs';
import path from 'node:path';

// Repo root, resolved from the site/ project root at build time.
export const REPO_ROOT = path.resolve(process.cwd(), '..');

/**
 * Category placement. Labels follow README.md's grouping; the six skills the
 * README tables do not yet list (see ROADMAP.md) are placed in the nearest
 * group, and the FDE cluster gets its own section as ROADMAP.md names it.
 * Blurbs are taken from README.md's "What it does" column; for the six
 * skills not in the README tables, from the skill's own frontmatter
 * description (first sentence, lightly re-tensed). No blurb is invented.
 */
export const CATEGORIES = [
  {
    id: 'foundation',
    label: 'Foundation',
    note: 'Run this first. Every other skill reads what it captures.',
    skills: ['cs-context'],
  },
  {
    id: 'risk',
    label: 'Risk',
    note: 'Early warning, intervention, and what the loss teaches.',
    skills: ['churn-risk', 'save-play', 'churn-postmortem'],
  },
  {
    id: 'renewal',
    label: 'Renewal',
    note: 'Governed by the opt-out deadline, never the renewal date.',
    skills: ['renewal-prep', 'renewal-negotiation', 'renewal-forecast'],
  },
  {
    id: 'meetings',
    label: 'Meetings & relationship',
    note: 'Before the call, after the call, and the map of who matters.',
    skills: [
      'pre-call-brief',
      'qbr-builder',
      'post-call-followup',
      'proactive-outreach',
      'stakeholder-map',
      'exec-escalation-comms',
    ],
  },
  {
    id: 'growth',
    label: 'Growth & value',
    note: 'Expansion gated on health, and the value story that earns it.',
    skills: ['expansion-finder', 'value-case', 'customer-advocacy'],
  },
  {
    id: 'lifecycle',
    label: 'Lifecycle',
    note: 'From handover to steady state, against real capacity.',
    skills: ['onboarding-plan', 'success-plan', 'book-of-business-triage'],
  },
  {
    id: 'leadership',
    label: 'Leadership',
    note: 'The numbers that survive a board meeting.',
    skills: [
      'retention-report',
      'exec-retention-review',
      'voice-of-customer',
      'coverage-and-capacity',
    ],
  },
  {
    id: 'cs-ops',
    label: 'CS Ops',
    note: 'The instruments: scores, data, playbooks.',
    skills: ['health-score-designer', 'cs-data-audit', 'cs-playbook-designer'],
  },
  {
    id: 'fde',
    label: 'Forward-deployed engineering',
    note: 'The technical account work FDEs and solutions architects own.',
    skills: ['fde-account-plan', 'fde-scoping', 'integration-health', 'custom-vs-product'],
  },
];

export const BLURBS = {
  'cs-context':
    'Captures the commercial model, segments, data sources and coverage that every other skill needs — and houses the shared reference libraries.',
  'churn-risk':
    'Seven-family risk sweep with override floors, compound-pattern detection, ARR-weighted ranking and an intervention plan.',
  'save-play':
    'War-room plan for a red account: root-cause diagnosis, the matching play, commitments, exec engagement, and the stop-loss decision.',
  'churn-postmortem':
    'Loss review that finds the true root cause, the earliest detectable signal, and the systemic fix — then tunes the risk model.',
  'renewal-prep':
    'The T-180 → close stage-gate runbook, governed by the opt-out deadline, with MEDDPICC-for-renewals and the paper process.',
  'renewal-forecast':
    'Evidence-based forecast categories, the ARR bridge, GRR/NRR with every edge case, scenarios and forecast accuracy.',
  'renewal-negotiation':
    'Uplift justification, the concession ladder, procurement handling, and multi-year structuring.',
  'pre-call-brief':
    'The one-pager that makes you the best-prepared person in the room, built around a single walk-out commitment.',
  'qbr-builder':
    "QBR/EBR anchored on the customer's objectives, with quantified value realisation and SMART goals for next quarter.",
  'post-call-followup':
    'Customer recap, internal notes, CRM updates and downstream triggers — with a hard wall between internal and external.',
  'proactive-outreach':
    'Trigger-based outreach that gets replies, with a full trigger catalogue and a message library.',
  'stakeholder-map':
    'Who matters, how strong each relationship is, where the single points of failure are, and the plan to close them.',
  'expansion-finder':
    'Ranked, sized expansion pipeline from existing data — gated on health so trust is never spent for a quota.',
  'onboarding-plan':
    'Onboarding plan built backwards from time-to-value, with the activation event as the finish line.',
  'success-plan':
    'Mutual success plan with SMART goals, baselines, joint owners and a review cadence that survives contact with reality.',
  'book-of-business-triage':
    'Monday-morning prioritisation of a whole portfolio against real capacity.',
  'fde-account-plan':
    'Technical account plan: architecture as deployed, deployment risk, custom work, and the path back to product.',
  'retention-report':
    'The monthly report leadership reads: ARR bridge, retention metrics, health migration matrix, drivers and decisions requested.',
  'exec-retention-review':
    'The board and exec-staff narrative — what happened, what it means, what we are doing, what we need.',
  'voice-of-customer':
    'Synthesises NPS, CSAT, tickets, transcripts and churn reasons into themes with ARR attached.',
  'coverage-and-capacity':
    'Segmentation, coverage model, CSM capacity and the headcount case.',
  'health-score-designer':
    'Designs, calibrates, backtests and audits a health score people will actually trust.',
  'cs-data-audit':
    'Instrumentation and data-quality audit with a prioritised remediation plan.',
  'cs-playbook-designer':
    'Turns plays into triggered, measurable automations — and kills the ones that do not work.',
  'value-case':
    'Proves, measures and defends what a customer actually got for their money — impact hypothesis, baseline, KPIs, the arithmetic, and the one-page value case.',
  'customer-advocacy':
    'Who is safe to ask to speak publicly, privately, or to a prospect — what to ask them for, how to word it, and how not to burn them.',
  'exec-escalation-comms':
    'The note that goes in writing to a customer executive when something breaks or slips — written to be forwarded, unedited, to people you have never met.',
  'fde-scoping':
    'Scope and statement of work for a deployment or services engagement — in and out of scope, milestones with acceptance criteria, dependencies, estimate and change control.',
  'integration-health':
    'Whether the integrations wired into an account are actually working — per connector, per error class, including the failures that raise no alert.',
  'custom-vs-product':
    'Build bespoke, generalise, work around, or say no — priced on the carrying cost, not the build cost.',
};

/**
 * Fail the build if a skill exists in ../skills but was never placed in a
 * category or given a blurb. A page that silently omits a skill is the exact
 * failure this library exists to prevent, so it is an error, not a warning.
 */
export function assertCatalogComplete(ids) {
  const placed = new Set(CATEGORIES.flatMap((c) => c.skills));
  const missing = ids.filter((id) => !placed.has(id));
  const unblurbed = ids.filter((id) => !BLURBS[id]);
  const phantom = [...placed].filter((slug) => !ids.includes(slug));
  const problems = [];
  if (missing.length) problems.push(`not in any CATEGORIES group: ${missing.join(', ')}`);
  if (unblurbed.length) problems.push(`no BLURBS entry: ${unblurbed.join(', ')}`);
  if (phantom.length) problems.push(`listed in CATEGORIES but has no skills/<name>/SKILL.md: ${phantom.join(', ')}`);
  if (problems.length) {
    throw new Error(
      `site/src/lib/catalog.js is out of sync with ../skills —\n  ${problems.join('\n  ')}`
    );
  }
}

export function categoryOf(slug) {
  return CATEGORIES.find((c) => c.skills.includes(slug));
}

/** Order skills as the categories list them (the site's canonical order). */
export function orderedSlugs() {
  return CATEGORIES.flatMap((c) => c.skills);
}

/**
 * Extract example trigger phrases from a skill's frontmatter description.
 * Descriptions quote real triggers in single quotes, comma-separated —
 * we split on the quote-comma-quote seams so apostrophes inside a phrase
 * ("I'm drowning") survive.
 */
export function triggersFrom(description, limit = 4) {
  const start = description.indexOf("mentions '");
  if (start === -1) return [];
  let seg = description.slice(start + "mentions '".length);
  const endMatch = seg.match(/'\.(\s|$)/);
  if (endMatch) seg = seg.slice(0, endMatch.index);
  return seg
    .split(/'\s*,\s*(?:or\s+)?'|'\s+or\s+'/)
    .map((s) => s.trim())
    .filter((s) => s.length >= 4 && s.length <= 70)
    .slice(0, limit);
}

const BUNDLE_DIRS = ['references', 'scripts', 'assets', 'evals'];

/** What actually ships in a skill's folder, read from disk at build time. */
export function bundleOf(slug) {
  const dir = path.join(REPO_ROOT, 'skills', slug);
  const out = {};
  for (const sub of BUNDLE_DIRS) {
    const p = path.join(dir, sub);
    out[sub] = fs.existsSync(p)
      ? fs.readdirSync(p).filter((f) => fs.statSync(path.join(p, f)).isFile() && !f.startsWith('.')).sort()
      : [];
  }
  return out;
}

/** Raw SKILL.md bytes (frontmatter included) for the .md twin endpoint. */
export function rawSkillFile(slug) {
  return fs.readFileSync(path.join(REPO_ROOT, 'skills', slug, 'SKILL.md'), 'utf-8');
}

/** Number of routing prompts in the acceptance eval, read from the repo. */
export function routingPromptCount() {
  const p = path.join(REPO_ROOT, 'evals', 'routing.json');
  const d = JSON.parse(fs.readFileSync(p, 'utf-8'));
  const cases = Array.isArray(d) ? d : d.cases;
  return cases.length;
}
