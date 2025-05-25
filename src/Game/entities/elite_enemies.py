import pygame
import math
import random

from ..core.define import *
from ..entities.enemy import Enemy, Bullet
from ..managers.image_manager import *

class Elite_1(Enemy):
    def __init__(self, player):
        # Initialize base class first
        super(Elite_1, self).__init__(player)
        
        # Elite-specific attributes
        self.base_size = 10  # Base size for elite enemies
        self.size = self.base_size  # Final size after scaling
        self.speed = 5
        self.hp = 500
        self.collide_damage = 20  # Higher damage for elite enemies
        
        # Use the pre-scaled sprites from image_manager
        self.sprite = eghost_sprite
        if self.sprite and len(self.sprite) > 0:
            # Create a new surface with the correct size
            self.surf = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
            # Scale the sprite to fit our surface size
            sprite_img = pygame.transform.scale(self.sprite[0], (self.size, self.size))
            # Blit the scaled sprite
            self.surf.blit(sprite_img, (0, 0))
        else:
            # Fallback if sprites didn't load
            self.surf = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
            pygame.draw.rect(self.surf, (255, 0, 0), (0, 0, self.size, self.size))
        
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
        
        # Set initial position
        self.target_pos = (player.get_position_x(), player.get_position_y())
        self.spawn_radius = 600
        self.generate_random_position(player)
    
    # Override the load_sprite method from the parent class
    def load_sprite(self, clock):
        self.left_or_right()
        
        self.sprite_time += clock.get_time()
        if self.sprite_index >= len(self.sprite):
            self.sprite_index = 0
        
        if self.sprite_time >= 250:
            if self.direction == "right":
                # Scale the sprite to our desired size
                original_sprite = self.sprite[self.sprite_index]
                self.surf = pygame.transform.scale(original_sprite, (self.size, self.size))
            else:
                # For left direction, scale first then flip
                original_sprite = self.sprite[self.sprite_index]
                scaled_sprite = pygame.transform.scale(original_sprite, (self.size, self.size))
                self.surf = pygame.transform.flip(scaled_sprite, True, False)
            
            self.sprite_index += 1
            self.sprite_time = 0
        
    def move(self, clock, player_new_pos):
        self.time_since_last_moved += clock.get_time() / 1000
        
        if self.time_since_last_moved >= self.move_rate:
            # Tính toán hướng vector từ kẻ địch đến người chơi
            self.target_pos = player_new_pos
            self.time_since_last_moved = 0
            
        dx = self.target_pos[0] - self.rect.centerx
        dy = self.target_pos[1] - self.rect.centery
        distance = math.sqrt(dx ** 2 + dy ** 2)
        
        stopping_distance = 10
        if distance > stopping_distance:
            # Chuẩn hóa hướng vector
            if distance != 0:
                dx_normalized = dx / distance
                dy_normalized = dy / distance
            else:
                dx_normalized = 0
                dy_normalized = 0
            # Di chuyển kẻ địch theo hướng vector đã chuẩn hóa
            self.rect.move_ip(dx_normalized * self.speed, dy_normalized * self.speed)
        
    def fire_bullets(self, camera, clock, player_new_pos, elite_bullets, all_sprites):
        # Cập nhật thời gian giữa các lần bắn đạn
        self.time_since_last_shot += clock.get_time() / 1000  # Đổi từ mili-giây sang giây

        # Kiểm tra nếu đủ thời gian để bắn đạn
        if self.time_since_last_shot >= self.fire_rate:
            # Chuyển đổi tọa độ Player sang tọa độ trong thế giới game và áp dụng sự di chuyển của Camera
            player_new_pos = (player_new_pos[0], 
                              player_new_pos[1])
            # Tạo viên đạn với vị trí đã chuyển đổi
            new_bullet = Bullet(self, player_new_pos)
            new_bullet.size = 100
            new_bullet.surf = pygame.Surface((30, 30))
            new_bullet.surf.fill(White)
            new_bullet.rect = self.surf.get_rect()
            elite_bullets.add(new_bullet)
            all_sprites.add(new_bullet)
            # Đặt lại thời gian giữa các lần bắn đạn
            self.time_since_last_shot = 0
    
    def update(self, player, elite_bullets, all_sprites, clock):
        self.load_sprite(clock)
        player_new_pos = (player.get_position_x(), player.get_position_y())
        self.move(clock, player_new_pos)
        self.fire_bullets(None, clock, player_new_pos, elite_bullets, all_sprites)


