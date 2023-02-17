"""Cli for checkers game."""
import uuid

import click

from python_spielplatz.checkers.boardstate import position_from_position_str
from python_spielplatz.checkers.game_state_persistence import (
    GameStateManager,
    GlobalSettings,
)
from python_spielplatz.checkers.rule_sets import StandardRuleSet

from . import __version__


@click.group()
@click.version_option(version=__version__)
def main() -> None:
    """This a checkers game command line interface."""


@click.command(name="new-game")
def new() -> None:
    """Initialize a new game."""
    game_state_manager = GameStateManager()
    game_id = game_state_manager.initialize_new_game(StandardRuleSet())
    game_state_manager.try_update_current_game_settings(
        GlobalSettings(current_game_identifier=game_id),
    )
    current_game_state = game_state_manager.try_load_game_state(game_id)
    print(f" Game: {game_id}")
    print(f" It's now {current_game_state.whose_turn}'s turn\n")
    print(current_game_state.board_state)


@click.command(name="list")
def list_games() -> None:
    """Initialize a new game."""
    game_state_manager = GameStateManager()
    games = game_state_manager.get_game_list()
    if not games:
        print("Currently no saved games")
    for game in games:
        print(game)


@click.command()
def clear() -> None:
    """Initialize a new game."""
    game_state_manager = GameStateManager()
    game_state_manager.clear_games()


@click.command()
@click.option("-g", "--game-id", type=uuid.UUID)
def show(game_id: uuid.UUID) -> None:
    """Show state of game."""
    game_state_manager = GameStateManager()
    if not game_id:
        game_settings = game_state_manager.try_get_current_game_settings()
        if not game_settings:
            print("No game id provided and no default game id found")
        game_id = game_settings.current_game_identifier
    current_game_state = game_state_manager.try_load_game_state(game_id)
    if not current_game_state:
        print(f"Could not load state for game {game_id}, does this game exist?")
    print(f" Game: {game_id}")
    print(f" It's now {current_game_state.whose_turn}'s turn\n")
    print(current_game_state.board_state)


@click.command(
    help="Move piece at PIECE_POSITION along MOVE_PATH. MOVE_PATH is a space separated list of Positions",
)
@click.argument("piece_position", nargs=1, type=str)
@click.argument("move_path", nargs=-1, required=True, type=str)
def move(piece_position: str, move_path: str) -> None:
    """Make a move."""
    start = position_from_position_str(piece_position)
    if start is None:
        print("Position 1 is il-formatted, try again")
        return
    target_sequence = [position_from_position_str(pos) for pos in move_path]
    for i, pos in enumerate(target_sequence):
        if pos is None:
            print(f"Position {i+2} is il-formatted, try again")
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
