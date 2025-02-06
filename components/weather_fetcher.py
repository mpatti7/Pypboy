import requests
from io import BytesIO
import threading
import pygame
from components.luck_manager import LuckManager


class WeatherFetcher():
    def __init__(self, api_key):
        self.api_key = api_key
        self.weather_data = None
        self.weather_icon = None
        self.is_fetching = True
        self.luck_manager = LuckManager()
    

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
            self.luck_manager.set_weather_data(self.weather_data)
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
            response = requests.get("https://ipinfo.io/json")
            data = response.json()
            if 'loc' in data:
                return data['loc'].split(',')
            else:
                print("Error fetching location: ", data)
                return None, None
        except Exception as e:
            print(f"[ERROR] in weather_fetcher.py: Failed to fetch location:", e)
            return None, None