from abc import (
    ABC,
    abstractmethod,
)
from dataclasses import dataclass

from python_spielplatz.checkers.boardstate import BoardState, PieceType, Position
from python_spielplatz.checkers.pieces import PieceColor


@dataclass
class Move:
    """Defines a move."""

    starting_position: Position
    target_position: Position


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
    ) -> bool:
        """is this move allowed given board state.

        Args:
            move: The move in question
            board_state: the current state of the board
            current_player: color of player whose turn it is

        Returns:
            True if move is legal, False if move is illegal.
        """

    @staticmethod
    @abstractmethod
    def initial_game_occupancies() -> dict[Position, PieceType]:
        """Return the occupancies of the board at the beginning of the game."""

    @staticmethod
    @abstractmethod
    def first_player() -> PieceColor:
        """which player color is allowed to go first."""


class StandardRuleSet(RuleSet):
    """The standard rule set.

    - No moves are forced.
    - Movement without capture is always one diagonal position at a time
    - A capture is possible if:
       1. The piece is next to an enemy
       2. From the pieces perspective the position on the other side of the enemy is unoccupied
    - To capture, a piece "jumps" over the enemy
    - Soldiers can only move diagonally "up". Any number of captures are allowed moving diagonally "up".
    - Queens can move in any diagonal direction. Any number of captures are allowed.
    - Soldiers become queens by reaching the end of the board
    """

    @staticmethod
    def is_legal_move(
        move: Move,
        board_state: BoardState,
        current_player: PieceColor,
    ) -> bool:
        """is this move allowed given board state.

        Args:
            move: The move in question
            board_state: the current state of the board
            current_player: color of player whose turn it is

        Returns:
            True if move is legal, False if move is illegal.
        """
        if move.target_position == move.starting_position:
            return False
        occupant = board_state.occupancies.get(move.starting_position)
        if occupant is None:
            return False
        if occupant.value.color != current_player:
            return False
        return True

    @staticmethod
    def initial_game_occupancies() -> dict[Position, PieceType]:
        """Return the occupancies of the board at the beginning of the game."""
        occupancies = {}
        for column in range(0, 8, 2):
            for row in range(0, 3):
                occupancies[Position(row, column + row % 2)] = PieceType.WHITE_SOLDIER
            for row in range(5, 8):
                occupancies[Position(row, column + row % 2)] = PieceType.BLACK_SOLDIER
        return occupancies

    @staticmethod
    def first_player() -> PieceColor:
        """which player color is allowed to go first."""
        return PieceColor.WHITE
