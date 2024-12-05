# test_board.py
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# test_board.py

import pytest
from board import Board
from piece import Piece

def test_board_init():
    pieces = [Piece('12WN'), Piece('14BN'), Piece('24WY')]
    board = Board(pieces, 'W')
    assert board.get_pieces() == pieces
    assert board.get_color_up() == 'W'

def test_get_piece_by_index():
    pieces = [Piece('12WN'), Piece('14BN'), Piece('24WY')]
    board = Board(pieces, 'W')
    assert board.get_piece_by_index(0) == pieces[0]
    assert board.get_piece_by_index(1) == pieces[1]
    assert board.get_piece_by_index(2) == pieces[2]

def test_has_piece():
    pieces = [Piece('0BN')]
    board = Board(pieces, 'W')
    assert board.has_piece(0) == True
    assert board.has_piece(1) == False

# Teste para cada linha do tabuleiro, cada linha tem 4 casas possíveis, partindo do 0.
def test_get_row_number():
    pieces = [Piece('0BN')]
    board = Board(pieces, 'W')
    assert board.get_row_number(0) == 0
    assert board.get_row_number(1) == 0
    assert board.get_row_number(4) == 1

# Teste para cada coluna do tabuleiro, cada linha tem 4 casas possíveis, partindo do 0. linhas ímpares tem um offset de 1, pois a primeira casa é uma casa clara.
def test_get_col_number():
    pieces = [Piece('0BN')]
    board = Board(pieces, 'W')
    print(board.get_col_number(4))
    assert board.get_col_number(0) == 0
    assert board.get_col_number(1) == 2
    assert board.get_col_number(4) == 1


def test_get_row():
    pieces = [Piece('0BN'), Piece('1BN'), Piece('2BN'), Piece('3BN')]
    board = Board(pieces, 'W')
    assert board.get_row(0) == set(pieces)
    assert board.get_row(1) == set()

def test_get_pieces_by_coords():
    pieces = [Piece('0BN'), Piece('1BN'), Piece('2BN'), Piece('3BN')]
    board = Board(pieces, 'W')
    result = board.get_pieces_by_coords((0, 0), (0,2))
    assert result == [pieces[0], pieces[1]]
    result = board.get_pieces_by_coords((1, 0), (1,2))
    assert result == [None, None]


# Teste de movimentação simples sem captura
def test_move_piece():
    pieces = [Piece('12WN')]
    board = Board(pieces, 'W')
    board.move_piece(0, 16)  # Movimenta a peça de 12 para 16
    assert pieces[0].get_position() == '16'
    assert pieces[0].get_has_eaten() == False
    
    
# Teste de captura de peça adversária
def test_move_piece_eat():
    pieces = [Piece('12WN'), Piece('17BN')]
    board = Board(pieces, 'W')
    board.move_piece(0, 21)  # Peça em 12 captura a peça em 17 e vai para 21
    assert pieces[0].get_position() == '21'
    assert pieces[0].get_has_eaten() == True
    assert len(board.get_pieces()) == 1  # Peça em 17 foi removida
    assert board.get_pieces()[0].get_position() == '21'

# Teste de promoção de peça com captura
def test_move_piece_promotion_():
    pieces = [Piece('22WN'), Piece('27BN')]
    board = Board(pieces, 'B')
    
    board.move_piece(0, 31)  # Movimento de 26 para 31, capturando 29
    assert pieces[0].get_position() == '31'
    assert board.get_pieces() == [pieces[0]]
    assert pieces[0].is_king() == True
    
# Teste de promoção de peça sem captura
def test_move_piece_promotion():
    pieces = [Piece('27WN')]
    board = Board(pieces, 'B')
    
    board.move_piece(0, 31)  # Movimento de 26 para 31
    assert pieces[0].get_position() == '31'
    assert board.get_pieces() == [pieces[0]]
    assert pieces[0].is_king() == True
    
# Teste de movimento da dama
def test_move_king():
    pieces = [Piece('13WY')]
    board = Board(pieces, 'W')
    board.move_piece(0, 17)  # Dama se move para trás
    assert pieces[0].get_position() == '17'
    assert pieces[0].is_king() == True
    
# Teste de vencedor
def test_get_winner():
    pieces = [Piece('0BN')]
    board = Board(pieces, 'W')
    assert board.get_winner() == 'B'
    pieces = [Piece('0WN')]
    board = Board(pieces, 'W')
    assert board.get_winner() == 'W'
    pieces = [Piece('0WN'), Piece('1BN')]
    board = Board(pieces, 'W')
    assert board.get_winner() == None