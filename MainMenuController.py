from pygame import NOFRAME
from scenes.MainMenu import MainMenu
import pygame
from scenes.GameScene import GameScene
from utils.AudioPlayer import AudioPlayer


class MainMenuController:
    def __init__(self):
        pygame.init()
        self.audio_gestor = AudioPlayer()
        self.menu = MainMenu()
        self.game = GameScene()
        self.running = True
        self.show_options = False
        self.to_play = False


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
                        self.menu.show_options = True

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.menu.fullscreen_off_rect.collidepoint(self.menu.mouse_position):
                        self.menu.fullscreened = not self.menu.fullscreened and self.show_options == True
                        if self.menu.fullscreened:
                            display_info = pygame.display.Info()
                            self.menu.width, self.menu.height = display_info.current_w, display_info.current_h
                            self.menu.screen = pygame.display.set_mode((display_info.current_w, display_info.current_h), pygame.FULLSCREEN)

                        else:
                            self.menu.screen = pygame.display.set_mode((self.menu.width, self.menu.height))

                    if self.menu.with_sound_rect.collidepoint(self.menu.mouse_position) and self.show_options == True:
                        self.menu.muted = not self.menu.muted
                        if self.menu.muted:
                            pygame.mixer.music.set_volume(0)

                        else:
                            pygame.mixer.music.set_volume(0.03)

                    if self.menu.back_button_rect.collidepoint(self.menu.mouse_position):
                        self.show_options = False

                    for i, rect in enumerate(self.menu.button_rects):
                        if rect.collidepoint(self.menu.mouse_position):
                            selected_option = self.menu.options[i]
                            if selected_option == "Play" and self.show_options == False:
                                self.to_play = True
                            elif selected_option == "Quit":
                                quit()
                            elif selected_option == "Options":
                                self.show_options = True

    def run(self):
        self.menu.mouse_position = pygame.mouse.get_pos()
        self.handle_events()
        self.menu.cursor.update()
        if self.show_options:
            self.menu.options_menu()
        elif self.to_play:
            self.game.run()
        else:
            self.menu.menuPrincipal()
