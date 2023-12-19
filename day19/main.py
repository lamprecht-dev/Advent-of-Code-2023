import sys
import pprint as pp
sys.path.append('../')
from utils import *


def s(d, part):
    ins, pa = d.split("\n\n")
    ins = lines(ins)
    pa = lines(pa)

    instructions = {}
    for i in ins:
        name, actions = i.strip("}").split("{")
        instructions[name] = []
        for a in actions.split(","):
            ins_action = {'comp': None, "value": None, "comp_type": None, 'target': None}
            if ":" not in a:
                ins_action["target"] = a
            else:
                if ">" in a:
                    l, r = a.split(">")
                    m, t = r.split(":")
                    ins_action["target"] = t
                    ins_action["comp"] = ">"
                    ins_action["value"] = int(m)
                    ins_action["comp_type"] = l
                elif "<" in a:
                    l, r = a.split("<")
                    m, t = r.split(":")
                    ins_action["target"] = t
                    ins_action["comp"] = "<"
                    ins_action["value"] = int(m)
                    ins_action["comp_type"] = l
                else:
                    assert False
            instructions[name].append(ins_action)

    if part == 2:
        return sum([math.prod([a[1] - a[0] + 1 for a in r.values()]) for r in get_range(instructions, "in")])

    # Part 1 Only
    sum_ = 0
    for p in pa:
        d = {}
        for v in p.strip("{}").split(","):
            vs = v.split("=")
            d[vs[0]] = int(vs[1])
        if crawl(d, instructions):
            sum_ += sum(d.values())

    return sum_


def merge_range(a, b):
    merged = {}
    for k in a:
        b0 = b[k][0] if k in b else 0
        b1 = b[k][1] if k in b else 4000
        merged[k] = (max(a[k][0], b0), min(a[k][1], b1))
    return merged


def get_range(instructions, entry):
    # WORKING BACKWARDS
    if entry == "A":
        return [{'x': (0, 4000), 'm': (0, 4000), 'a': (0, 4000), 's': (0, 4000)}]

    valid_ranges = []
    current_range = {'x': (1, 4000), 'm': (1, 4000), 'a': (1, 4000), 's': (1, 4000)}
    # Walk through the actions and edit current_range as the access is getting more difficult
    for action in instructions[entry]:
        # If target is R we don't care but still have to update current_range
        if action['target'] == "R":
            if action["comp"] is not None:
                if action["comp"] == ">":
                    denied_value = {action['comp_type']: (1, action['value'])}
                else:
                    denied_value = {action['comp_type']: (action['value'], 4000)}
                current_range = merge_range(current_range, denied_value)
            continue

        # Two sub ranges: One for target reached, one for not reached
        # Next we want to look at what happens if we go into the next target.
        # We will receive their ranges and merge with ours and add
        sub_ranges = get_range(instructions, action['target'])
        for sub_range in sub_ranges:
            current_sub_range = merge_range(current_range, sub_range)
            if action["comp"] is None:
                # Just add
                valid_ranges.append(current_sub_range)
                continue

            if action["comp"] == ">":
                validate = {action['comp_type']: (action['value'] + 1, 4000)}
                valid_ranges.append(merge_range(current_sub_range, validate))
            elif action["comp"] == "<":
                validate = {action['comp_type']: (1, action['value'] - 1)}
                valid_ranges.append(merge_range(current_sub_range, validate))

        # Next we want to check out the opposite case and cary it down the line, so we just edit current_range
        if action["comp"] is not None:
            if action["comp"] == ">":
                denied_value = {action['comp_type']: (1, action['value'])}
            else:
                denied_value = {action['comp_type']: (action['value'], 4000)}
            current_range = merge_range(current_range, denied_value)

    return valid_ranges


def crawl(data, instructions):
    c_ins = "in"
    while c_ins not in ["R", "A"]:
        for a in instructions[c_ins]:
            if compare(a, data):
                c_ins = a['target']
                break
    return c_ins == "A"


def compare(action, el):
    if action["comp"] is None:
        return True

    if action["comp"] == ">":
        return el[action["comp_type"]] > int(action["value"])
    else:
        return el[action["comp_type"]] < int(action["value"])


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
    example = """px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}

{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}"""
    a1 = 19114
    a2 = 167409079868000
    return validate_solution((s(example, 1), s(example, 2)), (a1, a2))


main()

# 167 180 171 559 200
# 167 459 205 617 600

# 167 363 302 159 200
# 167 276 053 617 600

# 167 409 079 868 000