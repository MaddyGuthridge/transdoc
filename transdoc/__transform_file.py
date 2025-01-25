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

    If no handlers are able to handle the file, raise a `TransdocHandlerError`.
    To avoid this, explicitly choose a handler, and use its `transform_file`
    method.

    Args:
        handlers (Sequence[TransdocHandler]): list of handlers to use
        transformer (TransdocTransformer): transformer to use
        in_path (str): path of the input file
        in_file (IO): input file
        out_file (IO | None): output file, if required

    Raises:
        TransdocHandlerError: no handlers that match input file
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
