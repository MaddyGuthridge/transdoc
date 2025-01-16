"""
# Transdoc / Handlers / API

API definition for Transdoc handler modules.
"""
from collections.abc import Sequence
import re
from typing import Protocol
from pathlib import Path
from transdoc.__transformer import TransdocTransformer


RegexPattern = re.Pattern[str] | str


class TransdocHandler(Protocol):
    """
    A language handler plugin for transdoc.
    """

    def get_file_matchers(self) -> Sequence[RegexPattern]:
        """
        Returns the list of file extensions that this handler supports.

        This should be a sequence of regular expressions which match the
        desired files.

        Returns:
            list[str]: supported file extensions (eg `['txt', 'md'])
        """
        ...

    def transform_file(
        self,
        transformer: TransdocTransformer,
        in_path: Path,
        out_path: Path,
    ) -> None:
        """
        Transforms the contents of the file at `in_path`, writing the
        transformed output into the file at `out_path`.

        Args:
            transformer (TransdocTransformer): use `transformer.transform` on
            any strings where rules should be applied.
            in_path (Path): path to input file
            out_path (Path): path to output file
        """
        ...
