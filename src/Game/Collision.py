import pygame

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

def enemy_collide_with(enemy, bullets, exp_items, all_sprites):
    for bullet in bullets:
        if pygame.sprite.collide_rect(enemy, bullet):
            new_exp_item = ExpItem(enemy)
            exp_items.add(new_exp_item)
            all_sprites.add(new_exp_item)
            bullet.kill()
            enemy.kill()
            return True
    return False