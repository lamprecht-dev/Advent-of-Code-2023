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
    # stats(d)
    # print("Input: ", repr(d))

    # nums = ints(d)

    # ll = lines(d)
    # for line in ll:

    # ww = words(d)
    # for line in ww:

    return 0


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
    example = """"""
    a1 = None
    a2 = None
    return validate_solution((s(example, 1), s(example, 2)), (a1, a2))


main()
