import pygame
from pygame.locals import *
from GUI import *

pygame.init()


# Khởi tạo màn hình game
def main():
    screen, background_image, button_play, button_settings, button_quit, button_play_rect, button_settings_rect, button_quit_rect, button_play_text, button_play_text_rect, button_setting_text, button_setting_text_rect, button_quit_text, button_quit_text_rect = initialize_screen()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                elif event.key == K_x:  # Nhấn phím F để chuyển đổi fullscreen
                    screen = modify_screen(screen)

        # Blit the background and buttons onto the screen
        screen.blit(background_image, (0, 0))
        screen.blit(button_play, button_play_rect )
        screen.blit(button_settings, button_settings_rect)
        screen.blit(button_quit, button_quit_rect)
        screen.blit(button_play_text, button_play_text_rect)
        screen.blit(button_setting_text, button_setting_text_rect)
        screen.blit(button_quit_text, button_quit_text_rect)


        pygame.display.flip()

    pygame.quit()

# Main chay
if __name__ == "__main__":
    main()