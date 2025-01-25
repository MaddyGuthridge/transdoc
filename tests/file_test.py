"""
# Tests / file test

Test cases for the `transform_file` function.
"""

from io import StringIO

import pytest
from tests.handlers.example_handlers import SimpleHandler, UnsupportedHandler
from transdoc import TransdocTransformer
import transdoc
from transdoc.errors import TransdocNoHandlerError


def test_transforms_file(transformer: TransdocTransformer):
    input = StringIO("Example text")
    output = StringIO()
    transdoc.transform_file(
        [SimpleHandler()], transformer, "<string>", input, output
    )
    output.seek(0)
    # SimpleHandler doesn't write output
    assert output.read() == ""


def test_no_matching_handlers(transformer: TransdocTransformer):
    input = StringIO("Example text")
    output = StringIO()
    with pytest.raises(TransdocNoHandlerError):
        transdoc.transform_file(
            [UnsupportedHandler()], transformer, "<string>", input, output
        )
