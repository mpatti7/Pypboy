import pygame
from config import BLACK, GREEN, MAIN_GREEN, SCREEN_HEIGHT, SCREEN_WIDTH
from components.button import Button
import psutil
import threading
import time
from components.weather_fetcher import WeatherFetcher
from components.special_calculator import SpecialCalculator
from components.charisma_monitor import CharismaMonitor
from components.stocks_fetcher import StocksFetcher
from components.speed_fetcher import SpeedFetcher
from datetime import datetime
import platform
import subprocess


class StatsView():
    def __init__(self, screen, area, weather_api_key, stocks_api_key):
        self.screen = screen
        self.area = area
        self.font = pygame.font.Font('assets/fonts/monofonto_rg.otf', 20)

        self.background_image = pygame.image.load("assets/images/pipboy_stats_no_background.png")
        self.background_image = pygame.transform.scale(self.background_image, (SCREEN_WIDTH * .75, SCREEN_HEIGHT * .75))

        self.current_view = 'main'
        self.special_view = SpecialView(self.screen, self.area, weather_api_key, stocks_api_key)
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
    CHARISMA_REFRESH_INTERVAL = 180

    def __init__(self, screen, area, weather_api_key, stocks_api_key):
        self.screen = screen
        self.area = area
        self.font = pygame.font.Font('assets/fonts/monofonto_rg.otf', 20)
        self.special_logo = pygame.image.load("assets/images/special_logo.png")
        self.special_logo = pygame.transform.scale(self.special_logo, (SCREEN_WIDTH , SCREEN_HEIGHT * .5))
        self.stats_area = pygame.Rect(self.area.left, 160, self.area.width, self.area.height - 125)
        self.strength_sprite = pygame.image.load("assets/sprite_sheets/strength_sprite_sheet_no_bg.png").convert_alpha()
        self.perception_sprite = pygame.image.load("assets/sprite_sheets/perception_sprite_sheet_no_bg.png").convert_alpha()
        self.endurance_sprite = pygame.image.load("assets/sprite_sheets/endurance_sprite_sheet_no_bg.png").convert_alpha()
        self.charisma_sprite = pygame.image.load("assets/sprite_sheets/charisma_sprite_sheet_no_bg.png").convert_alpha()
        self.intelligence_sprite = pygame.image.load("assets/sprite_sheets/intelligence_sprite_sheet_no_bg.png").convert_alpha()
        self.agility_sprite = pygame.image.load("assets/sprite_sheets/agility_sprite_sheet_no_bg.png").convert_alpha()

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
        self.charisma_thread = None
        self.running = False  # Thread loop condition

        self.cpu_usage = 0
        self.core_usages = []
        self.freq = None
        self.cores = 0
        self.used_memory = 0
        self.total_memory = 0
        self.memory_percent= 0

        self.uptime_hours = 0
        self.cpu_temp = 50

        self.base_ip = "192.168.50"  # Replace with your subnet if different
        self.gateway_ip = "192.168.50.1"  # Typical gateway IP
        self.devices = {}
        self.device_count = 0
        self.gateway_status = None

        self.weather_fetcher = WeatherFetcher(weather_api_key)
        self.charisma_monitor = CharismaMonitor(self.base_ip, self.gateway_ip, self)
        self.stocks_fetcher = StocksFetcher(stocks_api_key)
        self.speed_fetcher = SpeedFetcher()

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
        self.start_charisma_monitor()

        while self.running:
            if self.current_stat == "Strength":
                self.cpu_usage = psutil.cpu_percent(interval=0.5, percpu=False)
                self.core_usages = psutil.cpu_percent(interval=None, percpu=True)
                self.freq = psutil.cpu_freq()
                self.cores = psutil.cpu_count(logical=True)
                self.used_memory = (psutil.virtual_memory().used // 1024) // 1024
                self.total_memory = (psutil.virtual_memory().available // 1024) // 1024
                self.memory_percent = psutil.virtual_memory().percent
                self.strength_value = SpecialCalculator.calculate_strength(self.cpu_usage, self.freq.current, self.used_memory, self.cores, self.core_usages)

            elif self.current_stat == 'Perception':
                self.weather_fetcher.fetch_weather_data_async()
                if self.weather_fetcher.weather_data != None:
                    self.perception_value, factors_list = SpecialCalculator.calculate_perception(self.weather_fetcher)

            elif self.current_stat == 'Endurance':
                uptime_seconds = time.time() - psutil.boot_time()
                self.uptime_hours = uptime_seconds // 3600

                try:
                    temp_sensor = psutil.sensors_temperatures().get("cpu-thermal", [])
                    self.cpu_temp = temp_sensor[0].current if temp_sensor else 50.0  # Assume 50°C if unavailable
                except Exception as e:
                    print(f'[Error]: in update_stats, endurance: {e}')
                    self.cpu_temp = 50.0
                
                self.endurance_value = SpecialCalculator.calculate_endurance(self.uptime_hours, self.cpu_temp)
            
            elif self.current_stat == 'Intelligence':
                if self.stocks_fetcher.stocks_data != None:
                    self.intelligence_value = SpecialCalculator.calculate_intelligence(self.stocks_fetcher.stocks_data)
                else:
                    self.stocks_fetcher.fetch_stocks_data_async()
            
            elif self.current_stat == 'Agility':
                self.speed_fetcher.fetch_download_upload_speed_async()
                self.speed_fetcher.fetch_disk_speed_async()

                if self.speed_fetcher.upload_speed != None and self.speed_fetcher.download_speed != None:
                    self.agility_value = SpecialCalculator.calculate_agility(self.speed_fetcher.read_speed, self.speed_fetcher.write_speed, 
                                                                             self.speed_fetcher.disk_queue_length, self.speed_fetcher.upload_speed,
                                                                             self.speed_fetcher.download_speed)
            
            # elif self.current_stat == 'Charisma':
            #     self.devices, self.device_count, self.gateway_status = self.charisma_monitor.get_charisma_factors()
            #     self.charisma_value = SpecialCalculator.calculate_charisma(self.devices, self.device_count, self.gateway_status)

            time.sleep(0.1)
    

    # Charisma calculation is slow due to network pinging, so it is in another thread that runs every few minutes outside the charisma view
    # to ensure the data will be there to display and not block the rest of the app
    def start_charisma_monitor(self):
        def charisma_background_task():
            while self.running:
                self.devices, self.device_count, self.gateway_status = self.charisma_monitor.get_charisma_factors()
                self.charisma_value = SpecialCalculator.calculate_charisma(self.devices, self.device_count, self.gateway_status)
                time.sleep(self.CHARISMA_REFRESH_INTERVAL) #Run this code every few minutes

        self.charisma_thread = threading.Thread(target=charisma_background_task, daemon=True)
        self.charisma_thread.start()
    

    def update_frontend_with_charisma_data(self, devices, device_count, gateway_status):
        self.devices = devices
        self.device_count  = device_count
        self.gateway_status = gateway_status
        self.charisma_value = SpecialCalculator.calculate_charisma(self.devices, self.device_count, self.gateway_status)
        

    def get_sprite_sheet_frames(self, sprite_sheet, num_frames, frame_width, frame_height):
        frames = []

        scale_factor = min(self.stats_area.width / (num_frames * frame_width), self.stats_area.height / frame_height)
        
        scaled_frame_width = int(frame_width * scale_factor) 
        scaled_frame_height = int(frame_height * scale_factor)

        for i in range(num_frames):
            frame_rect = pygame.Rect(i * frame_width, 0, frame_width, frame_height)
            frame = sprite_sheet.subsurface(frame_rect).copy()
            # frame = pygame.transform.scale(frame, (scaled_frame_width, scaled_frame_height))
            frames.append(frame)

        return frames


    def animate_sprite(self, sprite_sheet, screen, x, y, num_frames, frame_width, frame_height):
        frames = self.get_sprite_sheet_frames(sprite_sheet, num_frames, frame_width, frame_height)
        frame_delay = 150
        now = pygame.time.get_ticks()
        if now - self.last_update > frame_delay:
            self.current_frame = (self.current_frame + 1) % num_frames
            self.last_update = now

        screen.blit(frames[self.current_frame], (x, y))
    

    def display_strength(self):
        diff = self.strength_value - 5
        strength_text = self.font.render(f'Strength Value: {str(self.strength_value)}({"+" if diff >= 0 else ""}{diff})', True, self.main_font_color)
        center_x = self.area.left + (self.area.width - strength_text.get_width()) // 2
        center_y = self.area.top + (self.area.height - strength_text.get_width()) // 2
        y_offset = self.stats_area.top + 10
        self.screen.blit(strength_text, (center_x, y_offset))

        col1_x = self.stats_area.left + 50
        col2_x = self.stats_area.left + (self.stats_area.width * 3 // 4)

        cpu_text = self.font.render(f"CPU Usage: {self.cpu_usage:.1f}%", True, (95, 255, 177))
        self.screen.blit(cpu_text, (col1_x, y_offset + 25))
        
        if self.freq:
            freq_text = self.font.render(f"Frequency: {self.freq.current:.1f} MHz", True, (95, 255, 177))
            self.screen.blit(freq_text, (col1_x, y_offset + 50))
        
        memory_text = self.font.render(f"Memory: {self.used_memory} MB/{self.total_memory} MB, {self.memory_percent}%", True, (95, 255, 177)) 
        self.screen.blit(memory_text, (col1_x, y_offset + 75))
        
        cores_text = self.font.render(f"Logical Cores: {self.cores}", True, (95, 255, 177))
        self.screen.blit(cores_text, (col1_x, y_offset + 100))

        for i, core_usage in enumerate(self.core_usages):
            core_text = self.font.render(f"Core {i + 1}: {core_usage:.1f}%", True, (95, 255, 177))
            self.screen.blit(core_text, (col2_x, y_offset + 25 + i * 30))

        frame_width = self.strength_sprite.get_width() // 14
        sprite_x = (self.stats_area.left + self.stats_area.width // 2) - frame_width // 2
        sprite_y = y_offset + 50
        self.animate_sprite(self.strength_sprite, self.screen, sprite_x, sprite_y, 14, frame_width, self.strength_sprite.get_height())

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
            percep_text = self.font.render(f'Perception Value: {str(self.perception_value)}({"+" if diff >= 0 else ""}{diff})', True, self.main_font_color)
            col1_x = self.stats_area.left + 50
            y_offset = self.stats_area.top + 10
            center_x = self.area.left + (self.area.width - percep_text.get_width()) // 2
            center_y = self.area.top + (self.area.height - percep_text.get_width()) // 2

            self.screen.blit(percep_text, (center_x, y_offset))

            temp_f = self.weather_fetcher.weather_data["current"]["temp_f"]
            cloud_cover = self.weather_fetcher.weather_data["current"]["cloud"]
            wind_mph = self.weather_fetcher.weather_data['current']['wind_mph']
            localtime_epoch = datetime.fromtimestamp(self.weather_fetcher.weather_data['location']['localtime_epoch'])

            temp_text = self.font.render(f"Temp: {temp_f}°F", True, self.main_font_color)
            cloud_cover_text = self.font.render(f'Cloud Cover: {cloud_cover}', True, self.main_font_color)
            wind_mph_text = self.font.render(f'Wind: {str(wind_mph)} mph', True, self.main_font_color)
            localtime_text = self.font.render(f'{str(localtime_epoch)}', True, self.main_font_color)

            self.screen.blit(temp_text, (col1_x, y_offset + 25))
            self.screen.blit(cloud_cover_text, (col1_x, y_offset + 50))  
            self.screen.blit(wind_mph_text, (col1_x, y_offset + 75))  
            self.screen.blit(localtime_text, (col1_x, y_offset + 100))  

            frame_width = self.perception_sprite.get_width() // 14
            sprite_x = (self.stats_area.left + self.stats_area.width // 2) - frame_width // 2
            sprite_y = y_offset + 50
            self.animate_sprite(self.perception_sprite, self.screen, sprite_x, sprite_y, 14, frame_width, self.perception_sprite.get_height())

            pygame.display.flip()


    def display_endurance(self):
        col1_x = self.stats_area.left + 50
        col2_x = self.stats_area.left + (self.stats_area.width * 3 // 4)
        y_offset = self.stats_area.top + 10

        uptime_text = self.font.render(f"Uptime: {int(self.uptime_hours)} hours", True, self.main_font_color)
        self.screen.blit(uptime_text, (col1_x, y_offset + 30))

        temp_text = self.font.render(f"CPU Temp: {self.cpu_temp:.1f}°C", True, self.main_font_color)
        self.screen.blit(temp_text, (col1_x, y_offset + 60))

        diff = self.endurance_value - 5
        endurance_text = self.font.render(f"Endurance Value: {str(int(self.endurance_value))}({'+' if diff >= 0 else ''}{int(diff)})", True, self.main_font_color)
        center_x = self.area.left + (self.area.width - endurance_text.get_width()) // 2
        center_y = self.area.top + (self.area.height - endurance_text.get_width()) // 2
        self.screen.blit(endurance_text, (center_x, y_offset))

        frame_width = self.endurance_sprite.get_width() // 14
        sprite_x = (self.stats_area.left + self.stats_area.width // 2) - frame_width // 2
        sprite_y = y_offset + 50
        self.animate_sprite(self.endurance_sprite, self.screen, sprite_x, sprite_y, 14, frame_width, self.endurance_sprite.get_height())

        pygame.display.flip()


    def display_charisma(self):
        col1_x = self.stats_area.left + 50
        col2_x = self.stats_area.left + (self.stats_area.width * 3 // 4)
        y_offset = self.stats_area.top + 10

        device_count_text = self.font.render(f"# of Devices: {int(self.device_count)}", True, self.main_font_color)
        self.screen.blit(device_count_text, (col1_x, y_offset + 25))
        gateway_status_text = self.font.render(f"Gateway Status: {self.gateway_status}", True, self.main_font_color)
        self.screen.blit(gateway_status_text, (col1_x, y_offset + 50))

        devices_text = self.font.render(f"Devices: ", True, self.main_font_color)
        self.screen.blit(devices_text, (col1_x, y_offset + 75))
        
        ip_y_offset = y_offset + 100
        for ip, value in self.devices.items():
            text = self.font.render(f'{ip} - {value}', True, self.main_font_color)
            self.screen.blit(text, (col1_x+15, ip_y_offset))
            ip_y_offset += 30
        
        diff = self.charisma_value - 5
        charisma_text = self.font.render(f"Charisma Value: {str(self.charisma_value)}({'+' if diff >= 0 else ''}{diff})", True, self.main_font_color)
        center_x = self.area.left + (self.area.width - charisma_text.get_width()) // 2
        center_y = self.area.top + (self.area.height - charisma_text.get_width()) // 2
        self.screen.blit(charisma_text, (center_x, y_offset))

        
        frame_width = self.charisma_sprite.get_width() // 14
        sprite_x = (self.stats_area.left + self.stats_area.width // 2) - frame_width // 2
        sprite_y = y_offset + 50

        self.animate_sprite(self.charisma_sprite, self.screen, sprite_x, sprite_y, 14, frame_width, self.charisma_sprite.get_height())
        
        pygame.display.flip()


    def display_intelligence(self):
        if self.stocks_fetcher.stocks_data == None:
            loading_text = self.font.render("Loading...", True, self.main_font_color)
            text_width = loading_text.get_width()
            text_height = loading_text.get_height()

            center_x = self.area.left + (self.area.width - text_width) // 2
            center_y = self.area.top + (self.area.height - text_height) // 2

            self.screen.blit(loading_text, (center_x, center_y))
        else:
            diff = self.intelligence_value - 5
            intel_text = self.font.render(f'Intelligence Value: {str(self.intelligence_value)}({"+" if diff >= 0 else ""}{diff})', True, self.main_font_color)
            col1_x = self.stats_area.left + 50
            col2_x = self.stats_area.left + (self.stats_area.width * 3 // 4)
            y_offset = self.stats_area.top + 10
            center_x = self.area.left + (self.area.width - intel_text.get_width()) // 2
            center_y = self.area.top + (self.area.height - intel_text.get_width()) // 2

            self.screen.blit(intel_text, (center_x, y_offset))

            devices_text = self.font.render(f"Stock Prices: ", True, self.main_font_color)
            self.screen.blit(devices_text, (col1_x, y_offset + 50))
            
            price_y_offset = y_offset + 100
            for company in self.stocks_fetcher.stocks_data.keys():
                diff = float(self.stocks_fetcher.stocks_data[company]['closing_price']) - float(self.stocks_fetcher.stocks_data[company]['opening_price'])
                text = self.font.render(f"{company}: ${self.stocks_fetcher.stocks_data[company]['closing_price']}", True, self.main_font_color)
                percent_text = self.font.render(f"{self.stocks_fetcher.stocks_data[company]['percent_change']}%", True, self.main_font_color)
                self.screen.blit(text, (col1_x+15, price_y_offset))
                self.screen.blit(percent_text, (col2_x+15, price_y_offset))
                price_y_offset += 30
            
            frame_width = self.intelligence_sprite.get_width() // 14
            sprite_x = (self.stats_area.left + self.stats_area.width // 2) - frame_width // 2
            sprite_y = y_offset + 50

            self.animate_sprite(self.intelligence_sprite, self.screen, sprite_x, sprite_y, 14, frame_width, self.intelligence_sprite.get_height())
            
            pygame.display.flip()


    def display_agility(self):
        diff = self.agility_value - 5
        intel_text = self.font.render(f'Agility Value: {str(self.agility_value)}({"+" if diff >= 0 else ""}{diff})', True, self.main_font_color)
        col1_x = self.stats_area.left + 50
        y_offset = self.stats_area.top + 10
        center_x = self.area.left + (self.area.width - intel_text.get_width()) // 2
        center_y = self.area.top + (self.area.height - intel_text.get_width()) // 2

        self.screen.blit(intel_text, (center_x, y_offset))

        if self.speed_fetcher.disk_queue_length != None:
            read_speed_text = self.font.render(f"Read Speed: {self.speed_fetcher.read_speed} MB/s", True, self.main_font_color)
            self.screen.blit(read_speed_text, (col1_x, y_offset + 50))

            write_speed_text = self.font.render(f"Write Speed: {self.speed_fetcher.write_speed} MB/s", True, self.main_font_color)
            self.screen.blit(write_speed_text, (col1_x, y_offset + 75))

            disk_length_text = self.font.render(f"Disk Queue Length: {self.speed_fetcher.disk_queue_length}", True, self.main_font_color)
            self.screen.blit(disk_length_text, (col1_x, y_offset + 100))

        if self.speed_fetcher.upload_speed == None:
            loading_text = self.font.render("Loading Upload/Download Speed...", True, self.main_font_color)
            text_width = loading_text.get_width()
            text_height = loading_text.get_height()

            center_x = self.area.left + (self.area.width - text_width) // 2
            center_y = self.area.top + (self.area.height - text_height)

            self.screen.blit(loading_text, (center_x, center_y))
        else:
            upload_speed_text = self.font.render(f"Upload Speed: {round(self.speed_fetcher.upload_speed, 2)} Mbps", True, self.main_font_color)
            self.screen.blit(upload_speed_text, (col1_x, y_offset + 125))

            download_speed_text = self.font.render(f"Download Speed: {round(self.speed_fetcher.download_speed, 2)} Mbps", True, self.main_font_color)
            self.screen.blit(download_speed_text, (col1_x, y_offset + 150))
            
        frame_width = self.agility_sprite.get_width() // 14
        sprite_x = (self.stats_area.left + self.stats_area.width // 2) - frame_width // 2
        sprite_y = y_offset + 50

        self.animate_sprite(self.agility_sprite, self.screen, sprite_x, sprite_y, 14, frame_width, self.agility_sprite.get_height())
        
        pygame.display.flip()




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


