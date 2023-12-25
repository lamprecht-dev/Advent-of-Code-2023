import sys
import sympy

sys.path.append('../')
from utils import *


def part1(d, search_range=(200000000000000, 400000000000000)):
    paths = []

    ll = lines(d)
    for line in ll:
        pos, direction = line.split(" @ ")
        pos = [int(p) for p in pos.split(", ")]
        direction = [int(di) for di in direction.split(", ")]
        a = direction[1] / direction[0]
        b = pos[1] - (pos[0] * a)

        paths.append((pos, direction, a, b))

    count_test_encounter = 0
    for i1 in range(len(paths)):
        p1 = paths[i1]
        for i2 in range(i1 + 1, len(paths)):
            p2 = paths[i2]
            if p1 is p2:
                continue

            # Me trying to do some math
            bd = (p2[3] - p1[3])
            ad = (p1[2] - p2[2])
            if ad != 0:
                x = bd / ad
                y = p1[2] * x + p1[3]
                p1dir = (x - p1[0][0]) / p1[1][0]
                p2dir = (x - p2[0][0]) / p2[1][0]

                if (search_range[0] <= x <= search_range[1] and search_range[0] <= y <= search_range[1] and
                        p1dir > 0 and p2dir > 0):
                    count_test_encounter += 1

    return count_test_encounter


def part2(d):
    ll = lines(d)
    paths = []
    for line in ll:
        pos, direction = line.split(" @ ")
        pos = [int(p) for p in pos.split(", ")]
        direction = [int(di) for di in direction.split(", ")]

        paths.append((pos, direction))

    # This is what we are solving for
    rockx, rocky, rockz, rockVx, rockVy, rockVz = sympy.symbols("rockx, rocky, rockz, rockVx, rockVy, rockVz")

    sympy_functions = []
    for p in paths:
        # These we know from the storms
        (x, y, z), (vx, vy, vz) = p
        # Sympy should use these functions to calculate the solutions for our symbols
        sympy_functions.append((rockx - x) * (vy - rockVy) - (rocky - y) * (vx - rockVx))
        sympy_functions.append((rockz - z) * (vy - rockVy) - (rocky - y) * (vz - rockVz))

    answer = sympy.solve(sympy_functions)
    assert len(answer) == 1
    print(answer[0])

    return answer[0][rockx] + answer[0][rocky] + answer[0][rockz]


def main():
    if test():
        file = inp(os.path.join(os.path.dirname(__file__), 'input.txt'))
        solutions = (part1(file), part2(file))
        print("\n\n" + BColors.HEADER + "Solutions" + BColors.ENDC)
        for sol in solutions:
            print(sol)
    else:
        print("\n\n" + BColors.FAIL + "Not All Test Successful" + BColors.ENDC)


def test():
    example = """19, 13, 30 @ -2,  1, -2
18, 19, 22 @ -1, -1, -2
20, 25, 34 @ -2, -2, -4
12, 31, 28 @ -1, -2, -1
20, 19, 15 @  1, -5, -3"""
    a1 = 2
    a2 = 47
    return validate_solution((part1(example, (7, 27)), part2(example)), (a1, a2))


main()
