import copy

from hanoi import Hanoi
from plot import show_anim

game = Hanoi([[4, 3], [1], [2]])
game_states = [copy.deepcopy(game)]


# locate ring, find entire stack above it (including it)
# return (tower index, stack)
def above(target):
    tower, index = game.towers_dict.get(target, -1)
    return tower, game.towers[tower][index:]

# locate intended parent of ring
# return tower index of parent
def below(target):
    ring = min([ring for ring in game.towers_dict.keys() if ring > target])

    return game.towers_dict[ring][0]


def hanoi(target, location):
    t, stack = above(target)
    if t == -1:
        print("target doesn't exist")
        return
    elif t == location:
        return
    
    if len(stack) != 1:
        # find location for target's child
        open_spot = 3 - t - location
        # move target's child to that location
        hanoi(stack[1], open_spot)
    # move target
    game.move(t, location)
    game_states.append(copy.deepcopy(game))
    if len(stack) != 1:
        # move target's child on top of target
        hanoi(stack[1], location)


def hanoi_start():
    rings = list(game.towers_dict.keys())
    rings.sort()

    # from smallest to largest ring, place it on top of its parent
    for r in rings[:-1]:
        print(f"fixing ring {r}")
        hanoi(r, below(r))

    # move largest ring to destination
    hanoi(rings[-1], 2)



hanoi_start()
show_anim(game_states)

print(game.move_count)
