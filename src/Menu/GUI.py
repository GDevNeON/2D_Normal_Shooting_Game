import pygame
import os
import sys
sys.path.insert(0, r"D:\WorkSpace\python_project\python_game_project\2D_Normal_Shooting_Game\src\Game")
import main # type: ignore


from pygame.locals import *
from pygame.font import Font
from define import *

pygame.init()

font1 = pygame.font.SysFont("Constantia", 30)
font2 = pygame.font.SysFont("None", 20)

# screen = pygame.display.set_mode((WIDTH_SCREEN * 0.7, HEIGHT_SCREEN * 0.7))
screen = pygame.display.set_mode((1344, 750))
class Button_Text():
    def __init__(self, x_text, y_text, x_img, y_img, text, img, scale):
        self.x_text = x_text
        self.y_text = y_text
        self.text = text
        width = img.get_width()
        height = img.get_height()
        self.img = pygame.transform.scale(img, (int(width * scale), int(height * scale)))
        self.rect = self.img.get_rect(topleft=(x_img, y_img))

    def draw_button(self, color):
        screen.blit(self.img, self.rect.topleft)
        text_surface = font1.render(self.text, True, color)
        text_rect = text_surface.get_rect(center=(self.rect.centerx, self.rect.centery))
        screen.blit(text_surface, text_rect)

    def is_clicked(self):
        pos = pygame.mouse.get_pos()
        button_rect = self.rect
        if button_rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                return True
        return False
    
class Button_image():
    def __init__(self, x, y, img, scale):
        width = img.get_width()
        height = img.get_height() 
        self.img = pygame.transform.scale(img, (int(width * scale), int(height * scale)))
        self.rect = self.img.get_rect()
        self.rect.topleft = (x, y)

    def draw(self):
        screen.blit(self.img, (self.rect.x, self.rect.y))

    def is_clicked(self):
        pos = pygame.mouse.get_pos()
        button_rect = self.rect
        if button_rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                return True
        return False
    

def draw_text(text, font, text_color, x, y):
    img = font.render(text, True, text_color)
    screen.blit(img, (x, y))

def draw_map(img, scale, x, y):
    sub_img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
    screen.blit(sub_img, (x, y))


