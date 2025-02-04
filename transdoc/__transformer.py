"""
# Transdoc / Transformer

Code that transforms input strings given a set of rules.
"""

import sys
import importlib.util
from io import StringIO
from pathlib import Path
import re
from typing import Any

from transdoc import TransdocRule
from transdoc.util import indent_by
from transdoc.source_pos import SourcePos, SourceRange
from transdoc.errors import (
    TransdocTransformationError,
    TransdocEvaluationError,
    TransdocSyntaxError,
    TransdocNameError,
)


class TransdocTransformer:
    """
    Transdoc transformer, responsible for applying rules to given inputs.
    """

    def __init__(self, rules: dict[str, TransdocRule]) -> None:
        """
        Create an instance of a TransdocTransformer, given the given rule-set.

        Parameters
        ----------
        rules : dict[str, TransdocRule]
            Dictionary, mapping between rule names, and their corresponding
            functions.
        """
        self.__rules = rules

    def __repr__(self) -> str:
        return f"TransdocTransformer({self.__rules})"

    @classmethod
    def from_file(cls, rule_file: Path) -> "TransdocTransformer":
        """
        Create a TransdocTransformer by loading rules from a Python file.

        Items are considered to be rules if they are callable, and if they are
        contained within the module's `__all__` attribute (if one exists).

        Parameters
        ----------
        rule_file : Path
            path to Python file to load from.

        Returns
        -------
        TransdocTransformer
            Transformer with rules loaded from the given Python file.
        """
        # https://docs.python.org/3/library/importlib.html#importing-a-source-file-directly
        module_name = (
            f"transdoc.rules_temp.{rule_file.name.removesuffix('.py')}"
        )

        # Add rule file's directory to the module search path, so that imports
        # work as-expected
        sys.path.append(str(rule_file.parent.absolute()))
        # Now begin the import
        spec = importlib.util.spec_from_file_location(module_name, rule_file)
        if spec is None:
            raise ImportError(
                f"Import spec for rule file '{rule_file}' was None"
            )

        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module

        if spec.loader is None:
            raise ImportError(
                f"Spec loader for rule file '{rule_file}' was None"
            )

        # Any exceptions this raises get caught by the calling code
        try:
            spec.loader.exec_module(module)
        except BaseException as e:
            e.add_note(
                f"This exception occurred during execution of rule file "
                f"{rule_file}. It is unlikely to be an issue with Transdoc."
            )
            raise e

        return cls.from_namespace(module)

    @classmethod
    def from_namespace(cls, namespace: Any) -> "TransdocTransformer":
        """
        Create a `TransdocTransformer` from attributes on a namespace (module
        or object).

        Attributes are considered to be rules if they are callable, and if they
        are contained within the namespace's `__all__` attribute (if one
        exists).

        Parameters
        ----------
        namespace : Any
            Namespace to collect rules from. This can be a Python module, or
            any other object.

        Returns
        -------
        TransdocTransformer
            Transformer with rules loaded from the given namespace.
        """
        all_attrs = getattr(namespace, "__all__", dir(namespace))

        collected_rules = {}

        for attr_name in all_attrs:
            item = getattr(namespace, attr_name)
            if callable(item):
                collected_rules[attr_name] = item

        return TransdocTransformer(collected_rules)

    def _eval_rule(
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

        Parameters
        ----------
        input : str
            Input string to transform
        filename : str
            Name of file which the input string belongs to, used in error
            reporting.
        position_offset : SourcePos, optional
            Source position to use when offsetting source positions in errors.
        indentation : str, optional
            String to use for indentation (eg `' ' * 4` for 4 spaces, or
            `'\\t'` for one tab).

        Returns
        -------
        str
            Resultant text.
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
            start = position_offset.offset_by_str(input[: match.start()])
            end = position_offset.offset_by_str(input[: match.end()])

            # Add non-matched input to output
            output.write(input[input_pos : match.start()])
            input_pos = match.end()

            try:
                output.write(
                    self._eval_rule(
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
