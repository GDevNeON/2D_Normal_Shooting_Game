import pygame
import random
import math
from pygame.locals import (
    RLEACCEL,
    USEREVENT,
    FULLSCREEN,
    K_w,
    K_a, 
    K_s, 
    K_d,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

# Init âm thanh, pygame
pygame.mixer.init()
pygame.init()


# Set FPS cho game
FPS = 60

# Screen resolution
SCREEN_WIDTH    = 1366
SCREEN_HEIGHT   = 768

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


# Định nghĩa các lớp
class Player(pygame.sprite.Sprite):
    # Constructor
    def __init__(self):
        # Player's base attr
        self.size = 25
        self.color = Red
        self.speed = 3
        super(Player, self).__init__()
        
        # Player's health attr 
        self.current_health = 200
        self.maximum_health = 1000
        self.health_bar_length = 400
        self.health_ratio = self.maximum_health / self.health_bar_length
        self.target_health = 500
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
        
        # Health attr
        self.current_health = 200
        self.maximum_health = 1000
        self.health_bar_length = 400
        self.health_ratio = self.maximum_health / self.health_bar_length
        self.target_health = 500
        self.health_change_speed = 5
        
    # Các phương thức get/set
    def get_player_position_x(self):
        return self.rect.x
    
    def get_player_position_y(self):
        return self.rect.y
    
    def set_player_size(self, value):
        self.size = value
        
    def get_player_size(self):
        return self.size
    
    def set_player_color(self, value):
        self.color = value
        
    def get_player_color(self):
        return self.color
    
    def set_player_speed(self, value):
        self.speed = value
        
    def get_player_speed(self):
        return self.speed
    
    # Các hàm phụ cho Player
    def get_damage(self, amount):
        if self.current_health > 0:
            self.current_health -= amount
        if self.current_health <= 0:
            self.current_health = 0
    
    def basic_health(self):
        pygame.draw.rect(screen, (255,0,0), (10,10,self.current_health/self.health_ratio,25))
        pygame.draw.rect(screen, (255,255,255), (10,10,self.health_bar_length,25), 4)
        
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
        
        pygame.draw.rect(screen, (255,0,0), health_bar_rect)
        pygame.draw.rect(screen, transition_color, transition_bar_rect)
        pygame.draw.rect(screen, (255,255,255), (10,45,self.health_bar_length,25), 4)
        
    def update_player(self):
        self.surf = pygame.Surface((self.size, self.size))
        self.surf.fill(self.color)
        self.rect = self.surf.get_rect(center = self.rect.center)
            
    # Hàm cập nhật trạng thái Player
    def update(self, pressed_keys):
        self.update_player()
        
        # Health_bar
        self.basic_health()
        self.advanced_health()
        
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

class Enemy(pygame.sprite.Sprite):
    def __init__(self, player_rect):
        # Enemy's base attr
        self.size = 20
        self.color = White
        self.speed = 3
        super(Enemy, self).__init__()

        # Enemy's surf attr
        self.surf = pygame.Surface((self.size, self.size))
        self.surf.fill(self.color)
        self.rect = self.surf.get_rect()
        
        # Tính toán vị trí ngẫu nhiên xung quanh người chơi
        self.generate_random_position(player_rect)
        
    # Các phương thức get/set
    def set_enemy_size(self, value):
        self.size = value
        
    def get_enemy_size(self):
        return self.size
    
    def set_enemy_color(self, value):
        self.color = value
        
    def get_enemy_color(self):
        return self.color
    
    def set_enemy_speed(self, value):
        self.speed = value
        
    def get_enemy_speed(self):
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

class Bullet(pygame.sprite.Sprite):
    def __init__(self, player, mouse):
        # Bullet's base attr
        self.size = 20
        self.color = Yellow
        self.speed = 10
        super(Bullet, self).__init__()
          
        # Bullet's position attr
        self.x = player.get_player_position_x()
        self.y = player.get_player_position_y()
        self.dx = 0
        self.dy = 0
        self.dx_normalized = 0
        self.dy_normalized = 0

        # Bullet's surf attr
        self.surf = pygame.Surface((self.size, self.size))
        self.surf.fill(self.color)
        self.rect = self.surf.get_rect()

        # Bullet's target attr
        self.target_x, self.target_y = mouse
            
    def update_bullets(self):
        self.surf = pygame.Surface((self.size, self.size))
        self.surf.fill(self.color)
        self.rect = self.surf.get_rect(center = self.rect.center)
        
    def update(self, player, enemies):
        self.update_bullets()

        player_pos_x = player.get_player_position_x()
        player_pos_y = player.get_player_position_y()
        self.dx = self.target_x - player_pos_x
        self.dy = self.target_y - player_pos_y
        distance = math.sqrt(self.dx ** 2 + self.dy ** 2)

        if distance != 0:
            self.dx_normalized = self.dx / distance
            self.dy_normalized = self.dy / distance
        else:
            self.dx_normalized = 0
            self.dy_normalized = 0

        self.dx = self.dx_normalized
        self.dy = self.dy_normalized

        self.x += self.dx * self.speed
        self.y += self.dy * self.speed

        self.rect.move_ip(self.x, self.y)
        
        pygame.draw.rect(screen, Yellow, self.rect, 20)

        # Xóa đạn khi ra khỏi màn hình hoặc va chạm với kẻ địch
        if (0 < self.rect.x < SCREEN_WIDTH) or (0 < self.rect.y < SCREEN_HEIGHT):
            for enemy in enemies:
                if pygame.sprite.collide_rect(self, enemy):
                    self.kill()
                    enemy.kill()
                    break
        


if __name__ == '__main__':
    clock = pygame.time.Clock()
    
    # Tạo màn hình trò chơi và set tên cửa sổ
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), FULLSCREEN)
    pygame.display.set_caption('A 2D NORMAL SHOOTING GAME')
    
    # background = pygame.image.load("")
    
    # Tạo sự kiện
    ADD_ENEMY = USEREVENT + 1
    pygame.time.set_timer(ADD_ENEMY, 2000)
    INCREASE_STAT = USEREVENT + 2
    pygame.time.set_timer(INCREASE_STAT, 10000)
    FIRE_RATE = USEREVENT + 3
    pygame.time.set_timer(FIRE_RATE, 500)
    
    # Tạo ra 1 object
    player = Player()
    enemy = Enemy(player.rect)
    enemy_new_size = enemy.get_enemy_size()
    enemy_new_speed = enemy.get_enemy_speed()
    enemy_new_color = enemy.get_enemy_color()
    
    # Tạo 3 nhóm (groups) để lưu người chơi, đạn, tất cả sprite đang có
    # - Nhóm enemies để phát hiện va chạm và cập nhật vị trí
    # - Nhóm bullets để phát hiện va chạm và cập nhật vị trí
    # - Nhóm all_sprites để render ảnh
    enemies = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)
    
    # Gameplay chạy trong này
    running = True
    while running:
        pressed_keys = pygame.key.get_pressed()
        clicked_mouse = pygame.mouse.get_pressed()
        screen.fill(Black)
        # background = pygame.image.load("")

        # Xử lý sự kiện (Event Handling)
        for event in pygame.event.get():
            # Các sự kiện nhấn phím
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False    
            elif event.type == QUIT:
                running = False
                
            # Các sự kiện của Enemy
            if event.type == ADD_ENEMY:
                for _ in range(5):  # Tạo 10 kẻ địch
                    new_enemy = Enemy(player.rect)
                    new_enemy.set_enemy_size(enemy_new_size)
                    new_enemy.set_enemy_speed(enemy_new_speed)
                    new_enemy.set_enemy_color(enemy_new_color)
                    enemies.add(new_enemy)
                    all_sprites.add(new_enemy)
            elif event.type == INCREASE_STAT:
                enemy_new_size += 15
                enemy_new_speed += 1
                if enemy_new_color == White:
                    enemy_new_color = Cyan
                else:
                    enemy_new_color = White
            elif event.type == FIRE_RATE:
                mouse = pygame.mouse.get_pos()
                new_bullet = Bullet(player, mouse)
                bullets.add(new_bullet)
                all_sprites.add(new_bullet)
        
        # Kiểm tra xem enemy đụng vào người chơi chưa
        # if pygame.sprite.spritecollideany(player, enemies):
            # player.kill()
            # running = False
        for enemy in enemies:
            if pygame.sprite.spritecollideany(enemy, bullets):
                enemy.kill()
        
        # Cập nhật màn hình trò chơi
        player.update(pressed_keys)
        enemies.update(player.rect)
        bullets.update(player, enemies)
        
        # Vẽ tất cả các sprite ra màn hình
        for entity in all_sprites:
            screen.blit(entity.surf, entity.rect) 

        # Cập nhật màn hình
        pygame.display.update()
        
        clock.tick(FPS)
    
    pygame.quit()
