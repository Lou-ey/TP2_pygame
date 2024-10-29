import pygame
import os

class MainMenu:
    def __init__(self):
        pygame.init()
        self.width = 1000
        self.height = 800
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()
        self.options = ["Play", "Options", "Quit"]
        self.selected_option = 0
        self.running = True

        self.background_image = pygame.image.load(os.path.join('assets/images/menu/Banner_Vertical.png'))
        self.button_image = pygame.image.load(os.path.join('assets/images/menu/Button_Red_3Slides.png'))
        self.font = pygame.font.Font(pygame.font.get_default_font(), 36)

    def draw_text(self, text, color, x, y):
        text_surface = self.font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.screen.blit(text_surface, text_rect)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    self.selected_option = (self.selected_option + 1) % len(self.options)
                elif event.key == pygame.K_UP:
                    self.selected_option = (self.selected_option - 1) % len(self.options)
                elif event.key == pygame.K_RETURN:
                    return self.options[self.selected_option]

    def run(self):
        while self.running:
            self.screen.blit(self.background_image, (0, 0))

            # Desenhar opções de menu
            for i, option in enumerate(self.options):
                color = (255, 0, 0) if i == self.selected_option else (255, 255, 255)
                self.draw_text(option, color, self.width / 2, self.height / 2 + i * 50)

            pygame.display.flip()
            selected_action = self.handle_events()
            if selected_action:
                print(f"Selected Option: {selected_action}")
                return selected_action

            self.clock.tick(60)


menu = MainMenu()
choice = menu.run()
print(f"User chose: {choice}")
pygame.quit()


