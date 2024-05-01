import pygame
import os
import sys
sys.path.insert(0, r"./src/Game")
import main 

from pygame.locals  import *
from pygame.font    import Font
from define         import *
from Sounds         import menu

pygame.init()

font1 = pygame.font.SysFont("Constantia", 30)
font2 = pygame.font.SysFont("None", 60)
screen = pygame.display.set_mode((1344, 750))

class Screen():
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.SCREEN = pygame.display.set_mode((width, height))
    
    def blitt(self, x, y, img):
        self.SCREEN.blit(img, (x, y))
    
    def get_Size(self):
        return [self.SCREEN.get_width(), self.SCREEN.get_height()]
    
    def get_Width(self):
        return self.SCREEN.get_width()

    def get_Height(self):
        return self.SCREEN.get_height()

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

def draw_img(img, scale, x, y):
    sub_img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
    screen.blit(sub_img, (x, y))

def Run_Gameover_Interface():
    game_over_title = pygame.image.load(PATH_TO_GAME_OVER_TITLE).convert_alpha()
    path_button_image = pygame.image.load(PATH_TO_TRY_AGAIN_BUTTON).convert_alpha()
    screen_center_x_1 = screen.get_width() / 3.1
    screen_center_x_2 = screen.get_width() / 1.91
    five_six_height = int(screen.get_height() * 0.8)
    button_width, button_height = path_button_image.get_width() * 0.4, path_button_image.get_height() * 0.3
    back_to_menu = Button_image(screen_center_x_2 - button_width, five_six_height - button_height / 2, path_button_image, 0.6)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if back_to_menu.is_clicked():
                    running = False

        screen.fill(BLACK_COLOR)
        draw_img(game_over_title, 0.3, screen_center_x_1, -20)
        back_to_menu.draw()
        pygame.display.update()
    Run_User_Interface()


