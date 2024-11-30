import pygame

class LoadingScene:
    def __init__(self):
        self.font = pygame.font.Font(None, 36)

    def run(self, game_scene):
        """Exibe a tela de carregamento enquanto carrega a cena do jogo."""
        screen = pygame.display.get_surface()
        clock = pygame.time.Clock()

        while not game_scene.loaded:  # Continua até o jogo estar completamente carregado
            screen.fill((0, 0, 0))

            # Desenha o texto de carregamento
            text = self.font.render("Loading...", True, (219, 87, 26))
            screen.blit(text, (screen.get_width() // 2 - text.get_width() // 2,
                               screen.get_height() // 2 - text.get_height() // 2 - 20))

            # Desenha uma barra de progresso
            progress_width = int((game_scene.load_progress / game_scene.total_steps) * 300)
            progress_bar_rect = pygame.Rect((screen.get_width() // 2 - 150,
                                             screen.get_height() // 2 + 20),
                                            (progress_width, 20))
            pygame.draw.rect(screen, (219, 87, 26), progress_bar_rect)
            pygame.draw.rect(screen, (255, 255, 255), progress_bar_rect, 2)

            pygame.display.update()
            clock.tick(60)

            # Executa uma etapa do carregamento
            game_scene.load_step()