class Elite_2(Enemy):
    def __init__(self, player):
        # Initialize base class first
        super(Elite_2, self).__init__(player)
        
        # Elite-specific attributes
        self.base_size = 10  # Base size for elite enemies
        self.size = self.base_size  # Final size after scaling
        self.speed = 5
        self.hp = 500
        self.collide_damage = 20  # Higher damage for elite enemies
        
        # Use the pre-scaled sprites from image_manager
        self.sprite = egoblin_sprite
        if self.sprite and len(self.sprite) > 0:
            # Create a new surface with the correct size
            self.surf = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
            # Scale the sprite to fit our surface size
            sprite_img = pygame.transform.scale(self.sprite[0], (self.size, self.size))
            # Blit the scaled sprite
            self.surf.blit(sprite_img, (0, 0))
        else:
            # Fallback if sprites didn't load
            self.surf = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
            pygame.draw.rect(self.surf, (0, 255, 0), (0, 0, self.size, self.size))
        
        # Update the rect with the new size
        self.rect = self.surf.get_rect()
        
        # Combat attributes
        self.skill_dmg = [10, 20]
        self.normal_bullet_damage = self.skill_dmg[1]
        self.fire_rate = 2  # Time between shots (in seconds)
        self.time_since_last_shot = 0
        self.move_rate = 3  # Time between moves (in seconds)
        self.time_since_last_moved = 0
        self.is_hitted = False
        self.hitted_time = 0
        
        # Set initial position
        self.target_pos = (player.get_position_x(), player.get_position_y())
        self.spawn_radius = 600
        self.generate_random_position(player)
    
    # Override the load_sprite method from the parent class
    def load_sprite(self, clock):
        self.left_or_right()
        
        self.sprite_time += clock.get_time()
        if self.sprite_index >= len(self.sprite):
            self.sprite_index = 0
        
        if self.sprite_time >= 250:
            if self.direction == "right":
                # Scale the sprite to our desired size
                original_sprite = self.sprite[self.sprite_index]
                self.surf = pygame.transform.scale(original_sprite, (self.size, self.size))
            else:
                # For left direction, scale first then flip
                original_sprite = self.sprite[self.sprite_index]
                scaled_sprite = pygame.transform.scale(original_sprite, (self.size, self.size))
                self.surf = pygame.transform.flip(scaled_sprite, True, False)
            
            self.sprite_index += 1
            self.sprite_time = 0
        
    def move(self, clock, player_new_pos):
        self.time_since_last_moved += clock.get_time() / 1000
        
        if self.time_since_last_moved >= self.move_rate:
            # Tính toán hướng vector từ kẻ địch đến người chơi
            self.target_pos = player_new_pos
            self.time_since_last_moved = 0
            
        dx = self.target_pos[0] - self.rect.centerx
        dy = self.target_pos[1] - self.rect.centery
        distance = math.sqrt(dx ** 2 + dy ** 2)
        
        stopping_distance = 10
        if distance > stopping_distance:
            # Chuẩn hóa hướng vector
            if distance != 0:
                dx_normalized = dx / distance
                dy_normalized = dy / distance
            else:
                dx_normalized = 0
                dy_normalized = 0
            # Di chuyển kẻ địch theo hướng vector đã chuẩn hóa
            self.rect.move_ip(dx_normalized * self.speed, dy_normalized * self.speed)
        
    def fire_bullets(self, camera, clock, player_new_pos, elite_bullets, all_sprites):
        # Cập nhật thời gian giữa các lần bắn đạn
        self.time_since_last_shot += clock.get_time() / 1000  # Đổi từ mili-giây sang giây

        # Kiểm tra nếu đủ thời gian để bắn đạn
        if self.time_since_last_shot >= self.fire_rate:
            # Chuyển đổi tọa độ Player sang tọa độ trong thế giới game và áp dụng sự di chuyển của Camera
            player_new_pos = (player_new_pos[0], 
                              player_new_pos[1])
            # Tạo viên đạn với vị trí đã chuyển đổi
            new_bullet = Bullet(self, player_new_pos)
            new_bullet.size = 100
            new_bullet.surf = pygame.Surface((30, 30))
            new_bullet.surf.fill(White)
            new_bullet.rect = self.surf.get_rect()
            elite_bullets.add(new_bullet)
            all_sprites.add(new_bullet)
            # Đặt lại thời gian giữa các lần bắn đạn
            self.time_since_last_shot = 0
    
    def update(self, player, elite_bullets, all_sprites, clock):
        self.load_sprite(clock)
        player_new_pos = (player.get_position_x(), player.get_position_y())
        self.move(clock, player_new_pos)
        self.fire_bullets(None, clock, player_new_pos, elite_bullets, all_sprites)


