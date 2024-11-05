import pygame

class Enemy(pygame.sprite.Sprite):
    def __init__(self, name, health, attack, defense, speed, size):
        super().__init__()
        self.name = name
        self.health = health
        self.attack = attack
        self.defense = defense
        self.speed = speed
        self.size = size

        self.image = None
        self.rect = None

        self.collider = pygame.Rect(0, 0, self.size[0], self.size[1])

        self.original_image = self.image
        self.is_facing_right = True

        self.idle_animation = None
        self.walk_animation = None

    def flip(self):
        self.walk_animation = [pygame.transform.flip(image, True, False) for image in self.walk_animation]

    def move_towards_player(self, player_position):
        if isinstance(player_position, tuple) and len(player_position) == 2:
            # Calcula a direção para o jogador
            direction = pygame.math.Vector2(player_position) - pygame.math.Vector2(self.rect.center)

            # Normaliza a direção para evitar divisão por zero
            if direction.length() != 0:
                direction = direction.normalize()

            # Atualiza a posição do inimigo
            self.rect.x += direction.x * self.speed
            self.rect.y += direction.y * self.speed

            # Atualiza a direção do inimigo
            if direction.x > 0 and not self.is_facing_right:
                self.is_facing_right = True
                self.flip()
            elif direction.x < 0 and self.is_facing_right:
                self.is_facing_right = False
                self.flip()

    def avoid_overlapping(self, enemies):
        # Define uma pequena distância de segurança
        distancia_segura = 10
        for enemy in enemies:
            if enemy != self:
                # Verifica a colisão
                if self.rect.colliderect(enemy.rect):
                    # Calcula a direção de separação
                    separacao = pygame.math.Vector2(self.rect.center) - pygame.math.Vector2(enemy.rect.center)

                    # Se a distância de separação for pequena, aplica o movimento
                    if separacao.length() != 0:
                        separacao = separacao.normalize()

                        # Ajuste para manter o inimigo na área jogável
                        self.rect.x += separacao.x * distancia_segura
                        self.rect.y += separacao.y * distancia_segura

