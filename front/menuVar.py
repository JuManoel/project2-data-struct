import pygame


class ResponsiveMenu:
    def __init__(self, screen, options):
        self.screen = screen
        self.options = options
        self.font = pygame.font.Font(None, 30)
        self.selected_option = None
        self.margin_top = 20
        self.calculate_layout()

    def calculate_layout(self):
        self.menu_width = self.screen.get_width()
        self.option_spacing = self.menu_width // (len(self.options) + 1)
        self.option_positions = [
            (self.option_spacing * (i + 1), self.margin_top)
            for i in range(len(self.options))
        ]

    def draw(self):
        for i, option in enumerate(self.options):
            color = (0, 0, 0) if i != self.selected_option else (255, 0, 0)
            text = self.font.render(option, True, color)
            text_rect = text.get_rect(center=self.option_positions[i])
            self.screen.blit(text, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for i, position in enumerate(self.option_positions):
                x, y = position
                text_rect = self.font.render(self.options[i], True, (0, 0, 0)).get_rect(center=position)
                if text_rect.collidepoint(event.pos):
                    print(f"Selected: {self.options[i]}")
                    self.selected_option = i
