import pygame
import random

class Tree(pygame.sprite.Sprite):
    def __init__(self, x, y, tile_size):
        super().__init__()
        self.x = x
        self.y = y
        self.tile_size = tile_size

        self.animation_speed = random.uniform(0.07, 0.09)
        self.current_frame = 0
        self.frame_counter = 0

        self.idle_animation = [pygame.image.load(f"assets/images/map/tree/0{i}.png").convert_alpha() for i in range(1, 4)]

        self.image = self.idle_animation[self.current_frame]
        self.rect = self.image.get_rect(midbottom=(x, y))

    def update(self, *args):
        self.animate_idle()

    def animate_idle(self):
        self.frame_counter += self.animation_speed
        if self.frame_counter >= len(self.idle_animation):
            self.frame_counter = 0
        self.image = self.idle_animation[int(self.frame_counter)]
