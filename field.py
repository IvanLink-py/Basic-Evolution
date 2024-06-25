import random

import pygame
import numpy as np
import numba
from consts import *

FIELD = np.zeros((FIELD_RESOLUTION[0], FIELD_RESOLUTION[1], 3), dtype=np.float32)
DRAW_FIELD = np.empty_like(FIELD)

AGENT_TYPES = -np.ones(AGENT_LIMIT, dtype=np.int8)  # Типы агентов
AGENT_ENERGY = np.zeros(AGENT_LIMIT, dtype=np.float32)  # Энергия агента
AGENT_SPEED = np.zeros(AGENT_LIMIT, dtype=np.int32)  # Быстроходность агента
AGENT_TIMER = np.zeros(AGENT_LIMIT, dtype=np.int32)  # Таймер репродуктивности
AGENT_POS = np.zeros((AGENT_LIMIT, 2), dtype=np.float32)  # Положение агента
AGENT_DIRECTION = np.zeros(AGENT_LIMIT, dtype=np.float32)  # Поворот агента в радианах
AGENT_IMPULSE = np.zeros((AGENT_LIMIT, 2), dtype=np.float32)  # Текущая скорость агента
AGENT_SENSE = np.zeros(AGENT_LIMIT, dtype=np.uint8)  # Чувствительность агента к еде

pygame.font.init()
FONT_1 = pygame.font.SysFont('arial', 10)

DEBUG_RENDER = False

def init():
    # FIELD[10:12, :, 0] = 50
    # FIELD[14:16, :, 1] = 50
    # FIELD[18:20, :, 2] = 50
    FIELD[:, :, :] = 50

    # spawn_agent(0, 0, 50, 1, 0, (20, 20), 0, (1, 1), 10)
    # spawn_agent(1, 1, 50, 1, 0, (60, 20), 0, (0.01, 0), 10)

    for i in range(10):
        spawn_agent(types=0, energy=50, speed=1, timer=random.randint(0, AGENT_DUPLE_TIMER[0]),
                    pos=(random.random() * FIELD_SIZE[0], random.random() * FIELD_SIZE[1]),
                    direction=random.random() * np.pi * 2,
                    impulse=(0, 0), sense=1)

    for i in range(10):
        spawn_agent(types=1, energy=50, speed=1, timer=random.randint(0, AGENT_DUPLE_TIMER[1]),
                    pos=(random.random() * FIELD_SIZE[0], random.random() * FIELD_SIZE[1]),
                    direction=random.random() * np.pi * 2,
                    impulse=(0, 0), sense=1)

    for i in range(10):
        spawn_agent(types=2, energy=50, speed=1, timer=random.randint(0, AGENT_DUPLE_TIMER[2]),
                    pos=(random.random() * FIELD_SIZE[0], random.random() * FIELD_SIZE[1]),
                    direction=random.random() * np.pi * 2,
                    impulse=(0, 0), sense=1)


def spawn_agent(i=-1, types=None, energy=None, speed=None, timer=None, pos=None, direction=None, impulse=None,
                sense=None):
    global AGENT_TYPES, AGENT_ENERGY, AGENT_SPEED, AGENT_TIMER, AGENT_POS, AGENT_DIRECTION, AGENT_IMPULSE, AGENT_SENSE

    if i == -1:
        for j in range(AGENT_LIMIT):
            if AGENT_TYPES[j] == -1:
                i = j
                break
        else:
            return

    AGENT_TYPES[i] = 1 if types is None else types
    AGENT_ENERGY[i] = 0 if energy is None else energy
    AGENT_SPEED[i] = 1 if speed is None else speed
    AGENT_TIMER[i] = 0 if timer is None else timer
    AGENT_POS[i] = (0, 0) if pos is None else pos
    AGENT_DIRECTION[i] = 0 if direction is None else direction
    AGENT_IMPULSE[i] = (0, 0) if impulse is None else impulse
    AGENT_SENSE[i] = 1 if sense is None else sense


