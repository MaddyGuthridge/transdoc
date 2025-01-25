"""
# Tests / Rules / Markdown docs link

Test cases for Transdoc rule for generating markdown documentation links.
"""

from transdoc.__transformer import TransdocTransformer
from transdoc.rules.__markdown_docs_link import markdown_docs_link_rule_gen


def test_creates_links():
    transformer = TransdocTransformer(
        {"docs": markdown_docs_link_rule_gen("https://example.com")}
    )

    assert (
        transformer.transform("{{docs('test', 'text')}}", "<string>")
        == "[text](https://example.com/test)"
    )


def test_creates_links_with_default_text():
    transformer = TransdocTransformer(
        {"docs": markdown_docs_link_rule_gen("https://example.com")}
    )

    assert (
        transformer.transform("{{docs[test]}}", "<string>")
        == "[https://example.com/test](https://example.com/test)"
    )


def test_handles_trailing_slash():
    transformer = TransdocTransformer(
        {"docs": markdown_docs_link_rule_gen("https://example.com/")}
    )

    assert (
        transformer.transform("{{docs[test]}}", "<string>")
        == "[https://example.com/test](https://example.com/test)"
    )
