"""
# Tests / Handlers / Get handlers test

Test cases for `transdoc.handlers.get_all_handlers`
"""

from typing import IO
import jestspectation as expect
import pytest
from pytest_mock import MockerFixture

from tests.conftest import mock_metadata_entry_points
import transdoc
from transdoc.errors import TransdocHandlerLoadError
from transdoc.handlers.api import TransdocHandler
from transdoc.handlers.plaintext import PlaintextHandler


def test_default_handlers():
    # By default, only the plaintext handler is included
    assert transdoc.handlers.get_all_handlers() == [
        expect.Any(PlaintextHandler)
    ]


# Test actual plugin loading using pytest-mock
###############################################################################


def test_handler_load_valid(mocker: MockerFixture):
    mock_metadata_entry_points(mocker, ValidHandler)
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


class ValidHandler(TransdocHandler):
    """Simple, valid handler plugin"""

    group = "transdoc.handlers"

    def matches_file(self, file_path: str) -> bool:
        return False

    def transform_file(
        self,
        transformer: transdoc.TransdocTransformer,
        in_path: str,
        in_file: IO,
        out_file: IO | None,
    ) -> None:
        pass


class FailToLoadHandler(TransdocHandler):
    """Handler plugin that fails to load due to an exception during creation"""

    group = "transdoc.handlers"

    def __init__(self) -> None:
        raise RuntimeError("Intentional failure to load plugin")

    def matches_file(self, file_path: str) -> bool:
        raise NotImplementedError()

    def transform_file(
        self,
        transformer: transdoc.TransdocTransformer,
        in_path: str,
        in_file: IO,
        out_file: IO | None,
    ) -> None:
        raise NotImplementedError()


class ProtocolMismatchHandler:
    """Handler plugin that doesn't match the protocol"""

    group = "transdoc.handlers"

    # Intentionally empty
