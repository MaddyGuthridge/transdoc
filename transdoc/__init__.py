"""
# 🏳️‍⚧️ Transdoc 🏳️‍⚧️

A simple tool for transforming Python docstrings by embedding results from
Python function calls.
"""

__all__ = [
    "__version__",
    "transform_tree",
    "transform_file",
    "TransdocHandler",
    "TransdocTransformer",
    "TransdocRule",
]

from io import StringIO
from .__rule import TransdocRule
from .__consts import VERSION as __version__
from .__transformer import TransdocTransformer
from .handlers import TransdocHandler, PlaintextHandler
from .__transform_tree import transform_tree
from .__transform_file import transform_file


def transform(
    transformer: TransdocTransformer,
    input: str,
    path: str = "<string>",
) -> str:
    """
    Transform the given input string.

    Args:
        transformer (TransdocTransformer): Transformer with all desired rules
        input (str): input string to transform
        path (str, optional): name of input string to use when reporting errors
    """
    handlers = [PlaintextHandler()]
    in_buf = StringIO(input)
    out_buf = StringIO()
    transform_file(handlers, transformer, path, in_buf, out_buf)
    out_buf.seek(0)
    return out_buf.read()
