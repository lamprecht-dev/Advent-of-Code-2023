import pprint as pp

from utils import *


def s(d):
    ll = lines(d)
    ins = [0 if c == "L" else 1 for c in ll[0]]

    directions = {}

    for line in ll[2:]:
        direction = line.split(" = ")
        directions[direction[0]] = direction[1].strip("()").split(", ")

    steps = 0
    ins_point = 0
    cur = "AAA"
    tar = "ZZZ"
    while cur != tar:
        i = ins[ins_point % len(ins)]
        cur = directions[cur][i]

        steps += 1
        ins_point += 1

    return steps


def s2(d):
    ll = lines(d)
    ins = [0 if c == "L" else 1 for c in ll[0]]

    directions = {}

    for line in ll[2:]:
        direction = line.split(" = ")
        directions[direction[0]] = direction[1].strip("()").split(", ")

    zmap = {}

    for d in directions:
        if d[2] == "Z":
            cur = d
            s = 0
            tempins = ins[:]
            temp_pointer = 0
            while True:
                t = tempins[temp_pointer % len(tempins)]
                cur = directions[cur][t]

                s += 1
                temp_pointer += 1

                if cur[2] == "Z":
                    break

            if d[2] == "Z":
                zmap[d] = (s, cur)

    # return general_solution_attempt(cur, zmap, len(inp))

    # This solution only works for the types of inputs we are getting.
    # We are trying to get the lowest common multiple

    return math.lcm(*[zmap[x][0] for x in zmap])


def main():
    if test():
        file = inp(os.path.join(os.path.dirname(__file__), 'input.txt'))
        solutions = (s(file), s2(file))
        print("\n\n" + BColors.HEADER + "Solutions" + BColors.ENDC)
        for sol in solutions:
            print(sol)
    else:
        print("\n\n" + BColors.FAIL + "Not All Test Successful" + BColors.ENDC)


def test():
    example = """LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)"""

    example2 = """LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)"""
    a1 = 6
    a2 = 6
    return validate_solution((s(example), s2(example2)), (a1, a2))


main()
