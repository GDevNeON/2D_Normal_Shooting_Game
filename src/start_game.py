"""
Main entry point for the 2D Normal Shooting Game
This file should be run to start the game.
"""
import os
import sys
import pygame

# Initialize pygame
pygame.init()
pygame.mixer.init()

# Add the src directory to the Python path
src_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, src_dir)

# Import modules
from Menu.scenes.main_menu_scene import MainMenuScene
from Menu.managers.scene_manager import SceneManager
from Menu.config.constants import WIDTH_SCREEN, HEIGHT_SCREEN

# Import Game modules
from Game.core.define import *

def main():
    """Main entry point for the game"""
    # Set up display
    pygame.display.set_caption('A 2D NORMAL SHOOTING GAME')
    screen = pygame.display.set_mode((WIDTH_SCREEN, HEIGHT_SCREEN))
    
    # Create scene manager
    manager = SceneManager(screen)
    
    # Start with main menu scene
    main_menu = MainMenuScene(screen)
    
    # Store the scene manager for future reference
    # This will be passed down to all scenes
    main_menu.parent_scene_manager = manager
    
    manager.start_scene(main_menu)
    
    # Run the game loop
    manager.run()
    
    # Clean up when done
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
