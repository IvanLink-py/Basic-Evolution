import pygame
import numpy as np
import numba
from consts import *

FIELD = np.zeros((FIELD_RESOLUTION[0], FIELD_RESOLUTION[1], 3), dtype=np.uint8)

AGENT_TYPES = np.zeros(AGENT_LIMIT, dtype=np.uint8)  # Типы агентов
AGENT_ENERGY = np.zeros(AGENT_LIMIT, dtype=np.int32)  # Энергия агента
AGENT_SPEED = np.zeros(AGENT_LIMIT, dtype=np.int32)  # Быстроходность агента
AGENT_TIMER = np.zeros(AGENT_LIMIT, dtype=np.int32)  # Таймер репродуктивности
AGENT_POS = np.zeros((AGENT_LIMIT, 2), dtype=np.float32)  # Положение агента
AGENT_IMPULSE = np.zeros((AGENT_LIMIT, 2), dtype=np.float32)  # Текущая скорость агента
AGENT_SENSE = np.zeros(AGENT_LIMIT, dtype=np.uint8)  # Чувствительность агента к еде


def init():
    FIELD[1, 1] = 100, 150, 200
    FIELD[2, 1] = 0, 160, 0

    spawn_agent(0, 1, 50, 1, 0, (20, 20), (0, 0), 10)
    spawn_agent(1, 2, 50, 1, 0, (60, 20), (0, 0), 10)
    spawn_agent(2, 3, 50, 1, 0, (20, 60), (0, 0), 10)


def spawn_agent(i=-1, types=None, energy=None, speed=None, timer=None, pos=None, impulse=None, sense=None):
    global AGENT_TYPES, AGENT_ENERGY, AGENT_SPEED, AGENT_TIMER, AGENT_POS, AGENT_IMPULSE, AGENT_SENSE

    if i == -1:
        for j in range(AGENT_LIMIT):
            if AGENT_TYPES[j] == 0:
                i = j
                break
            else:
                return

    AGENT_TYPES[i] = 1 if types is None else types
    AGENT_ENERGY[i] = 0 if energy is None else energy
    AGENT_SPEED[i] = (0, 0) if speed is None else speed
    AGENT_TIMER[i] = 0 if timer is None else timer
    AGENT_POS[i] = (0, 0) if pos is None else pos
    AGENT_IMPULSE[i] = (0, 0) if impulse is None else impulse
    AGENT_SENSE[i] = 0 if sense is None else sense


def pos2cell(pos):
    return 0, 0


def update():
    update_agents(AGENT_TYPES, AGENT_ENERGY, AGENT_SPEED, AGENT_TIMER, AGENT_POS, AGENT_IMPULSE, AGENT_SENSE)


def update_agents(agent_types, agent_energy, agent_speed, agent_timer, agent_pos, agent_impulse, agent_sense):
    for agent in range(AGENT_LIMIT):
        update_agent(agent, agent_types, agent_energy, agent_speed, agent_timer, agent_pos, agent_impulse, agent_sense)

    agent_pos += agent_impulse
    agent_timer += 1


def update_agent(agent, agent_types, agent_energy, agent_speed, agent_timer, agent_pos, agent_impulse, agent_sense):
    if agent_types[agent] == 0:
        return

    if agent_types[agent] == 1:
        pass
    if agent_types[agent] == 2:
        pass
    if agent_types[agent] == 3:
        pass


def duple(parent, agent_types, agent_energy, agent_speed, agent_timer, agent_pos, agent_impulse, agent_sense):
    pass


def kill(agent, agent_types):
    agent_types[agent] = 0


def render(screen):
    render_field(screen)
    render_agents(screen)
    render_ui(screen)


def render_field(screen):
    pygame.draw.rect(screen, (25, 25, 25), (FIELD_POS - (10, 10), FIELD_SIZE + (20, 20)))
    for x in range(FIELD_RESOLUTION[0]):
        for y in range(FIELD_RESOLUTION[1]):
            pygame.draw.rect(screen, FIELD[x, y],
                             (FIELD_POS + (FIELD_CELL_SIZE[0] * x, FIELD_CELL_SIZE[1] * y), FIELD_CELL_SIZE))


def render_agents(screen):
    for i in range(AGENT_LIMIT):
        render_agent(screen, i)


def render_agent(screen, agent):
    if AGENT_TYPES[agent] == 0:
        return

    if AGENT_TYPES[agent] == 1:
        pygame.draw.circle(screen, (0, 255, 0), (FIELD_POS + AGENT_POS[agent]).tolist(), AGENT_DRAW_SIZE / 2)
    elif AGENT_TYPES[agent] == 2:
        pygame.draw.polygon(screen, (255, 0, 0),
                            (FIELD_POS + AGENT_POS[agent] + (-AGENT_DRAW_SIZE / 2, AGENT_DRAW_SIZE / 3),
                             FIELD_POS + AGENT_POS[agent] + (0, -AGENT_DRAW_SIZE / 1.5),
                             FIELD_POS + AGENT_POS[agent] + (AGENT_DRAW_SIZE / 2, AGENT_DRAW_SIZE / 3)))
    elif AGENT_TYPES[agent] == 3:
        pygame.draw.rect(screen, (0, 0, 255), (
            FIELD_POS + AGENT_POS[agent] - (AGENT_DRAW_SIZE / 2, AGENT_DRAW_SIZE / 2),
            (AGENT_DRAW_SIZE, AGENT_DRAW_SIZE)))

    # pygame.draw.circle(screen, (255, 255, 255), (FIELD_POS + AGENT_POS[agent]).tolist(), 2)


def render_ui(screen):
    pass
