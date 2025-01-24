import pygame
from config import BLACK, GREEN, MAIN_GREEN, SCREEN_HEIGHT, SCREEN_WIDTH
from components.button import Button
import requests
import threading
import os
import json



class MapView():
    def __init__(self, screen, area, api_key):
        self.screen = screen
        self.area = area
        self.api_key = api_key
        self.font = pygame.font.Font('assets/fonts/monofonto_rg.otf', 20) 
        self.main_font_color = (95, 255, 177, 128)
        self.map_image = None
        self.temp_background_image = pygame.image.load("assets/images/boston_screenshot.png")
        self.temp_background_image = pygame.transform.scale(self.temp_background_image, (area.width, area.height))

        self.is_fetching = True
        self.fetch_map_image_async()
    

    def draw_background(self):
        # self.temp_background_image.set_alpha(128)
        # self.screen.blit(self.temp_background_image, self.area.topleft)
        if self.is_fetching:
            self.display_loading_message()
        elif self.map_image:
            # self.map_image.set_alpha(128)
            center_x = self.area.left + (self.area.width - self.map_image.get_width()) // 2
            center_y = self.area.top + (self.area.height - self.map_image.get_height()) // 2

            self.screen.blit(self.map_image, (center_x, center_y + 15))

    
    def display_loading_message(self):
        loading_text = self.font.render("Loading map...", True, self.main_font_color)
        text_width = loading_text.get_width()
        text_height = loading_text.get_height()

        center_x = self.area.left + (self.area.width - text_width) // 2
        center_y = self.area.top + (self.area.height - text_height) // 2

        self.screen.blit(loading_text, (center_x, center_y))
    

    def handle_event(self, event):
        pass


    def fetch_map_image_async(self):
        thread = threading.Thread(target=self.fetch_map_image, daemon=True)
        thread.start()


    def fetch_map_image(self):
        try:
            lat, lon = self.fetch_current_location()

            cached_map = f'assets/maps/map_image_{lat}_{lon}.png'

            if os.path.exists(cached_map):
                self.map_image = pygame.image.load(cached_map)
                return 'Cached map image used!'

            with open("assets/map_styles/fallout4_map_style.json", "r") as file:
                SNAPPY_MAP_STYLE = json.load(file)
            style = self.convert_snazzy_style_to_query(SNAPPY_MAP_STYLE)

            url = f"https://maps.googleapis.com/maps/api/staticmap"
            params = {
                "center": f"{lat},{lon}",
                "zoom": 15,
                "size": "600x400",
                "maptype": "roadmap",
                "style": '',
                # "markers": f"color:red|label:A|{lat},{lon}",
                "key": self.api_key
            }
            response = requests.get(url, params=params)
            if response.status_code == 200:
                with open(f"assets/maps/map_image_{lat}_{lon}.png", "wb") as f:
                    f.write(response.content)
                self.map_image = pygame.image.load(f"assets/maps/map_image_{lat}_{lon}.png")
                return "Map image saved!"
            else:
                print("Error fetching map:", response.text)
                return None
        except Exception as e:
            print(f'[Error]: {e}')
        finally:
            self.is_fetching = False
    

    def fetch_current_location(self):
        # Fetch current latitude and longitude based on IP address.
        try:
            response = requests.get("http://ip-api.com/json/")
            data = response.json()
            if data["status"] == "success":
                return data["lat"], data["lon"]
            else:
                print("Error fetching location:", data["message"])
                return None, None
        except Exception as e:
            print("Failed to fetch location:", e)
            return None, None
    

    def convert_snazzy_style_to_query(self, style_json):
        # Convert Snazzy Maps JSON style to Google Maps Static API style string.
        style_query = ""
        for rule in style_json:
            feature = f"feature:{rule['featureType']}" if 'featureType' in rule else ""
            element = f"element:{rule['elementType']}" if 'elementType' in rule else ""
            stylers = "|".join(
                [f"{key}:{value.replace('#', '0x')}" if key == "color" else f"{key}:{value}"
                for s in rule.get('stylers', []) for key, value in s.items()]
            )
            style_query += f"style={feature}|{element}|{stylers}&"
        return style_query.rstrip("&")