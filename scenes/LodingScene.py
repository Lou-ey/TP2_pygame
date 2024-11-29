import pygame
import time  # Para esperar durante o carregamento

class LoadingScene:
    def __init__(self):
        self.font = pygame.font.Font(None, 36)
        self.text = self.font.render("Loading...", True, (255, 255, 255))

    def run(self, game_scene):
        """Simula o carregamento e depois passa para o GameScene"""
        start_ticks = pygame.time.get_ticks()  # Marca o tempo de início

        # Simula o tempo de carregamento
        while True:
            seconds = (pygame.time.get_ticks() - start_ticks) / 1000  # Tempo decorrido em segundos

            # Se passou o tempo de carregamento, inicia a GameScene
            if seconds > 2:  # Carrega por 2 segundos, você pode mudar o tempo conforme necessário
                return game_scene  # Retorna a instância do GameScene

            # Desenha a tela de carregamento
            self.draw()

            pygame.display.update()

    def draw(self):
        """Desenha a tela de carregamento"""
        screen = pygame.display.get_surface()
        screen.fill((0, 0, 0))
        screen.blit(self.text, (screen.get_width() // 2 - self.text.get_width() // 2, screen.get_height() // 2 - self.text.get_height() // 2))