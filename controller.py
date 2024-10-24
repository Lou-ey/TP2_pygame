import pygame
from scenes.game_scene import GameScene

pygame.init()

def main():
    game_scene = GameScene()
    while True:
        game_scene.run()
        pygame.display.update()

if __name__ == "__main__":
    main()
