import logging
from pathlib import Path
from typing import IO, Sequence

from transdoc.__transformer import TransdocTransformer
from transdoc.handlers.api import TransdocHandler


log = logging.getLogger("transdoc.transform_file")


def transform_file(
    handlers: Sequence[TransdocHandler],
    transformer: TransdocTransformer,
    in_path: str,
    in_file: IO,
    out_file: IO | None,
) -> None:
    """
    Given an input file, its path and an output file, transform the file using
    the given handlers.
    """
    for handler in handlers:
        if any(
            Path(in_path).suffix == f".{m}"
            if isinstance(m, str)
            else m.search(Path(in_path).name)
            for m in handler.get_file_matchers()
        ):
            # This handler can handle the file
            log.info(f"Handler {handler} can handle file {in_path}")
            handler.transform_file(
                transformer,
                in_path,
                in_file,
                out_file,
            )
            break
    else:
        log.info(f"No handlers found that match file {in_path}, copying...")
        if out_file:
            out_file.write(in_file.read())
