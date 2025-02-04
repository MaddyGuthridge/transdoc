"""
# 🏳️‍⚧️ Transdoc 🏳️‍⚧️

A simple tool for transforming Python docstrings by embedding results from
Python function calls.
"""

__all__ = [
    "__version__",
    "transform_tree",
    "transform_file",
    "TransdocTransformer",
    "TransdocRule",
    "get_all_handlers",
    "TransdocHandler",
    "util",
]

from io import StringIO
import logging
from typing import Optional
from .__rule import TransdocRule
from .__consts import VERSION as __version__
from .__transformer import TransdocTransformer
from .handlers import TransdocHandler, PlaintextHandler, get_all_handlers
from .__transform_tree import transform_tree
from .__transform_file import transform_file
from . import util


log = logging.getLogger("transdoc")


def transform(
    transformer: TransdocTransformer,
    input: str,
    path: str = "<string>",
    handler: Optional[TransdocHandler] = None,
) -> str:
    """
    Transform the given input string using Transdoc.

    Parameters
    ----------
    transformer : TransdocTransformer
        Transformer with all desired transformation rules.
    input : str
        Input string to transform.
    path : str, optional = "<string>"
        Name of input string to use when reporting errors.
    handler : TransdocHandler, optional
        Handler to use for transformation. Defaults to `PlaintextHandler()`
        when not provided.

    Returns
    -------
    str
        Transformed text.
    """
    if handler is None:
        handler = PlaintextHandler()

    if not handler.matches_file(path):
        log.warning(
            f"The given handler {handler} does not match the input file path '{path}'"
        )

    in_buf = StringIO(input)
    out_buf = StringIO()
    handler.transform_file(transformer, path, in_buf, out_buf)
    out_buf.seek(0)
    return out_buf.read()
