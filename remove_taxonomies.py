#!/usr/bin/env python3
"""Remove taxonomies from Zola post frontmatter."""

import re
from pathlib import Path

def remove_taxonomies_from_file(file_path):
    """Remove [taxonomies] section from a file's TOML frontmatter."""
    content = file_path.read_text(encoding='utf-8')

    # Match the frontmatter
    pattern = r'(\+\+\+.*?)\n\[taxonomies\].*?(?=\n\w|\n\[|\+\+\+)(\+\+\+.*)'

    # Try to remove taxonomies section
    new_content = re.sub(
        r'(\+\+\+.*?)\n+\[taxonomies\][^\+]+(\+\+\+.*)',
        r'\1\n\2',
        content,
        flags=re.DOTALL
    )

    if new_content != content:
        file_path.write_text(new_content, encoding='utf-8')
        return True
    return False

posts_dir = Path('/home/user/metacortex.engineer/zola-site/content/posts')
fixed = 0

for post_file in posts_dir.glob('*.md'):
    if post_file.name != '_index.md':
        if remove_taxonomies_from_file(post_file):
            fixed += 1
            print(f"✓ Fixed: {post_file.name}")

print(f"\n✅ Fixed {fixed} files")
