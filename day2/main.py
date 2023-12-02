import functools

from utils import *


def solve(d):
    ll = lines(d)
    limit = {"red": 12, "green": 13, "blue": 14}
    add_totals = 0
    power = 0

    for line in ll:
        (game, rest) = line.lstrip("Game ").split(": ")
        game = int(game)
        groups = list(map(lambda g: tuple(map(lambda v: v.split(" "), g.split(", "))), rest.split("; ")))
        valid = True
        fewest = {"red": 0, "blue": 0, "green": 0}

        for group in groups:
            count = {"red": 0, "blue": 0, "green": 0}
            for item in group:
                count[item[1]] += int(item[0])
                fewest[item[1]] = max(fewest[item[1]], int(item[0]))
            for key in count:
                if limit[key] < count[key]:
                    valid = False
                    break
        if valid:
            add_totals += game

        power += functools.reduce(lambda a, b: a*b, fewest.values())

    return add_totals, power


def main():
    if test():
        solutions = solve(inp(os.path.join(os.path.dirname(__file__), 'input.txt')))
        print("\n\n" + BColors.HEADER + "Solutions" + BColors.ENDC)
        for s in solutions:
            print(s)
    else:
        print("\n\n" + BColors.FAIL + "Not All Test Successful" + BColors.ENDC)


def test():
    s = """Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green"""
    a1 = 8
    a2 = 2286
    return validate_solution(solve(s), (a1, a2))


main()
