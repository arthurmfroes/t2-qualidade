import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from unittest.mock import Mock
from piece import Piece

@pytest.fixture
def mock_board():
    board = Mock()
    board.get_col_number.side_effect = lambda pos: (pos % 8) * 2 + (pos // 8 % 2)
    board.get_row_number.side_effect = lambda pos: pos // 4
    board.get_color_up.return_value = "W"
    board.has_piece.side_effect = lambda pos: False
    board.get_pieces_by_coords.return_value = [None, None, None, None]

    return board


def test_get_name():
    piece = Piece("16WN")
    
    assert piece.get_name() == "16WN"


def test_get_position():
    piece = Piece("16WN")
    
    assert piece.get_position() == "16"


def test_get_color():
    piece = Piece("16WN")

    assert piece.get_color() == "W"


def test_is_king():
    king_piece = Piece("16WY")
    non_king_piece = Piece("16WN")

    assert king_piece.is_king() is True
    assert non_king_piece.is_king() is False


def test_set_position():
    piece = Piece("16WN")
    piece.set_position("20")

    assert piece.get_position() == "20"


def test_set_is_king():
    piece = Piece("16WN")
    piece.set_is_king(True)

    assert piece.is_king() is True


def test_has_eaten():
    piece = Piece("16WN")
    piece.set_has_eaten(True)

    assert piece.get_has_eaten() is True


def test_get_adjacent_squares(mock_board):
    piece = Piece("16WN")
    adjacent_squares = piece.get_adjacent_squares(mock_board)

    assert adjacent_squares == [(3, 1)]


def test_get_moves_no_eating(mock_board):
    piece = Piece("16WN")
    mock_board.get_pieces_by_coords.return_value = [None, None, None, None]
    mock_board.get_col_number.return_value = 2
    mock_board.get_row_number.return_value = 4

    moves = piece.get_moves(mock_board)

    assert len(moves) == 2
    assert moves == [
        {"position": "12", "eats_piece": False},
        {"position": "13", "eats_piece": False}
    ]


def test_get_moves_eating(mock_board):
    piece = Piece("16WN")
    enemy_piece = Mock()
    enemy_piece.get_color.return_value = "B"

    mock_board.get_pieces_by_coords.return_value = [enemy_piece, None, None, None]
    mock_board.get_col_number.return_value = 2
    mock_board.get_row_number.return_value = 4
    mock_board.has_piece.side_effect = lambda pos: pos != 12

    moves = piece.get_moves(mock_board)

    assert len(moves) == 1
    assert moves == [
        {"position": "12", "eats_piece": True}
    ]


def test_get_moves_king(mock_board):
    king_piece = Piece("16WY")
    mock_board.get_pieces_by_coords.return_value = [None, None, None, None]

    moves = king_piece.get_moves(mock_board)

    assert len(moves) == 4