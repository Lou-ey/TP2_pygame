import pygame
from pygame.time import Clock
from MainMenuController import MainMenuController

pygame.init()

#corre o jogo toudo
def main():
    menu_controller = MainMenuController()
    while True:
        menu_controller.run()
        pygame.display.update() # Atualiza a tela
        Clock().tick(60)

if __name__ == "__main__":
    main()
