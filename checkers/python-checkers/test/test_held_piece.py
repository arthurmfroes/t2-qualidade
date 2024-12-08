import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from unittest.mock import Mock
from pygame import Surface, Rect
import pygame
from held_piece import HeldPiece
from utils import (
    get_piece_gui_coords,
    get_surface_mouse_offset
)

@pytest.fixture
def mock_surface():
    surface = Mock(spec=Surface)
    surface.get_rect.return_value = Rect(0, 0, 50, 50)

    return surface

@pytest.fixture
def held_piece(mock_surface):
    return HeldPiece(mock_surface, (10, 15))

@pytest.fixture
def gui_coords():
    return {
        "square_dist": 50,
        "top_left_coords": (100, 100)
    }
    
# Esse teste verifica se o construtor da classe HeldPiece está atribuindo os valores corretos
def test_initialization(mock_surface):
    offset = (10, 15)
    held_piece = HeldPiece(mock_surface, offset)

    assert held_piece.surface == mock_surface
    assert held_piece.offset == offset
    assert held_piece.draw_rect == mock_surface.get_rect()



# Esse teste verifica se a função draw_piece está desenhando a peça na posição correta
def test_draw_piece(held_piece, monkeypatch):
    pygame.init()
    monkeypatch.setattr(pygame.mouse, "get_pos", lambda: (200, 300))
    mock_display_surface = Mock(spec=Surface)
    held_piece.draw_piece(mock_display_surface)

    assert held_piece.draw_rect.x == 10
    assert held_piece.draw_rect.y == 15

    mock_display_surface.blit.assert_called_once_with(held_piece.surface, held_piece.draw_rect)



# Esse teste verifica se a função check_collision retorna None quando não há colisão
def test_check_collision_no_collision(held_piece, gui_coords):
    rect_list = [
        Rect(*get_piece_gui_coords((2, 0), **gui_coords), 50, 50),
        Rect(*get_piece_gui_coords((3, 1), **gui_coords), 50, 50),
    ]

    result = held_piece.check_collision(rect_list)

    assert result is None



# Esse teste verifica se a função check_collision retorna o rect correto quando
# há colisão entre o rect do held_piece e um dos rects da lista passada como argumento
def test_check_collision_with_collision(held_piece, gui_coords):
    rect_list = [
        Rect(*get_piece_gui_coords((2, 0), **gui_coords), 50, 50),
        Rect(*get_piece_gui_coords((3, 1), **gui_coords), 50, 50),
    ]

    held_piece.draw_rect = Rect(*get_piece_gui_coords((3, 1), **gui_coords), 50, 50)
    result = held_piece.check_collision(rect_list)

    assert result == rect_list[1]



# Esse teste verifica se a função check_collision retorna None quando a lista de rects
# passada como argumento está vazia
def test_check_collision_empty_list(held_piece):
    rect_list = []
    result = held_piece.check_collision(rect_list)

    assert result is None



# Esse teste verifica se a função get_piece_gui_coords retorna as coordenadas corretas
# para cada par de coordenadas (row, col) passado como argumento
def test_offset_calculation_with_surface_mouse_offset(mock_surface):
    surface_pos = (200, 300)
    mouse_pos = (180, 280)
    offset = get_surface_mouse_offset(surface_pos, mouse_pos)

    held_piece = HeldPiece(mock_surface, offset)

    assert held_piece.offset == (20, 20)