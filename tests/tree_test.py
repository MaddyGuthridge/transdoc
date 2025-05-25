"""# Tests / Tree test

Test cases for `transdoc.transform_tree`
"""

from pathlib import Path
from shutil import rmtree

import pytest
from PIL import Image

from transdoc import TransdocTransformer, transform_tree
from transdoc.errors import TransdocNameError
from transdoc.handlers.plaintext import PlaintextHandler


def test_transforms_directory(transformer: TransdocTransformer):
    """Creates an output directory if one does not exist, then transforms files
    into it
    """
    temp = Path("temp")
    rmtree(temp, ignore_errors=True)
    transform_tree(
        [PlaintextHandler()],
        transformer,
        Path("tests/data/directory"),
        temp,
    )
    assert temp.is_dir()
    # Test all files were created correctly
    for file in ["LICENSE.txt", "README.md", "brick.png"]:
        assert (temp / file).is_file()

    # In particular, the image (a binary file) should still be valid
    with Image.open("temp/brick.png") as im:
        im.verify()


def test_transforms_single_file(transformer: TransdocTransformer):
    """Creates an output directory if one does not exist, then transforms files
    into it
    """
    out = Path("temp/README.md")
    rmtree("temp", ignore_errors=True)
    transform_tree(
        [PlaintextHandler()],
        transformer,
        Path("tests/data/directory/README.md"),
        out,
    )
    assert out.is_file()


def test_produces_no_output_when_out_path_is_none(
    transformer: TransdocTransformer,
):
    transform_tree(
        [PlaintextHandler()],
        transformer,
        Path("tests/data/directory"),
        None,
    )
    # No output produced


def test_overwrites_when_force_used(transformer: TransdocTransformer):
    temp = Path("temp")
    rmtree(temp, ignore_errors=True)
    transform_tree(
        [PlaintextHandler()],
        transformer,
        Path("tests/data/directory"),
        temp / "README.md",
    )
    # Forceful should not cause error
    transform_tree(
        [PlaintextHandler()],
        transformer,
        Path("tests/data/directory"),
        temp,
        force=True,
    )


def test_fails_when_output_dir_already_exists(
    transformer: TransdocTransformer,
):
    temp = Path("temp")
    rmtree(temp, ignore_errors=True)
    transform_tree(
        [PlaintextHandler()],
        transformer,
        Path("tests/data/directory"),
        temp,
    )
    with pytest.raises(FileExistsError):
        transform_tree(
            [PlaintextHandler()],
            transformer,
            Path("tests/data/directory"),
            temp,
        )


def test_fails_when_output_file_already_exists(
    transformer: TransdocTransformer,
):
    temp = Path("temp")
    rmtree(temp, ignore_errors=True)
    transform_tree(
        [PlaintextHandler()],
        transformer,
        Path("tests/data/directory/README.md"),
        temp / "README.md",
    )
    with pytest.raises(FileExistsError):
        transform_tree(
            [PlaintextHandler()],
            transformer,
            Path("tests/data/directory/README.md"),
            temp / "README.md",
        )


def test_writes_into_existing_empty_dir(transformer: TransdocTransformer):
    temp = Path("temp")
    rmtree(temp, ignore_errors=True)
    Path("temp").mkdir()
    transform_tree(
        [PlaintextHandler()],
        transformer,
        Path("tests/data/directory"),
        temp,
    )


def test_passes_on_errors_during_transformation(
    transformer: TransdocTransformer,
):
    temp = Path("temp")
    rmtree(temp, ignore_errors=True)
    with pytest.raises(ExceptionGroup) as exc:
        transform_tree(
            [PlaintextHandler()],
            transformer,
            Path("tests/data/invalid_call.txt"),
            temp / "invalid_call.txt",
        )

    assert exc.group_contains(TransdocNameError)
