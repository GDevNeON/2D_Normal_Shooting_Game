import pygame

from img                import *
from pygame.locals      import *
from pygame.font        import Font
from define             import *
from define             import SCREEN 

def draw_text(text, font, text_color, x, y):
    img = font.render(text, True, text_color)
    SCREEN.blit(img, (x, y))

def draw_img(img, scale, x, y):
    sub_img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
    SCREEN.blit(sub_img, (x, y))