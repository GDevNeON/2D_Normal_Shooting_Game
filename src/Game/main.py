import pygame
# import sys
# sys.path.insert(0, r"D:\WorkSpace\python_project\python_game_project\2D_Normal_Shooting_Game\src\Menu")
# import GUI # type: ignore

from DEFINE     import *
from Camera     import *
from Player     import *
from Enemy      import *
from Items      import *
from Functions  import *
from Image      import *
from Background import *


# Init âm thanh, pygame
pygame.mixer.init()
pygame.init()


def Run_Game():
    clock = pygame.time.Clock()
    
    pygame.display.set_caption('A 2D NORMAL SHOOTING GAME')
    
    enemies         = pygame.sprite.Group()
    elites          = pygame.sprite.Group()
    player_bullets  = pygame.sprite.Group()
    elite_bullets   = pygame.sprite.Group()
    boss_bullets    = pygame.sprite.Group()
    exp_items       = pygame.sprite.Group()
    energy_items    = pygame.sprite.Group()
    hp_items        = pygame.sprite.Group()
    items_group     = pygame.sprite.Group()
    all_sprites     = pygame.sprite.Group()
    
    # Tạo ra 1 object
    camera = Camera(LEVEL_WIDTH, LEVEL_HEIGHT)
    
    player = Player_Male()
    player_new_size = player.get_size()
    player_new_speed = player.get_speed()
    player_new_color = player.get_color()
    player_new_pos = (player.get_position_x(), player.get_position_y())
    all_sprites.add(player)
    
    enemy = Normal(player)
    enemy_new_size = enemy.get_size()
    enemy_new_speed = enemy.get_speed()
    enemy_new_color = enemy.get_color()
    enemy_new_pos = (enemy.get_position_x(), enemy.get_position_y())
    background = Background(background_sprite)
    

    # Gameplay chạy trong này
    running = True
    while running:
        # GUI.Run_User_Interface()
        pressed_keys = pygame.key.get_pressed()
        clicked_mouse = pygame.mouse.get_pressed()
        SCREEN.fill(Black)

        # Xử lý sự kiện (Event Handling)
        for event in pygame.event.get():
            # Các sự kiện nhấn phím
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                elif event.key == K_q and player.energy >= player.maximum_energy:
                    player.energy = 0
                    player.burst = True
            elif event.type == QUIT:
                running = False
                
            # Các sự kiện của Enemy
            if event.type == ADD_ENEMY:
                for _ in range(10):  # Tạo 10 kẻ địch
                    new_enemy = Normal(player)
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
        
        # Phát hiện va chạm, debusg:
        items_move_towards_player(player, items_group)
        if player_collide_with_enemies(player, enemies) == True:
            # print('play die')
            pass
        if player_collide_with_exp_items(player, exp_items) == True:
            # print('yes')
            pass
        if player_collide_with_energy_items(player, energy_items) == True:
            # print('yesYES')
            pass
        if player_collide_with_hp_items(player, hp_items) == True:
            # print('Heal')
            pass
        for enemy in enemies:
            if enemy_collide_with_player_bullets(enemy, player_bullets, exp_items, hp_items, energy_items, items_group, all_sprites) == True:
                # print('killed')
                pass
        for elite in elites:
            if elite_collide_with_player_bullets(elite, player_bullets) == True:
                # print('Elite slain!')
                pass
        
        background.blitting(SCREEN)
        for entity in all_sprites:
            SCREEN.blit(entity.surf, camera.apply(entity)) 

        # Cập nhật màn hình trò chơi
        camera.update(player)
        player.update(clock, camera, pressed_keys, player_bullets, all_sprites, background)
        player_bullets.update()
        enemies.update(player)
        player_new_pos = (player.get_position_x(), player.get_position_y())
        elites.update(camera, clock, player_new_pos, elite_bullets, all_sprites)
        elite_bullets.update()
        pygame.display.update()
        
        clock.tick(FPS)
        # if player.get_Current_Health() == 0:
        #     running = False

    # GUI.Run_User_Interface()
    pygame.quit()


if __name__ == '__main__':
    Run_Game()
    # GUI.Run_User_Interface()
