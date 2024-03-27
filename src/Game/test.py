import pygame
import numpy
import math
import random

from pygame.locals import (
    RLEACCEL,
    USEREVENT,
    FULLSCREEN,
    RESIZABLE,
    K_w,
    K_a, 
    K_s, 
    K_d,
    K_q,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

# Set FPS cho game
FPS = 60

# Screen resolution
SCREEN_WIDTH    = 1366
SCREEN_HEIGHT   = 768
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), RESIZABLE)
# BACKGROUND = pygame.image.load("")

# Mã màu
Black   = (0,0,0)
White   = (255,255,255)
Red	    = (255,0,0)
Lime    = (0,255,0)
Blue    = (0,0,255)
Yellow  = (255,255,0)
Cyan    = (0,255,255)
Magenta = (255,0,255)
Silver  = (192,192,192)
Gray    = (128,128,128)
Maroon  = (128,0,0)
Olive   = (128,128,0)
Green   = (0,128,0)
Purple  = (128,0,128)
Teal    = (0,128,128)
Navy    = (0,0,128)

# Tạo sự kiện
ADD_ENEMY = USEREVENT + 1
pygame.time.set_timer(ADD_ENEMY, 5000)
INCREASE_STAT = USEREVENT + 2
pygame.time.set_timer(INCREASE_STAT, 20000)
PLAYER_FIRE_RATE = USEREVENT + 3
pygame.time.set_timer(PLAYER_FIRE_RATE, 300)
ADD_ELITE = USEREVENT + 10
pygame.time.set_timer(ADD_ELITE, 3000, 1)
ELITE_CHANGE_DIRECTION = USEREVENT + 11
pygame.time.set_timer(ELITE_CHANGE_DIRECTION, 3000)
ELITE_FIRE_RATE = USEREVENT + 12
pygame.time.set_timer(ELITE_FIRE_RATE, 5000)
ADD_BOSS = USEREVENT + 20
pygame.time.set_timer(ADD_BOSS, 300000, 1)


# Init âm thanh, pygame
pygame.mixer.init()
pygame.init()

class Enemy(pygame.sprite.Sprite):
    def __init__(self, player_rect):
        # Enemy's base attr
        self.size = 20
        self.color = White
        self.speed = 1.5
        super(Enemy, self).__init__()

        # Enemy's surf attr
        self.surf = pygame.Surface((self.size, self.size))
        self.surf.fill(self.color)
        self.rect = self.surf.get_rect()
        
        # Tính toán vị trí ngẫu nhiên xung quanh người chơi
        self.generate_random_position(player_rect)
        
    # Các phương thức get/set
    def get_position_x(self):
        return self.rect.x
    
    def get_position_y(self):
        return self.rect.y
    
    def set_size(self, value):
        self.size = value
        
    def get_size(self):
        return self.size
    
    def set_color(self, value):
        self.color = value
        
    def get_color(self):
        return self.color
    
    def set_speed(self, value):
        self.speed = value
        
    def get_speed(self):
        return self.speed
    
    # Các hàm phụ cho lớp Enemy
    def generate_random_position(self, player_rect):
        # Bán kính của vùng phát sinh ngẫu nhiên
        radius = 350
        # Tạo một vị trí ngẫu nhiên xung quanh người chơi
        angle = random.uniform(0, 2 * math.pi)
        random_x = player_rect.centerx + radius * math.cos(angle)
        random_y = player_rect.centery + radius * math.sin(angle)
        # Cập nhật vị trí của kẻ địch
        self.rect.center = (random_x, random_y)
    
    def update_enemy(self):
        self.surf = pygame.Surface((self.size, self.size))
        self.surf.fill(self.color)
        self.rect = self.surf.get_rect(center = self.rect.center)
        
    # Hàm cập nhật trạng thái Enemy
    def update(self, player_rect):
        self.update_enemy()

        # Tính toán hướng vector từ kẻ địch đến người chơi
        dx = player_rect.centerx - self.rect.centerx
        dy = player_rect.centery - self.rect.centery
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
        
