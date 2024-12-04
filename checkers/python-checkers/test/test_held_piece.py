import pytest
from unittest.mock import Mock
from pygame import Surface, Rect
from held_piece import HeldPiece
from utils import (
    get_position_with_row_col,
    get_piece_position,
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

def test_draw_piece(held_piece, monkeypatch):
    pytest.MonkeyPatch.setattr("pygame.mouse.get_pos", lambda: (200, 300))
    mock_display_surface = Mock(spec=Surface)
    held_piece.draw_piece(mock_display_surface)

    assert held_piece.draw_rect.x == 200 + 10
    assert held_piece.draw_rect.y == 300 + 15

    mock_display_surface.blit.assert_called_once_with(held_piece.surface, held_piece.draw_rect)


def test_check_collision_no_collision(held_piece, gui_coords):
    rect_list = [
        Rect(*get_piece_gui_coords((2, 0), **gui_coords), 50, 50),
        Rect(*get_piece_gui_coords((3, 1), **gui_coords), 50, 50),
    ]

    result = held_piece.check_collision(rect_list)

    assert result is None


def test_check_collision_with_collision(held_piece, gui_coords):
    rect_list = [
        Rect(*get_piece_gui_coords((2, 0), **gui_coords), 50, 50),
        Rect(*get_piece_gui_coords((3, 1), **gui_coords), 50, 50),
    ]

    held_piece.draw_rect = Rect(*get_piece_gui_coords((3, 1), **gui_coords), 50, 50)
    result = held_piece.check_collision(rect_list)

    assert result == rect_list[1]


def test_check_collision_empty_list(held_piece):
    rect_list = []
    result = held_piece.check_collision(rect_list)

    assert result is None


def test_offset_calculation_with_surface_mouse_offset(mock_surface):
    surface_pos = (200, 300)
    mouse_pos = (180, 280)
    offset = get_surface_mouse_offset(surface_pos, mouse_pos)

    held_piece = HeldPiece(mock_surface, offset)

    assert held_piece.offset == (20, 20)