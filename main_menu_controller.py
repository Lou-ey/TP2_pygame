from scenes.main_menu import MainMenu
import pygame

class MainMenuController:
    def __init__(self):
        pygame.init()
        self.menu = MainMenu()
        self.running = True
        self.show_options = False
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    self.menu.selected_option = (self.menu.selected_option + 1) % len(self.menu.options)
                elif event.key == pygame.K_UP:
                    self.menu.selected_option = (self.menu.selected_option - 1) % len(self.menu.options)
                elif event.key == pygame.K_RETURN:
                    selected_option = self.menu.options[self.menu.selected_option]
                    if selected_option == "Quit":
                        self.running = False
                    elif selected_option == "Options":
                        self.menu.show_options = True  # Alterna para o menu de opções

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.menu.checkbox_rect.collidepoint(self.menu.mouse_position):
                        self.menu.checkbox_checked = not self.menu.checkbox_checked
                        if self.menu.checkbox_checked:
                            self.menu.screen = pygame.display.set_mode((self.menu.width, self.menu.height),pygame.FULLSCREEN)
                        else:
                            self.menu.screen = pygame.display.set_mode((self.menu.width, self.menu.height))
                    for i, rect in enumerate(self.menu.button_rects):
                        if rect.collidepoint(self.menu.mouse_position):
                            selected_option = self.menu.options[i]
                            if selected_option == "Quit":
                                self.running = False
                            elif selected_option == "Options":
                                self.show_options = True


    def run(self):
        while self.running:
            self.menu.mouse_position = pygame.mouse.get_pos()
            self.handle_events()
            self.menu.cursor.update()
            if self.show_options:
                self.menu.options_menu()
            else:
                self.menu.menuPrincipal()
            self.menu.clock.tick(60)

if __name__ == "__main__":
    menu_controller = MainMenuController()
    menu_controller.run()