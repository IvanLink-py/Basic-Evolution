import matplotlib.pyplot as plt
import matplotlib
import numpy as np
from consts import *


def draw(frame, agent_count, field_energy, agent_energy, agent_speed, agent_sense):
    fig, ax = plt.subplots(3, 2, figsize=(16, 9))
    time_line = np.arange(frame)

    ax[0, 0].set_title('Кол-во агентов')
    ax[0, 0].plot(time_line, agent_count[:frame, :].sum(1) / 3, color='black', label='Всего')
    ax[0, 0].plot(time_line, agent_count[:frame, 0], color='green', label='Растения')
    ax[0, 0].plot(time_line, agent_count[:frame, 1], color='red', label='Животные')
    ax[0, 0].plot(time_line, agent_count[:frame, 2], color='blue', label='Грибы')
    ax[0, 0].yaxis.set_data_interval(vmin=0, vmax=0, ignore=False)
    ax[0, 0].legend()
    ax[0, 0].grid(True)

    ax[1, 0].set_title('Энергия поля')
    ax[1, 0].plot(time_line, field_energy[:frame, :].sum(1) / 3, color='black', label='Всего')
    ax[1, 0].plot(time_line, field_energy[:frame, 0], color='red', label='Органика')
    ax[1, 0].plot(time_line, field_energy[:frame, 1], color='green', label='Растительность')
    ax[1, 0].plot(time_line, field_energy[:frame, 2], color='blue', label='Минералы')
    ax[1, 0].yaxis.set_data_interval(vmin=0, vmax=0, ignore=False)
    ax[1, 0].legend()
    ax[1, 0].grid(True)

    ax[2, 0].set_title('Энергия агентов')
    ax[2, 0].plot(time_line, agent_energy[:frame, :].sum(1) / 3, color='black', label='Всего')
    ax[2, 0].plot(time_line, agent_energy[:frame, 0], color='green', label='Растения')
    ax[2, 0].plot(time_line, agent_energy[:frame, 1], color='red', label='Животные')
    ax[2, 0].plot(time_line, agent_energy[:frame, 2], color='blue', label='Грибы')
    ax[2, 0].yaxis.set_data_interval(vmin=0, vmax=0, ignore=False)
    ax[2, 0].legend()
    ax[2, 0].grid(True)

    ax[0, 1].set_title('Эволюция агентов (скорость)')
    ax[0, 1].plot(time_line, agent_speed[:frame, :].sum(1) / agent_count[:frame, :].sum(1), color='black',
                  label='Всего')
    ax[0, 1].plot(time_line, agent_speed[:frame, 0] / agent_count[:frame, 0], color='green', label='Растения')
    ax[0, 1].plot(time_line, agent_speed[:frame, 1] / agent_count[:frame, 1], color='red', label='Животные')
    ax[0, 1].plot(time_line, agent_speed[:frame, 2] / agent_count[:frame, 2], color='blue', label='Грибы')
    ax[0, 1].yaxis.set_data_interval(vmin=0, vmax=0, ignore=False)
    ax[0, 1].legend()
    ax[0, 1].grid(True)

    ax[1, 1].set_title('Эволюция агентов (зрение)')
    ax[1, 1].plot(time_line, agent_sense[:frame, :].sum(1) / agent_count[:frame, :].sum(1), color='black',
                  label='Всего')
    ax[1, 1].plot(time_line, agent_sense[:frame, 0] / agent_count[:frame, 0], color='green', label='Растения')
    ax[1, 1].plot(time_line, agent_sense[:frame, 1] / agent_count[:frame, 1], color='red', label='Животные')
    ax[1, 1].plot(time_line, agent_sense[:frame, 2] / agent_count[:frame, 2], color='blue', label='Грибы')
    ax[1, 1].yaxis.set_data_interval(vmin=0, vmax=0, ignore=False)
    ax[1, 1].legend()
    ax[1, 1].grid(True)

    ax[2, 1].set_title('Параметры системы')
    ax[2, 1].get_yaxis().set_visible(False)
    ax[2, 1].get_xaxis().set_visible(False)

    a_count = round(agent_count[frame - 1].sum(), 5)
    avg_speed = round(agent_speed[frame - 1].sum() / a_count, 5)
    avg_sense = round(agent_sense[frame - 1].sum() / a_count, 5)
    avg_consume = round(AGENT_LIFE_COST[0] +
                        AGENT_LIFE_COST_PER_SPEED[0] * avg_speed + avg_sense * AGENT_LIFE_COST_PER_SENSE[0], 5)
    avg_produce = round(avg_consume * AGENT_PRODUCING[0], 5)
    avg_balane = round(avg_produce - avg_consume, 5)
    sys_balane = round(avg_balane * a_count, 5)

    avg_light = round(1.65 * 0.5 + 0.65 * 0.5, 5)
    tree_count = round(agent_count[frame - 1, 0], 5)
    avg_mineral = round(field_energy[frame-1, 2] / (FIELD_RESOLUTION[0] * FIELD_RESOLUTION[1]), 5)
    avg_tree_produce = (min(AGENT_CONSUMING[0], avg_mineral) * avg_light) - min(AGENT_CONSUMING[0], avg_mineral)
    tree_produce = avg_tree_produce * tree_count


    ax[2, 1].text(0, 0, f'Кол-во агентов: {a_count}')
    ax[2, 1].text(0, -1, f'Средняя скорость: {avg_speed}')
    ax[2, 1].text(0, -2, f'Средняя чувствительность: {avg_sense}')
    ax[2, 1].text(0, -3, f'Потребление среднего агента:  {avg_consume}')
    ax[2, 1].text(0, -4, f'Возврат среднего агента:  {avg_produce}')
    ax[2, 1].text(0, -5, f'Баланс среднего агента:  {avg_balane}')
    ax[2, 1].text(0, -6, f'Баланс системы:  {sys_balane}')

    ax[2, 1].text(0, -8, f'Средний уровень света:  {avg_light}')
    ax[2, 1].text(0, -9, f'Кол-во растений:  {tree_count}')
    ax[2, 1].text(0, -10, f'Среднее кол-во минералов в клетке:  {avg_mineral}')
    ax[2, 1].text(0, -11, f'Приток энергии в систему от 1 агента:  {avg_tree_produce}')
    ax[2, 1].text(0, -12, f'Общий приток энергии в систему:  {tree_produce}')

    ax[2, 1].yaxis.set_view_interval(vmin=-12, vmax=1, ignore=True)
    ax[2, 1].xaxis.set_view_interval(vmin=0, vmax=2, ignore=True)

    plt.show()
