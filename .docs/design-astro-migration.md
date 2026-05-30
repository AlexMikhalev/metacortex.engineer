# Implementation Plan: Hugo/Wowchemy to Astro Migration

**Status**: Draft
**Research Doc**: `.docs/research-astro-migration.md`
**Author**: Opencode Agent
**Date**: 2026-05-30
**Estimated Effort**: 3-4 days

## Overview

### Summary

Migrate metacortex.engineer from Hugo/Wowchemy to Astro 5, using the portfolio design from metacortex-portfolio.html as the homepage, with blog posts managed via Astro Content Collections.

### Approach

Hybrid architecture: single-page portfolio homepage (matching metacortex-portfolio.html design) plus a `/post/` section for blog content. Data-driven components pull author info, experience, skills from JSON/YAML data files (extracted from Hugo config) rather than hardcoding.

### Scope

**In Scope:**
- Portfolio homepage with hero, projects, skills, experience, contact sections
- Blog section with all 38 posts via Content Collections
- Projects page (1 project: The Pattern)
- Publications page (section stub)
- Talks/Events page (5 events)
- CI/CD to Cloudflare R2 via GitHub Actions
- RSS feed, sitemap, robots.txt
- URL preservation (redirect map if needed)
- Google Analytics integration

**Out of Scope:**
- 98 RST archive posts
- Full-text search (Pagefind)
- Dark mode toggle
- Comment system
- CMS admin interface
- Multi-language support

**Avoid At All Cost** (from 5/25 analysis):
- React/Vue/Svelte component framework integration (unnecessary complexity)
- Headless CMS integration (over-engineering for single-maintainer site)
- Complex animation libraries (portfolio HTML uses only CSS transitions)
- Image optimisation pipeline (only avatar.jpg exists; not worth infra)
- Tag/category taxonomy pages (can add later)

## Architecture

### Component Diagram

```
astro-site/
  src/
    layouts/
      BaseLayout.astro          # <html>, <head>, <body> shell, meta, analytics
    pages/
      index.astro               # Portfolio homepage (nav + hero + projects + skills + exp + contact)
      post/
        index.astro             # Blog listing page
        [...slug].astro         # Individual blog post (dynamic route)
      projects/
        index.astro             # Projects listing
        [slug].astro            # Individual project page
      publications.astro        # Publications page
      talks/
        index.astro             # Talks listing
    components/
      Nav.astro                 # Fixed navbar with logo and links
      Hero.astro                # Full-viewport hero section
      ProjectsGrid.astro        # Project cards grid
      ProjectCard.astro         # Single project card
      SkillsGrid.astro          # Skills categories grid
      SkillCategory.astro       # Single skill category with dot levels
      ExperienceTimeline.astro  # Timeline of career positions
      ExperienceItem.astro      # Single timeline entry
      Contact.astro             # Contact section
      Footer.astro              # Site footer
      BlogCard.astro            # Blog post preview card
    content/
      config.ts                 # Content Collection schemas
      post/                     # 38 migrated blog posts (.md)
      project/                  # Project content (.md)
      event/                    # Talk/event content (.md)
    data/
      author.json               # Author profile data
      experience.json           # Career history
      skills.json               # Skills with levels
      projects.json             # Featured projects (portfolio homepage data)
      navigation.json           # Nav links config
      social.json               # Social links
    styles/
      global.css                # Portfolio CSS (from metacortex-portfolio.html)
  public/
    img/                        # Avatar, images
    media/                      # CV PDFs
    slides/                     # Presentation slides
    uploads/                    # Misc uploads
  astro.config.mjs
  package.json
```

### Data Flow

```
Content Collections (post/, project/, event/) --> pages/post/[...slug].astro --> HTML
Data files (JSON)                              --> components/*.astro        --> HTML
Static assets (public/)                        --> copied as-is              --> static
```

### Key Design Decisions

| Decision | Rationale | Alternatives Rejected |
|----------|-----------|----------------------|
| Hybrid: SPA homepage + blog pages | Portfolio design is inherently single-page; blog needs individual pages | Full SPA (bad for blog SEO), full multi-page (loses portfolio UX) |
| JSON data files for portfolio content | Simple, no schema overhead, easy to edit | YAML (extra parser), Astro Content Collections for non-blog (unnecessary) |
| Keep `/post/` URL prefix | Matches current Hugo URL structure, preserves SEO | `/blog/` (breaks existing URLs) |
| Content Collections for blog only | Blog benefits from type-safe schemas; portfolio sections are one-off | Content Collections everywhere (over-engineering) |
| Vanilla CSS (no framework) | Portfolio CSS already works; ~470 lines of clean CSS | Tailwind (rewrite everything), Bulma (adds dependency) |

