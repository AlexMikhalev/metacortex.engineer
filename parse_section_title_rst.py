#!/usr/bin/env python3
"""
some text

=====
Title
=====
Subtitle
--------

Titles are underlined (or over- and underlined) with a printing
nonalphanumeric 7-bit ASCII character. Recommended choices are "``= -
` : ' " ~ ^ _ * + # < >``".  The underline/overline must be at least
as long as the title text.

A lone top-level (sub)section is lifted up to be the document's (sub)title.
"""
from docutils.core import publish_doctree

def section_title(node):
    """Whether `node` is a section title.

    Note: it DOES NOT include document title!
    """
    try:
        return node.parent.tagname == "section" and node.tagname == "title"
    except AttributeError:
        return None # not a section title

# get document tree
doctree = publish_doctree(__doc__)
titles = doctree.traverse(condition=section_title)
print("\n".join([t.astext() for t in titles]))
