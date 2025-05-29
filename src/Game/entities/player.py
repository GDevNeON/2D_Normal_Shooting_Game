import pygame
import random

from ..core.define import *
from ..components.ui import UI
from ..managers.image_manager import *

# Base class
class Player(pygame.sprite.Sprite):
    # Constructor
    def __init__(self):
        super(Player, self).__init__()
        # Player's base attr
        self.size = 50  # Standardized player size
        self.speed = 1
        
        # Player's health attr 
        self.current_health = 100
        self.maximum_health = 100
        self.health_bar_length = 300
        self.health_ratio = self.maximum_health / self.health_bar_length
        self.health = 100
        self.health_change_speed = 5
        
        # Player's energy attr 
        self.current_energy = 0
        self.maximum_energy = 3
        self.energy_bar_length = 200
        self.energy_ratio = self.maximum_energy / self.energy_bar_length
        self.energy = 0
        self.energy_change_speed = 1
        
        # Player's exp attr 
        self.current_exp = 100
        self.maximum_exp = 100
        self.exp_bar_length = 500
        self.exp_ratio = self.maximum_exp / self.exp_bar_length
        self.exp = 0
        self.exp_change_speed = 1
        
        # Player's score attr
        self.score = 0
        
        # Damage state
        self.is_damaged = False
        self.damage_time = 0
        self.damage_cooldown = 1000  # 1 second cooldown between damage
        
        # Player's surf attr
        self.idle_time = 0
        self.idle_index = 0
        self.run_time = 0
        self.run_index = 0
        self.surf = None
        self.rect = None
        self.move_left = False
        self.move_right = False
        self.direction = "right"
        
        # Other player's attr
        self.normal_bullet_damage = 0
        self.level = 1
        self.fire_rate = 500
        self.time_since_last_shot = 0  
        self.burst = False
        self.time_since_last_burst_shot = 0
        self.burst_clock = 0
        self.burst_time = 5000
        
        # Buff
        self.attack_speed_buff = 0  # Tỷ lệ tăng tốc độ tấn công
        self.damage_buff = 0  # Tỷ lệ tăng sát thương
        self.max_hp_buff = 0  # Tỷ lệ tăng máu
        self.movement_speed_buff = 0  # Tỷ lệ tăng tốc độ di chuyển
        self.defense_buff = 0  # Tỷ lệ tăng phòng thủ
        self.bullet_size_buff = 0  # Tỷ lệ tăng kích thước đạn
        
        # Level up state
        self.is_leveling_up = False
        self.available_buffs = []
        self.selected_buff = None
        
        # UI
        self.ui = UI()
        
        # Sprite clock
        self.warning_time = 0
        self.is_hit = False
        self.hit_time = 0
        
    # Các phương thức get/set
    def get_position_x(self):
        return self.rect.centerx
    
    def get_position_y(self):
        return self.rect.centery
    
    def set_size(self, value):
        self.size = value
        
    def get_size(self):
        return self.size
    
    def set_speed(self, value):
        self.speed = value
        
    def get_speed(self):
        return self.speed
    
    # Các hàm animate sprite                    
    def idle_anim(self):
        pass
    
    def run_anim(self):
        pass
    
    # Các hàm phụ cho Player
    def add_experience(self, amount):
        """Add experience points and check for level up"""
        if self.is_leveling_up:  # Don't gain exp while leveling up
            return
            
        self.exp += amount
        # Check if we have enough exp to level up
        if self.exp >= self.maximum_exp:
            self.exp = self.maximum_exp  # Cap at max exp until level up is processed
            self.is_leveling_up = True
            self.prepare_level_up()
    
    def update_health_ratio(self):
        """Cập nhật tỉ lệ máu dựa trên máu tối đa hiện tại"""
        self.health_ratio = self.maximum_health / self.health_bar_length
    
    def take_damage(self, amount):
        if self.current_health > 0:
            # Apply defense buff only
            damage = amount * (1 - (self.defense_buff / 100)) if self.defense_buff > 0 else amount
            damage = max(1, damage)  # Ensure at least 1 damage is taken
            
            # Debug print for damage calculation
            print(f"Original damage: {amount}, After defense: {damage} (Defense: {self.defense_buff}%)")
            
            self.health = max(0, self.health - damage)  # Update the target health
            self.current_health = max(0, self.current_health - damage)  # Also update current health immediately
            if self.current_health <= 0:
                self.current_health = 0
                self.health = 0
                return True  # Player has died
        return False  # Player is still alive
    
    def basic_health(self):
        pygame.draw.rect(SCREEN, (255,0,0), (10,10,self.current_health/self.health_ratio,25))
        pygame.draw.rect(SCREEN, (255,255,255), (10,10,self.health_bar_length,25), 4)
        
    def advanced_health(self):
        transition_width = 0
        transition_color = (255,0,0)
        
        if self.current_health < self.health:
            self.current_health += self.health_change_speed
            transition_width = int((self.health - self.current_health)/self.health_ratio)
            transition_color = (0,255,0)
        if self.current_health > self.health:
            self.current_health -= self.health_change_speed
            transition_width = int((self.health - self.current_health)/self.health_ratio)
            transition_color = (255,255,0)
            
        health_bar_rect = pygame.Rect(10,10,self.current_health/self.health_ratio,25)
        transition_bar_rect = pygame.Rect(health_bar_rect.right,10,transition_width,25)
        
        pygame.draw.rect(SCREEN, (255,0,0), health_bar_rect)
        pygame.draw.rect(SCREEN, transition_color, transition_bar_rect)
        pygame.draw.rect(SCREEN, (255,255,255), (10,10,self.health_bar_length,25), 3)
        
    def advanced_energy(self):
        transition_width = 0
        transition_color = (255,0,0)
        
        if self.current_energy < self.energy:
            self.current_energy += self.energy_change_speed
            transition_width = int((self.energy - self.current_energy)/self.energy_ratio)
            transition_color = (0,255,0)
        if self.current_energy > self.energy:
            self.current_energy -= self.energy_change_speed
            transition_width = int((self.energy - self.current_energy)/self.energy_ratio)
            transition_color = (255,255,0)
            
        energy_bar_rect = pygame.Rect(10,32,self.current_energy/self.energy_ratio,20)
        transition_bar_rect = pygame.Rect(energy_bar_rect.right,32,transition_width,20)
        
        pygame.draw.rect(SCREEN, (0,0,255), energy_bar_rect)
        pygame.draw.rect(SCREEN, transition_color, transition_bar_rect)
        pygame.draw.rect(SCREEN, (255,255,255), (10,32,self.energy_bar_length,20), 3)
        
        # Hiển thị điểm và level
        score_text = self.ui.font.render(f"Score: {self.score}", True, (255,255,255))
        level_text = self.ui.font.render(f"Level: {self.level}", True, (255,255,255))
        SCREEN.blit(score_text, (10, 55))
        SCREEN.blit(level_text, (10, 80))
        
    def advanced_exp(self):
        transition_width = 0
        transition_color = (255,0,0)
        
        if self.current_exp < self.exp:
            self.current_exp += self.exp_change_speed
            transition_width = int((self.exp - self.current_exp)/self.exp_ratio)
            transition_color = Yellow
        if self.current_exp > self.exp:
            self.current_exp -= self.exp_change_speed
            transition_width = int((self.exp - self.current_exp)/self.exp_ratio)
            transition_color = (255,255,0)
            
        exp_bar_rect = pygame.Rect(400,670,self.current_exp/self.exp_ratio,15)
        transition_bar_rect = pygame.Rect(exp_bar_rect.right,670,transition_width,15)
        
        pygame.draw.rect(SCREEN, (255,255,0), exp_bar_rect)
        pygame.draw.rect(SCREEN, transition_color, transition_bar_rect)
        pygame.draw.rect(SCREEN, (255,255,255), (400,670,self.exp_bar_length,15), 3)
    
    def handle_level_up_selection(self, mouse_pos):
        # Check which option was clicked
        option_height = 60
        option_spacing = 10  # Match the spacing in UI class
        total_options = len(self.available_buffs)
        
        # Calculate menu dimensions to match UI class
        menu_width = 600
        menu_height = 400
        menu_x = (SCREEN_WIDTH - menu_width) // 2
        menu_y = (SCREEN_HEIGHT - menu_height) // 2
        
        # Button dimensions to match UI class
        button_width = 500
        button_height = 60
        button_x = menu_x + (menu_width - button_width) // 2
        
        for i in range(total_options):
            # Calculate button position to match UI class
            button_y = menu_y + 120 + i * (button_height + option_spacing)
            button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
            
            if button_rect.collidepoint(mouse_pos):
                # Play button select sound
                from ..managers.sound_manager import SoundManager
                SoundManager.play_button_select()
                
                self.selected_buff = self.available_buffs[i]
                self.apply_buff(self.selected_buff)
                self.is_leveling_up = False
                pygame.mixer.music.unpause()  # Resume music after level up
                break
                
    def prepare_level_up(self):
        # Reset experience
        self.exp = 0
        self.current_exp = 0
        self.level += 1
        
        # Increase maximum exp for next level
        self.maximum_exp = int(self.maximum_exp * 1.2)  # Increase by 20% each level
        self.exp_ratio = self.maximum_exp / self.exp_bar_length
        
        # Play level up sound effect
        from ..managers.sound_manager import SoundManager
        SoundManager.play_level_up()
        
        # Generate random buffs to choose from
        self.available_buffs = []
        buff_options = [
            "attack_speed", "damage", "max_hp", "movement_speed", 
            "defense", "bullet_size"
        ]
        # Select 3 random unique buffs
        selected_buffs = random.sample(buff_options, min(3, len(buff_options)))
        
        for buff in selected_buffs:
            if buff == "attack_speed":
                self.available_buffs.append(("Attack Speed +10%", "attack_speed", 10))
            elif buff == "damage":
                self.available_buffs.append(("Damage +15%", "damage", 15))
            elif buff == "max_hp":
                self.available_buffs.append(("Max HP +20%", "max_hp", 20))
            elif buff == "movement_speed":
                self.available_buffs.append(("Movement Speed +10%", "movement_speed", 10))
            elif buff == "defense":
                self.available_buffs.append(("Defense +15%", "defense", 15))
            elif buff == "bullet_size":
                self.available_buffs.append(("Bullet Size +15%", "bullet_size", 15))
            elif buff == "damage_reduction":
                self.available_buffs.append(("Damage Reduction +10%", "damage_reduction", 10))
    
    def apply_buff(self, buff):
        buff_name = buff[0]
        buff_type = buff[1]
        buff_value = buff[2]
        
        print(f"Applying buff: {buff_name} ({buff_type} +{buff_value}%)")
        
        if buff_type == "attack_speed":
            # More balanced attack speed calculation
            self.attack_speed_buff += buff_value
            # Reduce fire rate by a percentage (but not as aggressively as before)
            fire_rate_reduction = buff_value / 200  # Reduced from /100 to make it less aggressive
            self.fire_rate = max(100, int(self.fire_rate * (1 - fire_rate_reduction)))
            print(f"New fire rate: {self.fire_rate}ms")
            
        elif buff_type == "damage":
            self.damage_buff += buff_value
            print(f"Total damage buff: {self.damage_buff}%")
            
        elif buff_type == "max_hp":
            old_max = self.maximum_health
            self.maximum_health = int(self.maximum_health * (1 + buff_value/100))
            self.health_ratio = self.maximum_health / self.health_bar_length
            # Also increase current health proportionally
            health_increase = self.maximum_health - old_max
            self.health += health_increase
            self.current_health += health_increase
            print(f"Max HP increased by {health_increase} (Total: {self.maximum_health})")
            
        elif buff_type == "movement_speed":
            self.movement_speed_buff = min(100, self.movement_speed_buff + buff_value)  # Cap at 100%
            base_speed = 5  # Original speed
            self.speed = base_speed * (1 + self.movement_speed_buff/100)
            print(f"Movement speed: {self.speed}")
            
        elif buff_type == "defense":
            self.defense_buff = min(90, self.defense_buff + buff_value)  # Cap at 90%
            print(f"Defense: {self.defense_buff}%")
            
        elif buff_type == "bullet_size":
            self.bullet_size_buff += buff_value
            print(f"Bullet size buff: {self.bullet_size_buff}%")
            

    
    def draw_level_up_ui(self):
        # Create semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))  # Black with alpha 180
        SCREEN.blit(overlay, (0, 0))
        
        # Draw level up title
        level_up_text = self.ui.big_font.render(f"LEVEL UP! - Level {self.level}", True, (255, 255, 0))
        text_rect = level_up_text.get_rect(center=(SCREEN_WIDTH//2, 100))
        SCREEN.blit(level_up_text, text_rect)
        
        # Draw instructions
        instruction_text = self.ui.font.render("Choose one buff:", True, (255, 255, 255))
        instruction_rect = instruction_text.get_rect(center=(SCREEN_WIDTH//2, 160))
        SCREEN.blit(instruction_text, instruction_rect)
        
        # Draw buff options
        option_height = 60
        option_spacing = 20
        total_options = len(self.available_buffs)
        
        for i, buff in enumerate(self.available_buffs):
            buff_name = buff[0]
            
            # Calculate position for centered alignment
            option_rect = pygame.Rect(
                SCREEN_WIDTH // 2 - 150,
                SCREEN_HEIGHT // 2 - ((total_options * (option_height + option_spacing)) // 2) + i * (option_height + option_spacing),
                300,
                option_height
            )
            
            # Draw button background
            pygame.draw.rect(SCREEN, (50, 50, 70), option_rect)
            pygame.draw.rect(SCREEN, (255, 255, 255), option_rect, 2)
            
            # Draw buff text
            buff_text = self.ui.font.render(buff_name, True, (255, 255, 255))
            text_rect = buff_text.get_rect(center=option_rect.center)
            SCREEN.blit(buff_text, text_rect)