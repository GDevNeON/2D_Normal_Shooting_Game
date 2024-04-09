import pygame
import math
import os

from DEFINE import *

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
        #ExpItem's base attr
        self.image = pygame.image.load("C:\\Users\\Admin\\Downloads\\2D_Normal_Shooting_Game-main (2)\\2D_Normal_Shooting_Game-main\\src\\Game\\item_exp.png").convert()
        self.image.set_colorkey((255, 255, 255), RLEACCEL)
        self.size = self.image.get_size()
        # create a 2x bigger image than self.image
        self.bigger_img = pygame.transform.scale(self.image, (int(self.size[0]*2), int(self.size[1]*2)))
        # draw bigger image to screen at x=100 y=100 position
        self.surf = self.bigger_img
        
        # ExpItem's surf attr
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
        # EnergyItem's base attr
        self.size = 15
        self.color = Blue

        # EnergyItem's surf attr
        self.surf = pygame.Surface((self.size, self.size))
        self.surf.fill(self.color)
        self.rect = self.surf.get_rect(
            center = (
                self.x + enemy.get_size()/2, 
                self.y + enemy.get_size()/2
            )
        )
        
class HpItem(Items):
    def __init__(self, enemy):
        super(HpItem, self).__init__(enemy)
        # HpItem's base attr
        self.size = 17
        self.color = Red

        # HpItem's surf attr
        self.surf = pygame.Surface((self.size, self.size))
        self.surf.fill(self.color)
        self.rect = self.surf.get_rect(
            center = (
                self.x + enemy.get_size()/2, 
                self.y + enemy.get_size()/2
            )
        )
        
class Bullet(pygame.sprite.Sprite):
    file_path = os.path('.','player_bullet.png')
    def __init__(self, current, target):
        super(Bullet, self).__init__()
        # Bullet's base attr
        self.size = 20
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
        self.image = pygame.image.load(file_path).convert()
        self.image.set_colorkey((255, 255, 255), RLEACCEL)
        self.size = self.image.get_size()
        # create a 2x bigger image than self.image
        self.bigger_img = pygame.transform.scale(self.image, (int(self.size[0]*2), int(self.size[1]*2)))
        # draw bigger image to screen at x=100 y=100 position
        self.surf = self.bigger_img
        self.surf.fill(self.color)
        self.rect = self.surf.get_rect(
            center = (
                current.get_position_x(),
                current.get_position_y()
            )
        )
    
    def update(self):
        self.surf = pygame.Surface((self.size, self.size))
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
        
