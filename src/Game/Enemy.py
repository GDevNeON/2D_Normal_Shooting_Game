import pygame
import math
import random

from DEFINE import *
from Items import *

# Base class
class Enemy(pygame.sprite.Sprite):
    def __init__(self, player):
        super(Enemy, self).__init__()
        # Enemy's base attr
        self.size = 20
        self.speed = 1.5
        self.health = 10
        self.collide_damage = 10

        # Enemy's surf attr
        self.sprite = None
        self.surf = pygame.Surface((self.size, self.size))
        self.rect = self.surf.get_rect()
        self.sprite_time = 0
        self.sprite_index = 0
        self.old_x = self.get_position_x()
        self.direction = "right"
        
        # Tính toán vị trí ngẫu nhiên xung quanh người chơi
        self.spawn_radius = 400
        self.generate_random_position(player)
        
    # Các phương thức get/set
    def get_position_x(self):
        return self.rect.x
    
    def get_position_y(self):
        return self.rect.y
    
    def set_size(self, value):
        self.size = value
        
    def get_size(self):
        return self.size
    
    def set_speed(self, value):
        self.speed = value
        
    def get_speed(self):
        return self.speed
    
    # Các hàm phụ cho lớp Enemy
    def left_or_right(self):
        new_x = self.get_position_x()
        if new_x >= self.old_x:     # Sprite hướng về bên phải
            self.direction = "right"
        else:
            self.direction = "left"
        self.old_x = new_x      # Cập nhật vị trí mới của old_x
        
    def load_sprite(self, clock):
        self.left_or_right()
        
        self.sprite_time += clock.get_time()
        if self.sprite_index == len(self.sprite):
            self.sprite_index = 0
        
        if self.sprite_time >= 250:
            if self.direction == "right":
                self.surf = self.sprite[self.sprite_index]
            else:
                reverse = pygame.transform.flip(self.sprite[self.sprite_index], True, False)
                self.surf = reverse
            self.sprite_index += 1
            self.sprite_time = 0
        
    def generate_random_position(self, player):
        # Tạo một vị trí ngẫu nhiên xung quanh người chơi
        angle = random.uniform(0, 2 * math.pi)
        random_x = player.get_position_x() + self.spawn_radius * math.cos(angle)
        random_y = player.get_position_y() + self.spawn_radius * math.sin(angle)
        # Cập nhật vị trí của kẻ địch
        self.rect.center = (random_x, random_y)

    def move_towards_player(self, player):
        # Tính toán hướng vector từ kẻ địch đến người chơi
        dx = player.get_position_x() - self.rect.centerx
        dy = player.get_position_y() - self.rect.centery
        distance = math.sqrt(dx ** 2 + dy ** 2)
        # Chuẩn hóa hướng vector
        if distance != 0:
            dx_normalized = dx / distance
            dy_normalized = dy / distance
        else:
            dx_normalized = 0
            dy_normalized = 0
        # Di chuyển kẻ địch theo hướng vector đã chuẩn hóa
        self.rect.move_ip(dx_normalized * self.speed, dy_normalized * self.speed)
        
    # Hàm cập nhật trạng thái Enemy
    def update(self, player):
        self.move_towards_player(player)


# Derived class
class Normal(Enemy):
    def __init__(self, player):
        super(Normal, self).__init__(player)
        
        rand = random.randint(0, 3)
        if rand == 0:
            self.sprite = ghost_sprite
            self.surf = ghost_sprite[0]
        elif rand == 1:
            self.sprite = goblin_sprite
            self.surf = goblin_sprite[0]
        elif rand == 2:
            self.sprite = skeleton_sprite
            self.surf = skeleton_sprite[0]
        else:
            self.sprite = slime_sprite
            self.surf = slime_sprite[0]
        
    def update(self, player, clock):
        self.load_sprite(clock)
        self.move_towards_player(player)