### Eliminated Options (Essentialism)

| Option Rejected | Why Rejected | Risk of Including |
|-----------------|--------------|-------------------|
| Tailwind CSS | Would require rewriting all 470 lines of portfolio CSS | 2-3 days extra work for zero benefit |
| React/Svelte islands | No interactive components need a framework | Bundle size increase, dependency management |
| MDX for blog posts | No JSX needed in blog content | Unnecessary build complexity |
| Image optimisation | Only 1 image (avatar.jpg, 33KB) | Infrastructure for no gain |
| Pagination for blog | 38 posts fit on one page easily | Premature optimisation |

### Simplicity Check

**What if this could be easy?**

The simplest design: copy the portfolio HTML into Astro's `src/pages/index.astro`, add a Content Collection for blog posts, and a dynamic route to render them. That's essentially what we're doing. The only added complexity is extracting data into JSON files instead of hardcoding - this is justified because it makes the site editable without touching component code.

**Senior Engineer Test**: A senior engineer would call this "obvious" rather than "overcomplicated". The architecture is flat: pages consume components, components consume data files. No abstractions, no framework dependencies, no state management.

**Nothing Speculative Checklist**:
- [x] No features the user didn't request
- [x] No abstractions "in case we need them later"
- [x] No flexibility "just in case"
- [x] No error handling for scenarios that cannot occur
- [x] No premature optimisation

## File Changes

### New Files

| File | Purpose |
|------|---------|
| `astro-site/package.json` | Project dependencies (astro, @astrojs/sitemap, @astrojs/rss) |
| `astro-site/astro.config.mjs` | Astro configuration |
| `astro-site/tsconfig.json` | TypeScript config |
| `astro-site/src/layouts/BaseLayout.astro` | HTML shell with head, meta, analytics |
| `astro-site/src/pages/index.astro` | Portfolio homepage |
| `astro-site/src/pages/post/index.astro` | Blog listing |
| `astro-site/src/pages/post/[...slug].astro` | Blog post template |
| `astro-site/src/pages/projects/index.astro` | Projects listing |
| `astro-site/src/pages/projects/[slug].astro` | Project detail page |
| `astro-site/src/pages/publications.astro` | Publications page |
| `astro-site/src/pages/talks/index.astro` | Talks listing |
| `astro-site/src/components/Nav.astro` | Navigation bar |
| `astro-site/src/components/Hero.astro` | Hero section |
| `astro-site/src/components/ProjectsGrid.astro` | Projects grid |
| `astro-site/src/components/ProjectCard.astro` | Project card |
| `astro-site/src/components/SkillsGrid.astro` | Skills categories |
| `astro-site/src/components/SkillCategory.astro` | Skill category |
| `astro-site/src/components/ExperienceTimeline.astro` | Experience timeline |
| `astro-site/src/components/ExperienceItem.astro` | Timeline entry |
| `astro-site/src/components/Contact.astro` | Contact section |
| `astro-site/src/components/Footer.astro` | Footer |
| `astro-site/src/components/BlogCard.astro` | Blog post card |
| `astro-site/src/content/config.ts` | Content Collection schemas |
| `astro-site/src/data/author.json` | Author profile |
| `astro-site/src/data/experience.json` | Career history |
| `astro-site/src/data/skills.json` | Skills with levels |
| `astro-site/src/data/projects.json` | Featured projects |
| `astro-site/src/data/navigation.json` | Nav links |
| `astro-site/src/data/social.json` | Social links |
| `astro-site/src/styles/global.css` | Portfolio CSS |
| `scripts/migrate-posts.mjs` | Blog post frontmatter migration script |
| `.github/workflows/deploy-astro-r2.yml` | CI/CD for Astro |

### Modified Files

| File | Changes |
|------|---------|
| `.github/workflows/deploy-astro-r2.yml` | New workflow (adapted from Zola R2 workflow) |

### Deleted Files

None during migration. Original Hugo content preserved in repo. Defer cleanup to post-launch.

## API Design

### Content Collection Schema (src/content/config.ts)

```typescript
import { defineCollection, z } from 'astro:content';

const postCollection = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    subtitle: z.string().optional(),
    slug: z.string().optional(),
    description: z.string().default(''),
    tags: z.union([z.string(), z.array(z.string())]).transform(val => {
      if (typeof val === 'string') return val.split(',').map(t => t.trim());
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
    summary: z.string(),
    tags: z.array(z.string()).default([]),
    date: z.coerce.date(),
    external_link: z.string().optional(),
    url_code: z.string().optional(),
    url_slides: z.string().optional(),
    url_video: z.string().optional(),
    image: z.object({
      caption: z.string().optional(),
      focal_point: z.string().optional(),
    }).optional(),
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
    tags: z.array(z.string()).default([]),
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
```

