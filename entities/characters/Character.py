import pygame
from utils.LifeBar import LifeBar
from utils.XPBar import XPBar
from entities.enemies.Enemy import Enemy

class Character(pygame.sprite.Sprite):
    def __init__(self, name, max_health, max_xp, attack, defense, speed, x, y, width, height):
        super().__init__()
        self.name = name
        self.max_health = max_health
        self.current_health = max_health
        self.max_xp = max_xp
        self.current_xp = 0
        self.health_bar_width = 100
        self.xp_bar_width = pygame.display.Info().current_w - 20
        self.current_level = 1
        self.attack = attack
        self.defense = defense
        self.speed = speed
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.displacement = 0

        # Carrega as animações
        self.idle_animation = [pygame.image.load(f"assets/images/player/knight/idle/0{i}.png").convert_alpha() for i in range(1, 6)]
        self.walk_animation = [pygame.image.load(f"assets/images/player/knight/walk/0{i}.png").convert_alpha() for i in range(1, 6)]
        self.attack_animation = [pygame.image.load(f"assets/images/player/knight/attack/0{i}.png").convert_alpha() for i in range(1, 12)]
        self.die_animation = [pygame.image.load(f"assets/images/player/knight/die/0{i}.png").convert_alpha() for i in range(1, 14)]

        # Ajuste das imagens e criação do retângulo de colisão
        self.image = self.idle_animation[0]
        self.rect = self.image.get_rect(center=(self.x, self.y))

        self.health_bar = LifeBar(self.max_health, self.current_health, self.health_bar_width)
        self.xp_bar = XPBar(self.max_xp, self.current_xp, self.xp_bar_width)

        # Escala das animações
        for i in range(len(self.idle_animation)):
            self.idle_animation[i] = pygame.transform.scale(self.idle_animation[i], (self.width, self.height))
        for i in range(len(self.walk_animation)):
            self.walk_animation[i] = pygame.transform.scale(self.walk_animation[i], (self.width, self.height))
        for i in range(len(self.attack_animation)):
            self.attack_animation[i] = pygame.transform.scale(self.attack_animation[i], (self.width, self.height))
        for i in range(len(self.die_animation)):
            self.die_animation[i] = pygame.transform.scale(self.die_animation[i], (self.width, self.height))

        # Variáveis de animação
        self.current_frame = 0
        self.frame_counter = 0
        self.idle_animation_speed = 0.1
        self.walk_animation_speed = 0.12
        self.attack_animation_speed = 0.25
        self.die_animation_speed = 0.1
        self.is_moving = False
        self.is_attacking = False
        self.is_dead = False
        self.attack_duration = 45
        self.attack_timer = 0
        self.facing_left = False
        self.facing_right = True

    def update(self, keys):
        self.is_moving = False

        # Inicia o ataque com o espaço
        if keys[pygame.K_SPACE] and not self.is_attacking:
            self.is_attacking = True
            self.attack_timer = self.attack_duration
            self.frame_counter = 0

        if self.is_dead: # Verifica se o personagem está morto
            self.die() # Animação de morte
            return

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
        #self.die_animation = [pygame.transform.flip(image, True, False) for image in self.die_animation]

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

    def animate_die(self):
        """Animação de morte."""
        if not self.is_dead:
            return

        self.frame_counter += self.die_animation_speed # Incrementa o contador de frames
        if int(self.frame_counter) < len(self.die_animation): # Verifica se o contador é maior que o número de frames
            self.image = self.die_animation[int(self.frame_counter)] # Atualiza a imagem
        else:
            self.image = self.die_animation[-1] # Mantém a última imagem

    def attack(self, enemy):
        """Ataque do personagem."""
        # cria um collider para o ataque
        attack_collider = pygame.Rect(self.rect.x, self.rect.y, self.width, self.height)
        attack_collider.width = 100
        attack_collider.height = 100
        if attack_collider.colliderect(enemy.rect):

            enemy.health -= self.attack - enemy.defense
            if enemy.health <= 0:
                enemy.kill()
                self.gain_xp(enemy.xp)

    def die(self):
        if self.current_health == 0:
            if not self.is_dead:
                self.is_dead = True
                self.frame_counter = 0
                self.animate_die()
                self.speed = 0
                self.is_moving = False
                self.is_attacking = False
            self.animate_die()

    def take_damage(self, damage):
        self.current_health = max(0, self.current_health - damage)
        self.health_bar.update(self.current_health)

    def gain_xp(self, xp):
        self.xp_bar.current_xp += xp
        if self.xp_bar.current_xp >= self.xp_bar.max_xp:
            self.level_up()
            self.xp_bar.current_xp = 0
        self.xp_bar.update(self.xp_bar.current_xp)

    def level_up(self):
        if self.xp_bar.current_xp == self.xp_bar.max_xp:
            self.current_level += 1
            self.xp_bar.max_xp *= 2
            self.xp_bar.current_xp = 0
            self.xp_bar.update_bar()