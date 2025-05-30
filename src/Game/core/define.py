import pygame
import os

from pygame.locals import (
    RLEACCEL, USEREVENT, FULLSCREEN, RESIZABLE,
    K_w, K_a, K_s, K_d, K_q, K_p,
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
Red     = (255,0,0)
Yellow  = (255,255,0)

# Tạo sự kiện
ADD_ENEMY = USEREVENT + 1
pygame.time.set_timer(ADD_ENEMY, 7000)  # 7 giây
INCREASE_STAT = USEREVENT + 2
pygame.time.set_timer(INCREASE_STAT, 60000)  # 1 phút
ADD_ELITE = USEREVENT + 3
pygame.time.set_timer(ADD_ELITE, 40000)  # 40 giây

# Boss events
ADD_BOSS = USEREVENT + 4
BOSS_DASH = USEREVENT + 5
BOSS_SKILL_1 = USEREVENT + 6
BOSS_SKILL_2 = USEREVENT + 7
BOSS_PHASE_TRANSITION = USEREVENT + 8
BOSS_DEFEATED = USEREVENT + 9
BOSS_SPAWN_FEATHERS = USEREVENT + 10

# Set timers for boss events (these can be overridden in the boss class)
pygame.time.set_timer(ADD_BOSS, 300000)  # 5 phút (for endless mode)
pygame.time.set_timer(BOSS_DASH, 5000)  # 5 giây (will be reset in boss class)
pygame.time.set_timer(BOSS_SKILL_1, 10000)  # 10 giây (will be reset in boss class)

def clear_all_timers():
    """Clear all active pygame timers"""
    # Clear all user events (events with IDs >= USEREVENT and < NUMEVENTS)
    for event_id in range(pygame.USEREVENT, pygame.NUMEVENTS):
        pygame.time.set_timer(event_id, 0)

def clear_timers():
    """Clear all game-specific timers"""
    clear_all_timers()  # Clear all timers first
    # Then set up any default timers if needed
    # pygame.time.set_timer(ADD_ENEMY, 7000)  # Uncomment and set default values if needed

def reset_timer():
    clear_timers()