import pygame


class Button:
    def __init__(self, x, y, width, height, text, font, color, text_color, transparent=False, outline=None, action=None, is_active=False):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.color = color
        self.text_color = text_color
        self.transparent = transparent
        self.outline = outline
        self.action = action
        self.is_active = is_active


    def draw(self, surface):
        if not self.transparent:
            pygame.draw.rect(surface, self.color, self.rect, border_radius=5)
        if self.outline != None:
            pygame.draw.rect(surface, self.outline, self.rect, width=2, border_radius=5)

        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

        if self.is_active:
            underline_start = (text_rect.left, text_rect.bottom + 2)
            underline_end = (text_rect.right, text_rect.bottom + 2)
            pygame.draw.line(surface, self.text_color, underline_start, underline_end, 2)
    

    def button_active(self, surface):
        pass


    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                if self.action:
                    self.action()