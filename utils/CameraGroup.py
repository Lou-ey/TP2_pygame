import pygame

class CameraGroup(pygame.sprite.Group):
    def __init__(self, screen_width, screen_height, map_width, map_height):
        super().__init__()
        self.display = pygame.display.get_surface()
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.map_width = map_width
        self.map_height = map_height
        self.offset = pygame.math.Vector2()

    def center_on(self, target):
        # Centraliza a camera no alvo
        self.offset.x = target.rect.centerx - self.screen_width // 2
        self.offset.y = target.rect.centery - self.screen_height // 2

        # Limita a câmera para os limites do mapa
        self.offset.x = max(0, min(self.offset.x, self.map_width - self.screen_width))
        self.offset.y = max(0, min(self.offset.y, self.map_height - self.screen_height))

        # Limita o character para os limites da camera
        target.rect.x = max(0, min(target.rect.x, self.map_width - target.rect.width + 20))
        target.rect.y = max(0, min(target.rect.y, self.map_height - target.rect.height + 20))

    def draw(self):
        # Desenha todos os sprites com o deslocamento da camera
        for sprite in sorted(self.sprites(), key=lambda x: x.rect.bottom):
            offset_pos = sprite.rect.topleft - self.offset
            self.display.blit(sprite.image, offset_pos)

    def update(self, *args):
        super().update(*args)  # Passa as teclas pressionadas para os sprites do grupo