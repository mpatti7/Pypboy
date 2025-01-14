import pygame
from views.home import HomeView


class HomeController():
    def __init__(self, screen):
        self.view = HomeView(screen)


    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if 50 <= x <= 250 and 150 <= y <= 200:  # Button boundaries
                print("Stats button clicked!")


    def update(self):
        # Add any dynamic updates here (e.g., animations)
        pass


    def render(self):
        self.view.draw_background()