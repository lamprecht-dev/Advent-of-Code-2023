import sys
sys.path.append('../')
from utils import *


def s(d, part):
    global DP
    DP = []
    ll = lines(d)
    dim = (len(ll), len(ll[0]))  # H, W
    rocks, boulders = set(), set()
    for r, line in enumerate(ll):
        for c, ch in enumerate(line):
            if ch == "#":
                rocks.add((c, r))
            elif ch == "O":
                boulders.add((c, r))

    i = 0
    total = 1000000000
    jump_done = False
    while i < total:
        boulders, jump = shift(dirs["u"], dim, rocks, boulders, jump_done)
        if jump is not None:
            i += ((total - i) // jump) * jump
            jump_done = True
        if part == 2:
            boulders, _ = shift(dirs["l"], dim, rocks, boulders)
            boulders, _ = shift(dirs["d"], dim, rocks, boulders)
            boulders, _ = shift(dirs["r"], dim, rocks, boulders)
        else:
            break
        i += 1
    # print_boulders(boulders, rocks, dim)

    return sum([dim[1] - b[1] for b in boulders])


# For Debug Only
def print_boulders(boulders, rocks, dim):
    print(boulders, rocks, dim)
    for r in range(dim[1]):
        row = []
        for c in range(dim[0]):
            if (c, r) in boulders:
                row.append("O")
            elif (c, r) in rocks:
                row.append("#")
            else:
                row.append(".")
        print("".join(row))


DP = []


def shift(dir, dim, rocks, boulders, ignore_dp = False):
    global DP
    new_boulders = set()
    for _ in range(len(boulders)):
        b = boulders.pop()
        possible = b
        for i in range(1, max(dim)):
            n_pos = dir[0] * i + b[0], dir[1] * i + b[1]
            if (n_pos[0] < 0 or n_pos[1] < 0 or n_pos[1] >= dim[1] or n_pos[0] >= dim[0] or
                    n_pos in new_boulders or n_pos in rocks):
                break
            if n_pos in boulders:
                continue
            possible = n_pos
        new_boulders.add(possible)

    if dir == dirs["u"] and not ignore_dp:
        if frozenset(new_boulders) in DP:
            return new_boulders, len(DP) - DP.index(new_boulders)

        DP.append(frozenset(new_boulders))
    return new_boulders, None


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
    example = """O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#...."""
    a1 = 136
    a2 = 64
    return validate_solution((s(example, 1), s(example, 2)), (a1, a2))


main()
