# Research Document: Hugo/Wowchemy to Astro Migration

**Status**: Draft
**Author**: Opencode Agent
**Date**: 2026-05-30
**Reviewers**: Alex Mikhalev

## Executive Summary

Migrate metacortex.engineer from Hugo/Wowchemy (currently deployed to AWS S3+CloudFront) to Astro with the portfolio design from metacortex-portfolio.html, deployed to Cloudflare R2. The site serves as a personal portfolio and blog for Dr Alexander Mikhalev. Astro is the optimal choice because the portfolio HTML maps almost 1:1 to Astro components, while Content Collections handle blog posts naturally.

## Essential Questions Check

| Question | Answer | Evidence |
|----------|--------|----------|
| Energizing? | Yes | Combines clean portfolio design with technical blog, removes dependency on unmaintained Wowchemy theme |
| Leverages strengths? | Yes | Portfolio HTML already designed; Astro's HTML-first approach means minimal translation |
| Meets real need? | Yes | Current Hugo/Wowchemy stack is stale (Hugo 0.84, Wowchemy CMS), costs $17/mo on AWS, theme is complex to maintain |

**Proceed**: Yes (3/3)

## Problem Statement

### Description

The current site runs Hugo 0.84 with Wowchemy CMS modules, deployed to AWS S3+CloudFront. The Wowchemy theme is heavyweight, requires Go module management, and the Hugo version is severely outdated. A new portfolio design (`metacortex-portfolio.html`) exists as a standalone HTML page but has no integration with the blog content.

### Impact

- Site owner cannot easily update the site without Hugo/Wowchemy expertise
- AWS hosting costs ~$17/month for a personal site
- Hugo 0.84 is years behind current (5.x); upgrading risks breaking Wowchemy
- Portfolio design and blog content are in separate, disconnected systems

### Success Criteria

1. Portfolio homepage matching the metacortex-portfolio.html design
2. All 38 blog posts accessible at their current URLs (or redirecting)
3. Projects section with content from `content/project/`
4. Publications section with content from `content/publication/`
5. Talks/Events section with content from `content/event/`
6. Deployed to Cloudflare R2 via GitHub Actions
7. Build time under 10 seconds
8. Monthly hosting cost under $1

## Current State Analysis

### Existing Implementation

**Stack**: Hugo 0.84 (extended) + Wowchemy CMS modules + AWS S3 + CloudFront

**Content inventory**:

| Content Type | Count | Format | Location |
|-------------|-------|--------|----------|
| Blog posts | 38 | Markdown (YAML frontmatter) | `content/post/` |
| Archive posts | 98 | reStructuredText | `content/archive/` |
| Projects | 1 (The Pattern) | Markdown | `content/project/` |
| Publications | 1 (section only) | Markdown | `content/publication/` |
| Events/Talks | 5 | Markdown | `content/event/` |
| Author profile | 1 | YAML+Markdown | `content/authors/admin/` |
| Homepage widgets | 11 | YAML frontmatter | `content/home/` |

**Static assets**:

| Asset | Size | Location |
|-------|------|----------|
| Media (CV docs) | 180KB | `static/media/` |
| Slides (RedisConf, INCOSE) | 3.7MB | `static/slides/` |
| Uploads | 0 (empty) | `static/uploads/` |

**Homepage widgets** (content/home/):
- `index.md` - headless widget page
- `about.md` - biography (references admin author)
- `experience.md` - 8 career positions with dates
- `skills.md` - 9 skills with icons
- `projects.md` - portfolio widget (project page type)
- `featured.md` - featured publications widget
- `posts.md` - blog posts listing
- `publications.md` - publications listing
- `talks.md` - talks listing
- `accomplishments.md` - accomplishments
- `contact.md` - contact form
- `tags.md` - tag cloud

**Frontmatter formats observed**:

Blog posts use two distinct formats:

**Format A** (older posts):
```yaml
---
title: "Building Knowledge graph..."
author: "Alex Mikhalev"
date: 2020-04-20T19:25:51.091Z
lastmod: 2021-06-11T09:59:25+01:00
description: ""
subtitle: ""
aliases:
- "/building-knowledge-graph-...-f0178d2a19bd"
---
```

