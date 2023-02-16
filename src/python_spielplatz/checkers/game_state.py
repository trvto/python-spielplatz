from dataclasses import dataclass
from python_spielplatz.checkers.boardstate import BoardState
from python_spielplatz.checkers.pieces import Color
from python_spielplatz.checkers.rule_sets import RuleSet


@dataclass
class GameState:
    board_state: BoardState
    rule_set: RuleSet
    whose_turn: Color

