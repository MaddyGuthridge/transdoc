"""
# Transdoc / Handlers / Plaintext

A Transdoc handler for plain-text files.
"""

import re
from pathlib import Path
from transdoc import TransdocTransformer
from transdoc.handlers import TransdocHandler


class PlaintextHandler:
    """
    Transdoc handler for plain-text files.
    """

    def get_file_matchers(self):
        return [
            re.compile(r'\.txt$'),
            re.compile(r'\.md$'),
            re.compile(r'\.ascii$'),
        ]

    def transform_file(
        self,
        transformer: TransdocTransformer,
        in_path: Path,
        out_path: Path,
    ):
        with open(in_path) as in_file:
            with open(out_path) as out_file:
                out_file.write(transformer.apply(in_file.read(), in_path))


if __name__ == '__main__':
    # Ensure type-safety
    handler: TransdocHandler = PlaintextHandler()
