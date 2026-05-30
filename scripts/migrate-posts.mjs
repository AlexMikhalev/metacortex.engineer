import { readdir, readFile, writeFile, mkdir } from 'node:fs/promises';
import { join, basename } from 'node:path';

const SRC = join(import.meta.dirname, '..', 'content', 'post');
const DST = join(import.meta.dirname, '..', 'astro-site', 'src', 'content', 'post');

function parseFrontmatter(content) {
  const match = content.match(/^---\r?\n([\s\S]*?)\r?\n---\r?\n([\s\S]*)$/);
  if (!match) return null;
  return { raw: match[1], body: match[2] };
}

function parseYamlSimple(raw) {
  const data = {};
  const lines = raw.split('\n');
  let currentKey = null;
  let inArray = false;
  let arrayItems = [];

  for (const line of lines) {
    const trimmed = line.trim();

    if (trimmed.startsWith('- ') && inArray) {
      let val = trimmed.slice(2).trim();
      if (val.startsWith("'") || val.startsWith('"')) {
        val = val.slice(1, -1);
      }
      if (val.startsWith('/')) {
        arrayItems.push(val);
      }
      continue;
    }

    if (currentKey && inArray) {
      data[currentKey] = arrayItems;
      inArray = false;
      currentKey = null;
    }

    const kvMatch = trimmed.match(/^([\w]+):\s*(.*)$/);
    if (kvMatch) {
      const key = kvMatch[1];
      let val = kvMatch[2].trim();

      if (val === '' || val === '|2-' || val === '|') {
        if (key === 'aliases') {
          currentKey = key;
          inArray = true;
          arrayItems = [];
        }
        continue;
      }

      if (val.startsWith("'") || val.startsWith('"')) {
        val = val.slice(1, -1);
      }

      if (key === 'tags') {
        if (val.startsWith('[')) {
          val = val.slice(1, -1);
        }
        data[key] = val;
      } else if (key === 'date' || key === 'lastmod') {
        data[key] = val;
      } else if (key === 'aliases') {
        data[key] = [val];
      } else {
        data[key] = val;
      }
    }
  }

  if (currentKey && inArray) {
    data[currentKey] = arrayItems;
  }

  return data;
}

function buildFrontmatter(data) {
  let fm = '---\n';
  fm += `title: "${(data.title || '').replace(/"/g, '\\"')}"\n`;

  if (data.subtitle) {
    fm += `subtitle: "${data.subtitle.replace(/"/g, '\\"')}"\n`;
  }

  if (data.slug) {
    fm += `slug: "${data.slug}"\n`;
  }

  if (data.description && data.description !== '""') {
    fm += `description: "${(data.description || '').replace(/"/g, '\\"')}"\n`;
  }

  if (data.tags) {
    if (typeof data.tags === 'string') {
      fm += `tags: "${data.tags}"\n`;
    } else if (Array.isArray(data.tags) && data.tags.length > 0) {
      fm += `tags:\n`;
      for (const t of data.tags) {
        fm += `  - "${t}"\n`;
      }
    }
  }

  if (data.author) {
    fm += `author: "${data.author}"\n`;
  }

  fm += `date: "${data.date}"\n`;

  if (data.lastmod) {
    fm += `lastmod: "${data.lastmod}"\n`;
  }

  if (data.aliases && Array.isArray(data.aliases) && data.aliases.length > 0) {
    fm += `aliases:\n`;
    for (const a of data.aliases) {
      fm += `  - "${a}"\n`;
    }
  }

  fm += `draft: false\n`;
  fm += '---\n';
  return fm;
}

async function migrate() {
  await mkdir(DST, { recursive: true });

  const files = await readdir(SRC);
  const mdFiles = files.filter(f =>
    f.endsWith('.md') && !f.startsWith('draft__') && f !== '_index.md'
  );

  console.log(`Found ${mdFiles.length} blog posts to migrate`);

  let migrated = 0;
  let errors = 0;

  for (const file of mdFiles) {
    try {
      const content = await readFile(join(SRC, file), 'utf-8');
      const parsed = parseFrontmatter(content);

      if (!parsed) {
        console.log(`SKIP (no frontmatter): ${file}`);
        continue;
      }

      const data = parseYamlSimple(parsed.raw);

      if (!data.date) {
        const dateFromName = file.match(/^(\d{4}-\d{2}-\d{2})/);
        if (dateFromName) {
          data.date = dateFromName[1];
        } else {
          console.log(`SKIP (no date): ${file}`);
          continue;
        }
      }

      if (!data.title) {
        data.title = file.replace(/\.md$/, '').replace(/^\d{4}-\d{2}-\d{2}-?/, '').replace(/-/g, ' ');
      }

      const newFm = buildFrontmatter(data);
      const newContent = newFm + '\n' + parsed.body;

      let outName = file;

      const slugMatch = file.match(/^\d{4}-\d{2}-\d{2}-?(.+)\.md$/);
      if (slugMatch && data.slug) {
        outName = data.slug + '.md';
      } else if (slugMatch) {
        outName = slugMatch[1] + '.md';
      }

      await writeFile(join(DST, outName), newContent, 'utf-8');
      migrated++;
      console.log(`OK: ${file} -> ${outName}`);
    } catch (err) {
      errors++;
      console.error(`ERROR: ${file}: ${err.message}`);
    }
  }

  console.log(`\nMigrated: ${migrated}, Errors: ${errors}`);
}

migrate();
