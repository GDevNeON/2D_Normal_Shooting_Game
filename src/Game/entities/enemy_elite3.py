import pygame
import math
import random

from ..core.define import *
from ..entities.enemy import Enemy
from ..entities.items import EliteBullet
from ..managers.image_manager import *

class Elite_3(Enemy):
    """
    Elite 3 is an elite mob enemy with special abilities.
    Uses pre-scaled sprites from image_manager.
    """
    def __init__(self, player):
        # Initialize base class first
        super(Elite_3, self).__init__(player)
        
        # Elite-specific attributes
        self.speed = 5
        self.hp = 500
        self.collide_damage = 10
        
        # Use the pre-scaled sprites from image_manager
        self.sprite = eskeleton_sprite
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
        self.skill_dmg = [10, 20]
        self.fire_rate = 2  # Time between shots (in seconds)
        self.time_since_last_shot = 0
        self.move_rate = 3  # Time between moves (in seconds)
        self.time_since_last_moved = 0
        self.is_hitted = False
        self.hitted_time = 0
        
        # Dash attack attributes
        self.is_dashing = False
        self.dash_cooldown = 4000  # Slightly faster cooldown than Elite_2
        self.dash_duration = 400  # Slightly faster dash than Elite_2
        self.dash_distance = 200  # Pixels
        self.dash_damage = 25  # Slightly more damage than Elite_2
        self.last_dash_time = 0
        self.dash_start_time = 0
        self.dash_start_x = 0
        self.dash_start_y = 0
        self.dash_dx = 0
        self.dash_dy = 0
        self.dash_sprite = None
        self.orig_sprite = self.surf.copy()
        
        # Trail effect for dash
        self.trail_positions = []
        self.max_trail_length = 8  # Number of trail images to show
        
        # Initialize dash sprite with a different color than Elite_2
        if self.sprite and len(self.sprite) > 0:
            self.dash_sprite = self.sprite[0].copy()
            # Add visual effect for dash (purple tint for Elite_3)
            self.dash_sprite.fill((200, 100, 255, 128), special_flags=pygame.BLEND_RGB_MULT)
        
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
    
    def start_dash(self, player):
        """
        Start a dash attack toward the player
        """
        self.is_dashing = True
        self.dash_start_time = pygame.time.get_ticks()
        self.dash_start_x = self.rect.centerx
        self.dash_start_y = self.rect.centery
        
        # Calculate direction to player
        dx = player.get_position_x() - self.rect.centerx
        dy = player.get_position_y() - self.rect.centery
        distance = math.sqrt(dx**2 + dy**2)
        
        if distance > 0:
            self.dash_dx = dx / distance
            self.dash_dy = dy / distance
        else:
            self.dash_dx = 0
            self.dash_dy = 0
        
        # Store original sprite for restoring later
        self.orig_sprite = self.surf.copy()
        
        # Set dash sprite
        if self.dash_sprite:
            self.surf = self.dash_sprite

    def perform_dash_attack(self, player, clock):
        """
        Perform the dash attack
        """
        current_time = pygame.time.get_ticks()
        dash_progress = min(1.0, (current_time - self.dash_start_time) / self.dash_duration)
        
        if dash_progress < 1.0:
            # Calculate new position based on progress
            new_x = self.dash_start_x + (self.dash_dx * self.dash_distance * dash_progress)
            new_y = self.dash_start_y + (self.dash_dy * self.dash_distance * dash_progress)
            
            # Store current position for trail effect (every few frames)
            if random.random() < 0.3:  # 30% chance to add a trail position each frame
                if hasattr(self, 'dash_sprite') and self.dash_sprite:
                    # Create a copy of the dash sprite with reduced opacity for trail effect
                    trail_surf = self.dash_sprite.copy()
                    trail_surf.set_alpha(120)  # 47% opacity
                    
                    # Add current position and sprite to trail
                    self.trail_positions.append({
                        'x': self.rect.centerx,
                        'y': self.rect.centery,
                        'surf': trail_surf,
                        'time': current_time
                    })
                    
                    # Limit trail length
                    if len(self.trail_positions) > self.max_trail_length:
                        self.trail_positions.pop(0)
            
            # Update position
            self.rect.centerx = int(new_x)
            self.rect.centery = int(new_y)
            
            # Keep dash sprite
            if self.dash_sprite:
                self.surf = self.dash_sprite
                
            # Check for collision with player during dash
            if self.rect.colliderect(player.rect):
                player.take_damage(self.dash_damage)
                
            return False  # Dash not complete
        else:
            # Dash complete
            self.is_dashing = False
            self.last_dash_time = current_time
            
            # Clear trail positions after dash completes
            self.trail_positions = []
            
            # Restore original sprite
            if self.orig_sprite is not None:
                self.surf = self.orig_sprite
            return True  # Dash complete

    def update(self, player, elite_bullets, all_sprites, clock):
        current_time = pygame.time.get_ticks()
        
        # Remove old trail positions (older than 400ms)
        if hasattr(self, 'trail_positions') and self.trail_positions:
            self.trail_positions = [t for t in self.trail_positions if current_time - t['time'] < 400]
        
        # Update sprite animation
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
        
        # Move towards player if not dashing
        if not self.is_dashing:
            self.move(clock, (player.get_position_x(), player.get_position_y()))

        # Check if dash is ready
        if not self.is_dashing and current_time - self.last_dash_time >= self.dash_cooldown:
            # 10% chance to dash when cooldown is over
            if random.random() < 0.1:
                self.start_dash(player)

        # Perform dash attack if started
        if self.is_dashing:
            self.perform_dash_attack(player, clock)
            
    def render_trail(self, screen):
        """Render the dash trail effect"""
        if hasattr(self, 'trail_positions') and self.trail_positions:
            for trail in self.trail_positions:
                # Create a rect for the trail image
                trail_rect = trail['surf'].get_rect(center=(trail['x'], trail['y']))
                # Draw the trail on the screen
                screen.blit(trail['surf'], trail_rect)