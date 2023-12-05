from utils import *


def solve(d):
    state = 0

    last_values = []
    new_values = []

    ww = words(d)
    for line in ww:
        if len(line) == 0:
            state += 1
            for i in range(len(new_values)):
                if new_values[i] is None:
                    new_values[i] = last_values[i]
            last_values = new_values
            new_values = [None] * len(last_values)
            continue

        if state == 0:
            new_values = list(map(lambda x: int(x), line[1:]))
        elif state > 0:
            if not line[0].isnumeric():
                continue
            cto, cfrom, clen = int(line[0]), int(line[1]), int(line[2])
            for i, v in enumerate(last_values):
                if cfrom <= v < cfrom + clen:
                    new_values[i] = v + (cto - cfrom)

    for i in range(len(new_values)):
        if new_values[i] is None:
            new_values[i] = last_values[i]

    return min(new_values)


def solve2(d):
    state = 0

    values = []
    transformations = []

    ww = words(d)
    for line in ww:
        if len(line) == 0:
            state += 1
            if state > 1:
                values = process_step(transformations, values)
            transformations = []
            continue

        if state == 0:
            seeds = list(map(lambda x: int(x), line[1:]))
            for i in range(0, len(seeds), 2):
                values.append((seeds[i], seeds[i + 1]))
        elif state > 0:
            if not line[0].isnumeric():
                continue
            transformations.append((int(line[0]), int(line[1]), int(line[2])))

    values = process_step(transformations, values)

    return min(map(lambda x: x[0], values))


def split_range(original, transform):
    parts_transformed = []
    parts_not_transformed = []

    offset = transform[0] - transform[1]

    if original[0] + original[1] <= transform[1] or original[0] >= transform[1] + transform[2]:
        # No overlap
        parts_not_transformed.append(original)
    elif original[0] >= transform[1] and original[0] + original[1] <= transform[1] + transform[2]:
        # Full overlap
        parts_transformed = [(original[0] + offset, original[1])]
    elif transform[1] > original[0] and transform[1] + transform[2] < original[0] + original[1]:
        # Split both ways
        l1 = transform[1] - original[0]
        l2 = transform[2]
        l3 = original[1] - l1 - l2
        parts_not_transformed.append((original[0], l1))
        parts_transformed.append((transform[0], l2))
        parts_not_transformed.append((original[0] + l1 + l2, l3))
    elif original[0] >= transform[1]:
        # Trail is out
        l1 = transform[1] + transform[2] - original[0]
        parts_transformed.append((original[0] + offset, l1))
        parts_not_transformed.append((original[0] + l1, original[1] - l1))
    else:
        # Lead is out
        l1 = transform[1] - original[0]
        parts_not_transformed.append((original[0], l1))
        parts_transformed.append((original[0] + l1 + offset, original[1] - l1))

    return parts_transformed, parts_not_transformed


def process_step(transformations, values):
    new_values = []
    while len(values) > 0:
        v = values[0]
        did_transform = False
        for t in transformations:
            transformed, not_transformed = split_range(v, t)
            if len(transformed) > 0:
                did_transform = True
                new_values.extend(transformed)
                values.extend(not_transformed)
                break
        if not did_transform:
            new_values.append(v)  # Just enter unaltered values
        values.pop(0)

    return new_values


def main():
    if test():
        file = inp(os.path.join(os.path.dirname(__file__), 'input.txt'))
        solutions = (solve(file), solve2(file))
        print("\n\n" + BColors.HEADER + "Solutions" + BColors.ENDC)
        for s in solutions:
            print(s)
    else:
        print("\n\n" + BColors.FAIL + "Not All Test Successful" + BColors.ENDC)


def test():
    s = """seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4"""
    a1 = 35
    a2 = 46
    return validate_solution((solve(s), solve2(s)), (a1, a2))


main()
