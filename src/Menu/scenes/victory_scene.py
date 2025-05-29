import pygame
import sys
import os
from pathlib import Path

# Add paths for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
menu_dir = os.path.dirname(current_dir)
sys.path.insert(0, os.path.dirname(menu_dir))  # Add src directory

# Use relative imports
from .base_scene import Scene
from ..utils.asset_loader import AssetLoader
from ..config.constants import BLACK_COLOR, WHITE_COLOR

# Import Game font manager
from Game.managers.font_manager import FontManager

# Get the root directory of the project
root_dir = Path(__file__).parent.parent.parent.parent

class VictoryScene(Scene):
    """Victory scene shown after defeating the boss"""
    def __init__(self, screen):
        super().__init__(screen)
        self.assets = AssetLoader()
        self.width, self.height = screen.get_size()
        self.next_scene = None
        self.score = 0
        
        # Initialize font manager
        self.font_manager = FontManager()
        self.title_font = self.font_manager.title_font
        self.large_font = self.font_manager.large_font
        self.medium_font = self.font_manager.medium_font
        self.small_font = self.font_manager.small_font
        
        # Button attributes
        self.back_button = None
        self.button_hover = False
        
        # Colors
        self.GOLD = (255, 215, 0)
        
        # Background
        self.background = None
        try:
            bg_path = root_dir / "assets" / "images" / "backgrounds" / "gameoverlogo.png"
            if bg_path.exists():
                self.background = self.assets.get_image('gameoverlogo')
                self.background = pygame.transform.scale(self.background, (self.width, self.height))
        except Exception as e:
            print(f"Error loading victory background: {e}")
        
        # Music
        self.victory_music = None
        try:
            music_path = root_dir / "assets" / "sounds" / "victory_music.ogg"
            if music_path.exists():
                self.victory_music = str(music_path)
        except Exception as e:
            print(f"Error loading victory music: {e}")
            
        # Setup UI elements
        self.ui_elements = []
        
    def setup(self, score=0):
        """Initialize the scene with the player's score"""
        super().setup()
        self.next_scene = None
        self.score = score
        
        # Create back button
        button_width, button_height = 200, 50
        self.back_button = pygame.Rect(
            (self.width - button_width) // 2,
            self.height * 3 // 4,
            button_width,
            button_height
        )
        
        # Play victory music if available
        if self.victory_music:
            pygame.mixer.music.load(self.victory_music)
            pygame.mixer.music.play(loops=-1)
    
    def handle_event(self, event):
        """Handle pygame events"""
        if super().handle_event(event):
            return True
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.next_scene = "menu"
                self.is_running = False
                return True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.back_button.collidepoint(event.pos):
                self.next_scene = "menu"
                self.is_running = False
                return True
        elif event.type == pygame.MOUSEMOTION:
            self.button_hover = self.back_button.collidepoint(event.pos)
            
        return False
    
    def update(self, dt):
        """Update scene state"""
        for element in self.ui_elements:
            element.update(dt)
            
        # Update button animation if needed
        pass
    
    def draw(self):
        """Draw the scene"""
        # Clear the screen
        self.screen.fill(BLACK_COLOR)
        
        # Create overlay for better text visibility
        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))  # Semi-transparent black
        self.screen.blit(overlay, (0, 0))
        
        # Draw background if available
        if self.background:
            self.screen.blit(self.background, (0, 0))
        
        # Draw victory text
        victory_text = self.title_font.render("VICTORY!", True, self.GOLD)
        text_rect = victory_text.get_rect(center=(self.width // 2, self.height // 3))
        self.screen.blit(victory_text, text_rect)
        
        # Draw score
        score_text = self.large_font.render(f"Final Score: {self.score}", True, WHITE_COLOR)
        score_rect = score_text.get_rect(center=(self.width // 2, self.height // 2))
        self.screen.blit(score_text, score_rect)
        
        # Draw back button
        button_color = (100, 100, 255) if self.button_hover else (70, 70, 220)
        pygame.draw.rect(self.screen, button_color, self.back_button, border_radius=10)
        pygame.draw.rect(self.screen, (200, 200, 255), self.back_button, width=2, border_radius=10)
        
        # Draw button text
        button_text = self.medium_font.render("Back to Menu", True, WHITE_COLOR)
        button_text_rect = button_text.get_rect(center=self.back_button.center)
        self.screen.blit(button_text, button_text_rect)
        
        # Update display
        pygame.display.flip()
    
    def cleanup(self):
        """Clean up resources"""
        pygame.mixer.music.stop()
        super().cleanup()
