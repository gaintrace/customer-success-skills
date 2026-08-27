import { defineCollection } from 'astro:content';
import { z } from 'astro/zod';
import { glob } from 'astro/loaders';

// Every SKILL.md in the repository is the single source of truth.
// The site renders those files verbatim — no skill copy is duplicated here.
const skills = defineCollection({
  loader: glob({
    pattern: '*/SKILL.md',
    base: '../skills',
    generateId: ({ entry }) => entry.split('/')[0],
  }),
  schema: z.object({
    name: z.string(),
    description: z.string(),
    license: z.string().optional(),
    metadata: z
      .object({
        version: z.string().optional(),
        role: z.string().optional(),
        cadence: z.string().optional(),
      })
      .passthrough()
      .optional(),
  }),
});

export const collections = { skills };
