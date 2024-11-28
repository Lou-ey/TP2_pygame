import pygame
from entities.enemies.Enemy import Enemy

class TorchGoblin(Enemy, pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)

        # Inicializa com atributos específicos do Goblin
        super().__init__(name="Goblin", health=50, attack=0.5, defense=5, speed=1, size=(60, 60))
        self.x = x
        self.y = y

        self.idle_animation = [pygame.image.load(f"assets/images/enemies/torch_goblin/idle/0{i}.png").convert_alpha() for i in range(1, 7)]
        self.walk_animation = [pygame.image.load(f"assets/images/enemies/torch_goblin/walk/0{i}.png").convert_alpha() for i in range(1, 6)]
        #self.die_animation = [pygame.image.load(f"assets/images/enemies/torch_goblin/die/0{i}.png").convert_alpha() for i in range(1, 7)]

        self.image = self.walk_animation[0]
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

        self.idle_animation_speed = 0.2
        self.walk_animation_speed = 0.1
        self.frame_counter = 0
        self.current_frame = 0

        self.is_facing_right = True

    def update(self, player_position):
        self.move_towards_player(player_position)
        self.animate_walk()
        #self.avoid_overlapping(enemies)

    def animate_idle(self):
        self.frame_counter += self.idle_animation_speed
        if self.frame_counter >= len(self.idle_animation):
            self.frame_counter = 0
        self.image = self.idle_animation[int(self.frame_counter)]

    def animate_walk(self):
        self.frame_counter += self.walk_animation_speed
        if self.frame_counter >= len(self.walk_animation):
            self.frame_counter = 0
        self.image = self.walk_animation[int(self.frame_counter)]