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
        
        # Fonts
        self.large_font = pygame.font.Font(None, 72)
        self.medium_font = pygame.font.Font(None, 48)
        self.small_font = pygame.font.Font(None, 36)
        
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
        
        # Play victory music if available
        if self.victory_music:
            pygame.mixer.music.load(self.victory_music)
            pygame.mixer.music.play(loops=-1)
    
    def handle_event(self, event):
        """Handle pygame events"""
        if super().handle_event(event):
            return True
            
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_ESCAPE, pygame.K_RETURN, pygame.K_SPACE):
                self.is_running = False
                self.next_scene = "menu"
                return True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self.is_running = False
            self.next_scene = "menu"
            return True
            
        return False
    
    def update(self, dt):
        """Update scene state"""
        for element in self.ui_elements:
            element.update(dt)
    
    def draw(self):
        """Draw the scene"""
        # Clear the screen
        self.screen.fill(BLACK_COLOR)
        
        # Draw background if available
        if self.background:
            self.screen.blit(self.background, (0, 0))
        
        # Draw victory text
        victory_text = self.large_font.render("VICTORY!", True, self.GOLD)
        text_rect = victory_text.get_rect(center=(self.width // 2, self.height // 3))
        self.screen.blit(victory_text, text_rect)
        
        # Draw score
        score_text = self.medium_font.render(f"Final Score: {self.score}", True, WHITE_COLOR)
        score_rect = score_text.get_rect(center=(self.width // 2, self.height // 2))
        self.screen.blit(score_text, score_rect)
        
        # Draw instruction text
        instruction = self.medium_font.render("Press any key to continue...", True, WHITE_COLOR)
        instr_rect = instruction.get_rect(center=(self.width // 2, self.height * 2 // 3))
        self.screen.blit(instruction, instr_rect)
        
        # Draw UI elements
        for element in self.ui_elements:
            element.draw(self.screen)
            
        pygame.display.flip()
    
    def cleanup(self):
        """Clean up resources"""
        pygame.mixer.music.stop()
        super().cleanup()
