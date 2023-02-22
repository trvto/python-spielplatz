"""Cli for checkers game."""
import itertools
import uuid

import click

from . import __version__
from .board_state import Position, position_from_position_str
from .checkerserror import CheckersError
from .game_state import try_make_moves
from .game_state_persistence import (
    Game,
    GameStateManager,
    GlobalSettings,
)
from .movement import Move
from .rule_set_map import get_rule_set


@click.group()
@click.version_option(version=__version__)
def main() -> None:
    """This a checkers game with a command line interface."""


@click.command(name="new-game")
@click.option("-r", "--rule-set", "rule_set_str", type=str, default="StandardRuleSet")
def new(rule_set_str: str) -> None:
    """Initialize a new game."""
    rule_set = get_rule_set(rule_set_str)
    if isinstance(rule_set, CheckersError):
        print(rule_set.error_message)
        return

    result = GameStateManager.initialize_new_game(
        rule_set,
    )
    if isinstance(result, CheckersError):
        print(f"Error initializing game: {result.error_message}")
        return

    update_result = GameStateManager.update_global_checkers_settings(
        GlobalSettings(current_game_identifier=result.game_id),
    )
    if isinstance(update_result, CheckersError):
        print(update_result.error_message)
    print(f" New game: {result.game_id}")
    print(result.game_state.board_state)
    print(f"  -> {result.game_state.whose_turn} to play")


@click.command(name="list")
def list_games() -> None:
    """List all saved games."""
    games = GameStateManager.get_saved_game_list()
    if not games:
        print("Currently no saved games")
    for game in games:
        print(game)


@click.command()
def clear() -> None:
    """Clear all saved games."""
    GameStateManager.clear_saved_games()


@click.command()
@click.option("-g", "--game-id", type=uuid.UUID)
def show(game_id: uuid.UUID | None) -> None:
    """Show state of game. If no game id is provided, show game saved as current."""
    current_game = _try_load_game(game_id)
    if isinstance(current_game, CheckersError):
        print(current_game.error_message)
        return
    print(f" Game: {current_game.game_id}")
    print(current_game.game_state.board_state)
    print(f"  -> {current_game.game_state.whose_turn} to play")


@click.command(name="move")
@click.option("-g", "--game-id", type=uuid.UUID)
@click.argument("move_path", nargs=-1, required=True, type=str)
def perform_move_sequence(game_id: uuid.UUID | None, move_path: list[str]) -> None:
    """Move piece along MOVE_PATH.

    MOVE_PATH is a space separated list of positions that the piece should move through

    Positions are given in the format "<row>,<column>", where <row> and <column> are integers.

    The first position in MOVE_PATH is the starting position. This position must be occupied by a piece belonging
    to the current player
    """
    position_sequence = _get_position_sequence_from_input_move_path(move_path)
    if isinstance(position_sequence, CheckersError):
        print(position_sequence.error_message)
        return

    move_list = [
        Move(starting_position=position_start, target_position=position_end)
        for position_start, position_end in itertools.pairwise(position_sequence)
    ]

    current_game = _try_load_game(game_id)
    if isinstance(current_game, CheckersError):
        print(current_game.error_message)
        return

    new_game_state = try_make_moves(move_list, current_game.game_state)
    if isinstance(new_game_state, CheckersError):
        print(new_game_state.error_message)
        return

    GameStateManager.save_game_state(current_game.game_id, new_game_state)

    print(f" Game: {current_game.game_id}")
    print(new_game_state.board_state)
    print(f"  -> {new_game_state.whose_turn} to play")


main.add_command(new)
main.add_command(show)
main.add_command(list_games)
main.add_command(clear)
main.add_command(perform_move_sequence)


def _get_position_sequence_from_input_move_path(
    move_path: list[str],
) -> list[Position] | CheckersError:
    position_sequence = []
    for i, position_str in enumerate(move_path, start=1):
        position = position_from_position_str(position_str)
        if isinstance(position, CheckersError):
            return CheckersError(
                f"Error in argument {i}, '{position_str}': {position.error_message}",
            )
        position_sequence.append(position)
    return position_sequence


def _try_load_game(game_id: uuid.UUID | None) -> Game | CheckersError:
    """Retrieve game state.

    Args:
        game_id: game id as UUID or None to use default game.

    Returns:
        game state for given uuid or default game state if None, Checkers Error on load error
    """
    if game_id is None:
        return GameStateManager.load_default_game()
    return GameStateManager.load_game_from_id(game_id)
