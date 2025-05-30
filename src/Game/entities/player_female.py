import math
import random

from ..entities.player import Player
from ..entities.items import Bullet
from ..managers.image_manager import *
from pygame.locals import (
    K_w,
    K_a, 
    K_s, 
    K_d,
)

class Player_Female(Player):
    def __init__(self):
        super(Player_Female, self).__init__()
        self.normal_bullet_damage = 10
        self.fire_rate = 200

        self.maximum_health = 200
        self.current_health = self.maximum_health
        self.health = self.maximum_health
        self.update_health_ratio()  # Ensure health ratio is updated after setting max health
        self.speed = 2

        self.surf = female_idle_sprite[0]
        self.rect = self.surf.get_rect(
            center = (
                (LEVEL_WIDTH-self.surf.get_width())/2,
                (LEVEL_HEIGHT-self.surf.get_height())/2
            ) 
        )
        
    def idle_anim(self, clock):
        self.idle_time += clock.get_time()
        if self.idle_time >= 200:
            self.idle_time = 0
            # Only increment index if we have sprites loaded
            if female_idle_sprite:
                self.idle_index = (self.idle_index + 1) % len(female_idle_sprite)
            else:
                # Create a simple colored rectangle as fallback
                fallback = pygame.Surface((32, 64))
                fallback.fill((255, 0, 255))  # Magenta color for visibility
                self.surf = fallback
                return
            
        try:
            if self.direction == "right":
                if female_idle_sprite:  # Check if list is not empty
                    self.surf = female_idle_sprite[self.idle_index]
            elif female_idle_sprite_left:  # Check if list is not empty
                self.surf = female_idle_sprite_left[self.idle_index]
        except IndexError:
            # If we still get an index error, create a fallback surface
            fallback = pygame.Surface((32, 64))
            fallback.fill((0, 255, 255))  # Cyan color to indicate error state
            self.surf = fallback
    
    def run_anim(self, clock):
        self.run_time += clock.get_time()
        if self.run_time >= 125:
            self.run_time = 0
            # Only increment index if we have sprites loaded
            if female_run_sprite:
                self.run_index = (self.run_index + 1) % len(female_run_sprite)
            else:
                # Create a simple colored rectangle as fallback
                fallback = pygame.Surface((32, 64))
                fallback.fill((255, 128, 0))  # Orange color for visibility
                self.surf = fallback
                return
            
        try:
            if self.direction == "right":
                if female_run_sprite:  # Check if list is not empty
                    self.surf = female_run_sprite[self.run_index]
            elif female_run_sprite_left:  # Check if list is not empty
                self.surf = female_run_sprite_left[self.run_index]
        except IndexError:
            # If we still get an index error, create a fallback surface
            fallback = pygame.Surface((32, 64))
            fallback.fill((128, 0, 128))  # Purple color to indicate error state
            self.surf = fallback
            
    def fire_bullets(self, camera, clock, player_bullets, all_sprites):
        self.time_since_last_shot += clock.get_time()

        if self.time_since_last_shot >= self.fire_rate:
            mouse = pygame.mouse.get_pos()
            player_to_mouse = (mouse[0] - camera.camera.x - self.rect.centerx, 
                             mouse[1] - camera.camera.y - self.rect.centery)
            angle_to_mouse = -math.atan2(player_to_mouse[1], player_to_mouse[0])
            
            # Create bullet at player's position
            bullet_pos = (self.rect.centerx, self.rect.centery)
            # Offset bullet position slightly in the direction of fire
            bullet_pos = (bullet_pos[0] + 50 * math.cos(angle_to_mouse), 
                         bullet_pos[1] - 50 * math.sin(angle_to_mouse))
            
            new_bullet = Bullet(self, bullet_pos)
            new_bullet.distance_limit = 700
            player_bullets.add(new_bullet)
            all_sprites.add(new_bullet)
            self.time_since_last_shot = 0
            
    def burst_skill(self, camera, clock, player_bullets, all_sprites):
        self.time_since_last_burst_shot += clock.get_time()
        
        if self.time_since_last_burst_shot >= 100:
            mouse = pygame.mouse.get_pos()
            player_to_mouse = (mouse[0] - camera.camera.x - self.rect.centerx, mouse[1] - camera.camera.y - self.rect.centery)
            angle_to_mouse = - math.atan2(player_to_mouse[1], player_to_mouse[0])
            
            # Tính toán hướng mới cho hai viên đạn cách biệt 10 độ với hướng của chuột
            new_angle1 = angle_to_mouse + math.radians(10)
            new_angle2 = angle_to_mouse - math.radians(10)
            
            # Tạo viên đạn với hướng mới
            bullet1_pos = (self.rect.centerx, self.rect.centery)
            bullet2_pos = (self.rect.centerx, self.rect.centery)
            
            # Tính toán vị trí mới của viên đạn theo hướng mới
            bullet1_pos = (bullet1_pos[0] + 75 * math.cos(new_angle1), bullet1_pos[1] - 75 * math.sin(new_angle1))
            bullet2_pos = (bullet2_pos[0] + 75 * math.cos(new_angle2), bullet2_pos[1] - 75 * math.sin(new_angle2))
            
            # Tạo viên đạn với vị trí và hướng mới
            new_bullet1 = Bullet(self, bullet1_pos)
            new_bullet1.distance_limit = 700
            new_bullet2 = Bullet(self, bullet2_pos)
            new_bullet2.distance_limit = 700
            
            player_bullets.add(new_bullet1, new_bullet2)
            all_sprites.add(new_bullet1, new_bullet2)
            
            # Đặt lại thời gian giữa các lần bắn đạn
            self.time_since_last_burst_shot = 0
    
    def burst_(self, camera, clock, player_bullets, all_sprites):
        self.burst_clock += clock.get_time()
        
        if self.burst_clock >= self.burst_time:
            self.burst = False
            self.burst_clock = 0
            return
        
        self.burst_skill(camera, clock, player_bullets, all_sprites)
    
    def get_movement_speed(self):
        # Apply movement speed buff to base speed
        base_speed = 5  # Original base speed
        buffed_speed = base_speed * (1 + self.movement_speed_buff / 100)
        return buffed_speed
        
    def update(self, clock, camera, pressed_keys, player_bullets, all_sprites, background):
        # Get current movement speed with all buffs applied
        current_speed = self.get_movement_speed()
        
        # Reset movement flags
        is_moving = False
        
        # Handle movement with diagonal support
        move_x = 0
        move_y = 0
        
        if pressed_keys[K_w]:
            move_y -= current_speed
            is_moving = True
        if pressed_keys[K_s]:
            move_y += current_speed
            is_moving = True
        if pressed_keys[K_a]:
            move_x -= current_speed
            self.move_left = True
            self.move_right = False
            self.direction = "left"
            is_moving = True
        elif pressed_keys[K_d]:
            move_x += current_speed
            self.move_right = True
            self.move_left = False
            self.direction = "right"
            is_moving = True
            
        # Normalize diagonal movement to maintain consistent speed
        if move_x != 0 and move_y != 0:
            # This ensures diagonal movement isn't faster than horizontal/vertical
            move_x *= 0.7071  # 1/sqrt(2)
            move_y *= 0.7071
            
        # Apply movement if any key is pressed
        if is_moving:
            self.rect.move_ip(move_x, move_y)
            self.run_anim(clock)
        else:
            self.idle_anim(clock)
            
        # Make sure player doesn't leave the screen
        self.rect.left = max(0, self.rect.left)
        self.rect.right = min(LEVEL_WIDTH, self.rect.right)
        self.rect.top = max(0, self.rect.top)
        self.rect.bottom = min(LEVEL_HEIGHT, self.rect.bottom)
        
        # Energy should only be gained from pickups, not regenerated automatically
        
        # Fire bullets automatically as in original code
        self.fire_bullets(camera, clock, player_bullets, all_sprites)
            
        # Burst skill
        if self.burst:
            self.burst_(camera, clock, player_bullets, all_sprites)
            
    def show_stats(self):
        print(f"Player Stats - Level: {self.level}, HP: {self.maximum_health}, DMG: {self.normal_bullet_damage}, SPD: {self.speed}")
        
    def show_boss_defeated_message(self):
        """Show a message when a boss is defeated in endless mode"""
        # Create a semi-transparent overlay with a message
        overlay = pygame.Surface((SCREEN_WIDTH, 100), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))  # Semi-transparent black
        
        # Draw the overlay at the top center of the screen
        screen = pygame.display.get_surface()
        screen.blit(overlay, (0, 50))
        
        # Draw the message
        message = self.ui.font.render("BOSS DEFEATED! SCORE +1000", True, (255, 215, 0))  # Gold color
        message_rect = message.get_rect(center=(SCREEN_WIDTH // 2, 100))
        screen.blit(message, message_rect)
        
        # Update the display
        pygame.display.flip()
        
        # Set a timer to clear the message after 2 seconds
        pygame.time.set_timer(pygame.USEREVENT + 1, 2000, True)  # One-time event
