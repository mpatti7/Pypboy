import pygame
from config import BLACK, GREEN, MAIN_GREEN, SCREEN_HEIGHT, SCREEN_WIDTH
from components.button import Button


class RadioView():
    def __init__(self, screen, area):
        self.screen = screen
        self.area = area

        self.background_image = pygame.image.load("assets/images/radio.png")
        # self.background_image = pygame.transform.scale(self.background_image, (self.area.width * .5, self.area.height * .25))
    

    def draw_background(self):
        self.background_image.set_alpha(128)
        self.screen.blit(self.background_image, (self.area.x, 25))
    

    def handle_event(self, event):
        pass