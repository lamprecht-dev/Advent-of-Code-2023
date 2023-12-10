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
    return srec(d, part)
    row_sums = []
    ll = lines(d)
    for line in ll:
        rows = [[x for x in ints(line)]]
        # Construct Rows
        # while sum(rows[-1]) != 0: CAN CAUSE ERRORS!
        while any(x != 0 for x in rows[-1]):
            row = []
            for i, c in enumerate(rows[-1]):
                if i == 0:
                    continue
                row.append(c - rows[-1][i - 1])
            rows.append(row)

        # Find Next in Sequence
        j = len(rows) - 2
        while j > 0:
            j -= 1
            if part == 1:
                rows[j].append(rows[j][-1] + rows[j + 1][-1])
            else:
                rows[j].insert(0, rows[j][0] - rows[j + 1][0])
        if part == 1:
            row_sums.append(rows[0][-1])
        else:
            row_sums.append(rows[0][0])

    return sum(row_sums)


def srec(d, part):
    return sum([next_value(ints(line), part) for line in lines(d)])


def next_value(values, part):
    # Realize we only care about the last/first value anyway in all cases
    differences = [values[i + 1] - values[i] for i in range(len(values) - 1)]
    if any(x != 0 for x in values):
        return values[part - 2] + (next_value(differences, part) * (1 if part == 1 else - 1))
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
    example = """0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45"""
    a1 = 114
    a2 = 2
    return validate_solution((s(example, 1), s(example, 2)), (a1, a2))


main()
