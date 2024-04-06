import pygame
import math
import random

from DEFINE import *
from Items import *

# Base class
class Enemy(pygame.sprite.Sprite):
    def __init__(self, player):
        super(Enemy, self).__init__()
        # Enemy's base attr
        self.size = 20
        self.color = White
        self.speed = 1.5
        self.health = 10

        # Enemy's surf attr
        self.surf = pygame.Surface((self.size, self.size))
        self.surf.fill(self.color)
        self.rect = self.surf.get_rect()
        
        # Tính toán vị trí ngẫu nhiên xung quanh người chơi
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
    
    def set_color(self, value):
        self.color = value
        
    def get_color(self):
        return self.color
    
    def set_speed(self, value):
        self.speed = value
        
    def get_speed(self):
        return self.speed
    
    # Các hàm phụ cho lớp Enemy
    def generate_random_position(self, player):
        # Bán kính của vùng phát sinh ngẫu nhiên
        radius = 350
        # Tạo một vị trí ngẫu nhiên xung quanh người chơi
        angle = random.uniform(0, 2 * math.pi)
        random_x = player.get_position_x() + radius * math.cos(angle)
        random_y = player.get_position_y() + radius * math.sin(angle)
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

class Elite_1(Enemy):
    def __init__(self, player):
        super(Elite_1, self).__init__(player)
        self.size = 100
        self.color = Purple
        self.speed = 20
        self.hp = 1000
        
        self.surf = pygame.Surface((self.size, self.size))
        self.surf.fill(self.color)
        self.rect = self.surf.get_rect()
        
        self.target_pos = (player.get_position_x(), player.get_position_y())
        
        self.fire_rate = 2  # Thời gian giữa các lần bắn đạn (tính bằng giây)
        self.time_since_last_shot = 0  # Thời gian đã trôi qua kể từ lần bắn đạn cuối cùng
        self.move_rate = 3  # Thời gian giữa các lần di chuyển (tính bằng giây)
        self.time_since_last_moved = 0
        
        self.generate_random_position(player)

    def generate_random_position(self, player):
        # Bán kính của vùng phát sinh ngẫu nhiên
        radius = 500
        # Tạo một vị trí ngẫu nhiên xung quanh người chơi
        angle = random.uniform(0, 2 * math.pi)
        random_x = player.get_position_x() + radius * math.cos(angle)
        random_y = player.get_position_y() + radius * math.sin(angle)
        # Cập nhật vị trí của kẻ địch
        self.rect.center = (random_x, random_y)
        
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
            elite_bullets.add(new_bullet)
            all_sprites.add(new_bullet)
            # Đặt lại thời gian giữa các lần bắn đạn
            self.time_since_last_shot = 0
    
    def update(self, camera, clock, player_new_pos, elite_bullets, all_sprites):
        self.move(clock, player_new_pos)
        self.fire_bullets(camera, clock, player_new_pos, elite_bullets, all_sprites)
               
