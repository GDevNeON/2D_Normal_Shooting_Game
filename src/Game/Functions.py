
import pygame
import numpy

from DEFINE import *
from Player import *
from Enemy import *
from Items import *

# Các hàm di chuyển
def items_move_towards_player(player, items_group):
    for item in items_group:
        # Tính toán hướng vector từ kẻ địch đến người chơi
        dx = player.rect.centerx - item.rect.centerx
        dy = player.rect.centery - item.rect.centery
        distance = math.sqrt(dx ** 2 + dy ** 2)
        # Nếu khoảng cách từ Player đến items nhỏ hơn 40px thì kéo items về Player
        if (distance <= 100):
        # Chuẩn hóa hướng vector
            if distance != 0:
                dx_normalized = dx / distance
                dy_normalized = dy / distance
            else:
                dx_normalized = 0
                dy_normalized = 0
            # Di chuyển kẻ địch theo hướng vector đã chuẩn hóa
            item.rect.move_ip(dx_normalized * 10, dy_normalized * 10)

# Các hàm phát hiện va chạm
def player_collide_with_enemies(player, enemies, clock):
    for enemy in enemies:
        if pygame.sprite.collide_rect(player, enemy):
            player.is_hit = True
            player.health -= enemy.collide_damage
            enemy.health -= 10
            if player.health <= 0:
                return True
            elif enemy.health <= 0:
                enemy.kill()
    
    if player.is_hit == True:
        player.hit_time += clock.get_time()
        player.surf = change_color(player.surf, White)
        if player.hit_time >= 50:
            player.hit_time = 0
            player.is_hit = False
    return False
    
def player_collide_with_exp_items(player, exp_items):
    for exp in exp_items:
        if pygame.sprite.collide_rect(player, exp):
            player.exp += 2
            exp.kill()
            return True
    return False

def player_collide_with_energy_items(player, energy_items):
    for ener in energy_items:
        if pygame.sprite.collide_rect(player, ener):
            player.energy += 1
            if player.energy >= player.maximum_energy:
                player.energy = player.maximum_energy
            ener.kill()
            return True
    return False

def player_collide_with_hp_items(player, hp_items):
    for hp in hp_items:
        if pygame.sprite.collide_rect(player, hp):
            player.health += 10
            if player.health >= player.maximum_health:
                player.health = player.maximum_health
            hp.kill()
            return True
    return False

def enemy_collide_with_player_bullets(enemy, player_bullets, exp_items, hp_items, energy_items, items_group, all_sprites, clock):
    for bullet in player_bullets:
        if pygame.sprite.collide_rect(enemy, bullet):
            enemy.is_hit = True
            enemy.health -= bullet.damage
            if enemy.health <= 0:
                enemy.kill()
                # Chắc chắn rớt
                new_exp_item = ExpItem(enemy)
                exp_items.add(new_exp_item)
                items_group.add(new_exp_item)
                all_sprites.add(new_exp_item)
                # Có khả năng rớt
                rand = numpy.random.choice(numpy.arange(0, 3), p=[0.2, 0.2, 0.6])
                if rand == 0:
                    new_energy_item = EnergyItem(enemy)
                    energy_items.add(new_energy_item)
                    all_sprites.add(new_energy_item)
                    items_group.add(new_energy_item)
                elif rand == 1:
                    new_hp_item = HpItem(enemy)
                    hp_items.add(new_hp_item)
                    all_sprites.add(new_hp_item)
                    items_group.add(new_hp_item)

            bullet.kill()
            return True
        
    if enemy.is_hit == True:
        enemy.hit_time += clock.get_time()
        enemy.surf = change_color(enemy.surf, White)
        if enemy.hit_time >= 50:
            enemy.hit_time = 0
            enemy.is_hit = False
    return False

def elite_collide_with_player_bullets(elite, player_bullets, clock):
    for bullet in player_bullets:
        elite.is_hitted = True
        if elite.hp <= 0:
            elite.kill()
            Enemy.elite_slain_time += 1
            return True
        else:
            if pygame.sprite.collide_rect(bullet, elite):
                # print('HP remaining: ', elite.hp)
                elite.hp -= bullet.damage
                bullet.kill()
                
    if elite.is_hitted == True:
        # elite.surf = change_color(elite.surf, White)
        elite.is_hitted = False
    return False

def elite_collide_with_player(elites, player, clock):
    for elite in elites:
        if elite.hp <= 0:
            elite.kill()
            Enemy.elite_slain_time += 1
            return True
        else:
            if pygame.sprite.collide_rect(player, elite):
                elite.is_hit = True
                player.health = 0
                # print('HP remaining: ', elite.hp)
                elite.hp -= 10
            
    if elite.is_hitted == True:
        # elite.surf = change_color(elite.surf, White)
        elite.is_hitted = False
    return False
