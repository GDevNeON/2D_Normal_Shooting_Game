"""Utility functions for handling button sounds in the menu system."""
import sys
import os

# Add Game directory to path for sound manager
current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
game_dir = os.path.join(os.path.dirname(current_dir), 'Game')
if game_dir not in sys.path:
    sys.path.append(game_dir)

def play_button_select():
    """Play the button select sound effect.
    
    This function is safe to call even if the sound manager is not available.
    """
    try:
        from Game.managers.sound_manager import SoundManager
        SoundManager.play_button_select()
    except (ImportError, AttributeError):
        pass  # Silently fail if sound manager is not available
