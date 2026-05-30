import rss from '@astrojs/rss';
import { getCollection } from 'astro:content';
import type { APIContext } from 'astro';

export async function GET(context: APIContext) {
  const posts = (await getCollection('post'))
    .filter(post => !post.data.draft)
    .sort((a, b) => b.data.date.valueOf() - a.data.date.valueOf());

  return rss({
    title: 'Metacortex Engineer',
    description: 'Science, Artificial Intelligence and Engineering by Dr Alexander Mikhalev',
    site: context.site!,
    items: posts.map(post => ({
      title: post.data.title,
      pubDate: post.data.date,
      description: post.data.description || post.data.subtitle || '',
      link: `/post/${post.slug}/`,
    })),
    customData: `<language>en-gb</language>`,
  });
}
