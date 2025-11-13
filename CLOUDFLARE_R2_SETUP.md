# Cloudflare R2 Quick Setup Guide

## Why Cloudflare R2?

**Cost Comparison for 100GB monthly traffic:**
- AWS S3 + CloudFront: ~$17/month
- **Cloudflare R2: ~$0.50/month** ✅
- **Savings: 97% ($200+/year)**

**Key Benefits:**
- ✅ Zero egress fees (bandwidth is FREE)
- ✅ S3-compatible API (easy migration)
- ✅ Global CDN included
- ✅ Automatic SSL certificates
- ✅ Built-in DDoS protection
- ✅ Simple one-service setup

---

## Step-by-Step Setup

### 1. Create R2 Bucket (5 minutes)

1. Login to [Cloudflare Dashboard](https://dash.cloudflare.com)
2. Click **R2** in sidebar
3. Click **Create bucket**
   - Name: `metacortex-engineer-website`
   - Location: Automatic
4. Click **Create bucket**

### 2. Enable Public Access (2 minutes)

1. Click on your new bucket
2. Go to **Settings** tab
3. Scroll to **Public access** section
4. Click **Allow Access**
5. Click **Connect Domain**
6. Enter your domain: `metacortex.engineer`
7. Click **Connect Domain**

**What happens automatically:**
- ✅ DNS CNAME record created
- ✅ SSL certificate provisioned
- ✅ CDN configured globally
- ✅ Your site is now accessible!

### 3. Fix index.html Routing (3 minutes)

R2 doesn't auto-serve index.html. Fix with Transform Rule:

1. Go to your domain dashboard
2. Click **Rules** → **Transform Rules**
3. Click **Create rule**
4. Click **Rewrite URL**
5. Configure:

```
Rule name: R2 Index HTML Routing

When incoming requests match:
  Custom filter expression:
  (http.request.uri.path eq "/" or http.request.uri.path ends with "/")

Then:
  Rewrite to → Dynamic
  Expression: concat(http.request.uri.path, "index.html")
```

6. Click **Deploy**

**Result:** `metacortex.engineer/blog/` now serves `blog/index.html` ✅

### 4. Create API Tokens (3 minutes)

1. In R2 dashboard, click **Manage R2 API Tokens**
2. Click **Create API Token**
3. Configure:
   - Name: `GitHub Actions Deploy`
   - Permissions: **Object Read & Write**
   - Apply to: **Specific bucket** → `metacortex-engineer-website`
   - TTL: Forever
4. Click **Create API Token**

**⚠️ IMPORTANT:** Save these values immediately (shown only once):
- Access Key ID
- Secret Access Key

**Also note your Account ID:**
- Visible in R2 dashboard URL: `dash.cloudflare.com/<ACCOUNT-ID>/r2/`

### 5. Configure GitHub Secrets (2 minutes)

1. Go to your GitHub repository
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Add these four secrets:

```
Name: R2_ACCESS_KEY_ID
Value: <paste access key id>

Name: R2_SECRET_ACCESS_KEY
Value: <paste secret access key>

Name: R2_ACCOUNT_ID
Value: <paste account id>

Name: R2_BUCKET_NAME
Value: metacortex-engineer-website
```

### 6. Optional: Cache Purging (5 minutes)

To auto-clear CDN cache on deployment:

**Get Zone ID:**
1. Go to domain Overview in Cloudflare
2. Scroll to **API** section in right sidebar
3. Copy **Zone ID**

**Create API Token:**
1. Click **My Profile** (top right) → **API Tokens**
2. Click **Create Token**
3. Click **Get started** on "Custom token"
4. Configure:
   - Token name: `GitHub Actions Cache Purge`
   - Permissions:
     - Zone → Cache Purge → Purge
     - Zone → Zone → Read
   - Zone Resources:
     - Include → Specific zone → `metacortex.engineer`
5. Click **Continue to summary** → **Create Token**
6. Copy the token (shown only once)

**Add to GitHub Secrets:**
```
Name: CLOUDFLARE_ZONE_ID
Value: <paste zone id>

Name: CLOUDFLARE_API_TOKEN
Value: <paste api token>
```

---

## Deploy Workflow

The workflow at `.github/workflows/deploy-zola-r2.yml` is ready to use!

**What it does:**
1. ✅ Builds your Zola site
2. ✅ Uploads to R2 bucket
3. ✅ Sets optimal cache headers
4. ✅ Purges Cloudflare cache (if configured)
5. ✅ Shows deployment summary

**Trigger deployment:**
```bash
git push origin claude/website-migration-research-011CV55NHr1a89N9HvP59cqf
```

---

## Verify Deployment

### Check GitHub Actions
1. Go to repository → **Actions** tab
2. Watch the "Deploy Zola site to Cloudflare R2" workflow
3. Should complete in 1-3 minutes

### Check Your Site
```bash
curl -I https://metacortex.engineer
# Should return 200 OK with cloudflare headers
```

### Test Features
- [ ] Homepage loads
- [ ] Dark mode toggle works
- [ ] Blog posts accessible
- [ ] Images load
- [ ] PDF downloads work
- [ ] Mobile responsive

---

## Troubleshooting

### Error: "AccessDenied"
**Cause:** Invalid API credentials
**Fix:**
1. Regenerate R2 API token
2. Update GitHub secrets
3. Try deployment again

### Error: "NoSuchBucket"
**Cause:** Wrong bucket name or account ID
**Fix:**
1. Verify bucket name in R2 dashboard
2. Check account ID in URL
3. Update GitHub secrets

### Site Shows "NoSuchKey" Error
**Cause:** index.html routing not configured
**Fix:** Add Transform Rule (see Step 3 above)

### CSS/Images Not Loading
**Cause:** Wrong base URL in config
**Fix:** Update `config.toml`:
```toml
base_url = "https://metacortex.engineer"
```

### Cache Not Updating
**Cause:** Cloudflare CDN cache
**Fix Option 1:** Wait 1 hour (default TTL)
**Fix Option 2:** Manual purge:
1. Domain dashboard → **Caching**
2. Click **Purge Everything**

**Fix Option 3:** Add cache purge secrets (see Step 6)

---

## Monitoring & Costs

### Check R2 Costs
1. R2 dashboard → **Usage**
2. View storage & request metrics

**Expected costs:**
- Storage (10GB): ~$0.15/month
- Requests (10k): ~$0.36/month
- **Total: <$1/month**

### Monitor Performance
```bash
# Check response time
curl -w "Time: %{time_total}s\n" -o /dev/null -s https://metacortex.engineer

# Check headers
curl -I https://metacortex.engineer | grep -i "cf-"
```

### View Analytics
Cloudflare Dashboard → Your domain → **Analytics**
- Traffic metrics
- Bandwidth (all free!)
- Request count
- Geographic distribution

---

## Advanced Configuration

### Custom Cache Rules

Create cache rules for better performance:

1. Domain → **Rules** → **Cache Rules**
2. Click **Create rule**

**Example: Cache static assets longer**
```
Rule name: Cache Static Assets

When incoming requests match:
  File extension is one of: jpg png gif svg webp css js woff woff2

Then:
  Cache eligibility: Eligible for cache
  Edge TTL: 1 year
  Browser TTL: 1 year
```

### Security Headers

Add security headers with Transform Rules:

1. Domain → **Rules** → **Transform Rules** → **Modify Response Header**
2. Create rules for:
   - `X-Content-Type-Options: nosniff`
   - `X-Frame-Options: SAMEORIGIN`
   - `Referrer-Policy: strict-origin-when-cross-origin`

### Custom Error Pages

Upload custom 404 page:

```bash
# Create 404.html in Zola
# It will be deployed automatically
```

---

## Migration from S3+CloudFront

### 1. Copy Existing Content

```bash
# Sync from S3 to R2
aws s3 sync s3://old-bucket/ s3://metacortex-engineer-website/ \
  --endpoint-url https://<ACCOUNT-ID>.r2.cloudflarestorage.com \
  --source-region us-east-1
```

### 2. Update DNS

If using custom domain:
1. Update CNAME to R2 bucket domain
2. Wait for propagation (1-24 hours)
3. Test new URL

### 3. Disable Old Resources

After verifying R2 works:
1. Disable CloudFront distribution
2. Keep S3 bucket for 30 days (backup)
3. Delete S3 bucket after confirmation

---

## Best Practices

### Cache Strategy
- **HTML/XML:** 1 hour (short TTL, frequently updated)
- **CSS/JS/Images:** 1 year (immutable, versioned URLs)
- **PDFs/Downloads:** 1 month (moderate TTL)

### Security
- ✅ Use time-limited API tokens
- ✅ Rotate tokens quarterly
- ✅ Never commit secrets to git
- ✅ Use GitHub Secrets for credentials

### Performance
- ✅ Compress images before upload
- ✅ Use WebP format for images
- ✅ Minify HTML/CSS/JS
- ✅ Enable Brotli compression (auto in Cloudflare)

### Cost Optimization
- ✅ Delete old/unused files from bucket
- ✅ Use Cloudflare's image optimization
- ✅ Enable Cloudflare's Auto Minify
- ✅ Monitor usage monthly

---

## Summary

**Total Setup Time:** ~20 minutes
**Monthly Cost:** <$1 (vs $17+ for AWS)
**Performance:** Global CDN, <100ms latency
**Maintenance:** Minimal (automated deploys)

**You're all set! 🚀**

Questions? Check:
- [Cloudflare R2 Docs](https://developers.cloudflare.com/r2/)
- [GitHub Actions Docs](https://docs.github.com/en/actions)
- [Zola Documentation](https://www.getzola.org/documentation/)