class Elite_1(Enemy):
    def __init__(self, player):
        super(Elite_1, self).__init__(player)
        self.size = 100
        self.speed = 20
        self.hp = 1000
        
        self.sprite = eghost_sprite
        self.surf = eghost_sprite[0]
        self.rect = self.surf.get_rect()
        
        self.target_pos = (player.get_position_x(), player.get_position_y())
        self.spawn_radius = 600
        
        # Set up 1 list sát thương của các skill của quái ứng với: Skill1 = (int)dmg, Skill2= (int)dmg, Skilln = (int)dmg
        self.skill_dmg = [10, 20]
        self.collide_damage = self.skill_dmg[0]
        self.fire_rate = 2  # Thời gian giữa các lần bắn đạn (tính bằng giây)
        self.time_since_last_shot = 0  # Thời gian đã trôi qua kể từ lần bắn đạn cuối cùng
        self.move_rate = 3  # Thời gian giữa các lần di chuyển (tính bằng giây)
        self.time_since_last_moved = 0
        
        self.generate_random_position(player)
        
    def move(self, clock, player_new_pos):
        self.time_since_last_moved += clock.get_time() / 1000
        
        if self.time_since_last_moved >= self.move_rate:
            # Tính toán hướng vector từ kẻ địch đến người chơi
            self.target_pos = player_new_pos
            self.time_since_last_moved = 0
            
        dx = self.target_pos[0] - self.rect.centerx
        dy = self.target_pos[1] - self.rect.centery
        distance = math.sqrt(dx ** 2 + dy ** 2)
        
        stopping_distance = 10
        if distance > stopping_distance:
            # Chuẩn hóa hướng vector
            if distance != 0:
                dx_normalized = dx / distance
                dy_normalized = dy / distance
            else:
                dx_normalized = 0
                dy_normalized = 0
            # Di chuyển kẻ địch theo hướng vector đã chuẩn hóa
            self.rect.move_ip(dx_normalized * self.speed, dy_normalized * self.speed)
        
    def fire_bullets(self, camera, clock, player_new_pos, elite_bullets, all_sprites):
        # Cập nhật thời gian giữa các lần bắn đạn
        self.time_since_last_shot += clock.get_time() / 1000  # Đổi từ mili-giây sang giây

        # Kiểm tra nếu đủ thời gian để bắn đạn
        if self.time_since_last_shot >= self.fire_rate:
            # Chuyển đổi tọa độ Player sang tọa độ trong thế giới game và áp dụng sự di chuyển của Camera
            player_new_pos = (player_new_pos[0], 
                              player_new_pos[1])
            # Tạo viên đạn với vị trí đã chuyển đổi
            new_bullet = Bullet(self, player_new_pos)
            new_bullet.size = 100
            elite_bullets.add(new_bullet)
            all_sprites.add(new_bullet)
            # Đặt lại thời gian giữa các lần bắn đạn
            self.time_since_last_shot = 0
    
    def update(self, camera, clock, player_new_pos, elite_bullets, all_sprites):
        self.load_sprite(clock)
        self.move(clock, player_new_pos)
        self.fire_bullets(camera, clock, player_new_pos, elite_bullets, all_sprites)
        
class Elite_2(Enemy):
    def __init__(self, player):
        super(Elite_2, self).__init__(player)
        self.size = 100
        self.speed = 20
        self.hp = 1000
        
        self.sprite = egoblin_sprite
        self.surf = egoblin_sprite[0]
        self.rect = self.surf.get_rect()
        
        self.target_pos = (player.get_position_x(), player.get_position_y())
        self.spawn_radius = 600
        
        self.skill_dmg = [10, 20]
        self.collide_damage = self.skill_dmg[0]
        self.normal_bullet_damage = self.skill_dmg[1]
        self.fire_rate = 2  # Thời gian giữa các lần bắn đạn (tính bằng giây)
        self.time_since_last_shot = 0  # Thời gian đã trôi qua kể từ lần bắn đạn cuối cùng
        self.move_rate = 3  # Thời gian giữa các lần di chuyển (tính bằng giây)
        self.time_since_last_moved = 0
        
        self.generate_random_position(player)
        
    def move(self, clock, player_new_pos):
        self.time_since_last_moved += clock.get_time() / 1000
        
        if self.time_since_last_moved >= self.move_rate:
            # Tính toán hướng vector từ kẻ địch đến người chơi
            self.target_pos = player_new_pos
            self.time_since_last_moved = 0
            
        dx = self.target_pos[0] - self.rect.centerx
        dy = self.target_pos[1] - self.rect.centery
        distance = math.sqrt(dx ** 2 + dy ** 2)
        
        stopping_distance = 10
        if distance > stopping_distance:
            # Chuẩn hóa hướng vector
            if distance != 0:
                dx_normalized = dx / distance
                dy_normalized = dy / distance
            else:
                dx_normalized = 0
                dy_normalized = 0
            # Di chuyển kẻ địch theo hướng vector đã chuẩn hóa
            self.rect.move_ip(dx_normalized * self.speed, dy_normalized * self.speed)
        
    def fire_bullets(self, camera, clock, player_new_pos, elite_bullets, all_sprites):
        # Cập nhật thời gian giữa các lần bắn đạn
        self.time_since_last_shot += clock.get_time() / 1000  # Đổi từ mili-giây sang giây

        # Kiểm tra nếu đủ thời gian để bắn đạn
        if self.time_since_last_shot >= self.fire_rate:
            # Chuyển đổi tọa độ Player sang tọa độ trong thế giới game và áp dụng sự di chuyển của Camera
            player_new_pos = (player_new_pos[0], 
                              player_new_pos[1])
            # Tạo viên đạn với vị trí đã chuyển đổi
            new_bullet = Bullet(self, player_new_pos)
            new_bullet.size = 100
            elite_bullets.add(new_bullet)
            all_sprites.add(new_bullet)
            # Đặt lại thời gian giữa các lần bắn đạn
            self.time_since_last_shot = 0
    
    def update(self, camera, clock, player_new_pos, elite_bullets, all_sprites):
        self.load_sprite(clock)
        self.move(clock, player_new_pos)
        self.fire_bullets(camera, clock, player_new_pos, elite_bullets, all_sprites)
    
