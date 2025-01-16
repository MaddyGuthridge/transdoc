"""
# Transdoc / Handlers / API

API definition for Transdoc handler modules.
"""
from collections.abc import Sequence
import re
from typing import Protocol, IO
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
        in_path: str,
        in_file: IO,
        out_file: IO | None,
    ) -> None:
        """
        Transforms the contents of the file at `in_path`, writing the
        transformed output into the file at `out_path`.

        If any errors occur during transformation, no

        Args:
            transformer (TransdocTransformer): use `transformer.apply` on
            any strings where rules should be applied.
            in_path (str): path to input file, to be used in error reporting.
            in_file (IO): file to read input from.
            out_file (IO | None): the file to write the output to, or `None` if
            no output should be produced.

        Raises:
            ExceptionGroup[TransdocError]: errors encountered during
            transformation.
        """
        ...
