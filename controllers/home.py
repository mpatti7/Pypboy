import pygame
from views.home import HomeView
from views.stats import StatsView
from views.map import MapView
from views.weather import WeatherView
from views.game import GameView
from views.radio import RadioView

# Map view names to view classes
VIEW_CLASSES = {
    "Stats": StatsView,
    "Map": MapView,
    "Weather": WeatherView,
    "Game": GameView,
    "Radio": RadioView
}


class HomeController():
    def __init__(self, screen, ROTARY_SWITCH_EVENT):
        self.view = HomeView(screen)
        self.rotary_switch_event = ROTARY_SWITCH_EVENT


    def handle_event(self, event):
        if event.type == self.rotary_switch_event:
            view_name = event.view_name
            if view_name in VIEW_CLASSES:
                print(f"Switching to {view_name} View")
                self.view.set_active_view(VIEW_CLASSES[view_name])
        
        self.view.handle_event(event)


    def update(self):
        # Add any dynamic updates here (e.g., animations)
        pass


    def render(self):
        self.view.draw_background()