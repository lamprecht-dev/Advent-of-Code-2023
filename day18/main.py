import sys
sys.path.append('../')
from utils import *


def s(d, part):
    ww = words(d)
    cur = (0, 0)
    verts = []
    b = 0
    for line in ww:
        if part == 1:
            d = dirs[line[0].lower()]
            dist = int(line[1])
        else:
            dir_names = ['r', 'd', 'l', 'u']
            hex = line[2].strip("()")
            d = dirs[dir_names[int(hex[-1])]]
            dist = int(hex[1:-1], 16)
        b += dist
        cur = (cur[0] + d[0] * dist, cur[1] + d[1]* dist)
        verts.append(cur)

    # Shoelace problem
    A = 0
    for i in range(len(verts)):
        before = verts[i - 1][1] if i > 0 else verts[-1][1]
        after = verts[i + 1][1] if i < len(verts) - 1 else verts[0][1]
        A += verts[i][0] * (after - before)
    A = abs(A / 2)

    # Picks Theorem
    # A = i + (b / 2) - 1
    i = A - (b / 2) + 1

    return int(b + i)


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
    example = """R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)"""
    a1 = 62
    a2 = 952408144115
    return validate_solution((s(example, 1), s(example, 2)), (a1, a2))

main()
