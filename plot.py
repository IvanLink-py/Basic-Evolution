import matplotlib.pyplot as plt
import matplotlib
import numpy as np
from consts import *

def handle(event):
    if event.key == 'escape':
        plt.close('all')


def draw(frame, agent_count, field_energy, agent_energy, agent_speed, agent_sense):
    fig, ax = plt.subplots(3, 4, figsize=(18, 9), sharex='row')
    time_line = np.arange(frame)

    ax[0, 0].set_title('Кол-во агентов')
    ax[0, 0].plot(time_line, agent_count[:frame, :].sum(1) / 3, color='black', label='Всего')
    ax[0, 0].plot(time_line, agent_count[:frame, 0], color='green', label='Растения')
    ax[0, 0].plot(time_line, agent_count[:frame, 1], color='red', label='Животные')
    ax[0, 0].plot(time_line, agent_count[:frame, 2], color='blue', label='Грибы')
    ax[0, 0].yaxis.set_data_interval(vmin=0, vmax=0, ignore=False)
    ax[0, 0].secondary_yaxis('right', functions=(lambda x: 3 * x, lambda x: x / 3))
    ax[0, 0].legend()
    ax[0, 0].grid(True)

    ax[0, 1].set_title('Энергия поля')
    ax[0, 1].plot(time_line, field_energy[:frame, :].sum(1) / 3, color='black', label='Всего')
    ax[0, 1].plot(time_line, field_energy[:frame, 0], color='red', label='Органика')
    ax[0, 1].plot(time_line, field_energy[:frame, 1], color='green', label='Растительность')
    ax[0, 1].plot(time_line, field_energy[:frame, 2], color='blue', label='Минералы')
    ax[0, 1].yaxis.set_data_interval(vmin=0, vmax=0, ignore=False)
    ax[0, 1].secondary_yaxis('right', functions=(lambda x: 3 * x, lambda x: x / 3))
    ax[0, 1].legend()
    ax[0, 1].grid(True)

    ax[0, 2].set_title('Энергия агентов')
    avg_agent_energy = agent_energy[:frame, :].sum(1) / agent_count[:frame, :].sum(1)
    scale = max(min(1, 1 / (agent_energy.max() / avg_agent_energy.max())), np.float32(.00001))
    ax[0, 2].plot(time_line, agent_energy[:frame, :].sum(1) / 3, color='black', label='Всего')
    ax[0, 2].plot(time_line, avg_agent_energy / scale, color='black', label='Средняя агента', linestyle='--')
    ax[0, 2].plot(time_line, agent_energy[:frame, 0], color='green', label='Растения')
    ax[0, 2].plot(time_line, agent_energy[:frame, 1], color='red', label='Животные')
    ax[0, 2].plot(time_line, agent_energy[:frame, 2], color='blue', label='Грибы')
    ax[0, 2].yaxis.set_data_interval(vmin=0, vmax=0, ignore=False)
    ax[0, 2].secondary_yaxis('right', functions=(lambda x: scale * x, lambda x: x / scale))
    ax[0, 2].legend()
    ax[0, 2].grid(True)

    ax[0, 3].set_title('Энергия системы')
    ax[0, 3].plot(time_line, field_energy[:frame, 1] + agent_energy[:frame, 0], color='green', label='Растения + Растительность')
    ax[0, 3].plot(time_line, field_energy[:frame, 0] + agent_energy[:frame, 1], color='red', label='Животные + Органика')
    ax[0, 3].plot(time_line, field_energy[:frame, 2] + agent_energy[:frame, 2], color='blue', label='Грибы + Минералы')
    ax[0, 3].plot(time_line, (field_energy[:frame, :].sum(1) + agent_energy[:frame, :].sum(1))/3, color='black', label='Общая')
    ax[0, 3].secondary_yaxis('right', functions=(lambda x: 3 * x, lambda x: x / 3))
    ax[0, 3].yaxis.set_data_interval(vmin=0, vmax=0, ignore=False)
    ax[0, 3].legend()
    ax[0, 3].grid(True)

    ax[1, 0].set_title('Эволюция агентов (скорость)')
    ax[1, 0].plot(time_line, agent_speed[:frame, :].sum(1) / agent_count[:frame, :].sum(1), color='black',
                  label='Всего')
    ax[1, 0].plot(time_line, agent_speed[:frame, 0] / agent_count[:frame, 0], color='green', label='Растения')
    ax[1, 0].plot(time_line, agent_speed[:frame, 1] / agent_count[:frame, 1], color='red', label='Животные')
    ax[1, 0].plot(time_line, agent_speed[:frame, 2] / agent_count[:frame, 2], color='blue', label='Грибы')
    ax[1, 0].yaxis.set_data_interval(vmin=0, vmax=0, ignore=False)
    ax[1, 0].legend()
    ax[1, 0].grid(True)

    ax[1, 1].set_title('Эволюция агентов (зрение)')
    ax[1, 1].plot(time_line, agent_sense[:frame, :].sum(1) / agent_count[:frame, :].sum(1), color='black',
                  label='Всего')
    ax[1, 1].plot(time_line, agent_sense[:frame, 0] / agent_count[:frame, 0], color='green', label='Растения')
    ax[1, 1].plot(time_line, agent_sense[:frame, 1] / agent_count[:frame, 1], color='red', label='Животные')
    ax[1, 1].plot(time_line, agent_sense[:frame, 2] / agent_count[:frame, 2], color='blue', label='Грибы')
    ax[1, 1].yaxis.set_data_interval(vmin=0, vmax=0, ignore=False)
    ax[1, 1].legend()
    ax[1, 1].grid(True)

    ax[2, 0].set_title('Параметры системы')
    ax[2, 0].get_yaxis().set_visible(False)
    ax[2, 0].get_xaxis().set_visible(False)

    ax[2, 0].text(0, -0, 'Потребление энергии агентом ' + str(AGENT_CONSUMING))
    ax[2, 0].text(0, -1, '% возврата энергии в систему ' + str(AGENT_PRODUCING))
    ax[2, 0].text(0, -2, 'Максимальная энергия агента ' + str(AGENT_MAX_ENERGY))

    ax[2, 0].text(0, -4, 'Потребеление энергии агентом ' + str(AGENT_LIFE_COST))
    ax[2, 0].text(0, -5, 'Цена единицы скорости ' + str(AGENT_LIFE_COST_PER_SPEED))
    ax[2, 0].text(0, -6, 'Цена единицы чувствительности ' + str(AGENT_LIFE_COST_PER_SENSE))

    ax[2, 0].text(0, -8, 'Период "деления" агента ' + str(AGENT_DUPLE_TIMER))
    ax[2, 0].text(0, -9, 'Минимальная энергия для "деления" ' + str(AGENT_DUPLE_COST))

    ax[2, 0].text(0, -11, 'Коэфицент скорости агента ' + str(AGENT_SPEED_MODIFIER))
    ax[2, 0].text(0, -12, 'Случайный поворот агента ' + str(AGENT_RANDOM_ROTATION))
    ax[2, 0].text(0, -13, 'Модификатор чувствительности агента ' + str(AGENT_SENSE_MODIFIER))

    ax[2, 0].xaxis.set_view_interval(vmin=0, vmax=2, ignore=True)
    ax[2, 0].yaxis.set_view_interval(vmin=-14, vmax=1, ignore=True)



    ax[2, 1].set_title('Энергетический баланс системы')
    ax[2, 1].get_yaxis().set_visible(False)
    ax[2, 1].get_xaxis().set_visible(False)

    a_count = round(agent_count[frame - 1].sum(), 5)
    avg_speed = round(agent_speed[frame - 1].sum() / a_count, 5)
    avg_sense = round(agent_sense[frame - 1].sum() / a_count, 5)
    avg_consume = round(AGENT_LIFE_COST[0] +
                        AGENT_LIFE_COST_PER_SPEED[0] * avg_speed + avg_sense * AGENT_LIFE_COST_PER_SENSE[0], 5)
    avg_produce = round(avg_consume * AGENT_PRODUCING[0], 5)
    avg_balane = round(avg_produce - avg_consume, 5)
    sys_consume = round(avg_balane * a_count, 5)

    avg_light = round(1.65 * 0.5 + 0.65 * 0.5, 5)
    tree_count = round(agent_count[frame - 1, 0], 5)
    avg_mineral = round(float(field_energy[frame - 1, 2] / (FIELD_RESOLUTION[0] * FIELD_RESOLUTION[1])), 5)
    avg_tree_produce = round((min(AGENT_CONSUMING[0], avg_mineral) * avg_light)
                             - min(AGENT_CONSUMING[0], avg_mineral), 5)
    tree_produce = round(avg_tree_produce * tree_count, 5)
    sys_balance = tree_produce - sys_consume

    ax[2, 1].text(0, 0, f'Кол-во агентов: {a_count}')
    ax[2, 1].text(0, -1, f'Средняя скорость: {avg_speed}')
    ax[2, 1].text(0, -2, f'Средняя чувствительность: {avg_sense}')
    ax[2, 1].text(0, -3, f'Потребление среднего агента:  {avg_consume}')
    ax[2, 1].text(0, -4, f'Возврат среднего агента:  {avg_produce}')
    ax[2, 1].text(0, -5, f'Баланс среднего агента:  {avg_balane}')
    ax[2, 1].text(0, -6, f'Расход системы:  {sys_consume}')

    ax[2, 1].text(0, -8, f'Средний уровень света:  {avg_light}')
    ax[2, 1].text(0, -9, f'Кол-во растений:  {tree_count}')
    ax[2, 1].text(0, -10, f'Среднее кол-во минералов в клетке:  {avg_mineral}')
    ax[2, 1].text(0, -11, f'Приток энергии в систему от 1 агента:  {avg_tree_produce}')
    ax[2, 1].text(0, -12, f'Общий приток энергии в систему:  {tree_produce}')
    ax[2, 1].text(0, -13, f'Баланс системы:  {sys_balance}')

    ax[2, 1].xaxis.set_view_interval(vmin=0, vmax=2, ignore=True)
    ax[2, 1].yaxis.set_view_interval(vmin=-18, vmax=1, ignore=True)

    fig.canvas.mpl_connect('key_press_event', handle)

    plt.get_current_fig_manager().full_screen_toggle()
    plt.subplots_adjust(left=0.03,
                        bottom=0.04,
                        right=0.955,
                        top=0.959,
                        wspace=0.25,
                        hspace=0.262)
    plt.show()
