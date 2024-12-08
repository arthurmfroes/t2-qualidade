
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from unittest.mock import Mock, patch
import pygame

from game_control import GameControl
from piece import Piece
from utils import get_piece_gui_coords

# Função utilitária interna para obter a posição do mouse em relação a uma peça
def get_mouse_pos_position(position):
    # Converter posição em linha e coluna
    row = position // 4
    col = (position % 4) * 2 + (1 if row % 2 == 0 else 0)
    
    # Obter coordenadas da GUI
    SQUARE_DIST = 56
    TOPLEFTBORDER = (34, 34)
    x_pos, y_pos = get_piece_gui_coords((row, col), SQUARE_DIST, TOPLEFTBORDER)
    
    # Ajustar para o centro da peça
    x_center = x_pos + 41 // 2
    y_center = y_pos + 41 // 2
    mouse_pos = (x_center, y_center)
    return mouse_pos

# Esse teste verifica se o construtor da classe GameControl está atribuindo os valores corretos
def test_game_control_init():
    game = GameControl("W", False)
    assert game.get_turn() == "W"
    assert game.get_winner() == None
    game = GameControl("B", False)
    assert game.get_turn() == "B"
    assert game.get_winner() == None


# Esse teste verifica se a função get_turn retorna o valor correto
def test_game_control_ai_control():
    game = GameControl("W", True)
    assert game.ai_control != None

    game = GameControl("W", False)
    assert game.ai_control == None


# Esse teste verifica se a função setup está criando o tabuleiro com as peças corretas para um jogo novo
def test_game_control_setup_pieces():
    game = GameControl("W", False)
    pieces = game.board.get_pieces()
    num_white_pieces = sum(1 for p in pieces if p.get_color() == "W")
    num_black_pieces = sum(1 for p in pieces if p.get_color() == "B")
    assert num_white_pieces == 12
    assert num_black_pieces == 12


# Esse teste verifica se a função hold_piece não atribui posição a peça caso não seja o turno da peça clicada 
# recebe uma posição de mouse e não atribui a peça clicada a variável held_piece
def test_hold_piece_wrong_turn():
        game = GameControl("W", False)
        game.hold_piece(get_mouse_pos_position(0))
        assert game.held_piece == None

# Esse teste verifica se a função hold_piece não atribui posição a peça caso não haja peça na posição clicada
# recebe uma posição de mouse e não atribui nada a variável held_piece
def test_hold_piece_no_piece():
        game = GameControl("W", False)
        game.hold_piece(get_mouse_pos_position(17))
        assert game.held_piece == None

# Esse teste verifica se a função hold_piece atribui posição a peça corretamente
# recebe uma posição de mouse e atribui a peça clicada a variável held_piece
def test_hold_piece_valid():
        game = GameControl("W", False)
        game.hold_piece(get_mouse_pos_position(20))
        assert game.held_piece != None

# Esse teste verifica o movimento de uma peça sem captura
# recebe uma posição de mouse e move a peça para a posição clicada
def test_drag_and_drop_piece_without_capture():
    game = GameControl("W", False)
    game.board.get_pieces().clear()
    game.board.get_pieces().extend([
        Piece('12WN'),
        Piece('0BN')
    ])
    game.board_draw.set_pieces(game.board_draw.get_piece_properties(game.board))
    
    assert len(game.board.get_pieces()) == 2
    assert game.board.get_pieces()[0].get_position() == '12'
    
    game.hold_piece(get_mouse_pos_position(12))
    
    with patch('held_piece.HeldPiece.check_collision') as mock_collision:
        mock_rect = pygame.Rect(*get_piece_gui_coords((2, 0), 56, (34, 34)), 41, 41)
        mock_collision.return_value = mock_rect
            
        game.release_piece()
    
    remaining_pieces = game.board.get_pieces()
    assert len(remaining_pieces) == 2
    assert remaining_pieces[0].get_position() == '8'
    assert remaining_pieces[0].get_has_eaten() == False
    
# Esse teste verifica o movimento de uma peça com captura de peça adversária
# recebe uma posição de mouse e move a peça para a posição clicada, capturando a peça adversária
def test_drag_and_drop_piece_with_capture():
    game = GameControl("W", False)
    # Setup - Criar situação onde peça branca pode capturar peça preta
    game.board.get_pieces().clear()
    game.board.get_pieces().extend([
        Piece('17WN'),   # Peça branca que vai capturar
        Piece('12BN')  # Peça preta peça preta que vai ser capturada
    ])
    game.board_draw.set_pieces(game.board_draw.get_piece_properties(game.board))
    
    assert len(game.board.get_pieces()) == 2
    assert game.board.get_pieces()[0].get_position() == '17'
    assert game.board.get_pieces()[1].get_position() == '12'
    
    game.hold_piece(get_mouse_pos_position(17))

    piece_moves = game.board.get_pieces()[0].get_moves(game.board)
    assert piece_moves[0]['position'] == '8'
    assert piece_moves[0]['eats_piece'] == True
    
    with patch('held_piece.HeldPiece.check_collision') as mock_collision:
        mock_rect = pygame.Rect(*get_piece_gui_coords((2, 0), 56, (34, 34)), 41, 41)
        mock_collision.return_value = mock_rect
            
        game.release_piece()
    
    remaining_pieces = game.board.get_pieces()
    assert len(remaining_pieces) == 1324
