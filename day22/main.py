import copy
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

class Brick:
    def __init__(self, b1, b2):
        b1 = [int(b) for b in b1.split(",")]
        b2 = [int(b) for b in b2.split(",")]

        self.pfrom = (min(b1[0], b2[0]), min(b1[1], b2[1]), min(b1[2], b2[2]))
        self.pto = (max(b1[0], b2[0]), max(b1[1], b2[1]), max(b1[2], b2[2]))

        self.dim = (abs(b1[0] - b2[0]) + 1, abs(b1[1] - b2[1]) + 1, abs(b1[2] - b2[2]) + 1)

    def move_down(self, height_map):
        diff = self.get_diff(height_map)
        # self.print()
        self.pfrom = (self.pfrom[0], self.pfrom[1], self.pfrom[2] - diff)
        self.pto = (self.pto[0], self.pto[1], self.pto[2] - diff)
        # self.print()
        # print(diff)

        for c in range(self.dim[0]):
            for r in range(self.dim[1]):
                c2 = c + self.pfrom[0]
                r2 = r + self.pfrom[1]
                height_map[(c2, r2)] = self.pto[2]

        return height_map, self.pfrom[2], self

    def can_move(self, height_map):
        return self.get_diff(height_map) > 0

    def get_diff(self, height_map):
        max_value = 0
        for c in range(self.dim[0]):
            for r in range(self.dim[1]):
                c2 = c + self.pfrom[0]
                r2 = r + self.pfrom[1]
                max_value = max(max_value, height_map[(c2, r2)])

        return self.pfrom[2] - max_value - 1

    def get_new_submap(self, height_map):
        diff = self.get_diff(height_map)
        submap = collections.defaultdict(int)
        for c in range(self.dim[0]):
            for r in range(self.dim[1]):
                c2 = c + self.pfrom[0]
                r2 = r + self.pfrom[1]
                submap[(c2, r2)] = self.pto[2] - diff
        return submap, self.pto[2] - diff

    def print(self):
        print(self.pfrom, self.pto, self.dim, math.prod(self.dim))

    def overlap(self, other):
        for c in range(self.dim[0]):
            for r in range(self.dim[1]):
                c2 = c + self.pfrom[0]
                r2 = r + self.pfrom[1]
                # print(c2, range(other.pfrom[0], other.pto[0] + 1), c2 in range(other.pfrom[0], other.pto[0] + 1))
                # print(r2, range(other.pfrom[1], other.pto[1] + 1), r2 in range(other.pfrom[1], other.pto[1] + 1))
                # print()
                if (c2 in range(other.pfrom[0], other.pto[0] + 1) and r2 in range(other.pfrom[1], other.pto[1] + 1)
                        and self.pto[2] + 1 == other.pfrom[2]):
                    # print(range(self.pfrom[0], self.pto[0]), range(self.pfrom[1], self.pto[1]), self.pto[2], range(other.pfrom[0], other.pto[0]), range(other.pfrom[1], other.pto[1]), other.pfrom[2])
                    # self.print()
                    # other.print()
                    # print()
                    return True
        return False


def s(d, part):
    if part == 2:
        return 0

    ll = lines(d)

    height_map = collections.defaultdict(int)
    height = collections.defaultdict(list)
    heights = []
    for line in ll:
        brick = Brick(*line.split("~"))
        height[brick.pfrom[2]].append(brick)
        heights.append(brick.pfrom[2])

    heights.sort()
    new_height = collections.defaultdict(list)
    new_heights = set()
    for h in heights:
        for b in height[h]:
            height_map, nh, b = b.move_down(height_map)
            new_height[nh].append(b)
            new_heights.add(nh)

    new_heights = list(new_heights)
    new_heights.sort()
    height_map = collections.defaultdict(int)   # Reset

    bricks_touching = collections.defaultdict(list)
    all_locations = set()
    for h in new_heights:
        for i in range(len(new_height[h])):
            b = new_height[h][i]
            b.print()
            print(h, i)
            for j in range(len(new_height[b.pto[2] + 1])):
                b2 = new_height[b.pto[2] + 1][j]
                if b.overlap(b2):
                    bricks_touching[(b.pto[2] + 1, j)].append((h, i))
            all_locations.add((h, i))

    # pp.pprint(bricks_touching)
    # print(all_locations, len(all_locations))
    all_shots = 0
    for loc in all_locations:
        can_shoot = True
        for bt in bricks_touching:
            if loc in bricks_touching[bt] and len(bricks_touching[bt]) == 1:
                # print(loc, bt, bricks_touching[bt])
                can_shoot = False
                break

        if can_shoot:
            all_shots += 1

    return all_shots


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
    example = """1,0,1~1,2,1
0,0,2~2,0,2
0,2,3~2,2,3
0,0,4~0,2,4
2,0,5~2,2,5
0,1,6~2,1,6
1,1,8~1,1,9"""
    a1 = 5
    a2 = None
    return validate_solution((s(example, 1), s(example, 2)), (a1, a2))


main()


# 6514
# SHOULD BE 463