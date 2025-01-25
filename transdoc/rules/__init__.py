"""
# Transdoc / Rules

This module contains definitions for some simple commonly-used rules.
"""

__all__ = [
    "file_contents",
    "python_object_attributes",
    "python_object_attributes_rule_gen",
    "markdown_docs_link_rule_gen",
]

from transdoc.rules.__file_contents import file_contents
from transdoc.rules.__attributes import (
    python_object_attributes,
    python_object_attributes_rule_gen,
)
from transdoc.rules.__markdown_docs_link import markdown_docs_link_rule_gen
