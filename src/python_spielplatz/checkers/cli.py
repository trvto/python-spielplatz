import uuid

from typing import Union
import click
from python_spielplatz.checkers.game_state_persistence import GameStateManager, GameSettings
from python_spielplatz.checkers.rule_sets import StandardRuleSet


from . import __version__


@click.group()
@click.version_option(version=__version__)
def main():
    """This a checkers game command line interface."""
    pass

@click.command()
def new():
    """Initialize a new game."""
    game_state_manager = GameStateManager()
    game_id = game_state_manager.initialize_new_game(StandardRuleSet())
    game_state_manager.try_update_current_game_settings(
        GameSettings(current_game_identifier=game_id))
    current_game_state = game_state_manager.try_get_current_game_state(game_id)
    print(f" Game: {game_id}")
    print(f" It's now {current_game_state.whose_turn}'s turn\n")
    print(current_game_state.board_state)

@click.command()
def list():
    """Initialize a new game."""
    game_state_manager = GameStateManager()
    games = game_state_manager.list_games()
    if not games:
        print("Currently no saved games")
    for game in games:
        print(game)

@click.command()
def clear():
    """Initialize a new game."""
    game_state_manager = GameStateManager()
    game_state_manager.clear_games()

@click.command()
@click.option('-g', "--game-id", type=uuid.UUID)
def show(game_id):
    """Show state of game."""
    game_state_manager = GameStateManager()
    if not game_id:
        game_settings = game_state_manager.try_get_current_game_settings()
        if not game_settings:
            print("No game id provided and no default game id found")
        game_id = game_settings.current_game_identifier
    current_game_state = game_state_manager.try_get_current_game_state(game_id)
    if not current_game_state:
        print(f"Could not load state for game {game_id}, does this game exist?")
        return
    print(f" Game: {game_id}")
    print(f" It's now {current_game_state.whose_turn}'s turn\n")
    print(current_game_state.board_state)


@click.command(help="Move piece at PIECE_POSITION along PATH. PATH is a space separated list of Positions")
@click.argument('piece_position', nargs=1)
@click.argument('path', nargs=-1, required=True)
def move(piece_position, path):
    """Make a move."""
    print(f" {piece_position} ", end="->")
    for position in path[:-1]:
        print(f" {position} ", end="->")
    print(f" {path[-1]}")


main.add_command(new)
main.add_command(show)
main.add_command(list)
main.add_command(clear)
main.add_command(move)
