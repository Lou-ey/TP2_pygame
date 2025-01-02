import pytest
from entities.characters.Character import Character
from entities.enemies.Enemy import Enemy
from utils.CameraGroup import CameraGroup
import pygame

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

@pytest.fixture(scope="module", autouse=True)
def init_pygame():
    pygame.init()
    pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    yield
    pygame.quit()

# Teste de morte
def test_character_death():
    character = Character("TestPlayer", 1, 10, 25, 5, 2, 100, 100, 170, 170, 50, 1)

    character.take_damage(110)

    assert character.current_health <= 0
    assert character.is_dead

#teste subir de nível
def test_character_level_up():
    character = Character("TestPlayer", 100, 100, 5, 2, 1, 0, 100, 170, 170,50, 1)

    assert character.level == 1
    character.gain_xp(100)
    character.level_up()
    assert character.current_level == 2

    #assert character.xp == 0

def test_character_heal():
    character = Character("TestPlayer", 100, 100, 5, 2, 1, 0, 100, 170, 170,50, 1)

    character.take_damage(50)

    assert character.current_health == 50

    character.heal(50)

    assert character.current_health == 100

def test_character_take_damage():
    character = Character("TestPlayer", 100, 100, 5, 2, 1, 0, 100, 170, 170,50, 1)

    character.take_damage(50)

    assert character.current_health == 50

def test_enemy_move_towards_player():
    enemy = Enemy("TestEnemy", 100, 10, 5, 2, 100, 100, 100)

    enemy.rect = pygame.Rect(0, 0, 100, 100)

    enemy.move_towards_player((100, 100))

    assert enemy.rect.x != 0
    assert enemy.rect.y != 0

def test_playing_audio():
    enemy = Enemy("TestEnemy", 100, 10, 5, 2, 100, 100, 100)

    enemy.audio_player.load_sounds()

    assert enemy.audio_player.sounds is not None




