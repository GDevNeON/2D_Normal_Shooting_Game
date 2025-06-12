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
from Game.core.game_engine import Run_Game

class GameScene(Scene):
    """Scene for the main game"""
    def __init__(self, screen, character_select=0, game_mode=0, custom_mode_name=None):
        super().__init__(screen)
        self.character_select = character_select  # 1: male, 0: female
        self.game_mode = game_mode  # 1: normal, 0: endless, 2: custom
        self.custom_mode_name = custom_mode_name  # Name of the custom game mode if any
        self.parent_scene_manager = None  # Will store the scene manager
        
        # Debug info
        print(f"[DEBUG] GameScene initialized - Character: {character_select}, Mode: {game_mode}, Custom Mode: {custom_mode_name}")
        
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
        scene_manager = getattr(self, 'parent_scene_manager', None)
        print(f"[DEBUG] Using parent_scene_manager: {scene_manager is not None}")
        
        try:
            # Run the game with selected character, mode, and custom mode, passing the scene manager
            next_scene = Run_Game(
                current_mode=self.game_mode, 
                character_select=self.character_select, 
                custom_mode_name=self.custom_mode_name,
                scene_manager=scene_manager
            )
            
            if next_scene is not None:
                print(f"[DEBUG] GameScene - game returned a scene: {type(next_scene).__name__}")
                
                # Get the score from the scene if available
                scene_score = getattr(next_scene, 'score', 0)
                self.score = scene_score
                print(f"[DEBUG] GameScene - setting score to: {self.score}")
                
                # Determine scene type
                scene_type = type(next_scene).__name__
                
                # Use scene manager if available
                if scene_manager:
                    if "GameOverScene" in scene_type:
                        print(f"[DEBUG] Changing to game over scene with score: {self.score}")
                        scene_manager.change_scene("game_over", self.score)
                    elif "VictoryScene" in scene_type:
                        print(f"[DEBUG] Changing to victory scene with score: {self.score}")
                        scene_manager.change_scene("victory", self.score)
                    elif "MainMenuScene" in scene_type:
                        scene_manager.change_scene("menu")
                    else:
                        print(f"[WARNING] Unknown scene type: {scene_type}")
                        scene_manager.change_scene("menu")
                else:
                    # Fallback to direct scene switching
                    print(f"[DEBUG] No scene manager, using direct scene switch")
                    self.switch_to_scene(next_scene, self.score)
            else:
                # If no scene was returned, return to main menu
                print("[DEBUG] Game returned None, returning to main menu")
                if scene_manager:
                    scene_manager.change_scene("menu")
                else:
                    from .main_menu_scene import MainMenuScene
                    self.switch_to_scene(MainMenuScene(self.screen))
                    
        except Exception as e:
            print(f"[ERROR] Error in game loop: {str(e)}")
            import traceback
            traceback.print_exc()
            
            # Try to return to main menu even if there was an error
            if scene_manager:
                scene_manager.change_scene("menu")
            else:
                from .main_menu_scene import MainMenuScene
                self.switch_to_scene(MainMenuScene(self.screen))
        
        # Mark this scene as done
        self.is_running = False
        
    def draw(self):
        """Draw the game"""
        # The game handles its own drawing
        pass
