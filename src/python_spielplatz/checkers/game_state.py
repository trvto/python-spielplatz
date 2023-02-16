from dataclasses import dataclass

from python_spielplatz.checkers.boardstate import BoardState
from python_spielplatz.checkers.pieces import PieceColor
from python_spielplatz.checkers.rule_sets import RuleSet


@dataclass
class GameState:
    """The state of a game.

    Data:
      board_state: The current state of the game board.
      rule_set: The rule set being applied to this game.
      whose_turn: Which color piece is currently allowed to move.
    """

    board_state: BoardState
    rule_set: RuleSet
    whose_turn: PieceColor
