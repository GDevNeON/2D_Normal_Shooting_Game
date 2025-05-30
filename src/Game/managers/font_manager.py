import pygame
import os

class FontManager:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(FontManager, cls).__new__(cls)
            cls._instance._initialize_fonts()
        return cls._instance
    
    def _initialize_fonts(self):
        """Initialize all game fonts"""
        try:
            # Try to load the custom font from the Menu directory
            font_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "Menu", "assets", "fonts", "game_font.ttf")
            self.title_font = pygame.font.Font(font_path, 30)
            self.large_font = pygame.font.Font(font_path, 22)
            self.medium_font = pygame.font.Font(font_path, 16)
            self.small_font = pygame.font.Font(font_path, 14)
            self.tiny_font = pygame.font.Font(font_path, 12)
            print("Custom font loaded successfully")
        except Exception as e:
            print(f"Error loading custom font: {e}. Falling back to system fonts.")
            # Fallback to system fonts if custom font not found
            self.title_font = pygame.font.SysFont("Arial", 30, bold=False)
            self.large_font = pygame.font.SysFont("Arial", 22, bold=False)
            self.medium_font = pygame.font.SysFont("Arial", 16)
            self.small_font = pygame.font.SysFont("Arial", 14)
            self.tiny_font = pygame.font.SysFont("Arial", 12)
    
    @classmethod
    def get_font(cls, size=24):
        """Get a font with the specified size"""
        instance = cls()
        if size >= 30:
            return instance.title_font if size >= 30 else instance.large_font
        elif size >= 22:
            return instance.medium_font
        elif size >= 16:
            return instance.small_font
        else:
            return instance.tiny_font
