"""Cli for checkers game."""
import uuid

import click

from python_spielplatz.checkers.standard_rule_set import StandardRuleSet

from . import __version__
from .board_state import position_from_position_str
from .checkerserror import CheckersError
from .game_state_persistence import (
    Game,
    GameStateManager,
    GlobalSettings,
)


@click.group()
@click.version_option(version=__version__)
def main() -> None:
    """This a checkers game with a command line interface."""


@click.command(name="new-game")
def new() -> None:
    """Initialize a new game."""
    result = GameStateManager.initialize_new_game(
        StandardRuleSet(),
    )
    if isinstance(result, CheckersError):
        print(f"Error initializing game: {result.error_message}")
        return

    update_result = GameStateManager.try_update_current_game_settings(
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
    games = GameStateManager.get_game_list()
    if not games:
        print("Currently no saved games")
    for game in games:
        print(game)


@click.command()
def clear() -> None:
    """Clear all saved games."""
    GameStateManager.clear_games()


@click.command()
@click.option("-g", "--game-id", type=uuid.UUID)
def show(game_id: uuid.UUID | None) -> None:
    """Show state of game. If no game id is provided, show game saved as current."""
    current_game = try_load_game(game_id)
    if isinstance(current_game, CheckersError):
        print(current_game.error_message)
        return
    print(f" Game: {current_game.game_id}")
    print(current_game.game_state.board_state)
    print(f"  -> {current_game.game_state.whose_turn} to play")


@click.command()
@click.option("-g", "--game-id", type=uuid.UUID)
@click.argument("piece_position", nargs=1, type=str)
@click.argument("move_path", nargs=-1, required=True, type=str)
def move(game_id: uuid.UUID | None, piece_position: str, move_path: str) -> None:
    """Move piece at PIECE_POSITION along MOVE_PATH.

    PIECE_POSITION is the starting position given in the format "<row>,<column>",
    where <row> and <column> are integers.

    MOVE_PATH is a space separated list of positions that the piece should move through
    """
    start = position_from_position_str(piece_position)
    if isinstance(start, CheckersError):
        print(f"Error in argument 1, '{piece_position}': {start.error_message}")
        return
    target_sequence = [position_from_position_str(pos) for pos in move_path]
    for i, pos in enumerate(target_sequence):
        if isinstance(pos, CheckersError):
            print(f"Error in argument {i+2}, '{move_path[i]}': {pos.error_message}")
            return

    current_game = try_load_game(game_id)
    if isinstance(current_game, CheckersError):
        print(current_game.error_message)
        return

    print(f" {piece_position} ", end="->")
    for position in move_path[:-1]:
        print(f" {position} ", end="->")
    print(f" {move_path[-1]}")


main.add_command(new)
main.add_command(show)
main.add_command(list_games)
main.add_command(clear)
main.add_command(move)


def try_load_game(game_id: uuid.UUID | None) -> Game | CheckersError:
    """Retrieve game state.

    Args:
        game_id: game id as UUID or None to use default game.

    Returns:
        game state for given uuid or default game state if None, Checkers Error on load error
    """
    if game_id is None:
        return GameStateManager.try_load_default_game()
    return GameStateManager.try_load_game_from_id(game_id)
