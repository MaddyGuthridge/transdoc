"""
# Transdoc / Handlers / API

API definition for Transdoc handler modules.
"""

from abc import abstractmethod
from typing import Protocol, IO, runtime_checkable
from transdoc.__transformer import TransdocTransformer


@runtime_checkable
class TransdocHandler(Protocol):
    """
    A language handler plugin for transdoc.
    """

    @abstractmethod
    def matches_file(self, file_path: str) -> bool:
        """
        Given a file path, return whether this handler is capable of
        transforming the given file.

        Parameters
        ----------
        file_path : str
            The file path of the input.

        Returns
        -------
        bool
            Whether the file can be transformed using this transformer.
        """
        raise NotImplementedError()

    @abstractmethod
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

        If any errors occur during transformation, they should be collected and
        raised as an `ExceptionGroup[TransdocError]`.

        Parameters
        ----------
        transformer : TransdocTransformer
            Use `transformer.apply` on any strings where rules should be
            applied.
        in_path : str
            Path to input file, to be used in error reporting.
        in_file : IO
            File to read input from.
        out_file : IO | None
            The file to write the output to, or `None` if no output should be
            produced.

        Raises
        ------
        ExceptionGroup[TransdocError]
            errors encountered during transformation.
        """
        raise NotImplementedError()
