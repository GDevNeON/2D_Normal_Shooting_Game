import pygame
import math

from ..core.define import *
from ..managers.image_manager import *

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
        self.image = exp_sprite
        # set_colorkey được dùng để làm cho vùng màu trên sprite trùng với màu đc truyền vào hàm trở thành trong suốt
        self.image.set_colorkey(White)
        self.size = self.image.get_size()
        self.size_ratio = 4.5
        self.smaller_img = pygame.transform.scale(self.image, (int(self.size[0]/self.size_ratio), int(self.size[1]/self.size_ratio)))
        self.surf = self.smaller_img
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
        self.image = energy_sprite
        self.image.set_colorkey(White)
        self.size = self.image.get_size()
        self.size_ratio = 4.5
        self.smaller_img = pygame.transform.scale(self.image, (int(self.size[0]/self.size_ratio), int(self.size[1]/self.size_ratio)))
        self.surf = self.smaller_img
        self.rect = self.surf.get_rect(
            center = (
                self.x + enemy.get_size()/2, 
                self.y + enemy.get_size()/2
            )
        )
        
    def update(self):
        self.rect = self.surf.get_rect(center = self.rect.center)
        
class HpItem(Items):
    def __init__(self, enemy):
        super(HpItem, self).__init__(enemy)
        # HpItem's surf attr
        self.image = hp_sprite
        self.image.set_colorkey(White)
        self.size = self.image.get_size()
        self.size_ratio = 5
        self.smaller_img = pygame.transform.scale(self.image, (int(self.size[0]/self.size_ratio), int(self.size[1]/self.size_ratio)))
        self.surf = self.smaller_img
        self.rect = self.surf.get_rect(
            center = (
                self.x + enemy.get_size()/2, 
                self.y + enemy.get_size()/2
            )
        )
        
    def update(self):
        self.rect = self.surf.get_rect(center = self.rect.center)
        
class Bullet(pygame.sprite.Sprite):
    def __init__(self, current, target):
        super(Bullet, self).__init__()
        # Bullet's base attr
        self.speed = 20
        # Set up sát thương của đạn dựa trên sát thương của người bắn
        self.damage = current.normal_bullet_damage * (1 + current.damage_buff / 100)  # Apply damage buff
          
        # Bullet's position attr
        self.x = current.get_position_x()
        self.y = current.get_position_y()
        self.dx = 0
        self.dy = 0
        self.dx_normalized = 0
        self.dy_normalized = 0

        # Bullet's fire range attr
        self.distance = 0
        self.distance_limit = 1000  # Increased default range

        # Bullet's target attr
        self.target_x, self.target_y = target

        def angle(self):
            vector_to_mouse = pygame.math.Vector2(self.target_x - self.x, self.target_y - self.y)
            angle_to_mouse = math.degrees(math.atan2(*vector_to_mouse)) - 90
            return angle_to_mouse
        
        # Bullet's surf attr
        self.image = player_bullet_sprite
        self.image = pygame.transform.rotate(self.image, angle(self))
        self.image.set_colorkey(White, RLEACCEL)
        
        # Apply bullet size buff
        self.size = self.image.get_size()
        self.size_ratio = 2 * (1 - current.bullet_size_buff / 200)  # Smaller ratio = bigger bullet
        self.size_ratio = max(0.5, self.size_ratio)  # Prevent negative or zero size
        
        self.smaller_img = pygame.transform.scale(
            self.image, 
            (
                int(self.size[0] / self.size_ratio), 
                int(self.size[1] / self.size_ratio)
            )
        )
        
        self.surf = self.smaller_img
        self.rect = self.surf.get_rect(
            center=(
                current.get_position_x(),
                current.get_position_y()
            )
        )
        
        # Increase damage based on size buff (bigger bullets do more damage)
        size_damage_multiplier = 1 + (current.bullet_size_buff / 200)  # Up to 1.5x damage at max buff
        self.damage = int(self.damage * size_damage_multiplier)
    
    def update(self, camera=None):
        """
        Update bullet position.
        The camera parameter is accepted for compatibility with Pygame's sprite group update calls,
        but it's not used in the actual bullet movement calculation.
        """
        self.rect = self.surf.get_rect(center=self.rect.center)

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
