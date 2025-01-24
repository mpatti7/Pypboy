import pygame
from config import BLACK, GREEN, MAIN_GREEN, SCREEN_HEIGHT, SCREEN_WIDTH
from components.button import Button


class GameView():
    def __init__(self, screen, area):
        self.screen = screen
        self.area = area
        self.font = pygame.font.Font('assets/fonts/monofonto_rg.otf', 20)

        self.background_image = pygame.image.load("assets/images/pipboy_stats_no_background.png")
        self.background_image = pygame.transform.scale(self.background_image, (SCREEN_WIDTH * .75, SCREEN_HEIGHT * .75))

        self.buttons = []

            
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


    def create_action(self, button_name):
        def action():
            # Set this button active and all others inactive
            for button in self.buttons:
                button.is_active = (button.text == button_name)
            print(f"{button_name} button clicked!")

        return action