# 3 types of Elite enemies
class Elite_1(pygame.sprite.Sprite):
    def __init__(self, player):
        self.size = 100
        self.color = Purple
        self.speed = 15
        self.hp = 5000
        self.shoot_flag = 0
        super(Elite_1, self).__init__()
        
        self.surf = pygame.Surface((self.size, self.size))
        self.surf.fill(self.color)
        self.rect = self.surf.get_rect()
        
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
    
    def set_color(self, value):
        self.color = value
        
    def get_color(self):
        return self.color
    
    def set_speed(self, value):
        self.speed = value
        
    def get_speed(self):
        return self.speed
            
    def generate_random_position(self, player):
        # Bán kính của vùng phát sinh ngẫu nhiên
        radius = 500
        # Tạo một vị trí ngẫu nhiên xung quanh người chơi
        angle = random.uniform(0, 2 * math.pi)
        random_x = player.get_position_x() + radius * math.cos(angle)
        random_y = player.get_position_y() + radius * math.sin(angle)
        # Cập nhật vị trí của kẻ địch
        self.rect.center = (random_x, random_y)
        
    def move(self, player_new_pos):
        # Tính toán hướng vector từ kẻ địch đến người chơi
        dx = player_new_pos[0] - self.rect.centerx
        dy = player_new_pos[1] - self.rect.centery
        distance = math.sqrt(dx ** 2 + dy ** 2)
        # Chuẩn hóa hướng vector
        if distance != 0:
            dx_normalized = dx / distance
            dy_normalized = dy / distance
        else:
            dx_normalized = 0
            dy_normalized = 0
        # Di chuyển kẻ địch theo hướng vector đã chuẩn hóa
        if float(self.rect.centerx) != float(player_new_pos[0]) and float(self.rect.centery) != float(player_new_pos[1]):
            self.rect.move_ip(dx_normalized * self.speed, dy_normalized * self.speed)
        
    def shoot(self, player_new_pos, elite_bullets, all_sprites):
        bullet = Bullet(self, player_new_pos)
        bullet.size = 200
        elite_bullets.add(bullet)
        all_sprites.add(bullet)
    
    def update(self, player_new_pos, elite_bullets, all_sprites):
        self.move(player_new_pos)
        if self.shoot_flag % 4 == 0:
            self.shoot(player_new_pos, elite_bullets, all_sprites)
            self.shoot_flag += 1

class ExpItem(pygame.sprite.Sprite):
    def __init__(self, enemy):
        #ExpItem's base attr
        self.size = 10
        self.color = Blue
        self.x = enemy.get_position_x()
        self.y = enemy.get_position_y()
        super(ExpItem, self).__init__()
        
        # ExpItem's surf attr
        self.surf = pygame.Surface((self.size, self.size))
        self.surf.fill(self.color)
        self.rect = self.surf.get_rect(
            center = (
                self.x + enemy.get_size()/2, 
                self.y + enemy.get_size()/2
            )
        )
        
    def update(self):
        self.surf = pygame.Surface((self.size, self.size))
        self.surf.fill(self.color)
        self.rect = self.surf.get_rect(center = self.rect.center)
        
class EnergyItem(pygame.sprite.Sprite):
    # EnergyItem's base attr
    def __init__(self, enemy):
        self.size = 15
        self.color = Lime
        self.x = enemy.get_position_x()
        self.y = enemy.get_position_y()
        super(EnergyItem, self).__init__()

        # EnergyItem's surf attr
        self.surf = pygame.Surface((self.size, self.size))
        self.surf.fill(self.color)
        self.rect = self.surf.get_rect(
            center = (
                self.x + enemy.get_size()/2, 
                self.y + enemy.get_size()/2
            )
        )
        
class Bullet(pygame.sprite.Sprite):
    def __init__(self, current, target):
        # Bullet's base attr
        self.size = 20
        self.color = Yellow
        self.speed = 20
        self.damage = 100
        super(Bullet, self).__init__()
          
        # Bullet's position attr
        self.x = current.get_position_x()
        self.y = current.get_position_y()
        self.dx = 0
        self.dy = 0
        self.dx_normalized = 0
        self.dy_normalized = 0

        # Bullet's target attr
        self.target_x, self.target_y = target
        
        # Bullet's surf attr
        self.surf = pygame.Surface((self.size, self.size))
        self.surf.fill(self.color)
        self.rect = self.surf.get_rect(
            center = (
                current.get_position_x() + current.get_size()/2, 
                current.get_position_y() + current.get_size()/2
            )
        )
    
    def update(self, player):
        self.surf = pygame.Surface((self.size, self.size))
        self.surf.fill(self.color)
        self.rect = self.surf.get_rect(center = self.rect.center)

        self.dx = self.target_x - self.x
        self.dy = self.target_y - self.y
        distance = math.sqrt(self.dx ** 2 + self.dy ** 2)

        if distance != 0:
            self.dx_normalized = self.dx / distance
            self.dy_normalized = self.dy / distance
        else:
            self.dx_normalized = 0
            self.dy_normalized = 0

        self.rect.move_ip(self.dx_normalized * self.speed, self.dy_normalized * self.speed)    
        
