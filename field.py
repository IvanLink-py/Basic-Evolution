import random
import plot
import pygame
import numpy as np
import numba
from consts import *

FIELD = np.zeros((FIELD_RESOLUTION[0], FIELD_RESOLUTION[1], 3), dtype=np.float32)
DRAW_FIELD = np.empty_like(FIELD)

AGENT_TYPES = -np.ones(AGENT_LIMIT, dtype=np.int8)  # Типы агентов
AGENT_ENERGY = np.zeros(AGENT_LIMIT, dtype=np.float32)  # Энергия агента
AGENT_SPEED = np.zeros(AGENT_LIMIT, dtype=np.float32)  # Быстроходность агента
AGENT_TIMER = np.zeros(AGENT_LIMIT, dtype=np.int32)  # Таймер репродуктивности
AGENT_POS = np.zeros((AGENT_LIMIT, 2), dtype=np.float32)  # Положение агента
AGENT_DIRECTION = np.zeros(AGENT_LIMIT, dtype=np.float32)  # Поворот агента в радианах
AGENT_IMPULSE = np.zeros((AGENT_LIMIT, 2), dtype=np.float32)  # Текущая скорость агента
AGENT_SENSE = np.zeros(AGENT_LIMIT, dtype=np.float32)  # Чувствительность агента к еде
AGENT_DUPLE_DISTANCE = np.zeros(AGENT_LIMIT, dtype=np.float32)  # Растояние от родителя на котором появиться клон

HISTORY_AGENT_COUNT = np.zeros((HISTORY_CHUNK_SIZE, 3), dtype=np.int32)
HISTORY_FIELD_ENERGY = np.zeros((HISTORY_CHUNK_SIZE, 3), dtype=np.float32)
HISTORY_AGENT_ENERGY = np.zeros((HISTORY_CHUNK_SIZE, 3), dtype=np.float32)
HISTORY_AGENT_SPEED = np.zeros((HISTORY_CHUNK_SIZE, 3), dtype=np.float32)
HISTORY_AGENT_SENSE = np.zeros((HISTORY_CHUNK_SIZE, 3), dtype=np.float32)
HISTORY_AGENT_DUPLE_DISTANCE = np.zeros((HISTORY_CHUNK_SIZE, 3), dtype=np.float32)

pygame.font.init()
FONT_1 = pygame.font.SysFont('arial', 10)
FONT_3 = pygame.font.SysFont('roboto', 22)

DEBUG_RENDER = False
AGENT_RENDER = False


def init():
    # FIELD[0:4, :, 0] = 100
    # FIELD[6:10, :, 1] = 50
    # FIELD[10:14, :, 2] = 25
    FIELD[:, :, :] = 10

    # spawn_agent(0, 0, 50, 1, 0, (20, 20), 0, (1, 1), 10)
    # spawn_agent(1, 1, 50, 1, 0, (60, 20), 0, (0.01, 0), 10)

    for i in range(100):
        spawn_agent(types=0, energy=50, speed=0.0, timer=random.randint(0, AGENT_DUPLE_TIMER[0]),
                    pos=(random.random() * FIELD_SIZE[0], random.random() * FIELD_SIZE[1]),
                    direction=random.random() * np.pi * 2,
                    impulse=(0, 0), sense=0, duple_distance=4)

    for i in range(100):
        spawn_agent(types=1, energy=50, speed=0.5, timer=random.randint(0, AGENT_DUPLE_TIMER[1]),
                    pos=(random.random() * FIELD_SIZE[0], random.random() * FIELD_SIZE[1]),
                    direction=random.random() * np.pi * 2,
                    impulse=(0, 0), sense=0, duple_distance=0)

    for i in range(100):
        spawn_agent(types=2, energy=50, speed=0.5, timer=random.randint(0, AGENT_DUPLE_TIMER[2]),
                    pos=(random.random() * FIELD_SIZE[0], random.random() * FIELD_SIZE[1]),
                    direction=random.random() * np.pi * 2,
                    impulse=(0, 0), sense=0, duple_distance=0)


