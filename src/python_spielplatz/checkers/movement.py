from dataclasses import dataclass

from .board_state import Position
from .checkerserror import CheckersError
from .game_state import GameState


@dataclass
class Move:
    """Defines a move."""

    starting_position: Position
    target_position: Position


def try_make_move(move: Move, game_state: GameState) -> GameState | CheckersError:
    """Given a move and the current game state, return the resulting board state.

    This method simply sets the
    """
    game_state.rule_set.try_make_move(
        move,
        game_state.board_state,
        game_state.whose_turn,
    )
    return game_state
