import pygame
from entities.characters.Character import Character
from entities.enemies.Enemy import Enemy

class GameScene:
    def __init__(self):
        self.SCREEN_WIDTH = 800
        self.SCREEN_HEIGHT = 600
        self.SCREEN = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("Game Scene")

        self.character = Character("Player", 100, 10, 5, 10, 50, 50)
        self.enemy = Enemy("Enemy", 100, 10, 5, 10)

        self.background_color = (255, 255, 255)  # Branco

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.character.y -= self.character.speed
        if keys[pygame.K_a]:
            self.character.x -= self.character.speed
        if keys[pygame.K_s]:
            self.character.y += self.character.speed
        if keys[pygame.K_d]:
            self.character.x += self.character.speed

        if self.character.x < 0:
            self.character.x = 0
        if self.character.x > self.SCREEN_WIDTH - self.character.width:
            self.character.x = self.SCREEN_WIDTH - self.character.width
        if self.character.y < 0:
            self.character.y = 0
        if self.character.y > self.SCREEN_HEIGHT - self.character.height:
            self.character.y = self.SCREEN_HEIGHT - self.character.height

    def render(self):
        self.SCREEN.fill(self.background_color)

        pygame.draw.rect(self.SCREEN, (0, 0, 255), (self.character.x, self.character.y, self.character.width, self.character.height))

        pygame.display.update()

    def run(self):
        self.handle_events()
        self.update()
        self.render()
