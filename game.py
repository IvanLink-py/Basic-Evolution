import numpy as np
import pygame
from consts import *
import field

pygame.init()
field.init()

screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("My Game")
running = True
mouse_pos = np.zeros(2)

while running:

    screen.fill((0, 0, 0))
    field.add_food(mouse_pos)
    field.update()
    field.render(screen)

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEMOTION:
            mouse_pos[0] = event.pos[0]
            mouse_pos[1] = event.pos[1]


pygame.quit()
