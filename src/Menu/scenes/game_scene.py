import pygame
import sys
import os

# Add paths for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
menu_dir = os.path.dirname(current_dir)
sys.path.insert(0, os.path.dirname(menu_dir))  # Add src directory
sys.path.insert(0, os.path.join(os.path.dirname(menu_dir), 'Game'))  # Add Game directory

# Use relative imports
from .base_scene import Scene
from Game.core.game import Run_Game

class GameScene(Scene):
    """Scene for the main game"""
    def __init__(self, screen, character_select=0, game_mode=0):
        super().__init__(screen)
        self.character_select = character_select  # 1: male, 0: female
        self.game_mode = game_mode  # 1: normal, 0: endless
        
    def setup(self):
        """Initialize the game"""
        super().setup()
        
        # Stop menu music before starting game
        pygame.mixer.music.stop()
        
    def update(self, dt):
        """Update the game"""
        # Run the game with selected character and mode
        next_scene = Run_Game(self.game_mode, self.character_select)
        
        if next_scene:
            # If the game returned a scene (like game over), switch to it
            self.switch_to_scene(next_scene)
        else:
            # If no scene was returned, return to main menu
            from .main_menu_scene import MainMenuScene
            self.switch_to_scene(MainMenuScene(self.screen))
            
        # Mark this scene as done
        self.is_running = False
        
    def draw(self):
        """Draw the game"""
        # The game handles its own drawing
        pass
