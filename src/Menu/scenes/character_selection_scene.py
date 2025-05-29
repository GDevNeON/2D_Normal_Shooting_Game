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
from ..components.button import ImageButton, Button
from ..utils.asset_loader import AssetLoader
from ..utils.drawing import draw_image, draw_text
from ..utils.font_manager import FontManager
from ..config.constants import WHITE_COLOR

class CharacterSelectionScene(Scene):
    """Scene for selecting player character"""
    def __init__(self, screen, game_mode):
        super().__init__(screen)
        self.assets = AssetLoader()
        self.font_manager = FontManager()
        self.game_mode = game_mode  # 1: normal, 0: endless
        self.character = 1  # 1: male, 0: female
        self.character_names = {1: "MALE KNIGHT", 0: "FEMALE ARCHER"}
        
    def setup(self):
        """Initialize character selection elements"""
        super().setup()
        
        # Load background and character images
        self.background = self.assets.get_image('background_selection')
        self.male_char_img = self.assets.get_image('male_char')
        self.female_char_img = self.assets.get_image('female_char')
        
        # Scale background to fit screen
        self.sub_background = pygame.transform.scale(
            self.background, 
            (int(self.background.get_width() * 0.7), 
             int(self.background.get_height() * 0.7))
        )
        
        # Get screen dimensions
        screen_width = self.screen.get_width()
        screen_height = self.screen.get_height()
        screen_center_x = screen_width // 2
        
        # Create buttons
        back_button_img = self.assets.get_image('back_button')
        select_button_img = self.assets.get_image('select_button')
        arrow_img = self.assets.get_image('arrow')
        
        # Position back button in top-left corner
        self.back_button = ImageButton(20, 20, back_button_img, 0.6).set_callback(self.on_back_clicked)
        
        # Position select button at bottom center
        select_btn_width = int(select_button_img.get_width() * 1.5)
        select_btn_x = screen_center_x - (select_btn_width // 2)
        select_btn_y = screen_height - 120  # Position from bottom with some padding
        self.select_button = ImageButton(
            select_btn_x, 
            select_btn_y, 
            select_button_img, 
            1.5
        ).set_callback(self.on_select_clicked)
        
        # Position arrow buttons on either side of character
        arrow_offset = 200  # Distance from center to arrows
        arrow_y = screen_height // 2  # Vertical center
        
        self.left_arrow = ImageButton(
            screen_center_x - arrow_offset - 50,  # 50 is half arrow width
            arrow_y,
            pygame.transform.rotate(arrow_img, 180), 
            0.8
        ).set_callback(self.on_left_clicked)
        
        self.right_arrow = ImageButton(
            screen_center_x + arrow_offset - 30,  # 30 is half arrow width after scaling
            arrow_y,
            arrow_img, 
            0.8
        ).set_callback(self.on_right_clicked)
        
        # Add buttons to ui_elements
        self.ui_elements = [
            self.back_button,
            self.select_button,
            self.left_arrow,
            self.right_arrow
        ]
        
        # Create character info panel
        panel_width = 500
        panel_height = 140
        panel_x = screen_center_x - (panel_width // 2)
        panel_y = screen_height - 200  # Position above select button
        
        self.info_panel = {
            "rect": pygame.Rect(panel_x, panel_y, panel_width, panel_height),
            "bg_color": (30, 30, 30, 180),
            "border_color": (200, 200, 200)
        }
        
    def update(self, dt):
        """Update the character selection screen"""
        super().update(dt)
    
    def draw(self):
        """Draw the character selection screen"""
        # Get screen dimensions
        screen_width = self.screen.get_width()
        screen_height = self.screen.get_height()
        screen_center_x = screen_width // 2
        
        # Draw background with overlay
        self.screen.blit(self.sub_background, (0, 0))
        overlay = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))  # Semi-transparent black overlay
        self.screen.blit(overlay, (0, 0))
        
        # Draw title with custom font
        title_font = self.font_manager.heading_font()
        draw_text(self.screen, "CHARACTER SELECTION", title_font, WHITE_COLOR, 
                 screen_center_x, 70)
        
        # Draw character images with nicer framing
        character_frame_width = 400
        character_frame_height = 400
        character_frame = pygame.Rect(
            screen_center_x - (character_frame_width // 2),
            (screen_height // 2) - (character_frame_height // 2) - 20,  # Slightly higher than center
            character_frame_width,
            character_frame_height
        )
        pygame.draw.rect(self.screen, (30, 30, 30, 150), character_frame, border_radius=15)
        pygame.draw.rect(self.screen, (200, 200, 200), character_frame, 2, border_radius=15)
        
        # Draw character with glow effect when selected and fit properly in the panel
        if self.character == 1:
            # Calculate scaled image dimensions to fit panel
            char_img = self.male_char_img
            padding = 20  # Padding from panel edge
            max_width = character_frame.width - (padding * 2)
            max_height = character_frame.height - (padding * 2)
            
            # Calculate scale to fit within panel
            width_scale = max_width / char_img.get_width()
            height_scale = max_height / char_img.get_height()
            scale = min(width_scale, height_scale)  # Use smaller scale to ensure it fits
            
            # Draw glow effect
            glow_surf = pygame.Surface((max_width + 20, max_height + 20), pygame.SRCALPHA)
            pygame.draw.ellipse(glow_surf, (100, 100, 255, 50), (0, 0, max_width + 20, max_height + 20))
            self.screen.blit(glow_surf, (character_frame.centerx - (max_width + 20)//2, character_frame.centery - (max_height + 20)//2))
            
            # Draw character centered in the panel
            scaled_width = int(char_img.get_width() * scale)
            scaled_height = int(char_img.get_height() * scale)
            scaled_img = pygame.transform.scale(char_img, (scaled_width, scaled_height))
            
            # Position image centered in the panel
            img_x = character_frame.centerx - scaled_width // 2
            img_y = character_frame.centery - scaled_height // 2
            self.screen.blit(scaled_img, (img_x, img_y))
        else:
            # Calculate scaled image dimensions to fit panel
            char_img = self.female_char_img
            padding = 20  # Padding from panel edge
            max_width = character_frame.width - (padding * 2)
            max_height = character_frame.height - (padding * 2)
            
            # Calculate scale to fit within panel
            width_scale = max_width / char_img.get_width()
            height_scale = max_height / char_img.get_height()
            scale = min(width_scale, height_scale)  # Use smaller scale to ensure it fits
            
            # Draw glow effect
            glow_surf = pygame.Surface((max_width + 20, max_height + 20), pygame.SRCALPHA)
            pygame.draw.ellipse(glow_surf, (255, 100, 100, 50), (0, 0, max_width + 20, max_height + 20))
            self.screen.blit(glow_surf, (character_frame.centerx - (max_width + 20)//2, character_frame.centery - (max_height + 20)//2))
            
            # Draw character centered in the panel
            scaled_width = int(char_img.get_width() * scale)
            scaled_height = int(char_img.get_height() * scale)
            scaled_img = pygame.transform.scale(char_img, (scaled_width, scaled_height))
            
            # Position image centered in the panel
            img_x = character_frame.centerx - scaled_width // 2
            img_y = character_frame.centery - scaled_height // 2
            self.screen.blit(scaled_img, (img_x, img_y))
        
        # Draw info panel
        info_panel_surf = pygame.Surface((self.info_panel["rect"].width, self.info_panel["rect"].height), pygame.SRCALPHA)
        info_panel_surf.fill(self.info_panel["bg_color"])
        pygame.draw.rect(info_panel_surf, self.info_panel["border_color"], 
                        (0, 0, self.info_panel["rect"].width, self.info_panel["rect"].height), 2, border_radius=10)
        self.screen.blit(info_panel_surf, self.info_panel["rect"])
        
        # Draw character info
        char_name = self.character_names[self.character]
        char_font = self.font_manager.subheading_font()
        desc_font = self.font_manager.small_font()
        
        name_y = self.info_panel["rect"].y + 20
        desc_y = name_y + 40
        
        draw_text(self.screen, char_name, char_font, WHITE_COLOR, self.info_panel["rect"].centerx, name_y)
        
        # Display character description based on selected character
        if self.character == 1:
            description = "Strong spreadshooter with high HP"
        else:
            description = "Agile ranged fighter with machine gun"
            
        draw_text(self.screen, description, desc_font, WHITE_COLOR, self.info_panel["rect"].centerx, desc_y)
        
        # Draw UI elements (buttons)
        super().draw()
        
        # Draw navigation hints
        hint_font = self.font_manager.small_font()
        arrow_y = self.left_arrow.rect.centery + 80  # Position below arrows
        draw_text(self.screen, "< Previous", hint_font, WHITE_COLOR, 
                 self.left_arrow.rect.centerx, arrow_y)
        draw_text(self.screen, "Next >", hint_font, WHITE_COLOR, 
                 self.right_arrow.rect.centerx, arrow_y)
        
    def on_back_clicked(self):
        """Handle back button click"""
        from .game_mode_scene import GameModeScene
        self.switch_to_scene(GameModeScene(self.screen))
        
    def on_select_clicked(self):
        """Handle select button click - Start the game"""
        # Import here to avoid circular imports
        from .game_scene import GameScene
        
        # Switch to game scene with selected character and mode
        self.switch_to_scene(GameScene(self.screen, self.character, self.game_mode))
        
    def on_left_clicked(self):
        """Handle left arrow click"""
        self.character = 1  # Male character
        
    def on_right_clicked(self):
        """Handle right arrow click"""
        self.character = 0  # Female character
