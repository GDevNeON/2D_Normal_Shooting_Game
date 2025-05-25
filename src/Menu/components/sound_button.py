"""Button components with sound effects."""
import pygame
from .button import Button, ImageButton
from ..utils.sound_utils import play_button_select

class SoundButton(Button):
    """Button with sound effects on click."""
    def handle_event(self, event):
        """Handle pygame events with sound feedback."""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.is_hovered and self.callback:
                play_button_select()
                self.callback()
                return True
        return False

class SoundImageButton(ImageButton):
    """Image button with sound effects on click."""
    def handle_event(self, event):
        """Handle pygame events with sound feedback."""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.is_hovered and self.callback:
                play_button_select()
                self.callback()
                return True
        return False
