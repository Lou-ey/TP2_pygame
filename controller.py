import pygame
from scenes.game_scene import GameScene

pygame.init()

def main():
    game_scene = GameScene() # Instancia a cena do jogo
    run = True
    while run:
        game_scene.run() # Roda o jogo
        pygame.display.update() # Atualiza a tela

if __name__ == "__main__":
    main()
