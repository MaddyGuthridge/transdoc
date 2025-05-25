"""# Transdoc / Tests / Rules / Attributes Test

Test cases for Transdoc's built-in `attributes` rule.
"""

from textwrap import dedent
from typing import Any

from transdoc import TransdocTransformer
from transdoc.rules import (
    python_object_attributes,
    python_object_attributes_rule_gen,
)


class Example:
    """{{attributes("tests.rules.attributes_test", "Example")}}
    """

    some_attribute = "value"

    def __init__(self) -> None:
        raise NotImplementedError()

    def some_fn(self):
        raise NotImplementedError()


def test_class_attributes():
    transformer = TransdocTransformer({"attributes": python_object_attributes})

    EXPECTED = dedent(
        """
        * some_attribute
        * some_fn
        """.lstrip("\n").rstrip(),
    )
    assert (
        transformer.transform(
            "{{attributes('tests.rules.attributes_test', 'Example')}}",
            "<string>",
        )
        == EXPECTED
    )


def test_module_attrs():
    transformer = TransdocTransformer({"attributes": python_object_attributes})

    expected = dedent(
        """
        * hello
        """.lstrip("\n").rstrip(),
    )
    assert (
        transformer.transform(
            "{{attributes('tests.data.module')}}",
            "<string>",
        )
        == expected
    )


def test_custom_filter():
    def filter_attrs(name: str, ref: Any) -> bool:
        return name == "__init__"

    transformer = TransdocTransformer(
        {"attributes": python_object_attributes_rule_gen(filter=filter_attrs)},
    )

    EXPECTED = dedent(
        """
        * __init__
        """.lstrip("\n").rstrip(),
    )

    assert (
        transformer.transform(
            "{{attributes('tests.rules.attributes_test', 'Example')}}",
            "<string>",
        )
        == EXPECTED
    )


def test_custom_formatter():
    def format_attrs(
        module: str, object: str | None, attribute: str,
    ) -> str:
        return f"{module}.{object}.{attribute}"

    transformer = TransdocTransformer(
        {
            "attributes": python_object_attributes_rule_gen(
                formatter=format_attrs,
            ),
        },
    )

    EXPECTED = dedent(
        """
        tests.rules.attributes_test.Example.some_attribute
        tests.rules.attributes_test.Example.some_fn
        """.lstrip("\n").rstrip(),
    )

    assert (
        transformer.transform(
            "{{attributes('tests.rules.attributes_test', 'Example')}}",
            "<string>",
        )
        == EXPECTED
    )
