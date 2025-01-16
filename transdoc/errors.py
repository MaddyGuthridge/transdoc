"""
# Transdoc / Errors

Definitions for error classes used by Transdoc.
"""
from pathlib import Path
from typing import Any

from transdoc.source_pos import SourcePos


class TransdocError(Exception):
    """
    An error that occurred when processing errors.
    """

    def __init__(self, filename: Path, pos: SourcePos, *args: Any) -> None:
        super().__init__(args)
        self.filename = filename
        self.pos = pos


class TransdocSyntaxError(TransdocError):
    """SyntaxError when transforming documentation"""


class TransdocNameError(TransdocError):
    """NameError when attempting to execute rule"""


class TransdocEvaluationError(TransdocError):
    """Error occurred when evaluating rule"""
