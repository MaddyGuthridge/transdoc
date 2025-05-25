"""# Tests / Source pos test

Test cases for SourcePos and SourceRange classes.
"""

from transdoc.source_pos import SourcePos, SourceRange


def test_zero_pos():
    assert SourcePos.zero().row == 0
    assert SourcePos.zero().col == 0


def test_zero_range():
    assert SourceRange.zero().start == SourcePos.zero()
    assert SourceRange.zero().end == SourcePos.zero()


def test_stringify_pos():
    assert str(SourcePos(5, 10)) == "5:10"


def test_add_pos():
    assert SourcePos(2, 1) + SourcePos(2, 3) == SourcePos(3, 3)


def test_add_pos_col():
    assert SourcePos(2, 2) + SourcePos(1, 2) == SourcePos(2, 3)


def test_offset_pos_str():
    assert SourcePos(2, 2).offset_by_str("12345") == SourcePos(2, 7)


def test_offset_pos_str_newline():
    assert SourcePos(2, 2).offset_by_str("a\nb\n123") == SourcePos(4, 4)
