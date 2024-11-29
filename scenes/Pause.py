import pygame
import os

class Pause:
    def __init__(self, screen):
        self.screen = screen
        self.font_title = pygame.font.Font(os.path.join('assets/fonts/DungeonFont.ttf'), 50)
        self.font_option = pygame.font.Font(os.path.join('assets/fonts/DungeonFont.ttf'), 30)
        self.overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        self.overlay.fill((0, 0, 0, 180))  # Preenchimento com transparência

    def draw(self):
        # Desenha o overlay
        self.screen.blit(self.overlay, (0, 0))

        # Textos
        title_text = self.font_title.render("Paused", True, (255, 255, 255))
        resume_text = self.font_option.render("Resume (ESC)", True, (255, 255, 255))
        main_menu_text = self.font_option.render("Main Menu", True, (255, 255, 255))

        # Posiciona os textos
        title_pos = title_text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 3))
        resume_pos = resume_text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))
        main_menu_pos = main_menu_text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 + 50))

        # Renderiza os textos na tela
        self.screen.blit(title_text, title_pos)
        self.screen.blit(resume_text, resume_pos)
        self.screen.blit(main_menu_text, main_menu_pos)