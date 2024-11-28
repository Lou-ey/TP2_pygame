import pygame
import random
import os.path
from entities.characters.Character import Character
from entities.enemies.types.TorchGoblin import TorchGoblin
from entities.objects.Tree import Tree
from entities.objects.Stone import Stone
from entities.objects.Mushroom import Mushroom
from entities.objects.Bush import Bush
from utils.CameraGroup import CameraGroup
from utils.Cursor import Cursor

class GameScene:
    def __init__(self):
        self.SCREEN_WIDTH = 800 #pygame.display.Info().current_w
        self.SCREEN_HEIGHT = 600 #pygame.display.Info().current_h
        self.SCREEN = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
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
        self.character = Character("Player", 100, 1000, 10, 5, 2, self.MAP_WIDTH * self.TILE_SIZE // 2, self.MAP_HEIGHT * self.TILE_SIZE // 2, self.CHARACTER_SIZE[0], self.CHARACTER_SIZE[1])
        self.camera.add(self.character) # Adiciona o personagem à camera

        # Instancia dos inimigos
        self.enemies = pygame.sprite.Group()

        self.num_trees = 2000
        self.num_stones = 1000
        self.num_mushrooms = 1000
        self.num_bushes = 1000

        self.generate_trees(self.num_trees)
        self.generate_stones(self.num_stones)
        self.generate_mushrooms(self.num_mushrooms)
        self.generate_bushes(self.num_bushes)

        self.background_color = (39, 110, 58)

        self.enemies_spawned_limit = 50

        # Variável para controlar o tempo entre spawns
        self.spawn_interval = 1000 # 1 segundo
        self.last_spawn_time = pygame.time.get_ticks()

        self.is_paused = False

        # busca todas as músicas disponíveis
        musics = os.listdir("assets/sounds/game")

        for music in musics:
            if music.endswith(".wav"):
                self.music = f"assets/sounds/game/{music}"

        # inicia a música
        pygame.mixer.init()
        pygame.mixer.music.load(self.music)
        pygame.mixer.music.set_volume(0.05)
        pygame.mixer.music.play(-1)

    def stop_music(self):
        pygame.mixer.music.stop()

    def generate_map(self):
        empty_map = [[0 for _ in range(self.MAP_WIDTH)] for _ in range(self.MAP_HEIGHT)]
        return empty_map

    def generate_trees(self, num_trees):
        for _ in range(num_trees):
            tree_x = random.randint(0, self.MAP_WIDTH - 1) * self.TILE_SIZE
            tree_y = random.randint(0, self.MAP_HEIGHT - 1) * self.TILE_SIZE
            tree = Tree(tree_x, tree_y, self.TILE_SIZE)
            self.camera.add(tree)  # Adiciona as árvores à câmera

    def generate_stones(self, num_stones):
        stone_images = [
            pygame.image.load("assets/images/map/stone/stone_01.png").convert_alpha(),
            pygame.image.load("assets/images/map/stone/stone_02.png").convert_alpha(),
            pygame.image.load("assets/images/map/stone/stone_03.png").convert_alpha(),
        ]

        for _ in range(num_stones):
            stone_x = random.randint(0, self.MAP_WIDTH - 1) * self.TILE_SIZE
            stone_y = random.randint(0, self.MAP_HEIGHT - 1) * self.TILE_SIZE
            stone = Stone(stone_x, stone_y, self.TILE_SIZE, stone_images)
            self.camera.add(stone)

    def generate_mushrooms(self, num_mushrooms):
        mushroom_images = [
            pygame.image.load("assets/images/map/mushroom/mushroom_01.png").convert_alpha(),
            pygame.image.load("assets/images/map/mushroom/mushroom_02.png").convert_alpha(),
            pygame.image.load("assets/images/map/mushroom/mushroom_03.png").convert_alpha(),
        ]

        for _ in range(num_mushrooms):
            mushroom_x = random.randint(0, self.MAP_WIDTH - 1) * self.TILE_SIZE
            mushroom_y = random.randint(0, self.MAP_HEIGHT - 1) * self.TILE_SIZE
            mushroom = Mushroom(mushroom_x, mushroom_y, self.TILE_SIZE, mushroom_images)
            self.camera.add(mushroom)

    def generate_bushes(self, num_bushes):
        # Carrega as imagens dos bushes (carregar uma vez para evitar repetição)
        bush_images = [
            pygame.image.load("assets/images/map/bush/bush_01.png").convert_alpha(),
            pygame.image.load("assets/images/map/bush/bush_02.png").convert_alpha(),
            pygame.image.load("assets/images/map/bush/bush_03.png").convert_alpha(),
        ]

        for _ in range(num_bushes):
            bush_x = random.randint(0, self.MAP_WIDTH - 1) * self.TILE_SIZE
            bush_y = random.randint(0, self.MAP_HEIGHT - 1) * self.TILE_SIZE
            bush = Bush(bush_x, bush_y, self.TILE_SIZE, bush_images)
            self.camera.add(bush)

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

    def pause_game(self):
        self.is_paused = not self.is_paused
        if self.is_paused:
            pygame.mixer.music.pause()
            self.cursor.show()
        else:
            pygame.mixer.music.unpause()
            self.cursor.hide()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # pause the game
                    self.pause_game()
                if event.key == pygame.K_LCTRL:
                    self.cursor.show()
                ### apenas para teste
                if event.key == pygame.K_CAPSLOCK:
                    self.character.gain_xp(100)
                ###
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LCTRL:
                    self.cursor.hide()

    def culling(self, character_x, character_y):
        character_tile_x = character_x // self.TILE_SIZE
        character_tile_y = character_y // self.TILE_SIZE

        # Define os limites visíveis
        visible_range_x = 20
        visible_range_y = 15

        # Calcula os limites da área visível considerando as bordas do mapa
        min_x = max(0, character_tile_x - visible_range_x)
        max_x = min(self.MAP_WIDTH, character_tile_x + visible_range_x)
        min_y = max(0, character_tile_y - visible_range_y)
        max_y = min(self.MAP_HEIGHT, character_tile_y + visible_range_y)

        # Desenha o mapa dentro da área visível
        for row in range(min_y, max_y):
            for col in range(min_x, max_x):
                tile = self.map_layout[row][col]
                tile_asset = self.tile_assets[tile]
                pos_x = col * self.TILE_SIZE - self.camera.offset.x
                pos_y = row * self.TILE_SIZE - self.camera.offset.y
                self.SCREEN.blit(tile_asset, (pos_x, pos_y))

    def update(self):
        keys = pygame.key.get_pressed()
        self.character.update(keys)
        self.camera.center_on(self.character)  # Centraliza a câmera no personagem
        self.camera.update(keys)
        self.cursor.update()
        self.character.die()

        # Controla o tempo para spawnar novos inimigos
        current_time = pygame.time.get_ticks() # tick atual
        num_current_enemies = len(self.enemies) # Número de inimigos atualmente na tela
        if current_time - self.last_spawn_time >= self.spawn_interval and num_current_enemies < self.enemies_spawned_limit: #
            self.spawn_enemy(TorchGoblin)  # Spawna um novo goblin fora da area visível
            self.last_spawn_time = current_time
        else:
            # para de spawnar inimigos
            pass

        player_position = self.character.rect.center
        for enemy in self.enemies:
            enemy.update(player_position)

            # Verifica se o inimigo colidiu com o personagem
            if self.character.rect.colliderect(enemy.rect):
                self.character.take_damage(enemy.attack)

    def render(self):
        self.SCREEN.fill(self.background_color)

        character_x, character_y = self.character.rect.center
        self.culling(character_x, character_y)

        # Desenha todos os sprites controlados pela câmera
        self.camera.draw()

        # Render a barra de vida do personagem
        health_bar_offset_y = 5  # Distância acima do personagem
        # Posição da barra de vida
        health_bar_position = (self.character.rect.x + 35 - self.camera.offset.x,
                            self.character.rect.y - self.camera.offset.y - health_bar_offset_y) # Centraliza a barra de vida
        self.SCREEN.blit(self.character.health_bar.image, health_bar_position)

        self.SCREEN.blit(self.character.xp_bar.image, (10, 10))
        level_label = pygame.font.Font(os.path.join('assets/fonts/DungeonFont.ttf'), 30).render(f"Level: {self.character.current_level}", True, (255, 255, 255))
        xp_label = pygame.font.Font(os.path.join('assets/fonts/DungeonFont.ttf'), 15).render(f"XP: {self.character.xp_bar.current_xp}/{self.character.xp_bar.max_xp}", True, (255, 255, 255))
        self.SCREEN.blit(level_label, (10, 30))
        self.SCREEN.blit(xp_label, (self.SCREEN_WIDTH - 73, 25))

        # Desenha o cursor se ele tiver uma imagem
        if self.cursor.image:
            self.cursor.draw(self.SCREEN)

        # Desenha o rect do personagem ajustado pela câmera
        pygame.draw.rect(
            self.SCREEN,(0, 0, 255),
            pygame.Rect(
                self.character.rect.x - self.camera.offset.x,
                self.character.rect.y - self.camera.offset.y,
                self.character.rect.width,
                self.character.rect.height,
                ),
        2,
        )

        # Desenha o rect dos inimigos ajustado pela câmera
        for enemy in self.enemies:
            pygame.draw.rect(self.SCREEN,(255, 0, 0),
                             pygame.Rect(
                                 enemy.rect.x - self.camera.offset.x,
                                 enemy.rect.y - self.camera.offset.y,
                                 enemy.rect.width, enemy.rect.height),
                             2)

        pygame.display.update()

    def run(self):
        self.handle_events()
        self.update()
        self.render()