"""
# Transdoc / Transformer

Code that transforms input strings given a set of rules.
"""

from pathlib import Path

from transdoc import TransdocRule
from transdoc.source_pos import SourcePos, SourceRange
from ..transdoc.errors import (
    TransdocError,
    TransdocEvaluationError,
    TransdocSyntaxError,
    TransdocNameError,
)


def indent_by(indent: str, string: str) -> str:
    """
    Indent the given string using the given indentation.
    """
    return '\n'.join(
        [f"{indent}{line.rstrip()}" for line in string.splitlines()]
    ).lstrip()


class TransdocTransformer:
    """
    Transdoc transformer, responsible for applying rules to given inputs.
    """

    def __init__(self, rules: dict[str, TransdocRule]) -> None:
        self.__rules = rules

    def __eval_rule(
        self,
        rule: str,
        filename: Path,
        position: SourceRange,
        indent: str,
        errors: list[TransdocError],
    ) -> str:
        """
        Execute a command, alongside the given set of rules.

        Returns the output of the given command.
        """
        # String to return if an error occurred -- simply the original rule
        # string without modification.
        # This produces a string like "{{rule}}"
        # It is horrific, but it works
        # https://stackoverflow.com/a/42521252/6335363
        error_return = f"{{{{{rule}}}}}"

        def name_error(name: str):
            """Report a NameError"""
            errors.append(TransdocNameError(
                filename,
                position,
                f"Unrecognised rule name '{rule}'"
            ))
            return error_return

        def eval_error(e: Exception):
            exc = TransdocEvaluationError(
                filename,
                position,
            )
            # Associate new exception with old one
            # https://stackoverflow.com/a/54768419/6335363
            exc.__cause__ = e
            errors.append(exc)
            return error_return

        # If it's just a function name, evaluate it as a call with no arguments
        if rule.isidentifier():
            if rule not in self.__rules:
                return name_error(rule)
            try:
                return indent_by(indent, self.__rules[rule]())
            except Exception as e:
                return eval_error(e)
        # If it uses square brackets, then extract the contained string, and
        # pass that
        if rule.split('[')[0].isidentifier() and rule.endswith(']'):
            rule_name, content_str = rule.split('[', 1)
            if rule not in self.__rules:
                return name_error(rule_name)
            try:
                return indent_by(indent, self.__rules[rule_name](content_str))
            except Exception as e:
                return eval_error(e)
        # Otherwise, it should be a regular function call
        # This calls `eval` with the rules dictionary set as the globals, since
        # otherwise it'd just be too complex to parse things.
        if rule.split('(')[0].isidentifier() and rule.endswith(')'):
            if rule.split('(', 1)[0] not in self.__rules:
                return error_return
            try:
                return indent_by(indent, eval(rule, self.__rules))
            except Exception as e:
                return eval_error(e)

        # If we reach this point, it's not valid data, and we should give an
        # error
        errors.append(TransdocSyntaxError(
            filename,
            position,
            "unable to evaluate rule due to invalid syntax"
        ))
        return error_return

    def apply(
        self,
        input: str,
        filename: Path,
        position_offset: SourcePos = SourcePos(1, 1),
        indentation: str = '',
    ) -> str:
        """
        Apply the Transdoc rules to the given input, returning the result.

        Args:
            input (str): Input string to transform
            filename (Path): Path of file which the input string belongs to
            position_offset (SourcePos, optional): Source position to use when
            offsetting source positions in errors.
            indentation (str, optional): string to use for indentation (eg
            `' ' * 4` for 4 spaces, or `'\\t'` for one tab).
        """
        # TODO
        ...
