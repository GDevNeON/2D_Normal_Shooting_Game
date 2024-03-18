import pygame
from pygame.locals import *
from pygame.font import Font
pygame.init()

font = Font(None, 50)

WIDTH_SCREEN = 1920
HEIGHT_SCREEN = 1080
# BACKGROUND = "2D_Normal_Shooting_Game/src/Menu/assets/imgs/br1.jpg"
# BUTTON = "2D_Normal_Shooting_Game/src/Menu/assets/imgs/button.png"  
BACKGROUND = "./2D_Normal_Shooting_Game/src/Menu/assets/imgs/br1.jpg"
BUTTON = "./2D_Normal_Shooting_Game/src/Menu/assets/imgs/button.png"  

# Giao diện game
def initialize_screen():
    # Building frame
    screen = pygame.display.set_mode((WIDTH_SCREEN, HEIGHT_SCREEN))

    
    # Setting Name
    pygame.display.set_caption("2D NORMAL SHOOTING GAME")
    
    
    # Setting Background
    background_image = pygame.image.load(BACKGROUND)

    # Loading button image
    button_play = pygame.image.load(BUTTON)
    button_settings = pygame.image.load(BUTTON)
    button_quit = pygame.image.load(BUTTON)

    # Decreasing button image
    button_play = pygame.transform.scale(button_play, (int(button_play.get_width() * 0.35), int(button_play.get_height() * 0.35)))
    button_settings = pygame.transform.scale(button_settings, (int(button_settings.get_width() * 0.35), int(button_settings.get_height() * 0.35)))
    button_quit = pygame.transform.scale(button_quit, (int(button_quit.get_width() * 0.35), int(button_quit.get_height() * 0.35)))

    # Caculating button position
    top_offset = 350  # Distance from top to first button
    button_height = button_play.get_height()  # Setting button same height
    button_spacing = 5  # Distance between 2 button
    # Setting button position
    button_play_rect = button_play.get_rect(center=(WIDTH_SCREEN // 2, top_offset + button_height // 2))
    button_settings_rect = button_settings.get_rect(center=(WIDTH_SCREEN // 2, button_play_rect.bottom + button_spacing + button_height // 2))
    button_quit_rect = button_quit.get_rect(center=(WIDTH_SCREEN // 2, button_settings_rect.bottom + button_spacing + button_height // 2))

    # Creating button text
    button_play_text = font.render("Play", True, (255, 255, 255))  # chữ, khử răng cưa, màu
    button_settings_text = font.render("Setting", True, (255, 255, 255))
    button_quit_text = font.render("Exit", True, (255, 255, 255))

    # Adjusting text position
    button_play_text_rect = button_play_text.get_rect(center=(button_play_rect.centerx, button_play_rect.centery))  
    button_settings_text_rect = button_settings_text.get_rect(center=(button_settings_rect.centerx, button_settings_rect.centery ))  
    button_quit_text_rect = button_quit_text.get_rect(center=(button_quit_rect.centerx, button_quit_rect.centery))  

    return screen, background_image, button_play, button_settings, button_quit, button_play_rect, button_settings_rect, button_quit_rect, button_play_text, button_play_text_rect, button_settings_text, button_settings_text_rect, button_quit_text, button_quit_text_rect


#Thay đổi thông số resolution
def modify_screen(screen):
    current_width, current_height = screen.get_size()
    if screen.get_flags() & pygame.FULLSCREEN:
        screen = pygame.display.set_mode((1680, 1050))
    else:
        screen = pygame.display.set_mode((WIDTH_SCREEN, HEIGHT_SCREEN), FULLSCREEN)
    return screen