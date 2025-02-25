import pygame
from config import BLACK, GREEN, MAIN_GREEN, SCREEN_HEIGHT, SCREEN_WIDTH
from components.button import Button
from .stats import StatsView
from .map import MapView
from .weather import WeatherView
from .radio import RadioView
from .game import GameView
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()


class HomeView():
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font('assets/fonts/monofonto_rg.otf', 36)

        self.background_image = pygame.image.load("assets/images/pipboy.png")
        self.background_image = pygame.transform.scale(self.background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

        self.overlay_image = pygame.image.load("assets/images/overlay.png")
        self.overlay_image = pygame.transform.scale(self.overlay_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

        self.border_image = pygame.image.load("assets/images/border.png")
        self.border_image = pygame.transform.scale(self.border_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

        self.header = Header(screen, self.set_active_view)
        self.footer = Footer(screen)

        header_height = 25
        footer_height = 40
        self.content_area = pygame.Rect(0, header_height, screen.get_width(), screen.get_height() - header_height - footer_height)

        self.active_view = StatsView(self.screen, self.content_area, weather_api_key=os.getenv("WEATHER_API_KEY"), stocks_api_key=os.getenv("STOCK_MARKET_API_KEY"))
    

    def set_active_view(self, view_class):
        if view_class == StatsView:
            self.active_view = view_class(self.screen, self.content_area, weather_api_key=os.getenv("WEATHER_API_KEY"), stocks_api_key=os.getenv("STOCK_MARKET_API_KEY"))
        elif view_class == WeatherView:
            self.active_view = view_class(self.screen, self.content_area, weather_api_key=os.getenv("WEATHER_API_KEY"))
        elif view_class == MapView:
            self.active_view = view_class(self.screen, self.content_area, api_key=os.getenv("GOOGLE_MAPS_API_KEY"))
        else:
            self.active_view = view_class(self.screen, self.content_area)


    def draw_background(self):
        self.overlay_image.set_alpha(128)
        self.screen.blit(self.overlay_image, (0, 0))

        self.header.draw_header()
        self.footer.draw_footer()

        if self.active_view:
            self.active_view.draw_background()
    

    def handle_event(self, event):
        self.header.handle_event(event)
        if self.active_view:
            self.active_view.handle_event(event)



class Header():
    def __init__(self, screen, set_active_view_callback):
        self.screen = screen
        self.header_surface = pygame.Surface((SCREEN_WIDTH, 20), pygame.SRCALPHA)
        self.font = pygame.font.Font('assets/fonts/monofonto_rg.otf', 20)
        self.buttons = [
            Button(10, 10, 75, 25, "Stats", self.font, (95, 255, 177), (95, 255, 177), transparent=True, action=self.create_action('Stats'), is_active=True),
            Button(75, 10, 75, 25, "Map", self.font, (95, 255, 177), (95, 255, 177), transparent=True, action=self.create_action('Map')),
            Button(150, 10, 75, 25, "Weather", self.font, (95, 255, 177), (95, 255, 177), transparent=True, action=self.create_action('Weather')),
            Button(225, 10, 75, 25, "Game", self.font, (95, 255, 177), (95, 255, 177), transparent=True, action=self.create_action('Game')),
            Button(300, 10, 75, 25, "Radio", self.font, (95, 255, 177), (95, 255, 177), transparent=True, action=self.create_action('Radio')),
        ]
        self.set_active_view = set_active_view_callback


    def draw_header(self):
        self.header_surface.fill((0, 0, 0, 0))  # Transparent background
        color = (95, 255, 177, 128)

        pygame.draw.line(self.header_surface, color, (5, 5), (5, 25), 2)
        pygame.draw.line(self.header_surface, color, (5, 5), (SCREEN_WIDTH - 154, 5), 2)
        pygame.draw.line(self.header_surface, color, (SCREEN_WIDTH - 154, 5), (SCREEN_WIDTH - 154, 25), 2)
        pygame.draw.line(self.header_surface, color, (SCREEN_WIDTH - 148, 5), (SCREEN_WIDTH - 13, 5), 2)
        pygame.draw.line(self.header_surface, color, (SCREEN_WIDTH - 13, 5), (SCREEN_WIDTH - 13, 25), 2)

        self.draw_buttons()

        self.screen.blit(self.header_surface, (0, 0))

        return self.buttons
    

    def draw_buttons(self):
        for button in self.buttons:
            button.draw(self.screen)


    def handle_event(self, event):
        # Delegate event handling to buttons
        for button in self.buttons:
            button.handle_event(event)
    

    def create_action(self, button_name):
        def action():
            # Set this button active and all others inactive
            for button in self.buttons:
                button.is_active = (button.text == button_name)
            print(f"{button_name} button clicked!")

            if button_name == "Stats":
                self.set_active_view(StatsView)
            elif button_name == "Map":
                self.set_active_view(MapView)
            elif button_name == "Weather":
                self.set_active_view(WeatherView)
            elif button_name == "Radio":
                self.set_active_view(RadioView)
            elif button_name == 'Game':
                self.set_active_view(GameView)

        return action


    def draw_button(self, btn_text, btn_color, left, right, width, height, font_x, font_y=7):
        pygame.draw.rect(self.header_surface, btn_color, (left, right, width, height))
        button_text = self.font.render(btn_text, True, btn_color)
        self.screen.blit(button_text, (font_x, font_y))
        self.buttons[btn_text] = pygame.Rect(left, right, width, height)



class Footer():
    def __init__(self, screen):
        self.screen = screen
        self.footer_surface = pygame.Surface((SCREEN_WIDTH, 20), pygame.SRCALPHA)
        self.font = pygame.font.Font('assets/fonts/monofonto_rg.otf', 20) 


    def draw_footer(self):
        self.footer_surface.fill((0, 0, 0, 0))  # Transparent background

        footer_top = SCREEN_HEIGHT - 20
        footer_bottom = SCREEN_HEIGHT - 2
        color = (95, 255, 177, 128)

        # Draw lines onto the footer surface
        pygame.draw.line(self.footer_surface, color, (5, 0), (5, 18), 2)

        current_time = datetime.now()
        formatted_time = current_time.strftime("%Y-%m-%d %H:%M")
        formatted_time = self.font.render(formatted_time, True, color)
        self.footer_surface.blit(formatted_time, (15, -5))

        pygame.draw.line(self.footer_surface, color, (5, 18), (SCREEN_WIDTH - 13, 18), 2)
        pygame.draw.line(self.footer_surface, color, (SCREEN_WIDTH - 13, 0), (SCREEN_WIDTH - 13, 18), 2)

        self.screen.blit(self.footer_surface, (0, footer_top))







        # # Example text
        # text_surface = self.font.render("Welcome to the Pipboy", True, GREEN)
        # self.screen.blit(text_surface, (50, 50))

        # # Example button
        # pygame.draw.rect(self.screen, GREEN, (50, 150, 200, 50))
        # button_text = self.font.render("Stats", True, BLACK)
        # self.screen.blit(button_text, (100, 160))