from abc import ABC, abstractmethod

from python_spielplatz.checkers.board_state import (
    BoardState,
    BoardStateUpdates,
    PieceType,
    Position,
)

from .checkerserror import CheckersError
from .movement import Move
from .pieces import PieceColor


class RuleSet(ABC):
    """Interface to a rule set.

    Anything a rule set needs is defined here
    """

    @staticmethod
    @abstractmethod
    def try_make_move(
        move: Move,
        board_state: BoardState,
        current_player: PieceColor,
    ) -> BoardStateUpdates | CheckersError:
        """Try to make move, given current board state.

        Args:
            move: The move in question
            board_state: the current state of the board
            current_player: color of player whose turn it is

        Returns:
            Board state updates if move is legal, CheckersError if move is illegal.
        """

    @staticmethod
    @abstractmethod
    def initial_game_occupancies() -> dict[Position, PieceType]:
        """Return the occupancies of the board at the beginning of the game."""

    @staticmethod
    @abstractmethod
    def first_player() -> PieceColor:
        """which player color is allowed to go first."""
