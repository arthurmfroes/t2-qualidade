import pytest
from unittest.mock import Mock, patch
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pygame as pg
from checkers import main

@pytest.fixture
def mock_pygame():
    with patch('checkers.pg') as mock_pg:
        yield mock_pg

@pytest.fixture
def mock_game_control():
    with patch('checkers.GameControl') as mock_gc:
        yield mock_gc



def test_main_cpu_mode(mock_pygame, mock_game_control):
    mock_pygame.display.set_mode.return_value = Mock()
    mock_pygame.font.SysFont.return_value = Mock()
    mock_pygame.time.Clock.return_value = Mock()
    mock_game_control.return_value = Mock()

    with patch('sys.argv', ['checkers.py', 'cpu']):
        main('cpu')

    mock_pygame.init.assert_called_once()
    mock_pygame.display.set_mode.assert_called_once_with((700, 500))
    mock_pygame.display.set_caption.assert_called_once_with('Checkers in Python')
    mock_pygame.font.SysFont.assert_called_once_with("Arial", 25)
    mock_game_control.assert_called_once_with("W", True)



def test_main_pvp_mode(mock_pygame, mock_game_control):
    mock_pygame.display.set_mode.return_value = Mock()
    mock_pygame.font.SysFont.return_value = Mock()
    mock_pygame.time.Clock.return_value = Mock()
    mock_game_control.return_value = Mock()

    with patch('sys.argv', ['checkers.py', 'pvp']):
        main('pvp')

    mock_pygame.init.assert_called_once()
    mock_pygame.display.set_mode.assert_called_once_with((700, 500))
    mock_pygame.display.set_caption.assert_called_once_with('Checkers in Python')
    mock_pygame.font.SysFont.assert_called_once_with("Arial", 25)
    mock_game_control.assert_called_once_with("W", False)