**Format B** (newer posts):
```yaml
---
title: "Microsoft releases GitHub co-pilot..."
subtitle: "It's brilliant..."
slug: microsoft-releases-github-co-pilot-ai-ethical-challenge
description:
tags: ai,data,ethics
author: Alex Mikhalev
username: alexmikhalev
date: 2021-07-07
---
```

### Code Locations

| Component | Location | Purpose |
|-----------|----------|---------|
| Hugo config | `config/_default/*.yaml` | Site configuration (4 files) |
| Content | `content/` | All site content |
| Static assets | `static/` | Images, PDFs, slides |
| Hugo modules | `go.mod`, `go.sum` | Wowchemy theme dependencies |
| GitHub Actions | `.github/workflows/` | 2 workflows (old Hugo/S3, new Zola/R2) |
| Netlify config | `netlify.toml` | Legacy deployment config |
| Portfolio design | (downloaded) `/tmp/metacortex-portfolio/metacortex-portfolio.html` | New design target |

### Integration Points

- **Google Analytics**: `G-J7D112V28F` (configured in params.yaml)
- **Domain**: `metacortex.engineer` (currently on CloudFront, will move to R2)
- **Social links**: GitHub (AlexMikhalev), LinkedIn (alexmikhalev), Patreon
- **CV/Resume**: PDF in `static/media/cv.pdf`

## Constraints

### Technical Constraints

| Constraint | Description | Source |
|-----------|-------------|--------|
| Astro framework | Must use Astro as chosen SSG | User decision |
| Portfolio design | Must match metacortex-portfolio.html aesthetic | User requirement |
| Cloudflare R2 | Must deploy to R2 (zero egress) | Cost optimisation |
| URL preservation | Blog post URLs should remain valid or redirect | SEO preservation |
| No JavaScript frameworks | Astro islands only where needed; default zero JS | Performance |

### Business Constraints

| Constraint | Description | Source |
|-----------|-------------|--------|
| Timeline | 5-7 days for complete migration | Budget constraint |
| Cost target | <$1/month hosting | Current AWS bill is ~$17/mo |
| Single maintainer | Site must be easy for one person to update | Operational reality |

### Non-Functional Requirements

| Requirement | Target | Current |
|-------------|--------|---------|
| Build time | <10s | ~5-10s (Hugo) |
| Lighthouse score | >90 | Unknown |
| Page load | <2s | Unknown |
| Monthly cost | <$1 | ~$17 |
| Dependencies | Minimal | Go modules + Wowchemy |

## Vital Few (Essentialism)

### Essential Constraints (Max 3)

| Constraint | Why It's Vital | Evidence |
|------------|----------------|----------|
| Portfolio design fidelity | The entire point of this migration is the new design | metacortex-portfolio.html was specifically created for this |
| Blog content preservation | 38 posts represent years of SEO and content investment | Posts date from 2020-2022 |
| Zero-JS default | Portfolio HTML has minimal JS; Astro should match this | metacortex-portfolio.html uses 3 small scripts |

### Eliminated from Scope

| Eliminated Item | Why Eliminated |
|----------------|----------------|
| 98 RST archive posts | Legacy content from Pelican era; can be migrated later with pandoc |
| Netlify CMS integration | Not used; Astro has no built-in CMS requirement |
| Multi-language support | Current site is English-only |
| Comment system | Not currently active |
| Full-text search | Nice-to-have; can add Pagefind later |
| Dark mode toggle | Portfolio design uses single light theme; not in original HTML |
| Publication citation export | Only 1 publication currently |
| Contact form backend | Wowchemy form was likely not functional; use email link |

## Dependencies

### Internal Dependencies

| Dependency | Impact | Risk |
|------------|--------|------|
| Hugo frontmatter schema | Must parse all 38 posts' YAML correctly | Medium - two different formats |
| Static assets (3.7MB slides) | Must copy to Astro public/ | Low - simple file copy |
| Google Analytics ID | Must configure in Astro | Low - simple config |

