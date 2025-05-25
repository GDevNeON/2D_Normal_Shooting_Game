import pygame

class Scene:
    """Base class for all game scenes"""
    def __init__(self, screen):
        self.screen = screen
        self.next_scene = None
        self.is_running = False
        self.ui_elements = []
        
    def setup(self):
        """Initialize scene - called when scene becomes active"""
        self.is_running = True
        
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
        
    def switch_to_scene(self, scene):
        """Set the next scene to transition to"""
        self.next_scene = scene
        self.is_running = False