### Data File Schemas

**author.json:**
```typescript
{
  name: string;           // "Dr Alexander Mikhalev"
  role: string;           // "AI/ML Architect"
  tagline: string;        // "Technology Leader & Innovation Architect"
  bio: string;            // Full biography
  avatar: string;         // "/img/avatar.jpg"
  organisations: Array<{
    name: string;
    url: string;
  }>;
  education: Array<{
    course: string;
    institution: string;
    year: number;
  }>;
  email: string;
}
```

**experience.json:**
```typescript
Array<{
  title: string;
  company: string;
  company_url?: string;
  location: string;
  date_start: string;     // ISO date
  date_end: string;       // ISO date or "" for current
  description: string;
}>
```

**skills.json:**
```typescript
Array<{
  category: string;       // "AI & Data Science"
  skills: Array<{
    name: string;
    level: 1|2|3|4|5;     // Dot level
  }>
}>
```

**projects.json:**
```typescript
Array<{
  title: string;
  description: string;
  tags: string[];
  url?: string;
  image?: string;
}>
```

## Test Strategy

### Build Tests

| Test | Method | Purpose |
|------|--------|---------|
| `astro build` succeeds | CLI | All pages render without errors |
| All 38 posts render | Script | Verify no frontmatter parse failures |
| All internal links valid | `astro check` | No broken links |
| CSS renders correctly | Visual inspection | Portfolio design preserved |

### Content Validation

| Test | Method | Purpose |
|------|--------|---------|
| Frontmatter schema valid | `astro check` | All posts match Content Collection schema |
| No missing dates | Script | Every post has a valid date |
| Tags normalised | Script | Tags are arrays (not comma strings) |

### Deployment Tests

| Test | Method | Purpose |
|------|--------|---------|
| R2 deploy succeeds | GitHub Actions | Workflow completes |
| Live site loads | Manual | Homepage, blog, projects all accessible |
| Google Analytics fires | Browser DevTools | GA script loads |

## Implementation Steps

### Step 1: Project Scaffold
**Files:** `astro-site/package.json`, `astro.config.mjs`, `tsconfig.json`
**Description:** Create Astro project with bun, install dependencies, verify dev server starts
**Tests:** `bun dev` starts without error
**Estimated:** 30 min

```bash
mkdir astro-site && cd astro-site
bun init -y
bun add astro @astrojs/sitemap @astrojs/rss
```

### Step 2: Portfolio CSS + Base Layout
**Files:** `src/styles/global.css`, `src/layouts/BaseLayout.astro`
**Description:** Copy CSS from metacortex-portfolio.html into global.css. Create BaseLayout with `<html>`, `<head>` (meta, GA, sitemap), `<body>`.
**Tests:** Build succeeds, CSS loads
**Estimated:** 1 hour

### Step 3: Data Files
**Files:** `src/data/*.json`
**Description:** Extract author, experience, skills, projects, navigation, social data from Hugo config into JSON files
**Tests:** JSON is valid, all fields populated
**Dependencies:** Step 2
**Estimated:** 1 hour

### Step 4: Homepage Components
**Files:** `src/components/*.astro`, `src/pages/index.astro`
**Description:** Build Nav, Hero, ProjectsGrid, SkillsGrid, ExperienceTimeline, Contact, Footer components. Wire into index.astro.
**Tests:** `bun dev` shows portfolio homepage matching metacortex-portfolio.html
**Dependencies:** Step 2, Step 3
**Estimated:** 3-4 hours

### Step 5: Blog Content Migration
**Files:** `scripts/migrate-posts.mjs`, `src/content/config.ts`, `src/content/post/*.md`
**Description:** Write migration script to copy 38 posts, normalise frontmatter (handle both formats), skip drafts. Set up Content Collection schema.
**Tests:** `astro check` passes for all posts; all 38 render in dev
**Dependencies:** Step 2
**Estimated:** 2 hours

### Step 6: Blog Pages
**Files:** `src/pages/post/index.astro`, `src/pages/post/[...slug].astro`, `src/components/BlogCard.astro`
**Description:** Blog listing page and individual post page. Add reading time, date formatting, back link.
**Tests:** All 38 posts accessible at their URLs
**Dependencies:** Step 5
**Estimated:** 2 hours