@numba.njit()
def pos2cell(field, pos, field_cell_size, field_resolution):
    x = round((pos[0] // field_cell_size[0] + field_resolution[0]) % field_resolution[0])
    y = round((pos[1] // field_cell_size[1] + field_resolution[1]) % field_resolution[1])

    return field[x, y]


def add_food(pos):
    x = round(((pos[0] - FIELD_POS[0]) // FIELD_CELL_SIZE[0] + FIELD_RESOLUTION[0]) % FIELD_RESOLUTION[0])
    y = round(((pos[1] - FIELD_POS[1]) // FIELD_CELL_SIZE[1] + FIELD_RESOLUTION[1]) % FIELD_RESOLUTION[1])

    FIELD[x, y] += 5


def update():
    update_agents(AGENT_TYPES, AGENT_ENERGY, AGENT_SPEED, AGENT_TIMER, AGENT_POS, AGENT_DIRECTION, AGENT_IMPULSE,
                  AGENT_SENSE, FIELD, AGENT_LIMIT, AGENT_SPEED_MODIFIER, FIELD_CELL_SIZE, AGENT_SENSE_RADIUS,
                  AGENT_SENSE_MODIFIER, FIELD_RESOLUTION, AGENT_MAX_ENERGY,
                  AGENT_CONSUMING, AGENT_LIFE_COST, AGENT_DUPLE_TIMER, AGENT_DUPLE_COST, AGENT_PRODUCING)


@numba.njit()
def update_agents(agent_types, agent_energy, agent_speed, agent_timer,
                  agent_pos, agent_direction, agent_impulse, agent_sense, field, agent_limit, agent_speed_modifier,
                  field_cell_size, agent_sense_radius, agent_sense_modifier, field_resolution, agent_max_energy,
                  agent_consuming, agent_life_cost, agent_duple_timer, agent_duple_cost, agent_producing):
    for agent in range(agent_limit):
        update_agent(agent, agent_types, agent_energy, agent_speed, agent_timer,
                     agent_pos, agent_direction, agent_impulse, agent_sense, field, agent_limit, agent_speed_modifier,
                     field_cell_size, agent_sense_radius, agent_sense_modifier, field_resolution, agent_max_energy,
                     agent_consuming, agent_life_cost, agent_duple_timer, agent_duple_cost, agent_producing)

    agent_pos += agent_impulse
    agent_impulse *= FIELD_FRICTION
    agent_pos %= FIELD_SIZE
    agent_direction += (np.random.random(AGENT_LIMIT) - 0.5) * AGENT_RANDOM_ROTATION
    agent_timer += 1


@numba.njit()
def update_agent(agent, agent_types, agent_energy, agent_speed, agent_timer,
                 agent_pos, agent_direction, agent_impulse, agent_sense, field, agent_limit, agent_speed_modifier,
                 field_cell_size, agent_sense_radius, agent_sense_modifier, field_resolution, agent_max_energy,
                 agent_consuming, agent_life_cost, agent_duple_timer, agent_duple_cost, agent_producing):
    if agent_types[agent] == -1:
        return

    food_index = int(2 - agent_types[agent])
    cal_index = (food_index + 2) % 3
    type_index = int(agent_types[agent])

    food_in_cell = pos2cell(field, agent_pos[agent], field_cell_size, field_resolution)[food_index]
    if agent_energy[agent] < agent_max_energy[type_index] and food_in_cell > agent_consuming[type_index]:
        pos2cell(field, agent_pos[agent], field_cell_size, field_resolution)[food_index] -= agent_consuming[type_index]
        agent_energy[agent] += agent_consuming[type_index]

    if agent_energy[agent] < agent_life_cost[type_index]:
        kill(agent, agent_types)
        return
    #
    if agent_timer[agent] > agent_duple_timer[type_index]:
        if agent_energy[agent] > agent_duple_cost[type_index]:
            duple(agent, agent_types, agent_energy, agent_speed, agent_timer,
                  agent_pos, agent_direction, agent_impulse, agent_sense, agent_limit)
        agent_timer[agent] = 0

    agent_impulse[agent][0] += np.cos(agent_direction[agent]) * agent_speed[agent] * agent_speed_modifier[type_index]
    agent_impulse[agent][1] += -np.sin(agent_direction[agent]) * agent_speed[agent] * agent_speed_modifier[type_index]

    sense(agent, agent_pos, agent_direction, agent_impulse, agent_sense, field, agent_sense_modifier, field_cell_size,
          field_resolution, food_index)

    agent_energy[agent] -= agent_life_cost[type_index]
    pos2cell(field, agent_pos[agent], field_cell_size, field_resolution)[cal_index] += agent_producing[type_index]


@numba.njit()
def sense(agent, agent_pos, agent_direction, agent_impulse, agent_sense, field, agent_sense_modifier, field_cell_size,
          field_resolution, food_index):
    x = round((agent_pos[agent][0] // field_cell_size[0] + field_resolution[0]) % field_resolution[0])
    y = round((agent_pos[agent][1] // field_cell_size[1] + field_resolution[1]) % field_resolution[1])

    angle = int(np.floor((agent_direction[agent] + np.pi * (1 / 16)) / (np.pi * 2) * 8) % 8)

    neibors = (
        ((x + 1) % field_resolution[0], (y) % field_resolution[1]),
        ((x + 1) % field_resolution[0], (y - 1) % field_resolution[1]),
        ((x) % field_resolution[0], (y - 1) % field_resolution[1]),
        ((x - 1) % field_resolution[0], (y - 1) % field_resolution[1]),
        ((x - 1) % field_resolution[0], (y) % field_resolution[1]),
        ((x - 1) % field_resolution[0], (y + 1) % field_resolution[1]),
        ((x) % field_resolution[0], (y + 1) % field_resolution[1]),
        ((x + 1) % field_resolution[0], (y + 1) % field_resolution[1]))

    front_score = (field[neibors[(angle + 0) % 8][0], neibors[(angle + 0) % 8][1], food_index] +
                   field[neibors[(angle + 1) % 8][0], neibors[(angle + 1) % 8][1], food_index] +
                   field[neibors[(angle - 1) % 8][0], neibors[(angle - 1) % 8][1], food_index])

    back_score = (field[neibors[(angle + 4) % 8][0], neibors[(angle + 4) % 8][1], food_index] +
                  field[neibors[(angle + 5) % 8][0], neibors[(angle + 5) % 8][1], food_index] +
                  field[neibors[(angle + 3) % 8][0], neibors[(angle + 3) % 8][1], food_index])

    left_score = (field[neibors[(angle + 1) % 8][0], neibors[(angle + 1) % 8][1], food_index] +
                  field[neibors[(angle + 2) % 8][0], neibors[(angle + 2) % 8][1], food_index] +
                  field[neibors[(angle + 3) % 8][0], neibors[(angle + 3) % 8][1], food_index])

    right_score = (field[neibors[(angle + 5) % 8][0], neibors[(angle + 5) % 8][1], food_index] +
                   field[neibors[(angle + 6) % 8][0], neibors[(angle + 6) % 8][1], food_index] +
                   field[neibors[(angle + 7) % 8][0], neibors[(angle + 7) % 8][1], food_index])

    if front_score >= back_score:
        dir_mod = np.float32(0.2)
    else:
        dir_mod = np.float32(1)

    if left_score > right_score:
        agent_direction[agent] += agent_sense_modifier * agent_sense[agent] * dir_mod

    elif left_score < right_score:
        agent_direction[agent] -= agent_sense_modifier * agent_sense[agent] * dir_mod


@numba.njit()
def duple(parent, agent_types, agent_energy, agent_speed, agent_timer,
          agent_pos, agent_direction, agent_impulse, agent_sense, agent_limit):
    for i in range(agent_limit):
        if agent_types[i] == -1:
            agent_energy[parent] /= 2

            agent_types[i] = agent_types[parent]
            agent_energy[i] = agent_energy[parent]
            agent_speed[i] = agent_speed[parent]
            agent_timer[i] = 0
            agent_pos[i] = agent_pos[parent]
            agent_direction[i] = agent_direction[parent]
            agent_impulse[i] = agent_impulse[parent]
            agent_sense[i] = agent_sense[parent]
            return


@numba.njit()
def kill(agent, agent_types):
    agent_types[agent] = -1


def render(screen):
    render_field(screen)
    render_agents(screen)
    render_ui(screen)


def draw_field(draw_field):
    draw_field[:] = FIELD
    f_max = max(200, FIELD.max())
    draw_field *= 255 / f_max


def render_field(screen):
    draw_field(DRAW_FIELD)
    pygame.draw.rect(screen, (25, 25, 25), (FIELD_POS - (10, 10), FIELD_SIZE + (20, 20)))
    for x in range(FIELD_RESOLUTION[0]):
        for y in range(FIELD_RESOLUTION[1]):
            pygame.draw.rect(screen, DRAW_FIELD[x, y],
                             (FIELD_POS + (FIELD_CELL_SIZE[0] * x, FIELD_CELL_SIZE[1] * y), FIELD_CELL_SIZE))


def render_agents(screen):
    for i in range(AGENT_LIMIT):
        render_agent(screen, i)


def render_agent(screen, agent):
    if AGENT_TYPES[agent] == -1:
        return

    if AGENT_TYPES[agent] == 0:
        pygame.draw.circle(screen, (0, 255, 0), (FIELD_POS + AGENT_POS[agent]).tolist(), AGENT_DRAW_SIZE / 2)
    elif AGENT_TYPES[agent] == 1:
        pygame.draw.polygon(screen, (255, 0, 0),
                            (FIELD_POS + AGENT_POS[agent] + (-AGENT_DRAW_SIZE / 2, AGENT_DRAW_SIZE / 3),
                             FIELD_POS + AGENT_POS[agent] + (0, -AGENT_DRAW_SIZE / 1.5),
                             FIELD_POS + AGENT_POS[agent] + (AGENT_DRAW_SIZE / 2, AGENT_DRAW_SIZE / 3)))
    elif AGENT_TYPES[agent] == 2:
        pygame.draw.rect(screen, (0, 0, 255), (
            FIELD_POS + AGENT_POS[agent] - (AGENT_DRAW_SIZE / 2, AGENT_DRAW_SIZE / 2),
            (AGENT_DRAW_SIZE, AGENT_DRAW_SIZE)))
    if DEBUG_RENDER:
        energy_txt = FONT_1.render(str(round(AGENT_ENERGY[agent])), 1, (255, 255, 255))
        screen.blit(energy_txt, (FIELD_POS + AGENT_POS[agent]).tolist())
        pygame.draw.line(screen, (255, 255, 255), (FIELD_POS + AGENT_POS[agent]).tolist(), (FIELD_POS + AGENT_POS[agent] + (
            np.cos(AGENT_DIRECTION[agent]) * DISPLAY_DIRECTION_LENGHT,
            -np.sin(AGENT_DIRECTION[agent]) * DISPLAY_DIRECTION_LENGHT)).tolist())

        FIELD_POS + AGENT_POS + (np.cos(AGENT_DIRECTION[agent]) * FIELD_CELL_SIZE[0],np.sin(AGENT_DIRECTION[agent]) * FIELD_CELL_SIZE[1])


def render_ui(screen):
    pass
