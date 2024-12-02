from scenes.MainMenu import MainMenu
import pygame
from scenes.GameScene import GameScene
from utils.AudioPlayer import AudioPlayer
from utils.State import State
from scenes.LodingScene import LoadingScene

class MainMenuController:
    def __init__(self):
        pygame.init()
        self.audio_gestor = AudioPlayer()
        self.menu = MainMenu()
        self.State = State
        self.running = True
        self.show_options = False
        self.current_state = self.State.MENU
        self.to_play = False
        self.game = None
        self.loading = LoadingScene()

    def handle_events_menu(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.menu.fullscreen_off_rect.collidepoint(self.menu.mouse_position):
                        self.menu.fullscreened = not self.menu.fullscreened and self.show_options == True
                        if self.menu.fullscreened:
                            display_info = pygame.display.Info()
                            self.menu.width, self.menu.height = display_info.current_w, display_info.current_h
                            print(display_info.current_w, display_info.current_h)
                            self.menu.screen = pygame.display.set_mode((self.menu.width, self.menu.height), pygame.FULLSCREEN)
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
                                self.current_state = State.GAME
                                self.game = GameScene()
                            elif selected_option == "Quit" and self.show_options == False:
                                pygame.quit()
                                quit()
                            elif selected_option == "Options" and self.show_options == False:
                                self.show_options = True

    def run(self):
        self.menu.mouse_position = pygame.mouse.get_pos()
        if self.current_state == self.State.MENU:
            self.menu.cursor.update()
            self.handle_events_menu()
            if self.show_options:

                self.menu.options_menu()
            else:
                self.menu.menuPrincipal()

        elif self.current_state == State.GAME:
            if not self.to_play:
                self.game = GameScene()  # Cria a instância do jogo
                #self.loading.run(self.game)
                self.to_play = True

            self.game.run()
