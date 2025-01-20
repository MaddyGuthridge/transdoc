"""
# Transdoc / Tests / Rules / File Contents Test

Test cases for the `file_contents` rule.
"""

from transdoc import TransdocTransformer
from transdoc.rules import file_contents


def test_file_contents():
    transformer = TransdocTransformer({"file_contents": file_contents})
    assert (
        transformer.transform(
            "{{file_contents[tests/data/example.txt]}}", "<string>"
        )
        == "Contents of example file"
    )
