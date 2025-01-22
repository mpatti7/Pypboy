import pygame
from config import BLACK, GREEN, MAIN_GREEN, SCREEN_HEIGHT, SCREEN_WIDTH
from components.button import Button
import pygame.mixer
import vlc


class RadioView():
    def __init__(self, screen, area):
        self.screen = screen
        self.area = area
        self.font = pygame.font.Font('assets/fonts/monofonto_rg.otf', 20) 
        self.background_image = pygame.image.load("assets/images/radio.png")
        # self.background_image = pygame.transform.scale(self.background_image, (self.area.width * .5, self.area.height * .25))

        self.radio_stations = [
            {'name': 'Kiss 108', 'url': 'http://stream.revma.ihrhls.com/zc1097'}
        ]
        self.current_station = None
        pygame.mixer.init()

        self.buttons = [
            Button(self.area.x + 50, 50, 75, 25, "Kiss 108", self.font, (95, 255, 177), (95, 255, 177), transparent=True, action=self.create_action('Kiss 108'))
        ]
    

    def draw_background(self):
        self.background_image.set_alpha(128)
        self.screen.blit(self.background_image, (self.area.x, 25))
        self.draw_buttons()

        if self.current_station != None:
            self.play_stream(self.current_station)
    

    def draw_buttons(self):
        for button in self.buttons:
            button.draw(self.screen)
    

    def handle_event(self, event):
        for button in self.buttons:
            button.handle_event(event)


    def set_current_station(self, station_name):
        self.current_station = station_name
    

    def play_stream(self, station):
        try:
            url = station['url']
            self.radio_player = vlc.MediaPlayer(url)
            self.radio_player.play()
        except Exception as e:
            print(f"Error playing stream: {e}")


    def create_action(self, button_name):
        def action():
            # Set this button active and all others inactive
            for button in self.buttons:
                button.is_active = (button.text == button_name)
            print(f"{button_name} button clicked!")

            if button_name == "Kiss 108":
                self.set_current_station(self.radio_stations[0])

        return action