"""
# Tests / Conftest

Pytest configuration
"""

import pytest
from transdoc.rules import file_contents
from transdoc import TransdocTransformer


@pytest.fixture
def transformer():
    return TransdocTransformer(
        {
            "simple": simple_rule,
            "multiline": multiline_rule,
            "echo": echo_rule,
            "error": error_rule,
            "file_contents": file_contents,
        }
    )


# Simple rules


def simple_rule():
    return "Simple rule"


def multiline_rule():
    return "Multiple\nLines"


def echo_rule(value):
    return value


def error_rule(exc_type: str = "TypeError"):
    raise eval(exc_type)
