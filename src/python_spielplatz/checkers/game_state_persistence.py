import uuid
from dataclasses import dataclass
import pathlib
import pickle
from tempfile import gettempdir
from typing import Union
from uuid import UUID
from python_spielplatz.checkers.rule_sets import RuleSet
from python_spielplatz.checkers.game_state import GameState
from python_spielplatz.checkers.boardstate import BoardState
import click


@dataclass
class GameSettings:
    current_game_identifier: UUID


class GameStateManager:
    _cli_cache_dir = "checkers_cache"
    _cli_cache_dir_path = pathlib.Path(gettempdir(), _cli_cache_dir)
    _cli_cache_settings_path = pathlib.Path(_cli_cache_dir_path, "settings.pkl")

    def try_get_current_game_settings(self) -> Union[None, GameSettings]:
        if not self._cli_cache_settings_path.exists():
            return None
        with open(self._cli_cache_settings_path, "rb") as settings_file:
            return pickle.load(settings_file)

    def try_update_current_game_settings(self, game_settings: GameSettings) -> bool:
        try:
            self._cli_cache_dir_path.mkdir(parents=True, exist_ok=True)
            with open(self._cli_cache_settings_path, "wb") as settings_file:
                pickle.dump(game_settings, settings_file)
            return True
        except OSError:
            print("failed to update game settings")
            return False

    def try_get_current_game_state(self, game_id: UUID) -> Union[None, GameState]:
        game_path = pathlib.Path(self._cli_cache_dir_path, f"{game_id}.pkl")
        if not game_path.exists():
            return None
        with open(game_path, "rb") as game_file:
            return pickle.load(game_file)

    def list_games(self) -> list[str]:
        if not self._cli_cache_dir_path.exists():
            return []
        path_strings = [str(path.stem) for path in self._cli_cache_dir_path.iterdir()]
        if "settings" in path_strings:
            path_strings.remove("settings")
        return path_strings

    def clear_games(self) -> None:
        if not self._cli_cache_dir_path.exists():
            print("Nothing to remove")
            return
        paths = [path for path in self._cli_cache_dir_path.iterdir()]
        if not paths:
            print("Nothing to remove")
            return
        print(f"Removing all files in directory {self._cli_cache_dir_path}:")
        for path in paths:
            print(path)
        click.confirm("Confirm deletion of these files", abort=True)
        for path in paths:
            path.unlink()

    def try_save_current_game_state(self, game_id: UUID, game_state: GameState) -> bool:
        try:
            self._cli_cache_dir_path.mkdir(parents=True, exist_ok=True)
            game_path = pathlib.Path(self._cli_cache_dir_path, f"{game_id}.pkl")
            with open(game_path, "wb") as game_file:
                pickle.dump(game_state, game_file)
            return True
        except OSError:
            print("unable to write game state")
            return False

    def initialize_new_game(self, rule_set: RuleSet) -> UUID:
        game_state = GameState(
            rule_set=rule_set,
            board_state=BoardState(
                occupancies=rule_set.initial_game_occupancies()
            ),
            whose_turn=rule_set.first_player(),
        )
        game_id = uuid.uuid4()
        if not self.try_save_current_game_state(game_id, game_state):
            raise Exception("Failed to initialize new game")
        return game_id
