import pygame
import random
import numpy

from DEFINE import *
from Player import *
from Enemy import *
from Items import *
from Collision import *

def player_collide_with(player, enemies):
    if pygame.sprite.spritecollideany(player, enemies):
        player.kill()
        return True
    return False
    
def player_collide_with(player, exp_items):
    for exp in exp_items:
        if pygame.sprite.collide_rect(player, exp):
            exp.kill()
            return True
    return False

def player_collide_with(player, energy_items):
    for ener in energy_items:
        if pygame.sprite.collide_rect(player, ener):
            if player.energy <= 3:
                player.energy += 1
            else:
                player.energy = 3
            ener.kill()
            return True
    return False

def enemy_collide_with(enemy, player_bullets, exp_items, energy_items, all_sprites):
    for bullet in player_bullets:
        if pygame.sprite.collide_rect(enemy, bullet):
            new_exp_item = ExpItem(enemy)
            exp_items.add(new_exp_item)
            all_sprites.add(new_exp_item)
            
            # Tỉ lệ rớt ra Energy là 8%
            rand = numpy.random.choice(numpy.arange(0, 2), p=[0.08, 0.92])
            if rand == 0:
                new_energy_item = EnergyItem(enemy)
                energy_items.add(new_energy_item)
                all_sprites.add(new_energy_item)
            
            bullet.kill()
            enemy.kill()
            return True
    return False

def elite_collide_with(elite, player_bullets):
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
