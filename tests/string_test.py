"""# Tests / string test

Test cases for transforming strings
"""

from pytest_mock import MockerFixture

import transdoc
from tests.handlers.example_handlers import SimpleHandler, UnsupportedHandler
from transdoc import TransdocTransformer


def test_transforms_strings(transformer: TransdocTransformer):
    assert transdoc.transform(transformer, "Input") == "Input"


def test_transforms_using_given_handler(
    mocker: MockerFixture, transformer: TransdocTransformer,
):
    handler = SimpleHandler()
    matches_file = mocker.spy(handler, "matches_file")
    transform_file = mocker.spy(handler, "transform_file")

    transdoc.transform(transformer, "Input", path="<test>", handler=handler)

    matches_file.assert_called_once_with("<test>")
    transform_file.assert_called_once()


def test_unsupported_handler_warning(transformer: TransdocTransformer):
    handler = UnsupportedHandler()
    transdoc.transform(transformer, "Input", path="<test>", handler=handler)
    # Not testing for logging issues, because that's sorta annoying. This is
    # just here for coverage
