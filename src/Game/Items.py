import pygame
import math

from DEFINE import *

class ExpItem(pygame.sprite.Sprite):
    def __init__(self, enemy):
        #ExpItem's base attr
        self.size = 10
        self.color = Blue
        self.x = enemy.get_position_x()
        self.y = enemy.get_position_y()
        super(ExpItem, self).__init__()
        
        # ExpItem's surf attr
        self.surf = pygame.Surface((self.size, self.size))
        self.surf.fill(self.color)
        self.rect = self.surf.get_rect(
            center = (
                self.x + enemy.get_size()/2, 
                self.y + enemy.get_size()/2
            )
        )
        
    def update(self):
        self.surf = pygame.Surface((self.size, self.size))
        self.surf.fill(self.color)
        self.rect = self.surf.get_rect(center = self.rect.center)
        
class EnergyItem(pygame.sprite.Sprite):
    # EnergyItem's base attr
    def __init__(self, enemy):
        self.size = 15
        self.color = Lime
        self.x = enemy.get_position_x()
        self.y = enemy.get_position_y()
        super(EnergyItem, self).__init__()

        # EnergyItem's surf attr
        self.surf = pygame.Surface((self.size, self.size))
        self.surf.fill(self.color)
        self.rect = self.surf.get_rect(
            center = (
                self.x + enemy.get_size()/2, 
                self.y + enemy.get_size()/2
            )
        )
        
class Bullet(pygame.sprite.Sprite):
    def __init__(self, current, target):
        # Bullet's base attr
        self.size = 20
        self.color = Yellow
        self.speed = 20
        super(Bullet, self).__init__()
          
        # Bullet's position attr
        self.x = current.get_position_x()
        self.y = current.get_position_y()
        self.dx = 0
        self.dy = 0
        self.dx_normalized = 0
        self.dy_normalized = 0

        # Bullet's target attr
        self.target_x, self.target_y = target
        
        # Bullet's surf attr
        self.surf = pygame.Surface((self.size, self.size))
        self.surf.fill(self.color)
        self.rect = self.surf.get_rect(
            center = (
                current.get_position_x() + current.get_size()/2, 
                current.get_position_y() + current.get_size()/2
            )
        )
    
    def update(self):
        self.surf = pygame.Surface((self.size, self.size))
        self.surf.fill(self.color)
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
        