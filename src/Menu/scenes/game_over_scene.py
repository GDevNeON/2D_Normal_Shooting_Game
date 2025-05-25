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
from ..config.constants import BLACK_COLOR

class GameOverScene(Scene):
    """Game over scene with option to return to main menu"""
    def __init__(self, screen):
        super().__init__(screen)
        self.assets = AssetLoader()
        
    def setup(self):
        """Initialize game over elements"""
        super().setup()
        
        # Load game over title and button images
        self.game_over_title = self.assets.get_image('game_over_title')
        back_button_img = self.assets.get_image('try_again_button')
        
        # Calculate positions
        screen_center_x_1 = self.screen.get_width() / 3.1
        screen_center_x_2 = self.screen.get_width() / 1.91
        five_six_height = int(self.screen.get_height() * 0.8)
        
        # Calculate button dimensions
        button_width = back_button_img.get_width() * 0.4
        button_height = back_button_img.get_height() * 0.3
        
        # Create back to menu button
        self.back_to_menu = ImageButton(
            screen_center_x_2 - button_width, 
            five_six_height - button_height / 2, 
            back_button_img, 
            0.6
        ).set_callback(self.on_back_clicked)
        
        # Add buttons to ui_elements
        self.ui_elements = [self.back_to_menu]
        
    def update(self, dt):
        """Update the game over screen"""
        super().update(dt)
    
    def draw(self):
        """Draw the game over screen"""
        # Fill background
        self.screen.fill(BLACK_COLOR)
        
        # Draw game over title
        draw_image(self.screen, self.game_over_title, 0.3, self.screen.get_width() / 3.1, -20)
        
        # Draw UI elements
        super().draw()
        
    def on_back_clicked(self):
        """Handle back to menu button click"""
        from .main_menu_scene import MainMenuScene
        self.switch_to_scene(MainMenuScene(self.screen))
