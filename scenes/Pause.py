import pygame
import os
from utils.Cursor import Cursor

class Pause:
    def __init__(self, screen, game_scene):
        self.screen = screen
        self.game_scene = game_scene
        self.font_title = pygame.font.Font(os.path.join('assets/fonts/DungeonFont.ttf'), 60)
        self.font_option = pygame.font.Font(os.path.join('assets/fonts/DungeonFont.ttf'), 40)
        self.overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        self.overlay.fill((0, 0, 0, 180))  # Preenchimento com transparência
        self.background_image = pygame.image.load('assets/images/menu/fundo_paused.png')
        self.background_image = pygame.transform.scale(self.background_image,(self.screen.get_width(), self.screen.get_height()))
        self.with_sound = self.load_and_scale_image('assets/images/UI/menuUI/with_Sound.png', (90, 90))
        self.with_sound_rect = self.with_sound.get_rect(center=(self.screen.get_width() - self.screen.get_width() * 0.9, self.screen.get_height() * 0.9))
        self.sound_muted = self.load_and_scale_image('assets/images/UI/menuUI/Sound_mute.png', (90, 90))

        self.cursor = Cursor('assets/images/UI/pointer/01.png', (15,23))
        self.is_muted = False

        self.mouse_position = (0, 0)

        self.title_text = self.font_title.render("Paused", True, (255, 255, 255))
        self.resume_text = self.font_option.render("Resume (ESC)", True, (255, 255, 255))
        self.main_menu_text = self.font_option.render("Main Menu", True, (255, 255, 255))

        #posicionar os textos na tela
        self.title_pos = self.title_text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() * 0.3))
        self.resume_pos = self.resume_text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))
        self.main_menu_pos = self.main_menu_text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 + 50))

    def load_and_scale_image(self, path, size):
        image = pygame.image.load(path)
        return pygame.transform.scale(image, size)

    def handle_events(self):
        self.mouse_position = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.with_sound_rect.collidepoint(self.mouse_position):
                        self.is_muted = not self.is_muted
                        if self.is_muted:
                            self.game_scene.audio_player.mute_music()  # Para a música
                        else:
                            self.game_scene.audio_player.unmute_music()

                    if self.resume_pos.collidepoint(self.mouse_position):
                        self.game_scene.is_paused = False
                    elif self.main_menu_pos.collidepoint(self.mouse_position):
                        self.game_scene.switch_to_main_menu()
                        print("Bora para o main menu")


    def draw(self):
        # Desenha a imagem de fundo
        self.screen.blit(self.background_image, (0, 0))

        # Desenha o overlay
        self.screen.blit(self.overlay, (0, 0))

        self.screen.blit(self.title_text, self.title_pos)
        self.screen.blit(self.resume_text, self.resume_pos)
        self.screen.blit(self.main_menu_text, self.main_menu_pos)

        if self.is_muted:
            self.screen.blit(self.sound_muted, self.with_sound_rect.topleft)
        else:
            self.screen.blit(self.with_sound, self.with_sound_rect.topleft)

        #pygame.draw.rect(self.screen, (255, 0, 0), self.with_sound_rect, 2)

        self.cursor.draw(self.screen)
        self.cursor.show()
        self.cursor.update()
        pygame.display.flip()
