import pygame
import random

class Enemy(pygame.sprite.Sprite):
    def __init__(self, name, health, attack, defense, speed, width, height, xp_range):
        super().__init__()
        self.name = name
        self.health = health
        self.attack = attack
        self.defense = defense
        self.speed = speed
        self.width = width
        self.height = height
        self.xp_range = xp_range
        self.is_defeated = False

        self.image = None
        self.rect = None
        self.collision_rect = None

        self.original_image = self.image
        self.is_facing_right = True

        self.take_damage_image = None

        self.idle_animation = None
        self.walk_animation = None

    def flip(self):
        self.walk_animation = [pygame.transform.flip(image, True, False) for image in self.walk_animation]
        self.take_damage_image = pygame.transform.flip(self.take_damage_image, True, False)

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

    def avoid_overlapping(self, enemies, character):
        # Define uma pequena distância de segurança
        distancia_segura = 1

        # Evitar overlap com outros inimigos
        for enemy in enemies:
            if enemy != self:
                if self.collision_rect.colliderect(enemy.collision_rect):
                    # Calcula a direção de separação
                    separacao = pygame.math.Vector2(self.rect.center) - pygame.math.Vector2(enemy.collision_rect.center)
                    if separacao.length() != 0:
                        separacao = separacao.normalize()
                        self.rect.x += separacao.x * distancia_segura
                        self.rect.y += separacao.y * distancia_segura

        # Evitar overlap com o personagem
        if self.collision_rect.colliderect(character.collision_rect):
            separacao = pygame.math.Vector2(self.rect.center) - pygame.math.Vector2(character.collision_rect.center)
            if separacao.length() != 0:
                separacao = separacao.normalize()
                self.rect.x += separacao.x * distancia_segura
                self.rect.y += separacao.y * distancia_segura

    def give_xp(self):
        """Calcula e retorna XP se o inimigo foi derrotado"""
        if self.is_defeated:
            return random.randint(*self.xp_range)
        return 0  # Retorna 0 se o inimigo ainda não foi derrotado

    def die(self):
        """Executa a animação de morte e remove o inimigo"""
        self.is_defeated = True
        self.kill()

    def take_damage(self, damage, attacker_position):
        """Reduz a vida do inimigo e verifica se ele foi derrotado, aplica knockback"""
        self.health -= damage
        # O inimigo fica branquinho ao tomar dano
        self.image = self.take_damage_image

        # Calcular a direção do knockback (oposta à direção do atacante)
        direction = pygame.math.Vector2(self.rect.center) - pygame.math.Vector2(attacker_position)
        direction = direction.normalize()  # Normaliza o vetor para garantir que a força do empurrão seja consistente

        # Aplica o knockback com a força especificada
        self.knockback(direction, 5)

        if self.health <= 0:
            self.die()

    def knockback(self, direction, force):
        """Empurra o inimigo na direção especificada"""
        self.rect.x += direction.x * force
        self.rect.y += direction.y * force