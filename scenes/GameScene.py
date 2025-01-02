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
from utils.AudioPlayer import AudioPlayer
from utils.Cursor import Cursor
from scenes.MainMenu import MainMenu
from scenes.GameOver import GameOver
from scenes.Pause import Pause
from utils.State import State
from entities.objects.HealingItem import HealingItem

class GameScene:
    def __init__(self):
        self.SCREEN_WIDTH = pygame.display.Info().current_w
        self.SCREEN_HEIGHT = pygame.display.Info().current_h
        self.SCREEN = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT), pygame.WINDOWMAXIMIZED)
        pygame.display.set_caption("Cavaleiro Jeitoso")

        self.TILE_SIZE = 64
        self.MAP_WIDTH = 60
        self.MAP_HEIGHT = 60
        self.CURSOR_SIZE = (15, 23)
        self.CHARACTER_SIZE = (170, 170)
        self.map_layout = self.generate_map()
        self.tile_assets = self.load_grass_assets()

        # Instancia da camera
        self.camera = CameraGroup(self.SCREEN_WIDTH, self.SCREEN_HEIGHT, self.MAP_WIDTH * self.TILE_SIZE, self.MAP_HEIGHT * self.TILE_SIZE)
        self.cursor = Cursor("assets/images/UI/pointer/01.png", self.CURSOR_SIZE)  # Instancia do cursor

        self.current_state = State.GAME

        self.cursor.hide()  # Esconde o cursor

        # Instancia do personagem
        self.character = Character("Player", 100, 10, 25, 5, 2, self.MAP_WIDTH * self.TILE_SIZE // 2, self.MAP_HEIGHT * self.TILE_SIZE // 2, self.CHARACTER_SIZE[0], self.CHARACTER_SIZE[1], 10, 1)
        self.camera.add(self.character) # Adiciona o personagem à camera

        # Instancia dos inimigos
        self.enemies = pygame.sprite.Group()

        self.num_trees = 500
        self.num_stones = 200
        self.num_mushrooms = 200
        self.num_bushes = 200
        self.num_items = 5

        self.generate_trees(self.num_trees)
        self.generate_stones(self.num_stones)
        self.generate_mushrooms(self.num_mushrooms)
        self.generate_bushes(self.num_bushes)
        self.generate_healing_items(self.num_items)

        self.background_color = (39, 110, 58)

        self.enemies_spawned_limit = 50

        # Variável para controlar o tempo entre spawns
        self.spawn_interval = 1000 # 1 segundo
        self.last_spawn_time = pygame.time.get_ticks()

        self.menu_manager = MainMenu()

        # Instancia do AudioPlayer
        self.audio_player = AudioPlayer()
        self.audio_player.load_music()
        self.audio_player.load_sounds()
        self.audio_player.play_music()

        self.game_over_screen = GameOver(self.SCREEN)
        self.pause_screen = Pause(self.SCREEN, self)

        self.is_paused = False
        self.is_game_over = False
        self.is_muted = False

        self.game_over_start_time = None

        self.tutorial_movement = pygame.image.load("assets/images/UI/menuUI/AWSD.png").convert_alpha()
        self.tutorial_movement_scale = pygame.transform.scale(self.tutorial_movement, (self.SCREEN.get_width() * 0.09, self.SCREEN.get_height() * 0.09))
        self.tutorial_attack = pygame.image.load("assets/images/UI/menuUI/space_bar.png").convert_alpha()
        self.tutorial_attack_scale = pygame.transform.scale(self.tutorial_attack, (self.SCREEN.get_width() * 0.08, self.SCREEN.get_height() * 0.06))
        self.tutorial_pause = pygame.image.load("assets/images/UI/menuUI/esc.png").convert_alpha()
        self.tutorial_pause_scale = pygame.transform.scale(self.tutorial_pause, (self.SCREEN.get_width() * 0.04, self.SCREEN.get_height() * 0.06))

    # gera um mapa vazio e retorna-o
    def generate_map(self):
        empty_map = [[0 for _ in range(self.MAP_WIDTH)] for _ in range(self.MAP_HEIGHT)]
        return empty_map

    # gera árvores aleatórias no mapa
    def generate_trees(self, num_trees):
        for _ in range(num_trees):
            tree_x = random.randint(0, self.MAP_WIDTH - 1) * self.TILE_SIZE
            tree_y = random.randint(0, self.MAP_HEIGHT - 1) * self.TILE_SIZE
            tree = Tree(tree_x, tree_y, self.TILE_SIZE) # Instancia uma árvore
            self.camera.add(tree)  # Adiciona as árvores à câmera

    def generate_stones(self, num_stones):
        # diferentes imagens de pedras
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

    def generate_healing_items(self, num_items):
        for _ in range(num_items):
            item_x = random.randint(0, self.MAP_WIDTH - 1) * self.TILE_SIZE
            item_y = random.randint(0, self.MAP_HEIGHT - 1) * self.TILE_SIZE
            healing_potion = HealingItem("Healing Potion", 25, 30, 30)
            healing_potion.rect.x = item_x
            healing_potion.rect.y = item_y
            self.camera.add(healing_potion)

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

    # Da load dos assets do chão
    def load_grass_assets(self):
        grass_tile = pygame.image.load("assets/images/map/ground/grass_tile.png").convert_alpha()
        return {0: grass_tile}

    def restart_game(self):
        self.__init__()

    # Lida com os eventos do jogo (teclas pressionadas, cliques, etc)
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE and not self.is_game_over:
                    self.is_paused = not self.is_paused
                    if self.is_paused:
                        self.audio_player.pause_music()
                    else:
                        self.audio_player.unpause_music()
                if self.is_game_over:
                    if event.key == pygame.K_r:
                        self.restart_game()
                    if event.key == pygame.K_e:
                        quit()
                if event.key == pygame.K_LCTRL:
                    self.cursor.show()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LCTRL:
                    self.cursor.hide()

        self.audio_player.handle_music_event()

    # Culling é uma técnica de otimização que consiste em renderizar apenas o que está visível no ecrã neste caso apenas os assets do chão
    def culling(self, character_x, character_y):
        character_tile_x = character_x // self.TILE_SIZE
        character_tile_y = character_y // self.TILE_SIZE

        # Define os limites visíveis
        visible_range_x = 15
        visible_range_y = 10

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

    # loop principal da cena do jogo
    def update(self):
        if self.is_paused or self.is_game_over:
            return

        if self.is_muted:
            self.audio_player.mute_music()

        keys = pygame.key.get_pressed()
        self.character.update(keys)
        self.camera.center_on(self.character)  # Centraliza a câmera no personagem
        self.camera.update(keys)
        self.cursor.update()
        self.character.die()



        if self.character.current_health <= 0:
            # wait 3 seconds before showing game over screen
            if self.game_over_start_time is None: # Primeira vez que o jogo acaba
                self.game_over_start_time = pygame.time.get_ticks() # tick atual
            elif pygame.time.get_ticks() - self.game_over_start_time >= 1000:
                self.audio_player.stop_music()
                self.audio_player.play_sound("game_over", 0.1)
                self.is_game_over = True
                return

        # Controla o tempo para spawnar novos inimigos
        current_time = pygame.time.get_ticks() # tick atual
        num_current_enemies = len(self.enemies) # Número de inimigos atualmente no ecrã
        if current_time - self.last_spawn_time >= self.spawn_interval and num_current_enemies < self.enemies_spawned_limit: # se o ultimo spawn foi a mais de 1 segundo e o número de inimigos no ecrã for menor que 50
            self.spawn_enemy(TorchGoblin)  # Spawna um novo goblin fora da area visível
            self.last_spawn_time = current_time
        else:
            # para de spawnar inimigos
            pass

        player_position = self.character.rect.center
        for enemy in self.enemies:
            enemy.update(player_position, self.enemies, self.character)

            # Verifica se o inimigo colidiu com o personagem
            if self.character.collision_rect.colliderect(enemy.collision_rect):
                self.character.take_damage(enemy.attack)

        for item in self.camera: # Itera sobre todos os sprites na camera
            if isinstance(item, HealingItem): # se o sprite for uma healing potion
                if self.character.collision_rect.colliderect(item.rect): # se o character colidir com a poção
                    self.character.heal(item.give_health()) # cura o personagem
                    self.audio_player.play_sound("heal", 0.1)
                    item.kill() # remove a poção da câmera

        # ataque do personagem
        for enemy in self.enemies:
            if self.character.attack_rect.colliderect(enemy.collision_rect):
                enemy.take_damage(self.character.attack, self.character.rect.center)
            # Verifica se o inimigo foi derrotado
            if enemy.is_defeated:
                self.character.gain_xp(enemy.give_xp()) # Ganha XP ao derrotar inimigos
                enemy.die() # Remove o inimigo

    # Renderiza todos os elementos do jogo na cena
    def render(self):
        if self.is_game_over:
            self.game_over_screen.draw()
            self.cursor.show()
        elif self.is_paused:
            self.pause_screen.draw()
            self.pause_screen.handle_events()
        else: # Se o jogo não estiver pausado ou game over renderiza o jogo
            character_x, character_y = self.character.rect.center
            self.culling(character_x, character_y)

            # Desenha todos os sprites controlados pela câmera
            self.camera.draw()

            # Render da barra de vida do personagem
            health_bar_offset_y = 5  # Distância acima do personagem
            # Posição da barra de vida
            health_bar_position = (self.character.rect.x + 35 - self.camera.offset.x,
                               self.character.rect.y - self.camera.offset.y - health_bar_offset_y)  # Centraliza a barra de vida
            self.SCREEN.blit(self.character.health_bar.image, health_bar_position)

            # Render da barra de xp do personagem
            self.SCREEN.blit(self.character.xp_bar.image, (10, 10))
            level_label = pygame.font.Font(os.path.join('assets/fonts/DungeonFont.ttf'), 30).render(
            f"Level: {self.character.current_level}", True, (255, 255, 255))
            xp_label = pygame.font.Font(os.path.join('assets/fonts/DungeonFont.ttf'), 15).render(
            f"XP: {self.character.xp_bar.current_xp}/{self.character.xp_bar.max_xp}", True, (255, 255, 255))
            self.SCREEN.blit(level_label, (10, 30))
            self.SCREEN.blit(xp_label, (self.SCREEN_WIDTH - 73, 25))

            self.menu_manager.draw_text("Pause: ", (255, 255, 255),self.SCREEN.get_width() - self.SCREEN.get_width() * 0.96,self.SCREEN.get_height() - self.SCREEN.get_height() * 0.33, 25)
            self.SCREEN.blit(self.tutorial_pause_scale, (self.SCREEN.get_width() - self.SCREEN.get_width() * 0.93, self.SCREEN.get_height() - self.SCREEN.get_height() * 0.35))

            self.menu_manager.draw_text("Movement: ", (255, 255, 255),self.SCREEN.get_width() - self.SCREEN.get_width() * 0.93, self.SCREEN.get_height() - self.SCREEN.get_height() * 0.22,30)
            self.SCREEN.blit(self.tutorial_movement_scale, (self.SCREEN.get_width() - self.SCREEN.get_width() * 0.87, self.SCREEN.get_height() - self.SCREEN.get_height() * 0.27))

            self.menu_manager.draw_text("Attack: ", (255, 255, 255),self.SCREEN.get_width() - self.SCREEN.get_width() * 0.96,self.SCREEN.get_height() - self.SCREEN.get_height() * 0.12, 25)
            self.SCREEN.blit(self.tutorial_attack_scale, (self.SCREEN.get_width() - self.SCREEN.get_width() * 0.92, self.SCREEN.get_height() - self.SCREEN.get_height() * 0.14))

            # Desenha o cursor se ele tiver uma imagem
            if self.cursor.image:
                self.cursor.draw(self.SCREEN)

            # Coliders dos elementos do mapa
            #pygame.draw.rect(
            #    self.SCREEN,
            #    (255, 0, 0),  # Verde
            #    pygame.Rect(
            #        self.character.collision_rect.x - self.camera.offset.x,
            #        self.character.collision_rect.y - self.camera.offset.y,
            #        self.character.collision_rect.width,
            #        self.character.collision_rect.height
            #    ),
            #    2
            #)

            #pygame.draw.rect(
            #    self.SCREEN,
            #    (0, 255, 0),  # Verde
            #    pygame.Rect(
            #        self.character.attack_rect.x - self.camera.offset.x,
            #        self.character.attack_rect.y - self.camera.offset.y,
            #        self.character.attack_rect.width,
            #        self.character.attack_rect.height
            #    ),
            #    2
            #)

            #pygame.draw.rect(
            #    self.SCREEN, (0, 0, 255), # Azul
            #    pygame.Rect(
            #        self.character.rect.x - self.camera.offset.x,
            #        self.character.rect.y - self.camera.offset.y,
            #        self.character.rect.width, self.character.rect.height),
            #    2)

            #for enemy in self.enemies:
            #    pygame.draw.rect(
            #        self.SCREEN, (255, 0, 0),
            #        pygame.Rect(
            #            enemy.collision_rect.x - self.camera.offset.x,
            #            enemy.collision_rect.y - self.camera.offset.y,
            #           enemy.collision_rect.width,
            #            enemy.collision_rect.height),
            #        2)

                # pygame.draw.rect(
                #    self.SCREEN, (0, 255, 0),
                #    pygame.Rect(
                #        enemy.rect.x - self.camera.offset.x,
                #        enemy.rect.y - self.camera.offset.y,
                #        enemy.rect.width, enemy.rect.height),
                #    2)

        pygame.display.update()

    # Loop principal do jogo
    def run(self):
        self.handle_events()
        if not self.is_paused:
            self.update()
        self.render()