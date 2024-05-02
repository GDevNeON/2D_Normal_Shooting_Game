import pygame

from define     import *

title_img                           = pygame.image.load(PATH_TO_TITLE).convert_alpha()

background_img                      = pygame.image.load(PATH_TO_BACKGROUND).convert_alpha()
background_selection_menu_img       = pygame.image.load(PATH_TO_BACKGROUND_SELECTION_MENU).convert_alpha()

play_button_img                     = pygame.image.load(PATH_TO_START_BUTTON).convert_alpha()
setting_button_img                  = pygame.image.load(PATH_TO_SETTING_BUTTON).convert_alpha()
quit_button_img                     = pygame.image.load(PATH_TO_QUIT_BUTTON).convert_alpha()

setting_menu_button_img             = pygame.image.load(PATH_TO_VIDEO_SETTING_BUTTON).convert_alpha()
audio_button_img                    = pygame.image.load(PATH_TO_AUDIO_BUTTON).convert_alpha()
close_button_img                    = pygame.image.load(PATH_TO_CLOSE_BUTTON).convert_alpha()

back_button_img                     = pygame.image.load(PATH_TO_BACK_BUTTON).convert_alpha()
select_button_img                   = pygame.image.load(PATH_TO_SELECT_BUTTON).convert_alpha()

path_button_image                   = pygame.image.load(PATH_TO_START_BUTTON).convert_alpha()
path_button                         = pygame.image.load(PATH_TO_SELECT_BUTTON).convert_alpha()

map                                 = pygame.image.load(PATH_TO_MAP).convert_alpha()
endless_mode                        = pygame.image.load(PATH_TO_GAME_MODE_EL).convert_alpha()
normal_mode                         = pygame.image.load(PATH_TO_GAME_MODE_NM).convert_alpha()

male_char                           = pygame.image.load(PATH_TO_MALE_CHAR).convert_alpha()
female_char                         = pygame.image.load(PATH_TO_FEMALE_CHAR).convert_alpha()

left                                = pygame.image.load(PATH_TO_ARROW).convert_alpha()
right                               = pygame.image.load(PATH_TO_ARROW).convert_alpha()
