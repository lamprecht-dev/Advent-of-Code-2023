import sys
sys.path.append('../')
from utils import *


def s(d, part):
    total_arrangements = 0
    ll = lines(d)
    for r, line in enumerate(ll):
        pattern, groups = line.split()
        groups = tuple(ints(groups, ","))
        if part == 2:
            groups *= 5
            pattern = "?".join([pattern] * 5)
        arr = arrangements(pattern, groups)
        total_arrangements += arr

    return total_arrangements


cache = {}
def arrangements(pattern, groups):
    if len(groups) == 0:
        return not any([p == "#" for p in pattern])

    if len(pattern) == 0:
        return len(groups) == 0

    if (pattern, groups) in cache:
        return cache[(pattern, groups)]

    a_count = 0
    if pattern[0] == "." or pattern[0] == "?":
        a_count += arrangements(pattern[1:], groups)

    if pattern[0] == "?" or pattern[0] == "#":
        if (len(pattern) >= groups[0] and not any([pattern[g] == "." for g in range(groups[0])]) and
                (len(pattern) == groups[0] or pattern[groups[0]] != "#")):
            a_count += arrangements(pattern[groups[0] + 1:], groups[1:])

    cache[(pattern, groups)] = a_count
    return a_count


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


main()
