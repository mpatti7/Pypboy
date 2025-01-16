import pygame
from views.home import HomeView


class HomeController():
    def __init__(self, screen):
        self.view = HomeView(screen)


    def handle_event(self, event):
        self.view.handle_event(event)


    def update(self):
        # Add any dynamic updates here (e.g., animations)
        pass


    def render(self):
        self.view.draw_background()