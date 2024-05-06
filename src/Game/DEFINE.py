import pygame
import os

from pygame.locals import (
    RLEACCEL, USEREVENT, FULLSCREEN, RESIZABLE,
    K_w, K_a, K_s, K_d, K_q,
    K_ESCAPE, KEYDOWN, QUIT,
)

# Set FPS cho game
FPS = 60

# Screen resolution
LEVEL_WIDTH     = 5000
LEVEL_HEIGHT    = 5000
SCREEN_WIDTH    = 1366
SCREEN_HEIGHT   = 768
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), RESIZABLE)

# Mã màu
Black   = (0,0,0)
White   = (255,255,255)
Red	    = (255,0,0)
Yellow  = (255,255,0)

# Tạo sự kiện
ADD_ENEMY = USEREVENT + 1
pygame.time.set_timer(ADD_ENEMY, 3000)
INCREASE_STAT = USEREVENT + 2
pygame.time.set_timer(INCREASE_STAT, 60000)
ADD_ELITE = USEREVENT + 3
pygame.time.set_timer(ADD_ELITE, 60000)
