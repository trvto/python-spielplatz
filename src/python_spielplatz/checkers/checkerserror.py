from dataclasses import dataclass


@dataclass
class CheckersError:
    """Class for reporting errors from the checkers cli."""

    error_message: str
