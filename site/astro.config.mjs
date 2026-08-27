// @ts-check
import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';
import { ORIGIN, BASE } from './site.config.mjs';

// URL is defined once, in site.config.mjs. See that file to move the site.
export default defineConfig({
  site: ORIGIN,
  base: BASE || '/',
  trailingSlash: 'ignore',
  integrations: [sitemap()],
  build: { format: 'directory' },
});
