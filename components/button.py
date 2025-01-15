import pygame

class Button:
    def __init__(self, text, x, y, width, height, color, font_color):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.font_color = font_color

    def draw(self, surface, font):
        pygame.draw.rect(surface, self.color, self.rect)
        text_surface = font.render(self.text, True, self.font_color)
        surface.blit(text_surface, (self.rect.x + 10, self.rect.y + 10))

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)