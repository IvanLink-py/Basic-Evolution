import pygame
from consts import *
import field

pygame.init()
field.init()

screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("My Game")
running = True

while running:

    screen.fill((0, 0, 0))
    field.update()
    field.render(screen)

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
