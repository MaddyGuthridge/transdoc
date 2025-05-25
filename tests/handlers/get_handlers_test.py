"""# Tests / Handlers / Get handlers test

Test cases for `transdoc.handlers.get_all_handlers`
"""

import jestspectation as expect
import pytest
from pytest_mock import MockerFixture

import transdoc
from tests.conftest import mock_metadata_entry_points
from transdoc.errors import TransdocHandlerLoadError
from transdoc.handlers.plaintext import PlaintextHandler

from .example_handlers import (
    FailToLoadHandler,
    ProtocolMismatchHandler,
    SimpleHandler,
)


def test_default_handlers():
    # By default, only the plaintext handler is included
    assert transdoc.handlers.get_all_handlers() == [
        expect.Any(PlaintextHandler),
    ]


# Test actual plugin loading using pytest-mock
###############################################################################


def test_handler_load_valid(mocker: MockerFixture):
    mock_metadata_entry_points(mocker, SimpleHandler)
    transdoc.handlers.get_all_handlers()


def test_handler_load_failure(mocker: MockerFixture):
    mock_metadata_entry_points(mocker, FailToLoadHandler)
    with pytest.raises(TransdocHandlerLoadError):
        # FailToLoadHandler should give an exception
        transdoc.handlers.get_all_handlers()


def test_handler_protocol_mismatch(mocker: MockerFixture):
    mock_metadata_entry_points(mocker, ProtocolMismatchHandler)
    with pytest.raises(TransdocHandlerLoadError):
        # FailToLoadHandler should give an exception
        transdoc.handlers.get_all_handlers()
