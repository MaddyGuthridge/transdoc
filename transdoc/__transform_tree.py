"""
# Transdoc / transform tree

Process an entire directory tree (or a single file) using transdoc.
"""

import logging
import os
from shutil import copyfile, rmtree
from pathlib import Path
from dataclasses import dataclass
from typing import Optional, Sequence

from transdoc.__transformer import TransdocTransformer
from transdoc.handlers import find_matching_handler
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
    Given a path, expand it into a list of files that are descendants of that
    path if the input is a directory.
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
    output: Path | None,
    *,
    force: bool = False,
) -> None:
    """
    Transform all files within a tree.

    This takes all files that are descendants of the input file, and transforms
    them, writing the results into the corresponding location on the output
    path.

    Parameters
    ----------
    handlers : Sequence[TransdocHandler]
        Handlers to consider using when transforming files.
    transformer : TransdocTransformer
        Transformer rules to use.
    input : Path
        Input path to transform. If a directory is given, all its descendants
        are transformed. If a regular file's path is given, it is transformed.
    output : Path | None
        Destination path. If a directory was given for `input`, a directory
        will be created at this path, and populated with the transformed
        contents of the `input` directory. If a regular file was given for
        `input`, the transformed output is written at that path.
    force : bool, optional = False
        Whether to remove the output if it already exists, rather than
        erroring. Defaults to `False`.

    Raises
    ------
    FileExistsError
        If output exists as a file or non-empty directory, and the `force`
        option was not set.
    ExceptionGroup
        Any exceptions that occurred while transforming the files.
    """
    file_mappings = expand_tree(input, output)

    if not force:
        if output is not None and output.exists():
            if output.is_dir():
                if len(os.listdir(output)):
                    raise FileExistsError(
                        f"Output directory '{output}' exists and is not empty"
                    )
                else:
                    # Output dir is empty directory, so no error
                    log.info(
                        f"Output dir '{output}' exists, but is empty. "
                        f"Will output to it."
                    )
            else:
                raise FileExistsError(
                    f"Output location '{output}' already exists"
                )

    # Remove the output file/directory
    if output is not None and output.is_dir() and force:
        log.info(f"Removing output dir {output}")
        rmtree(output)

    errors: list[Exception] = []

    # Consider using threading to speed this process up
    for mapping in file_mappings:
        # If we intend to output files, we should first create parent dirs
        if mapping.output is not None:
            mapping.output.parent.mkdir(parents=True, exist_ok=True)

        handler = find_matching_handler(handlers, str(mapping.input))
        if handler is None:
            # No handlers found, just copy file
            if mapping.output:
                act = "copying"
                copyfile(mapping.input, mapping.output)
            else:
                act = "skipping"
            log.info(
                f"No handlers found that match file {mapping.input}, {act}"
            )
        else:
            # Handler found
            log.info(f"Using handler {handler} to process {mapping.input}")
            # Now open files
            in_file = open(mapping.input)
            out_file = open(mapping.output, "w") if mapping.output else None
            # And perform the transformation
            try:
                handler.transform_file(
                    transformer,
                    str(mapping.input),
                    in_file,
                    out_file,
                )
            except Exception as e:
                msg = f"Error occurred while transforming {mapping.input}"
                log.exception(msg)
                e.add_note(msg)
                errors.append(e)

    if len(errors):
        raise ExceptionGroup(
            "Errors occurred while performing transformation", errors
        )
