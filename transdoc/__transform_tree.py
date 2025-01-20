"""
# Transdoc / tree transform

Process an entire directory tree (or a single file) using transdoc.
"""

import logging
import os
from shutil import rmtree
from pathlib import Path
from dataclasses import dataclass
from typing import Optional, Sequence

from transdoc.__transform_file import transform_file
from transdoc.__transformer import TransdocTransformer
from transdoc.handlers.api import TransdocHandler


log = logging.getLogger("transdoc.tree_transform")


@dataclass
class FileMapping:
    input: Path
    output: Optional[Path]


def expand_tree(
    input: Path,
    output: Optional[Path],
) -> list[FileMapping]:
    """
    Given a path
    """
    file_mappings: list[FileMapping] = []
    if input.is_dir():
        for dirpath, _, filenames in os.walk(input):
            for filename in filenames:
                in_file = Path(dirpath).joinpath(filename)
                if output is None:
                    out_file = None
                else:
                    out_file = output.joinpath(in_file.relative_to(input))
                file_mappings.append(
                    FileMapping(
                        in_file,
                        out_file,
                    )
                )
    else:
        file_mappings.append(FileMapping(input, output))

    return file_mappings


def transform_tree(
    handlers: Sequence[TransdocHandler],
    transformer: TransdocTransformer,
    input: Path,
    output: Path | None = None,
    *,
    force: bool = False,
) -> None:
    """
    Transform all files within a tree.
    """
    errors: list[Exception] = []
    file_mappings = expand_tree(input, output)

    if not force:
        if output is not None and output.exists():
            if output.is_dir() and len(os.listdir(output)):
                errors.append(
                    FileExistsError(
                        f"Output directory '{output}' exists and is not empty"
                    )
                )
            else:
                errors.append(
                    FileExistsError(
                        f"Output location '{output}' already exists"
                    )
                )

    if len(errors):
        raise ExceptionGroup(
            "Errors occurred while preparing transformation", errors
        )

    # Remove the output file/directory
    if output is not None and output.is_dir() and force:
        rmtree(output)

    for mapping in file_mappings:
        try:
            transform_file(
                handlers,
                transformer,
                str(mapping.input),
                open(mapping.input),
                None if mapping.output is None else open(mapping.output, "w"),
            )
        except Exception as e:
            e.add_note(f"Error occurred while transforming {mapping.input}")
            errors.append(e)

    if len(errors):
        raise ExceptionGroup(
            "Errors occurred while performing transformation", errors
        )
