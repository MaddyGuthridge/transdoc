"""# 🏳️‍⚧️ Transdoc 🏳️‍⚧️

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

import logging
from io import StringIO

from . import util
from .__consts import VERSION as __version__  # noqa: N811
from .__rule import TransdocRule
from .__transform_file import transform_file
from .__transform_tree import transform_tree
from .__transformer import TransdocTransformer
from .handlers import PlaintextHandler, TransdocHandler, get_all_handlers

log = logging.getLogger("transdoc")


def transform(
    transformer: TransdocTransformer,
    input: str,
    path: str = "<string>",
    handler: TransdocHandler | None = None,
) -> str:
    """Transform the given input string using Transdoc.

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
            f"The given handler {handler} does not match the input file path "
            f"'{path}'",
        )

    in_buf = StringIO(input)
    out_buf = StringIO()
    handler.transform_file(transformer, path, in_buf, out_buf)
    out_buf.seek(0)
    return out_buf.read()
