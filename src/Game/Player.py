from numpy import choose
import pygame
import math
import random

from DEFINE import *
from Image import *
from Items import *
from pygame.locals import (
    K_w,
    K_a, 
    K_s, 
    K_d,
)

# Base class
class Player(pygame.sprite.Sprite):
    # Constructor
    def __init__(self):
        super(Player, self).__init__()
        # Player's base attr
        self.size = 25
        self.speed = 5
        
        # Player's health attr 
        self.current_health = 100
        self.maximum_health = 100
        self.health_bar_length = 300
        self.health_ratio = self.maximum_health / self.health_bar_length
        self.health = 100
        self.health_change_speed = 5
        
        # Player's energy attr 
        self.current_energy = 0
        self.maximum_energy = 3
        self.energy_bar_length = 200
        self.energy_ratio = self.maximum_energy / self.energy_bar_length
        self.energy = 0
        self.energy_change_speed = 1
        
        # Player's exp attr 
        self.current_exp = 100
        self.maximum_exp = 100
        self.exp_bar_length = 500
        self.exp_ratio = self.maximum_exp / self.exp_bar_length
        self.exp = 0
        self.exp_change_speed = 1
        
        # Player's surf attr
        self.idle_time = 0
        self.idle_index = 0
        self.run_time = 0
        self.run_index = 0
        self.surf = None
        self.rect = None
        self.move_left = False
        self.move_right = False
        self.direction = "right"
        
        # Other player's attr
        self.normal_bullet_damage = 0
        self.level = 1
        self.fire_rate = 500
        self.time_since_last_shot = 0  
        self.burst = False
        self.time_since_last_burst_shot = 0
        self.burst_clock = 0
        self.burst_time = 5000
        
        # Buff
        self.attack_speed_buff_level = 0
        self.damage_buff_level = 0
        self.max_hp_buff_level = 0
        self.movement_speed_buff_level = 0
        self.defense_buff_level = 0
        self.bullet_size_buff_level = 0
        self.damage_reduction_buff_level = 0
        
        # Sprite clock
        self.warning_time = 0
        self.is_hit = False
        self.hit_time = 0
        
    # Các phương thức get/set
    def get_position_x(self):
        return self.rect.centerx
    
    def get_position_y(self):
        return self.rect.centery
    
    def set_size(self, value):
        self.size = value
        
    def get_size(self):
        return self.size
    
    def set_speed(self, value):
        self.speed = value
        
    def get_speed(self):
        return self.speed
    
    # Các hàm animate sprite                    
    def idle_anim(self):
        pass
    
    def run_anim(self):
        pass
    
    # Các hàm phụ cho Player
    def get_damage(self, amount):
        if self.current_health > 0:
            self.current_health -= amount
        if self.current_health <= 0:
            self.current_health = 0
    
    def basic_health(self):
        pygame.draw.rect(SCREEN, (255,0,0), (10,10,self.current_health/self.health_ratio,25))
        pygame.draw.rect(SCREEN, (255,255,255), (10,10,self.health_bar_length,25), 4)
        
    def advanced_health(self):
        transition_width = 0
        transition_color = (255,0,0)
        
        if self.current_health < self.health:
            self.current_health += self.health_change_speed
            transition_width = int((self.health - self.current_health)/self.health_ratio)
            transition_color = (0,255,0)
        if self.current_health > self.health:
            self.current_health -= self.health_change_speed
            transition_width = int((self.health - self.current_health)/self.health_ratio)
            transition_color = (255,255,0)
            
        health_bar_rect = pygame.Rect(10,10,self.current_health/self.health_ratio,25)
        transition_bar_rect = pygame.Rect(health_bar_rect.right,10,transition_width,25)
        
        pygame.draw.rect(SCREEN, (255,0,0), health_bar_rect)
        pygame.draw.rect(SCREEN, transition_color, transition_bar_rect)
        pygame.draw.rect(SCREEN, (255,255,255), (10,10,self.health_bar_length,25), 3)
        
    def advanced_energy(self):
        transition_width = 0
        transition_color = (255,0,0)
        
        if self.current_energy < self.energy:
            self.current_energy += self.energy_change_speed
            transition_width = int((self.energy - self.current_energy)/self.energy_ratio)
            transition_color = (0,255,0)
        if self.current_energy > self.energy:
            self.current_energy -= self.energy_change_speed
            transition_width = int((self.energy - self.current_energy)/self.energy_ratio)
            transition_color = (255,255,0)
            
        energy_bar_rect = pygame.Rect(10,32,self.current_energy/self.energy_ratio,20)
        transition_bar_rect = pygame.Rect(energy_bar_rect.right,32,transition_width,20)
        
        pygame.draw.rect(SCREEN, (0,0,255), energy_bar_rect)
        pygame.draw.rect(SCREEN, transition_color, transition_bar_rect)
        pygame.draw.rect(SCREEN, (255,255,255), (10,32,self.energy_bar_length,20), 3)
        
    def advanced_exp(self):
        transition_width = 0
        transition_color = (255,0,0)
        
        if self.current_exp < self.exp:
            self.current_exp += self.exp_change_speed
            transition_width = int((self.exp - self.current_exp)/self.exp_ratio)
            transition_color = Yellow
        if self.current_exp > self.exp:
            self.current_exp -= self.exp_change_speed
            transition_width = int((self.exp - self.current_exp)/self.exp_ratio)
            transition_color = (255,255,0)
            
        exp_bar_rect = pygame.Rect(400,670,self.current_exp/self.exp_ratio,15)
        transition_bar_rect = pygame.Rect(exp_bar_rect.right,670,transition_width,15)
        
        pygame.draw.rect(SCREEN, (0,255,0), exp_bar_rect)
        pygame.draw.rect(SCREEN, transition_color, transition_bar_rect)
        pygame.draw.rect(SCREEN, (255,255,255), (400,670,self.exp_bar_length,15), 2)
        
    def fire_bullets(self):
        pass
            
    def burst_skill(self):
        pass
    
    def burst_(self):
        pass
        
    def level_up(self):
        if self.exp >= self.maximum_exp:
            self.exp = math.fabs(self.exp - self.maximum_exp)
            self.maximum_exp += int(20/100 * self.maximum_exp)
            self.exp_ratio = self.maximum_exp / self.exp_bar_length
            self.level += 1
            
            print("level", self.level)
            print("max_ex", self.maximum_exp)

            self.auto_choose_buff()
    
    def auto_choose_buff(self):
        available_buffs = []
    
        if self.attack_speed_buff_level < 1:
            available_buffs.append(self.upgrade_attack_speed_buff)
        if self.damage_buff_level < 5:
            available_buffs.append(self.upgrade_damage_buff)
        if self.max_hp_buff_level < 3:
            available_buffs.append(self.upgrade_max_hp_buff)
        if self.movement_speed_buff_level < 3:
            available_buffs.append(self.upgrade_movement_speed_buff)
    
        if available_buffs:
            chosen_buff = random.choice(available_buffs)
            chosen_buff()
          
    # def choose_buffs(self):
    #     print("Choose buffs to upgrade:")
    #     if self.attack_speed_buff_level < 5:
    #         print("1. Increase Attack Speed (Current Level:", self.attack_speed_buff_level, ")")
    #     if self.damage_buff_level < 5:
    #         print("2. Increase Damage (Current Level:", self.damage_buff_level, ")")
    #     if self.max_hp_buff_level < 3:
    #         print("3. Increase Max HP (Current Level:", self.max_hp_buff_level, ")")
    #     if self.movement_speed_buff_level < 3:
    #         print("4. Increase Movement Speed (Current Level:", self.movement_speed_buff_level, ")")
    #     if self.defense_buff_level < 3:
    #         print("5. Increase Defense (Current Level:", self.defense_buff_level, ")")
    #     if self.bullet_size_buff_level < 5:
    #         print("6. Increase Bullet Size (Current Level:", self.bullet_size_buff_level, ")")
    #     if self.damage_reduction_buff_level == 0:
    #         print("7. Reduce Damage Taken (Current Level: Not unlocked)")

    #     choice = input("Enter the number of the buff you want to upgrade (1-7): ")

    #     if choice == '1' and self.attack_speed_buff_level < 5:
    #         self.upgrade_attack_speed_buff()
    #     elif choice == '2' and self.damage_buff_level < 5:
    #         self.upgrade_damage_buff()
    #     elif choice == '3' and self.max_hp_buff_level < 3:
    #         self.upgrade_max_hp_buff()
    #     elif choice == '4' and self.movement_speed_buff_level < 3:
    #         self.upgrade_movement_speed_buff()
    #     elif choice == '5' and self.defense_buff_level < 3:
    #         self.upgrade_defense_buff()
    #     elif choice == '6' and self.bullet_size_buff_level < 5:
    #         self.upgrade_bullet_size_buff()
    #     elif choice == '7' and self.damage_reduction_buff_level == 0:
    #         self.upgrade_damage_reduction_buff()
    #     else:
    #         print("Invalid choice. Please choose again.")
    #         self.choose_buffs()

    # Các hàm dưới đây để tăng cấp các buff tương ứng
    def upgrade_attack_speed_buff(self):
        if self.attack_speed_buff_level < 5:
            self.attack_speed_buff_level += 1
            print("Attack Speed buff upgraded to level", self.attack_speed_buff_level)
            
            self.fire_rate += 0.1*self.fire_rate
            print("Tốc đánh", self.fire_rate)
        else:
            print("Maximum level reached for Attack Speed buff.")

    def upgrade_damage_buff(self):
        if self.damage_buff_level < 5:
            self.damage_buff_level += 1
            print("Damage buff upgraded to level", self.damage_buff_level)
            
            self.normal_bullet_damage += 5
            print("Sát thương", self.normal_bullet_damage)
        else:
            print("Maximum level reached for Damage buff.")

    def upgrade_max_hp_buff(self):
        if self.max_hp_buff_level < 3:
            self.max_hp_buff_level += 1
            print("Max HP buff upgraded to level", self.max_hp_buff_level)
            
            self.maximum_health += 20
            self.health_ratio = self.maximum_health / self.health_bar_length
            print("max_health", self.maximum_health)
        else:
            print("Maximum level reached for Max HP buff.")

    def upgrade_movement_speed_buff(self):
        if self.movement_speed_buff_level < 3:
            self.movement_speed_buff_level += 1
            print("Movement Speed buff upgraded to level", self.movement_speed_buff_level)
            
            self.speed += 0.1*self.speed
            print("Tốc chạy", self.speed)
        else:
            print("Maximum level reached for Movement Speed buff.")

    def upgrade_defense_buff(self):
        if self.defense_buff_level < 3:
            self.defense_buff_level += 1
            print("Defense buff upgraded to level", self.defense_buff_level)
        else:
            print("Maximum level reached for Defense buff.")

    def upgrade_bullet_size_buff(self):
        if self.bullet_size_buff_level < 5:
            self.bullet_size_buff_level += 1
            print("Bullet Size buff upgraded to level", self.bullet_size_buff_level)
        else:
            print("Maximum level reached for Bullet Size buff.")

    def upgrade_damage_reduction_buff(self):
        if self.damage_reduction_buff_level == 0:
            self.damage_reduction_buff_level = 1
            print("Damage Reduction buff upgraded to level 1")
        else:
            print("Maximum level reached for Damage Reduction buff.")
            
    def movement(self, pressed_keys, bg):
        if pressed_keys[K_w] == False and pressed_keys[K_a] == False and pressed_keys[K_s] == False and pressed_keys[K_d] == False:
            self.move_left = False
            self.move_right = False
        else:
            if pressed_keys[K_w]:
                self.rect.move_ip(0, -self.speed)
                if (self.get_position_y() >= SCREEN_HEIGHT/2
                    and self.get_position_y() <= LEVEL_HEIGHT - SCREEN_HEIGHT/2):
                    bg.y += self.speed
                    
            if pressed_keys[K_s]:
                self.rect.move_ip(0, self.speed)
                if (self.get_position_y() >= SCREEN_HEIGHT/2
                    and self.get_position_y() <= LEVEL_HEIGHT - SCREEN_HEIGHT/2):
                    bg.y -= self.speed
                    
            if pressed_keys[K_a]:
                self.direction = "left"
                self.move_left = False
                self.move_right = True
                self.rect.move_ip(-self.speed, 0)
                if (self.get_position_x() >= SCREEN_WIDTH/2
                    and self.get_position_x() <= LEVEL_WIDTH - SCREEN_WIDTH/2):
                    bg.x += self.speed
                    
            if pressed_keys[K_d]:
                self.direction = "right"
                self.move_left = True
                self.move_right = False
                self.rect.move_ip(self.speed, 0)
                if (self.get_position_x() >= SCREEN_WIDTH/2
                    and self.get_position_x() <= LEVEL_WIDTH - SCREEN_WIDTH/2):
                    bg.x -= self.speed
            
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > LEVEL_WIDTH:
            self.rect.right = LEVEL_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= LEVEL_HEIGHT:
            self.rect.bottom = LEVEL_HEIGHT
            
    def get_Current_Health(self):
        return self.current_health
            
    # Hàm cập nhật trạng thái Player
    def update(self):
        pass


