
import pygame
import random
import numpy

from DEFINE import *
from Player import *
from Enemy import *
from Items import *
from Functions import *

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
            item.rect.move_ip(dx_normalized * 5, dy_normalized * 5)

# Các hàm phát hiện va chạm
def player_collide_with_enemies(player, enemies):
    for enemy in enemies:
        if pygame.sprite.collide_rect(player, enemy):
            player.health -= 10
            enemy.health -= 10
            print(player.health)
            if player.health == 0:
                return True
            elif enemy.health == 0:
                enemy.kill()
    return False
    
def player_collide_with_exp_items(player, exp_items):
    for exp in exp_items:
        if pygame.sprite.collide_rect(player, exp):
            player.exp += 25
            exp.kill()
            return True
    return False

def player_collide_with_energy_items(player, energy_items):
    for ener in energy_items:
        if pygame.sprite.collide_rect(player, ener):
            player.energy += 25
            if player.energy >= player.bar_maximum_energy:
                player.energy = player.bar_maximum_energy
            ener.kill()
            return True
    return False

def player_collide_with_hp_items(player, hp_items):
    for hp in hp_items:
        if pygame.sprite.collide_rect(player, hp):
            player.health += 10
            if player.health >= player.bar_maximum_health:
                player.health = player.bar_maximum_health
            hp.kill()
            return True
    return False

def enemy_collide_with_player_bullets(enemy, player_bullets, exp_items, hp_items, energy_items, items_group, all_sprites):
    for bullet in player_bullets:
        if pygame.sprite.collide_rect(enemy, bullet):
            # Chắc chắn rớt
            new_exp_item = ExpItem(enemy)
            exp_items.add(new_exp_item)
            items_group.add(new_exp_item)
            all_sprites.add(new_exp_item)
            
            # Có khả năng rót
            rand = numpy.random.choice(numpy.arange(0, 3), p=[0.33, 0.33, 0.34])
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
            enemy.kill()
            return True
    return False

def elite_collide_with_player_bullets(elite, player_bullets):
    for bullet in player_bullets:
        if elite.hp <= 0:
            elite.kill()
            return True
        else:
            if pygame.sprite.collide_rect(bullet, elite):
                print('HP remaining: ', elite.hp)
                if elite.get_color() == Purple:
                    elite.set_color(White)
                else:
                    elite.set_color(Purple)
                elite.hp -= bullet.damage
                bullet.kill()
    return False
