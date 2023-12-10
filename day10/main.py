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


def s(d):
    start = None
    ll = lines(d)
    for r, line in enumerate(ll):
        if start is not None:
            break
        for c, ca in enumerate(line):
            if ca == "S":
                start = (c, r)
                break

    first_pipe = traverse(start, ll, 1)
    loop_pipes = traverse(first_pipe, ll, 2)
    s_types = ["|", "-", "J", "F", "7", "L"]
    s_dirs = []
    for di in dirs:
        d = dirs[di]
        nc, nr = start[0] + d[0], start[1] + d[1]
        if (nc, nr) in loop_pipes:
            s_dirs.append(di)

    print(s_dirs)

    inside_loop = 0

    # nll = []
    # for l in ll:
    #     print(l)
    #
    # print()
    # for r, l in enumerate(ll):
    #     row = ""
    #     for c, ch in enumerate(l):
    #         if (c, r) in loop_pipes:
    #             row += ch
    #         else:
    #             row += " "
    #     nll.append(row)
    #     print(row)
    #
    # print()

    for r in range(len(ll)):
        inside = False

        for c in range(len(ll[0])):
            if (c, r) not in loop_pipes:
                inside_loop += inside
                continue

            # if ll[r][c] == ""


            if (c, r) in loop_pipes:
                continue
            count = 0
            for rr in range(r):
                if (c, rr) in loop_pipes and ll[rr][c] == "-":
                    count += 1
            if count % 2 == 0:
                continue
            count = 0
            for cc in range(c):
                if (cc, r) in loop_pipes and ll[r][cc] == "|":
                    count += 1
            if count % 2 == 1:
                inside_loop += 1


    return len(loop_pipes) // 2, inside_loop


def traverse(start, ll, part):
    seen = set()
    to_see = collections.deque()
    to_see.append(start)
    loop_found = False

    while len(to_see) > 0:
        seeing = to_see.popleft()

        p_dirs = get_directions(ll[seeing[1]][seeing[0]])
        for di in p_dirs:
            d = dirs[di]
            nc, nr = d[0] + seeing[0], d[1] + seeing[1]
            if (nc, nr) in seen:
                continue
            if nc < 0 or nr < 0 or nr >= len(ll) or nc >= len(ll[0]):
                continue

            p_dirs2 = get_directions(ll[nr][nc])
            for di2 in p_dirs2:
                d2 = dirs[di2]
                d2n = (d2[0] * -1, d2[1] * -1)
                if d2n != d:
                    continue

                if (nc, nr) in to_see:
                    if part == 1:
                        return nc, nr
                    loop_found = True
                to_see.append((nc, nr))

        seen.add(seeing)
    assert loop_found
    return seen


def get_directions(pipe):
    if pipe == "S":
        return ["u", "d", "r", "l"]
    if pipe == "|":
        return ["u", "d"]
    if pipe == "-":
        return ["r", "l"]
    if pipe == "F":
        return ["r", "d"]
    if pipe == "L":
        return ["r", "u"]
    if pipe == "J":
        return ["u", "l"]
    if pipe == "7":
        return ["d", "l"]
    return []


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
    example = """7-F7-
.FJ|7
SJLL7
|F--J
LJ.LJ"""
    example2 = """FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJ7F7FJ-
L---JF-JLJ.||-FJLJJ7
|F|F-JF---7F7-L7L|7|
|FFJF7L7F-JF7|JL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L"""
    a1 = 8
    a2 = 10
    return validate_solution((s(example)[0], s(example2)[1]), (a1, a2))


# 3769 too high
# 45

main()
