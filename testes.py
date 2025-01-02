import pytest
from entities.characters.Character import Character
import pygame


WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
@pytest.fixture(scope="module", autouse=True)
def init_pygame():
    pygame.init()
    pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    yield
    pygame.quit()
    #Louey biutifol

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
    assert character.level == 2

    assert character.xp == 0

