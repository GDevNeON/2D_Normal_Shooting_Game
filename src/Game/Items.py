import pygame
import math

from DEFINE import *

class ExpItem(pygame.sprite.Sprite):
    def __init__(self):
        #ExpItem's base attr
        self.size = 10
        self.color = Blue
        super(ExpItem, self).__init__()
        
        

class Bullet(pygame.sprite.Sprite):
    def __init__(self, player, mouse):
        # Bullet's base attr
        self.size = 20
        self.color = Yellow
        self.speed = 20
        super(Bullet, self).__init__()
          
        # Bullet's position attr
        self.x = player.get_player_position_x()
        self.y = player.get_player_position_y()
        self.dx = 0
        self.dy = 0
        self.dx_normalized = 0
        self.dy_normalized = 0

        # Bullet's target attr
        self.target_x, self.target_y = mouse
        
        # Bullet's surf attr
        self.surf = pygame.Surface((self.size, self.size))
        self.surf.fill(self.color)
        self.rect = self.surf.get_rect(
            center = (
                player.get_player_position_x() + player.get_player_size()/2, 
                player.get_player_position_y() + player.get_player_size()/2
            )
        )
            
    def update_bullets(self):
        self.surf = pygame.Surface((self.size, self.size))
        self.surf.fill(self.color)
        self.rect = self.surf.get_rect(center = self.rect.center)
        
    def update(self, player, enemies):
        self.update_bullets()

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

        # Xóa đạn khi ra khỏi màn hình hoặc va chạm với kẻ địch
        if (0 < self.rect.x < SCREEN_WIDTH) or (0 < self.rect.y < SCREEN_HEIGHT):
            for enemy in enemies:
                if pygame.sprite.collide_rect(self, enemy):
                    self.kill()
                    enemy.kill()
                    break
        