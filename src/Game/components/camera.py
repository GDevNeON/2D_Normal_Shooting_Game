import pygame

from ..core.define import *

class Camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def update(self, target):
        x = -target.rect.centerx + int(SCREEN_WIDTH / 2)
        y = -target.rect.centery + int(SCREEN_HEIGHT / 2)

        # Giới hạn di chuyển của camera
        x = min(0, x)  # Không di chuyển vượt ra bên trái
        y = min(0, y)  # Không di chuyển vượt ra bên trên
        x = max(-(self.width - SCREEN_WIDTH), x)  # Không di chuyển vượt ra bên phải
        y = max(-(self.height - SCREEN_HEIGHT), y)  # Không di chuyển vượt ra bên dưới

        self.camera = pygame.Rect(x, y, self.width, self.height)
