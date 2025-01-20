"""
# Transdoc / Handlers / Plaintext

A Transdoc handler for plain-text files.
"""

import re
from typing import IO
from transdoc import TransdocTransformer
from transdoc.handlers import TransdocHandler


class PlaintextHandler:
    """
    Transdoc handler for plain-text files.
    """

    def get_file_matchers(self):
        return [
            # <stdin> or <string>
            re.compile(r"^\<(stdin|string)\>$"),
            # *.txt
            re.compile(r"\.txt$"),
            # *.md
            re.compile(r"\.md$"),
            # *.ascii
            re.compile(r"\.ascii$"),
        ]

    def transform_file(
        self,
        transformer: TransdocTransformer,
        in_path: str,
        in_file: IO,
        out_file: IO | None,
    ):
        # Intentionally ignore exceptions, allowing them to fall through to
        # The caller
        transformed = transformer.transform(in_file.read(), in_path)

        if out_file is not None:
            out_file.write(transformed)


if __name__ == "__main__":
    # Ensure type-safety
    handler: TransdocHandler = PlaintextHandler()
