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


def s(d):
    # Prep Lists
    bricks_by_height = collections.defaultdict(list)
    available_heights = set()
    ll = lines(d)
    for l in ll:
        b = [[int(b) for b in l1.split(",")] for l1 in l.split("~")]
        assert not (b[0][0] > b[1][0] or b[0][1] > b[1][1] or b[0][2] > b[1][2])    # Making sure its already sorted

        bricks_by_height[b[0][2]].append(b)
        available_heights.add(b[0][2])

    available_heights = list(available_heights)
    available_heights.sort()

    bricks_by_height, available_heights, _ = move_down(bricks_by_height, available_heights)
    all_shots = 0
    chain_reaction = 0

    for h in available_heights:
        for i in range(len(bricks_by_height[h])):
            bbh = copy.deepcopy(bricks_by_height)
            bbh[h].pop(i)

            _, _, count_move = move_down(bbh, available_heights)
            if count_move == 0:
                all_shots += 1
            else:
                chain_reaction += count_move

    return all_shots, chain_reaction


def move_down(bricks_by_height, available_heights):
    count_move = 0
    height_map = collections.defaultdict(int)
    bricks_by_height2 = collections.defaultdict(list)
    available_heights2 = set()

    for h in available_heights:
        for i in range(len(bricks_by_height[h])):
            b = bricks_by_height[h][i]
            diff = move_diff(b, height_map)
            if diff > 0:
                count_move += 1
            nb = [[*b[0][:2], b[0][2] - diff], [*b[1][:2], b[1][2] - diff]]
            bricks_by_height2[nb[0][2]].append(nb)
            available_heights2.add(nb[0][2])
            height_map = edit_height_map(nb, height_map)

    available_heights2 = list(available_heights2)
    available_heights2.sort()
    return bricks_by_height2, available_heights2, count_move


def edit_height_map(b, height_map):
    for x in range(b[0][0], b[1][0] + 1):
        for y in range(b[0][1], b[1][1] + 1):
            height_map[(x, y)] = max(height_map[(x, y)], b[1][2])
    return height_map


def move_diff(b, height_map):
    highest_point = 0
    for x in range(b[0][0], b[1][0] + 1):
        for y in range(b[0][1], b[1][1] + 1):
            highest_point = max(height_map[(x, y)], highest_point)

    return b[0][2] - highest_point - 1


def main():
    if test():
        file = inp(os.path.join(os.path.dirname(__file__), 'input.txt'))
        solutions = s(file)
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
    a2 = 7
    return validate_solution(s(example), (a1, a2))


main()
