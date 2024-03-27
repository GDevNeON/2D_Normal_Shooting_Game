import pygame

from DEFINE import *
from Player import *
from Enemy import *
from Items import *
from Collision import *


# Init âm thanh, pygame
pygame.mixer.init()
pygame.init()


if __name__ == '__main__':
    clock = pygame.time.Clock()
    
    pygame.display.set_caption('A 2D NORMAL SHOOTING GAME')
    
    enemies = pygame.sprite.Group()
    elites = pygame.sprite.Group()
    player_bullets = pygame.sprite.Group()
    elite_bullets = pygame.sprite.Group()
    boss_bullets = pygame.sprite.Group()
    exp_items = pygame.sprite.Group()
    energy_items = pygame.sprite.Group()
    hp_items = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    
    # Tạo ra 1 object
    player = Player()
    player_new_size = player.get_size()
    player_new_speed = player.get_speed()
    player_new_color = player.get_color()
    player_new_pos = (player.get_position_x(), player.get_position_y())
    all_sprites.add(player)
    
    enemy = Enemy(player.rect)
    enemy_new_size = enemy.get_size()
    enemy_new_speed = enemy.get_speed()
    enemy_new_color = enemy.get_color()
    enemy_new_pos = (enemy.get_position_x(), enemy.get_position_y())
    
    # Gameplay chạy trong này
    running = True
    while running:
        pressed_keys = pygame.key.get_pressed()
        clicked_mouse = pygame.mouse.get_pressed()
        SCREEN.fill(Black)

        # Xử lý sự kiện (Event Handling)
        for event in pygame.event.get():
            # Các sự kiện nhấn phím
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                # elif event.key == K_q and player.energy == 100:
                    
            elif event.type == QUIT:
                running = False
                
            # Các sự kiện của Enemy
            if event.type == ADD_ENEMY:
                for _ in range(10):  # Tạo 10 kẻ địch
                    new_enemy = Enemy(player.rect)
                    new_enemy.set_size(enemy_new_size)
                    new_enemy.set_speed(enemy_new_speed)
                    new_enemy.set_color(enemy_new_color)
                    enemies.add(new_enemy)
                    all_sprites.add(new_enemy)
            elif event.type == INCREASE_STAT:
                enemy_new_speed += 1
                if enemy_new_color == White:
                    enemy_new_color = Cyan
                else:
                    enemy_new_color = White
                 
            # Các sự kiện của enemy Elite
            if event.type == ADD_ELITE:
                new_elite_1 = Elite_1(player)
                elites.add(new_elite_1)
                all_sprites.add(new_elite_1)
            elif event.type == ELITE_CHANGE_DIRECTION:
                for elite in elites:
                    elite.shoot_flag += 1
                    player_new_pos = (player.get_position_x(), player.get_position_y())
                    
                 
            # Tốc độ bắn đạn
            if event.type == PLAYER_FIRE_RATE:
                mouse = pygame.mouse.get_pos()
                new_bullet = Bullet(player, mouse)
                player_bullets.add(new_bullet)
                all_sprites.add(new_bullet)
        
        # Phát hiện va chạm, debusg:
        if player_collide_with_enemies(player, enemies) == True:
            print('play die')
        if player_collide_with_exp_items(player, exp_items) == True:
            print('yes')
        if player_collide_with_energy_items(player, energy_items) == True:
            print('yesYES')
        if player_collide_with_hp_items(player, hp_items) == True:
            print('Heal')
        for enemy in enemies:
            if enemy_collide_with_player_bullets(enemy, player_bullets, exp_items, hp_items, energy_items, all_sprites) == True:
                print('killed')
        for elite in elites:
            if elite_collide_with_player_bullets(elite, player_bullets) == True:
                print('Elite slain!')
        
        # Cập nhật màn hình trò chơi
        player.update(pressed_keys)
        player_bullets.update()
        enemies.update(player.rect)
        elites.update(player_new_pos, elite_bullets, all_sprites)
        elite_bullets.update()

        
        # Vẽ tất cả các sprite ra màn hình
        for entity in all_sprites:
            SCREEN.blit(entity.surf, entity.rect) 

        # Cập nhật màn hình
        pygame.display.update()
        
        clock.tick(FPS)
    
    pygame.quit()
