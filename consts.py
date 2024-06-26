import numpy as np


# Системные натройки
WINDOW_SIZE = (622, 622)
FPS_LIMIT = 60
FRAME = 0
DISPLAY_DIRECTION_LENGHT = 5
AGENT_DRAW_SIZE = 6

# Настройки поля
FIELD_POS = np.array((50, 50), dtype=np.uint8)
FIELD_SIZE = np.array((512, 512), dtype=np.int32)
FIELD_FRICTION = 0.98

FIELD_RESOLUTION = (32, 32)
FIELD_CELL_SIZE = (
    round(FIELD_SIZE[0] / FIELD_RESOLUTION[0]),
    round(FIELD_SIZE[1] / FIELD_RESOLUTION[1])
)


FIELD_REGEN = np.array((0.005, 0.005, 0.005))

# Параметры агентов


AGENT_LIMIT = 2500  # Максимальное число агентов

AGENT_MUTATION = 1  # Коэфицент мутации агентов (WIP)

AGENT_CONSUMING = (.5, .5, .5)  # Потребление энергии агентом
AGENT_PRODUCING = (0.8, 0.8, 0.8)  # Коэфицент возврата энергии в систему
AGENT_MAX_ENERGY = (200, 200, 200)  # Максимальная энергия системы

AGENT_LIFE_COST = (.05, .05, .05)  # Постянное потребеление энергии агентом
AGENT_LIFE_COST_PER_SPEED = (.02, .02, .02)  # Потребеление энергии агентом за единицу скорости
AGENT_LIFE_COST_PER_SENSE = (.01, .01, .01)  # Потребеление энергии агентом за единицу чувствительности

AGENT_DUPLE_TIMER = (200, 200, 200)  # Период "деления" агента
AGENT_DUPLE_COST = (50, 50, 50)  # Минимальная энергия для "деления"

AGENT_SPEED_MODIFIER = (0.0025, 0.0025, 0.0025)  # Коэфицент скорости агента
AGENT_RANDOM_ROTATION = 0.1  # Коэфицент случайного поворота агента

AGENT_SENSE_RADIUS = 1.5  # Радиус почувствительности агента (WIP)
AGENT_SENSE_MODIFIER = 0.05  # Модификатор чувствительности агента
AGENT_SENSE_BREAK = 0.0  # Модификатор чувствительности агента

HISTORY_CHUNK_SIZE = 200  # Размер блока истроии