def spawn_agent(i=-1, types=None, energy=None, speed=None, timer=None, pos=None, direction=None, impulse=None,
                sense=None, duple_distance=None):
    global AGENT_TYPES, AGENT_ENERGY, AGENT_SPEED, AGENT_TIMER, AGENT_POS, AGENT_DIRECTION, AGENT_IMPULSE, AGENT_SENSE, AGENT_DUPLE_DISTANCE

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
    AGENT_DUPLE_DISTANCE[i] = 0 if duple_distance is None else duple_distance
    AGENT_IMPULSE[i] = (0, 0) if impulse is None else impulse
    AGENT_SENSE[i] = 1 if sense is None else sense


@numba.njit()
def pos2cell(field, pos):
    x = round((pos[0] // FIELD_CELL_SIZE[0] + FIELD_RESOLUTION[0]) % FIELD_RESOLUTION[0])
    y = round((pos[1] // FIELD_CELL_SIZE[1] + FIELD_RESOLUTION[1]) % FIELD_RESOLUTION[1])

    return field[x, y]


@numba.njit()
def pos2cell_coord(pos):
    x = round((pos[0] // FIELD_CELL_SIZE[0] + FIELD_RESOLUTION[0]) % FIELD_RESOLUTION[0])
    y = round((pos[1] // FIELD_CELL_SIZE[1] + FIELD_RESOLUTION[1]) % FIELD_RESOLUTION[1])

    return x, y


@numba.njit()
def get_light_level(pos):
    # if (pos[1] % 32) > 16:
    #     return 0
    # else:
    #     return 2

    # if ((pos[0] // 4) % 2 + (pos[1] // 4) % 2) % 2 == 0:
    #     return 1.65
    # else:
    #     return 0.65

    # return max(0, (32 - pos[1]) / 16)

    return 1


def add_food(pos):
    x = round(((pos[0] - FIELD_POS[0]) // FIELD_CELL_SIZE[0] + FIELD_RESOLUTION[0]) % FIELD_RESOLUTION[0])
    y = round(((pos[1] - FIELD_POS[1]) // FIELD_CELL_SIZE[1] + FIELD_RESOLUTION[1]) % FIELD_RESOLUTION[1])

    FIELD[x - 3:x + 3, y - 3:y + 3] += 5


def update():
    global FRAME
    update_agents(AGENT_TYPES, AGENT_ENERGY, AGENT_SPEED, AGENT_TIMER, AGENT_POS, AGENT_DIRECTION, AGENT_IMPULSE,
                  AGENT_SENSE, FIELD, AGENT_DUPLE_DISTANCE)

    if FRAME % HISTORY_CHUNK_SIZE == HISTORY_CHUNK_SIZE - 1:
        HISTORY_AGENT_COUNT.resize((HISTORY_AGENT_COUNT.shape[0] + HISTORY_CHUNK_SIZE, 3), refcheck=False)
        HISTORY_FIELD_ENERGY.resize((HISTORY_FIELD_ENERGY.shape[0] + HISTORY_CHUNK_SIZE, 3), refcheck=False)
        HISTORY_AGENT_ENERGY.resize((HISTORY_AGENT_ENERGY.shape[0] + HISTORY_CHUNK_SIZE, 3), refcheck=False)
        HISTORY_AGENT_SPEED.resize((HISTORY_AGENT_SPEED.shape[0] + HISTORY_CHUNK_SIZE, 3), refcheck=False)
        HISTORY_AGENT_SENSE.resize((HISTORY_AGENT_SENSE.shape[0] + HISTORY_CHUNK_SIZE, 3), refcheck=False)
        HISTORY_AGENT_DUPLE_DISTANCE.resize((HISTORY_AGENT_DUPLE_DISTANCE.shape[0] + HISTORY_CHUNK_SIZE, 3),
                                            refcheck=False)

    collect_history(FRAME, FIELD, HISTORY_CHUNK_SIZE, HISTORY_AGENT_COUNT, AGENT_TYPES, AGENT_ENERGY, AGENT_LIMIT,
                    HISTORY_FIELD_ENERGY, HISTORY_AGENT_ENERGY, HISTORY_AGENT_SPEED, HISTORY_AGENT_SENSE, AGENT_SENSE,
                    AGENT_SPEED, HISTORY_AGENT_DUPLE_DISTANCE, AGENT_DUPLE_DISTANCE)
    HISTORY_FIELD_ENERGY[FRAME] = FIELD.sum((0, 1))

    FRAME += 1


@numba.njit()
def collect_history(frame, field, history_chunk_size, history_agent_count, agent_types, agent_energy, agent_limit,
                    history_field_energy, history_agent_energy, history_agent_speed, history_agent_sense, agent_sense,
                    agent_speed, history_duple_distance, agent_duple_distance):
    for agent in range(agent_limit):
        if agent_types[agent] == 0:
            history_agent_count[frame, 0] += 1
            history_agent_energy[frame, 0] += agent_energy[agent]
            history_agent_speed[frame, 0] += agent_speed[agent]
            history_agent_sense[frame, 0] += agent_sense[agent]
            history_duple_distance[frame, 0] += agent_duple_distance[agent]
        elif agent_types[agent] == 1:
            history_agent_count[frame, 1] += 1
            history_agent_energy[frame, 1] += agent_energy[agent]
            history_agent_speed[frame, 1] += agent_speed[agent]
            history_agent_sense[frame, 1] += agent_sense[agent]
            history_duple_distance[frame, 1] += agent_duple_distance[agent]
        elif agent_types[agent] == 2:
            history_agent_count[frame, 2] += 1
            history_agent_energy[frame, 2] += agent_energy[agent]
            history_agent_speed[frame, 2] += agent_speed[agent]
            history_agent_sense[frame, 2] += agent_sense[agent]
            history_duple_distance[frame, 2] += agent_duple_distance[agent]


@numba.njit()
def update_agents(agent_types, agent_energy, agent_speed, agent_timer,
                  agent_pos, agent_direction, agent_impulse, agent_sense, field, agent_duple_distance):
    for agent in range(AGENT_LIMIT):
        update_agent(agent, agent_types, agent_energy, agent_speed, agent_timer,
                     agent_pos, agent_direction, agent_impulse, agent_sense, field, agent_duple_distance)

    agent_pos += agent_impulse
    agent_impulse *= FIELD_FRICTION
    agent_pos %= FIELD_SIZE
    agent_direction += (np.random.random(AGENT_LIMIT) - 0.5) * AGENT_RANDOM_ROTATION
    agent_timer += 1

    field += FIELD_REGEN


@numba.njit()
def update_agent(agent, agent_types, agent_energy, agent_speed, agent_timer,
                 agent_pos, agent_direction, agent_impulse, agent_sense, field, agent_duple_distance):
    if agent_types[agent] == -1:
        return

    food_index = int(2 - agent_types[agent])
    cal_index = (food_index + 2) % 3
    type_index = int(agent_types[agent])

    if food_index == 2:
        pos = pos2cell_coord(agent_pos[agent])
        light = get_light_level(pos)
        food_in_cell = pos2cell(field, agent_pos[agent])[food_index]

        if agent_energy[agent] < AGENT_MAX_ENERGY[type_index]:
            eated = min(AGENT_CONSUMING[type_index], food_in_cell)
            pos2cell(field, agent_pos[agent])[food_index] -= eated
            agent_energy[agent] += eated * light
    else:
        food_in_cell = pos2cell(field, agent_pos[agent])[food_index]
        if agent_energy[agent] < AGENT_MAX_ENERGY[type_index]:
            eated = min(AGENT_CONSUMING[type_index], food_in_cell)
            pos2cell(field, agent_pos[agent])[food_index] -= eated
            agent_energy[agent] += eated

    if agent_energy[agent] < AGENT_LIFE_COST[type_index]:
        kill(agent, agent_types, field, agent_energy, agent_pos, cal_index, type_index)
        return

    if agent_timer[agent] > AGENT_LIFE_TIME[type_index]:
        kill(agent, agent_types, field, agent_energy, agent_pos, cal_index, type_index)
        return

    if agent_timer[agent] % AGENT_DUPLE_TIMER[type_index] == AGENT_DUPLE_TIMER[type_index] - 1:
        if agent_energy[agent] > AGENT_DUPLE_COST[type_index]:
            duple(agent, agent_types, agent_energy, agent_speed, agent_timer,
                  agent_pos, agent_direction, agent_impulse, agent_sense, agent_duple_distance)

    agent_impulse[agent][0] += np.cos(agent_direction[agent]) * agent_speed[agent] * AGENT_SPEED_MODIFIER[type_index]
    agent_impulse[agent][1] += -np.sin(agent_direction[agent]) * agent_speed[agent] * AGENT_SPEED_MODIFIER[type_index]

    sense(agent, agent_pos, agent_direction, agent_sense, field, food_index)

    life_cost = (AGENT_LIFE_COST[type_index] +
                 AGENT_LIFE_COST_PER_SPEED[type_index] * agent_speed[agent] +
                 AGENT_LIFE_COST_PER_SENSE[type_index] * agent_sense[agent])

    agent_energy[agent] -= life_cost
    pos2cell(field, agent_pos[agent])[cal_index] += life_cost * AGENT_PRODUCING[type_index]


@numba.njit()
def sense(agent, agent_pos, agent_direction, agent_sense, field, food_index):
    x = round((agent_pos[agent][0] // FIELD_CELL_SIZE[0] + FIELD_RESOLUTION[0]) % FIELD_RESOLUTION[0])
    y = round((agent_pos[agent][1] // FIELD_CELL_SIZE[1] + FIELD_RESOLUTION[1]) % FIELD_RESOLUTION[1])

    angle = int(np.floor((agent_direction[agent] + np.pi * (1 / 16)) / (np.pi * 2) * 8) % 8)

    if food_index == 2:
        neibors = (
            field[(x + 1) % FIELD_RESOLUTION[0],
                  (y) % FIELD_RESOLUTION[1], food_index] * get_light_level((x + 1, y)),
            field[(x + 1) % FIELD_RESOLUTION[0],
                  (y - 1) % FIELD_RESOLUTION[1], food_index] * get_light_level((x + 1, y - 1)),
            field[(x) % FIELD_RESOLUTION[0],
                  (y - 1) % FIELD_RESOLUTION[1], food_index] * get_light_level((x, y - 1)),
            field[(x - 1) % FIELD_RESOLUTION[0],
                  (y - 1) % FIELD_RESOLUTION[1], food_index] * get_light_level((x - 1, y - 1)),
            field[(x - 1) % FIELD_RESOLUTION[0],
                  (y) % FIELD_RESOLUTION[1], food_index] * get_light_level((x - 1, y)),
            field[(x - 1) % FIELD_RESOLUTION[0],
                  (y + 1) % FIELD_RESOLUTION[1], food_index] * get_light_level((x - 1, y + 1)),
            field[(x) % FIELD_RESOLUTION[0],
                  (y + 1) % FIELD_RESOLUTION[1], food_index] * get_light_level((x, y + 1)),
            field[(x + 1) % FIELD_RESOLUTION[0],
                  (y + 1) % FIELD_RESOLUTION[1], food_index] * get_light_level((x + 1, y + 1)))
    else:
        neibors = (
            field[(x + 1) % FIELD_RESOLUTION[0], (y) % FIELD_RESOLUTION[1], food_index],
            field[(x + 1) % FIELD_RESOLUTION[0], (y - 1) % FIELD_RESOLUTION[1], food_index],
            field[(x) % FIELD_RESOLUTION[0], (y - 1) % FIELD_RESOLUTION[1], food_index],
            field[(x - 1) % FIELD_RESOLUTION[0], (y - 1) % FIELD_RESOLUTION[1], food_index],
            field[(x - 1) % FIELD_RESOLUTION[0], (y) % FIELD_RESOLUTION[1], food_index],
            field[(x - 1) % FIELD_RESOLUTION[0], (y + 1) % FIELD_RESOLUTION[1], food_index],
            field[(x) % FIELD_RESOLUTION[0], (y + 1) % FIELD_RESOLUTION[1], food_index],
            field[(x + 1) % FIELD_RESOLUTION[0], (y + 1) % FIELD_RESOLUTION[1], food_index])

    front_score = (neibors[(angle + 0) % 8] +
                   neibors[(angle + 1) % 8] +
                   neibors[(angle - 1) % 8])

    back_score = (neibors[(angle + 4) % 8] +
                  neibors[(angle + 5) % 8] +
                  neibors[(angle + 3) % 8])

    left_score = (neibors[(angle + 1) % 8] +
                  neibors[(angle + 2) % 8] +
                  neibors[(angle + 3) % 8])

    right_score = (neibors[(angle + 5) % 8] +
                   neibors[(angle + 6) % 8] +
                   neibors[(angle + 7) % 8])

    if front_score >= back_score:
        dir_mod = np.float32(0.2)
    else:
        dir_mod = np.float32(1)

    if left_score > right_score:
        agent_direction[agent] += AGENT_SENSE_MODIFIER * agent_sense[agent] * dir_mod

    elif left_score < right_score:
        agent_direction[agent] -= AGENT_SENSE_MODIFIER * agent_sense[agent] * dir_mod


@numba.njit()
def duple(parent, agent_types, agent_energy, agent_speed, agent_timer,
          agent_pos, agent_direction, agent_impulse, agent_sense, agent_duple_distance):
    for i in range(AGENT_LIMIT):
        if agent_types[i] == -1:
            agent_energy[parent] /= 2

            agent_types[i] = agent_types[parent]
            agent_energy[i] = agent_energy[parent]
            agent_speed[i] = max(0, agent_speed[parent] + (random.random() - 0.5) * AGENT_MUTATION)
            agent_timer[i] = 0
            agent_pos[i] = agent_pos[parent] + np.array(
                [np.cos(agent_direction[parent]), -np.sin(agent_direction[parent])]) * agent_duple_distance[parent]
            agent_direction[i] = agent_direction[parent]
            agent_impulse[i] = agent_impulse[parent]
            agent_sense[i] = max(0, agent_sense[parent] + (random.random() - 0.5) * AGENT_MUTATION)
            agent_duple_distance[i] = max(0, agent_duple_distance[parent] + (
                        random.random() - 0.5) * AGENT_DUPLE_DISTANCE_MUTATION)
            return


@numba.njit()
def kill(agent, agent_types, field, agent_energy, agent_pos, cal_index, type_index):
    agent_types[agent] = -1
    pos2cell(field, agent_pos[agent])[cal_index] += agent_energy[agent] * AGENT_PRODUCING[type_index]


def render(screen):
    render_field(screen)
    if AGENT_RENDER:
        render_agents(screen)
    render_ui(screen)


def draw_field(draw_field):
    draw_field[:] = FIELD
    f_max = max(50, FIELD.max())
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
        pygame.draw.line(screen, (255, 255, 255), (FIELD_POS + AGENT_POS[agent]).tolist(),
                         (FIELD_POS + AGENT_POS[agent] + (
                             np.cos(AGENT_DIRECTION[agent]) * DISPLAY_DIRECTION_LENGHT,
                             -np.sin(AGENT_DIRECTION[agent]) * DISPLAY_DIRECTION_LENGHT)).tolist())

        FIELD_POS + AGENT_POS + (
            np.cos(AGENT_DIRECTION[agent]) * FIELD_CELL_SIZE[0], np.sin(AGENT_DIRECTION[agent]) * FIELD_CELL_SIZE[1])


def render_ui(screen):
    if HISTORY_AGENT_COUNT[FRAME - 1].sum() == 0:
        pygame.draw.rect(screen, (25, 25, 25), (FIELD_POS, FIELD_SIZE))
        txt = FONT_3.render('NO LIFE', 1, (255, 0, 0))
        screen.blit(txt, (WINDOW_SIZE[0] // 2 - txt.get_width() // 2, WINDOW_SIZE[1] // 2 - txt.get_height() // 2))


def plot_history():
    plot.draw(FRAME, HISTORY_AGENT_COUNT, HISTORY_FIELD_ENERGY, HISTORY_AGENT_ENERGY, HISTORY_AGENT_SPEED,
              HISTORY_AGENT_SENSE, HISTORY_AGENT_DUPLE_DISTANCE)
