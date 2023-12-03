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


def parse_input(d):
    symbols = set()
    gears = []
    numbers = []

    ll = lines(d)
    for row, line in enumerate(ll):
        current_num = None
        start = 0
        for col, c in enumerate(line):
            if c.isnumeric():
                if current_num is None:
                    current_num = int(c)
                    start = col
                else:
                    current_num = current_num * 10 + int(c)
            elif c == "." and current_num is not None:
                numbers.append((row, start, col - 1, current_num))
                current_num = None
            elif c != ".":
                symbols.add((row, col))
                if c == "*":
                    gears.append((row, col))
                if current_num is not None:
                    numbers.append((row, start, col - 1, current_num))
                    current_num = None
        if current_num is not None:
            numbers.append((row, start, len(line) - 1, current_num))
    return symbols, gears, numbers


def solve(d):
    part_sum = 0
    gear_ratios = 0

    symbols, gears, numbers = parse_input(d)

    for num in numbers:
        found_symbol = False
        for y in range(num[0] - 1, num[0] + 2):
            if found_symbol:
                break
            for x in range(num[1] - 1, num[2] + 2):
                if y == num[0] and num[1] <= x <= num[2]:
                    continue
                if (y, x) in symbols:
                    part_sum += num[3]
                    found_symbol = True
                    break

    dirs_diag = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    for g in gears:
        nums_found = set()
        nums_prod = 1

        for d in dirs_diag:
            ny, nx = g[0] + d[0], g[1] + d[1]
            for n in numbers:
                if n in nums_found:
                    continue
                if n[0] == ny and n[1] <= nx <= n[2]:
                    nums_found.add(n)
                    nums_prod *= n[3]

        if len(nums_found) == 2:
            gear_ratios += nums_prod

    return part_sum, gear_ratios


def main():
    if test():
        solutions = solve(inp(os.path.join(os.path.dirname(__file__), 'input.txt')))
        print("\n\n" + BColors.HEADER + "Solutions" + BColors.ENDC)
        for s in solutions:
            print(s)
    else:
        print("\n\n" + BColors.FAIL + "Not All Test Successful" + BColors.ENDC)


def test():
    s = """467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598.."""
    a1 = 4361
    a2 = 467835
    return validate_solution(solve(s), (a1, a2))


main()
