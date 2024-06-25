import matplotlib.pyplot as plt
import matplotlib
import numpy as np
from consts import *


def draw(frame, agent_count, field_energy, agent_energy):
    fig, ax = plt.subplots(3, 2, figsize=(16, 9))
    time_line = np.arange(frame)

    ax[0, 0].set_title('Кол-во агентов')
    ax[0, 0].plot(time_line, agent_count[:frame, 0], color='green', label='Растения')
    ax[0, 0].plot(time_line, agent_count[:frame, 1], color='red', label='Животные')
    ax[0, 0].plot(time_line, agent_count[:frame, 2], color='blue', label='Грибы')
    ax[0, 0].plot(time_line, agent_count[:frame, :].sum(1), color='black', label='Всего')
    ax[0, 0].yaxis.set_data_interval(vmin=0, vmax=AGENT_LIMIT, ignore=True)
    ax[0, 0].legend()
    ax[0, 0].grid(True)

    ax[1, 0].set_title('Энергия поля')
    ax[1, 0].plot(time_line, field_energy[:frame, 0], color='red', label='Органика')
    ax[1, 0].plot(time_line, field_energy[:frame, 1], color='green', label='Растительность')
    ax[1, 0].plot(time_line, field_energy[:frame, 2], color='blue', label='Минералы')
    ax[1, 0].plot(time_line, field_energy[:frame, :].sum(1), color='black', label='Всего')
    ax[1, 0].yaxis.set_data_interval(vmin=0, vmax=0, ignore=False)
    ax[1, 0].legend()
    ax[1, 0].grid(True)

    ax[2, 0].set_title('Энергия агентов')
    ax[2, 0].plot(time_line, agent_energy[:frame, 0], color='red', label='Растения')
    ax[2, 0].plot(time_line, agent_energy[:frame, 1], color='green', label='Животные')
    ax[2, 0].plot(time_line, agent_energy[:frame, 2], color='blue', label='Грибы')
    ax[2, 0].plot(time_line, agent_energy[:frame, :].sum(1), color='black', label='Всего')

    ax[2, 0].plot(time_line, agent_energy[:frame, 0] / agent_count[:frame, 0] * 400, color='red', label='Растения (Ср.)', linewidth=2, linestyle='--')
    ax[2, 0].plot(time_line, agent_energy[:frame, 1] / agent_count[:frame, 1] * 400, color='green', label='Животные (Ср.)', linewidth=2, linestyle='--')
    ax[2, 0].plot(time_line, agent_energy[:frame, 2] / agent_count[:frame, 2] * 400, color='blue', label='Грибы (Ср.)', linewidth=2, linestyle='--')
    ax[2, 0].plot(time_line, agent_energy[:frame, :].sum(1) / agent_count[:frame, :].sum(1) * 400, color='black', label='Всего (Ср.)', linewidth=2, linestyle='--')

    ax[2, 0].yaxis.set_data_interval(vmin=0, vmax=0, ignore=False)
    ax[2, 0].secondary_yaxis('right', functions=(lambda x: x / 400, lambda x: 400 * x))
    ax[2, 0].legend()
    ax[2, 0].grid(True)

    # ax[1, 1].set_title('Энергия системы')
    # ax[1, 1].plot(time_line, agent_energy[:frame, 0], color='red', label='Органика (А)', linewidth=2, linestyle=':')
    # ax[1, 1].plot(time_line, field_energy[:frame, 0], color='red', label='Органика (П)', linewidth=2, linestyle='--')
    # ax[1, 1].plot(time_line, agent_energy[:frame, 0] + field_energy[:frame, 0], color='red', label='Органика (О)', linewidth=2, linestyle='-')
    # ax[1, 1].plot(time_line, agent_energy[:frame, 1], color='green', label='Растительность (А)', linewidth=2, linestyle=':')
    # ax[1, 1].plot(time_line, field_energy[:frame, 1], color='green', label='Растительность (П)', linewidth=2, linestyle='--')
    # ax[1, 1].plot(time_line, agent_energy[:frame, 1] + field_energy[:frame, 1], color='green', label='Растительность (О)', linewidth=2, linestyle='-')
    # ax[1, 1].plot(time_line, agent_energy[:frame, 2], color='blue', label='Минералы (А)', linewidth=2, linestyle=':')
    # ax[1, 1].plot(time_line, field_energy[:frame, 2], color='blue', label='Минералы (П)', linewidth=2, linestyle='--')
    # ax[1, 1].plot(time_line, agent_energy[:frame, 2] + field_energy[:frame, 2], color='blue', label='Минералы (О)', linewidth=2, linestyle='-')
    # # ax[1, 1].plot(time_line, agent_energy[:frame, :].sum(1), color='black', label='Всего (А)', linewidth=2, linestyle=':')
    # # ax[1, 1].plot(time_line, field_energy[:frame, :].sum(1), color='black', label='Всего (П)', linewidth=2, linestyle='--')
    # # ax[1, 1].plot(time_line, agent_energy[:frame, :].sum(1) + field_energy[:frame, :].sum(1), color='black', label='Всего (О)', linewidth=2, linestyle='-')
    # ax[1, 1].yaxis.set_data_interval(vmin=0, vmax=0, ignore=False)
    # ax[1, 1].legend()
    # ax[1, 1].grid(True)

    plt.show()