class Elite_3(Enemy):
    def __init__(self, player):
        super(Elite_3, self).__init__(player)
        self.size = 100
        self.speed = 20
        self.hp = 1000
        
        self.sprite = eskeleton_sprite
        self.surf = eskeleton_sprite[0]
        self.rect = self.surf.get_rect()
        
        self.target_pos = (player.get_position_x(), player.get_position_y())
        self.spawn_radius = 600
        
        self.skill_dmg = [10, 20]
        self.collide_damage = self.skill_dmg[0]
        self.normal_bullet_damage = self.skill_dmg[1]
        self.fire_rate = 2  # Thời gian giữa các lần bắn đạn (tính bằng giây)
        self.time_since_last_shot = 0  # Thời gian đã trôi qua kể từ lần bắn đạn cuối cùng
        self.move_rate = 3  # Thời gian giữa các lần di chuyển (tính bằng giây)
        self.time_since_last_moved = 0
        
        self.generate_random_position(player)
        
    def move(self, clock, player_new_pos):
        self.time_since_last_moved += clock.get_time() / 1000
        
        if self.time_since_last_moved >= self.move_rate:
            # Tính toán hướng vector từ kẻ địch đến người chơi
            self.target_pos = player_new_pos
            self.time_since_last_moved = 0
            
        dx = self.target_pos[0] - self.rect.centerx
        dy = self.target_pos[1] - self.rect.centery
        distance = math.sqrt(dx ** 2 + dy ** 2)
        
        stopping_distance = 10
        if distance > stopping_distance:
            # Chuẩn hóa hướng vector
            if distance != 0:
                dx_normalized = dx / distance
                dy_normalized = dy / distance
            else:
                dx_normalized = 0
                dy_normalized = 0
            # Di chuyển kẻ địch theo hướng vector đã chuẩn hóa
            self.rect.move_ip(dx_normalized * self.speed, dy_normalized * self.speed)
        
    def fire_bullets(self, camera, clock, player_new_pos, elite_bullets, all_sprites):
        # Cập nhật thời gian giữa các lần bắn đạn
        self.time_since_last_shot += clock.get_time() / 1000  # Đổi từ mili-giây sang giây

        # Kiểm tra nếu đủ thời gian để bắn đạn
        if self.time_since_last_shot >= self.fire_rate:
            # Chuyển đổi tọa độ Player sang tọa độ trong thế giới game và áp dụng sự di chuyển của Camera
            player_new_pos = (player_new_pos[0], 
                              player_new_pos[1])
            # Tạo viên đạn với vị trí đã chuyển đổi
            new_bullet = Bullet(self, player_new_pos)
            new_bullet.size = 100
            elite_bullets.add(new_bullet)
            all_sprites.add(new_bullet)
            # Đặt lại thời gian giữa các lần bắn đạn
            self.time_since_last_shot = 0
    
    def update(self, camera, clock, player_new_pos, elite_bullets, all_sprites):
        self.load_sprite(clock)
        self.move(clock, player_new_pos)
        self.fire_bullets(camera, clock, player_new_pos, elite_bullets, all_sprites)
        
