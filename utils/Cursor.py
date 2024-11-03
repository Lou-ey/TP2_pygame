import pygame

class Cursor(pygame.sprite.Sprite):
    def __init__(self, image_path, size):
        super().__init__()
        self.image_path = image_path
        self.size = size
        if image_path:
            self.image = pygame.image.load(image_path).convert_alpha()

        self.rect = self.image.get_rect()

        pygame.mouse.set_visible(False)

    def update(self):
        self.rect.topleft = pygame.mouse.get_pos()

    def draw(self, surface):
        self.image = pygame.transform.scale(self.image, self.size)
        surface.blit(self.image, self.rect.topleft)

    def hide(self):
        self.image = None

    def show(self):
        self.image = pygame.image.load(self.image_path).convert_alpha()