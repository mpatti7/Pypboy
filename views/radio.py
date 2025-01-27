import pygame
from config import BLACK, GREEN, MAIN_GREEN, SCREEN_HEIGHT, SCREEN_WIDTH
from components.button import Button
import pygame.mixer
import subprocess
import threading
import random


class RadioView():
    def __init__(self, screen, area):
        self.screen = screen
        self.area = area
        self.font = pygame.font.Font('assets/fonts/monofonto_rg.otf', 20) 
        self.background_image = pygame.image.load("assets/images/vaultboy_music.png")
        self.background_image = pygame.transform.scale(self.background_image, (self.area.width * .50, self.area.height * .75))
        self.radio_thread = None
        self.stop_event = threading.Event()

        self.radio_stations = [
            {'name': 'Kiss 108', 'url': 'http://stream.revma.ihrhls.com/zc1097'},
            {'name': 'Magic 106.7', 'url': 'https://live.amperwave.net/direct/audacy-wmjxfmaac-imc'},
            {'name': 'Big 103.3', 'url': 'https://live.amperwave.net/direct/audacy-wbgbfmaac-imc'},
            {'name': 'WXLO 104.5', 'url': 'https://playerservices.streamtheworld.com/api/livestream-redirect/WXLOFMAAC.aac'},
            {'name': 'Mix 104.1', 'url': 'https://eus.rubiconproject.com/usync.html?p=7562&endpoint=us-west&auid=f8k:57e0ad9f43e2ae1b816bd54f752cbdd7'},
            {'name': '98.5 The Sports Hub', 'url': 'https://playerservices.streamtheworld.com/api/livestream-redirect/WBZFMDIALUPAAC.aac'}
        ]
        self.current_station = None

        self.buttons = [
            Button(self.area.x + 50, 50, 75, 25, "Kiss 108", self.font, (95, 255, 177), (95, 255, 177), transparent=True, action=self.create_action('Kiss 108')),
            Button(self.area.x + 50, 100, 75, 25, "Magic 106.7", self.font, (95, 255, 177), (95, 255, 177), transparent=True, action=self.create_action('Magic 106.7')),
            Button(self.area.x + 50, 150, 75, 25, "Big 103.3", self.font, (95, 255, 177), (95, 255, 177), transparent=True, action=self.create_action('Big 103.3')),
            Button(self.area.x + 50, 200, 75, 25, "WXLO 104.5", self.font, (95, 255, 177), (95, 255, 177), transparent=True, action=self.create_action('WXLO 104.5')),
            Button(self.area.x + 50, 250, 75, 25, "Mix 104.1", self.font, (95, 255, 177), (95, 255, 177), transparent=True, action=self.create_action('Mix 104.1')),
            Button(self.area.x + 75, 300, 75, 25, "98.5 The Sports Hub", self.font, (95, 255, 177), (95, 255, 177), transparent=True, 
                   action=self.create_action('98.5 The Sports Hub')),
            
        ]

        self.waves = AudioWaves(screen, area)
    

    def draw_background(self):
        self.background_image.set_alpha(128)
        center_x = self.area.left + (self.area.width - self.background_image.get_width()) // 2
        center_y = self.area.top + (self.area.height - self.background_image.get_height()) // 2

        self.screen.blit(self.background_image, (center_x, center_y))
        self.draw_buttons()
    

    def draw_buttons(self):
        for button in self.buttons:
            button.draw(self.screen)
    

    def handle_event(self, event):
        for button in self.buttons:
            button.handle_event(event)


    def set_current_station(self, station_name):
        if self.current_station == station_name:
            self.stop_stream()
            self.current_station = None
            return
        self.current_station = station_name
        self.play_stream(self.current_station)
    
    
    def play_stream(self, station):
        def stream_target():
            try:
                url = station['url']
                self.stop_event.clear()  # Ensure the stop event is reset
                process = subprocess.Popen(
                    ["ffplay", "-nodisp", "-autoexit", url],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
                print(f"Playing stream from: {url}")
                while process.poll() is None:  # Wait for the process to complete
                    self.waves.draw()
                    if self.stop_event.is_set():
                        process.terminate()
                        print("Stream stopped by user")
                        break
            except Exception as e:
                print(f"Error playing stream: {e}")

        # Check if a thread is already running and stop it
        if self.radio_thread and self.radio_thread.is_alive():
            self.stop_stream()
        
        self.radio_thread = threading.Thread(target=stream_target, daemon=True)
        self.radio_thread.start()
    

    def stop_stream(self):
        if self.radio_thread and self.radio_thread.is_alive():
            self.stop_event.set()
            self.radio_thread.join()  # Wait for the thread to finish
            print("Stream thread terminated")
        else:
            print("No active stream to stop")


    def create_action(self, button_name):
        def action():
            # Set this button active and all others inactive
            for button in self.buttons:
                button.is_active = (button.text == button_name)
            print(f"{button_name} button clicked!")

            for station in self.radio_stations:
                if button_name == station['name']:
                    self.set_current_station(station)
                    break
        return action



class AudioWaves:
    def __init__(self, screen, area):
        self.screen = screen
        self.area = area
        self.num_bars = 10  # Number of bars
        self.bar_width = 10  # Width of each bar

    def draw(self):
        for i in range(self.num_bars):
            # Randomize the height (simulate bouncing)
            bar_height = random.randint(10, self.area.height // 3.3)
            x = self.area.right - (self.num_bars - i) * (self.bar_width + 1)
            y = self.area.bottom - bar_height

            # Draw the bar
            pygame.draw.rect(self.screen, (95, 255, 177), (x-20, y+20, self.bar_width, bar_height))