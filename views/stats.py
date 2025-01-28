import pygame
from config import BLACK, GREEN, MAIN_GREEN, SCREEN_HEIGHT, SCREEN_WIDTH
from components.button import Button
import psutil


class StatsView():
    def __init__(self, screen, area):
        self.screen = screen
        self.area = area
        self.font = pygame.font.Font('assets/fonts/monofonto_rg.otf', 20)

        self.background_image = pygame.image.load("assets/images/pipboy_stats_no_background.png")
        self.background_image = pygame.transform.scale(self.background_image, (SCREEN_WIDTH * .75, SCREEN_HEIGHT * .75))

        self.current_view = 'main'
        self.special_view = SpecialView(self.screen, self.area)
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
    def __init__(self, screen, area):
        self.screen = screen
        self.area = area
        self.font = pygame.font.Font('assets/fonts/monofonto_rg.otf', 20)
        self.special_logo = pygame.image.load("assets/images/special_logo.png")
        self.special_logo = pygame.transform.scale(self.special_logo, (SCREEN_WIDTH , SCREEN_HEIGHT * .5))
        self.current_stat = None

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

            self.current_stat = button_name
            self.stats_dict[button_name]()

        return action
    

    def display_strength(self):
        print('Displaying Strength')

        # while self.current_stat == 'Strength':
        #     val = psutil.cpu_percent(interval=.5, percpu=False)
        #     print(val)


    def display_perception(self):
        print('Displaying perception')


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


