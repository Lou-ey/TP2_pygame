import pygame
import os
from utils.AudioPlayer import AudioPlayer

class GameOver:
    def __init__(self, screen):
        self.screen = screen
        self.font_title = pygame.font.Font(os.path.join('assets/fonts/DungeonFont.ttf'), 50)
        self.font_option = pygame.font.Font(os.path.join('assets/fonts/DungeonFont.ttf'), 30)
        self.overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        self.overlay.fill((0, 0, 0, 180))
        self.audio_player = AudioPlayer()

    def draw(self):
        # Desenha o overlay
        self.screen.blit(self.overlay, (0, 0))

        # Textos
        title_text = self.font_title.render("Game Over", True, (255, 0, 0))
        restart_text = self.font_option.render("Restart (R)", True, (255, 255, 255))
        main_menu_text = self.font_option.render("Main Menu (M)", True, (255, 255, 255))

        # Posiciona os textos
        title_pos = title_text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 3))
        restart_pos = restart_text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))
        main_menu_pos = main_menu_text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 + 50))

        # Renderiza os textos na tela
        self.screen.blit(title_text, title_pos)
        self.screen.blit(restart_text, restart_pos)
        self.screen.blit(main_menu_text, main_menu_pos)

        #self.audio_player.play_sound('game_over')  # Toca o som de game over
