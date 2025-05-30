import pygame
import math
import random

from ..core.define import *
from ..entities.items import *
from ..managers.image_manager import *  # Import all sprite images

# Base class
class Enemy(pygame.sprite.Sprite):
    elite_slain_time = 0
    
    def __init__(self, player):
        super(Enemy, self).__init__()
        # Enemy's base attr
        self.size = 10  # Standardized hitbox size for all enemies
        self.speed = 2
        self.health = 10
        self.collide_damage = 10
        self.is_hit = False
        self.hit_time = 0
        self.hit_cooldown = 300  # 0.3 seconds of hit stun
        self.player = player
        self.direction = "right"
        
        # Sprite and animation attributes
        self.sprite = None
        self.sprite_time = 0
        self.sprite_index = 0
        self.animation_speed = 4  # Frames per second
        self.old_x = 0
        self.surf = pygame.Surface((self.size, self.size))
        self.rect = self.surf.get_rect()
        
        # Animation states (spawn/death animations disabled)
        self.is_spawning = False
        self.is_dying = False
        self.is_invincible = False
        self.original_sprite = None  # Store the original sprite for reference
        
        # Movement tracking
        self.spawn_radius = 700
        self.old_position = (0, 0)
        
        # Initialize animation state
        self.last_update = pygame.time.get_ticks()
        
        # Calculate random position around player
        self.generate_random_position(player)
        
    # Các phương thức get/set
    def get_position_x(self):
        return self.rect.x
    
    def get_position_y(self):
        return self.rect.y
    
    def set_size(self, value):
        self.size = value
        
    def get_size(self):
        return self.size
    
    def set_speed(self, value):
        self.speed = value
        
    def get_speed(self):
        return self.speed

    def set_hp(self, value):
        self.health = value
    
    def get_hp(self):
        return self.health
    
    def set_damage(self, value):
        self.collide_damage = value
    
    def get_damage(self):
        return self.collide_damage
    
    # Các hàm phụ cho lớp Enemy
    def left_or_right(self):
        new_x = self.get_position_x()
        if new_x >= self.old_x:     # Sprite hướng về bên phải
            self.direction = "right"
        else:
            self.direction = "left"
        self.old_x = new_x      # Cập nhật vị trí mới của old_x
        
    def update_animation(self, clock):
        """Animation update (spawn/death animations disabled)"""
        if self.is_dying:
            self.kill()  # Remove enemy immediately when dead
            return True
        return False
    
    def start_death_animation(self):
        """Mark enemy for immediate removal (death animation disabled)"""
        if not self.is_dying:
            self.is_dying = True
            return True
        return False
    
    def load_sprite(self, clock):
        # Skip spawn/death animations, just handle normal sprite updates
        if self.is_dying:
            return True  # Remove enemy immediately
            
        # Handle hit animation
        if hasattr(self, 'is_hit') and self.is_hit:
            current_time = pygame.time.get_ticks()
            elapsed = current_time - self.hit_time
            if elapsed < self.hit_cooldown:
                # Flash white when hit
                if (current_time // 50) % 2 == 0:
                    self.surf = change_color(self.original_sprite, (255, 255, 255, 200))
                else:
                    self.surf = self.original_sprite
            else:
                self.surf = self.original_sprite
            return False
            
        # Normal animation
        if hasattr(self, 'sprite') and hasattr(self, 'sprite_index') and hasattr(self, 'animation_speed'):
            # Update animation frame based on time
            self.sprite_time += clock.get_time()
            if self.sprite_time >= 250:  # Change frame every 250ms
                self.sprite_index = (self.sprite_index + 1) % len(self.sprite)
                self.sprite_time = 0
                
            # Get current frame
            current_sprite = self.sprite[self.sprite_index]
            
            # Apply flip based on direction
            if self.direction == "right":
                self.surf = current_sprite
            else:
                self.surf = pygame.transform.flip(current_sprite, True, False)
                
            # Update the rect to match the new surface size
            old_center = self.rect.center
            self.rect = self.surf.get_rect(center=old_center)
            self.size = max(self.rect.width, self.rect.height)
            
            # Store the original sprite for animations
            self.original_sprite = self.surf.copy()
            
        return False  # Default: don't remove the enemy
        
    def generate_random_position(self, player):
        # Tạo một vị trí ngẫu nhiên xung quanh người chơi
        angle = random.uniform(0, 2 * math.pi)
        # Sử dụng một bán kính ngẫu nhiên từ 700 đến 1200px
        random_radius = random.uniform(700, 1200)
        random_x = player.get_position_x() + random_radius * math.cos(angle)
        random_y = player.get_position_y() + random_radius * math.sin(angle)
        # Cập nhật vị trí của kẻ địch
        self.rect.center = (random_x, random_y)

    def move_towards_player(self, player):
        # Calculate direction vector from enemy to player
        dx = player.get_position_x() - self.rect.centerx
        dy = player.get_position_y() - self.rect.centery
        distance = math.sqrt(dx ** 2 + dy ** 2)
        
        # Update direction based on movement (for sprite flipping)
        if dx > 0:
            self.direction = "right"
        elif dx < 0:
            self.direction = "left"
            
        # Cho phép enemy tiến đến sát player
        min_distance = 5  # Đã giảm khoảng cách tối thiểu xuống 5
        if distance > min_distance:
            # Normalize direction vector
            if distance != 0:
                dx_normalized = dx / distance
                dy_normalized = dy / distance
            else:
                dx_normalized = 0
                dy_normalized = 0
            # Move enemy along the normalized direction
            self.rect.move_ip(dx_normalized * self.speed, dy_normalized * self.speed)
        
    def take_damage(self, damage):
        """Handle taking damage with invincibility frames"""
        if self.is_invincible or self.is_dying or self.is_spawning:
            return False
            
        self.health -= damage
        if self.health <= 0:
            return self.start_death_animation()
            
        # Start hit animation
        self.is_hit = True
        self.hit_time = pygame.time.get_ticks()
        return False
        
    def update(self, player, player_bullets, all_sprites, clock):
        # Store old position for direction calculation
        self.old_position = (self.rect.centerx, self.rect.centery)
        
        # Update hit cooldown
        current_time = pygame.time.get_ticks()
        if self.is_hit and current_time - self.hit_time > self.hit_cooldown:
            self.is_hit = False
            
        # Update sprite animation (returns True if enemy should be removed)
        if self.load_sprite(clock):
            return True
            
        # If still in spawn animation, don't move or attack
        if self.is_spawning:
            return False
            
        # If in death animation, don't move or attack
        if self.is_dying:
            return False
            
        # Update direction based on movement
        if self.rect.centerx > self.old_position[0]:
            self.direction = "right"
        elif self.rect.centerx < self.old_position[0]:
            self.direction = "left"
            
        # Always move towards player if not in hit stun and not dying
        if not self.is_hit and not self.is_dying:
            self.move_towards_player(player)
            
        # Check for collisions with player bullets
        if not self.is_invincible and hasattr(self, 'check_bullet_collisions'):
            self.check_bullet_collisions(player_bullets, all_sprites)
            
        # Check for collision with player (only if not invincible, not hit, and not dying)
        if not self.is_invincible and not self.is_hit and not self.is_dying:
            if hasattr(player, 'rect') and hasattr(self, 'rect'):
                if self.rect.colliderect(player.rect):
                    if hasattr(player, 'take_damage') and hasattr(self, 'collide_damage'):
                        player.take_damage(self.collide_damage)
                        
        return False


    def check_bullet_collisions(self, player_bullets, all_sprites):
        """Check for collisions with player bullets"""
        hits = pygame.sprite.spritecollide(self, player_bullets, False)
        for bullet in hits:
            # Only process if bullet is active and not already collided
            if hasattr(bullet, 'active') and bullet.active and not bullet.collided:
                bullet.collided = True
                if self.take_damage(bullet.damage):
                    # If take_damage returns True, enemy is dead
                    if hasattr(bullet, 'on_hit'):
                        bullet.on_hit()
                    bullet.kill()
                    return True
                else:
                    # Just a hit, not a kill
                    bullet.kill()
        return False

# Derived class
class Normal(Enemy):
    def __init__(self, player):
        super(Normal, self).__init__(player)
        
        # Choose random enemy type
        rand = random.randint(0, 3)
        match rand:
            case 0:
                self.sprite = ghost_sprite
            case 1:
                self.sprite = goblin_sprite
            case 2:
                self.sprite = skeleton_sprite
            case _:
                self.sprite = slime_sprite
        
        # Use first sprite as initial surface (already scaled in image_manager)
        self.surf = self.sprite[0]
        self.original_sprite = self.surf.copy()  # Store original for animations
        
        # Update rect and size to match sprite dimensions
        self.rect = self.surf.get_rect(center=self.rect.center)
        self.size = max(self.rect.width, self.rect.height)
        
        # Set initial position (will be overridden by generate_random_position)
        self.rect.center = self.rect.center
        
        # Initialize animation variables
        self.animation_index = 0
        self.animation_speed = 0.15  # Lower is faster
        self.last_update = pygame.time.get_ticks()
        
        # No spawn animation - enemies appear and can move immediately
        self.is_spawning = False
        self.is_invincible = False
        
        # Generate random position around player
        self.generate_random_position(player)
        
    def update(self, player, player_bullets, all_sprites, clock):
        # Let the parent class handle the update logic and animations
        return super().update(player, player_bullets, all_sprites, clock)