import pygame
import os

from pygame.locals import *
from pygame.font import Font
from define import *

pygame.init()

font1 = pygame.font.SysFont("Constantia", 50)
font2 = pygame.font.SysFont("None", 50)

screen = pygame.display.set_mode((WIDTH_SCREEN, HEIGHT_SCREEN))

class Button_Text():
    def __init__(self, x_text, y_text, x_img, y_img, text, img, scale):
        self.x_text = x_text
        self.y_text = y_text
        self.text = text
        width = img.get_width()
        height = img.get_height()
        self.img = pygame.transform.scale(img, (int(width * scale), int(height * scale)))
        self.rect = self.img.get_rect(topleft=(x_img, y_img))

    def draw_button(self):
        screen.blit(self.img, self.rect.topleft)
        text_surface = font1.render(self.text, True, (255, 255, 255))
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
    


def Run_User_Interface():
    
    backgound = pygame.image.load(PATH_TO_BACKGROUND).convert_alpha()
    button_image = pygame.image.load(PATH_TO_BUTTON).convert_alpha()
    
    button_width, button_height = button_image.get_width() * 0.4, button_image.get_height() * 0.3
    screen_center_x = screen.get_width() // 2

    # Calculate the 3/4th height of the screen
    three_fourth_height = int(screen.get_height() * 0.68)

    button_spacing = 140

    # Place the buttons at 3/4th height with button_spacing in between
    button_play = Button_Text(0, 0, screen_center_x - button_width / 2, three_fourth_height - button_height / 2 - button_spacing, "Play", button_image, 0.4)
    button_setting = Button_Text(0, 0, screen_center_x - button_width / 2, three_fourth_height - button_height / 2, "Setting", button_image, 0.4)
    button_quit = Button_Text(0, 0, screen_center_x - button_width / 2, three_fourth_height - button_height / 2 + button_spacing, "Exit", button_image, 0.4)

    running = True
    while running:
        screen.blit(backgound, (0,0))
        
        button_play.draw_button()
        button_setting.draw_button()
        button_quit.draw_button()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_play.is_clicked():
                    print("Button Text clicked: play")
                if button_setting.is_clicked():
                    print("Button Image clicked: setting")
                if button_quit.is_clicked():
                    running = False
                    # pygame.quit()
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    Run_User_Interface()