class Elite_3(Enemy):
    def __init__(self, player):
        # Initialize base class first
        super(Elite_3, self).__init__(player)
        
        # Elite-specific attributes
        self.base_size = 10  # Base size for elite enemies
        self.size = self.base_size  # Final size after scaling
        self.speed = 5
        self.hp = 500
        self.collide_damage = 20  # Higher damage for elite enemies
        
        # Use the pre-scaled sprites from image_manager
        self.sprite = eskeleton_sprite
        if self.sprite and len(self.sprite) > 0:
            # Create a new surface with the correct size
            self.surf = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
            # Scale the sprite to fit our surface size
            sprite_img = pygame.transform.scale(self.sprite[0], (self.size, self.size))
            # Blit the scaled sprite
            self.surf.blit(sprite_img, (0, 0))
        else:
            # Fallback if sprites didn't load
            self.surf = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
            pygame.draw.rect(self.surf, (0, 0, 255), (0, 0, self.size, self.size))
        
        # Update the rect with the new size
        self.rect = self.surf.get_rect()
        
        # Combat attributes
        self.skill_dmg = [10, 20]
        self.normal_bullet_damage = self.skill_dmg[1]
        self.fire_rate = 2  # Time between shots (in seconds)
        self.time_since_last_shot = 0
        self.move_rate = 3  # Time between moves (in seconds)
        self.time_since_last_moved = 0
        self.is_hitted = False
        self.hitted_time = 0
        
        # Set initial position
        self.target_pos = (player.get_position_x(), player.get_position_y())
        self.spawn_radius = 600
        self.generate_random_position(player)
    
    # Override the load_sprite method from the parent class
    def load_sprite(self, clock):
        self.left_or_right()
        
        self.sprite_time += clock.get_time()
        if self.sprite_index >= len(self.sprite):
            self.sprite_index = 0
        
        if self.sprite_time >= 250:
            if self.direction == "right":
                # Scale the sprite to our desired size
                original_sprite = self.sprite[self.sprite_index]
                self.surf = pygame.transform.scale(original_sprite, (self.size, self.size))
            else:
                # For left direction, scale first then flip
                original_sprite = self.sprite[self.sprite_index]
                scaled_sprite = pygame.transform.scale(original_sprite, (self.size, self.size))
                self.surf = pygame.transform.flip(scaled_sprite, True, False)
            
            self.sprite_index += 1
            self.sprite_time = 0
        
    def move(self, clock, player_new_pos):
        self.time_since_last_moved += clock.get_time() / 1000
        
        if self.time_since_last_moved >= self.move_rate:
            # Tính toán hướng vector từ kẻ địch đến người chơi
            self.target_pos = player_new_pos
            self.time_since_last_moved = 0
            
        dx = self.target_pos[0] - self.rect.centerx
        dy = self.target_pos[1] - self.rect.centery
        distance = math.sqrt(dx ** 2 + dy ** 2)
        
        stopping_distance = 10
        if distance > stopping_distance:
            # Chuẩn hóa hướng vector
            if distance != 0:
                dx_normalized = dx / distance
                dy_normalized = dy / distance
            else:
                dx_normalized = 0
                dy_normalized = 0
            # Di chuyển kẻ địch theo hướng vector đã chuẩn hóa
            self.rect.move_ip(dx_normalized * self.speed, dy_normalized * self.speed)
        
    def fire_bullets(self, camera, clock, player_new_pos, elite_bullets, all_sprites):
        # Cập nhật thời gian giữa các lần bắn đạn
        self.time_since_last_shot += clock.get_time() / 1000  # Đổi từ mili-giây sang giây

        # Kiểm tra nếu đủ thời gian để bắn đạn
        if self.time_since_last_shot >= self.fire_rate:
            # Chuyển đổi tọa độ Player sang tọa độ trong thế giới game và áp dụng sự di chuyển của Camera
            player_new_pos = (player_new_pos[0], 
                              player_new_pos[1])
            # Tạo viên đạn với vị trí đã chuyển đổi
            new_bullet = Bullet(self, player_new_pos)
            new_bullet.size = 100
            new_bullet.surf = pygame.Surface((30, 30))
            new_bullet.surf.fill(White)
            new_bullet.rect = self.surf.get_rect()
            elite_bullets.add(new_bullet)
            all_sprites.add(new_bullet)
            # Đặt lại thời gian giữa các lần bắn đạn
            self.time_since_last_shot = 0
    
    def update(self, player, elite_bullets, all_sprites, clock):
        self.load_sprite(clock)
        player_new_pos = (player.get_position_x(), player.get_position_y())
        self.move(clock, player_new_pos)
        self.fire_bullets(None, clock, player_new_pos, elite_bullets, all_sprites)


