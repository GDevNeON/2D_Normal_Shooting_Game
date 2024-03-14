import pygame
import random
from pygame.locals import (
    RLEACCEL,
    K_w,
    K_a, 
    K_s, 
    K_d,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

#Init sounds, pygame
pygame.mixer.init()
pygame.init()

#Framerate per second
FPS = 30

#Screen resolution
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

#Basic color code
Black = (0,0,0)
White = (255,255,255)
Red	= (255,0,0)
Lime = (0,255,0)
Blue = (0,0,255)
Yellow = (255,255,0)
Cyan = (0,255,255)
Magenta = (255,0,255)
Silver = (192,192,192)
Gray = (128,128,128)
Maroon = (128,0,0)
Olive = (128,128,0)
Green = (0,128,0)
Purple = (128,0,128)
Teal = (0,128,128)
Navy = (0,0,128)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.Surface((25, 25))
        self.surf.fill(Red)
        self.rect = self.surf.get_rect(
            center = (
                (SCREEN_WIDTH-self.surf.get_width())/2,
                (SCREEN_HEIGHT-self.surf.get_height())/2
            ) 
        )
        
    def update(self, pressed_keys):
        if pressed_keys[K_w]:
            self.rect.move_ip(0, -1)
        if pressed_keys[K_s]:
            self.rect.move_ip(0, 1)
        if pressed_keys[K_a]:
            self.rect.move_ip(-1, 0)
        if pressed_keys[K_d]:
            self.rect.move_ip(1, 0)
        
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.Surface((20, 10))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect(
            center = (
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )
        self.speed = random.randint(5, 20)
        
    # Move the sprite based on speed
    # Remove the sprite when it passes the left edge of the screen
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()


clock = pygame.time.Clock()

# Create a screen and set window's name
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
screen.set_title('A 2D NORMAL SHOOTING GAME')

# Create custom events
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 250)

# Create the 'player'
player = Player()

# Create groups to hold enemy sprites and all sprites
# - enemies is used for collision detection and position updates
# - all_sprites is used for rendering
enemies = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

running = True
while running:
    pressed_keys = pygame.key.get_pressed()
    clicked_mouse = pygame.mouse.get_pressed()
    
    screen.fill(Black)
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
                
        elif event.type == QUIT:
            running = False
            
         # Add a new enemy?
        elif event.type == ADDENEMY:
            # Create the new enemy and add it to sprite groups
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)
            
    player.update(pressed_keys)
    enemies.update()
    
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)        
    screen.blit(player.surf, player.rect)
    
    # Check if any enemies have collided with the player
    if pygame.sprite.spritecollideany(player, enemies):
        # If so, then remove the player and stop the loop
        player.kill()
        running = False
    
    pygame.display.update()
    
    clock.tick(FPS)
    
pygame.quit()  
