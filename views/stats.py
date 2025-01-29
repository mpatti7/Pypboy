import pygame
from config import BLACK, GREEN, MAIN_GREEN, SCREEN_HEIGHT, SCREEN_WIDTH
from components.button import Button
import psutil
import threading
import time
from components.weather_fetcher import WeatherFetcher
from components.special_calculator import SpecialCalculator
from datetime import datetime


class StatsView():
    def __init__(self, screen, area, weather_api_key):
        self.screen = screen
        self.area = area
        self.font = pygame.font.Font('assets/fonts/monofonto_rg.otf', 20)

        self.background_image = pygame.image.load("assets/images/pipboy_stats_no_background.png")
        self.background_image = pygame.transform.scale(self.background_image, (SCREEN_WIDTH * .75, SCREEN_HEIGHT * .75))

        self.current_view = 'main'
        self.special_view = SpecialView(self.screen, self.area, weather_api_key)
        self.perks_view = PerksView(self.screen, self.area)

        self.buttons = [
            Button(self.area.x + 75, 65, 75, 25, "S.P.E.C.I.A.L", self.font, (95, 255, 177), (95, 255, 177), transparent=True, action=self.create_action('S.P.E.C.I.A.L')),
            Button(self.area.right - (self.area.right * .25), 65, 75, 25, "Perks", self.font, (95, 255, 177), (95, 255, 177), transparent=True, action=self.create_action('Perks')),
        ]

            
    def draw_background(self):
        if self.current_view == 'main':
            self.background_image.set_alpha(128)
            center_x = self.area.left + (self.area.width - self.background_image.get_width()) // 2
            center_y = self.area.top + (self.area.height - self.background_image.get_height()) // 2
            self.screen.blit(self.background_image, (center_x, center_y))

        elif self.current_view == 'special':
            self.special_view.draw()

        self.draw_buttons()
    

    def draw_buttons(self):
        for button in self.buttons:
            button.draw(self.screen)
            

    def handle_event(self, event):
        for button in self.buttons:
            button.handle_event(event)
        if self.current_view == 'special':
            self.special_view.handle_event(event)
        elif self.current_view == 'perks':
            self.perks_view.handle_event(event)


    def create_action(self, button_name):
        def action():
            # Set this button active and all others inactive
            for button in self.buttons:
                button.is_active = (button.text == button_name)
            print(f"{button_name} button clicked!")

            if button_name == 'S.P.E.C.I.A.L':
                self.current_view = 'special'
            elif button_name == 'Perks':
                self.current_view = 'perks'

        return action