# Derived class
class Player_Male(Player):
    def __init__(self):
        super(Player_Male, self).__init__()
        self.normal_bullet_damage = 10
        self.fire_rate = 500
        self.bullet_amount = 5
        self.spread_range = 45
        
        self.surf = male_idle_sprite[0]
        self.rect = self.surf.get_rect(
            center = (
                (LEVEL_WIDTH-self.surf.get_width())/2,
                (LEVEL_HEIGHT-self.surf.get_height())/2
            ) 
        )
        
    def idle_anim(self, clock):
        self.idle_time += clock.get_time()
        if self.idle_index == len(male_idle_sprite):
            self.idle_index = 0
            
        if self.idle_time >= 250:
            if self.direction == "right":
                self.surf = male_idle_sprite[self.idle_index]
            else:
                self.surf = pygame.transform.flip(male_idle_sprite[self.idle_index], True, False)
            self.idle_index += 1
            self.idle_time = 0
        
    def run_anim(self, clock):    
        self.run_time += clock.get_time()
        if self.run_index == len(male_run_sprite):
            self.run_index = 0
            
        if self.run_time >= 100:
            if self.direction == "right":
                self.surf = male_run_sprite[self.run_index]
            else:
                self.surf = pygame.transform.flip(male_run_sprite[self.run_index], True, False)
            self.run_index += 1
            self.run_time = 0

    def fire_bullets(self, camera, clock, player_bullets, all_sprites):
        self.time_since_last_burst_shot += clock.get_time()
        
        if self.time_since_last_burst_shot >= self.fire_rate:
            mouse = pygame.mouse.get_pos()
            player_to_mouse = (mouse[0] - camera.camera.x - self.rect.centerx, mouse[1] - camera.camera.y - self.rect.centery)
            angle_to_mouse = - math.atan2(player_to_mouse[1], player_to_mouse[0])

            for b in range(self.bullet_amount):
                rand_range = angle_to_mouse + math.radians(random.uniform(-self.spread_range, self.spread_range))
                bullet_pos = (self.rect.centerx, self.rect.centery)
                bullet_pos = (bullet_pos[0] + 75 * math.cos(rand_range), bullet_pos[1] - 75 * math.sin(rand_range))
                new_bullet = Bullet(self, bullet_pos)
                new_bullet.distance_limit = 200
                player_bullets.add(new_bullet)
                all_sprites.add(new_bullet)
            
            # Đặt lại thời gian giữa các lần bắn đạn
            self.time_since_last_burst_shot = 0
            
    def burst_skill(self, camera, clock, player_bullets, all_sprites):
        self.time_since_last_burst_shot += clock.get_time()
        
        if self.time_since_last_burst_shot >= self.fire_rate:
            mouse = pygame.mouse.get_pos()
            player_to_mouse = (mouse[0] - camera.camera.x - self.rect.centerx, mouse[1] - camera.camera.y - self.rect.centery)
            angle_to_mouse = - math.atan2(player_to_mouse[1], player_to_mouse[0])

            for b in range(self.bullet_amount):
                rand_range = angle_to_mouse + math.radians(random.uniform(-self.spread_range, self.spread_range))
                bullet_pos = (self.rect.centerx, self.rect.centery)
                bullet_pos = (bullet_pos[0] + 75 * math.cos(rand_range), bullet_pos[1] - 75 * math.sin(rand_range))
                new_bullet = Bullet(self, bullet_pos)
                player_bullets.add(new_bullet)
                all_sprites.add(new_bullet)
            
            # Đặt lại thời gian giữa các lần bắn đạn
            self.time_since_last_burst_shot = 0
            
    def burst_(self, camera, clock, player_bullets, all_sprites):
        if self.burst == True:
            self.fire_rate = 200
            self.burst_clock += clock.get_time()
            self.burst_skill(camera, clock, player_bullets, all_sprites)
            if self.burst_clock >= self.burst_time:
                self.fire_rate = 500
                self.burst = False
                self.burst_clock = 0
                
    # Hàm cập nhật trạng thái Player
    def update(self, clock, camera, pressed_keys, player_bullets, all_sprites, background):
        if self.move_left == True or self.move_right == True:
            self.run_anim(clock)
        elif self.move_left == False and self.move_right == False:
            self.idle_anim(clock)
        
        self.advanced_health()
        self.advanced_energy()
        self.advanced_exp()
        
        self.fire_bullets(camera, clock, player_bullets, all_sprites)
        self.burst_(camera, clock, player_bullets, all_sprites)
        self.level_up()
        self.movement(pressed_keys, background)

