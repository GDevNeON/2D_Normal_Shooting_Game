import pygame
from pygame.locals import *
from pygame.font import Font
pygame.init()

font = Font(None, 50)

WIDTH_SCREEN = 1920
HEIGHT_SCREEN = 1080
BACKGROUND = "D:/WorkSpace/python_project/python_game_project/2D_Normal_Shooting_Game/src/Menu/assets/imgs/br1.jpg"
BUTTON = "D:/WorkSpace\python_project/python_game_project/2D_Normal_Shooting_Game/src/Menu/assets/imgs/button.png"  

# Game display:
def initialize_screen():
    screen = pygame.display.set_mode((WIDTH_SCREEN, HEIGHT_SCREEN))
    pygame.display.set_caption("2D NORMAL SHOOTING GAME")
    background_image = pygame.image.load(BACKGROUND)

    # Load image
    button_play = pygame.image.load(BUTTON)
    button_settings = pygame.image.load(BUTTON)
    button_quit = pygame.image.load(BUTTON)

    # Scale button images (assuming Pygame version 1.9.1 or later)
    button_play = pygame.transform.scale(button_play, (int(button_play.get_width() * 0.35), int(button_play.get_height() * 0.35)))
    button_settings = pygame.transform.scale(button_settings, (int(button_settings.get_width() * 0.35), int(button_settings.get_height() * 0.35)))
    button_quit = pygame.transform.scale(button_quit, (int(button_quit.get_width() * 0.35), int(button_quit.get_height() * 0.35)))

   # Tính toán vị trí nút dựa trên hình ảnh
    top_offset = 300  # Khoảng cách từ đầu màn hình đến nút đầu tiên
    button_height = button_play.get_height()  # Giả sử tất cả các nút có cùng chiều cao
    button_spacing = 8  # Điều chỉnh giá trị này để kiểm soát khoảng cách giữa các nút

    button_play_rect = button_play.get_rect(center=(WIDTH_SCREEN // 2, top_offset + button_height // 2))
    button_settings_rect = button_settings.get_rect(center=(WIDTH_SCREEN // 2, button_play_rect.bottom + button_spacing + button_height // 2))
    button_quit_rect = button_quit.get_rect(center=(WIDTH_SCREEN // 2, button_settings_rect.bottom + button_spacing + button_height // 2))

    # Create button text surfaces
    button_play_text = font.render("Play", True, (255, 255, 255))  # Text, antialiasing, color
    button_settings_text = font.render("Setting", True, (255, 255, 255))
    button_quit_text = font.render("Exit", True, (255, 255, 255))

    # Blit text onto button images, centering them
    button_play_text_rect = button_play_text.get_rect(center=(button_play_rect.centerx, button_play_rect.centery))  # Điều chỉnh vị trí y của văn bản
    button_settings_text_rect = button_settings_text.get_rect(center=(button_settings_rect.centerx, button_settings_rect.centery ))  # Điều chỉnh vị trí y của văn bản
    button_quit_text_rect = button_quit_text.get_rect(center=(button_quit_rect.centerx, button_quit_rect.centery))  # Điều chỉnh vị trí y của văn bản

    # Blit text onto button images
    button_play.blit(button_play_text, button_play_text_rect)
    button_settings.blit(button_settings_text, button_settings_text_rect)
    button_quit.blit(button_quit_text, button_quit_text_rect)


    return screen, background_image, button_play, button_settings, button_quit, button_play_rect, button_settings_rect, button_quit_rect, button_play_text, button_play_text_rect, button_settings_text, button_settings_text_rect, button_quit_text, button_quit_text_rect

def modify_screen(screen):
    current_width, current_height = screen.get_size()
    if screen.get_flags() & pygame.FULLSCREEN:
        screen = pygame.display.set_mode((1680, 1050))
    else:
        screen = pygame.display.set_mode((WIDTH_SCREEN, HEIGHT_SCREEN), FULLSCREEN)
    return screen