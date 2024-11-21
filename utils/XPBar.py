import pygame

class XPBar(pygame.sprite.Sprite):
    def __init__(self, max_xp, current_xp, width, height=10, color=(0, 255, 0), bg_color=(50, 50, 50)):
        super().__init__()
        self.max_xp = max_xp
        self.current_xp = current_xp
        self.width = width
        self.height = height
        self.color = color
        self.bg_color = bg_color

        # Cria a superfície da barra de xp
        self.image = pygame.Surface((self.width, self.height))
        self.rect = self.image.get_rect()

        self.update_bar()

    def update_bar(self):
        # Desenha o fundo (cor de fundo)
        self.image.fill(self.bg_color)

        # Calcula a largura proporcional da barra de saúde
        xp_ratio = max(0, self.current_xp / self.max_xp)  # Garante que não seja menor que 0
        xp_width = int(self.width * xp_ratio)

        # Desenha a barra de xp
        xp_rect = pygame.Rect(0, 0, xp_width, self.height)
        pygame.draw.rect(self.image, self.color, xp_rect)

    def update(self, current_xp):
        self.current_xp = current_xp
        self.update_bar()