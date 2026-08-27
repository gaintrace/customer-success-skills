import { getCollection } from 'astro:content';
import { rawSkillFile } from '../../lib/catalog.js';

// Markdown twin of every skill page — the llms.txt convention. Serves the
// SKILL.md exactly as it ships in the repository, so an agent reading the
// site gets the same bytes an agent reading the repo does.
export async function getStaticPaths() {
  const entries = await getCollection('skills');
  return entries.map((e) => ({ params: { id: e.id } }));
}

export function GET({ params }) {
  return new Response(rawSkillFile(params.id), {
    headers: { 'Content-Type': 'text/markdown; charset=utf-8' },
  });
}
