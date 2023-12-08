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
# import sys
# sys.setrecursionlimit(1000000)

from utils import *


def s(d, part):
    ll = lines(d)
    ins = [0 if c == "L" else 1 for c in ll[0]]
    ins2 = []

    directions = {}

    gcur = []

    for line in ll[2:]:
        direction = line.split(" = ")
        directions[direction[0]] = direction[1].strip("()").split(", ")
        if direction[0][2] == "A":
            gcur.append(direction[0])

    steps = 0
    if part == 1:
        cur = "AAA"
        tar = "ZZZ"
        while cur != tar:
            i = ins.pop(0)
            cur = directions[cur][i]

            steps += 1
            ins2.append(i)
            if len(ins) == 0:
                ins = ins2
    else:
        while sum([0 if c[2] == "Z" else 1 for c in gcur]) != 0:
            i = ins.pop(0)
            ngcur = []
            for c in gcur:
                ngcur.append(directions[c][i])
            gcur = ngcur

            steps += 1
            ins2.append(i)
            if len(ins) == 0:
                ins = ins2

    return steps


def solve2(d):
    ll = lines(d)
    ins = [0 if c == "L" else 1 for c in ll[0]]
    ins2 = []

    directions = {}

    gcur = []

    for line in ll[2:]:
        direction = line.split(" = ")
        directions[direction[0]] = direction[1].strip("()").split(", ")
        if direction[0][2] == "A":
            gcur.append(direction[0])

    zmap = {}
    gcur = {}

    for d in directions:
        phasemap = {}
        if d[2] == "Z" or d[2] == "A":
            for i in range(len(ins)):
                if i > 0 and d[2] == "A":
                    break
                tempins = ins[i:] + ins[:i]
                tempins2 = []
                seen = set()
                cur = d
                s = 0
                while True:
                    t = tempins.pop(0)
                    cur = directions[cur][t]

                    if (s % len(ins), cur) in seen:
                        s = -1
                        break
                    seen.add((s % len(ins), cur))

                    s += 1
                    tempins2.append(t)
                    if len(tempins) == 0:
                        tempins = tempins2

                    if cur[2] == "Z":
                        break

                if s != -1:
                    phasemap[i] = (s, cur)

            if d[2] == "Z":
                zmap[d] = phasemap

            if d[2] == "A":
                gcur[d] = phasemap[0]

    pp.pprint(gcur)
    pp.pprint(zmap)

    overal_step = 0

    while not in_sync(gcur):
        smallest = None
        for i in gcur:
            c = gcur[i]
            if smallest is None or gcur[smallest][0] > c[0]:
                smallest = i
        sv = gcur[smallest]

        new_value = zmap[sv[1]][sv[0] % len(ins)]
        gcur[smallest] = (new_value[0] + sv[0], new_value[1])
        overal_step = new_value[0] + sv[0]


    #  16531 15989 14363  19241 19783 21409

    return overal_step

def in_sync(states):
    first = None
    for s in states:
        st = states[s]
        if first is None:
            first = st[0]
        elif first != st[0]:
            return False
    return True

def main():
    if test():
        file = inp(os.path.join(os.path.dirname(__file__), 'input.txt'))
        solutions = (s(file, 1), solve2(file))
        print("\n\n" + BColors.HEADER + "Solutions" + BColors.ENDC)
        for sol in solutions:
            print(sol)
    else:
        print("\n\n" + BColors.FAIL + "Not All Test Successful" + BColors.ENDC)


def test():
    example = """LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)"""

    example2 = """LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)"""
    a1 = 6
    a2 = 6
    return validate_solution((s(example, 1), solve2(example2)), (a1, a2))


main()
