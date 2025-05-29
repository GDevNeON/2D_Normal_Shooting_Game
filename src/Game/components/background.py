from ..core.define import (
    LEVEL_WIDTH, LEVEL_HEIGHT
)

class Background:
    def __init__(self, background_sprite):
        self.x = 0
        self.y = 0
        self.background = background_sprite

    def draw(self, screen, camera):
        WIDTH_RATIO = LEVEL_WIDTH / self.background.get_width()
        HEIGHT_RATIO = LEVEL_HEIGHT / self.background.get_height()
        
        for i in range(-int(WIDTH_RATIO) - 1, int(WIDTH_RATIO) + 1, 1):
            for j in range(-int(HEIGHT_RATIO) - 1, int(HEIGHT_RATIO) + 1, 1):
                screen.blit(self.background, (self.x + i * self.background.get_width() + camera.camera.x, 
                                             self.y + j * self.background.get_height() + camera.camera.y))
