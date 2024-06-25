import numpy as np
import pygame
from consts import *
import field
import time

pygame.init()
field.init()

screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("My Game")
running = True
mouse_pos = np.zeros(2)
adding = False
clock = pygame.time.Clock()

while running:
    t1 = time.time()
    screen.fill((0, 0, 0))
    field.update()
    field.render(screen)
    if adding:
        field.add_food(mouse_pos)
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEMOTION:
            mouse_pos[0] = event.pos[0]
            mouse_pos[1] = event.pos[1]
        elif event.type == pygame.MOUSEBUTTONDOWN:
            adding = True
        elif event.type == pygame.MOUSEBUTTONUP:
            adding = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                field.DEBUG_RENDER = not field.DEBUG_RENDER

    clock.tick(FPS_LIMIT)
    t2 = time.time()
    pygame.display.set_caption(str(round(1/(t2 - t1))))
    FRAME += 1

pygame.quit()
