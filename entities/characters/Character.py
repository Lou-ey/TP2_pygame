import pygame

class Character(pygame.sprite.Sprite):
    def __init__(self, name, health, attack, defense, speed, x, y):
        super().__init__()
        self.name = name
        self.health = health
        self.attack = attack
        self.defense = defense
        self.speed = speed
        #self.x = x
        #self.y = y
        #self.width = 25
        #self.height = 25

        self.idle_animation = [pygame.image.load("assets/images/player/player_idle/00.png"),
                               pygame.image.load("assets/images/player/player_idle/01.png"),
                               pygame.image.load("assets/images/player/player_idle/02.png"),
                               pygame.image.load("assets/images/player/player_idle/03.png"),
                               pygame.image.load("assets/images/player/player_idle/04.png"),
                               pygame.image.load("assets/images/player/player_idle/05.png")]

        self.walk_animation = [pygame.image.load("assets/images/player/player_walk/00.png"),
                               pygame.image.load("assets/images/player/player_walk/01.png"),
                               pygame.image.load("assets/images/player/player_walk/02.png"),
                               pygame.image.load("assets/images/player/player_walk/03.png"),
                               pygame.image.load("assets/images/player/player_walk/04.png"),
                               pygame.image.load("assets/images/player/player_walk/05.png")]

        self.image = self.idle_animation[0]
        self.rect = self.image.get_rect(center=(x, y))

        self.current_frame = 0
        self.idle_animation_speed = 0.1
        self.walk_animation_speed = 0.2
        self.frame_counter = 0
        self.is_moving = False
        self.facing_left = False

    def update(self, keys):
        self.is_moving = False

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
                self.flip_animation()
        if keys[pygame.K_d]:
            self.rect.x += self.speed
            self.is_moving = True
            if self.facing_left:
                self.facing_left = False
                self.flip_animation()

        if self.is_moving:
            self.animate_walk()
        else:
            self.animate_idle()

    # Vira a a imagem do personagem para a esquerda ou direita
    def flip_animation(self):
        self.idle_animation = [pygame.transform.flip(image, True, False) for image in self.idle_animation]
        self.walk_animation = [pygame.transform.flip(image, True, False) for image in self.walk_animation]

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