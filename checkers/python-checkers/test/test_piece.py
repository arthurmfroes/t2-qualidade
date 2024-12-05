import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from unittest.mock import Mock
from piece import Piece

@pytest.fixture
def mock_board():
    board = Mock()
    board.get_col_number.return_value = 1
    board.get_row_number.return_value = 3
    board.get_color_up.return_value = "W"

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

    assert adjacent_squares == [(2, 0), (2, 2)]



def test_get_adjacent_squares_consistency(mock_board):
    piece = Piece("16WN")
    adjacent_squares = piece.get_adjacent_squares(mock_board)

    assert len(adjacent_squares) > 0



def test_get_moves_no_obstacles(mock_board):
    piece = Piece("16WN")
    mock_board.get_pieces_by_coords.return_value = [None, None]
    mock_board.has_piece.return_value = False
    mock_board.get_col_number.return_value = 1
    mock_board.get_row_number.return_value = 3

    moves = piece.get_moves(mock_board)

    assert moves == [{"position": "8", "eats_piece": False}, {"position": "9", "eats_piece": False}]



def test_get_moves_with_obstacles(mock_board):
    piece = Piece("16WN")
    mock_piece = Mock()
    mock_piece.get_color.return_value = "B"
    mock_board.get_pieces_by_coords.return_value = [mock_piece, None]
    mock_board.has_piece.side_effect = lambda pos: pos == "5"
    mock_board.get_col_number.return_value = 1
    mock_board.get_row_number.return_value = 3

    moves = piece.get_moves(mock_board)

    assert moves == [{"position": "9", "eats_piece": False}]



# def test_get_moves_with_eating(mock_board):
#     piece = Piece("16WN")
#     mock_piece = Mock()
#     mock_piece.get_color.return_value = "B"
#     mock_board.get_pieces_by_coords.return_value = [mock_piece, None]
#     mock_board.has_piece.side_effect = lambda pos: pos == "25"
#     mock_board.get_col_number.side_effect = lambda pos: 1 if pos == 16 else 2
#     mock_board.get_row_number.side_effect = lambda pos: 3 if pos == 16 else 4

#     print(mock_board.get_col_number(16))
#     print(mock_board.get_row_number(16))

#     moves = piece.get_moves(mock_board)
    
#     assert moves == [{"position": "25", "eats_piece": True}]