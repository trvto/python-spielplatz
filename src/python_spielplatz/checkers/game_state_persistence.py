import logging
import pathlib
import pickle
import uuid
from dataclasses import dataclass
from tempfile import gettempdir
from uuid import UUID

import click

from python_spielplatz.checkers.board_state import BoardState
from python_spielplatz.checkers.checkerserror import CheckersError
from python_spielplatz.checkers.game_state import GameState
from python_spielplatz.checkers.standard_rule_set import RuleSet


@dataclass
class GlobalSettings:
    """Global settings."""

    current_game_identifier: UUID


@dataclass
class Game:
    """Info for a unique game."""

    game_id: UUID
    game_state: GameState


class GameStateManager:
    """Manage game states.

    Save and load games states to temporary files and keep track of global game settings
    """

    _cli_cache_dir = "checkers_cache"
    _cli_cache_dir_path = pathlib.Path(gettempdir(), _cli_cache_dir)
    _cli_cache_settings_path = pathlib.Path(_cli_cache_dir_path, "settings.pkl")

    @classmethod
    def try_get_current_game_settings(cls) -> GlobalSettings | CheckersError:
        """load settings from disk.

        Returns:
            Global settings if a settings.pkl file is found, otherwise Error
        """
        if not cls._cli_cache_settings_path.exists():
            return CheckersError(
                f"Settings file {cls._cli_cache_settings_path} does not exist",
            )
        with cls._cli_cache_settings_path.open("rb") as settings_file:
            return pickle.load(settings_file)

    @classmethod
    def try_update_current_game_settings(
        cls,
        game_settings: GlobalSettings,
    ) -> None | CheckersError:
        """tries to update global settings using the given object.

        Args:
            game_settings: A Global settings object to persist on file

        Returns:
            None if successful, Error otherwise
        """
        try:
            cls._cli_cache_dir_path.mkdir(parents=True, exist_ok=True)
            with cls._cli_cache_settings_path.open("wb") as settings_file:
                pickle.dump(game_settings, settings_file)
        except OSError:
            return CheckersError(
                f"Error writing to settings file {cls._cli_cache_settings_path}",
            )
        return None

    @classmethod
    def try_load_default_game(cls) -> Game | CheckersError:
        """tries to load default game state from file.

        Returns:
            GameState object of current default game if successful, Error otherwise
        """
        game_settings = cls.try_get_current_game_settings()
        if isinstance(game_settings, CheckersError):
            return CheckersError(
                f"Could not retrieve default game from settings: {game_settings.error_message}",
            )
        game_id = game_settings.current_game_identifier
        game_path = pathlib.Path(cls._cli_cache_dir_path, f"{game_id}.pkl")
        if not game_path.exists():
            return CheckersError(f"Default game state file {game_path} does not exist")
        with game_path.open("rb") as game_file:
            return Game(game_id=game_id, game_state=pickle.load(game_file))

    @classmethod
    def try_load_game_from_id(cls, game_id: UUID) -> Game | CheckersError:
        """tries to load game state from file for a given game id.

        Args:
            game_id: id of the game to load

        Returns:
            GameState object if successful, Error otherwise
        """
        game_path = pathlib.Path(cls._cli_cache_dir_path, f"{game_id}.pkl")

        if not game_path.exists():
            return CheckersError(f"Expected game state file {game_path} does not exist")

        with game_path.open("rb") as game_file:
            return Game(game_id=game_id, game_state=pickle.load(game_file))

    @classmethod
    def get_game_list(cls) -> list[str]:
        """Constructs a list of running games on file.

        Returns:
            a list of game ids in str format
        """
        if not cls._cli_cache_dir_path.exists():
            logging.warning(
                "No games found because cache directory %s does not exist",
                cls._cli_cache_dir_path,
            )
            return []
        path_strings = [str(path.stem) for path in cls._cli_cache_dir_path.iterdir()]
        if "settings" in path_strings:
            path_strings.remove("settings")
        return path_strings

    @classmethod
    def clear_games(cls) -> None:
        """Deletes all saved game states and global settings."""
        if not cls._cli_cache_dir_path.exists():
            return
        paths = list(cls._cli_cache_dir_path.iterdir())
        if not paths:
            return
        if click.confirm(
            f"Confirm deletion of these files within {cls._cli_cache_dir_path}",
        ):
            for path in paths:
                path.unlink()
        return

    @classmethod
    def try_save_game_state(
        cls,
        game_id: UUID,
        game_state: GameState,
    ) -> None | CheckersError:
        """tries to save game state to a file for a given game id.

        Args:
            game_id: id of the game to save
            game_state: the state of the game

        Returns:
            None if successful, Error otherwise
        """
        try:
            cls._cli_cache_dir_path.mkdir(parents=True, exist_ok=True)
            game_path = pathlib.Path(cls._cli_cache_dir_path, f"{game_id}.pkl")
            with game_path.open("wb") as game_file:
                pickle.dump(game_state, game_file)
        except OSError:
            return CheckersError(
                f"Error writing to game state file {cls._cli_cache_settings_path}",
            )
        return None

    @classmethod
    def initialize_new_game(
        cls,
        rule_set: RuleSet,
    ) -> Game | CheckersError:
        """Creates a new game and sets it as the default game.

        Args:
            rule_set: the rule set to use for the new game

        Returns:
            tuple (id, initial game state) of the created game if successful, tuple (None, Error) otherwise
        """
        game_state = GameState(
            rule_set=rule_set,
            board_state=BoardState(
                occupancies=rule_set.initial_game_occupancies(),
            ),
            whose_turn=rule_set.first_player(),
        )
        game_id = uuid.uuid4()
        save_result = cls.try_save_game_state(game_id, game_state)
        if isinstance(save_result, CheckersError):
            return save_result
        return Game(game_id=game_id, game_state=game_state)
