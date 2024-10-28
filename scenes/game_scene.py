import pygame
from entities.characters.Character import Character
from entities.enemies.Enemy import Enemy

class GameScene:
    def __init__(self):
        self.SCREEN_WIDTH = 1000
        self.SCREEN_HEIGHT = 800
        self.SCREEN = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("Game Scene")

        self.TILE_SIZE = 60
        self.MAP_WIDTH = 50
        self.MAP_HEIGHT = 50

        self.map_layout = self.generate_map()
        self.tile_assets = self.load_assets()

        self.character = Character("Player", 100, 10, 5, 3, self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2)
        self.enemy = Enemy("Enemy", 100, 10, 5, 10)

        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.character)

        self.background_color = (39, 110, 58)

    def generate_map(self):
        return [[0 for _ in range(self.MAP_WIDTH)] for _ in range(self.MAP_HEIGHT)]

    def load_assets(self):
        grass_tile = pygame.image.load("assets/images/map/grass_tile.png")
        return {0: grass_tile}

    # Metodo para lidar com eventos
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()

    # Metodo para atualizar o jogo
    def update(self):
        keys = pygame.key.get_pressed()
        self.character.update(keys)
        self.all_sprites.update(keys)

    # Metodo para renderizar o jogo
    def render(self):
        self.SCREEN.fill((0, 0, 0))

        # Desenha o mapa
        for row in range(self.MAP_HEIGHT):
            for col in range(self.MAP_WIDTH):
                tile = self.map_layout[row][col]
                tile_asset = self.tile_assets[tile]
                self.SCREEN.blit(tile_asset, (col * self.TILE_SIZE, row * self.TILE_SIZE))

        self.all_sprites.draw(self.SCREEN)

        pygame.display.update()

    # Metodo para rodar o jogo
    def run(self):
        self.handle_events()
        self.update()
        self.render()