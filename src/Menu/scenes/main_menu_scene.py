import pygame
import sys
import os

# Add paths for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
menu_dir = os.path.dirname(current_dir)
sys.path.insert(0, os.path.dirname(menu_dir))  # Add src directory
sys.path.insert(0, os.path.join(os.path.dirname(menu_dir), 'Game'))  # Add Game directory

# Use relative imports
from .base_scene import Scene
from ..components.button import ImageButton
from ..utils.asset_loader import AssetLoader
from ..config.constants import *

class MainMenuScene(Scene):
    """Main menu scene with play, settings, and quit options"""
    def __init__(self, screen):
        super().__init__(screen)
        self.assets = AssetLoader()
        
    def setup(self):
        """Initialize the main menu elements"""
        super().setup()
        
        # Calculate screen center
        screen_center_x = self.screen.get_width() // 2
        three_fourth_height = int(self.screen.get_height() * 0.7)
        button_spacing = 110
        
        # Load background and title
        self.background = self.assets.get_image('background')
        self.title_img = self.assets.get_image('title')
        
        # Create title
        self.title = ImageButton(
            screen_center_x - (self.title_img.get_width() * 0.5),
            90,
            self.title_img,
            1
        )
        
        # Scale background to fit screen
        self.main_background = pygame.transform.scale(
            self.background, 
            (int(self.background.get_width() * 0.7115), 
             int(self.background.get_height() * 0.7165))
        )
        
        # Calculate button dimensions
        play_button_img = self.assets.get_image('play_button')
        settings_button_img = self.assets.get_image('setting_button')
        quit_button_img = self.assets.get_image('quit_button')
        button_width = play_button_img.get_width() * 0.4
        
        # Create buttons
        self.button_play = ImageButton(
            screen_center_x - button_width, 
            three_fourth_height - play_button_img.get_height() * 0.3 / 2 - button_spacing, 
            play_button_img, 
            0.9
        ).set_callback(self.on_play_clicked)
        
        self.button_settings = ImageButton(
            screen_center_x - button_width, 
            three_fourth_height - settings_button_img.get_height() * 0.3 / 2, 
            settings_button_img, 
            0.9
        ).set_callback(self.on_settings_clicked)
        
        self.button_quit = ImageButton(
            screen_center_x - button_width, 
            three_fourth_height - quit_button_img.get_height() * 0.3 / 2 + button_spacing, 
            quit_button_img, 
            0.9
        ).set_callback(self.on_quit_clicked)
        
        # Add buttons to ui_elements
        self.ui_elements = [
            self.title,
            self.button_play,
            self.button_settings,
            self.button_quit
        ]
        
        # Start menu music
        try:
            # Get the path to the menu music file
            current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            music_path = os.path.normpath(os.path.join(
                current_dir, '..', 'Game', 'assets', 'sounds', 'bgm', 'menu_bgm.mp3'
            ))
            
            # Load and play the music
            pygame.mixer.music.load(music_path)
            pygame.mixer.music.set_volume(0.5)  # Set volume to 50%
            pygame.mixer.music.play(loops=-1)  # Loop indefinitely
        except Exception as e:
            print(f"Could not load menu music: {e}")
        
    def update(self, dt):
        """Update the main menu"""
        super().update(dt)
    
    def draw(self):
        """Draw the main menu"""
        # Draw background
        self.screen.blit(self.main_background, (0, 0))
        
        # Draw UI elements
        super().draw()
        
    def on_play_clicked(self):
        """Handle play button click"""
        from .game_mode_scene import GameModeScene
        self.switch_to_scene(GameModeScene(self.screen))
        
    def on_settings_clicked(self):
        """Handle settings button click"""
        from .settings_scene import SettingsScene
        self.switch_to_scene(SettingsScene(self.screen))
        
    def on_quit_clicked(self):
        """Handle quit button click"""
        pygame.quit()
        sys.exit()
