import pygame
import sys
import os

# Add paths for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
menu_dir = os.path.dirname(current_dir)
sys.path.insert(0, os.path.dirname(menu_dir))  # Add src directory

# Use relative imports
from .base_scene import Scene
from ..components.button import ImageButton
from ..utils.asset_loader import AssetLoader
from ..utils.drawing import draw_image
from ..config.constants import BLACK_COLOR, WHITE_COLOR

# Import Game font manager
from Game.managers.font_manager import FontManager

class GameOverScene(Scene):
    """Game over scene with option to return to main menu"""
    def __init__(self, screen):
        super().__init__(screen)
        self.assets = AssetLoader()
        
        # Use the game's font manager
        self.font_manager = FontManager()
        self.title_font = self.font_manager.title_font
        self.medium_font = self.font_manager.medium_font
        self.small_font = self.font_manager.small_font
        
        # Track button state
        self.button_hover = False
        self.back_button = None
        self.final_score = 0
        
    def setup(self, score):
        """Initialize game over elements"""
        super().setup()
        self.final_score = score
        
        # Create back button
        button_width, button_height = 200, 50
        self.back_button = pygame.Rect(
            (self.screen.get_width() - button_width) // 2,
            self.screen.get_height() * 3 // 4,
            button_width,
            button_height
        )
        
        # No need for UI elements list as we're drawing directly
        
    def update(self, dt):
        """Update the game over screen"""
        pass  # No animation updates needed
    
    def draw(self):
        """Draw the game over screen"""
        # Fill background with semi-transparent black
        self.screen.fill(BLACK_COLOR)
        
        # Create overlay for better text visibility
        overlay = pygame.Surface((self.screen.get_width(), self.screen.get_height()), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))  # Semi-transparent black
        self.screen.blit(overlay, (0, 0))
        
        # Draw game over title
        title_text = self.title_font.render("GAME OVER", True, (255, 0, 0))
        title_rect = title_text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 3))
        self.screen.blit(title_text, title_rect)
        
        # Draw score
        score_text = self.medium_font.render(f"Final Score: {self.final_score}", True, WHITE_COLOR)
        score_rect = score_text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))
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
        
    def handle_event(self, event):
        """Handle pygame events"""
        if super().handle_event(event):
            return True
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
                self.next_scene = "menu"
                self.is_running = False
                return True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                if self.back_button and self.back_button.collidepoint(event.pos):
                    self.next_scene = "menu"
                    self.is_running = False
                    return True
        elif event.type == pygame.MOUSEMOTION:
            # Update button hover state
            if self.back_button:
                self.button_hover = self.back_button.collidepoint(event.pos)
                return True
                
        return False