class Player(pygame.sprite.Sprite):
    # Constructor
    def __init__(self):
        # Player's base attr
        self.size = 25
        self.color = Red
        self.speed = 5
        self.energy = 0
        self.exp = 0
        super(Player, self).__init__()
        
        # Player's health attr 
        self.current_health = 200
        self.maximum_health = 1000
        self.health_bar_length = 400
        self.health_ratio = self.maximum_health / self.health_bar_length
        self.target_health = 1000
        self.health_change_speed = 5
        
        # Player's surf attr
        self.surf = pygame.Surface((self.size, self.size))
        self.surf.fill(self.color)
        self.rect = self.surf.get_rect(
            center = (
                (SCREEN_WIDTH-self.surf.get_width())/2,
                (SCREEN_HEIGHT-self.surf.get_height())/2
            ) 
        )
        
    # Các phương thức get/set
    def get_position_x(self):
        return self.rect.x
    
    def get_position_y(self):
        return self.rect.y
    
    def set_size(self, value):
        self.size = value
        
    def get_size(self):
        return self.size
    
    def set_color(self, value):
        self.color = value
        
    def get_color(self):
        return self.color
    
    def set_speed(self, value):
        self.speed = value
        
    def get_speed(self):
        return self.speed
    
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
        
        if self.current_health < self.target_health:
            self.current_health += self.health_change_speed
            transition_width = int((self.target_health - self.current_health)/self.health_ratio)
            transition_color = (0,255,0)
        if self.current_health > self.target_health:
            self.current_health -= self.health_change_speed
            transition_width = int((self.target_health - self.current_health)/self.health_ratio)
            transition_color = (255,255,0)
            
        health_bar_rect = pygame.Rect(10,45,self.current_health/self.health_ratio,25)
        transition_bar_rect = pygame.Rect(health_bar_rect.right,45,transition_width,25)
        
        pygame.draw.rect(SCREEN, (255,0,0), health_bar_rect)
        pygame.draw.rect(SCREEN, transition_color, transition_bar_rect)
        pygame.draw.rect(SCREEN, (255,255,255), (10,45,self.health_bar_length,25), 4)
                
    def update_player(self):
        self.surf = pygame.Surface((self.size, self.size))
        self.surf.fill(self.color)
        self.rect = self.surf.get_rect(center = self.rect.center)
            
    # Hàm cập nhật trạng thái Player
    def update(self, pressed_keys):
        self.update_player()
        
        # Health_bar
        #self.basic_health()
        self.advanced_health()
        
        # Movement
        if pressed_keys[K_w]:
            self.rect.move_ip(0, -self.speed)
        if pressed_keys[K_s]:
            self.rect.move_ip(0, self.speed)
        if pressed_keys[K_a]:
            self.rect.move_ip(-self.speed, 0)
        if pressed_keys[K_d]:
            self.rect.move_ip(self.speed, 0)
        
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            
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
            if player.energy <= 100:
                player.energy += 50
            else:
                player.energy = 100
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
            if player.energy <= 100:
                player.energy += 50
            else:
                player.energy = 100
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




if __name__ == '__main__':
    clock = pygame.time.Clock()
    
    pygame.display.set_caption('A 2D NORMAL SHOOTING GAME')
    
    enemies = pygame.sprite.Group()
    elites = pygame.sprite.Group()
    player_bullets = pygame.sprite.Group()
    elite_bullets = pygame.sprite.Group()
    boss_bullets = pygame.sprite.Group()
    exp_items = pygame.sprite.Group()
    energy_items = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    
    # Tạo ra 1 object
    player = Player()
    player_new_size = player.get_size()
    player_new_speed = player.get_speed()
    player_new_color = player.get_color()
    player_new_pos = (player.get_position_x(), player.get_position_y())
    all_sprites.add(player)
    
    enemy = Enemy(player.rect)
    enemy_new_size = enemy.get_size()
    enemy_new_speed = enemy.get_speed()
    enemy_new_color = enemy.get_color()
    enemy_new_pos = (enemy.get_position_x(), enemy.get_position_y())
    
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
                # elif event.key == K_q and player.energy == 100:
                    
            elif event.type == QUIT:
                running = False
                
            # Các sự kiện của Enemy
            if event.type == ADD_ENEMY:
                for _ in range(10):  # Tạo 10 kẻ địch
                    new_enemy = Enemy(player.rect)
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
            elif event.type == ELITE_CHANGE_DIRECTION:
                for elite in elites:
                    elite.shoot_flag += 1
                    player_new_pos = (player.get_position_x(), player.get_position_y())
                    
                 
            # Tốc độ bắn đạn
            if event.type == PLAYER_FIRE_RATE:
                mouse = pygame.mouse.get_pos()
                new_bullet = Bullet(player, mouse)
                player_bullets.add(new_bullet)
                all_sprites.add(new_bullet)
        
        # Phát hiện va chạm, debug:
        # if player_collide_with(player, enemies) == True:
        #     running = False
        if player_collide_with(player, exp_items) == True:
            print('yes')
        if player_collide_with(player, energy_items) == True:
            print('yesYES')
        for enemy in enemies:
            if enemy_collide_with(enemy, player_bullets, exp_items, energy_items, all_sprites) == True:
                print('killed')
        for elite in elites:
            if elite_collide_with(elite, player_bullets) == True:
                print('Elite slain!')
        
        # Cập nhật màn hình trò chơi
        player.update(pressed_keys)
        player_bullets.update()
        enemies.update(player.rect)
        elites.update(player_new_pos, elite_bullets, all_sprites)
        elite_bullets.update()

        
        # Vẽ tất cả các sprite ra màn hình
        for entity in all_sprites:
            SCREEN.blit(entity.surf, entity.rect) 

        # Cập nhật màn hình
        pygame.display.update()
        
        clock.tick(FPS)
    
    pygame.quit()
