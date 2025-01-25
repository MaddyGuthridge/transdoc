"""
# Tests / Handlers / Example handlers

Simple Transdoc handlers used for testing.
"""

from typing import IO
import transdoc
from transdoc.handlers.api import TransdocHandler


class SimpleHandler(TransdocHandler):
    """Simple, valid handler plugin"""

    group = "transdoc.handlers"

    def matches_file(self, file_path: str) -> bool:
        return True

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

    def matches_file(self, file_path: str) -> bool:
        return False

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
        raise RuntimeError("Intentional failure to load plugin")

    def matches_file(self, file_path: str) -> bool:
        raise NotImplementedError()

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
