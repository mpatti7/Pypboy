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
        self.background_image = pygame.image.load("assets/images/radio.png")
        self.background_image = pygame.transform.scale(self.background_image, (self.area.width * .25, self.area.height * .35))
        self.radio_thread = None
        self.stop_event = threading.Event()

        self.radio_stations = [
            {'name': 'Kiss 108', 'url': 'http://stream.revma.ihrhls.com/zc1097'},
            {'name': 'Magic 106.7', 'url': 'https://live.amperwave.net/direct/audacy-wmjxfmaac-imc'}
        ]
        self.current_station = None

        self.buttons = [
            Button(self.area.x + 50, 50, 75, 25, "Kiss 108", self.font, (95, 255, 177), (95, 255, 177), transparent=True, action=self.create_action('Kiss 108')),
            Button(self.area.x + 50, 100, 75, 25, "Magic 106.7", self.font, (95, 255, 177), (95, 255, 177), transparent=True, action=self.create_action('Magic 106.7'))
        ]

        self.waves = AudioWaves(screen, area)
    

    def draw_background(self):
        self.background_image.set_alpha(128)
        self.screen.blit(self.background_image, (self.area.right - (self.area.right * .35), self.area.top + (self.area.top * .35)))
        self.draw_buttons()

        # if self.current_station != None:
        #     self.play_stream(self.current_station)
    

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

            if button_name == "Kiss 108":
                self.set_current_station(self.radio_stations[0])
            if button_name == "Magic 106.7":
                self.set_current_station(self.radio_stations[1])

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