class SpecialView():
    def __init__(self, screen, area, weather_api_key):
        self.screen = screen
        self.area = area
        self.font = pygame.font.Font('assets/fonts/monofonto_rg.otf', 20)
        self.special_logo = pygame.image.load("assets/images/special_logo.png")
        self.special_logo = pygame.transform.scale(self.special_logo, (SCREEN_WIDTH , SCREEN_HEIGHT * .5))
        self.stats_area = pygame.Rect(self.area.left, 160, self.area.width, self.area.height - 125)
        self.strength_sprite = pygame.image.load("assets/sprite_sheets/strength_sprite_sheet_no_bg.png").convert_alpha()
        self.last_update = pygame.time.get_ticks()
        self.current_frame = 0
        self.main_font_color = (95, 255, 177, 128)

        self.strength_value = 5
        self.perception_value = 5
        self.endurance_value = 5
        self.charisma_value = 5
        self.intelligence_value = 5
        self.agility_value = 5
        self.luck_value = 5

        self.current_stat = None
        self.stats_thread = None 
        self.running = False  # Thread loop condition

        self.cpu_usage = 0
        self.core_usages = []
        self.freq = None
        self.cores = 0
        self.used_memory = 0
        self.total_memory = 0
        self.memory_percent= 0

        self.weather_fetcher = WeatherFetcher(weather_api_key)

        self.buttons = [
            Button(self.area.right - (self.area.right * .96), 125, 75, 25, "Strength", self.font, (95, 255, 177), (95, 255, 177), transparent=True, action=self.create_action('Strength')),
            Button(self.area.right - (self.area.right * .82), 125, 75, 25, "Perception", self.font, (95, 255, 177), (95, 255, 177), transparent=True, action=self.create_action('Perception')),
            Button(self.area.right - (self.area.right * .66), 125, 75, 25, "Endurance", self.font, (95, 255, 177), (95, 255, 177), transparent=True, action=self.create_action('Endurance')),
            Button(self.area.right - (self.area.right * .52), 125, 75, 25, "Charisma", self.font, (95, 255, 177), (95, 255, 177), transparent=True, action=self.create_action('Charisma')),
            Button(self.area.right - (self.area.right * .36), 125, 75, 25, "Intelligence", self.font, (95, 255, 177), (95, 255, 177), transparent=True, action=self.create_action('Intelligence')),
            Button(self.area.right - (self.area.right * .21), 125, 75, 25, "Agility", self.font, (95, 255, 177), (95, 255, 177), transparent=True, action=self.create_action('Agility')),
            Button(self.area.right - (self.area.right * .11), 125, 75, 25, "Luck", self.font, (95, 255, 177), (95, 255, 177), transparent=True, action=self.create_action('Luck')),
        ]

        self.stats_dict = {
            'Strength': self.display_strength,
            'Perception': self.display_perception,
            'Endurance': self.display_endurance,
            'Charisma': self.display_charisma,
            'Intelligence': self.display_intelligence,
            'Agility': self.display_agility,
            'Luck': self.display_luck
        }
    

    def draw(self):
        if self.current_stat == None:
            self.special_logo.set_alpha(128)
            center_x = self.area.left + (self.area.width - self.special_logo.get_width()) // 2
            center_y = self.area.top + (self.area.height - self.special_logo.get_height()) // 1.2
            self.screen.blit(self.special_logo, (center_x, center_y))
        else:
            self.stats_dict[self.current_stat]()

        self.draw_buttons()
    

    def draw_buttons(self):
        for button in self.buttons:
            button.draw(self.screen)


    def handle_event(self, event):
        for button in self.buttons:
            button.handle_event(event)


    def create_action(self, button_name):
        def action():
            # Set this button active and all others inactive
            for button in self.buttons:
                button.is_active = (button.text == button_name)
            print(f"{button_name} button clicked!")

            if button_name in self.stats_dict:
                self.stop_stats_thread()
                self.current_stat = button_name
                self.start_stats_thread(self.current_stat)

        return action


    def start_stats_thread(self, stat_name):
        self.stop_stats_thread()
        self.current_stat = stat_name
        self.running = True
        self.stats_thread = threading.Thread(target=self.update_stats, daemon=True)
        self.stats_thread.start()


    def stop_stats_thread(self):
        self.running = False
        if self.stats_thread:
            self.stats_thread.join()
            self.stats_thread = None
    

    def update_stats(self):
        while self.running:
            if self.current_stat == "Strength":
                self.cpu_usage = psutil.cpu_percent(interval=0.5, percpu=False)
                self.core_usages = psutil.cpu_percent(interval=None, percpu=True)
                self.freq = psutil.cpu_freq()
                self.cores = psutil.cpu_count(logical=True)
                self.used_memory = (psutil.virtual_memory().used // 1024) // 1024
                self.total_memory = (psutil.virtual_memory().available // 1024) // 1024
                self.memory_percent = psutil.virtual_memory().percent
            elif self.current_stat == 'Perception':
                self.weather_fetcher.fetch_weather_data_async()
                if self.weather_fetcher.weather_data != None:
                    self.perception_value, factors_list = SpecialCalculator.calculate_perception(self.weather_fetcher)
            time.sleep(0.1)
        

    def get_sprite_sheet_frames(self, num_frames, frame_width, frame_height):
        frames = []

        scale_factor = min(self.stats_area.width / (num_frames * frame_width), self.stats_area.height / frame_height)
        
        scaled_frame_width = int(frame_width * scale_factor) 
        scaled_frame_height = int(frame_height * scale_factor)

        for i in range(num_frames):
            frame_rect = pygame.Rect(i * frame_width, 0, frame_width, frame_height)
            frame = self.strength_sprite.subsurface(frame_rect).copy()
            # frame = pygame.transform.scale(frame, (scaled_frame_width, scaled_frame_height))
            frames.append(frame)

        return frames


    def animate_sprite(self, screen, x, y, num_frames, frame_width, frame_height):
        frames = self.get_sprite_sheet_frames(num_frames, frame_width, frame_height)
        frame_delay = 150
        now = pygame.time.get_ticks()
        if now - self.last_update > frame_delay:
            self.current_frame = (self.current_frame + 1) % num_frames
            self.last_update = now

        screen.blit(frames[self.current_frame], (x, y))
    

    def display_strength(self):
        col1_x = self.stats_area.left + 50
        col2_x = self.stats_area.left + (self.stats_area.width * 3 // 4)
        y_offset = self.stats_area.top + 10

        cpu_text = self.font.render(f"CPU Usage: {self.cpu_usage:.1f}%", True, (95, 255, 177))
        self.screen.blit(cpu_text, (col1_x, y_offset))
        
        if self.freq:
            freq_text = self.font.render(f"Frequency: {self.freq.current:.1f} MHz", True, (95, 255, 177))
            self.screen.blit(freq_text, (col1_x, y_offset + 25))
        
        memory_text = self.font.render(f"Memory: {self.used_memory} MB/{self.total_memory} MB, {self.memory_percent}%", True, (95, 255, 177)) 
        self.screen.blit(memory_text, (col1_x, y_offset + 50))
        
        cores_text = self.font.render(f"Logical Cores: {self.cores}", True, (95, 255, 177))
        self.screen.blit(cores_text, (col1_x, y_offset + 75))

        for i, core_usage in enumerate(self.core_usages):
            core_text = self.font.render(f"Core {i + 1}: {core_usage:.1f}%", True, (95, 255, 177))
            self.screen.blit(core_text, (col2_x, y_offset + i * 30))

        frame_width = self.strength_sprite.get_width() // 14
        sprite_x = (self.stats_area.left + self.stats_area.width // 2) - frame_width // 2
        sprite_y = y_offset + 50
        self.animate_sprite(self.screen, sprite_x, sprite_y, 14, frame_width, self.strength_sprite.get_height())

        pygame.display.flip()


    def display_perception(self):
        if self.weather_fetcher.weather_data == None:
            loading_text = self.font.render("Loading...", True, self.main_font_color)
            text_width = loading_text.get_width()
            text_height = loading_text.get_height()

            center_x = self.area.left + (self.area.width - text_width) // 2
            center_y = self.area.top + (self.area.height - text_height) // 2

            self.screen.blit(loading_text, (center_x, center_y))
        else:
            diff = self.perception_value - 5
            percep_text = self.font.render(f'Value: {str(self.perception_value)}({"-" if diff < 0 else "+"}){diff}', True, self.main_font_color)
            col1_x = self.stats_area.left + 50
            y_offset = self.stats_area.top + 10
            center_x = self.area.left + (self.area.width - percep_text.get_width()) // 2
            center_y = self.area.top + (self.area.height - percep_text.get_width()) // 2

            self.screen.blit(percep_text, (center_x, center_y))

            
            # for i, (key, value) in enumerate(self.weather_fetcher.weather_data.items()):
            #     weather_text = self.font.render(f"{key}: {value}", True, self.main_font_color)
            #     self.screen.blit(weather_text, (col1_x, y_offset + i * 25))

            pygame.display.flip()


    def display_endurance(self):
        print('Displaying endurance')


    def display_charisma(self):
        print('Displaying charisma')


    def display_intelligence(self):
        print('Displaying intelligence')


    def display_agility(self):
        print('Displaying agility')


    def display_luck(self):
        print('Displaying luck')



class PerksView():
    def __init__(self, screen, area):
        self.screen = screen
        self.area = area
        self.buttons = []


    def handle_event(self, event):
        for button in self.buttons:
            button.handle_event(event)


