import pygame
import sys
import sys
from pygame.locals import *
from define import *

pygame.init()

class Text_Create(pygame.sprite.Sprite):
    def __init__(self, text, font_size, color):
        super().__init__()
        self.text = text
        self.font = pygame.font.Font(None, font_size)
        self.color = color
        self.render_text()

    def render_text(self):
        self.image = self.font.render(self.text, True, self.color)
        self.rect = self.image.get_rect()

    def update_text(self, text):
        self.text = text
        self.render_text()


class Button(pygame.sprite.Sprite):
    def __init__(self, image, position):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=position)
        self.clicked = False

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.clicked = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if self.clicked and self.rect.collidepoint(event.pos):
                self.clicked = False
                return True
        return False

    def reset(self):
        self.clicked = False


def initialize_screen():
    WIDTH_SCREEN = 1920 
    HEIGHT_SCREEN = 1080
    screen = pygame.display.set_mode((WIDTH_SCREEN, HEIGHT_SCREEN))
    pygame.display.set_caption("2D NORMAL SHOOTING GAME")

    background_image = pygame.image.load(PATH_TO_BACKGROUND)

    button_play = pygame.image.load(PATH_TO_BUTTON)
    button_settings = pygame.image.load(PATH_TO_BUTTON)
    button_quit = pygame.image.load(PATH_TO_BUTTON)

    button_play = pygame.transform.scale(button_play, (int(button_play.get_width() * 0.35), int(button_play.get_height() * 0.35)))
    button_settings = pygame.transform.scale(button_settings, (int(button_settings.get_width() * 0.35), int(button_settings.get_height() * 0.35)))
    button_quit = pygame.transform.scale(button_quit, (int(button_quit.get_width() * 0.35), int(button_quit.get_height() * 0.35)))

    top_offset = 530  
    button_height = button_play.get_height()  
    button_spacing = -10  
    button_play_rect = button_play.get_rect(center=(WIDTH_SCREEN // 2, top_offset + button_height // 2))
    button_settings_rect = button_settings.get_rect(center=(WIDTH_SCREEN // 2, button_play_rect.bottom + button_spacing + button_height // 2))
    button_quit_rect = button_quit.get_rect(center=(WIDTH_SCREEN // 2, button_settings_rect.bottom + button_spacing + button_height // 2))

    button_play_text = Text_Create("Play", 65, (255, 255, 255))
    button_setting_text = Text_Create("Setting", 65, (255, 255, 255))
    button_exit_text = Text_Create("Exit", 65, (255, 255, 255))

    button_play_text.rect.center = button_play_rect.center
    button_setting_text.rect.center = button_settings_rect.center
    button_exit_text.rect.center = button_quit_rect.center

    return screen, background_image, button_play, button_settings, button_quit, button_play_rect, button_settings_rect, button_quit_rect, button_play_text, button_setting_text, button_exit_text


def show_settings_menu(screen, background_image):
    button_close = pygame.image.load(PATH_TO_CLOSE_BUTTON)
    button_close = pygame.transform.scale(button_close,(int(button_close.get_width() * 0.1), int(button_close.get_height() * 0.1)))
    
    button_close = pygame.transform.scale(button_close,(int(button_close.get_width() * 0.1), int(button_close.get_height() * 0.1)))
    
    overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 128))

    settings_menu_width = 1080
    settings_menu_height = 768

    settings_menu_x = (screen.get_width() - settings_menu_width) / 2
    settings_menu_y = (screen.get_height() - settings_menu_height) / 2

    settings_menu_surface = pygame.Surface((settings_menu_width, settings_menu_height))
    settings_menu_surface.fill((255, 255, 255))
    pygame.draw.rect(settings_menu_surface, (0, 0, 0), settings_menu_surface.get_rect(), 2)
    
    close_button_rect = button_close.get_rect(topright=(settings_menu_width - 50, 50))
    settings_menu_surface.blit(button_close, close_button_rect)
    close_button_rect = button_close.get_rect(topright=(settings_menu_width - 50, 50))
    settings_menu_surface.blit(button_close, close_button_rect)

    video_text = Text_Create("Video", 40, (0,0,0))
    sound_text = Text_Create("Sound", 40, (0,0,0))
    resolution_text = Text_Create("Resolution", 40, (0,0,0))
    
    text_width = video_text.rect.width
    text_spacing = 50
    text_start_x = 100
    video_text.rect.topleft = (text_start_x, 150)
    sound_text.rect.topleft = (text_start_x + text_width + text_spacing, 150)
    resolution_text.rect.topleft = (text_start_x + 2 * (text_width + text_spacing), 150)
    video_text.rect.topleft = (text_start_x, 150)
    sound_text.rect.topleft = (text_start_x + text_width + text_spacing, 150)
    resolution_text.rect.topleft = (text_start_x + 2 * (text_width + text_spacing), 150)
    
    settings_menu_surface.blit(video_text.image, video_text.rect.topleft)
    settings_menu_surface.blit(sound_text.image, sound_text.rect.topleft)
    settings_menu_surface.blit(resolution_text.image, resolution_text.rect.topleft)

    screen.blit(background_image, (0, 0))
    screen.blit(overlay, (0, 0))
    screen.blit(background_image, (0, 0))
    screen.blit(overlay, (0, 0))
    screen.blit(settings_menu_surface, (settings_menu_x, settings_menu_y))
    pygame.display.flip()  # Update the display

    # Xử lý sự kiện trong vòng lặp
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return  # Thoát khỏi hàm nếu nhấn ESC
            if event.type == pygame.MOUSEBUTTONDOWN:
                if close_button_rect.collidepoint(event.pos):
                    return  # Thoát khỏi hàm nếu nút đóng được nhấp
    pygame.display.flip()  # Update the display

    # Xử lý sự kiện trong vòng lặp
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return  # Thoát khỏi hàm nếu nhấn ESC
            if event.type == pygame.MOUSEBUTTONDOWN:
                if close_button_rect.collidepoint(event.pos):
                    return  # Thoát khỏi hàm nếu nút đóng được nhấp


def Run_User_Interface():
    screen, background_image, button_play, button_settings, button_quit, button_play_rect, button_settings_rect, button_quit_rect, button_play_text, button_setting_text, button_exit_text = initialize_screen()

    running = True
    settings_menu_visible = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_settings_rect.collidepoint(event.pos):
                    show_settings_menu(screen, background_image)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_settings_rect.collidepoint(event.pos):
                    show_settings_menu(screen, background_image)

        screen.blit(background_image, (0, 0))
        screen.blit(button_play, button_play_rect)
        screen.blit(button_settings, button_settings_rect)
        screen.blit(button_quit, button_quit_rect)

        screen.blit(button_play_text.image, button_play_text.rect)
        screen.blit(button_setting_text.image, button_setting_text.rect)
        screen.blit(button_exit_text.image, button_exit_text.rect)

        pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
if __name__ == '__main__':
    Run_User_Interface()
    

    