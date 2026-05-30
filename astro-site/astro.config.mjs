import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

export default defineConfig({
  site: 'https://metacortex.engineer',
  output: 'static',
  build: {
    format: 'directory',
  },
  redirects: {
    '/building-knowledge-graph-from-covid-medical-literature-kaggle-cord19-competition-f0178d2a19bd': '/post/building-knowledge-graph-from-covid-medical-literature-kaggle-cord19-competition/',
  },
  integrations: [sitemap()],
});
