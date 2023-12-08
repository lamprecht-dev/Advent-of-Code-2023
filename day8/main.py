import pprint as pp

from utils import *


def s(d):
    ll = lines(d)
    ins = [0 if c == "L" else 1 for c in ll[0]]
    ins2 = []

    directions = {}

    for line in ll[2:]:
        direction = line.split(" = ")
        directions[direction[0]] = direction[1].strip("()").split(", ")

    steps = 0
    cur = "AAA"
    tar = "ZZZ"
    while cur != tar:
        i = ins.pop(0)
        cur = directions[cur][i]

        steps += 1
        ins2.append(i)
        if len(ins) == 0:
            ins = ins2

    return steps


def s2(d):
    ll = lines(d)
    ins = [0 if c == "L" else 1 for c in ll[0]]

    directions = {}

    for line in ll[2:]:
        direction = line.split(" = ")
        directions[direction[0]] = direction[1].strip("()").split(", ")

    zmap = {}
    gcur = {}

    for d in directions:
        phasemap = {}
        if d[2] == "Z" or d[2] == "A":
            seen = set()
            cur = d
            s = 0
            tempins = ins[:]
            tempins2 = []
            while True:
                t = tempins.pop(0)
                cur = directions[cur][t]

                if (s % len(ins), cur) in seen:
                    s = -1
                    break
                seen.add((s % len(ins), cur))

                s += 1
                tempins2.append(t)
                if len(tempins) == 0:
                    tempins = tempins2

                if cur[2] == "Z":
                    break

            if d[2] == "Z":
                zmap[d] = (s, cur, s % len(ins))

            if d[2] == "A":
                gcur[d] = (s, cur, s % len(ins))

    # pp.pprint(gcur)
    # pp.pprint(zmap['11Z'][0])

    # return general_solution_attempt(cur, zmap, len(inp))

    # This solution only works for the types of inputs we are getting.
    # We are trying to get the lowest common multiple

    return math.lcm(*[zmap[x][0] for x in zmap])


def general_solution_attempt(cur, zmap, phase_length):
    steps = 0

    while not in_sync(cur):
        smallest = None
        for i in cur:
            c = cur[i]
            if smallest is None or cur[smallest][0] > c[0]:
                smallest = i
        sv = cur[smallest]

        new_value = zmap[sv[1]][sv[0] % phase_length]
        cur[smallest] = (new_value[0] + sv[0], new_value[1])
        steps = new_value[0] + sv[0]

    return steps


def in_sync(states):
    first = None
    for s in states:
        st = states[s]
        if first is None:
            first = st[0]
        elif first != st[0]:
            return False
    return True

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
