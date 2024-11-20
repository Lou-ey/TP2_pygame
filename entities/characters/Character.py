import pygame
from utils.LifeBar import LifeBar

class Character(pygame.sprite.Sprite):
    def __init__(self, name, max_health, attack, defense, speed, x, y, width, height):
        super().__init__()
        self.name = name
        self.max_health = max_health
        self.current_health = max_health
        self.attack = attack
        self.defense = defense
        self.speed = speed
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.displacement = 0

        # Carrega as animações
        self.idle_animation = [pygame.image.load(f"assets/images/player/idle/0{i}.png").convert_alpha() for i in range(1, 6)]
        self.walk_animation = [pygame.image.load(f"assets/images/player/walk/0{i}.png").convert_alpha() for i in range(1, 6)]
        self.attack_animation = [pygame.image.load(f"assets/images/player/attack/0{i}.png").convert_alpha() for i in range(1, 12)]

        # Ajuste das imagens e criação do retângulo de colisão
        self.image = self.idle_animation[0]
        self.rect = self.image.get_rect(center=(self.x, self.y))

        self.health_bar = LifeBar(self.max_health, self.current_health, 65, 10, (0, 255, 0), (255, 0, 0))

        # Escala das animações
        for i in range(len(self.idle_animation)):
            self.idle_animation[i] = pygame.transform.scale(self.idle_animation[i], (self.width, self.height))
        for i in range(len(self.walk_animation)):
            self.walk_animation[i] = pygame.transform.scale(self.walk_animation[i], (self.width, self.height))
        for i in range(len(self.attack_animation)):
            self.attack_animation[i] = pygame.transform.scale(self.attack_animation[i], (self.width, self.height))

        # Variáveis de animação
        self.current_frame = 0
        self.frame_counter = 0
        self.idle_animation_speed = 0.1
        self.walk_animation_speed = 0.12
        self.attack_animation_speed = 0.25
        self.is_moving = False
        self.is_attacking = False
        self.attack_duration = 45
        self.attack_timer = 0
        self.facing_left = False
        self.facing_right = True

    def update(self, keys):
        self.is_moving = False

        # Inicia o ataque com o botão esquerdo do mouse e reseta o contador de quadro
        if keys[pygame.K_SPACE] and not self.is_attacking:
            self.is_attacking = True
            self.attack_timer = self.attack_duration
            self.frame_counter = 0

        # Movimentação e orientação
        if not self.is_attacking:  # Impede que o movimento interrompa o ataque
            if keys[pygame.K_w]:
                self.rect.y -= self.speed
                self.is_moving = True
            if keys[pygame.K_s]:
                self.rect.y += self.speed
                self.is_moving = True
            if keys[pygame.K_a]:
                self.rect.x -= self.speed
                self.is_moving = True
                if not self.facing_left:
                    self.facing_left = True
                    self.facing_right = False
                    self.flip_animation()
            if keys[pygame.K_d]:
                self.rect.x += self.speed
                self.is_moving = True
                if self.facing_left:
                    self.facing_left = False
                    self.facing_right = True
                    self.flip_animation()

        # Escolhe a animação correta
        if self.is_attacking:
            self.animate_attack()
        elif self.is_moving:
            self.animate_walk()
        else:
            self.animate_idle()

    def flip_animation(self):
        """Inverte as animações para a direção em que o personagem está virado."""
        self.idle_animation = [pygame.transform.flip(image, True, False) for image in self.idle_animation]
        self.walk_animation = [pygame.transform.flip(image, True, False) for image in self.walk_animation]
        self.attack_animation = [pygame.transform.flip(image, True, False) for image in self.attack_animation]

    def animate_idle(self):
        """Animação de idle."""
        if not self.is_attacking:
            self.frame_counter += self.idle_animation_speed
            if self.frame_counter >= len(self.idle_animation):
                self.frame_counter = 0
            self.image = self.idle_animation[int(self.frame_counter)]

    def animate_walk(self):
        """Animação de caminhar."""
        if not self.is_attacking:
            self.frame_counter += self.walk_animation_speed
            if self.frame_counter >= len(self.walk_animation):
                self.frame_counter = 0
            self.image = self.walk_animation[int(self.frame_counter)]

    def animate_attack(self):
        """Animação de ataque."""
        if self.attack_timer > 0:
            self.frame_counter += self.attack_animation_speed
            if int(self.frame_counter) >= len(self.attack_animation):
                self.frame_counter = len(self.attack_animation) - 1  # Mantém o último quadro no ataque
            self.image = self.attack_animation[int(self.frame_counter)]
            self.attack_timer -= 1
        else:
            # Termina o ataque e reseta o estado
            self.is_attacking = False
            self.frame_counter = 0

    def take_damage(self, damage):
        self.current_health = max(0, self.current_health - damage)
        self.health_bar.update(self.current_health)

    def die(self):
        if self.current_health == 0:
            self.kill()