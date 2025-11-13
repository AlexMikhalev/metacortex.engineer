#!/usr/bin/env python3
"""
Script to migrate Hugo Academic/Wowchemy content to Zola-Academic format.
Handles frontmatter conversion from YAML to TOML and content organization.
"""

import os
import re
import yaml
from pathlib import Path
from datetime import datetime
import shutil

class HugoToZolaMigrator:
    def __init__(self, hugo_root, zola_root):
        self.hugo_root = Path(hugo_root)
        self.zola_root = Path(zola_root)

    def parse_hugo_frontmatter(self, content):
        """Extract YAML frontmatter and content from Hugo markdown file."""
        # Match YAML frontmatter between --- delimiters
        yaml_pattern = re.compile(r'^---\s*\n(.*?)\n---\s*\n(.*)', re.DOTALL)
        match = yaml_pattern.match(content)

        if match:
            try:
                frontmatter = yaml.safe_load(match.group(1))
                body = match.group(2)
                return frontmatter, body
            except yaml.YAMLError as e:
                print(f"YAML parsing error: {e}")
                return None, content
        return None, content

    def convert_to_toml_frontmatter(self, frontmatter, content_type="post"):
        """Convert Hugo YAML frontmatter to Zola TOML frontmatter."""
        toml_lines = ["+++"]

        # Required fields
        if 'title' in frontmatter:
            title = frontmatter['title'].replace('"', '\\"')
            toml_lines.append(f'title = "{title}"')

        if 'date' in frontmatter:
            date = frontmatter['date']
            if isinstance(date, datetime):
                date_str = date.strftime('%Y-%m-%d')
            else:
                date_str = str(date).split('T')[0] if 'T' in str(date) else str(date)
            toml_lines.append(f'date = {date_str}')

        # Optional fields
        if 'description' in frontmatter or 'summary' in frontmatter:
            desc = frontmatter.get('description') or frontmatter.get('summary', '')
            if desc:
                desc = desc.replace('"', '\\"').replace('\n', ' ')
                toml_lines.append(f'description = "{desc}"')

        if 'draft' in frontmatter:
            toml_lines.append(f'draft = {str(frontmatter["draft"]).lower()}')

        # Handle taxonomies
        taxonomies = []
        if 'tags' in frontmatter and frontmatter['tags']:
            tags = frontmatter['tags']
            if isinstance(tags, list):
                tags_str = ', '.join([f'"{tag}"' for tag in tags])
                taxonomies.append(f'tags = [{tags_str}]')
            elif isinstance(tags, str):
                # Handle comma-separated string
                tags_list = [t.strip() for t in tags.split(',')]
                tags_str = ', '.join([f'"{tag}"' for tag in tags_list])
                taxonomies.append(f'tags = [{tags_str}]')

        if 'categories' in frontmatter and frontmatter['categories']:
            cats = frontmatter['categories']
            if isinstance(cats, list):
                cats_str = ', '.join([f'"{cat}"' for cat in cats])
                taxonomies.append(f'categories = [{cats_str}]')

        if taxonomies:
            toml_lines.append('\n[taxonomies]')
            toml_lines.extend(taxonomies)

        # Extra fields for specific content types
        extra_fields = {}

        # Publication-specific fields
        if content_type == "publication":
            if 'authors' in frontmatter:
                authors = frontmatter['authors']
                if isinstance(authors, list):
                    authors_str = ', '.join([f'"{a}"' for a in authors])
                    extra_fields['authors'] = f'[{authors_str}]'

            if 'publication' in frontmatter:
                pub = frontmatter['publication'].replace('"', '\\"')
                extra_fields['publication'] = f'"{pub}"'

            if 'publication_short' in frontmatter:
                pub_short = frontmatter['publication_short'].replace('"', '\\"')
                extra_fields['publication_short'] = f'"{pub_short}"'

        # Project-specific fields
        if content_type == "project":
            if 'external_link' in frontmatter:
                extra_fields['external_link'] = f'"{frontmatter["external_link"]}"'

            if 'image' in frontmatter and isinstance(frontmatter['image'], dict):
                if 'filename' in frontmatter['image']:
                    extra_fields['image'] = f'"/img/{frontmatter["image"]["filename"]}"'

        # Links (for publications and projects)
        links = {}
        if 'url_pdf' in frontmatter:
            links['pdf'] = f'"{frontmatter["url_pdf"]}"'
        if 'url_code' in frontmatter:
            links['code'] = f'"{frontmatter["url_code"]}"'
        if 'url_slides' in frontmatter:
            links['slides'] = f'"{frontmatter["url_slides"]}"'
        if 'url_video' in frontmatter:
            links['video'] = f'"{frontmatter["url_video"]}"'

        # Add extra section if needed
        if extra_fields or links:
            toml_lines.append('\n[extra]')
            for key, value in extra_fields.items():
                toml_lines.append(f'{key} = {value}')
            for key, value in links.items():
                toml_lines.append(f'{key} = {value}')

        toml_lines.append('+++')
        return '\n'.join(toml_lines)

    def migrate_posts(self):
        """Migrate blog posts from Hugo to Zola."""
        hugo_posts = self.hugo_root / 'content' / 'post'
        zola_posts = self.zola_root / 'content' / 'posts'

        if not hugo_posts.exists():
            print(f"No posts directory found at {hugo_posts}")
            return

        # Create _index.md for posts section
        index_content = """+++
title = "Blog Posts"
sort_by = "date"
template = "posts.html"
page_template = "post.html"
+++

Latest articles and technical posts.
"""
        (zola_posts / '_index.md').write_text(index_content)

        migrated = 0
        for post_file in hugo_posts.rglob('*.md'):
            if post_file.name == '_index.md':
                continue

            try:
                content = post_file.read_text(encoding='utf-8')
                frontmatter, body = self.parse_hugo_frontmatter(content)

                if frontmatter:
                    toml_fm = self.convert_to_toml_frontmatter(frontmatter, "post")
                    new_content = f"{toml_fm}\n\n{body}"

                    # Create output filename
                    output_file = zola_posts / post_file.name
                    output_file.write_text(new_content, encoding='utf-8')
                    migrated += 1
                    print(f"✓ Migrated post: {post_file.name}")
            except Exception as e:
                print(f"✗ Error migrating {post_file.name}: {e}")

        print(f"\n📝 Migrated {migrated} blog posts")

    def migrate_projects(self):
        """Migrate projects from Hugo to Zola."""
        hugo_projects = self.hugo_root / 'content' / 'project'
        zola_projects = self.zola_root / 'content' / 'projects'

        if not hugo_projects.exists():
            print(f"No projects directory found at {hugo_projects}")
            return

        # Create _index.md for projects section
        index_content = """+++
title = "Projects"
sort_by = "date"
template = "projects.html"
page_template = "project.html"
+++

Portfolio of technical projects and research work.
"""
        (zola_projects / '_index.md').write_text(index_content)

        migrated = 0
        for project_dir in hugo_projects.iterdir():
            if not project_dir.is_dir():
                continue

            index_file = project_dir / 'index.md'
            if not index_file.exists():
                continue

            try:
                content = index_file.read_text(encoding='utf-8')
                frontmatter, body = self.parse_hugo_frontmatter(content)

                if frontmatter:
                    toml_fm = self.convert_to_toml_frontmatter(frontmatter, "project")
                    new_content = f"{toml_fm}\n\n{body}"

                    # Create output filename using directory name
                    output_file = zola_projects / f"{project_dir.name}.md"
                    output_file.write_text(new_content, encoding='utf-8')
                    migrated += 1
                    print(f"✓ Migrated project: {project_dir.name}")
            except Exception as e:
                print(f"✗ Error migrating {project_dir.name}: {e}")

        print(f"\n🚀 Migrated {migrated} projects")

    def migrate_publications(self):
        """Migrate publications from Hugo to Zola."""
        hugo_pubs = self.hugo_root / 'content' / 'publication'
        zola_pubs = self.zola_root / 'content' / 'publications'

        if not hugo_pubs.exists():
            print(f"No publications directory found at {hugo_pubs}")
            return

        # Create _index.md for publications section
        index_content = """+++
title = "Publications"
sort_by = "date"
template = "publications.html"
page_template = "publication.html"
+++

Academic publications and research papers.
"""
        (zola_pubs / '_index.md').write_text(index_content)

        migrated = 0
        for pub_dir in hugo_pubs.iterdir():
            if not pub_dir.is_dir():
                continue

            index_file = pub_dir / 'index.md'
            if not index_file.exists():
                continue

            try:
                content = index_file.read_text(encoding='utf-8')
                frontmatter, body = self.parse_hugo_frontmatter(content)

                if frontmatter:
                    toml_fm = self.convert_to_toml_frontmatter(frontmatter, "publication")
                    new_content = f"{toml_fm}\n\n{body}"

                    # Create output filename
                    output_file = zola_pubs / f"{pub_dir.name}.md"
                    output_file.write_text(new_content, encoding='utf-8')
                    migrated += 1
                    print(f"✓ Migrated publication: {pub_dir.name}")
            except Exception as e:
                print(f"✗ Error migrating {pub_dir.name}: {e}")

        print(f"\n📚 Migrated {migrated} publications")

    def migrate_events(self):
        """Migrate events/talks from Hugo to Zola."""
        hugo_events = self.hugo_root / 'content' / 'event'
        zola_talks = self.zola_root / 'content' / 'talks'

        if not hugo_events.exists():
            print(f"No events directory found at {hugo_events}")
            return

        # Create _index.md for talks section
        index_content = """+++
title = "Talks & Events"
sort_by = "date"
template = "talks.html"
page_template = "talk.html"
+++

Conference talks, presentations, and events.
"""
        (zola_talks / '_index.md').write_text(index_content)

        migrated = 0
        for event_dir in hugo_events.iterdir():
            if not event_dir.is_dir():
                continue

            index_file = event_dir / 'index.md'
            if not index_file.exists():
                continue

            try:
                content = index_file.read_text(encoding='utf-8')
                frontmatter, body = self.parse_hugo_frontmatter(content)

                if frontmatter:
                    toml_fm = self.convert_to_toml_frontmatter(frontmatter, "event")
                    new_content = f"{toml_fm}\n\n{body}"

                    # Create output filename
                    output_file = zola_talks / f"{event_dir.name}.md"
                    output_file.write_text(new_content, encoding='utf-8')
                    migrated += 1
                    print(f"✓ Migrated event: {event_dir.name}")
            except Exception as e:
                print(f"✗ Error migrating {event_dir.name}: {e}")

        print(f"\n🎤 Migrated {migrated} events/talks")

def main():
    hugo_root = Path('/home/user/metacortex.engineer')
    zola_root = Path('/home/user/metacortex.engineer/zola-site')

    migrator = HugoToZolaMigrator(hugo_root, zola_root)

    print("🔄 Starting migration from Hugo to Zola...\n")
    print("=" * 60)

    print("\n📝 Migrating blog posts...")
    migrator.migrate_posts()

    print("\n🚀 Migrating projects...")
    migrator.migrate_projects()

    print("\n📚 Migrating publications...")
    migrator.migrate_publications()

    print("\n🎤 Migrating events/talks...")
    migrator.migrate_events()

    print("\n" + "=" * 60)
    print("✅ Migration complete!")
    print("\nNext steps:")
    print("1. Copy static assets: cp -r static/* zola-site/static/")
    print("2. Test build: cd zola-site && zola build")
    print("3. Preview: cd zola-site && zola serve")

if __name__ == '__main__':
    main()
