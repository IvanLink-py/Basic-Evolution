import numpy as np
import pygame
from consts import *
import field
import time

pygame.init()
field.init()

screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("КОМПИЛЯЦИЯ")
FONT_2 = pygame.font.SysFont('roboto', 12)

running = True
mouse_pos = np.zeros(2)
adding = False
fps_limiting = False
clock = pygame.time.Clock()

pygame.draw.rect(screen, (25, 25, 25), ((0, 0), WINDOW_SIZE))
txt = field.FONT_3.render('КОМПИЛЯЦИЯ', 1, (255, 0, 0))
screen.blit(txt, (WINDOW_SIZE[0] // 2 - txt.get_width() // 2, WINDOW_SIZE[1] // 2 - txt.get_height() // 2))
pygame.display.update()

while running:
    t1 = time.time_ns()
    screen.fill((0, 0, 0))
    field.update()
    field.render(screen)
    if adding:
        field.add_food(mouse_pos)

    screen.blit(FONT_2.render(
        f'Режим отладки ({"on" if field.DEBUG_RENDER else "off"}) - D     '
        f'FPS lock ({"on" if fps_limiting else "off"}) - F     '
        f'Отображение агентов ({"on" if field.AGENT_RENDER else "off"}) - G     '
        f'Отобразить историю - H',
        1, (255, 255, 255)),
        (20, 584))

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
            if event.key == pygame.K_f:
                fps_limiting = not fps_limiting
            if event.key == pygame.K_g:
                field.AGENT_RENDER = not field.AGENT_RENDER
            if event.key == pygame.K_h:
                field.plot_history()

    if fps_limiting:
        clock.tick(FPS_LIMIT)
    t2 = time.time_ns()
    pygame.display.set_caption(str(FRAME) + ' ' + str(round(1e9 / (t2 - t1), 2)))
    FRAME += 1

pygame.quit()
