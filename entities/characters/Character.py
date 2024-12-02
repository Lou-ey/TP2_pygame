import pygame
from utils.LifeBar import LifeBar
from utils.XPBar import XPBar
from utils.AudioPlayer import AudioPlayer

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

        self.audio_player = AudioPlayer()
        self.audio_player.load_sounds()

        self.combo_stage = 0
        self.max_combo_stage = 2
        self.attack_stage_duration = [10, 10]  # Duração de cada ataque
        self.attack_timer = 0

        # Carrega as animações
        self.idle_animation = [pygame.image.load(f"assets/images/player/knight/idle/0{i}.png").convert_alpha() for i in range(1, 6)]
        self.walk_animation = [pygame.image.load(f"assets/images/player/knight/walk/0{i}.png").convert_alpha() for i in range(1, 6)]
        self.attack_animation = [pygame.image.load(f"assets/images/player/knight/attack/0{i}.png").convert_alpha() for i in range(1, 12)]
        self.die_animation = [pygame.image.load(f"assets/images/player/knight/die/0{i}.png").convert_alpha() for i in range(1, 14)]

        # Ajuste das imagens e criação do retângulo de colisão
        self.image = pygame.transform.scale(self.idle_animation[0], (self.width, self.height))
        self.rect = self.image.get_rect(center=(self.x, self.y))  # Retângulo principal da imagem

        # Criar o collision_rect com offset proporcional
        collision_width = int(self.rect.width * 0.2)  # 20% da largura do rect principal
        collision_height = int(self.rect.height * 0.15)  # 15% da altura do rect principal

        # Centraliza o collision_rect no rect principal
        self.collision_rect = pygame.Rect(0, 0, collision_width, collision_height)
        #self.collision_rect.center = self.rect.center

        #self.attack_rect_width = int(self.rect.width * 0.3)  # 30% da largura do rect principal
        #self.attack_rect_height = int(self.rect.height * 0.4)  # 40% da altura do rect principal

        self.attack_rect = pygame.Rect(0, 0, 0, 0)
        self.attack_rect.center = self.rect.center

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
        self.die_animation_speed = 0.09
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
            self.combo_stage = 0
            self.attack_timer = self.attack_stage_duration[self.combo_stage]
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

        self.collision_rect.center = self.rect.center

        if self.facing_right:
            self.attack_rect.midleft = self.collision_rect.midright
        elif self.facing_left:
            self.attack_rect.midright = self.collision_rect.midleft

        # Escolhe a animação correta
        if self.is_attacking:
            self.animate_attack()
        elif self.is_moving:
            self.animate_walk()
            self.audio_player.play_sound('player_walk', 0.2)
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
        """Animação e lógica de ataque."""
        # Verifica se o personagem está a atacar
        if self.combo_stage < self.max_combo_stage:
            total_frames = len(self.attack_animation)  # Total de frames da animação
            mid_frame = total_frames // 2  # Frame do meio da animação

            # Define os intervalos para os dois ataques
            if self.combo_stage == 0:  # Primeiro golpe
                start_frame = 0
                end_frame = mid_frame  # Vai até o frame 5
            elif self.combo_stage == 1:  # Segundo golpe
                start_frame = mid_frame  # Começa do frame 6
                end_frame = total_frames  # Vai até o último frame

            # Atualiza o contador de frames
            self.frame_counter += self.attack_animation_speed

            # Verifica se a animação atual está no intervalo do combo
            if int(self.frame_counter) >= end_frame:
                self.frame_counter = end_frame - 1  # Mantém no último frame do estágio atual

            # Define a imagem da animação de ataque
            self.image = self.attack_animation[int(self.frame_counter)]

            # Define a hitbox do ataque
            if self.combo_stage == 0:  # Primeiro golpe
                self.attack_rect.width = int(self.rect.width * 0.35)
                self.attack_rect.height = int(self.rect.height * 0.45)
            elif self.combo_stage == 1:  # Segundo golpe
                self.attack_rect.width = int(self.rect.width * 0.35)
                self.attack_rect.height = int(self.rect.height * 0.45)

            # Atualiza o temporizador de ataque
            self.attack_timer -= 0.5

            # Verifica se o ataque terminou
            if self.attack_timer <= 0:
                self.combo_stage += 1  # Avança para o próximo ataque
                if self.combo_stage == 1:  # Verifica se é o último ataque
                    self.attack_rect.size = (0, 0)  # Desativa o ataque (hitbox)
                    self.attack_timer = self.attack_stage_duration[self.combo_stage]  # Atualiza o temporizador
                if self.combo_stage < self.max_combo_stage: # Verifica se não ultrapassou o estágio máximo
                    self.attack_timer = self.attack_stage_duration[self.combo_stage]  # Atualiza o temporizador
                    self.frame_counter = mid_frame  # Reseta o contador de frames para o próximo golpe
                else:
                    self.is_attacking = False  # Finaliza o ataque
                    self.attack_rect.size = (0, 0)  # Desativa o ataque (hitbox)
        else:
            self.is_attacking = False  # Caso tenha finalizado o combo

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
        if self.is_attacking and self.attack_rect.colliderect(enemy.collision_rect):
            enemy.take_damage(self.attack)

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
        self.audio_player.play_sound('player_hit', 0.2)

    def gain_xp(self, xp):
        self.xp_bar.current_xp += xp
        if self.xp_bar.current_xp >= self.xp_bar.max_xp:
            self.level_up()
            self.xp_bar.current_xp = 0
        self.xp_bar.update(self.xp_bar.current_xp)

    def level_up(self):
        if self.xp_bar.current_xp >= self.xp_bar.max_xp:
            self.current_level += 1
            self.xp_bar.max_xp *= 2
            self.xp_bar.current_xp = 0
            self.xp_bar.update_bar()
            self.audio_player.play_sound('level_up', 0.2)