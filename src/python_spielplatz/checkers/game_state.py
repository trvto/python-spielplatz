from copy import deepcopy
from dataclasses import dataclass

from .board_state import BoardState
from .checkerserror import CheckersError
from .movement import Move
from .pieces import PieceColor
from .standard_rule_set import RuleSet


@dataclass(frozen=True)
class GameState:
    """Holds the state of a game."""

    board_state: BoardState
    rule_set: RuleSet
    whose_turn: PieceColor


def try_make_moves(
    moves: list[Move],
    game_state: GameState,
) -> GameState | CheckersError:
    """Given a move and the current game state, return the resulting game state.

    Args:
        moves: a list of moves to make
        game_state: current state of the game

    Returns:
        If moves sequence is valid, the resulting game state, otherwise an Error
    """
    board_state = deepcopy(game_state.board_state)
    for i, move in enumerate(moves, start=1):
        board_state_updates = game_state.rule_set.try_make_move(
            move,
            board_state,
            game_state.whose_turn,
        )
        if isinstance(board_state_updates, CheckersError):
            return CheckersError(
                f"Error encountered during move {i}: {board_state_updates.error_message}",
            )
        board_state.update(board_state_updates)

    return GameState(
        rule_set=game_state.rule_set,
        board_state=board_state,
        whose_turn=game_state.whose_turn.next_up(),
    )
