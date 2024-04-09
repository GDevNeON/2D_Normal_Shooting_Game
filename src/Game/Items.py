import pygame
import math
import os

from DEFINE import *
from pathlib import Path

cwd = Path.cwd()
mod_path = Path(__file__).parent
exp = "../../Sprites/Players/exp_item.png"
energy = "../../Sprites/Players/energy_item.png"
hp = "../../Sprites/Players/hp_item.png"
bullet_player = "../../Sprites/Players/player_bullet.png"
exp_sprite              = (mod_path / exp).resolve()
energy_sprite           = (mod_path / energy).resolve()
hp_sprite               = (mod_path / hp).resolve()
player_bullet_sprite    = (mod_path / bullet_player).resolve()
# Base class
class Items(pygame.sprite.Sprite):
    def __init__(self, target):
        super(Items, self).__init__()
        self.size = 0
        self.x = target.get_position_x()
        self.y = target.get_position_y()

# Derived class
class ExpItem(Items):
    def __init__(self, enemy):
        super(ExpItem, self).__init__(enemy)
        # ExpItem's surf attr
        self.image = pygame.image.load(exp_sprite).convert()
        self.image.set_colorkey(White, RLEACCEL)
        self.size = self.image.get_size()
        # create a 2x bigger image than self.image
        self.bigger_img = pygame.transform.scale(self.image, (int(self.size[0]*2), int(self.size[1]*2)))
        self.surf = self.bigger_img
        self.rect = self.surf.get_rect(
            center = (
                self.x + enemy.get_size()/2, 
                self.y + enemy.get_size()/2
            )
        )
        
    def update(self):
        self.rect = self.surf.get_rect(center = self.rect.center)
        
class EnergyItem(Items):
    def __init__(self, enemy):
        super(EnergyItem, self).__init__(enemy)
        # EnergyItem's surf attr
        self.image = pygame.image.load(energy_sprite).convert()
        self.image.set_colorkey(White, RLEACCEL)
        self.size = self.image.get_size()
        # create a 2x bigger image than self.image
        self.bigger_img = pygame.transform.scale(self.image, (int(self.size[0]*2), int(self.size[1]*2)))
        self.surf = self.bigger_img
        self.rect = self.surf.get_rect(
            center = (
                self.x + enemy.get_size()/2, 
                self.y + enemy.get_size()/2
            )
        )
        
class HpItem(Items):
    def __init__(self, enemy):
        super(HpItem, self).__init__(enemy)
        # HpItem's surf attr
        self.image = pygame.image.load(hp_sprite).convert()
        self.image.set_colorkey(White, RLEACCEL)
        self.size = self.image.get_size()
        # create a 2x bigger image than self.image
        self.bigger_img = pygame.transform.scale(self.image, (int(self.size[0]*2), int(self.size[1]*2)))
        self.surf = self.bigger_img
        self.rect = self.surf.get_rect(
            center = (
                self.x + enemy.get_size()/2, 
                self.y + enemy.get_size()/2
            )
        )
        
class Bullet(pygame.sprite.Sprite):
    def __init__(self, current, target):
        super(Bullet, self).__init__()
        # Bullet's base attr
        self.speed = 20
        self.damage = 100
          
        # Bullet's position attr
        self.x = current.get_position_x()
        self.y = current.get_position_y()
        self.dx = 0
        self.dy = 0
        self.dx_normalized = 0
        self.dy_normalized = 0
        self.distance = 0
        self.distance_limit = 400

        # Bullet's target attr
        self.target_x, self.target_y = target
        
        # Bullet's surf attr
        self.image = pygame.image.load(player_bullet_sprite).convert()
        self.image.set_colorkey(White, RLEACCEL)
        self.size = self.image.get_size()
        # create a 2x bigger image than self.image
        self.bigger_img = pygame.transform.scale(self.image, (int(self.size[0]*5), int(self.size[1]*5)))
        self.surf = self.bigger_img
        self.rect = self.surf.get_rect(
            center = (
                current.get_position_x(),
                current.get_position_y()
            )
        )
    
    def update(self):
        self.rect = self.surf.get_rect(center = self.rect.center)

        self.dx = self.target_x - self.x
        self.dy = self.target_y - self.y
        distance = math.sqrt(self.dx ** 2 + self.dy ** 2)

        if distance != 0:
            self.dx_normalized = self.dx / distance
            self.dy_normalized = self.dy / distance
        else:
            self.dx_normalized = 0
            self.dy_normalized = 0

        self.rect.move_ip(self.dx_normalized * self.speed, self.dy_normalized * self.speed)    
        self.distance = math.sqrt((self.rect.centerx - self.x)**2 + (self.rect.centery - self.y)**2)
        if self.distance > self.distance_limit:
            self.kill()
        
