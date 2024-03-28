import pygame

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
LEVEL_WIDTH     = 10000
LEVEL_HEIGHT    = 6000
SCREEN_WIDTH    = 1300
SCREEN_HEIGHT   = 700
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
