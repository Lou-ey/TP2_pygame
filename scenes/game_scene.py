import pygame
from entities.characters.Character import Character
from entities.enemies.types.TorchGoblin import TorchGoblin
from entities.objects.Tree import Tree
from utils.CameraGroup import CameraGroup
from utils.Cursor import Cursor
import random

class GameScene:
    def __init__(self):
        self.SCREEN_WIDTH = pygame.display.Info().current_w
        self.SCREEN_HEIGHT = pygame.display.Info().current_h
        self.SCREEN = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT), pygame.FULLSCREEN)
        pygame.display.set_caption("Game Scene")

        self.TILE_SIZE = 64
        self.MAP_WIDTH = 500
        self.MAP_HEIGHT = 500
        self.CURSOR_SIZE = (15, 23)
        self.CHARACTER_SIZE = (170, 170)
        self.map_layout = self.generate_map()
        self.tile_assets = self.load_grass_assets()

        # Instancia da camera
        self.camera = CameraGroup(self.SCREEN_WIDTH, self.SCREEN_HEIGHT, self.MAP_WIDTH * self.TILE_SIZE, self.MAP_HEIGHT * self.TILE_SIZE)
        self.cursor = Cursor("assets/images/UI/pointer/01.png", self.CURSOR_SIZE)  # Instancia do cursor

        self.cursor.hide()  # Esconde o cursor

        # Instancia do personagem
        self.character = Character("Player", 100, 10, 5, 2, self.MAP_WIDTH * self.TILE_SIZE // 2, self.MAP_HEIGHT * self.TILE_SIZE // 2, self.CHARACTER_SIZE[0], self.CHARACTER_SIZE[1])
        self.camera.add(self.character) # Adiciona o personagem à camera

        # Instancia dos inimigos
        self.enemies = pygame.sprite.Group()

        self.num_trees = 2000

        self.generate_trees(self.num_trees)

        self.background_color = (39, 110, 58)

        # Variável para controlar o tempo entre spawns
        self.spawn_interval = 1000  # 500 milissegundos (2 spawns por segundo)
        self.last_spawn_time = pygame.time.get_ticks()

    def generate_map(self):
        empty_map = [[0 for _ in range(self.MAP_WIDTH)] for _ in range(self.MAP_HEIGHT)]
        return empty_map

    def generate_trees(self, num_trees):
        for _ in range(num_trees):
            tree_x = random.randint(0, self.MAP_WIDTH - 1) * self.TILE_SIZE
            tree_y = random.randint(0, self.MAP_HEIGHT - 1) * self.TILE_SIZE
            tree = Tree(tree_x, tree_y, self.TILE_SIZE)
            self.camera.add(tree)  # Adiciona as árvores à câmera

    def spawn_enemy(self, enemy_class):
        """Função para spawnar inimigos fora da área visível, mas perto do personagem."""
        visible_margin = 100  # Margem além da área visível
        spawn_margin = 50     # Margem de spawn adicional ao redor da área visível

        # Centro do personagem
        character_x, character_y = self.character.rect.center

        # Posição de spawn
        spawn_x, spawn_y = character_x, character_y
        if random.choice([True, False]):
            # Horizontalmente além da área visível
            spawn_x += random.choice([-1, 1]) * (self.SCREEN_WIDTH // 2 + visible_margin + spawn_margin)
            spawn_y += random.randint(-self.SCREEN_HEIGHT // 2, self.SCREEN_HEIGHT // 2)
        else:
            # Verticalmente além da área visível
            spawn_x += random.randint(-self.SCREEN_WIDTH // 2, self.SCREEN_WIDTH // 2)
            spawn_y += random.choice([-1, 1]) * (self.SCREEN_HEIGHT // 2 + visible_margin + spawn_margin)

        # Cria e adiciona o inimigo
        new_enemy = enemy_class(spawn_x, spawn_y)
        self.enemies.add(new_enemy)
        self.camera.add(new_enemy)

    def load_grass_assets(self):
        grass_tile = pygame.image.load("assets/images/map/ground/grass_tile.png").convert_alpha()
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
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL:
                    self.cursor.show()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LCTRL:
                    self.cursor.hide()

    def update(self):
        keys = pygame.key.get_pressed()
        self.character.update(keys)
        self.camera.center_on(self.character)  # Centraliza a câmera no personagem
        self.camera.update(keys)
        self.cursor.update()

        # Controla o tempo para spawnar novos inimigos
        current_time = pygame.time.get_ticks()
        if current_time - self.last_spawn_time >= self.spawn_interval:
            self.spawn_enemy(TorchGoblin)  # Spawna um novo goblin fora da area visível
            self.last_spawn_time = current_time

        player_position = self.character.rect.center
        for enemy in self.enemies:
            enemy.update(player_position)

    def culling(self, character_x, character_y):
        # Define as coordenadas do personagem em tiles
        character_tile_x = character_x // self.TILE_SIZE
        character_tile_y = character_y // self.TILE_SIZE

        # Quantidade de tiles visíveis ao redor do personagem
        visible_range_x = 20
        visible_range_y = 10

        # Ajusta a área visível em X, considerando as bordas do mapa
        if character_tile_x < visible_range_x:
            # Quando o personagem está perto do lado esquerdo do mapa
            visible_tiles_x = range(0, visible_range_x * 2)
        elif character_tile_x > self.MAP_WIDTH - visible_range_x:
            # Quando o personagem está perto do lado direito do mapa
            visible_tiles_x = range(self.MAP_WIDTH - visible_range_x * 2, self.MAP_WIDTH)
        else:
            # Centro da área visível no personagem
            visible_tiles_x = range(character_tile_x - visible_range_x, character_tile_x + visible_range_x)

        # Ajusta a área visível em Y, considerando as bordas do mapa
        if character_tile_y < visible_range_y:
            # Quando o personagem está perto do topo do mapa
            visible_tiles_y = range(0, visible_range_y * 2)
        elif character_tile_y > self.MAP_HEIGHT - visible_range_y:
            # Quando o personagem está perto da parte inferior do mapa
            visible_tiles_y = range(self.MAP_HEIGHT - visible_range_y * 2, self.MAP_HEIGHT)
        else:
            # Centro da área visível no personagem
            visible_tiles_y = range(character_tile_y - visible_range_y, character_tile_y + visible_range_y)

        # Desenha o mapa usando a câmera
        for row in visible_tiles_y:
            for col in visible_tiles_x:
                tile = self.map_layout[row][col]
                tile_asset = self.tile_assets[tile]
                pos_x = col * self.TILE_SIZE - self.camera.offset.x
                pos_y = row * self.TILE_SIZE - self.camera.offset.y
                self.SCREEN.blit(tile_asset, (pos_x, pos_y))

    def render(self):
        self.SCREEN.fill(self.background_color)

        character_x, character_y = self.character.rect.center

        self.culling(character_x, character_y)

        # Desenha todos os sprites controlados pela câmera
        self.camera.draw()

        # Desenha o cursor se ele tiver uma imagem
        if self.cursor.image:
            self.cursor.draw(self.SCREEN)

        pygame.display.update()

    def run(self):
        self.handle_events()
        self.update()
        self.render()