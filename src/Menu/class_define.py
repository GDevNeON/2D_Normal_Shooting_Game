import pygame

from define     import *

class Button_image():
    def __init__(self, x, y, img, scale):
        width = img.get_width()
        height = img.get_height() 
        self.img = pygame.transform.scale(img, (int(width * scale), int(height * scale)))
        self.rect = self.img.get_rect()
        self.rect.topleft = (x, y)

    def draw(self):
        SCREEN.blit(self.img, (self.rect.x, self.rect.y))

    def is_clicked(self):
        pos = pygame.mouse.get_pos()
        button_rect = self.rect
        if button_rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                return True
        return False