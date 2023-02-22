from dataclasses import dataclass

from .board_state import Position


@dataclass(frozen=True)
class Move:
    """Defines a move."""

    starting_position: Position
    target_position: Position