class Elite_4(Enemy):
    def __init__(self, player):
        # Initialize base class first
        super(Elite_4, self).__init__(player)
        
        # Elite-specific attributes
        self.base_size = 10  # Base size for elite enemies
        self.size = self.base_size  # Final size after scaling
        self.speed = 5
        self.hp = 500
        self.collide_damage = 25  # Higher damage for elite enemies
        
        # Use the pre-scaled sprites from image_manager
        self.sprite = eslime_sprite
        if self.sprite and len(self.sprite) > 0:
            # Create a new surface with the correct size
            self.surf = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
            # Scale the sprite to fit our surface size
            sprite_img = pygame.transform.scale(self.sprite[0], (self.size, self.size))
            # Blit the scaled sprite
            self.surf.blit(sprite_img, (0, 0))
        else:
            # Fallback if sprites didn't load
            self.surf = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
            pygame.draw.rect(self.surf, (255, 255, 0), (0, 0, self.size, self.size))
        
        # Update the rect with the new size
        self.rect = self.surf.get_rect()
        
        # Combat attributes
        self.skill_dmg = [25]  # Single skill with higher damage
        # Fix typo in original code: self.skill_damage -> self.skill_dmg
        self.normal_bullet_damage = self.skill_dmg[0]
        self.fire_rate = 2  # Time between shots (in seconds)
        self.time_since_last_shot = 0
        self.move_rate = 3  # Time between moves (in seconds)
        self.time_since_last_moved = 0
        self.is_hitted = False
        self.hitted_time = 0
        
        # Set initial position
        self.target_pos = (player.get_position_x(), player.get_position_y())
        self.spawn_radius = 600
        self.generate_random_position(player)
    
    # Override the load_sprite method from the parent class
    def load_sprite(self, clock):
        self.left_or_right()
        
        self.sprite_time += clock.get_time()
        if self.sprite_index >= len(self.sprite):
            self.sprite_index = 0
        
        if self.sprite_time >= 250:
            if self.direction == "right":
                # Scale the sprite to our desired size
                original_sprite = self.sprite[self.sprite_index]
                self.surf = pygame.transform.scale(original_sprite, (self.size, self.size))
            else:
                # For left direction, scale first then flip
                original_sprite = self.sprite[self.sprite_index]
                scaled_sprite = pygame.transform.scale(original_sprite, (self.size, self.size))
                self.surf = pygame.transform.flip(scaled_sprite, True, False)
            
            self.sprite_index += 1
            self.sprite_time = 0
        
    def move(self, clock, player_new_pos):
        self.time_since_last_moved += clock.get_time() / 1000
        
        if self.time_since_last_moved >= self.move_rate:
            # Tính toán hướng vector từ kẻ địch đến người chơi
            self.target_pos = player_new_pos
            self.time_since_last_moved = 0
            
        dx = self.target_pos[0] - self.rect.centerx
        dy = self.target_pos[1] - self.rect.centery
        distance = math.sqrt(dx ** 2 + dy ** 2)
        
        stopping_distance = 10
        if distance > stopping_distance:
            # Chuẩn hóa hướng vector
            if distance != 0:
                dx_normalized = dx / distance
                dy_normalized = dy / distance
            else:
                dx_normalized = 0
                dy_normalized = 0
            # Di chuyển kẻ địch theo hướng vector đã chuẩn hóa
            self.rect.move_ip(dx_normalized * self.speed, dy_normalized * self.speed)
        
    def fire_bullets(self, camera, clock, player_new_pos, elite_bullets, all_sprites):
        # Cập nhật thời gian giữa các lần bắn đạn
        self.time_since_last_shot += clock.get_time() / 1000  # Đổi từ mili-giây sang giây

        # Kiểm tra nếu đủ thời gian để bắn đạn
        if self.time_since_last_shot >= self.fire_rate:
            # Chuyển đổi tọa độ Player sang tọa độ trong thế giới game và áp dụng sự di chuyển của Camera
            player_new_pos = (player_new_pos[0], 
                              player_new_pos[1])
            # Tạo viên đạn với vị trí đã chuyển đổi
            new_bullet = Bullet(self, player_new_pos)
            new_bullet.size = 100
            new_bullet.surf = pygame.Surface((30, 30))
            new_bullet.surf.fill(White)
            new_bullet.rect = self.surf.get_rect()
            elite_bullets.add(new_bullet)
            all_sprites.add(new_bullet)
            # Đặt lại thời gian giữa các lần bắn đạn
            self.time_since_last_shot = 0
    
    def update(self, player, elite_bullets, all_sprites, clock):
        self.load_sprite(clock)
        player_new_pos = (player.get_position_x(), player.get_position_y())
        self.move(clock, player_new_pos)
        self.fire_bullets(None, clock, player_new_pos, elite_bullets, all_sprites)
