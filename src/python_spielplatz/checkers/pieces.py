from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class PieceColor(Enum):
    """The colors that pieces can have."""

    WHITE = 0
    BLACK = 1

    def __str__(self) -> str:
        """Convert color Enum to string."""
        if self == PieceColor.WHITE:
            return "WHITE"
        return "BLACK"

    def next_up(self) -> PieceColor:
        """Return color who is up next."""
        if self == PieceColor.WHITE:
            return PieceColor.BLACK
        return PieceColor.WHITE


class Rank(Enum):
    """The ranks that pieces can have."""

    SOLDIER = 0
    QUEEN = 1


@dataclass(frozen=True)
class Piece:
    """A class that defines a single piece."""

    color: PieceColor
    rank: Rank
