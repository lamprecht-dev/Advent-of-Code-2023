import sys
import collections
import datetime
import itertools
import functools
import math
from operator import itemgetter as ig
import pprint as pp
import re
# import bisect
# import heapq
# sys.setrecursionlimit(1000000)

sys.path.append('../')
from utils import *


def s(d, part):
    ll = lines(d)
    galaxies = get_galaxies(ll)

    empty_rows = []
    empty_cols = []
    for r, line in enumerate(ll):
        if all(c == "." for c in line):
            empty_rows.append(r)

    for i in range(len(ll[0])):
        if all(ll[j][i] == "." for j in range(len(ll))):
            empty_cols.append(i)

    # Now "pathfinding" between any two galaxies
    path_sum = 0
    for a in range(len(galaxies)):
        for b in range(a + 1, len(galaxies)):
            path_sum += abs(galaxies[a][0] - galaxies[b][0]) + abs(galaxies[a][1] - galaxies[b][1])
            for er in empty_rows:
                if galaxies[a][1] <= er <= galaxies[b][1] or galaxies[b][1] <= er <= galaxies[a][1]:
                    path_sum += 1 if part == 1 else 999999
            for ec in empty_cols:
                if galaxies[a][0] <= ec <= galaxies[b][0] or galaxies[b][0] <= ec <= galaxies[a][0]:
                    path_sum += 1 if part == 1 else 999999

    return path_sum


def get_galaxies(ll):
    galaxies = []
    for r, l in enumerate(ll):
        for c, ch in enumerate(l):
            if ch == "#":
                galaxies.append((c, r))
    return galaxies


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
    example = """...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#....."""
    a1 = 374
    a2 = None
    return validate_solution((s(example, 1), s(example, 2)), (a1, a2))


main()
