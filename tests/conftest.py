"""
# Tests / Conftest

Pytest configuration
"""

from importlib import metadata
from typing import Any
import pytest
from pytest_mock import MockerFixture

from transdoc.rules import file_contents
from transdoc import TransdocTransformer


# Code for mocking Python's entry-points system
###############################################################################

# This code originates from Poetry's code for testing their own plugin system.
# https://github.com/python-poetry/poetry/blob/ecc2697fd79bbc7ef3037ea95c7ed1ef83b8a658/tests/helpers.py#L253
#
# Copyright (c) 2018-present Sébastien Eustace
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


def make_entry_point_from_plugin(
    name: str, cls: type[Any], dist: metadata.Distribution | None = None
) -> metadata.EntryPoint:
    """
    Create and return an importlib.metadata.EntryPoint object for the given
    plugin class.
    """
    group: str | None = getattr(cls, "group", None)
    ep = metadata.EntryPoint(
        name=name,
        group=group,  # type: ignore[arg-type]
        value=f"{cls.__module__}:{cls.__name__}",
    )

    if dist:
        ep = ep._for(dist)  # type: ignore[attr-defined,no-untyped-call]
        return ep

    return ep


def mock_metadata_entry_points(
    mocker: MockerFixture,
    cls: type[Any],
    name: str = "my-plugin",
    dist: metadata.Distribution | None = None,
) -> None:
    """
    Add a mock entry-point to importlib's metadata.

    The entry-point's group is determined using the static `group` attribute of
    the given `cls`.

    Args:
        mocker (MockerFixture): the mocker to use when mocking the values.
        cls (type[Any]): the class to register as a plugin. This class must be
        defined in an importable location (eg the global scope of a valid
        module).
        name (str, optional): name to use for the plugin. Defaults to
        `"my-plugin"`.
        dist (metadata.Distribution, optional): distribution info for the
        plugin. Defaults to `None`.
    """
    mocker.patch.object(
        metadata,
        "entry_points",
        return_value=[make_entry_point_from_plugin(name, cls, dist)],
    )


# Pytest fixture for `TransdocTransformer`
###############################################################################


@pytest.fixture
def transformer():
    return TransdocTransformer(
        {
            "simple": simple_rule,
            "multiline": multiline_rule,
            "echo": echo_rule,
            "error": error_rule,
            "file_contents": file_contents,
        }
    )


# Simple rules


def simple_rule():
    return "Simple rule"


def multiline_rule():
    return "Multiple\nLines"


def echo_rule(value):
    return value


def error_rule(exc_type: str = "TypeError"):
    raise eval(exc_type)
