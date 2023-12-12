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
    total_arrangements = 0
    ll = lines(d)
    for r, line in enumerate(ll):
        pattern, groups = line.split()
        groups = ints(groups, ",")
        if part == 2:
            groups *= 5
            pattern = "?".join([pattern] * 5)
        arr = arrangements(pattern, groups)
        total_arrangements += arr

    return total_arrangements


def arrangements(pattern, groups):
    if not any(p == "?" for p in pattern):
        return is_valid2(pattern, groups)

    arrangement_count = 0

    i = pattern.index("?")
    possible_pattern = pattern[:i] + "." + pattern[i+1:]
    if is_valid(possible_pattern, groups):
        arrangement_count += arrangements(possible_pattern, groups)

    possible_pattern = pattern[:i] + "#" + pattern[i+1:]
    if is_valid(possible_pattern, groups):
        arrangement_count += arrangements(possible_pattern, groups)

    return arrangement_count


def is_valid(pattern, groups):
    flex_pattern = [i for i in pattern.split(".") if i]
    for g in groups:
        # Go from left group to right and try to find if they fit in the patterns
        # If g is too big we need to discard patterns
        found_fit = False
        while not found_fit and len(flex_pattern) > 0:
            if g > len(flex_pattern[0]):
                # if any(c == "#" for c in flex_pattern[0]): # Cant discard something that is required
                #     return False
                flex_pattern.pop(0)
                continue
            found_fit = True
            # If match is exact, just remove
            if g == len(flex_pattern[0]):
                flex_pattern.pop(0)
                continue
            # Split at the earliest convinience
            fount_split = False
            for i in range(len(flex_pattern[0]) - g + 1):
                # Before and after must either be outside range or ?. If it is # it means its overlapping
                # print(i, g, len(flex_pattern[0]), flex_pattern[0])
                if ((i == 0 or flex_pattern[0][i - 1] == "?") and
                        (i + g >= len(flex_pattern[0]) or flex_pattern[0][i + g] == "?")):
                    fount_split = True
                    flex_pattern[0] = flex_pattern[0][i+g+1:]   # Leftover!!
                    if len(flex_pattern[0]) == 0:
                        flex_pattern.pop(0)
                    break
            if not fount_split:
                found_fit = False
                if any(c == "#" for c in flex_pattern[0]): # Cant discard something that is required
                    return False
                flex_pattern.pop(0)
        if not found_fit:
            return False

    # Find if there is any leftover requirements that are not fulfilled
    # for fp in flex_pattern:
    #     if any(c == "#" for c in fp):
    #         return False
    return True


def is_valid2(pattern, groups):
    pattern_group = [len(i) for i in pattern.split(".") if i]
    return pattern_group == groups

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
    example = """???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1"""
    a1 = 21
    a2 = 525152
    return validate_solution((s(example, 1), s(example, 2)), (a1, a2))

# 6203
# 7169!!!



main()
