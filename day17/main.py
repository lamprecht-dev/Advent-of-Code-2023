import sys
import heapq
sys.path.append('../')
from utils import *


def s(d, part):
    ll = lines(d)

    next = []
    seen = set()
    heapq.heappush(next, (0, ((0, 0), "r", 0)))  # weight, pos, dir, current_straight
    heapq.heappush(next, (0, ((0, 0), "d", 0)))  # weight, pos, dir, current_straight
    seen.add(((0, 0), "r", 0))
    seen.add(((0, 0), "d", 0))

    while len(next) > 0:
        weight, (pos, dir, dist) = heapq.heappop(next)
        p2_final_cond = part == 1 or 4 <= dist <= 10
        if pos == (len(ll[0]) - 1, len(ll) - 1) and p2_final_cond:
            return weight

        for d in dirs:
            if (d == "r" and dir == "l" or
                    d == "l" and dir == "r" or
                    d == "u" and dir == "d" or
                    d == "d" and dir == "u"):
                continue
            n = dirs[d][0] + pos[0], dirs[d][1] + pos[1]
            ndist = dist + 1 if d == dir else 1
            part1_cond = ndist > 3
            part2_cond = ndist > 10 or (dist < 4 and dir != d)
            part_cond = (part == 1 and part1_cond) or (part == 2 and part2_cond)
            inbound = 0 <= n[0] < len(ll[0]) and 0 <= n[1] < len(ll)
            if not inbound or part_cond or (n, d, ndist) in seen:
                continue
            heapq.heappush(next, (weight + int(ll[n[1]][n[0]]), (n, d, ndist)))
            seen.add((n, d, ndist))

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
    example = """2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533"""
    example2 = """111111111111
999999999991
999999999991
999999999991
999999999991"""
    a1 = 102
    a2 = 94
    a3 = 71
    return validate_solution((s(example, 1), s(example, 2), s(example2, 2)), (a1, a2, a3))


main()