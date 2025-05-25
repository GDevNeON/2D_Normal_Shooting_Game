import pygame
import sys
import os

# Add paths for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
menu_dir = os.path.dirname(current_dir)
src_dir = os.path.dirname(menu_dir)
sys.path.insert(0, src_dir)  # Add src directory

# Import sound utility
from ..utils.sound_utils import play_button_select

# Use relative imports
from .ui_element import UIElement

class Button(UIElement):
    """Button class with text or callback functionality"""
    def __init__(self, x, y, width, height, text, font, text_color=(255, 255, 255), 
                 bg_color=(50, 50, 50), hover_color=(70, 70, 70)):
        super().__init__(x, y, width, height)
        self.text = text
        self.font = font
        self.text_color = text_color
        self.bg_color = bg_color
        self.hover_color = hover_color
        self.callback = None
        self._create_surfaces()
        
    def _create_surfaces(self):
        """Create text surface"""
        self.text_surf = self.font.render(self.text, True, self.text_color)
        self.text_rect = self.text_surf.get_rect(center=self.rect.center)
        
    def set_callback(self, callback):
        """Set callback function to be called when button is clicked"""
        self.callback = callback
        return self
        
    def update(self, dt):
        """Update button state"""
        super().update(dt)
        
    def draw(self, surface):
        """Draw the button on the given surface"""
        # Draw button background
        color = self.hover_color if self.is_hovered else self.bg_color
        pygame.draw.rect(surface, color, self.rect, border_radius=12)
        pygame.draw.rect(surface, (200, 200, 200), self.rect, 2, border_radius=12)
        
        # Draw text
        surface.blit(self.text_surf, self.text_rect)
        
    def handle_event(self, event):
        """Handle pygame events"""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.is_hovered and self.callback:
                self.callback()
                return True
        return False


class ImageButton(UIElement):
    """Button class that uses an image instead of text"""
    def __init__(self, x, y, image, scale=1.0):
        # Scale the image
        width = image.get_width()
        height = image.get_height()
        self.original_image = image
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        super().__init__(x, y, self.image.get_width(), self.image.get_height())
        self.rect.topleft = (x, y)
        self.callback = None
        self.scale = scale
        self.hover_scale = scale * 1.05  # Slightly larger when hovered
        
    def set_callback(self, callback):
        """Set callback function to be called when button is clicked"""
        self.callback = callback
        return self
        
    def update(self, dt):
        """Update button state"""
        previous_hover = self.is_hovered
        super().update(dt)
        
        # Change scale on hover state change
        if previous_hover != self.is_hovered:
            if self.is_hovered:
                # Scale up when hovered
                self.image = pygame.transform.scale(
                    self.original_image, 
                    (int(self.original_image.get_width() * self.hover_scale), 
                     int(self.original_image.get_height() * self.hover_scale))
                )
            else:
                # Return to normal scale
                self.image = pygame.transform.scale(
                    self.original_image, 
                    (int(self.original_image.get_width() * self.scale), 
                     int(self.original_image.get_height() * self.scale))
                )
            # Update rect but keep the center position
            center = self.rect.center
            self.rect = self.image.get_rect()
            self.rect.center = center
        
    def draw(self, surface):
        """Draw the button on the given surface"""
        surface.blit(self.image, self.rect.topleft)
        
    def handle_event(self, event):
        """Handle pygame events"""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.is_hovered and self.callback:
                self.callback()
                return True
        return False
