"""# Transdoc / util

Utility functions for Transdoc.
"""

import sys
from pathlib import Path

from colored import Fore, Style

from transdoc.errors import TransdocTransformationError


def indent_by(indent: str, string: str) -> str:
    """Indent the given string using the given indentation."""
    return "\n".join(
        f"{indent}{line.rstrip()}" for line in string.splitlines()
    ).lstrip()


def print_error(e: Exception):
    """Utility function to print errors to `sys.stderr`."""

    def error_args(args: tuple) -> str:
        msg = []
        for arg in args:
            if isinstance(arg, tuple):
                msg.append(error_args(arg))
            else:
                msg.append(str(arg))
        return " ".join(msg)

    def display_transdoc_error(e: TransdocTransformationError):
        print(
            f"{Fore.CYAN}{e.filename}:{e.pos.start}{Style.RESET} "
            f"{Fore.RED}{type(e).__name__}{Style.RESET}: "
            f"{error_args(e.args)}",
            file=sys.stderr,
        )

    def display_syntax_error(e: SyntaxError):
        print(
            f"{Fore.CYAN}{e.filename}:{e.lineno}:{e.offset}{Style.RESET} "
            f"{Fore.RED}{type(e).__name__}{Style.RESET}: "
            f"{e.msg}",
            file=sys.stderr,
        )

    if isinstance(e, ExceptionGroup):
        for sub_error in e.exceptions:
            print_error(sub_error)
    elif isinstance(e, SyntaxError):
        display_syntax_error(e)
    elif isinstance(e, TransdocTransformationError):
        display_transdoc_error(e)
    else:
        print(
            f"{Fore.RED}{type(e).__name__}{Style.RESET}: {error_args(e.args)}",
            file=sys.stderr,
        )


__textchars = bytearray(
    {7, 8, 9, 10, 12, 13, 27} | set(range(0x20, 0x100)) - {0x7F},
)


def file_is_binary(p: Path):
    """
    Return whether the given file is binary.

    If any non-printable characters are contained in the first 1024 bytes, this
    returns True, as per the UNIX `file` program behaviour.

    Sources:
    * https://github.com/file/file/blob/f2a6e7cb7db9b5fd86100403df6b2f830c7f22ba/src/encoding.c#L151-L228
    * https://stackoverflow.com/a/7392391/6335363

    Parameters
    ----------
    p : Path
        Path of file to check
    """
    with open(p, "rb") as f:
        b = f.read(1024)
    return bool(b.translate(None, __textchars))
