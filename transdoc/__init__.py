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

from .__rule import TransdocRule
from .__consts import VERSION as __version__
from .__transformer import TransdocTransformer
from .handlers import TransdocHandler
from .__transform_tree import transform_tree
from .__transform_file import transform_file
