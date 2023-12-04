from collections import defaultdict
from utils import *


def solve(d):
    scratch_score = 0
    total_cards = 0

    scratch_counts = defaultdict(int)

    ll = lines(d)
    for i, line in enumerate(ll):
        _, data = line.split(": ")
        winning, mine = data.split(" | ")
        winning = list(map(lambda x: int(x), winning.split()))
        mine = set(map(lambda x: int(x), mine.split()))
        count = sum(w in mine for w in winning)
        if count > 0:
            scratch_score += 2 ** (count - 1)

        scratch_counts[i] += 1
        for j in range(count):
            scratch_counts[i + j + 1] += scratch_counts[i]
            total_cards += scratch_counts[i]
        total_cards += 1

    return scratch_score, total_cards


def main():
    if test():
        solutions = solve(inp(os.path.join(os.path.dirname(__file__), 'input.txt')))
        print("\n\n" + BColors.HEADER + "Solutions" + BColors.ENDC)
        for s in solutions:
            print(s)
    else:
        print("\n\n" + BColors.FAIL + "Not All Test Successful" + BColors.ENDC)


def test():
    s = """Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11"""
    a1 = 13
    a2 = 30
    return validate_solution(solve(s), (a1, a2))


main()
