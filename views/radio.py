import pygame
from config import BLACK, GREEN, MAIN_GREEN, SCREEN_HEIGHT, SCREEN_WIDTH
from components.button import Button
import pygame.mixer
import subprocess
import threading
import random
import time
import math


class RadioView():
    radio_thread = None
    stop_event = threading.Event()
    current_station = None


    def __init__(self, screen, area):
        self.screen = screen
        self.area = area
        self.font = pygame.font.Font('assets/fonts/monofonto_rg.otf', 20) 
        self.background_image = pygame.image.load("assets/images/radio.png")
        self.background_image = pygame.transform.scale(self.background_image, (self.area.width * .50, self.area.height))

        self.radio_stations = [
            {'name': 'Kiss 108', 'url': 'http://stream.revma.ihrhls.com/zc1097'},
            {'name': 'Magic 106.7', 'url': 'https://live.amperwave.net/direct/audacy-wmjxfmaac-imc'},
            {'name': 'WROR 105.7', 'url': 'https://playerservices.streamtheworld.com/api/livestream-redirect/WRORFMAAC.aac'},
            {'name': 'Big 103.3', 'url': 'https://live.amperwave.net/direct/audacy-wbgbfmaac-imc'},
            {'name': 'WXLO 104.5', 'url': 'https://playerservices.streamtheworld.com/api/livestream-redirect/WXLOFMAAC.aac'},
            {'name': 'Mix 104.1', 'url': 'https://live.amperwave.net/direct/audacy-wwbxfmaac-imc'},
            {'name': '98.5 The Sports Hub', 'url': 'https://playerservices.streamtheworld.com/api/livestream-redirect/WBZFMDIALUPAAC.aac'},
            {'name': 'Traffic on the 3s', 'url': 'https://stream.revma.ihrhls.com/zc7729/hls.m3u8'},
        ]

        self.buttons = [
            Button(self.area.x + 50, 50, 75, 25, "Kiss 108", self.font, (95, 255, 177), (95, 255, 177), transparent=True, action=self.create_action('Kiss 108')),
            Button(self.area.x + 50, 100, 75, 25, "Magic 106.7", self.font, (95, 255, 177), (95, 255, 177), transparent=True, action=self.create_action('Magic 106.7')),
            Button(self.area.x + 50, 150, 75, 25, "WROR 105.7", self.font, (95, 255, 177), (95, 255, 177), transparent=True, action=self.create_action('WROR 105.7')),
            Button(self.area.x + 50, 200, 75, 25, "Big 103.3", self.font, (95, 255, 177), (95, 255, 177), transparent=True, action=self.create_action('Big 103.3')),
            Button(self.area.x + 50, 250, 75, 25, "WXLO 104.5", self.font, (95, 255, 177), (95, 255, 177), transparent=True, action=self.create_action('WXLO 104.5')),
            Button(self.area.x + 50, 300, 75, 25, "Mix 104.1", self.font, (95, 255, 177), (95, 255, 177), transparent=True, action=self.create_action('Mix 104.1')),
            Button(self.area.x + 75, 350, 100, 25, "98.5 The Sports Hub", self.font, (95, 255, 177), (95, 255, 177), transparent=True, 
                   action=self.create_action('98.5 The Sports Hub')),
            Button(self.area.x + 75, 400, 100, 25, "Traffic on the 3s", self.font, (95, 255, 177), (95, 255, 177), transparent=True, 
                   action=self.create_action('Traffic on the 3s')),
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
            if RadioView.current_station != None and button.text == RadioView.current_station['name']:
                button.is_active = True
            button.draw(self.screen)
    

    def handle_event(self, event):
        for button in self.buttons:
            button.handle_event(event)


    def set_current_station(self, station_name):
        if RadioView.current_station == station_name:
            self.stop_stream()
            RadioView.current_station = None
            self.mark_button_inactive(station_name['name'])
            return
        RadioView.current_station = station_name
        self.play_stream(RadioView.current_station)
    
    
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
                    if RadioView.stop_event.is_set():
                        process.terminate()
                        print("Stream stopped by user")
                        break
            except Exception as e:
                print(f"Error playing stream: {e}")

        # Check if a thread is already running and stop it
        if RadioView.radio_thread and RadioView.radio_thread.is_alive():
            self.stop_stream()
        
        RadioView.radio_thread = threading.Thread(target=stream_target, daemon=True)
        RadioView.radio_thread.start()
    

    def stop_stream(self):
        if RadioView.radio_thread and RadioView.radio_thread.is_alive():
            RadioView.stop_event.set()
            RadioView.radio_thread.join()  # Wait for the thread to finish
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


    def mark_button_inactive(self, button_name):
        for button in self.buttons:
            if button.text == button_name:
                button.is_active = False
                return



class AudioWaves:
    def __init__(self, screen, area):
        self.screen = screen
        self.area = area
        self.num_bars = 3 
        self.bar_width = 5  
        self.font = pygame.font.Font('assets/fonts/monofonto_rg.otf', 20) 
        self.main_font_color = (95, 255, 177, 128)
        self.time_offset = time.time()  # Used for smooth animation


    def draw(self):
        radio_text = self.font.render('Radio', True, self.main_font_color)  
        x = 365
        current_time = time.time() - self.time_offset
        text_height = radio_text.get_height()

        for i in range(self.num_bars):
            bar_height = int((math.sin(current_time * 6 + i) + 1) / 2 * text_height) - 10
            x += 6
            pygame.draw.rect(self.screen, (95, 255, 177), (x, 30 - bar_height, self.bar_width, bar_height))
