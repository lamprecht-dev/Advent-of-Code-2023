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
    non_rocks = []
    start = (None, None)
    DIM = len(ll)
    for r, line in enumerate(ll):
        for c, ch in enumerate(line):
            if ch == ".":
                non_rocks.append((c, r))
            elif ch == "S":
                start = (c, r)

    odd = set()
    even = set()
    next = collections.deque()
    cur = collections.deque()
    cur.append(start)
    for i in range(65 if part == 1 else 26501366):
        while len(cur) > 0:
            c = cur.popleft()
            for d in dirs:
                dd = dirs[d]
                nn = (dd[0] + c[0], dd[1] + c[1])
                nnd = (nn[0] % DIM, nn[1] % DIM)

                if nn in odd or nn in even or nn in next or nn in cur or nnd not in non_rocks:
                    continue
                next.append(nn)

            if i % 2 == 0:
                even.add(c)
            else:
                odd.add(c)
        cur = next
        next = collections.deque()

    return len(even) if part == 1 else len(odd)


def main():
    file = inp(os.path.join(os.path.dirname(__file__), 'input.txt'))
    solutions = (s(file, 1), s(file, 2))
    print("\n\n" + BColors.HEADER + "Solutions" + BColors.ENDC)
    for sol in solutions:
        print(sol)


main()