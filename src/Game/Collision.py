import pygame
import random
import numpy

from DEFINE import *
from Player import *
from Enemy import *
from Items import *
from Collision import *

def player_collide_with_enemies(player, enemies):
    if pygame.sprite.spritecollideany(player, enemies):
        player.target_health -= 10
        if player.target_health == 0:
            return True
    return False
    
def player_collide_with_exp_items(player, exp_items):
    for exp in exp_items:
        if pygame.sprite.collide_rect(player, exp):
            if player.target_exp < 100:
                player.target_exp += 5
            else:
                player.target_exp = 100
            exp.kill()
            return True
    return False

def player_collide_with_energy_items(player, energy_items):
    for ener in energy_items:
        if pygame.sprite.collide_rect(player, ener):
            if player.target_energy < 100:
                player.target_energy += 10
            else:
                player.target_energy = 100
            ener.kill()
            return True
    return False

def player_collide_with_hp_items(player, hp_items):
    for hp in hp_items:
        if pygame.sprite.collide_rect(player, hp):
            if player.target_health < 1000:
                player.target_health += 100
            else:
                player.target_health = 1000
            hp.kill()
            return True
    return False

def enemy_collide_with_player_bullets(enemy, player_bullets, exp_items, hp_items, energy_items, all_sprites):
    for bullet in player_bullets:
        if pygame.sprite.collide_rect(enemy, bullet):
            new_exp_item = ExpItem(enemy)
            exp_items.add(new_exp_item)
            all_sprites.add(new_exp_item)
            
            # Tỉ lệ rớt ra Energy là 8%
            rand = numpy.random.choice(numpy.arange(0, 3), p=[0.08, 0.05, 0.87])
            if rand == 0:
                new_energy_item = EnergyItem(enemy)
                energy_items.add(new_energy_item)
                all_sprites.add(new_energy_item)
            elif rand == 1:
                new_hp_item = HpItem(enemy)
                hp_items.add(new_hp_item)
                all_sprites.add(new_hp_item)
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
