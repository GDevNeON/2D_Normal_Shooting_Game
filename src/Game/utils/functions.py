import pygame
import numpy
import math

from ..core.define import *
from ..entities.player import *
from ..entities.enemy import *
from ..entities.items import *
from ..managers.image_manager import change_color

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
            # Use the take_damage method which handles damage reduction and death state
            player_died = player.take_damage(enemy.collide_damage)
            enemy.health -= 10
            
            # If player died, return True to indicate game over
            if player_died:
                return True
                
            if enemy.health <= 0:
                enemy.kill()
    
    # Handle hit animation
    if player.is_hit:
        player.hit_time += clock.get_time()
        player.surf = change_color(player.surf, White)
        if player.hit_time >= 50:
            player.hit_time = 0
            player.is_hit = False
    return False
    
def player_collide_with_exp_items(player, exp_items):
    for exp in exp_items:
        if pygame.sprite.collide_rect(player, exp):
            # Play collect item sound
            from ..managers.sound_manager import SoundManager
            SoundManager.play_collect_item()
            
            player.add_experience(50)  # Use the new method to add experience
            exp.kill()
            return True
    return False

def player_collide_with_energy_items(player, energy_items):
    for ener in energy_items:
        if pygame.sprite.collide_rect(player, ener):
            # Play collect item sound
            from ..managers.sound_manager import SoundManager
            SoundManager.play_collect_item()
            
            player.energy += 1
            if player.energy >= player.maximum_energy:
                player.energy = player.maximum_energy
            ener.kill()
            return True
    return False

def player_collide_with_hp_items(player, hp_items):
    for hp in hp_items:
        if pygame.sprite.collide_rect(player, hp):
            # Play collect item sound
            from ..managers.sound_manager import SoundManager
            SoundManager.play_collect_item()
            
            player.health += 10
            if player.health >= player.maximum_health:
                player.health = player.maximum_health
            hp.kill()
            return True
    return False

def enemy_collide_with_player_bullets(enemy, player_bullets, exp_items, hp_items, energy_items, items_group, all_sprites, clock):
    enemy_died = False
    
    # Create a list of bullets that hit the enemy
    bullets_hit = [bullet for bullet in player_bullets if pygame.sprite.collide_rect(enemy, bullet)]
    
    # Process each bullet that hit the enemy
    for bullet in bullets_hit:
        # Play enemy hit sound
        from ..managers.sound_manager import SoundManager
        SoundManager.play_enemy_hit()
        
        enemy.is_hit = True
        enemy.health -= bullet.damage
        bullet.kill()  # Remove bullet from all groups
        
        # Check if enemy died from this hit
        if enemy.health <= 0 and not enemy_died:
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
            enemy_died = True
    
    # Handle hit effect
    if enemy.is_hit:
        enemy.hit_time += clock.get_time()
        enemy.surf = change_color(enemy.surf, White)
        if enemy.hit_time >= 50:
            enemy.hit_time = 0
            enemy.is_hit = False
    
    return enemy_died

def elite_collide_with_player_bullets(elite, player_bullets, clock, flag):
    elite_died = False
    
    # Create a list of bullets that hit the elite
    bullets_hit = [bullet for bullet in player_bullets if pygame.sprite.collide_rect(bullet, elite)]
    
    # Process each bullet that hit the elite
    for bullet in bullets_hit:
        elite.is_hitted = True
        elite.hp -= bullet.damage
        bullet.kill()  # Remove bullet from all groups
        
        # Check if elite died from this hit
        if elite.hp <= 0 and not elite_died:
            elite.kill()
            flag += 1
            elite_died = True
            break  # Exit loop if elite is dead
    
    return elite_died, flag

def elite_collide_with_player(elites, player, clock, flag):
    for elite in elites:
        if elite.hp <= 0:
            elite.kill()
            flag += 1
            return True
        else:
            if pygame.sprite.collide_rect(player, elite):
                elite.is_hitted = True
                player.health = 0
                # print('HP remaining: ', elite.hp)
                elite.hp -= 10
            
    # if elite.is_hitted == True:
    #     # elite.surf = change_color(elite.surf, White)
    #     elite.is_hitted = False
    return False

def boss_collide_with_player_bullets(boss, player_bullets, clock):
    for bullet in player_bullets:
        if pygame.sprite.collide_rect(boss, bullet):
            boss.is_hit = True
            boss.hp -= bullet.damage
            bullet.kill()
            return True
            
    if boss.is_hit == True:
        boss.hit_time += clock.get_time()
        boss.surf = change_color(boss.surf, White)
        if boss.hit_time >= 50:
            boss.hit_time = 0
            boss.is_hit = False
    return False

def boss_collide_with_player(boss, player, clock):
    # Only check collision if boss is alive
    if hasattr(boss, 'is_alive') and not boss.is_alive:
        return False
        
    if pygame.sprite.collide_rect(player, boss):
        player.is_hit = True
        player.health -= boss.collide_damage
        if player.health <= 0:
            return True
            
    if player.is_hit == True:
        player.hit_time += clock.get_time()
        player.surf = change_color(player.surf, White)
        if player.hit_time >= 50:
            player.hit_time = 0
            player.is_hit = False
    return False
