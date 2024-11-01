import pygame
from entities.enemies.Enemy import Enemy

class TorchGoblin(Enemy, pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)

        # Inicializa com atributos específicos do Goblin
        super().__init__(name="Goblin", health=50, attack=10, defense=5, speed=2)
        self.x = x
        self.y = y

        self.idle_animation = [pygame.image.load(f"assets/images/enemies/torch_goblin/idle/0{i}.png").convert_alpha() for i in range(1, 7)]
        #self.die_animation = [pygame.image.load(f"assets/images/enemies/torch_goblin/die/0{i}.png").convert_alpha() for i in range(1, 7)]

        # Carrega a imagem e define o retângulo para posicionamento
        self.image = self.idle_animation[0]
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        #self.image = self.die_animation[0]

        self.idle_animation_speed = 0.2
        self.frame_counter = 0
        self.current_frame = 0

    def attack(self, target):
        # Ataque especial do Goblin (pode ter um comportamento único)
        super().attack(target)  # Usa o ataque básico do Enemy como exemplo
        print("O torch_goblin usa um ataque rápido!")

    def update(self, player_position):
        self.animate_idle()

    def animate_idle(self):
        self.frame_counter += self.idle_animation_speed
        if self.frame_counter >= len(self.idle_animation):
            self.frame_counter = 0
        self.image = self.idle_animation[int(self.frame_counter)]