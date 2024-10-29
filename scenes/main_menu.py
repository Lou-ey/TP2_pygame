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

        self.background_image = self.load_and_scale_image('../assets/images/menu/Banner_Vertical.png', (350, 450))
        self.banner_image = self.load_and_scale_image('../assets/images/menu/Ribbon_Red_3Slides.png', (250, 80))
        self.button_image = self.load_and_scale_image('../assets/images/menu/Button_Red_3Slides.png', (150, 50))

        self.font = pygame.font.Font(os.path.join('../assets/fonts/DungeonFont.ttf'), 25)

    def load_and_scale_image(self, path, size):
        image = pygame.image.load(path)
        return pygame.transform.scale(image, size)

    def draw_text(self, text, color, x, y):
        text_surface = self.font.render(text, True, color)
        text_rect = text_surface.get_rect(center=(x, y))
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

    def draw_menu(self):
        button_width, button_height = self.button_image.get_size()
        start_y = (self.height - (len(self.options) * button_height)) // 2


        for i, option in enumerate(self.options):
            button_x = (self.width - button_width) // 2
            button_y = start_y + i * button_height

            self.screen.blit(self.button_image, (button_x, button_y))
            text_x = button_x + button_width // 2
            text_y = button_y + button_height - 60 // 2
            color = (255, 255, 255) if i == self.selected_option else (0, 0, 0)

            self.draw_text(option, color, text_x, text_y)

    def run(self):
        while self.running:
            self.screen.fill((71, 171, 169))

            banner_width, banner_height = self.background_image.get_size()
            banner_x = (self.width - banner_width) // 2
            banner_y = (self.height - banner_height) // 2

            self.screen.blit(self.background_image, (banner_x, banner_y))
            self.screen.blit(self.banner_image, (375, 240))
            self.draw_menu()

            pygame.display.flip()
            selected_action = self.handle_events()
            if selected_action:
                if selected_action == "Quit":
                    self.running = False  # Encerra o jogo

        pygame.quit()


menu = MainMenu()
choice = menu.run()
print(f"Usuário escolheu: {choice}")