### External Dependencies

| Dependency | Version | Risk | Alternative |
|------------|---------|------|-------------|
| Astro | 5.x (latest) | Low | None (chosen) |
| @astrojs/sitemap | Latest | Low | Manual sitemap |
| @astrojs/rss | Latest | Low | Manual RSS |
| @astrojs/mdx | Latest | Low | Standard markdown |
| Cloudflare R2 | N/A | Low | AWS S3, Vercel, Netlify |

## Risks and Unknowns

### Known Risks

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| URL structure change breaks SEO | Medium | High | Create redirect map from old to new URLs; use Astro redirects |
| Frontmatter parsing inconsistencies | Medium | Medium | Write migration script that handles both Format A and B |
| Portfolio design breaks in Astro components | Low | Medium | Test incrementally; HTML is simple, no framework dependency |
| Cloudflare R2 misconfiguration | Low | High | Follow existing CLOUDFLARE_R2_SETUP.md from Zola research |
| Loss of Wowchemy-specific shortcodes | Medium | Low | Audit posts for shortcodes; only 1-2 posts likely affected |

### Open Questions

1. **Should blog posts live at `/post/slug/` or `/blog/slug/`?** - Current Hugo uses `/post/`. Changing to `/blog/` breaks URLs unless redirects are set up. Recommend keeping `/post/`.
2. **Should we use hash-based navigation (#about, #projects) from portfolio HTML, or separate pages?** - Portfolio uses single-page with anchor links. Blog posts need separate pages. Recommend hybrid: single-page homepage + `/post/*` for blog.
3. **Draft posts** - 2 draft posts exist (`draft__*.md`). Include or exclude? Recommend exclude.
4. **RST archive** - 98 RST files. Defer to phase 2 or never?

### Assumptions Explicitly Stated

| Assumption | Basis | Risk if Wrong | Verified? |
|------------|-------|---------------|-----------|
| Astro Content Collections can handle both frontmatter formats | Astro is flexible with frontmatter parsing | Migration script needed to normalise | Partially |
| Portfolio CSS works as-is in Astro | It's vanilla CSS with CSS custom properties | Minimal risk - CSS is universal | Yes |
| Cloudflare R2 setup from Zola research applies | Same S3-compatible API | R2 config is the same regardless of SSG | Yes |
| Blog posts don't use Wowchemy shortcodes | Most posts are plain markdown | Shortcode content would render as raw text | Needs verification |

### Multiple Interpretations Considered

| Interpretation | Implications | Why Chosen/Rejected |
|----------------|--------------|---------------------|
| Single-page site (all content on homepage) | Blog posts inline; poor UX for 38 posts | Rejected - blog needs individual pages |
| Hybrid: portfolio homepage + blog section | Best of both worlds; portfolio design for homepage, blog listing at `/post/` | Chosen - matches both the portfolio design and content needs |
| Separate portfolio + blog sites | Two deployments, two domains | Rejected - unnecessary complexity |

## Research Findings

### Key Insights

1. **Frontmatter is inconsistent** - Two distinct YAML formats across the 38 blog posts. A migration script must handle both.
2. **Content is richer than the portfolio HTML** - Experience (8 positions), skills (9 items), education (2 degrees), social links, organisations all exist in Hugo data but the portfolio HTML hardcodes a subset. The Astro version should be data-driven.
3. **Portfolio HTML is almost already an Astro page** - The structure maps directly: `nav` -> Nav component, `section.hero` -> Hero component, etc. Minimal translation needed.
4. **The Zola research branch has R2 deployment figured out** - The existing `deploy-zola-r2.yml` workflow can be adapted for Astro with minimal changes (replace `zola build` with `npm run build`).
5. **Only 1 project and 1 publication** - The portfolio HTML shows 4 projects (hardcoded). Real content has 1 project. Need to decide: use real content only, or augment with portfolio HTML's additional entries.

### Relevant Prior Art

- **Astro Portfolio Themes**: Astro has several portfolio/blog starters (`astro-theme-portfolio`, `astro-blog-template`) that demonstrate the hybrid pattern
- **Hugo-to-Astro migration**: Well-documented pattern; frontmatter stays YAML, templates become `.astro` files
- **Cloudflare R2 + GitHub Actions**: Existing workflow in this repo handles it; just swap build step

### Technical Spikes Needed

| Spike | Purpose | Estimated Effort |
|-------|---------|------------------|
| Astro project scaffold | Verify Astro 5.x works with Bun, confirm Content Collections setup | 30 min |
| Portfolio HTML -> Astro components | Validate that the portfolio CSS/components work in Astro with zero breakage | 1 hour |
| Frontmatter migration script | Write Python/Bun script to normalise both YAML formats to a single Astro-compatible schema | 2 hours |
| URL redirect mapping | Determine exact URL patterns Hugo generates vs Astro, create redirect map | 1 hour |

## Recommendations

### Proceed/No-Proceed

**Proceed**. All essential constraints are met, risks are manageable, and the migration path is clear.

### Scope Recommendations

1. **Phase 1**: Portfolio homepage (nav, hero, projects grid, skills, experience timeline, contact, footer)
2. **Phase 2**: Blog section with Content Collections (all 38 posts)
3. **Phase 3**: Projects, Publications, Talks sections
4. **Phase 4**: CI/CD pipeline (adapt existing R2 workflow)
5. **Deferred**: RST archive (98 files), full-text search, dark mode

### Risk Mitigation Recommendations

1. Run the migration script on all 38 posts and validate frontmatter before any manual editing
2. Audit blog posts for Wowchemy shortcodes (`{{< >}}`) before migration
3. Deploy to a staging URL first (R2 supports custom domains)
4. Keep the Hugo site on AWS until the Astro site is verified live

## Next Steps

If approved:
1. Phase 2: Disciplined Design - produce detailed implementation plan with file map, component architecture, and step sequence
2. Create Astro project scaffold
3. Build portfolio homepage components
4. Migrate blog content
5. Set up deployment pipeline

## Appendix

### Hugo URL Patterns (current)

Based on Hugo config:
- Blog posts: `/post/{slug}/` (defined by permalink pattern)
- Events/Talks: `/talk/{slug}/`
- Tags: `/tag/{slug}/`
- Categories: `/category/{slug}/`
- Publications: `/publication-type/{slug}/`
- Projects: `/project/{slug}/`

### Portfolio HTML Structure

```
nav (fixed, blurred background)
  logo (triangle icon + METACORTEX)
  nav-links (About, Projects, Skills, Experience, Contact)
section.hero (full viewport, grid-pattern bg)
  h1, subtitle, description, CTA buttons
section#projects
  projects-grid (4 cards: The Pattern, MetaCortex AI, Terraphim AI, Blockchain)
section#skills
  skills-container (4 categories x 4 skills each with dot-level indicators)
section#experience
  experience-timeline (4 achievements)
section#contact
  contact-content (2-column: info + interests)
footer
```

### Author Data (from content/authors/admin/_index.md)

- Name: Dr Alexander Mikhalev
- Role: AI/ML Architect
- Organisations: Nationwide Building Society, Applied Knowledge Systems
- Bio: Experienced Technology Leader and Innovator...
- Interests: ML/AI, Information Retrieval, NLP, Data Fusion, Distributed Systems, Data Privacy, Digital Twin, Cyber-Physical Systems
- Education: PhD (Cranfield, 2010), MSc (MSTU Bauman, 2002)
- Social: GitHub, LinkedIn, Patreon, Email, CV

### Experience Data (8 positions)

1. Tech Lead/AI/ML Architect - Nationwide (2018-present)
2. Head of Prototyping Engineering - Nationwide (2017-2018)
3. Tech Lead - Nationwide (2014-2017)
4. Head of Architecture and Development - Shopitize (2011-2014)
5. Research Fellow - Cranfield University (2007-2009)
6. IT/IS Executive - Microsharp/Durand (2003-2007)
7. Co-founder/Editor-in-chief - samag.ru (2002-2003)
8. Various Engineering/Web Dev - Multiple companies (1999-2002)
