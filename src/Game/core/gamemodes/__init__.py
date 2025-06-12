"""
Game Modes Module

This module contains the base class and implementations for different game modes.
"""

from abc import ABC, abstractmethod
import pygame
import importlib
import pkgutil

class BaseGameMode(ABC):
    """Base class for all game modes."""
    
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.rules = {}
        self.is_endless = False
        self.victory_condition = None
        self.defeat_condition = None
    
    @abstractmethod
    def setup(self, game_state):
        """Initialize the game mode with the given game state."""
        pass
    
    @abstractmethod
    def update(self, game_state, dt):
        """Update the game mode state."""
        pass
    
    @abstractmethod
    def check_win_condition(self, game_state):
        """Check if the win condition is met."""
        pass
    
    @abstractmethod
    def check_lose_condition(self, game_state):
        """Check if the lose condition is met."""
        pass
    
    @abstractmethod
    def handle_events(self, game_state, event):
        """Handle game events specific to this game mode."""
        pass

# Dictionary to store all available game modes
GAME_MODES = {}

def register_game_mode(mode_class):
    """Register a game mode class."""
    mode = mode_class()
    GAME_MODES[mode.name.lower().replace(' ', '_')] = mode
    return mode_class

# Import all game modes to ensure they're registered
# This will automatically register them via the @register_game_mode decorator
try:
    from . import elite_madness
    from . import speed_demon
    from . import double_bozos
except ImportError as e:
    print(f"[WARNING] Failed to import game modes: {e}")
