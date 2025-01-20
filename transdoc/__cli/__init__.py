"""
# Transdoc / CLI / Main

Main entrypoint to the Transdoc CLI.
"""

import sys
from traceback import print_exc
import click
from pathlib import Path
from typing import IO, Optional

from transdoc.__collect_rules import load_rule_file
from transdoc.__transformer import TransdocTransformer
from transdoc.handlers import get_all_handlers
from .mutex import Mutex
from transdoc import transform_tree, transform_file

from transdoc.__consts import VERSION


@click.command("transdoc")
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
@click.version_option(VERSION)
def cli(
    input: str,
    rule_file: Path,
    output: Optional[Path] = None,
    *,
    dryrun: bool = False,
    force: bool = False,
) -> int:
    """
    Main entrypoint to the program.
    """
    transformer = TransdocTransformer(load_rule_file(rule_file))
    if input == "-":
        # Transform stdin
        if output is not None:
            out_file: IO | None = open(output, "w")
        else:
            out_file = sys.stdout
        try:
            transform_file(
                get_all_handlers(),
                transformer,
                "<stdin>",
                sys.stdin,
                out_file,
            )
        except ExceptionGroup:
            print_exc()
            return 1
    else:
        try:
            transform_tree(Path(input), rule_file, output, force=force)
        except ExceptionGroup:
            print_exc()
            return 1
    return 0
