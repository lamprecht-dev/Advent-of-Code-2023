import collections
import sys
sys.setrecursionlimit(1000000000)
sys.path.append('../')
from utils import *


def s(d, part):
    global dp
    dp = {}

    ll = lines(d)
    segments = set(get_segments((1, 0), (1, 0), (len(ll[1]) - 2, len(ll) - 1), ll, set(), set()))
    full_segments = set()
    for s in segments:
        full_segments.add(s)
        if part == 2:
            full_segments.add((s[1], s[0], s[2]))

    all_paths = find_paths((1, 0), (len(ll[1]) - 2, len(ll) - 1), full_segments, ())
    return max([sum([p[2] for p in ap]) for ap in all_paths])


def get_segments(start, first, end, ll, seen, crossings):
    segments = []
    next = collections.deque()
    next.append(start)
    cur_seg = [first]
    seen.add(first)
    # Run through grid checking for segments. Mostly there should be only one possibility,
    # but if we find multiple paths, we do recursion
    while len(next) > 0:
        cur = next.popleft()
        symbol = ll[cur[1]][cur[0]]
        # Find possible next steps after cur
        possible = []
        for d in dirs:
            n = (cur[0] + dirs[d][0], cur[1] + dirs[d][1])
            if n[0] >= len(ll[0]) or n[0] < 0 or n[1] >= len(ll) or n[1] < 0:
                continue
            symbol2 = ll[n[1]][n[0]]
            slope_restriction = ((symbol == ">" and d != "r") or (symbol == "<" and d != "l") or
                    (symbol == "^" and d != "u") or (symbol == "v" and d != "d"))
            if (symbol2 == "#" or slope_restriction):
                continue

            if n in cur_seg:
                continue
            possible.append(n)

        if len(possible) == 1:
            if cur not in cur_seg:
                cur_seg.append(cur)
            next.append(possible[0])
        elif len(possible) > 1 or cur == end:
            crossings.add(cur)
            segments.append((cur_seg[0], cur, len(cur_seg)))
            for p in possible:
                segments.extend(get_segments(p, cur, end, ll, seen, crossings))
        seen.add(cur)
    return segments


dp = {}
def find_paths(cur, end, segments, his):
    if (cur, his) in dp:
        return dp[(cur, his)]

    nexts = [seg for seg in segments if seg[0] == cur and seg not in his]
    paths = []
    for n in nexts:
        if n[1] in [h[0] for h in his]:
            continue
        if n[1] == end:
            paths.extend([[*his, n]])
        else:
            paths.extend(find_paths(n[1], end, segments, (*his, n)))

    dp[(cur, his)] = paths
    return paths


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
    example = """#.#####################
#.......#########...###
#######.#########.#.###
###.....#.>.>.###.#.###
###v#####.#v#.###.#.###
###.>...#.#.#.....#...#
###v###.#.#.#########.#
###...#.#.#.......#...#
#####.#.#.#######.#.###
#.....#.#.#.......#...#
#.#####.#.#.#########v#
#.#...#...#...###...>.#
#.#.#v#######v###.###v#
#...#.>.#...>.>.#.###.#
#####v#.#.###v#.#.###.#
#.....#...#...#.#.#...#
#.#########.###.#.#.###
#...###...#...#...#.###
###.###.#.###v#####v###
#...#...#.#.>.>.#.>.###
#.###.###.#.###.#.#v###
#.....###...###...#...#
#####################.#"""
    a1 = 94
    a2 = 154
    return validate_solution((s(example, 1), s(example, 2)), (a1, a2))


main()