class Player_Female(Player):
    def __init__(self):
        super(Player_Female, self).__init__()
        self.normal_bullet_damage = 10
        self.fire_rate = 400
        
        self.surf = female_idle_sprite[0]
        self.rect = self.surf.get_rect(
            center = (
                (LEVEL_WIDTH-self.surf.get_width())/2,
                (LEVEL_HEIGHT-self.surf.get_height())/2
            ) 
        )
        
    def idle_anim(self, clock):
        self.idle_time += clock.get_time()
        if self.idle_index == len(female_idle_sprite):
            self.idle_index = 0
            
        if self.idle_time >= 250:
            if self.direction == "right":
                self.surf = female_idle_sprite[self.idle_index]
            else:
                self.surf = pygame.transform.flip(female_idle_sprite[self.idle_index], True, False)
            self.idle_index += 1
            self.idle_time = 0
        
    def run_anim(self, clock):    
        self.run_time += clock.get_time()
        if self.run_index == len(female_run_sprite):
            self.run_index = 0
            
        if self.run_time >= 50:
            if self.direction == "right":
                self.surf = female_run_sprite[self.run_index]
            else:
                self.surf = pygame.transform.flip(female_run_sprite[self.run_index], True, False)
            self.run_index += 1
            self.run_time = 0
            
    def fire_bullets(self, camera, clock, player_bullets, all_sprites):
        self.time_since_last_shot += clock.get_time()

        if self.time_since_last_shot >= self.fire_rate:
            mouse = pygame.mouse.get_pos()
            mouse_world_pos = (mouse[0] - camera.camera.x, mouse[1] - camera.camera.y)
            new_bullet = Bullet(self, mouse_world_pos)
            new_bullet.distance_limit = 400
            player_bullets.add(new_bullet)
            all_sprites.add(new_bullet)
            self.time_since_last_shot = 0  
            
    def burst_skill(self, camera, clock, player_bullets, all_sprites):
        self.time_since_last_burst_shot += clock.get_time()
        
        if self.time_since_last_burst_shot >= 100:
            mouse = pygame.mouse.get_pos()
            player_to_mouse = (mouse[0] - camera.camera.x - self.rect.centerx, mouse[1] - camera.camera.y - self.rect.centery)
            angle_to_mouse = - math.atan2(player_to_mouse[1], player_to_mouse[0])
            
            # Tính toán hướng mới cho hai viên đạn cách biệt 10 độ với hướng của chuột
            new_angle1 = angle_to_mouse + math.radians(10)
            new_angle2 = angle_to_mouse - math.radians(10)
            
            # Tạo viên đạn với hướng mới
            bullet1_pos = (self.rect.centerx, self.rect.centery)
            bullet2_pos = (self.rect.centerx, self.rect.centery)
            
            # Tính toán vị trí mới của viên đạn theo hướng mới
            bullet1_pos = (bullet1_pos[0] + 75 * math.cos(new_angle1), bullet1_pos[1] - 75 * math.sin(new_angle1))
            bullet2_pos = (bullet2_pos[0] + 75 * math.cos(new_angle2), bullet2_pos[1] - 75 * math.sin(new_angle2))
            
            # Tạo viên đạn với vị trí và hướng mới
            new_bullet1 = Bullet(self, bullet1_pos)
            new_bullet1.distance_limit = 400
            new_bullet2 = Bullet(self, bullet2_pos)
            new_bullet2.distance_limit = 400
            
            player_bullets.add(new_bullet1, new_bullet2)
            all_sprites.add(new_bullet1, new_bullet2)
            
            # Đặt lại thời gian giữa các lần bắn đạn
            self.time_since_last_burst_shot = 0
        
    def burst_(self, camera, clock, player_bullets, all_sprites):
        if self.burst == True:
            self.fire_rate = 100
            self.burst_clock += clock.get_time()
            self.burst_skill(camera, clock, player_bullets, all_sprites)
            if self.burst_clock >= self.burst_time:
                self.fire_rate = 400
                self.burst = False
                self.burst_clock = 0
                
    # Hàm cập nhật trạng thái Player
    def update(self, clock, camera, pressed_keys, player_bullets, all_sprites, background):
        if self.move_left == True or self.move_right == True:
            self.run_anim(clock)
        elif self.move_left == False and self.move_right == False:
            self.idle_anim(clock)
        
        self.advanced_health()
        self.advanced_energy()
        self.advanced_exp()
        
        self.fire_bullets(camera, clock, player_bullets, all_sprites)
        self.burst_(camera, clock, player_bullets, all_sprites)
        self.level_up()
        self.movement(pressed_keys, background)
        