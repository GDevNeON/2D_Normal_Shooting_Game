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
        self.size = 20  # Standardized base size for normal enemies
        self.speed = 1.5
        self.health = 20
        self.collide_damage = 10
        self.normal_bullet_damage = 10
        self.damage_buff = 0  # Initialize damage buff to 0
        self.is_hit = False
        self.hit_time = 0

        # Enemy's surf attr
        self.sprite = None
        self.surf = pygame.Surface((self.size, self.size))
        self.rect = self.surf.get_rect()
        self.sprite_time = 0
        self.sprite_index = 0
        self.old_x = self.get_position_x()
        self.direction = "right"
        
        # Tính toán vị trí ngẫu nhiên xung quanh người chơi
        self.spawn_radius = 1000
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
        
    def load_sprite(self, clock):
        self.left_or_right()
        
        self.sprite_time += clock.get_time()
        if self.sprite_index == len(self.sprite):
            self.sprite_index = 0
        
        if self.sprite_time >= 250:
            if self.direction == "right":
                self.surf = self.sprite[self.sprite_index]
            else:
                reverse = pygame.transform.flip(self.sprite[self.sprite_index], True, False)
                self.surf = reverse
            self.sprite_index += 1
            self.sprite_time = 0
        
    def generate_random_position(self, player):
        # Tạo một vị trí ngẫu nhiên xung quanh người chơi
        angle = random.uniform(0, 2 * math.pi)
        random_x = player.get_position_x() + self.spawn_radius * math.cos(angle)
        random_y = player.get_position_y() + self.spawn_radius * math.sin(angle)
        # Cập nhật vị trí của kẻ địch
        self.rect.center = (random_x, random_y)

    def move_towards_player(self, player):
        # Tính toán hướng vector từ kẻ địch đến người chơi
        dx = player.get_position_x() - self.rect.centerx
        dy = player.get_position_y() - self.rect.centery
        distance = math.sqrt(dx ** 2 + dy ** 2)
        # Chuẩn hóa hướng vector
        if distance != 0:
            dx_normalized = dx / distance
            dy_normalized = dy / distance
        else:
            dx_normalized = 0
            dy_normalized = 0
        # Di chuyển kẻ địch theo hướng vector đã chuẩn hóa
        self.rect.move_ip(dx_normalized * self.speed, dy_normalized * self.speed)
        
    # Hàm cập nhật trạng thái Enemy
    def update(self, player):
        self.move_towards_player(player)


# Derived class
class Normal(Enemy):
    def __init__(self, player):
        super(Normal, self).__init__(player)
        
        rand = random.randint(0, 3)
        if rand == 0:
            self.sprite = ghost_sprite
            self.surf = ghost_sprite[0]
        elif rand == 1:
            self.sprite = goblin_sprite
            self.surf = goblin_sprite[0]
        elif rand == 2:
            self.sprite = skeleton_sprite
            self.surf = skeleton_sprite[0]
        else:
            self.sprite = slime_sprite
            self.surf = slime_sprite[0]
        
    def update(self, player, player_bullets, all_sprites, clock):
        self.load_sprite(clock)
        self.move_towards_player(player)