import sys
sys.path.append('../')
from utils import *


def s(d, part):
    blocks = d.split("\n\n")
    v, h = 0, 0
    for b in blocks:
        ll = lines(b)
        oldv = find_vert(ll)
        oldh = find_hor(ll)
        if part == 1:
            v += oldv or 0
            h += oldh or 0
            continue
        # Part 2 only
        changed = False
        for sm in range(len(ll) * len(ll[0])):
            smudge = get_smudge(ll, sm, part)
            fh = find_hor(smudge, oldh)
            fv = find_vert(smudge, oldv)
            if (fh == oldh and fv == oldv) or (fh is None is fv):
                continue

            changed = True
            if fv is None:
                h += fh or 0
                break
            if fh is None:
                v += fv or 0
                break
        if not changed:
            v += oldv or 0
            h += oldh or 0

    return 100 * h + v


def find_hor(block, ignore=None):
    for i in range(len(block) - 1):
        if ignore is not None and (i + 1) == ignore:
            continue
        if is_horizontal(block, i):
            return i + 1
    return None


def find_vert(block, ignore=None):
    for i in range(len(block[0]) - 1):
        if ignore is not None and (i + 1) == ignore:
            continue
        if is_vertical(block, i):
            return i + 1
    return None


def get_smudge(ll, index, part):
    if part == 1:
        return ll
    c = index // len(ll)
    r = index % len(ll)
    nll = ll[:]
    new_symbol = "#" if nll[r][c] == "." else "."
    nll[r] = nll[r][:c] + new_symbol + nll[r][c+1:]
    return nll


def is_vertical(pattern, location):
    pl = location
    pr = location + 1
    while pl >= 0 and pr < len(pattern[0]):
        for i in range(len(pattern)):
            if pattern[i][pl] != pattern[i][pr]:
                return False
        pl -= 1
        pr += 1
    return True


def is_horizontal(pattern, location):
    pt = location
    pb = location + 1
    while pt >= 0 and pb < len(pattern):
        if pattern[pt] != pattern[pb]:
            return False
        pt -= 1
        pb += 1
    return True


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
    example = """#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#"""
    a1 = 405
    a2 = 400
    return validate_solution((s(example, 1), s(example, 2)), (a1, a2))

main()
