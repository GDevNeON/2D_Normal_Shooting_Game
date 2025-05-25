import pygame
import os

class FontManager:
    """
    Manages game fonts to ensure consistency across all menu screens
    """
    def __init__(self):
        # Get the directory of the current file
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # Path to font file
        self.font_path = os.path.normpath(os.path.join(
            current_dir, '..', 'assets', 'fonts', 'game_font.ttf'
        ))
        
        # Initialize font cache
        self._fonts = {}
        
    def get_font(self, size):
        """Get a font with specific size"""
        if size not in self._fonts:
            try:
                # Try to load the custom game font
                self._fonts[size] = pygame.font.Font(self.font_path, size)
            except Exception as e:
                print(f"Warning: Could not load custom font: {e}")
                # Fall back to default font if custom font fails
                self._fonts[size] = pygame.font.SysFont("Arial", size)
        
        return self._fonts[size]
    
    # Font size constants for different UI elements
    TITLE_SIZE = 30
    HEADING_SIZE = 24
    SUBHEADING_SIZE = 20
    NORMAL_SIZE = 16
    SMALL_SIZE = 12
    
    # Helper methods for common font sizes
    def title_font(self):
        return self.get_font(self.TITLE_SIZE)
    
    def heading_font(self):
        return self.get_font(self.HEADING_SIZE)
    
    def subheading_font(self):
        return self.get_font(self.SUBHEADING_SIZE)
    
    def normal_font(self):
        return self.get_font(self.NORMAL_SIZE)
    
    def small_font(self):
        return self.get_font(self.SMALL_SIZE)
