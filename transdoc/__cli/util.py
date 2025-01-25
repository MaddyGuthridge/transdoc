"""
# Transdoc / CLI / Util

Utilities for CLI application.
"""

from collections.abc import Generator, Sequence
import random
from typing import TypeVar
from colored import Fore, Style


T = TypeVar("T")


# Manually define itertools.batched for Python 3.11 support
# https://stackoverflow.com/a/8290508/6335363
def batched(iterable: Sequence[T], n=1) -> Generator[Sequence[T], None, None]:
    """
    Batched iterator.

    >>> list(batched([1, 2, 3, 4, 5], 2))
    [[1, 2], [3, 4], [5]]
    """
    for ndx in range(0, len(iterable), n):
        yield iterable[ndx : min(ndx + n, len(iterable))]


# Flag colours from https://www.flagcolorcodes.com


RESET = Style.reset
RAINBOW = [
    Fore.rgb(228, 3, 3),  # Red
    Fore.rgb(255, 140, 0),  # Orange
    Fore.rgb(255, 237, 0),  # Yellow
    Fore.rgb(0, 128, 38),  # Green
    Fore.rgb(0, 76, 255),  # Blue
    Fore.rgb(115, 41, 130),  # Purple
]
TRANS = [
    Fore.rgb(91, 206, 250),  # Blue
    Fore.rgb(245, 169, 184),  # Pink
    Fore.rgb(255, 255, 255),  # White
    Fore.rgb(245, 169, 184),  # Pink
    Fore.rgb(91, 206, 250),  # Blue
    Fore.rgb(64, 64, 64),  # Grey for space
]
NB = [
    Fore.rgb(252, 244, 52),  # Yellow
    Fore.rgb(255, 255, 255),  # White
    Fore.rgb(156, 89, 209),  # Purple
    Fore.rgb(44, 44, 44),  # Black
]
# # https://www.reddit.com/r/thomastheplankengine/comments/1gw1v0c
NB_WARTIME = [
    Fore.rgb(252, 244, 52),  # Yellow
    Fore.rgb(44, 44, 44),  # Black
    Fore.rgb(156, 89, 209),  # Purple
    Fore.rgb(255, 255, 255),  # White
]
GENDERQUEER = [
    Fore.rgb(181, 126, 220),  # Lavender
    Fore.rgb(255, 255, 255),  # White
    Fore.rgb(74, 129, 35),  # Green
]
GENDERFLUID = [
    Fore.rgb(255, 118, 164),  # Pink
    Fore.rgb(255, 255, 255),  # White
    Fore.rgb(192, 17, 215),  # Purple
    Fore.rgb(44, 44, 44),  # Black (adjusted for visibility)
    Fore.rgb(47, 60, 190),  # Blue
]
AGENDER = [
    Fore.rgb(44, 44, 44),  # Black (adjusted for visibility)
    Fore.rgb(188, 196, 199),  # Gray
    Fore.rgb(255, 255, 255),  # White
    Fore.rgb(183, 246, 132),  # Green
    Fore.rgb(255, 255, 255),  # White
    Fore.rgb(188, 196, 199),  # Gray
    Fore.rgb(44, 44, 44),  # Black (adjusted for visibility)
]
BIGENDER = [
    Fore.rgb(196, 121, 162),  # Pink
    Fore.rgb(237, 165, 205),  # Light pink
    Fore.rgb(214, 199, 232),  # Lavender
    Fore.rgb(255, 255, 255),  # White
    Fore.rgb(214, 199, 232),  # Lavender
    Fore.rgb(154, 199, 232),  # Light blue
    Fore.rgb(109, 130, 209),  # Blue
]


DESIGNS = [
    RAINBOW,
    TRANS,
    NB,
    NB_WARTIME,
    GENDERQUEER,
    GENDERFLUID,
    AGENDER,
    BIGENDER,
]


def pride(text: str, chunks: int = 1) -> str:
    """Rainbow text"""
    pride = random.choice(DESIGNS)
    return (
        "".join(
            f"{pride[i % len(pride)]}{''.join(c)}"
            for i, c in enumerate(batched(text, chunks))
        )
        + f"{RESET}"
    )
