"""
# Transdoc / Handlers / Plaintext

A Transdoc handler for plain-text files.
"""

from pathlib import Path
from typing import IO
from transdoc import TransdocTransformer
from transdoc.handlers import TransdocHandler


class PlaintextHandler(TransdocHandler):
    """
    Transdoc handler for plain-text files.
    """

    def __repr__(self) -> str:
        return "PlaintextHandler"

    def matches_file(self, file_path: str) -> bool:
        return (
            # String inputs
            file_path in ["<string>", "<stdin>"]
            # Text-based file formats where other syntax won't cause issues
            or Path(file_path).suffix in [".txt", ".md", ".ascii"]
        )

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
