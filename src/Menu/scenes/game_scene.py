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
        self.parent_scene_manager = None  # Will store the scene manager
        
    def setup(self):
        """Initialize the game"""
        super().setup()
        
        # Stop menu music before starting game
        pygame.mixer.music.stop()
        
    def update(self, dt):
        """Update the game"""
        # Debug logs to track scene_manager
        print(f"[DEBUG] GameScene.update - has parent_scene_manager: {hasattr(self, 'parent_scene_manager')}")
        
        # Get the scene manager from the parent scene if available
        scene_manager = None
        if hasattr(self, 'parent_scene_manager'):
            scene_manager = self.parent_scene_manager
            print(f"[DEBUG] Using parent_scene_manager: {scene_manager is not None}")
        
        # Run the game with selected character and mode, passing the scene manager
        next_scene = Run_Game(self.game_mode, self.character_select, scene_manager)
        
        if next_scene:
            print(f"[DEBUG] GameScene - game returned a scene: {type(next_scene).__name__}")
            # If the game returned a scene (like game over), switch to it
            if hasattr(next_scene, 'score'):
                self.score = next_scene.score
                print(f"[DEBUG] GameScene - setting score from next_scene: {self.score}")
                
                # Use the scene_manager directly if available
                if scene_manager:
                    scene_name = "game_over" if "GameOverScene" in str(type(next_scene)) else "victory"
                    print(f"[DEBUG] Directly using scene_manager to change to {scene_name} with score {self.score}")
                    scene_manager.change_scene(scene_name, self.score)
                else:
                    # Fallback to switch_to_scene
                    print(f"[DEBUG] Using switch_to_scene with score {self.score}")
                    self.switch_to_scene(next_scene, self.score)
            else:
                # For other scenes
                if scene_manager:
                    # Determine scene name
                    if "MainMenuScene" in str(type(next_scene)):
                        scene_manager.change_scene("menu")
                    else:
                        # Fallback to switch_to_scene for unknown scenes
                        self.switch_to_scene(next_scene)
                else:
                    self.switch_to_scene(next_scene)
        else:
            # If no scene was returned, return to main menu
            print(f"[DEBUG] GameScene - game returned None, going back to menu")
            from .main_menu_scene import MainMenuScene
            
            if scene_manager:
                scene_manager.change_scene("menu")
            else:
                self.switch_to_scene(MainMenuScene(self.screen))
            
        # Mark this scene as done
        self.is_running = False
        
    def draw(self):
        """Draw the game"""
        # The game handles its own drawing
        pass
