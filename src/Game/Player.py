import pygame
import math

from DEFINE import *
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
        self.speed = 5
        self.exp = 0
        super(Player, self).__init__()
        
        # Player's health attr 
        self.current_health = 1000
        self.maximum_health = 1000
        self.health_bar_length = 300
        self.health_ratio = self.maximum_health / self.health_bar_length
        self.target_health = 500
        self.hp = self.target_health
        self.health_change_speed = 5
        
        # Player's energy attr 
        self.current_energy = 100
        self.maximum_energy = 100
        self.energy_bar_length = 200
        self.energy_ratio = self.maximum_energy / self.energy_bar_length
        self.target_energy = 10
        self.energy = self.target_energy
        self.energy_change_speed = 1
        
        # Player's exp attr 
        self.current_exp = 100
        self.maximum_exp = 100
        self.exp_bar_length = 200
        self.exp_ratio = self.maximum_exp / self.exp_bar_length
        self.exp = 10
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
        if self.current_health > 0:
            self.current_health -= amount
        if self.current_health <= 0:
            self.current_health = 0
    
    def basic_health(self):
        pygame.draw.rect(SCREEN, (255,0,0), (10,10,self.current_health/self.health_ratio,25))
        pygame.draw.rect(SCREEN, (255,255,255), (10,10,self.health_bar_length,25), 4)
        
    def advanced_health(self):
        transition_width = 0
        transition_color = (255,0,0)
        
        if self.current_health < self.target_health:
            self.current_health += self.health_change_speed
            transition_width = int((self.target_health - self.current_health)/self.health_ratio)
            transition_color = (0,255,0)
        if self.current_health > self.target_health:
            self.current_health -= self.health_change_speed
            transition_width = int((self.target_health - self.current_health)/self.health_ratio)
            transition_color = (255,255,0)
            
        health_bar_rect = pygame.Rect(10,10,self.current_health/self.health_ratio,25)
        transition_bar_rect = pygame.Rect(health_bar_rect.right,10,transition_width,25)
        
        pygame.draw.rect(SCREEN, (255,0,0), health_bar_rect)
        pygame.draw.rect(SCREEN, transition_color, transition_bar_rect)
        pygame.draw.rect(SCREEN, (255,255,255), (10,10,self.health_bar_length,25), 4)
        
    def advanced_energy(self):
        transition_width = 0
        transition_color = (255,0,0)
        
        if self.current_energy < self.target_energy:
            self.current_energy += self.energy_change_speed
            transition_width = int((self.target_energy - self.current_energy)/self.energy_ratio)
            transition_color = (0,255,0)
        if self.current_energy > self.target_energy:
            self.current_energy -= self.energy_change_speed
            transition_width = int((self.target_energy - self.current_energy)/self.energy_ratio)
            transition_color = (255,255,0)
            
        energy_bar_rect = pygame.Rect(10,32,self.current_energy/self.energy_ratio,20)
        transition_bar_rect = pygame.Rect(energy_bar_rect.right,32,transition_width,20)
        
        pygame.draw.rect(SCREEN, (0,0,255), energy_bar_rect)
        pygame.draw.rect(SCREEN, transition_color, transition_bar_rect)
        pygame.draw.rect(SCREEN, (255,255,255), (10,32,self.energy_bar_length,20), 4)
                
    def update_player(self):
        self.surf = pygame.Surface((self.size, self.size))
        self.surf.fill(self.color)
        self.rect = self.surf.get_rect(center = self.rect.center)
            
    # Hàm cập nhật trạng thái Player
    def update(self, pressed_keys):
        self.update_player()
        
        # Health_bar
        # self.basic_health()
        self.advanced_health()
        self.advanced_energy()
        
        # Movement
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
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            
