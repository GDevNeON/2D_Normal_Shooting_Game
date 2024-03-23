import pygame

from pygame.locals import (
    USEREVENT
)

# Set FPS cho game
FPS = 60

# Screen resolution
SCREEN_WIDTH    = 1366
SCREEN_HEIGHT   = 768
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
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
pygame.time.set_timer(INCREASE_STAT, 10000)
FIRE_RATE = USEREVENT + 3
pygame.time.set_timer(FIRE_RATE, 300)