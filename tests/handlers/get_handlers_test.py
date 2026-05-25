"""# Tests / Handlers / Get handlers test

Test cases for `transdoc.handlers.get_all_handlers`
"""

import jestspectation as expect
import pytest
from pytest_mock import MockerFixture
from transdoc_python import TransdocPythonHandler

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
    # Due to workspace config, Python handler is included by default when
    # running tests. If more handler plugins are added to the monorepo they
    # may need to be added to this list.
    assert transdoc.handlers.get_all_handlers() == [
        expect.Any(PlaintextHandler),
        expect.Any(TransdocPythonHandler),
    ]


# Test actual plugin loading using pytest-mock
###############################################################################


def test_handler_load_valid(mocker: MockerFixture):
    mock_metadata_entry_points(mocker, SimpleHandler)
    _ = transdoc.handlers.get_all_handlers()


def test_handler_load_failure(mocker: MockerFixture):
    mock_metadata_entry_points(mocker, FailToLoadHandler)
    with pytest.raises(TransdocHandlerLoadError):
        # FailToLoadHandler should give an exception
        _ = transdoc.handlers.get_all_handlers()


def test_handler_protocol_mismatch(mocker: MockerFixture):
    mock_metadata_entry_points(mocker, ProtocolMismatchHandler)
    with pytest.raises(TransdocHandlerLoadError):
        # FailToLoadHandler should give an exception
        _ = transdoc.handlers.get_all_handlers()
