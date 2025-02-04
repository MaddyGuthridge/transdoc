"""
# Transdoc / CLI / Main

Main entrypoint to the Transdoc CLI.
"""

import logging.config
import sys
import os
import click
from pathlib import Path
from typing import IO, Optional
import logging

from transdoc import (
    transform_tree,
    transform_file,
    TransdocTransformer,
    get_all_handlers,
)
from transdoc.util import print_error
from .mutex import Mutex
from .util import pride

from transdoc.__consts import VERSION


log = logging.getLogger(__name__)


help_text_width = os.get_terminal_size().columns - 4


HELP_TEXT = f"""
\b
{"Transdoc CLI".center(help_text_width)}
{pride("=" * help_text_width)}

\b
{"Transform your documentation by embedding results from Python function calls.".center(help_text_width)}
"""

HELP_EPILOG = f"""
\b
{"For more help, view the documentation online:".center(help_text_width)}
{"https://maddyguthridge.github.io/transdoc".center(help_text_width)}

\b
{pride("<3 " * (help_text_width // 3), 3)}

\b
{"Made with <3 by Maddy Guthridge".center(help_text_width)}

"""


def handle_verbose(verbose: int):
    mappings = {
        0: "CRITICAL",
        1: "WARNING",
        2: "INFO",
        3: "DEBUG",
    }
    logging.basicConfig(level=mappings.get(verbose, "DEBUG"))


@click.command("transdoc", help=HELP_TEXT, epilog=HELP_EPILOG)
@click.argument(
    "input",
    type=click.Path(exists=True, allow_dash=True),
    # help='Path to the input file or directory',
)
@click.option(
    "-r",
    "--rule-file",
    type=click.Path(exists=True, path_type=Path),
    required=True,
    help="Path to any Python file/module containing rules for Transdoc to use",
)
@click.option(
    "-o",
    "--output",
    type=click.Path(exists=False, path_type=Path),
    help="Path to the output file or directory",
    cls=Mutex,
    mutex_with=["dryrun"],
)
@click.option(
    "-d",
    "--dryrun",
    is_flag=True,
    help="Don't produce any output files",
)
@click.option(
    "-f",
    "--force",
    is_flag=True,
    help="Forcefully overwrite the output file/directory",
    cls=Mutex,
    mutex_with=["dryrun"],
)
@click.option("-v", "--verbose", count=True)
@click.version_option(VERSION)
def cli(
    input: str,
    rule_file: Path,
    output: Optional[Path] = None,
    *,
    dryrun: bool = False,
    force: bool = False,
    verbose: int = 0,
) -> int:
    """CLI entrypoint"""
    handle_verbose(verbose)
    try:
        transformer = TransdocTransformer.from_file(rule_file)
    except Exception as e:
        msg = f"Error evaluating rule file '{rule_file}'"
        log.exception(msg)
        print(msg, file=sys.stderr)
        print_error(e)
        return 1
    handlers = get_all_handlers()

    if input == "-":
        # Transform stdin
        if output is not None:
            out_file: IO | None = open(output, "w")
        else:
            out_file = sys.stdout
        try:
            transform_file(
                handlers,
                transformer,
                "<stdin>",
                sys.stdin,
                out_file,
            )
        except ExceptionGroup as e:
            print_error(e)
            return 1
    else:
        if output is None and not dryrun:
            print("--output must be given if --dryrun is not specified")
            return 2
        try:
            transform_tree(
                handlers,
                transformer,
                Path(input),
                output,
                force=force,
            )
        except ExceptionGroup as e:
            print_error(e)
            return 1
    return 0
