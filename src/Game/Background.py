import pygame

class Background:
    def __init__(self, background_sprite):
        self.x = 0
        self.y = 0
        self.background = pygame.image.load(background_sprite).convert()

    def blitting(self, screen):
        screen.blit(self.background, (self.x, self.y))
        screen.blit(self.background, (self.x + self.background.get_width(), self.y + self.background.get_height()))
