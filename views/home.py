import pygame
from config import BLACK, GREEN, MAIN_GREEN, SCREEN_HEIGHT, SCREEN_WIDTH


class HomeView():
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font('assets/fonts/monofonto_rg.otf', 36)

        self.background_image = pygame.image.load("assets/images/pipboy.png")
        self.background_image = pygame.transform.scale(self.background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

        self.overlay_image = pygame.image.load("assets/images/overlay.png")
        self.overlay_image = pygame.transform.scale(self.overlay_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

        self.border_image = pygame.image.load("assets/images/border.png")
        self.border_image = pygame.transform.scale(self.border_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

        self.header = Header(screen)
        self.footer = Footer(screen)

        self.buttons = {}


    def draw_background(self):
        # Draw the background
        self.screen.blit(self.border_image, (0, 0))
        self.screen.blit(self.background_image, (0, 0))
        self.overlay_image.set_alpha(128)
        self.screen.blit(self.overlay_image, (0, 0))

        self.buttons['header_btns'] = self.header.draw_header()
        self.buttons['footer_btns'] = self.footer.draw_footer()



class Header():
    def __init__(self, screen):
        self.screen = screen
        self.header_surface = pygame.Surface((SCREEN_WIDTH, 20), pygame.SRCALPHA)
        self.font = pygame.font.Font('assets/fonts/monofonto_rg.otf', 20)
        self.buttons = {}


    def draw_header(self):
        self.header_surface.fill((0, 0, 0, 0))  # Transparent background
        color = (95, 255, 177, 128)

        pygame.draw.line(self.header_surface, color, (5, 5), (5, 25), 2)

        self.draw_button('Stats', color, 7, 7, 100, 50, 10, 7)

        pygame.draw.line(self.header_surface, color, (5, 5), (SCREEN_WIDTH - 154, 5), 2)
        pygame.draw.line(self.header_surface, color, (SCREEN_WIDTH - 154, 5), (SCREEN_WIDTH - 154, 25), 2)
        pygame.draw.line(self.header_surface, color, (SCREEN_WIDTH - 148, 5), (SCREEN_WIDTH - 13, 5), 2)
        pygame.draw.line(self.header_surface, color, (SCREEN_WIDTH - 13, 5), (SCREEN_WIDTH - 13, 25), 2)

        self.screen.blit(self.header_surface, (0, 0))

        return self.buttons
    

    def draw_button(self, btn_text, btn_color, left, right, width, height, font_x, font_y=7):
        pygame.draw.rect(self.header_surface, btn_color, (left, right, width, height))
        button_text = self.font.render(btn_text, True, btn_color)
        self.screen.blit(button_text, (font_x, font_y))
        self.buttons[btn_text] = pygame.Rect(left, right, width, height)



class Footer():
    def __init__(self, screen):
        self.screen = screen
        self.footer_surface = pygame.Surface((SCREEN_WIDTH, 20), pygame.SRCALPHA)
        self.font = pygame.font.Font('assets/fonts/monofonto_rg.otf', 36) 


    def draw_footer(self):
        self.footer_surface.fill((0, 0, 0, 0))  # Transparent background

        footer_top = SCREEN_HEIGHT - 20
        footer_bottom = SCREEN_HEIGHT - 2
        color = (95, 255, 177, 128)

        # Draw lines onto the footer surface
        pygame.draw.line(self.footer_surface, color, (5, 0), (5, 18), 2)
        pygame.draw.line(self.footer_surface, color, (5, 18), (SCREEN_WIDTH - 13, 18), 2)
        pygame.draw.line(self.footer_surface, color, (SCREEN_WIDTH - 13, 0), (SCREEN_WIDTH - 13, 18), 2)

        # Blit the footer surface onto the main screen
        self.screen.blit(self.footer_surface, (0, footer_top))







        # # Example text
        # text_surface = self.font.render("Welcome to the Pipboy", True, GREEN)
        # self.screen.blit(text_surface, (50, 50))

        # # Example button
        # pygame.draw.rect(self.screen, GREEN, (50, 150, 200, 50))
        # button_text = self.font.render("Stats", True, BLACK)
        # self.screen.blit(button_text, (100, 160))