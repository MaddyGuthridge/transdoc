"""
# Tests / Transform test

Test cases for TransdocTransformer
"""

import pytest
from transdoc import TransdocTransformer
from transdoc.errors import (
    TransdocEvaluationError,
    TransdocNameError,
    TransdocSyntaxError,
)


def simple_rule():
    return "Simple rule"


def multiline_rule():
    return "Multiple\nLines"


def echo_rule(value):
    return value


def error_rule(exc_type: str = "TypeError"):
    raise eval(exc_type)


def make_transformer():
    return TransdocTransformer(
        {
            "simple": simple_rule,
            "multiline": multiline_rule,
            "echo": echo_rule,
            "error": error_rule,
        }
    )


###############################################################################


def test_leaves_strings_with_no_rules_as_is():
    transformer = make_transformer()
    assert (
        transformer.transform("Text without a rule call", "<string>")
        == "Text without a rule call"
    )


def test_embeds_rule_output():
    transformer = make_transformer()
    assert (
        transformer.transform("Call: {{simple}}", "<string>")
        == "Call: Simple rule"
    )


def test_multiline_rule():
    transformer = make_transformer()
    assert (
        transformer.transform("Call: {{multiline}}", "<string>")
        == "Call: Multiple\nLines"
    )


def test_rules_respect_indentation():
    transformer = make_transformer()
    assert (
        transformer.transform(
            "Call: {{multiline}}", "<string>", indentation="    "
        )
        == "Call: Multiple\n    Lines"
    )


def test_rules_bracket_syntax():
    transformer = make_transformer()
    assert (
        transformer.transform("Call: {{echo[Input text]}}", "<string>")
        == "Call: Input text"
    )


def test_rules_python_syntax():
    transformer = make_transformer()
    assert (
        transformer.transform("Call: {{echo('Input text')}}", "<string>")
        == "Call: Input text"
    )


###############################################################################


def test_errors_unclosed_call():
    transformer = make_transformer()
    with pytest.raises(ExceptionGroup) as excinfo:
        transformer.transform("{{Unclosed", "<string>")
    assert excinfo.group_contains(TransdocSyntaxError)


@pytest.mark.parametrize(
    "input",
    [
        "{{echo(}}",
        "{{echo[input}}",
        "{{echo'input'}}",
    ],
)
def test_invalid_call_syntax(input: str):
    transformer = make_transformer()
    with pytest.raises(ExceptionGroup) as excinfo:
        transformer.transform(input, "<string>")
    assert excinfo.group_contains(TransdocSyntaxError)


@pytest.mark.parametrize(
    "input",
    [
        "{{undefined}}",
        "{{undefined[input]}}",
        "{{undefined('input')}}",
    ],
)
def test_name_error(input: str):
    transformer = make_transformer()
    with pytest.raises(ExceptionGroup) as excinfo:
        transformer.transform(input, "<string>")
    assert excinfo.group_contains(TransdocNameError)


@pytest.mark.parametrize(
    ("input", "err_type"),
    [
        ("{{error}}", TypeError),
        ("{{error[ValueError]}}", ValueError),
        ("{{error('ValueError')}}", ValueError),
    ],
)
def test_eval_error(input, err_type):
    transformer = make_transformer()
    with pytest.raises(ExceptionGroup) as excinfo:
        transformer.transform(input, "<string>")
    assert excinfo.group_contains(TransdocEvaluationError)
    # Ensure that exception cause is a ValueError
    assert isinstance(excinfo.value.exceptions[0].__cause__, err_type)


def test_all_errors_reported():
    """
    When multiple errors occur when evaluating rules, are they all reported?
    """
    transformer = make_transformer()
    with pytest.raises(ExceptionGroup) as excinfo:
        transformer.transform(
            "{{undefined}} {{error[TypeError]}} {{unclosed", "<string>"
        )
    assert excinfo.group_contains(TransdocNameError)
    assert excinfo.group_contains(TransdocEvaluationError)
    assert excinfo.group_contains(TransdocSyntaxError)
    assert len(excinfo.value.exceptions) == 3
