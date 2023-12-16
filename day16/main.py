import sys
import collections
sys.path.append('../')
from utils import *


def s(d, part):
    ll = lines(d)
    DIM = (len(ll[0]), len(ll))
    if part == 1:
        return count_energized(ll, DIM, (-1, 0, "r"))

    max_count = 0

    for c in range(DIM[0]):
        max_count = max(count_energized(ll, DIM, (c, -1, "d")), max_count)
        max_count = max(count_energized(ll, DIM, (c, DIM[1], "u")), max_count)
    for r in range(DIM[1]):
        max_count = max(count_energized(ll, DIM, (-1, r, "r")), max_count)
        max_count = max(count_energized(ll, DIM, (DIM[0], r, "l")), max_count)

    return max_count


def count_energized(ll, DIM, starting):
    tiles = {}

    for r, line in enumerate(ll):
        for c, ch in enumerate(line):
            if ch != ".":
                tiles[(c, r)] = ch

    seen = set()
    next = collections.deque()
    next.append(starting)
    while len(next) > 0:
        n = next.popleft()
        new = n[0] + dirs[n[2]][0], n[1] + dirs[n[2]][1]
        nexts = get_nexts(new, n[2], tiles, DIM)
        for ne in nexts:
            if ne in seen:
                continue
            next.append(ne)
        seen.add(n)

    unique_seen = set()
    for se in seen:
        unique_seen.add((se[0], se[1]))

    return len(unique_seen) - 1


def get_nexts(tile, direction, tiles, dim):
    if tile[0] < 0 or tile[1] < 0 or tile[0] >= dim[0] or tile[1] >= dim[1]:
        return []
    if tile not in tiles:
        return [(*tile, direction)]
    t = tiles[tile]
    if t == "/":
        if direction == "r":
            return [(*tile, "u")]
        if direction == "u":
            return [(*tile, "r")]
        if direction == "d":
            return [(*tile, "l")]
        if direction == "l":
            return [(*tile, "d")]
    if t == "\\":
        if direction == "r":
            return [(*tile, "d")]
        if direction == "d":
            return [(*tile, "r")]
        if direction == "u":
            return [(*tile, "l")]
        if direction == "l":
            return [(*tile, "u")]
    if t == "-":
        if direction == "r":
            return [(*tile, "r")]
        if direction in "ud":
            return [(*tile, "r"), (*tile, "l")]
        if direction == "l":
            return [(*tile, "l")]
    if t == "|":
        if direction == "u":
            return [(*tile, "u")]
        if direction in "lr":
            return [(*tile, "u"), (*tile, "d")]
        if direction == "d":
            return [(*tile, "d")]
    return []


def main():
    if test():
        file = inp(os.path.join(os.path.dirname(__file__), 'input.txt'))
        solutions = (s(file, 1), s(file, 2))
        print("\n\n" + BColors.HEADER + "Solutions" + BColors.ENDC)
        for sol in solutions:
            print(sol)
    else:
        print("\n\n" + BColors.FAIL + "Not All Test Successful" + BColors.ENDC)


def test():
    example = r""".|...\....
|.-.\.....
.....|-...
........|.
..........
.........\
..../.\\..
.-.-/..|..
.|....-|.\
..//.|...."""
    a1 = 46
    a2 = 51
    return validate_solution((s(example, 1), s(example, 2)), (a1, a2))


main()