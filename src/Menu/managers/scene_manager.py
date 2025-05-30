import pygame
import sys
from Game.core.define import clear_all_timers

class SceneManager:
    """
    Manages scene transitions and the game loop for menu scenes
    """
    def __init__(self, screen):
        self.screen = screen
        self.current_scene = None
        self.running = False
        self.clock = pygame.time.Clock()
        self.fps = 60
        
    def start_scene(self, scene, data=None):
        """
        Set and start a new scene
        
        Args:
            scene: The scene to start
            data: Optional data to pass to the scene (like score)
        """
        print(f"[DEBUG] SceneManager.start_scene called with data: {data}")
        
        # Clear all timers before switching scenes
        clear_all_timers()
        
        # Ensure mouse is visible when switching scenes
        pygame.mouse.set_visible(True)
        self.current_scene = scene
        
        # Setup scene with data if provided
        if data is not None:
            print(f"[DEBUG] Setting up scene with score={data}")
            self.current_scene.setup(score=data)
            # Directly ensure score is set for GameOverScene and VictoryScene
            if hasattr(self.current_scene, 'final_score'):
                print(f"[DEBUG] Directly setting final_score={data}")
                self.current_scene.final_score = data
            # Always set the base score property
            self.current_scene.score = data
        else:
            print(f"[DEBUG] Setting up scene with default values")
            self.current_scene.setup()
        
    def change_scene(self, scene_name, data=None):
        """
        Change to a different scene with optional data
        
        Args:
            scene_name: String name of the scene to change to
            data: Optional data to pass to the scene (like score)
        """
        print(f"[DEBUG] SceneManager.change_scene called with: {scene_name}, data={data}")
        
        if scene_name == "menu":
            from ..scenes.main_menu_scene import MainMenuScene
            next_scene = MainMenuScene(self.screen)
            self.start_scene(next_scene)
        elif scene_name == "game_over":
            from ..scenes.game_over_scene import GameOverScene
            next_scene = GameOverScene(self.screen)
            print(f"[DEBUG] Creating new GameOverScene, passing score: {data}")
            # Directly set score for extra certainty
            next_scene.final_score = data if data is not None else 0
            next_scene.score = data if data is not None else 0
            self.start_scene(next_scene, data)
        elif scene_name == "victory":
            from ..scenes.victory_scene import VictoryScene
            next_scene = VictoryScene(self.screen)
            print(f"[DEBUG] Creating new VictoryScene, passing score: {data}")
            # Directly set score for extra certainty
            next_scene.score = data if data is not None else 0
            self.start_scene(next_scene, data)
        else:
            print(f"Unknown scene name: {scene_name}")
    
    def run(self):
        """
        Run the main game loop for the current scene
        """
        self.running = True
        
        while self.running and self.current_scene and self.current_scene.is_running:
            # Calculate delta time
            dt = self.clock.tick(self.fps) / 1000.0  # Convert to seconds
            
            # Process events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                    sys.exit()
                    
                # Let the scene handle the event
                self.current_scene.handle_event(event)
                
            # Update scene
            self.current_scene.update(dt)
            
            # Draw scene
            self.current_scene.draw()
            
            # Update display
            pygame.display.update()
            
            # Check for scene transition
            if self.current_scene.next_scene:
                self.current_scene.shutdown()
                # Handle string scene names
                if isinstance(self.current_scene.next_scene, str):
                    if self.current_scene.next_scene == "menu":
                        from ..scenes.main_menu_scene import MainMenuScene
                        next_scene = MainMenuScene(self.screen)
                        self.start_scene(next_scene)
                    elif self.current_scene.next_scene == "game_over":
                        from ..scenes.game_over_scene import GameOverScene
                        next_scene = GameOverScene(self.screen)
                        # Use passed data if available (through self.current_scene.score)
                        score = getattr(self.current_scene, 'score', 0)
                        self.start_scene(next_scene, score)
                    elif self.current_scene.next_scene == "victory":
                        from ..scenes.victory_scene import VictoryScene
                        next_scene = VictoryScene(self.screen)
                        # Use passed data if available (through self.current_scene.score)
                        score = getattr(self.current_scene, 'score', 0)
                        self.start_scene(next_scene, score)
                    else:
                        print(f"Unknown scene name: {self.current_scene.next_scene}")
                        next_scene = None
                else:
                    next_scene = self.current_scene.next_scene
                    self.start_scene(next_scene)
                
        # If we exit the loop but still running, we might need to go back to game
        return not self.running
