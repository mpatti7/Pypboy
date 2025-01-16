import pygame
from config import BLACK, GREEN, MAIN_GREEN, SCREEN_HEIGHT, SCREEN_WIDTH
from components.button import Button


class StatsView():
    def __init_(self, screen):
        self.background_image = pygame.image.load("assets/images/pipboy.png")
        self.background_image = pygame.transform.scale(self.background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

        self.overlay_image = pygame.image.load("assets/images/overlay.png")
        self.overlay_image = pygame.transform.scale(self.overlay_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

        self.border_image = pygame.image.load("assets/images/border.png")
        self.border_image = pygame.transform.scale(self.border_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    

    def draw_background(self):
        self.screen.blit(self.border_image, (0, 0))
        self.screen.blit(self.background_image, (0, 0))
        self.overlay_image.set_alpha(128)
        self.screen.blit(self.overlay_image, (0, 0))


