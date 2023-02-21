from .board_state import (
    BoardState,
    BoardStateUpdates,
    PieceType,
    Position,
)
from .checkerserror import CheckersError
from .movement import Move
from .pieces import PieceColor
from .rule_set_interface import RuleSet


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
            BoardStateUpdates if move is legal, CheckersError if move is illegal.
        """
        if move.target_position == move.starting_position:
            return CheckersError(
                "Target position must be different than starting position",
            )
        occupant = board_state.occupancies.get(move.starting_position)
        if occupant is None:
            return CheckersError("There is no piece at starting position")
        if occupant.value.color != current_player:
            return CheckersError("The piece at starting position is the wrong color")

        return BoardStateUpdates(
            {
                move.starting_position: None,
                move.target_position: occupant,
            },
        )

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