### Step 7: Projects, Publications, Talks Pages
**Files:** `src/content/project/*.md`, `src/content/event/*.md`, `src/pages/projects/*.astro`, `src/pages/publications.astro`, `src/pages/talks/*.astro`
**Description:** Migrate project and event content. Create listing and detail pages.
**Tests:** All sections render
**Dependencies:** Step 2
**Estimated:** 2 hours

### Step 8: Static Assets + RSS + Sitemap
**Files:** `public/` (copy from `static/`), RSS feed config, sitemap config
**Description:** Copy all static assets. Configure `@astrojs/rss` for feed. Enable `@astrojs/sitemap`.
**Tests:** RSS feed valid, sitemap generates, all assets load
**Dependencies:** Step 6, Step 7
**Estimated:** 1 hour

### Step 9: CI/CD Pipeline
**Files:** `.github/workflows/deploy-astro-r2.yml`
**Description:** Adapt existing Zola R2 workflow for Astro. Replace Zola build with `bun install && bun run build`. Same R2 sync step.
**Tests:** Push triggers workflow, deployment succeeds
**Dependencies:** Step 8
**Estimated:** 1 hour

### Step 10: URL Redirect Map
**Files:** `astro.config.mjs` (redirects)
**Description:** Compare Hugo URL patterns with Astro output. Add redirects in `astro.config.mjs` for any mismatched URLs.
**Tests:** Old URLs redirect correctly
**Dependencies:** Step 6
**Estimated:** 30 min

## Rollback Plan

1. Keep Hugo content untouched in repo during migration
2. Keep AWS deployment active until Astro site is verified
3. DNS switch to R2 is the point of no return - only do after verification
4. If R2 deployment fails, point DNS back to CloudFront

## Migration Script Design

### migrate-posts.mjs

```
Input:  content/post/*.md (Hugo posts)
Output: astro-site/src/content/post/*.md (Astro posts)

For each .md file:
1. Parse YAML frontmatter
2. Normalise fields:
   - tags: string -> string[] (split on comma)
   - date: keep as-is (Z-coerce in schema)
   - aliases: preserve for redirect mapping
   - Remove Hugo-specific fields (lastmod, username, type, weight)
   - Add draft: false if not present
3. Skip files matching draft__*
4. Write to output with clean frontmatter
5. Copy body unchanged
```

## Dependencies

### New Dependencies

| Package | Version | Justification |
|---------|---------|---------------|
| astro | ^5.x | Core framework |
| @astrojs/sitemap | latest | Sitemap generation |
| @astrojs/rss | latest | RSS feed generation |
| @astrojs/check | latest | Type checking |

### No Additional Dependencies

No CSS framework, no JS framework, no image processing, no search library.

## Performance Considerations

### Expected Performance

| Metric | Target | Measurement |
|--------|--------|-------------|
| Build time | <10s | `time bun run build` |
| Page weight (homepage) | <100KB | Lighthouse |
| Lighthouse score | >90 | Lighthouse CI |
| First contentful paint | <1.5s | WebPageTest |

### Why These Targets Are Achievable

- Astro ships zero JS by default (island architecture)
- CSS is ~5KB minified (from portfolio HTML)
- No images except avatar.jpg (33KB)
- No framework runtime (no React/Vue/Svelte)

## Open Items

| Item | Status | Owner |
|------|--------|-------|
| Should portfolio homepage show 4 projects (from HTML) or 1 (from content)? | Pending | Alex |
| Should old `/post/slug/` URLs use trailing slash? | Pending (Astro default: yes) | Alex |
| Confirm Google Analytics ID still valid | Pending | Alex |
| Verify Cloudflare R2 bucket exists or needs creation | Pending | Alex |

## Approval

- [ ] Technical review complete
- [ ] Test strategy approved
- [ ] Performance targets agreed
- [ ] Human approval received

---

## Summary of 10 Steps

| Step | Description | Effort | Dependencies |
|------|-------------|--------|-------------|
| 1 | Project scaffold (Astro + Bun) | 30 min | None |
| 2 | Portfolio CSS + BaseLayout | 1 hr | Step 1 |
| 3 | Data files (JSON) | 1 hr | Step 1 |
| 4 | Homepage components | 3-4 hr | Steps 2, 3 |
| 5 | Blog content migration | 2 hr | Step 2 |
| 6 | Blog pages | 2 hr | Step 5 |
| 7 | Projects, Publications, Talks | 2 hr | Step 2 |
| 8 | Static assets + RSS + sitemap | 1 hr | Steps 6, 7 |
| 9 | CI/CD pipeline (R2) | 1 hr | Step 8 |
| 10 | URL redirect map | 30 min | Step 6 |

**Total estimated effort**: 14-16 hours (3-4 working days)