def Run_User_Interface():
    #Đường dẫn của background img
    background_img = pygame.image.load(PATH_TO_BACKGROUND).convert_alpha()
    background_selection_menu_img = pygame.image.load(PATH_TO_BACKGROUND_SELECTION_MENU).convert_alpha()
    
    #Giảm scale của img xuống
    main_background = pygame.transform.scale(background_img, (int(background_img.get_width() * 0.7), int(background_img.get_height() * 0.7)))
    sub_background = pygame.transform.scale(background_selection_menu_img, (int(background_selection_menu_img.get_width() * 0.7), int(background_selection_menu_img.get_height() * 0.7)))
    
    #Đường dẫn của button img
    path_button_image = pygame.image.load(PATH_TO_BUTTON).convert_alpha()
    path_button_settings_video = pygame.image.load(PATH_TO_VIDEO_SETTING_BUTTON).convert_alpha()
    path_button_settings_audio = pygame.image.load(PATH_TO_AUDIO_BUTTON).convert_alpha()
    path_button_settings_close = pygame.image.load(PATH_TO_CLOSE_BUTTON).convert_alpha() 
    path_button_back = pygame.image.load(PATH_TO_BACK_BUTTON).convert_alpha()
    path_button_select = pygame.image.load(PATH_TO_SELECT_BUTTON).convert_alpha()
    map_1 = pygame.image.load(PATH_TO_MAP_1).convert_alpha()
    map_2 = pygame.image.load(PATH_TO_MAP_2).convert_alpha()
    
    #Tính toán vị trí của button
    button_width, button_height = path_button_image.get_width() * 0.4, path_button_image.get_height() * 0.3
    screen_center_x = screen.get_width() // 2

    three_fourth_height = int(screen.get_height() * 0.7)
    five_six_height = int(screen.get_height() * 0.9)

    button_spacing = 120

    button_play = Button_Text(0, 0, screen_center_x - button_width / 2, three_fourth_height - button_height / 2 - button_spacing, "Play", path_button_image, 0.3)
    button_setting = Button_Text(0, 0, screen_center_x - button_width / 2, three_fourth_height - button_height / 2, "Setting", path_button_image, 0.3)
    button_quit = Button_Text(0, 0, screen_center_x - button_width / 2, three_fourth_height - button_height / 2 + button_spacing, "Exit", path_button_image, 0.3)

    button_video_setting_menu = Button_image(210, 180, path_button_settings_video, 0.5)
    button_audio_setting_menu = Button_image(410, 180, path_button_settings_audio, 0.5)
    button_close_setting_menu = Button_image(1120, 90, path_button_settings_close, 0.1)

    button_back = Button_image(0, 0, path_button_back, 0.1)
    button_select = Button_Text(0, 0, (screen_center_x - button_width / 2) + 10, five_six_height - button_height / 2 - button_spacing, "Select", path_button_select, 0.15)

    left = pygame.image.load(PATH_TO_ARROW).convert_alpha()
    right = pygame.image.load(PATH_TO_ARROW).convert_alpha()

    left_arrow = Button_image(270, 300, pygame.transform.rotate(left, 180), 0.025)
    right_arrow = Button_image(1000, 300, right, 0.025)


    #Biến bật/tắt các menu con, biến đánh dấu
    check_switch_play = False
    check_switch_settings = False
    check_swich_button_in_menu_setting = True
    current_map_index = 0   
    
    running = True
    while running:
        screen.blit(main_background, (0,0))

        if check_switch_play == True:
            screen.blit(sub_background, (0, 0))
            overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 128))
            screen.blit(overlay, (0, 0))

            button_back.draw()
            button_select.draw_button(BLACK_COLOR)

            left_arrow.draw()
            right_arrow.draw()
            
            if current_map_index == 0:
                draw_map(map_1, 0.65, 437, 200)
            else: 
                draw_map(map_2, 0.5, 442, 150)

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if button_back.is_clicked():
                        check_switch_play = False
                    elif button_select.is_clicked():
                        # bỏ hàm run vào đây
                        print("Select Button is clicked")
                    if left_arrow.is_clicked():
                        current_map_index = (current_map_index - 1) % 2
                    elif right_arrow.is_clicked():
                        current_map_index = (current_map_index + 1) % 2

        elif check_switch_settings == True:
            overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 128))
            screen.blit(overlay, (0, 0))
            settings_menu_width = 1024
            settings_menu_height = 576

            settings_menu_x = (screen.get_width() - settings_menu_width) / 2
            settings_menu_y = (screen.get_height() - settings_menu_height) / 2

            settings_menu_surface = pygame.Surface((settings_menu_width, settings_menu_height))
            settings_menu_surface.fill((BLACK_COLOR))
            pygame.draw.rect(settings_menu_surface, (0, 0, 0), settings_menu_surface.get_rect(), 2)
            screen.blit(settings_menu_surface, (settings_menu_x, settings_menu_y))
            
            button_video_setting_menu.draw()
            button_audio_setting_menu.draw()
            button_close_setting_menu.draw()

            draw_text("Setting Menu", font1, WHITE_COLOR, 585, 120)
            
            if check_swich_button_in_menu_setting == True:
                draw_text("Resolution:", font1, WHITE_COLOR, 220, 250)
                draw_text("Video Mode:", font1, WHITE_COLOR ,220, 450)
                draw_text("1920 x 1080", font1, WHITE_COLOR, 480, 250)
                draw_text("1344 x 750", font1, WHITE_COLOR, 480, 350)
                draw_text("Fullscreen", font1, WHITE_COLOR, 480, 450)
                draw_text("Window", font1, WHITE_COLOR, 480, 550)
            else:
                draw_text("Music:", font1, WHITE_COLOR, 220, 280)
                draw_text("Mute", font1, WHITE_COLOR, 480,280)
                draw_text("Unmute", font1, WHITE_COLOR, 480,380)

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if button_close_setting_menu.is_clicked():
                        check_switch_settings = False
                    if button_audio_setting_menu.is_clicked():
                        check_swich_button_in_menu_setting = False
                    elif button_video_setting_menu.is_clicked():
                        check_swich_button_in_menu_setting = True
        else:
            button_play.draw_button(WHITE_COLOR)
            button_setting.draw_button(WHITE_COLOR)
            button_quit.draw_button(WHITE_COLOR)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_play.is_clicked():
                    check_switch_play = True
                if button_setting.is_clicked():
                    check_switch_settings = True
                        
                if button_quit.is_clicked():
                    running = False
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    Run_User_Interface()
