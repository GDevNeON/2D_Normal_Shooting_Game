import pygame
import os
import sys

# Add paths for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
menu_dir = os.path.dirname(current_dir)
sys.path.insert(0, os.path.dirname(menu_dir))  # Add src directory
sys.path.insert(0, os.path.join(os.path.dirname(menu_dir), 'Game'))  # Add Game directory

# Use relative imports
from ..config.constants import *

class AssetLoader:
    """
    Handles loading and caching of game assets like images and sounds
    """
    def __init__(self):
        self._images = {}
        self._sounds = {}
        self._load_assets()
        
    def _load_assets(self):
        """Load all assets and store them in cache dictionaries"""
        # Load all images
        self._images = {
            'title': pygame.image.load(PATH_TO_TITLE).convert_alpha(),
            'background': pygame.image.load(PATH_TO_BACKGROUND).convert_alpha(),
            'background_selection': pygame.image.load(PATH_TO_BACKGROUND_SELECTION_MENU).convert_alpha(),
            'play_button': pygame.image.load(PATH_TO_START_BUTTON).convert_alpha(),
            'setting_button': pygame.image.load(PATH_TO_SETTING_BUTTON).convert_alpha(),
            'quit_button': pygame.image.load(PATH_TO_QUIT_BUTTON).convert_alpha(),
            'setting_menu_button': pygame.image.load(PATH_TO_VIDEO_SETTING_BUTTON).convert_alpha(),
            'audio_button': pygame.image.load(PATH_TO_AUDIO_BUTTON).convert_alpha(),
            'close_button': pygame.image.load(PATH_TO_CLOSE_BUTTON).convert_alpha(),
            'back_button': pygame.image.load(PATH_TO_BACK_BUTTON).convert_alpha(),
            'select_button': pygame.image.load(PATH_TO_SELECT_BUTTON).convert_alpha(),
            'arrow': pygame.image.load(PATH_TO_ARROW).convert_alpha(),
            'map': pygame.image.load(PATH_TO_MAP).convert_alpha(),
            'endless_mode': pygame.image.load(PATH_TO_GAME_MODE_EL).convert_alpha(),
            'normal_mode': pygame.image.load(PATH_TO_GAME_MODE_NM).convert_alpha(),
            'male_char': pygame.image.load(PATH_TO_MALE_CHAR).convert_alpha(),
            'female_char': pygame.image.load(PATH_TO_FEMALE_CHAR).convert_alpha(),
            'game_over_title': pygame.image.load(PATH_TO_GAME_OVER_TITLE).convert_alpha(),
            'try_again_button': pygame.image.load(PATH_TO_TRY_AGAIN_BUTTON).convert_alpha(),
        }
        
        # Load all sounds
        try:
            # Get the directory of the current file
            current_dir = os.path.dirname(os.path.abspath(__file__))
            # Navigate to the menu bgm file
            sound_path = os.path.normpath(os.path.join(
                current_dir, '..', '..', 'Game', 'assets', 'sounds', 'bgm', 'menu_bgm.mp3'
            ))
            
            # Initialize the mixer if it's not already initialized
            if not pygame.mixer.get_init():
                pygame.mixer.init()
                
            # Load the sound
            menu_sound = pygame.mixer.Sound(sound_path)
            self._sounds = {
                'menu': menu_sound
            }
        except Exception as e:
            print(f"Warning: Could not load sound files: {e}")
        
    def get_image(self, key):
        """Get an image by its key"""
        if key in self._images:
            return self._images[key]
        else:
            raise KeyError(f"Image '{key}' not found in asset loader")
            
    def get_sound(self, key):
        """Get a sound by its key"""
        if key in self._sounds:
            return self._sounds[key]
        else:
            raise KeyError(f"Sound '{key}' not found in asset loader")
