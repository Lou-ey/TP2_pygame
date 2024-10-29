import pygame
import random

class Tree(pygame.sprite.Sprite):
    def __init__(self, x, y, tile_size):
        super().__init__()
        self.x = x
        self.y = y
        self.tile_size = tile_size

        self.animation_speed = random.uniform(0.1, 0.2)
        self.current_frame = 0


        self.idle_animation = [pygame.image.load("assets/images/map/tree/00.png"),
                               pygame.image.load("assets/images/map/tree/01.png"),
                               pygame.image.load("assets/images/map/tree/02.png"),
                               pygame.image.load("assets/images/map/tree/03.png"),]

        self.image = self.idle_animation[self.current_frame]
        self.rect = self.image.get_rect(midbottom=(x, y))

        self.frame_counter = 0

    def update(self, *args):
        self.animate_idle()

    def animate_idle(self):
        self.frame_counter += self.animation_speed
        if self.frame_counter >= len(self.idle_animation):
            self.frame_counter = 0
        self.image = self.idle_animation[int(self.frame_counter)]
