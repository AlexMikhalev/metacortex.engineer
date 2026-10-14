#!/bin/bash
set -euo pipefail

DIST_DIR="astro-site/dist"
BUCKET="metacortex-engineer"

source ~/.my_cloudflare.sh
[ -n "${CLOUDFLARE_API_TOKEN:-}" ] || { echo "CLOUDFLARE_API_TOKEN is empty (is 1Password unlocked?)" >&2; exit 1; }

upload_file() {
  local file="$1"
  local key="${file#$DIST_DIR/}"
  local content_type="application/octet-stream"
  
  case "$key" in
    *.html) content_type="text/html; charset=utf-8" ;;
    *.css)  content_type="text/css; charset=utf-8" ;;
    *.js)   content_type="application/javascript; charset=utf-8" ;;
    *.xml)  content_type="application/xml; charset=utf-8" ;;
    *.txt)  content_type="text/plain; charset=utf-8" ;;
    *.json) content_type="application/json; charset=utf-8" ;;
    *.jpg|*.jpeg) content_type="image/jpeg" ;;
    *.png)  content_type="image/png" ;;
    *.webp) content_type="image/webp" ;;
    *.svg)  content_type="image/svg+xml" ;;
    *.pdf)  content_type="application/pdf" ;;
    *.docx) content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document" ;;
    *.ico)  content_type="image/x-icon" ;;
  esac

  if ! out=$(wrangler r2 object put "$BUCKET/$key" --file "$file" --content-type "$content_type" --remote 2>&1); then
    echo "FAILED $key" >&2; echo "$out" | tail -3 >&2; exit 255
  fi
  echo "  $key"
}

export -f upload_file
export DIST_DIR BUCKET

TOTAL=$(find "$DIST_DIR" -type f | wc -l | tr -d ' ')
echo "Uploading $TOTAL files to R2 bucket $BUCKET..."

find "$DIST_DIR" -type f | xargs -I{} bash -c 'upload_file "$@"' _ {}

echo "Done. Uploaded $TOTAL files."
