import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ai import AI
from board import Board
from piece import Piece

@pytest.fixture
def board():
    pieces = [
        Piece("0WN"), Piece("1WN"), Piece("2BN"), Piece("3BN")
    ]

    return Board(pieces, "W")

@pytest.fixture
def ai():
    return AI("W")

# Esse teste verifica se o construtor da classe AI está atribuindo os valores corretos
def test_get_value_no_winner(ai, board):
    assert ai.get_value(board) == 0



# Esse teste verifica se o método get_value está retornando o valor correto para o caso em que
# a ai vence
def test_get_value_ai_wins(ai, board):
    board.pieces = [
        Piece("0WN"), Piece("1WN"), Piece("2WN"), Piece("3WN")
    ]
    board.get_winner = lambda: "W"

    assert ai.get_value(board) == 2



# Esse teste verifica se o método get_value está retornando o valor correto para o caso em que
# o oponente ganhe
def test_get_value_player_wins(ai, board):
    board.pieces = [
        Piece("0BN"), Piece("1BN"), Piece("2BN"), Piece("3BN")
    ]
    board.get_winner = lambda: "B"

    assert ai.get_value(board) == -2



# Esse teste verifica se o método get_value está retornando o valor correto para o caso em que
# o jogador tem mais peças que o oponente
def test_get_value_more_ai_pieces(ai, board):
    board.pieces = [
        Piece("0WN"), Piece("1WN"), Piece("2WN"), Piece("3BN")
    ]

    assert ai.get_value(board) == 1



# Esse teste verifica se o método get_value está retornando o valor correto para o caso em que
# o oponente tem mais peças que o jogador
def test_get_value_more_player_pieces(ai, board):
    board.pieces = [
        Piece("0WN"), Piece("1BN"), Piece("2BN"), Piece("3BN")
    ]

    assert ai.get_value(board) == -1



# Esse teste verifica se o método minimax está retornando o valor correto para o caso para
# maximizar
def test_minimax_maximize(ai, board):
    board.pieces = [
        Piece("17WN"), Piece("21WN"), Piece("9BN")
    ]
    board.get_winner = lambda: None
    assert ai.minimax(board, True, 1, "W") == 1
    assert ai.minimax(board, True, 2, "W") == 1



# Esse teste verifica se o método minimax está retornando o valor correto para o caso para
# minimizar
def test_minimax_minimize(ai, board):
    board.pieces = [
        Piece("17WN"), Piece("21WN"), Piece("9BN")
    ]
    board.get_winner = lambda: None
    assert ai.minimax(board, False, 1, "W") == 1
    assert ai.minimax(board, False, 2, "W") == 0



# Esse teste verifica se o método get_move está retornando o movimento correto
def test_get_move(ai, board):
    board.pieces = [
        Piece("17WN"), Piece("21WN"), Piece("9BN")
    ]

    moves = ai.get_move(board)

    assert moves == {"position_from": "17", "position_to": "13"} 