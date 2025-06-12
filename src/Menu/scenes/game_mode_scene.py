import pygame
import sys
import os
import importlib

# Add paths for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
menu_dir = os.path.dirname(current_dir)
sys.path.insert(0, os.path.dirname(menu_dir))  # Add src directory
sys.path.insert(0, os.path.join(os.path.dirname(menu_dir), 'Game'))  # Add Game directory

# Import components
from ..components.scrollable_panel import ScrollablePanel

# Try to import game mode configuration
try:
    from Game.core.gamemodes.config import DEFAULT_GAME_MODES, GAME_MODE_NORMAL, GAME_MODE_ENDLESS, GAME_MODE_CUSTOM
    HAS_GAME_MODES = True
except ImportError:
    print("[WARNING] Could not import game mode configuration")
    DEFAULT_GAME_MODES = []
    GAME_MODE_NORMAL = 1
    GAME_MODE_ENDLESS = 0
    GAME_MODE_CUSTOM = 2
    HAS_GAME_MODES = False

# Use relative imports
from .base_scene import Scene
from ..components.button import Button, ImageButton
from ..utils.asset_loader import AssetLoader
from ..utils.drawing import draw_image, draw_text
from ..managers.font_manager import FontManager
from ..config.constants import WHITE_COLOR

class GameModeScene(Scene):
    """Scene for selecting game mode and map"""
    def __init__(self, screen, manager=None):
        super().__init__(screen)
        self.manager = manager  # Store the scene manager
        self.assets = AssetLoader()
        self.font_manager = FontManager()
        
        # Game mode settings
        self.mode = 1  # 1: normal, 0: endless, 2: custom
        self.mode_names = {
            1: "NORMAL MODE",
            0: "ENDLESS MODE",
            2: "CUSTOM MODE"
        }
        self.mode_descriptions = {
            1: "Survive for 5 minutes and defeat the final boss",
            0: "Survive as long as possible with increasing difficulty",
            2: "Customize your own game mode with special rules"
        }
        
        # Initialize custom modes from configuration
        self.custom_modes = []
        # Define available game mode images with their asset keys
        game_mode_images = {
            "elite_madness": "custom_elite",
            "tiny_speed_demon": "custom_tiny",
            "double_bozos": "custom_bozos"
        }
        
        for mode_config in DEFAULT_GAME_MODES:
            try:
                # Use the corresponding image based on mode ID, fallback to default if not found
                mode_id = mode_config["id"].lower()
                if mode_id in game_mode_images:
                    try:
                        # Try to load the image
                        image_name = game_mode_images[mode_id]
                        self.assets.get_image(image_name)  # Test if image exists
                    except:
                        print(f"[WARNING] Image for mode {mode_id} not found, using default")
                        image_name = "default_mode"
                else:
                    print(f"[WARNING] No image mapping for mode {mode_id}, using default")
                    image_name = "default_mode"
                    
                self.custom_modes.append({
                    "id": mode_config["id"],
                    "name": mode_config["name"],
                    "image": image_name,
                    "description": mode_config["description"],
                    "rules": mode_config.get("rules", {})
                })
                print(f"[DEBUG] Loaded custom mode: {mode_config['name']} with image: {image_name}")
            except Exception as e:
                print(f"[ERROR] Failed to load game mode {mode_config.get('name', 'unknown')}: {e}")
        self.selected_custom_mode = 0
        self.show_custom_panel = False
        
        # Map settings
        self.current_map = 0  # Index of current selected map
        self.maps = [
            {"name": "GRASSPLAIN", "image": "map", "description": "A grassy plain with dangerous monsters"}
        ]
        
        # Initialize scrollable panel for rules
        self.rules_panel = None
        self.rules_content = None
        
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
        
        # Draw navigation buttons
        self.back_button = ImageButton(10, 10, back_button_img, 0.6).set_callback(self.on_back_clicked)
        self.select_button = ImageButton(
            (screen_center_x - button_width_select) / 1.15, 
            (five_six_height - back_button_img.get_height() * 0.3 / 1) + button_spacing, 
            select_button_img, 
            1.5
        ).set_callback(self.on_select_clicked)
        
        # Create text buttons for map navigation
        # Positioned at the same height as mode selection buttons
        button_y = 580  # Default position, will be updated in draw()
        self.prev_button = Button(70, button_y, 150, 40, "PREV", self.font_manager.small_font(), 
                               (200, 200, 200), (150, 150, 150), (100, 100, 100))
        self.next_button = Button(70 + 100 + 150, button_y, 150, 40, "NEXT", self.font_manager.small_font(),
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
        
        # Define sections first
        map_section = pygame.Rect(50, 140, 450, 500)  # Reduced width from 580 to 450
        mode_section = pygame.Rect(520, 140, 740, 500)  # Game mode section
        
        # Draw map selection section (left side) - narrower width
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
        
        # Position and draw navigation buttons centered in map section
        btn_y = mode_section.bottom - 70  # Same y position as mode buttons
        btn_width = 120
        btn_height = 40
        btn_spacing = 20
        
        # Calculate button positions - center them in the map section
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
        
        # Draw game mode selection section (right side) - wider width
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
        
        # Draw mode selection buttons - adjusted for wider panel
        mode_btn_width = 180  # Slightly wider buttons
        mode_btn_height = 40
        total_btn_width = mode_btn_width * 3 + 80  # 3 buttons with 40px spacing
        start_x = mode_section.x + 40  # Align buttons to the left with some padding
        
        # Draw mode buttons
        self.normal_btn = Button(
            start_x, mode_section.bottom - 65, mode_btn_width, mode_btn_height,
            "NORMAL", self.font_manager.normal_font(),
            hover_color=(100, 200, 100) if self.mode != 1 else (70, 170, 70)
        ).set_callback(self.on_normal_clicked)
        
        self.endless_btn = Button(
            start_x + mode_btn_width + 20, mode_section.bottom - 65, mode_btn_width, mode_btn_height,
            "ENDLESS", self.font_manager.normal_font(),
            hover_color=(200, 100, 100) if self.mode != 0 else (170, 70, 70)
        ).set_callback(self.on_endless_clicked)
        
        self.custom_btn = Button(
            start_x + (mode_btn_width + 20) * 2, mode_section.bottom - 65, mode_btn_width, mode_btn_height,
            "CUSTOM", self.font_manager.normal_font(),
            hover_color=(100, 100, 200) if self.mode != 2 else (70, 70, 170)
        ).set_callback(self.on_custom_clicked)
        
        # Highlight selected mode
        if self.mode == 1:
            pygame.draw.rect(self.screen, (100, 200, 100, 100),
                           (start_x - 5, mode_section.bottom - 70,
                            mode_btn_width + 10, mode_btn_height + 10),
                           border_radius=8)
        elif self.mode == 0:
            pygame.draw.rect(self.screen, (200, 100, 100, 100),
                           (start_x + mode_btn_width + 15, mode_section.bottom - 70,
                            mode_btn_width + 10, mode_btn_height + 10),
                           border_radius=8)
        else:  # Custom mode
            pygame.draw.rect(self.screen, (100, 100, 200, 100),
                           (start_x + (mode_btn_width + 20) * 2 - 5, mode_section.bottom - 70,
                            mode_btn_width + 10, mode_btn_height + 10),
                           border_radius=8)
        
        # Add mode buttons to UI elements
        self.ui_elements.extend([self.normal_btn, self.endless_btn, self.custom_btn])
        
        # Draw custom mode panel if custom mode is selected
        if self.mode == 2 and self.show_custom_panel:
            self.draw_custom_panel(mode_section)
        
        # No info panel at the bottom
        
        # Draw UI elements (buttons)
        super().draw()
        
        # Navigation hints are now inside the map panel
        
    def on_back_clicked(self):
        """Handle back button click"""
        from .main_menu_scene import MainMenuScene
        self.switch_to_scene(MainMenuScene(self.screen, self.manager))
        
    def on_select_clicked(self):
        """Handle select button click"""
        from .character_selection_scene import CharacterSelectionScene
        
        if self.show_custom_panel and self.selected_custom_mode is not None:
            # For custom modes, pass the mode ID to character selection
            selected_mode = self.custom_modes[self.selected_custom_mode]
            custom_mode_id = selected_mode["id"]
            print(f"[DEBUG] Selected custom mode: {custom_mode_id} ({selected_mode['name']})")
            
            # Create character selection scene with custom mode
            char_scene = CharacterSelectionScene(
                screen=self.screen, 
                game_mode=GAME_MODE_CUSTOM,  # Use constant for custom mode
                custom_mode=custom_mode_id,  # Pass the custom mode ID
                manager=self.manager
            )
            self.switch_to_scene(char_scene)
        else:
            # For normal/endless modes, just pass the mode
            self.switch_to_scene(CharacterSelectionScene(
                screen=self.screen, 
                game_mode=self.mode, 
                custom_mode=None,  # No custom mode for normal/endless
                manager=self.manager
            ))
        
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
        self.show_custom_panel = False
        self.selected_custom_mode = 0  # Reset to default instead of None
        
    def on_endless_clicked(self):
        """Handle endless mode button click"""
        self.mode = 0
        self.show_custom_panel = False
        self.selected_custom_mode = 0  # Reset to default instead of None
        
    def on_custom_clicked(self):
        """Handle custom mode button click"""
        self.mode = 2
        self.show_custom_panel = True
        
    def handle_event(self, event):
        """Handle pygame events"""
        # Handle events for the rules panel if it's visible
        if hasattr(self, 'show_custom_panel') and self.show_custom_panel and self.rules_panel:
            # Forward all mouse events to the panel
            if event.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION, pygame.MOUSEWHEEL):
                if self.rules_panel.handle_event(event):
                    return True
                # Forward mouse wheel events for scrolling
                elif event.type == pygame.MOUSEWHEEL:
                    if self.rules_panel.rect.collidepoint(pygame.mouse.get_pos()):
                        self.rules_panel.scroll(event.y * 20)  # Adjust scroll speed
                        return True
                
        # Let the base class handle other events
        return super().handle_event(event)
        
    def draw_custom_panel(self, parent_rect):
        """Draw the custom mode selection panel"""
        # Create panel (larger custom mode panel)
        panel_width = parent_rect.width - 20  # Use more of the parent width
        panel_height = parent_rect.height - 100  # Use more of the parent height
        panel_x = parent_rect.x + 10  # Centered with less margin
        panel_y = parent_rect.y + 30  # Slightly higher up
        
        # Draw panel background
        panel_rect = pygame.Rect(panel_x, panel_y, panel_width, panel_height)
        pygame.draw.rect(self.screen, (40, 40, 60, 200), panel_rect, border_radius=10)
        pygame.draw.rect(self.screen, (100, 100, 200), panel_rect, 2, border_radius=10)
        
        # Draw title
        title_font = self.font_manager.subheading_font()
        draw_text(self.screen, "CUSTOM GAME MODES", title_font, WHITE_COLOR,
                 panel_rect.centerx, panel_rect.y + 20)
        
        # Draw dropdown list (left side) - slightly narrower to fit better
        list_width = panel_width * 0.4  # Slightly reduced from 0.45 to 0.4
        list_rect = pygame.Rect(panel_rect.x + 20, panel_rect.y + 60, list_width, panel_height - 100)
        pygame.draw.rect(self.screen, (30, 30, 50), list_rect, border_radius=5)
        pygame.draw.rect(self.screen, (100, 100, 200), list_rect, 1, border_radius=5)
        
        # Draw mode list
        item_height = 40
        max_visible = (panel_height - 100) // item_height
        
        # Ensure we have a valid selected_custom_mode
        if not hasattr(self, 'selected_custom_mode') or self.selected_custom_mode is None or self.selected_custom_mode >= len(self.custom_modes):
            self.selected_custom_mode = 0
            
        start_idx = max(0, min(self.selected_custom_mode - max_visible // 2, 
                             len(self.custom_modes) - max_visible))
        
        for i in range(min(max_visible, len(self.custom_modes))):
            idx = start_idx + i
            if idx >= len(self.custom_modes):
                break
                
            item_rect = pygame.Rect(list_rect.x + 2, list_rect.y + 2 + i * item_height, 
                                 list_rect.width - 4, item_height - 2)
            
            # Highlight selected item
            if idx == self.selected_custom_mode:
                pygame.draw.rect(self.screen, (80, 80, 120), item_rect, border_radius=3)
            
            # Draw mode name
            draw_text(self.screen, self.custom_modes[idx]["name"], 
                     self.font_manager.small_font(), WHITE_COLOR,
                     item_rect.x + 10, item_rect.centery, align="left")
            
            # Handle clicks on mode items
            if item_rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                self.selected_custom_mode = idx
        
        # Draw mode details (right side)
        details_x = list_rect.right + 20
        details_width = panel_rect.right - details_x - 20
        
        # Draw mode name
        current_mode = self.custom_modes[self.selected_custom_mode]
        draw_text(self.screen, current_mode["name"], 
                 self.font_manager.subheading_font(), WHITE_COLOR,
                 details_x + details_width//2, panel_rect.y + 60)
        
        # Draw mode image (larger preview)
        try:
            mode_img = self.assets.get_image(current_mode["image"])
            img_rect = pygame.Rect(details_x, panel_rect.y + 90, 150, 150)  # Larger image
            pygame.draw.rect(self.screen, (20, 20, 40), img_rect, border_radius=5)
            scaled_img = pygame.transform.scale(mode_img, (img_rect.width-4, img_rect.height-4))
            self.screen.blit(scaled_img, (img_rect.x + 2, img_rect.y + 2))
        except:
            # Draw placeholder if image not found
            img_rect = pygame.Rect(details_x, panel_rect.y + 90, 150, 150)  # Larger placeholder
            pygame.draw.rect(self.screen, (20, 20, 40), img_rect, border_radius=5)
            draw_text(self.screen, "PREVIEW", self.font_manager.normal_font(), 
                     (100, 100, 100), img_rect.centerx, img_rect.centery)
        
        # Draw mode description (position adjusted for larger image)
        desc_rect = pygame.Rect(details_x + 160, panel_rect.y + 90, 
                              details_width - 140, 150)  # More height for description
        draw_text(self.screen, current_mode["description"], 
                 self.font_manager.small_font(), (200, 200, 200),
                 desc_rect.x, desc_rect.y, wrap_width=desc_rect.width, align="left")
        
        # Draw rules section (more space for rules)
        rules_y = panel_rect.y + 250  # Lower position for rules
        rules_title_rect = pygame.Rect(details_x, rules_y, details_width, 30)
        pygame.draw.rect(self.screen, (30, 30, 50, 100), rules_title_rect, border_radius=3)
        draw_text(self.screen, "RULES:", self.font_manager.normal_font(bold=True), 
                 (200, 200, 255), details_x + 10, rules_y + 5, align="left")
        
        # Prepare rules text with better formatting and line breaks
        rules_text = []
        for rule, value in current_mode["rules"].items():
            rule_name = rule.replace('_', ' ').title()
            # Only add 'x' suffix for multiplier values
            suffix = 'x' if 'multiplier' in rule.lower() or 'scale' in rule.lower() or 'factor' in rule.lower() else ''
            rules_text.append(f"• {rule_name}: {value}{suffix}")
        
        # Only (re)build the scrollable content surface when the rules change or when the panel is first created
        if self.rules_panel is None or self.rules_content != rules_text:
            self.rules_content = list(rules_text)  # cache current rules text so we know when it changes
            
            # Create a surface for the rules content
            font = self.font_manager.small_font()
            line_height = font.get_linesize() + 5
            content_height = len(rules_text) * line_height * 2  # Estimate height with some padding
            content_surface = pygame.Surface((details_width - 20, content_height), pygame.SRCALPHA)
            
            # Draw rules on the content surface
            y_offset = 0
            for rule_text in rules_text:
                # Split long lines if needed
                words = rule_text.split()
                lines = []
                current_line = []
                
                for word in words:
                    test_line = ' '.join(current_line + [word])
                    if font.size(test_line)[0] <= (details_width - 50):  # 50px padding for scrollbar and margins
                        current_line.append(word)
                    else:
                        lines.append(' '.join(current_line))
                        current_line = [word]
                if current_line:
                    lines.append(' '.join(current_line))
                
                # Draw each line of the rule
                for line in lines:
                    text_surface = font.render(line, True, (220, 220, 220))
                    content_surface.blit(text_surface, (0, y_offset))
                    y_offset += line_height
                # Extra space after each rule
                y_offset += 5
            
            # Update the scrollable panel with the new content (this resets scroll_y)
            if self.rules_panel is None:
                self.rules_panel = ScrollablePanel(
                    x=details_x,
                    y=rules_y + 35,
                    width=details_width,
                    height=panel_rect.bottom - (rules_y + 40),
                    background_color=(20, 20, 40, 150),
                    scroll_bar_color=(100, 100, 100, 200),
                    scroll_bar_hover_color=(120, 120, 120, 200),
                    scroll_bar_width=10,
                    padding=10
                )
            self.rules_panel.update_content(content_surface)
        
        # Draw the scrollable panel
        self.rules_panel.draw(self.screen)
        
        # Draw scroll indicators if needed
        if len(self.custom_modes) > max_visible:
            if start_idx > 0:
                # Draw up arrow
                pygame.draw.polygon(self.screen, (200, 200, 200), [
                    (list_rect.centerx, list_rect.y - 5),
                    (list_rect.centerx - 5, list_rect.y + 5),
                    (list_rect.centerx + 5, list_rect.y + 5)
                ])
            
            if start_idx + max_visible < len(self.custom_modes):
                # Draw down arrow
                pygame.draw.polygon(self.screen, (200, 200, 200), [
                    (list_rect.centerx, list_rect.bottom + 5),
                    (list_rect.centerx - 5, list_rect.bottom - 5),
                    (list_rect.centerx + 5, list_rect.bottom - 5)
                ])
