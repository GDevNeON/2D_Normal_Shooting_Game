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
from ..components.scrollable_panel import ScrollablePanel
from ..utils.asset_loader import AssetLoader
from ..utils.drawing import draw_text, draw_image
from ..managers.font_manager import FontManager
from ..config.constants import WHITE_COLOR, BLACK_COLOR
from Game.managers.sound_manager import SoundManager, select_button_sfx

class SettingsScene(Scene):
    """Scene for game settings (video, audio, and credits)"""
    def __init__(self, screen):
        super().__init__(screen)
        self.assets = AssetLoader()
        self.font_manager = FontManager()
        self.current_tab = "video"  # Start with video settings open
        
        # Initialize video settings
        self.resolution = (1920, 1080)  # Default resolution
        self.is_fullscreen = False  # Default to windowed mode
        self.original_size = screen.get_size()  # Store the original window size
        
    def setup(self):
        """Initialize settings elements"""
        super().setup()
        
        # Load background
        self.background = self.assets.get_image('background')
        
        # Scale background to fit screen
        self.main_background = pygame.transform.scale(
            self.background, 
            (int(self.background.get_width() * 0.7115), 
             int(self.background.get_height() * 0.7165))
        )
        
        # Load button images
        setting_menu_img = self.assets.get_image('setting_menu_button')
        audio_button_img = self.assets.get_image('audio_button')
        close_button_img = self.assets.get_image('back_button')  # Using xbutton for close
        
        # Get screen dimensions
        screen_width = self.screen.get_width()
        screen_height = self.screen.get_height()
        screen_center_x = screen_width // 2
        
        # Create menu buttons with better spacing
        tab_button_y = 140
        button_spacing = 120  # Space between tab buttons
        
        # Create tab buttons with consistent style
        normal_font = self.font_manager.normal_font()
        tab_btn_width = 150
        tab_btn_height = 40
        
        # Position tab buttons with better spacing
        tab_btn_spacing = 180  # Increased spacing between tab buttons
        
        # Create all tab buttons with same style
        self.howto_button = Button(
            screen_center_x - tab_btn_spacing * 2, 
            tab_button_y, 
            tab_btn_width, 
            tab_btn_height, 
            "HOW-TO", 
            normal_font, 
            hover_color=(100, 100, 200)
        ).set_callback(self.on_howto_clicked)
        
        self.video_settings_button = Button(
            screen_center_x - tab_btn_spacing, 
            tab_button_y, 
            tab_btn_width, 
            tab_btn_height, 
            "VIDEO", 
            normal_font, 
            hover_color=(100, 100, 200)
        ).set_callback(self.on_video_settings_clicked)
        
        self.audio_settings_button = Button(
            screen_center_x, 
            tab_button_y, 
            tab_btn_width, 
            tab_btn_height, 
            "AUDIO", 
            normal_font, 
            hover_color=(100, 100, 200)
        ).set_callback(self.on_audio_settings_clicked)
        
        self.credits_button = Button(
            screen_center_x + tab_btn_spacing, 
            tab_button_y, 
            tab_btn_width, 
            tab_btn_height, 
            "CREDITS", 
            normal_font, 
            hover_color=(100, 100, 200)
        ).set_callback(self.on_credits_clicked)
        
        # Position close button at top-left corner
        close_btn_x = 30
        close_btn_y = 30
        self.close_button = ImageButton(
            close_btn_x,
            close_btn_y,
            close_button_img,
            0.6  # Scale down the xbutton to be smaller
        ).set_callback(self.on_close_clicked)
        
        # Create video settings buttons with custom font
        normal_font = self.font_manager.normal_font()
        button_width = 200
        button_height = 40
        
        # Video settings - centered with more vertical space
        col_x = screen_center_x - button_width // 2
        row1_y = 260  # Increased vertical spacing
        row2_y = 340  # Increased vertical spacing
        
        # Display mode buttons - centered
        self.fullscreen_btn = Button(col_x, row1_y, button_width, button_height, "Fullscreen", normal_font, 
                                    hover_color=(80, 120, 200)).set_callback(self.on_fullscreen_clicked)
        self.windowed_btn = Button(col_x, row2_y, button_width, button_height, "Windowed", normal_font, 
                                  hover_color=(80, 120, 200)).set_callback(self.on_windowed_clicked)
        
        # Create audio settings buttons
        # Volume control buttons with more spacing
        vol_button_width = 60
        vol_button_height = 40
        button_spacing = 100  # Increased spacing between volume controls
        
        # Calculate positions for audio controls with better centering
        audio_controls_x = screen_center_x - (vol_button_width + button_spacing // 2)
        
        # Adjust audio control positions for better spacing
        row1_y = 260  # Increased vertical spacing
        row2_y = 340  # Increased vertical spacing
        
        # Music volume controls
        self.music_vol_down = Button(audio_controls_x, row1_y, vol_button_width, vol_button_height, "-", normal_font, 
                                   hover_color=(200, 80, 80)).set_callback(self.on_music_vol_down)
        self.music_vol_up = Button(audio_controls_x + vol_button_width + button_spacing, row1_y, 
                                 vol_button_width, vol_button_height, "+", normal_font, 
                                 hover_color=(80, 200, 80)).set_callback(self.on_music_vol_up)
        
        # SFX volume controls
        self.sfx_vol_down = Button(audio_controls_x, row2_y, vol_button_width, vol_button_height, "-", normal_font, 
                                 hover_color=(200, 80, 80)).set_callback(self.on_sfx_vol_down)
        self.sfx_vol_up = Button(audio_controls_x + vol_button_width + button_spacing, row2_y, 
                               vol_button_width, vol_button_height, "+", normal_font, 
                               hover_color=(80, 200, 80)).set_callback(self.on_sfx_vol_up)
        
        # Add common UI elements
        self.common_ui_elements = [
            self.howto_button,
            self.video_settings_button,
            self.audio_settings_button,
            self.credits_button,
            self.close_button
        ]
        
        # Credits information with more spacing
        self.credits_info = [
            {"title": "GAME DEVELOPMENT", "content": [
                "Lead Developer: Bui Bao Long (NeON)",
                "Game: Bui Bao Long. Nguyen Dinh Nam Khuong",
                "Menu: Wundsurf's Cascade, Dao Duy Hung",
                "Art Design: Doan Hoang Long (twitter.com/ryu_hoang)"
            ]},
            {"title": "AUDIO", "content": [
                "Menu Background Music: Sky Force Reloaded",
                "Game Background Music: Arknights OST Vector Breakthrough",
                "SFX: Pixabay",
            ]},
            {"title": "SPECIAL THANKS", "content": [
                "Thanks to all playtesters and all who supported this project"
            ]}
        ]
        
        # Initialize settings elements
        self.update_ui_elements()
        
        # Import SoundManager to initialize volumes
        from Game.managers.sound_manager import SoundManager
        
        # Settings state
        self.resolution = (1920, 1080)
        self.is_fullscreen = False
        
        # How-to instructions
        self.how_to_instructions = [
            {"title": "GAME CONTROLS", "content": [
                "Move: WASD",
                "Use skill: Q",
                "Pause: P",
                "Exit game: Esc",
                "Move your mouse to direct your character to shoot"
            ]},
            {"title": "GAME OBJECTIVES", "content": [
                "Survive waves of enemies",
                "Collect power-ups to enhance your abilities",
                "Defeat the boss to complete each level",
                "Achieve the highest score possible"
            ]},
            {"title": "TIPS", "content": [
                "Keep moving to avoid enemy fire",
                "Conserve your special ability for tough situations",
                "Prioritize collecting health, EXP",
                "Focus fire on one enemy at a time"
            ]}
        ]
        
        # Initialize scrollable panel for how-to
        self.howto_panel = None
        self.setup_howto_panel()
        
    def setup_howto_panel(self):
        """Initialize the scrollable panel for how-to content"""
        try:
            screen_width = self.screen.get_width()
            screen_height = self.screen.get_height()
            
            # Create scrollable panel for how-to content
            panel_width = screen_width - 200
            panel_height = 450  # Same as credits height
            panel_x = 100
            panel_y = 260
            
            # Create the panel with a visible background for debugging
            self.howto_panel = ScrollablePanel(
                panel_x, panel_y, 
                panel_width, panel_height,
                background_color=(30, 30, 50, 200)  # Semi-transparent dark blue
            )
            
            # Create a surface for the how-to content
            content_font = self.font_manager.small_font()
            title_font = self.font_manager.normal_font()
            
            # Calculate total height needed for content
            section_spacing = 30
            line_spacing = 30
            total_height = 0
            
            # First pass: calculate total height
            for section in self.how_to_instructions:
                total_height += section_spacing  # Section title
                total_height += len(section["content"]) * line_spacing  # Section content
                total_height += section_spacing  # Space after section
            
            # Add some padding at the bottom
            total_height += 20
            
            # Create content surface with per-pixel alpha
            content_surface = pygame.Surface((panel_width - 40, total_height), pygame.SRCALPHA)
            
            # Draw content on the surface
            y_pos = 0
            for section in self.how_to_instructions:
                # Draw section title
                title_surface = title_font.render(section["title"], True, (100, 200, 255))
                title_rect = title_surface.get_rect(x=10, top=y_pos)
                content_surface.blit(title_surface, title_rect)
                y_pos += section_spacing
                
                # Draw section content
                for line in section["content"]:
                    line_surface = content_font.render(line, True, (255, 255, 255))
                    line_rect = line_surface.get_rect(x=30, top=y_pos)
                    content_surface.blit(line_surface, line_rect)
                    y_pos += line_spacing
                
                y_pos += section_spacing // 2  # Smaller space after section
            
            # Save the content surface for debugging
            self.debug_content = content_surface
            
            # Update panel content
            self.howto_panel.update_content(content_surface)
            
        except Exception as e:
            print(f"Error setting up how-to panel: {e}")
            import traceback
            traceback.print_exc()
        
        # Initialize volumes from SoundManager
        self.music_volume = SoundManager.get_music_volume()
        self.sfx_volume = SoundManager.get_sfx_volume()
        
        # Credits scrolling state
        self.credits_scroll_y = 0
        self.credits_scroll_speed = 0.5
        self.credits_total_height = 1000  # Total height of credits content
        self.last_credits_update = 0
        
    def update_ui_elements(self):
        """Update UI elements based on which tab is active"""
        self.ui_elements = self.common_ui_elements.copy()
        
        if self.current_tab == "video":
            self.ui_elements.extend([
                self.fullscreen_btn,
                self.windowed_btn
            ])
        elif self.current_tab == "audio":
            self.ui_elements.extend([
                self.music_vol_up,
                self.music_vol_down,
                self.sfx_vol_up,
                self.sfx_vol_down
            ])
        # No additional UI elements for credits tab
    
    def update(self, dt):
        """Update the settings screen"""
        super().update(dt)
        
        current_time = pygame.time.get_ticks()
        
        # Update credits scrolling if credits tab is active
        if self.current_tab == "credits":
            if current_time - self.last_credits_update > 16:  # ~60fps
                self.credits_scroll_y += self.credits_scroll_speed
                self.last_credits_update = current_time
                
                # Reset scroll position when it reaches the bottom
                if self.credits_scroll_y > self.credits_total_height:
                    self.credits_scroll_y = -450  # Reset to just above the visible area
                    
        # Update how-to panel if active
        elif self.current_tab == "howto" and self.howto_panel:
            self.howto_panel.update()
    
    def draw(self):
        """Draw the settings screen"""
        # Draw background
        self.screen.blit(self.main_background, (0, 0))
        
        # Draw semi-transparent overlay
        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))
        self.screen.blit(overlay, (0, 0))
        
        # Get screen dimensions
        screen_width = self.screen.get_width()
        screen_height = self.screen.get_height()
        screen_center_x = screen_width // 2
        
        # Draw settings menu background with rounded corners - made larger
        settings_menu_width = 1152  # Increased width
        settings_menu_height = 700   # Increased height
        settings_menu_x = (screen_width - settings_menu_width) / 2
        settings_menu_y = (screen_height - settings_menu_height) / 2  # Slightly higher up
        
        # Create settings panel with semi-transparent background
        settings_menu_surface = pygame.Surface((settings_menu_width, settings_menu_height), pygame.SRCALPHA)
        settings_menu_surface.fill((20, 20, 20, 230))
        
        # Draw the panel with rounded corners
        settings_rect = pygame.Rect(0, 0, settings_menu_width, settings_menu_height)
        pygame.draw.rect(settings_menu_surface, (50, 50, 50, 200), settings_rect, 0, border_radius=15)
        pygame.draw.rect(settings_menu_surface, (200, 200, 200), settings_rect, 2, border_radius=15)
        self.screen.blit(settings_menu_surface, (settings_menu_x, settings_menu_y))
        
        # Draw settings title with custom font
        title_font = self.font_manager.title_font()
        draw_text(self.screen, "SETTINGS", title_font, WHITE_COLOR, screen_center_x, 80)
        
        # Removed tab indicator as requested
        
        # Draw UI elements
        super().draw()
        
        # Draw specific content based on current tab
        if self.current_tab == "howto":
            self.draw_howto()
        elif self.current_tab == "video":
            self.draw_video_settings()
        elif self.current_tab == "audio":
            self.draw_audio_settings()
        else:  # credits tab
            self.draw_credits()
            
    def draw_video_settings(self):
        """Draw video settings content"""
        # Get screen dimensions
        screen_width = self.screen.get_width()
        screen_center_x = screen_width // 2
        
        # Get fonts
        heading_font = self.font_manager.subheading_font()
        label_font = self.font_manager.normal_font()
        
        # Video settings title
        draw_text(self.screen, "VIDEO SETTINGS", heading_font, WHITE_COLOR, screen_center_x, 190)
        
        # Draw settings labels with custom font
        col1_label_x = screen_center_x - 120
        
        # Display mode label
        draw_text(self.screen, "Display Mode:", label_font, WHITE_COLOR, col1_label_x, 240)
        
        # Highlight current display mode with a more subtle indicator
        if self.is_fullscreen:
            pygame.draw.rect(self.screen, (80, 200, 80, 50),  # More transparent highlight
                           (self.fullscreen_btn.rect.x, self.fullscreen_btn.rect.y,
                            self.fullscreen_btn.rect.width, self.fullscreen_btn.rect.height), 
                           2, border_radius=8)  # Border instead of fill
        else:
            pygame.draw.rect(self.screen, (80, 200, 80, 50),  # More transparent highlight
                           (self.windowed_btn.rect.x, self.windowed_btn.rect.y,
                            self.windowed_btn.rect.width, self.windowed_btn.rect.height),
                           2, border_radius=8)  # Border instead of fill
        
    def draw_audio_settings(self):
        """Draw audio settings content"""
        # Get screen dimensions
        screen_width = self.screen.get_width()
        screen_center_x = screen_width // 2
        
        # Get fonts
        heading_font = self.font_manager.subheading_font()
        label_font = self.font_manager.normal_font()
        value_font = self.font_manager.normal_font()
        
        # Audio settings title
        draw_text(self.screen, "AUDIO SETTINGS", heading_font, WHITE_COLOR, screen_center_x, 190)
        
        # Column positions
        col1_label_x = screen_center_x - 250  # Labels
        value_x = screen_center_x  # Values
        
        # Music volume label
        draw_text(self.screen, "Music Volume:", label_font, WHITE_COLOR, col1_label_x, 240)
        
        # Music volume slider visualization
        slider_width = 200
        slider_height = 8
        slider_x = value_x - slider_width // 2
        slider_y = 240
        
        # Draw slider background
        pygame.draw.rect(self.screen, (50, 50, 50), 
                        (slider_x, slider_y, slider_width, slider_height), 0, border_radius=4)
        
        # Draw filled part of slider
        filled_width = int(slider_width * self.music_volume)
        if filled_width > 0:
            pygame.draw.rect(self.screen, (80, 200, 80), 
                            (slider_x, slider_y, filled_width, slider_height), 0, border_radius=4)
            
        # Draw music volume percentage
        draw_text(self.screen, f"{int(self.music_volume * 100)}%", value_font, WHITE_COLOR, value_x, 270)
        
        # SFX volume
        draw_text(self.screen, "SFX Volume:", label_font, WHITE_COLOR, col1_label_x, 310)
        
        # SFX volume slider visualization
        slider_y = 310
        
        # Draw slider background
        pygame.draw.rect(self.screen, (50, 50, 50), 
                        (slider_x, slider_y, slider_width, slider_height), 0, border_radius=4)
        
        # Draw filled part of slider
        filled_width = int(slider_width * self.sfx_volume)
        if filled_width > 0:
            pygame.draw.rect(self.screen, (80, 200, 80), 
                            (slider_x, slider_y, filled_width, slider_height), 0, border_radius=4)
            
        # Draw sfx volume percentage
        draw_text(self.screen, f"{int(self.sfx_volume * 100)}%", value_font, WHITE_COLOR, value_x, 340)
        
    def on_video_settings_clicked(self):
        """Switch to video settings tab"""
        self.current_tab = "video"
        self.update_ui_elements()
        
    def on_audio_settings_clicked(self):
        """Switch to audio settings tab"""
        self.current_tab = "audio"
        self.update_ui_elements()
        
    def on_howto_clicked(self):
        """Switch to how-to tab"""
        self.current_tab = "howto"
        self.setup_howto_panel()  # Rebuild panel in case window was resized
        self.update_ui_elements()
        
    def on_credits_clicked(self):
        """Switch to credits tab"""
        self.current_tab = "credits"
        self.credits_scroll_y = -450  # Start with credits at the bottom
        self.last_credits_update = pygame.time.get_ticks()
        self.update_ui_elements()
        
    def draw_credits(self):
        """Draw credits content with smooth scrolling"""
        # Get screen dimensions
        screen_width = self.screen.get_width()
        screen_center_x = screen_width // 2
        
        # Get fonts
        heading_font = self.font_manager.subheading_font()
        title_font = self.font_manager.normal_font()
        content_font = self.font_manager.small_font()
        
        # Credits title (fixed position)
        draw_text(self.screen, "CREDITS", heading_font, WHITE_COLOR, screen_center_x, 190)
        
        # Create a surface for the credits content with transparency
        credits_height = 450  # Height of the scrollable area
        credits_surface = pygame.Surface((screen_width - 200, credits_height), pygame.SRCALPHA)
        
        # Draw credits content with scrolling
        y_pos = 0  # Start drawing at the top of the surface
        section_spacing = 40
        line_spacing = 35
        
        for section in self.credits_info:
            # Draw section title
            title_y = y_pos - self.credits_scroll_y
            if -50 < title_y < credits_height + 50:  # Only draw if visible or nearly visible
                draw_text(credits_surface, section["title"], title_font, (200, 200, 255), 
                        credits_surface.get_width() // 2, title_y)
            y_pos += section_spacing
            
            # Draw section content
            for line in section["content"]:
                line_y = y_pos - self.credits_scroll_y
                if -50 < line_y < credits_height + 50:  # Only draw if visible or nearly visible
                    draw_text(credits_surface, line, content_font, WHITE_COLOR, 
                            credits_surface.get_width() // 2, line_y)
                y_pos += line_spacing
            
            # Add space after each section
            y_pos += section_spacing
        
        # Apply the credits surface to the screen with a mask for smooth edges
        self.screen.blit(credits_surface, (100, 260))
        
        # Draw version and copyright (fixed position at bottom)
        footer_y = 700  # Position at bottom of credits area
        version_text = "Version 1.1.0"
        copyright_text = "© 2025 NeON. All rights reserved."
        
        draw_text(self.screen, version_text, content_font, (180, 180, 180), screen_center_x, footer_y)
        draw_text(self.screen, copyright_text, content_font, (180, 180, 180), screen_center_x, footer_y + 25)
        
    def on_close_clicked(self):
        """Return to main menu"""
        from Menu.scenes.main_menu_scene import MainMenuScene
        self.switch_to_scene(MainMenuScene(self.screen))
        
    # Video settings handlers
    def on_fullscreen_clicked(self):
        """Set fullscreen mode"""
        if not self.is_fullscreen:  # Only apply if not already in fullscreen
            self.is_fullscreen = True
            self.apply_video_settings()
        
    def on_windowed_clicked(self):
        """Set windowed mode"""
        if self.is_fullscreen:  # Only apply if in fullscreen
            self.is_fullscreen = False
            self.apply_video_settings()
    
    def apply_video_settings(self):
        """Apply video settings to the game"""
        if self.is_fullscreen:
            # Get the current display mode for fullscreen
            info = pygame.display.Info()
            self.resolution = (info.current_w, info.current_h)
            self.screen = pygame.display.set_mode(self.resolution, pygame.FULLSCREEN)
        else:
            # Restore to windowed mode with original size
            self.screen = pygame.display.set_mode(self.original_size, pygame.RESIZABLE)
            
        # Update the display
        pygame.display.flip()
        
    # Audio settings handlers
    def on_music_vol_up(self):
        """Increase music volume"""
        from Game.managers.sound_manager import SoundManager
        self.music_volume = min(1.0, round(self.music_volume + 0.1, 1))
        SoundManager.set_music_volume(self.music_volume)
        # Play a sound to demonstrate volume
        SoundManager.play_sound(select_button_sfx, volume=0.5)
        
    def on_music_vol_down(self):
        """Decrease music volume"""
        from Game.managers.sound_manager import SoundManager
        self.music_volume = max(0.0, round(self.music_volume - 0.1, 1))
        SoundManager.set_music_volume(self.music_volume)
        # Play a sound to demonstrate volume
        SoundManager.play_sound(select_button_sfx, volume=0.5)
        
    def on_sfx_vol_up(self):
        """Increase SFX volume"""
        from Game.managers.sound_manager import SoundManager
        self.sfx_volume = min(1.0, round(self.sfx_volume + 0.1, 1))
        SoundManager.set_sfx_volume(self.sfx_volume)
        # Play a sound to demonstrate volume
        SoundManager.play_sound(select_button_sfx, volume=0.5)
        
    def on_sfx_vol_down(self):
        """Decrease SFX volume"""
        from Game.managers.sound_manager import SoundManager
        self.sfx_volume = max(0.0, round(self.sfx_volume - 0.1, 1))
        SoundManager.set_sfx_volume(self.sfx_volume)
        # Play a sound to demonstrate volume
        SoundManager.play_sound(select_button_sfx, volume=0.5)
        
    def handle_event(self, event):
        """Handle pygame events"""
        # Handle how-to panel events if active
        if self.current_tab == "howto" and self.howto_panel:
            if self.howto_panel.handle_event(event):
                return True
                
        # Let the base class handle other events
        return super().handle_event(event)
        
    def draw_howto(self):
        """Draw the how-to content with scrollable panel"""
        # Get screen dimensions and fonts
        screen_width = self.screen.get_width()
        screen_center_x = screen_width // 2
        heading_font = self.font_manager.subheading_font()
        
        # Draw the title
        draw_text(self.screen, "HOW TO PLAY", heading_font, WHITE_COLOR, screen_center_x, 190)
        
        # Draw the scrollable panel if it exists
        if self.howto_panel:
            # Draw a background for the panel
            panel_bg = pygame.Surface((self.howto_panel.rect.width, self.howto_panel.rect.height), pygame.SRCALPHA)
            panel_bg.fill((30, 30, 50, 200))  # Semi-transparent dark blue
            self.screen.blit(panel_bg, (self.howto_panel.rect.x, self.howto_panel.rect.y))
            
            # Draw the scrollable panel
            self.howto_panel.draw(self.screen)
            
            # Draw a border around the panel for better visibility
            pygame.draw.rect(self.screen, (100, 100, 150), 
                           (self.howto_panel.rect.x - 1, 
                            self.howto_panel.rect.y - 1,
                            self.howto_panel.rect.width + 2,
                            self.howto_panel.rect.height + 2), 
                           2, border_radius=5)
            
            # Debug code has been removed
