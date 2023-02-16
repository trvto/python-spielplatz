from dataclasses import dataclass
from abc import (
    ABC,
    abstractmethod,
)
from python_spielplatz.checkers.boardstate import Position, Occupancy, BoardState
from python_spielplatz.checkers.pieces import Color


@dataclass
class Move:
    starting_position: Position
    target_position: Position


class RuleSet(ABC):
    @staticmethod
    @abstractmethod
    def is_legal_move(move: Move, board_state: BoardState) -> bool:
        pass

    @staticmethod
    @abstractmethod
    def initial_game_occupancies() -> dict[Position, Occupancy]:
        pass

    @staticmethod
    @abstractmethod
    def first_player() -> Color:
        pass


class StandardRuleSet(RuleSet):
    @staticmethod
    def is_legal_move(move: Move, board_state: BoardState) -> bool:
        return True

    @staticmethod
    def initial_game_occupancies() -> dict[Position, Occupancy]:
        occupancies = {}
        for column in range(0, 8, 2):
            for row in range(0, 3):
                occupancies[Position(row, column + row % 2)] = Occupancy.WHITE_SOLDIER
            for row in range(5, 8):
                occupancies[Position(row, column + row % 2)] = Occupancy.BLACK_SOLDIER
        return occupancies

    @staticmethod
    def first_player() -> Color:
        return Color.WHITE
