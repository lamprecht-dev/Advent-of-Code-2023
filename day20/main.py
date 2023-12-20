import sys
import collections
import datetime
import itertools
import functools
import math
from operator import itemgetter as ig
import pprint as pp
import re
# import bisect
# import heapq
# sys.setrecursionlimit(1000000)

sys.path.append('../')
from utils import *


def s(d, part):
    ll = lines(d)
    broadcaster_targets = []
    flip_flops = {}
    conjunctions = {}

    inputs = collections.defaultdict(list)
    for line in ll:
        action, target = line.split("->")
        if action.strip() == "broadcaster":
            broadcaster_targets = target.strip().split(", ")
        elif "%" in action:
            ts = target.strip().split(", ")
            for t in ts:
                inputs[t].append(action.strip()[1:])
            flip_flops[action.strip()[1:]] = {'targets': ts, 'state': "low"}
        elif "&" in action:
            ts = target.strip().split(", ")
            for t in ts:
                inputs[t].append(action.strip()[1:])
            conjunctions[action.strip()[1:]] = {"targets": ts, "in": {}}

    for co in conjunctions:
        for i in inputs[co]:
            conjunctions[co]["in"][i] = "low"

    # action: target, pulse
    pulse_sum = (0, 0)
    if part == 1:
        for i in range(1000):
            pulses, broadcaster_targets, flip_flops, conjunctions, rx = press_button(broadcaster_targets, flip_flops, conjunctions)
            pulse_sum = (pulse_sum[0] + pulses[0], pulse_sum[1] + pulses[1])
    else:
        i = 1
        while True:
            pulses, broadcaster_targets, flip_flops, conjunctions, rx = press_button(broadcaster_targets, flip_flops, conjunctions)
            if rx:
                return i
            i += 1

    return pulse_sum[0] * pulse_sum[1]


def press_button(broadcaster_targets, flip_flops, conjunctions):
    pulses = [0, 0]
    actions = collections.deque()
    actions.append(("broadcaster", "low", "button"))
    count_rx = 0
    while len(actions) > 0:
        a = actions.popleft()
        if a[0] == "rx":
            count_rx += 1
        if a[1] == "low":
            pulses[0] += 1
        else:
            pulses[1] += 1

        if a[0] == "broadcaster":
            for t in broadcaster_targets:
                actions.append((t, a[1], "broadcaster"))
            continue
        if a[1] == "low" and a[0] in flip_flops:
            flip_flops[a[0]]['state'] = "low" if flip_flops[a[0]]['state'] == "high" else "high"
            for t in flip_flops[a[0]]['targets']:
                actions.append((t, flip_flops[a[0]]['state'], a[0]))

        if a[0] in conjunctions:
            conjunctions[a[0]]['in'][a[2]] = a[1]
            all_high = all([conjunctions[a[0]]['in'][i] == "high" for i in conjunctions[a[0]]['in']])
            for t in conjunctions[a[0]]['targets']:
                actions.append((t, "low" if all_high else "high", a[0]))
    return pulses, broadcaster_targets, flip_flops, conjunctions, count_rx == 1


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
