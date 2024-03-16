import pygame
import random
import math
from pygame.locals import (
    RLEACCEL,
    K_w,
    K_a, 
    K_s, 
    K_d,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

# Init âm thanh, pygame
pygame.mixer.init()
pygame.init()

# Set FPS cho game
FPS = 30

# Screen resolution
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Mã màu
Black = (0,0,0)
White = (255,255,255)
Red	= (255,0,0)
Lime = (0,255,0)
Blue = (0,0,255)
Yellow = (255,255,0)
Cyan = (0,255,255)
Magenta = (255,0,255)
Silver = (192,192,192)
Gray = (128,128,128)
Maroon = (128,0,0)
Olive = (128,128,0)
Green = (0,128,0)
Purple = (128,0,128)
Teal = (0,128,128)
Navy = (0,0,128)

# Định nghĩa các lớp
class Player(pygame.sprite.Sprite):
    # Constructor
    def __init__(self):
        self.player_size = 25
        self.player_color = Red
        self.player_speed = 5
        super(Player, self).__init__()
        
        self.surf = pygame.Surface((self.player_size, self.player_size))
        self.surf.fill(self.player_color)
        self.rect = self.surf.get_rect(
            center = (
                (SCREEN_WIDTH-self.surf.get_width())/2,
                (SCREEN_HEIGHT-self.surf.get_height())/2
            ) 
        )
        
    # Các phương thức set/get
    def set_player_size(self, value):
        self.player_size = value
        
    def get_player_size(self):
        return self.player_size
    
    def set_player_color(self, value):
        self.player_color = value
        
    def get_player_color(self):
        return self.player_color
    
    def set_player_speed(self, value):
        self.player_speed = value
        
    def get_player_speed(self):
        return self.player_speed
        
    # Các phương thức bổ trợ cho Player
    def update(self, pressed_keys):
        self.surf = pygame.Surface((self.player_size, self.player_size))
        self.surf.fill(self.player_color)
        self.rect = self.surf.get_rect(center=self.rect.center)
        
        if pressed_keys[K_w]:
            self.rect.move_ip(0, -self.player_speed)
        if pressed_keys[K_s]:
            self.rect.move_ip(0, self.player_speed)
        if pressed_keys[K_a]:
            self.rect.move_ip(-self.player_speed, 0)
        if pressed_keys[K_d]:
            self.rect.move_ip(self.player_speed, 0)
        
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        self.enemy_size = (20, 10)
        self.enemy_color = White
        self.enemy_speed = 10
        super(Enemy, self).__init__()
        
        self.surf = pygame.Surface(self.enemy_size)
        self.surf.fill(self.enemy_color)
        self.rect = self.surf.get_rect(
            center = (
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )
        
    def set_enemy_size(self, value):
        self.enemy_size = value
        
    def get_enemy_size(self):
        return self.enemy_size
    
    def set_enemy_color(self, value):
        self.enemy_color = value
        
    def get_enemy_color(self):
        return self.enemy_color
    
    def set_enemy_speed(self, value):
        self.enemy_speed = value
        
    def get_enemy_speed(self):
        return self.enemy_speed
    # Move the sprite based on speed
    # Remove the sprite when it passes the left edge of the screen
    def update(self):
        self.surf = pygame.Surface(self.enemy_size)
        self.surf.fill(self.enemy_color)
        
        self.rect.move_ip(-self.enemy_speed, 0)
        if self.rect.right < 0:
            self.kill()


if __name__ == '__main__':
    clock = pygame.time.Clock()
    
    # Tạo màn hình trò chơi và set tên cửa sổ
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption('A 2D NORMAL SHOOTING GAME')
    
    # Tạo sự kiện
    ADDENEMY = pygame.USEREVENT + 1
    pygame.time.set_timer(ADDENEMY, 250)
    
    # Tạo ra 1 thằng "Người chơi"
    player = Player()
    
    # Create groups to hold enemy sprites and all sprites
    # - enemies is used for collision detection and position updates
    # - all_sprites is used for rendering
    enemies = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)
    
    # Gameplay chạy trong này
    running = True
    while running:
        pressed_keys = pygame.key.get_pressed()
        clicked_mouse = pygame.mouse.get_pressed()
        
        screen.fill(Black)
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                    
            elif event.type == QUIT:
                running = False
                
             # Add a new enemy?
            elif event.type == ADDENEMY:
                # Create the new enemy and add it to sprite groups
                new_enemy = Enemy()
                enemies.add(new_enemy)
                all_sprites.add(new_enemy)
                
        player.update(pressed_keys)
        enemies.update()
        
        for entity in all_sprites:
            screen.blit(entity.surf, entity.rect)        
        screen.blit(player.surf, player.rect)
        
        # Kiểm tra xem enemy đụng vào người chơi chưa
        if pygame.sprite.spritecollideany(player, enemies):
            player.set_player_size(player.get_player_size() + 1)
            if (player.get_player_size() >= SCREEN_HEIGHT):
                player.kill()
                running = False
            
            
        
        pygame.display.update()
        
        clock.tick(FPS)
    
    pygame.quit()  
