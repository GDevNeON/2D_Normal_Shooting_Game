import pygame
import math
import random

from ..core.define import *
from ..entities.enemy import Enemy
from ..entities.items import EliteBullet
from ..managers.image_manager import *

class Elite_4(Enemy):
    """
    Elite 4 is an elite mob enemy that shoots 8 bullets in all directions every 5 seconds.
    Uses pre-scaled sprites from image_manager.
    """
    def __init__(self, player):
        # Initialize base class first
        super(Elite_4, self).__init__(player)
        
        # Elite-specific attributes
        self.speed = 5
        self.hp = 500
        self.collide_damage = 50
        
        # Shooting attributes
        self.bullet_size = 20  # Smaller bullets
        self.bullet_speed = 6
        self.bullet_damage = 50
        self.fire_rate = 5  # Time between shots (in seconds)
        self.time_since_last_shot = random.uniform(3.0, 4.5)  # Randomize initial timing
        self.bullet_directions = 8  # Number of directions to shoot
        self.bullet_color = (255, 255, 0)  # Yellow bullets for Elite_4
        
        # Use the pre-scaled sprites from image_manager
        self.sprite = eslime_sprite
        if self.sprite and len(self.sprite) > 0:
            # Use the pre-scaled sprite directly
            self.surf = self.sprite[0].copy()
            # Get the size from the loaded sprite
            self.size = max(self.surf.get_width(), self.surf.get_height())
        else:
            # Fallback if sprites didn't load
            self.size = 40
            self.surf = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
            pygame.draw.rect(self.surf, (0, 255, 0), (0, 0, self.size, self.size))
        
        # Update the rect with the new size
        self.rect = self.surf.get_rect()
        
        # Combat attributes
        self.skill_dmg = [50, 100]
        self.fire_rate = 5  # Time between shots (in seconds) - 5 seconds between bursts
        self.time_since_last_shot = random.uniform(0, 2)  # Randomize initial timing
        self.move_rate = 3  # Time between moves (in seconds)
        self.time_since_last_moved = 0
        self.is_hitted = False
        self.hitted_time = 0
        
        # Shooting attributes
        self.bullet_size = 12  # Smaller bullets
        self.bullet_speed = 6
        self.bullet_damage = 50
        self.bullet_directions = 8  # Number of directions to shoot
        self.bullet_color = (255, 255, 0)  # Yellow bullets for Elite_4
        
        # Set initial position
        self.target_pos = (player.get_position_x(), player.get_position_y())
        self.spawn_radius = 600
        self.generate_random_position(player)
    
    def load_sprite(self, clock):
        self.left_or_right()
        
        self.sprite_time += clock.get_time()
        if self.sprite_index >= len(self.sprite):
            self.sprite_index = 0
        
        if self.sprite_time >= 250:
            # Store the current center position
            old_center = self.rect.center
            
            # Get the current frame (already pre-scaled in image_manager)
            self.surf = self.sprite[self.sprite_index].copy()
            
            # Flip if facing left
            if self.direction == "left":
                self.surf = pygame.transform.flip(self.surf, True, False)
                
            # Update the rect while maintaining position
            self.rect = self.surf.get_rect(center=old_center)
            
            self.sprite_index += 1
            self.sprite_time = 0
    
    def move(self, clock, player_new_pos):
        self.time_since_last_moved += clock.get_time() / 1000
        
        if self.time_since_last_moved >= self.move_rate:
            # Calculate direction vector to player
            self.target_pos = player_new_pos
            self.time_since_last_moved = 0
            
        dx = self.target_pos[0] - self.rect.centerx
        dy = self.target_pos[1] - self.rect.centery
        distance = math.sqrt(dx ** 2 + dy ** 2)
        
        stopping_distance = 10
        if distance > stopping_distance:
            # Normalize direction vector
            if distance != 0:
                dx_normalized = dx / distance
                dy_normalized = dy / distance
            else:
                dx_normalized = 0
                dy_normalized = 0
            # Move enemy along the normalized direction
            self.rect.move_ip(dx_normalized * self.speed, dy_normalized * self.speed)
    
    def update(self, player, elite_bullets, all_sprites, clock):
        # Update sprite animation
        current_time = pygame.time.get_ticks()
        if current_time - self.sprite_time > 200:  # 200ms between frames
            self.sprite_time = current_time
            
            # Store the current center position
            old_center = self.rect.center
            
            # Get the current frame (already pre-scaled in image_manager)
            self.sprite_index = (self.sprite_index + 1) % len(self.sprite)
            self.surf = self.sprite[self.sprite_index].copy()
            
            # Flip if facing left
            if self.direction == "left":
                self.surf = pygame.transform.flip(self.surf, True, False)
                
            # Update the rect while maintaining position
            self.rect = self.surf.get_rect(center=old_center)
        
        # Move towards player
        self.move(clock, (player.get_position_x(), player.get_position_y()))
        
        # Update shooting timer
        self.time_since_last_shot += clock.get_time() / 1000  # Convert to seconds
        
        # Shoot 8 bullets in all directions every 5 seconds
        if self.time_since_last_shot >= self.fire_rate:
            # Reset timer
            self.time_since_last_shot = 0
            
            # Visual effect for shooting (optional - makes the sprite flash briefly)
            flash_surf = self.surf.copy()
            flash_surf.fill((150, 255, 150, 200), special_flags=pygame.BLEND_RGB_ADD)
            self.surf = flash_surf
            
            # Create bullets in multiple directions
            for i in range(self.bullet_directions):
                # Calculate angle for this bullet (in radians)
                angle = (2 * math.pi * i) / self.bullet_directions
                
                # Calculate target position (100 pixels away in this direction)
                target_x = self.rect.centerx + 100 * math.cos(angle)
                target_y = self.rect.centery + 100 * math.sin(angle)
                
                # Create bullet
                new_bullet = EliteBullet(
                    origin_enemy=self,
                    target_position=(target_x, target_y),
                    size=self.bullet_size,
                    speed=self.bullet_speed,
                    damage=self.bullet_damage,
                    color=self.bullet_color
                )
                
                # Add bullet to groups
                elite_bullets.add(new_bullet)
                all_sprites.add(new_bullet)
