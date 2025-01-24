"""
# Transdoc / Source pos

Definition for `SourcePos` class.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class SourcePos:
    """
    A position within a source file.
    """

    row: int
    """File row (1-indexed)"""
    col: int
    """File col (1-indexed)"""

    @staticmethod
    def zero() -> "SourcePos":
        """
        A zeroed source position. This indicates that an error associated with
        the file as a whole, rather than at a particular position in the file.
        """
        return SourcePos(0, 0)

    def __str__(self) -> str:
        return f"{self.row}:{self.col}"

    def __add__(self, other: "SourcePos") -> "SourcePos":
        if other.row == 1:
            # No change in row, offset column
            return SourcePos(self.row, self.col + other.col - 1)
        else:
            # Change in row, use other col
            return SourcePos(self.row + other.row - 1, other.col)

    def offset_by_str(self, string: str) -> "SourcePos":
        """
        Return a new `SourcePos` offset by the contents of the given string.
        """
        row_offset = string.count("\n")

        if row_offset == 0:
            return SourcePos(self.row, self.col + len(string))
        else:
            last_row = string.rsplit("\n", 1)[-1]
            return SourcePos(self.row + row_offset, len(last_row) + 1)


@dataclass(frozen=True)
class SourceRange:
    """
    A range of positions within a source file.

    Range is from `start <= p < end`.
    """

    start: SourcePos
    """Start position"""
    end: SourcePos
    """End position (exclusive)"""

    @staticmethod
    def zero():
        """
        A zeroed source position. This indicates that an error associated with
        the file as a whole, rather than at a particular position in the file.
        """
        return SourceRange(
            SourcePos.zero(),
            SourcePos.zero(),
        )
