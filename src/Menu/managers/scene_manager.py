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
        
    def start_scene(self, scene):
        """
        Set and start a new scene
        
        Args:
            scene: The scene to start
        """
        # Clear all timers before switching scenes
        clear_all_timers()
        
        # Ensure mouse is visible when switching scenes
        pygame.mouse.set_visible(True)
        self.current_scene = scene
        self.current_scene.setup()
        
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
                    else:
                        print(f"Unknown scene name: {self.current_scene.next_scene}")
                        next_scene = None
                else:
                    next_scene = self.current_scene.next_scene
                    
                if next_scene:
                    self.start_scene(next_scene)
                
        # If we exit the loop but still running, we might need to go back to game
        return not self.running
