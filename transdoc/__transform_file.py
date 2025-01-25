"""
# Transdoc / transform file

Process a single file using transdoc.
"""

import logging
from typing import IO, Sequence

from transdoc.__transformer import TransdocTransformer
from transdoc.errors import TransdocNoHandlerError
from transdoc.handlers import find_matching_handler
from transdoc.handlers.api import TransdocHandler
from transdoc.source_pos import SourceRange


log = logging.getLogger("transdoc.transform_file")


def transform_file(
    handlers: Sequence[TransdocHandler],
    transformer: TransdocTransformer,
    in_path: str,
    in_file: IO,
    out_file: IO | None,
) -> None:
    """
    Given an input file, its path and an output file, transform the file using
    the given handlers.

    If no handlers are able to handle the file, a `TransdocHandlerError` is
    raised. To avoid this, explicitly choose a handler, and use its
    `transform_file` method instead.

    Parameters
    ----------
    handlers : Sequence[TransdocHandler]
        List of handlers to consider for transforming the file.
    transformer : TransdocTransformer
        Transformer to use.
    in_path :  str
        Path of the input file
    in_file : IO
        Input file
    out_file : IO | None
        Output file, if output is desired.

    Raises
    ------
    TransdocHandlerError
        No handlers that match input file
    """
    handler = find_matching_handler(handlers, in_path)
    if handler is None:
        raise TransdocNoHandlerError(
            in_path,
            SourceRange.zero(),
            f"No handlers found that match file {in_path}!",
        )

    log.info(f"Handler {handler} can handle file {in_path}")
    handler.transform_file(
        transformer,
        in_path,
        in_file,
        out_file,
    )
