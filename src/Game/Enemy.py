import pygame
import math
import random

from DEFINE import *
from Items import *

class Enemy(pygame.sprite.Sprite):
    def __init__(self, player_rect):
        # Enemy's base attr
        self.size = 20
        self.color = White
        self.speed = 1.5
        super(Enemy, self).__init__()

        # Enemy's surf attr
        self.surf = pygame.Surface((self.size, self.size))
        self.surf.fill(self.color)
        self.rect = self.surf.get_rect()
        
        # Tính toán vị trí ngẫu nhiên xung quanh người chơi
        self.generate_random_position(player_rect)
        
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
    def generate_random_position(self, player_rect):
        # Bán kính của vùng phát sinh ngẫu nhiên
        radius = 350
        # Tạo một vị trí ngẫu nhiên xung quanh người chơi
        angle = random.uniform(0, 2 * math.pi)
        random_x = player_rect.centerx + radius * math.cos(angle)
        random_y = player_rect.centery + radius * math.sin(angle)
        # Cập nhật vị trí của kẻ địch
        self.rect.center = (random_x, random_y)
    
    def update_enemy(self):
        self.surf = pygame.Surface((self.size, self.size))
        self.surf.fill(self.color)
        self.rect = self.surf.get_rect(center = self.rect.center)
        
    # Hàm cập nhật trạng thái Enemy
    def update(self, player_rect):
        self.update_enemy()

        # Tính toán hướng vector từ kẻ địch đến người chơi
        dx = player_rect.centerx - self.rect.centerx
        dy = player_rect.centery - self.rect.centery
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
        
# 3 types of Elite enemies
class Elite_1(pygame.sprite.Sprite):
    def __init__(self, player):
        self.size = 100
        self.color = Purple
        self.speed = 15
        self.hp = 10000
        self.shoot_flag = 0
        super(Elite_1, self).__init__()
        
        self.surf = pygame.Surface((self.size, self.size))
        self.surf.fill(self.color)
        self.rect = self.surf.get_rect()
        
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
            
    def generate_random_position(self, player):
        # Bán kính của vùng phát sinh ngẫu nhiên
        radius = 500
        # Tạo một vị trí ngẫu nhiên xung quanh người chơi
        angle = random.uniform(0, 2 * math.pi)
        random_x = player.get_position_x() + radius * math.cos(angle)
        random_y = player.get_position_y() + radius * math.sin(angle)
        # Cập nhật vị trí của kẻ địch
        self.rect.center = (random_x, random_y)
        
    def move(self, player_new_pos):
        # Tính toán hướng vector từ kẻ địch đến người chơi
        dx = player_new_pos[0] - self.rect.centerx
        dy = player_new_pos[1] - self.rect.centery
        distance = math.sqrt(dx ** 2 + dy ** 2)
        # Chuẩn hóa hướng vector
        if distance != 0:
            dx_normalized = dx / distance
            dy_normalized = dy / distance
        else:
            dx_normalized = 0
            dy_normalized = 0
        # Di chuyển kẻ địch theo hướng vector đã chuẩn hóa
        if float(self.rect.centerx) != float(player_new_pos[0]) and float(self.rect.centery) != float(player_new_pos[1]):
            self.rect.move_ip(dx_normalized * self.speed, dy_normalized * self.speed)
        
    def shoot(self, player_new_pos, elite_bullets, all_sprites):
        bullet = Bullet(self, player_new_pos)
        bullet.size = 200
        elite_bullets.add(bullet)
        all_sprites.add(bullet)
    
    def update(self, player_new_pos, elite_bullets, all_sprites):
        self.move(player_new_pos)
        if self.shoot_flag % 4 == 0:
            self.shoot(player_new_pos, elite_bullets, all_sprites)
            self.shoot_flag += 1
