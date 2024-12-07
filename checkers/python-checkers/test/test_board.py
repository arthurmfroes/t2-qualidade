# test_board.py
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from board import Board
from piece import Piece


## Esse teste verifica se o construtor da classe Board está atribuindo os valores corretos
# Teste para inicialização do tabuleiro com 3 peças, 2 brancas e 1 preta
def test_board_init():
    pieces = [Piece('12WN'), Piece('14BN'), Piece('24WY')]
    board = Board(pieces, 'W')
    assert board.get_pieces() == pieces
    assert board.get_color_up() == 'W'


# Esse teste verifica se o índice da peça é retornado corretamente
# para cada posição passada como argumento, retorna a peça naquela posição
def test_get_piece_by_index():
    pieces = [Piece('12WN'), Piece('14BN'), Piece('24WY')]
    board = Board(pieces, 'W')
    assert board.get_piece_by_index(0) == pieces[0]
    assert board.get_piece_by_index(1) == pieces[1]
    assert board.get_piece_by_index(2) == pieces[2]

# Esse teste verifica se o tabuleiro retorna corretamente se uma peça está presente em uma casa
# para cada posição passada como argumento, retorna True se a peça está presente, False caso contrário
def test_has_piece():
    pieces = [Piece('0BN'), Piece('14BN')]
    board = Board(pieces, 'W')
    assert board.has_piece(0) == True
    assert board.has_piece(1) == False
    assert board.has_piece(14) == True
    assert board.has_piece(15) == False

# Teste para cada linha do tabuleiro, cada linha tem 4 casas possíveis, partindo do 0.
# para cada posição passada como argumento, retorna a linha daquela posição
def test_get_row_number():
    pieces = [Piece('0BN')]
    board = Board(pieces, 'W')
    assert board.get_row_number(0) == 0
    assert board.get_row_number(1) == 0
    assert board.get_row_number(4) == 1

# Teste para cada coluna do tabuleiro, cada linha tem 4 casas possíveis, partindo do 0. linhas ímpares tem um offset de 1, pois a primeira casa é uma casa clara.
# para cada posição passada como argumento, retorna a coluna daquela posição
def test_get_col_number():
    pieces = [Piece('0BN')]
    board = Board(pieces, 'W')
    print(board.get_col_number(4))
    assert board.get_col_number(0) == 0
    assert board.get_col_number(1) == 2
    assert board.get_col_number(4) == 1

# Esse teste verifica se  a linhha contém as peças corretas 
# para cada linha passada como argumento, retorna as peças daquela linha
def test_get_row():
    pieces = [Piece('0BN'), Piece('1BN'), Piece('2BN'), Piece('3BN')]
    board = Board(pieces, 'W')
    assert board.get_row(0) == set(pieces)
    assert board.get_row(1) == set()

# Esse teste verifica as coordenadas de uma peça
# para cada coordenada passada como argumento, retorna a peça naquela coordenada
def test_get_pieces_by_coords():
    pieces = [Piece('0BN'), Piece('1BN'), Piece('2BN'), Piece('3BN')]
    board = Board(pieces, 'W')
    result = board.get_pieces_by_coords((0, 0), (0,2))
    assert result == [pieces[0], pieces[1]]
    result = board.get_pieces_by_coords((1, 0), (1,2))
    assert result == [None, None]


# Teste de movimentação simples sem captura
# para cada índice da peça e posição passada como argumento, movimenta a peça para a posição
def test_move_piece():
    pieces = [Piece('12WN')]
    board = Board(pieces, 'W')
    board.move_piece(0, 16)  # Movimenta a peça de 12 para 16
    assert pieces[0].get_position() == '16'
    assert pieces[0].get_has_eaten() == False
    
    
# Teste de captura de peça adversária
# para cada índice da peça e posição passada como argumento, movimenta a peça para a posição e captura a peça adversária
def test_move_piece_eat():
    pieces = [Piece('12WN'), Piece('17BN')]
    board = Board(pieces, 'W')
    board.move_piece(0, 21)  # Peça em 12 captura a peça em 17 e vai para 21
    assert pieces[0].get_position() == '21'
    assert pieces[0].get_has_eaten() == True
    assert len(board.get_pieces()) == 1  # Peça em 17 foi removida
    assert board.get_pieces()[0].get_position() == '21'

# Teste de promoção de peça com captura
# para cada índice da peça e posição passada como argumento, movimenta a peça para a posição e promove a peça a dama
def test_move_piece_promotion_with_capture():
    pieces = [Piece('22WN'), Piece('27BN')]
    board = Board(pieces, 'B')
    
    board.move_piece(0, 31)  # Movimento de 26 para 31, capturando 29
    assert pieces[0].get_position() == '31'
    assert board.get_pieces() == [pieces[0]]
    assert pieces[0].is_king() == True
    
# Teste de promoção de peça sem captura
# para cada índice da peça e posição passada como argumento, movimenta a peça para a posição e promove a peça a dama sem captura
def test_move_piece_promotion_without_capture():
    pieces = [Piece('27WN')]
    board = Board(pieces, 'B')
    
    board.move_piece(0, 31)  # Movimento de 26 para 31
    assert pieces[0].get_position() == '31'
    assert board.get_pieces() == [pieces[0]]
    assert pieces[0].is_king() == True
    
# Teste de movimento da dama
# para cada índice da peça e posição passada como argumento, movimenta a dama para a posição
def test_move_king():
    pieces = [Piece('13WY')]
    board = Board(pieces, 'W')
    board.move_piece(0, 17)  # Dama se move para trás
    assert pieces[0].get_position() == '17'
    assert pieces[0].is_king() == True
    
# Teste de vencedor
# se houver apenas 1 peça de uma determinada cor, essa cor é o vencedor
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