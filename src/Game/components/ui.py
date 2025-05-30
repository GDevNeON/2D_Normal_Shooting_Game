import pygame

from ..core.define import *
from ..managers.font_manager import FontManager

class UI:
    def __init__(self):
        # Initialize font manager
        self.font_manager = FontManager()
        self.font = self.font_manager.medium_font
        self.title_font = self.font_manager.title_font
        self.large_font = self.font_manager.title_font  # Using title_font as large_font
        self.big_font = self.font_manager.title_font    # Using title_font as big_font
        self.small_font = self.font_manager.small_font
        self.tiny_font = self.font_manager.tiny_font
        self.boss_font = self.small_font  # Use small font for boss health bar
    
    def draw_score_and_level(self, screen, score, level):
        """Draw score and level information on screen"""
        score_text = self.font.render(f"Score: {score}", True, (255, 255, 255))
        level_text = self.font.render(f"Level: {level}", True, (255, 255, 255))
        screen.blit(score_text, (10, 55))
        screen.blit(level_text, (10, 80))
    
    def draw_level_up_menu(self, screen, available_buffs):
        """Draw level up menu with buff options"""
        # Create semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))  # Black with alpha
        screen.blit(overlay, (0, 0))
        
        # Menu dimensions
        menu_width = 600
        menu_height = 400
        menu_x = (SCREEN_WIDTH - menu_width) // 2
        menu_y = (SCREEN_HEIGHT - menu_height) // 2
        
        # Draw menu background
        menu_rect = pygame.Rect(menu_x, menu_y, menu_width, menu_height)
        pygame.draw.rect(screen, (50, 50, 50), menu_rect)
        
        # Draw gradient
        for i in range(menu_height):
            alpha = int(255 * (1 - i / menu_height))
            color = (100, 100, 100, alpha)
            pygame.draw.line(screen, color, (menu_x, menu_y + i), (menu_x + menu_width, menu_y + i))
        
        # Draw menu border
        pygame.draw.rect(screen, (255, 255, 255), menu_rect, 4)
        
        # Draw title
        title = self.title_font.render("Level Up!", True, (255, 215, 0))  # Gold color
        title_shadow = self.title_font.render("Level Up!", True, (0, 0, 0))  # Shadow
        title_rect = title.get_rect(centerx=SCREEN_WIDTH//2, top=menu_y + 30)
        screen.blit(title_shadow, (title_rect.x + 2, title_rect.y + 2))  # Draw shadow
        screen.blit(title, title_rect)
        
        # Create buff buttons
        button_rects = []
        for i, buff in enumerate(available_buffs):
            # Button dimensions
            button_width = 500
            button_height = 60
            button_x = menu_x + (menu_width - button_width) // 2
            button_y = menu_y + 120 + i * (button_height + 10)
            
            # Draw button
            button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
            pygame.draw.rect(screen, (70, 70, 70), button_rect)
            pygame.draw.rect(screen, (200, 200, 200), button_rect, 2)
            
            # Draw buff text - buff is a tuple (name, type, value)
            buff_name = buff[0] if isinstance(buff, tuple) else str(buff)
            buff_text = self.font.render(buff_name, True, (255, 255, 255))
            text_rect = buff_text.get_rect(center=button_rect.center)
            screen.blit(buff_text, text_rect)
            
            button_rects.append(button_rect)
            
        return button_rects
    
    def draw_pause_menu(self, screen, player=None, show_help=False):
        """Draw pause menu overlay with character stats and options
        
        Args:
            screen: The game screen surface
            player: The player object for stats
            show_help: If True, shows the help screen instead of the main pause menu
            
        Returns:
            dict: Dictionary of button rectangles for click detection
        """
        # Create semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))  # Semi-transparent black
        screen.blit(overlay, (0, 0))
        
        # Main menu container
        menu_width = 800
        menu_height = 500
        menu_x = (SCREEN_WIDTH - menu_width) // 2
        menu_y = (SCREEN_HEIGHT - menu_height) // 2
        menu_rect = pygame.Rect(menu_x, menu_y, menu_width, menu_height)
        
        # Draw menu background
        pygame.draw.rect(screen, (40, 40, 50), menu_rect)
        pygame.draw.rect(screen, (100, 100, 120), menu_rect, 3)
        
        if show_help:
            # Show help screen
            title = self.title_font.render("HOW TO PLAY", True, (100, 200, 255))
            title_rect = title.get_rect(centerx=menu_rect.centerx, top=menu_rect.top + 30)
            screen.blit(title, title_rect)
            
            # Help content
            help_texts = [
                "CONTROLS:",
                "WASD - Move character",
                "Mouse - Aim and shoot",
                "P - Pause game",
                "ESC - Exit to main menu",
                "",
                "GAME OBJECTIVES:",
                "- Defeat enemies to earn experience and level up",
                "- Collect health pickups to restore HP",
                "- Level up to get powerful buffs",
                "- Defeat the boss to win in Normal mode",
                "- Survive as long as possible in Endless mode"
            ]
            
            # Draw help texts
            text_x = menu_rect.left + 40
            text_y = menu_rect.top + 100
            for i, text in enumerate(help_texts):
                if ":" in text:  # Section headers
                    color = (100, 200, 255)
                    text_surface = self.font.render(text, True, color)
                else:
                    color = (220, 220, 220)
                    text_surface = self.small_font.render(text, True, color)
                screen.blit(text_surface, (text_x, text_y + i * 30))
            
            # Back button
            back_button = pygame.Rect(menu_rect.centerx - 100, menu_rect.bottom - 70, 200, 50)
            pygame.draw.rect(screen, (50, 50, 120), back_button)
            pygame.draw.rect(screen, (100, 100, 200), back_button, 2)
            back_text = self.font.render("Back", True, (255, 255, 255))
            back_text_rect = back_text.get_rect(center=back_button.center)
            screen.blit(back_text, back_text_rect)
            
            return {'back': back_button}
        
        else:
            # Show main pause menu
            title = self.title_font.render("GAME PAUSED", True, (255, 255, 255))
            title_rect = title.get_rect(centerx=menu_rect.centerx, top=menu_rect.top + 20)
            screen.blit(title, title_rect)
            
            # Draw dividing line
            pygame.draw.line(screen, (100, 100, 120), 
                          (menu_rect.centerx, menu_rect.top + 60), 
                          (menu_rect.centerx, menu_rect.bottom - 20), 2)
            
            # Left side: Character Stats
            if player:
                stats_x = menu_rect.left + 40
                stats_y = menu_rect.top + 80
                
                # Character Info
                char_title = self.font.render("CHARACTER STATS", True, (255, 255, 0))
                screen.blit(char_title, (stats_x, stats_y))
                
                # Basic Stats
                stats = [
                    f"Level: {player.level}",
                    f"HP: {int(player.health)} / {player.maximum_health}",
                    f"Damage: {player.normal_bullet_damage}",
                    f"Speed: {player.speed:.1f}",
                    f"Fire Rate: {player.fire_rate}ms",
                    "",
                    "BUFFS:"
                ]
                
                # Active Buffs
                buffs = []
                if player.attack_speed_buff > 0:
                    buffs.append(f"Attack Speed: +{player.attack_speed_buff}%")
                if player.damage_buff > 0:
                    buffs.append(f"Damage: +{player.damage_buff}%")
                if player.defense_buff > 0:
                    buffs.append(f"Defense: +{player.defense_buff}%")
                if player.movement_speed_buff > 0:
                    buffs.append(f"Movement: +{player.movement_speed_buff}%")
                if player.bullet_size_buff > 0:
                    buffs.append(f"Bullet Size: +{player.bullet_size_buff}%")
                if player.healing_efficiency > 0:
                    buffs.append(f"Healing: +{player.healing_efficiency}%")
                if player.exp_efficiency > 0:
                    buffs.append(f"EXP Gain: +{player.exp_efficiency}%")
                    
                if not buffs:
                    buffs = ["No active buffs"]
                    
                # Draw all stats and buffs
                for i, stat in enumerate(stats + buffs):
                    if stat:  # Skip empty strings used as separators
                        color = (200, 200, 200) if i < len(stats) - 1 else (150, 255, 150)
                        text = self.font.render(stat, True, color)
                        screen.blit(text, (stats_x, stats_y + 40 + i * 30))
            
            # Right side: Menu Buttons
            button_width = 250
            button_height = 50
            button_x = menu_rect.centerx + 40
            button_start_y = menu_rect.centery - 30
            
            # Resume button
            self.resume_rect = pygame.Rect(button_x, button_start_y, button_width, button_height)
            pygame.draw.rect(screen, (50, 120, 50), self.resume_rect)
            pygame.draw.rect(screen, (100, 200, 100), self.resume_rect, 2)
            resume_text = self.font.render("Resume Game", True, (255, 255, 255))
            resume_text_rect = resume_text.get_rect(center=self.resume_rect.center)
            screen.blit(resume_text, resume_text_rect)
            
            # Main Menu button
            self.menu_rect = pygame.Rect(button_x, button_start_y + 80, button_width, button_height)
            pygame.draw.rect(screen, (120, 50, 50), self.menu_rect)
            pygame.draw.rect(screen, (200, 100, 100), self.menu_rect, 2)
            menu_text = self.font.render("Main Menu", True, (255, 255, 255))
            menu_text_rect = menu_text.get_rect(center=self.menu_rect.center)
            screen.blit(menu_text, menu_text_rect)
            
            # How to Play button
            self.help_rect = pygame.Rect(button_x, button_start_y + 160, button_width, button_height)
            pygame.draw.rect(screen, (50, 50, 120), self.help_rect)
            pygame.draw.rect(screen, (100, 100, 200), self.help_rect, 2)
            help_text = self.font.render("How to Play", True, (255, 255, 255))
            help_text_rect = help_text.get_rect(center=self.help_rect.center)
            screen.blit(help_text, help_text_rect)
            
            # Return the button rects for click detection
            return {
                'resume': self.resume_rect,
                'menu': self.menu_rect,
                'help': self.help_rect
            }
    
    def draw_boss_health_bar(self, screen, boss):
        """Draw boss health bar at the top of the screen"""
        if boss.health <= 0 and boss.phase == 1:
            # Don't show health bar during phase transition
            return
            
        # Background bar (empty)
        bar_width = 500
        bar_height = 30
        bar_x = (SCREEN_WIDTH - bar_width) // 2
        bar_y = 20
        pygame.draw.rect(screen, (100, 100, 100), (bar_x, bar_y, bar_width, bar_height))
        
        # Health bar (filled)
        health_ratio = boss.health / boss.max_health
        health_width = bar_width * health_ratio
        
        # Color changes based on health
        if health_ratio > 0.6:
            color = (0, 255, 0)  # Green
        elif health_ratio > 0.3:
            color = (255, 255, 0)  # Yellow
        else:
            color = (255, 0, 0)  # Red
            
        pygame.draw.rect(screen, color, (bar_x, bar_y, health_width, bar_height))
        pygame.draw.rect(screen, (255, 255, 255), (bar_x, bar_y, bar_width, bar_height), 2)  # Border
        
        # Boss name and health value
        name_text = self.boss_font.render(f"{boss.name} - Phase {boss.phase}", True, (255, 255, 255))
        health_text = self.boss_font.render(f"{boss.health}/{boss.max_health} HP", True, (255, 255, 255))
        
        screen.blit(name_text, (bar_x, bar_y - 20))
        screen.blit(health_text, (bar_x + bar_width - health_text.get_width(), bar_y - 20))
        
        # If boss is in defeated state and in feather collection phase, draw feather indicator
        if boss.defeated and boss.phase == 2 and hasattr(boss, 'feathers') and boss.feathers:
            self.draw_feather_collection_indicator(screen, boss)
    
    def draw_feather_collection_indicator(self, screen, boss):
        """Draw feather collection indicator when boss is in defeated state"""
        # Draw a semi-transparent background for better visibility
        indicator_bg = pygame.Surface((350, 60), pygame.SRCALPHA)
        indicator_bg.fill((0, 0, 0, 180))  # Black with alpha
        screen.blit(indicator_bg, (SCREEN_WIDTH // 2 - 175, 70))
        
        # Draw the feather collection progress text
        indicator_text = self.font.render(f"Feathers: {boss.feathers_collected}/{boss.total_feathers}", True, (255, 255, 255))
        screen.blit(indicator_text, (SCREEN_WIDTH // 2 - indicator_text.get_width() // 2, 80))
        
        # Draw the time remaining
        time_remaining = max(0, (boss.defeat_time + boss.feather_collection_time - pygame.time.get_ticks()) // 1000)
        time_text = self.font.render(f"Time Remaining: {time_remaining} seconds", True, (255, 255, 255))
        screen.blit(time_text, (SCREEN_WIDTH // 2 - time_text.get_width() // 2, 110))
