import pytest
from utils import (
    get_position_with_row_col,
    get_piece_position,
    get_piece_gui_coords,
    get_surface_mouse_offset
)

def test_get_position_with_row_col():
    assert get_position_with_row_col(0, 0) == 0
    assert get_position_with_row_col(1, 0) == 4
    assert get_position_with_row_col(0, 2) == 1
    assert get_position_with_row_col(2, 7) == 11
    assert get_position_with_row_col(7, 7) == 31


def test_get_piece_position():
    square_dist = 50
    top_left_coords = (100, 100)
    
    coords = (150, 200)
    assert get_piece_position(coords, square_dist, top_left_coords) == 8

    coords = (100, 100)
    assert get_piece_position(coords, square_dist, top_left_coords) == 0

    coords = (450, 450)
    assert get_piece_position(coords, square_dist, top_left_coords) == 31

    coords = (50, 50)
    assert get_piece_position(coords, square_dist, top_left_coords) == -5


def test_get_piece_gui_coords():
    square_dist = 50
    top_left_coords = (100, 100)
    
    coords = (0, 0)
    assert get_piece_gui_coords(coords, square_dist, top_left_coords) == (100, 100)

    coords = (3, 3)
    assert get_piece_gui_coords(coords, square_dist, top_left_coords) == (250, 250)

    coords = (3, 0)
    assert get_piece_gui_coords(coords, square_dist, top_left_coords) == (150, 250)

    coords = (7, 7)
    assert get_piece_gui_coords(coords, square_dist, top_left_coords) == (450, 450)


def test_get_surface_mouse_offset():
    surface_pos = (200, 300)
    mouse_pos = (150, 250)
    assert get_surface_mouse_offset(surface_pos, mouse_pos) == (50, 50)

    surface_pos = (200, 300)
    mouse_pos = (200, 300)
    assert get_surface_mouse_offset(surface_pos, mouse_pos) == (0, 0)

    surface_pos = (100, 200)
    mouse_pos = (150, 250)
    assert get_surface_mouse_offset(surface_pos, mouse_pos) == (-50, -50)

    surface_pos = (0, 0)
    mouse_pos = (0, 0)
    assert get_surface_mouse_offset(surface_pos, mouse_pos) == (0, 0)