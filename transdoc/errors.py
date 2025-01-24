"""
# Transdoc / Errors

Definitions for error classes used by Transdoc.
"""
from typing import Any

from transdoc.source_pos import SourceRange


class TransdocError(Exception):
    """
    An error that occurred when processing files using Transdoc.
    """

    def __init__(self, filename: str, pos: SourceRange, *args: Any) -> None:
        super().__init__(args)
        self.filename = filename
        self.pos = pos


class TransdocHandlerError(TransdocError):
    """Unable to find a `TransdocHandler` that matches the given file"""


class TransdocSyntaxError(TransdocError):
    """SyntaxError when transforming documentation"""


class TransdocNameError(TransdocError):
    """NameError when attempting to execute rule"""


class TransdocEvaluationError(TransdocError):
    """Error occurred when evaluating rule"""
