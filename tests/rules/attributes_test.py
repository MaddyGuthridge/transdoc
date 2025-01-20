"""
# Transdoc / Tests / Rules / Attributes Test

Test cases for Transdoc's built-in `attributes` rule.
"""

from transdoc import TransdocTransformer
from transdoc.rules import attributes


class Example:
    """
    {{attributes("tests.rules.attributes_test", "Example")}}
    """

    some_attribute = "value"

    def __init__(self) -> None:
        pass

    def some_fn(self):
        pass


EXPECTED = """
* some_attribute
* some_fn
""".strip()


def test_attributes():
    transformer = TransdocTransformer({"attributes": attributes})

    assert (
        transformer.transform(
            "{{attributes('tests.rules.attributes_test', 'Example')}}",
            "<string>",
        )
        == EXPECTED
    )
