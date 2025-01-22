import pygame
from config import BLACK, GREEN, MAIN_GREEN, SCREEN_HEIGHT, SCREEN_WIDTH
from components.button import Button
import requests
import threading
from io import BytesIO


class WeatherView():
    def __init__(self, screen, area, api_key):
        self.screen = screen
        self.area = area
        self.api_key = api_key
        self.weather_data = None
        self.weather_icon = None
        self.font = pygame.font.Font('assets/fonts/monofonto_rg.otf', 20) 
        self.main_font_color = (95, 255, 177, 128)
        self.background_image = pygame.image.load("assets/images/green_weather.png")
        # self.background_image = pygame.transform.scale(self.background_image, (self.area.width * .5, self.area.height * .25))
        self.is_fetching = True

        self.fetch_weather_data_async()
    

    def draw_background(self):

        self.background_image.set_alpha(128)
        self.screen.blit(self.background_image, (self.area.x+550, 25))

        if self.is_fetching:
            self.display_loading_message()
        elif self.weather_data:
            self.display_weather_info()


    def display_loading_message(self):
        loading_text = self.font.render("Loading weather...", True, self.main_font_color)
        text_width = loading_text.get_width()
        text_height = loading_text.get_height()

        center_x = self.area.left + (self.area.width - text_width) // 2
        center_y = self.area.top + (self.area.height - text_height) // 2

        self.screen.blit(loading_text, (center_x, center_y))


    def display_weather_info(self):       
        location = self.weather_data['location']['name'] 
        temp_f = self.weather_data["current"]["temp_f"]
        condition = self.weather_data["current"]["condition"]["text"]

        location_text = self.font.render(f'Location: {location}, {self.weather_data["location"]["region"]}', True, self.main_font_color)
        temp_text = self.font.render(f"Temp: {temp_f}°F", True, self.main_font_color)
        condition_text = self.font.render(condition, True, self.main_font_color)

        self.screen.blit(location_text, (self.area.left + 50, self.area.top + 50))
        self.screen.blit(temp_text, (self.area.left + 50, self.area.top + 90))
        self.screen.blit(condition_text, (self.area.left + 50, self.area.top + 130))    

        if self.weather_icon:
            self.screen.blit(self.weather_icon, (condition_text.get_width() + 65, self.area.top + 105))


    def handle_event(self, event):
        pass


    def fetch_weather_data_async(self):
        thread = threading.Thread(target=self.fetch_weather_data, daemon=True)
        thread.start()


    def fetch_weather_data(self):
        try:
            lat, lon = self.fetch_current_location()
            response = requests.get(
                f"http://api.weatherapi.com/v1/current.json",
                params={"key": self.api_key, "q": f"{lat},{lon}"}
            )
            response.raise_for_status()
            self.weather_data = response.json()

            icon_url = f"http:{self.weather_data['current']['condition']['icon']}"
            self.weather_icon = self.fetch_weather_icon(icon_url)
        except Exception as e:
            print(f"Error fetching weather data: {e}")
        finally:
            self.is_fetching = False
    

    def fetch_weather_icon(self, url):
        try:
            response = requests.get(url)
            response.raise_for_status()
            image_data = BytesIO(response.content)
            return pygame.image.load(image_data)
        except Exception as e:
            print(f"Error fetching weather icon: {e}")
            return None
        

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