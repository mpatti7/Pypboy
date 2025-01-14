import pygame
from config import BLACK, GREEN, SCREEN_HEIGHT, SCREEN_WIDTH


class HomeView():
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 36)  # Default font

        self.background_image = pygame.image.load("assets/images/pipboy.png")
        self.background_image = pygame.transform.scale(self.background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

        self.overlay_image = pygame.image.load("assets/images/overlay.png")
        self.overlay_image = pygame.transform.scale(self.overlay_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

        self.border_image = pygame.image.load("assets/images/border.png")
        self.border_image = pygame.transform.scale(self.border_image, (SCREEN_WIDTH, SCREEN_HEIGHT))


    def draw_background(self):
        # Draw the background
        self.screen.blit(self.border_image, (0, 0))
        self.screen.blit(self.background_image, (0, 0))
        self.overlay_image.set_alpha(128)
        self.screen.blit(self.overlay_image, (0, 0))

        # self.background_image.fill((0, 0, 0))
        pygame.draw.line(self.background_image, (95, 255, 177), (5, 5), (5, 25), 2)
        pygame.draw.line(self.background_image, (95, 255, 177), (5, 5), (SCREEN_WIDTH - 154, 5), 2)
        pygame.draw.line(self.background_image, (95, 255, 177), (SCREEN_WIDTH - 154, 5), (SCREEN_WIDTH - 154, 25), 2)
        pygame.draw.line(self.background_image, (95, 255, 177), (SCREEN_WIDTH - 148, 5), (SCREEN_WIDTH - 13, 5), 2)
        pygame.draw.line(self.background_image, (95, 255, 177), (SCREEN_WIDTH - 13, 5), (SCREEN_WIDTH - 13, 25), 2)

        # # Example text
        # text_surface = self.font.render("Welcome to the Pipboy", True, GREEN)
        # self.screen.blit(text_surface, (50, 50))

        # # Example button
        # pygame.draw.rect(self.screen, GREEN, (50, 150, 200, 50))
        # button_text = self.font.render("Stats", True, BLACK)
        # self.screen.blit(button_text, (100, 160))