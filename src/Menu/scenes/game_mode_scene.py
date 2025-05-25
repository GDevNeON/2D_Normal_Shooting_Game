import pygame
import sys
import os

# Add paths for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
menu_dir = os.path.dirname(current_dir)
sys.path.insert(0, os.path.dirname(menu_dir))  # Add src directory

# Use relative imports
from .base_scene import Scene
from ..components.button import Button, ImageButton
from ..utils.asset_loader import AssetLoader
from ..utils.drawing import draw_image, draw_text
from ..utils.font_manager import FontManager
from ..config.constants import WHITE_COLOR

class GameModeScene(Scene):
    """Scene for selecting game mode and map"""
    def __init__(self, screen):
        super().__init__(screen)
        self.assets = AssetLoader()
        self.font_manager = FontManager()
        
        # Game mode settings
        self.mode = 1  # 1: normal, 0: endless
        self.mode_names = {1: "NORMAL MODE", 0: "ENDLESS MODE"}
        self.mode_descriptions = {
            1: "Complete 5 levels and defeat the final boss",
            0: "Survive as long as possible with increasing difficulty"
        }
        
        # Map settings
        self.current_map = 0  # Index of current selected map
        self.maps = [
            {"name": "GRASSPLAIN", "image": "map", "description": "A grassy plain with dangerous monsters"}
        ]
        
    def setup(self):
        """Initialize game mode selection elements"""
        super().setup()
        
        # Load background
        self.background = self.assets.get_image('background_selection')
        
        # Load map images
        for map_data in self.maps:
            try:
                map_data["image_surface"] = self.assets.get_image(map_data["image"])
            except:
                # If image loading fails, create a placeholder
                map_data["image_surface"] = None
        
        # Scale background to fit screen
        self.background = pygame.transform.scale(
            self.background, 
            (int(self.background.get_width() * 0.7), 
             int(self.background.get_height() * 0.7))
        )
        
        # Calculate screen center
        screen_center_x = self.screen.get_width() // 2
        five_six_height = int(self.screen.get_height() * 0.75)
        
        # Create buttons
        back_button_img = self.assets.get_image('back_button')
        select_button_img = self.assets.get_image('select_button')
        
        # Calculate button dimensions
        button_width_select = select_button_img.get_width() * 0.15
        button_spacing = 110
        
        # Create navigation buttons
        self.back_button = ImageButton(10, 10, back_button_img, 0.6).set_callback(self.on_back_clicked)
        self.select_button = ImageButton(
            (screen_center_x - button_width_select) / 1.15, 
            (five_six_height - back_button_img.get_height() * 0.3 / 1) + button_spacing, 
            select_button_img, 
            1.5
        ).set_callback(self.on_select_clicked)
        
        # Create text buttons for map navigation
        self.prev_button = Button(170, 495, 100, 40, "PREV", self.font_manager.small_font(), 
                               (200, 200, 200), (150, 150, 150), (100, 100, 100))
        self.next_button = Button(170 + 100 + 150, 495, 100, 40, "NEXT", self.font_manager.small_font(),
                               (200, 200, 200), (150, 150, 150), (100, 100, 100))
        
        # Set button callbacks
        self.prev_button.set_callback(self.on_left_clicked)
        self.next_button.set_callback(self.on_right_clicked)
        
        # Add buttons to ui_elements
        self.ui_elements = [
            self.back_button,
            self.select_button,
            self.prev_button,
            self.next_button
        ]
        
        # No info panel needed
        
    def update(self, dt):
        """Update the game mode selection screen"""
        super().update(dt)
    
    def draw(self):
        """Draw the game mode selection screen"""
        # Draw background with overlay
        self.screen.blit(self.background, (0, 0))
        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))  # Semi-transparent black overlay
        self.screen.blit(overlay, (0, 0))
        
        # Draw title with custom font
        title_font = self.font_manager.heading_font()
        screen_center_x = self.screen.get_width() // 2
        draw_text(self.screen, "GAME MODE SELECTION", title_font, WHITE_COLOR, 
                 screen_center_x, 70)
        
        # Draw map selection section (left side)
        map_section = pygame.Rect(100, 160, 500, 400)  # Increased height
        pygame.draw.rect(self.screen, (30, 30, 30, 150), map_section, border_radius=15)
        pygame.draw.rect(self.screen, (200, 200, 200), map_section, 2, border_radius=15)
        
        # Draw map section title
        section_title_font = self.font_manager.subheading_font()
        draw_text(self.screen, "SELECT MAP", section_title_font, WHITE_COLOR, 
                 map_section.centerx, map_section.y + 20)
        
        # Draw current map preview
        current_map = self.maps[self.current_map]
        map_preview_rect = pygame.Rect(map_section.centerx - 100, map_section.y + 60, 200, 120)
        pygame.draw.rect(self.screen, (20, 20, 20), map_preview_rect, border_radius=10)
        
        # Draw map preview or placeholder
        preview_surface = pygame.Surface((map_preview_rect.width - 10, map_preview_rect.height - 10))
        preview_surface.fill((40, 40, 40))  # Dark background for the preview
        
        if current_map.get("image_surface"):
            # If we have a map image, scale and draw it
            scaled_map = pygame.transform.scale(current_map["image_surface"], 
                                             (map_preview_rect.width - 10, map_preview_rect.height - 10))
            preview_surface.blit(scaled_map, (0, 0))
        
        # Draw the preview surface onto the screen
        self.screen.blit(preview_surface, (map_preview_rect.x + 5, map_preview_rect.y + 5))
        
        # Draw map name and description
        map_name_font = self.font_manager.normal_font()
        map_desc_font = self.font_manager.small_font()
        draw_text(self.screen, current_map["name"], map_name_font, WHITE_COLOR, 
                 map_section.centerx, map_section.y + 200)
        draw_text(self.screen, current_map["description"], map_desc_font, WHITE_COLOR, 
                 map_section.centerx, map_section.y + 230, wrap_width=400)
        
        # Position and draw navigation buttons at the bottom of the map panel
        btn_y = map_section.bottom - 70
        btn_width = 120
        btn_height = 40
        btn_spacing = 20
        
        # Calculate button positions
        prev_btn_x = map_section.centerx - btn_width - btn_spacing//2 - 5
        next_btn_x = map_section.centerx + btn_spacing//2 + 5
        
        # Draw previous button if not on first map
        if self.current_map > 0:
            # Highlight if hovered
            if self.prev_button.is_hovered():
                pygame.draw.rect(self.screen, (100, 150, 255, 100), 
                               (prev_btn_x - 5, btn_y - 5, 
                                btn_width + 10, btn_height + 10), 
                               border_radius=8)
            
            self.prev_button.x = prev_btn_x
            self.prev_button.y = btn_y
            self.prev_button.draw(self.screen)
        
        # Draw next button if not on last map
        if self.current_map < len(self.maps) - 1:
            # Highlight if hovered
            if self.next_button.is_hovered():
                pygame.draw.rect(self.screen, (100, 150, 255, 100), 
                               (next_btn_x - 5, btn_y - 5, 
                                btn_width + 10, btn_height + 10), 
                               border_radius=8)
            
            self.next_button.x = next_btn_x
            self.next_button.y = btn_y
            self.next_button.draw(self.screen)
        
        # Draw game mode selection section (right side)
        mode_section = pygame.Rect(660, 160, 500, 400)  # Increased height
        pygame.draw.rect(self.screen, (30, 30, 30, 150), mode_section, border_radius=15)
        pygame.draw.rect(self.screen, (200, 200, 200), mode_section, 2, border_radius=15)
        
        # Draw mode section title
        draw_text(self.screen, "SELECT GAME MODE", section_title_font, WHITE_COLOR, 
                 mode_section.centerx, mode_section.y + 20)
        
        # Draw mode selection
        mode_icon_y = mode_section.y + 80
        mode_desc_y = mode_icon_y + 40
        
        # Draw mode description
        current_mode_desc = self.mode_descriptions[self.mode]
        draw_text(self.screen, current_mode_desc, map_desc_font, WHITE_COLOR, 
                 mode_section.centerx, mode_desc_y, wrap_width=400)
        
        # Draw mode selection buttons
        mode_btn_width = 180
        mode_btn_height = 40
        normal_btn_x = mode_section.centerx - mode_btn_width - 20
        endless_btn_x = mode_section.centerx + 20
        
        # Highlight selected mode
        if self.mode == 1:
            pygame.draw.rect(self.screen, (100, 200, 100, 100), 
                           (normal_btn_x - 5, mode_section.bottom - 70, 
                            mode_btn_width + 10, mode_btn_height + 10), 
                           border_radius=8)
        else:
            pygame.draw.rect(self.screen, (200, 100, 100, 100), 
                           (endless_btn_x - 5, mode_section.bottom - 70, 
                            mode_btn_width + 10, mode_btn_height + 10), 
                           border_radius=8)
        
        # Draw mode buttons
        self.normal_btn = Button(normal_btn_x, mode_section.bottom - 65, mode_btn_width, mode_btn_height, 
                               "NORMAL", self.font_manager.normal_font(), 
                               hover_color=(100, 200, 100)).set_callback(self.on_normal_clicked)
        self.endless_btn = Button(endless_btn_x, mode_section.bottom - 65, mode_btn_width, mode_btn_height, 
                                "ENDLESS", self.font_manager.normal_font(), 
                                hover_color=(200, 100, 100)).set_callback(self.on_endless_clicked)
        
        # Add mode buttons to UI elements
        self.ui_elements.extend([self.normal_btn, self.endless_btn])
        
        # No info panel at the bottom
        
        # Draw UI elements (buttons)
        super().draw()
        
        # Navigation hints are now inside the map panel
        
    def on_back_clicked(self):
        """Handle back button click"""
        from .main_menu_scene import MainMenuScene
        self.switch_to_scene(MainMenuScene(self.screen))
        
    def on_select_clicked(self):
        """Handle select button click"""
        from .character_selection_scene import CharacterSelectionScene
        self.switch_to_scene(CharacterSelectionScene(self.screen, self.mode))
        
    def on_left_clicked(self):
        """Handle left arrow click for map navigation"""
        if self.current_map > 0:
            self.current_map -= 1
        
    def on_right_clicked(self):
        """Handle right arrow click for map navigation"""
        if self.current_map < len(self.maps) - 1:
            self.current_map += 1
            
    def on_normal_clicked(self):
        """Handle normal mode button click"""
        self.mode = 1
        
    def on_endless_clicked(self):
        """Handle endless mode button click"""
        self.mode = 0
