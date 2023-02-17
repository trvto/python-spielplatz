from dataclasses import dataclass

from python_spielplatz.checkers.boardstate import BoardState, Position


@dataclass
class Move:
    """Defines a move."""

    starting_position: Position
    target_position: Position


def make_move(move: Move, board_state: BoardState) -> BoardState:
    """Given a move and the current board state, return the resulting board state.

    This method simply sets the
    """
    if move.starting_position == move.target_position:
        return board_state
    return board_state
