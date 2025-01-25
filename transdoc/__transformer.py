"""
# Transdoc / Transformer

Code that transforms input strings given a set of rules.
"""

from io import StringIO
import re

from transdoc import TransdocRule
from transdoc.source_pos import SourcePos, SourceRange
from transdoc.errors import (
    TransdocTransformationError,
    TransdocEvaluationError,
    TransdocSyntaxError,
    TransdocNameError,
)


def indent_by(indent: str, string: str) -> str:
    """
    Indent the given string using the given indentation.
    """
    return "\n".join(
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
        filename: str,
        position: SourceRange,
        indent: str,
    ) -> str:
        """
        Execute a command, alongside the given set of rules.

        Returns the output of the given command.
        """

        def name_error(name: str):
            """Report a NameError"""
            return TransdocNameError(
                filename, position, f"Unrecognised rule name '{rule}'"
            )

        def eval_error():
            return TransdocEvaluationError(
                filename,
                position,
                "An error occurred while evaluating the rule",
            )

        # If it's just a function name, evaluate it as a call with no arguments
        if rule.isidentifier():
            if rule not in self.__rules:
                raise name_error(rule)
            try:
                return indent_by(indent, self.__rules[rule]())
            except Exception as e:
                raise eval_error() from e
        # If it uses square brackets, then extract the contained string, and
        # pass that
        if rule.split("[")[0].isidentifier() and rule.endswith("]"):
            rule_name, content_str = rule.split("[", 1)
            # Remove final `]`
            content_str = content_str[:-1]
            if rule_name not in self.__rules:
                raise name_error(rule_name)
            try:
                return indent_by(indent, self.__rules[rule_name](content_str))
            except Exception as e:
                raise eval_error() from e
        # Otherwise, it should be a regular function call
        # This calls `eval` with the rules dictionary set as the globals, since
        # otherwise it'd just be too complex to parse things.
        if rule.split("(")[0].isidentifier() and rule.endswith(")"):
            rule_name = rule.split("(", 1)[0]
            if rule_name not in self.__rules:
                raise name_error(rule_name)
            try:
                return indent_by(indent, eval(rule, self.__rules))
            except Exception as e:
                raise eval_error() from e

        # If we reach this point, it's not valid data, and we should give an
        # error
        raise TransdocSyntaxError(
            filename, position, "unable to evaluate rule due to invalid syntax"
        )

    def transform(
        self,
        input: str,
        filename: str,
        position_offset: SourcePos = SourcePos(1, 1),
        indentation: str = "",
    ) -> str:
        """
        Apply the Transdoc rules to the given input, returning the result.

        Args:
            input (str): Input string to transform
            filename (str): Name of file which the input string belongs to,
            used in error reporting.
            position_offset (SourcePos, optional): Source position to use when
            offsetting source positions in errors.
            indentation (str, optional): string to use for indentation (eg
            `' ' * 4` for 4 spaces, or `'\\t'` for one tab).
        """
        errors: list[TransdocTransformationError] = []

        # Match rule calls
        # \{\{  => opening '{{'
        # .+?   => any characters, non-greedy to avoid matching the entire
        #          input (including new-lines due to `re.DOTALL`)
        # \}\}  => closing '}}'
        rule_call_regex = re.compile(r"\{\{.+?\}\}", re.DOTALL)

        # Output buffer
        output = StringIO()

        # Position within input string, used for adding to output buffer
        input_pos = 0

        for match in rule_call_regex.finditer(input):
            # Rule call, excluding leading '{{' and trailing '}}'
            rule_call = match.group(0)[2:-2]
            start = position_offset.offset_by_str(indentation[: match.start()])
            end = position_offset.offset_by_str(indentation[: match.end()])

            # Add non-matched input to output
            output.write(input[input_pos : match.start()])
            input_pos = match.end()

            try:
                output.write(
                    self.__eval_rule(
                        rule_call,
                        filename,
                        SourceRange(start, end),
                        indentation,
                    )
                )
            except TransdocTransformationError as e:
                errors.append(e)

        # Finally, write remaining string
        output.write(input[input_pos:])

        # Check for un-closed instances of {{
        # Derived from: https://stackoverflow.com/a/406408/6335363
        # \{\{          => opening '{{'
        # (?!\}\})      => fail when encountering a closing `}}`
        # ((?!\}\}).)*  => repeatedly check for closing `}}` matching all chars
        #                  until it is found
        # $             => end of string
        unclosed_regex = re.compile(
            r"\{\{((?!\}\}).)*$",
            re.MULTILINE | re.DOTALL,
        )
        if unclosed := unclosed_regex.search(input):
            unclosed_pos = position_offset.offset_by_str(
                input[: unclosed.start()]
            )
            range = SourceRange(unclosed_pos, unclosed_pos + SourcePos(0, 2))
            errors.append(
                TransdocSyntaxError(
                    filename,
                    range,
                    "Unclosed rule call. Did you forget a closing '}}'?",
                )
            )

        if len(errors):
            raise ExceptionGroup(
                "Errors occurred while transforming string", errors
            )

        output.seek(0)
        return output.read()
