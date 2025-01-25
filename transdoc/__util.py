"""
# Transdoc / util

Utility functions for Transdoc.
"""


def indent_by(indent: str, string: str) -> str:
    """
    Indent the given string using the given indentation.
    """
    return "\n".join(
        f"{indent}{line.rstrip()}" for line in string.splitlines()
    ).lstrip()
