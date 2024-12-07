import sys
import os
from unittest.mock import patch, Mock
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Dicionário para armazenar os mocks das imagens
mocks = {
    "black_piece.png": "black_piece.png",
    "white_piece.png": "white_piece.png",
    "black_king_piece.png": "black_king_piece.png",
    "white_king_piece.png": "white_king_piece.png",
    "marking.png": "marking.png",
    "board.png": "board.png",
}

# GUI specifications
BOARD_POSITION = (26, 26)
TOPLEFTBORDER = (34, 34)
SQUARE_DIST = 56

# Função para mockar pygame.image.load com base no nome do arquivo
# Foi necessário criar essa função por erros de importação da imagem no módulo
def mock_pygame_image_load(path):
    filename = os.path.basename(path)
    if filename in mocks:
        return mocks[filename]
    else:
        raise FileNotFoundError(f"Imagem mockada não definida para: {filename}")


# Aplicar o patch antes de importar pygame e outros módulos que carregam imagens
with patch('pygame.image.load', side_effect=mock_pygame_image_load):
    import pygame
    from board import Board
    from piece import Piece
    from board_gui import BoardGUI
    from utils import get_piece_gui_coords

# Agora, as superfícies carregadas são mocks e podem ser comparadas nos testes

# Esse teste verifica se o construtor da classe BoardGUI está atribuindo os valores corretos
# para cada peça passada como argumento, as propriedades da peça
def test_get_piece_color():
    pieces = [Piece('12WN')]
    board = Board(pieces, 'W')
    board_gui = BoardGUI(board)
    result = board_gui.get_piece_properties(board)
    assert result[0]["color"] == "W"


# Esse teste verifica se o construtor da classe BoardGUI está atribuindo os valores corretos
# para cada peça passada como argumento, as propriedades da peça
def test_get_piece_king():
    pieces = [Piece('12WN'), Piece('14BY')]
    board = Board(pieces, 'W')
    board_gui = BoardGUI(board)
    result = board_gui.get_piece_properties(board)
    assert result[0]["is_king"] == False
    assert result[1]["is_king"] == True

# Esse teste verifica se o rect da peça é retornado corretamente
# os valores constantes são baseados nas especificações da GUI
def test_get_piece_rect():
    pieces = [Piece('0WN')]
    board = Board(pieces, 'W')
    board_gui = BoardGUI(board)
    result = board_gui.get_piece_properties(board)
    expected_rect = pygame.Rect(get_piece_gui_coords((0, 0), 56, (34, 34)), (41, 41))
    assert result[0]["rect"] == expected_rect

# Esse teste verifica se o índice da peça é retornado corretamente
# para cada peça passada como argumento, retorna o índice da peça
def test_get_piece_by_index():
    pieces = [Piece('12WN'), Piece('14BY')]
    board = Board(pieces, 'W')
    board_gui = BoardGUI(board)
    result = board_gui.get_piece_by_index(0)
    assert result == board_gui.pieces[0]


# Esste teste verifica se a peça é escondida e mostrada corretamente
# a peça escondida tem seu índice armazenado
# a peça mostrada tem seu índice retornado e o índice armazenado é resetado (-1)
def test_hide_show_piece():
    pieces = [Piece('12WN'), Piece('14BY')]
    board = Board(pieces, 'W')
    board_gui = BoardGUI(board)
    board_gui.hide_piece(0)
    assert board_gui.hidden_piece == 0
    assert board_gui.show_piece() == 0
    assert board_gui.hidden_piece == -1

# Os testes a seguir verificam se as imagens das peças são carregadas corretamente baseadas no tipo de peça
# para cada peça passada como argumento, retorna a superfície da peça
def test_get_surface_black_piece():
    pieces = [Piece('12BN')]
    board = Board(pieces, 'B')
    board_gui = BoardGUI(board)
    assert board_gui.get_surface(pieces[0]) == mocks['black_piece.png']

def test_get_surface_white_piece():
    pieces = [Piece('12WN')]
    board = Board(pieces, 'W')
    board_gui = BoardGUI(board)
    assert board_gui.get_surface(pieces[0]) == mocks['white_piece.png']

def test_get_surface_black_king_piece():
    pieces = [Piece('12BY')]
    board = Board(pieces, 'W')
    board_gui = BoardGUI(board)
    assert board_gui.get_surface(pieces[0]) == mocks['black_king_piece.png']

def test_get_surface_white_king_piece():
    pieces = [Piece('12WY')]
    board = Board(pieces, 'W')
    board_gui = BoardGUI(board)
    assert board_gui.get_surface(pieces[0]) == mocks['white_king_piece.png']
    

# Esse teste verifica se a função get_position_by_rect retorna a posição correta
# utiliza a função get_piece_gui_coords para obter as coordenadas da peça
def test_get_position_by_rect():
    pieces = [Piece('1WY')]
    board = Board(pieces, 'W')
    board_gui = BoardGUI(board)
    rect = pygame.Rect(get_piece_gui_coords((0, 2), SQUARE_DIST, TOPLEFTBORDER), (41, 41))
    result = board_gui.get_position_by_rect(rect)
    assert result == 1
    
