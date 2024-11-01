import pygame

class Character(pygame.sprite.Sprite):
    def __init__(self, name, health, attack, defense, speed, x, y, width, height):
        super().__init__()
        self.name = name
        self.health = health
        self.attack = attack
        self.defense = defense
        self.speed = speed
        #self.x = x
        #self.y = y
        self.width = width
        self.height = height
        self.displacement = 0

        self.idle_animation = [pygame.image.load(f"assets/images/player/idle/0{i}.png").convert_alpha() for i in range(1, 6)]

        self.walk_animation = [pygame.image.load(f"assets/images/player/walk/0{i}.png").convert_alpha() for i in range(1, 6)]

        self.attack_animation = [pygame.image.load(f"assets/images/player/attack_1/0{i}.png").convert_alpha() for i in range(1, 6)]

        #self.die_animation = [pygame.image.load(f"assets/images/player/die/0{i}.png").convert_alpha() for i in range(1, 7)]

        self.image = self.idle_animation[0]
        self.image = self.walk_animation[0]
        self.image = self.attack_animation[0]  # Use o primeiro quadro do ataque para começar
        self.rect = self.image.get_rect(topleft=(x, y))
        #self.image = self.die_animation[0]

        for i in range(len(self.idle_animation)):
            self.idle_animation[i] = pygame.transform.scale(self.idle_animation[i], (self.width, self.height))
            self.rect = self.idle_animation[i].get_rect(topleft=(x, y))
        for i in range(len(self.walk_animation)):
            self.walk_animation[i] = pygame.transform.scale(self.walk_animation[i], (self.width, self.height))
            self.rect = self.walk_animation[i].get_rect(topleft=(x, y))
        for i in range(len(self.attack_animation)):
            self.attack_animation[i] = pygame.transform.scale(self.attack_animation[i], (self.width, self.height))
            self.rect = self.attack_animation[i].get_rect(topleft=(x, y))

        self.current_frame = 0
        self.frame_counter = 0
        self.idle_animation_speed = 0.1
        self.walk_animation_speed = 0.2
        self.attack_animation_speed = 0.3
        self.is_moving = False
        self.is_attacking = False
        self.attack_duration = 15
        self.attack_timer = 0
        self.facing_left = False
        self.facing_right = True

    def update(self, keys):
        self.is_moving = False

        self.is_attacking = False

        keys = pygame.key.get_pressed()
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
        if keys[pygame.K_SPACE]:
            self.is_attacking = True
            self.attack_timer = self.attack_duration


        if self.is_attacking:
            self.animate_attack()
        elif self.is_moving:
            self.animate_walk()
        else:
            self.animate_idle()

    # Vira a a imagem do personagem para a esquerda ou direita
    def flip_animation(self):
        self.idle_animation = [pygame.transform.flip(image, True, False) for image in self.idle_animation]
        self.walk_animation = [pygame.transform.flip(image, True, False) for image in self.walk_animation]
        self.attack_animation = [pygame.transform.flip(image, True, False) for image in self.attack_animation]

    # Animação de idle
    def animate_idle(self):
        self.frame_counter += self.idle_animation_speed
        if self.frame_counter >= len(self.idle_animation):
            self.frame_counter = 0
        self.image = self.idle_animation[int(self.frame_counter)]

    # Animação de andar
    def animate_walk(self):
        self.frame_counter += self.walk_animation_speed
        if self.frame_counter >= len(self.walk_animation):
            self.frame_counter = 0
        self.image = self.walk_animation[int(self.frame_counter)]

    def animate_attack(self):
        """Atualiza a animação de ataque e controla seu término."""
        if self.attack_timer > 0:
            self.frame_counter += self.attack_animation_speed
            if int(self.frame_counter) >= len(self.attack_animation):
                self.frame_counter = 0  # Reseta para repetir a animação
            self.image = self.attack_animation[int(self.frame_counter)]

            # Reduz o temporizador a cada ciclo de atualização
            self.attack_timer -= 1
        else:
            # Termina o ataque quando o tempo expira
            self.is_attacking = False
            self.frame_counter = 0  # Reseta o quadro da animação
