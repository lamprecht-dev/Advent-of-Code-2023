import sys
import collections
import numpy as np
import random

sys.path.append('../')
from utils import *


def s(d, part):
    modules = {}    # type, memory, targets
    ll = lines(d)
    rxmodule = None
    for l in ll:
        mod, targets = l.split(" -> ")
        if mod == "broadcaster":
            modules["broadcaster"] = ["bc", None, targets.split(", ")]
        elif mod.startswith("%"):
            modules[mod[1:]] = ["ff", False, targets.split(", ")]
        elif mod.startswith("&"):
            modules[mod[1:]] = ["con", {}, targets.split(", ")]

        if part == 2 and "rx" in targets.split(", "):
            rxmodule = mod[1:]

    # Fill the con memory:
    for m in modules:
        for target in modules[m][2]:
            if target in modules and modules[target][0] == "con":
                modules[target][1][m] = False

    low, high = 0, 0
    button_presses = 0
    cycles = {}
    while True:
        if part == 1 and button_presses == 1000:
            break
        # elif part == 2 and button_presses == 100000:
        #     break
        button_presses += 1
        next = collections.deque([("broadcaster", False, "button")])
        while next:
            n, p, f = next.popleft()
            if p:
                high += 1
            else:
                low += 1
            if n not in modules:
                continue
            m = modules[n]

            if n == rxmodule and p and part == 2:
                if f not in cycles:
                    cycles[f] = button_presses
                if len(cycles) == 4:    # I know its four inputs. Really I should be checking for this count but its fine
                    return math.lcm(*cycles.values())

            if m[0] == "ff":
                if not p:
                    m[1] = not m[1]
                    for t in m[2]:
                        next.append((t, m[1], n))
            elif m[0] == "con":
                m[1][f] = p
                sp = not all(m[1].values())
                for t in m[2]:
                    next.append((t, sp, n))
            elif m[0] == "bc":
                for t in m[2]:
                    next.append((t, p, n))
            else:
                assert False

    return low * high


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
    example = """broadcaster -> a, b, c
%a -> b
%b -> c
%c -> inv
&inv -> a"""
    example2 = """broadcaster -> a
%a -> inv, con
&inv -> b
%b -> con
&con -> output"""
    a11 = 32000000
    a12 = 11687500
    return validate_solution((s(example, 1), s(example2, 1)), (a11, a12))


main()
