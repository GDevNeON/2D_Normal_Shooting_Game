import pygame
import math

from DEFINE import *
from Items import *
from pygame.locals import (
    K_w,
    K_a, 
    K_s, 
    K_d,
)

class Player(pygame.sprite.Sprite):
    # Constructor
    def __init__(self):
        # Player's base attr
        self.size = 25
        self.color = Red
        self.speed = 4
        super(Player, self).__init__()
        
        # Player's health attr 
        self.bar_current_health = 100
        self.bar_maximum_health = 100
        self.health_bar_length = 300
        self.health_ratio = self.bar_maximum_health / self.health_bar_length
        self.health = 100
        self.health_change_speed = 5
        
        # Player's energy attr 
        self.bar_current_energy = 100
        self.bar_maximum_energy = 100
        self.energy_bar_length = 200
        self.energy_ratio = self.bar_maximum_energy / self.energy_bar_length
        self.energy = 0
        self.energy_change_speed = 1
        
        # Player's exp attr 
        self.bar_current_exp = 100
        self.bar_maximum_exp = 100
        self.exp_bar_length = 500
        self.exp_ratio = self.bar_maximum_exp / self.exp_bar_length
        self.exp = 0
        self.exp_change_speed = 1
        
        # Player's surf attr
        self.surf = pygame.Surface((self.size, self.size))
        self.surf.fill(self.color)
        self.rect = self.surf.get_rect(
            center = (
                (SCREEN_WIDTH-self.surf.get_width())/2,
                (SCREEN_HEIGHT-self.surf.get_height())/2
            ) 
        )
        
        # Other player's attr
        self.level = 1
        self.fire_rate = 0.1  # Thời gian giữa các lần bắn đạn (tính bằng giây)
        self.time_since_last_shot = 0  # Thời gian đã trôi qua kể từ lần bắn đạn cuối cùng
        
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
    
    # Các hàm phụ cho Player
    def get_damage(self, amount):
        if self.bar_current_health > 0:
            self.bar_current_health -= amount
        if self.bar_current_health <= 0:
            self.bar_current_health = 0
    
    def basic_health(self):
        pygame.draw.rect(SCREEN, (255,0,0), (10,10,self.bar_current_health/self.health_ratio,25))
        pygame.draw.rect(SCREEN, (255,255,255), (10,10,self.health_bar_length,25), 4)
        
    def advanced_health(self):
        transition_width = 0
        transition_color = (255,0,0)
        
        if self.bar_current_health < self.health:
            self.bar_current_health += self.health_change_speed
            transition_width = int((self.health - self.bar_current_health)/self.health_ratio)
            transition_color = (0,255,0)
        if self.bar_current_health > self.health:
            self.bar_current_health -= self.health_change_speed
            transition_width = int((self.health - self.bar_current_health)/self.health_ratio)
            transition_color = (255,255,0)
            
        health_bar_rect = pygame.Rect(10,10,self.bar_current_health/self.health_ratio,25)
        transition_bar_rect = pygame.Rect(health_bar_rect.right,10,transition_width,25)
        
        pygame.draw.rect(SCREEN, (255,0,0), health_bar_rect)
        pygame.draw.rect(SCREEN, transition_color, transition_bar_rect)
        pygame.draw.rect(SCREEN, (255,255,255), (10,10,self.health_bar_length,25), 3)
        
    def advanced_energy(self):
        transition_width = 0
        transition_color = (255,0,0)
        
        if self.bar_current_energy < self.energy:
            self.bar_current_energy += self.energy_change_speed
            transition_width = int((self.energy - self.bar_current_energy)/self.energy_ratio)
            transition_color = (0,255,0)
        if self.bar_current_energy > self.energy:
            self.bar_current_energy -= self.energy_change_speed
            transition_width = int((self.energy - self.bar_current_energy)/self.energy_ratio)
            transition_color = (255,255,0)
            
        energy_bar_rect = pygame.Rect(10,32,self.bar_current_energy/self.energy_ratio,20)
        transition_bar_rect = pygame.Rect(energy_bar_rect.right,32,transition_width,20)
        
        pygame.draw.rect(SCREEN, (0,0,255), energy_bar_rect)
        pygame.draw.rect(SCREEN, transition_color, transition_bar_rect)
        pygame.draw.rect(SCREEN, (255,255,255), (10,32,self.energy_bar_length,20), 3)
        
    def advanced_exp(self):
        transition_width = 0
        transition_color = (255,0,0)
        
        if self.bar_current_exp < self.exp:
            self.bar_current_exp += self.exp_change_speed
            transition_width = int((self.exp - self.bar_current_exp)/self.exp_ratio)
            transition_color = Yellow
        if self.bar_current_exp > self.exp:
            self.bar_current_exp -= self.exp_change_speed
            transition_width = int((self.exp - self.bar_current_exp)/self.exp_ratio)
            transition_color = (255,255,0)
            
        exp_bar_rect = pygame.Rect(400,670,self.bar_current_exp/self.exp_ratio,15)
        transition_bar_rect = pygame.Rect(exp_bar_rect.right,670,transition_width,15)
        
        pygame.draw.rect(SCREEN, (0,255,0), exp_bar_rect)
        pygame.draw.rect(SCREEN, transition_color, transition_bar_rect)
        pygame.draw.rect(SCREEN, (255,255,255), (400,670,self.exp_bar_length,15), 2)
        
    def fire_bullets(self, camera, clock, player_bullets, all_sprites):
        # Cập nhật thời gian giữa các lần bắn đạn
        self.time_since_last_shot += clock.get_time() / 1000  # Đổi từ mili-giây sang giây

        # Kiểm tra nếu đủ thời gian để bắn đạn
        if self.time_since_last_shot >= self.fire_rate:
            # Lấy tọa độ chuột trên màn hình
            mouse = pygame.mouse.get_pos()
            # Chuyển đổi tọa độ chuột sang tọa độ trong thế giới game và áp dụng sự di chuyển của Camera
            mouse_world_pos = (mouse[0] - camera.camera.x, mouse[1] - camera.camera.y)
            # Tạo viên đạn với vị trí đã chuyển đổi
            new_bullet = Bullet(self, mouse_world_pos)
            player_bullets.add(new_bullet)
            all_sprites.add(new_bullet)
            # Đặt lại thời gian giữa các lần bắn đạn
            self.time_since_last_shot = 0  
        
    def level_up(self):
        if self.exp >= self.bar_maximum_exp:
            self.exp = math.fabs(self.exp - self.bar_maximum_exp)
            self.bar_current_exp = 0.2*self.bar_current_exp
            self.level += 1
            print('Player lv ', self.level)
            
    def movement(self, pressed_keys):
        if pressed_keys[K_w]:
            self.rect.move_ip(0, -self.speed)
        if pressed_keys[K_s]:
            self.rect.move_ip(0, self.speed)
        if pressed_keys[K_a]:
            self.rect.move_ip(-self.speed, 0)
        if pressed_keys[K_d]:
            self.rect.move_ip(self.speed, 0)
        
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > LEVEL_WIDTH:
            self.rect.right = LEVEL_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= LEVEL_HEIGHT:
            self.rect.bottom = LEVEL_HEIGHT
                
    def update_player(self):
        self.surf = pygame.Surface((self.size, self.size))
        self.surf.fill(self.color)
        self.rect = self.surf.get_rect(center = self.rect.center)
            
    # Hàm cập nhật trạng thái Player
    def update(self, clock, camera, pressed_keys, player_bullets, all_sprites):
        # self.basic_health()
        self.advanced_health()
        self.advanced_energy()
        self.advanced_exp()
        self.fire_bullets(camera, clock, player_bullets, all_sprites)
        self.level_up()
        self.movement(pressed_keys)
        self.update_player()
        
            