class Elite_4(Enemy):
    def __init__(self, player):
        super(Elite_4, self).__init__(player)
        self.size = 100
        self.speed = 20
        self.hp = 1000
        
        self.sprite = eslime_sprite
        self.surf = eslime_sprite[0]
        self.rect = self.surf.get_rect()
        
        self.target_pos = (player.get_position_x(), player.get_position_y())
        self.spawn_radius = 600
        
        self.skill_dmg = [20]
        self.normal_bullet_damage = self.skill_dmg[0]
        self.fire_rate = 2  # Thời gian giữa các lần bắn đạn (tính bằng giây)
        self.time_since_last_shot = 0  # Thời gian đã trôi qua kể từ lần bắn đạn cuối cùng
        self.move_rate = 3  # Thời gian giữa các lần di chuyển (tính bằng giây)
        self.time_since_last_moved = 0
        
        self.generate_random_position(player)
        
    def move(self, clock, player_new_pos):
        self.time_since_last_moved += clock.get_time() / 1000
        
        if self.time_since_last_moved >= self.move_rate:
            # Tính toán hướng vector từ kẻ địch đến người chơi
            self.target_pos = player_new_pos
            self.time_since_last_moved = 0
            
        dx = self.target_pos[0] - self.rect.centerx
        dy = self.target_pos[1] - self.rect.centery
        distance = math.sqrt(dx ** 2 + dy ** 2)
        
        stopping_distance = 10
        if distance > stopping_distance:
            # Chuẩn hóa hướng vector
            if distance != 0:
                dx_normalized = dx / distance
                dy_normalized = dy / distance
            else:
                dx_normalized = 0
                dy_normalized = 0
            # Di chuyển kẻ địch theo hướng vector đã chuẩn hóa
            self.rect.move_ip(dx_normalized * self.speed, dy_normalized * self.speed)
        
    def fire_bullets(self, camera, clock, player_new_pos, elite_bullets, all_sprites):
        # Cập nhật thời gian giữa các lần bắn đạn
        self.time_since_last_shot += clock.get_time() / 1000  # Đổi từ mili-giây sang giây

        # Kiểm tra nếu đủ thời gian để bắn đạn
        if self.time_since_last_shot >= self.fire_rate:
            # Chuyển đổi tọa độ Player sang tọa độ trong thế giới game và áp dụng sự di chuyển của Camera
            player_new_pos = (player_new_pos[0], 
                              player_new_pos[1])
            # Tạo viên đạn với vị trí đã chuyển đổi
            new_bullet = Bullet(self, player_new_pos)
            new_bullet.size = 100
            elite_bullets.add(new_bullet)
            all_sprites.add(new_bullet)
            # Đặt lại thời gian giữa các lần bắn đạn
            self.time_since_last_shot = 0
    
    def update(self, camera, clock, player_new_pos, elite_bullets, all_sprites):
        self.load_sprite(clock)
        self.move(clock, player_new_pos)
        self.fire_bullets(camera, clock, player_new_pos, elite_bullets, all_sprites)
               
class Boss(Enemy):
    def __init__(self, player):
        super(Boss, self).__init__(player)
        self.slain_time = 0
        self.size = 100
        self.speed = 20
        self.hp = 10000
        
        self.sprite = skelly_walk_sprite
        self.surf = skelly_walk_sprite[0]
        self.rect = self.surf.get_rect()
        
        self.target_pos = (player.get_position_x(), player.get_position_y())
        self.spawn_radius = 600
        
        # skill_dmg = [collision, slash, s1, s2]
        self.skill_dmg = [10, 20, 20, 20]
        self.collide_damage = self.skill_dmg[0]
        self.fire_rate = 2  # Thời gian giữa các lần bắn đạn (tính bằng giây)
        self.time_since_last_shot = 0  # Thời gian đã trôi qua kể từ lần bắn đạn cuối cùng
        self.move_rate = 3  # Thời gian giữa các lần di chuyển (tính bằng giây)
        self.time_since_last_moved = 0
        
        self.generate_random_position(player)
        
    def moving_trail(self):
        trail_positions = []
        sprite_center = self.rect.center
        trail_positions.append(sprite_center)
        trail_positions = trail_positions[-10:]  # Chỉ lưu trữ 10 vị trí gần nhất
        # Vẽ các bản sao của sprite với độ mờ khác nhau
        alpha = 255
        for pos in reversed(trail_positions):
            trail_sprite = self.surf.copy()
            trail_sprite.set_alpha(alpha)
            SCREEN.blit(trail_sprite, trail_sprite.get_rect(center=pos))
            alpha -= 25  # Giảm độ mờ cho mỗi bản sao
            
    def move(self, player_new_pos, clock):
        self.time_since_last_moved += clock.get_time() / 1000
        
        if self.time_since_last_moved >= self.move_rate:
            # Tính toán hướng vector từ kẻ địch đến người chơi
            self.target_pos = player_new_pos
            self.time_since_last_moved = 0
            
        dx = self.target_pos[0] - self.rect.centerx
        dy = self.target_pos[1] - self.rect.centery
        distance = math.sqrt(dx ** 2 + dy ** 2)
        
        stopping_distance = 10
        if distance > stopping_distance:
            # Chuẩn hóa hướng vector
            if distance != 0:
                dx_normalized = dx / distance
                dy_normalized = dy / distance
            else:
                dx_normalized = 0
                dy_normalized = 0
            # Di chuyển kẻ địch theo hướng vector đã chuẩn hóa
            self.rect.move_ip(dx_normalized * 30, dy_normalized * 30)
            
    def update(self, camera, clock, player_new_pos, elite_bullets, all_sprites):
        self.moving_trail()
        self.move(player_new_pos, clock)