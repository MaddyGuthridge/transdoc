"""
# Transdoc / Handlers

Code defining Transdoc handlers.
"""

import logging

from importlib.metadata import entry_points
from .api import TransdocHandler
from .plaintext import PlaintextHandler


log = logging.getLogger("transdoc.handlers")


def get_all_handlers() -> list[TransdocHandler]:
    """
    Returns a list of all handler objects.
    """
    handlers: list[TransdocHandler] = [PlaintextHandler()]
    log.info(f"Built-in handlers are: {handlers}")

    discovered = entry_points(group="transdoc.handler")
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


__all__ = ["TransdocHandler", "get_all_handlers"]
