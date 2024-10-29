import pygame
from entities.characters.Character import Character
from entities.objects.Tree import Tree
from utils.CameraGroup import CameraGroup
import random

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

        self.camera = CameraGroup(self.SCREEN_WIDTH, self.SCREEN_HEIGHT, self.MAP_WIDTH * self.TILE_SIZE, self.MAP_HEIGHT * self.TILE_SIZE)

        self.character = Character("Player", 100, 10, 5, 3, self.MAP_WIDTH * self.TILE_SIZE // 2, self.MAP_HEIGHT * self.TILE_SIZE // 2)
        self.camera.add(self.character)

        self.num_trees = 15

        self.generate_trees(self.num_trees)
        self.background_color = (39, 110, 58)

    def generate_map(self):
        return [[0 for _ in range(self.MAP_WIDTH)] for _ in range(self.MAP_HEIGHT)]

    def generate_trees(self, num_trees):
        for _ in range(num_trees):
            tree_x = random.randint(0, self.MAP_WIDTH - 1) * self.TILE_SIZE
            tree_y = random.randint(0, self.MAP_HEIGHT - 1) * self.TILE_SIZE
            tree = Tree(tree_x, tree_y, self.TILE_SIZE)
            self.camera.add(tree)  # Adiciona as árvores à câmera

    def load_assets(self):
        grass_tile = pygame.image.load("assets/images/map/grass_tile.png")
        return {0: grass_tile}

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
        self.character.update(keys)
        self.camera.center_on(self.character)  # Centraliza a câmera no personagem
        self.camera.update(keys)

    def render(self):
        self.SCREEN.fill(self.background_color)

        # Desenha o mapa usando a câmera
        for row in range(self.MAP_HEIGHT):
            for col in range(self.MAP_WIDTH):
                tile = self.map_layout[row][col]
                tile_asset = self.tile_assets[tile]
                pos_x = col * self.TILE_SIZE - self.camera.offset.x
                pos_y = row * self.TILE_SIZE - self.camera.offset.y
                self.SCREEN.blit(tile_asset, (pos_x, pos_y))

        # Desenha todos os sprites controlados pela câmera
        self.camera.draw()
        pygame.display.update()

    def run(self):
        self.handle_events()
        self.update()
        self.render()