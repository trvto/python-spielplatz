"""A class for storing board data"""
from enum import Enum
from python_spielplatz.checkers.pieces import Piece, Color, Rank
from attrs import define


@define
class Position:
    row: int
    column: int

    def __hash__(self) -> int:
        return (self.row, self.column).__hash__()


class Occupancy(Enum):
    WHITE_SOLDIER = Piece(color=Color.WHITE, rank=Rank.SOLDIER)
    BLACK_SOLDIER = Piece(color=Color.BLACK, rank=Rank.SOLDIER)
    WHITE_QUEEN = Piece(color=Color.WHITE, rank=Rank.QUEEN)
    BLACK_QUEEN = Piece(color=Color.BLACK, rank=Rank.QUEEN)


@define
class BoardState:
    occupancies: dict[Position, Occupancy]

    def __str__(self) -> str:
        state_str = "   " + "*"*(8*4 + 1)
        for row in range(7, -1, -1):
            state_str += f"\n {row} |"
            for col in range(0, 8):
                if (row + col) % 2 == 1:
                    state_str += "***"
                    state_str += "|"
                    continue
                match self.occupancies.get(Position(row=row, column=col)):
                    case None:
                        state_str += "   |"
                    case Occupancy.WHITE_SOLDIER:
                        state_str += " w |"
                    case Occupancy.BLACK_SOLDIER:
                        state_str += " b |"
                    case Occupancy.WHITE_QUEEN:
                        state_str += " W |"
                    case Occupancy.BLACK_QUEEN:
                        state_str += " B |"
            state_str += "\n"
            state_str += "   " + "*"*(8*4 + 1)
        state_str += "\n  "
        state_str += "   0"
        state_str += "   1"
        state_str += "   2"
        state_str += "   3"
        state_str += "   4"
        state_str += "   5"
        state_str += "   6"
        state_str += "   7"
        state_str += "\n"
        return state_str
