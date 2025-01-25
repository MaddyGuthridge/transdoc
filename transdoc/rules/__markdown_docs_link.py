"""
# Transdoc / Rules / Docs Link

A rule generator for generating Markdown links to a documentation site.
"""

from typing import Optional, Callable


def markdown_docs_link_rule_gen(
    base_url: str,
) -> Callable[[str, Optional[str]], str]:
    """
    Creates a rule for generating Markdown-style links to a site given a base
    URL.

    The rule can be generated using a base URL.

    ```py
    from transdoc.rules import docs_link_from_site
    docs = docs_link_from_site("https://example.com/")
    ```

    The rule can then be used as follows:

    ```md
    See documentation {{docs("some_function", "here")}}.
    ```

    Which will produce:

    ```md
    See documentation [here](https://example.com/some_function).
    ```

    Parameters
    ----------
    base_url : str
        Base URL to use for documentation site.

    Returns
    -------
    `(str, Optional[str]) -> str`
        A rule function that accepts a URL fragment and produces a
        Markdown-formatted link.
    """
    base_url = base_url.removesuffix("/")

    def markdown_docs_link(path: str, text: Optional[str] = None) -> str:
        full_url = f"{base_url}/{path}"
        if text is None:
            return f"[{full_url}]({full_url})"
        else:
            return f"[{text}]({full_url})"

    return markdown_docs_link
