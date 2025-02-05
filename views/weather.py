import pygame
from config import BLACK, GREEN, MAIN_GREEN, SCREEN_HEIGHT, SCREEN_WIDTH
from components.button import Button
from components.weather_fetcher import WeatherFetcher


class WeatherView():
    def __init__(self, screen, area, weather_api_key):
        self.screen = screen
        self.area = area
        self.api_key = weather_api_key
        self.font = pygame.font.Font('assets/fonts/monofonto_rg.otf', 20) 
        self.main_font_color = (95, 255, 177, 128)
        self.background_image = pygame.image.load("assets/images/green_weather.png")
        self.background_image = pygame.transform.scale(self.background_image, (self.area.width * .18, self.area.height * .25))
        self.weather_fetcher = WeatherFetcher(weather_api_key)
        self.weather_fetcher.fetch_weather_data_async()

        self.weather_images = {
            'Sunny': 'assets/images/vaultboy_sunny.png',
            'Partly cloudy': '',
            'Rainy': 'assets/images/vaultboy_umbrella.png',
            'Clear': '',
            'Light rain': '',
            'Overcast': ''
        }
    

    def draw_background(self):

        self.background_image.set_alpha(128)
        self.screen.blit(self.background_image, (self.area.right - (self.area.right * .25), self.area.top + (self.area.top * .35)))

        if self.weather_fetcher.is_fetching:
            self.display_loading_message()
        elif self.weather_fetcher.weather_data: 
            self.display_weather_info()


    def display_loading_message(self):
        loading_text = self.font.render("Loading weather...", True, self.main_font_color)
        text_width = loading_text.get_width()
        text_height = loading_text.get_height()

        center_x = self.area.left + (self.area.width - text_width) // 2
        center_y = self.area.top + (self.area.height - text_height) // 2

        self.screen.blit(loading_text, (center_x, center_y))


    def display_weather_info(self):       
        location = self.weather_fetcher.weather_data['location']['name'] 
        temp_f = self.weather_fetcher.weather_data["current"]["temp_f"]
        condition = self.weather_fetcher.weather_data["current"]["condition"]["text"]
        wind_mph = self.weather_fetcher.weather_data['current']['wind_mph']
        wind_chill = self.weather_fetcher.weather_data['current']['windchill_f']
        feels_like_f = self.weather_fetcher.weather_data['current']['feelslike_f']
        uv = self.weather_fetcher.weather_data['current']['uv']

        location_text = self.font.render(f'Location: {location}, {self.weather_fetcher.weather_data["location"]["region"]}', True, self.main_font_color)
        temp_text = self.font.render(f"Temp: {temp_f}°F", True, self.main_font_color)
        condition_text = self.font.render(condition, True, self.main_font_color)
        wind_mph_text = self.font.render(f'Wind: {str(wind_mph)} mph', True, self.main_font_color)
        wind_chill_text = self.font.render(f'Wind Chill: {str(wind_chill)}°F', True, self.main_font_color)
        feels_like_f_text = self.font.render(f'Feels Like: {str(feels_like_f)}°F', True, self.main_font_color)
        uv_text = self.font.render(f'UV: {str(uv)}', True, self.main_font_color)

        self.screen.blit(location_text, (self.area.left + 50, self.area.top + 50))
        self.screen.blit(temp_text, (self.area.left + 50, self.area.top + 90))
        self.screen.blit(condition_text, (self.area.left + 50, self.area.top + 130))  
        self.screen.blit(wind_mph_text, (self.area.left + 50, self.area.top + 170))  
        self.screen.blit(wind_chill_text, (self.area.left + 50, self.area.top + 210))  
        self.screen.blit(feels_like_f_text, (self.area.left + 50, self.area.top + 250))  
        self.screen.blit(uv_text, (self.area.left + 50, self.area.top + 290))  

        try:
            weather_image = pygame.image.load(self.weather_images[condition])
            center_x = self.area.left + (self.area.width - weather_image.get_width()) // 2
            center_y = self.area.top + (self.area.height - weather_image.get_width()) // 2

            self.screen.blit(weather_image, (center_x, center_y))
        except Exception as e:
            pass

        if self.weather_fetcher.weather_icon:
            self.screen.blit(self.weather_fetcher.weather_icon, (condition_text.get_width() + 65, self.area.top + 105))


    def handle_event(self, event):
        pass

    

