from enum import Enum
from dataclasses import dataclass


class Color(Enum):
    WHITE = 0
    BLACK = 1

    def __str__(self) -> str:
        match self:
            case Color.WHITE:
                return "WHITE"
            case Color.BLACK:
                return "BLACK"


class Rank(Enum):
    SOLDIER = 0
    QUEEN = 1


@dataclass
class Piece:
    color: Color
    rank: Rank


