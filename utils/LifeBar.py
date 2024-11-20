import pygame

class LifeBar(pygame.sprite.Sprite):
    def __init__(self, max_health, current_health, width=100, height=10, color=(255, 0, 0), bg_color=(50, 50, 50)):
        super().__init__()
        self.max_health = max_health
        self.current_health = current_health
        self.width = width
        self.height = height
        self.color = color
        self.bg_color = bg_color

        # Cria a superfície da barra de vida
        self.image = pygame.Surface((self.width, self.height))
        self.rect = self.image.get_rect()

        self.update_bar()

    def update_bar(self):
        # Desenha o fundo (cor de fundo)
        self.image.fill(self.bg_color)

        # Calcula a largura proporcional da barra de saúde
        health_ratio = max(0, self.current_health / self.max_health)  # Garante que não seja menor que 0
        health_width = int(self.width * health_ratio)

        # Desenha a barra de vida
        health_rect = pygame.Rect(0, 0, health_width, self.height)
        pygame.draw.rect(self.image, self.color, health_rect)

    def update(self, current_health):
        self.current_health = current_health
        self.update_bar()