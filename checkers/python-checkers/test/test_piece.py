import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from board import Board
from piece import Piece

# Esse teste verifica se o construtor da classe Piece está atribuindo os valores corretos
def test_get_name():
    piece = Piece("16WN")
    
    assert piece.get_name() == "16WN"



# Esse teste verifica se o método get_position está retornando a posição correta
def test_get_position():
    piece = Piece("16WN")
    
    assert piece.get_position() == "16"



# Esse teste verifica se o método get_color está retornando a cor correta
def test_get_color():
    piece = Piece("16WN")

    assert piece.get_color() == "W"



# Esse teste verifica se o método is_king está retornando o valor correto
def test_is_king():
    king_piece = Piece("16WY")
    non_king_piece = Piece("16WN")

    assert king_piece.is_king() is True
    assert non_king_piece.is_king() is False



# Esse teste verifica se o método set_position está atribuindo a posição correta
def test_set_position():
    piece = Piece("16WN")
    piece.set_position("20")

    assert piece.get_position() == "20"



# Esse teste verifica se o método set_is_king está atribuindo o valor correto
def test_set_is_king():
    piece = Piece("16WN")
    piece.set_is_king(True)

    assert piece.is_king() is True



# Esse teste verifica se o método set_has_eaten está atribuindo o valor correto
def test_has_eaten():
    piece = Piece("16WN")
    piece.set_has_eaten(True)

    assert piece.get_has_eaten() is True



# Esse teste verifica se o método get_adjacent_squares retorna as casas adjacentes corretas
def test_get_adjacent_squares():
    piece = Piece("16WN")
    board = Board([piece], "W")
    adjacent_squares = piece.get_adjacent_squares(board)

    assert adjacent_squares == [(2, 0), (2, 2)]



# Esse teste verifica se o método get_moves retorna as jogadas corretas
# quando não há peças adjacentes
def test_get_moves_no_obstacles():
    piece = Piece("16WN")
    board = Board([piece], "W")

    moves = piece.get_moves(board)

    assert moves == [{"position": "8", "eats_piece": False}, {"position": "9", "eats_piece": False}]



def test_get_moves_out_of_bounds():
    piece = Piece("8WN")
    board = Board([piece], "W")

    moves = piece.get_moves(board)

    assert moves == [{"position": "4", "eats_piece": False}]


# Esse teste verifica se o método get_moves retorna as jogadas corretas
# quando há peças adjacentes
def test_get_moves_with_obstacles():
    piece = Piece("16WN")
    board = Board([piece, Piece("8WN")], "W")

    moves = piece.get_moves()

    assert moves == [{"position": "9", "eats_piece": False}]



# Esse teste verifica se o método get_moves retorna as jogadas corretas
# quando há peças adjacentes e é possível comer uma peça
def test_get_moves_with_eating():
    piece = Piece("16WN")
    board = Board([piece, Piece("9BN")], "W")

    moves = piece.get_moves(board)
    
    assert moves == [{"position": "9", "eats_piece": True}]