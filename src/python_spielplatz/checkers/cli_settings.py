from dataclasses import dataclass
from uuid import UUID


@dataclass()
class CliSettings:
    current_game: UUID
