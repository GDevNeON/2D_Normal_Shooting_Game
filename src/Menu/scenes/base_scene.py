import pygame

class Scene:
    """Base class for all game scenes"""
    def __init__(self, screen):
        self.screen = screen
        self.next_scene = None
        self.is_running = False
        self.ui_elements = []
        self.score = 0  # Add score attribute to base class
        self.parent_scene_manager = None  # Reference to scene manager
        
    def setup(self, score=0):
        """Initialize scene - called when scene becomes active"""
        self.is_running = True
        self.score = score  # Store score
        
    def update(self, dt):
        """Update scene state - dt is delta time in seconds"""
        for element in self.ui_elements:
            element.update(dt)
            
    def draw(self):
        """Draw the scene on the screen"""
        for element in self.ui_elements:
            element.draw(self.screen)
            
    def handle_event(self, event):
        """Handle pygame events"""
        for element in self.ui_elements:
            if element.handle_event(event):
                # If an element handled the event, return
                return True
        return False
        
    def shutdown(self):
        """Clean up when scene is no longer active"""
        self.is_running = False
        
    def switch_to_scene(self, scene, score=None):
        """Set the next scene to transition to"""
        self.next_scene = scene
        
        # Pass parent_scene_manager to the next scene
        if hasattr(self, 'parent_scene_manager') and self.parent_scene_manager:
            scene.parent_scene_manager = self.parent_scene_manager
        
        # Pass score to the next scene
        if score is not None:
            self.score = score  # Store score for current scene
            scene.score = score  # Pass score directly to next scene
            
        self.is_running = False
