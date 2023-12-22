import copy
import sys
import collections

sys.path.append('../')
from utils import *


def s(d):
    # Prep Lists
    bricks_by_height = collections.defaultdict(list)
    available_heights = set()
    ll = lines(d)
    for l in ll:
        b = [[int(b) for b in l1.split(",")] for l1 in l.split("~")]
        assert not (b[0][0] > b[1][0] or b[0][1] > b[1][1] or b[0][2] > b[1][2])    # Making sure its already sorted

        bricks_by_height[b[0][2]].append(b)
        available_heights.add(b[0][2])

    available_heights = list(available_heights)
    available_heights.sort()

    bricks_by_height, available_heights, _ = move_down(bricks_by_height, available_heights)
    all_shots = 0
    chain_reaction = 0

    for h in available_heights:
        for i in range(len(bricks_by_height[h])):
            bbh = copy.deepcopy(bricks_by_height)
            bbh[h].pop(i)

            _, _, count_move = move_down(bbh, available_heights)
            if count_move == 0:
                all_shots += 1
            else:
                chain_reaction += count_move

    return all_shots, chain_reaction


def move_down(bricks_by_height, available_heights):
    count_move = 0
    height_map = collections.defaultdict(int)
    bricks_by_height2 = collections.defaultdict(list)
    available_heights2 = set()

    for h in available_heights:
        for i in range(len(bricks_by_height[h])):
            b = bricks_by_height[h][i]
            diff = move_diff(b, height_map)
            if diff > 0:
                count_move += 1
            nb = [[*b[0][:2], b[0][2] - diff], [*b[1][:2], b[1][2] - diff]]
            bricks_by_height2[nb[0][2]].append(nb)
            available_heights2.add(nb[0][2])
            height_map = edit_height_map(nb, height_map)

    available_heights2 = list(available_heights2)
    available_heights2.sort()
    return bricks_by_height2, available_heights2, count_move


def edit_height_map(b, height_map):
    for x in range(b[0][0], b[1][0] + 1):
        for y in range(b[0][1], b[1][1] + 1):
            height_map[(x, y)] = max(height_map[(x, y)], b[1][2])
    return height_map


def move_diff(b, height_map):
    highest_point = 0
    for x in range(b[0][0], b[1][0] + 1):
        for y in range(b[0][1], b[1][1] + 1):
            highest_point = max(height_map[(x, y)], highest_point)

    return b[0][2] - highest_point - 1


def main():
    if test():
        file = inp(os.path.join(os.path.dirname(__file__), 'input.txt'))
        solutions = s(file)
        print("\n\n" + BColors.HEADER + "Solutions" + BColors.ENDC)
        for sol in solutions:
            print(sol)
    else:
        print("\n\n" + BColors.FAIL + "Not All Test Successful" + BColors.ENDC)


def test():
    example = """1,0,1~1,2,1
0,0,2~2,0,2
0,2,3~2,2,3
0,0,4~0,2,4
2,0,5~2,2,5
0,1,6~2,1,6
1,1,8~1,1,9"""
    a1 = 5
    a2 = 7
    return validate_solution(s(example), (a1, a2))


main()
