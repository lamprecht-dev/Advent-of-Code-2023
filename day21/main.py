import sys
import collections

sys.path.append('../')
from utils import *


def s(d, part):
    if part == 2:
        return 0

    ll = lines(d)
    # Rows with no walls: 0 65 130
    # Cols with no walls: 65 130
    # Start 65, 65
    # Dimensions: 131 x 131
    # Steps to walk across: 131 (including the first step onto the grid from the previous grid)
    # The same is if we suddenly start to walk up or down.
    #   As it takes 66 to walk onto the center. And 65 to walk towards an edge.
    # This is the amount of steps we need: 26501365
    # It takes us 65 tiles to any edge from the start
    # Than we can cross 202300 Grids IN EACH DIRECTION.
    # The problem now left is how many steps does it take to fill a grid from each side
    # MAX AVAILABLE PER GRID: Odd/ Even (7584, 7613)
    # So we need to calulcate how many in grid are going to odd or even
    #   and then we need to calculate how many are on the outer edge

    # X X X 3 X X X
    # X X 3 2 3 X X
    # X 3 2 1 2 3 X
    # 3 2 1 0 1 2 3
    # X 3 2 1 2 3 X
    # X X 3 2 3 X X
    # X X X 3 X X X

    # 0: 1
    # 1: 4
    # 2: 8
    # 3: 12
    # N1 = N0 + 4 EXCEPT first one is from 1 -> 4

    steps = 26501365
    size = len(ll)

    # This section calculate the majority of the Grid
    layer_i = 1
    current_layer = 4
    odd_layers = 1
    even_layers = 4
    while layer_i < 202300 - 1:
        current_layer += 4
        if layer_i % 2 == 0:
            even_layers += current_layer
        else:
            odd_layers += current_layer
        layer_i += 1

    grid_width = steps // size - 1
    odd_layers = (grid_width // 2 * 2 + 1) ** 2
    even_layers = ((grid_width + 1) // 2 * 2) ** 2

    TOTAL_ODD = odd_layers * 7584 + even_layers * 7613

    # This section now add whatever is left for the outermost layer!
    for sf in [(65, 0), (130, 65), (65, 130), (0, 65)]:
        TOTAL_ODD += fill(sf[1], sf[0], ll, size - 1)

    smaller, bigger = 0, 0
    for sf in [(0, 0), (130, 130), (0, 130), (130, 0)]:
        smaller += fill(sf[1], sf[0], ll, size // 2 - 1)

    for sf in [(0, 0), (130, 130), (0, 130), (130, 0)]:
        bigger += fill(sf[1], sf[0], ll, size * 3 // 2 - 1)

    return fill(65, 65, ll, 64), TOTAL_ODD + smaller * (grid_width + 1) + bigger * grid_width


# Sadly I had to use some HEAVY help from HyperNeutrino as I did not know how I had my original fill funcion wrong...
def fill(sr, sc, ll, ss):
    ans = set()
    seen = {(sr, sc)}
    q = collections.deque([(sr, sc, ss)])

    while q:
        r, c, s = q.popleft()

        if s % 2 == 0:
            ans.add((r, c))
        if s == 0:
            continue

        for nr, nc in [(r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)]:
            if nr < 0 or nr >= len(ll) or nc < 0 or nc >= len(ll[0]) or ll[nr][nc] == "#" or (nr, nc) in seen:
                continue
            seen.add((nr, nc))
            q.append((nr, nc, s - 1))

    return len(ans)


def main():
    file = inp(os.path.join(os.path.dirname(__file__), 'input.txt'))
    solutions = (s(file, 1), s(file, 2))
    print("\n\n" + BColors.HEADER + "Solutions" + BColors.ENDC)
    for sol in solutions:
        print(sol)


main()
