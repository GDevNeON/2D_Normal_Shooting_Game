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
        
    def get_font(self, size, bold=False, italic=False):
        """
        Get a font with specific size and style
        
        Args:
            size: Font size
            bold: Whether to use bold style
            italic: Whether to use italic style
            
        Returns:
            pygame.Font: The requested font with specified style
        """
        # Create a unique key for the font with its style
        font_key = (size, bold, italic)
        
        if font_key not in self._fonts:
            try:
                # Try to load the custom game font with specified style
                font = pygame.font.Font(self.font_path, size)
                # Apply bold and italic styles
                font.set_bold(bold)
                font.set_italic(italic)
                self._fonts[font_key] = font
            except Exception as e:
                print(f"Warning: Could not load custom font: {e}")
                # Fall back to default font if custom font fails
                self._fonts[font_key] = pygame.font.SysFont("Arial", size, bold=bold, italic=italic)
        
        return self._fonts[font_key]
    
    # Font size constants for different UI elements
    TITLE_SIZE = 30
    HEADING_SIZE = 24
    SUBHEADING_SIZE = 20
    NORMAL_SIZE = 16
    SMALL_SIZE = 12
    
    # Helper methods for common font sizes and styles
    def title_font(self, bold=False, italic=False):
        return self.get_font(self.TITLE_SIZE, bold, italic)
    
    def heading_font(self, bold=False, italic=False):
        return self.get_font(self.HEADING_SIZE, bold, italic)
    
    def subheading_font(self, bold=False, italic=False):
        return self.get_font(self.SUBHEADING_SIZE, bold, italic)
    
    def normal_font(self, bold=False, italic=False):
        return self.get_font(self.NORMAL_SIZE, bold, italic)
    
    def small_font(self, bold=False, italic=False):
        return self.get_font(self.SMALL_SIZE, bold, italic)
