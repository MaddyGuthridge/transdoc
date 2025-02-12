"""
# Tests / Transformer test

Test cases for TransdocTransformer
"""

import pytest
from transdoc import TransdocTransformer
from transdoc.errors import (
    TransdocEvaluationError,
    TransdocNameError,
    TransdocSyntaxError,
)


###############################################################################


def test_leaves_strings_with_no_rules_as_is(transformer: TransdocTransformer):
    assert (
        transformer.transform("Text without a rule call", "<string>")
        == "Text without a rule call"
    )


def test_embeds_rule_output(transformer: TransdocTransformer):
    assert (
        transformer.transform("Call: {{simple}}", "<string>")
        == "Call: Simple rule"
    )


def test_embeds_multiple_rule_outputs(transformer: TransdocTransformer):
    assert (
        transformer.transform("Call: {{simple}} {{simple}}", "<string>")
        == "Call: Simple rule Simple rule"
    )


def test_multiline_output_rule(transformer: TransdocTransformer):
    assert (
        transformer.transform("Call: {{multiline}}", "<string>")
        == "Call: Multiple\nLines"
    )


def test_multiline_input_rule(transformer: TransdocTransformer):
    assert (
        transformer.transform("Call: {{multiline[sample\ntext]}}", "<string>")
        == "Call: Multiple\nLines sample\ntext"
    )


def test_rules_respect_indentation(transformer: TransdocTransformer):
    assert (
        transformer.transform(
            "Call: {{multiline}}", "<string>", indentation="    "
        )
        == "Call: Multiple\n    Lines"
    )


def test_rules_bracket_syntax(transformer: TransdocTransformer):
    assert (
        transformer.transform("Call: {{echo[Input text]}}", "<string>")
        == "Call: Input text"
    )


def test_rules_python_syntax(transformer: TransdocTransformer):
    assert (
        transformer.transform("Call: {{echo('Input text')}}", "<string>")
        == "Call: Input text"
    )


###############################################################################


def test_errors_unclosed_call(transformer: TransdocTransformer):
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
def test_invalid_call_syntax(transformer: TransdocTransformer, input: str):
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
def test_name_error(transformer: TransdocTransformer, input: str):
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
def test_eval_error(
    transformer: TransdocTransformer, input: str, err_type: type[Exception]
):
    with pytest.raises(ExceptionGroup) as excinfo:
        transformer.transform(input, "<string>")
    assert excinfo.group_contains(TransdocEvaluationError)
    # Ensure that exception cause is a ValueError
    assert isinstance(excinfo.value.exceptions[0].__cause__, err_type)


def test_all_errors_reported(transformer: TransdocTransformer):
    """
    When multiple errors occur when evaluating rules, are they all reported?
    """
    with pytest.raises(ExceptionGroup) as excinfo:
        transformer.transform(
            "{{undefined}} {{error[TypeError]}} {{unclosed", "<string>"
        )
    assert excinfo.group_contains(TransdocNameError)
    assert excinfo.group_contains(TransdocEvaluationError)
    assert excinfo.group_contains(TransdocSyntaxError)
    assert len(excinfo.value.exceptions) == 3
