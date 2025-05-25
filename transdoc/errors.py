"""# Transdoc / Errors

Definitions for error classes used by Transdoc.
"""

from collections.abc import Sequence
from importlib.metadata import EntryPoint
from pathlib import Path
from typing import Any, override

from transdoc.source_pos import SourceRange


class TransdocError(Exception):
    """Errors associated with Transdoc"""


class TransdocHandlerLoadError(TransdocError):
    """Error while loading a TransdocHandler"""


class TransdocHandlerConstructorError(TransdocHandlerLoadError):
    """Failed to construct transdoc handler"""

    def __init__(self, plugin: EntryPoint) -> None:
        """Failed to construct transdoc handler"""
        super().__init__(f"Error loading discovered handler plugin: {plugin}")


class TransdocHandlerProtocolError(TransdocHandlerLoadError):
    """Constructed handler does not match `TransdocHandler` protocol"""

    def __init__(self, plugin: EntryPoint) -> None:
        """Constructed handler does not match `TransdocHandler` protocol"""
        super().__init__(
            f"Plugin {plugin} doesn't match TransdocHandler protocol",
        )


class TransdocFileExistsError(TransdocError, FileExistsError):
    """File already exists"""


class TransdocOutputDirectoryNonEmptyError(TransdocFileExistsError):
    """Output directory already exists, and is non-empty"""

    def __init__(self, dir: Path) -> None:
        """Output directory already exists, and is non-empty"""
        super().__init__(f"Output directory '{dir}' exists and is not empty")


class TransdocOutputFileExistsError(TransdocFileExistsError):
    """Output file already exists"""

    def __init__(self, file: Path) -> None:
        """Output file already exists"""
        super().__init__(f"Output file '{file}' already exists")


class TransdocTransformationError(TransdocError):
    """An error that occurred when processing files using Transdoc."""

    def __init__(self, filename: str, pos: SourceRange, *args: Any) -> None:
        """An error that occurred when processing files using Transdoc."""
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


class TransdocTransformExceptionGroup(ExceptionGroup):
    """Exception group of errors when performing a transformation"""

    def __new__(
        cls,
        excs: Sequence[TransdocTransformationError],
    ) -> 'TransdocTransformExceptionGroup':
        """Exception group of errors when performing a transformation"""
        return super().__new__(
            cls,
            "Errors occurred while performing transformation",
            excs,
        )

    @override
    def derive(self, excs):
        return TransdocTransformExceptionGroup(excs)
