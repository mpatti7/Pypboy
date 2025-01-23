import pygame
from config import BLACK, GREEN, MAIN_GREEN, SCREEN_HEIGHT, SCREEN_WIDTH
from components.button import Button


class StatsView():
    def __init__(self, screen, area):
        self.screen = screen
        self.area = area
        self.font = pygame.font.Font('assets/fonts/monofonto_rg.otf', 20)

        self.background_image = pygame.image.load("assets/images/pipboy_stats_no_background.png")
        self.background_image = pygame.transform.scale(self.background_image, (SCREEN_WIDTH * .75, SCREEN_HEIGHT * .75))

        self.buttons = [
            Button(self.area.x + 50, 75, 75, 25, "Strength", self.font, (95, 255, 177), (95, 255, 177), transparent=True, action=self.create_action('Strength')),
            Button(self.area.x + 50, 125, 75, 25, "Perception", self.font, (95, 255, 177), (95, 255, 177), transparent=True, action=self.create_action('Perception')),
            Button(self.area.x + 50, 175, 75, 25, "Endurance", self.font, (95, 255, 177), (95, 255, 177), transparent=True, action=self.create_action('Endurance')),
            Button(self.area.x + 50, 225, 75, 25, "Charisma", self.font, (95, 255, 177), (95, 255, 177), transparent=True, action=self.create_action('Charisma')),
            Button(self.area.x + 50, 275, 75, 25, "Intelligence", self.font, (95, 255, 177), (95, 255, 177), transparent=True, action=self.create_action('Intelligence')),
            Button(self.area.x + 50, 325, 75, 25, "Agility", self.font, (95, 255, 177), (95, 255, 177), transparent=True, action=self.create_action('Agility')),
            Button(self.area.x + 50, 375, 75, 25, "Luck", self.font, (95, 255, 177), (95, 255, 177), transparent=True, action=self.create_action('Luck')),

        ]

            
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


