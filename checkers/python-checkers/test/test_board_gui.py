import sys
import os
from unittest.mock import patch, Mock

# Dicionário para armazenar os mocks das imagens
mocks = {
    "black_piece.png": Mock(spec='pygame.Surface'),
    "white_piece.png": Mock(spec='pygame.Surface'),
    "black_king_piece.png": Mock(spec='pygame.Surface'),
    "white_king_piece.png": Mock(spec='pygame.Surface'),
    "marking.png": Mock(spec='pygame.Surface'),
    "board.png": Mock(spec='pygame.Surface'),
}

# GUI specifications
BOARD_POSITION = (26, 26)
TOPLEFTBORDER = (34, 34)
SQUARE_DIST = 56

# Função para mockar pygame.image.load com base no nome do arquivo
def mock_pygame_image_load(path):
    filename = os.path.basename(path)
    if filename in mocks:
        return mocks[filename]
    else:
        raise FileNotFoundError(f"Imagem mockada não definida para: {filename}")


# Aplicar o patch antes de importar pygame e outros módulos que carregam imagens
with patch('pygame.image.load', side_effect=mock_pygame_image_load):
    import pygame

    # Adiciona o diretório principal do projeto ao sys.path para permitir importações
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

    # Obtém o diretório principal do projeto
    project_dir = os.path.dirname(os.path.dirname(__file__))

    # Preload images com pygame.image.load que agora está mockado
    BLACK_PIECE_SURFACE = pygame.image.load(os.path.join(project_dir, "images", "black_piece.png"))
    mocks["black_piece.png"] = BLACK_PIECE_SURFACE
    WHITE_PIECE_SURFACE = pygame.image.load(os.path.join(project_dir, "images", "white_piece.png"))
    mocks["white_piece.png"] = WHITE_PIECE_SURFACE
    BLACK_KING_PIECE_SURFACE = pygame.image.load(os.path.join(project_dir, "images", "black_king_piece.png"))
    mocks["black_king_piece.png"] = BLACK_KING_PIECE_SURFACE
    WHITE_KING_PIECE_SURFACE = pygame.image.load(os.path.join(project_dir, "images", "white_king_piece.png"))
    mocks["white_king_piece.png"] = WHITE_KING_PIECE_SURFACE
    MOVE_MARK = pygame.image.load(os.path.join(project_dir, "images", "marking.png"))
    mocks["marking.png"] = MOVE_MARK
    BOARD = pygame.image.load(os.path.join(project_dir, "images", "board.png"))
    mocks["board.png"] = BOARD

    from board import Board
    from piece import Piece
    from board_gui import BoardGUI
    from utils import get_piece_gui_coords

# Agora, as superfícies carregadas são mocks e podem ser comparadas nos testes

def test_get_piece_color():
    pieces = [Piece('12WN')]
    board = Board(pieces, 'W')
    board_gui = BoardGUI(board)
    result = board_gui.get_piece_properties(board)
    assert result[0]["color"] == "W"

def test_get_piece_king():
    pieces = [Piece('12WN'), Piece('14BY')]
    board = Board(pieces, 'W')
    board_gui = BoardGUI(board)
    result = board_gui.get_piece_properties(board)
    assert result[0]["is_king"] == False
    assert result[1]["is_king"] == True

# Verifica se o retângulo retornado é o esperado
def test_get_piece_rect():
    pieces = [Piece('0WN')]
    board = Board(pieces, 'W')
    board_gui = BoardGUI(board)
    result = board_gui.get_piece_properties(board)
    expected_rect = pygame.Rect(get_piece_gui_coords((0, 0), 56, (34, 34)), (41, 41))
    assert result[0]["rect"] == expected_rect

def test_get_piece_by_index():
    pieces = [Piece('12WN'), Piece('14BY')]
    board = Board(pieces, 'W')
    board_gui = BoardGUI(board)
    result = board_gui.get_piece_by_index(0)
    assert result == board_gui.pieces[0]

def test_hide_show_piece():
    pieces = [Piece('12WN'), Piece('14BY')]
    board = Board(pieces, 'W')
    board_gui = BoardGUI(board)
    board_gui.hide_piece(0)
    assert board_gui.hidden_piece == 0
    assert board_gui.show_piece() == 0
    assert board_gui.hidden_piece == -1

def test_get_surface_black_piece():
    pieces = [Piece('12BN')]
    board = Board(pieces, 'B')
    board_gui = BoardGUI(board)
    print (board_gui.get_surface(pieces[0]))
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
    
def test_get_position_by_rect():
    pieces = [Piece('1WY')]
    board = Board(pieces, 'W')
    board_gui = BoardGUI(board)
    rect = pygame.Rect(get_piece_gui_coords((0, 2), SQUARE_DIST, TOPLEFTBORDER), (41, 41))
    result = board_gui.get_position_by_rect(rect)
    assert result == 1
    
