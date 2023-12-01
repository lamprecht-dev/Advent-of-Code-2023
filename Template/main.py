import collections as coll
import datetime as dt
import itertools as it
import math
from operator import itemgetter as ig
import pprint as pp
import re
# import bisect
# import heapq
# import sys
# sys.setrecursionlimit(1000000)

from utils import *


def solve(d):
    stats(d)
    print("Input: ", repr(d))
    t = 0
    t2 = 0

    # nums = ints(d)

    # ll = lines(d)
    # for line in ll:

    # ww = words(d)
    # for line in ww:


    return t, t2


def main():
    if test():
        solutions = solve(inp(os.path.join(os.path.dirname(__file__), 'input.txt')))
        print("\n\n" + BColors.HEADER + "Solutions" + BColors.ENDC)
        for s in solutions:
            print(s)
    else:
        print("\n\n" + BColors.FAIL + "Not All Test Successful" + BColors.ENDC)


def test():
    s = """"""
    a1 = None
    a2 = None
    return validate_solution(solve(s), (a1, a2))


main()
