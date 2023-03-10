"""A class for storing board data."""
from __future__ import annotations

import re
from dataclasses import dataclass
from enum import Enum

from python_spielplatz.checkers.checkerserror import CheckersError
from python_spielplatz.checkers.pieces import Piece, PieceColor, Rank


@dataclass(frozen=True)
class Position:
    """A position on the board."""

    row: int
    column: int

    def __str__(self) -> str:
        """Convert to str."""
        return f"{self.row},{self.column}"


def position_from_position_str(position_string: str) -> Position | CheckersError:
    """Create a Position object from a position string.

    Function accepts strings that are any two integers separated by a comma

    Args:
        position_string: a string in the format "<row_integer>,<column_integer>"

    Returns:
        a Position object with row and column set from the position string or None
        if conversion failed
    """
    # check that string is exactly two integers, separated by a comma
    if not re.fullmatch(r"[0-9]+,[0-9]+", position_string):
        return CheckersError(
            "invalid syntax, a position string must have the form <row_integer>,<column_integer>",
        )
    position_int_array = [int(int_string) for int_string in position_string.split(",")]
    return Position(row=position_int_array[0], column=position_int_array[1])


class PieceType(Enum):
    """Types of pieces."""

    WHITE_SOLDIER = Piece(color=PieceColor.WHITE, rank=Rank.SOLDIER)
    BLACK_SOLDIER = Piece(color=PieceColor.BLACK, rank=Rank.SOLDIER)
    WHITE_QUEEN = Piece(color=PieceColor.WHITE, rank=Rank.QUEEN)
    BLACK_QUEEN = Piece(color=PieceColor.BLACK, rank=Rank.QUEEN)


@dataclass
class BoardStateUpdates:
    """A list of updates to the state of the board.

    Params:
    occupancy_updates: positions to update, and the piece (or no piece) that is now there
    """

    occupancy_updates: dict[Position, PieceType | None]


@dataclass
class BoardState:
    """The state of the checkerboard.

    Params:
    occupancies: which positions are occupied with which piece types
    """

    occupancies: dict[Position, PieceType]

    def update(self, board_state_updates: BoardStateUpdates) -> None:
        """Update board state from board state updates spec."""
        for position, update in board_state_updates.occupancy_updates.items():
            if update is None:
                self.occupancies.pop(position)
            else:
                self.occupancies[position] = update

    def __str__(self) -> str:
        """Represent board state as a multi-line string."""
        state_str = "   " + "*" * (8 * 4 + 1)
        for row in range(7, -1, -1):
            state_str += f"\n {row} |"
            for col in range(0, 8):
                if (row + col) % 2 == 1:
                    state_str += "***"
                    state_str += "|"
                    continue
                occupancy = self.occupancies.get(Position(row=row, column=col))
                if occupancy is None:
                    state_str += "   |"
                if occupancy == PieceType.WHITE_SOLDIER:
                    state_str += " w |"
                if occupancy == PieceType.BLACK_SOLDIER:
                    state_str += " b |"
                if occupancy == PieceType.WHITE_QUEEN:
                    state_str += " W |"
                if occupancy == PieceType.BLACK_QUEEN:
                    state_str += " B |"
            state_str += "\n"
            state_str += "   " + "*" * (8 * 4 + 1)
        state_str += "\n  "
        for i in range(8):
            state_str += f"   {i}"
        state_str += "\n"
        return state_str
