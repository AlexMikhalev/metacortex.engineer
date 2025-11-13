# Website Migration Plan: Hugo/Wowchemy → Zola-Academic + Cloudflare R2

## Executive Summary

**Goal:** Migrate from Hugo Academic/Wowchemy to Zola-Academic with Cloudflare R2 hosting

**Benefits:**
- ✅ **90% cost reduction** (R2 vs S3+CloudFront)
- ✅ **Zero egress fees** with R2
- ✅ **Simpler maintenance** (single binary, no dependencies)
- ✅ **Faster builds** (Rust-based Zola)
- ✅ **Modern design** (Bulma CSS + auto dark mode)
- ✅ **Feature parity** (publications, projects, blog, contact)

**Timeline:** 5-7 days
**Risk Level:** Low-Medium

---

## Phase 1: Cloudflare R2 Setup (Day 1)

### 1.1 Create R2 Bucket

1. Login to [Cloudflare Dashboard](https://dash.cloudflare.com)
2. Navigate to **R2 Object Storage**
3. Click **Create bucket**
   - Name: `metacortex-engineer-website`
   - Location: Automatic
4. Click **Create bucket**

### 1.2 Configure Public Access & Custom Domain

1. Go to bucket → **Settings** → **Public Access**
2. Click **Allow Access** → **Connect Domain**
3. Enter domain: `metacortex.engineer`
4. Review DNS records → Click **Connect Domain**
5. Wait 1-2 minutes for DNS propagation

**Result:** Automatic SSL + CDN + DNS configuration

### 1.3 Create Transform Rule for index.html

1. Go to domain in Cloudflare → **Rules** → **Transform Rules**
2. Click **Create rule** → **Rewrite URL**
3. Configure:
   - **Rule name:** `R2 Index HTML Routing`
   - **Field:** URI Path
   - **Operator:** ends with
   - **Value:** `/`
   - **Then:** Rewrite to → Dynamic
   - **Expression:** `concat(http.request.uri.path, "index.html")`
4. Click **Deploy**

### 1.4 Create R2 API Tokens

1. **R2** → **Manage R2 API Tokens** → **Create API Token**
2. Configure:
   - Name: `GitHub Actions Deploy`
   - Permissions: **Object Read & Write**
   - Apply to: `metacortex-engineer-website` (or all buckets)
   - TTL: Forever
3. **Save these values:**
   - Access Key ID
   - Secret Access Key
   - Account ID (from R2 dashboard URL)

### 1.5 Configure GitHub Secrets

Go to repository: **Settings** → **Secrets and variables** → **Actions**

Add secrets:
```
R2_ACCESS_KEY_ID = <access-key-id>
R2_SECRET_ACCESS_KEY = <secret-access-key>
R2_ACCOUNT_ID = <account-id>
R2_BUCKET_NAME = metacortex-engineer-website
```

**Optional (for cache purging):**
```
CLOUDFLARE_ZONE_ID = <zone-id>
CLOUDFLARE_API_TOKEN = <api-token>
```

---

## Phase 2: Zola Setup (Day 1-2)

### 2.1 Install Zola Locally

**Linux/macOS:**
```bash
# Via package manager
brew install zola                    # macOS
snap install zola --edge             # Linux

# Or via binary
curl -sL https://github.com/getzola/zola/releases/latest/download/zola-x86_64-unknown-linux-gnu.tar.gz | tar xz
sudo mv zola /usr/local/bin/
```

**Verify installation:**
```bash
zola --version
```

### 2.2 Clone Zola-Academic Example

```bash
cd /home/user/metacortex.engineer
git clone --recurse-submodules https://github.com/zola-academic/zola-academic-example zola-site
cd zola-site
```

### 2.3 Test Local Build

```bash
zola serve
# Visit http://127.0.0.1:1111
```

### 2.4 Configure Site

Edit `config.toml`:

```toml
base_url = "https://metacortex.engineer"
title = "Dr Alexander Mikhalev"
description = "AI Architect, Machine Learning & Natural Language Processing"
default_language = "en"

compile_sass = true
minify_html = true
build_search_index = true

[extra]
# Author information
author = "Dr Alexander Mikhalev"
bio = """
AI Architect specializing in Machine Learning, Natural Language Processing,
and Acoustic Source Localization. Passionate about building intelligent systems
that solve real-world problems.
"""
avatar = "/img/avatar.jpg"

# Social links
email = "your@email.com"
github = "AlexMikhalev"
twitter = "your_twitter"
scholar = "your_google_scholar_id"
linkedin = "your-linkedin"

# Theme settings
dark_mode = true
enable_search = true
enable_rss = true

# Navigation
[[extra.menu]]
name = "Home"
url = "/"

[[extra.menu]]
name = "Publications"
url = "/publications/"

[[extra.menu]]
name = "Projects"
url = "/projects/"

[[extra.menu]]
name = "Blog"
url = "/blog/"

[[extra.menu]]
name = "Contact"
url = "/contact/"
```

---

## Phase 3: Content Migration (Days 2-4)

### 3.1 Directory Structure

Create content directories:
```bash
mkdir -p content/{blog,projects,publications,talks}
mkdir -p static/{img,papers,slides}
```

### 3.2 Frontmatter Conversion

**Hugo format (current):**
```yaml
---
title: "Article Title"
date: 2022-02-06
tags: [tag1, tag2]
description: "Brief description"
---
```

**Zola format (target):**
```toml
+++
title = "Article Title"
date = 2022-02-06
description = "Brief description"

[taxonomies]
tags = ["tag1", "tag2"]
+++
```

### 3.3 Migration Script

Create `migrate_content.py`:

```python
#!/usr/bin/env python3
import os
import re
from pathlib import Path

def convert_frontmatter(content):
    """Convert Hugo YAML frontmatter to Zola TOML"""
    # Extract frontmatter
    match = re.match(r'^---\n(.*?)\n---\n(.*)', content, re.DOTALL)
    if not match:
        return content

    yaml_fm, body = match.groups()

    # Simple YAML to TOML conversion
    toml_fm = yaml_fm.replace(': ', ' = ')
    toml_fm = toml_fm.replace('[', '["').replace(']', '"]')
    toml_fm = toml_fm.replace(', ', '", "')

    # Rebuild with TOML
    return f"+++\n{toml_fm}\n+++\n{body}"

def migrate_posts():
    """Migrate blog posts from Hugo to Zola format"""
    hugo_posts = Path('content/post')
    zola_posts = Path('zola-site/content/blog')

    for post in hugo_posts.glob('**/*.md'):
        print(f"Migrating: {post.name}")
        content = post.read_text()
        converted = convert_frontmatter(content)

        output_path = zola_posts / post.name
        output_path.write_text(converted)

if __name__ == '__main__':
    migrate_posts()
    print("✅ Migration complete!")
```

Run migration:
```bash
python3 migrate_content.py
```

### 3.4 Content Type Templates

**Publications** (`content/publications/_index.md`):
```toml
+++
title = "Publications"
sort_by = "date"
template = "publications.html"
+++
```

**Single publication** (`content/publications/my-paper.md`):
```toml
+++
title = "Paper Title"
date = 2023-05-15
authors = ["Alexander Mikhalev", "Co-Author Name"]
publication = "Conference on AI"
publication_short = "CAI'23"

[extra]
pdf = "/papers/my-paper.pdf"
slides = "/slides/my-paper-slides.pdf"
code = "https://github.com/AlexMikhalev/project"
doi = "10.1234/example.doi"
+++

Abstract of the paper goes here...
```

**Projects** (`content/projects/the-pattern.md`):
```toml
+++
title = "The Pattern - ML/NLP System"
date = 2023-01-10
description = "Advanced machine learning system for pattern recognition"
featured = true

[extra]
image = "/img/projects/the-pattern.jpg"
github = "https://github.com/AlexMikhalev/the-pattern"
demo = "https://demo.example.com"
tags = ["Machine Learning", "NLP", "Python"]
+++

Detailed project description...
```

### 3.5 Copy Static Assets

```bash
# Copy images, PDFs, slides
cp -r ~/metacortex.engineer/static/* zola-site/static/

# Copy author avatar
cp ~/metacortex.engineer/content/authors/admin/avatar.jpg zola-site/static/img/avatar.jpg
```

---

## Phase 4: Legacy Content (Day 4)

### 4.1 Convert RST Archive to Markdown

```bash
# Install pandoc
sudo apt install pandoc  # or brew install pandoc

# Convert RST to Markdown
cd ~/metacortex.engineer/content/archive
for file in *.rst; do
    echo "Converting: $file"
    pandoc -f rst -t markdown "$file" \
      -o "../zola-site/content/blog/archive-$(basename $file .rst).md"
done
```

### 4.2 Add Archive Notice

Prepend to each converted file:
```markdown
> **Note:** This post was migrated from the archive and may contain outdated information.
```

---

## Phase 5: Deployment Setup (Day 5)

### 5.1 Add GitHub Actions Workflow

The workflow is already created at:
`.github/workflows/deploy-zola-r2.yml`

### 5.2 Test Build Locally

```bash
cd zola-site
zola build
ls -lh public/  # Check output
```

### 5.3 Initialize Git

```bash
cd zola-site
git init
git remote add origin https://github.com/AlexMikhalev/metacortex.engineer.git
git checkout -b zola-migration
```

### 5.4 Commit and Push

```bash
git add .
git commit -m "Migrate to Zola-Academic with Cloudflare R2 deployment"
git push -u origin zola-migration
```

---

## Phase 6: Testing & Validation (Days 6-7)

### 6.1 Build Checklist

- [ ] All blog posts render correctly
- [ ] Publications with PDFs/slides accessible
- [ ] Projects display with images
- [ ] Dark mode toggle works
- [ ] Mobile responsive design functions
- [ ] All social links work
- [ ] Search functionality operational (if enabled)
- [ ] RSS feed generates (`/rss.xml`)
- [ ] Sitemap exists (`/sitemap.xml`)
- [ ] No broken internal links

### 6.2 Performance Testing

```bash
# Test with Lighthouse
lighthouse https://metacortex.engineer --view

# Check load times
curl -w "@curl-format.txt" -o /dev/null -s https://metacortex.engineer
```

### 6.3 Cross-browser Testing

Test on:
- [ ] Chrome/Edge
- [ ] Firefox
- [ ] Safari
- [ ] Mobile browsers (iOS/Android)

---

## Phase 7: Go Live (Day 7)

### 7.1 Update DNS (if needed)

If domain is external:
1. Update CNAME to point to R2 bucket domain
2. Wait for DNS propagation (1-24 hours)

### 7.2 Merge to Main

```bash
git checkout main
git merge zola-migration
git push origin main
```

### 7.3 Monitor Deployment

Watch GitHub Actions: `https://github.com/AlexMikhalev/metacortex.engineer/actions`

### 7.4 Verify Live Site

1. Visit `https://metacortex.engineer`
2. Check all sections
3. Test dark mode
4. Verify all links
5. Check mobile version

---

## Rollback Plan

If issues occur:

### Quick Rollback

1. Revert GitHub Actions workflow:
   ```bash
   git revert HEAD
   git push origin main
   ```

2. Point DNS back to old S3+CloudFront (if needed)

### Full Rollback

1. Restore `.github/workflows/main.yml` (old workflow)
2. Push to master branch
3. AWS deployment resumes automatically

---

## Cost Comparison

### Current: AWS S3 + CloudFront

```
Storage (10GB):          $0.23/month
Requests (10k):          $0.05/month
Data transfer (100GB):   $8.50/month
CloudFront (100GB):      $8.50/month
TOTAL:                   ~$17.28/month
```

### New: Cloudflare R2

```
Storage (10GB):          $0.15/month
Requests (10k):          $0.36/month
Data transfer (100GB):   $0.00 (FREE!)
CDN (unlimited):         $0.00 (FREE!)
TOTAL:                   ~$0.51/month
```

**💰 Savings: ~$200/year (97% reduction!)**

---

## Maintenance Plan

### Weekly
- [ ] Check GitHub Actions status
- [ ] Monitor site performance

### Monthly
- [ ] Review R2 costs (should be minimal)
- [ ] Check for Zola updates: `zola --version`
- [ ] Verify SSL certificate (auto-renews)

### Quarterly
- [ ] Update zola-academic theme:
  ```bash
  cd themes/zola-academic
  git pull origin main
  ```
- [ ] Test all site features
- [ ] Review analytics

### Annually
- [ ] Evaluate Zola version upgrade
- [ ] Review content strategy
- [ ] Optimize images/assets

---

## Support & Resources

### Documentation
- Zola: https://www.getzola.org/documentation/
- Zola-Academic: https://github.com/zola-academic/zola-academic
- Cloudflare R2: https://developers.cloudflare.com/r2/

### Community
- Zola Forum: https://zola.discourse.group/
- Cloudflare Community: https://community.cloudflare.com/

### Emergency Contacts
- Cloudflare Support: https://dash.cloudflare.com/?to=/:account/support
- GitHub Support: https://support.github.com/

---

## Success Metrics

Track these after migration:

- [ ] **Performance:** PageSpeed score >90
- [ ] **Cost:** Monthly hosting <$1
- [ ] **Uptime:** >99.9%
- [ ] **Build time:** <60 seconds
- [ ] **Deploy time:** <120 seconds

---

## Next Steps

1. Review this plan
2. Create R2 bucket and configure
3. Test local Zola build
4. Migrate sample content (3-5 posts)
5. Review prototype
6. Proceed with full migration

**Estimated Total Time:** 5-7 days
**Estimated Cost Savings:** $200+/year
**Risk Level:** Low-Medium
**Recommended Approach:** Prototype first, then full migration
