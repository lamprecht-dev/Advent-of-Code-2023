import collections
import functools
from utils import *

hand_values = ["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2", "1"]


def solve(d, part):
    global hand_values

    if part == 2:
        hand_values = ["A", "K", "Q", "T", "9", "8", "7", "6", "5", "4", "3", "2", "1", "J"]

    hands = []
    ww = words(d)
    for line in ww:
        hands.append((hand_type(line[0], part), line[0], int(line[1])))

    hands.sort(key=functools.cmp_to_key(sort_hand))

    return sum([(el[0] + 1) * el[1][2] for el in enumerate(hands)])


def sort_hand(a, b):
    global hand_values
    if a[0] > b[0]:
        return 1
    if a[0] < b[0]:
        return -1

    for i in range(5):
        if hand_values.index(a[1][i]) < hand_values.index(b[1][i]):
            return 1
        elif hand_values.index(a[1][i]) > hand_values.index(b[1][i]):
            return -1

    return 0


def hand_type(hand, part):
    # 5, 4, f, 3, 2p, 1p, h
    c = collections.Counter(hand)

    if part == 2:
        mc = c.most_common(5)
        if mc[0][0] != "J":
            c[mc[0][0]] += c['J']
            c["J"] = 0
        elif len(mc) > 1 and mc[1][0] != "J":
            c[mc[1][0]] += c['J']
            c["J"] = 0

    mc = c.most_common(2)

    if mc[0][1] == 3 and mc[1][1] == 2:
        return 4
    elif mc[0][1] == 2 and mc[1][1] == 2:
        return 2
    elif mc[0][1] > 3:
        return mc[0][1] + 1
    elif mc[0][1] == 3:
        return 3

    return mc[0][1] - 1


def main():
    if test():
        file = inp(os.path.join(os.path.dirname(__file__), 'input.txt'))
        solutions = (solve(file, 1), solve(file, 2))
        print("\n\n" + BColors.HEADER + "Solutions" + BColors.ENDC)
        for s in solutions:
            print(s)
    else:
        print("\n\n" + BColors.FAIL + "Not All Test Successful" + BColors.ENDC)


def test():
    s = """32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483"""
    a1 = 6440
    a2 = 5905
    return validate_solution((solve(s, 1), solve(s, 2)), (a1, a2))


main()
