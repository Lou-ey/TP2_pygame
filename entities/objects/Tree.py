import pygame
import random

class Tree(pygame.sprite.Sprite):
    def __init__(self, x, y, tile_size):
        super().__init__()
        self.x = x
        self.y = y
        self.tile_size = tile_size

        self.animation_speed = 0.1
        self.current_frame = 0


        self.idle_animation = [pygame.image.load("assets/images/map/tree/00.png"),
                               pygame.image.load("assets/images/map/tree/01.png"),
                               pygame.image.load("assets/images/map/tree/02.png"),
                               pygame.image.load("assets/images/map/tree/03.png"),]

        self.image = self.idle_animation[self.current_frame]
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

        self.frame_counter = 0

    def update(self, *args):
        self.animate_idle()

    def animate_idle(self):
        self.frame_counter += 1
        if self.frame_counter >= 60 * self.animation_speed:
            self.frame_counter = 0
            self.current_frame = (self.current_frame + 1) % len(self.idle_animation)
            self.image = self.idle_animation[self.current_frame]
