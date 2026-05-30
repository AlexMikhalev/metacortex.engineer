import { defineCollection, z } from 'astro:content';

const postCollection = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    subtitle: z.string().optional(),
    slug: z.string().optional(),
    description: z.string().default(''),
    tags: z.union([z.string(), z.array(z.string())]).transform(val => {
      if (typeof val === 'string') return val.split(',').map(t => t.trim()).filter(Boolean);
      return val;
    }).default([]),
    author: z.string().default('Alex Mikhalev'),
    date: z.coerce.date(),
    lastmod: z.coerce.date().optional(),
    aliases: z.array(z.string()).optional(),
    draft: z.boolean().default(false),
  }),
});

const projectCollection = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    summary: z.string().default(''),
    tags: z.union([z.string(), z.array(z.string())]).transform(val => {
      if (typeof val === 'string') return val.split(',').map(t => t.trim()).filter(Boolean);
      return val;
    }).default([]),
    date: z.coerce.date(),
    external_link: z.string().optional(),
    url_code: z.string().optional(),
    url_slides: z.string().optional(),
    url_video: z.string().optional(),
  }),
});

const eventCollection = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    abstract: z.string().optional(),
    event: z.string().optional(),
    location: z.string().optional(),
    date: z.coerce.date(),
    tags: z.union([z.string(), z.array(z.string())]).transform(val => {
      if (typeof val === 'string') return val.split(',').map(t => t.trim()).filter(Boolean);
      return val;
    }).default([]),
    url_pdf: z.string().optional(),
    url_slides: z.string().optional(),
    url_video: z.string().optional(),
  }),
});

export const collections = {
  post: postCollection,
  project: projectCollection,
  event: eventCollection,
};
