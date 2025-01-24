"""
# Transdoc / Handlers

Code defining Transdoc handlers.
"""

import logging

from importlib.metadata import entry_points
from typing import Sequence
from .api import TransdocHandler
from .plaintext import PlaintextHandler


log = logging.getLogger("transdoc.handlers")


def get_all_handlers() -> list[TransdocHandler]:
    """
    Returns a list of all handler objects.

    This includes Transdoc built-in handlers, as well as any detected plugins.

    Returns:
        list[TransdocHandler]: found handlers
    """
    handlers: list[TransdocHandler] = [PlaintextHandler()]
    log.info(f"Built-in handlers are: {handlers}")

    discovered = entry_points(group="transdoc.handlers")
    for discovered_handler in discovered:
        try:
            loaded: type[TransdocHandler] = discovered_handler.load()
            handlers.append(loaded())
            log.info(f"Loaded handler plugin: {discovered_handler}")
        except Exception:
            log.exception(
                "Error loading discovered handler plugin:", discovered_handler
            )

    return handlers


def find_matching_handler(
    handlers: Sequence[TransdocHandler],
    file_path: str,
) -> TransdocHandler | None:
    """
    Find and return the first `TransdocHandler` capable of transforming the
    given file.

    If no match can be found, returns `None`.

    Args:
        handlers (Sequence[TransdocHandler]): list of handler plugins to check
        file_path (str): file path to check against

    Returns:
        TransdocHandler | None: matching handler or `None`
    """
    # https://stackoverflow.com/a/8534381/6335363
    return next(
        (h for h in handlers if h.matches_file(file_path)),
        None,
    )


__all__ = ["TransdocHandler", "get_all_handlers", "find_matching_handler"]
