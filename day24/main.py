import sys
import collections
import datetime
import itertools
import functools
import math
from operator import itemgetter as ig
import pprint as pp
import re
import numpy as np
# import bisect
# import heapq
# sys.setrecursionlimit(1000000)

sys.path.append('../')
from utils import *


def s(d, part, search_range=(200000000000000, 400000000000000)):
    if part == 2:
        return 0

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
    example = """19, 13, 30 @ -2,  1, -2
18, 19, 22 @ -1, -1, -2
20, 25, 34 @ -2, -2, -4
12, 31, 28 @ -1, -2, -1
20, 19, 15 @  1, -5, -3"""
    a1 = 2
    a2 = 47
    return validate_solution((s(example, 1, (7, 27)), s(example, 2)), (a1, a2))


main()
