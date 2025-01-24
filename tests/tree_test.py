"""
# Tests / Tree test

Test cases for `transdoc.transform_tree`
"""

from pathlib import Path
from shutil import rmtree
from PIL import Image

from transdoc import transform_tree
from transdoc import TransdocTransformer
from transdoc.handlers.plaintext import PlaintextHandler


def test_transforms_directory(transformer: TransdocTransformer):
    """
    Creates an output directory if one does not exist, then transforms files
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
    """
    Creates an output directory if one does not exist, then transforms files
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
        Path("tests/data/directory/README.md"),
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
