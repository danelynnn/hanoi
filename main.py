import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.cm as cm
from matplotlib import colormaps
from matplotlib.animation import FuncAnimation
import numpy as np
import copy

towers = [[8, 7, 6, 5, 4, 3, 2, 1], [], []]
game_states = [copy.deepcopy(towers)]
movecount = 0


class InvalidMoveException(Exception):
    pass


class MoveFailedException(Exception):
    pass


def move(pos1, pos2):
    if not towers[pos1]:
        raise InvalidMoveException

    print(f"moving {towers[pos1][-1]} from {pos1} to {pos2}")
    global movecount
    movecount += 1

    if towers[pos2] and towers[pos2][-1] < towers[pos1][-1]:
        raise MoveFailedException()

    towers[pos2].append(towers[pos1].pop(-1))
    game_states.append(copy.deepcopy(towers))
    print(towers)


def above(target):
    for i, tower in enumerate(towers):
        if target in tower:
            return i, tower[tower.index(target) :]
    return -1, None


def below(target):
    min_index, min_value = -1, -1
    for i, tower in enumerate(towers):
        for j in tower:
            if (min_index == -1) or (j < min_value and j > target):
                min_index = i
                min_value = j

    return min_index, min_value


def hanoi(target, location):
    i, stack = above(target)
    if i == -1:
        print("target doesn't exist")
        return
    elif i == location:
        return
    if len(stack) == 1:
        move(i, location)
        return

    open_spot = 3 - i - location
    hanoi(stack[1], open_spot)
    move(i, location)
    hanoi(stack[1], location)


def hanoi_start():
    rings = [ring for tower in towers for ring in tower]
    rings.sort()
    for r in rings[:-1]:
        print(f"fixing ring {r}")
        hanoi(r, below(r)[0])

    hanoi(rings[-1], 2)


def func(game_state):
    # arr = np.array(towers)
    lens = np.array([len(i) for i in game_state])
    mask = np.arange(lens.max()) < lens[:, None]
    arr = np.zeros(mask.shape)
    arr[mask] = np.concatenate(game_state)
    arr = np.transpose(arr)
    transpose = arr.tolist()

    flatten = [ring for tower in towers for ring in tower]
    mapping = cm.ScalarMappable(
        norm=colors.Normalize(vmin=min(flatten), vmax=max(flatten)),
        cmap=colormaps["rainbow"],
    )

    # cbar = fig.colorbar(mapping, orientation='vertical')
    bars = []
    bottom = np.zeros(3)

    axes.clear()
    axes.set_ylim(0, 80)
    axes.set_xlim(-10, 30)

    # axes.text(20, 20, horizontalalignment='right')

    for row in transpose:
        bars.append(
            axes.bar(
                x=range(0, len(towers) * 10, 10),
                height=5,
                width=[0 if r == 0 else (r + 2) for r in row],
                color=mapping.to_rgba(row),
                bottom=bottom,
            )
        )
        bottom += 5

    return bars


hanoi_start()

fig, axes = plt.subplots()
axes.set_ylim(0, 80)
axes.set_xlim(-7.5, 27.5)

animation = FuncAnimation(fig, func, frames=game_states, interval=500)
plt.show()

print(movecount)
