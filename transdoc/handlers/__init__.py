"""
# Transdoc / Handlers

Code defining Transdoc handlers.
"""

import logging

from importlib import metadata
from typing import Sequence

from transdoc.errors import TransdocHandlerLoadError
from .api import TransdocHandler
from .plaintext import PlaintextHandler


log = logging.getLogger("transdoc.handlers")


def get_all_handlers() -> list[TransdocHandler]:
    """
    Returns a list of all handler objects.

    This includes Transdoc built-in handlers, as well as any detected plugins.

    Returns
    -------
    list[TransdocHandler]
        Handlers found through package metadata, and default handlers.
    """
    handlers: list[TransdocHandler] = [PlaintextHandler()]
    log.info(f"Built-in handlers are: {handlers}")

    entry_points = metadata.entry_points(group="transdoc.handlers")
    for discovered in entry_points:
        try:
            constructor: type[TransdocHandler] = discovered.load()
            handler = constructor()
        except Exception as e:
            raise TransdocHandlerLoadError(
                f"Error loading discovered handler plugin: {discovered}"
            ) from e
        if not isinstance(handler, TransdocHandler):
            raise TransdocHandlerLoadError(
                f"Plugin {discovered} doesn't match TransdocHandler protocol"
            )
        handlers.append(handler)
        log.info(f"Loaded handler plugin: {discovered}")

    return handlers


def find_matching_handler(
    handlers: Sequence[TransdocHandler],
    file_path: str,
) -> TransdocHandler | None:
    """
    Find and return the first `TransdocHandler` capable of transforming the
    given file.

    If no match can be found, returns `None`.

    Parameters
    ----------
    handlers : Sequence[TransdocHandler]
        List of handler plugins to check.
    file_path : str
        File path to check against.

    Returns
    -------
    TransdocHandler | None
        Matching handler or `None` if no match found.
    """
    # https://stackoverflow.com/a/8534381/6335363
    return next(
        (h for h in handlers if h.matches_file(file_path)),
        None,
    )


__all__ = ["TransdocHandler", "get_all_handlers", "find_matching_handler"]
