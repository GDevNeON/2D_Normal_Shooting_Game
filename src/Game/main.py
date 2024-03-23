import pygame

from DEFINE import *
from Player import *
from Enemy import *
from Items import *
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
    
    # Tạo màn hình trò chơi và set tên cửa sổ
    
    pygame.display.set_caption('A 2D NORMAL SHOOTING GAME')
    # background = pygame.image.load("")
    
    # Tạo sự kiện
    ADD_ENEMY = USEREVENT + 1
    pygame.time.set_timer(ADD_ENEMY, 2000)
    INCREASE_STAT = USEREVENT + 2
    pygame.time.set_timer(INCREASE_STAT, 10000)
    FIRE_RATE = USEREVENT + 3
    pygame.time.set_timer(FIRE_RATE, 300)
    
    # Tạo ra 1 object
    player = Player()
    enemy = Enemy(player.rect)
    enemy_new_size = enemy.get_enemy_size()
    enemy_new_speed = enemy.get_enemy_speed()
    enemy_new_color = enemy.get_enemy_color()
    
    # Tạo 3 nhóm (groups) để lưu người chơi, đạn, tất cả sprite đang có
    # - Nhóm enemies để phát hiện va chạm và cập nhật vị trí
    # - Nhóm bullets để phát hiện va chạm và cập nhật vị trí
    # - Nhóm all_sprites để render ảnh
    enemies = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)
    
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
                enemy_new_speed += 1
                if enemy_new_color == White:
                    enemy_new_color = Cyan
                else:
                    enemy_new_color = White
            
            
            if event.type == FIRE_RATE:
                mouse = pygame.mouse.get_pos()
                new_bullet = Bullet(player, mouse)
                bullets.add(new_bullet)
                all_sprites.add(new_bullet)
        
        # Kiểm tra xem enemy đụng vào người chơi chưa
        # if pygame.sprite.spritecollideany(player, enemies):
            # player.kill()
            # running = False
        for enemy in enemies:
            if pygame.sprite.spritecollideany(enemy, bullets):
                enemy.kill()
        
        # Cập nhật màn hình trò chơi
        player.update(pressed_keys)
        enemies.update(player.rect)
        bullets.update(player, enemies)
        
        # Vẽ tất cả các sprite ra màn hình
        for entity in all_sprites:
            SCREEN.blit(entity.surf, entity.rect) 

        # Cập nhật màn hình
        pygame.display.update()
        
        clock.tick(FPS)
    
    pygame.quit()
