import pathlib
import pickle
import uuid
from dataclasses import dataclass
from tempfile import gettempdir
from uuid import UUID

import click

from python_spielplatz.checkers.boardstate import BoardState
from python_spielplatz.checkers.game_state import GameState
from python_spielplatz.checkers.standard_rule_set import RuleSet


@dataclass
class GlobalSettings:
    """Global settings."""

    current_game_identifier: UUID


class GameStateManager:
    """Manage game states.

    Save and load games states to temporary files and keep track of global game settings
    """

    _cli_cache_dir = "checkers_cache"
    _cli_cache_dir_path = pathlib.Path(gettempdir(), _cli_cache_dir)
    _cli_cache_settings_path = pathlib.Path(_cli_cache_dir_path, "settings.pkl")

    def try_get_current_game_settings(self) -> None | GlobalSettings:
        """load settings from disk.

        Returns:
            Global settings if a settings.pkl file is found, otherwise None
        """
        if not self._cli_cache_settings_path.exists():
            return None
        with self._cli_cache_settings_path.open("rb") as settings_file:
            return pickle.load(settings_file)

    def try_update_current_game_settings(self, game_settings: GlobalSettings) -> bool:
        """tries to update global settings using the given object.

        Args:
            game_settings: A Global settings object to persist on file

        Returns:
            True if successful, False otherwise
        """
        try:
            self._cli_cache_dir_path.mkdir(parents=True, exist_ok=True)
            with self._cli_cache_settings_path.open("wb") as settings_file:
                pickle.dump(game_settings, settings_file)
        except OSError:
            return False
        return True

    def try_load_game_state(self, game_id: UUID) -> None | GameState:
        """tries to load game state from file for a given game id.

        Args:
            game_id: id of the game to load

        Returns:
            GameState object if successful, None otherwise
        """
        game_path = pathlib.Path(self._cli_cache_dir_path, f"{game_id}.pkl")
        if not game_path.exists():
            return None
        with game_path.open("rb") as game_file:
            return pickle.load(game_file)

    def get_game_list(self) -> list[str]:
        """Constructs a list of running games on file.

        Returns:
            a list of game ids in str format
        """
        if not self._cli_cache_dir_path.exists():
            return []
        path_strings = [str(path.stem) for path in self._cli_cache_dir_path.iterdir()]
        if "settings" in path_strings:
            path_strings.remove("settings")
        return path_strings

    def clear_games(self) -> None:
        """Deletes all saved game states and global settings."""
        if not self._cli_cache_dir_path.exists():
            return
        paths = list(self._cli_cache_dir_path.iterdir())
        if not paths:
            return
        if click.confirm(
            f"Confirm deletion of these files within {self._cli_cache_dir_path}",
        ):
            for path in paths:
                path.unlink()

    def try_save_game_state(self, game_id: UUID, game_state: GameState) -> bool:
        """tries to save game state to a file for a given game id.

        Args:
            game_id: id of the game to save
            game_state: the state of the game

        Returns:
            True if successful, False otherwise
        """
        try:
            self._cli_cache_dir_path.mkdir(parents=True, exist_ok=True)
            game_path = pathlib.Path(self._cli_cache_dir_path, f"{game_id}.pkl")
            with game_path.open("wb") as game_file:
                pickle.dump(game_state, game_file)
        except OSError:
            return False
        return True

    def initialize_new_game(
        self,
        rule_set: RuleSet,
    ) -> tuple[UUID | None, GameState | None]:
        """Creates a new game and sets it as the default game.

        Args:
            rule_set: the rule set to use for the new game

        Returns:
            id of the created game if successful, None otherwise
        """
        game_state = GameState(
            rule_set=rule_set,
            board_state=BoardState(
                occupancies=rule_set.initial_game_occupancies(),
            ),
            whose_turn=rule_set.first_player(),
        )
        game_id = uuid.uuid4()
        if not self.try_save_game_state(game_id, game_state):
            return None, None
        return game_id, game_state
