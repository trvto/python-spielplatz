from dataclasses import dataclass

from python_spielplatz.checkers.board_state import BoardState
from python_spielplatz.checkers.pieces import PieceColor
from python_spielplatz.checkers.standard_rule_set import RuleSet


@dataclass
class GameState:
    """Holds the state of a game."""

    board_state: BoardState
    rule_set: RuleSet
    whose_turn: PieceColor
