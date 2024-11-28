import pygame
import random

class Bush(pygame.sprite.Sprite):
    def __init__(self, x, y, tile_size, bush_images):
        super().__init__()
        self.x = x
        self.y = y
        self.tile_size = tile_size

        self.image = random.choice(bush_images)
        self.image = pygame.transform.scale(self.image, (self.tile_size, self.tile_size))
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self, *args):
        pass