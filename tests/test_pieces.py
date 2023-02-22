import pytest
from python_spielplatz.checkers.pieces import PieceColor


@pytest.mark.parametrize(
    ("piece_color", "expected_next_color"),
    [
        (PieceColor.WHITE, PieceColor.BLACK),
        (PieceColor.BLACK, PieceColor.WHITE),
    ],
)
def test_piece_color_next(
    piece_color: PieceColor,
    expected_next_color: PieceColor,
) -> None:
    """The next color should identify the color of which player is turn it is after the given player color."""
    assert piece_color.next_up() == expected_next_color


@pytest.mark.parametrize(
    ("piece_color", "expected_str"),
    [
        (PieceColor.WHITE, "WHITE"),
        (PieceColor.BLACK, "BLACK"),
    ],
)
# comment
def test_piece_color_str_conversion(piece_color: PieceColor, expected_str: str) -> None:
    """Test that piece colors can be converted to strings."""
    assert f"{piece_color}" == expected_str
