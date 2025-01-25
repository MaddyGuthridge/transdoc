"""
# Transdoc / Errors

Definitions for error classes used by Transdoc.
"""

from typing import Any

from transdoc.source_pos import SourceRange


class TransdocError(Exception):
    """Errors associated with Transdoc"""


class TransdocHandlerLoadError(TransdocError):
    """`TransdocHandler` failed to load"""


class TransdocTransformationError(TransdocError):
    """
    An error that occurred when processing files using Transdoc.
    """

    def __init__(self, filename: str, pos: SourceRange, *args: Any) -> None:
        super().__init__(args)
        self.filename = filename
        self.pos = pos


class TransdocNoHandlerError(TransdocTransformationError):
    """Unable to find a `TransdocHandler` that matches the given file"""


class TransdocSyntaxError(TransdocTransformationError):
    """SyntaxError when transforming documentation"""


class TransdocNameError(TransdocTransformationError):
    """NameError when attempting to execute rule"""


class TransdocEvaluationError(TransdocTransformationError):
    """Error occurred when evaluating rule"""
