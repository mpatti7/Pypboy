import pygame
from config import BLACK, GREEN, MAIN_GREEN, SCREEN_HEIGHT, SCREEN_WIDTH
from components.button import Button
import requests


class MapView():
    def __init__(self, screen, area, api_key):
        self.screen = screen
        self.area = area
        self.api_key = api_key

        self.background_image = pygame.image.load("assets/images/boston_screenshot.png")
        self.background_image = pygame.transform.scale(self.background_image, (area.width, area.height))
    

    def draw_background(self):
        self.background_image.set_alpha(128)
        self.screen.blit(self.background_image, self.area.topleft)
        

    def draw_map(screen, map_path, area):
        map_image = pygame.image.load(map_path)
        scaled_map = pygame.transform.scale(map_image, (area.width, area.height))
        screen.blit(scaled_map, area.topleft)
    

    def handle_event(self, event):
        pass


    def fetch_map_image(lat, lon, api_key, style):
        url = f"https://maps.googleapis.com/maps/api/staticmap"
        params = {
            "center": f"{lat},{lon}",
            "zoom": 15,
            "size": "600x400",
            "maptype": "roadmap",
            "style": '',
            "key": api_key
        }
        response = requests.get(url)
        if response.status_code == 200:
            with open("map_image.png", "wb") as f:
                f.write(response.content)
            return "map_image.png"
        else:
            print("Error fetching map:", response.text)
            return None