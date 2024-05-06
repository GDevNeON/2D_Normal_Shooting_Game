
import pygame
import random
import sys
sys.path.insert(0, r"./src/Menu")
import GUI

from DEFINE     import *
from Camera     import *
from Player     import *
from Enemy      import *
from Items      import *
from Functions  import *
from Image      import *
from Background import *
from Sounds     import grassplain

pygame.mixer.init()
pygame.init()


def Run_Game(current_mode, character_select):    
    clock = pygame.time.Clock()
    pygame.display.set_caption('A 2D NORMAL SHOOTING GAME')
    pygame.mixer.music.load(grassplain)
    pygame.mixer.music.play(loops=-1)
    
    
    enemies         = pygame.sprite.Group()
    elites          = pygame.sprite.Group()
    player_bullets  = pygame.sprite.Group()
    elite_bullets   = pygame.sprite.Group()
    exp_items       = pygame.sprite.Group()
    energy_items    = pygame.sprite.Group()
    hp_items        = pygame.sprite.Group()
    items_group     = pygame.sprite.Group()
    all_sprites     = pygame.sprite.Group()
    
    # Tạo ra 1 object
    camera = Camera(LEVEL_WIDTH, LEVEL_HEIGHT)
    
    if character_select == 1:
        player = Player_Male()
    else:
        player = Player_Female()
    player_new_size = player.get_size()
    player_new_speed = player.get_speed()
    player_new_pos = (player.get_position_x(), player.get_position_y())
    all_sprites.add(player)

    enemy = Normal(player)
    enemy_new_size = enemy.get_size()
    enemy_new_speed = enemy.get_speed()
    enemy_new_pos = (enemy.get_position_x(), enemy.get_position_y())
    background = Background(background_sprite)
    
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
                elif event.key == K_q and player.energy >= player.maximum_energy and player.burst_clock < player.burst_time:
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
                    enemies.add(new_enemy)
                    all_sprites.add(new_enemy)
            elif event.type == INCREASE_STAT:
                enemy_new_speed += 1
                 
            # Các sự kiện của enemy Elite
            if event.type == ADD_ELITE:
                rand = random.randint(1, 4)
                if rand == 1:
                    new_elite = Elite_1(player)
                elif rand == 2:
                    new_elite = Elite_2(player)
                elif rand == 3:
                    new_elite = Elite_3(player)
                else:
                    new_elite = Elite_4(player)
                elites.add(new_elite)
                all_sprites.add(new_elite)
        
        # Phát hiện va chạm, debusg:
        items_move_towards_player(player, items_group)
        if player_collide_with_enemies(player, enemies, clock) == True:
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
            if enemy_collide_with_player_bullets(enemy, player_bullets, exp_items, hp_items, energy_items, items_group, all_sprites, clock) == True:
                # print('killed')
                pass
        for elite in elites:
            if elite_collide_with_player_bullets(elite, player_bullets, clock) == True:
                # print('Elite slain!')
                pass
            
            if elite_collide_with_player(elites, player, clock) == True:
                pass
        
        background.blitting(SCREEN)
        for entity in all_sprites:
            SCREEN.blit(entity.surf, camera.apply(entity)) 

        # Cập nhật màn hình trò chơi
        camera.update(player)
        player.update(clock, camera, pressed_keys, player_bullets, all_sprites, background)
        player_bullets.update()
        enemies.update(player, clock)
        player_new_pos = (player.get_position_x(), player.get_position_y())
        elites.update(camera, clock, player_new_pos, elite_bullets, all_sprites)
        elite_bullets.update()
        pygame.display.update()
        
        clock.tick(FPS)
        if player.get_Current_Health() == 0:
            pygame.mixer.music.stop()
            running = False
            GUI.Run_Gameover_Interface()
        if current_mode == 1 and Enemy.elite_slain_time == 3:   # Chỉnh chế độ normal và endless
            running = False
            GUI.Run_Gameover_Interface()    
            
    pygame.quit()


if __name__ == '__main__':
    Run_Game()
    # GUI.Run_User_Interface()
