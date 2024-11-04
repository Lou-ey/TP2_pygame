import pygame
from pygame.time import Clock
from scenes.game_scene import GameScene

pygame.init()



def main():
    game_scene = GameScene() # Instancia a cena do jogo
    while True:
        game_scene.run() # Roda o jogo
        pygame.display.update() # Atualiza a tela
        Clock().tick(60)

if __name__ == "__main__":
    main()
