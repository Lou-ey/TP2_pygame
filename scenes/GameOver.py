import pygame
import os
from utils.AudioPlayer import AudioPlayer

class GameOver:
    def __init__(self, screen):
        self.screen = screen
        self.font_title = pygame.font.Font(os.path.join('assets/fonts/Jacquard12-Regular.ttf'), 100)
        self.font_option = pygame.font.Font(os.path.join('assets/fonts/DungeonFont.ttf'), 30)
        self.overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        self.overlay.fill((0, 0, 0, 180))
        self.audio_player = AudioPlayer()

        self.title_text = self.font_title.render("Game Over", True, (255, 0, 0))
        self.restart_text = self.font_option.render("Restart (R)", True, (255, 255, 255))
        self.main_menu_text = self.font_option.render("Exit (E)", True, (255, 255, 255))

        # Posiciona os textos
        self.title_pos = self.title_text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 3))
        self.restart_pos = self.restart_text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))
        self.main_menu_pos = self.main_menu_text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 + 50))

        self.dead_knight = pygame.image.load('assets/images/player/knight/dead_knight.png').convert_alpha()
    def draw(self):
        # Desenha o overlay
        self.screen.blit(self.overlay, (0, 0))
        self.screen.blit(self.dead_knight, (self.screen.get_width() // 2 + self.screen.get_width() * 0.06, self.screen.get_height() // 2 - self.screen.get_height() * 0.15))


        # Textos


        # Renderiza os textos na tela
        self.screen.blit(self.title_text, self.title_pos)
        self.screen.blit(self.restart_text, self.restart_pos)
        self.screen.blit(self.main_menu_text, self.main_menu_pos)

        #self.audio_player.play_sound('game_over')  # Toca o som de game over
