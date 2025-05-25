"""# Tests / Handlers / Example handlers

Simple Transdoc handlers used for testing.
"""

from typing import IO

from typing_extensions import override

import transdoc
from transdoc.handlers.api import TransdocHandler


class SimpleHandler(TransdocHandler):
    """Simple, valid handler plugin"""

    group = "transdoc.handlers"

    @override
    def matches_file(self, file_path: str) -> bool:
        return True

    @override
    def transform_file(
        self,
        transformer: transdoc.TransdocTransformer,
        in_path: str,
        in_file: IO,
        out_file: IO | None,
    ) -> None:
        # Do nothing, we don't test outputs using this handler
        pass


class UnsupportedHandler(TransdocHandler):
    """handler plugin which supports no file types"""

    group = "transdoc.handlers"

    @override
    def matches_file(self, file_path: str) -> bool:
        return False

    @override
    def transform_file(
        self,
        transformer: transdoc.TransdocTransformer,
        in_path: str,
        in_file: IO,
        out_file: IO | None,
    ) -> None:
        # Do nothing, we don't test outputs using this handler
        pass


class FailToLoadHandler(TransdocHandler):
    """Handler plugin that fails to load due to an exception during creation"""

    group = "transdoc.handlers"

    def __init__(self) -> None:
        """Intentionally fail"""
        raise RuntimeError("Intentional failure to load plugin")  # noqa: TRY003

    @override
    def matches_file(self, file_path: str) -> bool:
        raise NotImplementedError()

    @override
    def transform_file(
        self,
        transformer: transdoc.TransdocTransformer,
        in_path: str,
        in_file: IO,
        out_file: IO | None,
    ) -> None:
        raise NotImplementedError()


class ProtocolMismatchHandler:
    """Handler plugin that doesn't match the protocol"""

    group = "transdoc.handlers"

    # Intentionally empty
