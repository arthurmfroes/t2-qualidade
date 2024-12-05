import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from unittest.mock import Mock
from ai import AI
from board import Board
from piece import Piece

@pytest.fixture
def mock_board():
    board = Mock(spec=Board)
    board.get_winner.return_value = None
    board.get_color_up.return_value = "W"

    return board

@pytest.fixture
def ai():
    return AI("W")

# Esse teste verifica se o construtor da classe AI está atribuindo os valores corretos
def test_get_value_no_winner(ai, mock_board):
    mock_board.get_pieces.return_value = [
        Piece("0WN"), Piece("1WN"), Piece("2BN"), Piece("3BN")
    ]

    assert ai.get_value(mock_board) == 0



# Esse teste verifica se o método get_value está retornando o valor correto para o caso em que
# o jogador ganha
def test_get_value_player_wins(ai, mock_board):
    mock_board.get_winner.return_value = "W"
    mock_board.get_pieces.return_value = [
        Piece("0WN"), Piece("1WN"), Piece("2WN"), Piece("3WN")
    ]

    assert ai.get_value(mock_board) == 2



# Esse teste verifica se o método get_value está retornando o valor correto para o caso em que
# o oponente ganha
def test_get_value_opponent_wins(ai, mock_board):
    mock_board.get_winner.return_value = "B"
    mock_board.get_pieces.return_value = [
        Piece("0BN"), Piece("1BN"), Piece("2BN"), Piece("3BN")
    ]

    assert ai.get_value(mock_board) == -2



# Esse teste verifica se o método get_value está retornando o valor correto para o caso em que
# o jogador tem mais peças que o oponente
def test_get_value_more_player_pieces(ai, mock_board):
    mock_board.get_pieces.return_value = [
        Piece("0WN"), Piece("1WN"), Piece("2WN"), Piece("3BN")
    ]

    assert ai.get_value(mock_board) == 1



# Esse teste verifica se o método get_value está retornando o valor correto para o caso em que
# o oponente tem mais peças que o jogador
def test_get_value_more_opponent_pieces(ai, mock_board):
    mock_board.get_pieces.return_value = [
        Piece("0WN"), Piece("1BN"), Piece("2BN"), Piece("3BN")
    ]

    assert ai.get_value(mock_board) == -1



# def test_minimax(ai, mock_board):
#     pieces = [
#         Mock(spec=Piece), Mock(spec=Piece), Mock(spec=Piece), Mock(spec=Piece)
#     ]
#     pieces[0].get_moves.return_value = [{"position": "4", "eats_piece": False}]
#     pieces[1].get_moves.return_value = [{"position": "5", "eats_piece": False}]
#     pieces[2].get_moves.return_value = [{"position": "6", "eats_piece": False}]
#     pieces[3].get_moves.return_value = [{"position": "7", "eats_piece": False}]
#     mock_board.get_pieces.return_value = pieces
    
#     assert ai.minimax(mock_board, True, 1, "W") == 1



# def test_get_move(ai, mock_board):
#     pieces = [
#         Mock(spec=Piece), Mock(spec=Piece), Mock(spec=Piece), Mock(spec=Piece)
#     ]
#     pieces[0].get_moves.return_value = [{"position": "4", "eats_piece": False}]
#     pieces[1].get_moves.return_value = [{"position": "5", "eats_piece": False}]
#     pieces[2].get_moves.return_value = [{"position": "6", "eats_piece": False}]
#     pieces[3].get_moves.return_value = [{"position": "7", "eats_piece": False}]
#     pieces[0].get_position.return_value = "0"
#     pieces[1].get_position.return_value = "1"
#     pieces[2].get_position.return_value = "2"
#     pieces[3].get_position.return_value = "3"
#     mock_board.get_pieces.return_value = pieces
#     mock_board.get_color_up.return_value = "W"
    
#     move = ai.get_move(mock_board)

#     assert move in [{"position_to": "4", "position_from": "0"}, {"position_to": "5", "position_from": "1"}]