def Run_User_Interface():
    pygame.mixer.music.load(menu)
    pygame.mixer.music.play(loops=-1)
    
    #Đường dẫn của background img
    background_img = pygame.image.load(PATH_TO_BACKGROUND).convert_alpha()
    background_selection_menu_img = pygame.image.load(PATH_TO_BACKGROUND_SELECTION_MENU).convert_alpha()

    pygame.display.set_caption('A 2D NORMAL SHOOTING GAME')
    
    #Giảm scale của img xuống
    main_background = pygame.transform.scale(background_img, (int(background_img.get_width() * 0.7), int(background_img.get_height() * 0.7)))
    sub_background = pygame.transform.scale(background_selection_menu_img, (int(background_selection_menu_img.get_width() * 0.7), int(background_selection_menu_img.get_height() * 0.7)))
    
    #Đường dẫn của button img
    path_button_image = pygame.image.load(PATH_TO_START_BUTTON).convert_alpha()
    path_button = pygame.image.load(PATH_TO_SELECT_BUTTON).convert_alpha()
    # map_1 = pygame.image.load(PATH_TO_MAP_1).convert_alpha()
    map = pygame.image.load(PATH_TO_MAP).convert_alpha()
    endless_mode = pygame.image.load(PATH_TO_GAME_MODE_EL).convert_alpha()
    normal_mode = pygame.image.load(PATH_TO_GAME_MODE_NM).convert_alpha()

    male_char = pygame.image.load(PATH_TO_MALE_CHAR).convert_alpha()
    female_char = pygame.image.load(PATH_TO_FEMALE_CHAR).convert_alpha()

    
    #Tính toán vị trí của button
    button_width_select, button_height_select = path_button.get_width() * 0.15, path_button.get_height() * 0.3
    button_width, button_height = path_button_image.get_width() * 0.4, path_button_image.get_height() * 0.3
    screen_center_x = screen.get_width() // 2

    three_fourth_height = int(screen.get_height() * 0.7)
    five_six_height = int(screen.get_height() * 0.75)

    button_spacing = 110

    button_play = Button_Text(0, 0, screen_center_x - button_width, three_fourth_height - button_height / 2 - button_spacing, "", pygame.image.load(PATH_TO_START_BUTTON).convert_alpha(), 0.9)
    button_setting = Button_Text(0, 0, screen_center_x - button_width, three_fourth_height - button_height / 2, "", pygame.image.load(PATH_TO_SETTING_BUTTON).convert_alpha(), 0.9)
    button_quit = Button_Text(0, 0, screen_center_x - button_width, three_fourth_height - button_height / 2 + button_spacing, "", pygame.image.load(PATH_TO_QUIT_BUTTON).convert_alpha(), 0.9)

    button_video_setting_menu = Button_image(210, 180, pygame.image.load(PATH_TO_VIDEO_SETTING_BUTTON).convert_alpha(), 0.5)
    button_audio_setting_menu = Button_image(410, 180, pygame.image.load(PATH_TO_AUDIO_BUTTON).convert_alpha(), 0.5)
    button_close_setting_menu = Button_image(1120, 90, pygame.image.load(PATH_TO_CLOSE_BUTTON).convert_alpha(), 0.1) 

    button_back = Button_image(10, 10, pygame.image.load(PATH_TO_BACK_BUTTON).convert_alpha(), 0.6)
    button_select = Button_Text(0, 0, (screen_center_x - button_width_select) / 1.15, (five_six_height - button_height / 1) + button_spacing, "", pygame.image.load(PATH_TO_SELECT_BUTTON).convert_alpha(), 1.5)

    left = pygame.image.load(PATH_TO_ARROW).convert_alpha()
    right = pygame.image.load(PATH_TO_ARROW).convert_alpha()

    left_arrow = Button_image(270, 300, pygame.transform.rotate(left, 180), 0.8)
    right_arrow = Button_image(1000, 300, right, 0.8)

    title = Button_image(screen_center_x - (pygame.image.load(PATH_TO_TITLE).convert_alpha().get_width()* 0.5), 90, pygame.image.load(PATH_TO_TITLE).convert_alpha(), 1)

    #Biến bật/tắt các menu con, biến đánh dấu
    check_switch_play = False
    check_switch_character_selection = False
    check_switch_settings = False
    check_swich_button_in_menu_setting = True
    # current_mode = 1: normal, = 0: perma
    current_mode = 1   
    # character_select = 1: male, = 0: female
    character_select = 1
    
    running = True
    while running:
        screen.blit(main_background, (0,0))

        if check_switch_play == True:
            screen.blit(sub_background, (0, 0))
            overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 128))
            screen.blit(overlay, (0, 0))

            button_back.draw()
            button_select.draw_button(WHITE_COLOR)

            left_arrow.draw()
            right_arrow.draw()
            
            if current_mode == 0:
                draw_img(endless_mode, 1.2, 585, 120)
                draw_img(map, 0.4, 490, 260)
            else: 
                draw_img(normal_mode, 1.2, 585, 120)
                draw_img(map, 0.4, 490, 260)

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if button_back.is_clicked():
                        check_switch_play = False
                    elif button_select.is_clicked():
                        check_switch_character_selection = True
                        check_switch_play = False
                    if left_arrow.is_clicked():
                        # current_map_index = (current_map_index - 1) % 2
                        current_mode = 1
                    elif right_arrow.is_clicked():
                        # current_map_index = (current_map_index + 1) % 2
                        current_mode = 0
        elif check_switch_character_selection == True:
            screen.blit(sub_background, (0, 0))
            overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 128))
            screen.blit(overlay, (0, 0))

            button_back.draw()
            button_select.draw_button(WHITE_COLOR)

            left_arrow.draw()
            right_arrow.draw()

            draw_text("CHARACTOR SELECTION", font2, WHITE_COLOR, 420, 100)

            if character_select == 1:
                draw_img(male_char, 0.7, 555, 190)
            else:
                draw_img(female_char, 0.7, 542.5, 175)

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if button_back.is_clicked():
                        check_switch_play = True
                        check_switch_character_selection = False
                    elif button_select.is_clicked():
                        running = False
                    if left_arrow.is_clicked():
                        # current_map_index = (current_map_index - 1) % 2
                        character_select = 1
                    elif right_arrow.is_clicked():
                        # current_map_index = (current_map_index + 1) % 2
                        character_select = 0
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
            overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 128))
            screen.blit(overlay, (0, 0))
            title.draw()
            button_play.draw_button(WHITE_COLOR)
            button_setting.draw_button(WHITE_COLOR)
            button_quit.draw_button(WHITE_COLOR)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_play.is_clicked():
                    check_switch_play = True
                if button_setting.is_clicked():
                    check_switch_settings = True  
                if button_quit.is_clicked():
                    pygame.quit()
        pygame.display.update()
    if current_mode == character_select:
        if(current_mode == 1):
            main.Run_Game(current_mode = 1, character_select = 1)
        else:
            main.Run_Game(current_mode = 0, character_select = 0)
    else:
        if(current_mode == 1):
            main.Run_Game(current_mode = 1, character_select = 0)
        else:    
            main.Run_Game(current_mode = 0, character_select = 1)

if __name__ == "__main__":
    Run_User_Interface()
    # Run_Gameover_Interface()
