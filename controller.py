import pygame

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
SCREEN = pygame.display.set_mode(SCREEN_SIZE)

while True:

    square = pygame.draw.rect(SCREEN, (255, 0, 0), (400, 300, 50, 50))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                quit()
            if event.key == pygame.K_w:
                square.y += 10
            if event.key == pygame.K_a:
                square.x -= 10
            if event.key == pygame.K_s:
                square.y -= 10
            if event.key == pygame.K_d:
                square.x += 10


    pygame.display.update()
    pygame.time.Clock().tick(60)