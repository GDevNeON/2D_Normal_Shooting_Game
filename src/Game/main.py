import pygame

from DEFINE import *
from Player import *
from Enemy import *
from Items import *
from Collision import *
from pygame.locals import (
    RLEACCEL,
    USEREVENT,
    FULLSCREEN,
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


if __name__ == '__main__':
    clock = pygame.time.Clock()
    
    pygame.display.set_caption('A 2D NORMAL SHOOTING GAME')
    
    enemies = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    exp_items = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    
    # Tạo ra 1 object
    player = Player()
    all_sprites.add(player)
    enemy = Enemy(player.rect)
    enemy_new_size = enemy.get_enemy_size()
    enemy_new_speed = enemy.get_enemy_speed()
    enemy_new_color = enemy.get_enemy_color()
    
    # Gameplay chạy trong này
    running = True
    while running:
        pressed_keys = pygame.key.get_pressed()
        clicked_mouse = pygame.mouse.get_pressed()
        SCREEN.fill(Black)
        # background = pygame.image.load("")

        # Xử lý sự kiện (Event Handling)
        for event in pygame.event.get():
            # Các sự kiện nhấn phím
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False    
            elif event.type == QUIT:
                running = False
                
            # Các sự kiện của Enemy
            if event.type == ADD_ENEMY:
                for _ in range(5):  # Tạo 10 kẻ địch
                    new_enemy = Enemy(player.rect)
                    new_enemy.set_enemy_size(enemy_new_size)
                    new_enemy.set_enemy_speed(enemy_new_speed)
                    new_enemy.set_enemy_color(enemy_new_color)
                    enemies.add(new_enemy)
                    all_sprites.add(new_enemy)
            elif event.type == INCREASE_STAT:
                enemy_new_size += 15
                if enemy_new_color == White:
                    enemy_new_color = Cyan
                else:
                    enemy_new_color = White
                 
            if event.type == FIRE_RATE:
                mouse = pygame.mouse.get_pos()
                new_bullet = Bullet(player, mouse)
                bullets.add(new_bullet)
                all_sprites.add(new_bullet)
        
        # Phát hiện va chạm:
        if player_collide_with(player, enemies) == True:
            running = False
        if player_collide_with(player, exp_items) == True:
            print('yes')
        for enemy in enemies:
            if enemy_collide_with(enemy, bullets, exp_items, all_sprites) == True:
                print('killed')
        
        # Cập nhật màn hình trò chơi
        player.update(pressed_keys)
        enemies.update(player.rect)
        bullets.update()
        
        # Vẽ tất cả các sprite ra màn hình
        for entity in all_sprites:
            SCREEN.blit(entity.surf, entity.rect) 

        # Cập nhật màn hình
        pygame.display.update()
        
        clock.tick(FPS)
    
    pygame.quit()
