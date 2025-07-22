import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.cm as cm
from matplotlib import colormaps
from matplotlib.animation import FuncAnimation
import numpy as np


fig, axes = plt.subplots()

def func(game_state):
    print(game_state)
    lens = np.array([len(tower) for tower in game_state.towers])
    mask = np.arange(lens.max()) < lens[:, None]
    arr = np.zeros(mask.shape)
    arr[mask] = np.concatenate(game_state.towers)
    arr = np.transpose(arr)
    transpose = arr.tolist()

    flatten = list(game_state.towers_dict.keys())
    mapping = cm.ScalarMappable(
        norm=colors.Normalize(vmin=min(flatten), vmax=max(flatten)),
        cmap=colormaps["rainbow"],
    )

    bars = []
    bottom = np.zeros(3)

    axes.clear()
    axes.set_ylim(0, 50)
    axes.set_xlim(-7.5, 27.5)
    axes.xaxis.set_visible(False)
    axes.spines['left'].set_visible(False)
    axes.yaxis.set_visible(False)
    axes.spines['top'].set_visible(False)
    axes.spines['right'].set_visible(False)

    # axes.text(20, 20, horizontalalignment='right')

    for row in transpose:
        bars.append(
            axes.bar(
                x=range(0, len(game_state.towers) * 10, 10),
                height=5,
                width=[0 if r == 0 else (r + 2) for r in row],
                color=mapping.to_rgba(row),
                bottom=bottom,
            )
        )
        bottom += 5

    return bars

def show_anim(game_states, speed=500):
    axes.xaxis.set_visible(False)
    axes.spines['left'].set_visible(False)
    axes.yaxis.set_visible(False)
    axes.spines['top'].set_visible(False)
    axes.spines['right'].set_visible(False)

    animation = FuncAnimation(fig, func, frames=game_states, interval=speed)
    plt.show()
