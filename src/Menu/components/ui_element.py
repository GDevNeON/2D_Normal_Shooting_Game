import pygame

class UIElement:
    """Base class for all UI elements"""
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.is_hovered = False
        
    def update(self, dt):
        """Update element state"""
        mouse_pos = pygame.mouse.get_pos()
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        
    def draw(self, surface):
        """Draw the element on the given surface"""
        pass
        
    def handle_event(self, event):
        """Handle pygame events"""
        pass
