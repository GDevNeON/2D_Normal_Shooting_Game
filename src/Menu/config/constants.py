import pygame
import os

# Screen dimensions
WIDTH_SCREEN = 1344
HEIGHT_SCREEN = 750.4
SCREEN = pygame.display.set_mode((WIDTH_SCREEN, HEIGHT_SCREEN))

# Colors
WHITE_COLOR = (255, 255, 255)
BLACK_COLOR = (0, 0, 0)
GRAY_COLOR = (100, 100, 100)
LIGHT_GRAY_COLOR = (200, 200, 200)
RED_COLOR = (255, 0, 0)
GREEN_COLOR = (0, 255, 0)
BLUE_COLOR = (0, 0, 255)

# Asset paths
PATH_DIRECTORY = os.path.dirname(os.path.dirname(__file__))

# Title and backgrounds
PATH_TO_TITLE = os.path.join(PATH_DIRECTORY, "assets/imgs/title-1.png.png")
PATH_TO_BACKGROUND = os.path.join(PATH_DIRECTORY, "assets/imgs/br1.jpg")
PATH_TO_BACKGROUND_SELECTION_MENU = os.path.join(PATH_DIRECTORY, "assets/imgs/br2.jpg")

# Main menu buttons
PATH_TO_START_BUTTON = os.path.join(PATH_DIRECTORY, "assets/imgs/start_button.png")
PATH_TO_SETTING_BUTTON = os.path.join(PATH_DIRECTORY, "assets/imgs/option_button.png")
PATH_TO_QUIT_BUTTON = os.path.join(PATH_DIRECTORY, "assets/imgs/quit button.png")

# Settings menu buttons
PATH_TO_CLOSE_BUTTON = os.path.join(PATH_DIRECTORY, "assets/imgs/close_button.png")
PATH_TO_VIDEO_SETTING_BUTTON = os.path.join(PATH_DIRECTORY, "assets/imgs/button_video.png")
PATH_TO_AUDIO_BUTTON = os.path.join(PATH_DIRECTORY, "assets/imgs/button_audio.png")

# Selection menu buttons
PATH_TO_SELECT_BUTTON = os.path.join(PATH_DIRECTORY, "assets/imgs/selectbutton.png")
PATH_TO_BACK_BUTTON = os.path.join(PATH_DIRECTORY, "assets/imgs/xbutton.png")
PATH_TO_ARROW = os.path.join(PATH_DIRECTORY, "assets/imgs/arrowbutton.png") 
PATH_TO_MAP = os.path.join(PATH_DIRECTORY, "assets/imgs/grassfield.png")

# Game over assets
PATH_TO_GAME_OVER_TITLE = os.path.join(PATH_DIRECTORY, "assets/imgs/game_over.png")
PATH_TO_TRY_AGAIN_BUTTON = os.path.join(PATH_DIRECTORY, "assets/imgs/back button.png")

# Game modes
PATH_TO_GAME_MODE_NM = os.path.join(PATH_DIRECTORY, "assets/imgs/normalbutton.png")
PATH_TO_GAME_MODE_EL = os.path.join(PATH_DIRECTORY, "assets/imgs/endlessbutton.png")

# Characters
PATH_TO_MALE_CHAR = os.path.join(PATH_DIRECTORY, "assets/imgs/malemc.png")
PATH_TO_FEMALE_CHAR = os.path.join(PATH_DIRECTORY, "assets/imgs/femalemc.png")

# Default font settings
DEFAULT_FONT = "Constantia"
TITLE_FONT_SIZE = 60
NORMAL_FONT_SIZE = 30
