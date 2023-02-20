from abc import ABC, abstractmethod

from python_spielplatz.checkers.board_state import (
    BoardState,
    BoardStateUpdates,
    PieceType,
    Position,
)
from python_spielplatz.checkers.movement import Move
from python_spielplatz.checkers.pieces import PieceColor


class RuleSet(ABC):
    """Interface to a rule set.

    Anything a rule set needs is defined here
    """

    @staticmethod
    @abstractmethod
    def is_legal_move(
        move: Move,
        board_state: BoardState,
        current_player: PieceColor,
    ) -> BoardStateUpdates | None:
        """is this move allowed given board state.

        Args:
            move: The move in question
            board_state: the current state of the board
            current_player: color of player whose turn it is

        Returns:
            Board state updates if move is legal, None if move is illegal.
        """

    @staticmethod
    @abstractmethod
    def initial_game_occupancies() -> dict[Position, PieceType]:
        """Return the occupancies of the board at the beginning of the game."""

    @staticmethod
    @abstractmethod
    def first_player() -> PieceColor:
        """which player color is allowed to go first."""
