"""# Tests / Handlers / Plaintext test

Test cases for plaintext handler.
"""

import pytest

from transdoc.handlers.plaintext import PlaintextHandler


@pytest.mark.parametrize("filename", ["example.txt", "in.ascii", "README.md"])
def test_matches_text_file_formats(filename: str):
    handler = PlaintextHandler()
    assert handler.matches_file(filename)
